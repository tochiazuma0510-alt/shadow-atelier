# 便 61 返信 — `Z-norm-seal/v1` apply 検収 / \(N_\infty\) stage-2 spec v3 監査

## F1. 総合判定

冒頭開示の snapshot 事故について、commit `3e52ca5` により便 59/60 の
**ターン完了時の最終版**へ記録が訂正されたことを確認した。今後 60 秒の
安定待ちを入れる措置も妥当である。過去返信は記録として変更せず、本便を
現在の裁定とする。

| Part | 判定 | 裁定 |
|---|---|---|
| **Part A — `Z-norm-seal/v1` apply** | **差戻し** | component 1/2、final seal、TB4 v2.5、Rule 1 v1.5、manifest v1.7 の核は通った。しかし \(B_{\rm FC}\) v2.12 が、全窓に対する \((Z_{2M}\text{-link})\) まで `Z-norm-seal/v1` が供給すると一般化しており、final seal の K3/A5=`pending` と正面衝突する。また component 1/2 の自己 SHA 記入枠は、提示 hash を確定した後に自ファイルを書き換える指示になっている。**原子的 payload は未成立なので発効宣言を出さない。** |
| **Part B — \(N_\infty\) spec v3** | **数学層 PASS / freeze 層は差戻し** | `N∞-N`、`N∞-1:1`、`N∞-pair`、`N∞-swap`、`N∞-div`、`N∞-criterion` の紙上核は通る。しかし採用裁定された D-2 はまだ一文の案で、certificate schema・digest・二 native divisor への束縛が無い。sealed schema も A/B の native divisor/partition を別々に保存せず、ACCEPT 用 reason code と B9 の field bundle 束縛も欠ける。**freeze ID は発行しない。実装認可も出さない。Model-Builder は LOCKED のまま。** |

従って本便では、Part A の `status_on_apply` / operative hash / receipt R /
CLAIMS 記帳を進めず、Part B の searcher/checker 実装にも着手してはならない。

---

## F2. 対象 blob・digest・形式検収

委嘱実体
`ops/inbox_codex/sol_task_61_apply_and_specv3.txt`、対話帳 T-17 まで、裁定 72、
対象 8 文書、便 60 最終返信、および必要な旧版差分を読んだ。

監査対象は委嘱指定 commit `b2f2985` である。現在 HEAD `98b0237` の対象
8 path は `b2f2985` と byte 同一であり、worktree とも一致した。

| artifact | LF 行数 | SHA-256 | 委嘱値 |
|---|---:|---|---|
| `docs/znorm_forall_proof_v1.md` | 87 | `a8eee73829a8f66c925f1eee18a8cd92fd505a8709d526d20ed594ce7c0d9c55` | 一致 |
| `docs/k5_migration_record_v1.md` | 89 | `ae1e9ef051c04d02c78f23bfb16b358da2077bfe65b684b9da6c998adb291120` | 一致 |
| `docs/znorm_seal_final_v1.md` | 211 | `022e6e2e92457666dec9194945e5ef5b5f94b646fae1be0fc7b2965a4a84dfe1` | 一致 |
| `docs/week4-TB4導出_opus_v1.md` | 892 | `b3ec912b7170fea8fcdcc77c6bca96e944abe676668591ff85c6c28b7388a77a` | 一致 |
| `docs/week4-K5_Rule1_v1_5.md` | 1052 | `861e934be7e309d4cd722874f2b04a9f44f1ab2f7c4f372dc225966813d2f431` | 一致 |
| `docs/manifest_k5_v1_7.md` | 220 | `307c57942c1ba9050fc3d9ee424ca812300da41665d39387defc4cbdfc57377d` | 一致 |
| `docs/week4-BFC攻略_opus_v2.md` | 1240 | `01741c0aef5fadad174a2b800911e48aa3ffbbc86033f7ebc619c2f28fd3c903` | 一致 |
| `docs/week4-NInfty_stage2_spec_v3.md` | 487 | `83c9f58887a508d2bbe451a456e41e6ff19f5b2eaa6fdfb957516f6a57aede3b` | 一致 |

全 8 blob で CR、TAB、LF 以外の C0 制御文字はいずれも 0 だった。これは
blob 同一性と形式の照合であり、以下の数学・型裁定とは別である。

---

# Part A — apply 検収

## F3. 通った部分

### F3.1 component 1 — 数学内容 PASS

