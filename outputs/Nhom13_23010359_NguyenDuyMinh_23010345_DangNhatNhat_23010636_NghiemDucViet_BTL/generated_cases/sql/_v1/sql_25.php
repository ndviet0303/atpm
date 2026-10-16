<?php
// SQL-25: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_25_v1(PDO $db, array $input): PDOStatement
{
    $category_id = sql_case_int(sql_case_present($input, 'category_id'), 1, 2147483647);
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("select * from category where category_id != :category_id");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->bindValue(':category_id', $category_id, PDO::PARAM_INT);
    $statement->execute();
    return $statement;
}
