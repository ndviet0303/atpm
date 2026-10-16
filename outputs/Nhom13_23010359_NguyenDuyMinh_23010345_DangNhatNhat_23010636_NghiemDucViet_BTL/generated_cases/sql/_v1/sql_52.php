<?php
// SQL-52: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_52_v1(PDO $db, array $input): PDOStatement
{
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("select * from users");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->execute();
    return $statement;
}
