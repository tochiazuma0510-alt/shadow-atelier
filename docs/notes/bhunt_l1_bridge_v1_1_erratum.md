# BH-BRIDGE **修文 addendum v1.1(erratum)** — 裁定 582 / Sol 返書 F109-2.2・F109-2.3 の逐語履行

**状態札: `candidate(paper-proof・v1 本文不改変の addendum・修文 2 点+狭形言明カード / 新規窓計算ゼロ / 機械は §3.8 の cert brgap1_kummer_20260806(75/75 PASS・負制御 6 本)/ 封印 3 量非接触 / novelty 主張なし)`**

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-06
- 委嘱: 司令塔(**裁定 582**)— Sol 便 109 返書 `sol/sol_reply_109_math35.md` の処方 2 点
- 対象: `docs/notes/bhunt_l1_bridge_v1.md`(**1 バイトも改変しない**。SHA-256 `dd2dac0d89fb453706fb3541a759a70387e8ece220cde01210e8305f9d6ebab9` を本 addendum 起草時に再計算して一致を確認 = Sol F109-1.1 の表と同一)

---

## 0. 先に 5 行

| # | 拘束 |
|---|---|
| **0-1** | **v1 は不改変。** 本 addendum が v1 の **§6.2(補題 BR-5 の証明)・§6.3(補題 BR-6)・§7.2 の前件表・§7.1 の一文**を上書きする。差分は §1.1 と §4 の表で明示する。 |
| **0-2** | **紙のみ+小さな整数検算。** GAP も pc 群も起動していない。窓の値(42 個の candidate key)を 1 個も読んでいない。 |
| **0-3** | **封印 3 量非接触**($n=5$ 系・$\mathrm{Im}\,R$・$d_N$・genuine 層の $u$ 値・PSL 量・$\varepsilon$ bits)。 |
| **0-4** | **新規の外部文献探索ゼロ。** 使ったのは既収蔵の [KUR] 印字 226/230/231/233 と [ICM] 印字 115 の**頁画像**のみ(§7 に pin 一覧)。**C1(Ichimura–Sakaguchi)は依然未入手であり、本 addendum は C1 を載荷根拠に使っていない**(§3 の証明は C1 なしで閉じる)。 |
| **0-5** | 結論はすべて **framework-relative + measurement-relative**。`cross-checked` も `verified` も付かない。 |

### 0.1 二行の結論

> $$\boxed{\ \textbf{修文 ①: Prop 5.1 の不等号誤用は }v1\ \S6.2\ \textbf{の証明 1 行のみに局在。Remark 5.2(実は等号)を載荷して閉じる。}\ }$$
> $$\boxed{\ \textbf{修文 ②: 【BR-GAP-1】は有限段 Kummer 類の直接比較で閉じた(}\S3\textbf{・補題 BR-6′)。残余ギャップは }0\ \textbf{個になった。}\ }$$

⚠ ただし **発効できるのは狭形のみ**(§5)。「非算術証人ゼロ」「FAKE-VOID」「初の窓レベル完全検証」は **発効不可**(Sol F109-3.2)。252 個の genuine/fake 分解は **UNKNOWN**。

---

## 1. 修文 ① — Kurihara Prop 5.1 の不等号向き

### 1.1 ★ 誤用箇所の特定(**1 箇所のみ・repo 全体を grep 済**)

| 場所 | v1 の記述 | 判定 |
|---|---|---|
| v1 §6.1 **(K4)** の見出し(l.233) | 「[KUR] 印字 233 **PROPOSITION 5.1** + **REMARK 5.2**」 | ✅ **正しい**(両方を (K4) として束ねている) |
| v1 §6.1 **(K4)** の逐語引用(l.234–235) | `#H^2 ≤ #(H^1/C)` および「(The above inequality is really an equality.)」 | ✅ **原典どおり**(§7 の頁画像で再照合) |
| ★ v1 §6.2 補題 BR-5 の**証明第 4 文**(l.245) | 「(K4) を $r=3$ で適用して $\#(H^1/C)\le\#H^2=1$、すなわち $C=H^1$」 | ❌ **誤用**。Prop 5.1 の不等号は逆向き。**載荷している言明(等号 = Remark 5.2)を明示的に呼び出していない**ため、書かれたとおりでは段が立たない |
| v1 §7.1(l.290) | 「[KUR] の $H^1$ 側の言明(Cor 3.8 → Cor 1.5 → **Prop 5.1**)だけを算術入力にした」 | ⚠ **前件の過少記載**(Remark 5.2 が抜けている) |
| v1 §7.2 定理の前件表 (γ)(l.274) | 「[KUR] Cor 3.8 / Cor 1.5 / §5 / **Prop 5.1**」 | ⚠ **同上**(Sol F109-2.2 の指示箇所) |
| v1 §7.3 格付け表 BR-5 行(l.313) | 「[KUR] の **4 定理**の合成のみ」 | ⚠ 正しくは **5 言明**(Cor 3.8 / Cor 1.5 / §5 の $H^1\cong\mathbb Z_p$ 段 / Prop 5.1 / **Remark 5.2**) |

> ★ **grep の結果**: 逆向き不等号は **v1 §6.2 の 1 行以外に出現しない**。`docs/`・`provenance/`・`sol/`・`ops/`・`search/certs/` を検索し、他文書への**伝播はゼロ**であることを確認した(LEDGER 2417 行の司令塔要約は Prop 4.2 / Rem 4.3 経路の記述であり、本誤用とは別物)。

### 1.2 逐語(**再照合済・頁画像 220 dpi**)

**[KUR] 印字 233 PROPOSITION 5.1**:
> "For an odd number $r\ge3$, $H^2(\mathbf Z[1/p],\mathbf Z_p(r))$ is finite, and we have
> $\#H^2(\mathbf Z[1/p],\mathbf Z_p(r))\ \leqslant\ \#(H^1(\mathbf Z[1/p],\mathbf Z_p(r))/C)$."

**[KUR] 印字 233 REMARK 5.2**:
> "This was already proved in **[2] (6.8) and (6.9)**. **(The above inequality is really an equality.)** We give here another proof following the argument of Kolyvagin. (We do not use Iwasawa's main conjecture for the proof.)"

**[KUR] 参考文献 [2]**(印字 236 で確認):
> "[2] Bloch, S. and Kato, K.: *L-functions and Tamagawa numbers of motives*, in The Grothendieck Festschrift Vol I, Progress in Math. Vol. 86, Birkhäuser (1990), 333–400."

### 1.3 ★ 修文後の補題 **BR-5**(v1 §6.2 を置き換える)

