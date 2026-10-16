<?php
// SQL-09: books.php:69-69.
// Query-only text example; never executed.
function sql_09_v0(array $input): mixed
{
    $cat_id = $input['cat_id'];
    return mysql_query("select * from category where category_id = '$cat_id'");
}
