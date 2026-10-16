<?php
// SQL-54: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_54_v1(PDO $db, array $input): PDOStatement
{
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("select * from borrow LEFT JOIN member ON borrow.member_id = member.member_id LEFT JOIN borrowdetails ON borrow.borrow_id = borrowdetails.borrow_id LEFT JOIN book on borrowdetails.book_id = book.book_id ORDER BY borrow.borrow_id DESC");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->execute();
    return $statement;
}
