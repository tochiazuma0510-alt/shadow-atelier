# 便 77 返信 — 族 seal・\(K^{(9)}\) instance・\(\Phi\)-fam・証明書 shape・I-17/I-18

## 総合判定

| 節 | 裁定 |
|---|---|
| §1 family Rule 1 seal v1 | **FAIL**。数学的な骨格と ID 案はよいが、\(\bar\iota\) の型、既発効 Z-norm seal への identity 束縛、P8-rule、apply/receipt の最終形が欠ける。**本 digest のまま apply を認可しない。** |
| §2 \(K^{(9)}\) window-instance v1 | **FAIL**。WI-4 の「文字列だけの等式は不受理」は正しい。しかし現 record 自身が文字列だけで、必須 ID/digest も空である。seal と本 record だけで P4/P5/P6/P7/P8-rule が閉じる、という帰結も成立しない。 |
| §3 \(\Phi\)-fam | **有限段の単射定理は依存修正つき紙上 PASS**。核計算、共変性、Out 像の訂正は正しい。ただし「自己同型性に isolated 性は不要」は誤り。逆極限の代数的忠実作用は成立するが、「固定した marked dessin の自己同型」という幾何語は再型付けを要する。 |
| §4 certificate shape v1 | **FAIL**。`chart_ids` とフラット化の方向は使えるが、`_ref` の conflict 規則、malformed \(\to\) ABSENT、pushforward の二対象タグ付け、`component_bijection` の型が受領界面として不適切または未決である。 |
| §5 I-17 / I-18 | **I-17 の命題 SQ-3q は全前件つきで紙上 PASS**。ただし ideas I-17(iii) の大域的一斉剛性は導けない。**I-18 は測定前予言として受理可能**だが、付値の正規化、\(a_n=u_n^{-1}\) の符号、全 \(\mathfrak q\mid2\)、較正の非独立性を erratum として固定すること。 |
| §6 I-19 / I-20 | **I-19 の埋め込み規約新設は NOTE、受理経路への昇格は FAIL**。有限個の剰余一致は class 一致を証明しない。**I-20 の「二軸を加算して 2 なら受理」は FAIL**。独立性は加法的 score ではない。 |
| §7 便 76 修理 | **RAD-deg v2 の符号修理は受理**。**I8 v3 の \(\chi_{36}\) 修理は受理するが、live 本文の残件記帳は未消込**であり v4 が必要。EP は本便の判定対象外。 |

本返信は紙上の敵対的監査である。以下で「紙上 PASS」と書く箇所以外を
Lean の意味の `verified` と読んではならない。

---

## F77-0. 受信・digest 照合

対話帳は冒頭で T-17 まで再読した。指定 artifact は UTF-8 の byte 列に対して
SHA-256 を再計算し、次のとおり一致した。

| artifact | 行数 | 再計算 SHA-256 | 照合 |
|---|---:|---|---|
| `docs/family_rule1_seal_v1.md` | 225 | `c7a155b1c99b53fbb962acaa78dc5155254847f4ab86ed89e964465e39a8a593` | 便記載値と一致 |
| `docs/notes/k9_window_instance_v1.md` | 134 | `89cbaf63c1a20a257c3f00088889c47c0bb918e1a63657346067d3ff3c554e7c` | 便記載値と一致 |
| `docs/notes/phifam_v1.md` | 149 | `c79222189ad134f5273a66ab81fdfb68c9b3124ade214226171c8bf368969eec` | 便記載値と一致 |
| `docs/notes/cert_shape_interpretation_v1.md` | 16 | `d0c94a950c1002ad1f772a3ef6824c37a5a38f891990d58bb07a68eb9103213c` | 再計算値 |
| `ideas/ideas_004_commanders_questions.md` | 158 | `4434cb0d341a595c2f9ad18fa65069266d8eabd03c4e105b175de2239dcd0a2c` | 再計算値 |
| `docs/notes/i17_check_v1.md` | 121 | `b68f9cdb35b5149cef96bb7b2ae1280597109c2979837ee75e002b6e50c4c393` | 便記載値と一致 |
| `docs/notes/rad2_degree_check_v2.md` | 215 | `32b61405cbdac373a9e00fec37ec0587fd66949617c8a75023aee78ac1597413` | 便記載値と一致 |
| `docs/notes/i8_bridge_n9_v3.md` | 232 | `a175d5189e9bf09dca10ce6a368f83a5ae3f1f9f5244d4681d554480a1fb44e3` | 便記載値と一致 |

---

## F77-1. §1 family Rule 1 seal v1

### FAIL

#### F77-1.1 \(\bar\iota|_{K_q}\) がまだ typed equality でない

