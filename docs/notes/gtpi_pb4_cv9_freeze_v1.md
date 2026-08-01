# PB₄ 線 — CV-9 主検問用 IF-FIRST 凍結宣言 $^{PB_4}$ v1(手 2)

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01・司令塔 GO(初動 3 手)の**手 2**
- **本ファイルは手 3 の計算前に固定する。結果によって書き換えない**(改訂は v2)。
- effective source: **裁定 370**(falsifier 非当事者判読・(α) 確定)+ **読解ノート v1.1** + `papers/2008.00066-what-are-gt-shadows.pdf`
- 前提の確定事項(裁定 370): probe の窓 6 元は $\rho=\pi\circ\mathrm{Rev}$ の像・`X13w` $=$ 正典 (A.5) の $x_{12}^{-1}c\,x_{23}^{-1}$・$c\in\ker\pi$(位数 1)・$\lvert Q_P\rvert=7500$ は 360 通り中 1 通り。

> **記号規律**: $PB_4$ 線の対象は右上に $^{PB_4}$ を付す。主線($K^{(n)}$ 族・$K_\pi$・$\mathcal G$)と物理的に別記号(2405 Remark 1.2 の同名別物)。

---

## 0. この凍結が殺しにいく事故

**f/f⁻¹ 族 5 件目は、私自身の対照実験の中で起きた**(裁定 370・gate ノート ERRATUM)。fwd 規約の生成元を rev 規約の行順に流し込み、well-defined ですらない写像から「60」という偽の反証値を出した。
⟹ 本凍結は **(b) well-definedness 検査の同梱を必須条件**とし、**本実験と対照実験の両方**に適用する。

---

## 1. 入力 universe(CV-9-1 ①)

### 1.1 $PB_4$ 窓

$$\pi:B_4\to E,\qquad \sigma_1\mapsto s_1,\quad\sigma_2\mapsto s_2,\quad\sigma_3\mapsto s_1 .$$
**$E$ 内で braid 関係を満たす $\sigma_3$ の像は一意**(手 1 実測: 候補ちょうど 1 個・$t=s_1$)。$\pi$ が $B_4$ 全体に延びるので
$$N_0:=\ker\pi\cap PB_4\ \in\ \mathrm{NFI}_{PB_4}(B_4)\qquad(B_4\text{-正規性は自動}).$$

### 1.2 shadow の宇宙

正典 2008 Def 2.19 + (2.4) より、shadow は $(m,f)\in\mathbb Z/N_{\rm ord}\times F_2/N_{F_2}$、$N_{F_2}=N_{PB_3}\cap F_2$、$N_{PB_3}$ は (2.4) の 5 本引き戻しの交叉。charming は $f\in[F_2/N_{F_2},F_2/N_{F_2}]$。
**事前登録**: $F_2/N_{F_2}=Q_F$(位数 1500)、$[Q_F,Q_F]=A$(**位数 60**)、$m\in\{0,1,3,4\}$ ⟹ **240 候補**。P6-1 と同額。

### 1.3 competitor universe(CV-9-5)

source の競合先は「$PB_4$ の指数 60 以下の部分群」ではなく、**$\lvert\langle(\pi(A_{ij}),T(A_{ij}))\rangle\rvert$ が取りうる値の全体**(60 なら核一致・>60 なら不一致)。settled 判定は 20 行それぞれで独立に 2 値。

---

## 2. 比較対象(CV-9-1 ②)

### 2.1 $T^{PB_4}_{m,f}$ の逐語(正典)

2008 の $T^{B_4}$(txt 行 979–987):
$$T(\sigma_1):=\sigma_1x_{12}^{m}N,\qquad T(\sigma_2):=\phi_{123}(f)^{-1}(\sigma_2x_{23}^{m})\phi_{123}(f)N,\qquad T(\sigma_3):=\phi_{12,3,4}(f)^{-1}(\sigma_3x_{34}^{m})\phi_{12,3,4}(f)N .$$
$\sigma_1x_{12}^m=\sigma_1^{2m+1}$、$\sigma_2x_{23}^m=\sigma_2^{2m+1}$、$\sigma_3x_{34}^m=\sigma_3^{2m+1}$。

### 2.2 ★ (a) pentagon の向き(司令塔 追加条件 (a))

**正典 (2.20) 剰余版(txt 行 906)逐語**:
$$\boxed{\ \phi_{234}(f)\ \phi_{1,23,4}(f)\ \phi_{123}(f)\ N\ =\ \phi_{1,2,34}(f)\ \phi_{12,3,4}(f)\ N\ }$$

