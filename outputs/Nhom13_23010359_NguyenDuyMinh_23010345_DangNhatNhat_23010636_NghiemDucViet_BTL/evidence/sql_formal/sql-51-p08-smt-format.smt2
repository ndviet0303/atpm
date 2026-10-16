; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_51_p08_value () Int)
(declare-fun sql_51_p08_format_ok () Bool)
(declare-fun sql_51_p08_type_ok () Bool)
(declare-fun sql_51_p08_present () Bool)
(declare-fun sql_51_p08_accepted () Bool)
(assert
 (let (($x147 (and sql_51_p08_present sql_51_p08_type_ok sql_51_p08_format_ok (>= sql_51_p08_value 1) (<= sql_51_p08_value 2147483647))))
 (= sql_51_p08_accepted $x147)))
(assert
 sql_51_p08_accepted)
(assert
 (not sql_51_p08_format_ok))
(check-sat)
