# Luna task 156c — GAP-native low-degree/product alternative

Independently find a GAP 4.16.0 exact route for the GF(5) map
`E:F2 -> P x GL(4,5)^5` that avoids the 3161-point disjoint vector action.

Write only `sol/luna_reply_156c_burau_gap_structure.md`.  Do not edit code,
run local GAP, commit, push, or dispatch.

Investigate with exact GAP APIs/documentation:

- matrix-group images for each A.18 block and block-diagonal 20x20 matrices;
- smaller faithful/projective actions while preserving scalar kernels;
- `Goursat`/subdirect-product, fp-presentation, Reidemeister-Schreier, or
  `IsomorphismFpGroupByGenerators` methods on the 36-point roof image;
- computing the derived subgroup kernel using relator evaluations and normal
  closure inside the matrix tuple group;
- exact section/preimage words for all 367,416 projected derived elements.

Give concrete GAP function names and pseudocode, and prove why the proposed
kernel is complete.  Separate APIs confirmed from local installed docs/source
from guesses.  Rank alternatives by likely memory on standard GHA.  A mere
higher `-o` value is not an acceptable primary solution.
