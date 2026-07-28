#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/verify-i1-i3.py -- I-1/I-3 独立照合器(第二系統・pure python)

設計上の分離規律(CLAUDE.md「探索器と照合器の分離」):
  この照合器は GAP の出力した証明書(search/certs/i3_equality_20260728.json の
  生成元文字列)だけを入力とする。GAP のコード(search/*.g)や GAP 実行時の
  中間結果は import・参照しない。I-1 のパラメータ化(H_{j,alpha,beta})と
  G_n = (Z/n)^3 x| C2^2 の群構造は sol/sol_reply_73_math.md Q1.1/Q1.2 の
  紙上の式から本ファイルが独立に再実装する(GAP 側の MakeGn/MakeDn とは
  別の座標系・別のコード)。二系統一致は cross-checked であって「検証
  (verified)」ではない(その語は Lean に予約)。

構成:
  1. I-3: D4^3 x D3^3 を 21 点置換で実装し、証明書記載の生成元 2 つの像を
     BFS 閉包で構成、位数を再計算(GAP 非依存)。fail-closed 固定値
     expected=864(Sol 便 73 Q2 承認値)。6912 は erratum 旧値であり照合しない。
  2. I-1(部分照合): G_n = (Z/n)^3 x| C2^2 を直接実装し、H_{j,alpha,beta}
     (Sol 便 73 (1.2))の各群について述語 ①[P_n:H]=2n ②N_Pn(H)=H
     ③<X_n> が P_n/H 上推移的、および自己正規化を検査する。
     射程: 「列挙の完全性」(他に該当 H が無いこと)は照合しない
     (それは GAP 悉皆 + ODD-H 証明の担当)。

出力: search/certs/i1i3_crosscheck_20260728.json
u・c 平方類には一切触れない。
"""

import json
import hashlib
import itertools
import re
import sys
from datetime import datetime, timezone

REPO_ROOT = "C:/Users/81905/Desktop/shadow-atelier"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


# =====================================================================
# 1. I-3: D4^3 x D3^3 の 21 点置換実装(証明書の生成元文字列のみを入力)
# =====================================================================

def parse_gap_cycles(s):
    """GAP のサイクル記法 "(1,2,3)(4,5)" を [[1,2,3],[4,5]] へ変換する。"""
    cycles = []
    for grp in re.findall(r"\(([^)]*)\)", s):
        cycles.append([int(x) for x in grp.split(",")])
    return cycles


def perm_from_cycles(cycles, npoints):
    """1..npoints 上の置換をタプル(0 番要素はダミー)として返す。"""
    p = list(range(npoints + 1))
    for c in cycles:
        L = len(c)
        for i in range(L):
            p[c[i]] = c[(i + 1) % L]
    return tuple(p)


def perm_mult(p, q, npoints):
    """合成: (p*q)(i) = p(q(i))。"""
    return tuple([0] + [p[q[i]] for i in range(1, npoints + 1)])


def perm_identity(npoints):
    return tuple(range(npoints + 1))


def bfs_closure(gens, npoints):
    """有限群の生成元集合から群全体を BFS で構成し、要素集合(set of tuple)を返す。"""
    ident = perm_identity(npoints)
    elements = {ident}
    frontier = [ident]
    while frontier:
        e = frontier.pop()
        for g in gens:
            ne = perm_mult(e, g, npoints)
            if ne not in elements:
                elements.add(ne)
                frontier.append(ne)
            # 逆方向(g*e)も加える -- 非可換群での閉包を確実にするため両側から積む
            ne2 = perm_mult(g, e, npoints)
            if ne2 not in elements:
                elements.add(ne2)
                frontier.append(ne2)
    return elements


def run_i3_check(cert_path):
    with open(cert_path, "r", encoding="utf-8") as f:
        cert = json.load(f)

    x_pair_str = cert["generators"]["x_pair"]
    y_pair_str = cert["generators"]["y_pair"]
    npoints = 21

    x_cycles = parse_gap_cycles(x_pair_str)
    y_cycles = parse_gap_cycles(y_pair_str)
    x_perm = perm_from_cycles(x_cycles, npoints)
    y_perm = perm_from_cycles(y_cycles, npoints)

    elements = bfs_closure([x_perm, y_perm], npoints)
    image_size = len(elements)

    EXPECTED_FIXED = 864  # fail-closed 固定値(Sol 便 73 Q2 承認・erratum 済み 6912 は対象外)

    verdict = "CROSS_CHECK_PASS" if image_size == EXPECTED_FIXED else "CROSS_CHECK_FAIL"

    return {
        "schema": "i3-crosscheck/v1",
        "input_cert_path": "search/certs/i3_equality_20260728.json",
        "input_cert_sha256": sha256_file(cert_path),
        "generators_used": {
            "x_pair": x_pair_str,
            "y_pair": y_pair_str,
        },
        "npoints": npoints,
        "recomputed_image_size": image_size,
        "expected_fixed_value": EXPECTED_FIXED,
        "expected_fixed_value_note": (
            "Sol 便 73 Q2 承認値。証明書内 registered_target=6912 は odd 分岐の"
            "誤適用による erratum 済み旧値であり、本照合では比較対象にしない(fail-closed)。"
        ),
        "verdict": verdict,
        "old_registered_target_in_cert": cert.get("registered_target"),
        "old_registered_target_note": "erratum 済み旧値・照合対象外として記録するのみ",
    }


# =====================================================================
# 2. I-1: G_n = (Z/n)^3 x| C2^2 の直接実装(sol_reply_73_math.md Q1.1/Q1.2)
# =====================================================================
#
# Q = C2 x C2 の元を (e1,e2) in {0,1}^2 で表す。
#   1  = (0,0)
#   q1 = (1,0)
#   q2 = (0,1)
#   q3 = q1 q2 = (1,1)
#
# 符号表(sol_reply_73_math.md Q1.1):
#        a1   a2   a3
#   q1:  +    -    -
#   q2:  -    +    -
#   q3:  -    -    +
#
# これは sign_a1(e1,e2) = (-1)^e2, sign_a2(e1,e2) = (-1)^e1,
#        sign_a3(e1,e2) = (-1)^(e1+e2 mod 2)
# という閉じた式と同値である(q1=(1,0): a1 fixed(e2=0), a2 flip(e1=1),
# a3 flip(e1+e2=1) -- 表と一致。他の行も同様に検算できる)。
#
# 群の元は ((v1,v2,v3) mod n, (e1,e2)) のペア。
# 半直積の積: (v,q)(v',q') = (v + q(v'), q+q')  [q(v') は上の符号を成分ごとに掛ける]


def q_signs(q):
    e1, e2 = q
    s_a1 = -1 if e2 == 1 else 1
    s_a2 = -1 if e1 == 1 else 1
    s_a3 = -1 if (e1 + e2) % 2 == 1 else 1
    return (s_a1, s_a2, s_a3)


def q_add(q, qp):
    return ((q[0] + qp[0]) % 2, (q[1] + qp[1]) % 2)


def g_mult(a, b, n):
    (v, q) = a
    (vp, qp) = b
    s = q_signs(q)
    nv = tuple((v[i] + s[i] * vp[i]) % n for i in range(3))
    nq = q_add(q, qp)
    return (nv, nq)


def g_inv(a, n):
    (v, q) = a
    s = q_signs(q)
    nv = tuple((-s[i] * v[i]) % n for i in range(3))
    return (nv, q)


def g_identity():
    return ((0, 0, 0), (0, 0))


def g_pow(a, k, n):
    """a^k for k >= 0 (k < n は十分)。"""
    r = g_identity()
    base = a
    kk = k % n if k >= 0 else k  # alpha/beta は [0,n) で渡す想定
    for _ in range(kk):
        r = g_mult(r, base, n)
    return r


Q1 = (1, 0)
Q2 = (0, 1)
Q3 = (1, 1)


def elem(v1, v2, v3, q, n):
    return ((v1 % n, v2 % n, v3 % n), q)


def all_elements(n):
    for v1 in range(n):
        for v2 in range(n):
            for v3 in range(n):
                for q in [(0, 0), Q1, Q2, Q3]:
                    yield ((v1, v2, v3), q)


def subgroup_closure(gens, n):
    """gens から生成される部分群を BFS で完全に構成する(frozenset of elements)。"""
    ident = g_identity()
    elements = {ident}
    frontier = [ident]
    while frontier:
        e = frontier.pop()
        for g in gens:
            ne = g_mult(e, g, n)
            if ne not in elements:
                elements.add(ne)
                frontier.append(ne)
            ne2 = g_mult(g, e, n)
            if ne2 not in elements:
                elements.add(ne2)
                frontier.append(ne2)
    return frozenset(elements)


def make_H(j, alpha, beta, n):
    a1 = elem(1, 0, 0, (0, 0), n)
    a2 = elem(0, 1, 0, (0, 0), n)
    a3 = elem(0, 0, 1, (0, 0), n)
    a1_alpha = g_pow(a1, alpha, n)
    a1_beta = g_pow(a1, beta, n)
    if j == 2:
        gens = [a2, g_mult(a1_alpha, a3, n), g_mult(a1_beta, elem(0, 0, 0, Q2, n), n)]
    elif j == 3:
        gens = [a3, g_mult(a1_alpha, a2, n), g_mult(a1_beta, elem(0, 0, 0, Q3, n), n)]
    else:
        raise ValueError("j must be 2 or 3")
    H = subgroup_closure(gens, n)
    return H, gens


def check_predicates(H, gens, n, X):
    """述語 ①[P_n:H]=2n ②N_Pn(H)=H ③<X> が P_n/H 上推移的、を直接計算で判定する。

    ①: |P_n|=4n^3 と |H| から index を計算(H が実際に閉じた部分群であることは
       subgroup_closure の構成自体が保証する)。
    ②: brute force で全 g in P_n を走査し、H の生成元 3 個を conjugate して
       H に留まるかを確認する(生成元が全て H に収まれば、conjugate が
       準同型であることから <生成元の像> = H^g subseteq H、|H^g|=|H| より
       H^g = H が従うので、生成元だけの確認で ②の判定として十分)。
       全要素チェックだと n=11 で計算コストが過大になるため、この縮約を用いる
       (縮約自体は素朴な自己正規化の定義から導かれる標準的な事実であり、
       GAP 側 helper の共有ではない)。
    ③: 命題 ODD-H (1.4) の紙上の同値 「<X> が P_n/H 上推移的 <=> <X> cap H = 1」
       を用いず、愚直に <X> の軌道(coset)を数える方式で独立に確認する
       (<X> cap H = 1 を仮定せず、実際に coset を辿って軌道長を数える)。
    """
    order_pn = 4 * n ** 3
    index = order_pn / len(H)
    p1 = (index == 2 * n)

    # p2: 自己正規化を brute force で判定(H の全要素を conjugate)。
    #     H^g subseteq H を確認できれば(|H^g|=|H| なので) H^g = H。
    #     g in H は自明に normalize するので、g not in H のみ走査し早期終了する。
    self_normalizing = True
    for g in all_elements(n):
        if g in H:
            continue
        ginv = g_inv(g, n)
        conj_in_H = True
        for h in gens:
            # g h g^-1 の型: 半直積の共役は g*h*g^-1 で計算する
            c = g_mult(g_mult(g, h, n), ginv, n)
            if c not in H:
                conj_in_H = False
                break
        if conj_in_H:
            self_normalizing = False
            break

    # p3: <X> の軌道を coset 上で愚直に数える。
    #     coset の代表元集合を保持し、X^k (k=0,1,2,...) がどの既知 coset に
    #     属するかを都度 H 経由で判定する。
    ident = g_identity()
    coset_reps = [ident]  # 既知の coset 代表(eH からスタート)
    cur = ident
    order_X = None
    xk = ident
    seen_order = 0
    max_iter = 4 * n  # 安全弁(理論上 ord(X)=2n)
    orbit_size = 1
    for k in range(1, max_iter + 1):
        xk = g_mult(xk, X, n)
        if xk == ident:
            order_X = k
            break
        # xk H が coset_reps のどれかと同じか判定
        is_new = True
        for rep in coset_reps:
            rep_inv = g_inv(rep, n)
            diff = g_mult(rep_inv, xk, n)
            if diff in H:
                is_new = False
                break
        if is_new:
            coset_reps.append(xk)
            orbit_size += 1
    transitive = (orbit_size == 2 * n)

    return {
        "p1_index_2n": p1,
        "p2_self_normalizing": self_normalizing,
        "p3_transitive": transitive,
        "order_X_measured": order_X,
        "orbit_size_measured": orbit_size,
        "index_measured": index,
        "H_order": len(H),
    }


def run_i1_check(universe):
    per_n = []
    for n in universe:
        a1 = elem(1, 0, 0, (0, 0), n)
        X = g_mult(a1, elem(0, 0, 0, Q1, n), n)

        qualifying_count = 0
        qualifying_alpha_nonzero_count = 0
        alpha_zero_all_fail_self_norm = True
        alpha_nonzero_all_pass = True
        details = []

        for j in (2, 3):
            for alpha in range(n):
                for beta in range(n):
                    H, gens = make_H(j, alpha, beta, n)
                    res = check_predicates(H, gens, n, X)
                    qualifies_123 = res["p1_index_2n"] and res["p2_self_normalizing"] and res["p3_transitive"]
                    if qualifies_123:
                        qualifying_count += 1
                        if alpha != 0:
                            qualifying_alpha_nonzero_count += 1

                    if alpha == 0:
                        if res["p2_self_normalizing"]:
                            alpha_zero_all_fail_self_norm = False
                    else:
                        # alpha != 0 -> 期待: 述語1,3 は成立、かつ自己正規化も成立
                        if not (res["p1_index_2n"] and res["p3_transitive"] and res["p2_self_normalizing"]):
                            alpha_nonzero_all_pass = False

                    details.append({
                        "j": j, "alpha": alpha, "beta": beta,
                        "p1": res["p1_index_2n"], "p2": res["p2_self_normalizing"],
                        "p3": res["p3_transitive"],
                    })

        expected_alpha_nonzero_count = 2 * n * (n - 1)  # Sol 便 73 (1.7)
        per_n.append({
            "n": n,
            "expected_alpha_nonzero_qualifying_count": expected_alpha_nonzero_count,
            "measured_qualifying_count": qualifying_count,
            "measured_qualifying_alpha_nonzero_count": qualifying_alpha_nonzero_count,
            "matches_expected_count": (qualifying_alpha_nonzero_count == expected_alpha_nonzero_count
                                       and qualifying_count == expected_alpha_nonzero_count),
            "alpha_zero_all_self_normalizing_fail": alpha_zero_all_fail_self_norm,
            "alpha_nonzero_all_qualify_and_self_normalizing": alpha_nonzero_all_pass,
        })
        print(f"n={n}: qualifying={qualifying_count} (期待 {expected_alpha_nonzero_count}), "
              f"alpha=0 全て自己正規化NG={alpha_zero_all_fail_self_norm}, "
              f"alpha!=0 全て該当かつ自己正規化={alpha_nonzero_all_pass}")

    return {
        "schema": "i1-partial-crosscheck/v1",
        "universe": universe,
        "scope_note": (
            "これは「列挙の完全性」(他に該当 H が無いこと)の照合ではない。"
            "H_{j,alpha,beta} (sol_reply_73_math.md (1.2)) というパラメータ化族の"
            "各員について述語①②③+自己正規化を直接計算で確認したものであり、"
            "GAP 悉皆列挙(SubgroupsSolvableGroup)+ODD-H 証明が担当する"
            "「他に該当 H が無い」ことの証拠ではない。"
        ),
        "results": per_n,
    }


def main():
    print("=" * 70)
    print("I-3 独立照合(GAP 非依存・python BFS closure)")
    print("=" * 70)
    i3_cert_path = f"{REPO_ROOT}/search/certs/i3_equality_20260728.json"
    i3_result = run_i3_check(i3_cert_path)
    print(json.dumps(i3_result, ensure_ascii=False, indent=2))

    print()
    print("=" * 70)
    print("I-1 独立照合(部分・GAP 非依存・python 直接実装)")
    print("=" * 70)
    universe = [3, 5, 7, 9, 11]
    i1_result = run_i1_check(universe)

    script_path = f"{REPO_ROOT}/search/verify-i1-i3.py"
    out = {
        "schema": "i1i3-crosscheck/v1",
        "generated_by": {
            "tool": f"python {sys.version.split()[0]}",
            "script": "search/verify-i1-i3.py",
        },
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "i3": i3_result,
        "i1": i1_result,
        "note_discipline": (
            "探索器(GAP)と照合器(この python)は helper を共有しない。"
            "本ファイルの群構造実装(g_mult/g_pow/subgroup_closure 等)は"
            "GAP 側の MakeGn/MakeDn とは独立に、sol_reply_73_math.md の"
            "紙上の式から書き起こした。u・c 平方類・c_mu には触れていない。"
        ),
    }

    out_path = f"{REPO_ROOT}/search/certs/i1i3_crosscheck_20260728.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    # スクリプト自身のハッシュは書き出し後に別途計算して追記する(自己参照ハッシュは
    # 書き出し前には確定できないため、二段書きにする)。
    script_sha = sha256_file(script_path)
    out["provenance"] = {"script_sha256": script_sha}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print()
    print(f"証明書を書き出した: {out_path}")


if __name__ == "__main__":
    main()
