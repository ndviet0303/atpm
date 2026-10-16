<?php
// SQL-22: delete_student.php:4-4.
// Query-only text example; never executed.
function sql_22_v0(array $input): mixed
{
    $id = $input['id'];
    return mysql_query("delete from member where member_id='$id'");
}
