# 補題 OPP の機械確認 — 正典の合成則 (3.53) は τ-座標で opposite 積になる
# 窓: K_pi(P = A5 = <x̄,ȳ>, x̄,ȳ 位数 5, u = 2m+1 ∈ {1,3,7,9})
# 主張:  τ(f1 · E_{m1,f1}(f2)) = Φ'_{m1,τ(f1)}(τ(f2)) · τ(f1)
#        ただし E_{m,f}: x̄↦x̄^u, ȳ↦f^{-1}ȳ^u f  (正典 3.53 の E)
#            Φ'_{m,g}: x̄↦x̄^u, ȳ↦ g ȳ^u g^{-1}
#            τ(g) = ĉ(g)^{-1}(ĉ = 両生成元を同時反転する Aut(P) の唯一元)
# 純整数(置換)演算のみ。
from itertools import permutations

N = 5
ID = tuple(range(N))
def mul(p, q): return tuple(p[q[i]] for i in range(N))      # (p∘q)(i)=p(q(i))
def inv(p):
    r = [0]*N
    for i, v in enumerate(p): r[v] = i
    return tuple(r)
def pw(p, k):
    r, k = ID, k % 60
    for _ in range(k): r = mul(r, p)
    return r
def sgn(p):
    s = 0
    for i in range(N):
        for j in range(i+1, N):
            if p[i] > p[j]: s += 1
    return (-1)**s

S5 = list(permutations(range(N)))
A5 = [p for p in S5 if sgn(p) == 1]
xb = (1, 2, 3, 4, 0)
yb = None
for p in A5:
    if p != ID and pw(p, 5) == ID:
        gen, fr = {ID}, [ID]
        while fr:
            nf = []
            for g in fr:
                for s in (xb, p):
                    h = mul(g, s)
                    if h not in gen: gen.add(h); nf.append(h)
            fr = nf
        if len(gen) == 60: yb = p; break
assert yb is not None

kap = [k for k in S5 if mul(mul(inv(k), xb), k) == inv(xb)
                    and mul(mul(inv(k), yb), k) == inv(yb)]
assert len(kap) == 1
kap = kap[0]
def chat(g): return mul(mul(inv(kap), g), kap)
def tau(g):  return inv(chat(g))
assert tau(xb) == xb and tau(yb) == yb, "tau は生成元を固定する(補題 OPP の骨)"
for a in A5:
    assert tau(tau(a)) == a
    for b in A5:
        assert tau(mul(a, b)) == mul(tau(b), tau(a))

# 語表現: P の各元を x̄,ȳ の語として持つ(BFS)
word = {ID: ()}
fr = [ID]
while fr:
    nf = []
    for g in fr:
        for lbl, s in (('x', xb), ('y', yb)):
            h = mul(g, s)
            if h not in word:
                word[h] = word[g] + (lbl,)
                nf.append(h)
        fr = fr  # noqa
    fr = nf
assert len(word) == 60

def evalw(w, ix, iy):
    r = ID
    for lbl in w: r = mul(r, ix if lbl == 'x' else iy)
    return r

def E_img(u, f):                       # E_{m,f}: x̄↦x̄^u, ȳ↦f^{-1}ȳ^u f
    return pw(xb, u), mul(mul(inv(f), pw(yb, u)), f)
def Phi_prime_img(u, g):               # Φ'_{m,g}: x̄↦x̄^u, ȳ↦ g ȳ^u g^{-1}
    return pw(xb, u), mul(mul(g, pw(yb, u)), inv(g))

def is_endo(ix, iy):                   # 生成元の像が P の自己準同型に延びるか(語の整合で判定)
    for g in A5:
        pass
    # 自由群 <x,y> ↠ P の核を保つか: 全語の評価が well-defined かを、
    # 「同じ元を表す 2 語の像が一致するか」で検査(BFS 語 + 追加の関係語)
    seen = {}
    frontier = [(ID, ID)]
    seen[ID] = ID
    while frontier:
        nf = []
        for g, img in frontier:
            for s, si in ((xb, ix), (yb, iy)):
                h, hi = mul(g, s), mul(img, si)
                if h in seen:
                    if seen[h] != hi: return False
                else:
                    seen[h] = hi; nf.append((h, hi))
        frontier = nf
    return len(seen) == 60

checked = 0
for m in range(5):
    u = 2*m + 1
    for f1 in A5:
        ix, iy = E_img(u, f1)
        if not is_endo(ix, iy):     # Φ_{m,f1} が存在しない場合は合成則の前提外
            continue
        g1 = tau(f1)
        jx, jy = Phi_prime_img(u, g1)
        assert is_endo(jx, jy), "Φ' も自己準同型のはず"
        for f2 in A5:
            lhs = tau(mul(f1, evalw(word[f2], ix, iy)))          # τ(f1 · E(f2))
            rhs = mul(evalw(word[tau(f2)], jx, jy), g1)          # Φ'(τ(f2)) · τ(f1)
            assert lhs == rhs, (m, f1, f2, lhs, rhs)
            checked += 1
print(f"lemma OPP: tau(f1*E_(m,f1)(f2)) == Phi'_(m,tau f1)(tau f2)*tau(f1)  -- {checked} pairs, all agree")
print("=> canonical composition (3.53) becomes the OPPOSITE product in tau-coordinates")
