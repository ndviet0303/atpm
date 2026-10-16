<?php
// SQL-04: advance_search.php:73-73.
// Query-only text example; never executed.
function sql_04_v0(array $input): mixed
{
    $cat_id = $input['cat_id'];
    return mysql_query("select * from category where category_id = '$cat_id'");
}
