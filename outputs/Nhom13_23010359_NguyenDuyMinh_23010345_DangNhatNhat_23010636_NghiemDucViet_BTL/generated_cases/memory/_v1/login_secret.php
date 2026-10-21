<?php
// Generated correction: LIMIT 1, row checked, and the password string is wiped.
// sodium_memzero() only zeroes a string with refcount 1, so the $_POST copy is unset first.
function login_v1(PDO $db): bool
{
    $username = (string) ($_POST['username'] ?? '');
    $password = (string) ($_POST['password'] ?? '');
    unset($_POST['password']);
    $stmt = $db->prepare('SELECT user_id, password_hash FROM users WHERE username = :u LIMIT 1');
    $stmt->execute([':u' => $username]);
    $row = $stmt->fetch(PDO::FETCH_ASSOC);
    $stmt = null;
    $ok = is_array($row) && password_verify($password, $row['password_hash']);
    sodium_memzero($password);
    if ($ok) {
        $_SESSION['id'] = (int) $row['user_id'];
    }
    return $ok;
}
