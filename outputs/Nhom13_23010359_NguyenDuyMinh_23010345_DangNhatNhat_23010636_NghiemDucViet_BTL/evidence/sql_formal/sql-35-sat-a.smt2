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
 (let (($x28 (not bound_year_level)))
 (let (($x15 (not bound_type)))
 (let (($x39 (not bound_contact)))
 (let (($x29 (not bound_address)))
 (let (($x31 (not bound_gender)))
 (let (($x46 (not bound_lastname)))
 (let (($x34 (not bound_firstname)))
 (or all_bound $x34 $x46 $x31 $x29 $x39 $x15 $x28)))))))))
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
 (let (($x33 (not all_bound)))
(or $x33)))
(check-sat)
