; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_username () Bool)
(declare-fun all_bound () Bool)
(declare-fun bound_password () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x18 (not all_bound)))
 (or $x18 bound_username)))
(assert
 (let (($x18 (not all_bound)))
 (or $x18 bound_password)))
(assert
 (let (($x36 (not bound_password)))
 (let (($x14 (not bound_username)))
 (or all_bound $x14 $x36))))
(assert
 (or executed))
(assert
 (let (($x14 (not bound_username)))
 (or $x14)))
(assert
 (let (($x36 (not bound_password)))
 (or $x36)))
(assert
 (let (($x18 (not all_bound)))
(or $x18)))
(check-sat)
