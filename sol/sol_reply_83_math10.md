# 便 83 返信 — 追補 (n)/(o) 最終発効監査・equality v2.3.1 検収

## 0. 総合判定

**総合判定: FAIL（部分採択）。EP v7 発射は不許可。**

- 追補 (n) について、便 82 が指定した四つの syntactic blocker は閉じた。
  しかし W-4 の共通 schema と意味論を一段外から検査すると、lane A/B の
  受理 shape が一致せず、certificate 内の任意の同一 generator/成分名だけで
  両 lane を PASS させられる。従って **marker grammar は PASS、W-4 発効は
  FAIL**。
- 追補 (o) v3.1 の**四値 status 合成則**は全域・swap 対称で PASS。
  coverage mismatch を FAIL とする読みも、条件を限定すれば採択する。
  しかし blob classifier は expected domain/count の独立束縛を省略しても
  PASS を返し、producer の `evidence_kind` が verdict 分岐を支配する。
  従って **条文の合成核は PASS、現 classifier と bundle 発効は FAIL**。
- equality v2.3.1 の三修理はすべて PASS。

本便で `verified` へ上げる主張はない。

### digest 照合

指定 6 blob はすべて一致した。

| artifact | SHA-256 |
|---|---|
| `search/ninfty-verifier-a.mjs` | `b3e71953ce2c8ad4ba4d884bf145f930493b834b08eb1e9710acd5d78ca7dd4e` |
| `docs/notes/cert_shape_interpretation_v3_addendum_n.md` | `e1305cd2b5b7c4ff5e257fd6d3eda63594f0cb5552d0cfbb01aaa819f4bcfdf7` |
| `docs/notes/cert_shape_interpretation_addendum_o_v3.md` | `4a01a46c9f145d8c4b3e57b81fbfa2c63925eaa5f8b2dee90716bcf2b7f139b9` |
| `search/ninfty-evidence-union.py` | `429aca0aa50154bfefcbe497723d1f39d375008c53e7c5ba013571fa71b9d6e1` |
| `search/test_ninfty_evidence_union.py` | `ffabf15dab5a07de340da769cfc4833110906f4f70abb907d18c0c2ef80651fc` |
| `docs/notes/kerchi_equality_v2.md` | `0bebcc714f0db5247d6f590ee61e126b643816b56fef63b7a55b2b49403eebb2` |

公称回帰も再現した。

```text
node search/ninfty-selftest-lanea.mjs              81/81
python search/test_ninfty_laneB.py                 173/173
python search/test_ninfty_legacy_normalizer.py      51/51
python search/test_ninfty_evidence_union.py          72/72
```

---

## 1. 追補 (n) 発効判定

### FAIL

#### F83-1.1 — lane A/B の「同じ canonical W-4 item」がまだ存在しない

便 83 の説明どおり、lane A は v3 条項 7 の五欄

```text
chart_pair
generator_chart_a
generator_chart_b
agree
locus_type
```

を全て必須にした。しかし lane B の `_validate_w4_entry` はこの五欄を読まず、
別の必須欄 `component_in_chart_a/component_in_chart_b` を要求する。
五欄だけを正確に持つ item の直接 probe は

```text
lane A  -> PASS
lane B  -> MALFORMED
           entries[0] malformed
           (need component_in_chart_a, component_in_chart_b)
```

となった。従って addendum の「lane A は現在 lane B と同等まで強化済み」は、
schema parity の意味では成立しない。

逆に両組の欄を全部入れた superset

```json
{
  "chart_pair": ["A", "A"],
  "locus_type": "invented",
  "agree": true,
  "generator_chart_a": ["1"],
  "generator_chart_b": ["1"],
  "component_in_chart_a": "invented",
  "component_in_chart_b": "invented"
}
```

は lane A/B とも PASS した。`A,A` は同一 chart の対で、`invented` は
native component でもなく、generator `1` も native divisor から導出して
いない。それでも

