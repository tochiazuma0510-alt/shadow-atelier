# Task1191 C — 独立 C10 設計・実装の静的納品

Helmholtz / 既存 C author。Task1191、1191a、1191b、裁定2293/2294/2295、root の20件維持裁定を適用した。2026-09-13 時点、C10 draft-v2 の自己静的別読と公開接続票を完成した。P10 最終 opaque descriptor は未供給であり、`CURRENT_PRODUCER_REGISTRATION` は **None** のままである。launch_ready=false。C10 の実行・import・AST・compile・selftest、P source/diff/fixture/current-count table の読取、Git/GHA/network/credential 操作、新 agent は全て0。

R = `C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163`。以下の新材料は R/task1191/C 以下に CreateNew/versioned 保存した。現 source と公開票は未測定を null のまま保持し、未発射 run の成功値を補わない。

## F1191.C1 — 現 source と残る1束縛

基点は自己 C9 repair2 `task1189/C/final-v1/search/check_d972_r07_fixed_lambda_cycle_batch_v9_repair_v2.py`、758932 B / `66132850f7dc4ff1edda0d5fe9bce565356fd84b0a10ca1ede328cd65d5b4ffa`。

現在の納品候補は `task1191/C/draft-v2/search/check_d972_r07_fixed_lambda_cycle_batch_v10.py`、**870098 B / `35e06aea469182866c5bc4da44d35f49f5c519173f34adcdd6acd690948ad6ca`**。291連続区間、11131 LF、CR0。基点263区間から旧18区間を明示変更し、新28区間を追加した。全数学 source の実行は行っていない。

draft-v1 は870108 B / `1813ad1068d83c1558d8af9ed4188ef5cd222bb36549c63e098b6ebf72097b76`として保存した。root が発見した第22親 artifact 名だけを v2 で修正した。実名は `d972-r07-fixed-lambda-cycle-batch-v9-candidate-34717506638-1` であり、`repair-v2` を含まない。歴史 workflow basename `d972-r07-fixed-lambda-cycle-batch-v9-repair-v2.yml` は正しく、保持した。差分は prefix 中の10 B削除1箇所、290 nonprefix raw は v1 と同一。

公開・私有を混同しないため、次の source 差分は root/C author 用であり、他著者への数学本文共有資料ではない。

- `draft-v2/draft1-to-draft2-full-forward-reverse-v1.json` — 1254 B / `863af48bafd59aaf19c53b1c74fca0be45404694a0e3b416d2acf62bdfe1d7d2`。
- `draft-v2/baseline-to-draft2-full-forward-reverse-v1.json` — 180550 B / `e11622715b497dcb9c47eb730b647feec779e265262e6a88b958fd663660f7ee`。全49差分、全EOF正逆一致。
- `draft-v2/all-regions-retention-v2.json` — 96757 B / `2414629683055a57f9f9bf55dd0bd2abc6c4d516021b71029279684d319feb1e`。
- `private-C10-native-v9-clone-full-forward-reverse-v1.json` — 180773 B / `0631b7d7f45781db8e4dc4b714d16be5115f49bad38d57418542a7e278147f73`。新27領域を既採用旧body・同時名称置換・全残差に分解した。新28番目は current observation header。

自己別読では全49差分、27 clone の共通置換後の全残差、新第9群全文、current observation header、v1→v2 の1修正を読んだ。source finding は上記 artifact 名1件で、v2に解消済み。root も全49差分と全残差を別読済みと報告した。

root の有限静的採用票 `task1191/C/root-draft2-static-bindings-adoption-v1.json` は14060 B / `b0f2bb2d9a38c4996dcc1d792b150f2a7e75af6a32676ab0b1e2fd7510309728`（58f4ff/native0）。これは metadata/source 静的採用であり、C10 native 実行結果ではない。P10 None を actual opaque D3 に結ぶ最終差分・全range更新・root再採用が残る。

## F1191.C2 — 独立和、実親、current/history

Pの登録表を読まず、自己の名前付き128行定数7個、基底rank1450/generation8155、元祖先32+65から導出した。current は22親・7層、previous768/total896、rank2346/generation9051、previous ancestry865/current ancestry993、5376 phase manifests、5404 checkpoints、7 invocations、pairing点1450/1578/1706/1834/1962/2090/2218/2346。current acceptance/start/intake/layout は13/64/81/15 keys。

