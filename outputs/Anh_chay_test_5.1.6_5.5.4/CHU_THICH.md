# Ảnh chạy test cho mục 5.1.6 và 5.5.4

Chụp ngày 25/10/2026 từ `chon_test.py` (http://127.0.0.1:8790). Test chạy trên bản sao `run_output/goi_chay_lai`. Cả bốn test chính đều Đạt, mã thoát 0. Ảnh nền sáng, độ phân giải 2x.

**Đánh số hình.** Hình 18 trở đi đã dùng ở Chương 9 của báo cáo nhóm. Chèn ảnh vào báo cáo nhóm trước rồi mới đánh số, để bản trích phần việc khớp số với báo cáo nhóm. Vì vậy chú thích dưới đây để `Hình ?`.

**Cách chụp.**
- Ảnh `giao_dien` là nguyên cửa sổ 1600×1500.
- Ảnh `nhat_ky` và `so_do` chụp ở khung rộng 760 px để chữ đủ đọc khi in. Ở mỗi ảnh này, khung nhật ký hoặc khung sơ đồ được kéo cao vừa đúng phần cần chụp, và nút phóng to/thu nhỏ của sơ đồ được ẩn. Nội dung không bị sửa.

## Mục 5.1.6 (Bảng 32)

| Tệp | Chú thích đề xuất | Ứng với |
|---|---|---|
| `5.1.6_a_sat_smt_giao_dien.png` | Hình ?. Giao diện chon_test.py khi chạy test “DPLL/SAT và SMT token”: nhật ký, kỳ vọng, thời gian chạy và sơ đồ kết quả | Ảnh tổng quan, tùy chọn |
| `5.1.6_b_sat_smt_nhat_ky.png` | Hình ?. Nhật ký chạy models/run_models.py: 16/16 công thức CNF cho kết quả trùng nhau giữa DPLL, Z3 và bảng chân trị; 10/10 bài toán SMT token đúng kỳ vọng | Bảng 32, hàng 1–2 |
| `5.1.6_c_sat_smt_so_do.png` | Hình ?. Kết quả SAT/SMT theo tệp mã sinh: mỗi tệp _v0 đều có ca có phản ví dụ, không tệp _v1 nào còn phản ví dụ | Bảng 32, hàng 1–2; Bảng 69 |
| `5.1.6_d_sql_giao_dien.png` | Hình ?. Giao diện chon_test.py khi chạy test “54 truy vấn SQL: CNF, SMT, mã sinh” | Ảnh tổng quan, tùy chọn |
| `5.1.6_e_sql_nhat_ky.png` | Hình ?. Nhật ký chạy models/run_sql_cases.py: 54 truy vấn, 92 tham số; 162/162 bài toán CNF và 552/552 bài toán SMT đúng kỳ vọng; lint 109 tệp mã sinh; Semgrep 54 hit ở _v0, 0 hit ở _v1 | Bảng 32, hàng 3–5 |
| `5.1.6_f_sql_so_do.png` | Hình ?. Kết quả 54 truy vấn SQL theo nhánh mã: source_v0, mã sinh _v0 và _v1 | Bảng 32, hàng 3–5 |
| `5.1.6_g_ma_sinh_nhat_ky.png` | Hình ?. Nhật ký quét mã sinh theo chức năng: Semgrep 8 hit trên 5 tệp _v0, 0 hit trên _v1 | Bảng 32, hàng 5 |

## Mục 5.5.4 (Bảng 44–46)

| Tệp | Chú thích đề xuất | Ứng với |
|---|---|---|
| `5.5.4_a_bo_nho_case_giao_dien.png` | Hình ?. Giao diện chon_test.py khi chạy test “Trạng thái, BMC, ngân sách, bộ đệm C” | Ảnh tổng quan, tùy chọn |
| `5.5.4_b_bo_nho_case_nhat_ky_vi_pham.png` | Hình ?. Nhật ký chạy models/run_memory_cases.py: 250 đối tượng trên 192 tệp; Z3, vét cạn và bộ duyệt trạng thái trùng nhau trên 250/250 đối tượng; baseline có 96 vi phạm thuộc 6 loại | Bảng 44, cột Baseline |
| `5.5.4_c_bo_nho_case_nhat_ky_c_models.png` | Hình ?. Kết quả Z3 cho 5 mô hình bộ đệm C: điều kiện vượt bộ đệm thỏa được ở _v0 (SAT) và không thỏa được ở _v1 (UNSAT) | Bảng 46, cột Z3 |
| `5.5.4_d_bo_nho_case_so_do.png` | Hình ?. Vi phạm bộ nhớ theo nhánh mã: baseline 96; mã chức năng 4 → 3; wrapper SQL 29 → 29; case bộ nhớ 14 → 0; 5 mô hình C chuyển từ SAT sang UNSAT | Bảng 44 và cột Z3 của Bảng 46 |
| `5.5.4_e_bo_nho_tinh_giao_dien.png` | Hình ?. Giao diện chon_test.py khi chạy test “Semgrep bộ nhớ, Clang, GCC (Docker)” | Ảnh tổng quan, tùy chọn |
| `5.5.4_f_bo_nho_tinh_nhat_ky_semgrep.png` | Hình ?. Nhật ký chạy evidence/run_memory_static.py, phần Semgrep: 130 kết quả của 6 luật PHP trên baseline và 15 kết quả của 4 luật C trên các tệp C _v0 | Bảng 45; cột Semgrep C của Bảng 46 |
| `5.5.4_g_bo_nho_tinh_nhat_ky_gcc_clang.png` | Hình ?. Kết quả GCC 14.4 -fanalyzer và Clang 21 --analyze trên mã C: GCC cảnh báo ở cả 5 tệp _v0, Clang ở 4/5; cả hai cho 0 kết quả trên 5 tệp _v1 | Bảng 46, cột GCC và Clang |
| `5.5.4_h_bo_nho_tinh_so_do.png` | Hình ?. Kết quả Semgrep, GCC và Clang theo nhánh mã: GCC cảnh báo ở cả 5 tệp C _v0, Clang ở 4/5; cả hai cho 0 cảnh báo trên 5 tệp _v1 | Bảng 45–46 |

**Ảnh `5.5.4_h` chụp lại ngày 26/10/2026.** Sơ đồ giờ đếm cảnh báo GCC và Clang theo cặp dòng–CWE không trùng, giống nhật ký (ảnh `5.5.4_g`) và Bảng 46. Vì vậy authorization.c và script_output.c ghi GCC 3, không còn ghi 4 như bản chụp trước.

## Bộ tối thiểu nếu không muốn chèn nhiều

- **5.1.6:** `b` và `e`. Hai ảnh này đủ cho bốn hàng đầu của Bảng 32; thêm `g` nếu muốn có hàng lint và quét mã sinh.
- **5.5.4:** `b`, `f`, `g`. Ba ảnh này lần lượt ứng với Bảng 44, 45, 46; thêm `c` nếu muốn có cột Z3.