> ### 補題 BR-5(v1.1)
> 任意の奇素数 $p$ に対し、Deligne–Soulé 円分元 $c(1)$ は $H^1(\mathbb Z[1/p],\mathbb Z_p(3))\cong\mathbb Z_p$ を**生成する**。
>
> **証明.**
> 1. **(K1) = [KUR] Cor 3.8**(印字 230)より、奇素数 $p$ に対し $A^{[p-3]}=0$(無条件。$p=3$ は正則素数として別途処理・根拠は [11] Lee–Szczarba の $K_4(\mathbf Z)$)。
> 2. $A^{[k]}$ は $\omega^k$-固有空間([KUR] 印字 226 逐語)ゆえ添字は $\bmod\ (p-1)$ で定まる。$1-3=-2\equiv p-3\pmod{p-1}$ より $A^{[1-3]}=A^{[p-3]}=0$。
> 3. **(K2) = [KUR] Cor 1.5**(印字 226・$r\ge2$)を $r=3$ に適用: $A^{[1-r]}$ が零 $\iff H^2(\mathbb Z[1/p],\mathbb Z_p(r))$ が零。ゆえに $$H^2(\mathbb Z[1/p],\mathbb Z_p(3))=0 .$$
> 4. **(K3) = [KUR] 印字 233 §5** より $H^1(\mathbb Z[1/p],\mathbb Z_p(3))\cong\mathbb Z_p$(自由階数 1・$r$ 奇ゆえ捩れなし)、かつ $c(1)\ne0$。
> 5. ★ **(K4) = [KUR] Prop 5.1 + Remark 5.2** を $r=3$ に適用する。**Remark 5.2 により Prop 5.1 の不等号は等号である**から $$\#\bigl(H^1(\mathbb Z[1/p],\mathbb Z_p(3))/C\bigr)\ =\ \#H^2(\mathbb Z[1/p],\mathbb Z_p(3))\ =\ 1 .$$
> 6. ゆえに $C=H^1(\mathbb Z[1/p],\mathbb Z_p(3))$、すなわち $c(1)$ は生成元。∎

> ⚠ **Prop 5.1 単独では出ない**(Sol F109-2.2 の指摘そのもの): $H^2=0$ と $\#H^2\le\#(H^1/C)$ から得られるのは $1\le\#(H^1/C)$ という**自明な式**だけである。**載荷しているのは Remark 5.2 の等号**であり、それを明示せずに書いた v1 §6.2 の当該行は無効である。

### 1.4 ★ 依存の申告(**等号の出所**)

| 言明 | 出所 | 当工房の保持 | 依存の重さ |
|---|---|---|---|
| $\#H^2\le\#(H^1/C)$(Prop 5.1) | [KUR] 印字 233–235。**Kolyvagin/Rubin 流の Euler system 論法**・逐語「We do not use Iwasawa's main conjecture for the proof.」 | ✅ 現物保持・証明本体も印字 234–235 に掲載 | 軽い(IMC 非依存を著者が明言) |
| **等号**(Remark 5.2) | [KUR] 印字 233 の Remark 5.2。出所帰属は **[2] = Bloch–Kato, Grothendieck Festschrift I (1990), (6.8)(6.9)** | ❌ **[2] は未保持**。載荷は「Kurihara Remark 5.2 の言明」への引用として記帳 | ⚠ 中(BK 側が岩澤主予想(Mazur–Wiles)を経由する可能性は排除できない。**いずれにせよ公刊の定理であり予想ではない**) |

> ★ **正直な記帳**: 「Kurihara は Prop 5.1 を IMC なしで証明した」という但し書きは **不等号 $\le$ 側についての著者の申告**であって、**等号側は [2] に帰属**する。したがって修文後の補題 BR-5 の載荷は「Prop 5.1(現物・IMC 非依存)+ Remark 5.2 の等号言明(BK 帰属・現物未保持)」の合成である。

> ### 【文献要請 **BH-L3**】(**小・非 blocker**)
> - **困難**: 補題 BR-5 の載荷のうち **等号側**([KUR] Remark 5.2)の一次出所 **Bloch–Kato (6.8)(6.9)** を当工房が保持していない。
> - **欲しい結果の型**: 「$r\ge3$ 奇に対し $\#H^2(\mathbb Z[1/p],\mathbb Z_p(r))=\#(H^1(\mathbb Z[1/p],\mathbb Z_p(r))/C)$」を述べる一節の**言明 pin と前件**(とくに岩澤主予想を使うか否か)。
> - **不要なもの**: BK の一般論(Tamagawa 数予想の全体)・motivic な定式化。**当該 2 式の言明と前件だけでよい。**
> - **代替(= 現状)**: §1.5 の第二経路(Prop 4.2 + Rem 4.3)が Prop 5.1/Remark 5.2 を**一切使わずに**同じ結論を与える。ゆえに **BH-L3 は blocker ではない**。

### 1.5 ★ 第二経路(**Prop 5.1 を使わない独立の引用連鎖**)

[KUR] 印字 231 の逐語(§7 の頁画像で照合):

> **PROPOSITION 4.2.** "The restriction of $\varphi$ to $G_{\mathbf Q(\mu_{p^\infty})}\to\Phi(3)$ induces a surjective $G_{\mathbf Q(\mu_{p^\infty})}\to\Phi(3)/\Phi(4)\simeq\mathbf Z_p$."
>
> **REMARK 4.3.** "… Hence, $\mathrm{gr}^3\varphi$ gives an element of $H^1(\mathbf Z[1/p],\mu_{p^\infty}],\mathbf Z_p(3))^{G_\infty}\simeq H^1(\mathbf Z[1/p],\mathbf Z_p(3))$. We know that $\mathrm{gr}^3\varphi$ … coincides with the cyclotomic element of Deligne–Soulé $c(1)$ … modulo $\mathbf Z_p^\times$ ([8] Th. B, [3] Th. C). **Hence, the surjectivity of $\mathrm{gr}^3\varphi$ corresponds to the fact that the cyclotomic element generates $H^1(\mathbf Z[1/p],\mathbf Z_p(3))$.** The latter is also deduced from Proposition 5.1 below and $H^2(\mathbf Z[1/p],\mathbf Z_p(3))=0$."

⟹ **Prop 4.2 + Remark 4.3 ⟹ 補題 BR-5 の結論**($c(1)$ が $H^1$ を生成する)。

> ★ **この第二経路は §7.1 の飽和性(saturation)の罠に触れない。** 罠は「$\Phi(3)/\Phi(4)\hookrightarrow\mathrm{gr}_3(\mathscr F)\otimes\mathbb Z_p$ の像が直和因子か」という**窓へ降ろす段**の問題であり、いま使っているのは **$H^1$ 側の生成性だけ**である(窓へ降ろすのは §3 の補題 BR-6′ と v1 の補題 BR-3 が担い、そこでは $\Phi$ を一切通らない)。v1 §7.1 の診断は**そのまま正しい**(Sol F109-2.4 も PASS)。
>
> ⚠ **依存申告**: 第二経路の入力 [7] Th. 6(Ihara, Annals 1986)・[8] Th. B(IKY)・[3] Th. C(Coleman)は **当工房未保持**。ゆえに第二経路は**引用連鎖レベルの独立確認**であって、自前で検証した経路ではない。**主経路は §1.3(修文後の BR-5)。**

### 1.6 前件表の差し替え(**Sol F109-2.2 の指示箇所**)

| v1 の記述 | v1.1 での正 |
|---|---|
| §7.2 定理 BH-BRIDGE 前件 (γ)「[KUR] Cor 3.8 / Cor 1.5 / §5 / **Prop 5.1**」 | 「[KUR] Cor 3.8(印字 230)/ Cor 1.5(印字 226)/ §5 の $H^1\cong\mathbb Z_p$ 段(印字 233)/ **Prop 5.1 + Remark 5.2**(印字 233)」 |
| §7.1 末「(Cor 3.8 → Cor 1.5 → **Prop 5.1**)だけを算術入力にした」 | 「(Cor 3.8 → Cor 1.5 → **Prop 5.1 + Remark 5.2**)だけを算術入力にした」 |
| §7.3 「[KUR] の **4 定理**の合成のみ」 | 「[KUR] の **5 言明**の合成のみ(自前の新段なし)」 |

---

## 2. 修文 ①の副産物 — 補題 **BR-5′**(生成 ⟹ 窓で使う全射性)

