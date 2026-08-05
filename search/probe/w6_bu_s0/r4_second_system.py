#!/usr/bin/env python3
"""
search/probe/w6_bu_s0/r4_second_system.py -- ISO-GATE route-2 R4: independent
second enumerator/checker (docs/notes/w6_bottomup_design_v4.md sec.5.4).

v2 (commander 裁定535, following falsifier CV-9-2 reading
docs/notes/iso_r3r4_cv9_reading_v1.md and mathematician
auto_settled_check_v1.md addendum A): repairs 【重大2】(verdict was a 2-arg
function here vs GAP's 3-/4-arg ComputeVerdict; h10_fail was counted per-f
instead of per-(f,m) pair, so the GAP identity
candidate_total-h10-h11-genfail=shadow_total did not even type-check on this
side) and mirrors the v2 GAP driver's M-ISO-2 reconstruction (witness moved
from h11_fail bucket to shadow bucket, real settled-check call, independent
genuineness re-check) and M-ISO-8 (settled:=true fixed mutant).

v2.1 (commander 裁定543, following falsifier CV-9-2 re-reading
docs/notes/iso_r3r4_cv9_reading_v2.md -- cross-checked grading GRANTED,
conditional on this repair): 【要修正A】M-ISO-8's detection mechanism changed
from verdict-comparison (which falsifier machine-confirmed is INSENSITIVE to
the settled mutation on the M-ISO-2(v2) datum -- the NONSHADOW gate dominates
regardless of settled=12 or 13) to detail-element comparison (the witness's
settled flag, real vs mutant). 【要修正B】conventions_used rebuilt with
canonical enum/dict values (byte-identical to the GAP cert on the 5 required
keys: perm_composition, abstract_prod_reversal, word_eval,
h10_fail_bookkeeping_unit, comparison_target) and grading_prohibitions moved
inside conventions_used (軽微F, same path as GAP). 軽微E: staged counters
(candidate_total/h10_fail/h11_fail/generation_fail) now asserted against the
GAP-dumped expected values, not just self-printed.

Independence discipline (探索器と照合器の分離): this script does NOT import or
read any GAP source file (search/*.g) and does NOT call GAP. Its ONLY input is
search/probe/w6_bu_s0/r4_input_data.json, a plain data dump (permutation images of the
generators x,y on n points for each fixture, plus the GAP driver's claimed
summary numbers to diff against). All group theory below (permutation
multiplication, BFS closure/generation, derived subgroup via commutator
closure, hexagon (3.10)/(3.11) via an independently-verified theta/tau
construction with contradiction detection, settled-check via the same
technique, isolated verdict) is reimplemented from scratch in Python.

GAP convention note: GAP permutations act on the RIGHT (k^(p*q) = (k^p)^q),
so "p*q" means "apply p first, then q" -- our compose(p,q) matches this.
HOWEVER: the GAP side's helper AbstractProd(list) (search/week3-battery-common.g)
does NOT evaluate a list [a,b,c] as a*b*c in that direct order -- its own
docstring says it implements the PAPER's left-to-right notation "f1 f2 ... fk"
via a REVERSAL: AbstractProd([a,b,c]) actually computes c*b*a in GAP semantics
(apply c first, then b, then a). This was found and confirmed by direct GAP
probing (scratchpad/debug_witness3.g) while chasing a witness-verification
mismatch during R4 cross-checking: for AbstractProd([f^-1, Y^u, f]) the actual
GAP-computed permutation is f * Y^u * f^-1 (apply f first, then Y^u, then
f^-1), NOT f^-1 * Y^u * f as the paper notation naively suggests. All uses of
this specific product below are written with that REVERSAL already applied
(compose(compose(f, Y^u), finv)), matching what GAP's AbstractProd([f^-1,Y^u,f])
actually returns. (Aggregate counts -- shadow_total, settled_count -- happen
to be invariant under this reversal since D=[G,G] is closed under inverses, so
this bug was invisible until a SPECIFIC labeled witness was checked; see the
driver-side comment for the parallel bug found in word-evaluation.)
"""
import json
import sys
from itertools import product


def compose(p, q):
    """p then q, matching GAP's k^(p*q) = (k^p)^q (1-indexed tuples)."""
    return tuple(q[p[i] - 1] for i in range(len(p)))


