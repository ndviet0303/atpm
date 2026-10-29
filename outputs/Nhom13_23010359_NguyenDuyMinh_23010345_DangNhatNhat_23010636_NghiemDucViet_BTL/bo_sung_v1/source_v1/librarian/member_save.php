<?php 
require_once __DIR__ . '/auth_guard.php';
if (isset($_POST['submit'])){
$firstname=$_POST['firstname'];
$lastname=$_POST['lastname'];
$gender=$_POST['gender'];
$address=$_POST['address'];
$contact=$_POST['contact'];
$type=$_POST['type'];
$year_level=$_POST['year_level'];



								
db_query("insert into member(firstname,lastname,gender,address,contact,type,year_level) values(?,?,?,?,?,?,?)", "sssssss", $firstname, $lastname, $gender, $address, $contact, $type, $year_level);
 
 
header('location:member.php');
}
?>	