`CURRENT_*` は歴史5層、`V9_CURRENT_*` は歴史6層として保存し、新 `V10_CURRENT_*` 14式を ordinary current consumer へ接続した。current intake 内に残る旧定数は途中の歴史anchorを表す。保存 native-v9 の21親・640/768・2218/8923・737/865・12/59/73/14を current 値で置き換えていない。

実公開 native-v9 metadata 17文書を全登録モデル2256957 B / `34ebee5249dfc275693a0c595ce0497239c5f775c45cdf6c65ec21a32c091187`へ結んだ素材票は `public-native-v9-metadata-inputs-v1.json`、43720 B / `f75c60f66d446e8c713cf5ec4e375f5827d75596191a8a1fc9278560cc9df8f3`。この範囲ではbinary要素を復号しない。新 native keyset helper の14表と別入口 acceptance12の全15 keysetsを実公開値へ独立一致させた。

第22親の実 formal5 は `run34717506638-reception-v1/root-v9-formal-inventory5-v1.json`、229 B / `1ec2fa54222c792b90d77ac2e0db9c84945ebd09b4781badbd3a23d9ab383f2e`。files12348/file_bytes1581230483/directories3679、files_sha256=`723f202c912420e2094259e1e09d60d51f7d4be078ac820c2cb818481d822b49`、directories_sha256=`8a53bbc3c6b15a7ee5ef48e90a2d3a928c5c6d311f66dc35494761ad08e050c9` を使用した。

root formal/CV9採用票は同dir `root-v9-formal-and-cv9-mathematical-adoption-v1.json`、551725 B / `f90d9eca4b61ed6ac6f8d3e243e4747f0ebd7f0c6b6a3af8a5e8e5cdc4978cc7`。2293/2294限定8、cross_checked=true/verified=false/A0_actual0/1という歴史root裁定の出典であり、C author がこの数学採用を再実行・自己発行したものではない。55 dirs は認証済み登録モデルの値で、新たなlocal復元/leaseとは主張しない。

## F1191.C3 — ordinary 自己検査と current exact7

23関数＋2class の旧selftest専用clone案は root が不採用とし、実装していない。旧8群の順序・件数28/9/6/7/8/10/14/15を保持し、新第9群20件を追加した。合計117件は source 上の登録数であり、実selftest PASSではない。

第1群は current acceptance 正例へ `batch_anchor_v9:{}` を1項追加しただけで、その他の関数rawを保持した。current schema/実checker source D3/22 role/WFを従来の `check_acceptance_header`、`check_executable_paths`、`compare_root_records`、`invocation_records` 等の ordinary 経路へ渡す。旧負例のv2 schema、固定v6 P/C basename、数学値・ordinary type・目的labelを保持した。

第2群 `k128_roster_canary` と従属publication canary の数学bodyは全raw同一で、同じcurrent `k128_fixture_records` と普通の選択・phase・publication・roster readerに接続する。これらの fixture-only root records は限定synthetic値であり、実親の13/64/81/15全入場試験を通したとは主張しない。

旧第3～8群は歴史固有payloadを保持する。第7群の負例schemaは元意味のv9へ明示固定し、第8群は元21親を `V9_PARENT_ROLES` に固定、負例schemaも歴史v9へ固定した。第8群の640→512/768→640、全15目的は保存した。保存wrapper自体はcurrent document schemaへ再束縛するが、歴史payloadへcurrent値を注入しない。双方向schema許容やglobal切替を加えていない。

第9群は採用済み `public-C10-ninth-exact-value-design-v3.json`、33574 B / `b3186b8f2a704f61fc578122a3b59332af5e5b45e991b7d66d7c539cc9073b79` の20件を実装した。v2に混入したPowerShell `{value,Count}` wrapperは v3で bare21 arrayへ1箇所修正済み、他値は同一。ordinary正例を先に呼び、唯一の登録変異に対し exact `cycle_batch:` 目的labelを要求し、保存positive/negative/support/rejectionをreadbackして台帳D3を作るsource経路である。synthetic観測配列EOFと native73 header/sealのcaseは、実親の全物理EOFや下流算術の肯定に格上げしない。

