; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_14_p02_text () String)
(declare-fun sql_14_p02_format_ok () Bool)
(declare-fun sql_14_p02_type_ok () Bool)
(declare-fun sql_14_p02_present () Bool)
(declare-fun sql_14_p02_accepted () Bool)
(assert
 (let (($x72 (and sql_14_p02_present sql_14_p02_type_ok sql_14_p02_format_ok (>= (str.len sql_14_p02_text) 0) (<= (str.len sql_14_p02_text) 100))))
 (= sql_14_p02_accepted $x72)))
(assert
 sql_14_p02_accepted)
(assert
 (let ((?x35 (str.len sql_14_p02_text)))
(= ?x35 101)))
(check-sat)
