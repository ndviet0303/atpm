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
├── chon_test.py                   # Giao diện web chọn test, chạy trên bản sao gói nộp, xuất báo cáo HTML
├── bien_ban_test.py               # Chạy đủ 12 test, xuất biên bản kiểm thử Word (outputs/Bien_ban_test_Nhom13.docx)
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

### Chọn test bằng giao diện

```bash
python3 chon_test.py
```

Script mở `http://127.0.0.1:8790` (đổi cổng: `python3 chon_test.py 8791`). Mỗi lần khởi động, script chép gói nộp sang `run_output/goi_chay_lai/` và chạy 12 bước của gói trên bản sao đó, nên `evidence/` và `checksums.json` của gói nộp không bị ghi đè. Sau mỗi lượt chạy, kết quả, nhật ký và báo cáo được lưu vào `run_output/goi_chay_lai/lan_chay.json`; lần mở sau, nếu gói nộp chưa đổi (so thời điểm sửa mới nhất của mọi tệp trong gói), giao diện giữ bản sao và nạp lại các test đã chạy, khỏi chạy lại. Gói đổi thì bản sao được chép mới và các test về "Chưa chạy". Muốn chạy lại từ đầu, xóa `run_output/goi_chay_lai/lan_chay.json` trước khi mở. Cột trái từ trên xuống có các phần sau:
- thẻ nguồn kiểm thử, có link tới `source_v0/librarian/`, `evidence/` và `generated_cases/`;
- danh sách 12 test: tích rồi bấm "Chạy các test đã chọn", mỗi test hiện Đạt hoặc Lỗi;
- ba nút bước 1–3, mỗi nút chạy cả một nhóm (Static testing, Mã sinh và hình thức, Bộ nhớ);
- nút "Chạy toàn bộ 12 test";
- nút "Mở báo cáo HTML", bật sau lần chạy đầu tiên;
- ô "Đầu vào đặc tả (JSON)", xem mục dưới.

Cột phải có ba khối:
- nhật ký chạy;
- chi tiết test đang chọn: kỳ vọng, mã thoát, nút "Chạy test này", và các tab mở script, tệp kết quả, file rule kèm số dòng;
- sơ đồ của test đang chọn, đổi theo test.

Kết quả theo nhánh mã nằm ở hai tab sơ đồ, mục lỗi tô đỏ. Tab "Kết quả v0" có hai nhánh `source_v0` (mã gốc) và `_v0` (mã lỗi cố ý); tab "Kết quả v1" có `_v1` (mã đã sửa) và `source_v1`. Nút không thuộc nhánh nào (unit test, ca đối chứng của bộ giải) hiện ở cả hai tab. Ba nhánh mã:
- `source_v0`: mã gốc;
- `_v0`: mã lỗi cố ý;
- `_v1`: mã đã sửa.

Hai nhánh `_v0` và `_v1` liệt kê cùng các tệp theo cùng thứ tự, kể cả tệp 0 hit, để so từng cặp.

