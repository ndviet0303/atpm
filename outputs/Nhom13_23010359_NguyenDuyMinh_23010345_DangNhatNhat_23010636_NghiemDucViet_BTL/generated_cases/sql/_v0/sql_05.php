<?php
// SQL-05: archive.php:37-37.
// Query-only text example; never executed.
function sql_05_v0(array $input): mixed
{
    return mysql_query("select * from book where status = 'Archive'");
}
