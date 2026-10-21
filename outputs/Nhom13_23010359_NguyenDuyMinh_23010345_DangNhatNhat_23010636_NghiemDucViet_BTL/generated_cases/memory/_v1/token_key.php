<?php
// Generated correction: the key is validated, used once and zeroed on every exit path.
function sign_token_v1(string $payload): string
{
    $key = base64_decode((string) getenv('LIBRARY_TOKEN_KEY_B64'), true);
    if (!is_string($key) || strlen($key) !== 32) {
        throw new RuntimeException('Invalid token key configuration');
    }
    try {
        return hash_hmac('sha256', $payload, $key);
    } finally {
        sodium_memzero($key);
    }
}
