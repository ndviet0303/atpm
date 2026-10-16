; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_35_p06_text () String)
(declare-fun sql_35_p06_format_ok () Bool)
(declare-fun sql_35_p06_type_ok () Bool)
(declare-fun sql_35_p06_present () Bool)
(declare-fun sql_35_p06_accepted () Bool)
(assert
 (let (($x12 (and sql_35_p06_present sql_35_p06_type_ok sql_35_p06_format_ok (>= (str.len sql_35_p06_text) 0) (<= (str.len sql_35_p06_text) 100))))
 (= sql_35_p06_accepted $x12)))
(assert
 sql_35_p06_accepted)
(assert
 (= sql_35_p06_text "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"))
(assert
 sql_35_p06_present)
(assert
 sql_35_p06_type_ok)
(assert
 sql_35_p06_format_ok)
(check-sat)
