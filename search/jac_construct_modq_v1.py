#!/usr/bin/env python3
"""
search/jac_construct_modq_v1.py -- mod-q construction pipeline for the Jacobson p-power formula
(裁定843, full follow-up to 裁定832's bounded-profiling diagnosis).

Diagnosis recap (scratchpad/profile_jac17.py, cProfile on p=17, 15-min cap): the bottleneck was
NOT the linear algebra (already mod-q since 裁定806) but the CONSTRUCTION itself
(search/jac_chk_v1.py's word_bracket/apply_substitution/theta_apply/tau_apply, using exact
Python Fraction arithmetic). Measured: theta_apply calls 1-5 (s_1..s_5, term counts 17-6188)
took 50.8s combined; call #6 alone (s_6, term count 12376, barely larger than the CUMULATIVE
sum of calls 1-5) did not complete within the remaining ~850s of the 15-minute cap -- clear
super-linear (worse than O(n)) blowup in the exact-Fraction machinery, explaining the GHA 2-hour
timeout for both p=17 and p=19.

Fix (裁定843, approved): rewrite the ENTIRE construction pipeline (word_bracket,
apply_substitution, theta_apply, tau_apply, build_jacobson_s) to use bounded INTEGER
mod-q arithmetic throughout (two large primes Q1,Q2, matching search/jac_chk2_modq_v1.py's
existing linear-algebra primes) instead of Python Fractions -- construction is run TWICE
(once per prime), not shared/cached across primes as the old design did (since there is no
longer an "exact" intermediate result to share; each prime gets its own independently
mod-reduced construction from scratch).

Regression anchor (裁定843 requirement ①): p=5,7,11's ALREADY-KNOWN exact values (dim R_p,
S3-isotypic type m_triv/m_sgn/m_std, from search/certs/jac_chk_v1_20260811.json) MUST be
reproduced by this mod-q construction before it is trusted for p=17,19,23. Checked in
scratchpad/jac_construct_modq_regression_test.py (not this module -- this module is pure
library code).

Requirement ② (裁定843, "可能なら"): the s_i are built via a running dict-of-dicts
(z_by_tpower, keyed by t-power) whose per-key dict is ALREADY continuously reduced (word_add
combines like terms immediately, every step) -- this is inherited unchanged from
search/jac_chk_v1.py's own build_jacobson_s structure (no separate "intermediate suppression"
needed there beyond what dict-accumulation already does). The REAL intermediate blowup was in
apply_substitution's per-letter tensor expansion (building up "cur" as a full tensor product
before final consolidation) -- mod-q bounds the COEFFICIENT SIZE (the actual measured cost
driver, per the profile: Fraction object construction/gcd-reduction dominated, not dict size
growth alone) but does NOT change the ALGORITHM's term-count growth pattern. Per 裁定843's own
instruction ("過剰設計は不要"), this module does NOT restructure apply_substitution's term-count
behavior -- only its coefficient arithmetic -- since the diagnosis attributed the cost to
Fraction overhead (confirmed: fractions.py's reverse/_add/_from_coprime_ints/__new__ accounted
for the overwhelming majority of self-time in the profile), not fundamentally to term count.

No verdict language. Pure construction library -- no cert output from this module itself.
"""


def word_bracket_modq(u, v, q):
    """[u,v] via free-Lie bracket on tensor-algebra words (letter 0=x,1=y), coefficients as
    bounded Python ints mod q (NOT Fractions)."""
    out = {}
    for w1, c1 in u.items():
        for w2, c2 in v.items():
            c = (c1 * c2) % q
            if c == 0:
                continue
            k1, k2 = w1 + w2, w2 + w1
            out[k1] = (out.get(k1, 0) + c) % q
            out[k2] = (out.get(k2, 0) - c) % q
    return {w: c for w, c in out.items() if c != 0}


def word_add_modq(*ds, q=None):
    out = {}
    for d in ds:
        for w, c in d.items():
            out[w] = (out.get(w, 0) + c) % q
    return {w: c for w, c in out.items() if c != 0}


def word_scale_modq(d, s, q):
    s = s % q
    return {w: (c * s) % q for w, c in d.items() if (c * s) % q != 0}


