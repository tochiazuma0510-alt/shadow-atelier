#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""命題 PH2-VOID の検算 + (3.60) blast radius の数値点検。

Sol の producer/checker は import しない(独立実装)。
Thm 4.3 (4.12) の座標だけを自前で書き、屋根模型
    ROOF(l) = GT(K^(l)) x_U GT(N_S4),  U = (Z/18)^x, |fibre| = 9
    R((e,s)) = (e mod K^(9), s)   <- S4 座標は恒等
のもとで |Im R| を計算し、恒等式
    |Im R_l| = |Im(GT(K^(l)) -> GT(K^(9)))| * 9
を確認する。あわせて Thm 4.3 の dihedral reduction の全射性を実測する。
"""
import json
import math

UNITS18 = (1, 5, 7, 11, 13, 17)


def kappa(m):
    return m + 1 if m % 2 else -m


def gt_dih(n):
    """2405 Thm 4.3 (4.12) の座標集合 (m mod n_ord, k mod k_period)。"""
    n_ord = math.lcm(n, 2)
    k_period = n // math.gcd(n, 2)
    out = set()
    for m in range(n_ord):
        if math.gcd(2 * m + 1, n_ord) != 1:
            continue
        for k in range(k_period):
            if n % 4 == 0 and (k - kappa(m) // 2) % 2:
                continue
            out.add((m, k))
    return out


def red(e, target):
    return (e[0] % math.lcm(target, 2), e[1] % target)


def u18(e):
    return (2 * (e[0] % 18) + 1) % 18


def roof_image(l):
    """屋根模型での像。S4 座標 = (u, translation), u=u18 で fibre 積。"""
    src = gt_dih(l)
    dom, img = 0, set()
    for e in src:
        ue = u18(e)
        for u, tr in ((u, tr) for u in UNITS18 for tr in range(9)):
            if u == ue:
                dom += 1
                img.add((red(e, 9), u, tr))
    return len(src), dom, len(img)


def gn_order(n):
    return 4 * n ** 3 if n % 2 else 4 * (n // 2) ** 3


def main():
    out = {}
    tgt9 = gt_dih(9)
    out["|GT(K^(9))| (= 標的 dihedral 座標数)"] = len(tgt9)
    out["|GT(N_S4)| 模型 (6 x 9)"] = len(UNITS18) * 9

    rows = {}
    for l in (9, 27, 36, 45, 54, 63, 72, 81, 108, 135, 162):
        src = gt_dih(l)
        im = {red(e, 9) for e in src}
        n_src, dom, img = roof_image(l)
        rows[l] = {
            "|GT(K^(l))|": n_src,
            "|Im(GT(K^(l))->GT(K^(9)))|": len(im),
            "dihedral_reduction_surjective": len(im) == len(tgt9),
            "roof_size": dom,
            "|Im R| (屋根模型)": img,
            "恒等式 |Im R| = |Im_dih| * 9": img == len(im) * 9,
        }
    out["depth_table"] = rows
    out["★ 全 l で |Im R| = 972 か"] = all(r["|Im R| (屋根模型)"] == 972 for r in rows.values())
    out["★ 全 l で dihedral reduction 全射か"] = all(r["dihedral_reduction_surjective"] for r in rows.values())

    # 屋根の位数(直積分解の帰結)
    out["roof_orders_G_l_x_504"] = {l: gn_order(l) * 504 for l in (9, 27, 36, 108)}
    out["|B3/M| = |G_9| x |PSL(2,8)|"] = {
        "G_9": gn_order(9), "PSL28": 504, "product": gn_order(9) * 504,
    }
    # G_l の位数はすべて 2^2 * 3^k か(=可解・7 を含まない ⟹ PSL(2,8) を商に持てない)
    fac = {}
    for l in (9, 27, 36, 81, 108):
        v = gn_order(l)
        d = {}
        for p in (2, 3, 5, 7):
            e = 0
            while v % p == 0:
                v //= p
                e += 1
            d[p] = e
        d["残り"] = v
        fac[l] = d
    out["|G_l| の素因数分解(7 の指数が 0 なら PSL(2,8) 商は不可能)"] = fac

    # (3.60) 旧 helper の方向性: modBase = coarseOrd/2 は真の法より粗い ⟹ 候補は上位集合
    coarse, fine = 18, 54
    for m0 in (0,):
        correct = [mm for mm in range(fine) if mm % coarse == m0 % coarse and math.gcd(2 * mm + 1, fine) == 1]
        legacy = [mm for mm in range(fine) if mm % (coarse // 2) == m0 % (coarse // 2) and math.gcd(2 * mm + 1, fine) == 1]
        out["(3.60) 方向性 (coarseOrd=18, fineOrd=54, m=0)"] = {
            "correct_candidates": correct,
            "legacy_candidates": legacy,
            "legacy は correct の上位集合": set(correct) <= set(legacy),
            "余分に混入した数": len(legacy) - len(correct),
            "帰結": "旧 helper は偽陽性のみを生む(|Im R| の過大評価側)",
        }

    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
