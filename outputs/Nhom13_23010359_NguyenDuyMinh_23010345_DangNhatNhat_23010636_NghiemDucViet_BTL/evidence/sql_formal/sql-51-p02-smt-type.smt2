; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_51_p02_text () String)
(declare-fun sql_51_p02_format_ok () Bool)
(declare-fun sql_51_p02_type_ok () Bool)
(declare-fun sql_51_p02_present () Bool)
(declare-fun sql_51_p02_accepted () Bool)
(assert
 (let (($x122 (and sql_51_p02_present sql_51_p02_type_ok sql_51_p02_format_ok (>= (str.len sql_51_p02_text) 0) (<= (str.len sql_51_p02_text) 100))))
 (= sql_51_p02_accepted $x122)))
(assert
 sql_51_p02_accepted)
(assert
 (not sql_51_p02_type_ok))
(check-sat)
