# Task993 — 同語 readout v2 型・保存境界の独立差分監査

## F0. 委嘱と現在の読了境界

Task991/992/993 を全文読了した。変更は本返信だけであり、旧 P982/C983/WF985 と返信984/987/988を変更しない。ローカル Python/import/AST/数値/GAP、network/git/credentials、実装変更、新 agent は使用していない。source と実 small JSON の読取り、bytes/SHA の照合だけを行った。**最終判定は SOURCE_WORKFLOW_DELTA_PASS_RUNTIME_PENDING**。新 P/C source と WF v2 の全差分、両作者の最終票、実30entry と最終 freeze hash を読了・照合し、追加必須修正なしとする。これは新実走の成功判定ではない。

Task988 は先に完成・凍結した（27,906 B / SHA256 `4f9ce529c21723cf8f07d3b18615bfd1daad3d3d37e25fd6d1a9b90cdae92aad`）。その固定 lambda 一括処理の条件付き数学判定と、本便の型・保存修理は別の対象である。

## F1. 既観測失敗と旧版の固定

原 run は `33995799635/1`、launch commit は `920780033b3aaa519a898e8b6b1d29fe67a04cd1`。diagnostic artifact `9978026066` は 244,085 B / SHA256 `e6565d625f42e9e3202a1faedc271ff07c5c6cfee9cc38558f879155312522b4`。root が ZIP 全体の bytes/hash と安全展開を照合した。こちらは実展開先 `%TEMP%/shadow-atelier-positive-readout-run33995799635-diagnostics-a1` の 64 files / 6 directories / 1,345,404 B を metadata で確認し、下記 small JSON を全文読了して個別 bytes/hash を測定した。ZIP 再展開や新数値 replay は行っていない。

診断内 `workflow.yml` は 84,418 B / `9e90bfeca6907fd71a4158308737a5a23677e3f2972b6e31391b5736b14bf36a` で凍結 WF985 に一致する。原 P v1 は 173,286 B / `f5b35c56869188d5e56480fb0615d85686eb4c1c982419b4e764f585a4a25473`、原 C v1 は 176,579 B / `a9e72980f3594842b5a7a4abaaf610b49a5d9202779ab1132c53c6bd4225ec98`。これらを新 v2 の全差分比較の基準にする。

`source-receipt.json` と `live-parent-intake.json` は source/runtime と全16 live parent / ZIP 入場の成功を記録している。これは本 P/D の数値実行や同語11slotの成功を意味しない。実 failure は accept 内で起き、P/D と両自測は未開始、candidate は無い。

## F2. Primary と secondary を分けた実診断

| 実保存 file | bytes | SHA256 | 読取り結果 |
|---|---:|---|---|
| `driver-accept-failure.json` | 787 | `227a9b5138ec92d41c6b1d7c891722f19c4307c3f7fb6a9ba8adbf47caee687a` | primary: `ValueError:positive_word_workflow:original-start-not-renamed` |
| `preservation-result.json` | 871 | `ec152f09f963f1118c30183399f697f63082389484ec80d6662bd029bf837b02` | `INCOMPLETE`、parent/source before 記帳と未開始 word/D の欠落 |
| `driver-always-failure.json` | 791 | `0279fab068ff99295f95c8f1cb3a3d6b853d9def5037865c303d125c6f552bce` | secondary: `ValueError:positive_word_workflow:always-preservation-incomplete` |
| `all-parent-files-after.json` | 234 | `59a3e3930478e177fec2731914bd8cef807df8c3c5a7e099b330564a20f14060` | `count=0`, `parents=[]` |
| `all-source-files-after.json` | 236 | `c94d5eebade8246cf5c14def0c452b49e746c7621b285298ed76759b75b53893` | `files=[]`, `acceptance=null` |
| `output-inventories.json` | 226 | `9b48653fe95f2ccfeb5c005c6cea4c2c4c0833636c4860895fdc7420bdf9b007` | `outputs={}` |

