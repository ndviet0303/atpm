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
 (let (($x25 (not bound_author)))
 (let (($x26 (not bound_title)))
 (or all_bound $x26 $x25))))
(assert
 (or executed))
(assert
 (or bound_title))
(assert
 (or bound_author))
(assert
 (or all_bound))
(check-sat)
