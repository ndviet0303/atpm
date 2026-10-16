<?php
// SQL-10: binding/guards only; caller must authorize.
require_once __DIR__ . '/../guards.php';
function sql_10_v1(PDO $db, array $input): PDOStatement
{
    $book_title = sql_case_text(sql_case_present($input, 'book_title'), 100);
    $category_id = sql_case_int(sql_case_present($input, 'category_id'), 1, 2147483647);
    $author = sql_case_text(sql_case_present($input, 'author'), 50);
    $book_copies = sql_case_int(sql_case_present($input, 'book_copies'), 0, 2147483647);
    $book_pub = sql_case_text(sql_case_present($input, 'book_pub'), 100);
    $publisher_name = sql_case_text(sql_case_present($input, 'publisher_name'), 100);
    $isbn = sql_case_text(sql_case_present($input, 'isbn'), 50);
    $copyright_year = sql_case_int(sql_case_present($input, 'copyright_year'), 0, 2147483647);
    $status = sql_case_text(sql_case_present($input, 'status'), 30);
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $statement = $db->prepare("insert into book (book_title,category_id,author,book_copies,book_pub,publisher_name,isbn,copyright_year,date_added,status) values(:book_title,:category_id,:author,:book_copies,:book_pub,:publisher_name,:isbn,:copyright_year,NOW(),:status)");
    if ($statement === false) {
        throw new RuntimeException('Preparation failed');
    }
    $statement->bindValue(':book_title', $book_title, PDO::PARAM_STR);
    $statement->bindValue(':category_id', $category_id, PDO::PARAM_INT);
    $statement->bindValue(':author', $author, PDO::PARAM_STR);
    $statement->bindValue(':book_copies', $book_copies, PDO::PARAM_INT);
    $statement->bindValue(':book_pub', $book_pub, PDO::PARAM_STR);
    $statement->bindValue(':publisher_name', $publisher_name, PDO::PARAM_STR);
    $statement->bindValue(':isbn', $isbn, PDO::PARAM_STR);
    $statement->bindValue(':copyright_year', $copyright_year, PDO::PARAM_INT);
    $statement->bindValue(':status', $status, PDO::PARAM_STR);
    $statement->execute();
    return $statement;
}
