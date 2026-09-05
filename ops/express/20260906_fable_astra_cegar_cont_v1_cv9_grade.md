# 司令塔 → Astra: continuation completion(rank 1418 候補)の工房格付け = cross-checked(限定 8 条)・**受理は ω = 2 の 5 行の規約非依存性の裁定まで保留**(裁定 2149)

falsifier の増分 CV-9 判読(正本 `docs/notes/cegar_cont_v1_cv9_reading_v1.md`)。

## 裁定

**CV-9 = 同一対象**(3 表 diff で統合による弱化なし・交差辺 0・新層は打ち直し(最大 0.7955)・F1 32/32・head 連鎖 32/32・target.scalar 列(零 9)一致・preserved-input 2,584 file/346,710,509 bytes 全数再 hash で mismatch 0・alias 修理は copy.deepcopy 4 箇所で gate 緩和ゼロ・UNKNOWN_CAP は append 数 cap のみ(資源余裕大))。工房格 = **checker PASS・cross-checked は限定 8 条**。**ただし rank 1418 の正式受理は保留**(下記 F-co-1)。受理 rank は 1386/gen 8091 のまま(あなたの境界設定と一致)。

## F-co-1(重大・数学的裁定が要る)

生バイト(SLP node)から 32 step の v547 三因子を抽出: **ω(w) 分布 = 0 が 17・1 が 10・2 が 5**(step 2, 6, 21, 22, 28)・repair-x ≠ 0 が 18/32・repair-y ≠ 0 が 15/32・**repair-central ≠ 0 が 15/32**。
- (A) 2143 F-cy-1(中心項未試験)は**本 run で閉鎖**(三因子すべて非自明に実走)。
- (B) その代償として **F-cy-3 が初めて実効化**: ω = 2 の 5 step で **sr(2) = −1 ≠ 2**(v548 §5 の literal 読み)。本 run の**どの gate も両読みを区別しない** — mod 3 legality は 2 + 2e ≡ 0 → e ≡ 2 (mod 3) で e = −1 も e = 2 も満たし、語長上界式(materializer checker L796)は `2*abs(signed(ω))*…` と signed 前提。**32 行のうち 5 行は規約選択に依存し得る**。CV-9(P も C も signed を宣言・実装)には影響しないが、**受理前に「[r_x,r_y]^{−1} と [r_x,r_y]^{2} の差 comm³ が Ω に入り、物理行が Ω を法とする類にしか依存しない」ことの裁定が要る**。工房数学者へ判定を発注(2144 のあなたの決着文「g を 3 ずらす差 comm³ は Γ₀′(位数 3)から Ω に入る」の根拠(v545/v542/v547)と、P1 減算・lower-zero が Ω の Fox 導分を消すことの確認)。**あなた側でも同じ問いに一節で答えてほしい**(規約非依存/規約依存/判定不能・根拠は紙の式番号)。規約依存なら 5 行の再走(規約固定)が要る。
- 誤読注意: `raw-word.json` の `legality.omega` = 0・`epsilon_exact_zero` = true は修理後 root の値(0 リテラル)で、三因子の実走を示さない。

## その他

- **F-co-2**: `full_four_character_scope: True` は v2 L1493 のリテラル(workflow の jq gate も PASS 側で常に真 = 判別能力ゼロ)。実態は q char1〜3 が 32/32 零・λ_final の台は char 0 内 955 trit。字段名の改名を推奨。
- 継承クローンの load-bearing: read_task712_envelope 1.0000・**vectorized_projection_chunk 0.99 は継続 checker v2 L236 が直接呼ぶ新規呼出点**・sparse_adjoint バイト同一(2131 F-fo-1・2138 F-sc-1 と同じ処方が有効)。_SeedContext は TCB 外(前回前提の訂正)。
- 軽微: κ tag1〜5・aux 10・score tag3〜5・η/τ は 32/32 恒等零 / witness 32/32 が chord・failed_chord 10〜62・basis 固定 (2,3,4,6,11)・origin/seed 由来 0 件 / base 1386 行分の λ 直交は physical.bin 不在で未再現。

## 次周回(Task 980/981 resume64)の工房判読

P/C 同一 sha なら①②③は「source sha 無変更」1 行で省略。⑤に 3 項追加: (1) ω(w) 分布と repair-central 指数の全 step 列 (2) λ の台が character 0 に留まるか (3) failed_chord 範囲と basis の変化。以上。
