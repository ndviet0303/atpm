## 1. Chuẩn bị baseline và phạm vi

- [x] 1.1 Lấy bản sao đúng commit đã chốt vào `study/source/`, giữ LICENSE; ghi nguồn, thời điểm, cách lấy và checksum trong `study/baseline.md`, không chạy ứng dụng upstream.
- [x] 1.2 Kiểm kê PHP trong `librarian/`, loại `vendors/` và bản sao; lưu danh mục tệp, số tệp, phương pháp đo số dòng và các loại trừ trong `study/scope.md`.
- [x] 1.3 Lập sơ đồ các trang xử lý, include và bảng dữ liệu liên quan đến bốn nhóm chức năng; ghi các phụ thuộc hỗ trợ và điểm chưa rõ trong `study/scope.md`.

## 2. Chuẩn hóa phương pháp và chọn công cụ

- [x] 2.1 Tạo `study/checklist.md` bao phủ xác thực/phiên, quyền truy cập, đầu vào/truy vấn, đầu ra, thao tác đổi trạng thái, xử lý lỗi và toàn vẹn nghiệp vụ; đánh dấu giả định chưa có đặc tả.
- [x] 2.2 Tra cứu tài liệu chính thức hiện hành để lập danh sách ngắn công cụ phân tích tĩnh PHP chạy cục bộ; ghi khả năng, giới hạn và tiêu chí lựa chọn trong `study/tooling.md`.
- [x] 2.3 Thử khả năng phân tích một tập tệp nhỏ của baseline mà không sửa nguồn; chọn công cụ và ghi phiên bản, quy tắc, cấu hình, lệnh, lỗi cú pháp hoặc giới hạn quan sát được.
- [x] 2.4 Tạo cấu trúc sổ `study/findings.md` theo design và quy ước lưu kết quả thô trong `study/results/`; chưa điền lỗi giả định thành kết quả xác nhận.

## 3. Thực hiện phân tích tĩnh

- [x] 3.1 Chạy công cụ đã chọn trên danh mục phạm vi; lưu đầu ra thô, lệnh/cấu hình, mã thoát và danh sách tệp không phân tích được.
- [x] 3.2 Rà soát thủ công nhóm đăng nhập/phiên và quyền tại các endpoint liên quan; ghi bằng chứng và cập nhật checklist.
- [x] 3.3 Rà soát thủ công thêm/sửa/xóa sách và các luồng tìm kiếm liên quan; ghi bằng chứng và cập nhật checklist.
- [x] 3.4 Rà soát thủ công các thao tác quản lý thành viên trong phạm vi; ghi bằng chứng và cập nhật checklist.
- [x] 3.5 Rà soát thủ công mượn–trả và cách cập nhật các bảng liên quan; tách lỗi có bằng chứng khỏi giả định nghiệp vụ.

## 4. Thẩm định và tái lập

- [x] 4.1 Đối chiếu từng cảnh báo với ngữ cảnh, kiểm tra cơ chế kiểm soát và phụ thuộc; gộp trùng, gán trạng thái và liên kết bằng chứng trong sổ phát hiện.
- [x] 4.2 Với phát hiện được xác nhận tĩnh, ghi tác động, điều kiện tiên quyết, mức độ có lý do, độ tin cậy và hướng khắc phục; kiểm tra định nghĩa CWE nếu sử dụng.
- [x] 4.3 Chạy lặp lại cùng phiên bản/cấu hình/phạm vi, đối chiếu kết quả và giải thích chênh lệch; xác minh checksum baseline không đổi.
- [x] 4.4 Tổng hợp số tệp đã phân tích, tiêu chí đã rà soát, cảnh báo thô và kết quả sau thẩm định; ghi riêng các mục chưa đủ bằng chứng và giới hạn.

## 5. Hoàn thiện báo cáo học phần

- [x] 5.1 Viết phần giới thiệu và cơ sở lý thuyết trong `study/report.md`, dẫn nguồn rõ ràng và phân biệt kiểm thử tĩnh với thực thi ứng dụng.
- [x] 5.2 Viết phần đối tượng, mô hình phân hệ, phạm vi và phương pháp dựa trên baseline, checklist và hồ sơ công cụ thực tế.
- [x] 5.3 Viết phần kết quả và phân tích trường hợp từ sổ phát hiện, không đưa cảnh báo chưa xác minh thành lỗ hổng kết luận.
- [x] 5.4 Viết thảo luận, đề xuất khắc phục, giới hạn, kết luận và phụ lục tái lập; không tuyên bố đã sửa hoặc thử khai thác.
- [x] 5.5 Kiểm tra liên kết bằng chứng, số liệu, nguồn trích dẫn, giấy phép và dữ liệu nhạy cảm; bảo đảm mọi tiêu chí có kết quả hoặc lý do chưa đánh giá trước bàn giao.
