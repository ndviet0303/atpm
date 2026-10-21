<?php
// Intentionally unsafe generated experiment. It is absent from the baseline.
// The decoded signing key is released at function exit without being overwritten.
function sign_token_v0(string $payload): string
{
    $key = base64_decode(getenv('LIBRARY_TOKEN_KEY_B64'));
    return hash_hmac('sha256', $payload, $key);
}
