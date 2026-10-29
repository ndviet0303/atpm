	<div id="delete_student<?php echo e((int) $id); ?>" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
		<div class="modal-body">
			<div class="alert alert-danger">Are you Sure yuo want to Delete this Data?</div>

		</div>
		<div class="modal-footer">
			<form method="post" action="delete_student.php" style="display:inline"><?php echo csrf_field(); ?><input type="hidden" name="id" value="<?php echo e((int) $id); ?>"><button type="submit" class="btn btn-danger">Yes</button></form>
			<button class="btn" data-dismiss="modal" aria-hidden="true"><i class="icon-remove icon-large"></i>&nbsp;Close</button>
		</div>
    </div>
	
