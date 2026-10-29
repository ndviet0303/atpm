"""Kiểm chứng tĩnh bo_sung_v1/source_v1 bằng đúng công cụ, rule và cấu hình đã dùng cho source_v0.

Dùng: python bo_sung_v1/check_v1.py <test>   với test thuộc
  kiem_ke, sast, bao_cao, phpstan, sql, auth, bo_nho_tinh, bo_nho_case
Mỗi test ghi bo_sung_v1/evidence_v1/<test>_v1.json (kèm số liệu v0 để đặt cạnh) và in tóm tắt.
Phi thực thi như phần v0: chỉ đọc mã, token và chạy công cụ phân tích tĩnh; không chạy PHP ứng dụng, không CSDL, không HTTP.
"""
from collections import Counter, deque
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
E = BASE / 'evidence'
OUT = HERE / 'evidence_v1'
V0, V1 = BASE / 'source_v0', HERE / 'source_v1'
LIB0, LIB1 = V0 / 'librarian', V1 / 'librarian'
ROOT = BASE.parents[1]
SEMGREP = os.environ.get('SEMGREP_BIN') or (str(ROOT / 'study/.venv/bin/semgrep') if (ROOT / 'study/.venv/bin/semgrep').exists()
                                            else shutil.which('semgrep'))
RULES = ['--config', 'evidence/frozen_registry_php_rules.json', '--config', 'evidence/custom_php_rules_corrected.yaml']
sys.path[:0] = [str(HERE), str(BASE / 'models')]
import make_v1  # noqa: E402  (chỉ dùng hằng và hàm patch, không ghi tệp)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):
    return json.loads(p.read_text(encoding='utf-8'))


