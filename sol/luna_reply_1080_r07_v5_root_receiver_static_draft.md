# Task1080 — v5 全 envelope 受領器の静的草案

F1. 通常受領経路まで接続した未実行の静的案を作者凍結した。`T = C:/Users/81905/AppData/Local/Temp/shadow-atelier-audit163/task1080` とし、正本は `T/root-review-receiver-v5-guardclosed-v1.ps1`、516693 B / SHA256 `b54e58f1bc33df144a3c2e6b20dc14a8b963356b914028148a965a758c15dbb3`、LF4626 / CR0 / ASCII / BOMなし / 最終LF / 行末空白0。`audit-r07-batch-v5-metadata-v1.ps1` と `draft-07-cost-registered-input-types.ps1` も全 bytes 同一である。全受領器・cost 関数を実行した回数は 0。ExpectedLaunch / ExpectedArtifact / ExpectedApproval は null、最上位 ImplementationComplete は false のままで、静的完成と実取得の登録を分けた。

Task1080 全文、1074作者票、1077/1078 の公開 interface v1/v2、1079公開 serializer v2・fixed-reference R1・最終 binding v3、1082正式 inventory 契約を読んだ。P5 の私的 source／差分／作者票や Task1076 source-body material は読んでいない。公開 opaque descriptor と範囲表を読むことを P の算術本文の共有にしていない。

F2. 基点は `T/baseline-1074-v4-metadata-v5.ps1`、261800 B / `dcccf94a7eb3458d6cf709478a449d3377f86e5b90edfa0a9f011d82122ac411`。全 EOF を、column-zero の関数開始と通常 main 開始により、基点62／新版96区間へ raw 分割した。59区間同一、3区間変更、34区間追加、削除0。保存した changed/added raw と同一区間から新版全文を再構成し、逆方向も基点全文と完全一致した。これは文字列・bytes の静的比較であり、AST／parser 実行ではない。

旧60関数の本文は別の raw body 範囲でも全件同一である。一般 Same／PlainInt／Fields／Pin／JSON 読出しも不変。区間名 `function:ManifestFiles` は関数の後ろに続く main も含むため区間としては CHANGED だが、ManifestFiles 関数本文自体は同一である。変更3区間は PREAMBLE、MAIN_PREFIX、この main 後半区間であり、旧数学 source の修理ではない。

| T 内の記録 | bytes | SHA256 |
| --- | ---: | --- |
| full-raw-region-index-draft07-v1.json | 695572 | 8bd73c188cf6b31941118fc7cf799ae80be31718643e1797c68b0228c2fc8f4f |
| full-raw-diff-draft07-v1.txt | 390983 | 586aa7e13fac5937b862daa126cb453b48236d5c6599f88259eb16087252b170 |
| full-raw-review-summary-draft07-v1.json | 543 | 818e86dd89323c4d7d115c183f904d6b2d3824adbe2694e9617855d1e8e7daf6 |
| author-static-self-review-v1.json | 7578 | 412f08513487286740486f7611c7a0b13574f6b4f5fa4e8f7a3be7fb968cf319 |

F3. 新 main は v5 schema／plain acceptance 8 key／17役を受ける。旧 `batch-parent` は v3、追加 `batch-parent-v4` は v4 のまま保持する。1450→1578→1706、97→225→353、親の128+128行／1536 candidate phases／1544 checkpoints／2 invocations を別々の実保存 prefix から結ぶ。各親の772 checkpoint は sequence0..771で、最後の separator phase を checkpoint772 として足していない。current の previous target は v4 `start.target_remainder_sha256`、current target と選択 lambda は v4 final の値である。

`ReceiveHistoricalV4CompleteEnvelope` は基点の通常 main 全射程を明示的な local v4 binding の下で通す。旧全 source/TCB/registry、16親、v3保存prefix、固定 reference と原64の全16 payload、全 file/dir、全 ZIP、全 fixture、全 invocation/checkpoint/row/phase、全 before/middle/after、最終 REPORT を省いていない。歴史 root metadata PASS 票の読出しやキャッシュで代替せず、その呼出しで得た実 metadata を返す。歴史 main の末尾は外部票への書込みから内部結果の返却へ変え、歴史 fixture reader は復元計画を読んだうえで未復元0件を要求する。歴史親への mkdir は行わない。local の歴史 guard=true は原 v4 の既知 binding に限り、最上位の未登録 v5 guard を開かない。

