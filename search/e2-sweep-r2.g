# search/e2-sweep-r2.g -- workorder5 continuation: item1 (synthetic negative smoke test) +
# item3 (sweep (1) r2, linear stage only -- see report to commander for the precise scope note
# on the quadratic/obstruction stage).
#
# Design source (spec projection only): docs/week4-掃引宇宙_v3.md + search/manifest_spec_e2_actions.md.
# Reuses the SAME truncated-polynomial model machinery as search/e19.g (SetClass/ThetaP/SigmaP/EmP),
# because manifest_spec_e2_actions.md's own dictionary states Abar's basis (10-dim: w,p,q,r1,r2,r3,
# t1,t2,t3,t4) is IN BIJECTION with metab.mjs's c=5 monomial basis -- i.e. bar_theta = ThetaP,
# bar_sigma(.,m) = SigmaP(.,m), bar_E_m = EmP(m) at class c=5 exactly (same functions, no new
# derivation needed for the LINEAR stage). The C-level action (sigma|_C, theta|_C, N_C) is NEW data
# from manifest_spec_e2_actions.md, verified below (S-3 stop condition: N_C=0 must reproduce).

SizeScreen([4096, 0]);;
Read("search/e19.g");;
