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
 (= 2147483647 sql_03_p01_value))
(assert
 sql_03_p01_present)
(assert
 sql_03_p01_type_ok)
(assert
 sql_03_p01_format_ok)
(check-sat)
