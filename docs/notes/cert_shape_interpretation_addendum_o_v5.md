# interp 追補 (o) v5 — trust-boundary 正本化(Sol 便85 F85-6.3 B85-o1..o4/P85-5 処方)

状態: interpretation / candidate(v4 は履歴として非上書き — v4 の RouteResult **nominal schema**
自体は本追補でも不変。本追補が改めるのは、そのシェイプの通った値がどこから来たかという
**trust boundary**)。合成器名は evidence-union/fail-closed-v2(P81-E)のまま不変 —
`compose_route_statuses` の 4 規則(N83-2.1、便83 で Sol 確認済み PASS)は本追補でも不変。

## ★ 教材(便85 より): schema は provenance ではない

正しい `schema_id` と field shape は誰でも書ける。origin を主張するなら、receiver-side
dispatch と raw artifact の再 hash が要る。v4 は RouteResult の**シェイプ**を強く縛ったが、
「このシェイプの値は本当に route-specific verifier が生成したものか」という**入れ物の出自**
は縛っていなかった。便85 の F85-6.3 直接 probe(`sol/sol_reply_85_math12.md` §6.3)は、
実装 `main()` が **既に組み立て済みの `{route1, route2}` RouteResult ペアを JSON からそのまま
読み、一度も route-specific verifier を呼ばずに合成器へ渡していた**ことを示した。

## B85-o1..o4: 四つの blocker と対応する修理

### B85-o1 — raw producer の self-asserted PASS が通る

**症状**: `main()` が `{route1, route2}` という**既に組み立て済みの RouteResult dict**を JSON
から読み、そのまま `evidence_union_fail_closed_v2` へ渡していた。正しい `schema_id`・`R1/R2`・
同じ偽 digest/count さえ書けば、攻撃者は route-specific verifier を一度も走らせずに PASS へ到達
できた。

**修理**: 公開エントリポイントを入れ替えた。**RouteResult を受ける公開関数はもう存在しない**。
新しい唯一の公開エントリポイントは `evidence_union_from_raw_w6(raw)`(CLI `main()` もこれを
呼ぶだけ)であり、**raw evidence artifact**
`{schema_id: "mb/ninfty-evidence-union/raw-w6-evidence/v1", certificate, native_a, native_b}`
だけを入力に取る。receiver 側の dispatch は固定 — `_build_R1(raw)`/`_build_R2(raw)` は
それぞれ内部で `_run_w6_verifier(raw)` を呼び、これが `ninfty-verifier-b.verify_W6_single`
を**自分自身で**呼ぶ。呼び出し元が「verifier は既に PASS と言った」と主張する経路は存在しない。

RouteResult の schema_id(`mb/ninfty-evidence-union/route-result/v1`)と raw evidence artifact
の schema_id(`mb/ninfty-evidence-union/raw-w6-evidence/v1`)は意図的に別文字列にした —
producer が組み立て済み RouteResult を raw evidence だと偽って新エントリポイントへ渡しても、
schema_id 不一致で `_run_w6_verifier` が MALFORMED を返す(`_validate_raw_w6_evidence`)。

### B85-o2 — provenance refs が必須でない

**症状**: `claim_source_ref`/`evidence_refs` は PASS/FAIL の allowed field だったが、
`coerce_to_route_result` は non-None・shape・参照先 digest のいずれも検査しなかった。
constructor の default `None` のままで PASS した。

**修理(二段)**:
1. **shape 必須化**: `_route_result_pass`/`_route_result_fail`(旧 `route_result_pass`/`_fail`、
   便85 で module-private に改名 — 下記 item 7)は `claim_source_ref`/`evidence_refs` を
   **必須引数**(デフォルト `None` を廃止)にし、`{"source": <非空文字列>, "digest": <64-hex>}`
   の shape を自身で検査する。`coerce_to_route_result` も同じ shape 検査を PASS/FAIL 経路へ追加
   した(non-null・構造チェック — ここまでは「シェイプ」の検査)。
2. **再計算による解決**: shape が通るだけでは B85-o1 と同じ「自己申告の一致」問題が残る
   (Sol の指摘: 「self-reported digest の比較だけにしない」)。そこで、raw evidence artifact
   を実際に保持しているのは受領側の公開エントリポイントだけなので、
   `_cross_check_refs_against_raw(route, raw)` を新設し、`evidence_union_from_raw_w6` が
   `_build_R1`/`_build_R2` の出力**双方**にこれを必ず適用する — 受領側が独自に
   `sha256_of(raw)` を再計算し、route の `claim_source_ref`/`evidence_refs` が申告する digest
   と**一致しない**場合、その route を MALFORMED へ格下げする。route が「見た目は正しい shape の
   ref を持つが、実際にはこの raw を指していない」場合に検出できる(テスト:
   `_cross_check_refs_against_raw(route built from raw_pos_01, but checked against a DIFFERENT
   raw artifact) -> MALFORMED`)。

