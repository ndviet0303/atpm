; benchmark generated from python API
(set-info :status unknown)
(declare-fun len () Int)
(assert
 (let (($x1494 (< (- len 16) 0)))
(let (($x147 (= len 5)))
(and $x147 $x1494))))
(check-sat)
