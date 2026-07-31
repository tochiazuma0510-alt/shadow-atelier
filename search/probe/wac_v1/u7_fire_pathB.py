# u7 FIRE - path B (block character) + F-arithmetic of the measured value.
# Pure integer / finite-group arithmetic.  n = 5 skipped (freeze U7-NO5).
from fractions import Fraction as Fr
import sys
sys.path.insert(0, ".")
from tw_blocks import QTAB

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

if __name__ == "__main__":
    for n in (3, 7, 9, 11, 13):
        for a in range(1, (n-1)//2 + 1):
            print(block_character(n, a), flush=True)
    print("---- F-arithmetic ----", flush=True)
    print("n=3 (calibration, public u_3=-4):", F_arith(3, -4), flush=True)
    print("n=7 (window alpha=1):           ", F_arith(7, -4), flush=True)
