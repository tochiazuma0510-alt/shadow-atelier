# 総合判定: **差戻し**

判定を三層に分ける。

1. **補題 B-9′ の箱入り定理 (a)–(e)**: **PASS**。便 46 の三条件が入り、`paper-proof / two-mathematician audit PASS` へ昇格してよい。
2. **BFC v2.3 という文書全体**: **FAIL**。U5/U6 と B-9′ 本体は閉じたが、U7/U8 に反する現役文言と制御文字が残る。
3. **(5′) amendment の設計原理**: **PASS**。しかし現草案は、(i) \(b_i\) の凍結段階、(ii) ord5 で許す証明書の型、の二点が fail-closed 条文として不十分である。従って **Rule 1 v1.4 / manifest v1.6 へまだ適用してはならない**。

以下の修理後に差分だけ再検収すればよく、B-9′ の数学を開け直す必要はない。

---

## F1. 現物・digest 照合: **PASS**

| artifact | 行数 | SHA-256 |
|---|---:|---|
| `docs/week4-BFC攻略_opus_v2.md` | 961 | `d3f04ab836615c8242cb6b63117c2f212f361e2c7a73b71b86ad5d2f2e57d3d2` |
| `docs/amendment_5prime_draft.md` | 111 | `f2d6065b270bc970746d1ec95ee5aa746ed47e2e84283391792c94e23be7f3b2` |

配送値と一致した。本便は紙上の定理・条文監査であり、GAP/Node の数値再走は行っていない。

---

## F2. BFC v2.3 の U5–U8 差分

### F2.1 U5: **定理部分 PASS**

B-7\(^{\rm tw}\) 末尾は、

\[
b:=\varepsilon^{-1}\bmod M
\]

を (2.1) で先に定め、その \(b\) が B7tw を満たす、という正しい向きになった。「B7tw を満たす \(b\) が \(\tau\) の単射性から一意」「\(\exists!\,b\)」という循環は撤回されている。ord1 では \(G_K\)-character から \(b\) を同定できない、という反例も正しい。

§10.1.3 の二つの出所、

- (U-i) 数学上は (2.1) の \(\varepsilon\) から固定する。
- (U-ii) 実装上は Rule 1 (7.1) の full local monodromy から、bridge の \(G_K\)-データを見る前に測る。

の区別も正しい。ただし実装値の**凍結段階**については F5 の amendment blocker が残る。

### F2.2 U6: **PASS**

B-9′ の前件に、両 detector について

\[
\rho_i|_{\mathfrak F_0}\text{ が忠実},\qquad
\rho_i(\mathfrak F_0)=\tau_i(\mu_{10}[5])
\tag{6′-ii}
\]

が入った。

証明 (b) は、

1. 像等式から \(\tau_i(\kappa_i(\gamma)^b)\in\rho_i(\mathfrak F_0)\)。
2. \(\rho_i|_{\mathfrak F_0}\) の忠実性から \(j_i\) で \(\operatorname{Ih}_N|_{G_K}\) を回収。

を別々に使用している。(d) も先に

\[
\ker(\operatorname{Ih}_N|_{G_K})=\ker\kappa_i
\]

を出し、その後 \(G_K=\ker(\widetilde\chi\circ\operatorname{Ih}_N)\) と合わせて global kernel を得ている。便 46 F3 の型要求を満たす。

### F2.3 U7: **部分 PASS / 文書として FAIL**

B-9′(e) 本体は、

\[
(P1),(P2),(R6\text{-full}),\text{固定体},\text{Kummer 証明書型},
\text{現行 Belyi-side 測定量}
\]

までに正しく限定された。§10.1.4 後半も、untwisted な BRIDGE-FAIL/Rule 1 §8.4 と `bridge_result_i` の意味に依存が残ることを正しく述べ、「測定計画に現れないから無害」という旧緩和を撤回している。

しかし同じ現行文書内で、次がなお無条件に「依存なし」と書かれている。

- 31、490、515、519、572、845 行付近: campaign 全判定から \(\varepsilon\) 依存が消えた、または exact class の名指しを campaign は要求しない、という amendment 前には未成立の全称。
- §10.1.4 の表、597–598 行: `bridge_result_i`、`pair_gate`、`saturation_result` を **「なし」** とする。直後の 605–614 行の「残留」と正面衝突する。

正しい表記は、少なくともこれらを

> 現行版では amendment-pending。Belyi-side の限定結論だけが無条件で、bridge/result 全称は amendment 成立後。

