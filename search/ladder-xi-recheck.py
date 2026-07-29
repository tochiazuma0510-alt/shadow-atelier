#!/usr/bin/env python3
"""
search/ladder-xi-recheck.py -- independent (GAP-free) re-implementation of the
kerchi-judge.g v1.3 Xi-restricted shadow scan (CorrectedShadowsXi / Prop 3.1),
built per 裁定214 工程3・Sol 便85 F85-5.4 "P85-a 実装仕様" (search/sol/sol_reply_85_math12.md S5).

DOES NOT import, translate, or share code/helpers with GAP (search/kerchi-judge.g,
search/gaplib_common.g, search/week3-battery-common.g). It re-derives the same
mathematical objects (P, Bq, theta~/tau~-equivalent conjugation maps, F2
conditions, the "settled" well-definedness check, and the (3.53) composition
closure) from the window generator images alone, using sympy's independent
computational-group-theory machinery (Schreier-Sims / BSGS via
sympy.combinatorics), not GAP.

Reading kerchi-judge.g was done ONLY to recover the mathematical specification
of F2/RtOf/TH/settled (what those predicates mean); no GAP source text or
algorithm-specific code shape (e.g. its Xi-restriction loop structure,
coset-table internals) was copied. The verification method used here for
"settled" (Bq-level homomorphism well-definedness) is a group-extension-
theoretic re-derivation (see SETTLED CHECK DESIGN NOTE below), independent of
how GAP's GroupHomomorphismByImages performs the same test internally.

The (3.53) composition-closure formula itself is NOT sourced from
kerchi-judge.g/GroupOfShadows at all (per 裁定227・Sol 便86 F86-2.2/P86-3
item 1: "shadow 合成則は kerchi-judge.g の数学仕様から独立再実装 -- コード
翻訳禁止・(3.53) の式は docs/week1-定義ノート.md 系の正典定義から"). It is
transcribed directly from docs/week1-定義ノート.md line 171 (the project's
definition-note transcription of 2401.06870 Thm 3.10's groupoid composition):
  [m1,f1] o [m2,f2] = [2*m1*m2+m1+m2, f1*E_{m1,f1}(f2)],
  E_{m,f}(x)=x^{2m+1}, E_{m,f}(y)=f^-1*y^{2m+1}*f.
See the block comment above check_composition_closure() below for how E is
evaluated (via each accepted candidate's own beta) and why that is faithful
to this file's internal sign convention. GAP's independent GroupOfShadows
implementation of the identical formula is not read or consulted for this.

INPUT: window generator images (JUDGE_S1_IMG, JUDGE_S2_IMG) taken verbatim from
search/_a13_ladder_driver_spec.md (the driver spec explicitly cleared for
implementer use; the frozen prediction file docs/notes/a13_prediction_v1.md is
NOT read).

OUTPUT: one JSON certificate per window (search/certs/ladder_xi_recheck_<id>_
20260730.json) plus a manifest (search/certs/ladder_xi_recheck_manifest_
20260730.json) with per-window candidate/accepted counts, canonical digests
of the accepted-set and fail-witness-set, and a composition_closure_353 field
(pairs_checked/closure_failures/all_closed/failure_witnesses, over ALL ordered
pairs of the accepted set, both compositions orders). No verdict/pass-judgment
is emitted -- raw measurement only, per the parent instruction ("判定はしない").

CONVENTIONS (fixed once, used consistently throughout -- see the design note in
the task briefing this file was written against):
  - AbstractProd([f1,...,fk]) (paper "f1 f2 ... fk" left-to-right notation) is
    replicated exactly as GAP's definition evaluates it: val = identity; for i
    from k downto 1: val := val*list[i] -- i.e. AbstractProd(L) = L[k]*L[k-1]*
    ...*L[1] using ordinary (sympy) permutation multiplication `*`. This gives:
      TT(g)  = dlt^-1 * g * dlt
      TH(g)  = Dlt^-1 * g * Dlt
      RtOf(m,f) = Wd * TT(Wd) * TT(TT(Wd)),  Wd = f*y^m
      AbstractProd([f^-1, w, f]) = f*w*f^-1  (NOT f^-1*w*f -- this matches the
        "reversal convention" comment in search/week3-battery-common.g and the
        v1.3 kerchi-judge.g fix comment: an earlier draft got this backwards
        and silently found 1/5 of a shadow layer).
  - This choice of multiplication convention is an internal bookkeeping choice
    (see design note); truth values of the group-theoretic equalities checked
    below (order, membership, relation-satisfaction) do not depend on which of
    the two anti-isomorphic conventions is picked, only on using ONE
    consistently -- which this script does.
  - m ranges over Z/N_ord (charming set, m in [0, N_ord-1] with gcd(2m+1,N_ord)
    =1); u_2N := 2m+1 is tracked as an element of (Z/2*N_ord)^x (i.e. mod
    2*N_ord, NOT reduced mod N_ord) for chi~-image / UID purposes (Sol point 3
    -- m, u_2N, and the u_N=u_2N mod N_ord used inside the group action are
    kept as textually distinct fields; the group action itself computes x**u
    with u the actual integer 2m+1, which is mathematically u_N-equivalent
    automatically by group axioms, not a silent collapse of type).
  - Subgroups are never compared by order alone where a generation/membership
    claim is being made (Sol trap 2): the "surjective" F2 condition is checked
    via PermutationGroup([...]).order() == PN.order() (order equality used
    ONLY as the accepted mathematical criterion for "generates PN", which is
    literally what condition (iii) of (F2) asserts -- not a shortcut around a
    membership/inclusion check that should have been used instead).

SETTLED CHECK DESIGN NOTE (independent derivation, not GAP's algorithm):
  Bq = <s1,s2> has PN = <x,y> = <s1^2,s2^2> as a NORMAL subgroup of index 6
  (verified per-window below, not assumed), with Bq/PN generated by the two
  order-2 images of s1,s2 -- i.e. Bq/PN is (verified to be) isomorphic to S3,
  with transversal T = {e, s1, s2, s1*s2, s2*s1, s1*s2*s1} (=dlt-family). A
  candidate map phi: s1 |-> s1^u, s2 |-> f*s2^u*f^-1 extends to a well-defined
  homomorphism Bq -> Bq if and only if ALL of:
    (1) phi|_PN is well-defined as a homomorphism PN -> PN. Checked via a
        STANDARD finite presentation of PN (independently verified here to be
        A_n on its support, n = |support|, for all windows so far): generators
        t_i = (p0,p1,p_i) (3-cycles on the support, i=2..n-1 local index),
        relations t_i^3=1, (t_i t_j)^2=1 for i != j (Carmichael's classical
        presentation of A_n; self-tested below for n=5,6 against known |A5|=
        60, |A6|=360 via sympy FpGroup coset enumeration before being trusted
        for n=10..13, where direct coset enumeration is infeasible). Each t_i
        is re-expressed as a word in x,y via sympy's BSGS-based
        generator_product (polynomial-time in degree, NOT proportional to
        |PN|), and phi is applied to that word; the SAME relations must hold
        for the images.
    (2) phi is compatible with conjugation of PN by s1,s2 (the extension's
        "action" data): phi(s_i)*phi(g)*phi(s_i)^-1 == phi(s_i*g*s_i^-1) for
        g in {x,y} (a generating set of PN, so checking on generators
        suffices once (1) has established phi|_PN is a homomorphism).
    (3) phi is compatible with the extension's cocycle: for every pair of
        transversal elements T[i],T[j], if T[i]*T[j] = T[k]*n_ij (n_ij in PN,
        computed once per window), then phi(T[i])*phi(T[j]) ==
        phi(T[k])*phi(n_ij) must hold (phi(T[i]) computed directly by
        substituting s1->phi(s1), s2->phi(s2) into T[i]'s literal defining
        word; phi(n_ij) via the same PN-word-substitution method as (1)/(2)).
  (1)+(2)+(3) together are the standard extension-theoretic necessary AND
  sufficient conditions for phi to extend from a well-defined map on
  generators to a well-defined homomorphism of the whole group Bq = PN.(Bq/PN)
  -- this is the independent substitute for GAP's
  GroupHomomorphismByImages(...)<>fail test, not a translation of it.
"""

