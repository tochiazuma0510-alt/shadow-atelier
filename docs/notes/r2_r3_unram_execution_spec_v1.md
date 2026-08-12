# R-2 / R-3 / UNRAM U3-1..3 実行 spec(宣言済みモデル $W(P_1)$ 上)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔裁定 1115(R-1 発令 → 下流工程の起草)
前提の凍結物 = `p8_prereg_v3_2.md`(sha `3a9cfb06…`)・`branchP_and_r_spec_v1.md`(r カード v2・sha `b1300005…`)・宣言正本 `r1_declaration_v4.md`(tag `v1.0-r1`)
生成 script(裁定 1103 規約)= `scratchpad/r2r3_model_invariants.py`(本書の全数値の出所)
⚠ **prereg 規律**: $d_9$・$r$・$a_{\rm class}$ の値は本書で**一切計算していません**。本書は「測る手順」のみを凍結します。**発火は司令塔検問後**。
⚠ $u$/$c$ 非接触・封印非接触。**格: candidate**(Sol 未監査)。

---

## §0 ★★★ 先に 1 つ — 宣言モデルは **$\mathbf Q$ 上に降ります**

置換 $x=\zeta_3^{\,2}X$($y=Y$)で(機械検算・script §descent_check):

$$\boxed{\ E_{\mathbf Q}:\ Y^2+3XY+2Y=X^3,\qquad W_{\mathbf Q}:\ X^2w^3-27\,Y\,(w+1)=0,\qquad t=-\frac{Y^2}{4}\ }$$

- $E$: $y^2+3\zeta_3xy+2y-x^3\mapsto Y^2+3XY+2Y-X^3$ ⟹ **$\zeta_3$ が消える** ✔
- $W$: $\zeta_3\bigl(X^2w^3-27Y(w+1)\bigr)$ ⟹ **単数 $\zeta_3$ を割って有理** ✔
- 標識点: $Q_0=(0,0)\mapsto(0,0)$、$Q_\infty=O$、$P_1=(0,-2)\mapsto(0,-2)$ ⟹ **すべて $\mathbf Q$-有理** ✔($B_1,B_2$ は $Y^2+4=0$ という**有理因子**)
- $\Delta(E_{\mathbf Q})=-216=-2^3\cdot3^3$、$c_4=-63$、$j=9261/8=21^3/2^3$(宣言・falsifier 監査の既公開値と一致)

$$\boxed{\ \Longrightarrow\ \lambda_9\ \textbf{の定義体}\ \subseteq\ \mathbf Q\ }$$

⚠ **宣言(v4)は falsify されません** — v4 は「定義体 $\subseteq\mathbf Q(\zeta_3)$」で、$\mathbf Q\subseteq\mathbf Q(\zeta_3)$ ゆえ**真のまま**です。本節は**その精密化**であり、凍結された宣言文には手を触れません(記録は本 spec に)。
★ **帰結 1**:【D2-GAP-7】(324 の 3 本の Galois 軌道)は **完全閉鎖** — $\lambda_9$ は $\mathbf Q$ 上定義されるので $\mathrm{Gal}(\bar{\mathbf Q}/\mathbf Q)$-軌道は**単元**、moduli 体 $=\mathbf Q$。
★ **帰結 2**: 発注の「$\mathbf Z$ 係数化配慮」は**近似ではなく厳密に満たされます** — U3-1 は真正の $\mathbf Z[1/S]$-モデルになります(第 III 部)。

---

# 第 I 部 — R-2(検算残)

## §1 R-2 の再定義

旧 spec(`branchP_and_r_spec_v1.md` §I.4 [P2])は**平面モデル $F(t,w)$** を前提にしていました。宣言モデルは**塔** $W\xrightarrow{3}E\xrightarrow{3}\mathbf P^1_s\xrightarrow{2}\mathbf P^1_t$ なので、R-2 の各項を塔の言葉に翻訳し、**済/残**を仕分けます。

## §2 ★ 済んでいる分(再実行不要・根拠を明記)

