; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_36_p04_text () String)
(declare-fun sql_36_p04_format_ok () Bool)
(declare-fun sql_36_p04_type_ok () Bool)
(declare-fun sql_36_p04_present () Bool)
(declare-fun sql_36_p04_accepted () Bool)
(assert
 (let (($x53 (and sql_36_p04_present sql_36_p04_type_ok sql_36_p04_format_ok (>= (str.len sql_36_p04_text) 0) (<= (str.len sql_36_p04_text) 100))))
 (= sql_36_p04_accepted $x53)))
(assert
 sql_36_p04_accepted)
(assert
 (not sql_36_p04_type_ok))
(check-sat)
