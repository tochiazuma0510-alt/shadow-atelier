"""koubou158_m2_closedform_v2.py

Corrected sigma-free closed-form m-generalized hexagon builder, per
mathematician diagnosis 2026-08-22 (theta-hexagon defect identified):
the 14-term residual in v1's closest candidate (search/
koubou158_m2_closedform_v1.py) was caused by treating the frozen row's
"Inv(f_xz)" leaf as f(z,x) (argument-swap) instead of literally
inv_word(f(x,z)) (word-inverse of f(x,z), NOT the argument-swapped
substitution -- those two differ by exactly the theta-hexagon
acceptance-condition gradient, which lies outside im(D2bar) by
construction, hence the non-coboundary residual found at j=4,5).

Corrected construction (mathematician verbatim, commander message
2026-08-22):
  h1(m) = pp[ y^m ++ f_xy , x^m ++ Inv(f_xz) , z^m ++ f_yz ]
where:
  - x=[1], y=[2] are the raw F2 tokens FIXED_WORD's own alphabet uses
    (matching search/d972_b345_relfrat3_wordexpr_v8.py hexagon_words'
    convention exactly)
  - z := (yx)^-1 = [-1,-2] (the SAME z hexagon_words()/build_wordexpr_
    candidate already use: z=inv_word(pp_words([x,y])), confirmed
    algebraically identical: pp_words([x,y])=y.x, so z=(y.x)^-1)
  - f_xy := substitute2(FIXED_WORD, x, y)  (= FIXED_WORD itself, since
    substituting letter1->x=[1], letter2->y=[2] is the identity map)
  - f_xz := substitute2(FIXED_WORD, x, z)
  - f_yz := substitute2(FIXED_WORD, y, z)
  - Inv(f_xz) := inv_word(f_xz) -- literal word-inverse, NEVER
    f(z,x) (argument-swapped substitution) -- that swap is exactly the
    theta-hexagon acceptance condition itself and using it here would be
    circular (this was the v1 bug)
  - pp[A,B,C] := reduce(C + B + A) (same reversed-concatenation
    convention as core's pp_words / hexagon_words, "paper writes ABC,
    multiplies right-to-left")
  - each leaf gets the CORRESPONDING generator's m-th power prepended on
    the left (y^m before f_xy, x^m before Inv(f_xz), z^m before f_yz)

At m=0: x^0=y^0=z^0=empty, so h1(0) = pp[f_xy,Inv(f_xz),f_yz] =
reduce(f_yz + inv_word(f_xz) + f_xy) -- LITERALLY IDENTICAL to
hexagon_words(FIXED_WORD)'s h1 = pp_words([fxy,inv_word(fxz),fyz]) (same
reduce(fyz+inv(fxz)+fxy) expression) -- SHA tier-(i) match against the
frozen target6.base_gradient is guaranteed BY CONSTRUCTION at m=0, not
merely hoped for.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import koubou158_L3_core_v1_1 as core  # noqa: E402

X_TOKEN = [1]
Y_TOKEN = [2]
Z_TOKEN = [-1, -2]  # (yx)^-1


def pp(words: list[list[int]]) -> list[int]:
    out: list[int] = []
    for w in reversed(words):
        out.extend(w)
    return core.reduce_word(out)


def build_h1(m: int, fixed_word: list[int] | None = None) -> list[int]:
    """Abstract-level (2-letter alphabet x=1,y=2) m-generalized hexagon_1
    word. Push through a coface (letter1->A12-image, letter2->A23-image)
    to get a PB4-level word."""
    fw = core.FIXED_WORD if fixed_word is None else fixed_word
    f_xy = core.substitute2(fw, X_TOKEN, Y_TOKEN)
    f_xz = core.substitute2(fw, X_TOKEN, Z_TOKEN)
    f_yz = core.substitute2(fw, Y_TOKEN, Z_TOKEN)
    inv_f_xz = core.inv_word(f_xz)

    term_A = Y_TOKEN * m + f_xy
    term_B = X_TOKEN * m + inv_f_xz
    term_C = Z_TOKEN * m + f_yz

    return pp([term_A, term_B, term_C])


def push_through_coface(word: list[int], coface_slot: list[list[int]]) -> list[int]:
    images = [coface_slot[0], coface_slot[2]]
    out: list[int] = []
    for letter in word:
        img = images[abs(letter) - 1]
        out.extend(img if letter > 0 else core.inv_word(img))
        out = core.reduce_word(out)
    return out