`parent_count=0` は親が未取得だったという事実ではない。全文読了した live-parent-intake は全16取得を記録しているが、always 側は保存された parent-paths/before を読む段階で止まったため、取得済み親の after roster を採取できなかった。原 primary を保存不足で置き換えてはならず、欠落を PASS としてもならない。

## F3. 実 count 型と旧監査の見落とし

実64親の `output/start.json` を直接読んで bytes/hash を再照合した。54,707 B / SHA256 `87bd9b89c593d68fba65b765bfe9f17bcc47d52cc9afce6f53f8c131a24f816b`、`rank=1386`, `generation=8091`, `completed_steps=0`, **`external_e_attached=1` は JSON 整数**（読取型 `System.Int32`）、`external_e_numerically_replayed=false` は JSON 真偽値（`System.Boolean`）である。開始 snapshot のこれらの値を、最終64段の rank1450/gen8155 へ書き換えるものでもない。

P v1 `read_selected_head` の835–837行と WF v1 `authenticate_continuation` の796行は、前者の count を `is True` と照合している。これは実 schema に不一致であり、今回の primary を説明する。**私の返信984/987の静的 PASS は、この実 count と bool の違いを見落とした。** 旧票を事後改変せず、本便で誤りを明記する。

新 production helper は `type(value) is int and value == 1` に限って通し、`true`, `1.0`, `"1"`, `0`, `2` は拒否する必要がある。Python の bool は int の派生型なので、`== 1` だけ、または `isinstance(value, int)` だけでは本契約を満たさない。実 `external_e_numerically_replayed is False` は別の真偽値字段として維持する。原 start bytes と P971/継続 C v2 は不変である。

## F4. 保存順序の静的根拠と修理の最小条件

旧 WF v1 `accept`（882–927行）を全文読了した。`paths=root_paths()` と全親 `inventories` は先に計算するが、`authenticate_continuation` を通過した後、908–913行で初めて acceptance / parent-paths / all-parent-files-before / all-source-files-before を保存する。したがって今回の796行での拒否では、既に RAM にある取得済み親と source の記帳が耐久保存されない。

旧 `always_preserve`（1061–1104行）も全文読了した。parents_check は保存 parent-paths と before を読むまで scan へ進まず、sources_check も before 読取り後に初めて現 source を採る。この順序が、primary 後の空 after receipts を説明する。

最小修理は、受領済み親の解決結果・読取可能な全 file/directory roster と source/raw の基準を、失敗し得る continuation admission より前に保存し、always では before/acceptance の欠落と独立に存在する after/部分 receipt を採取できる順序にすることである。複数親の途中失敗も、取得済みの部分を失わず、欠けた対象は明示して `INCOMPLETE` を保つ必要がある。元の primary failure receipt を保持する。

before/after が実際に揃わないものを「不変」と推測してはならない。旧 finish（1111行以降）の全16親/source/raw/acceptance/word/D 不変、両自測、P/D exit0、同語全比較の実 PASS を必要とする candidate 条件は弱めない。部分記帳の成功と数学 readout の成功は別である。

## F5. 初期段階の差分監査待ち範囲

初期段階では、新 P の strict count production helper / 六型 canary / source path 変更、C の producer/self path だけの移行、WF の新 identity/pins・早期保存・always 部分採取と全成功 gate、作者票と最終 bytes/SHA を待ちとした。これらは完成 block 保存後に全 v1→v2 差分を読み、F7–F11 で閉じた。他の bool/int 同種候補も F6/F9 の通り実 small JSON 型に照らして限定的に確認した。

全16親・実64・全30entry、runtime、保持 C9/C4、WORD_SCHEMA と C wire schema、全13 P output・同一 ROOT・11slot・full filtered 80,644・元 fresh rho2・資源上限は修理によって変更しない契約である。新算術、SLP/LEFT Fox/mod54/signed の変更は本修理の範囲にない。現時点で新 GHA / canary / 本 P/D / 新 CV9 / grade / A0 の結果を先取りしない。

