# LOCAL-3 — $u_{\rm dih}$ アンカーと S9 符号規約台帳 v1

`DIR: 972 fake/証人の 1 ビット / FRAME: B₃-gentle・IDX3`
**委嘱**: 司令塔・裁定 1713 札 1(implementer が c′ 宣言を fail-closed 保留中)。
**正本**: `scratchpad/d972_idx3_arith_datum_independent_v1.md` §7.3(LOCAL-3・S1–S10・DC-1〜5 凍結済)。
**格**: §A = `paper-proof + 機械裏取り`(GAP + sympy)。§B = **規約台帳(宣言文書)** — 各項に「決定者」欄があり、**私が決めた項**と**cert/census を読まねば決まらない項**を峻別する。**未確定項は fail-closed。**
**著者**: 数学者(Opus 5)/ 2026-08-28。

> ### 規約 2 本(全文書共通)
> **(R-1)** 訂正は同ターンで本文に打つ(⚠ マーカ)。**(R-2)** `gate:` は述語を実際に評価した場合のみ・文書内の文字列検査は `doc-keyword:`。

---

# §A $u_{\rm dih}$ アンカーの実行(委嘱 (a))

## A.1 二面体側 cover の同定 — passport で一意に決まる

$K^{(9)}$ 側で 規約 D が要求するのは「**index-9 の cusp を持つ被覆**」である。二面体層の被覆は $D_9$(位数 18)の**次数 9 の作用**(点固定化群 = 鏡映 $C_2$)で与えられる。

```
gate: identify the dihedral degree-9 cover  (scratchpad/math_udih_v1.g)
  D9 order = 18   point stabilizer order = 2   index = 9
  degree-9 monodromy group = D18 order 18  transitive ? true
  Aut(cover) = N_G(Stab)/Stab : |N| = 2 => Aut order = 1
  involution cycle type = 2^4 (with 1 fixed point)
  #(sigma0 9-cycle, sigma1 invol, sigma_inf invol, product 1, generating) = 54
    up to conjugacy in G : 3       [ Out(D9) = C3 が 3 類を融合 => S9-類は 1 = rigid ]
  RH: sum(e-1) = 8+4+4 = 16 ; 2g-2 = -18+16 = -2  =>  g = 0
  cyclic C9 with (ord 9, ord 3, ord 3), product 1 : impossible (false)
```

**帰結 3 点**:
1. **passport は $(9;\,2^4 1;\,2^4 1)$、種数 0。**
2. **$\mathrm{Aut}(\text{cover})=1$** ⟹ **捻り(twist)がない**($H^1(G_{\mathbb Q},\mathrm{Aut})=1$)⟹ **ℚ-model は一意**(源の Möbius $s\mapsto\lambda s$ を除く)⟹ **$[u_{\rm dih}]\in\mathbb Q^\times/(\mathbb Q^\times)^9$ は曖昧さなく定まる**(NO-CANON (a) と整合)。
3. **巡回 $C_9$ の代替は存在しない**: index-9 点を持つ $C_9$-被覆で passport $(9,3,3)$ は $1+3(a+b)\equiv0\ (9)$ を要求し不可能。⟹ **二面体側の index-9 cusp を持つ被覆は上記 1 種類に限る。**

⟹ **この被覆は Chebyshev 写像 $T_9$**(次数 9・$\infty$ で完全分岐・$\pm1$ 上が $2^41$)。

## A.2 規約 D での $u_{\rm dih}$(機械計算)

規約 D:「index-$n$ cusp を $t=0$ の上に置き、$s$ を局所助変数、$u:=\lim_{s\to0}t/s^{n}$」。
$T_9$ の完全分岐点は $x=\infty\mapsto T_9=\infty$ なので、$\{\infty,1,-1\}\to\{0,1,\infty\}$ を送る Möbius で正規化する($s=1/x$)。

```
gate: Chebyshev normalisation  (sympy)
  T_9(x) = 256*x^9 - 576*x^7 + 432*x^5 - 120*x^3 + 9*x     leading coeff = 256 = 2^8
  T_9(x) - 1  = (x-1)(2x+1)^2(8x^3-6x+1)^2        multiplicities 1,2,2,2,2  = 2^4*1  ✓
  T_9(x) + 1  = (x+1)(2x-1)^2(8x^3-6x-1)^2        multiplicities 1,2,2,2,2  = 2^4*1  ✓
  mu' : (inf,1,-1)->(0,1,inf)   t = 2/(1 + T9(1/s))   u_dih = lim t/s^9 =  1/128
  mu  : (inf,-1,1)->(0,1,inf)   t = 2/(1 - T9(1/s))   u_dih = lim t/s^9 = -1/128
```

