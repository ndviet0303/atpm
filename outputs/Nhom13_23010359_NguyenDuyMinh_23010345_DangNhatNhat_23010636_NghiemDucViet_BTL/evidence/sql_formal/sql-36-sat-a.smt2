; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_username () Bool)
(declare-fun all_bound () Bool)
(declare-fun bound_password () Bool)
(declare-fun bound_firstname () Bool)
(declare-fun bound_lastname () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x17 (not all_bound)))
 (or $x17 bound_username)))
(assert
 (let (($x17 (not all_bound)))
 (or $x17 bound_password)))
(assert
 (let (($x17 (not all_bound)))
 (or $x17 bound_firstname)))
(assert
 (let (($x17 (not all_bound)))
 (or $x17 bound_lastname)))
(assert
 (let (($x36 (not bound_lastname)))
 (let (($x27 (not bound_firstname)))
 (let (($x45 (not bound_password)))
 (let (($x28 (not bound_username)))
 (or all_bound $x28 $x45 $x27 $x36))))))
(assert
 (or executed))
(assert
 (or bound_username))
(assert
 (or bound_password))
(assert
 (or bound_firstname))
(assert
 (or bound_lastname))
(assert
 (let (($x17 (not all_bound)))
(or $x17)))
(check-sat)
