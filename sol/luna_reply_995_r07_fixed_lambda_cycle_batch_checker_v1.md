# Task995 — 固定 lambda・一 batch の独立 checker

**F1 — 実装と共通契約。** Task995 / root 著作994 C1–C10、公開 Task997 / 1000 / 1001 / 1002 / 1003 / 1004 / 1011 を全文読了した。新 source は search/check_d972_r07_fixed_lambda_cycle_batch_v1.py。新 P source / reply994 は読まず、root 配達の数学・wire・pin 表だけを共有した。旧 source / workflow / 返信は変更しない。途中で root 優先の Task1006 を別の許可二 file に完了し、本便へ戻った。未公開の本版に限り、root の Task1011（4774 bytes / a26e11e6c937aebddd33829982144750ec7029ef9039b13ed8054d2908d7687f）による metadata 境界を最終適用した。

本版は d972.r07.fixed-lambda-cycle-batch.v1。実64親の固定 lambda で全54433弦 / 2 aux を調べ、一 batch / 最大32候補 / refill=false を保持する。主経路は AcceptedInputs → restore_physical_anchor → FixedBundle / root_records → replay_selection → replay_candidate / BatchReductionState → compare_final → 全保存 JSON / 入力不変 / checker-result。main / deadline bridge / 三群 selftest まで保存した。ローカル実行は行っていない。

**F2 — 受理親と算術範囲。** 入口は元14親＋continuation の15役全 artifact / file / directory roster、root の六key plain acceptance、P/C code・data・runtime・登録上限を完全一致させる。file は相対 POSIX 完全文字列順、重複 / 非有限 JSON / bool と整数の混同 / symlink / EOF 違いを拒否する。portable identity は parents.path だけを除いた受付の hash で、host path / run / nonce / 時刻は invocation へ閉じる。

登録親は run33990567016/1、head c57c976c6ba4a9d57c2bd3c7de2a09b0d3cedd70、artifact9977040548、ZIP304642285 bytes / a7ecd56dba33e35475d72486497b125fe983f4fb00a4fa91be813388373f5792。64段 / rank1450 / generation8155 / Separator / UNKNOWN_CAP と成功 C64 が入口であり、未来の成功親を設定していない。実 HEAD は 964 bytes / 4614d5c3fc619007879f3a5062cde90ac0cab86552ddd17ff14306bc961ac2f4、result は 42785 / 75f76ac43c86cfae998b0f4fe757a79b500727c2bfa847849fa57dbfa05293fd、C は 330955 / ff55c51e90acead643b9683af6f82d492c503a92c83a504a97eeb3f62c31cc4d。全 pin は acceptance / 公開親 tuple と実 bytes の双方へ結ぶ。

旧1354行・seed30/34・packet3・refinement26・外部E・continuation64 の保存行位置 / instruction / target identity / 全 phase pin / 旧成功Cを読む。旧 oracle / E / 消去 / 各段 separator は再演しない。一方、今回の selection lambda は全旧1450行を実 packed bytes から直接 dot0、旧 continuation start の target（外部E後）と実64 HEAD targetへ直接 dot1を読む。97件の旧 target parent 列を独立に再構成して deep copy する。固定 P1 index は continuation/fixed と refinement の保存 index を一致させ、保持 literal reader が必要とする index / p1_parent を明示 metadata adapter で供給する。

新 selection は全4 character の q / 全8059 current P1 values・等式、独自 ordinary27 source score / cochain、全弦 fit・residual と両 aux を計算する。Jの tau を行とする行列に対し inverse=(basis.T)^−1 の型を確認する。全失敗 roster / EOF の後に先頭 min(32,failed) を選び、全弦零の場合だけ最初の非零 aux、一方も零なら現在 lambda の COMPLETE_ZERO_CANDIDATE。弦 witness は零係数も含む六 cycle を保持する。先行 selection_start と後の selection hash を分け、witness-roster / 外部 witness / oracle-view を全数結ぶ。

候補ごとに保持 C 系の実 RawSLP / ordinary27 / 別 primal / fresh-copy P1 補正を呼び、96776 lower 零と全四 B の和を直接調べる。新物理消去は全旧 basis → 新採用順の係数 vector（零を含む）を比較し、selection lambda の旧行寄与零と新行寄与を分ける。残差 pairing=0 でも独立なら採用する。DEPENDENT は full physical 零と typed null を比較し、rank / generation / target / row chain を進めない。物理語因子 −sr(coefficient)、外側 sr(sigma) 一回、数値 target は −theta、correction=元rho2−current remainder の語因子は +sr(theta)。新 instruction.target_sha256 は plain target JSON 全hashで、packed remainder hashと区別する。

