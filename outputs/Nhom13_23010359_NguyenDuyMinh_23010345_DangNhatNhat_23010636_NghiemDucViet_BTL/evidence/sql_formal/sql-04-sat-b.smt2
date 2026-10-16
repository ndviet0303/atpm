; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_cat_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x26 (not all_bound)))
 (or $x26 bound_cat_id)))
(assert
 (let (($x12 (not bound_cat_id)))
 (or all_bound $x12)))
(assert
 (or executed))
(assert
 (let (($x12 (not bound_cat_id)))
 (or $x12)))
(assert
 (let (($x26 (not all_bound)))
(or $x26)))
(check-sat)
