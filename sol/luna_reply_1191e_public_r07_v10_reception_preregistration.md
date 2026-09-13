# Task1191e — V10 公開受領の静的事前登録

Noether / receiver_cost_repair。実 artifact を待たず、Task1190 の O01〜O12 を V10 の公開 caller と必要入力へ接続した。新 receiver の実装・実行は行っていない。P/C 私有本文・私有差分・数学 fixture 本文の読取、archive decode、対象 import/AST/compile/selftest、Git/GHA/network はすべて 0。

固定対象は run **34731988156 / attempt 1**、head **785bd2d87f2b97452a7f0deb2085afe4e7e56d95**、workflow ID **356853218**、job **103656346430**。観測の正本は root-v10-run34731988156-first-observation-v2.json。2026-09-13 02:14:25.474425 UTC の時点で step 1〜13 success、step 14 は 02:11:11 UTC から in_progress。これは実保存 P/C result、自己検査各 case、終端 inventory の受領ではない。

WF は `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v10.yml`、name は `d972-r07-fixed-lambda-cycle-batch-v10-envelope-v1`、marker は `[r07-fixed-lambda-cycle-batch-v10-envelope-v1-run]`。採用済み source は変更していない。

| runtime file | bytes | SHA-256 |
|---|---:|---|
| search/d972_r07_fixed_lambda_cycle_batch_v10.py | 1034265 | 33c4bbb97313bc1ea2017b6ac6ad2cc0932ae15d1affc8bcd6a8aaedd0c76085 |
| search/check_d972_r07_fixed_lambda_cycle_batch_v10.py | 870249 | a21fd2b54958f84ea67e7b3a079893cff70544961005d6c79a0f6ff47e752ca8 |
| search/d972_r07_fixed_lambda_cycle_batch_v10_workflow_driver_v1.py | 32326911 | acf206e5fe423288f3449e5e034a1bd125a6c203e6c274b64f41fc36ab94c802 |
| .github/workflows/d972-r07-fixed-lambda-cycle-batch-v10.yml | 47555 | 88856a3329ccb59750c427fd27ba6857d89953b75a65f93a11f260783f67f34a |

4 source は Task1191 manifest-v2（10391 B / 5420bd1d20c10d71a8eb41d0e2b78c23ca67ac4e0b3044895dfce20b7e626054）と root 最終 closure（15447 B / 67844e92b012f7e4f7125c7a2a70a2ed26dbaae7246858e352aec90bbfba5613）から束縛した。P/C 本文は開いていない。裁定2296の4者配置一致・実発射の記帳と、今後の実受領を区別する。

提出物は `%TEMP%/shadow-atelier-audit163/task1191e/public/` に CreateNew で保存した。旧稿は保持し、採用対象は次の組合せとする。

| file | bytes | SHA-256 |
|---|---:|---|
| public-input-preregistration-v2.json | 26502 | bf2317f9504795d32287f07ebc2cc03dd4ae43218609deeddad9db1e60276d03 |
| public-O01-O12-obligation-preregistration-v3.json | 38252 | 559a12924a26ddb831cf7e91c55e7611f9ffa381dd9c5815a23d1eda7e2e6f7c |
| public-raw-range-connections-v3.json | 39620 | 1812976e05889eff4b89a7078400ca050bf972bd0d834608cac4b5b80966c2a7 |
| public-old-receiver-required-deltas-v2.json | 20709 | 521982130cb80cd9cc2680041f62f7461df95cbec57eae26eedbe2144eb7f6b3 |
| public-static-selfread-and-input-closure-v2.json | 6412 | 51afcd54dc08a5c81c7d2fb63919ca71c3a29a01adb274ea8c7ebfa94e41ec26 |

最終 manifest は同じ directory の `public-final-material-manifest-v2.json`。本返信を含む実 D3 を別に保存し、自己参照 hash は作らない。

O01〜O12 の全文表には、旧義務、担当、必要な保存名・field、公開 driver の実 offset/bytes/SHA、旧 helper の正確な raw 範囲、未着入力を収録した。担当境界の要点は以下の通り。

| 義務 | 保存入力と担当 |
|---|---|
| O01 | run/head/source variant と実 artifact・原 host は root が供給。public は固定入力を比較する。 |
| O02 | whole ZIP/EOF/CRC・完全 model は root。public は許可した metadata の全 raw と model D3 を結ぶ。 |
| O03 | source-before/receipt/after、8 registry、audit receipts、F2/F5、WF copy。実 source/物理由来は root、保存値比較は public。 |
| O04 | 5 label の execution start/result、全 argv/runtime/caps/log D3/native。完全 checked_execution は実成功枝だけに使用する。 |
| O05 | parent-timing/outer/{stage}/{ordinal:02d}-{role}.json の登録59名を全列挙。未保存を P/C 内側件数から補わない。 |
| O06 | ordinary の原 stderr・completed_intervals・registered_measurements。P/C が内側を受領し、root が各 status と joins を採用する。 |
| O07 | authentication と native operations は別 wrapper。P/C 別 scope・null/partial/FAILED/observer error を維持する。 |
| O08 | phase manifest/telemetry、cost inputs、signed residual は public。candidate/row/payload の数学は P/C と root。 |
| O09 | 22 親 acquired before/after、7 transport/restoration/fixed-reference。元 archive と directory 由来は root。 |
| O10 | preservation、入力 freeze、4 input inventory raw、P/C input_preservation exact9、fixture/output inventory。fixture 本文は P/C/root。 |
| O11 | P/C 各受領 status、全参照鎖、自己検査全値、F5 実2子を root が採用。public の pin 一致で代行しない。 |
| O12 | run-receipt/current/null と元終端を保存。完全 inventory/formal5/CV9 最終判断は root/Sol。 |

