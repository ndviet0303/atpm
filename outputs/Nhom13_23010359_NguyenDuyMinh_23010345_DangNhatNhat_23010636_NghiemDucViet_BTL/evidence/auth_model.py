"""Check a manually derived finite abstraction of PHP authorization paths.

This script checks a model only. It never loads or executes PHP application code.
Terminal states self-loop so CTL path semantics remain total.
"""
from pathlib import Path
from collections import deque
import json

edges = {
    'unauthenticated': ['denied', 'authenticated', 'unauthorized_write'],
    'denied': ['denied'],
    'authenticated': ['authorized_write'],
    'authorized_write': ['authorized_write'],
    'unauthorized_write': ['unauthorized_write'],
}
labels = {
    'unauthenticated': [],
    'denied': ['denied'],
    'authenticated': ['authenticated'],
    'authorized_write': ['authenticated','write'],
    'unauthorized_write': ['write','violation'],
}
initial = 'unauthenticated'
queue = deque([(initial,[initial])])
visited = set()
witness = None
while queue:
    state, path = queue.popleft()
    if state in visited: continue
    visited.add(state)
    if 'write' in labels[state] and 'authenticated' not in labels[state] and witness is None:
        witness = path
    for target in edges[state]: queue.append((target,path+[target]))
record = {
    'scope':'Manually derived authorization abstraction; no application execution',
    'initial_state':initial,
    'states':edges,
    'labels':labels,
    'reachable':sorted(visited),
    'results':[
        {'formula':'AG(write -> authenticated)','initial_satisfies':witness is None,'counterexample':witness},
        {'formula':'EF(denied)','initial_satisfies':any('denied' in labels[s] for s in visited)},
        {'formula':'EF(authenticated)','initial_satisfies':any('authenticated' in labels[s] for s in visited)},
    ],
    'deadlocks_in_abstraction':[s for s in visited if not edges[s]],
    'source_refs':['session.php:5-7','delete_user.php:2-6','login.php:10-12'],
    'limits':'Assumes direct endpoint reachability and successful database statements; excludes server rules, SQL failures, actual concurrency and deployment policy.'
}
Path(__file__).with_name('auth_model.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
print(json.dumps(record,ensure_ascii=False,indent=2))
