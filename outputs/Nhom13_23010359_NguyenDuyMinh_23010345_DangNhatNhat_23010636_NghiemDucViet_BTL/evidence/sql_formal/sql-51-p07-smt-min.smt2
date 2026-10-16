; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_51_p07_text () String)
(declare-fun sql_51_p07_format_ok () Bool)
(declare-fun sql_51_p07_type_ok () Bool)
(declare-fun sql_51_p07_present () Bool)
(declare-fun sql_51_p07_accepted () Bool)
(assert
 (let (($x61 (and sql_51_p07_present sql_51_p07_type_ok sql_51_p07_format_ok (>= (str.len sql_51_p07_text) 0) (<= (str.len sql_51_p07_text) 100))))
 (= sql_51_p07_accepted $x61)))
(assert
 sql_51_p07_accepted)
(assert
 (= sql_51_p07_text ""))
(assert
 sql_51_p07_present)
(assert
 sql_51_p07_type_ok)
(assert
 sql_51_p07_format_ok)
(check-sat)