v1 §6.2 の末尾には「$c(1)$ は $p$ で割れない ⟹ 準同型として全射」という括弧書きがあったが、**そこで暗黙に使われている同型**(制限写像が $G_\infty$-不変部分への同型であること)が明示されていなかった。修文の機会に厳密化する。**これは Sol の指摘事項ではない自主的な補強である。**

> ### 補題 BR-5′
> $p$ 奇素数、$r=3$。$c(1)$ が $H^1(\mathbb Z[1/p],\mathbb Z_p(3))\cong\mathbb Z_p$ を生成するならば、$\kappa^{(p)}_3$ が定める準同型
> $$\kappa^{(p)}_3\big\vert:\ G_{\mathbb Q(\mu_{p^\infty})}\longrightarrow\mathbb Z_p$$
> は**全射**である。とくに $\kappa^{(p)}_3(\sigma)\in\mathbb Z_p^\times$ なる $\sigma\in G_{\mathbb Q(\mu_{p^\infty})}$ が存在する。
>
> **証明.**
> **(i)** $\kappa^{(p)}_3$ は [ICM] 印字 115 §6.2 (ii) により $\mathrm{Gal}(\mathbb Q(\mu_{p^\infty})^{\rm ab}/\mathbb Q)$ を経由し、$p$ の外で不分岐([ICM] 印字 112 §5.2・[KUR] Rem 4.3 の "unramified outside $p$")。ゆえに類 $[\kappa^{(p)}_3]\in H^1(\mathbb Z[1/p],\mathbb Z_p(3))$ が定まる。
> **(ii)** §3 の定理 BR-6′ より $[\kappa^{(p)}_3]=u\,[c(1)]$($u\in\mathbb Z_p^\times$)。仮定より $[\kappa^{(p)}_3]$ も生成元。
> **(iii)** $G_\infty=\mathrm{Gal}(\mathbb Q(\mu_{p^\infty})/\mathbb Q)$、$\Delta\subseteq G_\infty$ を位数 $p-1$ の部分群とする。$M=\mathbb Z_p(3)$ に $\Delta$ は $\omega^3$ で作用し、$3\not\equiv0\pmod{p-1}$($p$ 奇ゆえ $p-1$ は偶数で $p-1\nmid3$)より $M^\Delta=0$。$\lvert\Delta\rvert$ は $p$ と互いに素なので $H^i(G_\infty,M)=H^i(G_\infty/\Delta,M^\Delta)=0$($i\ge0$)。inflation–restriction より
> $$\mathrm{Res}:\ H^1(\mathbb Z[1/p],\mathbb Z_p(3))\ \xrightarrow{\ \sim\ }\ H^1(\mathbb Z[1/p,\mu_{p^\infty}],\mathbb Z_p(3))^{G_\infty}$$
> は**同型**(この同型は [KUR] 印字 231 Remark 4.3 が逐語で述べているものと同一)。右辺は $G_{S}(\mathbb Q(\mu_{p^\infty}))$ が $\mathbb Z_p(3)$ に自明に作用するので $\mathrm{Hom}^{G_\infty}_{\rm cont}\bigl(G_S(\mathbb Q(\mu_{p^\infty}))^{\rm ab},\mathbb Z_p(3)\bigr)$ であり、$\mathbb Z_p$ 自由階数 1、生成元は $[\kappa^{(p)}_3]$。
> **(iv)** もし像が $p^k\mathbb Z_p$($k\ge1$)に含まれるなら $p^{-k}\kappa^{(p)}_3$ も同じ Hom 群の元、ゆえに $p^{-k}\kappa^{(p)}_3=c\,\kappa^{(p)}_3$($c\in\mathbb Z_p$)。Hom 群は捩れなしで $\kappa^{(p)}_3\ne0$ ゆえ $p^{-k}=c\in\mathbb Z_p$ となり $k\ge1$ に矛盾。∎

> ★ **独立の第二論法(mod $p$ 版)**: $H^2(\mathbb Z[1/p],\mathbb Z_p(3))=0$(補題 BR-5 の段 3)より、係数の短完全列 $0\to\mathbb Z_p(3)\xrightarrow{p}\mathbb Z_p(3)\to\mathbb F_p(3)\to0$ から $$H^1(\mathbb Z[1/p],\mathbb F_p(3))\ \cong\ H^1(\mathbb Z[1/p],\mathbb Z_p(3))/p\ \cong\ \mathbb F_p .$$ 生成元の mod $p$ 還元は非零、かつ $\mathrm{Res}$ は mod $p$ でも単射((iii) と同じ理由)ゆえ $\kappa^{(p)}_3\bmod p\ne0$。同じ結論。**二つの論法は同じ入力から独立に落ちる。**

---

## 3. 修文 ② — 【BR-GAP-1】を**有限段 Kummer 類の直接比較**で閉じる

Sol F109-2.3 の処方(「有限段 $K_n$ で Kummer 類を直接比較せよ」)を、**逐語 pin つきの完全な証明**として書き下す。v1 §6.3 のスケッチを置き換える。

### 3.0 設定・記号・正規化規約

- $p$ 奇素数、$r\ge3$ 奇(必要なのは $r=3$)、$S=\{p,\infty\}$。
- $K_n=\mathbb Q(\mu_{p^n})$、$R_n=\mathbb Z[1/p,\mu_{p^n}]$、$R_0=\mathbb Z[1/p]$、$G_n=\mathrm{Gal}(K_n/\mathbb Q)\cong(\mathbb Z/p^n)^\times$、$\tau_a(\zeta)=\zeta^a$。
- $H^i(R,\,\cdot\,)$ は $p$ 冪係数の étale = $G_S$ の Galois コホモロジー($p$ 奇ゆえ実素点の寄与なし)。
- **(NORM-1)** [ICM] 印字 115 の $\zeta_n=\exp(2\pi i/p^n)$ を**両構成で共通に**使う。これは $\zeta_{n+1}^{\,p}=\zeta_n$ を満たす整合系であり、$\mathbb Z_p(m)$ の基底 $\zeta^{\otimes m}$ と $\mathbb Z/p^n(m)$ の基底 $\zeta_n^{\otimes m}$ を与える。**Kummer 類の取り方は $\sigma\mapsto\sigma(u^{1/p^n})/u^{1/p^n}$**、$p^n$ 乗根は [ICM] の規約どおり**正の実根**を取る($\varepsilon_{m,n}$ は totally positive — [ICM] 逐語)。
- **(NORM-2)** 別の整合系 $\zeta^u$($u\in\mathbb Z_p^\times$)や逆向きの Kummer 規約を採れば、両辺はそれぞれ $\mathbb Z_p^\times$ 倍だけ動く。ゆえに**結論「$\mathbb Z_p^\times$ 倍で一致」は正規化に依らない**。以下は (NORM-1) の下で**等号**まで出す。

**[KUR] 印字 233 §5 (4) 逐語**(頁画像で再照合):
> "$H^1(\mathbf Z[1/p,\eta,\mu_{p^n}],\mathbf Z/p^n(r))$ of $(1-\zeta_{p^n}\eta^{1/p^n})\otimes(\zeta_{p^n})^{\otimes(r-1)}\in(\mathbf Z[1/p,\eta,\mu_{p^n}]^\times/p^n)\otimes\mu_{p^n}^{\otimes(r-1)}$.
> Further, we define Deligne–Soulé's cyclotomic element by
> $c(\eta)=\varprojlim_n\mathrm{Cor}_{\mathbf Z[1/p,\eta,\mu_{p^n}]/\mathbf Z[1/p,\eta]}(\eta_n)\in\varprojlim H^1(\mathbf Z[1/p,\eta],\mathbf Z/p^n(r))=H^1(\mathbf Z[1/p,\eta],\mathbf Z_p(r))$ … (4)"

