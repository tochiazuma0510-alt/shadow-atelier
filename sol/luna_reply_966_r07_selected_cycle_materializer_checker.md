# Task966 — selected-cycle E checker / workflow 最終凍結

F0. 指定三ファイルを完成した。Task965/966、reply963、reply957 E、reply958、v547/v548、最終959/965公開ABIを読み、割込みTask968を先に公開凍結してから本便へ戻った。旧source/workflow/replyは変更していない。新producer算術の読取・import・共有、ローカルPython/import/AST/数値/GAP、network/git/credential/dispatch、追加agentはない。source/JSON/metadata/bytes/hash読取りと指定ファイルの実装だけを行った。rootとTask967が最終source/workflowを全文読了し、必須修正なしを報告した。これは静的受領であり、新Eの実行PASSではない。

## F1. 凍結値と実親

| file | bytes | SHA256 | LF / CR |
|---|---:|---|---:|
| `search/check_d972_r07_selected_cycle_materializer_v1.py` | 103757 | `a6d52e0d12d97201f0a19f25c54e0924e3fbea89fefa3554727a7178881218b4` | 1516 / 0 |
| `.github/workflows/d972-r07-selected-cycle-materializer-v1.yml` | 44334 | `def1e1813427ebd530210cc743c79dd3e3b983114bd689c6a94d6c1154c75483` | 689 / 0 |

双方BOMなし・末尾LFあり。末尾空白text検索一致0。固定相手producerは **88929 bytes / `4f600aae93bf5749d15229cfdfe3e4546267f8b0a642ac46b65125a3c3164ac3`**。公開ABI正本 `sol/luna_reply_965_r07_selected_cycle_materializer.md` は **30068 / `ae01a8352e4ab5bc16cac8b788dbd090892f9ff8f5f32f3df50780c1218b4835`**。

実oracle親は **run33977701313/1、head `bbce98d8f95a845f36fe89c0f507b9360792666f`**、workflow `.github/workflows/d972-r07-section-cochain-checker-completion-v1.yml`、artifact **9972829869**、name `d972-r07-section-cochain-checker-completion-v1-candidate-33977701313-1`、ZIP **2299772 / `sha256:1a5c8800af563493b95dd4166d20c2fe1b74449f5f7f15aa99278d9b1c1b878d`**。root回収先 `%TEMP%/shadow-atelier-section-oracle-completion-run33977701313-candidate-a1` の十entryを独立bytes/SHA照合した。

| entry | bytes | SHA256 |
|---|---:|---|
| source-receipt.json | 2673 | `cd9a45a389cafd0cfb3813181c1365b0a66cdd682cc737a1a68f27b438d92934` |
| checker-result.json | 15387 | `92739f2db1007ec9ee040716c9dcb26859c10e5a5917a377514bb8e4eb4cd41a` |
| completion-run-receipt.json | 2089 | `3c2eb678db147c7538adf7520f19d91610b255488464704d32a224f9cda4102b` |
| repair-source-receipt.json | 3204 | `2b2efda3b1922e30246621a8b8cf87a277587767ca77662a03b7a35ef821bd37` |
| preserved-input.json | 10504 | `332f6b62aca1042868e65117d4cc9de952ef8d4817d5169ae8a1ee1a9298e625` |
| output/manifest.json | 1430 | `7df077372a51d12cbf95be5f26c94a5e29ef0f6b118f1ed7efb452ba01942639` |
| output/start.json | 48377 | `7ff970e54dec57512593f5445fed387075d6602bff31f41b7db9f34bab045a2a` |
| output/owner.json | 8419 | `6c71fbc405105bd0722924a308594ba41aea6745725ae85d046ff7409998b322` |
| output/source.json | 1246 | `af1e178d19e4ee427439d102de74a559ed6202ca0a2839212a60748ccfe482ac` |
| output/result.json | 13727 | `c7f65255443a8901fa1b6fbab69e81bbc811014e1eb527e7f671e2f6343ba312` |

preserved-input中のoutput全 **44 files / 5361492 bytes** も実hashと独立照合し、不一致0、実directory4を確認した。実親metadataは PASS/VIOLATION_CANDIDATE、rank1385/gen8090、8059等式・54433chords・2aux・全arrays比較、physical0。headは `8f6605a28d337cd8541a7eacf6aef78f5a70308a6bb71fd105138803ca623a61`、lambdaは `1e720af4a30bac955ab4565366f0242b5c2d43125eb280e241df20976331cdf1`、targetは `111d12e064b96a6bf579f39a9c9d5e35181560c0403bf0d237bffc924230c0ad`。witness全file SHAは `1c282b82cbf430b3ef492a325c26ac3c7d2bf9146f15aa76c94744f8477620fd`。cycle順[12,2,3,4,6,11]、係数[1,1,0,1,1,1]、eta[0,0]、tau零、scalar1は受理親metadataであり、新Eのtarget scalar/終端を予測しない。

