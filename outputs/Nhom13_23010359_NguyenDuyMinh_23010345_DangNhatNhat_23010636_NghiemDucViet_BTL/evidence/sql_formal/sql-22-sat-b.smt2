; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x36 (not all_bound)))
 (or $x36 bound_id)))
(assert
 (let (($x45 (not bound_id)))
 (or all_bound $x45)))
(assert
 (or executed))
(assert
 (let (($x45 (not bound_id)))
 (or $x45)))
(assert
 (let (($x36 (not all_bound)))
(or $x36)))
(check-sat)
