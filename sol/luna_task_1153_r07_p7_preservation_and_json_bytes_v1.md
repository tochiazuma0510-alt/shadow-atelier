# Task1153 — P7 の終了時 input-preservation と実 parse bytes 計器

発: Sol/root。役: 既存 P author Pauli。1151 を不変版として handback 後に続行する。
返信: `sol/luna_reply_1153_r07_p7_preservation_and_json_bytes_v1.md`。材料は `%TEMP%/shadow-atelier-audit163/task1153/` の CreateNew。

裁定2246の v7 必須計器②③④のうち P の②④を実装する。2244 の実 ordered_reductions 要素数/秒を実装した1151の最終草稿を基点にする。実CV9受理は1962/8667・限定7、formal5は未着。親19、k128/max1/no-refill、宇宙、caps、C4 retained、共有TCB、著者分離を変えない。新承認待ちを設けない。圧縮実装は本便の範囲外。

1. 既存 `finish_inputs()` が行う終了時の全親 inventory 再走査を実 caller 区間で測る。元の関数・チェック・例外・read-only/失敗/完了分岐と呼出回数を保持する。保護された raw body の外の呼出境界から括る。monotonic 開始/終了、実呼出 ordinal、完了か失敗か、実際に対象だった親集合/範囲を公開イベントとして記録する。成功のみの測定と partial/unavailable を混同せず、未実行を完了0へ補完しない。logging failure が数学の返値・元例外を置き換えない。
2. 保存4親で通常 parser が読む `output/candidates/<ordinal6>/reduction/reduction.json` と `physical-literal.json` の **実 raw バイト長**を、その読込みから計上する。同じ bytes を元 parser へ渡す。追加の open/read/parse/stat、ファイル宣言 bytes や rank からの推定で代用しない。通常 parse の重複を含む総件数/総bytesと、同一role/pathを一度だけ数える件数/bytesを明確に分け、文書種別ごとにも示す。中央directoryの合計は各文書一度の量であり、反復 parse 総量と同じではない。hashだけの再読は parse回数に含めない。実測対象区間、成功 parse と失敗途中の扱い、既存 native-metadata への包含を公開する。
3. 1151 exact25/旧 exact12・29本の wire/順序/意味は保持する。追加診断には独立した versioned schema/eventを用い、実event順序と partial branch を全列挙して driver作者へ渡せる公開票にする。追加の測定を既存 inclusive秒へ足さない。数学的 PASS gate は増やさない。

源は自己 P/自己1151 と root 公開規約のみ。C private source・差分・helper・fixtureは禁止。数学sourceの import/AST/compile/実行/selftest、GAP、Git/gh/network/credential、process操作、新agentは禁止。rootのみ後で実行/bindingする。1151完成票は上書きせず、全変更前後raw、全EOF往復、37 bodies/4 original loaders/25 old readers、旧6群設計、全 public consumer/raw位置の差分閉包、source bytes/fullSHA、normal guardsの所在を返す。全旧同一領域は既採択票に結合し、不要な同じ巨大表の複製を避けてよい。独立 root 別読と最終 in-run selftest 実績を作者の静的成立と区別する。

終了時: `AUDIT_1153_VERDICT:`。
