; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_50_p07_text () String)
(declare-fun sql_50_p07_format_ok () Bool)
(declare-fun sql_50_p07_type_ok () Bool)
(declare-fun sql_50_p07_present () Bool)
(declare-fun sql_50_p07_accepted () Bool)
(assert
 (let (($x50 (and sql_50_p07_present sql_50_p07_type_ok sql_50_p07_format_ok (>= (str.len sql_50_p07_text) 0) (<= (str.len sql_50_p07_text) 100))))
 (= sql_50_p07_accepted $x50)))
(assert
 sql_50_p07_accepted)
(assert
 (= sql_50_p07_text ""))
(assert
 sql_50_p07_present)
(assert
 sql_50_p07_type_ok)
(assert
 sql_50_p07_format_ok)
(check-sat)
