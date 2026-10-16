<?php
// SQL-43: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_43_v1(PDO $db, array $input): PDOStatement
{
    $id = sql_case_int(sql_case_present($input, 'id'), 1, 2147483647);
    $book_id = sql_case_int(sql_case_present($input, 'book_id'), 1, 2147483647);
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("update borrow LEFT JOIN borrowdetails on borrow.borrow_id = borrowdetails.borrow_id set borrow_status='returned',date_return= NOW() where borrow.borrow_id=:id and borrowdetails.book_id = :book_id");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->bindValue(':id', $id, PDO::PARAM_INT);
    $statement->bindValue(':book_id', $book_id, PDO::PARAM_INT);
    $statement->execute();
    return $statement;
}
