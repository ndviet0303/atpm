; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_35_p03_text () String)
(declare-fun sql_35_p03_format_ok () Bool)
(declare-fun sql_35_p03_type_ok () Bool)
(declare-fun sql_35_p03_present () Bool)
(declare-fun sql_35_p03_accepted () Bool)
(assert
 (let (($x142 (and sql_35_p03_present sql_35_p03_type_ok sql_35_p03_format_ok (>= (str.len sql_35_p03_text) 0) (<= (str.len sql_35_p03_text) 10))))
 (= sql_35_p03_accepted $x142)))
(assert
 sql_35_p03_accepted)
(assert
 (= sql_35_p03_text "AAAAAAAAAA"))
(assert
 sql_35_p03_present)
(assert
 sql_35_p03_type_ok)
(assert
 sql_35_p03_format_ok)
(check-sat)
