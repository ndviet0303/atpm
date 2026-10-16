<?php
// SQL-16: borrow_save.php:26-26.
// Query-only text example; never executed.
function sql_16_v0(array $input): mixed
{
    $selector_item = $input['selector_item'];
    $borrow_id = $input['borrow_id'];
    return mysql_query("insert borrowdetails (book_id,borrow_id,borrow_status) values('$selector_item','$borrow_id','pending')");
}
