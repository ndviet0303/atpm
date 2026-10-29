<?php 
require_once __DIR__ . '/auth_guard.php';
if (isset($_POST['submit'])){
$id=$_POST['id'];
$book_title=$_POST['book_title'];
$category_id=$_POST['category_id'];
$author=$_POST['author'];
$book_copies=$_POST['book_copies'];
$book_pub=$_POST['book_pub'];
$publisher_name=$_POST['publisher_name'];
$isbn=$_POST['isbn'];
$copyright_year=$_POST['copyright_year'];
/* $date_receive=$_POST['date_receive'];
$date_added=$_POST['date_added']; */
$status=$_POST['status'];




db_query("update book set book_title=?,category_id=?,author=?
,book_copies = ?,book_pub = ?,publisher_name = ?,isbn = ?,copyright_year=?,status=? where book_id=?", "sisssssssi", $book_title, $category_id, $author, $book_copies, $book_pub, $publisher_name, $isbn, $copyright_year, $status, $id);
								
								
 header('location:books.php');
}
?>	