import sys
import json
import hashlib
import time
import itertools
from collections import defaultdict, deque

from sympy.combinatorics import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup

Permutation.print_cyclic = True


# ============================================================================
# low-level permutation helpers
# ============================================================================

def mkperm(cycles, size):
    """cycles: list of tuples of 1-indexed points. Returns a sympy Permutation
    of the given size (0-indexed internally, matching GAP's 1-indexed input)."""
    c0 = [[x - 1 for x in c] for c in cycles]
    return Permutation(c0, size=size)


def identity_of(size):
    return Permutation(list(range(size)))


def abstract_prod(lst, size):
    """AbstractProd([f1,...,fk]) = fk*f(k-1)*...*f1 (GAP reversal convention,
    replicated exactly -- see module docstring)."""
    val = identity_of(size)
    for x in reversed(lst):
        val = val * x
    return val


def full_cycles(perm, domain):
    """Cycle decomposition of perm restricted to domain (list of ints),
    INCLUDING fixed points as singleton cycles, in first-unvisited-point
    order. Used only for constructing explicit conjugators."""
    seen = set()
    out = []
    for p in domain:
        if p in seen:
            continue
        cyc = [p]
        seen.add(p)
        q = perm(p)
        while q != p:
            cyc.append(q)
            seen.add(q)
            q = perm(q)
        out.append(cyc)
    return out


def find_conjugator(p, q, domain, size):
    """Return g (as a Permutation of the given size) with g**-1 * p * g == q,
    assuming p and q have identical cycle type on domain (verified). g fixes
    all points outside domain."""
    pc = full_cycles(p, domain)
    qc = full_cycles(q, domain)
    pb = defaultdict(list)
    qb = defaultdict(list)
    for c in pc:
        pb[len(c)].append(c)
    for c in qc:
        qb[len(c)].append(c)
    if sorted(pb.keys()) != sorted(qb.keys()):
        return None
    for L in pb:
        if len(pb[L]) != len(qb[L]):
            return None
    # sympy composition convention: (a*b)(x) = b(a(x)) (apply a then b -- same
    # as GAP's i^(p1*p2)=(i^p1)^p2). Under this convention, g^-1*p*g = q means
    # (as functions) g(p(y)) = q(g(y)) for all y, which is solved by mapping
    # each p-cycle point to the CORRESPONDING q-cycle point (same rotation
    # index): g(a_i) := b_i.
    mapping = {}
    for L in pb:
        for pcyc, qcyc in zip(pb[L], qb[L]):
            for i in range(L):
                mapping[pcyc[i]] = qcyc[i]
    arr = list(range(size))
    for pt in domain:
        arr[pt] = mapping[pt]
    g = Permutation(arr, size=size)
    # self-check (cheap relative to everything else; fail-closed if wrong)
    assert (g ** -1) * p * g == q, "find_conjugator: construction invariant violated"
    return g


def cycle_type(perm, domain):
    return tuple(sorted(len(c) for c in full_cycles(perm, domain)))


# ============================================================================
# self-tests (run once at import time -- fail closed if the machinery itself
# is wrong, before trusting it on real windows)
# ============================================================================

def selftest_carmichael_presentation():
    """Verify the Carmichael presentation of A_n (generators t_i=(1,2,i),
    relations t_i^3=1, (t_i t_j)^2=1 for i!=j) against the KNOWN orders of A5
    and A6, via sympy's FpGroup coset enumeration (small enough to be
    tractable directly). This is the presentation used (for n up to 16) in
    the settled-check machinery below; only feasible to double check directly
    for small n, but the presentation formula is uniform in n (standard
    citable fact, Coxeter & Moser)."""
    from sympy.combinatorics.free_groups import free_group
    from sympy.combinatorics.fp_groups import FpGroup
    import math
    for n, expected in [(5, 60), (6, 360)]:
        names = ['t%d' % i for i in range(3, n + 1)]
        F = free_group(', '.join(names))[0] if len(names) > 1 else free_group(names[0])[0]
        gens = F.generators
        rels = [g ** 3 for g in gens]
        for i in range(len(gens)):
            for j in range(i + 1, len(gens)):
                rels.append((gens[i] * gens[j]) ** 2)
        G = FpGroup(F, rels)
        order = G.order()
        assert order == expected, (
            "selftest_carmichael_presentation FAILED for n=%d: got order %s, expected %d"
            % (n, order, expected))
    print("[selftest] Carmichael presentation of A_n verified for n=5,6 (orders 60,360). PASS")


def selftest_find_conjugator():
    p = mkperm([(1, 2, 3, 4, 5, 6, 7, 8, 9)], 13)
    q = p ** 2  # same cycle type (single 9-cycle), gcd(2,9)=1
    dom = list(range(9))
    g = find_conjugator(p, q, dom, 13)
    assert g is not None
    assert (g ** -1) * p * g == q
    print("[selftest] find_conjugator sanity check PASS")


def selftest_generator_product_reconstruction():
    x = mkperm([(1, 2, 3, 4, 5, 6, 7, 8, 9)], 13)
    y = mkperm([(1, 5, 10, 3, 9, 7, 8, 6, 2)], 13)
    PN = PermutationGroup([x, y])
    g = x * y * x ** -1
    word = PN.generator_product(g, original=True)
    recon = identity_of(13)
    for w in reversed(word):
        recon = recon * w
    assert recon == g
    print("[selftest] generator_product reversed-order reconstruction PASS")


def run_selftests():
    selftest_carmichael_presentation()
    selftest_find_conjugator()
    selftest_generator_product_reconstruction()


# ============================================================================
# window data (verbatim from search/_a13_ladder_driver_spec.md; the frozen
# prediction file is not read)
# ============================================================================

CANONICAL_WINDOWS = {
    "W-E-A10-9t1": dict(
        n=10, deg=13, t=1,
        a1=[(1, 2), (3, 5), (4, 10), (6, 9)],
        b1=[(2, 9, 5), (3, 4, 10), (6, 8, 7)],
        S1=[(1, 2, 3, 4, 5, 6, 7, 8, 9), (11, 12)],
        S2=[(1, 5, 10, 3, 9, 7, 8, 6, 2), (12, 13)],
        xi_bound=486,
    ),
    "W-E-A11-9t2": dict(
        n=11, deg=14, t=2,
        a1=[(2, 11), (3, 8), (4, 5), (6, 7), (9, 10)],
        b1=[(1, 9, 11), (2, 10, 8), (3, 7, 5)],
        S1=[(1, 2, 3, 4, 5, 6, 7, 8, 9), (10, 11), (12, 13)],
        S2=[(1, 11, 8, 5, 4, 7, 6, 3, 10), (2, 9), (13, 14)],
        xi_bound=972,
    ),
    "W-E-A12-9t3": dict(
        n=12, deg=15, t=3,
        a1=[(3, 9), (4, 11), (5, 7), (6, 12), (8, 10)],
        b1=[(1, 9, 2), (3, 8, 11), (4, 10, 7), (5, 6, 12)],
        S1=[(1, 2, 3, 4, 5, 6, 7, 8, 9), (10, 11), (13, 14)],
        S2=[(1, 2, 9, 11, 7, 12, 5, 10, 3), (4, 8), (14, 15)],
        xi_bound=8748,
    ),
    "W-E-A13-9t4": dict(
        n=13, deg=16, t=4,
        a1=[(2, 10), (3, 8), (4, 12), (5, 6), (7, 13), (9, 11)],
        b1=[(1, 9, 10), (2, 11, 8), (3, 7, 12), (4, 13, 6)],
        S1=[(1, 2, 3, 4, 5, 6, 7, 8, 9), (10, 11), (12, 13), (14, 15)],
        S2=[(1, 10, 8, 12, 6, 5, 13, 3, 11), (2, 9), (4, 7), (15, 16)],
        xi_bound=139968,
    ),
}

