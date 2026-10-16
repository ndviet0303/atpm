; benchmark generated from python API
(set-info :status unknown)
(declare-fun emitted () Bool)
(declare-fun context_encoded () Bool)
(declare-fun untrusted_text () Bool)
(assert
 (or emitted))
(assert
 (or context_encoded))
(assert
 (or emitted))
(assert
 (or untrusted_text))
(assert
 (let (($x11 (not context_encoded)))
(or $x11)))
(check-sat)
