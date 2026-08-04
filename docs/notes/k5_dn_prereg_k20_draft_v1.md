# $d_N$ 本測定の事前登録票 — **$K^{(20)}$ 較正版 v1(草案)**

**状態札: `prereg draft / 較正走 / 実測ゼロ / Sol 未監査 / 発火未認可 / 封印なし(裁定 463 ★3)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-04
- 委嘱: 司令塔 —「$K^{(5)}$ 戦役の本測定($d_N$)の事前登録票を $K^{(20)}$ 標的版へ改訂起草(走らない・準備のみ)」+ **裁定 463**(走行中の 3 点裁定・本票 §0.3 に反映)
- 様式: `docs/notes/k5_genuine_campaign_v1.md` §4(IF-FIRST 凍結)/ `docs/notes/hs_prop7_translation_v1.md` §9(**S-7′ / S-8**)/ `docs/notes/k5_w6_construction_v1.md` §5(**P-W6-x / S-W6-x**)
- **本票は $\mathrm{Im}\,R_{N,K^{(5)}}$ の走査を一度も走らせる前に固定する。走行結果によって書き換えない**(改訂が要るなら v2 — **S-7′**)。
- **versioned 規律**: 本票は `k5_dn_prereg_k20_draft_v1.md`。上書き改訂はしない。

### 入力正本(SHA-256・本票起草時点)

| 出所 | SHA-256 | 使う内容 |
|---|---|---|
| `docs/notes/k5_genuine_campaign_v1.md` | `ae0433241d65ff57f50fe448437af06979aad9017819d9f4a4843f114626d7a6` | §2.1 $d_N$ の定義(逐語)・§2.2 非接触リスト・§3.2 命題 K5-DIH0・§4.3 走査規模の一般式・§4.4 衝突表・§5 実装仕様・§5.5 停止規則 |
| `docs/notes/k5_genuine_campaign_v1_addendum_a_k5mod.md` | `f91acbf2c72df4606e9eefc2e4c59cc58138ed2df8dc501a5e8981519d6e473b` | §A.13 current erratum(ERR-§5.0・elementary-5 見出し規律) |
| `docs/notes/k5_w6_construction_v1.md` | `a363b87f39026da63662f862344a33095431c13555619a921ae49f54e7dbe5d9` | §0-2 旧 2 標的の死亡・§2.1 障害の還元と前件 (V-ab)(V-der)(V-cen)・§2.3 定理 W6-OBS・§4.3 DF-W6-2・§5.2 停止規則 S-W6-x |
| `docs/notes/k5_w6_construction_v1_addendum_b_k20paper.md` | `21cd745c2e49d7287f91ad110ed89ffd41224bab8249ff53dd7eb0d394556b97` | $V=\langle r^{10}\rangle^3\cong(\mathbf Z/2)^3$・$\theta\vert_V,\tau\vert_V$・$\dim\operatorname{coker}\psi_V=1$・**S-W6-3 冒頭転記** |
| `search/certs/w6_coker_tool_20260804.json` | `288d7120dfc139dc9dfb304471430cebd0790cf99388663811d7442e42ee7c88` | 裁定 451 の機械側正本(`part3_k20_module`) |
| `docs/notes/hs_prop7_translation_v1.md` | (既登録) | §9.1 **S-7′** 逐語 |
| 正典 arXiv **2405.11725** | — | **Thm 4.3 (4.12)**(較正ゲートの正解データ)・(4.9)・Prop 3.4/3.5・Thm 4.4 |

---

> ## 非接触の申告(**campaign §6 が正本・スコープ照合は司令塔**)
>
> **本票は次を一切入力にも出力にもしていない**(campaign §2.2 の禁止量・逐語):
> > 本測定は次を**一切入力にも出力にもしない**: $u_{5,\widetilde\alpha}$ の値・$[u]_{2n}$ の類・$\hat c_\mu$・分岐値・平方類・PSL 窓の `gt_count`/`n_m`/`class_coefficient`/`settled_*`/`isolated`/`phi_image`/`normalizer_order`・rigidity 欄・`epsbits_*` の持上げ位数/P-bit・dessin の passport / perm_triple。
>
> **封印 3 量に非接触**: $\hat c_\mu$ / PSL 窓の構造量 / ε bits。**曲線・dessin・Kummer・$u$ 値も一切使わない。**
> 使った $n=5$ の情報は $G_5$ の**構造**($\lvert G_5\rvert=500$・$\lvert[G_5,G_5]\rvert=125$)と、$\mathfrak F_0$ の生成元 $\phi_1$ の**座標**(裁定 396/398 で封印解除済)だけである。
>
> ### ★ 逸脱申告(**先に名指す** — 司令塔の裁定 463 ★1 で受理済)
> **本票の起草中に、$d_{K^{(20)}}$ の値が紙で確定してしまった**(§1.3)。委嘱は「走行・実測・封印量への接触は一切しない」としており、私は hexagon 走査を 1 行も走らせていないが、**正典 Thm 4.3 の閉じた式が $\mathrm{GT}(K^{(20)})$ と $\mathrm{GT}(K^{(5)})$ の両側に与えられているため、還元 (3.60) が整数演算になり、$d_{K^{(20)}}=5$ が 4 行で出た**。
> - これは**新しい開示ではない**: campaign §3.7 の W-3 行は既に予言 $d_N=\mathbf 5$ を掲げ、**命題 K5-DIH0(2)** が $4\mid q$ 分岐でそれを主張している。本票はその値に**独立の witness を与えた**だけである。
> - しかし**設計上の含意は大きい**(§1.5)。⟹ **走行を止めずに司令塔へ速達済**(裁定 463 で受理・便 102 の枠組みは司令塔側で修正)。

---

## 0. 判定(先に 8 行)

1. **本票が事前登録するのは fake 狩りではない。** $K^{(20)}$ は**族 A(Dih)**であり、campaign **命題 K5-DIH0(2)** が既に $d_{K^{(20)}}=5$(検出力ゼロ)を主張している窓である。⟹ **本票は「較正走(DF-W6-2 control の実弾化)の事前登録」である**(裁定 463 ★1)。
2. ★ **その $d=5$ に独立の紙 witness を与えた**(§1.3): 正典 Thm 4.3 (4.12) の下で $\phi_1$ の持上げは $\mathrm{GT}(K^{(20)})$ の中に**ちょうど 2 個** — $(\widetilde m,\widetilde k)=(0,6)$ と $(10,1)$。⟹ $\phi_1\in\mathrm{Im}\,R$、$d_{K^{(20)}}=5$。**正典 Thm 4.4 の $4\mid q$ 分岐を信用せずに済む**(【W6B-GAP-2】の迂回)。
3. ★★ **$K^{(20)}$ は「3 つ目の標的死」だが、死に方が前 2 つと違う。** elementary-5 と WARN-13500 は $\operatorname{coker}\psi=0$(**障害群が消える**)で死んだ。$K^{(20)}$ は $\operatorname{coker}\ne0$ の**まま**、**障害類が $0$** で死ぬ。⟹ **S-W6-3(群 $\ne$ 類)の実物教材であり、DF-W6-2 が要求していた control そのもの**である。
4. ★★ **W6 ノート §4.3 の retrodiction は無効である**(§5 の erratum): 「$d=5$ が既知 ⟹ 障害類 $=0$」は出ない — $d=5$ は $\widetilde m=10$ の項からでも来うるからで、実際 $(10,1)$ が在る。**正しい根拠は $\widetilde m=0$ の直接 witness $(0,6)$** であり、それが在るので**結論「障害類 $=0$」は正しい**。
5. ★★ **さらに新しい欠陥を 1 件見つけた**(§2.6): **前件 (V-der)($V\subseteq[P_N,P_N]$)は $K^{(20)}$ で破れる**。$\lvert[G_{20},G_{20}]\rvert=250$ に対し $V\cong(\mathbf Z/2)^3$ は位数 8 で、$\lvert V\cap[G_{20},G_{20}]\rvert=\mathbf 2$。⟹ **障害の載る加群は $V$(3 次元)ではなく $W:=V\cap[P_N,P_N]\cong\mathbf F_2$(1 次元・$\Gamma$ 自明作用)である。**
6. ⚠ ★ **cert `w6_coker_tool_20260804.json` の `coker_dim`$=1$ は、$K^{(20)}$ 窓の障害群としては「正しい値・別の加群」である**($\dim\operatorname{coker}\psi_V=\dim\operatorname{coker}\psi_W=1$ が偶然一致する)。⟹ **CV-9 判読事項として起票**(§6 監査点 A-3)。
7. **凍結する走査規模は極小**: T2 全列挙 raw $=\lvert\mathcal X_{20}\rvert\cdot\lvert[P_N,P_N]\rvert=16\cdot250=\mathbf{4000}$、T1 走査候補 $=2\cdot\lvert W\rvert=\mathbf 4$。**RAM も cap も律速ではない。**
8. ⚠ **買わないもの**: 本票の走行は $d_{\rm gen}(5)$ について何も加えない。**$B_{\rm FC}$ への有限テストにもならない**(§3.3: $K^{(20)}$ 版の衝突表には「正典 Thm 4.3 が偽」という安価な選言が入るため、campaign §4.4 の選言は**清潔に発火しない**)。

---

## 1. 標的差替の宣言

### 1.1 旧 2 標的の死亡根拠(**W6-OBS・逐語**)

`k5_w6_construction_v1.md` §0-2(逐語):

> **委嘱が挙げた 2 候補は両方とも死んでいる。**
> - **elementary-5 側 = $\rho$ / $\rho\otimes\varepsilon$(次元 3・$62{,}500$)**: 両型とも $\operatorname{coker}\psi_V=0$ ⟹ $\phi_1$ は**必ず持ち上がる** ⟹ $d_N=5$ ⟹ **検出力ゼロ**(定理 W6-NULL5・§2.5)。**構成しても無駄弾**。
> - **$p=3$ 側 = WARN-13500($S_4$ 標準 3 次元 $\mathbb F_3$-加群)**: 同じく $\operatorname{coker}\psi_V=0$ ⟹ **検出力ゼロ**(§3.2)。**実現性を調べる前に落ちる。**

機構(同 §2.6): **$\theta$ の位数 2 と $\tau$ の位数 3 が標数を割るときだけ機構が壊れる**($p\nmid6$ なら定理 W6-OBS (C) で $\operatorname{coker}\psi_V\cong((V^\ast)^\Gamma)^\ast$ が消える)。⟹ 生存標的は $p\in\{2,3\}$ に限られる。

### 1.2 $K^{(20)}$ 採用根拠(**裁定 451**)

| 事実 | 値 | 出所 |
|---|---|---|
| $K^{(20)}=K^{(5)}\cap K^{(4)}\subset K^{(5)}$ | — | 正典 Prop 3.5($5\mid\operatorname{lcm}(20,2)=20$)/ addendum B §1 |
| $V:=\ker(G_{20}\twoheadrightarrow G_5)=K^{(5)}/K^{(20)}=\langle r^{10}\rangle^3$ | $\cong(\mathbf Z/2)^3$、$\lvert V\rvert=8$ | addendum B §2.2(紙)+ cert `v_order`=8 |
| $\theta\vert_V(b_1,b_2,b_3)=(b_2,b_1,b_3)$、$\tau\vert_V(b_1,b_2,b_3)=(b_3,b_1,b_2)$ | ($p=2$ で (4.7) の符号が消える) | addendum B §2.3 |
| $\dim_{\mathbf F_2}\operatorname{coker}\psi_V=1$ | **非零** | addendum B §2.4((A) 式のみ)+ cert `coker_dim`=1 |

**採用根拠**: 旧 2 標的が $\operatorname{coker}=0$ で死んだのに対し、$K^{(20)}$ は**両標的死亡後に初めて現れた「障害群が非零」の実標的**である(裁定 451)。

> ### ★ 冒頭転記 — 停止規則 **S-W6-3**(`k5_w6_construction_v1.md` §5.2・逐語)
> > | **S-W6-3** ★ | $\operatorname{coker}\psi_V\ne0$ を確認しただけで「検出力ある窓を作った」と書こうとした | `OVERCLAIM / STOP` | ★ **群 $\ne$ 類**(§4.1)。**障害類の非零性まで到達していない限り candidate と書く** |
>
> **⟹ 本票は $K^{(20)}$ について検出力を一切主張しない。** それどころか §1.3 で**検出力ゼロを紙で確定**する。

### 1.3 ★★ $K^{(20)}$ の $d$ は正典 Thm 4.3 だけで決まる(**本票の第 1 の内容**)

**正典 2405 Thm 4.3 (4.12)**(定義ノート §3 の【画像照合済】欄より):

$$\mathrm{GT}(K^{(n)})=\bigl\{\bigl(m,\ (r^{2k},r^{-2k},r^{\varkappa(m)})\bigr)\ \big|\ m\in\mathcal X_n,\ k\in\mathbb Z\bigr\},\qquad
\textbf{4\,|\,n のときのみ追加条件}\ \ k\equiv\tfrac{\varkappa(m)}2\ (\mathrm{mod}\ 2),$$
$$\mathcal X_n=\{m\in\{0,\dots,K_{\rm ord}^{(n)}-1\}\mid\gcd(2m+1,K_{\rm ord}^{(n)})=1\},\qquad
\varkappa(m)=\begin{cases}m+1&(m\ \text{奇})\\-m&(m\ \text{偶})\end{cases}\ \textbf{(4.9)},$$
$k$ は $\bmod\ \operatorname{ord}(r^2)=n_1$($n$ 偶なら $n/2$)。

**$n=20$ での instantiate**($K_{\rm ord}^{(20)}=20$、$n_1=10$、$4\mid20$ ゆえ追加条件が**効く**):

$$\mathcal X_{20}=\{m\in\mathbf Z/20:\ m\not\equiv2\ (\mathrm{mod}\ 5)\},\qquad\lvert\mathcal X_{20}\rvert=\mathbf{16},\qquad
\lvert\mathrm{GT}(K^{(20)})\rvert=16\cdot5=\mathbf{80}.$$

**還元(正典 (3.60)・逐語)**: $R_{N,H}:\mathrm{GT}(N)\to\mathrm{GT}(H)$、$[m,f]\mapsto(m+H_{\rm ord}\mathbb Z,\ fH_{F_2})$。ここで $H=K^{(5)}$、$H_{\rm ord}=10$。$f$-部は $D_{20}\twoheadrightarrow D_5$($r\mapsto\bar r$)の成分ごとの誘導。

> ### ★★ 補題 K20-LIFT(**本票・candidate**)
> $\phi_1=[0,(\bar r^2,\bar r^{-2},1)]\in\mathfrak F_0\subseteq\mathrm{GT}(K^{(5)})$ とする。$R_{K^{(20)},K^{(5)}}$ による $\phi_1$ の原像は、Thm 4.3 (4.12) の下で**ちょうど 2 元**であり
> $$\boxed{\ (\widetilde m,\widetilde k)=(0,\,6)\quad\text{と}\quad(10,\,1)\ }$$
> である。とくに $\phi_1\in\mathrm{Im}\,R_{K^{(20)},K^{(5)}}$、ゆえに(命題 K5-BIT より)
> $$\boxed{\ d_{K^{(20)}}=5\qquad(\textbf{検出力ゼロ})\ }$$

**証明.** $R([\widetilde m,\widetilde f])=\phi_1$ は 3 条件に分解する。
**(i) $m$ 部**: $\widetilde m\equiv0\ (\mathrm{mod}\ 10)$、$\widetilde m\in\mathcal X_{20}$ ⟹ $\widetilde m\in\{0,10\}$(どちらも $\not\equiv2\ (5)$ ゆえ $\mathcal X_{20}$ の元)。
**(ii) $f$ 第 1 成分**: $r^{2\widetilde k}\mapsto\bar r^{2\widetilde k}$ が $\bar r^2$ ⟺ $2\widetilde k\equiv2\ (\mathrm{mod}\ 5)$ ⟺ $\widetilde k\equiv1\ (\mathrm{mod}\ 5)$。第 2 成分は自動。
**(iii) $f$ 第 3 成分**: $r^{\varkappa(\widetilde m)}\mapsto\bar r^{\varkappa(\widetilde m)}$ が $1$ ⟺ $5\mid\varkappa(\widetilde m)$。$\varkappa(0)=0$ ✓、$\varkappa(10)=-10$ ✓。
**(iv) $4\mid20$ の追加条件**: $\widetilde k\equiv\varkappa(\widetilde m)/2\ (\mathrm{mod}\ 2)$。$\widetilde m=0$ では $\varkappa/2=0$ ⟹ $\widetilde k$ **偶**;$\widetilde m=10$ では $\varkappa/2=-5$ ⟹ $\widetilde k$ **奇**。
(ii)+(iv) を $\widetilde k\in\mathbf Z/10$ で解くと $\widetilde m=0$ では $\widetilde k=6$、$\widetilde m=10$ では $\widetilde k=1$ の各 1 個。∎

**★ 検出力ゼロの意味**: $\widetilde m=0$ の項に解が在るので、**命題 K5-BIT の系((N$_\theta$)(N$_\tau$)(SURJ))は $\widetilde m=0$ で可解**であり、W6 ノート §2.1 の対応により **障害類 $=0$**(§2.6 で加群を訂正した上でも同じ)。

> ⚠ **格**: 補題 K20-LIFT は**正典 Thm 4.3 の閉じた式にのみ相対**する。工房補完(THM44-odd)にも、正典 Thm 4.4 の $4\mid q$ 分岐にも、(AR) にも依存しない。**Sol 未監査。**

### 1.4 命題 K5-DIH0(2) との合流(**独立 2 経路が同じ値に着く**)

campaign §3.2 命題 K5-DIH0(2)(逐語):

> **(2)** $K^{(q)}\subseteq K^{(5)}$ となる $q\ge3$ は $5\mid\mathrm{lcm}(q,2)$ すなわち $5\mid q$。そのすべてで
> $$d_{K^{(q)}}=5\qquad(R_{K^{(q)},K^{(5)}}\ \text{は全射}).$$
> 根拠: $q$ 奇 ⟹ **補題 THM44-odd**(工房補完);$4\mid q$ ⟹ **正典 2405 Thm 4.4 の証明掲載分岐**;$q\equiv2\ (4)$ ⟹ Prop 3.4 で奇分岐に帰着。
> ⟹ **Dih 族の検出力はゼロ。**

| 経路 | 依拠 | $K^{(20)}$ での結論 | 格 |
|---|---|---|---|
| **既存**: 命題 K5-DIH0(2) | 正典 **Thm 4.4** の $4\mid q$ 分岐(**工房は再検分していない** = 【W6B-GAP-2】) | $d=5$ | paper-proof candidate(正典相対) |
| ★ **本票**: 補題 K20-LIFT | 正典 **Thm 4.3** (4.12) の閉じた式 + (3.60) | $d=5$、**witness つき** | paper-proof candidate(正典相対・**別定理**) |

> ### ★ 【W6B-GAP-2】は $K^{(20)}$ に限り**迂回して閉じた**
> addendum B §8 の申し送り「**正典 Thm 4.4($4\mid q$ 分岐)の $d=5$ を再検分していない**」は、$K^{(20)}$ については**不要になった** — Thm 4.3 で足りるからである。
> ⚠ **Thm 4.3 の読み(とくに $4\mid n$ の追加条件)は既存証明書 8 本で較正済**である(§2.5)。⟹ この迂回は**工房の在庫で裏取りされた読み**に立っている。
> ⚠ **他の Dih 窓($K^{(15)},K^{(25)},\dots$)へは本票では波及させない**(認可外)。**方法が効くことだけを記録する**(§7.4 申し送り 3)。

### 1.5 ⟹ 本票の性格(**裁定 463 ★1**)

$$\boxed{\ \textbf{本票は }K^{(20)}\textbf{ を「本測定(fake 狩り)の標的」としては事前登録しない。}\ }$$
$$\boxed{\ \textbf{事前登録するのは「較正走 = DF-W6-2 control の実弾化」である。}\ }$$

**この走行が買うもの / 買わないもの**(正直に):

| | 内容 |
|---|---|
| **買う (1)** ★★ | **「障害群は非零だが障害類は $0$」という control の実物**。DF-W6-2 が要求していたもの(W6 §4.3)。⟹ **障害ソルバが「解あり」を正しく返せることの、合成 dummy でない実窓での実証** |
| **買う (2)** ★★ | **$4\mid n$ 分岐 × 還元 の初回較正**。$\lvert\mathrm{GT}(K^{(20)})\rvert=80$ という**正典の正解データ**に対して走査器を当てる(§2.5)。$K^{(4)},K^{(8)},K^{(12)},K^{(16)}$ の既存証明書の GT 数は $4\mid n$ 追加条件込みの閉じた式と一致する(本票検算 A)ので**走査器は当該分岐を再現している**が、**$K^{(5)}$ への還元 $R$ と組で走らせたことは一度もない**(campaign §6.3: `K5.v1.json` の `reduction` 欄は空) |
| **買う (3)** ★ | **T1/T2 の tier 間突合(P-K5-10)の実弾化**。T1 候補 4 個・T2 raw 4000 と極小なので、両方走らせても無害 |
| **買う (4)** ★ | **(V-der) 破れという実物の前件破れ**(§2.6)。W6-OBS の前件が実窓で破れる初例 ⟹ **S-W6-5 の実地試験** |
| ★ **買わない (1)** | **$d_{\rm gen}(5)$ の情報**。$d_{K^{(20)}}=5$ は $\gcd$ を動かさない |
| ★ **買わない (2)** | **fake の証拠**。P-K5-1′(有限深度の PASS から genuine を導かない)は不変 |
| ★ **買わない (3)** | **$B_{\rm FC}$ への有限テスト**。§3.3 のとおり衝突が清潔に発火しない |

---

## 2. 測定の宇宙の事前固定(**走査前に固定・後から変えない**)

### 2.1 窓対(**1 対のみ**)

$$\boxed{\ N:=K^{(20)}=K^{(5)}\cap K^{(4)}=\ker\psi_{20},\qquad H:=K^{(5)}=\ker\psi_5\ }$$

$PB_3/N=G_{20}$、$PB_3/H=G_5$。$c\in K^{(m)}$(∵ 正典 (3.1) で $\psi_m(c)=(1,1,1)$)ゆえ **$c\in N$**、したがって $P_N:=F_2/N_{F_2}=PB_3/N=G_{20}$。

> ★ **$c\in N$ の帰結(危険箇所 D-6 の解除)**: campaign §5.0 の注意「$\theta,\tau$ を商 $F_2/N_{F_2}$ 上で準同型として評価する近道は $N_{F_2}$ の $\theta,\tau$-不変性を要し、それは **$c\in N$** に依存する」は、**$K^{(20)}$ では前件が満たされる**。⟹ **商水準の評価経路が使える**(語レベル経路への切替は不要)。**ただし段 0 で `c in N` を assert する**ことは省かない(campaign §5.0 の発注仕様)。

**他の窓は触らない。** $K^{(15)}$・$K^{(25)}$・PSL 屋根・$K^{(5)}\cap N_0$ は本票の宇宙に**入れない**。

### 2.2 reduction $R$(**正典 (3.60) 逐語**)

> $N\le H$ ⟹ $R_{N,H}:\mathrm{GT}(N)\to\mathrm{GT}(H)$、$[m,f]\mapsto(m+H_{\rm ord}\mathbb Z,\ fH_{F_2})$(3.60)。**isolated 同士なら群準同型。**

本件: $H_{\rm ord}=K_{\rm ord}^{(5)}=10$。$K^{(m)}$ は **isolated**(正典 Thm 4.3 / Lem 4.2)ゆえ $R_{K^{(20)},K^{(5)}}$ は**群準同型**であり (HOM) が使える。⟹ 命題 K5-BIT の前件は満たされる。
⚠ ただし実装側は **段 K5-8(settled 判定)を省かない**(campaign §5.2)。正典の isolated 主張を**信用して省略しない**ことを発注仕様に書く。

### 2.3 $d_N$ の定義(**campaign §2.1 逐語**)

> isolated な $N\subseteq K^{(5)}$($N\in\mathrm{NFI}_{PB_3}(B_3)$)に対し
> $$\boxed{\ d_N:=\bigl\lvert\mathrm{Im}\,R_{N,K^{(5)}}\cap\mathfrak F_0\bigr\rvert\ \in\ \{1,5\}\ }\qquad(\text{素数窓ゆえ 2 値 = \textbf{1 ビット}}),$$
> $$d_{\rm gen}(5)=\gcd_N d_N\quad(\text{系 DIV-GEN(2)}),\qquad\textbf{降下は高々 }\Omega(5)=1\ \textbf{回}.$$

**併せて必ず別欄で報告する量**(campaign §2.1 逐語・**fail-closed のため**):

| 欄 | 量 | なぜ別欄か |
|---|---|---|
| `image_size` | $\lvert\mathrm{Im}\,R_{N,K^{(5)}}\rvert$ | DIV-LAW が正しければ $\in\{8,40\}$。**他の値は前件のどれかの反証** |
| `chi_image` | $\widetilde\chi(\mathrm{Im})\subseteq(\mathbb Z/20)^\times$ | (CHI) の実測。**$\ne$ 全像なら補題 CHI か (AR) が偽**(パリティ罠 $H^{\rm bad}$ の検出器) |
| `iota_in_image` | $\iota=[9,1]\in\mathrm{Im}$ か | 補題 PIN-A の**枠組み非依存**な健全性検査(P-DIV-3) |
| `d_N` | $\lvert\mathrm{Im}\cap\mathfrak F_0\rvert$ | ★ **本命** |
| `k_profile` | $\{k(\xi):\xi\in\mathrm{Im}\}$ の $u,\varepsilon$ 依存性 | 像が $\{k\equiv0\ (5/d)\}$ の形か(P-DIV-2) |

> ⚠ **`image_size` から `d_N` を推論しない・`d_N` から `image_size` を推論しない。** 両方を独立に測って**突合する**のが本設計の fail-closed の核である(campaign §2.1)。

### 2.4 ★ 列挙範囲と走査規模の**凍結**(事前登録・後から増やさない)

| 量 | 凍結値 | 出所 |
|---|---|---|
| $\lvert G_{20}\rvert=\lvert P_N\rvert$ | **4000** | 紙 $4(m/2)^3$(addendum B §2.1)/ cert `g20_order` / 本票検算 C1 |
| $\lvert G_5\rvert$ | **500** | 同上 |
| $\lvert A_{20}=G_{20}\cap C_{20}^3\rvert=\lvert\langle r^2\rangle^3\rvert$ | **1000** | addendum B §2.1 / 本票検算 |
| ★ $\lvert[P_N,P_N]\rvert=\lvert[G_{20},G_{20}]\rvert$ | **250** | ★ **本票が初出**(§2.6) |
| $\lvert G_{20}^{\rm ab}\rvert$ | **16** | 同上 |
| $K_{\rm ord}^{(20)}$ | **20** | 定義ノート §3 / campaign §3.7 W-3 行 |
| $\lvert\mathcal X_{20}\rvert$ | **16** | Thm 4.3 / campaign §3.7 W-3 行 |
| ★ $\lvert\mathrm{GT}(K^{(20)})\rvert$ | **80** | ★ **Thm 4.3 (4.12) の閉じた式**(§1.3)= **較正ゲートの正解** |
| $\lvert V\rvert=\lvert K^{(5)}/K^{(20)}\rvert$ | **8** | addendum B §2.2 / cert `v_order` |
| ★ $\lvert W\rvert=\lvert V\cap[P_N,P_N]\rvert$ | **2** | ★ **本票が初出**(§2.6) |
| **T2 全列挙 raw 候補** | $\lvert\mathcal X_{20}\rvert\cdot\lvert[P_N,P_N]\rvert=16\cdot250=\mathbf{4000}$ | campaign §4.3 の様式 |
| **T1 走査候補** | $\#\{\widetilde m\in\mathcal X_{20}:\widetilde m\equiv0\ (10)\}\times\lvert W\rvert=2\cdot2=\mathbf 4$ | campaign §4.3 の一般式 |
| シャード | **不要** | 規模が 3 桁小さい |

**cap(campaign §4.3 継承・変更しない)**: `per_stage_wall_seconds: 600`・`aggregate_wall_seconds: 1800`・`gap_options: -o 2g`。**二乗 Cayley 表は禁止**。

> ⚠ **走査規模を後から増やさない**(S-7′ の運用形 2)。T1 候補 4・T2 raw 4000 は本票の凍結値であり、**実測で候補数が食い違ったら S-K20-2 で停止**する。

### 2.5 ★ 較正ゲート(**Thm 4.3 照合が先・不一致なら停止**)

$K^{(20)}$ は **Thm 4.3 族**なので**正解データが正典に在る**。⟹ 本走行は**まず較正ゲートを通す**。

| 段 | 検査 | 期待値(凍結) | 不一致時 |
|---|---|---|---|
| **G-0** | $\lvert G_{20}\rvert$・$\lvert G_5\rvert$・$\lvert[G_{20},G_{20}]\rvert$・$\lvert V\rvert$・$\lvert W\rvert$ | 4000 / 500 / 250 / 8 / 2 | **S-K20-2** |
| **G-1** ★ | $\mathcal X_{20}$ をリテラルで assert | $\{0,1,3,4,5,6,8,9,10,11,13,14,15,16,18,19\}$(16 個) | **S-K20-2** |
| **G-2** ★★ | $\mathrm{GT}(K^{(20)})$ を **hexagon 走査で全列挙**し、**Thm 4.3 (4.12) の閉じた式と集合等号**($4\mid n$ 追加条件込み) | **80 元・集合等号** | ★ **S-K20-2**(以後の全段へ進まない) |
| **G-3** | $\mathrm{GT}(K^{(5)})$ を同じ判定関数で単体走査(campaign 段 K5-3 の再実行) | **40 元**・`K5.v1.json` と $\Theta$ 集合が集合等号 | campaign **S-1** |
| **G-4** | $\mathrm{GT}(K^{(3)})$ 単体(campaign 段 K5-4) | **12 元** | campaign **S-1** |
| **G-5** | 識別力 fixture DF-1/DF-2/DF-3(campaign §5.3) | 3/3 | campaign **S-2** |

> ### ★★ G-2 が本走行の主産物である
> $4\mid n$ の追加条件 $k\equiv\varkappa(m)/2\ (\mathrm{mod}\ 2)$ は、**奇 $n$ では空虚**であり、工房の $K^{(5)}$ 系の走査は一度もこれを通っていない。$K^{(20)}$ でこれを通すことは、**走査器が Thm 4.3 の $4\mid n$ 分岐を正しく再現するかの初回試験**である。
> ⚠ **期待値 80 は driver 内のリテラル定数として hard assert する**(campaign §5.0 の証明書非読規律)。**Thm 4.3 の式をコードに書いて自分自身と比較しない**(トートロジー禁止 — 裁定 459 の 2 回目再発を防ぐ)。**閉じた式の生成側と、hexagon 走査の受理側は、別の関数・別の入力から出すこと。**

**証明書非読の例外**(addendum A §A.13.5 **ERR-§5.0** が effective source): 証明書を読む例外は **K5-1 と K5-2 の二段**。本票の G-3 は `K5.v1.json` との突合が目的そのものなので**例外の範囲内**。G-2 は**証明書を読まない**($K^{(20)}$ の証明書は存在しない — `certificates/` に `K20.v1.json` は無い)。

### 2.6 ★★ 前件 (V-der) が $K^{(20)}$ で破れる(**本票の第 2 の内容**)

W6 ノート §2.1 は障害の還元にあたり 3 前件を置いた(逐語):

> | **(V-ab)** | $V$ はアーベル |
> | **(V-der)** | $V\subseteq A_N$ |
> | **(V-cen)** | $V$ は $A_N$ の中心に入る(**または** §2.2 の捻れ版で読み替える)

($A_N:=[P_N,P_N]$。)

**実測(本票検算・python 単系統)**:

| 量 | 値 |
|---|---|
| $\lvert[G_{20},G_{20}]\rvert$ | **250** $(=2\cdot5^3)$ |
| $\lvert V\rvert$ | 8 |
| ★ $\lvert V\cap[G_{20},G_{20}]\rvert$ | **2** |
| $f_1$ の $A_{20}$ 内の持上げ | 8 個($V$-torsor) |
| ★ $f_1$ の $[G_{20},G_{20}]$ 内の持上げ | **2 個** |

$$\Longrightarrow\ \boxed{\ V\not\subseteq[P_N,P_N]\ :\ \textbf{前件 (V-der) は }K^{(20)}\textbf{ で破れる}\ }$$

(位数からも即座: $[G_{20},G_{20}]$ の位数 $250=2\cdot5^3$ の 2-部は位数 2 なので、初等アーベル位数 8 の $V$ を含めない。)

> ### ★ 傍証 — **campaign §4.3 の T1 一般式は最初から正しかった**
> campaign §4.3 の走査候補数の一般式(逐語)は
> $$\#\bigl\{\widetilde m\in\mathcal X_N:\widetilde m\equiv0\ (\mathrm{mod}\ 10)\bigr\}\ \times\ \bigl\lvert\,(K^{(5)}_{F_2}/N_{F_2})\cap[P_N,P_N]\,\bigr\rvert$$
> と、**最初から $\cap[P_N,P_N]$ を含んでいる**。⟹ 本票の $W=V\cap[P_N,P_N]$ という同定は **campaign の走査規模の式と整合**する。**食い違っているのは W6 ノート §2.1 の前件 (V-der)($V\subseteq A_N$)の側**であり、そこが「$V$ 全体で $\widetilde f$ をパラメトライズできる」と暗黙に仮定した。$K^{(25)}$ 型(campaign §4.3 の W-2 行: $5\times125$)では $V\subseteq[P_N,P_N]$ が成り立つので差が見えず、**$K^{(20)}$ で初めて分岐した**。

> ### ★ 正しい障害加群 $W$(**訂正**)
> 命題 K5-BIT は $\widetilde f\in[P_N,P_N]$ を要求する。$\widetilde f=\widetilde f_0\,b$($\widetilde f_0\in A_N$ は $f_1$ の持上げ)が $A_N$ に留まるには $b\in V\cap A_N$ でなければならない。ゆえに
> $$\boxed{\ W:=V\cap[P_N,P_N],\qquad \lvert W\rvert=2,\qquad W=\langle(1,1,1)\rangle\subseteq V\ (\text{対角線}),\qquad \Gamma\ \text{は}\ W\ \text{に自明に作用}\ }$$
> であり、**アフィン線型系は $W$ 上に載る**($\beta_\theta,\beta_\tau\in W$ も直接確認)。$W$ は $V$ の**唯一の 1 次元 $\Gamma$-部分加群**(3 点置換加群の socle)である。
> $W$(1 次元・自明)の上では $N_\theta=1+\theta=0$、$N_\tau=1+\tau+\tau^2=3=\mathrm{id}$、$W^\theta=W^\tau=W$ ゆえ
> $$\psi_W:W\to W^\theta\oplus W^\tau,\ w\mapsto(0,w),\qquad\dim\operatorname{im}=1,\ \dim(W^\theta\oplus W^\tau)=2,\qquad\boxed{\dim\operatorname{coker}\psi_W=1}.$$

> ### ⚠ **cert `w6_coker_tool_20260804.json` との関係(CV-9 事項・実装欠陥の指摘ではない)**
> cert の `part3_k20_module.coker_dim`$=1$ は **3 次元加群 $V$** 上の計算である。$K^{(20)}$ 窓の**持上げ障害**が載るのは **1 次元加群 $W$** であり、両者は**別の加群**である。**値はどちらも $1$ で一致するが、それは偶然である**(3 点置換加群と自明 1 次元加群がたまたま同じ $\dim\operatorname{coker}$ を与える)。
> ⟹ **「$\dim\operatorname{coker}\psi_V=1$ だから $K^{(20)}$ 窓の障害群は $\mathbf Z/2$」という推論は成立しない。** 結論は正しいが根拠が違う — **addendum B §3 の `formulas_agree` 意味論の確認要請と同じ型**である。**CV-9 判読(falsifier・非当事者)へ回す**(§6 監査点 A-3)。
> ⚠ **これは cert の欠陥ではない**: cert は「$V$ の $\Gamma$-加群分解」を委嘱されて $V$ を計算した(裁定 451 (3))。**(V-der) を検査する委嘱ではなかった。**

**⟹ 停止規則への反映**: W6 §5.2 の **S-W6-5**(「(V-cen) / 補題 TWIST の前件が破れる窓に当たったら `SCOPE_OUT / STOP`」)は、字義どおりなら本走行を止める。本票は §4 で **S-W6-5 の $K^{(20)}$ 版**を明示し、**「前件破れを検出したら停止」ではなく「前件破れを事前に申告した上で、$W$ 上の系として走る」**という扱いを**事前登録**する(事後の弱め方ではない)。**この扱いの可否は Sol 監査点 A-2。**

---

## 3. 予言の述語固定

### 3.1 予言表(**IF-FIRST** — 走査を一度も走らせる前に凍結)

> **裁定 463 ★3 により、本票は値を封印しない。全欄を公開し、導出を併記する。**

| # | 予言 | 値 | 根拠 | ★ 反証条件(対称形) |
|---|---|---|---|---|
| **P-K20-1** ★★ | $\lvert\mathrm{GT}(K^{(20)})\rvert$ と、その $\Theta$ 集合が Thm 4.3 (4.12) の閉じた式と**集合等号** | **80** | 正典 Thm 4.3(§1.3) | ★ **不一致 ⟹ 走査器が $4\mid n$ 分岐を再現できない、または Thm 4.3 の読みが偽**。以後の全段の情報量が消える ⟹ **S-K20-2** |
| **P-K20-2** ★★ | $\phi_1$ の原像はちょうど **2 元**、$(\widetilde m,\widetilde k)=(0,6)$ と $(10,1)$ | 上記 | ★ **補題 K20-LIFT**(本票・§1.3) | ★ 個数・座標のいずれかが外れれば **補題 K20-LIFT が偽**(= 私の紙の誤り)か還元規約が偽 |
| **P-K20-3** ★★ | $d_{K^{(20)}}$ | **5** | 補題 K20-LIFT ∧ 命題 K5-DIH0(2) の**二経路** | ★ $d=1$ ⟹ §3.3 の衝突(**まず正典 Thm 4.3 と実装を疑う**)⟹ **S-K20-1** |
| **P-K20-4** ★ | 障害類 $[(-\beta_\theta,-\beta_\tau)]\in\operatorname{coker}\psi_W\cong\mathbf Z/2=\{0,1\}$ | **$0$** | $\widetilde m=0$ の witness $(0,6)$(§1.3)。★ **retrodiction ではない**(§5) | ★ 非零 ⟹ 補題 K20-LIFT・W6-OBS・§2.6 の加群同定・補題 TWIST・実装のいずれかが偽 |
| **P-K20-5** ★★ | 障害群 $\dim_{\mathbf F_2}\operatorname{coker}\psi_W$ | **1**($\ne0$) | §2.6($W$ 1 次元自明) | ★ $0$ なら §2.6 の $W$ 同定が偽。**$3$ 次元 $V$ 上の値と混同しない**(§2.6 の警告) |
| **P-K20-6** | `image_size` $=\lvert\mathrm{Im}\,R\rvert$ | **40**(全射) | 命題 K5-DIH0(2)「$R$ は全射」 | ★ $\notin\{8,40\}$ ⟹ DIV-LAW / (AR) / (HOM) / 実装のいずれかが偽(campaign P-K5-5) |
| **P-K20-7** | `chi_image` $=\widetilde\chi(\mathrm{Im})$ | **$(\mathbb Z/20)^\times$ 全 8 値** | 補題 CHI | 4 値なら**パリティ罠**((CHI) 破れ・campaign §1.4 G8) |
| **P-K20-8** | `iota_in_image`($\iota=[9,1]$) | **true** | 補題 PIN-A(**枠組み非依存**) | false ⟹ braid 恒等式か実装が偽(**最安の健全性検査**) |
| **P-K20-9** | `k_profile`: 像は $\{k\equiv0\ (\mathrm{mod}\ 5/d)\}=\mathbb Z/5$ 全体($u,\varepsilon$ 非依存) | **全 $k$** | 定理 DIV-LAW (3) | $u,\varepsilon$ 依存の像 ⟹ DIV-LAW が偽 |
| **P-K20-10** ★ | **T1 と T2 が一致**($d_N$ が同値) | 一致 | 命題 K5-BIT(campaign P-K5-10) | 不一致 ⟹ K5-BIT の証明か実装が偽 ⟹ **中止・即報** |
| **P-K20-11** ★ | 段 K5-8(settled 判定)の fail | **0** | 正典 Thm 4.3 の isolated 主張 | ★ fail>0 ⟹ **正典の isolated 主張と食い違う** ⟹ (HOM) が使えず $d_N$ を主張しない(campaign S-6) |
| **P-K20-12** | 走査候補数(T1 / T2 raw) | **4 / 4000** | §2.4 の凍結値 | 食い違い ⟹ **S-K20-2**(宇宙の取り違え) |

> ⚠ **P-K20-1〜12 はすべて「何も出ない」ことを予言している**(較正型)。**当たっても fake 非存在の証拠にはならない。** 値打ちは**反証可能性**の側にある(campaign §4.2 の注記と同型)。
> ⚠ ★ **とくに P-K20-3(=$d=5$)は「予言」ではなく「紙で確定した値の再現」である**。当たって当然であり、**当たったことを成果と書かない**。

### 3.2 封印プロトコル(**§ は残す・適用対象は繰り延べ** — 裁定 463 ★3)

> ### ★ 封印の原理(一行)
> **封印は、導出より先に値へ到達する手段が無いときにのみ意味を持つ。**

**⟹ 本票($K^{(20)}$)には封印を適用しない。** 理由: $d_{K^{(20)}}$ も障害類も **§1.3/§3.1 で紙から導出済**であり、これを金庫封印して開封対決を演出すれば**予言の偽装**になる(裁定 447 N-1・S-8・DUM-G3 と同型の事故)。司令塔が能動的に禁止した(裁定 463 ★3)。

**封印プロトコル本体(適用対象 = 本命 W-6 標的・未構成・【K5-GAP-W4】)**:

| # | 手順 |
|---|---|
| **SEAL-1** | 標的窓 $N$ が確定し、かつ **$\operatorname{coker}\psi_{W_N}\ne0$ が紙で示され、しかも障害類が紙で決まらない**ことを起草者が明記する(=「導出より先に値へ到達する手段が無い」の確認)。**この確認が取れない標的には封印を適用しない。** |
| **SEAL-2** | 予言の**述語**(「障害類 $=0$ か否か」「$d_N\in\{1,5\}$ のどちらか」)を本票と同じ形式で**公開の票**に書く。**値は書かない。** |
| **SEAL-3** | 値(1 ビット ×2)を司令塔が**金庫**(リポジトリ外)へ封印する。封印体の SHA-256 のみを票と LEDGER に記帳する。**payload はリポジトリに一切書かない**(配置図 2026-07-25)。 |
| **SEAL-4** | 走行 → cert 出力 → **司令塔が開封して突合** → 一致/不一致を LEDGER に記帳。**不一致でも票は書き換えない**(S-7′)。 |
| **SEAL-5** | 封印量が campaign §2.2 の禁止量に触れないことを、封印前に司令塔がスコープ照合する(**専権**)。 |

### 3.3 ★★ 衝突の凍結($K^{(20)}$ 版 — **campaign §4.4 との差分が本節の要点**)

campaign §4.4 は「ある isolated $N$ で $d_N=1$ が出た」ときの 5 行の衝突を凍結し、

> $$\boxed{\ \Longrightarrow\ d_N=1\ \text{が出たら、}\ \{\text{(RCYC) の前件(とくに比較橋 }B_{\rm FC}),\ \text{(AR)},\ \text{DIV-LAW},\ u_5\ \text{測定},\ \text{本測定}\}\ \text{のどれかが偽。}\ }$$

と結んだ。**$K^{(20)}$ ではこの選言に項が 1 本増える。**

| # | 主張 | 出所 | $d_{K^{(20)}}=1$ の下での帰結 |
|---|---|---|---|
| **(0)** ★★ **新規** | $\phi_1$ の原像が $\mathrm{GT}(K^{(20)})$ に**在る**($(0,6)$ と $(10,1)$) | ★ **正典 2405 Thm 4.3 (4.12)**(+ (3.60)・本票 補題 K20-LIFT) | ★ **正典 Thm 4.3、または本票の読み、または実装が偽** |
| **(0′)** | $R_{K^{(20)},K^{(5)}}$ は全射 | 正典 2405 **Thm 4.4** の $4\mid q$ 分岐 | 正典 Thm 4.4 が偽(命題 K5-DIH0(2) の $4\mid q$ 根拠) |
| **(1)–(5)** | campaign §4.4 の 5 行(DIV-GEN・ML-ODD・FAKE-LIFT・DIV-LAT・(RCYC)+$u_5$ 実測) | campaign §4.4 | (そのまま) |

$$\boxed{\ \Longrightarrow\ K^{(20)}\ \text{で}\ d_N=1\ \text{が出たら、\textbf{まず (0)(0′) を疑う}。}\ }$$

> ### ★★ ⟹ **$K^{(20)}$ は $B_{\rm FC}$ への有限テストにならない**(campaign §4.4 の値打ちは継承されない)
> campaign §4.4 は「$n=5$ は $B_{\rm FC}$ に有限計算で触れる唯一の窓」と書いたが、**それは「$d_N=1$ を出す窓が存在したら」の話**である。$K^{(20)}$ では選言に **(0)(0′) = 正典の 2 定理**が入り、**そちらの方が圧倒的に安価な説明**である(正典には証明が載っており、工房の走査器は $4\mid n$ 分岐を一度も通していない)。
> ⟹ **$K^{(20)}$ で $d=1$ が出た場合、それは「fake の発見」ではなく「整合性の破綻」として扱う**(§4 の **S-K20-1**)。
> ⚠ **campaign §4.4 の衝突表そのものは無傷である**(本票はそれを $K^{(20)}$ で発火させないだけ)。**本命 W-6 標的(Dih 族の外・正典に定理が無い窓)では選言 (0)(0′) が入らないので、§4.4 は完全な形で使える。**

---

## 4. 停止規則

### 4.1 継承する規則(**逐語**)

> | **S-4** ★(campaign §5.5) | 測定の途中で §2.2 の禁止量($\hat c_\mu$・PSL 封印欄・ε bits・$u$ 値・dessin データ)に**触れざるを得なくなった** | **即停止・司令塔へ上申**(スコープ照合は司令塔の専権)。**自己判断で続行しない** |

> ### 停止規則 S-7′(`hs_prop7_translation_v1.md` §9.1・逐語)
> **NW-P2 のいずれかが不一致なら `PREREGISTRATION_FALSIFIED / INTEGRITY_STOP` として直ちに停止する。結果を保存し、構成 bug と数学予言の偽のどちらかを別検分する。同じ run/同じ登録の中で実測次元へ予言を書き換えない。実測値を入力にした次の研究を行うなら、旧予言が外れた事実を明記した別 version の事前登録から開始する。**
>
> **本票への読み替え**: 「NW-P2」を「**本票 §3.1 の P-K20-1〜12**」と読む。**事前登録の改稿は禁止**(改訂が要るなら v2 で、旧予言が外れた事実と本票の digest を明記して開始する)。

| # | trigger | verdict | note |
|---|---|---|---|
| **S-1**(campaign) | アンカー G-3 / G-4 のいずれかが外れる | 即停止・次段へ進まない | 後段の既知値で補正しない。`stop_reason`/`stage`/`observed`/`expected` を残す |
| **S-2**(campaign) | 識別力 fixture DF-1 が $d=1$ を返さない | 即停止 | 以後の PASS に情報量が無い |
| **S-3**(campaign) | T1 が $d_N=1$ を出す | **T2 を必ず追走** | T2 完了まで「fake 発見」と書かない。**司令塔へ即報** |
| **S-4**(campaign) | 上記逐語 | 即停止・上申 | 自己判断で続行しない |
| **S-5**(campaign) | cap 超過 | `stage_result = UNKNOWN; halt` | **事後免除なし** |
| **S-6**(campaign) | settled 判定(K5-8)で fail > 0 | $d_N$ を主張せず **UNKNOWN** | $N$ が isolated でない ⟹ (HOM) が使えない |
| **S-W6-2** | 障害ソルバが DF-W6-1(合成 dummy)で「解なし」を返さない | `CALIBRATION_FAILED / INTEGRITY_STOP` | 識別力ゼロの検査を「通った」と数えない |
| **S-W6-3** | $\operatorname{coker}\ne0$ を確認しただけで「検出力ある窓を作った」と書こうとした | `OVERCLAIM / STOP` | **群 $\ne$ 類** |
| **S-W6-6** | campaign §2.2 の禁止量に触れざるを得なくなった | campaign **S-4** 逐語 | 即停止・上申 |

### 4.2 ★ 本票が新設する規則(**$K^{(20)}$ 固有**)

| # | trigger | verdict | note |
|---|---|---|---|
| **S-K20-1** ★★ | **$d_{K^{(20)}}=1$ が出た** | `INTEGRITY_STOP`(**「fake 発見」ではない**) | ★ §3.3 の選言 (0)(0′) が先。**正典 Thm 4.3 の $4\mid n$ 追加条件の実装・還元規約・$\Theta$ 抽出器を先に検分**する。campaign **S-3** も同時発動(T2 追走・即報)。**「fake GT-shadow を発見した」と書くことを禁止する** |
| **S-K20-2** ★★ | **較正ゲート G-0/G-1/G-2 のいずれかが外れる**(とくに $\lvert\mathrm{GT}(K^{(20)})\rvert\ne80$ または集合等号が成らない) | `PREREGISTRATION_FALSIFIED / INTEGRITY_STOP`(**S-7′ 逐語**) | ★ **以後の段へ進まない**。走査器が $4\mid n$ 分岐を再現できていない可能性が最も高い ⟹ **正解データ(Thm 4.3)側と走査器側を別検分**(S-7′ 運用形 3) |
| **S-K20-3** ★ | **障害類が非零**($\ne$ P-K20-4) | `INTEGRITY_STOP` | ★ 補題 K20-LIFT の witness $(0,6)$ と**正面衝突**する。**W6-OBS が偽・§2.6 の $W$ 同定が偽・補題 TWIST の前件が破れている・実装が偽**を別検分。**この場合も「検出力ある窓を見つけた」と書かない**(S-W6-3) |
| **S-K20-4** ★ | **(V-der) 以外の前件も破れていることが判明した**(とくに (V-cen) / 補題 TWIST の $\theta_\ast^2=\mathrm{id}$・$\tau_\ast^3=\mathrm{id}$) | `SCOPE_OUT / STOP`(**S-W6-5 の本票版**) | 【K5-GAP-W1】未閉鎖 ⟹ **自己判断で続行しない**。⚠ **(V-der) の破れは §2.6 で事前申告済なので、これ単独では停止しない**(事後の弱めではなく事前登録) |
| **S-K20-5** ★ | **G-2 の受理側と生成側が同一の関数・同一の入力を通っている**ことが判明した | `TAUTOLOGY / STOP` | ★ 裁定 459(自己検査の無内容化)の 2 回目再発を防ぐ。**閉じた式(生成)と hexagon 走査(受理)は別実装・別入力**であることを発注仕様の受入条件にする |

---

## 5. ★ `k5_w6_construction_v1.md` §4.3(DF-W6-2)への **erratum**(裁定 463 ★2)

> **形式: 追記型。本体 `docs/notes/k5_w6_construction_v1.md` は一切改変しない。** 本節が当該箇所の **effective source** である(CV-10 有効出所連鎖)。引用時は本節を併記されたい。

### 5.1 対象箇所(逐語)

`k5_w6_construction_v1.md` §4.3 の DF-W6-2 注記:

> ### ★ DF-W6-2 の値打ち(**新しい実測を要しない**)
> `certificates` に $K^{(20)}$ の GT が無くとも、**$V=K^{(5)}/K^{(20)}$ の $\Gamma$-加群構造は紙で書ける**(2405 の $K^{(4)}$ 側)。⟹ **$\operatorname{coker}\ne0$ を紙で確認し、$d=5$ が既知であることから「類 $=0$」を retrodiction として得る。**

### 5.2 ★ 誤りの所在(**推論が無効**)

**「$d=5$ が既知 ⟹ 障害類 $=0$」は成立しない。**

$d=5\iff\phi_1\in\mathrm{Im}\,R$ であり(命題 K5-BIT)、その原像は $\widetilde m\equiv0\ (\mathrm{mod}\ 10)$ の**すべての項**にわたって探される。障害類 $[(-\beta_\theta,-\beta_\tau)]$ が支配するのは **$\widetilde m=0$ の項だけ**である(W6 §2.1 は $\widetilde m=0$ で $y^{\widetilde m}=1$ として系を退化させている)。ゆえに

$$\text{障害類}=0\ \Longrightarrow\ d=5\qquad\textbf{(正しい向き — W6 §1.2 の「論理の向き」そのもの)}$$
$$\text{障害類}=0\ \Longleftarrow\ d=5\qquad\textbf{(★ 成立しない)}$$

**$K^{(20)}$ ではこれが空論でない**: $\phi_1$ の原像は **2 個**あり、そのうち $(10,1)$ は $\widetilde m=10\ne0$ の項である(§1.3)。**もし $(0,6)$ が存在しなければ、$d=5$ でありながら障害類は非零だった。**

> ★ **これは W6 ノート自身の危険箇所 D-3 の裏面である**。D-3 は「$\widetilde m=0$ での不可解性から $d_N=1$ を結論する」誤りを警告した。**§4.3 の retrodiction は、同じ非対称を逆向きに踏んでいる。**

### 5.3 ★ 正しい根拠(**結論は変わらない**)

$$\boxed{\ \text{障害類}=0\ \text{の根拠は、}\widetilde m=0\ \text{の項の直接 witness}\ (\widetilde m,\widetilde k)=(0,6)\ \text{である(本票 補題 K20-LIFT)。}\ }$$

$(0,6)$ は Thm 4.3 (4.12) により $\mathrm{GT}(K^{(20)})$ の元であり、したがって (3.10)(3.11) + charming + (SURJ) を満たす。その $f$ 部 $(r^{12},r^{-12},1)$ は $[G_{20},G_{20}]$ に属する(本票検算で確認)ので、命題 K5-BIT の系の $\widetilde m=0$ 分岐の解である。⟹ **障害類 $=0$。**

### 5.4 波及(**3 点**)

| # | 波及 | 判定 |
|---|---|---|
| **E-1** | **DF-W6-2 の期待出力は不変**(「$\operatorname{coker}\ne0$ かつ 障害類 $=0$ かつ $d=5$」)。**fixture としては引き続き有効** | ✅ 不変(根拠のみ差替) |
| **E-2** | **【W6B-GAP-2】**(addendum B §8:「正典 Thm 4.4($4\mid q$ 分岐)の $d=5$ を再検分していない」)は、**$K^{(20)}$ に限り Thm 4.3 経由で迂回して閉じた** | ★ **閉(候補・$K^{(20)}$ 限定)** |
| **E-3** | **W6 §4.3 の【K5-GAP-W3】**(「$V=K^{(5)}/K^{(20)}$ の $\Gamma$-加群としての明示分解」)は addendum B が閉じたが、**本票 §2.6 により「$V$ ではなく $W=V\cap[P_N,P_N]$ が障害の載る加群」という訂正が要る** | ★ **【K20-GAP-1】として新設**(§7.3) |

---

## 6. Sol への監査点(**優先順**)

### A. 本票の数学(最優先)

- **A-1(最優先)** ★★ **補題 K20-LIFT**(§1.3)。とくに **(iv) $4\mid n$ の追加条件 $k\equiv\varkappa(m)/2\ (\mathrm{mod}\ 2)$ の使い方**と、$k$ を $\bmod\ \operatorname{ord}(r^2)=n/2=10$ で取ること。$\phi_1$ の原像が**ちょうど $(0,6)$ と $(10,1)$ の 2 元**であること、および**還元 $D_{20}\twoheadrightarrow D_5$ が $f$-三つ組に成分ごとに効く**という私の読み。**ここが本票の全体重を支えている。**
- **A-2** ★★ **前件 (V-der) の破れ**(§2.6)。$\lvert[G_{20},G_{20}]\rvert=250$・$\lvert V\cap[G_{20},G_{20}]\rvert=2$ から「**障害が載るのは $V$ ではなく $W=\langle(1,1,1)\rangle\cong\mathbf F_2$**」を結ぶ段。とくに **$\beta_\theta,\beta_\tau\in W$**(単に $\in V$ ではない)という主張と、$\widetilde f_0$ を $A_N$ の中に取れること。**さらに: 前件破れを「S-W6-5 で停止」ではなく「事前申告して $W$ 上で走る」と扱う本票の判断は妥当か**(§2.6 末尾)。
- **A-3** ★ **CV-9 事項**(§2.6 の警告枠)。cert `w6_coker_tool_20260804.json` の $\dim\operatorname{coker}\psi_V=1$(3 次元 $V$)と、本票の $\dim\operatorname{coker}\psi_W=1$(1 次元 $W$)は**別の加群の同じ値**である。**「値が一致したから二系統一致」と読まない**ための判読を求める。**falsifier(非当事者)へ回すべきか、Sol の監査で足りるか**の判断も。

### B. 設計の妥当性

- **B-1** ★★ **標的差替の妥当性**(§1.5)。「$K^{(20)}$ は Dih 族なので本測定の標的にならず、較正 control としてのみ事前登録する」という本票の判断。**裁定 451 の「W-6 標的差替の筆頭 = $K^{(20)}$」は撤回されるべきか**(司令塔は裁定 463 で撤回済 — Sol の独立判定を求める)。
- **B-2** ★★ **$p=2$ 特有の注意**。addendum B が示した「**(B) 式は $p=2$ で未証明ではなく偽**(値 $0$ を返す)」「(C) は前件不成立で数値が偶然一致」「(4.7) の符号が $p=2$ で不可視になり $\Gamma\vert_V$ の像が $S_4$ でなく $S_3$」の 3 点は、本票の $W$(1 次元自明)にどう効くか。**$W$ 上では $N_\theta=0$・$N_\tau=\mathrm{id}$ という退化が起きる**が、これは (A) 式のみで扱えているか。
- **B-3** ★ **衝突表の $K^{(20)}$ 版に漏れがないか**(§3.3)。選言に **(0) 正典 Thm 4.3 / (0′) 正典 Thm 4.4** を足したが、他に足すべき項はないか。とくに **(3.60) の還元規約**と **$\Theta_5$ 抽出器の向き規約**が独立の選言項として立つべきか。また「$K^{(20)}$ は $B_{\rm FC}$ テストにならない」という結論は正しいか。
- **B-4** ★ **erratum §5 の判定**。「$d=5\Rightarrow$ 障害類 $=0$」が無効であること、および正しい根拠が witness $(0,6)$ であること。**【W6B-GAP-2】を $K^{(20)}$ 限定で閉と記帳してよいか。**
- **B-5** **較正ゲート G-2 の設計**(§2.5)。閉じた式(生成)と hexagon 走査(受理)を別実装にする要求(S-K20-5)で、裁定 459 型のトートロジーは塞げているか。**期待値 80 を driver にリテラルで書く**ことと **CV-13(生成・受理・生成条件が同一関数)** の両立は正しいか。

---

## 7. 非接触の再宣言・格付け・検算・GAP・申し送り

### 7.1 ★ 非接触の再宣言

- **封印 3 量($\hat c_\mu$ / PSL 窓の構造量 / ε bits)に一切触れていない。**
- **$u$ 値・$[u]_{2n}$ の類・分岐値・平方類・dessin の passport / perm_triple に一切触れていない。**
- **$\mathrm{Im}\,R_{N,K^{(5)}}$ の hexagon 走査を 1 行も走らせていない**(本票で使ったのは正典 Thm 4.3 の**閉じた式**と、有限群 $G_{20},G_5$ の**構造計算**だけである)。
- ⚠ **ただし §1.3 の逸脱申告は有効**: 正典の閉じた式から $d_{K^{(20)}}=5$ が紙で出てしまった。**これは campaign §3.7 W-3 行が既に掲げていた値であり、新しい開示ではない。** 司令塔が裁定 463 ★1 で受理済。
- **$K^{(5)}$ 算術飽和 manifest の封印予言 (P1)(P2) への inference-contact event は発火していない**(裁定 412 の条件は「$d=1$ が確定した時点」であり、本票は $d=5$ 側)。W6 §6.3 X-1 行の判断を継承。
- **cert 名前空間**: 本走行の cert は **`certificates/k5gen/`** の下に置く。`k5blocks/ k5e/ k5fixture/ k5pipeline/`(すべて算術飽和戦役)に **1 バイトも書かない**。
- **`epsbits` を grep して本走行の cert が引っかからないこと**を受入条件にする(campaign N-1・W6 N-1)。

### 7.2 格付け

| 主張 | 格 |
|---|---|
| **補題 K20-LIFT**($\phi_1$ の原像 = $(0,6),(10,1)$・$d_{K^{(20)}}=5$) | ★★ **paper-proof candidate**(正典 Thm 4.3 相対・**Sol 未監査**)+ python 単系統の検算 |
| **(V-der) の破れ・$W=V\cap[P_N,P_N]\cong\mathbf F_2$ の同定** | ★★ **candidate**(**python 単系統**・**Sol 未監査**・紙の再導出は未) |
| $\dim\operatorname{coker}\psi_W=1$ | ★ **paper-proof candidate**(1 次元自明加群上の直接計算) |
| §5 の erratum(retrodiction 無効・根拠差替) | ★ **candidate**(論理の指摘・**Sol 未監査**) |
| $\lvert\mathrm{GT}(K^{(20)})\rvert=80$・$\lvert\mathcal X_{20}\rvert=16$ | **正典 Thm 4.3 からの導出**(既存証明書 8 本で読みを較正・**python 単系統**) |
| $\lvert G_{20}\rvert=4000$・$\lvert[G_{20},G_{20}]\rvert=250$ | **python 単系統**。$\lvert G_{20}\rvert$ は紙(addendum B §2.1)+ GAP cert(裁定 451)とも一致 ⟹ **3 系統一致だが CV-9 判読未** |
| 予言 **P-K20-1〜12** | **prediction(未走行)**。ただし **P-K20-2〜5 は紙で確定済の値の再現**であり、当たっても情報量はない |
| $d_{\rm gen}(5)$ の値 | ★ **UNKNOWN**(不変) |
| Lean 検証 | ✗ **していない** |

> ⚠ **cross-checked を名乗らない。** $\lvert[G_{20},G_{20}]\rvert=250$ と $W$ の同定は**本票の python 単系統のみ**である。GAP 側の独立再計算(implementer)と CV-9 判読を経るまで **candidate**。

### 7.3 【GAP】

| 札 | 内容 | 状態 |
|---|---|---|
| ★ **【K20-GAP-1】(新設)** | **$W=V\cap[P_N,P_N]$ の紙による同定**。本票は python 単系統で $\lvert W\rvert=2$・$W=\langle(1,1,1)\rangle$ を出したが、**$\lvert[G_{20},G_{20}]\rvert=250$ の紙の導出をしていない**。addendum B §2.1 が $A_m=\langle r^2\rangle^3$($m$ 偶)を紙で出したのと同じ型の計算で閉じると見積もる(**安い**) | **UNKNOWN(明示)** |
| ★ **【K20-GAP-2】(新設)** | **$\beta_\theta,\beta_\tau\in W$ の紙の確認**。本票は「$\widetilde f_0\in A_N$ を取れば $\beta$ が $W$ に落ちる」を構造から述べたが、**書き下していない**。W6 §2.1 の制約($\theta\beta_\theta=\beta_\theta$、$\tau\beta_\tau=\beta_\tau$)と合わせて 3〜5 行と見積もる | **UNKNOWN(安い)** |
| **【K5-GAP-W1】**(W6 §7.3) | 補題 TWIST の $\theta_\ast^2=\mathrm{id}$・$\tau_\ast^3=\mathrm{id}$ | **不変・UNKNOWN**。⚠ ★ **本票では射程に入る**((V-cen) を確認していないため)⟹ **S-K20-4** |
| **【K5-GAP-W3】**(W6 §7.3) | $V=K^{(5)}/K^{(20)}$ の $\Gamma$-加群分解 | addendum B が閉(紙・candidate)。★ **ただし「障害の載る加群」としては訂正が要る**(§5.4 E-3 →【K20-GAP-1】) |
| **【K5-GAP-W4】**(W6 §7.3) | **2/3-primary な $N\trianglelefteq B_3$、$N\subseteq K^{(5)}$、$V$ が生存型、の実在** | ★★ **不変・本命の律速**。$K^{(20)}$ は**これを満たさない**(Dih 族・検出力ゼロ確定) |
| **【W6B-GAP-2】**(addendum B §8) | 正典 Thm 4.4($4\mid q$ 分岐)の $d=5$ の再検分 | ★ **$K^{(20)}$ に限り閉(迂回・§5.4 E-2)**。他窓では不変 |

**【文献要請】**: 本票からの新規は**なし**。

### 7.4 申し送り(司令塔へ)

1. ★★ **便 102 の枠組み**(裁定 463 ★1 で既決): $K^{(20)}$ は (a) **較正 control の事前登録**として提出し、(b) 本命 W-6 標的の探索(**【K5-GAP-W4】**)を別立てにする。**「K⁽²⁰⁾ を本測定標的として認可請求」は撤回済。**
2. ★★ **裁定 451 の「標的差替の筆頭 = $K^{(20)}$」の訂正記帳**(司令塔が実施予定)。★ **死に方の差**(旧 2 標的 = 障害群 $0$ で死亡 / $K^{(20)}$ = 障害群 $\mathbf Z/2$ 非零・**障害類 $0$** で死亡)は **S-W6-3 の実物教材**として便 102 に載せる価値がある。
3. ★ **本票の方法の射程**(記録のみ・**波及させない**): 「Thm 4.3 が両側に閉じた式を与えるので Dih 窓の $d$ は紙 4 行で決まる」は、$K^{(15)}$・$K^{(25)}$ 等にも原理的に効く。**$K^{(15)}$ は Phase 1(認可済・段 K5-1)で証明書突合により既に確認されている**。**$K^{(25)}$ 以降は認可外なので本票では触れていない。** 起票の可否は司令塔判断。
4. ★ **【K20-GAP-1】(= $\lvert[G_{20},G_{20}]\rvert=250$ の紙)と【K20-GAP-2】($\beta\in W$ の紙)は安い**。**数学者(紙)+ implementer(GAP 裏取り)の 1 束**にまとめられる。**$\mathrm{Im}\,R$ 非接触・Phase 2 の解錠を要しない。**
5. ★ **cert `w6_coker_tool_20260804.json` の読み方**: `part3_k20_module.coker_dim`$=1$ を「$K^{(20)}$ 窓の障害群」と台帳に書くと**加群の取り違え**になる(§2.6)。**台帳の文言は「$V$(3 次元)上の $\dim\operatorname{coker}\psi_V$」と限定**されたい。cert 自体は不改変で正しい。
6. **番号衝突の回避**: 本票の新設札は **【K20-GAP-x】**・予言は **P-K20-x**・停止規則は **S-K20-x** とした(**全 3 系統を `docs/` `sol/` `provenance/` `search/` で grep 済 — 未使用を確認**)。W6 ノート §6.1 N-2 が記録した【K5-GAP-4/5】番号衝突を繰り返さないための措置。

### 7.5 検算(**証明とは独立・single lane python**)

| script | SHA-256 | 内容 | 結果 |
|---|---|---|---|
| `scratchpad/k20_prereg_universe_check.py` | `508a9e80152ba85aa7850eeb978e98b4468d307718080b71ceb6143eb2c7b388` | (A) Thm 4.3 (4.12) の読みを**既存証明書 8 本**($K^{(3)},K^{(4)},K^{(5)},K^{(8)},K^{(9)},K^{(12)},K^{(15)},K^{(16)}$)で較正 —— **$4\mid n$ 分岐込みで全一致**。(B) $n=20$ の列挙範囲。(C) ★ $\phi_1$ の原像 $=\{(0,6),(10,1)\}$ | **FAILS = 0** |
| `scratchpad/k20_g20_structure_check.py` | `71f7b8f3651e6ca16160f071586cea986b77588a8fc99127dc53269908798c36` | $G_{20}$ の構造($\lvert G_{20}\rvert=4000$・$\lvert A_{20}\rvert=1000$・★ $\lvert[G_{20},G_{20}]\rvert=250$・$\lvert V\cap[G,G]\rvert=2$)、$f_1$ の持上げ数($A_{20}$ 内 8 / $[G,G]$ 内 2)、witness $(0,6)$ の $f$ 部が $[G,G]$ に在ること、$W=\langle(1,1,1)\rangle$ の同定と $\Gamma$ 自明性、$G_5$ 側の対照($500$/$125$) | **FAILS = 0** |

**環境**: Python 3.13.14 / Windows。

> **格**: ★ **single lane(python)。cross-checked ではない・Lean 検証ではない。**
> **証明書は 8 本読んだ**(Thm 4.3 の読みの較正のため・§2.5 G-2 の期待値の根拠)。$K^{(20)}$ の証明書は**存在しない**。**$\mathrm{Im}\,R$ の hexagon 走査は 1 回も走らせていない。**
> ⚠ **検算 (A) の証明書突合は「本票の期待値 80 の根拠」であって「走査器の較正」ではない**。走査器の較正は走行時の **G-2** で行う(そこでは証明書を読まない)。

---

## 付録 A. 記号早見(本票固有)

| 記号 | 意味 | 値 |
|---|---|---|
| $N$ | 測定窓 | $K^{(20)}=K^{(5)}\cap K^{(4)}$ |
| $H$ | 底窓 | $K^{(5)}$、$H_{\rm ord}=10$ |
| $P_N$ | $F_2/N_{F_2}=PB_3/N$($c\in N$ ゆえ) | $G_{20}$、位数 **4000** |
| $A_N$ | $[P_N,P_N]$ | 位数 **250** |
| $A_{20}$ | $G_{20}\cap C_{20}^3=\langle r^2\rangle^3$ | 位数 1000(**$\ne A_N$**) |
| $V$ | $K^{(5)}_{F_2}/N_{F_2}=\ker(G_{20}\twoheadrightarrow G_5)=\langle r^{10}\rangle^3$ | $\cong(\mathbf Z/2)^3$、位数 8 |
| ★ $W$ | $V\cap A_N$ — **障害が実際に載る加群** | $=\langle(1,1,1)\rangle\cong\mathbf F_2$、位数 **2**、$\Gamma$ 自明作用 |
| $\phi_1$ | $\mathfrak F_0$ の生成元 $[0,(\bar r^2,\bar r^{-2},1)]$ | $\Theta_5(\phi_1)=(1,1,0)$ |
| $\mathcal X_{20}$ | charming set | $\{m\in\mathbf Z/20:m\not\equiv2\ (5)\}$、16 個 |
| $\varkappa(m)$ | (4.9) | $m+1$($m$ 奇)/ $-m$($m$ 偶) |
| $d_N$ | $\lvert\mathrm{Im}\,R_{N,K^{(5)}}\cap\mathfrak F_0\rvert$ | **予言 5**(§1.3 で紙確定) |
