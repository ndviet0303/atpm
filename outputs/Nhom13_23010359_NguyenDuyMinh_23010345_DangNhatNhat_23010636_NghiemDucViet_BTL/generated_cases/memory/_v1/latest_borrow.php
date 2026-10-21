<?php
// Generated correction: LIMIT 1 bounds the buffer, the row is checked before it is read.
function latest_borrow_id_v1(PDO $db): ?int
{
    $stmt = $db->query('SELECT borrow_id FROM borrow ORDER BY borrow_id DESC LIMIT 1');
    $row = $stmt->fetch(PDO::FETCH_ASSOC);
    $stmt->closeCursor();
    if (!is_array($row)) {
        return null;
    }
    return (int) $row['borrow_id'];
}
