# S4 = PSL(2,8) 窓($k=9$)での SURJ 押し込み **v2**

**状態札: candidate — `paper-proof (framework-conditional) / 1-bit reduction: Sol 条件付き PASS(便 86 F86-4.1.3)`**
起草: Claude(数学者レイヤー・Opus 5)/ 2026-07-30
**v1 → v2 の根拠**: 裁定 227 / **P86-5**(便 86 の局所修理 4 件)。v1(`surj_s4_v1.md`・SHA `659163bd…9356e`)は**上書きせず保存**。

**v1 → v2 差分一覧**

| # | P86-5 項 | v1 | v2 |
|---|---|---|---|
| **A** | 1 | (W5$^{\mathbb Q}$) の「位数 56 は極大ゆえ Borel」= **循環**(便 86 NOTE 1) | **§3.6 を Sylow 2/7 の完全証明に差し替え**(Dickson は元の位数のみ引用)+ GAP 独立確認 |
| **B** | 2 | 固定体を「9 次巡回」と書いた | **$[\,K((u^{-1})^{1/9}):K\,]=\mathrm{ord}([u^{-1}]_9)\in\{1,3,9\}$ と正記**(§4) |
| **C** | 3 | SD-c は scratchpad 単系統・未 commit / S4 settled は本文引用のみ | **証明書 2 通に収蔵**(§7・§3.5)。SD-c は `search/certs/sdc_twist_W_E_A10_9t1_20260730.json` を新規生成、S4 settled 54 件は `certificates/S4.v2.json` を**再走で再現確認** |
| **D** | 4 | 「$(Z_{18}$-link$)$ は手続き」と書きつつ定理文は素で提示 | **定理 SURJ-S4 の札を `framework-conditional` に固定**(§0・§4)。$(Z_{18}$-link$)$ 完了までこの札を外さない |
| **E** | — | — | **新規発見(§7.3)**: `settled_fail_count` は**走査集合相対**の量。梯子証明書の `=0` は Ξ 制限下(486 走査)の値で、悉皆走査(1,814,400)では $m=0$ 層だけで **45** 件。SD-a の射程がさらに縮む |

**依拠**: v1 と同一(BFC v2.15 / $R^{\rm cyc}_{\rm formal}$ = W3-13 / 定理 A₅ = W3-8 / `week3-PSL封印計算_opus_v1.md` §5.4 / `week4-E2作戦_v1.md` / `phifam_v1.md` §2 / `surj_d4_t1_v1.md`)+ 便 86 `sol/sol_reply_86_math13.md` §4.1。

> ## 封印遵守
> **$u_{S4}$ の値には触れない**(§5 は測定**計画**まで)。$K^{(5)}$ 非接触。公開値($A_5$ の $u^{-1}=-2$、$K^{(3)}$ の $u=-4$)は先例の形を示すためにのみ使用。

---

## 0. 判定(v2)

$$\boxed{\ \textbf{前件は揃う。1 ビット帰着は成立。札は }\texttt{framework-conditional}\ \textbf{に固定(}(Z_{18}\text{-link})\textbf{ 未完)。}\ }$$

$$\boxed{\ \mathrm{Ih}_{S4}\ \text{全射}\iff\mathrm{ord}\bigl([u^{-1}]_9\bigr)=9\iff u^{-1}\notin K^{\times3},\qquad K=\mathbf Q(\zeta_{18})=\mathbf Q(\zeta_9)\ }$$

**前件の内訳**: (W2)群・**(W3)(W4)(W5)(W5$^{\mathbb Q}$)**(6′)は紙上証明(v2 で (W5$^{\mathbb Q}$) の循環を解消)/ (W2)算術半・(CAL) は窓非依存 / **(W1) のみ機械測定依存**(ただし壁窓とは別実装・別身分 — §3.5)/ $(Z_{18}$-link$)$ は**手続き未了**。

---

## 1. 窓データ(v1 §1 と同一・再掲は要点のみ)

