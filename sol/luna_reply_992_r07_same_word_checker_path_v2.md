# Task992 — 同語 checker の v2 path 移行

**F1 — 完了範囲。** Task990 を凍結した後、本 Task992 を全文読了して指定の新 C v2 を作成した。変更は AcceptedInputs.check_runtime_sources の producer path と自己 path の二 literal だけである。P991/WF991 の source・返信は読んでいない。P の bool/int 修理や算術 helper を C に複製していない。新 P/WF の最終 pin 接続と GHA は root の工程である。

実 run 33995799635/1 の停止理由は root から受けた観測通知（P/WF が実 integer 1 の external_e_attached を is True と読んだ）に基づく。C v1 L1114 は ==1 なので今回の integer 1 拒否を共有していない。この比較を追加変更せず、新 producer v2 の実 path/whole-file receipt を受ける入口だけ移行した。本便で実 diagnostic の数値再生はしていない。

**F2 — 全差分と source freeze。**

| ファイル | bytes | SHA256 |
|---|---:|---|
| search/check_d972_r07_continuation_same_word_eleven_slots_v1.py（旧、不変） | 176579 | a9e72980f3594842b5a7a4abaaf610b49a5d9202779ab1132c53c6bd4225ec98 |
| search/check_d972_r07_continuation_same_word_eleven_slots_v2.py（新、凍結） | 176579 | 865ed6a50b95303fdecafbc69e841da018858aa4624467fb17cdf80a0beadfd1 |

新 source は LF2636 / CR0 / BOMなし / final LF。全行を静的比較した差分は次の二行だけ。

- L1066: search/d972_r07_continuation_positive_word_readout_v1.py → search/d972_r07_continuation_positive_word_readout_v2.py
- L1067: search/check_d972_r07_continuation_same_word_eleven_slots_v1.py → search/check_d972_r07_continuation_same_word_eleven_slots_v2.py

この二つの完全 path を新 source 内で逆置換した結果は、旧 source 全 bytes と一致した。旧 source の実 hash も前後同一である。従って全算術、一般 LEFT Fox/非単位子 Act、typed E3 40 B/E4 154 B、11 slot、full filtered 80644、fresh rho2、Ref recipe/全13 word files/target history/EOF、resource/terminal、三群 canary の本文はすべて不変。docstring の Task983 表記も原著由来のまま保存した。これは文字列/bytes 比較であり、Python/import/AST/数値テストではない。

L1069–1071 の descriptor_check と file_receipt により、acceptance.consumer_sources の producer/checker はこの正確な二 path と実 bytes/SHA に一致しなければ拒否する。producer は whole file を hash するだけで、実装解釈・import はしない。旧 C9/C4 と raw4 の pins/認証は不変である。

**F3 — CLI と wire は不変。** C schema は d972.r07.continuation-same-word-eleven-slots.v1、WORD_SCHEMA は d972.r07.continuation-positive-word.v1 のまま。ファイル名 v2 を wire v2 と取り違えない。source receipt と acceptance の consumer_sources だけに新実 path/hash を入れる。

本番は新 source に、既存の全16親、--acceptance、--word-root、--output、--max-seconds、--max-memory-mib、--producer-max-seconds、--producer-max-memory-mib を渡す。block-root は既存順の四件。--output は未存在の出力ディレクトリ、全入力との非重複/no-reparse gate を保持する。C max-seconds は正の有限 float、memory は正整数、P の二上限は正整数で、既存の登録値をそのまま渡す。新資源枠は本票では登録しない。

三群 selftest は同じ --selftest --max-seconds SEC --max-memory-mib MIB。--output は任意で、stdout は同じ sealed .selftest、status=PASS、tests は次の三件・各 status=PASS を期待する（L1992 / L2022 / L2072）。

1. actual_nonunit_Act_inverse_typed_codec_endpoint_and_printed_order
2. same_root_EOF_mod54_and_resealed_Ref_word_key_mutations
3. actual_eleven_adapter_binary_JSONL_and_Linear_null_contracts

本番 exit0 は complete receipt を返し、status は actual current grade の結果により PASS 又は NOT_APPLICABLE。status=PASS の terminal は SAME_WORD_CURRENT_GRADE_COMPARED、NOT_APPLICABLE は NORMALIZED_PAIR_NOT_APPLICABLE。全未完/資源は exit3・UNKNOWN_RESOURCE、型/算術の失敗は exit1・FAIL。complete_output_report L2182 が完全 manifest/receipt と未完 diagnostic を分ける契約、complete_receipt/eof、全13 word files、全 node/Ref/同 root/normalized pair/全11 slots/full filtered/fresh rho2 の字段は不変である。

**F4 — 未実行と引継ぎ。** ローカル Python/import/AST/数値/GAP、network/Git/credential、新 agent、GHA は実施していない。新 C v2 の実 selftest/P–C 本走は未観測であり、旧 run の停止を修理 success と読み替えない。保持 TCB・cross-checked の限定・verified=false・grade2 NOT_DECIDED・full_A0=false は不変。Task993 へ source の全差分と最終 hash を通知し、二 path literal だけの差分・逆置換後の旧全 bytes SHA 一致・追加必須修正なしとの独立静的確認を受領した。Task993 の正式票、新 P/WF の完成、root の実 run/pins は別の記録に属する。

判定: PATH_ONLY_SOURCE_DELTA_COMPLETE。旧 C 全 bytes との二 literal 以外の一致を静的確認し、新 source を凍結した。実行による修理完了を認定する票ではない。

AUDIT_992_VERDICT:
