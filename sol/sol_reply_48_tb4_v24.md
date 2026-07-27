# 総合判定: **差戻し**

二部を独立に判定する。

- **Part A: 差戻し。** GAP certificate の v2.4 への再束縛自体は **PASS** した。しかし BFC v2.4 には未清掃の stale 全称と新たな数式破損が残り、amendment v2 の antecedent bundle は未証明の **(5′) 自体を前件に入れる循環**を起こしている。従って **Rule 1 v1.4 / manifest v1.6 の版上げを許可しない**。
- **Part B: 条件付き PASS（核心計算は PASS、現行の TB4-A(a) と一括版上げは差戻し）。** 補題 TB4-2 の解析持ち上げと
  \[
  \zeta_n^\varepsilon=\bar\iota^{-1}(e^{2\pi i/n})
  \]
  は、明記された位相–étale 比較を前件にすれば正しい。(Z-norm) を追加した TB4-B も正しい。一方、**既存凍結文だけ**から \(\varepsilon\equiv1\pmod {20}\) を出す TB4-A(a) には、(TB2) の \(\zeta_{20}\) と Rule 1 の体生成元 \(\zeta_{20}\) が同一であるという型付けがない。また TB4-C は (C1) 単独から (C2) 全体を導いていない。

従って本便では、(Z-norm) 追記、状態札更新、Rule 1 §7.4 強化、文献要請 13(ii) 取下げの**一括承認はしない**。下記の有限差分を直した再提出で足り、解析持ち上げの計算を開け直す必要はない。

---

## F1. 現物・digest・検算

配送対象を UTF-8 で全行読んだ。

| artifact | 行数 | SHA-256 | 判定 |
|---|---:|---|---|
| `docs/week4-BFC攻略_opus_v2.md` | 997 | `52b77ffdcd632adefb5b490e416bd51e77940dadcaa72cd88a3cb24215d0a83d` | 配送値一致 |
| `docs/amendment_5prime_draft.md` | 193 | `a921cb70e37f0978f36e1878f8d013cee1ededaf23880c384bbbb7f59c8a8eaa` | 配送値一致 |
| `docs/week4-TB4導出_opus_v1.md` | 392 | `0c64c4410fc41736b110df49457033cb213a0cb8cee31d294b3d3a7b53518926` | 配送値一致 |
| `search/tb4-monodromy-check.mjs` | 132 | `3e43dee2caf0e54e7897b72030c67a06d58a080bdb8e3bd307d576eb5c7a2e39` | 配送値一致 |
| `search/bfc-antecedents-check.g` | 435 | `104e748bb44c34024bd725d608659c0265d4b5d1b3e2c669cc9908ac63d825d9` | 配送値一致 |
| `certificates/bfc/bfc-antecedents.json` | 1 | `f2b5d20e06c09faf410d27455b55c80f7edb17b666b65e256c349fbd98b55797` | 配送値一致 |

BFC / amendment / TB4 はいずれも **CR 0、C0 制御文字 0**。この点は修理済みである。

`node search/tb4-monodromy-check.mjs` を独立に再走し、**15/15 PASS** を再現した。ただしこれは Kummer 被覆の玩具的数値サニティであり、K\(^{(5)}\) に接触せず、位相–étale 比較や根系の型付けを証明しない。従って状態は `verified` でも `cross-checked theorem` でもない。

---

# Part A

## F2. BFC v2.4 の F2.3/F2.4 清掃: **FAIL**

### F2.1 修理できた箇所

§10.1.4 の表 625–626 行は、

- `bridge_result_i`: `amendment-pending`
- `pair_gate` / `saturation_result`: `bridge_result_i` を入力にする限り同じ札

へ同期した。冒頭 31 行と補題 B-9′ の箱 996 行も、Belyi-side 限定形と amendment 後の全称を区別している。この局所差分は **PASS**。

### F2.2 blocker A1 — stale 全称が現役のまま残る

同じ文書内で次がなお現役の断定になっている。

