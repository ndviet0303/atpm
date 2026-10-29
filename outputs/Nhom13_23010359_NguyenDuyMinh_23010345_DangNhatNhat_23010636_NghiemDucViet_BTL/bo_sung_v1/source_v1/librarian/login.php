	<?php
	if (isset($_POST['submit'])){
	start_secure_session();
	$username = $_POST['username'];
	$password = $_POST['password'];
	unset($_POST['password']); // v1 — CWE-316: chỉ còn một tham chiếu nên sodium_memzero xóa được chuỗi
	// v1 — CWE-89: tra cứu bằng tham số; CWE-256: so khớp băm bằng password_verify, không so sánh bản rõ trong SQL.
	$result = db_query("SELECT user_id, password FROM users WHERE username = ?", "s", $username);
	$row = mysqli_fetch_array($result);
	$ok = false;
	if ($row && password_verify($password, $row['password'])) {
	$ok = true;
	}
	sodium_memzero($password);
	if ($ok) {
	session_regenerate_id(true);
	$_SESSION['id']=$row['user_id'];
	header('location:dashboard.php');
	exit();
	}
	else{ ?>
	<div class="alert alert-danger">Access Denied</div>
	<?php
	}}
	?>