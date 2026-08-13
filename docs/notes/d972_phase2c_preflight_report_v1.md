# D972 Phase 2c — 非完全候補の前件ゲート報告 v1

日付: 2026-08-13。仕様正本は `docs/notes/c1p5_v2_diff_review_v1.md`。候補を

\[
E=P\times C_3,qquad P=\mathrm{PSL}(2,8),qquad |E|=1512
\]

に固定し、測定前の三前件と PH2-VOID′ の停止条件を順に調べた。u/c、封印 K5、既存の事前登録量には触れていない。

## 1. E-1

`d972_phase2_void_addendum_v2.md` §3 の散文式だけを `d972_phase2_void_addendum_v2_1.md` で訂正した。正しい式は

\[
|GT(K^{(l)})|=2n_0\varphi(n_0),\qquad
n_0=l/\gcd(l,2)
\]

である。旧表と旧 cert の全数値は変更していない。$4(l/2)^3$ は偶数レベルの $|G_l|$ であって shadow count ではない。

## 2. 候補と marking

$PB_3=F_2\times\langle c\rangle$ の marked generators を $x,y,c$ とする。対角写像

\[
\delta:PB_3\longrightarrow C_3,qquad
\delta(x)=\delta(y)=1,quad\delta(c)=0
\]

と標準の $PB_3\twoheadrightarrow P$ を組み合わせた。機械生値は

| 量 | 生値 |
|---|---:|
| $|P|$ | 504 |
| $|E|$ | 1512 |
| $|[E,E]|$ | 504 |
| $|E^{\mathrm{ab}}|$ | 3 |
| $[E,E]=\ker(E\to C_3)$ | true |
| $\langle x,y\rangle=E$ | true |

である。従って候補自体は非完全で、可換化は $C_3$ である。

ここで $E=P\times C_3$ が split であることは設計どおりであり、候補 $E$ 自身の非分裂性は要求していない。目的は $E$ の非完全性である。$P$ の Schur 乗数が自明であることを別の拡大探索へ読み替えず、後段で調べるのは $G_l$ と $E$ の間の純商が直積かどうかだけである。

## 3. 前件① — $K^{(l)}\subseteq\ker\delta$

包含は、$\delta$ が $PB_3/K^{(l)}=G_l$ を経由することと同値である。ところが標準 marking は、全ての正整数 $l$ について座標ごとに

\[
xyx=x^{-1}yx^{-1},\qquad yxy=y^{-1}xy^{-1}
\tag{2}
\]

を満たす。$G_l\to C_3$ の任意の写像に (2) を入れると、加法記法で

\[
4\delta(x)=4\delta(y)=0.
\]

$4\equiv1\pmod3$ なので $\delta(x)=\delta(y)=0$ しかない。従って対角 assignment $(1,1)$ はどの $G_l$ にも降りず、

\[
\boxed{\{l>0:K^{(l)}\subseteq\ker\delta\}=\varnothing.}
\]

登録 12 レベルでは SymPy permutation group と標準ライブラリだけの tuple permutation checker が別々に (2) と最初の Cayley 衝突を再現した。

| $l$ | $|G_l|$ | $|[G_l,G_l]|$ | $|G_l^{\rm ab}|$ | 包含生値 |
|---:|---:|---:|---:|:---:|
| 9 | 2916 | 729 | 4 | false |
| 27 | 78732 | 19683 | 4 | false |
| 36 | 23328 | 1458 | 16 | false |
| 45 | 364500 | 91125 | 4 | false |
| 54 | 78732 | 19683 | 4 | false |
| 63 | 1000188 | 250047 | 4 | false |
| 72 | 186624 | 11664 | 16 | false |
| 81 | 2125764 | 531441 | 4 | false |
| 108 | 629856 | 39366 | 16 | false |
| 126 | 1000188 | 250047 | 4 | false |
| 135 | 9841500 | 2460375 | 4 | false |
| 162 | 2125764 | 531441 | 4 | false |

