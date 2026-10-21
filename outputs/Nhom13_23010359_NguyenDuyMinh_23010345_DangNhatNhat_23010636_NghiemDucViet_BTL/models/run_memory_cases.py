"""Memory study runner: typestate walk, Z3 bounded model check per object, SMT memory budget, C buffer-size SMT.
Reads PHP tokens and C text only. Never runs target PHP functions, binaries, DB or HTTP."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from itertools import product
import json
import z3
import memory_typestate as m

BASE = m.BASE
E = m.E
OUT = E / 'memory_formal'
OUT.mkdir(exist_ok=True)
# php.ini-development / php.ini-production default; mysqlnd buffers count against it
MEMORY_LIMIT = 128 * 1024 * 1024
GROUPS = [('baseline', 'source_v0/librarian', False),
          ('generated/_v0', 'generated_cases/_v0', True), ('generated/_v1', 'generated_cases/_v1', True),
          ('sql/_v0', 'generated_cases/sql/_v0', True), ('sql/_v1', 'generated_cases/sql/_v1', True),
          ('memory/_v0', 'generated_cases/memory/_v0', True), ('memory/_v1', 'generated_cases/memory/_v1', True)]
PATH_VIOLATIONS = ['E_USE_FALSE', 'E_ROW_UNCHECKED', 'E_USE_RELEASED', 'E_DOUBLE_RELEASE',
                   'E_HELD_TO_END', 'E_SECRET_RESIDUE']
SIDX = {s: i for i, s in enumerate(m.STATES)}
VIDX = {None: 0, **{v: i + 1 for i, v in enumerate(m.VIOLATIONS)}}


def walk():
    tables = m.schema()
    files = []
    for group, rel, php8 in GROUPS:
        for entry in m.tokens_for([BASE / rel]):
            name = Path(entry['path']).name
            files.append((group, m.analyze_file(entry, tables, php8=php8, label=f'{group}/{name}'), entry))
    return tables, files


def reachable(obj):
    """Brute force over every success/failure choice: violations some concrete path reaches."""
    choices = [i for i, ev in enumerate(obj.timeline) if ev in m.CHOICE_EVENTS]
    found = set()
    for bits in product((True, False), repeat=len(choices)):
        ok = dict(zip(choices, bits))
        state = 'UNDEF'
        for i, ev in enumerate(obj.timeline):
            state, violation = m.concrete_step(state, ev, ok.get(i, True), obj.kind)
            found.add(violation)
    return found - {None}


def bmc(obj, target=None):
    """Unrolled transition relation of concrete_step over the object's event sequence."""
    n = len(obj.timeline)
    s = [z3.Int(f's{i}') for i in range(n + 1)]
    ok = [z3.Bool(f'ok{i}') for i in range(n)]
    v = [z3.Int(f'v{i}') for i in range(n)]
    solver = z3.Solver()
    solver.add(s[0] == SIDX['UNDEF'])
    for i, ev in enumerate(obj.timeline):
        solver.add(z3.Or([z3.And(s[i] == SIDX[st], ok[i] == b, s[i + 1] == SIDX[nxt], v[i] == VIDX[vio])
                          for st in m.STATES for b in (True, False)
                          for nxt, vio in [m.concrete_step(st, ev, b, obj.kind)]]))
    goal = [x != 0 for x in v] if target is None else [x == VIDX[target] for x in v]
    solver.add(z3.Or(goal) if goal else z3.BoolVal(False))
    status = str(solver.check()).upper()
    witness = None
    if status == 'SAT':
        model = solver.model()
        names = {i: k for k, i in SIDX.items()}
        vnames = {i: k for k, i in VIDX.items()}
        witness = [{'event': ev, 'ok': z3.is_true(model.eval(ok[i], model_completion=True)),
                    'to': names[model[s[i + 1]].as_long()], 'violation': vnames[model[v[i]].as_long()]}
                   for i, ev in enumerate(obj.timeline)]
    return status, solver, witness


def check_objects(files):
    rows = []
    for group, w, _ in files:
        for obj in w.objs.values():
            abstract = {r['violation'] for r in w.trace if r['obj'] == obj.id and r['violation'] in PATH_VIOLATIONS}
            brute = reachable(obj)
            status, solver, witness = bmc(obj)
            per = {vid: bmc(obj, vid)[0] for vid in PATH_VIOLATIONS} if status == 'SAT' else {}
            z3_set = {vid for vid, st in per.items() if st == 'SAT'}
            assert z3_set == brute == abstract, (obj.id, obj.timeline, z3_set, brute, abstract)
            row = {'group': group, 'file': w.file, 'obj': obj.id, 'kind': obj.kind, 'var': obj.var,
                   'line': obj.line, 'events': obj.timeline, 'z3': status, 'violations': sorted(z3_set),
                   'witness': witness}
            if group.startswith('memory/'):
                path = OUT / (obj.id.replace('/', '_').replace('#', '_obj') + '_bmc.smt2')
                path.write_text(solver.to_smt2())
                row['smt2'] = str(path.relative_to(BASE))
            rows.append(row)
    return rows


