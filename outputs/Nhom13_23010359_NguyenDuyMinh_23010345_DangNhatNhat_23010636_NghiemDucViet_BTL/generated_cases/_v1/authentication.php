<?php
// Generated correction: requires an independent migration to password_hash.
function authenticate_v1(PDO $db, string $username, string $password): ?array
{
    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    $stmt = $db->prepare('SELECT user_id, password_hash FROM users WHERE username = :username');
    $stmt->execute([':username' => $username]);
    $row = $stmt->fetch(PDO::FETCH_ASSOC);
    if (!is_array($row) || !password_verify($password, $row['password_hash'])) {
        return null;
    }
    return ['user_id' => (int) $row['user_id']];
}
function hash_new_password_v1(string $password): string
{
    return password_hash($password, PASSWORD_DEFAULT);
}
