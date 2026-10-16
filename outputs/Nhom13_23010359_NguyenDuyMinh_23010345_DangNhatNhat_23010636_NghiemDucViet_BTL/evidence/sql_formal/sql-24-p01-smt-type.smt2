; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_24_p01_value () Int)
(declare-fun sql_24_p01_format_ok () Bool)
(declare-fun sql_24_p01_type_ok () Bool)
(declare-fun sql_24_p01_present () Bool)
(declare-fun sql_24_p01_accepted () Bool)
(assert
 (let (($x53 (and sql_24_p01_present sql_24_p01_type_ok sql_24_p01_format_ok (>= sql_24_p01_value 1) (<= sql_24_p01_value 2147483647))))
 (= sql_24_p01_accepted $x53)))
(assert
 sql_24_p01_accepted)
(assert
 (not sql_24_p01_type_ok))
(check-sat)
