; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_cat_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x34 (not all_bound)))
 (or $x34 bound_cat_id)))
(assert
 (let (($x7 (not bound_cat_id)))
 (or all_bound $x7)))
(assert
 (or executed))
(assert
 (let (($x7 (not bound_cat_id)))
 (or $x7)))
(assert
 (let (($x34 (not all_bound)))
(or $x34)))
(check-sat)
