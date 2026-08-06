# RIBET-WINDOW 検証 — 狩場プロファイル 3 条件の**全充足可否**(裁定 701)

**状態札: `design only / candidate / Sol 未監査 / 走行ゼロ・窓ゼロ・GAP ゼロ・封印非接触 / ★ 判定 = 不充足(①のみ成立・②③は構造的に落ちる)`**

- 起草: 影工房 数学者(Claude / Opus 5)・2026-08-06 / 委嘱: 司令塔 **裁定 701**(研究者最優先指令)
- 文献正本(配達): `docs/scout/ribet_sharifi_retrieval_v1.md`(9a35e7b)・`papers/` に 6 件配置済
- 既在道具: **補題 FRAT-SPLIT**(`theorem_check_mirrorall_l3vacuous_v1.md` §G.11・逐語確認済)/ **定理 MIRROR-ODD**(同 §A.3)/ **補題 SG-AB**(`sg_band_sweep_prereg_iffirst_v1.md` §2.1)/ Schur–Zassenhaus

---

## 0. 判定(先に)

> $$\boxed{\ \textbf{3 条件は全充足しない。①成立・②は Schur–Zassenhaus で構造的に不成立・③は補題 SG-AB で決定的に不成立。}\ }$$
> - **②**: 像は $C_{691}\rtimes C_m$($m\mid690$)で $\gcd(691,m)=1$ ⟹ **群拡大としては常に分裂**(Schur–Zassenhaus)⟹ FRAT-SPLIT により $C_{691}\not\le\Phi$。★ **「表現が非分裂」と「群拡大が非分裂」は別物**(§3 の罠)。
> - **③**: 像は中心自明 ⟹ $B_3$ の商なら $c\mapsto1$ 強制 ⟹ 補題 SG-AB で $\widehat G^{\rm ab}\in\{C_2,C_6\}$ 必須。しかし $\widehat G^{\rm ab}=C_{690}$。**⟹ Ribet 群は窓商になれない。**
> ⟹ **狙い撃ち作戦(④)は起票しない。**救済 3 本(§5)のうち唯一構成可能な R1 は **MIRROR-ODD が即発火して B 型を殺す**。
> ★ **ただし配達により「691 に触る道」は Lie 側で 2 本に増えた**(§6・Brown (1.4))。

---

## 1. 対象の同定 — ① $C_p$ ねじれは**成立**

**逐語根拠(配達 pin)**: **Ribet 1976, Thm 1.3(p.152)の明示的 Borel 型構成**。$\tau(n)\equiv\sigma_{11}(n)\ (691)$ より
$$\bar\rho_{\Delta,691}\ \sim\ \begin{pmatrix}\chi^{11}&*\\0&1\end{pmatrix},\qquad *\ne0\ (\text{非分解}).$$
$T$ は $U$ に**両対角指標の比 $\chi^{11}$** で作用。$\chi$ は $\bmod691$ で位数 $690$、$\gcd(11,690)=1$($690=2\cdot3\cdot5\cdot23$)ゆえ $\chi^{11}$ も**位数 690**。
$$\boxed{\ G:=\mathrm{Im}\,\bar\rho\ \cong\ C_{691}\rtimes C_{690}=\mathrm{AGL}(1,\mathbb F_{691}),\quad \lvert G\rvert=476{,}790,\quad [G,G]=C_{691},\ G^{\rm ab}=C_{690},\ Z(G)=1.\ }$$
**① = 成立**(半直積の作用が $\chi^{11}$ = 像の定義そのもの)。
**有限商の取っ手**(配達): Mazur の Eisenstein 商($\mathrm{Mordell\text{–}Weil}=\mathbb Z/n$)— 窓を切る際の有限性の担保はここから取れる。**②③ の判定は指数に依存しない**ので、以下の結論は $\chi^{11}$ の向き・正規化に不変。

## 2. ★★ ② Frattini 死角 — **構造的に不成立**(中核)

