# P4-0 骨子 追補 A — Sharifi 線の受領と**二段設計の強化**(裁定 838)

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5) / **状態**: candidate(Sol 未監査)
**入力**: `docs/scout/sharifi_bridge_intel_v1.md`(文献ゲート②・司令塔の機構抽出+一工夫)/ 現物 3 本は `papers/`
**先行**: `p4_0_def_lattice_compare_skeleton_v1.md`(380b289)§3 — 本追補は**その §3 を書き換える**

---

## §0 判定(1 行)

> $$\boxed{\ \textbf{二段設計は採る。ただし Sharifi の余核は「}\textbf{中継点}\textbf{」ではなく「}\textbf{差し引くべき項}\textbf{」である。}}$$
> これにより、骨子 §3.2 で指摘した**循環**が**破れる** — 循環の原因だった仮定「算術像 $=\langle\sigma\rangle$」を、**仮定せずに Sharifi の定理で測って引く**ことができる。

---

## §1 ★★★ 循環が破れる理由

骨子 §3.2 の指摘は次だった:
> $E\Rightarrow CE$ の順方向には $(\text{算術像})\subseteq L_{\rm gen}\otimes\mathbf F_p$ が要るが、成り立つのは逆向きだけで、必要な向きは「算術像が $\sigma$ たちで生成される」= 井原予想の一形 ⟹ **循環**。

**Sharifi の $\psi:\mathfrak s\to\mathfrak g$ は、まさにこの「算術像が $\sigma$ たちで生成されるか」を測る写像**である($\mathfrak s$ = Soulé 元 $\sigma_m$ 上の自由 $\mathbf Z_p$-Lie 代数、$\mathfrak g$ = 井原 Galois Lie 代数)。
- **Thm 2**($p$ 正則・Deligne 条件): $\Psi$ **全射** ⟹ 欠けていた包含は**成り立つ**。
- **Thm 3**($p$ 非正則 + Greenberg): **全射でない** ⟹ 欠けていた包含は**破れ、その破れ幅が $\mathrm{coker}_p(\psi)$**。

> $$\boxed{\ \Longrightarrow\ \textbf{「仮定できないから循環」だった量が、「条件つきで}\textbf{測れる}\textbf{量」に変わった。}}$$

---

## §2 ★★★ 中継点ではなく**差し引き** — 指数の三分解

四つの $\mathbf Z_p$-格子(または pro-$p$ 対象)を**同じ $\mathbf Q_p$-空間の中**に並べる(**同一視は §3 の未決**):

$$L_{\rm gen}\ \subseteq\ \psi(\mathfrak s)\ \subseteq\ \mathfrak g\ \subseteq\ \mathrm{ls}^{\mathbf Z_p}$$

| 記号 | 意味 | 誰が測るか |
|---|---|---|
| $[\psi(\mathfrak s):L_{\rm gen}]$ | **$\sigma$ の正規化・格子選択の差**(同じ「$\sigma$ 生成」の二表現) | P4-0 課題 1/2(格子固定) |
| $[\mathfrak g:\psi(\mathfrak s)]=\lvert\mathrm{coker}_p\psi\rvert$ | ★ **算術が $\sigma$ 生成より大きい分**(Sharifi・非正則 $p$ で非零) | **Sharifi Thm 3**(条件つき) |
| $[\mathrm{ls}^{\mathbf Z_p}:\mathfrak g]$ | ★★ **ambient が算術より大きい分 = 反例の住処** | **未建設**(北極星側) |

$$\boxed{\ E(k,p)\ \text{が測る全体} \;=\;[\mathrm{ls}^{\mathbf Z_p}:L_{\rm gen}]\;=\;\underbrace{[\mathrm{ls}^{\mathbf Z_p}:\mathfrak g]}_{\textbf{反例部}}\cdot\underbrace{[\mathfrak g:\psi(\mathfrak s)]}_{\textbf{Sharifi 部}}\cdot\underbrace{[\psi(\mathfrak s):L_{\rm gen}]}_{\textbf{正規化部}}\ }$$

> ### ★★★ 帰結 1 — **$E\ne0$ が反例の証拠にならない理由が定量化される**
> 非正則 $p$ では **Sharifi 部が非零であることが(条件つき)定理**。⟹ $E\ne0$ は**まず Sharifi 部で説明される**。
> $$\boxed{\ \textbf{alarm の正体}: E\ne0\ \textbf{は「非正則 }p\ \textbf{で Galois が }\sigma\ \textbf{生成より大きい」という}\textbf{既知の現象}\textbf{の再検出でありうる。}}$$

> ### ★★★ 帰結 2 — **正しい観測量は $E$ ではなく「$E$ ÷ Sharifi 部」**
> $$\boxed{\ \textbf{反例のシグナル} \;=\; \frac{E(k,p)}{\lvert\mathrm{coker}_p\psi\rvert\cdot[\psi(\mathfrak s):L_{\rm gen}]}\;>\;1\ }$$
> **一致すれば**: $E$ は完全に Sharifi(+正規化)で説明され、**井原側のシグナルはゼロ** ⟹ ④ の 691 は「反例の兆候」ではなく **Sharifi 現象の Lie 側の影**。
> **超過があれば**: その超過分だけが $[\mathrm{ls}:\mathfrak g]>1$ の候補 ⟹ **初めて alarm が意味を持つ**。
> ⟹ ★ **司令塔の「中継点」案を、より強い「差し引き」設計に置き換えることを提案する。**