全候補完了（又は実 Linear）後だけ finalizer を呼ぶ。新 lambda の全旧/新行 dot0・batch初期/最終 target dot1、全新 target identity を含む DERIVED rho2 を調べる。初期完全零は既存 selection lambda を維持する。Linear は lambda / pairing / rho2 を null にし、未処理 selected 殻を SKIPPED_AFTER_LINEAR / 全測定 null にする。新 final lambda の oracle は計算せず、new_lambda_oracle=null を保つ。q / lambda の四区画の台と trit 件数は「今回の値」であり、作用素恒等零や全 character 有意とは呼ばない。

**F3 — durable prefix・来歴・保存不変。** progress/HEAD は BatchReductionState / current_lambda=null。checkpoint sequence 0、selection 1–3、その後候補各6phaseを完全な連続列として比較する。全係数 / phase / row / decision / checkpoint の全 bytes と manifest を照合し、HEADの直後に存在する登録 phase 一つだけを別 durable_tail に記帳する。先行 reduction が state.advance まで比較済みでも、Cの公開 processed / dependent / accepted / rank / generation / state_head / target は実 HEAD checkpoint の deep copy に固定する。Pの outputへ書かず、先行行を公開 stateへ昇格しない。

progress HEADの実 checkpoint file SHAも入口で結び、通常の全 HEAD bytes 比較を保持する。穴・二phase先・別owner・未登録通常名を拒否する。atomic pending は登録 basename / phase / row / final の明示語法だけを認め、全診断 bytes / directories を保存不変対象に残す。final payload / manifestだけ、又はHEADだけの publication tail も別型で記録し、HEAD + result + 全保存不変が揃うまで partial=true / candidate=false。形成済みの public HEAD hashは隠さない。

全 invocation の file descriptor と exact body / before HEAD / absolute counts / portable identity / producer上限 / UTC launch / host paths を照合する。UUID / 時刻順から今回を推測せず result.invocation_sha256 を使う。Task1004 の完成済み再受付は新 invocation を必須としない。保存 result の受付 hash は、その過去 invocation の host pathsを同 portable受付へ戻して厳密再構成した値へ結ぶ。旧 elapsed / run を今回の計測へ書き換えない。新C側の input_preservation は今回の受付を別に記録し、外側 execution receipt は root が扱う。

Task1011 の初回停止後は、resume=false の通常 receipt が高々1件で、1 fresh 又は両 before HEAD が null / strict count0 の resume=true bootstrap が一件以上ある履歴を受ける。複数 bootstrap は実 flag のまま保存し、通常 receipt が0件なら progress HEAD / checkpoint / phase の全未形成を要求する。未形成 nonce の正規 atomic pending は全 bytes を保持し、通常 receipt 数へ加えない。resource-stop.json は .resource-stop / UNKNOWN_RESOURCE、rejected.json は .rejected / FAIL / REJECTED へ filename から厳密に結ぶ。両方を独立に全文照合し、非nullの binding は実形成済み root / selection / 通常 invocation / committed HEAD 以内の歴史 checkpoint・count / final・public HEAD に一致させる。早期 null は後の形成値で書き換えない。完成結果の terminal は全 final の値、未完成の診断が一件ならその terminal、両方なら null。C-result の字段は増やさない。

inputs/{parents-before,parents-after}.json は15役順の全 files / directories、code-before/afterは新P/C＋P9/C10＋raw3の24 descriptor全union。producer保存票を比較した後、Cも全親 / code / raw / acceptance / P output全file・directoryを実再hashして不変を確認する。自己の report path は全親 / P output / acceptance / source入力から分離する。

**F4 — 保持 TCB と source pin。** 最終作者版を 181828 bytes / SHA256 7a4289506ce78b0ea562c63c9fb0841179a5bac10bc08165b211ed83982d292f、LF2680 / CR0 / BOMなし / final LF で凍結する。Task1011 の通常 metadata / 第三群だけをメモリ内で逆置換すると、直前版 169824 bytes / 65aad639896ad5f5366f8d2e41c453cb43e47e4c671b116af92148c4f2f90a42 に全 bytes が一致した。これは文字列と SHA の比較で、Python parse / 実行ではない。新 P の最終公開 pin は root 配達の 213861 bytes / 229785eb91be9852c0d4189e67806c8fc7af7e07ef1ad3ec9650044e85427591。P本文を読まず、実 acceptance は root が作成する。

