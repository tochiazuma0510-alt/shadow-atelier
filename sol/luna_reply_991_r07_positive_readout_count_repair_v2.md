# Task991 — 実 original start count 修理と診断保存 v2

## F1. 実失敗と本便の範囲

Task991 を全文読み、Task989 の指定返信を完成・凍結した後に実施した。変更は新 `search/d972_r07_continuation_positive_word_readout_v2.py`、新 `.github/workflows/d972-r07-continuation-positive-word-readout-v2.yml`、本返信の三本だけ。旧 P982 / WF985 / 返信、P971 / continuation checker v2 は変更していない。新 D v2 の算術 source は読まず、root が中継した公開 ABI と実 bytes / SHA だけを使用した。

原 run33995799635/1、head920780033b3aaa519a898e8b6b1d29fe67a04cd1 は source / runtime と十六 live / whole ZIP を通過した後、accept の `positive_word_workflow:original-start-not-renamed` で停止した。P / D / canary は未実行、candidate はない。原診断 artifact9978026066 は 244085 B / e6565d625f42e9e3202a1faedc271ff07c5c6cfee9cc38558f879155312522b4。root が回収・安全展開した `%TEMP%/shadow-atelier-positive-readout-run33995799635-diagnostics-a1` の実小 JSON を読んだ。

| 原診断の実 file | bytes | SHA256 |
|---|---:|---|
| driver-accept-failure.json | 787 | 227a9b5138ec92d41c6b1d7c891722f19c4307c3f7fb6a9ba8adbf47caee687a |
| preservation-result.json | 871 | ec152f09f963f1118c30183399f697f63082389484ec80d6662bd029bf837b02 |
| all-parent-files-after.json | 234 | 59a3e3930478e177fec2731914bd8cef807df8c3c5a7e099b330564a20f14060 |
| source-receipt.json | 2245 | 498227a0bf21378f7351ad21cc21cce073762c7272dc257479ab963948c5f86f |
| workflow.yml | 84418 | 9e90bfeca6907fd71a4158308737a5a23677e3f2972b6e31391b5736b14bf36a |

原 preservation は before receipt 不在の INCOMPLETE。欠品は parent-paths / all-source-files-before と未開始 word / D であり、all-parent-files-after は count=0 だった。実十六 ZIP の取得成功を取り消す数学 FAIL ではなく、取得後の保存順序にも欠陥があった。原エラー・原診断・原 source は保存したまま新 version に進める。

## F2. 実 start 型と修理理由

実64親 `output/start.json` は 54707 B / 87bd9b89c593d68fba65b765bfe9f17bcc47d52cc9afce6f53f8c131a24f816b である。root 手渡し候補のこの同じ file を子も metadata 読取した。

| 字段 | 実 JSON 値 | PowerShell 読取型 | GHA Python 入場型 |
|---|---:|---|---|
| rank | 1386 | System.Int32 | int |
| generation | 8091 | System.Int32 | int |
| completed_steps | 0 | System.Int32 | int |
| external_e_attached | 1 | System.Int32 | int |
| external_e_numerically_replayed | false | System.Boolean | bool |

start が resume 基点へ改名されたという解釈は棄却する。同じ original start を消費し、別 path / 別 state に差し替えない。旧 P v1:835–837 / WF v1:795–796 の `external_e_attached is True` が整数1を拒否した箇所である。

新 production helper `validate_original_start_header` は前四字段について各 `type(value) is int` かつ実期待値を要求し、replay は `is False` を要求する。P の `read_selected_head` と WF の `authenticate_continuation` が各自この契約を呼ぶ。bool を整数として許す単独の `== 1` には変更していない。

## F3. 公開 P v2 と第四 canary

P は WORD_SCHEMA = `d972.r07.continuation-positive-word.v1`、八 op / ordered root / SLP / signed convention / mod54 / arithmetic / 全13出力 roster / 通常 CLI を保持した。producer/checker の source 入場 path を両 v2 へ移した。最上部説明を Task991 に更新し、二つの関数を追加した。テキスト上の既存58関数区分のうち変更は `admit_parents` の二 path、`read_selected_head` の header helper 呼出し、`selftest` の第四群接続だけで、残る55区分は同一である。これは AST 実行ではなく source 文字列の比較である。

P の `--selftest` は次の exact 四群、各要素は `name/status/rejected_cases` を含む。

1. ordered-word-same-root-mod54
2. target-history-positioned-readonly
3. raw-cycle-auxiliary-four-B
4. actual-start-header-count-type

追加群は実五字段型を canonical JSON / decode した metadata fixture で同じ production helper を呼ぶ。整数1の正例と、attached の `true / 1.0 / "1" / 0 / 2` の五逆対照、rank / generation の float、completed_steps の bool false、replayed の整数0の四逆対照を定義した。期待する拒否名は `attached-bool-true, attached-float-one, attached-string-one, attached-zero, attached-two, rank-float, generation-float, completed-bool-false, replayed-integer-zero` の順である。

