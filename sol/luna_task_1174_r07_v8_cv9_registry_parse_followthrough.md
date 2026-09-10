# Task 1174 — 裁定2262のV8追加前件（1171/1172/1173への公開補足）

宛先: Pauli(P1171)、Helmholtz(C1172)、Noether(public driver1173)。既存分業・著者分離・root単一brokerを維持。返信は各自の指定1171/1172/1173返信へ統合する。新たな親追加やcapsの承認待ちはない。

全文必読: ops/express/20260911_fable_astra_2262_batch_v7_cv9_grading.md と provenance/rulings_2262_snapshot_20260911.md。CV-9正本 docs/notes/fixed_lambda_batch_v7_cv9_reading_v1.md は73489 B / 7cb86ee27c4bc240cbf04871da6a92d6b2a2d0dd7f483a2b803b9e43f81501c3。rootは全627行を読了した。

正式親は run34523172734/1、head bf0b5c0b6ee00736481575b98f50ac071fc97e28、rank2090/gen8795、state_head31b3d6db8712a2dda6619a38c2713af60ffd7be40461e4d2c0ab6d29fa2a4a7c。cross-checked（限定7条）、verified=false、A0 actual0/1。未受理の初回失敗runの同rank sealは親に用いない。正式5は既受領root-v7-formal-inventory5-v1.json229/c44c63ef95459fa219291c266f787e74b9a435d1ac1d5cd7d603b93fb7c9097b。CV9待ちは解消。

F-v7-4: Pは実際にaudit-region-registry.jsonのnew_source_audit登録表を読み、現行親行数・祖先数・key数をそこから導出して全serializer/reader/HEAD/result/final/reentryで用いる。診断表の併記や同じliteralの二重登録だけでは満たさない。Pとdriverは公開wire・load順・hashの循環回避を相談し、閉じたデータ経路を示す。Cは独立の名前つき定数和を維持し、公開表との一致を静的票で示す。現在値と旧native値を表内でも分離し、旧凍結親に新表を遡及適用しない。整数はboolで代用しない。

F-v7-2: Pの各親reduction.jsonの二重parseを解消する。全ての元の受理/拒否述語・順序・seal/descriptor/EOF条件を保持し、同じ登録済rawに対する行単位の再利用とする。キャッシュ境界と寿命、再read/hashの扱い、observerの計数/終了窓、例外時の挙動を公開別読票で説明。現行readだけでなく全5親層を対象にし、全件自己観測のrepeated_parse_attemptsを正直に記録する。従前のbyte-identical制約はこの明示修理の必要箇所のみ正逆差分＋独立別読を条件として例外。数学の述語、C4 raw、資源上限、著者分離は例外なし。

第7metadata群はroot-v8-seventh-public-fixture-design-adoption-v1.jsonで公開設計を採択済。P12件/C14件の各有限案を実装可。全件同じ通常helperの正対照、単独変異、実caller、coherent seal/pin、完全一致の目的拒否を固定する。metadata fixtureの通過は数学肯定/物理EOF/未来oracleではない。旧6群のscopeと目的を保ち、旧path負例は必ずactual identityと異なるfilenameとなることを明示。source未実行のままfinal readbackを提出する。

費用は診断。層費用の加速という旧主張を持ち越さず、失敗rosterの単調減少や残run数を推定しない。fresh lambda2090 oracleは未計算。新5層の計器を継続し、P計器のliteral/path依存2箇所の接続とCの陳腐化コメントを精査する。現在のcold-storage/親統合への宇宙変更は行わない。

最終source pin、別読、marker/name expressを満たしてrootが配置・GHAを発射する。ローカルP/C/driver実行・import・AST・compile・selftestは禁止を維持。
