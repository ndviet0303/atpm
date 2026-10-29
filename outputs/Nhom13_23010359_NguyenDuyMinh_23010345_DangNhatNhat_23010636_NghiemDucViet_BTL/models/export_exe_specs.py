"""Xuất đặc tả JSON theo định dạng của SpecVerificationLab.exe (dataset/specs/FORMAT.md) từ bằng chứng đã có.

Mỗi tệp trong exe_specs/ nạp được bằng nút "Nạp từ file JSON khác..." của exe. Script chỉ đọc evidence/,
bo_sung_v1/evidence_v1/ và các sheet yêu cầu của tệp xlsx; không chạy lại phân tích nào.
"""
from pathlib import Path
import ast
import json
import keyword
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

import z3

sys.path.insert(0, str(Path(__file__).parent))
from memory_typestate import TABLE, step  # noqa: E402

BASE = Path(__file__).resolve().parents[1]
E, V1, OUT = BASE / 'evidence', BASE / 'bo_sung_v1' / 'evidence_v1', BASE / 'exe_specs'
XLSX = BASE / 'Nhom_13_Dac_ta_va_TestCase_Thu_vien.xlsx'
# Parser CTL của exe chỉ nhận OP(atom) hoặc OP(!atom); AG(write -> authenticated) viết lại thành AG(!violation)
# vì nhãn violation chỉ gắn ở trạng thái có write mà thiếu authenticated (auth_model.py).
AUTH_CTL = ['AG(!violation)', 'EF(denied)', 'EF(authenticated)']


def load(path):
    return json.loads(path.read_text())


def auth_kripke(d):
    """auth_model.json ({trạng thái: [kế tiếp]}, labels, initial_state) -> state_machine của exe."""
    return {'states': list(d['states']), 'initial': [d['initial_state']], 'labeling': d['labels'],
            'transitions': [[a, b] for a, ts in d['states'].items() for b in ts]}


def memory_kripke(states, edges):
    """Phép chuyển typestate (từ, đến, vi phạm) -> Kripke. Vi phạm nằm trên phép chuyển nên tách thành trạng thái
    riêng mang nhãn violation; trạng thái không có phép chuyển ra được thêm vòng tự lặp như auth_model.py."""
    start = next(iter(states))
    labeling = {s: [v['id']] for s, v in states.items()}
    trans = set()
    for a, b, v in edges:
        if v:
            mid = f'{a}_{v}'
            labeling[mid] = [v, 'violation']
            trans |= {(a, mid), (mid, b)}
        else:
            trans.add((a, b))
    seen = {start} | {s for t in trans for s in t}
    trans |= {(s, s) for s in seen if not any(a == s for a, _ in trans)}
    return {'states': [s for s in labeling if s in seen], 'initial': [start],
            'labeling': {s: labeling[s] for s in labeling if s in seen}, 'transitions': sorted(map(list, trans))}


def branch(path):
    """Nhánh mã theo quy ước của gói: _v0 là mã lỗi cố ý, _v1 là mã đã sửa, còn lại là mã gốc source_v0."""
    return '_v0' if '_v0' in path else '_v1' if '_v1' in path else 'source_v0'


def memory_walk(d, name):
    """Phép chuyển mà các đối tượng của một nhánh thực sự đi qua, phát lại bằng step() của memory_typestate."""
    edges = set()
    for o in d['objects']:
        if branch(o['group']) != name:
            continue
        s, found = next(iter(d['states'])), set()
        for event in o['events']:
            if (s, event) not in TABLE:  # cặp không có trong bảng giữ nguyên trạng thái, không vẽ vòng
                continue
            nxt, v = step(s, event, o['kind'])
            edges.add((s, nxt, v))
            found.add(v)
            s = nxt
        assert found - {None} == set(o['violations']), o['obj']  # phát lại phải ra đúng vi phạm đã ghi
    return edges


# ------------------------------------------------------------------ SMT-LIB -> điều kiện của exe

OPS = {z3.Z3_OP_LE: '<=', z3.Z3_OP_LT: '<', z3.Z3_OP_GE: '>=', z3.Z3_OP_GT: '>',
       z3.Z3_OP_ADD: '+', z3.Z3_OP_SUB: '-', z3.Z3_OP_MUL: '*'}
