<?php
// SQL-24: edit_book.php:10-10.
// Query-only text example; never executed.
function sql_24_v0(array $input): mixed
{
    $get_id = $input['get_id'];
    return mysql_query("select * from book LEFT JOIN category on category.category_id  = book.category_id where book_id='$get_id'");
}
