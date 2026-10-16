; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_35_p01_text () String)
(declare-fun sql_35_p01_format_ok () Bool)
(declare-fun sql_35_p01_type_ok () Bool)
(declare-fun sql_35_p01_present () Bool)
(declare-fun sql_35_p01_accepted () Bool)
(assert
 (let (($x60 (and sql_35_p01_present sql_35_p01_type_ok sql_35_p01_format_ok (>= (str.len sql_35_p01_text) 0) (<= (str.len sql_35_p01_text) 100))))
 (= sql_35_p01_accepted $x60)))
(assert
 sql_35_p01_accepted)
(assert
 (let ((?x87 (str.len sql_35_p01_text)))
(= ?x87 101)))
(check-sat)
