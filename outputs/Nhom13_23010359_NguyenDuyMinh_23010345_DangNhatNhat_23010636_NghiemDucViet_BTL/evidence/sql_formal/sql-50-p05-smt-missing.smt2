; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_50_p05_text () String)
(declare-fun sql_50_p05_format_ok () Bool)
(declare-fun sql_50_p05_type_ok () Bool)
(declare-fun sql_50_p05_present () Bool)
(declare-fun sql_50_p05_accepted () Bool)
(assert
 (let (($x124 (and sql_50_p05_present sql_50_p05_type_ok sql_50_p05_format_ok (>= (str.len sql_50_p05_text) 0) (<= (str.len sql_50_p05_text) 100))))
 (= sql_50_p05_accepted $x124)))
(assert
 sql_50_p05_accepted)
(assert
 (not sql_50_p05_present))
(check-sat)
