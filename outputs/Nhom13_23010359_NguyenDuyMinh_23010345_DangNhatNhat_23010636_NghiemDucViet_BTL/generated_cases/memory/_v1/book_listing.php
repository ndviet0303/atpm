<?php
// Generated correction: one bounded page, one joined query, rows checked by fetchAll, cursor closed.
const BOOK_PAGE_SIZE_V1 = 50;

function list_books_v1(PDO $db, int $page): array
{
    $sql = 'SELECT b.book_id, b.book_title, c.classname, COUNT(d.borrow_details_id) AS pending
            FROM book b LEFT JOIN category c ON c.category_id = b.category_id
            LEFT JOIN borrowdetails d ON d.book_id = b.book_id AND d.borrow_status = \'pending\'
            WHERE b.status != \'Archive\' GROUP BY b.book_id ORDER BY b.book_id LIMIT 50 OFFSET :offset';
    $stmt = $db->prepare($sql);
    $stmt->bindValue(':offset', max(0, $page) * BOOK_PAGE_SIZE_V1, PDO::PARAM_INT);
    $stmt->execute();
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
    $stmt->closeCursor();
    $stmt = null;
    return $rows;
}