> ### 命題 RW-FRAT(candidate・本ノート)
> $1\to C_p\to\widehat P\to R\to1$、$p\nmid\lvert R\rvert$ ⟹ Schur–Zassenhaus で拡大は分裂。補題 FRAT-SPLIT($\lvert X\rvert$ 素数 ⟹ $X\le\Phi\iff$ 非分裂)より
> $$\boxed{\ C_p\le\Phi(\widehat P)\ \Longrightarrow\ p\mid\lvert R\rvert\ \Longrightarrow\ p^2\mid\lvert\widehat P\rvert.\ }$$
> Ribet 第 1 層は $691^2\nmid\lvert G\rvert$ ⟹ $C_{691}\not\le\Phi(G)$。実際 $\Phi(G)=1$(補群 $C_{690}$ の共役の交わりが自明)。∎

> ### ★ 罠の名指し(**規約台帳 pending 8 件目として上申**)
> **「表現の非分裂(加群として直和因子でない)」と「群拡大の非分裂($X\le\Phi$)」を混同しない。**
> Ribet の $*\ne0$ は**前者**。後者は Schur–Zassenhaus により $p\nmid\lvert R\rvert$ の限り**常に偽**。
> ⟹ 司令塔の②の直感(「分裂 Borel では $U\not\subset\Phi$」)は**正しく、しかも例外がない** — 選べる話ではなく強制である。

**②の正確な充足条件**: $C_{691}\le\Phi$ ⟺ $691\mid\lvert\widehat P/C_{691}\rvert$ ⟺ **691-tower の第 2 層以上**($\bmod\,691^2$ 表現・類体塔の次段)。第 1 層では**不可能**。

## 3. ★★ ③ GT 接続 — **決定的に不成立**

> ### 命題 RW-NOWIN(candidate・本ノート)
> $Z(G)=1$ の有限群 $G$ が $B_3$ の商なら $c$($=Z(B_3)$ 生成元)の像は $Z(G)=1$ ⟹ **$c\in N$ 強制** ⟹ 補題 SG-AB より $\widehat G^{\rm ab}\in\{C_2,C_6\}$。Ribet 群は $C_{690}$。∎
> $$\boxed{\ \textbf{Ribet 群(第 1 層・完全像)は }B_3\ \textbf{の窓商になりえない — SYN-0/B 型測定を載せる台がない。}\ }$$

## 4. ⑤ 救済 3 本 — いずれも代償つき

