<?php include('header.php'); ?>
<?php include('session.php'); ?>
<?php include('navbar_books.php'); ?>
    <div class="container">
		<div class="margin-top">
			<div class="row">	
			<div class="span12">	
			   <div class="alert alert-danger">
                                    <button type="button" class="close" data-dismiss="alert">&times;</button>
                                    <strong><i class="icon-user icon-large"></i>&nbsp;Books Table</strong>
                                </div>
						<!--  -->
								    <ul class="nav nav-pills">
										<li><a href="books.php">All</a></li>
										<li><a href="new_books.php">New Books</a></li>
										<li><a href="old_books.php">Old Books</a></li>
										<li><a href="lost.php">Lost Books</a></li>
										<li><a href="damage.php">Damage Books</a></li>
										<li class="active"><a href="sub_rep.php">Subject for Replacement</a></li>
									</ul>
						<!--  -->
						<center class="title">
						<h1>Subject for Replacement</h1>
						</center>
                            <table cellpadding="0" cellspacing="0" border="0" class="table  table-bordered" id="example">
								<div class="pull-right">
								<a href="" onclick="window.print()" class="btn-default" >Print</a>
								</div>
								<p><a href="add_books.php" class="btn-default">&nbsp;Add Books</a></p>
							
                                <thead>
                                    <tr>
									    <th>Acc No.</th>                                 
                                        <th>Book Title</th>                                 
                                        <th>Category</th>
										<th>Author</th>
										<th class="action">copies</th>
										<th>Book Pub</th>
										<th>Publisher Name</th>
										<th>ISBN</th>
										<th>Copyright Year</th>
										<th>Date Added</th>
										<th class="action">Action</th>		
                                    </tr>
                                </thead>
                                <tbody>
								 
                                  <?php  $user_query=db_query("select book.*, category.classname from book left join category on category.category_id = book.category_id where status = 'Subject for Replacement'");
									while($row=mysqli_fetch_array($user_query)){
									$id=$row['book_id'];  
									$cat_id=$row['category_id'];

									?>
									<tr class="del<?php echo e((int) $id); ?>">
									
									                              
                                    <td><?php echo e($row['book_id']); ?></td>
                                    <td><?php echo e($row['book_title']); ?></td>
									<td><?php echo e($row['classname']); ?> </td>
                                    <td><?php echo e($row['author']); ?> </td> 
                                    <td class="action"><?php echo e($row['book_copies']); ?> </td>
                                     <td><?php echo e($row['book_pub']); ?></td>
									 <td><?php echo e($row['publisher_name']); ?></td>
									 <td><?php echo e($row['isbn']); ?></td>
									 <td><?php echo e($row['copyright_year']); ?></td>		
									 <td><?php echo e($row['date_added']); ?></td>
									<?php include('toolttip_edit_delete.php'); ?>
                                    <td class="action">
                                      <div class="span2">
                                        <a rel="tooltip"  title="Delete" id="<?php echo e((int) $id); ?>" href="#delete_book<?php echo e((int) $id); ?>" data-toggle="modal"    class="btn-default"><i class="icon-trash icon-large"></i></a>
                                        <?php include('delete_book_modal.php'); ?>
										<div class="span1">
										<a  rel="tooltip"  title="Edit" id="e<?php echo e((int) $id); ?>" href="edit_book.php<?php echo e('?id=' . (int) $id); ?>" class="btn-default"><i class="icon-pencil icon-large"></i></a>
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