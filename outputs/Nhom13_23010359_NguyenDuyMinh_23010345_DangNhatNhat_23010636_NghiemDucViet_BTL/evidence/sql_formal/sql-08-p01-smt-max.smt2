; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_08_p01_value () Int)
(declare-fun sql_08_p01_format_ok () Bool)
(declare-fun sql_08_p01_type_ok () Bool)
(declare-fun sql_08_p01_present () Bool)
(declare-fun sql_08_p01_accepted () Bool)
(assert
 (let (($x25 (and sql_08_p01_present sql_08_p01_type_ok sql_08_p01_format_ok (>= sql_08_p01_value 1) (<= sql_08_p01_value 2147483647))))
 (= sql_08_p01_accepted $x25)))
(assert
 sql_08_p01_accepted)
(assert
 (= sql_08_p01_value 2147483648))
(check-sat)