def invert(p):
    n = len(p)
    inv = [0] * n
    for i in range(n):
        inv[p[i] - 1] = i + 1
    return tuple(inv)


def identity(n):
    return tuple(range(1, n + 1))


def power(p, k, n):
    if k == 0:
        return identity(n)
    if k < 0:
        return power(invert(p), -k, n)
    result = identity(n)
    base = p
    while k > 0:
        if k & 1:
            result = compose(result, base)
        base = compose(base, base)
        k >>= 1
    return result


def order(p, n):
    idn = identity(n)
    cur = p
    k = 1
    while cur != idn:
        cur = compose(cur, p)
        k += 1
        if k > 100000:
            raise RuntimeError("order() did not converge")
    return k


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


def bfs_closure(gens, n):
    """Standard orbit/closure BFS: all elements of <gens> as a set of tuples."""
    idn = identity(n)
    seen = {idn}
    queue = [idn]
    qi = 0
    while qi < len(queue):
        cur = queue[qi]
        qi += 1
        for g in gens:
            nv = compose(cur, g)
            if nv not in seen:
                seen.add(nv)
                queue.append(nv)
    return seen


def derived_subgroup(G_elements, n):
    """Commutator subgroup: subgroup generated by ALL commutators [g,h],
    g,h in G_elements. g^-1 h^-1 g h in GAP's Comm(g,h) convention; we just
    need SOME generating set of the derived subgroup, and "all commutators of
    all pairs" is a textbook-correct (if brute-force) choice, independent of
    GAP's DerivedSubgroup() algorithm."""
    commutators = set()
    G_list = list(G_elements)
    for g in G_list:
        ginv = invert(g)
        for h in G_list:
            hinv = invert(h)
            # [g,h] = g^-1 h^-1 g h  (standard commutator; any fixed convention
            # generates the same derived subgroup as long as applied to ALL pairs)
            comm = compose(compose(compose(ginv, hinv), g), h)
            commutators.add(comm)
    return bfs_closure(list(commutators), n)


def build_hom_with_check(G_elements, gens_domain, gens_image, n):
    """Independently construct a candidate endomorphism g -> phi(g) by BFS
    over the Cayley graph generated by gens_domain (each with its OWN image in
    gens_image, matched by index, both directions +1/-1), propagating images
    in lockstep, and DETECTING CONTRADICTIONS (same domain element reached via
    two paths with different images => map is NOT well-defined). This is a
    genuine, from-scratch verification, not an assumption.
    Returns (ok, phi_dict_or_reason).
    """
    idn = identity(n)
    phi = {idn: idn}
    queue = [idn]
    qi = 0
    # build the +1/-1 step list: each gens_domain[i] paired with gens_image[i]
    steps = []
    for gd, gi in zip(gens_domain, gens_image):
        steps.append((gd, gi))
        steps.append((invert(gd), invert(gi)))
    while qi < len(queue):
        cur = queue[qi]
        qi += 1
        cur_img = phi[cur]
        for gd, gi in steps:
            nv = compose(cur, gd)
            nv_img = compose(cur_img, gi)
            if nv in phi:
                if phi[nv] != nv_img:
                    return False, "CONTRADICTION: domain element reached with two different images"
            else:
                phi[nv] = nv_img
                queue.append(nv)
    if len(phi) != len(G_elements):
        return False, "INCOMPLETE: BFS from generators did not cover all of G"
    return True, phi


def compute_verdict(all_shadows_genuine, shadow_sum_ok, total_shadows, settled_count):
    """★ v2 (R-A): mirrors GAP's ComputeVerdict(allShadowsGenuine, shadowSumOk,
    totalShadows, settledCount) exactly -- a 4-argument function with the
    genuineness gate at highest priority, matching the v2 GAP driver
    (search/probe/w6_bu_s0/iso_gate_r3r4_driver.g). v1 of this file had NO
    such function (verdict was computed by an inline 2-arg expression with no
    sum-check gate at all) -- falsifier 【重大2】.
    """
    if not all_shadows_genuine:
        return {"verdict": "UNKNOWN", "reason": "NONSHADOW_IN_DATUM"}
    if not shadow_sum_ok:
        return {"verdict": "UNKNOWN", "reason": "CANDIDATE_ENUM_INCONSISTENT"}
    if total_shadows == 0:
        return {"verdict": "UNKNOWN", "reason": "NO_SHADOWS"}
    if settled_count == total_shadows:
        return {"verdict": "TRUE", "reason": ""}
    return {"verdict": "FALSE", "reason": ""}


