	<?php
 	require_once __DIR__ . '/auth_guard.php';
	
		$id=$_POST['selector'] ?? '';
 	$member_id  = $_POST['member_id'];
	$due_date  = $_POST['due_date'];

	if ($id == '' ){ 
	header("location: borrow.php");
	?>
	

	<?php }else{
	


	// v1 — CWE-362: phiếu và chi tiết trong một giao dịch InnoDB; ID lấy từ chính kết nối này.
	mysqli_begin_transaction($conn);
	db_query("insert into borrow (member_id,date_borrow,due_date) values (?,NOW(),?)", "is", $member_id, $due_date);
	$borrow_id = mysqli_insert_id($conn);
	foreach ($id as $book_id) {
	    db_query("insert into borrowdetails (book_id,borrow_id,borrow_status) values(?,?,'pending')", "ii", (int) $book_id, $borrow_id);
	}
	mysqli_commit($conn);
header("location: borrow.php");
}  
?>
	
	

	
	