ATOMS = {z3.Z3_OP_EQ, z3.Z3_OP_DISTINCT, z3.Z3_OP_LE, z3.Z3_OP_LT, z3.Z3_OP_GE, z3.Z3_OP_GT}


def int_ite(e):
    """ite kiểu Int đầu tiên trong một phép so sánh số học; exe không có ite nên phải nhấc ra ngoài."""
    for c in e.children():
        if z3.is_int(c) and c.decl().kind() == z3.Z3_OP_ITE:
            return c
        if z3.is_int(c) and (found := int_ite(c)) is not None:
            return found
    return None


def smt_to_check(path):
    """Một tệp .smt2 (Bool, Int, str.len của String) -> arithmetic_check của exe: and/or/not, so sánh, + - *.
    Bool thành biến nguyên 0/1; String chỉ xuất hiện trong str.len hoặc so bằng một hằng nên thay bằng biến
    độ dài >= 0, không đổi SAT/UNSAT. Gặp cú pháp khác thì báo lỗi thay vì dịch sai."""
    bools, ints, memo, literals = set(), set(), {}, {}

    def ident(e):
        n = re.sub(r'\W', '_', e.decl().name())
        return n + '_' if keyword.iskeyword(n) else n

    def go(e):
        if e.get_id() in memo:
            return memo[e.get_id()]
        k, a = e.decl().kind(), e.children()
        t = int_ite(e) if k in ATOMS and z3.is_int(a[0]) else None
        if t is not None:  # P(ite(c, x, y)) = (c and P(x)) or (not c and P(y)), như min(len, 32) của mô hình bộ đệm C
            c, x, y = t.children()
            r = f'(({go(c)} and {go(z3.substitute(e, (t, x)))}) or ((not {go(c)}) and {go(z3.substitute(e, (t, y)))}))'
        elif z3.is_true(e) or z3.is_false(e):
            r = '(1 == 1)' if z3.is_true(e) else '(0 == 1)'
        elif z3.is_const(e) and k == z3.Z3_OP_UNINTERPRETED and (z3.is_bool(e) or z3.is_int(e)):
            r = ident(e)
            (bools if z3.is_bool(e) else ints).add(r)
            r = f'({r} == 1)' if z3.is_bool(e) else r
        elif z3.is_int_value(e):
            r = str(e.as_long()) if e.as_long() >= 0 else f'(0 - {-e.as_long()})'
        elif k == z3.Z3_OP_SEQ_LENGTH and z3.is_const(a[0]) and a[0].decl().kind() == z3.Z3_OP_UNINTERPRETED:
            r = 'len_' + ident(a[0])
            ints.add(r)
        elif k in (z3.Z3_OP_AND, z3.Z3_OP_OR):
            r = '(' + (' and ' if k == z3.Z3_OP_AND else ' or ').join(map(go, a)) + ')' if a else \
                ('(1 == 1)' if k == z3.Z3_OP_AND else '(0 == 1)')
        elif k == z3.Z3_OP_NOT:
            r = f'(not {go(a[0])})'
        elif k == z3.Z3_OP_IMPLIES:
            r = f'((not {go(a[0])}) or {go(a[1])})'
        elif k == z3.Z3_OP_EQ and z3.is_string(a[0]) and z3.is_string_value(a[1]) and \
                a[0].decl().kind() == z3.Z3_OP_UNINTERPRETED:
            # text == "hằng": khi mỗi biến chỉ so với một hằng, chỉ còn độ dài là quan trọng
            r = 'len_' + ident(a[0])
            literals.setdefault(r, set()).add(a[1].as_string())
            assert len(literals[r]) == 1, (path.name, r)
            ints.add(r)
            r = f'({r} == {len(a[1].as_string())})'
        elif k in (z3.Z3_OP_EQ, z3.Z3_OP_DISTINCT) and len(a) == 2:
            x, y = go(a[0]), go(a[1])
            r = f'(({x} and {y}) or ((not {x}) and (not {y})))' if z3.is_bool(a[0]) else f'({x} == {y})'
            r = f'(not {r})' if k == z3.Z3_OP_DISTINCT else r
        elif k == z3.Z3_OP_ITE and z3.is_bool(e):
            c = go(a[0])
            r = f'(({c} and {go(a[1])}) or ((not {c}) and {go(a[2])}))'
        elif k == z3.Z3_OP_UMINUS:
            r = f'(0 - {go(a[0])})'
        elif k in OPS and a:
            r = '(' + f' {OPS[k]} '.join(map(go, a)) + ')'
        else:
            raise ValueError(f'{path.name}: không dịch được {e.sexpr()[:80]}')
        memo[e.get_id()] = r
        return r

    asserts = z3.parse_smt2_file(str(path))
    body = [go(f) for f in asserts]
    domain = [f'({b} >= 0) and ({b} <= 1)' for b in sorted(bools)] + \
             [f'({v} >= 0)' for v in sorted(ints) if v.startswith('len_')]
    cond = ' and '.join(domain + body) or '(1 == 1)'
    solver = z3.Solver()
    solver.add(asserts)
    status = str(solver.check()).upper()
    int_vars = sorted(bools | ints)
    assert exe_status(cond, int_vars) == status, path.name  # điều kiện đã dịch phải cho cùng kết quả với tệp gốc
    return {'name': f'{path.stem} (kỳ vọng {status})', 'int_vars': int_vars, 'condition': cond, 'overflow_expr': None}


