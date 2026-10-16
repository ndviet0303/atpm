; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_41_p01_value () Int)
(declare-fun sql_41_p01_format_ok () Bool)
(declare-fun sql_41_p01_type_ok () Bool)
(declare-fun sql_41_p01_present () Bool)
(declare-fun sql_41_p01_accepted () Bool)
(assert
 (let (($x6 (and sql_41_p01_present sql_41_p01_type_ok sql_41_p01_format_ok (>= sql_41_p01_value 1) (<= sql_41_p01_value 2147483647))))
 (= sql_41_p01_accepted $x6)))
(assert
 sql_41_p01_accepted)
(assert
 (not sql_41_p01_format_ok))
(check-sat)
