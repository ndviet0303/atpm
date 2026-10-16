; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_45_p04_text () String)
(declare-fun sql_45_p04_format_ok () Bool)
(declare-fun sql_45_p04_type_ok () Bool)
(declare-fun sql_45_p04_present () Bool)
(declare-fun sql_45_p04_accepted () Bool)
(assert
 (let (($x115 (and sql_45_p04_present sql_45_p04_type_ok sql_45_p04_format_ok (>= (str.len sql_45_p04_text) 0) (<= (str.len sql_45_p04_text) 100))))
 (= sql_45_p04_accepted $x115)))
(assert
 sql_45_p04_accepted)
(assert
 (= sql_45_p04_text ""))
(assert
 sql_45_p04_present)
(assert
 sql_45_p04_type_ok)
(assert
 sql_45_p04_format_ok)
(check-sat)
