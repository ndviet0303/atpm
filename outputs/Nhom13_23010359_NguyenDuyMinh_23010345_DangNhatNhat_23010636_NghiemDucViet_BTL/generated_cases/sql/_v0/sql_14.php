<?php
// SQL-14: borrow_save.php:17-17.
// Query-only text example; never executed.
function sql_14_v0(array $input): mixed
{
    $member_id = $input['member_id'];
    $due_date = $input['due_date'];
    return mysql_query("insert into borrow (member_id,date_borrow,due_date) values ('$member_id',NOW(),'$due_date')");
}
