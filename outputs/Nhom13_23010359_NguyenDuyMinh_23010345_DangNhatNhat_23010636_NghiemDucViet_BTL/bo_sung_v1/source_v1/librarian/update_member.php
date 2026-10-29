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
$status=$_POST['status'];

db_query("update member set firstname=?,lastname=?,gender=?,address = ?,contact = ?,type = ?,year_level = ?,status = ? where member_id=?", "ssssssssi", $firstname, $lastname, $gender, $address, $contact, $type, $year_level, $status, $id);
								
								
header('location:member.php');
}
?>	