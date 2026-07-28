#!/usr/bin/env python3
# search/kerchi-abelianization-check.py
#
# 数学者(Opus 5)の検算スクリプト -- docs/notes/kerchi_equality_v1.md 用。
# 登録掃引ではない(宇宙の事前登録は不要 -- 既存証明書の再解析のみ・新規列挙なし)。
#
# 目的: 既存証明書 certificates/*.json の **shadow 水準 composition_table**((3.53) で構成)
#       から、各窓 N について
#         (a) chi~_{2M}: [m,f] -> 2m+1 mod 2*N_ord  が群準同型か(fail-closed assert)
#         (b) |ker chi~| と Im chi~
#         (c) [GT(N), GT(N)](交換子部分群)
#         (d) 等号 ker chi~ = [GT,GT] の成否
#       を測る。**Phi 像は一切使わない**(C2F の教訓・宇宙登録 v1.1 (2b))。
#
# 実行: python search/kerchi-abelianization-check.py   (リポジトリ直下から)
# 依存: 標準ライブラリのみ。GAP 不要(全群 |GT| <= 312)。

import json, glob, os, sys
from math import gcd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def phi(n):
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


def load_group(path):
    """composition_table を持つ証明書から (mul, m_list, N_ord) を返す。無ければ None。"""
    d = json.load(open(path, encoding='utf-8'))
    if 'composition_table' not in d or not d['composition_table']:
        return None
    sh, ct = d['shadows'], d['composition_table']
    n = len(sh)
    mul = [[None] * n for _ in range(n)]
    for a, b, c in ct:
        assert mul[a][b] is None, ('duplicate entry', path, a, b)
        mul[a][b] = c
    assert all(all(x is not None for x in row) for row in mul), ('incomplete table', path)
    return mul, [s['m'] for s in sh], d['target']['invariants']['N_ord']


def analyze(path):
    got = load_group(path)
    if got is None:
        return None
    mul, m, Nord = got
    n = len(m)

    # --- 群の公理(fail-closed) ---
    ids = [i for i in range(n)
           if all(mul[i][j] == j for j in range(n)) and all(mul[j][i] == j for j in range(n))]
    assert len(ids) == 1, ('identity', path, ids)
    e = ids[0]
    assert all(mul[mul[i][j]][k] == mul[i][mul[j][k]]
               for i in range(n) for j in range(n) for k in range(n)), ('assoc', path)
    inv = [next(j for j in range(n) if mul[i][j] == e) for i in range(n)]

    # --- (3.53) 第一成分の再現(表が本当に GT-shadow 合成か) ---
    assert all((2 * m[i] * m[j] + m[i] + m[j]) % Nord == m[mul[i][j]] % Nord
               for i in range(n) for j in range(n)), ('(3.53) first component', path)

    # --- chi~ at level 2M ---
    L = 2 * Nord
    chit = [(2 * x + 1) % L for x in m]
    assert all(chit[mul[i][j]] == chit[i] * chit[j] % L
               for i in range(n) for j in range(n)), ('chi~ not a homomorphism', path)
    ker = {i for i in range(n) if chit[i] == 1 % L}
    img = sorted(set(chit))
    units = [u for u in range(L) if gcd(u, L) == 1]

    def closure(gens):
        S = {e} | set(gens)
        fr = list(S)
        while fr:
            x = fr.pop()
            for y in list(S):
                for z in (mul[x][y], mul[y][x]):
                    if z not in S:
                        S.add(z); fr.append(z)
        return S

    D = closure({mul[mul[i][j]][mul[inv[i]][inv[j]]] for i in range(n) for j in range(n)})
    # [GT, F_0] (coinvariant の分母)
    C = closure({mul[mul[g][x]][mul[inv[g]][inv[x]]] for g in range(n) for x in ker})

    return dict(name=os.path.basename(path).split('.')[0], order=n, N_ord=Nord,
                phi2N=phi(L), ker=len(ker), img=len(img), img_full=(len(img) == len(units)),
                D=len(D), D_in_ker=(D <= ker), equal=(D == ker),
                coinv=len(ker) // len(C), ker_abelian=all(mul[i][j] == mul[j][i] for i in ker for j in ker),
                count_id=(len(ker) * phi(L) == n))


def main():
    rows = [r for r in (analyze(p) for p in sorted(glob.glob(os.path.join(REPO, 'certificates', '*.json')))) if r]
    hdr = ['name', '|GT|', 'N_ord', 'phi(2N)', '|ker|', '|Im|', 'Im=full', '|[G,G]|',
           'EQUAL', '|(F0)_Q|', 'kerAb', 'count_id']
    print('| ' + ' | '.join(hdr) + ' |')
    print('|' + '---|' * len(hdr))
    for r in rows:
        print('| {name} | {order} | {N_ord} | {phi2N} | {ker} | {img} | {img_full} | {D} | '
              '{equal} | {coinv} | {ker_abelian} | {count_id} |'.format(**r))
    print()
    print('windows analysed          :', len(rows))
    print('EQUALITY FAILS            :', [r['name'] for r in rows if not r['equal']] or 'none')
    print('chi~ NOT surjective       :', [r['name'] for r in rows if not r['img_full']] or 'none')
    print('|ker|*phi(2N) != |GT|     :', [r['name'] for r in rows if not r['count_id']] or 'none')
    print('[G,G] NOT inside ker      :', [r['name'] for r in rows if not r['D_in_ker']] or 'none')
    return 0


if __name__ == '__main__':
    sys.exit(main())
