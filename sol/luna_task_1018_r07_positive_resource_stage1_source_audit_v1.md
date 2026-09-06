# Task1018 — 正語P4/D4の限定資源移行・新source監査

宛先: 既存packet_bounds_audit。1014最終票は18881 B/27743bc9fdaa26ab8a1d757b4a4b16e5405a4c9876148af69b8b69ab7b8409b9で凍結不変。新公開Task1015（7560 B/ac06f6997090358956e0f61661afc695fb6d75201c7916f3eadd3f9f84a01a7d）と自系委嘱1016/1017を全文読んで、sol/luna_reply_1018_r07_positive_resource_stage1_source_audit_v1.md だけに新source監査を返す。rootは初回batch実run34004423047/1の本C・全artifact回収と両sourceの独自静的監査を並行する。実装・ローカルPython/import/AST/GAP/数値・ネット/GHA/git/credentials/追加agentは禁止。

新対象は search/d972_r07_continuation_positive_word_readout_v4.py と search/check_d972_r07_continuation_same_word_eleven_slots_v4.py。各作者が作成中なので、先に公開契約と旧sourceとの差分の監査観点を整理できる。draft本文を読んだ場合は読取範囲/pinと未freezeを明示する。最終PASSはrootからの最終source/pin/作者票通知後に全本文/全diffを読み、実値一致を確認してから出す。source/他返信/Task1015を編集しない。私的本文/helper/設計を作者間へ転送せず、所見はrootへ返す。

重点は1014 F3–F9。PのWordDAG hash/pairと別phaseの空indexからのmod54再読、unused positions、Dのoffset/hash/child/uses/到達/各pass remainingをdisk化しているかを見る。sum64 MiBのcache上限、dirty page/部分append/read after write/reset、元IDの正負index/型、stride×count/offset/完全edge span、最終EOFと全zero/反復edge、source-bound scratch、fresh/no-resume/成功13fileからの分離を点検する。合法な行64 MiB/16 GiB scratch/minfree1 GiB/u64資源超過はUNKNOWN_RESOURCEで、hash/型/意味不一致や無関係な実装例外を資源扱いに隠さない。

既存canonical writer/reader・DFS add/yield/send順・Ref全scopeと実親recipe join・一般LEFT Fox/非unit Act・全11slot/full80644・現在PB4-dropped gradeを保持する。ordered-wordの固定入力での同一bytesと、新source等を含む外側来歴hashの変更を区別する。unused pointedの保持廃止が元pointer/型/hash/意味認証を落とさないこと、全11slotのremainingを独立初期化し、Ref alias/空row/operand保持/last-useに誤りがないことを確認する。symbol/ancestor/paused factors/Fox live等を残すこと自体は段階契約内であり、全常駐量有界とは呼ばせない。

新 --resource-selftest が通常helperを通るか、固定した旧自系の小helperまたは具体byte anchorとの対照であるか、大小cache境界/eviction/partial/EOF/型/到達/反復/0冪/異scope/行上限/pathを実発火できるかを静的に追う。旧P3/D3を対照だけに動的ロードする場合は全path/bytes/SHA/closureを登録し、旧suite一括やP/D共有helperを避ける。内部300秒/外部360秒の枠、新CLI受付、メモリ失敗時の小sample/外側保全、telemetryが全N表を再作成しないことも対象。

必要修理は早めにrootへF番号で伝える。最終票では新P/Dと全作者票のfull pin/読了範囲、実行未済、残存資源限界を記録する。新workflowは後段の別委嘱であり、本便で変更しない。末行は AUDIT_1018_VERDICT: とする。
