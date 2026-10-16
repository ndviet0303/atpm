; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_45_p07_text () String)
(declare-fun sql_45_p07_format_ok () Bool)
(declare-fun sql_45_p07_type_ok () Bool)
(declare-fun sql_45_p07_present () Bool)
(declare-fun sql_45_p07_accepted () Bool)
(assert
 (let (($x21 (and sql_45_p07_present sql_45_p07_type_ok sql_45_p07_format_ok (>= (str.len sql_45_p07_text) 0) (<= (str.len sql_45_p07_text) 100))))
 (= sql_45_p07_accepted $x21)))
(assert
 sql_45_p07_accepted)
(assert
 (= sql_45_p07_text "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"))
(assert
 sql_45_p07_present)
(assert
 sql_45_p07_type_ok)
(assert
 sql_45_p07_format_ok)
(check-sat)
