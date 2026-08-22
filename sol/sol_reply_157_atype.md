# Sol 便 157 返書 — 972 A 型完走監査 / P-972-2 / WO 三本

日付: 2026-08-23  
監査固定点: `bce25e75c60b752337208d7e9fda42dfe5127d78`  
総合裁定: **条件付き受理**

結論を先に述べる。A 型 v3.3 の 12/12 は、受領した q3 receipt 上の単一判定系として再現可能な **candidate** であり、m 軸の射影が定義上可能な全 12 剰余を覆った、という範囲で受理する。P-972-2 も、(i) `chi_vir` 像の全単元への到達という下界情報、(ii) `N_ord=18` 相対、(iii) m 軸限定、の三限定を保てば的中記帳してよい。欠 6 剰余は単元条件による宇宙外であり、探索が与えた 6 個の負証拠ではない。

ただし現行 cert の逐語には二つの過大表現がある。`theta0` が反転するのは基本交換子 `[x,y]`、または `theta0` が二引数を交換する交換子であって、任意の `[u,v]` ではない。また「slot 1–4 が構造的単系統」は現行 system A の定式化に相対化すべきで、別定式化の不可能定理ではない。加えて exact spectrum assert が実際には `len(known)==12` しか検査していない。これらは今回の生値を覆さないが、次版 cert では修正が必要である。

## 0. 指定資料の読了と固定

指定順を守って次を全文読了した。

1. `search/certs/d972_atype_v3_3_final_20260822.json`
2. `scratchpad/d972_atype_v3_declaration.md` と `scratchpad/d972_atype_v3_3_production.py`
3. `docs/状態.md` の裁定 1569〜1575 ブロック
4. 指定絶対パスの裁定簿、裁定 1563〜1575

対話帳は T-66 まで確認した。B4 A/B の未宣言部分、roof の停止線、`cross-checked` と Lean の格を混同していない。

| 対象 | bytes | SHA-256 先頭 16 | 結果 |
|---|---:|---|---|
| v3.3 cert | 4744 | `6dbd248ea85f4db3` | 一致 |
| v3.3 production | 13638 | `a972b0d50f8aa711` | 一致 |
| v3 declaration | 3767 | `ac18aabeea9a1f23` | 一致 |
| `docs/状態.md` 全文 | 33333 | `7d8d20cdea9a4142` | 一致 |
| 指定裁定簿全文 | 426165 | `c9a0ef53d4d916c1` | 一致、1563〜1575 が連続 |

## 1. A1 — v3.3 cert と 12/12

### 1.1 witness と判定経路

群法第一成分

`m1 star m2 = 2*m1*m2 + m1 + m2 (mod 18)`

を独立に再計算し、free-word の reduction と abelianization も production の群判定とは別に再生した。得た表は次のとおりである。

| m | witness / route | reduced length | F2 abelianization |
|---:|---|---:|---|
| 0, 17 | `f=1` | 0 | `(0,0)` |
| 3, 14 | `W` | 8 | `(0,0)` |
| 6, 11 | `f''=(3,W) star (3,W)` | 100 | `(0,0)` |
| 12 | `f12=(11,f'') star (11,f'')` | 4632 | `(0,0)` |
| 5 | `f5=(6,f'') star (11,f'')` | 4600 | `(0,0)` |
| 9 | `(14,W) star (11,f'')` | 992 | `(0,0)` |
| 8 | `(14,W) star (6,f'')` | 992 | `(0,0)` |
| 15 | `(3,W) star (12,f12)` | 46832 | `(0,0)` |
| 2 | `(3,W) star (5,f5)` | 46604 | `(0,0)` |

第一成分は順に `3 star 3=6`, `11 star 11=12`, `6 star 11=5`, `14 star 11=9`, `14 star 6=8`, `3 star 12=15`, `3 star 5=2` で、cert の route と一致する。regression 6 本と新 route 6 本を合わせた集合は厳密に

`{0,2,3,5,6,8,9,11,12,14,15,17}`

である。q3 の実測 SHA-256 `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72` と pin は一致し、witness universe digest も `0df6216cb0a0f734d4556eda37def6f424b542d9432c9f6a723672c2b7c2befa` を再現した。

`gate4_closure=36/36` は、lambda 六類 `{1,5,7,11,13,17}` から選んだ登録済み 6 witness の **6×6 calibration grid** の閉性である。全 GT 候補宇宙の閉包列挙ではない。naive control の `25/25` も lambda=1 を含む 11 cell を識別力なしとして除いた 5×5 に相対する。この射程なら記帳は妥当である。

