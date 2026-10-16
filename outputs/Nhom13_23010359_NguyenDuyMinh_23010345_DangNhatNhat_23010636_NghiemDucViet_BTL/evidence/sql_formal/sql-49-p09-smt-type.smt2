; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_49_p09_text () String)
(declare-fun sql_49_p09_format_ok () Bool)
(declare-fun sql_49_p09_type_ok () Bool)
(declare-fun sql_49_p09_present () Bool)
(declare-fun sql_49_p09_accepted () Bool)
(assert
 (let (($x76 (and sql_49_p09_present sql_49_p09_type_ok sql_49_p09_format_ok (>= (str.len sql_49_p09_text) 0) (<= (str.len sql_49_p09_text) 30))))
 (= sql_49_p09_accepted $x76)))
(assert
 sql_49_p09_accepted)
(assert
 (not sql_49_p09_type_ok))
(check-sat)
