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
 (let (($x27 (not bound_book_id)))
 (let (($x18 (not bound_id)))
 (or all_bound $x18 $x27))))
(assert
 (or executed))
(assert
 (let (($x18 (not bound_id)))
 (or $x18)))
(assert
 (let (($x27 (not bound_book_id)))
 (or $x27)))
(assert
 (let (($x7 (not all_bound)))
(or $x7)))
(check-sat)
