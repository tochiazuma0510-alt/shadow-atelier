# 総合判定: **差戻し**

**(β) 版イベントは不許可。Rule 1 v1.4 / manifest v1.6 の作成開始、および S5 Model-Builder の追加 unlock は本便からは出さない。**

数学核については、TB4 の型分離・TB4-D/E・検出表・検査 5(d′) の算術はほぼ閉じている。しかし、便 49 F8 の六条件は現物ではまだ全件閉じていない。

- 条件 1: **PASS**
- 条件 2: **条件付き PASS**（TB4-D/E は閉鎖、`\hat b_i=b_{\rm op}` の statement-level typing は未完）
- 条件 3: **PASS**
- 条件 4: **FAIL**（BFC v2.7 の live 本文に旧式が複数残る）
- 条件 5: **FAIL**（amendment v4 の結果 record が旧 bundle ID をまだ受理する）
- 条件 6: **FAIL**（certificate 再束縛は PASS、status copy 除去と CLAIMS 同期は未完）

新規二点は、**検査 5(d′) は full tuple として PASS**、**四段のはしごは数学的意図を支持するが現行表示は修文が必要**、である。

---

## F1. 監査対象・digest・再現

委嘱表の行数と SHA-256 は全件一致した。

| artifact | wc -l | SHA-256 | 判定 |
|---|---:|---|---|
| `docs/week4-BFC攻略_opus_v2.md` | 1144 | `3c45d4409e353be5fa55a38862f6162db991f729d30deabc58504b89de693839` | 一致 |
| `docs/amendment_5prime_draft.md` | 299 | `2ca542852f676c4dab7117c276556c960088f7ffed381e9abfae5e6ce0b3333e` | 一致 |
| `docs/week4-TB4導出_opus_v1.md` | 754 | `10b42cbe1e3dc8ef6b81b4bf5f3a9985f9a581dc1d5452235e9710cb7573e49e` | 一致 |
| `certificates/bfc/bfc-antecedents.json` | 1 | `84d98b86b91b9a76ada32455c276e8d9c64fa8ae7915b91f52f6b731d926976e` | 一致 |
| `docs/対話帳.md`（T-14 まで） | — | `1d7e58bee157f7d5d17b422b0a1277c873f21ca45f366bf49c8dc81e4640c3b5` | 一致 |

再走・束縛検査:

1. `node search/tb4-monodromy-check.mjs` は **33/33 PASS**。
2. `node search/week4-bfc-antecedents.mjs` は **13/13 PASS**。
3. BFC certificate は `pass_count=25`, `fail_count=0`, `fail_closed=true`。
4. certificate の
   - `input_doc_sha256 = 3c45d440...` は BFC v2.7 現物と一致、
   - `script_sha256 = 104e748b...` は GAP script 現物と一致、
   - `node_counterpart_sha256 = f7429890...` は Node 現物と一致。

したがって **GAP certificate の v2.7 への再束縛そのものは PASS** である。GAP は本便では再生成していない。

ただし TB4 checker の新規部分は、

- `Z2Mlink(t2) := (t2===1)` と定義してから同じ含意を検査する、
- path ごとの `b_op=9/1/null` を表に hard-code して件数を数える、

という **regression lint** である。33/33 は文書との転記一致を確認するが、link の数学や各 path の効果を独立導出する証明書ではない。本返信では該当算術を別に紙上再導出した。

---

## F2. 便 49 F8 の六条件

### F2.1 条件 1 — \(t_{2M}\) と \(\bar t_M\): **PASS**

TB4 v2.2 §3.5.1 の

\[
t_{2M}\in(\mathbb Z/2M)^\times,\qquad
\bar t_M=t_{2M}\bmod M
\]

および

\[
(Z_{2M}\text{-link})\iff t_{2M}=1
\]

は正しい。`\bar t_M=1` は link の必要十分条件でないことも、\(M=10,t_{20}=11\) で正しく示されている。

\[
\ker\bigl((\mathbb Z/20)^\times\to(\mathbb Z/10)^\times\bigr)=\{1,11\}
\]

も再計算一致した。辞書

\[
b_{\rm op}=b_{\rm cmp}\bar t_M^{-1}
\]

への型修理も正しい。

### F2.2 条件 2 — named antecedents: **条件付き PASS**

次は閉じた。

- TB4-D の (D-i) Kummer 作用、(D-ii) \(c_\Lambda\) の \(x\)-同変性、(D-iii) Rule 1 marking。
- TB4-E の (E-i) orientation package、(E-ii) 埋め込み、(E-iii) actual marking/intertwiner、(E-iv) \(\tau\)-marking。
- TB4-E が TB4-3 全体ではなく TB4-2 orientation package で足りるという依存削減。

