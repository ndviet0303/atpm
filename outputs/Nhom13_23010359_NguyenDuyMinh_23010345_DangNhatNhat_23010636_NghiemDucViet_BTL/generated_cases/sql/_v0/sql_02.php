<?php
// SQL-02: advance_search.php:58-59.
// Query-only text example; never executed.
function sql_02_v0(array $input): mixed
{
    $title = $input['title'];
    $author = $input['author'];
    return mysql_query("select * from book where status != 'Archive' and book_title LIKE  '%$title%'
								  OR status != 'Archive' and author LIKE '%$author%'");
}
