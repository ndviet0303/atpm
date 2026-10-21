; benchmark generated from python API
(set-info :status unknown)
(declare-fun n () Int)
(declare-fun amp () Int)
(declare-fun gt () Int)
(declare-fun lt () Int)
(assert
 (let ((?x2556 (+ (+ (+ (+ n (* 3 lt)) (* 3 gt)) (* 4 amp)) 1)))
(let (($x905 (>= amp 0)))
(let (($x992 (>= gt 0)))
(let (($x1930 (>= lt 0)))
(let (($x1893 (>= n 0)))
(and $x1893 (< n 4096) $x1930 $x992 $x905 (<= (+ (+ lt gt) amp) n) (> ?x2556 (+ (* 5 n) 1)))))))))
(check-sat)
