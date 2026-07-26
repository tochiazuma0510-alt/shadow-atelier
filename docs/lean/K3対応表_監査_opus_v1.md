# 定理 K3 有限層 Lean 化 — **翻訳忠実性監査** v1(独立監査)

2026-07-27 / 監査者: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(Lean 翻訳忠実性監査)。**

**監査の性格**: カーネルが証明項を検査済みという前提のもと、「**Lean の主張が紙の補題と同じことを言っているか**」だけを見る。
- **証明項・tactic は一切読んでいない**(委嘱どおり)。読んだのは `theorem`/`def`/`abbrev` の**型と定義本体**のみ。
- 設計者・実装者の作業記録・意図は参照していない。参照した紙側は `docs/lean/K3対応表_v0.md`(v1)・`docs/week4-K3飽和_opus_v3.md`(v3.1+v3.2)のみ。
- **自前の独立検算**: `scratchpad/audit-k3lean.mjs`(node・25 項目)。Lean の定義を node で再実装し、(a) Lean にある主張が真か (b) **Lean に無い橋渡し命題が真か** を確認。**25/25 PASS**。

**対象**: `lean/K3/` の 8 ファイル(Base・Shadows・Counting・Lambda・Group・LambdaFull・Struct・CountingFull)。
**範囲外**: `lean/Marking.lean`(W3-5 で監査済)、および監査中に出現した **`lean/K3/Conjugator.lean`(F29・作成 01:56)**— 委嘱の 8 ファイルに含まれないため未監査(§5 に注記)。

---

## 0. 総合判定

> **全行 FAITHFUL ではない。要修正は 2 件(構造的)+ 軽微 5 件。ただし数学的な誤りは 1 件も無い。**

| 判定 | 件数 | 行 |
|---|---|---|
| **FAITHFUL** | 20 | F1 F2 F4 F5 F6 F7 F9 F10 F11 F12 F14 F15 F16 F18 F19 F22(下段) F25 F26 F32 定義層 D-A〜D-D・D-F |
| **DEVIATION** | 6 | **F3**(軽微)・**F8**(申告どおり)・**F13**(軽微)・**F20**(不足)・**F21**(構造)・**F23**(接続欠)・**F24**(定義化) |
| **VACUITY-RISK** | 2 | **F27**(ρ_Λ 未正当化)・**F22 の「正典 Thm 4.6 の独立確認」札** |
| **UNKNOWN** | 0 | — |
| **未実装(逸脱ではない)** | 1 | F17(設計上 `β`・Mathlib 側 F17′ に置く行) |

**要修正の 2 件(構造的・これだけが本監査の主眼)**

- **【D-1】$T$ と $\Phi$ が Lean 内で接続されていない**(§3.1)。`Shadows.lean` の 12 個の具体自己同型 `Phicf m k` と、`Counting.lean` の 12 元抽象群 `T` の間に**写像が一本も無い**。ゆえに F21/F22/F23/F24/F26/F27 は「**ある** 12 元群についての真理」であり、「$\Phi(\mathrm{GT}(K^{(3)}))$ についての真理」ではない。
  設計の忠実性ノート **(δ2)** が射程外と宣言しているのは「$T$ と**圏論的** GT の一致」であって、ここで欠けているのは**同じ Lean ファイル群の中にある `Phicf` との一致**であり、これは有限・完全に scope 内である。
- **【D-2】$\rho_\Lambda$ が二重定義で、$\S2.6$ 側(`rhoLam`)に正当化補題が無い**(§3.2)。`Lambda.lean` の `rhoF0`/`tauAct` には「共役が $H_c$ を $H_{\rho(c)}$ へ写す」ことの自己完結 decide 補題があるのに、`CountingFull.lean` の `rhoLam` には対応物が無い。F27 はその未正当化の写像に依存している。

**両者とも、私の独立検算では「主張は真・接続も真」である**(§4 の PASS 一覧)。すなわち**誤りではなく欠落**であり、**decide 補題 5〜6 本(いずれも 12×12 または 216 級)で閉じる**。

---

## 1. 定義層の監査(最重要)

正典実現 = `docs/notes/抽出_Kn定義_D1.md` 由来の (3.1)(3.6)(4.9)(4.12)、および `week4-K3飽和_opus_v3.md` §2.5 の逐語式。

