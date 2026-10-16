<?php
// A query example only. Caller still needs authorization and CSRF checks.
function delete_book_v1(PDO $db, string $rawId): void
{
    $id = filter_var($rawId, FILTER_VALIDATE_INT, ['options' => ['min_range' => 1]]);
    if ($id === false) {
        throw new InvalidArgumentException('Invalid book identifier');
    }
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $stmt = $db->prepare('DELETE FROM book WHERE book_id = :id');
    $stmt->bindValue(':id', $id, PDO::PARAM_INT);
    $stmt->execute();
}
