## Why

Học phần An toàn phần mềm cần một nghiên cứu kiểm thử tĩnh có phạm vi vừa sức, bằng chứng truy xuất được và kết quả được thẩm định. Phân hệ thủ thư của một hệ thống thư viện PHP có sẵn cho phép tập trung vào đọc mã và phân tích tự động thay vì xây dựng ứng dụng mới.

## What Changes

- Tên đề tài: **Áp dụng kiểm thử tĩnh để đánh giá mã nguồn phân hệ thủ thư của hệ thống quản lý thư viện PHP**.
- Chọn repository https://github.com/vinitshahdeo/Library-Management-System tại commit `082d6fb9bdd7846b57033513791ba5b6d2095c11` làm baseline khảo sát.
- Lập danh mục mã và checklist cho đăng nhập/phiên làm việc, quản lý sách, thành viên và mượn–trả trong `librarian/`; tham chiếu `db/eb_lms.sql` khi cần hiểu dữ liệu.
- Kết hợp rà soát thủ công với phân tích tự động; chọn công cụ sau khi xác minh khả năng xử lý mã PHP của baseline.
- Lập sổ phát hiện phân biệt cảnh báo chưa xác minh, lỗi được xác nhận, cảnh báo giả và trường hợp chưa đủ bằng chứng.
- Viết báo cáo gồm cơ sở lý thuyết, đối tượng và phạm vi, phương pháp, kết quả, hướng khắc phục và giới hạn.
- Không xây dựng tính năng, không sửa baseline, không kiểm thử khai thác trên dịch vụ công khai; sửa lỗi hoặc chạy thử ứng dụng là phạm vi bổ sung cần thống nhất riêng.

## Capabilities

### New Capabilities

Không bổ sung hành vi sản phẩm. Đây là nghiên cứu và tài liệu học phần; dùng `skip_specs: true`, không tạo yêu cầu chức năng giả cho ứng dụng thư viện.

### Modified Capabilities

Không thay đổi yêu cầu hiện có của ứng dụng.

## Impact

- Sản phẩm dự kiến: manifest baseline, danh mục phạm vi, checklist, hồ sơ công cụ/cấu hình, kết quả thô, sổ phát hiện và báo cáo Markdown trong `study/`.
- Loại khỏi phạm vi chính: bản sao `library/`, ZIP, `librarian/vendors/`, tài sản giao diện tĩnh, tài liệu upstream và các luồng độc giả ở thư mục gốc. Loại khỏi khảo sát không có nghĩa đã an toàn.
- Giữ nguồn gốc và giấy phép MIT khi lưu bản sao mã; chỉ dùng dữ liệu giả nếu cần minh họa.
- Không có thay đổi API, cơ sở dữ liệu đang chạy hoặc triển khai. Không đặt chỉ tiêu phải tìm được một số lượng lỗ hổng cố định.
