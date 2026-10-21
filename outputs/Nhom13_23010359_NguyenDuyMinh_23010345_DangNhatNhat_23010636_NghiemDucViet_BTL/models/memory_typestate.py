"""Static memory/resource typestate for PHP token streams.

Reads tokens produced by evidence/extract_memory_tokens.php. Never runs target PHP functions, DB or HTTP.
TABLE drives both the path-insensitive walker here and the concrete Z3 model in run_memory_cases.py.
"""
from pathlib import Path
import json
import re
import subprocess

BASE = Path(__file__).resolve().parents[1]
E = BASE / 'evidence'

STATES = {
    'UNDEF': ('P0', 'Biến chưa gán, chưa trỏ tới vùng nhớ hay resource nào'),
    'PENDING': ('P1', 'Vừa gọi hàm cấp phát, chưa kiểm tra; có thể là FALSE'),
    'FALSE': ('P2', 'Cấp phát thất bại, giá trị FALSE'),
    'ALLOCATED': ('P3', 'Resource hoặc bộ đệm kết quả hợp lệ, refcount >= 1'),
    'ROW_PENDING': ('P4', 'Mảng dòng vừa fetch, chưa kiểm tra; có thể FALSE khi hết dòng'),
    'ROW': ('P5', 'Mảng dòng hợp lệ đã kiểm tra'),
    'NOROW': ('P6', 'Fetch trả FALSE vì hết dòng'),
    'SECRET': ('P7', 'Chuỗi mật khẩu hoặc khóa dạng rõ đang nằm trong heap'),
    'WIPED': ('P8', 'Chuỗi bí mật đã ghi đè 0 bằng sodium_memzero'),
    'RELEASED': ('P9', 'Refcount về 0 hoặc đã free/close/unset'),
    'ESCAPED': ('P10', 'Trả về nơi gọi, quyền sở hữu chuyển ra ngoài'),
    'HELD_TO_END': ('P11', 'Vẫn giữ tới khi request kết thúc, engine dọn ở shutdown'),
    'DONE': ('P12', 'Nhánh lỗi đã thoát (die/exit/throw)'),
}

VIOLATIONS = {
    'E_USE_FALSE': (['CWE-252', 'CWE-690'], 'medium', 'Dùng kết quả cấp phát khi chưa loại trừ FALSE'),
    'E_ROW_UNCHECKED': (['CWE-252'], 'low', 'Đọc chỉ mục trên dòng fetch chưa kiểm tra FALSE'),
    'E_USE_RELEASED': (['CWE-672'], 'medium', 'Dùng resource sau khi đã giải phóng'),
    'E_DOUBLE_RELEASE': (['CWE-675'], 'low', 'Giải phóng một resource hai lần'),
    'E_HELD_TO_END': (['CWE-772'], 'low', 'Resource không giải phóng sau vòng đời hiệu dụng, giữ tới hết request'),
    'E_SECRET_RESIDUE': (['CWE-226', 'CWE-316'], 'low', 'Bí mật dạng rõ còn trong heap, không xóa trước khi giải phóng'),
    'E_UNBOUNDED_ALLOC': (['CWE-770', 'CWE-400'], 'medium', 'Bộ đệm kết quả SELECT không có cận trên số dòng'),
    'E_ALLOC_IN_LOOP': (['CWE-1050'], 'medium', 'Cấp phát kết quả truy vấn mới ở mỗi vòng lặp (N+1)'),
}