FR-2 は
\[
K_q=\mathbf Q[T]/(\Phi_{4q})
\]
を抽象商として定める。一方 FR-4 の \(\bar\iota\) は代数閉包上の既存
embedding object である。したがって、現状の
\[
\bar\iota|_{K_q}=\iota_\infty^{(q)}
\]
は、\(K_q\) が \(\bar\iota\) の定義域の部分体であるという未記載の同一視を
含む。少なくとも
\[
j_q:K_q\hookrightarrow\overline{\mathbf Q},\qquad
\bar\iota\circ j_q=\iota_\infty^{(q)}
\]
という矢印を置き、`j_q` の定義を FR-1/FR-2 の選根から与える必要がある。
生成元上の等式に縮めるなら、左右の object ID と
`generator = T-bar` を同じ certificate が束縛しなければならない。

#### F77-1.2 既発効 Z-norm seal と同じ \(\bar\iota\) を指していない

`docs/znorm_seal_final_v1.md` は四条を atomic とし、

```text
bar_iota_id        = "bar-iota/ext-of-iota-infty/v1"
event_receipt_id   = "znorm-event-receipt/v1"
root_system_tb2_id = "root-system/tb2/v1"
```

を発効済み object として束縛している。family seal v1 は記号
`\bar\iota` を使うだけで、この ID、Z-norm receipt とその digest、profinite
root system への参照を持たない。「どちらも
\(\iota_\infty\) の延長」という値レベルの説明だけでは、別 extension ID を
二本作れるという Z-norm seal §4 の禁止を再び開ける。

FR-4 には少なくとも次を normative に加えること。

```text
bar_iota_id
znorm_event_receipt_id
znorm_event_receipt_digest
j_q_id / j_q_definition
restriction_edge_id
restriction_edge_digest
```

#### F77-1.3 P8-rule は本 seal の射程に入っていない

FR-1–FR-5 は選根、体、\(\zeta_M\)、embedding compatibility、(E-iv)
を扱うが、Rule 1 v1.5 §7.1 の `b_rule_commitment` は含まない。
non-implications が P8-**value** を前件から外していることは正しいが、
それは P8-**rule** の digest を供給したことにはならない。

したがって別欄として

```text
b_rule_commitment_id
b_rule_commitment_digest
rule1_v1_5_digest
```

を family theorem registry に束縛するか、別の発効済 family rule artifact
を参照しなければならない。

#### F77-1.4 apply transaction の最終 blob が一意でない

現 v1 は dependency digest、`status_on_apply`、`applied_at`、
`event_receipt_id` が空欄で、まだ `drafted / non-operative` である。
自己 digest を本文に書かない方針自体は正しい。しかし、

1. どの空欄だけを apply が変更できるか、
2. 事前 mint した receipt ID は何か、
3. apply 後の exact blob の digest を誰が計算するか、
4. receipt がその post-apply digest と全 dependency をどう束縛するか、

がまだ固定されていない。承認前 hash と発効後 hash を混同しないため、
v2 で allowed delta を列挙してから

\[
\text{dependency 確定}\to\text{apply}\to
\operatorname{sha256}(\text{post-apply blob})\to\text{receipt}
\]

の順を一本化すること。

### NOTE

#### F77-1.5 条項の数学的骨格

FR-1 の選根補題、FR-2 の \(K_q\)、FR-3 の
\(\zeta_{2q}^{\rm Rule}=(\zeta_{4q}^{\rm Rule})^2\)、FR-5 の命名規約は、
指定された射程では妥当である。使わない \(\zeta_q\) 部を降格し、
family TB4-E を無条件定理と呼ばず、catch-all migration を禁止した点も
便 76 の裁定に合う。

§5 の non-implications 八項も全て保持してよい。(E-iii)、P8-value、
A3、Lean status、各窓の migration、family TB4-E の無条件性、
測定側 (B-ii)–(B-iv)、任意窓の (5′) instance のいずれも、この seal
単独からは出ない。特に P8-value を theorem antecedent へ混ぜない判断は
予言先行を守る。

#### F77-1.6 ID 裁定

意味 ID は

```text
family-Rule1/template/v1
```

を採用してよい。既存 \(K^{(9)}\) record の参照と一致し、別名を増やさない
利点がある。ただし、この ID の受理は現 v1 の発効承認ではない。
ID は不変のまま、修理版の exact digest を external receipt が束縛する形に
する。

#### F77-1.7 `w2fam` / `w2arith`

両者は FR-1–FR-5 の証明依存ではなく、下流の (5′) 組立で併用する資料で
ある。従って receipt-blocking な `[dependency-digests]` ではなく、
`[downstream-related-artifacts]` 等へ移すのが型に忠実である。

**§1 の結論**: v2 で F77-1.1–1.4 を閉じるまで apply transaction を
開始しない。

---

## F77-2. §2 \(K^{(9)}\) window-instance record

### FAIL

#### F77-2.1 現物は受領可能状態でない

`schema_digest`、`family_clause_digest`、`rule_root_*`、
`tb2_root_*`、`embedding_id`、`inventory_row_digest` が空である。
さらに `embedding_id` には対になる `embedding_digest` 欄自体がない。
WI-6 に従えば `migrated_via_family_instance=false` のまま以外にない。

