<?php
// SQL-29: edit_student.php:77-77.
// Query-only text example; never executed.
function sql_29_v0(array $input): mixed
{
    $get_id = $input['get_id'];
    return mysql_query("select * from member where member_id='$get_id'");
}
