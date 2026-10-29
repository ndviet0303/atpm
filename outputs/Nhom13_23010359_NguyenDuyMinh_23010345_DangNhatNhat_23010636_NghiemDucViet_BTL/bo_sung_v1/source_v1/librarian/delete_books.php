<?php
require_once __DIR__ . '/auth_guard.php';
$id=$_POST['id'];
db_query("update book set status = 'Archive' where book_id=?", "i", $id);
header('location:books.php');
?>