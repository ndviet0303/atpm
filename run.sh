#!/usr/bin/env bash
# Tái lập lần quét hợp lệ trong báo cáo (Bảng 25): Semgrep OSS 1.176.1 với snapshot 24 rule registry
# + 4 rule tùy biến đã sửa, trên 66 tệp PHP của study/source/librarian/; kèm PHPStan level 0.
# Dùng: ./run.sh [thư_mục_kết_quả]   (mặc định: run_output/, không ghi đè study/results/ hay evidence/)
set -euo pipefail
cd "$(dirname "$0")"

OUT="${1:-run_output}"
VENV=study/.venv
EVID=outputs/Nhom13_23010359_NguyenDuyMinh_23010345_DangNhatNhat_23010636_NghiemDucViet_BTL/evidence
EXPECTED_SEMGREP=322
EXPECTED_PHPSTAN=17

if [ ! -x "$VENV/bin/semgrep" ]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install semgrep==1.176.1
fi
mkdir -p "$OUT"

# Rule đóng băng thay cho p/php... để kết quả không trôi theo registry (bản live hiện có 44 rule)
rc=0
"$VENV/bin/semgrep" scan --metrics off --jobs 1 --no-git-ignore \
  --config "$EVID/frozen_registry_php_rules.json" \
  --config "$EVID/custom_php_rules_corrected.yaml" \
  --json --output "$OUT/semgrep.json" \
  study/source/librarian/*.php > "$OUT/semgrep.log" 2>&1 || rc=$?
# Bỏ dòng nhắc nâng cấp và quảng cáo Semgrep Pro cho ảnh chụp gọn; log đầy đủ ở $OUT/semgrep.log
grep -vE 'new version of Semgrep|Semgrep Pro|sg\.run/false-positives' "$OUT/semgrep.log" | cat -s || true

# Bảng theo rule, đối chiếu Bảng 26 của báo cáo
python3 - "$OUT/semgrep.json" <<'PY'
import json, sys, collections
res = json.load(open(sys.argv[1]))['results']
rule = lambda x: x['check_id'].rsplit('.', 1)[-1]
meta = {rule(x): (x['extra']['severity'], x['extra'].get('metadata', {}).get('cwe', ['-'])[0].split(':')[0]) for x in res}
print(f"{'Số hit':>6}  {'Mức':<8} {'CWE':<8} Rule")
for r, n in collections.Counter(map(rule, res)).most_common():
    print(f"{n:>6}  {meta[r][0]:<8} {meta[r][1]:<8} {r}")
sev = collections.Counter(x['extra']['severity'] for x in res)
print(f"{len(res):>6}  " + ", ".join(f"{n} {s}" for s, n in sorted(sev.items())) + "\n")
PY

read -r semgrep_total semgrep_errors < <(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(len(d['results']), len(d['errors']))" "$OUT/semgrep.json")
echo "Semgrep: $semgrep_total cảnh báo, mã thoát $rc, $semgrep_errors lỗi công cụ (kỳ vọng $EXPECTED_SEMGREP, 0, 0)"

if command -v php >/dev/null && [ -f study/phpstan.phar ]; then
  php -d memory_limit=1G study/phpstan.phar analyse -c study/phpstan.neon \
    --error-format=json --no-progress > "$OUT/phpstan.json" || true
  phpstan_total=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['totals']['file_errors'])" "$OUT/phpstan.json")
  echo "PHPStan: $phpstan_total thông báo (kỳ vọng $EXPECTED_PHPSTAN)"
else
  echo "Bỏ qua PHPStan (thiếu php hoặc study/phpstan.phar)"
fi

# Lần quét hợp lệ = mã thoát 0 + errors rỗng + đúng số hit (lần 270 hit cũ có mã thoát 2)
[ "$rc" -eq 0 ] && [ "$semgrep_errors" -eq 0 ] && [ "$semgrep_total" -eq "$EXPECTED_SEMGREP" ] \
  || { echo "LỆCH so với baseline!" >&2; exit 1; }
echo "OK: khớp baseline. Kết quả tại $OUT/"
