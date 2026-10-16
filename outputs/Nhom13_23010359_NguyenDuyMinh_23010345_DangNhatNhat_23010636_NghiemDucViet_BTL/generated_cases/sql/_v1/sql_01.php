<?php
// SQL-01: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_01_v1(PDO $db, array $input): PDOStatement
{
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("select * from category");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->execute();
    return $statement;
}
