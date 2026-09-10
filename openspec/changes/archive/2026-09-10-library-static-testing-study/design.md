## Context

Xem `proposal.md` về mục tiêu và phạm vi. Workspace hiện chưa chứa baseline PHP hoặc kết quả quét. Khảo sát sơ bộ upstream phát hiện nhiều bản sao mã và sự không đồng nhất giữa luồng độc giả ở thư mục gốc với SQL đi kèm. Các nhận xét này là dữ liệu định hướng, không phải kết quả kiểm thử toàn diện.

Tài liệu thiết kế cần thiết vì việc lựa chọn phạm vi, công cụ và chuẩn bằng chứng ảnh hưởng trực tiếp đến độ tin cậy của nghiên cứu an toàn phần mềm.

## Goals / Non-Goals

**Goals:**

- Cho phép người khác tái lập phân tích trên cùng commit, tập tệp, phiên bản công cụ và bộ quy tắc.
- Tách chất lượng mã, lỗi nghiệp vụ và vấn đề an toàn; không đánh đồng cảnh báo tự động với lỗ hổng.
- Đảm bảo mỗi kết luận đều có vị trí mã, ngữ cảnh và giới hạn bằng chứng.

**Non-Goals:**

- Không chứng minh khả năng khai thác bằng tấn công động; không truy cập demo công khai.
- Không nâng cấp PHP, sửa mã hoặc chuyển đổi cơ sở dữ liệu để phục vụ việc chạy ứng dụng.
- Không dùng số lượng cảnh báo làm thước đo duy nhất; không tuyên bố hệ thống an toàn nếu không tìm thấy lỗi.

## Decisions

### 1. Baseline bất biến, phạm vi theo danh mục tệp

Ở giai đoạn thực hiện, lấy đúng commit trong proposal vào `study/source/`, giữ LICENSE và ghi URL, commit, thời điểm lấy, cách lấy cùng checksum vào `study/baseline.md`. Không thực thi script từ upstream. Đặt danh mục tệp vào `study/scope.md`; đo lại quy mô cho riêng phạm vi, không dùng con số toàn repo làm số đo của phân hệ thủ thư.

Phạm vi chính là PHP tự viết trong `librarian/`, không gồm `vendors/`; SQL chỉ làm bằng chứng hỗ trợ mô hình dữ liệu. Nếu một include hoặc cấu hình bên ngoài phạm vi ảnh hưởng trực tiếp đến kết luận, đọc và ghi rõ là phụ thuộc hỗ trợ; mở rộng khảo sát sang chức năng mới cần thống nhất lại.

Thay vì quét toàn repo, cách này tránh đếm bản sao và mẫu mã bên thứ ba như lỗi của phân hệ. Bản sao `library/` không mặc nhiên đồng nhất toàn bộ với bản chính.

### 2. Checklist trước, công cụ sau

Lập `study/checklist.md` với: mã tiêu chí, nhóm chức năng, câu hỏi kiểm tra, cách thu thập bằng chứng và trạng thái. Các nhóm gồm xác thực/phiên, phân quyền tại endpoint, đầu vào/truy vấn, đầu ra HTML, bảo vệ thao tác đổi trạng thái, xử lý lỗi và toàn vẹn mượn–trả.

Đối với quy tắc nghiệp vụ không có đặc tả upstream rõ ràng, ghi là giả định cần kiểm chứng, không tự kết luận vi phạm yêu cầu. Kiểm tra các điểm vào xử lý trực tiếp, không chỉ các trang giao diện.

Chọn một công cụ phân tích tĩnh hỗ trợ PHP sau thử nghiệm nhỏ trên baseline. Ghi tài liệu chính thức hiện hành, phiên bản, giấy phép, giới hạn phân tích, cấu hình, bộ quy tắc và lệnh trong `study/tooling.md`; ưu tiên xử lý cục bộ. Nếu phải gửi mã đến dịch vụ ngoài hoặc phát sinh chi phí, xin xác nhận trước. Không mặc định công cụ kiểm tra kiểu hoặc phong cách là công cụ phát hiện đầy đủ lỗ hổng.

Lưu đầu ra thô vào `study/results/`; ghi lỗi phân tích cú pháp, tệp bị bỏ qua và mã thoát. Nếu công cụ không đọc được mã, đổi công cụ/cấu hình thay vì sửa baseline. Phương án chỉ đọc mã thủ công không đáp ứng mục tiêu kết hợp hai phương pháp, nên phải báo lại nếu không tìm được công cụ phù hợp.