追加群には `accepted_header`、固定した original start の `source_header_file`、`actual_parent_numerically_replayed=false` を記録する。これは五字段の入場 fixture であり、実親の数値証明書を再生したものではない。各 PASS 字段は実装上の成功時 return であり、本便で実行した結果ではない。

D は root から Task992 の path-only v2 として受領した。公開 `D_SCHEMA = d972.r07.continuation-same-word-eleven-slots.v1` / CLI / 三群 / 算術は不変。WF の D exact 群名は次のままである。

1. actual_nonunit_Act_inverse_typed_codec_endpoint_and_printed_order
2. same_root_EOF_mod54_and_resealed_Ref_word_key_mutations
3. actual_eleven_adapter_binary_JSONL_and_Linear_null_contracts

## F4. WF v2 の保存順序と公開 receipt

自身 name / marker / path / upload名を v2 にした。marker は `[r07-continuation-positive-word-readout-v2-run]`、wrapper 自身の schema だけ `d972.r07.continuation-positive-word-workflow.v2`。P / D / continuation の既存 wire schema は保持した。source pair の新 bytes / SHA と closure label P991-v2 / D992-v2 を接続した。

`sources` は source / raw / driver の実入場と GHA AST 後、accept より前に `source-files-before-admission.json` を保存する。四 source、四 raw、自身 WF の全 file pin、driver、source-receipt を束縛する。原失敗の実 run / head / diagnostic tuple / 旧 P・D・WF pin は `REPAIR_PROVENANCE` と `repair-intake.json` に記録した。原診断を新 runner で再実行したとも、成功親に使用したとも記録しない。十六親へ未指定の第十七親を追加していない。

`admit_live` は各 role の live API / whole ZIP / safe extraction 完了ごとに元 live-one receipt を保存し、直後に `acquired-parents/<role>.json` を保存する。後者は抽出 root path / artifact tuple / live receipt 全 pin / 全 file bytes・SHA / 全 directory roster である。抽出 root の全体は accepted consumer root と区別し、後者の代用にはしない。

`accept` は root 解決と実 scan の後、`parent-paths.json` と `all-parent-files-before.json` を `authenticate_continuation` より前に保存する。原 start の固定 pin / seal を読んだ直後に `original-start-header.json` を保存する。これは actual_start 全 file pin、expected_start pin、五字段の value と Python の `type(value).__name__`、`status=OBSERVED / header_gate_applied=false / start_replaced_or_renamed=false` を持つ。その後で入場の strict header gate を適用する。OBSERVED を合格票と扱わない。

数値入場・fresh rho2・P1・accepted legacy checker の gate を全部通ってから、従来どおり WORD v1 acceptance と最終 `all-source-files-before.json` を作り、全親・source・raw・acceptance・driver を read-only にして admission PASS を公開する。

## F5. always の未完・不変の境界

`always_preserve` は存在する各 extraction の actual after を先に採り、その後で対応する acquisition before / live receipt と比較する。role 単位で例外を記録し、他の取得済み role の採取を続ける。`acquired-parent-files-after.json` に実採取数、期待数16、各全 inventory と `unchanged_from_acquisition` を残す。live 途中の不足や before 欠品も INCOMPLETE の理由として残る。

accepted consumer root の実 after も role ごとに採り、before 読取を後に行う。`all-parent-files-after.json` は取得できた全 rows を保存する。source / raw / WF の actual after と driver も final before / acceptance の読取前に採取する。早い source baseline が揃うときの `acquired_sources_unchanged` と、全 source / raw / acceptance / driver の最終不変判定は別字段である。acceptance 欠品を source の早期一致で補わない。

word / D は作成済み範囲を全 file / directory roster で保存する。欠品または採取失敗は `INCOMPLETE_OR_NOT_CREATED` とし、word-before-D がなければ「Dによる不変」を true にしない。既存 `driver-*-failure.json` の全 file pin も preservation-result に残し、元 accept failure を上書き・隠蔽しない。

preservation のエラーが一件でもあれば `status=INCOMPLETE` を保存して非零終了する。成功側の `finish` は従来の全16 before / after 一致、source / raw / acceptance / driver 不変、P出力のDによる不変、P/D各一回 exit0、全13 P file / D完全 manifest / 同 root・同 normalized pair / 全80644座標 / 十一 slot / exact rho2 を引き続き要求する。run receipt に修理 provenance と header / early source receipt の pin を追加した。candidate upload 条件は緩めていない。

## F6. 維持した実入力と型の追加検索

continuation は実64の run33990567016/1、headc57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70、artifact9977040548、304642285 B / a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792。元 original start rank1386 / gen8091 / count0 と、現在 HEAD count64 / rank1450 / gen8155 / Separator / UNKNOWN_CAP の区別を維持する。現 target の非零に対する positive NOT_APPLICABLE を変更しない。新成功親や未完 run を先取りしていない。

