# -*- coding: utf-8 -*-
"""
narrative 由来行の追記(手動転記・機械抽出ではない)。

extract_features.py が抽出した JSON cert 群には、主戦線の主要窓(K3/K5/K9 roof/K15/K20/W-5等)の
多くが「構造化 cert」としてまだ整備されていない(地図.md 本文・LEDGER 裁定に散在)。
これらを含めないと層別の対象母集団が偏るため、明示的に narrative ソースとして追記する。

規律:
- source_cert 列に "narrative:裁定NNN(docs/地図.md)" の形で出所を明記 -- 機械抽出行と混同しない。
- 数値が文中で確認できないものは UNKNOWN のまま(補完しない)。
- 封印3量・Im R・d_N・u値には触れない(読んでいない)。
"""
import csv, os

HERE = os.path.dirname(__file__)
CSV_PATH = os.path.join(HERE, "atlas_features_v1.csv")

FIELDS = [
    "window_id", "type", "n", "N_ord", "N_ord_factor_type", "exponent_band",
    "G_order", "kernel_order", "kernel_struct", "kernel_abelian",
    "kernel_solvable", "derived_length", "xi_eq_centralizer", "E_eq_6_An",
    "mcov_status", "N_prime_partner", "note", "source_cert",
]

NARRATIVE_ROWS = [
    {
        "window_id": "K3", "type": "dihedral(main-line, n=odd)", "n": 3, "N_ord": "UNKNOWN",
        "N_ord_factor_type": "UNKNOWN", "exponent_band": "settled(theorem K3)",
        "G_order": "UNKNOWN", "kernel_order": "UNKNOWN", "kernel_struct": "UNKNOWN",
        "kernel_abelian": "UNKNOWN", "kernel_solvable": "UNKNOWN", "derived_length": "UNKNOWN",
        "xi_eq_centralizer": "UNKNOWN", "E_eq_6_An": "UNKNOWN", "mcov_status": "UNKNOWN(別途MCOVペア表を参照)",
        "N_prime_partner": "", "note": "帯0 = 定理K3で全射踏破(settled)。数値欄は本調査で未機械確認のためUNKNOWN。",
        "source_cert": "narrative:地図.md 全体図(帯0)/ 裁定不特定(定理K3)",
    },
    {
        "window_id": "K5", "type": "dihedral(main-line, n=odd, blind campaign)", "n": 5, "N_ord": "UNKNOWN",
        "N_ord_factor_type": "odd-prime-power", "exponent_band": "front-line(Phase1 GO)",
        "G_order": "UNKNOWN(候補下限|GT|=40と記述されるが本調査未確認)", "kernel_order": "UNKNOWN",
        "kernel_struct": "UNKNOWN", "kernel_abelian": "UNKNOWN", "kernel_solvable": "UNKNOWN",
        "derived_length": "UNKNOWN", "xi_eq_centralizer": "UNKNOWN", "E_eq_6_An": "UNKNOWN",
        "mcov_status": "UNKNOWN", "N_prime_partner": "",
        "note": "isolated=UNKNOWN(blind campaign継続中・裁定413 Phase1較正 K5-1..K5-5全PASS)。genuine判定は未確定=UNKNOWN。",
        "source_cert": "narrative:LEDGER裁定413/裁定412(地図.md P1行)",
    },
    {
        "window_id": "M=K9capNS4(roof,972)", "type": "roof(entangled-candidate, over K9)", "n": 9,
        "N_ord": "UNKNOWN", "N_ord_factor_type": "odd-prime-power", "exponent_band": "UNKNOWN",
        "G_order": "UNKNOWN", "kernel_order": "UNKNOWN", "kernel_struct": "UNKNOWN",
        "kernel_abelian": "UNKNOWN", "kernel_solvable": "UNKNOWN", "derived_length": "UNKNOWN",
        "xi_eq_centralizer": "UNKNOWN", "E_eq_6_An": "UNKNOWN", "mcov_status": "MCOV_HOLDS(anchor pair K9xS4, 別表参照)",
        "N_prime_partner": "S4",
        "note": "|GT(M)|=972が二経路(R4a/R4b)+二環境で集合水準cross-checked(裁定412/456-461)。split/non-split判定は本調査未確認=UNKNOWN。",
        "source_cert": "narrative:LEDGER裁定385/387/412/456-461(地図.md P2/P6行)",
    },
    {
        "window_id": "K15(FIVE-BYPASS route)", "type": "dihedral(main-line, n=odd, mixed-factor)", "n": 15,
        "N_ord": "UNKNOWN", "N_ord_factor_type": "odd-composite(3x5)", "exponent_band": "UNKNOWN",
        "G_order": "UNKNOWN", "kernel_order": "UNKNOWN", "kernel_struct": "UNKNOWN",
        "kernel_abelian": "UNKNOWN", "kernel_solvable": "UNKNOWN", "derived_length": "UNKNOWN",
        "xi_eq_centralizer": "UNKNOWN", "E_eq_6_An": "UNKNOWN", "mcov_status": "UNKNOWN",
        "N_prime_partner": "",
        "note": "系FIVE-BYPASS=K(15)経由の封印非接触迂回candidate(裁定394)。量化緩和形のみ登録・genuine判定UNKNOWN。",
        "source_cert": "narrative:LEDGER裁定394(地図.md P1行)",
    },
    {
        "window_id": "K20(calibration control)", "type": "dihedral(main-line, n=even, DEMOTED to control)", "n": 20,
        "N_ord": "UNKNOWN", "N_ord_factor_type": "mixed-2-and-odd(2^2x5)", "exponent_band": "UNKNOWN",
        "G_order": "UNKNOWN", "kernel_order": "UNKNOWN", "kernel_struct": "UNKNOWN",
        "kernel_abelian": "UNKNOWN", "kernel_solvable": "UNKNOWN", "derived_length": "UNKNOWN",
        "xi_eq_centralizer": "UNKNOWN", "E_eq_6_An": "UNKNOWN", "mcov_status": "UNKNOWN",
        "N_prime_partner": "",
        "note": "dim coker psi_V = 1 over F2(裁定451・射影加群はW=<(1,1,1)>=F2に精密化)。d_Nは紙で確定=3つ目の標的死(裁定463)。較正controlへ転役(裁定447/451/463)。coker≠0の希少な確認済み実例。",
        "source_cert": "narrative:LEDGER裁定446/451/463(地図.md P6行)",
    },
    {
        "window_id": "W6-cand-elementary5(62500)", "type": "W6-roof-candidate(K5 campaign, killed)", "n": "UNKNOWN",
        "N_ord": "UNKNOWN", "N_ord_factor_type": "UNKNOWN", "exponent_band": "62500",
        "G_order": 62500, "kernel_order": "UNKNOWN", "kernel_struct": "UNKNOWN",
        "kernel_abelian": "UNKNOWN", "kernel_solvable": "UNKNOWN", "derived_length": "UNKNOWN",
        "xi_eq_centralizer": "UNKNOWN", "E_eq_6_An": "UNKNOWN", "mcov_status": "UNKNOWN",
        "N_prime_partner": "",
        "note": "coker psi_V(N_theta,N_tau)=0=検出力ゼロで死亡(裁定446)。K5-GAP-1閉鎖に伴う標的死1件目。",
        "source_cert": "narrative:LEDGER裁定446(地図.md P6行)",
    },
    {
        "window_id": "W6-cand-p3(13500)", "type": "W6-roof-candidate(K5 campaign, killed)", "n": "UNKNOWN",
        "N_ord": "UNKNOWN", "N_ord_factor_type": "UNKNOWN", "exponent_band": "13500",
        "G_order": 13500, "kernel_order": "UNKNOWN", "kernel_struct": "UNKNOWN",
        "kernel_abelian": "UNKNOWN", "kernel_solvable": "UNKNOWN", "derived_length": "UNKNOWN",
        "xi_eq_centralizer": "UNKNOWN", "E_eq_6_An": "UNKNOWN", "mcov_status": "UNKNOWN",
        "N_prime_partner": "",
        "note": "coker psi_V(N_theta,N_tau)=0=検出力ゼロで死亡(裁定446)。K5-GAP-1閉鎖に伴う標的死2件目。",
        "source_cert": "narrative:LEDGER裁定446(地図.md P6行)",
    },
    {
        "window_id": "W-5(entangled roof, Arf-type)", "type": "roof(entangled, NON-SPLIT candidate)", "n": "UNKNOWN",
        "N_ord": 20, "N_ord_factor_type": "mixed-2-and-odd(2^2x5)", "exponent_band": "1000",
        "G_order": 1000, "kernel_order": "UNKNOWN", "kernel_struct": "UNKNOWN",
        "kernel_abelian": "UNKNOWN", "kernel_solvable": "UNKNOWN", "derived_length": "UNKNOWN",
        "xi_eq_centralizer": "UNKNOWN", "E_eq_6_An": "UNKNOWN", "mcov_status": "UNKNOWN",
        "N_prime_partner": "",
        "note": "isolated=TRUE確定(裁定482・80/80 settled・|GT(W-5)|=80)。付録A=ENT-1と3軸で走査域外・非分裂4行証明(裁定476)。機構=G5/Q8の同一C2^2商の対角潰れ(裁定473)。|PB3/N|=1000・N_ord=20は裁定473で訂正済(旧記載4000/40は誤り)。工房で最も具体的な非分裂拡大の実例。",
        "source_cert": "narrative:LEDGER裁定472/473/476/482(地図.md 帯1近傍・W-6札)",
    },
]


def main():
    if not os.path.exists(CSV_PATH):
        raise SystemExit("run extract_features.py first")
    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
        existing = list(csv.DictReader(f))
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in existing:
            w.writerow(r)
        for r in NARRATIVE_ROWS:
            for k in FIELDS:
                r.setdefault(k, "UNKNOWN")
            w.writerow(r)
    print("appended", len(NARRATIVE_ROWS), "narrative rows; total now",
          len(existing) + len(NARRATIVE_ROWS))


if __name__ == "__main__":
    main()
