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
from collections import Counter, defaultdict
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


def state_graph(nodes, edges, start):
    """Sơ đồ trạng thái viết bằng cú pháp Mermaid, Pele vẽ thành SVG. nodes: [(tên, chữ hiển thị, đỏ)], edges: [(từ, đến, nhãn, đỏ)].
    Pele tải từ CDN; offline thì trang hiện nguyên văn bản này, vẫn đọc được từng phép chuyển."""
    ids = {name: f's{i}' for i, (name, *_) in enumerate(nodes)}  # id ngắn, tránh từ khóa Mermaid như end
    out = ['flowchart LR'] + ([f'  start(( )) --> {ids[start]}'] if start else [])
    out += [f'  {ids[n]}["{text}"]' + (':::bad' if bad else '') for n, text, bad in nodes]
    out += [f'  {ids[a]} -->' + (f'|"{label}"|' if label else '') + f' {ids[b]}' for a, b, label, _ in edges]
    red = [str(i + bool(start)) for i, e in enumerate(edges) if e[3]]  # cạnh 0 là mũi tên vào trạng thái đầu, nếu có
    out += [f'  linkStyle {",".join(red)} stroke:#d93025,stroke-width:2.5px'] if red else []
    out.append('  classDef bad stroke:#d93025,stroke-width:2.5px')
    return chr(10).join(out)


def auth_graph(d):
    """Cấu trúc Kripke từ auth_model.json: trạng thái mang nhãn violation và đường phản ví dụ tô đỏ."""
    paths = [r.get('counterexample') or [] for r in d['results']]
    cex = {pair for p in paths for pair in zip(p, p[1:])}
    nodes = [(s, s + '<br>{' + ', '.join(d['labels'][s]) + '}', 'violation' in d['labels'][s]) for s in d['states']]
    edges = [(a, b, '', (a, b) in cex) for a, targets in d['states'].items() for b in targets]
    return nodes, edges, d['initial_state']


def memory_graph(d):
    """Mô hình trạng thái bộ nhớ từ memory_case_results.json: gộp phép chuyển cùng hai đầu, phép chuyển sinh vi phạm tô đỏ."""
    by_edge = defaultdict(list)
    for t in d['transition_table']:
        by_edge[t['from'], t['to']].append(t)
    edges = [(a, b, '<br>'.join(t['event'] + (f' ⚠ {t["violation"]}' if t['violation'] else '') for t in ts),
              any(t['violation'] for t in ts)) for (a, b), ts in by_edge.items()]
    nodes = [(s, f'{s} ({v["id"]})', False) for s, v in d['states'].items()]
    return nodes, edges, next(iter(d['states']))  # trạng thái đầu là P0, mục đầu của states


SRC, V0, V1 = 'source_v0: mã gốc', '_v0: mã lỗi cố ý', '_v1: mã đã sửa'


def ver(path):
    """Nhánh mã của một tệp hay nhóm theo quy ước của gói: thư mục _v0 là mã lỗi, _v1 là mã đã sửa, còn lại là mã gốc."""
    p = f'/{path}/'
    return V0 if '/_v0/' in p else V1 if '/_v1/' in p else SRC


def memory_walk(d, branch):
    """Phép chuyển mà đối tượng của một nhánh mã thực sự đi qua: phát lại chuỗi sự kiện từng đối tượng trên bảng chuyển."""
    step = {(t['from'], t['event']): t for t in d['transition_table']}
    start, used = next(iter(d['states'])), Counter()
    for o in d['objects']:
        if ver(o['group']) != branch:
            continue
        s, found = start, set()
        for event in o['events']:
            t = step.get((s, event))
            if t is None:  # cặp không có trong bảng giữ nguyên trạng thái, như step() của memory_typestate.py
                continue
            v = t['violation'] if t['violation'] != 'E_HELD_TO_END' or o['kind'] in ('link', 'result', 'stmt') else None
            used[s, event, t['to'], v] += 1
            found.add(v)
            s = t['to']
        assert found - {None} == set(o['violations']), o['obj']  # phát lại phải ra đúng vi phạm run_memory_cases.py đã ghi
    table = [{'from': a, 'event': f'{event} ×{n}', 'to': b, 'violation': v} for (a, event, b, v), n in used.items()]
    seen = {start} | {t[k] for t in table for k in ('from', 'to')}
    return memory_graph({'states': {s: v for s, v in d['states'].items() if s in seen}, 'transition_table': table})


def rule_hits(data):
    hits = Counter(r['check_id'].rsplit('.', 1)[-1] for r in data['results'])
    return [(f'{rule}<br>{n} hit · {FINDS.get(rule, "—")}', True) for rule, n in hits.most_common()]