$P=\mathrm{PSL}(2,8)$、$\lvert P\rvert=504=2^3\cdot3^2\cdot7$、$M:=\mathrm{ord}(X)=9$、$N_{\rm ord}=9$、$2M=18$、$\varphi(18)=6$、$K=\mathbf Q(\zeta_{18})=\mathbf Q(\zeta_9)$、$e=\lvert\mathfrak F_0\rvert=54/6=9$。**$M=e=9$。** charming set $=\{0,2,3,5,6,8\}$、$\{2m+1\bmod18\}=(\mathbf Z/18)^\times$。$\lvert\mathrm{GT}(N)\rvert=54$、`n_m_uniform` $=9$、`phi_image` $=N_{\mathrm{P\Gamma L}(2,8)}(\langle X\rangle)=\mathrm{Hol}(\mathbf Z/9)$、`phi_bijective: true`。

---

## 2. 道具(v1 §2 と同一)

**補題 Φ-univ(窓非依存)**: $\Phi$ は共変な準同型。証明は `phifam_v1.md` §2 の計算が座標も $n$ の奇偶も使わないことによる。⟹ **【GAP-06a】を紙で閉鎖**。(便 86 F86-4.1.3 が「Φ-univ の共変性」を紙上 PASS として採択。)

---

## 3. 前件の逐項確認

§3.1–§3.4・§3.7 は **v1 のまま**(便 86 が紙上 PASS と判定)。以下は v2 で変更・補強した箇所のみ。

### 3.1 (W3)・3.2 (W4)(再掲・変更なし)

$H:=$ Borel(点安定化群、位数 56)、$[P:H]=504/56=9=M$。$\langle X\rangle$(位数 9・非分裂トーラス)は $\mathbf P^1(\mathbf F_8)$ の 9 点上**固定点自由**(位数 3 の元も $\mathbf F_4\cap\mathbf F_8=\mathbf F_2$ より固有値が $\mathbf F_8$ に無い)⟹ **単純推移** ⟹ (W4) ✓。$N_P(H)=H$ ⟹ (W3) ✓(§3.6 の証明が $H=N_P(U)$ を与えるので自己正規化も従う)。

### 3.3 $\mathfrak F_0\cong C_9$(補題 F0・変更なし)

$\Phi_{0,f}(X)=X$ ⟹ $\Phi(\mathfrak F_0)\subseteq C_{\mathrm{Aut}(P)}(X)=\langle X\rangle$、$\Phi$ 単射・$\lvert\mathfrak F_0\rvert=9=\lvert\langle X\rangle\rvert$ ⟹ $\mathfrak F_0\cong C_9$ かつ $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X\rangle)$。
**v2 の補強**: $C_{\mathrm{Aut}(P)}(X)=\langle X\rangle$(位数 9)は `certificates/S4.v2.json` の **`centralizer_witness.order = 9`** として証明書に載っている(v1 は本文引用のみだった)。再走で再現確認済(§7.2)。

### 3.5 (W1)— 身分の明確化【v2 で補強】

`certificates/S4.v2.json` の `settled_count = 54` / `settled_detail` 54 件。**その意味論**(便 86 F86-4.1.2 が指摘し、私も `search/week3-psl-common.g` L371–390 を読んで確認):

```gap
for sh in result.shadows do
  targetX := Xperm^u;;  targetY := AbstractProd([f^-1, Yperm^u, f]);;
  for e in cfg.autElements do
    h := e.perm;;
    if h^-1*Xperm*h = targetX and h^-1*Yperm*h = targetY then witness := e; break; fi;
  od;
```

すなわち **$T_{m,f}$ を実現する実際の自己同型 $h\in\mathrm{Aut}(\hat G)$ を探索**している。$X,Y$ が $P$ を生成するので、witness の存在は $T_{m,f}$ が単射(自己同型)であること、したがって $\ker T_{m,f}=N$ を与える。**これは定義ノート §3 の settled そのもの**である。

$$\boxed{\ \textbf{S4 の settled は壁 judge の }\texttt{settled\_fail\_count}\ \textbf{(well-definedness)とは別物であり、真の settled である。}\ }$$

