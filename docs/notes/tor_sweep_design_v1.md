# TOR-SWEEP 設計 v1 — S 側の捩れ素数を重みごとに 1 回の整数計算で悉皆する(裁定 726)

**状態札: `design + paper proof / all candidate / Sol 未監査 / GAP 実走ゼロ・cert 発行ゼロ / 封印非接触 / ★ 新規 S 形成ゼロ($\mathcal S_{16}$ 等は作らない — 整構造の設計のみ)/ 判定語の発効は司令塔専権`**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-07 / 委嘱: 司令塔(**裁定 726**・研究者批判起点)
- **研究者の批判(採択済・本設計の存在理由)**: 「A で異常が出てからじゃないと S を調べないなら、**異常が S にしかいなかったら見逃す**」
- 入力正本: `b_type_synthesis_design_v1.md` §(𝒮_k の定義)/ `b_type_synthesis_design_v1_addendum_edim56_prediction.md`・`_result.md`($\rho,j,\nu_k$ の定義と較正)/ `edim_semidirect_model_design_v1.md`(規模表)/ `hs_prop7_translation_v1.md` §(記号表)/ `aside_measurement_design_v1_addendum_d.md`(【D-GAP-1】)/ 裁定 706(E-DIM 実測値)
- **自前検算**: 次元の会計($\mathrm{Witt}(3,k)+\mathrm{Witt}(2,k)$)のみ手計算で確認。**行列は組んでいない**(設計のみ)。

---

## 0. 判定一覧(先に 8 行)

| # | 事項 | 結果 |
|---|---|---|
| **①** | **整捩れ言明の精密化** | $\dim\mathcal S_k@p>\dim\mathcal S_k(\mathbf Q)\iff p\mid d_r(M_k)$($d_r$ = 最大単因子)$\iff p\in\mathrm{supp}\bigl(\mathrm{coker}(M_k)_{\rm tors}\bigr)$。**単因子は $\mathbf Z$-基底の取り方に依存しないが、$\mathbf Z$-格子の取り方には依存する** ⟹ 格子を明示(§1.2)。**格付け = 格子言明**(【D-GAP-1】と同型の限界)(§1.4) |
| **②** ★★★ | **構造定理 TOR-S3**: $p\ge5$ では **$1+\theta$ と $1+\tau+\tau^2$ のブロックは捩れを一切産まない**(Maschke;$\mathbf Z_{(p)}[S_3]$ が最大整環)⟹ 捩れは **$\nu_k$ ブロックだけ**から来る | §2.1 |
| **③** ★★★ | **還元**: 捩れ素数の判定は $\ \nu_k\circ j|_{H_k}:H_k^{\mathbf Z}\to\mathfrak t_k^{\mathbf Z}\ $ **ただ 1 本の行列**の単因子で決まる。$\mathrm{rank}\,H_k=\mathrm{mult}_{\rm std}\bigl(\mathrm{Lie}(x,y)_k\bigr)\approx\mathrm{Witt}(2,k)/3$ ⟹ **$k{=}12$ で $\sim110$ 行、$k{=}13$ で $\sim210$ 行**。$M_k$(全体)を組む必要はない | §2.2 |
| **④** ★★★ | **計算法**: 本命予言(捩れゼロ)の**確認には因数分解が要らない** — $r\times r$ 小行列式を数本取って **gcd $=\pm1$** を見るだけ。$r\sim110$ の Bareiss 行列式 = ミリ秒。gcd $>1$ のときだけ因数分解し、候補ごとに $\mathrm{rank}_p$ で検証 | §3.2 |
| **⑤** ★★★ | **実行可能性**: **$k\le12$ は軽量**(行列 $\sim110\times44{,}555$ = 約 39 MB)。★ **$k=13$ も立つ**($\sim210\times123{,}270$ = 約 207 MB)— **E-DIM $k{=}13$(10–20 時間/数十 GiB 見積)とは別物**。$k\ge14$ は $\mathfrak t_{14}=342{,}645$ で境界(要見積り走) | §4 |
| **⑥** ★★★ | **F-GAP-3 との共通化 — 予想外の副産物** | 同じ「**小さい source × 大きい target**」の再定式化が $\sigma_m$ の構築にもそのまま効く。$\sigma_{13}\in\mathcal S_{13}=\ker(\nu_{13}|_{H_{13}})$ ⟹ **$\sigma_{13}$ が $\sim210\times123{,}270$ の核計算に落ちる可能性** ⟹ **重み族分光 §4.2 の「$\sigma_{13}$ は射程外」判定を条件付きで覆す**(§4.3) |
| **⑦** | **予言凍結** | **P-T-1(本命)= 捩れ素数ゼロ**($k\le12$、可能なら $k=13$)。的中なら「$k^*\ge13$ は S の意味で**全素数無条件**」へ格上げ。外れれば **S 単独異常の第一発見** ⟹ 検疫手順を先に固定(§5) |
| **⑧** | **拘束の遵守** | $\mathcal S_{16}$ 等の新規 S は形成しない。本設計が触るのは **$k\le13$ の既存模型の整構造だけ** |

> ### ★ 本設計の一行
> $$\boxed{\ \textbf{素数を走査する代わりに、重みごとに 1 本の整数行列の単因子を見る。隠れ場所は原理的に存在しない。}\ }$$

---

# 1. 委嘱① — 整捩れ言明の精密化

## 1.1 模型の記号(既在の定義を再定義しない)