1. **488 行**
   > exact \(b=1\) が要るのは二 dessin 比較 \(a_{\rm eff}\) の側だけ

   これは B-9′(a)(c) がまさに撤回した文言である。

2. **539 行、543 行、612 行、875 行**
   > \(\varepsilon\) 依存は campaign の判定から完全に消える  
   > campaign の判定は exact \(\varepsilon\) に依存しない  
   > campaign は \(b\) の値を一度も必要としない

   §10.1.4 の 625–634 行は、現行 untwisted predicate では `bridge_result_i` とその下流結果に依存が残る、と正しく書いている。従って上記の全称は、少なくとも

   > Belyi-side の列挙量については無条件。bridge/result 全称は amendment 成立後。

   と限定しなければ自己矛盾する。

3. **514 行、769 行**

   関所名がなお `exact b=1` である。F2.4 の規律どおり、関所名は **exact \(\varepsilon=1\)**、\(b=1\) はその mod \(M\) 帰結、と同期すべきである。

従って「stale 全称の全清掃」は未完了である。

### F2.3 blocker A2 — byte 清掃で新たな数式破損

707–708 行で

```text
a_{
m eff}=a=1
```

と改行されている。意図は明らかに

\[
a_{\rm eff}=a=1
\]

であり、現物は TeX として壊れている。C0 が 0 であることと、数式が保存されたことは別の検査である。ここを直せば BFC digest が変わるので、現 certificate はもう一度再束縛が必要になる。

### F2.4 certificate 再束縛そのもの: **PASS**

certificate 現物は次を満たす。

- `schema = bfc-antecedents-check/v3`
- `pass_count = 25`
- `fail_count = 0`
- `fail_closed = true`
- `provenance.script_sha256 = 104e748b…25d9`
- `provenance.input_doc_path = docs/week4-BFC攻略_opus_v2.md`
- `provenance.input_doc_sha256 = 52b77ffd…a83d`
- Node counterpart の path/digest も束縛

checker 本体 386、427 行も v2 path を読む。従って **現在の 997 行 artifact に対する再束縛は正しい**。Node/GAP の独立表現が既に一致している有限計算 bundle は、この provenance について閉じている。

ただし BFC 本文 7、31、346、690、870、913 行はなお「provenance 束縛が残る」「現 certificate は v1 を指す」と書く。これは certificate を最終本文の後で発行する自己参照順序から生じる status-layer の問題である。本文を再編集して status を直すたび certificate が失効するので、最終状態は本文でなく外部 CLAIMS / certificate ledger に置くべきである。

なお checker 冒頭 1、11 行のコメントも v1 のままだが、実読込 path と certificate 値は v2 であり、これは非 load-bearing なコメント stale である。

---

## F3. amendment v2

### F3.1 便 47 の二 blocker と付随修理

| 項目 | 判定 | 理由 |
|---|---|---|
| 8.4.0: Freeze 1 rule / Freeze 2 value | **PASS** | 65–67 行は actual \(b_i\) を Freeze 2 / atomic BRIDGE-IN に置き、\(u\)・\(G_K\) 観測より前と明記した |
| F10.1 schema | **PASS** | rule digest、actual value、source artifact、事前観測宣言を分離した |
| 8.4.1 (5′\(_b\)) | **PASS** | `(5′)` の既存名を上書きせず operative predicate だけを捻った |
| 8.4.2 C-i / C-ii | **条件付き PASS** | field/kernel 一致単独を明示排除した点は正しい。C-ii の operational schema は下記 F3.3 を要する |
| ord1 修文 | **PASS** | 空虚なのは \(b\) の同定だけで、左辺の自明性試験は残る |
| I-n | **PASS** | fitting 違反 run の隔離・同 run 内の救済禁止まで入った |
| digest / predicate ID | **PASS** | readable version だけでなく SHA-256 と schema ID に束縛した |
| I-n と I-h / I-i | **矛盾なし** | I-n は観測順序・fitting、I-h/I-i は別の provenance/integrity 原因。欠落 field は新 schema では I-n とする |

