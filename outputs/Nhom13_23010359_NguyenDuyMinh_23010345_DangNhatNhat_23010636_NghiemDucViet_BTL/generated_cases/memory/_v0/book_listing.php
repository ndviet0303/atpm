<?php
// Intentionally unsafe generated experiment. It is absent from the baseline.
// Mirrors books.php:55-75: unbounded SELECT, one extra query per row, unchecked result and row.
function list_books_v0(): void
{
    $user_query = mysql_query("select * from book where status != 'Archive'") or die(mysql_error());
    while ($row = mysql_fetch_array($user_query)) {
        $id = $row['book_id'];
        $borrow_details = mysql_query("select * from borrowdetails where book_id = '$id' and borrow_status = 'pending'");
        $row11 = mysql_fetch_array($borrow_details);
        $cat_id = $row['category_id'];
        $cat_query = mysql_query("select * from category where category_id = '$cat_id'") or die(mysql_error());
        $cat_row = mysql_fetch_array($cat_query);
        echo $row['book_title'], $cat_row['classname'], $row11['borrow_status'];
    }
}
