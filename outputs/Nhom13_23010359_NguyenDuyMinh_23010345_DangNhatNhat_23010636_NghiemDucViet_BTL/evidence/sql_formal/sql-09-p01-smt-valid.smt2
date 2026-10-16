; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_09_p01_value () Int)
(declare-fun sql_09_p01_format_ok () Bool)
(declare-fun sql_09_p01_type_ok () Bool)
(declare-fun sql_09_p01_present () Bool)
(declare-fun sql_09_p01_accepted () Bool)
(assert
 (let (($x86 (and sql_09_p01_present sql_09_p01_type_ok sql_09_p01_format_ok (>= sql_09_p01_value 1) (<= sql_09_p01_value 2147483647))))
 (= sql_09_p01_accepted $x86)))
(assert
 sql_09_p01_accepted)
(assert
 (= 2147483647 sql_09_p01_value))
(assert
 sql_09_p01_present)
(assert
 sql_09_p01_type_ok)
(assert
 sql_09_p01_format_ok)
(check-sat)
