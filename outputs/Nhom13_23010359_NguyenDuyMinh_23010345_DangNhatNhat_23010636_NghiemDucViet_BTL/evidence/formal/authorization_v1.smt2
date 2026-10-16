; benchmark generated from python API
(set-info :status unknown)
(declare-fun authenticated () Bool)
(declare-fun grant () Bool)
(declare-fun role_permitted () Bool)
(assert
 (let (($x28 (not grant)))
 (or $x28 authenticated)))
(assert
 (let (($x28 (not grant)))
 (or $x28 role_permitted)))
(assert
 (let (($x15 (not role_permitted)))
 (let (($x26 (not authenticated)))
 (or grant $x26 $x15))))
(assert
 (or grant))
(assert
 (let (($x15 (not role_permitted)))
(let (($x26 (not authenticated)))
(or $x26 $x15))))
(check-sat)
