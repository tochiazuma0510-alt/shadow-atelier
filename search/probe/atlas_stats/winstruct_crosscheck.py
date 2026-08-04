# -*- coding: utf-8 -*-
"""
winstruct_crosscheck.py -- 独立照合器(探索器と helper 非共有)。

入力: search/certs/winstruct_K{n}_20260805.json (GAP 探索器の出力証明書のみ)。
GAP のコード・中間結果は import しない(CLAUDE.md 鉄則2: 探索器と照合器の分離)。

やること: 各窓について、cert が報告する n だけを使い、正典 arXiv 2405.11725
Thm 4.3 (4.12) の閉じた式を本スクリプトで独立に再計算し、GT(K^(n)) の
(m,k) 集合として cert の shadows_mk (decode_ok=true のみ) と**集合として**突合する。

Thm 4.3 (4.12) (docs/week1-定義ノート.md より逐語):
  GT(K^(n)) = { (m, (r^{2k}, r^{-2k}, r^{kappa(m)})) | m in X_n, k in Z },
  4|n のときのみ追加条件 k = kappa(m)/2 (mod 2).
  X_n = { m in {0..N_ord-1} | gcd(2m+1, N_ord) = 1 },  N_ord = lcm(n,2)
  kappa(m) = m+1 (m odd) / -m (m even)
  k は mod n1 := ord(r^2) = n/2 (n偶) / n (n奇)

格: これは「照合済み(cross-checked)」であって Lean 検証ではない(CLAUDE.md 用語規律)。
"""
import json
import os
from math import gcd

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CERTS = os.path.join(ROOT, "search", "certs")

TARGET_NS = [15, 6, 10, 12, 14, 18]


def thm43_predicted_set(n):
    Nord = n if n % 2 == 0 else 2 * n  # lcm(n,2)
    n1 = n // 2 if n % 2 == 0 else n
    Xn = [m for m in range(Nord) if gcd(2 * m + 1, Nord) == 1]
    pred = set()
    for m in Xn:
        kappa = (m + 1) if (m % 2 == 1) else (-m)
        assert kappa % 2 == 0, "kappa(m) must be even by construction"
        if n % 4 == 0:
            target_parity = (kappa // 2) % 2
            allowed_k = [k for k in range(n1) if k % 2 == target_parity]
        else:
            allowed_k = list(range(n1))
        for k in allowed_k:
            pred.add((m, k))
    return Xn, Nord, n1, pred


def load_cert(n):
    path = os.path.join(CERTS, "winstruct_K%d_20260805.json" % n)
    if not os.path.exists(path):
        return None, path
    with open(path, encoding="utf-8") as f:
        return json.load(f), path


def crosscheck_one(n):
    cert, path = load_cert(n)
    if cert is None:
        return {"n": n, "status": "CERT_MISSING", "cert_path": os.path.relpath(path, ROOT).replace("\\", "/")}

    Xn, Nord, n1, predicted = thm43_predicted_set(n)
    predicted_total = len(predicted)

    # cert-reported values (used only as reported values to compare, not trusted blindly)
    cert_Nord = cert.get("N_ord")
    cert_Xn = sorted(int(m) for m in cert.get("charming_set", []))
    cert_Xn_size = cert.get("charming_set_size")
    cert_n1 = cert.get("n1_ord_r2")
    cert_shadow_total = cert.get("hexagon_scan", {}).get("shadow_total")
    decode_fail_count = cert.get("decode_fail_count", None)

    actual_set = set()
    decode_ok_count = 0
    for sh in cert.get("shadows_mk", []):
        if sh.get("decode_ok"):
            actual_set.add((int(sh["m"]), int(sh["k"])))
            decode_ok_count += 1

    checks = {}
    checks["N_ord_match"] = (cert_Nord == Nord)
    checks["n1_match"] = (cert_n1 == n1)
    checks["charming_set_match"] = (cert_Xn == sorted(Xn))
    checks["charming_set_size_match"] = (cert_Xn_size == len(Xn))
    checks["decode_fail_zero"] = (decode_fail_count == 0)
    checks["shadow_total_matches_predicted_count"] = (cert_shadow_total == predicted_total)
    checks["decode_ok_count_matches_shadow_total"] = (decode_ok_count == cert_shadow_total)
    checks["set_equality"] = (actual_set == predicted)

    only_in_actual = sorted(actual_set - predicted)
    only_in_predicted = sorted(predicted - actual_set)

    overall_pass = all(checks.values())

    return {
        "n": n,
        "status": "PASS" if overall_pass else "FAIL",
        "cert_path": os.path.relpath(path, ROOT).replace("\\", "/"),
        "N_ord": Nord,
        "n1": n1,
        "X_n_size": len(Xn),
        "predicted_total": predicted_total,
        "cert_shadow_total": cert_shadow_total,
        "decode_ok_count": decode_ok_count,
        "checks": checks,
        "only_in_actual_not_predicted": only_in_actual[:20],
        "only_in_predicted_not_actual": only_in_predicted[:20],
        "diff_counts": {
            "only_in_actual": len(only_in_actual),
            "only_in_predicted": len(only_in_predicted),
        },
    }


def main():
    results = [crosscheck_one(n) for n in TARGET_NS]
    out = {
        "crosscheck_version": "winstruct_crosscheck_v1",
        "generated": "20260805",
        "note": "independent re-derivation of Thm 4.3 (4.12) from n only; reads GAP cert JSON only, no GAP code import",
        "targets": TARGET_NS,
        "results": results,
    }
    out_path = os.path.join(os.path.dirname(__file__), "winstruct_crosscheck_20260805.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print("=== winstruct crosscheck ===")
    npass = 0
    nfail = 0
    for r in results:
        print("n=%2d  status=%s" % (r["n"], r["status"]))
        if r["status"] == "PASS":
            npass += 1
        else:
            nfail += 1
            print("   ", json.dumps(r, ensure_ascii=False))
    print("PASS: %d  FAIL: %d  (of %d)" % (npass, nfail, len(results)))
    print("wrote", out_path)


if __name__ == "__main__":
    main()
