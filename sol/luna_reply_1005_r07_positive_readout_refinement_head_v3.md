# Task1005 — 正語 P v3 / WF v4、refinement HEAD schema 修理

## F1. 読了・保存境界

Task1005 と Task1004 を全文読了した。1005 の指定新 P・新 WF・本返信だけを変更する。旧 P/D/WF と公刊返信は不変であり、D 新本文・新返信は読まない。ローカル Python/import/AST/数値/GAP、network/git/credential、追加 agent は行わない。

Task994 は source 124674 B / 94088f9eade39f3d7a89440c2e89e74c08b13f15721902fcc27a1b07a494a368、LF 2076 の未凍結保存境界で保留する。private checkpoint・E phase・DERIVED・final payload と public_head_value まで保存済み。残る全 prefix loader / durable recovery / inputs・invocation / final publication orchestration / result・CLI / 三群 canary と最終凍結は未完成。996 の saved_selection_values nested bool 型指摘は strict ordinary int/trit 修理後に作者が再読し、解消済みと通知した。新たな未解決996必須指摘は受領していない。Task1004 の完成済 resume は全入力・全保存・HEAD/result 結合を認証後、既存 result bytes をそのまま返し、新 invocation/result を書かない契約として994へ戻った時に接続する。

## F2. 実失敗と修理の根拠

run 33999045563/1、head a324e4b44e3d24def59c901f2dbee758f04369fd の実診断を読んだ。P-stdout.json は 510 B / c6c1da75f292f8978a79564a0597b7db30547afe0f05b583cbca0d005895ab13、FAIL、KeyError:'target_remainder_sha256'、elapsed 19.929537、最後の progress は base-record-closure。旧 progress は実例外行を指すものではない。全16親、source/raw、20拒否の新 inventory 群、P4/D3 interface 群は実 PASS、D 本走は未開始。preservation-result は全取得親/source 不変で、word/D 未作成の二件だけ INCOMPLETE。

既に保存されている成功 completion の実 refinement output/HEAD を再読した。921 B / 6bf3b4fce6a3f159563c13a9aa50f6478827fbad1af13d820b70359b3b2f5cba、schema d972.r07.full-origin-refinement.v1.head、completed_steps=26、rank=1385、generation=8090、kind=Separator。target_remainder_sha256 は存在せず、step_manifest_sha256 は 1bfd33af5054a11b8210781146a872e914acb1bd7214b0b945f7e3520b31200c。旧 source head_record の定義と一致する。seed30/seed34 は既存の legacy=True 呼出しを保ち、その分岐が読まない flat key を原因とはしない。

## F3. P v3 の完成差分

新 P は旧 P v2 の本文を継承し、次の範囲だけを変更した。

- current producer/checker の入場 path を P v3 / D v3 に更新。語の schema は d972.r07.continuation-positive-word.v1 のまま。
- validate_refinement_head は実15字段を exact keys で読み、schema・inner seal、全六 binding、ordinary int の count26/rank1385/gen8090、Separator/null scan cursor を確認する。bool/float は整数として受け入れない。新 target 字段を後付けしても拒否する。
- read_refinement_parent は実 source/start/owner の全 seal と whole-file pin、packet manifest/owner、canonical index、元 start1359/gen8064/全6 target親、旧 terminal result/HEAD を結ぶ。HEAD の実921 B pinも保持する。
- read_target_history は旧 base、legacy seed30/34、packet3段、refinement26段、external E、全保存 continuation を従来通り読む。全26 manifest/payload/target差分/祖先を読み、各 refinement の schema、owner、packet、index、rank/generation を確認する。末尾では validate_refinement_terminal が HEAD と最後の manifest・instruction・result・target-remainder.bin の同一性を結ぶ。HEADへ無いtargetを作らず、最終targetの条件を省略しない。
- 旧 target 更新係数、挿入順、零係数、literal word の作り方、P1/source/physical の演算、13 output file、11 slot/80644 座標への公開契約は変更していない。

