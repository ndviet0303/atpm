; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_get_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x13 (not all_bound)))
 (or $x13 bound_get_id)))
(assert
 (or all_bound (not bound_get_id)))
(assert
 (or executed))
(assert
 (or bound_get_id))
(assert
 (let (($x13 (not all_bound)))
(or $x13)))
(check-sat)
