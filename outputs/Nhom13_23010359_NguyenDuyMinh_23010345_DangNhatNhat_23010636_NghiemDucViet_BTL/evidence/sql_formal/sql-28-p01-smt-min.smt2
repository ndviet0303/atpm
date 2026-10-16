; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_28_p01_value () Int)
(declare-fun sql_28_p01_format_ok () Bool)
(declare-fun sql_28_p01_type_ok () Bool)
(declare-fun sql_28_p01_present () Bool)
(declare-fun sql_28_p01_accepted () Bool)
(assert
 (let (($x24 (and sql_28_p01_present sql_28_p01_type_ok sql_28_p01_format_ok (>= sql_28_p01_value 1) (<= sql_28_p01_value 2147483647))))
 (= sql_28_p01_accepted $x24)))
(assert
 sql_28_p01_accepted)
(assert
 (= sql_28_p01_value 0))
(check-sat)
