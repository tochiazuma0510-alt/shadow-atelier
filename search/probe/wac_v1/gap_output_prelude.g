#############################################################################
## gap_output_prelude.g — GAP 出力罠の共通対処(2026-08-01 制度化・裁定 330)
## 全 probe は冒頭で Read("search/probe/wac_v1/gap_output_prelude.g"); すること。
## 対処する既知の罠(いずれも実事故由来):
##  1) Print/PrintTo が SizeScreen 幅で折り返し、JSON トークン中に \ 継続改行を
##     挿入して壊す(裁定 329・m2_crosstable の 1 回目実行で json.load 失敗)
##  2) SizeScreen の既定/4096 上限問題(wall28 系での事故)
##  3) 出力整形(インデント挿入)が machine-piped パースを壊す
## 使い方: cert を書く前に本ファイルを Read。個別 probe に同種の行を重複して
## 書かない(重複定義は本 prelude への一本化で置換していく)。
#############################################################################
SizeScreen([ 1000000, 1000000 ]);;
SetPrintFormattingStatus("*stdout*", false);