def exe_status(cond, int_vars):
    """Giải điều kiện bằng đúng tập cú pháp exe chấp nhận (BoolOp, Not, Compare, BinOp, Name, Constant)."""
    env = {v: z3.Int(v) for v in int_vars}
    cmp = {ast.Lt: lambda x, y: x < y, ast.LtE: lambda x, y: x <= y, ast.Gt: lambda x, y: x > y,
           ast.GtE: lambda x, y: x >= y, ast.Eq: lambda x, y: x == y, ast.NotEq: lambda x, y: x != y}
    arith = {ast.Add: lambda x, y: x + y, ast.Sub: lambda x, y: x - y, ast.Mult: lambda x, y: x * y}

    def build(n):
        if isinstance(n, ast.BoolOp):
            return (z3.And if isinstance(n.op, ast.And) else z3.Or)(*map(build, n.values))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
            return z3.Not(build(n.operand))
        if isinstance(n, ast.Compare) and len(n.ops) == 1:
            return cmp[type(n.ops[0])](build(n.left), build(n.comparators[0]))
        if isinstance(n, ast.BinOp):
            return arith[type(n.op)](build(n.left), build(n.right))
        if isinstance(n, ast.Name):
            return env[n.id]
        if isinstance(n, ast.Constant) and type(n.value) is int:
            return z3.IntVal(n.value)
        raise ValueError(ast.dump(n)[:80])

    solver = z3.Solver()
    solver.add(build(ast.parse(cond, mode='eval').body))
    return str(solver.check()).upper()


# ------------------------------------------------------------------ yêu cầu và test case

