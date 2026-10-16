<?php
// SQL-37: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_37_v1(PDO $db, array $input): PDOStatement
{
    $username = sql_case_text(sql_case_present($input, 'username'), 100);
    $password = sql_case_text(sql_case_present($input, 'password'), 100);
    $firstname = sql_case_text(sql_case_present($input, 'firstname'), 100);
    $lastname = sql_case_text(sql_case_present($input, 'lastname'), 100);
    $user_id = sql_case_int(sql_case_present($input, 'user_id'), 1, 2147483647);
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("update users set username=:username, password=:password , firstname = :firstname , lastname = :lastname where user_id=:user_id");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->bindValue(':username', $username, PDO::PARAM_STR);
    $statement->bindValue(':password', $password, PDO::PARAM_STR);
    $statement->bindValue(':firstname', $firstname, PDO::PARAM_STR);
    $statement->bindValue(':lastname', $lastname, PDO::PARAM_STR);
    $statement->bindValue(':user_id', $user_id, PDO::PARAM_INT);
    $statement->execute();
    return $statement;
}
