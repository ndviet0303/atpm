<?php
require_once __DIR__ . '/security.php';
start_secure_session();
$_SESSION = [];
session_destroy();
header('location:../index.php');
?>