def verify_shadows_genuine(G, X, Y, theta, tau, n_points, shadow_list):
    """Independent re-check that every (m, f, genA, genB) in shadow_list
    actually satisfies hex310/hex311/SURJ -- mirrors the GAP driver's
    VerifyShadowsGenuine. For a shadow_list built entirely from run_fixture's
    own `shadows` output this is trivially true; it only matters when a
    shadow list is hand-assembled (the M-ISO-2(v2) reconstruction below).
    """
    idn = identity(n_points)
    g_size = len(G)
    for (m, f, genA, genB) in shadow_list:
        thetaf = theta[f]
        if compose(thetaf, f) != idn:
            return False
        ym = power(Y, m, n_points)
        ymf = compose(f, ym)
        tau_ymf = tau[ymf]
        tau2_ymf = tau[tau_ymf]
        if compose(compose(ymf, tau_ymf), tau2_ymf) != idn:
            return False
        gensub = bfs_closure([genA, genB], n_points)
        if len(gensub) != g_size:
            return False
    return True


def run_fixture(name, n_points, x_img, y_img, expected):
    print(f"=== {name} ===")
    X = tuple(x_img)
    Y = tuple(y_img)
    idn = identity(n_points)

    # 1. independently enumerate G = <X,Y> via BFS closure
    G = bfs_closure([X, Y], n_points)
    g_size = len(G)
    print(f"  |G| (independent BFS closure) = {g_size}  (GAP claims {expected['expected_g_size']})")
    assert g_size == expected['expected_g_size'], "G size mismatch vs GAP claim"

    # 2. N_ord, charming set (independent: order() via repeated squaring/BFS)
    ordX = order(X, n_points)
    ordY = order(Y, n_points)
    nOrd = lcm(ordX, ordY)
    print(f"  ord(X)={ordX} ord(Y)={ordY} N_ord={nOrd}  (GAP claims {expected['expected_n_ord']})")
    assert nOrd == expected['expected_n_ord'], "N_ord mismatch vs GAP claim"
    charming = [m for m in range(nOrd) if gcd(2 * m + 1, nOrd) == 1]

    # 3. derived subgroup D = [G,G], independent commutator-closure computation
    D = derived_subgroup(G, n_points)
    print(f"  |D|=|[G,G]| (independent commutator closure) = {len(D)}")

    # 4. theta (x->y,y->x) and tau (x->y,y->z=(xy)^-1) via independent
    #    BFS-with-contradiction-detection construction (genuine verification,
    #    not assumed)
    # z := AbstractProd([X,Y])^-1; AbstractProd([X,Y]) reverses to compose(Y,X) -- see module docstring
    z = invert(compose(Y, X))
    theta_ok, theta = build_hom_with_check(G, [X, Y], [Y, X], n_points)
    tau_ok, tau = build_hom_with_check(G, [X, Y], [Y, z], n_points)
    print(f"  theta well-defined (independent BFS check): {theta_ok}")
    print(f"  tau well-defined (independent BFS check): {tau_ok}")
    if not (theta_ok and tau_ok):
        print("  theta/tau not well-defined -- cannot proceed with hexagon enumeration (matches GAP's THETA_TAU_NOT_WELLDEFINED branch)")
        return {"name": name, "theta_tau_ok": False}

    # 5. hexagon (3.10)/(3.11) + generation(SURJ), independently, over D x charming.
    #    ★ v2 (R-A): h10_fail is now counted PER (f,m) PAIR -- matching the GAP
    #    side's actual loop structure exactly (EnumerateReducedHexagon checks
    #    hex310 INSIDE the "for m in charmingSet do" loop, even though hex310
    #    does not depend on m, so a failing f contributes len(charming) to
    #    h10_fail, not 1). v1 counted h10_fail once per f (a DIFFERENT
    #    bookkeeping unit), so the identity
    #    candidate_total - h10 - h11 - genfail = shadow_total
    #    did not hold on the Python side at all (falsifier 【重大2】). It holds
    #    on both sides now.
    candidate_total = len(D) * len(charming)
    shadow_total = 0
    h10_fail = 0
    h11_fail = 0
    generation_fail = 0
    shadows = []
    for f in D:
        thetaf = theta[f]
        # AbstractProd([f, thetaf]) reverses to compose(thetaf, f) -- see module docstring
        hex310 = compose(thetaf, f) == idn
        for m in charming:
            if not hex310:
                h10_fail += 1
                continue
            u = 2 * m + 1
            ym = power(Y, m, n_points)
            # AbstractProd([y^m, f]) reverses to compose(f, y^m) -- see module docstring
            ymf = compose(f, ym)
            tau_ymf = tau[ymf]
            tau2_ymf = tau[tau_ymf]
            # AbstractProd([tau2ymf, tauymf, ymf]) reverses to compose(compose(ymf, tau_ymf), tau2_ymf)
            hex311 = compose(compose(ymf, tau_ymf), tau2_ymf) == idn
            if not hex311:
                h11_fail += 1
                continue
            genA = power(X, u, n_points)
            finv = invert(f)
            # AbstractProd([finv, Y^u, f]) reverses to compose(compose(f, Y^u), finv)
            genB = compose(compose(f, power(Y, u, n_points)), finv)
            gensub = bfs_closure([genA, genB], n_points)
            if len(gensub) != g_size:
                generation_fail += 1
                continue
            shadow_total += 1
            shadows.append((m, f, genA, genB))

    shadow_sum_check = (candidate_total - h10_fail - h11_fail - generation_fail == shadow_total)
    print(f"  candidate_total(|D|x|charming|)={candidate_total}  h10_fail(f,m pairs)={h10_fail} "
          f"h11_fail(f,m pairs)={h11_fail} generation_fail(f,m pairs)={generation_fail} shadow_total={shadow_total}")
    print(f"  shadow_sum_check: {candidate_total}-{h10_fail}-{h11_fail}-{generation_fail}={candidate_total - h10_fail - h11_fail - generation_fail} =?= {shadow_total} -> {shadow_sum_check}")
    print(f"  (GAP claims shadow_total={expected['expected_shadow_total']})")
    assert shadow_total == expected['expected_shadow_total'], "shadow_total mismatch vs GAP claim"
    assert shadow_sum_check, "shadow_sum_check identity does not hold on the Python side"
    # ★ v2.1 【軽微E】: staged counters were only self-printed in v2, not
    # asserted against the GAP-dumped values -- assert them now.
    assert candidate_total == expected['expected_candidate_total'], "candidate_total mismatch vs GAP claim"
    assert h10_fail == expected['expected_h10_fail'], "h10_fail mismatch vs GAP claim"
    assert h11_fail == expected['expected_h11_fail'], "h11_fail mismatch vs GAP claim"
    assert generation_fail == expected['expected_generation_fail'], "generation_fail mismatch vs GAP claim"

    # 6. settled check: independently build T_{m,f} via the same BFS-with-
    #    contradiction-detection technique, check well-defined AND surjective
    #    (=> bijective on the finite set G, by the pigeonhole argument)
    settled_count = 0
    settled_detail = []
    for (m, f, genA, genB) in shadows:
        ok, phi = build_hom_with_check(G, [X, Y], [genA, genB], n_points)
        settled = False
        if ok:
            image = set(phi.values())
            settled = (len(image) == g_size)  # surjective on finite G => bijective
        if settled:
            settled_count += 1
        settled_detail.append({"m": m, "f": f, "settled": settled})
    print(f"  settled (independent) = {settled_count}/{shadow_total}  (GAP claims {expected['expected_settled_count']}/{expected['expected_settled_total']})")
    assert settled_count == expected['expected_settled_count'], "settled_count mismatch vs GAP claim"
    assert shadow_total == expected['expected_settled_total'], "settled_total mismatch vs GAP claim"

    all_genuine = True  # trivially true here: every element of `shadows` passed hex310/hex311/SURJ by construction
    verdict_rec = compute_verdict(all_genuine, shadow_sum_check, shadow_total, settled_count)
    print(f"  independent verdict = {verdict_rec['verdict']}  (GAP claims {expected['expected_verdict']})")
    assert verdict_rec['verdict'] == expected['expected_verdict'], "verdict mismatch vs GAP claim"
    print(f"  [MATCH] {name}: independent second system agrees with GAP driver on all summary numbers\n")
    return {"name": name, "theta_tau_ok": True, "g_size": g_size, "n_ord": nOrd,
            "candidate_total": candidate_total, "h10_fail": h10_fail, "h11_fail": h11_fail,
            "generation_fail": generation_fail, "shadow_total": shadow_total,
            "shadow_sum_check": shadow_sum_check, "settled_count": settled_count,
            "settled_detail": settled_detail, "shadows": shadows,
            "verdict": verdict_rec['verdict'], "match_gap": True,
            "G": G, "D": D, "X": X, "Y": Y, "theta": theta, "tau": tau}


