<?php
// SQL-36: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_36_v1(PDO $db, array $input): PDOStatement
{
    $username = sql_case_text(sql_case_present($input, 'username'), 100);
    $password = sql_case_text(sql_case_present($input, 'password'), 100);
    $firstname = sql_case_text(sql_case_present($input, 'firstname'), 100);
    $lastname = sql_case_text(sql_case_present($input, 'lastname'), 100);
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("insert into users (username,password,firstname,lastname) values(:username,:password,:firstname,:lastname)");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->bindValue(':username', $username, PDO::PARAM_STR);
    $statement->bindValue(':password', $password, PDO::PARAM_STR);
    $statement->bindValue(':firstname', $firstname, PDO::PARAM_STR);
    $statement->bindValue(':lastname', $lastname, PDO::PARAM_STR);
    $statement->execute();
    return $statement;
}