# (state, event) -> (next state, violation). Pairs not listed keep the state.
TABLE = {
    ('UNDEF', 'alloc'): ('PENDING', None),
    ('UNDEF', 'alloc_checked'): ('ALLOCATED', None),
    ('UNDEF', 'fetch'): ('ROW_PENDING', None),
    ('UNDEF', 'fetch_checked'): ('ROW', None),
    ('UNDEF', 'secret'): ('SECRET', None),
    ('PENDING', 'check'): ('ALLOCATED', None),
    ('PENDING', 'use'): ('ALLOCATED', 'E_USE_FALSE'),
    ('PENDING', 'release'): ('RELEASED', None),
    ('PENDING', 'drop'): ('RELEASED', None),
    ('PENDING', 'return'): ('ESCAPED', None),
    ('PENDING', 'end'): ('HELD_TO_END', 'E_HELD_TO_END'),
    ('ALLOCATED', 'release'): ('RELEASED', None),
    ('ALLOCATED', 'drop'): ('RELEASED', None),
    ('ALLOCATED', 'return'): ('ESCAPED', None),
    ('ALLOCATED', 'end'): ('HELD_TO_END', 'E_HELD_TO_END'),
    ('ROW_PENDING', 'check'): ('ROW', None),
    ('ROW_PENDING', 'read'): ('ROW', 'E_ROW_UNCHECKED'),
    ('ROW_PENDING', 'release'): ('RELEASED', None),
    ('ROW_PENDING', 'drop'): ('RELEASED', None),
    ('ROW_PENDING', 'return'): ('ESCAPED', None),
    ('ROW_PENDING', 'end'): ('HELD_TO_END', None),
    ('ROW', 'release'): ('RELEASED', None),
    ('ROW', 'drop'): ('RELEASED', None),
    ('ROW', 'return'): ('ESCAPED', None),
    ('ROW', 'end'): ('HELD_TO_END', None),
    ('SECRET', 'wipe'): ('WIPED', None),
    ('SECRET', 'release'): ('RELEASED', 'E_SECRET_RESIDUE'),
    ('SECRET', 'drop'): ('RELEASED', 'E_SECRET_RESIDUE'),
    ('SECRET', 'return'): ('ESCAPED', None),
    ('SECRET', 'end'): ('HELD_TO_END', 'E_SECRET_RESIDUE'),
    ('WIPED', 'release'): ('RELEASED', None),
    ('WIPED', 'drop'): ('RELEASED', None),
    ('WIPED', 'end'): ('RELEASED', None),
    ('RELEASED', 'use'): ('RELEASED', 'E_USE_RELEASED'),
    ('RELEASED', 'read'): ('RELEASED', 'E_USE_RELEASED'),
    ('RELEASED', 'release'): ('RELEASED', 'E_DOUBLE_RELEASE'),
}
EVENTS = ['alloc', 'alloc_checked', 'fetch', 'fetch_checked', 'secret', 'share', 'check',
          'use', 'read', 'wipe', 'release', 'drop', 'return', 'end']
CHOICE_EVENTS = {'alloc', 'alloc_checked', 'fetch', 'fetch_checked'}
RESOURCE_KINDS = {'link', 'result', 'stmt'}


def step(state, event, kind='result'):
    """Abstract transition: PENDING/ROW_PENDING stand for both outcomes of the call."""
    nxt, violation = TABLE.get((state, event), (state, None))
    if violation == 'E_HELD_TO_END' and kind not in RESOURCE_KINDS:
        violation = None
    return nxt, violation


def concrete_step(state, event, ok, kind='result'):
    """One concrete path: ok=True means the allocation succeeded / a row exists."""
    if state in ('DONE', 'ESCAPED', 'HELD_TO_END'):
        return state, None
    if event in CHOICE_EVENTS:
        success = 'ROW' if event.startswith('fetch') else 'ALLOCATED'
        failure = 'DONE' if event.endswith('_checked') else ('NOROW' if event == 'fetch' else 'FALSE')
        return (success if ok else failure), None
    if state in ('FALSE', 'NOROW'):
        if (state, event) in (('FALSE', 'use'), ('NOROW', 'read')):
            return state, 'E_USE_FALSE' if state == 'FALSE' else 'E_ROW_UNCHECKED'
        if event == 'check':
            return 'DONE', None
        return ('RELEASED', None) if event in ('drop', 'release', 'end') else (state, None)
    return step(state, event, kind)

# ---------------------------------------------------------------- schema and SQL row bounds


def schema(path=None):
    text = Path(path or BASE / 'source_v0/db/eb_lms.sql').read_text()
    tables = {}
    for table, body in re.findall(r'CREATE TABLE IF NOT EXISTS `(\w+)` \((.*?)\) ENGINE=', text, re.S):
        columns = {}
        for name, kind, width in re.findall(r'^\s*`(\w+)`\s+(\w+)(?:\((\d+)\))?', body, re.M):
            fixed = {'datetime': 19, 'timestamp': 19, 'date': 10, 'text': 65535}.get(kind.lower())
            columns[name.lower()] = fixed or int(width or 11)
        pk = re.search(r'PRIMARY KEY \(`(\w+)`\)', body)
        tables[table.lower()] = {'columns': columns, 'pk': pk[1].lower() if pk else None,
                                 'row_width': sum(columns.values())}
    return tables


