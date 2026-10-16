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
 (let (($x12 (not bound_author)))
 (let (($x21 (not bound_title)))
 (or all_bound $x21 $x12))))
(assert
 (or executed))
(assert
 (or bound_title))
(assert
 (or bound_author))
(assert
 (let (($x8 (not all_bound)))
(or $x8)))
(check-sat)
