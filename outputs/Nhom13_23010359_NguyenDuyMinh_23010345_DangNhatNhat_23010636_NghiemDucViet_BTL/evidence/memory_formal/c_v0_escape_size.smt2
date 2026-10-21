; benchmark generated from python API
(set-info :status unknown)
(declare-fun n () Int)
(declare-fun lt () Int)
(assert
 (let (($x2999 (= lt 2)))
(let (($x1986 (= n 25)))
(and $x1986 $x2999 (> (+ (+ n (* 3 lt)) 1) (+ n 1))))))
(check-sat)
