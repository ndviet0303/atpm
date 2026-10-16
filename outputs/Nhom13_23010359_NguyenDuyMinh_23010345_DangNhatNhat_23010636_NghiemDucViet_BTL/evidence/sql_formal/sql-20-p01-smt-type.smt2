; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_20_p01_value () Int)
(declare-fun sql_20_p01_format_ok () Bool)
(declare-fun sql_20_p01_type_ok () Bool)
(declare-fun sql_20_p01_present () Bool)
(declare-fun sql_20_p01_accepted () Bool)
(assert
 (let (($x78 (and sql_20_p01_present sql_20_p01_type_ok sql_20_p01_format_ok (>= sql_20_p01_value 1) (<= sql_20_p01_value 2147483647))))
 (= sql_20_p01_accepted $x78)))
(assert
 sql_20_p01_accepted)
(assert
 (not sql_20_p01_type_ok))
(check-sat)
