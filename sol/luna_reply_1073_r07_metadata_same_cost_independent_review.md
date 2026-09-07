# Reply1073 — Same比較コスト限定案の独立別読

F1. `LIMITED_SAME_COMPARISON_PASS_GUARD_CLOSED`。1072作者案に残る必須修正は見つけていない。Sameの新旧全文、全差分、作者事前登録二票・fixture全184行・全62対照と20計測値・最終返信全文を読了した。Task1073全文2802 B / `37a611ab1373585a69ccda33d445474ab5c4da78a301ff3f2f75fef9d13f5a5e`、Task1072全文3748 B / `9f6d4d592aca1918115bbb5dbe713f28d5687f13bbba508c9378e8a821333904` の限定に従う。全受領器は未実行で、実candidateの受領速度・数学成果を判定していない。

対象全helperは261620 B / SHA256 `a16d8497aafec0cebc6d1c07cc962024ce344854d6d374810e26dc47ce54cb74`、LF2474/CR0/ASCII/BOMなし/最終LF/行末空白0。Sameだけを戻した全rawは、基点1071の260010 B / `accc758ebe41c6c5a239245a62beb961ef1f145bf04f3154c6b34442ec774e44` に一致した。基点の全受領契約は1071および以前の受理根拠を保持し、本便で全保持本文を新たに読んだとはしない。

F2. 独自照合で、旧Sameはoffset5027/L55–75の1409 B / `b2c9cd7561cadfe70653cbe29bcf9be31cc115599a9bbc42d79764cffb899f04`、新Sameは同offset/L55–105の3019 B / `55a6b4b67a7bdb3c6094cbc8211330caf09248ddee13f0fc0432c14bbdbda73a` と確認した。先行5027 B・後続253574 Bは全raw不変、順方向再構成と完全逆置換がそれぞれ新旧全rawへ一致する。作者および独自fixtureの両比較関数も、公開Sameとの差が関数名と再帰呼出名だけであることを全文照合した。

Need/PlainInt/FilePin/JSON reader/main/全scope/closure/親/phase/fixture/全file・pin・seal・EOFの本文を省略・変更していない。新旧ともSet-StrictModeの記述はない。prefixの実Launch34120585268/1・head92720e5371164545259c3007cb11e951fa5e1686・承認2197、Artifact=null、ImplementationComplete=falseは全raw不変である。rootが別snapshotへ実artifactを登録するまでは閉じたままとする。

F3. 新規の二箇所は、配列要素またはobjectのfieldをlocal変数に置いて、null/string/ValueTypeの判定だけをinlineにした。nullを先に処理し、左右両方null以外を拒否する。stringは右もstringかつcase-sensitive同値を要求し、ValueTypeはGetType一致とEqualsを同じ式で評価する。Int32/Int64、boolと整数、Single/Double/Decimalの等値数を統一しない。NaN/Infinityの対照は元SameのEquals意味を保持するだけで、別のfinite/JSON入場gateを緩めない。

配列container自体の条件は従来どおりArrayであることと長さであり、要素をindex順にすべて比較する。空のint[]とobject[]を同じとする元の挙動まで保持し、containerのCLR storage型を新たに厳格化してはいない。array/objectのchildは従来のSameへ再帰する。objectは元のOrdinal key sort、全key数・全key文字列・同fieldの比較を保持し、順序違いを受理しつつ大小文字・欠品・nullとの混同を拒否する。

Needは条件不成立時にlabelをthrowし、成立時に出力を持たない。inline側も同じ条件・同じlabelをthrowし、成功時には比較結果やleafをsuccess streamへ出さずcontinueする。再帰先からの例外をcatchして受理へ変える経路は加えていない。例外メッセージと拒否を対象とし、関数内の行番号・call stack位置の同一性は主張しない。通常のJSON由来metadataと現受領器のplain PS metadataを対象とし、実行可能ScriptProperty等を持つ任意のPS objectまでの観測同値を主張しない。

F4. 作者事前登録は2223 B / `ecc6e81afdc375667b15c38541156f8c838deb6d8d42fcd4fc06a62c52e5bb16`、exact追補1108 B / `0567f21ab0d31537252c35ccb4b7a4d732e273cf7e225b012b22e2a213d30a20`。22 seedをarray/object双方へ置く44件とcontainer18件の計62件・124比較、warmup4回、timed20回・5roundの先行順交替を事前登録している。実fixture13971 B / `12b8f806d5d7a7fad8912fe3c47ed730aa20dc0e4c0972a38edd2541b0c701cb` と合成入力30707 B / `1ca61b4714843f6abdc378c3b0fb02f685f342100c2c5dde63e9cdf7b46dadb4` を全pinへ結んだ。

