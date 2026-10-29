"""Sinh bo_sung_v1/source_v1 từ source_v0 theo các bản vá của Chương 7 (mỗi CWE một bước, có thể đọc lại).

source_v0 không bị sửa. Chạy lại cho ra đúng cùng nội dung (mã băm mật khẩu mẫu ghi cứng).
Script chỉ biến đổi văn bản; không chạy mã PHP, không kết nối CSDL.
Dùng: python bo_sung_v1/make_v1.py
"""
from pathlib import Path
import re
import shutil

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / 'source_v0'
OUT = Path(__file__).resolve().parent / 'source_v1'

HANDLERS = ['books_save', 'borrow_save', 'delete_books', 'delete_member', 'delete_student', 'delete_user',
            'member_save', 'return_save', 'student_save', 'update_books', 'update_member', 'update_students']
LIST_PAGES = ['books', 'advance_search', 'new_books', 'old_books', 'lost', 'damage', 'sub_rep', 'archive', 'borrow']
EDIT_PAGES = ['edit_book', 'edit_member', 'edit_student']
CONFIRM_MODALS = ['delete_book_modal', 'delete_member_modal', 'delete_student_modal', 'delete_user_modal']
INT_VARS = {'id', 'get_id', 'cat_id', 'category_id', 'book_id', 'member_id', 'borrow_id', 'user_id'}
ADMIN_HASH = '$2y$12$DvJxC0CQ4ByTq87/bmPa0OwZa1/gWzUWSkm7GuH2tvwMfBye3BN9e'  # password_hash('admin'), dữ liệu mẫu

NEW_FILES = {
    'security.php': r"""<?php
// v1 — CWE-79, CWE-352: mã hóa đầu ra, phiên an toàn và token CSRF dùng chung.
function e($value)
{
    return htmlspecialchars((string) $value, ENT_QUOTES, 'UTF-8');
}

function start_secure_session()
{
    if (session_status() !== PHP_SESSION_ACTIVE) {
        session_set_cookie_params(['httponly' => true, 'secure' => !empty($_SERVER['HTTPS']), 'samesite' => 'Strict']);
        session_start();
    }
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
}

function csrf_field()
{
    return '<input type="hidden" name="csrf_token" value="' . e($_SESSION['csrf_token']) . '">';
}

function csrf_verify($token)
{
    return is_string($token) && isset($_SESSION['csrf_token']) && hash_equals($_SESSION['csrf_token'], $token);
}
?>""",
    'auth_guard.php': r"""<?php
// v1 — CWE-306, CWE-352: mọi handler ghi dữ liệu phải qua guard này trước khi chạm CSDL.
require_once __DIR__ . '/session.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !csrf_verify($_POST['csrf_token'] ?? '')) {
    http_response_code(403);
    exit('Yêu cầu không hợp lệ.');
}
require_once __DIR__ . '/dbcon.php';
?>""",
    'dbcon.php': r"""<?php
// v1 — CWE-209: lỗi CSDL chỉ ghi log phía server, người dùng nhận thông báo chung.
ini_set('display_errors', '0');
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
set_exception_handler(function ($e) {
    error_log('[LMS] ' . $e);
    http_response_code(500);
    exit('Hệ thống tạm thời gặp lỗi. Vui lòng thử lại sau.');
});
$conn = mysqli_connect(getenv('LMS_DB_HOST') ?: 'localhost', (string) getenv('LMS_DB_USER'), (string) getenv('LMS_DB_PASS'), getenv('LMS_DB_NAME') ?: 'eb_lms');
mysqli_set_charset($conn, 'utf8mb4');

// CWE-89: tham số luôn đi qua prepared statement, không bao giờ được ghép vào chuỗi SQL.
function db_query($sql, $types = '', ...$params)
{
    global $conn;
    $stmt = mysqli_prepare($conn, $sql);
    if ($types !== '') {
        mysqli_stmt_bind_param($stmt, $types, ...$params);
    }
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);
    return $result === false ? mysqli_stmt_affected_rows($stmt) : $result;
}
require_once __DIR__ . '/security.php';
?>""",
    'session.php': r"""<?php
//Start session
// v1 — cookie phiên HttpOnly, SameSite=Strict; tạo token CSRF cho phiên.
require_once __DIR__ . '/security.php';
start_secure_session();
//Check whether the session variable SESS_MEMBER_ID is present or not
if (!isset($_SESSION['id']) || (trim($_SESSION['id']) == '')) {
    header("location: index.php");
    exit();
}
$session_id=$_SESSION['id'];
?>""",
    'logout.php': r"""<?php
require_once __DIR__ . '/security.php';
start_secure_session();
$_SESSION = [];
session_destroy();
header('location:../index.php');
?>""",
}

