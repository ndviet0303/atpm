# Baseline Khảo sát Mã nguồn

## 1. Thông tin Kho lưu trữ và Commit

- **Tên dự án gốc:** Library-Management-System (Upstream)
- **Tác giả upstream:** Vinit Shahdeo
- **Kho lưu trữ (Repository URL):** `https://github.com/vinitshahdeo/Library-Management-System`
- **Commit chốt:** `082d6fb9bdd7846b57033513791ba5b6d2095c11`
- **Tên nhánh/trạng thái:** detached HEAD tại commit `082d6fb9bdd7846b57033513791ba5b6d2095c11`
- **Thông điệp commit:** `added social icons`
- **Thời điểm commit gốc:** `2020-02-12 17:21:32 +0530`

## 2. Thời điểm và Phương thức Lấy mã

- **Thời điểm lấy (Timestamp):** `2026-09-10T02:40:00Z`
- **Phương thức lấy mã:**
  1. Sử dụng lệnh Git chính thức để sao chép kho từ GitHub:
     ```bash
     git clone https://github.com/vinitshahdeo/Library-Management-System.git study/tmp_repo
     cd study/tmp_repo
     git checkout 082d6fb9bdd7846b57033513791ba5b6d2095c11
     ```
  2. Loại bỏ thư mục nội bộ `.git/` của repo tạm và chuyển toàn bộ cây mã nguồn nguyên vẹn sang vị trí cố định của nghiên cứu tại `study/source/`:
     ```bash
     rm -rf study/tmp_repo/.git
     mv study/tmp_repo study/source
     ```
  3. Bảo toàn nguyên vẹn tệp bản quyền `LICENSE` (giấy phép MIT của tác giả Vinit Shahdeo) tại `study/source/LICENSE`.

## 3. Mã băm Kiểm tra Toàn vẹn (Checksums)

- **Git Archive TAR SHA-256:**
  `fabac8fc61e74d2124eeb31a82d73acc8d0234a57ffdd57b54af3184b37293c7`
- **LICENSE SHA-256 (`study/source/LICENSE`):**
  `2e21d291d98be3562c6c122c35e9e624ef31950db4fdfbd95a5aa5b23ce192c0`
- **Database Schema Script SHA-256 (`study/source/db/eb_lms.sql`):**
  `1d2817e54dfc20d81e169e8080a05f4bc805711e8676359ee69f6d67f20ce8d4`
- **Toàn vẹn tệp PHP trong phạm vi phân hệ thủ thư (`study/source/librarian/`):**
  Danh sách SHA-256 chi tiết của từng tệp mã PHP tự viết trong phân hệ thủ thư được lưu trữ đồng bộ trong `study/scope.md` để hỗ trợ kiểm tra đối sánh tái lập bất biến.

## 4. Nguyên tắc An toàn và Phạm vi Thực thi

1. **Tuyệt đối không thực thi ứng dụng upstream:** Không khởi chạy web server (Apache/Nginx/PHP built-in server), không kết nối tới cơ sở dữ liệu MySQL/MariaDB trực tiếp, không gọi script với dữ liệu thực tế từ môi trường mạng hoặc trình duyệt.
2. **Thuần túy phân tích tĩnh và đọc mã:** Mọi hoạt động nghiên cứu chỉ dựa trên việc đọc mã tĩnh, phân tích cú pháp tĩnh, phân tích luồng dữ liệu tĩnh và đối chiếu mô hình cấu trúc bảng từ tệp định nghĩa SQL đi kèm.
3. **Bảo tồn bản quyền:** Toàn bộ mã nguồn nghiên cứu tuân thủ giấy phép MIT gốc; không phân phối lại dưới dạng sản phẩm thương mại và chỉ phục vụ mục đích học thuật của học phần An toàn phần mềm.