def build_jacobson_s_modq(p, q):
    """Returns list [s_1, ..., s_{p-1}], each a dict word_tuple->int-mod-q, via iterated
    application of ad(tx+y) to x, tracking t-power exactly -- mod-q analogue of
    search/jac_chk_v1.py's build_jacobson_s. ALL arithmetic is bounded-integer mod q."""
    X = {(0,): 1 % q}
    z_by_tpower = {0: dict(X)}
    for _ in range(p - 1):
        nxt = {}
        for k, wd in z_by_tpower.items():
            brx = word_bracket_modq({(0,): 1 % q}, wd, q)
            if brx:
                nxt[k + 1] = word_add_modq(nxt.get(k + 1, {}), brx, q=q)
            bry = word_bracket_modq({(1,): 1 % q}, wd, q)
            if bry:
                nxt[k] = word_add_modq(nxt.get(k, {}), bry, q=q)
        z_by_tpower = nxt

    s_list = []
    for i in range(1, p):
        coeff_ti_minus_1 = z_by_tpower.get(i - 1, {})
        inv_i = pow(i % q, q - 2, q)
        s_i = word_scale_modq(coeff_ti_minus_1, inv_i, q)
        s_list.append(s_i)
    leftover = z_by_tpower.get(p - 1, {})
    return s_list, leftover


def apply_substitution_modq(vec, img_x, img_y, q):
    """Apply the linear substitution x->img_x, y->img_y to a tensor-word element vec (dict
    word_tuple->int-mod-q), via word-by-word replacement and multinomial re-expansion -- mod-q
    analogue of search/jac_chk_v1.py's apply_substitution.

    *** PERFORMANCE FIX (裁定843 requirement ②, self-discovered during this run) ***: an earlier
    version of this function called word_add_modq(out, cur, q=q) ONCE PER WORD in vec -- since
    word_add_modq REBUILDS a fresh dict by iterating over BOTH input dicts' full key sets every
    call, and `out` grows to the FINAL accumulated size (up to ~24310 terms for the largest s_i
    at p=17) over the course of the loop, this made the outer accumulation itself O(n^2) in the
    number of words (up to ~24310^2 ~ 6*10^8 operations for the largest s_i) -- NOT a term-count
    blowup in apply_substitution's own per-letter expansion (which was already bounded and fine,
    contrary to what this function's docstring originally speculated). Measured: p=17 did not
    complete within ~12 minutes and grew to 1.2GB+ resident memory before being killed -- this
    matches the O(n^2) accumulation pattern, not a fundamentally exponential term-count blowup.
    FIXED here by accumulating directly into a single mutable dict via in-place updates
    (out[key] = out.get(key,0)+val), giving O(total number of (word, resulting-term) pairs
    across the whole vec) instead of O(n^2) -- the term-count growth pattern per INDIVIDUAL word
    substitution is otherwise UNCHANGED (not restructured further, per 裁定843's "過剰設計は
    不要" instruction -- this fix is the accumulation pattern only, not the substitution
    algorithm itself)."""
    out = {}
    for w, c in vec.items():
        cur = {(): c % q}
        for letter in w:
            img = img_x if letter == 0 else img_y
            nxt = {}
            for w1, c1 in cur.items():
                for w2, c2 in img.items():
                    key = w1 + w2
                    cc = (c1 * c2) % q
                    if cc != 0:
                        nxt[key] = (nxt.get(key, 0) + cc) % q
            cur = nxt
        for key, val in cur.items():
            nv = (out.get(key, 0) + val) % q
            if nv == 0:
                if key in out:
                    del out[key]
            else:
                out[key] = nv
    return out


def theta_apply_modq(vec, q):
    return apply_substitution_modq(vec, {(1,): 1 % q}, {(0,): 1 % q}, q)


def tau_apply_modq(vec, q):
    # x -> y ; y -> -(x+y)   (leading/associated-graded action, same convention as
    # search/jac_chk_v1.py's tau_apply)
    img_x = {(1,): 1 % q}
    img_y = {(0,): (-1) % q, (1,): (-1) % q}
    return apply_substitution_modq(vec, img_x, img_y, q)