TB4-D/D′ と TB4-E の証明核は **PASS**。

一方、§3.5.3 の

> 判定: \(\hat b_i=b_{\rm op}\)

は、導出本文では \(c_i=c_\Lambda\)、\(\zeta_{10}=\zeta_{10}^{\rm Rule1}\)、\(\ell_i=x=[\gamma_0]\) を列挙しているが、**statement 自体には前件欄がない**。便 49 F8-2 は \(\hat b_i=b_{\rm op}\) についても theorem statement に named antecedents を要求した。

これは数学核の穴ではないが、今回と同型の「証明本文にはあるが statement から落ちる」事故を残す。少なくとも次を statement 直下に掲示すべきである。

1. \(c_i=c_\Lambda\) は Rule 1 §4.3 / B-4c の actual intertwiner。
2. \(\ell_i\) は **§1.1 の同じ** \(x=[\gamma_0]\) が Fib に誘導する作用。
3. (7.1) の \(\zeta_{10}\) は Rule 1 field generator の冪。
4. \(\tau_i\) は Rule 1 (1.8) の marking。

### F2.3 条件 3 — 検出表: **PASS**

§3.5.4 の二分割は正しい。

- finite operational suite: paths \(1,2,3,4,6,7,8\)、**6 detected / 1 root-link blind**。
- profinite root-normalization suite: path 5、**finite measurement out-of-scope**。

したがって母数を明記した

\[
6/8\quad\text{または}\quad6/7
\]

は正しい。「盲点」と「測定宇宙外」を分離し、single-axis regression set と限定し、複数反転の網羅性を主張しない修文も適切である。

\[
(7.1)\text{ は }(Z_{2M}\text{-link})\text{ の代替でも }(Z\text{-norm})\text{ の certificate でもない}
\]

も正しい。

### F2.4 条件 4 — BFC v2.7 全文同期: **FAIL**

v2.7 の差分表 G1–G9 と後半の新しい型表は正しい。しかし、**live 本文がその差分表に従い切っていない**。履歴欄に旧式を引用すること自体ではなく、現在形の定義・定理・状態欄に残っているものを挙げる。

#### blocker 4-a: §2 がまだ「未調整」

BFC 246–260 行付近に、

- (2.1) を裸の \(b:=\varepsilon^{-1}\) と定義、
- \(t\in(\mathbb Z/2M)^\times\) と \(t\varepsilon\) を混用、
- 一般論で `(Z20-link)` を使用、
- \(b_{(8.1)}\), \(b_{\rm TB4}\) という旧名を使用、
- 「**未調整・司令塔裁定事項**」「断定しない」

が現役のまま残る。とくに 252 行の

\[
m((\zeta_M^{\rm Rule1})^{t\varepsilon})
\]

は \(m((\zeta_M^{\rm Rule1})^{\bar t_M\varepsilon})\) でなければ型が合わない。260 行は、すでに確定した \(\hat b_i=b_{\rm op}\) と正面衝突する。

この block は履歴として残すなら全体を明示的に `RETRACTED v2.6` とし、直後に現行式だけを置くべきである。現状は v2.7 の定義節として読める。

#### blocker 4-b: \(\kappa\) 相殺説が一文残る

552 行は前半で「\(\kappa\) は無関係」と訂正した直後に、

> \((\zeta_n)\mapsto(\zeta_n^t)\) で \(\tau\) の生成元と **\(\kappa\) の値が同時にひねられて相殺する**

と再び書いている。これは G1 が撤回した命題そのものである。相殺するのは \(\sigma_\zeta^{\rm TB2}\) と \(\tau\) の命名であり、\(\kappa\) は元として生成元非依存である。

#### blocker 4-c: link 前件の脱落が残る

- 555 行の boxed state は \(b=1\) を TB2+TB4 に相対化するが \(Z\) を落としている。
- 598 行の B-7 exact 状態表は前件を `(TB1)–(TB4)+(CAL)+(W1)–(W5)` とし、\((Z_{2M}\)-link) を落としている。
- 193 行は「札 2 件」と書いた同じ段落で TB4 を「唯一 load-bearing」と呼び直している。

少なくとも B-7 exact の現行 proof は B-6 を継承するため、link が必要である。TB4-E alternate を採る別 proof と、現行 BFC proof の前件を混ぜてはならない。

#### blocker 4-d: 裸の \(b\) 禁止と本文が不一致

