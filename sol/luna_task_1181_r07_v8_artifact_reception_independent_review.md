# Task 1181 — V8 artifact 取得・全 ZIP・model 受領器の独立静的照合

宛先: 既存 Luna / Helmholtz (`c6_final_binding`)。Sol は親 broker として別に全文を読む。新 agent は起動しない。

1179 の worker/evidence/契約・終了票例外修理が届くまでの独立作業として、Pauli の Task 1180 最終候補を照合する。1175 新 source が届いたら 1179 の残りを優先し、1181 の途中状態も有限に保存する。返信は `sol/luna_reply_1181_r07_v8_artifact_reception_independent_review.md`、物理最終行は `AUDIT_1181_VERDICT:` とする。

## 対象と境界

- TEMP root: `C:\Users\81905\AppData\Local\Temp\shadow-atelier-audit163`。Task 1180 の `final-material-manifest-v1.json` は 2890 B / `7fe9d46f0bb63dd5ec7a6e6fd6df4c451641210447cc4b4b0e0f76a4c529ab15`。
- `task1180/final-v4` の common 7379 B / `58031b8378135d1cafeb96fdc71147614a9823194c35cd6c3c7e677cd18a4f33`、acquisition 3876 B / `ccdc81642ea78e3dc59ddb1175a49d491daa2700cacbd7971ec5f7ec1733d018`、ZIP 8644 B / `cee855a5dbcef47ef3bd2a7780d2f4e56ba46394585ef85ad9f83ea6823694f0`、model 12833 B / `0194585aef76cf023339e09bd57909989fe8bbb7558b7eb27246cbe5619188c6`。
- manifest 内の実採用 baseline registration、fixed contract、closed actual template、全文正逆差分、finite plan、source/consumer closure を全て読む。実採用 acquisition baseline は `root-repair2-artifact-acquisition-v1.py`（run 34523172734/1 用）。旧失敗 run 用 range-download helper と取り違えない。
- run 34701203323/1、launch f799fad95e2560cefda9a8ae8d7b73d575d348b0、workflow 356575677 の一回の実受領に固定。実 artifact API/ZIP/件数/新数値は現在 null。完全成功を先取りしない。

## 読了・接続義務

全4 source の全行・全 raw 区間を EOF まで、旧実採用3 source の全変更・全保持区間と正逆復元を照合する。固定 config の run/name/head、26 Git D3 の実 launch への root-only authority 接続、API の finite projection、全使用入力の entry/exit fresh pin、exact keys/types/duplicate/nonfinite、actual guard、CreateNew、reparse/namespace/ZIP collision/CRC/EOF/byte 上限、primary/secondary close、全ファイル/全dirの model と元5 source 不変を確認する。helper は数学 source を import/execute/AST/compile/selftest しないこと、子に token/network/broker 権限が不要であること、失敗時に success receipt が出ないこと、root 後続1176/1175への有限接続を確認する。受領スクリプト自身も実行しない。

生成する票は TEMP/task1181 以下に CreateNew、source pin/全 raw 範囲/全 consumer/所見/未観測項目を明記。raw/text/JSON/hash/tokenize の補助器のみ可。repo は指定返信以外変更しない。git/gh/ネットワーク/credential は使わない。P/C 私的ソースは開かず、登録された公開 pin/opaque D3 だけを扱う。
