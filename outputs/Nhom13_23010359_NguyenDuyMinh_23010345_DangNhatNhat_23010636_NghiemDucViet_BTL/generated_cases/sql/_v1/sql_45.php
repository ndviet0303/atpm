<?php
// SQL-45: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_45_v1(PDO $db, array $input): PDOStatement
{
    $firstname = sql_case_text(sql_case_present($input, 'firstname'), 100);
    $lastname = sql_case_text(sql_case_present($input, 'lastname'), 100);
    $gender = sql_case_text(sql_case_present($input, 'gender'), 10);
    $address = sql_case_text(sql_case_present($input, 'address'), 100);
    $contact = sql_case_text(sql_case_present($input, 'contact'), 100);
    $type = sql_case_text(sql_case_present($input, 'type'), 100);
    $year_level = sql_case_text(sql_case_present($input, 'year_level'), 100);
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("insert into member(firstname,lastname,gender,address,contact,type,year_level) values(:firstname,:lastname,:gender,:address,:contact,:type,:year_level)");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->bindValue(':firstname', $firstname, PDO::PARAM_STR);
    $statement->bindValue(':lastname', $lastname, PDO::PARAM_STR);
    $statement->bindValue(':gender', $gender, PDO::PARAM_STR);
    $statement->bindValue(':address', $address, PDO::PARAM_STR);
    $statement->bindValue(':contact', $contact, PDO::PARAM_STR);
    $statement->bindValue(':type', $type, PDO::PARAM_STR);
    $statement->bindValue(':year_level', $year_level, PDO::PARAM_STR);
    $statement->execute();
    return $statement;
}
