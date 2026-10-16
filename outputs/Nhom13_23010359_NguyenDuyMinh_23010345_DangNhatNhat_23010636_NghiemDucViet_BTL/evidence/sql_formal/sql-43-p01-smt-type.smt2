; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_43_p01_value () Int)
(declare-fun sql_43_p01_format_ok () Bool)
(declare-fun sql_43_p01_type_ok () Bool)
(declare-fun sql_43_p01_present () Bool)
(declare-fun sql_43_p01_accepted () Bool)
(assert
 (let (($x39 (and sql_43_p01_present sql_43_p01_type_ok sql_43_p01_format_ok (>= sql_43_p01_value 1) (<= sql_43_p01_value 2147483647))))
 (= sql_43_p01_accepted $x39)))
(assert
 sql_43_p01_accepted)
(assert
 (not sql_43_p01_type_ok))
(check-sat)