| # | 定義 | 場所 | verdict | 根拠(手計算 + 独立検算) |
|---|---|---|---|---|
| **D-A** | `D = Fin 3 × Bool`・`dmul`・`dinv`・`done` | Base 13–25 | **FAITHFUL** | $r^as^e$ 表示。$e=0$: $(a+b,f)$ ✓ / $e=1$: $r^as\cdot r^bs^f=r^{a-b}s^{1\oplus f}$ ✓(`if a.2 then a.1-b.1`)。逆元 $(r^as)^{-1}=r^as$(対合)・$(r^a)^{-1}=r^{-a}$ ✓ |
| **D-B** | `E`・`emul`・`einv`・`eone`・`par`・`inG` | Base 16–40 | **FAITHFUL** | $D_3^3$ = (3.1) の値域。`par` = 3 成分 $e$-flag の xor、`inG = ker(par)` ✓。$H_c\subseteq G_3$ も自動(共役は flag 保存) |
| **D-C** | `xb`/`yb`/`zb` | Base 43–47 | **FAITHFUL** | (3.6) の**逐語リテラル**: $\bar x=(r,s,s)$, $\bar y=(rs,r,rs)$, $\bar z=(r^2s,r^{-1}s,r)$。$r^{-1}=r^2$ の変換も正しい。手計算で $\bar x\bar y\bar z=1$ を確認 ✓ |
| **D-D** | `um`/`kappa3`/`X3`/`alpha`/`Phicf`/`canonX`/`canonY` | Shadows 17–60 | **FAITHFUL** | **v3 §2.5 の boxed 式と表に逐語一致**。$\Phi(\bar x)=(r^{u_m},s,s)$・$\Phi(\bar y)=(r^{1-4k}s,\,r^{u_m},\,r^{1-2\kappa(m)}s)$ ✓。$\kappa$ の分岐 `if m%2=1 then m+1 else 3-m%3` は $m\in\{0,2,3,5\}$ で正典表 $(1,0)(2,1)(1,1)(2,0)$ を再現 ✓(検算 5) |
| **D-E** | `T`・`mulT`・`oneT`・`invT`・`chiT`・`inF0`・`vval` | Counting 18–51 | **DEVIATION** | 群としては正しい($\mathrm{Aff}(\mathbb Z/3)\times C_2$ の忠実な符号化・$vval$ の $\{1,2\}\leftrightarrow$ xor 対応も正しい)。**しかし $\Phi$ の像である証拠が Lean に無い** → 【D-1】 |
| **D-F** | `inHc`/`inH`・`g0`・`rhoF0`・`tauAct`・`mu6_3` | Lambda 18–53 | **FAITHFUL** | N2 の閉形そのもの。`inH = inHc done` は $v_3=v_1\wedge v_2\in\langle r\rangle$ に簡約 ✓。**`rhoF0_conj_correct`/`tauAct_conj_correct` が「共役の添字則」を自己完結で正当化しており、この 2 つは模範的** |
| **D-G** | `convElem`・`rhoLam` | CountingFull 22–32 | **VACUITY-RISK** | `alpha_is_conj`($\alpha_{v,t}=\mathrm{Ad}(\mathrm{convElem})$)は正しい。しかし **`rhoLam` が $\Lambda$ 上の作用であることを述べる補題が無い** → 【D-2】 |
| **D-H** | `epow6`/`pow3`/`allD`/`allE`/`allT`/`cosetAct`/`conjE`/`actSig`/`ordT`/`ordAff` | 各所 | **FAITHFUL**(注記つき) | `epow6 x j = x^j` ✓・`pow3 g a = g^a` ✓。`ordT` の「それ以外は 6」は `F22_order6_check` が正当化しており健全。**`allE`/`allT` の Nodup が未記載**(§3.3 A-1) |

> **★ 定義層の結論**: **正典実現との同一性は D-A〜D-D・D-F で完全に取れている**。$r^3=s^2=1$・$X=(r,s,s)$ 型・marking (3.6)・(4.9)(4.12) のすべてが逐語で入っており、**「定義が違えば全定理が別対象の真理」という最悪のシナリオは起きていない**。問題は $T$ 側(D-E)と $\rho_\Lambda$ 側(D-G)の**接続の欠落**に限局する。

---

## 2. statement 層 — 行ごとの verdict

### 2.1 基盤(Base.lean・Group.lean)

