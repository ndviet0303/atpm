; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_10_p03_text () String)
(declare-fun sql_10_p03_format_ok () Bool)
(declare-fun sql_10_p03_type_ok () Bool)
(declare-fun sql_10_p03_present () Bool)
(declare-fun sql_10_p03_accepted () Bool)
(assert
 (let (($x67 (and sql_10_p03_present sql_10_p03_type_ok sql_10_p03_format_ok (>= (str.len sql_10_p03_text) 0) (<= (str.len sql_10_p03_text) 50))))
 (= sql_10_p03_accepted $x67)))
(assert
 sql_10_p03_accepted)
(assert
 (not sql_10_p03_type_ok))
(check-sat)
