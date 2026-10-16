<?php
// SQL-33: lost.php:53-53.
// Query-only text example; never executed.
function sql_33_v0(array $input): mixed
{
    $cat_id = $input['cat_id'];
    return mysql_query("select * from category where category_id = '$cat_id'");
}
