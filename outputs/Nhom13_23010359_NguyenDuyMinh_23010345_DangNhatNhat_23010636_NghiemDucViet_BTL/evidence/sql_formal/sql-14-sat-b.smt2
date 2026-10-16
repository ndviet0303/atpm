; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_member_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun bound_due_date () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x33 (not all_bound)))
 (or $x33 bound_member_id)))
(assert
 (let (($x33 (not all_bound)))
 (or $x33 bound_due_date)))
(assert
 (let (($x28 (not bound_due_date)))
 (let (($x42 (not bound_member_id)))
 (or all_bound $x42 $x28))))
(assert
 (or executed))
(assert
 (let (($x42 (not bound_member_id)))
 (or $x42)))
(assert
 (let (($x28 (not bound_due_date)))
 (or $x28)))
(assert
 (let (($x33 (not all_bound)))
(or $x33)))
(check-sat)