def sql_bound(sql, tables):
    """Upper bound on rows a SELECT buffers, from the SQL text and the schema only."""
    s = ' '.join((sql or '').lower().split())
    info = {'sql': sql, 'select': s.startswith(('select', 'show')), 'tables': [], 'limit': None,
            'pk_equality': False, 'aggregate': False, 'bounded': True, 'max_rows': 0,
            'row_width': None, 'reason': 'Không phải SELECT: không tạo result set'}
    if not info['select']:
        return info
    named = re.findall(r'\b(?:from|join)\s+`?(\w+)`?', s)
    info['tables'] = [t for t in named if t in tables]
    main = named[0] if named else None
    if main not in tables:
        info.update(bounded=False, max_rows=None, reason=f'Bảng {main} không có trong schema eb_lms.sql: không chặn được')
        return info
    limit = re.search(r'\blimit\s+(\d+)(?:\s*,\s*(\d+))?', s)
    info['limit'] = int(limit[2] or limit[1]) if limit else None
    where = s.split(' where ', 1)[1] if ' where ' in s else ''
    pk = tables[main]['pk']
    info['pk_equality'] = bool(pk and re.search(rf'(?<![\w.])(?:{main}\.)?{pk}\s*=', where))
    info['aggregate'] = bool(re.match(r'select\s+count\s*\(', s)) and ' group by ' not in s
    chosen = (re.match(r'select\s+(.*?)\s+from\s', s) or [None, '*'])[1]
    info['row_width'] = sum(w for t in info['tables'] for c, w in tables[t]['columns'].items()
                            if '*' in chosen or re.search(rf'(?<!\w){c}(?!\w)', chosen)) or None
    if info['aggregate']:
        info.update(max_rows=1, reason='Hàm gộp không GROUP BY: một dòng')
    elif info['pk_equality']:
        info.update(max_rows=1, reason=f'So bằng khóa chính {main}.{pk}')
    elif info['limit'] is not None:
        info.update(max_rows=info['limit'], reason=f'LIMIT {info["limit"]}')
    else:
        info.update(bounded=False, max_rows=None,
                    reason=f'Không LIMIT, không lọc theo khóa chính: số dòng tăng theo bảng {main}')
    return info

# ---------------------------------------------------------------- tokens -> statement units


SKIP = {'T_WHITESPACE', 'T_COMMENT', 'T_DOC_COMMENT', 'T_INLINE_HTML', 'T_OPEN_TAG'}
CONTROL = {'T_WHILE', 'T_FOR', 'T_FOREACH', 'T_IF', 'T_ELSEIF', 'T_SWITCH', 'T_DO', 'T_ELSE',
           'T_TRY', 'T_CATCH', 'T_FINALLY', 'T_FUNCTION'}
STRING_TOKENS = ('T_CONSTANT_ENCAPSED_STRING', 'T_ENCAPSED_AND_WHITESPACE')


def tokens_for(paths):
    run = subprocess.run(['php', str(E / 'extract_memory_tokens.php'), *map(str, paths)],
                         capture_output=True, text=True, check=True)
    return json.loads(run.stdout)


def clean(tokens):
    """Drop layout tokens; '?>' ends a statement. Each token keeps a 'space before' flag for display."""
    out, space = [], False
    for name, text, line in tokens:
        if name in SKIP:
            space = True
            continue
        if name == 'T_CLOSE_TAG':
            name, text = 'CHAR', ';'
        elif name == 'T_OPEN_TAG_WITH_ECHO':
            name, text = 'T_ECHO', 'echo'
        out.append([name, text, line, space])
        space = False
    return out


def is_char(tok, ch):
    return tok[0] == 'CHAR' and tok[1] == ch


def delta(tok):
    if tok[0] in ('T_CURLY_OPEN', 'T_DOLLAR_OPEN_CURLY_BRACES'):
        return 1
    return (tok[1] in '([{') - (tok[1] in ')]}') if tok[0] == 'CHAR' else 0


def match_close(toks, i):
    depth = 0
    for j in range(i, len(toks)):
        depth += delta(toks[j])
        if depth == 0:
            return j
    raise ValueError(f'unbalanced {toks[i][1]} at line {toks[i][2]}')


