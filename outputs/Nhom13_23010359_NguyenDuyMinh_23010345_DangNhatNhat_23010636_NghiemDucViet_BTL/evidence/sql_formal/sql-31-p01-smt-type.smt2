; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_31_p01_text () String)
(declare-fun sql_31_p01_format_ok () Bool)
(declare-fun sql_31_p01_type_ok () Bool)
(declare-fun sql_31_p01_present () Bool)
(declare-fun sql_31_p01_accepted () Bool)
(assert
 (let (($x83 (and sql_31_p01_present sql_31_p01_type_ok sql_31_p01_format_ok (>= (str.len sql_31_p01_text) 0) (<= (str.len sql_31_p01_text) 100))))
 (= sql_31_p01_accepted $x83)))
(assert
 sql_31_p01_accepted)
(assert
 (not sql_31_p01_type_ok))
(check-sat)