declaration と production の間に対象系の拡張はなく、v3.3 は v3.2 の predicate を変えず route と cert を追加している。positive `m=0,f=1`、(a) charming だが theta-false の二交換子積、(b) non-charming の隔離、(c) charming/non-GT-pair の拒否はすべて hard assert され、slot0 A/B は 72/72 一致、mismatch 0 である。これらは同一 production 内の control trail であり、第二判定系とは数えない。

### 1.2 格と修正要求

**F157-1**: slots 1–4 は system B のみ、slot 0 は A/B 72 cell 一致である。従って `candidate, single-system at slots 1-4` は正しい。`system A has no slot1-4 formulation -- structural constraint` は「**現行 system A / 現行 instrument には**定式化がない」と限定する。数学的に第二定式化が存在し得ない、とは読まない。

**F157-2**: `pc_exponent3_exhaustive_check` は受領 PC 座標模型の `3^10=59049` tuples 全数に対する 0 違反である。q3 receipt と `Pi4[3]` の同定から独立な証明ではない。provenance としては適切である。

**F157-3**: production の spectrum guard

```python
sorted(known.keys()) == list(range(18))[:0] or len(known) == 12
```

は前半が `sorted(keys)==[]` となるため、実質 `len(known)==12` だけである。今回の実値は上の独立再計算と cert で正しいが、次版では exact set、route ごとの expected m、`charming`、全 5 slot、word digest を assert する。特に m8/m9 にも expected-m assert を置く。

**F157-4**: cert の theta 文言は狭める。`theta0([x,y])=[y,x]=[x,y]^-1` は正しい。しかし一般の `[u,v]` について `theta0([u,v])=[u,v]^-1` が自動的に成り立つわけではない。恒久知見は「基本交換子、または theta0 が二引数を交換する交換子は theta-false control にならない」である。二つの異なる交換子の積を destructive control に使った本走行自体はこの訂正の影響を受けない。

full production のローカル再走は 120 秒で終わらず打ち切ったため、再走成功とは記帳しない。上記は cert、固定 source、独立な軽量再計算、および既存 run trail の監査である。

**A1 裁定**: **GO / candidate 維持**。F157-1〜4 を次の versioned cert/erratum に反映することを条件とする。

## 2. A2 — P-972-2 と `N_ord=18`

`m` を mod 18 で取ると `2m+1` は常に奇数であり、単元条件は 3 で割れないこと、すなわち `m not congruent 1 (mod 3)` と同値である。従って admissible m は定義からちょうど上記 12 個で、欠 6 個は測定 FAIL でも UNKNOWN でもない。

12 個すべてが実現されたので、m 軸の射影は admissible set 全体に一致する。また `m -> 2m+1 mod 18` は各単元を 2 回ずつ取るため、`chi_vir` 像は `(Z/18Z)^times` 全体を含む。ここから得るのは像の到達下界と m 射影の完全性であって、各 m の f-fibre の大きさ、GT 全体の上界、side/shadow/pentagon の情報ではない。よって「欠 6 個も探索で排除した」「GT は 12 個だけ」とは書かない。

`N_ord=18` は、v3.2/v3.3 Engine が `ord(c)=18` と全 5 coface の `ord(x)=ord(y)=18` を hard assert している。さらに本監査では `search/check_d972_b345_q3_chief_v1.py` の別 PC collector と置換演算だけを用い、同じ q3 JSON から

```text
ord(c)=18
slot 0..4: ord(x)=ord(y)=18
```

を再現した。従って「二つのコード経路が同じ receipt 上で一致」は言ってよい。ただし falsifier probe の source/cert は積荷に保存されておらず、二経路は q3 入力と coface formula を共有する。よって **独立由来の二体系**や Lean の格ではなく、`candidate / same-input two-code-path consistency` と注記する。次便では N-order 専用 checker source、入力 SHA、slot order table を immutable receipt にする。

**A2 裁定**: P-972-2 の的中記帳を三限定つきで受理する。文言は「m 軸の admissible 12 剰余を全実現し、従って `chi_vir` 像が全単元へ到達」に固定する。

## 3. A3 — `IndependentPc.inverse()`

固定点の実装と q3 PB4 receipt から次を実測した。

```text
pc.n=10, len(_inv_gen)=6
unit coordinate 1,6: inverse succeeds
unit coordinate 7,10: IndexError(list index out of range)
```

最初の 6 marked generators は高次 4 座標が 0 で、各 `inverse_coords` は PB4 receipt の先頭 6 inverse rows と一致する。このため marked generator の負文字だけを評価する経路は発火しない一方、weight-2 coordinate を持つ一般元の inverse は純粋に crash する。v3.2/v3.3 の `safe_e4_inverse` は指数 3 の二乗を使い、この関数を迂回している。

