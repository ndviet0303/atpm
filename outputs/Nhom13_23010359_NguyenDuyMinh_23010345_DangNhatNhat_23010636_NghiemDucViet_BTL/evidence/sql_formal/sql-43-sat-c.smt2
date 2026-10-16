; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_id () Bool)
(declare-fun all_bound () Bool)
(declare-fun bound_book_id () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x7 (not all_bound)))
 (or $x7 bound_id)))
(assert
 (let (($x7 (not all_bound)))
 (or $x7 bound_book_id)))
(assert
 (let (($x22 (not bound_book_id)))
 (let (($x53 (not bound_id)))
 (or all_bound $x53 $x22))))
(assert
 (or executed))
(assert
 (or bound_id))
(assert
 (or bound_book_id))
(assert
 (or all_bound))
(check-sat)
