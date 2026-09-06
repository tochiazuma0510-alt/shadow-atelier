# Task1022 — P4の公開resource metadataのnested型

宛先: 既存 packet_producer / Luna。完成P4/返信1016は凍結不変。Task1019 wrapper作者が他系本文を読まずに厳密接続できるよう、Task1020で未掲載のpublic metadata型だけを新 `sol/luna_reply_1022_r07_positive_resource_public_nested_receipts.md` に記す。本票はroot読了後にwrapper作者へそのまま公開する。私的算法・helper本文・codecの実装手順は含めず、serialization interfaceの字段/型/順序/全pinと再現入口だけを書く。

指定新返信だけを書き、source/WF/旧票は変更しない。ローカル実行/import/AST/数学/network/git/GHA/credentials/追加agentなし。自系最終252290 B / 0fc1c039d3ae076107585da88624c01656458c11d1d07df0054dcbec88fadeeaをtextとして参照する。

必要な公開型は次のとおり。

- 通常resource startのformat/cache/limitsとbinding内acceptance/parents/consumer_sources/raw_sources/runtime/accepted_owner/accepted_headのexact字段・型・list順序・descriptorのfile名基準。外側全pin/self sealの区別。
- 通常resource resultのindices/index_states/cacheと各index receiptのexact字段・型/順序、word/result/manifestのどの全bytes hashへ結ぶか。完了closed/finished/durableとUNKNOWN_RESOURCE時のnull/未形成を区別。
- P対照paths_receipt.fileの絶対/REPORT相対の別。三群scratch/start/telemetry/result/paths receiptの実相対配置。paths.producer/reference_sourceのrelative baseと全pin。
- 第一test rows/cache、第二test word/root/normalized_pair/ops/reference_sourceのexact型、第三群fixture resource枠の配置。public fieldsを通常とfixtureで混ぜない。旧full suite未実行/三false assuranceを再掲する。

実未実行の自己試験stdoutを作らず、sourceから読んだinterface仕様として列挙する。封印値や他系本文は無い。記述の全textとsource対応を静的に読了して実bytes/SHAをrootへ返す。最後は `AUDIT_1022_VERDICT:`。本語/自己試験/ASTのPASSや新数値を先取りしない。
