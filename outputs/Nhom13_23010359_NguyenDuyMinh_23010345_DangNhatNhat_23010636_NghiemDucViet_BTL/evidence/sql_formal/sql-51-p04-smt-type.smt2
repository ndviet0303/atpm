; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_51_p04_text () String)
(declare-fun sql_51_p04_format_ok () Bool)
(declare-fun sql_51_p04_type_ok () Bool)
(declare-fun sql_51_p04_present () Bool)
(declare-fun sql_51_p04_accepted () Bool)
(assert
 (let (($x109 (and sql_51_p04_present sql_51_p04_type_ok sql_51_p04_format_ok (>= (str.len sql_51_p04_text) 0) (<= (str.len sql_51_p04_text) 100))))
 (= sql_51_p04_accepted $x109)))
(assert
 sql_51_p04_accepted)
(assert
 (not sql_51_p04_type_ok))
(check-sat)
