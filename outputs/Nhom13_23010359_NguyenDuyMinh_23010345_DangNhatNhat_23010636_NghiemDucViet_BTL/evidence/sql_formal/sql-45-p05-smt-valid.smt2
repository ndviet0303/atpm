; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_45_p05_text () String)
(declare-fun sql_45_p05_format_ok () Bool)
(declare-fun sql_45_p05_type_ok () Bool)
(declare-fun sql_45_p05_present () Bool)
(declare-fun sql_45_p05_accepted () Bool)
(assert
 (let (($x118 (and sql_45_p05_present sql_45_p05_type_ok sql_45_p05_format_ok (>= (str.len sql_45_p05_text) 0) (<= (str.len sql_45_p05_text) 100))))
 (= sql_45_p05_accepted $x118)))
(assert
 sql_45_p05_accepted)
(assert
 (= sql_45_p05_text "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"))
(assert
 sql_45_p05_present)
(assert
 sql_45_p05_type_ok)
(assert
 sql_45_p05_format_ok)
(check-sat)
