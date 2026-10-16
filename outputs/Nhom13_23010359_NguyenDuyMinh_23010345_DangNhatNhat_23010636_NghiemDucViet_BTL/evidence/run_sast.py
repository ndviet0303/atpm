from pathlib import Path
import json
import os
import hashlib
import subprocess
import time
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo

out = Path(__file__).resolve().parent
base = out.parent
root = base.parents[1]
source_root = root/'study/source' if (root/'study/source/librarian').exists() else base/'source_v0'
source = source_root/'librarian'
import shutil
scanner = os.environ.get('SEMGREP_BIN') or (str(root/'study/.venv/bin/semgrep') if (root/'study/.venv/bin/semgrep').exists() else shutil.which('semgrep'))
assert scanner, 'Install Semgrep 1.176.1 or set SEMGREP_BIN'
rules = json.loads((out/'frozen_registry_php_rules.json').read_text())['rules']
packs = [{'package':'php','new_php_rules':24}, {'package':'sql-injection','new_php_rules':0}, {'package':'xss','new_php_rules':0}]
expected_rules = {'frozen_registry_php_rules.json':'a1b9b9e96f3377860e7f9e37a729ef140f0e51aa0ac43ab5f80742aa6146335d', 'custom_php_rules_corrected.yaml':'8e07a286e0bea1ff8e7960e29e06d52deea8b0379747939fa7de73ac51142764'}
for name, digest in expected_rules.items():
    assert hashlib.sha256((out/name).read_bytes()).hexdigest()==digest, name
# Use the exact frozen rules. No rule download and no source execution.
env = os.environ.copy()
certificates = sorted((root/'study/.venv/lib').glob('python*/site-packages/certifi/cacert.pem'))
if certificates: env['SSL_CERT_FILE']=str(certificates[0])
env.update({'SEMGREP_ENABLE_VERSION_CHECK':'0', 'SEMGREP_LOG_FILE':str(out/'semgrep.log'), 'SEMGREP_SETTINGS_FILE':str(out/'semgrep-settings.yml'), 'SEMGREP_SEND_METRICS':'off'})
targets = sorted(str(p) for p in source.glob('*.php'))
assert len(targets)==66
scan_records = []
for index in (1,2):
    dest = out / ('semgrep_run%d.json' % index)
    command = [scanner, 'scan', '--metrics', 'off', '--jobs', '1', '--no-git-ignore', '--config', str(out/'frozen_registry_php_rules.json'), '--config', str(out/'custom_php_rules_corrected.yaml'), '--json', '--output', str(dest)] + targets
    start = time.perf_counter()
    run = subprocess.run(command, cwd=base, env=env, capture_output=True, text=True)
    duration = time.perf_counter()-start
    (out / ('semgrep_run%d.stdout' % index)).write_text(run.stdout)
    (out / ('semgrep_run%d.stderr' % index)).write_text(run.stderr)
    data = json.loads(dest.read_text()) if dest.exists() else {}
    record = {'run':index, 'command':command, 'exit_code':run.returncode, 'duration_seconds':round(duration,3), 'version':data.get('version'), 'result_count':len(data.get('results',[])), 'errors':data.get('errors',[]), 'scanned_file_count':len(data.get('paths',{}).get('scanned',[])), 'counts_by_rule':dict(Counter(r['check_id'] for r in data.get('results',[])))}
    scan_records.append(record)
    print(json.dumps(record,ensure_ascii=False),flush=True)
    if run.returncode != 0 or data.get('errors'):
        print(run.stderr[-4000:],flush=True)
        break

def signatures(data):
    return set((r['check_id'],r['path'],r['start']['line'],r['start']['col'],r['end']['line'],r['end']['col']) for r in data['results'])
repeat = None
if len(scan_records)==2 and all(s['exit_code']==0 and not s['errors'] for s in scan_records):
    a=signatures(json.loads((out/'semgrep_run1.json').read_text()))
    b=signatures(json.loads((out/'semgrep_run2.json').read_text()))
    repeat={'only_run1':len(a-b),'only_run2':len(b-a),'identical':a==b,'signature_count':len(a)}
inventory=json.loads((out/'source_inventory.json').read_text())
checks=[{'file':row['file'],'matches':hashlib.sha256((source/row['file']).read_bytes()).hexdigest()==row['sha256']} for row in inventory]
manifest={'timestamp':datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat(), 'scan_runs':scan_records,'repeatability':repeat,'php_registry_rule_count':len(rules),'custom_rule_count':4,'registry_packs':packs,'source_unchanged':all(c['matches'] for c in checks),'source_checks':checks,'rule_file_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [out/'frozen_registry_php_rules.json',out/'custom_php_rules_corrected.yaml']},'original_rule_change':'Added final semicolon to echo mysql_error(...); in a copied configuration only.'}
(out/'sast_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
