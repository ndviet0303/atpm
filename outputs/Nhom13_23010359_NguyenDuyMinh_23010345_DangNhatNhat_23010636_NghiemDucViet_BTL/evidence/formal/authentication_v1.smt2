; benchmark generated from python API
(set-info :status unknown)
(declare-fun row_exists () Bool)
(declare-fun grant () Bool)
(declare-fun password_valid () Bool)
(assert
 (let (($x31 (not grant)))
 (or $x31 row_exists)))
(assert
 (let (($x31 (not grant)))
 (or $x31 password_valid)))
(assert
 (let (($x13 (not password_valid)))
 (let (($x14 (not row_exists)))
 (or grant $x14 $x13))))
(assert
 (or grant))
(assert
 (let (($x13 (not password_valid)))
(or $x13)))
(check-sat)
