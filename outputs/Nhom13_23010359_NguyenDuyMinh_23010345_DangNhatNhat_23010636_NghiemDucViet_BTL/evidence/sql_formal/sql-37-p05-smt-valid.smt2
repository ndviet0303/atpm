; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_37_p05_value () Int)
(declare-fun sql_37_p05_format_ok () Bool)
(declare-fun sql_37_p05_type_ok () Bool)
(declare-fun sql_37_p05_present () Bool)
(declare-fun sql_37_p05_accepted () Bool)
(assert
 (let (($x18 (and sql_37_p05_present sql_37_p05_type_ok sql_37_p05_format_ok (>= sql_37_p05_value 1) (<= sql_37_p05_value 2147483647))))
 (= sql_37_p05_accepted $x18)))
(assert
 sql_37_p05_accepted)
(assert
 (= 2147483647 sql_37_p05_value))
(assert
 sql_37_p05_present)
(assert
 sql_37_p05_type_ok)
(assert
 sql_37_p05_format_ok)
(check-sat)