`b_type_synthesis_design_v1.md` と `..._addendum_edim56_*.md` より:
$$\boxed{\ \dim\mathcal S_k=\dim\Bigl(\ker(1+\theta)\ \cap\ \ker(1+\tau+\tau^2)\ \cap\ \ker\bigl(\nu_k\circ j\bigr)\Bigr)\ }$$
- **source の ambient**: $\Lambda_k:=\mathrm{Lie}(x,y)_k$、$\dim_{\mathbf Q}=\mathrm{Witt}(2,k)$。
- $\theta$: $x\leftrightarrow y$(位数 2)。$\tau$: $x\mapsto y\mapsto z\mapsto x$、$z=-x-y$(位数 3)。$\langle\theta,\tau\rangle\cong S_3$ が $\Lambda_k$ に作用。
- $\mathfrak t:=\mathrm{gr}(K(0,5))$ = 5 生成元 $T_0,\dots,T_4$ の自由 Lie 環を Drinfeld–Kohno の 2 次関係式で割ったもの。$\dim_{\mathbf Q}\mathfrak t_k=\mathrm{Witt}(3,k)+\mathrm{Witt}(2,k)$(**$K(0,5)\cong F_3\rtimes F_2$**・次数 6 まで実測較正済)。
- $j:x\mapsto T_0(=t_{12}),\ y\mapsto T_1(=t_{23})$、$\rho:T_i\mapsto T_{i+3\bmod5}$(位数 5)、$\nu_k=\sum_{i=0}^4\rho^i$($C_5$ のノルム元)。

**次元の会計(自前確認)**
| $k$ | $\mathrm{Witt}(2,k)$ | $\mathrm{Witt}(3,k)$ | $\dim\mathfrak t_k$ | 語 ambient $3^k{+}2^k$ |
|---:|---:|---:|---:|---:|
| 11 | 186 | **16,104**(裁定 732 訂正) | **16,290**(同左) | 179,195 |

> **(裁定 732 訂正・司令塔修正権行使)**: 本行の原記載は Witt(3,11)=14,880・dim 𝔱₁₁=15,066(起草者「手計算のみ」箇所)。実装係のカナリア T-a が捕獲し、機械 3 系統(メビウス公式 (3¹¹−3)/11=16,104・Lyndon 直接列挙・司令塔独立検算)+既存台帳値(裁定 659: dim 𝔱₁₁=16,290)で **16,104 / 16,290** に確定。k=12,13,14 行は機械検算一致・無傷。
| **12** | **335** | 44,220 | **44,555** ✔(委嘱の値と一致) | 535,537 |
| **13** | **630** | 122,640 | **123,270** ✔(委嘱の値と一致) | 1,602,515 |
| 14 | 1,161 | 341,484 | 342,645 | 4,799,353 |

## 1.2 ★ $\mathbf Z$-格子の明示(**ここを固定しないと言明が意味を持たない**)

> ### 定義 LAT($\mathbf Z$-構造の正本)
> - $\Lambda_k^{\mathbf Z}:=$ **自由 Lie 環** $\mathrm{Lie}_{\mathbf Z}(x,y)$ の次数 $k$ 部分。**Lyndon 基底が $\mathbf Z$-基底**(古典)⟹ 階数 $\mathrm{Witt}(2,k)$ の自由 $\mathbf Z$-加群 ✔
> - $\mathfrak t_k^{\mathbf Z}:=$ $T_0,\dots,T_4$ 上の**自由 Lie 環**を DK 関係式の生成する**イデアルで割った**もの(**群の下中心列の gr ではなく、表示による定義**)。
> - $\theta,\tau,\rho,j$ はすべて**生成元を生成元の整係数線形結合に写す**ので $\mathbf Z$-格子を保つ ✔($\tau(y)=z=-x-y$ も整) ⟹ $M_k$ は**整行列**であり、分母を払う操作は一切要らない。

> ### ⚠ 仮定 (H-LAT)(**明示する・カナリアで検査する**)
> $\mathfrak t_k^{\mathbf Z}$ が**捩れのない**自由 $\mathbf Z$-加群で階数 $=\mathrm{Witt}(3,k)+\mathrm{Witt}(2,k)$ であること。
> **根拠**: 既在の較正(`_addendum_edim56_result.md`)が $K(0,5)\cong F_3\rtimes F_2$ の半直積構造を次数 6 まで再現している ⟹ $\mathfrak t\cong\mathrm{Lie}(3\ \text{gens})\ltimes\mathrm{Lie}(2\ \text{gens})$ が**次数ごとに $\mathbf Z$ 上でも分裂**すれば、Lyndon(3)$\sqcup$Lyndon(2) が $\mathbf Z$-基底になる。
> **カナリア T-a**: 各 $k$ で $\mathfrak t_k^{\mathbf Z}$ の Hermite 標準形の対角成分がすべて $\pm1$(= 表示から作った生成系が $\mathbf Z$ 上自由で階数が予測どおり)。**失敗したら $\mathfrak t$ 自身に捩れがあり、TOR-SWEEP の全ての値が $\mathfrak t$ の捩れ素数と混ざる ⟹ STOP。**

## 1.3 ★ 主定理(整捩れの判定式)

> ### 定理 TOR-1(candidate・本ノート。**古典的事実の本設定への正確な適用**)
> $M_k:\Lambda_k^{\mathbf Z}\to\Lambda_k^{\mathbf Z}\oplus\Lambda_k^{\mathbf Z}\oplus\mathfrak t_k^{\mathbf Z}$、$v\mapsto\bigl((1+\theta)v,\ (1+\tau+\tau^2)v,\ \nu_k(j(v))\bigr)$ とし、$r:=\mathrm{rank}_{\mathbf Q}M_k$、$d_1\mid d_2\mid\cdots\mid d_r$ を非零単因子とする。このとき
> $$\boxed{\ \dim_{\mathbf F_p}\mathcal S_k@p\ >\ \dim_{\mathbf Q}\mathcal S_k\ \iff\ \mathrm{rank}_{\mathbf F_p}M_k<r\ \iff\ p\mid d_r\ \iff\ p\mid\prod_{i=1}^r d_i\ }$$
> さらに $\ \{p:\ p\mid d_r\}=\mathrm{supp}\bigl(\mathrm{coker}(M_k)_{\rm tors}\bigr)$。
> **証明.** $\dim\ker=n-\mathrm{rank}$。Smith 標準形で $\mathrm{rank}_{\mathbf F_p}M_k=\#\{i\le r: p\nmid d_i\}$ ⟹ $<r\iff p\mid d_i$ なる $i$ が在る $\iff p\mid d_r$($d_i\mid d_r$)$\iff p\mid\prod d_i$。最後の等式は $\mathrm{coker}(M_k)_{\rm tors}\cong\bigoplus\mathbf Z/d_i$。∎
> ### 系(**委嘱の骨子の正確形**)
> $$\boxed{\ \textbf{捩れ素数の完全リスト}\ =\ \{p:\ p\mid d_r(M_k)\}\ \textbf{— 有限で、1 回の整数計算で求まる。素数走査は不要。}\ }$$