Nhánh `source_v1` lấy từ `bo_sung_v1/`: `make_v1.py` sinh `source_v1/` từ `source_v0` theo các đoạn mã ở Chương 7, còn `check_v1.py <test>` chạy cùng phép kiểm trên `source_v1` và ghi `bo_sung_v1/evidence_v1/<test>_v1.json`. Tám test (kiem_ke, sast, bao_cao, phpstan, sql, auth, bo_nho_tinh, bo_nho_case) chạy thêm bước này ngay sau lệnh chính, nhật ký ghi mã thoát của cả hai, và cột thực tế nối thêm số liệu v1. Test mô hình xác thực có thêm sơ đồ Kripke của `source_v1`. Khi nào Nhất gửi bản vá của Chương 7, thay `bo_sung_v1/source_v1/` bằng bản đó rồi chạy lại test. Sơ đồ của test "Sổ hồ sơ test case" xếp mỗi hồ sơ vào đúng một nhánh: TC-17–22 ở `_v0`, TC-23–28 ở `_v1`, ca đối chứng của bộ giải DPLL có nút riêng. Test mô hình xác thực có thêm sơ đồ Kripke. Test trạng thái bộ nhớ có mô hình đầy đủ và một sơ đồ Kripke cho mỗi nhánh `source_v0`, `_v0`, `_v1`, `source_v1`, vẽ bằng cách phát lại chuỗi sự kiện của từng đối tượng: trạng thái là (typestate, vi phạm vừa sinh) mang nhãn mệnh đề, cạnh ghi mệnh đề PHP kèm số lần. Hai test bộ nhớ còn lại hiện cùng các Kripke đó (ba test là ba cách kiểm cùng một mô hình). Test DPLL/SAT và test 54 truy vấn SQL có tab "Cây DPLL": cây tìm kiếm của từng ca dựng lại từ vết `unit`/`pure`/`branch`/`conflict` mà `run_models.py` ghi, gom theo nhánh mã (SQL chia B trước sửa, A sau sửa, C hợp lệ); lá xung đột và lá SAT là phản ví dụ tô đỏ, ca UNSAT phải có mọi lá là xung đột và đường của ca SAT phải khớp nhân chứng đã ghi. Tab SQL có 54 cây, dùng "Xem toàn màn hình" và nút phóng to để đọc. Các test khác không có trạng thái hay phép chuyển nên không có Kripke. Nút "Xem toàn màn hình" phóng to khung sơ đồ. Kéo thanh chia giữa hai cột, hoặc dùng phím mũi tên, để đổi độ rộng. Giao diện theo màu của shadcn/ui và tự đổi sáng/tối theo hệ thống. Báo cáo nằm ở `run_output/goi_chay_lai/bao_cao.html`. Báo cáo có bảng kỳ vọng so với thực tế và một mục riêng cho mỗi test đã chạy: phát hiện Semgrep nhóm theo rule (CWE, FIND, vị trí, dòng mã), thông báo PHPStan, bài toán SAT/SMT, 54 truy vấn SQL, danh sách unit test, sổ 822 hồ sơ test case, lỗi bộ nhớ PHP/C. Báo cáo dùng cùng bảng màu shadcn với giao diện, và mỗi mục có đúng các sơ đồ mà giao diện hiện cho test đó, xếp liền nhau để in. Mục mô hình xác thực có sơ đồ Kripke vẽ từ `auth_model.json` (đường phản ví dụ tô đỏ). Mục bộ nhớ có Kripke cho từng nhánh và mô hình đầy đủ 13 trạng thái vẽ từ `memory_case_results.json` (phép chuyển sinh vi phạm tô đỏ, ghi mã E_…); mỗi nhóm vi phạm ghi phép chuyển tương ứng để dò trên sơ đồ. Sơ đồ viết bằng cú pháp Mermaid và vẽ bằng [Pele](https://pele.run/) 1.3.0 tải từ CDN, có nút phóng to/thu nhỏ; khi offline, trang hiện văn bản định nghĩa sơ đồ thay cho hình. Nút "In / lưu PDF" để xuất PDF.

#### Đầu vào đặc tả (JSON)

Ô này nhận file `.json` cùng định dạng với SpecVerificationLab.exe (`dataset/specs/FORMAT.md` của exe): chọn một đặc tả mẫu trong `dac_ta/` rồi bấm "Nạp đặc tả đã chọn", hoặc bấm "Nạp từ file JSON khác…". Giao diện vẽ Kripke của `state_machine` và từng `additional_flows`, kiểm từng công thức trong `safety_properties` (`AG/EF/AF/EG/AX/EX` với `(p)` hoặc `(!p)`, như parser của exe), `mutual_exclusion` và trạng thái deadlock, in phản ví dụ hoặc nhân chứng và tô đỏ trạng thái `violation`. Kết quả mỗi lần nạp ghi vào `dac_ta/ket_qua/<tên>.json`. Phần `functions` và `arithmetic_checks` (sinh mã, Z3 của exe) chưa chạy, giao diện ghi rõ khi file có các phần này.

Sáu đặc tả mẫu do `python3 dac_ta/tao_dac_ta.py` sinh từ evidence của gói: `nhom13_xac_thuc_source_v0/v1` (luồng đăng nhập, phân quyền) và `nhom13_bo_nho_source_v0/v0/v1/source_v1` (Kripke bộ nhớ của bốn nhánh, kiểm `AG(!violation)`, `AG(!E_…)` từng loại vi phạm và `EF(released)`). Kết quả mẫu nằm sẵn trong `dac_ta/ket_qua/`. Ngày 30/10/2026 đã đối chiếu với chính bộ kiểm của exe trên 6 đặc tả này và 7 đặc tả mẫu của exe: cả 12 file có `state_machine` ra cùng kết quả từng công thức, deadlock và loại trừ (`resource_pool_spec.json` không có `state_machine`, cả hai đều bỏ qua). Các file này cũng nạp được vào exe bằng nút "Nạp từ file JSON khác...".

Rule nằm ở `evidence/` của gói nộp: `custom_php_rules_corrected.yaml` (4 rule tự viết), `frozen_registry_php_rules.json` (24 rule registry), `memory_rules.yaml` (11 rule bộ nhớ), `generated_case_rules.yaml` (6 rule cho mã sinh). Riêng PHPStan dùng `tools/phpstan.neon`. Trên giao diện, mỗi test có link mở thẳng file rule mà nó nạp. Tệp `study/rules/custom_php_rules.yaml` là bản cũ, lỗi parse (lần quét 270), không dùng nữa.

### Biên bản kiểm thử

```bash
python3 bien_ban_test.py
```

Chạy đủ 12 test của `chon_test.py` trên bản sao riêng `run_output/bien_ban/` (chạy được cả khi giao diện đang mở) và ghi `outputs/Bien_ban_test_Nhom13.docx`: thông tin chung, môi trường, bảng kỳ vọng/thực tế, sổ phát hiện, lỗi bộ nhớ, kết luận, chỗ ký và lệnh chạy ở phụ lục. Mục kiểm thử lại trên source_v1 để trống, chờ `bo_sung_v1/`.

Lần quét lịch sử 270 cảnh báo dùng `--config p/php --config p/sql-injection --config p/xss --config study/rules/custom_php_rules.yaml`; chạy lại lệnh đó có thể ra số khác vì registry thay đổi theo thời gian.
