"""Static runs for the memory study: php -l, Semgrep memory rules, clang --analyze and gcc -fanalyzer.
No PHP function, binary or database is executed; compilers only parse and analyse (-c -o /dev/null)."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import os
import re
import shutil
import subprocess

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
E = BASE / 'evidence'
SCANNER = os.environ.get('SEMGREP_BIN') or (str(ROOT / 'study/.venv/bin/semgrep') if (ROOT / 'study/.venv/bin/semgrep').exists() else shutil.which('semgrep'))
assert SCANNER, 'Install Semgrep 1.176.1 or set SEMGREP_BIN'
GCC_IMAGE = 'gcc@sha256:2cb9daf6237bf6837fc1445eff1737b626fd640f5827e6c290d15ffbe5930bf5'  # gcc:14, GCC 14.4.0
rules = E / 'memory_rules.yaml'
TARGETS = ['source_v0/librarian', 'generated_cases/memory', 'generated_cases/memory_c',
           'generated_cases/_v0', 'generated_cases/_v1']
C_FILES = sorted((BASE / 'generated_cases/memory_c').glob('_v*/*.c'))
# clang SARIF has no CWE taxa; the checker message names the defect
CLANG_CWE = [(r'leak', 'CWE-401'), (r'after it is freed', 'CWE-416'), (r'free released memory', 'CWE-415'),
             (r'garbage value|uninitiali[sz]ed', 'CWE-457'), (r'null pointer', 'CWE-476'),
             (r'out of bound', 'CWE-787')]


def group(path):
    parts = Path(path).parts
    if parts[0] == 'source_v0':
        return 'baseline'
    return '/'.join(parts[1:3]) if parts[1].startswith('memory') else 'generated/' + parts[1]


def sarif(raw, tool):
    findings = []
    for run in raw['runs']:
        for r in run.get('results', []):
            region = r['locations'][0]['physicalLocation']
            text = r['message']['text']
            if tool == 'clang':
                cwe = [c for p, c in CLANG_CWE if re.search(p, text, re.I)][:1]
                assert cwe, ('clang message without CWE mapping', text)
            else:
                cwe = ['CWE-' + t['id'] for t in r.get('taxa', []) if t['toolComponent']['name'] == 'cwe']
            events = [{'line': l['location']['physicalLocation']['region']['startLine'],
                       'event': l['location'].get('message', {}).get('text', '')}
                      for flow in r.get('codeFlows', [])[:1] for tf in flow['threadFlows'] for l in tf['locations']]
            findings.append({'rule': r['ruleId'], 'cwe': cwe, 'line': region['region']['startLine'],
                             'message': text, 'path_events': events})
    return findings


lint = []
for path in sorted((BASE / 'generated_cases/memory').glob('_v*/*.php')):
    check = subprocess.run(['php', '-l', str(path)], capture_output=True, text=True)
    lint.append({'file': str(path.relative_to(BASE)), 'exit_code': check.returncode, 'stdout': check.stdout})
    assert check.returncode == 0, check.stderr

env = dict(os.environ, SEMGREP_SEND_METRICS='off', SEMGREP_ENABLE_VERSION_CHECK='0',
           SEMGREP_SETTINGS_FILE=str(E / 'memory_semgrep_settings.yml'), SEMGREP_LOG_FILE=str(E / 'memory_semgrep.log'))
certificates = sorted((ROOT / 'study/.venv/lib').glob('python*/site-packages/certifi/cacert.pem'))
if certificates:
    env['SSL_CERT_FILE'] = str(certificates[0])
command = [SCANNER, 'scan', '--metrics', 'off', '--jobs', '1', '--no-git-ignore', '--config', str(rules.relative_to(BASE)),
           '--json', '--output', 'evidence/memory_semgrep.json', *TARGETS]
check = subprocess.run(command, capture_output=True, text=True, env=env, cwd=BASE)
raw = json.loads((E / 'memory_semgrep.json').read_text())
assert check.returncode == 0 and not raw['errors'], (check.returncode, raw['errors'])
hits = [{'group': group(r['path']), 'file': r['path'], 'line': r['start']['line'], 'rule': r['check_id'],
         'cwe': r['extra']['metadata']['cwe']} for r in raw['results']]
semgrep = {'command': command, 'exit_code': check.returncode, 'semgrep_version': raw['version'],
           'errors': raw['errors'], 'findings': len(hits),
           'by_group_rule': {g: dict(Counter(h['rule'] for h in hits if h['group'] == g))
                             for g in sorted({h['group'] for h in hits})},
           'hits': hits}

compilers = []
clang_version = subprocess.run(['clang', '--version'], capture_output=True, text=True).stdout.splitlines()[0]
docker = shutil.which('docker')
for path in C_FILES:
    rel = str(path.relative_to(BASE / 'generated_cases/memory_c'))
    out = BASE / 'evidence' / 'memory_clang.sarif'
    run = subprocess.run(['clang', '--analyze', '--analyzer-output', 'sarif', '-o', str(out), str(path)],
                         capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    compilers.append({'tool': 'clang', 'file': rel, 'findings': sarif(json.loads(out.read_text()), 'clang')})
    out.unlink()
    if not docker:
        compilers.append({'tool': 'gcc', 'file': rel, 'skipped': 'docker not installed'})
        continue
    run = subprocess.run(['docker', 'run', '--rm', '--network', 'none', '-v', f'{path.parent}:/src:ro', '-w', '/src',
                          GCC_IMAGE, 'gcc', '-std=gnu17', '-O0', '-Wall', '-fanalyzer',
                          '-fdiagnostics-format=sarif-stderr', '-c', '-o', '/dev/null', path.name],
                         capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    compilers.append({'tool': 'gcc', 'file': rel, 'findings': sarif(json.loads(run.stderr), 'gcc')})

ran = [c for c in compilers if 'findings' in c]
assert not any(c['findings'] for c in ran if c['file'].startswith('_v1')), '_v1 must be clean'
assert all(any(c['findings'] for c in ran if c['file'] == f'_v0/{p.name}')
           for p in C_FILES if p.parent.name == '_v0'), 'every _v0 needs a compiler finding'
summary = {f"{c['tool']}:{c['file']}": sorted({f"{f['line']} {','.join(f['cwe']) or f['rule']}" for f in c['findings']},
                                                 key=lambda s: int(s.split()[0])) for c in compilers if 'findings' in c}
(E / 'memory_static_results.json').write_text(json.dumps({
    'scope': 'Static only: generated PHP is linted, PHP and C text is scanned, C is analysed by compilers without linking or running',
    'rule_sha256': hashlib.sha256(rules.read_bytes()).hexdigest(),
    'php_lint': lint,
    'semgrep': semgrep,
    'compilers': {'clang': clang_version, 'gcc_image': GCC_IMAGE, 'runs': compilers},
    'limits': 'Semgrep PHP hits are candidates (no schema, no refcount); models/memory_typestate.py decides them. '
              'Zero analyzer findings on _v1 covers only the defect classes these analyzers model.'
}, ensure_ascii=False, indent=2))
print(json.dumps({'semgrep': semgrep['by_group_rule'], 'compilers': summary}, ensure_ascii=False, indent=2))
