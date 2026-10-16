<?php
// SQL-32: lost.php:48-48.
// Query-only text example; never executed.
function sql_32_v0(array $input): mixed
{
    return mysql_query("select * from book where status = 'lost'");
}
