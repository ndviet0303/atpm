; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_14_p01_value () Int)
(declare-fun sql_14_p01_format_ok () Bool)
(declare-fun sql_14_p01_type_ok () Bool)
(declare-fun sql_14_p01_present () Bool)
(declare-fun sql_14_p01_accepted () Bool)
(assert
 (let (($x91 (and sql_14_p01_present sql_14_p01_type_ok sql_14_p01_format_ok (>= sql_14_p01_value 1) (<= sql_14_p01_value 2147483647))))
 (= sql_14_p01_accepted $x91)))
(assert
 sql_14_p01_accepted)
(assert
 (not sql_14_p01_format_ok))
(check-sat)
