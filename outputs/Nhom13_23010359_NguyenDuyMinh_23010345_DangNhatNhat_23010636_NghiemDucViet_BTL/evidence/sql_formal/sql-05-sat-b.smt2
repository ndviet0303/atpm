; benchmark generated from python API
(set-info :status unknown)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (or all_bound))
(assert
 (or executed))
(assert
 (let (($x23 (not all_bound)))
(or $x23)))
(check-sat)