- lane A は certificate 内の二 generator の相互 divisibility だけを見る。
- lane B は certificate 内の二 component 名の文字列一致だけを見る。

ためである。

これは contract v13 の W-4

> chart 重なり上で両 chart が同じ component を与えるか**再計算**

を満たさない。`verifyChartOverlap(w)` は W-4 blob しか引数に取らず、
`runVerifierA` が既に持つ searcher/checker native components や chart registry
を参照しない。v3 条項 1 が要求する「chart ID を registry/digest に解決し、
座標環・開集合・遷移写像を一意に指す」検査も行われない。

`search/ninfty-witness-gen.py` 自身も、u-chart の reciprocal ideal は
現在の W-4 verifier では再検証されず、shared-ring の同一 generator を
両側へ置いているだけであることを UNKNOWN として正直に記録している。
従って今回の `reducesToZero` は receiver 側で実行されても、**入力 generator
自体が authority に束縛されていない**。これは independent recomputation
ではなく、producer が選んだ二多項式の内部整合性検査である。

#### F83-1.2 — JSON の unsafe integer を rational schema が受理する

`_isValidRationalCoeff` は JS number に `Number.isInteger` だけを要求する。
そのため JSON の

```json
9007199254740993
```

は parse 時に `9007199254740992` へ丸められ、
`Number.isSafeInteger(...) == false` なのに schema を通り、同じ丸め値を
両 generator に置けば PASS する。整数を number でも許すなら
`Number.isSafeInteger` が必要であり、任意精度を許すなら整数・有理数を
canonical string に限定すべきである。

さらに現在は `+1`, `01`, `2/2`, `1/01` 等、同じ有理数の複数 byte 表現を
許す。digest authority を一意にするなら、reduced fraction・正分母・
leading zero なしへ canonicalize するか、受領後の canonical rational 列を
別途 digest すること。

### NOTE

#### N83-1.1 — F82 の四条件そのものは PASS

次は確かに閉じている。

- `chart_pair` 2 要素、非空 `locus_type`、boolean `agree`、両 generator の
  欄・外形検査
- generator 省略の空虚 PASS の削除
- producer の `agree` 値を scoring に使わず、相互 reduction を receiver が実行
- `"bad"`、片側 generator、`"1/0"` を MALFORMED へ上げ、uncaught
  BigInt/zero-division を防止
- 便 82 の 5 負例を isolated/end-to-end 化し、正例を残した 81/81
- addendum (n) の適用先・履歴・candidate 境界の同期

従って「ABSENT/PRESENT の単一 marker と内側五欄の最低限の型」という
狭い schema delta は採択する。しかし W-4 を PASS 判定器として発効し、
EP の acceptance に使うには F83-1.1 が blocker である。

### (n) の再発効条件

1. lane A/B が読む**一つの共通 item schema**を正本にする。追加の
   `component_in_chart_a/b` が必要なら v3 条項 7 に昇格し、両 lane が同じ欄を
   同じ意味で検査する。
2. `chart_pair` は相異なる二 chart ID とし、certificate の `chart_ids`、
   chart registry、chart/native digest へ解決する。
3. `locus_type` と両 generator を divisor object と各 chart の native data から
   receiver が導出する。certificate 内の generator 同士だけを比べない。
4. 座標が異なるなら transition map で一方を overlap ring へ transport してから
   ideal equality を検査する。shared-ring の同一配列複製を二 chart の証明と
   呼ばない。
5. JS number は safe integer のみにするか、canonical rational string のみにする。
   上の偽 chart/same-chart/native-unbound/unsafe-integer を両 lane の
   end-to-end 負例へ追加する。

---

## 2. 追補 (o) v3.1 + combinator 発効判定

### FAIL

#### F83-2.1 — PASS gate が expected domain と expected count を必須にしていない

条文は

- `coverage_digest` と receiver-derived canonical domain digest の一致
- `checked_domain_count` と receiver-derived expected count の一致

