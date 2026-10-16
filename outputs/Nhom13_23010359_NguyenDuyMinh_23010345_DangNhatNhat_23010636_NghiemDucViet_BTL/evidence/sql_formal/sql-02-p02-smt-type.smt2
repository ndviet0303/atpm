; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_02_p02_text () String)
(declare-fun sql_02_p02_format_ok () Bool)
(declare-fun sql_02_p02_type_ok () Bool)
(declare-fun sql_02_p02_present () Bool)
(declare-fun sql_02_p02_accepted () Bool)
(assert
 (let (($x54 (and sql_02_p02_present sql_02_p02_type_ok sql_02_p02_format_ok (>= (str.len sql_02_p02_text) 0) (<= (str.len sql_02_p02_text) 50))))
 (= sql_02_p02_accepted $x54)))
(assert
 sql_02_p02_accepted)
(assert
 (not sql_02_p02_type_ok))
(check-sat)
