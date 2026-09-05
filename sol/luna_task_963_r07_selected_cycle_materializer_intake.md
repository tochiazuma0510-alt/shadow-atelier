# Task963 — v548非零witnessを実physical rowへ結ぶ最小consumer調査

役: Luna / read-only実装設計。Task959のparent-pin待ちの間に実施する。
変更可は `sol/luna_reply_963_r07_selected_cycle_materializer_intake.md` のみ。
ローカル数値/Python import/AST/GAP/network/git/credential/dispatch/追加agent禁止。
source/JSON/byte/hashを読み、数値や将来terminalを予測せず具体的ABIを報告する。

Task957の正式EとTask958 positive intake、v547/v548、Task959公開witness/geometry
ABIが前提。完全oracleは未走行で非零とは未確定だが、非零なら後続のEが必要。
producer sourceは完成・completion成功artifact pin待ち。この待ち時間で、Eを
最小のGHA consumerへ切り出す具体的接続を確定する。新実装はまだ書かない。

1. oracleのauxまたは六cycle witnessから一つのordered raw word SLPを構成し、
   tau零、普通整数指数、omegaをbottom-upで求める。v547のexact normalizerを
   chord branchに適用し、aux branchのc_x/c_yを勝手に厳密指数零へ修正しない。
   actual Q0/Q2 endpoint/carry/omegaとsame-word sourceの確認APIを列記する。
2. closed-word source評価をSLP DAGへ拡張する最小演算を示す。新group actionの
   左右とmixed degreesを明示。短いraw wordのflattenを用いるなら実語長の上界を
   保存geometry/word metadataから安全に導く方法を示す。非可換なP1語全体は
   flatten/係数集約しない。source評価とliteral祖先の型を分ける。
3. primal section消去はold元embedded lead昇順→new各owner元lead昇順。
   全8059係数とfull96776 lower zero、全4×36288 topからのcanonical subtractionを
   同じ受理P1 basisで構成する。元normalized rowにscaleを重ねない。
4. physical rowは**四characterのBを全て足す**。単一char materializer wrapperを
   そのまま呼ばない。oracle scalarとactual lambda·G、current全pivotに対する
   rank上昇、target更新、fresh separator/両target dot/全rows sweepへ接続する。
   保存row/target/literalの次consumerへのABIは、現26段prefixを前提として薄く
   追加一行を読む最小形式を提案する。旧scan/insert全算術の再走を要求しない。
5. 下流のgrade2 MEMBER時にはTask958の同一語normalized pair/11-slot readoutが
   別途必要。Eで新pivotができただけではfull A0やMEMBERを宣言しない。

必要な既存関数は正確なsource path/関数名/引数/返値と保持前提まで読む。
不足する最小新関数と、producer/checkerで共有せず別計算にする実raw-source部分を
特定する。未実測のend-to-end秒数やrank収束回数は書かない。
原rho2のDERIVEDと保存target実dotを区別、verified=false。
最終行 `AUDIT_963_VERDICT:`。
