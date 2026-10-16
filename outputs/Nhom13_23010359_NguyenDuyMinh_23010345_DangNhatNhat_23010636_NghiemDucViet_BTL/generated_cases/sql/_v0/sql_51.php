<?php
// SQL-51: update_students.php:15-15.
// Query-only text example; never executed.
function sql_51_v0(array $input): mixed
{
    $firstname = $input['firstname'];
    $lastname = $input['lastname'];
    $gender = $input['gender'];
    $address = $input['address'];
    $contact = $input['contact'];
    $type = $input['type'];
    $year_level = $input['year_level'];
    $id = $input['id'];
    return mysql_query("update member set firstname='$firstname',lastname='$lastname',gender='$gender',address = '$address',contact = '$contact',type = '$type',year_level = '$year_level' where member_id='$id'");
}