## 1.4 ★ 基底非依存性と**格付け**(委嘱の指定)

- **基底非依存 ✔**: 単因子は $\mathbf Z$-加群の準同型の不変量であり、source/target の $\mathbf Z$-基底を $GL_n(\mathbf Z)$ で取り替えても不変。⟹ Lyndon 基底でも Hall 基底でもよい。
- **格子依存 ⚠**: **格子を替えると単因子は変わる。** とくに
 - $\Lambda_k^{\mathbf Z}$ を「Lie 環の $\mathbf Z$-形」ではなく「語 ambient $\mathbf Z\langle x,y\rangle_k$ の中の Lie 部分の $\mathbf Z$-span」で取ると**同じ**(自由 Lie 環は結合的自由環の $\mathbf Z$-直和因子 — PBW が $\mathbf Z$ 上成立)⟹ ここは安全。
 - $\mathfrak t_k^{\mathbf Z}$ を「表示による $\mathbf Z$-形」で取るか「語 ambient $3^k{+}2^k$ 内の span」で取るかは**別の格子になりうる** ⟹ **必ず (H-LAT) のカナリアを通す**。
- **★ 格付け(【D-GAP-1】との関係)**:
 $$\boxed{\ \textbf{TOR-SWEEP の出力は「指定した }\mathbf Z\textbf{-格子上の格子言明」であって、算術的対象そのものの言明ではない。}\ }$$
 【D-GAP-1】(`aside_..._addendum_d.md` §0.7: 「$\mathcal A_{12}@691{=}1$ は括弧格子 $M$ の言明であり、SYN-0 が要求する算術像の第 12 層へ渡すには『$\mathrm{gr}_{12}(H)=M$ の還元』という一段が要る — 未証明」)と**同型の限界**である。⟹ 捩れゼロが出ても「全素数で $\mathcal S$ に異常なし」までであり、そこから B 型不在へ渡るには **D-GAP-1 と同じ一段**が要る。**この限定を報告に必ず併記すること。**

---

# 2. ★★★ 構造定理 — 捩れは $\nu_k$ ブロックにしか棲めない

## 2.1 定理 TOR-S3($S_3$ ブロックの無捩れ性)

> ### 定理 TOR-S3(candidate・本ノート)
> $\Lambda$ を有限階数の $\mathbf Z[S_3]$-格子、$N_\theta:=1+\theta$、$N_\tau:=1+\tau+\tau^2$、$H:=\ker N_\theta\cap\ker N_\tau\subseteq\Lambda$(飽和部分格子)とする。**$p\ge5$** なら
> $$\boxed{\ H\otimes\mathbf F_p\ \xrightarrow{\ \sim\ }\ \ker(N_\theta\bmod p)\cap\ker(N_\tau\bmod p)\ }$$
> すなわち **$S_3$ ブロック単独では跳びが起こらない**。
>
> **証明.** $p\nmid6=\lvert S_3\rvert$ ⟹ $e_{\rm triv},e_{\rm sgn},e_{\rm std}\in\mathbf Z_{(p)}[S_3]$(分母は 6 の約数)⟹ $\Lambda_{(p)}=e_{\rm triv}\Lambda\oplus e_{\rm sgn}\Lambda\oplus e_{\rm std}\Lambda$ は $\mathbf Z_{(p)}$-直和分解。各成分での作用:
> $$N_\theta:\ 2\ (\text{triv}),\quad 0\ (\text{sgn}),\quad 1+\rho_{\rm std}(\theta)\ (\text{std});\qquad N_\tau:\ 3\ (\text{triv}),\quad 3\ (\text{sgn}),\quad 0\ (\text{std}).$$
> $2,3\in\mathbf Z_{(p)}^\times$ ⟹ triv 成分の核は $0$、sgn 成分の核は $N_\tau=3$ ゆえ $0$。std 成分では $N_\tau=0$ かつ $\tfrac{1+\rho_{\rm std}(\theta)}2$ が $\mathbf Z_{(p)}$ 上の冪等 2×2 行列 ⟹ $\ker(1+\rho_{\rm std}(\theta))$ は直和因子(std の $\theta$ に関する $-1$ 固有直線)。
> ゆえに $H_{(p)}$ は $\Lambda_{(p)}$ の**直和因子** ⟹ $\bmod p$ 還元と可換。∎
>
> ### 系 TOR-S3′(**行数と階数**)
> $$\mathrm{rank}\,H_k=\mathrm{mult}_{\rm std}\bigl(\Lambda_k\bigr)=\tfrac16\sum_{g\in S_3}\chi_{\rm std}(g)\,\mathrm{tr}(g\mid\Lambda_k)\ \approx\ \tfrac13\mathrm{Witt}(2,k).$$
> ($\Lambda_k$ の std 各コピーがちょうど 1 次元を寄与する。厳密値は段 T1 の出力。)

## 2.2 ★★ 還元(**本設計の実装上の心臓**)

