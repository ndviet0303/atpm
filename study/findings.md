# Sổ Theo dõi và Thẩm định Phát hiện An toàn Mã nguồn (Findings Registry)

## 1. Tổng quan Thẩm định và Tóm tắt Số liệu

Quá trình phân tích tĩnh kết hợp hai phương pháp:
- **Phân tích tự động bằng Semgrep OSS (1.176.1):** Quét toàn bộ 66 tệp PHP trong phạm vi phân hệ thủ thư, ghi nhận **270 cảnh báo thô (raw alerts)**.
- **Rà soát thủ công chuyên sâu (Manual Code Review):** Đối chiếu 25 tiêu chí theo Checklist an toàn (`study/checklist.md`), kiểm tra luồng xác thực, kiểm soát truy cập, toàn vẹn nghiệp vụ và liên kết tệp.

### Kết quả sau Quá trình Thẩm định và Gộp trùng:
- **Tổng số cảnh báo thô từ công cụ:** 270 cảnh báo.
- **Tổng số phát hiện sau khi gộp theo nguyên nhân gốc (Deduplicated Findings):** **11 nhóm phát hiện kỹ thuật** được xác nhận tĩnh (`confirmed-static`).
- **Cảnh báo giả được ghi nhận và phân tích (False Positive):** **01 trường hợp tiêu biểu (`FP-01`)** do công cụ tự động gán nhầm nguồn dữ liệu tainted từ request vào khóa chính số `book_id` lấy từ CSDL.
- **Mục nghiệp vụ chưa đủ căn cứ đặc tả (Inconclusive / Unspecified Assumption):** **01 nhóm nghiệp vụ (`BIZ-INC-01`)** về kiểm tra số lượng tồn kho và hạn mức mượn sách.

### Bảng Thống kê Phát hiện theo Mức độ Nghiêm trọng

| Mức độ nghiêm trọng | Số lượng phát hiện | Danh sách mã phát hiện | Trạng thái thẩm định |
|---|:---:|---|:---:|
| **CRITICAL** | 2 | `FIND-01`, `FIND-02` | `confirmed-static` |
| **HIGH** | 4 | `FIND-03`, `FIND-04`, `FIND-05`, `FIND-06` | `confirmed-static` |
| **MEDIUM** | 3 | `FIND-07`, `FIND-08`, `FIND-09` | `confirmed-static` |
| **LOW / INFO** | 2 | `FIND-10`, `FIND-11` | `confirmed-static` |
| **FALSE POSITIVE** | 1 | `FP-01` | `false-positive` |
| **INCONCLUSIVE** | 1 | `BIZ-INC-01` | `inconclusive` |
| **TỔNG CỘNG** | **13** | | |

---

## 2. Chi tiết Các Phát hiện Được Xác nhận Tĩnh (`confirmed-static`)

---

### FIND-01: SQL Injection tại Endpoint Đăng nhập dẫn đến Vượt qua Xác thực (Authentication Bypass)

- **Mã định danh:** `FIND-01`
- **Nguồn phát hiện:** Semgrep (`php.lang.security.injection.tainted-sql-string`) & Rà soát thủ công (Checklist `AUTH-01`).
- **Commit khảo sát:** `082d6fb9bdd7846b57033513791ba5b6d2095c11`.
- **Tệp và dòng mã:** `study/source/librarian/login.php` (dòng 4 - 7).
- **Đoạn trích mã nguồn:**
  ```php
  $username = $_POST['username'];
  $password = $_POST['password'];
  $query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
  $result = mysql_query($query)or die(mysql_error());
  ```
- **Mô tả luồng dữ liệu / Ngữ cảnh:** Biến đầu vào `$_POST['username']` và `$_POST['password']` được gán trực tiếp vào chuỗi câu lệnh SQL không qua bất kỳ hàm lọc, kiểm tra định dạng hay escape nào.
- **Cơ chế kiểm soát đã kiểm tra:** Không có Prepared Statements, không có `mysql_real_escape_string()`, không có validation.
- **Phân loại CWE:** `CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')`.
- **Tác động an toàn:** Kẻ tấn công không cần tài khoản hợp lệ, chỉ cần nhập chuỗi payload (ví dụ `admin' -- ` hoặc `' OR '1'='1`) để đăng nhập thành công với quyền thủ thư cao nhất của hệ thống.
- **Điều kiện tiên quyết:** Endpoint `login.php` mở công khai cho người dùng truy cập.
- **Mức độ & Lý do:** `CRITICAL`. Lỗ hổng cho phép chiếm quyền quản trị toàn bộ ứng dụng ngay tại cổng vào xác thực với độ phức tạp tấn công cực thấp.
- **Độ tin cậy:** `HIGH` (Bằng chứng tĩnh hiển nhiên qua luồng dữ liệu).
- **Trạng thái thẩm định:** `confirmed-static`.
- **Hướng khắc phục:** Chuyển sang sử dụng PDO / MySQLi với Prepared Statements và tham số hóa câu truy vấn:
  ```php
  $stmt = $pdo->prepare("SELECT user_id, password FROM users WHERE username = :username");
  $stmt->execute(['username' => $username]);
  $user = $stmt->fetch();
  ```
