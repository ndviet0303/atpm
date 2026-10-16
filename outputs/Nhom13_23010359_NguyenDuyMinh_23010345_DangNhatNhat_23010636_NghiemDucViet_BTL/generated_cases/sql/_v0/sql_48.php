<?php
// SQL-48: unstudents.php:29-29.
// Query-only text example; never executed.
function sql_48_v0(array $input): mixed
{
    return mysql_query("select * from students where status = 'unactive' ");
}
