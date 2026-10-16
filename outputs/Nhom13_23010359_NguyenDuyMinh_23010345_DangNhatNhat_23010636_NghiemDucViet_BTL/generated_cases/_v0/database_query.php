<?php
// Generated case corresponding to the baseline CRUD query pattern.
function delete_book_v0(string $id): void
{
    $query = "DELETE FROM book WHERE book_id='$id'";
    mysql_query($query);
}
