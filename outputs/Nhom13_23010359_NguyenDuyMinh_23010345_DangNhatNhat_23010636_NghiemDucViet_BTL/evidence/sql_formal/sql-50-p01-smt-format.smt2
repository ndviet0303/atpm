; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_50_p01_text () String)
(declare-fun sql_50_p01_format_ok () Bool)
(declare-fun sql_50_p01_type_ok () Bool)
(declare-fun sql_50_p01_present () Bool)
(declare-fun sql_50_p01_accepted () Bool)
(assert
 (let (($x106 (and sql_50_p01_present sql_50_p01_type_ok sql_50_p01_format_ok (>= (str.len sql_50_p01_text) 0) (<= (str.len sql_50_p01_text) 100))))
 (= sql_50_p01_accepted $x106)))
(assert
 sql_50_p01_accepted)
(assert
 (not sql_50_p01_format_ok))
(check-sat)
