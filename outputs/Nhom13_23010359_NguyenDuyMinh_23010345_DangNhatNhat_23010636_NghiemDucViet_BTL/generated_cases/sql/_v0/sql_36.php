<?php
// SQL-36: modal_add_user.php:48-48.
// Query-only text example; never executed.
function sql_36_v0(array $input): mixed
{
    $username = $input['username'];
    $password = $input['password'];
    $firstname = $input['firstname'];
    $lastname = $input['lastname'];
    return mysql_query("insert into users (username,password,firstname,lastname) values('$username','$password','$firstname','$lastname')");
}
