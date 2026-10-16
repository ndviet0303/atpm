; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_category_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x42 (not all_bound)))
 (or $x42 bound_category_id)))
(assert
 (let (($x39 (not bound_category_id)))
 (or all_bound $x39)))
(assert
 (or executed))
(assert
 (let (($x39 (not bound_category_id)))
 (or $x39)))
(assert
 (let (($x42 (not all_bound)))
(or $x42)))
(check-sat)