- **Giới hạn phân tích tĩnh:** Không cần kiểm thử động vẫn chứng minh được lỗ hổng do câu truy vấn không có bất kỳ lớp cản nào.

---

### FIND-02: Thiếu Kiểm soát Xác thực Phiên tại các Endpoint Thay đổi Trạng thái và Dữ liệu (Broken Access Control)

- **Mã định danh:** `FIND-02`
- **Nguồn phát hiện:** Rà soát thủ công (Checklist `AC-02`) đối chiếu sơ đồ Include.
- **Commit khảo sát:** `082d6fb9bdd7846b57033513791ba5b6d2095c11`.
- **Tệp và dòng mã:**
  - `delete_user.php` (dòng 1 - 9)
  - `delete_books.php` (dòng 1 - 6)
  - `delete_member.php` / `delete_student.php` (dòng 1 - 6)
  - `books_save.php` (dòng 1 - 25)
  - `member_save.php` / `student_save.php` (dòng 1 - 20)
  - `borrow_save.php` (dòng 1 - 28)
  - `return_save.php` (dòng 1 - 9)
  - `update_books.php` (dòng 1 - 26)
  - `update_member.php` / `update_students.php` (dòng 1 - 19)
- **Đoạn trích mã nguồn (`delete_user.php:1-8`):**
  ```php
  <?php
  include('dbcon.php');
  $id=$_GET['id'];
  mysql_query("delete from users where user_id='$id'") or die(mysql_error());
  header('location:users.php');
  ?>
  ```
- **Mô tả luồng dữ liệu / Ngữ cảnh:** Trong khi các trang giao diện (`dashboard.php`, `users.php`) có `include('session.php')`, tất cả các tệp thực thi hành động nhạy cảm (Xóa user, Xóa sách, Xóa thành viên, Thêm sách, Thêm thành viên, Mượn sách, Trả sách) hoàn toàn **không include `session.php`**.
- **Cơ chế kiểm soát đã kiểm tra:** Không gọi `session_start()`, không kiểm tra `$_SESSION['id']`, không kiểm tra quyền người dùng.
- **Phân loại CWE:** `CWE-306: Missing Authentication for Critical Function` & `CWE-284: Improper Access Control`.
- **Tác động an toàn:** Kẻ tấn công trái phép trên mạng không cần đăng nhập vẫn có thể gọi trực tiếp URL (hoặc gửi HTTP POST/GET) để xóa sạch tài khoản thủ thư, thêm/sửa/xóa sách, và tạo các giao dịch mượn/trả sách tùy ý.
- **Điều kiện tiên quyết:** Kẻ tấn công biết hoặc đoán được đường dẫn tương đối của các endpoint này.
- **Mức độ & Lý do:** `CRITICAL`. Phá vỡ hoàn toàn ranh giới bảo vệ của hệ thống quản trị nội bộ.
- **Độ tin cậy:** `HIGH` (Kiểm tra tệp tin cho thấy 100% không có include session).
- **Trạng thái thẩm định:** `confirmed-static`.
- **Hướng khắc phục:** Bắt buộc include tệp kiểm tra phiên ở đầu tất cả các tệp xử lý:
  ```php
  require_once('session.php');
  ```
- **Giới hạn phân tích tĩnh:** Khẳng định tĩnh chắc chắn vì mã nguồn độc lập của các tệp này không chứa cơ chế xác thực.

---

### FIND-03: SQL Injection Diện rộng tại Toàn bộ các Chức năng CRUD Sách, Độc giả và Giao dịch

