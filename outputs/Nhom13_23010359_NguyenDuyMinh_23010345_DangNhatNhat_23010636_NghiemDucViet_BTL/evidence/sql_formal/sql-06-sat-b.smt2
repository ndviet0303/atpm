; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_cat_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x25 (not all_bound)))
 (or $x25 bound_cat_id)))
(assert
 (let (($x32 (not bound_cat_id)))
 (or all_bound $x32)))
(assert
 (or executed))
(assert
 (let (($x32 (not bound_cat_id)))
 (or $x32)))
(assert
 (let (($x25 (not all_bound)))
(or $x25)))
(check-sat)
