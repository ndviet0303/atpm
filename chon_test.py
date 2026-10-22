#!/usr/bin/env python3
"""Giao diện web nhỏ để chọn và chạy các bước phân tích tĩnh của gói BTL.
Dùng: python3 chon_test.py [cổng]   (mặc định 8790, tự mở http://127.0.0.1:8790)
Mỗi lần khởi động, gói nộp được chép lại vào run_output/goi_chay_lai/ và mọi test chạy trên bản sao đó,
nên evidence/ và checksums.json của gói nộp không bị ghi đè. Kết quả lần chạy trước trong bản sao bị xóa.
Chạy xong mỗi lượt, báo cáo HTML được ghi vào run_output/goi_chay_lai/bao_cao.html."""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import webbrowser
from collections import defaultdict
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
PKG = ROOT / 'outputs/Nhom13_23010359_NguyenDuyMinh_23010345_DangNhatNhat_23010636_NghiemDucViet_BTL'
WORK = ROOT / 'run_output/goi_chay_lai'  # cùng độ sâu với outputs/<gói> nên các script vẫn tìm thấy study/
VENV = ROOT / 'study/.venv/bin'
PY = str(VENV / 'python') if (VENV / 'python').exists() else sys.executable
SEMGREP = str(VENV / 'semgrep') if (VENV / 'semgrep').exists() else shutil.which('semgrep') or 'semgrep'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8790
HOSTS = {f'127.0.0.1:{PORT}', f'localhost:{PORT}'}
E = 'evidence/'
CUSTOM, REGISTRY = E + 'custom_php_rules_corrected.yaml', E + 'frozen_registry_php_rules.json'
RULES = ['--config', REGISTRY, '--config', CUSTOM]  # như run_sast.py

# (id, nhóm, tên, lệnh chạy trong bản sao, kết quả kỳ vọng theo README của gói, mã thoát coi là đạt)
TESTS = [
    ('kiem_ke', 'Static testing', 'Kiểm kê nguồn: số tệp, số dòng, lint PHP', [PY, E + 'collect_static.py'],
     '66 tệp, 2978 dòng; lint 66/66', {0}),
    ('sast', 'Static testing', 'Semgrep SAST, quét 2 lần', [PY, E + 'run_sast.py'],
     '322 hit mỗi lần, trùng 322/322 chữ ký; nguồn không đổi', {0}),
    ('bao_cao', 'Static testing', 'Semgrep xuất .txt, .sarif, .json',
     [SEMGREP, 'scan', '--metrics', 'off', '--no-git-ignore', *RULES, '--text-output=bao_cao_semgrep.txt',
      '--sarif-output=bao_cao_semgrep.sarif', '--json-output=bao_cao_semgrep.json', 'source_v0/librarian'],
     '322 kết quả', {0}),
    ('phpstan', 'Static testing', 'PHPStan level 0',
     ['php', '-d', 'memory_limit=1G', str(ROOT / 'study/phpstan.phar'), 'analyse', '-c', 'tools/phpstan.neon',
      '--error-format=json', '--no-progress'],
     '17 thông báo trên 16 tệp; mã 1 nghĩa là có thông báo', {0, 1}),
    ('ma_sinh', 'Mã sinh và hình thức', 'Mã sinh _v0/_v1: lint và Semgrep', [PY, E + 'run_generated_static.py'],
     '8 hit ở _v0, 0 hit ở _v1; lint 10/10', {0}),
    ('sat_smt', 'Mã sinh và hình thức', 'DPLL/SAT và SMT token', [PY, 'models/run_models.py'],
     '16/16 CNF trùng DPLL, Z3, bảng chân trị; 10/10 SMT đúng kỳ vọng', {0}),
    ('sql', 'Mã sinh và hình thức', '54 truy vấn SQL: CNF, SMT, mã sinh', [PY, 'models/run_sql_cases.py'],
     '162/162 CNF, 552/552 SMT; lint 109/109; 54 hit _v0, 0 hit _v1', {0}),
    ('auth', 'Mã sinh và hình thức', 'Mô hình xác thực', [PY, E + 'auth_model.py'],
     'AG(write -> authenticated) sai, có phản ví dụ', {0}),
    ('so_ho_so', 'Mã sinh và hình thức', 'Sổ hồ sơ test case', [PY, 'models/build_case_register.py'],
     '816 hồ sơ: 22 tổng hợp, 54 SQL, 178 SAT, 562 SMT', {0}),
    ('bo_nho_unit', 'Bộ nhớ', 'Unit test bộ phân tích trạng thái', [PY, 'models/test_memory_typestate.py', '-v'],
     '19/19 unit test đạt', {0}),
    ('bo_nho_tinh', 'Bộ nhớ', 'Semgrep bộ nhớ, Clang, GCC (Docker)', [PY, E + 'run_memory_static.py'],
     '167 hit; GCC lỗi ở 5/5 tệp C _v0, Clang 4/5, _v1 sạch', {0}),
    ('bo_nho_case', 'Bộ nhớ', 'Trạng thái, BMC, ngân sách, bộ đệm C', [PY, 'models/run_memory_cases.py'],
     '96 vi phạm trên 27/66 tệp; BMC 250/250, 92 SAT', {0}),
]
# File rule/cấu hình mà mỗi test nạp; giao diện hiện thành link để mở khi bị hỏi
RULE_FILES = {'sast': [CUSTOM, REGISTRY], 'bao_cao': [CUSTOM, REGISTRY], 'phpstan': ['tools/phpstan.neon'],
              'ma_sinh': [E + 'generated_case_rules.yaml'], 'sql': [E + 'generated_case_rules.yaml'],
              'bo_nho_tinh': [E + 'memory_rules.yaml']}
