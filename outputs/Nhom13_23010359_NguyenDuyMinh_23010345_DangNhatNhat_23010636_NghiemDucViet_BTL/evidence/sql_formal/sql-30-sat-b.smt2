; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_username () Bool)
(declare-fun all_bound () Bool)
(declare-fun bound_password () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x25 (not all_bound)))
 (or $x25 bound_username)))
(assert
 (let (($x25 (not all_bound)))
 (or $x25 bound_password)))
(assert
 (let (($x39 (not bound_password)))
 (let (($x14 (not bound_username)))
 (or all_bound $x14 $x39))))
(assert
 (or executed))
(assert
 (let (($x14 (not bound_username)))
 (or $x14)))
(assert
 (let (($x39 (not bound_password)))
 (or $x39)))
(assert
 (let (($x25 (not all_bound)))
(or $x25)))
(check-sat)
