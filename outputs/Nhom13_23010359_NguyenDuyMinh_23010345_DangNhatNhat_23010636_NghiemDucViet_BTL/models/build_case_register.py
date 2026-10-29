"""Build the detailed case register from saved static/solver outputs."""
from pathlib import Path
import json
BASE=Path(__file__).resolve().parents[1]
E=BASE/'evidence'

def compact(model):
    return json.dumps(model,ensure_ascii=False,separators=(',',':')) if model else 'Không có model: UNSAT'

def main():
    data=json.loads((E/'report_case_metadata.json').read_text())
    sql=json.loads((E/'sql_inventory.json').read_text())
    expanded=json.loads((E/'sql_case_results.json').read_text())
    core=json.loads((E/'formal_results.json').read_text())
    master=[]
    for c in data['cases']:
        master.append([c[0],c[1],c[2],c[3],c[4],c[5],
                       'HIGH' if c[0] in ('TC-01','TC-02') else 'MEDIUM',c[6],c[7]])
    for i,c in enumerate(data['additional']):
        branch=('_v0','_v1')[i//6]  # TC-17..22 là _v0, TC-23..28 là _v1, cùng thứ tự chức năng
        master.append([c[0],c[1],'Tổng hợp '+['Login','Authz','Query','Script','Token Bool','Token SMT'][i%6]+' '+branch,
                       f'Mã sinh {branch} và mô hình thủ công; xem các case con riêng.',
                       f"Đối chiếu từng case {branch} trong {'SMTChiTiet' if i%6==5 else 'SATChiTiet'}.",
                       'Kết quả khớp các case con; không suy kết quả mô hình thành bảo mật runtime.',
                       'HIGH',c[2],c[3]])
    qmap={q['id']:q for q in sql['queries']}
    for q in sql['queries']:
        loc=f"{q['file']}:{q['start_line']}-{q['end_line']}"
        master.append([q['id'],'REQ-L01' if q['file'] in ('index.php','login.php') else 'REQ-L03',
                       f"{q['operation']} tại {loc}",
                       'Đọc source_v0 và schema; SQL bên dưới chỉ là văn bản.',
                       '1 Đọc SQL và từng phép gán tại vị trí đã lưu.\n2 Truy nguồn GET/POST hoặc kết quả CSDL.\n'
                       '3 Phân loại sink: SQL hằng, dữ liệu HTTP hay kết quả CSDL.\n'
                       f"4 Case con {q['id']}-SAT-* và {q['id']}-P*-SMT-* ghi riêng theo nhánh mã.",
                       'Dữ liệu không đổi cú pháp query; query hằng là đối chứng; phân loại theo nguồn.',
                       'HIGH' if q['classification']=='HTTP_INTERPOLATION' else 'MEDIUM',
                       q['baseline_result'],f"sql_inventory.json#{q['id']}; {loc}"])
    sat=[]
    for n,c in enumerate(core['boolean_cases'],1):
        row={'id':f'SAT-CORE-{n:02}','model_id':c['id'],'query_id':'CORE',
             'source':c['source'],'variables':c['variables'],'clauses':c['clauses'],
             'expected':'UNSAT' if c['id'].endswith('_v1') or c['id']=='dpll_branch_control' else 'SAT',
             'dpll':c['dpll'],'z3_sat':c['z3_sat'],'truth_table':c['truth_table'],
             'witness':c['witness'],'trace':c['dpll_trace'],
             'cnf':f"evidence/formal/{c['id']}.cnf",'smt2':f"evidence/formal/{c['id']}.smt2",
             'purpose':c['purpose']}
        assert row['expected']==row['dpll']==row['z3_sat']==row['truth_table']
        sat.append(row)
    for c in expanded['boolean_cases']:
        row=dict(c)
        row['model_id']=c['id']
        row['purpose']=f"Binding {c['query_id']} "+{'before':'trước sửa','after':'sau sửa','valid':'đối chứng hợp lệ'}[c['version']]
        sat.append(row)
    core_requirements={'authentication':'REQ-G01','authorization':'REQ-G02',
                       'database_query':'REQ-G03','script_output':'REQ-G04',
                       'token_crypto':'REQ-G05','dpll_branch_control':'NFR-A04'}
    for c in sat:
        req='REQ-G03' if c['query_id']!='CORE' else next(
            value for prefix,value in core_requirements.items() if c['model_id'].startswith(prefix))
        master.append([c['id'],req,
                       c['purpose'],c['source'],
                       '1 Đọc mapping biến và clauses.\n2 Chạy DPLL, Z3 SAT và bảng chân trị.\n3 So model/trace với file CNF.',
                       c['expected']+' trong quan hệ đã khai báo; đối chứng không thay thế chứng minh PHP.',
                       'HIGH',f"DPLL={c['dpll']}; Z3={c['z3_sat']}; truth table={c['truth_table']}; "+compact(c['witness']),
                       c['cnf']+'; '+c['smt2']])
    predicates={
        'token_v0_counterexample':'accepted=parsed; key=16, nonce=16, tag=0, tag_ok=false; NOT policy',
        'token_v1_key_length':'accepted AND key_bytes != 32',
        'token_v1_nonce_length':'accepted AND nonce_bytes != 12',
        'token_v1_tag_length':'accepted AND tag_bytes != 16',
        'token_v1_expired':'accepted AND exp <= now',
        'token_v1_excess_ttl':'accepted AND exp-iat > 1800',
        'token_v1_future_iat':'accepted AND iat > now',
        'token_v1_identity_audience':'accepted AND (uid <= 0 OR NOT audience_ok)',
        'token_v1_invalid_tag':'accepted AND NOT tag_ok',
        'token_v1_valid_control':'key=32; nonce=12; tag=16; uid=1; iat=1000; now=1100; exp=2800; guards=true',
    }
    smt=[]
    for n,c in enumerate(core['smt_cases'],1):
        smt.append({'id':f'SMT-CORE-{n:02}','model_id':c['id'],'query_id':'CORE','field_id':'TOKEN',
                    'parameter':'token/claims','kind':'Int/Bool','purpose':c['id'],'input':predicates[c['id']],
                    'policy':('accepted <-> parsed' if c['id']=='token_v0_counterexample' else
                              'accepted <-> parsed AND key=32 AND nonce=12 AND tag=16 AND tag_ok AND audience_ok AND uid>0 AND 0<=iat<=now<exp AND exp-iat<=1800'),
                    'predicate':predicates[c['id']],'expected':c['expected'],'status':c['status'],
                    'witness':c['witness'],'smt2':f"evidence/formal/{c['id']}.smt2",'source':c['source']})
    for c in expanded['smt_cases']:
        row=dict(c)
        row['model_id']=c['id']
        smt.append(row)
    for c in smt:
        master.append([c['id'],'REQ-G06' if c['query_id']=='CORE' else 'REQ-G03',
                       c['purpose']+' — '+c['field_id'],c['source'],
                       '1 Đọc guard/biến miền và công thức.\n2 Thêm điều kiện '+c['input']+
                       '.\n3 Chạy Z3 và lưu SMT-LIB; nếu SAT đọc model.',
                       c['expected']+' trong mô hình; UNSAT không chứng minh primitive/runtime.',
                       'MEDIUM',c['status']+'; '+compact(c['witness']),c['smt2']])
    assert len(master)==822 and len(sat)==178 and len(smt)==562
    assert len({c[0] for c in master})==822
    # mỗi hồ sơ thuộc đúng một nhánh mã: không dòng nào nhắc cả _v0 lẫn _v1
    mixed=[c[0] for c in master if all(b in ' '.join(c).replace('source_v0','') for b in ('_v0','_v1'))]
    assert not mixed,mixed
    result={'summary':{'overview_cases':28,'sql_source_cases':54,'sat_cases':178,
                       'smt_cases':562,'total_cases':822,'sql_field_occurrences':92},
            'master_rows':master,'sat_rows':sat,'smt_rows':smt}
    (E/'case_register.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result['summary'],ensure_ascii=False,indent=2))

if __name__=='__main__':main()