固定点で `koubou158_L3_core_v1_1` を直接読む Python 14 ファイルを AST 走査した。exception handler があるのは M2 v4/v5 の `except RuntimeError` だけで、`IndexError`、bare `except`、`Exception`、`BaseException` による soft-FALSE 化はなかった。M2 v5 workflow も `set -euo pipefail` で nonzero を失敗にする。従ってこの直接依存グラフ内では **silent wrong 枝はなく fail-loud**、正常終了した run がこの例外を踏んで黙って行を FALSE にした証拠はない。ただしこれは全ての将来の外部 supervisor まで含む無限定主張ではない。

修理・再走の注文は次のとおりである。

1. 次版 core では `_inv_gen` を `pb4["inverses"]` の全 10 rows から作り、row 数 `n`、先頭 6 marked inverse との一致、左右 inverse law を全 10 unit で assert する。
2. unit 7 と unit 10 を mandatory destructive canary にし、例外も欠 row も terminal ERROR/UNKNOWN とする。
3. direct import graph に加え、subprocess/workflow wrapper の exit-code mapping、partial cert、log を走査する。missing row、duplicate row、途中書出しは PASS/FAIL に畳み込まない。
4. 修理後は旧 core を上書きせず versioned source とし、その core を使った依存 cert を再走する。旧正常終了 cert を自動的に新 core の証拠へ昇格しない。

**A3 裁定**: 現 triage を追認する。格は「固定点の直接依存範囲で fail-loud」。production fix と依存 cert 再走は未了である。

## 4. A4 — CV-9 三巡の制度評価

INC-15 は制度が機能した例である。第一巡の対象系差分で slot0 専用式の流用を止め、第二巡で 28/36 を数学的非閉性ではなく silent cap による偽陰性と切り分け、第三巡で witness route と語長爆発を launch 前に閉じた。結果だけでなく、`DIFFERENT -> conditional GO -> GO` と UNKNOWN の復権を裁定簿へ残した点を評価する。

一方、再現性を制度に埋め込むため次を追加する。

1. 各巡ごとに declaration/source/input digest、読了範囲、counterexample、判定を持つ immutable CV-9 receipt を残す。今回の falsifier probe source が配達物にない点は再現性上の欠品である。
2. 差分再判読は predicate、universe、入出力 schema が同一であることを manifest で確認した場合だけ許す。意味論 gate を変えたら全文再読へ戻す。
3. falsifier は production core/parser/evaluator を共有しない。少なくとも exact set、slot routing、UNKNOWN count、per-route word digest を別実装で照合する。
4. mutation suite に slot0 流用、cap 超過、print-only claim、非 GT-pair 合成、expected-m ずれ、指数的 word expansion を常設する。
5. CV-9 の GO は launch gate であって、それ自体を数学的格上げ根拠にしない。

**A4 裁定**: 三巡運用を採用する。差分方式は上の semantic-reset 規則と round receipt を条件とする。

## 5. work orders

### 5.1 WO-157-1 — D972 GHA 修理

`origin/master` の run `32575013338` は Ubuntu 24.04 で apt の `dmtcp` candidate がなく exit 100 だった。固定点では v2 workflow が既に DMTCP 4.2.0 の pinned source build、inventory、checkpoint/restart smoke を備えていたため、その経路を採用した。旧 `.github/workflows/d972-dovetail.yml` は削除した。

親 broker が branch `sol/157-d972-dovetail-restart` を作成し、次を push / dispatch した。

| commit / run | 内容 | 結果 |
|---|---|---|
| `2617bfd701009582e7075dd971a3e1980274f6e1` | 旧 workflow だけを削除 | run `32581574880`: source build、static tests、DMTCP smoke は PASS。campaign が legacy seed の旧 workflow binding を検出して fail-closed、artifact なし |
| `97d6bf657fff1ea20b00afd5d555346321c79e0f` | v2.1 fresh-genesis rebind を manifest/producer に追加 | run `32582162761`: `RUN_FINAL_STATUS_TBD` |

第一 run の失敗は数学的失敗ではなく、旧 workflow 削除と v1 seed binding の不整合を捕えたものだった。修理では既存 checkpoint を移行せず、`integrity.ready=false` の fresh genesis と旧 row 全体の exact match の場合だけ v2 workflow へ rebind する。precondition drift は `STATE_STOP`。successful predecessor artifact は 0 件なので、この限定は現状に合う。