作者実結果82547 B / `9ef4889c4ecc3bf4975c25e9be1dcf645bea6466f0bb577d034c398cff3a997b` の全62件の両観測・期待値・例外メッセージを読了し、全一致を独自metadata比較でも確認した。初回表示で切れたfixture末尾と結果票は、末尾の小分け再読と全字段の空白圧縮表示で補完した。作者唯一のfixtureは本体5.6232714秒、正しさ部分0.3576708秒、exec外枠6.2609622秒/exit0。再実行していない。

| 作者が一回のfixtureで測った合成入力 | 旧中央値秒 | 新中央値秒 | 新/旧 |
| --- | ---: | ---: | ---: |
| scalar leaf 512個 | 0.1081056 | 0.0008041 | 0.00743810 |
| metadata record 128件 | 0.5067662 | 0.2300979 | 0.45405139 |

全20実測値から各5値の中央値を再集計し、両方が事前の20%短縮条件を満たすことを確認した。これは保存済み測定値のmetadata再集計であり、新しい性能測定ではない。全file hash、ZIP、disk、その他の受領処理の寄与は測られていないため、前回約81分や今回の全受領時間へ短縮率を掛けない。

F5. 未被覆の具体的懸念は、直接引数からlocal代入に変わる際の「実際に格納された入れ子空配列・一要素配列」の扱いだった。独自TEMPに公開両関数を見える全文で保存し、8ケース/入口16比較、一回、10秒上限・一比較中の超過猶予5秒を実行前に登録した。性能測定や作者62件の再走は含めない。

私の途中説明で「元受領器StrictMode 2」と述べたのは誤りで、root指摘と原helper全文検索で訂正した。両受領器自身にその設定はない。実行前の別scope票471 B / `23367bafa8d17e34403cb51d473cbda75a2764bbd04ae38299e522e94d97a639` へ、独自fixtureのStrictMode 2は外側hostが設定した場合の追加境界であり、新しい受領器要件ではないと記録した。

独自実行は一回0.1899234秒/exit0。格納したempty array、singleton array、object内の両nested arrays、empty対null、container対scalar、外側StrictMode下のempty object、独立に二度JSONから読んだnested arrays、string対singleton string[]の8ケース全てで、期待した受理/拒否・例外CLR型・Message・観測FQIDが一致し、success stream出力は全0だった。StrictMode下のempty objectは両方PropertyNotFoundStrictを保ち、その外側設定の挙動を通常hostの新しい成功条件へ変えていない。

| 独自TEMP/task1073の票 | bytes | SHA256 |
| --- | ---: | --- |
| assignment-boundary-preregistration-v1.json | 1491 | `a7de615b9303bdad6da13f900800d384f110d37685281f04e37d4cd341445e5f` |
| assignment-boundary-fixture-v1.ps1 | 8921 | `d80195c72195d2caaa7d3b73cce5213c928ba1e62050bd040d9f47e1bfd2f27a` |
| assignment-boundary-fixture-result-v1.json | 11941 | `78d0c04fcf9aecf068720981ef9481b5763c293cbcabe9e8662f1d60de0c2c02` |
| independent-same-raw-boundary-v1.json | 3498 | `236aaa5aea1b0e3631495fcc68cafae0964ec47244b59c9cddf9012688235e18` |
| independent-saved-observations-review-v1.json | 7480 | `8dbe8cd6983717fe994642de26f5d23ade4e45e863c64dcb88916878dc262954` |

F6. 作者の全最終返信8431 B / `613e436112caa85d1d1406388dcf8a198530e6d26f805abfcdf7a86280e3892e`、全function差分4481 B / `ca82b7eb5e637005eeef234518ffa0904f10727d554ed724187043280c8a7477`、全helper差分4593 B / `199144f405ea0a70b4df11369130da39dd37b9a4ff9a66dfa170edda252fc25f` とraw逆置換票2384 B / `6a2c7a6bd4ffa804d565aa8f851f0979f173decc4ee16a896cf811e07116a716` を読了した。作者最終delivery4321 B / `133ccfc2164092dd4bd08a0530470c8630c29faca77c49f3f7e3316002e2f4ce` の全15fileを実bytes/SHAへ独立照合した。二つの公開P metadata入力も17587/768cbfec…と267079/b36818b4…を保持する。

本便で変更したのは本返信と指定TEMP/task1073のみ。P/C私的数学本文は読まず、原1071/1072/実入力/source/WFは変更していない。許可された独自の小metadata fixture一回以外に、全受領器の実行・dot-source・Invoke-Expression・ScriptBlock変換、P/C/source/数学/Python/import/AST/compile/GAP/Git/GHA/network/credentials、新agentは実行していない。性能追加再走0。具体的な未解決の意味差はなく、残る全受領時間への寄与は未測定である。候補使用はroot最終読了・採否と実artifact登録後の別snapshotに委ね、1071を使用できる既存経路を止めない。

AUDIT_1073_VERDICT: LIMITED_SAME_COMPARISON_PASS_GUARD_CLOSED