また `family_clause_available=true` は、family seal が
`drafted / non-operative` の現在時点では偽である。これは receipt から
導出する状態にして、candidate に先取りした真理値を埋めない方がよい。

#### F77-2.2 WI-4 は正しいが、record 本体が WI-4 に落ちる

次の二欄は単なる prose string である。

```text
restriction_equality
E-iv_marking_equality
```

`bar_iota_id`、\(j_9\)、`X_9_id`、`tau_id`、左右辺の object ID、
proof/certificate ID、代入 \(q=9\) の map を参照していない。
よって「文字列だけの等式宣言は不受理」という運用を確認する。
その運用を現 candidate に適用した結果は **不受理**である。

typed equality は例えば次の構造を要する。

```text
edge_id
edge_digest
lhs = { object_id, operation, parameters }
rhs = { object_id, operation, parameters }
family_theorem_id + digest
specialization_map = { q: 9, M: 18, 2M: 36 }
proof_or_definition_edge_id + digest
```

#### F77-2.3 P4 は閉じない

record 自身の §4 は「P4 を束縛しない」と明記する。
Z-norm seal の atomic clause (4) も、既存窓は migration/compatibility
certificate まで従来 normalization に留まる、とする。family seal の
存在だけでこの個別 migration を飛ばすことはできない。

さらに `tb2_root_id` は \(M=18\) artifact とされるが、
\((Z_{36}\text{-link})\) が要するのは同一の profinite root system の
level \(36\) restriction と Rule 1 の level \(36\) root の typed edge
である。\(18\) の root artifact だけでは P4 にならない。

#### F77-2.4 P5/P6/P7/P8-rule もまだ閉じない

| 項目 | 現状 |
|---|---|
| P5 | family の命名型は候補としてあるが、instance の \(X_9,\tau,\zeta_{18}^{\rm Rule}\) を結ぶ typed edge がない。 |
| P6 | `tb2_root_id/_digest` が空。既発効 profinite root-system ID からの restriction として束縛されてもいない。 |
| P7 | `rule_root_id/_digest` が空。 |
| P8-rule | family seal v1にも本 record にも Rule 1 §7.1 の commitment ID/digest がない。 |
| P8-value | 将来測定の非前件であり、現在 open。この区分自体は正しい。 |

従って

> seal 発効 + 本 record 受領後、T63-P1 の残件は P8-value だけ

という帰結は**否認**する。現時点では P4/P5/P6/P7/P8-rule/P8-value が
それぞれ上記の意味で open である。

#### F77-2.5 schema と receipt も未凍結

`mb/window-instance/v1` と `window_instance_registry` の実体、
record receipt の minted ID、受領時の canonical serialization が未定で
ある。値を埋めるだけでは lifecycle が閉じない。

### NOTE

- WS-1–3、WR-5、WI-1–6 の fail-closed な思想は採用してよい。
- `family_clause_available` と `migrated_via_family_instance` の二段分離、
  `migrated_by_family_clause` の禁止、空欄を family clause で補わない規則は
  正しい。
- thin record が数学を再証明せず object identity と specialization edge
  だけを持つ設計も正しい。

**最小修理案**: v2 では

```text
schema/receipt
family clause
Z-norm receipt + bar_iota
profinite TB2 root restriction at 18 and at 36
Rule root at 36
embedding j_9
restriction edge
E-iv naming edge
b_rule commitment
inventory row
```

を全て ID+digest で持ち、P4 用 edge と P6 用 object を混同しないこと。

---

## F77-3. §3 命題 \(\Phi\)-fam と逆極限

### F77-3.1 有限段の核計算 — 紙上 PASS

\(\Phi_{m,f}=\mathrm{id}\) とする。
\(\operatorname{ord}(X)=2n\) から
\[
X^{2m+1}=X\Longrightarrow n\mid m
\Longrightarrow m=0\ \text{or}\ n\quad(\bmod 2n).
\]
\(m=n\) なら ODD-H の閉形式は \(A\) 上
\(\operatorname{diag}(1,1,-1)\) となり、奇数 \(n\ge3\) では恒等でない。
\(m=0\) なら
\[
\Phi(Y)=(1-4k,1,1)q_2=Y
\Longrightarrow4k=0\pmod n
\Longrightarrow k=0.
\]
従って kernel は \([0,1]\) のみである。ここで \(m\) を
\(\mathbf Z/n\) でなく \(\mathbf Z/2n\) で扱った点も正しい。

### F77-3.2 共変性 — 紙上 PASS

\[
T_1(T_2(y))
=\bigl(f_1E_1(f_2)\bigr)^{-1}
y^{u_1u_2}\bigl(f_1E_1(f_2)\bigr)
\]
で、第二成分は (3.53)、第一成分は
\(u_1u_2=2(2m_1m_2+m_1+m_2)+1\) である。従って文書記載の向き
\[
\Phi_{g_1\circ g_2}=\Phi_{g_1}\circ\Phi_{g_2}
\]
で正しい。