F4. root1074 session5057 が 5994.9909333 秒後に旧 v3 空36 directory の未復元で停止したという実所見を反映した。`PreflightReadOnlyParentTree` を全 payload hash／source body 照合／新 REPORT の復元より前に置いた。固定 pin の run/envelope から完全な file 名・長さと directory 集合を構成し、実 tree と照合する。欠けた登録 directory があれば role／実 root／全欠品 path／期待数・実数／parent_tree_written=false を付けて早期拒否し、root の復元 handoff に戻す。子が数学親を直す処理は追加していない。

正式 v4 inventory は root の後着1082による。11648 files／1308094050 B／3525 directories、正式票7022 B / `64e3f8e6a434be335a88c1dee6efa4aae7b3d669faac28e704aefd0f8e3f4753`。canonical files 全配列1931889 B / `ffec515b0a235ce2dd99770e51619252c725269970b71e32180be5f14cafaff5`、directories 全配列200290 B / `f9562484c91c05c517b50065d86e1a88f16af6b1e3198b1d0ba1adb645f9dc64` を helper の sibling に保存した。両材料自身の full pin と全配列を通常入力に結び、その後の全 payload 再 hash と完全一致を維持する。formal inventory 票を full typed metadata の PASS と読む処理はない。旧 v3 の空36復元／全11437 file の前後不変は root の別作業であり、今回の子の実行成果とはしていない。

F5. 公開 final-binding v2 により、以下の実 source／配置／registry pin を定数へ接続した。これらは実 v5 artifact の受領値ではなく、公刊済み実装の登録値である。

| 公開対象 | bytes | SHA256 |
| --- | ---: | --- |
| P5 | 366644 | 664f593a4c9b6eb5d088960215674175a123d7f5a5f2bb3e134d3cb0e16c1c66 |
| C5 | 336193 | 47cf2596e9e9dabaab89395f5274ce15b9443002922ba7bfdbca42022979de73 |
| active v5 workflow | 26294 | f5abb0c604a53142accf6c02fb092cee1e448cba27ff428f67be4788894cc0d3 |
| REPORT driver | 1145254 | f7181bc573c3aff041d6fff3520266ca401de6416b410d145c94aceaf3a18913 |
| current full registry | 499053 | e30a6bde668f0778932f0c4fbd62752c698bd70b97e9b097dccde4e9348c2858 |

registry は整形された full bytes 499053 を正本とし、別の compact 428925 B と混同していない。current／historical v3／previous v4 の三票を別々の full pin で読む。10 source、8 historical copies、4→5の全2 transition、3→5の8 loader、4→5のP37/C20 body保持を全範囲で結ぶ。P37内の4 loader を追加の独立件数にしない。正式 inventory の exact4 wrapper、内側の正式5 key／root receipt pin／full_typed_parent_metadata_complete=false も照合する。4 shared kernel は既存の同じ table に結び、call coverage は NOT_MEASURED、第三独立性の追加はない。

小WFの起動／終了時11 SHA行、旧巨大WF／旧小WF／受理済みv4 WF・driver の別配置、五 execution の実 argv、pre-P controls、開始／終了／P後C前／always／run の全結合を読む。source／registry の全 EOF を retained opaque bytes へ結び、実装を import しない。

F6. fixed-reference R1 は旧 `batch-fixed-reference-receipt.json` と新 `next-batch-fixed-reference-receipt.json` の二役を分けた。各 plain exact17字段の元 reference manifest、原64の全17 file、JSON5／binary11 descriptor、実 oracle geometry inventory を読み、親の fixed directory に payload が複写されたとは扱わない。acceptance の二役 pin map、sealed exact8 の `fixed-reference-receipts-after.json`、run／preservation.flags の両 full pin を接続した。

本案は完成 candidate の通常受領器であり、この入口では両票の実形成を要求する。WFの early required=false／両未形成null／片方だけ形成という診断型を完成 admission へ上げない。既存の early-failure 専用受領器を新設したとの主張はなく、今回の completed main を未完 artifact へ適用して PASS にする用途でもない。完成 packet 内に保存された resource-stop.json／rejected.json は、各型／自己の invocation と checkpoint／全 pin／保守的 observation を別々に読む。