⟹ $\eta=1$ に特殊化して($\eta^{1/p^n}=1$)、**有限段の Kurihara 元**は
$$c_n\ :=\ \bigl[(1-\zeta_n)\bigr]\otimes\zeta_n^{\otimes(r-1)}\ \in\ H^1(R_n,\mathbb Z/p^n(r)),\qquad c(1)=\varprojlim_n\mathrm{Cor}_{R_n/R_0}(c_n).$$
(v1 §6.3 の書き方と同一。**原典は一般の $\eta$ 付きであり、$c(1)$ はその $\eta=1$ 特殊化**であることを明記しておく。)

**[ICM] 印字 115 §6.2 (ii) 逐語**(頁画像で再照合):
> "$\varepsilon_{m,n}=\prod_a(\zeta_n^a-1)^{\langle a^{m-1}\rangle}$, where the product is over all integers $a$ such that $0<a<l^n$ and $(a,l)=1$; $\langle a^{m-1}\rangle$ is the smallest positive integer congruent to $a^{m-1}$ mod $l^n$. … Hence there is a unique $\kappa^{(l)}_m(\sigma)\in\mathbb Z_l$ such that
> $\sigma((\varepsilon_{m,n})^{1/l^n})=(\sigma(\varepsilon_{m,n}))^{1/l^n}\cdot\zeta_n^{\chi^{(l)}(\sigma)^{1-m}\cdot\kappa^{(l)}_m(\sigma)}$
> holds for all $n\ge2$."

### 3.1 補題 A(**制限写像の単射性**)

> $r\not\equiv0\pmod{p-1}$(とくに $r=3$、$p$ 奇)ならば、任意の $n\ge1$ に対し
> $$\mathrm{Res}:\ H^1(R_0,\mathbb Z/p^n(r))\ \xrightarrow{\ \sim\ }\ H^1(R_n,\mathbb Z/p^n(r))^{G_n}$$
> は同型。とくに**単射**。
>
> **証明.** $K_n/\mathbb Q$ は $S$ の外で不分岐ゆえ $1\to G_S(K_n)\to G_S(\mathbb Q)\to G_n\to1$ は完全。$M=\mathbb Z/p^n(r)$ に $G_S(K_n)$ は自明に作用する($\mu_{p^n}\subset K_n$)ので $M^{G_S(K_n)}=M$、$G_n$ は $\chi^r$ で作用。$\Delta\subseteq G_n$ を位数 $p-1$ の部分群、$g$ をその生成元とすると、$g\bmod p$ は $(\mathbb Z/p)^\times$ の生成元ゆえ $g^r\equiv1\pmod p\iff(p-1)\mid r$。仮定より $g^r-1$ は $\mathbb Z/p^n$ の単元で $M^\Delta=0$。$\lvert\Delta\rvert$ は $p$ と互いに素、$M$ は $p$ 群なので
> $$H^i(G_n,M)=H^i(G_n/\Delta,\ M^\Delta)=0\qquad(\forall i\ge0).$$
> inflation–restriction 列の両端が消えるので同型。∎($g^r-1$ の単元性は §3.8 cert の (K5))

### 3.2 補題 B(**$\mathrm{Res}\circ\mathrm{Cor}=\sum_{a\in G_n}(\tau_a)_*$**)

> $H\trianglelefteq G$ を開正規部分群、$M$ を離散 $G$-加群とすると、$H^*(H,M)$ 上で
> $$\mathrm{Res}^G_H\circ\mathrm{Cor}^G_H=\sum_{g\in G/H}g_* .$$
>
> **証明(標準・自己完結)**。両辺は $\delta$-関手 $H^*(H,-)$ の自己射であり、連結写像と可換する。次数 0 では $\mathrm{Cor}(x)=\sum_{g\in G/H}gx$、$\mathrm{Res}$ は包含なので両辺は $x\mapsto\sum_g g_*x$ で一致する。正次数では $M$ を余誘導加群に埋め込む次元シフトで次数 0 に帰着する。∎
>
> 本件では $G=G_S(\mathbb Q)$、$H=G_S(K_n)$、$G/H=G_n$ であり、$g_*$ は $H^1(R_n,M)$ 上の $G_n$ の自然な作用(共役 + 係数作用)である。

> ★ **これで v1 §6.3 の「逐語確認点 その 1」(corestriction を $\sum\tau_a$ と書くか $\sum\tau_a^{-1}$ と書くか)は完全に消える**: 和は $G_n$ **全体**を走るので $\sum_a\tau_a=\sum_a\tau_a^{-1}$ が群環 $\mathbb Z[G_n]$ の中で**元として等しい**。向きの問題は生じない(§3.8 cert の (K3) で $\{a^{-1}\}=\{a\}$ を機械確認)。**v1 のスケッチが $b=a^{-1}$ の置換で得た式は正しかったが、その正当化はいま不要になった。**

### 3.3 補題 C(**$G_n$ 作用の明示形**)

> $u\in R_n^\times$、$a\in(\mathbb Z/p^n)^\times$ に対し、$H^1(R_n,\mathbb Z/p^n(r))$ の中で
> $$\tau_a\bigl([u]\otimes\zeta_n^{\otimes(r-1)}\bigr)\ =\ \bigl[\tau_a(u)^{a^{r-1}}\bigr]\otimes\zeta_n^{\otimes(r-1)} .$$
>
> **証明.** Kummer 写像 $R_n^\times/(R_n^\times)^{p^n}\hookrightarrow H^1(R_n,\mu_{p^n})$ は $G_S(\mathbb Q)$-同変。$\tau_a(\zeta_n)=\zeta_n^a$ より $(\zeta_n^a)^{\otimes(r-1)}=a^{r-1}\cdot\zeta_n^{\otimes(r-1)}$($\mu_{p^n}^{\otimes(r-1)}\cong\mathbb Z/p^n$ の中の等式)。Kummer 群は $\mathbb Z/p^n$-加群なのでスカラー $a^{r-1}$ を指数へ移せる。∎

> ⟹ 補題 B・C と $\tau_a(1-\zeta_n)=1-\zeta_n^a$ より、$H^1(R_n,\mathbb Z/p^n(r))$ の中で
> $$\boxed{\ \mathrm{Res}\bigl(\mathrm{Cor}_{R_n/R_0}(c_n)\bigr)\ =\ \Bigl[\ \prod_{a\in(\mathbb Z/p^n)^\times}(1-\zeta_n^a)^{a^{r-1}}\ \Bigr]\otimes\zeta_n^{\otimes(r-1)} .\ }\tag{3.1}$$
> (指数 $a^{r-1}$ は $\bmod\ p^n$ で定まればよい。)

### 3.4 補題 D(**Ihara の $\varepsilon_{r,n}$ と一致**)