| # | 救済 | ①$\chi^{11}$ | ②$\Phi$ | ③窓 | 判定 |
|---|---|---|---|---|---|
| **R1** 切り詰め $C_{691}\rtimes C_m$($m\in\{2,6\}$・指数 1382/**4146**) | ✗ **11 が消える** | ✗ | ✔ | ★ **構成可能だが無意味**: $\mathrm{Syl}_{691}=C_{691}$ 巡回・正規・$q\ge5$ ⟹ **MIRROR-ODD 即発火** ⟹ 非 isolated・witness $[-1,1]$(**算術元・B 型でない**) |
| **R2** 第 2 層($691^2$) | ✔ | ✔ | ✗ $G^{\rm ab}$ は $C_{690}$ 系のまま | ③未解決ゆえ無効。$\lvert\widehat G\rvert\gtrsim3.3\times10^8$ で列挙外 |
| **R3** $c\notin N$($h^{\rm cen}$ 層へ) | ✔ | — | ✗ **$Z(G)=1$ が $c\in N$ を強制** | 原理的に閉じている |

> ★ **R1 の含意が最も重い**: Ribet 族から作れる唯一の合法な窓は **MIRROR-ODD 射程のど真ん中**。
> ⟹ **「$q\ge5$ の巡回正規 Sylow をもつ窓は B 型の狩場にならない」**の具体例。**狩場は $2^a3^b$ 型に戻る** — 帯掃引(`sg_band_sweep_prereg_iffirst_v1.md`)の設計が正しかったことの独立確認。

## 5. ④ 工程表 — **起票しない**(不充足)+ 器具の流用地図

| 器具 | Ribet 線での可否 |
|---|---|
| FRAT-CHIR / $H^2$ 器具 | ✗ 第 1 層は $H^2(C_{690},C_{691})=0$(位数互素)⟹ **拡大類が空で見るものがない** |
| **WWE Thm 1.2.1**(cup 積 ⟺ rank 判定・配達) | ★ **接続点として記録**。我々の $H^1/H^2$(CHIR 系)器具と同じ言語。**ただし第 1 層では $H^2=0$ ゆえ空回り** ⟹ 効くのは R2(第 2 層)以降。**WWE の $N$ と $p$ のどちらが 691 特化かは未確定**(司令塔が翻訳を引き取り済)⟹ 本ノートは「$p=691$ 特化」を**仮定**して読んでいる【RW-GAP-3】 |
| EMB-LIN | △ 出番なし(R1 が無意味) |
| **E-DIM 模型** | ✔ **無関係に有効**(§6) |
| BIT-252 型片側判定 | △ 型は流用可・標的なし |

## 6. ★ 691 に触る道は Lie 側に 2 本(**配達で 1 本増えた**)

| 道 | 内容 | 深さ | 状態 |
|---|---|---|---|
| **(A)** Ihara–Takao | $2\{f_3,f_9\}-27\{f_5,f_7\}\equiv0\ (691)$・重み 12 | **depth 2** | E-DIM $k{=}12$/$p{=}691$(裁定 656 凍結済) |
| **(B)** ★ **新**: Brown 1301.3053 **式 (1.4)** | **691 が分母として明示出現(depth-4 関係式)** | **depth 4** | ★ **本配達で判明** |

> ### ★ 前判定の訂正(`..._addendum_l4_reflection.md` §4)
> 私は「Brown 1301.3053 の深読みは**現時点では不要**」と判定した。**配達により条件が変わった**: (1.4) に **691 が分母として現れる**なら、$\mathbb F_{691}$ では**その関係式が退化する** ⟹ **GT 側($\mathcal S$ 側)にも 691 特異点がありうる**。
> これは §5 の判定「$p=691$ で落ちるのは $\mathcal A$ 側だけ」という**暗黙の前提を崩しうる** — もし $\mathcal S$ も落ちるなら不均衡は出ない。
> $$\boxed{\ \textbf{⟹ 判定を「不要」から「★ 要(条件つき・優先度中)」へ改める。読むべきは (1.4) の 691 が}\ \mathcal S\ \textbf{側の次元に効くか否かの 1 点。}\ }$$
> ⚠ **混入注意(配達の注意札を採択)**: Brown/Pollack は **pentagon 込み $B_4$ 系**が主題。$B_3$-gentle への移送は **XFER 系補題の精度確認**を通すこと。**Pollack は未刊行卒論**(格注意・単独引用しない)。

## 7. IF-FIRST 予言枠(1 本だけ登録)

| # | 予言 | 反証条件 |
|---|---|---|
| **P-RW-1** | $G'=C_{691}\rtimes C_6$(位数 4146)は $(2,3)$-生成で $B_3$ の窓商として**実在** | 非存在 ⟹ 位数 691 の元が $r,s$ の積で作れない |
| **P-RW-2** ★ | その窓で **MIRROR-ODD 発火**・$\iota(N)\ne N$・witness $[-1,1]$(算術) | 発火せず ⟹ 前件解釈の誤り |
| **P-RW-3** | その窓に **B 型候補ゼロ** | 出れば MIRROR-ODD の射程理解が誤り = 一級 |

費用: GAP 数秒(位数 4146・SmallGroups 射程外だが直接構成可)。**§0 の結論を覆さないが MIRROR-ODD の実弾較正として安い。**

## 8. GAP

- **【RW-GAP-1】** RW-FRAT / RW-NOWIN は本ノート起草の candidate(単系統・Sol 未監査)。**「Ribet 窓は存在しない」を確定として引用しない。**
- **【RW-GAP-2】** R2(第 2 層)で $\widehat G^{\rm ab}$ を $C_2/C_6$ に落とす構成の**非存在は示していない**(探索未実施)。
- **【RW-GAP-3】** WWE の $N$/$p$ のどちらが 691 特化かは未確定。本ノートは「$p=691$ 特化」を仮定。**司令塔の翻訳待ち**。
- **【RW-GAP-4】** ★ Brown (1.4) の 691 が $\mathcal S$ 側($\mathfrak{grt}$/GT 側)の次元に効くか未判定(§6・depth 4 は本工房の weight 軸と直交)。**$k=12$/$p=691$ 実験の解釈に直結**。
