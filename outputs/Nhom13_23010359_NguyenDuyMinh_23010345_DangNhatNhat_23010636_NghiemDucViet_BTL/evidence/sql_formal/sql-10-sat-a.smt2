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
(declare-fun executed () Bool)
(assert
 (let (($x12 (not all_bound)))
 (or $x12 bound_book_title)))
(assert
 (let (($x12 (not all_bound)))
 (or $x12 bound_category_id)))
(assert
 (let (($x12 (not all_bound)))
 (or $x12 bound_author)))
(assert
 (let (($x12 (not all_bound)))
 (or $x12 bound_book_copies)))
(assert
 (let (($x12 (not all_bound)))
 (or $x12 bound_book_pub)))
(assert
 (let (($x12 (not all_bound)))
 (or $x12 bound_publisher_name)))
(assert
 (let (($x12 (not all_bound)))
 (or $x12 bound_isbn)))
(assert
 (let (($x12 (not all_bound)))
 (or $x12 bound_copyright_year)))
(assert
 (let (($x12 (not all_bound)))
 (or $x12 bound_status)))
(assert
 (let (($x28 (not bound_status)))
 (let (($x38 (not bound_copyright_year)))
 (let (($x27 (not bound_isbn)))
 (let (($x39 (not bound_publisher_name)))
 (let (($x25 (not bound_book_pub)))
 (let (($x40 (not bound_book_copies)))
 (let (($x16 (not bound_author)))
 (let (($x41 (not bound_category_id)))
 (let (($x35 (not bound_book_title)))
 (or all_bound $x35 $x41 $x16 $x40 $x25 $x39 $x27 $x38 $x28)))))))))))
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
 (let (($x12 (not all_bound)))
(or $x12)))
(check-sat)