LOGIN_V1 = """if (isset($_POST['submit'])){
start_secure_session();
$username = $_POST['username'];
$password = $_POST['password'];
unset($_POST['password']); // v1 — CWE-316: chỉ còn một tham chiếu nên sodium_memzero xóa được chuỗi
// v1 — CWE-89: tra cứu bằng tham số; CWE-256: so khớp băm bằng password_verify, không so sánh bản rõ trong SQL.
$result = db_query("SELECT user_id, password FROM users WHERE username = ?", "s", $username);
$row = mysqli_fetch_array($result);
$ok = false;
if ($row && password_verify($password, $row['password'])) {
$ok = true;
}
sodium_memzero($password);
if ($ok) {
session_regenerate_id(true);
$_SESSION['id']=$row['user_id'];
header('location:dashboard.php');
exit();
}
else{ ?>
<div class="alert alert-danger">Access Denied</div>
<?php
}}"""

ADD_USER_V1 = """if (isset($_POST['submit'])){
if (!csrf_verify($_POST['csrf_token'] ?? '')) { http_response_code(403); exit('Yêu cầu không hợp lệ.'); }
$username=$_POST['username'];
// v1 — CWE-256: chỉ lưu giá trị băm thích ứng của mật khẩu.
$plain_password=$_POST['password'];
unset($_POST['password']); // v1 — CWE-316: chỉ còn một tham chiếu
$password=password_hash($plain_password, PASSWORD_DEFAULT);
sodium_memzero($plain_password);
$firstname=$_POST['firstname'];
$lastname=$_POST['lastname'];

db_query("insert into users (username,password,firstname,lastname) values(?,?,?,?)", "ssss", $username, $password, $firstname, $lastname);
}"""

EDIT_USER_V1 = """if (isset($_POST['edit'])){
if (!csrf_verify($_POST['csrf_token'] ?? '')) { http_response_code(403); exit('Yêu cầu không hợp lệ.'); }
$user_id=$_POST['id'];
$username=$_POST['username'];
$firstname=$_POST['firstname'];
$lastname=$_POST['lastname'];
// v1 — CWE-256: chỉ lưu giá trị băm; để trống nghĩa là giữ mật khẩu cũ.
$plain_password=$_POST['password'];
unset($_POST['password']); // v1 — CWE-316: chỉ còn một tham chiếu
if ($plain_password === '') {
db_query("update users set username = ?, firstname = ?, lastname = ? where user_id = ?", "sssi", $username, $firstname, $lastname, $user_id);
} else {
$password=password_hash($plain_password, PASSWORD_DEFAULT);
db_query("update users set username = ?, password = ?, firstname = ?, lastname = ? where user_id = ?", "ssssi", $username, $password, $firstname, $lastname, $user_id);
}
sodium_memzero($plain_password); ?>"""

BORROW_V1 = """	// v1 — CWE-362: phiếu và chi tiết trong một giao dịch InnoDB; ID lấy từ chính kết nối này.
	mysqli_begin_transaction($conn);
	db_query("insert into borrow (member_id,date_borrow,due_date) values (?,NOW(),?)", "is", $member_id, $due_date);
	$borrow_id = mysqli_insert_id($conn);
	foreach ($id as $book_id) {
	    db_query("insert into borrowdetails (book_id,borrow_id,borrow_status) values(?,?,'pending')", "ii", (int) $book_id, $borrow_id);
	}
	mysqli_commit($conn);
"""

QUERY = re.compile(r'mysql_query\(\s*"((?:[^"\\]|\\.)*)"\s*\)(\s*or\s+die\s*\(\s*mysql_error\(\)\s*\))?', re.S)
INTERP = re.compile(r"'(%?)\$(\w+)((?:\[\$\w+\])?)(%?)'|\$(\w+)")
ECHO = re.compile(r'<\?php(\s+)echo\s+(.*?)\s*;?\s*\?>')


def sub1(text, old, new):
    """Thay đúng một chỗ; sai số lần là bản vá không còn khớp mã gốc."""
    assert text.count(old) == 1, (old[:60], text.count(old))
    return text.replace(old, new)


