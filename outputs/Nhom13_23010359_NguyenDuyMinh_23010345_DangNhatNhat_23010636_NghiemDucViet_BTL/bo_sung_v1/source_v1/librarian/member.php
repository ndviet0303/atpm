<?php include('header.php'); ?>
<?php include('session.php'); ?>
<?php include('navbar_member.php'); ?>
    <div class="container">
		<div class="margin-top">
			<div class="row">	
			<div class="span12">	
			   <div class="alert alert-danger">
                                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                                    <strong><i class="icon-user icon-large"></i>&nbsp;Member Table</strong>
                                </div>
                            <table cellpadding="0" cellspacing="0" border="0" class="table  table-bordered" id="example">
                             
								<p><a href="add_member.php" class="btn-default">&nbsp;Add Member</a></p>
							
                                <thead>
                                    <tr>
                       
                                        <th>Name</th>                                 
                                        <th>Gender</th>
										<th>Address</th>
										<th>Contact</th>
										<th>Type</th>
										<th>Year level</th>
										<th>Status</th>
										<th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
								 
                                  <?php  $user_query=db_query("select * from member");
									while($row=mysqli_fetch_array($user_query)){
									$id=$row['member_id'];  ?>
									<tr class="del<?php echo e((int) $id); ?>">
									
									                              
                                    <td><?php echo e($row['firstname']." ".$row['lastname']); ?></td>
                                    <td><?php echo e($row['gender']); ?> </td> 
                                    <td><?php echo e($row['address']); ?> </td>
                                    <td><?php echo e($row['contact']); ?></td>
									<td><?php echo e($row['type']); ?></td> 
									<td><?php echo e($row['year_level']); ?></td> 
									<td><?php echo e($row['status']); ?></td> 
									<?php include('toolttip_edit_delete.php'); ?>
                                    <td width="100">
									<div class="span2">
                                        <a rel="tooltip"  title="Delete" id="<?php echo e((int) $id); ?>" href="#delete_student<?php echo e((int) $id); ?>" data-toggle="modal"    class="btn-default"><i class="icon-trash icon-large"></i></a>
                                        <?php include('delete_student_modal.php'); ?>
										<div class="span1">
										<a  rel="tooltip"  title="Edit" id="e<?php echo e((int) $id); ?>" href="edit_member.php<?php echo e('?id=' . (int) $id); ?>" class="btn-default"><i class="icon-pencil icon-large"></i></a>
										</div></div>
                                    </td>
									
                                    </tr>
									<?php  }  ?>
                           
                                </tbody>
                            </table>
							
			
			</div>		
			</div>
		</div>
    </div>
<?php include('footer.php') ?>