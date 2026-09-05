# Task1000 — batch公開wireの残るnested型・root確定

宛先: Task994/995/996。Task997は凍結不変。本便は両作者の公開型の問いだけをrootで裁定した共通追補。
相手の新source/返信を読まない。Task994の数学・宇宙・非宣言境界・GHA限定は保持する。

## D1. 直接pairingはfive-key receipt、rowsは整数count

start.anchor_pairing と final/separator.direct_pairing は、plain exact
rows,row_pairings_sha256,lambda_pivots,lambda_parent_remainder,lambda_new_remainder の五key。
rowsは今回直接読んだ全行数、row_pairings_sha256は挿入順に実計算した全pairing u8 bytesのSHA256。
単に零列の期待hashを計算して実dotを省かない。lambda_pivots=0、二target値=1。

start.anchor_pairing_rows は実anchor rankのordinary整数（本初回1450）。零listにはしない。
final.separator.anchor_pairing_rows は新final lambdaで直接読んだ旧行count、final_pairing_rowsは旧＋採用行全count。
final.direct_pairing.rowsはfinal_pairing_rowsと一致。全旧/新row直接dot0、batch開始/最終target直接dot1。
Linearではfinalのdirect_pairing/lambda_rho2/lambda_sha256/anchor_pairing_rows/final_pairing_rowsをnull。
startは元Separatorへの入場なのでそのdirect receipt/countを保持する。

## D2. readoutのsupportは全タグが分かる固定型

p1_equation_residual_support は全8059式の保存residual非零件数のordinary整数、成功時0。
score_support はplain exact total,by_tag。totalは全score非零数、by_tagはtag0..5の六ordinary整数。
score既存shape[6,2,54432]のtag block毎に数え、六件の和=total。
kappa_support はplain exact total,degree0_by_character_tag,degree1_by_character_tag,aux_values。
二つのby_character_tagはcharacter0..3を行、tag0..5を列とした4x6のordinary整数list。
同既登録kappa[0:24192]を[4,6,2,504]、[24192:96768]を[4,6,2,3,504]として各character/tagのsupportを数える。
aux_valuesはkappa[96768:96776]の八tritをそのまま保持。totalは二表の全件数＋この八tritの非零数。
selection_readout.aux_valuesは従前通り実b_aux二件で、kappa_support.aux_values八件とは別。
これはTask994 C10の全tag/aux計測のexact型であり、full scopeを新しく広げるものではない。
既計算q/lambda character receipt、final q未計算、計測/P1同一lambdaは997通り。

## D3. 派生rho2と新rowのtarget親

新start.accepted_target_derivation_parentsは実anchorの最終result/C lambda_rho2にある全97親をdeepcopyする。
元output/startの33親へ戻さず、全64stepを含む97親の各full辞書/順/hash結合を認証する。
新final.lambda_rho2はplain exact八key:
mode,value,original_rho2_directly_read,original_rho2_packed_sha256,accepted_target_derivation_parents,
identity_convention,anchor_completed_steps,new_batch_target_steps_executed。
mode="derived",value=1,original_rho2_directly_read=false。元rho2 packed pinは旧受理の実値。
anchor_completed_stepsは実旧64、新batch_target_steps_executedは採用行数だけ。selected/processedとは同一視しない。
新parentsは旧97辞書の深いcopyを先頭に保持し、採用rowだけ一件ずつ追記。DEPENDENTは追記しない。

新追記一件のplain exact keyは
role,local_row_offset,candidate_ordinal,row_manifest_sha256,instruction_sha256,target_sha256,state_head,
parent_remainder_sha256,remainder_sha256,scalar。
role="batch-row"。local/ordinalはそれぞれ採用localと候補番号。row_manifest/instruction/targetは各実file全hash。
target_sha256はrows/<local>/target.jsonの全file hashで、remainder_sha256（packed target arrayのhash）とは別。
親/子remainder/scalarはそのtarget.jsonの三keyと完全一致し、実全座標の親−子=scalar*normalizedを再照合する。
state_headはその採用instruction rolling hash。未成立のresult_sha256を足さない。

identity_conventionはplain exact四keyで、文字列は次の通り:
- base: rho2 - base_remainder = sum(target.reductions.scalar * base_normalized_row)
- saved_deltas: parent_remainder - child_remainder = sum(target.new_reductions.scalar * saved_normalized_row)
- all_one_row_steps: parent_remainder - child_remainder = target.scalar * accepted_normalized_row
- batch_rows: parent_remainder - child_remainder = target.scalar * accepted_normalized_row; correction appends normalized_word^sr(target.scalar)

新final lambdaで全採用語像を殺すことと全target identityからrho2=1をDERIVEDとする。
Linearではlambda_rho2=null。ただしstartの旧親と各rowのtarget identity/literal factorは保存される。

## D4. 新fixed descriptorと旧manifestは別型として認証

旧continuation fixed/manifestのfilesはJSONにもdtype="json",shape=nullを持つ既存五key型。
その旧manifest全bytes/hash/各旧descriptorはそのまま旧型で認証し、変更しない。
新fixed/manifest.filesではJSONに限り、旧descriptorが正確にdtype="json",shape=nullと確認してから
file,bytes,sha256の三keyへ射影する。binaryは旧五keyのdtype/shapeを維持。
accepted_fixed_manifest自体の新descriptorは三key。新filesはその親directoryからの相対payloadを指す。
このmetadata射影でpayload/file hash、全EOF、role、元のaccepted manifest bindingを変えない。

## D5. source closureの記録

新P/C・各保持Python依存・rawはrootが最終全source/importを静的に読み、実全file/bytes/SHAで確定する。
Cからの公開見込みはcontinuation C v2を用いる十Pythonで、旧continuation C v1をimportしない。
見込みcountだけをfreezeせず、両作者は自系実closureのexact path列と実pinsを最終票へ記載する。
相手側はroot配達の公開pin rosterと実file hashのみ認証し、新算術本文を読まない。
