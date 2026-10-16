; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_35_p04_text () String)
(declare-fun sql_35_p04_format_ok () Bool)
(declare-fun sql_35_p04_type_ok () Bool)
(declare-fun sql_35_p04_present () Bool)
(declare-fun sql_35_p04_accepted () Bool)
(assert
 (let (($x120 (and sql_35_p04_present sql_35_p04_type_ok sql_35_p04_format_ok (>= (str.len sql_35_p04_text) 0) (<= (str.len sql_35_p04_text) 100))))
 (= sql_35_p04_accepted $x120)))
(assert
 sql_35_p04_accepted)
(assert
 (not sql_35_p04_format_ok))
(check-sat)
