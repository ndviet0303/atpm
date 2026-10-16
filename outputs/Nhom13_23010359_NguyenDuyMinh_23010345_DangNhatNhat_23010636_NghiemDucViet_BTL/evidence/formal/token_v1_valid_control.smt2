; benchmark generated from python API
(set-info :status unknown)
(declare-fun iat () Int)
(declare-fun exp () Int)
(declare-fun now () Int)
(declare-fun uid () Int)
(declare-fun audience_ok () Bool)
(declare-fun tag_ok () Bool)
(declare-fun tag_bytes () Int)
(declare-fun nonce_bytes () Int)
(declare-fun key_bytes () Int)
(declare-fun parsed () Bool)
(declare-fun accepted () Bool)
(assert
 (let (($x8 (>= iat 0)))
 (let (($x37 (= tag_bytes 16)))
 (let (($x23 (= nonce_bytes 12)))
 (let (($x28 (= key_bytes 32)))
 (let (($x25 (and parsed $x28 $x23 $x37 tag_ok audience_ok (> uid 0) $x8 (<= iat now) (> exp now) (<= (- exp iat) 1800))))
 (= accepted $x25)))))))
(assert
 accepted)
(assert
 (let (($x63 (= exp 2800)))
 (let (($x61 (= now 1100)))
 (let (($x59 (= iat 1000)))
 (let (($x57 (= uid 1)))
 (let (($x37 (= tag_bytes 16)))
 (let (($x23 (= nonce_bytes 12)))
 (let (($x28 (= key_bytes 32)))
 (and $x28 $x23 $x37 tag_ok audience_ok parsed $x57 $x59 $x61 $x63)))))))))
(assert
 (>= now 0))
(assert
 (>= key_bytes 0))
(assert
 (>= nonce_bytes 0))
(assert
 (>= tag_bytes 0))
(check-sat)