> $$\Bigl[\prod_a(1-\zeta_n^a)^{a^{r-1}}\Bigr]\ =\ \bigl[\varepsilon_{r,n}\bigr]\qquad\text{in }R_n^\times/(R_n^\times)^{p^n}.$$
>
> **証明.** 2 点。
> **(D1) 指数の代表.** $\langle a^{r-1}\rangle\equiv a^{r-1}\pmod{p^n}$(最小正代表の定義)。$R_n^\times/(R_n^\times)^{p^n}$ は $p^n$ で消えるので指数の代表の取り方に依らない。具体的には $d_a:=(\langle a^{r-1}\rangle-a^{r-1})/p^n\in\mathbb Z_{\le0}$ とおくと $(1-\zeta_n^a)^{\langle a^{r-1}\rangle-a^{r-1}}=\bigl((1-\zeta_n^a)^{d_a}\bigr)^{p^n}$。
> **(D2) 符号.** $\zeta_n^a-1=-(1-\zeta_n^a)$、かつ $p^n$ は奇数ゆえ $-1=(-1)^{p^n}\in(R_n^\times)^{p^n}$。ゆえに $S:=\sum_a\langle a^{r-1}\rangle$ に対し $(-1)^S=\bigl((-1)^S\bigr)^{p^n}$ は $p^n$ 乗。
> 合わせて $\varepsilon_{r,n}\cdot\prod_a(1-\zeta_n^a)^{-a^{r-1}}=\bigl((-1)^S\prod_a(1-\zeta_n^a)^{d_a}\bigr)^{p^n}$。∎
>
> ★ **副産物**: $r$ が奇 ⟹ $r-1$ が偶 ⟹ $\langle a^{r-1}\rangle=\langle(-a)^{r-1}\rangle$ で項が対になり **$S$ は常に偶数**。したがって本件では符号因子は**そもそも消えている**((D2) はより頑健な理由を与えるので両方を残す)。§3.8 cert の (K1)(K2)(K4)(K7)+負制御 (N2)(N4)(N5)(N6)。

> ★ **これで v1 §6.3 の「逐語確認点 その 2」($\langle a^{m-1}\rangle$ の最小正代表の扱い)も消える。**

### 3.5 補題 E(**$\kappa^{(p)}_r$ の Kummer 記述**)

> $n\ge2$ に対し、$H^1(R_n,\mathbb Z/p^n(r))$ の中で
> $$\mathrm{Res}\bigl([\kappa^{(p)}_r]\bmod p^n\bigr)\ =\ [\varepsilon_{r,n}]\otimes\zeta_n^{\otimes(r-1)} .$$
>
> **証明.** $\sigma\in G_S(K_n)$ とすると $\chi^{(p)}(\sigma)\equiv1\pmod{p^n}$ ゆえ $\chi^{(p)}(\sigma)^{1-r}\equiv1$、また $\varepsilon_{r,n}\in K_n$ より $\sigma(\varepsilon_{r,n})=\varepsilon_{r,n}$。[ICM] 印字 115 の定義式はこの $\sigma$ に対し
> $$\frac{\sigma(\varepsilon_{r,n}^{1/p^n})}{\varepsilon_{r,n}^{1/p^n}}=\zeta_n^{\ \kappa^{(p)}_r(\sigma)\bmod p^n}$$
> となる。左辺は定義により $\varepsilon_{r,n}$ の Kummer 1-cocycle の $\sigma$ での値、右辺は基底 $\zeta_n$ による $\mu_{p^n}\cong\mathbb Z/p^n(1)$ の同一視での $\kappa^{(p)}_r(\sigma)$。$\zeta_n^{\otimes(r-1)}$ を掛けて $\mathbb Z/p^n(r)$ 係数にすれば、$G_S(K_n)$ は $\mathbb Z/p^n(r)$ に自明に作用するので $H^1(R_n,\mathbb Z/p^n(r))=\mathrm{Hom}_{\rm cont}(G_S(K_n),\mathbb Z/p^n(r))$ であり、**両辺は準同型として各点で一致する**。∎
>
> (前提: $\varepsilon_{r,n}=\prod_a(\zeta_n^a-1)^{\langle\cdot\rangle}$ は $R_n=\mathbb Z[1/p,\mu_{p^n}]$ の単元 — $(\zeta_n^a-1)$ は $p$ の上の素元 — ゆえ Kummer 拡大は $p$ の外で不分岐で、類は $H^1(R_n,\cdot)$ に入る。)

### 3.6 ★★ 定理 **BR-6′**(v1 の補題 BR-6 = 【BR-GAP-1】を置き換える)

> ### 定理 BR-6′
> $p$ 奇素数、$r\ge3$ 奇、(NORM-1) の規約の下で
> $$\boxed{\ [\kappa^{(p)}_r]\ =\ [c(1)]\quad\text{in }H^1(\mathbb Z[1/p],\mathbb Z_p(r)).\ }$$
> とくに $\kappa^*_r=(p^{r-1}-1)^{-1}\kappa^{(p)}_r$ について $[\kappa^*_r]=(p^{r-1}-1)^{-1}[c(1)]$ であり、$p^{r-1}-1\equiv-1\pmod p$ は $\mathbb Z_p^\times$ の元。ゆえに規約に依らず
> $$[\kappa^{(p)}_r]=u\,[c(1)],\qquad [\kappa^*_r]=u'\,[c(1)],\qquad u,u'\in\mathbb Z_p^\times .$$
>
> **証明.** $n\ge2$ を固定する。
> $$\mathrm{Res}\bigl(\mathrm{Cor}_{R_n/R_0}(c_n)\bigr)\overset{(3.1)}{=}\Bigl[\prod_a(1-\zeta_n^a)^{a^{r-1}}\Bigr]\otimes\zeta_n^{\otimes(r-1)}\overset{\text{補題 D}}{=}[\varepsilon_{r,n}]\otimes\zeta_n^{\otimes(r-1)}\overset{\text{補題 E}}{=}\mathrm{Res}\bigl([\kappa^{(p)}_r]\bmod p^n\bigr).$$
> 補題 A より $\mathrm{Res}$ は $H^1(R_0,\mathbb Z/p^n(r))$ 上単射なので
> $$\mathrm{Cor}_{R_n/R_0}(c_n)=[\kappa^{(p)}_r]\bmod p^n\qquad\text{in }H^1(R_0,\mathbb Z/p^n(r)).$$
> $n\ge2$ について射影極限を取り、[KUR] (4) の $c(1)=\varprojlim_n\mathrm{Cor}(c_n)$ と $\varprojlim_nH^1(R_0,\mathbb Z/p^n(r))=H^1(R_0,\mathbb Z_p(r))$(同 (4) の逐語)を使うと結論を得る。∎

> ### 系 BR-6′-a($p=7$・$r=3$)
> $\kappa^{(7)}_3$ は $H^1(\mathbb Z[1/7],\mathbb Z_7(3))$ の生成元(補題 BR-5 + 定理 BR-6′)。ゆえに補題 BR-5′ より $\kappa^{(7)}_3(\sigma)\in\mathbb Z_7^\times$ なる $\sigma\in G_{\mathbb Q(\mu_{7^\infty})}$ が存在する。
> ⟹ v1 §7 定理 BH-BRIDGE の証明の第 1・2 段(「補題 BR-5 より全射、補題 BR-6 より $\kappa^{(7)}_3$ も全射」)は**そのまま立つ**。

### 3.7 v1 §6.3 の 2 つの「逐語確認点」の決着

