; benchmark generated from python API
(set-info :status unknown)
(declare-fun authenticated () Bool)
(declare-fun grant () Bool)
(declare-fun role_permitted () Bool)
(assert
 (let (($x26 (not grant)))
 (or $x26 authenticated)))
(assert
 (let (($x26 (not grant)))
 (or $x26 role_permitted)))
(assert
 (or grant (not authenticated) (not role_permitted)))
(assert
 (or grant))
(assert
 (or authenticated))
(assert
 (or role_permitted))
(check-sat)
