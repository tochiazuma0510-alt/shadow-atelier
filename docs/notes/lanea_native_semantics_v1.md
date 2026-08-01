# lane A `searcher_native` の数学的意味論 v1 — 3-loci カタログの正体と A/B 照合仕様

2026-08-01 起草: Claude(第三数学者インスタンス・Opus 5)。**状態 = candidate。**
裁定 309 の発見(lane B checker_native と lane A searcher_native が構造的に非可比)への回答。
正典: `docs/week4-NInfty_stage2_spec_v18.md` §1/§2/§3/§4.1、`docs/notes/e5_interpretation_v1.md`(裁定 113)。
参照した実装: `search/ninfty-searcher-v2.mjs` の `buildSearcherNative`(L488-549)、`search/ninfty-checker.py`(L547-621)。
**私は checker_native を書いていないので lane 独立性は壊れていない**(司令塔の明示許可による lane A コード閲覧)。

---

## 0. 結論(先に 6 行)

1. lane A の 3-loci は **R_μ の表現ではない**。**different の塔公式の「有限成分の材料表」**である — 3 つのうち **d だけが R_μ に寄与し、p と f6 は打ち消し合って寄与 0**。
2. ただし **翻訳辞書は存在し、閉じている**(§2 定理 A):T-1 と E-1〜E-4 の下で $R_\mu=\pi^*V(d)+4(\infty_++\infty_-)$。**係数まで一意**。
3. **無限遠成分は lane A に「無い」のではなく「x-line のイデアルでは原理的に書けない」** — $\mathbb Q[x]$ のアフィンイデアルは $\infty$ を見ない。コード自身が SCOPE NOTE で T-5 未計算と自己申告しており、**設計の欠落ではなく表現形式の限界**。
4. **`branch_divisor_on_P1_ref` は同値ではない・誤ラベルである。** 中身は同じ x-line イデアルの複製で、`pushforward_of` が主張する押し出しは $\mu_*$ ではない。真の $\mu_*R_\mu=4[0]+2[s]+2[-s]+4[\infty]$ は **v-line** 上にある。
5. **朗報**: $\mu_*R_\mu$ は $s\notin\mathbb Q$ でも **$\mathbb Q$-有理な閉点因子**として書ける($4[v]+2[v^2+C]+4[\infty]$)。ゆえに lane A の「$\mathbb Q$ 係数モニックイデアル」様式を**捨てずに**正しくできる(§3)。
6. **E-5 は lane B の発見どおり導出可能** — ただし lane B の論証は **$n=5$ を出していない**(§5)。しかもこれは裁定 113(`e5_interpretation_v1.md` 命題 E5-D)の**独立再発見**であり、lane A は既に導出実装済み・**lane B の checker.py だけが陳腐化している**。

---

## 1. 幾何の型(spec §1.1 の再掲 + 塔の可換図式)

$$ C:\ y^2=f_6(x),\quad \mu=a+py,\quad \mu^\iota=a-py,\quad \mu\mu^\iota=C\in\mathbb Q^\times,\quad \mu+\mu^\iota=2a $$

$q(v):=\dfrac{v^2+C}{2v}$($\deg q=2$)とおくと $q\circ\mu=\dfrac{\mu^2+\mu\mu^\iota}{2\mu}=\dfrac{\mu+\mu^\iota}{2}=a$。ゆえに**可換図式**

```text
        mu                                     deg mu = 5
  C ----------> P^1_v                          deg pi  = 2
  |               |                            deg a   = 5
  | pi            | q                          deg q   = 2
  v               v                            q o mu = a o pi  (= 10 : 10)
 P^1_x --------> P^1_w
        a
```

**この図式が lane A の 3-loci の正体を説明する。** 各写像の ramification divisor:

| 写像 | $R$ | $\deg R$ |
|---|---|---|
| $\pi:C\to\mathbb P^1_x$ | $\sum_{i=1}^{6}W_i$(Weierstrass 点・$e=2$) | 6 |
| $a:\mathbb P^1_x\to\mathbb P^1_w$ | $V(p)+V(d)+4[\infty_x]$($a'\doteq pd$ = §1.7 (60.5)) | 8 |
| $q:\mathbb P^1_v\to\mathbb P^1_w$ | $[\sqrt C]+[-\sqrt C]$($q'=(v^2-C)/2v^2$) | 2 |
| $\mu:C\to\mathbb P^1_v$ | **求めるもの** | 12 |

**lane A が輸出する 3 つの locus は、正確に「$R_\pi$ の定義多項式 $f_6$」「$R_a$ の有限部の 2 成分 $p,d$」である。**
すなわち **`weierstrass-locus` = $R_\pi$・`p-locus` と `a-pair-locus` = $R_a$ の有限部**。$R_a$ の $4[\infty_x]$ と $R_q$ は輸出されていない。

---

## 2. 翻訳辞書

### 定理 A(R_μ の閉形)

> **E-1〜E-4 と T-1($\operatorname{rootpart}(a)=[2,2,1]$)の下で、$d:=\operatorname{monic}\gcd(a,a')$ とおくと**
> $$ \boxed{\ R_\mu=\pi^*V(d)+4(\infty_+)+4(\infty_-)\ },\qquad \deg=2\cdot 2+8=12 $$
> **かつ $\pi^*V(d)$ は被約**(4 つの相異なる点、係数 1)。

**証明(spec 内で閉じる・塔公式を使わない).**
(a) **無限遠**: 命題 E5-D(`e5_interpretation_v1.md` §2.2)より $\operatorname{div}(\mu)=5(\infty_-)-5(\infty_+)$、ゆえに $\mu$ は $\infty_\pm$ で全分岐 $e=5$、$e-1=4$。
(b) **有限**: §1.5 `N∞-pair` より $s^2=-C$ に対し $\operatorname{part}\mu^{-1}(\pm s)=\operatorname{rootpart}(a)=[2,2,1]$、その $x$-座標は $a$ の根。$e=2$ の点は $a$ の**二重根** $=V(d)$($\deg d=2$・squarefree は T-1)。
(c) **$\pi^*V(d)$ が被約**: $x_0\in V(d)\Rightarrow a(x_0)=0$、(Pell) と $C\ne0$ より $p(x_0)^2f_6(x_0)=-C\ne0$、ゆえに **$f_6(x_0)\ne0$ かつ $p(x_0)\ne0$**(§1.5 の証明そのもの)。よって $x_0$ 上に相異なる 2 点 $(x_0,\pm y_0)$、$y_0\ne0$、$\pi$ は不分岐。各点は $\mu$ の $e=2$ 点で $e-1=1$。$\mu(x_0,y_0)=p(x_0)y_0=\pm s$ で 2 点は $s$ と $-s$ に 1 つずつ振り分けられる。
(d) **他に無い**: §1.8 `N∞-criterion` の (⇒) 方向が $\deg R_\mu=12$ を $4+4+2+2$ で使い切ることを示している。∎

**★ 追加仮定は一つも要らない。** `gcd(d,f6)=1`・`gcd(d,p)=1` は (c) のとおり **(Pell)+$C\ne0$ からの定理**であって、入力条件ではない。

### 定理 B(打ち消しの正体 — なぜ p と f6 が現れるか)

> 同じ仮定の下で $p$ は squarefree かつ $\gcd(p,f_6)=1$ であり、**二つの fixed fiber($v^2=C$)は**
> $$ \mu^*R_q=\underbrace{\textstyle\sum_{i=1}^{6}W_i}_{=R_\pi}+\underbrace{\pi^*V(p)}_{4\ \text{点}},\qquad \text{全点で}\ e=1 $$
> **ゆえに塔公式 $R_\mu=R_\pi+\pi^*R_a-\mu^*R_q$ において $R_\pi$ と $\pi^*V(p)$ は完全に打ち消え、定理 A が再導出される。**

**証明.**
(i) $f_6(x_0)=0\Rightarrow$ (Pell) より $a(x_0)^2=C$、$p(x_0)=0\Rightarrow$ 同じく $a(x_0)^2=C$。**すなわち 6 個の Weierstrass 点と $V(p)$ 上の点はすべて fixed fiber に落ちる。**
(ii) $p$ が重根を持つ、または $\gcd(p,f_6)\ne1$ なら §1.4 の (ii)$m{=}2$ / (iii) より $v^2=C$ なる値の上に $e\ge2$ の点が出る。しかし $C\ne0$ ゆえ $v\ne0$ かつ $v\ne\pm s$($v=\pm s$ なら $C=-C$)。ゆえに $v\notin\operatorname{Br}(\mu)=\{0,s,-s,\infty\}$(§1.8)に矛盾。よって $p$ squarefree・$\gcd(p,f_6)=1$。
(iii) ゆえに fixed fiber の点は §1.4(i)($y_0=0$、$e=1$)と §1.4(ii)$m{=}1$($e=1$、$x_0$ 上に 2 点)のみ。$\Sigma e=6\cdot1+4\cdot1=10=2\deg\mu$ で二 fiber を**ちょうど使い切る**。∎

**この打ち消しこそが lane A の native に `p-locus` と `weierstrass-locus` が載っている理由である** — それらは **$R_\mu$ の成分ではなく、$R_\mu$ を得るために引き算される項**。lane A の native は「$R_\mu$」ではなく「$R_\mu$ の**塔材料**」を輸出している。

### 2.3 機械照合(genuine fixture `search/fixtures/ninfty/checker_pos_01.json`・厳密有理数)

```text
a = x^5+15x^4+88x^3+252x^2+352x+192,  p = x^2+6x+44/5,  C = 256/3125
d = gcd(a,a') = x^2+6x+8 = (x+2)(x+4)     rootpart(a)=[2,2,1]      T-1 OK
a' = 5*p*d  (厳密恒等)                     gcd(p,d)=1               T-2 OK
x0=-2: a=0, a'=0, a''=8,  p=4/5, f6=-16/125,  p^2 f6 = -256/3125 = -C   (定理A(c))
x0=-4: a=0, a'=0, a''=-8, p=4/5, f6=-16/125,  p^2 f6 = -256/3125 = -C
fixed fiber v=+sqrt(C): Weierstrass 3 点 + p 根 1 個(x-重複度2) -> sum e = 3+2 = 5
fixed fiber v=-sqrt(C): Weierstrass 3 点 + p 根 1 個            -> sum e = 3+2 = 5
  => mu^* R_q = 6 Weierstrass + 4 p-points, 全て e=1     (定理B)
deg: R_pi 6 + pi^*R_a 16 - mu^*R_q 10 = 12 = deg R_mu   有限部 4 / 無限部 8
```
検算スクリプトは scratchpad(使い捨て)。**手写しではなく機械出力**。

---

## 3. 判定 1 — lane A の 3-loci は R_μ と同値か

| slot | 判定 | 理由 |
|---|---|---|
| `ramification_divisor_on_C_ref` | **条件つき同値(復元可能)・ただし as-is では非可比** | 定理 A の辞書で $R_\mu$ が一意に復元できる。しかし (α) 無限遠成分が欠落(x-line イデアルでは表現不能)、(β) 3 成分中 2 つは寄与 0、(γ) `multiplicity:1` は因子の係数ではなく「locus 存在」フラグ($d$ については偶然 $e-1=1$ に一致) |
| `branch_divisor_on_P1_ref` | **非同値(誤ラベル)** | 中身は ram slot と同じ x-line イデアル。真値 $\mu_*R_\mu=4[0]+2[s]+2[-s]+4[\infty]$ は **v-line** 上で、係数は $(4,2,2,4)$。`pushforward_of` が主張する恒等押し出しは $\mu_*$ ではない。spec §3 は lane A の職務を「local differential → R on C → **$\mu_*R$**」と定めている |

### 3.1 翻訳辞書(各 locus はどの点集合か・無限点はどこへ行ったか)

```text
a-pair-locus       gen = d = gcd(a,a')     -> pi^*V(d) = 4 点 {(x0,±y0) : d(x0)=0}
                                              = R_mu の有限部・各係数 e-1 = 1
                                              (mu で s と -s へ 2 点ずつ振り分け)
p-locus            gen = p                 -> R_mu への寄与 0(定理 B で打ち消し)
                                              身分 = T-3「fixed fiber 上で e=1」の非分岐証明材料
weierstrass-locus  gen = f6                -> R_mu への寄与 0(定理 B で打ち消し)
                                              身分 = T-4「Weierstrass 点で e=1」の非分岐証明材料
無限遠 4(inf_+)+4(inf_-)  -> lane A には無い。R_a の 4[inf_x] を pi^* した項に相当し、
                            Q[x] のアフィンイデアルでは原理的に表現できない。
                            値は candidate に依存しない定数(命題 E5-D の帰結)。
```

### 3.2 ★ 重大な副次発見(裁定 309 とは別件)

`buildSearcherNative` は **decision verdict に非依存で無条件実行**される(`search/certs/ep_first_run_20260801.json` L92 の自己申告)。しかし **定理 A/B の辞書は T-1 と (Pell) が成り立つときにしか意味を持たない。**
実例: beta candidate は $d=x$($\deg=1$)で T-1 が破れており、$\deg a'=4\ne\deg p+\deg d=3$ ゆえ **(60.5) $a'\doteq pd$ 自体が偽**。このとき輸出された 3 多項式は**因子データとして何も意味しない**(ただの 3 本の多項式)。
⇒ **native artifact は「REJECT 済み candidate に対しても divisor を名乗るオブジェクトを吐く」という fail-open 形状を持つ。** 下流が verdict を見ずに native 同士を比較すれば無意味なものを比較する。
**是正案**: native は T-1 & T-2 & (Pell) が PASS のときのみ mint し、それ以外は §3.4 R-2 の **ABSENT**(lane A が [16]-[24] で既に守っている規律と同じ)。または native に `validity_precondition_witness` 欄を必須化する。

---

## 4. 判定 2/3 — A/B「native 一致検査」をどの等式として定義するか

**両 native を生の形で field-by-field 比較してはならない**(A = x-line の塔材料イデアル、B = $\bar{\mathbb Q}$ 点+重複度 — 圏が違う)。
**正規形(NF)を spec §4.1 に凍結し、各 lane が自分の native から独立に NF を計算し、NF 同士を比較する。** これは §4 冒頭の独立性条項(「二 lane が**仕様だけ**を共有して canonicalizer を独立実装すれば単一 shared implementation にはならない」)に正確に適合する — **NF は形式契約であって共有実装ではない**。

### 4.1 正規形 NF(提案・spec §4.1 の native schema 改訂)

```text
native = {
  ram_finite = {                       # R_mu の有限部
      variable: "x",
      ideal_generator: monic in Q[x],  # A: d ;  B: 有限分岐点の x-座標の最小多項式の積
      pullback: "pi^*",                # pi^*V(gen) と読む
      reduced: true,                   # gcd(gen,f6)=1 の証明つき(定理A(c))
      coefficient: 1                   # 各点の e-1
  },
  ram_infinite = [                     # R_mu の無限遠部(candidate 非依存の定数)
      { point: "inf_plus",  e: 5, coefficient: 4 },
      { point: "inf_minus", e: 5, coefficient: 4 }
  ],
  branch = {                           # mu_* R_mu on P^1_v(閉点因子・Q-有理)
      variable: "v",
      components: [
        { ideal_generator: [0,1],        coefficient: 4 },   # v      : mu(inf_-) = 0
        { ideal_generator: [C,0,1],      coefficient: 2 },   # v^2+C  : 調和対 {s,-s}
        { at_infinity: true,             coefficient: 4 }    # v = inf: mu(inf_+) = inf
      ]
  },
  non_ramification_certificates = {     # 旧 p-locus / weierstrass-locus の再定義先
      p_locus:  { generator: monic p,  squarefree: true, coprime_to_f6: witness },  # T-3
      w_locus:  { generator: monic f6, squarefree: true, coprime_to_p:  witness },  # T-4
      claim: "contributes 0 to R_mu"    # 定理 B
  }
}
```

**照合すべき等式(commit_generation の native 一致検査 = 次の 5 本、すべて $\mathbb Q$ 上の厳密演算)**

```text
N-1  ram_finite.ideal_generator:  monic 正規化後の係数完全一致
       (既存の §4.2 reduction-to-zero 双方向 witness をそのまま使える)
N-2  ram_finite.coefficient 一致、かつ 2*deg(gen)*coefficient = 4      [有限部の次数]
N-3  ram_infinite が両 lane で {(inf_+,4),(inf_-,4)} に一致           [E5-D の帰結]
N-4  branch: 成分ごとに (ideal_generator, coefficient) の完全一致、かつ
       sum(deg(gen)*coefficient) + at_infinity.coefficient = 12 = deg R_mu   [押し出しの次数保存]
N-5  non_ramification_certificates の 2 生成元がイデアルとして一致
       (これが A の「余分な 2 成分」を B 側に受け皿を作って対応づける = 
        component_bijection が全単射になる条件)
```

**要点 1 — 分岐因子は $\mathbb Q$-有理である。** $s\notin\mathbb Q$(fixture では $s=16\sqrt5\,i/125$)でも、**閉点** $\{s,-s\}$ は $\mathbb Q$ 上既約な $v^2+C$ 一個で表される。ゆえに **$\bar{\mathbb Q}$ 算術も根の数値近似も一切不要**で、lane A の「モニック生成元」様式のまま正しく書ける。$-C$ が $\mathbb Q$ の平方のときだけ 2 成分に分裂する(その場合も係数 2 ずつ)。
**要点 2 — 無料の cross-check が二つ手に入る。** (a) 有限分岐イデアルが **degree 2 かつ even**($v^2+C$)であることは §1.8 の結論そのもの ⇒ **T-7 の一部が N-4 に吸収される**。(b) E-7(調和対)は「有限 branch 生成元が $v^2+C$ の形」と literally 同値 ⇒ **T-6 の *形* の検査が封印値に触れずに機械化できる**(封印値との照合は従来の位置に据え置き)。
**要点 3 — 封印規律**: `branch` の生成元 $v^2+C$ の $C=a^2-f_6p^2$ は candidate 由来。**既存 native が既に $d,p,f_6$ を平文で載せているので新たな露出クラスは生じない**(同一秘匿クラス)。ただし T-6 の**値**照合は §3 の sealed 扱いのまま。

### 4.2 判定 3 — 本番 bundle の native スロットに何を置くか

- **native スロット = NF(§4.1)。** spec §4.1 は両 lane が**同じ二対象**($R_\mu$ と $\mu_*R_\mu$)を持つことを要求しており、そうでなければ `component_bijection` / `exact_point_equality_witnesses` が定義できない。B 側の点ベース形式は $\bar{\mathbb Q}$ 算術を bundle に持ち込むので**そのままでは本番向きでない** — B は自分の点集合から最小多項式を取って NF へ落とす(これは B 側の独立実装)。
- **lane A の 3-loci カタログは廃棄せず「降格」する。** `searcher_native.derivation_inputs`(仮称 `tower_ingredient_loci`)として NF の**導出証跡**の位置に移し、`p-locus`/`weierstrass-locus` は §4.1 の `non_ramification_certificates`(= T-3/T-4)へ再型付けする。**lane A が計算したものは一つも無駄にならない — 型が変わるだけ。**
- **A 側に新規実装が要るのは 2 点のみ**: (i) `ram_infinite` の定数出力(V-E5.1..4 が真なら無条件、探索不要)、(ii) `branch` を v-line で書き直す($C$ は既に計算済みなので係数 $[C,0,1]$ を並べるだけ)。**探索コストはゼロ**(resultant も $\bar{\mathbb Q}$ も不要 — lane A の「searcher は resultant を使わない」規律を破らない)。

---

## 5. 副件 — E-5(orientation)についての lane B の発見

### 5.1 当否

**結論: 主張は正しい。ただし提示された論証は (Or) の半分しか出していない。**

- $\mu\mu^\iota=C\ne0$ から出るのは「$\operatorname{div}(\mu)$ の台が $\{\infty_+,\infty_-\}$ に含まれる」= $\operatorname{div}(\mu)=n\big((\infty_-)-(\infty_+)\big)$ **まで**(`e5_interpretation_v1.md` §2.2 の (1)(2)(3) に対応)。
- **$n=5$ は出ない。** spec §1.1 の (Or) は $(\mu)=5P_0-5P_\infty$ と **5 を含む**。$n=5$ には $t=1/x$ 展開 $\mu=(a_5\pm p_2)t^{-5}+O(t^{-4})$ と **E-3($a_5=p_2\ne0$)** が要る(同 §2.2 の (4))。
- **精密化(本稿で追加)**: $\deg a=5,\deg p=2$ と (Pell) の $x^{10}$ 係数 $a_5^2-p_2^2=0$ から **$a_5=\pm p_2$ は自動**。ゆえに **$|n|=5$ は E-1/E-2/E-4 だけで従い、E-3 の符号は向き($P_0$ がどちらの無限点か)だけを決める。** これが「orientation」の実体。
- ゆえに lane B の発見は **裁定 113 の命題 E5-D の独立再発見**である。lane B は spec のみから、私(2026-07-28・紙)とは別経路で同じ結論に到達した ⇒ **E5-D の二系統 cross-checked** として台帳に登録する価値がある(**verified ではない** — Lean 化していない)。

### 5.2 「caller-attested のみ」設計の変更提案(実施は司令塔裁定)

現状の齟齬(**発見**):

| lane | E-5 の扱い | 出所 |
|---|---|---|
| A | **DERIVED**(V-E5.1..4)・`orientation_declared_ok` は任意 cross-check に降格・不一致のみ [6] | `ninfty-searcher-v2.mjs` L34-46, L390-405(裁定 113 準拠) |
| B | **caller-attested only**・`"cannot be re-derived from (a,p,f6) alone"` と明記・E-5 を恒久 UNKNOWN に登録 | `ninfty-checker.py` L547, L618-620 |

**すなわち lane B の checker.py は裁定 113 に対して陳腐化しており、コメントの主張は命題 E5-D により偽である。**

提案:

```text
C-1  lane B も V-E5.1..V-E5.4 を実行して E-5 を導出する。
     追加機械は不要 — V-E5.1..4 は E-1..E-4 そのもので、lane B は既に全部計算している。
C-2  result["unknown"] から E-5 の行を削除する(UNKNOWN の水増しになっている)。
C-3  divisor_orientation_attested=False かつ V-E5.1..4 が全て真のとき:
       現状 REJECT[6]  ->  INTEGRITY_STOP へ再送。
     理由: 定理に反する attestation は「候補の欠陥」ではなく「入力の不整合」。
     spec §2 が E-6 について既に同じ判定を下している —
       「E-4 exact PASS 後の gcd(a,p)!=1 は REJECT ではなく INTEGRITY_STOP」(§2 / §5.3)。
     E-5 も E-1..E-4 からの導出条件なので、同じ型の先例に従うのが一貫する。
C-4  attestation 欠落は REJECT しない(導出値が権威)。lane A は既にこの形。
C-5  ★独立性の保全: C-1..C-4 は spec/契約レベルの条項として両 lane へ同時に降ろす。
     片方の lane へ実装を耳打ちしてはならない(§4 冒頭の独立性条項)。
     E5-D は既に共有文書 e5_interpretation_v1.md にあるので共通地であり、
     これを引くこと自体は lane 独立性を侵さない。
```

---

## 6. UNKNOWN と申告

- **UNKNOWN-1**: 本稿は $-C$ が $\mathbb Q$ の平方になる candidate が campaign 内に実在するかを調べていない(その場合 `branch` の $v^2+C$ が 2 成分に分裂する。§4.1 の N-4 は両方を扱えるが、**fixture が無い**)。
- **UNKNOWN-2**: 定理 A/B の検証は genuine fixture `checker_pos_01` **1 本**と reject 例 beta **1 本**のみ。二例は証明を代替しない(証明は §2 にあり、fixture は独立系統の確認)。
- **UNKNOWN-3**: NF(§4.1)を採ったときの `chart_overlap_witnesses` / `total_coverage_and_no_extra_component_witness` への波及は本稿の範囲外。特に `ram_infinite` を成分として数えると **coverage の全成分数が 2(A の 3-loci)から 4(finite 1 + infinite 2 + branch 3)へ変わる**ので、§4.3 の総和条項の再点検が要る。
## 7. §4.3 総和条項の再点検(UNKNOWN-3 の回答・2026-08-01 追記)

**司令塔指示 item 5 への回答。** NF 採用により旧 3-loci(finite の a-pair/p/weierstrass の 3 成分)が NF の 4 スロット(`ram_finite` 1・`ram_infinite` 2・`branch` 3・`non_ramification_certificates` は非分岐証跡なので coverage 対象外)に再編されたことで、**「全成分数 3→6」という UNKNOWN-3 の懸念は誤りだった** — 正しくは **「coverage 対象の成分数は、NF の 2 divisor object(`ram_finite`+`ram_infinite`=R_μ 側 3 成分、`branch`=μ_*R_μ 側 3 成分)にそれぞれ分かれる」**。

- `ramification_divisor_on_C` 側の coverage: **3 成分**(`ram_finite` の $\pi^*V(d)$・`ram_infinite` の $\infty_+$・$\infty_-$)。次数は $\pi^*V(d)$ が $2\deg(d)\cdot\text{coefficient}=2\cdot2\cdot1=4$(N-2 が保証)、$\infty_\pm$ が各 $4$(N-3 が保証)で、合計 $4+4+4=12=\deg R_\mu$。
- `branch_divisor_on_P1` 側の coverage: `branch` の 3 成分(v・v²+C・∞)がそのまま total_coverage の対象。N-4 の次数和検査(deg(gen)·coeff の総和 + at_infinity.coeff = 12)がこれを保証する。
- `non_ramification_certificates`(旧 p-locus/weierstrass-locus)は **R_μ の成分ではない**(定理 B の帰結)ので、coverage witness の対象から**除外**するのが正しい。§3.2 の是正(mint gate)と合わせ、`total_coverage_and_no_extra_component_witness` を NF ベースへ書き換える際は「2 divisor object × 各 3 成分」という新しい total_coverage 契約になる — 旧「1 object あたり 3 loci」からの単純な数合わせではなく、**object の意味(R_μ vs μ_*R_μ)ごとに再定義**する必要がある。
- **この再点検は bundle/commit_generation 経路の再配線を含まない**(司令塔指示: 残工程は別便)。ここでは NF 内部の N-1..N-5 検算式が新 coverage 契約を代替的に保証していることの確認に留める。UNKNOWN-3 は本節により **設計レベルでは解消**、**実装(bundle 側の `total_coverage_and_no_extra_component_witness` 生成コード)は未着手のまま**(次工程)。

## 8. 実装状況(2026-08-01 実装担当追記)

- **NF 両 lane 独立実装済み**: lane A = `search/ninfty-searcher-v2.mjs` の `computeNormalFormLaneA`(+ CLI `search/ninfty-nf-lanea-cli.mjs`)。lane B = `search/ninfty-nf-laneb.py` の `compute_normal_form_lane_b`(`search/ninfty-checker.py`/`search/ninfty-checker-native.py` という lane B 自身の既存ファイルのみに依存、lane A のコードは import していない)。
- **N-1..N-5 判定器**: `search/ninfty-nf-crosscheck.py`(第三のスクリプト・両 lane の CLI を**別プロセス**として起動し出力 JSON のみを比較・いずれのコードも import しない)。
- **mint ゲート**: 両 lane とも「REJECT ⇒ ABSENT / INTEGRITY_STOP ⇒ INTEGRITY_STOP(mint しない)/ ACCEPT(全 prerequisite + 定理強制恒等式 PASS)⇒ PRESENT」を実装(P94-4.1 準拠)。
- **E-5 C-1..C-5**: lane B(`search/ninfty-checker.py`)を修正 — E-5 を DERIVED として扱い(C-1)、`unknown` リストから削除(C-2)、attested=False が導出値と矛盾する場合は REJECT[6] ではなく新規 INTEGRITY コード `divisor-orientation-attestation-mismatch`[27] へ再送(C-3)、attestation 欠落は REJECT しない(C-4、従来どおり)。lane A(`search/ninfty-searcher-v2.mjs`)側も同じ理由で REJECT[6]→INTEGRITY[27] へ修正(C-3 は両 lane 同時適用)。
- **テスト**: `search/test_ninfty_nf.py`(genuine fixture 3 本 = PRESENT・N-1..N-5 全 PASS・nf_digest 完全一致/ beta candidate = 両 lane 揃って ABSENT・decision_lane_concordance)。既存回帰: `test_ninfty_checker_native.py` 50/50・`test_ninfty_laneB.py` 184/184・`test_ninfty_evidence_union.py` 227/227・`test_ninfty_legacy_normalizer.py` 51/51、すべて PASS(E-5 の C-1..C-5 修正による regression なし)。
- **未着手(次工程・司令塔指示どおり本便の範囲外)**: 真の bundle 生成(`buildSearcherNative`/`checkerNative` を呼ぶ既存の巨大 cert 生成コード、L680-858 付近)を NF ベースへ配線する作業、`commit_generation`/registry への mint 反映、CI 経路。§7 の total_coverage 再定義もこの配線作業の一部として未実装。

- **申告**: lane A のコードは司令塔の明示許可で読んだ(L488-549 の `buildSearcherNative` と L34-46/L285-405 の E-5 周辺、および `ninfty-checker.py` L541-626)。**lane B の checker_native(`ninfty-checker-native.py`)は読んでいない** — 判定 4 の当否は lane B の**主張の再構成**に対して行った。
- **接触規律**: 使用した数値は公開 fixture `checker_pos_01.json` と `beta_candidate.json` のみ。封印集合の係数には触れていない。
- **cross-checked / verified の区別**: 本稿の主張はすべて **紙の証明 + 1 系統の機械検算**。Lean 化していないので **verified ではない**。
