<?php
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
?>