| 旧項 | 内容 | 判定 | 根拠 |
|---|---|---|---|
| [P1] | 平面モデル $F(t,w)$ の構成 | ★ **不要**(方式変更) | 塔モデルが宣言済。$F(t,w)$ は消去すれば得られるが**下流のどの工程も要求しません** |
| [P2](a) | $\lambda_9^{-1}(0)=\{P_0\}$ | ★ **済** | passport の $\sigma_0=$ 18-cycle ⟹ $t=0$ 上は 1 点(cert `r13_r0_v1_1` + 母集団 cert・**cross-checked**) |
| [P2](b) | $P_0$ の有理性 | ★ **済(紙)** | §2.1 |
| F-7 | $\dim L(18P_\infty)=15$ | ★ **済(紙)** | $g=4$・$\deg18>2g-2=6$ ⟹ Riemann–Roch で $18-4+1=15$(機械帳簿) |
| F-8 | $18(P_0-P_\infty)\sim0$ | ★ **済(自明)** | $\mathrm{div}(\lambda_9)=18(P_0-P_\infty)$ ⟹ 主因子。さらに補題 ORD9 で $\mathrm{ord}(P_0-P_\infty)=9$、$9\mid18$ ✔ |
| [P1](e)③ | Jac の torsion 確認 | ★ **済** | 同上(ORD9) |

### 2.1 ★ 補題 P0-RAT($P_0,P_\infty$ の有理性 — 計算不要)

> $\lambda_9$ は $t=0$ で**全分岐**(passport)⟹ $\lambda_9^{-1}(0)$ は**1 点** $P_0$。$W$ と $\lambda_9$ は $\mathbf Q$ 上定義される(§0)ので $\mathrm{Gal}(\bar{\mathbf Q}/\mathbf Q)$ は $\lambda_9^{-1}(0)$ を保つ。1 点集合ゆえ各元は固定される ⟹
> $$\boxed{\ P_0\ \textbf{は }\mathbf Q\textbf{-有理点。同様に }P_\infty\ \textbf{も}\ }$$

⟹ 旧 [P2](b) の「非有理なら即停止・UNKNOWN(u3)」という枝は **発生しません**。$F_9=\mathbf Q(\zeta_{36})$ どころか $\mathbf Q$ 有理です。

## §3 ★ 残る分 — 有理 uniformizer の構成([R-2-U])

残るのは実質 **1 項目**です。

```
=== [R-2-U] P_0 における有理 uniformizer(R-2 の残り全部)===
根拠: docs/notes/r2_r3_unram_execution_spec_v1.md §3
モデル: E_Q : Y^2+3XY+2Y=X^3 , W_Q : X^2 w^3 - 27 Y (w+1) = 0 , t = -Y^2/4
⚠ u/c 非接触・prereg 非抵触(u_9 の *値* は本工程では出さない)

[U-1] P_0 の局所座標を確定
   P_0 = W_Q の Q_0=(0,0) 上の唯一の点(W->E で全分岐 e=3)
   ★ E 上の Q_0 での uniformizer: div_E(Y)=3Q_0-3Q_inf ゆえ Y は 3 位の零 ⟹ Y は不可
      X は?  div_E(X)=Q_0+P_1-2Q_inf ⟹ Q_0 で 1 位の零 ⟹ ★ X が E の uniformizer
[U-2] W 上へ引き戻す: W->E は Q_0 で全分岐(e=3) ⟹ ord_{P_0}(pi^*X)=3
   ⟹ ★ W の uniformizer は「3 位の零を 1 位にする」量が要る
   候補 s = X/w^a など。w の P_0 での位数を Newton 多角形で決めてから選ぶこと
[U-3] ★ 2 通りの uniformizer s^(1), s^(2) を取り両方 cert に記録
   (= prereg v3 の T63-UNIF-INV 検査用・r カード [5] s9_variants 欄)
[U-4] 見張り(fail-closed)
   (W-a) ord_{P_0}(s) = 1 を厳密に確認(数値で確認しない)
   (W-b) ord_{P_0}(lambda_9) = 18 を確認(passport との整合)
   (W-c) s は Q-有理(係数が Q)。非有理なら即停止・報告
出力: cert (schema r2_unif/v1)。u_touched=false ; c_touched=false
★ 規模: 局所展開のみ。分〜時級。
```