- **Mã định danh:** `FIND-03`
- **Nguồn phát hiện:** Semgrep (`php.lang.security.injection.tainted-sql-string`, `study.rules.php-direct-mysql-query-taint` - 80 cảnh báo) & Rà soát thủ công (`INP-01`, `INP-02`, `INP-03`).
- **Commit khảo sát:** `082d6fb9bdd7846b57033513791ba5b6d2095c11`.
- **Tệp và dòng mã tiêu biểu:**
  - `advance_search.php` (dòng 58 - 59)
  - `books_save.php` (dòng 20 - 21)
  - `update_books.php` (dòng 20 - 21)
  - `delete_books.php` (dòng 4)
  - `member_save.php` (dòng 15)
  - `update_member.php` (dòng 14)
  - `borrow_save.php` (dòng 16, 23)
  - `return_save.php` (dòng 7)
  - `modal_add_user.php` (dòng 50)
  - `modal_edit_user.php` (dòng 55)
- **Đoạn trích mã nguồn (`advance_search.php:58-59`):**
  ```php
  $user_query=mysql_query("select * from book where status != 'Archive' and book_title LIKE '%$title%'
  OR status != 'Archive' and author LIKE '%$author%'")or die(mysql_error());
  ```
- **Đoạn trích mã nguồn (`borrow_save.php:16,23`):**
  ```php
  mysql_query("insert into borrow (member_id,date_borrow,due_date) values ('$member_id',NOW(),'$due_date')")or die(mysql_error());
  mysql_query("insert borrowdetails (book_id,borrow_id,borrow_status) values('$id[$i]','$borrow_id','pending')")or die(mysql_error());
  ```
- **Mô tả luồng dữ liệu / Ngữ cảnh:** Toàn bộ tham số nhận từ `$_POST` và `$_GET` được nối trực tiếp bằng dấu nháy đơn vào câu lệnh `mysql_query(...)`. Không có bất kỳ trường số nào (như `book_id`, `member_id`, `category_id`) được ép kiểu `intval()`.
- **Cơ chế kiểm soát đã kiểm tra:** Không có Prepared Statements, không có whitelist validation, không có escaping.
- **Phân loại CWE:** `CWE-89: Improper Neutralization of Special Elements used in an SQL Command`.
- **Tác động an toàn:** Trích xuất toàn bộ dữ liệu CSDL (thông tin người dùng, mật khẩu), sửa đổi hoặc phá hủy cấu trúc dữ liệu qua kỹ thuật Stacked Queries / Union-based SQL Injection.
- **Điều kiện tiên quyết:** Gửi yêu cầu HTTP POST/GET với payload độc hại.
- **Mức độ & Lý do:** `HIGH`. Mức độ phủ sóng lỗi 100% các câu truy vấn có biến số trong phân hệ.
- **Độ tin cậy:** `HIGH`.
- **Trạng thái thẩm định:** `confirmed-static`.
- **Hướng khắc phục:** Áp dụng Prepared Statements đồng bộ trên toàn bộ phân hệ; ép kiểu chặt chẽ các khóa số (`(int)$_POST['id']`).
- **Giới hạn phân tích tĩnh:** Tĩnh đã chứng minh đủ cấu trúc ghép chuỗi không an toàn.

---

### FIND-04: Lỗ hổng Cross-Site Scripting (Stored & Reflected XSS) do Xuất Dữ liệu Động Thiếu Thoát Ký tự

- **Mã định danh:** `FIND-04`
- **Nguồn phát hiện:** Semgrep (`php.lang.security.injection.echoed-request.echoed-request`) & Rà soát thủ công (`OUT-01`, `OUT-02`).
- **Commit khảo sát:** `082d6fb9bdd7846b57033513791ba5b6d2095c11`.
- **Tệp và dòng mã tiêu biểu:**
  - `books.php`, `advance_search.php` (dòng 77 - 87)
  - `member.php` (dòng 52 - 62)
  - `users.php` (dòng 46 - 50)
  - `view_borrow.php` (dòng 66 - 74)
  - `edit_book.php` (dòng 45 - 90)
  - `edit_member.php` (dòng 30 - 75)
- **Đoạn trích mã nguồn (`advance_search.php:78,80`):**
  ```php
  <td><?php echo $row['book_title']; ?></td>
  <td><?php echo $row['author']; ?> </td>
  ```
- **Đoạn trích mã nguồn (`edit_book.php:48`):**
  ```php
  <input type="text" class="span4" id="inputEmail" name="book_title" value="<?php echo $row['book_title']; ?>" placeholder="book_title" required>
  ```
