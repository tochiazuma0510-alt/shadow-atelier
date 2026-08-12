"""
crosscheck/check_s4_settled54.py -- independent crosscheck for search/certs/s4_settled54_v2_20260812.json
(S4-SETTLED-54, 裁定889/891/892).

Search/crosscheck separation: this file does NOT import search/*.g or any GAP output beyond the
final JSON cert (raw m/f_word/witness data). All group theory below (GF(8) arithmetic, P^1(GF8)
permutation action, PSL(2,8)/PGammaL(2,8) construction, BFS closure, homomorphism well-definedness
test, kernel computation, automorphism-witness search) is a FROM-SCRATCH Python re-implementation,
independent of search/week3-psl-common.g / week3-battery-common.g.

Method for the PRIMARY kernel-equality re-check (independent of GAP's GroupHomomorphismByImages):
for each shadow, build F:Gg->Gg by (1) BFS-closing Gg from X,Y with a canonical word per element,
(2) defining F(g) := substitute X->A, Y->B into g's canonical word and evaluate, (3) TESTING
F(g*X)=F(g)*A and F(g*Y)=F(g)*B for EVERY g in Gg (this is both necessary and sufficient for F to be
a well-defined homomorphism, by induction on generator words -- see file docstring below in
_is_homomorphism_well_defined). Kernel = {g : F(g)=identity}; kernel_trivial = (len(kernel)==1).

No "cross-checked"/"verified" language is asserted by this file beyond raw agree/disagree booleans.
"""
import json
import sys
from itertools import product

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CERT_PATH = "search/certs/s4_settled54_v2_20260812.json"

FAILS = []


def fail(msg):
    FAILS.append(msg)
    print("[FAIL]", msg)


def ok(msg):
    print("[OK]", msg)


# ================= GF(8) = F2[x]/(x^3+x+1), independent bit-based implementation =================
def gf8_add(a, b):
    return a ^ b


def gf8_mul(a, b):
    # carryless multiply then reduce mod x^3+x+1 (0b1011), independent from-scratch implementation
    result = 0
    aa = a
    for i in range(3):
        if (b >> i) & 1:
            result ^= aa << i
    # reduce degree-<=4 result mod x^3+x+1
    for i in (4, 3):
        if (result >> i) & 1:
            result ^= 0b1011 << (i - 3)
    return result & 0x7


def gf8_inv(a):
    if a == 0:
        raise ValueError("no inverse of 0")
    for b in range(1, 8):
        if gf8_mul(a, b) == 1:
            return b
    raise ValueError("not found")


def gf8_self_check():
    x = 2
    x2 = gf8_mul(x, x)
    x3 = gf8_mul(x2, x)
    assert x2 == 4, x2
    assert x3 == gf8_add(x, 1), x3


gf8_self_check()
ok("GF(8) self-check: x^2=4, x^3=x+1 (independent bit arithmetic)")

# ================= P^1(GF8): 9 points, index 0=infinity, 1+v for v in 0..7 =================
NPTS = 9


def mat_to_perm(M):
    a, b, c, d = M[0][0], M[0][1], M[1][0], M[1][1]
    images = [None] * NPTS
    images[0] = 0 if c == 0 else 1 + gf8_mul(a, gf8_inv(c))
    for v in range(8):
        num = gf8_add(gf8_mul(a, v), b)
        den = gf8_add(gf8_mul(c, v), d)
        images[1 + v] = 0 if den == 0 else 1 + gf8_mul(num, gf8_inv(den))
    return tuple(images)


def perm_mul(p, q):
    # (p then q): result[i] = q[p[i]]  (matches GAP's x^(p*q)=(x^p)^q convention used consistently
    # throughout this file -- internal consistency is what matters for an independent re-derivation)
    return tuple(q[p[i]] for i in range(NPTS))


def perm_inv(p):
    inv = [0] * NPTS
    for i, pi in enumerate(p):
        inv[pi] = i
    return tuple(inv)


IDENT = tuple(range(NPTS))


def perm_pow(p, n):
    if n == 0:
        return IDENT
    if n < 0:
        return perm_pow(perm_inv(p), -n)
    result = IDENT
    base = p
    while n:
        if n & 1:
            result = perm_mul(result, base)
        base = perm_mul(base, base)
        n >>= 1
    return result


def det2(M):
    return gf8_add(gf8_mul(M[0][0], M[1][1]), gf8_mul(M[0][1], M[1][0]))


