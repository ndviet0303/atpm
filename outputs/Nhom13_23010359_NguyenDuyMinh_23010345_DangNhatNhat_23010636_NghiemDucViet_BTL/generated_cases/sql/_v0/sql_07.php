<?php
// SQL-07: books.php:55-55.
// Query-only text example; never executed.
function sql_07_v0(array $input): mixed
{
    return mysql_query("select * from book where status != 'Archive'");
}
