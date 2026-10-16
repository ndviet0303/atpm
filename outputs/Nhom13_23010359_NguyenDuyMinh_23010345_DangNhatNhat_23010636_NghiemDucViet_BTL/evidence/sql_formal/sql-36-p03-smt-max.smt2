; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_36_p03_text () String)
(declare-fun sql_36_p03_format_ok () Bool)
(declare-fun sql_36_p03_type_ok () Bool)
(declare-fun sql_36_p03_present () Bool)
(declare-fun sql_36_p03_accepted () Bool)
(assert
 (let (($x49 (and sql_36_p03_present sql_36_p03_type_ok sql_36_p03_format_ok (>= (str.len sql_36_p03_text) 0) (<= (str.len sql_36_p03_text) 100))))
 (= sql_36_p03_accepted $x49)))
(assert
 sql_36_p03_accepted)
(assert
 (let ((?x37 (str.len sql_36_p03_text)))
(= ?x37 101)))
(check-sat)
