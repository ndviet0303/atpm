"""Per-query SQL static cases. Never runs target PHP functions, DB or HTTP."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from itertools import product
import hashlib, importlib.util, json, os, re, shutil, subprocess, sys
BASE=Path(__file__).resolve().parents[1]
REPO=BASE.parents[1]
E=BASE/'evidence'
SOURCE=BASE/'source_v0/librarian'
OUT=E/'sql_formal'
OUT.mkdir(exist_ok=True)
deps=Path(os.environ.get('Z3_DEPS','/private/tmp/atpm-report-20261004/solver_deps'))
if deps.exists():sys.path.insert(0,str(deps))
import z3
spec=importlib.util.spec_from_file_location('core_models',BASE/'models/run_models.py')
core=importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
VAR=re.compile(r'\$[A-Za-z_]\w*(?:\[\$[A-Za-z_]\w*\])?')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def schema_columns():
    text=(BASE/'source_v0/db/eb_lms.sql').read_text()
    columns={}
    for table,body in re.findall(r'CREATE TABLE IF NOT EXISTS \x60(\w+)\x60 \((.*?)\) ENGINE=',text,re.S):
        for name,kind,width in re.findall(r'^\s*\x60([^\x60]+)\x60\s+(varchar|int|bigint)\((\d+)\)',body,re.M|re.I):
            columns[(table,name)]={'kind':kind.lower(),'width':int(width)}
    return columns

def column_for(q,expression,rhs):
    name=expression[1:].split('[')[0]
    sql=q['sql'].lower()
    if name in ('title','book_title'):return 'book','book_title'
    if name in ('cat_id','category_id'):
        return ('category' if re.search(r'\bfrom\s+category\b',sql) else 'book'),'category_id'
    if name in ('get_id','id','user_id','book_id','borrow_id','member_id'):
        if expression=='$id[$i]':return 'book','book_id'
        if name in ('book_id','borrow_id','member_id','user_id'):
            return {'book_id':'book','borrow_id':'borrow','member_id':'member','user_id':'users'}[name],name
        row=re.search(r"\$row\['([^']+)'\]",rhs)
        if row:return {'book_id':'book','member_id':'member','borrow_id':'borrow'}[row[1]],row[1]
        if q['file']=='return_save.php':return 'borrow','borrow_id'
        if re.search(r'\b(?:from|update|into)\s+book\b',sql):return 'book','book_id'
        if re.search(r'\b(?:from|update|into)\s+users\b',sql):return 'users','user_id'
        return 'member','member_id'
    if name=='due_date':return 'borrow','due_date'
    if q['file'] in ('index.php','login.php','modal_add_user.php','modal_edit_user.php'):return 'users',name
    if q['file'] in ('books_save.php','update_books.php','advance_search.php'):return 'book',name
    return 'member',name

def inventory():
    run=subprocess.run(['php',str(E/'extract_sql_calls.php'),str(SOURCE)],capture_output=True,text=True,check=True)
    raw=json.loads(run.stdout)
    old=json.loads((E/'php_tokens.json').read_text())
    positions={(r['file'],c['line']) for r in old for c in r['calls'] if c['name']=='mysql_query'}
    assert {(r['file'],r['start_line']) for r in raw}==positions and len(raw)==54
    columns=schema_columns()
    queries=[]
    for number,entry in enumerate(raw,1):
        resolved=entry['resolved_expression']
        assert resolved[0]==resolved[-1]=='"',resolved
        sql=resolved[1:-1]
        q={k:entry[k] for k in ['file','start_line','end_line','argument','sql_assignment','source_sha256']}
        q.update(id=f'SQL-{number:02}',sql=sql,operation=sql.split()[0].upper())
        fields=[]
        for expression in dict.fromkeys(VAR.findall(sql)):
            origin=entry['preceding_assignments'][expression.split('[')[0]]
            rhs=origin['expression']
            http=re.fullmatch(r"\$_(GET|POST)\['([^']+)'\]",rhs)
            row=re.fullmatch(r"\$row\['([^']+)'\]",rhs)
            assert http or row,(entry['file'],expression,rhs)
            table,column=column_for(q,expression,rhs)
            definition=columns[(table,column)]
            integer=definition['kind'] in ('int','bigint')
            kind=http[1] if http else ('DB_AFTER_UNSAFE_SELECT' if q['file'] in ('advance_search.php','edit_book.php') else 'DB_INTEGER')
            fields.append({
                'id':f'{q["id"]}-P{len(fields)+1:02}','expression':expression,
                'parameter':'selector_item' if '[' in expression else expression[1:],
                'origin_line':origin['line'],'origin_expression':rhs,'origin_kind':kind,
                'request_key':http[2] if http else None,'schema_column':f'{table}.{column}',
                'schema_kind':definition['kind'],'schema_width':definition['width'],
                'guard_kind':'int' if integer else 'text',
                'minimum':0 if not integer or column in ('book_copies','copyright_year') else 1,
                'maximum':2147483647 if integer else definition['width'],
                'limit_basis':'INT32 target/reference range; int(n) is display width, not bits' if integer else f'VARCHAR({definition["width"]}) character capacity'})
        direct=any(f['origin_kind'] in ('GET','POST') for f in fields)
        derived=any(f['origin_kind']=='DB_AFTER_UNSAFE_SELECT' for f in fields)
        q['fields']=fields
        q['classification']='HTTP_INTERPOLATION' if direct else 'DB_AFTER_UNSAFE_SELECT' if derived else 'DB_INTEGER_INTERPOLATION' if fields else 'CONSTANT_QUERY'
        q['baseline_result']=(
            'Không đạt SQLi: GET/POST nội suy trực tiếp; đối chiếu được đường nguồn tới query.' if direct else
            'Nguy cơ nối tiếp: SELECT trước chưa bind; không mặc định tin cột INT khi result-set có thể bị thay thế.' if derived else
            'Chưa xác nhận SQLi: biến từ cột INT của query hằng; thiếu bind vi phạm hardening, chưa tự chứng minh SQLi.' if fields else
            'Đạt đối chứng SQLi ở sink này: SQL hằng. Các lỗi API/error/schema xét riêng.')
        q['residual']=[]
        if q['file'] in ('index.php','login.php','modal_add_user.php','modal_edit_user.php'):
            q['residual'].append('Chỉ sửa binding; password bản rõ vẫn cần sửa theo FIND-05/core authentication.')
        if q['file']=='borrow_save.php':q['residual'].append('Chưa sửa ID toàn cục/MyISAM; cần ID theo kết nối và transaction sau đổi engine.')
        if q['file']=='unstudents.php':q['residual'].append('Bảng students thiếu trong schema; query hằng chưa đáp ứng tính đầy đủ tham chiếu.')
        if q['file']=='advance_search.php' and direct:q['residual'].append('Bản sinh chọn literal substring, escape !/%/_; policy wildcard chưa có SRS.')
        q['residual'].append('Wrapper SQL không tự triển khai session/authz/CSRF, ownership hoặc toàn bộ nghiệp vụ.')
        queries.append(q)
    return {'source_scope':'All 54 mysql_query calls in 66 direct librarian PHP files',
            'schema_sha256':sha(BASE/'source_v0/db/eb_lms.sql'),'queries':queries,
            'summary':{'queries':54,'files':len({q['file'] for q in queries}),
                       'dynamic_queries':sum(bool(q['fields']) for q in queries),
                       'constant_queries':sum(not q['fields'] for q in queries),
                       'field_occurrences':sum(len(q['fields']) for q in queries),
                       'classification_counts':dict(Counter(q['classification'] for q in queries)),
                       'origin_counts':dict(Counter(f['origin_kind'] for q in queries for f in q['fields']))},
            'limits':['Extraction/mappings apply to these 54 calls; not a general taint engine or SQL parser.',
                      'DB column types trusted only for results from declared non-injected query.',
                      'Query positions, fields, formal cases and vulnerability groups are different counts.']}

HELPERS="""<?php
// Educational guards; no DB connection is created.
function sql_case_int(mixed $raw, int $minimum, int $maximum): int
{
    if (!is_int($raw) && !is_string($raw)) {
        throw new InvalidArgumentException('Integer scalar required');
    }
    $value = filter_var($raw, FILTER_VALIDATE_INT,
        ['options' => ['min_range' => $minimum, 'max_range' => $maximum]]);
    if ($value === false) {
        throw new InvalidArgumentException('Invalid integer range or format');
    }
    return $value;
}
function sql_case_text(mixed $raw, int $maximum): string
{
    if (!is_string($raw) || strpos($raw, "\\0") !== false) {
        throw new InvalidArgumentException('Text scalar required without NUL');
    }
    $length = preg_match_all('/./us', $raw);
    if ($length === false || $length > $maximum) {
        throw new InvalidArgumentException('Invalid UTF-8 or character capacity');
    }
    return $raw;
}
function sql_case_present(array $input, string $key): mixed
{
    if (!array_key_exists($key, $input)) {
        throw new InvalidArgumentException('Missing parameter');
    }
    return $input[$key];
}
"""

def generate(queries):
    root=BASE/'generated_cases/sql'
    for v in ('_v0','_v1'):(root/v).mkdir(parents=True,exist_ok=True)
    (root/'guards.php').write_text(HELPERS)
    for q in queries:
        name=q['id'].lower().replace('-','_')
        raw_sql=q['sql'].replace('$id[$i]','$selector_item')
        before=['<?php',f'// {q["id"]}: {q["file"]}:{q["start_line"]}-{q["end_line"]}.',
                '// Query-only text example; never executed.',f'function {name}_v0(array $input): mixed','{']
        before += [f"    {'$'}{f['parameter']} = $input['{f['parameter']}'];" for f in q['fields']]
        before += [f'    return mysql_query("{raw_sql}");','}']
        statement=q['sql']
        for f in q['fields']:
            expr=re.escape(f['expression'])
            if f['parameter'] in ('title','author') and q['file']=='advance_search.php':
                statement=re.sub(r"'\%"+expr+r"\%'",':'+f['parameter']+" ESCAPE '!'",statement)
            else:statement=re.sub("'"+expr+"'",':'+f['parameter'],statement)
        assert not VAR.search(statement),(q['id'],statement)
        statement=' '.join(statement.split())
        after=['<?php',f'// {q["id"]}: binding/guards only; caller must authorize.',
               "require_once __DIR__ . '/../guards.php';",f'function {name}_v1(PDO $db, array $input): PDOStatement','{']
        for f in q['fields']:
            arg=f"sql_case_present($input, '{f['parameter']}')"
            guard=f"sql_case_int({arg}, {f['minimum']}, {f['maximum']})" if f['guard_kind']=='int' else f"sql_case_text({arg}, {f['maximum']})"
            after.append(f"    {'$'}{f['parameter']} = {guard};")
            if f['parameter'] in ('title','author') and q['file']=='advance_search.php':
                after.append(f"    {'$'}{f['parameter']} = '%' . strtr({'$'}{f['parameter']}, ['!' => '!!', '%' => '!%', '_' => '!_']) . '%';")
        after+=['    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);',
                '    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);',
                f'    $statement = $db->prepare("{statement}");','    if ($statement === false) {',
                "        throw new RuntimeException('Preparation failed');",'    }']
        for f in q['fields']:
            kind='PDO::PARAM_INT' if f['guard_kind']=='int' else 'PDO::PARAM_STR'
            after.append(f"    $statement->bindValue(':{f['parameter']}', {'$'}{f['parameter']}, {kind});")
        after+=['    $statement->execute();','    return $statement;','}']
        for version,lines in [('_v0',before),('_v1',after)]:
            p=root/version/(name+'.php')
            p.write_text('\n'.join(lines)+'\n')
            q['generated'+version]=str(p.relative_to(BASE))
            q['generated'+version+'_sha256']=sha(p)
        q['prepared_sql']=statement
        code=(BASE/q['generated_v1']).read_text()
        placeholders=re.findall(r'(?<!:):([A-Za-z_]\w*)',statement)
        bindings=re.findall(r"bindValue\(':([^']+)'",code)
        assert Counter(placeholders)==Counter(bindings)==Counter(f['parameter'] for f in q['fields'])
        for f in q['fields']:
            assert f"sql_case_present($input, '{f['parameter']}')" in code
            assert (f", {f['minimum']}, {f['maximum']});" if f['guard_kind']=='int' else f", {f['maximum']});") in code
    return root

def solve_cnf(q,version):
    names={1:'executed',2:'all_bound'}
    names.update({3+i:'bound_'+f['parameter'] for i,f in enumerate(q['fields'])})
    inputs=list(range(3,len(names)+1))
    clauses=core.gate_cnf(2,inputs)+[[1]]+[[v if version!='before' else -v] for v in inputs]
    clauses += [[2] if version=='valid' else [-2]]
    expected='SAT' if version=='valid' or version=='before' and inputs else 'UNSAT'
    trace=[]
    assignment=core.dpll(clauses,trace=trace)
    status='SAT' if assignment is not None else 'UNSAT'
    symbols={v:z3.Bool(n) for v,n in names.items()}
    solver=z3.Solver()
    solver.add(*[z3.Or(*[symbols[abs(v)] if v>0 else z3.Not(symbols[abs(v)]) for v in c]) for c in clauses])
    other=str(solver.check()).upper()
    exhaustive=next((dict(zip(names,values)) for values in product((False,True),repeat=len(names))
                     if core.satisfies(clauses,dict(zip(names,values)))),None)
    truth='SAT' if exhaustive is not None else 'UNSAT'
    assert status==other==truth==expected
    case_id=q['id']+'-SAT-'+{'before':'B','after':'A','valid':'C'}[version]
    stem=case_id.lower()
    (OUT/(stem+'.cnf')).write_text(''.join(f'c {v} {n}\n' for v,n in names.items())+
        f'p cnf {len(names)} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
    (OUT/(stem+'.smt2')).write_text(solver.to_smt2())
    return {'id':case_id,'query_id':q['id'],'version':version,'variables':names,
            'relation':'all_bound <-> AND(each dynamic parameter bound); executed=true',
            'predicate':'executed AND all_bound' if version=='valid' else 'executed AND NOT all_bound',
            'clauses':clauses,'expected':expected,'dpll':status,'z3_sat':other,'truth_table':truth,'trace':trace,
            'witness':{names[v]:assignment.get(v,False) for v in names} if assignment is not None else None,
            'source':q['generated_v0'] if version=='before' else q['generated_v1'],
            'cnf':str((OUT/(stem+'.cnf')).relative_to(BASE)),'smt2':str((OUT/(stem+'.smt2')).relative_to(BASE)),
            'interpretation':'Binding-policy model; SAT is not a SQL exploit. Empty AND true for constant SQL.'}

def solve_fields(q,f):
    prefix=f['id'].lower().replace('-','_')
    accepted,present,type_ok,format_ok=z3.Bools(prefix+'_accepted '+prefix+'_present '+prefix+'_type_ok '+prefix+'_format_ok')
    value=z3.Int(prefix+'_value') if f['guard_kind']=='int' else z3.String(prefix+'_text')
    size=value if f['guard_kind']=='int' else z3.Length(value)
    policy=z3.And(present,type_ok,format_ok,size>=f['minimum'],size<=f['maximum'])
    valid=value==(z3.IntVal(f['maximum']) if f['guard_kind']=='int' else z3.StringVal('A'*f['maximum']))
    tests=[
        ('MISSING',z3.Not(present),'UNSAT','Thiếu khóa đầu vào','present=false'),
        ('TYPE',z3.Not(type_ok),'UNSAT','Kiểu array/bool không hợp lệ','type_ok=false'),
        ('FORMAT',z3.Not(format_ok),'UNSAT','Số không parse hoặc UTF-8/NUL lỗi','format_ok=false'),
        ('MAX',size==f['maximum']+1,'UNSAT','Vượt cận trên một đơn vị',f'value/Length={f["maximum"]+1}'),
        ('MIN',value==f['minimum']-1 if f['guard_kind']=='int' else value==z3.StringVal(''),
         'UNSAT' if f['guard_kind']=='int' else 'SAT',
         'Dưới cận dưới một đơn vị' if f['guard_kind']=='int' else 'Chuỗi rỗng hợp lệ theo schema, không tự gán nonempty',
         f'value={f["minimum"]-1}' if f['guard_kind']=='int' else 'Length=0; guards=true'),
        ('VALID',valid,'SAT','Đối chứng đúng cận trên',f'value/Length={f["maximum"]}; guards=true')]
    rows=[]
    for suffix,predicate,expected,purpose,input_text in tests:
        solver=z3.Solver()
        solver.add(accepted==policy,accepted,predicate)
        if suffix in ('VALID','MIN') and expected=='SAT':solver.add(present,type_ok,format_ok)
        status=str(solver.check()).upper()
        assert status==expected,(q['id'],f['id'],suffix,status)
        model=solver.model() if status=='SAT' else None
        witness={str(v):str(model.eval(v,model_completion=True)) for v in [accepted,present,type_ok,format_ok,size]} if model is not None else None
        name=f['id']+'-SMT-'+suffix
        path=OUT/(name.lower()+'.smt2')
        path.write_text(solver.to_smt2())
        rows.append({'id':name,'query_id':q['id'],'field_id':f['id'],'parameter':f['parameter'],'kind':f['guard_kind'],
                     'input':input_text,'purpose':purpose,
                     'policy':f'accepted <-> present AND type_ok AND format_ok AND {f["minimum"]} <= '+
                              ('value' if f['guard_kind']=='int' else 'Length(text)')+f' <= {f["maximum"]}',
                     'predicate':str(predicate),'expected':expected,'status':status,'witness':witness,
                     'smt2':str(path.relative_to(BASE)),'source':q['generated_v1'],
                     'assumptions':'Manual guard model; primitive parse/character counting assumed; no PHP execution.'})
    return rows

def static_generated(root):
    files=sorted(root.rglob('*.php'))
    assert len(files)==109
    lint=[]
    for p in files:
        r=subprocess.run(['php','-l',str(p)],capture_output=True,text=True)
        assert r.returncode==0,(p,r.stderr)
        lint.append({'file':str(p.relative_to(BASE)),'exit_code':0,'stdout':r.stdout.strip()})
    scanner=os.environ.get('SEMGREP_BIN') or (str(REPO/'study/.venv/bin/semgrep') if (REPO/'study/.venv/bin/semgrep').exists() else shutil.which('semgrep'))
    assert scanner,'Set SEMGREP_BIN'
    env=os.environ.copy()
    certs=list((REPO/'study/.venv/lib').glob('python*/site-packages/certifi/cacert.pem'))
    if certs and not env.get('SSL_CERT_FILE'):env['SSL_CERT_FILE']=str(certs[0])
    env.update(SEMGREP_SEND_METRICS='off',SEMGREP_ENABLE_VERSION_CHECK='0',
               SEMGREP_SETTINGS_FILE=str(E/'sql_semgrep_settings.yml'),SEMGREP_LOG_FILE=str(E/'sql_semgrep.log'))
    scans=[]
    for version in ('_v0','_v1'):
        command=[scanner,'scan','--metrics','off','--jobs','1','--no-git-ignore','--config',
                 str(E/'generated_case_rules.yaml'),'--json','--output',str(E/('sql_generated'+version+'.json'))]
        command += [str(p) for p in sorted((root/version).glob('*.php'))]
        output=E/('sql_generated'+version+'.json')
        output.unlink(missing_ok=True)
        r=subprocess.run(command,env=env,capture_output=True,text=True)
        (E/('sql_generated'+version+'.stdout')).write_text(r.stdout)
        (E/('sql_generated'+version+'.stderr')).write_text(r.stderr)
        if r.returncode!=0:
            raise RuntimeError(f'Semgrep {version} exited {r.returncode}: '+r.stderr[-1200:])
        raw=json.loads(output.read_text())
        assert not raw.get('errors'),raw.get('errors')
        assert len(raw['results'])==(54 if version=='_v0' else 0)
        scans.append({'version':version,'exit_code':r.returncode,'findings':len(raw['results']),
                      'scanned':len(raw['paths']['scanned']),'errors':raw.get('errors',[]),
                      'command':command,'semgrep_version':raw['version']})
    result={'lint':lint,'scans':scans,'rules_sha256':sha(E/'generated_case_rules.yaml'),
            'limits':'54 v0 raw API matches include constant queries; not 54 SQLi findings.'}
    (E/'sql_static_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    return result

def main():
    inv=inventory()
    root=generate(inv['queries'])
    (E/'sql_inventory.json').write_text(json.dumps(inv,ensure_ascii=False,indent=2))
    boolean=[solve_cnf(q,v) for q in inv['queries'] for v in ('before','after','valid')]
    smt=[r for q in inv['queries'] for f in q['fields'] for r in solve_fields(q,f)]
    static=static_generated(root)
    result={'timestamp':datetime.now(timezone.utc).isoformat(),'z3_version':z3.get_full_version(),
            'model_kind':'Manual per-query binding policy and per-field guards',
            'boolean_cases':boolean,'smt_cases':smt,
            'summary':{'queries':54,'fields':92,'query_cnf_cases':len(boolean),'query_cnf_crosschecks_passed':len(boolean),
                       'field_smt_cases':len(smt),'field_smt_expected_passed':len(smt),
                       'generated_query_pairs':54,'generated_sql_lint':len(static['lint']),
                       'generated_v0_rule_hits':54,'generated_v1_rule_hits':0},
            'assumptions':['PDO native binding isolates values; no DB connection created.',
                           'PHP guard primitives match declared Bool/Int/String contracts.',
                           'VARCHAR capacity comes from schema; Unicode storage needs charset review.',
                           'Binding does not prove authz/CSRF/password storage/ownership/atomicity/runtime outcomes.']}
    assert len(smt)==552
    (E/'sql_case_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps({'inventory':inv['summary'],'models':result['summary']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
