# 【SS-GAP-1】$\lvert GT(N')\rvert$ 計数の実行設計(Sol 計算レーン仕様書)— 裁定 1089

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔裁定 1089(便 122 積荷)
前提 = `set_surgery_vetting_v1.md` §1(定理 TORSOR)・§3(類公式)・§4(上界式)
宛先 = **Sol 計算レーン**(裁定 1024: 高難度実装は最初から Sol)
⚠ $u$/$c$ 非接触・封印非接触・prereg 非抵触・**算術入力ゼロ(純群論)**。**格: candidate**(Sol 未監査)。

---

## §0 ★★★ 結論を先に — 装置は**クラウド級から秒級へ落ちました**

検分 v1 の時点では「$\tilde H$($6.5\times10^{17}$)の共役類 $\approx5\times10^5$ 本とべき写像を構造論で書き下せるか」が壁でした(【SS-GAP-1】)。
本 spec でその壁は**消えます**。理由は 1 行:

$$\boxed{\ c\in N'\ \Longrightarrow\ \textbf{全ての }K\in\mathcal C(N')\ \textbf{が }c\ \textbf{を含む}\ \Longrightarrow\ \textbf{計数は }B_3\ \textbf{でなく }\mathrm{PSL}(2,\mathbf Z)=\mathbf Z/2*\mathbf Z/3\ \textbf{上で行える}\ }$$

自由積ゆえ $\#\mathrm{Hom}(\mathbf Z/2*\mathbf Z/3,H)=i_2(H)\cdot i_3(H)$ — **共役類も指標もべき写像も要りません**。要るのは
$$i_2^T:=\#\{A\in\tilde H: A^2=1,\ p(A)\in T\},\qquad i_3^R:=\#\{B\in\tilde H: B^3=1,\ p(B)\in R\}$$
の 2 つの整数だけ($p:\tilde H\twoheadrightarrow S_3$、$T$=互換、$R$=3-巡回)。

$$\boxed{\ \bigl\lvert GT(N')\bigr\rvert\ \le\ \bigl\lvert GT^{\rm settled}(N')\bigr\rvert\cdot\frac{i_2^T\cdot i_3^R\cdot\lvert Z(\tilde H)\rvert}{\lvert\tilde H\rvert}\ =\ \frac{2\,i_2^T\,i_3^R\,\lvert Z(\tilde H)\rvert}{\lvert\tilde H\rvert}\ }$$

⚠ **粗い見積り(§5.1・外挿ラベルつき)では右辺は $10^5$–$10^6$ 級** ⟹ 既知下界 $30{,}360$ と無矛盾で、**$N'$ は「規模で詰んだ窓」ではなく GAP の射程内**という 1 ビットが出ます。

---

## §1 ★★ 定理 COUNT-PSL

> **【定理 COUNT-PSL】** $N\in\mathrm{NFI}_{PB_3}(B_3)$ が $c\in N$ を満たすとする。このとき
> **(i)** 全ての $K\in\mathcal C(N)$ は $c$ を含む。
> **(ii)** $\displaystyle\#\mathcal C(N)\ \le\ \#\bigl\{\bar K\lhd\mathrm{PSL}(2,\mathbf Z)\ :\ \bar K\le\overline{PB_3},\ \mathrm{PSL}(2,\mathbf Z)/\bar K\cong B_3/N\bigr\}\ =\ \frac{\#\mathrm{Epi}^{\rm mk}\bigl(\mathbf Z/2*\mathbf Z/3,\ \tilde H\bigr)}{\lvert\mathrm{Aut}(\tilde H)\rvert}$
> **(iii)** $\#\mathrm{Hom}^{\rm mk}\bigl(\mathbf Z/2*\mathbf Z/3,\tilde H\bigr)=i_2^T\cdot i_3^R$。

