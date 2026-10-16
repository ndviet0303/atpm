; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_title () Bool)
(declare-fun all_bound () Bool)
(declare-fun bound_author () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x8 (not all_bound)))
 (or $x8 bound_title)))
(assert
 (let (($x8 (not all_bound)))
 (or $x8 bound_author)))
(assert
 (let (($x9 (not bound_author)))
 (let (($x12 (not bound_title)))
 (or all_bound $x12 $x9))))
(assert
 (or executed))
(assert
 (let (($x12 (not bound_title)))
 (or $x12)))
(assert
 (let (($x9 (not bound_author)))
 (or $x9)))
(assert
 (let (($x8 (not all_bound)))
(or $x8)))
(check-sat)
