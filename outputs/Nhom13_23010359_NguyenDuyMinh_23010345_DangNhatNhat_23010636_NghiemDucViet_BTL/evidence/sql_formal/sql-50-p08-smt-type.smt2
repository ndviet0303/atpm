; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_50_p08_text () String)
(declare-fun sql_50_p08_format_ok () Bool)
(declare-fun sql_50_p08_type_ok () Bool)
(declare-fun sql_50_p08_present () Bool)
(declare-fun sql_50_p08_accepted () Bool)
(assert
 (let (($x137 (and sql_50_p08_present sql_50_p08_type_ok sql_50_p08_format_ok (>= (str.len sql_50_p08_text) 0) (<= (str.len sql_50_p08_text) 100))))
 (= sql_50_p08_accepted $x137)))
(assert
 sql_50_p08_accepted)
(assert
 (not sql_50_p08_type_ok))
(check-sat)
