# 規約辞書 W(candidate v1)— 工房の全規約を一表に

**状態札: candidate(裁定前・未 commit)**
起草: 実装者 / 2026-07-29 ・ 裁定 160 §処置 2(提案 SGN-5 の実施)
正典: `docs/week1-定義ノート.md` §1.5.1(規約 W-1〜W-4、**併合済み・工房の正本**)
出所: `search/week3-battery-common.g` の W-1〜W-4 系記載(`AbstractProd` コメント L46-54、`BuildQTGeneral` 等)+ `docs/notes/sgn_c_resolution_v1.md` §4(規約 W-4 の辞書・§4.2/§4.3 の boxed 式)

**この文書の位置づけ**: `docs/week1-定義ノート.md` §1.5.1 の **W-1〜W-4 は語の掛け算の向き(積・語レベル評価・判定式)に関する規約**であり、すでに Sol 便 11 で併合・裁定済みの正本である。本稿はそれとは**別の 4 項目**——(W-\*)(W-^)(W-nf)(W-perm) と番号を変えて衝突を避けている——を扱う。うち (W-\*) は正典 W-1 の**AbstractProd 実装上の言い換え**、(W-^) と (W-nf) は `sgn_c_resolution_v1.md` が発見した**正典に未記載だった 2 項目**(裁定 160 §処置 2「提案 SGN-5」)、(W-perm) は独立に自己発見された置換合成の向きの規約である。**本稿は candidate — 司令塔レビュー・Sol ゲートを経て正典への統合を判断する。**

---

## 一覧表