`b_observed_before_gk = true` は必要だが自己申告でもある。将来は Freeze 2 event ID、観測 artifact ID、順序を示す append-only log digest を併記するとより fail-closed になる。これは本便の blocker にはしない。

### F3.2 blocker A3 — AB-1 が結論を前件に入れる循環: **FAIL**

amendment 123 行は

```text
(AB-1) FORMAL-IN((0)(1)(2)(3)(5′)(6′))
```

とする。しかし現 manifest v1.5 の 22 行は

```text
FORMAL-IN = (0)(1)(2)(3a–d)(6′-i)(6′-ii) ...
(5′) は PENDING
```

と明示する。(5′) は BFC が導くべき橋そのものであり、BRIDGE-FAIL が試す対象である。これを antecedent bundle に入れると、

- 個別反例は、既に (5′) を真と仮定した上で (5′\(_b\)) の破れを探すことになる。
- (P1) の破れも、(5′)+(6′) から \( \operatorname{ord}([u^{-1}]_M)\mid e\) を出す \(R^{\rm cyc}_{\rm formal}\) と正面衝突し、反証分岐が空になる。
- pairwise の破れから「少なくとも一方の橋が偽」を言いたいのに、前件で exact bridge を真と置いてしまう。

これは単なる表記重複ではなく、**falsifier を論理的に殺す blocker** である。

修理は一行でよい。

```text
(AB-1) 現行 manifest の FORMAL-IN:
       (0)(1)(2)(3a–d)(6′-i)(6′-ii) の証拠 ID、
       K5-1、j_i、formal a=1。
       (5′) および (5′_b) は含めない。
```

(AB-2) に B-9′ の共通枠組み前件と (6′-ii) を置く判断は正しい。(AB-1) と一部重複しても害はなく、むしろ theorem provenance と campaign evidence の役割が違うので残してよい。

### F3.3 C-ii の operational な意味

「oriented \(\mu_{10}\)-torsor 同型」は数学的には十分読めるが、実装者の提出物を一意にするには `orientation_certificate` が単なる boolean / field ID であってはならない。少なくとも次を束縛すべきである。

1. source/target torsor の artifact ID と digest。
2. 凍結済み \(\zeta_{10},\tau_i,j_i,b_i\) と、選択した Kummer root の ID。
3. 選択基点の像、または全点の明示写像 \(\Phi_i\)。
4. \(\mu_{10}\)-equivariance の向き:
   \[
   \Phi_i(\xi\cdot p)=\tau_i(\xi^{\,b_i})\Phi_i(p).
   \]
5. \(G_K\)-equivariance:
   \[
   \Phi_i(\gamma\cdot p)=\rho_i(\operatorname{Ih}_N(\gamma))\Phi_i(p),
   \]
   を全 \(\gamma\) について証明する artifact。

この二式を満たして初めて C-ii は C-i と同じ character 情報を保持する。有限個の \(\gamma\) のサンプルや抽象 field equality では不足する。

### F3.4 Part A の最終判定

amendment の中心設計は維持してよい。しかし、

1. BFC stale 全称の清掃、
2. 707–708 行の \(a_{\rm eff}\) 修復、
3. AB-1 から (5′) を除去、
4. C-ii certificate schema の上記一意化、
5. 修復後 BFC digest への certificate 再束縛、

が終わるまで Part A は PASS でない。従って **Rule 1 v1.4 / manifest v1.6 の版上げは未許可**。

---

# Part B

## F4. 規約表 (C1)–(C11) の監査

