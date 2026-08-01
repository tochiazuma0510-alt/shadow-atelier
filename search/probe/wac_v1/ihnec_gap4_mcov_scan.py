# -*- coding: utf-8 -*-
"""
【IHNEC-GAP-4】(MCOV) 全数走査(裁定 389・司令塔広い解釈裁定 2026-08-01)

目的: docs/notes/ihnec_v1.md 追補D §D.1.2 の前件 (MCOV) --
  forall m in X_n exists m~ (mod M_ord): m~ == m (mod 2n), m~ mod N'_ord in m(N')
を、工房に既に登録済みの窓インベントリから機械的に拾える (K^(n), N') 全対について
成立/破れ/DATA_MISSING を有限集合比較で全数判定する。

宇宙の凍結(裁定どおり・走査前に固定・結果を見て足し引きしない):
  K^(n) 側: certificates/*.v1.json のうち target.family == "dihedral" かつ
            target.n が奇数 >= 3 であるもの(SPLIT-NULL / 系 SPLIT-NULL' の前提 "n 奇 >= 3"
            そのもの)。X_n は n のみに依存する純算術量なので cert 読解は不要
            (X_n = { m mod 2n : gcd(2m+1, 2n) == 1 })。
  N' 側:    certificates/ 直下の単体 JSON ファイル(サブディレクトリは E1/EP/N-infinity 等の
            別系統の作業台であり本件の窓レジストリではないので除外)のうち、
            universe.n_ord + universe.charming_set を直接持つもの(schema gtsh-cert/v2,
            v2-psl)、または target.invariants.N_ord を持ち shadows[].m の distinct 値から
            m(N') を機械抽出できるもの(schema gtsh-cert/v1・family in {general, control})。
            family == "dihedral" の窓(K*)は K 側専用としこちら側からは除外する
            (K^(n) 同士のペアリングは本 GAP-4 の対象外 -- SPLIT-NULL は K^(n) と
            「非 dihedral の N'」の対を前提にしている)。
            charming/N_ord を機械読みできない亜種(A1.v2.1.json, A1.v2.2.json など)は
            N' レジストリに含めない(この2ファイルは universe.n_ord も charming_set も
            持たない = 機械抽出条件を満たさないため、はじめから宇宙に入れない。走査後の
            間引きではない)。

DATA_MISSING は正直記帳する。今回の凍結宇宙では両側とも machine-readable な窓のみを
集めたため理論上 DATA_MISSING は出ない設計だが、コードとしては一般に対応する。

期待値はコードに書かない(接触遮断)。MCOV_FAILS は「fake witness」ではなく
「fake witness 候補の対」として記帳する(数学的解釈は数学者+falsifier 行き)。
"""
import json
import hashlib
import os
from math import gcd
from datetime import datetime, timezone

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CERT_DIR = os.path.join(REPO_ROOT, "certificates")
OUT_PATH = os.path.join(REPO_ROOT, "search", "certs", "ihnec_gap4_mcov_scan_20260801.json")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def rel(path):
    return os.path.relpath(path, REPO_ROOT).replace("\\", "/")


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def charming_set_from_n(n):
    """X_n = { m mod 2n : gcd(2m+1, 2n) == 1 } -- 純算術(cert 不要)。"""
    two_n = 2 * n
    return sorted(m for m in range(two_n) if gcd(2 * m + 1, two_n) == 1)


# ---------------------------------------------------------------------------
# 宇宙の凍結: K 側(奇数 n>=3 の dihedral 窓・certificates/K*.v1.json)
# ---------------------------------------------------------------------------

def discover_k_side():
    entries = []
    for fname in sorted(os.listdir(CERT_DIR)):
        fpath = os.path.join(CERT_DIR, fname)
        if not os.path.isfile(fpath) or not fname.endswith(".json"):
            continue
        try:
            d = load_json(fpath)
        except Exception:
            continue
        target = d.get("target")
        if not isinstance(target, dict):
            continue
        if target.get("family") != "dihedral":
            continue
        n = target.get("n")
        if not isinstance(n, int) or n < 3 or n % 2 == 0:
            continue
        entries.append({
            "window_id": target.get("id"),
            "n": n,
            "two_n": 2 * n,
            "source_cert": {"path": rel(fpath), "sha256": sha256_of(fpath)},
        })
    entries.sort(key=lambda e: e["n"])
    return entries


