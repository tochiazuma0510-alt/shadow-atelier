# D972 Phase 2 — PH2-VOID addendum v2.1

日付: 2026-08-13。`d972_phase2_void_addendum_v2.md` の §3 にある散文式だけを訂正する版である。表と既存 cert の全数値は変更しない。

## 1. 命題 PH2-VOID

$9\mid l$ で $K^{(l)}\subseteq K^{(9)}$ となる admissible level を取る。`triad972_canonical_addendum_v2.md` 式 (5) により

\[
GT(K^{(l)}\cap N_{S4})
=GT(K^{(l)})\times_U GT(N_{S4}).
\]

reduction は S4 座標を恒等に保つ。各 $u\in U$ 上の S4 fibre は常に 9 個なので

\[
|\operatorname{Im}R|
=|\operatorname{Im}(GT(K^{(l)})\to GT(K^{(9)}))|\cdot9.
\tag{1}
\]

Thm. 4.3 の dihedral reduction は全射で、右辺の第一因子は 108。従って

\[
\boxed{|\operatorname{Im}R|=108\cdot9=972}
\tag{PH2-VOID}
\]

が全 admissible level で成り立つ。

## 2. 完全直積が原因であること

$G_l=PB_3/K^{(l)}$ は可解、$P=PB_3/N_{S4}\cong\mathrm{PSL}(2,8)$ は非可換単純である。共通の非自明商が無いので

\[
PB_3/(K^{(l)}\cap N_{S4})\cong G_l\times P.
\]

従って dihedral 因子を深めても $P$ 座標には作用しない。旧 324 分岐はこの族では到達不能であり、停止規則から撤回する。SINGLE-BIT の具体判定をこの族で行うことはできず、全体の状態は **UNKNOWN** である。

## 3. v2.1 の raw table と E-1 訂正

producer/checker は次の 12 level を別の coordinate representation で数えた。

| $l$ | 9 | 27 | 36 | 45 | 54 | 63 | 72 | 81 | 108 | 126 | 135 | 162 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| $|GT(K^{(l)})|$ | 108 | 972 | 216 | 2160 | 972 | 4536 | 864 | 8748 | 1944 | 4536 | 19440 | 8748 |
| dihedral 像 | 108 | 108 | 108 | 108 | 108 | 108 | 108 | 108 | 108 | 108 | 108 | 108 |
| roof raw 像 | 972 | 972 | 972 | 972 | 972 | 972 | 972 | 972 | 972 | 972 | 972 | 972 |

shadow count の正しい一様式は

\[
\boxed{
|GT(K^{(l)})|=2n_0\varphi(n_0),\qquad
n_0=\begin{cases}
l,&l\text{ が奇数},\\
l/2,&l\text{ が偶数}
\end{cases}}
\tag{E-1}
\]

である。特に $l=126$ では $n_0=63$ なので $2\cdot63\cdot\varphi(63)=4536$。v2 §3 の「$2l\varphi(l/2)$」は散文式だけの誤記であり、$4(l/2)^3$ は shadow count ではなく $|G_l|$ の偶数レベル公式である。上表および既存の producer/checker/cert はこの訂正値を既に用いており、変更しない。

## 4. 旧 cert の位置づけ

- `d972_phase2_coord_v1.py` の producer と checker は helper を共有しないが、どちらも同じ fibre-product 意味論を実装していた。従って上限は **cross-checked(model-only)** である。
- roof 模型そのものの等式は canonical addendum v2 の純商直積と $F_2$ 分解で紙前件を補った。
- 旧 Phase 1 の `coarseOrd/2` は候補を過大にする向きの座標瑕疵で、旧 cert は superseded。修理後の raw 972 は値として再現したが、PH2-VOID により情報量はない。
- P-PH2-1 の $l=81$ raw 972 も予測的データではなく、式 (PH2-VOID) の定理再導出である。
- Phase 2 cert が旧 Phase 1 cert の SHA を束縛していても、履歴 binding であり数学的根拠には使わない。

## 5. 証明書と再現

```powershell
python search/d972_phase2_void_v2.py --hard-timeout-seconds 900
python search/check_d972_phase2_void_v2.py
```

- `search/certs/d972_phase2_void_v2_20260813.json`
- `search/certs/d972_phase2_void_v2_check_20260813.json`
- `search/certs/d972_phase2_void_v2_checkpoint.json`

有限表は模型内の照合、全 level への延長と直積は紙の証明である。有限深度 B 型認定は行わない。

