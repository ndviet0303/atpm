# Vì sao nạp 28 rule nhưng chỉ chạy 27

Log Semgrep của lần quét hợp lệ có ba dòng:

```
Scanning 66 files with 28 Code rules:
Scanning 66 files with 27 php rules.
Rules run: 27
```

## Kết luận

Rule không chạy là `php.wordpress-plugins.security.audit.wp-ssrf-audit.wp-ssrf-audit`. Đây là 1 trong 24 rule registry đóng băng. Rule này giới hạn phạm vi quét bằng `paths.include: ['**/wp-content/plugins/**/*.php']`, nghĩa là chỉ áp dụng cho plugin WordPress. Phân hệ `librarian/` không có tệp nào nằm dưới `wp-content/plugins/`, nên Semgrep nạp rule nhưng không áp dụng nó cho tệp nào.

Phép tính: 23 rule registry + 4 rule tùy biến = 27 rule chạy.

Việc này không làm mất cảnh báo nào. Khi bỏ bộ lọc đường dẫn để rule chạy trên cả 66 tệp, tổng vẫn là 322. Lý do là rule chỉ tìm các hàm HTTP của WordPress (`wp_remote_get` và các hàm tương tự), mà mã nguồn librarian không dùng WordPress.

## Bằng chứng (chạy ngày 16/10/2026, Semgrep 1.176.1, cùng 66 tệp)

| Lần chạy | Bộ rule | Code rules | php rules | Rules run | Cảnh báo | errors |
|---|---|---|---|---|---|---|
| Gốc (`./run.sh`) | 24 registry + 4 tùy biến | 28 | 27 | 27 | 322 | 0 |
| Đối chứng A | Bỏ `wp-ssrf-audit` | 27 | 27 | 27 | 322 | 0 |
| Đối chứng B | Giữ `wp-ssrf-audit` nhưng xóa `paths` | 28 | 28 | 28 | 322 | 0 |

- Lần A: bỏ đúng rule này thì "Code rules" giảm còn 27, còn "Rules run" không đổi. Vậy rule bị loại chính là rule này.
- Lần B: xóa bộ lọc đường dẫn thì cả 28 rule đều chạy. Vậy nguyên nhân là bộ lọc `paths`, không phải rule bị lỗi. Kết quả này cũng bác bỏ giả thuyết "hai rule `tainted-exec` trùng nhau". Hai rule đó có id đầy đủ khác nhau (`php.lang.security.tainted-exec.tainted-exec` và `php.lang.security.injection.tainted-exec.tainted-exec`), và cả hai đều có trong 28 rule chạy ở lần B.
- Log `--debug` của lần gốc liệt kê `running 28 rules from 2 configs`, trong đó có `wp-ssrf-audit`, rồi in `Scanning 66 files with 27 php rules`. Nghĩa là rule được nạp và hợp lệ, chỉ bị loại ở bước chọn rule áp dụng cho tệp.

## Câu trả lời khi bị hỏi

> Bộ quét nạp đủ 28 rule (24 rule registry đóng băng và 4 rule tùy biến). Một rule registry, `wp-ssrf-audit`, chỉ áp dụng cho thư mục `wp-content/plugins/` của WordPress, nên Semgrep tự loại nó khỏi danh sách áp dụng: 27 rule thực chạy. Nhóm đã kiểm chứng: bỏ bộ lọc đường dẫn thì 28 rule cùng chạy và kết quả vẫn đúng 322 cảnh báo, nên con số trong báo cáo không bị ảnh hưởng.

## Tái lập lần đối chứng B

```bash
E=outputs/Nhom13_23010359_NguyenDuyMinh_23010345_DangNhatNhat_23010636_NghiemDucViet_BTL/evidence
python3 -c "import json,sys; d=json.load(open(sys.argv[1])); [r.pop('paths',None) for r in d['rules'] if r['id'].endswith('wp-ssrf-audit')]; json.dump(d,open('run_output/rules_no_wp_paths.json','w'))" $E/frozen_registry_php_rules.json
study/.venv/bin/semgrep scan --metrics off --jobs 1 --no-git-ignore --config run_output/rules_no_wp_paths.json --config $E/custom_php_rules_corrected.yaml --json --output run_output/no_wp_paths.json study/source/librarian/*.php
```

Kỳ vọng: `Scanning 66 files with 28 php rules`, `Rules run: 28`, `Findings: 322`.