最後の実 manifest は 1932 B / 1bfd33af5054a11b8210781146a872e914acb1bd7214b0b945f7e3520b31200c。instruction は 147304 B / db5327c34a6447220a4309bd4f606a9372849977221bb1c290730c53df52ddc9、result は 151584 B / 45588d8b319fe4c3497bb9ae6d7768119711aa2c8779779945bdf5fcbf78edd7。target は 12096 B / 111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad、係数1、親 target5cb563ec85586ff7653ded61edb51dfb8748576a8e42d92323625552b5c96427。全26段の最後の state は8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61。旧 terminal.lambda_rho2 と最後の separator.lambda_rho2 も実全辞書一致した。

Task1008 を全文読了し、root 公開実表と自己読取した保存 completion の metadata が一致した。root は全 ZIP 51943596 B / 0d4af3475ca62da1d7436246bd36109d380e0a463a713de1c1e3db69f90c9db8 を取得・照合したと通知した。こちらは network取得せず、保存済み実 files の読取と whole hash を行った。

## F4. 同じ本番 helper を通す第5群

selftest に actual-refinement-head-last-target を追加した。保存親を変更せず、実 HEAD15字段・実最終 manifest全文・実 instruction17字段/result14字段の小さい射影・三 payload descriptor を source 内の metadata fixture とした。これは旧全26段の算術証明書や再走ではない。本番は大きな instruction/result全bytesと seal/rolling chain を認証してから同じ字段を射影し、fixtureと同じ validate_refinement_terminal に渡す。

31拒否は schema/count(bool・floatを含む)/rank/gen/state/last manifest/kind/current scan/不存在target字段追加、六 bindingの変更、inner seal破損、replayの最終/親target、instruction/result/payloadのtarget、bool係数、payload長、instruction file hash、rolling state、result rank型、最終step型である。元 fixture bytes の不変と再受理も確認するコードを保存した。HEAD seal は該当する逆対照で再計算し、単に破損 seal だけを拒否する試験にしていない。manifest の全 seal/hash も照合し、元の bytes は変更しない。

公開 selftest は同じ .selftest schema と tests:[{name,status,rejected_cases,...}] を保つ。P群は以下の順で5件、D群は公刊ABIの3件。

1. ordered-word-same-root-mod54
2. target-history-positioned-readonly
3. raw-cycle-auxiliary-four-B
4. actual-start-header-count-type
5. actual-refinement-head-last-target

第5群は production helper名、実HEAD pin、実最後のmanifest/target pin、head_fields=15、target_field_in_HEAD=false、actual_parent_numerically_replayed=falseを返す。WFが全31拒否名の順序を含めて照合する。新群の実PASSはまだ観測していない。既存P4/D3とinventory20拒否群のPASSは run33999045563/1 の実績であり、新版8 interface群の実績とは区別する。

## F5. progress と旧schema再点検

read_target_history の境界に history-selected-continuation、history-base、history-legacy-delta(role)、history-packet-step(step)、history-refinement-parent、history-refinement-step(step)、history-refinement-complete、history-external-E、history-continuation-step(step)、history-continuation-final を置いた。エラー時は通常の traceback を stderr に保存する。locals captureや環境変数値の列挙を行わない。stdout の diagnostic schema と FAIL/UNKNOWN_RESOURCE exit1/3は維持する。

後続の read_loop_step、TargetHistory.add_delta の legacy/plain 分岐、P1/Task554 loader、legacy/packet/refinement source、raw E・primal/P1 correction・全四B・physical recipe の schema 読取も静的に再点検した。実 external E と保存64段の末尾 instruction/result、source-correction/p1-reductions/p1-roots/step manifest の字段を照合した。この範囲では同じ不存在target参照の追加欠陥は見つからず、当該算術本文は変更しなかった。これは新Pの全本走が成功したとの主張ではない。

## F6. WF v4 の完成差分と保持境界

