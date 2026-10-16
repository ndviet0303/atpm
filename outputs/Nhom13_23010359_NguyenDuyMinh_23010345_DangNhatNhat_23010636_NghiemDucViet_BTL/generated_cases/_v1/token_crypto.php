<?php
// Generated AES-GCM token policy, not an implemented baseline feature.
const TOKEN_CIPHER_V1 = 'aes-256-gcm';
const TOKEN_KEY_BYTES_V1 = 32;
const TOKEN_NONCE_BYTES_V1 = 12;
const TOKEN_TAG_BYTES_V1 = 16;
const TOKEN_TTL_SECONDS_V1 = 1800;
const TOKEN_AAD_V1 = 'library-token-v1';

function token_key_v1(): string
{
    $encoded = getenv('LIBRARY_TOKEN_KEY_B64');
    $key = is_string($encoded) ? base64_decode($encoded, true) : false;
    if (!is_string($key) || strlen($key) !== TOKEN_KEY_BYTES_V1) {
        throw new RuntimeException('Invalid token key configuration');
    }
    return $key;
}

function issue_token_v1(int $userId, int $now): string
{
    if ($userId <= 0 || $now < 0) {
        throw new InvalidArgumentException('Invalid token claims');
    }
    $claims = ['uid' => $userId, 'aud' => 'library', 'iat' => $now,
        'exp' => $now + TOKEN_TTL_SECONDS_V1];
    $plain = json_encode($claims, JSON_THROW_ON_ERROR);
    $nonce = random_bytes(TOKEN_NONCE_BYTES_V1);
    $tag = '';
    $ciphertext = openssl_encrypt($plain, TOKEN_CIPHER_V1, token_key_v1(),
        OPENSSL_RAW_DATA, $nonce, $tag, TOKEN_AAD_V1, TOKEN_TAG_BYTES_V1);
    if ($ciphertext === false || strlen($tag) !== TOKEN_TAG_BYTES_V1) {
        throw new RuntimeException('Token encryption failed');
    }
    return base64_encode($nonce . $tag . $ciphertext);
}

function read_token_v1(string $token, int $now): ?array
{
    if (strlen($token) > 4096 || $now < 0) {
        return null;
    }
    $raw = base64_decode($token, true);
    $prefix = TOKEN_NONCE_BYTES_V1 + TOKEN_TAG_BYTES_V1;
    if (!is_string($raw) || strlen($raw) <= $prefix) {
        return null;
    }
    $nonce = substr($raw, 0, TOKEN_NONCE_BYTES_V1);
    $tag = substr($raw, TOKEN_NONCE_BYTES_V1, TOKEN_TAG_BYTES_V1);
    $ciphertext = substr($raw, $prefix);
    if (strlen($nonce) !== TOKEN_NONCE_BYTES_V1
        || strlen($tag) !== TOKEN_TAG_BYTES_V1) {
        return null;
    }
    $plain = openssl_decrypt($ciphertext, TOKEN_CIPHER_V1, token_key_v1(),
        OPENSSL_RAW_DATA, $nonce, $tag, TOKEN_AAD_V1);
    if ($plain === false) {
        return null;
    }
    try {
        $claims = json_decode($plain, true, 8, JSON_THROW_ON_ERROR);
    } catch (JsonException $error) {
        return null;
    }
    if (!is_array($claims) || !is_int($claims['uid'] ?? null)
        || $claims['uid'] <= 0 || ($claims['aud'] ?? null) !== 'library'
        || !is_int($claims['iat'] ?? null) || !is_int($claims['exp'] ?? null)
        || $claims['iat'] < 0 || $claims['iat'] > $now
        || $claims['exp'] <= $now
        || $claims['exp'] - $claims['iat'] > TOKEN_TTL_SECONDS_V1) {
        return null;
    }
    return $claims;
}

function csrf_token_v1(): string
{
    return bin2hex(random_bytes(32)); // 32 random bytes -> 64 hex characters.
}
function csrf_valid_v1(string $expected, string $received): bool
{
    return strlen($expected) === 64 && strlen($received) === 64
        && ctype_xdigit($expected) && ctype_xdigit($received)
        && hash_equals($expected, $received);
}
