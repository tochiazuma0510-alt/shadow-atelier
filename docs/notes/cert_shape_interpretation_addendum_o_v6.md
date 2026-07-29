# interp 追補 (o) v6 — public facade 一本化・R2 独立実装・native dereference(Sol 便86 F86-1.4 B86-o1..o3/P86-2 処方)

状態: interpretation / candidate(v5 は履歴として非上書き — v5 の raw-evidence trust-boundary
自体は本追補でも不変。本追補が改めるのは (1) 公開面の一本化、(2) R1/R2 の実装独立性、
(3) W-6 map_ref の native artifact への実際の dereference)。合成器名は
evidence-union/fail-closed-v2(P81-E)のまま不変 — `_compose_route_statuses` の 4 規則
(N83-2.1、便83 で Sol 確認済み PASS)は本追補でも不変。

## 便86 差戻しの三блока: B86-o1 / B86-o2 / B86-o3

### B86-o1 — 公開面が一本化されていない

**症状(Sol 指摘)**: `evidence_union_fail_closed_v2(route1, route2)` と
`route_from_verifier_b_w6(status, detail, route_id, raw)` が非 underscore 名で module 直下に
残り、`__all__` も無かった。suite は「forged-but-valid-shape R1/R2 → overall PASS」を
EXPECTED control として通していたが、これは in-process API でも raw RouteResult dict を
public trust boundary に置かない、という P85-5 item 7 の趣旨を完全には閉じていなかった。

**修理**: `search/ninfty-evidence-union.py` の低レベル combinator/adapter を全て
module-private(先頭アンダースコア)へ改名した:

| 旧名(v5) | 新名(v6) |
|---|---|
| `compose_route_statuses` | `_compose_route_statuses` |
| `coerce_to_route_result` | `_coerce_to_route_result` |
| `evidence_union_fail_closed_v2` | `_evidence_union_fail_closed_v2` |
| `route_from_verifier_b_w6` | `_route_from_verifier_result`(R1/R2 共用に一般化、下記 B86-o2) |

`__all__ = ["evidence_union_from_raw_w6"]` を設置した — この module が公開する名前は
**これ一つだけ**。「forged PASS = EXPECTED control」の suite 行は、私有 API
(`_coerce_to_route_result`/`_evidence_union_fail_closed_v2`)を直接叩く**白箱テスト**として
明示的に隔離し(`search/test_ninfty_evidence_union.py` §7、control とコメントで明記)、
公開 façade `evidence_union_from_raw_w6` 経由の同種 forged 入力は
`search/test_ninfty_evidence_union.py` §10b の新負例で INTEGRITY_STOP を確認した
(単一の forged RouteResult dict を **wrapping なしでそのまま** `raw` 引数へ渡す —
`{route1, route2}` 形式でラップした旧来の probe より一段厳格な形)。

**構造テスト**(§8): `eu.__all__ == ["evidence_union_from_raw_w6"]` の直接検査に加え、
`search/` 直下の他の全ファイルが `ninfty-evidence-union.py` を実際に動的ロードしているか
(このコードベースの規約 = `importlib.util.spec_from_file_location` へ引き渡す引数として
`"ninfty-evidence-union.py"` という quoted path literal を含むか)を grep する。
現状ロードしているのは本テストファイル自身のみ — 従って「本番呼び出し元が低レベル API へ
到達できる経路」はゼロであることを機械的に確認した。素朴な private 名の部分文字列一致は
`_verifier_b` が `ninfty-verifier-b.py` 自身の無関係な `run_verifier_b` 関数名と衝突するなど
偽陽性を生むため採用せず、word-boundary 正規表現かつロード元ファイルに限定した defense-in-depth
チェックを別途置いた。

### B86-o2 — R1/R2 が同一 verifier の二重実行

**症状**: `_build_R1`/`_build_R2` はいずれも `_run_w6_verifier(raw)` →
`ninfty-verifier-b.verify_W6_single` を呼んでいた。同じ raw・同じ実装・同じ predicate なので
二経路 evidence union になっていなかった(v5 はこれを UNKNOWN 申告のまま「発効対象外」と
明記していたが、発効させないという意味で問題を先送りしていただけだった)。

**修理**: **第二の独立実装** `search/ninfty-verifier-w6-r2.py` を新設した。
`verify_W6_single_r2(cert, native_a, native_b)` は `ninfty-verifier-b.py` と
**helper 関数もimport も一切共有しない**、素朴な単一関数実装(RFC 6901 pointer walk・
ref-triple reader・map reducer を独自にベタ書き)で、同じ数学的 predicate
(「searcher/checker 両 lane が同じ {branch_value: multiplicity} pushforward map を証言するか」)
を独立に再計算する。`_build_R2` はこれを呼ぶよう変更した。