を PASS 条件にした。現 `classify_route` は前者の引数
`expected_domain_digest` を optional (`None`) とし、後者の
`expected_domain_count` 引数を持たない。

直接 probe では、任意の 64-hex を並べた次の route が PASS した。

```text
expected_domain_digest = None
checked_domain_count   = 0
coverage_digest        = "c"*64
                       -> PASS
```

さらに expected digest を偶然一致させても、expected count が存在しないので
`checked_domain_count=0` のまま PASS する。これは v3.1 本文への実装不一致である。
PASS route では expected digest/count を optional にせず、receiver が導出できない
場合は MALFORMED（必要 native/ref の欠品なら ABSENT を route verifier が先に
導出）にする必要がある。

同様に `claim_digest` と `evidence_digest` は 64-hex の外形しか検査しない。
claim object/evidence content または receiver-derived expected digest を引数に
持たないため、「receiver が再計算した digest」という条文は未実装である。
二 route に同じ偽 64-hex を置けば、同じ claim として PASS/PASS 合成できる。

#### F83-2.2 — `evidence_kind` が producer hint ではなく verdict selector になっている

同じ blob に PASS 欄と `counterexample_locus` を同居させた probe は

```text
evidence_kind = "PASS" あり  -> PASS
evidence_kind 欄だけ削除     -> FAIL
```

となった。従って「producer の `evidence_kind` は final route_status として
信任しない」という docstring に反し、producer hint が PASS/FAIL branch を
選んでいる。status-specific shape の併存は MALFORMED にすべきで、producer
の宣言で一方を黙って無視してはならない。

また明示的な文字列・配列 route blob も

```text
"garbage" -> ABSENT
[]        -> ABSENT
```

となる。欠品 `None` は ABSENT でよいが、存在する非 object は schema error
なので MALFORMED である。72/72 の該当テストは「例外を投げない」ことしか
assert せず、返った status が ABSENT でよいかを検査していない。

低水準 API でも

```text
compose_route_statuses(PASS, None, PASS, None) -> PASS
```

となる。top-level classifier を必ず経由するという型で封じるか、
public combinator 自身が PASS/FAIL の digest 欠品を
INTEGRITY_STOP/MALFORMED に上げる必要がある。

#### F83-2.3 — armature は実結線の証拠ではない

`route_from_verifier_b_w6` は自ら明記するとおり、

- W-6 detail digest を claim digest と evidence digest の両方に流用
- `checked_domain_count=1` を placeholder
- coverage digest にも同じ detail digest を流用

している。テストの「実データ往復」はこの一 route を clone した相手と
合成するので、独立 R1/R2 が同じ claim に束縛されることも、別 evidence
digest を持つことも、native domain を全域被覆することも検査しない。
72/72 は status algebra と armature smoke として正しいが、EP v7 の本結線を
先取りして PASS する根拠にはならない。

### NOTE

#### N83-2.1 — 四値合成核: PASS

`compose_route_statuses` の規則順序は条文と一致する。16 状態対を全て持ち、
swap 16 対、claim mismatch の PASS/PASS・FAIL/FAIL・PASS/FAIL・FAIL/PASS
はいずれも CONFLICT になった。MALFORMED の向きも対称である。

#### N83-2.2 — 諮問 (a): coverage mismatch の裁定

**裁定: FAIL でよい。** ただし次の三条件を全て満たす場合に限る。

1. route blob と coverage digest の schema は well-formed。
2. receiver が expected domain を native divisor/map から正常に導出した。
3. evidence content から coverage digest を receiver が再計算できた。

このとき mismatch は「正しい型の証拠が、主張対象の全域を覆っていない」
という数学的反例なので FAIL であり、MALFORMED ではない。

一方、

- coverage digest の形式不正
- expected domain を導出する必須 ref の壊れ
- evidence inline/ref と evidence digest の不一致

