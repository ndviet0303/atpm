; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_selector_item () Bool)
(declare-fun all_bound () Bool)
(declare-fun bound_borrow_id () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x36 (not all_bound)))
 (or $x36 bound_selector_item)))
(assert
 (let (($x36 (not all_bound)))
 (or $x36 bound_borrow_id)))
(assert
 (let (($x27 (not bound_borrow_id)))
 (let (($x34 (not bound_selector_item)))
 (or all_bound $x34 $x27))))
(assert
 (or executed))
(assert
 (or bound_selector_item))
(assert
 (or bound_borrow_id))
(assert
 (or all_bound))
(check-sat)