class Parser:
    """Flat units in source order; if/else bodies run in sequence, loop bodies are unrolled twice."""

    def __init__(self, toks):
        self.t = toks

    def parse(self):
        return self.block(0, False)[0]

    def block(self, i, braced):
        t, units, buf, depth = self.t, [], [], 0

        def flush():
            if buf:
                units.append({'type': 'stmt', 'tokens': buf[:], 'line': buf[0][2]})
                buf.clear()
        while i < len(t):
            tok = t[i]
            if depth == 0:
                if braced and is_char(tok, '}'):
                    flush()
                    return units, i + 1
                if not buf and tok[0] in CONTROL:
                    more, i = self.control(i)
                    units += more
                    continue
                if not buf and tok[0] in ('T_CASE', 'T_DEFAULT'):
                    while not (is_char(t[i], ':') or is_char(t[i], ';')):
                        i += 1
                    i += 1
                    continue
                if is_char(tok, '{') or is_char(tok, ';'):
                    flush()
                    if tok[1] == ';':
                        i += 1
                    else:
                        inner, i = self.block(i + 1, True)
                        units += inner
                    continue
            depth += delta(tok)
            buf.append(tok)
            i += 1
        flush()
        return units, i

    def body(self, i):
        t = self.t
        if is_char(t[i], '{'):
            return self.block(i + 1, True)
        if is_char(t[i], ':'):
            raise ValueError(f'alternative syntax at line {t[i][2]} is not supported')
        if t[i][0] in CONTROL:
            return self.control(i)
        j, depth = i, 0
        while not (depth == 0 and is_char(t[j], ';')):
            depth += delta(t[j])
            j += 1
        return ([{'type': 'stmt', 'tokens': t[i:j], 'line': t[i][2]}] if j > i else []), j + 1

    @staticmethod
    def unroll(iteration):
        def mark(n):
            return [dict(u, iter=f'{n}.{u["iter"]}' if 'iter' in u else str(n)) for u in iteration]
        line = iteration[0]['line'] if iteration else 0
        return [{'type': 'loop_start', 'line': line}] + mark(1) + mark(2) + [{'type': 'loop_end', 'line': line}]

    def control(self, i):
        t, name, line = self.t, self.t[i][0], self.t[i][2]
        if name == 'T_FUNCTION':
            fname = t[i + 1][1] if t[i + 1][0] == 'T_STRING' else '<closure>'
            k = next(k for k in range(i, len(t)) if is_char(t[k], '{'))
            params = [tok[1] for tok in t[i:k] if tok[0] == 'T_VARIABLE']
            inner, end = self.block(k + 1, True)
            return ([{'type': 'func_start', 'name': fname, 'params': params, 'line': line}] + inner
                    + [{'type': 'func_end', 'name': fname, 'line': t[end - 1][2]}]), end
        if name in ('T_ELSE', 'T_TRY', 'T_FINALLY'):
            return self.body(i + 1)
        if name == 'T_DO':
            body, j = self.body(i + 1)
            close = match_close(t, j + 1)
            return self.unroll(body + [{'type': 'cond', 'tokens': t[j + 2:close], 'line': t[j][2]}]), close + 2
        close = match_close(t, i + 1)
        header = t[i + 2:close]
        body, end = self.body(close + 1)
        cond = [{'type': 'cond', 'tokens': header, 'line': line}]
        if name == 'T_CATCH':
            return body, end
        if name in ('T_IF', 'T_ELSEIF', 'T_SWITCH'):
            return cond + body, end
        if name in ('T_WHILE', 'T_FOREACH'):
            return self.unroll(cond + body), end
        parts, cur, depth = [], [], 0
        for tok in header:
            if depth == 0 and is_char(tok, ';'):
                parts.append(cur)
                cur = []
                continue
            depth += delta(tok)
            cur.append(tok)
        init, test, inc = parts[0], parts[1], cur
        pre = [{'type': 'stmt', 'tokens': init, 'line': line}] if init else []
        test = [{'type': 'cond', 'tokens': test, 'line': line}] if test else []
        inc = [{'type': 'stmt', 'tokens': inc, 'line': line}] if inc else []
        return pre + self.unroll(test + body + inc), end

# ---------------------------------------------------------------- walker


SECRET_NAME = re.compile(r'(^|_)(pass|passwd|password|secret|key)$', re.I)
SECRET_SOURCES = {'$_POST', '$_GET', '$_REQUEST', '$_COOKIE'}
SECRET_CALLS = {'getenv', 'base64_decode', 'hex2bin', 'random_bytes'}
KEY_LOADER = re.compile(r'(^|_)(key|secret)(_|$)')
PROPAGATING_CALLS = {'base64_decode', 'base64_encode', 'trim', 'substr', 'sprintf', 'hex2bin',
                     'bin2hex', 'strtolower', 'strtoupper'}
