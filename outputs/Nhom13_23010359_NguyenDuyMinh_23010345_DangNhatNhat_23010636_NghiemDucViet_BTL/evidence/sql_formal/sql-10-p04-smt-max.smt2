; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_10_p04_value () Int)
(declare-fun sql_10_p04_format_ok () Bool)
(declare-fun sql_10_p04_type_ok () Bool)
(declare-fun sql_10_p04_present () Bool)
(declare-fun sql_10_p04_accepted () Bool)
(assert
 (let (($x13 (and sql_10_p04_present sql_10_p04_type_ok sql_10_p04_format_ok (>= sql_10_p04_value 0) (<= sql_10_p04_value 2147483647))))
 (= sql_10_p04_accepted $x13)))
(assert
 sql_10_p04_accepted)
(assert
 (= sql_10_p04_value 2147483648))
(check-sat)