⚠ **[U-2] の注意**: $\mathrm{ord}_{P_0}(\lambda_9)=18$ と $\mathrm{ord}_{P_0}(\pi^*X)=3$ から、$s$ は $\lambda_9$ と $\pi^*X$ の適当な単項式では作れません($\gcd(18,3)=3\ne1$)。**$w$ の位数を先に決める**必要があります(Newton 多角形)。⟹ ここが R-2 の実質的な唯一の作業です。

---

# 第 II 部 — R-3(a_class 出力)と $r$ 突合

## §4 $u_9$ の抽出仕様([R-3-U9])

$$\lambda_9=u_9\,s^{18}\bigl(1+O(s)\bigr)\qquad\Longrightarrow\qquad u_9=\lim_{s\to0}\lambda_9\,s^{-18}$$

```
=== [R-3-U9] u_9 の厳密抽出 ===
前件: [R-2-U] 完了(s が確定)
[9-1] P_0 の周りで lambda_9 = -Y^2/4 を s の Puiseux/冪級数に厳密展開(浮動小数点禁止)
[9-2] u_9 := 主係数。★ 2 通りの s で計算し、u_9^(1)/u_9^(2) が 18 乗であることを確認
      (= T63-UNIF-INV。u_9 は 18 乗を除いてしか定まらない — これが a_9 が法 18 である理由)
[9-3] 出力は u_9 の *厳密値* と、その類 [u_9^{-1}]
出力: cert (schema r3_u9/v1)
⚠ ★ この cert が出た時点で u は touched。以後の工程は司令塔検問下。
```

## §5 ★★【r-GAP-1】の規約提案 — 法 18 → 法 9 の落とし方

r カード v2 §II.1.1 は「$a_9$(法 18・$F^\times$)から $[a]$(法 9・$\mathbf Q^\times$)を取り出す規約は**未確定**」を本仕様**最大の前件**としています。以下を提案します。

> **【規約 DESC-9】(3 段・各段 fail-closed)**
> **(D-i) 指数の落とし**: 自然な全射 $F^\times/(F^\times)^{18}\twoheadrightarrow F^\times/(F^\times)^{9}$ で $a_9$ を送る。像を $\bar a\in F^\times/(F^\times)^9$ と書く。
> **(D-ii) 有理性検査(fail-closed)**: $\bar a$ が $\iota:\mathbf Q^\times/(\mathbf Q^\times)^9\to F^\times/(F^\times)^9$ の**像に入るか**を判定する。
>  ⟹ **入らなければ即停止**: K9-KUMMER の「$L_{9,\rm Aff}=\mathbf Q(\zeta_9,\sqrt[9]{a})$、$a\in\mathbf Q^\times$」という前提そのものが破れている ⟹ UNKNOWN(新枝)として報告。
> **(D-iii) 降下**: **RES-INJ-9**($\iota$ の単射性・r カード前件 A4 に既収載)により、像に入るなら $[a]$ は**一意に定まる**。その素因子指数ベクトル(法 9)が $a_{\rm class}$。

$$\boxed{\ \textbf{r-GAP-1 は「指数の落とし + 有理性検査 + RES-INJ-9」に分解され、未確定部分は (D-ii) だけになる}\ }$$

★ **要点**: 「位数だけでは $r$ は決まらない」という r カードの指摘は正しく、**DESC-9 は位数を経由しません**(類そのものを運びます)⟹ カードの禁止事項 [5] を満たします。
⚠ **(D-ii) は仮定ではなく検査**です。通らない場合を UNKNOWN 枝として先に登録してください(下記 (r5))。

### 5.1 ⚠ r カード [2] の UNKNOWN 枝に 1 本追加を要請

```
(r5) 新設: DESC-9 の (D-ii) 有理性検査が落ちる
     ⟹ [a] が Q^x/(Q^x)^9 に存在しない ⟹ K9-KUMMER の前提が破れ
     ⟹ r も a_class も定義できない。★ MISS ではなく UNKNOWN。
```

## §6 ⚠ 型境界 — 体が $\mathbf Q(\zeta_{36})$ から $\mathbf Q$ へ変わりました

r カード v2 は $a_9\in F_9^\times/(F_9^\times)^{18}$、$F_9=\mathbf Q(\zeta_{36})$ と型づけています。しかし §0 のとおり**宣言モデルは $\mathbf Q$ 上**なので、$u_9$ は $\mathbf Q^\times$ の元として出ます。

