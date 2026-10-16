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
 (let (($x14 (not bound_password)))
 (let (($x34 (not bound_username)))
 (or all_bound $x34 $x14))))
(assert
 (or executed))
(assert
 (or bound_username))
(assert
 (or bound_password))
(assert
 (let (($x25 (not all_bound)))
(or $x25)))
(check-sat)
