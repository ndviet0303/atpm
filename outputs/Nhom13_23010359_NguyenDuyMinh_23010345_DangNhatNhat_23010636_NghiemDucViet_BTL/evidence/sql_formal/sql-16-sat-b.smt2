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
 (let (($x28 (not bound_borrow_id)))
 (let (($x42 (not bound_selector_item)))
 (or all_bound $x42 $x28))))
(assert
 (or executed))
(assert
 (let (($x42 (not bound_selector_item)))
 (or $x42)))
(assert
 (let (($x28 (not bound_borrow_id)))
 (or $x28)))
(assert
 (let (($x36 (not all_bound)))
(or $x36)))
(check-sat)