$$\boxed{\ u_{\rm dih}\ =\ \pm\,2^{-7}\ =\ \pm\tfrac1{128}\ }$$

- **残り 2 分岐点($1$ と $\infty$)のラベル付けは無害**: 2 通りで $u_{\rm dih}$ の**符号だけ**が変わり、$-1=(-1)^9=(-1)^3$ ゆえ $\mathbb Q^\times/(\mathbb Q^\times)^9$ でも $/(\mathbb Q^\times)^3$ でも**同じ類**。
- **源の $s\mapsto\lambda s$ も無害**: $u\mapsto\lambda^{-9}u$(NO-CANON (a))。

$$[u_{\rm dih}]_9=[2]^{-7}=[2]^{2},\qquad \boxed{\ [u_{\rm dih}]_3=[2^{-7}]_3=[2]^{-1}=[2]^{2}\ }$$

## A.3 ★ LOCAL-3 への訂正 — S4/S6/S7 は $\beta$ ではなく $u_{\rm dih}$ を使う

**§7.3.0 の設計原理**は「両窓の $u$ を**同一のレシピ**で計算し比を取る(向き convention は分子・分母に同じく効いて相殺)」である。ところが**現行 S4 は $S_\beta:=\mathrm{cube}(\beta)$、$\beta=2$(§3.1)を使っている**。

> ### ⚠ 訂正 C-A3(実装に直結)
> $\beta$ は**幾何の 規約 D ではなく、Kummer marking($\sigma_\kappa:\sqrt[9]\beta\mapsto\zeta_9\sqrt[9]\beta$)+ 正規化定数 $c\in(\mathbb Z/9)^\times$** で向きが決まる量である。$c$ は **§6.6 P-a で「未固定」**。⟹ **$\beta$ を使うと、アンカーで消すはずだった向きの自由度が別ルートから再流入する。**
> **正しい形**: S4 を
> $$S_{\rm anc}:=\mathrm{cube}(u_{\rm dih})\qquad(u_{\rm dih}=\pm2^{-7}\ \text{— 規約 D で計算済})$$
> に置換し、S6/S7 の $S_\beta$ を $S_{\rm anc}$ に置換する。**規約 D の反転は $u_{S4}$ と $u_{\rm dih}$ に同時に効く**ので、$c'=\log S_{u_{S4}}/\log S_{\rm anc}$ は**規約無依存**になる ✓(これが 7.3.0 の意図の正しい実装)。

**$\beta$ との関係(重要な観測)**: $[u_{\rm dih}]_3=[2]^{2}=[\beta]_3^{-1}$($\beta=2$ 前提)。
⟹ **アンカーは $\beta$ の「逆向き」に一致する。**$\beta$ をそのまま使う現行 S4 は **$c'$ を反転して返す**。§7.3.3 の予言表を書き直すと:

| 規約 D が採る量 | $S_u$ vs $S_{\rm anc}$ | **$c'$(訂正後)** | 現行表($\beta$ 使用)の値 |
|---|---|---|---|
| $u_{S4}=u_0$($[2]^2$) | $S_u=S_{\rm anc}^{1}$ | **$c'=+1$** | $-1$(反転していた) |
| $u_{S4}=u_0^{-1}$($[2]^1$) | $S_u=S_{\rm anc}^{2}$ | **$c'=-1$** | $+1$(反転していた) |

(mod 9 でも整合: Sol の「$[2]^7$ は $\beta{=}2$ 支持」に対し $[u_{\rm dih}]_9=[2]^{-7}$ — **ちょうど逆**。§6.5 の $3^6$ 成分のずれとは別要因。)

## A.4 残る 1 ビットと、その所在(**UNKNOWN・推測で埋めない**)

$c'$ を返すには **「ds4 の $u_0$ と $u_0^{-1}$ のどちらが 規約 D の $\lim_{s\to0}t/s^9$ か」** の 1 ビットが要る。

