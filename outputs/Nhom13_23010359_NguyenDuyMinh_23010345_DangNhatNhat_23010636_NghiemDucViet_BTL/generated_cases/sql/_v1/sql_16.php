<?php
// SQL-16: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_16_v1(PDO $db, array $input): PDOStatement
{
    $selector_item = sql_case_int(sql_case_present($input, 'selector_item'), 1, 2147483647);
    $borrow_id = sql_case_int(sql_case_present($input, 'borrow_id'), 1, 2147483647);
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("insert borrowdetails (book_id,borrow_id,borrow_status) values(:selector_item,:borrow_id,'pending')");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->bindValue(':selector_item', $selector_item, PDO::PARAM_INT);
    $statement->bindValue(':borrow_id', $borrow_id, PDO::PARAM_INT);
    $statement->execute();
    return $statement;
}
