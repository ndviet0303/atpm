<?php
// SQL-37: modal_edit_user.php:53-53.
// Query-only text example; never executed.
function sql_37_v0(array $input): mixed
{
    $username = $input['username'];
    $password = $input['password'];
    $firstname = $input['firstname'];
    $lastname = $input['lastname'];
    $user_id = $input['user_id'];
    return mysql_query("update users set username='$username', password='$password' , firstname = '$firstname' , lastname = '$lastname'  where user_id='$user_id'");
}