⚠ **ただし 2 点を明記する**:
1. **機械測定であって定理ではない**。$K^{(n)}$ 族では isolated は正典 Thm 4.3 の**定理**だった。
2. **証明書自身は `"isolated": "UNKNOWN"` と書いている**(`week3-psl-common.g` L452 のハードコード)。`week4-E2作戦_v1.md` の isolated 表が `true` と記すのは、その 54/54 settled から**人が導いた**読みである。**証明書の欄と文書の表が食い違っている**ので、台帳では「settled 54/54(証明書)⟹ isolated(導出・人手)」と二段で書くべき。**v1 はこの区別をしていなかった — 自認。**

### 3.6 (W5) と (W5$^{\mathbb Q}$)【v2 で全面差し替え — P86-5 項 1】

**(W5)**(変更なし): §3.3 より $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X\rangle)\subseteq\mathrm{Inn}(P)$、$\Lambda$ は $P$-共役類全体ゆえ $\mathrm{Inn}(P)$-安定 ✓。

**(W5$^{\mathbb Q}$)**: v1 は「指数 9 ⟹ 極大 ⟹ 位数 56 の極大部分群は Borel に限る」と書いた。**便 86 NOTE 1 のとおり最後の一歩が循環である**(「Borel に限る」が未証明)。以下に差し替える。

> ### 補題 W5Q-S4(位数 56 の部分群の決定)
> $P=\mathrm{PSL}(2,8)$ の位数 56 の部分群は、**ちょうど Sylow 2-部分群の正規化群**(= Borel)であり、それらは単一の $P$-共役類をなす。

**使う標準事実(Dickson の部分群分類は使わない)**:
> **(E)** $P=\mathrm{PSL}(2,8)$ の元の位数は $1,2,3,7,9$ のいずれか。
> (標準: 標数 2 ゆえ非自明 unipotent は位数 2、半単純元は分裂トーラス $C_{q-1}=C_7$ か非分裂トーラス $C_{q+1}=C_9$ に属す。Dickson の**元の位数**についての標準事実であり、部分群分類は不要。GAP で確認済 — §7.4。)

**証明.**
**(1) $H\le P$、$\lvert H\rvert=56=2^3\cdot7$ とする。$n_7(H)=8$ である。**
Sylow より $n_7(H)\equiv1\ (\mathrm{mod}\ 7)$ かつ $n_7(H)\mid8$、よって $n_7(H)\in\{1,8\}$。$n_7(H)=1$ と仮定すると Sylow 7-部分群 $T\trianglelefteq H$。$H/C_H(T)\hookrightarrow\mathrm{Aut}(C_7)\cong C_6$ で $\gcd(56,6)=2$ ゆえ $[H:C_H(T)]\in\{1,2\}$、すなわち $\lvert C_H(T)\rvert\in\{56,28\}$。いずれも偶数なので $C_H(T)$ は対合 $t$ を含む。$t$ は位数 7 の元と可換だから $P$ に**位数 14 の元**が存在する — **(E) に矛盾**。ゆえに $n_7(H)=8$。

**(2) $H$ は Sylow 2-部分群を唯一もつ。**
(1) より $H$ は位数 7 の元を $8\cdot(7-1)=48$ 個もつ。残りは $56-48=8$ 個。Sylow 2-部分群は位数 8 で位数 7 の元を含まないから、この 8 元の集合と一致する。とくに Sylow 2-部分群は**一意**、すなわち $U_H\trianglelefteq H$ で $H\le N_P(U_H)$。

**(3) $\lvert N_P(U)\rvert=56$($U\in\mathrm{Syl}_2(P)$)。**
$H\le N_P(U_H)$ より $56\mid\lvert N_P(U_H)\rvert$。$504$ の約数で 56 の倍数は $56,168,504$、対応する $n_2(P)=[P:N_P(U)]$ は $9,3,1$。$n_2=1$ なら $U\trianglelefteq P$ で単純性に反する。$n_2=3$ なら剰余類作用 $P\to S_3$ の核は単純性より $1$ となり $504\le6$ で矛盾。ゆえに $n_2(P)=9$、$\lvert N_P(U)\rvert=56$。

