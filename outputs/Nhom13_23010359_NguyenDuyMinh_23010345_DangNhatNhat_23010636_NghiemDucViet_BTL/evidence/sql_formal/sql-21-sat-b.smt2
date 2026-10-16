; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x13 (not all_bound)))
 (or $x13 bound_id)))
(assert
 (let (($x45 (not bound_id)))
 (or all_bound $x45)))
(assert
 (or executed))
(assert
 (let (($x45 (not bound_id)))
 (or $x45)))
(assert
 (let (($x13 (not all_bound)))
(or $x13)))
(check-sat)
