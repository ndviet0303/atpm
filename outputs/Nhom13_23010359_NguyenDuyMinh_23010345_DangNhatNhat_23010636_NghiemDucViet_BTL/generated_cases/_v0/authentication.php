<?php
// Generated educational case. Do not deploy or execute against a database.
function authenticate_v0(string $username, string $password): array|false
{
    $query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
    $result = mysql_query($query);
    return mysql_num_rows($result) > 0 ? mysql_fetch_array($result) : false;
}