**(4) 結論.** (2)(3) より $H=N_P(U_H)$。Sylow の定理で $\mathrm{Syl}_2(P)$ は単一共役類、$U\mapsto N_P(U)$ は共役同変な単射だから、位数 56 の部分群は**単一の共役類**をなす。それは点安定化群(位数 $504/9=56$)を含むので、その共役類 = Borel の類である。$\blacksquare$

> **系 W5Q-S4′.** 指数 9 の部分群は位数 56 ゆえ補題 W5Q-S4 より Borel。したがって $\Lambda$(= $H$ の $P$-共役類)は**「指数 9 の部分群全体」という純群論的条件で特徴づけられる**。任意の $\sigma\in\mathrm{Aut}(P)$ は指数を保つので $\Lambda$ を保つ。
> $$\boxed{\ \textbf{(W5}^{\mathbb Q}\textbf{) 成立 — 循環は解消した。}\ }$$
> **付随**: (3) より $N_P(H)=H$(= (W3))も同じ計算から出る。

**機械独立確認**(§7.4): GAP が `ConjugacyClassesSubgroups` で「位数 56 の部分群の共役類はちょうど 1 個・類の大きさ 9・IdGroup [56,11]・$=N_P(\mathrm{Syl}_2)$」および「指数 9 の部分群の共役類はちょうど 1 個」を返した。**紙の結論と一致。**

### 3.7 (6′)(変更なし)

$\rho_0$ 忠実・$\rho_0(\mathfrak F_0)=\tau(\mu_M[e])$。$\Lambda\cong P/H$ 上で $\Phi(\mathfrak F_0)=\mathrm{inn}(\langle X\rangle)$ は左移動として作用し、$\langle X\rangle$ は単純推移ゆえ忠実。$e=M=9$ より $\mu_M[e]=\mu_9$ ✓。**盲点定理チェック**: $\ker(\Phi\vert_{\mathfrak F_0})=1$ ⟹ SCHEMA-OUT ではない ✓。

### 3.8 枠組前件【v2 で札を固定 — P86-5 項 4】

| 前件 | status |
|---|---|
| (CAL) | ✅ 窓非依存に証明済($A_5$ v4 §1.4) |
| (TB1)(TB2)(TB3) | retained framework |
| exact (TB4) | `Z-norm-seal/v1` が global に供給(W3-21) |
| **$(Z_{18}$-link$)$** | ⚠ **per-window・S4 は inventory に未登録** ⟹ 補題 B-6($b_{\rm op}=1$)は S4 では `not_assessed` |
| A3 | 未閉(別線・全窓共通) |

$$\boxed{\ \textbf{⟹ 定理 SURJ-S4 の札は }\texttt{framework-conditional}\ \textbf{に固定する。}(Z_{18}\text{-link})\ \textbf{完了まで外さない。}\ }$$

### 3.9 前件表

| # | S4 | 供給 | 型 |
|---|---|---|---|
| (W1) | ✅ | settled 54/54(**真の settled** = 自己同型 witness・§3.5)+ 補題 W1-a + (CAL) | **機械測定**(定理ではない) |
| (W2) 群 | ✅ | §3.4(SURJ-Split (a) + charming 全単射 + §3.3) | 紙 |
| (W2) 算術 | ✅ | 補題 SURJ-Split (b) | 紙・窓非依存 |
| (W3) | ✅ | 補題 W5Q-S4 (3) | **紙(v2 で強化)** |
| (W4) | ✅ | §3.2 | 紙 |
| (W5) | ✅ | §3.6 | 紙 |
| (W5$^{\mathbb Q}$) | ✅ | **補題 W5Q-S4 + 系(v2 で循環解消)** | **紙** |
| (6′) | ✅ | §3.7 | 紙 |
| (CAL) | ✅ | $A_5$ v4 §1.4 | 紙・窓非依存 |
| $(Z_{18}$-link$)$ | ⚠ | 未登録 | 手続き |

---

## 4. 1 ビット帰着【v2 で次数を正記 — P86-5 項 2】

