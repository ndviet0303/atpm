# Nghiên cứu An toàn Phần mềm: Đánh giá Mã nguồn Phân hệ Thủ thư bằng Kiểm thử Tĩnh

Dự án thực nghiệm học phần **An toàn phần mềm**: Áp dụng phương pháp kiểm thử tĩnh (Static Testing - kết hợp rà soát thủ công theo Checklist và phân tích tự động bằng Semgrep OSS) để đánh giá toàn diện an toàn mã nguồn phân hệ thủ thư (`librarian/`) thuộc hệ thống quản lý thư viện PHP mã nguồn mở.

---

## 1. Thông tin Baseline Khảo sát

- **Kho lưu trữ gốc:** [vinitshahdeo/Library-Management-System](https://github.com/vinitshahdeo/Library-Management-System)
- **Commit chốt:** `082d6fb9bdd7846b57033513791ba5b6d2095c11`
- **Giấy phép gốc:** MIT License (bảo toàn nguyên vẹn tại `study/source/LICENSE`)
- **Nguyên tắc an toàn:** Không thực thi ứng dụng upstream, không chạy CSDL trực tiếp, không khai thác tấn công động; 100% phân tích tĩnh và đọc mã nguồn.

---

## 2. Cấu trúc Dự án

```
atpm/
├── README.md                      # Giới thiệu tổng quan dự án
├── .gitignore                     # Bỏ qua môi trường ảo và tệp nhị phân
├── run.sh                         # Tái lập lần quét hợp lệ (322 cảnh báo) + PHPStan
├── outputs/Nhom13_..._BTL/        # Gói nộp: báo cáo PDF/Word, Excel, bằng chứng, mã sinh, mô hình
├── openspec/                      # Quản lý vòng đời đặc tả nghiên cứu (OpenSpec)
│   └── changes/archive/           # Artifacts nghiên cứu đã hoàn thành và lưu trữ
└── study/                         # Toàn bộ hồ sơ nghiên cứu và sản phẩm thực nghiệm
    ├── baseline.md                # Nguồn gốc commit, thời điểm và các mã băm SHA-256
    ├── scope.md                   # Kiểm kê 66 tệp PHP (2,551 SLOC), sơ đồ include, CSDL
    ├── checklist.md               # Bảng kiểm tra 25 tiêu chí (7 nhóm an toàn)
    ├── tooling.md                 # Khảo sát, thực nghiệm và cấu hình công cụ SAST
    ├── findings.md                # Sổ theo dõi 11 phát hiện xác nhận, 1 false positive, 1 inconclusive
    ├── summary.md                 # Tổng hợp số liệu định lượng và ma trận phân loại CWE
    ├── report.md                  # Báo cáo học thuật hoàn chỉnh (7 chương)
    ├── source/                    # Bản sao snapshot mã nguồn baseline tại commit đã chốt
    ├── rules/                     # Bộ quy tắc tùy biến Semgrep (`custom_php_rules.yaml`)
    └── results/                   # Kết quả quét thô (JSON), siêu dữ liệu và báo cáo tái lập
```

---

## 3. Tóm tắt Kết quả Nghiên cứu

> **Lưu ý về số liệu (270 và 322).** Mục này và các tệp trong `study/` ghi lại lần quét lịch sử ngày 10/09/2026: 270 cảnh báo, nhưng Semgrep trả mã thoát 2 vì rule CWE-209 trong `study/rules/custom_php_rules.yaml` lỗi parse (pattern `echo mysql_error(...)` thiếu dấu `;`), nên rule đó không chạy và thiếu đúng 52 hit. Báo cáo nộp dùng lần quét hợp lệ ngày 04/10/2026: snapshot 24 rule registry + 4 rule tùy biến đã sửa, **322 cảnh báo**, mã thoát 0, trường `errors` rỗng, hai lần quét trùng 322/322 chữ ký. Khi thẩm định lại, checklist tăng từ 25 lên 27 tiêu chí và số handler thiếu kiểm tra phiên từ 8 lên 12. Gói nộp đầy đủ nằm ở `outputs/Nhom13_23010359_NguyenDuyMinh_23010345_DangNhatNhat_23010636_NghiemDucViet_BTL/`; lệnh và `check_id` trong `evidence/sast_manifest.json` mang tên thư mục làm việc `outputs/bao_cao_thu_vien_20261004/` (bản trùng, không commit), số đếm không đổi.

- **Quy mô phân hệ:** 66 tệp PHP, 2,978 dòng vật lý, **2,551 dòng mã thực tế (SLOC)**.
- **Cảnh báo thô (Raw Alerts):** 270 cảnh báo từ Semgrep OSS 1.176.1 + 17 lỗi tệp từ PHPStan.
- **Phát hiện xác nhận tĩnh (`confirmed-static`):** **11 nhóm phát hiện kỹ thuật**:
  - **CRITICAL (2):** SQL Injection gây Authentication Bypass tại `login.php` (CWE-89); Missing Session Check / Broken Access Control tại 8 endpoint xử lý dữ liệu (`delete_*.php`, `*_save.php`) (CWE-306, CWE-284).
  - **HIGH (4):** SQL Injection diện rộng tại các hàm CRUD (CWE-89); Stored/Reflected XSS (CWE-79); Mật khẩu lưu và hiển thị dạng bản rõ (CWE-256, CWE-312); Thao tác xóa qua HTTP GET thiếu Anti-CSRF token (CWE-352).
  - **MEDIUM (3):** Race Condition & thiếu Transaction trong mượn sách (CWE-362); Hardcoded CSDL credentials (CWE-798); Sử dụng thư viện `mysql_*` lỗi thời đã bị khai tử (CWE-477).
  - **LOW (2):** Lộ cấu trúc CSDL qua `mysql_error()` (CWE-209); Include tệp gãy và tệp rỗng 0 bytes (CWE-398).
- **Cảnh báo giả (`false-positive`):** 01 trường hợp tiêu biểu (`FP-01`) do công cụ tự động gán nhầm nguồn tainted request vào khóa chính số trong CSDL.
- **Mục chưa đủ đặc tả (`inconclusive`):** 01 nhóm giả định nghiệp vụ mượn sách (`BIZ-INC-01`) do upstream không cung cấp tài liệu SRS.
- **Tính tái lập:** Chạy lặp lại (Run 1 vs Run 2) đạt tính tất định tuyệt đối 100% với độ lệch 0%.

---

## 4. Hướng dẫn Tái lập Kết quả (Reproducibility)

Yêu cầu môi trường: Python 3.10+, bash; thêm PHP và `study/phpstan.phar` nếu muốn chạy cả PHPStan (thiếu thì script bỏ qua bước này).

```bash
./run.sh
```

Kỳ vọng: `Semgrep: 322 cảnh báo, mã thoát 0, 0 lỗi công cụ` và `PHPStan: 17 thông báo`. Script tự tạo `study/.venv` với Semgrep 1.176.1, quét 66 tệp `study/source/librarian/*.php` bằng bộ rule đóng băng trong `evidence/` của gói nộp, ghi kết quả vào `run_output/` và trả mã khác 0 nếu lệch.

Lần quét lịch sử 270 cảnh báo dùng `--config p/php --config p/sql-injection --config p/xss --config study/rules/custom_php_rules.yaml`; chạy lại lệnh đó có thể ra số khác vì registry thay đổi theo thời gian.
