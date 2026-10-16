<?php
// Generated example of placing untrusted text directly inside JavaScript.
function script_value_v0(string $value): string
{
    return '<script>const title = "' . $value . '";</script>';
}