F7. current は1706行の全 insertion-order source と、採用済み新行だけを prior-only に結ぶ。全係数列には0も含め、旧353件と新採用の十key target record を全件連結する。普通整数 scalar、target JSON 全hashとpacked remainder hash、instruction rolling、row manifest、全6 phase、実 checkpoint、最終HEAD／final／P／Cを照合する。128件すべてが独立という条件は追加していない。DEPENDENT の row・normalization・target は型付きnull、Linear後の未処理候補には実在しないphaseを要求しない。Linear の lambda はnullであり、零vectorや新oracleへ読み替えない。COMPLETE_ZEROも候補0／phase0の実型として区別する。

selectionの観測は実 progress sequence>=3、first processing は>=9に限る。直後の durable tail を公開countsへ足さない。保存診断の intake 前条件は、後の完成時点でtrueへ置換しない。初回独立の判読は、候補存在・親span零・derived rho2=1・実 raw pairing 非零という登録済み条件の組に限る。旧failed setの単調性や独立率を予測せず、新 final lambda oracle は null のままである。

F8. P/Cの新四群は P[30,10,6,7]／C[28,9,6,7]、旧数学suiteの再走0。第四群は保存された P28 files／C15 files の全名前・directory EOF・bytes/hash・全JSONを読み、正対照／一箇所変異／rejection票の observed_error と目的labelを実bodyへ結ぶ。Cのcase内 `positive.json` pin とWF側の `case/positive.json` pinは同じ実fileへの相対基準の違いとして射影する。Pのplain rejection票をC形式へ変更していない。第四群を1706算術の再演や新full-parent受理と呼ばない。

旧DEPENDENT継続 fixture の116 fileは歴史全scopeの内側で保持する。旧陰性の到達点は expected-file size/hash gate であり、semantic outcome比較に到達したという主張へ変えない。全fixtureの空／hidden directoryとinner ZIPの全entry EOF／SHA、before/middle/afterの全資料を保持する。CRCについてはGHAの申告と局所SHA／EOFを区別し、独立CRCを今回実行したとはしない。

F9. cost receipt は公開15 top／8 seconds／6 phase／7 count／18 contextと、全実入力descriptorを接続した。P全体、P selection、Pの六候補相、P final、P residual、C全体、P+C全体を別字段で読む。current codeと17親の実 acquired receipt、各親のfile／directory／bytes、native pairing rows 1450/1578/1706 とC5追加callという混在要因も記帳する。prior232.786064秒や予想値を今回の成功条件にしない。負のP residualはNEGATIVE_RESIDUALとして保持し、0へ丸めない。

和の照合には cost 専用の有限double partial-sum案を追加した。各入力の加算誤差をpartialに保持し、最後の合算で同符号の未合算tailがhalfway境界を越す場合の補正を明示する。Boolean／非数値／非有限、途中・最終のoverflowは拒否する。一般 Same／整数型／JSON parser は変更せず、許容誤差も設けていない。このアルゴリズムは未実行で、Python math.fsum との bit-exact 一致を達成した、性能が改善した、GTの数学独立性が増えた、とは書かない。全アルゴリズム本文を独立別読対象へ渡した。

INCOMPLETE／INVALID_METADATA のcostは、形成済みpin／欠品／理由／nullを保存型として区別するが、完成 candidate main の最終成功には使わない。完全観測された PASS または NEGATIVE_RESIDUALだけを全実phase数と結ぶ。新phase manifestはfieldが自己申告されたか否かで判定しない。登録済みbase4 fileとphase path／ordinalから7対8 keyを決め、全phaseの実manifest full pinへ接続する。

F10. 自己静読中の修理は、新v4 rowのglobal_row_id、実phase-telemetry schema、C/P第四群の相対pin、三つの新保全flagのflags配下、実v3 parent_layout.code、普通integer bytesとInt32/Int64の区別、17親とmetadata16の別countなどである。いずれも未公開の新版へ保存し、旧sourceや旧一般比較器は修理していない。draft05／06／07はそれぞれの全rawを保存している。

