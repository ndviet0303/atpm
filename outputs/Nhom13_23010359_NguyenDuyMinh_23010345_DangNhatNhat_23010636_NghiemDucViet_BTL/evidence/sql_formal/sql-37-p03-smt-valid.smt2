; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_37_p03_text () String)
(declare-fun sql_37_p03_format_ok () Bool)
(declare-fun sql_37_p03_type_ok () Bool)
(declare-fun sql_37_p03_present () Bool)
(declare-fun sql_37_p03_accepted () Bool)
(assert
 (let (($x103 (and sql_37_p03_present sql_37_p03_type_ok sql_37_p03_format_ok (>= (str.len sql_37_p03_text) 0) (<= (str.len sql_37_p03_text) 100))))
 (= sql_37_p03_accepted $x103)))
(assert
 sql_37_p03_accepted)
(assert
 (= sql_37_p03_text "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"))
(assert
 sql_37_p03_present)
(assert
 sql_37_p03_type_ok)
(assert
 sql_37_p03_format_ok)
(check-sat)
