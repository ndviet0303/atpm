; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_cat_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x37 (not all_bound)))
 (or $x37 bound_cat_id)))
(assert
 (let (($x22 (not bound_cat_id)))
 (or all_bound $x22)))
(assert
 (or executed))
(assert
 (let (($x22 (not bound_cat_id)))
 (or $x22)))
(assert
 (let (($x37 (not all_bound)))
(or $x37)))
(check-sat)
