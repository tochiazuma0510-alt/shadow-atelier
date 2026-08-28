# 汎用 fibre checker 仕様 v2 —(F2)商規律版

`DIR: 972 fake 側(落下狩り)/ FRAME: B₃-gentle`
**委嘱**: 司令塔・裁定 1736(落下狩り前哨 NO-GO の根因是正)。**v1(sha16 `2878d55f90feae3c`)は改変せず並置(§2.3 に ⚠⚠⚠ を打った)。本 v2 が v1 を supersede する。**
**著者**: 数学者(Opus 5)/ 2026-08-28。

> ### ★★ 本文書の規約(**wcp5d を正本参照として明記**)
> **(R-0・新設)** **述語の正本 = `docs/notes/wcp5d_resolution_v1.md`(裁定 164/165・cross-checked)。実装の正本 = `search/wall-miner-v4.g` の `CorrectedShadows`。** 本仕様の判定述語は**すべてこれに従属**する。齟齬があれば wcp5d が勝つ。
> **(R-1)** 訂正は同ターンで本文に打つ(被訂正文は除去か ⚠ マーカ)。**(R-2)** `gate:` は述語を実際に評価した場合のみ・文書内の文字列検査は `doc-keyword:`。

---

## 0. ★ 訂正表(v1 → v2)— **私の裁定伝搬失敗の是正**

| # | v1 の記述 | 判定 | v2 |
|---|---|---|---|
| **C-1** | §2.3「**$\theta,\tau$ は語レベルで適用してから商へ落とす**」 | ❌ **致命的誤り**。裁定 164/165 が既に棄却した旧処方。**$c\notin N$ の窓で $\tau$ が降りない**(66 窓中 40 窓)⟹ **同じ群元 $f$ でも語を替えると (3.11) の値が変わる**(falsifier 較正窓で 600/600 の反転反例)⟹ **false NONMEMBER = 偽の 648 一括宣言** | **§3 の (F2) 商規律へ全面差し替え** |
| **C-2** | 必須フィールドが receipt 中心 | ⚠ 不足 | **§4**: 窓ごとの `c_in_K` / `tau_descends`(fail-closed)・`F4_isolated: NOT_EVALUATED`・`positive_recordability: NONE`・`node_id` 事前登録・`seed_key` digest(語+index) |
| **C-3** | checker は roster/verdict の再演のみ | ⚠ 不足 | **§5**: charming の $[G,G]$ 半分の**独立再導出**を必須(falsifier が 15 行 0.4 秒で実証 — 「Python 不能」申告は**不成立**)・`F2 × 1,469,664 == F5` と M ブロック位数の検査・**短絡行は `false` でなく `null`** |
| **C-4** | mandatory mutants 12 本 | ❌ **原理的に無効**。全て **receipt 改竄型**で、**producer の数学誤りを検出できない**(まさに C-1 が素通りした) | **§6**: **producer を実走させる mutant** へ再設計。筆頭 = **群元関数性 mutant**(語代表を関係子倍だけ変えて verdict 不変を要求) |
| **C-5** | 較正 6 窓(既知値との突合) | ⚠ 不足 | **§7**: **$K_2$(raw 48 / valid 2)と PΓL(2,8)(valid 9)を新実装を通して再導出**することを**本走前の必須ゲート**に |
| **C-6** | DROP 時の第二系統が未指定 | ⚠ 欠落 | **§8**: 第二系統 = **$B_3/K$ 内の full hexagon (3.3)(3.4)**(wcp5d V4 が (F2)⟺full hexagon の 100% 一致を機械確認済 = **別の数学経路**) |
| **C-7** | 段 0 は全窓の予算表のみ | ⚠ 不足 | **§9**: **最大規模窓 1 本(b3_index 1944 級・$\lvert G\rvert\sim1.5\times10^8$)を先に実測**してから venue 決定。**コスト driver は候補数でなく窓構築+warmup**(実測判明)・**8GB OOM 未評価** |

---

## 1. #fib 式の裁定(v1 §1 を維持・変更なし)

$$\#\mathrm{fib}(K)=\frac{K_{\rm ord}}{M_{\rm ord}}\cdot[M_{F_2}:K_{F_2}]\qquad(K\le M,\ M_{\rm ord}=18)$$
2 因子は GT-pair $[m,f]$ の 2 座標。**$K_{\rm ord}/M_{\rm ord}\ne[M:K]$。**$K_2$ で $\frac{36}{18}\cdot24=48$(実測一致)。詳細と再計算指示は v1 §1(**この節は誤りを含まない**)。

