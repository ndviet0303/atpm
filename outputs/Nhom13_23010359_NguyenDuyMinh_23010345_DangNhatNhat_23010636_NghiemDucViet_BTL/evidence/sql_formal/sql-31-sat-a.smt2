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
 (or all_bound (not bound_username) (not bound_password)))
(assert
 (or executed))
(assert
 (or bound_username))
(assert
 (or bound_password))
(assert
 (let (($x18 (not all_bound)))
(or $x18)))
(check-sat)