def budget(files):
    """SAT: some row count N makes N * row_width exceed memory_limit. UNSAT: the SQL caps N below it."""
    rows, seen = [], set()
    for group, w, _ in files:
        for obj in w.objs.values():
            b = obj.bound
            # a query inside an unrolled loop yields one object per iteration: one budget per call site
            if not b or not b['select'] or (w.file, obj.line) in seen:
                continue
            seen.add((w.file, obj.line))
            width = b['row_width']
            rec = {'group': group, 'file': w.file, 'line': obj.line, 'var': obj.var, 'sql': b['sql'],
                   'bounded': b['bounded'], 'max_rows': b['max_rows'], 'row_width': width, 'reason': b['reason']}
            if width is None:
                rows.append({**rec, 'z3': 'UNKNOWN', 'note': 'Không suy ra được độ rộng dòng từ schema'})
                continue
            n = z3.Int('rows')
            opt = z3.Optimize()
            opt.add(n >= 0, n * width > MEMORY_LIMIT)
            if b['bounded']:
                opt.add(n <= b['max_rows'])
            opt.minimize(n)
            rec['z3'] = str(opt.check()).upper()
            if rec['z3'] == 'SAT':
                rec['min_rows_over_limit'] = opt.model()[n].as_long()
            assert rec['z3'] == ('UNSAT' if b['bounded'] else 'SAT'), rec
            if group.startswith('memory/'):
                path = OUT / f"{w.file.replace('/', '_')}_L{obj.line}_budget.smt2"
                path.write_text(opt.sexpr())
                rec['smt2'] = str(path.relative_to(BASE))
            rows.append(rec)
    return rows


def c_models():
    """Buffer-size formulas read off the C cases. v0 is pinned to its demo literal; v1 is for all inputs.
    ponytail: Int arithmetic, size_t wraparound is not modelled; the v1 guards keep sizes below 2^13."""
    L, n, lt, gt, amp, ulen = z3.Ints('len n lt gt amp ulen')
    user = 'librarian-account-with-a-very-long-name-0001'
    sql_id = "1' OR '1'='1' -- padding padding padding padding"
    fmt = "DELETE FROM book WHERE book_id='%s'"
    key = 'demo-fixed-key16-demo-fixed-key16'
    html = '<script>alert(1)</script>'
    models = [
        ('auth_name_copy', 'authentication.c', (12, 25), ['CWE-121', 'CWE-787'], user,
         'strcpy/memcpy username vào char name[32]: số byte ghi > 32',
         z3.And(L == len(user), L + 1 > 32),
         z3.And(L >= 0, ulen == z3.If(L < 32, L, 32), ulen != 32, ulen + 1 > 32)),
        ('query_format', 'database_query.c', (9, 21), ['CWE-122', 'CWE-787'], sql_id,
         'sprintf câu SQL vào malloc(64) / memcpy sizeof sql vào malloc(sizeof sql)',
         z3.And(L == len(sql_id), len(fmt) - 2 + L + 1 > 64),
         z3.And(n == len('DELETE FROM book WHERE book_id = ?') + 1, n > n)),
        ('key_copy', 'token_crypto.c', (10, 22), ['CWE-122', 'CWE-787'], key,
         'chép len byte khóa vào malloc(16) / chỉ chép khi len == 32 vào malloc(32)',
         z3.And(L == len(key), L > 16),
         z3.And(L == 32, L > 32)),
        ('tag_offset', 'token_crypto.c', (17, 38), ['CWE-127', 'CWE-125'], '"short"',
         'đọc 16 byte từ token + len - 16: lệch âm khi len < 16',
         z3.And(L == len('short'), L - 16 < 0),
         z3.And(L >= 16, L <= 4096, L - 16 < 0)),
        ('escape_size', 'script_output.c', (12, 20), ['CWE-122', 'CWE-787'], html,
         'đầu ra escape (+3 byte mỗi <, >, +4 mỗi &) vượt bộ đệm n+1 / 5n+1',
         z3.And(n == len(html), lt == html.count('<'), n + 3 * lt + 1 > n + 1),
         z3.And(n >= 0, n < 4096, lt >= 0, gt >= 0, amp >= 0, lt + gt + amp <= n,
                n + 3 * lt + 3 * gt + 4 * amp + 1 > 5 * n + 1)),
    ]
    rows = []
    for name, file, lines, cwe, literal, desc, v0, v1 in models:
        assert literal in (BASE / 'generated_cases/memory_c/_v0' / file).read_text(), (name, literal)
        for version, formula, line, expected in (('_v0', v0, lines[0], 'SAT'), ('_v1', v1, lines[1], 'UNSAT')):
            solver = z3.Solver()
            solver.add(formula)
            status = str(solver.check()).upper()
            assert status == expected, (name, version, status)
            path = OUT / f'c{version}_{name}.smt2'
            path.write_text(solver.to_smt2())
            rows.append({'model': name, 'file': f'memory_c/{version}/{file}', 'line': line, 'cwe': cwe,
                         'description': desc, 'z3': status, 'smt2': str(path.relative_to(BASE)),
                         'witness': {str(d): str(solver.model()[d]) for d in solver.model()} if status == 'SAT' else None})
    return rows


