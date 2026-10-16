; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_username () Bool)
(declare-fun all_bound () Bool)
(declare-fun bound_password () Bool)
(declare-fun bound_firstname () Bool)
(declare-fun bound_lastname () Bool)
(declare-fun bound_user_id () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x30 (not all_bound)))
 (or $x30 bound_username)))
(assert
 (let (($x30 (not all_bound)))
 (or $x30 bound_password)))
(assert
 (let (($x30 (not all_bound)))
 (or $x30 bound_firstname)))
(assert
 (let (($x30 (not all_bound)))
 (or $x30 bound_lastname)))
(assert
 (let (($x30 (not all_bound)))
 (or $x30 bound_user_id)))
(assert
 (let (($x35 (not bound_user_id)))
 (let (($x40 (not bound_lastname)))
 (let (($x42 (not bound_firstname)))
 (let (($x25 (not bound_password)))
 (let (($x28 (not bound_username)))
 (or all_bound $x28 $x25 $x42 $x40 $x35)))))))
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
 (or bound_user_id))
(assert
 (let (($x30 (not all_bound)))
(or $x30)))
(check-sat)