- **Mô tả luồng dữ liệu / Ngữ cảnh:** Dữ liệu chuỗi từ CSDL (đã bị nhiễm từ form thêm sách/thành viên hoặc từ đầu vào) được in thẳng ra cấu trúc DOM HTML hoặc giá trị thuộc tính `value="..."` mà không thông qua hàm mã hóa thực thể HTML.
- **Cơ chế kiểm soát đã kiểm tra:** Không sử dụng `htmlspecialchars()` hay `htmlentities()`.
- **Phân loại CWE:** `CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')`.
- **Tác động an toàn:** Cho phép kẻ tấn công chèn mã JavaScript độc hại vào cơ sở dữ liệu (Stored XSS). Khi thủ thư mở trang danh sách, script tự động thực thi với phiên của thủ thư (đánh cắp cookie, giả mạo thao tác xóa hệ thống).
- **Điều kiện tiên quyết:** Kẻ tấn công tạo bản ghi chứa payload XSS (thông qua form thêm sách/thành viên không được kiểm tra phiên ở FIND-02).
- **Mức độ & Lý do:** `HIGH`. Dễ khai thác kết hợp với FIND-02 để tấn công người quản trị.
- **Độ tin cậy:** `HIGH`.
- **Trạng thái thẩm định:** `confirmed-static`.
- **Hướng khắc phục:** Áp dụng hàm `htmlspecialchars($data, ENT_QUOTES, 'UTF-8')` cho mọi biến xuất ra trang HTML.
- **Giới hạn phân tích tĩnh:** Tĩnh đã chỉ ra điểm thiếu hàm thoát ký tự tại mọi thẻ xuất dữ liệu.

---

### FIND-05: Lưu trữ và Hiển thị Mật khẩu Dạng Bản rõ (Plaintext Password Storage and Exposure)

- **Mã định danh:** `FIND-05`
- **Nguồn phát hiện:** Rà soát thủ công (`AUTH-02`, `ERR-03`) đối chiếu `db/eb_lms.sql` và mã nguồn PHP.
- **Commit khảo sát:** `082d6fb9bdd7846b57033513791ba5b6d2095c11`.
- **Tệp và dòng mã:**
  - `login.php` (dòng 6)
  - `modal_add_user.php` (dòng 50)
  - `modal_edit_user.php` (dòng 18, 55)
  - `unstudents.php` (dòng 17, 34)
  - `study/source/db/eb_lms.sql` (bảng `users` và `students`)
- **Đoạn trích mã nguồn (`modal_edit_user.php:18`):**
  ```php
  <input type="text" name="password" id="inputPassword" value="<?php echo $row['password']; ?>" required>
  ```
- **Đoạn trích mã nguồn (`unstudents.php:17,34`):**
  ```php
  <th>Password</th>
  ...
  <td><?php echo $row['password']; ?></td>
  ```
- **Mô tả luồng dữ liệu / Ngữ cảnh:** Mật khẩu người dùng được lưu trữ nguyên văn (plaintext) không qua băm (hashing). Khi chỉnh sửa thông tin thủ thư, mật khẩu hiện tại được in trực tiếp vào thẻ input HTML. Tại trang danh sách sinh viên chưa xác nhận (`unstudents.php`), mật khẩu thậm chí được hiển thị công khai trên một cột của bảng.
- **Cơ chế kiểm soát đã kiểm tra:** Không sử dụng `password_hash()`, `bcrypt` hay bất kỳ thuật toán băm nào.
- **Phân loại CWE:** `CWE-256: Unprotected Storage of Credentials` & `CWE-312: Cleartext Storage of Sensitive Information`.
- **Tác động an toàn:** Bất kỳ ai có quyền đọc CSDL hoặc nhìn vào màn hình thủ thư đều có thể thu thập toàn bộ mật khẩu người dùng mà không cần bẻ khóa.
- **Điều kiện tiên quyết:** Truy cập giao diện hoặc trích xuất CSDL qua SQLi.
- **Mức độ & Lý do:** `HIGH`. Vi phạm nghiêm trọng tiêu chuẩn bảo mật dữ liệu định danh.
- **Độ tin cậy:** `HIGH`.
- **Trạng thái thẩm định:** `confirmed-static`.
- **Hướng khắc phục:** Sử dụng hàm băm mật khẩu chuẩn của PHP (`password_hash($password, PASSWORD_BCRYPT)`) và so sánh bằng `password_verify()`; không bao giờ hiển thị lại mật khẩu trên giao diện form.
- **Giới hạn phân tích tĩnh:** Đọc mã và SQL script chứng minh mật khẩu dạng plain text 100%.

---

### FIND-06: Thao tác Thay đổi Trạng thái Qua Phương thức GET và Thiếu Cơ chế Chống Giả mạo Yêu cầu (State Change via GET & Missing CSRF Protection)

