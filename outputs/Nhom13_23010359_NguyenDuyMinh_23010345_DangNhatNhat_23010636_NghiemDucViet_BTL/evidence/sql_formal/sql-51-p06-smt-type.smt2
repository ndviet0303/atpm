; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_51_p06_text () String)
(declare-fun sql_51_p06_format_ok () Bool)
(declare-fun sql_51_p06_type_ok () Bool)
(declare-fun sql_51_p06_present () Bool)
(declare-fun sql_51_p06_accepted () Bool)
(assert
 (let (($x95 (and sql_51_p06_present sql_51_p06_type_ok sql_51_p06_format_ok (>= (str.len sql_51_p06_text) 0) (<= (str.len sql_51_p06_text) 100))))
 (= sql_51_p06_accepted $x95)))
(assert
 sql_51_p06_accepted)
(assert
 (not sql_51_p06_type_ok))
(check-sat)