**証明**:
(i) $K=\ker T_{m,f}$ で $T_{m,f}(c)=c^{2m+1}N$。$c\in N$ ⟹ $T(c)=1$ ⟹ $c\in K$ ✔
(ii) Prop 3.8($GTSh(K,N)\ne\emptyset\Rightarrow B_3/K\cong B_3/N=\tilde H$)+ (i) + 便 121 A7.1($K\le PB_3$)。$\langle c\rangle=Z(B_3)$ の正規閉包で割ると $B_3/\langle c\rangle=\langle a,b\mid a^2=b^3=1\rangle=\mathbf Z/2*\mathbf Z/3=\mathrm{PSL}(2,\mathbf Z)$($a=\Delta,\ b=\delta$・`照合_B3表示_T2土台` (D2)(D3) で $a^2=b^3=c$)。核の数 = Epi 数 / $\lvert\mathrm{Aut}\rvert$ ✔
(iii) 自由積の普遍性: $\mathrm{Hom}(\mathbf Z/2*\mathbf Z/3,H)=\{(A,B):A^2=1,B^3=1\}$。$\ker\subseteq PB_3$ の条件は $p(A)\in T$ かつ $p(B)\in R$(互換と 3-巡回は $S_3$ を生成するので、これだけで $p\circ\varphi=\pi_{S_3}$ が $\mathrm{Aut}(S_3)$ を除いて従う)⟹ 独立に数えられ積になる ✔ ∎

$$\boxed{\ \textbf{★ 発案係の指標和}(10^{11})\ \to\ \textbf{私の類公式}(10^{5\text{–}6})\ \to\ \textbf{本定理}(\textbf{整数 2 個})\ }$$

⚠ **適用範囲**: $c\in N$ の窓のみ。$N'$ は $c\in N'$(`settled_grp_proof` §5.1)✔ $K^{(n)}$ 族も $c\in K^{(n)}$(定義ノート §3: $\psi_n(c)=(1,1,1)$)✔ **83 窓は $c\notin N$ ⟹ 適用外**(そこは検分 §3.2 の類公式を使う)。

---

## §2 上界式(最終形)

$\lvert\mathrm{Aut}(\tilde H)\rvert\ge\lvert\mathrm{Inn}(\tilde H)\rvert=\lvert\tilde H\rvert/\lvert Z(\tilde H)\rvert$ と $\#\mathrm{Epi}\le\#\mathrm{Hom}$ より

