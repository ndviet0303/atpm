; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_cat_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x25 (not all_bound)))
 (or $x25 bound_cat_id)))
(assert
 (or all_bound (not bound_cat_id)))
(assert
 (or executed))
(assert
 (or bound_cat_id))
(assert
 (let (($x25 (not all_bound)))
(or $x25)))
(check-sat)
