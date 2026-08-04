# -*- coding: utf-8 -*-
"""
atlas 統計調査 v1 -- データ収穫 script(探索器側)。

位置づけ: これは候補発見器の入力を作る機械抽出であって、格・定理主張の根拠ではない
(CLAUDE.md 冒頭規律・solver-candidate 哲学)。禁止列(封印3量・Im R・d_N・u値)は
一切読まない -- 対象 cert のうちそれらのフィールドは触れずに無視する。

出力: search/probe/atlas_stats/atlas_features_v1.csv
不明欄は UNKNOWN のまま埋めない(補完禁止)。

抽出対象は2系統:
  (A) search/certs/ 内の構造化 JSON cert(wac_v1-wall*/dl3/centb/l25t5 系・
      kernel_structure 系・ihnec_gap4_mcov_scan)-- 機械抽出、source列に cert path。
  (B) 主要窓で JSON cert が未整備のもの(K3/K5/K9(M)/K15/K20/W-5 等)は
      地図.md / LEDGER.md の記述から人手転記 -- 別 script (manual_narrative_rows.py) で
      追記し、source列に "narrative:裁定NNN" と明記して機械抽出と混同しない。
"""
import json, csv, os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CERTS = os.path.join(ROOT, "search", "certs")
OUT_CSV = os.path.join(os.path.dirname(__file__), "atlas_features_v1.csv")

FIELDS = [
    "window_id", "type", "n", "N_ord", "N_ord_factor_type", "exponent_band",
    "G_order", "kernel_order", "kernel_struct", "kernel_abelian",
    "kernel_solvable", "derived_length", "xi_eq_centralizer", "E_eq_6_An",
    "mcov_status", "N_prime_partner", "note", "source_cert",
]

def factor_type(n):
    """粗い素因数型: '2-power' / 'odd-prime' / 'odd-composite' / 'mixed' / UNKNOWN"""
    if n is None:
        return "UNKNOWN"
    try:
        n = int(n)
    except Exception:
        return "UNKNOWN"
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
    # all odd
    if len(primes) == 1:
        return "odd-prime-power"
    return "odd-composite"


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def row_from_wall_cert(path, d):
    wl = d.get("window_label", os.path.basename(path))
    wa = d.get("window_asserts", {}) or {}
    cw0 = d.get("centralizer_w0", {}) or {}
    xi = d.get("xi_image", {}) or {}
    n = d.get("n", wa.get("n"))
    N_ord = wa.get("N_ord")
    return {
        "window_id": wl,
        "type": "wall(Dih-B4)",
        "n": n,
        "N_ord": N_ord,
        "N_ord_factor_type": factor_type(N_ord),
        "exponent_band": "UNKNOWN",
        "G_order": "UNKNOWN",
        "kernel_order": cw0.get("size", "UNKNOWN"),
        "kernel_struct": cw0.get("structure_description", "UNKNOWN"),
        "kernel_abelian": "UNKNOWN",
        "kernel_solvable": cw0.get("solvable", "UNKNOWN"),
        "derived_length": cw0.get("derived_length", "UNKNOWN"),
        "xi_eq_centralizer": xi.get("eq_centralizer_w0", "UNKNOWN"),
        "E_eq_6_An": wa.get("E_eq_6_An", "UNKNOWN"),
        "mcov_status": "UNKNOWN",
        "N_prime_partner": "",
        "note": d.get("window_label", "") + " / " + d.get("f_orientation", ""),
        "source_cert": os.path.relpath(path, ROOT).replace("\\", "/"),
    }


def row_from_kernel_structure(path, d, label, n_hint):
    return {
        "window_id": label,
        "type": "metabelian-pincer(band1)",
        "n": n_hint,
        "N_ord": "UNKNOWN",
        "N_ord_factor_type": "UNKNOWN",
        "exponent_band": "UNKNOWN",
        "G_order": d.get("group_order") or d.get("G_order", "UNKNOWN"),
        "kernel_order": d.get("ker_size") or d.get("K_order", "UNKNOWN"),
        "kernel_struct": d.get("K_struct", "UNKNOWN"),
        "kernel_abelian": d.get("K_is_abelian", "UNKNOWN"),
        "kernel_solvable": "TRUE(metabelian band)",
        "derived_length": d.get("derived_length_G", "UNKNOWN"),
        "xi_eq_centralizer": "UNKNOWN",
        "E_eq_6_An": "UNKNOWN",
        "mcov_status": "UNKNOWN",
        "N_prime_partner": "",
        "note": "K_struct=%s / Kab_struct=%s" % (d.get("K_struct"), d.get("Kab_struct")),
        "source_cert": os.path.relpath(path, ROOT).replace("\\", "/"),
    }


def rows_from_mcov_scan(path, d):
    out = []
    for pr in d.get("pairs", []):
        out.append({
            "window_id": pr.get("K_window"),
            "type": "dihedral(K-side, MCOV pair)",
            "n": pr.get("n"),
            "N_ord": "UNKNOWN(pair-level; N_prime_ord below)",
            "N_ord_factor_type": factor_type(pr.get("n")),
            "exponent_band": "UNKNOWN",
            "G_order": "UNKNOWN",
            "kernel_order": "UNKNOWN",
            "kernel_struct": "UNKNOWN",
            "kernel_abelian": "UNKNOWN",
            "kernel_solvable": "UNKNOWN",
            "derived_length": "UNKNOWN",
            "xi_eq_centralizer": "UNKNOWN",
            "E_eq_6_An": "UNKNOWN",
            "mcov_status": pr.get("status"),
            "N_prime_partner": "%s(N_prime_ord=%s)" % (pr.get("N_prime_window"), pr.get("N_prime_ord")),
            "note": "M_ord=%s" % pr.get("M_ord"),
            "source_cert": os.path.relpath(path, ROOT).replace("\\", "/"),
        })
    return out


def main():
    rows = []

    wall_files = [
        "wall2_cert_20260731.json",
        "wall28_cert_20260731.json",
        "wall36_cert_20260731_r2.json",
        "wall37_cert_20260731_r2.json",
        "wall40_cert_20260801.json",
        "wall45_cert_20260801.json",
        "centb_cert_20260731.json",
        "dl3_cert_20260731.json",
        "l25t5_count_20260731.json",
    ]
    for fn in wall_files:
        p = os.path.join(CERTS, fn)
        if not os.path.exists(p):
            continue
        d = load(p)
        if "window_asserts" in d or "centralizer_w0" in d:
            rows.append(row_from_wall_cert(p, d))

    kernel_files = {
        "a16_kernel_structure_20260729.json": ("W-D-A16-11a", 11),
        "a18_kernel_structure_20260729.json": ("W-D-A18-13a", 13),
        "a20_kernel_structure_20260729.json": ("W-D-A20-15a", 15),
    }
    for fn, (label, n_hint) in kernel_files.items():
        p = os.path.join(CERTS, fn)
        if os.path.exists(p):
            d = load(p)
            rows.append(row_from_kernel_structure(p, d, label, n_hint))

    mcov_p = os.path.join(CERTS, "ihnec_gap4_mcov_scan_20260801.json")
    if os.path.exists(mcov_p):
        d = load(mcov_p)
        rows.extend(rows_from_mcov_scan(mcov_p, d))

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            for k in FIELDS:
                r.setdefault(k, "UNKNOWN")
            w.writerow(r)

    print("wrote", OUT_CSV, "rows=", len(rows))


if __name__ == "__main__":
    main()
