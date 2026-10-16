; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_39_p01_value () Int)
(declare-fun sql_39_p01_format_ok () Bool)
(declare-fun sql_39_p01_type_ok () Bool)
(declare-fun sql_39_p01_present () Bool)
(declare-fun sql_39_p01_accepted () Bool)
(assert
 (let (($x119 (and sql_39_p01_present sql_39_p01_type_ok sql_39_p01_format_ok (>= sql_39_p01_value 1) (<= sql_39_p01_value 2147483647))))
 (= sql_39_p01_accepted $x119)))
(assert
 sql_39_p01_accepted)
(assert
 (not sql_39_p01_format_ok))
(check-sat)
