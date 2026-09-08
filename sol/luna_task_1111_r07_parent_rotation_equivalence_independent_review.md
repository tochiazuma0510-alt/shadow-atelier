# Task1111 — v7以降の統合親・回転案の同値性に対する独立数学監査
宛先: packet_bounds_audit。**Task1108の完成・全材料freezeとrootへの納品を先に行う。その後にrootの開始連絡で本便を読む。1108の実装を本案へ変更しない。** 本便はSol/rootが書いた数学・契約案の独立監査であり、新P/C/driver実装ではない。返信は sol/luna_reply_1111_r07_parent_rotation_equivalence_independent_review.md、末行 AUDIT_1111_VERDICT:。必要な未実行監査材料は %TEMP%/shadow-atelier-audit163/task1111/ に新規保存する。新agent、Git/GHA/network/credential、source/数学/AST/import/compile/自己試験の実行、既processへの操作は禁止。相手P/Cの私的本文は読まない。

## 依頼の根拠と変更しない現在便
2224正本 docs/notes/fixed_lambda_batch_v5_cv9_reading_v1.md =64510/11b5a48cf34bcc9f4e6bdafb1d78513bcd40d30236bfdb5476b52d6443f904ea の §7・末尾裁定、2224速達5183/97acf6b1…、2225速達1354/0c49e0966c452473a3efcd3ec620e4108fc869c8d236ba248839d48ac2ac5c99 と snapshot2809/543072d0632a2f4e3d8d155ca24c534ee54a8d62ccafb8c046c39830a837a93e、reply163 F8.169を読んでから監査する。2225原commitは5c356f45a9e4a75b7adc1daaad7399b8d9cad8a1。

現在のv6は既承認の18親/9-key/k128/同caps一runである。本案はその親・宇宙・caps・marker・workflowを変えず、v7以降の別namespace/別公開wire/具体親集合の事前登録へ向けた提案に限る。正式状態はrun34161493396/1/heada5b456a973f8a917f3af386d327061a02a0cf900、rank1834/gen8539、cross-checked限定7条、A0 actual0/1・階段1/6・grade2両NOT_DECIDED・verified=false。次のv6採用数は未計算であり、全128採用も次の親rank1962も事実として置かない。

## 原案R1 — 統合とは証明書の順序付き再配置である
既登録のphysical quotientのF3空間をEとする。original64/continuationの受理済み状態を基点Bとし、その全1450行を(b_0,...,b_1449)、基点のtarget remainderをt_B、保持するtarget祖先列をD_Bと書く。D_Bの長さは97（先頭32の元5-key、後続65の元6-key）である。基点のraw・固定16payload・全source来歴・認証範囲は変更しない。

その後の採用行を履歴順にq_0,...,q_(A-1)とする。候補順c_jと採用順jを区別し、dependentやSKIPPED_AFTER_LINEARはqを増やさない。各採用行の元literal/source/normalization/reduction/witnessを、その行が作られた **origin artifact全pin + native schema + 元相対path** の文脈に束縛しておく。単に「batch-row/local0」だけをグローバル識別子にしない。新旧runの同名role/local0もこの文脈で区別する。

統合親Sは、論理上の行列 (b_0,...,b_1449,q_0,...,q_(A-1))、D_Bに各採用行の元target ten-key記録を順に連結したD_S、最新target t_S、最新generation/state/terminalと、全origin資料を解決できる表現を持つ。行を別の基底へ取り替えず、行順/lead/係数/零/出自を保持する。単に同じspanであることでは足りない。A=384の現在例ではR=1834、D長=481、base generation8155から8539である。v6後を考えるときはA=384+aとし、aはその実際の受理済み採用数だけから得る。

物理的には新bundle内のrow-logへq列を連続配置してよい。ただし全q_jについて、元physical-normalized.binの全12096 bytesと新row sliceの全bytesが一致し、global index1450+j・origin文脈・元candidate ordinal・採用j・元sha・正確なoffset/lengthを相互に結ぶ。複数同一payloadの内容アドレスによる共有は、元namespace/path/明示空dir/全inventoryの写像を保持してからに限る。型を変えたpayloadや、同値なだけで別bytesのJSONへの置換はこのR1に含めない。