| v1 の未確認点 | v1.1 での決着 |
|---|---|
| corestriction の向き($\sum\tau_a$ か $\sum\tau_a^{-1}$ か) | **消滅**。補題 B が $\mathrm{Res}\circ\mathrm{Cor}=\sum_{a\in G_n}(\tau_a)_*$ を与え、和は群全体を走るので $\sum\tau_a=\sum\tau_a^{-1}$(cert (K3))。**向きは判定に影響しない**(Sol F109-2.3 と同結論・こちらは理由まで確定) |
| $\langle a^{m-1}\rangle$ の最小正代表 | **消滅**。補題 D (D1)(cert (K1)(K2)(K7)) |
| (v1 に無かった第 3 点)符号 $\zeta^a-1$ vs $1-\zeta^a$ | 補題 D (D2)。しかも $r$ 奇のとき $S$ は偶数で**そもそも符号は立たない**(cert (N2)) |
| (v1 に無かった第 4 点)$\chi^{1-m}$ 捻り因子 | 補題 E。$\sigma\in G_S(K_n)$ で $\chi^{1-r}\equiv1\pmod{p^n}$ ゆえ消える |

⟹ **【BR-GAP-1】は CLOSED**(格: paper-proof + 整数検算 cert。`cross-checked` にも `verified` にも**昇格しない**)。

> ★ **【文献要請 BH-L2】(C1 = Ichimura–Sakaguchi)の扱い**: 本節が自前で閉じたので、**BH-L2 は blocker から「任意の第三照合先」へ降格**する。取得できれば §3 の独立確認になるが、**発効には不要**。(v1 §9.2 の起票はこの降格を添えて有効のまま。)

### 3.8 機械検算(**cert 化・手写しゼロ**)

- cert = `search/certs/brgap1_kummer_20260806.json`(schema `brgap1-kummer/v1`)
  - SHA-256 = `6531945c4ded5be34b44dd15c08641d8cfe30dbe7ad8365cc8c5b04722d3121b`
- script = `scratchpad/brgap1_kummer_check.py`
  - SHA-256 = `04303f80e3c4ba4e470587d518372180796a93d5fc9be7641110fb644d2980a9`
- **判定行 75 / PASS 75 / FAIL 0**(`results.all_pass = true`)。厳密整数演算のみ(浮動小数点なし)。
- 宇宙(事前固定): $r=3$;$p\in\{7\ (\text{主}),5,11,13\ (\text{対照})\}$;$n\in\{1,2,3\}$;(K7) の厳密環計算は $(p,n)\in\{(5,1),(7,1),(11,1),(13,1),(5,2)\}$。

| cert 行 | 検証した命題 | 本文の対応 |
|---|---|---|
| (K1) | $\langle a^{r-1}\rangle\equiv a^{r-1}\pmod{p^n}$(全単元) | 補題 D (D1) |
| (K2) | $d_a=(\langle a^{r-1}\rangle-a^{r-1})/p^n$ は整数かつ $\le0$ | 補題 D (D1) |
| (K3) | $\{a^{-1}\}=\{a\}$ かつ $\sum\tau_a$ と $\sum\tau_a^{-1}$ の指数関数が一致 | 補題 B の系(向き無関係) |
| (K4) | $p^n$ 奇 ⟹ $-1=(-1)^{p^n}$;$S=\sum\langle a^{r-1}\rangle$ の値 | 補題 D (D2) |
| (K5) | $(p-1)\nmid r$ ⟹ $\Delta$ の生成元 $g$ で $g^r-1$ が $\bmod\ p$ 単元 ⟹ $(\mathbb Z/p^n(r))^\Delta=0$ | 補題 A |
| (K6) | $p^{r-1}-1\in\mathbb Z_p^\times$($p=7$: $48\equiv6$) | 定理 BR-6′ の $\kappa^*$ 換算 |
| **(K7)** | ★ $\mathbb Z[x]/(\Phi_{p^n})$ の**厳密等式** $\prod_a(z^a-1)^{\langle a^2\rangle}\cdot\prod_a(1-z^a)^{p^n(-d_a)}=(-1)^S\prod_a(1-z^a)^{a^2}$ | 補題 D 全体 |
| **(N1)–(N6)** | ★ **負制御 6 本**(識別力の機械確認): 法を $p^{n+1}$ にすると (K1) は破れる / $r$ 奇の対称性で $S$ 偶 / $r'=6\equiv0\ (p-1)$ では (K5) の判定が逆転 / (K7) は指数 1 個・$d_a$ 1 個・大域符号のいずれを摂動しても破れる | 検算が恒真でないことの確認(Sol F109-4 条件 2 の趣旨) |

⚠ **検算の限界(正直な申告)**: これは **1 系統の python** であり `cross-checked` ではない。cert が押さえているのは**算術の帳簿(指数・符号・単元性・厳密環等式)だけ**であり、**コホモロジーの段(補題 A・B・C・E)は紙の証明**である。

### 3.9 ★ 残す申告(**証明が使った「教科書事実」の一覧**)

外部文献を新たに漁らずに済ませるため、以下は**標準的な副有限群コホモロジー/Kummer 理論の事実**として使った(いずれも当工房の正典・配達済み文献には明示の pin がない):

1. inflation–restriction 完全列(補題 A・BR-5′)。
2. $\lvert\Delta\rvert$ が $p$ と互いに素なら $H^i(G,M)=H^i(G/\Delta,M^\Delta)$($M$ は $p$ 群)(補題 A・BR-5′)。
3. $\mathrm{Res}\circ\mathrm{Cor}=\sum_{g\in G/H}g_*$($H$ 正規)(補題 B・§3.2 に自己完結の証明を付した)。
4. Kummer 写像 $R^\times/(R^\times)^{p^n}\hookrightarrow H^1(R,\mu_{p^n})$ の $G$-同変性(補題 C・E)。

> これらは**予想ではなく教科書事実**であり、§3.2 のように短い自前証明を付けられる。**Lean 化の際はこの 4 点が公理化対象**になる(memory: lean-axiom-policy)。

---

## 4. 修文後の格付け表(v1 §7.3 との差分のみ)

| 対象 | v1 の格 | **v1.1 の格** |
|---|---|---|
| 補題 **BR-5** | paper-proof([KUR] の 4 定理の合成) | **paper-proof**([KUR] の **5 言明**の合成 = Cor 3.8 / Cor 1.5 / §5 / Prop 5.1 / **Rem 5.2**)。★ 等号の出所は BK [2] (6.8)(6.9)(未保持・§1.4)。Sol F109-2.2 により**修文後 PASS** |
| **BR-5′**(新設) | — | **paper-proof**(生成 ⟹ 全射。$\mathrm{Res}$ 同型は [KUR] Rem 4.3 逐語と自前証明の二重) |
| 補題 **BR-6** ⟶ 定理 **BR-6′** | ⚠ paper-proof candidate(スケッチ)= 【BR-GAP-1】 | ★ **paper-proof(CLOSED)**。有限段 Kummer 比較(§3)+ cert `brgap1_kummer_20260806`(75/75)。逐語確認 2 点は**消滅** |
| **【BR-GAP-1】** | 唯一の真の残余 | ★ **閉**(残余ギャップ **0 個**) |
| 【BR-GAP-2】(生成対同一視) | 軽微 | **CLOSED**(Sol F109-2.5: 正典の同一 splitting pin により。★ **v1 の $\tau$ 型排除論法は不採用** — 自由副有限群の中心化群と交換子部分群の交叉に関する補題を省いていた。正しい根拠は [2405] printed 2/4 と [ICM] printed 114 が**同じ座標を採用している**という source pin) |
| 【BR-GAP-3】([C2] cert 単系統) | 測定依存 | **不変**(measurement-relative のまま) |
| 【BR-GAP-4】(ICM §6.3 の Theorem は引用) | 再導出予定なし | **不変** |
| 定理 **BH-BRIDGE** | paper-proof candidate(【BR-GAP-1】相対) | ★ **paper-proof(前件相対 PASS)**。前件 = §1.6 の差し替え済み表 + [C2] 測定。Sol F109-6: **前件相対 PASS**(C2 測定依存・not cross-checked / not verified) |
| 補題 **BR-3** | paper-proof candidate | **paper-proof PASS**(Sol F109-2.1。一般の $f$ に対する紙の証明を Sol が再導出し一致) |
| 「三重裏取り」の呼称 | 独立の三証明のように読める | ★ **不採用**。正しい呼称は「**識別力を持つ consistency checks**」(Sol F109-1.4)。J1′ は Galois 像の非消滅を測っておらず、Rem 4.3 と ICM §6.3 は IKY/Coleman 系の同じ定理群に由来する |
| `cross-checked` / `verified` | ✗ | ✗(**不変**) |
| novelty | 主張しない | **主張しない**(不変) |

