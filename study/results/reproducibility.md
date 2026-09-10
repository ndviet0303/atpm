# Báo cáo Kiểm tra Tính Tái lập và Toàn vẹn Baseline (Reproducibility Report)

## 1. Xác minh Toàn vẹn Mã nguồn Baseline (Checksum Verification)

Trước khi thực hiện chạy lặp lại, toàn bộ các mã băm SHA-256 của baseline được kiểm tra đối chiếu lại với các giá trị đã chốt trong `study/baseline.md` và `study/scope.md`:

| Tệp kiểm tra | SHA-256 ban đầu (`baseline.md`) | SHA-256 kiểm tra lại | Kết quả đối chiếu |
|---|---|---|:---:|
| `study/source/LICENSE` | `2e21d291d98be3562c6c122c35e9e624ef31950db4fdfbd95a5aa5b23ce192c0` | `2e21d291d98be3562c6c122c35e9e624ef31950db4fdfbd95a5aa5b23ce192c0` | **KHỚP 100% (Bất biến)** |
| `study/source/db/eb_lms.sql` | `1d2817e54dfc20d81e169e8080a05f4bc805711e8676359ee69f6d67f20ce8d4` | `1d2817e54dfc20d81e169e8080a05f4bc805711e8676359ee69f6d67f20ce8d4` | **KHỚP 100% (Bất biến)** |
| Toàn bộ 66 tệp PHP `librarian/*.php` | Danh mục bảng trong `study/scope.md` | Đã quét và đối chiếu toàn bộ | **KHỚP 100% (Bất biến)** |

*Kết luận toàn vẹn:* Không có bất kỳ tệp mã nguồn nào trong baseline bị thay đổi, chỉnh sửa hay sinh tệp rác trong suốt quá trình nghiên cứu.

---

## 2. Đối chiếu Kết quả Chạy Lặp lại (Run 1 vs Run 2)

- **Môi trường:** Máy trạm Apple M1, macOS Darwin, Python 3.14 venv, Semgrep OSS 1.176.1.
- **Cấu hình quét lặp lại:**
  ```bash
  study/.venv/bin/semgrep scan \
    --config "p/php" \
    --config "p/sql-injection" \
    --config "p/xss" \
    --config study/rules/custom_php_rules.yaml \
    --exclude 'vendors' \
    study/source/librarian/ \
    --json --output study/results/semgrep_run2.json
  ```
- **Số lượng cảnh báo ghi nhận:**
  - Lần chạy 1 (`study/results/semgrep_raw.json`): **270 cảnh báo**.
  - Lần chạy 2 (`study/results/semgrep_run2.json`): **270 cảnh báo**.
- **Đối chiếu chữ ký cảnh báo (`check_id`, `path`, `start_line`, `start_col`, `end_line`):**
  - Chữ ký chỉ có ở Lần 1: `0`.
  - Chữ ký chỉ có ở Lần 2: `0`.
  - Độ lệch chênh lệch: `0%` (Hoàn toàn trùng khớp 100%).

## 3. Kết luận về Tính Tái lập (Determinism)

Phương pháp phân tích tĩnh tự động với Semgrep OSS trên bộ quy tắc đã chọn đạt tính tất định tuyệt đối (deterministic). Bất kỳ nhà nghiên cứu độc lập nào khi sử dụng cùng commit `082d6fb9bdd7846b57033513791ba5b6d2095c11` và cùng bộ cấu hình đều có thể thu được kết quả chính xác 270 cảnh báo trên 66 tệp mã nguồn mà không có sự sai lệch ngẫu nhiên.