| 規約 | 判定 | 監査結果 |
|---|---|---|
| **C1** | **PASS** | W-1 は左作用式を凍結している |
| **C2** | **部分 PASS** | A5 v4 補題 C の \(p\cdot v_1=v_0\) は forward transport を実際に使う。ただし C1 単独から C2 全体は出ない |
| **C3** | **PASS / load-bearing** | 後合成の左作用は TB4\(^{\rm u}\) に明記される。反転表にも載せるべき |
| **C4** | **型不足** | Rule 1 の体生成元 \(\zeta_{20}^{R}\) の像は凍結済み。しかしそれが TB2 の根系の \(\zeta_{20}^{T}\) と同じとは書かれていない |
| **C5** | **PASS** | 反時計回り正、\(x=\gamma_0\) は Rule 1 §1.1 に凍結済み |
| **C6** | **PASS（A3 条件）** | 正の実分枝による標識は妥当。標識の平行移動は巡回 torsor 上の作用を変えない |
| **C7** | **UNKNOWN の分類は正しい** | \(n\nmid20\) の具体値を凍結する正典条項は見つからない |
| **C8** | **UNKNOWN の分類は正しいが前件に要る** | \(\bar\iota\) の延長は他所で凍結されていない。存在は標準だが、比較データとして明示量化が必要 |
| **C9** | **PASS / 非本質** | 置換合成は凍結済み |
| **C10** | **PASS** | 証明は \(\mathrm{Gal}(C_n/U)\cong\mathbf Z/n\) の任意同一視を使っていない |
| **C11** | **PASS** | radial comparison の変更は cyclic torsor の共役＝平行移動で消える。ただし A3 自体は消えない |

正典 grep では C7/C8 を既に exact に凍結する文は見つからなかった。従って「実は他所で閉じていた」という近道はない。

重要なのは、**C4 が凍結済みであることと、C4 が TB2 の根系を凍結することは別**だという点である。同じ字形 \(\zeta_{20}\) を二文書で使うだけでは typed equality にならない。

---

## F5. 補題 TB4-C: **現題名は FAIL、条件付き内容は PASS**

62–65 行の証明が実際に示すのは、

> 経路が自分の向きへ forward transport として作用すること、および輸送の関手性を認めれば、C1 は積を「右の経路、左の経路」の順に読むことを決める。

である。これは正しい。

しかし「経路が自分の向きへ輸送する」は C2 の半分であり、補題の仮定 63 行に既に入っている。抽象的な左作用式

\[
(AB)\cdot i=A\cdot(B\cdot i)
\]

だけでは、幾何経路を forward transport で読むか inverse transport で読むかは決まらない。左作用は、既に選ばれた群積に関する作用公理を言うだけで、群積と path concatenation の対応を単独では生成しない。

従って正しい分解は、

\[
\boxed{\text{C1 + forward path transport/A3 + 関手性}\Longrightarrow
\text{right-to-left concatenation}}
\]

である。A5 v4 補題 C の三つの型チェックは forward transport の独立証拠として使えるので、核心を捨てる必要はない。ただし依存表 A8 の

> A4 から導出、独立仮定ではない

は撤回し、**A3 または A5 v4 補題 C に依存**と書くこと。

---

## F6. 補題 TB4-2: **A3 条件付き PASS**

解析計算は正しい。

\[
\beta(t)=\delta e^{2\pi it},\qquad
w_j(t)=\bar\iota(\zeta_n)^j\delta^{1/n}e^{2\pi it/n}
\]

は、

- \(w_j(t)^n=\beta(t)\)
- 指定始点を持つ
- 連続である

を満たす。被覆空間の持ち上げ一意性により唯一で、終点は \(e^{2\pi i/n}\) 倍である。接基点から \(\delta\) への正実軸 radial path も明示されている。標識を一定の \(\mu_n\)-元だけ変えても、巡回平行移動同士の共役は自明なのでモノドロミー乗数は変わらない。

薄いのは解析持ち上げではなく、最後の

> 位相的 forward transport が algebraic fiber functor の後合成左作用と同じである

という **A3** である。文書自身も 266、346 行でこれを framework input と認めている。従って TB4-2 の正しい前件は少なくとも

\[
\text{C1, C5, chosen }\bar\iota,\text{ radial comparison, A3}
\]

である。「三本の工房規約だけ」の結論ではない。

---

## F7. TB4-3 と TB4-A の核心

### F7.1 TB4-1 / TB4-3

後合成作用の計算

\[
\iota(\sigma)\cdot(\xi\beta^{1/n})
=\chi_n(\sigma)\xi\beta^{1/n}
\]

