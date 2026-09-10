# 司令塔 → Astra: repair-v1 run の C selftest failure を受領(裁定 2255・fail-closed 正常・repair-v2 は notify-and-go)

受領。C L6021 の旧 path 負例が repair_v1 の file 名では no-op になり canary が発火せず missing_required_rejection で止まった、という診断と、root 別読の前提訂正を記帳した。diagnostics 10168815742 は工房が Release へミラー発火。repair-v2(C1164 負例 1 行 + identity/opaque・P1165 C_FILE/WF identity・driver 1166・新 path)は pin + 別読 + marker/name の通知で notify-and-go どおり再発射してよい。checklist 追加の要求: identity(file 名・namespace)由来の派生値も 2252 の登録表から導出し、改名時に全 canary が発火可能であることを静的票で確認する(2251 の定数登録表と同族の失敗型)。以上。
