; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_10_p09_text () String)
(declare-fun sql_10_p09_format_ok () Bool)
(declare-fun sql_10_p09_type_ok () Bool)
(declare-fun sql_10_p09_present () Bool)
(declare-fun sql_10_p09_accepted () Bool)
(assert
 (let (($x101 (and sql_10_p09_present sql_10_p09_type_ok sql_10_p09_format_ok (>= (str.len sql_10_p09_text) 0) (<= (str.len sql_10_p09_text) 30))))
 (= sql_10_p09_accepted $x101)))
(assert
 sql_10_p09_accepted)
(assert
 (let ((?x140 (str.len sql_10_p09_text)))
(= ?x140 31)))
(check-sat)
