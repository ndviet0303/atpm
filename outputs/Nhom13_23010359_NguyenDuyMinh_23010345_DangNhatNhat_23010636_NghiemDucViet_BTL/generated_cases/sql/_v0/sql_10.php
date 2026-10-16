<?php
// SQL-10: books_save.php:20-21.
// Query-only text example; never executed.
function sql_10_v0(array $input): mixed
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
    return mysql_query("insert into book (book_title,category_id,author,book_copies,book_pub,publisher_name,isbn,copyright_year,date_added,status)
 values('$book_title','$category_id','$author','$book_copies','$book_pub','$publisher_name','$isbn','$copyright_year',NOW(),'$status')");
}
