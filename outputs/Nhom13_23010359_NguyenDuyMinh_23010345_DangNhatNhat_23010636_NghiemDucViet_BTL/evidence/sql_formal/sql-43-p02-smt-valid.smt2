; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_43_p02_value () Int)
(declare-fun sql_43_p02_format_ok () Bool)
(declare-fun sql_43_p02_type_ok () Bool)
(declare-fun sql_43_p02_present () Bool)
(declare-fun sql_43_p02_accepted () Bool)
(assert
 (let (($x85 (and sql_43_p02_present sql_43_p02_type_ok sql_43_p02_format_ok (>= sql_43_p02_value 1) (<= sql_43_p02_value 2147483647))))
 (= sql_43_p02_accepted $x85)))
(assert
 sql_43_p02_accepted)
(assert
 (= 2147483647 sql_43_p02_value))
(assert
 sql_43_p02_present)
(assert
 sql_43_p02_type_ok)
(assert
 sql_43_p02_format_ok)
(check-sat)