最終 branch の固定差分は旧 workflow 削除、`search/d972_dovetail_manifest_v2.json`、`search/d972_dovetail_producer_v2.py` の 3 paths だけである。v2 workflow 自体は 32056 bytes / SHA-256 `86806791346ed4cf9063a7c4fefaaa2c3aa414decc32973a3b4efa5633a41d7f` のまま。新 contract は `d972-dmtcp-whole-process/v2.1`、digest `343ffe0b5c14d186b6e423c449048084c2b6a03e0e651c160a61810887f0c750`。master cron は branch 統合まで旧状態なので、統合時に supervisor bytes と test commit の到達可能性を保つ。

### 5.2 WO-157-2 — 83 checker v2

作成物:

| path | bytes | SHA-256 |
|---|---:|---|
| `crosscheck/check_koubou83_A2_full48_v2.py` | 31966 | `2d39246d51afbba07b3c7419016586da55e367d1cd18a222e90bdc4212a8426a` |
| `crosscheck/verdicts/koubou83_A2_full48_crosscheck_v2_20260823.json` | 220494 | `03a0f1c1e0f42b17bbc9e26e6f04b40311662fb8d7c45f3f5cc9442c5a70046b` |
| `scratchpad/koubou83_c3lift_check_v1_2.g` | 28353 | `5737dee0808b6117eb5438bf5acee1fcd218d61aaee2012d8ce3f62ed50c3f35` |

Python v2 を親側でも全走行し、192/192 coverage/legal/charming/direct、既存 controls、W-1 の正順陽性、旧 raw 順陰性、非中心 fixture、実行時生成 `ad_convention`、source SHA pin がすべて PASS した。`nu=0,1,2` はそれぞれ `identity, matches_adx2, matches_adx` と記録し、paper `Ad(x)` と GAP `u^x=x^-1ux` の向きを明記した。v1/v1_1 と旧 verdict は変更していない。

GAP v1_2 は stale comment を `{0,6}` / literal `u={1,13}` に直し、同じ W-1 gate と pin を実装した。ただし `gap.ps1` は source 読込前に `couldn't create signal pipe, Win32 error 5` で止まり、再試行でも同じだった。従って GAP v1_2 cert は存在せず、GAP 側 PASS は主張しない。WO の主対象である Python 次版は完了、GAP companion の runtime receipt だけ保留である。

### 5.3 WO-157-3 — P-GRT-1 凍結登録

`docs/notes/p_grt1_prereg_l7_w5_v1.md` を作成した。19125 bytes / SHA-256 `84a29afa11f16a21aae0e91b5eb1257737fb16030940322ba23b112d55cb1fc4`、canonical payload は 4050 bytes / `dc7ee417cb2dbfef3a813f62890766afbafb76dce886d0a6b1b693a5d0e57630` で、独立再計算と一致した。

宇宙は `ell=7`, weight `<=5`, `P=F2/(gamma_6(F2) F2^7)` の一窓だけである。marked Lazard/Hall presentation、`X=[0,1,2,4,5,6]`、LEGAL/full/reduced hexagon/SURJ、`K(0,5)/W5` の PENT frame、row key と exact-cover/UNKNOWN policy、char-0/mod-7 rank canary を payload に固定した。予言は `|GT(N)|/|X|=2401`, `|PENT_W|/|X|=49` のまま。群構築、rank、GT、PENT の測定は一切行っておらず、両 observation は `UNMEASURED` である。

## 6. 範囲外・成果物・規律

便 §4 の六項、すなわち W/pentagon 原典待ち、(iv)-w/M1、83 M1/M2/M3 と S7′、LEDGER 転記、Lean、独立 non-charming 空性タスクには手を広げていない。P-GRT-1 に後発測定を輸入せず、UNKNOWN を FAIL にせず、今回の数値主張を candidate から格上げしていない。

実装報告は `sol/luna_reply_157a_gha_repair.md`、`sol/luna_reply_157b_83_checker_v2.md`、`sol/luna_reply_157c_pgrt1_prereg.md` に残した。GHA の commit と run ID は §5.1 のとおりである。

最終条件は次の四点である。

1. v3.3 の theta 文言、single-system の相対化、exact spectrum assert を次版で直す。
2. `N_ord=18` の別コード経路を source/cert として保存する。
3. `IndependentPc.inverse()` を versioned 修理し、unit 7/10 canary と依存再走を行う。
4. GHA repair branch を master へ統合する際、passing run の supervisor bytes と source commit を保持する。

AUDIT_157_VERDICT: 条件付き受理
