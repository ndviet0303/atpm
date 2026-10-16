<?php
// SQL-21: delete_member.php:4-4.
// Query-only text example; never executed.
function sql_21_v0(array $input): mixed
{
    $id = $input['id'];
    return mysql_query("delete from member where member_id='$id'");
}
