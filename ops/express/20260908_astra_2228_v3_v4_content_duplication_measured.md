宛先: 司令塔 / Opus。裁定2228の冷保存設計用に、rootが v3/v4 の全 ordinary ZIP entry 目録を SHA256＋bytes で集計した。数学本文の実行0。これは次 v6 の18親/k128/capsを変更しない。

v3 run34023589045/1 は11437 file・1267599138 B、v4 run34120585268/1 は11648 file・1308094050 B。両目録の全23085件を、case-sensitive path・普通整数bytes・完全SHA256へ結合した。入力目録は v3=2101151/520aefab2ce1dafef319b1b07e765a41927639d4d321dd2de5ee5246bb16d42a、v4=2141758/c2ec141eecbc435972d750ae7beb31382c6108ad93ccb698181b311d77390fb3。元全ZIP/entry EOF受領の既存pinに結び、今回の全payload再hashとは称さない。

v4全件の排他的内訳は、同path同content **933件/45373127 B**、別pathでv3中に同content **10件/501997 B**、v3に同contentなし **10705件/1262218926 B**。output/ に限ると同content399件/10117076 Bに対し、新content6188件/1205023375 B。ファイル全体のbyte一致から、旧親出力が新artifactへ全量累積しているという仮説は採らない。

両artifact内の重複も除いた共通contentは261 blob/16472393 B。両方の論理合計2575693188 Bに対し一意blob保存量2463644182 B、差112049006 B。この差には各artifact内重複の削減も含む。単純な内容アドレス保存だけの効果はこの登録宇宙では限定的で、冷保存の主案である『毎run再導出する命題と過去採用済み命題のpin引用の区分』を置き換えない。圧縮ZIP転送量・実walltime短縮をこの差から断定しない。ZIP内部をさらに展開したchunk重複は今回の宇宙外。

全件対応票 `%TEMP%/shadow-atelier-audit163/root-v3-v4-all-entry-content-duplication-rows-v1.json` **11687467/702c6b9a4375800e79490b4003307b2fc1c7b6a0e703e284b97e6e45a1eeb417**。集計/4分類/入力pin/射程票 `root-v3-v4-all-entry-content-duplication-summary-v1.json` **12933/67839f0e0ec01af0ab92c586769f2dd71adce1d02e6c6f58fbc40273a9b491ec**。再現は保存した全件票の class/category ごとの件数・bytes加算、および全2目録の (sha256,bytes) 一意集合で可能。

完全typed受領の空dir再欠損は原因主体UNKNOWNのまま。Task1112=5189/b60e5a7cef8bc4bf621f2ff5948b12b4b6abbfa6822625ff41940133bffa850dで、全歴史照合を保持した namespace保持と失敗journalを自作TEMPのみで小対照中。親適用・再launchはroot独立静読後。P計器の12-key/26完了順は静的採択済み、C第五群は公開目的との差2件をrootが発見し作者が修理中。研究者のGHA継続認可を保持し、未受領の正式inventory5を捏造しない。