def main():
    tables, files = walk()
    traces = [{'file': w.file, 'path': str(Path(e['path']).relative_to(BASE)), 'sha256': e['sha256'],
               'objects': [{'id': o.id, 'kind': o.kind, 'var': o.var, 'line': o.line, 'sql': o.sql,
                            'final': o.state, 'events': o.timeline} for o in w.objs.values()],
               'trace': w.trace} for _, w, e in files]
    violations = [v for _, w, _ in files for v in w.violations]
    by_group = {}
    for group, w, _ in files:
        by_group.setdefault(group, Counter()).update(v['id'] for v in w.violations)
    memory = {w.file: [(v['id'], v['line'], v['var']) for v in w.violations]
              for g, w, _ in files if g.startswith('memory/')}
    assert all(memory[f] for f in memory if f.startswith('memory/_v0')), memory
    assert not any(memory[f] for f in memory if f.startswith('memory/_v1')), memory
    objects = check_objects(files)
    budgets = budget(files)
    c = c_models()
    for f in memory:
        sat = any(o['z3'] == 'SAT' for o in objects if o['file'] == f)
        assert sat == f.startswith('memory/_v0'), (f, sat)
    cwe = Counter(c for v in violations for c in v['cwe'])
    result = {
        'timestamp': datetime.now(timezone.utc).isoformat(), 'z3_version': z3.get_full_version(),
        'states': {k: {'id': p, 'meaning': d} for k, (p, d) in m.STATES.items()},
        'violations': {k: {'cwe': c_, 'severity': s, 'label': lbl} for k, (c_, s, lbl) in m.VIOLATIONS.items()},
        'transition_table': [{'from': a, 'event': b, 'to': nxt, 'violation': vio}
                             for (a, b), (nxt, vio) in m.TABLE.items()],
        'schema_row_width': {t: v['row_width'] for t, v in tables.items()},
        'summary': {'files': len(files), 'objects': len(objects),
                    'objects_z3_sat': sum(o['z3'] == 'SAT' for o in objects),
                    'z3_bruteforce_walker_agree': len(objects),
                    'by_group': {g: dict(c_) for g, c_ in by_group.items()},
                    'cwe_baseline': dict(Counter(c_ for v in violations if v['file'].startswith('baseline/')
                                                 for c_ in v['cwe'])),
                    'budget': {f'{g}:{s}': k for (g, s), k in Counter((r['group'], r['z3']) for r in budgets).items()},
                    'c_models': {f"{r['model']}{r['file'].split('/')[1]}": r['z3'] for r in c}},
        'memory_pairs': memory,
        'findings': violations,
        'objects': objects,
        'budget': budgets,
        'c_models': c,
        'assumptions': [
            'Phân tích tĩnh trên token PHP; không chạy hàm PHP, không kết nối CSDL, không gửi HTTP.',
            'Vòng lặp được trải 2 lần; mỗi lần gọi cấp phát/fetch có 2 nhánh thành công/thất bại.',
            'Độ rộng dòng lấy từ khai báo cột trong eb_lms.sql, không tính overhead zval/HashTable.',
            f'memory_limit = {MEMORY_LIMIT} byte (128M mặc định của php.ini).',
            'Mô hình C dùng số nguyên toán học, không mô hình tràn size_t.'],
    }
    (E / 'memory_traces.json').write_text(json.dumps(traces, ensure_ascii=False, indent=1))
    (E / 'memory_case_results.json').write_text(json.dumps(result, ensure_ascii=False, indent=1))
    print(json.dumps({**result['summary'], 'cwe_all': dict(cwe)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
