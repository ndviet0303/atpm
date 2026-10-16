<?php
// Models the missing guard before a baseline write handler.
function authorize_v0(array $session, string $action): bool
{
    return true;
}