任意の延長
\(\bar\iota:\overline{\mathbb Q}\hookrightarrow\mathbb C\) を一つ固定し、

\[
\zeta_n^{\rm TB2}
 :=\bar\iota^{-1}(e^{2\pi i/n})
 =\zeta_n^{\rm can}\qquad(n\ge1)
\]

とする一つの全称証明になっている。有限列挙 digest を全称命題に偽装して
おらず、compatible/primitive、\(n=20\) restriction、非含意も正しい。
特に、これ単独では他窓の Rule-side root object identity を与えない、と
§5.3 で明記している。

### F3.2 component 2 — K5 migration の数学・型 PASS

`bar_iota_id` の restriction、既存 finite edge
`rule1-tb2-root-equality/v1`、Rule 1 root object の identity を一段で束ね、
K5 だけを `migrated` にしている。finite edge を profinite edge へ改名せず、

```text
compatibility_status = migrated
```

と

```text
root_normalization_level = profinite
```

を同一視しない限定も正しい。

### F3.3 final seal — P59-A1–A4 と F4.2–F4.4 は PASS

- profinite edge と level-20 edge は別 ID・別 scope;
- K5=`migrated`、K3/A5=`pending`、他窓は明示 catch-all;
- `migrated` の K5 digest は component 2 の実値;
- \(n\nmid20\) の空白を「具体値と typed comparison data」に縮小;
- catch-all と default fallback を分離;
- K3 の root-link-free な \(b_{\rm op}=1\) と、link を要する
  \(t_{12}=1\) 等を分離;
- final seal hash は receipt 側に置く C \(\to\) R 構造

を確認した。final seal 自身に receipt **digest** を書かない設計は正しい。

### F3.4 TB4 / Rule 1 / manifest の個別差分 — PASS

TB4 v2.5 の P-1 札更新と P-2 の (R1)(R2)(R3)、Rule 1 v1.5 と manifest
v1.7 の typed reference block は、既存 `Z20-link-seal/v1` と finite edge
を保存し、seal reference の追加だけで既存 record を profinite へ自動昇格
させない。これら三差分単独には blocker を認めない。

---

## F4. blocker A-1 — \(B_{\rm FC}\) v2.12 が窓別 link を全称供給にした

final seal §3 の inventory は明瞭である。

```text
K5 : migrated
K3 : pending
A5 : pending
other windows : not_assessed
```

seal が新たに全称供給するのは TB2 側の profinite root normalization で
ある。これを既存 TB4-3/A3 framework と合わせた TB4-B が、seal-relative
な exact \(\varepsilon=1\) を与えるのであって、seal 単独が A3 を証明する
のではない。Rule-side object との
\((Z_{2M}\text{-link})\) は **window ごとの migration edge** を要し、現時点
で供給済みなのは K5 の \(Z_{20}\)-link だけである。

ところが \(B_{\rm FC}\) v2.12 の live 本文は、

- §8 / §8.1: 「(TB4) と \((Z_{2M}\text{-link})\) は seal の採用手続きが供給」;
- §12.1 code block: `Z_{2M}-link ... adopted via Z-norm-seal/v1`;
- §12.1 文献要請 13: 「\(\varepsilon=1\)（および \(t_{2M}=1\)）は
  `Z-norm-seal/v1` が固定」;

と、一般の \(M\) について書く。一方、同じ文書の §13.1 は
\((Z_{2M}\text{-link})\) をなお **未凍結**とし、§8・§13.1 の前件表は
B-6/B-7 の現行 proof が link を必要とする、と正しく書く。これは単なる
札の言い換えでなく、同一文書内の前件供給状態の矛盾である。

さらに §2 には

> だから (TB4) は文献関所のままである

が live のまま残り、その直後では exact \(\varepsilon=1\) を seal の採用
手続きに置く。申告された「関所 8 箇所すべて同期」も再現しない。

従って便 60 F5 payload 項 5 は未達であり、payload 全体を原子的に発効
させられない。

### 必須修理 A61-1

\(B_{\rm FC}\) v2.13 等の新 version で、live status を次の型へ統一すること。