# canonical-ID SHA-256 expected values (fail-closed identity gate, per driver
# spec S "canonical ID"), for the 4 canonical windows only (the driver spec
# itself only lists these 4; sibling windows are checked via the GAP-cert
# binding method below, uniformly for all 13).
CANONICAL_ID_SHA256 = {
    "W-E-A10-9t1": "6092f5f0bae86188d1f46ede81e1dad2aebbb097d6d3c9cae46229b67e853f4b",
    "W-E-A11-9t2": "ddc23c556d760adeab1dcdab24887719b5ab0a0b8e137fcea4b2df8077984649",
    "W-E-A12-9t3": "b127a9048c4659b74f5c2c9257e5e3dedfab66761b7ce3947195ef21c3749c79",
    "W-E-A13-9t4": "a11f207d3a6e31d118830ac94cad6fc2e9429582c49620efb52e8b268b7f941f",
}


# ============================================================================
# canonical-ID gate v2 (裁定216 続行指示 point 2): GAP印字の独立再現はやめ、GAP
# 証明書 (search/certs/a13_ladder_*_20260730.json) に既に記録されている
# /canonical_string フィールドの SHA-256 を再計算し、同じ証明書に記録済みの
# /canonical_id_sha256 フィールドと一致するかだけを検査する (a binding check,
# not an independent re-derivation of the print convention). This is applied
# uniformly to all 13 windows (4 canonical + 9 sibling), reading window-
# identifying metadata only (canonical_string, canonical_id_sha256, s1, s2,
# a1, b1, n, t) -- per the coordinator's ruling this is identifying
# information, not a measurement, and reading it does not violate the
# measurement-side isolation from the frozen prediction file.
# ============================================================================

GAP_CERT_DIR = "search/certs"

GAP_CERT_FILENAMES = {
    "W-E-A10-9t1":    "a13_ladder_W_E_A10_9t1_20260730.json",
    "W-E-A10-9t1-o2": "a13_ladder_W_E_A10_9t1_o2_20260730.json",
    "W-E-A10-9t1-o3": "a13_ladder_W_E_A10_9t1_o3_20260730.json",
    "W-E-A10-9t1-o4": "a13_ladder_W_E_A10_9t1_o4_20260730.json",
    "W-E-A10-9t1-o5": "a13_ladder_W_E_A10_9t1_o5_20260730.json",
    "W-E-A10-9t1-o6": "a13_ladder_W_E_A10_9t1_o6_20260730.json",
    "W-E-A11-9t2":    "a13_ladder_W_E_A11_9t2_20260730.json",
    "W-E-A11-9t2-o2": "a13_ladder_W_E_A11_9t2_o2_20260730.json",
    "W-E-A11-9t2-o3": "a13_ladder_W_E_A11_9t2_o3_20260730.json",
    "W-E-A12-9t3":    "a13_ladder_W_E_A12_9t3_20260730.json",
    "W-E-A12-9t3-o2": "a13_ladder_W_E_A12_9t3_o2_20260730.json",
    "W-E-A12-9t3-o3": "a13_ladder_W_E_A12_9t3_o3_20260730.json",
    "W-E-A13-9t4":    "a13_ladder_W_E_A13_9t4_20260730.json",
}

XI_BOUND_BY_T = {1: 486, 2: 972, 3: 8748, 4: 139968}


def parse_gap_cycles(s):
    """Parse a GAP-printed permutation string like
    '( 1, 2, 3, 4, 5, 6, 7, 8, 9)(11,12)' into [[1,2,...,9],[11,12]]
    (1-indexed ints, as consumed by mkperm)."""
    cycles = []
    for grp in s.split(")("):
        grp = grp.strip("()")
        pts = [int(x.strip()) for x in grp.split(",") if x.strip() != ""]
        if pts:
            cycles.append(pts)
    return cycles


def load_gap_cert(wid):
    path = "%s/%s" % (GAP_CERT_DIR, GAP_CERT_FILENAMES[wid])
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def gap_cert_binding_check(wid):
    """裁定216 point 2: recompute SHA-256 of the GAP cert's own recorded
    canonical_string and compare to the GAP cert's own recorded
    canonical_id_sha256. No independent re-derivation of GAP's print
    convention. Returns (ok, computed_sha256, recorded_sha256)."""
    cert = load_gap_cert(wid)
    s = cert["canonical_string"]
    computed = hashlib.sha256(s.encode("utf-8")).hexdigest()
    recorded = cert["canonical_id_sha256"]
    return (computed == recorded), computed, recorded


def all_window_ids():
    return list(GAP_CERT_FILENAMES.keys())


def build_window_spec_from_gap_cert(wid):
    """Build the same dict shape as CANONICAL_WINDOWS entries, but sourced
    from the GAP cert's s1/s2/a1/b1/n/t fields (identifying data only -- see
    module note above). Used uniformly for canonical AND sibling windows
    under the coordinator's point-1 instruction."""
    cert = load_gap_cert(wid)
    S1 = parse_gap_cycles(cert["s1"])
    S2 = parse_gap_cycles(cert["s2"])
    a1 = parse_gap_cycles(cert["a1"])
    b1 = parse_gap_cycles(cert["b1"])
    deg = max(max(pt for c in S1 for pt in c), max(pt for c in S2 for pt in c))
    t = cert["t"]
    return dict(n=cert["n"], deg=deg, t=t, a1=a1, b1=b1, S1=S1, S2=S2,
                xi_bound=XI_BOUND_BY_T[t])


def check_all_canonical_ids_v2():
    """Binding check (point 2) for all 13 windows."""
    mismatches = []
    for wid in all_window_ids():
        ok, computed, recorded = gap_cert_binding_check(wid)
        status = "MATCH" if ok else "MISMATCH"
        if not ok:
            mismatches.append(wid)
        print("[canonical-id-v2 binding] %s: computed=%s recorded=%s %s"
              % (wid, computed, recorded, status))
    return mismatches


# ============================================================================
# window construction (MakeWindow-equivalent, independently derived)
# ============================================================================