## 原案R2 — 認証対象を保持するための十分条件と紙上の論証
次の条件を別作者Cが実際の原入力と統合出力から照合した場合だけR1を受理候補とする。

(i) **行identity**: 全1450+A行の順序付きbytes、native packed3型/長さ/正規化、全logical-to-origin-to-slice対応が一致する。重複global index/欠け/alias/途中EOF/不正tritは禁止。基点固定資料も元全pinのまま保持する。
(ii) **元の導出の意味**: 元D_Bと各q_jのliteral/source witnessはnative文脈を含む完全な参照閉包を持つ。再配置後の参照解決が元解決と同じraw bytes・同じsource word・同じρ2・同じphysical mapへ到達することを、ただのhash一覧ではなくtyped解決の同値性として示す。元の証明書が持つ限定は継承し、未監査の旧算術を新たに監査済みとはしない。
(iii) **target履歴**: 公刊signは t_before - theta*q_j = t_after である。各採用行のtheta（0も含む）と元前後target/state/命令を順序付きに保ち、全原target辞書と前後pinを一致させる。特に元97を10-keyへcastしない、theta0を消さない、candidate ordinalとaccepted localを等しいと仮定しない。
(iv) **状態とterminal**: latest R=1450+A、generation8155+A、D長97+A、current/previous target、最新state/terminal/λの役割を元完成状態と一致させる。currentやpreviousの意味を便名から推定せず、実start/finalへ束縛する。未完成prefix/durable_tailは本案の完成統合親にしない。
(v) **全閉包と保全**: 必須の旧元bytes・明示空dir・runtime/source/fixture/receipt・来歴の全参照を解決し、元ordinary file/dir inventoryに対する全射で欠けがなく、同じlogical pathへの二重割当もない。unobserved/nullと0を区別する。証明書closureの一部を単に前runのsealだけへ置き換えない。

(i)により順序付き線形消去で参照する行は一対一に同じものとなり、既lead順と行のspanの両方が保たれる。(ii)の参照グラフ同型と各葉のidentityを前件とすると、DAG上の構造帰納法により各literal導出が表す語・ρ2・physical rowの意味も変わらない。(iii)の各式を履歴順に連鎖すると
 t_B = t_S + sum_(j=0)^(A-1) theta_j*q_j
であり、元基点identityと合成した認証対象が保持される。この式の総和だけを確認して個々の祖先identityを捨ててはならない。λが存在するnonzero終端では、(i)と同じλ bytesにより全R行へのpairingとtargetの値は不変である。ただし次便の新λは別に全R行へdirect pairingする。positive終端はt_S=0と元祖先を保持するだけであり、same-word adapter/positive readoutが未了ならMEMBERへ昇格しない。これらは **十分条件付きの紙上論証** であり、まだ実bundleが条件を満たしたという主張ではない。

独立監査では(i)–(v)から本当に意味保存が従うか、DAG同型の前件が循環・native環境・署名付き語・target基点・cross-checked限定を抜かしていないかを特に攻撃する。元の語/ρ2の認証範囲がDERIVEDに留まる部分を、構造帰納法で独立実算へ昇格させることはできない。

## 原案R3 — 一つの統合親で持ち回る具体的な形
基点の既15 roleは当面変更しない。その後のv3/v4/v5/...各batch専用roleを将来の新wireでは一つの **consolidated-batch-parent** へまとめる案とする（名称/実装ABIは提案、現在便の確定名ではない）。基点15＋統合親1の通常入場を提案し、最初の変換便だけは実際の旧全親集合を入力とする。初回変換がどの受理済みheadから始まるかは、実際のv6結果が出た後に別に固定する。v6成功/128採用を今から仮定しない。

