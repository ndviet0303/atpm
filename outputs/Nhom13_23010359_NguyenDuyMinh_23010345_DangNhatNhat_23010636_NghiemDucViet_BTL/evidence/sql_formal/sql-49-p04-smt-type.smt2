; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_49_p04_value () Int)
(declare-fun sql_49_p04_format_ok () Bool)
(declare-fun sql_49_p04_type_ok () Bool)
(declare-fun sql_49_p04_present () Bool)
(declare-fun sql_49_p04_accepted () Bool)
(assert
 (let (($x49 (and sql_49_p04_present sql_49_p04_type_ok sql_49_p04_format_ok (>= sql_49_p04_value 0) (<= sql_49_p04_value 2147483647))))
 (= sql_49_p04_accepted $x49)))
(assert
 sql_49_p04_accepted)
(assert
 (not sql_49_p04_type_ok))
(check-sat)