def branches(tid):
    """Kết quả của test chia theo nhánh mã (mã gốc, _v0, _v1): (tệp nguồn dữ liệu, {nhánh: [(chữ, lỗi)]}).
    Lỗi TypeError khi JSON chưa có (load trả None), tức test chưa chạy."""
    if tid == 'kiem_ke':
        d = load(E + 'static_summary.json')
        n = d['php_file_count']
        return E + 'static_summary.json', {SRC: [
            (f"{n} tệp PHP, {d['physical_lines']} dòng", False), (f"lint {d['lint_ok']}/{n}", d['lint_ok'] < n),
            (f"{len(d['empty_files'])} tệp rỗng", bool(d['empty_files'])),
            (f"{len(d['missing_includes'])} include gãy", bool(d['missing_includes']))]}
    if tid in ('sast', 'bao_cao'):
        rel = E + 'semgrep_run1.json' if tid == 'sast' else 'bao_cao_semgrep.json'
        return rel, {SRC: rule_hits(load(rel))}
    if tid == 'phpstan':
        d = phpstan_data()
        return None, {SRC: [(f"{Path(f).name}: {v['errors']} thông báo", True) for f, v in d['files'].items()]}
    if tid == 'ma_sinh':
        d = load(E + 'generated_static_results.json')
        return E + 'generated_static_results.json', {ver(r['version']): [  # cùng 5 tệp ở cả hai nhánh, tệp 0 hit vẫn hiện
            (f"{x['file']}: {r['by_file'].get(x['file'], 0)} hit · lint {'đạt' if x['exit_code'] == 0 else 'lỗi'}",
             r['by_file'].get(x['file'], 0) > 0 or x['exit_code'] != 0) for x in r['lint']] for r in d['runs']}
    if tid == 'sat_smt':
        cases = defaultdict(list)
        for c in load(E + 'formal_results.json')['boolean_cases'] + load(E + 'formal_results.json')['smt_cases']:
            # SAT ở ca kiểm vi phạm là có phản ví dụ; ca đối chứng (control) phải SAT nên không tô đỏ
            cases[ver(c['source']), Path(c['source']).name].append(
                c.get('status', c.get('dpll')) == 'SAT' and 'control' not in c['id'])
        out = defaultdict(list)
        for (b, f), bad in sorted(cases.items()):
            if b != SRC:  # ca đối chứng của chính DPLL, không thuộc nhánh mã nào
                out[b].append((f'{f}: {sum(bad)}/{len(bad)} ca có phản ví dụ', any(bad)))
        return E + 'formal_results.json', dict(out)
    if tid == 'sql':
        s, st = load(E + 'sql_case_results.json')['summary'], load(E + 'sql_static_results.json')
        lint = defaultdict(list)
        for x in st['lint']:
            lint[ver(x['file'])].append(x['exit_code'] == 0)
        return E + 'sql_case_results.json', {SRC: [
            (f"{s['queries']} truy vấn, {s['fields']} trường", False),
            (f"CNF {s['query_cnf_crosschecks_passed']}/{s['query_cnf_cases']} trùng", s['query_cnf_crosschecks_passed'] < s['query_cnf_cases']),
            (f"SMT {s['field_smt_expected_passed']}/{s['field_smt_cases']} đúng kỳ vọng", s['field_smt_expected_passed'] < s['field_smt_cases'])],
            **{ver(sc['version']): [(f"Semgrep: {sc['findings']} hit / {sc['scanned']} tệp", sc['findings'] > 0),
                                    (f"lint {sum(lint[ver(sc['version'])])}/{len(lint[ver(sc['version'])])}",
                                     not all(lint[ver(sc['version'])]))] for sc in st['scans']}}
    if tid == 'auth':
        d = load(E + 'auth_model.json')
        return E + 'auth_model.json', {SRC: [(f"{r['formula']}: {'đúng' if r['initial_satisfies'] else 'sai'}",
                                              not r['initial_satisfies']) for r in d['results']]}
    if tid == 'so_ho_so':
        d = load(E + 'case_register.json')
        rows = defaultdict(list)
        for r in d['sat_rows'] + d['smt_rows']:
            rows[ver(r['source'])].append(r.get('status', r.get('dpll')) == r['expected'])
        return E + 'case_register.json', {
            SRC: [(f"{d['summary']['overview_cases']} hồ sơ tổng hợp, {d['summary']['sql_source_cases']} truy vấn SQL", False)],
            **{b: [(f'{len(ok)} hồ sơ SAT/SMT', False), (f'khớp kỳ vọng {sum(ok)}/{len(ok)}', not all(ok))]
               for b, ok in sorted(rows.items()) if b != SRC}}
    if tid == 'bo_nho_unit':
        by_class = defaultdict(list)
        for _, cls, status in unit_tests():
            by_class[cls.split('.')[-2] if '.' in cls else cls].append(status == 'ok')  # như sec_bo_nho_unit
        return None, {'models/test_memory_typestate.py': [(f'{c}: {sum(ok)}/{len(ok)} đạt', not all(ok))
                                                         for c, ok in by_class.items()]} if by_class else None
    if tid == 'bo_nho_tinh':
        d, out = load(E + 'memory_static_results.json'), {SRC: [], V0: [], V1: []}
        rules = d['semgrep']['by_group_rule']
        for g in dict.fromkeys([*rules, *(g.replace('_v0', '_v1') for g in rules)]):  # nhóm 0 hit không có trong JSON
            n = sum(rules.get(g, {}).values())
            out[ver(g)].append((f'Semgrep {g}: {n} hit', n > 0))
        runs = defaultdict(dict)
        for r in d['compilers']['runs']:
            # GCC báo 2 lần cùng dòng, cùng CWE; đếm như nhật ký và Bảng 46
            runs[r['file']][r['tool']] = len({(f['line'], tuple(f['cwe']) or f['rule']) for f in r['findings']})
        for f, n in runs.items():
            out[ver(f)].append((f"{Path(f).name}: GCC {n.get('gcc', '—')}, Clang {n.get('clang', '—')}", any(n.values())))
        return E + 'memory_static_results.json', out
    if tid == 'bo_nho_case':
        s, out = load(E + 'memory_case_results.json')['summary'], {SRC: [], V0: [], V1: []}
        for g, codes in s['by_group'].items():
            out[ver(g)].append((f'{g}: {sum(codes.values())} vi phạm' + ''.join(f'<br>{c} ×{n}' for c, n in codes.items()),
                                bool(codes)))
        for m, z in s['c_models'].items():
            out[V0 if m.endswith('_v0') else V1].append((f'C {m[:-3]}: {z}', z == 'SAT'))
        return E + 'memory_case_results.json', out


