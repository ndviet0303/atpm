; benchmark generated from python API
(set-info :status unknown)
(declare-fun grant () Bool)
(declare-fun role_permitted () Bool)
(declare-fun authenticated () Bool)
(assert
 (or grant))
(assert
 (or grant))
(assert
 (or (not authenticated) (not role_permitted)))
(check-sat)
