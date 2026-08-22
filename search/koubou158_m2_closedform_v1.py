"""koubou158_m2_closedform_v1.py

Sigma-free closed-form m-generalized hexagon builder, per mathematician
spec relayed by commander 2026-08-22 (v3 order). No GAP, no
Reidemeister-Schreier -- pure free-group word substitution throughout,
matching FIXED_WORD's own native 2-letter alphabet (letter 1 = "x" =
A12/x12 role, letter 2 = "y" = A23/x23 role -- the SAME convention
hexagon_words()/build_wordexpr_candidate already use, e.g.
search/d972_b345_relfrat3_wordexpr_v8.py hexagon_words(f): x,y=[1],[2]).

Construction (mathematician verbatim):
  1. g := y^m ++ FIXED_WORD  (y prepended on the LEFT -- NOT f.y^m)
  2. tau := letter substitution x->y, y->(xy)^-1=[-y,-x] (free reduction
     only -- NEVER evaluated as a quotient homomorphism; per the
     mathematician's M5 warning, N_F2's tau-invariance is required at
     the FREE GROUP level)
  3. H := tau^2(g) ++ tau(g) ++ g, freely reduced
     (expands to [x^m f(z,x)]*[z^m f(y,z)]*[y^m f(x,y)] -- each f-leaf
     gets the NEXT generator's m-th power prepended; degenerates to the
     frozen m=0 form automatically)
  4. push H through the 5 receipt cofaces (formulas.cofaces_3_4) to PB4
     -> hexagon_1_coface_{0..4}
  5. pentagon row is m-invariant -- reuse the frozen value unchanged

FORBIDDEN: normalizing any leaf via f(v,u)=f(u,v)^-1 (that IS the
hexagon acceptance condition itself -- using it here would be circular).
The frozen row's "Inv(f_xz)" leaf is treated as f(z,x) directly (an
independent substitution, prefixed by x^m), never as inv(f(x,z)).

Remaining ambiguity (mathematician: any m-generalization choice below is
claimed equivalent, since the substitution f -> y^m*f is rotation-
independent) -- resolved by an m=0 SHA canary against the frozen
target6.base_gradient (entry_count=72, sha256=
788fd8712f76a3ca254bb2179b5498fed3ca00e649ba0321ef297d2d985cc71e):
  - tau_direction in {A, B}: A is x->y,y->(xy)^-1 as given; B=tau^-1=tau^2
    is x->(xy)^-1,y->x (the other order-3 generator of the same cyclic
    subgroup)
  - rotation in {0,1,2}: which cyclic ordering of the 3-factor product
    [tau^2(g),tau(g),g] -> [tau(g),g,tau^2(g)] -> [g,tau^2(g),tau(g)]
6 combinations total (superset of the "4-choice" canary mentioned by the
commander -- tested exhaustively rather than guessing which 4 of the 6,
since finding the unique SHA match is what matters).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import koubou158_L3_core_v1_1 as core  # noqa: E402


def word_substitute(word: list[int], images: list[list[int]]) -> list[int]:
    out: list[int] = []
    for letter in word:
        img = images[abs(letter) - 1]
        out.extend(img if letter > 0 else core.inv_word(img))
        out = core.reduce_word(out)
    return out


TAU_IMAGES = {
    "A": [[2], [-2, -1]],   # x->y, y->(xy)^-1
    "B": [[-2, -1], [1]],   # x->(xy)^-1, y->x  (= tau^-1 = tau^2 of A)
}


def apply_tau(word: list[int], direction: str) -> list[int]:
    return word_substitute(word, TAU_IMAGES[direction])


def build_g(m: int) -> list[int]:
    return core.reduce_word([2] * m + core.FIXED_WORD)


def build_H(m: int, direction: str, rotation: int) -> list[int]:
    g = build_g(m)
    tau_g = apply_tau(g, direction)
    tau2_g = apply_tau(tau_g, direction)
    factors = [tau2_g, tau_g, g]  # base order: tau^2(g), tau(g), g
    rotated = factors[rotation:] + factors[:rotation]
    return core.reduce_word(rotated[0] + rotated[1] + rotated[2])


def push_through_coface(word: list[int], coface_slot: list[list[int]]) -> list[int]:
    # coface_slot = cofaces_3_4[slot] = [A12_image, A13_image, A23_image]
    # H's own alphabet is {1=x=A12-role, 2=y=A23-role} only (never uses A13)
    images = [coface_slot[0], coface_slot[2]]
    return word_substitute(word, images)


def all_combos():
    for direction in ("A", "B"):
        for rotation in (0, 1, 2):
            yield direction, rotation
