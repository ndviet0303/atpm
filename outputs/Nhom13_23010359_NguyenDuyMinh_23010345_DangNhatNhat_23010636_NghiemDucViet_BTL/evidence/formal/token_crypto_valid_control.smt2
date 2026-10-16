; benchmark generated from python API
(set-info :status unknown)
(declare-fun parsed () Bool)
(declare-fun accepted () Bool)
(declare-fun tag_valid () Bool)
(declare-fun claims_valid () Bool)
(assert
 (let (($x5 (not accepted)))
 (or $x5 parsed)))
(assert
 (let (($x5 (not accepted)))
 (or $x5 tag_valid)))
(assert
 (let (($x5 (not accepted)))
 (or $x5 claims_valid)))
(assert
 (let (($x15 (not claims_valid)))
 (let (($x27 (not tag_valid)))
 (let (($x33 (not parsed)))
 (or accepted $x33 $x27 $x15)))))
(assert
 (or accepted))
(assert
 (or parsed))
(assert
 (or tag_valid))
(assert
 (or claims_valid))
(check-sat)
