# Sol 便 147 返信

## 進行記録 0 — 受領

- 受信便 `ops/inbox_codex/sol_task_147_settle.txt` を全行・全番号節について受領した。
- 受信便 SHA-256: `9df856dfd200576fe35ec7b0e04dd8572fdae1e49c910cf008082700bc69a635`。
- 本便だけを現行委嘱として扱い、972 roof の A/B 二択を根拠付きで裁定する。

## 進行記録 1 — 二択の必要十分条件を再固定

以下では正典どおり

\[
A_{\rm ar}:=\operatorname{Im}(G_{\mathbf Q}\to GT(M)),\qquad
P_M:=\mathcal{PR}_M(\widehat{GT}_{\rm gen})
\]

と置く。既確定の $M$ isolated、

\[
|GT(M)|=972,\qquad |A_{\rm ar}|=324,\qquad
A_{\rm ar}\le P_M\le GT(M)
\]

から、指数 $3$ の素数性により

\[
P_M=A_{\rm ar}\quad\text{または}\quad P_M=GT(M)
\tag{1}
\]

である。従って 648 個が一斉に A 型または一斉に B 型になること自体は確定している。
ただし (1) は二択を作るだけで、そのどちらかを選ぶ根拠ではない。

A 側の十分条件は、ある $g\in GT(M)\setminus A_{\rm ar}$ と isolated 細分
$K\le M$ に対する空 reduction fiber

\[
R_{K,M}^{-1}(g)=\varnothing
\tag{2}
\]

一件である。B 側の十分条件は、全 isolated 細分での survival、同値に cofinal
族上の互換な逆極限元の構成である。有限個の窓で像が 972 だったことは、この全称命題を
含意しない。

## 進行記録 2 — 現証明書の最終監査

- A 側: (2) を満たす組は現台帳に一件もない。
- 型付き B4 窓 $\widetilde K=C_M\cap\widetilde{\mathbf N}^{*}$ は全 972 target で
  PASS fiber 非空 (`TYPED-FIBER-ALLPASS-143`)。
- 正しい四つの $Q_8$ 窓との型付き交叉も 972/972
  (`Q8-TYPED-ALLPASS-143B`)。
- 最初の非自明な ISO order event、kernel $C_2$ の三 marked orbit も全て isolated、
  reduction image 972、zero fiber 0 (`C2-EVENT-ALLPASS-143B`)。
- B 側: 上の窓族は cofinal でない。三つの index-2 kernel の交叉より下に入るものが
  この三行族にないため、局所全通過を COMPACT へ上げられない。
- `NO-FINITE-B-140` の抽象逆系反例により、任意の noncofinal な有限観測が全て 972
  でも B は論理的に従わない。
- B4 pentagon の有限 PASS/FAIL は Drinfeld $\widehat{GT}$ 水準の必要条件であり、
  正典の A/B が定義される $\widehat{GT}_{\rm gen}$ 水準へはそのまま移せない。
  両者の等号 U-10 は未解決である。

従って、既存の有限成果物から A を書けば (2) の証明書を捏造することになり、B を書けば
有限-to-family の過大格付けになる。

## 最終裁定

**「648 は全部 A 型」も「648 は全部 B 型」も、現時点では根拠付きで確定できない。**

これは第三の数学的分岐を主張するものではない。真値が二択であることは (1) で確定して
いるが、その真値を選ぶ証明が無い、という区別である。便 147 の第 5–6 行だけなら二択の
いずれかを書くよう要求される一方、第 10 行は捏造と過大格付けを明示的に禁じている。
両方を同時に守る A/B 文は、現証拠からは作れない。従って第 10 行の不変条件に従い、
決着を装わない。

### 資源要求に対する回答

GHA、SmallGroups、PackageGT、計算時間の増量だけで B 側を有限時間に証明することは
できない。B 側には次のどちらかの新しい数学的入力が必要である。

1. restricted かつ enumerable な cofinal isolated family と、その同一族上での一様な
   reduction 全射定理。
2. outside-$A_{\rm ar}$ 元一つについて、全深度で互換な lift を与える明示的逆極限構成。

A 側は半決定可能である。資源を投入するなら、

\[
|E|=k|PB_3/M|\quad(k=3,4,\ldots)
\]

の順に、$PB_3\twoheadrightarrow E\twoheadrightarrow PB_3/M$ の
$B_3$-安定 marked extension を重複なく dovetail し、isolated 性と全 reduction fiber を
独立二系統で検査し、最初の (2) で停止する無期限 GHA job が正しい要求になる。しかし
A が偽ならこの探索に停止保証はなく、有限 cap まで kill が無いことを B の証明にはできない。

## provenance

| 入力 | SHA-256 |
|---|---|
| `ops/inbox_codex/sol_task_147_settle.txt` | `9df856dfd200576fe35ec7b0e04dd8572fdae1e49c910cf008082700bc69a635` |
| `sol/sol_reply_140_finish.md` | `3463fe6ca0d876b2b512a270e907c32ea82afa6183848c92de63fee8a0ba0da2` |
| `sol/sol_reply_143_typedfiber.md` | `ef6490f286b82ade2ee5995a00a857dd92fbca6f5e136c79f855d81adab7da3a` |
| `docs/notes/ihnec_v1.md` | `498b24ef9e907b0708c0915c36aa3e2a13bf07e63c753967e920d4731bfe663f` |

- 便 144・145・146 は読まず、破棄済みとして扱った。
- 新しい機械計算、commit、push、workflow dispatch は行っていない。
- Lean certificate はなく、`verified` の語は用いない。
- 本便で変更した対象は、この返信ファイルだけである。

FINAL: NO_HONEST_A_OR_B_CERTIFICATE
