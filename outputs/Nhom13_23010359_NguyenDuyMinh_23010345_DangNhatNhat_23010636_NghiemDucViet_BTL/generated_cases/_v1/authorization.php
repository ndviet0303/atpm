<?php
// Declared educational policy; upstream has no role specification.
// Session values must be assigned by a trusted server-side login flow.
function authorize_v1(array $session, string $action): bool
{
    $policy = [
        'book_write' => ['librarian', 'admin'],
        'user_delete' => ['admin'],
    ];
    $id = $session['id'] ?? null;
    $role = $session['role'] ?? null;
    return is_int($id) && $id > 0 && is_string($role)
        && isset($policy[$action])
        && in_array($role, $policy[$action], true);
}