current formed `batch_observation` は exact7、`old_side_recomputed_in_this_run is False`。true・整数0・欠品を別の3負例とした。ordinary writerとP-result比較は新headerを直接通す。C4 `compare_diagnostic` 本体には手を入れず、元のfull canonical比較へ新writerの exact7/False期待値を供給する。歴史native-v9以下はexact6のまま。初期whole null、最初のadmittedFalse、以降の逐次代入、sequence−1/3/9、FAIL/UNKNOWNの最後に到達した値を保存する。old lambda2218の35647/index242/edge489は保存値で、新lambda2346のoracleは未測定null。old側の再計算はない。

## F1191.C4 — 全consumer、raw保持、計器

current source の291全区間、916登録constant出現、3702定義名参照をraw座標で列挙した。文字列・宣言を含むlexical索引をASTや実call graphの証明と混同しない。その別票で新27ordinary production helper の各直接callerと、新selftest入口1個を実rawへ結んだ。selftestの宣言interfaceは実79件。

C4名義24/実21区間と旧saved-row/progress/promote/historical-intake計23本は基点raw同一。authentication原wrapper群・operations原wrapper群・ordered・preservationの本体も同一。計器登録だけを27 authentication callbacks、42 local function hooks＋3 method hooks、7 native operation windows、14 parser rowsへ拡張した。canonical/shaは自己moduleの既存local aliasであり、このCファイル内の新関数定義と偽って範囲を割り当てていない。

条件付きの通常1回全COMPLETE順は137 event = base10 51 + authentication15 54 + operations15 14 + ordered16 14 + preservation11 2 + parser12 2。parser12はeventの12 keysであり、rowsは14。STARTED/COMPLETE/FAILED/UNAVAILABLE、各ordinary型、partial/null、実read/parse/unique/repeat、signed残差、no-call0の限定を維持する。missingや未観測を0にしない。PとCの計器範囲を同一視せず、nested inclusive秒を合算しない。計器は数学gateではない。

登録はmain actual枝で一度、元callableを全captureした後に置換し、原引数/返値identity/原例外を一度だけ通す。27原callback間に互いの呼出を追加していない。original FAILEDとobserverfaultの併発でも元例外を優先する。最後は元順の bundle.unchanged → inputs.unchanged の実区間 → files.unchanged → main parser context終了である。

## F1191.C5 — 公開最終材料

次の全ファイルは `R/task1191/C/public-draft-v2-complete-v3/` にある。数学private本文は含まない。Noether/rootへ実pinを直接共有済み。過去契約のraw座標は歴史provenanceと区別し、current reader/parserの座標はv2で直接再結合した。

| 材料 | bytes | SHA-256 |
|---|---:|---|
| public-C10-draft2-material-manifest-v2.json | 5985 | ec7c471c9802cdce76041eb669b6c34245a0f3023a6f7a9430093960650015c7 |
| public-C10-author-static-closure-and-real-edges-v1.json | 98719 | 06ea79ccea61533077da6d35ae3a5ccedb4137df3704ba95e3893af45cffbd3e |
| public-C10-all-current-source-consumers-v1.json | 1577809 | ae3e7ffe0d1a987f8fe87d7627b772480b9638758ac7fbb353f85ab558eed06c |
| public-C10-retained24-and-native23-v1.json | 25976 | 0f178fe1f654bbed00b81c82670b72509f7fb204992c27f81972b426a20081fd |
| public-C10-wrapper-and-parser-actual-connections-v1.json | 506985 | a925d22c5776ef4efc4e3559ec33fdd608f12bf30b989a1e4783bd5a24c6e187 |
| public-C10-telemetry-and-scope-v2.json | 82910 | 19203bcadffbfc286be627f65acc28af459c47ed5efcdf69199a89b6ba591823 |
| public-C10-wire-and-current-branch-overlay-v2.json | 85484 | 41ba85aa690a9aaeb984b06eaaf9966b761ab252c8f9419a08c8f3dd11c95846 |
| public-C10-independent-expressions-and-counts-v1.json | 21107 | 2be98e405dc17603777421bd04b745226d1b5a8ab57b28e5c4744f8cadf07907 |
| public-C10-ordinary-first-two-and-all-nine-groups-v1.json | 62450 | 8739bcaa1ec6f708e4ddc59c9936354ac3147ca4839b6796ad544a071be9ab4c |
| public-C10-native-v9-clone-review-index-v2.json | 30743 | 69b17f37c28edd8cbe87e0b27ae299b92e4b006b20c53a7dd30c6611f0f2835b |
| public-C10-ninth-serialized-source-binding-v1.json | 1704 | f43d77730878f30c187076ba47230ff782e3d64394fcd01b4126682d4397b64c |

