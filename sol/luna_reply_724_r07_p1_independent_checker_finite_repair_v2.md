# Luna Reply 724 — independent P1 checker v2 finite repair

## Verdict

`DONE`. Task718 の完全 blocker list だけを v2 checker に有限修理した。producer v4、workflow、Task554 artifact、git には触れていない。real artifact replay と GHA は実行していない。

## Output

- `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v2.py`
  - bytes: `130683`
  - LF: `2689`
  - CRLF: `0`
  - final LF: `true`
  - SHA-256: `8636440c5e51d71a1f06d20d89a3d60c588453e741b17fbbd61735c76a9d3e88`
- `sol/luna_reply_724_r07_p1_independent_checker_finite_repair_v2.md`
  - この返信の最終 bytes/LF/SHA-256 は保存後のファイル値を正本とする。

## Exact repairs

1. `BLOCK_BODY_KEYS` に `origin_reductions` を追加し、production の `validate_block_body_keys` を body validator と fixture が共有するようにした（checker lines 1373–1389）。
2. packet origin は index `i` 同士で照合し、`[-1]` と反復 slice を除去した。入力終了時に exact count を要求する（lines 1630–1695）。
3. producer v4 の path と SHA-256 を literal pin し、artifact 認証前に actual bytes を照合する。入力は canonical prepare + ordered block 0–3 + join の六 receipt のみにした（lines 1711–1721, 2082–2130, 2174–2195）。
4. `cv_sum_table` は length 4、全要素 `plain_int`、exact `[1,0,0,0]` を要求し、受信した typed list から digest を再計算する（lines 1991–2009）。
5. production-called `validate_cli` が selftest / compact / complete named のちょうど一つだけを許す。compact は12引数、named は5 phase receipts と join を必須化した（lines 2606–2669）。
6. production helper/kernel を通る bounded live fixtures を追加した。block key 欠落・rename、二 origin swap、実 old-lift 負号、parent/claim/join mutation、bool projector、producer bytes/SHA、receipt reorder、CLI 混在・partial を拒否し、完全六 receipt chain を production join validator で受理する。

最終 checker result は六 canonical raw receipt の SHA-256（prepare、blocks 0–3、join）を個別に束縛する。成功メタデータは `independent_checker=true` のみで、`precision2/A0/COMMON/COMPATIBLE_LIFT/FAKE/IHARA/verified=false` を維持した。

## Bounded checks

実行:

```text
python -m py_compile crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v2.py
python crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v2.py --selftest
```

結果:

```text
py_compile: PASS
selftest: PASS
fixture_accept: 6
rejections: 41
all rejection_table entries: REJECT
```

Producer pin の独立照合:

```text
path: search/d972_r07_grade2_p1_componentwise_semantic_replay_v4.py
bytes: 41259
LF: 381
final LF: true
SHA-256: ff50d0ad50e080a15075bb52365987d9e389bf59e5e39666002b710947287a17
```

`ACTUAL_FIVE_ARTIFACT_CHECK=DEFERRED_TO_GHA`

`verified=false`