は正しい。TB4\(^{\rm u}\) で

\[
x=\iota(\sigma_\zeta^\varepsilon)
\]

と書き、TB4-2 と比較すれば

\[
\boxed{\zeta_n^\varepsilon
=\eta_n
=\bar\iota^{-1}(e^{2\pi i/n})}
\tag{*}
\]

が出る。torsor 作用の自由性による乗数の一意性も正しい。

従って、任意に選んだ \(\bar\iota\) を前件に明記すれば、

\[
\varepsilon=\chi_{\rm cyc}(\vartheta),\qquad
\vartheta(\zeta_n)=\eta_n
\]

という TB4-A の一般式は **PASS**。

### F7.2 blocker B1 — 「既存三文書だけで mod 20」は型付け不足

(TB2) は compatible root system \((\zeta_n^T)\) を固定する。一方 Rule 1 (1.5)–(1.7) は

\[
K=\mathbf Q[T]/(\Phi_{20}),\qquad
\zeta_{20}^R=\bar T,\qquad
\iota_\infty(\zeta_{20}^R)=e^{2\pi i/20}
\]

を固定する。両者を同一視する条項は現行正典にない。

これは表記上の潔癖さではなく、結論を変える。\(t\in\widehat{\mathbf Z}^{\times}\) を

\[
t\equiv3\pmod {20}
\]

となるように取り、TB2 の compatible system を canonical system の \(t\) 乗として選ぶ一方、Rule 1 の体生成元はそのまま canonical root とする。この選択は、両根を同一視しない現行文面のすべてを満たす。

すると

\[
\bar\iota(\zeta_{20}^{T})=e^{2\pi i\cdot3/20},
\qquad
\eta_{20}=\bar\iota^{-1}(e^{2\pi i/20}),
\]

なので (*) は

\[
3\varepsilon\equiv1\pmod {20},
\qquad
\varepsilon\equiv7\pmod {20}.
\]

従って \(b=\varepsilon^{-1}\pmod {10}=3\) であり、現行文面だけから \(b=1\) は出ない。

修理は次の typed equality を一行入れるだけでも有限レベルには足りる。

\[
\boxed{\zeta_{20}^{\rm TB2}
=\zeta_{20}^{\rm Rule1}\in K\subset\bar{\mathbf Q}.}
\tag{Z20-link}
\]

同じ記号を使っていたから同じ、ではなく、この同一視を normative clause にすること。

### F7.3 TB4-A の修正版

定理を三段に分けるのが安全である。

1. **TB4-3（比較式）**: A1–A3、C1、C5、chosen \(\bar\iota\) の下で (*)。
2. **TB4-A20（有限正規化）**: さらに (Z20-link) と Rule 1 (1.6) の下で
   \[
   \varepsilon\equiv1\pmod {20}.
   \]
3. **TB4-B（全正規化）**: さらに全 \(n\) の (Z-norm) の下で
   \[
   \varepsilon=1.
   \]

この分割なら、どの結論が framework、finite root link、full root normalization のどれを使うかが一意になる。

---

## F8. (Z-norm): **数学的には PASS、条文を atomic seal にせよ**

\(\iota_\infty\) の延長

\[
\bar\iota:\bar{\mathbf Q}\hookrightarrow\mathbf C
\]

を一つ選び、

\[
\zeta_n^{\rm TB2}:=\bar\iota^{-1}(e^{2\pi i/n})
\]

と定めれば compatible system になり、\(n\mid20\) では Rule 1 の選択と整合する。従って (Z-norm) は新しい算術仮定ではなく、未指定だった比較データの選択であり、**採用可能**である。

ただし §4.3 の悉皆表には「同じ字形の object identity」が抜けている。安全な条文は次を一つの atomic seal にする。

```text
TB2-norm/comparison-root seal:
  (i)  bar_iota extends Rule1 iota_infty;
  (ii) zeta_n^TB2 = bar_iota^{-1}(exp(2*pi*i/n)) for every n;
  (iii) in particular zeta_20^TB2 = zeta_20^Rule1;
  (iv) all TB4 comparisons use this same bar_iota and this same root system.
```