元producer/source/outputは **33975617653 / head `c57a722224320f9a573cfe84dea6979df5cb5320`** のv1、producer **73290 / `4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb`**。成功checkerはv2 **84402 / `a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d`**。旧v1 FAILを上書きしない。旧14 source receipt＝repair先頭14、新repair末尾v2、completion/preserved originとruntimeを別に結ぶ。今回の実行closureは **E2＋元14＝16 Python、3 data files**。v2は親provenanceであり今回importしない。

## F2. 実装とABI

schemaは `d972.r07.selected-cycle-materializer.v1`。ASCII/key順/compact/末尾LF、sealは自身shaだけ除外、file hashは全bytes。instructionはrolling_sha256、targetはplain三字段。residue54は通常int0..53/bool不可で、tritやpacked3ではない。

本番は独自RawSLP→actual Q0/Q2/整数epsilon/omega/LEFT Fox→同じraw-rootの直接六tag Fox→ordinary27差分基底の全degree/四character/sharedauxへ接続済み。producer binomial helperを使わない。rootの指摘したatom/Fox-zeroの誤gateを修理し、r_x/r_y自身はendpointだけ、実 r_x^3/r_y^3/commutator の三修復語にFox-zeroを要求する。canaryもatom augmentation2と三修復語零を区別する。六cycleの零係数・順序、v547普通整数/6、auxの同じeta、actual36点Q0とGamma0の区別を保つ。

primalはold全embedded元lead昇順→new owner-major元lead昇順、全8059alpha/eventと全96776 lower-zero。old四d1 companion/sharedauxを含め、normalized rowへscaleを再乗算しない。prepareと各new bodyは一つずつ読み、大きな旧bodyを次の前に解放する。P1 literalは1-based seed、owner-local actor/reductions、whole old defectを一度project、internal scale一回をmod54へ送り、全8059 positioned instructions/ancestryをjoinする。整数projector4をF3の1に潰さない。巨大P1普通整数をexportしたとは言わず、mod54で18整除と/18 mod3を完全に決める。raw /6は普通整数のまま。

全12 source blobと全P1 cache/8059 row/EOFを認証し、raw tupleのfresh copyからP1を一度だけ引く。別に求めたprimal lowerと全96776座標で比較し、同じalphaで全四topを補正する。四Bは出力座標別の整数grouped sum、fresh qはown pullback。`selected = homogeneous-section = corrected = physical = remainder !=0`を要求する。accepted checker物理primitiveで一行を消去/normalize/追加し、動的rank/gen、target scalar0、fresh separatorの全current rowsと両target dotを保持する。元rho2は受理target identities＋新一行identityによる明示DERIVED。

V_wordのsource-lower零とConnを引くnormalized literalのphysical-lower零を分け、後者は `source_lower_zero:NOT_ASSERTED`。raw whole-wordだけ直接実行、P1語はtyped ancestry＋source replay。normalized/target whole-word・全11slotは未再生。target零は `LINEAR_MEMBERSHIP_CANDIDATE` / `TASK958_PENDING`、MEMBER/full A0へ上げない。

全array/JSON/typed roster/manifest/HEADを完全bytes＋1byte超読で比較した後だけchecker PASS。telemetryのstage/bytes/letters/alpha support/EOFを実payloadへ結び、elapsed_secondsだけはfinite非負で双方値一致を要求しない。内部deadline/SIGINT/SIGTERMは完成stageだけを残すUNKNOWN_RESOURCE/exit3。旧26scan/insertや旧oracle A–D一式を再走しない。

## F3. 新gate・workflow・再現CLI

親metadata変異は旧15＋oracle roster/witness/snapshot/EOF/current-rootの5、計20。新checker selftestは三群：(1)非可換負冪/Fox/omega、実normalizer/負九乗raw六tag/directsource、全24塊mixed probe/shared8aux、(2)逆挿入と異なる元lead順/old四d1/sharedaux/mod54型、(3)one-row/target scalar0/linear candidate/dynamic generation/plain target/全EOF。親不要の入力fixtureだけにretained v1 Geometry、比較anchorだけにretained polynomial forwardを使う。旧full selftest/section/cochain/tree solverは呼ばない。本番ordinary27経路にpolynomial helperへの辺はない。

workflow markerは `[r07-selected-cycle-materializer-v1-run]`、branchは `sol/r07-explicit-lift-20260825`。既存12親＋実oracleの13 live tuples、実oracle ZIP/十entry、16 source/三raw data/19-word rosterを認証する。source ASTはGHAだけ、dataへLF正規化を掛けない。producer selftestはpublic `groups`、checkerは`tests`を別gateにして各三群を確認する。

