<?php
// SQL-23: delete_user.php:6-6.
// Query-only text example; never executed.
function sql_23_v0(array $input): mixed
{
    $id = $input['id'];
    return mysql_query("delete from users where user_id='$id'");
}