# Mã kiểm thử và tệp kết quả của mỗi test (ngoài script trong lệnh chạy); thư mục kết thúc bằng /
VIEW = {'kiem_ke': [E + 'static_summary.json', E + 'source_inventory.json', E + 'php_lint.json'],
        'sast': [E + 'semgrep_run1.json', E + 'semgrep_run2.json', E + 'sast_manifest.json'],
        'bao_cao': ['bao_cao_semgrep.txt', 'bao_cao_semgrep.sarif', 'bao_cao_semgrep.json'],
        'phpstan': ['source_v0/librarian/'],
        'ma_sinh': ['generated_cases/_v0/', 'generated_cases/_v1/', E + 'generated_static_results.json'],
        'sat_smt': [E + 'formal/', E + 'formal_results.json'],
        'sql': ['generated_cases/sql/', E + 'sql_formal/', E + 'sql_inventory.json', E + 'sql_case_results.json'],
        'auth': [E + 'auth_model.json'],
        'so_ho_so': [E + 'case_register.json'],
        'bo_nho_tinh': ['generated_cases/memory_c/', E + 'memory_static_results.json'],
        'bo_nho_case': ['generated_cases/memory/', E + 'memory_formal/', E + 'memory_case_results.json']}
# Rule Semgrep → phát hiện trong sổ phát hiện (Bảng 26 của báo cáo)
FINDS = {'php-direct-mysql-query-taint': 'FIND-01/03', 'tainted-sql-string': 'FIND-01/03', 'echoed-request': 'FIND-04',
         'php-hardcoded-db-credentials': 'FIND-08', 'php-legacy-mysql-extension': 'FIND-09',
         'php-mysql-error-information-disclosure': 'FIND-10'}
assert all((PKG / part).exists() for t in TESTS for part in t[3] if part.endswith('.py')), 'thiếu script trong gói'
assert all((PKG / f).exists() for files in RULE_FILES.values() for f in files), 'thiếu file rule trong gói'
assert all((PKG / f).exists() for files in VIEW.values() for f in files if not f.startswith('bao_cao_')), 'thiếu tệp kết quả'

state = {'running': None, 'result': {}, 'report': None}
log_lines = []
outputs = {}  # id → stdout của lần chạy gần nhất, dùng cho báo cáo
lock = threading.Lock()


def esc(value):
    return html.escape('' if value is None else str(value))


def log(text):
    with lock:
        log_lines.append(text)


def set_result(tid, result):
    with lock:
        state['result'][tid] = result


def run(ids):
    env = dict(os.environ, SEMGREP_BIN=SEMGREP, PYTHONUNBUFFERED='1')
    try:
        for tid, _, title, cmd, _, ok in [t for t in TESTS if t[0] in ids]:
            state['running'] = tid
            set_result(tid, {'status': 'running'})
            log(f'\n===== {title}\n$ {" ".join(Path(c).name if c in (PY, SEMGREP) else c for c in cmd)}\n')
            start, code, lines = time.time(), None, []
            try:
                proc = subprocess.Popen(cmd, cwd=WORK, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                        text=True, encoding='utf-8', errors='replace')
                for line in proc.stdout:
                    lines.append(line)
                    log(line)
                code = proc.wait()
            except OSError as error:  # thiếu php, semgrep hoặc phar
                lines.append(f'{error}\n')
                log(f'{error}\n')
            outputs[tid] = ''.join(lines)
            secs = round(time.time() - start, 1)
            set_result(tid, {'status': 'ok' if code in ok else 'fail', 'code': code, 'secs': secs})
            log(f'----- mã thoát {code}, {secs} giây\n')
        try:
            (WORK / 'bao_cao.html').write_text(build_report(), encoding='utf-8')
            state['report'] = datetime.now().strftime('%H:%M:%S')
            log(f'\n===== Đã xuất báo cáo: {WORK / "bao_cao.html"}\n')
        except Exception as error:  # báo cáo hỏng không được làm mất kết quả đã chạy
            log(f'\nLỗi khi dựng báo cáo: {error!r}\n')
    finally:
        state['running'] = None


# ---------- Báo cáo HTML: đọc JSON mà chính các test vừa ghi trong bản sao ----------

