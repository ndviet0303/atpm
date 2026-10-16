; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_10_p08_value () Int)
(declare-fun sql_10_p08_format_ok () Bool)
(declare-fun sql_10_p08_type_ok () Bool)
(declare-fun sql_10_p08_present () Bool)
(declare-fun sql_10_p08_accepted () Bool)
(assert
 (let (($x143 (and sql_10_p08_present sql_10_p08_type_ok sql_10_p08_format_ok (>= sql_10_p08_value 0) (<= sql_10_p08_value 2147483647))))
 (= sql_10_p08_accepted $x143)))
(assert
 sql_10_p08_accepted)
(assert
 (not sql_10_p08_type_ok))
(check-sat)
