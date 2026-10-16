; benchmark generated from python API
(set-info :status unknown)
(declare-fun executed () Bool)
(declare-fun bound_parameter () Bool)
(declare-fun untrusted_input () Bool)
(assert
 (or executed))
(assert
 (or bound_parameter))
(assert
 (or executed))
(assert
 (or untrusted_input))
(assert
 (let (($x29 (not bound_parameter)))
(or $x29)))
(check-sat)