$$\boxed{\ \textbf{R-3 の出力は }\ [u_9^{-1}]\in\mathbf Q^\times/(\mathbf Q^\times)^{18}\ \textbf{と、その }F_9\ \textbf{への像の}\textbf{両方}\ \textbf{を記録すること}\ }$$

- **利点**: $\mathbf Q$ 側の方が**細かい**情報です($\mathbf Q^\times/(\mathbf Q^\times)^{18}\to F_9^\times/(F_9^\times)^{18}$ は単射とは限らない)。⟹ DESC-9 の (D-ii)(有理性検査)が**自明に通ります** — $u_9$ が最初から有理だからです。
- ⚠ **凍結カードとの整合**: 型が変わるので、**司令塔が r カードに「$F$ の実体は宣言モデルの定義体 = $\mathbf Q$」という 1 行を追記**してください(カード本体は不改変・追記形)。⟹ **【r-GAP-2】(新)**。
- ★ ⟹ **DESC-9 は実質 (D-i) の指数落としだけになります**: $[u_9^{-1}]\in\mathbf Q^\times/(\mathbf Q^\times)^{18}\to\mathbf Q^\times/(\mathbf Q^\times)^{9}$。

## §7 $a_{\rm class}$ 出力 schema(P8 v3.2 §2 準拠・追加欄つき)

```
schema : p8_a_class/v1   (P8 v3.2 の凍結 schema をそのまま使用)
a_class : {
  representation : "exponent vector mod 9 over the support primes"
  support        : [p_1, ..., p_k]     昇順・重複なし
  exponents      : [e_1, ..., e_k]     e_i in Z/9
  order          : 9 / gcd(9, gcd_i e_i)          in {1,3,9}
  normalization  : "a は Q^x/(Q^x)^9 の代表・sign は 9 乗で消えるため無視"
}
a_9_field_note : {                    ★ 本 spec §6 で追加を要請する欄
  u9_home_field  : "Q"                 (宣言モデルの定義体・R-1 v4 + 本 spec §0)
  class_mod18_Q  : [u_9^{-1}] in Q^x/(Q^x)^18     ★ 素因子指数ベクトル(法 18)
  image_in_F9    : 同じ類の F_9^x/(F_9^x)^18 での像(旧カードの型との橋)
  desc9_rule     : "DESC-9 (D-i)->(D-ii)->(D-iii)"
  desc9_step_ii_passed : true/false    ★ fail-closed
}
```

★ **P-K9U-1 の判定は $a_{\rm class}$ が出た瞬間に確定します**(r カード [3]・B-1 の順序要件)⟹ **score rule S-1**(P8 v3.2 §3)を**同一 cert 内で同時に評価**してください: `support == [3]` **かつ** `order == 9`。**support だけで判定しない**。

## §8 $r$ 突合手順(一気通貫)

```
=== [R-3-r] r 測定と TRIAD-972 突合 ===
前件(r カード v2 [0] の A1-A4 + 本 spec の (r5))
  A1 : R-3 が [a] を *類として* 出力(= §7 の a_class)      ← DESC-9 で充足
  A2 : [b] は *在庫済* — ds4 cert 内 {2:-8, 3:6, 5:9}       ← 再測定不要
  A3 : 両側の正規化が同一(法 9・Q^x/(Q^x)^9・素因子指数の基底)
  A4 : TRIAD-972 の前提(i not in L_S4 / RES-INJ-9 / R3-GAP-4/5)
[r-1] 基底の統一: supp(a) ∪ supp(b) を昇順の素数リストに揃え、
      両側の指数ベクトルを法 9 で同じ基底上に書く
      ★ [b] = {2:-8, 3:6, 5:9} は法 9 に正規化すると {2:1, 3:6, 5:0}
        (-8 = 1 mod 9 ; 9 = 0 mod 9)  ⟹ 5 は台から落ちる
[r-2] r := |<[a]> cap <[b]>|  in  (+)_p Z/9
      既存 r_intersection_template_v1.py(canary 4/4)で計算
[r-3] 見張り: r | gcd(d_9, d_S4) を確認 ⟹ 破れたら (r2) UNKNOWN
[r-4] TRIAD-972: |X\A| = 972 - 12 d_9 d_S4 / r
      ⚠ ★ d_9, d_S4, r が *全て確定した後* にのみ評価(P8 v3.2 S-4)
      ⚠ (r4) の射程: M = K^(9) cap N_S4 屋根に限る。972 以外へ流用しない
[r-5] QUAR: |X\A| > 0 なら r カード [4] の 8 要件(Q1-Q8)を発動
      ★ (Q8): 「反例を得た」と書かない(個数であって witness ではない)
出力: cert (schema r_receipt/v1)。r カード [6] の全欄。
```

