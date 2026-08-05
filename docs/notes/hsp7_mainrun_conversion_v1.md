# HS 本走 — 設計ギャップ 2 件の解消(P→Q 変換 / pcgs→語コスト)v1

**起草**: 数学者(Opus 5)/ **日付**: 2026-08-05 / **委嘱**: 司令塔(裁定 524・便 105 本走再申請に同梱)
**対象**: `hsp7_mainrun_prereg_v2.md` §8 未解決 2 と 3(`lane_wrapper_P.g` / `lane_wrapper_V.g` の `OPEN_ITEM`)
**範囲**: 構成と証明+コスト上界のみ。実装はしていない。TOY 窓での検証計算のみ実行(下記)。
**前提の確認**: 主走の窓対は §8.7 の **verbal** 対 `N_F₂ := γ₅(F₂)F₂^p`, `W := γ₅(K(0,5))K(0,5)^p`(p=7)。候補鍵は `Pcgs([P,P])` の指数ベクトル (e₁..e₆) ∈ {0..6}⁶、正規形 `g₁^{e₁}···g₆^{e₆}`(左→右)。

---

## 0. 結論

| | 判定 |
|---|---|
| **ギャップ①(Lane P: P→Q 変換)** | **解消**。変換は **6 元の前計算 + 6 冪の積**。well-defined は **verbal 性から自動**、さらに **j̄ は単射**(新補題 CONV-INJ)。語展開は不要 |
| **ギャップ②(Lane V: pcgs→語コスト)** | **解消(かつ回避可能)**。修理 A の語長上界は $\lvert f\rvert_{x,y}\le 452$、rate 補正 **≈ ×1.0(補正不要)**。さらに **closed form(下記 CF)で語展開そのものが消える** — TOY で literal と完全一致を確認済み |

**★ 本票の主産物**: full hexagon の **閉形式判定式 CF**。$f$ を群元のまま消費し、語長にも $m$ にも依存しない $O(1)$ 群演算で (3.3)(3.4) を判定する。Sol への高速化諮問(付録 C §10.2)の項目 **1・3・5 を同時に解消**する。

---

## 1. ギャップ① — P 側 pcgs 候補 → Q 側評価対象の標準変換

### 1.1 構成(CONV-P)

$j:F_2=K(0,4)\hookrightarrow K(0,5)$, $x\mapsto x_{12},\ y\mapsto x_{23}$。

> **構成 CONV-P.**
> **(前計算・1 回限り)** $D:=[P,P]$ の固定 pcgs $g_1,\dots,g_6$ に対し
> 1. 各 $i$ について $w_i\in F(x,y)$ を 1 つ選び、$P$ での像が $g_i$ となるようにする(`PreImagesRepresentative` を **6 回だけ** 呼ぶ。**候補ごとには呼ばない**);
> 2. $\widehat G_i := w_i\bigl(x_{12}W,\ x_{23}W\bigr)\in Q$ を評価する(6 元)。
>
> **(候補ごと)** 指数ベクトル $(e_1,\dots,e_6)$ に対し
> $$\boxed{\ \bar\jmath(\bar f)\;=\;\widehat G_1^{\,e_1}\widehat G_2^{\,e_2}\cdots \widehat G_6^{\,e_6}\ }\qquad(\text{左から右へ、候補鍵と同一の積順})$$

**★ 罠**: $D=[P,P]$ は**非可換**($[\gamma_2,\gamma_2]\subseteq\gamma_4\ne1$)。積順を候補鍵の宣言(`candidate_key_lib.g`: $g_1^{e_1}\cdots g_6^{e_6}$、$e_1$ が最上位桁)と**厳密に一致**させること。順序を入れ替えると別の元になる。

**必須ゲート(安価・決定的)**: 前計算の $w_i$ について、$P$ の中で $w_i(\bar x,\bar y)=g_i$ を機械照合(6 件)。これが通れば残りは定理(§1.2)で保証される — $w_i$ の選び方に依らない。

