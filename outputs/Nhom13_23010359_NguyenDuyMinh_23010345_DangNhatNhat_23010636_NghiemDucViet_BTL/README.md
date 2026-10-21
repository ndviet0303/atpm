# Nhóm 13 — Kiểm thử tĩnh mã nguồn hệ thống quản lý thư viện

**Môn ưu tiên:** CSE703093 An toàn phần mềm. Hướng dẫn BTL được dùng cho báo cáo 7 phần. report_guide được tham chiếu cho bảng trước/sau.

| Thành viên | MSSV |
|---|---|
| Nguyễn Duy Minh | 23010359 |
| Đặng Nhất Nhất | 23010345 |
| Nghiêm Đức Việt | 23010636 |

Mã lớp và học kỳ chưa được cung cấp. Không tự gán phân công hoặc tỷ lệ đóng góp cho thành viên.

## Phạm vi và kết quả

Baseline upstream `082d6fb9bdd7846b57033513791ba5b6d2095c11`, dự án [Library Management System](https://github.com/vinitshahdeo/Library-Management-System), giấy phép MIT. Phạm vi: **66 PHP trực tiếp trong librarian** và đọc schema `db/eb_lms.sql`. Không tính vendor, bản sao library, portal hoặc tài sản JS/CSS riêng.

Đã thực hiện đọc nguồn, lint, SAST và solver offline. **Không khởi chạy ứng dụng, import CSDL, gửi HTTP hoặc thực thi các hàm PHP của mã sinh.** PHP `-l` chỉ phân tích cú pháp; bộ token đọc văn bản bằng `token_get_all`. PHPStan dùng stub hàm rỗng để nhận biết API cổ. Phần bộ nhớ (21/10/2026) cũng chỉ phân tích văn bản: Clang `--analyze` và GCC `-fanalyzer -c -o /dev/null` không liên kết hay chạy chương trình C.

| Bằng chứng | Kết quả nền 04/10, mở rộng 05/10 và bộ nhớ 21/10/2026 |
|---|---|
| Semgrep OSS 1.176.1 | 322 hit trên 66 PHP ở mỗi lần; 0 errors; exit 0 |
| Lặp Semgrep | 322 chữ ký giống nhau; chênh 0/0 |
| PHPStan 2.1.8 level 0 | 17 messages/16 tệp: 14 whitespace, 3 include thiếu; exit 1 |
| PHP CLI 8.5.10 lint | 66/66 thành công; không chứng minh ứng dụng chạy được |
| SHA-256 baseline | 66/66 PHP không đổi; schema/LICENSE khớp |
| 10 mã sinh PHP | 8 hit _v0, 0 hit _v1 theo 6 rule hẹp; 10/10 lint |
| DPLL, Z3 SAT, bảng chân trị | 16/16 CNF trùng kết quả; có đối chứng quay lui |
| Z3 SMT 5.1.0.0 | 10/10 đúng kỳ vọng: 1 SAT trước, 8 UNSAT sau, 1 SAT đối chứng |
| Kiểm kê SQL theo từng sink | 54 query trong 37 tệp: 35 động, 19 hằng; 92 lần xuất hiện field |
| Mã sinh SQL theo từng query | 54 cặp +1 helper =109 PHP; lint109/109; 54 raw mysql_query hit _v0, 0 _v1 |
| CNF SQL | 162/162 khớp kỳ vọng và ba cách giải DPLL/Z3/bảng chân trị |
| SMT từng field | 552/552 khớp kỳ vọng; sáu điều kiện riêng cho mỗi trong 92 field |
| Trạng thái bộ nhớ (13 trạng thái, 36 phép chuyển) | 96 vi phạm trên 27/66 PHP baseline; _v0/_v1: mã sinh 4/3, SQL 29/29, memory 14/0; 19/19 unit test |
| Z3 BMC bộ nhớ | 250/250 đối tượng: Z3, vét cạn và bộ phân tích trùng kết quả; 92 SAT |
| Z3 ngân sách 128 MiB | Baseline 24 SAT, 14 UNSAT, 1 không xác định; memory/_v1 4/4 UNSAT |
| Semgrep bộ nhớ (7 luật PHP, 4 luật C) | 167 hit ứng viên; 0 errors; exit 0 |
| C: GCC 14.4, Clang 21, Z3 | GCC báo lỗi ở 5/5 tệp _v0, Clang ở 4/5; 0 kết quả ở _v1; 5 mô hình bộ đệm: _v0 SAT, _v1 UNSAT |

322 hit là cảnh báo thô, chưa phải số lỗ hổng độc lập. 11 nhóm phát hiện đã được đối chiếu source. Baseline **chưa được vá**. 0 hit ở mã sinh hoặc UNSAT trong mô hình không chứng minh phần mềm an toàn. Vi phạm bộ nhớ là kết quả của mô hình trạng thái trừu tượng; 38 E_HELD_TO_END có mức thấp vì PHP dọn resource khi request kết thúc.

## Thành phần

- `Nhom_13_Bao_cao_Static_Testing_Thu_vien.pdf`: bản báo cáo để nộp (bản 21/10/2026, 108 trang, thêm mục 5.5 kiểm thử tĩnh bộ nhớ; xem ghi chú đầu `KIEM_TRA_HOAN_THIEN.md`).
- `.docx` cùng tên: bản chỉnh sửa, mục lục có trường Word; số trang cached đã đối chiếu bản PDF.
- `Nhom_13_Dac_ta_va_TestCase_Thu_vien.xlsx`: 10 sheet theo mẫu +4 sheet chi tiết, có 816 hồ sơ: 22 tổng hợp, 54 source SQL, 178 SAT/CNF và 562 SMT. Không coi 22 mục tổng hợp là phép chạy mới. Thêm 5 sheet bộ nhớ: BoNhoTrangThai, BoNhoViPham, BoNhoBMC, BoNhoNganSach, BoNhoBoDemC.
- `source_v0/`: bản sao đúng 66 PHP khảo sát, schema và LICENSE; không phải gói triển khai đủ tài sản giao diện/vendor.
- `generated_cases/_v0/` và `_v1/`: 5 cặp về login, authz, query, token và encoding script. `_v0` có lỗi cố ý, chỉ dùng phân tích tĩnh.
- `models/run_models.py`: DPLL cùng cross-check Z3/bảng chân trị; 10 bài toán SMT token.
- `generated_cases/sql/_v0/`, `_v1/` và `guards.php`: 54 cặp SQL độc lập cùng guard dùng chung; không tích hợp vào baseline.
- `models/run_sql_cases.py`: trích đủ 54 query, truy nguồn 92 field, sinh mã và chạy 162 CNF/552 SMT mới; lint/SAST109 PHP. `models/build_case_register.py` xây sổ 816 hồ sơ từ output đã lưu.
- `evidence/`: raw JSON, log, snapshot rule, manifest, inventory; `formal/` chứa DIMACS CNF và SMT-LIB.
- `evidence/sql_formal/`: công thức từng case SQL. Toàn gói có 178 `.cnf` và 785 `.smt2`; 178 SMT-LIB mã hóa SAT, 562 SMT-LIB cho token/field và 45 SMT-LIB bộ nhớ trong `evidence/memory_formal/`.
- `generated_cases/memory/_v0/`, `_v1/`: 4 cặp PHP cho bộ nhớ; `generated_cases/memory_c/_v0/`, `_v1/`: 5 cặp C viết lại năm chức năng. Chỉ phân tích văn bản, không chạy.
- `models/memory_typestate.py` và `evidence/extract_memory_tokens.php`: bộ phân tích trạng thái bộ nhớ trên token PHP; `models/test_memory_typestate.py`: 19 unit test; `models/run_memory_cases.py`: chạy bộ phân tích trên mọi nhóm mã, BMC, ngân sách bộ nhớ và mô hình bộ đệm C bằng Z3.
- `evidence/run_memory_static.py`, `memory_rules.yaml`: lint, Semgrep, Clang và GCC cho phần bộ nhớ; output ở `memory_static_results.json`, `memory_semgrep.json`, `memory_case_results.json`, `memory_traces.json` và `memory_cwe_cve.json` (CWE/CVE tra MITRE và NVD ngày 21/10/2026).
- `tools/mysql_stub.php`, `tools/phpstan.neon`: cấu hình phân tích tĩnh cho bản sao nguồn trong gói.

## Chuẩn bị công cụ

Dùng Python 3.11 trở lên, PHP CLI và công cụ có đúng phiên bản nếu cần so lại số liệu. Gói không chứa runtime hoặc môi trường ảo. Từ thư mục gói đã giải nén:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install semgrep==1.176.1 z3-solver==5.1.0.0
curl -L -o tools/phpstan.phar https://github.com/phpstan/phpstan/releases/download/2.1.8/phpstan.phar
```

Chỉ bước cài công cụ cần mạng. Quét dùng snapshot rule local, `--metrics off`, không upload source. Trên macOS nếu Semgrep báo thiếu trust anchors, dùng CA bundle của certifi từ môi trường đã cài công cụ, không tắt xác minh TLS:

```sh
export SSL_CERT_FILE="$(.venv/bin/python -m certifi)"
```

Phần bộ nhớ cần thêm `clang` (số liệu trong gói dùng Apple clang 21.0.0). GCC 14.4 chạy trong Docker từ image ghim theo digest, với `--network none`; nếu không có Docker, `run_memory_static.py` ghi `skipped` cho GCC thay vì kết quả.

## Chạy lại phân tích tĩnh

Nên sao chép gói trước khi chạy lại vì các script ghi đè output cùng tên. Kết quả gốc trong gói ZIP và `checksums.json` giúp so sánh.

```sh
export SEMGREP_BIN="$PWD/.venv/bin/semgrep"
.venv/bin/python evidence/collect_static.py
.venv/bin/python evidence/run_sast.py
.venv/bin/python evidence/run_generated_static.py
.venv/bin/python models/run_models.py
.venv/bin/python models/run_sql_cases.py
.venv/bin/python models/build_case_register.py
.venv/bin/python evidence/auth_model.py
php -d memory_limit=1G tools/phpstan.phar analyse -c tools/phpstan.neon --error-format=json --no-progress --debug
.venv/bin/python models/test_memory_typestate.py
.venv/bin/python evidence/run_memory_static.py
.venv/bin/python models/run_memory_cases.py
```

Script tự chọn `study/source` khi chạy trong repo ban đầu hoặc `source_v0` khi giải nén riêng. `run_sast.py` kiểm tra SHA-256 rule trước khi quét; mỗi lần quét phải exit 0 và `errors=[]`. PHPStan exit 1 khi có messages là kết quả phân tích có lỗi trong nguồn, không có nghĩa công cụ không chạy. Với `--debug`, stdout có danh sách tệp trước JSON cuối; giữ nguyên log, tách đối tượng JSON cuối để so 17 thông báo. Đường dẫn và timestamp có thể khác khi giải nén, so chữ ký đã chuẩn hóa theo tên tệp/toạ độ và tổng hợp rule.

PHP sinh được lint trong `run_generated_static.py` và `run_sql_cases.py`. Không chạy `php generated_cases/...` để thử nghiệp vụ. Không cần secret key triển khai, CSDL hoặc tài khoản ứng dụng cho các phép kiểm tra này.

## Tra từng query và case SQL

Phụ lục G ghi từng SQL-01 đến SQL-54; phụ lục H tách 16 SAT và 10 SMT chức năng. Trong Excel:

| Sheet | Nội dung |
|---|---|
| SQLTruyVan | 54 điểm gọi: source/dòng, SQL gốc, SQL prepared, nguồn dữ liệu, kết luận và giới hạn |
| SQLDauVao | 92 field: biến, GET/POST hoặc DB, dòng gán, cột schema, kiểu/miền và binding |
| SATChiTiet | 178 case: mapping biến, CNF, kỳ vọng, DPLL/Z3/vét cạn, witness, trace và file công thức |
| SMTChiTiet | 562 case: miền, guard, input/predicate, kỳ vọng, Z3, model và SMT-LIB |
| TestCase | 816 ID để lọc và truy vết yêu cầu, điều kiện, bước, kết quả và bằng chứng |

**Phân loại source:** 23 query nhận HTTP trực tiếp; 3 dùng hàng từ SELECT chưa bind; 9 dùng INT từ SELECT hằng; 19 query hằng. Có 79 field GET/POST và 13 field DB. Rule raw API bắt cả query hằng, vì vậy **54 hit không phải 54 SQLi**. Với cột INT từ query hằng, thiếu bind là vấn đề hardening; chưa tự xác nhận khả năng SQLi. Hàng sau SELECT chưa bind không được mặc định tin cậy chỉ vì tên cột ban đầu là INT.

Mỗi query có `SQL-xx-SAT-B` (trước sửa), `SAT-A` (sau sửa) và `SAT-C` (đối chứng). Query động kỳ vọng SAT/UNSAT/SAT; query hằng UNSAT/UNSAT/SAT vì hội rỗng của binding là true. Đây là mô hình policy binding, không là payload khai thác SQL.

Mỗi field có sáu SMT riêng: MISSING, TYPE, FORMAT, MAX, MIN, VALID. Bốn case đầu từ chối đầu vào thiếu/sai/vượt cận trên. Int dưới minimum bị từ chối; chuỗi rỗng vẫn được schema cho phép. VALID nhận giá trị đúng cận trên. Cận VARCHAR lấy schema; cận trên INT32 là 2.147.483.647. Minimum ID=1, số bản sách/năm=0 là chính sách mã sinh đề xuất, chưa có SRS xác nhận. `int(11)`/`int(50)` là độ rộng hiển thị, không là số bit.

Wrapper chỉ xử lý query, kiểu và binding. Caller còn kiểm tra phiên/quyền/CSRF, ownership và transaction. Các mẫu login SQL chỉ minh họa binding, vẫn cần xử lý mật khẩu theo FIND-05/core authentication. LIKE chọn literal substring và escape `!/%/_`; nếu tích hợp cần xác nhận wildcard policy và charset vì schema dùng latin1 còn guard chuỗi dùng UTF-8.

Đường dẫn công thức theo ID viết thường, ví dụ `evidence/sql_formal/sql-10-sat-b.cnf` và `evidence/sql_formal/sql-10-p01-smt-max.smt2`. Expected được đặt trước khi giải; actual/model/trace lấy từ công cụ. `sql_case_results.json`, `sql_inventory.json` và `case_register.json` nối mã case với source và mã sinh.

## Cách đọc formal results

Các mô hình là **phép dịch thủ công các guard/policy**, không phải symbolic execution đầy đủ của PHP. `formal_results.json` ghi biến, clauses, trace, witness, assumptions và hash mã sinh. SAT có phản ví dụ trong quan hệ được khai báo; UNSAT không có phản ví dụ trong quan hệ đó.

- Login: row tồn tại và password hợp lệ mới được cấp.
- Authz: phiên và role phải phù hợp action. RBAC admin/librarian là chính sách thí nghiệm; upstream chưa có SRS vai trò.
- Query: thao tác với dữ liệu không tin cậy phải bind; ngữ nghĩa PDO được giả định đúng.
- Script: serialize theo ngữ cảnh; đây là encoding, không phải mã hóa mật mã.
- Token: GCM key 32 byte, nonce 12 byte, tag 16 byte, TTL 1800 giây; guard uid/audience/iat/exp. Constants được đọc lại từ PHP.

Mô hình tin vào `password_verify`, PDO binding, OpenSSL tag verification, JSON serialization và `random_bytes`. Không chứng minh entropy khóa, uniqueness nonce, an toàn AES, replay, rotation hoặc policy đúng với SRS. Baseline không có cơ chế token crypto ứng dụng; `_v0/_v1/token_crypto.php` là thí nghiệm riêng. Base64 chỉ là encoding truyền tải. Lưu khóa môi trường trong `_v1` không tự chứng minh cách quản trị secret an toàn.

Tệp `.smt2` có thể được đưa vào Z3 CLI đã cài:

```sh
z3 evidence/formal/token_v1_expired.smt2
```

Kết quả kỳ vọng: `unsat`. Trace/witness đối chiếu trong JSON được tạo bởi chương trình đã chạy; không phải giá trị ví dụ được điền bằng tay.

## Kiểm thử tĩnh bộ nhớ

Mục 5.5 của báo cáo trình bày phần này. Trong Excel:

| Sheet | Nội dung |
|---|---|
| BoNhoTrangThai | 36 phép chuyển (trạng thái, sự kiện) → (trạng thái mới, vi phạm, CWE) |
| BoNhoViPham | 175 vi phạm của mọi nhóm mã: tệp, dòng, biến, mệnh đề, vi phạm, CWE, mức |
| BoNhoBMC | 250 đối tượng: chuỗi sự kiện, kết quả Z3, vi phạm và một nhân chứng |
| BoNhoNganSach | 128 truy vấn: SQL, cận số dòng, byte mỗi dòng, Z3 và N nhỏ nhất vượt 128 MiB |
| BoNhoBoDemC | 10 mô hình bộ đệm C (_v0 và _v1): CWE, Z3, nhân chứng và tệp SMT-LIB |

Bộ phân tích không phân biệt đường đi, trải vòng lặp 2 lần và không nối `include`. Độ rộng dòng lấy theo khai báo cột trong `eb_lms.sql`; ngân sách giả định driver mysqlnd. CVE trong `memory_cwe_cve.json` chỉ là ví dụ cùng lớp CWE trên sản phẩm khác, không gán cho mã thư viện.

## Toàn vẹn và nguồn tham khảo

`checksums.json` chứa SHA-256 của các thành phần nộp; `source_inventory.json` chứa hash/LOC đầy đủ 66 PHP. Source baseline, schema và các mẫu đầu vào được giữ nguyên. Rule cũ có lỗi parse được sửa **trên bản sao**: thêm `;` sau `echo mysql_error(...)`. Vì vậy 270 hit cũ không đầy đủ, 322 hit mới hợp lệ.

`evidence/expanded_validation.json` ghi đối chiếu từng vị trí SQL với bộ token độc lập, các ID trong Word/Excel và kết quả tái lập trên bản sao độc lập. `evidence/final_quality_check.json` ghi số trang nội dung chính, mục lục và kiểm tra định dạng của bản nộp.

`KIEM_TRA_HOAN_THIEN.md` đối chiếu từng yêu cầu của nhóm với vị trí trong báo cáo và bằng chứng; `evidence/completion_audit.json` ghi kiểm tra toàn bộ dữ liệu của năm sheet tra cứu với inventory và output gốc.

AI hỗ trợ: Codex hỗ trợ đọc nguồn/tài liệu, sinh mã, xây DPLL/mô hình Z3, chạy công cụ, tổng hợp bằng chứng và định dạng báo cáo. Không nhận kết quả IoT của template làm bằng chứng cho thư viện.

Tham khảo: tài liệu BTL do người dùng cung cấp; [Semgrep CLI](https://semgrep.dev/docs/cli-reference); [PHPStan CLI](https://phpstan.org/user-guide/command-line-usage); [Z3 Guide](https://github.com/microsoft/z3guide); [PHP OpenSSL](https://www.php.net/manual/en/function.openssl-decrypt.php); các định nghĩa MITRE CWE và bibliography trong báo cáo.