⚠ **$[b]$ の法 9 正規化は私が本 spec で初めて書いたので、実装は必ず再導出してください**(在庫値 $\{2:-8,3:6,5:9\}$ の出所 = ds4 cert)。★ 生成 script 添付規約の対象です。

---

# 第 III 部 — UNRAM U3-1..3 の具体化

## §9 U3-1 — integral model($\mathbf Z[1/S]$ 上・★ $\mathbf Z$ 係数で立ちます)

§0 により分母は $t=-Y^2/4$ の **4** だけです。

```
=== [U3-1] Z[1/S]-モデルの構成 ===
[1-1] E_Z : Y^2 + 3XY + 2Y = X^3            over Z          (Delta = -216 = -2^3 3^3)
[1-2] W_Z : X^2 w^3 - 27 Y (w+1) = 0        over Z
[1-3] t   : -Y^2/4                          over Z[1/2]
      ★ 代替: t' := -Y^2 と置き直すと Z 上になるが、分岐点が t'=-4 に移る
        ⟹ Belyi 正規化 {0,1,inf} を保つなら 1/2 を許すのが素直
[1-4] 出力: 係数行列・判別式イデアル・特異点の候補(Jacobian が消える点)
出力: cert (schema u3_model/v1)
```

★ **配慮の達成**: 発注の「$\mathbf Z$ 係数化配慮」は §0 の降下で**厳密に**満たされました。$\mathbf Z[\zeta_3]$ を経由する必要はありません ⟹ **「3 の外で不分岐」の主語が $\mathbf Q$ の素点になり、(K9-UNRAM) の言明と型が合います**(旧設計では $\mathbf Z[\zeta_3]$ の素点になり 3 が分岐して型がずれる懸念がありました)。

## §10 U3-2 — 平滑性 / 非衝突 / エタール性

```
=== [U3-2] 幾何的条件 ===
[2-1] 分岐因子 D={0,1,inf} の非衝突: Z[1/2] 上で自動(3 点はどの F_p でも相異なる)
      ★ 紙で済む(旧設計の指摘どおり)
[2-2] W_Z が Z[1/S] 上平滑: Jacobian 判定
      ideal( W, dW/dX, dW/dY, dW/dw ) + E の関係式 で Groebner
[2-3] W -> P^1_t が D の外でエタール: 相対微分の消滅イデアルを計算し
      その台が D の上に載ることを確認
[2-4] 塔で分けてよい(層ごとに): W->E , E->P^1_s , P^1_s->P^1_t
      ★ 層ごとの方が軽い。合成のエタール性は各層のエタール性から従う
出力: cert (schema u3_smooth/v1)
```

## §11 U3-3 — 判別式 → $S$

```
=== [U3-3] 悪い素点の集合 S ===
[3-1] 層ごとの判別式:
      (a) E->P^1_Y : disc_X(X^3 - 3YX - (Y^2+2Y))  ... の Y-判別式
      (b) W->E     : disc_w(X^2 w^3 - 27Y(w+1))
      (c) P^1_s->P^1_t : t=s^2 ⟹ 2 のみ
[3-2] S := { p : p | (上の判別式たちの内容 idealの生成元) } ∪ {2}
[3-3] 各層の bad prime を *別々に* 記録(合成してから因数分解しない)
[3-4] 見張り: Delta(E)= -216 = -2^3 3^3 ⟹ S ⊇ {2,3} の *下限* は確定
      ⚠ ★ 上限(S ⊆ ...)を出すのが本工程の目的
出力: cert (schema u3_disc/v1)
```

