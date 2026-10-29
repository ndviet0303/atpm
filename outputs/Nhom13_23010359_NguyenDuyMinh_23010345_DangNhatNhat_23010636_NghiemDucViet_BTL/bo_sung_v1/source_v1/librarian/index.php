<?php include('header.php'); ?>
<?php include('navbar.php'); ?>
    <div class="container">
		<div class="margin-top">
			<div class="row">	
			<div class="span12">
					<div class="sti">
						<img src="../LMS/vit.png" class="img-rounded">
					</div>
				<div class="login">
				<div class="log_txt">
				<p><strong>Please Enter the Details Below..</strong></p>
				</div>
						<form class="form-horizontal" method="POST">
								<div class="control-group">
									<label class="control-label" for="inputEmail">Username</label>
									<div class="controls">
									<input type="text" name="username" id="username" placeholder="Username" required>
									</div>
								</div>
								<div class="control-group">
									<label class="control-label" for="inputPassword">Password</label>
									<div class="controls">
									<input type="password" name="password" id="password" placeholder="Password" required>
								</div>
								</div>
								<div class="control-group">
									<div class="controls">
									<button id="login" name="submit" type="submit" class="btn"><i class="icon-signin icon-large"></i>&nbsp;Submit</button>
								</div>
								</div>
								
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
						</form>
				
				</div>
			</div>		
			</div>
		</div>
    </div>
<?php include('footer.php') ?>