R1/R2 双方の RouteResult に新しい PASS/FAIL 専用フィールド `implementation_id`(非空文字列)・
`source_digest`(その verifier module 自身のファイルバイト列を毎回再計算した SHA-256、
キャッシュや自己申告ではない)を追加した — `_route_result_pass`/`_route_result_fail` の
必須 keyword-only 引数、`_coerce_to_route_result` でも同じ必須性を検査する。

`evidence_union_from_raw_w6` は合成の直前に新設の
`_require_distinct_implementations(route1, route2)` を通す: 両方が PASS/FAIL に到達していて
`implementation_id` または `source_digest` が一致していたら、**両方を MALFORMED へ格下げ**
(→ 合成後 overall INTEGRITY_STOP)する。これにより「R1/R2 の実装独立性」は文書上の限界注記
ではなく、**再発を機械的に検出する回帰ガード**になった
(`search/test_ninfty_evidence_union.py` §9 の
「REGRESSION GUARD: 同一 implementation_id/source_digest を持つ二つの PASS route を union に
かけると両方 MALFORMED になる」テストがこれを直接検証する)。

### B86-o3 — native dereference が未実装

**症状**: `ninfty-verifier-b.py::_extract_w6_map` は map_ref の `inline` 内容のみを
再検証し、`json_pointer`/`object_id` を実際の `native_payload`(受領側が保持する pinned
native artifact)へ解決する処理が存在しなかった。攻撃者は certificate・native_a・native_b・
互いに自己整合的な二つの inline map を一緒に作れば、native 本体に存在しない同一 map を
両 lane に書いて PASS を作れた。

**修理**: `ninfty-verifier-b.py` に `_resolve_json_pointer`(RFC 6901、
`ninfty-verifier-a.mjs` の `resolveJsonPointer` と同じアルゴリズムを独立に移植)と
`_dereference_native_ref` を新設した。優先順位:

1. `json_pointer` が `native_payload` 内で解決する → その値が**権威的な候補**。
   再計算した digest が ref 自身の `digest` と一致しなければ既存の `[12] RefDigestMismatch`
   (MALFORMED)。**`inline` の有無に関わらず**、この経路が優先される — 攻撃者が
   digest-self-consistent な inline を用意していても、native artifact の実際の内容と
   一致しなければ検出される。
2. `json_pointer` が無い/解決しない場合のみ `inline` へフォールバック(既存の
   digest-consistency check、裁定150 items 2/3 の意味論のまま — 既存 fixture の
   native artifact は `/pushforward_map` キーを持たないため、この経路が使われ続け、
   既存の positive/negative fixture 群への回帰影響はゼロ)。
3. どちらも解決しない → `(None, <reason>)`(UNKNOWN、無言の PASS にしない、変更なし)。

`_extract_w6_map` は map_ref についてこの新しい dereference を使うよう変更した
(ramification_ref/branch_ref/witness_ref の scope は変更していない — Sol の B86-o3 指摘は
map_ref に特化していたため)。

## 新負例 3 種(P86-2 item 4)

`search/test_ninfty_evidence_union.py` §10 に追加(全て `verify_W6_single` 単体と
`evidence_union_from_raw_w6` 経由の両方で確認):

1. **公開façade経由の forged RouteResult**(§10b): 有効な shape の PASS RouteResult を
   ラップなしでそのまま `raw` 引数として `evidence_union_from_raw_w6` へ渡す →
   `schema_id` が raw evidence 用のものと一致しないため INTEGRITY_STOP。
2. **一致する forged inline map**(§10c): searcher/checker 両 lane が同じ自己整合的な
   forged inline map を持つ(v5 以前なら PASS していたケース)→ 実際の native artifact の
   `/pushforward_map` を dereference すると異なる内容が出るため RefDigestMismatch →
   MALFORMED → INTEGRITY_STOP。
3. **native ref の入れ替え**(§10d): 正当な certificate が searcher の map を native_a の
   真の内容に、checker の map を native_b の(別の)真の内容にそれぞれ pin している状態で、
   `native_a`/`native_b` を**引数レベルで入れ替えて**渡す → 各 lane の json_pointer が
   誤った artifact を dereference し、certificate が pin した digest と食い違う →
   MALFORMED → INTEGRITY_STOP。正しい(入れ替えなし)割り当てでは legitimate な FAIL
   (実際に map が異なる)になることも control として確認した。

## CLI exit code(P86-2 の NOTE)

