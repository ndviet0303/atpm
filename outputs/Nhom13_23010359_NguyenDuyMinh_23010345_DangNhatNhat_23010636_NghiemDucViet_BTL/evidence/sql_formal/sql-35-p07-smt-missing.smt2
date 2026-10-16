; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_35_p07_text () String)
(declare-fun sql_35_p07_format_ok () Bool)
(declare-fun sql_35_p07_type_ok () Bool)
(declare-fun sql_35_p07_present () Bool)
(declare-fun sql_35_p07_accepted () Bool)
(assert
 (let (($x55 (and sql_35_p07_present sql_35_p07_type_ok sql_35_p07_format_ok (>= (str.len sql_35_p07_text) 0) (<= (str.len sql_35_p07_text) 100))))
 (= sql_35_p07_accepted $x55)))
(assert
 sql_35_p07_accepted)
(assert
 (not sql_35_p07_present))
(check-sat)
