; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_firstname () Bool)
(declare-fun all_bound () Bool)
(declare-fun bound_lastname () Bool)
(declare-fun bound_gender () Bool)
(declare-fun bound_address () Bool)
(declare-fun bound_contact () Bool)
(declare-fun bound_type () Bool)
(declare-fun bound_year_level () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x33 (not all_bound)))
 (or $x33 bound_firstname)))
(assert
 (let (($x33 (not all_bound)))
 (or $x33 bound_lastname)))
(assert
 (let (($x33 (not all_bound)))
 (or $x33 bound_gender)))
(assert
 (let (($x33 (not all_bound)))
 (or $x33 bound_address)))
(assert
 (let (($x33 (not all_bound)))
 (or $x33 bound_contact)))
(assert
 (let (($x33 (not all_bound)))
 (or $x33 bound_type)))
(assert
 (let (($x33 (not all_bound)))
 (or $x33 bound_year_level)))
(assert
 (let (($x40 (not bound_year_level)))
 (let (($x45 (not bound_type)))
 (let (($x42 (not bound_contact)))
 (let (($x34 (not bound_address)))
 (let (($x31 (not bound_gender)))
 (let (($x39 (not bound_lastname)))
 (let (($x28 (not bound_firstname)))
 (or all_bound $x28 $x39 $x31 $x34 $x42 $x45 $x40)))))))))
(assert
 (or executed))
(assert
 (let (($x28 (not bound_firstname)))
 (or $x28)))
(assert
 (let (($x39 (not bound_lastname)))
 (or $x39)))
(assert
 (let (($x31 (not bound_gender)))
 (or $x31)))
(assert
 (let (($x34 (not bound_address)))
 (or $x34)))
(assert
 (let (($x42 (not bound_contact)))
 (or $x42)))
(assert
 (let (($x45 (not bound_type)))
 (or $x45)))
(assert
 (let (($x40 (not bound_year_level)))
 (or $x40)))
(assert
 (let (($x33 (not all_bound)))
(or $x33)))
(check-sat)