```
gate: search/certs/ds4_receipt_v1_20260812.json
  /d1_input_tamper_check/u0_inverse_read     = -1423828125/256
  /input_u0_inverse                          = -1423828125/256
  /sign_note/claim = "-1 = (-1)^9, so sign contributes trivially to the 9th-power class"
  /prerequisites_status/P5_u0_eq_uS4_identity = "unconfirmed ... NOT established by this script"
```
**cert は $u_0$ の定義(どちら向きが $t/s^9$ か)を宣言していない。**

- **私の読解(candidate)**: 正本 §7.2(NO-CANON)は $u(s):=(t/s^9)(P_0)$ と定義し、その実測値を $u_0$ と呼んでいる ⟹ **$u_{S4}=u_0$** ⟹ 上表より **$c'=+1$**。
- ⚠ **しかしこれは私自身のノートの語法からの読解であって、ds4 producer の実装規約の宣言ではない。**しかも **P5($u_0=u_{S4}$)は cert 自己申告で `unconfirmed`**。
- ⟹ **$c'=+1$ は `candidate(規約読解相対)`。**§B の宣言 **D-5** が埋まるまで **fail-closed**。

**必要な作業(1 行)**: ds4 producer(または受領票の生成コード)で「index-9 cusp を $t=0$ の上に置き $u=\lim_{s\to0}t/s^9$ を計算した値」が `u0` か `u0_inverse` かを**宣言として cert に追記**する。**幾何の再計算は不要。**

---

# §B S9 符号規約台帳(委嘱 (b)・**implementer の 2 系統実装がこれを消費する**)

**目的**: CV-9 型事故(規約差の二系統齟齬)の予防。**各項は「宣言」であり、両系統が同一宣言を消費したことを cert に記録する。**
**書式**: `決定者` = 数学者(本文書で確定)/ cert-reading(読めば決まる)/ census-reading(census を読めば決まる)/ **未確定(fail-closed)**。

