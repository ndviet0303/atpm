; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_13_p01_value () Int)
(declare-fun sql_13_p01_format_ok () Bool)
(declare-fun sql_13_p01_type_ok () Bool)
(declare-fun sql_13_p01_present () Bool)
(declare-fun sql_13_p01_accepted () Bool)
(assert
 (let (($x8 (and sql_13_p01_present sql_13_p01_type_ok sql_13_p01_format_ok (>= sql_13_p01_value 1) (<= sql_13_p01_value 2147483647))))
 (= sql_13_p01_accepted $x8)))
(assert
 sql_13_p01_accepted)
(assert
 (= 2147483647 sql_13_p01_value))
(assert
 sql_13_p01_present)
(assert
 sql_13_p01_type_ok)
(assert
 sql_13_p01_format_ok)
(check-sat)
