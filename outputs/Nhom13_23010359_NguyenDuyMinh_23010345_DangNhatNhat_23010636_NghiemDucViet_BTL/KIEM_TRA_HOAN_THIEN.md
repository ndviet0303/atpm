# Rà soát mức độ hoàn thiện báo cáo Nhóm 13

Bản kiểm tra này đối chiếu yêu cầu của nhóm với bản PDF, Word, Excel và bằng chứng đã lưu. Có 17 trang nội dung chính, 54 hồ sơ SQL, 178 case SAT và 562 case SMT.

| ID | Yêu cầu | Đối chiếu trong báo cáo | Bằng chứng |
|---|---|---|---|
| R01 | Ưu tiên hướng dẫn BTL môn An toàn phần mềm; đủ 7 phần; 10–20 trang chính | Bìa và mục lục; phần 2–7; 17 trang chính | PDF trang 1–19; evidence/final_quality_check.json |
| R02 | Bìa đúng Nhóm 13, tên và MSSV; không tự điền thông tin chưa có | Bìa và mục 7.2 | PDF trang 1,18; provenance.json |
| R03 | Tiếng Việt, định dạng nhất quán, sơ đồ và mục lục đúng trang | Phần 3 có hình kiến trúc; toàn bộ 172 trang đã xem; mục lục tự động có cache đối chiếu PDF | DOCX; PDF; evidence/final_quality_check.json |
| R04 | Đọc mã nguồn thư viện hiện tại và xác định phạm vi | 66 PHP giữ nguyên SHA-256, schema, LICENSE; 2.978 dòng; chỉ phân hệ librarian | source_v0; evidence/source_inventory.json; evidence/static_summary.json |
| R05 | Phân tích xác thực đăng nhập, phân quyền và đường đi dữ liệu | Phần 4.4–4.5 và 5.2; mã trước/sau authentication và authorization | PDF trang 7,11; generated_cases/_v0,_v1; SATChiTiet |
| R06 | Tách từng truy vấn SQL và từng đầu vào | 54 SQL trong 37 tệp; 92 field; đối chiếu mọi trường trong các sheet chi tiết với inventory | Phụ lục G; SQLTruyVan; SQLDauVao; evidence/sql_inventory.json |
| R07 | Phân tích script encoding và encryption/token đúng bản chất | Phần 4.6,5.3,5.4; phân biệt Base64, encoding script, hash mật khẩu và AEAD | PDF trang 8,12,13; generated_cases/_v0,_v1/script_output.php và token_crypto.php |
| R08 | Token có thuộc tính mật mã, độ dài và secret key | Key32/nonce12/tag16 byte; TTL1800 giây; constants trong mã khớp mô hình; nguồn khóa và giới hạn quản trị được nêu | PDF trang 8,13; evidence/formal_results.json; token_crypto.php |
| R09 | Sinh mã cho các chức năng và từng SQL; có trước/sau | 5 cặp chức năng,54 cặp SQL và helper:119 PHP; chỉ lint/SAST, chưa tích hợp vào baseline | generated_cases; HamSinhMa; evidence/generated_static_results.json; evidence/sql_static_results.json |
| R10 | Từng case DPLL/SAT có công thức, kỳ vọng, kết quả và phản ví dụ/trace | 178 case; mọi hàng SATChiTiet khớp biến,CNF,predicate,expected,actual,witness,trace và đường bằng chứng | Phụ lục G,H; SATChiTiet; evidence/formal; evidence/sql_formal |
| R11 | Từng case SMT/Z3 có miền, guard, input, kỳ vọng và kết quả | 562 case; mọi hàng SMTChiTiet khớp policy,predicate,input,expected,actual,model và bằng chứng | Phụ lục G,H; SMTChiTiet; evidence/formal_results.json; evidence/sql_case_results.json |
| R12 | Chạy công cụ thật trong phạm vi static testing | Raw Semgrep 322/322,exit0,errors0; lint/SAST và kết quả solver đã lưu; không chạy ứng dụng,CSDL hay HTTP | evidence/sast_manifest.json; semgrep_run1/2.json; expanded_validation.json; portability_check.json |
| R13 | Kết quả có bằng chứng, CWE, nguyên nhân và mức ưu tiên; không dùng số hit/case làm số lỗi | Phần 5 phân tích11 nhóm; SQL hằng/HTTP/DB tách riêng; 816 hồ sơ gồm22 tổng hợp | PDF trang 10–16; TestCase; evidence/case_register.json |
| R14 | Thảo luận giới hạn, tài liệu tham khảo và công bố hỗ trợ AI | Phần 6,7.2,7.4; mô hình guard thủ công; chưa chứng minh AES/entropy/replay; baseline chưa vá | PDF trang 17–19; README.md |
| R15 | Có thể tra cứu và tái lập, nộp đủ PDF/Word/Excel/mã/kết quả | README có lệnh tái lập; bản sao độc lập đã khớp; source,models,raw output và manifest trong ZIP theo tên/MSSV | README.md; evidence/expanded_validation.json; evidence/portability_check.json; checksums.json |

## Thông tin và giới hạn cần đọc kèm

- Mã lớp và học kỳ chưa được cung cấp; giữ thông báo rõ trên bìa.
- Phân công cá nhân chưa được cung cấp; không tự gán đóng góp.
- RBAC,TTL và một số cận nghiệp vụ là chính sách đề xuất; chưa phải SRS upstream.
- Mô hình guard thủ công; kết quả SMT không là chứng minh mật mã hoặc toàn bộ hành vi PHP.

Đối chiếu toàn bộ 18,840 ô dữ liệu thuộc năm sheet TestCase, SQLTruyVan, SQLDauVao, SATChiTiet và SMTChiTiet với inventory và output gốc; không chỉ kiểm tra ID hoặc tổng số case.

Bản đối chiếu có dữ liệu máy đọc trong evidence/completion_audit.json. SHA-256 của các tài liệu báo cáo được ghi kèm để xác định đúng phiên bản.
