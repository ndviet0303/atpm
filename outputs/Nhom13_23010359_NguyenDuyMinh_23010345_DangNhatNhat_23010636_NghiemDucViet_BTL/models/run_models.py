"""Static, manually translated models. Never executes PHP or database queries."""
from pathlib import Path
from itertools import product
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import sys

deps = Path(os.environ.get('Z3_DEPS', '/private/tmp/atpm-report-20261004/solver_deps'))
if deps.exists():
    sys.path.insert(0, str(deps))
import z3

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'evidence' / 'formal'
OUT.mkdir(parents=True, exist_ok=True)


def simplify(clauses, literal):
    return [[v for v in clause if v != -literal]
            for clause in clauses if literal not in clause]


def dpll(clauses, assignment=None, trace=None):
    """DPLL: unit propagation, pure literal elimination, then branching."""
    assignment = dict(assignment or {})
    trace = trace if trace is not None else []
    while True:
        if not clauses:
            return assignment
        if any(not c for c in clauses):
            trace.append({'event': 'conflict'})
            return None
        units = [c[0] for c in clauses if len(c) == 1]
        literals = {v for c in clauses for v in c}
        pure = sorted(v for v in literals if -v not in literals)
        if not units and not pure:
            break
        chosen = units[0] if units else pure[0]
        assignment[abs(chosen)] = chosen > 0
        trace.append({'event': 'unit' if units else 'pure', 'literal': chosen})
        clauses = simplify(clauses, chosen)
    variable = abs(clauses[0][0])
    for chosen in (variable, -variable):
        trace.append({'event': 'branch', 'literal': chosen})
        candidate = dict(assignment)
        candidate[variable] = chosen > 0
        result = dpll(simplify(clauses, chosen), candidate, trace)
        if result is not None:
            return result
    return None


def satisfies(clauses, assignment):
    return all(any(assignment.get(abs(lit), False) == (lit > 0)
                   for lit in clause) for clause in clauses)


def gate_cnf(output, inputs):
    # output <-> conjunction(inputs), with numeric variable identifiers.
    return [[-output, value] for value in inputs] + [[output] + [-v for v in inputs]]


def solve_cnf(name, names, clauses, expected, purpose, source):
    trace = []
    model = dpll(clauses, trace=trace)
    status = 'SAT' if model is not None else 'UNSAT'
    vars_z3 = {k: z3.Bool(v) for k, v in names.items()}
    solver = z3.Solver()
    for clause in clauses:
        solver.add(z3.Or(*[vars_z3[abs(v)] if v > 0 else z3.Not(vars_z3[abs(v)])
                          for v in clause]))
    z3_status = str(solver.check()).upper()
    exhaustive = next((dict(zip(names, vals))
                      for vals in product((False, True), repeat=len(names))
                      if satisfies(clauses, dict(zip(names, vals)))), None)
    truth_status = 'SAT' if exhaustive is not None else 'UNSAT'
    if model is not None:
        assert satisfies(clauses, model)
    assert status == z3_status == truth_status == expected
    dimacs = 'c ' + name + '\n' + ''.join(f'c {i} {n}\n' for i, n in names.items())
    dimacs += f'p cnf {len(names)} {len(clauses)}\n'
    dimacs += ''.join(' '.join(map(str, clause)) + ' 0\n' for clause in clauses)
    (OUT / (name + '.cnf')).write_text(dimacs)
    (OUT / (name + '.smt2')).write_text(solver.to_smt2())
    return {'id': name, 'purpose': purpose, 'source': source, 'variables': names,
            'clauses': clauses, 'dpll': status, 'z3_sat': z3_status,
            'truth_table': truth_status, 'dpll_trace': trace,
            'witness': {names[i]: model.get(i, False) for i in names} if model is not None else None}


def bool_cases():
    rows = []
    scenarios = [
        ('authentication', {1: 'grant', 2: 'row_exists', 3: 'password_valid'},
         gate_cnf(1, [2]), gate_cnf(1, [2, 3]), [[1], [-3]], [2, 3],
         'Cấp đăng nhập khi mật khẩu không hợp lệ', 'authentication.php'),
        ('authorization', {1: 'grant', 2: 'authenticated', 3: 'role_permitted'},
         [[1]], gate_cnf(1, [2, 3]), [[1], [-2, -3]], [2, 3],
         'Cho phép ghi khi thiếu phiên hoặc thiếu quyền', 'authorization.php'),
        ('database_query', {1: 'executed', 2: 'untrusted_input', 3: 'bound_parameter'},
         [[1], [-3]], [[1], [3]], [[1], [2], [-3]], [2, 3],
         'Đầu vào không tin cậy đi vào truy vấn chưa bind', 'database_query.php'),
        ('token_crypto', {1: 'accepted', 2: 'parsed', 3: 'tag_valid', 4: 'claims_valid'},
         gate_cnf(1, [2]), gate_cnf(1, [2, 3, 4]), [[1], [-3, -4]], [2, 3, 4],
         'Chấp nhận token chưa kiểm tra tag hoặc claims', 'token_crypto.php'),
        ('script_output', {1: 'emitted', 2: 'untrusted_text', 3: 'context_encoded'},
         [[1], [-3]], [[1], [3]], [[1], [2], [-3]], [2, 3],
         'Xuất chuỗi không tin cậy vào script chưa serialize', 'script_output.php'),
    ]
    for name, variables, before, after, violation, valid, purpose, file in scenarios:
        for version, relation, expected in [('_v0', before, 'SAT'), ('_v1', after, 'UNSAT')]:
            rows.append(solve_cnf(name + version, variables, relation + violation,
                                  expected, purpose, f'generated_cases/{version}/{file}'))
        rows.append(solve_cnf(name + '_valid_control', variables,
                              after + [[1]] + [[v] for v in valid], 'SAT',
                              'Đối chứng cho phép trường hợp hợp lệ', f'generated_cases/_v1/{file}'))
    # A separate nontrivial formula forces branching and conflicts; not a PHP claim.
    hard = [[1, 2], [1, -2], [-1, 2], [-1, -2]]
    rows.append(solve_cnf('dpll_branch_control', {1: 'p', 2: 'q'}, hard,
                          'UNSAT', 'Đối chứng nhánh và quay lui DPLL', 'models/run_models.py'))
    return rows