def to_db_query(m):
    """CWE-89, CWE-477, CWE-209: mysql_query("... '$x' ...") or die(mysql_error()) -> db_query("... ? ...", "s", $x)."""
    types, params = '', []

    def place(v):
        nonlocal types
        name = v.group(5) or v.group(2)
        expr = '$' + name + (v.group(3) or '')
        parts = [f"'{v.group(1)}'"] * bool(v.group(1)) + [expr] + [f"'{v.group(4)}'"] * bool(v.group(4))
        params.append(' . '.join(parts))
        types += 'i' if name in INT_VARS else 's'
        return '?'
    sql = INTERP.sub(place, m.group(1))
    return f'db_query("{sql}"' + (f', "{types}", ' + ', '.join(params) if params else '') + ')'


def encode_echo(m):
    """CWE-79: mọi echo giá trị động qua e(); ID (cả trong bộ chọn jQuery) ép (int) trước rồi mới qua e()."""
    expr = re.sub(r'/\*.*?\*/', '', m.group(2)).strip().rstrip(';').strip()
    if expr.startswith(('csrf_field(', '(int)', 'e(')) or re.fullmatch(r"'[^']*'", expr):
        new = expr
    elif link := re.fullmatch(r"'([^']*)'\s*\.\s*(\$\w+)", expr):
        new = f"e('{link[1]}' . (int) {link[2]})"
    elif re.fullmatch(r'\$\w*id', expr) or expr == '$total':
        new = f'e((int) {expr})'
    else:
        new = f'e({expr})'
    return f'<?php{m.group(1)}echo {new}; ?>'


def patch(name, text):
    stem = name[:-4]
    if stem in ('index', 'login'):
        start = text.index("if (isset($_POST['submit'])){")
        end = text.index('}}', start) + 2
        indent = text[text.rindex('\n', 0, start) + 1:start]
        text = text[:start] + LOGIN_V1.replace('\n', '\n' + indent) + text[end:]
    if stem == 'modal_add_user':
        start = text.index("if (isset($_POST['submit'])){")
        text = text[:start] + ADD_USER_V1.replace('\n', '\n\t') + text[text.index('}', text.index('mysql_query', start)) + 1:]
    if stem == 'modal_edit_user':
        text = sub1(text, '<input type="text" name="password" id="inputPassword" value="<?php echo $row[\'password\']; ?>" required>',
                    '<input type="password" name="password" id="inputPassword" placeholder="Để trống nếu giữ mật khẩu cũ">')
        start = text.index("if (isset($_POST['edit'])){")
        end = text.index('?>', text.index('mysql_query', start)) + 2
        text = text[:start] + EDIT_USER_V1.replace('\n', '\n\t') + text[end:]
    if stem in ('modal_add_user', 'modal_edit_user'):  # form tự gửi về users.php, kiểm token ở khối xử lý phía trên
        text = sub1(text, '<form class="form-horizontal" method="post">',
                    '<form class="form-horizontal" method="post"><?php echo csrf_field(); ?>')
    if stem == 'users':  # CWE-256: không hiển thị mật khẩu
        text = sub1(text, "<td><?php echo $row['password']; ?></td>", '<td>********</td>')
    if stem == 'header':
        text = sub1(text, "<?php include('dbcon.php'); ?>", "<?php require_once __DIR__ . '/dbcon.php'; ?>")
    if stem in HANDLERS:  # CWE-306, CWE-352: guard trước CSDL, chỉ nhận POST
        text = sub1(text, "include('dbcon.php');", "require_once __DIR__ . '/auth_guard.php';")
        text = text.replace('$_GET[', '$_POST[')
    if stem == 'borrow_save':
        start = text.index('\tmysql_query("insert into borrow ')
        end = text.index('header("location: borrow.php");\n}')
        text = text[:start] + BORROW_V1 + text[end:]
        text = sub1(text, "$id=$_POST['selector'];", "$id=$_POST['selector'] ?? '';")
    if stem in CONFIRM_MODALS:  # CWE-352: nút Yes thành form POST (token chèn ở bước form bên dưới)
        text = re.sub(r'<a class="(btn btn-\w+)" href="(\w+\.php)<\?php echo \'\?id=\'\.\$id; \?>">(.*?)</a>',
                      r'<form method="post" action="\2" style="display:inline">'
                      r'<input type="hidden" name="id" value="<?php echo e((int) $id); ?>">'
                      r'<button type="submit" class="\1">\3</button></form>', text)
    if stem == 'modal_return':
        text = sub1(text, """<a class="btn btn-success" href="return_save.php<?php echo '?id='.$id; ?>&<?php echo 'book_id='.$book_id; ?>">Yes</a>""",
                    '<form method="post" action="return_save.php" style="display:inline">'
                    '<input type="hidden" name="id" value="<?php echo e((int) $id); ?>">'
                    '<input type="hidden" name="book_id" value="<?php echo e((int) $book_id); ?>">'
                    '<button type="submit" class="btn btn-success">Yes</button></form>')
    # CWE-352: form gửi tới handler ghi dữ liệu mang token
    text = re.sub(r'(<form [^>]*action="(\w+)\.php"[^>]*>)',
                  lambda f: f[1] + '<?php echo csrf_field(); ?>' if f[2] in HANDLERS else f[1], text)
    if stem in LIST_PAGES:  # CWE-1050: tên danh mục và số bản đang mượn lấy trong cùng truy vấn danh sách
        pending = (", (select count(*) from borrowdetails where borrowdetails.book_id = book.book_id"
                   " and borrow_status = 'pending') as pending") if stem in ('books', 'advance_search') else ''
        text = sub1(text, 'mysql_query("select * from book where',
                    f'mysql_query("select book.*, category.classname{pending} from book'
                    ' left join category on category.category_id = book.category_id where')
        text = re.sub(r'\n[ \t]*\$cat_query = mysql_query\(.*', '', text)
        text = re.sub(r'\n[ \t]*\$cat_row = mysql_fetch_array\(.*', '', text)
        text = re.sub(r"\$cat_row ?\['classname'\]", "$row['classname']", text)
        if pending:
            text = re.sub(r'\$borrow_details = mysql_query\(.*\n[ \t]*\$row11 = .*\n[ \t]*\$count = mysql_num_rows\(\$borrow_details\);',
                          "$count = (int) $row['pending']; // v1 — CWE-1050: đếm trong cùng truy vấn danh sách", text)
    if stem in EDIT_PAGES:  # CWE-252: không đọc dòng khi bản ghi không tồn tại
        text = sub1(text, '$row=mysql_fetch_array($query);\n',
                    "$row=mysql_fetch_array($query);\n\t\tif (!$row) { exit('Không tìm thấy dữ liệu.'); } // v1 — CWE-252\n")
    text = QUERY.sub(to_db_query, text)
    for old, new in (('mysql_fetch_array', 'mysqli_fetch_array'), ('mysql_num_rows', 'mysqli_num_rows')):
        text = text.replace(old, new)
    return ECHO.sub(encode_echo, text)


