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
 (or all_bound (not bound_member_id) (not bound_due_date)))
(assert
 (or executed))
(assert
 (or bound_member_id))
(assert
 (or bound_due_date))
(assert
 (let (($x33 (not all_bound)))
(or $x33)))
(check-sat)