## §12 ⚠⚠ prereg 危険 — U3-3 は **P-K9U-1 を部分的に先取りします**

$$\boxed{\ S\ \textbf{が確定すると }L_{9,\rm Aff}\ \textbf{の分岐可能素点が上から抑えられ、}\operatorname{supp}(a)\ \textbf{が制約される}\ }$$

- $\operatorname{supp}(a)\subseteq S\cup\{3\}$(ざっくり)⟹ **$S\subseteq\{3\}$ が出れば $\operatorname{supp}(a)=\{3\}$ が(位数 9 と併せて)確定** ⟹ **P-K9U-1 が $a_{\rm class}$ より先に決まってしまう**。
- ⚠ これは r カード v2 の **B-1 で摘出された順序要件と同型**であり、「**同時に判定される命題を全部先に列挙する**」(原則 3)を**三度目に破る**危険です。

$$\boxed{\ \textbf{要請}:\ \textbf{U3-3 の発火前に、P-K9U-1 が}\textbf{同時判定される}\textbf{ことを prereg 台帳へ明記すること}\ }$$

**選べる 2 案(司令塔裁定事項)**:
| 案 | 内容 | 得失 |
|---|---|---|
| **(α)** U3-3 を $a_{\rm class}$ 凍結**後**に発火 | 順序を守る | UNRAM が待たされる |
| **(β)** U3-3 の cert に「P-K9U-1 の同時判定」を**事前登録して**同時発火 | 待ちがない | 登録漏れがあれば原則 3 の三度目 |

★ 私の推薦は **(β)**: $S$ は**上限**を与えるだけで $\operatorname{supp}(a)$ を**決めない**ことも多く($S=\{2,3\}$ なら未決)、待たせる価値が薄いためです。ただし**事前登録は必須**。
⚠ ただし **$\Delta(E)=-2^3 3^3$ という下限情報は $\operatorname{supp}(a)$ を制約しません**($S$ の下限は $a$ の台の上限を与えない)⟹ §0 の公開値は prereg 抵触しません。**私はここで止めています。**

## §13 残る紙の 1 段

`win83_audit_and_unram3_v1.md` II.3 のとおり、$U3\text{-}1\sim3$ が済んでも
$$\boxed{\ p\notin S\ \Longrightarrow\ \rho_9(I_p)=1\ }$$
は**紙**(specialization の $G_{\mathbf Q_p}$-同変性)で、**【UNRAM-GAP-4】**として残ります。★ Annals Thm 1(i) は pro-$l$ outer についてで**直接は効きません**(B119-1)。
⟹ **【文献要請 U3-L1】**(既出【UNRAM-GAP-5】と併せて):
- **困難**: 「良い還元をもつ被覆の specialization が $I_p$ を自明に送る」型の定理を、**二面体 translation の設定**へ翻訳したい。
- **欲しい結果の型**: $\mathcal W\to\mathbf P^1_{\mathbf Z[1/S]}$ が $D$ の外でエタール・$\mathcal W$ 平滑 ⟹ $\pi_1$ の specialization が $p\notin S$ で不分岐、という**構造定理**(SGA1 系 or Beckmann 型)。
- ★ **$\mathbf Q$ 上に降りた**(§0)ので、$\mathbf Z[\zeta_3]$ を扱う版ではなく**標準的な $\mathbf Z$ 上の版**が使えるはずです ⟹ 文献の当たりが良くなりました。

---

# 第 IV 部 — 分担と発火順

## §14 工房 / Sol 分担(裁定 1024 基準)

| 工程 | 内容の重さ | 担当 | 理由 |
|---|---|---|---|
| **[R-2-U]** uniformizer | 局所展開(Newton 多角形)・数体なし | ★ **工房**(implementer) | $\mathbf Q$ 上に降りたので数体演算が消えた |
| **[R-3-U9]** $u_9$ 抽出 | 次数 18 の塔の**厳密 Puiseux 展開** | ★ **Sol** | 重い厳密代数(裁定 1024) |
| **DESC-9** (D-i)(D-iii) | 指数落とし + 素因数分解(有理数) | ★ **工房** | §6 により $\mathbf Q$ 上で完結・軽い |
| **[R-3-r]** $r$ 交差 | $\bigoplus_p\mathbf Z/9$ の巡回部分群の交わり | ★ **工房** | 既存 template(canary 4/4) |
| **[U3-1]** integral model | 係数整理 | ★ **工房** | §0 で $\mathbf Z$ 係数 |
| **[U3-2]** 平滑/エタール | $\mathbf Z$ 上の Gröbner(3 層) | ★ **Sol** | 整数係数 Gröbner は重い |
| **[U3-3]** 判別式 → $S$ | 終結式・判別式の因数分解 | ★ **Sol** | 同上 |
| **【UNRAM-GAP-4】** | 紙(specialization の同変性) | ★ **数学者**(私)+ 文献要請 | — |

