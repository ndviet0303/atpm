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
(declare-fun bound_status () Bool)
(declare-fun bound_id () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x49 (not all_bound)))
 (or $x49 bound_firstname)))
(assert
 (let (($x49 (not all_bound)))
 (or $x49 bound_lastname)))
(assert
 (let (($x49 (not all_bound)))
 (or $x49 bound_gender)))
(assert
 (let (($x49 (not all_bound)))
 (or $x49 bound_address)))
(assert
 (let (($x49 (not all_bound)))
 (or $x49 bound_contact)))
(assert
 (let (($x49 (not all_bound)))
 (or $x49 bound_type)))
(assert
 (let (($x49 (not all_bound)))
 (or $x49 bound_year_level)))
(assert
 (let (($x49 (not all_bound)))
 (or $x49 bound_status)))
(assert
 (let (($x49 (not all_bound)))
 (or $x49 bound_id)))
(assert
 (let (($x10 (not bound_id)))
 (let (($x22 (not bound_status)))
 (let (($x14 (not bound_year_level)))
 (let (($x53 (not bound_type)))
 (let (($x8 (not bound_contact)))
 (let (($x31 (not bound_address)))
 (let (($x36 (not bound_gender)))
 (let (($x27 (not bound_lastname)))
 (let (($x47 (not bound_firstname)))
 (or all_bound $x47 $x27 $x36 $x31 $x8 $x53 $x14 $x22 $x10)))))))))))
(assert
 (or executed))
(assert
 (let (($x47 (not bound_firstname)))
 (or $x47)))
(assert
 (let (($x27 (not bound_lastname)))
 (or $x27)))
(assert
 (let (($x36 (not bound_gender)))
 (or $x36)))
(assert
 (let (($x31 (not bound_address)))
 (or $x31)))
(assert
 (let (($x8 (not bound_contact)))
 (or $x8)))
(assert
 (let (($x53 (not bound_type)))
 (or $x53)))
(assert
 (let (($x14 (not bound_year_level)))
 (or $x14)))
(assert
 (let (($x22 (not bound_status)))
 (or $x22)))
(assert
 (let (($x10 (not bound_id)))
 (or $x10)))
(assert
 (let (($x49 (not all_bound)))
(or $x49)))
(check-sat)
