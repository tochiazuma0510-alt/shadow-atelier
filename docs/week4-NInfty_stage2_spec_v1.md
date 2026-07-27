# $N_\infty$ searcher v2 — **stage 2 fiber-partition 述語の仕様(spec v1)**

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**司令塔委嘱(裁定 66-6 の再建線・第一歩)。**
**身分**: **spec 草案**。**凍結 → 実装は別途 implementer**(本稿は実装しない)。**Sol 監査前**。
**正典**: `sol/sol_reply_54_event_candidates.md` **F6 / F9 / F12.2**(仕様の骨格)・`docs/week4-K5_S5設計_opus_v1.md` **§3.3.5**(命題 S5-3∞)・**§3.3 命題 S5-2**(分岐型)・`docs/week4-K5_Rule1_v1_4.md`(operative)。
**接触規律**: **本稿は値に依存しない設計である。** $\hat c_\mu$・$C$・$h$・$a_5$・leading coefficient・平方類・符号・具体的な分岐値を**一切書いていない**。隔離済み 8 tuple は **shard 名 + index + digest** でのみ参照し、**係数を転記していない**(§4)。本稿の作成で行った機械計算は **(i) 恒等式 (F-1) の数値健全性検査**(乱数係数・Pell 条件を課さない一般恒等式)と **(ii) 8 tuple の digest 計算**の 2 本のみで、**候補値・$u$・平方類には触れていない**。

---

## 0. この spec が何を凍結するか(先に 8 行)

1. **stage 2 の述語を「resultant の平方性」から「fiber divisor の multiplicity partition」へ置き換える**(便 54 F6.2)。
2. **二次因子の `while` 全除去を禁止**する。代わりに **(A) 一般補題で baseline multiplicity を証明して除く**か **(B) fiber divisor を直接計算する**の 2 経路を規定し、**本 spec は (B) を第一経路、(A) を独立照合器の経路とする**(§2.2)。
3. **補題 N∞-F(fiber reduction)** を証明して、fiber 多項式を $H_v(x)=v^2-2v\,a(x)+\hat c_\mu$ に還元する(§1.3)。これにより stage 2 は **degree-5 多項式 $a$ の臨界値の分解**に帰着し、exact 有理演算だけで閉じる。
4. **$x=0$ chart を明示検査する**。「$s=\infty$ だから artifact」で幾何点を捨てない(便 54 F9.1-2)。
5. **判定は $2^21$ を multiplicity partition として直接検査**する。$3\,1^2$ との区別は `triple_gcd_degree` で行う(§2.4)。
6. **分岐値は sealed field**。人間可視 certificate には **digest と partition のみ**(§3・§6)。**理由は補題 N∞-L(§1.5)** — 分岐値の平方が $\hat c_\mu$ を決め、平方類が (P1) を決めるため。
7. **隔離済み 8 tuple を全件 negative regression fixture** として事前登録(§4)。**期待 verdict は `REJECT / triple-fiber-at-x0`**。
8. **end-to-end 陽性コントロールが 1 件揃うまで、探索器の札は `partial predicate / UNKNOWN`**(便 54 F9.1-6・§5)。

> **⚠ 本 spec 自体の状態札**: `spec draft / single-mathematician / 未監査`。**§1 の補題 N∞-F・N∞-P・N∞-L は本稿発の導出**であり、**Sol 監査を経てから凍結すること**。実装着手は凍結後(便 54 F9.2 末「exact fiber-partition specification を文書で先に凍結し、その後に二実装を作る」)。

---

## 1. 数学的基礎(spec が依拠する命題)

### 1.1 設定と記号(すべて S5 §3.3.5 / Rule 1 から)

$$ C:\ y^2=f_6(x),\quad \deg f_6=6,\qquad \mu=a(x)+p(x)\,y,\quad \deg a=5,\ \deg p=2, $$
$$ \textbf{(Pell)}\qquad N(\mu)=\mu\,\mu^\iota=a(x)^2-f_6(x)\,p(x)^2=\hat c_\mu\in\mathbb Q^\times\ (\textbf{定数}) $$
($\iota$ は超楕円対合)。**$\mu:C\to\mathbf P^1$ は次数 5**、$(\mu)=5P_0-5P_\infty$(S5 命題 S5-2)。

