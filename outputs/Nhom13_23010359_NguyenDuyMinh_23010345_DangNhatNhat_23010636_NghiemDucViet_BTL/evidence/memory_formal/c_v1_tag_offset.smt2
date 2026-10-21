; benchmark generated from python API
(set-info :status unknown)
(declare-fun len () Int)
(assert
 (let (($x1494 (< (- len 16) 0)))
(let (($x3417 (>= len 16)))
(and $x3417 (<= len 4096) $x1494))))
(check-sat)
