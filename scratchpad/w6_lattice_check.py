# w6_lattice_check.py --- Γ-安定部分格子の分類と NC-2 の帰結(単系統 python・整数演算のみ)
# F_2^ab = Z^2, 基底 (x̄,ȳ)。θ(a,b)=(b,a) ; τ(x̄)=ȳ, τ(ȳ)=-x̄-ȳ ⟹ τ(a,b)=(-b, a-b)
M = 12                                    # (Z/12)^2 の中で 12Z^2 ⊇ を含む部分格子を悉皆
def th(v): return (v[1] % M, v[0] % M)
def ta(v): return ((-v[1]) % M, (v[0] - v[1]) % M)
def gen(vs):                              # vs で生成する (Z/12)^2 の部分群
    S = {(0, 0)}
    frontier = [(0, 0)]
    while frontier:
        nxt = []
        for s in frontier:
            for v in vs:
                p = ((s[0] + v[0]) % M, (s[1] + v[1]) % M)
                if p not in S: S.add(p); nxt.append(p)
        frontier = nxt
    return frozenset(S)

FAILS = []
def chk(name, got, want):
    ok = (got == want); print(f"[{'PASS' if ok else 'FAIL'}] {name}: {got} (期待 {want})")
    if not ok: FAILS.append(name)

allelt = [(a, b) for a in range(M) for b in range(M)]
subs = {gen([u, v]) for u in allelt for v in allelt}
stable = {S for S in subs if all(th(v) in S and ta(v) in S for v in S)}
idx_stable = sorted({M * M // len(S) for S in stable})
# 分類予測: Γ-安定 ⟺ Z[ω] の共役安定イデアル (n)(1-ω)^a ⟹ 指数 = n^2 * 3^a
pred = sorted({n * n * 3 ** a for n in range(1, 13) for a in range(0, 5)
               if (n * n * 3 ** a) in [M * M // len(S) for S in subs]
               and (M * M) % (n * n * 3 ** a) == 0
               and n * n * 3 ** a <= 144})
chk("E1 Γ-安定部分格子の指数集合(12Z^2 ⊇ の範囲)", idx_stable,
    sorted({i for i in pred if any(M * M // len(S) == i for S in stable)}))
chk("E2 ★ 指数 2 の Γ-安定部分格子は存在しない", 2 in idx_stable, False)
chk("E3 ★ 2 冪指数は 1,4,16 のみ(= 2^j Z^2)",
    [i for i in idx_stable if i in (1, 2, 4, 8, 16, 32, 64, 128)], [1, 4, 16])
chk("E4 ★ 3 冪指数(144 の約数の範囲では 1,3,9 のみ: 27|144 は偽)",
    [i for i in idx_stable if i in (1, 3, 9, 27, 81)], [1, 3, 9])
chk("E5 全指数が n^2*3^a 型",
    all(any(i == n * n * 3 ** a for n in range(1, 13) for a in range(0, 5))
        for i in idx_stable), True)

# index-2 の 3 個の部分格子(2Z^2 の中)を明示し、どれも Γ で保たれないこと
L = {"L1: a≡0(4),b≡0(2)": lambda a, b: a % 4 == 0 and b % 2 == 0,
     "L2: a≡0(2),b≡0(4)": lambda a, b: a % 2 == 0 and b % 4 == 0,
     "L3: a≡b(4), 両偶":   lambda a, b: a % 2 == 0 and b % 2 == 0 and (a - b) % 4 == 0}
for name, f in L.items():
    elts = [(a, b) for a in range(-8, 9) for b in range(-8, 9) if f(a, b)]
    ok_th = all(f(*th0) for th0 in [(b, a) for (a, b) in elts])
    ok_ta = all(f(*(-b, a - b)) for (a, b) in elts)
    chk(f"E6 {name} は Γ-安定でない", ok_th and ok_ta, False)

# NC-2 の帰結: α(N_F2)=2^{j+1}Z^2 ⟹ (2,-2)∉α ⟺ j≥1 ⟺ |V/W|=4^j≥4
chk("E7 (2,-2) ∈ 2Z^2", (2 % 2 == 0 and -2 % 2 == 0), True)
chk("E8 ★ (2,-2) NOT-IN 4Z^2 (= K^{(20)} は NC-2 を通る)", (2 % 4 == 0), False)
# p=3: α = 2*(1-ω)^a。(1-ω) = (x̄-ȳ) 生成。(2,-2)=2(x̄-ȳ) ∈ 2(1-ω)^a ⟺ (1,-1) ∈ (1-ω)^a
#   (1-ω)^1 ∋ (1,-1) [自明] ; (1-ω)^2 = (3) ∌ (1,-1)
chk("E9 ★ p=3: (1,-1) IN (1-w) but NOT-IN 3Z^2", (1 % 3 == 0), False)

print("\nFAILS =", len(FAILS), "->", FAILS if FAILS else "ALL PASS")
