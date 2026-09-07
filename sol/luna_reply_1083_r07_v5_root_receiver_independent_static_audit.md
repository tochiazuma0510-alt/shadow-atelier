# Task1083 — v5 root metadata 受領器の独立静的監査

F1. Task1083 / Task1080 全文を読了し、1081 の最終 WF / driver 別読を凍結した後、本便を完了した。判定は完成候補用受領器の STATIC_CONTRACT_PASS、未解決 required finding は 0。対象は作者が固定した draft06、限定修理後の draft07、最後に同じ全 bytes で凍結した root-review-receiver-v5-guardclosed-v1.ps1 である。mutable working copy や作者自己票を独立根拠の代用にしていない。Git / GHA / network / credentials / Python / GAP / import / AST / compile / source・受領器・fixture の実行はすべて 0、新 agent も 0。変更した作業ツリーは本返信だけ、独自材料は TEMP/shadow-atelier-audit163/task1083 の新 file だけである。

F2. 最終受領器は 516693 B / b54e58f1bc33df144a3c2e6b20dc14a8b963356b914028148a965a758c15dbb3、LF 4626 / CR 0 / ASCII のみ / BOM なし / final LF あり / 行末空白 0。作者の draft07、作者凍結名、独自 snapshot-07.ps1 の三つを全 raw bytes で比較して同一だった。受領器に登録する新 v5 の launch / artifact / approval は null、normal guard は false のままである。既知の歴史 v4 tuple は歴史専用局所 scope の値であり、新 v5 の実観測や新候補受理に流用しない。後着の具体的な定数結合と実受領は root の別便で行う。本票完了を GHA 発射の追加条件にはしていない。

F3. 監査正本と全材料の pin は次のとおり。パス先頭 T は TEMP/shadow-atelier-audit163。P / C 数値 source は公開 opaque pin / raw range のみを用い、新しい私的数値本文や相手の私的監査票を読んでいない。

| 正本 | bytes | SHA256 |
| --- | ---: | --- |
| T/task1074/audit-r07-batch-v4-metadata-v5.ps1 | 261800 | dcccf94a7eb3458d6cf709478a449d3377f86e5b90edfa0a9f011d82122ac411 |
| T/task1080/root-review-receiver-v5-guardclosed-v1.ps1 | 516693 | b54e58f1bc33df144a3c2e6b20dc14a8b963356b914028148a965a758c15dbb3 |
| T/task1080/full-raw-region-index-draft07-v1.json | 695572 | 8bd73c188cf6b31941118fc7cf799ae80be31718643e1797c68b0228c2fc8f4f |
| T/task1080/full-raw-diff-draft07-v1.txt | 390983 | 586aa7e13fac5937b862daa126cb453b48236d5c6599f88259eb16087252b170 |
| T/task1080/final-static-delivery-v1.json | 19983 | 5c28026c4fa75e4f45f33d6d1fe1933175ac6e4efe44fb3a85cc543286b81af6 |
| T/task1080/public-material-index-v1.json | 14008 | ecb07144d4fe33892bb2bd32be6bb30867651ad51908b8fa8c5d8d7e9ce14a4c |
| T/task1083/independent-draft07-raw-and-static-review-v1.json | 2982 | 8f0a594ecee46d3301640dd9c53cac568247e605d9e98d14757cf919803ef766 |
| T/task1083/independent-final-delivery-pin-review-v1.json | 42800 | 3e5a1c7ca5daf03ae59c26ba2900d6a30953d92ad1be2bbed2e682a3f44149b3 |

作者の全納品目録 73 file の実全 bytes / SHA を独立に読み直し、全件一致した。公開入力 23 件は保存 copy と原所在の両方を全 file pin へ結び、23 組すべて一致した。73 件は目録自身と未来の返信を明示的に除く定義であり、その後に増えた directory 全 EOF まで比較したとは記さない。作者返信 1080 は 16321 B / b843025ab5bdccdfb2b1e56ba28adc820ad55440d36f6b25a3082e4615cdc9a4 の opaque pin のみ確認した。作者自己票 7578 B / 412f08513487286740486f7611c7a0b13574f6b4f5fa4e8f7a3be7fb968cf319 も 73 件内の pin として保持し、独立判定の代用にしない。