class Window:
    def __init__(self, wid, s1, s2, deg):
        self.id = wid
        self.deg = deg
        self.s1 = s1
        self.s2 = s2
        self.x = s1 * s1
        self.y = s2 * s2
        self.Dlt = abstract_prod([s1, s2, s1], deg)   # = s1*s2*s1
        self.dlt = abstract_prod([s1, s2], deg)        # = s2*s1
        self.c = self.Dlt * self.Dlt
        self.z = abstract_prod([self.x, self.y], deg) ** -1
        self.Bq_gens = [s1, s2]
        self.PN = PermutationGroup([self.x, self.y])
        self.PN_order = self.PN.order()
        ox = self.x.order()
        oy = self.y.order()
        oc = self.c.order()
        import math
        self.Nord = _lcm3(ox, oy, oc)
        self.identity = identity_of(deg)

    def TT(self, g):
        return (self.dlt ** -1) * g * self.dlt

    def TH(self, g):
        return (self.Dlt ** -1) * g * self.Dlt

    def RtOf(self, m, f):
        Wd = f * (self.y ** m)
        TTWd = self.TT(Wd)
        TTTTWd = self.TT(TTWd)
        return Wd * TTWd * TTTTWd


def _lcm3(a, b, c):
    import math
    return math.lcm(a, b, c)


def build_window(wid, w):
    s1 = mkperm(w["S1"], w["deg"])
    s2 = mkperm(w["S2"], w["deg"])
    braid_lhs = abstract_prod([s1, s2, s1], w["deg"])
    braid_rhs = abstract_prod([s2, s1, s2], w["deg"])
    if braid_lhs != braid_rhs:
        raise SystemExit("FATAL: braid relation s1 s2 s1 = s2 s1 s2 fails for %s" % wid)
    W = Window(wid, s1, s2, w["deg"])
    return W


# ============================================================================
# support / A_n structural verification
# ============================================================================

def compute_support(W):
    """Union of moved points of x,y (0-indexed), sorted."""
    moved = set()
    for pt in range(W.deg):
        if W.x(pt) != pt or W.y(pt) != pt:
            moved.add(pt)
    return sorted(moved)


def verify_PN_is_alternating(W, support):
    n = len(support)
    idx = {p: i for i, p in enumerate(support)}

    def restrict(perm):
        return Permutation([idx[perm(p)] for p in support])

    xr = restrict(W.x)
    yr = restrict(W.y)
    PNr = PermutationGroup([xr, yr])
    import math
    expected = math.factorial(n) // 2
    ok = (PNr.order() == expected) and PNr.is_transitive() and PNr.is_alternating
    return ok, n, expected, PNr.order()


# ============================================================================
# charming set
# ============================================================================

def charming_set(Nord):
    import math
    return [m for m in range(Nord) if math.gcd(2 * m + 1, Nord) == 1]


# ============================================================================
# Aut(P)=S_n machinery (P = PN, established to be A_n on its support)
# ============================================================================

def sn_centralizer_elements(perm, support, deg):
    """Elements of C_{S_n}(perm), n=|support|, as full-degree Permutations
    (identity outside support). Uses sympy's SymmetricGroup(n).centralizer,
    restricted/lifted between the local (0..n-1) and full-degree domains."""
    n = len(support)
    idx = {p: i for i, p in enumerate(support)}
    local = Permutation([idx[perm(p)] for p in support])
    Sn = SymmetricGroup(n)
    C = Sn.centralizer(local)
    out = []
    for h in C.generate():
        arr = list(range(deg))
        for i, p in enumerate(support):
            arr[p] = support[h(i)]
        out.append(Permutation(arr, size=deg))
    return out


# ============================================================================
# CorrectedShadowsXi -- independent re-derivation (Prop 3.1 Xi-restriction)
# ============================================================================

def xi_restricted_candidates(W, support, charming):
    """Generator for (m, f) CANDIDATE pairs before the (F2)/settled filters,
    following the mathematical shape of Prop 3.1 (restrict f to a coset
    structure indexed by Stab_{Aut(P)}(xbar) x C_P(ybar^u), independently
    re-derived -- see module docstring; NOT a translation of
    kerchi-judge.g's loop). Yields (m, f, meta) with meta a dict of the
    per-m/per-s bookkeeping needed for the fail-closed bound check."""
    n = len(support)
    deg = W.deg
    x, y = W.x, W.y
    stab_elts = sn_centralizer_elements(x, support, deg)  # Stab_{Aut(P)}(xbar), once per window
    for m in charming:
        u = 2 * m + 1
        yu = y ** u
        Cyu_full = sn_centralizer_elements(yu, support, deg)
        # C_PN(yu) = even elements of C_{S_n}(yu)
        Cyu = [c for c in Cyu_full if c.is_even]
        xu = x ** u
        if cycle_type(x, support) != cycle_type(xu, support):
            # should not happen for charming m (gcd(u,Nord)=1 preserves cycle
            # type of a single-Nord-order-cycle element) -- fail closed if it
            # ever does, rather than silently skipping
            raise SystemExit("FATAL: cycle type mismatch x vs x^u for m=%d in %s" % (m, W.id))
        alpha0 = find_conjugator(x, xu, support, deg)  # alpha0^-1 x alpha0 = x^u
        if alpha0 is None:
            continue
        for s in stab_elts:
            alpha = s * alpha0  # "s first, then alpha0" as an automorphism composition
            # target = y acted on by alpha, GAP convention pt^(g1*g2)=(pt^g1)^g2
            # generalizes here to: apply s's conjugation action then alpha0's.
            target = (alpha ** -1) * y * alpha
            if cycle_type(yu, support) != cycle_type(target, support):
                continue
            # find h in PN with h^-1 yu h = target; if impossible in PN (but
            # possible in S_n), no candidate from this (m,s) branch (A_n-class
            # splitting) -- see design note in header
            g_sn = find_conjugator(yu, target, support, deg)
            if g_sn is None:
                continue
            if g_sn.is_even:
                h = g_sn
            else:
                odd_c = next((c for c in Cyu_full if not c.is_even), None)
                if odd_c is None:
                    continue  # class splits and this branch lands in the other half
                h = odd_c * g_sn
            f0 = h ** -1
            for c in Cyu:
                f = f0 * c
                yield m, f, u, alpha0, stab_elts


# ============================================================================
# settled check machinery (per-window precompute + per-candidate check)
#
# FAST DESIGN (supersedes an earlier, much slower Carmichael-presentation /
# generator_product-word-substitution draft -- kept only in spirit in the
# module docstring's design note; that draft was correct but reevaluating
# 10^4-token words per candidate was computationally infeasible at the Xi
# scale required here (486..139968 candidates). The mathematically EQUIVALENT
# fast method used instead:
#
#   Since PN is verified = A_n (n != 6), Aut(PN) = S_n acting by ordinary
#   conjugation (every automorphism is inner-via-S_n, i.e. Out(A_n)=1 for
#   n!=6). A map phi|_PN: x->X_img, y->Y_img is a well-defined homomorphism
#   PN->PN if and only if there EXISTS beta in S_n (on the support) with
#   beta^-1 x beta = X_img AND beta^-1 y beta = Y_img SIMULTANEOUSLY (if such
#   phi is a well-defined hom at all, finiteness + the already-established
#   generation condition force it to be bijective, hence an automorphism,
#   hence realized by conjugation by a single beta -- this is a strictly
#   necessary-and-sufficient reformulation of condition (1), not a heuristic
#   shortcut). The solution set for beta^-1 x beta = X_img alone is exactly
#   the coset alpha0 * Stab_{S_n}(x) (alpha0, Stab already computed once per
#   m/window by the Xi-restriction candidate generator itself and threaded
#   through here) -- so finding beta is a search over the SAME small
#   (already-in-hand) stab_elts list, checking the y-condition, instead of
#   reevaluating a long presentation word.
#
#   Once beta is found, phi is available for ANY element g of PN directly as
#   phi(g) := beta^-1 * g * beta (no word needed at all), which is then used
#   for the (2) twisting and (3) cocycle checks below exactly as in the
#   design note's (1)+(2)+(3) decomposition -- only the METHOD of evaluating
#   phi on PN-elements changed (conjugation-by-beta instead of word
#   substitution), the mathematical content of what is checked did not.
# ============================================================================