### 1.2 well-defined 性(急所)

> **補題 CONV-WD.** $\mathcal V$ を任意の語集合による verbal 作用素とし、$N_{F_2}:=\mathcal V(F_2)$, $W:=\mathcal V(K(0,5))$ とする。このとき $j(N_{F_2})\subseteq W$。ゆえに $j$ は群準同型
> $$\bar\jmath:\;P=F_2/N_{F_2}\;\longrightarrow\;Q=K(0,5)/W$$
> を誘導し、$\bar\jmath(\bar f)$ は代表語 $f$ の取り方に依らない。
>
> **証明.** $\mathcal V(G)$ は語 $v(u_1,\dots,u_k)$($v\in\mathcal V$, $u_i\in G$)の値で生成される。$j$ は準同型ゆえ $j(v(u_1,\dots,u_k))=v(j u_1,\dots,j u_k)\in\mathcal V(K(0,5))=W$。生成元の像が $W$ に入るので $j(\mathcal V(F_2))\subseteq W$。∎

本走の $\mathcal V=\{\text{5 重交換子},\ g^{p}\}$ は verbal(γ₅ も $G^p$ も verbal、verbal の積は verbal)⟹ **(W-c)/(WD) は自動**。これは既存の**補題 NW-2 と同一内容**であり、本票は独立に再証明した(NW-2 追認)。

**⟹ well-defined 判定: 成立(証明つき)。** $\bar\jmath$ が準同型であることから、正規形の像は $\widehat G_i$ の同順序の積になる(CONV-P の公式が正当化される)。

**★ 射程の限定(申し送り)**: 委嘱文の「$K^{(7)}\cap F_2$」で読むと話が変わる。**$K^{(n)}=\ker\psi_n$ は verbal ではない**ので、窓を dihedral 側に差し替える場合 CONV-WD は使えず、$j(K^{(7)}\cap F_2)\subseteq W$ を別途証明する必要がある。本走(§8.7 の verbal 窓対)では**この問題は生じない**。

### 1.3 追加の収穫 — 変換は候補を潰さない

> **補題 CONV-INJ(新 — 本リポジトリに既載なし・`grep` 確認済み。既存の NW-2 は $j$ の単射性を**証明中で使う**が $\bar\jmath$ の単射性は述べていない)。** §1.2 の設定で $\bar\jmath:P\to Q$ は**単射**。
>
> **証明.** $K(0,5)\cong F_3\rtimes K(0,4)$(HS §1.1)で、$j$ はこの半直積の $K(0,4)$ 因子の包含。半直積の射影 $r:K(0,5)\twoheadrightarrow K(0,4)=F_2$($\ker r=F_3$)は準同型で $r\circ j=\mathrm{id}_{F_2}$。いま $f\in F_2$ が $\bar\jmath(\bar f)=1$、すなわち $j(f)\in W=\mathcal V(K(0,5))$ を満たすとする。$r$ は全射準同型ゆえ $r(\mathcal V(K(0,5)))=\mathcal V(r(K(0,5)))=\mathcal V(F_2)=N_{F_2}$。よって $f=r(j(f))\in N_{F_2}$、すなわち $\bar f=1$。∎

**含意**: 117,649 個の候補は $Q$ の中でも相異なる。**変換による候補衝突はゼロ**(join の全単射性が数学的に保証される)。また「hexagon で判定した $\bar f$」と「pentagon で判定した $\bar\jmath(\bar f)$」が**同一対象を指す**ことの正確な意味づけになる(CV-9 仕様同一性判読の材料)。

### 1.4 較正走との接続ゲート(必須)

較正走の Lane P 候補 `jh4^t, jh3` は $Q$/$K(0,5)$ の語として**直接**与えられていた。本走パイプラインの健全性は次で機械確認できる:

> $h_4$(および $h_3$)の `Pcgs(D)` 指数ベクトルを求め、それを CONV-P に通した結果が、**較正走が用いた $Q$ 元と一致する**こと(t=0..6 の 7 件 + h₃)。

