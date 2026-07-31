# Atomic confrontation: our coarse GT(N_A) list vs the third-party (Package GT) charming list.
# All permutations on {0..7} (GAP points 1..8 shifted), GAP convention: (p*q)(i) = q(p(i)).
import json, io, itertools

N = 8
def perm(cycles):
    p = list(range(N))
    for cyc in cycles:
        for i in range(len(cyc)):
            p[cyc[i]-1] = cyc[(i+1) % len(cyc)] - 1     # 1-based cycles in
    return tuple(p)
def mul(p, q):                      # GAP: first p, then q
    return tuple(q[p[i]] for i in range(N))
def inv(p):
    r = [0]*N
    for i, v in enumerate(p): r[v] = i
    return tuple(r)
def pw(p, k):
    if k < 0: p, k = inv(p), -k
    r = tuple(range(N))
    for _ in range(k): r = mul(r, p)
    return r
def cyc_str(p):                     # 1-based cycle notation
    seen = [False]*N; out = []
    for i in range(N):
        if not seen[i] and p[i] != i:
            c = []; j = i
            while not seen[j]:
                seen[j] = True; c.append(j+1); j = p[j]
            out.append(tuple(c))
    return "()" if not out else "".join("(" + ",".join(map(str, c)) + ")" for c in out)
ONE = tuple(range(N))

# ---- window (probe pent_t2t3_v2_20260731.g lines 33-40) ----
tt = perm([(1,2,3)]); aa = perm([(1,4,5)])
XX = mul(aa, inv(tt)); ss = mul(tt, pw(XX,3))
b1, a1 = tt, ss
aE = mul(a1, perm([(6,8)])); bE = mul(b1, perm([(6,8,7)]))
s1 = mul(inv(bE), aE); s2 = mul(aE, pw(bE,2)); cc = pw(mul(s1,s2),3)
xb = pw(s1,2); yb = pw(s2,2)
print("xb =", cyc_str(xb), " yb =", cyc_str(yb), " c =", cyc_str(cc))

# A5 = <xb,yb> on points 1..5
def closure(gens):
    S = {ONE}; frontier = [ONE]
    while frontier:
        nf = []
        for a in frontier:
            for g in gens:
                b = mul(a, g)
                if b not in S: S.add(b); nf.append(b)
        frontier = nf
    return S
P = closure([xb, yb]); print("|P| =", len(P))

# ---- our coarse hexagon (probe 'Hex', GAP left-to-right order) ----
def Hex_ours(m, f):
    u = 2*m+1
    L1 = mul(mul(mul(pw(s1,u), inv(f)), pw(s2,u)), f)
    R1 = mul(mul(mul(inv(f), mul(s1,s2)), pw(xb,-m)), pw(cc,m))
    L2 = mul(mul(mul(inv(f), pw(s2,u)), f), pw(s1,u))
    R2 = mul(mul(mul(mul(s2,s1), pw(yb,-m)), pw(cc,m)), f)
    return L1 == R1 and L2 == R2
charm = [m for m in range(5) if __import__('math').gcd(2*m+1,5) == 1]
ours = []
for m in charm:
    for f in sorted(P):
        if Hex_ours(m, f) and closure([xb, mul(mul(inv(f), yb), f)]) == P:
            ours.append((m, f))
print("our |GT(N_A)| =", len(ours))
ours_by_m = {}
for m, f in ours: ours_by_m.setdefault(m, []).append(cyc_str(f))
for m in sorted(ours_by_m): print("   m=%d:" % m, sorted(ours_by_m[m]))

# ---- third-party charming rows ----
d = json.load(io.open('search/certs/pent_thirdparty_gt_20260731.json', encoding='utf-8'))
rows = d['coarse_reduction']['charming']['per_entry_rows']
gens = {0: xb, 1: yb, 2: mul(inv(yb), inv(xb))}      # x12, x23, x13 (c=1 coarsely)

def evalword(w, reverse=False):
    letters = list(reversed(w)) if reverse else list(w)
    r = ONE
    for i in letters: r = mul(r, gens[i])
    return r

print("\n--- third-party charming rows vs our coarse list ---")
theirs = []
for r in rows:
    w, m = r['word'], r['m']
    rec = tuple(r['coarse_f_array_form'])
    fwd, rev = evalword(w, False), evalword(w, True)
    tag = "fwd" if fwd == rec else ("rev" if rev == rec else "NEITHER")
    f = rec
    theirs.append((m, f))
    print(f"  m={m} word_len={len(w)} recorded={cyc_str(rec)} eval[{tag}] "
          f"fwd={cyc_str(fwd)} rev={cyc_str(rev)}  ourHex={Hex_ours(m,rec)} "
          f"ourHex(f^-1)={Hex_ours(m,inv(rec))}")

so, st = set((m, cyc_str(f)) for m, f in ours), set((m, cyc_str(f)) for m, f in theirs)
print("\n|ours|=%d |theirs|=%d  |intersection|=%d" % (len(so), len(st), len(so & st)))
print("only ours  :", sorted(so - st))
print("only theirs:", sorted(st - so))

# is theirs = ours conjugated by a fixed sigma in S5 (acting on points 1..5)?
print("\n--- conjugation search ---")
for sig5 in itertools.permutations(range(1,6)):
    sig = tuple([sig5[i]-1 for i in range(5)] + [5,6,7])
    conj = set((m, cyc_str(mul(mul(inv(sig), f), sig))) for m, f in ours)
    if conj == st:
        print("  FOUND sigma =", cyc_str(sig))
# is theirs = {(m, f^-1)} of ours?
print("inverse map matches:", set((m, cyc_str(inv(f))) for m, f in ours) == st)
