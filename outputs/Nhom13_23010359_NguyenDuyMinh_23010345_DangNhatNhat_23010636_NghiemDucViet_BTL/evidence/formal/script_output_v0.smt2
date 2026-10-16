; benchmark generated from python API
(set-info :status unknown)
(declare-fun emitted () Bool)
(declare-fun context_encoded () Bool)
(declare-fun untrusted_text () Bool)
(assert
 (or emitted))
(assert
 (let (($x36 (not context_encoded)))
 (or $x36)))
(assert
 (or emitted))
(assert
 (or untrusted_text))
(assert
 (let (($x36 (not context_encoded)))
(or $x36)))
(check-sat)
