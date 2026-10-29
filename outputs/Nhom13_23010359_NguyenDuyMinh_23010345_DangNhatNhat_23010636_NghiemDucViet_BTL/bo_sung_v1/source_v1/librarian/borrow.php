<?php include('header.php'); ?>
<?php include('session.php'); ?>
<?php include('navbar_borrow.php'); ?>
    <div class="container">
		<div class="margin-top">
			<div class="row">	
								<div class="alert alert-danger">
                                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                                    <strong><i class="icon-user icon-large"></i>&nbsp;Borrow Table</strong>
                                </div>

		<div class="span12">		

		<form method="post" action="borrow_save.php"><?php echo csrf_field(); ?>
<div class="span3">

											<div class="control-group">
				<label class="control-label" for="inputEmail">Borrower Name</label>
				<div class="controls">
				<select name="member_id" class="chzn-select"required/>
				<option></option>
				<?php $result =  db_query("select * from member"); 
				while ($row=mysqli_fetch_array($result)){ ?>
				<option value="<?php echo e($row['member_id']); ?>"><?php echo e($row['firstname']." ".$row['lastname']); ?></option>
				<?php } ?>
				</select>
				</div>
			</div>
				<div class="control-group"> 
					<label class="control-label" for="inputEmail">Due Date</label>
					<div class="controls">
					<input type="text"  class="w8em format-d-m-y highlight-days-67 range-low-today" name="due_date" id="sd" maxlength="10" style="border: 3px double #CCCCCC;" required/>
					</div>
				</div>
				<div class="control-group"> 
					<div class="controls">

								<button name="delete_student" class="btn btn-default">Borrow</button>
					</div>
				</div>
				</div>
				<div class="span8">
						<div class="alert alert-success"><strong>Select Book</strong></div>
                            <table cellpadding="0" cellspacing="0" border="0" class="table" id="example">

                                <thead>
                                    <tr>
                       
                                        <th>Acc No.</th>                                 
                                        <th>Book title</th>                                 
                                        <th>Category</th>
										<th>Author</th>
										<th>Publisher name</th>
										<th>status</th>
										<th>Add</th>
										
                                    </tr>
                                </thead>
                                <tbody>
								 
                                  <?php  $user_query=db_query("select book.*, category.classname from book left join category on category.category_id = book.category_id where status != 'Archive' ");
									while($row=mysqli_fetch_array($user_query)){
									$id=$row['book_id'];  
									$cat_id=$row['category_id'];

									?>
									<tr class="del<?php echo e((int) $id); ?>">
									
									                              
                                    <td><?php echo e($row['book_id']); ?></td>
                                    <td><?php echo e($row['book_title']); ?></td>
									<td><?php echo e($row['classname']); ?> </td> 
                                    <td><?php echo e($row['author']); ?> </td> 
									 <td><?php echo e($row['publisher_name']); ?></td>
									  <td width=""><?php echo e($row['status']); ?></td> 
									<?php include('toolttip_edit_delete.php'); ?>
                                    <td width="20">
												<input id="" class="uniform_on" name="selector[]" type="checkbox" value="<?php echo e((int) $id); ?>" >
												
                                    </td>
									
                                    </tr>
									<?php  }  ?>
                                </tbody>
                            </table>
							
			    </form>
			</div>		
			</div>		
<script>		
$(".uniform_on").change(function(){
    var max= 3;
    if( $(".uniform_on:checked").length == max ){
	
        $(".uniform_on").attr('disabled', 'disabled');
		         alert('3 Books are allowed per borrow');
        $(".uniform_on:checked").removeAttr('disabled');
		
    }else{

         $(".uniform_on").removeAttr('disabled');
    }
})
</script>		
			</div>
		</div>
    </div>
<?php include('footer.php') ?>