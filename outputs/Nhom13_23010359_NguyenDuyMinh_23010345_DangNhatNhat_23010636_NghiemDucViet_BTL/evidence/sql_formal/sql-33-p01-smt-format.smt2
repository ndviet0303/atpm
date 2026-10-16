; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_33_p01_value () Int)
(declare-fun sql_33_p01_format_ok () Bool)
(declare-fun sql_33_p01_type_ok () Bool)
(declare-fun sql_33_p01_present () Bool)
(declare-fun sql_33_p01_accepted () Bool)
(assert
 (let (($x126 (and sql_33_p01_present sql_33_p01_type_ok sql_33_p01_format_ok (>= sql_33_p01_value 1) (<= sql_33_p01_value 2147483647))))
 (= sql_33_p01_accepted $x126)))
(assert
 sql_33_p01_accepted)
(assert
 (not sql_33_p01_format_ok))
(check-sat)