### B85-o3 — status enum の fall-through

**症状**: `route_from_verifier_b_w6` は `ABSENT`/`MALFORMED` を明示分岐し、続いて `FAIL` を
分岐したあと、**残り全部を無条件 else で PASS 扱い**していた。従って
`route_from_verifier_b_w6("BOGUS", ..., "R2").route_status` は PASS になっていた。

**修理**: 四つの既知ステータス(`ABSENT`/`MALFORMED`/`FAIL`/`PASS`)を **exhaustive な
if/elif チェイン**にし、最後に明示的な `else` 相当の分岐を置いて、未知の値は
**必ず MALFORMED** を返すようにした。「それ以外は PASS」という暗黙の分岐はファイル中どこにも
残っていない。

### B85-o4 — connector 自身が armature/placeholder(count/digest)

**症状**: PASS 分岐が `expected_domain_count=checked_domain_count=1` を hardcode し、
`claim_digest`/`evidence_digest`/`expected_domain_digest`/`coverage_digest` すべてを
`sha256_of(detail)` から使い回していた。「1」は何の域も表していない発明された数だった。

**修理**: `expected_domain_count`/`checked_domain_count` を、W-6 契約が実際に持つ**二 lane 構造**
(`W6_DOMAIN_LANES = ("checker", "searcher")`、`ninfty-verifier-b.py` の
`NATIVE_SIDE_VALUES` に対応)から導出するよう変更した — PASS に到達する(つまり
`verify_W6_single` が両 lane を実際に解決し、比較一致した)場合のみ
`expected_domain_count=checked_domain_count=2`、`expected_domain_digest=coverage_digest=
sha256_of(sorted(W6_DOMAIN_LANES))` とする。これは「発明」ではなく、W-6 が契約上検査すべき
対象そのものの実数である。

**残る限界(発明しない・UNKNOWN 申告)**: R1(recomputation route)と R2(witness-coverage
route)は、依然として**同一の** `_run_w6_verifier(raw)` 呼び出し(= `verify_W6_single`)から
導出される — 本コードベースには W-6 用の**独立した第二の検証器**が実装されていない。
Sol の処方「できない部分は UNKNOWN 申告で残し『発効対象外』と明記 — 発明しない」に従い、
`_build_R2` のドキュメント文字列にこの限界を明記した。R1/R2 の genuine な実装独立性は
UNKNOWN のままであり、本追補はこれを解消したと主張しない — 解消したのは trust boundary
(raw evidence を受領側が自分で呼ぶかどうか)のみである。

## P85-5 item 7: 内部 constructor の module-private 化

`route_result_pass`/`_fail`/`_absent`/`_malformed` を `_route_result_pass` 等(先頭アンダース
コア、Python の「公開 API ではない」慣習)へ改名した。この module が公開する
untrusted-input 用のエントリポイントは `evidence_union_from_raw_w6(raw)` のみであり、
組み立て済み RouteResult を top-level 入力として受ける公開関数はもう存在しない
(`evidence_union_fail_closed_v2` は残るが、white-box な合成ロジック検査用の内部/テスト用途
であり、CLI からは到達しない)。

## 新しいエントリポイントの構造(要約)

```text
evidence_union_from_raw_w6(raw)                     <- 公開 trust boundary(唯一)
  |-- _build_R1(raw)   -- route_id="R1" 固定、raw のみ引数           \  ともに
  |     `-- _run_w6_verifier(raw)                                    |  受領側が
  |            `-- 自前で verify_W6_single(cert, native_a, native_b)  |  独自に
  |-- _build_R2(raw)   -- route_id="R2" 固定、raw のみ引数           |  呼ぶ
  |     `-- _run_w6_verifier(raw)  (同上、armature 限界は上記参照)   /
  |-- _cross_check_refs_against_raw(route1, raw)  -- refs を raw に対して再解決・再計算
  |-- _cross_check_refs_against_raw(route2, raw)
  `-- evidence_union_fail_closed_v2(route1, route2)  -- coerce_to_route_result で shape 再検査 -> 合成
```

`_build_R1`/`_build_R2` はいずれも引数を `raw` 一つだけ持つ(`inspect.signature` で機械検査
— テスト §7b)。route_id を呼び出し元が渡す余地は構造的に存在しない。

