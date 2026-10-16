<?php
// Output encoding is different from cryptographic encryption.
function script_value_v1(string $value): string
{
    $json = json_encode($value, JSON_HEX_TAG | JSON_HEX_AMP
        | JSON_HEX_APOS | JSON_HEX_QUOT | JSON_THROW_ON_ERROR);
    return '<script>const title = ' . $json . ';</script>';
}
