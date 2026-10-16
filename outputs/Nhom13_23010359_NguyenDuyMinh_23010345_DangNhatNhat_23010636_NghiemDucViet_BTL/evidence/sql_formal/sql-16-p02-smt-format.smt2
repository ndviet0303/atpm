; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_16_p02_value () Int)
(declare-fun sql_16_p02_format_ok () Bool)
(declare-fun sql_16_p02_type_ok () Bool)
(declare-fun sql_16_p02_present () Bool)
(declare-fun sql_16_p02_accepted () Bool)
(assert
 (let (($x27 (and sql_16_p02_present sql_16_p02_type_ok sql_16_p02_format_ok (>= sql_16_p02_value 1) (<= sql_16_p02_value 2147483647))))
 (= sql_16_p02_accepted $x27)))
(assert
 sql_16_p02_accepted)
(assert
 (not sql_16_p02_format_ok))
(check-sat)
