# w6_vcen_check.py --- F102-6.2 の主張「V ⊄ Z(G_20)」の検算(単系統 python・整数演算のみ)
# D_m = <r,s | r^m, s^2, srs^-1 r>,  元は (eps,k) = r^k s^eps
# psi_20: x -> (r,s,s), y -> (rs,r,rs), c -> (1,1,1)   [addendum B §1 逐語]
M = 20
def mul1(a, b):            # (eps_a,k_a)*(eps_b,k_b)
    ea, ka = a; eb, kb = b
    return ((ea + eb) % 2, (ka + (-kb if ea else kb)) % M)
def inv1(a):
    e, k = a
    return (e, k % M) if e else (0, (-k) % M)
def mul(g, h): return tuple(mul1(g[i], h[i]) for i in range(3))
def inv(g):    return tuple(inv1(g[i]) for i in range(3))
ID = ((0,0),(0,0),(0,0))
r  = (0,1); s = (1,0); rs = mul1(r, s)
X  = (r, s, s)
Y  = (rs, r, rs)

def closure(gens, seed=ID):
    G, frontier = {seed}, [seed]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                p = mul(g, h)
                if p not in G: G.add(p); nxt.append(p)
        frontier = nxt
    return G

G = closure([X, Y])
FAILS = []
def chk(name, got, want):
    ok = (got == want); print(f"[{'PASS' if ok else 'FAIL'}] {name}: {got} (期待 {want})")
    if not ok: FAILS.append(name)

chk("D1 |G_20|", len(G), 4000)

# V = <r^10>^3  (addendum B §2.2)
V = [tuple((0, 10*b[i]) for i in range(3)) for b in
     [(a,b_,c_) for a in (0,1) for b_ in (0,1) for c_ in (0,1)]]
chk("D2 V ⊆ G_20", all(v in G for v in V), True)
chk("D3 |V|", len(set(V)), 8)

# ★ 核心: V の各元が G_20 の全元と可換か(= V ⊆ Z(G_20))
chk("D4 V ⊆ Z(G_20) [全 8×4000 対]",
    all(mul(v, g) == mul(g, v) for v in V for g in G), True)

# Z(G_20) を完全に計算(生成元との可換で判定)
Z = {g for g in G if mul(g, X) == mul(X, g) and mul(g, Y) == mul(Y, g)}
chk("D5 |Z(G_20)|", len(Z), 8)
chk("D6 Z(G_20) = V", Z == set(V), True)

# 導来部分群 [G,G] と W = V ∩ [G,G]
comms = [mul(mul(inv(a), inv(b)), mul(a, b)) for a in (X, Y) for b in (X, Y)]
D = closure(comms)
while True:                                   # 正規閉包
    new = [mul(mul(g, d), inv(g)) for g in (X, Y) for d in D]
    D2 = closure(list(D) + new)
    if D2 == D: break
    D = D2
chk("D7 |[G_20,G_20]|", len(D), 250)
W = [v for v in V if v in D]
chk("D8 |W| = |V ∩ [G,G]|", len(W), 2)
chk("D9 W = 対角 <(r^10,r^10,r^10)>", set(W) == {ID, ((0,10),(0,10),(0,10))}, True)

# 屋根 witness (f_1,1) = (6,4,0) 座標 = (r^12, r^8, 1)
wit = ((0,12), (0,8), (0,0))
chk("D10 witness ∈ G_20", wit in G, True)
chk("D11 witness ∈ [G_20,G_20]", wit in D, True)
f1lift = ((0,2), (0,18), (0,0))               # f_1 = (r^2, r^-2, 1)
red5 = lambda g: tuple((e, k % 5) for (e, k) in g)   # D_20 -> D_5
chk("D12 witness ≡ f_1 (mod 5)", red5(wit) == red5(f1lift), True)
chk("D13 witness と f_1 の差 ∈ V", mul(inv(f1lift), wit) in V, True)

# θ: X<->Y が G_20 の自己同型か(graph が |G| 位数か)を確認し、V 上の作用を読む
def closure2(gens):                      # G×G の中での閉包
    S, frontier = {(ID, ID)}, [(ID, ID)]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                p = (mul(g[0], h[0]), mul(g[1], h[1]))
                if p not in S: S.add(p); nxt.append(p)
        frontier = nxt
    return S
GR = closure2([(X, Y), (Y, X)])
chk("D14 θ(X)=Y, θ(Y)=X は自己同型(graph 位数)", len(GR) == len(G), True)
th = dict(GR)
Vfix = [v for v in V if th[v] == v]
chk("D15 V^θ は V 全体ではない(= θ は座標を入れ替える)", len(Vfix), 4)
chk("D16 V^θ ∩ 対角 = W", all(w in Vfix for w in W), True)
# ★ 対比: θ は V を点ごとに固定しない が、V は Z(G_20) に入る
chk("D17 ★ (V ⊆ Z(G_20)) かつ (V^θ ≠ V) が両立",
    (set(V) <= Z) and (len(Vfix) < len(V)), True)

print("\nFAILS =", len(FAILS), "->", FAILS if FAILS else "ALL PASS")
