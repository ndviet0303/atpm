; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_02_p01_text () String)
(declare-fun sql_02_p01_format_ok () Bool)
(declare-fun sql_02_p01_type_ok () Bool)
(declare-fun sql_02_p01_present () Bool)
(declare-fun sql_02_p01_accepted () Bool)
(assert
 (let (($x68 (and sql_02_p01_present sql_02_p01_type_ok sql_02_p01_format_ok (>= (str.len sql_02_p01_text) 0) (<= (str.len sql_02_p01_text) 100))))
 (= sql_02_p01_accepted $x68)))
(assert
 sql_02_p01_accepted)
(assert
 (let ((?x19 (str.len sql_02_p01_text)))
(= ?x19 101)))
(check-sat)