- **Mã định danh:** `FIND-06`
- **Nguồn phát hiện:** Rà soát thủ công (`STATE-01`, `STATE-02`, `STATE-03`).
- **Commit khảo sát:** `082d6fb9bdd7846b57033513791ba5b6d2095c11`.
- **Tệp và dòng mã:**
  - `delete_user.php` (dòng 4)
  - `delete_books.php` (dòng 3)
  - `delete_member.php` (dòng 3)
  - `return_save.php` (dòng 4 - 5)
  - Toàn bộ các biểu mẫu trong `librarian/*.php`
- **Đoạn trích mã nguồn (`delete_books.php:3-4`):**
  ```php
  $id=$_GET['id'];
  mysql_query("update book set status = 'Archive' where book_id='$id'")or die(mysql_error());
  ```
- **Mô tả luồng dữ liệu / Ngữ cảnh:** Các hành động xóa và đổi trạng thái sử dụng HTTP GET. Toàn bộ các form thêm/sửa dữ liệu sử dụng HTTP POST nhưng không có bất kỳ trường token chống CSRF nào.
- **Cơ chế kiểm soát đã kiểm tra:** Không có CSRF Token (`$_SESSION['csrf_token']`), không kiểm tra HTTP Referer/Origin header.
- **Phân loại CWE:** `CWE-352: Cross-Site Request Forgery ('CSRF')`.
- **Tác động an toàn:** Kẻ tấn công có thể nhúng thẻ `<img src="http://target/librarian/delete_user.php?id=1">` vào trang web bất kỳ. Khi thủ thư đang đăng nhập vô tình ghé thăm trang web đó, trình duyệt tự động gửi yêu cầu xóa tài khoản thủ thư hoặc sách mà thủ thư không hề hay biết.
- **Điều kiện tiên quyết:** Nạn nhân (thủ thư) có phiên đăng nhập hợp lệ và bị lừa truy cập liên kết của kẻ tấn công.
- **Mức độ & Lý do:** `HIGH`. Dễ kích hoạt thông qua thẻ HTML vô hại hoặc tin nhắn lừa đảo.
- **Độ tin cậy:** `HIGH`.
- **Trạng thái thẩm định:** `confirmed-static`.
- **Hướng khắc phục:** Chuyển toàn bộ thao tác thay đổi dữ liệu sang phương thức HTTP POST; sinh và kiểm tra Anti-CSRF token ngẫu nhiên cho mỗi phiên làm việc.
- **Giới hạn phân tích tĩnh:** Tĩnh đã kiểm tra toàn bộ form không có trường token.

---

### FIND-07: Điều kiện Cạnh tranh và Thiếu Tính Toàn tử (Non-Atomic Multi-table Inserts & Race Condition) trong Luồng Mượn Sách

- **Mã định danh:** `FIND-07`
- **Nguồn phát hiện:** Rà soát thủ công (`BIZ-03`, `Checklist`).
- **Commit khảo sát:** `082d6fb9bdd7846b57033513791ba5b6d2095c11`.
- **Tệp và dòng mã:** `study/source/librarian/borrow_save.php` (dòng 16 - 25).
- **Đoạn trích mã nguồn:**
  ```php
  mysql_query("insert into borrow (member_id,date_borrow,due_date) values ('$member_id',NOW(),'$due_date')")or die(mysql_error());
  $query = mysql_query("select * from borrow order by borrow_id DESC")or die(mysql_error());
  $row = mysql_fetch_array($query);
  $borrow_id = $row['borrow_id'];
  $N = count($id);
  for($i=0; $i < $N; $i++) {
      mysql_query("insert borrowdetails (book_id,borrow_id,borrow_status) values('$id[$i]','$borrow_id','pending')")or die(mysql_error());
  }
  ```
- **Mô tả luồng dữ liệu / Ngữ cảnh:** Mã nguồn lấy khóa chính vừa chèn bằng cách truy vấn `SELECT * FROM borrow ORDER BY borrow_id DESC`. Đồng thời, các thao tác chèn nhiều dòng vào `borrowdetails` không được bọc trong một Database Transaction (ACID).
- **Cơ chế kiểm soát đã kiểm tra:** Không sử dụng `mysql_insert_id()`, không có `START TRANSACTION` / `COMMIT`.
- **Phân loại CWE:** `CWE-362: Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')`.
- **Tác động an toàn:** Trong môi trường có nhiều thủ thư cùng tạo phiếu mượn đồng thời, thủ thư A có thể ghi nhầm danh sách sách của mình vào `borrow_id` của thủ thư B. Nếu vòng lặp chèn chi tiết bị ngắt giữa chừng, cơ sở dữ liệu sẽ tồn tại các bản ghi mồ côi (orphaned rows) làm sai lệch số liệu quản lý kho sách.
- **Điều kiện tiên quyết:** Có hai hoặc nhiều giao dịch mượn sách diễn ra đồng thời.
- **Mức độ & Lý do:** `MEDIUM`. Lỗi thiết kế nghiệp vụ gây sai lệch toàn vẹn dữ liệu nghiêm trọng khi tải tăng.
- **Độ tin cậy:** `HIGH`.
- **Trạng thái thẩm định:** `confirmed-static`.
- **Hướng khắc phục:** Sử dụng hàm lấy ID chèn trực tiếp của kết nối (`$pdo->lastInsertId()`) và đưa toàn bộ quy trình mượn sách vào Database Transaction:
  ```php
  $pdo->beginTransaction();
  // insert borrow...
  $borrow_id = $pdo->lastInsertId();
  // insert borrowdetails in loop...
  $pdo->commit();
  ```