def smt_cases():
    code = (BASE / 'generated_cases/_v1/token_crypto.php').read_text()
    constants = {name: int(value) for name, value in re.findall(r'const (TOKEN_\w+_V1) = (\d+);', code)}
    assert constants == {'TOKEN_KEY_BYTES_V1': 32, 'TOKEN_NONCE_BYTES_V1': 12,
                         'TOKEN_TAG_BYTES_V1': 16, 'TOKEN_TTL_SECONDS_V1': 1800}
    key, nonce, tag, now, issued, expires, uid = z3.Ints('key_bytes nonce_bytes tag_bytes now iat exp uid')
    accepted, parsed, tag_ok, audience_ok = z3.Bools('accepted parsed tag_ok audience_ok')
    policy = z3.And(parsed, key == constants['TOKEN_KEY_BYTES_V1'],
                    nonce == constants['TOKEN_NONCE_BYTES_V1'],
                    tag == constants['TOKEN_TAG_BYTES_V1'], tag_ok, audience_ok,
                    uid > 0, issued >= 0, issued <= now, expires > now,
                    expires - issued <= constants['TOKEN_TTL_SECONDS_V1'])
    violations = [
        ('key_length', key != 32), ('nonce_length', nonce != 12),
        ('tag_length', tag != 16), ('expired', expires <= now),
        ('excess_ttl', expires - issued > 1800),
        ('future_iat', issued > now), ('identity_audience', z3.Or(uid <= 0, z3.Not(audience_ok))),
        ('invalid_tag', z3.Not(tag_ok)),
    ]
    rows = []
    tests = [('token_v0_counterexample', accepted == parsed,
              z3.And(key == 16, nonce == 16, tag == 0,
                     z3.Not(tag_ok), parsed, z3.Not(policy)), 'SAT')]
    tests += [('token_v1_' + name, accepted == policy, predicate, 'UNSAT')
              for name, predicate in violations]
    tests += [('token_v1_valid_control', accepted == policy,
               z3.And(key == 32, nonce == 12, tag == 16, tag_ok, audience_ok,
                      parsed, uid == 1, issued == 1000, now == 1100, expires == 2800), 'SAT')]
    allvars = [key, nonce, tag, now, issued, expires, uid, accepted, parsed, tag_ok, audience_ok]
    for name, relation, predicate, expected in tests:
        solver = z3.Solver()
        solver.add(relation, accepted, predicate, now >= 0, key >= 0, nonce >= 0, tag >= 0)
        status = str(solver.check()).upper()
        assert status == expected, (name, status)
        witness = None
        if status == 'SAT':
            model = solver.model()
            witness = {str(v): str(model.eval(v, model_completion=True)) for v in allvars}
        (OUT / (name + '.smt2')).write_text(solver.to_smt2())
        rows.append({'id': name, 'status': status, 'expected': expected,
                     'witness': witness, 'source': 'generated_cases/' + ('_v0' if '_v0_' in name else '_v1') + '/token_crypto.php'})
    return rows, constants


def main():
    boolean = bool_cases()
    arithmetic, constants = smt_cases()
    hashes = {str(p.relative_to(BASE)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted((BASE / 'generated_cases').rglob('*.php'))}
    result = {'timestamp': datetime.now(timezone.utc).isoformat(), 'z3_version': z3.get_full_version(),
              'model_kind': 'Manual abstraction of selected guards and policies; not automatic PHP semantics',
              'assumptions': [
                  'Prepared parameter binding isolates values from SQL syntax in the declared PDO environment.',
                  'password_verify correctly implements the password-valid predicate.',
                  'Server-side session values and role policy are trusted.',
                  'OpenSSL tag verification, JSON serialization and random_bytes are trusted primitives.',
                  'Models do not prove entropy, cipher security, unique nonces, replay protection or complete application security.'
              ],
              'boolean_cases': boolean, 'smt_cases': arithmetic,
              'php_constants_checked': constants, 'generated_source_sha256': hashes,
              'summary': {'boolean_cases': len(boolean), 'boolean_crosschecks_passed': len(boolean),
                          'smt_cases': len(arithmetic), 'smt_expected_passed': len(arithmetic)}}
    (BASE / 'evidence/formal_results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps({'z3_version': result['z3_version'], **result['summary']}, indent=2))


if __name__ == '__main__':
    main()