これで TB4-B の exact \(\varepsilon=1\) は正しい。別に A3 の

```text
positive topological transport ↔ algebraic postcomposition-left action
```

を framework seal として残すこと。(Z-norm) は A3 を証明しない。

---

## F9. §6 反実仮想表: **不完全**

掲載された C1、C2、C5、C4、C7 の反転は有用で、時計回りなら \(\varepsilon=-1\) という数値検算とも一致する。しかし少なくとも次の経路が未掲載である。

1. **C3 の反転**: 後合成左作用を前合成・右作用として読む。
2. **A3 の反転**: 位相 forward transport を algebraic action の逆へ送る comparison。
3. **root-object のずれ**: TB2 の \(\zeta_{20}\) を Rule 1 の \(\zeta_{20}\) の \(t\) 乗として読む。これは単なる \(\pm1\) でなく任意の \(t\in(\mathbf Z/20)^\times\) を生む。

したがって「反転経路をすべて列挙した」とはまだ言えない。特に第三項は本便の具体的 countermodel である。

---

## F10. Part B の状態札・運用変更

### F10.1 現時点で認める状態

| 主張 | 判定 |
|---|---|
| TB4-1 | **paper-proof PASS** |
| TB4-2 | **paper-proof / A3-framework-conditional PASS** |
| TB4-3 の比較式 (*) | **paper-proof / framework-conditional PASS** |
| 現行 TB4-A(a): 既存三文書だけで \(\varepsilon\equiv1\pmod {20}\) | **FAIL（Z20-link 欠品）** |
| TB4-B: 明示的 (Z-norm) 下で \(\varepsilon=1\) | **条件付き PASS** |
| 数値 checker | **15/15 sanity only** |

従って、修理後なら

- TB1/TB3/TB4\(^{\rm u}\): framework
- TB2 + TB2-norm: 工房規約
- TB4: 上記 framework と規約に相対的な paper theorem

という札へ更新できる。現時点ではまだ更新しない。

### F10.2 Rule 1 §7.4 の文言

> \(b_i\ne1\) は必ず実装事故

は強すぎる。TB4 は A1–A3 の framework-conditional な紙上定理であり、不一致の診断候補には、

- 実装の左右・向きの事故
- input / root-system seal の不一致
- 位相–étale comparison の適用不一致
- 紙上 framework 前件または証明の誤り

がある。

安全な文言は、

> 採用済み framework、TB2-norm/comparison seal、凍結 input がすべて正しく実現されている限り \(b_i=1\) は定理である。\(b_i\ne1\) は新しい算術現象として受理せず integrity quarantine とし、実装・transport・input seal・framework proof を順に監査する。

である。

### F10.3 文献要請 13

root normalization 自体は工房規約なので、外部文献に exact root の選択を決めてもらう必要はない。しかし A3 の comparison orientation は load-bearing のままである。従って文献要請 13(ii) は**全面取下げでなく**、

> 正の位相 transport が algebraic fiber functor の後合成左作用へ送られ、逆作用でないことの標準比較定理・記法確認

へ狭めるのがよい。(i)(iii) は委嘱どおり維持。

---

## F11. TB4 と amendment の相互作用

便 47 F10.3 の設計を維持する。

仮に修理後 TB4-B により \(\varepsilon=1\)、従って真値 \(b_i=1\) が定理になっても、

- Freeze 1 で rule を事前コミットする。
- Freeze 2 で actual \(b_i\) を \(u/G_K\) 観測前に記録する。
- 観測後 fitting と \(\exists b\) PASS を禁止する。
- \(b_i\ne1\) を integrity quarantine に送る。

という規律は regression control として必要である。定理があることは、実装がその定理の規約を実現したことを保証しない。従って TB4 の成立を理由に amendment の二段コミットや I-n を削ってはならない。

---

## F12. ★教材 T1 / T2

### T1: **採用**

枠組み札を立てる前に、姉妹凍結文の対を突合する運用は有効である。本便では、