def check_m_iso2_v2(k3_result, witness, n_points):
    """★ v2: mirrors the GAP driver's M-ISO-2(v2) reconstruction exactly --
    move the witness from the h11_fail bucket to the shadow bucket (real data,
    not a scalar), run the real settled-check on the 13-element list, and
    independently re-verify genuineness. Uses the GAP driver's raw f_images
    dump for the witness (NOT f_word -- word evaluation is convention-fragile,
    see module docstring and the driver-side comment near FindH11FailWitness).
    """
    print("=== M-ISO-2(v2) reconstruction (independent second system) ===")
    G, X, Y, theta, tau = k3_result["G"], k3_result["X"], k3_result["Y"], k3_result["theta"], k3_result["tau"]
    g_size = k3_result["g_size"]
    m = witness['m']
    u = 2 * m + 1
    f = tuple(witness['f_images'])
    genA = power(X, u, n_points)
    finv = invert(f)
    # AbstractProd([finv, Y^u, f]) reverses to compose(compose(f, Y^u), finv) -- see module docstring
    genB = compose(compose(f, power(Y, u, n_points)), finv)
    subgroup = bfs_closure([genA, genB], n_points)
    print(f"  witness m={m} f_word={witness['f_word']} stage={witness.get('stage')}")
    print(f"  independent |<genA,genB>| = {len(subgroup)}  (GAP claims {witness['expected_subgroup_size']}, |G|={g_size})")
    assert len(subgroup) == witness['expected_subgroup_size'], "witness subgroup size mismatch"
    is_proper = len(subgroup) < g_size
    assert is_proper == witness['expected_subgroup_size_lt_g'], "witness proper-subgroup mismatch"

    recon = witness  # the driver dumps m_iso2_v2_reconstruction as a sibling; caller passes it in via `witness` param merge -- see main()
    v2 = recon['_v2_reconstruction']

    # ★ real path: move witness from h11_fail into the shadow list (not a scalar)
    mIso2_shadows = list(k3_result["shadows"]) + [(m, f, genA, genB)]
    mIso2_h11_fail = k3_result["h11_fail"] - 1
    mIso2_shadow_total = k3_result["shadow_total"] + 1
    mIso2_shadow_sum_ok = (k3_result["candidate_total"] - k3_result["h10_fail"] - mIso2_h11_fail
                           - k3_result["generation_fail"] == mIso2_shadow_total)
    mIso2_all_genuine = verify_shadows_genuine(G, X, Y, theta, tau, n_points, mIso2_shadows)

    # real settled-check on the FULL 13-element list (real call, not hand-computed)
    mIso2_settled_count = 0
    witness_settled = None
    for (mm, ff, ga, gb) in mIso2_shadows:
        ok, phi = build_hom_with_check(G, [X, Y], [ga, gb], n_points)
        settled = ok and (len(set(phi.values())) == g_size)
        if settled:
            mIso2_settled_count += 1
        if ff == f and mm == m:
            witness_settled = settled

    mIso2_verdict = compute_verdict(mIso2_all_genuine, mIso2_shadow_sum_ok, mIso2_shadow_total, mIso2_settled_count)

    print(f"  h11_fail {k3_result['h11_fail']}->{mIso2_h11_fail}  shadow_total {k3_result['shadow_total']}->{mIso2_shadow_total}  "
          f"identity holds={mIso2_shadow_sum_ok}")
    print(f"  settled (real path) = {mIso2_settled_count}/{mIso2_shadow_total}  witness_settled={witness_settled} (expect False)")
    print(f"  all_shadows_genuine (independent) = {mIso2_all_genuine} (expect False)")
    print(f"  verdict = {mIso2_verdict['verdict']}/{mIso2_verdict['reason']}  (GAP v2 expects {v2['expected_verdict']}/{v2['expected_unknown_reason']})")

    assert mIso2_h11_fail == v2['expected_h11_fail'], "h11_fail mismatch vs GAP v2 claim"
    assert mIso2_shadow_total == v2['expected_shadow_total'], "shadow_total mismatch vs GAP v2 claim"
    assert mIso2_shadow_sum_ok == v2['expected_shadow_sum_check'], "shadow_sum_check mismatch vs GAP v2 claim"
    assert mIso2_settled_count == v2['expected_settled_count'], "settled_count mismatch vs GAP v2 claim"
    assert mIso2_shadow_total == v2['expected_settled_total'], "settled_total mismatch vs GAP v2 claim"
    assert witness_settled == v2['expected_witness_settled'], "witness settled-flag mismatch vs GAP v2 claim"
    assert mIso2_all_genuine == v2['expected_all_shadows_genuine'], "all_shadows_genuine mismatch vs GAP v2 claim"
    assert mIso2_verdict['verdict'] == v2['expected_verdict'], "M-ISO-2(v2) verdict mismatch vs GAP v2 claim"
    assert mIso2_verdict['reason'] == v2['expected_unknown_reason'], "M-ISO-2(v2) reason mismatch vs GAP v2 claim"
    print("  [MATCH] R4 second system independently confirms the GAP v2 M-ISO-2 reconstruction "
          "(NOT an isolated=FALSE claim -- see driver's m_iso2_construction_note)\n")

    return {
        "witness_subgroup_size": len(subgroup), "witness_proper_subgroup_independent": is_proper,
        "mIso2_shadows": mIso2_shadows, "mIso2_h11_fail": mIso2_h11_fail,
        "mIso2_shadow_total": mIso2_shadow_total, "mIso2_shadow_sum_ok": mIso2_shadow_sum_ok,
        "mIso2_all_genuine": mIso2_all_genuine, "mIso2_settled_count": mIso2_settled_count,
        "witness_settled": witness_settled, "verdict": mIso2_verdict["verdict"],
        "reason": mIso2_verdict["reason"],
    }