F4. 旧 1074 と新最終版の全 EOF 台帳を別に照合した。作者の区分は旧 62 → 新 96、IDENTICAL 59 / CHANGED 3 / ADDED 34 / 削除 0。旧新の区分に欠落・重複はなく、全 554 回の raw range SHA 照合、変更区間に収められた全文と実 bytes の一致、旧不変部と新変更部による全 516693 bytes の再構成、逆方向の旧 261800 bytes 再構成が一致した。旧 60 function body も全 raw 同一である。独自の最初の lexical 分割は HEADER + pre-main 59 関数 + 未分割 MAIN の 61 → 95。作者はさらに MAIN 内の global ManifestFiles を区切るので 62 → 96 となる。この 60 個目の本文も独立に全 raw 照合しており、件数の違いを欠落として放置していない。

新 34 関数、HEADER 全体、歴史 main を収める局所 wrapper、通常 main 全体、最後の cost だけの修理差分まで全文を静読した。旧 main 544 行は 8 space の移動インデントを除くと、RestoreFixtures を RestoreHistoricalFixturesReadOnly へ替えた一行だけが異なる。wrapper の旧 receipt 書出しから値 return への変更、引数と局所変数、script 状態の退避・復元、finally は別に全文を読んだ。全旧主張を残すことと、旧受領器プロセスを実行したという主張は別である。本便では実行していない。

F5. 歴史 v4 wrapper は旧 16 役、旧 root / schema / 実 tuple、旧64と v3 親、旧 registry / 固定 source を明示した局所 scope に結ぶ。局所 guard=true はこの歴史 scope に限定され、外側新 v5 の guard=false を開かない。旧 main の全親・全 file / dir / ZIP・原64 fixed payload・registry / TCB・checkpoint / invocation / row / phase・diagnostic / DEPENDENT の到達を保持する。返値に成功ログや collection 操作の余分な値を混ぜないこと、空・一要素・nested array と List.ToArray() の接続、script の directory plan / restoration / checks の finally 復元を追跡した。一般 Same / PlainInt / JSON parser の既受理本文は不変である。

RestoreHistoricalFixturesReadOnly は内側 ZIP の全 entry、全 file SHA / EOF、型、全 directory と三群の全 fixture 比較を局所的に読み直し、directory plan が to_create=0 であることを要求する。歴史親へ mkdir しない。旧 receipt の PASS を新たな信頼根にしたり、長い全受領を cache へ置換する枝はない。新 current REPORT に限った認証済み空 directory の復元とは別の経路である。

F6. 旧 v3 / v4 両親の preflight は、全名前・サイズ・保存目録・全 directory を重い内容 hash より前に調べ、欠品時は明示した引渡し診断へ出る。親へ新規 directory を作らない。その後も全 payload SHA / 全目録 / 内外 ZIP 照合を省かず、canonical 目録の pin 一致だけで本文再読を済ませない。正式 whole-inventory 登録は 7022 B / 64e3f8e6a434be335a88c1dee6efa4aae7b3d669faac28e704aefd0f8e3f4753 の root 票へ結ぶ。全 11648 file / 1308094050 B / 3525 directory、files 1931889 B / ffec515b0a235ce2dd99770e51619252c725269970b71e32180be5f14cafaff5、directories 200290 B / f9562484c91c05c517b50065d86e1a88f16af6b1e3198b1d0ba1adb645f9dc64 の公開登録を用いる。この登録と未完の full typed 親受領を分ける full_typed_parent_metadata_complete=false は残っている。2210 により発射条件から分けられた境界を、本票で PASS へ補完しない。

F7. 新通常入口は exact 17 役 / plain 8-key acceptance、旧16投影の同一性、旧64の 1450 行、v3 の 128 行、別 v4 の 128 行を順に束縛する。1450 → 1578 → 1706 と直近128 / 前層128 / 合計256を区別し、世代ごとの local 0 を同じ row に潰さない。元97親 → 225親 → 353親は全保存 prefix と全128項を照合し、theta=0 の項も落とさない。previous target は直近 v4 の start.target であり、その start.previous_target ではない。plain target JSON SHA と packed remainder SHA、参照 manifest と原64実 payload の所在も区別する。

過去二層の実128は過去の完全受領条件である。新 current の採用数は 0..128 の保存観測を読むので、次も128本独立という前提を追加しない。全1706親の ordered row / reducer source と零係数、current の動的採用行、全 checkpoint / final derivation まで接続した。current fresh invocation は一件として認証し、過去の invocation を新 resume と呼ばない。checkpoint の sequence は実 HEAD の prefix に制限し、直後の durable tail を処理済み件数へ足さない。通常 complete 候補は未完 tail を受理しない。

