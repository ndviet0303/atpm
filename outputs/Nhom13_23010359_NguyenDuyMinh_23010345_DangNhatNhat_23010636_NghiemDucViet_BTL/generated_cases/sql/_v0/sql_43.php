<?php
// SQL-43: return_save.php:7-7.
// Query-only text example; never executed.
function sql_43_v0(array $input): mixed
{
    $id = $input['id'];
    $book_id = $input['book_id'];
    return mysql_query("update borrow LEFT JOIN borrowdetails on borrow.borrow_id = borrowdetails.borrow_id   set borrow_status='returned',date_return= NOW() where borrow.borrow_id='$id' and borrowdetails.book_id = '$book_id'");
}
