# Task999 — 同語readout WF-only v3 の独立差分監査

## F0. 委嘱と保存境界

Task996の既読境界を同返信F10/F11へ保存した後、Task998/999を全文読了した。本票だけを変更し、旧991–993/987/984の票、P/C v2 source、旧WFを変更していない。ローカルPython/import/AST/数値/GAP、network/git/credentials、新agentは用いず、source/JSON/bytes/hashだけを読んだ。rootが唯一のrelease/GHA brokerである。

初期WF暫定全1597行、103,557 B / `1b1a4698be894228d853cd2055b6ab515dceab6148a39bcfb7bb0c064c5c36bd` を全文読了した。長い一回の出力切詰めは131–485行、881–931行を再読して補った。その後三つの必須修理をF5で閉じ、最終1674行版と作者返信の全差分・全内容を読了した。最終判定は **WF_DELTA_STATIC_PASS_RUNTIME_PENDING**。新runtime PASSは出していない。

## F1. 実v2診断と旧監査の見落とし

rootが回収した `%TEMP%/shadow-atelier-positive-readout-run33997745566-diagnostics-a1` のsmall JSONとP.logを全文読んだ。実run33997745566/1、head `c6278fe1365f447b6183600e446f36defef80e76`、artifact9978580135の実走では、16親入場とP四群/D三群はPASS、その後本Pは `ValueError:unique_sorted_files` で停止し、本Dは未開始である。P-stdoutは501 B / `a5c248537a4e4f80a9fe503fea57418534dc94a63cbf97f696a52be710ecfb2d`、記録elapsed_secondsは0.265004。速度比較や数学的成否には使わない。

実P自己試験2256 B / `34735ea19a3bbe8214eedf4f5e99b86245c08ef40d43991c73737f4155f91eb7`、D自己試験678 B / `7ca09522e6f3955fdde2281a7acb0fbb08d3e198f76f30702ad213587decc3be`、七群receipt1508 B / `615beda80c792a0e1dab1267c40e072072e96c4ea9c1ee4c597a8e2abf761ca0` を実bytes/hashと照合した。保存receipt893 B / `5268e4bf4ce62eb87e13089de5a2c1542c27b4554d97d554212f533f4426d620` は全16親/取得済みsource/raw/acceptance/driver不変true、word/D不足のINCOMPLETEである。元start観測782 B / `9f627644db1f043ae2a60d40c0f59c26c0705372f0fc28cbb9fa673dfd9e7401` の四countはint、replayはbool falseで、前便の型修理が通ったことと新順序失敗を分ける。

実acceptance.json 1,493,571 B / `2c619f2fc4cc37e36d60175a7c68947da35d57023cf6159a89d6aca42ce10b8f` の全16roleを、PowerShellのOrdinal文字列比較だけで調べた。相対文字列順との初不一致はoracleの58、task712の0、continuationの41の三roleだけで、rootの報告と一致した。oracleは `repair-source/check_...` より `repair-source-receipt.json`、task712は `r07-grade2-maps-v4/B_adj_a0.jsonl` より `r07-grade2-maps-v4-checker.json`、continuationは `accepted-completion/original/artifact-...` より `accepted-completion/original-cegar-run.json` が先になる。

私の旧993/987/984の静的監査も、WFのPath component順と、P/Cの完全相対POSIX文字列順を同一視する境界の誤りを見逃した。P v2 637–639行とD v2 1033–1038行は正しく完全sort/uniqueと実全inventory一致を要求しており、これらを緩める修理ではない。旧票は公刊時点の記録として不変とし、この見落としを本票で明示する。

## F2. 新scanと本番直結metadata canary

暫定WFの `scan` / `validate_inventory`（585–617行）は全file/dirを列挙し、相対名・symlink・regular file・全hashを保ったうえで、返すfilesをentry.file全体、directoriesを全文字列でsortする。validatorはexact fields、strict int size、裸64桁hash、sort/unique、file/dir衝突、実全descriptor/dir EOFを要求する。同じhelperが新入場、取得直後before、最終after、各出力一覧へ接続している。