def build_pgl8():
    seen = set()
    elts = []
    for a, b, c, d in product(range(8), repeat=4):
        M = ((a, b), (c, d))
        if det2(M) == 0:
            continue
        # canonicalize by first nonzero entry
        flat = [a, b, c, d]
        first = next(x for x in flat if x != 0)
        inv = gf8_inv(first)
        canon = tuple(gf8_mul(x, inv) for x in flat)
        if canon in seen:
            continue
        seen.add(canon)
        M2 = ((canon[0], canon[1]), (canon[2], canon[3]))
        elts.append(mat_to_perm(M2))
    return elts


def frob_perm():
    images = [0]
    for v in range(8):
        images.append(1 + gf8_mul(v, v))
    return tuple(images)


pgl_elts = build_pgl8()
assert len(pgl_elts) == 504, len(pgl_elts)
ok(f"PGL(2,8) independently enumerated: {len(pgl_elts)} elements (expect 504)")

frob = frob_perm()


def group_closure(gens):
    seen = {IDENT}
    queue = [IDENT]
    while queue:
        cur = queue.pop()
        for g in gens:
            nv = perm_mul(cur, g)
            if nv not in seen:
                seen.add(nv)
                queue.append(nv)
    return seen


aut_elts = group_closure(pgl_elts + [frob])
assert len(aut_elts) == 1512, len(aut_elts)
ok(f"PGammaL(2,8) independently enumerated: {len(aut_elts)} elements (expect 1512)")

# ================= S, T marking (same spec-given matrices as the GAP driver -- independent build) =================
Smat = ((1, 0), (1, 1))
Tmat = ((4, 3), (1, 5))
S = mat_to_perm(Smat)
T = mat_to_perm(Tmat)
assert perm_pow(S, 2) == IDENT, "S^2 != 1"
assert perm_pow(T, 3) == IDENT, "T^3 != 1"
ok("ord(S)=2, ord(T)=3 (independent recompute)")

point2_c_in_n_independent = (perm_pow(S, 2) == IDENT)

w = perm_mul(S, perm_inv(T))
X = perm_pow(w, 2)
Y = perm_mul(perm_mul(perm_inv(S), X), S)

eOrd = 1
p = w
while p != IDENT:
    p = perm_mul(p, w)
    eOrd += 1
kOrd = 1
p = X
while p != IDENT:
    p = perm_mul(p, X)
    kOrd += 1
print(f"[INFO] independent ord(w)={eOrd} (expect 9), ord(X)={kOrd} (expect 9)")
if eOrd != 9 or kOrd != 9:
    fail(f"ord(w)/ord(X) mismatch: {eOrd}/{kOrd}")

Gg = group_closure([X, Y])
assert len(Gg) == 504, len(Gg)
ok(f"Gg=<X,Y> independently enumerated: {len(Gg)} elements (expect 504)")

nOrd = kOrd
charming_set_independent = sorted(m for m in range(nOrd) if __import__("math").gcd(2 * m + 1, nOrd) == 1)
print(f"[INFO] independent charming_set = {charming_set_independent}")


# ================= BFS canonical word for every element of Gg (own construction) =================
def bfs_words(gens_dict):
    # gens_dict: {"x":X_perm, "y":Y_perm}; returns {perm: word} with word = list of (letter, +-1)
    word_of = {IDENT: []}
    queue = [IDENT]
    letters = [("x", 1, gens_dict["x"]), ("x", -1, perm_inv(gens_dict["x"])),
               ("y", 1, gens_dict["y"]), ("y", -1, perm_inv(gens_dict["y"]))]
    while queue:
        cur = queue.pop(0)
        cur_word = word_of[cur]
        for sym, pw, gperm in letters:
            nv = perm_mul(gperm, cur)  # matches GAP's BFSWords "nv := g.gap*cur" (prepend)
            if nv not in word_of:
                word_of[nv] = cur_word + [(sym, pw)]
                queue.append(nv)
    return word_of


word_of_Gg = bfs_words({"x": X, "y": Y})
assert len(word_of_Gg) == 504, len(word_of_Gg)


def eval_word(word, xg, yg):
    val = IDENT
    for sym, pw in word:
        letter = perm_pow(xg, pw) if sym == "x" else perm_pow(yg, pw)
        val = perm_mul(letter, val)  # prepend, matching BFSWords' construction rule
    return val


