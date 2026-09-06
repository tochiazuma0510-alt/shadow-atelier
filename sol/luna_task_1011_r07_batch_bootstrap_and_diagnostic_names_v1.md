# Task1011 — 初回 invocation 形成前の再開と二つの診断名

宛先: 既存994 P作者、995 C作者（1009 WF作者）、996/1010監査官。rootが公開997 F4/F10の未指定境界を確定する。算術本文・他系helperを共有せず、下記共通wireだけを適用する。変更は各人の未公開指定source/WF/返信だけ。995の作者完成票はまだ未公開なので、この根拠ある限定修理と最終pinの訂正を行う。公刊source/旧票は不変。ローカルPython/import/AST/数値・network/gitは禁止、GHAと公開はrootのみ。

## 1. invocation形成前に停止したrootのbootstrap再開

初回freshが通常invocations/<32hex>.jsonの形成前に停止しても、登録済みの未完rootは --resume で再受付できる。今回の実flagはresume=trueのまま保存し、過去のfreshへ改名しない。両before HEADが未形成なら両hashはnull、processed_candidates_before/accepted_new_rows_beforeはstrict普通整数0。nonce・時刻から最初/最後を推測しない。

全通常invocationについて、exact body/schema/seal/全file hash、portable binding、code/runtime/登録policy、実旧hostから再構成した全acceptance SHA、実launch、実保存before checkpoint/physical HEADとの結合を維持する。そのうえでfresh=falseではなく **resume=falseの通常receiptは高々1件**。通常receiptがある履歴は、resume=falseが1件ある場合、またはresume=true・両before HEAD null・strict count0のbootstrap通常receiptが1件以上ある場合を受理する。HEAD形成前の停止を繰り返せるのでbootstrapを1件だけに制限しない。pendingの残存は必須証拠にしない。通常receiptが0件の保存prefixは、従来どおりprogress HEAD/checkpoint/phaseが未形成の場合だけである。

未形成の新nonceを含む invocations/.<32hex>.json.pending-<32hex> は、997の登録atomic診断である。正確なnamespace/basenameと非symlink型を全rosterでも認証し、全bytesを保持するが、通常invocation数・開始receipt列・数学的進捗へ加算しない。部分JSONを通常receiptへ昇格しない。

初回GHA1009自体はfresh一回の登録のまま。このbootstrap契約を理由に自動再試行や追加invocationを本runへ足さない。

## 2. 二つの診断名と全結合

prefix=d972.r07.fixed-lambda-cycle-batch.v1、bodyは997 F155のexact bodyを維持する。通常rootの診断名を次の二本に固定する。

| filename | schema | status | terminal |
|---|---|---|---|
| resource-stop.json | prefix.resource-stop | UNKNOWN_RESOURCE | UNKNOWN_RESOURCE |
| rejected.json | prefix.rejected | FAIL | REJECTED |

両者が存在すれば両者を独立に全文照合する。名前とschema/status/terminalの相互入替えは拒否する。いずれもpartial=true/candidate=false/cross_checked=false/verified=false。exact fields、登録資源、finite非負elapsed、phase/reason文字列を確認する。

非nullのowner/source/start/selection_start/selection/invocation/実歴史progress HEAD/checkpoint/count/final/public HEADは、当該全保存実物と全hashへ結ぶ。非nullのinvocationは全通常receipt列の一件だけ。非nullのprogressは現在のcommitted HEAD以内の認証済み歴史checkpointだけとし、durable未commit先行分を既完了countへ使わない。早期nullは後で形成された値へ遡及置換しない。progress HEADがnullならcheckpointと5 count/rank字段もnull。public finalの非nullをprivate成果と偽装しない。

二診断は保存された停止履歴として保持し、ファイル名やnonce/時刻だけで最新停止を決めない。Cの完成result/terminalは従来どおり全finalから決める。未完成で診断が一件ならそのterminal、両方ならterminal=nullのままとし、Cのpartial=trueと実committed進捗は維持する。既存C-result bodyへ新字段を増やさない。

## 3. 公開前の閉鎖

両系が自系の通常helperを通す小さいmetadata逆対照を既存第三群へ追加する。0 fresh＋有効bootstrap、複数bootstrap、2 fresh拒否、bootstrapのbool count拒否、未形成nonceのatomic尾部と通常count分離、二診断の同時保持・名前/schema入替え・非null binding改竄拒否を確認する。新旧数学親の数値再走は不要。実行はGHAだけ。

994/995返信と996票へ限定差分・実pin・未実行を記帳する。Cの最終source公開pinはrootが1009へ再配達する。WFの初回fresh/全15親/64rank1450/k32/1/refill=false、全数学gate・全保全・全final成功条件は不変。rootと監査官の読了後にだけ初回batchを公開する。
