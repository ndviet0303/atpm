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
 (let (($x53 (not bound_year_level)))
 (let (($x17 (not bound_type)))
 (let (($x38 (not bound_contact)))
 (let (($x43 (not bound_address)))
 (let (($x24 (not bound_gender)))
 (let (($x56 (not bound_lastname)))
 (let (($x28 (not bound_firstname)))
 (or all_bound $x28 $x56 $x24 $x43 $x38 $x17 $x53)))))))))
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
 (let (($x16 (not all_bound)))
(or $x16)))
(check-sat)
