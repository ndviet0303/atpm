; benchmark generated from python API
(set-info :status unknown)
(declare-fun sql_10_p02_value () Int)
(declare-fun sql_10_p02_format_ok () Bool)
(declare-fun sql_10_p02_type_ok () Bool)
(declare-fun sql_10_p02_present () Bool)
(declare-fun sql_10_p02_accepted () Bool)
(assert
 (let (($x97 (and sql_10_p02_present sql_10_p02_type_ok sql_10_p02_format_ok (>= sql_10_p02_value 1) (<= sql_10_p02_value 2147483647))))
 (= sql_10_p02_accepted $x97)))
(assert
 sql_10_p02_accepted)
(assert
 (= sql_10_p02_value 2147483648))
(check-sat)
