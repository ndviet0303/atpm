; benchmark generated from python API
(set-info :status unknown)
(declare-fun parsed () Bool)
(declare-fun accepted () Bool)
(declare-fun tag_valid () Bool)
(declare-fun claims_valid () Bool)
(assert
 (let (($x9 (not accepted)))
 (or $x9 parsed)))
(assert
 (let (($x9 (not accepted)))
 (or $x9 tag_valid)))
(assert
 (let (($x9 (not accepted)))
 (or $x9 claims_valid)))
(assert
 (let (($x29 (not claims_valid)))
 (let (($x5 (not tag_valid)))
 (let (($x25 (not parsed)))
 (or accepted $x25 $x5 $x29)))))
(assert
 (or accepted))
(assert
 (let (($x29 (not claims_valid)))
(let (($x5 (not tag_valid)))
(or $x5 $x29))))
(check-sat)