| 行 | Lean 定理 | verdict | 内容 |
|---|---|---|---|
| **F1** | `dmul_assoc`, `dmul_one_*`, `dmul_inv_*`, `F1_rel_r3/s2/srsr` | **FAITHFUL** | 表示 $\langle r,s\mid r^3,s^2,srs^{-1}r\rangle$ の 3 関係式が逐語で入っている。〔注〕「$r,s$ が $D$ を生成」は未記載 — 表示との同型は「関係式 + $\lvert D\rvert=6$ + 生成」で閉じるので、形式的には 1 行足りない(実害なし) |
| **F2** | `F2_assoc/one_left/one_right/inv_left/inv_right` | **FAITHFUL** | 成分に落とす設計どおり |
| **F3** | `F3_marking`, `F3_order_xb` | **DEVIATION(軽微)** | marking $\bar x\bar y\bar z=1$ は完全 ✓。**位数は $\bar x$ のみ**で、紙の「$\mathrm{ord}=6,6,6$」のうち $\bar y,\bar z$ が欠。$\bar x$ の論法($x^6=1\wedge x^2\ne1\wedge x^3\ne1$ ⇒ 位数 6)は正しい。$\bar y,\bar z$ も真(検算 4) |
| **F4** | `F4_par_hom` | **FAITHFUL** | 全 $x,y\in E$ ✓ |
| **F5** | `F5_card_G3` | **FAITHFUL**(アンカー注記) | `(allE.filter inG).length = 108`。**リスト長 = 集合の濃度**には `allE.Nodup` が要る(§3.3 A-1)。真(検算 1,2) |
| **F6** | `F6_G3_gen` | **FAITHFUL** | **全 $v\in E$ 上の $\leftrightarrow$**。右辺は $\bar x,\bar y$ の語のみ ⇒ $G_3=\langle\bar x,\bar y\rangle$ が両包含で出る。正典 p.15 の $J_q$ コセット分解と 1:1。**弱体化なし** |

### 2.2 $\Lambda$ と補題 P(a′)(LambdaFull.lean)

| 行 | Lean 定理 | verdict | 内容 |
|---|---|---|---|
| **F7** | `F7_one/closed/inv/subset_G3/card` | **FAITHFUL** | 部分群性 4 本 + $\lvert H\rvert=18$。$H\subseteq G_3$ も明示 ✓ |
| **F8** | `F8_index` | **DEVIATION(申告どおり)** | Lean は $108=6\times18$ の**数値等式のみ**。紙の $[G_3:H]=6$ は **Lagrange を Lean 外に置く**。$H\le G_3$ は F7 で確立済みなので数学的には同値だが、「剰余類が 6 個」という Lean 命題は存在しない。〔補足〕F10_distinct+F11_surjective が $\lvert\Lambda\rvert=6$ を与え、F9($N=H$)と併せれば軌道-固定群からも $[G_3:H]=6$ が出る(これも Lean 外) |
| **F9** | `F9_normalizer` | **FAITHFUL** | $g\in G_3\Rightarrow(gHg^{-1}\subseteq H\leftrightarrow g\in H)$。有限群で $\subseteq$ は $=$ と同値ゆえ $N_{G_3}(H)=H$ そのもの。**両向き**が入っており空虚でない |
| **F10** | `F10_conj_rule`(fwd+bwd)・`F10_distinct` | **FAITHFUL** | 申告の「全数 decide → D 成分の構造補題」は**同値な置換**。$\leftrightarrow$ の両方向が保存されている(bwd は `dconj_inj` で $g_3$-共役をキャンセル — 論理的に健全)。**`F10_distinct`($c\mapsto H_c$ の単射)が $\lvert\Lambda\rvert=6$ の要のアンカー**で、これがあるおかげで「$\Lambda$ を $D$ で添字づける」全ての命題(F11/F12/F32/F27)が置換の等式として読める |
| **F11** | `F11_injective`, `F11_surjective` | **FAITHFUL** | `tauAct i done` $=s^ir^{-i}$ が設計 N2 の $c_i$ と一致することを手計算で確認 ✓。単射+全射 = 単純推移(stabilizer 自明は単射から)。**v1 の誤りを構造的に回避**という設計意図どおり |
| **F12** | `F12_all_ramified` | **FAITHFUL** | 全 $g\in G_3$・全 $i\ne0$。$\langle\bar x\rangle=\{\bar x^i\}$ は $\mathrm{ord}(\bar x)=6$(F3)から ✓ |
| **F13** | `F13_permX_eq_tauAct1`, `F13_permY_cycle_type`, `F13_permZ_order6` | **DEVIATION(軽微・非対称)** | $\bar y$ は 6 点すべての像を書き下しており型 $2^21^2$ が**完全に決着** ✓。$\bar z$ は「$\mathrm{permZ}^i(p)\ne p\ (i=1,2,3)$ かつ $\mathrm{permZ}^6(p)=p$」で軌道長 6 ⇒ 型 $(6)$ が**論理的に閉じている** ✓。**$\bar x$ だけが `permX = tauAct 1` しか言っていない** — 6-サイクル性は F11 から従うが、そのための「`cosetAct` が作用」補題が Lean に無い(§3.3 A-4)。真(検算 12) |
| **F14** | `F14_core_mem/complete/card/image_order36` | **FAITHFUL** | **申告の「二重 ∀ → ¬∃ 書換え」は同値**($\lnot\exists g,(A\wedge B\wedge g\notin L)\leftrightarrow\forall g,A\to B\to g\in L$ は $L$ の membership が decidable ゆえ構成的に成立)。`F14_core_mem` が証人を与えるので空虚でない。$\lvert\mathrm{core}\rvert=3$ ⇒ $C_3$ ✓。`image_order36` は `eraseDups` なので `allE` の重複に**頑健**。紙の「6T9 という名前」を付けていない点も設計どおり ✓ |
| **F15** | `F15_one/closed/inv/subset_G3/card/meets_trivial/stabilizer_order2` | **FAITHFUL** | 反例として完全: $H'$ が部分群・$\lvert H'\rvert=18$・$H'\cap\langle\bar x\rangle=1$・にもかかわらず $\mathrm{Stab}=\{0,3\}$(位数 2)。**$\leftrightarrow(i=0\lor i=3)$ と両向きで書かれており、「位数 2 ちょうど」が言えている** ✓ |