def reconstruct_f(f_word):
    return eval_word(f_word, X, Y)


def is_homomorphism_well_defined_and_kernel(A, B):
    """
    Build F(g) for all g in Gg via canonical BFS word substitution (X->A, Y->B), then test
    F(g*X)=F(g)*A and F(g*Y)=F(g)*B for EVERY g in Gg. If both hold for all g, F is a genuine
    well-defined homomorphism (standard induction: holds on generator-words by construction of F
    itself; this test additionally confirms F respects EVERY relation true in Gg between X,Y,
    since every element of Gg is reachable from every other by right-multiplication by X^-1,Y^-1
    starting from the BFS tree root, and the test checks consistency along ALL such edges, not just
    the tree edges used to define F). Returns (well_defined: bool, kernel_size: int, F: dict).
    """
    F = {}
    for g, w in word_of_Gg.items():
        F[g] = eval_word(w, A, B)
    well_defined = True
    for g in Gg:
        gx = perm_mul(X, g)
        gy = perm_mul(Y, g)
        if F.get(gx) != perm_mul(A, F[g]):
            well_defined = False
        if F.get(gy) != perm_mul(B, F[g]):
            well_defined = False
    kernel_size = sum(1 for g in Gg if F[g] == IDENT) if well_defined else None
    return well_defined, kernel_size, F


def generates_full_Gg(A, B):
    return group_closure([A, B]) == Gg