> ### ★ 帰結 3 — $k=12$, $p=691$ の即席の検算対象
> 我々の測定は $\mathbf Z/691$(**格子の再定義後に再確認が要る** — 骨子 §1.4 と発注 LAT-CV9)。Sharifi 部は $(691,12)$ が非正則対ゆえ**非零が期待される**。
> $$\boxed{\ \textbf{IF-FIRST 凍結案 P-SHAR-1}:\ \ E(12,691)\ \textbf{と}\ \mathrm{coker}_{691}(\psi)\ \textbf{は}\textbf{同じ位数}\ (=691)\ \textbf{である}}$$
> **陽性(一致)** = ④ の 691 は Sharifi 現象 ⟹ **反例シグナルはゼロ**(そして「捩れを発見」型の主張は完全に封じられる — EIS-INDEX(骨子 §2.2)と**同方向の防波堤**)。
> **陰性(超過)** = 超過分が $[\mathrm{ls}:\mathfrak g]$ の候補 ⟹ 一級。
> ⚠ **前件**: 左の橋(§3)が立つこと。立たないうちは**この比較自体が定義できない**。

---

## §3 左の橋(motivic/ls ⟷ Galois)— **依然として最大の未決**

$\mathrm{ls}^{\mathbf Z}$ は**深さ次数付き motivic(pro-unipotent)**側、$\mathfrak g$ は**$\ell$ 進 Galois** 側。両者を同じ空間に並べるには **motivic ⟹ $\ell$ 進実現**が要り、そこで**新たな格子選択**が入る。

- ★ **ただし難度は下がった**: 骨子 §3 では「格子欠損 ⟹ 有限反例」という**異種間**の比較だった。いまは「$\sigma$ 生成 vs ambient」という**同型の量**同士の比較になる。
- **照合観点**(覚書の hunter 指定を受諾):
 (i) **両側が同じ非正則指数に支配されるか**($p\mid B_{p-k}$ 型)。
 (ii) ★ **Sharifi の $p-1$ シフト**($\sigma_{m+p-1}$ を $\sigma_m$ から作る帰納構成)が、深さ次数側の**周期性**として現れるか。
 ⟹ **(ii) は我々の側に既に相方がある**: CC-1★ の $k\equiv k_0\ (\mathrm{mod}\ p-1)$ と $j^*$ 構造(`cone_design_v1_addendum_c.md`)は**まさに $p-1$ 周期**。**同じ周期が両側に出ることは、橋の存在の状況証拠**(証明ではない)。
- **【文献要請 SHAR-LIT-1】**(一点読): `sharifi-0104116.pdf` Thm 2/3 の**正確な条件**と、$\psi$ の**定義域・値域の整構造**($\mathbf Z_p$-Lie 代数としての生成元の正規化)。**これが分からないと $[\psi(\mathfrak s):L_{\rm gen}]$ が定義できない。**

---

## §4 右の橋(Galois ⟷ 窓)と、WR-6 への集中

$\mathfrak g$ は塔($K^{(n)}$ 族・$B_3$ 有限商)の**逆極限側**の対象 ⟹ 右の橋は既存の「逆極限 ⟷ 有限窓」辞書の圏内。
$$\boxed{\ \textbf{右の橋の未決は }\mathbf{WR\text{-}6}\ \textbf{(cofinality)と}\textbf{同じ場所}\textbf{に集中する — 覚書の読みを是認する。}}$$
⟹ **WR-6 の重みがさらに上がる**(`見立て_相2_v1_3.md` §5-1 の記述を強化する材料)。COMPACT-COMPLETE(条件つき批准)+ 右の橋 = **同一の未決**。

---

## §5 McCallum–Sharifi と SAT-37 の接触 — ★ **緊張関係を先に記録**

M-S の cup 積全射性は **$p=37$ で証明済**(覚書)。一方 **P-SAT-37** は「$p=37$ の窓で算術像の指数が 37 で割れる」= **算術側の薄さ**の予言。

> ### ⚠ 記録すべき緊張(candidate・断定しない)
> cup 積全射性は「深さ 2 の算術スロットが**満杯**」を意味しうる。P-SAT-37 は「重み 5(深さ 1)の**円分元が $p$ 倍深い**」を意味する。
> $$\boxed{\ \textbf{深さが違うので直接矛盾はしないが、「37 で算術は薄いのか厚いのか」を同一の言葉で書き直す必要がある。}}$$
> ⟹ **発注案 MS37-CHK**(紙): M-S の $p=37$ 結果の**深さ・固有空間・係数**を pin し、P-SAT-37 の観測量(深さ 1・重み 5・$\omega^5$ 側)と**同じ座標に置いて比較**せよ。矛盾があれば P-SAT-37 が誤り。整合すれば **SAT-37 の岩澤側【HUNT-GAP-1】に文献の足場ができる**。
> 【文献要請 SHAR-LIT-2】(一点読): `mccallum-sharifi-0202161.pdf` の $p=37$ 証明の機構と、その固有空間・深さの規約。

