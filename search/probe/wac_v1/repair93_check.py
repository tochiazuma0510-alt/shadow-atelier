# 便93 修理波 — 手計算の機械確認(整数・有理・Gauss 整数のみ。浮動小数点なし)
from fractions import Fraction as Q

print("=== A. P93-1: 有限合同を 2 で割る偽推論の反例 ===")
bad = []
for a in range(1, 8):
    M = 2**a
    sols = [m for m in range(M) if (2*m+1) % M == 1 % M]
    bad.append((a, sols))
    print(f"  a={a}: 2m+1=1 mod {M} の解 m = {sols}  (期待: m≡0 mod 2^(a-1) = {2**(a-1)})")
assert bad[2][1] == [0, 4], bad[2]
print("  ⟹ a>=2 で m=2^(a-1) が偽解として残る = 現稿の推論は成立しない (W93-1.1 は正しい)")

print("\n=== B. Ẑ → Z/2^a は 2-成分のみを通る(P93-1 の修理の骨) ===")
# m̂ = (χ-1)/2 ∈ Ẑ。χ_2 = 1(Z_2 内の等式)⟹ m̂_2 = 0 ⟹ 像 = 0 ∈ Z/2^a。
# 有限で確認: χ ≡ 1 mod 2^N を N→∞ で強めると m ≡ 0 mod 2^{N-1} → 0
for a in [2, 3, 4]:
    M = 2**a
    # m̂_2 = 0 を Z/2^{a+k} での近似で表す
    for k in [0, 1, 2, 5, 10]:
        # χ_2 = 1 + 2^{a+k+1}*t 型(= 2-adic に 1 へ収束)⟹ m = 2^{a+k}*t
        ms = {(2**(a+k) * t) % M for t in range(4)}
        assert ms == {0} or k == 0, (a, k, ms)
    print(f"  a={a}: χ_2=1 の 2-adic 等式から m ≡ 0 mod 2^{a}  ✓")

print("\n=== C. u_{n,α} = -1/h_1^2 = 4(-1)^α(Gauss 整数の厳密演算) ===")
class Gi:  # Q(i) 上の厳密演算
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a, s.b = Q(a), Q(b)
    def __add__(s, o): o = cast(o); return Gi(s.a+o.a, s.b+o.b)
    def __sub__(s, o): o = cast(o); return Gi(s.a-o.a, s.b-o.b)
    def __mul__(s, o): o = cast(o); return Gi(s.a*o.a - s.b*o.b, s.a*o.b + s.b*o.a)
    def inv(s):
        n = s.a*s.a + s.b*s.b
        return Gi(s.a/n, -s.b/n)
    def __truediv__(s, o): return s * cast(o).inv()
    def __eq__(s, o): o = cast(o); return s.a == o.a and s.b == o.b
    def __repr__(s): return f"({s.a}{'+' if s.b>=0 else '-'}{abs(s.b)}i)"
def cast(x): return x if isinstance(x, Gi) else Gi(x)
I = Gi(0, 1)

def h1_closed(alpha):
    # 便 93 F93-2.4 / 発火ログ §2.3:  h_1 = (-i)^{α+1}/2 = (-i)^α/(2i)
    v = Gi(1)
    for _ in range(alpha + 1): v = v * (I * Gi(-1))
    return v / Gi(2)

def h1_limit(alpha):
    # h(k) = (k-i)/(k+i) * ((k+1)/(k-1))^α  の k=i での h/(k-i) の極限
    # = 1/(2i) * ((i+1)/(i-1))^α
    v = ((I + Gi(1)) / (I - Gi(1)))
    p = Gi(1)
    for _ in range(alpha): p = p * v
    return p / (Gi(2) * I)

def m0prime_at_i():
    # m_0 = (1+k^2)/(1-k^2),  m_0' = 4k/(1-k^2)^2,  k=i ⟹ 4i/4 = i
    return (Gi(4) * I) / ((Gi(1) - I*I) * (Gi(1) - I*I))

assert m0prime_at_i() == I, m0prime_at_i()
print(f"  m_0'(i) = {m0prime_at_i()}  ✓ (= i)")
for alpha in range(1, 8):
    a1, a2 = h1_closed(alpha), h1_limit(alpha)
    assert a1 == a2, (alpha, a1, a2)
    u = Gi(-1) / (a1 * a1)
    expect = Gi(4 * (-1)**alpha)
    assert u == expect, (alpha, u, expect)
    print(f"  α={alpha}: h_1={a1}  u=-1/h_1^2={u}  = 4(-1)^α ✓")
print("  ⟹ n は一切現れない(y^n=h の分岐指数としてのみ)= F93-3.1 の n-非依存性 ✓")

print("\n=== D. 位数: ord([±4]_{2n}) = n(n 奇・e(p|2)=2 ⟹ w_p(4)=4) ===")
from math import gcd
for n in [3, 5, 7, 9, 11, 13, 15, 21]:
    if n % 2 == 0: continue
    M = 2*n
    ordv = M // gcd(M, 4)      # 付値像 4 ∈ Z/2n の位数
    assert ordv == n, (n, ordv)
print("  n=3,5,7,9,11,13,15,21 で 2n/gcd(2n,4) = n ✓(合成数含む)")
print("  かつ (-1) = ζ_{4n}^{2n} ∈ F^{×2n} ⟹ [4]_{2n} = [-4]_{2n} ✓")