- **Giới hạn phân tích tĩnh:** Tĩnh đã chứng minh cơ chế truy vấn DESC là không an toàn đối với concurrency.

---

### FIND-08: Lưu trữ Cố định Thông tin Kết nối Cơ sở Dữ liệu trong Mã nguồn (Hardcoded Database Credentials)

- **Mã định danh:** `FIND-08`
- **Nguồn phát hiện:** Semgrep (`study.rules.php-hardcoded-db-credentials`) & Rà soát thủ công (`ERR-03`).
- **Commit khảo sát:** `082d6fb9bdd7846b57033513791ba5b6d2095c11`.
- **Tệp và dòng mã:** `study/source/librarian/dbcon.php` (dòng 2).
- **Đoạn trích mã nguồn:**
  ```php
  mysql_select_db('eb_lms',mysql_connect('localhost','root',''))or die(mysql_error());
  ```
- **Mô tả luồng dữ liệu / Ngữ cảnh:** Tệp cấu hình kết nối CSDL hardcode trực tiếp tài khoản quản trị mặc định `root` với mật khẩu rỗng và tên CSDL `eb_lms`.
- **Cơ chế kiểm soát đã kiểm tra:** Không sử dụng biến môi trường (Environment Variables) hoặc tệp cấu hình `.env` tách biệt nằm ngoài web root.
- **Phân loại CWE:** `CWE-798: Use of Hard-coded Credentials`.
- **Tác động an toàn:** Nếu máy chủ gặp sự cố cấu hình web server không thực thi PHP mà trả về mã nguồn thô (source code leakage) hoặc tệp được lưu trên kho lưu trữ công khai, thông tin truy cập CSDL bị lộ ngay lập tức.
- **Điều kiện tiên quyết:** Đọc được tệp `dbcon.php`.
- **Mức độ & Lý do:** `MEDIUM`. Rủi ro cấu hình và an toàn triển khai.
- **Độ tin cậy:** `HIGH`.
- **Trạng thái thẩm định:** `confirmed-static`.
- **Hướng khắc phục:** Tách thông số kết nối vào biến môi trường hệ thống hoặc tệp cấu hình `.env` được bảo vệ ngoài thư mục web công cộng.
- **Giới hạn phân tích tĩnh:** Bằng chứng tĩnh hiển nhiên.

---

### FIND-09: Sử dụng Phần Mở rộng Cơ sở Dữ liệu Lỗi thời và Đã Bị Loại bỏ (`ext/mysql`)

- **Mã định danh:** `FIND-09`
- **Nguồn phát hiện:** Semgrep (`study.rules.php-legacy-mysql-extension` - 147 cảnh báo) & PHPStan (Fatal error missing functions).
- **Commit khảo sát:** `082d6fb9bdd7846b57033513791ba5b6d2095c11`.
- **Tệp và dòng mã tiêu biểu:** Xuất hiện tại 38 tệp mã nguồn PHP trong phân hệ thủ thư (`dbcon.php`, `login.php`, `books.php`, `member.php`, `borrow_save.php`...).
- **Đoạn trích mã nguồn:**
  Các hàm: `mysql_connect()`, `mysql_select_db()`, `mysql_query()`, `mysql_fetch_array()`, `mysql_num_rows()`, `mysql_error()`.
