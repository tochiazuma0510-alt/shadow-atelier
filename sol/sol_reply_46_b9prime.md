# 総合判定: **条件付き PASS**

補題 B-9′ の中心命題

\[
b_{\rm sq}=b_{\rm ns}=\varepsilon^{-1}\bmod 10,\qquad
a_{\rm eff}=a=1
\]

は正しい。とくに \(\varepsilon\) の定義には \(c_i,\Lambda_i,H_i,u_i\) は入らず、二 dessin で同じ \(\operatorname{Ih}_N|_{G_K}\) を比較する消去計算も正しい。したがって、**(P1)、(P2)、位数、核、全射判定、固定体、および Belyi 側の根基 2 観測列が exact \(\varepsilon\) に依存しない**という数学的骨格を承認する。

ただし、現行の補題文をそのまま `two-mathematician audit PASS` へ上げることはできない。必要な修理は三点である。

1. \(j_i\)、位数、核を使う (b)–(d) の前件に、各 detector の **(6′-ii)**、すなわち
   \[
   \rho_i|_{\mathfrak F_0}\text{ が忠実},\qquad
   \rho_i(\mathfrak F_0)=\tau_i(\mu_{10}[5])
   \]
   を明記する。
2. B-7\(^{\rm tw}\) 末尾および §10.1.4/§15.8 の「\(\tau\) の単射性から \(b\) が一意」「\(\exists !\,b\)」を撤回する。**一意なのは (2.1) で先に固定された \(b\)、または Rule 1 (7.1) の全 torsor 慣性から測る \(b_i\)** であって、\(G_K\)-character の等式だけから常に一意なのではない。
3. manifest/Rule 1 の untwisted (5′) を versioned amendment で直す。それまでは B-9′(e) の「`bridge_result_i` を含む campaign 全判定」は現行規則の意味では過大である。

この三点と末尾 F8 の stale 文言を直せば、B-9′ を `paper-proof / two-mathematician audit PASS` へ上げてよい。既受理の B-7 本体を開け直す必要はない。

---

## F1. 現物照合

本便で得た SHA-256 は次のとおり。

| artifact | SHA-256 |
|---|---|
| `docs/week4-BFC攻略_opus_v1.md` | `659a9570118df503b5cd88b03562954cb6fac1ece9150c2908c8327915c36100` |
| `docs/week4-BFC攻略_opus_v2.md` | `adbf252b76cc012253de0c7464c57d8c2db70898cc2e856a8b48720f77313dae` |
| `search/week4-bfc-antecedents.mjs` | `97621fdb488e92fd4b13e5a7ce7d1665e239dc08ebee4b441b7736973d4ec7d7` |
| `search/bfc-antecedents-check.g` | `4ec0952323e425ae391e988b2ea54b51e43752823968d8d9804bfd5e5ea3e232` |
| `certificates/bfc/bfc-antecedents.json` | `fb23e97802ae15e04c9386e7017c0c0071b5b50c09108a7c7b941e55aa8ec080` |

Node 系を再走し、**13/13 PASS**、V3 の \(12/0\)、V7 の \(1296/432\) を再現した。現 GAP certificate は schema v3、25/25、`fail_closed=true`、全 marking transport `true`、V3 \(12/12\) を記録している。

---

## F2. B-9′(a): **PASS**

(TB4\(^{\rm u}\)) の下で、\(x\) と \(\iota(\sigma_\zeta)\) は

\[
I_0\simeq\widehat{\mathbb Z}(1)
\]

の同じ procyclic 部分群の位相的生成元である。従って

\[
x=\iota(\sigma_\zeta^\varepsilon)
\]

を満たす \(\varepsilon\in\widehat{\mathbb Z}^{\times}\) は一意である。この等式のデータは

\[
U,\quad x,\quad(\zeta_n),\quad\iota
\]

だけであり、\(N,H_i,\Lambda_i,c_i,u_i\) は現れない。よって同じ底・同じ根系・同じ \(M=10\) を使う二 dessin では

\[
\boxed{b_{\rm sq}=b_{\rm ns}=\varepsilon^{-1}\bmod 10}
\]

である。