# ---------------------------------------------------------------------------
# 宇宙の凍結: N' 側(certificates/ 直下・非 dihedral・N_ord+charming が機械読みできる窓)
# ---------------------------------------------------------------------------

def discover_nprime_side():
    entries = []
    for fname in sorted(os.listdir(CERT_DIR)):
        fpath = os.path.join(CERT_DIR, fname)
        if not os.path.isfile(fpath) or not fname.endswith(".json"):
            continue
        try:
            d = load_json(fpath)
        except Exception:
            continue

        target = d.get("target")
        if isinstance(target, dict) and target.get("family") == "dihedral":
            continue  # K 側専用、N' 側からは除外

        n_ord = None
        charming = None
        window_id = None

        universe = d.get("universe")
        if isinstance(universe, dict) and isinstance(universe.get("n_ord"), int) \
                and isinstance(universe.get("charming_set"), list):
            n_ord = universe["n_ord"]
            charming = sorted(universe["charming_set"])
            window_id = fname[:-len(".v2.json")] if fname.endswith(".v2.json") else fname

        elif isinstance(target, dict):
            inv = target.get("invariants")
            shadows = d.get("shadows")
            if isinstance(inv, dict) and isinstance(inv.get("N_ord"), int) and isinstance(shadows, list) and shadows:
                n_ord = inv["N_ord"]
                charming = sorted(set(s["m"] for s in shadows if isinstance(s, dict) and "m" in s))
                window_id = target.get("id") or fname

        if n_ord is None or not charming:
            continue  # 機械読み不可 -> 宇宙に入れない(間引きではなく最初から不採用)

        entries.append({
            "window_id": window_id,
            "N_ord": n_ord,
            "m_image_mod_N_ord": charming,
            "source_cert": {"path": rel(fpath), "sha256": sha256_of(fpath)},
        })
    entries.sort(key=lambda e: (e["N_ord"], e["window_id"]))
    return entries


def lcm(a, b):
    return a * b // gcd(a, b)


def check_mcov(n, two_n, x_n, n_prime_ord, m_image):
    """
    (MCOV): forall m in X_n exists m~ (mod M_ord):
        m~ == m (mod 2n)  and  m~ mod N'_ord in m(N')
    ここで M_ord := lcm(2n, N'_ord)。
    m~ の候補は m, m+2n, m+2*2n, ... の M_ord/2n 個(mod M_ord)を尽くせば十分。
    """
    m_ord = lcm(two_n, n_prime_ord)
    m_image_set = set(m_image)
    missing = []
    for m in x_n:
        found = False
        witness = None
        k = 0
        while m + k * two_n < m_ord:
            candidate = m + k * two_n
            if candidate % n_prime_ord in m_image_set:
                found = True
                witness = candidate
                break
            k += 1
        if not found:
            missing.append(m)
    holds = len(missing) == 0
    return {
        "M_ord": m_ord,
        "holds": holds,
        "missing_m": missing,
    }