## Sol の三 probe + union 経路の負例化(P85-5 item 6)

`search/test_ninfty_evidence_union.py` §7/§7b に、便85 の F85-6.3 に記載された三つの literal
probe と union 経路を、そのまま返却 status まで assert する形で追加した:

1. `r1.claim_source_ref=None, r1.evidence_refs=None` -> `coerce_to_route_result` は MALFORMED
   (旧: PASS)。
2. `route_from_verifier_b_w6("BOGUS", forged_detail, "R2", raw).route_status` -> MALFORMED
   (旧: PASS)。
3. `union(r1, r2)`(refs=None 版)-> overall INTEGRITY_STOP(旧: PASS)。
4. 「valid-shape forged PASS」自体は白箱テストとして**意図的に PASS のまま残している**
   (`coerce_to_route_result` は shape だけを見る関数なので、shape が正しければ単体では
   PASS で正しい — 修理はこの関数自体を変えることではなく、この shape だけの値が**公開
   trust boundary から到達不能**になったことにある)。その到達不能性を、旧 `{route1, route2}`
   形式を新エントリポイント `evidence_union_from_raw_w6` に食わせる probe で確認し、
   overall INTEGRITY_STOP を assert した。

## 数値(機械出力、司令塔の検分用)

```text
python search/test_ninfty_evidence_union.py  -> 116/116 checks passed. (exit 0)
node search/ninfty-selftest-lanea.mjs        -> 93/93 passed. (exit 0, 回帰・無変更領域)
python search/test_ninfty_laneB.py           -> 184/184 checks passed. (exit 0, 回帰・無変更領域)
python search/test_ninfty_legacy_normalizer.py -> 51/51 checks passed. (exit 0, 回帰・無変更領域)
```

evidence-union は 94/94(便85 時点)から 116/116(+22, 便85 の三 probe・union 経路・
`evidence_union_from_raw_w6` の正例/負例・構造検査・B85-o2 の cross-check 負例を新規追加)。
lane A/B・normalizer の 3 suite はこの修理の影響範囲外(evidence-union.py 以外に変更なし)で
無変更・全 PASS を確認した。

## v4 → v5 差分まとめ

| 項目 | v4 | v5 |
|---|---|---|
| 公開エントリポイント | `evidence_union_fail_closed_v2(route1, route2)`(CLI もこれを直接叩く) | `evidence_union_from_raw_w6(raw)` のみ(CLI はこれだけを呼ぶ)。`evidence_union_fail_closed_v2` は内部/白箱テスト用途に降格 |
| CLI 入力 | 組み立て済み `{route1, route2}` RouteResult JSON | raw evidence artifact `{schema_id, certificate, native_a, native_b}` のみ |
| route-specific verifier の起動 | 呼び出し元が別途実行し、結果だけを渡す(未検証でも可) | receiver 側 dispatch (`_run_w6_verifier`) が自分で `verify_W6_single` を呼ぶ |
| route_id 指定 | `route_from_verifier_b_w6(status, detail, route_id)` の第三引数で呼び出し元が指定 | `_build_R1`/`_build_R2` は `raw` 一引数のみ、route_id は関数ごとに固定 |
| claim_source_ref/evidence_refs | allowed field、None 許容、shape/内容とも未検査 | 必須・non-null・shape 検査(コンストラクタ+coerce)+受領側による raw との digest 再計算・再検査 |
| status enum 分岐 | ABSENT/MALFORMED/FAIL を明示、残りは無条件 PASS(fall-through) | ABSENT/MALFORMED/FAIL/PASS を exhaustive if/elif、未知値は明示 MALFORMED |
| PASS の domain count/digest | hardcoded `1`/`1`、`sha256_of(detail)` の使い回し | 実際の W-6 二 lane 構造(`W6_DOMAIN_LANES`)から導出 |
| constructor の公開性 | `route_result_pass` 等が公開名 | `_route_result_pass` 等、module-private 命名に改名 |

## 状態

Sol 便85 F85-6.3/P85-5 の是正として起草。実装(`search/ninfty-evidence-union.py`)・テスト
(`search/test_ninfty_evidence_union.py`、Sol の literal probe 全てを負例化し返却 status まで
assert、加えて新エントリポイントの正例/負例・構造検査)のフル再走で確認 — 数値は上記に
機械出力のまま記載した。v2/v3/v3.1/v4 は既存ファイルのまま非上書き(履歴として残す)。
本追補はコミットしていない(実装担当タスクの指示により)。
