; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x12 (not all_bound)))
 (or $x12 bound_id)))
(assert
 (let (($x20 (not bound_id)))
 (or all_bound $x20)))
(assert
 (or executed))
(assert
 (let (($x20 (not bound_id)))
 (or $x20)))
(assert
 (let (($x12 (not all_bound)))
(or $x12)))
(check-sat)