FETCH_CALLS = {'mysql_fetch_array', 'mysql_fetch_assoc', 'mysql_fetch_row', 'mysql_fetch_object'}
USE_CALLS = FETCH_CALLS | {'mysql_num_rows', 'mysql_result', 'mysql_data_seek', 'mysql_num_fields',
                           'mysql_field_name'}
CHECK_CALLS = {'is_array', 'is_resource', 'is_object', 'is_string', 'isset', 'empty'}
STMT_METHODS = {'execute', 'rowcount', 'bindvalue', 'bindparam', 'closecursor', 'columncount',
                'setfetchmode', 'fetch', 'fetchall', 'fetchcolumn', 'fetchobject'}


class Obj:
    def __init__(self, oid, kind, var, line, sql=None, bound=None):
        self.id, self.kind, self.var, self.line, self.sql, self.bound = oid, kind, var, line, sql, bound
        self.state, self.refs, self.timeline = 'UNDEF', set(), []


class Walker:
    def __init__(self, file, units, tables, php8=False):
        self.file, self.units, self.tables, self.php8 = file, units, tables, php8
        self.objs, self.scopes = {}, [self.new_scope('<global>')]
        self.trace, self.violations, self._seen = [], [], set()
        self.loop_depth, self.iter = 0, '0'

    def new_scope(self, name):
        # counts: $n = mysql_num_rows($r) -> id of $r, so "if ($n > 0)" also checks rows fetched from $r
        return {'name': name, 'vars': {}, 'strings': {}, 'counts': {}, 'pdo_exc': self.php8}

    @property
    def scope(self):
        return self.scopes[-1]

    def new(self, kind, var, line, **extra):
        obj = Obj(f'{self.file}#{len(self.objs) + 1}', kind, var, line, **extra)
        self.objs[obj.id] = obj
        return obj

    def obj_of(self, var):
        return self.objs.get(self.scope['vars'].get(var))

    def emit(self, obj, event, line, stmt, var=None, note=None):
        before = obj.state
        obj.state, violation = step(before, event, obj.kind)
        obj.timeline.append(event)
        self.trace.append({'file': self.file, 'line': line, 'iter': self.iter, 'stmt': stmt,
                           'var': var or obj.var, 'obj': obj.id, 'kind': obj.kind, 'event': event,
                           'from': before, 'to': obj.state, 'violation': violation, 'note': note})
        if violation:
            self.flag(violation, line, var or obj.var, stmt, obj)

    def flag(self, violation, line, var, stmt, obj, extra=None):
        if (violation, line, var) in self._seen:
            return
        self._seen.add((violation, line, var))
        cwe, severity, label = VIOLATIONS[violation]
        self.violations.append({'id': violation, 'cwe': cwe, 'severity': severity, 'label': label,
                                'file': self.file, 'line': line, 'var': var, 'stmt': stmt,
                                'obj': obj.id, 'kind': obj.kind, **(extra or {})})

    def bind(self, var, obj, line, stmt):
        self.unbind(var, line, stmt)
        if obj is not None:
            self.scope['vars'][var] = obj.id
            obj.refs.add((len(self.scopes), var))

    def unbind(self, var, line, stmt, event='drop'):
        old = self.obj_of(var)
        if old is None:
            return
        del self.scope['vars'][var]
        old.refs.discard((len(self.scopes), var))
        if not old.refs and old.state not in ('RELEASED', 'ESCAPED'):
            self.emit(old, event, line, stmt, var, note='refcount về 0' if event == 'drop' else None)

    def run(self):
        for unit in self.units:
            self.iter = unit.get('iter', '0')
            kind = unit['type']
            if kind == 'loop_start':
                self.loop_depth += 1
            elif kind == 'loop_end':
                self.loop_depth -= 1
            elif kind == 'func_start':
                self.scopes.append(self.new_scope(unit['name']))
                for p in filter(lambda p: SECRET_NAME.search(p[1:]), unit['params']):
                    obj = self.new('secret', p, unit['line'])
                    obj.borrowed = True
                    self.bind(p, obj, unit['line'], f'function {unit["name"]}(... {p})')
                    self.emit(obj, 'secret', unit['line'], f'function {unit["name"]}(... {p})', p,
                              note='tham số: chuỗi do nơi gọi sở hữu')
            elif kind == 'func_end':
                for var in list(self.scope['vars']):
                    obj = self.obj_of(var)
                    if getattr(obj, 'borrowed', False) and obj.state == 'SECRET':
                        self.emit(obj, 'return', unit['line'], f'}} // hết hàm {unit["name"]}', var,
                                  note='refcount giảm, chuỗi vẫn thuộc nơi gọi')
                for var in list(self.scope['vars']):
                    self.unbind(var, unit['line'], f'}} // hết hàm {unit["name"]}')
                self.scopes.pop()
            elif unit['tokens']:
                self.statement(unit['tokens'], unit['line'], cond=kind == 'cond')
        end = max((u['line'] for u in self.units), default=1)
        self.iter = '0'
        for var in list(self.scope['vars']):
            obj = self.obj_of(var)
            if obj.state not in ('RELEASED', 'ESCAPED', 'HELD_TO_END'):
                self.emit(obj, 'end', end, '<kết thúc request>', var)
        for obj in self.objs.values():
            if obj.var == '<default-link>' and obj.state not in ('RELEASED', 'HELD_TO_END'):
                self.emit(obj, 'end', end, '<kết thúc request>')
        return self

    def statement(self, toks, line, cond=False):
        stmt = ''.join((' ' if t[3] else '') + t[1] for t in toks).strip()[:200]
        names, text, n = [t[0] for t in toks], [t[1] for t in toks], len(toks)
        start = 0
        while cond and start < n and toks[start][0] == 'CHAR' and toks[start][1] in '(!@':
            start += 1
        target, rhs_start = None, 0
        if start + 1 < n and names[start] == 'T_VARIABLE':
            if is_char(toks[start + 1], '='):
                target, rhs_start = text[start], start + 2
            elif is_char(toks[start + 1], '['):
                close = match_close(toks, start + 1)
                if close + 1 < n and is_char(toks[close + 1], '='):
                    rhs_start = close + 2
        elif names[0] == 'T_RETURN':
            rhs_start = 1
        rhs = toks[rhs_start:]
        or_die = any(names[k] in ('T_LOGICAL_OR', 'T_BOOLEAN_OR') and names[k + 1] == 'T_EXIT'
                     for k in range(n - 1))
        if 'ERRMODE_EXCEPTION' in text:
            self.scope['pdo_exc'] = True

        # (name, receiver, argument tokens, index where the call expression starts)
        calls = []
        for k in range(rhs_start, n - 1):
            if names[k] in ('T_STRING', 'T_NAME_FULLY_QUALIFIED', 'T_UNSET') and is_char(toks[k + 1], '('):
                args = toks[k + 2:match_close(toks, k + 1)]
                fname, prev = text[k].lower().lstrip('\\'), names[k - 1] if k else None
                if prev in ('T_OBJECT_OPERATOR', 'T_NULLSAFE_OBJECT_OPERATOR'):
                    calls.append(('->' + fname, text[k - 2] if names[k - 2] == 'T_VARIABLE' else None, args, k - 2))
                elif prev == 'T_NEW':
                    calls.append(('new ' + fname, None, args, k - 1))
                elif prev not in ('T_FUNCTION', 'T_DOUBLE_COLON'):
                    calls.append((fname, None, args, k))
        call_names = {c[0] for c in calls}

        def direct(s):
            return target is not None and all(is_char(x, '@') for x in toks[rhs_start:s])

        def var_obj(args):
            var = next((t[1] for t in args if t[0] == 'T_VARIABLE'), None)
            return var, self.obj_of(var)

        # 1) uses, releases and wipes of tracked objects; fetch creates a row object
        handled, new_obj, count_of = set(), None, None
        counted = {self.scope['counts'][t[1]] for t in toks if cond and t[1] in self.scope['counts']}
        for cname, recv, args, s in calls:
            var, obj = (recv, self.obj_of(recv)) if cname.startswith('->') else var_obj(args)
            if obj is not None and cname in ('mysql_num_rows', '->rowcount'):
                counted |= {obj.id} if cond else set()
                count_of = obj.id if direct(s) else None
            if obj is None and cname == 'mysql_close':
                obj = next((o for o in self.objs.values() if o.var == '<default-link>'), None)
            if obj is None or cname == 'unset':
                if cname == 'unset':
                    for j, tok in enumerate(args):
                        if tok[0] == 'T_VARIABLE' and (o := self.obj_of(tok[1])):
                            self.unbind(tok[1], line, stmt, 'release' if len(o.refs) == 1 else 'drop')
                            handled.add(tok[1])
                        elif tok[1] in SECRET_SOURCES and j + 2 < len(args) and is_char(args[j + 1], '['):
                            for o in self.objs.values():
                                if getattr(o, 'input', None) == f'{tok[1]}[{args[j + 2][1]}]':
                                    o.input = None
                                    self.emit(o, 'share', line, stmt, o.var, note='refcount giảm còn 1')
                continue
            if cname in USE_CALLS or (cname.startswith('->') and cname[2:] in STMT_METHODS):
                self.emit(obj, 'use', line, stmt, var)
                handled.add(var)
                if direct(s) and new_obj is None and (cname in FETCH_CALLS or cname[2:] in ('fetch', 'fetchobject', 'fetchcolumn')):
                    new_obj = self.new('row', target, line)
                    new_obj.source = obj.id
                    self.emit(new_obj, 'fetch_checked' if cond else 'fetch', line, stmt, target,
                              note='điều kiện if/vòng lặp kiểm tra' if cond else 'chưa kiểm tra FALSE')
                elif direct(s) and new_obj is None and cname == '->fetchall':
                    new_obj = self.new('rows', target, line, sql=obj.sql, bound=obj.bound)
                    self.emit(new_obj, 'alloc_checked', line, stmt, target)
                    if obj.bound and not obj.bound['bounded']:
                        self.flag('E_UNBOUNDED_ALLOC', line, target, stmt, new_obj, {'sql_bound': obj.bound})
            elif cname in ('mysql_free_result', 'mysql_close'):
                self.emit(obj, 'release', line, stmt, var)
                handled.add(var)
            elif cname == 'sodium_memzero':
                # php-src ext/sodium: zeroes only when refcount == 1, then always convert_to_null()
                if len(obj.refs) == 1 and not getattr(obj, 'input', None):
                    self.emit(obj, 'wipe', line, stmt, var)
                elif len(obj.refs) == 1:
                    self.emit(obj, 'drop', line, stmt, var,
                              note=f'refcount 2 (chuỗi còn trong {obj.input}): sodium_memzero chỉ gán null')
                self.unbind(var, line, stmt)
                handled.add(var)
            elif cname in CHECK_CALLS:
                self.emit(obj, 'check', line, stmt, var)

        # 2) allocation of a result buffer, statement or link (one per statement)
        for cname, recv, args, s in calls:
            method = cname.startswith('->')
            if cname == 'mysql_query' or (method and cname[2:] in ('prepare', 'query')):
                sql = self.resolve_sql(args)
                bound = sql_bound(sql, self.tables) if sql is not None else None
                if bound and not bound['select']:
                    continue
                checked = or_die or (method and self.scope['pdo_exc'])
                var = target if direct(s) else '<tạm>'
                obj = self.new('stmt' if method else 'result', var, line, sql=sql, bound=bound)
                self.emit(obj, 'alloc_checked' if checked else 'alloc', line, stmt, var,
                          note='or die / ERRMODE_EXCEPTION' if checked else 'không kiểm tra FALSE')
                if bound and not bound['bounded']:
                    self.flag('E_UNBOUNDED_ALLOC', line, var, stmt, obj, {'sql_bound': bound})
                if self.loop_depth:
                    self.flag('E_ALLOC_IN_LOOP', line, var, stmt, obj)
                if direct(s):
                    new_obj = obj
                else:
                    if call_names & USE_CALLS:
                        self.emit(obj, 'use', line, stmt, var)
                    self.emit(obj, 'drop', line, stmt, var, note='giá trị tạm, refcount về 0')
                break
            if cname in ('mysql_connect', 'mysql_pconnect', 'new pdo'):
                var = target if direct(s) else '<default-link>'
                obj = self.new('link', var, line)
                self.emit(obj, 'alloc_checked' if or_die or cname == 'new pdo' else 'alloc', line, stmt, var)
                if direct(s):
                    new_obj = obj
                break

        # 3) remaining mentions: checks in conditions, index reads, returns, secret uses
        for row in [o for o in self.objs.values() if getattr(o, 'source', None) in counted]:
            if row.state == 'ROW_PENDING':
                self.emit(row, 'check', line, stmt, row.var, note='số dòng > 0 nên fetch có dòng')
        for k, tok in enumerate(toks):
            if tok[0] != 'T_VARIABLE' or tok[1] in handled or (k == start and target):
                continue
            obj = self.obj_of(tok[1])
            if obj is None:
                continue
            if k + 1 < n and is_char(toks[k + 1], '[') and k >= rhs_start:
                self.emit(obj, 'read', line, stmt, tok[1])
            elif cond:
                self.emit(obj, 'check', line, stmt, tok[1])
            elif names[0] == 'T_RETURN' and n == 2:
                self.emit(obj, 'return', line, stmt, tok[1])
            elif obj.kind == 'secret' and k >= rhs_start:
                self.emit(obj, 'use', line, stmt, tok[1])
        for cname, recv, args, s in calls:
            if KEY_LOADER.search(cname) and not direct(s):
                temp = self.new('secret', '<tạm>', line)
                self.emit(temp, 'secret', line, stmt, f'{cname}()', note='khóa trả về làm đối số tạm')
                self.emit(temp, 'drop', line, stmt, f'{cname}()', note='hết lời gọi, refcount về 0')
        if not target:
            return

        # 4) $a = $b shares one zval (refcount + 1)
        single = rhs[0][1] if len(rhs) == 1 and rhs[0][0] == 'T_VARIABLE' and rhs[0][1] != target else None
        if new_obj is None and single and (alias := self.obj_of(single)):
            self.bind(target, alias, line, stmt)
            self.emit(alias, 'share', line, stmt, target, note=f'refcount = {len(alias.refs)}')
            return

        # 5) secrets: from request input, literals or key-loading calls, and plain copies of a secret
        if new_obj is None:
            literal = any(t[0] == 'T_CONSTANT_ENCAPSED_STRING' and len(t[1]) > 2 for t in rhs)
            copied = next((t[1] for t in rhs if t[0] == 'T_VARIABLE' and (o := self.obj_of(t[1]))
                           and o.kind == 'secret' and o.state == 'SECRET'), None)
            if (SECRET_NAME.search(target[1:]) and ({t[1] for t in rhs} & SECRET_SOURCES or literal
                                                    or call_names & SECRET_CALLS or any(map(KEY_LOADER.search, call_names)))) \
                    or (copied and not call_names - PROPAGATING_CALLS):
                new_obj = self.new('secret', target, line)
                # $p = $_POST['k'] shares one zend_string with the request array (refcount 2)
                new_obj.input = next((f'{t[1]}[{rhs[j + 2][1]}]' for j, t in enumerate(rhs[:-2])
                                      if t[1] in SECRET_SOURCES and is_char(rhs[j + 1], '[')), None)
                self.emit(new_obj, 'secret', line, stmt, target,
                          note=f'sao chép từ {copied}' if copied else (f'dùng chung chuỗi với {new_obj.input}'
                                                                       if new_obj.input else None))

        # 6) assignment releases the old value after the right-hand side is built
        self.bind(target, new_obj, line, stmt)
        if count_of:
            self.scope['counts'][target] = count_of
        else:
            self.scope['counts'].pop(target, None)
        if (new_obj is None or new_obj.kind == 'secret') and any(t[0] in STRING_TOKENS for t in rhs):
            self.scope['strings'][target] = self.string_text(rhs)
        else:
            self.scope['strings'].pop(target, None)

    @staticmethod
    def string_text(toks):
        return ''.join(t[1][1:-1] if t[0] == 'T_CONSTANT_ENCAPSED_STRING' else t[1] for t in toks
                       if t[0] in STRING_TOKENS + ('T_VARIABLE', 'T_LNUMBER', 'T_STRING'))

    def resolve_sql(self, args):
        first, depth = [], 0
        for t in args:
            if depth == 0 and is_char(t, ','):
                break
            depth += delta(t)
            first.append(t)
        if len(first) == 1 and first[0][0] == 'T_VARIABLE':
            return self.scope['strings'].get(first[0][1])
        return self.string_text(first) if any(t[0] in STRING_TOKENS for t in first) else None


def analyze_file(entry, tables, php8=False, label=None):
    units = Parser(clean(entry['tokens'])).parse()
    return Walker(label or Path(entry['path']).name, units, tables, php8).run()