metadata author scriptはsourceをbytes/regex/JSONとして読むだけである。最初の3版のclosure生成はlocal aliasとsha256 categoryの列挙assertで停止し、v4が完了した。最後のfieldset抽出も大文字fieldを含む字句集合へ訂正した版で完了した。停止版と部分材料は保存し、これらのmetadata helper終了をC10のnative/selftest成功とは扱わない。

## F1191.C6 — canonical調査と権限範囲

`public-C10-canonical-and-loop-investigation-v1.json`、15985 B / `af4f8a3d902560b5863bcbf08ec14d1702b09c333171cc9832b503ee9731c891` を納品した。実旧Cの6 native窓ではcanonical1420回、first loads149回、read/pin185回、seal/helper49041回、sha326回。第2→第3層168→11940は、第三inventoryの11750 filesに対する descriptor helper各1回と残る22回の増分で説明でき、残る22回の個々の内訳・時間配賦は未同定である。11940は11750+190であり、すべての算術loopや残余機構を解明したとの主張ではない。

回数は同一parsed object数とは異なる。same_jsonの2canonical、seal projection、first/repeated loadsのrole/path/callback範囲、UTF-8 decode除外、read/pinを純IOと呼ばない点を明記した。Pの22663/4773をCの計器へ移し替えていない。参考0.343194秒を将来の再構成の時間下界にしない。canonical重複除去・cache・最適化は実装していない。

current source/WF pathとname/markerはTask1191指定のv10 identity。凍結54432/108864/54433、k128/max1/no-refill、元算術・caps・C4・著者分離を保持する。F-v9-2のauthor D3はroot全文別読へのprovenanceであり、実runがauthor文書を再認証したとの主張ではない。F-v9-5/7/8のP子process・公開driver/WF変更は相手のprivate sourceを読まず、公開担当/rootが閉じる範囲である。

残作業はrootからの実P10 final opaque D3到着後の1token束縛と、全range/差分の版更新・root最終採用。新C10 runtime結果は存在しない。

AUDIT_1191_C_VERDICT: STATIC_DRAFT_COMPLETE_P10_FINAL_OPAQUE_UNBOUND

## F1191.C7 — 実opaque最終束縛とroot採用（後着追記）

本追記で前段の P10 None 状態を更新する。root から実P10 descriptor `{file:search/d972_r07_fixed_lambda_cycle_batch_v10.py, bytes:1034265, sha256:33c4bbb97313bc1ea2017b6ac6ad2cc0932ae15d1affc8bcd6a8aaedd0c76085}` と採用票 `R/task1191/P/root-final-source-adoption-v1.json`、4057 B / `c62c7fd3d479420d1399d233d177ae29ad53b8299a76d09d580be41958c0f11d`（b08f0e/native0）が届いた。採用票をraw hashで確認し、P source本体・private資料・P登録表を開かず、提示されたopaque3値だけを使用した。

最終 C source は **`R/task1191/C/final-v1/search/check_d972_r07_fixed_lambda_cycle_batch_v10.py`、870249 B / `a21fd2b54958f84ea67e7b3a079893cff70544961005d6c79a0f6ff47e752ca8`**。`CURRENT_PRODUCER_REGISTRATION` の RHS `None` 4 Bを、実one-line ASCII dictionary155 Bへ1箇所束縛した。+151 B、11131 LF不変、他の全raw bytes不変。全290 nonprefix body・C4名義24/実21・旧native23は同一。最終source pinは先にroot/Noetherへ通知した。

source差分は `final-v1/draft2-to-final-full-forward-reverse-v1.json`、1802 B / `331f83b0b7bc1f1f4fcab995f87d9fdbee06f68ea6a30d9e710a721d275b7a77`。whole sourceの正逆一致を実bytesで照合した。sourceを生成したmetadata-only binderは109ed6/native0、公開票再座標化は899b0b/native0。いずれもC/P数学targetの実行ではない。

