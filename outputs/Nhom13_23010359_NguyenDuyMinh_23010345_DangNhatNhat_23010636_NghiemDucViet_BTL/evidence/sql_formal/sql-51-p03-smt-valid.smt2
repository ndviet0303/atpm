; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_51_p03_text () String)
(declare-fun sql_51_p03_format_ok () Bool)
(declare-fun sql_51_p03_type_ok () Bool)
(declare-fun sql_51_p03_present () Bool)
(declare-fun sql_51_p03_accepted () Bool)
(assert
 (let (($x27 (and sql_51_p03_present sql_51_p03_type_ok sql_51_p03_format_ok (>= (str.len sql_51_p03_text) 0) (<= (str.len sql_51_p03_text) 10))))
 (= sql_51_p03_accepted $x27)))
(assert
 sql_51_p03_accepted)
(assert
 (= sql_51_p03_text "AAAAAAAAAA"))
(assert
 sql_51_p03_present)
(assert
 sql_51_p03_type_ok)
(assert
 sql_51_p03_format_ok)
(check-sat)
