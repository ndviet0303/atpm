<?php
// SQL-31: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_31_v1(PDO $db, array $input): PDOStatement
{
    $username = sql_case_text(sql_case_present($input, 'username'), 100);
    $password = sql_case_text(sql_case_present($input, 'password'), 100);
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("SELECT * FROM users WHERE username=:username AND password=:password");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->bindValue(':username', $username, PDO::PARAM_STR);
    $statement->bindValue(':password', $password, PDO::PARAM_STR);
    $statement->execute();
    return $statement;
}