有限表は全レベル主張の根拠ではなく、式 (2) に対する登録宇宙内の機械側 receipt である。

## 4. 前件② — $N_E$ の isolated 性

$[E,E]=P\times1$ の 504 元と charming な $m\bmod9$ の 6 値を全走査した。

| 段 | 生値 |
|---|---:|
| raw candidate | 3024 |
| hexagon (3.10) で除外 | 2640 |
| hexagon (3.11) で除外 | 330 |
| generation で除外 | 0 |
| shadow | 54 |
| direct marked endomorphism が well-defined | 54/54 |
| 同 endomorphism の像サイズ | 1512 (全 54 件) |
| settled | 54/54 |

各 shadow image について、marked Cayley graph 上に $E\to E$ を直接延長し、1512 元全てで矛盾がなく像も 1512 元であることを調べた。producer と helper 非共有 checker の生値が一致し、`N_E_isolated=true` となった。

## 5. 前件③ — $\theta,\tau$ 不変性

$z=(xy)^{-1}$ とし、marked maps

\[
\theta:(x,y)\mapsto(y,x),\qquad
\tau:(x,y)\mapsto(y,z)
\]

を $E$ の全 1512 元へ延長した。生値は

| 量 | 生値 |
|---|:---:|
| $\theta$ well-defined / bijective | true / true |
| $\tau$ well-defined / bijective | true / true |
| $(\delta(x),\delta(y),\delta(z))$ | $(1,1,1)$ |
| $\delta\circ\theta=\delta$ on all $E$ | true |
| $\delta\circ\tau=\delta$ on all $E$ | true |

であり、PSL marking と対角成分を組み合わせた $N_E$ は両作用で不変である。

## 6. PH2-VOID′ 非積ゲート

候補側の $E^{\rm ab}=C_3$ は立ったが、前件①の全レベル論証により $G_l$ は $C_3$ 商を持たない。また $G_l$ は可解なので非可換単純群 $P$ を商に持たない。$P\times C_3$ の正規商を調べると、両群に共通する非自明商は無い。Goursat の部分直積記述から

\[
PB_3/(K^{(l)}\cap N_E)\cong G_l\times(P\times C_3)
\qquad(l>0)
\]

となる。従って非積ゲートの要求生値は false、純商直積の生値は true、`PH2_VOID_prime_applies=true` である。

ここで停止規則を適用した。スペクトル・分岐先の事前登録は作らず、reduction image set も作っていない。

| 測定欄 | 生値 |
|---|---|
| preregistration created | false |
| measurement authorized | false |
| measurement performed | false |
| reduction image set formed | false |
| $|\operatorname{Im}R|$ raw | null (未測定) |
| 状態 | UNKNOWN |
| 有限深度 B 型認定 | false |

非完全性だけでは足りず、選んだ $C_3$ quotient が実際に $G_l$ と共通であることが独立の必須条件だった。この候補はその条件で止まる。Schur 乗数や非分裂拡大の探索へ宇宙を広げていない。

## 7. 任意 helper 欄

今後の直積族用に、PH2-VOID′ の算術だけを cert 内の fixture として置いた。

\[
\text{roof raw}=18\cdot\text{target internal image count},qquad
18\mapsto324,quad54\mapsto972.
\]

これは Phase 2c の像測定には使用していない。

## 8. 再現

```powershell
python search/d972_phase2c_preflight_v1.py --hard-timeout-seconds 900
python search/check_d972_phase2c_preflight_v1.py --hard-timeout-seconds 900
```

- `search/certs/d972_phase2c_preflight_v1_20260813.json`
- `search/certs/d972_phase2c_preflight_v1_check_20260813.json`
- `search/certs/d972_phase2c_preflight_v1_checkpoint.json`
- `search/certs/d972_phase2c_preflight_v1_check_checkpoint.json`

producer は SymPy permutation group を用い、checker は標準ライブラリの tuple permutations のみを用いた。checker は producer を import していない。両系統とも u/c と K5 のファイルを入力にしていない。
