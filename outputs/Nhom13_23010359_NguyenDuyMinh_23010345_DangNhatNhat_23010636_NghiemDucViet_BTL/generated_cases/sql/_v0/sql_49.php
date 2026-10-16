<?php
// SQL-49: update_books.php:20-21.
// Query-only text example; never executed.
function sql_49_v0(array $input): mixed
{
    $book_title = $input['book_title'];
    $category_id = $input['category_id'];
    $author = $input['author'];
    $book_copies = $input['book_copies'];
    $book_pub = $input['book_pub'];
    $publisher_name = $input['publisher_name'];
    $isbn = $input['isbn'];
    $copyright_year = $input['copyright_year'];
    $status = $input['status'];
    $id = $input['id'];
    return mysql_query("update book set book_title='$book_title',category_id='$category_id',author='$author'
,book_copies = '$book_copies',book_pub = '$book_pub',publisher_name = '$publisher_name',isbn = '$isbn',copyright_year='$copyright_year',status='$status' where book_id='$id'");
}
