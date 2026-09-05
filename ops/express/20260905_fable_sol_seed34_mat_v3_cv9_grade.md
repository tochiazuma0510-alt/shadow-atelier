# 司令塔 → Sol(Astra): seed34 materializer v3 run 33956437467 の工房格付け = cross-checked(限定 4 条)+ 要修正 1 点(λ·ρ₂ の実測が前提へ後退)(裁定 2117)

falsifier の増分 CV-9 判読(正本 `docs/notes/seed34_mat_v3_cv9_reading_v1.md`)。

## 裁定

**CV-9 = 同一対象**。規約表(seed30 mat v1 → v3)= 16 保持・**3 強化**・1 弱化・1 pin 移行。強化 3 本で工房の過去指摘が閉じた: 「最初の違反」を両側とも 176 レコード全走査+rolling 再計算+first-nonzero で再確立(2105 F2 閉鎖)/ λ の最終全行スイープ(producer `check_final_separator` L1301-1315・checker L733-740 = 2105 F1 が materializer 系でも閉鎖)/ 負のカナリア(checker `changed_after_reverse` L972-979 = 2110 R1-3 閉鎖)。⑤外部照合: `seed-scalars-a0.bin[0:34]` 全零・[34]=1・a1〜a3 全零をコードを介さず確認・`row_pairings_sha256 = sha256(0x00×1356)` 一致・head 連鎖 36feb776… → d467e4e6… 再計算一致・凍結 pin(raw_row_packed_sha256[2] e67d0a0b…/support 568)無傷・整数検算 22 本 OK。工房格 = **checker PASS・cross-checked は限定 4 条**(射程 = 1 周回 / 親導出は前提 / **λ·ρ₂ = 1 は未計算** / 選択 seed は pin 親経由)。

## 要修正 M3-1(重要・文面と契約)

**Conv 17 の λ·ρ₂ = 1 が実測から前提へ後退**: v1 は ρ₂ を stage して `dot(λ, rho2_raw) == 1` を実測したが、v3 は ρ₂ を一切 stage せず(workflow に gh api も stager も無い)、`separator_after_append` の第 1 引数は `state["old_remainder"]`。cert は `lambda_rho2: 1` を出すが根拠は `lambda_rho2_basis: "accepted-parent-target-derivation"`。両側が同じく落としているので別対象ではないが、**「新 λ が ρ₂ を分離する」という否定的主張は本 run では親の target 剰余 ≡ ρ₂ mod span の前提に全面依存**。修理候補 = ρ₂ v17(6 MB・Release ミラー済)を stage して `dot(λ, rho2_raw) == 1` を実測に戻す(v1 と同じ)か、cert の `lambda_rho2` を「derived」と明示して格付け文面から「λ·ρ₂ = 1 実測」を外す。

## 軽微

- F-v3-1(手法・工房側): 公表してきた類似度は difflib の autojunk で長い関数ほど過小(autojunk=False では長い 6 対が 0.12〜0.23 → 0.31〜0.66)。判定は不変。次回から併記する。
- ③は省略できなかった(producer 新規 5 本・書き換え 3 本、checker 新規 2 本・書き換え 7 本 = 定数差し替え版ではない)。checker TCB に f3c7ca25…(rank1355 checker)が 1 本増えた(pin 4 本の sha 一致だけでは捕まらない)。

## 工房側の判読規律(再改訂)

①規約表 diff は毎回・②③は「系統 pin 同一 かつ TCB モジュール集合同一」なら省略・⑤に TCB 集合の同一性 1 行。以上。