実装の接続点: `predicate_lib_laneP.g` L63 が既に `jx := kX12;; jy := kX23;;` を、L115-116 が `jh4Q := ImageElm(epi, jh4);;` を持つ。CONV-P の前計算はこの `epi` をそのまま使い $\widehat G_i:=\mathrm{ImageElm}(\mathtt{epi},\,w_i(\mathtt{jx},\mathtt{jy}))$ とすればよい。ゲートは $\widehat G_1^{e_1}\cdots\widehat G_6^{e_6}$ と `jh4Q` の一致。

一致すれば、変換層は較正走の判定を再現する(判定 predicate `PENT`/`NrhoQ` は digest 不変のまま)。**不一致なら STOP。**

### 1.5 コスト上界(Lane P)

| | 演算 |
|---|---|
| 前計算(1 回) | `PreImagesRepresentative` 6 回 + $Q$ での語評価 6 回 |
| **候補ごと** | $\widehat G_i^{\,e_i}$ を 6 個($e_i\le6$、square-and-multiply で各 $\le3$ 乗算)+ 5 乗算 ⟹ **$\le 23$ 回の $Q$ 上 pc 乗算** |

現行 Lane P の支配項は `ImageElm(rhoQ,·)` 4 連鎖(付録 C §10.1)。$Q$ は 40 生成 pc 群なので `ImageElm` 1 回 ≳ 40 乗算相当。
$$\text{補正係数}\;\approx\;\frac{4\times40+23}{4\times40}\;=\;1.14$$
⟹ **Lane P rate 補正: ×1.15(上界 ×1.2)**。付録 C の central 0.5 s/候補 → **0.575 s/候補**。shard 数は 131 → 151(central)。**壁時計への影響は 7.5 h → 約 8.0 h 程度で、発注可否を変えない。**

---

## 2. ギャップ② — Lane V の語展開コスト

### 2.1 修理 A(現行 `EvalFullHexagonFixed`)の語長上界

候補は $w_1^{e_1}\cdots w_6^{e_6}$ として**語のまま線形展開**できる($\bar\jmath$ と同じ理由で $F(x,y)\to P$ が準同型ゆえ正しい)。⟹ **`PreImagesRepresentative` は候補ごとには不要**(前計算 6 回のみ)。

$$\lvert f\rvert_{x,y}\;\le\;\sum_{i=1}^{6}e_i\lvert w_i\rvert\;\le\;6\,L_{\rm pcgs},\qquad L_{\rm pcgs}:=\sum_i\lvert w_i\rvert$$

**基本交換子基底での実測**(GAP・自由簡約後、`scratchpad/conv_check2.g`):

| $\gamma_2$ の基本交換子 | $[y,x]$ | $[[y,x],x]$ | $[[y,x],y]$ | $[[[y,x],x],x]$ | $[[[y,x],x],y]$ | $[[[y,x],y],y]$ | 合計 |
|---|---|---|---|---|---|---|---|
| 語長(x,y 文字) | 4 | 10 | 8 | 20 | 22 | 18 | **$L_{\rm basic}=82$** |

⟹ **最悪 $\lvert f\rvert_{x,y}\le 452$**(自由簡約込みの実測。素朴上界 $6\times82=492$)、平均 $\approx 3\times82=246$。
σ 文字数は $x=\sigma_1^2,\ y=\sigma_2^2$ で 2 倍: **最悪 904・平均 492**。

`EvalFullHexagonFixed` の 4 系列の総 σ 文字数(コードから逐条計上):
$$\#\mathrm{ApplyGen}\;=\;4u+6\lvert f\rvert_\sigma+16m+4\;=\;6\lvert f\rvert_\sigma+24m+8$$
⟹ **平均 ≈ 3,044・最悪 ≈ 5,576 回/(m,候補)**。

### 2.2 rate 補正 — 実は「補正不要」

較正走の候補語長(同スクリプト実測): $\lvert h_3\rvert=18$、$\lvert h_4^t\rvert\ (t=0..6)=0,98,196,294,392,490,588$。