### 2.3 $\Phi$ と (K4)(Shadows.lean)

| 行 | Lean 定理 | verdict | 内容 |
|---|---|---|---|
| **F16** | `F16_alpha_hom` | **FAITHFUL(むしろ強い)** | 設計は $v\in\{1,2\}$ だが Lean は**全 $v$**(=0 でも準同型なのは真)。強い方向の逸脱で無害 |
| **F17** | — | **未実装** | 設計上 `β`(Mathlib 側 F17′)。**逸脱ではない**。F19 が F17 を経由しないのは論理的に正しい(下記) |
| **F18** | `F18_closed_form_matches` | **FAITHFUL** | $m\in\mathcal X_3$・$k\in\mathbb Z/3$ の 24 等式。**`canonX`/`canonY` を `Phicf` から独立に書き下している**ので「閉形は仮定でない」という設計意図が statement 上で読める ✓。私が v3 §2.5 の boxed 式・表と逐語照合 ✓ |
| **F19** | `F19_injective`, `F19_injective_phicf` | **FAITHFUL(むしろ強い)** | **申告の「F6/F17 を経由しない直接 decide」は健全**。単射性の向きは「$(m,k)\ne(m',k')\Rightarrow$ 生成元像が違う $\Rightarrow$ **写像として**違う」であり、**拡張原理は要らない**(要るのは逆向き = 「生成元像が同じなら写像が同じ」で、それは (K4) には不要)。`F19_injective_phicf` は $E$ 全体上の 12 写像の相異性を与えるので $G_3$ 上の相異性より強い ✓ |
| **F20** | `F20_alpha_bij/v_nonzero/bijective/preserves_par/maps_G3_to_G3` | **DEVIATION(不足)** | 紙(v3 §2.5 強化 T7b)の主張は「**12 個が実際に $\mathrm{Aut}(G_3)$ の元**(準同型性の悉皆検査+全単射性)」。Lean にあるのは**全単射性($E$ 上)+ par 保存 + $G_3\to G_3$** だけで、**準同型性 $\Phi(xy)=\Phi(x)\Phi(y)$ がどこにも無い**。`F16_alpha_hom` + 成分構造から 3 行で出るが未記載。真(検算 8) |

### 2.4 群構造 $T$・$\tilde\chi$(Counting.lean・Struct.lean)

