<?php
// SQL-29: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_29_v1(PDO $db, array $input): PDOStatement
{
    $get_id = sql_case_int(sql_case_present($input, 'get_id'), 1, 2147483647);
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("select * from member where member_id=:get_id");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->bindValue(':get_id', $get_id, PDO::PARAM_INT);
    $statement->execute();
    return $statement;
}