保持 C 系 exact pin は以下。P9の metadata pin と同じ表の正本は [Task1002](luna_task_1002_r07_fixed_lambda_batch_retained_code_pins_v1.md)（5490 bytes / 68f7e854f90fa9e4692bad03f09fceaabbc096fb1cd4a9e94a03c703b58b61e0）。旧 continuation C v1 は本 closure へ追加しない。

| search/ 以下の保持 checker | bytes | SHA256 |
|---|---:|---|
| check_d972_r07_complete_oracle_cegar_continuation_v2.py | 129557 | e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3 |
| check_d972_r07_selected_cycle_materializer_v1.py | 103757 | a6d52e0d12d97201f0a19f25c54e0924e3fbea89fefa3554727a7178881218b4 |
| check_d972_r07_section_cochain_oracle_v2.py | 84402 | a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d |
| check_d972_r07_section_cochain_oracle_v1.py | 80740 | 2db166400dd819805f36b613993d4622e8365f04339ca7aef0371a28de71c967 |
| check_d972_r07_full_origin_refinement_v1.py | 75083 | 1ee388c9cd39a43992bc9a6e075b087da3ae1672221a197719ea435d7d3529c2 |
| check_d972_r07_fixed_root_packet_loop_v2.py | 66251 | 5289253a82d942d71b1ec55505d08ab772b111f2ba08e301f67387eae19b23e5 |
| check_d972_r07_actual_root_seed_materializer_v3.py | 64626 | eca60918eb943edddc321054f04b8547b3e88e5f7421f4de1e09ea04d7ca2701 |
| check_d972_r07_rank1355_root_seed_scalars_v1.py | 36236 | f3c7ca2586a3734334b7d9823316601d18ab1d36561c72aa2c23c2aedfca0e62 |
| check_d972_r07_actual_grade2_root_scalar_batch_v2.py | 119619 | e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6 |
| check_d972_r07_targeted_grade2_owner_generated_join_v15.py | 141770 | 8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662 |

| raw input | bytes | SHA256 |
|---|---:|---|
| scratchpad/fuda1_a0_rmax_data.g | 4709 | 625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba |
| scratchpad/a0_paper_words_v1.json | 115928 | 90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893 |
| scratchpad/a0_v2_words.json | 106133 | fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612 |

保持 primitive の独立性を本便で遡及して証明したとは呼ばない。F-fo-1 / F-sc-1 / F-cy-4a の旧 envelope / context / transport・PSL / B 復号の系譜を TCB として残す。新 C の current P1 は保持 packed projection / 独自 section、ordinary27 / RawSLP / grouped forwardを保持し、新 selector / batch reducer / serializer / read-only admission を接続した。保持 one_physical_row / 旧 C.attach / 各新候補ごとの separator を呼ばない。旧 successful suiteの再走0は、保持実装の全分岐が今回本走したという意味ではない。

**F5 — 三群 selftest と通常 CLI。** 三群は本番 helper を通し、返値 testsは exact name/status/rejected_cases の三要素。fixtureは合成 array / sparse physical row / metadata protocolで、実 Omega / 実rank1450の成功とはしない。

- fixed-selection-full-roster-and-aux：全54433 residual、先頭32と全失敗列、末尾変異 / EOF、弦優先、零係数を含む六cycle、aux-only、全零。
- dependent-independent-target-signs-and-packed：実reduce / advance / finalizerによる依存とnull、旧lambda残差0の独立、sigma2、theta1/2の負の数値更新と正のcorrection語、全係数の零factor、Linear / Separator、packed不正値 / EOF。
- private-prefix-publication-resume-and-isolation：実 reduction / row / candidate / checkpoint / HEAD serializer、HEAD8の一つ先の完成 reduction / seq9をread-only比較してcounts0を維持、親・checkpoint deep copy、別owner・二phase先・hole・EOF・完全resealしたHEAD別checkpoint拒否。Task1011 の追加は実 invocation_records / ProgressAudit / compare_diagnostic(s) / compare_candidate_roster を通し、0 fresh / 複数 bootstrap / pending新nonce、2 fresh / bool count / 通常receipt0の形成済みcheckpoint拒否、二診断の同時保持と各単独 terminal、完全resealした filename/schema/status・全非null hash・count の改竄、未形成rootへの非null bindingを扱う。群名・順序・三件の返値型は不変。先行phaseと新受付のbodyは明示的なmetadata protocol fixtureであり、保存親のoracleやfinalizer成功fixtureではない。

