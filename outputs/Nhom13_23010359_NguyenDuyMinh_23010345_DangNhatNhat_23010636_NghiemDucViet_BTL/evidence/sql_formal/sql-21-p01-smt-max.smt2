; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_21_p01_value () Int)
(declare-fun sql_21_p01_format_ok () Bool)
(declare-fun sql_21_p01_type_ok () Bool)
(declare-fun sql_21_p01_present () Bool)
(declare-fun sql_21_p01_accepted () Bool)
(assert
 (let (($x29 (and sql_21_p01_present sql_21_p01_type_ok sql_21_p01_format_ok (>= sql_21_p01_value 1) (<= sql_21_p01_value 2147483647))))
 (= sql_21_p01_accepted $x29)))
(assert
 sql_21_p01_accepted)
(assert
 (= sql_21_p01_value 2147483648))
(check-sat)
