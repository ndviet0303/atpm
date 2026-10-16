; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_49_p01_text () String)
(declare-fun sql_49_p01_format_ok () Bool)
(declare-fun sql_49_p01_type_ok () Bool)
(declare-fun sql_49_p01_present () Bool)
(declare-fun sql_49_p01_accepted () Bool)
(assert
 (let (($x20 (and sql_49_p01_present sql_49_p01_type_ok sql_49_p01_format_ok (>= (str.len sql_49_p01_text) 0) (<= (str.len sql_49_p01_text) 100))))
 (= sql_49_p01_accepted $x20)))
(assert
 sql_49_p01_accepted)
(assert
 (not sql_49_p01_present))
(check-sat)
