; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_10_p07_text () String)
(declare-fun sql_10_p07_format_ok () Bool)
(declare-fun sql_10_p07_type_ok () Bool)
(declare-fun sql_10_p07_present () Bool)
(declare-fun sql_10_p07_accepted () Bool)
(assert
 (let (($x103 (and sql_10_p07_present sql_10_p07_type_ok sql_10_p07_format_ok (>= (str.len sql_10_p07_text) 0) (<= (str.len sql_10_p07_text) 50))))
 (= sql_10_p07_accepted $x103)))
(assert
 sql_10_p07_accepted)
(assert
 (not sql_10_p07_present))
(check-sat)
