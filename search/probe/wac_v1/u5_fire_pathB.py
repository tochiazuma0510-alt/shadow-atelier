# u5 FIRE - path B (block character + orientation self-check) + F-arithmetic of the
# measured value.  Pure integer / finite-group arithmetic.  Ported verbatim from
# u7_fire_pathB.py (block_character, F_arith) with an added orientation_self_check
# (ported from tw_orient.py's O1/O2/O3 mechanism) for the CV-13 calibration gate.
#
# n=5 DISCIPLINE:
#   ALLOWED_N below intentionally contains 5.  This is a *versioned release*, scoped to
#   this script only, under 裁定 396 (2026-08-01 研究者一括認可 (2) n=5 開封).  No other
#   probe's ALLOWED_N is touched or reinterpreted; freeze U7-NO5 remains in force
#   everywhere else (tw_blocks.py / tw_orient.py / u7_fire_path{A,B}.py / m2_*.py).
#
# Independence from path A (u5_fire_pathA.py): this module shares NO code, NO helper
# functions and NO intermediate values with path A.  It only shares the low-level
# permutation-arithmetic table tw_blocks.QTAB with itself (same in-path sharing as the
# u7 firing had between u7_fire_pathB.py and tw_orient.py/tw_blocks.py).
from fractions import Fraction as Fr
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tw_blocks import QTAB

ALLOWED_N = (5,)   # 裁定396 (2026-08-01) による n=5 の versioned 解除。この script 限定。


