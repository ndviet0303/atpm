; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_47_p01_value () Int)
(declare-fun sql_47_p01_format_ok () Bool)
(declare-fun sql_47_p01_type_ok () Bool)
(declare-fun sql_47_p01_present () Bool)
(declare-fun sql_47_p01_accepted () Bool)
(assert
 (let (($x29 (and sql_47_p01_present sql_47_p01_type_ok sql_47_p01_format_ok (>= sql_47_p01_value 1) (<= sql_47_p01_value 2147483647))))
 (= sql_47_p01_accepted $x29)))
(assert
 sql_47_p01_accepted)
(assert
 (= sql_47_p01_value 0))
(check-sat)
