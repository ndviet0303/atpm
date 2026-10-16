<?php
// SQL-14: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_14_v1(PDO $db, array $input): PDOStatement
{
    $member_id = sql_case_int(sql_case_present($input, 'member_id'), 1, 2147483647);
    $due_date = sql_case_text(sql_case_present($input, 'due_date'), 100);
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("insert into borrow (member_id,date_borrow,due_date) values (:member_id,NOW(),:due_date)");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->bindValue(':member_id', $member_id, PDO::PARAM_INT);
    $statement->bindValue(':due_date', $due_date, PDO::PARAM_STR);
    $statement->execute();
    return $statement;
}