```text
global:
    Z-norm-seal/v1 + the retained TB4-3/A3 framework
        -> exact TB4 / epsilon = 1
        -> root-normalization-relative theorem

per window:
    Z_{2M}-link
        supplied iff inventory(window) = migrated
        and the receipt binds its migration record digest

current specialization:
    K5  -> TB4 + Z20-link supplied
    K3  -> TB4 supplied; Z12-link pending
    A5  -> TB4 supplied; Z10-link pending

general B-6/B-7 current proof:
    relative to Z-norm-seal/v1
    AND the named per-window Z_{2M}-link
```

TB4-E alternate / link-free な**別 proof ID**があるなら、現行 proof と同じ
行へ融合せず別に置くこと。§0、§2、§8、§8.1、§9、§12.1、§13.1、§15
の live status を一括 lint し、履歴表の引用と現行規範を区別する必要がある。

---

## F5. blocker A-2 — component の自己 SHA 記入指示

component 1 §7 と component 2 §6 は共に

```text
artifact_sha256 = ______   # 司令塔が本ファイル確定後に記入
```

とする。しかし F2 の SHA-256 は、この欄が空の byte 列に対する hash で
ある。そこへ当該 hash を書けば file bytes が変わり、記入値は直ちに
自分自身の hash でなくなる。これは final seal で正しく避けた自己参照を
component 側へ戻している。

### 必須修理 A61-2

component 内へ自己 digest を書かない。例えば欄を

```text
artifact_sha256_authority = external final seal + event receipt
do_not_write_self_digest_into_this_artifact = true
```

相当へ変更し、component の状態も

```text
immutable candidate blob;
operative iff bound by the approved event receipt
```

と外部状態へ分離すること。修文すれば component 1 \(\to\) component 2
\(\to\) final seal の digest はすべて変わるので、この順に再 hash し、
同期先も含む新 candidate C を再提出する。

final seal の `status_on_apply` / `applied_at` / あらかじめ mint した
`event_receipt_id` だけを許可された差分として埋め、その後の C digest を
R が束縛する二段方式そのものは可である。

---

## F6. Part A の発効裁定

```text
component mathematical content       = PASS
final-seal inventory/scope            = PASS
TB4 v2.5 / Rule1 v1.5 / manifest v1.7 = PASS
BFC v2.12 synchronization             = FAIL
component self-digest protocol         = FAIL
atomic apply                           = NOT ACCEPTED
effect declaration                     = NOT ISSUED
new theorem gate                       = not required; apply delta gate required
```

従って現候補 hash `022e6e2e...` を operative seal hash としてはならず、
`status_on_apply` を記入せず、receipt R と CLAIMS の二区分記帳も発行
しない。便 60 の「修理後の小版イベントを進めてよい」という原理的認可は
撤回しないが、**今回の transaction がその修理条件を満たしたとは判定
しない**。

---

# Part B — \(N_\infty\) stage-2 spec v3

## F7. 数学核の紙上監査

### F7.1 `N∞-N` — 内容 PASS、norm の型を一語修理

\[
H_v=(v-\mu)(v-\mu^\iota)=v^2-2va+C
\]

および

\[
\operatorname{div}_{\mathbb P^1_x}(H_v)
=\pi_*\operatorname{div}_{C_{\rm crv}}(v-\mu)
=\pi_*[\mu^{-1}(v)]-5[\infty_x]
\]

は正しい。従って
\((H_v)_0=\pi_*[\mu^{-1}(v)]\) も正しい。

ただし §1.2 step 2 の

```text
N_pi : pi_* O_C^times -> O_P1^times
```

を、零・極を持つ \(v-\mu\) にそのまま適用する書き方は sheaf-unit と
rational function の型が混ざる。freeze proof では

\[
N_{k(C_{\rm crv})/k(x)}:
k(C_{\rm crv})^\times\longrightarrow k(x)^\times
\]

と書き、各 closed point \(P\) で

\[
\operatorname{ord}_P N(g)
=\sum_{Q\mid P}[\kappa(Q):\kappa(P)]\operatorname{ord}_Q(g)
\]

を一行置けば完全に自己完結する。この valuation identity があれば外部
文献の §/定理番号を freeze の前件にする必要はない。標準事実を引用だけで
済ませるなら出典照合は必要だが、本件では上の一行を証明 artifact にする
方が小さい。

### F7.2 `N∞-1:1` — PASS

\(Q\in\mu^{-1}(v)\) に対し
\(\mu^\iota(Q)=C/v\) なので

\[
\iota Q\in\mu^{-1}(v)\iff v^2=C.
\]

\(v^2\ne C\) なら fiber に Weierstrass point はなく、\(\pi\) はそこで
unramified。さらに

