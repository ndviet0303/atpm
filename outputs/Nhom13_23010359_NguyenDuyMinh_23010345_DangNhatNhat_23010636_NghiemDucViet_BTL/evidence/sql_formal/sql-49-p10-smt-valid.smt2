; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_49_p10_value () Int)
(declare-fun sql_49_p10_format_ok () Bool)
(declare-fun sql_49_p10_type_ok () Bool)
(declare-fun sql_49_p10_present () Bool)
(declare-fun sql_49_p10_accepted () Bool)
(assert
 (let (($x22 (and sql_49_p10_present sql_49_p10_type_ok sql_49_p10_format_ok (>= sql_49_p10_value 1) (<= sql_49_p10_value 2147483647))))
 (= sql_49_p10_accepted $x22)))
(assert
 sql_49_p10_accepted)
(assert
 (= 2147483647 sql_49_p10_value))
(assert
 sql_49_p10_present)
(assert
 sql_49_p10_type_ok)
(assert
 sql_49_p10_format_ok)
(check-sat)
