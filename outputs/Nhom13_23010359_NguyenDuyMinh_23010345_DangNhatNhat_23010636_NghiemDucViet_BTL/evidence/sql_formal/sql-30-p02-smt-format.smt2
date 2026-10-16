; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_30_p02_text () String)
(declare-fun sql_30_p02_format_ok () Bool)
(declare-fun sql_30_p02_type_ok () Bool)
(declare-fun sql_30_p02_present () Bool)
(declare-fun sql_30_p02_accepted () Bool)
(assert
 (let (($x74 (and sql_30_p02_present sql_30_p02_type_ok sql_30_p02_format_ok (>= (str.len sql_30_p02_text) 0) (<= (str.len sql_30_p02_text) 100))))
 (= sql_30_p02_accepted $x74)))
(assert
 sql_30_p02_accepted)
(assert
 (not sql_30_p02_format_ok))
(check-sat)
