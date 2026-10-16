<?php
// SQL-28: edit_student.php:58-58.
// Query-only text example; never executed.
function sql_28_v0(array $input): mixed
{
    $get_id = $input['get_id'];
    return mysql_query("select * from member where member_id='$get_id'");
}
