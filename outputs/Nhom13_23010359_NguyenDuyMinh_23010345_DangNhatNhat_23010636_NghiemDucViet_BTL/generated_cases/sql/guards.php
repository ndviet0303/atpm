<?php
// Educational guards; no DB connection is created.
function sql_case_int(mixed $raw, int $minimum, int $maximum): int
{
    if (!is_int($raw) && !is_string($raw)) {
        throw new InvalidArgumentException('Integer scalar required');
    }
    $value = filter_var($raw, FILTER_VALIDATE_INT,
        ['options' => ['min_range' => $minimum, 'max_range' => $maximum]]);
    if ($value === false) {
        throw new InvalidArgumentException('Invalid integer range or format');
    }
    return $value;
}
function sql_case_text(mixed $raw, int $maximum): string
{
    if (!is_string($raw) || strpos($raw, "\0") !== false) {
        throw new InvalidArgumentException('Text scalar required without NUL');
    }
    $length = preg_match_all('/./us', $raw);
    if ($length === false || $length > $maximum) {
        throw new InvalidArgumentException('Invalid UTF-8 or character capacity');
    }
    return $raw;
}
function sql_case_present(array $input, string $key): mixed
{
    if (!array_key_exists($key, $input)) {
        throw new InvalidArgumentException('Missing parameter');
    }
    return $input[$key];
}