- **較正走の最悪 588 > 本走の最悪 452。**
- 較正走の平均 $\approx 2076/8=259.5$ ≈ 本走の平均 246。

$$\text{補正係数}\;=\;\frac{6\cdot(2\cdot246)+24\cdot3.5+8}{6\cdot(2\cdot259.5)+8}\;=\;\frac{3044}{3122}\;\approx\;\mathbf{0.98}$$

⟹ **付録 C の Lane V rate に語長由来の補正は要らない(むしろ僅かに保守側)**。prereg v2 §8-3 の懸念「見積りは短い明示語のみを想定」は、**$h_4^6$ が 588 文字で既に本走最悪を上回るため、事実として成り立たない**。

**★ 条件**: これは 6 本の参照語が**基本交換子**である場合。GAP の `Pcgs(D)` 生成元の前像語が長ければ補正は $L_{\rm pcgs}/82$ 倍になる。
**⟹ 指示**: 前計算時に $L_{\rm pcgs}$ を**測定して cert に pin** し、$L_{\rm pcgs}>164$($=2\times82$)なら基本交換子基底へ座標変換してから語展開すること(座標変換は $P$ 内の collection 1 回・候補ごと 1 回で $\lvert f\rvert_{x,y}\le452$ を保証)。

### 2.3 ★ 閉形式 CF — 語展開を消す(推奨)

修理 A は「$\mathrm{ApplyQElt}$ が transversal 共役を落としていた」(仲裁 §3.2)への**安全側の**対処だった。共役を正しく入れれば、$f$ は**群元のまま**扱えて語展開は不要になる。

状態 $(t,d)$ は $g=\tilde d\,\tilde t$ を表す(仲裁 §3.1)。$A_1:=\mathrm{Ad}(\sigma_1)|_Q$, $A_2:=\mathrm{Ad}(\sigma_2)|_Q$、
$$A_1:\ x\mapsto x,\quad y\mapsto y^{-1}x^{-1}c \qquad A_2:\ x\mapsto x^{-1}y^{-1}c,\quad y\mapsto y \qquad(\text{正典 }(1.11)(1.12))$$
$A_{12}:=A_1\circ A_2=\mathrm{Ad}(\sigma_1\sigma_2)$, $A_{21}:=A_2\circ A_1=\mathrm{Ad}(\sigma_2\sigma_1)$, $\beta:=A_1(y)$, $\alpha:=A_2(x)$ とおくと:

> **判定式 CF.** $u=2m+1$ に対し
> $$\text{(3.3)}\iff x^{m}\,A_1(f^{-1})\,\beta^{m}\,A_{12}(f)\;=\;f^{-1}\,A_{12}(x^{-m})\,c^{m} \qquad[\text{両辺 }t=4]$$
> $$\text{(3.4)}\iff f^{-1}\,y^{m}\,A_2(f)\,\alpha^{m}\;=\;A_{21}(y^{-m})\,c^{m}\,A_{21}(f) \qquad[\text{両辺 }t=5]$$

**導出**: 状態機械を正しい規則 $\mathrm{newD}=d\cdot\mathrm{Ad}(\tilde t)(q)$ で追い、$\sigma_1^{2}$ が $t=1$ で $d\mapsto dx$、$\sigma_2^{2}$ が $t=2$ で $d\mapsto d\beta$、$\sigma_2^{2}$ が $t=1$ で $d\mapsto dy$、$\sigma_1^{2}$ が $t=3$ で $d\mapsto d\alpha$ を与えることによる。純 Q 因子が置かれる transversal は語の形だけで決まる($f^{-1}$ は $t=2$、$f$ は $t=4$;(3.4) では $t=1,3,5$)。