def main():
    k_side = discover_k_side()
    n_side = discover_nprime_side()

    universe = {
        "k_side_criterion": "certificates/*.json の直下ファイルで target.family==\"dihedral\" かつ target.n が奇数>=3",
        "k_side_source_dir": "certificates/ (直下ファイルのみ・サブディレクトリ除外)",
        "k_side_count": len(k_side),
        "k_side": k_side,
        "n_prime_side_criterion": (
            "certificates/*.json の直下ファイルで target.family!=\"dihedral\" かつ "
            "(universe.n_ord+universe.charming_set が直接存在) または "
            "(target.invariants.N_ord が存在し shadows[].m の distinct 値で m(N') を機械抽出できる)"
        ),
        "n_prime_side_source_dir": "certificates/ (直下ファイルのみ・サブディレクトリ除外)",
        "n_prime_side_excluded_unreadable": [
            "A1.v2.1.json", "A1.v2.2.json"
        ],
        "n_prime_side_excluded_unreadable_reason": "universe.n_ord / universe.charming_set を持たず機械抽出条件を満たさないため、走査前から宇宙に含めない",
        "n_prime_side_count": len(n_side),
        "n_prime_side": n_side,
        "note_subdirectories_excluded": (
            "certificates/ のサブディレクトリ(a5, bfc, e19, e2c6, e2c6j3, e2sweep, k3, "
            "k5blocks, k5e, k5fixture, k5pipeline, mb, twincell)は E1/EP/N-infinity 等の"
            "別系統の作業台であり、本件 IHNEC の K^(n)/N' 窓レジストリではないため除外"
        ),
    }

    pairs = []
    mcov_holds_count = 0
    mcov_fails_count = 0
    data_missing_count = 0

    for k in k_side:
        x_n = charming_set_from_n(k["n"])
        for np_ in n_side:
            if x_n is None or np_["m_image_mod_N_ord"] is None:
                pairs.append({
                    "K_window": k["window_id"],
                    "n": k["n"],
                    "N_prime_window": np_["window_id"],
                    "status": "DATA_MISSING",
                    "reason": "X_n または m(N') のいずれかを取得できなかった",
                })
                data_missing_count += 1
                continue

            result = check_mcov(k["n"], k["two_n"], x_n, np_["N_ord"], np_["m_image_mod_N_ord"])
            status = "MCOV_HOLDS" if result["holds"] else "MCOV_FAILS_CANDIDATE"
            if status == "MCOV_HOLDS":
                mcov_holds_count += 1
            else:
                mcov_fails_count += 1

            pairs.append({
                "K_window": k["window_id"],
                "n": k["n"],
                "two_n": k["two_n"],
                "N_prime_window": np_["window_id"],
                "N_prime_ord": np_["N_ord"],
                "M_ord": result["M_ord"],
                "X_n": x_n,
                "m_image_N_prime": np_["m_image_mod_N_ord"],
                "status": status,
                "missing_m": result["missing_m"],
            })

    total_pairs = len(pairs)

    # 外部アンカー: 既知対 (K9, S4) は裁定389で MCOV 成立が確認済み -- 合格条件
    anchor_pair = next(
        (p for p in pairs if p.get("K_window") == "K9" and p.get("N_prime_window") == "S4"),
        None,
    )
    anchor_status = anchor_pair["status"] if anchor_pair else "PAIR_NOT_FOUND"
    anchor_ok = anchor_status == "MCOV_HOLDS"

    cert = {
        "schema": "ihnec-gap4-mcov-scan/v1",
        "generated_by": {
            "tool": "python3 (single-implementation exploratory scan, not GAP)",
            "script": rel(os.path.abspath(__file__)),
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        },
        "task_ref": "【IHNEC-GAP-4】docs/notes/ihnec_v1.md 追補D §D.1.2/§D.1.5, P98-3.1(sol/sol_reply_98_math25.md)",
        "claim_class": "exploration",
        "note": (
            "各対で (MCOV) の成立/破れを m 水準の有限集合比較のみで全数判定する。"
            "MCOV_FAILS_CANDIDATE は fake witness そのものではなく "
            "fake witness 候補の対 -- 屋根 M の実在・reduction 意味論の適用可否の"
            "数学確認は数学者+falsifier 行き。"
        ),
        "mcov_definition": (
            "forall m in X_n exists m~ (mod M_ord): "
            "m~ == m (mod 2n)  and  m~ mod N'_ord in m(N'),  M_ord := lcm(2n, N'_ord)"
        ),
        "universe": universe,
        "total_pairs": total_pairs,
        "summary": {
            "MCOV_HOLDS": mcov_holds_count,
            "MCOV_FAILS_CANDIDATE": mcov_fails_count,
            "DATA_MISSING": data_missing_count,
        },
        "anchor_check": {
            "description": "既知対 (K^(9), N_S4) は裁定389/追補D §D.1.3 で MCOV 成立が数値確認済み -- これが不成立なら scanner 側のバグ",
            "pair": "K9 x S4",
            "status": anchor_status,
            "pass": anchor_ok,
        },
        "mcov_fails_candidate_pairs": [
            p for p in pairs if p["status"] == "MCOV_FAILS_CANDIDATE"
        ],
        "pairs": pairs,
        "conventions_used": {
            "ledger_version": "conventions_ledger_v1_3",
            "perm_composition": "n/a(整数演算のみ・置換なし)",
            "comparison_target": {
                "as_function_of": "cert から読んだ N_ord/charming_set と、n のみから計算する X_n との有限集合包含判定",
                "function_a": {"name": "charming_set_from_n(n)", "domain": "odd n>=3 (K side)", "source_digest": sha256_of(os.path.abspath(__file__))},
                "function_b": {"name": "n_prime cert の universe.charming_set / shadows[].m 抽出", "domain": "N' side registry", "source_digest": "n/a(各窓 cert 個別、universe.n_prime_side[].source_cert に列挙)"},
                "normalization_digest": "n/a(正規化なし、mod 演算の等式判定のみ)",
            },
            "chi_P_criterion": {
                "value": "exact",
                "justification": "m の mod 演算による有限集合包含判定であり generator/orientation は不要(向きに依存しない算術等式)",
                "generator_fixed": "n/a",
                "orientation_fixed": "n/a",
            },
            "separation": {
                "included": False,
                "competitor_universe": [],
                "result": {"result_digest": "n/a(比較対象は各窓固有・分離実験ではない)"},
                "forbidden_values": {"handling": "n/a", "list": []},
                "dummy_fixture": {
                    "id": "n/a",
                    "normalised_input": "n/a",
                    "normalised_output": "n/a",
                    "discriminating_power": {"input_layer_novel": False, "output_layer_novel": False},
                    "expected": "n/a", "observed": "n/a", "verdict": "n/a",
                },
            },
            "cv13_orientation_self_assert": {
                "status": "n/a",
                "reason": "本 probe は候補生成器を持たない(既存 cert から読んだ2つの有限集合の mod 包含判定のみ)。CV-13 は生成器・受理器の向き自己検査であり対象外。",
            },
        },
        "cross_checked_status": {
            "status": "n/a",
            "reason": "単一実装(python)の探索的走査。cross-checked を主張しない。claim_class=exploration。",
        },
        "effective_source_chain": {
            "status": "n/a",
            "reason": "この cert は既存の複数窓 cert から機械抽出した集合の算術比較であり、単一の有効出所連鎖を持たない。各窓の出所は universe.k_side[].source_cert / universe.n_prime_side[].source_cert に個別記録。",
        },
        "seal_recoverability": {
            "status": "n/a",
            "reason": "封印 fixture を使用しない",
        },
        "level": "PB3",
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(cert, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print("=== IHNEC-GAP-4 (MCOV) 全数走査 ===")
    print("K side (odd n>=3 dihedral windows):", len(k_side), [k["window_id"] for k in k_side])
    print("N' side (charming/N_ord machine-readable windows):", len(n_side), [n_["window_id"] for n_ in n_side])
    print("total pairs =", total_pairs)
    print("MCOV_HOLDS =", mcov_holds_count)
    print("MCOV_FAILS_CANDIDATE =", mcov_fails_count)
    print("DATA_MISSING =", data_missing_count)
    print("anchor (K9 x S4) status =", anchor_status, "pass =", anchor_ok)
    if mcov_fails_count:
        print("--- MCOV_FAILS_CANDIDATE pairs ---")
        for p in pairs:
            if p["status"] == "MCOV_FAILS_CANDIDATE":
                print(" ", p["K_window"], "x", p["N_prime_window"], "missing_m=", p["missing_m"])
    print("cert written to:", rel(OUT_PATH))


if __name__ == "__main__":
    main()
