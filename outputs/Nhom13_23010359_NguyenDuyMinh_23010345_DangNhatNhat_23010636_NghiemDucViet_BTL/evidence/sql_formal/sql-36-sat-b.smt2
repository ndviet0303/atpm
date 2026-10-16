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
 (let (($x16 (not bound_lastname)))
 (let (($x14 (not bound_firstname)))
 (let (($x45 (not bound_password)))
 (let (($x36 (not bound_username)))
 (or all_bound $x36 $x45 $x14 $x16))))))
(assert
 (or executed))
(assert
 (let (($x36 (not bound_username)))
 (or $x36)))
(assert
 (let (($x45 (not bound_password)))
 (or $x45)))
(assert
 (let (($x14 (not bound_firstname)))
 (or $x14)))
(assert
 (let (($x16 (not bound_lastname)))
 (or $x16)))
(assert
 (let (($x17 (not all_bound)))
(or $x17)))
(check-sat)