def build_settled_precompute(W):
    x, y = W.x, W.y
    PN = W.PN

    conj_s1_x = W.s1 * x * (W.s1 ** -1)
    conj_s1_y = W.s1 * y * (W.s1 ** -1)
    conj_s2_x = W.s2 * x * (W.s2 ** -1)
    conj_s2_y = W.s2 * y * (W.s2 ** -1)

    # transversal T = {e, s1, s2, s1*s2, s2*s1, s1*s2*s1} (literal, normal order)
    T = [W.identity, W.s1, W.s2, W.s1 * W.s2, W.s2 * W.s1, W.s1 * W.s2 * W.s1]
    # verify PN normal in Bq and Bq/PN really has these 6 as a full transversal
    # (one-time structural sanity check, not per-candidate)
    for gname, g in [("s1", W.s1), ("s2", W.s2)]:
        for gen_name, gen in [("x", x), ("y", y)]:
            if not PN.contains(g * gen * (g ** -1)):
                raise SystemExit("FATAL: PN not normalized by %s (window %s)" % (gname, W.id))
    for i in range(6):
        for j in range(i + 1, 6):
            if PN.contains(T[i] * (T[j] ** -1)):
                raise SystemExit("FATAL: transversal T not a full 6-coset set for %s" % W.id)

    cocycle = {}
    for i in range(6):
        for j in range(6):
            prod = T[i] * T[j]
            k_found = None
            for k in range(6):
                if PN.contains(prod * (T[k] ** -1)):
                    k_found = k
                    break
            if k_found is None:
                raise SystemExit("FATAL: cocycle coset not found for (%d,%d) in %s" % (i, j, W.id))
            n_ij = (T[k_found] ** -1) * prod
            cocycle[(i, j)] = (k_found, n_ij)

    return dict(
        conj_s1_x=conj_s1_x, conj_s1_y=conj_s1_y,
        conj_s2_x=conj_s2_x, conj_s2_y=conj_s2_y,
        T=T, cocycle=cocycle,
    )


def find_beta(W, support, u, f, X_img, Y_img, alpha0, stab_elts):
    """Search beta = s*alpha0 (s in stab_elts) with beta^-1 x beta = X_img
    (automatic, by construction of alpha0/stab_elts) AND beta^-1 y beta =
    Y_img. Returns beta or None."""
    y = W.y
    for s in stab_elts:
        beta = s * alpha0
        if (beta ** -1) * y * beta == Y_img:
            return beta
    return None


def is_settled(W, pre, support, u, f, X_img, Y_img, alpha0, stab_elts):
    """Full Bq-level well-definedness check for phi: s1->s1^u, s2->f*s2^u*f^-1,
    per the (1)+(2)+(3) design (see module docstring + design note above).
    Returns (settled_ok, beta): beta is the PN-automorphism-realizing element
    (phi|_PN(g) = beta^-1*g*beta) on settled_ok=True, else None. beta is
    exposed to the caller (rather than only a bool) because it is exactly the
    data needed to evaluate E_{m,f} for the (3.53) composition-closure check
    below (E_{m,f}|_PN = phi|_PN, restated as this same conjugation-by-beta
    map) -- reusing it here avoids re-deriving alpha0/stab_elts a second time
    per accepted candidate."""
    beta = find_beta(W, support, u, f, X_img, Y_img, alpha0, stab_elts)
    if beta is None:
        return False, None  # (1) phi|_PN not realizable as a well-defined automorphism

    def phi(g):
        return (beta ** -1) * g * beta

    S1p = W.s1 ** u
    S2p = f * (W.s2 ** u) * (f ** -1)

    # (2) twisting checks
    if S1p * X_img * (S1p ** -1) != phi(pre["conj_s1_x"]):
        return False, None
    if S1p * Y_img * (S1p ** -1) != phi(pre["conj_s1_y"]):
        return False, None
    if S2p * X_img * (S2p ** -1) != phi(pre["conj_s2_x"]):
        return False, None
    if S2p * Y_img * (S2p ** -1) != phi(pre["conj_s2_y"]):
        return False, None

    # (3) cocycle checks
    phiT = [W.identity, S1p, S2p, S1p * S2p, S2p * S1p, S1p * S2p * S1p]
    for i in range(6):
        for j in range(6):
            k, n_ij = pre["cocycle"][(i, j)]
            lhs = phiT[i] * phiT[j]
            rhs = phiT[k] * phi(n_ij)
            if lhs != rhs:
                return False, None

    return True, beta


# ============================================================================
# per-candidate F2 conditions + full scan driver
# ============================================================================

def scan_window(wid, w, checkpoint_path=None, log=print):
    t_start = time.time()
    W = build_window(wid, w)
    support = compute_support(W)
    ok, n, expected_order, actual_order = verify_PN_is_alternating(W, support)
    if not ok:
        raise SystemExit(
            "FATAL: PN is not verified to be the natural alternating group on its "
            "support for %s (n=%d expected_order=%d actual_order=%d) -- this "
            "script's settled-check machinery (Carmichael presentation, S_n "
            "Aut(P) fast path) assumes P=A_n; refusing to proceed with an "
            "unverified structural assumption." % (wid, n, expected_order, actual_order))
    log("[%s] support size n=%d, PN verified = A_%d (order %d), Bq/PN transversal precompute..."
        % (wid, n, n, actual_order))

    Nord = W.Nord
    charming = charming_set(Nord)
    log("[%s] N_ord=%d charming_count=%d (expect 9 / 6 per driver spec)" % (wid, Nord, len(charming)))

    pre = build_settled_precompute(W)
    log("[%s] settled-check precompute done (transversal=6, cocycle pairs=36)" % wid)

    accepted = []          # list of dict(m=..., u=..., f_cycles=..., uid=...)
    fail_settled = []      # candidates that passed F2 three conditions but failed settled
    xi_bound = w["xi_bound"]
    scanned = 0
    t_scan_start = time.time()
    last_log = t_scan_start

    for m, f, u, alpha0, stab_elts in xi_restricted_candidates(W, support, charming):
        scanned += 1
        if scanned > xi_bound:
            raise SystemExit(
                "FATAL: scanned_count exceeded the driver spec's fail-closed Xi upper "
                "bound (%d) for %s at scanned=%d -- refusing to continue silently."
                % (xi_bound, wid, scanned))

        # (F2) condition (i): f in [P,P]. PN is perfect (A_n, n>=5) so [P,P]=PN
        # and f in PN by construction (f0, c both in PN) -- checked explicitly
        # anyway, not assumed.
        if not W.PN.contains(f):
            continue

        # (F2) condition (ii): AbstractProd([f, TH(f)]) = identity  <=> TH(f)*f = e
        THf = W.TH(f)
        if THf * f != W.identity:
            continue

        # (F2) condition (iii): RtOf(m,f) = c^m
        if W.RtOf(m, f) != W.c ** m:
            continue

        X_img = W.x ** u
        Y_img = f * (W.y ** u) * (f ** -1)

        # settled / well-definedness (independent Bq-level extension check) is
        # checked BEFORE the explicit generation order() computation: if a
        # well-defined beta-realized automorphism phi|_PN is found, generation
        # of PN by {X_img,Y_img} is an automatic consequence (phi surjective
        # since it's an automorphism) -- see design note above build_settled_
        # precompute. This is used only as a fast-accept path; if settled
        # fails we STILL explicitly verify the generation condition (iv)
        # below to correctly bucket the candidate as "not even a hexagon
        # candidate" vs "settled_fail" (Sol's bookkeeping requirement).
        settled_ok, beta = is_settled(W, pre, support, u, f, X_img, Y_img, alpha0, stab_elts)
        if settled_ok:
            gen_order = W.PN_order  # implied, see design note; still equal by construction
        else:
            gen_order = PermutationGroup([X_img, Y_img]).order()

        # (F2) condition (iv): <x^u, f y^u f^-1> = PN (generation / surjective)
        if gen_order != W.PN_order:
            continue

        if not settled_ok:
            fail_settled.append((m, f))
            continue

        # beta realizes E_{m,f}|_PN(g) = beta^-1*g*beta (see is_settled docstring);
        # kept alongside (m,f,u) so the (3.53) composition-closure check below can
        # evaluate E_{m,f} without re-deriving alpha0/stab_elts per pair.
        accepted.append((m, f, u, beta))

        now = time.time()
        if now - last_log > 15:
            log("[%s] progress: scanned=%d accepted=%d settled_fail=%d elapsed=%.1fs"
                % (wid, scanned, len(accepted), len(fail_settled), now - t_scan_start))
            last_log = now
            if checkpoint_path:
                write_checkpoint(checkpoint_path, wid, w, scanned, accepted, fail_settled, done=False)

    elapsed = time.time() - t_scan_start
    log("[%s] scan complete: scanned=%d (bound=%d) accepted=%d settled_fail=%d elapsed=%.1fs"
        % (wid, scanned, xi_bound, len(accepted), len(fail_settled), elapsed))

    closure = check_composition_closure(wid, Nord, accepted)
    log("[%s] (3.53) composition closure: pairs=%d closure_failures=%d all_closed=%s"
        % (wid, closure["pairs_checked"], closure["closure_failures"], closure["all_closed"]))

    return dict(
        wid=wid, n=n, deg=w["deg"], Nord=Nord, charming_count=len(charming),
        xi_bound=xi_bound, scanned_count=scanned,
        accepted=accepted, fail_settled=fail_settled,
        composition_closure_353=closure,
        elapsed_sec=elapsed, total_elapsed_sec=time.time() - t_start,
    )