def main():
    with open(CERT_PATH, encoding="utf-8") as fh:
        cert = json.load(fh)

    if cert.get("schema") != "s4-settled54/v2":
        fail(f"unexpected schema: {cert.get('schema')}")

    # ---- (2) c in N_S4 direct value, independently recomputed ----
    claimed_c_in_n = cert["point2_c_in_N"]["s_squared_is_identity"]
    if claimed_c_in_n != point2_c_in_n_independent:
        fail(f"point2_c_in_N mismatch: cert={claimed_c_in_n} independent={point2_c_in_n_independent}")
    else:
        ok(f"point2_c_in_N agrees: cert={claimed_c_in_n} independent={point2_c_in_n_independent}")

    # ---- (a) enumeration completeness raw facts, independently recomputed ----
    a = cert["a_enumeration_completeness"]
    if a["g_size"] != len(Gg):
        fail(f"g_size mismatch: cert={a['g_size']} independent={len(Gg)}")
    if a["charming_set_size"] != len(charming_set_independent):
        fail(f"charming_set_size mismatch: cert={a['charming_set_size']} independent={len(charming_set_independent)}")
    if a["n_ord"] != nOrd:
        fail(f"n_ord mismatch: cert={a['n_ord']} independent={nOrd}")
    exp_candidate_total = len(Gg) * len(charming_set_independent)  # Gg perfect (PSL(2,8) simple) => D=Gg
    if a["candidate_total"] != exp_candidate_total:
        fail(f"candidate_total mismatch: cert={a['candidate_total']} independent={exp_candidate_total}")
    else:
        ok(f"candidate_total agrees: {a['candidate_total']} (= |Gg| x |charming_set|, independent)")
    if not a["derived_subgroup_order_agrees"] or a["derived_subgroup_order_via_dwords_count"] != len(Gg):
        fail("cert's own derived-subgroup-order agreement check is not internally consistent")

    # ---- (b) kernel equality, independent from-scratch re-derivation per shadow ----
    detail = cert["b_kernel_equality"]["detail"]
    shadow_total = cert["b_kernel_equality"]["shadow_total"]
    if len(detail) != shadow_total:
        fail(f"detail length {len(detail)} != shadow_total {shadow_total}")

    n_agree = 0
    n_disagree = 0
    n_kernel_trivial_independent = 0
    for entry in detail:
        m = entry["m"]
        f_word = [(l[0], l[1]) for l in entry["f_word"]]
        u = 2 * m + 1
        f = reconstruct_f(f_word)
        A = perm_pow(X, u)
        # NOTE convention: GAP's AbstractProd([f^-1, Y^u, f]) computes val=list[1]^0 then
        # val:=val*list[3] (=f); val:=val*list[2] (=f*Y^u); val:=val*list[1] (=f*Y^u*f^-1) --
        # i.e. the GAP-form REVERSAL of the paper's "f^-1 Y^u f", giving the LITERAL GAP value
        # f * Y^u * f^-1 (search/week3-battery-common.g AbstractProd, read in full this session;
        # re-derived by hand-tracing the loop, not assumed from the paper-notation docstring).
        B = perm_mul(perm_mul(f, perm_pow(Y, u)), perm_inv(f))
        surj = generates_full_Gg(A, B)
        well_defined_ind, kernel_size_ind, _F = is_homomorphism_well_defined_and_kernel(A, B)
        kernel_trivial_ind = well_defined_ind and (kernel_size_ind == 1)
        if kernel_trivial_ind:
            n_kernel_trivial_independent += 1

        cert_wd = entry["well_defined"]
        cert_kt = entry["kernel_trivial"]
        if (cert_wd, cert_kt) == (well_defined_ind, kernel_trivial_ind):
            n_agree += 1
        else:
            n_disagree += 1
            print(f"[DISAGREE] m={m} f_word={f_word}: cert(well_defined={cert_wd},kernel_trivial={cert_kt}) "
                  f"independent(well_defined={well_defined_ind},kernel_trivial={kernel_trivial_ind},"
                  f"kernel_size={kernel_size_ind},surj={surj})")

    print(f"[RAW] per-shadow agree={n_agree} disagree={n_disagree} out of {len(detail)}")
    print(f"[RAW] independent kernel_trivial_count={n_kernel_trivial_independent} "
          f"cert kernel_trivial_count={cert['b_kernel_equality']['kernel_trivial_count']}")
    if n_disagree > 0:
        fail(f"{n_disagree} shadow(s) disagree between cert and independent recomputation")
    if n_kernel_trivial_independent != cert["b_kernel_equality"]["kernel_trivial_count"]:
        fail("independent kernel_trivial_count != cert's kernel_trivial_count")

    # ---- secondary K5-8 automorphism-witness cross-reference, independently re-searched ----
    # NOTE: this is explicitly non-load-bearing (per cert's own secondary_cross_reference.note);
    # reported as a raw independent count, not used to determine isolated here.
    aut_elts_list = list(aut_elts)
    n_settled_independent = 0
    settled_mismatch = []
    for entry in detail:
        m = entry["m"]
        f_word = [(l[0], l[1]) for l in entry["f_word"]]
        u = 2 * m + 1
        f = reconstruct_f(f_word)
        targetX = perm_pow(X, u)
        targetY = perm_mul(perm_mul(f, perm_pow(Y, u)), perm_inv(f))  # same AbstractProd reversal, see above
        witness_found = False
        for h in aut_elts_list:
            hinv = perm_inv(h)
            if perm_mul(perm_mul(hinv, X), h) == targetX and perm_mul(perm_mul(hinv, Y), h) == targetY:
                witness_found = True
                break
        if witness_found:
            n_settled_independent += 1

    print(f"[RAW] independent K5-8 witness settled_count={n_settled_independent} "
          f"cert secondary settled_count={cert['b_kernel_equality']['secondary_cross_reference']['settled_count']}")
    if n_settled_independent != cert["b_kernel_equality"]["secondary_cross_reference"]["settled_count"]:
        fail("independent K5-8 settled_count != cert's secondary_cross_reference.settled_count")

    # ---- isolated field, recomputed from independent kernel_trivial_count ----
    isolated_independent = (n_kernel_trivial_independent == shadow_total)
    if cert["isolated"] != isolated_independent:
        fail(f"isolated mismatch: cert={cert['isolated']} independent={isolated_independent}")
    else:
        ok(f"isolated agrees: cert={cert['isolated']} independent={isolated_independent}")

    print(f"\n[RAW SUMMARY] shadow_total={shadow_total} "
          f"kernel_trivial_count: cert={cert['b_kernel_equality']['kernel_trivial_count']} "
          f"independent={n_kernel_trivial_independent} | "
          f"K5-8 settled_count: cert={cert['b_kernel_equality']['secondary_cross_reference']['settled_count']} "
          f"independent={n_settled_independent} | "
          f"isolated: cert={cert['isolated']} independent={isolated_independent} | "
          f"prior human claim: settled_count=54/54")

    if FAILS:
        print(f"\n{len(FAILS)} check(s) FAILED:")
        for m in FAILS:
            print(" -", m)
        sys.exit(1)
    else:
        print("\nAll checks: raw agreement, no disagreement found (cross-checked, not verified).")
        sys.exit(0)


if __name__ == "__main__":
    main()
