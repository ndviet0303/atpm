<?php
require_once __DIR__ . '/auth_guard.php';

$id=$_POST['id'];

db_query("delete from users where user_id=?", "i", $id);

header('location:users.php');
?>