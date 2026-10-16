; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_45_p06_text () String)
(declare-fun sql_45_p06_format_ok () Bool)
(declare-fun sql_45_p06_type_ok () Bool)
(declare-fun sql_45_p06_present () Bool)
(declare-fun sql_45_p06_accepted () Bool)
(assert
 (let (($x123 (and sql_45_p06_present sql_45_p06_type_ok sql_45_p06_format_ok (>= (str.len sql_45_p06_text) 0) (<= (str.len sql_45_p06_text) 100))))
 (= sql_45_p06_accepted $x123)))
(assert
 sql_45_p06_accepted)
(assert
 (let ((?x113 (str.len sql_45_p06_text)))
(= ?x113 101)))
(check-sat)
