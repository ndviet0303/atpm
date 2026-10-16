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
 (let (($x62 (not bound_id)))
 (let (($x57 (not bound_year_level)))
 (let (($x47 (not bound_type)))
 (let (($x49 (not bound_contact)))
 (let (($x33 (not bound_address)))
 (let (($x9 (not bound_gender)))
 (let (($x36 (not bound_lastname)))
 (let (($x23 (not bound_firstname)))
 (or all_bound $x23 $x36 $x9 $x33 $x49 $x47 $x57 $x62))))))))))
(assert
 (or executed))
(assert
 (or bound_firstname))
(assert
 (or bound_lastname))
(assert
 (or bound_gender))
(assert
 (or bound_address))
(assert
 (or bound_contact))
(assert
 (or bound_type))
(assert
 (or bound_year_level))
(assert
 (or bound_id))
(assert
 (or all_bound))
(check-sat)
