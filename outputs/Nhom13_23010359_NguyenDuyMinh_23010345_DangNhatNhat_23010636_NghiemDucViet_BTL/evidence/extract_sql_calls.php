<?php
// Static text inspection only. Target PHP is never included or evaluated.
$directory = $argv[1];
$queries = array();
function token_text($token) { return is_array($token) ? $token[1] : $token; }
function significant($tokens, $index) {
    while ($index < count($tokens) && is_array($tokens[$index]) &&
        in_array($tokens[$index][0], array(T_WHITESPACE, T_COMMENT, T_DOC_COMMENT))) {
        $index++;
    }
    return $index;
}
function expression($tokens, $start, $stopOnClosing) {
    $pieces = ''; $round = 0; $square = 0;
    for ($j = $start; $j < count($tokens); $j++) {
        $token = $tokens[$j];
        if (!is_array($token)) {
            if ($token === '(') $round++;
            elseif ($token === ')') {
                if ($round === 0) return array(trim($pieces), $j);
                $round--;
            }
            elseif ($token === '[') $square++;
            elseif ($token === ']') $square--;
            elseif ($round === 0 && $square === 0 &&
                ($token === ';' || ($token === ',' && $stopOnClosing))) {
                return array(trim($pieces), $j);
            }
        }
        $pieces .= token_text($token);
    }
    throw new RuntimeException('Unterminated expression');
}
foreach (glob($directory . '/*.php') as $path) {
    $text = file_get_contents($path);
    $tokens = token_get_all($text);
    $assignments = array(); $line = 1;
    foreach ($tokens as $i => $token) {
        $currentLine = is_array($token) ? $token[2] : $line;
        if (is_array($token) && $token[0] === T_VARIABLE) {
            $j = significant($tokens, $i + 1);
            if (isset($tokens[$j]) && $tokens[$j] === '=') {
                list($rhs, $end) = expression($tokens, $j + 1, false);
                $assignments[$token[1]] = array('line' => $currentLine, 'expression' => $rhs);
            }
        }
        if (is_array($token) && $token[0] === T_STRING &&
            strtolower($token[1]) === 'mysql_query') {
            $j = significant($tokens, $i + 1);
            if (!isset($tokens[$j]) || $tokens[$j] !== '(') continue;
            list($arg, $end) = expression($tokens, $j + 1, true);
            $resolved = $arg;
            $assignment = null;
            if (preg_match('/^\$[A-Za-z_]\w*$/', $arg) && isset($assignments[$arg])) {
                $assignment = $assignments[$arg];
                $resolved = $assignment['expression'];
            }
            $endLine = $currentLine;
            for ($k = $i; $k <= $end; $k++) $endLine += substr_count(token_text($tokens[$k]), "\n");
            $queries[] = array(
                'file' => basename($path), 'start_line' => $currentLine,
                'end_line' => $endLine, 'argument' => $arg,
                'resolved_expression' => $resolved, 'sql_assignment' => $assignment,
                'preceding_assignments' => $assignments,
                'source_sha256' => hash('sha256', $text)
            );
        }
        $line += substr_count(token_text($token), "\n");
    }
}
echo json_encode($queries, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
