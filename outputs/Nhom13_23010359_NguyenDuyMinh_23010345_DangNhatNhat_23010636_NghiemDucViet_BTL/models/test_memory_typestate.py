"""Unit tests for the memory typestate. Snippets are tokenised by php, never executed.
Run: study/.venv/bin/python models/test_memory_typestate.py"""
from collections import Counter
from pathlib import Path
import sys
import tempfile
import textwrap
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import memory_typestate as m

TABLES = m.schema()


def analyze(code, php8=False):
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / 'snippet.php'
        path.write_text('<?php\n' + textwrap.dedent(code))  # snippet line 1 is file line 2
        return m.analyze_file(m.tokens_for([path])[0], TABLES, php8=php8)


def found(w):
    return sorted((v['id'], v['line']) for v in w.violations)


class Table(unittest.TestCase):
    def test_transitions(self):
        self.assertEqual(m.step('UNDEF', 'alloc'), ('PENDING', None))
        self.assertEqual(m.step('PENDING', 'use'), ('ALLOCATED', 'E_USE_FALSE'))
        self.assertEqual(m.step('ROW_PENDING', 'read'), ('ROW', 'E_ROW_UNCHECKED'))
        self.assertEqual(m.step('RELEASED', 'use'), ('RELEASED', 'E_USE_RELEASED'))
        self.assertEqual(m.step('RELEASED', 'release'), ('RELEASED', 'E_DOUBLE_RELEASE'))
        self.assertEqual(m.step('SECRET', 'drop'), ('RELEASED', 'E_SECRET_RESIDUE'))
        self.assertEqual(m.step('WIPED', 'end'), ('RELEASED', None))
        self.assertEqual(m.step('ALLOCATED', 'end', 'result'), ('HELD_TO_END', 'E_HELD_TO_END'))
        self.assertEqual(m.step('ALLOCATED', 'end', 'row'), ('HELD_TO_END', None))  # only resources leak

    def test_concrete_paths(self):
        self.assertEqual(m.concrete_step('UNDEF', 'alloc_checked', False), ('DONE', None))
        self.assertEqual(m.concrete_step('UNDEF', 'alloc', False), ('FALSE', None))
        self.assertEqual(m.concrete_step('FALSE', 'use', True), ('FALSE', 'E_USE_FALSE'))
        self.assertEqual(m.concrete_step('NOROW', 'read', True), ('NOROW', 'E_ROW_UNCHECKED'))
        self.assertEqual(m.concrete_step('NOROW', 'check', True), ('DONE', None))

    def test_every_violation_has_cwe(self):
        targets = {v for _, v in m.TABLE.values() if v}
        self.assertTrue(targets <= set(m.VIOLATIONS))
        self.assertTrue(all(c.startswith('CWE-') for cwe, _, _ in m.VIOLATIONS.values() for c in cwe))


class SqlBound(unittest.TestCase):
    def test_bounds(self):
        b = lambda sql: m.sql_bound(sql, TABLES)
        self.assertEqual(b('SELECT * FROM book LIMIT 50')['max_rows'], 50)
        self.assertEqual(b("SELECT * FROM book WHERE book_id = '1'")['max_rows'], 1)
        self.assertEqual(b('SELECT count(*) FROM book')['max_rows'], 1)
        self.assertFalse(b('SELECT * FROM member')['bounded'])
        self.assertEqual(b('SELECT * FROM member')['row_width'], 721)
        self.assertFalse(b('SELECT * FROM students')['bounded'])  # not in eb_lms.sql
        self.assertFalse(b('DELETE FROM book')['select'])


