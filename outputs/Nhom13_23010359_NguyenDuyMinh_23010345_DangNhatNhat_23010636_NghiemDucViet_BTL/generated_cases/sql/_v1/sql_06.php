<?php
// SQL-06: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_06_v1(PDO $db, array $input): PDOStatement
{
    $cat_id = sql_case_int(sql_case_present($input, 'cat_id'), 1, 2147483647);
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("select * from category where category_id = :cat_id");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->bindValue(':cat_id', $cat_id, PDO::PARAM_INT);
    $statement->execute();
    return $statement;
}
