; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_50_p03_text () String)
(declare-fun sql_50_p03_format_ok () Bool)
(declare-fun sql_50_p03_type_ok () Bool)
(declare-fun sql_50_p03_present () Bool)
(declare-fun sql_50_p03_accepted () Bool)
(assert
 (let (($x73 (and sql_50_p03_present sql_50_p03_type_ok sql_50_p03_format_ok (>= (str.len sql_50_p03_text) 0) (<= (str.len sql_50_p03_text) 10))))
 (= sql_50_p03_accepted $x73)))
(assert
 sql_50_p03_accepted)
(assert
 (= sql_50_p03_text ""))
(assert
 sql_50_p03_present)
(assert
 sql_50_p03_type_ok)
(assert
 sql_50_p03_format_ok)
(check-sat)