> ### 定理 SURJ-S4(**framework-conditional** candidate)
> **前件**: (TB1)(TB2)(TB3)(TB4)+**$(Z_{18}$-link$)$**+(CAL)+(W1)(W2)(W3)(W4)(W5)+(6′)。$K=\mathbf Q(\zeta_{18})=\mathbf Q(\zeta_9)$、$M=e=9$、$u\in K^\times$ を窓 $(P,H)=(\mathrm{PSL}(2,8),\text{Borel})$ の cusp 主係数(補題 B-5 (ii))とする。
> $$\boxed{\ \mathrm{Ih}_{S4}:G_{\mathbf Q}\to\mathrm{GTSh}(N,N)\cong\mathrm{Hol}(\mathbf Z/9)\ \text{全射}\iff\mathrm{ord}\bigl([u^{-1}]_9\bigr)=9\ }$$
> **固定体**: $L:=K\bigl((u^{-1})^{1/9}\bigr)$ は全射性によらず定まり、
> $$\boxed{\ [L:K]\ =\ \mathrm{ord}\bigl([u^{-1}]_9\bigr)\ \in\ \{1,\,3,\,9\}\ }$$
> **9 次巡回になるのは全射の場合に限る**(便 86 NOTE 2 — v1 の「9 次巡回」は無条件形として誤り。**自認・訂正**)。対応表:
>
> | $\mathrm{ord}([u^{-1}]_9)$ | $[L:K]$ | $\lvert\mathrm{Ih}(G_{\mathbf Q})\rvert$ | 判定 |
> |---|---|---|---|
> | 1 | 1($L=K$) | 6 | 非全射 |
> | 3 | 3 | 18 | 非全射 |
> | 9 | 9(巡回) | 54 | **全射 = genuine** |

**位数条件の初等化**: $\mathrm{ord}([u^{-1}]_9)=9\iff u^{-1}\notin K^{\times3}$。

> **系 4.1**(変更なし). $u^{-1}\in\mathbf Q^\times$ が有理数の 3 乗でなければ $\mathrm{ord}([u^{-1}]_9)=9$、すなわち全射。
> **証明.** $u^{-1}=y^3$($y\in K$)なら $\mathbf Q(y)\subseteq K=\mathbf Q(\zeta_9)$ はアーベル拡大の部分体ゆえ正規。$[\mathbf Q(y):\mathbf Q]=3$ なので共役 $\zeta_3y$ を含み $\zeta_3\in\mathbf Q(y)$、$2\nmid3$ で矛盾。$\blacksquare$

**先例**: $A_5$ 窓($M=e=5$)は $u^{-1}=-2$ で全射・固定体 $\mathbf Q(\zeta_5,\sqrt[5]2)$(W3-8)。$K^{(3)}$ は $u=-4$(W3-11)。**2 件とも $u^{\pm1}\in\mathbf Q^\times$** — ただし**これは予想であって証明ではない**(§8【S4-c】で凍結を提案)。

---

## 5. $u_{S4}$ の測定計画(v1 §5 と同一)

M0 窓の再構成(封印 JSON の $S,T$ から)→ **M1 ordered passport**($0$ 上は $(9)$ が先験的に確定・$1,\infty$ 上は要計算)→ M2 Riemann–Hurwitz で種数 → M3 Belyi 写像の構成(**passport は M3 の前に凍結**)→ M4 $P_0$ と $K$-有理 uniformizer → M5 $\lambda=u\,s^9(1+O(s))$ から $u$ → **M6 判定**($u^{-1}\in K^{\times3}$ か)→ M7 第二系統照合。

**期待コスト**: $A_5$ 窓(次数 5)の 1 段上。$g=0$ なら 1 変数有理関数の係数連立。

---

## 6. 【SD-a】の再確認(v1 §6・判定不変)

`kerchi-judge.g` の `settled_fail_count` は $T_{m,f}$ の **well-definedness**(裁定 169 KJ-1)であって $\ker T_{m,f}=N$ ではない。judge のソース自身が「genuine isolated-ness は本キャンペーンでどこでも独立検証されていない」と明記(既出 **GAP-4**)。**便 86 F86-4.1.2 が PASS 判定。** ⟹ **壁窓の (W1) は UNKNOWN**。**§7.3 でこの射程がさらに縮んだ。**

