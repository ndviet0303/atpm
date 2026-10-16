<?php
// SQL-40: old_books.php:48-48.
// Query-only text example; never executed.
function sql_40_v0(array $input): mixed
{
    return mysql_query("select * from book where status = 'old'");
}
