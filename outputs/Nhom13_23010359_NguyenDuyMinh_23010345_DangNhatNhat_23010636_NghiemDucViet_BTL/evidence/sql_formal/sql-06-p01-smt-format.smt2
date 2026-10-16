; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_06_p01_value () Int)
(declare-fun sql_06_p01_format_ok () Bool)
(declare-fun sql_06_p01_type_ok () Bool)
(declare-fun sql_06_p01_present () Bool)
(declare-fun sql_06_p01_accepted () Bool)
(assert
 (let (($x46 (and sql_06_p01_present sql_06_p01_type_ok sql_06_p01_format_ok (>= sql_06_p01_value 1) (<= sql_06_p01_value 2147483647))))
 (= sql_06_p01_accepted $x46)))
(assert
 sql_06_p01_accepted)
(assert
 (not sql_06_p01_format_ok))
(check-sat)