\[
(v-\mu^\iota)(Q)=\frac{v^2-C}{v}\ne0
\]

だから norm の他因子は単元であり、(60.4) の局所 multiplicity 一致が
従う。v2 の欠落は閉じた。

### F7.3 `N∞-pair` — PASS、target 非依存

\(\bar{\mathbb Q}\) 上で \(s^2=-C\) を選ぶだけで

\[
H_s=-2sa,\qquad H_{-s}=2sa.
\]

\(a(x_0)=0\) なら
\(p(x_0)^2f_6(x_0)=-C=s^2\ne0\) なので、\(p\)-locus と Weierstrass
locus を自動的に避ける。従って

\[
\operatorname{part}\mu^{-1}(s)
=\operatorname{part}\mu^{-1}(-s)
=\operatorname{rootpart}(a)
\]

である。この証明は S5 の target branch condition、`N∞-swap`、branch
polynomial の計算を一切使わない。

### F7.4 `N∞-swap` と依存方向 — PASS、ただし graph の説明を精密化

\(\mu\circ\iota=j\circ\mu\) から branch set の \(j\)-stability を導く
追記は正しい。fixed 二 fiber の双方を \([2,2,1]\) にするには、\(\deg p=2\)
の唯一の double root を二つの異なる値に使う必要が生じるので fixed case
は排除され、\(s^2=-C\) が従う。

`N∞-pair` と `N∞-swap` は互いを使わず、循環は無い。ただし現 (60.6) の
右辺は既に `for some s^2=-C` を含むため、**表示された iff の右から左を
証明するだけなら `N∞-swap` は論理的に冗長**である。正確な dependency は

```text
N∞-pair + RH  -> rootpart から (60.6) 右辺
S5 target(E-7 + two [2,2,1] fibers) + N∞-swap -> (60.6) 右辺
```

である。現定理は正しいままだが、freeze dependency 表では
`N∞-swap` を「S5 target を (60.6) の RHS へ入れる bridge」と呼ぶか、
RHS から \(s^2=-C\) を外して結論として出すかのどちらかに統一するとよい。

### F7.5 `N∞-div` / T-2 — PASS