def check_m_iso8(k3_result, mIso2_result, n_points):
    """★ v2.1 【要修正A】fix (mirrors the GAP driver's corrected M-ISO-8):
    settled:=true fixed mutant, applied to the SAME 13-element M-ISO-2(v2)
    datum. falsifier machine-confirmed the VERDICT is insensitive to this
    mutation on this datum (NONSHADOW_IN_DATUM fires regardless of
    settled_count=12 or 13, since the genuineness gate dominates) -- so
    detection must strike the settled CHANNEL directly via detail-element
    comparison, not a verdict comparison (that was v2's bug, effectively
    duplicating M-ISO-3).
    """
    print("=== M-ISO-8 (independent second system, v2.1 detail-comparison fix) ===")
    shadows13 = mIso2_result["mIso2_shadows"]
    mutant_settled_count = len(shadows13)  # settled:=true for every element, including the witness
    mutant_total = len(shadows13)
    real_witness_settled = mIso2_result["witness_settled"]  # False, from the real SettledCheckGeneral path
    mutant_witness_settled = True  # MutantSettledAlwaysTrue always reports True
    detected = (real_witness_settled != mutant_witness_settled)
    print(f"  mutant settled_count={mutant_settled_count}/{mutant_total}  "
          f"real witness_settled={real_witness_settled}  mutant witness_settled={mutant_witness_settled}  "
          f"mismatch (settled channel struck directly)={detected}")
    # sanity: verdict really is insensitive here (documents the falsifier finding, not the detection itself)
    real_verdict = compute_verdict(mIso2_result["mIso2_all_genuine"], mIso2_result["mIso2_shadow_sum_ok"],
                                    mutant_total, mutant_settled_count)
    mutant_verdict_matches_real = (real_verdict["verdict"] == mIso2_result["verdict"] == "UNKNOWN"
                                    and real_verdict["reason"] == mIso2_result["reason"] == "NONSHADOW_IN_DATUM")
    print(f"  (verdict insensitivity check: mutant-settled verdict == real verdict == "
          f"UNKNOWN/NONSHADOW_IN_DATUM regardless of settled count? {mutant_verdict_matches_real} -- "
          f"confirms the kill is NOT visible at the verdict level, per falsifier)")
    assert detected, "M-ISO-8: settled:=true mutant was NOT detected at the detail-element level"
    assert real_witness_settled is False and mutant_witness_settled is True, "M-ISO-8 detail shape mismatch"
    assert mIso2_result["mIso2_settled_count"] == 12 and mutant_settled_count == 13, "M-ISO-8 settled_count shape mismatch"
    print("  [MATCH] R4 second system independently confirms M-ISO-8 is killed via detail-element "
          "comparison (real witness_settled=False vs mutant witness_settled=True), NOT via verdict comparison\n")
    return {"real_witness_settled": real_witness_settled, "mutant_witness_settled": mutant_witness_settled,
            "detected": detected, "verdict_insensitive_to_mutation": mutant_verdict_matches_real}


