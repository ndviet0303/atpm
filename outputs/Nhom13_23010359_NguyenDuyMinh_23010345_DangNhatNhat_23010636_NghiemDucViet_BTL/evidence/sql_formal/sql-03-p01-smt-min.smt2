; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_03_p01_value () Int)
(declare-fun sql_03_p01_format_ok () Bool)
(declare-fun sql_03_p01_type_ok () Bool)
(declare-fun sql_03_p01_present () Bool)
(declare-fun sql_03_p01_accepted () Bool)
(assert
 (let (($x74 (and sql_03_p01_present sql_03_p01_type_ok sql_03_p01_format_ok (>= sql_03_p01_value 1) (<= sql_03_p01_value 2147483647))))
 (= sql_03_p01_accepted $x74)))
(assert
 sql_03_p01_accepted)
(assert
 (= sql_03_p01_value 0))
(check-sat)
