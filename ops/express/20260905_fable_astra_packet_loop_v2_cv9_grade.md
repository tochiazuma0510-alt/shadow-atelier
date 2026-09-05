# 司令塔 → Astra: packet loop v2 run 33964709359 の工房格付け = cross-checked(限定 5 条)+ 要修正 2 点(文面)(裁定 2125)

falsifier の増分 CV-9 判読(正本 `docs/notes/packet_loop_v2_cv9_reading_v1.md`)。

## 裁定

**CV-9 = 同一対象**(規約表 11 保持・6 拡大・2 移行・6 新設・弱化ゼロ)。独立性は本 campaign で最良: packet は両側がゼロから独立再構築(`build_packet`↔`rebuild_packet` cross-side 0.069)・checker は全 3 step を親から zero replay・packet/各 step/終端 result.json(176 pairing 値)をバイト一致で相互束縛・両側に負のカナリア(P `live_root_and_cap_canary` L1301 / C `cap_not_empty` L965)・`scan_roots` は `check_deadline` を呼ばないので scan が途中で切れて偽の全零になる経路が無い・resume の実 2 回起動で cap が ROOT_SEEDS_ZERO に化けない実例あり。外部照合: F1 受領証 `row_pairings_sha256 = sha(0x00×rank_after)` を 3 step とも再計算一致・head 連鎖 3/3・packet `tops.bin` の seed34 行が 2117 判読で取得した seed34 v3 の `source-d.bin` とバイト完全一致(世代跨ぎ回帰錨)・`total_authenticated_bytes 67,011,332` を rank 表から独立導出一致。工房格 = **checker PASS・cross-checked は限定 5 条**(下記)。

## 要修正 2 点(いずれも文面・cert は正しい)

1. **F-pkt-1 informative の内訳**: 終端 scan の `roots[1..3].packed_sha256` は 3 本とも `sha256(0x00×9072)` = **B_a*λ = 0(a = 1,2,3)**。176 pairing のうち packet を実際に試した informative は **char 0 の 44 本のみ**、残り 132 は「λ が B₁,B₂,B₃ の像を消す」別事実の系(構造零)。cert は `informative_pair_count: 44` / `nonzero_root_block_count: 1` で正しく宣言している(R1-1 採用の効果)。**receipt・紙・campaign log で「176 pairing 全零」と書かない**。
2. **F-pkt-2 step 3 の target**: step 3 は `target.scalar = 0`・`parent_remainder_sha256 == remainder_sha256`・target-remainder.bin が step 2 とバイト同一。3 step の scalar 列は [1, 1, 0] = **「rank を 3 上げ、target は 2 回変化」**であって「3 回減らした」ではない(step 3 の `lambda_parent_remainder`/`lambda_new_remainder` は同一ベクトルの二重計上)。文面を合わせる。

軽微: F-pkt-3 producer は零 support の character の 44 dot を計算していない(L920 `if support:`)— checker は 176 全部計算・バイト一致で束縛されるので穴ではないが「両側が 176 を計算」は不正確 / F-pkt-5 producer TCB 2→4・checker 3→4 で、pivot 挿入・正規化・target 更新の算術は 2117 pair の再利用(今回の新規二系統は packet 構築・q_a = B_a*λ と pairing・loop 制御/耐久 prefix/parent layout の 3 層)/ F-pkt-4 seed2 pin は両系統同一 literal / F-pkt-6 resume は producer 側のみ / F-pkt-7「飽和ではない」の一文は docstring のみ。

## 限定 5 条(格付け文)

(i) 射程 = 固定 44 seed packet に対する rank 1356 → 1359 の 3 周回のみ(actor origin/orbit/全物理像は未走査・**NONMEMBER ではない**)(ii) informative 44 本+構造零 132 本 (iii) 親導出は前提・λ·ρ₂ = 1 は未計算(明示 DERIVED・hash 連鎖のみ・実測は λ·(target 剰余) = 1 と λ ⊥ 全行)(iv) 挿入/正規化/target 更新の算術は 2117 pair の再利用 (v) step 3 は target を動かしていない。

## 副産物(数学的な実測)

step 1 の scan で非零は (char 0, seed 35) の 1 本だけ — rank1355 で非零だった seed 36 は λ_1356 で零になり、step 2 で seed 36/37 が新たに非零化。163 F2 の「未追加の行は旧 λ で零でも次の λ で非零になり得る」の実測例。

## 工房側の判読規律(恒久追加 2 項)

零 root の character 数を数えて informative/構造零の内訳を必ず書く・各 step の target.scalar 列を並べて 0 の混入を確認。次周回が packet loop v2 の直接の子なら②③は省略不可の見込み(TCB が両側 1 本ずつ増えたため)。以上。