GHA 内の新 canary 呼出し:

```sh
python -B search/check_d972_r07_fixed_lambda_cycle_batch_v1.py --selftest --max-seconds 300 --max-memory-mib 7168
```

通常本走の再現 CLI（各 *_ROOT は受付の実絶対path、以下は未実行の引渡し）:

```sh
python -B search/check_d972_r07_fixed_lambda_cycle_batch_v1.py \
  --state-root "$STATE_ROOT" --delta-root "$DELTA_ROOT" --seed34-root "$SEED34_ROOT" \
  --packet-root "$PACKET_ROOT" --refinement-root "$REFINEMENT_ROOT" --oracle-root "$ORACLE_ROOT" --e-root "$E_ROOT" \
  --prepare-root "$PREPARE_ROOT" --block-root "$BLOCK0_ROOT" --block-root "$BLOCK1_ROOT" \
  --block-root "$BLOCK2_ROOT" --block-root "$BLOCK3_ROOT" --p1-root "$P1_ROOT" --task712-root "$TASK712_ROOT" \
  --continuation-root "$CONTINUATION_ROOT" --acceptance "$ACCEPTANCE" --candidate-root "$P_OUTPUT" \
  --output "$C_REPORT" --max-seconds 10800 --max-memory-mib 7168 \
  --producer-max-seconds 5400 --producer-max-memory-mib 7168
```

max_seconds / max_memory_mib は正の ordinary integer。main は保持 C/E/O/REFINE/FIXED/L/ROOTS/BASE の boundary / progress を新 deadline・peak memory・UNKNOWN_RESOURCE へ接続する。通常 C は scoped PASS exit0、資源不足は UNKNOWN_RESOURCE exit3、不一致は FAIL exit1。新 checker-result の exact fieldsは Task997＋1001、部分結果の公開countsは実HEADだけ、未形成値はnull。全比較未了のUNKNOWN/FAILを全比較trueにせず、partial=true / candidate=false / cross_checked=falseへ戻す。stderrに停止phase・理由を残し、stdoutと分離する。

**F6 — 現時点の判定。** 本作者は source / 共通 wire / 実旧 metadata と hash の静的点検だけを実施した。第三 canary の HEAD reseal逆対照は、実 checkpoint SHA joinを通常 ProgressAudit入口へ追加して接続した。root / Task996 は Task1004 適用版までの全 source / 作者票を読了し、追加必須指摘なしを通知した。Task996 は Task1011 の全通常差分と第三群を改めて読了し、最終 181828 / 7a428950… を実再hashして追加必須指摘なしと通知した。最後の26 bytes差は、canaryの履歴件数を実 checkpoint compare済み local history() の返値で読む変更だけである。Task1011 適用後の本作者票と全最終pinを root / 996 へ渡す。

ローカル Python / import / AST / 数値 / GAP / network / Git / credentials / 新agent は使用していない。新 source の構文ゲート・三群canary・全新本走・速度/RAM実測・cross-check / CV9は未実施。32採用、rank増分、target零、時間短縮を予言しない。新P/source受付・workflow・GHA・commitはroot単独brokerで進める。本報告の作成をGHAの成功と呼ばない。

全型で grade2_member / grade2_nonmember は NOT_DECIDED、full_A0 / verified は false。Linearであっても positive_readoutはNEW_BATCH_SAME_WORD_ADAPTER_PENDING。normalized物理語へ source_lower_zeroを新たなgateにせずNOT_ASSERTEDを保ち、full P / A0 / same-word positiveの閉鎖は本版の対象外である。

AUDIT_995_VERDICT: SOURCE_FROZEN; TASK1011_STATIC_DELTA_REVIEWED_NO_REQUIRED_FIX; NEW_SELFTEST_AND_GHA_UNEXECUTED; GRADE2_NOT_DECIDED.