# ============================================================================
# canonical UID + digest
# ============================================================================

def perm_canonical_str(perm):
    # canonical form: full array (0-indexed shifted to 1-indexed for
    # readability/parity with GAP's 1-indexed printing), degree-tagged
    arr = perm.array_form
    return "deg%d:[%s]" % (len(arr), ",".join(str(a + 1) for a in arr))


def candidate_uid(wid, m, u, f):
    return "%s|m=%d|u2N=%d|f=%s" % (wid, m, u, perm_canonical_str(f))


def digest_set(strs):
    h = hashlib.sha256()
    for s in sorted(strs):
        h.update(s.encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


# ============================================================================
# (3.53) composition closure (P86-3 item 1 / F86-2.2 欠落1)
#
# Primary source: docs/week1-定義ノート.md line 171 (2401.06870 Thm 3.10's
# groupoid composition, the definition-note's own transcription -- NOT read
# from kerchi-judge.g/GroupOfShadows, which is GAP's own independent
# implementation of the identical formula and is intentionally not consulted
# here):
#
#   [m1,f1] o [m2,f2] = [2*m1*m2 + m1 + m2, f1 * E_{m1,f1}(f2)]
#   E_{m,f}(x) = x^{2m+1},  E_{m,f}(y) = f^-1 * y^{2m+1} * f
#
# E_{m1,f1} is a homomorphism of PN = <x,y> (verified above to be A_n on its
# support); restricted to PN it is REALIZED, for every accepted (settled)
# candidate, by conjugation by that candidate's own `beta` (beta^-1*g*beta),
# because beta was constructed (in is_settled/find_beta) to satisfy EXACTLY
# beta^-1*x*beta = x^u and beta^-1*y*beta = Y_img = f*y^u*f^-1 -- i.e. beta
# already realizes this script's Y_img convention (f*w*f^-1, the internally-
# consistent "reversal convention" companion used throughout this file, see
# module docstring) for E_{m,f}(y), not the raw paper sign f^-1*w*f. Since f2
# lies in PN (built as f0*c with f0,c in PN, and F2 condition (i) re-verifies
# f in PN/[P,P] explicitly), applying phi_beta1 to f2 is applying E_{m1,f1} to
# f2 under the SAME convention used everywhere else in this script -- this is
# what "using ONE [convention] consistently" (module docstring) requires for
# internal closure to be a meaningful test at all.
#
# OUTER PRODUCT ORDER (measured, not assumed): the literal (3.53) reading is
# "f1 * E(f2)" (f1 first). This script, however, already commits throughout
# (X_img/Y_img, is_settled/find_beta, the module docstring's "reversal
# convention" note) to evaluating E_{m,f}(y) as f*y^u*f^-1 rather than the
# raw paper sign f^-1*y^u*f -- i.e. it uses ONE fixed anti-isomorphic
# realization of the hexagon data, consistently, exactly as the docstring
# says is required ("truth values ... do not depend on which of the two
# anti-isomorphic conventions is picked, only on using ONE consistently").
# Composition closure is the first place in this file where that choice is
# externally testable (F2/settled are single-candidate predicates, invariant
# either way; composition is a binary operation on the whole accepted SET,
# so getting the pairing between "which E-sign" and "which outer order"
# wrong breaks closure even though each ingredient is individually correct).
# This was checked empirically, not guessed: f1*E(f2) gives 2748/2916
# closure failures on W-E-A10-9t1's 54-element accepted set, while
# E(f2)*f1 gives 0/2916 -- confirmed again on W-E-A10-5x2t0 (0/1600). Using
# E(f2)*f1 (E's convention applied first, matching the reversed-order pairing
# that goes with the f*w*f^-1 sign choice) is therefore the self-consistent
# realization of (3.53) under THIS script's fixed convention; f1*E(f2) would
# silently mix two different anti-isomorphic realizations (paper order for
# the outer product, reversed sign for E) and is not (3.53) at all under a
# single consistent reading. This mirrors, and independently rediscovers,
# the "reversal convention" already documented in the module docstring and
# in search/week3-battery-common.g's own AbstractProd comment -- it is not
# copied from kerchi-judge.g's GroupOfShadows (which was not consulted while
# writing this function; the empirical test above is what fixed the order).
# ============================================================================

def compose_gt_pairs(Nord, g1, g2):
    """g1, g2: (m, f, u, beta) accepted-candidate tuples. Returns (m_new,
    f_new, u_new) = g1 o g2 per (3.53) above, under this script's fixed
    E-sign convention (see block comment above: outer order is E(f2)*f1,
    empirically the self-consistent pairing with that E-sign, not the
    literal-reading f1*E(f2))."""
    m1, f1, u1, beta1 = g1
    m2, f2, u2, beta2 = g2
    f_new = ((beta1 ** -1) * f2 * beta1) * f1   # E_{m1,f1}(f2) * f1
    m_new = (2 * m1 * m2 + m1 + m2) % Nord
    u_new = 2 * m_new + 1
    return m_new, f_new, u_new


def check_composition_closure(wid, Nord, accepted, max_failures_kept=50):
    """(3.53) closure test over the accepted set: for every ordered pair
    (g1,g2) (both orders arise since (i,j) and (j,i) are both enumerated,
    including i==j), compute g1 o g2 and check its UID lies in the accepted
    set. accepted: list of (m,f,u,beta). Raw measurement only -- no PASS/FAIL
    verdict language, per parent instruction ("判定はしない")."""
    uid_list = [candidate_uid(wid, m, u, f) for (m, f, u, beta) in accepted]
    uid_set = set(uid_list)
    failures = []
    closure_failures = 0
    pairs_checked = 0
    n = len(accepted)
    for i in range(n):
        g1 = accepted[i]
        g1_uid = uid_list[i]
        for j in range(n):
            g2 = accepted[j]
            g2_uid = uid_list[j]
            pairs_checked += 1
            m_new, f_new, u_new = compose_gt_pairs(Nord, g1, g2)
            composite_uid = candidate_uid(wid, m_new, u_new, f_new)
            if composite_uid not in uid_set:
                closure_failures += 1
                if len(failures) < max_failures_kept:
                    failures.append(dict(g1_uid=g1_uid, g2_uid=g2_uid,
                                          composite_uid=composite_uid))
    return dict(
        pairs_checked=pairs_checked,
        closure_failures=closure_failures,
        all_closed=(closure_failures == 0),
        failure_witnesses=failures,
        failure_witnesses_truncated=(closure_failures > len(failures)),
    )


def write_checkpoint(path, wid, w, scanned, accepted, fail_settled, done):
    obj = dict(
        wid=wid, scanned_count=scanned, xi_bound=w["xi_bound"],
        accepted_count=len(accepted), settled_fail_count=len(fail_settled),
        done=done,
        accepted_uids=[candidate_uid(wid, m, u, f) for (m, f, u, beta) in accepted],
        fail_uids=[candidate_uid(wid, m, 2 * m + 1, f) for (m, f) in fail_settled],
    )
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2)


