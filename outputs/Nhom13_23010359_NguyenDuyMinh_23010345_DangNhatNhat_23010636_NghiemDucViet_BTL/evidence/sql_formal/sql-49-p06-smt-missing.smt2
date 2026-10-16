; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_49_p06_text () String)
(declare-fun sql_49_p06_format_ok () Bool)
(declare-fun sql_49_p06_type_ok () Bool)
(declare-fun sql_49_p06_present () Bool)
(declare-fun sql_49_p06_accepted () Bool)
(assert
 (let (($x68 (and sql_49_p06_present sql_49_p06_type_ok sql_49_p06_format_ok (>= (str.len sql_49_p06_text) 0) (<= (str.len sql_49_p06_text) 100))))
 (= sql_49_p06_accepted $x68)))
(assert
 sql_49_p06_accepted)
(assert
 (not sql_49_p06_present))
(check-sat)
