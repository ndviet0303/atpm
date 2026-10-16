<?php
// SQL-50: update_member.php:14-14.
// Query-only text example; never executed.
function sql_50_v0(array $input): mixed
{
    $firstname = $input['firstname'];
    $lastname = $input['lastname'];
    $gender = $input['gender'];
    $address = $input['address'];
    $contact = $input['contact'];
    $type = $input['type'];
    $year_level = $input['year_level'];
    $status = $input['status'];
    $id = $input['id'];
    return mysql_query("update member set firstname='$firstname',lastname='$lastname',gender='$gender',address = '$address',contact = '$contact',type = '$type',year_level = '$year_level',status = '$status' where member_id='$id'");
}