★ **§0 の降下により工房側の取り分が増えました**(数体演算が消えたため)。Sol へ回すのは **[R-3-U9]・[U3-2]・[U3-3]** の 3 本です。

## §15 発火順と検問点

```
 (0) 司令塔検問 ─┬─ [R-2-U] (工房)  ────┐
                 └─ [U3-1] (工房)  ─────┼─→ [U3-2] (Sol) → [U3-3] (Sol)
                                        │        ↑ ★ §12 の prereg 登録が前件
                        [R-3-U9] (Sol) ←┘
                              ↓  ★ ここで u が touched
                        DESC-9 (工房)
                              ↓
                        a_class 出力 ★ 同時に P-K9U-1 が確定(S-1)
                              ↓
                        [R-3-r] (工房) → TRIAD-972 突合(d_9, d_S4 が揃った後)
```

**検問点 3 つ**:
1. **[R-3-U9] 発火前** — $u$ touched になるので司令塔検問。
2. **$a_{\rm class}$ 出力前** — P8 v3.2 の 4 条件(§4)が凍結済であることの確認。★ **既に凍結済**(sha `3a9cfb06…`)⟹ 通過可。
3. **[U3-3] 発火前** — §12 の (α)/(β) の裁定と prereg 登録。

---

## §16 記帳

- ★ **本 spec の新規部分**: ① ★★ **宣言モデルの $\mathbf Q$ への降下**($x=\zeta_3^2X$・機械検算)⟹ 定義体 $\subseteq\mathbf Q$・**【D2-GAP-7】完全閉鎖**・$\mathbf Z$ 係数化が厳密に達成 ② **補題 P0-RAT**(全分岐 ⟹ 唯一点 ⟹ Galois 固定 ⟹ 有理)で R-2 の停止枝を消去 ③ R-2 の残りが **uniformizer 1 項目**に縮約 ④ ★★ **規約 DESC-9**(【r-GAP-1】を「指数落とし + 有理性検査 + RES-INJ-9」に分解)⑤ **型境界の摘出**($F_9=\mathbf Q(\zeta_{36})$ → $\mathbf Q$)と【r-GAP-2】 ⑥ UNKNOWN 枝 (r5) の追加要請 ⑦ ★★ **§12 の prereg 危険の事前摘出**(U3-3 の $S$ が P-K9U-1 を先取りしうる・原則 3 の三度目を防ぐ)⑧ 分担案(降下により工房の取り分が増加)。
- **【r-GAP-1】** ⟹ DESC-9 で **(D-ii) を除き解消**。§6 により (D-ii) も自明化する見込み(要 R-3 実測)。
- **【r-GAP-2】(小・新)** r カード v2 の型欄($F_9=\mathbf Q(\zeta_{36})$)への追記(実体は $\mathbf Q$)。**カード本体は不改変・追記形**で司令塔が執行。
- **【UNRAM-GAP-4/5】** 不変。★ ただし $\mathbf Q$ 降下により文献の当たりが良くなった(§13)。
- ⚠ **prereg 申告**: 本書は $d_9$・$r$・$a_{\rm class}$・$S$ を**一切計算していません**。§0 の $\Delta(E)=-216$・$j=9261/8$ は宣言と falsifier 監査で**既公開**の値で、$S$ の**下限**にしか効かず $\operatorname{supp}(a)$ を制約しません(§12 末尾)。
- **申告**: sympy(`scratchpad/r2r3_model_invariants.py`)+ 紙。本書の全数値は機械生成(裁定 1103 規約)。$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