新 WF は schema d972.r07.continuation-positive-word-workflow.v4、path/name/upload を v4、push markerを [r07-continuation-positive-word-readout-v4-run] に統一した。草案のmarkerがv3に残っていた点は root の静的指摘を受けて公開前に修理し、最終 hash は後掲の値となった。

新 P/D の実 path・bytes/SHA、P5/D3 exact名、新第5群の全metadata gateだけを実行接続へ反映した。旧 v1/v2失敗来歴を保持し、run33999045563/1の head、全診断ZIP pin、旧 P/D/WF pin、P elapsed/最終progress、全16親/source不変・word/D未作成、P4/D3/inventory群の実PASSを previous_readout_v3 へ追加した。診断を第17数学親にせず、旧失敗の再実行も行わない。

全16数学親・全各tuple/entry・実64段・30直接entry pin・旧completion全保存・原owner/source/start・全raw/runtime・全ZIP/expiry/安全展開・相対POSIX全文字列整列・旧inventory copy adapter・取得単位before/always-after・13P/可変D全保存・same-root/current-grade成功条件を保持した。未知targetを補うdefault/getや gate削除は追加していない。最終 candidate にはP/D単一成功実行と全入力/語不変が必要である。

実CLIは前版と同じ。Pは16親root（blockはowner順4回）・acceptance・新output・max-seconds=5400・max-memory-mib=7168。Dは同じ16親/acceptance、word-root、別output、producer-max-seconds=5400、producer-max-memory-mib=7168、自身max-seconds=10800。P/D selftest内部各300秒、外各360秒、P外6000秒、D外11400秒、job330分を維持する。上限は速度予測ではない。

## F7. 最終 files と静的照合

| file | bytes | SHA256 | LF |
|---|---:|---|---:|
| search/d972_r07_continuation_positive_word_readout_v3.py | 200658 | bc51546ee1b2e73cff3a115947c817164199179b25699f90a7cae3283872e16e | 3274 |
| .github/workflows/d972-r07-continuation-positive-word-readout-v4.yml | 112685 | a4a436934f545465c97cbaed5cafcd38a73c253581fd6707676c7942af03c0f5 | 1718 |
| 公開pinのみ参照: search/check_d972_r07_continuation_same_word_eleven_slots_v3.py | 176579 | 273f0283186ef30e6833d6b7e402140fcb8bf832a22dbc0146c73412672f8e2c | 2636 |

新 P/WF は UTF-8 BOM無し、CR0、final LFあり、行末空白0。旧 P v2 は175318/cf6ac987acb2f399f36a8438cca78b773d7791286473b68362f2824a35d6451c、旧 WF v3 は108358/04f06ac35b7cc98cbe5e78a011f28b5250a7fe69537332d21eb2c109a45b8604のまま。D v3はroot配達の公刊path/pinだけを使い、新D本文/返信は読んでいない。

実行したのは静的source読取、公開ABI照合、保存metadataのJSON読取・字段/全辞書一致、whole-file bytes/SHAと改行の確認である。ローカルPython/import/AST/数値/GAPや新P/D selftestは行っていない。新GHAのAST、P5/D3、新旧metadata群、本P/Dと全出力照合がruntimeとして残る。root/Task1007の全文監査後だけrootが公開し、単一git/GHA brokerとして実run/commitを記帳する。

## F8. 凍結と994への復帰

この P/WF source pin を完成静的修理として凍結候補に渡す。本返信の完了票と最終bytes/SHAをroot/1007へ通知し、監査で新しい根拠ある必須修理が出た場合にのみ未公開版の限定差分を扱う。公刊後の旧版上書きは行わない。

1005の新runtime、全grade2、COMMON/cofinal/fake/Ihara、full A0、verifiedは主張しない。Task994はF1の境界から再開し、Task1004の完成済resume契約と997–1003の共通公開表に従って残るprivate recovery/final/CLI/canaryを完成させる。初回batch親は実64/rank1450のままで、後続96への差替えをしない。

AUDIT_1005_VERDICT: P_V3_WF_V4_STATIC_REPAIR_COMPLETE_RUNTIME_PENDING
