; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_37_p01_text () String)
(declare-fun sql_37_p01_format_ok () Bool)
(declare-fun sql_37_p01_type_ok () Bool)
(declare-fun sql_37_p01_present () Bool)
(declare-fun sql_37_p01_accepted () Bool)
(assert
 (let (($x104 (and sql_37_p01_present sql_37_p01_type_ok sql_37_p01_format_ok (>= (str.len sql_37_p01_text) 0) (<= (str.len sql_37_p01_text) 100))))
 (= sql_37_p01_accepted $x104)))
(assert
 sql_37_p01_accepted)
(assert
 (not sql_37_p01_format_ok))
(check-sat)
