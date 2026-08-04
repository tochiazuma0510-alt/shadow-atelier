# -*- coding: utf-8 -*-
"""
穴(1)(3) 用の窓構造 cert バッチ(K(15) 直接窓 + mixed-2-and-odd 帯 K(6,10,12,14,18))を
atlas_features_v1.csv に機械抽出で追記する。

入力: search/certs/winstruct_K{n}_20260805.json (GAP 探索器出力)
      search/probe/atlas_stats/winstruct_crosscheck_20260805.json (独立照合器出力)
両方読んで note 列に Thm 4.3 照合の PASS/FAIL を機械転記する(手写しなし)。

kernel_* 列の意味(この行群のみ): D = [G_n,G_n] (derived subgroup of G_n = F2/N_F2)。
K^(n) 自体は PB3 の無限指数正規部分群であり有限の「位数」を持たないため、
charming 条件の対象である F2/N_F2 の交換子部分群 D を "kernel の構造" 欄として報告する
(week3-battery-common.g の EnumerateReducedHexagon が候補 f を D 上に制限しているのと同じ対象)。
"""
import csv, json, os

HERE = os.path.dirname(__file__)
CSV_PATH = os.path.join(HERE, "atlas_features_v1.csv")
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
CERTS = os.path.join(ROOT, "search", "certs")

FIELDS = [
    "window_id", "type", "n", "N_ord", "N_ord_factor_type", "exponent_band",
    "G_order", "kernel_order", "kernel_struct", "kernel_abelian",
    "kernel_solvable", "derived_length", "xi_eq_centralizer", "E_eq_6_An",
    "mcov_status", "N_prime_partner", "note", "source_cert",
]

TARGET_NS = [15, 6, 10, 12, 14, 18]


def factor_type(n):
    if n is None:
        return "UNKNOWN"
    n = int(n)
    if n <= 1:
        return "UNKNOWN"
    x = n
    p = 2
    factors = {}
    while p * p <= x:
        while x % p == 0:
            factors[p] = factors.get(p, 0) + 1
            x //= p
        p += 1
    if x > 1:
        factors[x] = factors.get(x, 0) + 1
    primes = sorted(factors.keys())
    if primes == [2]:
        return "2-power"
    if 2 in primes and len(primes) > 1:
        return "mixed-2-and-odd"
    if len(primes) == 1:
        return "odd-prime-power"
    return "odd-composite"


def main():
    if not os.path.exists(CSV_PATH):
        raise SystemExit("run extract_features.py first")

    xcheck_path = os.path.join(HERE, "winstruct_crosscheck_20260805.json")
    with open(xcheck_path, encoding="utf-8") as f:
        xcheck = json.load(f)
    xcheck_by_n = {r["n"]: r for r in xcheck["results"]}

    new_rows = []
    for n in TARGET_NS:
        cert_path = os.path.join(CERTS, "winstruct_K%d_20260805.json" % n)
        with open(cert_path, encoding="utf-8") as f:
            d = json.load(f)
        xr = xcheck_by_n[n]

        hx = d.get("hexagon_scan", {})
        note = (
            "D=[G,G] struct=%s / G_derived_length=%s / D_2part=%s D_oddpart=%s / "
            "charming|X_n|=%s / hexagon shadow_total=%s (candidate_total=%s, h10_fail=%s, h11_fail=%s, generation_fail=%s) / "
            "decode_fail_count=%s / Thm4.3 crosscheck=%s (predicted_total=%s, set_equality=%s) / "
            "crosscheck_cert=%s"
        ) % (
            d.get("derived_subgroup_struct"), d.get("G_derived_length"),
            d.get("derived_subgroup_2part"), d.get("derived_subgroup_oddpart"),
            d.get("charming_set_size"), hx.get("shadow_total"), hx.get("candidate_total"),
            hx.get("h10_fail"), hx.get("h11_fail"), hx.get("generation_fail"),
            d.get("decode_fail_count"),
            xr["status"], xr.get("predicted_total"), xr["checks"].get("set_equality") if "checks" in xr else "UNKNOWN",
            os.path.relpath(os.path.join(HERE, "winstruct_crosscheck_20260805.json"), ROOT).replace("\\", "/"),
        )

        row = {
            "window_id": "KDIR-%d" % n,
            "type": "dihedral(K-window, direct enum, calibration)",
            "n": n,
            "N_ord": d.get("N_ord"),
            # NB: factor_type(n) here, not factor_type(N_ord) -- matches the existing
            # dihedral(K-side, MCOV pair) row convention (rows_from_mcov_scan in
            # extract_features.py uses factor_type(pr.get("n"))). N_ord=lcm(n,2) is
            # trivially mixed-2-and-odd for every odd n (2n always has a lone factor of 2),
            # so classifying by N_ord would misfile n=15 (odd-composite, hole 1) into the
            # mixed-2-and-odd band (hole 3) it does not belong to.
            "N_ord_factor_type": factor_type(n),
            "exponent_band": "UNKNOWN",
            "G_order": d.get("G_order"),
            "kernel_order": d.get("derived_subgroup_order"),
            "kernel_struct": d.get("derived_subgroup_struct"),
            "kernel_abelian": d.get("derived_subgroup_abelian"),
            "kernel_solvable": d.get("derived_subgroup_solvable"),
            "derived_length": d.get("derived_subgroup_derived_length"),
            "xi_eq_centralizer": "UNKNOWN",
            "E_eq_6_An": "UNKNOWN",
            "mcov_status": "UNKNOWN(この行はMCOVペア表と無関係)",
            "N_prime_partner": "",
            "note": note,
            "source_cert": os.path.relpath(cert_path, ROOT).replace("\\", "/"),
        }
        new_rows.append(row)

    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
        existing = list(csv.DictReader(f))
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in existing:
            w.writerow(r)
        for r in new_rows:
            for k in FIELDS:
                r.setdefault(k, "UNKNOWN")
            w.writerow(r)

    print("appended", len(new_rows), "winstruct rows; total now", len(existing) + len(new_rows))


if __name__ == "__main__":
    main()
