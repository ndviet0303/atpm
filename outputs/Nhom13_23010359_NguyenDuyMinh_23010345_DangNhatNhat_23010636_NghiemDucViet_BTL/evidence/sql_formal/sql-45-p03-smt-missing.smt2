; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_45_p03_text () String)
(declare-fun sql_45_p03_format_ok () Bool)
(declare-fun sql_45_p03_type_ok () Bool)
(declare-fun sql_45_p03_present () Bool)
(declare-fun sql_45_p03_accepted () Bool)
(assert
 (let (($x47 (and sql_45_p03_present sql_45_p03_type_ok sql_45_p03_format_ok (>= (str.len sql_45_p03_text) 0) (<= (str.len sql_45_p03_text) 10))))
 (= sql_45_p03_accepted $x47)))
(assert
 sql_45_p03_accepted)
(assert
 (not sql_45_p03_present))
(check-sat)
