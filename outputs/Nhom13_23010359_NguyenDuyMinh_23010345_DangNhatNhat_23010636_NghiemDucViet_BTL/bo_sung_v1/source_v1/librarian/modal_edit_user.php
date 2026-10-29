	<div id="edit<?php echo e((int) $id); ?>" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
		<div class="modal-body">
			<div class="alert alert-info"><strong>Edit User</strong></div>
	<form class="form-horizontal" method="post"><?php echo csrf_field(); ?>
			<div class="control-group">
				<label class="control-label" for="inputEmail">Username</label>
				<div class="controls">
				<input type="hidden" id="inputEmail" name="id" value="<?php echo e($row['user_id']); ?>" required>
				<input type="text" id="inputEmail" name="username" value="<?php echo e($row['username']); ?>" required>
				</div>
			</div>
			<div class="control-group">
				<label class="control-label" for="inputPassword">Password</label>
				<div class="controls">
				<input type="password" name="password" id="inputPassword" placeholder="Để trống nếu giữ mật khẩu cũ">
				</div>
			</div>
				<div class="control-group">
				<label class="control-label" for="inputEmail">Firstname</label>
				<div class="controls">
	
				<input type="text" id="inputEmail" name="firstname" value="<?php echo e($row['firstname']); ?>" required>
				</div>
			</div>
				<div class="control-group">
				<label class="control-label" for="inputEmail">Lastname</label>
				<div class="controls">

				<input type="text" id="inputEmail" name="lastname" value="<?php echo e($row['lastname']); ?>" required>
				</div>
			</div>
			<div class="control-group">
				<div class="controls">
				<button name="edit" type="submit" class="btn btn-success"><i class="icon-save icon-large"></i>&nbsp;Update</button>
				</div>
			</div>
    </form>
		</div>
		<div class="modal-footer">
			<button class="btn" data-dismiss="modal" aria-hidden="true"><i class="icon-remove icon-large"></i>&nbsp;Close</button>
		</div>
    </div>
	
	<?php
	if (isset($_POST['edit'])){
	if (!csrf_verify($_POST['csrf_token'] ?? '')) { http_response_code(403); exit('Yêu cầu không hợp lệ.'); }
	$user_id=$_POST['id'];
	$username=$_POST['username'];
	$firstname=$_POST['firstname'];
	$lastname=$_POST['lastname'];
	// v1 — CWE-256: chỉ lưu giá trị băm; để trống nghĩa là giữ mật khẩu cũ.
	$plain_password=$_POST['password'];
	unset($_POST['password']); // v1 — CWE-316: chỉ còn một tham chiếu
	if ($plain_password === '') {
	db_query("update users set username = ?, firstname = ?, lastname = ? where user_id = ?", "sssi", $username, $firstname, $lastname, $user_id);
	} else {
	$password=password_hash($plain_password, PASSWORD_DEFAULT);
	db_query("update users set username = ?, password = ?, firstname = ?, lastname = ? where user_id = ?", "ssssi", $username, $password, $firstname, $lastname, $user_id);
	}
	sodium_memzero($plain_password); ?>
	<script>
	window.location="users.php";
	</script>
	<?php
	}
	?>