# ---------- path B : does Phi(F_0) = inn(<X^2>) preserve each block of Lambda ? ----------
def block_character(n, alpha):
    def enc(v, q): return ((v[0]*n + v[1])*n + v[2])*4 + q
    def dec(x):
        q = x % 4; x //= 4
        c = x % n; x //= n
        return (x // n, x % n, c), q
    def act(q, v):
        if q == 0: return v
        return tuple(v[j] if (j+1) == q else (-v[j]) % n for j in range(3))
    def mul(x, y):
        v, q = dec(x); w, r = dec(y); aw = act(q, w)
        return enc(tuple((v[j]+aw[j]) % n for j in range(3)), QTAB[q][r])
    def inv(x):
        v, q = dec(x); return enc(act(q, tuple((-t) % n for t in v)), q)

    G = list(range(4*n**3))
    U = [((alpha*t) % n, s % n, t % n) for s in range(n) for t in range(n)]
    H = frozenset(enc(v, q) for v in U for q in (0, 2))
    AH = set(enc((a,b,c), q) for a in range(n) for b in range(n) for c in range(n) for q in (0,2))
    X  = enc((1,0,0), 1); X2 = mul(X, X)

    # Lambda = set of G-conjugates of H  (identified with G/H since N_G(H) = H)
    Lam = set()
    for g in G:
        Lam.add(frozenset(mul(mul(g, h), inv(g)) for h in H))
    Lam = sorted(Lam, key=lambda s: min(s))
    idx = {s: i for i, s in enumerate(Lam)}
    def conj(g, S): return frozenset(mul(mul(g, h), inv(g)) for h in S)

    # blocks = AH-orbits on Lambda (by conjugation)
    seen = [-1]*len(Lam); nb = 0
    for i0 in range(len(Lam)):
        if seen[i0] != -1: continue
        st = [i0]; seen[i0] = nb
        while st:
            x = st.pop()
            for g in AH:
                y = idx[conj(g, Lam[x])]
                if seen[y] == -1: seen[y] = nb; st.append(y)
        nb += 1
    blocks = [len([i for i in range(len(Lam)) if seen[i] == b]) for b in range(nb)]

    # Phi(F_0) = inn(<X^2>)   [canon: Sol bin 73 Q1.5 / w2fam_v1.md 3.5]
    gen = X2; g = enc((0,0,0), 0); F0img = []
    for _ in range(n):
        F0img.append(g); g = mul(g, gen)
    swaps = [any(seen[idx[conj(g, Lam[i])]] != seen[i] for i in range(len(Lam))) for g in F0img]
    return dict(n=n, alpha=alpha, nblocks=nb, blocks=blocks,
                X2_in_AH=(X2 in AH), F0img_size=len(set(F0img)),
                any_element_swaps_blocks=any(swaps),
                block_character_trivial=(not any(swaps)))


# ---------- orientation self-check (ported from tw_orient.py) ----------
# (O1) Is H conjugate to XHX^{-1} inside AH?   (expected NO, because N_G(H)=H)
# (O2) rotation ratio r_inf/r_0 read on block 1 vs block 2 (expected: r and -r)
# (O3) does the AH-block system get swapped by X?  (expected YES)
def orientation_self_check(n, alpha):
    def enc(v, q): return ((v[0]*n + v[1])*n + v[2])*4 + q
    def dec(x):
        q = x % 4; x //= 4
        c = x % n; x //= n
        return (x // n, x % n, c), q
    def act(q, v):
        if q == 0: return v
        return tuple(v[j] if (j+1) == q else (-v[j]) % n for j in range(3))
    def mul(x, y):
        v, q = dec(x); w, r = dec(y); aw = act(q, w)
        return enc(tuple((v[j]+aw[j]) % n for j in range(3)), QTAB[q][r])
    def inv(x):
        v, q = dec(x); return enc(act(q, tuple((-t) % n for t in v)), q)

    G = list(range(4*n**3))
    U = [((alpha*t) % n, s % n, t % n) for s in range(n) for t in range(n)]
    H = [enc(v, q) for v in U for q in (0, 2)]
    Hset = set(H)
    AH = [enc((a,b,c), q) for a in range(n) for b in range(n) for c in range(n) for q in (0,2)]

    X  = enc((1,0,0), 1)
    Y  = enc((1,1,1), 2)
    XY = mul(X, Y)
    Z  = inv(XY)
    X2 = mul(X, X); Z2 = mul(Z, Z)

    # (O1)
    XHX = set(mul(mul(X, h), inv(X)) for h in H)
    conj_in_AH = any(set(mul(mul(g, h), inv(g)) for h in XHX) == Hset for g in AH)

    # cosets
    def coset(g): return min(mul(g, h) for h in H)
    cid = {}; reps = []
    canon = {}
    for g in G:
        c = coset(g)
        if c not in cid:
            cid[c] = len(reps); reps.append(c)
        canon[g] = cid[c]
    L = len(reps)
    def app(g, k): return canon[mul(g, reps[k])]

    # blocks
    seen = [-1]*L; nb = 0
    for k in range(L):
        if seen[k] != -1: continue
        st=[k]; seen[k]=nb
        while st:
            x = st.pop()
            for g in AH:
                y = app(g, x)
                if seen[y] == -1: seen[y]=nb; st.append(y)
        nb += 1
    blocks = [[k for k in range(L) if seen[k]==b] for b in range(nb)]

    # (O3)
    X_swaps = (seen[app(X, blocks[0][0])] != 0)

    # (O2) ratio on each block
    ratios = []
    for b in blocks:
        p = b[0]
        phi = {}; x = p
        for j in range(n):
            phi[x] = j; x = app(X2, x)
        assert x == p and len(phi) == n, "X^2 not an n-cycle on the block"
        r = phi[app(Z2, p)]
        ok = all((phi[app(Z2, y)] - phi[y]) % n == r for y in b)
        ratios.append((r, ok))

    out = dict(n=n, alpha=alpha,
                H_conj_XHXinv_in_AH=conj_in_AH,
                X_swaps_blocks=X_swaps,
                ratio_r_inf_over_r0_per_block=[r for r, _ in ratios],
                translation_consistent=[o for _, o in ratios],
                sum_of_two_ratios_mod_n=(ratios[0][0] + ratios[1][0]) % n)
    print(out, flush=True)
    return out


# ---------- F-arithmetic of the measured value in F_n = Q(zeta_{4n}) ----------
def ord_mod(a, m):
    r, k = a % m, 1
    while r != 1:
        r = (r*a) % m; k += 1
    return k

def F_arith(n, u_num):
    """u_num : the measured u_n (a nonzero rational).  F = Q(zeta_{4n}), M = 2n."""
    M = 2*n; N = 4*n
    u = Fr(u_num)
    # prime factorisation of |u| over Q
    val_Q = {}
    for x, s in ((u.numerator, 1), (u.denominator, -1)):
        x = abs(x); p = 2
        while x > 1:
            while x % p == 0: val_Q[p] = val_Q.get(p, 0) + s; x //= p
            p += 1
    sign = -1 if u < 0 else 1
    # ramification of p in Q(zeta_N): N = p^a * m, e = phi(p^a), f = ord of p mod m, g = phi(N)/(e f)
    def phi(x):
        r, y, p = x, x, 2
        while p*p <= y:
            if y % p == 0:
                while y % p == 0: y //= p
                r -= r//p
            p += 1
        if y > 1: r -= r//y
        return r
    def efg(p):
        a, m = 0, N
        while m % p == 0: m //= p; a += 1
        e = phi(p**a) if a > 0 else 1
        f = ord_mod(p % m, m) if m > 1 else 1
        return e, f, phi(N)//(e*f)
    places = {}
    for p, vq in val_Q.items():
        e, f, g = efg(p)
        places[p] = dict(e=e, f=f, g=g, v_Q=vq, w_frak_p=e*vq)
    # power tests, all by valuations (sufficient here since u is rational)
    def not_a_dth_power(d):
        return any(pl["w_frak_p"] % d != 0 for pl in places.values())
    # [u]_2 : u is a square in F iff |u| is a square in Q up to the roots of unity in F.
    # mu(F) = mu_{4n} (4|4n) so i in F; -1 = i^2.  So [u]_2 = [|u|]_2 and |u| = 4 => square.
    absu = abs(u)
    absu_is_square = (Fr(absu).numerator ** 0 == 1) and all(v % 2 == 0 for v in val_Q.values())
    return dict(
        u=str(u), sign=sign, places={str(p): v for p, v in places.items()},
        w_nonzero_places=[f"p|{p} (g={v['g']} primes, w={v['w_frak_p']})" for p, v in places.items()],
        minus_one_is_Mth_power_in_F=True,       # -1 = zeta_{4n}^{2n} = zeta_{2M}^M
        u_in_F_square=absu_is_square,           # |u| square in Q, and -1 = i^2 with i in F
        u_not_in_F_nth_power=not_a_dth_power(n),
        u_not_in_F_Mth_power=not_a_dth_power(M),
        u_not_in_Q_nth_power=any(v % n != 0 for v in val_Q.values()),
        exists_p_w_not_div_n=[p for p, v in places.items() if v["w_frak_p"] % n != 0],
        # order of [u]_M in F^x/F^{xM}:  divides n  (since u^n has all w == 0 mod M and
        # (-1) is an M-th power in F = Q(zeta_{2M})), and != 1, and n is prime here.
        ord_of_class_mod_M=(n if (not_a_dth_power(M) and all(
            (v["w_frak_p"]*n) % M == 0 for v in places.values())) else None),
        ord_certificate=dict(u_pow_n_all_w_div_M=all((v["w_frak_p"]*n) % M == 0
                                                     for v in places.values()),
                             class_nontrivial=not_a_dth_power(M)),
    )


def _load_u7_cert():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", "..", ".."))
    with open(os.path.join(root, "search", "certs", "u7_fire_20260801.json"), encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    # ---- CV-13 anchor: n=7 (and n=3) must bit-reproduce the frozen u7 cert ----
    cert = _load_u7_cert()
    anchor_fail = []

    bc3 = block_character(3, 1)
    if bc3["block_character_trivial"] != cert["path_B"]["all_alpha"]["n3_a1"]:
        anchor_fail.append(f"n=3 a=1 block_character_trivial: got {bc3['block_character_trivial']!r}")

    bc7 = {}
    for a in (1, 2, 3):
        r = block_character(7, a)
        bc7[f"n7_a{a}"] = r
        if r["block_character_trivial"] != cert["path_B"]["all_alpha"][f"n7_a{a}"]:
            anchor_fail.append(f"n=7 a={a} block_character_trivial: got {r['block_character_trivial']!r}")

    r7a1 = bc7["n7_a1"]
    if r7a1["X2_in_AH"] != cert["path_B"]["X2_in_AH"]:
        anchor_fail.append(f"n=7 a=1 X2_in_AH: got {r7a1['X2_in_AH']!r}")
    if r7a1["F0img_size"] != cert["path_B"]["PhiF0_image_size"]:
        anchor_fail.append(f"n=7 a=1 F0img_size: got {r7a1['F0img_size']!r}")
    if r7a1["any_element_swaps_blocks"] != cert["path_B"]["any_element_swaps_blocks"]:
        anchor_fail.append(f"n=7 a=1 any_element_swaps_blocks: got {r7a1['any_element_swaps_blocks']!r}")

    arith7 = F_arith(7, -4)   # -4 is the frozen public/measured u_7 value, not a prediction
    cert_places = cert["measured_quantities"]["(iv) all valuations"]["nonzero_places"]
    if {str(k): v for k, v in arith7["places"].items()} != cert_places:
        anchor_fail.append(f"n=7 F_arith places: got {arith7['places']!r}, cert {cert_places!r}")
    if arith7["ord_of_class_mod_M"] != cert["measured_quantities"]["(vi) ord(a_7)"]:
        anchor_fail.append(f"n=7 ord_of_class_mod_M: got {arith7['ord_of_class_mod_M']!r}")
    if arith7["u_in_F_square"] != cert["measured_quantities"]["(i) [u_7]_2"]["trivial"]:
        anchor_fail.append(f"n=7 u_in_F_square: got {arith7['u_in_F_square']!r}")

    # orientation self-check is not part of the u7 cert (new for CV-13); assert the
    # *structural* expectations documented in tw_orient.py's own header, for n=7 first.
    orient_fail = []
    for a in (1, 2, 3):
        o = orientation_self_check(7, a)
        if o["H_conj_XHXinv_in_AH"] is not False:
            orient_fail.append(f"n=7 a={a}: H_conj_XHXinv_in_AH expected False, got {o['H_conj_XHXinv_in_AH']!r}")
        if o["X_swaps_blocks"] is not True:
            orient_fail.append(f"n=7 a={a}: X_swaps_blocks expected True, got {o['X_swaps_blocks']!r}")
        if not all(o["translation_consistent"]):
            orient_fail.append(f"n=7 a={a}: translation_consistent expected all True, got {o['translation_consistent']!r}")
        if o["sum_of_two_ratios_mod_n"] != 0:
            orient_fail.append(f"n=7 a={a}: sum_of_two_ratios_mod_n expected 0, got {o['sum_of_two_ratios_mod_n']!r}")

    print("CV-13 ANCHOR (n=7 bit reproduction):", "PASS" if not anchor_fail else "FAIL", flush=True)
    for msg in anchor_fail:
        print("  MISMATCH:", msg, flush=True)
    print("CV-13 ORIENTATION SELF-CHECK (n=7 structural):", "PASS" if not orient_fail else "FAIL", flush=True)
    for msg in orient_fail:
        print("  MISMATCH:", msg, flush=True)
    assert not anchor_fail, "CV-13 anchor (n=7 bit reproduction of u7_fire_20260801.json) failed"
    assert not orient_fail, "CV-13 orientation self-check (n=7 structural expectations) failed"

    # ---- n=5 measurement (post-anchor; ALLOWED_N release scoped to this run) ----
    bc5 = []
    orient5 = []
    for n in ALLOWED_N:           # = (5,)  -- 裁定396 versioned release
        for a in range(1, (n-1)//2 + 1):
            bc5.append(block_character(n, a))
            orient5.append(orientation_self_check(n, a))

    orient5_ok = all(
        (o["H_conj_XHXinv_in_AH"] is False) and (o["X_swaps_blocks"] is True) and
        all(o["translation_consistent"]) and (o["sum_of_two_ratios_mod_n"] == 0)
        for o in orient5)
    print("n=5 orientation self-check structural-expectations hold:", orient5_ok, flush=True)
    print("n=5 all block_character_trivial:", all(r["block_character_trivial"] for r in bc5), flush=True)