---

## 7. 証明書の収蔵【v2 新規 — P86-5 項 3】

### 7.1 SD-c 証明書(新規生成)

`search/certs/sdc_twist_W_E_A10_9t1_20260730.json`(schema `sdc-twist/v1`・生成 `search/sdc-twist-a10-9t1.g`)。

| 欄 | 値 |
|---|---|
| 窓 assert | `|Bq| = 10886400`・`|P| = 1814400 = |A10|`・`ord_x = ord_y = 9`・`c_in_N = true`・`N_ord = 9`(**kerchi-judge と独立に再現**) |
| $C_{S_{10}}(X)$ | **9** $=\lvert\langle X\rangle\rvert$ |
| $N_{S_{10}}(\langle X\rangle)$ | **54**、IdGroup **[54,6]**(= 測定済 GTSh の IdGroup と一致) |
| 走査 | `scan_mode = exhaustive_over_P`、`scanned = 1814400`(**悉皆**) |
| $\mathfrak F_0$ | `F0_size = 9`(梯子証明書の `ker_size = 9` と一致) |
| $j$ 表 | `j_values = [0,8,6,5,1,7,3,2,4]`、`j_table` に $f$ の置換表示つき 9 行 |
| 結論欄 | `phi_F0_into_inn_X = true`、`phi_F0_bijective_onto_inn_X = true` |
| `all_pass` | **true** |

**⟹ 便 86 NOTE 3 の「監査可能な証明書が無い」は解消。** ただし札は **measured candidate(単系統 GAP)**のまま — cross-checked へは上げない(第二系統なし)。

### 7.2 S4 settled 54 件(既存証明書の再現確認)

`certificates/S4.v2.json`(git 追跡済・schema `gtsh-cert/v2-psl`)に `settled_count = 54`・`settled_detail` 54 件(各 `{m, f_word, settled, automorphism_witness}`)が**既に収蔵されている**。v2 で `.\gap.ps1 search\week3-psl-S4.g` を**再走**し:

* `settled witness search: 54/54 settled`
* `candidate_total=3024 h10_fail=2640 h11_fail=330 generation_fail=0 shadow_total=54`(排他整合 ✓)
* `C_Aut(w): order=9`(= §3.3 の $C_{\mathrm{Aut}(P)}(X)=\langle X\rangle$ の機械確認)
* 再走出力と git HEAD 版の差分は **`runtime.wall_seconds` の 1 欄のみ**(`settled_detail` 54 件・`centralizer_witness` はビット同一)

$$\boxed{\ \textbf{S4 settled 54 件は versioned certificate に収蔵済・再走で再現確認。}\ }$$

### 7.3 ★ 新規発見 — `settled_fail_count` は**走査集合相対**の量

SD-c の悉皆走査が副産物として次を出した:

| 経路 | 走査候補数 | $m=0$ 層の settled 不合格数 |
|---|---|---|
| 梯子証明書(`scan_mode = xi_restricted`) | 486 | **0** |
| SD-c(`exhaustive_over_P`) | 1,814,400 | **45** |

両者は**受理集合については一致する**(`F0_size = 9` ↔ `ker_size = 9`、梯子側は `26_naive_shadow_digest = 27_xi_shadow_digest` で naive/Ξ 一致も記録)。食い違うのは**棄却された候補の数**だけであり、それは走査した候補集合に依存する量である。