def load(rel):
    try:
        return json.loads((WORK / rel).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None


def passed(tid):
    return state['result'].get(tid, {}).get('status') == 'ok'


def src_line(path, line):
    for base in (WORK, ROOT):  # Semgrep ghi đường dẫn tương đối theo nơi quét, PHPStan ghi tuyệt đối
        try:
            return (base / path).read_text(encoding='utf-8', errors='replace').splitlines()[line - 1].strip()[:160]
        except (OSError, IndexError):
            pass
    return ''


def phpstan_data():
    text = outputs.get('phpstan', '')
    start = re.search(r'^\{', text, re.M)  # bỏ các dòng "Note: ..." PHPStan in ra stderr trước JSON
    try:
        return json.JSONDecoder().raw_decode(text[start.start():])[0] if start else None
    except ValueError:
        return None


def unit_tests():
    return re.findall(r'^(test\w+) \(([\w.]+)\)[^\n]*? \.\.\. (\w+)', outputs.get('bo_nho_unit', ''), re.M)


def table(head, rows):
    th = ''.join(f'<th>{h}</th>' for h in head)
    return f'<div class="scroll"><table><tr>{th}</tr>{"".join(rows)}</table></div>'


def tr(*cells):
    return '<tr>' + ''.join(cells) + '</tr>'


def td(value, cls=''):
    return f'<td class="{cls}">{esc(value)}</td>' if cls else f'<td>{esc(value)}</td>'


def code(value):
    return f'<td><code>{esc(value)}</code></td>'


def details(count, title, note, body):
    return (f'<details><summary><span class="count">{count}</span><b>{title}</b>{note}</summary>'
            f'<div class="scroll">{body}</div></details>')


def tags(*values):
    return ''.join(f'<span class="tag">{esc(v)}</span>' for v in values if v)


def actual(tid):
    """Một dòng số liệu thực tế của test, để đặt cạnh cột kỳ vọng."""
    if tid == 'kiem_ke':
        d = load(E + 'static_summary.json')
        return f"{d['php_file_count']} tệp, {d['physical_lines']} dòng; lint {d['lint_ok']}/{d['php_file_count']}"
    if tid == 'sast':
        d, m = load(E + 'semgrep_run1.json'), load(E + 'sast_manifest.json')
        rep = m['repeatability']
        return (f"{len(d['results'])} hit, {len(d['errors'])} errors; trùng {rep['signature_count']} chữ ký"
                f"{'' if rep['identical'] else ' (KHÁC NHAU)'}; nguồn {'không đổi' if m['source_unchanged'] else 'ĐÃ ĐỔI'}")
    if tid == 'bao_cao':
        d = load('bao_cao_semgrep.json')
        return f"{len(d['results'])} kết quả, {len(d['errors'])} errors"
    if tid == 'phpstan':
        d = phpstan_data()
        return f"{d['totals']['file_errors']} thông báo trên {len(d['files'])} tệp"
    if tid == 'ma_sinh':
        d = load(E + 'generated_static_results.json')
        lint = [x for r in d['runs'] for x in r['lint']]
        return '; '.join(f"{r['findings']} hit ở {r['version']}" for r in d['runs']) + \
            f"; lint {sum(x['exit_code'] == 0 for x in lint)}/{len(lint)}"
    if tid == 'sat_smt':
        s = load(E + 'formal_results.json')['summary']
        return (f"{s['boolean_crosschecks_passed']}/{s['boolean_cases']} CNF trùng; "
                f"{s['smt_expected_passed']}/{s['smt_cases']} SMT đúng kỳ vọng")
    if tid == 'sql':
        s = load(E + 'sql_case_results.json')['summary']
        return (f"{s['query_cnf_crosschecks_passed']}/{s['query_cnf_cases']} CNF, "
                f"{s['field_smt_expected_passed']}/{s['field_smt_cases']} SMT; lint {s['generated_sql_lint']}; "
                f"{s['generated_v0_rule_hits']} hit _v0, {s['generated_v1_rule_hits']} hit _v1")
    if tid == 'auth':
        d = load(E + 'auth_model.json')
        return '; '.join(f"{r['formula']}: {'đúng' if r['initial_satisfies'] else 'sai'}" for r in d['results'])
    if tid == 'so_ho_so':
        s = load(E + 'case_register.json')['summary']
        return (f"{s['total_cases']} hồ sơ: {s['overview_cases']} tổng hợp, {s['sql_source_cases']} SQL, "
                f"{s['sat_cases']} SAT, {s['smt_cases']} SMT")
    if tid == 'bo_nho_unit':
        found = unit_tests()
        return f"{sum(s == 'ok' for *_, s in found)}/{len(found)} unit test đạt"
    if tid == 'bo_nho_tinh':
        d = load(E + 'memory_static_results.json')
        runs = d['compilers']['runs']
        dirty = lambda tool, ver: sum(1 for r in runs if r['tool'] == tool and r['file'].startswith(ver) and r['findings'])
        n = sum(1 for r in runs if r['tool'] == 'gcc' and r['file'].startswith('_v0/'))
        v1 = dirty('gcc', '_v1/') + dirty('clang', '_v1/')
        return (f"{d['semgrep']['findings']} hit; GCC lỗi ở {dirty('gcc', '_v0/')}/{n} tệp _v0, "
                f"Clang {dirty('clang', '_v0/')}/{n}; _v1 {'sạch' if not v1 else f'còn lỗi ở {v1} lượt'}")
    if tid == 'bo_nho_case':
        d = load(E + 'memory_case_results.json')
        base = [f for f in d['findings'] if f['file'].startswith('baseline/')]
        s = d['summary']
        return (f"{len(base)} vi phạm trên {len({f['file'] for f in base})} tệp; "
                f"BMC {s['z3_bruteforce_walker_agree']}/{s['objects']}, {s['objects_z3_sat']} SAT")
    return '—'


def semgrep_rules(data):
    by_rule = defaultdict(list)
    for r in data['results']:
        by_rule[r['check_id'].rsplit('.', 1)[-1]].append(r)
    blocks = []
    for rule, hits in sorted(by_rule.items(), key=lambda kv: -len(kv[1])):
        extra = hits[0]['extra']
        cwe = extra.get('metadata', {}).get('cwe', [])
        cwe = ', '.join(c.split(':')[0] for c in ([cwe] if isinstance(cwe, str) else cwe))
        rows = [tr(td(f'{Path(h["path"]).name}:{h["start"]["line"]}', 'loc'), code(src_line(h['path'], h['start']['line'])))
                for h in hits]
        note = tags(extra['severity'], cwe) + f'<span class="tag find">{esc(FINDS.get(rule, "—"))}</span>' + \
            f'<div class="muted">{esc(extra["message"])}</div>'
        blocks.append(details(len(hits), esc(rule), note, f'<table class="locs">{"".join(rows)}</table>'))
    return len(by_rule), ''.join(blocks)


def sec_kiem_ke():
    d, inv = load(E + 'static_summary.json'), load(E + 'source_inventory.json')
    miss = [tr(td(f'{m["file"]}:{m["line"]}', 'loc'), code(m['path'])) for m in d['missing_includes']]
    files = [tr(td(f['file'], 'loc'), td(f['lines'], 'num'), code(f['sha256'])) for f in inv]
    return (f'{d["php_file_count"]} tệp PHP, {d["physical_lines"]} dòng ({d["blank_lines"]} dòng trống), lint '
            f'{d["lint_ok"]}/{d["php_file_count"]}; tệp rỗng: {esc(", ".join(d["empty_files"]))}; '
            f'checklist {d["checklist_count"]} mục.',
            '<h3>Include trỏ tới tệp không tồn tại</h3>' + table(['Vị trí', 'Tệp được include'], miss) +
            details(len(files), 'tệp nguồn: số dòng, SHA-256', '', table(['Tệp', 'Dòng', 'SHA-256'], files)))


def sec_sast():
    m = load(E + 'sast_manifest.json')
    n, blocks = semgrep_rules(load(E + 'semgrep_run1.json'))
    rep = m['repeatability']
    return (f'Hai lần quét trùng {rep["signature_count"]} chữ ký (chỉ ở lần 1: {rep["only_run1"]}, chỉ ở lần 2: '
            f'{rep["only_run2"]}); nguồn {"không đổi" if m["source_unchanged"] else "ĐÃ ĐỔI"}. {n} rule có hit; bấm vào rule '
            f'để xem vị trí và dòng mã. Rule ở <code>{CUSTOM}</code> (4 rule tự viết) và <code>{REGISTRY}</code> (24 rule registry).',
            blocks)


def sec_bao_cao():
    links = ' · '.join(f'<a href="/{f}">{f}</a>' for f in VIEW['bao_cao'])
    if passed('sast'):
        return f'Ba định dạng: {links}. Phát hiện theo rule xem ở mục Semgrep SAST.', ''
    n, blocks = semgrep_rules(load('bao_cao_semgrep.json'))
    return f'Ba định dạng: {links}. {n} rule có hit; bấm vào rule để xem vị trí và dòng mã.', blocks


def sec_phpstan():
    d = phpstan_data()
    rows = [tr(td(f'{Path(f).name}:{m["line"]}', 'loc'), td(m['message']), code(m.get('identifier')))
            for f, v in sorted(d['files'].items()) for m in v['messages']]
    return (f'{d["totals"]["file_errors"]} thông báo, cấu hình <code>tools/phpstan.neon</code>.',
            table(['Vị trí', 'Thông báo', 'Mã'], rows))


def sec_ma_sinh():
    d = load(E + 'generated_static_results.json')
    files = [tr(td(r['version']), td(f, 'loc'), td(n, 'num')) for r in d['runs'] for f, n in sorted(r['by_file'].items())]
    rules = [tr(td(r['version']), code(k.rsplit('.', 1)[-1]), td(n, 'num')) for r in d['runs'] for k, n in sorted(r['by_rule'].items())]
    return ('; '.join(f'{r["version"]}: {r["findings"]} hit' for r in d['runs']) +
            '. Mã nguồn ở <a href="/generated_cases/_v0/">generated_cases/_v0/</a> và '
            '<a href="/generated_cases/_v1/">generated_cases/_v1/</a>.',
            '<h3>Theo tệp</h3>' + table(['Bản', 'Tệp', 'Hit'], files) + '<h3>Theo rule</h3>' + table(['Bản', 'Rule', 'Hit'], rules))


def sec_sat_smt():
    d = load(E + 'formal_results.json')
    sat = [tr(code(c['id']), td(c['purpose']), td(c['dpll']), td(c['z3_sat']), td(c['truth_table'])) for c in d['boolean_cases']]
    smt = [tr(code(c['id']), td(c['expected']), td(c['status']), code(c['source'])) for c in d['smt_cases']]
    return (f'{esc(d["z3_version"])}. Tệp CNF/SMT-LIB ở <a href="/evidence/formal/">evidence/formal/</a>.',
            '<h3>Bài toán SAT (CNF)</h3>' + table(['ID', 'Mục đích', 'DPLL', 'Z3', 'Bảng chân trị'], sat) +
            '<h3>Bài toán SMT</h3>' + table(['ID', 'Kỳ vọng', 'Z3', 'Nguồn'], smt))


def sec_sql():
    s, inv = load(E + 'sql_case_results.json')['summary'], load(E + 'sql_inventory.json')
    rows = [tr(code(q['id']), td(f'{q["file"]}:{q["start_line"]}', 'loc'), td(q['operation']), td(q['classification']),
               code((q.get('sql') or q.get('argument') or '')[:160])) for q in inv['queries']]
    return (f'{s["queries"]} truy vấn, {s["fields"]} field; {s["query_cnf_crosschecks_passed"]}/{s["query_cnf_cases"]} CNF, '
            f'{s["field_smt_expected_passed"]}/{s["field_smt_cases"]} SMT. Mã sinh ở '
            '<a href="/generated_cases/sql/">generated_cases/sql/</a>, công thức ở <a href="/evidence/sql_formal/">evidence/sql_formal/</a>.',
            details(len(rows), 'truy vấn trong mã gốc', '', table(['ID', 'Vị trí', 'Loại', 'Phân loại', 'SQL'], rows)))


def sec_auth():
    d = load(E + 'auth_model.json')
    rows = [tr(code(r['formula']), td('đúng' if r['initial_satisfies'] else 'sai'), td(' → '.join(r.get('counterexample', []))))
            for r in d['results']]
    return (f'{esc(d["scope"])} Trạng thái đạt tới: {esc(", ".join(d["reachable"]))}.',
            table(['Công thức', 'Từ trạng thái đầu', 'Phản ví dụ'], rows))


def sec_so_ho_so():
    d = load(E + 'case_register.json')
    s, rows, start, blocks = d['summary'], d['master_rows'], 0, []
    for name, n in [('test case tổng hợp (TC)', s['overview_cases']), ('hồ sơ nguồn SQL', s['sql_source_cases']),
                    ('bài toán SAT/CNF', s['sat_cases']), ('bài toán SMT', s['smt_cases'])]:
        body = [tr(code(r[0]), td(r[1], 'loc'), td(r[2]), td(r[6]), td(r[7]), td(r[8], 'muted')) for r in rows[start:start + n]]
        blocks.append(details(n, name, '', table(['ID', 'Yêu cầu', 'Tên', 'Mức', 'Kết quả', 'Bằng chứng'], body)))
        start += n
    return (f'{s["total_cases"]} hồ sơ, cùng nội dung sheet TestCase trong Excel; bấm từng nhóm để xem.', ''.join(blocks))


def sec_bo_nho_unit():
    found = unit_tests()
    rows = [tr(code(name), td(cls.split('.')[-2] if '.' in cls else cls), td(status)) for name, cls, status in found]
    return ('Mã test ở <a href="/models/test_memory_typestate.py">models/test_memory_typestate.py</a>, chạy với <code>-v</code>.',
            table(['Unit test', 'Nhóm', 'Kết quả'], rows))


def sec_bo_nho_tinh():
    d = load(E + 'memory_static_results.json')
    rows = [tr(td(f'{r["file"]}:{f.get("line", "")}', 'loc'), td(r['tool']), code(f.get('rule')),
               td(', '.join(f.get('cwe', [])) or '—'), td(f.get('message')))
            for r in sorted(d['compilers']['runs'], key=lambda r: (r['file'], r['tool'])) for f in r['findings']]
    clean = sum(1 for r in d['compilers']['runs'] if r['file'].startswith('_v1/') and not r['findings'])
    groups = tags(*(f'{g}: {sum(v.values())}' for g, v in d['semgrep']['by_group_rule'].items()))
    return (f'{clean} lượt phân tích trên _v1 không có kết quả. Mã C ở <a href="/generated_cases/memory_c/">generated_cases/memory_c/</a>. '
            f'Semgrep bộ nhớ: {d["semgrep"]["findings"]} hit (rule ở <code>{E}memory_rules.yaml</code>) theo nhóm: {groups}',
            table(['Vị trí', 'Công cụ', 'Rule', 'CWE', 'Thông báo'], rows))


def sec_bo_nho_case():
    d = load(E + 'memory_case_results.json')
    by_kind = defaultdict(list)
    for f in d['findings']:
        if f['file'].startswith('baseline/'):
            by_kind[f['id']].append(f)
    blocks = []
    for kind, items in sorted(by_kind.items(), key=lambda kv: -len(kv[1])):
        rows = [tr(td(f'{Path(f["file"]).name}:{f["line"]}', 'loc'), code(f['var']), code(f['stmt'][:140])) for f in items]
        note = tags(items[0]['severity'], ', '.join(items[0]['cwe'])) + f'<div class="muted">{esc(items[0]["label"])}</div>'
        blocks.append(details(len(items), esc(kind), note, f'<table class="locs">{"".join(rows)}</table>'))
    total = sum(map(len, by_kind.values()))
    return (f'{total} vi phạm trên {len({f["file"] for v in by_kind.values() for f in v})} tệp baseline, theo mô hình '
            f'{len(d["states"])} trạng thái và {len(d["transition_table"])} phép chuyển. Mã case ở '
            '<a href="/generated_cases/memory/">generated_cases/memory/</a>.', ''.join(blocks))


SECTIONS = {'kiem_ke': sec_kiem_ke, 'sast': sec_sast, 'bao_cao': sec_bao_cao, 'phpstan': sec_phpstan, 'ma_sinh': sec_ma_sinh,
            'sat_smt': sec_sat_smt, 'sql': sec_sql, 'auth': sec_auth, 'so_ho_so': sec_so_ho_so,
            'bo_nho_unit': sec_bo_nho_unit, 'bo_nho_tinh': sec_bo_nho_tinh, 'bo_nho_case': sec_bo_nho_case}
assert set(SECTIONS) == {t[0] for t in TESTS}, 'test chưa có mục báo cáo'


def build_report():
    ran = [t for t in TESTS if state['result'].get(t[0], {}).get('status') in ('ok', 'fail')]
    rows, sections = [], []
    for tid, group, title, _, expect, _ in ran:
        r = state['result'][tid]
        ok = r['status'] == 'ok'
        try:
            got = esc(actual(tid)) if ok else f'<pre>{esc("".join(outputs.get(tid, "").splitlines(True)[-12:]))}</pre>'
            intro, body = SECTIONS[tid]() if ok else ('Test lỗi, xem log ở cột Thực tế của bảng tổng hợp.', '')
        except Exception as error:  # JSON thiếu trường: báo trong mục đó, không làm hỏng cả báo cáo
            got = intro = f'Không đọc được kết quả: {esc(repr(error))}'
            body = ''
        rows.append(f'<tr><td><a href="#{tid}"><b>{esc(title)}</b></a><div class="muted">{esc(group)}</div></td>'
                    f'<td><span class="status {r["status"]}">{"Đạt" if ok else "Lỗi"}</span></td>'
                    f'<td>{esc(expect)}</td><td>{got}</td><td class="num">{r["code"]}</td><td class="num">{r["secs"]}</td></tr>')
        sections.append(f'<section id="{tid}"><h2>{esc(title)}</h2>'
                        f'<p class="muted">{intro}</p>{body}</section>')
    n_ok = sum(state['result'][t[0]]['status'] == 'ok' for t in ran)
    return (REPORT.replace('__TIME__', datetime.now().strftime('%d/%m/%Y %H:%M'))
            .replace('__SUMMARY__', f'{n_ok}/{len(ran)} test đạt')
            .replace('__ROWS__', ''.join(rows)).replace('__DETAILS__', ''.join(sections)))


REPORT = '''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Báo cáo kiểm thử tĩnh – Nhóm 13</title>
<style>
:root { --bg:#f6f4ef; --card:#fbfaf7; --line:#ddd6c8; --text:#13202e; --muted:#4f5a66; --accent:#a84a14; --link:#1f5c99;
  --ok:#1f6b3a; --ok-bg:#e3f1e7; --fail:#b3261e; --fail-bg:#fbe6e4; --code:#efeae0; }
@media (prefers-color-scheme: dark) { :root { --bg:#10161d; --card:#18212b; --line:#2c3845; --text:#e8edf2; --link:#7fb2e5;
  --muted:#a9b4bf; --accent:#f08a3c; --ok:#5fc27e; --ok-bg:#16301f; --fail:#ff8a80; --fail-bg:#3a1a18; --code:#0f151c; } }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--text); font:15px/1.5 system-ui, sans-serif; }
main { max-width:1180px; margin:0 auto; padding:32px 16px 64px; }
a { color:var(--link); }
h1 { font-size:26px; margin:0; } h2 { font-size:19px; margin:40px 0 4px; color:var(--accent); } h3 { font-size:15px; margin:18px 0 6px; }
section { scroll-margin-top:16px; }
.muted { color:var(--muted); font-size:13px; }
.head { display:flex; flex-wrap:wrap; justify-content:space-between; gap:12px; align-items:end;
  border-bottom:2px solid var(--accent); padding-bottom:14px; }
.big { font-size:22px; font-weight:700; }
button { font:inherit; padding:7px 14px; border-radius:8px; border:1px solid var(--line); background:var(--card); color:var(--text); cursor:pointer; }
.scroll { overflow-x:auto; }
table { width:100%; border-collapse:collapse; background:var(--card); font-size:14px; }
th, td { text-align:left; vertical-align:top; padding:7px 10px; border-bottom:1px solid var(--line); }
th { font-size:12px; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); }
td.num { text-align:right; font-variant-numeric:tabular-nums; }
.status { display:inline-block; padding:2px 10px; border-radius:999px; font-weight:600; font-size:13px; white-space:nowrap; }
.status.ok { color:var(--ok); background:var(--ok-bg); } .status.fail { color:var(--fail); background:var(--fail-bg); }
code, pre { font:12.5px/1.45 ui-monospace, Menlo, monospace; }
code { background:var(--code); padding:1px 5px; border-radius:4px; word-break:break-word; }
pre { margin:0; white-space:pre-wrap; max-height:220px; overflow:auto; }
details { background:var(--card); border:1px solid var(--line); border-radius:10px; margin:8px 0; }
summary { cursor:pointer; padding:10px 14px; display:flex; flex-wrap:wrap; gap:6px 10px; align-items:baseline; }
summary .muted { flex-basis:100%; }
.count { min-width:44px; font-weight:700; font-variant-numeric:tabular-nums; color:var(--accent); }
.tag { font-size:12px; padding:1px 8px; border:1px solid var(--line); border-radius:999px; color:var(--muted); margin-right:4px; }
.tag.find { color:var(--accent); border-color:var(--accent); }
td.loc { white-space:nowrap; font-family:ui-monospace, Menlo, monospace; font-size:12.5px; }
td:first-child code { white-space:nowrap; word-break:normal; }
@media print { button { display:none; } body { background:#fff; } details { break-inside:avoid-page; } }
</style></head><body><main>
<div class="head"><div><h1>Báo cáo kiểm thử tĩnh – Nhóm 13</h1>
<div class="muted">Hệ thống quản lý thư viện (librarian, 66 tệp PHP). Chỉ phân tích mã nguồn, không chạy ứng dụng hay CSDL. Tạo lúc __TIME__.</div></div>
<div><div class="big">__SUMMARY__</div>
<button onclick="document.querySelectorAll('details').forEach(d => d.open = true)">Mở hết</button>
<button onclick="document.querySelectorAll('details').forEach(d => d.open = true); print()">In / lưu PDF</button></div></div>
<h2>Tổng hợp</h2><p class="muted">Cột thực tế đọc từ JSON mà chính lần chạy này ghi ra; cột kỳ vọng lấy theo README của gói. Bấm tên test để tới mục chi tiết.</p>
<div class="scroll"><table><tr><th>Test</th><th>Kết quả</th><th>Kỳ vọng</th><th>Thực tế</th><th>Mã</th><th>Giây</th></tr>__ROWS__</table></div>
__DETAILS__
</main></body></html>
'''


class Handler(SimpleHTTPRequestHandler):
    TEXT = 'text/plain; charset=utf-8'  # mở rule, mã nguồn và báo cáo ngay trong trình duyệt thay vì tải về
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, **dict.fromkeys(
        ['.yaml', '.neon', '.txt', '.py', '.php', '.c', '.h', '.cnf', '.smt2', '.md'], TEXT), '.sarif': 'application/json'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WORK), **kwargs)  # các đường dẫn khác = tệp trong bản sao

    def log_message(self, *args):
        pass

    def send_body(self, body, kind):
        self.send_response(200)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == '/':
            tests = [{'id': t[0], 'group': t[1], 'title': t[2], 'expect': t[4], 'rules': RULE_FILES.get(t[0], []),
                      'view': [p for p in t[3] if p.endswith('.py')] + VIEW.get(t[0], [])} for t in TESTS]
            data = json.dumps(tests, ensure_ascii=False).replace('</', '<\\/')
            page = PAGE.replace('__TESTS__', data).replace('__WORK__', str(WORK.relative_to(ROOT)))
            self.send_body(page.encode(), 'text/html; charset=utf-8')
        elif url.path == '/api/state':
            start = int(parse_qs(url.query).get('from', ['0'])[0])
            with lock:
                data = {'running': state['running'], 'result': state['result'], 'report': state['report'],
                        'log': ''.join(log_lines[start:]), 'next': len(log_lines)}
                body = json.dumps(data, ensure_ascii=False).encode()
            self.send_body(body, 'application/json; charset=utf-8')
        else:
            super().do_GET()

    def do_POST(self):
        # Chỉ nhận JSON từ chính trang này: trang khác không gửi được lệnh chạy (preflight, kiểm Host chống DNS rebinding)
        if (self.path != '/api/run' or self.headers.get('Content-Type') != 'application/json'
                or self.headers.get('Host') not in HOSTS):
            return self.send_error(400)
        wanted = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'{}').get('ids', [])
        ids = [t[0] for t in TESTS if t[0] in wanted]
        with lock:
            started = bool(ids) and state['running'] is None
            if started:
                state['running'] = ids[0]
        if started:
            threading.Thread(target=run, args=(ids,), daemon=True).start()
        self.send_body(json.dumps({'started': started}).encode(), 'application/json')


