"""Lint and scan generated PHP text, without invoking its functions."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import os
import subprocess
import shutil

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
SCANNER = os.environ.get('SEMGREP_BIN') or (str(ROOT / 'study/.venv/bin/semgrep') if (ROOT/'study/.venv/bin/semgrep').exists() else shutil.which('semgrep'))
assert SCANNER, 'Install Semgrep 1.176.1 or set SEMGREP_BIN'
E = BASE / 'evidence'
rules = E / 'generated_case_rules.yaml'
records = []
for version in ('_v0', '_v1'):
    files = sorted((BASE / 'generated_cases' / version).glob('*.php'))
    lint = []
    for path in files:
        check = subprocess.run(['php', '-l', str(path)], capture_output=True, text=True)
        lint.append({'file': path.name, 'exit_code': check.returncode,
                     'stdout': check.stdout, 'stderr': check.stderr})
        assert check.returncode == 0
    command = [SCANNER, 'scan', '--metrics', 'off', '--jobs', '1', '--no-git-ignore',
               '--config', str(rules), '--json', '--output', str(E / ('generated' + version + '.json'))]
    command.extend(str(path) for path in files)
    env = dict(os.environ)
    env['SEMGREP_SEND_METRICS'] = 'off'
    env['SEMGREP_ENABLE_VERSION_CHECK'] = '0'
    certificates = sorted((ROOT / 'study/.venv/lib').glob('python*/site-packages/certifi/cacert.pem'))
    if certificates:
        env['SSL_CERT_FILE'] = str(certificates[0])
    env['SEMGREP_SETTINGS_FILE'] = str(E / 'generated_semgrep_settings.yml')
    env['SEMGREP_LOG_FILE'] = str(E / 'generated_semgrep.log')
    check = subprocess.run(command, capture_output=True, text=True, env=env)
    (E / ('generated' + version + '.stdout')).write_text(check.stdout)
    (E / ('generated' + version + '.stderr')).write_text(check.stderr)
    raw = json.loads((E / ('generated' + version + '.json')).read_text())
    assert check.returncode == 0 and not raw['errors'], (check.returncode, raw['errors'])
    records.append({'version': version, 'command': command, 'exit_code': check.returncode,
                    'semgrep_version': raw['version'], 'errors': raw['errors'],
                    'findings': len(raw['results']),
                    'by_rule': dict(Counter(r['check_id'] for r in raw['results'])),
                    'by_file': dict(Counter(Path(r['path']).name for r in raw['results'])),
                    'lint': lint})
assert records[0]['findings'] > 0 and records[1]['findings'] == 0
(E / 'generated_static_results.json').write_text(json.dumps({
    'scope': '10 generated cases only; six narrow educational rules',
    'rule_sha256': hashlib.sha256(rules.read_bytes()).hexdigest(),
    'runs': records,
    'limits': 'Zero selected rule hits is not proof of application security or cryptographic correctness.'
}, ensure_ascii=False, indent=2))
print(json.dumps([{k: r[k] for k in ('version', 'findings', 'by_file', 'by_rule')} for r in records], indent=2))
