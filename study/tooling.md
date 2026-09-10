# Hồ sơ Công cụ Phân tích Tĩnh (Static Analysis Tooling)

## 1. Khảo sát Danh sách Ngắn các Công cụ Phân tích Tĩnh PHP Cục bộ

Để phục vụ nghiên cứu kiểm thử tĩnh mã nguồn phân hệ thủ thư của hệ thống quản lý thư viện PHP cổ điển (PHP 5.x procedural), nhóm nghiên cứu đã tra cứu tài liệu chính thức hiện hành và lập danh sách đánh giá các công cụ chạy hoàn toàn cục bộ (offline / local execution):

| Tên công cụ | Đơn vị / Dự án | Tài liệu chính thức | Phương pháp phân tích | Trọng tâm chính |
|---|---|---|---|---|
| **Semgrep OSS** | Semgrep, Inc. | `https://semgrep.dev/docs/` | Phân tích cây cú pháp trừu tượng (AST), so khớp mẫu ngữ nghĩa (semantic pattern matching), taint analysis | Phát hiện lỗ hổng an toàn thông tin (OWASP, CWE), quy chuẩn mã an toàn |
| **PHPStan** | Ondřej Mirtes & Community | `https://phpstan.org/user-guide/getting-started` | Phân tích kiểu dữ liệu tĩnh (Static type analysis), kiểm tra ngữ nghĩa biểu thức | Phát hiện lỗi logic kiểu, biến chưa định nghĩa, gọi hàm không tồn tại |
| **Psalm** | Vimeo & Community | `https://psalm.dev/docs/` | Phân tích kiểu dữ liệu sâu (Type inference), phân tích dòng dữ liệu độc hại (Taint analysis) | Kiểm tra kiểu nghiêm ngặt và tìm kiếm lỗ hổng bảo mật dòng dữ liệu |
| **PHP_CodeSniffer & PHPCompatibility** | Squiz Labs / Wim Godden | `https://github.com/squizlabs/PHP_CodeSniffer` | Phân tích token (Tokenization / Lexical analysis) | Chuẩn phong cách mã (PSR-12) và tính tương thích phiên bản PHP |

---

## 2. Tiêu chí Lựa chọn Công cụ cho Dự án

Mã nguồn phân hệ thủ thư có các đặc thù kỹ thuật rõ rệt:
1. **Mã nguồn PHP 5.x thủ tục (procedural PHP):** Không sử dụng Composer, không tuân thủ autoloading PSR-4, không sử dụng class/namespace OOP, mã xử lý PHP lồng ghép trực tiếp với giao diện HTML.
2. **Sử dụng phần mở rộng cơ sở dữ liệu đã bị xóa (`mysql_*`):** Thư viện `mysql_connect`, `mysql_query` đã bị khai tử và loại bỏ từ PHP 7.0 trở đi.
3. **Yêu cầu không sửa đổi baseline:** Không được chỉnh sửa mã nguồn gốc chỉ để phục vụ công cụ phân tích chạy được.
4. **Mục tiêu an toàn phần mềm:** Cần phát hiện các lỗ hổng an ninh thông tin thực tế (SQL Injection, XSS, Broken Access Control, Hardcoded Credentials, Information Disclosure) thay vì chỉ tập trung vào phong cách thụt lề hay khai báo kiểu biến.

### Bảng đối chiếu tiêu chí lựa chọn:

- **Khả năng chạy cục bộ 100% (Local / Offline):** Semgrep OSS, PHPStan, Psalm và PHPCS đều đáp ứng.
- **Khả năng phân tích mã PHP cũ không có Composer/Autoload:** Semgrep vượt trội nhờ phân tích trực tiếp theo AST của từng tệp mã mà không phụ thuộc vào bộ nạp lớp hay cấu hình môi trường PHP runtime tương ứng. PHPStan và Psalm gặp trở ngại lớn do phụ thuộc vào autoloading và môi trường runtime hiện đại.
- **Trọng tâm bảo mật (Security Focus):** Semgrep được thiết kế chuyên biệt cho AppSec, có sẵn các bộ quy tắc chuẩn hóa theo OWASP Top 10 và CWE Top 25.

---

## 3. Thử nghiệm Thực tế trên Tập tệp Mẫu Baseline (Empirical Trial)

Nhóm nghiên cứu tiến hành thử nghiệm song song trên tập tệp mẫu của baseline gồm `login.php`, `dbcon.php` và `delete_user.php` mà **hoàn toàn không chỉnh sửa bất kỳ dòng mã nào của baseline**.

### 3.1. Thử nghiệm với PHPStan (Phiên bản 2.1.8)

- **Lệnh thực thi:**
  ```bash
  php study/phpstan.phar analyse study/source/librarian/login.php --level=0 --error-format=json
  ```