> ### FINDING S4-9(v2 新規)
> $$\boxed{\ \texttt{settled\_fail\_count = 0}\ \textbf{は「この窓に ill-defined な候補が無い」を意味しない。}\ }$$
> 意味するのは「**走査した候補集合の中に**無い」だけである。Ξ 制限下では 0、悉皆では($m=0$ 層だけで)45。
> **⟹ SD-a の射程がさらに縮む**: v1 で私は「`settled_fail_count` は well-definedness であって isolated ではない」と言ったが、正しくは「**走査集合に相対的な** well-definedness 不合格数であって isolated ではない」。
> **⚠ 便 86 F86-2.1 への註**: 「各窓 settled fail 0」を GAP と SymPy で cross-checked と認めた判定は、**両系統が同じ Ξ 候補集合を走査している限り正しい**(同じ量を二系統で測った)。本 FINDING はその判定を覆さず、**その量が何であるかの語法**を正すものである。台帳には「Ξ 候補集合における settled 不合格 0」と書くべきで、「窓に ill-defined 候補なし」と書いてはならない。

### 7.4 (W5$^{\mathbb Q}$) の機械独立確認

GAP(`PSL(2,8)` を直接構成・使い捨て・scratchpad):

```
|PSL(2,8)| = 504   factors = [[2,3],[3,2],[7,1]]
|Sylow_7| = 7   |N_P(T)| = 14
|Sylow_2| = 8   |N_P(U)| = 56   n_2 = 9
conjugacy classes of subgroups of order 56 : 1
   class size = 9   IdGroup = [56,11]   = N_P(Syl2)?  true
conjugacy classes of subgroups of INDEX 9 : 1
```

**紙の補題 W5Q-S4 と全項一致。** ⚠ これは事後の裏取りであり、§3.6 の証明は機械計算に依存しない。

---

## 8. FINDING と未閉鎖(v2)

| # | 種別 | 内容 |
|---|---|---|
| **S4-1** | 成立 | 前件が揃い **1 ビット帰着が成立**(便 86 条件付き PASS)。札は **framework-conditional** |
| **S4-2** | 道具 | **補題 Φ-univ** で【GAP-06a】を紙で閉鎖 |
| **S4-3** | 一般化 | **補題 F0** = 命題 K5-1 の族外一般化 |
| **S4-4** | 分水嶺 | (W4) 成立の境界は「$M\ge$ 最小忠実置換次数」。S4 は $M=9=\lvert\mathbf P^1(\mathbf F_8)\rvert$ でちょうど成立 |
| **S4-5** | 【SD-a】 | 判定不変(便 86 PASS)。§7.3 で射程がさらに縮む |
| **S4-6** | 【SD-c】 | $a=+1$。**証明書に収蔵**(§7.1)。札は measured candidate |
| **S4-7** | procedural | $(Z_{18}$-link$)$ 未登録。$K^{(3)}/A_5$ と同格の pending |
| **S4-8** | **修理完了(v2)** | (W5$^{\mathbb Q}$) の循環を **Sylow 2/7 の完全証明**で解消(§3.6)+ 機械確認 |
| **S4-9** | **新規(v2)** | `settled_fail_count` は**走査集合相対**(§7.3)。台帳の語法修正を要請 |
| **S4-10** | **語法(v2)** | 証明書は `"isolated": "UNKNOWN"`、文書の表は `true`。**二段(settled 54/54 は証明書 / isolated はそこからの人手の導出)で書くべき**(§3.5) |

### 未閉鎖・次の一手

* 【S4-a】**$(Z_{18}$-link$)$ の window inventory 行の起票**(手続き・司令塔案件)。$K^{(3)}/A_5$ の pending 解消と同便で処理するのが効率的。
* 【S4-b】**予言先行の凍結**: 測定前に系 4.1 と「先例からの予想 = 全射」を凍結。的中判定が M6 で自動的に付く。
* 【S4-c】測定発注(§5 の M0–M7)。**M1(passport)を M3 の前に凍結**。
* 【S4-d】**§7.3 の台帳語法修正**: 梯子 13 窓の `settled_fail_count = 0` を「Ξ 候補集合における」と限定して記帳。
* 【S4-e】**§3.5 の証明書/文書の食い違い**の整理(`week4-E2作戦_v1.md` の isolated 表 vs 証明書の `"isolated":"UNKNOWN"`)。
* 【S4-f】本稿は**紙上・単系統・framework-conditional**。**Lean 検証ではない。** $u_{S4}$ の値には触れていない。$K^{(5)}$ 非接触。
