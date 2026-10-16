<?php
// Intentionally unsafe generated experiment. It is absent from the baseline.
function issue_token_v0(array $claims): string
{
    $key = 'demo-fixed-key16';
    $iv = str_repeat("\0", 16);
    $plain = json_encode($claims, JSON_THROW_ON_ERROR);
    $ciphertext = openssl_encrypt($plain, 'aes-128-cbc', $key, OPENSSL_RAW_DATA, $iv);
    return base64_encode($iv . $ciphertext);
}
function read_token_v0(string $token): mixed
{
    $raw = base64_decode($token);
    $plain = openssl_decrypt(substr($raw, 16), 'aes-128-cbc',
        'demo-fixed-key16', OPENSSL_RAW_DATA, substr($raw, 0, 16));
    return json_decode($plain, true);
}