def schema(text):
    """CWE-362: hai bảng mượn sang InnoDB; CWE-256: mật khẩu mẫu thành giá trị băm."""
    lines = text.split('\n')
    for n in (83, 107):  # borrow, borrowdetails
        assert 'ENGINE=MyISAM' in lines[n - 1], n
        lines[n - 1] = lines[n - 1].replace('ENGINE=MyISAM', 'ENGINE=InnoDB')
    return sub1('\n'.join(lines), "(2, 'admin', 'admin', 'john', 'smith');", f"(2, 'admin', '{ADMIN_HASH}', 'john', 'smith');")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / 'librarian').mkdir(parents=True)
    (OUT / 'db').mkdir()
    changed = []
    for f in sorted((SRC / 'librarian').glob('*.php')):
        old = f.read_text(encoding='utf-8', errors='surrogateescape')
        new = NEW_FILES.get(f.name) or patch(f.name, old)
        (OUT / 'librarian' / f.name).write_text(new, encoding='utf-8', errors='surrogateescape')
        changed += [f.name] * (new != old)
    for name in ('security.php', 'auth_guard.php'):
        (OUT / 'librarian' / name).write_text(NEW_FILES[name], encoding='utf-8')
    (OUT / 'db/eb_lms_v1.sql').write_text(schema((SRC / 'db/eb_lms.sql').read_text(encoding='utf-8')), encoding='utf-8')
    # Tự kiểm: không còn ext/mysql, không còn die(mysql_error()), mọi db_query có SQL là chuỗi hằng
    for f in (OUT / 'librarian').glob('*.php'):
        t = f.read_text(encoding='utf-8', errors='surrogateescape')
        assert not re.search(r'\bmysql_\w+\(', t), f.name
        for sql in re.findall(r'db_query\("((?:[^"\\]|\\.)*)"', t):
            assert '$' not in sql, (f.name, sql)
    print(f'source_v1: {len(changed)} tệp sửa, 2 tệp thêm (security.php, auth_guard.php), schema eb_lms_v1.sql')
    print('Tệp sửa:', ', '.join(changed))


if __name__ == '__main__':
    main()