def xlsx_rows(path, sheet):
    """Các dòng của một sheet xlsx dưới dạng dict theo dòng tiêu đề, chỉ dùng thư viện chuẩn."""
    m = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
    r = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
    z = zipfile.ZipFile(path)
    shared = [''.join(t.text or '' for t in si.iter(m + 't')) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))] \
        if 'xl/sharedStrings.xml' in z.namelist() else []  # tệp của nhóm ghi chữ trực tiếp trong ô (inlineStr)
    rid = next(s.get(r + 'id') for s in ET.fromstring(z.read('xl/workbook.xml')).iter(m + 'sheet')
               if s.get('name') == sheet)
    target = next(x.get('Target') for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels')) if x.get('Id') == rid)
    rows = []
    for row in ET.fromstring(z.read('xl/' + target.lstrip('/').removeprefix('xl/'))).iter(m + 'row'):
        cells = {}
        for c in row.iter(m + 'c'):
            v = c.find(m + 'v')
            cells[re.match(r'[A-Z]+', c.get('r')).group()] = (
                shared[int(v.text)] if c.get('t') == 's' else
                ''.join(t.text or '' for t in c.iter(m + 't')) if c.get('t') == 'inlineStr' else
                v.text if v is not None else '')
        rows.append(cells)
    head = rows[0]
    return [{head[k]: v for k, v in row.items() if k in head} for row in rows[1:] if any(row.values())]


def requirements():
    out = [{'id': x['ID'], 'text': x['MoTa'], 'category': x.get('DanhMuc') or 'functional', 'priority': x['MucUuTien']}
           for x in xlsx_rows(XLSX, 'YeuCauChucNang')]
    for sheet in ('YeuCauPhiChucNang', 'RangBuoc'):  # exe chỉ có một danh sách yêu cầu; ghi tên sheet vào category
        out += [{'id': x['ID'], 'text': x['MoTa'], 'category': sheet, 'priority': x['MucUuTien']}
                for x in xlsx_rows(XLSX, sheet)]
    return out


def test_cases():
    """822 dòng TestCase từ case_register.json; exe không có cột thực tế/bằng chứng nên ghi kèm kết quả mong đợi."""
    return [{'id': r[0], 'requirement_ids': [x.strip() for x in r[1].split(',') if x.strip()], 'title': r[2],
             'preconditions': r[3], 'steps': [s for s in re.split(r'\n|;\s*', r[4]) if s.strip()],
             'expected_result': f'{r[5]}\nThực tế: {r[7]}\nBằng chứng: {r[8]}', 'priority': r[6]}
            for r in load(E / 'case_register.json')['master_rows']]


# ------------------------------------------------------------------ các tệp đặc tả

def main():
    OUT.mkdir(exist_ok=True)
    info = {x['Truong']: x['GiaTri'] for x in xlsx_rows(XLSX, 'ThongTin')}
    a0, a1 = load(E / 'auth_model.json'), load(V1 / 'auth_v1.json')
    mem = load(E / 'memory_case_results.json')
    full = {(t['from'], t['to'], t['violation']) for t in mem['transition_table']}
    codes = sorted({v for *_, v in full if v})
    smt = {d: [smt_to_check(p) for p in sorted((E / d).glob('*.smt2'))] for d in ('formal', 'sql_formal', 'memory_formal')}
    specs = {'nhom13_00_tong_hop': {
        'name': 'nhom13_tong_hop', 'description': f"{info.get('description', '')} Yêu cầu và 822 test case truy vết; "
        'phần kiểm chứng nằm ở các tệp 01-04.', 'requirements': requirements(), 'test_cases': test_cases()}}
    for t, main_, o, other in (('v0', a0, 'v1', a1), ('v1', a1, 'v0', a0)):
        specs[f'nhom13_01_xac_thuc_{t}'] = {
            'name': f'nhom13_xac_thuc_{t}', 'description': f'Mô hình trừu tượng đăng nhập → phân quyền → ghi của '
            f'source_{t} (evidence/auth_model.py). Luồng phụ là bản còn lại để đối chiếu.',
            'state_machine': auth_kripke(main_), 'additional_flows': {f'source_{o} (đối chiếu)': auth_kripke(other)},
            'safety_properties': AUTH_CTL}
    specs['nhom13_02_ma_sinh_sat_smt'] = {
        'name': 'nhom13_ma_sinh_sat_smt', 'description': 'CNF (DPLL) và SMT token của mã sinh _v0/_v1, dịch từ '
        'evidence/formal/*.smt2.', 'arithmetic_checks': smt['formal']}
    specs['nhom13_03_sql_sat_smt'] = {
        'name': 'nhom13_sql_sat_smt', 'description': 'CNF binding và SMT trường nhập của các truy vấn SQL, dịch từ '
        'evidence/sql_formal/*.smt2. SQL không có mô hình trạng thái nên không có Kripke.',
        'arithmetic_checks': smt['sql_formal']}
    for b in ('source_v0', '_v0', '_v1'):
        specs[f'nhom13_04_bo_nho_{b.lstrip("_")}'] = {
            'name': f'nhom13_bo_nho_{b.lstrip("_")}', 'description': f'Typestate bộ nhớ: Kripke chính là các phép '
            f'chuyển mà đối tượng nhánh {b} thực sự đi qua; vi phạm tách thành trạng thái mang nhãn violation và '
            'mã lỗi. Luồng phụ là mô hình đầy đủ.',
            'state_machine': memory_kripke(mem['states'], memory_walk(mem, b)),
            'additional_flows': {'Mô hình typestate đầy đủ': memory_kripke(mem['states'], full)},
            'safety_properties': ['AG(!violation)'] + [f'AG(!{c})' for c in codes],
            'arithmetic_checks': [c for c in smt['memory_formal'] if branch(c['name']) == b]}
    for name, s in specs.items():
        (OUT / f'{name}.json').write_text(json.dumps(s, ensure_ascii=False, indent=1) + '\n')
    print({k: len(v) for k, v in smt.items()}, 'ca SMT đã dịch và kiểm lại;', len(specs), 'tệp trong', OUT.name)


if __name__ == '__main__':
    main()
