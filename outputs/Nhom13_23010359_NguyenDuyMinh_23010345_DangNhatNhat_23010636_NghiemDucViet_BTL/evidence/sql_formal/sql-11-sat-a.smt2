; benchmark generated from python API
(set-info :status unknown)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (or all_bound))
(assert
 (or executed))
(assert
 (let (($x14 (not all_bound)))
(or $x14)))
(check-sat)
