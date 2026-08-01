#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C2-Q calibration stage (裁定380 / docs/notes/fake_void_v1.md A.4 / docs/scout/覚書_fvl1_20260801.md).

Scope (calibration ONLY -- probe stage is separately gated, NOT run here):
  Population = K^(3) の 12 元(certificates/K3.v1.json)+ N_A の 20 元(certificates/A1.v2.2.json) = 32 元。
  Both windows are THEOREM-covered arithmetical (定理K3 / 定理A5), so the relation
  lambda^2 = 24*c2(f) + 1 is PREDICTED to hold for all 32 -- this script does not assert
  that prediction in code, it only computes and records the observed values (接触遮断).

c2(f) definition (逐語 from docs/scout/覚書_fvl1_20260801.md 型(i)/(ii) and
docs/notes/fake_void_v1.md A.4 point 4):
  c2(f) := the exponent of the commutator (x,y) in gamma2(F2)/gamma3(F2) ~= Z.
  Computed here via the truncated (degree <= 2) Magnus expansion of the free group F2
  into the ring of noncommutative formal power series Z<<X,Y>> (x -> 1+X, y -> 1+Y).
  For w in gamma2(F2) (zero abelianization), the quadratic part of the Magnus expansion
  of w is necessarily antisymmetric: coeff(XY) = -coeff(YX), and c2(w) := coeff(XY),
  normalized so that c2([x,y]) = c2(x y x^-1 y^-1) = +1.

CV-13 (orientation lock): the extractor above has a single fixed sign convention (word
read left-to-right, x before y positive). This is anchored externally by a round-trip
test on a witness that is NOT self-inverse: w = [x,y] and w^-1 = [y,x] (w != w^-1 in F2,
since F2 is free / torsion-free). Convention is locked iff c2(w) = +1 and c2(w^-1) = -1
and c2(w) != c2(w^-1). This script aborts (raises) if the anchor fails.

lambda: for a GT-shadow (m, f) in GT(N), lambda := 2m+1 (definition ノート (3.53)/(180):
chi_vir([m,f]) = 2m+1 mod N_ord). We use the exact integer 2m+1 from the certificate's m
(m is already a canonical representative in {0,...,N_ord-1} in both source certs).

Quadratic-residue solvability battery ("各有限法での可解性"): for a fixed modulus battery
(the window's own N_ord -- the only modulus with an explicit definitional pedigree here,
line 180 of week1-定義ノート.md -- plus a fixed generic small-prime battery), we record,
for rhs = 24*c2+1 mod d:
  - qr_solvable(d): does ANY y in Z/d satisfy y^2 = rhs mod d?
  - lambda_is_witness(d): does the OBSERVED lambda satisfy lambda^2 = rhs mod d?
No values are predicted in code; this is a pure recording pass (distribution only).

