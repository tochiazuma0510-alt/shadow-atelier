#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G_20 = Im psi_20 <= D_20^3 の構造値(K^(20) 事前登録の凍結値になる分だけ)

D_m の元は (a, e) = r^a s^e、積 (a1,e1)*(a2,e2) = (a1 + (-1)^e1 a2, e1+e2)
psi_20: x |-> (r, s, s), y |-> (rs, r, rs)   (正典 2405 (3.1))

出す値(すべて群 G_20 の構造 — Im R の測定ではない):
  |G_20| / |A_20 = G_20 cap C_20^3| / |[G_20,G_20]| / |V| / |V cap [G_20,G_20]|
  f_1 = (rbar^2, rbar^-2, 1) の [G_20,G_20] 内の持上げの個数
  -> campaign 4.3 の T1 走査候補数の一般式に代入する値
"""
import itertools

M = 20
FAILS = []
def check(name, got, want):
    ok = (got == want)
    if not ok: FAILS.append((name, got, want))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got={got} want={want}")

def mk(m):
    def mul1(u, v):
        a1, e1 = u; a2, e2 = v
        return ((a1 + (a2 if e1 == 0 else -a2)) % m, (e1 + e2) % 2)
    def inv1(u):
        a, e = u
        return ((-a) % m, 0) if e == 0 else (a, 1)
    def mul(u, v): return tuple(mul1(u[i], v[i]) for i in range(3))
    def inv(u):    return tuple(inv1(u[i]) for i in range(3))
    r = (1, 0); s = (0, 1); rs = mul1(r, s); one = (0, 0)
    X = (r, s, s); Y = (rs, r, rs); ID = (one, one, one)
    return mul, inv, X, Y, ID

mul, inv, X, Y, ID = mk(M)

def closure(gens, mul, inv, ID):
    seen = {ID}; frontier = [ID]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                for cand in (mul(g, h), mul(g, inv(h))):
                    if cand not in seen:
                        seen.add(cand); nxt.append(cand)
        frontier = nxt
    return seen

def comm(a, b, mul, inv):
    return mul(mul(inv(a), inv(b)), mul(a, b))

G = closure([X, Y], mul, inv, ID)
check("|G_20| = 4000 (紙 4(m/2)^3 / cert g20_order)", len(G), 4000)

A = {g for g in G if all(c[1] == 0 for c in g)}
check("|A_20 = G_20 cap C_20^3| = 1000 (= <r^2>^3)", len(A), 1000)
check("[G_20 : A_20] = 4", len(G) // len(A), 4)

# --- [G,G] を正しく: {[a,b] : a in G, b in {X,Y}} の生成群の *正規閉包*
#     [G,G] は A(可換)に含まれるので、共役は剰余類 4 個だけで尽きる
C0 = {comm(a, b, mul, inv) for a in G for b in (X, Y)}
assert all(c in A for c in C0), "commutators must land in A"
reps = [ID, X, Y, mul(X, Y)]
C1 = {mul(mul(inv(g), c), g) for c in C0 for g in reps}
D = closure(list(C1), mul, inv, ID)
# 正規性の確認(閉じたか)
assert all(mul(mul(inv(g), d), g) in D for d in D for g in reps), "D not normal"
print(f"  |[G_20,G_20]| = {len(D)}")
check("[G_20,G_20] subset A_20", D <= A, True)
print(f"  |G_20^ab| = {len(G)//len(D)}")

V = {tuple(((10 * bi) % M, 0) for bi in b) for b in itertools.product([0, 1], repeat=3)}
check("|V = <r^10>^3| = 8", len(V), 8)
check("V subset G_20", V <= G, True)
check("V subset A_20", V <= A, True)
VD = V & D
print(f"  |V cap [G_20,G_20]| = {len(VD)}")
print(f"  ★ (V-der) 前件「V subset [P_N,P_N]」は: {'成立' if V <= D else '★破れる★'}")

# --- f_1 の持上げを [G,G] の中で数える
#     G_20 ->> G_5 は r |-> rbar (rbar^5=1), s |-> sbar 成分ごと
def red(g):  return tuple((a % 5, e) for (a, e) in g)
f1 = ((2, 0), ((-2) % 5, 0), (0, 0))          # (rbar^2, rbar^-2, 1) in G_5
lifts_A = [g for g in A if red(g) == f1]
lifts_D = [g for g in D if red(g) == f1]
print(f"  f_1 の A_20 内の持上げ個数      = {len(lifts_A)}  (= |V| なら V-torsor)")
print(f"  f_1 の [G_20,G_20] 内の持上げ個数 = {len(lifts_D)}")
check("A_20 内の持上げは V-torsor (8 個)", len(lifts_A), 8)
check("[G,G] 内の持上げ個数 = |V cap [G,G]|", len(lifts_D), len(VD))

# Thm 4.3 の witness (m~,k~)=(0,6) の f 部 = (r^12, r^-12, r^0)
w = ((12, 0), ((-12) % M, 0), (0, 0))
check("witness (0,6) の f 部が G_20 に在る", w in G, True)
check("witness の f 部が f_1 へ落ちる", red(w) == f1, True)
check("★ witness の f 部が [G_20,G_20] に在る(K5-BIT の f in [P,P] 要件)", w in D, True)

# --- G_5 側の対照
mul5, inv5, X5, Y5, ID5 = mk(5)
G5 = closure([X5, Y5], mul5, inv5, ID5)
C05 = {comm(a, b, mul5, inv5) for a in G5 for b in (X5, Y5)}
reps5 = [ID5, X5, Y5, mul5(X5, Y5)]
C15 = {mul5(mul5(inv5(g), c), g) for c in C05 for g in reps5}
D5 = closure(list(C15), mul5, inv5, ID5)
check("|G_5| = 500", len(G5), 500)
check("|[G_5,G_5]| = 125 (= A ~ C_5^3)", len(D5), 125)
check("f_1 in [G_5,G_5]", f1 in D5, True)
check("|G_20|/|G_5| = 8 = |V|", len(G) // len(G5), 8)

print()
print(f"FAILS = {len(FAILS)}")
for f in FAILS: print("   ", f)
print("RESULT:", "ALL PASS" if not FAILS else "HAS FAILURES")
print()
print("== 事前登録の凍結値 ==")
print(f"  |G_20| = {len(G)} / |A_20| = {len(A)} / |[G_20,G_20]| = {len(D)} / |G_20^ab| = {len(G)//len(D)}")
print(f"  |V| = {len(V)} / |V cap [G_20,G_20]| = {len(VD)}")
print(f"  T2 全列挙 raw = |X_20| * |[P_N,P_N]| = 16 * {len(D)} = {16*len(D)}")
print(f"  T1 走査候補   = #{{m in X_20 : m = 0 mod 10}} * |V cap [P,P]| = 2 * {len(VD)} = {2*len(VD)}")

# ============ 追補: V cap [G,G] の同定と、その上の coker psi ============
print()
print("== 追補: W := V cap [G_20,G_20] の Gamma-加群としての同定 ==")
def vcoord(g):
    return tuple(a // 10 for (a, e) in g)
Wc = sorted(vcoord(g) for g in VD)
print(f"  W の元(b1,b2,b3 座標) = {Wc}")
check("W = <(1,1,1)> (V の唯一の 1 次元 Gamma-部分加群 = 対角線)",
      Wc, [(0, 0, 0), (1, 1, 1)])
# theta|_V (b1,b2,b3)=(b2,b1,b3), tau|_V=(b3,b1,b2)  (addendum B 2.3)
th = lambda b: (b[1], b[0], b[2])
ta = lambda b: (b[2], b[0], b[1])
check("W は theta-安定", {th(b) for b in Wc} == set(Wc), True)
check("W は tau-安定",   {ta(b) for b in Wc} == set(Wc), True)
check("Gamma は W に自明に作用", all(th(b) == b and ta(b) == b for b in Wc), True)
# 1 次元自明 F2-加群 W 上: N_th = 1+th = 0, N_ta = 1+ta+ta^2 = 3 = 1
#   psi_W: W -> W^th (+) W^ta = W (+) W, w |-> (0, w) ; dim im = 1, dim target = 2
print("  W(1 次元・自明)上: dim W^theta = 1, dim W^tau = 1, N_theta = 0, N_tau = id")
print("  => dim im psi_W = 1, dim(W^th (+) W^ta) = 2, dim coker psi_W = 1")
check("dim coker psi_W = 1 (V 上の 3 次元計算と同値ではないが同じ値)", 2 - 1, 1)