| 行 | Lean 定理 | verdict | 内容 |
|---|---|---|---|
| **F21** | `F21_assoc/one_left/one_right/inv_right/inv_left` | **DEVIATION(構造・【D-1】)** | 群公理は正しい。しかし紙の主張は「$T:=\Phi(\mathrm{GT}(K^{(3)}))$ **は位数 12 の群**」であり、Lean は (i) $\Phi$ との同定を持たず (ii) $\lvert T\rvert=12$ も述べていない(`allT_complete` は被覆のみ・長さ未記載)。**`mulT` が $\Phi$ の合成であることを言う命題がゼロ** |
| **F22** | `F22_order_counts/order6_check/Aff_is_S3/Aff_order3_check/center_card` | **FAITHFUL**(命題として)/ **VACUITY-RISK**(札として) | 位数分布 $[1,2^7,3^2,6^2]$・$Z$ の位数 2・$\mathrm{Aff}$ 側 $[1,2^3,3^2]$ — すべて真で、`ordT` の暫定値 6 を `F22_order6_check` で正当化する処理は**健全**(位数 4,12 を排除できている)。〔注 1〕「位数 6 の群の分類 ⇒ $S_3$」は Lean 外(明示されており可)。〔注 2〕**「正典 Thm 4.6 の**独立確認**」という設計の札は、$T$ と $\Phi$ が未接続である限り成立しない** — 現状は「ある 12 元群が $S_3\times C_2$」の確認にとどまる |
| **F23** | `F23_chiVal_bij` | **DEVIATION(接続欠)** | `X3.map chiVal = Z12x` は単射+全射を一撃で与える良い書き方 ✓。**しかし `chiVal : Fin 6 → Fin 12` と、counting で実際に使われる `chiT : T → Bool × Bool` が Lean 上で無関係**。「$\tilde\chi$ が円分指標である」ことが F26/F27 に接続していない |
| **F24** | `inF0` の定義 + `F24_chiT_hom/invT/ker_step` | **DEVIATION(定義化+アンカー欠)** | `inF0 x := chiT x = (false,false)` と**定義**したため、設計の「`inF0 a ↔ chiT a = 1`」は内容ゼロの恒真式になった(それ自体は無害・むしろ簡潔)。**問題は紙の (K2) の一部「$\mathfrak F_0\cong C_3$(位数 3)」がどこにも無い**こと。`F24_ker_step`(合成事実)は counting の中核として適切 ✓ |
| **F26** | `K3_counting` | **FAITHFUL** | 設計 §4.5 の擬似コードと**逐語 1:1**。仮定 3 本が紙 §2.4 の step 3(円分全射)・step 4(補題 P(d′))・部分群性に正しく対応。**$A$ を具体化しない抽象述語版**という (δ3) 忠実性が守られている ✓。仮定は充足可能($A\equiv\top$)なので空虚な前件ではない ✓ |
| **F27** | `F27` | **VACUITY-RISK(【D-2】)** | 命題「$\tilde\chi(t)=1\wedge\rho_\Lambda(t)=\mathrm{id}\Rightarrow t=1$」の形は紙 §2.6 と一致 ✓。**しかし `rhoLam` が $\Lambda$ 上の作用である保証が Lean に無い** — `rhoLam` は `convElem` による閉形として天下りに定義されただけ。$T$ 上の真の制約ではあるが、**「§2.6 の有限部分」という意味は担保されていない**。真(検算 17,18: `rhoLam(param(m,k))` は本当に $\Phi_{m,k}$ の $\Lambda$ 作用で、`rhoLam(param(0,k)) = rhoF0 k`) |

### 2.5 $\rho_0$・$\tau$ の窓実例(Lambda.lean)

| 行 | Lean 定理 | verdict | 内容 |
|---|---|---|---|
| **N4** | `N4_Phicf0_is_conj` | **FAITHFUL** | $\Phi_{0,k}=\mathrm{Ad}((r^k,1,1))$ を**全 $v\in E$ で**確認 ✓。手計算でも $\alpha_{1,-k}=\mathrm{Ad}(r^{-2k})=\mathrm{Ad}(r^k)$ ✓ |
| **F25** | `F25_faithful/fixed_point_free/order3_cubed/order3` | **FAITHFUL** | 忠実性(単射)・不動点なし・位数ちょうど 3(3 乗 = id かつ $\rho\ne$ id かつ $\rho^2\ne$ id)。∃ を具体証人 `done` で構成する処理も内容を変えていない ✓。紙 §2.6 の load-bearing 部分 |
| **F32** | `F32_E/G/H_subset/H_superset/I` | **FAITHFUL** | 委嘱の重点行(∃ 形)を精査した結果:**∃ 形は弱体化していない**。`∃ j, ∀ c, rhoF0 k c = tauAct j c` は「$\Lambda$($=D$、6 点)上の置換としての等式」であり、`F10_distinct` が $c\mapsto H_c$ の単射を保証しているので $D\cong\Lambda$ が成立し、**置換の等式そのもの**として読める。(H) は `subset`+`superset` の**両包含**で書かれており $\rho_\Lambda(\mathfrak F_0)=\tau(\mu_6[3])$ に過不足なし ✓。(I) の可換性も全 $k,j,c$ ✓ |

> **★ F32 について特記**: v3 §5.2.3 の★教材(「型 $3.3$ だけでは $\tau(\mu_6[3])$ を同定できない — $S_6$ に $C_3$ が 20 個ある」)への配慮が statement に効いている。Lean は**置換型ではなく写像の等式**で書いているので、教材が警告した同定失敗は構造的に起きない。