- **Mô tả luồng dữ liệu / Ngữ cảnh:** Ứng dụng phụ thuộc hoàn toàn vào driver `ext/mysql` nguyên thủy của PHP. Thư viện này đã bị đánh dấu deprecated từ PHP 5.5 (2013) và bị loại bỏ hoàn toàn khỏi lõi PHP từ phiên bản PHP 7.0 (2015).
- **Phân loại CWE:** `CWE-477: Use of Deprecated Function`.
- **Tác động an toàn & Vận hành:** Ứng dụng hoàn toàn không thể chạy trên các phiên bản PHP hiện đại (PHP 7.x, PHP 8.x) nếu không sửa mã. Driver cũ này không hỗ trợ Prepared Statements, khuyến khích lập trình viên sử dụng kỹ thuật nối chuỗi kém an toàn.
- **Điều kiện tiên quyết:** Triển khai trên môi trường máy chủ PHP chuẩn hiện hành.
- **Mức độ & Lý do:** `MEDIUM`. Nợ kỹ thuật lớn cản trở việc vá lỗi và vận hành an toàn.
- **Độ tin cậy:** `HIGH`.
- **Trạng thái thẩm định:** `confirmed-static`.
- **Hướng khắc phục:** Nâng cấp toàn bộ tầng truy cập dữ liệu sang PDO (PHP Data Objects) hoặc MySQLi.
- **Giới hạn phân tích tĩnh:** Kiểm tra tĩnh xác nhận 100% các hàm gọi là `mysql_*`.

---

### FIND-10: Tiết lộ Thông tin Chi tiết Cấu trúc Cơ sở Dữ liệu qua Thông báo Lỗi (`mysql_error()`)

- **Mã định danh:** `FIND-10`
- **Nguồn phát hiện:** Semgrep & Rà soát thủ công (`ERR-01`).
- **Commit khảo sát:** `082d6fb9bdd7846b57033513791ba5b6d2095c11`.
- **Tệp và dòng mã tiêu biểu:** Hầu như toàn bộ các tệp thực thi truy vấn đều chứa `or die(mysql_error())` (ví dụ `login.php:7`, `books_save.php:21`, `advance_search.php:59`...).
- **Đoạn trích mã nguồn:**
  ```php
  $result = mysql_query($query)or die(mysql_error());
  ```
- **Mô tả luồng dữ liệu / Ngữ cảnh:** Khi câu truy vấn SQL gặp lỗi cú pháp (hoặc do payload SQLi đưa vào gây lỗi), hàm `mysql_error()` in trực tiếp thông báo lỗi chi tiết của MySQL ra màn hình người dùng.
- **Cơ chế kiểm soát đã kiểm tra:** Không có try/catch, không có hàm xử lý lỗi tập trung, không tắt `display_errors`.
- **Phân loại CWE:** `CWE-209: Generation of Error Message Containing Sensitive Information`.
- **Tác động an toàn:** Giúp kẻ tấn công thu thập cấu trúc bảng, tên cột và phiên bản CSDL một cách nhanh chóng để tinh chỉnh payload tấn công SQL Injection.
- **Điều kiện tiên quyết:** Kích hoạt truy vấn SQL lỗi.
- **Mức độ & Lý do:** `LOW`. Lỗ hổng hỗ trợ trinh sát (reconnaissance).
- **Độ tin cậy:** `HIGH`.
- **Trạng thái thẩm định:** `confirmed-static`.
- **Hướng khắc phục:** Bắt ngoại lệ và ghi log lỗi vào tệp log an toàn trên server; chỉ hiển thị thông báo lỗi chung chung, thân thiện cho người dùng.
- **Giới hạn phân tích tĩnh:** Bằng chứng hiển thị rõ trong mã nguồn.

---

### FIND-11: Liên kết Tệp Include Bị Gãy, Truy vấn Bảng Không Tồn tại và Tệp Rỗng (Structural Code Defects)

- **Mã định danh:** `FIND-11`
- **Nguồn phát hiện:** PHPStan (`include.fileNotFound`) & Rà soát cấu trúc mã nguồn thủ công.
- **Commit khảo sát:** `082d6fb9bdd7846b57033513791ba5b6d2095c11`.
- **Tệp và dòng mã:**
  - `archive.php` (dòng 3): `include('navbar_archive.php');` -> Tệp không tồn tại.
  - `unstudents.php` (dòng 3): `include('navbar_dasboard.php');` -> Sai chính tả (`navbar_dashboard.php`).
  - `unstudents.php` (dòng 72): `include('confirm_request.php');` -> Tệp không tồn tại.
  - `unstudents.php` (dòng 29): `SELECT * FROM students` -> Bảng `students` không tồn tại trong `eb_lms.sql`.
  - `unreturned_books.php`: Kích thước 0 bytes (tệp rỗng hoàn toàn).
