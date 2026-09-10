# Luna reply 1151 — P7 ordered_reductions 静的計器納品

**F1 — 納品。** Task1147 draft03（536780 B / `91ac102990f56dee8f05a369edbbe8e30d115d537de4f66b7324191927a6e8fe`）を保存し、新しい未実行 P7 draft02 を作成した。正本は `%TEMP%/shadow-atelier-audit163/task1151/draft02/d972_r07_fixed_lambda_cycle_batch_v7.py`、**544642 B / `a47d978ffd5b1504b55828b6ee26b72bb52b53cd5539e11b71a1527df9fd2b68`**、ASCII・8044 LF・CR/BOM なし・末尾 LF。以下の材料は同じ task1151 直下。納品 manifest は **12178 B / `033b6a56b162282002655547f76def0b2a77f22481c4dc82361e4f28d3031a23`**。root は draft02 全差分・observer 全行・4 通常 reader 接続を別読し、source finding なしと報告済み。root の正式 binding・発射をこの便で代行していない。

**F2 — 実読 scope。** 通常再認証の `batch-parent` / `batch-parent-v4` / `batch-parent-v5` / `batch-parent-v6` の4層だけに observer を接続した。active root と `output/candidates/<6桁>/reduction/reduction.json` の完全一致を使い、元 `read_json` が成功して返した実 list の `len` を加える。phase payload と専用 saved-row の重複 parse は実 occurrence として加算し、unique path と repeat を別 field に出す。rank から予測せず、追加の file/array 走査をせず、current v7 候補へ広げない。

元の `batch_saved_full_ordered_reduction_ancestry` 判定が成功した直後に型走査窓を開始し、全 event の元 key/type/ordinal 判定を通った後、同じ candidate の manifest 読取入口で閉じる。その時だけ直前に parse した実 list 長を型走査済みとして加算する。元条件・4 saved-row reader 本文・元例外を保持した。未完の loop を完了数へ入れない。

`read_parse_elapsed_seconds` は元 safe_file/read_bytes/json_bytes/任意の generic seal と境界 hook の小さな overhead、`typecheck_elapsed_seconds` は元 full element loop と境界 overhead の、互いに重ならない成功窓の和。caller の後続 native seal、前段 row hash/target 処理、後段 source/lead projection はその窓外。`elapsed_seconds` は最初の対象 read から最後の観測終了までの間隔で、窓間の隙間を含む。FAILED prefix では対象 read の例外出口まで含み得る一方、成功窓の和には失敗 read を足さない。UTC は内部秒単位、秒数は内部 monotonic 差。stderr 到着時刻を使わず、既 inclusive parent interval へ加算しない。overhead の内外は `public-P7-ordered-telemetry-delivery-notes-v1.md` に明記した。

**F3 — 公開 wire と失敗。** 新 schema は `d972.r07.fixed-lambda-cycle-batch.v7.ordered-reductions-timing.v1`、side `P`、stage `saved-batch-ordered-reductions`、ordinal 0..3。公開票は exact25 全 key・ordinary integer/有限秒/nullable 型・書込位置・4 layer の呼出を収録。元 parent-timing の exact12 writer raw と29本の stage/role/ordinal/order を保持した。両 timing schema に絞った完走順序は旧 inventory 0..18、旧 continuation native 19、新0→旧20、新1→旧21、新2→旧22、新3→旧23、旧 state 24..28 の33本。他 progress stderr はこの本数に含めない。

`COMPLETED` は観測 scope が閉じた意味で数学 PASS ではない。元 reader が例外なら `FAILED` と観測済み prefix を残し、元例外を bare raise する。計器異常は最初の成功 parse 前でも `OBSERVER_ERROR`。成功 parse のない正常終了は `NO_OBSERVATIONS` で未観測 count/秒は null。未開始、process 中断、計器初期化/出力失敗では missing を保持し、0・完了 event を合成しない。計器初期化失敗でも元 reader を継続し、finally で前 observer を戻す。未完/observer error の公開型を維持する。C は独立 scope/schema であり、P の個数・窓との同一性を主張しない。