---

## 5. ★★ 狭形言明カード **BH-α-pent v1.1**(**versioned 記帳**)

> **発効ステータス: 司令塔裁定待ち**(裁定 582 =「修文後に狭形発効(次便)」)。本カードは発効文言の**確定稿**であり、数学者側の記帳である。

### 5.1 発効してよい言明(**これだけ**)

> ### **BH-α-pent**(**$\mathrm{PENT}_W$ フィルタの算術飽和**)
> 窓 $\mathbf N=$ **NW(7)** において
> $$\boxed{\ \mathfrak G_{\rm ar}(\mathbf N)\ =\ \mathfrak G_{\rm pent}(\mathbf N)\ =\ H_W,\qquad \lvert H_W\rvert=42 .\ }$$
> すなわち **$\mathrm{PENT}_W$-PASS 集合の中の非算術 shadow は 0 個**である。

**格札(この文字列をそのまま使う — Sol F109-3.1 指定)**:
```
framework-relative + measurement-relative candidate
(paper bridge audited; numerical predicates not cross-checked; Lean not used)
```

**成立の理由(1 行)**: 定義上の鎖 $\mathfrak G_{\rm ar}\subseteq\mathfrak G_{\rm pent}\subseteq\mathfrak G_{\rm gen}\subseteq\mathrm{GT}(\mathbf N)$ と HSP-SOUND の $\mathfrak G_{\rm pent}\subseteq H_W$、および BH-1 の二値 + 定理 BH-BRIDGE(修文後)による $\mathfrak G_{\rm ar}=H_W$ の sandwich。

**前件(すべて明示)**:
| # | 前件 |
|---|---|
| (α) | [2405] §1.3 の Ihara 埋め込み (1.5)(1.6)(1.11)–(1.13) |
| (β) | [ICM] §6.1 / 6.3 / 6.4 の 4 式(v1 §4.1) |
| (γ) | [KUR] Cor 3.8 / Cor 1.5 / §5 / **Prop 5.1 + Remark 5.2**(§1.6 で差し替え済) |
| (δ) | ~~補題 BR-6【BR-GAP-1】~~ ⟶ **定理 BR-6′(CLOSED・§3)** |
| (ε) | [C2] cert の測定 $\lvert P\rvert=7^8$・LCS $[2,1,2,3]$(**単系統 = 【BR-GAP-3】**) |
| (ζ) | 補題 BR-1 の規約整合(正典の同一 splitting pin・【BR-GAP-2】CLOSED) |
| (η) | BH-1 の二値・HSP-SOUND・SUP-4・BH-4([PRE]) |
| (θ) | scoring / J0–J2 の測定値(**single-lane candidate**・Sol F109-4) |

**副次的帰結(Sol F109-3.1 による v1 §8.1 の訂正)**:
> v1 §8.1 は [PRE] §6.5 (1)「42 個が genuine とは言えない」を継承していたが、**これは filter だけを見ていた段階の警告**である。$\mathfrak G_{\rm ar}=H_W$ の等号が発効した後は、42 個は**算術的であり、算術的なら genuine でもある**。⟹ **等号発効後の 42 個は arithmetic かつ genuine**。

### 5.2 ★ 書いてはいけない言明(**発効不可・UNKNOWN 維持**)

| 言明 | 判定 | 理由 |
|---|---|---|
| 「NW(7) の**非算術証人ゼロ**」 | ❌ **不採択** | $\mathfrak G_{\rm gen}\subseteq H_W$ がどこにもない。$\mathrm{PENT}_W$ は $\widehat{GT}$ の pentagon の必要条件であって、pentagon を課さない $\widehat{GT}_{\rm gen}$ の必要条件ではない |
| 「**FAKE-VOID**」 | ❌ **不採択** | 同上 |
| 「**初の窓レベル完全検証**」 | ❌ **不採択** | 数学内容も未閉鎖、かつ「**検証(verified)**」は Lean に予約 |
| 「**P5 決着**」 | ❌ **不採択** | 上記の理由により窓レベルでも閉じていない |
| $\mathfrak G_{\rm gen}(\mathbf N)=\mathfrak G_{\rm ar}(\mathbf N)$ | ❌ **UNKNOWN** | — |
| $\mathrm{GT}(\mathbf N)\setminus\mathfrak G_{\rm gen}(\mathbf N)=\varnothing$ | ❌ **UNKNOWN** | — |

**確定しているのは次の 1 本だけ**: $\mathfrak G_{\rm pent}\setminus\mathfrak G_{\rm ar}=\varnothing$。

### 5.3 残る 252 個 — **正確な式と UNKNOWN の明記**