root C最終source採用票 **`R/task1191/C/root-final-source-adoption-v1.json`、3314 B / `66063f8211dd1078e6b7455f46c7332e20c4cb38ed41a3f91f46439055e7c7be`**（75f415/native0）を受領した。rootもactual P None→D3だけの全正逆一致を採用した。source変更はここで終了し、runtime結果はnullのままである。

最終公開材料はすべて `R/task1191/C/final-v1/` に固定した。current291区間と公開接続7121箇所の前後SHA/byte span/最終占有行を実rawへ再照合し、13公開材料と最終sourceをfresh pin照合した。計器13 semantic subtree、current wire9 subtreeはopaque座標を除いて前稿と全JSON同一。137条件付きevent順、14 parser rows、current exact7/false、historical exact6、全case/型/値を保持する。baseline/previous/historicalの出典票はその時点の値のまま保存した。

| 最終材料 | bytes | SHA-256 |
|---|---:|---|
| public-C10-final-material-manifest-v2.json | 7332 | e7d76cf0d97e5152eb760eb1c968ebc922d46503249cd82bc3c2ed79a7b06af0 |
| public-C10-final-author-receipt-v1.json | 3693 | 52a26c62eff0c1a557d10cb8fa93ef78f052264a91cfb6e01c2bc7a0eb38258e |
| public-C10-final-opaque-binding-guard-v2.json | 2880 | b611249ef513cc528173f6c8c1cf1a43d0c9bead3e06be31e9026e870ec1e13a |
| public-C10-final-all291-ranges-v1.json | 126383 | a4b32d9057fea17f69b6c5795369f46a02a0912fa9b94dd91129ac21ecef12fd |
| public-C10-final-public-range-rebase-v1.json | 4598382 | 39b704a66a2b959bc38153b420ce856b765a9e521c7d93adade37219baa86e02 |
| public-C10-wire-and-current-branch-overlay-final-v1.json | 87205 | c5ab4ae44cf9a67c22e04bbcff9cbc5c8316120a69608f78476d5978a0b66426 |
| public-C10-telemetry-and-scope-final-v1.json | 84329 | cd70f01fd81efdc8f6b113475806e0ce3e085eab3707bd79bfee859a2a30d52a |
| public-C10-retained24-and-native23-final-v1.json | 27422 | aa89c458462a71bcf99e1f1e16f790b8ce7eed0e2ba325c4aed7730d23eed746 |
| public-C10-all-current-source-consumers-final-v1.json | 1579262 | 7fb703ed7e7940950046eec37de828dcb62322878a07f383ad6887a71933c10b |
| public-C10-wrapper-and-parser-actual-connections-final-v1.json | 508436 | ee164384bba8a78ee5d869b58da9e5f67fc32305433b2c24cb017ef505ba36e2 |
| public-C10-ordinary-first-two-and-all-nine-groups-final-v1.json | 63888 | 08ed266f8fe2aff0f414c4f08850d9989fb3876964be6db597740cdd767033c9 |
| public-C10-ninth-serialized-source-binding-final-v1.json | 3121 | 30de5f6937f258a3b73fc911c72de4494e65246ad23ecf3269b531da5c536ce8 |
| public-C10-author-static-closure-and-real-edges-final-v1.json | 100173 | 863207cdac712b65c3fc4fa15a8027aa212a8db70ffe1e93b3072a4d115c3ba5 |
| public-C10-independent-expressions-and-counts-final-v1.json | 22554 | 920e0b1f4330f8ce2014fd0e873ffeab761eaa0448fa6d5a931071de6d966b76 |
| public-C10-native-v9-clone-review-index-final-v1.json | 32184 | 41681d29bf7c5a9b5270e9e5698454ec2ca3f65d831b7972596ad456ee8a07bc |

最新guard/receipt/manifestはrootのP/C実source採用票へ接続した。旧guardのroot_C_final_adoption=nullは発行時点の記録として残し、v2が後着採用を記録する。新source・public域の静的納品を完了した。実driver/WF統合・配置・GHA・runtime受領はrootの後続範囲であり、C10数学target実行/import/AST/compile/selftestは引き続き0。

