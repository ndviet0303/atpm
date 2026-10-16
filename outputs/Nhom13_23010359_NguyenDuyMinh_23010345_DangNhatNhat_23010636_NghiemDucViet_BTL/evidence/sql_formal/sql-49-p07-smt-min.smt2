; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_49_p07_text () String)
(declare-fun sql_49_p07_format_ok () Bool)
(declare-fun sql_49_p07_type_ok () Bool)
(declare-fun sql_49_p07_present () Bool)
(declare-fun sql_49_p07_accepted () Bool)
(assert
 (let (($x15 (and sql_49_p07_present sql_49_p07_type_ok sql_49_p07_format_ok (>= (str.len sql_49_p07_text) 0) (<= (str.len sql_49_p07_text) 50))))
 (= sql_49_p07_accepted $x15)))
(assert
 sql_49_p07_accepted)
(assert
 (= sql_49_p07_text ""))
(assert
 sql_49_p07_present)
(assert
 sql_49_p07_type_ok)
(assert
 sql_49_p07_format_ok)
(check-sat)
