; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x19 (not all_bound)))
 (or $x19 bound_id)))
(assert
 (let (($x9 (not bound_id)))
 (or all_bound $x9)))
(assert
 (or executed))
(assert
 (let (($x9 (not bound_id)))
 (or $x9)))
(assert
 (let (($x19 (not all_bound)))
(or $x19)))
(check-sat)
