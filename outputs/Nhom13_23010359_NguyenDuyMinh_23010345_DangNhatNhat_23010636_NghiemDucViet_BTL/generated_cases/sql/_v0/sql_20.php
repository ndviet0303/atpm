<?php
// SQL-20: delete_books.php:4-4.
// Query-only text example; never executed.
function sql_20_v0(array $input): mixed
{
    $id = $input['id'];
    return mysql_query("update book set status = 'Archive' where book_id='$id'");
}