F8. batch observation は実保存の sequence >= 3 で current selection、sequence >= 9 で第一 candidate の完了を認める。intake 前や未形成観測は null、診断はその保存 checkpoint の prefix に結ぶ。first independent の条件は、親全行の pairing=0、processed=0、subtracted_new_pairing=0、非零 selection scalar と raw pairing の一致という保存条件へ結ぶ。二本目以降の独立や次 oracle の失敗数減少を仮定しない。Linear は lambda / pairings の null 型を守り、COMPLETE_ZERO に存在しない phase を作らない。early failure / resource stop を完成候補の null 埋めへ変換する入口はない。完成出力に併存する保存 diagnostic は各履歴 checkpoint と原識別子へ結び、実在しない歴史 HEAD 全 bytes を再生成比較したとは記さない。

F9. 公開 WF / driver の 11 行 bootstrap SHA と before / after の全 placement 票を照合し、旧 WF 二 archive、直近 v4 の WF / driver、新 driver / WF の全 raw pin を接続した。三 registry は歴史 76867 B / 9fe3d9cf1449c3535618a8c7618c6ab6e5fa4426f0f902c419fbbf91ad873b38、直近 v4 236390 B / 84f5bbc6a85e77915535968e4342c09b6bf3e5b94638ab14184c67ca677ce114、新 v5 499053 B / e30a6bde668f0778932f0c4fbd62752c698bd70b97e9b097dccde4e9348c2858 を各全 file pin で照合する。三つとも受領器の literal と公開目録で全 SHA を比較した。current P 137 → 156 / C 117 → 140 の全 EOF と分類、旧8 loader、P37 / C20 の計57 body、歴史60範囲、共有4 kernel をそれぞれの版・scope に結ぶ。変更本文を旧 raw 同一 claim へ混ぜない。全10版の source ID と非実行 history 8 file は、実行 closure 21 Python + 3 raw と分けて全保存される。

全5 execution start / result、P 後 C 前、always / final run と audit materials before / after を追跡した。live receipt に存在しない audit_materials 字段を発明せず、凍結 driver の呼出し順と実 launch / API / 17 親 / pre-P controls で間接結合する部分を明記している。call coverage=NOT_MEASURED、共有 TCB、第三の数値独立性なし、candidate / cross_checked / verified の保証限界を保持する。ZIP の局所全 EOF / SHA と、GHA 保存票に明示された CRC 読取は区別し、局所 CRC 再計算を主張しない。

F10. 1081-R1 に対応する二層の receipt は、旧 batch-fixed-reference-receipt.json と新 next-batch-fixed-reference-receipt.json の別 basename / plain17key として全接続を再読した。参照側 directory は manifest 一件、旧64の original manifest は exact8key、元16 descriptor / 全17 fileを本来の旧64 payload へ結ぶ。JSON descriptor の五→三key射影と binary の五keyを混同せず、geometry の親も結ぶ。両 receipt の intake / acceptance / pre-P / P start / always readback / preservation flag / final run pin を追跡し、排他的 save の衝突だけを避けて参照を失う実装ではないことを確認した。always で票が形成されたことだけから、未実施の数学入場を受理済みにしない。

F11. 第四群は P 28 file / C 15 file の全 tree、全 JSON 読出し、7 正負対照の順序、保存 observed_error / rejection 票 / ledger を公開型へ結ぶ。C の7ケースは正例から一箇所だけ変えた宣言を個別に照合する。P の公開 body / label / positive inventory と全前後 bytes も結び、公開されていない共通内部型を作らない。原三群に属する P17役 / C歴史16役という非対称はそれぞれの実 fixture で保持する。期待拒否件数は P[30,10,6,7] / C[28,9,6,7]、群の格付けは数学2 + 親 metadata2、driver は登録済み16 metadata対照で数学0である。第三・第四群を新たな full1706 算術や第三独立計算と呼ばない。既存 DEPENDENT fixture も全保存された metadata / bytes の範囲で追い、実行結果を本便で生成していない。

F12. cost は exact15key、8秒欄、6相、全 phase count と登録 input の field / unit / 全 file pin を公開 serializer から比較した。base4票と各 phase を、complete 候補では順序付き 8 + 6*processed の入力へ結ぶ。P residual は P total から P の selection / 各相 / final を引く signed 値、C total と P+C total は別字段である。全17親の規模・tuple・旧新 source の文脈を残し、歴史 P の 232.786064 秒を新速度の gate や予測値にしない。

