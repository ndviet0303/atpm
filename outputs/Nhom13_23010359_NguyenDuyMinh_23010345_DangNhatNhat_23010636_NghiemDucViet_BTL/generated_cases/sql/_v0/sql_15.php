<?php
// SQL-15: borrow_save.php:18-18.
// Query-only text example; never executed.
function sql_15_v0(array $input): mixed
{
    return mysql_query("select * from borrow order by borrow_id DESC");
}