付録 A の三量表は正しいが、246、255–260、539、554–559、570–580、598 行等では、現行命題を裸の \(b\) で書いている。link 下の局所略記なら

> 以下この命題内では \(b:=b_{\rm op}=b_{\rm cmp}\)

と scope を宣言すればよい。無宣言のまま「裸の \(b\) は使わない」と両立させることはできない。

### F2.5 条件 5 — amendment theorem bundle と \(b\)-schema: **FAIL**

v4 の中心修理は正しい。

\[
\begin{aligned}
\texttt{THEOREM-ANTECEDENT-Rcyc/twisted/v1}
 &= \texttt{base}+(5'_b),\\
\texttt{THEOREM-ANTECEDENT-Rcyc/exact/v1}
 &= \texttt{base}+(5')+(b_i=1)
\end{aligned}
\]

の二 ID、`b_value_i=b_op`、`b_semantics="op"`、二つの root-twist 欄、`rho_i_id` / `Ih_N_id` hardening は **PASS**。

しかし operative result schema が旧名を残している。

- amendment 183 行:
  `THEOREM-ANTECEDENT-Rcyc / FALSIFIER-ANTECEDENT-BFC`
- amendment 219 行:
  `antecedent_bundle_id # THEOREM-ANTECEDENT-Rcyc | FALSIFIER-ANTECEDENT-BFC`

この schema では `/twisted/v1` と `/exact/v1` を保存できず、A12 の修理を結果 record が再び潰す。183 行と 219 行を少なくとも

```text
THEOREM-ANTECEDENT-Rcyc/twisted/v1
THEOREM-ANTECEDENT-Rcyc/exact/v1
FALSIFIER-ANTECEDENT-BFC/twisted/v1
```

の closed enumeration に直す必要がある。未知 ID は fail-closed とせよ。

### F2.6 条件 6 — status/provenance: **FAIL（再束縛部分だけ PASS）**

certificate の final BFC digest への再束縛は F1 のとおり **PASS**。しかし残り二部分が閉じていない。

#### status copy の除去未完

BFC 本文は「現況は本文に書かず外部台帳を正とする」と宣言しながら、

- 7 行: 「現在は v1 の `659a9570…` を指す」「残るのは provenance 1 件」
- 52 行: 「残るのは fail-closed・assert・fixture・provenance の 4 件」
- 1005 行: 「cross-checked 昇格に残るのは provenance 1 件」
- 1037–1047 行: pass count、fixture、群位数等の現況値を再複製

を残している。7 行は現 certificate と直接矛盾する。外部化方針を採るなら、履歴として日付・版を固定した引用を除き、live status copy は除去すべきである。

#### CLAIMS W3-17 が v2.7 へ同期していない

`provenance/CLAIMS.md` W3-17 は現在も、

- 「自前導出 v2.1」
- 「攻略 v1→v2.6」
- 「便 49 監査中・型付け修理中」
- framework condition を TB1–TB4 のみで記載

している。一方で同じ行が `artifact 残差 0` とする。現行 proof の \((Z_{2M}\)-link) と v2.7 / TB4 v2.2 / amendment v4 を反映していないため、これは「同期済み」ではない。

BFC 本文修理後に digest が再び変わるので、順序は

1. BFC / amendment / TB4 の live 本文修理、
2. final digest 固定、
3. GAP certificate 再束縛、
4. CLAIMS W3-17 更新、
5. digest と status の最終 lint、

でなければならない。

---

## F3. 新規監査 1 — §3.5.1a「四段のはしご」

### F3.1 数学的意図: **支持**

共通前件を固定すれば、狙っている strict hierarchy は正しい。

\[
\begin{array}{ll}
L1:&b_{\rm op}=1,\\
L2:&b_{\rm cmp}=1\iff\bar t_M=1,\\
L3:&\varepsilon\equiv1\pmod{2M}\iff t_{2M}=1,\\
L4:&\varepsilon=1.
\end{array}
\]

反例も各段を分離する。

- \(L1\nRightarrow L2\): \(M=10,t_{20}=3\)。TB4-3 下で \(b_{\rm op}=1,\ b_{\rm cmp}=3\)。
- \(L2\nRightarrow L3\): \(M=10,t_{20}=11\)。\(\bar t_{10}=1\) だが \(t_{20}\ne1\)。
- \(L3\nRightarrow L4\): \(\hat{\mathbb Z}^{\times}\) の \(2\)-進・\(5\)-進成分を \(1\)、\(3\)-進成分を \(-1\)、他を \(1\) とする unit は mod \(20\) で \(1\) だが exact に \(1\) ではない。

したがって F4.1 の本質を「L2 と L3 の同欄圧潰」と読むことは正しい。

### F3.2 現行表示: **修文要**

現行表は「下へ行くほど強い」と書く一方、行間に直接の含意矢印を置かず、各行の右側に出所を置いている。そのため **条件・結論・定理名**が同じ列に混ざる。

また TB4-E を「無条件」と呼ぶのは過大である。正しくは

> **root-link-free**（ただし (E-i)–(E-iv) に相対的）

である。

安全な表示は二段に分けることである。

\[
(Z\text{-norm})
\Longrightarrow
(Z_{2M}\text{-link}:t_{2M}=1)
\Longrightarrow
(\bar t_M=1),
\]

\[
\varepsilon=1
\Longrightarrow
\varepsilon\equiv1\pmod{2M}
\Longrightarrow
b_{\rm cmp}=1,
\qquad
b_{\rm op}=1\ \text{は TB4-E により root-link-free}.
\]

その上で「共通の D/E/TB4-3 package の下では \(L4\Rightarrow L3\Rightarrow L2\Rightarrow L1\)、上記 witness により各逆向きは偽」と書けば、\(\subsetneq\) の意味が一意になる。

よって四段のはしごは **修文後 PASS**。現行の「無条件」と未型付けの強弱記号のまま版正本へ入れることには反対する。

---

## F4. 新規監査 2 — 検査 5(d′) と T-14

### F4.1 算術: **PASS**

countermodel / TB4-3 の関係

\[
\varepsilon\equiv t_{20}^{-1}\pmod{20}
\]

を含む full fixture

\[
(M,t_{20},\bar t_{10},\varepsilon,b_{\rm cmp},b_{\rm op},Z20\text{-link})
=(10,11,1,11,1,1,\mathrm{false})
\]

は正しい。実際 \(11^{-1}\equiv11\pmod{20}\) で、

\[
b_{\rm cmp}=\varepsilon^{-1}\equiv1\pmod{10},\qquad
b_{\rm op}=b_{\rm cmp}\bar t_{10}^{-1}=1.
\]

したがって

> 「\(b\) が 1 だから root objects も一致する」

は \(b_{\rm cmp}\) と \(b_{\rm op}\) のどちらで読んでも偽である。T-14 の強化提案を採用する。

### F4.2 ただし「invariant」ではなく negative fixture

\(t_{20}=11\) **だけ**から \(b_{\rm cmp}=1\) は出ない。上の \(\varepsilon=11\)（または TB4-3 proof ID）が必要である。したがって schema では (d′) を普遍 invariant のように

```text
t_20 = 11 => b_cmp = b_op = 1
```

と書かず、上の full tuple を束縛した **negative regression fixture** として保存すべきである。現 checker は内部で `e=inv(t2bad,20)` を置いているので、実計算はこの正しい読みになっている。

### F4.3 \(K^{(3)}\) の副次記録: **PASS**

\[
\ker\bigl((\mathbb Z/12)^\times\to(\mathbb Z/6)^\times\bigr)=\{1,7\}
\]

は正しい。同じ型の fixture は

\[
(M,t_{12},\bar t_6)=(6,7,1)
\]

で作れる。これは K3 の既存判定を反転させる主張ではなく、level \(12\) equality を level \(6\) の指数から復元してはならないという型警告である。

---

## F5. TB4 §8.10 の四問への回答

1. **四段のはしご**: F3 のとおり、数学的骨格は正しい。`unconditional` を `root-link-free under (E-i)–(E-iv)` に直し、条件列と結論列を分ければ PASS。
2. **suite 二分割**: **PASS**。`6 detected / 1 root-link blind` と `out-of-scope` は F10.2 の意図どおり。ただし checker は効果を hard-code して数える regression lint であり、網羅証明ではない。
3. **検査 5(d′)**: **PASS**。ただし F4.2 の full tuple / proof-ID つき negative fixture として採録する。
4. **§8.9 Rule 1 条文案**: **意図 PASS・文言は型をもう一段明示せよ**。

問 4 の推奨条文は次である。

> Rule 1 §1.1 の底を \(U_\lambda=\mathbf P^1_\lambda\setminus\{0,1,\infty\}\) と書き、TB4/BFC の \(U_\beta\) と座標同型 \(\beta=\lambda\) により、接基点 \(\vec{01}\)、標準向き、ループ \(\gamma_0\) を保って同一視する。§7.1 の \(\ell_i\) は、この **同じ** \(x=[\gamma_0]\) が \(\operatorname{Fib}_{\vec{01}}(W_0^{(i)})\) に誘導する permutation であり、別の local generator を再定義したものではない。

現案の「\(\lambda\) の値域が \(U\) の座標 \(\beta\)-線」は意図は読めるが、map・base・接基点を一つの typed equality にしていない。上の形なら ★教材 T5 に耐える。

---

## F6. 版イベント再審査

**不許可。**

イベント設計自体は便 49 F8 のものを維持してよい。しかし「六条件 + 新規二点が PASS」という発火条件を満たしていない。再提出の最小修理は次の四束である。

1. **BFC live 本文**
   - 246–260 行を \(b_{\rm cmp},b_{\rm op},t_{2M},\bar t_M\) へ全面同期。
   - 「未調整」「断定しない」を閉じる。
   - 552 行の \(\kappa\) 相殺残文を削除。
   - 555、598 行ほかの link 前件を復帰。
   - 裸の \(b\) は scope 宣言つき局所略記以外禁止。
2. **amendment result schema**
   - 183、219 行を predicate-version 付き closed enumeration へ。
   - unknown / unversioned bundle ID は fail-closed。
3. **四段のはしごと \(\hat b_i\) statement**
   - F3 の共通前件と strictness を明記。
   - \(\hat b_i=b_{\rm op}\) の named antecedents と \(\ell_i=x\) の typed equality を statement に掲示。
4. **status 最終化**
   - BFC の live status copies を除去。
   - CLAIMS W3-17 を v2.7 / TB4 v2.2 / \((Z_{2M}\)-link) 前件へ更新。
   - その編集後の final BFC digest に GAP certificate を再束縛。

この四束の差分検収が通れば、Rule 1 v1.4 / manifest v1.6 の versioned event、札更新、文献要請 13(ii) の縮小維持、B-9′(e′) の \(b_{\rm op}\) 形復帰を一つのイベントとして許可できる。現時点では S5 をその新版 predicate の下で走らせる根拠がない。

---

## F7. ★教材

1. **差分表が「修理済み」と言っても live body が直ったことにはならない。** 今回は G1–G9 の表が正しく、同じファイルの定義節・定理表・状態欄がその表に反していた。
2. **versioned ID は定義箇所だけでなく、全 consumer の enumeration まで伝播して初めて一意化される。** theorem bundle を二つに割っても result record が旧 ID 一つなら、保存時に再融合する。
3. **negative fixture は入力一個ではなく反例の全自由変数を束縛する。** \(t_{20}=11\) だけでなく \(\varepsilon=11\) と link=false を含めて初めて (d′) になる。
4. **status 外部化は宣言ではなく削除操作で完成する。** 「certificate/CLAIMS が正」と書きながら本文に旧現況を残すと、読者は相反する二つの live state を受け取る。
5. **「無条件」は空の前件を意味する。** 「root-link を使わない」と「何も仮定しない」は別である。TB4-E は前者であって後者ではない。

---

## F8. 共同設計者としての発案

### F8.1 version-event preflight lint

版イベントの直前だけ、次の token を current theorem/status section から fail-closed で探索する。

```text
未調整
要調整
現在は v1
残るのは ... provenance
THEOREM-ANTECEDENT-Rcyc        # slash/version なし
b_(8.1), b_TB4, 裸の b
t epsilon                      # t_2M / t_M-bar でないもの
```

履歴表・取り消し引用は allowlist した block 内だけ許す。今回の残差はこの小型 lint で全て止まる。

### F8.2 normalization-level を独立 enum にする

四段のはしごを prose だけでなく

```text
root_normalization_level =
  none | mod_M | level_2M | profinite
```

として記録し、各値に許される結論を固定する。

```text
none       -> b_op = 1 only
mod_M      -> b_cmp = 1
level_2M   -> epsilon = 1 mod 2M
profinite  -> epsilon = 1
```

これなら L2/L3 の同欄圧潰を schema が拒否できる。

### F8.3 certificate 発行順の固定

```text
paper edits closed
  -> document digest frozen
  -> GAP/Node certificates bound
  -> CLAIMS updated
  -> no-stale-status lint
  -> version event authorization
```

certificate の再束縛後に本文を直して再び失効させる往復を、この順序で止められる。

---

## F9. 監査範囲外申告

監査範囲外は、K\(^{(5)}\) の個別モデル・\(u\)・封印値、S5 Model-Builder の探索結果、Lean 形式化、外部文献原文である。GAP certificate は schema・pass/fail・fail-closed・三 digest を検収したが、本便では GAP を再生成していない。既存 Node 二本だけを再走した。

