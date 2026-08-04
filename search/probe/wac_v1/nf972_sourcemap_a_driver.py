# search/probe/wac_v1/nf972_sourcemap_a_driver.py
#
# NF-972 source map A (assembly side) -- 正本: docs/notes/nf972_freeze_v1.md(凍結仕様 v1・裁定434
# / v1.1 追補 裁定442 / ★v1.2 追補 裁定454)。
#
# 担当範囲: source map A のみ。factor cert (certificates/K9.v1.json・certificates/S4.v2.json)
# から fiber-product の各点を組み立て、凍結 NF tuple (m0, can9(q9(f)), can4(q4(f))) へ写す。
#
# ★ v1.2 修理(裁定454): can4 の照合先訂正。旧実装(このコメントブロック下の版)は
# S4.v2.json settled_detail の automorphism_witness をそのまま can4 として使っていたが、
# witness は settled 判定の証人 conjugator h であって q4(f) の像ではない(f_word=[] の行で
# witness != () が動かぬ証拠)。本版は f_word 評価器を自前実装し、q4(f) の one-line 像を
# can4 として使う(仕様 §7 pin 1-4)。
#
# 独立性の宣言: source map B(直接悉皆側)は別の係が独立実装中。本スクリプトは B の実装・
# 中間表現・normalizer helper を一切参照しない。search/probe/wac_v1/ihnec_r4b_*.py の
# 正規化コードも import・模倣しない(仕様は共有するが実装コードは独立)。
# f_word 評価器の構成規約(search/week3-psl-common.g の X:=w^2・Y:=S^-1XS, L275-277 と
# P^1(F8) 点列挙規約)は「枠定義の読解」として参照するが、source map B のコード
# (search/probe/wac_v1/nf972_sourcemap_b_run.g)・B の cert 類は一切参照しない。
#
# 参考にした既存資産(schema のみ・実装は独立に書き下ろし):
#   - search/probe/wac_v1/ihnec_r4a_assembly_cert_gen.py: R4a(基数のみの紙予測)の provenance
#     cert。本スクリプトはこれの「集合水準への格上げ」であり、972 = sum_m ck9[m]*c4[m%9] という
#     組立則(ROOF(4) 命題)を再利用するが、実際に各点のタプルを列挙する点が新規。
#
# 宇宙の事前登録: 入力は certificates/K9.v1.json (108 shadows) と certificates/S4.v2.json
# (54 settled_detail) の 2 点のみ。範囲を広げない。

