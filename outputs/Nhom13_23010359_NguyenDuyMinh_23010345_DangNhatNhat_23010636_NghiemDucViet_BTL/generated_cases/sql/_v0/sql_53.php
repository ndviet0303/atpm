<?php
// SQL-53: view_borrow.php:24-29.
// Query-only text example; never executed.
function sql_53_v0(array $input): mixed
{
    return mysql_query("select * from borrow
								LEFT JOIN member ON borrow.member_id = member.member_id
								LEFT JOIN borrowdetails ON borrow.borrow_id = borrowdetails.borrow_id
								LEFT JOIN book on borrowdetails.book_id =  book.book_id 
								ORDER BY borrow.borrow_id DESC
								  ");
}
