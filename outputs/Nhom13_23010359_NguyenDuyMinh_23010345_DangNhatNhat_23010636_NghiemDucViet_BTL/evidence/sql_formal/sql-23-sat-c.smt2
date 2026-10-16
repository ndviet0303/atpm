; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x42 (not all_bound)))
 (or $x42 bound_id)))
(assert
 (or all_bound (not bound_id)))
(assert
 (or executed))
(assert
 (or bound_id))
(assert
 (or all_bound))
(check-sat)