- **Hiện tượng và Giới hạn quan sát được:**
  - PHPStan thực thi trên môi trường máy chủ (PHP 8.5) lập tức dừng với mã thoát lỗi (Exit code 1) và báo 4 lỗi biểu tượng không tồn tại:
    - `Function mysql_error not found.` (line 7)
    - `Function mysql_query not found.` (line 7)
    - `Function mysql_num_rows not found.` (line 8)
    - `Function mysql_fetch_array not found.` (line 9)
  - Khi nhóm tiến hành cung cấp tệp stub giả lập các hàm `mysql_*` (`study/mysql_stub.php`) và thiết lập `level: 2`, PHPStan hoàn thành nhưng báo **0 lỗi**:
    - `{"totals":{"errors":0,"file_errors":0},"files":[],"errors":[]}`
  - **Đánh giá:** PHPStan bỏ sót hoàn toàn lỗ hổng SQL Injection nghiêm trọng tại dòng 6 của `login.php` (`select * from users where username='$username' and password='$password'`). Điều này chứng minh công cụ kiểm tra kiểu thông thường không phù hợp để đánh giá an toàn mã nguồn trong ngữ cảnh ứng dụng này.

### 3.2. Thử nghiệm với Semgrep OSS (Phiên bản 1.176.1)

- **Lệnh thực thi:**
  ```bash
  study/.venv/bin/semgrep scan --config "p/php" --config "p/sql-injection" --config "p/xss" study/source/librarian/login.php --json
  ```
- **Hiện tượng và Kết quả quan sát được:**
  - Semgrep phân tích thành công 100% cú pháp tệp `login.php` mà không gặp bất kỳ lỗi cú pháp nào.
  - Phát hiện ngay lập tức lỗ hổng SQL Injection nghiêm trọng:
    - **Check ID:** `php.lang.security.injection.tainted-sql-string.tainted-sql-string`
    - **CWE:** `CWE-89: Improper Neutralization of Special Elements used in an SQL Command`
    - **Vị trí:** `login.php` dòng 6, cột 11 đến 84.
    - **Thông báo:** Dữ liệu người dùng từ `$_POST['username']` và `$_POST['password']` chảy trực tiếp vào chuỗi truy vấn SQL nối thủ công.
  - Khi thử nghiệm trên `dbcon.php` với bộ quy tắc tùy biến:
    - Phát hiện hardcoded credentials trong lệnh `mysql_connect('localhost', 'root', '')` (CWE-798).
    - Phát hiện sử dụng API lỗi thời bị loại bỏ (CWE-477).

---

## 4. Quyết định Lựa chọn Công cụ và Chiến lược Phân tích

Dựa trên kết quả thử nghiệm thực nghiệm:

1. **Công cụ tự động chính:** Chọn **Semgrep OSS phiên bản 1.176.1**.
   - **Bộ quy tắc áp dụng:**
     - Bộ quy tắc chính thức: `p/php`, `p/sql-injection`, `p/xss`, `p/owasp-top-ten`, `p/cwe-top-25`.
     - Bộ quy tắc tùy biến ngữ cảnh dự án (`study/rules/custom_php_rules.yaml`): Nhận diện các mẫu truy vấn `mysql_*` cổ điển, in lỗi trực tiếp qua `die(mysql_error())`, và thông tin kết nối CSDL cố định.
   - **Lệnh quét chuẩn:**
     ```bash
     study/.venv/bin/semgrep scan \
       --config "p/php" \
       --config "p/sql-injection" \
       --config "p/xss" \
       --config study/rules/custom_php_rules.yaml \
       study/source/librarian/ \
       --json --output study/results/semgrep_raw.json
     ```
2. **Phương pháp kết hợp (Hybrid Approach):**
   - Công cụ tĩnh tự động chịu trách nhiệm rà quét trên diện rộng (66 tệp) để lập danh sách cảnh báo thô (raw alerts) đối với SQLi, XSS, lỗi thời API và lộ thông tin lỗi.
   - Chuyên gia kiểm thử thực hiện **rà soát thủ công (Manual Code Review)** đối chiếu theo Checklist (`study/checklist.md`) cho các vấn đề mà công cụ tự động khó nhận diện:
     - Kiểm tra sự thiếu vắng kiểm soát phiên (Missing Session Verification / Broken Access Control) tại các endpoint xử lý `delete_*.php`, `*_save.php`.
     - Đánh giá toàn vẹn nghiệp vụ mượn–trả sách (Business Logic & Transaction Integrity).
     - Rà soát các phụ thuộc include bị gãy và bảng CSDL không tồn tại.
   - Toàn bộ kết quả từ cả hai phương pháp được đưa vào Sổ phát hiện (`study/findings.md`) để thẩm định chéo.