`main()` は `overall_status == "PASS"` のときのみ exit 0、それ以外は 1 を返すよう変更した
(旧: 常に 0)。`search/test_ninfty_evidence_union.py` §11 が subprocess 経由で
PASS/FAIL/INTEGRITY_STOP それぞれの raw evidence に対する実際の終了コードを確認する。

## 数値(機械出力、司令塔の検分用)

```text
python search/test_ninfty_evidence_union.py     -> 153/153 checks passed. (exit 0)
node search/ninfty-selftest-lanea.mjs           -> 93/93 passed. (exit 0, 回帰・無変更領域)
python search/test_ninfty_laneB.py              -> 184/184 checks passed. (exit 0, 回帰 -- ninfty-verifier-b.py
                                                     の map_ref dereference 変更を含むが、既存 fixture は
                                                     json_pointer 未解決経路のままなので無影響)
python search/test_ninfty_legacy_normalizer.py  -> 51/51 checks passed. (exit 0, 回帰・無変更領域)
```

evidence-union は 116/116(便85 v5 時点)から 153/153(+37, 便86 の §8 public-facade
構造テスト・§9 R2 独立性/回帰ガード・§10 native dereference 正例+新負例3種・§11 CLI exit code
を新規追加、既存 §1-7 は private 名改名+implementation_id/source_digest 必須化に伴う更新)。

## R1/R2 実装 ID・source digest(機械出力)

```text
IMPLEMENTATION_ID_R1 = "ninfty-verifier-b.py::verify_W6_single"
IMPLEMENTATION_ID_R2 = "ninfty-verifier-w6-r2.py::verify_W6_single_r2"

source_digest(ninfty-verifier-b.py)      = 999ed1fde84addf21940a7ff8601cfbbfec0fcd488fa12686d7c39826f8e0039
source_digest(ninfty-verifier-w6-r2.py)  = aafbb4b4e8528df5116482517901a3f9d6e360bea43a726d50497288e7409717

ninfty-evidence-union.py       sha256 = 18fbd0ef7ca0594e602c43975809fa8d329e3468ac63867126de472837107727
ninfty-verifier-b.py           sha256 = 999ed1fde84addf21940a7ff8601cfbbfec0fcd488fa12686d7c39826f8e0039
ninfty-verifier-w6-r2.py       sha256 = aafbb4b4e8528df5116482517901a3f9d6e360bea43a726d50497288e7409717
test_ninfty_evidence_union.py  sha256 = 2976327022438af18a18cd2210a1d2233c114de1dce584b6abddc1e8f6f484a6
```

R1/R2 は実際に異なる `implementation_id`・異なる `source_digest` を持つ(`evidence_union_from_raw_w6`
の genuine raw evidence の実行結果で毎回確認可能 -- §7b・§9 参照)。

## v5 → v6 差分まとめ

| 項目 | v5 | v6 |
|---|---|---|
| 公開エクスポート | 未宣言(`__all__` なし) | `__all__ = ["evidence_union_from_raw_w6"]` のみ |
| 低レベル combinator の可視性 | 非 underscore(公開名) | 全て `_` 私有化 |
| R2 の実装 | R1 と同一の `verify_W6_single` を再呼び出し(UNKNOWN 申告のまま) | 独立実装 `ninfty-verifier-w6-r2.py::verify_W6_single_r2`(helper 非共有) |
| R1/R2 独立性の検査 | 文書上の限界注記のみ | `_require_distinct_implementations` が implementation_id/source_digest 一致を検出し MALFORMED へ格下げ(機械的な回帰ガード) |
| W-6 map_ref の native 拘束 | inline のみ再検証(digest-only ref は UNKNOWN) | json_pointer を実際の native artifact へ解決、権威的な値として digest 再検査(inline は解決不能時のみのキャッシュ) |
| CLI exit code | 常に 0 | overall_status=="PASS" のときのみ 0、それ以外は 1 |
| RouteResult PASS/FAIL 必須フィールド | claim_source_ref/evidence_refs | 上記 + implementation_id/source_digest |

## 状態

Sol 便86 F86-1.4 B86-o1..o3/P86-2 の是正として起草。実装
(`search/ninfty-evidence-union.py`・`search/ninfty-verifier-b.py`・新設
`search/ninfty-verifier-w6-r2.py`)・テスト(`search/test_ninfty_evidence_union.py`)の
フル再走で確認 — 数値は上記に機械出力のまま記載した。v2/v3/v3.1/v4/v5 は既存ファイルのまま
非上書き(履歴として残す)。本追補はコミットしていない(実装担当タスクの指示により)。
