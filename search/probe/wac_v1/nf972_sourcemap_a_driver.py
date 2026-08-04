# search/probe/wac_v1/nf972_sourcemap_a_driver.py
#
# NF-972 source map A (assembly side) -- 正本: docs/notes/nf972_freeze_v1.md(凍結仕様 v1・裁定434)。
#
# 担当範囲: source map A のみ。factor cert (certificates/K9.v1.json・certificates/S4.v2.json)
# から fiber-product の各点を組み立て、凍結 NF tuple (m0, can9(q9(f)), can4(q4(f))) へ写す。
#
# 独立性の宣言: source map B(直接悉皆側)は別の係が独立実装中。本スクリプトは B の実装・
# 中間表現・normalizer helper を一切参照しない。search/probe/wac_v1/ihnec_r4b_*.py の
# 正規化コードも import・模倣しない(仕様は共有するが実装コードは独立)。
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
# 1. can9 / can4 のカノニカル serialization(仕様 §1 逐条実装)
# ---------------------------------------------------------------------------


def can9_of(f_triple):
    """dihedral 座標側 = r^a s^eps の指数 tuple(3 成分・成分順固定・仕様§1)。"""
    return tuple((int(a), int(e)) for a, e in f_triple)


def can4_of(witness):
    """置換像側 = 固定 degree(9)・固定生成元(points 1..9)・one-line image(仕様§1)。"""
    return parse_perm_one_line(witness, degree=9)


K9_RECORDS = [{"m": s["m"], "can9": can9_of(s["f_triple"])} for s in K9_SHADOWS]
chk(len(set((r["m"], r["can9"]) for r in K9_RECORDS)) == 108,
    "K9_RECORDS: (m,can9) が 108 通り相異なる")

S4_RECORDS = [{"m": r["m"], "can4": can4_of(r["automorphism_witness"])} for r in S4_SETTLED]
chk(len(set((r["m"], r["can4"]) for r in S4_RECORDS)) == 54,
    "S4_RECORDS: (m,can4) が 54 通り相異なる")

# S4 側 fiber 内の witness が実際に相異なる置換であることの確認(退化してないか)。
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
ENUM_OUT = os.path.join(ROOT, "search", "certs", "nf972_sourcemap_a_tuples_20260804.json")
with open(ENUM_OUT, "w", encoding="utf-8") as f:
    json.dump({
        "schema": "nf972-sourcemap-a-tuples/v1",
        "note": "canonical sorted enumeration of the 972-element tuple set (source map A). sha256 of the canonical bytes below is recorded in the main cert.",
        "canonicalization": "json.dumps(list_of_[m0,[[a,eps],[a,eps],[a,eps]],[img1..img9]], separators=(',',':'), ensure_ascii=True), list sorted by python tuple order",
        "count": len(CANONICAL_JSON_OBJ),
        "canonical_bytes_sha256": CANONICAL_SHA256,
        "tuples": CANONICAL_JSON_OBJ,
    }, f, ensure_ascii=True, indent=None, separators=(",", ":"))
    f.write("\n")

RESULT = "ALL PASS" if not FAILS else "FAILED"

# ---------------------------------------------------------------------------
# 5. conventions_used(規約台帳 v1.6 準拠・CV-1/CV-2 宣言欄)
# ---------------------------------------------------------------------------