ここでは二種類の \(b\) を区別すると混乱がない。

- 数学上の \(b\): (2.1) の \(\varepsilon\) から定まる。
- 実装の \(\widehat b_i\): 凍結済み \(c_i,\ell_i\) を Rule 1 (7.1) に入れて測る。

\(\widehat b_{\rm sq}=\widehat b_{\rm ns}\) は定理の再仮定ではなく、二つの transport が同じ数学上の \(b\) を実現したことの**必要な integrity 検査**である。この役割分担は正しい。

---

## F3. B-9′(b)–(d): **前件追記を条件に PASS**

### F3.1 \(q\)-free cocycle の型

必要な写像は

\[
\kappa_i:G_K\longrightarrow\mu_{10},\qquad
[b]\in\operatorname{Aut}(\mu_{10}[5]),\qquad
j_i:\mu_{10}[5]\xrightarrow{\sim}\mathfrak F_0
\]

である。B-7\(^{\rm tw}\) と (6′) から

\[
\rho_i(\operatorname{Ih}_N(\gamma))
 =\tau_i(\kappa_i(\gamma)^b)
 \in\tau_i(\mu_{10}[5]).
\]

\(\tau_i\) は単射で、\([b]\) は \(\mu_{10}\) の自己同型だから

\[
\kappa_i(G_K)\subseteq\mu_{10}[5].
\]

さらに \(\rho_i|_{\mathfrak F_0}\) の逆を施せば

\[
\boxed{\operatorname{Ih}_N|_{G_K}
 =j_i\circ[b]\circ\kappa_i}
\]

を得る。計算自体は正しい。

### F3.2 現定理文から (6′) が脱落している

§10.1.1 で

\[
j_i=(\rho_i|_{\mathfrak F_0})^{-1}\circ
\tau_i|_{\mu_{10}[5]}
\]