## F6. 同種の型境界の追加確認

旧 P/WF の `is True` / `is False` と count/replay 字段を静的検索し、実64親の start/result/checker-result/run-receipt の該当 small JSON 型を読んだ。`external_e_attached` は start/result/checker で整数1、`old_scans_numerically_replayed` / `old_inserts_numerically_replayed` / `old_success_suites` は整数0、`external_e_numerically_replayed`・assurance flags・全比較/不変 flags は真偽値である。読んだ実入力に、今回の二つの `is True` と同じ追加拒否点は見つからなかった。これは一般的な全 schema 型の新保証ではなく、当該修理に必要な同種箇所の限定照合である。

旧 C v1 は `external_e_attached == 1` を使用し、今回の `is True` 拒否を共有していない。C 側は指示通り producer/self path だけを v2 に移し、P の型 helper や算術を共有しない方針が適切である。新 path-only source の実全文差分は保存後に別途照合する。

## F7. C v2 の全差分と凍結票

新 `search/check_d972_r07_continuation_same_word_eleven_slots_v2.py` を旧凍結 C と全 file 比較した。差分は実 source 1066/1067行、`AcceptedInputs.check_runtime_sources` 内の producer path と自身 path の二 literal を v1 から v2 にした箇所だけである。両 literal をメモリ内で元へ戻して UTF-8 bytes を照合すると、176,579 B / SHA256 `a9e72980f3594842b5a7a4abaaf610b49a5d9202779ab1132c53c6bd4225ec98` に一致した。Python/AST/import は行っていない。

新 C の実凍結値は **176,579 B / `865ed6a50b95303fdecafbc69e841da018858aa4624467fb17cdf80a0beadfd1`、LF2636 / CR0 / BOMなし / final LF**。1069–1071行の descriptor と実 file receipt による正確な両 path/全 bytes/hash 照合は維持される。WORD_SCHEMA・C wire schema・保持 C9/C4/raw4・全算術・同語11slot/full filtered/fresh rho2・全 canary・通常 resource/terminal の本文は不変。Task992 に必要な修理として追加必須指摘は無い。

返信992は最終凍結版まで全文読了した。**5,334 B / SHA256 `5af1f369c0df339342aec74c027880f84b537a34277ac54e356ed65d737c0691`**。初読5,195 B版から、output は未存在ディレクトリという表記と、本監査による二 literal 以外の一致の受領記録が加わった。二 path 以外の一致、旧三群の名前、未実行、P helper を C へ複製しない境界を正しく記録している。source に追加変更は無い。

## F8. 保存済み P v2 の型 helper と全差分

P v1→v2 の全 file 差分を読了した。変更は docstring の便名、両 consumer source path、新 `validate_original_start_header` と `read_selected_head` からの呼出し、新 `selftest_original_start_header` と四群 selftest 接続だけである。読了版は 175,318 B / SHA256 `cf6ac987acb2f399f36a8438cca78b773d7791286473b68362f2824a35d6451c`。これはこの段階の source 読了値で、作者の最終 freeze と WF pin は後に再照合する。

809–817行の helper は rank1386/generation8091/completed_steps0/external_e_attached1 の四字段へ各 `type(...) is int` と期待整数の一致を要求し、replay は `is False` に保つ。五字段とも F3 の実 original start 型に一致する。production 呼出しは846行で、全実 owner/source/start pins と sealed selected values を読んだ後に同 helper を通す。後続の64段・絶対 rank/gen・全 prefix/cardinality/HEAD/runtime gate は不変である。

2759–2778行の新群は JSON を往復した実五字段の metadata fixture で整数1の helper 呼出しを通し、attached の true/1.0/"1"/0/2 を同 helper に渡す。加えて rank/generation float、completed bool false、replay int0 の四拒否もある。既存 `selftest_rejection` は ValueError が出た時だけ該当名を追加し、拒否しなければ AssertionError となるので、単に期待名を列挙して PASS とする作りではない。新群名は `actual-start-header-count-type`、status/name/rejected_cases、元 start の exact bytes/hash と actual_parent_numerically_replayed=false を保持する。

