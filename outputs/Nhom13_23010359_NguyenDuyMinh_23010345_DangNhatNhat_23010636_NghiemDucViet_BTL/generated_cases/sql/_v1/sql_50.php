<?php
// SQL-50: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_50_v1(PDO $db, array $input): PDOStatement
{
    $firstname = sql_case_text(sql_case_present($input, 'firstname'), 100);
    $lastname = sql_case_text(sql_case_present($input, 'lastname'), 100);
    $gender = sql_case_text(sql_case_present($input, 'gender'), 10);
    $address = sql_case_text(sql_case_present($input, 'address'), 100);
    $contact = sql_case_text(sql_case_present($input, 'contact'), 100);
    $type = sql_case_text(sql_case_present($input, 'type'), 100);
    $year_level = sql_case_text(sql_case_present($input, 'year_level'), 100);
    $status = sql_case_text(sql_case_present($input, 'status'), 100);
    $id = sql_case_int(sql_case_present($input, 'id'), 1, 2147483647);
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("update member set firstname=:firstname,lastname=:lastname,gender=:gender,address = :address,contact = :contact,type = :type,year_level = :year_level,status = :status where member_id=:id");
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
    $statement->bindValue(':status', $status, PDO::PARAM_STR);
    $statement->bindValue(':id', $id, PDO::PARAM_INT);
    $statement->execute();
    return $statement;
}