> **求める分岐型**(S5 命題 S5-2): $(5,\ 2^21,\ 2^21,\ 5)$。すなわち
> - $v=0$ 上: 1 点で $e=5$、$v=\infty$ 上: 1 点で $e=5$、
> - **有限かつ非零の分岐値がちょうど 2 個**で、**各々 partition $2^21$**、
> - **それ以外に分岐値は無い**。
>
> **Riemann–Hurwitz 検算**: $2\cdot2-2=5(0-2)+\sum(e-1)\Rightarrow\sum(e-1)=12=\underbrace{4+4}_{P_0,P_\infty}+\underbrace{2+2}_{2\times 2^21}$ ✓。

### 1.2 $\iota$ による分岐値集合の対称性

$\mu^\iota=\hat c_\mu/\mu$ だから、**分岐値集合は $v\mapsto\hat c_\mu/v$ で安定**である。

### 1.3 補題 N∞-F(fiber reduction)【**本稿発・要監査**】

> **補題 N∞-F.** (Pell) の下で、$v\in\mathbb P^1\smallsetminus\{0,\infty\}$ の fiber は、$x$-line 上の多項式
> $$ \boxed{\ H_v(x)\ :=\ (v-a(x))^2-p(x)^2f_6(x)\ =\ v^2-2v\,a(x)+\hat c_\mu\ } \tag{F-1} $$
> の零点と(重複度込みで)対応する。さらに $v\ne0$ なら
> $$ \boxed{\ H_v(x)\ =\ -2v\Bigl(a(x)-w\Bigr),\qquad w:=\frac{v^2+\hat c_\mu}{2v}\ } \tag{F-2} $$
> であり、**$\mu$ の $v$ 上の multiplicity partition は、$a(x)-w$ の根の multiplicity partition に一致する**。

**証明.** $\mu(x,y)=v$ は $py=v-a$。$C$ 上では $y^2=f_6$ だから両辺を 2 乗して $p^2f_6=(v-a)^2$、すなわち $H_v(x)=0$。逆に $H_v(x_0)=0$ かつ $p(x_0)\ne0$ なら $y_0:=(v-a(x_0))/p(x_0)$ は $y_0^2=f_6(x_0)$ を満たし、$Q=(x_0,y_0)\in C$ で $\mu(Q)=v$。
(F-1) の第 2 の等号は展開して (Pell) を代入するだけ:
$$(v-a)^2-p^2f_6=v^2-2va+\underbrace{(a^2-f_6p^2)}_{=\hat c_\mu}.$$
$\deg_x H_v=5$($v\ne0$・$\mathrm{lc}=-2v\,\mathrm{lc}(a)\ne0$)で $\deg\mu=5$ だから、根は重複度込みで fiber と 1:1。(F-2) は (F-1) を $-2v$ でくくるだけ。
$Q=(x_0,y_0)$ で $f_6(x_0)\ne0$ なら $x$ は $Q$ の uniformizer だから $e_Q(\mu)=\mathrm{ord}_{x_0}(\mu-v)=\mathrm{ord}_{x_0}(H_v)=\mathrm{ord}_{x_0}(a-w)$。∎

> **⚠ 補題 N∞-F の適用条件(実装が必ず検査する)**:
> **(F-a)** $p(x_0)\ne0$ — $p$ の零点上では $y$ が消去できないので**別扱い**(§2.5)。
> **(F-b)** $f_6(x_0)\ne0$ — Weierstrass 点($\iota$ の固定点)では $x$ が uniformizer でないので**別扱い**(§2.5)。
> **(F-c)** $v\ne0,\infty$ — $v=0,\infty$ は §2.6 で別に扱う。
> **これらを検査せずに (F-2) を使うことを禁止する。**

### 1.4 系 N∞-P(partition 判定)【**本稿発・要監査**】

> **系 N∞-P.** (F-a)(F-b)(F-c) が成り立つ $v$ について、$w=(v^2+\hat c_\mu)/(2v)$ と置くと
> $$ \mu^{-1}(v)\ \text{の partition}=2^21 \iff \deg\gcd(a-w,\ a')=2,\ \ \gcd(a-w,a')\ \text{squarefree},\ \ \gcd(a-w,a',a'')=1 $$
> である。**$3\,1^2$ のときは $\gcd(a-w,a',a'')\ne1$**(または $\gcd(a-w,a')$ が重根をもつ)。

