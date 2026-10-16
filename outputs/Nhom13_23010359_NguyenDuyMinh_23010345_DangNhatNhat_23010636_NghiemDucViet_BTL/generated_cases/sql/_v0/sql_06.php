<?php
// SQL-06: archive.php:42-42.
// Query-only text example; never executed.
function sql_06_v0(array $input): mixed
{
    $cat_id = $input['cat_id'];
    return mysql_query("select * from category where category_id = '$cat_id'");
}
