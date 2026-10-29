	<div id="add_user" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
		<div class="modal-body">
			<div class="alert alert-info"><strong>Add User</strong></div>
	<form class="form-horizontal" method="post"><?php echo csrf_field(); ?>
			<div class="control-group">
				<label class="control-label" for="inputEmail">Username</label>
				<div class="controls">
				<input type="text" id="inputEmail" name="username" placeholder="Username" required>
				</div>
			</div>
			<div class="control-group">
				<label class="control-label" for="inputPassword">Password</label>
				<div class="controls">
				<input type="password" name="password" id="inputPassword" placeholder="Password" required>
				</div>
			</div>
				<div class="control-group">
				<label class="control-label" for="inputEmail">Firstname</label>
				<div class="controls">
				<input type="text" id="inputEmail" name="firstname" placeholder="Username" required>
				</div>
			</div>
				<div class="control-group">
				<label class="control-label" for="inputEmail">Lastname</label>
				<div class="controls">
				<input type="text" id="inputEmail" name="lastname" placeholder="Username" required>
				</div>
			</div>
			<div class="control-group">
				<div class="controls">
				<button name="submit" type="submit" class="btn btn-success"><i class="icon-save icon-large"></i>&nbsp;Save</button>
				</div>
			</div>
    </form>
		</div>
		<div class="modal-footer">
			<button class="btn" data-dismiss="modal" aria-hidden="true"><i class="icon-remove icon-large"></i>&nbsp;Close</button>
		</div>
    </div>
	
	<?php
	if (isset($_POST['submit'])){
	if (!csrf_verify($_POST['csrf_token'] ?? '')) { http_response_code(403); exit('Yêu cầu không hợp lệ.'); }
	$username=$_POST['username'];
	// v1 — CWE-256: chỉ lưu giá trị băm thích ứng của mật khẩu.
	$plain_password=$_POST['password'];
	unset($_POST['password']); // v1 — CWE-316: chỉ còn một tham chiếu
	$password=password_hash($plain_password, PASSWORD_DEFAULT);
	sodium_memzero($plain_password);
	$firstname=$_POST['firstname'];
	$lastname=$_POST['lastname'];
	
	db_query("insert into users (username,password,firstname,lastname) values(?,?,?,?)", "ssss", $username, $password, $firstname, $lastname);
	}
	?>