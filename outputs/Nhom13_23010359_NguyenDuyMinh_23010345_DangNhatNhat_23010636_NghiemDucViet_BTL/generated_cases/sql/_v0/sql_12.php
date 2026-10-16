<?php
// SQL-12: borrow.php:61-61.
// Query-only text example; never executed.
function sql_12_v0(array $input): mixed
{
    return mysql_query("select * from book where status != 'Archive' ");
}
