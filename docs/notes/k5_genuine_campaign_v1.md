# $K^{(5)}$ genuine 判定戦役 — 設計と IF-FIRST 予言凍結 v1

**状態札: `design / IF-FIRST 凍結宣言 / 実測ゼロ / Sol 未監査 / 発火認可待ち`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01
- 委嘱: 司令塔(**裁定 407** の戦略反転 = 系 FAKE-LIFT の極小元原理 ⟹ 次標的は $K^{(5)}$ 直撃・$\lvert\mathrm{GT}(K^{(5)})\rvert=40$ が最小)
- 様式: `docs/notes/roof2_cv9_freeze_v1.md`(R4b/roof2 の IF-FIRST 凍結様式)/ `docs/notes/gtpi_cv9_freeze_v1.md`
- **本ファイルは $\mathrm{Im}\,R_{N,K^{(5)}}$ を一度も測る前に固定する。実測結果によって書き換えない**(改訂が要るなら v2)。
- 入力正本: `docs/notes/div_law_v1.md`(計器)/ `docs/notes/ihnec_v1_addendum_e_fivebypass.md`+追記 F(戦略反転)/ `docs/notes/fam_u_v1_addendum_domain_restore.md`(domain 復帰)/ `docs/notes/ihnec_v1.md` §6+追補 D(SPLIT-NULL・(MCOV))/ `docs/notes/roof2_cv9_freeze_v1.md`(ENT-CRIT・NO-CENTRAL)/ 正典 2401.06870・2405.11725。

> ## 封印遵守の申告(**§6 が正本・スコープ照合は司令塔**)
> - **$K^{(5)}$ 窓そのものの封印は裁定 396/398 で解除済**(`fam_u_v1_addendum_domain_restore.md` §2.1)。本稿が $K^{(5)}$ の位数・座標・元を書くのは認可された行為である。
> - **本設計は次の 3 量に一切触れない**: ① **$\hat c_\mu$**(N∞ 枝の norm 定数・その平方類/平方因子/符号)② **PSL 窓の構造量**(`seal_PSL_v1` メタデータ水準 = case A/B の `gt_count`/`n_m`/`class_coefficient`/`settled_*`/`isolated`/`phi_image`/`normalizer_order`・rigidity 4 欄)③ **ε bits**(`epsbits_*` 系 = 壁キャンペーンの持上げ位数/P-bit)。
> - **本設計は曲線・dessin・Kummer・$u$ 値を一切使わない**。使うのは有限群 $B_3/M$ の中の hexagon 判定と $\mathbb Z$ 上の整数演算だけである。
> - ★ **ただし「触れない」と「干渉しない」は別である。** §6 に**推論水準の干渉**を 9 件列挙した(とくに X-1 は $K^{(5)}$ 算術飽和 manifest の封印予言 (P1) と**同じ 1 ビットの別層**である)。**採否・スコープ照合は司令塔の専権**であり、本稿は列挙のみ行う。
> - ⚠ **記号衝突を先に名指しする**(§6 N-1〜N-3): 本稿の $\varepsilon$($=m\bmod2$)は**封印語彙の「ε bits」ではない**。本稿の $K^{(5)}$ は証明書 `N5.v1.json`(= $c$ の位数 5 の control 窓)**ではない**。$K^{(10)}=K^{(5)}$(Prop 3.4)ゆえ `K10.v1.json` と `K5.v1.json` は**同一対象**であり二重計上禁止。

---

## 0. 先に結論(司令塔向け・6 行)

1. **測る量は 1 ビットである。** $n=5$ は素数ゆえ $d_{\rm gen}(5)\in\{1,5\}$、降下は高々 1 回(系 DIV-GEN(5))。$\mathrm{GT}_{\rm gen}(K^{(5)})$ は $H_1$(位数 8)か $T$(位数 40)のいずれか — **中間はない**(§1.4 で 40 元の完全列挙により機械確認)。
2. ★ **その 1 ビットは「1 個の元が持ち上がるか」に収縮する**(命題 K5-BIT・§2.3)。$\mathfrak F_0(K^{(5)})$ は**$m=0$ の繊維そのもの**であり、$d_N=5\iff[0,(r^2,r^{-2},1)]\in\mathrm{Im}\,R_{N,K^{(5)}}$。⟹ **$\mathrm{GT}(N)$ の全列挙は不要**・走査規模は 3 桁下がる(§4.3)。しかもこの収縮は**枠組み非依存**である。
3. ★★ **しかし現時点で発火できる検出力のある窓は 1 個も無い。** 二つの負の定理が候補族を尽くしている: **Dih 族は全滅**(命題 K5-DIH0・THM44-odd)、**分裂屋根も全滅**((AR) 相対・命題 K5-SPL0 = 系 DIV-SPLIT の $n=5$ 特化)。残るのは entangled 屋根だけで、**その構成は未着手**(【IHNEC-GAP-2】)。
4. ★★ **さらに悪い報せ(本稿の実質的発見)**: 「entangled(ENT-CRIT の正規補群なし)⟹ 検出力あり」は**偽**である。反例 = **$K^{(np)}$($p\mid n$ 素数)**。$n=5$ では $K^{(25)}$、そして **$n=3$ の実例 $K^{(9)}\to K^{(3)}$ は既存証明書で全射 12/12 と測定済**(命題 K5-ENT-INSUF・§3.4)。⟹ **`roof2_cv9_freeze_v1.md` §7.4 の標的 ENT-1 は、このままでは「もう 1 個の検出力ゼロ屋根」を作る恐れがある** — 発注前に篩(§3.6)を通すこと。
5. **さらに $n=5$ では最小の $B_3$-安定 entangled 核が $K^{(25)}$ に食われている**(命題 K5-MOD・§3.5): $\mathbb F_5[G_5]$ の既約は $\mathbf1,\chi_1,\chi_2,\chi_3$ の 4 個、$H^2(G_5,\mathbf1)=0$、$\{\chi_i\}$ は $S_3$ の 1 軌道 ⟹ 最小の $B_3$-安定非中心核は $\chi_1\oplus\chi_2\oplus\chi_3\cong A$(次元 3)で、それは**まさに $G_{25}\to G_5$ の核**である。⟹ 標的は「$H^2(G_5,A)^{S_3}$ の中の $[K^{(25)}]$ **以外**の類」へ具体化される(§3.6)。
6. **基準予言は $d_{\rm gen}(5)=5$(全 40 genuine)** = FV-SOLV が賭ける側。**ただし本戦役はそれを証明できない**((COR54) の壁・【IHNEC-GAP-1】)。**できるのは反証だけ**である。§4 は「何が出たら何が倒れるか」を対称に凍結した — とくに **$d_N=1$ が 1 個出れば、測定済の $\mathrm{ord}([u_5]_{10})=5$ と (RCYC) が同時に立たなくなる**(衝突行 X1)⟹ **$K^{(5)}$ は枠組み橋 $B_{\rm FC}$ に有限計算で触れる最初の窓**である(§4.4)。

---

## 1. 宇宙の事前登録(**走査前に固定・後から変えない**)

### 1.1 対象は 1 個

$$\boxed{\ T:=\mathrm{GT}(K^{(5)}),\qquad K^{(5)}=\ker\psi_5,\quad PB_3/K^{(5)}\cong G_5\ (\lvert G_5\rvert=500),\quad K^{(5)}_{\rm ord}=10,\ [B_3{:}K^{(5)}]=3000\ }$$

**Prop 3.4 の同一視**: $K^{(10)}=K^{(5)}$。⟹ `certificates/K10.v1.json` と `certificates/K5.v1.json` は**同一対象の 2 通の証明書**であり、**独立 2 例として二重計上しない**(`docs/manifest_k5_v1.md` 宇宙欄と同一規律)。

**他の窓は触らない**。§3 の候補族に挙げた窓も、**§4 の予言凍結までは一切列挙しない**。

### 1.2 入力(既存・再測定しない)

| 出所 | SHA-256 | 使う内容 |
|---|---|---|
| `certificates/K5.v1.json` | `b659cc18e1083b9aedf2d1d9ccf87424ca9fe9f3d1a4bbc19a369ffd4057c6d3` | 40 shadow・合成表 1600 対・逆元表・$N_{\rm ord}=10$・$[PB_3{:}]=500$・`derived_order`$=125$ |
| `certificates/K15.v1.json` | `08493ccec8f75469f681f7e1397a45364a1f4cdef9a1164ac498683cdbc102cc` | 240 shadow・$N_{\rm ord}=30$・$[PB_3{:}]=13500$(**Phase 1 の相手側**) |
| `certificates/K3.v1.json` | `d7cd44ea6d71e341e3e1a6164ce03540e92c50d405113ad1d3dc26972b1e8171` | 12 shadow(**アンカー**) |
| `docs/notes/div_law_v1.md` | `b94c3bd6341f97dcdaa6ff19580213f040182d2dc62c890d08c3ca1fe9e4444f` | 定理 DIV-LAW・補題 PIN-A/CHI・系 DIV-GEN/SPLIT・換算表 |
| `docs/notes/ihnec_v1_addendum_e_fivebypass.md` | `640b356cfa38f7d934acfec49d9a2bd434a91aaf5c6a9bcf21fb0d1bfd765119` | 系 THM43-odd・補題 THM44-odd・補題 GEN-DESC・系 FAKE-LIFT・追記 F |
| `docs/notes/roof2_cv9_freeze_v1.md` | `94ac28568674980558439b1a2dccb36cda2841fababb834eb8c9d1f2a3845915` | 定理 REFACT・命題 ENT-CRIT・補題 NO-CENTRAL |

**検算スクリプト**(整数演算 + 証明書読み出しのみ・**$\mathrm{Im}\,R$ の測定は 1 件も含まない**):

| script | SHA-256 | 内容 |
|---|---|---|
| `search/probe/wac_v1/k5gen_universe_check.py` | `c8b03bb049360c654e5a810edfa5a864b1b89a6674eb5045403270647e3674d1` | §1.3–1.5 の全事実(37 検査・**ALL PASS**) |
| `search/probe/wac_v1/k5gen_design_check.py` | `c2920227d36a8c261a7c46c7c9797ca45273efb460b1bddeae7dbd3f56ac87c2` | §3.4 の $K^{(np)}$ 反例(7 対 + 3 対照)・§3.5 の $H^*$ 指標計算・§4.3 の走査規模(**ALL PASS**) |

> ⚠ **格**: python 単系統。**cross-checked ではない。verified(Lean)でもない。** 証明書側の生成は GAP 単系統である。

### 1.3 構成法と座標(**系 THM43-odd の $n=5$ 特化**)

正典 2405 Thm 4.3 (4.12) + 工房補完(`ihnec_v1_addendum_e_fivebypass.md` §E-F.3.1 系 THM43-odd)より

$$\mathcal X_5=\{m\in\mathbb Z/10:\gcd(2m+1,10)=1\}=\{0,1,3,4,5,6,8,9\}\quad(\lvert\mathcal X_5\rvert=2\varphi(5)=8),$$
$$\varkappa(m)=\begin{cases}m+1&(m\ \text{奇})\\-m&(m\ \text{偶})\end{cases}\quad(4.9),\qquad
\mathrm{GT}(K^{(5)})=\bigl\{\bigl(m,\ (r^{2k},\,r^{-2k},\,r^{\varkappa(m)})\bigr)\ :\ m\in\mathcal X_5,\ k\in\mathbb Z/5\bigr\}.$$

$$\boxed{\ \lvert T\rvert=\lvert\mathcal X_5\rvert\cdot5=8\cdot5=\mathbf{40}=2n\varphi(n)\ }$$

