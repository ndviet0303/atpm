; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_50_p09_value () Int)
(declare-fun sql_50_p09_format_ok () Bool)
(declare-fun sql_50_p09_type_ok () Bool)
(declare-fun sql_50_p09_present () Bool)
(declare-fun sql_50_p09_accepted () Bool)
(assert
 (let (($x132 (and sql_50_p09_present sql_50_p09_type_ok sql_50_p09_format_ok (>= sql_50_p09_value 1) (<= sql_50_p09_value 2147483647))))
 (= sql_50_p09_accepted $x132)))
(assert
 sql_50_p09_accepted)
(assert
 (= sql_50_p09_value 0))
(check-sat)
