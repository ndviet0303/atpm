<?php
// SQL-13: borrow.php:66-66.
// Query-only text example; never executed.
function sql_13_v0(array $input): mixed
{
    $cat_id = $input['cat_id'];
    return mysql_query("select * from category where category_id = '$cat_id'");
}
