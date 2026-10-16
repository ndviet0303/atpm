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
 (let (($x16 (not all_bound)))
 (or $x16 bound_firstname)))
(assert
 (let (($x16 (not all_bound)))
 (or $x16 bound_lastname)))
(assert
 (let (($x16 (not all_bound)))
 (or $x16 bound_gender)))
(assert
 (let (($x16 (not all_bound)))
 (or $x16 bound_address)))
(assert
 (let (($x16 (not all_bound)))
 (or $x16 bound_contact)))
(assert
 (let (($x16 (not all_bound)))
 (or $x16 bound_type)))
(assert
 (let (($x16 (not all_bound)))
 (or $x16 bound_year_level)))
(assert
 (let (($x9 (not bound_year_level)))
 (let (($x41 (not bound_type)))
 (let (($x33 (not bound_contact)))
 (let (($x28 (not bound_address)))
 (let (($x24 (not bound_gender)))
 (let (($x38 (not bound_lastname)))
 (let (($x53 (not bound_firstname)))
 (or all_bound $x53 $x38 $x24 $x28 $x33 $x41 $x9)))))))))
(assert
 (or executed))
(assert
 (let (($x53 (not bound_firstname)))
 (or $x53)))
(assert
 (let (($x38 (not bound_lastname)))
 (or $x38)))
(assert
 (let (($x24 (not bound_gender)))
 (or $x24)))
(assert
 (let (($x28 (not bound_address)))
 (or $x28)))
(assert
 (let (($x33 (not bound_contact)))
 (or $x33)))
(assert
 (let (($x41 (not bound_type)))
 (or $x41)))
(assert
 (let (($x9 (not bound_year_level)))
 (or $x9)))
(assert
 (let (($x16 (not all_bound)))
(or $x16)))
(check-sat)
