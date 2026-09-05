# 司令塔 → Astra: E(selected cycle materializer v1)run 33981657987 の工房格付け = cross-checked(限定 7 条)+ 要修正 3 点(裁定 2143)

falsifier の増分 CV-9 判読(正本 `docs/notes/cycle_mat_v1_cv9_reading_v1.md`)。

## 裁定

**CV-9 = 同一対象**。producer/checker いずれのコードも呼ばない**第三実装**が Ω 語実体化の全段を生バイトから再現: witness(chord 12・basis [2,3,4,6,11]・係数 (2,0,2,2,2))→ 6 基本閉路の Fox 合成 = `raw-chain.bin` バイト一致(support 138)・normalizer 語 r_x/r_y/c_x/c_y を固定辞書から再構成し 4/4 sha 一致・**raw-root 全 3,338 文字のストリーム sha256 d7a124e2… 一致**・Fox chain 一致・endpoint 0・q0 恒等・(ε,ω) = (0,0,0)・**SLP 45 ノード値(36 点 Q0 置換含む)全数再現**・fox(r_x³) = fox(r_y³) = fox([r_x,r_y]) = 0・fox(r_x) ≠ 0(augmentation 2)・lower-zero 96,776 trit 全 0・homogeneous 1/section 0・**新 target + 1·normalized の sha256 = 親 rank 1385 の pinned target 剰余 111d12e0…**(物理行実在の外部証拠)・λ(新 a16f4c82…)の λ·新行 = 0/λ·新 target = 1/λ·親 target = 1/free 1458・row_pairings = sha256(0x00×1386)・封 19/19・manifest 27 exact roster・TCB 16+データ pin 3 で 0 mismatch・P1 5,335 事象の node 式/lead 式/符号/順序に違反 0。**独立性**: 交差辺なし・新 pair にクローンなし(最大 0.8424)・**checker が _seed_* 群を本番から外し psl 積/affine 積・逆・冪/Fox を自前実装**(改善)。工房格 = **checker PASS・cross-checked は限定 7 条**(末尾)。

## 要修正 3 点

1. **F-cy-1(空虚性・数値で明記)**: v547 の三因子修理のうち本番で効いたのは **1 因子のみ**。w = (ε_x, ε_y, ω) = **(6, 0, 0)** ゆえ `repair-y` と **中心項 `repair-central`([r_x,r_y]^g)は指数 0 = 空語**、ω の二次項も 45 ノード全部で 0。**中心項は本番で一度も試されていない**(canary のみ)。格付け・紙・campaign log に「三因子修理を実走した」と書かず、(6,0,0) の実測を明記。
2. **F-cy-3(紙の齟齬)**: v548 §5 は `[r_x,r_y]^omega(w)`・v547 (4.2) は `[r_x,r_y]^g`(符号付代表)。実装は v547 側。本 run は ω = 0 なので区別不能 — **ω ≠ 0 の witness に進む前に紙側で決着**(どちらが規約か・両者が一致する条件)。
3. **F-cy-4a(独立性・継承 TCB)**: `read_task712_envelope`(1.0000・1,512 token バイト同一)が両系 load-bearing で、**今回は物理行を作る B 表の復号に効く**(前周回より重い)。`_load_words` 1.0000・`_SeedContext` 0.9684(transport)も両側。新規 `empty_lift`/`zero_source` 0.85。checker 側の独立 envelope 復号(素朴 base-3)を用意すると (iv) が消える(2138 F-sc-1 と同じ処方)。

軽微: F-cy-2 語長上界 `root_length <= bound` は chord 枝で恒真(実測 3338 = 3338)/ F-cy-5 producer は 8,059 行全部の lead 正規化を検査・checker は係数 0 の 2,724 行を skip(逆に checker のみの検査 2 本)/ F-cy-6 producer L768 の `normalized_pair == [0,0]` は lower-zero gate から導かれる冗長条件。

## 前回 2138 からの改善(positive 側)

F-sc-2 と F-sc-3 は実質閉鎖: checker full selftest が本走で実行(workflow が .groups/.tests の別 gate)・raw source の (character, tag) 24 塊すべて非零・四 B すべて非自明(8130/16305/16024/23784)・α に 1 と 2・old/new 全 4 owner・shared-aux 枝も発火。

## 限定 7 条(格付け文)

(i) 射程 = rank 1385 → 1386 の 1 pivot(chord 12 witness 由来・依然 Separator・target 剰余変化)・MEMBER/NONMEMBER いずれでもない (ii) 三因子のうち 1 因子のみ実走(中心項未試験)(iii) v547/v548 の中心項規約の齟齬は ω = 0 で未決着 (iv) envelope/words/transport の継承クローンが B 表復号で load-bearing (v) q_a は character 0 のみ非零・κ は tag 0 のみ台(tag 1〜5・aux 8 は零)(vi) λ·ρ₂ は DERIVED(2117 規約 17)(vii) B 行列・旧 1385 行・P1 cache 由来 5,335 lift は二系統一致のみ。以上。
