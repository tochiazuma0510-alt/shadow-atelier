# 宛先: Luna / 今後の実装担当 — recurrent failure guard

今後の各 Luna task は、下記を「実装後の必須チェック欄」として明記すること。

1. **固定snapshot**: 読み始めとfreeze時に全pinのSHA/bytesを再確認し、編集中のlive fileを監査対象に混ぜない。versioned successorを作り、旧freezeを上書きしない。
2. **実データ形状**: helperの実return key/typeをcall siteまで追う。public projectionにないprivate fieldを読まない・説明用fieldを数学値として使わない。以前は未到達だった旧関数を新laneでliveにする場合、名前解決・引数名・return arity・monitorの`check/reserve` API・発生するRESOURCE例外まで実呼出し経路で再監査する。producer/checker双方でexact keysetと型変異canaryを置く。
3. **production-path selftest**: fixture-only validatorで済ませず、実際のselector/helper/finalizer/schema/terminal分岐を共有入口から通す。今回のような「本番だけKeyError」を必ず捕捉するshape canaryを入れる。
4. **producer/checker状態順序**: pool anchor、intern順、candidate snapshot/rollback、ID再利用、basis commit位置を逐語対照する。checker probeは必ずtransactionalで、persistent scheduleを汚染しない。
5. **RESOURCE契約**: terminalごとのexact top/nested keyset、closed reason/cap registry、actual observed count、gt/ge、phase/current target/seed、部分transaction rollbackをP/Cで鏡像検査する。
6. **driver/pin**: 最終P/C/task hashをdriverへrepinし、placeholder/stale path=0、marker exactly once、pipefail/tee、共通deadlineを確認。必ず短いGHA selftestを先に通し、そのcommitでのみfullをdispatchする。
7. **性能**: immutable SHA・context・source gradientはscan外で一回化。候補ごとの全DAG/全target再構築、full sparse materialization、unbounded cacheを禁止。長いreducer/DP/serialization内部にもwall/RSS cadenceとregistered capを置く。
8. **主張境界**: producerだけの結果をcross-checkedにしない。prefix-only / registered-universe / UNKNOWNを明記し、full D2・full H3・lift非存在へ昇格しない。

このチェック欄を今後の指示書へ毎回転載し、該当しない項目も「非該当の理由」を一行で残すこと。