---

## 3. 総括所見

### 3.1 【D-1】$T$ と $\Phi$ の非接続(**要修正・最優先**)

`Shadows.lean` は 12 個の具体自己同型 $\{\Phi_{m,k}\}_{m\in\mathcal X_3,k\in\mathbb Z/3}$ を持ち、`Counting.lean` は 12 元の抽象群 $T$ を持つ。**両者を結ぶ写像も等式も Lean に一つも無い**。帰結:

| 紙の主張 | Lean が実際に言っていること |
|---|---|
| $T=\Phi(\mathrm{GT}(K^{(3)}))$ は位数 12 の群 | 型 `(Bool×Fin 3)×Bool` 上の `mulT` が群 |
| $\tilde\chi$ は円分指標 | `chiT` は第 1・第 3 成分の射影 |
| $\mathfrak F_0=\ker\tilde\chi$ は $\Phi_{0,k}$ たち | `inF0` は `chiT = (false,false)` |
| $A=T$(主定理の骨格) | ある抽象群の全体 |

**設計の (δ2) が免責しているのは「圏論的 GT との一致」だけ**であり、`Phicf` との一致は有限で完全に scope 内。**私の独立検算では次の 3 つがすべて真**である(検算 13–15):

- `param (m,k) := ((um m = 2, 1-4k-um m), 1-2·kappa3 m = 2)` は $\mathcal X_3\times\mathbb Z/3\to T$ の**全単射**
- `mulT (param m k) (param m' k')` に対応する自己同型 $=$ `Phicf m k ∘ Phicf m' k'`(**左作用・向きも一致**。設計 §9【GAP-L3】の懸案はこれで解消する)
- `chiT ∘ param` の 4 つの値は $m\mapsto 2m+1\bmod 12$ の 4 値と 1:1

⇒ **足すべきは 3 本**(いずれも 12×12 または 216 級の decide):
```
theorem T_param_bij   : ∀ m ∈ X3, ∀ k, …  -- param が全単射・|T| = 12
theorem T_mul_is_comp : ∀ m ∈ X3, ∀ m' ∈ X3, ∀ k k', ∀ x : E,
                          Phicf m k (Phicf m' k' x) = phiOf (mulT (param m k) (param m' k')) x
theorem T_chi_is_chiVal : ∀ m ∈ X3, ∀ m' ∈ X3, ∀ k k',
                          (chiT (param m k) = chiT (param m' k')) ↔ chiVal m = chiVal m'
```

### 3.2 【D-2】$\rho_\Lambda$ の二重定義(**要修正**)

`Lambda.lean` は**模範的**である — `rhoF0`/`tauAct` を閉形で定義した直後に、
```
rhoF0_conj_correct : ∀ k c v, inHc c v ↔ inHc (rhoF0 k c) (g0 k * v * (g0 k)⁻¹)
tauAct_conj_correct: ∀ j c v, inHc c v ↔ inHc (tauAct j c) (x̄ʲ * v * (x̄ʲ)⁻¹)
```
という**正当化補題**を置き、「この閉形は本当に $\Lambda$ 上の作用である」ことを自己完結で示している(docstring も「F10 を外部から仮定しない」と明言)。

`CountingFull.lean` の `rhoLam` には**この対応物が無い**。あるのは `alpha_is_conj`($\alpha_{v,t}$ が内部自己同型)と `rhoLam_hom`(準同型)だけで、**「$\Phi$ が $H_c$ を $H_{\rho_\Lambda(c)}$ へ写す」という肝心の命題が欠けている**。⇒ 足すべきは 1 本:
```
theorem rhoLam_conj_correct :
  ∀ m ∈ X3, ∀ k, ∀ c : D, ∀ v : E, inHc c v ↔ inHc (rhoLam (param m k) c) (Phicf m k v)
```
(私の検算 18 で真を確認。【D-1】の `param` を導入すれば同時に書ける。)
**副産物**: これを入れると `rhoLam (param 0 k) = rhoF0 k`(検算 17)も出て、**F27 の $\rho_\Lambda$ と F32 の $\rho_\Lambda$ が同一物であること**が Lean 内で確定する。現状はこれも未接続である。

### 3.3 非空虚性アンカーの充足状況

