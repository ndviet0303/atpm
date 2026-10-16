; benchmark generated from python API
(set-info :status unknown)
(declare-fun parsed () Bool)
(declare-fun accepted () Bool)
(declare-fun claims_valid () Bool)
(declare-fun tag_valid () Bool)
(assert
 (let (($x22 (not accepted)))
 (or $x22 parsed)))
(assert
 (or accepted (not parsed)))
(assert
 (or accepted))
(assert
 (or (not tag_valid) (not claims_valid)))
(check-sat)
