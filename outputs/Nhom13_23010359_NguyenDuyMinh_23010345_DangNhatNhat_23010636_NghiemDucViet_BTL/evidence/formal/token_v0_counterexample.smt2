; benchmark generated from python API
(set-info :status unknown)
(declare-fun parsed () Bool)
(declare-fun accepted () Bool)
(declare-fun iat () Int)
(declare-fun exp () Int)
(declare-fun now () Int)
(declare-fun uid () Int)
(declare-fun audience_ok () Bool)
(declare-fun tag_ok () Bool)
(declare-fun tag_bytes () Int)
(declare-fun nonce_bytes () Int)
(declare-fun key_bytes () Int)
(assert
 (= accepted parsed))
(assert
 accepted)
(assert
 (let (($x8 (>= iat 0)))
 (let (($x37 (= tag_bytes 16)))
 (let (($x23 (= nonce_bytes 12)))
 (let (($x28 (= key_bytes 32)))
 (let (($x25 (and parsed $x28 $x23 $x37 tag_ok audience_ok (> uid 0) $x8 (<= iat now) (> exp now) (<= (- exp iat) 1800))))
 (let (($x48 (not tag_ok)))
 (let (($x52 (= tag_bytes 0)))
 (let (($x51 (= nonce_bytes 16)))
 (let (($x50 (= key_bytes 16)))
 (and $x50 $x51 $x52 $x48 parsed (not $x25))))))))))))
(assert
 (>= now 0))
(assert
 (>= key_bytes 0))
(assert
 (>= nonce_bytes 0))
(assert
 (>= tag_bytes 0))
(check-sat)