$$\mathrm{GT}(\mathbf N)\setminus H_W=\bigl(\mathfrak G_{\rm gen}\setminus H_W\bigr)\ \sqcup\ \bigl(\mathrm{GT}(\mathbf N)\setminus\mathfrak G_{\rm gen}\bigr),$$
$$\boxed{\ 252\ =\ \#\{\text{genuine だが非算術}\}\ +\ \#\{\text{fake}\},\qquad \textbf{この二項の内訳は UNKNOWN}.\ }$$

**呼称(Sol F109-5 により改名は必須)**:
| 廃止 | 正 |
|---|---|
| ~~「A 型 fake 候補 252」~~ | **「$\mathrm{PENT}_W$-FAIL 非算術 shadow 252 個」** または **「$\mathrm{PENT}_W$ 排除集合 $\mathrm{GT}(\mathbf N)\setminus H_W$」** |
| ~~「$\mathrm{PENT}_W$ 偽 = pentagon-fake の有限証明書」~~(HSP-SOUND §1.3) | **「$\widehat{GT}$-lift 不存在の有限証明書」** |
| ~~`TRUNC 余剰候補`~~(本窓では非推奨・既存 $\mathrm{TRUNC}^{B_4}$ と衝突) | 一般語が要るときのみ「有限段余剰候補」 |

**252 個について確定していること**: 全て**非算術**である。各元が genuine か fake かは **UNKNOWN**。

### 5.4 記帳案(**司令塔が `provenance/CLAIMS.md` へ貼るための確定文**)

```
### BH-α-pent(PENT_W フィルタの算術飽和・NW(7))
- 主張: 𝔊_ar(N) = 𝔊_pent(N) = H_W、|H_W| = 42。ゆえに PENT_W-PASS 集合内の非算術 shadow は 0。
  等号発効後の 42 個は arithmetic かつ genuine。
- 格: framework-relative + measurement-relative candidate
  (paper bridge audited; numerical predicates not cross-checked; Lean not used)
- 根拠: docs/notes/bhunt_l1_bridge_v1.md + docs/notes/bhunt_l1_bridge_v1_1_erratum.md(修文 2 点)、
  docs/notes/bhunt_prereg_iffirst_v1.md(BH-1/BH-4/SUP-4)、
  search/certs/{nw7_mainrun_scoring_20260806, bhunt_j0j2_20260806, bhbridge_foxcheck_20260806,
  brgap1_kummer_20260806}.json、papers/kurihara-1992-compositio-cyclotomic-Kgroups.pdf
  (sha256 70ee5919eae904197bf5949e9a8af2b45a805d31e2976241217be329360becca)。
- ★ 書かない: 「非算術証人ゼロ」「FAKE-VOID」「初の窓レベル完全検証」「P5 決着」= すべて不採択。
- UNKNOWN: 252 = #{genuine だが非算術} + #{fake}(内訳不明)。𝔊_gen ⊆ H_W は成立していない。
- 呼称: 残り 252 は「PENT_W-FAIL 非算術 shadow」(「A 型 fake 候補」は廃止)。
- 出所: Sol 便 109 返書 F109-2.2/2.3/3.1/3.2/4/5(分割 PASS)+ 裁定 582。
```

---

## 6. 規律申告

- ★ **新規の窓計算ゼロ。** GAP も pc 群も起動していない。機械は §3.8 の python(整数・整数係数多項式)のみで、**42 個の candidate key の値は 1 個も読んでいない**。cert から参照した構造欄も**なし**(本 addendum は [C2] も [J0J2] も新たに読んでいない — §5.1 の前件表は v1 の記載を引き写しただけ)。
- **検算は cert 化した**(`brgap1_kummer_20260806`・75/75 PASS・**負制御 6 本つき**)。本文の数値・ハッシュはすべて機械生成物からのコピーで、**手写しゼロ**。
- **封印 3 量非接触**($n=5$ 系・$\mathrm{Im}\,R$・$d_N$・genuine 層の $u$ 値・PSL 量・$\varepsilon$ bits)。本 addendum の $\kappa,\kappa^*,c(1),C,\varepsilon_{r,n},d_a,S$ はすべて数論側の記号。⚠ **$\varepsilon_{r,n}$ は Ihara の円分単数であり「$\varepsilon$ bits」とは無関係**(規約台帳 §1.3.10 の分離を遵守)。
- **文献**: **新規の外部文献探索はゼロ**。使ったのは既収蔵の [KUR](司令塔が裁定 578 で降ろした 1 本)の印字 226 / 230 / 231 / 233 / 236 と [ICM](既在の正典)の印字 115 の**頁画像**のみ。**C1(Ichimura–Sakaguchi)は依然未入手であり、載荷根拠に数えていない**(§3 は C1 なしで閉じた)。新たに **【文献要請 BH-L3】**(BK (6.8)(6.9) の言明 pin・**非 blocker**)を起票し、**【文献要請 BH-L2】**(C1)を blocker から任意の第三照合先へ**降格**した。
- **既存文書は 1 バイトも改変していない**(`bhunt_l1_bridge_v1.md` = `dd2dac0d…`・`bhunt_prereg_iffirst_v1.md` = `578815ad…` を起草時に再計算して一致確認)。修文はすべて本 addendum に書き、v1 の該当箇所は §1.1 と §4 の表で**差分として指し示す**形にした。
- **原文引用**はすべて 220–300 dpi の頁画像で照合(OCR テキストは補助のみ)。
- **格の申告**: 本 addendum の結論はすべて **paper-proof**。`cross-checked` にも `verified` にも昇格しない。**novelty は主張しない**(内容は [KUR]・[ICM] の既知定理 + 標準的なコホモロジー操作の合成)。

---

## 7. 付録 — 本 addendum で使った逐語引用の頁 pin(v1 付録 B への追加分)

| # | 出所 | 頁 | 内容 | 画像 |
|---|---|---|---|---|
| C-1 | [KUR] | 印字 233 | ★ **§5 (4) の $c(\eta)$ 定義全文**($\eta_n=(1-\zeta_{p^n}\eta^{1/p^n})\otimes\zeta_{p^n}^{\otimes(r-1)}$・$\mathrm{Cor}$ の域と余域)/ $H^1\cong\mathbb Z_p$ の段 / **PROPOSITION 5.1**(不等号の向き)/ **REMARK 5.2**(「実は等号」+ 出所 [2] (6.8)(6.9)+「IMC を使わない」の但し書き) | `scratchpad/bhbridge_img/kuri_p233-12.png` |
| C-2 | [KUR] | 印字 231 | **PROPOSITION 4.2**(全射性)/ **REMARK 4.3** 全文(★ $H^1(\mathbb Z[1/p,\mu_{p^\infty}],\mathbb Z_p(3))^{G_\infty}\simeq H^1(\mathbb Z[1/p],\mathbb Z_p(3))$ の同型・「surjectivity ⟺ generates」・[8] Th. B / [3] Th. C) | `scratchpad/bhbridge_img/kuri-10.png` |
| C-3 | [KUR] | 印字 230 | **COROLLARY 3.8**($A^{[p-3]}=0$ が奇素数で無条件・[11] Lee–Szczarba) | `scratchpad/bhbridge_img/kuri_p230-09.png` |
| C-4 | [KUR] | 印字 226 | **COROLLARY 1.5**($r\ge2$)+ ★ **$A^{[k]}$ = $\omega^k$-固有空間**の定義(添字が $\bmod\ (p-1)$ で定まることの根拠) | `scratchpad/bhbridge_img/kuri_p226-05.png` |
| C-5 | [KUR] | 印字 236 | 参考文献 **[2] = Bloch–Kato**(Grothendieck Festschrift I, Progress in Math. 86, 333–400)・**[3] = Coleman** ASPM 17 (1989) 55–72・**[7] = Ihara** Ann. Math. 123 (1986) 43–106・**[8] = Ihara–Kaneko–Yukinari** ASPM 12 (1987) 65–86・**[11] = Lee–Szczarba** | pdftotext(頁 15) |
| C-6 | [ICM] | 印字 115(PDF 203) | ★ §6.2 (ii) 全文: $\zeta_n=\exp(2\pi i/l^n)$(**整合系**)・$\varepsilon_{m,n}=\prod_a(\zeta_n^a-1)^{\langle a^{m-1}\rangle}$・積の範囲($0<a<l^n$, $(a,l)=1$)・$\langle\cdot\rangle$ の定義・**totally positive** と正実根の規約・$\varepsilon_{m,n+1}/\varepsilon_{m,n}$ が $l^n$ 乗(**整合性**)・定義式(**$n\ge2$ で成立**)・(6.2.1)・「factors through $\mathrm{Gal}(\mathbb Q(\mu_{l^\infty})^{\rm ab}/\mathbb Q)$」・Soulé 非消滅 / §6.3 の $\kappa^*_m=((l^{m-1}-1)^{-1}\kappa^{(l)}_m)_l$ | `scratchpad/bhbridge_img/ihara_p115-203.png` |

> ★ **[ICM] 印字 115 の小さな異物(記録のみ)**: Ihara は「$\kappa^*_m(\sigma)\in\widehat{\mathbb Z}^\times=\prod_l\mathbb Z_l^\times$」と書くが、$\kappa^{(l)}_m(\sigma)$ が単元とは限らないので、これは $\widehat{\mathbb Z}=\prod_l\mathbb Z_l$ の誤植と読むのが自然である。**本 addendum の使い方($\kappa^*_3=(p^2-1)^{-1}\kappa^{(p)}_3$ という $\mathbb Z_p$ 内の等式)には影響しない。**
