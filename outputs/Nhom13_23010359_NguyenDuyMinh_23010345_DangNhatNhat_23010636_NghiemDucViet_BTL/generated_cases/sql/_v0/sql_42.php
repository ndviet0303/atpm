<?php
// SQL-42: return.php:26-31.
// Query-only text example; never executed.
function sql_42_v0(array $input): mixed
{
    return mysql_query("select * from borrow
								LEFT JOIN member ON borrow.member_id = member.member_id
								LEFT JOIN borrowdetails ON borrow.borrow_id = borrowdetails.borrow_id
								LEFT JOIN book on borrowdetails.book_id =  book.book_id 
								where borrowdetails.borrow_status = 'returned'ORDER BY borrow.borrow_id DESC
								  ");
}