def summary_of(result):
    """Strip non-JSON-serializable internal fields (G/D as sets of tuples,
    theta/tau as dicts with tuple keys, shadows/settled_detail as tuples)
    before writing the output cert -- keep only summary scalars."""
    keys = ["name", "theta_tau_ok", "g_size", "n_ord", "candidate_total", "h10_fail",
            "h11_fail", "generation_fail", "shadow_total", "shadow_sum_check",
            "settled_count", "verdict", "match_gap"]
    return {k: result[k] for k in keys if k in result}


def main():
    with open("search/probe/w6_bu_s0/r4_input_data.json", encoding="utf-8") as f:
        data = json.load(f)

    results = {}
    results['k3'] = run_fixture("K^(3)", data['k3']['n_points'], data['k3']['x_images'],
                                 data['k3']['y_images'], data['k3'])
    results['w5'] = run_fixture("W-5", data['w5']['n_points'], data['w5']['x_images'],
                                 data['w5']['y_images'], data['w5'])

    witness = dict(data['m_iso2_witness'])
    witness['_v2_reconstruction'] = data['m_iso2_v2_reconstruction']
    mIso2_result = check_m_iso2_v2(results['k3'], witness, data['m_iso2_witness']['n_points'])
    mIso8_result = check_m_iso8(results['k3'], mIso2_result, data['m_iso2_witness']['n_points'])

    print("ALL R4 CROSS-CHECKS PASSED (v2): independent Python second system agrees with the GAP driver "
          "(search/probe/w6_bu_s0/iso_gate_r3r4_driver.g) on K^(3), W-5, M-ISO-2(v2), and M-ISO-8.")

    # ★ v2.1【要修正B】: canonical conventions_used, byte-identical to the GAP
    # cert on the 5 required keys (perm_composition, abstract_prod_reversal,
    # word_eval, h10_fail_bookkeeping_unit, comparison_target) -- enum/dict
    # values, prose moved to *_note siblings. grading_prohibitions moved
    # inside conventions_used (軽微F, same path as GAP's cert).
    CANON_GRADING_PROHIBITION = ("PERMANENT BAN (commander ruling 535/543, falsifier finding): never write "
                                 "that numeric agreement between two implementations demonstrates convention "
                                 "identity. Any same-object verdict must rest on source-reading (CV-9 judge), "
                                 "never on a cert's own numeric match.")
    conventions_used = {
        "ledger_version": "conventions_ledger_v1_6",
        "perm_composition": "gap_native_right",
        "perm_composition_note": "GAP permutations act on the right: i^(p*q)=(i^p)^q. Python's compose(p,q) implements the same convention.",
        "abstract_prod_reversal": {
            "reversed": True,
            "rule": "AbstractProd([a1,...,ak]) = ak*a(k-1)*...*a1",
            "usages": [
                {"site": "z", "formula": "AbstractProd([x,y])^-1 = (y*x)^-1"},
                {"site": "hex310", "formula": "AbstractProd([f,thetaf])=1 <=> thetaf*f=1"},
                {"site": "ymf", "formula": "AbstractProd([y^m,f]) = f*y^m"},
                {"site": "hex311", "formula": "AbstractProd([tau2,tau1,ymf])=1 <=> ymf*tau1*tau2=1"},
                {"site": "genB", "formula": "AbstractProd([f^-1,y^u,f]) = f*y^u*f^-1"},
            ],
        },
        "abstract_prod_reversal_note": "confirmed by direct GAP probe and independently by falsifier's third implementation (docs/notes/iso_r3r4_cv9_reading_v1.md sec.2.1)",
        "word_eval": [
            {"layer": "BFSWords_storage", "direction": "prepend", "word_source": "internal_gap"},
            {"layer": "witness_reconstruction", "direction": "prepend", "word_source": "internal_gap"},
        ],
        "word_eval_note": "BFSWords storage is prepend (裁定166); witness reconstruction must use EvalWordInQ (prepend), NOT EvalWordQT (natural), which reconstructs a different element for the same word. Python side bypasses word evaluation entirely via raw f_images but declares the same layer/direction/word_source shape for machine-diffability.",
        "enumeration_domain": "group_elements",
        "group_side": "P_PB3_mod_N",
        "h10_fail_bookkeeping_unit": "per_fm_pair",
        "h10_fail_bookkeeping_unit_note": "theta/tau precondition (hex310) is checked inside the m-loop, redundantly per m, matching the GAP loop structure in EnumerateReducedHexagon exactly; NOT per-f.",
        "comparison_target": {
            "as_function_of": "marked_datum",
            "function_a": {"name": "IsoGateCheck_ComputeVerdict_GAP", "domain": "marked_datum_to_5_quantities"},
            "function_b": {"name": "run_fixture_compute_verdict_python", "domain": "marked_datum_to_5_quantities"},
            "normalization_digest": "n/a",
        },
        "comparison_target_note": "5 quantities = g_size, n_ord, shadow_total, settled_count/total, verdict per docs/notes/iso_r3r4_iffirst_freeze_v1.md sec.2",
        "grading_prohibitions": [CANON_GRADING_PROHIBITION],
        "grading_prohibitions_note": ("falsifier's third independent implementation showed the compared 5 "
                                       "quantities (|G|, N_ord, shadow_total, settled_count/total) are "
                                       "IDENTICAL whether AbstractProd is evaluated with the real reversal or "
                                       "with the naive (unreversed) paper-order convention -- i.e. this "
                                       "observation window has ZERO discriminating power for convention "
                                       "identity (docs/notes/iso_r3r4_cv9_reading_v1.md sec.3 【重大1】)."),
        "level": "PB3",
    }

    out = {
        "schema": "gtsh-cert/iso-gate-r4-second-system/v2.1",
        "generated_by": {"tool": "python3 (independent, no GAP)", "script": "search/probe/w6_bu_s0/r4_second_system.py"},
        "independence_declaration": "does not import/read any search/*.g file or call GAP; only input is search/probe/w6_bu_s0/r4_input_data.json (raw generator permutation images + GAP's claimed summary numbers to diff against); all group theory (BFS closure, derived subgroup via commutator closure, theta/tau construction with contradiction detection, hexagon, generation/SURJ, settled-check, ComputeVerdict, VerifyShadowsGenuine) reimplemented from scratch in Python",
        "conventions_used": conventions_used,
        "k3": summary_of(results['k3']),
        "w5": summary_of(results['w5']),
        "m_iso2_v2_independent_check": {
            "witness_subgroup_size": mIso2_result["witness_subgroup_size"],
            "witness_proper_subgroup_independent": mIso2_result["witness_proper_subgroup_independent"],
            "h11_fail_24_to": mIso2_result["mIso2_h11_fail"],
            "shadow_total_12_to": mIso2_result["mIso2_shadow_total"],
            "shadow_sum_check": mIso2_result["mIso2_shadow_sum_ok"],
            "all_shadows_genuine": mIso2_result["mIso2_all_genuine"],
            "settled_count": mIso2_result["mIso2_settled_count"],
            "witness_settled": mIso2_result["witness_settled"],
            "verdict": mIso2_result["verdict"],
            "reason": mIso2_result["reason"],
        },
        "m_iso8_independent_check": {
            "detection_mechanism": "detail-element comparison (v2.1 fix, NOT verdict comparison)",
            "real_witness_settled": mIso8_result["real_witness_settled"],
            "mutant_witness_settled": mIso8_result["mutant_witness_settled"],
            "detected": mIso8_result["detected"],
            "verdict_insensitive_to_mutation_confirmed": mIso8_result["verdict_insensitive_to_mutation"],
        },
        "all_crosschecks_pass": True,
    }
    with open("search/probe/w6_bu_s0/r4_second_system_output_v2_1.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print("\nwrote search/probe/w6_bu_s0/r4_second_system_output_v2_1.json")


if __name__ == "__main__":
    main()
