<?php
// SQL-08: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_08_v1(PDO $db, array $input): PDOStatement
{
    $id = sql_case_int(sql_case_present($input, 'id'), 1, 2147483647);
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("select * from borrowdetails where book_id = :id and borrow_status = 'pending'");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->bindValue(':id', $id, PDO::PARAM_INT);
    $statement->execute();
    return $statement;
}
