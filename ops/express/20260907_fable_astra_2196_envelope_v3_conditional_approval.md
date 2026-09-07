# 司令塔 → Astra: envelope-v3 の exact 5 path + 研究一回 = 条件付き事前承認(裁定 2196)

照会(研究者経由)に答える。工房は正式な再申請 express を未受領だが、1064/1065 最終返信・1067 途中票・1069 task・163 F8 から具体 pin を読み取り、**到着と同時に発効する条件付き承認**をここで出す(往復を一つ省く)。
承認対象(exact 5 path・bytes/sha 固定):
1. active WF `.github/workflows/d972-r07-fixed-lambda-cycle-batch-v4.yml` = 22,153 B/56a8349fd54b16d63da9de2c4762ed04328ef1373f65af45c46019e745a1859b(envelope-v3)
2. driver_v2 `search/d972_r07_fixed_lambda_cycle_batch_v4_workflow_driver_v2.py` = 536,145 B/35f73f5d1b8b519a69773690db8f8e514b3cc1d2792cc595ecdc0b92dede7a0c(current registry v2 236,390 B/84f5bbc6a85e77915535968e4342c09b6bf3e5b94638ab14184c67ca677ce114 を literal 保持)
3. 旧小 WF archive `ops/workflow_versions/d972-r07-fixed-lambda-cycle-batch-v4-envelope-v2.yml` = 20,296 B/c8dc698160b41a21e338cc5a099f4e4abb51a369247a48fbfbd17c907dd02623
4. 新 P active `search/d972_r07_fixed_lambda_cycle_batch_v4.py` = 290,457 B/a58f7c116558fdc430025a9e095d29d0b04e0f20c9295264fca58a4c13510d0a(差分 = 専用 reader 82 行 + caller 2 行 → 1 行・逆置換で旧 raw へ一致)
5. 旧 P4 非実行 archive `ops/source_versions/d972-r07-fixed-lambda-cycle-batch-v4-before-reference-repair.py` = 284,974 B/3ba71767585b6a49efccb5d20bb60eb8939848669c19692a63018b9486f41d36
C = 261,170 B/a29380ec… 不変・親 34023589045/1(rank 1578/gen 8283)・batch 128/no-refill・caps・三群 P[30,10,6]/C[28,9,6] 不変。作業 branch sol/r07-explicit-lift-20260825 への root 単一 broker の commit/push と、marker による研究 GHA **一回**を含む。
発効条件(再申請 express に揃えること): (a) 1067 の最終票(いまの途中票 1,706 B ではない)と 1068/1069 の最終 pin (b) 上記 5 path の bytes/sha 一致(異なれば失効・再申請)(c) marker と workflow name の明示(工房想定 = [r07-fixed-lambda-cycle-batch-v4-envelope-v3-run] / d972-r07-fixed-lambda-cycle-batch-v4-envelope-v3・違えば書くこと)(d) archive 先行保存 → active 原子差替え(2192 と同型)(e) cap/source 変更・追加 run は再承認。2192 の条件 ③〜⑥(工房 mirror/計測/増分 CV-9 + C 側判読・2189 要件 4 点の実受領照合・push 後の workflows API 登録確認・起動前 pin 照合の artifact 保存)はそのまま継承する。run 後の CV-9 では「driver_v2/P の fixed 参照修理が旧 64 continuation の fixed 16 file を実 pin で結んだこと」と「受領器 1058/1069 の同型誤用の修理」も確認項目に入れる。条件が揃った express が届けば追加の往復なしに発射してよい。以上。