HONESTY NOTE (explicit UNKNOWN, not a silent cap): the TRUE finite modulus d at which
c2(f) is well-defined as an invariant of the coset f * N_F2 (rather than of the specific
word representative) is the order of the image of [x,y] in the derived-subgroup quotient
gamma2(F2 N_F2/N_F2) / gamma3(...) of the window's actual finite quotient F2/N_F2. That
computation requires GAP (LowerCentralSeries of the window's concrete finite quotient) and
is OUT OF SCOPE for this python-only calibration pass. We do NOT claim N_ord is that true
modulus -- N_ord is used here only because it has an independent definitional pedigree
(line 180, chi_vir mod N_ord) and is the natural place to start a calibration battery.
"""
import json
import hashlib
import datetime
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

K3_PATH = os.path.join(ROOT, "certificates", "K3.v1.json")
A1_PATH = os.path.join(ROOT, "certificates", "A1.v2.2.json")
OUT_PATH = os.path.join(ROOT, "search", "certs", "c2q_calibration_20260801.json")

GENERIC_MODULI = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Truncated (degree <= 2) noncommutative Magnus expansion in Z<<X,Y>>
# ---------------------------------------------------------------------------

ZERO_PS = {"1": 1, "X": 0, "Y": 0, "XX": 0, "XY": 0, "YX": 0, "YY": 0}


def letter_ps(letter, exp):
    """Truncated degree<=2 Magnus expansion of generator^exp.
    (1+G)^exp = 1 + exp*G + C(exp,2)*G^2 as a formal power series (valid for any integer exp)."""
    c2coef = exp * (exp - 1) // 2  # exp*(exp-1) is always even
    ps = dict(ZERO_PS)
    ps["1"] = 1
    if letter == "x":
        ps["X"] = exp
        ps["XX"] = c2coef
    elif letter == "y":
        ps["Y"] = exp
        ps["YY"] = c2coef
    else:
        raise ValueError("unknown generator letter: %r" % (letter,))
    return ps


def mul_ps(a, b):
    r = {}
    r["1"] = a["1"] * b["1"]
    r["X"] = a["1"] * b["X"] + a["X"] * b["1"]
    r["Y"] = a["1"] * b["Y"] + a["Y"] * b["1"]
    r["XX"] = a["1"] * b["XX"] + a["X"] * b["X"] + a["XX"] * b["1"]
    r["XY"] = a["1"] * b["XY"] + a["X"] * b["Y"] + a["XY"] * b["1"]
    r["YX"] = a["1"] * b["YX"] + a["Y"] * b["X"] + a["YX"] * b["1"]
    r["YY"] = a["1"] * b["YY"] + a["Y"] * b["Y"] + a["YY"] * b["1"]
    return r


def magnus_of_word(f_word):
    ps = dict(ZERO_PS)
    for letter, exp in f_word:
        ps = mul_ps(ps, letter_ps(letter, exp))
    return ps


def c2_of(f_word):
    """c2(f) := coeff(XY) of the truncated Magnus expansion of f, with the sign
    convention fixed by the CV-13 anchor (c2([x,y]) = +1)."""
    ps = magnus_of_word(f_word)
    if ps["X"] != 0 or ps["Y"] != 0:
        raise ValueError(
            "f not in commutator subgroup (nonzero linear/abelianized part): X=%d Y=%d word=%r"
            % (ps["X"], ps["Y"], f_word)
        )
    if ps["XY"] != -ps["YX"]:
        raise ValueError(
            "quadratic part not antisymmetric (unexpected for a gamma2(F2) element): "
            "XY=%d YX=%d word=%r" % (ps["XY"], ps["YX"], f_word)
        )
    return ps["XY"]


def word_to_str(f_word):
    if not f_word:
        return "1"
    parts = []
    for letter, exp in f_word:
        if exp == 1:
            parts.append(letter)
        elif exp == -1:
            parts.append(letter + "^-1")
        else:
            parts.append("%s^%d" % (letter, exp))
    return "*".join(parts)


# ---------------------------------------------------------------------------
# CV-13 external anchor: round-trip on a non-self-inverse witness
# ---------------------------------------------------------------------------

def cv13_anchor_check():
    comm_xy = [["x", 1], ["y", 1], ["x", -1], ["y", -1]]  # [x,y] = x y x^-1 y^-1
    comm_yx = [["y", 1], ["x", 1], ["y", -1], ["x", -1]]  # [y,x] = [x,y]^-1
    c2_xy = c2_of(comm_xy)
    c2_yx = c2_of(comm_yx)
    ok = (c2_xy == 1) and (c2_yx == -1) and (c2_xy != c2_yx)
    return {
        "witness_w": "[x,y] = x*y*x^-1*y^-1",
        "witness_w_inv": "[y,x] = [x,y]^-1 = y*x*y^-1*x^-1",
        "self_inverse": False,
        "c2_w": c2_xy,
        "c2_w_inv": c2_yx,
        "expected_c2_w": 1,
        "expected_c2_w_inv": -1,
        "orientation_fixed": ok,
    }


# ---------------------------------------------------------------------------
# Quadratic residue battery
# ---------------------------------------------------------------------------

def qr_set(d):
    return set((k * k) % d for k in range(d))


def modulus_checks(rhs, lam, moduli):
    out = []
    for d in moduli:
        squares = qr_set(d)
        rhs_mod = rhs % d
        out.append({
            "modulus": d,
            "rhs_mod": rhs_mod,
            "qr_solvable": rhs_mod in squares,
            "lambda_is_witness": (lam * lam) % d == rhs_mod,
        })
    return out


# ---------------------------------------------------------------------------
# Load calibration population: K^(3) 12 elements + N_A 20 elements
# ---------------------------------------------------------------------------

def load_k3():
    with open(K3_PATH, "r", encoding="utf-8") as fh:
        cert = json.load(fh)
    n_ord = cert["target"]["invariants"]["N_ord"]
    shadows = []
    for i, sh in enumerate(cert["shadows"]):
        shadows.append({"window": "K3", "index": i, "m": sh["m"], "f_word": sh["f_word"]})
    return shadows, n_ord, K3_PATH


def load_na():
    with open(A1_PATH, "r", encoding="utf-8") as fh:
        cert = json.load(fh)
    # N_ord=5 for N_A: docs/week4-A5算術飽和_v4.md line 76 ("c in N_A, N_ord = 5"),
    # NOT present as a field in A1.v2.2.json itself -- recorded here with its source pin.
    n_ord = 5
    shadows = []
    for i, sh in enumerate(cert["settled_witness"]["detail"]):
        shadows.append({"window": "N_A", "index": i, "m": sh["m"], "f_word": sh["f_word"]})
    return shadows, n_ord, A1_PATH


def main():
    anchor = cv13_anchor_check()
    if not anchor["orientation_fixed"]:
        raise SystemExit("CV-13 anchor FAILED -- refusing to emit calibration cert: %r" % anchor)

    k3_shadows, k3_n_ord, k3_path = load_k3()
    na_shadows, na_n_ord, na_path = load_na()

    windows = [
        {"name": "K3", "n_ord": k3_n_ord, "shadows": k3_shadows, "source_path": k3_path,
         "source_sha256": sha256_file(k3_path),
         "theorem_pin": "定理K3(W3-11): Ih_{K3} 全射(K3.v1.json counts.thm46_expected_order=12=charming_pass=surjective_pass)"},
        {"name": "N_A", "n_ord": na_n_ord, "shadows": na_shadows, "source_path": na_path,
         "source_sha256": sha256_file(na_path),
         "theorem_pin": "定理A5(W3-8, (I1)(I2)条件付き): Ih_{N_A} 全射(A1.v2.2.json settled_witness.settled_count=20=total)"},
    ]

    records = []
    for w in windows:
        moduli = sorted(set([w["n_ord"]] + GENERIC_MODULI))
        for sh in w["shadows"]:
            m = sh["m"]
            f_word = sh["f_word"]
            c2 = c2_of([tuple(step) if isinstance(step, list) else step for step in f_word])
            lam = 2 * m + 1
            lhs = lam * lam
            rhs = 24 * c2 + 1
            records.append({
                "window": w["name"],
                "index": sh["index"],
                "m": m,
                "f_word": f_word,
                "f_word_str": word_to_str(f_word),
                "c2": c2,
                "lambda": lam,
                "lambda_sq": lhs,
                "rhs_24c2plus1": rhs,
                "exact_eq_over_Z": lhs == rhs,
                "modulus_checks": modulus_checks(rhs, lam, moduli),
            })

    exact_pass = sum(1 for r in records if r["exact_eq_over_Z"])
    exact_fail = sum(1 for r in records if not r["exact_eq_over_Z"])

    c2_values = [r["c2"] for r in records]
    c2_hist = {}
    for v in c2_values:
        c2_hist[str(v)] = c2_hist.get(str(v), 0) + 1

    per_window_summary = {}
    for w in windows:
        wrecs = [r for r in records if r["window"] == w["name"]]
        per_window_summary[w["name"]] = {
            "count": len(wrecs),
            "n_ord": w["n_ord"],
            "exact_eq_pass": sum(1 for r in wrecs if r["exact_eq_over_Z"]),
            "exact_eq_fail": sum(1 for r in wrecs if not r["exact_eq_over_Z"]),
            "c2_values_sorted": sorted(r["c2"] for r in wrecs),
            "c2_min": min(r["c2"] for r in wrecs),
            "c2_max": max(r["c2"] for r in wrecs),
        }

    cert = {
        "schema": "c2q-calibration/v1",
        "note": "較正段のみ・プローブ段は別認可(裁定380/docs/notes/fake_void_v1.md A.4 point 1)。"
                "値の予言はコードに書いていない -- 全て計算値をそのまま記録する(接触遮断)。",
        "generated_by": {
            "tool": "python " + os.sys.version.split()[0],
            "script": "search/probe/wac_v1/c2q_calibration.py",
            "date": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
        },
        "definition_source": {
            "c2_definition": "docs/scout/覚書_fvl1_20260801.md 型(i)/(ii)・docs/notes/fake_void_v1.md A.4 point 4"
                              "([F2,F2]/[[F2,F2],F2] における (x,y) の指数、Magnus展開の次数2項 XY 係数として計算)",
            "lambda_definition": "docs/week1-定義ノート.md line 180 (chi_vir([m,f]) = 2m+1 mod N_ord)",
            "target_relation": "lambda^2 = 24*c2(f) + 1 (Furusho, arXiv math/0702128, Question 14 の前提関係式)",
        },
        "cv13_orientation_anchor": anchor,
        "population": {
            "spec": "K^(3) の 12 元(certificates/K3.v1.json)+ N_A の 20 元(certificates/A1.v2.2.json) = 32 元。"
                     "両窓とも定理級(K3・A5)で arithmetical が閉じている -- 較正段はこの32元に限定し、"
                     "定理に覆われていない窓(N_Q・K^(12)・帯Wの4窓)へのプローブ段は本cert の範囲外(別認可待ち)。",
            "total_count": len(records),
            "windows": [
                {"name": w["name"], "n_ord": w["n_ord"], "count": len(w["shadows"]),
                 "source_path": os.path.relpath(w["source_path"], ROOT).replace("\\", "/"),
                 "source_sha256": w["source_sha256"],
                 "theorem_pin": w["theorem_pin"]}
                for w in windows
            ],
        },
        "generic_moduli_battery": GENERIC_MODULI,
        "records": records,
        "summary": {
            "total": len(records),
            "exact_eq_over_Z_pass": exact_pass,
            "exact_eq_over_Z_fail": exact_fail,
            "c2_distribution": c2_hist,
            "per_window": per_window_summary,
        },
        "honesty_note": "本cert は c2(f) の『真の』有限法 d(窓の F2/N_F2 における gamma2/gamma3 の位数)を"
                         "GAP で導出していない -- UNKNOWN のまま申告する(silent cap 禁止)。ここで使う modulus は "
                         "(i) N_ord(週1定義ノート line 180 の chi_vir mod N_ord という独立の出所を持つ)と "
                         "(ii) 固定の小素数バッテリー のみで、d の正体を主張しない。",
        "effective_source_chain": {"status": "n/a", "reason": "この cert は単系統python探索であり cross-checked を主張しない"},
        "seal_recoverability": {"status": "n/a", "reason": "この cert は封印 fixture を使用しない"},
        "level": "PB3",
    }

    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(cert, fh, ensure_ascii=False, indent=None, separators=(",", ":"))

    print("CV13_ANCHOR:", anchor)
    print("TOTAL_RECORDS=%d EXACT_EQ_PASS=%d EXACT_EQ_FAIL=%d" % (len(records), exact_pass, exact_fail))
    print("C2_DISTRIBUTION=%s" % json.dumps(c2_hist, sort_keys=True))
    for wname, s in per_window_summary.items():
        print("WINDOW=%s n_ord=%d count=%d exact_pass=%d exact_fail=%d c2_sorted=%s"
              % (wname, s["n_ord"], s["count"], s["exact_eq_pass"], s["exact_eq_fail"], s["c2_values_sorted"]))
    print("OUT_PATH=%s" % os.path.relpath(OUT_PATH, ROOT).replace("\\", "/"))
    print("OUT_SHA256=%s" % sha256_file(OUT_PATH))
    print("VERDICT: %s" % ("ALL EXACT MATCH" if exact_fail == 0 else "MISMATCHES PRESENT -- see records"))


if __name__ == "__main__":
    main()
