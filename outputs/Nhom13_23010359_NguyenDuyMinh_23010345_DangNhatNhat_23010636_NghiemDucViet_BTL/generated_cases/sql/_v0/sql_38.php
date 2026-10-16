<?php
// SQL-38: new_books.php:48-48.
// Query-only text example; never executed.
function sql_38_v0(array $input): mixed
{
    return mysql_query("select * from book where status = 'new'");
}