**証明.** $\deg(a-w)=5$。partition が $2^21$ ⟺ 相異なる二重根 2 個と単純根 1 個。$\gcd(a-w,a')$ はちょうどそれら二重根を単純に含み degree 2・squarefree。三重根があれば $a''$ もそこで消えるので $\gcd(a-w,a',a'')\ne1$。∎(便 54 F9.1-3 の 3 条件と逐語一致)

> **★ 8 hit の棄却がこの系で説明される**(便 54 F6): 当該 tuple は $a'=\epsilon\,5x^2p$、$p(0)\ne0$ を満たすので $\mathrm{ord}_0(a')=2$、すなわち $a-a(0)$ は $x=0$ で**三重根**をもつ。partition は $3\,1^2$ で $2^21$ ではない。**本 spec の判定はこれを `triple_gcd_degree>0` で直接拒否する。**

### 1.5 補題 N∞-L(leakage)【**便 54 F12.4 の再掲・sealing の根拠**】

> **補題 N∞-L.** 有限分岐値の集合が $\iota$-安定で、かつ **2 個の有限分岐値がそれぞれ $\iota$-固定**であるとき、その分岐値 $s$ は $s^2=\hat c_\mu$ を満たす。

**証明.** §1.2 より分岐値集合は $v\mapsto\hat c_\mu/v$ で安定。§1.1 の分岐型では有限分岐値は 2 個で、両方とも partition $2^21$。(F-2) より同じ $w$ を与える 2 値 $v,\hat c_\mu/v$ は**同じ partition**をもつ。この 2 個が互いに移り合うなら $w$ は 1 個しかなく、$a'$ の 4 根のうち 2 根しか消費できず $\sum(e-1)=4$ に足りない。ゆえに**各分岐値は $\iota$-固定**、すなわち $v=\hat c_\mu/v$、$v^2=\hat c_\mu$。∎

> **⇒ sealing の根拠**: **分岐値を 1 つ開示すると $\hat c_\mu$ が($\pm$ を除いて)決まり、その平方類が (P1) を決める**(S5 命題 S5-4∞: $(N_\infty)$ では $\hat c=1$ ゆえ $\hat c_\mu$ 単独で (P1) が決まる)。**したがって分岐値・その平方・平方類は I-b∞ の禁止量である**(§6)。**本 spec は分岐値を certificate の sealed field に置く。**

---

## 2. stage 2 述語の定義(便 54 F9.1 の 6 条件の条文化)

**入力**: tuple $(a,p,f_6)$(exact 有理係数)。**出力**: 三値 verdict $\in\{\texttt{ACCEPT},\texttt{REJECT},\texttt{INTEGRITY\_STOP}\}$ + reason code + §3 の certificate。

### 2.0 事前条件(満たさなければ `REJECT / precondition`)

| # | 条件 | reason code |
|---|---|---|
| P-1 | $\deg a=5$・$\deg p=2$・$\deg f_6=6$ | `degree-mismatch` |
| P-2 | $f_6$ が squarefree(曲線が非特異) | `curve-not-squarefree` |
| P-3 | $a^2-f_6p^2$ が**定数**かつ非零(= (Pell)) | `pell-violation` |
| P-4 | $\gcd(a,p,f_6)$ の共通根なし(退化排除) | `common-root` |

### 2.1 条件 1 — 二次因子の除去を禁止

> **【禁止】** `stripKnownQuadraticFactor` 型の「割れる限り除去」(`while`)を**使ってはならない**。
> **【許される 2 経路】**
> - **(A) baseline 経路**: 固定次数 Sylvester 行列が強制する baseline multiplicity を**一般補題として証明**し、**その分だけ**除く。**証明を certificate に proof ID で束縛**する。
> - **(B) divisor 経路(本 spec の第一経路)**: **resultant を使わず**、homogeneous / two-chart で **fiber divisor を直接計算**する。
>
> **本 spec は (B) を第一実装(searcher v2)、(A) を独立照合器(§5)の経路とする。**
> **理由**: 便 54 F6.1 の事故は (A) の baseline を 1 と誤仮定したことによる。**(B) は baseline の概念自体を持たない**ので同型の事故が起きない。**二実装が別経路であることは F9.2 の「別実装」要件も同時に満たす。**

### 2.2 条件 2 — $x=0$ chart の明示検査

