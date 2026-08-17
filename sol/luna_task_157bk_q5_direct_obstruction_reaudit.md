# Luna task 157bk — q5 direct profinite-obstruction re-audit

You are Luna, acting as an adversarial mathematical auditor.  Do not run local
GAP, git, push, GHA, or edit implementation.  Write only
`sol/luna_reply_157bk_q5_direct_obstruction_reaudit.md`.

## Objective

Re-audit the negative verdict in reply 157bi against the following proposed
direct argument.  Do not require an isolated PB4 source object unless the
definition of the image of `widehat GT -> GT^heart(M)` genuinely requires it.
The question is whether a finite quotient can directly obstruct an exact
profinite pentagon lift.

Let `F=F2=<x,y>`.  Let `r:F -> R=PB3/M` be the exact frozen roof map and let
`b_j:F -> GL_4(F_q)` be the five homomorphisms obtained by literal A.18
cofaces followed by the exact Burau specialization.  Put

    Psi=(r,b_1,...,b_5): F -> R x GL_4(F_q)^5,
    H=im(Psi), H'=[H,H], pi:H'->R'.

Because `F -> H` is onto, `Psi(F')=H'`.  Thus for each target
`fbar in R'`, the exact finite image of *all* commutator representatives
`f in F'` lifting `fbar` is the complete coset `h0*K_H`, where
`K_H=ker(pi)`.  The same remains true for continuous maps from the profinite
completion because the codomain is finite.

If `(lambda,fhat) in widehat GT` projects to a frozen roof row, then
`fhat in widehat F'`, its image lies in `h0*K_H`, and its exact pentagon in
`widehat PB4` forces the five-block specialized Burau defect to be identity.
Therefore, if the complete finite coset has identity-defect count zero, that
row cannot lie in the image of `widehat GT`, regardless of whether the tuple
kernel is itself packaged as an isolated PB4 object.  The two hexagons need
not be rechecked for every element of the superset fiber: any hypothetical
global lift already satisfies them, while scanning a superset cannot create
a false exclusion.

## Required decisions

1. Prove or find the first exact failure in this argument.  In particular
   audit `Psi(F')=H'`, profinite density/finite-image passage, the right-coset
   fiber, literal A.18 defect orientation, and whether all five blocks really
   are homomorphisms from the same F2.
2. Decide whether a single PB4 quotient/kernel or the raw-158 presentation is
   logically necessary for this *one-direction obstruction*.  Distinguish
   necessity from a convenient GT-shadow survival certificate.
3. Revisit the index-3 promotion using the already accepted theorem-level
   premises `X=GT^heart(M)` of order 972, arithmetic image A of order 324,
   `A <= I=im(widehat GT -> X) <= X`, and I a subgroup.  Explain whether an
   explicit 324-row list or advance outside label is needed.  Compare
   `sol/sol_reply_152_pushback.md` section 13.3.
4. Inspect the actual v4 producer/checker to ensure the finite fiber is
   exactly the one above and not a different normal closure, and list only
   genuinely missing data.  If a zero q5 receipt plus checker PASS is enough,
   state the exact terminal seal contract.  If not, give a concrete
   counterexample/model to the proposed implication, not merely missing
   metadata.

End with exactly one token:

- `Q5_DIRECT_OBSTRUCTION_TERMINAL_A_IF_ZERO`
- `Q5_DIRECT_OBSTRUCTION_NEEDS_<short_reason>`
- `Q5_DIRECT_OBSTRUCTION_REFUTED_<short_reason>`
