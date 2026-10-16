; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_10_p06_text () String)
(declare-fun sql_10_p06_format_ok () Bool)
(declare-fun sql_10_p06_type_ok () Bool)
(declare-fun sql_10_p06_present () Bool)
(declare-fun sql_10_p06_accepted () Bool)
(assert
 (let (($x120 (and sql_10_p06_present sql_10_p06_type_ok sql_10_p06_format_ok (>= (str.len sql_10_p06_text) 0) (<= (str.len sql_10_p06_text) 100))))
 (= sql_10_p06_accepted $x120)))
(assert
 sql_10_p06_accepted)
(assert
 (not sql_10_p06_present))
(check-sat)