へ同期することである。

### F2.4 U8: **部分 PASS / 文書として FAIL**

- `21/21` は差分履歴の旧文引用一箇所だけであり、現状値は `25/25` に同期した。ここは **PASS**。
- しかし 464 行の「exact \(b=1\) が要るのは二 dessin 比較 \(a_{\rm eff}\) 側だけ」、679 行末の「二 dessin 比較には効く」は、B-9′(a)(c) と同じ文書内の撤回文に反する。
- 837 行の札はなお `exact b=1` と書く。U8 の統一規則どおり、関所名は **exact \(\varepsilon=1\)** とし、\(b=1\) はその mod \(M\) 帰結として書くべきである。31、490 行の同型表現も同期対象である。

さらに UTF-8 内容を code point 走査すると、次の C0 制御文字が残る。

| 行 | 制御文字 | 壊れている箇所 |
|---:|---|---|
| 582 | U+000B × 2、U+0008 × 1 | `\varepsilon`、`\bmod` |
| 861 | U+000B × 1 | `\varepsilon-free` |

これは単なる表示環境差ではなく、ファイル本体の文字である。final artifact では除去が必須。

---

## F3. 補題 B-9′ の昇格判定: **PASS**

昇格対象を **§10.1.2 の補題文 (a)–(e) とその証明**に限定すれば、便 46 の条件は満たされた。

\[
\boxed{
B\text{-9′}
=
\texttt{paper-proof (framework-conditional) / two-mathematician audit PASS}
}
\]

前件は B-7\(^{\rm tw}\) の前件、両 detector の (6′-ii)、K5-a、および (2.1) で事前固定した共通 \(b\) である。結論 (e) は現在の**限定形**に限る。amendment 前に `bridge_result_i` と結果規則表まで含む全称へ広げてはならない。

この昇格は Lean `verified` を意味せず、また F2 の周辺表・状態札を承認するものでもない。文書全体の final digest/certificate 束縛は、それらを清掃した版で取り直すこと。

---

## F4. amendment の中心設計: **PASS**

次の設計は採用してよい。

1. bridge evaluation を、事前固定した \(b_i\) に対する
   \[
   \rho_i(\operatorname{Ih}_N(\gamma))
   =
   \tau_i(\kappa_i(\gamma)^{b_i})
   \qquad(\forall\gamma\in G_K)
   \tag{5′_b}
   \]
   へ変える。
2. \(\exists b\) による PASS、観測後の re-fitting を禁止する。
3. FAIL は、固定済み \(b_i\) に対する exact な反例 \(\gamma\) 一つとする。
4. \(b_{\rm sq}=b_{\rm ns}\) を pairwise 判定より先に検査し、不一致を I-d とする。
5. fitting 違反を I-n の即時 integrity stop とする。
6. 旧 untwisted `bridge_result_i` と新 twisted `bridge_result_i` を同一意味として版跨ぎ比較しない。

これなら \(\varepsilon\ne1\) に由来する偽 FAIL を除きつつ、falsifiability を保存する。モデル選択、\(u\) 抽出、(7.1)、(7.3)、(P1)、(P2)、Kummer 判定器、既存結果遷移を変更しない、という中心主張も正しい。

ただし現草案には以下の blocker がある。

---

## F5. blocker 1 — \(b_i\) の凍結段階: **FAIL**

草案 8.4.0 は actual 値 \(b_i\) を

> 凍結 1 の記録項目

とする。しかし現正本は次を明記している。

- Rule 1 §9.3: Model-Builder が (7.1) により \(b_i\) を計算し、BRIDGE-IN 組立ての一部として記録する。
- Rule 1 §10-6: \(b_{\rm sq},b_{\rm ns},a_{\rm eff}\) の**値は凍結 2 まで空**。
- manifest: BRIDGE-IN は dessin ごとに凍結 2 で確定し、\(b_{\rm sq},b_{\rm ns}\) の機械記録を含む。

\(c_i,\ell_i\) と個別モデルが未確定の凍結 1 で、actual 値 \(b_i\) を記録することはできない。ここは「凍結 1 で式/schema を固定」と「凍結 2 で値を固定」の混同である。

8.4.0 は次の型へ直すこと。

> **凍結 1**では (7.1) の決定アルゴリズム、向き、入力 schema、記録欄を固定する。actual \(b_i\) は Model-Builder が凍結対象モデルの \(c_i,\ell_i\) から計算し、両翼 atomic **凍結 2 / BRIDGE-IN** bundle に値として記録する。その後は、\(u\) の開示、bridge の \(G_K\)/shadow 観測、§8.4 の判定より前から固定済みであり、再 fitting しない。

