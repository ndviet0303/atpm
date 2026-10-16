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
 (let (($x27 (not bound_user_id)))
 (let (($x45 (not bound_lastname)))
 (let (($x28 (not bound_firstname)))
 (let (($x42 (not bound_password)))
 (let (($x35 (not bound_username)))
 (or all_bound $x35 $x42 $x28 $x45 $x27)))))))
(assert
 (or executed))
(assert
 (let (($x35 (not bound_username)))
 (or $x35)))
(assert
 (let (($x42 (not bound_password)))
 (or $x42)))
(assert
 (let (($x28 (not bound_firstname)))
 (or $x28)))
(assert
 (let (($x45 (not bound_lastname)))
 (or $x45)))
(assert
 (let (($x27 (not bound_user_id)))
 (or $x27)))
(assert
 (let (($x30 (not all_bound)))
(or $x30)))
(check-sat)
