# Task959 — v548 single-snapshot complete scalar oracle producer

役: Luna / 実装。先行Task958を完了してから本taskへ進む。
変更可は `search/d972_r07_section_cochain_oracle_v1.py` と
`sol/luna_reply_959_r07_section_cochain_oracle.md` のみ。
数値/Python import/AST/GAPはGHAのみ。ローカルはsource/JSON/byte/hashと指定編集。
network、credential、git、dispatch、追加agentは禁止。rootが単一broker。

## 登録宇宙と前提

Task954 full-origin run33967668257/1、source commit
fd04734d20d472e7c09f31de3f92f8a50d6d841aが走行中。
新parentのexact artifact/entry pinは完了後にrootが送る。予測値でfreezeしない。
単一の新しい現Separatorに対する**完全スカラーoracle**を実装する。
ROOT_ORIGINS_ZEROを入力条件にしない。v548は任意の受理済み現lambdaに適用可能。
当前source/Conn/target前提を保ち、新prefixの旧算術を再実行しない。

reply957を全文読み、その具体ABIと訂正を採用する。未完成なら公開された式と
正本v548/v543/v546/v547/Task957から独立なcoreを進め、最終replyと照合する。
数学上の段階A–Dだけで完全零判定ができる。非零の実体化Eは次consumerであり、
本版は正直にMATERIALIZATION_PENDINGを出す。新pivot/target更新は行わない。

## A–Dの実装

A. geometry: Q2=504*27*4=54432頂点、PSL index最速、kはbase3辞書順、parity外側。
   正edgeはRIGHT product q→qX/qY、edge index=2*q+slot。既存pmapはLEFTなので
   graph successorに流用しない。全vertex、全108864edge、六tag置換mapと全edge
   整合、固定positive BFS tree/parent/edge/order、五carryを保存・認証する。
   carryではrotation-left v=sign(e)kへ変換。六tag順/monomial/character順は実v15。
B. current_section: 新parentのlambda、全4 B-adjoint root、全8059 canonical lift
   contractionの和chiからjoint kappaを求める。新d1の6045行→旧d0/共有aux2014行。
   **逆代入はembedded ORIGINAL lead降順**。Task554は挿入順を逆にしてはならない。
   元row IDとchi値を保持し、全8059等式を最後の同じkappaで実測する。
   full96776の共有auxを4複製しない。物理basisの挿入順とは別契約。
C. source_cochain: 全六tag・d0/d1/d2・shared etaを含むactual source-edge pullback。
   `f=sum_a q_a Psi2[a]-kappa Psi1`。tagged Foxはphi_j(q)*prefixというLEFT product。
   `_seed_qnorm`はclosed word専用なのでraw edgeには新しいlinear adapterを作る。
   RIGHT X/XB正規化、augmentationのaux0..5、b_aux=-kappa_aux[6:8]を含める。
   有限score[6,2,54432]とf[108864]、b_aux[2]を封印する。mod3値を18で割らない。
D. complete_tree_test: 固定treeのpotential、全54433 chordのtau/値/残差を保存。
   最初の五つの独立tau columnを決定論的に選び、fit係数と全EOFを確認する。
   二auxと全chord residualが零ならCOMPLETE_ZERO_CANDIDATE。非零なら最初の
   aux、または最初のfailed chordから高々6cycleの固定順係数を出し、tau零と
   scalar非零を実測しVIOLATION_CANDIDATE/MATERIALIZATION_PENDINGとする。

deadline/cap/部分走査を零判定にしない。UNKNOWN_RESOURCEはdiagnosticのみ。
数学的範囲は全有限集合、時間上限は運用。巨大なfull source-edge matrixや
8059全decoded lift matrixを保持しない。Task554 bodyは一度に一つ、cacheは
chunkで読み、rho2元入力は旧同様の明示DERIVEDとactual current-target dotを区別。

## 実装と証拠の分離

公開CLI/JSON/array ABIを早期にreply959へ書きTask960へ伝える。共有はその契約、
正本の式、input pinだけ。新算術は自系retained lineageから独立に実装し、
checker source/solverを読まない。親admissionは実parent到着後にexactレイアウト
canaryを作り、旧成功算術を再実行しない。

CLIは既存11 roots＋新 `--refinement-root`、`--output`、`--max-seconds`、
`--selftest`、`--parent-layout-selftest`を基本にcheckerと固定する。
新source-only canaryは非単調lead、左右の非可換積、nonclosed raw edge、
全chord後端の改変/偽EOFを狙う少数のみ。本数値・AST・canaryはGHAで行う。
全配列とmanifest/roster/実source/runtime pinを独立checkerが再計算・比較できる形。

全出力はcandidate、cross_checked=false、verified=false。完全零はv548の
保持前提下の負判定候補であり、工房裁定前に格上げしない。非零から新rowや
literal/11-slot/fullA0を宣言しない。final byte/SHA、TCB、未実行gateを返信へ記す。
