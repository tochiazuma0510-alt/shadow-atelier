# Task1110 addendum v1 — 祖先recordの旧shapeを保持する
宛先: packet_checker、公開部分は packet_producer / packet_bounds_audit にも適用。Task1110本体6639/978cc9e442b5c886ef13faed0af5d879c8059de317107e946414cd8a1444da78は上書きせず保持する。
本体要件3の「旧97→225→353→481の全十key辞書」という短縮句を、**各世代の元keysetを維持する**意味へ限定する。元97件は32件の5-key＋65件の6-keyを原辞書/順序/pinのまま保持し、その後のv3/v4/v5の各128件（384件）だけが10-key batch target recordsである。481件を一律10-keyへcast/拡張/再封印しない。次start481、final481＋採用a、追加a件だけ10-key。零scalarも保持する。根拠2224正本§4.4と既1103の全353prefix/481保存票。
これは旧型を新型へ変更する委嘱ではなく、本体の語句の明確化。1107の公開wireにもこの区別を反映し、source実装の全consumer目録で旧root/schemaのnative keysetを照合する。P/C私的本文共有/数学実行/親変更0。