> **$x=0$ を含む有限 chart を明示的に検査する。** 「$s=\infty$ だから artifact」という理由で**幾何点を捨ててはならない**。
> **実装要件**: fiber の計算は **$x$-chart と $x=\infty$ chart(斉次座標 $[X:Z]$、$Z=0$)の 2 chart を両方**走る。各 chart で得た divisor を貼り合わせ、**degree の総和が 5 であること**を assert する(不一致は `INTEGRITY_STOP / chart-degree-mismatch`)。

### 2.3 条件 3 — 分岐値集合の決定(exact)

**手順**(経路 (B)):
1. $a'$ を計算($\deg a'=4$)。
2. $a'$ の squarefree 分解と、**臨界値集合** $W:=\{a(x_i):a'(x_i)=0\}$ を **exact に**求める。実装は $x_i$ を数値で求めず、**$\mathrm{Res}_x(a-W,\ a')$ の $W$-多項式**(= $a$ の critical-value polynomial)$\Delta_a(W):=\mathrm{Res}_x(a(x)-W,\ a'(x))$ を計算し、その根として $W$ を扱う。**$\Delta_a$ は $\mathbb Q[W]$ の多項式で degree 4。**
3. 各臨界値 $w$(= $\Delta_a$ の根)に対し、対応する分岐値は $v^2-2wv+\hat c_\mu=0$ の 2 根。§1.5 より**要求される分岐型では $w^2=\hat c_\mu$**、すなわち $v=w$(重根)。
4. **判定に使うのは $\Delta_a$ の根の重複度構造と、各根での partition のみ。$w$ の値そのものは sealed field へ入れる。**

> **注(実装の自由度)**: 上の 2–3 は「$\Delta_a$ を factor して各既約因子ごとに partition を検査する」形でも、「$a'$ の squarefree 分解から直接 partition を組む」形でもよい。**要求は「exact であること」と「$w$ を人間可視出力に出さないこと」だけ**である。

### 2.4 条件 4 — $2^21$ を multiplicity partition として検査

各分岐値($v\ne0,\infty$)について、**系 N∞-P の 3 条件を exact に検査**する:

$$ \boxed{\ \deg\gcd(H,H')=2,\qquad \gcd(H,H')\ \text{squarefree},\qquad \deg\gcd(H,H',H'')=0\ } $$

ここで $H$ は当該 fiber の **飽和した degree-5 fiber 多項式**($=H_v$、または経路 (B) では chart ごとの fiber divisor から組んだもの)。

| 記録欄 | 意味 | `ACCEPT` の要件 |
|---|---|---|
| `fiber_degree` | $\deg H$(chart 合算) | $=5$ |
| `multiplicity_partition` | 重複度の降順列 | $[2,2,1]$ |
| `gcd_degree` | $\deg\gcd(H,H')$ | $=2$ |
| `gcd_squarefree` | $\gcd(H,H')$ が squarefree | `true` |
| `triple_gcd_degree` | $\deg\gcd(H,H',H'')$ | $=0$ |

> **$3\,1^2$ の拒否**: `triple_gcd_degree>0` または `gcd_squarefree=false` ⟹ **`REJECT / triple-fiber`**。$x=0$ で起きた場合の reason code は **`triple-fiber-at-x0`**(§4 の negative fixture が期待する値)。

### 2.5 退化点の別扱い(補題 N∞-F の適用条件)

| 場合 | 扱い | reason code(違反時) |
|---|---|---|
| $p(x_0)=0$ かつ $x_0$ が fiber に属する | (F-2) を使わず、**その点で $\mu$ の局所式を直接展開**して $e$ を求める | `p-vanishing-unhandled` |
| $f_6(x_0)=0$(Weierstrass 点) | $x$ が uniformizer でないので **$y$ を uniformizer として** $e$ を求める | `weierstrass-unhandled` |
| 上記の点で `INTEGRITY_STOP` に落ちる条件 | **未処理のまま partition を出力した場合** | `INTEGRITY_STOP / unhandled-chart` |

> **「未処理は UNKNOWN でなく INTEGRITY_STOP」**(便 54 F9.2)。

### 2.6 条件 5 — $v\in\{0,\infty\}$ の全分岐性

$$ (\mu)=5P_0-5P_\infty\ \Longrightarrow\ \mu^{-1}(0)=\{P_0\}\ (e=5),\quad \mu^{-1}(\infty)=\{P_\infty\}\ (e=5). $$
**これを assert する**(divisor 恒等式の再計算)。破れは **`INTEGRITY_STOP / divisor-identity`**(入力破損)。

### 2.7 条件 6 — 分岐値が所望集合以外に無いこと(projective 検査)

> **`projective_coverage`**: **2 chart の分岐 divisor を合算し、$\sum(e_Q-1)=12$**(Riemann–Hurwitz)**であることと、分岐値の総数が $\{0,\infty\}$ + **ちょうど 2 個の有限値**であることを assert する。
> 余分な分岐値が 1 個でもあれば **`REJECT / extra-branch-value`**。合算が 12 にならなければ **`INTEGRITY_STOP / rh-mismatch`**(chart 取りこぼしの検出器)。

### 2.8 `ACCEPT` の定義(閉じた列挙)

$$ \texttt{ACCEPT}\iff \text{P-1..P-4} \wedge \text{§2.2 の chart 合算} \wedge \text{§2.6} \wedge \bigl(\text{有限分岐値が 2 個}\bigr)\wedge\bigl(\text{各々 §2.4 の 5 欄をすべて満たす}\bigr)\wedge\text{§2.7} $$
**それ以外はすべて `REJECT` か `INTEGRITY_STOP`。中間札は作らない。**

---

## 3. fiber-partition certificate schema(便 54 F12.2)

```text
schema            = "mb/ninfty-fiber-partition/v1"
candidate_id                       # 入力 tuple の digest(値は含まない)
input_digest                       # canonical (a,p,f6) の sha256
searcher_id, searcher_digest       # 実装 artifact の束縛
predicate_spec_id                  # 本 spec の ID + digest(§8)
verdict                            # ACCEPT | REJECT | INTEGRITY_STOP
reason_code                        # 閉じた enum(§7)

# --- fiber ごと(有限分岐値 + 0 + infinity)---
fibers = [
  {
    chart_id                       # "x-affine" | "x-infinity"
    fiber_degree                   # int
    multiplicity_partition         # 降順 int 配列(例 [2,2,1])
    gcd_degree                     # int
    gcd_squarefree                 # bool
    triple_gcd_degree              # int
    branch_value_ref               # SEALED(下記)
  }, ...
]

projective_coverage = {
  charts_covered                   # ["x-affine","x-infinity"]
  ramification_sum                 # sum(e-1) — 12 を期待
  finite_branch_value_count        # 2 を期待
  total_branch_value_count         # 4 を期待(0, infinity, 有限 2 個)
}

# --- sealed 区画(人間可視 certificate には出さない)---
sealed = {
  branch_values                    # SEALED
  branch_value_digests             # 人間可視にはこちらだけ
  critical_value_polynomial        # SEALED(Delta_a)
}
```

> **人間可視 certificate に出してよいのは**: `candidate_id`・`input_digest`・`verdict`・`reason_code`・`multiplicity_partition`・`gcd_*`・`triple_gcd_degree`・`projective_coverage` の各 int/bool・`branch_value_digests`。
> **出してはならない**(便 54 F9.2 逐語): **$C$・$h$・$a_5$・leading coefficient・平方類・因数・符号**、および**分岐値そのもの**(§1.5 補題 N∞-L)。**ログ・例外文・fixture 名にも出さない。**

---

## 4. negative regression fixtures(隔離済み 8 tuple 全件)

**事前登録**(便 54 F9.1-5)。**tuple は `certificates/mb/actions/30289323147/` の生証明書から参照のみ。値の再計算・転記をしない。**

| # | shard file | hit index | shard sha256[:16] | tuple digest[:16] | 期待 verdict / reason |
|---|---|---:|---|---|---|
| 1 | `ninfty-b5-a5m-p21.json` | 0 | `d40d077833cfadbb` | `b22e3380f09b0707` | `REJECT / triple-fiber-at-x0` |
| 2 | `ninfty-b5-a5m-p21.json` | 1 | `d40d077833cfadbb` | `1499fefed2c9164c` | 同上 |
| 3 | `ninfty-b5-a5m-p2m1.json` | 0 | `c17c4a2bb1972b58` | `b5214efa30f7bcc5` | 同上 |
| 4 | `ninfty-b5-a5m-p2m1.json` | 1 | `c17c4a2bb1972b58` | `b0cb0e31f1906dd0` | 同上 |
| 5 | `ninfty-b5-a5p-p21.json` | 0 | `831b6dd9b448e13e` | `28a5f4d67fb18dec` | 同上 |
| 6 | `ninfty-b5-a5p-p21.json` | 1 | `831b6dd9b448e13e` | `9e5f774bf7c42ee4` | 同上 |
| 7 | `ninfty-b5-a5p-p2m1.json` | 0 | `6794d00e0e3302dd` | `f5b08938ae0f7772` | 同上 |
| 8 | `ninfty-b5-a5p-p2m1.json` | 1 | `6794d00e0e3302dd` | `6fbc3097e77225b0` | 同上 |

- **tuple digest** = `sha256(canonical_json({a,p,f6}))`(キー辞書順・空白なし)。**値を出さずに同一性を固定するための ID。**
- 8 件とも生証明書の `quadratic_artifact_power` は同一値であり、**便 54 F6.1 の「予想した artifact power を超えた」= integrity alarm** に対応する。**v2 はこの field を持たない**(概念ごと廃止)。
- **fixture 名に値・符号・平方類を含めない。**`ninfty-neg-01` … `ninfty-neg-08` を推奨。
- **期待 partition**: `[3,1,1]`、`triple_gcd_degree > 0`。**この 2 欄が一致することまでを回帰の合格条件とする**(verdict だけの一致では、別の理由で偶然 REJECT になった場合を見逃す)。

> **⚠ 救済禁止**: `RETRACTED_AS_CANDIDATE.md` のとおり、**これらを候補として引用・救済・照合器入力にしてはならない**。**negative fixture としての参照のみ**が許される。

---

## 5. end-to-end 陽性コントロール要件(便 54 F9.1-6)

> **要件 EP**: **実曲線・実写像から出発する陽性例を 1 件**用意する。すなわち
> **(EP-1)** 明示の $(a,p,f_6)$ で (Pell) を満たすもの、
> **(EP-2)** その $\mu$ が $(5,2^21,2^21,5)$ を実現すること、
> **(EP-3)** それを **stage 2 述語が `ACCEPT` すること**、
> **(EP-4)** 独立照合器(§6)も `ACCEPT` すること。
>
> **synthetic な resultant pattern は EP の代わりにならない**(便 54 F6.1: それが今回の事故の直接原因)。

> **状態札の規約**:
> $$ \boxed{\ \text{EP が 1 件も無い間、探索器の札は }\texttt{partial predicate / UNKNOWN}\ } $$
> **`candidate detector calibrated` と書いてはならない。** EP が揃った時点で初めて `detector calibrated (1 positive control)` へ上げる。
> **EP が $K^{(5)}$ の本番 tuple であってはならない**(封印違反)。**別の $(f_6,\deg)$ 設定で作った教材例**とし、**その旨を certificate に `positive_control_scope="synthetic-curve, non-campaign"` として明記**する。

---

## 6. 独立照合器の要件(便 54 F9.2)

| # | 要件 | 実装上の意味 |
|---|---|---|
| V-1 | **helper 非共有** | `mb-frac.mjs`・`mb-polyops.mjs`・resultant helper を **import しない**。有理数演算・多項式演算を独立に持つ |
| V-2 | **別実装** | exact arithmetic と **projective fiber calculation** を別に書く。**§2.1 の経路 (A) を使う**(searcher v2 は経路 (B))— **同じ predicate の 2 経路** |
| V-3 | **canonical input digest へ束縛** | `input_digest` が一致しない入力を受け付けない |
| V-4 | **再計算する項目** | curve squarefree / norm(Pell)・divisor 恒等式 / **全 fiber partition** / branch set / degree・genus |
| V-5 | **mismatch は `INTEGRITY_STOP`** | **`UNKNOWN` へ丸めない**。未処理 chart・飽和失敗も同様 |
| V-6 | **pre-Freeze 2 の人間可視出力の限定** | `candidate_id`・`input_digest`・`output_digest`・三値 verdict・`reason_code`・`partition_ok` 等の**非漏洩 boolean のみ** |
| V-7 | **禁止語彙** | $C$・$h$・$a_5$・leading coefficient・平方類・因数・符号を**ログ / 例外文 / fixture 名**へ出さない |
| V-8 | **投入時点** | **v1 hit を照合器へ渡して救済しない**。**v2 の全域再走の出力に対して**新設 |

> **★ 二 checker の一致は「正しい predicate」を前提として初めて意味をもつ**(便 54 F9.2 末)。**ゆえに本 spec の凍結が先。**

---

## 7. reason code(閉じた enum)

```text
# REJECT
precondition/degree-mismatch, precondition/curve-not-squarefree,
precondition/pell-violation, precondition/common-root,
triple-fiber, triple-fiber-at-x0,
partition-mismatch, extra-branch-value, finite-branch-count-mismatch

# INTEGRITY_STOP
chart-degree-mismatch, unhandled-chart, p-vanishing-unhandled,
weierstrass-unhandled, divisor-identity, rh-mismatch,
digest-mismatch, checker-mismatch, sealed-field-leak
```
**未知の reason code は fail-closed**(記録を拒否して停止)。

---

## 8. dependency-typed whitelist — $N_\infty$ 節(便 54 F12.1)

各出力 field に次を持たせる。

```text
semantic_quantity
determines_prediction = [P1, P2, ...]
release_stage          = {pre-freeze2, post-freeze2}
branch_scope           = {W, N_aff, N_infty}
```

**$N_\infty$ の機械可読規則**(登録必須):

```text
rule: branch_value_square -> squareclass(c_hat_mu) -> P1
  semantic_quantity      = branch_value_square
  determines_prediction  = [P1]
  release_stage          = post-freeze2
  branch_scope           = N_infty
  aliases_blocked        = [branch_value, s^2, mu_norm_constant, c_hat_mu,
                            squareclass(c_hat_mu), sqfree(c_hat_mu),
                            sign(c_hat_mu), h, discriminant_leading_class]
```

> **「名前を変えただけの同値量」も gate で拒否する**(便 54 F12.1)。**上の `aliases_blocked` は列挙であって網羅ではない** — **新しい量を出力に足すときは、それが $\hat c_\mu$ の平方類を決めないことを示す 1 行を添える**ことを規則とする(**挙証責任は追加側**)。
> **根拠**: §1.5 補題 N∞-L(便 54 F12.4)+ S5 命題 S5-4∞(**$(N_\infty)$ では $\hat c_\mu$ 単独で (P1) が決まる**)。**Rule 1 v1.3 §9.2 の I-b∞ の具体例として参照する。**

---

## 9. 前件表の型列挙(★教材 T7 様式)

| # | 前件 | 型 | 状態 | 本 spec での用途 |
|---|---|---|---|---|
| **S-1** | $C:y^2=f_6$、$\deg f_6=6$、$C$ 非特異 | **凍結文**(S5 §3.3) | 閉 | P-1・P-2 |
| **S-2** | $\mu=a+py$、$\deg a=5$、$\deg p=2$ | **凍結文**(S5 §3.3.5 命題 S5-3∞) | 閉 | P-1 |
| **S-3** | (Pell) $a^2-f_6p^2=\hat c_\mu\in\mathbb Q^\times$ | **凍結文**(同上) | 閉 | P-3・補題 N∞-F |
| **S-4** | $(\mu)=5P_0-5P_\infty$・分岐型 $(5,2^21,2^21,5)$ | **凍結文**(S5 命題 S5-2) | 閉 | §2.6・§2.7 |
| **S-5** | $\hat c=1$ ゆえ $\hat c_\mu$ 単独で (P1) が決まる | **凍結文**(S5 命題 S5-4∞) | 閉 | §8 の sealing 根拠 |
| **N-1** | **補題 N∞-F**(fiber reduction) | **導出(本稿発)** | **未監査** | §2.3・§2.4 の第一経路 |
| **N-2** | **系 N∞-P**(partition 判定) | **導出(本稿発)** | **未監査** | §2.4 |
| **N-3** | **補題 N∞-L**(leakage) | **導出(本稿発)**・便 54 F12.4 と同内容 | **未監査**(F12.4 は Sol 発) | §8 |
| **R-1** | 二次因子の while 全除去禁止 | **規約**(便 54 F6.2) | 閉 | §2.1 |
| **R-2** | 分岐値 sealed・非漏洩 boolean 限定 | **規約**(便 54 F9.2・F12.2) | 閉 | §3・§6 |
| **R-3** | mismatch は `INTEGRITY_STOP` | **規約**(便 54 F9.2) | 閉 | §2.5・§7 |
| **R-4** | EP が無い間は `partial predicate / UNKNOWN` | **規約**(便 54 F9.1-6) | 閉 | §5 |

---

## 10. 出所対応表(P56-1 5 欄)

| spec 条項 | 出所文書 | §・式番号 | 引用の型 | 状態 |
|---|---|---|---|---|
| §2.1 条件 1(while 禁止・2 経路) | 便 54 | F9.1-1・F6.1・F6.2 | **要約**(2 経路への分割は本稿の設計判断) | 凍結候補 |
| §2.2 条件 2($x=0$ chart) | 便 54 | F9.1-2 | **逐語** | 凍結候補 |
| §2.4 条件 3($2^21$・3 条件) | 便 54 | F9.1-3 | **逐語**(3 条件の式まで) | 凍結候補 |
| §2.7 条件 4(projective) | 便 54 | F9.1-4 | **要約**(RH 合算の実装形は本稿発) | 凍結候補 |
| §4 negative fixtures | 便 54 | F9.1-5 | **逐語**(`triple-fiber-at-x0`) | 凍結候補 |
| §5 EP 要件・札 | 便 54 | F9.1-6 | **逐語**(`partial predicate / UNKNOWN`) | 凍結候補 |
| §6 独立照合器 V-1..V-8 | 便 54 | F9.2 | **逐語**(禁止語彙まで) | 凍結候補 |
| §3 certificate schema | 便 54 | F12.2 | **逐語**(7 欄)+ 本稿の拡張(`projective_coverage` の内訳・`sealed` 区画) | 凍結候補 |
| §8 whitelist 規則 | 便 54 | F12.1・F12.4 | **逐語**(規則行)+ `aliases_blocked` は本稿発 | 凍結候補 |
| §1.1 設定・分岐型 | S5 設計 v1.2 | §3.3.5(命題 S5-3∞)・§3.3(命題 S5-2) | **逐語** | 凍結済(S5 側) |
| §8 sealing 根拠 | S5 設計 v1.2 | §6.2(命題 S5-4∞) | **逐語** | 凍結済(S5 側) |
| §1.3 補題 N∞-F | — | — | **本稿発の導出** | **未監査** |
| §1.4 系 N∞-P | — | — | **本稿発の導出** | **未監査** |
| §1.5 補題 N∞-L | 便 54 | F12.4 | **同内容の独立導出**(本稿は $\iota$-固定性の論証を追加) | **未監査** |
| §2.5 退化点の別扱い | — | — | **本稿発**(補題 N∞-F の適用条件から) | **未監査** |

---

## 11. Sol への監査依頼(凍結前)

1. **【必須】補題 N∞-F** — (F-1) の第 2 等号は (Pell) の代入だけだが、**「根と fiber の 1:1(重複度込み)」の論証**、とくに **$p(x_0)=0$ と Weierstrass 点の扱い**(§2.5)が過不足ないか。
2. **【必須】系 N∞-P** — 便 54 F9.1-3 の 3 条件と**完全に同値**か。$H$ が「適切に飽和した degree-5」でない場合(chart 合算後)にも成り立つ形になっているか。
3. **【必須】補題 N∞-L の $\iota$-固定性の論証** — 「2 個の有限分岐値が互いに移り合うと $a'$ の 4 根を消費できない」という数え上げ。**RH の $\sum(e-1)=12$ と整合しているか。**
4. **【推奨】§2.1 の経路分割**(searcher = (B) divisor / checker = (A) baseline)が **F9.2 の「別実装」要件を満たす**か。**同じ predicate の 2 経路**という設計でよいか。
5. **【推奨】§4 の回帰合格条件**を「verdict + `multiplicity_partition` + `triple_gcd_degree`」の 3 欄一致としたこと(verdict 単独では偶然の REJECT を見逃す)。
6. **【推奨】§8 の `aliases_blocked` を「列挙であって網羅ではない」とし、挙証責任を追加側に置いた**こと。

---

## 12. 実装着手の条件(まとめ)

$$ \boxed{\ \text{本 spec の Sol 監査 PASS}\ \longrightarrow\ \text{spec 凍結(ID+digest 発行)}\ \longrightarrow\ \text{searcher v2 と独立照合器を}\ \textbf{別々に}\ \text{実装}\ } $$

- **spec 凍結前に実装を始めない**(便 54 F9.2 末)。
- **searcher v2 は経路 (B)、照合器は経路 (A)。実装者を分ける**ことが望ましい。
- **EP(§5)が揃うまで札は `partial predicate / UNKNOWN`。**
- **v1 の 8 hit は negative fixture としてのみ使う。**