**Rev 規約との対応(凍結)**: $\Psi=\Theta\circ\mathrm{Rev}$ は**反**準同型なので、積は順序反転で運ばれる。5 成分と 5 写像の対応を**確定的に固定する**:
$$v_1=\phi_{123},\quad v_2=\phi_{234},\quad v_3=\phi_{12,3,4},\quad v_4=\phi_{1,23,4},\quad v_5=\phi_{1,2,34}$$
(`cof[1]`$=(x_{12},x_{23},x_{13})$ = 素の包含 = $\phi_{123}$;`cof[2]`$=(x_{23},x_{34},x_{24})$ = $\phi_{234}$;`cof[3]`$=(x_{13}x_{23},x_{34},x_{14}x_{24})$ の rev = $\phi_{12,3,4}$;`cof[4]`$=(x_{13}x_{12},x_{34}x_{24},x_{14})$ の rev = $\phi_{1,23,4}$;`cof[5]`$=(x_{12},x_{24}x_{23},x_{14}x_{13})$ の rev = $\phi_{1,2,34}$)。

この対応のもとで、正典 (2.20) 剰余版の**語反転**は
$$\phi_{123}(f)\ \phi_{1,23,4}(f)\ \phi_{234}(f)\ =\ \phi_{12,3,4}(f)\ \phi_{1,2,34}(f)\quad\Longleftrightarrow\quad \boxed{\ v_1v_4v_2=v_3v_5\ }$$
であり、これは probe の `Pent` **逐語**である。
**⟹ 凍結: probe の `Pent` は正典 (2.20) 剰余版の Rev 版であり、両者の対応は上の 5 対応で与えられる。これを手 3 の probe で機械照合する(§3 P-PB4-2b)。**

### 2.3 共役の向き(T′ の教訓の $^{PB_4}$ 版)

正典は $\phi(f)^{-1}(\cdot)\phi(f)$。Rev 規約に運ぶと $v(\cdot)v^{-1}$ になる(`pent_settled_cent_v1.md` §6 の (U-rev) と同型の議論)。
**凍結: 主測定は $v(\cdot)v^{-1}$(整合)。混成 $v^{-1}(\cdot)v$ も併走して両方 cert に書く(判定しない・接触遮断)。**

### 2.4 settled の判定式(literal)

$$\text{settled}^{PB_4}(m,f)\ :\iff\ \ker\bigl(T^{PB_4}_{m,f}\bigr)\cap PB_4=N_0 .$$
**実装**: $\Xi:=(\pi,T_{m,f}):B_4\to E\times E$ とし
$$\text{settled}^{PB_4}\iff \bigl\lvert\langle\,\Xi(A_{ij})\ :\ 1\le i<j\le4\,\rangle\bigr\rvert=\lvert\pi(PB_4)\rvert=60 .$$
(核が一致 $\iff$ 対写像の像が対角的 $\iff$ 位数が増えない。)**GAP の写像積は使わない**(P6-1 §2.4 の規律を継承)。

### 2.5 Prop 3.3 の $N^\sharp$

$$N^\sharp:=\bigcap_{K\in\mathrm{Ob}(\mathrm{GTSh}^\heartsuit_{\rm conn}(N_0))}K .$$
**実装**: $PB_4/N^\sharp\hookrightarrow\prod_{[(m,f)]}PB_4/\ker T_{m,f}$ ゆえ
$$\lvert PB_4/N^\sharp\rvert=\bigl\lvert\langle\,(\,T_{m,f}(A_{ij})\,)_{[(m,f)]}\ :\ i<j\,\rangle\bigr\rvert\quad\text{in}\ E^{\lvert\mathrm{GT}^\heartsuit(N_0)\rvert}.$$

---

## 3. ★ (b) well-definedness 検査(司令塔 追加条件 (b)・裁定 370 教材の履行)

**probe に同梱し、これが落ちたら計算を続けない**(唯一の中断 assert。他はすべてログのみ)。

> **WD-1((A.5) 二表示一致・5 成分)**: 各成分 $i$ で、$x_{13}$ の 3 つの正典表示
> $$\sigma_2\sigma_1^2\sigma_2^{-1},\qquad \sigma_1^{-1}\sigma_2^2\sigma_1,\qquad x_{12}^{-1}c\,x_{23}^{-1}$$
> を**宣言した規約(Rev)で**評価し、$\mathrm{cof}[i][3]$ と一致することを assert。**5 成分すべて。**
>
> **WD-2(準同型性)**: 各成分 $i$ で $(x_{12},x_{23},c)\mapsto(\mathrm{cof}[i][1],\mathrm{cof}[i][2],\mathrm{cofc}[i])$ が $PB_3=F_2\times\langle c\rangle$ からの準同型であること = **$\mathrm{cofc}[i]$ が $\langle\mathrm{cof}[i][1],\mathrm{cof}[i][2]\rangle$ の中心にある**ことを assert。
>
> **WD-3(braid)**: $\pi$ の 3 像が $B_4$ の 3 関係を満たすことを assert。
>
> **WD-4(混成検出器・★ 識別力の証明)**: **fwd 生成元 × rev 行順**の組合せを作り、**WD-1 が落ちること**を確認する(落ちなければこの検査に識別力がない)。裁定 370 が指摘した私のバグ(`gtpi_pb4_gate_stdwindow_20260801.g` L35)を、この検査が実際に捕まえることの証明。