通常 `--selftest` は原三群にこの一群を加え、全四群 status PASS と非空 rejected_cases を要求し、同じ production helper 名を receipt に記録する。通常 main からこの入口へつながる。原三群の本文、SLP/LEFT Fox/mod54/signed、Ref recipe、全13 output と同語 readout 算術に差分は無い。実自測の成功は GHA 待ちであり、metadata fixture を受理済み数値証明書としていない。返信991の保存済み F1–F4 も全文読了した。

## F9. WF v2 の完成差分と保存修理

新 WF v2 の全 v1→v2 file 差分を読了し、変更を含む sources/admit_live/header/accept/always の各関数を全文、後続 finish/main と実 YAML 起動・自測・P/D・always・upload tail も読了した。読了版は **92,986 B / SHA256 `47043063db8e330210a29594cb8b91900a40c0750f651b2647c2101047bc8477`、1444行**。元の大きな親定数・数値 consumer 本文は全差分比較で不変と確認した。本時点の完成 block に追加必須修正は無い。

新 WF name/path/marker と workflow 自身の SCHEMA を v2 にした一方、WORD_SCHEMA / C schema / LOOP_SCHEMA は v1 のまま。REPAIR_PROVENANCE は今回の失敗 run/head/診断 ZIP/旧 source と WF の値に一致し、失敗診断を成功親へ入れず、再実行や数学 wire 変更を主張しない。source receipt は新 P991/D992 の path/実 hash と保持 C9/C4 を別々に記録する。

source 取得・AST 審査後の640–647行で、9 files（新 P/D・C9/C4・raw4・新 WF）、driver と source receipt の early baseline を保存する。AST は将来 GHA 内の処理であり、こちらでは実行していない。admit_live の721–724行は各 role の取得直後に exact artifact/live intake と extraction 全 files/directories を保存するため、後続 role の取得失敗でも既に記帳した分を失わない。accept の927–929行は paths と全16親 before を continuation 型判定前に保存する。取得途中に未完となった extraction は always の診断対象になり得るが、before/成功 live が無ければ受理済み親の代用にはならない。

761–792行は実 start の exact pin と五字段の value/type を header gate より前に保存し、770–774行の strict helper を838行から呼ぶ。観測 receipt の `header_gate_applied=false` は判定前に書いた時点を表す。842–845行の九 count 字段も厳密 int へ強化した点を追加差分として読んだ。実保存 checker の8059/54433/2/96776/54/1/0/0/0は全て JSON 整数であり、真偽値 flags を同じループへ混ぜていない。

always（1104–1215行）は、各 extraction の after scan をその before 読取りより先に実行し、一件ごとの例外を記録して他件の採取を継続する。accepted parent roots も paths/before の不足と各 after scan を分ける。source/raw/WF/driver/acceptance の読取可能な after pin は final before/acceptance が欠けても保存する。word/D は存在する全 file/directory roster を採り、未作成を `INCOMPLETE_OR_NOT_CREATED` と記録する。`original_driver_failures` は元の primary receipt の hash を残し、最後に欠落が一件でもあれば `INCOMPLETE` として失敗する。actual before/after 比較の成功だけで各不変 flag を立てるため、before 欠落を保存成功に変える修理ではない。

## F10. 完全比較 gate、実 pin と未実走の境界

P 自測は原三群＋`actual-start-header-count-type` の exact四群、D は従来の exact三群である。WF は status/name の順序・群数を exact roster で照合し、P rejected_cases 非空、双方の exit0/assurance 条件を保持する。資源は P5400秒・外5970秒＋kill30秒/step100分、D10800秒・外11370秒＋kill30秒/step190分、memory7168 MiB、job330分のまま。新 header の数学と無関係な旧成功 suite 再走を追加していない。