**$\Theta_5$ 座標**(命題 E1-S1):
$$\Theta_5:T\ \xrightarrow{\ \sim\ }\ \mathrm{Aff}(\mathbb Z/5)\times C_2,\qquad[m,f]\mapsto(k,u,\varepsilon),\quad u=2m+1\bmod5,\ \ \varepsilon=m\bmod2,$$
$$(k_1,u_1,\varepsilon_1)(k_2,u_2,\varepsilon_2)=(k_1+u_1k_2,\ u_1u_2,\ \varepsilon_1+\varepsilon_2).$$
$k$ の復元: $f$-三つ組の第 1 成分 $r^{a_1}$ から $k=3a_1\bmod5$($2^{-1}=3$ in $\mathbb Z/5$)。

**$\widetilde\chi$ と $\mathfrak F_0$**: $\widetilde\chi=\widetilde\chi_{20}:[m,f]\mapsto2m+1\bmod20$、$Q:=(\mathbb Z/20)^\times=\{1,3,7,9,11,13,17,19\}$($\lvert Q\rvert=2\varphi(5)=8$)。
$$\boxed{\ \mathfrak F_0=\ker\widetilde\chi=\{[0,(r^{2k},r^{-2k},1)]:k\in\mathbb Z/5\}\cong C_5\ =\ \textbf{$m=0$ の繊維そのもの}\ }$$
($2m+1\equiv1\ (\mathrm{mod}\ 20)\iff m\equiv0\ (\mathrm{mod}\ 10)\iff m=0$;$\varkappa(0)=0$ ゆえ第 3 成分は $1$。)

$$T=\mathfrak F_0\rtimes Q^{\rm std},\qquad Q^{\rm std}=H_1=\{(0,u,\varepsilon)\}\ (\lvert H_1\rvert=8),\qquad H_5=T.$$

### 1.4 ★ 40 元の全数機械確認(証明書との突合)

`k5gen_universe_check.py` が `K5.v1.json` に対して行った検査(**すべて PASS**):

| # | 検査 | 結果 |
|---|---|---|
| **A** | $\lvert\mathcal X_5\rvert=8$・$\mathcal X_5=\{0,1,3,4,5,6,8,9\}$ | PASS |
| **B** | 証明書の 40 shadow・$N_{\rm ord}=10$・`thm46_expected_order`$=40$・$[PB_3{:}]=500$・`derived_order`$=125$ | PASS |
| **C** | **全 40 元**で `f_triple` が $(r^{2k},r^{-2k},r^{\varkappa(m)})$ の形(反射成分ゼロ・第 2 成分 $=-2k$・第 3 成分 $=\varkappa(m)$)。$\Theta_5$ は単射かつ $\mathbb Z/5\times(\mathbb Z/5)^\times\times C_2$ へ全単射 | PASS |
| **D** | ★ **合成表 1600 対すべて**で $(k,u,\varepsilon)$ の半直積法則が再現(mismatch 0)。単位元 $=[0,1]$、逆元表 $=$ アフィン逆 | PASS |
| **E** | $\iota=[m=9,f=1]$ が**証明書 index 1 に実在**、$\Theta_5(\iota)=(0,4,1)$、合成表上で $\iota^2=$ 単位元、$\widetilde\chi(\iota)=19\equiv-1\ (20)$ | PASS |
| **F** | $\widetilde\chi$ の像 $=(\mathbb Z/20)^\times$(8 値)・$\lvert\ker\rvert=5$・$\mathfrak F_0=\{(k,1,0)\}$・**合成表の上で** $\mathfrak F_0=\langle(1,1,0)\rangle\cong C_5$ | PASS |
| **G** | $H_1$ は合成表上で部分群・$\lvert H_1\rvert=8$・$H_1\cap\mathfrak F_0=\{e\}$・$\widetilde\chi(H_1)=Q$ 全像・$\iota\in H_1$・$[T{:}H_1]=5$ | PASS |
| **G7** | ★ **悉皆列挙**: $T$ の部分群のうち「$\widetilde\chi$ 全像 **かつ** $\iota$ を含む」ものは**ちょうど $\{H_1,T\}$ の 2 個**(サイズ 8 と 40) | PASS |
| **G8/G9** | **パリティ罠**の実物確認: $H^{\rm bad}=\{\varepsilon=0\}$ は部分群・$d=5$・指数 2・$\iota\notin H^{\rm bad}$・$\widetilde\chi(H^{\rm bad})=\{1,9,13,17\}$(位数 4 = **(CHI) 破れ**) | PASS |
| **I** | Prop 3.5 の近傍: $K^{(5)}\subseteq K^{(nn)}$ となる $nn\ge3$ は $\{5,10\}$ **のみ**。$K^{(q)}\subseteq K^{(5)}$ となる奇 $q$ は $5\mid q$ | PASS |

> ★ **(G7) の意味**: 定理 DIV-LAW の $n=5$ 特化を**分類定理としてではなく実物の悉皆列挙として**確認した。⟹ 以後「$\mathrm{Im}\,R$ は $H_1$ か $T$」という言明は、**(CHI)+(PIN)+部分群性を仮定した上での有限事実**であって、DIV-LAW の一般証明を信用する必要がない。

### 1.5 ★ 三状態しかない($K^{(5)}$ の完全な地図)

系 DIV-LAT の $n=5$ 特化: $d_{\rm arith}(5)\mid d_{\rm gen}(5)\mid5$、$5$ 素数ゆえ

| 状態 | $d_{\rm arith}$ | $d_{\rm gen}$ | 意味 | 帰結 |
|---|---|---|---|---|
| **(I)** | 5 | 5 | $\mathrm{GT}_{\rm arith}=\mathrm{GT}_{\rm gen}=T$ | **odd Conj 5.1 が窓 $n=5$ で成立**。fake 0・非算術証人 0 |
| **(II)** | 1 | 5 | $\mathrm{GT}_{\rm arith}=H_1$、全 40 genuine | fake 0 だが**非算術証人が 32 個**(B 型)⟹ (U-10) の下で **FAKE-KILL 発火 = ¬井原(全射部)** |
| **(III)** | 1 | 1 | $\mathrm{GT}_{\rm arith}=\mathrm{GT}_{\rm gen}=H_1$ | **fake が 32 個**($k\not\equiv0$ の全元)⟹ **ML-ODD (iii) が偽** ⟹ 系 FAKE-LIFT で $K^{(15)},K^{(25)},K^{(35)},\dots$ 全てが fake を含む |

($d_{\rm arith}=5,d_{\rm gen}=1$ は $d_{\rm arith}\mid d_{\rm gen}$ に反し不可能。fake 数 $=(5-d_{\rm gen})\cdot2\varphi(5)=8(5-d_{\rm gen})$、非算術証人数 $=(d_{\rm gen}-d_{\rm arith})\cdot8$。)

> **本戦役が測るのは (III) と {(I),(II)} の境界**である。(I)/(II) の分離は算術層の仕事(`manifest_k5` 系・FAM-U 系)であって本戦役の射程外。⟹ **層の混同禁止**(裁定 374 の fake / 非算術の二義)。

---

## 2. 測定量の限定(**測るのはこれだけ**)

### 2.1 定義

isolated な $N\subseteq K^{(5)}$($N\in\mathrm{NFI}_{PB_3}(B_3)$)に対し

$$\boxed{\ d_N:=\bigl\lvert\mathrm{Im}\,R_{N,K^{(5)}}\cap\mathfrak F_0\bigr\rvert\ \in\ \{1,5\}\ }\qquad(\text{素数窓ゆえ 2 値 = \textbf{1 ビット}}),$$
$$d_{\rm gen}(5)=\gcd_N d_N\quad(\text{系 DIV-GEN(2)}),\qquad\textbf{降下は高々 }\Omega(5)=1\ \textbf{回}.$$

**併せて必ず別欄で報告する量**(fail-closed のため・§4 の P-K5-5/6 が効く):

| 欄 | 量 | なぜ別欄か |
|---|---|---|
| `image_size` | $\lvert\mathrm{Im}\,R_{N,K^{(5)}}\rvert$ | DIV-LAW が正しければ $\in\{8,40\}$。**他の値は前件のどれかの反証** |
| `chi_image` | $\widetilde\chi(\mathrm{Im})\subseteq(\mathbb Z/20)^\times$ | (CHI) の実測。**$\ne$ 全像なら補題 CHI か (AR) が偽**(パリティ罠 $H^{\rm bad}$ の検出器) |
| `iota_in_image` | $\iota=[9,1]\in\mathrm{Im}$ か | 補題 PIN-A の**枠組み非依存**な健全性検査(P-DIV-3) |
| `d_N` | $\lvert\mathrm{Im}\cap\mathfrak F_0\rvert$ | ★ **本命** |
| `k_profile` | $\{k(\xi):\xi\in\mathrm{Im}\}$ の $u,\varepsilon$ 依存性 | 像が $\{k\equiv0\ (5/d)\}$ の形か(P-DIV-2) |

> ⚠ **`image_size` から `d_N` を推論しない・`d_N` から `image_size` を推論しない。** 両方を独立に測って**突合する**のが本設計の fail-closed の核である(DIV-LAW を検査対象に残す)。

### 2.2 触れない量(**測定設計からの明示的排除**)

本測定は次を**一切入力にも出力にもしない**: $u_{5,\widetilde\alpha}$ の値・$[u]_{2n}$ の類・$\hat c_\mu$・分岐値・平方類・PSL 窓の `gt_count`/`n_m`/`class_coefficient`/`settled_*`/`isolated`/`phi_image`/`normalizer_order`・rigidity 欄・`epsbits_*` の持上げ位数/P-bit・dessin の passport / perm_triple。**必要になった時点で停止して司令塔へ上申する**(§5.5 の停止規則 S-4)。

### 2.3 ★★ 命題 K5-BIT(**測定の収縮 — 本稿の第 1 の設計成果**)

> ### 命題 K5-BIT
> $N\subseteq K^{(5)}$ を isolated とし、$f_1:=(r^2,r^{-2},1)\in G_5$、$\phi_1:=[0,f_1]\in\mathfrak F_0$($\Theta_5(\phi_1)=(1,1,0)$、$\mathfrak F_0=\langle\phi_1\rangle$)と置く。このとき
> $$\boxed{\ d_N=5\iff\phi_1\in\mathrm{Im}\,R_{N,K^{(5)}}\ },\qquad\text{すなわち}\qquad d_N=1\iff\phi_1\notin\mathrm{Im}\,R_{N,K^{(5)}}.$$
> 具体的には、$d_N=5$ $\iff$ **次の系を満たす $(\widetilde m,\widetilde f)$ が存在する**:
> $$\widetilde m\in\mathcal X_N,\ \ \widetilde m\equiv0\ (\mathrm{mod}\ 10);\qquad \widetilde f\in[P_N,P_N]\ \ (P_N:=F_2/N_{F_2}),\ \ \widetilde f\bmod K^{(5)}_{F_2}=f_1;$$
> $$\textbf{(3.10)}\ \ \widetilde f\,\theta(\widetilde f)\in N_{F_2};\qquad\textbf{(3.11)}\ \ \tau^2(y^{\widetilde m}\widetilde f)\,\tau(y^{\widetilde m}\widetilde f)\,y^{\widetilde m}\widetilde f\in N_{F_2};\qquad\textbf{(SURJ)}\ \ \langle\bar x^{\,2\widetilde m+1},\ \widetilde f^{-1}\bar y^{\,2\widetilde m+1}\widetilde f\rangle=P_N.$$
> とくに $\widetilde m=0$ の項では系は**捻れのない 2 本のノルム方程式**に退化する:
> $$\widetilde f\,\theta(\widetilde f)=1,\qquad\tau^2(\widetilde f)\,\tau(\widetilde f)\,\widetilde f=1,\qquad\langle\bar x,\widetilde f^{-1}\bar y\widetilde f\rangle=P_N.$$