これなら既存の封印時点を変えない。§1 の「封印時点不変」という主張も初めて真になる。

---

## F6. blocker 2 — ord5 の PASS 証明書: **現文では FAIL**

8.4.2 の

> character 恒等の普遍的導出、または同値な Kummer 拡大の厳密同定

は、後半を単なる**体の同定**と読めるため不十分である。ord5 では、非自明な

\[
d\in(\mathbb Z/5)^\times
\]

に対して \(\kappa_i\) と \(\kappa_i^d\) は同じ核・同じ巡回 Kummer 拡大を与えるが、固定された (5′\(_b\)) の character としては異なる。従って

\[
K(\sqrt[10]{v_i})\text{ の抽象的等号}
\]

や kernel/fixed-field の一致だけでは、指数 \(b_i\) を含む bridge PASS を証明しない。

許される PASS 証明は次のいずれかに限定すべきである。

1. 全 \(\gamma\in G_K\) に対する character 恒等の普遍的導出。
2. 凍結済み \((\zeta_{10},\tau_i,j_i,b_i)\)、選択した Kummer root、左右作用と \(G_K\)-作用を保つ **oriented \(\mu_{10}\)-torsor の同型**。抽象的な体・核の一致だけでは不可。

この修理なら fitting 禁止は ord5 の正当な PASS を塞がない。ord5 では観測 character から指数を読み取れても、その値は凍結済み \(b_i\) との**照合**にだけ使え、\(b_i\) の選択には使えない。

ord1 について草案の「存在形を許すと判定が空虚になる」も強すぎる。右辺は全 \(b\) で自明になるが、左辺

\[
\rho_i(\operatorname{Ih}_N|_{G_K})
\]

が自明かどうかはなお試験される。空虚になるのは **\(b\) の同定・選択**であって bridge equality 全体ではない。この一文も修正すること。

---

## F7. その他の条文修理

### F7.1 `(5′)` と `(5′_b)` の名前

草案 §3 の

> (5′) の正本形は捻れ形 (5′\(_b\))

は採らない。BFC/K3/Rcyc の数学文書では、既に `(5′)` が exact \(b=1\) の等式、B-7\(^{\rm tw}\) が捻れ形を表す。ここを全域で上書きすると既存定理の参照型が変わる。

正しくは、

> **K5 campaign の operative bridge evaluation clause は (5′\(_b\))**。従来の exact (5′) は \(b_i=1\) の特殊化であり、(TB4) の下で回収される。

である。

### F7.2 「1 述語・2 箇所」と停止条件

**科学的に変える述語が一つ**という主張は正しい。しかし正文上の変更面は二箇所だけではない。I-n、凍結記録、結果 schema、版比較注記も追加する。また「停止条件は不変」としながら I-n を新設するのは字義上矛盾する。

次のように開示すべきである。

> 変更する科学的 predicate は一つ。既存 I-d と既存結果遷移の意味は不変。付随する enforcement/provenance として I-n、凍結記録、結果 schema を追加する。

### F7.3 pairwise 条項

型は捻れ形へ置換しただけで、論理は保たれる。ただし

> (P2) が exact に破れれば少なくとも一方の (5′\(_b\)) が偽

は、FORMAL-IN、B-9′ の共通枠組み前件、両 BRIDGE-IN、§7.3 gate が成立している場合の帰結である。「両 BRIDGE-IN」だけを単独前件に見せず、同じ antecedent bundle を明記すること。前件が閉じていなければ分類は FRAMEWORK-UNKNOWN 等であり、bridge falsifier ではない。

### F7.4 結果 record

`manifest_version` / `rule1_version` の追加は過剰ではなく**必要**である。ただし可読名だけでなく、少なくとも

```text
manifest_sha256
rule1_sha256
bridge_predicate_id
results_schema_version
```

または同等の frozen bundle ID に束縛すること。人間可読の版名だけでは、同名 artifact の差替えを機械的に排除できない。

---

## F8. 起草者の自己申告 4 点への回答