PAGE = '''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chọn test – Nhóm 13</title>
<style>
:root { --bg:#f6f4ef; --card:#fbfaf7; --line:#ddd6c8; --text:#13202e; --muted:#4f5a66; --accent:#a84a14;
  --ok:#1f6b3a; --fail:#b3261e; --run:#1f5c99; --log-bg:#13202e; --log-text:#dfe6ee; }
@media (prefers-color-scheme: dark) { :root { --bg:#10161d; --card:#18212b; --line:#2c3845; --text:#e8edf2;
  --muted:#a9b4bf; --accent:#f08a3c; --ok:#5fc27e; --fail:#ff8a80; --run:#7fb2e5; --log-bg:#0b1016; } }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--text); font:15px/1.45 system-ui, sans-serif; }
main { max-width:1280px; margin:0 auto; padding:24px 16px; display:grid; gap:20px; grid-template-columns:minmax(0,5fr) minmax(0,6fr); }
header { grid-column:1/-1; }
h1 { font-size:22px; margin:0 0 4px; }
.muted { color:var(--muted); font-size:13px; }
a { color:var(--run); }
h2 { font-size:13px; text-transform:uppercase; letter-spacing:.06em; color:var(--accent); margin:16px 0 6px; }
label.test { display:grid; grid-template-columns:auto 1fr auto; gap:4px 10px; align-items:start; background:var(--card);
  border:1px solid var(--line); border-radius:10px; padding:10px 12px; margin-bottom:6px; cursor:pointer; }
label.test input { margin-top:3px; }
.expect { grid-column:2/4; color:var(--muted); font-size:13px; word-break:break-word; }
.badge { font-size:12px; white-space:nowrap; padding:2px 8px; border-radius:999px; border:1px solid var(--line); color:var(--muted); }
.badge.ok { color:var(--ok); border-color:var(--ok); } .badge.fail { color:var(--fail); border-color:var(--fail); }
.badge.running { color:var(--run); border-color:var(--run); }
.actions { display:flex; flex-wrap:wrap; gap:8px; margin:12px 0; align-items:center; }
button, a.button { font:inherit; padding:8px 14px; border-radius:8px; border:1px solid var(--line); background:var(--card);
  color:var(--text); cursor:pointer; text-decoration:none; }
button.primary { background:var(--accent); border-color:var(--accent); color:#fff; font-weight:600; }
a.button.report { border-color:var(--ok); color:var(--ok); font-weight:600; }
button:disabled { opacity:.5; cursor:default; }
pre { margin:0; background:var(--log-bg); color:var(--log-text); border-radius:10px; padding:14px; height:calc(100vh - 170px);
  min-height:320px; overflow:auto; font:12.5px/1.45 ui-monospace, Menlo, monospace; white-space:pre-wrap; word-break:break-word; }
@media (max-width: 860px) { main { grid-template-columns:1fr; } pre { height:60vh; } }
</style></head><body><main>
<header><h1>Chọn test phân tích tĩnh – Nhóm 13</h1>
<div class="muted">Chạy trên bản sao <code>__WORK__</code>, không ghi đè gói nộp. Chạy xong sẽ có báo cáo HTML.
Tệp kết quả: <a href="/evidence/" target="_blank">evidence/</a> · <a href="/generated_cases/" target="_blank">generated_cases/</a></div></header>
<section><div class="actions">
<button class="primary" id="run">Chạy các test đã chọn</button>
<button id="all">Chọn tất cả</button><button id="none">Bỏ chọn</button>
<a class="button report" id="report" href="/bao_cao.html" target="_blank" hidden>Mở báo cáo</a></div>
<div id="list"></div></section>
<section><pre id="log" aria-live="polite">Chọn test rồi bấm “Chạy các test đã chọn”.</pre></section>
</main><script>
const TESTS = __TESTS__;
const list = document.getElementById('list'), log = document.getElementById('log'), runBtn = document.getElementById('run');
const report = document.getElementById('report');
const link = (href, text) => `<a href="/${href}" target="_blank">${text}</a>`;
const name = p => p.replace(/\\/$/, '').split('/').pop() + (p.endsWith('/') ? '/' : '');
let group = null, from = 0, started = false;
for (const t of TESTS) {
  if (t.group !== group) { group = t.group; list.insertAdjacentHTML('beforeend', `<h2>${group}</h2>`); }
  list.insertAdjacentHTML('beforeend', `<label class="test"><input type="checkbox" value="${t.id}">
    <span>${t.title}</span><span class="badge" id="b-${t.id}">Chưa chạy</span>
    <span class="expect">Kỳ vọng: ${t.expect}</span>
    ${t.rules.length ? `<span class="expect">Rule: ${t.rules.map(f => link(f, f)).join(' · ')}</span>` : ''}
    <span class="expect">Xem: ${t.view.map(f => link(f, name(f))).join(' · ')}${t.view.length ? ' · ' : ''}<a class="rep" hidden
      href="/bao_cao.html#${t.id}" target="_blank">mục trong báo cáo</a></span></label>`);
}
const boxes = () => [...list.querySelectorAll('input')];
document.getElementById('all').onclick = () => boxes().forEach(b => b.checked = true);
document.getElementById('none').onclick = () => boxes().forEach(b => b.checked = false);
runBtn.onclick = async () => {
  const ids = boxes().filter(b => b.checked).map(b => b.value);
  if (!ids.length) { alert('Chưa chọn test nào.'); return; }
  runBtn.disabled = true;
  for (const id of ids) setBadge(id, {status: 'queued'});
  await fetch('/api/run', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ids})});
};
function setBadge(id, r) {
  const b = document.getElementById('b-' + id);
  b.className = 'badge ' + r.status;
  b.textContent = {queued: 'Đang chờ', running: 'Đang chạy…', ok: `Đạt · mã ${r.code} · ${r.secs} s`,
    fail: `Lỗi · mã ${r.code} · ${r.secs} s`}[r.status];
}
async function poll() {
  try {
    const s = await (await fetch('/api/state?from=' + from)).json();
    from = s.next;
    if (s.log) { if (!started) { log.textContent = ''; started = true; } log.textContent += s.log; log.scrollTop = log.scrollHeight; }
    for (const [id, r] of Object.entries(s.result)) {
      setBadge(id, r);
      if (s.report && r.status !== 'running') document.querySelector(`a.rep[href$="#${id}"]`).hidden = false;
    }
    runBtn.disabled = s.running !== null;
    if (s.report) { report.hidden = false; report.textContent = `Mở báo cáo (${s.report})`; }
  } catch (e) { runBtn.disabled = true; }
  setTimeout(poll, 1000);
}
poll();
</script></body></html>
'''

if __name__ == '__main__':
    try:
        server = ThreadingHTTPServer(('127.0.0.1', PORT), Handler)  # bind trước khi xóa bản sao của phiên đang chạy
    except OSError as error:
        sys.exit(f'Không mở được cổng {PORT}: {error}. Thử: python3 chon_test.py 8791')
    shutil.rmtree(WORK, ignore_errors=True)
    shutil.copytree(PKG, WORK, ignore=shutil.ignore_patterns('~$*', '.DS_Store'))
    url = f'http://127.0.0.1:{PORT}'
    print(f'Bản sao: {WORK}\nGiao diện: {url}  (Ctrl+C để dừng)', flush=True)
    if not os.environ.get('NO_BROWSER'):
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
