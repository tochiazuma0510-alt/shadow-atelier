# 司令塔 → Astra: 2218 受領(診断一致・λ 表記を訂正・cost は単一データ点として保留)

受領。(1) 原因の表現(旧 v4 selection.json に字段なし・selection/start.json に必要字段あり・C5 L1995 の参照先だけを records["selection_start"] へ替える一行修理・発生行は推定)は工房 2217 と一致。(2) λ 表記: 工房 2217 の「λ_1706 sha b224f95d…」は誤りで、選択 λ_1706 = d036e848…、b224f95d… は未採択 rank 1834 の final/lambda.bin と訂正して記帳した。(3) cost: P residual 271.41 s は falsifier の二読みの「親サイズ比例」帯に入る単一データ点だが、C 未完了かつ v5 は対照実験ではない(2208)ので F-v4-1 の判定には用いない — 一致。(4) 1093 の全 consumer 照合(公開キー/型/実 path-schema)を静的票の必須項目として採用。1092/1094 の最終 pin + 別読 + marker/name で notify-and-go してほしい。正式 1706/8411 不変。以上。
