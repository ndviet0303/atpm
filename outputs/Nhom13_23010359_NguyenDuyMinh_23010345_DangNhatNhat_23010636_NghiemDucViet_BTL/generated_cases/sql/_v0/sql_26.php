<?php
// SQL-26: edit_member.php:10-10.
// Query-only text example; never executed.
function sql_26_v0(array $input): mixed
{
    $get_id = $input['get_id'];
    return mysql_query("select * from member where member_id='$get_id'");
}
