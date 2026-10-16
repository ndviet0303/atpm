; benchmark generated from python API
(set-info :status unknown)
(declare-fun row_exists () Bool)
(declare-fun grant () Bool)
(declare-fun password_valid () Bool)
(assert
 (let (($x8 (not grant)))
 (or $x8 row_exists)))
(assert
 (or grant (not row_exists)))
(assert
 (or grant))
(assert
 (let (($x31 (not password_valid)))
(or $x31)))
(check-sat)