| # | アンカー | 状態 | 効く行 |
|---|---|---|---|
| ✓ | $\lvert G_3\rvert=108$ | `F5_card_G3` ✓ | 全体 |
| ✓ | $\lvert H\rvert=18$ | `F7_card` ✓ | F7 F8 |
| ✓ | $\lvert\Lambda\rvert=6$ | `F10_distinct`+`F11_surjective` ✓(実質的に成立) | F10 F11 F12 F32 |
| ✓ | $\Lambda$ 上の全単射(F11) | `F11_injective`+`F11_surjective` ✓ | 補題 P(a′) |
| ✓ | 12 個の $\Phi$ が相異 | `F19_injective_phicf` ✓ | (K4) |
| ✓ | $\lvert\mathrm{core}\rvert=3$・像 36 | `F14_core_card`+`F14_image_order36` ✓ | (P1) |
| ✓ | 反例の存在(F15) | `F15_*` ✓ | ★教材 |
| **A-1** | **`allE.Nodup`(または `allE.length = 216`)** | **欠** | F5・F7_card・F8・F15_card が「リスト長」であって「集合の濃度」でない。1 行(`by decide +kernel`)で閉じる |
| **A-2** | **$\lvert\mathfrak F_0\rvert=3$** | **欠** | (K2) の核・F24・F25 の「3 元の $\mathfrak F_0$」。`(allT.filter inF0).length = 3` の 1 行 |
| **A-3** | **$\lvert T\rvert=12$** | **欠**(`F22_order_counts` の和 $1{+}7{+}2{+}2$ から従うが未記載) | F21・F22・主定理の看板「位数 12」 |
| **A-4** | **`cosetAct` が作用**($\mathrm{cosetAct}(gh)=\mathrm{cosetAct}\,g\circ\mathrm{cosetAct}\,h$) | **欠** | F13 の $\bar x$ 6-サイクル性・$\tau$ が準同型であること(F32 の「$\tau(\mu_6)$」の群構造) |
| **A-5** | **`Phicf` の準同型性** | **欠** | F20 の「$\mathrm{Aut}(G_3)$ の元」 |
| **A-6** | **$\mathrm{ord}(\bar y)=\mathrm{ord}(\bar z)=6$** | **欠** | F3(紙は 3 元とも主張) |
| **A-7** | **`param` 3 本 + `rhoLam` 正当化 1 本** | **欠** | 【D-1】【D-2】 |

**A-1〜A-7 はすべて真**(§4 の独立検算で確認済み)。**合計 8〜9 本の decide 補題**で全部埋まる。

### 3.4 弱体化・空虚性・スコープずれの検査結果(委嘱の 4 つの疑い型)

| 疑い型 | 検査結果 |
|---|---|
| **弱体化**(生成元のみ検査 vs 全元) | **F20 で 1 件**(準同型性が生成元でも全元でも検査されていない = そもそも無い)。他は該当なし。F19 は生成元像だが**それが正しい定式**。F6・F9・F10・F14・F32 はすべて全元 |
| **空虚性**(空集合上の ∀・充足不能な前件) | **該当なし**。`∀ m ∈ X3`(4 元)・`v ≠ 0`(2 元)・`i ≠ 0`(5 元)・`ordT x = 6`(2 元)・`K3_counting` の仮定($A\equiv\top$ で充足)— すべて証人を確認した。`F14_core_complete` の $\lnot\exists$ も `F14_core_mem` が証人を与える |
| **スコープずれ**($G_3$ のつもりが $E$ 等) | **該当なし(良い方向のずれのみ)**。F9・F12 は `inG g →` を正しく置き、F19・F20・F10 は $E$ 全体で述べているが**これは強い方向**。$H_c\subseteq G_3$ も自動で保たれる |
| **量化の向き** | **該当なし**。F32 の `∃ j, ∀ c`(先に $j$ を選ぶ = 強い)・F11 の `∀ c, ∃ i`(全射)・F14 の $\lnot\exists$ — すべて意図どおり |

---

## 4. 独立検算(node・25/25 PASS)

`scratchpad/audit-k3lean.mjs`。Lean の定義を node で再実装し、Lean の主張と**Lean に無い橋渡し命題**の両方を検査した。