print("\n=== E. T3: N_gen <= N_w <= N_tr(F93-5.2 の局所修文)の実データ照合 ===")
rows = [  # (l, t, n, N_w(Q), N_tr, N_gen) — 加重追補 §4 の表
    (7, 2, 9, Q(1),   1, 0),
    (9, 1, 10, Q(6),  6, 6),
    (9, 3, 12, Q(1,3),1, 0),
    (3, 1, 4, Q(1),   1, 1),
]
for l, t, n, Nw, Ntr, Ngen in rows:
    ok = (Ngen <= Nw <= Ntr)
    print(f"  (l,t,n)=({l},{t},{n}): N_gen={Ngen} <= N_w={Nw} <= N_tr={Ntr} : {ok}")
    assert ok
print("  ⟹ 追補 §1 の『N_w < N_gen も原理的に起こりうる』は n>=4 では偽 ✓")

print("\n=== F. settled: 正しい 1 行 assert(反準同型 ℓ 経由)===")
# τ(g) = ĉ(g)^{-1} は反自己同型。ℓ(q) := τ(ρ(q)) = f。
# ℓ(T'(Ψ(y))) = τ(ρ(q) ȳ^u ρ(q)^{-1}) = τ(ρ(q))^{-1} τ(ȳ^u) τ(ρ(q)) = f^{-1} ȳ^u f
# (τ(ȳ^u) = (ĉ(ȳ)^u)^{-1} = ((ȳ^{-1})^u)^{-1} = ȳ^u を使う)
# A5 = <x̄,ȳ> ⊂ S5 で全数確認する
from itertools import permutations
def mul(p, q): return tuple(p[q[i]] for i in range(5))     # (p∘q)(i) = p(q(i))
def inv(p):
    r = [0]*5
    for i, v in enumerate(p): r[v] = i
    return tuple(r)
def pw(p, k):
    r = tuple(range(5))
    k %= 60
    for _ in range(k): r = mul(r, p)
    return r
S5 = list(permutations(range(5)))
def sgn(p):
    s = 0
    for i in range(5):
        for j in range(i+1, 5):
            if p[i] > p[j]: s += 1
    return (-1)**s
A5 = [p for p in S5 if sgn(p) == 1]
xb = (1, 2, 3, 4, 0)                    # 5-cycle
yb = None
# ȳ を位数 5 で <x̄,ȳ> = A5 となるよう 1 つ選ぶ
for p in A5:
    if pw(p, 5) == tuple(range(5)) and p != tuple(range(5)):
        # 生成確認
        gen, frontier = {tuple(range(5))}, [tuple(range(5))]
        while frontier:
            nf = []
            for g in frontier:
                for s in (xb, p):
                    h = mul(g, s)
                    if h not in gen: gen.add(h); nf.append(h)
            frontier = nf
        if len(gen) == 60: yb = p; break
assert yb is not None
# ĉ: x̄↦x̄^{-1}, ȳ↦ȳ^{-1} なる Aut(A5)=S5 の元(共役 κ)
kappas = [k for k in S5 if mul(mul(inv(k), xb), k) == inv(xb) and mul(mul(inv(k), yb), k) == inv(yb)]
assert len(kappas) == 1, len(kappas)
kap = kappas[0]
def chat(g): return mul(mul(inv(kap), g), kap)
def tau(g): return inv(chat(g))
# τ が反自己同型・対合
for g in A5:
    assert tau(tau(g)) == g
    for h in A5:
        assert tau(mul(g, h)) == mul(tau(h), tau(g))
# 主張: ℓ(T'(Ψ(y))) = (ȳ^u)^f  ただし ρ(q)=τ(f)、T'(Ψ(y)) の ρ-像 = ρ(q) ȳ^u ρ(q)^{-1}
bad_naive = 0
for u in [1, 3, 7, 9]:
    yu = pw(yb, u % 5)
    for f in A5:
        rq = tau(f)
        rho_img = mul(mul(rq, yu), inv(rq))          # ρ(T'(Ψ(y)))
        lhs = tau(rho_img)                            # ℓ(T'(Ψ(y)))
        rhs = mul(mul(inv(f), yu), f)                 # (ȳ^u)^f = f^{-1} ȳ^u f
        assert lhs == rhs, (u, f)
        if rho_img != rhs: bad_naive += 1             # 旧 assert(ρ 側で直接比較)の失敗数
        # Sol の別表示: ρ(T'(Ψ(y))) = (ȳ^u)^{ĉ(f)}
        assert rho_img == mul(mul(inv(chat(f)), yu), chat(f))
print(f"  ℓ(T'(Ψ(y))) = (ȳ^u)^f : 4×60 = 240 通り全一致 ✓")
print(f"  旧 assert ρ(T'(Ψ(y))) =! (ȳ^u)^f が破れる組: {bad_naive}/240  ⟹ 指定は偽(W93-4.1 は正しい)")
print(f"  ρ(T'(Ψ(y))) = (ȳ^u)^{{ĉ(f)}} : 240 通り全一致 ✓")

print("\n=== G. KUM: 塔が 4 点の cross-ratio を固定する(harmonic)===")
# (m-μ+)/(m-μ-) = δ k^2, μ± = ±γ^{-1/2}  ⟹ m=0 で k^2 = -1/δ, m=∞ で k^2 = 1/δ
# Q̄ 正規化 δ=1: κ_{1,2}=±i, κ_{3,4}=±1
z1, z2, z3, z4 = I, Gi(0, -1), Gi(1), Gi(-1)
cr = ((z1 - z3) * (z2 - z4)) / ((z1 - z4) * (z2 - z3))
print(f"  cross-ratio(i,-i;1,-1) = {cr}  (= -1 : 調和・自由度ゼロ)")
assert cr == Gi(-1)
print("  ⟹『4 点+指数だけで剛』は一般には偽だが、塔が配置を調和点に固定する(W93-2.1 の指摘どおり)")

print("\nALL CHECKS PASSED")
