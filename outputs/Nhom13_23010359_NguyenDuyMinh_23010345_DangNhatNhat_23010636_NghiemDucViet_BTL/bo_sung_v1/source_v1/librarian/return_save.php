<?php 
require_once __DIR__ . '/auth_guard.php';

$id=$_POST['id'];
$book_id = $_POST['book_id'];

db_query("update borrow LEFT JOIN borrowdetails on borrow.borrow_id = borrowdetails.borrow_id   set borrow_status='returned',date_return= NOW() where borrow.borrow_id=? and borrowdetails.book_id = ?", "ii", $id, $book_id);						
 header('location:view_borrow.php');

?>	