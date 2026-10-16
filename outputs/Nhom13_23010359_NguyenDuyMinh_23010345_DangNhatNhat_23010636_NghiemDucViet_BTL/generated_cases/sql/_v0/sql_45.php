<?php
// SQL-45: student_save.php:15-15.
// Query-only text example; never executed.
function sql_45_v0(array $input): mixed
{
    $firstname = $input['firstname'];
    $lastname = $input['lastname'];
    $gender = $input['gender'];
    $address = $input['address'];
    $contact = $input['contact'];
    $type = $input['type'];
    $year_level = $input['year_level'];
    return mysql_query("insert into member(firstname,lastname,gender,address,contact,type,year_level) values('$firstname','$lastname','$gender','$address','$contact','$type','$year_level')");
}
