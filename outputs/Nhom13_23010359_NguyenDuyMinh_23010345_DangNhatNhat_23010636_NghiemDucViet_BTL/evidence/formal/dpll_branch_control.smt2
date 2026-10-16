; benchmark generated from python API
(set-info :status unknown)
(declare-fun q () Bool)
(declare-fun p () Bool)
(assert
 (or p q))
(assert
 (let (($x34 (not q)))
 (or p $x34)))
(assert
 (let (($x36 (not p)))
 (or $x36 q)))
(assert
 (let (($x34 (not q)))
(let (($x36 (not p)))
(or $x36 $x34))))
(check-sat)
