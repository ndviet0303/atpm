<?php
// Intentionally unsafe generated experiment. It is absent from the baseline.
// Mirrors borrow_save.php:18-20: buffers the whole borrow table to read one row, row not checked.
function latest_borrow_id_v0(): int
{
    $query = mysql_query("select * from borrow order by borrow_id DESC") or die(mysql_error());
    $row = mysql_fetch_array($query);
    return (int) $row['borrow_id'];
}
