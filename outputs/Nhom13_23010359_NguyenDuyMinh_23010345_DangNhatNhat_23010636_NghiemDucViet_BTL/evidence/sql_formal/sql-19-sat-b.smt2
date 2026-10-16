; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_cat_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x13 (not all_bound)))
 (or $x13 bound_cat_id)))
(assert
 (let (($x14 (not bound_cat_id)))
 (or all_bound $x14)))
(assert
 (or executed))
(assert
 (let (($x14 (not bound_cat_id)))
 (or $x14)))
(assert
 (let (($x13 (not all_bound)))
(or $x13)))
(check-sat)
