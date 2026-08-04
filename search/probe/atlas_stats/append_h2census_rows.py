# -*- coding: utf-8 -*-
"""
H2CENSUS 行種の追記: search/certs/h2_census_s4_20260805.json の在庫表(V-cen層
p=2 dim2-4 の厳密12型 + p=3 dim2 の悉皆5型)を atlas_features_v1.csv へ機械追記する。

司令塔発注「統計調査の穴(2) = H^2(S4,V) 在庫表 census」(F102-6.3 限定認可分)の
統計表側の反映。既存 CSV スキーマ(window/kernel 構造用)は本質的にモジュール加群の
census 用ではないため、type 列に "H2CENSUS" を立てて他の kernel_* 列は UNKNOWN のまま
残し、note 列に本 census 固有の値(p, dim, s3_inflated, dim_H2_S4, dim_H2_S3, dim_H1_S4,
window_order, band_note)を機械転記する。手書きなし(cert から読むのみ)。

判定欄は持たない(S-BU-10 準拠): note に棄却/生存/EMPTY の語を書かない。
"""
import csv
import json
import os

HERE = os.path.dirname(__file__)
CSV_PATH = os.path.join(HERE, "atlas_features_v1.csv")
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
CERT_PATH = os.path.join(ROOT, "search", "certs", "h2_census_s4_20260805.json")

FIELDS = [
    "window_id", "type", "n", "N_ord", "N_ord_factor_type", "exponent_band",
    "G_order", "kernel_order", "kernel_struct", "kernel_abelian",
    "kernel_solvable", "derived_length", "xi_eq_centralizer", "E_eq_6_An",
    "mcov_status", "N_prime_partner", "note", "source_cert",
]


def main():
    if not os.path.exists(CSV_PATH):
        raise SystemExit("atlas_features_v1.csv not found -- run extract_features.py first")
    with open(CERT_PATH, "r", encoding="utf-8") as f:
        cert = json.load(f)

    with open(CSV_PATH, "r", encoding="utf-8", newline="") as f:
        existing = list(csv.DictReader(f))
    existing_ids = set(r["window_id"] for r in existing)

    new_rows = []
    for row in cert["rows"]:
        wid = "H2CENSUS-" + row["module_id"]
        if wid in existing_ids:
            continue
        note = (
            "H2 census(F102-6.3限定認可分・棄却/生存/EMPTY不使用). p=%d dim=%d "
            "s3_inflated=%s socle=%s dim_H2_S4=%d dim_H2_S3=%d dim_H1_S4=%d "
            "window_order=%d band_note=%s scope=inventory-only(判定欄なし)"
            % (
                row["p"], row["dim"], row["s3_inflated"], row["socle_structure"],
                row["dim_H2_S4"], row["dim_H2_S3"], row["dim_H1_S4"],
                row["window_order"], row["band_note"],
            )
        )
        new_rows.append({
            "window_id": wid,
            "type": "H2CENSUS",
            "n": "UNKNOWN",
            "N_ord": "UNKNOWN",
            "N_ord_factor_type": "UNKNOWN",
            "exponent_band": "UNKNOWN",
            "G_order": "UNKNOWN",
            "kernel_order": row["window_order"],
            "kernel_struct": row["socle_structure"],
            "kernel_abelian": "UNKNOWN",
            "kernel_solvable": "UNKNOWN",
            "derived_length": "UNKNOWN",
            "xi_eq_centralizer": "UNKNOWN",
            "E_eq_6_An": "UNKNOWN",
            "mcov_status": "UNKNOWN",
            "N_prime_partner": "",
            "note": note,
            "source_cert": "search/certs/h2_census_s4_20260805.json",
        })

    if not new_rows:
        print("no new H2CENSUS rows to append (already present)")
        return

    with open(CSV_PATH, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        for r in new_rows:
            w.writerow(r)

    print("appended %d H2CENSUS rows to %s" % (len(new_rows), CSV_PATH))


if __name__ == "__main__":
    main()