---

## 2. 事前計算(v1 §2.1 を拡張)

| # | 量 | 用途 |
|---|---|---|
| F1 | $K_{\rm ord}$、$M_{\rm ord}=18$、比 | $m$ 方向。整除しなければ停止 |
| F2 | $[M_{F_2}:K_{F_2}]$ | $f$ 方向 |
| F3 | $\#\mathrm{fib}=$F1×F2 | 予算確定(列挙前) |
| ~~F4~~ | ~~isolated 判定~~ | ⚠ **`NOT_EVALUATED` と記録する**(§4)。落下狩りに不要・$\diamond$ 閉包は高い |
| F5 | $\lvert PB_3/K\rvert$ | 述語評価の作業サイズ。**検査: `F2 × 1,469,664 == F5`**(§5) |
| **★ F6(新)** | **$c\in K$ か**($c$ = $PB_3$ の中心生成元) | (F1) 語規律が使えるかの判定。**$c\notin K$ なら語規律は禁止** |
| ~~**★ F7(新)**~~ | ~~**$\tau$ が $F_2/K_{F_2}$ に降りるか**~~ | ⚠⚠ **意味を再定義(2026-08-29・裁定 1759(3)(b))**: (F2) 規律下では $\tilde\tau=\mathrm{Ad}(\delta)$ は **常に $A=PB_3/K$ の自己同型**($K\trianglelefteq B_3$ から従う)⟹ 「降りるか」は**恒真で 0 ビット**。**F7 は (F1) 語規律を使う場合に限り**「$\tau$ が $F_2/K_{F_2}$ に降りるか」の意味で残す。**(F2) 単独運用なら F7 は廃止**し、欄は `NOT_APPLICABLE` とする |
| **★ F8(新)** | $\mathrm{ord}(c\bmod K)$ | (F1) を代替に使う場合の語条件 $e(w)\equiv0$ の法 |

---

## 3. ★★ 判定述語 —(F2)商規律(**v1 §2.3 の全面差し替え**)

**正本**: `docs/notes/wcp5d_resolution_v1.md` §(F2)。**実装正本**: `search/wall-miner-v4.g` の `CorrectedShadows`。

> ### 3.0 ★ 積順序の裁定(2026-08-29・裁定 1759(1))— **receipt 宣言文(逐語で載せること)**
>
> **`product_order = "tau2_tau_id"`**
> 判定式 (3.11) の積順序は **$\tilde\tau^{2}(w)\cdot\tilde\tau(w)\cdot w$**、ここで **$w=y^{m}\!\cdot\! f$**($y^m$ が**左**)。
> 典拠 = arXiv:2401.06870 Proposition 3.4 の逐語:
> $$\tau^{2}(y^{m}f)\,\tau(y^{m}f)\,y^{m}f\in N_{F_2}\tag{3.11}$$
> 同 Prop の自己書き換え (3.13) $=x^{m}f(z,x)\,z^{m}f(y,z)\,y^{m}f\in N_{F_2}$($z:=y^{-1}x^{-1}$)と**語として一致**することを機械確認済(`MO_IDENTITY_311_EQUALS_313 true`)。逆順 $w\,\tilde\tau(w)\,\tilde\tau^{2}(w)$ は (3.13) と**一致しない**(`MO_REVERSED_ORDER_ALSO_EQUALS_313 false`)⟹ **別対象**。
>
> **`word_eval_order`** — 上の順序は**評価方向と対でしか意味を持たない**:
> - `word_eval_order = "append"`(標準準同型 $F_2\to G$)⟹ 群の積を**そのままの順**で組む: `t2*t1*w`。
> - `word_eval_order = "prepend"`(反準同型 $\psi(w_1w_2)=\psi(w_2)\psi(w_1)$)⟹ 群の積を**反転**して組む: `AbstractProd([t2,t1,w])`(= `w*t1*t2` in GAP)。
>
> **⟹ 工房の既存パイプラインは `prepend`**(`EvalWordInQ` は `val := g^pow * val`)。したがって `wall-miner-v4` の `CorrectedShadows`/`RtOf` が使う `AbstractProd` の反転は**誤りではなく正しい補正**である(`suite-wp2-explorer.g` L56 の自己申告「paper 記法, 左から順 → GAP 表現; 反転規約, 実測確認済み」と整合)。
> **⟹ 規約を混ぜたものだけが誤り。** 受領票は 2 欄を必ず対で宣言し、不一致は fail-closed で停止すること。