**検証(実行済み)**: `scratchpad/conv_check.g` / `conv_check2.g`
- $A_1,A_2$ が **B₃/N 内の literal 共役と全元一致**(主窓 27 元・control 窓 81 元)。
- **CF と literal 構成の判定が完全一致**: 主窓(c=1)162/162、**control 窓(c の位数 3・c-項が生きる)486/486**、いずれも mismatch **0**。charming に限らず $Q$ の**全元** $\times$ $m=0..5$ で照合。

**コスト**: $m$ 依存量($x^m,\beta^m,A_{12}(x^{-m}),c^m,y^m,\alpha^m,A_{21}(y^{-m})$)は **$m$ ごとに 1 回**前計算(= Sol 諮問 §10.2-1 の「m 外側 loop」)。候補ごとは
$$4\ \text{回の }\mathrm{ImageElm}\ (A_1(f^{-1}),A_{12}(f),A_2(f),A_{21}(f))\;+\;\sim12\ \text{乗算}\;+\;2\ \text{比較}$$
**語長にも $m$ にも依存しない。**

$P$ は 8 生成 pc 群なので `ImageElm` ≈ 8 乗算相当 ⟹ $\approx 44$ 乗算相当/候補。修理 A は $\approx3{,}044$ 回の `ApplyGen`(各 1–3 乗算)⟹ **概算で 100–140 倍の削減**(実測ではない・CI 較正 shard で確定させること)。

**N と N₀ の 2 倍係数について**(Sol 諮問 §10.2-5・Sol 回答 F104-1.5 item 5 への回答): $f\in[F_2,F_2]$ ゆえ $\nu(f)=0$($\nu:F_2\to\mathbb Z$ は c-成分を与える準同型で交換子群を殺す)。よって $\mathrm{Ad}(\sigma_i)(f)$ の c-成分は自明で、**$A_1(f^{-1}),A_{12}(f),A_2(f),A_{21}(f)$ は N 窓と N₀ 窓で同一の $P$ の元**。技術的には 4 回の `ImageElm` を両窓で共有でき、Lane V の「×2」は ×1.1 に落ちる。

**★ ただし共有は推奨しない(判定)**。Sol F104-1.5 item 5 は「N/N₀ の word parsing や入力展開は共有してよい」とする一方「判定結果は共有しない。S-9/S-8′ の独立検出力を失わせない」と留保する。ここで**仲裁 §1.1 (P-1) により、charming 候補では N と N₀ の full hexagon 判定は数学的に必ず一致する** — すなわち S-8′ に残っている価値は**実装の交差検査**のみである。自己同型像を共有すると、S-8′ が検査していた当のもの(c 成分の会計)が共有部分に隠れて検出力を失う。CF 採用後は Lane V が費用項でなくなる(§3)ので、**2 倍を払って両窓を独立に計算するのが正しい取引**。共有する場合は S-8′ の格下げを cert に明記すること。

**Sol 諮問 §10.2-3(系列間の部分式再利用)への回答**: CF では 4 系列が同一候補内で 4 つの自己同型像を共有するが、これは**判定の意味論を変えない**(各系列は独立に $Q$ 内の等式であり、共有されるのは入力側の前計算量のみ)。窓をまたぐ共有(上記)とは別問題。

### 2.4 導入方針(安全側)

Sol F104-1.5 の締め(「最適化後の code は較正 driver と byte-identical ではなくなる。**「同じ数学述語」を source-map と両縁 fixture で示し、optimized lane と baseline lane の登録 sample 全一致を新しい較正として置くのが正順**」)と、prereg v2 §6.2(「Lane S/V の m 外側 loop + 前計算 — 設計方針として採択・実装は保留」)・§6.3(optimized-vs-baseline 較正段の新設)にそのまま乗る:

1. **CF を Lane V の判定経路に採用**(§6.2 の「前計算」方針の具体形)。**Lane S には触れない**(Sol item 5 の「S/V の判定コード・群 object を共有しない」を維持)。
2. **`EvalFullHexagonFixed`(修理 A)は baseline として保存**し、標本交差検査に降格: 各 shard で無作為 $k$ 件(例 $k=64$)について CF と baseline の判定一致を機械確認し、件数を cert に記録。**1 件でも不一致なら shard STOP**。これが §6.3 の optimized-vs-baseline 較正段の実体。
3. **較正走 18 件の全一致を発効条件**とする(CF が較正走の判定を 18/18 再現するまで本走に使わない)。
4. **TOY 窓 fixture を恒久回帰に**: `conv_check.g`/`conv_check2.g` の literal 突合(162 点 c=1 / 486 点 c≠1)を driver 起動時セルフテストに組み込む。**c≠1 側を必ず含める** — 主窓だけでは CF の $c^m$ 項が一度も試されない(仲裁で判明した盲点と同型)。既存の TOY fixture(裁定 469 でゲート化済み・162 点)を **486 点側へ拡張**する形になる。
5. **digest**: `EvalFullHexagonFixed` の digest は不変のまま、**CF は新規 predicate として別 digest で pin**(prereg v2 §7-8 の「判定 predicate/library の digest 不変 / 新規 wrapper の個別 pin」の分離規律)。
6. Sol §6.4 で**不採択**の Gray-code 巡回とは独立(CF は候補の列挙順に依存しない)。将来 Gray-code を採るなら CF の上に重ねられる。

---

## 3. rate 見積への反映(付録 C への差分)

| レーン | 付録 C v2 central | 本票の補正 | 補正後 central |
|---|---|---|---|
| **P**(PENT, Q) | 0.5 s/候補 | **×1.15**(CONV-P の 23 乗算) | **0.575** |
| **S**(簡約, P) | 0.05 s/候補(推測) | 変更なし(Lane S は語を使わない) | 0.05 |
| **V**(full ×2, P) | 0.10 s/候補(推測) | **修理 A のまま: ×0.98(補正不要)** / **CF 採用時: 概算 ×0.01**(×2 は温存 — §2.3) | 0.098 / **≈0.001** |

- **修理 A のまま**なら壁時計は付録 C v2 の central 7.5 h からほぼ動かない(Lane P の +15% 分のみ)。**発注可否は変わらない** — これが本票の第一の実務的結論。
- **CF 採用**なら Lane V は費用項から実質脱落し、律速は Lane P(+15%)に一本化される。付録 C v2 §1.2 の shard 数は central 172 → 約 170(P 131→151・V 27→数本)。
- Lane V の per-candidate timeout(prereg v2 §3 の 30 秒)は、修理 A の最悪 5,576 `ApplyGen` でも CF でも余裕(現行 rate の 20 倍マージンは維持される)。
- **未解消(本票の対象外)**: 付録 C §10.2-2(群構築 62 s/46 s の shard ごと再払い)、Lane S/V rate の実測(CI 較正 shard 待ち)。本票の補正係数はいずれも**演算数の比からの見積りであって実測ではない** — CI 較正 shard で確定させること。

---

## 4. 未解決 / 申し送り

- **【要測定・1 回】** $L_{\rm pcgs}=\sum_i\lvert w_i\rvert$($P$ の ANUPQ 構築 62 s が要るため本票では未測定)。$>164$ なら §2.2 の座標変換を発動。**修理 A を採る場合のみ必要**(CF 採用なら不要)。
- **【GAP なし】** ①②とも数学的には閉じた。
- **申し送り(射程)**: CONV-WD/CONV-INJ は **verbal 窓対に限る**。dihedral 窓 $K^{(n)}$ へ差し替える設計変更が出たら両補題とも再証明が要る(§1.2 末)。
- **CF の監査依頼**: 導出は状態機械モデル $g=\tilde d\tilde t$(仲裁 §3.1 で literal 突合済み)に依存する。Sol には **CF の 2 式そのもの**と、$\nu(f)=0$ による N/N₀ 共有の主張を検問してほしい。

**使用ソフト**: GAP 4.16.0(`gap.ps1`・`-o 2g`)
**検証スクリプト**: `scratchpad/conv_check.g`(主窓 162 点)、`scratchpad/conv_check2.g`(control 窓 486 点+語長実測)