def save(name, summary, detail=None):
    OUT.mkdir(exist_ok=True)
    (OUT / f'{name}_v1.json').write_text(json.dumps({**summary, **(detail or {})}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def semgrep(args):
    env = dict(os.environ, SEMGREP_SEND_METRICS='off', SEMGREP_ENABLE_VERSION_CHECK='0')
    run = subprocess.run([SEMGREP, 'scan', '--metrics', 'off', '--jobs', '1', '--no-git-ignore', *args],
                         cwd=BASE, env=env, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr[-2000:]


def rule_counts(data):
    return dict(Counter(r['check_id'].rsplit('.', 1)[-1] for r in data['results']))


def kiem_ke():
    files = sorted(LIB1.glob('*.php'))
    lint = {f.name: subprocess.run(['php', '-l', str(f)], capture_output=True).returncode for f in files}
    # source_v1 phải đúng là đầu ra của make_v1.py: sinh lại trong bộ nhớ rồi so từng tệp
    regen = {n: make_v1.NEW_FILES[n] for n in ('security.php', 'auth_guard.php')}
    for f in sorted(LIB0.glob('*.php')):
        regen[f.name] = make_v1.NEW_FILES.get(f.name) or make_v1.patch(f.name, f.read_text(encoding='utf-8', errors='surrogateescape'))
    same = [f.name for f in files if regen.get(f.name) == f.read_text(encoding='utf-8', errors='surrogateescape')]
    assert len(same) == len(files), sorted({f.name for f in files} - set(same))
    v0 = {f.name: sha(f) for f in LIB0.glob('*.php')}
    tokens = json.loads(subprocess.run(['php', str(E / 'static_inventory.php'), str(LIB1)],
                                       capture_output=True, text=True, check=True).stdout)
    schema = (V1 / 'db/eb_lms_v1.sql').read_text(encoding='utf-8')
    calls = Counter(c['name'] for t in tokens for c in t['calls'])
    save('kiem_ke', {
        'php_file_count': len(files), 'physical_lines': sum(len(f.read_text(errors='replace').splitlines()) for f in files),
        'lint_ok': sum(code == 0 for code in lint.values()),
        'files_changed_from_v0': sum(f.name in v0 and sha(f) != v0[f.name] for f in files),
        'files_added': [f.name for f in files if f.name not in v0],
        'make_v1_reproduced': f'{len(same)}/{len(files)}',
        'missing_includes': [dict(file=t['file'], **i) for t in tokens for i in t['includes'] if not i['exists']],
        'schema_engines': dict(re.findall(r'CREATE TABLE IF NOT EXISTS `([^`]+)`[\s\S]*?\) ENGINE=(\w+)', schema)),
        'mysql_ext_calls': sum(n for c, n in calls.items() if c.startswith('mysql_')),
        'function_calls': dict(calls.most_common(12)),
    }, {'lint': lint})


def sast():
    semgrep([*RULES, '--json', '--output', str(OUT / 'semgrep_v1.json'), str(LIB1.relative_to(BASE))])
    data, v0 = load(OUT / 'semgrep_v1.json'), load(E / 'semgrep_run1.json')
    save('sast', {'findings': len(data['results']), 'errors': len(data['errors']),
                  'scanned': len(data['paths']['scanned']), 'by_rule': rule_counts(data),
                  'v0_findings': len(v0['results']), 'v0_by_rule': rule_counts(v0)})


def bao_cao():
    names = {k: f'bao_cao_semgrep_v1.{k}' for k in ('txt', 'sarif', 'json')}
    semgrep([*RULES, f'--text-output={names["txt"]}', f'--sarif-output={names["sarif"]}', f'--json-output={names["json"]}',
             str(LIB1.relative_to(BASE))])
    data = load(BASE / names['json'])
    save('bao_cao', {'findings': len(data['results']), 'errors': len(data['errors']), 'files': list(names.values())})


def phpstan():
    run = subprocess.run(['php', '-d', 'memory_limit=1G', str(ROOT / 'study/phpstan.phar'), 'analyse', '-c',
                          str(HERE / 'phpstan_v1.neon'), '--error-format=json', '--no-progress'],
                         cwd=BASE, capture_output=True, text=True)
    assert run.returncode in (0, 1), run.stderr[-2000:]  # 1 = có thông báo
    data = json.JSONDecoder().raw_decode(run.stdout[run.stdout.index('{'):])[0]
    ids = Counter(m.get('identifier') for v in data['files'].values() for m in v['messages'])
    save('phpstan', {'file_errors': data['totals']['file_errors'], 'by_identifier': dict(ids),
                     'files': {Path(f).name: v['errors'] for f, v in data['files'].items()},
                     'stub_used': False, 'function_not_found': ids.get('function.notFound', 0)})


# Truy vấn v0 bị bỏ hẳn ở v1 (CWE-1050 gộp vào truy vấn danh sách; CWE-362 thay bằng mysqli_insert_id)
DROPPED = [('select * from category where category_id = ', 'gộp vào JOIN của truy vấn danh sách'),
           ('select * from borrowdetails where book_id', 'gộp vào truy vấn con đếm bản đang mượn'),
           ('select * from borrow order by borrow_id desc', 'thay bằng mysqli_insert_id trong giao dịch')]
DB_QUERY = re.compile(r'db_query\(\s*"((?:[^"\\]|\\.)*)"(?:\s*,\s*"(\w*)")?')


def sql():
    v1 = {}
    for f in sorted(LIB1.glob('*.php')):
        for m in DB_QUERY.finditer(f.read_text(encoding='utf-8', errors='surrogateescape')):
            v1.setdefault(f.name, []).append({'sql': ' '.join(m[1].split()), 'types': m[2] or '',
                                              'placeholders': m[1].count('?'), 'literal': '$' not in m[1]})
    calls = [c for cs in v1.values() for c in cs]
    assert all(c['literal'] and len(c['types']) == c['placeholders'] for c in calls)
    rows, left = [], {f: list(cs) for f, cs in v1.items()}
    for q in load(E / 'sql_inventory.json')['queries']:
        drop = next((why for key, why in DROPPED if key in ' '.join(q['sql'].lower().split())), None)
        c = None if drop else left[q['file']].pop(0)  # còn lại: cùng tệp, cùng thứ tự xuất hiện
        rows.append({'id': q['id'], 'file': q['file'], 'line': q['start_line'], 'v0_class': q['classification'],
                     'v0_fields': len(q['fields']), 'v1_sql': c and c['sql'],
                     'v1': drop or ('db_query có tham số' if c['placeholders'] else 'db_query chuỗi hằng')})
    kept = [r for r in rows if r['v0_fields'] and r['v1_sql']]
    save('sql', {'v1_db_query_calls': len(calls), 'literal_sql': f"{sum(c['literal'] for c in calls)}/{len(calls)}",
                 'parameterized_calls': sum(c['placeholders'] > 0 for c in calls),
                 'placeholders_bound': sum(c['placeholders'] for c in calls),
                 'v0_queries': len(rows), 'v0_to_v1': dict(Counter(r['v1'] for r in rows)),
                 'v0_with_fields_now_bound': f"{sum(r['v1'] == 'db_query có tham số' for r in kept)}/{len(kept)}",
                 'extra_v1_calls': {f: len(cs) for f, cs in left.items() if cs}},
         {'rows': rows})


def controls(lib):
    """Harness kiểm soát: guard trước CSDL ở 12 handler, handler đọc $_GET, form/hộp thoại tới handler có token, giao dịch mượn."""
    text = {f.name: f.read_text(encoding='utf-8', errors='surrogateescape') for f in lib.glob('*.php')}
    guard = text.get('auth_guard.php', '')
    guard_ok = bool(guard) and "!== 'POST'" in guard and 'csrf_verify' in guard and guard.index('session.php') < guard.index('dbcon.php')
    unguarded = []
    for h in make_v1.HANDLERS:
        t = text[h + '.php']
        g, db = t.find("require_once __DIR__ . '/auth_guard.php'"), re.search(r'\b(db_query|mysql_query)\(', t)
        if not (guard_ok and 0 <= g < (db.start() if db else len(t))):
            unguarded.append(h + '.php')
    # form tới handler: token phải nằm ngay sau thẻ <form>
    forms = [m[2] for t in text.values() for m in re.finditer(r'<form [^>]*action="(\w+)\.php"[^>]*>(.{0,40})', t)
             if m[1] in make_v1.HANDLERS]
    links = [f for f, t in text.items() for h in make_v1.HANDLERS if re.search(rf'href="{h}\.php', t)]
    borrow = text['borrow_save.php']
    return {'handlers_without_guard': f'{len(unguarded)}/{len(make_v1.HANDLERS)}', 'unguarded': unguarded,
            'handlers_reading_get': [h + '.php' for h in make_v1.HANDLERS if '$_GET' in text[h + '.php']],
            'get_links_to_write_handlers': len(links),
            'forms_to_handlers_without_token': f"{sum('csrf_field' not in f for f in forms)}/{len(forms)}",
            'self_post_modals_with_csrf_verify': f"{sum('csrf_verify' in text[f] for f in ('modal_add_user.php', 'modal_edit_user.php'))}/2",
            'borrow_id_by_order_by_desc': 'order by borrow_id desc' in borrow.lower(),
            'borrow_insert_id': 'mysqli_insert_id' in borrow, 'borrow_transaction': 'mysqli_begin_transaction' in borrow,
            'password_hash_calls': sum(t.count('password_hash(') for t in text.values()),
            'password_verify_calls': sum(t.count('password_verify(') for t in text.values())}


def kripke(unguarded):
    """Cùng cấu trúc Kripke với evidence/auth_model.py; cạnh unauthenticated → unauthorized_write chỉ còn khi có handler thiếu guard."""
    edges = {'unauthenticated': ['denied', 'authenticated'] + ['unauthorized_write'] * bool(unguarded),
             'denied': ['denied'], 'authenticated': ['authorized_write'],
             'authorized_write': ['authorized_write'], 'unauthorized_write': ['unauthorized_write']}
    labels = {'unauthenticated': [], 'denied': ['denied'], 'authenticated': ['authenticated'],
              'authorized_write': ['authenticated', 'write'], 'unauthorized_write': ['write', 'violation']}
    queue, seen, witness = deque([('unauthenticated', ['unauthenticated'])]), set(), None
    while queue:
        s, path = queue.popleft()
        if s in seen:
            continue
        seen.add(s)
        if 'write' in labels[s] and 'authenticated' not in labels[s] and witness is None:
            witness = path
        queue.extend((t, path + [t]) for t in edges[s])
    states = {s: t for s, t in edges.items() if s in seen}
    return {'initial_state': 'unauthenticated', 'states': states, 'labels': {s: labels[s] for s in states},
            'reachable': sorted(seen),
            'results': [{'formula': 'AG(write -> authenticated)', 'initial_satisfies': witness is None, 'counterexample': witness},
                        {'formula': 'EF(denied)', 'initial_satisfies': 'denied' in seen},
                        {'formula': 'EF(authenticated)', 'initial_satisfies': 'authenticated' in seen}]}


def auth():
    c0, c1 = controls(LIB0), controls(LIB1)
    model = kripke(c1['unguarded'])
    save('auth', {'v0': {k: v for k, v in c0.items() if k != 'unguarded'}, 'v1': {k: v for k, v in c1.items() if k != 'unguarded'},
                  'AG(write -> authenticated)': {'v0': kripke(c0['unguarded'])['results'][0]['initial_satisfies'],
                                                 'v1': model['results'][0]['initial_satisfies']}},
         {'scope': 'Cạnh của mô hình suy từ harness trên mã v1 (guard trước CSDL ở 12 handler); không chạy ứng dụng', **model})


def bo_nho_tinh():
    semgrep(['--config', 'evidence/memory_rules.yaml', '--json', '--output', str(OUT / 'memory_semgrep_v1.json'),
             str(LIB1.relative_to(BASE))])
    data = load(OUT / 'memory_semgrep_v1.json')
    v0 = load(E / 'memory_static_results.json')['semgrep']['by_group_rule'].get('baseline', {})
    save('bo_nho_tinh', {'findings': len(data['results']), 'by_rule': rule_counts(data),
                         'v0_findings': sum(v0.values()), 'v0_by_rule': {k.rsplit('.', 1)[-1]: n for k, n in v0.items()}})


def v1_tokens(tokens):
    """Ánh xạ API v1 về mô hình đã kiểm của bộ phân tích: db_query là cấp phát kết quả đã kiểm tra
    (MYSQLI_REPORT_STRICT ném ngoại lệ thay vì trả FALSE, như mysql_query ... or die); mysqli_* là hàm mysql_* cùng tên."""
    out, i = [], 0
    while i < len(tokens):
        t = tokens[i]
        if t[0] == 'T_STRING' and t[1] in ('mysqli_fetch_array', 'mysqli_num_rows'):
            t = [t[0], t[1].replace('mysqli_', 'mysql_'), t[2]]
        if t[0] == 'T_STRING' and t[1] == 'db_query':
            depth, j = 0, i + 1
            while True:  # tìm dấu ) đóng lời gọi rồi chèn "or exit"
                if tokens[j][0] == 'CHAR':
                    depth += {'(': 1, ')': -1}.get(tokens[j][1], 0)
                if depth == 0:
                    break
                j += 1
            out += [[t[0], 'mysql_query', t[2]], *tokens[i + 1:j + 1], ['T_LOGICAL_OR', 'or', t[2]], ['T_EXIT', 'exit', t[2]]]
            i = j + 1
            continue
        out.append(t)
        i += 1
    return out


def bo_nho_case():
    import memory_typestate as m
    entries = json.loads(subprocess.run(['php', str(E / 'extract_memory_tokens.php'), str(LIB1)],
                                        capture_output=True, text=True, check=True).stdout)
    tables, found, files, objs = m.schema(), [], 0, []
    for entry in entries:
        w = m.analyze_file({**entry, 'tokens': v1_tokens(entry['tokens'])}, tables,
                           label='source_v1/' + Path(entry['path']).name)
        found += [{'id': v['id'], 'file': Path(entry['path']).name, 'line': v['line'], 'var': v['var']} for v in w.violations]
        files += bool(w.violations)
        # chuỗi sự kiện từng đối tượng, để chon_test.py vẽ Kripke source_v1 như source_v0
        objs += [{'group': 'source_v1', 'obj': o.id, 'kind': o.kind,
                  'events': o.timeline} for o in w.objs.values()]
    v0 = [f for f in load(E / 'memory_case_results.json')['findings'] if f['file'].startswith('baseline/')]
    save('bo_nho_case', {'violations': len(found), 'files_with_violation': f'{files}/{len(entries)}',
                         'by_code': dict(Counter(f['id'] for f in found)),
                         'v0_violations': len(v0), 'v0_files_with_violation': f"{len({f['file'] for f in v0})}/66",
                         'v0_by_code': dict(Counter(f['id'] for f in v0))}, {'findings': found, 'objects': objs})


if __name__ == '__main__':
    assert V1.exists(), 'chưa có source_v1: chạy python bo_sung_v1/make_v1.py'
    {'kiem_ke': kiem_ke, 'sast': sast, 'bao_cao': bao_cao, 'phpstan': phpstan, 'sql': sql, 'auth': auth,
     'bo_nho_tinh': bo_nho_tinh, 'bo_nho_case': bo_nho_case}[sys.argv[1]]()