conventions_used = {
    "ledger_version": "conventions_ledger_v1_6",
    "perm_composition": "n/a(本スクリプトは permutation の合成を行わない -- can4 は cycle notation を\n"
                          "one-line image へ変換する単一の記法変換であり、複数 permutation の積は取らない)",
    "conjugation": "n/a(共役演算を行わない)",
    "coset_object": "n/a(剰余類演算を行わない -- K9/S4 cert が既に q9,q4 の像を確定値として提供)",
    "action_side": "n/a(単一 permutation の cycle-notation 読み取りのみ。作用側の選択に依存しない)",
    "coset_side_derivation": "n/a",
    "cv1_cv2_scope_note": "source map A は factor cert(K9.v1.json/S4.v2.json)が既に計算済みの"
                            "(m, f_triple)・(m, automorphism_witness) を canonical serialization"
                            "するだけであり、GAP 側の合成順序・作用側規約を新たに適用する箇所を持たない。"
                            "CV-1/CV-2 が非自明に関与するのは factor cert 自体の生成(K9.v1.json/"
                            "S4.v2.json 側)であって、本 source map A の組立ではない。",
    "chi_P_criterion": {
        "value": "exact",
        "justification": "(m, f_triple)・(m, automorphism_witness) をそのまま canonical化して数える厳密基数(conjugacy class への縮約なし)",
        "generator_fixed": True,
        "orientation_fixed": True,
    },
    "separation": {
        "included": True,
        "competitor_universe": ["F1_orientation_flip", "F2_generator_swap", "F3_wrong_m_modulus"],
        "result": {"result_digest": CANONICAL_SHA256},
        "forbidden_values": {"handling": "n/a", "list": []},
        "dummy_fixture": {
            "id": "nf972_sourcemap_a_separation_fixtures_v1",
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
    ],
    "effective_source": {"path": relpath(K9P), "sha256": sha_file(K9P)},
    "seal_recoverability": {"status": "n/a", "reason": "封印 fixture を使用しない"},
    "level": "PB3",
}

cert = {
    "schema": "nf972-sourcemap-a/v1",
    "generated_by": {
        "tool": "python (independent source-map-A implementer; no shared code with source map B)",
        "script": relpath(os.path.abspath(__file__)),
        "date": "2026-08-04",
        "python_version": sys.version,
        "platform": platform.platform(),
    },
    "task_ref": "NF-972 source map A(組立側)。正本 docs/notes/nf972_freeze_v1.md(凍結 v1・裁定434)。",
    "spec_ref": {"path": relpath(os.path.join(ROOT, "docs", "notes", "nf972_freeze_v1.md")),
                 "sha256": sha_file(os.path.join(ROOT, "docs", "notes", "nf972_freeze_v1.md"))},
    "inputs": {
        "K9_v1": {"path": relpath(K9P), "sha256": sha_file(K9P)},
        "S4_v2": {"path": relpath(S4P), "sha256": sha_file(S4P)},
    },
    "independence_declaration": "source map B(直接悉皆側)の実装・中間表現・normalizer helper を"
                                  "一切参照・共有していない(共有は凍結仕様の schema のみ)。"
                                  "search/probe/wac_v1/ihnec_r4b_*.py のコードは import・複製していない。",
    "construction": {
        "compat_rule": "K9 shadow(m in [0,18)) と S4 settled entry(m in [0,9)) の組は "
                         "K9.m % 9 == S4.m のときのみ fiber-product 点を成す(P-IHN 互換性)。",
        "m0_definition": "m0 = K9 shadow の m(mod 18 のまま。S4 側の m はこの m0 mod 9 に一致するのみで、"
                           "情報として m0 に追加を持たない)。",
        "can9_definition": "K9 shadow の f_triple = [[a1,eps1],[a2,eps2],[a3,eps3]] をそのまま"
                             "(a mod 9, eps in {0,1}) の 3 成分 tuple として使用(成分順固定)。",
        "can4_definition": "S4 settled_detail の automorphism_witness(GAP cycle notation, 1-indexed, "
                             "points 1..9)を固定 degree 9 の one-line image へ変換。",
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
    },
    "conventions_used": conventions_used,
    "failures": FAILS,
    "overall_result": RESULT,
    "driver_done": (RESULT == "ALL PASS"),
}

CERT_OUT = os.path.join(ROOT, "search", "certs", "nf972_sourcemap_a_20260804.json")
with open(CERT_OUT, "w", encoding="utf-8") as f:
    json.dump(cert, f, ensure_ascii=False, indent=2)
    f.write("\n")

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
print("Wrote", relpath(ENUM_OUT))
print("DRIVER_DONE:", cert["driver_done"])
