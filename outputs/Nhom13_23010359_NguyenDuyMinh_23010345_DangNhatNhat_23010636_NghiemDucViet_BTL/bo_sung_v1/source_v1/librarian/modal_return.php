	<div id="delete_book<?php echo e((int) $borrow_details_id); ?>" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
		<div class="modal-body">
			<div class="alert alert-success">Do you want to Return this Book?</div>

		</div>
		<div class="modal-footer">
			<form method="post" action="return_save.php" style="display:inline"><?php echo csrf_field(); ?><input type="hidden" name="id" value="<?php echo e((int) $id); ?>"><input type="hidden" name="book_id" value="<?php echo e((int) $book_id); ?>"><button type="submit" class="btn btn-success">Yes</button></form>
			<button class="btn" data-dismiss="modal" aria-hidden="true"><i class="icon-remove icon-large"></i>&nbsp;Close</button>
		</div>
    </div>
	
