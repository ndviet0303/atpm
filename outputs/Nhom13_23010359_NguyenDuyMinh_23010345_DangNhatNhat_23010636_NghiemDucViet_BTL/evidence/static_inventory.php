<?php
// Reads the target source as text. No target script is included or evaluated.
$rows = array();
foreach (glob($argv[1] . '/*.php') as $filename) {
    $source = file_get_contents($filename);
    $tokens = token_get_all($source);
    $counts = array(); $variables = array(); $includes = array(); $requests = array();
    $decisions = array(); $loops = array(); $calls = array();
    foreach ($tokens as $i => $token) {
        if (!is_array($token)) { continue; }
        list($kind, $text, $line) = $token;
        $name = token_name($kind);
        $counts[$name] = isset($counts[$name]) ? $counts[$name] + 1 : 1;
        if ($kind == T_VARIABLE) { $variables[$text] = true; }
        if (in_array($kind, array(T_IF, T_ELSEIF, T_CASE, T_CATCH, T_BOOLEAN_AND, T_BOOLEAN_OR, T_LOGICAL_AND, T_LOGICAL_OR))) {
            $decisions[] = array('token' => $name, 'line' => $line);
        }
        if (in_array($kind, array(T_FOR, T_FOREACH, T_WHILE, T_DO))) { $loops[] = array('token' => $name, 'line' => $line); }
        if (in_array($kind, array(T_INCLUDE, T_INCLUDE_ONCE, T_REQUIRE, T_REQUIRE_ONCE))) {
            $path = null;
            for ($j = $i + 1; $j < count($tokens) && $j < $i + 12; $j++) {
                if (is_array($tokens[$j]) && $tokens[$j][0] == T_CONSTANT_ENCAPSED_STRING) { $path = trim($tokens[$j][1], "\"'"); break; }
                if ($tokens[$j] === ';') { break; }
            }
            $includes[] = array('line' => $line, 'path' => $path, 'exists' => $path !== null && is_file(dirname($filename) . '/' . $path));
        }
        if ($kind == T_VARIABLE && in_array($text, array('$_GET', '$_POST', '$_SESSION', '$_FILES'))) { $requests[] = array('variable' => $text, 'line' => $line); }
        if ($kind == T_STRING) {
            $j = $i + 1;
            while ($j < count($tokens) && is_array($tokens[$j]) && $tokens[$j][0] == T_WHITESPACE) { $j++; }
            if (isset($tokens[$j]) && $tokens[$j] === '(') { $calls[] = array('name' => strtolower($text), 'line' => $line); }
        }
    }
    $rows[] = array('file' => basename($filename), 'token_counts' => $counts, 'variables' => array_keys($variables), 'includes' => $includes, 'request_tokens' => $requests, 'decisions' => $decisions, 'loops' => $loops, 'calls' => $calls);
}
echo json_encode($rows, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
