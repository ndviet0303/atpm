<?php
// Static text inspection only. Target PHP is never included or evaluated.
// Usage: php extract_memory_tokens.php <file-or-directory>...
$files = array();
foreach (array_slice($argv, 1) as $target) {
    if (is_dir($target)) {
        foreach (glob(rtrim($target, '/') . '/*.php') as $path) $files[] = $path;
    } else {
        $files[] = $target;
    }
}
$rows = array();
foreach ($files as $path) {
    $text = file_get_contents($path);
    $tokens = array();
    $line = 1;
    foreach (token_get_all($text) as $token) {
        if (is_array($token)) {
            $tokens[] = array(token_name($token[0]), $token[1], $token[2]);
            $line = $token[2] + substr_count($token[1], "\n");
        } else {
            $tokens[] = array('CHAR', $token, $line);
        }
    }
    $rows[] = array('path' => $path, 'sha256' => hash('sha256', $text), 'tokens' => $tokens);
}
echo json_encode($rows, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