順序は source/親→双方20 metadata→新三群→producer一回→checker一回→oracle全44files/4dirs/十entryと16source/三dataの前後不変→candidate。双方内1800秒/外40分/job100分、metadataとcanaryは各内240秒/外5分。UNKNOWN/failureはcandidateにせずdiagnostics always。NOT_APPLICABLEはphysical0の型付きreportだけ。`oracle-intake-receipt.json` と `run-receipt.json` はcandidate/diagnostic双方へ残し、run/attempt/head/workflowSHA/runtime/各回数/上限を保存する。

GHAで親root環境変数を解決した後の実CLI（ローカル実行していない）：

```bash
python -B -u search/d972_r07_selected_cycle_materializer_v1.py \
  --state-root "$STATE_ROOT" --delta-root "$DELTA_ROOT" --seed34-root "$SEED34_ROOT" \
  --packet-root "$PACKET_ROOT" --refinement-root "$REFINEMENT_ROOT" --oracle-root "$ORACLE_ROOT" \
  --prepare-root "$PREPARE_ROOT" --block-root "$BLOCK_0_ROOT" --block-root "$BLOCK_1_ROOT" \
  --block-root "$BLOCK_2_ROOT" --block-root "$BLOCK_3_ROOT" --p1-root "$P1_ROOT" --task712-root "$TASK712_ROOT" \
  --output "$RUNNER_TEMP/output" --max-seconds 1800
python -B -u search/check_d972_r07_selected_cycle_materializer_v1.py \
  --state-root "$STATE_ROOT" --delta-root "$DELTA_ROOT" --seed34-root "$SEED34_ROOT" \
  --packet-root "$PACKET_ROOT" --refinement-root "$REFINEMENT_ROOT" --oracle-root "$ORACLE_ROOT" \
  --prepare-root "$PREPARE_ROOT" --block-root "$BLOCK_0_ROOT" --block-root "$BLOCK_1_ROOT" \
  --block-root "$BLOCK_2_ROOT" --block-root "$BLOCK_3_ROOT" --p1-root "$P1_ROOT" --task712-root "$TASK712_ROOT" \
  --candidate-root "$RUNNER_TEMP/output" --output "$RUNNER_TEMP/checker-result.json" --max-seconds 1800
```

## F4. 2138/2131の保持TCBと未実行範囲

`docs/notes/section_cochain_v1_cv9_reading_v1.md` を全文読んだ。2138はoracleをSAME_OBJECT/cross-checked限定8条とした。rank1385の現lambdaに対する有限事実だけを受理し、新EのPASSやMEMBER/NONMEMBERへ移さない。

- F-sc-1：`read_task712_envelope`/`_load_words`の同一clone、context高類似が残る。transport/PSL列挙/B復号、source/P1/Conn completenessは保持入力TCBであり、新二系統一致だけの射程外。
- F-sc-2：実親q1..3零、24 coefficient blocks中非零6、score tag3..5零、kappa aux8零、zero/aux branch本番未走。全四scopeを保持するが全部が有意とは言わない。新canaryは旧空虚性を遡及的に閉じない。
- F-sc-3：completionはv2専用15 serialization canaryだけ、保存full selftestはv1。Eのretained importもv1であり、不良geometry_payloadsは呼ばない。次の実v2使用runでfull selftest一回の義務はrootが保持する。
- F-sc-4/5、q/kappa/受理親への第三実装の未到達、最初のfailed chordを選ぶ偏りも親限定のまま。第三実装のscore/f/tree全一致は親の証拠であってE実行結果ではない。
- 2131/F-fo-1：旧scan child covector同一実装/P1 projection near-clone、seed2 hash継承、packet target[1,1,0]、lambda-rho2 DERIVEDとrank1385七限定を残す。Task958 positive/normalized・target whole-word11slotは別consumer。

F5. 残gateはrootの最終source/workflow/Task967突合とrelease、GHAのAST・実親20変異・新三群、実一行producer、独立全payload照合、runtime/immutable receipt、candidate回収、新E CV9。**新E run ID/commit/terminalは未観測**。本workerは発火せず、rootが唯一のbrokerとして実run/commitを記録する。凍結後に必要修正があれば根拠と新hashをrootへ連絡する。

AUDIT_966_VERDICT: SOURCE_AND_WORKFLOW_FROZEN_WITH_OBSERVED_ORACLE_PARENT; STATIC_SOURCE_WORKFLOW_NO_REMAINING_FIX; NEW_GHA_AND_E_CV9_PENDING; CV9_2138_EIGHT_LIMITS_AND_2131_SEVEN_LIMITS_RETAINED; verified=false
