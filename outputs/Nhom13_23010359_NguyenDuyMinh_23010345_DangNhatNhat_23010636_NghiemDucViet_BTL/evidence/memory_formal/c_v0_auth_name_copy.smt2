; benchmark generated from python API
(set-info :status unknown)
(declare-fun len () Int)
(assert
 (let (($x14 (= len 44)))
(and $x14 (> (+ len 1) 32))))
(check-sat)
