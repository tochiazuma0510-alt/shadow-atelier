# Luna task 153c — independent Python cross-check of the Burau finite fiber

Read `sol/luna_task_153_b5_burau_fiber.md` and
`sol/luna_reply_153b_burau_soundness.md` completely.  Own only
`search/check_d972_b4_burau_fiber_v1.py` and report to
`sol/luna_reply_153c_burau_crosscheck.md`; do not edit the GAP producer,
workflow files, or another reply.

Build a helper-independent checker.  In Python, reconstruct the compact D972
roof generators by porting the frozen `MakeDn`/`MakeGn(9)` and GF(8)/PSL
formulae, then replay all 972 signed representative words against their exact
stored target keys.  Reconstruct the finite Burau matrices over GF(3) and
GF(4), the six pure Artin generators, the five literal A.18 pairs, and the raw
defect using the frozen opposite-product convention.

Use SymPy 1.14's permutation-group implementation to reconstruct
`H=<Hx,Hy>`, `H'`, and the kernel of the faithful 36-point roof projection
(successive point stabilizers).  Independently check all group orders and
enumerate every relevant exact kernel coset, replaying every defect and
matching the producer counts/digests.  Reject any incomplete, empty, or
unreplayable terminal record.

Negative mutation tests must actually fail for reversed `PaperProd`, reversed
`x13`, swapped leading factors, deletion of a kernel element, and corruption
of a roof word/key.  Tautological tests are forbidden.  An all-pass finite
specialization remains `UNKNOWN`.

Do not run heavy GAP, commit, push, or dispatch GHA.  Lightweight Python
selftests are allowed.