新 WF の CONTINUATION_ENTRIES の JSON literal を読み、実64親の該当全30 files の bytes/hash に直接照合した結果、**30件一致・不一致0**。四 source の実 bytes/hash も SOURCES pin と一致した。全16 parent artifact tuple・実64/rank1450/gen8155/Separator/UNKNOWN_CAP・元32 completion の歴史的入場・同 owner/source/start/fixed・Python全文/NumPy・raw4・元 rho2 の pins は旧 WF と差分が無い。新 header 入場のために原 start を変更していない。

finish の条件は、全16親/source/raw/acceptance/driver と D 前後の P output の不変、P/D一回ずつ exit0、両自測の実 PASS、全13 P files・全 ordered node/Ref EOF・同じ ROOT と normalized pair・11 endpoint/typed slot・全三 printed direct/prefix・full filtered80644・元 fresh rho2 の直接読出しを維持する。物理 lower32260 と top48384 を区別し、PB4 Fox零/full P零を主張しない。非零 current target の場合は positive readout が NOT_APPLICABLE のままでも、全 readout 比較は省略しない。成功 candidate はこれらの実 gate 成功時のみ、diagnostics は常時・hidden含有・30日保存である。

今回の差分は数学・一般 LEFT Fox/Act・SLP/Ref・mod54/signed/full filtered の新算法ではない。保持 C9/C4 と既存 TCB の独立性を新たに立証するものでもない。受理済み1450と原64段の照合結果を、新 P/D の実走結果へ流用しない。GHA 内 AST/四群・三群/本P-D、工房 CV9、grade2/全A0 の新結果は未観測である。

## F11. 最終作者票・freeze と判定

作者の freeze 宣言後、返信991の F1–F9 全114行を全文読了した。P の差分、actual count と原 start/最終 HEAD の区別、新四群、WF の保存と受理の別、未実走を正確に記録する。返信992も最終39行版を全文読了済みである。最終ファイルを独立に再 hash した結果は次の通り。

| 最終 file | bytes | SHA256 | LF |
|---|---:|---|---:|
| `search/d972_r07_continuation_positive_word_readout_v2.py` | 175318 | `cf6ac987acb2f399f36a8438cca78b773d7791286473b68362f2824a35d6451c` | 2873 |
| `search/check_d972_r07_continuation_same_word_eleven_slots_v2.py` | 176579 | `865ed6a50b95303fdecafbc69e841da018858aa4624467fb17cdf80a0beadfd1` | 2636 |
| `.github/workflows/d972-r07-continuation-positive-word-readout-v2.yml` | 92986 | `47043063db8e330210a29594cb8b91900a40c0750f651b2647c2101047bc8477` | 1444 |
| `sol/luna_reply_991_r07_positive_readout_count_repair_v2.md` | 15212 | `896b29a97912ed3ca31ea910319adf900de2ca14e1f8038d8658d390ab426930` | 114 |
| `sol/luna_reply_992_r07_same_word_checker_path_v2.md` | 5334 | `5af1f369c0df339342aec74c027880f84b537a34277ac54e356ed65d737c0691` | 39 |

全五 file は CR0 / BOMなし / final LF、両作者票の末行 marker は指定通り。source/WF は既読版から不変で、WF の P/C pins と実 bytes/hash が一致する。旧 P v1 173286/f5b35c56…、旧 C v1 176579/a9e72980…、旧 WF v1 84418/9e90bfec… も再 hash して不変を確認した。

**SOURCE_WORKFLOW_DELTA_PASS_RUNTIME_PENDING。** 原型拒否の二点を実 schema へ修理し、同 production helper の反例接続、C path-only、保存順序と欠落の明示、全数値・同語・保存 gate の維持を静的に確認した。追加必須 source/workflow 修正は無い。984/987での私の count/bool 見落としは F3 に残し、旧票は改変しない。本票はここで凍結し、新 GHA の AST/自測/全 P-D/保存・工房 CV9 の実結果は root の後続記録へ委ねる。新 grade 判定・全 A0・verified を主張しない。

AUDIT_993_VERDICT:
