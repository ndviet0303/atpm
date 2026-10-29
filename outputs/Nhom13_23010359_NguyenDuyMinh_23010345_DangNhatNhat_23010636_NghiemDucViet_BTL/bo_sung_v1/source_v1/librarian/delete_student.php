<?php
require_once __DIR__ . '/auth_guard.php';
$id=$_POST['id'];
db_query("delete from member where member_id=?", "i", $id);
header('location:member.php');
?>