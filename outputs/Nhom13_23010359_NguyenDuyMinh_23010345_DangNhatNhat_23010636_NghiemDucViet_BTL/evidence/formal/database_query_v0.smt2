; benchmark generated from python API
(set-info :status unknown)
(declare-fun executed () Bool)
(declare-fun bound_parameter () Bool)
(declare-fun untrusted_input () Bool)
(assert
 (or executed))
(assert
 (let (($x27 (not bound_parameter)))
 (or $x27)))
(assert
 (or executed))
(assert
 (or untrusted_input))
(assert
 (let (($x27 (not bound_parameter)))
(or $x27)))
(check-sat)