新 `inventory_canary` はREPORTの専用fixtureで同prefix file/directory、'-'/'/'の逆転、複数階層、uppercase、空directoryを作り、実scanと既知全bytes/hash/dirを比較する。component順・directory逆順・重複・size/hash改変・bool size・余分key・非POSIX名・file/空directory欠落を同じvalidatorで拒否する設計である。これはGHA上の新metadata試験で、ローカル未実行。既存七群のv2実PASSと、新WFに結んで再実行する七群を混ぜない。

## F3. 全文監査で見つかった三つの必須修理

第一に、私の独立読取りで、修理後string-sortのinventoryを旧保存rosterへ直接list比較している1019–1020行を指摘した。実旧 `retained-parent-receipts/resume64/all-parent-files-before.json` は593,399 B / `e89fe5fcac1ceb4bbc871d613774ac46ea00535536a891232eaf69af202d448c` であり、ORACLE_ROOTの58、TASK712_ROOTの0、COMPLETION_ROOTの41が旧component順である。このままでは新入場が拒否される。旧JSONのexact hashとbefore==afterを維持し、型・重複・全descriptor/dir EOFを照合した比較用コピーだけを全文字列sortして新scanへ比較するadapterを作者/rootへ要求した。旧artifactや旧receiptの上書きは不要である。実old outputのpreservation/before-checkerは5145files/836dirsとも文字列順との不一致0であることもmetadataだけで確認した。

第二・第三にrootの独立全差分監査で、旧 `exact_pin` helper四行の意図しない脱落と、新metadata stepのprintfのbackslash二重化が発見された。前者はsource入場でNameErrorとなり、後者はexit-code.txtに文字通りのbackslash-nを残してfinishのstrip=='0'と矛盾する。元helperを復元し、printfを既存各stepと同じ一つのbackslashへ戻す必要がある。三点とも未公開WFだけの修理で、P/C sourceや数学gateの変更を求めない。作者が修理した最終差分を再読してから閉じる。

## F4. 不変の source・数学親・実走条件

新旧WFのARTIFACTS、COMPLETION_ENTRIES、ACCEPTED_COMPLETION_ARTIFACT、CONTINUATION_ENTRIESの全literalを文字列として比較し、全て同一だった。P_SOURCE/D_SOURCE/SOURCES/RAW/RHO2_FILES、Task554 primary/旧loop/source/runtime、LIMITSの区間も全text同一と確認した。v2失敗ZIPはrepair provenanceへ追加するだけで、第17数学親にはならない。実64/rank1450/gen8155/Separator/UNKNOWN_CAPという親と全64履歴、fresh rho2親は変更しない。

P v2は175,318 B / `cf6ac987acb2f399f36a8438cca78b773d7791286473b68362f2824a35d6451c`、LF2873、D v2は176,579 B / `865ed6a50b95303fdecafbc69e841da018858aa4624467fb17cdf80a0beadfd1`、LF2636、旧WF v2は92,986 B / `47043063db8e330210a29594cb8b91900a40c0750f651b2647c2101047bc8477`、LF1444へ実再hashで一致した。三本ともCR0/BOMなし/末尾LF。sourceの算術/reader/selftest/CLI変更は無い。

全13word files/同ordered ROOT/同normalized pair/11 typed slots/全80644座標/fresh original rho2/current targetのjoin、source lowerとphysical lowerの区別、全inputとwordのbefore-after不変、P一回/D一回、P5400秒/外100分・D10800秒/外190分・7168MiB/job330分を保持する。新metadata試験だけを別300秒枠で追加し、そのPASS/全拒否名/driver hash/exit/stdoutとreceiptの実bytes同一をfinishへ要求する。新試験に失敗すればcandidate uploadへ到達しない。

strict original-start countを観測してから判定する入口、取得済み各親の早いbaseline、sourceのadmission前baseline、alwaysでafter採取をbefore読取りから分離する前便の修理も保つ。失敗や未開始出力はINCOMPLETEとして保存し、未作成word/Dを成功へ置換しない。候補は全成功後のみ、診断はalways/hidden含有/30日保持。現gradeの同語比較をgrade2/A0/COMMON/cofinal/verifiedへ昇格させず、retained C9/C4の独立性を新規に証明したとも称さない。

