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
 (let (($x27 (not bound_id)))
 (let (($x7 (not bound_status)))
 (let (($x36 (not bound_year_level)))
 (let (($x23 (not bound_type)))
 (let (($x31 (not bound_contact)))
 (let (($x38 (not bound_address)))
 (let (($x8 (not bound_gender)))
 (let (($x34 (not bound_lastname)))
 (let (($x33 (not bound_firstname)))
 (or all_bound $x33 $x34 $x8 $x38 $x31 $x23 $x36 $x7 $x27)))))))))))
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
 (or bound_status))
(assert
 (or bound_id))
(assert
 (or all_bound))
(check-sat)