def diagrams(tid):
    """Sơ đồ của một test cho giao diện: kết quả theo nhánh mã, thêm mô hình trạng thái nếu test có."""
    out = []
    try:
        rel, b = branches(tid)
    except TypeError:
        rel, b = None, None
    if b:
        if SRC in b:  # bản vá của mã gốc (source_v1) chưa có trong gói
            b['source_v1: mã gốc đã vá'] = [('chưa có trong gói, chờ bo_sung_v1/', False)]
        title = next(t[2] for t in TESTS if t[0] == tid)
        out.append({'title': 'Kết quả theo nhánh mã', 'file': rel, 'src': state_graph(*tree_graph(title, b))})
    if tid == 'auth' and (d := load(E + 'auth_model.json')):
        out.append({'title': 'Kripke source_v0', 'file': E + 'auth_model.json', 'src': state_graph(*auth_graph(d))})
    if tid == 'bo_nho_case' and (d := load(E + 'memory_case_results.json')):
        out += [{'title': f'Trạng thái {b.split(":")[0]}', 'file': E + 'memory_case_results.json',
                 'src': state_graph(*memory_walk(d, b))} for b in (SRC, V0, V1)]
        out.append({'title': 'Mô hình đầy đủ', 'file': E + 'memory_case_results.json', 'src': state_graph(*memory_graph(d))})
    return out


