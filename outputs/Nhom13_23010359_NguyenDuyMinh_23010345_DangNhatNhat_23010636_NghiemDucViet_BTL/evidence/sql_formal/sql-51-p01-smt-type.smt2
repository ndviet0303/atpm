; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_51_p01_text () String)
(declare-fun sql_51_p01_format_ok () Bool)
(declare-fun sql_51_p01_type_ok () Bool)
(declare-fun sql_51_p01_present () Bool)
(declare-fun sql_51_p01_accepted () Bool)
(assert
 (let (($x39 (and sql_51_p01_present sql_51_p01_type_ok sql_51_p01_format_ok (>= (str.len sql_51_p01_text) 0) (<= (str.len sql_51_p01_text) 100))))
 (= sql_51_p01_accepted $x39)))
(assert
 sql_51_p01_accepted)
(assert
 (not sql_51_p01_type_ok))
(check-sat)