旧 WF と新 WF の `ARTIFACTS` JSON 全16 tuple、`COMPLETION_ENTRIES` 10 pin、`CONTINUATION_ENTRIES` 30 pin は文字列を含め同一である。owner / source / start / fixed、fresh rho2 全 body、三 source dictionary と chief raw、retained C9 / C4、全 runtime、既存 input admission / safe extraction / P/D CLI を保持した。source/data の型や数学の修理は加えていない。

P / WF の `is True / is False / external_e_attached` を静的検索した。新 source に attached を bool とする入場は残っていない。WF が読む実 continuation checker の次の九字段も、元候補小 JSON で全て System.Int32 と確認し、既存 `== wanted` に `type(value) is int` を付けた：section_equalities_each=8059、chords_each=54433、auxiliary_tests_each=2、source_lower_trits_each_E=96776、literal_modulus=54、external_e_attached=1、old_scans_numerically_replayed=0、old_inserts_numerically_replayed=0、old_success_suites=0。他の EOF / source equality / all-compared 等の boolean gate は維持した。

## F7. 公開 CLI と GHA 上限

P v2 通常 CLI は `--state-root --delta-root --seed34-root --packet-root --refinement-root --oracle-root --e-root --prepare-root`、owner順四回の `--block-root`、`--p1-root --task712-root --continuation-root --rho2-root --acceptance --output --max-seconds --max-memory-mib`。通常 P の二資源値は正整数必須。P selftest は `--selftest --max-seconds 300 --max-memory-mib 7168` を wrapper から渡す。

D は公開 ABI の同16親と acceptance に加え、`--word-root --output --producer-max-seconds 5400 --producer-max-memory-mib 7168` を取り、自身の `--max-seconds 10800 --max-memory-mib 7168` を wrapper が渡す。D arithmetic source は読んでいない。

GHA は Python `3.13.15 (main, Aug  6 2026, 02:15:18) [GCC 13.3.0]` / NumPy2.5.1 の全文一致、memory7168 MiB、job330分。P/D selftest 各内300秒・外360秒、合計外12分、P内5400秒・外6000秒、D内10800秒・外11400秒である。GNU timeout の TERM と kill-after の合計が各外枠に収まり、driver は os.execv で consumer に signal を到達させる既存構造を保持した。これは上限であり速度や完了の予測ではない。

新 source AST / 新P四群・D三群 / 本P一回・D一回 / complete same-root比較 / always保存の実走は root / GHA のみで行う。旧数値成功 suite の再走は追加していない。GH_TOKEN は live download の process 環境だけに置く既存構造を保持した。root が一回の release と run id / launch / actual artifact を別途記帳する。

## F8. 静的確認と最終 freeze

新 P は二 helper 追加と既存三関数区分だけの metadata / canary 差分。WF は二 header 関数の追加と sources / admit_live / authenticate_continuation / accept / check_canaries / always_preserve / finish の変更、定数・selftest名・YAML identity の更新である。driver の残る23関数区分は文字列同一。execute / record / safe extraction / root 解決 / word / D full comparison の算術・公開 gate を新実装へ置き換えていない。

Task993 は新 P 全差分と WF 全変更関数・成功 finish・YAML tail を静的に読み、現版に追加必須修正なしと通知した。子も実 file bytes / SHA / LF / CR / BOM / finalLF / 行末空白を確認した。旧 P173286 / f5b35c56…、旧 WF84418 / 9e90bfec…、Task989返信28738 / 6dc50eed… の不変を metadata で再確認した。ローカル AST / import / Python / numerical execution / GAP / network / git / credential / new agent は行っていない。

| 凍結 file | bytes | SHA256 |
|---|---:|---|
| search/d972_r07_continuation_positive_word_readout_v2.py | 175318 | cf6ac987acb2f399f36a8438cca78b773d7791286473b68362f2824a35d6451c |
| .github/workflows/d972-r07-continuation-positive-word-readout-v2.yml | 92986 | 47043063db8e330210a29594cb8b91900a40c0750f651b2647c2101047bc8477 |
| search/check_d972_r07_continuation_same_word_eleven_slots_v2.py（Task992・root手渡しpinのみ） | 176579 | 865ed6a50b95303fdecafbc69e841da018858aa4624467fb17cdf80a0beadfd1 |

P は LF2873、WF は LF1444、どちらも CR0 / BOMなし / finalLFあり / 行末空白0。D は source を開かず全 file bytes / SHA のみ再照合した。本 P / WF はここで凍結し、根拠ある修正が必要なら root に通知してから扱う。本返信の全 bytes / SHA は自己参照を避け、完成後 root / Task993 へ別途通知する。

## F9. 結論と残る実走

要求された型修理、production helper に結ぶ新 canary、両 v2 source pin、失敗時の取得済み保存順序を実装し、静的差分の限定性と実親 metadata の型を確認した。本便の判定は IMPLEMENTED_STATIC_DELTA。新 GHA AST / P四群・D三群 / 本P・D / preservation 成功 / 工房CV9 は未実行であり、成功と記録しない。原の入力型拒否を閉じる source 修理と、新算術の実結果を区別する。verified=false、同語・grade2・A0の新しい成功主張はない。

AUDIT_991_VERDICT:
