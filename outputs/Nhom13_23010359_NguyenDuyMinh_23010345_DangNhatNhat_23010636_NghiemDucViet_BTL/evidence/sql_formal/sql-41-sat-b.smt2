; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_cat_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x43 (not all_bound)))
 (or $x43 bound_cat_id)))
(assert
 (let (($x40 (not bound_cat_id)))
 (or all_bound $x40)))
(assert
 (or executed))
(assert
 (let (($x40 (not bound_cat_id)))
 (or $x40)))
(assert
 (let (($x43 (not all_bound)))
(or $x43)))
(check-sat)