def tree_graph(title, branches):
    """Cây kết quả: gốc là test, mỗi nhánh mã nối tới các mục của nó, mục lỗi tô đỏ."""
    nodes, edges = [('test', title, False)], []
    for i, (branch, items) in enumerate(branches.items()):
        nodes.append((f'b{i}', branch, False))
        edges.append(('test', f'b{i}', '', False))
        for j, (text, bad) in enumerate(items):
            nodes.append((f'b{i}.{j}', text, bad))
            edges.append((f'b{i}', f'b{i}.{j}', '', bad))
    return nodes, edges, None


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
        return (f"{len(base)} vi phạm trên {len({f['file'] for f in base})}/{load(E + 'static_summary.json')['php_file_count']} tệp; "
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
    rows = [tr(code(r['formula']), td('đúng' if r['initial_satisfies'] else 'sai'), td(' → '.join(r.get('counterexample') or [])))
            for r in d['results']]
    return (f'{esc(d["scope"])}. Trạng thái đạt tới: {esc(", ".join(d["reachable"]))}. '
            f'Mô hình dựng từ {esc(", ".join(d["source_refs"]))}.',
            '<p class="muted">Cấu trúc Kripke: mỗi ô là một trạng thái, {…} là nhãn mệnh đề, mũi tên là phép chuyển, '
            'mũi tên quay về chính ô là tự lặp. Đỏ: trạng thái mang nhãn violation và đường phản ví dụ của công thức sai. '
            'Đọc công thức: AG(p) là p đúng ở mọi trạng thái đi tới được; EF(p) là có ít nhất một đường tới trạng thái có p.</p>' +
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
    steps = defaultdict(list)
    for t in d['transition_table']:
        if t['violation']:
            steps[t['violation']].append(f'{t["from"]} –{t["event"]}→ {t["to"]}')
    states = [tr(code(v['id']), code(s), td(v['meaning'])) for s, v in d['states'].items()]
    blocks = []
    for kind, items in sorted(by_kind.items(), key=lambda kv: -len(kv[1])):
        rows = [tr(td(f'{Path(f["file"]).name}:{f["line"]}', 'loc'), code(f['var']), code(f['stmt'][:140])) for f in items]
        note = tags(items[0]['severity'], ', '.join(items[0]['cwe']), *(steps[kind] or ['ngoài sơ đồ: kiểm tra câu SQL'])) + \
            f'<div class="muted">{esc(items[0]["label"])}</div>'
        blocks.append(details(len(items), esc(kind), note, f'<table class="locs">{"".join(rows)}</table>'))
    total = sum(map(len, by_kind.values()))
    return (f'{total} vi phạm trên {len({f["file"] for v in by_kind.values() for f in v})} tệp baseline, theo mô hình '
            f'{len(d["states"])} trạng thái và {len(d["transition_table"])} phép chuyển. Mã case ở '
            '<a href="/generated_cases/memory/">generated_cases/memory/</a>.',
            '<p class="muted">Mỗi biến PHP giữ resource hoặc bí mật đi theo mô hình đầy đủ ở trên từ UNDEF. Nhãn mũi tên là sự kiện '
            'trong mã; mũi tên đỏ có ⚠ là phép chuyển sinh vi phạm. Mỗi nhóm vi phạm bên dưới ghi phép chuyển tương ứng '
            'để dò lại trên sơ đồ.</p>' + details(len(states), 'trạng thái và ý nghĩa', '', table(['ID', 'Trạng thái', 'Ý nghĩa'], states)) +
            ''.join(blocks))


SECTIONS = {'kiem_ke': sec_kiem_ke, 'sast': sec_sast, 'bao_cao': sec_bao_cao, 'phpstan': sec_phpstan, 'ma_sinh': sec_ma_sinh,
            'sat_smt': sec_sat_smt, 'sql': sec_sql, 'auth': sec_auth, 'so_ho_so': sec_so_ho_so,
            'bo_nho_unit': sec_bo_nho_unit, 'bo_nho_tinh': sec_bo_nho_tinh, 'bo_nho_case': sec_bo_nho_case}
assert set(SECTIONS) == {t[0] for t in TESTS}, 'test chưa có mục báo cáo'


def figures(tid):
    """Các sơ đồ của test như khung sơ đồ của giao diện, xếp liền nhau để báo cáo in được."""
    out = ''
    for g in diagrams(tid):
        src = f'<a href="/{g["file"]}">{g["file"]}</a>' if g['file'] else 'nhật ký của lần chạy'
        out += (f'<figure><figcaption><b>{esc(g["title"])}</b> · vẽ từ {src}</figcaption>'
                f'<pre class="mermaid">{esc(g["src"])}</pre></figure>')
    return out


def build_report():
    ran = [t for t in TESTS if state['result'].get(t[0], {}).get('status') in ('ok', 'fail')]
    rows, sections = [], []
    for tid, group, title, _, expect, _ in ran:
        r = state['result'][tid]
        ok = r['status'] == 'ok'
        try:
            got = esc(actual(tid)) if ok else f'<pre>{esc("".join(outputs.get(tid, "").splitlines(True)[-12:]))}</pre>'
            intro, body = SECTIONS[tid]() if ok else ('Test lỗi, xem log ở cột Thực tế của bảng tổng hợp.', '')
            body = (figures(tid) if ok else '') + body
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


THEME = '''/* Màu và bán kính theo theme neutral của shadcn/ui; viết CSS thường để trang vẫn là một tệp, không cần build */
:root { --radius:0.625rem; --background:oklch(1 0 0); --foreground:oklch(0.145 0 0); --card:oklch(1 0 0);
  --primary:oklch(0.205 0 0); --primary-foreground:oklch(0.985 0 0); --secondary:oklch(0.97 0 0); --muted:oklch(0.97 0 0);
  --muted-foreground:oklch(0.556 0 0); --accent:oklch(0.97 0 0); --destructive:oklch(0.577 0.245 27.325);
  --border:oklch(0.922 0 0); --input:oklch(0.922 0 0); --ring:oklch(0.708 0 0);
  --ok:oklch(0.527 0.154 150.069); --run:oklch(0.546 0.245 262.881); color-scheme:light dark; }
@media (prefers-color-scheme: dark) { :root { --background:oklch(0.145 0 0); --foreground:oklch(0.985 0 0);
  --card:oklch(0.205 0 0); --primary:oklch(0.922 0 0); --primary-foreground:oklch(0.205 0 0); --secondary:oklch(0.269 0 0);
  --muted:oklch(0.269 0 0); --muted-foreground:oklch(0.708 0 0); --accent:oklch(0.269 0 0);
  --destructive:oklch(0.704 0.191 22.216); --border:oklch(1 0 0 / 10%); --input:oklch(1 0 0 / 15%); --ring:oklch(0.556 0 0);
  --ok:oklch(0.792 0.209 151.711); --run:oklch(0.707 0.165 254.624); } }'''

REPORT = '''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Báo cáo kiểm thử tĩnh – Nhóm 13</title>
<style>
__THEME__
* { box-sizing:border-box; }
body { margin:0; background:var(--background); color:var(--foreground); font:14px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width:1180px; margin:0 auto; padding:32px 16px 64px; }
a { color:inherit; text-decoration:underline; text-decoration-color:color-mix(in oklch, currentColor 35%, transparent); text-underline-offset:3px; }
a:hover { text-decoration-color:currentColor; }
h1 { font-size:20px; font-weight:600; letter-spacing:-0.01em; margin:0; }
h2 { font-size:16px; font-weight:600; margin:36px 0 4px; } h3 { font-size:14px; font-weight:600; margin:18px 0 6px; }
section { scroll-margin-top:16px; }
.muted { color:var(--muted-foreground); font-size:13px; }
.head { display:flex; flex-wrap:wrap; justify-content:space-between; gap:12px; align-items:end;
  border-bottom:1px solid var(--border); padding-bottom:16px; }
.big { font-size:20px; font-weight:600; margin-bottom:8px; }
button { height:32px; padding:0 12px; font:500 13px system-ui, sans-serif; border:1px solid var(--border); cursor:pointer;
  border-radius:calc(var(--radius) * 0.8); background:var(--background); color:var(--foreground); box-shadow:0 1px 2px 0 rgb(0 0 0 / 0.05); }
button:hover { background:var(--accent); }
.scroll { overflow-x:auto; background:var(--card); border:1px solid var(--border); border-radius:calc(var(--radius) * 1.4); }
details .scroll { border:0; border-top:1px solid var(--border); border-radius:0; }
table { width:100%; border-collapse:collapse; font-size:14px; }
th, td { text-align:left; vertical-align:top; padding:8px 12px; border-bottom:1px solid var(--border); }
tr:last-child td { border-bottom:0; }
th { font-size:12px; font-weight:500; color:var(--muted-foreground); background:var(--muted); }
td.num { text-align:right; font-variant-numeric:tabular-nums; }
.status { display:inline-flex; padding:2px 8px; border-radius:calc(var(--radius) * 0.8); font-weight:500; font-size:12px; white-space:nowrap; }
.status.ok { color:var(--ok); background:color-mix(in oklch, var(--ok) 12%, transparent); }
.status.fail { color:var(--destructive); background:color-mix(in oklch, var(--destructive) 12%, transparent); }
code, pre { font:12px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace; }
code { background:var(--muted); padding:1px 5px; border-radius:calc(var(--radius) * 0.6); word-break:break-word; }
pre { margin:0; white-space:pre-wrap; max-height:220px; overflow:auto; }
figure { margin:12px 0; } figcaption { font-size:13px; color:var(--muted-foreground); margin-bottom:6px; }
figcaption b { color:var(--foreground); font-weight:600; }
pre.mermaid { max-height:none; background:var(--card); border:1px solid var(--border); border-radius:calc(var(--radius) * 1.4);
  padding:12px; text-align:center; font-family:system-ui, sans-serif; --pele-font:system-ui, sans-serif; --pele-bg:var(--card);
  --pele-fg:var(--foreground); --pele-muted:var(--muted-foreground); --pele-line:var(--muted-foreground); --pele-surface:var(--muted);
  --pele-surface-alt:var(--secondary); --pele-border:var(--ring); --pele-accent:var(--primary); }
details { background:var(--card); border:1px solid var(--border); border-radius:calc(var(--radius) * 1.4); margin:8px 0; overflow:hidden; }
summary { cursor:pointer; padding:10px 14px; display:flex; flex-wrap:wrap; gap:6px 10px; align-items:baseline; }
summary:hover { background:var(--accent); }
summary .muted { flex-basis:100%; }
.count { min-width:44px; font-weight:600; font-variant-numeric:tabular-nums; }
.tag { font-size:12px; padding:1px 8px; border:1px solid var(--border); border-radius:calc(var(--radius) * 0.8);
  color:var(--muted-foreground); margin-right:4px; }
.tag.find { color:var(--run); border-color:color-mix(in oklch, var(--run) 40%, transparent); }
td.loc { white-space:nowrap; font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:12px; }
td:first-child code { white-space:nowrap; word-break:normal; }
@media print { button { display:none; } body { background:#fff; } details, figure { break-inside:avoid-page; } }
</style></head><body><main>
<div class="head"><div><h1>Báo cáo kiểm thử tĩnh – Nhóm 13</h1>
<div class="muted">Hệ thống quản lý thư viện (librarian, 66 tệp PHP). Chỉ phân tích mã nguồn, không chạy ứng dụng hay CSDL. Tạo lúc __TIME__.</div></div>
<div><div class="big">__SUMMARY__</div>
<button onclick="document.querySelectorAll('details').forEach(d => d.open = true)">Mở hết</button>
<button onclick="document.querySelectorAll('details').forEach(d => d.open = true); print()">In / lưu PDF</button></div></div>
<h2>Tổng hợp</h2><p class="muted">Cột thực tế đọc từ JSON mà chính lần chạy này ghi ra; cột kỳ vọng lấy theo README của gói. Bấm tên test để tới mục chi tiết. Mỗi mục có các sơ đồ như giao diện chọn test: kết quả theo nhánh mã
(source_v0 mã gốc, _v0 mã lỗi cố ý, _v1 mã đã sửa), thêm Kripke và sơ đồ trạng thái bộ nhớ ở mục tương ứng; màu đỏ là lỗi hoặc vi phạm.</p>
<div class="scroll"><table><tr><th>Test</th><th>Kết quả</th><th>Kỳ vọng</th><th>Thực tế</th><th>Mã</th><th>Giây</th></tr>__ROWS__</table></div>
__DETAILS__
</main>
<script type="module">
import { mount } from 'https://cdn.jsdelivr.net/npm/pele@1.3.0/dist/pele.js';
for (const el of document.querySelectorAll('pre.mermaid')) mount(el, el.textContent);
</script>
</body></html>
'''.replace('__THEME__', THEME)


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
        elif url.path == '/api/diagrams':  # đọc lại JSON mỗi lần, để sơ đồ theo kết quả của lần chạy mới nhất
            tid = parse_qs(url.query).get('test', [''])[0]
            data = diagrams(tid) if any(t[0] == tid for t in TESTS) else []
            self.send_body(json.dumps(data, ensure_ascii=False).encode(), 'application/json; charset=utf-8')
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
__THEME__
* { box-sizing:border-box; }
body { margin:0; background:var(--background); color:var(--foreground); font:14px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
.app { max-width:1440px; margin:0 auto; padding:16px; }
header { margin-bottom:14px; }
h1 { font-size:20px; font-weight:600; letter-spacing:-0.01em; margin:0; }
h2 { font-size:14px; font-weight:600; margin:0; }
.desc { color:var(--muted-foreground); font-size:13px; margin:2px 0 0; }
a { color:inherit; text-decoration:underline; text-decoration-color:color-mix(in oklch, currentColor 35%, transparent); text-underline-offset:3px; }
a:hover { text-decoration-color:currentColor; }
code { font:12px ui-monospace, SFMono-Regular, Menlo, monospace; background:var(--muted); padding:1px 5px; border-radius:calc(var(--radius) * 0.6); }
:focus-visible { outline:none; box-shadow:0 0 0 3px color-mix(in oklch, var(--ring) 50%, transparent); }
.panes { display:grid; grid-template-columns:var(--left, 360px) 16px minmax(0, 1fr); }
aside { display:flex; flex-direction:column; gap:16px; min-height:0; }
.right { display:grid; gap:16px; min-height:0; min-width:0; }
.card { background:var(--card); border:1px solid var(--border); border-radius:calc(var(--radius) * 1.4); padding:16px;
  box-shadow:0 1px 2px 0 rgb(0 0 0 / 0.05); min-width:0; }
.card-head { display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:12px; }
.stack { display:grid; gap:8px; }
hr { border:0; border-top:1px solid var(--border); margin:4px 0; }
.btn { display:inline-flex; align-items:center; justify-content:center; gap:8px; height:36px; padding:0 16px; width:100%;
  border:1px solid transparent; border-radius:calc(var(--radius) * 0.8); font-family:inherit; font-size:14px; font-weight:500;
  white-space:nowrap; cursor:pointer; transition:background-color .15s; }
.btn.primary { background:var(--primary); color:var(--primary-foreground); box-shadow:0 1px 2px 0 rgb(0 0 0 / 0.05); }
.btn.primary:hover { background:color-mix(in oklch, var(--primary) 90%, transparent); }
.btn.outline { background:var(--background); border-color:var(--border); color:var(--foreground); box-shadow:0 1px 2px 0 rgb(0 0 0 / 0.05); }
.btn.secondary { background:var(--secondary); color:var(--foreground); }
.btn.secondary:hover { background:color-mix(in oklch, var(--secondary) 80%, transparent); }
.btn.ghost { background:transparent; color:var(--foreground); width:auto; }
.btn.outline:hover, .btn.ghost:hover { background:var(--accent); }
.btn.sm { height:32px; padding:0 12px; font-size:13px; gap:6px; width:auto; }
.btn.step { justify-content:flex-start; padding:0 12px; }
.btn:disabled { opacity:.5; pointer-events:none; }
.num { display:inline-grid; place-items:center; width:22px; height:22px; border-radius:999px; background:var(--secondary);
  font-size:12px; font-weight:600; flex:none; }
.grow { flex:1; text-align:left; }
.group { font-size:12px; font-weight:500; color:var(--muted-foreground); margin:12px 0 4px; padding:0 8px; }
.group:first-child { margin-top:0; }
.row { display:flex; align-items:center; gap:10px; padding:4px 8px; border-radius:calc(var(--radius) * 0.8); cursor:pointer; }
.row:hover { background:color-mix(in oklch, var(--accent) 60%, transparent); }
.row.active { background:var(--accent); }
.row.active .name { font-weight:500; }
.row input { width:16px; height:16px; margin:0; accent-color:var(--primary); flex:none; cursor:pointer; }
.name { flex:1; min-width:0; text-align:left; background:none; border:0; padding:2px 0; font:inherit; color:inherit; cursor:pointer; border-radius:4px; }
.badge { display:inline-flex; align-items:center; border:1px solid var(--border); border-radius:calc(var(--radius) * 0.8);
  padding:1px 8px; font-size:12px; font-weight:500; white-space:nowrap; color:var(--muted-foreground); flex:none; }
.badge.ok { color:var(--ok); border-color:transparent; background:color-mix(in oklch, var(--ok) 12%, transparent); }
.badge.fail { color:var(--destructive); border-color:transparent; background:color-mix(in oklch, var(--destructive) 12%, transparent); }
.badge.running, .badge.queued { color:var(--run); border-color:transparent; background:color-mix(in oklch, var(--run) 12%, transparent); }
.tabs { display:inline-flex; flex-wrap:wrap; gap:2px; background:var(--muted); border-radius:var(--radius); padding:3px; }
.tab { border:1px solid transparent; background:transparent; color:var(--muted-foreground); font:inherit; font-size:13px; font-weight:500;
  padding:2px 10px; border-radius:calc(var(--radius) * 0.8); cursor:pointer; white-space:nowrap; }
.tab:hover { color:var(--foreground); }
.tab[aria-selected="true"] { background:var(--background); color:var(--foreground); box-shadow:0 1px 2px 0 rgb(0 0 0 / 0.05); }
.detail-head { display:flex; justify-content:space-between; align-items:flex-start; gap:12px; }
.detail-head h2 { font-size:16px; }
.actions { display:flex; align-items:center; gap:8px; flex:none; }
.filebar { display:flex; flex-wrap:wrap; align-items:center; gap:8px 12px; margin:10px 0; font-size:13px; }
.sash { position:relative; cursor:col-resize; touch-action:none; border-radius:4px; }
.sash::after { content:''; position:absolute; left:6px; top:50%; width:4px; height:36px; margin-top:-18px; border-radius:4px;
  background:var(--border); transition:background-color .15s; }
.sash:hover::after, .sash.drag::after, .sash:focus-visible::after { background:var(--ring); }
pre { margin:0; background:var(--muted); border-radius:calc(var(--radius) * 0.8); padding:12px; overflow:auto; height:50vh;
  font:12.5px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace; }
#log { white-space:pre-wrap; word-break:break-word; }
.code { white-space:pre; counter-reset:ln; padding-left:0; }
.code span { display:block; }
.code span::before { counter-increment:ln; content:counter(ln); display:inline-block; width:4.5em; padding-right:12px; margin-right:12px;
  text-align:right; color:var(--muted-foreground); border-right:1px solid var(--border); background:var(--muted); position:sticky; left:0; user-select:none; }
.code em { display:block; padding:8px 12px; color:var(--muted-foreground); font-style:normal; }
.diagram { height:50vh; overflow:auto; border:1px solid var(--border); border-radius:calc(var(--radius) * 0.8); padding:8px; text-align:center;
  --pele-font:system-ui, sans-serif; --pele-bg:var(--card); --pele-fg:var(--foreground); --pele-muted:var(--muted-foreground);
  --pele-line:var(--muted-foreground); --pele-surface:var(--muted); --pele-surface-alt:var(--secondary); --pele-border:var(--ring);
  --pele-accent:var(--primary); }
.diagram pre { height:100%; padding:0; background:none; text-align:left; white-space:pre; }
.diagram svg { width:100%; height:100% !important; max-width:none !important; }  /* Pele gắn style height:auto; cho sơ đồ co vừa khung */
#diagram-card:fullscreen { border:0; border-radius:0; padding:24px; }
/* Màn rộng: hai cột cao bằng cửa sổ như ứng dụng desktop; danh sách test và cột phải cuộn bên trong */
@media (min-width: 861px) { html, body { height:100%; } .app { height:100%; display:flex; flex-direction:column; }
  .panes { flex:1; min-height:0; } aside { overflow:auto; } .list-card { flex:1; min-height:300px; display:flex; flex-direction:column; }
  #list { flex:1; min-height:0; overflow:auto; }
  .right { overflow:auto; grid-template-rows:minmax(180px, .7fr) minmax(340px, 1.3fr) minmax(400px, 1.5fr); }
  .flex-card { display:flex; flex-direction:column; min-height:0; } .fill { flex:1; min-height:0; height:auto; } }
@media (max-width: 860px) { .panes { grid-template-columns:1fr; gap:16px; } .sash { display:none; } }
@media (prefers-color-scheme: dark) { .tab[aria-selected="true"] { background:var(--card); border-color:var(--input); } }
</style></head><body><div class="app">
<header><h1>Chọn test phân tích tĩnh – Nhóm 13</h1>
<p class="desc">Mã nguồn PHP → Semgrep, PHPStan → Mã sinh và hình thức → Bộ nhớ → Báo cáo</p></header>
<div class="panes" id="panes">
<aside>
<section class="card"><h2>Nguồn kiểm thử</h2>
<p class="desc">Phân hệ librarian, 66 tệp PHP; chỉ đọc mã, không chạy ứng dụng hay CSDL. Chạy trên bản sao
<code>__WORK__</code>, gói nộp giữ nguyên.</p>
<p class="desc"><a href="/source_v0/librarian/" target="_blank">source_v0/librarian/</a> · <a href="/evidence/" target="_blank">evidence/</a> ·
<a href="/generated_cases/" target="_blank">generated_cases/</a></p></section>
<section class="card list-card"><div class="card-head"><h2>Danh sách test</h2><span>
<button class="btn ghost sm" id="all">Chọn tất cả</button><button class="btn ghost sm" id="none">Bỏ chọn</button></span></div>
<div id="list"></div><button class="btn secondary" id="run" style="margin-top:12px">Chạy các test đã chọn</button></section>
<section class="card"><div class="card-head"><div><h2>Chạy theo bước</h2><p class="desc">Mỗi bước chạy cả nhóm test.</p></div></div>
<div class="stack" id="steps"></div>
<button class="btn outline" id="report" style="margin-top:8px" disabled>Mở báo cáo HTML</button>
<p class="desc">Báo cáo đầy đủ nhất khi đã chạy cả 3 bước; trong báo cáo có nút In / lưu PDF.</p></section>
</aside>
<div class="sash" id="sash" role="separator" aria-orientation="vertical" tabindex="0"
  aria-label="Thanh chia hai cột: kéo hoặc dùng phím mũi tên trái, phải"></div>
<div class="right">
<section class="card flex-card"><div class="card-head"><h2>Nhật ký chạy</h2></div>
<pre id="log" class="fill" aria-live="polite">Tích test rồi bấm “Chạy các test đã chọn”, hoặc chọn một bước.</pre></section>
<section class="card flex-card"><div id="detail"></div><pre id="code" class="code fill"></pre></section>
<section class="card flex-card" id="diagram-card"><div class="card-head"><div class="tabs" id="graphs" role="tablist"
  aria-label="Sơ đồ của test đang chọn"></div><button class="btn outline sm" id="full">Xem toàn màn hình</button></div>
<div class="diagram fill" id="diagram"></div><p class="desc" id="graph-note"></p></section>
</div></div></div>
<script>
const TESTS = __TESTS__;
const MAX = 3000;  // số dòng tối đa trong khung mã nguồn; tệp dài hơn thì mở bằng link
const $ = id => document.getElementById(id);
const list = $('list'), log = $('log'), report = $('report'), panes = $('panes'), sash = $('sash');
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const link = (href, text) => `<a href="/${href}" target="_blank">${text}</a>`;
const name = p => p.replace(/\\/$/, '').split('/').pop() + (p.endsWith('/') ? '/' : '');
const STATUS = {queued: 'Đang chờ', running: 'Đang chạy…', ok: 'Đạt', fail: 'Lỗi'};
const results = {};
let selected = TESTS[0].id, file = null, loaded = null, reportAt = null, busy = false, from = 0, started = false, shown = '';
let graphs = [], graph = 0, pele = null;
[...new Set(TESTS.map(t => t.group))].forEach((group, i) => {
  const tests = TESTS.filter(t => t.group === group);
  $('steps').insertAdjacentHTML('beforeend', `<button class="btn outline step" data-run="${tests.map(t => t.id)}">
    <span class="num">${i + 1}</span><span class="grow">${group}</span><span class="desc">${tests.length} test</span></button>`);
  list.insertAdjacentHTML('beforeend', `<p class="group">${i + 1}. ${group}</p>` + tests.map(t => `<div class="row" data-id="${t.id}">
    <input type="checkbox" value="${t.id}" aria-label="Chọn ${t.title}"><button type="button" class="name">${t.title}</button>
    <span class="badge" id="b-${t.id}">Chưa chạy</span></div>`).join(''));
});
$('steps').insertAdjacentHTML('beforeend', `<hr><button class="btn primary" data-run="${TESTS.map(t => t.id)}">
  Chạy toàn bộ ${TESTS.length} test</button>`);
const boxes = () => [...list.querySelectorAll('input')];
$('all').onclick = () => boxes().forEach(b => b.checked = true);
$('none').onclick = () => boxes().forEach(b => b.checked = false);
$('run').onclick = () => start(boxes().filter(b => b.checked).map(b => b.value));
report.onclick = () => open('/bao_cao.html', '_blank');
$('full').onclick = () => $('diagram-card').requestFullscreen();
document.addEventListener('click', e => {
  const run = e.target.closest('[data-run]'), tab = e.target.closest('[data-file]'), g = e.target.closest('[data-graph]');
  const row = e.target.closest('.row');
  if (run) start(run.dataset.run.split(','));
  else if (tab) { file = tab.dataset.file; render(); }
  else if (g) showGraph(+g.dataset.graph);
  else if (row && e.target.tagName !== 'INPUT' && row.dataset.id !== selected) {
    selected = row.dataset.id; file = null; graph = 0; render(); loadGraphs();
  }
});
const setLeft = px => panes.style.setProperty('--left', Math.max(280, Math.min(px, panes.clientWidth - 440)) + 'px');
sash.onpointerdown = e => { e.preventDefault(); sash.setPointerCapture(e.pointerId); sash.classList.add('drag'); };
sash.onpointermove = e => { if (sash.hasPointerCapture(e.pointerId)) setLeft(e.clientX - panes.getBoundingClientRect().left - 8); };
sash.onpointerup = () => sash.classList.remove('drag');
sash.onkeydown = e => { const step = {ArrowLeft: -24, ArrowRight: 24}[e.key];
  if (step) { e.preventDefault(); setLeft(document.querySelector('aside').offsetWidth + step); } };
async function start(ids) {
  if (!ids.length) { alert('Chưa chọn test nào.'); return; }
  busy = true;
  for (const id of ids) results[id] = {status: 'queued'};
  render();
  await fetch('/api/run', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ids})});
}
const badge = r => `<span class="badge ${r ? r.status : ''}">${r ? STATUS[r.status] : 'Chưa chạy'}</span>`;
function render() {
  const t = TESTS.find(t => t.id === selected), files = [...t.view, ...t.rules].filter(f => !f.endsWith('/'));
  if (!files.includes(file)) file = files[0] || null;
  const key = JSON.stringify([results, selected, file, reportAt, busy]);
  if (key === shown) return;  // vẽ lại mỗi giây sẽ làm mất focus trên nút và link trong khung chi tiết
  shown = key;
  for (const t of TESTS) $('b-' + t.id).outerHTML = badge(results[t.id]).replace('<span', `<span id="b-${t.id}"`);
  list.querySelectorAll('.row').forEach(row => row.classList.toggle('active', row.dataset.id === selected));
  const r = results[t.id], done = r && (r.status === 'ok' || r.status === 'fail');
  $('detail').innerHTML = `<div class="detail-head"><div><p class="desc">${t.group}</p><h2>${t.title}</h2></div>
    <div class="actions">${badge(r)}<button class="btn outline sm" data-run="${t.id}">Chạy test này</button></div></div>
    <p class="desc">Kỳ vọng: ${t.expect}${done ? ` · Lần chạy: mã thoát ${r.code}, ${r.secs} giây` : ''}${reportAt && done
      ? ` · <a href="/bao_cao.html#${t.id}" target="_blank">mục trong báo cáo</a>` : ''}</p>
    <div class="filebar"><div class="tabs" role="tablist" aria-label="Tệp của test">${files.map(f => `<button class="tab" role="tab"
      data-file="${f}" aria-selected="${f === file}" title="${f}">${t.rules.includes(f) ? 'rule: ' : ''}${name(f)}</button>`).join('')}</div>
      ${t.view.filter(f => f.endsWith('/')).map(f => link(f, name(f))).join(' · ')}${file ? (t.view.some(f => f.endsWith('/')) ? ' · ' : '') +
      link(file, 'mở tệp riêng') : ''}</div>`;
  document.querySelectorAll('[data-run], #run').forEach(b => b.disabled = busy);
  report.disabled = !reportAt;
  report.textContent = reportAt ? `Mở báo cáo HTML (${reportAt})` : 'Mở báo cáo HTML';
  showFile();
}
async function showFile() {
  if (file === loaded) return;
  const want = loaded = file, code = $('code');
  if (!want) { code.innerHTML = '<em>Test này không có tệp văn bản; mở thư mục ở link bên trên.</em>'; return; }
  const res = await fetch('/' + want).catch(() => null);
  let text = res && res.ok ? await res.text() : null;
  if (want !== loaded) return;  // đã chọn tệp khác trong lúc tải
  if (text === null) { code.innerHTML = '<em>Chưa có tệp này trong bản sao; chạy test để tạo ra nó.</em>'; return; }
  if (want.endsWith('.json') || want.endsWith('.sarif')) try { text = JSON.stringify(JSON.parse(text), null, 2); } catch (e) {}
  const lines = text.split('\\n');
  code.innerHTML = lines.slice(0, MAX).map(l => `<span>${esc(l)}</span>`).join('') +
    (lines.length > MAX ? `<em>Còn ${lines.length - MAX} dòng nữa: ${link(want, 'mở tệp đầy đủ')}</em>` : '');
  code.scrollTop = 0;
}
async function loadGraphs() {
  const want = selected;
  let got;
  try { got = await (await fetch('/api/diagrams?test=' + want)).json(); } catch (e) { return; }
  if (want !== selected) return;  // đã chọn test khác trong lúc chờ
  graphs = got;
  $('graphs').innerHTML = graphs.map((g, i) => `<button class="tab" role="tab" data-graph="${i}">${g.title}</button>`).join('');
  if (graphs.length) return showGraph(Math.min(graph, graphs.length - 1));
  $('diagram').innerHTML = '<p class="desc">Test này chưa có dữ liệu để vẽ: bấm “Chạy test này”.</p>';
  $('graph-note').textContent = '';
}
async function showGraph(i) {
  const g = graphs[graph = i], box = $('diagram');
  $('graphs').querySelectorAll('.tab').forEach((b, j) => b.setAttribute('aria-selected', j === i));
  box.innerHTML = '<pre class="mermaid"></pre>';
  box.firstChild.textContent = g.src;  // offline thì giữ văn bản này, vẫn đọc được từng phép chuyển
  $('graph-note').innerHTML = `Vẽ từ ${g.file ? link(g.file, g.file) : 'nhật ký của lần chạy'}, cập nhật sau mỗi lần chạy
    “${TESTS.find(t => t.id === selected).title}”. Màu đỏ: lỗi hoặc vi phạm (hit, ca có phản ví dụ, trạng thái violation, phép chuyển ⚠ E_…).`;
  try { pele = pele || await import('https://cdn.jsdelivr.net/npm/pele@1.3.0/dist/pele.js'); pele.mount(box.firstChild, g.src); }
  catch (e) {}
}
async function poll() {
  try {
    const s = await (await fetch('/api/state?from=' + from)).json();
    from = s.next;
    if (s.log) { if (!started) { log.textContent = ''; started = true; } log.textContent += s.log; log.scrollTop = log.scrollHeight; }
    Object.assign(results, s.result);
    busy = s.running !== null;
    if (s.report && s.report !== reportAt) { loaded = null; loadGraphs(); }  // vừa chạy xong: tệp và sơ đồ có thể đã đổi
    reportAt = s.report;
  } catch (e) { busy = true; }
  render();
  setTimeout(poll, 1000);
}
render();
loadGraphs();
poll();
</script></body></html>
'''.replace('__THEME__', THEME)

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
