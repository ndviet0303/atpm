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
 (let (($x45 (not bound_lastname)))
 (let (($x28 (not bound_firstname)))
 (let (($x42 (not bound_password)))
 (let (($x35 (not bound_username)))
 (or all_bound $x35 $x42 $x28 $x45))))))
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
 (or all_bound))
(check-sat)
