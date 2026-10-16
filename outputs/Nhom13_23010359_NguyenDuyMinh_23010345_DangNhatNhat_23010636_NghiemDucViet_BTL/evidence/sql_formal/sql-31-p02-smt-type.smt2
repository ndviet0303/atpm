; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_31_p02_text () String)
(declare-fun sql_31_p02_format_ok () Bool)
(declare-fun sql_31_p02_type_ok () Bool)
(declare-fun sql_31_p02_present () Bool)
(declare-fun sql_31_p02_accepted () Bool)
(assert
 (let (($x71 (and sql_31_p02_present sql_31_p02_type_ok sql_31_p02_format_ok (>= (str.len sql_31_p02_text) 0) (<= (str.len sql_31_p02_text) 100))))
 (= sql_31_p02_accepted $x71)))
(assert
 sql_31_p02_accepted)
(assert
 (not sql_31_p02_type_ok))
(check-sat)