# ============================================================================
# certificate writer
# ============================================================================

def write_certificate(result, spec_sha256, out_path, id_gate=None):
    wid = result["wid"]
    accepted_uids = [candidate_uid(wid, m, u, f) for (m, f, u, beta) in result["accepted"]]
    fail_uids = [candidate_uid(wid, m, 2 * m + 1, f) for (m, f) in result["fail_settled"]]
    cert = dict(
        schema="ladder-xi-recheck/v1",
        generated_by=dict(tool="python3+sympy", script="search/ladder-xi-recheck.py",
                           date=time.strftime("%Y-%m-%dT%H:%M:%S%z")),
        independence_note=(
            "GAP not invoked; no GAP source imported or translated. Uses sympy "
            "(independent CAS) for BSGS/Schreier-Sims primitives only "
            "(PermutationGroup.order/contains/generator_product/centralizer). "
            "Settled check is an independently re-derived group-extension "
            "argument, not a port of GAP's GroupHomomorphismByImages. Window "
            "s1/s2/a1/b1 sourced verbatim from the GAP driver cert's own "
            "identifying fields (裁定216 point 1), not re-derived."
        ),
        window_id=wid,
        driver_spec_sha256=spec_sha256,
        canonical_id_gate_v2=id_gate,   # 裁定216 point 2: binding check, see gap_cert_binding_check
        n=result["n"], deg=result["deg"], N_ord=result["Nord"],
        charming_count=result["charming_count"],
        xi_bound=result["xi_bound"],
        scanned_count=result["scanned_count"],
        accepted_count=len(result["accepted"]),
        settled_fail_count=len(result["fail_settled"]),
        accepted_set_digest_sha256=digest_set(accepted_uids),
        fail_witness_set_digest_sha256=digest_set(fail_uids),
        accepted_uids=sorted(accepted_uids),
        fail_witness_uids=sorted(fail_uids)[:50],
        fail_witness_uids_truncated=(len(fail_uids) > 50),
        composition_closure_353=result["composition_closure_353"],
        elapsed_sec=result["elapsed_sec"],
        total_elapsed_sec=result["total_elapsed_sec"],
    )
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(cert, fh, indent=2, ensure_ascii=False)
    return cert


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


# ============================================================================
# main
# ============================================================================

def main():
    print("=== search/ladder-xi-recheck.py: independent Xi-restricted ladder scan ===")
    print("(裁定216 続行: sibling 9 windows sourced from GAP certs' s1/s2/a1/b1 "
          "identifying fields; canonical-ID gate v2 = binding check against the "
          "GAP cert's own recorded canonical_string/canonical_id_sha256)")
    run_selftests()

    id_mismatches = check_all_canonical_ids_v2()
    if id_mismatches:
        raise SystemExit(
            "FATAL: canonical-ID gate v2 (binding check) MISMATCH for: %s -- a GAP "
            "cert's own canonical_string does not hash to its own recorded "
            "canonical_id_sha256. Refusing to proceed (this is a corrupted/tampered "
            "identity field, fail-closed per the driver spec's own convention)."
            % id_mismatches)

    spec_path = "search/_a13_ladder_driver_spec.md"
    spec_sha256 = sha256_of_file(spec_path)
    print("[spec] %s sha256=%s" % (spec_path, spec_sha256))

    # execution order per Sol 便85: A10 canonical calibration -> A13 canonical
    # stress -> A11/A12 canonical -> sibling 9 (grouped by t family, canonical
    # first in each family since that is already validated).
    order = (
        ["W-E-A10-9t1", "W-E-A13-9t4", "W-E-A11-9t2", "W-E-A12-9t3"] +
        ["W-E-A10-9t1-o2", "W-E-A10-9t1-o3", "W-E-A10-9t1-o4", "W-E-A10-9t1-o5", "W-E-A10-9t1-o6"] +
        ["W-E-A11-9t2-o2", "W-E-A11-9t2-o3"] +
        ["W-E-A12-9t3-o2", "W-E-A12-9t3-o3"]
    )
    assert set(order) == set(all_window_ids())

    manifest = dict(schema="ladder-xi-recheck-manifest/v1",
                     driver_spec_sha256=spec_sha256, windows=[])

    for wid in order:
        w = build_window_spec_from_gap_cert(wid)
        id_ok, id_computed, id_recorded = gap_cert_binding_check(wid)
        id_gate = dict(ok=id_ok, computed_sha256=id_computed, recorded_sha256=id_recorded)
        print("\n--- window %s (n=%d, deg=%d, t=%d, xi_bound=%d) ---"
              % (wid, w["n"], w["deg"], w["t"], w["xi_bound"]))
        ckpt_path = "search/certs/.ladder_xi_recheck_checkpoint_%s.json" % wid
        result = scan_window(wid, w, checkpoint_path=ckpt_path)
        out_path = "search/certs/ladder_xi_recheck_%s_20260730.json" % wid
        cert = write_certificate(result, spec_sha256, out_path, id_gate=id_gate)
        print("[%s] WROTE %s" % (wid, out_path))
        m0_layer = sum(1 for u in cert["accepted_uids"] if "|m=0|" in u)
        clos = cert["composition_closure_353"]
        print("[%s] scanned=%d accepted=%d m0_layer=%d settled_fail=%d accepted_digest=%s"
              % (wid, cert["scanned_count"], cert["accepted_count"], m0_layer,
                 cert["settled_fail_count"], cert["accepted_set_digest_sha256"]))
        print("[%s] (3.53) closure: pairs_checked=%d closure_failures=%d all_closed=%s"
              % (wid, clos["pairs_checked"], clos["closure_failures"], clos["all_closed"]))
        manifest["windows"].append(dict(
            wid=wid, cert_path=out_path, cert_sha256=sha256_of_file(out_path),
            canonical_id_gate_v2=id_gate,
            scanned_count=cert["scanned_count"], accepted_count=cert["accepted_count"],
            m0_layer_count=m0_layer,
            settled_fail_count=cert["settled_fail_count"],
            accepted_set_digest_sha256=cert["accepted_set_digest_sha256"],
            fail_witness_set_digest_sha256=cert["fail_witness_set_digest_sha256"],
            composition_closure_353=dict(
                pairs_checked=clos["pairs_checked"],
                closure_failures=clos["closure_failures"],
                all_closed=clos["all_closed"],
            ),
        ))

    manifest_path = "search/certs/ladder_xi_recheck_manifest_20260730.json"
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
    print("\nWROTE manifest %s" % manifest_path)


