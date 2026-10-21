; benchmark generated from python API
(set-info :status unknown)
(declare-fun ulen () Int)
(declare-fun len () Int)
(assert
 (let (($x3030 (>= len 0)))
(and $x3030 (= ulen (ite (< len 32) len 32)) (and (distinct ulen 32) true) (> (+ ulen 1) 32))))
(check-sat)
