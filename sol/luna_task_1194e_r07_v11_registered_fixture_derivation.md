# Task1194e — 2312/F-v11-2 を1194d修理へ反映する追補

宛先: 既存Pauli/P・Helmholtz/C・Noether/public。1194dの同一修理を継続する追補であり、新agent・新宇宙・新承認待ちを設けない。rootが裁定2312全文を0bcf07、express全文を2a9c24で読了。研究者のGHA継続認可および2199/2312のnotify-and-go内で進む。

2312/F-v11-2は「selftest fixture の key 集合・schema 版は登録表から導出し literal 重複を禁止・配置前に『全 k128 canary が期待 gate に到達する』静的自己整合(dry canary)を driver selftest に含める」と定める。1194dの2 literalへ1 keyずつ追加する案は原因を特定した中間証拠として保存し、最終配備は登録表導出案にする。否定例の期待gateを手前の14-key gateへ変更しない。歴史的旧schema拒否の意図を維持する。

Pauli: current acceptance合成入力の基底key集合とcurrent schemaは既存登録表から導出する。old-acceptanceはcurrent形状からold schemaだけを変異させ、portableはcurrent形状へ必要な内容を上書きする。current fixtureの複数literalへの新key追加を恒久策にしない。他のcurrent k128 fixtureについても登録表からのschema/key導出と意図的なold schema変異を区別し、全30 caseの静的前提・到達gate・根拠source範囲を公開票として出す。公開票はsourceの実差分/通常gate順序にrootが結び、自己申告だけで到達済みと認定しない。通常reader/述語/順序/旧expected reason/原30 caseと元2 child/absolute300は維持。旧歴史入力をcurrentへ書換えない。原37+4+25=66保持域にk128_registration_canaryは含まれず、66保持はそのまま可能。同関数のregistry分類は変更域へ正しく更新する。

Noether: Pauliの公開descriptorと登録表から、全k128 canaryの意図する変異と先行gate前提を照合する小さいdry整合検査をdriver selftestへ含める。対象P/Cをimport・AST・compile・実行してはならない。通常readerや数学本走の代替判定器にはしない。既metadata21 case、その出力schema/数、1194cのlive/saved exact5理由修理を保持し、dry整合検査はこれらに先行する静的前提確認として必要な差分を明示する。全355関数不変の旧予定は必要変更域を除く保持へ訂正。配備前rootが小さい全差分と公開根拠を別読する。

Helmholtz: 同型欠品なしの1194d自担当監査を維持。Pの中間pin1129251/be63f17b…は配備に使用せず、改訂最終Pのroot source-only採用後に実opaque pinをC唯一RHSへ結合する。C独立本文/C4/原親/ケースは保持し、必要な公開metadataも実新D3へ結ぶ。

全員: 1194dの返信先とR/task1194d/{P,C,public}を継続使用し、TEMPは新version/fileで旧案を保存する。source→root source-only leaf→必要canonical/registry→carrier/dry公開契約→driver→WF→root closureの非循環順で、後着可能なところを並行作業する。C/metadataもP pin依存のため変わることは2312の『変わるなら明記』に従い通知へ記す。source-only採用とdry整合はruntime成功を意味しない。実行はrootが同じname/markerで新GHAを発射し、2段の修理差分と弱化なしをCV-9へ引継ぐ。caps・23親/8層・k128/max_batches1/no-refill・著者分離など1194d凍結条件は全て不変。
