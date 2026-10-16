<?php
// SQL-20: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_20_v1(PDO $db, array $input): PDOStatement
{
    $id = sql_case_int(sql_case_present($input, 'id'), 1, 2147483647);
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("update book set status = 'Archive' where book_id=:id");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->bindValue(':id', $id, PDO::PARAM_INT);
    $statement->execute();
    return $statement;
}
