<?php
// v1 — CWE-306, CWE-352: mọi handler ghi dữ liệu phải qua guard này trước khi chạm CSDL.
require_once __DIR__ . '/session.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !csrf_verify($_POST['csrf_token'] ?? '')) {
    http_response_code(403);
    exit('Yêu cầu không hợp lệ.');
}
require_once __DIR__ . '/dbcon.php';
?>