class Snippets(unittest.TestCase):
    def test_or_die_checks_the_result(self):
        w = analyze("""\
            $r = mysql_query("SELECT * FROM book WHERE book_id = 1") or die(mysql_error());
            $n = mysql_num_rows($r);
            mysql_free_result($r);
            """)
        self.assertEqual(found(w), [])

    def test_unchecked_result(self):
        w = analyze("""\
            $r = mysql_query("SELECT * FROM book WHERE book_id = 1");
            $n = mysql_num_rows($r);
            mysql_free_result($r);
            """)
        self.assertEqual(found(w), [('E_USE_FALSE', 3)])

    def test_unbounded_held_to_end(self):
        w = analyze("""\
            $r = mysql_query("SELECT * FROM book") or die(mysql_error());
            """)
        self.assertEqual(found(w), [('E_HELD_TO_END', 2), ('E_UNBOUNDED_ALLOC', 2)])

    def test_query_in_loop(self):
        w = analyze("""\
            foreach ($ids as $id) {
                $r = mysql_query("SELECT * FROM book WHERE book_id = '$id'") or die();
                mysql_free_result($r);
            }
            """)
        self.assertEqual(found(w), [('E_ALLOC_IN_LOOP', 3)])

    def test_use_after_free_and_double_free(self):
        w = analyze("""\
            $r = mysql_query("SELECT * FROM book WHERE book_id = 1") or die();
            mysql_free_result($r);
            $n = mysql_num_rows($r);
            mysql_free_result($r);
            """)
        self.assertEqual(found(w), [('E_DOUBLE_RELEASE', 5), ('E_USE_RELEASED', 4)])

    def test_alias_keeps_refcount(self):
        w = analyze("""\
            $a = mysql_query("SELECT * FROM book WHERE book_id = 1") or die();
            $b = $a;
            unset($a);
            $n = mysql_num_rows($b);
            mysql_free_result($b);
            """)
        self.assertEqual(found(w), [])

    def test_row_guarded_by_num_rows(self):
        w = analyze("""\
            $r = mysql_query("SELECT * FROM users WHERE user_id = 1") or die();
            $n = mysql_num_rows($r);
            $row = mysql_fetch_array($r);
            if ($n > 0) { $id = $row['user_id']; }
            mysql_free_result($r);
            """)
        self.assertEqual(found(w), [])

    def test_row_unchecked(self):
        w = analyze("""\
            $r = mysql_query("SELECT * FROM users WHERE user_id = 1") or die();
            $row = mysql_fetch_array($r);
            $id = $row['user_id'];
            mysql_free_result($r);
            """)
        self.assertEqual(found(w), [('E_ROW_UNCHECKED', 4)])

    def test_return_moves_ownership(self):
        w = analyze("""\
            function one() {
                $r = mysql_query("SELECT * FROM book WHERE book_id = 1") or die();
                return $r;
            }
            """)
        self.assertEqual(found(w), [])

    def test_password_wiped_after_unset(self):
        w = analyze("""\
            $password = (string) $_POST['password'];
            unset($_POST['password']);
            $ok = password_verify($password, $hash);
            sodium_memzero($password);
            """, php8=True)
        self.assertEqual(found(w), [])

    def test_memzero_without_unset_leaves_residue(self):
        # php-src ext/sodium: refcount 2 (the $_POST copy) -> only convert_to_null, no wipe
        w = analyze("""\
            $password = $_POST['password'];
            $ok = password_verify($password, $hash);
            sodium_memzero($password);
            """, php8=True)
        self.assertEqual([v[0] for v in found(w)], ['E_SECRET_RESIDUE'])

    def test_secret_param_is_borrowed(self):
        w = analyze("""\
            function check($password) {
                return password_verify($password, '$2y$10$x');
            }
            """, php8=True)
        self.assertEqual(found(w), [])


class Cases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = {}
        for version in ('_v0', '_v1'):
            for entry in m.tokens_for([m.BASE / 'generated_cases/memory' / version]):
                w = m.analyze_file(entry, TABLES, php8=True)
                cls.result[version, w.file] = sorted((v['id'], v['line'], v['var']) for v in w.violations)

    def test_v0_expected(self):
        self.assertEqual(self.result['_v0', 'book_listing.php'], [
            ('E_ALLOC_IN_LOOP', 9, '$borrow_details'), ('E_ALLOC_IN_LOOP', 12, '$cat_query'),
            ('E_ROW_UNCHECKED', 14, '$cat_row'), ('E_ROW_UNCHECKED', 14, '$row11'),
            ('E_UNBOUNDED_ALLOC', 6, '$user_query'), ('E_UNBOUNDED_ALLOC', 9, '$borrow_details'),  # book_id is not the borrowdetails key
            ('E_USE_FALSE', 10, '$borrow_details')])
        self.assertEqual([v[:2] for v in self.result['_v0', 'latest_borrow.php']],
                         [('E_ROW_UNCHECKED', 8), ('E_UNBOUNDED_ALLOC', 6)])
        self.assertEqual(Counter(v[0] for v in self.result['_v0', 'login_secret.php']),
                         Counter({'E_SECRET_RESIDUE': 2, 'E_UNBOUNDED_ALLOC': 1, 'E_ROW_UNCHECKED': 1}))
        self.assertEqual([v[0] for v in self.result['_v0', 'token_key.php']], ['E_SECRET_RESIDUE'])

    def test_v1_clean(self):
        for (version, name), hits in self.result.items():
            if version == '_v1':
                self.assertEqual(hits, [], name)

    def test_baseline_counts(self):
        total = Counter()
        for entry in m.tokens_for([m.BASE / 'source_v0/librarian']):
            total.update(v['id'] for v in m.analyze_file(entry, TABLES).violations)
        self.assertEqual(total, Counter({'E_HELD_TO_END': 38, 'E_UNBOUNDED_ALLOC': 25, 'E_ROW_UNCHECKED': 13,
                                         'E_ALLOC_IN_LOOP': 11, 'E_SECRET_RESIDUE': 6, 'E_USE_FALSE': 3}))


if __name__ == '__main__':
    unittest.main()