### 3. Sổ phát hiện có thẩm định

Mỗi mục trong `study/findings.md` gồm ID, nguồn phát hiện, commit, tệp/dòng, trích đoạn ngắn, luồng dữ liệu hoặc điều kiện nghiệp vụ, cơ chế kiểm soát đã kiểm tra, tác động, điều kiện tiên quyết, mức độ và lý do, độ tin cậy, trạng thái, hướng khắc phục và giới hạn.

Trạng thái: `candidate`, `confirmed-static`, `false-positive`, `inconclusive`. Chỉ dùng `confirmed-static` khi bằng chứng đọc mã đủ chứng minh thiếu sót trong ngữ cảnh; không diễn giải thành đã khai thác thành công. Phân loại CWE khi phù hợp và đã kiểm tra nguồn định nghĩa. Gộp cảnh báo cùng nguyên nhân/vị trí thành một phát hiện, giữ liên kết đến cảnh báo gốc.

Các đoạn mượn–trả đã xem là điểm bắt đầu khảo sát, chưa được nhập sẵn thành lỗi xác nhận. Không chép toàn bộ dữ liệu cá nhân, mật khẩu hoặc bí mật từ SQL vào báo cáo.

### 4. Đề cương báo cáo và tiêu chí hoàn thành

Tạo `study/report.md` theo cấu trúc:

1. Giới thiệu: bài toán, mục tiêu, phạm vi và câu hỏi nghiên cứu.
2. Cơ sở lý thuyết: kiểm thử tĩnh, rà soát thủ công, phân tích tự động, cảnh báo giả và giới hạn.
3. Đối tượng khảo sát: nguồn/commit, cấu trúc phân hệ, mô hình dữ liệu và danh mục loại trừ.
4. Phương pháp: checklist, cấu hình công cụ, quy trình thẩm định và tái lập.
5. Kết quả: độ bao phủ khảo sát, cảnh báo thô, phát hiện sau gộp/thẩm định, các trường hợp tiêu biểu.
6. Thảo luận và đề xuất: điểm mạnh/yếu hai phương pháp, hướng khắc phục, giới hạn và kết luận.
7. Tài liệu tham khảo và phụ lục bằng chứng.

Hoàn thành khi mọi tiêu chí có kết quả hoặc lý do chưa đánh giá; mọi cảnh báo có quyết định thẩm định hoặc được ghi chưa đủ bằng chứng; thống kê khớp sổ phát hiện; một lần chạy lặp lại được đối chiếu và chênh lệch được giải thích. Không bắt buộc phát hiện số lỗi tối thiểu. Không tạo kết quả trước–sau sửa mã trong nghiên cứu này.

## Risks / Trade-offs

- [Mã cũ gây lỗi công cụ] → Thử trên mẫu trước; lưu giới hạn và không sửa baseline để làm đẹp kết quả.
- [Phạm vi thủ thư không đại diện toàn hệ thống] → Ghi rõ ngay tên đề tài và kết luận.
- [Suy đoán nghiệp vụ hoặc thiếu phụ thuộc] → Phân biệt giả định, đọc phụ thuộc liên quan và dùng `inconclusive` khi cần.
- [Cảnh báo giả/trùng lặp làm tăng số lỗi] → Thẩm định ngữ cảnh, gộp theo nguyên nhân và công bố tiêu chí đếm.
- [Tài liệu upstream dễ bị dùng như bài làm của nhóm] → Chỉ tham khảo có dẫn nguồn; báo cáo và phân tích phải do nghiên cứu này tạo ra.

## Migration Plan

Không triển khai hoặc migration. Giai đoạn thực hiện chỉ bổ sung tài liệu, cấu hình phân tích và bản sao nguồn có nguồn gốc rõ ràng; baseline không chỉnh sửa. Không tự động xóa dữ liệu workspace nếu thay đổi kế hoạch.

## Open Questions

- Công cụ và bộ quy tắc cụ thể: quyết định qua bước kiểm chứng tương thích trước khi quét đầy đủ.
- Số thành viên, thời hạn và định dạng nộp: chưa được cung cấp; kế hoạch chia theo đầu việc, chưa cam kết lịch hoặc tạo Word/PDF/slide.
