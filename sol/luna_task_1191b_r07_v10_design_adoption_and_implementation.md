# Task1191b — V10の設計採用と実装開始範囲

宛先: 既存 Pauli(P) / Helmholtz(C) / Noether(public)。Solは下記の有限設計を採用し、各自のTEMP内versioned source実装を開始可とする。Task1191/1191a、裁定2199/2293/2294/2295を継承する。これは設計から実装へ進む判断であり、未実装sourceの静的採用や未発射GHAの成功を意味しない。配置/発射はrootの最終source全文・差分・4者identity採用後。

## 採用材料と読取根拠

R = C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163、材料はR/task1191。

- P登録表 public-P10-registry-current-count-inputs-v1.json: 12401 / 6f92e487d6190ac36c00b40392a1082d9854032af4fbade4f2e30d9ad7126c00。全文628332。current/historical差分3673/80a92379…は5ebf5dで全文。
- P第9群 v2: public-P10-ninth-group-exact-cases-and-serializer-plan-v2.json、46143 / 354e87fed21c44c1a56b754e487a56adb9c39d8c9d2aebafa2ed7bc223ab3018。v1全文b4d67e＋case25回復628332、v1→v2全JSON差分5eba09。29負例、合計111予定。unsealed acceptanceのschemaはnamespace+.acceptanceであり、old-input projectionが受けるparent-layoutと区別する。
- P全consumer設計 v2: public-P10-all-baseline-consumers-and-planned-scopes-v2.json、51573 / 1a59da66bb4d895c36d37913e96de0de1a17ded1255c3d7aef18f707c107b449。0d411e＋group29–40回復1ab19fで全64scope/357 lexical siteを読了。これは文字列/宣言も含む全検索で、実call graphの完成証拠ではない。歴史authenticate_*内のsaved batch_observation等へcurrent exact7を注入してはならない。最終sourceでは全実consumer分類とraw範囲を改めて接続する。
- C独立core 10780 / 85abf62a4746778f4754984e7205c3c10a4a7505dfd5c0544527f21ea2c9ec91（a437bb）、修正自己検査接続v2 6625 / 26edf94a8d736a05786f18e447dc48d66a36982e64d169ae98df21bda73588b3（e93e18）。
- C第9群 v3: public-C10-ninth-exact-value-design-v3.json、33574 / b3186b8f2a704f61fc578122a3b59332af5e5b45e991b7d66d7c539cc9073b79。v2全文d5e3a2でnativeのPowerShell wrapper混入を検出。v3はその1箇所だけ裸21配列へ修正したことをroot242d63/native0でJSON全同一性照合。20負例、合計117予定。C全consumer分類票は最終sourceとともに全実辺を提出すること。未提出票を既読/全数採用とは記さない。
- public計数/identity案14518 / 94dce2114136539a51b1d5a515bd386f557e93f256aebc8c032e28d5c81c9975（74e97b）、追加前件案18025 / c7ddf25ead83a208231d91135fa06e04679fc2ba63420c8a4e76f14c647b6169（37d3c6）。以下の限定された差分を実装対象とする。

root242d63/native0により全16計数、15 keysets、旧21親/旧6層prefix一致を独立照合。current22親/7層、768/896行、祖先865/993、rank2346/gen9051、5376相/5404 checkpoint/7 invocation、13/64/81/15 keysを採用。旧native-v9は歴史6層、旧native-v8は歴史5層のnumeric view/文書keysetを分離する。数学payload再計算は行っていない。

## 実装するもの

各自の既採用V9 sourceを基準に、第22親の有限受領・独立昇格adapter、current7層の明示派生、old-side false、上記第9群、Task1191aのordinary自己検査経路を実装する。P登録表とC独立和の著者分離、原P37数学+4loader+25native等の保全条件を維持。旧constant/callerのcurrent→historical rebindingと新adapter追加は全正逆raw差分を出す。未完了header D3や新P/C最終pinに依存しないsource部分から進め、最終固定までに実値で閉じる。仮pinのままfinal/採用済みとしない。

Pの新第9子processは旧第8子と同じ元selftest300秒の絶対deadlineを共有する。同一実source/registryを両側前後でpin、環境allowlist、親production=Falseの保持、異常時の回収を継承。publicのcurrent_execution_edgesでは旧第8と新第9を別辺として記帳し、実CLI mode名をP最終公開票へ一致させる。子ごとの300秒追加配分は禁止。元shared_tcbのkernel2本/4区間/NOT_MEASURED/第三独立性なしは同一のまま。

public F-v9-2のprovenance明示、F-v9-4 current exact7と全コピー、F-v9-5の上記実辺追加、F-v9-8のWF起動時bytes/SHA・noclobber raw copy・cmp・前後照合を採用。WFの期待全SHAはrootの事前最終WF D3/commitが外部権威である。bootstrapの初回自己観測を独立期待hashと偽称しない。driverへWF全SHAを逆埋込する循環は禁止。原source/typed/caps/保存predicateを保持する。

F-v9-7は今回、2つの自己申告statementの安定名化だけ採用する:
selection_lambda_oracle_is_separate_from_new_final_lambda_oracle、
new_batch_parent_and_adapter_added。
値trueの意味は不変。6 anchor/12 receiptの既存flat fieldsを2つのrole mapsへ一斉移行する案は本V10では保留。必要な第7親の3 field追加と全consumerを明示する。大きなwire配置移行を追加して通常V10実装を止めない。historical V9 raw/schemaは全保存する。

public外側55→59 intervalsは22 live-parent+22 intake-inventory+8 native-intake+7 restorationの実caller4件追加へ限定。P/C内側countsから未形成を補完しない。現実に失敗/未形成ならその状態を保存する。canonical重複除去/圧縮/計算高速化の判定経路変更は今回実装範囲外で、別の具体的審査に残す。

## 固定・引渡し

旧版を上書きせず、指定source名のTEMP候補と、全raw partition・新旧差分・独立consumer票・public literals/key/value定義・実D3を版付きで提出する。source未固定の間はlive fileをroot最終票へ混ぜない。P/C相互の私有source/diff/fixture閲覧禁止、Noetherは公開契約とopaque D3のみ。新targetのlocal実行/import/AST/compile/selftest禁止を継承。GHAはrootのみ、2199のpin/別読/name/marker通知後に進める。元のsol/luna_reply_1191_{p,c,public}_r07_v10_registered_parent_and_premises.mdへ続けて報告する。