$A:=PB_3/K$、$\tilde\theta:=\mathrm{Ad}(\Delta)|_A$、$\tilde\tau:=\mathrm{Ad}(\delta)|_A$($K\trianglelefteq B_3$ ゆえ**常に** $A$ の自己同型として well-defined)。**語を一切使わず $A$ の中で**:

$$\boxed{\ \text{(i)}\ f\cdot\tilde\theta(f)=1\quad\wedge\quad \text{(ii)}\ \tilde\tau^{2}(y^{m}f)\,\tilde\tau(y^{m}f)\,(y^{m}f)\;=\;\boxed{c^{\,m}}\quad\wedge\quad\text{(iii)}\ \langle x^{u},\,f^{-1}y^{u}f\rangle=F_2/K_{F_2}\ }$$

($u=2m+1$)。**(ii) の右辺は $1$ ではなく $c^{m}$** — ここが旧処方との差である。

**charming の半分**: $f$ は $\mathrm{DerivedSubgroup}(PB_3/K)$ を走る(実装正本と同じ)。$m$ は $\gcd(2m+1,K_{\rm ord})=1$。

**参照実装(逐語・`wall-miner-v4.g` L100–109)**:
```gap
CorrectedShadows := function(W, charmingSet)
  local out, f, m, u;  out := [];
  for f in Elements(DerivedSubgroup(W.PN)) do
    if AbstractProd([f, TH(W, f)]) <> Identity(W.Bq) then continue; fi;      # (i)  f·θ̃(f)=1
    for m in charmingSet do
      u := 2*m + 1;
      if RtOf(W, m, f) <> W.c^m then continue; fi;                            # (ii) R_τ̃ = c^m
      if Size(Group(W.x^u, AbstractProd([f^-1, W.y^u, f]))) <> Size(W.PN)
        then continue; fi;                                                    # (iii) onto
      Add(out, [m, f]);
```

> ### ⚠⚠ 訂正済(2026-08-29・裁定 1759(3)(a))— 旧記述は**誤り**
> ~~**$\sigma_1,\sigma_2$ を保持すること($B_3/K$ の marking を捨てない)。** $\tilde\theta=\mathrm{Ad}(\Delta)$・$\tilde\tau=\mathrm{Ad}(\delta)$ は $B_3/K$ の元による共役なので、**$PB_3/K$ だけでは作れない**。~~
>
> **正しい記述**: $K\trianglelefteq B_3$(NFI の定義)ゆえ $\mathrm{Ad}(g)$($g\in B_3$)は $PB_3$ と $K$ をともに保ち、**$A=PB_3/K$ の自己同型を直接誘導する**。さらにその生成子像は $x=\sigma_1^2,\ y=\sigma_2^2,\ c=(\sigma_1\sigma_2\sigma_1)^2$ の**閉形式**で書け、$\sigma_i$ を一切通らない:
> $$\tilde\theta:\ x\mapsto y,\ y\mapsto x,\ c\mapsto c\ ;\qquad \tilde\tau:\ x\mapsto y,\ y\mapsto y^{-1}x^{-1}c,\ c\mapsto c .$$
> **⟹ $B_3/K$ の構成は不要**($6\lvert Q\rvert$ の正則表現爆発も不要)。必要なのは $A=\langle\bar x,\bar y,\bar c\rangle$ のみで、$\bar c$ は既存 record の `Cp_on_L` から次数を増やさずに作れる。
> **機械裏取り**: `scratchpad/math_f6false_admarking_v1.g` — index$\le$100 の全 **150 窓**で恒等式 I1–I5 が `all_ok=true`;F6=false 窓 b3_index=96 で `theta_welldefined=true tau_welldefined=true theta^2=id=true tau^3=id=true`。
> **falsifier が per-window の `GroupHomomorphismByImages` 実検査で独立確認**(裁定 1759)。⟹ **v3 の $p$ 直接評価は原理的に正当。**
>
> $c\in K$ の窓では $\bar c=1$ となり旧式に退化する ⟹ **分岐不要・(F2) 一本で全窓を通せる。**