$$\boxed{\ \#\mathcal C(N')\ \le\ \frac{i_2^T\cdot i_3^R\cdot\lvert Z(\tilde H)\rvert}{\lvert\tilde H\rvert},\qquad \bigl\lvert GT(N')\bigr\rvert=2\cdot\#\mathcal C(N')\ \le\ \frac{2\,i_2^T\,i_3^R\,\lvert Z(\tilde H)\rvert}{\lvert\tilde H\rvert}\ }$$

($\lvert GT^{\rm settled}(N')\rvert=2$ は cert `e41191d6` の全数確定値。)
★ **精密化したければ** $\lvert\mathrm{Aut}(\tilde H)\rvert$ を実測(Stage 3)し、Möbius で $\#\mathrm{Epi}$ に落とす(Stage 4)。**1 ビットには不要**。

---

## §3 Stage 1 — $\tilde H$ の構造確定(入力の所在)

**入力**: `docs/notes/q3r1_lift_spec_v1.md` §3–4 の**実測値**(mod $691^2$)— $\bar x,\bar y,\bar\sigma_1,\bar\sigma_2$ の明示行列。
既知(再導出せず引用してよい): $\lvert\tilde H\rvert\approx6.5\times10^{17}$・$Q:=F_2N'/N'$・$\mathrm{ord}(\bar x)=\mathrm{ord}(\bar y)=47679=3\cdot23\cdot691$・$C_Q(\bar y)\cong(\mathbf Z/691^2)^\times$(位数 476,790)・$\mathrm{Aut}(Q)\cong PGL(2,\mathbf Z/691^2)$。

```
[S1-1] a_0 := σ̄_1σ̄_2σ̄_1 (=Δ の像) , b_0 := σ̄_1σ̄_2 (=δ の像) を明示構成
       ★ 検算: c ∈ N' ⟹ a_0^2 = b_0^3 = 1 を確認(これが定理 COUNT-PSL の入口)
          ⟹ 破れたら c ∈ N' の同定が誤り ⟹ 即停止
[S1-2] Q = ⟨σ̄_1^2, σ̄_2^2⟩ の同定: |Q| = |H̃|/6 か / Q ≅ SL(2,Z/691^2) か
       ★ 検算: |SL(2,Z/p^2)| = p^4(p^2-1) = 691^4·477480 = 1.0886e17 , ×6 = 6.53e17
[S1-3] p : H̃ ↠ S_3 の明示(= B_3 ↠ S_3 の像)。T, R の逆像コセットを名指し
[S1-4] Z(H̃) の決定(位数だけでよい)
[S1-5] H̃ が行列群として実現できるか(GL(2,Z/691^2) の部分群 or 拡大)を判定
       ⟹ YES なら §4 の閉形式が使える / NO なら §4-alt(コセット走査の構造版)
出力: cert (schema ssg1_structure/v1)。生値のみ。
```

⚠ **落とし穴**: $\mathrm{Aut}(Q)\cong PGL(2,\mathbf Z/p^2)$ の位数は $p^4(p^2-1)=\lvert Q\rvert$ なので、$\tilde H\to\mathrm{Aut}(Q)$ は**単射になり得ません**($6\lvert Q\rvert/\lvert C_{\tilde H}(Q)\rvert\le\lvert Q\rvert$ ⟹ $\lvert C_{\tilde H}(Q)\rvert\ge6$)。⟹ **$S_3$ の一部は $Q$ に自明に作用する** ⟹ $\tilde H$ は単純な半直積ではありません。**[S1-4][S1-5] で正確に決めること**(私の紙では決められません)【SSG1-GAP-1】。

---

## §4 Stage 2 — $i_2^T$ と $i_3^R$ の計数

### 4.1 ★ 行列で書ける場合の閉形式(Cayley–Hamilton)

$2\times2$ 行列 $A$($\mathbf Z/p^2$ 上)について C–H は $A^2=\mathrm{tr}(A)A-\det(A)I$。

- **$A^2=1$**: $\mathrm{tr}(A)A=(1+\det A)I$。$A$ が非スカラーなら $A,I$ が一次独立 ⟹
$$\boxed{\ A^2=1\ (A\ \text{非スカラー})\iff \mathrm{tr}(A)=0\ \wedge\ \det(A)=-1\ }$$
- **$B^3=1$**: $B^3=(\mathrm{tr}^2-\det)B-\mathrm{tr}\cdot\det\cdot I$。非スカラーなら
$$\boxed{\ B^3=1\iff \mathrm{tr}(B)^2=\det(B)\ \wedge\ \mathrm{tr}(B)\det(B)=-1\ }$$
 ⟹ $\mathrm{tr}^3=-1$ かつ $\det=\mathrm{tr}^2$($\mathrm{tr}$ は $-1$ の 3 乗根)。
- スカラー解は別途($A=\pm I$、$B=\omega I$ で $\omega^3=1$)。

⟹ **計数は「与えられた $(\mathrm{tr},\det)$ をもつ行列の個数」の総和**に落ちます。これは $\mathbf Z/p^2$ 上の初等的な数え上げ($\mathrm{tr},\det$ を固定した $2\times2$ 行列の個数は $p^2$ の冪と Legendre 記号で閉形式)。
$$\boxed{\ \textbf{計算量: }O(1)\ \textbf{の閉形式 or }O(p^2)\approx5\times10^5\ \textbf{の走査 ⟹ 秒級}\ }$$

⚠ ただし **$T$/$R$ コセット条件**(= $\tilde H$ の中のどのコセットか)を課す必要があり、そこは Stage 1 の構造に依存します。⟹ [S1-5] が YES ならコセットは行列条件(行列式の値・特定部分群への所属)で書けるはず。

### 4.2 §4-alt(行列で書けない場合)

$\{q\in Q: q\,\alpha(q)=1\}$($\alpha=\mathrm{conj}$ by $a_0$)と $\{q: q\,\beta(q)\beta^2(q)=1\}$($\beta=\mathrm{conj}$ by $b_0$)の計数に落とす($a_0^2=b_0^3=1$ を使用)。これは **$\alpha$-捻れ共役類**の言葉で、同梱パッケージ **`twistedconjugacy`** の射程です(CLAUDE.md 棚卸し)。⟹ 規模は $Q$ の構造論次第・**Sol の設計裁量**。

---

## §5 段階設計 — 「どこまでで 1 ビットが取れるか」

### 5.1 ★★ Stage 0(最安・**$p=691$ を触らずに 1 ビット**)

小さい $p$ で $SL(2,\mathbf Z/p^2)$ 型の**上界の $p$-依存性を実測して外挿**する:

```
[S0] p = 3,5,7,11,13 について、Q_p := SL(2,Z/p^2) と「S_3 を上に乗せた模型」で
     i_2^T · i_3^R · |Z| / |H| を *全数列挙* で計算(|SL(2,Z/169)| = 13^4·168 ≈ 4.8e6 まで)
     ⟹ 指数 e を fit: 上界 ≈ const · p^e
     ⟹ p = 691 へ外挿(★ 外挿ラベル必須・W-48)
```
**私の紙の見立て**: $i_2^T,i_3^R\approx\lvert\tilde H\rvert/p^2$ 級(対合・位数 3 元はトレース条件 1 本で切られる)⟹ 上界 $\approx\lvert\tilde H\rvert/p^4\cdot\lvert Z\rvert\approx p^2\cdot\lvert Z\rvert$。
$$\boxed{\ \Longrightarrow\ \bigl\lvert GT(N')\bigr\rvert\ \lesssim\ 2\cdot691^2\cdot\lvert Z(\tilde H)\rvert\ \approx\ 10^6\text{–}10^7\qquad(\textbf{見積り})\ }$$
★ **Stage 0 だけで「$\lessgtr10^7$」の 1 ビットが出ます**(外挿格)。これが便 122 の積荷の最低ライン。

### 5.2 Stage 1–2($p=691$ の実値)

Stage 1(構造)+ Stage 2(閉形式)で **証明された上界**が出ます。⟹ 外挿ラベルが外れる。

### 5.3 Stage 3–4(精密化・任意)

$\lvert\mathrm{Aut}(\tilde H)\rvert$ の実測 / Möbius による $\#\mathrm{Epi}$ 化 / さらに「$\mathcal C(N')$ = 実際に shadow の核になる $K$」への絞り込み。⟹ **上界が実値に近づく**。⚠ 段階 4 は本命ではありません(1 ビットには不要)。

---

## §6 ★ 陽性対照(必須・fail-closed)

| # | 対照 | 予言 | 意味 |
|---|---|---|---|
| **PC-1** | 私の 16 群 3 系統一致の再現(`scratchpad/set_surgery_hom_b3.g`) | 全群で 全数=類公式=指標和 | 装置(第 1 版)の再現 |
| **PC-2** | $\mathbf Z/2*\mathbf Z/3$ 版の較正: 小群 $H$ で $i_2(H)i_3(H)$ と $\#\{(A,B):A^2=B^3=1\}$ の全数一致 | 厳密一致 | ★ **定理 COUNT-PSL (iii) の機械確認** |
| **PC-3** | $K^{(9)}$($c\in K$・isolated・$\lvert GT\rvert=108$・$\#\mathcal C=1$) | 上界 $\ge1$、緩みを実測 | ★ **上界式の緩みの初測定**(Prop 3.8 上界がどれだけ甘いか) |
| **PC-4** | $K^{(3)},K^{(4)},K^{(8)},K^{(12)}$(Thm 4.3 で $\lvert GT\rvert$ 既知) | 上界 $\ge\lvert GT\rvert/\lvert GT^{\rm settled}\rvert=1$ | 族での緩みの傾向 |
| **PC-5** | $SL(2,\mathbf Z/p^2)$($p=3,5,7$)で §4.1 の閉形式 vs 全数列挙 | 厳密一致 | ★ **C–H 閉形式の検証**(これが外れたら §4.1 は使えない) |

$$\boxed{\ \textbf{PC-2 と PC-5 が通らないうちは }p=691\ \textbf{に触らないこと}\ }$$

---

## §7 PARTIAL / checkpoint 設計

```
CP-A  [S1-1] a_0^2 = b_0^3 = 1        ⟹ 破れたら即停止(c ∈ N' の同定が誤り)
CP-B  [S1-2] |Q| = |H̃|/6 と Q ≅ SL(2,Z/691^2)  ⟹ 破れたら即停止(H̃ の同定が誤り)
CP-C  PC-2 / PC-5                      ⟹ 破れたら装置を破棄(数学の誤り)
CP-D  ★ 一致検査: 得た上界 U に対し U ≥ 30,360/2 = 15,180
      (= 円分下界 |a_{N'}| ≥ 30,360 と TORSOR から出る #C(N') の下界)
      ⟹ U < 15,180 なら *矛盾* ⟹ 即停止し、前提 4 つ
         (Prop 3.8 の使い方 / |GT^settled(N')|=2 / 円分下界 / H̃ の同定)を洗い直す
      ★ これは装置の正しさの最強のテストです
CP-E  Stage 0 だけで打ち切ってよい(1 ビットは出る)。Stage 1-2 が重ければ PARTIAL 報告可
```

**PARTIAL の型**: 「Stage 0 完了・外挿で $\lesssim10^{6\text{-}7}$」/「Stage 1 完了・構造確定」/「Stage 2 完了・証明された上界 $U=\dots$」の 3 段。**どの段で止まっても便 122 に載る**形にしてあります。

---

## §8 Sol への受け渡し(スペック要約)

| 項目 | 内容 |
|---|---|
| **目的** | $\lvert GT(N')\rvert$ の**上界**を出す(証明された値、または外挿見積り) |
| **本命の 1 ビット** | $\lvert GT(N')\rvert\lessgtr10^7$(⟹ ③ 線の「計数不能」判定の是非) |
| **入力** | `docs/notes/q3r1_lift_spec_v1.md` §3–4($\bar\sigma_1,\bar\sigma_2$ の mod $691^2$ 実測値)・cert `e41191d6`($\lvert GT^{\rm settled}(N')\rvert=2$)・本 spec |
| **数学の正本** | 定理 COUNT-PSL(§1・私の証明)・上界式(§2)・C–H 閉形式(§4.1) |
| **出力** | cert(schema `ssg1_count/v1`)。生値のみ・判定は司令塔。必須欄: $i_2^T,i_3^R,\lvert Z(\tilde H)\rvert,\lvert\tilde H\rvert$, 上界 $U$, CP-A〜E の可否, Stage 到達段 |
| **禁止** | $u$/$c$ の値に触れること・封印 3 量($K^{(5)}$ インスタンス)・prereg 量($d_9$, $r$)の計算 |
| **受け入れ条件** | PC-2 と PC-5 が PASS・CP-A〜D が PASS・上界 $U$ とその導出過程が cert に生値で入っていること |
| **規模見込み** | Stage 0: 分級 / Stage 1: 分〜時級(構造同定が主) / Stage 2: 秒〜分級(閉形式が立てば) |

⚠ **Sol への注意 2 点**:
1. **$\tilde H$ を列挙しないこと**。$6.5\times10^{17}$ です。すべてトレース・行列式・コセットの条件で数えます。
2. §3 の落とし穴(**$S_3$ の一部が $Q$ に自明に作用する**)を先に片付けること【SSG1-GAP-1】。ここを飛ばすと $i_2^T,i_3^R$ のコセット条件が書けません。

---

## §9 記帳

- ★ **本 spec の新規部分**: ① **定理 COUNT-PSL**($c\in N$ 窓で計数が $\mathbf Z/2*\mathbf Z/3$ 上に落ち、$\#\mathrm{Hom}^{\rm mk}=i_2^T\cdot i_3^R$ という**整数 2 個**になる)② C–H による対合・位数 3 元の**閉形式判定**($\mathrm{tr}=0\wedge\det=-1$ / $\mathrm{tr}^3=-1\wedge\det=\mathrm{tr}^2$)③ **Stage 0**($p$ を触らずに小 $p$ の外挿で 1 ビット)④ **CP-D 一致検査**(円分下界 $15{,}180$ との突合が装置の最強テスト)⑤ $\tilde H\to\mathrm{Aut}(Q)$ が単射でないことの位数勘定による摘出。
- **【SSG1-GAP-1】(中・新)** $\tilde H$ の拡大型($S_3$ のどの部分が $Q$ に自明に作用するか・$Z(\tilde H)$)。私の紙では決まりません ⟹ Stage 1 の主対象。
- **【SS-GAP-1】★ 実質縮小**: 「$\tilde H$ の共役類 $5\times10^5$ 本を構造論で書き下す」は**不要になりました**(定理 COUNT-PSL)。残るのは Stage 1 の構造同定のみ。
- ⚠ **適用範囲の明記**: 定理 COUNT-PSL は $c\in N$ 窓限定。83 窓($c\notin N$)には検分 §3.2 の類公式を使うこと(そちらも $O(\#\text{classes})$ で軽い)。
- **申告**: 紙のみ(本 spec の機械走行はゼロ)。第 I 部 §4.1 の 16 群計算は `scratchpad/set_surgery_hom_b3.g`。$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
