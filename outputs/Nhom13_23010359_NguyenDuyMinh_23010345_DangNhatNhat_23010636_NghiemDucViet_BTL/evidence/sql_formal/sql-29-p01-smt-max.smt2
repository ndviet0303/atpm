; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_29_p01_value () Int)
(declare-fun sql_29_p01_format_ok () Bool)
(declare-fun sql_29_p01_type_ok () Bool)
(declare-fun sql_29_p01_present () Bool)
(declare-fun sql_29_p01_accepted () Bool)
(assert
 (let (($x17 (and sql_29_p01_present sql_29_p01_type_ok sql_29_p01_format_ok (>= sql_29_p01_value 1) (<= sql_29_p01_value 2147483647))))
 (= sql_29_p01_accepted $x17)))
(assert
 sql_29_p01_accepted)
(assert
 (= sql_29_p01_value 2147483648))
(check-sat)
