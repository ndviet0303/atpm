; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_get_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x25 (not all_bound)))
 (or $x25 bound_get_id)))
(assert
 (let (($x36 (not bound_get_id)))
 (or all_bound $x36)))
(assert
 (or executed))
(assert
 (let (($x36 (not bound_get_id)))
 (or $x36)))
(assert
 (let (($x25 (not all_bound)))
(or $x25)))
(check-sat)
