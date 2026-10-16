; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_37_p04_text () String)
(declare-fun sql_37_p04_format_ok () Bool)
(declare-fun sql_37_p04_type_ok () Bool)
(declare-fun sql_37_p04_present () Bool)
(declare-fun sql_37_p04_accepted () Bool)
(assert
 (let (($x136 (and sql_37_p04_present sql_37_p04_type_ok sql_37_p04_format_ok (>= (str.len sql_37_p04_text) 0) (<= (str.len sql_37_p04_text) 100))))
 (= sql_37_p04_accepted $x136)))
(assert
 sql_37_p04_accepted)
(assert
 (let ((?x41 (str.len sql_37_p04_text)))
(= ?x41 101)))
(check-sat)
