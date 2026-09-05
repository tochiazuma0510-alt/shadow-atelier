# Task970 — v548完全oracle＋Eの継続器 intake（設計のみ）

役: Luna 実装接続の読取/設計。Task965の最終freeze後に開始する。
変更可は `sol/luna_reply_970_r07_complete_oracle_cegar_continuation_intake.md` のみ。
公刊前後を問わず965のsource/replyを変更しない。ローカル数値/Python/import/AST/GAP、
network/git/credential/dispatch、追加agent、実装・workflow新設は禁止。
rootはTask966/967の監査とE実走を継続する。本便はそのrelease条件ではない。

目的: 一つのEの後に、新しいcurrent stateで完全oracleを再評価する実装接続を具体化し、
継承WO-162-1の自走CEGARを一回ごとの手作業のpin入替なしに継続できる設計を出す。
Task957/963/964の数学を繰り返してページを増やさず、既存関数の実signatureと
動的state/receiptの必要差分に絞る。新sourceの宇宙は追加しない。

登録宇宙は同じD=ker(five carry)＋二eta、Q2全54432 vertices/108864 edges、六tag、
四character、全8059 P1/96776 lower、四B/48384 physical、retained Conn前提。
原点は成功oracle completion33977701313/1のrank1385/gen8090。E runの結果は未観測。
成功する場合のrank1386を現在値として先取りせず、実Eの新deltaを薄く取り込む契約を
場合分けで書く。Eがtarget-zeroならTask958へ分岐し、余分なoracle実行を要求しない。

読取正本: 新965 sourceとreply、959 producer/960・968 checker、957/958/963/964、
既存full-origin v1のcap/resumeとcheckpoint schema。公刊sourceは読取のみ。

提出内容（この順で短く、根拠関数/行を付す）:

1. 既存関数の接続表。受理済みrank1385 prefix＋E一行deltaのloadからcurrent physical
   rows/records/target/lambdaへ入る薄いadapterを具体化する。owner/source/startの
   原producer・completion・Eの由来、canonical P1 Refと新physical Refのnamespaceを分離。
   historical 26 scans/insertsや旧成功suiteを再走する案にはしない。
2. 何をrun中に一度認証/構築して保持でき、何が各lambdaで変わるかを列挙する。
   geometry/tag/BFS/carryとP1/index/lower readers/四Bは固定、q/chi/kappa/cochain/tree residual
   とwitnessはcurrent lambdaに依存する。初期化関数の中に固定値/副作用/全body再読込が
   隠れている箇所を実sourceで示す。source dualの元lead降順とE primalの元lead昇順を維持。
   本便でGammaを実装したり、未計測キャッシュの速さを仮定しない。
3. 一つのstepの状態遷移と保存物を具体化する。current lambdaで全oracle EOF、非零なら
   同じwitnessのraw/P1/fourB/E、一度normalizeしてrank/gen+1、target/freshlambda/allrow。
   complete-zeroならv548/Conn前提付きseparator候補、target-zeroならlinear候補とTask958。
   zero/nonzero/missing/UNKNOWN_RESOURCEを分ける。同じlambdaに旧witnessを使い回さない。
4. cap/resumeに必要な最小ABI。fixed source/geometry owner、start、各stepのoracle/E output、
   instruction/predecessor/HEAD、exact EOF、last-complete cursor、checkpoint不変項と
   全未完phaseを指定する。新capの値・反復数・速度・終了予測は書かない。
   resumeが既済みstepを再計算せず独立checkerが全new stepsを照合できる切れ目を示す。
5. 独立checkerが保持できるTCBと新たに全数照合すべき算術/配列/型を分ける。
   producerのhelperを新checkerが使う案は禁止。普通27source/別primal/全四Bと同じ
   raw word/typed ancestry、全8059/54433/2を残す。positive全11-slot gateは未実装と明示。
6. Task964の固定complete packet案との選択に次のE実測から何を使えるかだけを付記する。
   一個のscalar/alpha support/実時間から残iteration数やsource sparsityを予測しない。
   追加profileが必要なら、計測対象と保持する等式を具体化して指示案に止める。

未来のsource/run/artifact SHAは未観測のままにする。独立実装の新設は次の別委嘱。
設計上のblockerがあれば具体的に報告し、ない場合は最小adapter/実装範囲まで固める。
最終行 `AUDIT_970_VERDICT:`。新rank/grade2 MEMBER/NONMEMBER/fullA0/verifiedの主張なし。