---

## 4. 同値関係・NF・filter・失敗状態(CV-9-1 ③④⑤⑥)

| 項目 | 宣言 |
|---|---|
| **③ 同値** | 部分群の **literal 一致**(GAP の `=`)。位数一致だけでは同一視しない。ただし settled 判定は §2.4 の位数 60 判定を用い、**別途 literal 核比較も併記**する |
| **④ NF** | $A_{ij}$ の語は標準形 $A_{ij}=\sigma_{j-1}\cdots\sigma_{i+1}\sigma_i^2\sigma_{i+1}^{-1}\cdots\sigma_{j-1}^{-1}$ に固定。$m$ は $\{0,1,3,4\}\subset\mathbb Z/5$ |
| **⑤ filter** | なし。20 行すべて・両共役向き |
| **⑥ 失敗状態** | (a) WD-1〜3 のいずれかが false ⟹ **Error() で中断**(唯一の中断点)。(b) $T_{m,f}$ が準同型に延びない ⟹ 行に `T_undefined` を記録し継続。(c) settled 判定は 2 値で記録・**期待値を probe に書かない** |

---

## 5. 予言(IF-FIRST・計算前に凍結)

> **P-PB4-1**: WD-1/2/3 は全成分・全項で **true**。WD-4(混成)は **false**(= 検査に識別力あり)。
> **P-PB4-2a**: (2.4) の 5 本引き戻し交叉 $N_{PB_3}(N_0)$ は $K_\pi$ に一致、$\lvert PB_3/N_{PB_3}\rvert=\mathbf{7500}$。
> **P-PB4-2b**: `Pent`($v_1v_4v_2=v_3v_5$)が正典 (2.20) 剰余版と §2.2 の 5 対応のもとで**逐語一致**。
> **P-PB4-3**: charming 宇宙 $=[Q_F,Q_F]$、**60 元**。$\mathrm{GT}^\heartsuit(N_0)$ は P6-1 の $\mathcal G$ と**同一の 20 行**。
> **P-PB4-4(本命)**: 整合規約($v(\cdot)v^{-1}$)で **20/20 が settled$^{PB_4}$** ⟹ **$N_0$ は isolated** ⟹ Prop 3.3 で $N^\sharp=N_0$、$\lvert PB_4/N^\sharp\rvert=\mathbf{60}$。
> **P-PB4-5**: 混成規約($v^{-1}(\cdot)v$)では settled 数が 20 未満に落ちる(規約の識別力)。
> **P-PB4-6(結論の予言)**: P-PB4-3 + P-PB4-4 が出れば、**定理 GTPI の $\mathcal G$ は正典の $\mathrm{GT}^\heartsuit(N_0)$ そのもの**であり、**LEVEL CAVEAT は解除される**($PB_3$ 実装模型水準 → $PB_4$ 水準)。
>
> **外れた場合の意味**: P-PB4-4 が外れれば $N_0$ は isolated でなく、Prop 3.3 の交叉で真に小さい $N^\sharp$ が出る — その $\lvert PB_4/N^\sharp\rvert$ が新しい測定値になる(打ち切り閾 $10^6$)。

---

## 6. 非当事者性の申告(CV-9-1.3.3)

**起草者は当事者である**(P6-1 の仕様・実装・一次 grading を書いた本人)。本凍結は主検問の**入力**であって主検問ではない。**主検問(falsifier)PASS まで cross-checked と書かない。**
参照 provenance: 裁定 370 / 読解ノート v1.1 / `docs/notes/gtpi_cv9_freeze_v1.md`(`b5b39698…19cd539c`)/ `docs/notes/gtpi_v1.md`(`0d8f7f90…bab9d5bf`)/ `search/certs/gtpi_closure_20260801.json`(`76178579…2bf683f35`)/ 2008 txt 行 591(2.4)・906(pentagon)・979–987($T$)・3678–3682((A.5))。

## 7. 司令塔 追加条件 (c) の扱い

**cc 空虚性**(現行較正族は全窓で $c$ 像自明 ⟹ $c$ 項実装が未検査)は本凍結の射程外とする。手 3 と並行で**新規較正窓 1 本(c 像非自明)**を組むのは、$\pi(c)\ne1$ となる $B_4$ 表現の探索を要し**本件より重い**。⟹ **便 98 に起票のみ**(§8 に文案)。**本測定の結論は「$c$ 項が未検査である」という射程宣言つきで出す。**
