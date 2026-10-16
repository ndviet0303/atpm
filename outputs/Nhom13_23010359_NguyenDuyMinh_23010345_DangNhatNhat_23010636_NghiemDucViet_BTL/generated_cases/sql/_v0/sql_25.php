<?php
// SQL-25: edit_book.php:32-32.
// Query-only text example; never executed.
function sql_25_v0(array $input): mixed
{
    $category_id = $input['category_id'];
    return mysql_query("select * from category where category_id != '$category_id'");
}