\[
\text{TB2 の根系}\quad\leftrightarrow\quad
\text{Rule 1 の field generator}
\]

を単独表だけで読んだため、同じ \(\zeta_{20}\) という字形を同じ object と誤認した。単独項目がそれぞれ正しくても、橋の typed equality がなければ結論は出ない。

### T2: **採用、二欄に強化**

規約表には

1. **対の整合の相手**
2. **両者を運ぶ比較写像 / equality の artifact ID**

の二欄を置くべきである。「相手」だけでは、今回の \(\zeta_{20}\) のように同名 object が無言で同一視される。比較写像の向きまで記録すれば A3/C3 の逆転も同じ表で検査できる。

### 本便の追加教材

1. **同じ glyph は同じ object ではない。** 別文書の \(\zeta_{20}\) を使って剰余結論を出すなら equality を前件に置く。
2. **左作用式は forward transport を定義しない。** action law、path concatenation、transport direction、topological–étale comparison を分ける。
3. **C0=0 は数式保存の証明ではない。** byte filter 後には delimiter/brace と改行境界を別に検査する。
4. **falsifier の前件に被検命題を入れない。** theorem-use 用の FORMAL antecedent と experiment/falsifier 用の FORMAL-IN は別 bundle ID にする。

---

## F13. 共同設計者としての発案（常設）

### F13.1 `TB4-comparison-seal/v1`

TB4 の依存を一つの machine-readable seal にまとめることを提案する。

```text
root_system_id
rule1_zeta20_id
zeta20_equality_certificate
bar_iota_id
topological_loop_orientation = ccw
path_transport = forward
algebraic_action = postcomposition_left
top_etale_comparison_orientation_certificate
```

この seal の digest を Rule 1、BFC、結果 record の三者が参照する。同じ root name を人間が再解釈する余地を消せる。

### F13.2 theorem を finite / profinite に分離

実運用の K\(^{(5)}\) に必要なのは \(\varepsilon\bmod10\) だけである。従って、

- TB4-A20 / Z20-link: \(M\mid20\) の finite theorem
- TB4-B / Z-norm: 全 \(n\) の profinite theorem

を別札にする。全 profinite normalization の版上げ事故が K\(^{(5)}\) の finite 結論を不必要に巻き込むことを防ぐ。

### F13.3 AB bundle を二種類に分離

```text
THEOREM-ANTECEDENT-Rcyc
  = ... + (5′_b)                 # 定理を適用する側

FALSIFIER-ANTECEDENT-BFC
  = ... without (5′), (5′_b)    # 橋を試す側
```

と別 ID にする。今回の AB-1 は、前者の一覧を後者へ転記した事故である。

---

## F14. 再提出の最小差分

1. BFC 488、539、543、612、875 行等の stale 全称を `amendment-pending` に限定し、514、769 行の関所名を exact \(\varepsilon=1\) へ統一。
2. BFC 707–708 行の \(a_{\rm eff}\) を修復。
3. amendment AB-1 から (5′) を除去し、現 manifest の FORMAL-IN を逐語転記。
4. C-ii の operational certificate を F3.3 の二つの equivariance 式で定義。
5. TB4-C を「C1 + forward transport/A3」へ修文。
6. TB4-A に chosen \(\bar\iota\)、A3、(Z20-link) を明記。
7. (Z-norm) を F8 の atomic seal とし、反実仮想表へ C3/A3/root-object mismatch を追加。
8. 修復後 BFC digest に GAP certificate を再束縛。

この差分が通れば、Part A の Rule 1 v1.4 / manifest v1.6 と、Part B の TB2-norm / TB4 状態更新を同一 version event で再審査できる。

監査範囲外は、K\(^{(5)}\) の個別モデル・\(u\)・封印値、Model-Builder/S5 探索、Lean 形式化、外部文献の原文照合、TB4 checker 以外の新規機械計算である。GAP certificate は現物・provenance・fail-closed fields を検収したが、出力 artifact を書き換える再走はしていない。本返信以外のファイルは変更していない。