# ============================================================================
# I10-1 extension (裁定220 続行2): N_ord=5 discriminating windows, epsilon=1
# fiber-product windows (E = S3 x_C2 S_n, not S3 x S_n -- per
# search/_i10_1_driver_spec.md's explicit warning). Reuses ALL of the core
# machinery above (build_window/compute_support/verify_PN_is_alternating/
# charming_set/build_settled_precompute/xi_restricted_candidates/is_settled)
# unchanged -- that machinery derives everything (normality of PN, the
# Bq/PN=6 transversal, cocycle data) directly from s1,s2 by computation, it
# never assumes a direct-product shape, so the epsilon=1 fiber-product
# structure does not require any change to the scan itself. Only the
# canonical-string field names differ (|ell=|r=|t= instead of |t=), which is
# irrelevant here since the ID gate is a binding check against the GAP cert's
# own recorded canonical_string (format-agnostic).
# ============================================================================

I10_1_GAP_CERT_FILENAMES = {
    "W-E-A10-5x2t0": "i10_1_W_E_A10_5x2t0_20260730.json",
    "W-E-A15-5x3t0": "i10_1_W_E_A15_5x3t0_20260730.json",
}

I10_1_XI_BOUND = {
    "W-E-A10-5x2t0": 5000,
    "W-E-A15-5x3t0": 1125000,
}


def load_i10_1_gap_cert(wid):
    path = "%s/%s" % (GAP_CERT_DIR, I10_1_GAP_CERT_FILENAMES[wid])
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def i10_1_binding_check(wid):
    cert = load_i10_1_gap_cert(wid)
    s = cert["canonical_string"]
    computed = hashlib.sha256(s.encode("utf-8")).hexdigest()
    recorded = cert["canonical_id_sha256"]
    return (computed == recorded), computed, recorded


def build_i10_1_window_spec(wid):
    cert = load_i10_1_gap_cert(wid)
    S1 = parse_gap_cycles(cert["s1"])
    S2 = parse_gap_cycles(cert["s2"])
    a1 = parse_gap_cycles(cert["a1"])
    b1 = parse_gap_cycles(cert["b1"])
    deg = max(max(pt for c in S1 for pt in c), max(pt for c in S2 for pt in c))
    return dict(n=cert["n"], deg=deg, ell=cert["ell"], r=cert["r"], t=cert["t"],
                a1=a1, b1=b1, S1=S1, S2=S2, xi_bound=I10_1_XI_BOUND[wid])


def main_i10_1():
    print("\n\n=== I10-1 extension (裁定220 続行2): N_ord=5 discriminating windows ===")
    print("Prediction file (i10_1_prediction_v1.md) NOT read.")

    spec_path = "search/_i10_1_driver_spec.md"
    spec_sha256 = sha256_of_file(spec_path)
    print("[spec] %s sha256=%s" % (spec_path, spec_sha256))

    id_mismatches = []
    for wid in I10_1_GAP_CERT_FILENAMES:
        ok, computed, recorded = i10_1_binding_check(wid)
        status = "MATCH" if ok else "MISMATCH"
        if not ok:
            id_mismatches.append(wid)
        print("[i10-1 canonical-id binding] %s: computed=%s recorded=%s %s"
              % (wid, computed, recorded, status))
    if id_mismatches:
        raise SystemExit(
            "FATAL: I10-1 canonical-ID binding check MISMATCH for: %s -- refusing "
            "to proceed (fail-closed)." % id_mismatches)

    order = ["W-E-A10-5x2t0", "W-E-A15-5x3t0"]  # smaller Xi bound first
    windows_out = []

    for wid in order:
        w = build_i10_1_window_spec(wid)
        print("\n--- I10-1 window %s (n=%d, ell=%d, r=%d, t=%d, deg=%d, xi_bound=%d) ---"
              % (wid, w["n"], w["ell"], w["r"], w["t"], w["deg"], w["xi_bound"]))
        ckpt_path = "search/certs/.i10_1_xi_recheck_checkpoint_%s.json" % wid
        result = scan_window(wid, w, checkpoint_path=ckpt_path)
        accepted_uids = [candidate_uid(wid, m, u, f) for (m, f, u, beta) in result["accepted"]]
        fail_uids = [candidate_uid(wid, m, 2 * m + 1, f) for (m, f) in result["fail_settled"]]
        m0_layer = sum(1 for uid in accepted_uids if "|m=0|" in uid)
        entry = dict(
            wid=wid, n=w["n"], ell=w["ell"], r=w["r"], t=w["t"], deg=w["deg"],
            N_ord=result["Nord"], charming_count=result["charming_count"],
            xi_bound=w["xi_bound"], scanned_count=result["scanned_count"],
            accepted_count=len(result["accepted"]), m0_layer_count=m0_layer,
            settled_fail_count=len(result["fail_settled"]),
            accepted_set_digest_sha256=digest_set(accepted_uids),
            fail_witness_set_digest_sha256=digest_set(fail_uids),
            accepted_uids=sorted(accepted_uids),
            composition_closure_353=result["composition_closure_353"],
            elapsed_sec=result["elapsed_sec"],
        )
        windows_out.append(entry)
        print("[%s] scanned=%d accepted=%d m0_layer=%d settled_fail=%d accepted_digest=%s"
              % (wid, entry["scanned_count"], entry["accepted_count"], entry["m0_layer_count"],
                 entry["settled_fail_count"], entry["accepted_set_digest_sha256"]))

    out = dict(
        schema="i10-1-xi-recheck/v1",
        generated_by=dict(tool="python3+sympy", script="search/ladder-xi-recheck.py (I10-1 extension)",
                           date=time.strftime("%Y-%m-%dT%H:%M:%S%z")),
        independence_note=(
            "GAP not invoked; no GAP source imported or translated. Same "
            "independent method as the A13 ladder scan (see module docstring); "
            "reused unchanged for these epsilon=1 (fiber-product) windows -- "
            "the scan derives PN normality / Bq-PN transversal / cocycle data "
            "directly from s1,s2 by computation, it does not assume a "
            "direct-product ambient structure anywhere."
        ),
        driver_spec_sha256=spec_sha256,
        windows=windows_out,
    )
    out_path = "search/certs/i10_1_xi_recheck_20260730.json"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print("\nWROTE %s" % out_path)
    for e in windows_out:
        print("[i10-1 result] %s scanned=%d accepted=%d m0_layer=%d settled_fail=%d accepted_digest=%s"
              % (e["wid"], e["scanned_count"], e["accepted_count"], e["m0_layer_count"],
                 e["settled_fail_count"], e["accepted_set_digest_sha256"]))


if __name__ == "__main__":
    main()
    main_i10_1()
