; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_51_p05_text () String)
(declare-fun sql_51_p05_format_ok () Bool)
(declare-fun sql_51_p05_type_ok () Bool)
(declare-fun sql_51_p05_present () Bool)
(declare-fun sql_51_p05_accepted () Bool)
(assert
 (let (($x36 (and sql_51_p05_present sql_51_p05_type_ok sql_51_p05_format_ok (>= (str.len sql_51_p05_text) 0) (<= (str.len sql_51_p05_text) 100))))
 (= sql_51_p05_accepted $x36)))
(assert
 sql_51_p05_accepted)
(assert
 (= sql_51_p05_text "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"))
(assert
 sql_51_p05_present)
(assert
 sql_51_p05_type_ok)
(assert
 sql_51_p05_format_ok)
(check-sat)