## F5. 三修理の閉鎖と最終差分の静的判定

修理版WF 108,358 B / `04f06ac35b7cc98cbe5e78a011f28b5250a7fe69537332d21eb2c109a45b8604`、1674行を再hashし、追加helper585–766行、歴史入場1066–1114行、finish1415–1435行、新step1565–1577行を全文読了した。F3の三点は全て閉鎖した。

`inventory_fields` は順序に依存しない型・exact fields・重複・file/dir衝突の拒否だけを担い、`validate_inventory` は新規inventoryの全文字列sortと全実EOFを引き続き厳密要求する。`retained_inventory` だけが、既に旧fileのexact hashへ結ばれた歴史rosterの比較コピーをsortする。旧15roleのexact集合/unique、各entryのfile/bytes/sha256、全directoryを保ったまま、実scanとの全一致を要求する。旧before/after JSON全fileのpinsと元list同一条件も残る。順序差を理由に旧親のpayloadを省略したり、P/Cのreaderを緩めたりしない。

canaryには旧component順のコピーをadapterで受理する経路と、元canonical bytes不変、duplicate file/dir・size/hash・file/dir欠落・extra字段・wrong roleの八拒否が加わった。元十二拒否と合わせた二十件のexact順リスト、三つの実helper名、元copy不変、driver hash、elapsed上限、stdout/receipt全bytes同一、exit0をfinishで要求する。候補はこの新metadata試験にも従属する。ローカルでfixtureやP/Cの試験を実行した事実は無い。

旧 `exact_pin` は元本文とtext同一で復元され、新metadata stepのprintfは既存と同じbackslash一つである。全差分は静的file比較で読み、さらに10空白indentのtop-level def本文をtext境界で比較した。旧32関数の脱落は0、変更はscan/authenticate_continuation/finish/mainの四つだけ、新規はinventory_fields/validate_inventory/retained_inventory/inventory_canaryの四つである。mainの比較範囲には後続YAMLも含めて読み、新mode/新step/v3名とcandidate/diagnostic名を確認した。この比較はPythonやASTを実行したものではない。

以上から新WFへの追加必須修理は無い。**WF_DELTA_STATIC_PASS_RUNTIME_PENDING**。既観測のv2七群PASSを、新v3のmetadata二十拒否・再結合七群・本P/D・同語/11slot成功へ先取りしない。

## F6. 最終返信読了・凍結・射程

返信998の最終F1–F8全111行を全文読了した。実12,389 B / `b8334b7fe2fd0085365f753dd48043f68fb6df1ee63d3ab88f5fe759b0f3d196`、LF111/CR0/BOMなし/末尾LF。新WFも108,358 B / `04f06ac35b7cc98cbe5e78a011f28b5250a7fe69537332d21eb2c109a45b8604`、LF1674/CR0/BOMなし/末尾LFへ再hashで一致した。F4に掲げたP/D v2と旧WF v2のpinsも不変である。

作者の実15歴史roster全descriptor/dir照合、旧component順差の3/50/53件、同七群の既観測PASSと新metadata/runtime未観測の区別は、本監査の独立実metadata読取りおよびsource判定と矛盾しない。旧fileを修理したとの主張、P/D算術を変更したとの主張、新GHA成功を先取りする記述は無い。

本Task999を完成・凍結する。**必須修正は全三点閉鎖、追加必須修正なし。WF_DELTA_STATIC_PASS_RUNTIME_PENDING。** 今回の静的判定はdriverの一覧順序・旧歴史との比較・保存/成功gateの接続に限る。旧993/987/984の見落としはF1へ明記した。新run/commit/candidate、同語11slotの実比較、CV9、grade2/A0の新判定は未観測。公開とGHAはrootが担当し、私はTask996へ戻る。

AUDIT_999_VERDICT:
