; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_35_p05_text () String)
(declare-fun sql_35_p05_format_ok () Bool)
(declare-fun sql_35_p05_type_ok () Bool)
(declare-fun sql_35_p05_present () Bool)
(declare-fun sql_35_p05_accepted () Bool)
(assert
 (let (($x27 (and sql_35_p05_present sql_35_p05_type_ok sql_35_p05_format_ok (>= (str.len sql_35_p05_text) 0) (<= (str.len sql_35_p05_text) 100))))
 (= sql_35_p05_accepted $x27)))
(assert
 sql_35_p05_accepted)
(assert
 (not sql_35_p05_type_ok))
(check-sat)
