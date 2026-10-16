; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_45_p01_text () String)
(declare-fun sql_45_p01_format_ok () Bool)
(declare-fun sql_45_p01_type_ok () Bool)
(declare-fun sql_45_p01_present () Bool)
(declare-fun sql_45_p01_accepted () Bool)
(assert
 (let (($x9 (and sql_45_p01_present sql_45_p01_type_ok sql_45_p01_format_ok (>= (str.len sql_45_p01_text) 0) (<= (str.len sql_45_p01_text) 100))))
 (= sql_45_p01_accepted $x9)))
(assert
 sql_45_p01_accepted)
(assert
 (not sql_45_p01_format_ok))
(check-sat)
