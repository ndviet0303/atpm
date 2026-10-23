#!/usr/bin/env python3
"""Biên bản kiểm thử dạng Word từ một lần chạy đủ 12 test của chon_test.py.
Dùng: python3 bien_ban_test.py
Script chép gói nộp sang run_output/bien_ban/, chạy lần lượt 12 test bằng chính hàm run() của chon_test.py
(báo cáo HTML vẫn được ghi vào bao_cao.html), rồi ghi outputs/Bien_ban_test_Nhom13.docx.
Chỉ dùng thư viện chuẩn: tệp .docx được ghi thẳng bằng zipfile."""
import os
import platform
import re
import shutil
import subprocess
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import datetime
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

import chon_test as ct

ct.WORK = ct.ROOT / 'run_output/bien_ban'  # bản sao riêng: không đụng bản sao của giao diện chon_test.py đang mở
OUT = ct.ROOT / 'outputs/Bien_ban_test_Nhom13.docx'
REPO = 'https://github.com/ndviet0303/atpm'
WIDTH = 9071  # bề rộng chữ của A4 dọc, lề trái 3 cm, phải 2 cm (DXA)
SEVERITY = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']


# ---------- Chạy test và gom số liệu ----------

def run_all():
    shutil.rmtree(ct.WORK, ignore_errors=True)
    shutil.copytree(ct.PKG, ct.WORK, ignore=shutil.ignore_patterns('~$*', '.DS_Store'))
    start = datetime.now()
    for tid, _, title, *_ in ct.TESTS:
        print(f'{title} ...', end=' ', flush=True)
        ct.run([tid])  # bao_cao.html được dựng lại sau mỗi test, bản cuối có đủ 12 mục
        r = ct.state['result'][tid]
        print(f"{'đạt' if r['status'] == 'ok' else 'LỖI'}, mã {r['code']}, {r['secs']} s", flush=True)
    return start, datetime.now()


def matches(expect, got, code):
    # ponytail: so theo tập số nguyên nên hai số đổi chỗ vẫn lọt; bảng in cả kỳ vọng và thực tế để người ký đối chiếu
    nums = lambda s: set(re.findall(r'(?<![A-Za-z_])\d+', s))  # bỏ chữ số trong _v0, Z3
    return nums(expect) <= nums(got) | {str(code)}


assert matches('8 hit ở _v0, 0 hit ở _v1; lint 10/10', '8 hit ở _v0; 0 hit ở _v1; lint 10/10', 0)
assert not matches('322 kết quả', '321 kết quả, 0 errors', 0)


def results():
    rows = []
    for tid, group, title, _, expect, _ in ct.TESTS:
        r = ct.state['result'][tid]
        try:
            got = ct.actual(tid) if r['status'] == 'ok' else \
                next((line for line in reversed(ct.outputs.get(tid, '').splitlines()) if line.strip()), 'không có output')[:300]
        except Exception as error:  # JSON thiếu trường: ghi vào biên bản thay vì dừng
            got = f'Không đọc được kết quả: {error!r}'
        rows.append((tid, group, title, expect, got, r, r['status'] == 'ok' and matches(expect, got, r['code'])))
    return rows


def version(*cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120).stdout
    except (OSError, subprocess.TimeoutExpired):
        return 'không có'
    return next((line.strip() for line in out.splitlines() if re.search(r'\d+\.\d+', line)), 'không rõ')


def git(*args):
    return subprocess.run(['git', '-C', str(ct.ROOT), *args], capture_output=True, text=True)


def environment():
    mem = ct.load(ct.E + 'memory_static_results.json')['compilers']
    mac = platform.mac_ver()[0]
    return [('Hệ điều hành', f'macOS {mac} ({platform.machine()})' if mac else platform.platform()),
            ('Python (study/.venv)', version(ct.PY, '-V')),
            ('Semgrep', version(ct.SEMGREP, '--version')),
            ('PHP', version('php', '-v')),
            ('PHPStan', version('php', str(ct.ROOT / 'study/phpstan.phar'), '--version')),
            ('Z3', ct.load(ct.E + 'formal_results.json')['z3_version']),
            ('Clang', mem['clang']),
            ('GCC (ảnh Docker)', mem['gcc_image']),
            ('Docker', version('docker', '--version'))]


