#############################################################################
## search/probe/wac_v1/roof2_a4_anchor_run.g
## M2 屋根走査 R2-5(アンカー A4)の起動ラッパー。
##
## docs/notes/roof2_cv9_freeze_v1.md SS5.1 R2-5 の指示:「既存 R4b driver を
## 無改変で m=0 シャードだけ再走する」。search/probe/wac_v1/ihnec_r4b_run.g
## は自身の preamble 変数 R4B_TARGET_MS / R4B_OUTPUT による shard 注入機構を
## 既に備えている(同ファイル冒頭コメント参照)ので、本ラッパーはその機構を
## 使って m=0 だけを注入するだけであり、ihnec_r4b_run.g 自体は一切変更しない。
##
## 出力: search/certs/roof2_a4_anchor_20260801.json(972屋根 m=0 シャードの
## 再現・shadow_total は roof2_scan_20260801.g の主 driver から期待値 81 と
## 突合される)。ihnec_r4b_run.g は末尾で QUIT するので本ラッパーは独立プロセス
## として実行すること: .\gap.ps1 search\probe\wac_v1\roof2_a4_anchor_run.g
#############################################################################
R4B_TARGET_MS := [0];;
R4B_OUTPUT := "search/certs/roof2_a4_anchor_20260801.json";;
Read("search/probe/wac_v1/ihnec_r4b_run.g");
