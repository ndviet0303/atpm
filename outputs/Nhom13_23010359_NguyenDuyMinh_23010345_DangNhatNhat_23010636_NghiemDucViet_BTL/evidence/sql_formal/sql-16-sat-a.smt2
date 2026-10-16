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
 (or all_bound (not bound_selector_item) (not bound_borrow_id)))
(assert
 (or executed))
(assert
 (or bound_selector_item))
(assert
 (or bound_borrow_id))
(assert
 (let (($x36 (not all_bound)))
(or $x36)))
(check-sat)
