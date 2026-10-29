<?php 
require_once __DIR__ . '/auth_guard.php';
if (isset($_POST['submit'])){
$id=$_POST['id'];
$firstname=$_POST['firstname'];
$lastname=$_POST['lastname'];
$gender=$_POST['gender'];
$address=$_POST['address'];
$contact=$_POST['contact'];
$type=$_POST['type'];
$year_level=$_POST['year_level'];



db_query("update member set firstname=?,lastname=?,gender=?,address = ?,contact = ?,type = ?,year_level = ? where member_id=?", "sssssssi", $firstname, $lastname, $gender, $address, $contact, $type, $year_level, $id);
								
								
header('location:students.php');
}
?>	