def findings():
    hits = Counter()
    for h in ct.load(ct.E + 'semgrep_run1.json')['results']:
        find = ct.FINDS.get(h['check_id'].rsplit('.', 1)[-1])
        for num in find.removeprefix('FIND-').split('/') if find else []:
            hits['FIND-' + num] += 1
    rows = []
    for fid, title, sev, cwe, _, locs, *_ in ct.load(ct.E + 'report_case_metadata.json')['findings']:
        where = '; '.join(f'{loc[0]}:{loc[1]}' + (f'–{loc[2]}' if len(loc) > 2 and loc[2] != loc[1] else '') for loc in locs)
        rows.append((fid, title, sev, cwe, where, hits.get(fid, '—')))
    return rows


def memory():
    by_kind = defaultdict(list)
    for f in ct.load(ct.E + 'memory_case_results.json')['findings']:
        if f['file'].startswith('baseline/'):
            by_kind[f['id']].append(f)
    return [(kind, v[0]['label'], ', '.join(v[0]['cwe']), v[0]['severity'].upper(), len(v), len({f['file'] for f in v}))
            for kind, v in sorted(by_kind.items(), key=lambda kv: -len(kv[1]))]


def command(cmd):
    return ' '.join(os.path.basename(c) if c in (ct.PY, ct.SEMGREP) else
                    os.path.relpath(c, ct.WORK) if os.path.isabs(c) else c for c in cmd)


# ---------- WordprocessingML ----------

