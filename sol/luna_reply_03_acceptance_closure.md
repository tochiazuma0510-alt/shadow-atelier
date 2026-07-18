# Luna reply 03 — acceptance closure

対象 `sol/luna_task_03_acceptance_closure.md` を読み、指定範囲で最終受入れ検査を実施した。commit/push はしていない。

## 対象ファイル

- 実装・検査器: `crosscheck/check.mjs`
- GAP shard: `search/suite-wp2-explorer.g`, `search/suite-wp2-explorer-q1836.g`
- 証明書: `certificates/K3.v1.json`, `K4.v1.json`, `K5.v1.json`, `K6.v1.json`, `K7.v1.json`, `K8.v1.json`, `K9.v1.json`, `K10.v1.json`, `K11.v1.json`, `K12.v1.json`, `K13.v1.json`, `K14.v1.json`, `K15.v1.json`, `K16.v1.json`, `K18.v1.json`, `K36.v1.json`, `N5.v1.json`
- Node verdict: 対応する17件の `crosscheck/verdicts/*.v1.verdict.json` と `crosscheck/verdicts/global.v1.verdict.json`
- hash 台帳: `provenance/cert-hashes-wp2.txt`
- 本返信: `sol/luna_reply_03_acceptance_closure.md`

## 実行結果

構文検査:

```text
node --check crosscheck/check.mjs
Exit code: 0
```

フル Node 実行（18 verdict + global）は 571 秒で完了し、自己検査・Thm.4.3 自前生成・全 verdict・global のすべてが PASS だった。

```text
node crosscheck/check.mjs --cap 600000
自己検査: ALL PASS
...
GLOBAL ALL PASS: YES
```

代表的な出力:

```text
K36: 0_schema_fail_closed ... 13_varrho: PASS
ALL PASS (cross-checked): YES
N5: 1_n5_full_enumeration: PASS
ALL PASS (cross-checked): YES
numeric: PASS
doubling: PASS
Prop.3.5: PASS true=44 false=212 mismatch=0
K36 triangle: PASS checked=216/216
GLOBAL ALL PASS: YES
```

global-only 再実行:

```text
node crosscheck/check.mjs --global-only --cap 600000
cap_ms=600000 status=PASS numeric=PASS doubling=PASS Prop.3.5=PASS checked=256/256
```

## A: raw formula

全16 dihedral cert で `claimed_raw = |X_n| * |[G_n,G_n]|` を Node が再計算し、誤値を reject する fail-closed fixture も自己検査 PASS だった。

| cert | claimed | expected | |X_n| | derived | ok |
|---|---:|---:|---:|---:|---|
| K3 | 108 | 108 | 4 | 27 | PASS |
| K4 | 8 | 8 | 4 | 2 | PASS |
| K5 | 1000 | 1000 | 8 | 125 | PASS |
| K6 | 108 | 108 | 4 | 27 | PASS |
| K7 | 4116 | 4116 | 12 | 343 | PASS |
| K8 | 128 | 128 | 8 | 16 | PASS |
| K9 | 8748 | 8748 | 12 | 729 | PASS |
| K10 | 1000 | 1000 | 8 | 125 | PASS |
| K11 | 26620 | 26620 | 20 | 1331 | PASS |
| K12 | 432 | 432 | 8 | 54 | PASS |
| K13 | 52728 | 52728 | 24 | 2197 | PASS |
| K14 | 4116 | 4116 | 12 | 343 | PASS |
| K15 | 54000 | 54000 | 16 | 3375 | PASS |
| K16 | 2048 | 2048 | 16 | 128 | PASS |
| K18 | 8748 | 8748 | 12 | 729 | PASS |
| K36 | 34992 | 34992 | 24 | 1458 | PASS |

Result: raw 16/16.

N5 independent enumeration: raw 5/5, hexagon 5/5, charming 4/4, surjective 4/4; central-power check 4/4.

## B: factor maps and global counts

| suite | result |
|---|---:|
| numeric rows | 16/16 PASS |
| doubling isomorphism rows | 7/7 PASS |
| Prop.3.5 ordered pairs | 256/256 PASS |
| number-theory true pairs | 44 |
| false pairs | 212 |
| false pair collision detected | 212 |
| false-yet-well-defined | 0 |
| true pair collision | 0 |
| mismatch | 0 |
| K36 reduction triangle | 216/216 PASS |