初回変換器Pと独立Cは旧native各層を元文脈で読み、R2全条件を全原入力へ接続する。後続便では現在統合親と新packetの全証拠を連結した新統合親を出力する。新Cは自分のreader/row index/closure resolverで新全bundleと旧受理済み入力・新実行を照合する。**新統合親が過去の統合親を再帰loadしないと全意味を解決できない状態はR3の失敗** である。過去aggregateのpinは来歴として残してよいが、必須payloadを外に残してこの条件を満たしたことにはしない。

統合coreのmanifestは自身の全SHAを自己参照せず、payload/index/元資料の閉じた内容をsealする。C結果とGHA外側run/artifact/whole inventoryの束縛はcoreの後に形成し、自己hash循環を作らない。元原資料のnative sealは変更せず、新wrapperがnative context→bundle pathの解決を担当する。source/workflow/new public exact-key/schema/全consumer/拒否群と正式親pinは別途凍結・独立別読・司令塔への具体通知/必要な親変更裁定を経る。本数学案をその実装/配置承認とみなさない。

## 原案R4 — 実際に省く仕事と残る仕事
狙いは古いv3→v4→v5→...の再帰adapterを便ごとに重ねて起動し、同じ祖先への型解釈・bytehash・native direct pairingを重複することを減らす点にある。統合readerは全原文脈を一度ずつ認証する一本の走査とし、全n層のprefixを何度も再走査しない。原資料の参照解決が本当に一度になったことを、計測用のunique bytes/files/rows/contexts と total visit の別カウンタで公開する。

残る仕事は全origin closureの必要metadata/bytesの読取と保全、全R行の真正性、最新λでの全R行と二targetへのdirect pairing、全新k候補のraw/source/P1/B/reduction、全新target/literal導出、統合出力のEOF・index/closure照合である。R・祖先長L・origin metadata量M・新選択数k・型ごとの処理量に依存し、親role数が一定でも一定時間にはならない。core pack作成/重複排除/インデックス照合にも費用がある。保持する原証拠の全量が単調増加すれば、一回走査のI/Oも増える。

過去whole envelope/fixture/runtime/rawを全closureから外して「冷たい場所のpinだけ」にする案は、本R1–R4の同じ保全条件を満たさない **別のスコープ変更** として分ける。必要な旧証拠を一部読まない方式を、無条件に同等で速い案とはしない。R3で全意味を自己完結させてもR4の削減量が実測で小さい可能性は残す。

同n再測定P residual271.411740 vs277.828094 sや回帰モデルの係数は候補見積もりであり、因果識別・constant-time証明・acceptance gateではない。親層の数は実際の契約/到達readerから判定する。k425/約110 runのA0完了は保証しない。**k引上げはR1–R4の採択/実装/計測後に別の具体preregistration** とし、初回統合のk/capsをここで勝手に変えない。

## 求める納品
F1: R2十分条件に対する敵対的判定。成立するなら条件付き命題を明示し、不足なら反例を具体化する。特に「spanだけ同一」「元local0衝突」「元97を10-key化」「theta0を削る」「target sign反転」「最新λを再利用して新λ照合を省く」「sealed prefixだけで参照閉包を切る」「hidden history import」「positiveをMEMBERへ変える」を個別に裁定する。
F2: 必要なtyped解決環境と全証拠closureの具体境界。rho2/literalの意味保存と、その数値を新たに独立再生したことを区別する。
F3: 現15基点＋1統合親の提案が親層を定数にした意味、残るR/L/M依存と実際に消える重複仕事、費用を識別する公開計測項目。利益が未証明なら未証明とする。
F4: 具体実装委嘱の前に必要な公開schema/参照表/positive・negative/adversarial fixtures/全consumer表。旧private helperは共有せず、P/C著者分離の実現方法を示す。
F5: R1–R4の採択可否・必要修正・未決定の実親/元17or18集合/pins。新GHA/数学実行0、v6変更0、verified=falseを記載する。

本便作成時点で実統合bundle/初回変換器/C/公開ABI/新runは存在せず、rootも数学の同値性を実測済みとは扱っていない。

