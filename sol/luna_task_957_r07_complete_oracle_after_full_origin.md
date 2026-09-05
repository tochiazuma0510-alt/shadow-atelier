# Task957 — full-origin走行中の完全source oracle接続設計

役: Luna / 限定read-only設計。rootのTask163/WO-162-1を継承する。
変更を許すのは `sol/luna_reply_957_r07_complete_oracle_after_full_origin.md` のみ。
Python/GAP等の数値実行・import/AST実行、network、credential、git、dispatch、
追加agentは禁止。source/JSON/byte/hashの読取と指定返信だけを行う。

## 前提と範囲

Task954/955/956は最終source静的PASS、run33967668257/1で現在実行中。
source commit fd04734d20d472e7c09f31de3f92f8a50d6d841a。
新runtime結果はまだ与えていない。成功やroot零、rank増加を予測しない。
受理済み親はrank1359/gen8064、fixed44 run33964709359/1、工房裁定2125の
限定付きcross-checked。current scalar44件と構造零132件、target係数[1,1,0]。

新full-origin consumerは各lambdaで全4×32280 originsを調べるが、
ROOT_ORIGINS_ZEROはgrade2 NONMEMBERでない。次の完全oracleの接続を
実装可能な型まで詰める。reply953の一般論を繰り返さず、**v548のjoint kappa
とsource cochainの具体的array/edge ABI**に限定して既存sourceとの継目を決める。
rootは同時に実走の観測、artifact結果と次のcampaign判断を行う。

## 読む正本

- reply953全文とTasks954/955の公開ABI、v548/v543/v546/v547。
- 両系v15のSourceContext/group enumeration/affine Fox/qnorm/character transport。
- 実Task554のold/new lower row、P1 index/cacheの形式と元leadの意味。
- v459とv547の五carry・literal正規化・固定relator/word辞書の根拠。
- 新full-origin実装から必要なのは現lambda/8059行/parentと新prefixの読取契約。
  既走sourceを変更しない。原rho2直接読取の新義務を追加しない。

## 必須成果

1. Q2頂点の明示的index、全2正generator edge、tag置換のvertex mapの配列型を
   固定する。section-left/kernel-rightとrotation-leftの変換を式とsource行で結ぶ。
   actual input parityが左actorのkernel shiftを決める規約を保つ。
2. kappa補間の二段階を既存保存rowに接続する。新d1 6045行→旧d0/共有aux2014行、
   各段のrow/lead/index/target-value型、逆代入方向、全8059等式を列記。
   old leadは元width6056の座標であり、full lowerのfirst_nonzeroへ置換しない。
3. `f = sum_a q_a Psi2[a] - kappa Psi1` のraw source edgeへのpullbackを、
   六tagの実Fox substitution、右qnorm、degree0/1/2、Fourier重みで具体式にする。
   既存関数のどれを呼び、どれを新たに書くか、返るarrayのshapeを定める。
   shared aux6/7は独立eta入力であり、edge augmentationを18で割らない。
4. tree/carry、全54433 chord equalityと二auxの完全零判定を新consumerへ接続する。
   非零なら最初のfailed chordから高々6cycleの合法sourceを作る固定順と、
   v547 SLP→full P1 reduction→full lower-zero/Bまでの新しいconsumer境界を示す。
5. 新oracleに必要な追加入力の正確な既存path/pinまたは未作成の機能を列挙する。
   欠品を推測せず、既存にないexportを既存機能と呼ばない。二系統独立実装の
   小さな差分に分けられる単位を挙げる。実行時間の予想や旧504の再利用はしない。

主張は設計のみ。数値gate、新しいNONMEMBER/MEMBER/fullword、cross-checked、
verifiedを宣言しない。最後を `AUDIT_957_VERDICT:` で終える。
