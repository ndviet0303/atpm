<?php
// SQL-03: advance_search.php:65-65.
// Query-only text example; never executed.
function sql_03_v0(array $input): mixed
{
    $id = $input['id'];
    return mysql_query("select * from borrowdetails where book_id = '$id' and borrow_status = 'pending'");
}
