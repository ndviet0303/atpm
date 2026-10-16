; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_49_p02_value () Int)
(declare-fun sql_49_p02_format_ok () Bool)
(declare-fun sql_49_p02_type_ok () Bool)
(declare-fun sql_49_p02_present () Bool)
(declare-fun sql_49_p02_accepted () Bool)
(assert
 (let (($x80 (and sql_49_p02_present sql_49_p02_type_ok sql_49_p02_format_ok (>= sql_49_p02_value 1) (<= sql_49_p02_value 2147483647))))
 (= sql_49_p02_accepted $x80)))
(assert
 sql_49_p02_accepted)
(assert
 (not sql_49_p02_present))
(check-sat)