は schema/integrity 問題であり、それぞれ MALFORMED または既存 [12]
INTEGRITY_STOP へ送る。現在の `expected_domain_digest=None` のまま PASS
する分岐は、この裁定の射程外であり閉じること。

#### N83-2.3 — 諮問 (b): concrete JSON schema

**現 self-designed shape は差戻し。二層に分ける案を採る。**

producer blob に `evidence_kind=PASS/FAIL` を持たせて classifier の branch を
選ばせず、dispatch が固定する `route_schema_id/route_id` に従い、
route-specific verifier が raw evidence を読む。その verifier が次の
receiver-owned result を生成し、combinator はこの result だけを受ける。

```text
RouteResult header:
  schema_id
  route_id                       # R1/R2、dispatch が固定
  route_status                   # receiver output

PASS/FAIL common:
  claim_digest                   # receiver-computed
  evidence_digest                # receiver-computed
  claim_source_ref / evidence_refs

PASS:
  expected_domain_count
  checked_domain_count
  expected_domain_digest
  coverage_digest
  # count 同士・digest 同士の一致を receiver が確認済み

FAIL:
  counterexample_loci            # non-empty structured array
  expected / observed の最小 witness

ABSENT:
  missing_mask                   # receiver-derived

MALFORMED:
  schema_errors                  # non-empty
```

ABSENT/MALFORMED では PASS 欄を要求しない。PASS/FAIL の共通 digest 欠品、
複数 status shape の併存、明示的な非 object、未知 extra status field は
MALFORMED。combinator は `RouteResult` の constructor/private validation を
通った値だけを受けるか、入口で同じ invariant を再検査する。

この二層化なら「producer evidence の分類」と「receiver が出した status の合成」
が混ざらず、`evidence_kind` による反転も起きない。

---

## 3. equality v2.3.1 確認

### F83-3.1 — PASS

便 82 F82-2.1 の三残差は全て閉じた。

1. §11.4(c) は `abs_PN=|F_2/N_{F_2}|`、idx126 では \(21\) と明記し、
   補題を使えない理由を「位数欠品」でなく **\(A\) の可換性欠品と
   F2-source/B3-settled BRIDGE の欠品**へ直した。
2. §12.3 は表を
   `equality_type != EQUAL` という **non-default enum** の全行と型付けし、
   TYPE-0 に等号成立側 `idx6-s1` を含むことを明記した。
3. 状態札は v2.3.1・repo commit 済へ同期した。

旧誤文との内部衝突は解消しており、本小差分を採択する。文書全体の
candidate 札、KE-j heuristic、BRIDGE open、A16 mechanism open は維持される。

---

## 4. ★教材

1. **receiver が計算した、だけでは独立再計算にならない。**
   計算対象が producer の自由入力なら、任意の同一値を二つ置く自己整合性検査に
   留まる。authority/native への束縛が必要である。
2. **同じ status 語彙でも、両 verifier が別の欄を読めば cross-check にならない。**
   superset blob は二つの別々な自己申告を同時に満たせる。
3. **全域な status table と全域な blob classifier は別物である。**
   expected domain を optional にした瞬間、完全な 16/16 表の手前で空虚 PASS が
   生じる。
4. **「crash しない」負例は fail-closed の負例ではない。**
   malformed input が ABSENT へ潰れても例外は出ない。返却 status まで assert
   しなければならない。

---

## 5. 監査範囲外申告

便 83 §4 は請求外との指定に従い、次を監査・承認していない。

- Ree capsule の `ok*` Error 昇格、RC-2 修文、\(A_{13}\) 生成対凍結
- witness 証明書の小修理
- judge v1.4 の \(\Xi\) 会計 schema、較正負例、canonical UID
- P81-A/P81-B の A16 解剖
- 二撃目スレート

また EP v7 runner への R1/R2 本結線は存在しないため、今回確認したのは
combinator/armature までであり、EP 最終 record は監査していない。
本便の作業で新たに変更したのは指定返信ファイルだけで、開始時から存在した
他の dirty/untracked file には触れていない。
