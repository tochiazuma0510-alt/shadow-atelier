# Luna 便02b返信 — global sweep follow-up

## 完了結果

Node 側 global sweep を完走させた。source 群の Cayley BFS は対象ごとに一度だけ構築し、親ポインタ＋整数 generator edge を全 pair で再利用した。`--cap <ms>` と `GTSH_GLOBAL_CAP_MS` を追加し、既定値は 120000 ms のまま。

global verdict の結果:

- numeric: 16/16 PASS（K3..K16,K18,K36 の `|G_n|` と `N_ord`）
- doubling: 7/7 PASS（source n=3,5,7,9,11,13,15；target 22,26,30 は補助 target）
- Prop.3.5: 256/256 PASS
- number-theory true/false: 44 / 212
- mismatch: 0
- false collision: 0（false 対 212 件は全て collision、誤受理なし）
- 実測: 3816 ms（`--cap 600000`、cap内）

司令塔側の GAP 再生成が並行完了し、K36→K4 direct entry が追加された。`global.all_pass=true`、K36 triangle 216/216 PASS。

## 変更差分

- `crosscheck/check.mjs`
  - global-only mode で証明書別 self-check/Thm4.3再計算をスキップ。
  - `buildGnLight` を追加し、global sweep では derived subgroup を再計算しない。
  - source Cayley table を parent/generator integer edge で一回だけ構築。
  - pair ごとの target image を親から伝播し、source edge collision を検査。
  - doubling の補助対象を source 22/26/30 ではなく target 22/26/30 として修正。
  - factor map の acceptance 条件を injectivity ではなく well-definedness に修正（仕様は source collision の一致を要求する quotient/factor map）。
  - `--cap <ms>` / `GTSH_GLOBAL_CAP_MS` を実装。
- `certificates/K36.v1.json`: GAP 再生成で K36→K4 direct entry が追加された。
- `crosscheck/verdicts/global.v1.verdict.json`: PASS sweep 結果を再生成。
- `sol/luna_reply_02b_global_sweep.md`: 本返信。

証明書別 verdict の再実行は指示どおり行っていない。GAP側再生成は並行完了済み。

## 実行出力（原文）

```text
node --check crosscheck/check.mjs

node crosscheck/check.mjs --global-only --cap 600000
=== global-only: certificate self-check skipped (last full run was ALL PASS) ===

=== 証明書の検査 ===

=== global suite only: numeric/doubling/Prop.3.5 ===
global verdict -> C:\Users\81905\Desktop\shadow-atelier\crosscheck\verdicts\global.v1.verdict.json
  cap_ms=600000 status=PASS numeric=PASS doubling=PASS Prop.3.5=PASS checked=256/256
```

verdict の要約:

```text
status=PASS
elapsed_ms=3816
numeric.ok=true
doubling.ok=true
prop_3_5.ok=true
prop_3_5.total=256
prop_3_5.true_count=44
prop_3_5.false_count=212
prop_3_5.mismatch_count=0
prop_3_5.checked_pairs=256
prop_3_5.false_collision_count=0
reduction_triangle=PASS (216/216)
all_pass=true
```

## git status --short

```text
 M certificates/K36.v1.json
 M certificates/N5.v1.json
 M crosscheck/check.mjs
 M crosscheck/verdicts/K10.v1.verdict.json
 M crosscheck/verdicts/K11.v1.verdict.json
 M crosscheck/verdicts/K12.v1.verdict.json
 M crosscheck/verdicts/K13.v1.verdict.json
 M crosscheck/verdicts/K14.v1.verdict.json
 M crosscheck/verdicts/K15.v1.verdict.json
 M crosscheck/verdicts/K16.v1.verdict.json
 M crosscheck/verdicts/K18.v1.verdict.json
 M crosscheck/verdicts/K3.v1.verdict.json
 M crosscheck/verdicts/K36.v1.verdict.json
 M crosscheck/verdicts/K4.v1.verdict.json
 M crosscheck/verdicts/K5.v1.verdict.json
 M crosscheck/verdicts/K6.v1.verdict.json
 M crosscheck/verdicts/K7.v1.verdict.json
 M crosscheck/verdicts/K8.v1.verdict.json
 M crosscheck/verdicts/K9.v1.verdict.json
 M crosscheck/verdicts/N5.v1.verdict.json
 M provenance/cert-hashes-wp2.txt
 M search/suite-wp2-explorer-q1836.g
 M search/suite-wp2-explorer.g
 ?? crosscheck/verdicts/global.v1.verdict.json
?? ops/inbox_codex/20260719-003000_luna02-global-sweep-followup.md
?? sol/luna_reply_02_gate_closure.md
?? sol/luna_reply_02b_global_sweep.md
```

Commit/push はしていない。
