; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_10_p01_text () String)
(declare-fun sql_10_p01_format_ok () Bool)
(declare-fun sql_10_p01_type_ok () Bool)
(declare-fun sql_10_p01_present () Bool)
(declare-fun sql_10_p01_accepted () Bool)
(assert
 (let (($x82 (and sql_10_p01_present sql_10_p01_type_ok sql_10_p01_format_ok (>= (str.len sql_10_p01_text) 0) (<= (str.len sql_10_p01_text) 100))))
 (= sql_10_p01_accepted $x82)))
(assert
 sql_10_p01_accepted)
(assert
 (= sql_10_p01_text ""))
(assert
 sql_10_p01_present)
(assert
 sql_10_p01_type_ok)
(assert
 sql_10_p01_format_ok)
(check-sat)