**F4 — raw と全 consumer。** 全200領域＝193 raw 同一＋4変更（MODULE / require / read_json / authenticate_acceptance）＋3追加。正逆 delta は source 全544642 B と baseline 全536780 B をそれぞれ EOF まで復元した。登録37 bodies・4 old loaders・25 native v3/v4 readers の全66区間、4 saved-row reader、旧 timing writer、全 canary/selftest 設計 scope は Task1147 から raw 同一。全22 embedded constants・792 key/type も同一。元 metadata 履歴を残し、current P7 の実 offset/pin を更新した。

全10866 literal・1443 dynamic＝12309点を source raw 範囲へ結んだ。旧12234点は pin 済み Task1147 の各 ID 契約と対応し、新75点は origin/type/control/呼出を個別に明示。退役旧点は task 名の docstring 1点だけ。7領域の意味と global observer の有効範囲は手読 overlay に記し、regex 集合だけを意味の照合と扱っていない。現在の source self-pin に依存する生成 JSON の metadata 差は継承契約どおりで、旧 physical fixture bytes・数学 scope・case labels を変更していない。

| 材料 | bytes / SHA256 |
|---|---|
| `public-P7-ordered-reductions-wire-and-order-v1.json` | 33520 / `3af07299598d531e2b0567f66cb7f1792b9edf10ae73c07cace1ab8b10e35017` |
| `public-P7-ordered-telemetry-source-and-ranges-v1.json` | 282907 / `bd259e803d0490082c871511c02adedf1ca1000564fae6da13bd6d2ce689d7c2` |
| `private-P7-ordered-telemetry-full200-forward-reverse-v1.json` | 1634987 / `bfcc7209daeea0afc3f15bbbfcd4b0ce0b476542a4e70467521656c6a4f545ce` |
| `public-P7-ordered-telemetry-consumer-overlay-v1.json` | 9773 / `071332adc86eecf4cd0bdc8819d5a7d6288534a1ce8ed56e5af070b8635cafec` |
| `public-P7-ordered-telemetry-all75-new-point-decisions-v1.json` | 71749 / `76ac1075a994780dc45bc39f1af187357e4f71a35acd0485d6810f16f002841b` |
| `public-P7-ordered-telemetry-consumer-static-closure-v1.json` | 3627 / `a6952f46f4190254abff3cd3e25733bf1383d7798648a9aace450c0ba1e820d6` |
| `public-P7-ordered-telemetry-static-final-consistency-v1.json` | 5033 / `2e0abc47a70f4f1383faf1d67ea28453ba24d0540f08abea6cbf77b7a4e91e3e` |
| `P7-ordered-telemetry-static-delivery-manifest-v1.json` | 12178 / `033b6a56b162282002655547f76def0b2a77f22481c4dc82361e4f28d3031a23` |

全 per-ID2票、embedded792票、4境界票、全材料26件と継承元15件の実 pin は manifest に収録し、保存後の再読で全件一致した。private delta/source を C に渡さず、root が公開 wire/scope を渡せる形で納品した。

**F5 — F-v6-3/4 と未実行の境界。** current CLI の `production_requires_exact_nineteen_roots_acceptance_and_output` は本 source L8011、main 全 raw は Task1147 と同一。歴史 P6 は変更していない。C4 raw、caps、k128/no-refill、19親/native18/17/16/15、数学宇宙、P/C 著者分離を保持した。新 source の import/AST/compile/数学実行/selftest は一切行わず、実測 count/秒も未取得。旧 selftest は設計の raw 継承だけであり、旧 PASS をこの binary に移していない。最終本走 binary の実 selftest と計器実測は後続 root 実行の仕事。

裁定2244により native rank1962/gen8667 は同じ限定7条で cross-checked と正式受理済みだが、lambda1962 oracle・A0 actual0/1・verified=false は従来どおり。この便で新しい数学成立条件や承認待ちを加えていない。`BATCH_V6_INVENTORY_REGISTRATION` は L759/token offset38917/4 B の `None`、`IMPLEMENTATION_COMPLETE` は L761/token offset39049/5 B の `False`。formal5 は root の実受領後に別途 binding する。新 agent/Git/GHA/network/credential/C private 読取/live process 操作は行っていない。

AUDIT_1151_VERDICT: AUTHOR_STATIC_DELIVERY_COMPLETE_GUARD_CLOSED_NOT_EXECUTED
