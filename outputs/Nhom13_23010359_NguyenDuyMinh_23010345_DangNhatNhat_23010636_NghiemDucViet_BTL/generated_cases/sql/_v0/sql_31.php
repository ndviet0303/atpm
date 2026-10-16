<?php
// SQL-31: login.php:7-7.
// Query-only text example; never executed.
function sql_31_v0(array $input): mixed
{
    $username = $input['username'];
    $password = $input['password'];
    return mysql_query("SELECT * FROM users WHERE username='$username' AND password='$password'");
}
