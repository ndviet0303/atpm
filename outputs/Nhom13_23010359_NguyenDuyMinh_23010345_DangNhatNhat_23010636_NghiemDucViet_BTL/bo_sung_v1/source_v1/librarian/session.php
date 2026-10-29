<?php
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
?>