---

## §6 罠の携行(覚書 §4 を受諾・1 件は規約化を提案)

| 罠 | 携行形 |
|---|---|
| **条件性** | Sharifi Thm 2/3 は **Deligne 予想・Greenberg 予想に条件つき** ⟹ 引用時に条件を落とさない。§2 の分解は**条件つき**であり、**Sharifi 部が非零であること自体が仮定に依存**する |
| ★ **語彙の罠** | Goncharov の「dihedral Lie algebra」($\mu_N$ の二面体対称由来)は **我々の dihedral 商と同名別物の可能性が高い** ⟹ **判読前に同一視しない** |
| **設定差** | Sharifi は $\mathbf Q(\zeta_{p^\infty})$ 上の pro-$p$ 塔、我々は $B_3$ 有限商の hexagon-only 系 ⟹ 翻訳に一工夫が要る(§3 の橋そのもの) |
| **格** | 覚書自身が明記するとおり **hunter の実読は Luminy ノート 3 頁のみ** ⟹ 節単位の主張は **reader 精読を経てから**。本追補の Sharifi 引用は**すべて覚書経由の二次引用**【要 pin: SHAR-LIT-1/2】 |

> ### 規約案 **NAME-COLLIDE**(規約台帳 pending へ)
> $$\boxed{\ \textbf{同名の術語(dihedral・shadow・genuine 等)を外部文献から引くときは、}\textbf{定義の一致を明示的に照合してから}\textbf{同一視する。照合前は「同名別物疑い」の札を付ける。}}$$

---

## §7 骨子 §3 の差し替え文(**確定形**)

> **旧(骨子 §3.4)**: 「$E\Rightarrow CE$ の建設は推奨しない。代わりに $CE\Rightarrow E$ を事後検証器として設計するのが健全。」
> **新(本追補)**:
> $$\boxed{\ \textbf{$E$ を「差し引き後の量」として再定義する。}\ E\ \textbf{そのものではなく }E/(\text{Sharifi 部}\times\text{正規化部})\ \textbf{が反例のシグナルである。}}$$
> ⟹ ④ の役回りは「反例検出器」でも単なる「事後検証器」でもなく、
> $$\boxed{\ \textbf{④ = 「既知の算術現象(Sharifi)を差し引いた残差を見る差分計器」}}$$
> ⟹ **実験列順位 0(P4-0)の課題 3 は、比較射の建設ではなく「差し引き項の同定」に置き換える。**

---

## §8 【GAP】・帰属・novelty

| # | 内容 | 重さ |
|---|---|---|
| ★ **【P40-GAP-4】**(新) | **左の橋**(motivic $\mathrm{ls}^{\mathbf Z}$ ⟷ $\ell$ 進 $\mathfrak g$)の格子つき比較 — 未建設。§2 の分解はこれに依存 | ★★ 最大 |
| ★ **【P40-GAP-5】**(新) | $[\psi(\mathfrak s):L_{\rm gen}]$(正規化部)は $\psi$ の整構造を pin しないと定義できない ⟹ SHAR-LIT-1 | ★ 中 |
| **【P40-GAP-6】**(新) | §5 の M-S($p=37$)と P-SAT-37 の座標合わせ未了 ⟹ MS37-CHK | 中 |
| **【P40-GAP-1/2/3】** | 骨子から継続(LAT-CV9・EIS-INDEX・§3.2 の読み) | 中 |

**帰属**: 遠征・悉皆的空振りの確定(**ls の $\mathbf Z$-整構造を扱う文献は存在しない**)= **paper-hunter**。機構抽出・翻訳・二段設計の一工夫 = **司令塔**(裁定 838)。Sharifi Thm 2/3・M-S cup 積 = **文献引用**【要 pin】。
**本追補の新規部分** = **§1 の「循環が破れる」機構**(Sharifi の $\psi$ が、循環の原因だった仮定そのものを測る写像であることの同定)/ ★ **§2 の指数三分解と「中継点 → 差し引き」への設計変更** / **観測量の再定義($E$ ではなく $E/$Sharifi 部)** / **予言候補 P-SHAR-1** / **§3(ii) の $p-1$ 周期が CC-1★ の $j^*$ 構造と同じであるという照合観点** / **§5 の M-S と SAT-37 の緊張の記録と MS37-CHK** / **規約案 NAME-COLLIDE** / **§7 の ④ の役回りの確定形(差分計器)**。

**novelty grep**(`docs/` `provenance/`): `P-SHAR-1` `MS37-CHK` `NAME-COLLIDE` `差分計器` `指数三分解` = **0 hit(本追補初出)**。`Sharifi` は `docs/scout/ribet_sharifi_retrieval_v1.md` に既在(retrieval 記録)。