### 3.1 (F1) 語規律(代替・**条件つきでのみ許可**)

(3.10)(3.11) をそのまま使ってよいのは、**$f$ を表す語 $w$ が $e(w)\equiv0\ (\mathrm{mod}\ \mathrm{ord}(c\bmod K))$ を満たす場合に限る**(Prop 3.4 の仮定「$f\in[F_2,F_2]$」は**語に対する条件**;交換子語なら $e_x=e_y=0$ で自動)。
⚠ **BFS 語は一般にこれを満たさない。$c\notin K$(F6=false)の窓では $P_K$ 内で書けないので (F1) は使えない** ⟹ **(F2) が唯一の一般解**。
⟹ **既定は (F2)。(F1) を使うなら F6/F8 を検査し、語条件を cert に記録すること。**

### 3.2 ずれの公式(なぜ旧処方が壊れるか・記録)

$$\tilde\tau(\bar w)=\overline{\tau(w)}\cdot c^{\,e_y(w)},\qquad \tilde\tau^{2}(\bar w)=\overline{\tau^{2}(w)}\cdot c^{\,e_x(w)}\ \Longrightarrow\ R_{\tilde\tau}(m,f)=R_{\rm naive}(y^mw)\cdot c^{\,m+e(w)}$$
⟹ **同じ群元 $f$ でも語 $w$ の総指数和 $e(w)$ が変われば判定が変わる** = **shadow 座標 $[m,fK_{F_2}]$ の関数になっていない**。**これが 600/600 の反転反例の正体。**

---

## 4. 必須フィールド(cert・C-2)

| フィールド | 値 | 意味 |
|---|---|---|
| `predicate_rule` | `"F2_quotient"`(または `"F1_word"`) | **必須**。`F1_word` なら下 2 つも必須 |
| `c_in_K` | bool(F6) | $c\notin K$ で `F1_word` を選んだら **fail-closed で停止** |
| `tau_descends` | bool / `NOT_APPLICABLE`(F7・再定義後) | ⚠ **(F2) 運用では `NOT_APPLICABLE` 固定**(恒真ゆえ 0 ビット)。`F1_word` 使用時のみ bool で、`false` なら**停止** |
| **`product_order`**(新設・裁定 1759(1)) | `"tau2_tau_id"` 固定 | **§3.0 の宣言文を逐語で載せる。単独では意味を持たない** — 次欄と対で必須 |
| **`word_eval_order`**(新設・裁定 1759(1)) | `"prepend"` / `"append"` | **`product_order` と対で宣言。不一致は fail-closed で停止**(CV-9) |
| `word_exponent_condition` | `e(w) mod ord(c mod K) == 0` の実測 | (F1) 使用時のみ |
| **`F4_isolated`** | **`NOT_EVALUATED`** | ⚠ 落下狩りに不要。**評価していないことを明示的に書く**(空欄禁止) |
| **`positive_recordability`** | **`NONE`** | ★ **片道切符の機械化**: 非 isolated 窓では陽性($g^\ast$ が持ち上がった)を**記帳できない**(cofin v1.2 §9.2 W-4)。**このフィールドが `NONE` の cert は陽性主張に使ってはならない** |
| `node_id` | 事前登録した窓 ID | 走行前に pin(事後の窓すり替え防止) |
| `seed_key` | **語 + index の digest**(2 欄) | row 36 の同一性。**index だけ / 語だけは不可** |
| `reduction_index_order` | `"source_first"` | 既定 |
| `wcp5d_ref` | `"docs/notes/wcp5d_resolution_v1.md (裁定164/165)"` | ★ **正本参照の明示**(R-0) |

---

## 5. checker 要件の強化(C-3)

| # | 要件 | 根拠 |
|---|---|---|
| **CK-1** | **charming の $[G,G]$ 半分を独立に再導出**する($\mathrm{DerivedSubgroup}(PB_3/K)$ を checker 側で別実装で作る) | falsifier が **15 行 0.4 秒**で実装可能と実証 ⟹ **「Python では不能」という申告は不成立**。producer の $[G,G]$ を信用しない |
| **CK-2** | **`F2 × 1,469,664 == F5`** を検査($1{,}469{,}664=\lvert F_2/M_{F_2}\rvert=\lvert Q_0\rvert$) | 窓の $F_2$-部分の整合。ずれたら $K\not\le M$ か index 計算の誤り |
| **CK-3** | **M ブロック位数**の検査(窓が $M$ を正しく含むこと) | 同上 |
| **CK-4** | **短絡した行は `false` でなく `null`** | ⚠ `continue` で飛ばした候補を `false`(=判定した)と記録すると、**被覆完全性 CC-1 が偽陽性になる**。**評価していない行は `null`** |
| **CK-5** | producer/checker の **source/helper 非共有**(v1 §2.4 を維持) | — |

