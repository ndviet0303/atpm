<?php
// SQL-08: books.php:61-61.
// Query-only text example; never executed.
function sql_08_v0(array $input): mixed
{
    $id = $input['id'];
    return mysql_query("select * from borrowdetails where book_id = '$id' and borrow_status = 'pending'");
}
