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
(declare-fun bound_id () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x32 (not all_bound)))
 (or $x32 bound_firstname)))
(assert
 (let (($x32 (not all_bound)))
 (or $x32 bound_lastname)))
(assert
 (let (($x32 (not all_bound)))
 (or $x32 bound_gender)))
(assert
 (let (($x32 (not all_bound)))
 (or $x32 bound_address)))
(assert
 (let (($x32 (not all_bound)))
 (or $x32 bound_contact)))
(assert
 (let (($x32 (not all_bound)))
 (or $x32 bound_type)))
(assert
 (let (($x32 (not all_bound)))
 (or $x32 bound_year_level)))
(assert
 (let (($x32 (not all_bound)))
 (or $x32 bound_id)))
(assert
 (let (($x31 (not bound_id)))
 (let (($x38 (not bound_year_level)))
 (let (($x8 (not bound_type)))
 (let (($x34 (not bound_contact)))
 (let (($x33 (not bound_address)))
 (let (($x47 (not bound_gender)))
 (let (($x62 (not bound_lastname)))
 (let (($x12 (not bound_firstname)))
 (or all_bound $x12 $x62 $x47 $x33 $x34 $x8 $x38 $x31))))))))))
(assert
 (or executed))
(assert
 (let (($x12 (not bound_firstname)))
 (or $x12)))
(assert
 (let (($x62 (not bound_lastname)))
 (or $x62)))
(assert
 (let (($x47 (not bound_gender)))
 (or $x47)))
(assert
 (let (($x33 (not bound_address)))
 (or $x33)))
(assert
 (let (($x34 (not bound_contact)))
 (or $x34)))
(assert
 (let (($x8 (not bound_type)))
 (or $x8)))
(assert
 (let (($x38 (not bound_year_level)))
 (or $x38)))
(assert
 (let (($x31 (not bound_id)))
 (or $x31)))
(assert
 (let (($x32 (not all_bound)))
(or $x32)))
(check-sat)
