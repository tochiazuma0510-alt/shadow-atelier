# Task1091 — Luna: v5 envelope-v2 実停止診断

宛先: packet_bounds_audit（1086 driver作者、1084停止診断担当）。返信は sol/luna_reply_1091_r07_v5_envelope_v2_stopped_run_metadata_triage.md。材料は %TEMP%/shadow-atelier-audit163/task1091/ の新fileだけ。source修理は別便で行う。本便は実metadata/read-only診断。

実run34148667863/attempt1、head3e7e1ccf1996dad15b9019de849cf61548c654d1、workflow352449001/job101826078241、event push、envelope-v2。18:17:20Z更新のrun APIはcompleted/failure。全17親・intake・metadata16・P/C四群success。P wrapper14は17:45:32–18:15:22Z、postP15は18:15:22–35Z、C wrapper16は18:15:35–49Z、cost17/fixture18/preservation19/after-placement20はstep success、final21がfailure、candidate22はskipped。wrapper successをactual P/C exitへ補完しない。

根拠audit TEMP: v5-run34148667863-final-observation-v1.json=13846/99e8d4f52f73052aa30f046b4cc522ff3bbec2a253132b4c16d7bc6a780303dd、v5-run34148667863-artifacts-observation-v1.json=817/980134a8226eaa987d828dfe30e15c184ad2d82c3f17049765823d0a935316c0、v5-run34148667863-job101826078241-logs-v1.log=318016/bd85c25cbee777e8b2d4c0665b91a174eb76c3977306103d9349204e19cacb13。ログroot限定検索は例外本文未発見、例外なしではない。

実diagnostics id10029340951、name d972-r07-fixed-lambda-cycle-batch-v5-diagnostics-34148667863-1、API ZIP384805623/8947aa9b44be82c9d5f8d8d08f86c3da3fdf5eb8ba0d96c38eedf460e40d71e1。rootが全download中で、未完ZIPを開かない。取得・全展開完了後にrootが実root/取得票を通知する。それまでは既読WF/driverの実制御分岐と既知API metadataのみ整理できる。

P5=366659/6e19d029c0f4aa55e39d24022008a29ab666c50bc52d5d086917f7dbc10cb99d、C5=336193/47cf2596e9e9dabaab89395f5274ce15b9443002922ba7bfdbca42022979de73、driver_v2=1145223/238285767c62b0377d1192bd264233252870e0a5cfb9906a75035c0de2139573、WF=26294/3c20910e9fcce7cb8e05e234b7cbf8f1e329146a62613c6031dc8440d11431f7。1086の限定修理と既読公開serializerの範囲を保持する。

実受領後は actual P exit/result/selection、actual C exit/stderr/result、cost、三fixture ticket、最終保全、最終gateの最初の不一致と二次症状を分け、必要な最小修理の所属を根拠の実path/pin/行で返す。前回二不具合（P formal file_bytes consumer、C開始前ticket配置）が実runで通ったかも、実receiptからだけ判定する。失敗runの候補rankを正式parentにしない。個々の値が未観測ならnull/UNKNOWN。

Git/GHA/network/credential、Python/GAP/AST/import/compile/dot-source/数学source実行は禁止。全source・親・fixture・旧受領processを変更せず、P/C私的数学本文へ新規に踏み込まない。公開stderrの型/ラベル/公開schema/metadataだけ可。新agentなし、継続GHA認可の再取得不要。最終行 AUDIT_1091_VERDICT: を付ける。