> ### 系 TOR-2(candidate・本ノート)
> $H_k^{\mathbf Z}:=\Lambda_k^{\mathbf Z}\cap\ker N_\theta\cap\ker N_\tau$(**飽和**)とし、$N_k:=\nu_k\circ j\big|_{H_k^{\mathbf Z}}:H_k^{\mathbf Z}\to\mathfrak t_k^{\mathbf Z}$ と置く。**$p\ge5$** に対し
> $$\boxed{\ \mathcal S_k@p\ \textbf{の跳び}\ \iff\ p\mid d_{r'}(N_k)\qquad(r'=\mathrm{rank}_{\mathbf Q}N_k)\ }$$
> すなわち **捩れ素数($\ge5$)の完全リストは $N_k$ ただ 1 本の単因子で決まる**。$M_k$ 全体を組む必要はない。
> **証明.** 定理 TOR-S3 より $\ker(N_\theta,N_\tau)\bmod p=H_k\otimes\mathbf F_p$。$\mathcal S_k@p=\ker(N_k\bmod p)$、$\mathcal S_k(\mathbf Q)=\ker(N_k\otimes\mathbf Q)$。定理 TOR-1 を $N_k$ に適用。∎
>
> $$\Longrightarrow\ \textbf{行列サイズ}:\ \underbrace{\mathrm{rank}\,H_k}_{\approx\mathrm{Witt}(2,k)/3}\ \times\ \underbrace{\dim\mathfrak t_k}_{44{,}555\ (k{=}12)}\qquad\textbf{— 行が極端に少ない「縦長でなく横長」の行列}$$
>
> ### ★ これが効く理由(一行)
> $$\boxed{\ \textbf{単因子は高々 }\mathrm{rank}\,H_k\ \textbf{個しかない。}\ \mathfrak t_k\ \textbf{がいくら大きくてもそこは効かない。}\ }$$

> ### ⚠ 実装上の必須注意 **SAT**
> $H_k^{\mathbf Z}$ は**飽和**でなければならない($\mathbf Q$ 上で核を取り、$\Lambda_k^{\mathbf Z}$ との交わりを Hermite 標準形で取る)。飽和していない格子を使うと**存在しない捩れ素数が湧く**(最も起きやすい実装事故)。⟹ **カナリア T-b**: $\Lambda_k^{\mathbf Z}/H_k^{\mathbf Z}$ が捩れなし(HNF の対角が全て $\pm1$ になる部分を確認)。

## 2.3 $p=2,3$ の扱い(正直に)

定理 TOR-S3 は $p\ge5$ 限定。$p=2,3$ では $S_3$ ブロック自身が捩れを産みうる($\hat H^*(C_2,\Lambda)$、$\hat H^*(C_3,\Lambda)$)。
$$\boxed{\ \textbf{捩れ素数}\subseteq\{2,3\}\ \cup\ \{p\ge5:\ p\mid d_{r'}(N_k)\}\ }$$
本設計は **$p\ge5$ を対象とする**($B$ 型・非正則素数の議論はすべて $p\ge5$)。$p=2,3$ を含めた完全版が要るなら $M_k$ 全体で回す(コストは §4 の $\times3$ 程度)。

---

# 3. 委嘱② — 計算法の設計

## 3.1 素朴 SNF が駄目な理由(確認)

$N_k$ の Smith 標準形を消去で直接求めると中間係数が爆発する(古典的な SNF の悪性)。$r'\sim110$ でも、$44{,}555$ 列を消去していく過程で係数が指数的に伸びうる。⟹ **素朴 SNF は使わない。**

## 3.2 ★★★ 推奨アルゴリズム **TOR-DET**(本命予言の確認に因数分解が不要)

> ### アルゴリズム TOR-DET
> 1. **$r'$ を決める**: 大きめのランダム素数 $q$($\sim2^{61}$)で $\mathrm{rank}_{\mathbf F_q}N_k$ を計算 ⟹ $r'$(**カナリア T-c**: 複数の $q$ で一致)。
> 2. **非特異 $r'\times r'$ 小行列を取る**: $\bmod q$ の階段化で行・列の pivot 集合 $(I,J)$ を得て、整数行列 $A_1:=N_k[I,J]$ を切り出す($\det A_1\ne0$)。
> 3. **行列式を厳密に計算**: **Bareiss(分数なし消去)**で $\det A_1\in\mathbf Z$。$r'\sim110$ ⟹ **ミリ秒〜秒**。
> 4. **独立な小行列をあと 2〜4 本**($J$ を別の pivot 集合に取り替える)⟹ $\det A_2,\dots,\det A_s$。
> 5. $g:=\gcd(\det A_1,\dots,\det A_s)$。
> - **$\lvert g\rvert=1$** ⟹ $d_{r'}=1$ ⟹ $\boxed{\textbf{捩れ素数ゼロ(全素数について証明終わり)}}$。★ **因数分解は一切不要。**
> - **$\lvert g\rvert>1$** ⟹ 捩れ候補は $g$ の素因子のみ。$g$ を因数分解し(通常は小さい)、各候補 $p$ について $\mathrm{rank}_{\mathbf F_p}N_k<r'$ を直接確認して**確定**。
>
> **正当性**: $D_{r'}(N_k)=\gcd(\text{全 }r'\times r'\text{ 小行列式})\mid\gcd_i\det A_i=g$、かつ $d_{r'}\mid D_{r'}$ ⟹ $p\mid d_{r'}\Rightarrow p\mid g$。∎
> ★ **非対称性が効く**: 「捩れゼロ」は $\gcd=1$ の**1 行**で証明でき、「捩れあり」のときだけ追加作業が要る。**本命予言側が最も安い**という良い設計。

## 3.3 代替・補助

| 手法 | 使いどころ | 評価 |
|---|---|---|
| **Bareiss + gcd(TOR-DET)** | **本命** | $r'^3$ の整数演算 + gcd ⟹ 秒。**推奨** |
| **HNF → SNF**($r'\times r'$ に潰してから) | $g>1$ のとき単因子の**完全な列**が要る場合 | $r'\sim110$ なら実用。$44{,}555$ 列を直接 SNF しない |
| **多素数 rank プロファイル + CRT** | 交差検証・**独立系統** | $\mathrm{rank}_{\mathbf F_p}$ を素数ごとに測る。**悉皆性は無い**が、TOR-DET の結果と矛盾しないことの検温になる |
| **$p$ 進 Dixon 法**($\det$ を $p$ 進で解く) | $r'$ が数千に育ったとき | $k\ge14$ 用の予備 |
| **既存 packed int64 資産の再利用** | 段 T2 の $\bmod q$ 階段化 | 裁定 706 の工事(dict→packed int64)がそのまま効く ⟹ **ep-keeper へ流用依頼** |

## 3.4 実装指示書 **TOR-1**(数学者 → 実装係 / ep-keeper)

**宇宙の事前登録(走行前に凍結)**: 重み $k\in\{9,10,11,12\}$(本命)+ $k=13$(認可後)。**$k\ge14$ と $k=16$ は本票の射程外**。格子は §1.2 の定義 LAT。

| 段 | 内容 | 出力 | 予測/カナリア |
|---|---|---|---|
| **T0** | $\mathfrak t_k^{\mathbf Z}$ を表示から構成し HNF で自由性と階数を確認 | `t_rank`, `t_hnf_diag_all_units(bool)` | **カナリア T-a**: 階数 $=\mathrm{Witt}(3,k)+\mathrm{Witt}(2,k)$、対角全 $\pm1$。失敗 ⟹ STOP |
| **T1** | $H_k^{\mathbf Z}=\Lambda_k^{\mathbf Z}\cap\ker N_\theta\cap\ker N_\tau$ を**飽和して**構成 | `H_rank`, `H_basis`, `saturated(bool)` | **カナリア T-b**(飽和)。`H_rank` $\approx\mathrm{Witt}(2,k)/3$ |
| **T2** | $N_k=\nu_k\circ j\vert_{H}$ を組む(**$H$ の基底ベクトルにだけ $\nu_k\circ j$ を適用**) | 疎/密行列 `H_rank × dim t_k` | 行数が `H_rank` であることを assert |
| **T3** | $r'=\mathrm{rank}_{\mathbf F_q}N_k$ を 3 個の大素数で | `rank_q[3]` | **カナリア T-c**: 3 個一致。**副産物: $\dim\mathcal S_k(\mathbf Q)=\mathrm{H\_rank}-r'$** |
| **T4** ★ | **TOR-DET**: $s\ge3$ 本の $r'\times r'$ 小行列式 → `gcd` | `dets[s]`(桁数のみ報告可)、`gcd_abs` | **P-T-1**: `gcd_abs = 1` |
| **T5** | `gcd_abs>1` のときのみ: 因数分解 → 各候補 $p$ で $\mathrm{rank}_{\mathbf F_p}N_k$ | `torsion_primes[]`, `jump_at_p[]` | §5 の**検疫手順へ直行**(発表しない) |

**出力 cert**: `search/certs/torsweep_k<k>_<date>.json` — 上記全欄 + `witt2, witt3, t_rank, H_rank, rank_q, dim_S_Q, gcd_abs, torsion_primes[]`、および環境(版・seed・入力ハッシュ)。
**停止規則**: `S-TOR-1` カナリア T-a/T-b/T-c いずれか失敗 ⟹ `LATTICE_CANARY_FAIL / STOP`(値を報告しない)。`S-TOR-2` `dim_S_Q` が既知の $k\le11$ の値と食い違う ⟹ `REGRESSION_FAIL / STOP`。`S-TOR-3` 壁時計 cap: $k\le12$ は 3,600 秒、$k=13$ は 14,400 秒。`S-TOR-4` **判定語禁止** — cert に「捩れなし」「全素数無条件」等を書かない(生値と bool のみ・発効は司令塔)。

---

# 4. 委嘱③ — 実行可能性表

## 4.1 規模

| $k$ | $\mathrm{rank}\,H_k$(概算 $\approx\mathrm{Witt}(2,k)/3$) | $\dim\mathfrak t_k$ | $N_k$ の int64 サイズ | 判定 |
|---:|---:|---:|---:|---|
| 9 | $\approx19$ | **2,240**(裁定 732 系訂正) | 0.34 MB | ✔ 秒 |
| 10 | $\approx33$ | **5,979**(同) | 1.58 MB | ✔ 秒 |
| 11 | $\approx62$ | **16,290**(同) | **8.08 MB** | ✔ 秒〜分 |
| **12** | $\approx112$ | **44,555** | **40 MB** | ★ **✔ 軽量** |
| **13** | $\approx210$ | **123,270** | **207 MB** | ★ **✔ 立つ**(本機 8 GB 内) |
| 14 | $\approx387$ | 342,645 | 1.06 GB | △ 境界(要見積り走・GHA 推奨) |
| $\ge15$ | — | — | — | ✗ **圏外**(明記) |

> ### ★ 追認と自己捕獲の拡大(**裁定 732・起草者の追認**・2026-08-07)
> **裁定 732 を追認する。$\mathrm{Witt}(3,11)=16{,}104$・$\dim\mathfrak t_{11}=16{,}290$ が正しく、原記載 14,880 / 15,066 は起草者(数学者)の誤り**である。機械 3 系統(メビウス公式・Lyndon 列挙・司令塔検算)+ 裁定 659 の台帳値との一致を、起草者側でも独立に再現した((3¹¹−3)/11 = 177,144/11 = **16,104**)。
> ★ **さらに自己捕獲**: 同じ検算を §4.1 の**全行**に掛けたところ、**$k=9,10$ も誤っていた**(2,182 → **2,240** / 6,018 → **5,979**)。すなわち誤りは 1 セルの孤立事故ではなく、**「手計算のみ」で埋めたセルが $k\le11$ で全滅**していた。$k=12,13,14$ は委嘱で与えられた値に錨を取っていたため無傷。
> **結論への影響はゼロ**: $\mathrm{rank}\,H_k\approx\mathrm{Witt}(2,k)/3$ 列と判定列(✔/△/✗)は不変、$k=11$ のサイズが 7.5 → 8.08 MB に変わるだけ。§2 の定理群・§3 のアルゴリズム・§4.3 の $\sigma_{13}$ 覆しはいずれも**数値に依存しない**。
> **教訓の受理**(裁定 668 規則の適用拡張): **設計表の各セルに検算コマンドを併記する**。本表の再現コマンド:
> ```
> python -c "
> def mu(n):
>  r=1;d=2;m=n
>  while d*d<=m:
>   if m%d==0:
>    m//=d
>    if m%d==0: return 0
>    r=-r
>   d+=1
>  if m>1: r=-r
>  return r
> def witt(q,n):
>  s=sum(mu(d)*q**(n//d) for d in range(1,n+1) if n%d==0); assert s%n==0; return s//n
> for k in range(9,15):
>  w2,w3=witt(2,k),witt(3,k); print(k,w2,w3,w2+w3,round(w2/3),round(w2/3)*(w2+w3)*8/1e6)
> "
> ```
> 出力(**本表の正本**): `9 56 2184 2240 19 0.34` / `10 99 5880 5979 33 1.58` / `11 186 16104 16290 62 8.08` / `12 335 44220 44555 112 39.92` / `13 630 122640 123270 210 207.09` / `14 1161 341484 342645 387 1060.83`。
> ★ **カナリア T-a の設計が機能した実例**として記録(段 T0 の「階数が $\mathrm{Witt}(3,k)+\mathrm{Witt}(2,k)$ と一致するか」が、走る前に設計表の誤りを捕まえた)。

> ### ★ E-DIM との比較(**重要な差**)
> E-DIM の $k=12$ 見積りは **100–120 分 / peak 6–9 GiB**(裁定 706)。TOR-SWEEP は **同じ模型の同じ $k$** でありながら桁違いに軽い。理由:
> 1. **行が少ない**: $\mathcal S_k$ の計算を「$\mathfrak t_k$ 全体の連立」ではなく「$H_k$ の基底 $\sim112$ 本の像」に落としている(系 TOR-2)。
> 2. **語 ambient を使わない**: Lyndon 基底で $\mathfrak t_{12}$ は 44,555(語 ambient $3^{12}{+}2^{12}=535{,}537$ の **1/12**)。
> ⟹ ★ **既存 E-DIM 実装がこの 2 つの節約をしていない可能性が高い**(裁定 706 の工事記述「112 行×$(3^{12}+2^{12})$」は語 ambient を示唆)。**ep-keeper への確認事項**。**していないなら、E-DIM 本体にもこの節約が効く。**

## 4.2 $k\ge14$ = 圏外の明記

$\mathfrak t_{14}=342{,}645$、$\mathrm{rank}\,H_{14}\approx387$ ⟹ 密行列 1.06 GB。**本機(8 GB)では階段化の作業領域が足りない見込み**。$k\ge15$ は $\mathfrak t_{15}\approx0.96$M ⟹ **圏外**。
$$\boxed{\ \textbf{TOR-SWEEP の射程は }k\le13\ \textbf{(}k=14\ \textbf{は要見積り)。}k\ge15\ \textbf{は掘らないのであって、空ではない。}\ }$$

## 4.3 ★★★ 委嘱: F-GAP-3 との道具共通化 — **予想外の副産物**

**F-GAP-3**(`weight_family_spectroscopy_design_v1.md` §4.3): 「$\sigma_m$ solver は深さ切り詰め可能か。可なら重み 16 は立ち、不可なら立たない。」そこで私は $\sigma_{13}$ を **E-DIM $k{=}13$ 相当(10–20 時間 / 60–100 GiB)**と外挿し、**射程外**と判定した。

> ### ★ 本設計による条件付き覆し
> $\sigma_{13}$ は **$\mathcal S_{13}$ の元**である。系 TOR-2 より
> $$\mathcal S_{13}=\ker\Bigl(N_{13}:H_{13}^{\mathbf Z}\to\mathfrak t_{13}^{\mathbf Z}\Bigr),\qquad \mathrm{rank}\,H_{13}\approx210,\ \dim\mathfrak t_{13}=123{,}270 .$$
> ⟹ $\sigma_{13}$ の構築は **$\sim210\times123{,}270$ 行列の核**を取るだけ(段 T1–T3 と**同一の計算**)。
> $$\boxed{\ \textbf{TOR-SWEEP が立つなら }\sigma_{13}\ \textbf{も立つ。深さ切り詰め(F-GAP-3)は不要になる。}\ }$$
> ⟹ **重み族分光 §4.2 の「$\sigma_{13}$ は射程外」判定は、この再定式化が実装可能なら覆る。**
> ⚠ **条件**(過大主張しない): (a) $\nu_k\circ j$ を $H_k$ の基底ベクトルに適用する計算自体のコストが線形であること(括弧の展開が爆発しないこと)、(b) (H-LAT) が通ること、(c) 既存実装がこの形に組み替えられること。**(a) が唯一の実質的リスク** ⟹ **段 T2 の実測が $k=11$ で軽ければ (a) は解決**。
> ⟹ **推奨**: **段 T0–T3 を $k=11$ で先に走らせる**($k=11$ は E-DIM 実測 662 秒の既知点 ⟹ 直接比較できる)。**ここが TOR-SWEEP と重み 16 の両方の生死を同時に決める最安の一手**である。

## 4.4 共通化の一覧(委嘱の「明記せよ」)

| 道具 | TOR-SWEEP | F-GAP-3 / 重み 16 | 共通か |
|---|---|---|---|
| $\mathfrak t_k^{\mathbf Z}$ の Lyndon 基底構成 | 必須(段 T0) | $\sigma_{13}$ に必須 | ★ **完全共通** |
| $H_k^{\mathbf Z}$ の飽和構成 | 必須(段 T1) | $\sigma_m$ の解空間の母体 | ★ **完全共通** |
| $\nu_k\circ j$ の基底ベクトル適用 | 必須(段 T2) | 同上 | ★ **完全共通** |
| 大素数 rank / packed int64 | 段 T3 | $\bmod p$ 走 | ★ 共通(裁定 706 資産) |
| Bareiss 整数行列式 | 段 T4 | 不要 | TOR 専用 |
| **深さ切り詰め** | ★ **不要** | F-GAP-3 の争点 | ★ **TOR は F-GAP-3 に依存しない** |
| $\theta$ の深さ反転 | 影響なし | F-GAP-3 の障害 | — |

$$\boxed{\ \textbf{TOR-SWEEP は F-GAP-3 の回答を待たずに走れる。逆に TOR-SWEEP の成功が F-GAP-3 を不要にしうる。}\ }$$

---

# 5. 委嘱④ — 予言凍結と検疫手順

## 5.1 IF-FIRST 予言(**測定前に凍結**)

| # | 予言 | **偽ならどう変わるか**(検定力) |
|---|---|---|
| **P-T-1** ★本命 | $k\in\{9,10,11,12\}$ で **捩れ素数ゼロ**($\gcd=\pm1$) | 非ゼロ ⟹ **S 単独異常の第一発見** ⟹ §5.3 の検疫へ |
| **P-T-2** | $k=13$ でも捩れ素数ゼロ | 同上 |
| **P-T-3** | 段 T3 の副産物 $\dim\mathcal S_k(\mathbf Q)$ が $k\le11$ の既知値を再現 | 不一致 ⟹ 模型・格子・実装のいずれかが違う ⟹ STOP(回帰) |
| **P-T-4** | $\mathrm{rank}\,H_k=\mathrm{mult}_{\rm std}(\Lambda_k)$ が $\approx\mathrm{Witt}(2,k)/3$ | 大きく外れる ⟹ $S_3$-作用の実装ミス(系 TOR-S3′ の検算) |
| **P-T-5** | (H-LAT) が通る($\mathfrak t_k^{\mathbf Z}$ 自由・階数一致) | 失敗 ⟹ $\mathfrak t$ 自身の捩れ ⟹ **TOR-SWEEP の全結果が汚染** ⟹ STOP |

## 5.2 ★ 的中したときの格上げ文(**先に文言を固定する**)

P-T-1(+P-T-2)が的中し、既在の「$k\le12$ で測った全素数が有理値どおり」と合わせると:

> $$\boxed{\ \textbf{$k\le12$(可能なら 13)について、}\dim\mathcal S_k@p=\dim\mathcal S_k(\mathbf Q)\ \textbf{が}\ \textbf{全ての素数 }p\ge5\ \textbf{で成立する(格子言明)。}\ }$$
> ⟹ **「$k^*\ge13$ は S の意味で全素数無条件」**へ格上げできる。
> ⚠ **限定 3 点(必ず併記)**: (i) **格子言明**であり算術像への移送は【D-GAP-1】と同じ一段を要する。(ii) $p=2,3$ は本設計の射程外(§2.3)。(iii) 「$k^*\ge13$」は **S 側の言明**であり、$\mathcal A$ 側との比較($\dim\mathcal S_k>\dim\mathcal A_k$ の初発点)は別の入力を要する。
> ★ **研究者の批判への回答**: この格上げが成れば「**異常が S にしかいなかったら見逃す**」という抜け穴は $k\le13$ の範囲で**原理的に閉じる**(素数走査ではなく単因子の悉皆だから、どの素数にも隠れ場所がない)。

## 5.3 ★ 捩れが出たときの**検疫手順**(発火前に固定)

> ### 手順 QUAR-TOR(**この順序を守る・逸脱は逸脱として報告**)
> 1. **封鎖**: 検出素数 $p_0$ を `QUARANTINED` として記録し、**cert の外に出さない**。司令塔以外へ流さない。判定語(「捩れ発見」「S 単独異常」)を**書かない**。
> 2. **実装事故の排除(最優先)**:
> (a) **飽和忘れ**(カナリア T-b)— 最頻の事故。$H_k^{\mathbf Z}$ を HNF で取り直して再計算。
> (b) **(H-LAT) 違反**(カナリア T-a)— $\mathfrak t_k^{\mathbf Z}$ 自身の捩れが混入していないか。
> (c) **小行列選択の偏り** — 別の pivot 集合で $\det$ を取り直し、$p_0\mid\gcd$ が保たれるか。
> 3. **独立系統での再現**: $\mathrm{rank}_{\mathbf F_{p_0}}N_k<r'$ を **TOR-DET とは別の実装**(多素数 rank 経路)で直接確認。**一致するまで先へ進まない**。
> 4. **格子依存性の診断**: **別の $\mathbf Z$-格子**(Lyndon 基底 vs 語 ambient 内の span)で再計算。
> - 両方で $p_0$ が出る ⟹ 格子に鈍感 = **本物の候補**。
> - 片方だけ ⟹ **格子アーティファクト**(【D-GAP-1】型の限界の実例)⟹ そう記録して閉じる。
> 5. **算術側との突合**: $p_0$ が **Bernoulli 分子**(691, 3617, 43867, 283, 617, 131, 593, …)や既知の非正則素数かを照合。
> - 該当 ⟹ **重み $k$ と $p_0$ の対**を記録し、A 側の同 $(p_0,k)$ の値と突き合わせる(**A で異常がなく S だけ異常なら、それが研究者の指摘した当のケース**)。
> - 非該当 ⟹ 小さい素数(2,3,5,7…)なら模型の分母由来を疑う。
> 6. **Sol 監査**: 上記 1–5 の記録一式を添えて Sol へ。**司令塔の裁定前に「発見」と呼ばない。**
> 7. **blind 規律**: $k=13$ 以降の値について**予測を書かない**。本票は条件文のみで書いてある。

---

# 6. 【GAP】・novelty・帰属

## 6.1 未閉の穴

| # | 内容 | 重さ |
|---|---|---|
| **【T-GAP-1】** ★ | **(H-LAT)**: $\mathfrak t_k^{\mathbf Z}$ が自由で階数が $\mathrm{Witt}(3,k)+\mathrm{Witt}(2,k)$ であること。既在の較正は $\mathbf Q$ 上・次数 6 まで。$\mathbf Z$ 上・次数 12/13 は**未確認** ⟹ カナリア T-a で毎回検査 | ★ 大 |
| **【T-GAP-2】** ★ | **格子言明の限界**(§1.4)。【D-GAP-1】と同型。捩れゼロから「B 型不在」へは渡らない | ★ 大 |
| **【T-GAP-3】** | 段 T2 のコスト(基底ベクトルへの $\nu_k\circ j$ 適用)が線形で済むかは**未実測**。§4.3 の $\sigma_{13}$ 覆しはこれに条件つき | 大 |
| **【T-GAP-4】** | $p=2,3$ は射程外(§2.3)。完全版は $M_k$ 全体で回す必要 | 中 |
| **【T-GAP-5】** | $\mathrm{rank}\,H_k$ の厳密値は未計算(概算 $\mathrm{Witt}(2,k)/3$ のみ)。段 T1 の出力で確定 | 小 |
| **【T-GAP-6】** | 本ノートの全命題は **candidate(単系統・Sol 未監査)**。**定理 TOR-1 / TOR-S3 / 系 TOR-2 を確定として引用しない**。判定語の発効は司令塔専権 | — |

## 6.2 novelty grep(実施済・`docs/` `provenance/` `sol/` 全域)

| 語 | hit |
|---|---|
| `TOR-SWEEP` / `TOR-1` / `TOR-S3` / `TOR-2` / `TOR-DET` / `QUAR-TOR` / `H-LAT` / `P-T-` | **0**(本ノート初出) |
| `単因子` / `Smith` / `elementary divisor` | **0** ⟹ 整捩れの道具立ては工房初出 |
| `Maschke` / `捩れ素数` | **0** |
| $\nu_k$ / $\mathfrak t=\mathrm{gr}(K(0,5))$ / $\rho$ / $j$ | 既在(`b_type_synthesis_design_v1.md`・`_addendum_edim56_*`・`edim_semidirect_model_design_v1.md`・`hs_prop7_translation_v1.md`)⟹ **定義は借用・整構造化が新規** |

## 6.3 帰属

- **批判と方針**: 研究者(逐語「A で異常が出てからじゃないと S を調べないなら、異常が S にしかいなかったら見逃す」)。委嘱: 司令塔(裁定 726)。骨子(整数版制約行列の単因子で捩れ素数を悉皆する着想・RDV-1 の S 側移植)も司令塔。
- **本ノートの新規部分**: 定義 LAT と仮定 (H-LAT) / **定理 TOR-1**(判定式の正確形と格付け)/ **定理 TOR-S3**($p\ge5$ で $S_3$ ブロックは無捩れ)/ **系 TOR-2**(判定が $\nu_k\vert_{H_k}$ 1 本に還元・行数 $\approx\mathrm{Witt}(2,k)/3$)/ **アルゴリズム TOR-DET**(本命側が因数分解不要)/ 実行可能性表と $k\ge15$ 圏外の明示 / **§4.3 の $\sigma_{13}$ 覆し**(F-GAP-3 非依存かつ F-GAP-3 を不要にしうる)/ 手順 QUAR-TOR。
- 既在(引用): $\mathcal S_k$ の定義・$\nu_k=\sum\rho^i$・$\mathfrak t=\mathrm{gr}(K(0,5))$・$j$・半直積較正($K(0,5)\cong F_3\rtimes F_2$、$\mathrm{Witt}(3,k)+\mathrm{Witt}(2,k)$)/ 【D-GAP-1】/ 裁定 706 の E-DIM 実測(k=11: 662 秒 627 MiB;k=12 見積 100–120 分 6–9 GiB)/ packed int64 工事。

## 6.4 次の一手(優先順・司令塔裁定用)

1. ★★★ **段 T0–T3 を $k=11$ で走らせる**(最安の一手)。$k=11$ は E-DIM 実測 662 秒の既知点なので**直接比較**でき、【T-GAP-3】(段 T2 のコスト)と (H-LAT) が同時に決まる。**ここが TOR-SWEEP と重み 16($\sigma_{13}$)の両方の生死を決める。**
2. ★ **段 T4 を $k\le12$ で**($k=9,10,11,12$)。**P-T-1 の検定** — 捩れゼロなら「$k^*\ge13$ は S の意味で全素数無条件(格子言明)」へ格上げ請求。
3. **$k=13$** は 1・2 が通ってから。**$\dim\mathcal S_{13}(\mathbf Q)$ と $\sigma_{13}$ が副産物で出る**(blind 規律: 値の予測は書かない)。
4. **ep-keeper への確認 2 件**: (a) 既存 E-DIM 実装は語 ambient($3^k{+}2^k$)を使っているか(Lyndon 基底なら 12 倍の節約)。(b) 「$H_k$ の基底像だけを組む」再定式化は現行 pipeline に載るか。**載るなら E-DIM 本体のコストも下がる。**
5. **Sol 便への積荷候補**: 定理 TOR-S3 + 系 TOR-2 + アルゴリズム TOR-DET を 1 束で。**走らせる前に監査を通せば、出た値がそのまま使える。**
6. §1.4 の格付け(格子言明)を**地図と台帳に先に登録**しておく — 捩れゼロが出たときに過大主張しないための予防。
