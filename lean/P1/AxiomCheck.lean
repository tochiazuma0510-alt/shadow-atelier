/-
P1/AxiomCheck.lean — #print axioms 全量照合(lean_axiom_policy_v1.md v1.6-3)。

sorry-free な主定理について、実際に使われた axiom 集合を機械出力する。
`sorryAx` が一本でも出れば fail-closed(方針違反)。ここでは目視+grep で
確認する(自動 CI 化は次波)。
-/

import P1.Order
import P1.BlockA

#print axioms X_pow_2n
#print axioms X_pow_lt_2n_ne
#print axioms epow_fst
#print axioms epow_snd
#print axioms epow_thd
#print axioms dpow_rot_flag
#print axioms dpow_rot_val
#print axioms dpow_refl_even
#print axioms dpow_refl_odd
#print axioms Gn_X_eq_a1_q1
#print axioms Gn_X_sq
#print axioms Gn_ord_X