---

## 6. ★ mutants の再設計(C-4)— **producer を実走させる**

> **v1 の 12 本は全て receipt 改竄型**(digest を書き換えて checker が弾くかを見る)であり、**producer の数学的誤りを原理的に検出できない**。実際 **C-1 の誤りは 12 本すべてを素通りする**。⟹ **全面再設計。**

| # | mutant | 実行形 | 期待 |
|---|---|---|---|
| **★ MU-1(筆頭)** | **群元関数性 mutant** | 各候補 $f$ の**語代表を関係子倍だけ変えて** producer を**実走**させる($w\to w\cdot r$、$r\in K_{F_2}$) | **verdict が完全不変**。1 行でも変わったら **述語が shadow 座標の関数になっていない** ⟹ **即停止**(これが C-1 を検出する) |
| **MU-2** | **$c^m\to1$ 改竄** | (ii) の右辺を $1$ にして実走 | $c\notin K$ の窓で **verdict が変わる**。変わらなければ $c$ が効いていない = 実装が (F2) になっていない |
| **MU-3** | **$\tilde\tau\to\tau_{\rm naive}$** | $\mathrm{Ad}(\delta)$ を素朴 $\tau$ に差し替えて実走 | $c\notin K$ の窓で **verdict が変わる**(wcp5d の反転反例の再現)|
| **MU-4** | **$\tilde\theta$ の $\Delta$ を $\delta$ に取り違え** | 実走 | verdict が変わる |
| **MU-5** | **onto を charming に取り違え** | 実走 | verdict が変わる |
| **MU-6** | **$m$ 方向の脱落**($\#\mathrm{fib}=[M_{F_2}:K_{F_2}]$ 固定) | 実走 | $K_{\rm ord}>M_{\rm ord}$ の窓で **CC-1(被覆完全性)が発火** |
| **MU-7** | **$\#\mathrm{fib}$ を $[M:K]\cdot[M_{F_2}:K_{F_2}]$ で計算** | 実走 | CC-1 が発火 |
| **MU-8** | **seed を `symdiff_432` から取る** | 実走 | `seed_key` digest 不一致で停止 |
| **MU-9** | **W-1 reverse**(paper 語順 ↔ GAP 語順) | 実走 | verdict が変わる |
| ~~**MU-10**~~ | ~~**marking 破棄**($\sigma_1,\sigma_2$ を落として $PB_3/K$ だけで $\tilde\theta,\tilde\tau$ を作ろうとする)~~ | ~~実走~~ | ~~**構成不能で停止**~~ |
| **MU-10′**(差替・2026-08-29) | **$\tilde\tau$ の生成子像から $c$ を落とす**($y\mapsto y^{-1}x^{-1}c$ を $y\mapsto y^{-1}x^{-1}$ に) | 実走 | **F6=false 窓で判定が変わる**(F6=true 窓では不変)⟹ **陰性対照として有効**。旧 MU-10 は「構成不能」を期待していたが**構成は常に可能**なので mutant として無効 |

⚠ **MU-1 は「数学の誤りを検出する」唯一の mutant** である。**これを必ず筆頭に置き、通らなければ本走禁止。**

---

## 7. 較正の正本化(C-5)— **新実装を通した再導出を必須ゲートに**

| 窓 | 再導出すべき値 | 出所 |
|---|---|---|
| **$K_2=K_1\cap\ker(\exp_{B_3}\bmod3)$** | **raw $\#\mathrm{fib}=48$** かつ **valid lift $=2$**(R07/R40) | sol §23.11 |
| **PΓL(2,8) 窓** | **valid $=9$** | OBS-UNIF-1 第 4 行 |

> **両方を「新しい (F2) 実装を通して」再導出できること**が**本走前の必須ゲート**。
> ⚠ **既存 cert の値を引き写すのは較正ではない。**新実装が同じ数を**出す**ことを見る。
> ⚠ **OBS-UNIF-1 の 2,2,2,3,9 は GT-繊維(valid)であって raw $\#\mathrm{fib}$ ではない**(v1 §2.5 の注意を維持)。**別欄で報告。**

**参考(維持)**: 他の 4 窓($K^{(36)}\cap N_{S4}$・$K_Q$・LINS-48B・Heisenberg)は valid = 2,2,2,3。

---

## 8. DROP 時のエスカレーション契約(C-6)

`ROW36_NO_LIFT` が出たら、**第二系統は実装の別実装ではなく「別の数学経路」**を使う:

$$\boxed{\ \textbf{第二系統}=B_3/K\ \text{内の}\ \textbf{full hexagon (3.3)(3.4)}\ +\ \text{全射}\ }$$

**根拠**: wcp5d **V4** が「(F2) の述語 ⟺ $B_3/K$ 内の full hexagon (3.3)(3.4)+全射」を **W-C-p5 の全 960 候補と idx192-s4 の全候補で 100% 一致**(片側だけ真になる候補ゼロ)と機械確認済。
⟹ **(F2) と full hexagon は数学的に独立な 2 経路**であり、**両者一致で初めて `ROW36_NO_LIFT_CROSS_CHECKED`**。
⚠ **同じ (F2) を 2 回実装しても第二系統にならない**(共通仕様誤りを検出できない)。

**証明書要件 CC-1〜CC-6**(v1 §2.6)は維持。ただし **CC-2(early stop なし)は CK-4(短絡行は `null`)と合わせて読む** — `null` 行があれば **CC-1 は自動的に不合格**。

---

## 9. 段 0 の追加(C-7)— **最大規模窓を先に 1 本**

> **コスト driver は候補数($\#\mathrm{fib}$)ではなく「窓構築 + warmup」であることが実測で判明した。**⟹ $\#\mathrm{fib}$ 昇順の cheap-first は**コストの並べ替えとして不正確**。

| 段 | 内容 |
|---|---|
| **0-a** | **358 窓**すべてで F1–F3・F6–F8 を計算し `budget_table` を出す(⚠ v1 の「$\le100$ が 61 窓」は**誤読分布に基づく**ので破棄・本表で再確定) |
| **★ 0-b(新)** | **最大規模窓 1 本を実測**(b3_index 1944 級・$\lvert G\rvert\sim1.5\times10^8$)。測るのは **(i) 窓構築時間 (ii) warmup 時間 (iii) 候補 1 本あたりの述語評価時間 (iv) ピーク RSS** |
| **0-c** | **0-b の結果で venue を決める**。⚠ **8GB OOM は未評価** ⟹ **RSS が 6GB を超えたらローカル禁止**(RAM 8GB 制約)。GHA なら **falsifier 前哨必須** |
| 1 | 較正(§7)— **新実装を通した再導出**。不合格なら本走禁止 |
| 2 | 本走(モード A)。**順序は $\#\mathrm{fib}$ ではなく 0-b で得たコストモデルで決める** |
| 3 | モード B(row 71・全悉皆) |

⚠ **MONO は包含鎖上のみ**(cofin v1.2 §6.3 W-2)— 在庫窓どうしは大半が非比較なので、**順序は殺傷力の最適化ではない**(v1 の注意を維持)。

---

## 10. UNKNOWN

1. **358 窓の F6/F7($c\in K$ / $\tau$ 降下)の分布**は未測定。**$c\notin K$ の窓では (F1) が原理的に使えない**ので、(F2) 一本で通す前提でよいが、**分布は段 0-a で出すこと**。
2. **0-b の 4 数値**(構築・warmup・述語・RSS)は未実測。**8GB OOM 未評価。**
3. **wcp5d の GAP-1**((F2) の $R_{\tilde\tau}=c^m$ を 2401 Prop 3.4 から**解析的に再導出していない**)は**未解消**。本仕様はその上に乗る ⟹ **格は「wcp5d 相対」**。
4. wcp5d の **GAP-3**(「$\tau$ が降りない ⟺ 語経路が誤答」の ⟸ は未証明)⟹ **危険判定は保守側**(降りない ⟹ 危険)で使う。
5. v1 §2.8 の残項(較正窓の raw $\#\mathrm{fib}$・row 71 の $\#\mathrm{fib}$)は**未計算のまま**。