- **Mô tả luồng dữ liệu / Ngữ cảnh:** Lỗi lập trình và mã nguồn rác chưa được dọn dẹp khi tác giả sao chép từ dự án khác hoặc sửa dở dang.
- **Phân loại CWE:** `CWE-398: Indicator of Poor Code Quality` & `CWE-703: Improper Check or Handling of Exceptional Conditions`.
- **Tác động an toàn & Vận hành:** Khi người dùng truy cập các trang này, ứng dụng sẽ sinh cảnh báo PHP Warning (làm lộ đường dẫn máy chủ) hoặc sập trang hoàn toàn khi truy vấn bảng không tồn tại.
- **Mức độ & Lý do:** `LOW`. Vấn đề chất lượng mã nguồn và bảo trì.
- **Độ tin cậy:** `HIGH`.
- **Trạng thái thẩm định:** `confirmed-static`.
- **Hướng khắc phục:** Sửa chính tả tệp include, loại bỏ mã thừa hoặc cập nhật định nghĩa CSDL đồng bộ.
- **Giới hạn phân tích tĩnh:** Kiểm tra tĩnh xác nhận chắc chắn sự thiếu vắng của các tệp và bảng này.

---

## 3. Phân tích Cảnh báo Giả Tiêu biểu (`false-positive`)

### FP-01: Semgrep Cảnh báo Echoed-Request trên Khóa Chính Số CSDL tại `advance_search.php`

- **Mã định danh:** `FP-01`
- **Nguồn cảnh báo gốc:** Semgrep rule `php.lang.security.injection.echoed-request.echoed-request`.
- **Vị trí cảnh báo:** `study/source/librarian/advance_search.php` dòng 76 (`<tr class="del<?php echo $id ?>">`).
- **Lý do công cụ tự động cảnh báo:** Tại đầu tệp `advance_search.php`, có dòng `$title = $_POST['title'];`. Bộ phân tích tĩnh của Semgrep đánh dấu biến môi trường bị tainted và suy diễn rằng các biến in ra HTML phía dưới (`$id`) có thể bắt nguồn từ request của người dùng.
- **Kết quả đối chiếu và thẩm định ngữ cảnh:**
  - Đọc kỹ mã nguồn tại dòng 60 - 61:
    ```php
    while($row=mysql_fetch_array($user_query)){
    $id=$row['book_id'];
    ...
    <tr class="del<?php echo $id ?>">
    ```
  - Biến `$id` hoàn toàn được gán từ trường `book_id` (kiểu dữ liệu số `int(11) AUTO_INCREMENT`) của bảng `book` trong cơ sở dữ liệu `eb_lms.sql`.
  - Đây **không phải là Reflected XSS** từ tham số request của người dùng.
- **Kết luận thẩm định:** Gán trạng thái **`false-positive`** đối với cảnh báo cụ thể này của Semgrep.
- **Ý nghĩa phương pháp luận:** Kết quả này chứng minh sự cần thiết bắt buộc của việc kết hợp rà soát ngữ cảnh thủ công với công cụ quét tự động; không thể đánh đồng số lượng cảnh báo thô từ máy quét với số lượng lỗ hổng thực tế.

---

## 4. Mục Nghiệp vụ Chưa đủ Căn cứ Đặc tả (`inconclusive`)

### BIZ-INC-01: Kiểm tra Giới hạn Mượn và Ràng buộc Số lượng Bản sao Khả dụng

- **Mã định danh:** `BIZ-INC-01`
- **Nội dung:**
  - Trong `borrow_save.php`, hệ thống không kiểm tra số lượng sách khả dụng (`book_copies - pending > 0`) trước khi cho mượn và không giới hạn số sách tối đa một độc giả được phép mượn.
  - Đồng thời, trạng thái tài khoản thành viên (`member.status`) không được kiểm tra trong luồng mượn sách.
- **Đánh giá thẩm định:**
  - Dự án upstream không cung cấp tài liệu đặc tả yêu cầu (SRS) hay quy chế thư viện chính thức.
  - Về mặt kỹ thuật, việc cho phép mượn sách mà không kiểm tra số lượng tồn kho có thể là một thiếu sót kiểm soát nghiệp vụ (Business Logic Flaw). Tuy nhiên, vì không có đặc tả quy định rõ hành vi kỳ vọng của hệ thống, nhóm nghiên cứu không tự ý kết luận đây là vi phạm yêu cầu an toàn phần mềm.
- **Kết luận thẩm định:** Gán trạng thái **`inconclusive`** (Ghi nhận dưới dạng giả định nghiệp vụ chưa có ràng buộc, cần nhà phát triển hoặc chủ sở hữu sản phẩm xác nhận).
