# Luna 便02返信 — G1★ gate closure

## 結果

Node checker の証明書別 fail-closed 検査は 17 通中 16 通が ALL PASS。N5、全 dihedral composition/inverse、代表元不変性、K4/K8/K16 の ϱ は PASS。未完了は環境起因の GAP 再生成、K36→K4 直接 entry、global 256 対であり、全体 `all_pass=false` を維持した。

## 変更ファイル

- `crosscheck/check.mjs`: schema/必須 field/invariants fail-closed、N5全列挙、厳密 composition/inverse coverage、reduction coverage、代表元、theta/tau、ϱ、global verdict を追加。
- `search/suite-wp2-explorer.g`: N5 の `target.n=5`、`f_triple`、counts (`5,5,4,4`) を出力するよう変更。
- `search/suite-wp2-explorer-q1836.g`: K4再構成と K36→K4 直接 reduction を出力するよう変更（GAP起動障害のため未実行）。
- `certificates/N5.v1.json`: 上記スキーマ/countsを反映。
- `crosscheck/verdicts/K*.v1.verdict.json`, `N5.v1.verdict.json`: Node checker 再生成。
- `crosscheck/verdicts/global.v1.verdict.json`: global fail-closed UNKNOWN verdict。
- `provenance/cert-hashes-wp2.txt`: N5 hash を更新。

## 実行出力

```text
node --check crosscheck/check.mjs
  node syntax ok

.\gap.ps1 search\suite-wp2-explorer.g
  gap.exe: *** fatal error - couldn't create signal pipe, Win32 error 5

.\gap.ps1 search\suite-wp2-explorer-q1836.g
  gap.exe: *** fatal error - couldn't create signal pipe, Win32 error 5

node crosscheck/check.mjs
  self-check: ALL PASS
  certificate verdicts: K3..K16,K18,K36,N5 written
  K3..K16,K18,K4..K9,N5: ALL PASS
  K36: FAIL only at 9_reduction (required K4 entry missing; K12 entry PASS)
  global sweep: exceeded 120000 ms cap; process stopped at 576.5 s

node crosscheck/check.mjs --global-only
  status=UNKNOWN numeric=PASS doubling=UNKNOWN Prop.3.5=UNKNOWN checked=0/256
```

`[ANOMALY]` は Node 側で 0 件。GAP は signal-pipe 作成前に停止したため、GAP 側 anomaly 判定には到達していない。

## certificate counts

| target | |G| | shadows | raw | hex | charming | surj | reduction |
|---:|---:|---:|---:|---:|---:|---:|:---|
| K3 | 108 | 12 | 108 | 12 | 12 | 12 | — |
| K4 | 32 | 4 | 8 | 4 | 4 | 4 | — |
| K5 | 500 | 40 | 1000 | 40 | 40 | 40 | — |
| K6 | 108 | 12 | 108 | 12 | 12 | 12 | — |
| K7 | 1372 | 84 | 4116 | 84 | 84 | 84 | — |
| K8 | 256 | 16 | 128 | 16 | 16 | 16 | K4 |
| K9 | 2916 | 108 | 8748 | 108 | 108 | 108 | K3 |
| K10 | 500 | 40 | 1000 | 40 | 40 | 40 | — |
| K11 | 5324 | 220 | 26620 | 220 | 220 | 220 | — |
| K12 | 864 | 24 | 432 | 24 | 24 | 24 | K4 |
| K13 | 8788 | 312 | 52728 | 312 | 312 | 312 | — |
| K14 | 1372 | 84 | 4116 | 84 | 84 | 84 | — |
| K15 | 13500 | 240 | 54000 | 240 | 240 | 240 | — |
| K16 | 2048 | 64 | 2048 | 64 | 64 | 64 | — |
| K18 | 2916 | 108 | 8748 | 108 | 108 | 108 | K3 |
| K36 | 23328 | 216 | 34992 | 216 | 216 | 216 | K12; K4 missing |
| N5 | — | 4 | 5 | 5 | 4 | 4 | — |

N5 independent enumeration: `m-set={0,1,3,4}`, direct central-power PASS for all four accepted shadows; m=2 is hexagon PASS but charming-unit and surjective FAIL. `tc_check_pass=true`.

## coverage and global tables

- Every dihedral certificate has composition rows `S*S` and inverse rows `S`; all such rows PASS. LS coverage is `S` exactly for `3|n`, and expected-zero otherwise.
- ϱ: n=4 `(4 shadows, 16 products) PASS`; n=8 `(16,256) PASS`; n=16 `(64,4096) PASS`. Witnesses: n=8 products `5` vs `3`, n=16 products `5` vs `3`, hence noncommuting PASS. Shadow counts equal `2^(2α−2)`.
- Numeric global rows: 16/16 PASS for `|G_n|` and `N_ord`, including K18/K36.
- Prop.3.5 number-theory partition: true `44`, false `212`, total `256`; source Cayley collision sweep checked `0/256` before cap, so no PASS is inferred.
- Doubling: required odd n `3,5,7,9,11,13,15`; auxiliary `22,26,30`; UNKNOWN (not completed within cap).
- K36 triangle: UNKNOWN/0 of 216 because direct K36→K4 certificate entry was not regenerated.

## hashes

All unchanged certificate prefixes remain as recorded in `provenance/cert-hashes-wp2.txt`; N5 changed from `9f26d82ca15014b6` to `740d63869189d6ae`. K36 hash is unchanged because the direct entry was not regenerated.

## git status --short

```text
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
?? sol/luna_reply_02_gate_closure.md
```

Commit/push はしていない。