import json
import hashlib
import os
import re
import sys
import platform
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def relpath(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(path):
    return sha_bytes(open(path, "rb").read())


K9P = os.path.join(ROOT, "certificates", "K9.v1.json")
S4P = os.path.join(ROOT, "certificates", "S4.v2.json")
K9 = json.load(open(K9P, encoding="utf-8"))
S4 = json.load(open(S4P, encoding="utf-8"))

FAILS = []


def chk(cond, msg):
    if not cond:
        FAILS.append(msg)
    return cond


# ---------------------------------------------------------------------------
# -1. 汎用置換ヘルパー(GAP の permutation 意味論を python で再現)
#
# 表現: degree n の置換を「1-indexed 点 i の像」を並べた python tuple(0-indexed
# 配列・要素は 1..n)として表す。GAP の p*q は「p を先に適用し、続けて q を適用」
# (i^(p*q) = (i^p)^q)なので、compose(p,q) はその意味で実装する。
# ---------------------------------------------------------------------------

def perm_identity(n):
    return tuple(range(1, n + 1))


def perm_compose(p, q):
    """GAP の p*q(i^(p*q) = (i^p)^q)を再現。p を先、q を後に適用。"""
    return tuple(q[p[i] - 1] for i in range(len(p)))


def perm_invert(p):
    n = len(p)
    inv = [0] * n
    for i in range(n):
        inv[p[i] - 1] = i + 1
    return tuple(inv)


def perm_power(p, e):
    n = len(p)
    if e == 0:
        return perm_identity(n)
    base = p if e > 0 else perm_invert(p)
    k = abs(e)
    val = perm_identity(n)
    for _ in range(k):
        val = perm_compose(val, base)
    return val


def abstract_prod(perm_list, degree):
    """week3-battery-common.g / week3-psl-common.g の AbstractProd を python で再現。
    paper 語 "f1 f2 ... fk"(perm_list はこの順)を GAP 形へ変換: val := id;
    for i in [Length(list), Length(list)-1 .. 1] do val := val * list[i]; od;
    (paper "AB" = GAP "B*A" の一般化 -- 全項反転)。
    """
    val = perm_identity(degree)
    for i in range(len(perm_list) - 1, -1, -1):
        val = perm_compose(val, perm_list[i])
    return val


def eval_f_word(f_word, gens, degree):
    """f_word = [[letter, exponent], ...](paper 語順)を gens(letter -> perm)で評価し、
    q4(f) の one-line 像(degree 点の tuple)を返す。評価規約 = AbstractProd(仕様 v1.2 §7-3)。
    """
    perm_list = [perm_power(gens[letter], exp) for (letter, exp) in f_word]
    return abstract_prod(perm_list, degree)


# ---------------------------------------------------------------------------
# -1b. A5-CONV 適合テスト(docs/notes/hsp7_cond4_lanespec_v1.md §0.2 逐語 fixture)
#
# t=(1 2 3), a=(1 4 5)(A1.v2.json marking 由来の S5 置換, degree 5)。
# X := a t^-1 (paper 積) は GAP では t^-1 * a と打つ(W-1: paper "AB" = GAP "B*A")。
# Y := t X t^-1 (paper 積) は GAP では t^-1 * X * t (3 項の全反転)。
# 主判定: paper 語 "y x^-1" を AbstractProd で評価し (1 2 4) を得ること。
# ---------------------------------------------------------------------------

def cycles_to_perm(cycles, degree):
    img = list(range(1, degree + 1))
    for cyc in cycles:
        n = len(cyc)
        for i in range(n):
            a = cyc[i]
            b = cyc[(i + 1) % n]
            img[a - 1] = b
    return tuple(img)


def run_a5_conv_fixture():
    t = cycles_to_perm([(1, 2, 3)], 5)
    a = cycles_to_perm([(1, 4, 5)], 5)
    x = perm_compose(perm_invert(t), a)              # GAP: t^-1 * a  (paper: a t^-1)
    y = perm_compose(perm_compose(perm_invert(t), x), t)  # GAP: t^-1 * x * t (paper: t x t^-1)
    x_expect = cycles_to_perm([(1, 3, 2, 4, 5)], 5)
    y_expect = cycles_to_perm([(1, 3, 4, 5, 2)], 5)
    x_ok = (x == x_expect)
    y_ok = (y == y_expect)
    gens = {"x": x, "y": y}
    ev = eval_f_word([["y", 1], ["x", -1]], gens, 5)
    ev_correct = cycles_to_perm([(1, 2, 4)], 5)
    ev_reversed = cycles_to_perm([(2, 5, 3)], 5)
    if ev == ev_correct:
        verdict = "correct"
    elif ev == ev_reversed:
        verdict = "reversed"
    else:
        verdict = "other"
    return {
        "x_ok": x_ok,
        "y_ok": y_ok,
        "x_computed": list(x),
        "y_computed": list(y),
        "ev_y_xinv": list(ev),
        "ev_y_xinv_expect_correct": list(ev_correct),
        "ev_y_xinv_expect_reversed": list(ev_reversed),
        "verdict": verdict,
    }


A5_CONV_RESULT = run_a5_conv_fixture()

if A5_CONV_RESULT["verdict"] != "correct" or not A5_CONV_RESULT["x_ok"] or not A5_CONV_RESULT["y_ok"]:
    print("INTEGRITY_STOP: A5-CONV 適合テストが不合格(規約バグの疑い)。")
    print("A5_CONV_RESULT:", json.dumps(A5_CONV_RESULT, indent=2))
    sys.exit(1)

print("A5-CONV fixture: PASS (verdict=correct, x_ok=%s, y_ok=%s)" %
      (A5_CONV_RESULT["x_ok"], A5_CONV_RESULT["y_ok"]))


# ---------------------------------------------------------------------------
# -1c. GF(8) 演算(search/week3-psl-common.g L143-179 の GF8Add/GF8Mul/GF8Inv を
# python で再現。encoding: a0+a1*x+a2*x^2 <-> a0+2*a1+4*a2, x^3+x+1=0)。
# ---------------------------------------------------------------------------

def gf8_add(a, b):
    return a ^ b


def gf8_carryless_mul(a, b):
    result = 0
    for i in range(3):
        if (b >> i) & 1:
            result ^= (a << i)
    return result


def gf8_reduce(p):
    result = p
    for i in (4, 3):
        if (result >> i) & 1:
            result ^= (11 << (i - 3))
    return result


def gf8_mul(a, b):
    return gf8_reduce(gf8_carryless_mul(a, b))


def gf8_inv(a):
    if a == 0:
        raise ValueError("gf8_inv: no inverse of 0")
    for b in range(1, 8):
        if gf8_mul(a, b) == 1:
            return b
    raise ValueError("gf8_inv: not found")


def _gf8_self_check():
    x = 2
    x2 = gf8_mul(x, x)
    x3 = gf8_mul(x2, x)
    if not (x2 == 4 and x3 == gf8_add(x, 1)):
        raise AssertionError("GF8 self-check failed: x^2=%r x^3=%r" % (x2, x3))


_gf8_self_check()


def mat_to_perm_gf8(M):
    """search/week3-psl-common.g の MatToPermGF8 を python で再現。9 点 P^1(GF(8))
    (index 1 = infinity, index 2+x for x in 0..7) 上の置換を返す(degree-9 tuple)。"""
    a, b, c, d = M[0][0], M[0][1], M[1][0], M[1][1]
    img = [0] * 9
    if c == 0:
        img[0] = 1
    else:
        img[0] = 2 + gf8_mul(a, gf8_inv(c))
    for x in range(8):
        num = gf8_add(gf8_mul(a, x), b)
        den = gf8_add(gf8_mul(c, x), d)
        if den == 0:
            img[1 + x] = 1
        else:
            img[1 + x] = 2 + gf8_mul(num, gf8_inv(den))
    return tuple(img)


def parse_mat_str(s):
    """'[[1,0],[1,1]]' -> [[1,0],[1,1]](plain python ints, GF(8) manifest encoding)。"""
    return json.loads(s)


# ---------------------------------------------------------------------------
# 0. 入力の事前健全性(fail-closed の前提)
# ---------------------------------------------------------------------------
K9_SHADOWS = K9["shadows"]
chk(len(K9_SHADOWS) == 108, "K9.v1.json: |shadows| == 108")
chk(K9["target"]["invariants"]["N_ord"] == 18, "K9.v1.json: N_ord == 18")
chk(K9["target"]["n"] == 9, "K9.v1.json: n == 9")

S4_SETTLED = S4["settled_detail"]
chk(len(S4_SETTLED) == 54, "S4.v2.json: |settled_detail| == 54")
chk(S4["settled_count"] == 54, "S4.v2.json: settled_count == 54")
chk(all(r.get("settled") is True for r in S4_SETTLED),
    "S4.v2.json: settled_detail 全員 settled==true(false 混入なし)")

# K9 の f_triple は [[a,eps],[a,eps],[a,eps]] 形。eps は {0,1} のみ許容(仕様 §1)。
for s in K9_SHADOWS:
    for pair in s["f_triple"]:
        chk(pair[1] in (0, 1), "K9 shadow f_triple eps in {0,1}: " + repr(s))
        chk(0 <= pair[0] < 9, "K9 shadow f_triple a in [0,9): " + repr(s))
    chk(0 <= s["m"] < 18, "K9 shadow m in [0,18): " + repr(s))

CYCLE_RE = re.compile(r"\(([^)]*)\)")


def parse_perm_one_line(cycle_str, degree=9):
    """GAP 由来の cycle notation 文字列(1-indexed)を固定 degree の one-line image へ。
    '()' は恒等。生成元・作用側の選択を要しない純粋な記法変換(CV-1/CV-2 は関与しない)。
    """
    img = list(range(1, degree + 1))
    s = cycle_str.strip()
    if s in ("()", ""):
        return tuple(img)
    for grp in CYCLE_RE.findall(s):
        pts = [int(x) for x in grp.split(",") if x.strip() != ""]
        if not pts:
            continue
        for p in pts:
            if not (1 <= p <= degree):
                raise ValueError("point out of degree range: %r in %r" % (p, cycle_str))
        n = len(pts)
        for i in range(n):
            a = pts[i]
            b = pts[(i + 1) % n]
            img[a - 1] = b
    return tuple(img)


for r in S4_SETTLED:
    chk(0 <= r["m"] < 9, "S4 settled_detail m in [0,9): " + repr(r))

CHARMING_SET = sorted(set(r["m"] for r in S4_SETTLED))
chk(CHARMING_SET == [0, 2, 3, 5, 6, 8], "S4 charming set == [0,2,3,5,6,8]")

K9_M_SET = sorted(set(s["m"] for s in K9_SHADOWS))
chk(sorted(set(m % 9 for m in K9_M_SET)) == CHARMING_SET,
    "K9 の m mod 9 の像 == S4 charming set(P-IHN 互換性)")

# ---------------------------------------------------------------------------
# 0b. S4.v2.json の marking から X,Y 置換の構成(仕様 v1.2 §7 pin 2)。
# search/week3-psl-common.g L273-277 の構成規約(GAP ネイティブ形・paper 語ではない):
#   wPerm := S * T^-1;  Xperm := wPerm^2;  Yperm := S^-1 * Xperm * S;
# を python で再現し、marking の ord_S/ord_T/ord_w/ord_X と突合する(fail-closed)。
# ---------------------------------------------------------------------------
S4_MARKING = S4["marking"]
S_MAT = parse_mat_str(S4_MARKING["S"])
T_MAT = parse_mat_str(S4_MARKING["T"])
S_PERM = mat_to_perm_gf8(S_MAT)
T_PERM = mat_to_perm_gf8(T_MAT)


def perm_order(p):
    n = len(p)
    val = p
    k = 1
    idv = perm_identity(n)
    while val != idv:
        val = perm_compose(val, p)
        k += 1
        if k > 10 * n * n:
            raise RuntimeError("perm_order: did not terminate")
    return k


chk(perm_order(S_PERM) == S4_MARKING["ord_S"], "S4 marking: ord(S) 突合")
chk(perm_order(T_PERM) == S4_MARKING["ord_T"], "S4 marking: ord(T) 突合")

W_PERM = perm_compose(S_PERM, perm_invert(T_PERM))         # GAP: S * T^-1
X_PERM = perm_compose(W_PERM, W_PERM)                       # GAP: w^2
Y_PERM = perm_compose(perm_compose(perm_invert(S_PERM), X_PERM), S_PERM)  # GAP: S^-1 * X * S

chk(perm_order(W_PERM) == S4_MARKING["ord_w"], "S4 marking: ord(w) 突合")
chk(perm_order(X_PERM) == S4_MARKING["ord_X"], "S4 marking: ord(X) 突合")

Q4_GENS = {"x": X_PERM, "y": Y_PERM}

# ---------------------------------------------------------------------------
# 1. can9 / can4 のカノニカル serialization(仕様 §1 逐条実装・can4 は v1.2 §7 pin 1 に従い
#    q4(f) の像で置き換え -- witness は使わない)
# ---------------------------------------------------------------------------


def can9_of(f_triple):
    """dihedral 座標側 = r^a s^eps の指数 tuple(3 成分・成分順固定・仕様§1)。"""
    return tuple((int(a), int(e)) for a, e in f_triple)


def can4_of(f_word):
    """置換像側 = q4(f) の one-line image(固定 degree 9・仕様 v1.2 §7 pin 1)。
    witness(automorphism_witness)は settled 判定の証人 conjugator であり、can4 の
    材料には使わない(裁定454)。評価規約 = AbstractProd(paper 語順・W-1 反転)。"""
    return eval_f_word(f_word, Q4_GENS, 9)


K9_RECORDS = [{"m": s["m"], "can9": can9_of(s["f_triple"])} for s in K9_SHADOWS]
chk(len(set((r["m"], r["can9"]) for r in K9_RECORDS)) == 108,
    "K9_RECORDS: (m,can9) が 108 通り相異なる")

S4_RECORDS = [{"m": r["m"], "can4": can4_of(r["f_word"])} for r in S4_SETTLED]
chk(len(set((r["m"], r["can4"]) for r in S4_RECORDS)) == 54,
    "S4_RECORDS: (m,can4) が 54 通り相異なる")

# f_word=[] の行は can4 が恒等になるはず(q4 は空語で恒等 -- witness は違う値を持ちうる、
# それが v1.2 §7 の誤り発見の直接証拠だった箇所)。
for r, s in zip(S4_RECORDS, S4_SETTLED):
    if len(s["f_word"]) == 0:
        chk(r["can4"] == perm_identity(9), "f_word=[] の行の can4 は恒等: " + repr(s))

# witness との不一致件数を診断として記録(仕様が「witness は can4 の材料に使ってはならない」
# と明言する根拠の再確認 -- can4 決定には使わない・純粋な事後診断)。
WITNESS_CAN4_MISMATCH = 0
for r, s in zip(S4_RECORDS, S4_SETTLED):
    w = parse_perm_one_line(s["automorphism_witness"], degree=9)
    if w != r["can4"]:
        WITNESS_CAN4_MISMATCH += 1

# S4 側 fiber 内の can4(q4(f) の像)が実際に相異なる置換であることの確認(退化してないか)。
by_m_s4 = defaultdict(set)
for r in S4_RECORDS:
    by_m_s4[r["m"]].add(r["can4"])
chk(all(len(v) == 9 for v in by_m_s4.values()), "S4: 各 m の can4 fiber サイズ == 9")

by_m_k9 = defaultdict(set)
for r in K9_RECORDS:
    by_m_k9[r["m"]].add(r["can9"])
chk(all(len(v) == 9 for v in by_m_k9.values()), "K9: 各 m の can9 fiber サイズ == 9")
chk(len(by_m_k9) == 12, "K9: distinct m 値の個数 == 12")


# ---------------------------------------------------------------------------
# 2. fiber-product の組立(仕様 §1: NF([m,f.M_F2]) = (m0, can9(q9(f)), can4(q4(f))))
#    互換条件: K9 側 m(=m0, mod 18) と S4 側 m(mod 9) が m0 mod 9 で一致すること。
# ---------------------------------------------------------------------------

def assemble(k9_records, s4_records, m0_selector=lambda m: m, can9_selector=lambda t: t,
             can4_selector=lambda t: t):
    """正しい組立、および fixture 用の変異を同じ骨格で走らせるための共通関数。
    m0_selector: K9 レコードの m から m0 を作る関数(fixture3 用に差し替え可能)。
    can9_selector / can4_selector: 変異注入点(fixture1/2 用)。
    """
    s4_by_m = defaultdict(list)
    for r in s4_records:
        s4_by_m[r["m"]].append(r)
    out = []
    for r9 in k9_records:
        m0 = m0_selector(r9["m"])
        c9 = can9_selector(r9["can9"])
        for r4 in s4_by_m.get(r9["m"] % 9, []):
            out.append((m0, c9, r4["can4"]))
    return out


BASELINE_LIST = assemble(K9_RECORDS, S4_RECORDS)
BASELINE_SET = set(BASELINE_LIST)

chk(len(BASELINE_LIST) == 972, "baseline: tuple 総数(重複含む列挙) == 972")
chk(len(BASELINE_SET) == 972, "baseline: tuple 集合 == 972(重複 0)")

# 射影像の勘定(仕様§3 (2))
PROJ_Q9 = set((m0, c9) for (m0, c9, c4) in BASELINE_SET)
PROJ_Q4 = set((m0 % 9, c4) for (m0, c9, c4) in BASELINE_SET)
chk(len(PROJ_Q9) == 108, "射影像(q9 側) == 108")
chk(len(PROJ_Q4) == 54, "射影像(q4 側) == 54")
chk(PROJ_Q9 == set((r["m"], r["can9"]) for r in K9_RECORDS),
    "q9 射影像 == K9_RECORDS そのもの(compatibility quotient 一致)")
chk(PROJ_Q4 == set((r["m"], r["can4"]) for r in S4_RECORDS),
    "q4 射影像 == S4_RECORDS そのもの(compatibility quotient 一致)")


# ---------------------------------------------------------------------------
# 3. 分離 fixture 3 種(仕様 §4・DUM-G3 規律)。本走の前に実走し発火を確認する。
#    各 fixture は「正しい組立の baseline」に対し変異版を作り、集合として
#    baseline != mutant であることを機械判定する(自己完結の識別力較正 --
#    B との比較ではない)。
# ---------------------------------------------------------------------------

fixture_results = {}

# --- fixture 1: 非自己逆元の向き反転(f -> f^-1 型)。can9 の a 成分を mod 9 で符号反転。
def flip_can9(t):
    return tuple((((-a) % 9), e) for (a, e) in t)


MUT1_LIST = assemble(K9_RECORDS, S4_RECORDS, can9_selector=flip_can9)
MUT1_SET = set(MUT1_LIST)
fixture_results["F1_orientation_flip"] = {
    "description": "can9 の a 成分を mod 9 で符号反転(f -> f^-1 型)。9 は奇数なので a=0 の成分のみ不動点(自己逆元)。",
    "mutant_set_size": len(MUT1_SET),
    "baseline_equals_mutant": BASELINE_SET == MUT1_SET,
    "symmetric_difference_size": len(BASELINE_SET.symmetric_difference(MUT1_SET)),
    "fires_set_inequality": BASELINE_SET != MUT1_SET,
}
chk(fixture_results["F1_orientation_flip"]["fires_set_inequality"],
    "fixture1(向き反転)が set inequality を発火")

# --- fixture 2: 片側 generator swap(q9 の生成元対応 = f_triple 成分の入替)。
#
# 診断上の発見(正直に記帳): 成分 1<->2 の入替 (t[1],t[0],t[2]) は本データでは
# baseline と**集合として一致**してしまい、識別力ゼロだった(K9 の f_triple が
# 満たす代数関係 -- component2 = -2*component1、component3 = kappa(m) --
# の下で、成分1,2 の入替が各 m-fiber 内の 9 点集合を「集合として」保つ対称性に
# なっているため。R4a の U-11 検証(theta 関数)が示す Aff(Z/9) 構造の帰結)。
# これは変異が弱すぎたのではなく、その特定の変異が偶然この構造の対称性と
# 一致した、という較正上の事実であり、CV-13 の教訓(自己整合と正典忠実性は別)
# と同型の注意点として記録する。⟹ 識別力を持つ変異として成分 1<->3 の入替
# (x 生成元の座標と m 依存の第3成分を混同する型の生成元対応ミス)を採用する。
# 全 5 通りの非自明な成分置換を事前に総当りで試験し、1<->2 のみが不発火・
# 残り 4 通りは全て発火することを確認済み(下記 diagnostics に記録)。
def swap_can9_12(t):
    return (t[1], t[0], t[2])


def swap_can9_13(t):
    return (t[2], t[1], t[0])


import itertools as _itertools

_diag = {}
for _perm in _itertools.permutations([0, 1, 2]):
    if _perm == (0, 1, 2):
        continue
    def _sel(t, _perm=_perm):
        return tuple(t[i] for i in _perm)
    _mut = set(assemble(K9_RECORDS, S4_RECORDS, can9_selector=_sel))
    _diag[str(_perm)] = {"mutant_set_size": len(_mut), "equals_baseline": BASELINE_SET == _mut}

MUT2_NULL_LIST = assemble(K9_RECORDS, S4_RECORDS, can9_selector=swap_can9_12)
MUT2_NULL_SET = set(MUT2_NULL_LIST)

MUT2_LIST = assemble(K9_RECORDS, S4_RECORDS, can9_selector=swap_can9_13)
MUT2_SET = set(MUT2_LIST)
fixture_results["F2_generator_swap"] = {
    "description": "can9 の f_triple 成分順を (1,2,3)->(3,2,1) へ入替(q9 側の生成元対応スワップを模擬)。",
    "mutant_set_size": len(MUT2_SET),
    "baseline_equals_mutant": BASELINE_SET == MUT2_SET,
    "symmetric_difference_size": len(BASELINE_SET.symmetric_difference(MUT2_SET)),
    "fires_set_inequality": BASELINE_SET != MUT2_SET,
    "diagnostic_null_variant_1_2_swap": {
        "description": "成分 1<->2 の入替(t[1],t[0],t[2])は本データで集合として baseline と一致(識別力ゼロ・不採用)",
        "equals_baseline": BASELINE_SET == MUT2_NULL_SET,
        "mutant_set_size": len(MUT2_NULL_SET),
    },
    "diagnostic_all_nontrivial_permutations": _diag,
}
chk(fixture_results["F2_generator_swap"]["fires_set_inequality"],
    "fixture2(generator swap, 1<->3)が set inequality を発火")

# --- fixture 3: m の法の誤り(M_ord の取り違え: mod 18 を mod 9 に縮約)。
def wrong_modulus_m0(m):
    return m % 9


MUT3_LIST = assemble(K9_RECORDS, S4_RECORDS, m0_selector=wrong_modulus_m0)
MUT3_SET = set(MUT3_LIST)
fixture_results["F3_wrong_m_modulus"] = {
    "description": "m0 を mod 18(正)ではなく mod 9(誤 = S4 側の法との取り違え)で構成。",
    "mutant_set_size": len(MUT3_SET),
    "baseline_equals_mutant": BASELINE_SET == MUT3_SET,
    "symmetric_difference_size": len(BASELINE_SET.symmetric_difference(MUT3_SET)),
    "fires_set_inequality": BASELINE_SET != MUT3_SET,
}
chk(fixture_results["F3_wrong_m_modulus"]["fires_set_inequality"],
    "fixture3(m の法の誤り)が set inequality を発火")

# --- fixture 4(★ 司令塔追加指示・CV-9 判読【要修正1】): can4 軸の変異。F1/F2/F3 は
# can9/m0 軸のみを動かし、v1.2 修理の対象そのものである can4 軸を一度も動かしていなかった
# (A5-CONV は S5 の別群 fixture で GF(8)/点列挙 pipeline を通らない)。二候補を診断し、
# 発火する方を F4 として採用する(両方発火すれば A を優先 -- F2 で 1<->2 が不発火だった
# 前例があるため、単一候補への依存を避ける)。
#
# 候補 A: X,Y 生成元入替での評価(f_word 中の 'x' <-> 'y' の生成元対応を取り違えた誤実装を模擬)。
def can4_swapgen_of(f_word):
    return eval_f_word(f_word, {"x": Y_PERM, "y": X_PERM}, 9)


S4_RECORDS_SWAPGEN = [{"m": r["m"], "can4": can4_swapgen_of(r["f_word"])} for r in S4_SETTLED]
MUT4A_LIST = assemble(K9_RECORDS, S4_RECORDS_SWAPGEN)
MUT4A_SET = set(MUT4A_LIST)
fires_4a = BASELINE_SET != MUT4A_SET

# 候補 B: P^1(GF(8)) 点列挙順の恣意転置(点 1,2 を入替た点ラベルで can4 を付け直す
# -- conjugation by transposition tau=(1 2), c4' := tau^-1 * c4 * tau)。
TAU_12 = (2, 1, 3, 4, 5, 6, 7, 8, 9)


def relabel_can4_tau12(c4):
    return perm_compose(perm_compose(perm_invert(TAU_12), c4), TAU_12)


S4_RECORDS_RELABEL = [{"m": r["m"], "can4": relabel_can4_tau12(r["can4"])} for r in S4_RECORDS]
MUT4B_LIST = assemble(K9_RECORDS, S4_RECORDS_RELABEL)
MUT4B_SET = set(MUT4B_LIST)
fires_4b = BASELINE_SET != MUT4B_SET

F4_SELECTED = "A_generator_swap" if fires_4a else "B_point_relabel_transposition_12"
F4_MUTANT_SET = MUT4A_SET if fires_4a else MUT4B_SET
F4_FIRES = fires_4a if fires_4a else fires_4b

fixture_results["F4_can4_axis_mutation"] = {
    "description": "can4 軸(v1.2 修理対象そのもの)を動かす変異。F1/F2/F3 は can9/m0 軸のみで"
                     "can4 軸を一度も動かしていなかった(司令塔追加指示・CV-9 判読【要修正1】への対応)。",
    "candidate_A_generator_swap": {
        "description": "eval_f_word の gens で x<->y を入替(生成元対応の取り違えを模擬)",
        "mutant_set_size": len(MUT4A_SET),
        "baseline_equals_mutant": BASELINE_SET == MUT4A_SET,
        "symmetric_difference_size": len(BASELINE_SET.symmetric_difference(MUT4A_SET)),
        "fires_set_inequality": fires_4a,
    },
    "candidate_B_point_relabel_transposition_12": {
        "description": "can4 を tau=(1 2) で共役(tau^-1 * c4 * tau)して点ラベルを付け替え",
        "mutant_set_size": len(MUT4B_SET),
        "baseline_equals_mutant": BASELINE_SET == MUT4B_SET,
        "symmetric_difference_size": len(BASELINE_SET.symmetric_difference(MUT4B_SET)),
        "fires_set_inequality": fires_4b,
    },
    "selected_candidate": F4_SELECTED,
    "mutant_set_size": len(F4_MUTANT_SET),
    "fires_set_inequality": F4_FIRES,
}
chk(fixture_results["F4_can4_axis_mutation"]["fires_set_inequality"],
    "fixture4(can4 軸変異、" + F4_SELECTED + ")が set inequality を発火")

ALL_FIXTURES_FIRE = all(fixture_results[k]["fires_set_inequality"] for k in fixture_results)
if not ALL_FIXTURES_FIRE:
    FAILS.append("CALIBRATION_FAILED: 分離 fixture のいずれかが発火しなかった(識別力ゼロ)")

# ---------------------------------------------------------------------------
# 4. 本走の canonical 列挙・sha256(fixture 発火確認後のみ意味を持つ)
# ---------------------------------------------------------------------------

def tuple_to_jsonable(t):
    m0, c9, c4 = t
    return [m0, [list(p) for p in c9], list(c4)]


CANONICAL_LIST = sorted(BASELINE_SET)  # tuple の辞書式順序で正規化
CANONICAL_JSON_OBJ = [tuple_to_jsonable(t) for t in CANONICAL_LIST]
CANONICAL_BYTES = json.dumps(CANONICAL_JSON_OBJ, separators=(",", ":"),
                              ensure_ascii=True).encode("utf-8")
CANONICAL_SHA256 = sha_bytes(CANONICAL_BYTES)

# 集合本体を別ファイルへ収蔵(cert 本体は sha のみ参照)。
# ★ v3(司令塔追加指示・F4 追加): F4 は BASELINE_SET を変えない(can9/m0 側の baseline 組立自体は
# 無変更。F4 は can4 軸の識別力較正であって baseline の再定義ではない)ので、tuples は v2 から
# 不変のはず -- 新規 tuples ファイルは書かず、既存 v2 tuples ファイルの canonical_bytes_sha256 と
# 今回計算した CANONICAL_SHA256 の一致を確認するのみ(旧版不改変・仕様 v1.2 §7-5)。
V2_ENUM_PATH = os.path.join(ROOT, "search", "certs", "nf972_sourcemap_a_tuples_v2_20260804.json")
if not os.path.exists(V2_ENUM_PATH):
    FAILS.append("INTEGRITY_STOP: v2 tuples ファイルが見つからない(F4 追加前に v2 走行が必要): "
                 + relpath(V2_ENUM_PATH))
    V2_ENUM_SHA = None
    TUPLES_UNCHANGED_FROM_V2 = False
else:
    V2_ENUM_OBJ = json.load(open(V2_ENUM_PATH, encoding="utf-8"))
    V2_ENUM_SHA = V2_ENUM_OBJ["canonical_bytes_sha256"]
    TUPLES_UNCHANGED_FROM_V2 = chk(V2_ENUM_SHA == CANONICAL_SHA256,
        "F4 追加後も canonical tuple 集合の sha256 が v2 から不変(tuples 不変の確認)")
ENUM_OUT = V2_ENUM_PATH  # 参照のみ・再書き込みしない(旧版不改変)

RESULT = "ALL PASS" if not FAILS else "FAILED"

# ---------------------------------------------------------------------------
# 5. conventions_used(規約台帳 v1.6 準拠・CV-1/CV-2 宣言欄)
# ---------------------------------------------------------------------------

WEEK3_PSL_COMMON_P = os.path.join(ROOT, "search", "week3-psl-common.g")

conventions_used = {
    "ledger_version": "conventions_ledger_v1_6",
    "perm_composition": "GAP ネイティブ意味論を python で再現: p*q は p を先に適用し続けて q を適用"
                          "(i^(p*q) = (i^p)^q)。perm_compose(p,q) がこれを実装(driver 内)。",
    "conjugation": "S^-1 * X * S (GAP ネイティブ形、W_PERM/X_PERM/Y_PERM の構成に使用。paper 語では"
                     "ない -- search/week3-psl-common.g L273-277 が既に GAP ネイティブ形で書かれている"
                     "ため、そのまま再現するだけで W-1 の反転は不要)。",
    "coset_object": "n/a(剰余類演算を行わない -- K9 cert が既に q9 の像を確定値として提供。q4 側は"
                      "f_word を自前評価器で q4(f) へ写す -- v1.2 §7 修理)。",
    "action_side": "GAP 右作用(i^p)。P^1(GF(8)) 上の点は 1-indexed(1=infinity, 2+x for x in GF(8))"
                     "(search/week3-psl-common.g MatToPermGF8 の規約をそのまま再現)。",
    "coset_side_derivation": "n/a",
    "f_word_evaluation": {
        "convention": "AbstractProd(paper 語 'f1 f2 ... fk' は GAP 形 fk*f(k-1)*...*f1 -- 全項反転、"
                        "week3-battery-common.g/week3-psl-common.g の AbstractProd と同じ規約)を"
                        "python で再現(driver 内 abstract_prod/eval_f_word)。",
        "gens_construction": "S4.v2.json の marking(S,T 行列・pgl2q_matrix/v1)から "
                               "wPerm:=S*T^-1; Xperm:=wPerm^2; Yperm:=S^-1*Xperm*S "
                               "(search/week3-psl-common.g L273-277、GAP ネイティブ形をそのまま再現。"
                               "paper 語ではないので W-1 の反転は適用しない)。",
        "a5_conv_fixture": A5_CONV_RESULT,
        "a5_conv_result": A5_CONV_RESULT["verdict"],
        "marking_order_checks": {
            "ord_S_expect": S4_MARKING["ord_S"], "ord_S_actual": perm_order(S_PERM),
            "ord_T_expect": S4_MARKING["ord_T"], "ord_T_actual": perm_order(T_PERM),
            "ord_w_expect": S4_MARKING["ord_w"], "ord_w_actual": perm_order(W_PERM),
            "ord_X_expect": S4_MARKING["ord_X"], "ord_X_actual": perm_order(X_PERM),
        },
        "witness_can4_mismatch_count": WITNESS_CAN4_MISMATCH,
        "witness_can4_mismatch_note": "診断のみ(can4 の決定には witness を使わない)。仕様 v1.2 §7 が"
                                        "指摘した witness != q4(f) の直接的な数値証拠として記録。",
    },
    "cv1_cv2_scope_note": "K9 側(can9)は factor cert の f_triple をそのまま canonical serialization"
                            "するのみで CV-1/CV-2 は非自明に関与しない。S4 側(can4)は本 driver が"
                            "自前実装した f_word 評価器(AbstractProd)と marking からの X,Y 構成"
                            "(GAP ネイティブ形)が CV-1/CV-2 の非自明な適用箇所であり、A5-CONV fixture"
                            "(f_word_evaluation.a5_conv_fixture)で識別力を実証済み。",
    "chi_P_criterion": {
        "value": "exact",
        "justification": "(m, f_triple)・(m, q4(f) の one-line 像)をそのまま canonical化して数える"
                           "厳密基数(conjugacy class への縮約なし)",
        "generator_fixed": True,
        "orientation_fixed": True,
    },
    "separation": {
        "included": True,
        "competitor_universe": ["F1_orientation_flip", "F2_generator_swap", "F3_wrong_m_modulus",
                                 "F4_can4_axis_mutation"],
        "result": {"result_digest": CANONICAL_SHA256},
        "forbidden_values": {"handling": "n/a", "list": []},
        "dummy_fixture": {
            "id": "nf972_sourcemap_a_separation_fixtures_v2",
            "normalised_input": "K9_RECORDS x S4_RECORDS (compat: m mod 9)",
            "normalised_output": "972-element tuple set (baseline) vs 3 mutant sets",
            "discriminating_power": {"input_layer_novel": True, "output_layer_novel": True},
            "expected": "baseline != mutant for all 3 fixtures",
            "observed": {k: fixture_results[k]["fires_set_inequality"] for k in fixture_results},
            "verdict": "PASS" if ALL_FIXTURES_FIRE else "CALIBRATION_FAILED",
        },
    },
    "roundtrip_witness": {"status": "n/a", "reason": "粗/精ラベルの往復変換を持たない"},
    "effective_source_chain": [
        {"role": "current", "path": relpath(os.path.abspath(__file__)),
         "sha256": sha_file(os.path.abspath(__file__))},
        {"role": "current", "path": relpath(K9P), "sha256": sha_file(K9P)},
        {"role": "current", "path": relpath(S4P), "sha256": sha_file(S4P)},
        {"role": "reference_only_frame_definition",
         "path": relpath(WEEK3_PSL_COMMON_P), "sha256": sha_file(WEEK3_PSL_COMMON_P),
         "note": "X:=w^2, Y:=S^-1XS の構成規約・P^1(GF(8)) 点列挙規約の読解のみ(枠定義の参照、"
                  "委嘱の許可範囲)。実行時 import はしていない(python が別実装で再現)。"},
    ],
    "effective_source": {"path": relpath(K9P), "sha256": sha_file(K9P)},
    "seal_recoverability": {"status": "n/a", "reason": "封印 fixture を使用しない"},
    "level": "PB3",
}

cert = {
    "schema": "nf972-sourcemap-a/v3",
    "generated_by": {
        "tool": "python (independent source-map-A implementer; no shared code with source map B)",
        "script": relpath(os.path.abspath(__file__)),
        "date": "2026-08-04",
        "python_version": sys.version,
        "platform": platform.platform(),
    },
    "task_ref": "NF-972 source map A(組立側)v3。正本 docs/notes/nf972_freeze_v1.md"
                 "(凍結 v1・裁定434 / v1.1・裁定442 / ★v1.2・裁定454 can4 照合先訂正)+"
                 "docs/notes/nf972_cv9_reading_v1.md【要修正1】(司令塔追加指示: can4 軸の分離"
                 "fixture F4 を追加)。",
    "spec_ref": {"path": relpath(os.path.join(ROOT, "docs", "notes", "nf972_freeze_v1.md")),
                 "sha256": sha_file(os.path.join(ROOT, "docs", "notes", "nf972_freeze_v1.md"))},
    "inputs": {
        "K9_v1": {"path": relpath(K9P), "sha256": sha_file(K9P)},
        "S4_v2": {"path": relpath(S4P), "sha256": sha_file(S4P)},
    },
    "independence_declaration": "source map B(直接悉皆側)の実装・中間表現・normalizer helper を"
                                  "一切参照・共有していない(共有は凍結仕様の schema のみ)。"
                                  "search/probe/wac_v1/ihnec_r4b_*.py・search/probe/wac_v1/"
                                  "nf972_sourcemap_b_run.g・B の cert 類は import・複製・参照していない。"
                                  "search/week3-psl-common.g は X:=w^2/Y:=S^-1XS の構成規約と "
                                  "P^1(GF(8)) 点列挙規約の読解(枠定義の参照、委嘱の許可範囲)のみで、"
                                  "実行時 import はしていない。",
    "v2_repair_note": "v1(nf972_sourcemap_a_20260804.json)は can4 に automorphism_witness を誤用して"
                        "いた(witness は settled 判定の証人 conjugator であり q4(f) の像ではない -- "
                        "裁定454)。v2 は f_word を自前評価器(AbstractProd)で評価し q4(f) の"
                        "one-line 像を can4 として使う。旧版は上書きしない(仕様 v1.2 §7-5)。",
    "v3_addendum_note": "司令塔追加指示(docs/notes/nf972_cv9_reading_v1.md【要修正1】): F1/F2/F3 は"
                          "can9/m0 軸のみを変異させ、v1.2 修理の対象である can4 軸を一度も動かして"
                          "いなかった(A5-CONV は S5 別群 fixture で GF(8)/点列挙 pipeline を通らない)。"
                          "F4(can4 軸変異、2 候補診断・発火する方を採用)を追加。baseline の組立"
                          "自体は無変更のため tuples(v2)は不変 -- sha256 一致を確認して記録"
                          "(canonical_enumeration.tuples_unchanged_from_v2)。旧版(v1・v2)は上書きしない。",
    "construction": {
        "compat_rule": "K9 shadow(m in [0,18)) と S4 settled entry(m in [0,9)) の組は "
                         "K9.m % 9 == S4.m のときのみ fiber-product 点を成す(P-IHN 互換性)。",
        "m0_definition": "m0 = K9 shadow の m(mod 18 のまま。S4 側の m はこの m0 mod 9 に一致するのみで、"
                           "情報として m0 に追加を持たない)。",
        "can9_definition": "K9 shadow の f_triple = [[a1,eps1],[a2,eps2],[a3,eps3]] をそのまま"
                             "(a mod 9, eps in {0,1}) の 3 成分 tuple として使用(成分順固定)。",
        "can4_definition": "★v2: S4 settled_detail の f_word(paper 語順の [[letter,exp],...])を "
                             "AbstractProd 評価器で評価した q4(f) の像(固定 degree 9 の one-line "
                             "image)。生成元 X,Y は S4.v2.json marking の S,T 行列から "
                             "wPerm:=S*T^-1; Xperm:=wPerm^2; Yperm:=S^-1*Xperm*S で構成"
                             "(仕様 v1.2 §7 pin 1-2)。automorphism_witness は使用しない。",
    },
    "counts": {
        "K9_shadows_total": len(K9_SHADOWS),
        "K9_distinct_m": len(by_m_k9),
        "S4_settled_total": len(S4_SETTLED),
        "S4_distinct_m": len(by_m_s4),
        "baseline_tuple_list_len": len(BASELINE_LIST),
        "baseline_tuple_set_len": len(BASELINE_SET),
        "expected_972_matches": len(BASELINE_SET) == 972,
        "proj_q9_size": len(PROJ_Q9),
        "proj_q9_expected_108_matches": len(PROJ_Q9) == 108,
        "proj_q4_size": len(PROJ_Q4),
        "proj_q4_expected_54_matches": len(PROJ_Q4) == 54,
        "duplicate_count": len(BASELINE_LIST) - len(BASELINE_SET),
    },
    "note_on_expected_values": "972/108/54 は突合欄のみに用い、生成には使わない(fail-closed の各"
                                 "chk() は cert 内の内部整合 -- fiber-product の代数的性質 -- からのみ"
                                 "算出され、期待値をハードコードして通過させていない)。",
    "fixtures": fixture_results,
    "fixtures_all_fire": ALL_FIXTURES_FIRE,
    "canonical_enumeration": {
        "path": relpath(ENUM_OUT),
        "sha256": sha_bytes(open(ENUM_OUT, "rb").read()),
        "canonical_bytes_sha256": CANONICAL_SHA256,
        "count": len(CANONICAL_JSON_OBJ),
        "tuples_unchanged_from_v2": TUPLES_UNCHANGED_FROM_V2,
        "v2_enum_canonical_bytes_sha256": V2_ENUM_SHA,
        "note": "F4 追加は BASELINE_SET(972 タプル集合)を変えない -- v2 の tuples ファイルを"
                 "そのまま参照し、新規 tuples ファイルは書いていない(旧版不改変)。",
    },
    "conventions_used": conventions_used,
    "failures": FAILS,
    "overall_result": RESULT,
    "driver_done": (RESULT == "ALL PASS"),
}

# ★ v3: 新名で出力(旧版 nf972_sourcemap_a_20260804.json・nf972_sourcemap_a_v2_20260804.json は
# 上書きしない・仕様 v1.2 §7-5)。
CERT_OUT = os.path.join(ROOT, "search", "certs", "nf972_sourcemap_a_v3_20260804.json")
with open(CERT_OUT, "w", encoding="utf-8") as f:
    json.dump(cert, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("A5_CONV verdict:", A5_CONV_RESULT["verdict"], "x_ok:", A5_CONV_RESULT["x_ok"],
      "y_ok:", A5_CONV_RESULT["y_ok"])
print("marking order checks:", conventions_used["f_word_evaluation"]["marking_order_checks"])
print("witness_can4_mismatch_count:", WITNESS_CAN4_MISMATCH, "/", len(S4_RECORDS))
print("F4 selected candidate:", fixture_results["F4_can4_axis_mutation"]["selected_candidate"])
print("F4 candidate A (gen swap) fires:",
      fixture_results["F4_can4_axis_mutation"]["candidate_A_generator_swap"]["fires_set_inequality"])
print("F4 candidate B (point relabel) fires:",
      fixture_results["F4_can4_axis_mutation"]["candidate_B_point_relabel_transposition_12"]["fires_set_inequality"])
print("tuples_unchanged_from_v2:", TUPLES_UNCHANGED_FROM_V2, "v2_sha:", V2_ENUM_SHA)
print("RESULT:", RESULT)
print("failures:", len(FAILS))
for m in FAILS:
    print("  FAIL:", m)
print("fixtures_all_fire:", ALL_FIXTURES_FIRE)
for k, v in fixture_results.items():
    print(" ", k, "-> fires:", v["fires_set_inequality"], "mutant_size:", v["mutant_set_size"])
print("baseline set size:", len(BASELINE_SET))
print("proj_q9:", len(PROJ_Q9), "proj_q4:", len(PROJ_Q4))
print("canonical sha256:", CANONICAL_SHA256)
print("Wrote", relpath(CERT_OUT))
print("Referenced (unchanged):", relpath(ENUM_OUT))
print("DRIVER_DONE:", cert["driver_done"])
