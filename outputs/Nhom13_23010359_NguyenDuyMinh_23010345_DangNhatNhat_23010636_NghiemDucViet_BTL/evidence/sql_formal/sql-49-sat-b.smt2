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
 (let (($x15 (not bound_id)))
 (let (($x30 (not bound_status)))
 (let (($x35 (not bound_copyright_year)))
 (let (($x36 (not bound_isbn)))
 (let (($x14 (not bound_publisher_name)))
 (let (($x7 (not bound_book_pub)))
 (let (($x38 (not bound_book_copies)))
 (let (($x42 (not bound_author)))
 (let (($x63 (not bound_category_id)))
 (let (($x33 (not bound_book_title)))
 (or all_bound $x33 $x63 $x42 $x38 $x7 $x14 $x36 $x35 $x30 $x15))))))))))))
(assert
 (or executed))
(assert
 (let (($x33 (not bound_book_title)))
 (or $x33)))
(assert
 (let (($x63 (not bound_category_id)))
 (or $x63)))
(assert
 (let (($x42 (not bound_author)))
 (or $x42)))
(assert
 (let (($x38 (not bound_book_copies)))
 (or $x38)))
(assert
 (let (($x7 (not bound_book_pub)))
 (or $x7)))
(assert
 (let (($x14 (not bound_publisher_name)))
 (or $x14)))
(assert
 (let (($x36 (not bound_isbn)))
 (or $x36)))
(assert
 (let (($x35 (not bound_copyright_year)))
 (or $x35)))
(assert
 (let (($x30 (not bound_status)))
 (or $x30)))
(assert
 (let (($x15 (not bound_id)))
 (or $x15)))
(assert
 (let (($x13 (not all_bound)))
(or $x13)))
(check-sat)