def x(text):
    return escape(re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', str(text)))


def r(text, b=False, i=False, sz=None, mono=False):
    pr = ('<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/>' if mono else '') + ('<w:b/>' if b else '') + \
        ('<w:i/>' if i else '') + (f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>' if sz else '')
    return f'<w:r><w:rPr>{pr}</w:rPr><w:t xml:space="preserve">{x(text)}</w:t></w:r>'


def p(*runs, style=None, jc=None, before=None):
    pr = (f'<w:pStyle w:val="{style}"/>' if style else '') + \
        (f'<w:spacing w:before="{before}"/>' if before is not None else '') + (f'<w:jc w:val="{jc}"/>' if jc else '')
    return f'<w:p><w:pPr>{pr}</w:pPr>{"".join(run if run.startswith("<w:r>") else r(run) for run in runs)}</w:p>'


def h(level, text):
    return p(text, style=f'Heading{level}')


def cp(*runs, jc=None):
    return p(*runs, style='Cell', jc=jc)


def cell(content, width, fill=None, b=False):
    if isinstance(content, tuple):  # (nội dung, màu nền)
        content, fill = content
    paras = content if isinstance(content, list) else [str(content)]
    body = ''.join(c if c.startswith('<w:p>') else cp(r(c, b=b)) for c in paras)
    shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>' if fill else ''
    return f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shd}</w:tcPr>{body}</w:tc>'


def table(widths, head, rows, borders=True):
    assert sum(widths) == WIDTH, widths
    edge = '<w:{} w:val="single" w:sz="4" w:space="0" w:color="808080"/>' if borders else '<w:{} w:val="nil"/>'
    out = (f'<w:tbl><w:tblPr><w:tblW w:w="{WIDTH}" w:type="dxa"/><w:tblBorders>'
           + ''.join(edge.format(e) for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
           + '</w:tblBorders><w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="80" w:type="dxa"/>'
           '<w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>'
           + ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths) + '</w:tblGrid>')
    if head:
        out += '<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>' + \
            ''.join(cell(c, w, 'D9E2F3', True) for c, w in zip(head, widths)) + '</w:tr>'
    out += ''.join('<w:tr><w:trPr><w:cantSplit/></w:trPr>' + ''.join(cell(c, w) for c, w in zip(row, widths)) + '</w:tr>'
                   for row in rows)
    return out + '</w:tbl>' + cp()  # đoạn trống để hai bảng liền nhau không bị Word gộp


def build(start, end):
    prov, summary = ct.load('provenance.json'), ct.load(ct.E + 'static_summary.json')
    rows, finds, mem = results(), findings(), memory()
    ok = sum(row[-1] for row in rows)
    commit = git('rev-parse', '--short', 'HEAD').stdout.strip()
    dirty = git('diff', '--quiet', 'HEAD').returncode != 0
    sev = Counter(f[2] for f in finds)
    sev_text = ', '.join(f'{s} {sev[s]}' for s in SEVERITY if sev[s])
    mem_total, mem_files = sum(m[4] for m in mem), len({f['file'] for f in ct.load(ct.E + 'memory_case_results.json')['findings']
                                                         if f['file'].startswith('baseline/')})
    failed = [row[2] for row in rows if not row[-1]]
    label = lambda text: cp(r(text, b=True))

    body = [
        p(r('HỌC PHẦN CSE703093 – AN TOÀN PHẦN MỀM', b=True), jc='center'),
        p(r(f'NHÓM {prov["group"]}', b=True), jc='center'),
        p('BIÊN BẢN KIỂM THỬ', style='Title'),
        p(r('Kiểm thử tĩnh mã nguồn hệ thống quản lý thư viện (phân hệ thủ thư)', i=True), jc='center'),

        h(1, '1. Thông tin chung'),
        table([2600, 6471], None, [
            [label('Đề tài'), 'Kiểm thử tĩnh mã nguồn hệ thống quản lý thư viện'],
            [label('Nhóm thực hiện'), [cp(f'{m["name"]} – {m["student_id"]}') for m in prov['members']]],
            [label('Đối tượng kiểm thử'), f'{prov["baseline_upstream"]}, commit {prov["baseline_commit"]}; '
                                          f'{summary["php_file_count"]} tệp PHP trong librarian/ và db/eb_lms.sql, '
                                          'không tính assets/vendor (source_v0 trong gói nộp)'],
            [label('Loại kiểm thử'), 'Kiểm thử tĩnh: kiểm kê và lint, Semgrep SAST, PHPStan, mã sinh, mô hình SAT/SMT, '
                                     'mô hình xác thực, phân tích bộ nhớ. Không chạy ứng dụng, không kết nối CSDL.'],
            [label('Kho mã'), f'{REPO}, commit {commit}' + (' (có sửa đổi chưa commit)' if dirty else '')],
            [label('Công cụ chạy'), f'chon_test.py, {len(rows)} test, gọi qua bien_ban_test.py; chạy trên bản sao '
                                    f'{ct.WORK.relative_to(ct.ROOT)}/ nên gói nộp không bị ghi đè'],
            [label('Thời gian chạy'), f'{start:%d/%m/%Y %H:%M:%S} – {end:%H:%M:%S} '
                                      f'({round((end - start).total_seconds())} giây)'],
            [label('Báo cáo chi tiết'), f'{ct.WORK.relative_to(ct.ROOT)}/bao_cao.html (phát hiện theo rule, vị trí, dòng mã)'],
        ]),

        h(1, '2. Môi trường kiểm thử'),
        table([2600, 6471], ['Thành phần', 'Phiên bản'], [list(e) for e in environment()]),

        h(1, '3. Kết quả kiểm thử'),
        p(f'Chạy {len(rows)} test, đạt {ok}/{len(rows)}. Một test đạt khi mã thoát nằm trong tập mã chấp nhận và mọi số '
          'liệu ở cột Kỳ vọng (lấy từ README của gói nộp) đều có trong cột Thực tế. Lệnh chạy và tệp bằng chứng của '
          'từng test ở Phụ lục.'),
        table([500, 2500, 2150, 2350, 771, 800], ['#', 'Test', 'Kỳ vọng', 'Thực tế', 'Mã / giây', 'Kết quả'], [
            [cp(str(n), jc='center'), [cp(r(title, b=True)), cp(r(f'{tid} · {group}', i=True, sz=16))], expect, got,
             cp(f"{res['code']} / {res['secs']}", jc='center'),
             (cp(r('Đạt' if good else 'Không đạt', b=True), jc='center'), 'E2EFDA' if good else 'F8CBAD')]
            for n, (tid, group, title, expect, got, res, good) in enumerate(rows, 1)]),

        h(1, '4. Lỗi phát hiện'),
        h(2, f'4.1. Sổ phát hiện an toàn ({len(finds)} phát hiện)'),
        p(f'Theo mức: {sev_text}. Nguồn: evidence/report_case_metadata.json. Cột Hit Semgrep đếm cảnh báo của lần chạy '
          'này ở các rule được gán cho phát hiện (một rule có thể gán cho nhiều phát hiện, như FIND-01/03, nên cột này '
          'không cộng dồn); dấu — nghĩa là chon_test.py không gán rule Semgrep nào cho phát hiện '
          'đó (xác nhận bằng rà soát thủ công theo checklist).'),
        table([1000, 2650, 1250, 1100, 1971, 1100], ['ID', 'Phát hiện', 'Mức', 'CWE', 'Vị trí', 'Hit Semgrep'],
              [[cp(r(fid, b=True)), title, sev, cwe, cp(r(where, sz=16)), cp(str(n), jc='center')]
               for fid, title, sev, cwe, where, n in finds]),
        h(2, '4.2. Lỗi bộ nhớ theo loại'),
        p(f'{mem_total} vi phạm trên {mem_files} tệp baseline, từ test "Trạng thái, BMC, ngân sách, bộ đệm C" '
          '(evidence/memory_case_results.json).'),
        table([2300, 3271, 1500, 1000, 1000], ['Mã', 'Mô tả', 'CWE', 'Mức', 'Vi phạm (tệp)'],
              [[cp(r(kind, sz=16, mono=True)), label_, cwe, sev_, cp(f'{n} ({files})', jc='center')]
               for kind, label_, cwe, sev_, n, files in mem]),

        h(1, '5. Kiểm thử lại trên source_v1'),
        p(r('Chưa thực hiện. Phần này để trống, chờ thư mục bo_sung_v1/ (mã đã sửa source_v1 và bằng chứng sau sửa) '
            'được đưa vào gói nộp. Khi có, chạy lại các test trên source_v1 và điền bảng dưới.', i=True)),
        table([2600, 2150, 2150, 2171], ['Test', 'Kết quả trên source_v0', 'Kết quả trên source_v1', 'Nhận xét'],
              [[''] * 4 for _ in range(5)]),

        h(1, '6. Kết luận'),
        p(f'Lần chạy ngày {start:%d/%m/%Y} thực hiện đủ {len(rows)} test của chon_test.py: {ok} đạt, '
          f'{len(rows) - ok} không đạt' + (f' ({", ".join(failed)}).' if failed else '; số liệu thực tế khớp kỳ vọng '
                                           'ghi trong README của gói nộp ở mọi test.')),
        p(f'Trên source_v0, sổ phát hiện ghi {len(finds)} phát hiện an toàn ({sev_text}); phân tích bộ nhớ ghi '
          f'{mem_total} vi phạm trên {mem_files} tệp.'),
        p('Phần kiểm thử lại trên source_v1 (mục 5) chưa thực hiện; biên bản sẽ được cập nhật khi có bo_sung_v1/.'),

        h(1, '7. Xác nhận'),
        p(r('Ngày ...... tháng ...... năm ............', i=True), jc='right'),
        table([3023, 3024, 3024], None, [
            [[cp(r('Thành viên', b=True), jc='center'), cp(r('(Ký, ghi rõ họ tên)', i=True, sz=18), jc='center'),
              *[cp() for _ in range(4)], cp(r(m['name'], b=True), jc='center')] for m in prov['members']]], borders=False),

        '<w:p><w:r><w:br w:type="page"/></w:r></w:p>',
        h(1, 'Phụ lục. Lệnh chạy và tệp bằng chứng'),
        p(f'Mọi lệnh chạy trong {ct.WORK.relative_to(ct.ROOT)}/; python là study/.venv/bin/python.'),
        table([1500, 4371, 3200], ['Test', 'Lệnh', 'Tệp kết quả'], [
            [cp(r(tid, sz=16, mono=True)), cp(r(command(cmd), sz=16, mono=True)),
             [cp(r(f, sz=16)) for f in ct.VIEW.get(tid, ['— (kết quả nằm trong log)'])]]
            for tid, _, _, cmd, _, _ in ct.TESTS]),
    ]
    return ''.join(body), all(row[-1] for row in rows)


NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
HEAD = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
CT = 'application/vnd.openxmlformats-officedocument.wordprocessingml.'
STYLES = f'''{HEAD}<w:styles {NS}><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" \
w:hAnsi="Times New Roman" w:eastAsia="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="26"/><w:szCs w:val="26"/>\
<w:lang w:val="vi-VN"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" \
w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>\
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>\
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr>\
<w:spacing w:before="240" w:after="120"/><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/>\
</w:rPr></w:style>\
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next \
w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr>\
<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>\
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next \
w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="180" w:after="80"/><w:outlineLvl w:val="1"/></w:pPr>\
<w:rPr><w:b/><w:i/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>\
<w:style w:type="paragraph" w:styleId="Cell"><w:name w:val="Table Text"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr>\
<w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="20"/>\
<w:szCs w:val="20"/></w:rPr></w:style></w:styles>'''
FOOTER = (f'{HEAD}<w:ftr {NS}><w:p><w:pPr><w:jc w:val="center"/></w:pPr>{r("Biên bản kiểm thử – Nhóm 13 – Trang ", sz=20)}'
          '<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
          '<w:r><w:fldChar w:fldCharType="separate"/></w:r>' + r('1', sz=20) +
          '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>')
PARTS = {
    '[Content_Types].xml': f'{HEAD}<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    f'<Override PartName="/word/document.xml" ContentType="{CT}document.main+xml"/>'
    f'<Override PartName="/word/styles.xml" ContentType="{CT}styles+xml"/>'
    f'<Override PartName="/word/footer1.xml" ContentType="{CT}footer+xml"/></Types>',
    '_rels/.rels': f'{HEAD}<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    f'<Relationship Id="rId1" Type="{REL}officeDocument" Target="word/document.xml"/></Relationships>',
    'word/_rels/document.xml.rels': f'{HEAD}<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    f'<Relationship Id="rIdStyles" Type="{REL}styles" Target="styles.xml"/>'
    f'<Relationship Id="rIdFooter" Type="{REL}footer" Target="footer1.xml"/></Relationships>',
    'word/styles.xml': STYLES,
    'word/footer1.xml': FOOTER,
}


def write(body):
    document = (f'{HEAD}<w:document {NS}><w:body>{body}<w:sectPr><w:footerReference w:type="default" r:id="rIdFooter"/>'
                '<w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1701" '
                'w:header="567" w:footer="567" w:gutter="0"/></w:sectPr></w:body></w:document>')
    parts = dict(PARTS, **{'word/document.xml': document})
    for xml in parts.values():
        ET.fromstring(xml.encode())  # tự kiểm: mọi phần đều là XML hợp lệ trước khi đóng gói
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, xml in parts.items():
            z.writestr(name, xml)


if __name__ == '__main__':
    start, end = run_all()
    body, all_ok = build(start, end)
    write(body)
    print(f'Đã ghi biên bản: {OUT}')
    sys.exit(0 if all_ok else 1)
