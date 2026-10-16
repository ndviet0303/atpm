<?php
// SQL-02: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_02_v1(PDO $db, array $input): PDOStatement
{
    $title = sql_case_text(sql_case_present($input, 'title'), 100);
    $title = '%' . strtr($title, ['!' => '!!', '%' => '!%', '_' => '!_']) . '%';
    $author = sql_case_text(sql_case_present($input, 'author'), 50);
    $author = '%' . strtr($author, ['!' => '!!', '%' => '!%', '_' => '!_']) . '%';
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("select * from book where status != 'Archive' and book_title LIKE :title ESCAPE '!' OR status != 'Archive' and author LIKE :author ESCAPE '!'");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->bindValue(':title', $title, PDO::PARAM_STR);
    $statement->bindValue(':author', $author, PDO::PARAM_STR);
    $statement->execute();
    return $statement;
}