| # | 項目 | 結果 |
|---|---|---|
| 1–4 | $\lvert E\rvert=216$/Nodup・$\lvert G_3\rvert=108$・marking・**$\bar x,\bar y,\bar z$ の位数 6** | PASS |
| 5 | **`um`/`kappa3` が v3 §2.5 の表と一致** | PASS |
| 6–7 | F18(閉形 = 正典式)・F19(単射) | PASS |
| **8** | **[Lean に無い] `Phicf` は $E$ 上の群準同型** | PASS |
| 9–10 | $\lvert H_c\rvert=18$・$c\mapsto H_c$ 単射・F11 全単射 | PASS |
| **11–12** | **[Lean に無い] `cosetAct` が作用・`permX` が 6-サイクル** | PASS |
| **13–15** | **[Lean に無い] `param` 全単射・`mulT` ↔ `Phicf` 合成・`chiT` ↔ $2m+1$** | PASS |
| **16** | **[Lean に無い] $\lvert\ker\tilde\chi\rvert=3$** | PASS |
| **17–19** | **[Lean に無い] `rhoLam∘param(0,k)=rhoF0 k`・`rhoLam` が真の $\Lambda$ 作用・$\tau$ が $\rho_\Lambda$ の像に入る** | PASS |
| 20–24 | F14(core 3・像 36)・F22(位数分布・中心)・F23・F27 | PASS |
| 25 | F15(反例・Stab 位数 2) | PASS |

> **⇒ Lean が言っていることは全部真。Lean が言っていないことも全部真。本監査で見つかったのは「誤り」ではなく「欠落」である。**

---

## 5. 範囲外の注記

- **`lean/K3/Conjugator.lean`(F29)が本監査中に出現した**(01:56 作成・委嘱の 8 ファイルに含まれず**未監査**)。設計表 F29 行は **v1.1 で値と規約が訂正**され、v3.3 erratum も (P4) の conjugator リテラルを訂正している(v3 §2.2 本文の $h=[6,1,5,4,2,3]$ は**誤り**と明記済み)。**リテラル pin が必須・再導出禁止**という (δ1) 注記が効く行なので、**別途の忠実性監査を強く推奨**する(どの規約 (i)(ii)(iii) の下でのリテラルかを statement/docstring で追える必要がある)。
- 表 A(A1–A6)・表 B(B1–B6)・表 E(S1–S11)は ✗S 宣言どおり Lean に現れない ✓。**射程外宣言の逸脱は無い**。
- **F30✗**(部分群全列挙)が Lean に紛れ込んでいないことを確認 ✓(探索は Lean に入れないという設計規律が守られている)。
- 設計 §9【GAP-L3】(「$\rho_\Lambda$ を $T$ 上の写像として書くときの合成の向き」)は、**`rhoLam_hom` の形($\rho(xy)=\rho(x)\circ\rho(y)$ の左作用)と、検算 14(`mulT` = 写像合成)により整合が取れている**。ただし §3.1 のとおり Lean 内では未接続。

---

## 6. 修正提案(優先順)

| 優先 | 内容 | 規模 | 閉じる行 |
|---|---|---|---|
| **1** | **`param` 橋 3 本**(§3.1) | decide 3 本 | F21 F22(札)F23 F24 F26 |
| **2** | **`rhoLam_conj_correct` 1 本**(§3.2) | decide 1 本 | F27 の VACUITY-RISK |
| **3** | **`Phicf` の準同型性**(A-5) | 構造 3 行(F16 から) | F20 |
| **4** | **`allE.Nodup`・$\lvert\mathfrak F_0\rvert=3$・$\lvert T\rvert=12$**(A-1〜A-3) | decide 3 行 | F5 F7 F8 F21 F24 |
| **5** | **`cosetAct` の作用性**(A-4)+ `permX` の 6-サイクル直接検査 | decide 2 本 | F13 |
| **6** | **$\mathrm{ord}(\bar y)=\mathrm{ord}(\bar z)=6$**(A-6) | decide 1 行 | F3 |
| — | F8 の Lagrange を Lean 内に入れるか | 剰余類分割の実装(重い) | **不要と判断**(数値版で数学的に同値。ただし論文の対応表に「Lagrange は Lean 外」と書くこと) |

> **★ 監査者の総評**: 有限層の**定義は正典に忠実**で、$\Lambda$ 側(LambdaFull・Lambda)の statement 設計は**自己完結の正当化補題を置くという点で模範的**である。弱点は $T$ 側に集中しており、それは「$T$ をパラメータ空間として定義した」という設計判断そのものではなく、**そのパラメータ空間が何のパラメータ空間かを Lean 内で一度も言っていない**ことに由来する。上の優先 1・2(decide 4 本)で構造的な欠落は消える。
>
> **札への含意**: 現時点で「**定理 K3 の有限層が verified**」と書くのは**まだ早い**。書けるのは「$G_3$・$H$・$\Lambda$・$\Phi$ の窓データが verified」までで、**$\mathrm{GT}(K^{(3)})$ の群構造と counting 論法は「ある 12 元群についての verified」**にとどまる。優先 1 を入れれば「$\Phi$ の像としての $T$」まで格上げできる。
