; benchmark generated from python API
(set-info :status unknown)
(declare-fun bound_book_title () Bool)
(declare-fun all_bound () Bool)
(declare-fun bound_category_id () Bool)
(declare-fun bound_author () Bool)
(declare-fun bound_book_copies () Bool)
(declare-fun bound_book_pub () Bool)
(declare-fun bound_publisher_name () Bool)
(declare-fun bound_isbn () Bool)
(declare-fun bound_copyright_year () Bool)
(declare-fun bound_status () Bool)
(declare-fun bound_id () Bool)
(declare-fun executed () Bool)
(assert
 (let (($x13 (not all_bound)))
 (or $x13 bound_book_title)))
(assert
 (let (($x13 (not all_bound)))
 (or $x13 bound_category_id)))
(assert
 (let (($x13 (not all_bound)))
 (or $x13 bound_author)))
(assert
 (let (($x13 (not all_bound)))
 (or $x13 bound_book_copies)))
(assert
 (let (($x13 (not all_bound)))
 (or $x13 bound_book_pub)))
(assert
 (let (($x13 (not all_bound)))
 (or $x13 bound_publisher_name)))
(assert
 (let (($x13 (not all_bound)))
 (or $x13 bound_isbn)))
(assert
 (let (($x13 (not all_bound)))
 (or $x13 bound_copyright_year)))
(assert
 (let (($x13 (not all_bound)))
 (or $x13 bound_status)))
(assert
 (let (($x13 (not all_bound)))
 (or $x13 bound_id)))
(assert
 (let (($x33 (not bound_id)))
 (let (($x32 (not bound_status)))
 (let (($x63 (not bound_copyright_year)))
 (let (($x29 (not bound_isbn)))
 (let (($x42 (not bound_publisher_name)))
 (let (($x12 (not bound_book_pub)))
 (let (($x38 (not bound_book_copies)))
 (let (($x23 (not bound_author)))
 (let (($x7 (not bound_category_id)))
 (let (($x57 (not bound_book_title)))
 (or all_bound $x57 $x7 $x23 $x38 $x12 $x42 $x29 $x63 $x32 $x33))))))))))))
(assert
 (or executed))
(assert
 (or bound_book_title))
(assert
 (or bound_category_id))
(assert
 (or bound_author))
(assert
 (or bound_book_copies))
(assert
 (or bound_book_pub))
(assert
 (or bound_publisher_name))
(assert
 (or bound_isbn))
(assert
 (or bound_copyright_year))
(assert
 (or bound_status))
(assert
 (or bound_id))
(assert
 (let (($x13 (not all_bound)))
(or $x13)))
(check-sat)