| # | 項目 | 宣言(v1) | 決定者 | 違反の検出 |
|---|---|---|---|---|
| **D-1** | **規約 D(向き)** | index-$n$ cusp を **$t=0$ の上**に置き、$s$ を ℚ-有理局所助変数、$u:=\lim_{s\to0}t/s^{n}$。**両窓で同一**。残り 2 分岐点のラベルは自由(mod 3/mod 9 で無害・§A.2) | **数学者(確定)** | DC-1(向き flip で SELECT が入れ替わること) |
| **D-2** | **アンカー量** | **$S_{\rm anc}:=\mathrm{cube}(u_{\rm dih})$、$u_{\rm dih}=\pm2^{-7}$。**$\beta$ は**使わない**(§A.3 訂正 C-A3) | **数学者(確定)** | $\beta$ を使う実装は D-2 違反 ⟹ **cert に `anchor_source: "u_dih"` を必須欄化** |
| **D-3** | **$\mu_3(\mathbb F_p)$ の生成元** | 実装が選ぶ任意の位数 3 元 $g_p$。**ただし $\log S_{u_{S4}}$ と $\log S_{\rm anc}$ で同一の $g_p$ を使う** | **数学者(確定)** | DC-2(生成元 flip で $c'$ 不変) |
| **D-4** | **指数の向き** | $S_{u_{S4}}=S_{\rm anc}^{\,c'}$、$c'\in\{1,2\}$($2\equiv-1$) | **数学者(確定)** | 逆向き($S_{\rm anc}=S_u^{c'}$)にしても mod 3 では $c'^{-1}=c'$ ゆえ**無害**(記録のみ) |
| **D-5** | ★ **$u_{S4}$ の同定** | **未確定**: `u0` か `u0_inverse` のどちらが $\lim_{s\to0}t/s^9$ か | **cert-reading(要追記)** | **未確定の間は $c'$ を宣言してはならない(fail-closed)** |
| **D-6** | ★ **census のラベル写像** | **未確定**: $c'=+1\mapsto$ NN-09 か NN-12 か。**census が $A_{c'}$ をどちらの符号で構成したか**に依存 | **census-reading** | **未確定の間は SELECT を宣言してはならない(fail-closed)** |
| **D-7** | **$\varepsilon$(ORIENT (c))** | 測定側 $\Psi=\varepsilon\Psi_0$ は **$c'\mapsto\varepsilon c'$**。工房実測「$\varepsilon$ は対を交換」(NN-09/NN-12 の入替)を採る | **cert-reading(既測・要 pin)** | $\varepsilon$ を無視した実装は SELECT が反転 |
| **D-8** | **判別力の前件** | $S_{u_{S4}}\ne1$ **かつ** $S_{\rm anc}\ne1$。$u_{\rm dih}=\pm2^{-7}$ ゆえ $S_{\rm anc}\ne1\iff 2$ が mod $p$ の立方でない | **数学者(確定)** | DC-4(前件を満たさない $p$ で停止) |
| **D-9** | **素数条件** | $p\equiv1\ (9)$、$p\nmid 2\cdot3\cdot5$、D-8。$u_{\rm dih}$ の分母は $2^7$ ゆえ**追加の除外素数は 2 のみ**(既に除外済) | **数学者(確定)** | S2 の assert |

## B.1 訂正後の S1–S10(差分のみ・実装はこれを写す)

```
S4'  Su   := cube(u_S4)             # u_S4 = u0 or u0^-1 per D-5   [FAIL-CLOSED until D-5]
     Sanc := cube(u_dih)            # u_dih = 2^-7 (or -2^-7); same class mod cubes   [D-2]
S5'  assert Su != 1 and Sanc != 1                                   # D-8
S6'  cprime := 1 if Su == Sanc else 2                               # D-4
S7'  k3  := discrete_log(Sanc, g_p)   # anchor side ; NOT from beta [D-2, D-3]
S8'  psi := discrete_log(Su,   g_p)   # same g_p                    [D-3]
S9'  SELECT := label(cprime, epsilon)  # per D-6 and D-7  [FAIL-CLOSED until D-6]
S10  unchanged (3 primes must agree)
```
**変更点は 3 つだけ**: (i) $S_\beta\to S_{\rm anc}$、(ii) $k_3$ を**アンカーの離散対数**にする(P1 corpus の marking を経由しない)、(iii) D-5/D-6 の fail-closed。

## B.2 破壊対照の更新(DC-1〜5 は維持・1 本追加)

| # | 対照 | 期待 |
|---|---|---|
| DC-1〜DC-5 | §7.3.4 のまま | 変更なし |
| **★ DC-6(アンカー整合・新設)** | $u_{\rm dih}$ を $u_{\rm dih}^{-1}$ に差し替えて再走 | **$c'$ が反転する**。反転しなければ実装がアンカーを見ていない |
| **★ DC-7($\beta$ 混入検出・新設)** | $S_\beta$($\beta=2$)を使う旧実装と結果を比較 | **必ず反対の $c'$ が出る**(§A.3)。**同じ値が出たら、どちらかの実装が D-2 を守っていない** |

> ⚠ **DC-7 は二系統齟齬の即時検出器である。**$[u_{\rm dih}]_3=[\beta]_3^{-1}$ が確定しているので、**新旧が一致してはならない**。一致したら停止。

## B.3 射程(§7.3.5 を継承・変更点のみ)

- 本文書が**新たに閉じた**もの: **アンカー $u_{\rm dih}$ の値と、$\beta$ を使う実装が符号を反転させるという事実**。
- **なお閉じていない**もの: **D-5**($u_{S4}$ の同定・cert 追記で閉じる)と **D-6**(census ラベル・census 読解で閉じる)、および **P5 `unconfirmed`**(これは $u_0$ を S4 窓の Kummer 類と読む段の前件で、$c'$ の**値**より上流)。
- **最大文(訂正後)**: 「規約 D を宣言し、二面体側アンカー $u_{\rm dih}=\pm2^{-7}$ を同一レシピで計算した。$c'$ は $S_{u_{S4}}=S_{\rm anc}^{c'}$ で規約無依存に定まる。**残るのは D-5(cert の 1 行)と D-6(census の 1 行)のみで、幾何側の未知はもう無い。**」

## B.4 UNKNOWN(推測で埋めていない)

1. **D-5**(`u0` vs `u0_inverse`)— cert に宣言なし。**私の読解では $u_{S4}=u_0$ ⟹ $c'=+1$ だが `candidate`。**
2. **D-6**(census ラベル写像)— census 未読。
3. **P5(`u_0=u_{S4}`)は `unconfirmed`** — cert 自己申告。$c'$ の値の上流にある別の前件。
4. **正規化定数 $c\in(\mathbb Z/9)^\times$**(§6.6 P-a)— **本訂正により $c'$ の決定には不要になった**(アンカー経路は $c$ を通らない)。ただし mod 9 の canonical marking には依然必要。
