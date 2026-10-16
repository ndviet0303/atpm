from pathlib import Path
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo

out = Path(__file__).resolve().parent
base = out.parent
root = base.parents[1]
source_root = root / 'study/source' if (root/'study/source/librarian').exists() else base/'source_v0'
source = source_root / 'librarian'
out.mkdir(parents=True, exist_ok=True)

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
inventory = []
lint = []
for p in sorted(source.glob('*.php')):
    text = p.read_text(errors='replace')
    lines = text.splitlines()
    inventory.append({'file': p.name, 'bytes': p.stat().st_size, 'lines': len(lines), 'blank': sum(not x.strip() for x in lines), 'sha256': digest(p)})
    r = subprocess.run(['php', '-l', str(p)], capture_output=True, text=True)
    lint.append({'file': p.name, 'exit_code': r.returncode, 'stdout': r.stdout.strip(), 'stderr': r.stderr.strip()})
(out / 'source_inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2))
(out / 'php_lint.json').write_text(json.dumps(lint, ensure_ascii=False, indent=2))
r = subprocess.run(['php', str(out/'static_inventory.php'), str(source)], capture_output=True, text=True)
assert r.returncode == 0, r.stderr
tokens = json.loads(r.stdout)
(out / 'php_tokens.json').write_text(json.dumps(tokens, ensure_ascii=False, indent=2))
checklist_path = root/'study/checklist.md'
ids = re.findall(r'^\| \*\*([A-Z]+-\d+)\*\*', checklist_path.read_text(), re.M) if checklist_path.exists() else json.loads((out/'static_summary.json').read_text())['checklist_ids']
sql = (source_root/'db/eb_lms.sql').read_text()
tables = re.findall(r'CREATE TABLE IF NOT EXISTS `([^`]+)`', sql)
engines = dict(re.findall(r'CREATE TABLE IF NOT EXISTS `([^`]+)`[\s\S]*?\) ENGINE=(\w+)', sql))
actions = ['delete_user.php','delete_books.php','delete_member.php','delete_student.php','books_save.php','member_save.php','student_save.php','borrow_save.php','return_save.php','update_books.php','update_member.php','update_students.php']
action_review=[]
for name in actions:
    row = next(t for t in tokens if t['file']==name)
    action_review.append({'file':name, 'session_include':any(i['path']=='session.php' for i in row['includes']), 'session_tokens':any(i['variable']=='$_SESSION' for i in row['request_tokens']), 'session_start':any(i['name']=='session_start' for i in row['calls'])})
missing = [dict(file=t['file'], **i) for t in tokens for i in t['includes'] if not i['exists']]
calls = Counter(c['name'] for t in tokens for c in t['calls'])
summary = {'timestamp':datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat(), 'source_directory':str(source), 'php_file_count':len(inventory), 'physical_lines':sum(i['lines'] for i in inventory), 'blank_lines':sum(i['blank'] for i in inventory), 'empty_files':[i['file'] for i in inventory if i['bytes']==0], 'checklist_ids':ids, 'checklist_count':len(ids), 'schema_tables':tables, 'schema_engines':engines, 'schema_sha256':digest(source_root/'db/eb_lms.sql'), 'license_sha256':digest(source_root/'LICENSE'), 'lint_ok':sum(l['exit_code']==0 for l in lint), 'missing_includes':missing, 'action_review':action_review, 'function_calls':dict(calls)}
(out/'static_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
historical_path = root/'study/results/semgrep_raw.json'
if historical_path.exists():
    raw = json.loads(historical_path.read_text())
    (out/'historical_semgrep_audit.json').write_text(json.dumps({'version':raw['version'], 'results_count':len(raw['results']), 'errors':raw.get('errors'), 'paths_scanned':len(raw.get('paths',{}).get('scanned',[])), 'warning_counts':dict(Counter(r['check_id'] for r in raw['results']))},ensure_ascii=False,indent=2))
print(json.dumps({k:summary[k] for k in ['php_file_count','physical_lines','blank_lines','empty_files','checklist_count','lint_ok','schema_engines','missing_includes','function_calls']},ensure_ascii=False,indent=2))