追加 double partial-sum helper は小さい metadata 集計専用として型 / finite / intermediate overflow / 打消し / 同符号 tail の halfway 補正と caller を静読した。PlainInt / double / Decimal の有限値に限定し、bool / NaN / Inf を認めず、許可された residual だけ負値を保つ。SameCostNumberV5 は tolerance を加えず、変換後の exact finite double を比較する。PASS / NEGATIVE_RESIDUAL / INCOMPLETE / INVALID_METADATA は別 status であり、欠品を成功値にしない。ただし PowerShell 5.1 上での実行も CPython math.fsum との bit-exact 実測も本便ではしておらず、その一致が事前に証明されたとは判定しない。一般 Same / PlainInt / parser を緩めないまま、実受領で確認すべき資源 metadata の限界として残す。

F13. 必須 finding は次の2件を author / root へ即時通知し、別 immutable draft07 の全差分で閉じた。いずれも実 artifact の破損を観測した所見や実 GHA 失敗ではなく、静的な型・登録入力の不足である。

| finding | draft06 の不足 | draft07 の限定修理と閉鎖根拠 |
| --- | --- | --- |
| 1083-R1 | cost context.parents[].status が -ceq / -cin だけで、左辺配列の一致要素が true 化され得る | status の string 型と OBSERVED / NOT_CREATED / INVALID の3値を先に要求する。全 receipt側 scalar の通常境界で拒否し、一般比較関数は不変 |
| 1083-R2 | cost input の manifest key の有無から phase か否かを決めるため、phase の key を削ると base7key 側へ落ち得る | 登録 base4 filename と限定した phase path 文法から7/8keyを決め、各 phase manifest を対応する実 /manifest.json へ結ぶ。candidate ordinal<128、全 phase manifest / payload pins を保持 |

draft06→07 は ReceiveCostReceiptV5 のみの修理で、関数外の全 prefix / suffix raw は不変だった。両修理後の全本文 / main を読了し、required finding 0 を author / root へ通知した。作者凍結名へ至る追加 source 差分は 0。実行を必要とする未観測事項は F2 / F12 のままで、静的 finding の未解消と混同しない。

F14. 正式 source / 配置契約の固定値も公開目録へ結ぶ。これらは 1081 の独立別読と今回受領器の登録照合の入力であり、本便が新配置や発射をした記録ではない。

| 公開対象 | bytes | SHA256 |
| --- | ---: | --- |
| P5 / task1082-P/d972_r07_fixed_lambda_cycle_batch_v5.py | 366644 | 664f593a4c9b6eb5d088960215674175a123d7f5a5f2bb3e134d3cb0e16c1c66 |
| C5 / task1082-C/root-review-checker-v5-bound-v1.py | 336193 | 47cf2596e9e9dabaab89395f5274ce15b9443002922ba7bfdbca42022979de73 |
| driver / task1079/review-snapshot-v2/driver.py | 1145254 | f7181bc573c3aff041d6fff3520266ca401de6416b410d145c94aceaf3a18913 |
| WF / task1079/review-snapshot-v2/workflow.yml | 26294 | f5abb0c604a53142accf6c02fb092cee1e448cba27ff428f67be4788894cc0d3 |
| registry / task1079/review-snapshot-v2/inheritance-registry.json | 499053 | e30a6bde668f0778932f0c4fbd62752c698bd70b97e9b097dccde4e9348c2858 |

本文静的採否を閉じるための未接続箇所は 0。launch / artifact / approval の後着登録と全 helper 実受領は未実施で、完成候補用の guard を閉じたまま最終票を凍結する。元 P / C / WF / driver / registry / 親 artifact / 旧受領器 / 作者 receiver と公開済み返信は変更していない。candidate=false / cross_checked=false / verified=false、本票は新しい数学矢印・GHA 成功・実候補受理を追加しない。

AUDIT_1083_VERDICT: STATIC_CONTRACT_PASS; REQUIRED_FINDINGS_0; R1_R2_CLOSED_DRAFT07; COMPLETE_CANDIDATE_RECEIVER_SCOPE_ONLY; GUARD_CLOSED; RECEIVER_LAUNCH_ARTIFACT_APPROVAL_BINDING_PENDING; NO_SOURCE_OR_RECEIVER_OR_FIXTURE_EXECUTION; CANDIDATE_FALSE; CROSS_CHECKED_FALSE; VERIFIED_FALSE.
