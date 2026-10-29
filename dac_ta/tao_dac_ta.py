#!/usr/bin/env python3
"""Sinh đặc tả JSON theo định dạng SpecVerificationLab.exe (dataset/specs/FORMAT.md) từ evidence của gói nộp,
để nạp ở ô "Đầu vào đặc tả" của chon_test.py hoặc ở nút "Nạp từ file JSON khác..." của exe.
Dùng: python3 dac_ta/tao_dac_ta.py   (ghi các file nhom13_*.json cạnh script này)"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.argv = sys.argv[:1]  # chon_test đọc cổng từ argv
import chon_test as c  # noqa: E402

EV, EV1 = c.PKG / 'evidence', c.PKG / 'bo_sung_v1/evidence_v1'
VIOLATIONS = ['E_USE_FALSE', 'E_ROW_UNCHECKED', 'E_USE_RELEASED', 'E_DOUBLE_RELEASE', 'E_HELD_TO_END', 'E_SECRET_RESIDUE']


def save(name, description, requirements, sm, props):
    spec = {'name': name, 'description': description, 'requirements': requirements, 'state_machine': sm,
            'safety_properties': props}
    (HERE / f'{name}.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding='utf-8')
    print(name, len(sm['states']), 'trạng thái')


def auth_sm(d):
    return {'states': list(d['states']), 'initial': [d['initial_state']], 'labeling': d['labels'],
            'transitions': [[a, b] for a, ts in d['states'].items() for b in ts]}


def memory_sm(walk):
    """Kripke bộ nhớ của một nhánh mã (như tab Kripke của chon_test.py): trạng thái 'TYPESTATE' hoặc 'TYPESTATE__E_...'."""
    nodes, edges, start = c.memory_kripke(walk)
    key = lambda n: n.replace('|', '__')
    labels = {}
    for n, _, _ in nodes:
        state, _, v = n.partition('|')
        labels[key(n)] = [state.lower()] + ([v, 'violation'] if v else [])
    return {'states': list(labels), 'initial': [key(start)], 'labeling': labels,
            'transitions': [[key(a), key(b)] for a, b, _, _ in edges]}


AUTH_REQ = [{'id': 'REQ-1', 'text': 'Mọi thao tác ghi chỉ xảy ra sau khi đã xác thực: AG(!violation), violation gắn ở trạng thái '
             'ghi mà chưa xác thực', 'category': 'safety', 'priority': 'HIGH'},
            {'id': 'REQ-2', 'text': 'Luôn còn đường bị từ chối khi sai thông tin: EF(denied)', 'category': 'liveness', 'priority': 'MEDIUM'},
            {'id': 'REQ-3', 'text': 'Luôn còn đường đăng nhập thành công: EF(authenticated)', 'category': 'liveness', 'priority': 'MEDIUM'}]
for tag, path in (('source_v0', EV / 'auth_model.json'), ('source_v1', EV1 / 'auth_v1.json')):
    save(f'nhom13_xac_thuc_{tag}', f'Luồng đăng nhập, phân quyền, ghi của {tag}, lấy từ {path.name}', AUTH_REQ,
         auth_sm(json.loads(path.read_text(encoding='utf-8'))), ['AG(!violation)', 'EF(denied)', 'EF(authenticated)'])

MEM_REQ = [{'id': 'MEM-1', 'text': 'Không đối tượng bộ nhớ nào rơi vào trạng thái vi phạm: AG(!violation)',
            'category': 'memory', 'priority': 'HIGH'},
           {'id': 'MEM-2', 'text': 'Từng loại vi phạm (dùng FALSE, đọc dòng chưa kiểm, dùng sau giải phóng, giải phóng hai lần, '
            'giữ tới cuối, còn bí mật trong heap) không xảy ra: AG(!E_...)', 'category': 'memory', 'priority': 'HIGH'},
           {'id': 'MEM-3', 'text': 'Luôn còn đường giải phóng tài nguyên: EF(released)', 'category': 'liveness', 'priority': 'MEDIUM'}]
d = json.loads((EV / 'memory_case_results.json').read_text(encoding='utf-8'))
v1 = json.loads((EV1 / 'bo_nho_case_v1.json').read_text(encoding='utf-8'))
assert 'objects' in v1, 'bo_nho_case_v1.json chưa có objects: chạy python bo_sung_v1/check_v1.py bo_nho_case trong gói'
branches = {'source_v0': [o for o in d['objects'] if c.ver(o['group']) == c.SRC],
            '_v0': [o for o in d['objects'] if c.ver(o['group']) == c.V0],
            '_v1': [o for o in d['objects'] if c.ver(o['group']) == c.V1], 'source_v1': v1['objects']}
for tag, objs in branches.items():
    save(f'nhom13_bo_nho_{tag.strip("_")}', f'Kripke typestate bộ nhớ của nhánh {tag} ({len(objs)} đối tượng), '
         'lấy từ memory_case_results.json / bo_nho_case_v1.json', MEM_REQ, memory_sm(c.memory_walk(d, objs)),
         ['AG(!violation)'] + [f'AG(!{v})' for v in VIOLATIONS] + ['EF(released)'])