と定義し、証明 §10.1.2(b) でも明示的に (6′) を使っている。しかし補題 B-9′ の前件と付録 B の依存欄は (TB#)、(CAL)、(W1)–(W5)、B-7\(^{\rm tw}\)、K5-a しか挙げていない。

(W5) が与えるのは \(\Lambda_i\) の安定性であって、\(\rho_i\) の忠実性ではない。本稿自身も §3 で

> (6′) 第 1 節 = (W5)、第 2 節の忠実性は formal 側

と区別している。従って現状では \(j_i\) の逆写像が定義できることも、(d) の

\[
|\operatorname{Ih}_N(G_K)|=\operatorname{ord}([v_i]_{10})
\]

も定理文の前件だけからは出ない。

これは \(K^{(5)}\) への実適用を壊す反例ではない。K5-1 により両 detector の (6′-ii) は既に閉じ、manifest の FORMAL-IN にも記録されている。**問題は load-bearing な既知前件の転記脱落**である。補題文と依存表へ、両 \(i\) について (6′) を追記すれば閉じる。

### F3.3 (c) の消去計算

\(\operatorname{Ih}_N|_{G_K}\) は窓 \(N\) の写像であり detector \(i\) に依存しないから、

\[
j_{\rm ns}[b]\kappa_{\rm ns}
 =j_{\rm sq}[b]\kappa_{\rm sq}.
\]

\(a=j_{\rm ns}^{-1}j_{\rm sq}\) とすれば

\[
[b]\kappa_{\rm ns}=a[b]\kappa_{\rm sq}.
\]

ここで

\[
[b],a\in\operatorname{Aut}(\mu_{10}[5])
\cong(\mathbb Z/5)^\times
\]

であり、この群は可換である。従って

\[
\kappa_{\rm ns}=a\kappa_{\rm sq},\qquad
a_{\rm eff}=[b]^{-1}a[b]=a=1.
\]

向き・合成順とも正しい。また

\[
(\mathbb Z/10)^\times\xrightarrow{\sim}(\mathbb Z/5)^\times
\]

なので exponent の mod \(10\) lift に曖昧さもない。Kummer 同型

\[
K^\times/K^{\times10}\simeq H^1(G_K,\mu_{10})
=\operatorname{Hom}(G_K,\mu_{10})
\]

から

\[
[v_{\rm ns}]_{10}=[v_{\rm sq}]_{10}
\]

が従う。ここは **PASS**。

### F3.4 位数・核

\([b]\) は自己同型なので

\[
|\operatorname{im}([b]\kappa_i)|=|\operatorname{im}\kappa_i|,
\qquad
\ker([b]\kappa_i)=\ker\kappa_i.
\]

(6′) の忠実性を加えれば

\[
|\operatorname{Ih}_N(G_K)|=\operatorname{ord}([v_i]_{10}),\qquad
\ker\operatorname{Ih}_N=G_K\cap\ker\kappa_i
\]

も正しい。型を明瞭にするなら前者の restricted 版を

\[
\ker(\operatorname{Ih}_N|_{G_K})=\ker\kappa_i
\]

と先に書き、global kernel は \(G_K=\ker(\widetilde\chi\circ\operatorname{Ih}_N)\) を使って導くとよい。

---

## F4. \(b\) の一意性: **二箇所を修理せよ**

B-7\(^{\rm tw}\) 末尾の

> \(b\) の一意性は \(\tau\) の単射性から

および §10.1.4/§15.8 の

\[
\rho_i(\operatorname{Ih}_N(\gamma))
=\tau_i(\kappa_i(\gamma)^b)
\qquad(\exists !\,b\in(\mathbb Z/10)^\times)
\]

は一般には正しくない。

反例は campaign 自身の `PASS(ord1)` 分岐である。もし

\[
\kappa_i(G_K)=1
\]

なら、四つの \(b\in\{1,3,7,9\}\) はすべて同じ trivial character を与える。\(\tau_i\) が単射でも \(b\) は区別できない。像が \(\mu_5\) 全体である `ord5` 分岐では一意になるが、補題と結果規則は `ord1` も含むので \(\exists!\) を無条件に置けない。

正しい一意性の出所は二つである。

1. **数学**: \(\varepsilon\) を先に定め、\(b:=\varepsilon^{-1}\bmod10\) とする。
2. **実装**: \(G_K\)-character を見て fitting せず、全 \(\mu_{10}\)-torsor 上の実 local monodromy に対する Rule 1 (7.1) から \(b_i\) を先に一意に測る。

従って B-7\(^{\rm tw}\) の結論は「(2.1) で一意に定めた \(b\) が式を満たす」と書けばよい。§15.8 でも existential fitting を禁止し、**事前凍結した (7.1) の \(b_i\)** を使うべきである。

---

## F5. B-9′(e) と残留条文: **現文のままでは FAIL、amendment now を推奨**

### F5.1 \(\varepsilon\)-free な量

次は exact \(\varepsilon\) に依存しない。

- (P1) の位数。
- (P2) の二 Kummer 類比較。
- R6-full と固定体。
- \(v_i\)、\(T^2-v_i\)、\(T^5-v_i\)、\(r=v_{\rm ns}/v_{\rm sq}^{a_{\rm eff}}\) を使う exact certificate。
- Rule 1 の extraction、停止条件、K3 regression、有限群 covariance。

これらについて B-9′(e) の論証は正しい。

### F5.2 現 frozen semantics との自己矛盾

一方、現 manifest の BRIDGE-FAIL ①と Rule 1 §8.4 は

\[
\rho_i(\operatorname{Ih}(\gamma))=\tau_i(\kappa_i(\gamma))
\]

という untwisted identity を採用している。従って \(\varepsilon\ne1\bmod10\) なら、数学的に正しい twisted bridge を偽 FAIL にできる。

これは単なる周辺注記ではない。`bridge_result_i` はこの橋の PASS/FAIL/UNKNOWN を記録し、結果規則表はそれを入力にする。従って現行 §10.1.2(e) の

> `bridge_result_i` と結果規則表の全遷移が \(\varepsilon\)-free

は、§10.1.4 の「二条文に残留」と同時には真にならない。現行測定計画が actual shadow をまだ測らないことは、**述語の意味**を \(\varepsilon\)-free にはしない。

ゆえに現時点では、B-9′(e) を

> P1/P2/R6/固定体/Kummer certificate と、現行の Belyi-side 測定量は \(\varepsilon\)-free

までに限定するか、下記 amendment の成立を前件に置く必要がある。

### F5.3 推奨 amendment

**note-and-defer ではなく amendment now** を推奨する。既知の偽 FAIL 条件を、外部 shadow 経路が入る直前まで normative text に残す利点がない。

ただし凍結記録を直接上書きしてはならない。manifest v1.6 / Rule 1 v1.4 等の**新 version**を作り、差分ゲートを通すべきである。修理形は次が安全である。

> \(b_i\) は Rule 1 (7.1) で actual \(G_K\) データを見る前に凍結された値とする。  
> BRIDGE identity は
> \[
> \rho_i(\operatorname{Ih}_N(\gamma))
> =\tau_i(\kappa_i(\gamma)^{b_i})
> \qquad(\forall\gamma\in G_K).
> \]
> FAIL は、この**固定済み \(b_i\)** に対する exact な反例 \(\gamma\) 一つ。  
> \(G_K\)-データを見てから \(b_i\) を再 fitting することは禁止する。

pairwise 運用では先に \(b_{\rm sq}=b_{\rm ns}\) の integrity gate を通す。これなら falsifiability を失わず、`ord1` 分岐でも偽の \(\exists!\) を置かない。

この amendment が変えるのは bridge predicate の typing であり、モデル正規形、selection、whitelist、封印時点、二経路 extraction、(7.1) の測定、I-d は変えない。ただし **Rule 1 §8.4 の一行は実際に変わる**ので、「凍結 1 の内容は一行も変わらない」ではなく、

> 凍結 1 のモデル探索・封印・抽出規律は不変。bridge evaluation clause のみ versioned amendment

と記録するのが正確である。

---

## F6. 根基 2 観測列・一様公式: **現行 Belyi 側なら PASS**

K3 v3.1 §6 の記録対象は、モデルの局所主要係数から得る

\[
q_*[u]\quad\text{または}\quad [u^{-1}]_M
\]

である。これは shadow を外部経路で正規化して得る量ではないから、現行の根基 2 観測列と、研究目的に登録した Belyi-side の \(u\) 一様公式は \(\varepsilon\)-free である。

将来 shadow 側で exact class を名指すなら

\[
\mathfrak s(N,H)=[u^{-1}]_M^{\,b_M},
\qquad b_M=\varepsilon^{-1}\bmod M
\]

という共通の profinite \(\varepsilon\) 由来の捩れを明記すること。位数や生成部分群への所属はなお不変でも、exact class・exact exponent の法則は捩れる。この射程注意も §10.1.5 の方向で正しい。

---

## F7. U1/U2 の差分検収

### F7.1 U1: **PASS**

\[
\text{(TB4)}\iff\varepsilon=1\Longrightarrow b=1,\qquad
b=1\iff\varepsilon\equiv1\pmod M
\]

への訂正は正しい。\(\widehat{\mathbb Z}^{\times}\to(\mathbb Z/M)^\times\) の核を忘れた旧同値は除去され、単窓の \(b=1\) から exact (TB4) を戻さない注意も入った。

### F7.2 U2: **PASS**

B-5\(^{\rm u}\) の各項を追うと、

- (i): 慣性**群**の軌道だけ。
- (iii), (7.1): 完備化と Eisenstein。
- (7.2): (TB2) の係数作用。
- (ii-loc): uniformizer 交換。

であり、どれも \(x=\iota(\sigma_\zeta)\) という exact generator equality を使わない。従って

\[
\text{TB4}^{\rm u}\Longrightarrow
\text{B-5}^{\rm u}+\text{B-6}^{\rm tw}
\Longrightarrow\text{B-7}^{\rm tw}
\]

と依存が閉じた。exact (TB4) が B-6 の \(b=1\) 一点にだけ残るという整理は正しい。残る修理は F4 の「\(b\) の一意性の理由」だけである。

---

## F8. U4・GAP/certificate の差分検収

| 項目 | 判定 |
|---|---|
| `failCount <> 0` を certificate 書出し前に `Error` | **PASS**。gate は script 369 行付近、`WriteFile` は 433 行付近 |
| 破壊テスト | 実測記録は retracted NOTE にある。独立 transcript はないが、現ソースの制御順だけで fail-closed 性は確認できるため blocker にしない |
| V3 | **PASS**。`v3bad=0 and v3n=12`、JSON に actual/expected \(12/12\) |
| \(\Phi(x,y,z)\) | **PASS**。三つを生座標から別 fixture で照合 |
| \(\Phi(f_{m,k})\) | **PASS**。実際に用いる全 12 組を検査 |
| aggregate fixture | **PASS**。`all_markings_phi_transport_check=true` |
| 数値 | Node/GAP が \(1296/432/12\) で一致、Node は本便再走 13/13 |
| script/node digest | certificate と現物が一致 |
| input digest | v1 原文とは一致するが final v2.2 には未束縛 |

従って便 45 の実装修理 3 点は閉じた。数値は不変である。

ただし v2.2 本文の自己記述にはまだ stale 箇所がある。

1. 冒頭 6 行目と U4 差分表は GAP **21/21**、他節は **25/25**。現物は 25/25。
2. §0、§8.1、§12.1 に「exact \(b=1\) は二 dessin 比較で load-bearing」という旧説明が残る一方、§10.1/§12.1 末では B-9′ により撤回している。少なくとも「共通 \(b\) が定理なので \(a_{\rm eff}\) から消える」へ同期すること。
3. B-7\(^{\rm tw}\) 末尾の一意性理由と §15.8 の \(\exists!\) を F4 の形へ直すこと。
4. B-9′ の前件表へ (6′) を加え、(e) を amendment 後の意味へ直すこと。

これらは final digest を取る前に直す必要がある。

---

## F9. bundle の `cross-checked` 昇格手順

現 certificate は内部的には整合している。

```text
script  = 4ec09523…e3e232  (現物一致)
node    = 97621fdb…4ec7d7  (現物一致)
input   = 659a9570…6100    (v1 原文と一致)
schema  = bfc-antecedents-check/v3
result  = 25/25, fail_closed=true
```

しかし final 正本 digest `adbf252b…13dae` は束縛していない。さらに本監査の修理で final digest は再び変わる。従って現在はまだ公式の `cross-checked` 昇格を行わない。

順序は次で確定する。

1. F3–F5/F8 の修理を反映した BFC final version と、必要な manifest/Rule 1 amendment を先に凍結する。
2. GAP checker の `input_doc_path` をその **exact final path** へ変更する。
3. Node 13/13 と GAP 25/25 を再走し、数値 \(1296/432/12\) と全 marked-fidelity fixture を再現する。
4. 新 certificate の script/input/node SHA-256 を現物から独立に再照合する。
5. 旧 certificate は「v1 input に対しては整合、final artifact 未束縛」と記録して保存し、新 certificate を現行にする。
6. その時点でのみ
   \[
   \boxed{\text{V1--V8 finite bundle = cross-checked}}
   \]
   としてよい。

この札の射程は有限計算 V1–V8 と marked fidelity であり、B-9′ の紙上証明を Lean `verified` にするものではない。

---

## F10. 最終裁定

- **B-9′(a)**: PASS。
- **B-9′(b)–(d)**: 計算 PASS、(6′) の前件追記が必須。
- **B-9′(e)**: P1/P2/R6/固定体/Belyi-side certificate について PASS。現 `bridge_result_i` まで含む全称は amendment 前には不可。
- **\(a_{\rm eff}=a=1\)**: PASS。exact \(\varepsilon\) 非依存。
- **根基 2 観測列・Belyi-side \(u\) 一様公式**: PASS。shadow-side exact 名指しだけは捩れを明記。
- **U1/U2**: PASS。
- **U4/GAP 25/25 修理**: 実装 PASS。本文同期と final provenance が残る。
- **残留条文**: `amendment now`。ただし既存凍結記録を上書きせず新 version + 差分ゲート。
- **B-9′ の two-mathematician 化**: F3–F5 の修文後に可。現文のままは不可。
- **bundle の `cross-checked` 昇格**: final path/digest への再束縛・再走後に可。