| ID | 規約(一行) | 詳細 | 破ると何が起きるか(事故 ID) |
|---|---|---|---|
| **(W-\*)** | `AbstractProd` の語順は紙面→GAP で**逆順**。paper 語 $w_1 w_2 \cdots w_k$ は GAP 生の積 $w_k \cdot w_{k-1} \cdots w_1$ に対応する | §1 | k9-package L221 F10 |
| **(W-^)** | GAP の `X^g`(定義 $g^{-1}Xg$)は**紙面の $\mathrm{inn}(g)(X) = gXg^{-1}$ そのもの**。$g$ を反転する必要はない | §2 | SGN-ĉ・S2(`ihc-fixture-v2.g` L199 `paperG := nativeG^-1`) |
| **(W-nf)** | conjugator の正規形は**紙面 $a\cdot q$**($a\in A$ が $q$ の右)。生 GAP 積 `conj * Inverse(q)` で分解すると紙面 $q\cdot a'$ の $a'$ が出る($a' = q\cdot a$、$q$ の $A$ 上の線形作用) | §3 | SGN-ĉ・S1(全編の根因。`ihc-fixture-v2.g` L84 `DecomposeConjugator`) |
| **(W-perm)** | 置換合成の向きは文書によって混在しうる: 「$(p\circ q)(i) = p(q(i))$」(関数合成規約)と GAP の「$i^{p*q} = (i^p)^q$」($p$ を先に適用)は**逆順**。「彼らの $pq$」= GAP の $q*p$ | §4 | `search/i24-u3-recheck.g` L189-193(自己発見・実装中に判明。fixture 自体は正しく、比較に規約変換が要ると判明した事例) |

**混同禁止**: 上表の (W-\*)(W-^)(W-nf)(W-perm) は、`docs/week1-定義ノート.md` §1.5.1 の**規約 W-1〜W-4(番号が同じ "W-" で紛らわしいが別体系)とは異なる 4 項目**である。特に (W-\*) は正典 W-1 と**同一内容**(AbstractProd 実装レベルの言い換え)なので、統合時は W-1 に一本化し (W-\*) は「W-1 の実装ノート」として吸収するのが自然(下記「統合案」参照)。(W-^)(W-nf) は正典に**存在しない**新規 2 項目(裁定 160 の指摘どおり)。(W-perm) は語(x,y の合成)ではなく**置換自体の合成**についての規約で、正典 W-1〜W-4 の射程外(適用対象が異なる)。

---

## §1 (W-\*) — AbstractProd の語順(正典 W-1 の実装ノート)

**定義**(`search/week3-battery-common.g` L46-54、`docs/week1-定義ノート.md` §1.5.1 規約 W-1 と同一内容):

```gap
AbstractProd := function(list)
  local val, i;
  val := list[1]^0;
  for i in [Length(list), Length(list)-1 .. 1] do
    val := val * list[i];
  od;
  return val;
end;;
```

paper 語 $w_1\,w_2\,\cdots\,w_k$($w_1$ を先頭に読む)は GAP の生の積で $w_k \cdot w_{k-1} \cdots w_1$(**末尾から掛ける**)に対応する。作用式での定義(正典・時間語なし): $(AB)\cdot i = A\cdot(B\cdot i)$、$i^{B*A} = (i^B)^A$、ゆえに **paper "AB" ↔ GAP `B*A`**。

**破った場合に何が起きるか**: `search/k9-package.g` L221-225(F10・裁定 109 で修理)。paper 語 "$f^{-1}Yf$" を素朴な GAP 積 `f^-1 * Y^u * f` とそのまま書いたのが F10 バグ — 正しくは `AbstractProd([f^-1, Y^u, f])`(= GAP 生の積 `f * Y^u * f^-1`)。修理コメント: 「素朴な GAP 積 f^-1\*Y^u\*f をそのまま書くのは規約違反(F10 バグ)だった」。

---

## §2 (W-^) — GAP `X^g` と紙面 $\mathrm{inn}(g)$ の対応

**定義**(`docs/notes/sgn_c_resolution_v1.md` §4.2、(W-\*) を 2 回使った帰結):

$$\texttt{X\^{}g} \;=\; g^{-1} *_{\mathrm{raw}} X *_{\mathrm{raw}} g \;=\; g\cdot X\cdot g^{-1} \;=\; \mathrm{inn}_{\mathrm{paper}}(g)(X)$$

恒等式として `X^g = AbstractProd([g, X, g^-1])`(GAP・紙面 二系統一致で確認済み・全 $n\in\{3,5,7,9,11\}$)。**したがって GAP の `^` は既に紙面の $\mathrm{inn}$ であり、$g$ を反転する必要はない。**「native = GAP規約 $g^{-1}Xg$、paper = 紙面規約 $hXh^{-1}$、変換式は $h=g^{-1}$」という二欄立ては phantom。

**破った場合に何が起きるか**: `search/ihc-fixture-v2.g` L7-8, L199, `notation_note`(FINDING SGN-ĉ の副次事故 S2)。`paperG := nativeG^-1` は逆向きの補正で、$h$ が**対合の場合は無害**(この fixture の $\widehat c=[2n-1,1]$ 本体では実害なし)だが、**非対合 conjugator では誤る** — `search/ihc-fixture-v3.g` TEST (ii)(m=0 族・$k=2$・$h=a_1^{-2k}$)で機械確認: native 探索が返すのは $h$ 自身であって $h^{-1}$ ではない($n\in\{3,5,7,9,11\}$ 全て `native = h_predicted: PASS`・`native = h_predicted^-1: FAIL`)。

---

## §3 (W-nf) — conjugator 正規形は紙面 $a\cdot q$

**定義**(`docs/notes/sgn_c_resolution_v1.md` §4.3):

$$\mathrm{conj} = a\cdot q \quad(\text{紙面正規形、}a\in A\text{ が }q\text{ の右})$$

分解するには紙面積 $\mathrm{conj}\cdot q^{-1}$ を計算しなければならず、これは **(W-\*) を通す**必要がある: `v := AbstractProd([conj, Inverse(q)])`(= GAP 生の積 `Inverse(q) * conj`)。生 GAP 積 `conj * Inverse(q)` をそのまま計算すると、(W-\*) より紙面 $q^{-1}\cdot\mathrm{conj}$ = 「$\mathrm{conj}=q\cdot a'$ の $a'$」が出る。両者は $q$ の $A$ 上の線形作用で結ばれる:

$$a' = q\cdot a \qquad (q_1 = \mathrm{diag}(+,-,-),\ q_2=\mathrm{diag}(-,+,-),\ q_3=\mathrm{diag}(-,-,+))$$

**破った場合に何が起きるか**: `search/ihc-fixture-v2.g` L84 `DecomposeConjugator`(FINDING SGN-ĉ の**根因そのもの**・S1)。$q=q_3$ の場合 $a'=(-a_1,-a_2,a_3)$ で、本件は $\mathrm{dv}_2=\mathrm{dv}_3=0$ だったため症状が「$\mathrm{dv}_1$ だけ符号反転」に見えた(`dv1_negated_only` という分類名自体が誤導的 — 真の規則は $(-,-,+)$ 全体)。`search/ihc-fixture-v3.g` の修理後は全 $n$ で `conversion_rule_check: PASS`(旧 buggy 分解が新分解の $q$-変換にちょうど一致することを assert・TEST i/iii)。

---

## §4 (W-perm) — 置換合成の向き

**定義**: 「$(p\circ q)(i) = p(q(i))$」(関数合成規約、$q$ を先に適用)と GAP の「$i^{p*q} = (i^p)^q$」($p$ を先に適用)は**逆順**。ゆえに **「彼らの $pq$」= GAP の $q*p$**(語の (W-\*) と同型の反転だが、対象は $x,y$ の**語**ではなく**置換そのもの**であり、正典 W-1〜W-4 は語レベル評価の規約なのでこの用法をカバーしない)。

**破った場合に何が起きるか**: `search/i24-u3-recheck.g` L189-193(自己発見・実装中に判明・事故化する前に検出)。`docs/manifest_k5_appendixA_v1.md` §2 の「規約(iii)」が $(p\circ q)(i)=p(q(i))$ と明記しているのに気づかず GAP の `*` でそのまま比較すると food fixture の $\bar z$ が再現できない(実際は $\bar z = (\bar y\cdot\bar x)^{-1}$ の**規約反転**を要する)。実装ノート: 「fixture 自体に誤りはなく、比較には規約変換が要る」— 検出はしたが、事故化する前に自己発見で止めた事例(cf. `search/a5-dessin-crosscheck.g` L227 も同型の注記あり)。

---

## 統合案(裁定へ)

1. **(W-\*)** は正典 `docs/week1-定義ノート.md` §1.5.1 の **規約 W-1 と同一内容**。統合するなら独立項目にせず、W-1 の説明に「実装は `AbstractProd`(week3-battery-common.g)」という一行の相互参照を足すだけでよい。
2. **(W-^)・(W-nf)** は正典に**存在しない**(裁定 160 の指摘)。この 2 つを正典 §1.5.1 に **W-5・W-6** として追記するのが最小の統合(番号衝突を避けるため、本稿の (W-^)(W-nf) 表記はあくまで candidate 段階の仮ラベル)。
3. **(W-perm)** は語レベルでなく置換自体の合成に関する規約で、正典 W-1〜W-4 の射程外。独立項目として残すか、あるいは「W-1 の適用範囲外(置換合成一般)」という注記に留めるか — **司令塔判断を仰ぐ**(単独の統合先が正典にないため)。

## 未閉鎖項

- 【WDICT-1】本稿は candidate。Sol ゲート・裁定を経ていない — commit しない。
- 【WDICT-2】(W-\*)(W-^)(W-nf)(W-perm) というラベルは本稿限りの仮称であり、正典への統合時に **W-5/W-6** 等へ差し替わる可能性がある(上記統合案 2)。
- 【WDICT-3】事故 ID は grep で確認した既知 4 件のみ。他にも同型の事故が未発見の可能性がある(悉皆調査はしていない)。