The existing `false_collision_count` meaning is preserved and is 0; additive fields record false-pair collision (212), false-pair well-defined (0), and true-pair collision (0). `global.v1.verdict.json` has `status=PASS`, `all_pass=true`, and `cap_ms=600000`; `all_pass` explicitly depends on numeric, doubling, Prop.3.5, and reduction-triangle results.

Doubling rows are `3→6, 5→10, 7→14, 9→18, 11→22, 13→26, 15→30`; every row has `well_defined=true`, `injective=true`, `image_order=target_order`.

## C: representative shift direct comparisons

For every canonical dihedral shadow, the checker directly applied `(m,f) -> (m+N_ord, f*x^N_ord)` and checked original/shifted hexagon, quotient `f`, both `T(sigma)` values, both shifted composition sides, and every required reduction source index. All `x^N_ord in N_F2` assertions and downstream checks passed.

| cert | shadows / hex shifted / equal | composition left | composition right | reduction |
|---|---:|---:|---:|---:|
| K3 | 12/12/12 | 144/144 | 144/144 | 0/0 |
| K4 | 4/4/4 | 16/16 | 16/16 | 0/0 |
| K5 | 40/40/40 | 1600/1600 | 1600/1600 | 0/0 |
| K6 | 12/12/12 | 144/144 | 144/144 | 0/0 |
| K7 | 84/84/84 | 7056/7056 | 7056/7056 | 0/0 |
| K8 | 16/16/16 | 256/256 | 256/256 | 16/16 |
| K9 | 108/108/108 | 11664/11664 | 11664/11664 | 108/108 |
| K10 | 40/40/40 | 1600/1600 | 1600/1600 | 0/0 |
| K11 | 220/220/220 | 48400/48400 | 48400/48400 | 0/0 |
| K12 | 24/24/24 | 576/576 | 576/576 | 24/24 |
| K13 | 312/312/312 | 97344/97344 | 97344/97344 | 0/0 |
| K14 | 84/84/84 | 7056/7056 | 7056/7056 | 0/0 |
| K15 | 240/240/240 | 57600/57600 | 57600/57600 | 0/0 |
| K16 | 64/64/64 | 4096/4096 | 4096/4096 | 0/0 |
| K18 | 108/108/108 | 11664/11664 | 11664/11664 | 108/108 |
| K36 | 216/216/216 | 46656/46656 | 46656/46656 | 432/432 |

## D: exact rho set

The independent set comparison for `n=4,8,16` has no missing, extra, or duplicate elements:

| n | expected | actual | missing | extra | duplicate | witness |
|---:|---:|---:|---:|---:|---:|---|
| 4 | 4 | 4 | 0 | 0 | 0 | N/A for n=4 |
| 8 | 16 | 16 | 0 | 0 | 0 | expected=actual; noncommuting PASS |
| 16 | 64 | 64 | 0 | 0 | 0 | expected=actual; noncommuting PASS |

For n=8 and n=16 the stored witness uses `(0,-1)` and `(1,5)`, including expected/actual rho products and the reverse-order distinction; both products match and are noncommuting.

## E: GAP status

Both prescribed shard commands were attempted through the repository wrapper, but GAP is unavailable in this sandbox:

```text
.\gap.ps1 search\suite-wp2-explorer.g
gap.exe: *** fatal error - couldn't create signal pipe, Win32 error 5

.\gap.ps1 search\suite-wp2-explorer-q1836.g
gap.exe: *** fatal error - couldn't create signal pipe, Win32 error 5
```

Therefore GAP shard acceptance is `UNKNOWN` (not FAIL). No GAP artifact was claimed as newly generated; the expected artifact commands are recorded above. Node acceptance is independent and PASS. No search scope was expanded.

## Certificate hashes

The 17 certificate prefixes match `provenance/cert-hashes-wp2.txt`:

```text
K3 d7cd44ea6d71e341
K4 0c206bf439db6aee
K5 b659cc18e1083b9a
K6 13587f751b87b5c5
K7 05399fc7602ecae5
K8 834b68d6e528c131
K9 ceac37e0039454d4
K10 a2af3e3aa96cd430
K11 d02ddf9aaa3b7fbf
K12 95a291e2d44f5628
K13 b9a89b812224ea17
K14 c90c80b8053a8a91
K15 08493ccec8f75469
K16 d540ec5caa3577eb
K18 412d2108f3d3794c
K36 feac2a0202e5b78
N5 a98df7f9ba4eef13
```

## 最終 `git status --short`

返信ファイル作成後の実状態は以下のとおり。

```text
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
 M crosscheck/verdicts/global.v1.verdict.json
?? sol/luna_reply_03_acceptance_closure.md
```

No commit/push performed.