V10 の current 22 親・n=7、16 量・15 keysets は実 current table（12401 B / 6f92e487d6190ac36c00b40392a1082d9854032af4fbade4f2e30d9ad7126c00）から導出した。登録量は previous768 / total896 / ancestry993 / rank2346 / generation9051。親履歴の phase5376・checkpoint5404 と、新128候補が実際に完全形成された場合の phase772 / cost776 は別の量である。native-v9 の旧6層・21親・640/768/865 と current7層を混ぜない。

F2 は宣言の purpose を ROOT_STATIC_REVIEW_PROVENANCE、contents-read と byte-monotonicity の主張を false のまま保存する。shared-tcb の current_execution_edges は宣言であり、実 child の代用品ではない。

F5 は `--key-contract-selftest` と `--selftest-parent2346-contract-child` の2辺を登録した。親 selftest は元300秒のまま、同じ `--key-contract-parent-deadline`、同一 P source/full registry の前後 D3、実 Python argv0 と環境 key 制限を各実 receipt へ結ぶ。旧第8群の完了を第9群の前件とし、追加300秒や第3の数学的独立性を導入しない。実2子の受領は P/root の義務である。

F7 は cost.context の `new_batch_parent_and_adapter_added` と run の `selection_lambda_oracle_is_separate_from_new_final_lambda_oracle` を固定文として保持する。run の追加3欄は `accepted_batch_anchor_v9`、`batch_parent_v9_restoration`、`batch_parent_v9_envelope_intake`。実値または null を保存し、既存18 flat fields の大型移行は行わない。current batch_observation は形成時 exact7 / old_side_recomputed_in_this_run is False、歴史 native は exact6、未形成 whole-null を保持する。

F8 は original WF と report/workflow.yml、driver-placement-before.sha256 / after.sha256、前後の regular/no-link、full raw cmp を実記録へ結ぶ。5個の WF raw 範囲を登録した。`envelope-inventory-before-run.json` は run receipt と自分の inventory control を作る前の scan であり、終端完全 inventory や formal5 へ昇格させない。

旧 helper の必要差分は16項に限定した。主な値差分は run/source/authority pin、registry7→8、非実行 history16→18、親21→22、transport等6→7、完全形成時 preservation flags38→40（11+22+7）。code union は24=21 executable+3 raw のままである。旧 helper が実成功・128完了へ固定されていた条件は、未受領の V10 へ転記しない。actual root の枝判定後にのみ利用可とし、失敗・未開始・partial・UNKNOWN はそのまま残す。陰性残差、未測定 null、inclusive/exclusive の区別も保持する。

旧 phase helper の Pauli 依存は、V9 では root が C1190 の実128鎖/768参照で代替採用している。これは V9 の過去事実であり、新 V10 の鎖には新しい P/C/root の実受領が必要である。

静的自己照合 v2 は metadata read/hash/JSON のみで実施した（24efd5/native0）。現 public58関数、旧18 raw 範囲、WF5範囲の全81範囲と、入力票に重複した3 caller の byte長/SHA/物理的な包含行番号を照合した。全12義務の参照、outer59名、22必須実入力の null、静的入力の fresh 前後一致を確認した。原 source/WF/旧票に変更はない。新 helper・receiver は作成も実行もしていない。

実 artifact ID/name/ZIP D3、実 root path/model、終端 conclusion、P/C result、原 execution status、各実受領票、完全 inventory/formal5、CV9、新 λ2346 oracle 等の22必須欄はすべて null。59個の timing file の actual D3 もすべて null である。未来の成功・件数・数学結果は記入していない。これらは本作業の未完了ではなく、実 artifact 取得後に root から受け取る次段の入力である。

表示行番号の正誤を追記する。root helper166540/diagnostic08c8dd は audit_material_bindings の offset18593831 / 7719 B が末尾 LF を含まず、実包含最終行5901に対して旧表示5900であることを発見した。旧自己票9fb011は同じ計算式を再使用しており、物理的包含行番号の照合にはなっていなかったため、この部分を v2 自己票で置き換える。

全81範囲について `line_last = 1 + LF_count(raw[:offset + bytes - 1])` を使用した。末尾 LF を含まない current58範囲の line_last を各+1、旧18範囲とWF5範囲は値を保持した。同じ表示値を持つ入力票の count/F2/F5 caller3箇所も各+1とした。offset・bytes・SHA・source D3・line_first、O01〜O12の責務、必要差分16項、固定値と実入力 null はすべて不変である。

正誤票 `public-physical-line-display-erratum-v1.json` は41008 B / 7ae3bbd8fc74b91d914333df6023d5797e88c874c625463c46190804b9d78bb5。81範囲+重複3箇所の全確認と、入力・map・義務・差分の4 JSON の全変更を正逆適用して原 canonical raw と一致させた記録を収録した。旧返信8826 B / 1a305258334ba3ea2e2bd8edc62bb1cdd986590ce3892e33e2ae87dcc278705b は TEMP の `reply1191e-public-before-physical-line-erratum-v1.md` に原 bytes のまま保存した。これは metadata の表示と束縛の訂正であり、target/source/WF または数学条件の修理ではない。

AUDIT_1191E_PUBLIC_VERDICT: STATIC_RECEPTION_PREREGISTRATION_COMPLETE_ACTUAL_ARTIFACT_UNOBSERVED
