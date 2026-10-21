<?php
// Intentionally unsafe generated experiment. It is absent from the baseline.
// Mirrors login.php:4-12: the plaintext password is copied into the query and never wiped.
function login_v0(): bool
{
    $username = $_POST['username'];
    $password = $_POST['password'];
    $query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
    $result = mysql_query($query) or die(mysql_error());
    $row = mysql_fetch_array($result);
    $_SESSION['id'] = $row['user_id'];
    return mysql_num_rows($result) > 0;
}
