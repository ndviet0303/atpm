<?php
// SQL-30: index.php:39-39.
// Query-only text example; never executed.
function sql_30_v0(array $input): mixed
{
    $username = $input['username'];
    $password = $input['password'];
    return mysql_query("SELECT * FROM users WHERE username='$username' AND password='$password'");
}