AUDIT_1191_C_VERDICT: FINAL_OPAQUE_BOUND_ROOT_STATIC_SOURCE_ADOPTED_TARGET_EXECUTION_ZERO

## F1191.C8 — current参照18点の公開座標訂正

root の公開票joinで、`public-C10-all-current-source-consumers-final-v1.json` の `/symbol_references/historical_v4_loader_pairs` から `historical_v9_loader_pairs` まで各3点・計18点が旧座標のままと判明した。再座標化helperが `historical_*` というkeyを一律provenance扱いし、**current関数名をkeyとする参照辞書**まで除外したことが原因である。source本体・全291region registry・算術predicateには変更がない。

consumer-final-v2では18個のoffsetだけを+151へ修正した。各beforeはunbound source、afterはfinal sourceの実raw SHAに一致し、bytes/hash/line/columnは同一。consumer JSONの他の全値・全rawは同一で、完全なJSON18差分とraw正逆差分を固定した。元consumer-v1と採用されていない旧公開票は保存した。

今回の全数照合は、実baseline/previous等のschema上のprovenance欄だけを明示除外し、current `symbol_references` は関数名によらず全keyを走査した。**全current7430範囲が実final bytes/SHA/最終占有行に一致、不一致0**。訂正前の不一致はこの18点だけだった。F1191.C7の初回確認は「列挙された7121座標変換」の前後一致であり、誤って除外された18参照を捕捉できていなかった。修正後は、明示的に更新した291regionと、全7139公開参照変換を合わせた全7430範囲を閉じた。

以下が同じ `R/task1191/C/final-v1/` の最新版。依存票の変更は訂正consumerと関連公開票のD3参照だけで、schema/型/value/137順/14row/第9群20caseは同一。guard-v2、source870249/a21fd2…、root C採用3314/66063…は不変。

| 訂正材料 | bytes | SHA-256 |
|---|---:|---|
| public-C10-final-material-manifest-v3.json | 8445 | 3bf37966a8c53896e9fc486f6aca32b5489d2364d5729f0779e188311e82c8b8 |
| public-C10-final-author-receipt-v2.json | 5055 | 1dd9d359dde4b9cde8fe641b4e101cca450219e0791baaff3194d6d1797b2c90 |
| public-C10-all-current-source-consumers-final-v2.json | 1579262 | 912f180c826c78a388b548d89ac025b796ad888a579b2c07a6014748d3fa5c23 |
| public-C10-current-reference18-full-forward-reverse-v1.json | 5579 | fc1145c4b9ae45ecdaf20a8a10caa9fde41f7648753078fbbeb1000100cc44c6 |
| public-C10-all7430-current-ranges-fresh-audit-v1.json | 8026 | 38bfc54a3b3c133eabef22fbe8768ea06618a56d4823512f7d7b7b2a893a7267 |
| public-C10-final-public-range-rebase-v2.json | 4610870 | 572efc4db91075de70fd9200bf5c8953eeafba96e222e111f98da5f241e3f77d |
| public-C10-wire-and-current-branch-overlay-final-v2.json | 87205 | 8698c64a850f60cf96500bbd1fb3a1089b9935cbbe1342149db19e54606645c3 |
| public-C10-ordinary-first-two-and-all-nine-groups-final-v2.json | 63888 | f1d15a55c68dedfabbff1252fd06e4c619dfc82cf765b99c980c02de85064b0b |
| public-C10-ninth-serialized-source-binding-final-v2.json | 3121 | 376d5fe899106ad2a465e8a7b3c7432dcb49392e732daed2ab045afa18d6e2de |
| public-C10-author-static-closure-and-real-edges-final-v2.json | 100173 | 71acac480657549c2ffdaa1c3b5b7634f13868b471488e667034699aed75027d |

訂正をroot/Noetherへ共有した。C sourceの追加修理や数学target実行は行っていない。rootの最終公開票joinとdriver/WF統合は後続の独立採用として扱う。

AUDIT_1191_C_VERDICT: FINAL_SOURCE_UNCHANGED_PUBLIC_COORDINATE18_CORRECTED_ALL7430_MATCH_TARGET_EXECUTION_ZERO
