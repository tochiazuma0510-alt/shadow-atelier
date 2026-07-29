# interp 追補 (o) v4 — RouteResult schema 正本化(Sol 便84 F84-5.4/P84-5 処方)

状態: interpretation / candidate(v3/v3.1 を置換)。合成器名は evidence-union/fail-closed-v2
(P81-E)のまま不変 — 本追補が改めるのは RouteResult **オブジェクトそのものの schema**(nominal
gate)であり、`compose_route_statuses` の 4 規則(N83-2.1、便83 で Sol 確認済み PASS)は不変。

## 経緯(v3.1 → v4)

追補(o) v3.1(`cert_shape_interpretation_addendum_o_v3.md`)は route blob の**内容**(claim_digest・
evidence_digest・coverage 束縛)を規定したが、「この blob は本当に signed/dispatch-fixed な
RouteResult なのか」という**入れ物そのものの正当性**を規定していなかった。便84
(`sol/sol_reply_84_math11.md` F84-5.4)の直接 probe で、実装 `coerce_to_route_result` が
`route_status` と status 別欄しか見ておらず、**`schema_id` と `route_id` を一切検査していない**
ことが判明した:

- `{schema_id 欠落, route_id 欠落, route_status:"PASS", ...}` → PASS(本来 MALFORMED であるべき)。
- `{schema_id:"evil/v9", route_id:"producer-choice", ...}` → PASS。
- 上記二本の union → overall PASS(本来 INTEGRITY_STOP)。
- `route_result_pass("producer-choice", ...)` 自体も任意の非空文字列を route_id として受理。
- combinator の第一引数/第二引数がそれぞれ `route_id="R1"`/`"R2"` であることも未検査。

「dispatch(どの constructor/どの引数 slot が呼ばれたか)が route_id/status を固定し、producer は
分岐不能」という N83-2.3 の核心を、nominal gate の欠落が事実上無効化していた。

## RouteResult schema(正本、v4)

RouteResult は以下の**厳密な** JSON shape を持つ。`schema_id`/`route_id`/`route_status` の 3 欄を
**header** と呼び、全 RouteResult に必須。

```json
{
  "schema_id": "mb/ninfty-evidence-union/route-result/v1",
  "route_id": "R1" | "R2",
  "route_status": "PASS" | "FAIL" | "ABSENT" | "MALFORMED",
  "...status 別必須欄(下記)..."
}
```

### header(全 status 共通・必須)

1. **`schema_id`**: 文字列定数 `"mb/ninfty-evidence-union/route-result/v1"` に**厳密一致**。
   欠落・別値(`"evil/v9"` 等)は MALFORMED。
2. **`route_id`**: `"R1"`(recomputation route)または `"R2"`(witness-coverage route)の
   **列挙値のみ**。producer が自由に選べる文字列ではない — **dispatch-fixed**(constructor 呼び出し
   自体が route_id を固定する。`route_result_pass("producer-choice", ...)` はコンストラクタ自体が
   拒否し MALFORMED へ fallback する)。
3. **`route_status`**: `PASS`/`FAIL`/`ABSENT`/`MALFORMED` の列挙値のみ。

### slot 束縛(combinator の義務)

`evidence_union_fail_closed_v2(route1, route2)` の**第一引数は `route_id="R1"` を、第二引数は
`route_id="R2"` を持つことを要求する**。route_id が正しい列挙値であっても、slot と一致しなければ
MALFORMED(「well-formed だが違う slot に置かれた」ことは黙って許容しない)。`None`(route が
genuinely 存在しない)は slot 検査の対象外 — ABSENT に短絡する。

### status 別 shape(v3.1 から不変、header 3 欄の下に additional)

- **PASS**: `claim_digest`・`evidence_digest`・`claim_source_ref`・`evidence_refs`(共通)
  + `expected_domain_count`・`checked_domain_count`・`expected_domain_digest`・`coverage_digest`
  (PASS 専用。count は等しく、expected digest と coverage digest も等しいことをコンストラクタ自身が
  検査する、F83-2.1 不変)。
- **FAIL**: 共通 4 欄 + `counterexample_loci`(非空配列)・`expected_witness`・`observed_witness`。
- **ABSENT**: `missing_mask`(受領側導出、必須・非 None)。
- **MALFORMED**: `schema_errors`(非空配列)。

### 未知/外来欄の拒否(F84-5.4 item 4)

上記 header 3 欄 + 現在の `route_status` に対応する shape 欄**以外**のいかなる欄も存在してはならない
— 存在すれば MALFORMED。これは v3.1 時代の「他 status の shape 欄が併存したら MALFORMED」という
co-presence 検査(F83-2.2)を**包含**し、さらに全く未知の欄名(`evil_extra_field` 等)も同じ扱いで
拒否する。

### route-specific verifier の義務(F84-5.4 item 5)

route-specific verifier(例: `route_from_verifier_b_w6`)は、**raw evidence(生の判定結果・detail）
から** `claim_source_ref`/`evidence_refs` を作り、digest を**都度再計算**しなければならない。
constructor のデフォルト `None` のまま放置してはならない — armature 段階であっても、raw evidence
への参照は必ず populate する。

### public combinator の義務(F84-5.4 item 6)

`evidence_union_fail_closed_v2` は本モジュールが公開する**唯一の**合成エントリポイントであり、
CLI(`main()`、raw producer JSON を読む経路)も in-process 呼び出しも**同一の**関数を経由し、常に
`coerce_to_route_result`(上記 header/slot/未知欄検査込み)を通す。「raw producer JSON を
RouteResult として直接受ける」経路は存在しない — 手作りの JSON であっても、schema_id/route_id/
shape の全検査を、constructor が作った RouteResult と全く同じ基準でくぐらなければ PASS/FAIL/ABSENT
のいずれにも到達しない。

## 合成の全域関数(v3.1 から不変)

`compose_route_statuses` の 4 規則(MALFORMED→INTEGRITY_STOP、非 ABSENT 二本の claim_digest 不一致
→CONFLICT、PASS/FAIL 混在→CONFLICT、それ以外は FAIL>PASS>ABSENT の優先)は**不変**。本追補が改めた
のは、この関数に status/digest が渡る**手前**の nominal gate のみである。

## v3.1 → v4 差分まとめ

| 項目 | v3.1 | v4 |
|---|---|---|
| `schema_id` 検査 | なし | **厳密一致必須** |
| `route_id` 列挙 | producer が任意の非空文字列を選べた | **`{"R1","R2"}` のみ、constructor でも拒否** |
| slot 束縛 | 未検査 | **第一引数=R1・第二引数=R2 を必須化** |
| 未知欄 | 他 status の shape 欄併存のみ検査 | **未知欄すべてを拒否**(co-presence 検査を包含) |
| route-specific verifier の ref | `None` のまま許容 | **raw evidence から populate 必須** |
| 公開エントリポイント | 複数経路が黙って RouteResult を信頼しうる余地 | **単一エントリポイント、常に coerce 経由** |

## 状態

Sol 便84 F84-5.4/P84-5 の是正として起草。実装(`search/ninfty-evidence-union.py`)・テスト
(`search/test_ninfty_evidence_union.py`、Sol の literal probe 全てを負例化し返却 status まで assert)
のフル再走で確認 — 数値は司令塔の検分・便85 への同梱時に機械出力のまま記載する。v2/v3(=v3.1)は
既存ファイルのまま非上書き(`cert_shape_interpretation_addendum_o_v3.md` 等に履歴として残す)。
