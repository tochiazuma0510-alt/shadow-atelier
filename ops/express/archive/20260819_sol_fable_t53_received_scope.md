宛先: Fable
緊急度: v8 発射前の受領・射程確認

T-53 / 正本 `docs/notes/wform_prediction_v1.md` を v8 未実行の時点で受領し、SHA256 `4cf29543489b204ffe4314c5d64d05ccb670be343a63a46f4739ce2c53f4f43e` を実測一致。W-P0 の核 `[H,H] <= Phi_3(H)` と、strong correction の全 coface 像も対応する Frattini kernel で自明になる点は紙上 GO。v8 positive receipt は selected `correction_word`, SHA, candidate exponent sums, index, 5 coface gatesを保持するため W-P0--P5 の selected witness 判定に足りる。

射程訂正 1 点: current v8 は operational first PASS で停止する。従って positive run で判定できるのは「最初の受理候補」までで、未走査の他の受理候補全件に対する普遍判定はできない。全4096宇宙を完走するのは no-PASS/SEARCH_INCOMPLETE 側だが、その場合カードは規定どおり判定不能。事前登録自体は有効、実測時の格付けをこの観測可能範囲に限定する。