1083からの必須R1（parent statusにstring guardがない）とR2（manifest keyの有無でphaseを自己選別できる）は、ReceiveCostReceiptV5だけを変えてdraft07で閉じた。R1はstring＋登録3値を分岐前に要求する。R2はF9の登録path分類へ接続する。監査官はdraft07のこの関数以外の全文不変、全新body／header／main／歴史wrapper／公開serializerを読み、両点の静的閉鎖と追加requiredなしを通知した。独立raw票は `task1083/independent-draft07-raw-and-static-review-v1.json`、2982 B / `8f0a594ecee46d3301640dd9c53cac568247e605d9e98d14757cf919803ef766`。本作者票はその通知とpinを記録するもので、独立1083最終返信の代わりではない。

F11. 公開23材料を `T/public-inputs/` へ全raw同一で複写し、`public-material-index-v1.json`（14008 B / `ecb07144d4fe33892bb2bd32be6bb30867651ad51908b8fa8c5d8d7e9ce14a4c`）に元pathと全pinを保存した。helper の実 sibling依存は、旧P4用公開二票と、正式 inventory root票／canonical二配列の計5本である。旧P4二票は17587 B / `768cbfec35dae2abc80cade25f184c626bef07a8fefb758383a8669e23a0ebed` と267079 B / `b36818b41ab82ea33e2008e6db921e9cfb4138af472a473b47bbeac2eac063b9` のまま。新P5の非公開source-body fileを追加依存にしていない。

`invocation-and-scope-contract-v1.json` は3016 B / `62986a9433ff7364b05e68a0fbd4efefcb814914c90b1cbb37f77e2305c437ab`。mandatory引数は ArtifactRoot／AcquisitionReceipt／Old64Root／BatchParentRoot／BatchParentArchive／BatchParentV4Root／BatchParentV4Archive／BatchParentV4AcquisitionReceipt／ReceiptPath の9個。新ArtifactRoot／取得票／新外部出力票は未登録である。rootが実取得と全材料を確認する後続の別bindingなしに実行しない。既存親root、archive、取得票、helperのsibling、書出し先の分離も通常gateに残した。

全73材料の `final-static-delivery-v1.json` は19983 B / `5c28026c4fa75e4f45f33d6d1fe1933175ac6e4efe44fb3a85cc543286b81af6`。初期draft、各追加block、全raw差分・再構成票、公開材料、自己票を含む。目録自身と後着の本返信は自己参照を避けて除外している。指定T以外のTEMPや既存source／WF／親artifact／root受領中入力は変更していない。

F12. rootから v5研究run34143415388/1、head2751f8942a50377a13078cbf646cfaaa3845b71f、workflow352449001／push開始・source/registry gate成功・17親live進行の通知は受領した。子はAPIを実行せず、この便のLaunch null／Artifact nullを更新していない。新artifactや新数学結果は未観測のままである。旧親については2206の1706/8411限定7条、2209の正式inventory／復元、full typed旧受領の未完という別の状態を保持する。現在のv5に格付けを移さない。

子の全受領器・dot-source・Invoke-Expression・ScriptBlock化・cost fixture実行、Python／GAP／AST／import／compile／数学、Git／network／GHA／credential利用、新agentは0。作成用PSはASCII文字列の組立、公開JSONの型読取、file hash、raw再構成、材料目録だけに使った。通常helperやその関数を読み込んで呼ぶ処理はしていない。今後必要なのはrootの全静読／1083別読と実取得後の別bindingであり、本便に未接続の通常blockは残していない。

AUDIT_1080_VERDICT: CONDITIONAL_STATIC_IMPLEMENTATION_COMPLETE; IMMUTABLE_SOURCE_AND_FULL_RAW_RECONSTRUCTION_SAVED; ALL_OLD60_FUNCTION_BODIES_RETAINED; R1_R2_STATICALLY_CLOSED; SOURCE_AND_FORMAL_INVENTORY_BOUND; CURRENT_LAUNCH_ARTIFACT_GUARD_CLOSED; RECEIVER_AND_COST_EXECUTION_ZERO; NO_NEW_MATHEMATICAL_ASSURANCE.
