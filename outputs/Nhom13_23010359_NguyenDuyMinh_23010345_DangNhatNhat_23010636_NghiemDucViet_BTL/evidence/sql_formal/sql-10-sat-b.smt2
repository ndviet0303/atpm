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
 (let (($x13 (not bound_status)))
 (let (($x36 (not bound_copyright_year)))
 (let (($x8 (not bound_isbn)))
 (let (($x26 (not bound_publisher_name)))
 (let (($x35 (not bound_book_pub)))
 (let (($x16 (not bound_book_copies)))
 (let (($x25 (not bound_author)))
 (let (($x27 (not bound_category_id)))
 (let (($x28 (not bound_book_title)))
 (or all_bound $x28 $x27 $x25 $x16 $x35 $x26 $x8 $x36 $x13)))))))))))
(assert
 (or executed))
(assert
 (let (($x28 (not bound_book_title)))
 (or $x28)))
(assert
 (let (($x27 (not bound_category_id)))
 (or $x27)))
(assert
 (let (($x25 (not bound_author)))
 (or $x25)))
(assert
 (let (($x16 (not bound_book_copies)))
 (or $x16)))
(assert
 (let (($x35 (not bound_book_pub)))
 (or $x35)))
(assert
 (let (($x26 (not bound_publisher_name)))
 (or $x26)))
(assert
 (let (($x8 (not bound_isbn)))
 (or $x8)))
(assert
 (let (($x36 (not bound_copyright_year)))
 (or $x36)))
(assert
 (let (($x13 (not bound_status)))
 (or $x13)))
(assert
 (let (($x12 (not all_bound)))
(or $x12)))
(check-sat)
