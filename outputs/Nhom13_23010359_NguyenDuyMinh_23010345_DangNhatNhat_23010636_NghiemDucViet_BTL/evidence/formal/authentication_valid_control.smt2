; benchmark generated from python API
(set-info :status unknown)
(declare-fun row_exists () Bool)
(declare-fun grant () Bool)
(declare-fun password_valid () Bool)
(assert
 (let (($x13 (not grant)))
 (or $x13 row_exists)))
(assert
 (let (($x13 (not grant)))
 (or $x13 password_valid)))
(assert
 (or grant (not row_exists) (not password_valid)))
(assert
 (or grant))
(assert
 (or row_exists))
(assert
 (or password_valid))
(check-sat)