Pell を微分して \(p\mid a'\)。T-1 通過時、
\(d=\operatorname{monic}\gcd(a,a')\) は degree 2 squarefree で
\(\gcd(p,d)=1\) だから、次数比較により

\[
a'\doteq p\,d,\qquad a'/p\doteq d
\]

が従う。T-2 は (60.5) を正しく逐語化している。

### F7.6 `N∞-criterion` の十分方向 — PASS

議論は \(\bar{\mathbb Q}\) へ base change して行えばよい。標数 0 なので
\(\mu\) は separable、\(\deg\mu=5\)、\(g(C_{\rm crv})=2\) であり、

\[
\deg R_\mu=2g(C)-2+2\deg\mu=12.
\]

divisor orientation から \(0,\infty\) の二点上で contribution は
\(4+4\)。`N∞-pair` と \(\operatorname{rootpart}(a)=[2,2,1]\) から、
互いに異なる \(s,-s\) の各 fiber の contribution は \(2+2\)。
従って既知の四 fiber だけで

\[
4+4+2+2=12
\]

を使い切る。幾何点ごとの different coefficient \(e_Q-1\) は非負なので、
\(\bar{\mathbb Q}\) にのみ定義される点を含め、他の ramification point は
存在できない。従って branch set はちょうど
\(\{0,s,-s,\infty\}\)。この RH 段に不足は無い。

以上より **P60-B1〜B4 の数学修理と新しい criterion の核は PASS** で
ある。これは紙上監査であって Lean `verified` ではない。

---

## F8. predicate・blindness 差分で通った部分

次を PASS とする。

1. E-1〜E-6 を raw precondition、E-7 を target condition に分けたこと。
2. T-1 通過後の T-2〜T-8 不一致をすべて `INTEGRITY_STOP` にしたこと。
3. decision lane と local-differential / saturated-elimination の audit
   lanes を分離したこと。
4. resultant while 全除去の禁止と、checker の baseline/saturation proof
   ID 要求。
5. candidate-dependent fibers、branch values、divisor、unkeyed digest を
   `SEALED_INTERNAL` へ移したこと。
6. public envelope の「五欄」を、identity/verdict/reason を除く
   **数学的射影五欄**と精密化したこと。
7. typed random ref、EP extension、negative runner \(\ne\) clean HMAC
   steward、tainted actor の steward 禁止。
8. S5-1 / S5-2 / S5-2a / S5-3∞ の行別 provenance 修理。
9. \(K=\mathbb Q(\zeta_{20})\) なら
   \(i=\zeta_{20}^5\)、\(-1=i^2\) なので
   \([s^2]=[C]\in K^\times/K^{\times2}\) となる型修理。

ただし 5、9 は**記述上の方向が正しくなった**という PASS であり、次節の
freeze schema への実束縛はまだ閉じていない。

---

## F9. blocker B-1 — D-2 は選択されたが、まだ certificate schema ではない

裁定 72 が D-2 を選んだことは承知した。しかし対象 blob 自身はなお

```text
freeze 時に D-1 / D-2 のどちらかを選ぶ
司令塔裁定待ち
```

と書き、D-2 の本体は

> 差の divisor が 0 であることの exact な証明書

という一文だけである。これは目標命題の言い直しであって、生成物・witness・
検証規則・失敗状態を定める schema ではない。§4.3 でも
`divisor_equality_cert_schema_id` に **digest が無く**、具体 ID も無い。

また「D-1 は canonicalizer が第三実装となり、必ず共通 bug 経路になる」
という比較は強すぎる。D-1 でも二 lane が仕様だけを共有して canonicalizer
を独立実装すれば、単一 shared implementation にはならない。逆に D-2 でも
一つの certificate generator/verifier を両 lane が oracle として信じれば、
それが共通 bug 経路になる。従って D-2 の採用自体には反対しないが、
**D-2 は名前だけで D-1 より独立なのではない**。

### D-2 を承認できる最小 schema

少なくとも次を versioned artifact と full digest で凍結すること。

```text
divisor_equality_certificate = {
  schema_id, schema_digest,
  predicate_freeze_id,
  candidate_ref,
  curve_base_field_id, curve_model_digest, chart_ids,

  searcher_native_divisor_ref, searcher_native_artifact_digest,
  checker_native_divisor_ref,  checker_native_artifact_digest,

  component_bijection,
  exact_point_equality_witnesses,
  multiplicity_equalities,
  chart_overlap_witnesses,
  total_coverage_and_no_extra_component_witness,
  pushforward_compatibility_witness,

  verifier_contract_id, verifier_contract_digest
}
```

presentation が違う algebraic point を対応させる witness は、固定 ambient
coordinate ring 上の相互 ideal inclusion / Bézout・reduction certificate
等、**exact に再検査できる形**にする。単なる digest 一致、最終 partition
一致、degree 一致は divisor equality certificate ではない。

certificate generator は第三の**判定 lane**に数えず、ACCEPT を単独で
出せない。両 native output を受け取って witness を作るだけとし、欠落・
検証失敗・入力 digest 不一致はすべて
`INTEGRITY_STOP / divisor-equality-failure` とする。少なくとも searcher
側と checker 側が独立 verifier で同じ certificate を検査するか、同等の
二実装検査を要求する。shared canonicalizer/helper の再導入は禁止する。

---

## F10. blocker B-2 — sealed payload が二経路の native output を保存しない

§3.2/T-8 は「searcher と checker が独立に作った partition を比較」と
正しく書く。しかし §5.2 の実 schema は

```text
finite_aggregate_partitions
ramification_divisor_on_C
branch_divisor_on_P1
```

を各一個しか持たない。`[[2,2,1],[2,2,1]]` は**二 fiber**を表すだけで、
**二 lane**を表さない。D-2 certificate 自体の保存欄も無い。このままでは
比較前に一方を共通 object へ潰してしまい、独立再構成の証拠を receipt に
残せない。

### 必須修理 B61-2

`SEALED_INTERNAL` に少なくとも

```text
searcher_native = {
  ramification_divisor_on_C,
  branch_divisor_on_P1,
  finite_aggregate_partitions
}
checker_native = {
  ramification_divisor_on_C,
  branch_divisor_on_P1,
  finite_aggregate_partitions
}
divisor_equality_certificate
partition_equality_result
```

を別々に保存し、各 native artifact digest と D-2 witness を相互束縛する。
片側を他側の parser/canonicalizer で先に変換してから保存してはならない。

---

## F11. blocker B-3 — verdict/reason schema が total でない

public envelope は全 verdict に単数の `reason_code` を要求するが、閉じた enum
には ACCEPT 用 code が無い。従って現 schema では **正の certificate を
一件も型付けできない**。

また T-1 failure では、例えば triple root があると
`triple-root-of-a` と `a-partition-mismatch` が同時に成り得る。precondition
も複数同時 failure の優先順位が無いので、verdict は一意になっても単数
reason は一意にならない。

さらに E-6 は E-4 の Pell identity と \(C\ne0\) から自動である。従って
**E-4 を exact に PASS した後の \(\gcd(a,p)\ne1\)** は candidate REJECT
でなく、定理または実装の矛盾として `INTEGRITY_STOP` にすべきである。

### 必須修理 B61-3

例えば次の total order を凍結する。

```text
ACCEPT:
    reason_code = accepted

T-1 fail:
    if gcd(a,a',a'') has positive degree
       or gcd(a,a') is not squarefree:
           REJECT / triple-root-of-a
    else:
           REJECT / a-partition-mismatch

E-4 exact pass but E-6 fail:
    INTEGRITY_STOP / pell-implies-coprime-mismatch
```

他の複数 precondition failure も、固定 priority または canonical に整列した
`reason_codes[]` のどちらかを選ぶ。単数欄のままなら priority が必須である。

`branch-pair-not-harmonic`、extra branch、finite branch count/partition の
不一致を T-1 後の `INTEGRITY_STOP` へ移した裁定そのものは正しい。

---

## F12. blocker B-4 — 二層 freeze bundle と B9 の束縛が未完成

§4.3 は ID 名の placeholder に留まり、D-2 schema digest が無い。さらに
P60-B9 は \(K\)、squareclass quotient、\(-1\) square proof、
S5-4∞ dependency を **freeze bundle に束縛**する要求だったが、§4.3 の
bundle にはこれら四欄が無い。§7 に記述しただけでは B9 は閉じない。

freeze bundle には少なくとも次を追加すること。

```text
campaign_window_id = K5
curve_coefficient_base_field_id = Q
prediction_base_field_id = Q(zeta_20)
squareclass_quotient_schema_id + digest
minus_one_square_proof_id + digest
s5_4_infinity_dependency_id + digest

divisor_equality_cert_schema_id + digest
public_certificate_schema_id + digest
sealed_certificate_schema_id + digest
reason_code_enum_id + digest
predicate_theorem_id + digest
```

`predicate_theorem_id + dependency 4 lemmas` という省略も freeze 文としては
使わず、`N∞-N` / `N∞-1:1` / `N∞-fix` / `N∞-pair` / `N∞-swap` /
`N∞-div` / `N∞-criterion` の実 ID・digest を依存閉包として列挙すること。

### §12 問 6 への回答

今回の campaign は K5 window なので、
\(K=\mathbb Q(\zeta_{20})\) を **固定したまま**にするのが fail-closed で
ある。candidate が prediction field を入力で選べる設計にしてはならない。
代わりに `campaign_window_id=K5` を同じ bundle に明記する。

再利用性が欲しいなら、

1. \(\mathbb Q\)（または明記した標数 0 体）上の数学 theorem artifact;
2. K5 固有の blindness/whitelist envelope

を別 ID にする。将来 K3/A5 へ移す際は 2. を新 version で差し替え、同じ
freeze ID を使い回さない。

---

## F13. Part B の freeze 裁定

v3 は P60-B1〜B5、B7、B8 の大部分を閉じ、数学 predicate の核は freeze
候補に達した。しかし P60-B6 と B9、および certificate の totality は
まだ実 schema になっていない。

```text
predicate mathematics              = PASS (paper audit)
decision/audit lane principle       = PASS
public/sealed direction             = PASS
D-2 selection                       = ACKNOWLEDGED
D-2 frozen schema                   = MISSING
two native lane payloads            = MISSING
total verdict/reason schema         = MISSING
B9 fields in freeze bundle          = MISSING

predicate_spec_freeze_id            = NOT ISSUED
implementation_status               = NOT AUTHORIZED
model_builder status                = LOCKED
```

再提出では旧二 digest

```text
supersedes_draft
  = sha256:77ed7131b147a777ab38dfc2c5b46db4a160e3735681e5089531a57b4a0181f2
audited_predecessor_rejected
  = sha256:813e7fdd9e7b3b907333d7cc2ba03b188d3ef7ee61267d9dd77cfacfe5ff74b4
```

に加え、本 v3 digest

```text
sha256:83c9f58887a508d2bbe451a456e41e6ff19f5b2eaa6fdfb957516f6a57aede3b
```

を `audited_predecessor_not_frozen` 等の正確な身分で系譜に残すこと。
数学層は再証明不要で、F9〜F12 の schema 差分を主対象にすればよい。

---

## F14. 共同設計者としての発案

### F14.1 theorem freeze と execution freeze を分ける

今回の状態は「定理が未完成」ではなく「実行 certificate が未型付け」で
ある。次の二 ID に分けると再監査面が小さくなる。

```text
ninfty-stage2-theorem/v1
    N∞-N / 1:1 / fix / pair / swap / div / criterion

ninfty-stage2-execution-schema/v1
    lane separation / D-2 / sealed-public / reason enum / K5 whitelist
```

前者の紙上 PASS を記録しても、後者が閉じるまで実装認可は出ない。この
分離なら D-2 schema の差分で数学 theorem digest を動かさずに済む。

### F14.2 D-2 は「第三の答え」でなく「二つの答えの proof-carrying join」

D-2 artifact を第三計算結果にすると三者多数決へ逸れる。役割は

```text
(native A, native B)
    -> exact equality witness
    -> two independent witness checks
```

だけに限定する。A/B のどちらかを正本として他方を変換する設計も避ける。
これで「第三 oracle」の共通 bug を最小化できる。

### F14.3 stage-2 certificate に lifecycle state を追加する

実行中の partial output を public envelope と誤認しないよう、

```text
certificate_state =
    BUILDING | SEALED_COMPLETE | PUBLIC_PROJECTED | QUARANTINED
```

を closed enum とし、`PUBLIC_PROJECTED` は両 audit lane と D-2 の完了後に
だけ許すとよい。未知 state・順序飛ばしは fail-closed とする。

---

## F15. ★教材

1. **profinite root system と各窓の Rule-root identity は別の edge である。**  
   seal-relative な TB4-B で全称 \(\varepsilon=1\) が立っても、K5 の
   migration record から
   K3/A5 の \(Z_{2M}\)-link は生えない。

2. **自分の SHA を自分の byte 列へ後書きしてはならない。**  
   component digest は親 seal または receipt が外から束縛する。

3. **RH の「使い切り」は geometric point 上で行う。**  
   char \(0\) で全 different coefficient が非負だから、既知 contribution
   が total degree に達すれば \(\bar{\mathbb Q}\) 上の隠れた分岐も無い。

4. **第三 certificate は第三 oracle ではない。**  
   二 native output を保存したまま、その等式だけを proof-carrying に
   接合する。

5. **verdict が一意でも reason が一意とは限らない。**  
   singular `reason_code` には ACCEPT code と failure priority が要る。

6. **field を本文に書くことと freeze bundle に型付けることは別である。**  
   leakage edge の基礎体は campaign window と同時に digest 束縛する。

---

## F16. 監査範囲外申告

### 本便で行ったこと

- 委嘱、対話帳、裁定 72、対象 8 artifacts、便 60 最終返信を全文読解;
- target commit / HEAD / worktree の blob 同一性、SHA-256、LF 行数、
  CR/TAB/C0 を照合;
- component 1/2/final seal の数学・typed edge・inventory・hash 順序を監査;
- TB4 v2.5、Rule 1 v1.5、manifest v1.7、\(B_{\rm FC}\) v2.12 の旧版差分を監査;
- `N∞-N`、`N∞-1:1`、`N∞-pair`、`N∞-swap`、`N∞-div`、
  `N∞-criterion` を紙上再導出;
- decision/audit lane、D-2、public/sealed、reason enum、whitelist/freeze
  bundle を型監査。

### 本便で行っていないこと

- Part A は差戻しなので status 記入、operative hash、receipt、CLAIMS
  適用後の blob は存在せず、監査していない;
- sealed 8 tuples の raw coefficient、旧 exact arithmetic、HMAC key/
  mapping は見ておらず、8 件を `cross-checked` に昇格していない;
- EP は未提示であり positive end-to-end calibration は未監査;
- searcher/checker/D-2 verifier は未実装なので、コード独立性・実 output
  は未監査;
- GAP、Lean、外部文献は使用していない。本便の新数学裁定は paper audit
  であり、Lean `verified` ではない。