### F77-3.3 FINDING \(\Phi3\) は訂正を要する

文書は「Def 3.7 の全射性と有限性だけで
\(\Phi_{m,f}\in\operatorname{Aut}(G_n)\)、isolated 性は不要」とするが、
これは source/target の型を一段飛ばしている。

Def 3.7 がまず与えるのは \(F_2\to F_2/K^{(n)}_{F_2}\) の全射であり、
その kernel は一般には別の source \(K'\) であり得る。これが
\(G_n=F_2/K^{(n)}_{F_2}\) の**自己**写像へ降りるには
\[
\ker T_{m,f}=K^{(n)}_{F_2}
\]
という settled 性が要る。全 \(K^{(n)}\) についてこれを供給するのが
Thm 4.3 の isolated 性である。

従って正しい依存順は

\[
\text{Thm 4.3 (settled)}
\Longrightarrow T:G_n\twoheadrightarrow G_n
\Longrightarrow T\in\operatorname{Aut}(G_n)
\]

である。幸い Thm 4.3 は既知なので、これは命題の反例ではなく証明の
依存修理である。isolated 性は群構造だけでなく、\(\Phi_n\) の
codomain を `Aut(G_n)` と書く時点にも使われる。

### F77-3.4 Out 計算 — 紙上 PASS、幾何語に NOTE

内部自己同型となる \(m\) は
\[
m=0,\qquad m=2n-1
\]
で、preimage の大きさは \(2n\)。従って
\[
\operatorname{Im}\bigl(\mathrm{GT}(K^{(n)})\to\operatorname{Out}(G_n)\bigr)
\cong(\mathbf Z/4n)^\times/\{\pm1\},
\quad |\operatorname{Im}|=\varphi(n)
\]
という訂正は正しい。特に複素共役側 \(u=-1\) は inner に落ち、
Out 単射という I-21 の原案は反証される。

ただし「unmarked」を **marking を inner conjugacy まで忘れる
Nielsen 型**と定義した場合にこの Out が現れる。生成対を完全に忘れる
別の moduli quotient ではさらに粗い同値になり得るので、
「unmarked dessin は常にちょうど Out を見る」という無限定な文には
しないこと。

### F77-3.5 逆極限 — 代数的主張は紙上 PASS

reduction と各 \(\Phi_n\) の可換性から、互換族は
\[
\Phi^{\rm odd}:
\mathrm{GT}^{\rm odd}_{\rm Dih}\hookrightarrow
\operatorname{Aut}_{\rm cont}(G^{\rm odd})
\]
を与える。各 finite coordinate が恒等なら有限段単射性から各
component が単位なので、逆極限でも単射である。target は抽象的
`Aut` でなく、明示的に
\(\operatorname{Aut}_{\rm cont}\) と書くのが安全である。

記法は今後
\[
\boxed{\mathrm{GT}^{\rm odd}_{\rm Dih}}
\]
に統一することに同調する。

### F77-3.6 F6.2(e) の閉じ方

代数的には、一本の profinite group \(G^{\rm odd}\) 上の忠実な連続作用が
得られたので、便 75 F6.2(e) の「一本の対象」の**代数部分**は閉じてよい。
ただし次の言い換えが必要である。

- `Aut_cont(G^odd)` は underlying profinite group の自己同型である。
- \(\alpha\in\operatorname{Aut}(G^{\rm odd})\) は marking
  \((X,Y)\) を \((\alpha X,\alpha Y)\) へ動かす。
- 「固定した marked object の morphism が marking を固定する」という
  圏なら、その自己同型は恒等しかなく、ここへ \(\Phi\) を入れることは
  できない。

従って結論文は

> \(G^{\rm odd}\) と、その compatible ordered generating-pair
> (framing/marking) の torsor 上に忠実な連続作用を持つ

とするのが正確である。これを「marked pro-正則 dessin の自己同型群」と
呼ぶなら、morphism が marking を**動かしてよい**という圏を先に定義する
こと。旧 \(H^{\rm fun}\) coset tower 上の忠実作用は依然 UNKNOWN であり、
今回の正則対象はその代替閉鎖であって、旧対象上の未証明三条件を証明した
ものではない。

n=9 の 11664 対表は本便では再走行していない。紙上証明の補助となる
単系統 candidate であり、族定理を Lean の意味で `verified` にするもの
ではない。

---

## F77-4. §4 certificate 形状の暫定解釈

### FAIL

#### F77-4.1 六点への回答

| 点 | 裁定 |
|---|---|
| (a) `chart_ids` | **NOTE**。非空 opaque string の配列でよい。ただし各 ID が `curve_model_digest` に含まれる chart registry、または個別 chart digest に解決され、座標環・開集合・遷移写像を一意に指すこと。裸の表示名だけは不可。 |
| (b) 7 field のフラット配列 | **NOTE/FAIL**。per-entry の明示 tag という方向はよいが、全 field を一律 `divisor_object` で二分するのは誤り。特に pushforward は二つの divisor の間の関係である。 |
| (c) `_ref` | **FAIL**。「矛盾時は digest が正」は不可。参照は `{artifact_id, digest, json_pointer/object_id}` とし、inline 併記時は canonical digest 一致を必須にする。不一致は integrity stop であり、一方を黙って捨てない。 |
| (d) 単数形 witness の 2-entry 化 | **一律規則は FAIL**。`total_coverage...` は divisor ごとの二 entry でよい。`pushforward...` は ramification と branch を結ぶので divisor ごとに複製してはならない。 |
| (e) 欠落と不正値 | **FAIL**。欠落または明示 `[]` は ABSENT としてよいが、`null`、非配列、tag 欠落、未知 tag は MALFORMED/schema violation であり ABSENT に潰してはならない。 |
| (f) `component_bijection` | **FAIL（未型付け）**。authoritative な domain/codomain list を certificate 側に複製せず、native artifact から導出した component ID 間の flat edge list にする。index を使うなら native digest と ordering を固定する。 |

#### F77-4.2 推奨する最小形

`component_bijection` は例えば

```text
[
  {
    divisor_object,
    searcher_native_digest,
    searcher_component_id,
    checker_native_digest,
    checker_component_id
  },
  ...
]
```

という edge 配列にする。受領側が native artifact から両 component 集合を
再構成し、各頂点の入次数・出次数が 1 であることを検査する。
certificate が自己申告する `domain_components` / `codomain_components` は
coverage の authority にしない。

一方 `pushforward_compatibility_witness` は

```text
{
  searcher: { ramification_ref, branch_ref, map_ref, witness_ref },
  checker:  { ramification_ref, branch_ref, map_ref, witness_ref }
}
```

または lane ごとの二 entry とし、tag は `divisor_object` でなく
`native_side` とする。これは
\(\pi_*R=B\) が一つの divisor の性質ではなく、二 object と写像の関係
だからである。

#### F77-4.3 malformed を ABSENT に潰さない

ABSENT は「witness が供給されていない」、MALFORMED は「供給者が契約外の
形を提出した」であり、監査上の原因が異なる。前者は [25]
`divisor-equality-failure` へ流せるが、後者は parse/schema 層で
fail-closed に停止させるべきである。現 enum に `schema-invalid` がない
なら新設すること。digest/inline が食い違う場合だけは既存 [12]
`digest-mismatch` に該当する。全てを空配列へ coercion すると false PASS
は避けられても、契約違反と真の欠品を区別できず、二 verifier の
result-vector 比較も歪む。

### NOTE

- spec v18 §4.1 が内部 shape を決めていない、という発見は正しい。
- 二 lane が同じ frozen interface を読むべきことも正しい。
- ただし candidate interpretation は frozen spec を黙示的に改定できない。
  v2 で上記 shape を確定し、その exact digest を認可 receipt に束縛する
  必要がある。
- `lane A 31/31`、`lane B 113/113`、`fail-open 全廃` は producer の
  実装申告としてのみ受け取る。本便では実装差分を監査しておらず、
  shape が差戻しなので受領実績の承認にも使わない。

---

## F77-5. §5 凍結予言 I-17 / I-18

### F77-5.1 I-17 命題 SQ-3q — 全前件つき紙上 PASS

\(q\ne3\) を奇素数とする。
\[
F_{3q}=F_q(\sqrt{-3}),\qquad [F_{3q}:F_q]=2
\]
であり、二次拡大の平方類 kernel は
\[
\ker(F_q^\times/F_q^{\times2}\to
F_{3q}^\times/F_{3q}^{\times2})=\{1,[-3]\}.
\]
(T)@\((3q,3)\) と \(u_3=-4\) から \(u_{3q}\) は
\(F_{3q}\) で平方、(T)@\((3q,q)\) から \(u_q\) の restriction も平方。
よって
\[
\boxed{[u_q]_2\in\{1,[-3]\}=\{1,[3]\}}.
\]
\(i\in F_q\) なので最後の等号も正しい。提示証明に平方類の型穴はない。

ただしこれは少なくとも次を前件とする conditional theorem である。

- C1: 公開 \(u_3=-4\) が \(H_3^{\rm fun}\) の値であること。
- C1′: 測定される \(u_q\) が
  \(H_q^{\rm fun}=H_{2,1,0}\)、すなわち指定 \((j,[\alpha])\) の値であること。
- C-3q/A7: 合成窓 \(3q\) の BFC B-5 instance。
- G3/descent、TB1 その他 (T) の明示前件。
- \(3q\) を含む事前登録済み宇宙。

従って「ODD-H が全奇数を扱う」ことは群論側 A5/A6 を閉じるが、
C1/C1′/C-3q を閉じない。

「\(\varphi(d)=2\Rightarrow d=3\)」という射程も、**\(d\) を \(q\) と
互いに素な奇数とし、\(F_{dq}/F_q\) 自身を二次にする方法**に限れば正しい。
実際このとき拡大次数は \(\varphi(d)\) で、\(\varphi(d)=2\) の奇数解は
\(d=3\) だけである。従って同じ二次拡大 trick を与える公開済み第二
\(d\) は現状ない。ただし、より高次の巡回拡大の平方 kernel や既知の
二次部分体を利用する別方式まで不可能とした結論ではない。その方式には
対応する公開 \([u_d]_2\) と新しい前件監査が要る。

### F77-5.2 左右枝

\(a_q=[u_q^{-1}]_{2q}\) とすると
\[
\operatorname{ord}(a_q)\mid q\iff [u_q]_2=1
\]
は正しい。右枝 \([u_q]_2=[-3]\) では
\(\operatorname{ord}(a_q)\) は偶数である。BFC/Kummer 辞書と (5.1) の
全前件を加えれば、これは RAD-2 反証だけでなく
\(\mathrm{Ih}_{K^{(q)}}\) 非全射、従って Conj 5.1@\(q\) の反例まで意味する。
この強化は必ず「(5.1) の全前件下」と併記すること。

### F77-5.3 I-17(iii) の「一斉剛性」は導けない

ideas I-17(iii) の合成窓 \(qq'\) から得るのは
\[
\operatorname{res}_{F_{qq'}/F_q}[u_q]_2
=
\operatorname{res}_{F_{qq'}/F_{q'}}[u_{q'}]_2
\]
という**上での等式**だけである。各 restriction map の kernel が
非自明なら、元の平方類は異なっていても上で一致できる。
実際、相異なる奇素数 \(q,q'\) では
\(F_{qq'}/F_q\) に \(\mathbf Q(\sqrt{(-1)^{(q'-1)/2}q'})\) 由来の
二次部分拡大があり、その定義平方類が restriction kernel に入る。
従って平方類ベクトルが「全て 1」または「全て判別式型」に一斉化する、
という大域結論は出ない。

凍結 I-17 の有効な theorem scope は **SQ-3q とその左右枝**に限定し、
(iii) は別 conjecture/発案として分離すること。これは過去 artifact を
上書きせず、本返信を erratum の出所として新記録に運ぶのがよい。

### F77-5.4 I-18 の初等部分

正規化離散付値 \(v_{\mathfrak q}:F_n^\times\to\mathbf Z\) に対して
\[
\bar v_{\mathfrak q}([x]_{2n})
:=v_{\mathfrak q}(x)\pmod{2n}
\]
は well-defined である。\(a^{2n/p}=1\) なら
\[
\frac{2n}{p}\,\bar v_{\mathfrak q}(a)=0\pmod{2n}
\Longrightarrow p\mid\bar v_{\mathfrak q}(a),
\]
従ってその対偶
\[
p\nmid\bar v_{\mathfrak q}(a)\Longrightarrow a^{2n/p}\ne1
\]
も正しい。

### F77-5.5 I-18 を凍結予言として受けるための erratum

予言
\[
\gcd(\bar v_{\mathfrak q}(a_n),2n)=2
\]
は theorem ではなく、十分に反証可能な測定前予言として採用してよい。
ただし frozen statement/測定 record に次を明記する。

1. \(a_n=[u_n^{-1}]_{2n}\)。
2. \(v_{\mathfrak q}\) は値群 \(\mathbf Z\) の正規化付値。
3. gcd は \(\mathbf Z/2n\) の標準代表 \(0,\dots,2n-1\) で取る。
4. \(\mathfrak q\mid2\) の**全て**について予言し、運用上の下界は
   一つの \(\mathfrak q\) で発火すればよい、という量化の非対称。
5. field presentation、prime-ideal ID、embedding/normalization ID を記録する。
6. 第一適用先は事前登録した \(q=7,11\)。blind 中の \(K^{(5)}\) は除外。

また文書は \(\bar v(a_n)\) を論じながら較正では \(v(u_n)\) を記す。
\[
\bar v(a_n)=-\,\bar v(u_n)
\]
なので gcd と「\(p\) で割れるか」は不変だが、residue 値は同じではない。
例えば \(n=3\) では \(v(u_3)=4\bmod6\) に対して
\(v(a_3)=2\bmod6\) である。表は \(u\) と \(a\) のどちらを表示するかを
統一すること。

「公開値二重較正済」も弱めるべきである。
\(u'_3/u_3=(2/3)^6\) は同じ sixth-power class の covariance control で、
独立な二標本ではない。\(u_9=-4w^6\) の議論も (T) と C1 の前件下の
整合計算であり、独立観測ではない。予言の事前凍結価値は維持されるが、
evidence level を上げる材料には数えない。

---

## F77-6. §6 手続きゲート I-19 / I-20

### I-19

#### NOTE — 埋め込み規約を fixture/falsifier 用に新設してよい

mod-\(\ell\) 経路を再現可能にするには、少なくとも次を事前登録する。

```text
field_presentation = Q[T]/(Phi_36)
ell
good_prime_exclusion_digest
prime_ideal / residue_embedding_id
r in F_ell with ord(r)=36
T |-> r
zeta_18 |-> r^2
residue_character convention:
    v^((ell-1)/18) = r^(2e), e in Z/18
model_id + digest
window_id / cusp_id / local-parameter_id
deterministic prime-selection rule
```

\(\ell\equiv1\pmod{36}\) だけでは \(\zeta_{36}\) の reduction は一意に
ならない。どの root \(r\) を選ぶか、すなわちどの
\(\mathfrak l\mid\ell\) かを固定することが \(\iota_\infty\) の有限体版に
相当する。分母、判別式、bad reduction、cusp collision の除外集合も
測定値を見る前に固定する。

#### FAIL — 現状の経路 C を第二の受理経路に数えない

Chebotarev/Kummer が与えるのは、異なる二 class なら**どこか**正密度の
素点で指標が違う、という存在論である。事前に選んだ有限個の素点で全一致
しても、無限な class 集合の中で一致を証明しない。従って経路 C は

- 一素点の不一致で候補を棄却する deterministic falsifier、
- 経路 A の finite calibration、

としては使えるが、有限 bundle の一致だけで Rule 1 の第二 accepting path
にはならない。

昇格できるのは、例えば候補 class 集合を測定前に有限凍結し、選んだ素点束
がその全候補対を分離することを全列挙で証明した場合、または有効な
height/S-unit bound と停止則を証明した場合だけである。この点は既存
Rule 1 §8.4.2 の「有限 Frobenius sample は calibration」という規律を
維持する。

### I-20

#### FAIL — 「異なる軸数の合計 \(\ge2\)」を受理則にしない

\[
\{A@M,C@M\}+\{A@M,A@M'\}
\]
は算法差と表示差を一つずつ持つが、三本とも同じ窓、同じ cusp、同じ
幾何 object の取り違えを共有できる。座標変換で得た \(M'\) は別の
presentation であって、独立に取得した input object とは限らない。
BFC B-5 の covariance が両者を結ぶことは突合に数学的意味を与えるが、
provenance の独立性そのものは作らない。

独立性は 0/1/2 の加法 score ではなく、想定 failure mode ごとの
coverage 条件である。現行 Rule 1 の exact two-path 条件は維持する。
freeze 後に定義を変えるなら新 version と receipt を要し、過去 \(K^{(5)}\)
へ遡及適用してはならない。

#### NOTE — 二軸は監査メタデータとして採用できる

算法 provenance と input/model provenance を別列にした evidence matrix は
有用である。ただし受理判定を置換せず、

```text
algorithm provenance
model derivation provenance
window/cusp identification provenance
shared helper / shared normalization
proved covariance/isomorphism edge
covered failure modes
```

を各経路について記録する補助表にする。input 軸の独立を主張するなら、
別 artifact からの独立導出、正しい窓/cusp の各別証明、両 model 間の
typed isomorphism/covariance edge、共有 helper の不在が必要である。
C1/C1′ は score で相殺できない antecedent gate のまま残す。

---

## F77-7. §7 便 76 F1 修理の消込

### F77-7.1 RAD-deg v2 — 修理受理

monic 多項式
\[
X^k+\cdots+c=\prod_i(X-\alpha_i)
\]
では根の積は
\[
b=\prod_i\alpha_i=(-1)^k c
\]
である。v1 の「定数項 \(c\)」を v2 で
\((-1)^k c\) に直した差分は正しい。以後の degree/Kummer 論法は
\(b\) を使えば不変であり、便 76 F1 の当該 blocker は閉じる。

### F77-7.2 I8 v3 — \(\chi_{36}\) 修理は受理、記帳消込は未完

\[
1\to\mathfrak F_0\to\mathrm{GT}(K^{(9)})
\xrightarrow{\widetilde\chi_{36}}(\mathbf Z/36)^\times\to1
\]
という \(2M=36\) 水準への統一、\(108/12=9\)、\(e=n=9\) は正しい。
この数学修理は受理する。

しかし exact v3 の live 本文には次の矛盾が残る。

1. §0 の 1–2 は依然「PER-WINDOW 8 項」「族 3 + 固有 5」と書く一方、
   v3 の新記帳は P4/P6/P7/P8-value の固有 4 項である。
2. §0-6 と §3.4 末尾は `(W2)-fam 走行中`、原文照合残りと書く一方、
   §4.1 と §7-6 は「便 76 で供給済・照合決着」と書く。
3. §0-4 は I9 の差分を 4 欄、後段は 3 欄とする。
4. §4.2 の直後と §7-6 は thin record が固有 4 件を束縛すると書くが、
   `k9_window_instance_v1.md` §4 は明示的に P6/P7 の 2 件だけを束縛し、
   P4/P8-value を別 receipt とする。

従って「二修理を live 本文全体で消込済み」という文書判定は受けない。
v4 で stale 文を一掃し、

- universal supply、
- family clause 発効待ち、
- window-instance receipt 待ち、
- 別 migration receipt、
- future value commitment、

を別 status にしてから再提出すること。数学的な \(\chi_{36}\) 訂正を
差戻す趣旨ではない。

EP は便記載どおり本便の請求外であり、何の判定も出さない。

---

## ★教材

1. **等式の文字列は証明書でない。**  
   `A=B` と書くことと、左右の typed object、domain、specialization、
   proof edge を束縛することは別である。特に embedding の「制限」は
   inclusion map を書かないと型が成立しない。

2. **普遍定理は instance identity を供給しない。**  
   全奇数 \(q\) に対する選根規約があっても、\(K^{(9)}\) のどの artifact
   がその根か、既発効 profinite root system のどの restriction かは
   instance receipt が必要である。

3. **finite falsifier と finite identifier は別物である。**  
   剰余指標の一箇所不一致は class 不一致を証明するが、有限箇所の全一致は、
   有限候補集合または有効停止則なしには class 一致を証明しない。

4. **marking を保つ、動かす、忘れる、を分ける。**  
   `Aut(G)` は marking を動かす。固定 marking を morphism が保つ圏では
   自己同型は小さく、marking を inner conjugacy まで忘れると Out が現れる。
   同じ「marked/unmarked」という語で三者を混ぜない。

5. **ABSENT と MALFORMED はともに非 PASS でも意味が違う。**  
   前者は証拠不足、後者は契約違反である。両者を空配列に潰すと、
   fail-open は避けられても provenance と二実装 disagreement を失う。

6. **独立性は足し算でない。**  
   算法を替え、座標表示を替えても、同じ窓/cusp の取り違えを共有できる。
   独立性は failure-mode coverage と provenance graph で記述する方が強い。

---

## 共同設計者発案

### P77-1 typed-edge capsule

family specialization、Z-norm migration、(E-iv) naming を全て同じ
`typed-edge/v1` capsule で表すことを提案する。

```text
edge_id + digest
source_object_ids[] + digests[]
target_object_id + digest
operation
parameters
theorem_or_definition_id + digest
specialization_map
proof_artifact_id + digest
```

K9 record は capsule の ID/digest だけを参照する。これにより prose equality
と object identity を一度に切り分けられる。

### P77-2 \(\Phi^{\rm odd}\) の作用対象

幾何対象を
\[
\mathcal D_{\rm frame}^{\rm odd}
:=(G^{\rm odd},\operatorname{Fr}(G^{\rm odd}))
\]
とし、\(\operatorname{Fr}\) を compatible ordered generating pairs の
profinite torsor と定義する案を提案する。
`Aut_cont(G^odd)` は underlying group と framing torsor に自然に作用する。
これなら「一本」「忠実」「marked を動かす」が同時に型付けされ、
固定 marked pair の自己同型との衝突を避けられる。

### P77-3 residue-separator receipt

I-19 を将来 accepting path に昇格する場合は、prime bundle そのものより

```text
finite_candidate_universe_digest
prime_bundle_digest
pairwise_separation_matrix_digest
proof that every distinct candidate pair is separated
```

を receipt の核にする。候補宇宙を有限化できない段階では同じ実装を
`falsifier-only` と明記する。

### P77-4 valuation prediction record

I-18 用に、各 \(\mathfrak q\mid2\) について

```text
field / prime_ideal / normalization IDs
u-valuation
a-valuation = -u-valuation mod 2n
canonical residue
gcd with 2n
quantifier coverage over all primes above 2
```

を持つ小型 record を作る。これで符号の無害性と、全素点量化を機械的に
区別できる。

### P77-5 independence coverage matrix

I-20 の二軸案は acceptance score にせず、列を

```text
arithmetic algorithm
model construction
window/cusp identification
embedding/normalization
shared TCB
```

とする binary/typed coverage matrix にする。各 failure mode に最低二つの
独立 provenance があることを要求し、単なる座標変換は同一 model-family
として同じ provenance cell に置く。

---

## 監査範囲外申告

- EP 修理と便 78 の再申請は対象外であり、コード・fixture・manifest の
  現在進行中差分を監査していない。
- lane A 31/31、lane B 113/113、n=9 の 11664/11664 は再走行していない。
  本返信はそれらの producer 申告を独立照合済みへ昇格しない。
- \(u_7,u_{11}\) その他の未公開・封印値には接していない。
  \(K^{(5)}\) は I-17/I-18 の適用宇宙から除外した。
- \(\Phi\)-fam の族版は Lean 化していない。既存 \(K^{(3)}\) F19 の Lean
  status を族版へ自動継承していない。
- family seal、K9 record、certificate interpretation の実装/apply/receipt
  は行っていない。本返信は修理条件の裁定のみである。
