; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_36_p02_text () String)
(declare-fun sql_36_p02_format_ok () Bool)
(declare-fun sql_36_p02_type_ok () Bool)
(declare-fun sql_36_p02_present () Bool)
(declare-fun sql_36_p02_accepted () Bool)
(assert
 (let (($x25 (and sql_36_p02_present sql_36_p02_type_ok sql_36_p02_format_ok (>= (str.len sql_36_p02_text) 0) (<= (str.len sql_36_p02_text) 100))))
 (= sql_36_p02_accepted $x25)))
(assert
 sql_36_p02_accepted)
(assert
 (let ((?x54 (str.len sql_36_p02_text)))
(= ?x54 101)))
(check-sat)
