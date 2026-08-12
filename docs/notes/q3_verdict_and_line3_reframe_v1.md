# (Q3) 結審 — $N'$ は**非 isolated** + ③ 線の形の再定義(裁定 1065)

作成: 数学者(Opus 5)/ 2026-08-13 / 入力 = cert `q3_m1_v1_20260813.json`(12d3efad・witness $u=3407$)
前提 = `iso_family_lemma_v1.md`(SETTLE-AUTO)・`q3_decision_design_v1.md`(§3 の論理鎖)・`q3r1_lift_spec_v1.md`
⚠ $u$/$c$ 非接触・prereg 非抵触。**格: candidate**(Sol 未監査)。

---

## §0 結審

$$\boxed{\ N'=\ker(B_3\to\tilde H)\ \textbf{は}\ \textbf{非 isolated}\ \ (\text{candidate})\ }$$

⟹ **$GT(N')$ は群にならず、$\rho_{N'}$(群準同型)は存在しません**。正典的にあるのは**集合写像 $a_{N'}$ まで**。

---

## §1 witness の独立検証(すべて PASS)

$$v'=\begin{pmatrix}121362&169410\\0&356118\end{pmatrix},\quad u'=\begin{pmatrix}441037&6442\\350246&36444\end{pmatrix}\pmod{691^2},\quad u=3407$$

| 検査 | 結果 |
|---|---|
| $v'^3=I$、$\det v'=1$ | ✔ |
| $u'^2=I$、$\det u'=-1$ | ✔ |
| $u'=v'\,\sigma_1^{3407}$ | ✔ |
| $T(\sigma_1)=v'^{-1}u'=\sigma_1^{3407}$ | ✔($v'^{-1}=v'^2$) |
| $u=3407\notin\{1,\,47678\}$($=\pm1\bmod47679$) | ✔ |

---

## §2 ★★ 生成性(最後のピース)— **確定**

### 2.1 mod 691 で Dickson の 4 除外(すべて通過)
$\bar u'=\begin{pmatrix}179&223\\600&512\end{pmatrix}$(位数 2・$\det=-1$)、$\bar v'=\begin{pmatrix}437&115\\0&253\end{pmatrix}$(位数 3・$\det=1$)。

| 除外 | 検査 | 結果 |
|---|---|---|
| **(a) Borel** | 共通固有点:$\bar u'$ は $\{279,484\}$、$\bar v'$ は $\{\infty,604\}$ ⟹ **共通なし** | ★ 排除 ✔ |
| **(b) トーラス正規化群(非原始的)** | $\bar v'$ は位数 3 ⟹ 対を保つなら両点を固定 ⟹ 保たれうる対は $\{\infty,604\}$ のみ。$\bar u'$ による像は $\{36,584\}$ ⟹ **不変でない** | ★ 排除 ✔ |
| **(c) 例外型 $A_4/S_4/A_5$** | $\mathrm{ord}(\bar u'\bar v')=138$ ⟹ $PSL$ 内で位数 $\ge34>5$ | ★ 排除 ✔ |
| **(d) 部分体** | 691 は素数 ⟹ 真の部分体なし | ★ 排除 ✔ |

$$\Longrightarrow\ \langle\bar u',\bar v'\rangle\supseteq SL(2,691),\quad \det\bar u'=-1\ \Longrightarrow\ \langle\bar u',\bar v'\rangle=SL^{\pm}(2,691)$$

### 2.2 mod $691^2$ への持ち上げ(非分裂論法)
reduction が $SL^\pm(2,691)$ を生成 + $\mathfrak{sl}_2$ は既約($p\ge5$)⟹ 極小正規 ⟹ $\langle u',v'\rangle\cap\mathfrak{sl}_2\in\{1,\mathfrak{sl}_2\}$。$=1$ なら補元 ⟹ 分裂 ⟹ **系統 C の非分裂に矛盾** ⟹
$$\langle u',v'\rangle=SL^{\pm}(2,\mathbf Z/691^2)$$

### 2.3 ★★ $\tilde H$ への全射性 — **自動**(S2-GAP-3 型の穴が閉じます)
$\pi\circ T=\pi$(便 121 A7.1)⟹ 像 $M$ は $S_3$ に全射 ✔ かつ $SL^\pm(2,\mathbf Z/691^2)$ に全射 ✔(§2.2)。
$\ker(\tilde H\to SL^\pm)\cong A_3=C_3$ ⟹ $M\cap A_3\in\{1,C_3\}$。
- $M\cap A_3=1$ なら $M\cong SL^\pm(2,\mathbf Z/691^2)$ で $S_3$ へ全射 ⟹ ⚠ **不可能**:$SL(2,\mathbf Z/p^2)$ は完全 ⟹ 全射 $SL^\pm\to S_3$ は $SL$ を $[S_3,S_3]=A_3$ へ送り、完全群の像は完全 ⟹ 自明 ⟹ $SL\le\ker$ ⟹ 商は $C_2$ の商 ⟹ $S_3$ になれない ✘

$$\boxed{\ \Longrightarrow\ M\cap A_3=C_3\ \Longrightarrow\ M=\tilde H\quad\textbf{★ 全射は自動}\ }$$

### 2.4 ★ charming も自動
charming の 2 条件のうち **$fN_{F_2}\in[Q,Q]$** は、$Q=SL(2,\mathbf Z/691^2)$ が**完全**ゆえ $[Q,Q]=Q$ ⟹ **自明に成立** ✔
残るは $u\in(\mathbf Z/N_{\rm ord})^\times$ ⟹ $u=3407$ は $47679=3\cdot23\cdot691$ と互いに素 ✔

### 2.5 ★ $f$ が $PB_3$ 側に取れること
$T(\sigma_2)\sim\sigma_2^u$ の共役元 $g$ の $S_3$-成分が互換 $\alpha_2$ でも、$g=\sigma_2h$($h\in PB_3$)と書けば
$$g\sigma_2^ug^{-1}=\sigma_2h\sigma_2^uh^{-1}\sigma_2^{-1}=h'\sigma_2^uh'^{-1},\qquad h':=\sigma_2h\sigma_2^{-1}\in PB_3$$
($PB_3\trianglelefteq B_3$ かつ $\sigma_2$ と $\sigma_2^u$ は可換)⟹ ★ **$f:=h'^{-1}\in PB_3$ が取れる** ✔

---

## §3 ★★★ 結審の論理鎖(逐語)

> 1. $[m,f]$($u=3407$)は **hexagon を満たす**(構成:$u'^2=v'^3=1$ ⟹ $B_3\to\tilde H$ が $c\mapsto1$ で定まる・§1)。
> 2. **charming**($u\in(\mathbf Z/47679)^\times$ ✔ / $[Q,Q]=Q$ ゆえ $f$ 条件は自明 ✔・§2.4)。
> 3. **全射**(§2.1–2.3)⟹ ★ **$[m,f]$ は GT-shadow**。
> 4. **前フィルタ**(cert `q3_r1_prefilter_v1`):$u\notin\{\pm1\}$ ⟹ $\bar x^{\,u}\not\sim\bar x$ ⟹ $\bar T$ は $Q$ の自己同型になり得ない ⟹ **well_defined 不可**。
> 5. **SETTLE-AUTO の対偶**:well_defined でない ⟹ $N_{F_2}\not\subseteq\ker T$ ⟹ $\ker T\ne N'$ ⟹ **非 settled**。
> 6. ⟹ **非 settled な shadow が存在** ⟹ ★ **$N'$ は非 isolated**。∎

**格**: ★ **candidate**。
- **機械側**(witness の存在・$\det$・位数・生成性の Dickson 検査)= GAP + 私の python の**二系統一致** ⟹ ★ **cross-checked**
- **紙側**(SETTLE-AUTO・前フィルタの trace 機構・§2.2–2.5)= **単系統(私)・Sol 未監査**
$$\boxed{\ \textbf{有限計算核は cross-checked、定理全体は candidate}\quad(\text{M121-7 の伝播禁止を遵守})\ }$$

**条件(逐語)**:(i) 前フィルタの trace 判定が正しいこと(cert `q3_r1_prefilter_v1`)(ii) SETTLE-AUTO(`iso_family_lemma_v1.md` §1)(iii) $\mathfrak{sl}_2$ の既約性($p\ge5$)(iv) 系統 C の非分裂。

★ **census との整合**: 83 窓 census では **15 窓中 13 窓が非 isolated**。⟹ 本結果は**その標準的な側**に落ちており、**例外的な事態ではありません**。

---

## §4 ★★ ③ 線の形の再定義(非 isolated 分岐)

### 4.1 失われるもの / 残るもの
| TYPE-IMAGE$^\rho$ の五対象 | 非 isolated での状態 |
|---|---|
| (1) marked target $T_N=GT(N)$ + marking | ★ **集合として残る** ✔ |
| (2) $\rho_N$(群準同型) | ✘ **消える** ⟹ 集合写像 $a_{N'}$ のみ |
| (3) 像 $A_N\le GT(N)$ | ✘ 部分**群**でない ⟹ ★ **部分集合としては残る** |
| (4) 核体 $L_N$ | ⚠ $a_{N'}^{-1}(1)$ が部分群かは要確認【L3-GAP-1】 |
| (5) 局所分岐 $S_N$ | (4) に依存 ⟹ 同じ |

$$\boxed{\ \textbf{★ 段 2 の群論成果(容器・非分裂拡大・braid 全射 }B_3\twoheadrightarrow\tilde H\textbf{)は}\textbf{完全に無傷}\ }$$
理由: それらは **$\tilde H$ 側(braid の群論)**の言明で、$GT(N')$ の型とは**独立**だからです。

### 4.2 ★★★ 代替枠の中核 — **settled 部分は群をなす**

> **【命題 SETTLED-GRP】(candidate)** $GT^{\rm settled}(N):=\{$settled な shadow$\}$ は $GT(N)$ の中で**群をなす**。
> **証明スケッチ**: SETTLE-AUTO より settled ⟺ $\bar T$ が $Q$ の**自己同型**。合成 (3.53) は $T$ の合成に対応し、自己同型の合成は自己同型 ⟹ 閉じる。単位 $[0,1]$ は恒等 ⟹ settled。逆射 (3.54) は逆自己同型 ⟹ settled。∎

⟹ ★★ **$GT^{\rm settled}(N')\hookrightarrow\mathrm{Aut}(Q)$**(自己同型群への埋め込み)⟹ **群として扱える土俵が残ります**。

### 4.3 代替五対象(設計素描)
| # | 代替対象 | 測れるか |
|---|---|---|
| **(1′)** | marked target = $GT(N')$(**集合**)+ ★ **$GT^{\rm settled}(N')$(群)** | ✔ |
| **(2′)** | $a_{N'}:G_\mathbf Q\to GT(N')$(集合写像)+ ★ **像が $GT^{\rm settled}$ に入るかの判定** | ★ 入れば**そこで群準同型として扱える** |
| **(3′)** | 像 $a_{N'}(G_\mathbf Q)$(部分**集合**)+ **サイズ** | ✔ ★ **サイズ会計(TRIAD 型)は集合水準で意味を保つ** |
| **(4′)** | $a_{N'}^{-1}(1)$(部分群か要確認) | 【L3-GAP-1】 |
| **(5′)** | 局所分岐 | (4′) 依存 |

### 4.4 (Q4)(Q5) の変形
| 旧 | ★ 新(非 isolated 版) |
|---|---|
| **(Q4)** $A_{N'}$ が $GT(N')$ を覆うか(**crown 検定**) | ⚠ **SURG バッテリーは使えません**($A\Phi=X$ は $A$ が部分群であることを要する)⟹ ★ **(Q4′)「$\lvert GT(N')\rvert$ と $\lvert a_{N'}(G_\mathbf Q)\rvert$ のサイズ会計」+「像が $GT^{\rm settled}$ に入るか」** |
| **(Q5)** 拡大類が $G_\mathbf Q$ 側で実現されるか(R-1) | ★ **不変**(R-1 は OPEN のまま)— ただし比較の土俵が (2′) になる |

$$\boxed{\ \textbf{★ 反例探索の観点では有利}\ :\ \textbf{非 isolated は「}GT(N')\setminus a_{N'}(G_\mathbf Q)\ \textbf{が非空」を}\textbf{集合水準で}\textbf{直接問える}\ }$$
⟹ ★ **crown 検定(群の枠)を失う代わりに、サイズ会計(集合の枠)が主装置になります** — これは札 I-CEX-1 の「サイズ会計」扉と同じ道具立てです。

---

## §5 GAP・次の一手

- **【L3-GAP-1】(中・新)** $a_{N'}^{-1}(1)$ が部分群か(⟹ 核体 $L_{N'}$ が定義できるか)。$\mathrm{Ih}$ は群準同型・$\mathcal{PR}_{N'}$ が集合写像 ⟹ 合成の逆像の構造は要確認。
- **【L3-GAP-2】(中・新)** 命題 SETTLED-GRP の**厳密証明**(合成 (3.53) と $T$ の合成の対応を逐語で)。⟹ ★ 代替枠の土台なので**優先**。
- **【Q3-GAP-2】★ 不要化**(ISO-RIGID$^{\rm w}$ は非 isolated 確定により迂回)。
- **【S2-GAP-3】★ 閉鎖**(§2.3 の全射自動性)。
- ★ **次の一手(推薦)**: **L3-GAP-2(SETTLED-GRP の証明)** ⟹ これが立てば ③ 線は「$GT^{\rm settled}(N')$ を土俵にする」形で**再出発**でき、段 2 の成果がそのまま接続します。
- **申告**: 私の側は python 行列演算のみ(GAP 走行ゼロ)・$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**。