**証明.** $N$ が isolated ゆえ (HOM)(2401 Remark 3.16)で $R_{N,K^{(5)}}$ は群準同型、$\mathrm{Im}$ は $T$ の部分群。ゆえに $\mathrm{Im}\cap\mathfrak F_0$ は $\mathfrak F_0\cong C_5$ の部分群であり、$5$ 素数ゆえ $\{e\}$ か $\mathfrak F_0$。後者 $\iff$ 生成元 $\phi_1\in\mathrm{Im}$。$\phi_1$ が $\mathfrak F_0$ の生成元であることは §1.3(および §1.4 検査 F)。具体形は (3.60) $R_{N,K^{(5)}}([\widetilde m,\widetilde f])=(\widetilde m\bmod10,\ \widetilde fK^{(5)}_{F_2})$ と、$[\widetilde m,\widetilde f]\in\mathrm{GT}(N)$ の定義(簡約 hexagon (3.10)(3.11) + charming + 全射性;定義ノート §2)を並べただけ。$\widetilde m=0$ で $y^{\widetilde m}=1$、$2\widetilde m+1=1$。∎

> ### ★ この命題の性格(**なぜ効くのか**)
> - **枠組み非依存**: 使ったのは (HOM)($N$ の isolated 性)と「$\mathfrak F_0$ が素数位数の巡回群」だけ。**補題 CHI も (AR) も (LS-CC) も使っていない**。⟹ **$d_N$ の測定そのものは framework-free**(格の申告 §7.1)。
> - **枠組みが要るのはその先だけ**: 「$\mathrm{Im}=H_{d_N}$」「genuine 判定が $k$ の合同式 1 本」(系 DIV-GEN(3))は (AR) 相対である。⟹ **測定と解釈を分離せよ**(§5.4)。
> - ★ **走査規模**: 全列挙は $\lvert\mathcal X_N\rvert\times\lvert[P_N,P_N]\rvert$ 候補を要するが、命題 K5-BIT の走査は
> $$\#\{\widetilde m\in\mathcal X_N:\widetilde m\equiv0\ (10)\}\ \times\ \lvert K^{(5)}_{F_2}/N_{F_2}\cap[P_N,P_N]\,\rvert$$
> だけである。§3.5 の最小候補($\lvert K^{(5)}{:}N\rvert=125$、$N_{\rm ord}=50$)では **$5\times125=625$ 候補** — 全列挙の $625{,}000$ に対し **1/1000**。
> - **新規性の申告**: 「$\mathfrak F_0(K^{(n)})$ が $m=0$ 繊維である」は $\widetilde\chi$ の定義から即座だが、**「genuine 1 ビットの測定が 1 元の持上げ判定に収縮する」という設計命題は工房内に見つからなかった**(§7.3 の grep 語)。**Sol 監査未。**

### 2.4 換算表の $n=5$ 行(DIV-LAW §6.2 の instance)

| 入力 | 型 | $d_{\rm gen}(5)$ への効き | fake の居場所 |
|---|---|---|---|
| **L3′** $\mathrm{ord}([u_5]_{10})=5$(**実測済** cert `u5_fire_20260801.json`)+ **(RCYC)**(framework-conditional・$B_{\rm FC}$ = UNKNOWN) | 整除 | $d_{\rm arith}(5)=5\Rightarrow d_{\rm gen}(5)=5$ | ★ **fake は無い**(状態 (I)) |
| **U1** ある isolated $N$ で $d_N=1$ の実測 | 有限計算 | $d_{\rm gen}(5)=1$ **確定** | **$k\not\equiv0\ (5)$ の 32 元すべてが fake**(explicit witness) |
| **X1** 上の 2 行の衝突 | — | — | ★ **(RCYC) の前件・(AR)・DIV-LAW・$u_5$ 測定・本測定のいずれかが偽**(§4.4) |
| **U2** $\lvert\mathrm{Im}\rvert\notin\{8,40\}$ | 有限計算 | — | DIV-LAW / (AR) / (HOM) / 実装のいずれかが偽 |

> ⚠ **有限深度の PASS から $d_{\rm gen}(5)=5$ を導かない**(工房の掟 2・DIV-LAW §6.4-1)。**U1/U2 は上界しか与えない。下界は算術層(L3′)からしか来ない。**

---

## 3. 細分 $N$ の族 — **どこに検出力があるか**

### 3.1 族の定義

$\mathcal N_5:=\{N\in\mathrm{NFI}_{PB_3}(B_3):N\subseteq K^{(5)}\}$。任意の $N\in\mathcal N_5$ は自明に屋根 $K^{(5)}\cap N$ であるから、分類の実体は

$$\textbf{(SPL)}\quad B_0:=K^{(5)}/N\ \text{が}\ PB_3/N\ \text{の中に}\ B_3\text{-安定な正規補群をもつか}$$

の 1 点(命題 ENT-CRIT・`roof2_cv9_freeze_v1.md` §2)。以下、族を **A(Dih)・B(分裂)・C(entangled)** に分ける。

### 3.2 命題 K5-DIH0(**族 A = Dih 族は全滅**)

> ### 命題 K5-DIH0
> **(1)** $K^{(5)}$ を含む dihedral 窓は $K^{(5)},K^{(10)}(=K^{(5)})$ **のみ**(Prop 3.5: $K^{(5)}\subseteq K^{(nn)}\iff nn\mid\mathrm{lcm}(5,2)=10$、$nn\ge3$)。⟹ **$K^{(5)}$ より粗い dihedral 窓は存在しない。**
> **(2)** $K^{(q)}\subseteq K^{(5)}$ となる $q\ge3$ は $5\mid\mathrm{lcm}(q,2)$ すなわち $5\mid q$。そのすべてで
> $$d_{K^{(q)}}=5\qquad(R_{K^{(q)},K^{(5)}}\ \text{は全射}).$$
> 根拠: $q$ 奇 ⟹ **補題 THM44-odd**(工房補完・`ihnec_v1_addendum_e_fivebypass.md` §E-F.3.2);$4\mid q$ ⟹ **正典 2405 Thm 4.4 の証明掲載分岐**;$q\equiv2\ (4)$ ⟹ Prop 3.4($\mathrm{GT}(K^{(q/2)})=\mathrm{GT}(K^{(q)})$、$q/2$ 奇)で奇分岐に帰着。
> ⟹ **Dih 族の検出力はゼロ。**

**系(重要な非対称)**: $n=9$ では定理 K3 が $K^{(3)}$ 経由で $\mathrm{GT}_{\rm gen}(K^{(9)})$ を守り、破れは $\Lambda=\ker(\to\mathrm{GT}(K^{(3)}))$ に局在した(系 GEN9-$\Lambda$)。**$n=5$ にはその保護が無い**((1) より $K^{(5)}$ の下に dihedral 窓が無い)。⟹ **$K^{(5)}$ では $T$ 全体が狩場**であり、同時に**既知定理からの下界も無い**(下界は算術層 L3′ のみ)。

### 3.3 命題 K5-SPL0(**族 B = 分裂屋根も全滅** — (AR) 相対)

> ### 命題 K5-SPL0
> $N=K^{(5)}\cap N'$ が**分裂屋根**($PB_3/N\cong G_5\times PB_3/N'$、$N'$ isolated)であるとき、**(AR) の下で**
> $$\mathrm{Im}\,R_{N,K^{(5)}}=T,\qquad d_N=5.$$
> すなわち **分裂屋根の検出力は $\mathfrak F_0$ 方向も $\widetilde\chi$ 方向もゼロ**である。

**証明.** 系 DIV-SPLIT(`div_law_v1.md` §4.5)の $n=5$ 特化。定理 SPLIT-NULL より像は $\widetilde\chi$-fiber の合併、(ARG)+(COR54) より $\mathrm{GT}_{\rm arith}\subseteq\mathrm{Im}$、補題 CHI より $\widetilde\chi(\mathrm{Im})=(\mathbb Z/20)^\times$、ゆえに系 DIV-CHI-NULL で $\mathrm{Im}=T$。**(MCOV) は自動**(前件として要らない)。∎

> ### ★ 設計上の帰結 2 つ
> 1. **(MCOV) 破れ走査($\chi$ 方向の安価な標的・【IHNEC-GAP-4】)は $K^{(5)}$ については空である。** 走らせても何も出ない ⟹ **起票しない**(DIV-LAW §7.3 R-2 の $n=5$ 適用)。
> 2. **どの分裂屋根も「較正」以上にはならない。** ただし較正としての価値はある: **命題 K5-SPL0 は (AR) 相対**なので、分裂屋根で $d_N=1$ が出れば **(AR) か SPLIT-NULL が倒れる**(§4 P-K5-9)。**(AR) はこの工房で唯一の算術的入力**であり、それに触れる有限テストは貴重である。