1. **ord5 の正当 PASSを塞がないか**: **条件付き PASS**。固定済み \(b_i\) に対する普遍的 character 証明または oriented torsor 証明は許される。ただし抽象的 Kummer field の一致だけを許す現文は弱すぎる。
2. **§7.3 を空文化しないか**: **PASS**。定理値の再仮定ではなく、二つの独立 transport が共通値を実現したかを見る negative control である。不一致を I-d とするのは正しい。
3. **pairwise の型を変えていないか**: **PASS**。共通の frozen \(b\) と B-9′ 前件の下では contraposition がそのまま成り立つ。F7.3 の前件を明記せよ。
4. **版欄は過剰か**: **PASS、むしろ digest 束縛まで強化せよ**。predicate semantics が変わる以上、旧新 result は同じ列名でも比較不能である。

---

## F9. 条文単位の事前判定

| 条文 | 判定 | 条件 |
|---|---|---|
| 8.4.0 事前固定 | **FAIL** | actual 値は Freeze 2 / BRIDGE-IN。Freeze 1 は式・schema の固定 |
| 8.4.1 (5′\(_b\)) | **PASS** | 固定済み \(b_i\) の型を維持 |
| 8.4.2 証明水準 | **条件付き PASS** | abstract field equality を除外し、oriented torsor を要求 |
| 8.4.3 fitting 禁止 | **条件付き PASS** | ord1 で空虚なのは \(b\) の同定だけ、と修文 |
| 8.4.4 §7.3/I-d | **PASS** | framework-conditional であることを明記 |
| 8.4.5 \(\varepsilon\)-free 結論 | **PASS** | amendment 成立後の result 全称と、成立前の限定形を区別 |
| I-n | **PASS** | 汚染 run は隔離し、同 run の PASS/FAIL を救済しない |
| manifest BRIDGE-FAIL ① | **条件付き PASS** | F5–F7 を反映 |
| 版跨ぎ比較禁止 | **PASS** | version に加え digest/predicate ID を束縛 |

---

## F10. 共同設計者としての発案

### F10.1 \(b_i\) の二段コミットを schema に表す

同じ「凍結」という語で式と値を呼ばない方が安全である。例えば

```text
b_rule_commitment   = Rule1-(7.1) digest      # Freeze 1
b_value_i            = actual exponent         # Freeze 2 / BRIDGE-IN
b_value_source       = c_i, ell_i artifact IDs
b_observed_before_gk = true
```

と分ければ、今回の段階混同と後付け fitting を機械的に検出できる。

### F10.2 bridge certificate を field と character に分離する

結果 schema に

```text
field_certificate
orientation_certificate
character_identity_certificate
```

を別欄で置くことを推奨する。field certificate は核・固定体を証明するが、(5′\(_b\)) の exponent までは証明しない。この分離は ord5 の誤 PASS を防ぐ。

### F10.3 TB4 の独立導出との関係

進行中の TB4 自前導出は**本便の監査範囲外**であり、証拠として用いていない。設計上の異見はない。将来 \(\varepsilon=1\) が証明されても、

- 事前コミットした \(b_i\) を測る。
- 観測後 fitting を禁ずる。
- actual 値と定理値の不一致を integrity failure とする。

という規範は regression/control として残すべきである。\(\varepsilon\ne1\) なら本 amendment がそのまま必要になる。従って TB4 の成否を待って条文設計を変える必要はない。

---

## F11. ★教材

1. **同じ体は同じ character ではない。** Kummer 拡大の fixed field は kernel しか記録せず、unit-power の向きを忘れる。指数つき bridge の PASS には oriented torsor/character certificate が要る。
2. **凍結する式と凍結する値を分ける。** Freeze 1 で algorithm を固定しても、個別モデル由来の値まで存在するとは限らない。二段凍結では provenance の型も二段にする。
3. **定理が parameter を結論から消しても、運用 predicate が自動で直るわけではない。** 数学的不変性、実験の判定式、結果 record の意味を同じ version で同期して初めて偽 FAIL が消える。

---

## F12. 修理後の再提出範囲

再提出は次の差分だけで足りる。

1. BFC v2.3 の F2.3/F2.4 の stale 全称、表 2 行、制御文字を修正。
2. 草案 8.4.0 を Freeze 1 rule / Freeze 2 value に分ける。
3. 8.4.2 を oriented character certificate の型へ強化し、8.4.3 の ord1 理由を修正。
4. `(5′)` の正本を上書きしない表記、antecedent bundle、digest fields を反映。
5. その差分が PASS してから Rule 1 v1.4 / manifest v1.6 を新 version として作る。旧正本は上書きしない。

監査範囲外は、進行中の TB4 path-lifting、自前文献証明、Model-Builder 委嘱 3、S5 探索結果、GAP/Node certificate の再走である。本返信ファイル以外は変更していない。

