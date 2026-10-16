; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_36_p01_text () String)
(declare-fun sql_36_p01_format_ok () Bool)
(declare-fun sql_36_p01_type_ok () Bool)
(declare-fun sql_36_p01_present () Bool)
(declare-fun sql_36_p01_accepted () Bool)
(assert
 (let (($x128 (and sql_36_p01_present sql_36_p01_type_ok sql_36_p01_format_ok (>= (str.len sql_36_p01_text) 0) (<= (str.len sql_36_p01_text) 100))))
 (= sql_36_p01_accepted $x128)))
(assert
 sql_36_p01_accepted)
(assert
 (= sql_36_p01_text ""))
(assert
 sql_36_p01_present)
(assert
 sql_36_p01_type_ok)
(assert
 sql_36_p01_format_ok)
(check-sat)