**$G_5$ の商の同定(分裂判定に必要)**: 補題 D0$^n$ より $G_5^{\rm ab}\cong C_2^2$、$[G_5,G_5]=A:=\langle r\rangle^3\cong(\mathbb Z/5)^3$。$A$ は $Q\cong C_2^2$ の**相異なる 3 つの非自明指標の和** $\chi_1\oplus\chi_2\oplus\chi_3$(座標 $j$ を反転する元の集合が $\chi_j$ を決める)。⟹ **$G_5$ の単純商は $C_2$ のみ。**
$$\boxed{\ \text{屋根 }K^{(5)}\cap N'\ \text{が分裂}\ \Longleftarrow\ PB_3/N'\ \text{が}\ C_2\ \text{商をもたない}\ (\text{すなわち}\ \lvert(PB_3/N')^{\rm ab}\rvert\ \text{が奇})\ }$$
例: $N'=N_0$(Heisenberg 27・$H_3^{\rm ab}=C_3^2$)⟹ **分裂**、$\lvert PB_3/(K^{(5)}\cap N_0)\rvert=500\cdot27=13500$、$N_{\rm ord}=\mathrm{lcm}(10,3)=30$、$\lvert\mathcal X\rvert=16$、$\lvert[Q,Q]\rvert=375$、raw 候補 $6000$。**⟹ 較正専用。**

### 3.4 ★★ 命題 K5-ENT-INSUF(**「entangled ⟹ 検出力」は偽** — 本稿の第 2 の設計成果)

> ### 命題 K5-ENT-INSUF
> $n$ 奇 $\ge3$、$p$ を **$n$ を割る**素数とし $N:=K^{(np)}$ と置く。このとき
> **(a)** $N\subseteq K^{(n)}$ かつ $B_0=K^{(n)}/N=\ker(G_{np}\twoheadrightarrow G_n)\cong nA_{np}\cong(\mathbb Z/p)^3$;
> **(b)** $B_0$ は $PB_3/N=G_{np}$ の中に**補群をもたない**(正規かどうか以前に、部分群としてすら) ⟹ **命題 ENT-CRIT (b) が破れる = 本質的 entangled**;
> **(c)** それにもかかわらず **$d_N=n$**(命題 K5-DIH0(2) / 補題 THM44-odd)= **検出力ゼロ**。
> $$\Longrightarrow\ \boxed{\ \textbf{ENT-CRIT の非分裂性は必要条件であって十分条件ではない。}\ }$$

**証明.**
**(a)** $n\mid np$ ゆえ Remark 3.3 で $K^{(np)}\le K^{(n)}$。$\eta_{np,n}:D_{np}\to D_n$($r\mapsto r,s\mapsto s$)の核は $\langle r^n\rangle$(位数 $p$)であり、$np$ 奇ゆえ補題 D0$^n$ で $[G_{np},G_{np}]=A_{np}:=\langle r\rangle^3\cong(\mathbb Z/np)^3\subseteq G_{np}$。したがって
$$K^{(n)}/K^{(np)}=\ker\bigl(G_{np}\twoheadrightarrow G_n\bigr)=G_{np}\cap\langle r^n\rangle^3=n\!\cdot\!A_{np}\cong(\mathbb Z/p)^3 .$$
**(b)** 補群 $C\le G_{np}$($C\cap B_0=1$、$CB_0=G_{np}$)があったとする。$B_0=nA_{np}\subseteq A_{np}$ ゆえ Dedekind の modular law で
$$A_{np}=A_{np}\cap CB_0=(A_{np}\cap C)\,B_0,\qquad(A_{np}\cap C)\cap B_0=1,$$
すなわち $D:=A_{np}\cap C$ は $B_0$ の $A_{np}$ 内の補群。ところが $p^e\,\|\,np$ と置くと $p\mid n$ より $e\ge2$ であり、$B_0$ の $p$-部分は $p^{e-1}(\mathbb Z/p^e)^3\subseteq p\,(\mathbb Z/p^e)^3=\Phi\bigl((\mathbb Z/p^e)^3\bigr)$、すなわち
$$\boxed{\ B_0\subseteq\Phi(A_{np})\ }$$
($n$ の $p$ 以外の素因子部分では $B_0$ の成分は $0$)。**Frattini 部分群に含まれる非自明な部分群は補群をもたない**($DB_0=A_{np}$ と $B_0\subseteq\Phi$ から $D=A_{np}$、すると $D\cap B_0=B_0\ne1$ で矛盾)。
**(b′) 第 2 の独立な証明(不変因子)**: 補群があれば $A_{np}\cong B_0\times(A_{np}/B_0)\cong(\mathbb Z/p)^3\times(\mathbb Z/n)^3$。$p$-成分の初等因子を比べると左辺は $(p^e,p^e,p^e)$、右辺は $(p,p,p,p^{e-1},p^{e-1},p^{e-1})$ で、$e\ge2$ ゆえ**同型でない**。∎
**(c)** 命題 K5-DIH0(2)(= 補題 THM44-odd / 正典 $4\mid q$ 分岐)。∎

> **機械側**(`k5gen_design_check.py` 検査 F・F*・F′ — **ALL PASS**): $(n,p)=(3,3),(5,5),(9,3),(7,7),(15,3),(15,5),(25,5)$ の 7 対で (b)(b′) 双方を確認。**対照 F′**: $p\nmid n$ の $(5,3),(7,3),(3,5)$ では CRT で $A_{np}\cong A_p\times A_n$ が**分裂する** ⟹ 命題の前件 $p\mid n$ が本質的であることの確認。とくに **$K^{(15)}$ は $K^{(5)}$ 上で $A$ 水準では分裂する屋根**である(それでも検出力はゼロ — 命題 K5-DIH0)。

> ### ★★ **この反例は既存証明書で測定済である**($n=3$、$p=3$、$N=K^{(9)}$)
> `certificates/K9.v1.json` の `reduction` 欄 = `{to:"K3", surjective:true}`(像 12/12)。かつ $K^{(3)}/K^{(9)}=3A_9\cong(\mathbb Z/3)^3$ は $A_9\cong(\mathbb Z/9)^3$ の中に補群を持たない。
> $$\Longrightarrow\ \textbf{「本質的 entangled かつ全射」という対は、工房の証明書の中に既に在った。}$$
> **これは予言ではなく retrodiction である**(§4 の P-K5-8 を「既測」欄に置いた理由)。**新しい実測を 1 件も要しない反例**であり、そのぶん強い。

> ### ★ 波及(**司令塔へ**)
> - `roof2_cv9_freeze_v1.md` §7.3–7.4 の **標的 ENT-1**(「$G_3$ の非分裂 $\chi_i$-拡大を探す」)は、**このままでは「もう 1 個の $K^{(27)}$」を作りうる**。ENT-1 の記述自体は ENT-CRIT を必要条件としてしか使っていない(誤りではない)が、**発注前に §3.6 の篩を通すべき**である。
> - 同じことが**対話帳 T-25**(3)の読者にも当てはまる — T-25 は補題 NO-CENTRAL までしか言っておらず十分性を主張していないが、**「残る道は $\chi_i$ 作用の $C_3$」という文が十分条件のように読まれる恐れ**がある。§3.6 を Sol への監査点として出す(§7.5)。

### 3.5 命題 K5-MOD(**$n=5$ で $B_3$-安定な核の分類** — 最小候補は $K^{(25)}$ に食われている)

> ### 命題 K5-MOD
> $N\subseteq K^{(5)}$、$B_0:=K^{(5)}/N$ が**初等アーベル 5 群**であるとする。$B_0$ は $\mathbb F_5[G_5]$-加群であり、$A=[G_5,G_5]$ は $G_5$ の正規 5-部分群だから任意の既約 $\mathbb F_5[G_5]$-加群に自明に作用する。ゆえに
> $$\textbf{既約 }\mathbb F_5[G_5]\textbf{-加群}=\textbf{既約 }\mathbb F_5[Q]\textbf{-加群}=\{\mathbf1,\ \chi_1,\ \chi_2,\ \chi_3\}\quad(\text{すべて }1\text{ 次元}).$$
> **(1)** $H^2(G_5,\mathbf1)=H^2(G_5,\mathbb F_5)=0$ — **補題 NO-CENTRAL の $n=5$ 版**。⟹ **中心 $C_5$ 拡大は全部分裂 = 検出力ゼロ。**
> **(2)** $\dim_{\mathbb F_5}H^2(G_5,\chi_i)=2$、$\dim H^1(G_5,\chi_i)=1$、$H^1(G_5,\mathbf1)=0$。⟹ **非分裂拡大は $\chi_i$ 係数でのみ存在。**
> **(3)** ★ $\theta,\tau$($=B_3/PB_3\cong S_3$ の作用)は $A$ の 3 座標を置換する((4.8): $\tau(r^{2n_1},r^{2n_2},r^{2n_3})=(r^{2n_3},r^{2n_1},r^{2n_2})$)。ゆえに $\{\chi_1,\chi_2,\chi_3\}$ は **$S_3$ の 1 軌道**であり、**単独の $\chi_i$ は $B_3$-安定でない**。
> ⟹ **最小の $B_3$-安定な非中心核は $\chi_1\oplus\chi_2\oplus\chi_3\cong A$(次元 3)**、すなわち
> $$[K^{(5)}{:}N]=125,\qquad\lvert PB_3/N\rvert=500\cdot125=\mathbf{62{,}500},\qquad[B_3{:}N]=375{,}000.$$
> **(4)** ★★ **その最小の枠は $N=K^{(25)}$ が既に実現しており、それは検出力ゼロである**(命題 K5-ENT-INSUF・$\lvert G_{25}\rvert=4\cdot25^3=62{,}500$ ✓)。

**証明.**(1)(2) $\lvert Q\rvert=4$ は $5$ と互いに素だから LHS スペクトル系列が退化して $H^\ast(G_5,M)=H^\ast(A,M)^Q$。$A\cong(\mathbb F_5)^3$ 初等アーベル・$p=5$ 奇より $H^\ast(A,\mathbb F_5)=\Lambda(x_1,x_2,x_3)\otimes\mathbb F_5[y_1,y_2,y_3]$($y_i=\beta x_i$)、
$$H^1(A,\mathbb F_5)=\langle x_1,x_2,x_3\rangle\cong\chi_1\oplus\chi_2\oplus\chi_3,\qquad H^2(A,\mathbb F_5)=\underbrace{\langle y_1,y_2,y_3\rangle}_{\chi_1\oplus\chi_2\oplus\chi_3}\oplus\underbrace{\langle x_ix_j\rangle_{i<j}}_{\chi_3\oplus\chi_2\oplus\chi_1}$$
($\chi_j\chi_k=\chi_i$;$Q\cong C_2^2$ の指標群で相異なる 2 つの非自明指標の積は第 3 のもの)。$Q$-不変部分は $0$ ⟹ (1)。$\chi_i$ で捻れば $H^2$ 側でちょうど 2 個($y_i$ と $x_jx_k$)、$H^1$ 側でちょうど 1 個($x_i$)が自明化 ⟹ (2)。
(3) (4.8) と、座標 $j$ の指標が「$Q$ の元が座標 $j$ を反転するか」で決まること(補題 D0$^n$ の作用表)。
(4) 命題 K5-ENT-INSUF (a)。∎

**機械側**(`k5gen_design_check.py` 検査 Q1/Q2/A1/B1–B6 — **ALL PASS**): 指標の掛け算表・$H^2(A,\mathbb F_5)$ の 6 成分とその指標(`y1,y2,y3,x1x2,x1x3,x2x3`)・$Q$-不変部分が空・各 $\chi_i$ の重複度がちょうど 2・$H^1$ の重複度が 1。

### 3.6 ★ 篩(**entangled 屋根の発注前に通す 4 段**)

命題 K5-ENT-INSUF が示すとおり、非分裂性だけでは足りない。**次の 4 段をすべて通ってから実装を発注すること**(通らない標的は起票しない)。

| 段 | 検査 | 落ちる例 |
|---|---|---|
| **F-1** | $B_0$ が $G_5$ の位数と共通素因子をもつ($\lvert B_0\rvert$ が $2$ か $5$ で割れる) | 互いに素なら Schur–Zassenhaus で補群が出る(**$B_3$-安定な補群が取れるかは【K5-GAP-3】**) |
| **F-2** | $B_0$ の $G_5$-加群構造が**自明でない**($H^2(G_5,\mathbf1)=0$;命題 K5-MOD(1)) | 中心持上げ型はすべてここで落ちる |
| **F-3** | 拡大類 $[\,\cdot\,]\in H^2(G_5,B_0)^{S_3}$ が **$K^{(np)}$ 型の類と異なる** | $K^{(25)}$($n=5$)・$K^{(27)}$($n=9$)はここで落ちる ⟹ **命題 K5-ENT-INSUF の実効化** |
| **F-4** ★ | **命題 K5-BIT の系が実際に不能であること**を、$\mathbb F_5$ 上の**線型代数として**先に紙で見積もる(§4.3 の設計仮説 D-1) | 系が可解なら $d_N=5$ が確定 ⟹ **走らせる前に検出力ゼロと分かる** |

> ### ★ 設計仮説 D-1(**予想ではない・標的の型の記述**)
> $\widetilde f=\widetilde f_0\,b$($b\in B_0$、$\widetilde f_0$ は $f_1$ の任意の持上げ)と書くと、命題 K5-BIT の (3.10)(3.11) は $B_0$ 上の**アフィン方程式系**になる:
> $$\theta\text{-ノルム}:\ b\cdot{}^{\theta}b=\beta_{\theta}^{-1},\qquad\tau\text{-ノルム}:\ b\cdot{}^{\tau}b\cdot{}^{\tau^2}b=\beta_{\tau}^{-1}$$
> ($\beta_\theta,\beta_\tau\in B_0$ は $\widetilde f_0$ から決まる**障害コサイクル**、${}^\sigma b$ は $\sigma$ の作用 — $B_0$ が非可換に埋まる場合は下位項が付く)。
> ⟹ **検出力があるのは「$\beta$ が $S_3$-捻れノルム写像の像に入らない」窓**である。この障害は $H^1$ 型の量であり、命題 K5-MOD(2) の $\dim H^1(G_5,\chi_i)=1$ が**非自明な余核の存在を許す**ことと整合する。
> **格: 設計仮説(UNKNOWN)。** ノルム写像の余核を実際に計算すること、および非可換下位項の扱いは**【K5-GAP-1】**。**これを閉じることが本戦役の律速段である。**

### 3.7 候補窓の一覧(**規模と役割**・実測はしない)

| # | 窓 $N$ | 族 | $\lvert PB_3/N\rvert$ | $N_{\rm ord}$ | $\lvert\mathcal X_N\rvert$ | 全列挙 raw | K5-BIT 走査 | 予言 $d_N$ | 役割 |
|---|---|---|---|---|---|---|---|---|---|
| **W-1** | $K^{(15)}$ | A | 13,500 | 30 | 16 | 54,000 | — | **5** | ★ **証明書 2 本が既在 ⟹ 追加列挙ゼロ**(§5.2) |
| **W-2** | $K^{(25)}$ | A/C | 62,500 | 50 | 40 | 625,000 | 625 | **5** | ENT-INSUF の $n=5$ 実物 |
| **W-3** | $K^{(20)}=K^{(5)}\cap K^{(4)}$ | A | — | 20 | 16 | — | — | **5** | 正典**証明掲載分岐**($4\mid q$)の較正 |
| **W-4** | $K^{(5)}\cap N_0$(Heis 27) | **B**(分裂・確定) | 13,500 | 30 | 16 | 6,000 | **6** | **5** | 分裂屋根較正 + **(AR) テスト** |
| **W-5** | $K^{(5)}\cap N_Q$($Q_8$) | **B?(要判定)** | 4,000 | 40 | 32 | 4,000 | 要計算 | **5**(分裂なら) | ⚠ $Q_8^{\rm ab}=C_2^2$ ゆえ **$C_2$ 共通商がありうる** — 段 0 で分裂判定してから族を決める |
| **W-6** | **ENT 標的**(§3.6 F-1〜F-4 通過必須) | C | $\ge62{,}500$ | ≥10 | ≥8 | $\ge10^5$ | $\le10^3$ | **UNKNOWN** | ★ **本命・未構成** |

> ⚠ **W-6 の行が空である限り、本戦役は「較正だけ回して何も出ない」戦役である。** これを隠さない(§7.2)。

---

## 4. 予言(**IF-FIRST** — $\mathrm{Im}\,R_{N,K^{(5)}}$ を一度も測る前に凍結)

### 4.1 基準予言

| # | 予言 | 根拠 | **反証条件(対称形)** |
|---|---|---|---|
| **P-K5-1** ★ | $d_{\rm gen}(5)=5$ — **$\mathrm{GT}(K^{(5)})$ の 40 元はすべて genuine**(状態 (I) または (II)) | **FV-SOLV が賭ける側**。支持 = L3′($\mathrm{ord}([u_5]_{10})=5$ 実測 + (RCYC) framework-conditional)+ 全観測で fake witness ゼロ | **ある isolated $N$ で $d_N=1$**。⟹ 32 個の fake が明示的に出る |
| **P-K5-1′** | ⚠ **P-K5-1 は本戦役では確認できない**(有限深度で全 genuine は決まらない・【IHNEC-GAP-1】) | (COR54) の壁 | — (**「PASS したから genuine」は禁止**) |

### 4.2 各窓の予言(**測る前に凍結**)

| # | 予言 | 根拠 | 反証の意味 |
|---|---|---|---|
| **P-K5-2** ★ | **W-1**: $R_{K^{(15)},K^{(5)}}$ は**全射**、$\lvert\mathrm{Im}\rvert=40$、$d=5$、繊維は**一様に 6**($m$ 部 2 × $k$ 部 3)、$m$ 部の写像 $\mathcal X_{15}\to\mathcal X_5$ は 2 対 1 の全射 | **補題 THM44-odd**(★ 正典に証明が無い奇分岐の**工房補完**) | ★ 非全射なら **補題 THM44-odd が偽**(= 工房補完の失敗)⟹ GEN-COFINAL・FIVE-BYPASS・E1-3d・ML-ODD (i)⟹(iii) が連鎖崩壊 |
| **P-K5-3** | $K^{(10)}$ 証明書と $K^{(5)}$ 証明書は**同一対象**: 40 shadow・$N_{\rm ord}=10$・$[PB_3{:}]=500$・$\Theta$ 座標集合が一致 | Prop 3.4 | 不一致なら証明書生成の向き規約か Prop 3.4 の適用が偽 |
| **P-K5-4** | **すべての**測定窓で $\iota=[9,1]\in\mathrm{Im}$ | 補題 PIN-A/系 PIN-gen(**枠組み非依存**) | 含まない像が出れば braid 恒等式か実装が偽(**最安の健全性検査**) |
| **P-K5-5** | **すべての**測定窓で $\lvert\mathrm{Im}\rvert\in\{8,40\}$ | 系 DIV-GEN(1)+§1.4 (G7) | 他の値 ⟹ DIV-LAW / (AR) / (HOM) / 測定のいずれかが偽 |
| **P-K5-6** | **すべての**測定窓で像は $\{k\equiv0\ (\mathrm{mod}\ 5/d)\}$ の形($u,\varepsilon$ に非依存) | 定理 DIV-LAW (3) | $u$ や $\varepsilon$ に依存する像 ⟹ DIV-LAW が偽 |
| **P-K5-7** | **W-2**: $\lvert\mathrm{GT}(K^{(25)})\rvert=2\cdot25\cdot\varphi(25)=1000$、$d=5$(全射)。かつ $K^{(5)}/K^{(25)}\cong(\mathbb Z/5)^3$ は $G_{25}$ 内に補群をもたない | 系 THM43-odd + 命題 K5-ENT-INSUF | ★ **「entangled かつ全射」の $n=5$ 実物**。非全射なら THM44-odd が偽 |
| **P-K5-8** | **既測(retrodiction・新規実測不要)**: $R_{K^{(9)},K^{(3)}}$ 全射 12/12(`K9.v1.json`)かつ $K^{(3)}/K^{(9)}$ は補群なし ⟹ **ENT-CRIT の非分裂性は十分でない** | 証明書 + 命題 K5-ENT-INSUF | 証明書の読み違いのみ(**検算 §5.2 の (A4) で確認**) |
| **P-K5-9** | **W-4**(分裂が確定している屋根): $d=5$・全射。(MCOV) は前件として要らない。**W-5 は段 0 の分裂判定に条件づける**($Q_8^{\rm ab}=C_2^2$ ゆえ $C_2$ 共通商がありうる — 分裂と判定された場合にのみ同じ予言を適用し、そうでなければ **UNKNOWN のまま走らせる**) | 命題 K5-SPL0(系 DIV-SPLIT) | ★ 分裂確定の窓で $d=1$ なら **(AR) か定理 SPLIT-NULL が偽** — 工房唯一の算術的入力への有限テスト |
| **P-K5-10** | **層の一致**: 命題 K5-BIT の targeted 走査と全列挙を両方走らせた窓で、$d_N$ が**一致する** | 命題 K5-BIT | 不一致 ⟹ K5-BIT の証明か実装が偽(**tier 間 fail-closed**) |
| **P-K5-11** | **識別力 fixture**(§5.3): 抽出器に $H_1$(8 元)を与えると $d=1$・$\lvert\mathrm{Im}\rvert=8$・(CHI) OK・$\iota\in$;$H^{\rm bad}$(20 元)を与えると $d=5$・$\lvert\mathrm{Im}\rvert=20$・**(CHI) 破れフラグ**・$\iota\notin$ | §1.4 (G8)(G9) | ★ **どちらかが再現しなければ抽出器は $d=1$ を報告する能力を持たない** ⟹ 全 PASS 群の情報量ゼロ |

> ⚠ **P-K5-2〜9 は「何も出ない」ことを予言している**(較正型)。**当たっても fake 非存在の証拠にはならない。** 値打ちは**反証可能性**の側にある(DIV-LAW §7.4 の注記と同型)。

### 4.3 走査規模の凍結(**事前登録・後から増やさない**)

| 窓 | 全列挙 raw 候補 | K5-BIT 走査候補 | シャード | 根拠 |
|---|---|---|---|---|
| W-1 | 0(**証明書 2 本の突合のみ**) | — | 不要 | §5.2 |
| W-4 | 6,000 | **6** | 不要 | 全列挙 $=\lvert\mathcal X_{30}\rvert\cdot\lvert[Q,Q]\rvert=16\cdot375$。T1 $=\#\{\widetilde m\in\mathcal X_{30}:\widetilde m\equiv0\ (10)\}\times\lvert\langle Z\rangle\rvert=\lvert\{0,20\}\rvert\times3$($\widetilde m=10$ は $\gcd(21,30)=3$ で脱落) |
| W-2 | 625,000 | **625** | **$m$ 別 40 シャード**(全列挙時) | 全列挙 $=\lvert\mathcal X_{50}\rvert\cdot25^3=40\cdot15625$。T1 $=\lvert\{0,10,20,30,40\}\rvert\times\lvert5A_{25}\rvert=5\times125$ |
| W-6 | $\ge10^5$ | $\le10^3$ | 全列挙は $m$ 別 | 未確定 |

**T1 走査候補数の一般式**(命題 K5-BIT):
$$\#\bigl\{\widetilde m\in\mathcal X_N:\widetilde m\equiv0\ (\mathrm{mod}\ 10)\bigr\}\ \times\ \bigl\lvert\,(K^{(5)}_{F_2}/N_{F_2})\cap[P_N,P_N]\,\bigr\rvert .$$

**RAM(8GB 制約)**: $\lvert PB_3/N\rvert\le62{,}500$ の置換表現 + `Elements(DerivedSubgroup)` $\le15{,}625$ ⟹ 無害。**二乗 Cayley 表は禁止**(既存 cap 規約を継承)。**cap**: `per_stage_wall_seconds: 600`・`aggregate_wall_seconds: 1800`・`gap_options: -o 2g`。

### 4.4 ★★ 衝突の凍結(**$d_N=1$ が出たとき何が起きるか** — 対称形の本体)

**ある isolated $N$ で $d_N=1$ が出た**とする。そのとき同時に成り立たないものが 5 つある:

| # | 主張 | 出所 | $d_N=1$ の下での帰結 |
|---|---|---|---|
| **(1)** | $d_{\rm gen}(5)=1$、$\mathrm{GT}_{\rm gen}(K^{(5)})=H_1$、**fake 32 個**($k\not\equiv0\ (5)$) | 系 DIV-GEN(2)(3) | ★ **fake GT-shadow の初の明示的証人**(P5 哨戒の 30 か月ぶんの陰性を覆す) |
| **(2)** | **ML-ODD (iii) が偽** ⟹ $\mathcal{PR}^{\rm odd}$ 非全射 | 定理 ML-ODD | 井原予想(全射部)への必要条件鎖 IH-NEC が切れる |
| **(3)** | 系 **FAKE-LIFT** により $K^{(15)},K^{(25)},K^{(35)},\dots$ **すべて**が fake を含む | 系 FAKE-LIFT | 系 FIVE-BYPASS の前件が偽 ⟹ 迂回線も同時に死ぬ |
| **(4)** | $d_{\rm arith}(5)\mid d_{\rm gen}(5)=1$ ⟹ $d_{\rm arith}(5)=1$ | 系 DIV-LAT | **odd Conj 5.1 が窓 $n=5$ で偽** = 本峰(P1)の反証 |
| **(5)** | しかし **(RCYC)**($d_{\rm arith}=\mathrm{ord}(a_5)$)+ **実測 $\mathrm{ord}([u_5]_{10})=5$**(cert `u5_fire_20260801.json`・裁定 398)は $d_{\rm arith}(5)=5$ を要求する | 系 DIV-ARITH + FAM-U domain 復帰 | ★★ **(4) と正面衝突** |

$$\boxed{\ \Longrightarrow\ d_N=1\ \text{が出たら、}\ \{\text{(RCYC) の前件(とくに比較橋 }B_{\rm FC}),\ \text{(AR)},\ \text{DIV-LAW},\ u_5\ \text{測定},\ \text{本測定}\}\ \text{のどれかが偽。}\ }$$

> ### ★★ これが $K^{(5)}$ 直撃の本当の値打ち
> **【GAP-Rcyc】= 比較橋 $B_{\rm FC}$ は UNKNOWN であり、工房はそれに触れる有限テストを 1 本も持っていなかった。** $n=5$ は
> - **素数**(約数束が 2 点 ⟹ 1 ビット)
> - **下に dihedral 窓が無い**(定理 K3 型の保護も無い ⟹ 中間状態が無い)
> - **$\mathrm{ord}(a_5)=5$ が既に測られている**(裁定 398)
>
> の 3 条件が揃う**唯一の窓**であり、そこで $d_N=1$ が出れば **枠組み層に有限計算で穴が開く**。⟹ 本戦役は「fake 探索」であると同時に **$B_{\rm FC}$ の間接テスト**である。
> ⚠ **ただし逆は言えない**: $d_N=5$ がいくつ出ても $B_{\rm FC}$ の証拠にはならない(§4.1 P-K5-1′・矢印を跨がない)。**非対称は不変**。

---

## 5. 実装仕様(**設計のみ** — 実装は implementer へ)

### 5.0 位置づけと前提

- **R4b 様式の再利用**: 単一判定関数 `ScanRoofHexagon(qrec, charmingSet)`(`search/probe/wac_v1/ihnec_r4b_run.g` L77–L116)を**逐語再利用**(改造禁止・**CV-13 の精神** = 生成・受理・生成条件が同一関数を通る)。
- **証明書非読**: driver は `certificates/*.json` を**一切読まない**(紙との独立性)。期待値は driver 内のリテラル定数として hard assert。**例外 = 段 K5-1(W-1)のみ**(そこは証明書突合が目的そのもの・§5.2)。
- ⚠ **$\theta/\tau$ の評価水準**(定義ノート §2 の 2026-07-25 注意): 商 $F_2/N_{F_2}$ 上で $\theta,\tau$ を準同型として評価する近道は **$N_{F_2}$ の $\theta,\tau$-不変性**を要し、それは **$c\in N$** に依存する。$c\notin N$ の窓では**自由群の語レベルで $\theta/\tau$ を適用してから $\varphi$ で評価する**こと。**W-4/W-5/W-6 では $c\in N$ を段 0 で assert する**(通らなければ語レベル経路へ切替・両方の結果を報告)。

### 5.1 二層測定(**tier を混ぜない**)

| tier | 何を測るか | 前件 | いつ使うか |
|---|---|---|---|
| **T1(targeted)** | 命題 K5-BIT の系が可解か($d_N$ の 1 ビット) | $N$ isolated + (HOM) — **枠組み非依存** | 全窓・第一手 |
| **T2(full)** | $\mathrm{GT}(N)$ 全列挙 → `image_size` / `chi_image` / `k_profile` / `iota_in_image` | 同上 | **較正窓は必須**・本命窓は T1 が $d=1$ を出したときに**必ず追走** |

> **規律**: **T1 が $d_N=1$ を出したら、T2 を走らせるまで「fake を発見した」と書かない。** T1 は「$\phi_1$ が見つからなかった」という**探索の失敗**であり、非存在の証明ではない(工房の掟: 負の探索結果は非存在の証明ではない)。T2 の悉皆列挙で $\mathrm{Im}$ を確定させて初めて $d_N=1$ を主張する。⟹ **停止規則 S-3**。

### 5.2 作業段

| 段 | 内容 | 出力 | 予言 | fail-closed assert |
|---|---|---|---|---|
| **K5-0** | 宇宙の再現: `MakeGn(5)`(`search/week3-battery-common.g`)で $G_5$ を生成、$\Theta_5$ 抽出器を実装 | — | §1.3 | `Size(G5)=500`・`Size(DerivedSubgroup(G5))=125`・$\mathcal X_5$ がリテラル $\{0,1,3,4,5,6,8,9\}$ |
| **K5-1**(★アンカー A1・**追加列挙ゼロ**) | `K5.v1.json` と `K15.v1.json` の $(m,k)$ 座標を抽出し、$R:(\widetilde m,\widetilde k)\mapsto(\widetilde m\bmod10,\widetilde k\bmod5)$ の像を整数演算で計算 | 40/40 | **P-K5-2** | 像 $=40$・繊維一様 6・$\lvert\mathcal X_{15}\rvert=16$・$m$ 部 2 対 1 |
| **K5-2**(アンカー A2) | 同じ $\Theta$ 抽出器 + 同じ $d$ 抽出器を **$K^{(3)}$ の既存 4 プローブ**($K^{(9)},K^{(18)},L_{01},M_{01}$ の `reduction:{to:"K3"}`)に適用 | $d=3$ ×4 | 既測(FV-05) | **4 本すべてで $d=3$・像 12/12**。1 本でも外れれば中止(**外部 anchor** = 凍結証明書の独立再現) |
| **K5-3**(アンカー A3) | 同一判定関数 `ScanRoofHexagon` を **$K^{(5)}$ 単体**に適用 | **40** | §1.3 | $=40$ でなければ**中止**。40 元の $\Theta$ 集合が `K5.v1.json` と**集合等号** |
| **K5-4**(アンカー A4) | 同関数を **$K^{(3)}$ 単体**に適用 | **12** | 証明書 K3 | $=12$ でなければ中止(向き規約の経時変化の検出) |
| **K5-5**(★識別力) | §5.3 の 3 fixture を $d$ 抽出器に流す | 3/3 | **P-K5-11** | **$H_1$ で $d=1$ が出ないなら以後の全 PASS は情報量ゼロ ⟹ 中止** |
| **K5-6** | **T1**: 対象窓で命題 K5-BIT の targeted 走査 | $d_N\in\{1,5\}$ | 窓ごとの予言 | 候補総数が §4.3 の凍結値と一致 |
| **K5-7** | **T2**: 全列挙(較正窓は必須) | `image_size` 他 5 欄 | P-K5-5/6/4 | `image_size`$\in\{8,40\}$・`chi_image` 全像・`iota_in_image` true |
| **K5-8** | **settled 判定**: 各 shadow で $x\mapsto x^u$、$y\mapsto f^{-1}y^uf$ が $\mathrm{Aut}(PB_3/N)$ に延びるか | fail 0 | — | **「真の settled」**(核 $=N$)であって壁 judge の well-definedness ではない(`ihnec_v1.md` §6.6 注意 2)。**fail>0 なら $N$ は isolated でなく (HOM) が使えない ⟹ $d_N$ は主張しない** |
| **K5-9** | T1/T2 の突合 | 一致 | **P-K5-10** | 不一致で**中止・即報** |

### 5.3 識別力のある dummy fixture(**CV-9-5 の要求**)

| fixture | 入力 | 期待出力 | 何を保証するか |
|---|---|---|---|
| **DF-1** | $H_1$(§1.3 の 8 元、$k=0$) | $d=1$・`image_size`$=8$・`chi_image` 全像(8 値)・`iota_in_image` true | ★ **抽出器が $d=1$ を報告できること**。これが無ければ全 PASS 群は情報量ゼロ |
| **DF-2** | $H^{\rm bad}=\{\varepsilon=0\}$(20 元) | $d=5$・`image_size`$=20$・**`chi_image` が 4 値 = (CHI) 破れフラグ**・`iota_in_image` **false** | ★ **パリティ罠**(裁定 209 型)の検出器。$\lvert\mathrm{Im}\rvert\notin\{8,40\}$ を正しく異常として立てるか |
| **DF-3** | $\mathcal X_5$ に $m=2$($\notin\mathcal X_5$、$\gcd(5,10)=5$)を混ぜた charming set | `charming_pass` が**増えない** | 生成器側の向き規約(CV-13) |

**competitor universe**(CV-9-5): 主張「$d_N=5$」は $\mathfrak F_0\cong C_5$ の 2 個の部分群のうち 1 個を当てる主張(偶然一致率 1/2)⟹ **1 ビットの主張は偶然一致しやすい**。ゆえに**単独の $d_N$ を成果としない** — `image_size`/`chi_image`/`k_profile`/`iota` の 4 欄と**同時に**一致して初めて 1 本のプローブとして数える(§7.1 の格)。

### 5.4 証明書スキーマ(`gtsh-cert/v1` 互換 + 本件の追加欄)

```
target.id            = "K5gen.<window>"            target.family = "genuine-probe"
target.base          = { id: "K5", n: 5, N_ord: 10, index_PB3: 500, |GT|: 40 }
target.construction  = { window: "<K15 | K25 | K5capN0 | ENT-...>", c_in_N: true|false,
                         theta_tau_eval: "quotient" | "wordlevel" }
tier                 = "T1" | "T2"
counts               = { raw_candidates, hexagon_pass, charming_pass, surjective_pass, settled_fail }
anchors              = { k5_alone: 40, k3_alone: 12, k3_probes_d: [3,3,3,3],
                         k15_to_k5_image: 40, discriminating_fixtures: {DF1:ok, DF2:ok, DF3:ok} }
measurement          = { d_N,                       # <- 1 bit, framework-free
                         image_size,                # <- separate field, NOT derived from d_N
                         chi_image,                 # <- list of residues mod 20
                         chi_image_full: true|false,
                         iota_in_image: true|false,
                         k_profile,                 # <- {k : xi in Im}, and (u,eps)-dependence flag
                         phi1_lift_found: true|false }   # <- the K5-BIT witness (T1)
witness              = { m_tilde, f_tilde_word }    # <- present iff phi1_lift_found
scope                = { isolated_N: "<canon|paper|machine-only>", lane: "GAP single lane",
                         framework_free_part: "d_N (prop K5-BIT)",
                         framework_relative_part: "Im = H_d (DIV-LAW, rel. (AR))" }
provenance           = { script_sha256, gap_version, plan_frozen_sha,
                         predictions_frozen: "docs/notes/k5_genuine_campaign_v1.md",
                         predictions_sha256 }
seal_declaration     = { touches_c_hat_mu: false, touches_psl_sealed_fields: false,
                         touches_epsbits: false, touches_u_values: false }   # <- 必須欄・§6
```

> **⚠ `d_N` と `image_size` を同一の計算から導かないこと**(§2.1)。schema がこの 2 欄を分けているのは、**DIV-LAW を検査対象に残す**ためである。

### 5.5 停止規則

| # | 条件 | 動作 |
|---|---|---|
| **S-1** | アンカー K5-1〜K5-4 のいずれかが外れる | **即停止**・次窓へ進まない・後段の既知値で補正しない・`stop_reason`/`stage`/`observed`/`expected` を残す |
| **S-2** | 識別力 fixture DF-1 が $d=1$ を返さない | **即停止**(以後の PASS に情報量が無い) |
| **S-3** | T1 が $d_N=1$ を出す | **T2 を必ず追走**。T2 完了まで「fake 発見」と書かない。**司令塔へ即報**(§4.4 の衝突が発火するため) |
| **S-4** ★ | 測定の途中で §2.2 の禁止量($\hat c_\mu$・PSL 封印欄・ε bits・$u$ 値・dessin データ)に**触れざるを得なくなった** | **即停止・司令塔へ上申**(スコープ照合は司令塔の専権)。**自己判断で続行しない** |
| **S-5** | cap 超過 | `stage_result = UNKNOWN; halt`。**事後免除なし** |
| **S-6** | settled 判定(K5-8)で fail > 0 | $N$ は isolated でない ⟹ (HOM) が使えない ⟹ **$d_N$ を主張せず UNKNOWN**($\mathrm{Im}$ は部分群とは限らない) |

---

## 6. ★ 干渉チェックリスト(**列挙のみ・スコープ照合は司令塔**)

### 6.1 名前衝突(**grep 事故の元** — 最優先)

| # | 衝突 | 正しい扱い |
|---|---|---|
| **N-1** ★ | **$\varepsilon$**。本稿の $\varepsilon=m\bmod2$($\Theta_n$ の第 3 成分)は、封印語彙の **「ε bits」**(`search/certs/epsbits_*.json`・壁キャンペーンの持上げ位数 / P-bit・`docs/notes/epsilon_mechanism_v2.md`)と**全くの別物**である | 証明書の欄名を `theta_eps` とし、`epsbits` の語を使わない。**`epsbits` を grep したときに本戦役の cert が引っかからないこと**を実装の受入条件にする |
| **N-2** ★ | **$N_5$ / K5**。`certificates/N5.v1.json` は **$c$ の位数 5 の control 窓**($N_{\rm ord}=5$・$[PB_3{:}]=5$・4 shadow)であって $K^{(5)}$ **ではない**。FAKE-VOID 母集団台帳 **FV-11** の「$N_5$」も同じ control 窓 | cert id を `K5gen.*` に統一。`N5` を base に取らない |
| **N-3** | **$K^{(10)}=K^{(5)}$**(Prop 3.4)。`K10.v1.json` と `K5.v1.json` は同一対象 | **独立 2 例として二重計上しない**(P-K5-3 で明示的に検査) |
| **N-4** | **「Thm 4.4」**。2401 Thm 4.4($\mathcal{PR}$ の関手性)と 2405 Thm 4.4(reduction 全射性)は別物 | 本稿の (THM44) は**すべて 2405**。論文 ID とセットで書く(`ihnec_v1_addendum_e_fivebypass.md` §E-F.2.1 の警告を継承) |
| **N-5** | **$M_5$ / $M_2$ / $M_{01}$**。`M01.v1.json`($N_{\rm ord}=30$)・roof2 の $M_2=K^{(9)}\cap L$・FV-14b の $M_5$ は全て別対象 | 本戦役は $M$ を対象名に使わない |

### 6.2 封印との交差(**データ水準**)

| # | 交差点 | 状態 | 本設計の扱い |
|---|---|---|---|
| **X-1** ★★ | **$K^{(5)}$ 算術飽和 manifest の封印予言 (P1)**: 「$\mathrm{ord}([u_i^{-1}]_{10})\in\{1,5\}$($i=$ sq, ns)」は、系 DIV-ARITH の下で **$d_{\rm arith}(5)\in\{1,5\}$ と同一の 1 ビット**である。本戦役が測る $d_{\rm gen}(5)$ はその**上の層**であり、$d_{\rm gen}=1$ は $d_{\rm arith}=1$ を**強制する** | ⟹ **本測定の陰性結果は封印予言 (P1) の値を(片側に)決めてしまう** | **測定設計上は非接触**($u$ を読まない)。しかし**推論水準では干渉する** ⟹ **司令塔のスコープ照合が要る**。本稿は $u$ 側の値を一切参照していない。→ **裁定 412(Sol F99-4.2)**: 干渉実在と裁定 — **Phase 2 で $d=1$ が確定した時点は inference-contact event として即停止・報告**(「$u$ が誤り」「BFC が誤り」と一足飛びに特定せず衝突選言の全段を保持)。(P1)(P2) の実効状態は provenance/results_k5.md Entry 1 が正本(外部解決の記帳・戦役 status = BRIDGE-UNKNOWN 不変) |
| **X-2** ★ | 同 manifest の **(P2)**「$[u_{ns}^{-1}]_{10}=[u_{sq}^{-1}]_{10}$」 | FAM-U の n=5 発火(裁定 398)で $u_{5,1}=-4$・$u_{5,2}=+4$・$[4]_{10}=[-4]_{10}$ が測られている ⟹ **(P1)(P2) は事実上答が出ている可能性がある** | ★ **本稿は判断しない。** 「manifest_k5 の封印が実効的にどの状態か」は**司令塔の記帳事項**として上申する(§7.5-3) |
| **X-3** ★ | **`seal_PSL_v1` の状態が台帳内で食い違っている**: LEDGER `2026-07-26` 項は「**封印 PSL_v1 開封: 7/7 完全一致**」、LEDGER `裁定 398` 項は「金庫の seal_PSL_v1(7/26・予言 7 本)は別下位戦役の封印 — **本対決では開封不要につき封印維持**」 | **決着(裁定 410)**: 同一封印・**開封済(7/26)が正**(金庫封印体=リポジトリ開封体=台帳ハッシュの三者一致・byte-identical)。裁定 398 の「封印維持」は状態誤認(実質判断は無傷) | 本設計は**どちらであっても PSL 窓に触れない**(下記 X-4)。X-4 の懸念はデータ水準では解消(7 窓の値は 7/26 から公開・cross-checked)— PSL 屋根除外は凍結設計として維持 |
| **X-4** | **PSL 窓を屋根の相手にすると封印欄に触れる**: $K^{(5)}\cap N_{\rm PSL}$ を組むと `gt_count`・`settled_*`・`isolated`・`phi_image`・`normalizer_order` が計算過程に現れる(= `seal_PSL_v1` のメタデータ水準) | 交差する | ★ **Phase 1 の候補窓から PSL 屋根を除外**(§3.7 に載せていない)。必要になれば S-4 で停止・上申 |
| **X-5** | **rigidity(case A/B の 4 欄分離・`docs/week3-manifest_v2_psl.md` P121)** | 交差しない | 本設計は Hurwitz / rigidity / dessin を一切使わない |
| **X-6** | **$\hat c_\mu$ / N∞ 曲線模型 / 分岐値 / 平方類**(`week4-NInfty_stage2_spec_v1.md` の I-b∞) | データ水準では交差しない | 本設計は有限群計算のみ ⟹ ✓ |
| **X-7** ★ | ただし **推論水準では交差する**: §4.4 の衝突が発火すると、解決先の候補に**比較橋 $B_{\rm FC}$**(= N∞ / curve-model 線が支えようとしている当のもの)が入る | 交差する(推論) | **本稿は「どれが偽か」を主張しない**(X1 行は選言のまま凍結)。裁定は司令塔 |
| **X-8** | **`certificates/k5blocks/` `k5e/` `k5fixture/` `k5pipeline/` の名前空間**はすべて**算術飽和戦役**のもの | 交差しうる(書き込み事故) | ★ **本戦役の cert は `certificates/k5gen/` に置く**(既存 4 ディレクトリに 1 バイトも書かない) |
| **X-9** | **FAKE-VOID 母集団台帳 FV-28**($K^{(5)}$ 系 = 「blind campaign・立入禁止・観測欄は封印」) | ★ **本戦役はこの欄を初めて埋める行為である** | 台帳 `fake_void_v1.md` §4 の FV-28 行の更新(封印解除の反映)は**司令塔の担当**。本稿は起票のみ |

### 6.3 在庫の棚卸し(**既に何が測られているか** — 委嘱 §1 への回答)

| 対象 | 既存資産 | 判定 |
|---|---|---|
| `certificates/K5.v1.json` | 40 shadow・合成表 1600・逆元表。**`reduction` 欄は空(長さ 0)**・`ls_witness` も空 | ★ **$K^{(5)}$ への reduction は 1 本も測られていない** |
| `certificates/K10.v1.json` | 同上(同一対象・`reduction` 空) | 同上 |
| `certificates/K15.v1.json` | 240 shadow・`reduction` 空 | **W-1 の相手側は在庫にある**(§5.2 K5-1 は追加列挙ゼロ) |
| FAKE-VOID 母集団台帳 | **FV-28 = $K^{(5)}$ 系・観測欄封印**。独立プローブ 7 本 / 底窓 5 個($N_Q,N_2,N_3,N_5,K^{(12)}$)+ spot-check 10 本($K^{(3)},K^{(4)},N_A$)の**どこにも $K^{(5)}$ は入っていない** | ★ **$K^{(5)}$ の fake プローブは 0 本** |
| `certificates/k5blocks/ k5e/ k5fixture/ k5pipeline/` | すべて**算術飽和戦役**($u$・dessin・Kummer・negcal)。`k5e` は $8\mid n$ の SCHEMA-OUT 裏取り、`k5fixture` は dessin の passport/perm_triple | ★ **genuine 層のデータは 1 件も無い** |
| 地図 P5 行「全観測で fake witness ゼロ(**K³/K⁵ 細分**…)」 | `fake_void_v1.md` §8 が「格の混在」として修文提案済。実体は 17 プローブ・底窓 8 個で、**$K^{(5)}$ を含まない** | ★ **地図の「K⁵ 細分」という記述は在庫に対応物が無い** ⟹ 司令塔へ上申(§7.5-4) |

$$\boxed{\ \textbf{結論: }K^{(5)}\ \textbf{の genuine 層はプローブ 0 本の完全な空白である。本戦役は 1 本目を打つ。}\ }$$

---

## 7. 格の申告・GAP・新規性・申し送り

### 7.1 格付け

| 主張 | 格 |
|---|---|
| §1.3–1.5 の宇宙(40 元・$\Theta_5$・$\mathfrak F_0$・$H_1$/$T$ の 2 択) | **証明書との突合で確認**(合成表 1600 対・悉皆部分群列挙)。**単系統 python × GAP 由来 cert** ⟹ **cross-checked ではない**(CV-9 判読未) |
| **命題 K5-BIT**($d_N$ の 1 元収縮) | ★ **paper-proof candidate**(初等・**枠組み非依存**・Sol 未監査) |
| **命題 K5-DIH0**(Dih 族の無力) | **paper-proof candidate**。(2) は **補題 THM44-odd(工房補完)** と正典の証明掲載分岐に相対 |
| **命題 K5-SPL0**(分裂屋根の無力) | **paper-proof candidate / (AR) 相対**(系 DIV-SPLIT の特化) |
| **命題 K5-ENT-INSUF**(entangled ⟹ 検出力 は偽) | ★★ **paper-proof candidate**。**$n=3$ の実例は既存証明書で確認済**(`K9.v1.json` reduction) |
| **命題 K5-MOD**($B_3$-安定核の分類・$H^2$ 計算) | **paper-proof candidate**(指標計算は機械確認・Sol 未監査) |
| **設計仮説 D-1**($S_3$-捻れノルムの余核) | ★ **UNKNOWN**(【K5-GAP-1】) |
| **予言 P-K5-1〜11** | **prediction(未測定)** |
| $d_{\rm gen}(5)$ の**値** | ★ **UNKNOWN**(【DIV-GAP-1】の $n=5$ 行) |
| Lean 検証 | ✗ **していない** |

### 7.2 ★ 正直な評価(**この戦役が買うもの・買わないもの**)

| | 内容 |
|---|---|
| **買うもの(1)** | **測定量の型の確定**: 1 ビット・1 元の持上げ判定・枠組み非依存。⟹ 実装コストが 3 桁下がり、以後どんな窓が構成されても**同じ 625 行の走査**で済む |
| **買うもの(2)** | ★ **候補族の刈り込み**: Dih 全滅(定理)・分裂屋根全滅((AR) 相対)・「entangled ⟹ 検出力」が偽(反例つき)⟹ **無駄弾を撃たない**。とくに標的 ENT-1 への篩(§3.6) |
| **買うもの(3)** | ★ **$B_{\rm FC}$ への有限テスト経路の同定**(§4.4)。$n=5$ が唯一の窓であることの根拠つき |
| ★ **買わないもの(1)** | **$d_{\rm gen}(5)=5$ の証明**。有限深度では原理的に決まらない(【IHNEC-GAP-1】・(COR54))。**PASS を genuine の証拠にしない** |
| ★★ **買わないもの(2)** | **発火できる本命窓**。W-6 は**未構成**であり、【K5-GAP-1】(ノルム余核)と【K5-GAP-2】(実現性)が閉じるまで**本戦役は較正しか回せない** |
| **買わないもの(3)** | **算術層の情報**。$d_{\rm arith}(5)$ = 状態 (I)/(II) の分離は本戦役の射程外 |

### 7.3 新規性の申告(**grep 済**)

**grep 語**: `K5-BIT`・`d_N`・`ENT-INSUF`・`ENT-CRIT`・`NO-CENTRAL`・`K^{(25)}`・`K25`・`entangled`・`屋根`・`$\mathfrak F_0$ 方向`・`genuine 判定`・`1 ビット`・`m=0 繊維`・`Schur-Zassenhaus`・`$H^2(G_n`。

| 項目 | 既出か | 差分 |
|---|---|---|
| 「$n$ 素数なら $d_{\rm gen}\in\{1,n\}$ の 1 ビット」 | ★ **既出**(`div_law_v1.md` 系 DIV-GEN(5)・§6.3・§7.3 R-4) | 本稿は $n=5$ に特化し、**40 元の実物と証明書で instantiate** した |
| **命題 K5-BIT**(1 元への収縮・$m=0$ 繊維・走査の 1/1000 化) | **発見できず** | ★ 本稿 |
| Dih 族の無力 | **半分既出**(THM44-odd は既存。$K^{(5)}$ の上に dihedral 窓が無いことは Prop 3.5 から即座) | 本稿は**族として閉じた**(命題 K5-DIH0) |
| 分裂屋根の無力 | ★ **既出**(系 DIV-SPLIT・`div_law_v1.md` §4.5) | 本稿は $n=5$ 特化 + **(MCOV) 走査を起票しない**という運用判断 |
| **命題 K5-ENT-INSUF**(非分裂性の非十分性・$K^{(np)}$ 反例) | **発見できず**(ENT-CRIT は必要条件としてのみ述べられている) | ★★ 本稿。**既存証明書に反例が在ったことの指摘**を含む |
| **命題 K5-MOD**($n=5$ の $H^2$・$S_3$ 軌道・最小核が $K^{(25)}$ に一致) | **部分的に既出**(補題 NO-CENTRAL は $n$ 一般で $\mathbb Z/3$ 係数・roof2 §7.2)。$\chi_i$ が $S_3$ の 1 軌道であることと**最小 $B_3$-安定核の同定**は発見できず | ★ 本稿($p=5$ 版 + $S_3$ 軌道 + $K^{(25)}$ との一致) |
| §4.4 の衝突表($B_{\rm FC}$ への有限テスト) | **発見できず**(換算表 X1 行は型としては既出) | ★ 本稿(**$n=5$ が唯一の窓である理由**の同定) |
| $K^{(5)}$ の genuine プローブが 0 本であること | ★ **既出**(`fake_void_v1.md` FV-28) | 本稿は**在庫を証明書側から機械的に確認**(`reduction` 欄が空) |

**「初」という語は使わない。** 「genuine 判定を 1 元の持上げに落とす」型は逆極限・障害理論では標準的でありうる。**本設定への翻訳と、既存資産による反例の同定が本稿の寄与**である。

**外部文献**: 使用なし。群論的入力は「巡回群の素数位数部分群は 2 個」「$p'$ 群による作用で $H^\ast$ が不変部分に退化」「初等アーベル $p$ 群($p$ 奇)のコホモロジー環」「Schur–Zassenhaus」— すべて標準。

### 7.4 【K5-GAP】一覧

| 札 | 内容 | 状態 |
|---|---|---|
| **【K5-GAP-1】** ★★ | **設計仮説 D-1 の余核計算**。$S_3$-捻れノルム写像 $b\mapsto(b\cdot{}^\theta b,\ b\cdot{}^\tau b\cdot{}^{\tau^2}b)$ の余核が非自明になる $B_0$ と拡大類の同定。**非可換に埋まる場合の下位項の扱いも未処理** | **UNKNOWN・本戦役の律速** |
| **【K5-GAP-2】** | $H^2(G_5,A)^{S_3}$ の類のうち、**$F_2$ の 2 生成商として実現し、かつ $\theta,\tau$ が持ち上がる**ものの同定。$[K^{(25)}]$ 以外に何個あるか | **未着手**(型は書けた) |
| **【K5-GAP-3】** | $\gcd(\lvert B_0\rvert,\lvert G_5\rvert)=1$ のとき Schur–Zassenhaus の補群を **$B_3$-安定に取れるか**(§3.6 F-1 の根拠) | **UNKNOWN**(Glauberman 型の補題が要る) |
| **【K5-GAP-4】** | $B_0$ が **2 群**の場合($\lvert Q\rvert=4$ と互いに素でないので LHS 退化が使えない)。$\mathfrak F_0\cong C_5$ の持上げを 2 群核が阻めるか | **UNKNOWN** |
| **【K5-GAP-5】** | **$d_{\rm gen}(5)$ の値**(【DIV-GAP-1】の $n=5$ 行) | **UNKNOWN** |

> ### 【文献要請 K5-L1】
> **困難**: 有限群 $G=A\rtimes Q$($A$ 初等アーベル $p$ 群・$Q$ が $p'$ 群・$A$ が $Q$ の相異なる非自明指標の和)と、$A$ の座標を巡回置換する外側の $\Gamma=S_3$ 作用が与えられたとき、$\Gamma$-同変な非分裂拡大 $1\to B_0\to\widehat G\to G\to1$ の類を**列挙し、しかもそのうちどれが「$B_0$ の $\Gamma$-捻れノルム写像が非自明な余核をもつ」かを判定する**機構が欲しい。
> **欲しい結果の型**: ① $\Gamma$-同変 Schur 乗数 / $H^2_\Gamma$ の inflation-restriction 版(**既出の【文献要請 ROOF2-L1】と同型 — 重複起票しない**)② ★ **新規部分**: 拡大類 $[\widehat G]$ と、その中での**特定元の持上げ可能性**(本件では $\phi_1$)を結ぶ障害の明示式。「与えられた $\bar g\in G$ が $\widehat G$ の中で指定された関係式(ここでは $\theta$-ノルム 1・$\tau$-ノルム 1)を満たす元に持ち上がるか」を $H^1$ / 捻れノルムの余核で書く定理。
> **既に持っているもの**: `lins`(低指数正規部分群)・`hap`/`cohomolo`(同梱)。総当たりで済むなら文献は不要 — **判断は司令塔へ**。

### 7.5 申し送り(司令塔へ)

1. ★★ **W-6(entangled 標的)が空である限り本戦役は発火できない。** 【K5-GAP-1】(ノルム余核)を閉じる委嘱を先に立てるか、それとも **Phase 1 の較正だけ回す**か、**司令塔の判断を仰ぐ**。私の推奨は「**Phase 1(§5.2 の K5-1〜K5-5)は追加列挙ほぼゼロなので即発火・W-6 は §3.6 の篩つきで別委嘱**」。
2. ★★ **`roof2_cv9_freeze_v1.md` §7.4 の標的 ENT-1 に篩(§3.6)を付けるか。** 命題 K5-ENT-INSUF により、ENT-1 は**もう 1 個の検出力ゼロ屋根**($n=9$ なら $K^{(27)}$ 型)を作りうる。**発注前の F-3/F-4 通過を必須化する**ことを提案する。
3. ★ **`manifest_k5_v1.md` の封印予言 (P1)(P2) の実効状態の記帳**(§6.2 X-1/X-2)。FAM-U の n=5 発火(裁定 398)が $u_{5,1}=-4$・$u_{5,2}=+4$ を出しているため、**別経路ではあるが (P1)(P2) と同じ量に答が出ている可能性がある**。本稿は判断しない。**記帳の整合は司令塔裁定事項。**
4. ★ **`seal_PSL_v1` の状態の食い違い**(§6.2 X-3)。LEDGER の 2 項が「開封済」と「封印維持」で矛盾して読める。**速達 `ops/express/` へ上申済。** → **決着(裁定 410・2026-08-01): 開封済(7/26)が正・398 は状態誤認(実質判断は無傷)。**
5. ★ **地図 P5 行の「K⁵ 細分」という記述**(§6.3)は在庫に対応物が無い(`K5.v1.json` の `reduction` 欄は空・FV-28 は観測欄封印)。`fake_void_v1.md` §8 の修文提案と同じ論点。**本戦役が 1 本目を打てば実体が生じる。**
6. **`fake_void_v1.md` FV-28 行の更新**(封印解除の反映)は司令塔の担当。本稿は起票のみ。
7. **cert 名前空間**: `certificates/k5gen/` を新設し、既存 `k5blocks/ k5e/ k5fixture/ k5pipeline/`(すべて算術飽和戦役)に**書き込まない**ことを実装の受入条件にする(§6.2 X-8)。

### 7.6 Sol への監査依頼(**優先順位つき・便 100 想定**)

1. ★★ **命題 K5-ENT-INSUF**(§3.4)— とくに (b) の「$p\mid n$ のとき $nA_{np}$ は $A_{np}$ 内に補群を持たない」という位数計算と、**「既存証明書 `K9.v1.json` の全射 12/12 がそのまま反例になっている」という読み**。ここが正しければ、entangled 屋根プログラム全体の設計前提が 1 段狭まる。
2. ★★ **命題 K5-BIT**(§2.3)— とくに「$\mathrm{Im}\cap\mathfrak F_0$ が $C_5$ の部分群である」に $N$ の isolated 性((HOM))**だけ**で足りる、という私の依存申告。**(AR) も補題 CHI も使っていない**という主張に穴はないか。
3. ★ **命題 K5-MOD**(§3.5)— (3) の「$\{\chi_1,\chi_2,\chi_3\}$ が $S_3$ の 1 軌道 ⟹ 単独の $\chi_i$ は $B_3$-安定でない」の段。$\tau$ が $Q$ にも作用することを勘定に入れた上で正しいか(私は (4.8) の座標巡回だけから結論している)。
4. **設計仮説 D-1**(§3.6)— 障害を $S_3$-捻れノルムの余核として書く型が妥当か。**$B_0$ が非可換に埋まる場合の下位項**をどう扱うべきか(私は【K5-GAP-1】として開いたまま)。
5. **§4.4 の衝突表** — 「$d_N=1$ ⟹ (RCYC)/(AR)/DIV-LAW/$u_5$ 測定/本測定 のいずれかが偽」という選言の**列挙に漏れがないか**。とくに $u_5$ 測定と (RCYC) の間にもう 1 段(FAM-U の枠組み層)が挟まっていないか。
6. **§5.1 の tier 分離**(T1 が $d=1$ を出しても T2 まで fake を主張しない)が過剰か適切か。

---

## 付録 A. 記号早見($n=5$ 特化)

| 記号 | 意味 | 値 |
|---|---|---|
| $T$ | $\mathrm{GT}(K^{(5)})$ | 位数 **40** |
| $\mathcal X_5$ | charming set | $\{0,1,3,4,5,6,8,9\}$(8 個) |
| $\Theta_5$ | $(k,u,\varepsilon)$、$u=2m+1\bmod5$、$\varepsilon=m\bmod2$ | $\mathbb Z/5\times(\mathbb Z/5)^\times\times C_2$ |
| $\widetilde\chi$ | $[m,f]\mapsto2m+1\bmod20$ | 像 $=(\mathbb Z/20)^\times=\{1,3,7,9,11,13,17,19\}$ |
| $\mathfrak F_0$ | $\ker\widetilde\chi$ = **$m=0$ 繊維** | $\cong C_5$、生成元 $\phi_1=[0,(r^2,r^{-2},1)]$、$\Theta_5(\phi_1)=(1,1,0)$ |
| $H_1$ | $Q^{\rm std}=\{(0,u,\varepsilon)\}$ | 位数 8、$[T{:}H_1]=5$ |
| $H^{\rm bad}$ | $\{\varepsilon=0\}$(**パリティ罠**) | 位数 20、$d=5$、$\iota\notin$、$\widetilde\chi$ 像 4 値 |
| $\iota$ | $[-1,1]=[m=9,f=1]$ | $\Theta_5(\iota)=(0,4,1)$、$\iota^2=e$、cert index 1 |
| $d_N$ | $\lvert\mathrm{Im}\,R_{N,K^{(5)}}\cap\mathfrak F_0\rvert$ | $\in\{1,5\}$ — ★ **測る量** |
| $G_5$ | $PB_3/K^{(5)}\le D_5^3$ | 位数 500、$[G_5,G_5]=A\cong C_5^3$、$G_5^{\rm ab}\cong C_2^2$ |
| $A$ | $\langle r\rangle^3$ | $\cong\chi_1\oplus\chi_2\oplus\chi_3$($Q=C_2^2$ の相異なる非自明指標)|
