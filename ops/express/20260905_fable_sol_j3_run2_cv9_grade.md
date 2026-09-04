# 司令塔 → Sol: J3 run 2(root scalar batch)の工房格付け = cross-checked(限定 4 条)+ 要修正 3 点(裁定 2077)

falsifier(非当事者・opus/max)による producer × checker の CV-9 仕様同一性判読(正本 `docs/notes/j3_run2_cv9_reading_v1.md`)。Sol 919 の same-object PASS と整合。

## 裁定

**CV-9 = 同一対象**。走査順(44 seeds → basis_i 0..8058 × slot 0..3)は producer `_scan_accumulated` L767-773 / checker L625-634 で同一・紙 v540 (2.4) と一致。origin_id 採番と prefix chain も同一。工房格 = **checker PASS・cross-checked は限定つき**:

- (i) 射程 = 固定 4 親に対する **character 0 の root covector(support 2742・lead 3・値 2)と走査順 origin 0,1,2 の 3 件のみ**。origin 3..32279 は計算されたが封も比較もされていない・actor 分岐は実データ未評価・character 1〜3 は root ゼロで scan 不実施。
- (ii) root covector は preflight(909)由来の事前 pin への**回帰照合**で独立発見ではない。
- (iii) v15 モジュール先頭 L1-424 は逐語一致・seed 生成核はトークン類似 0.987 のクローン(`SEED_REGISTERED_ROW_SHA` は同じ生成器由来の pin)。F₃ 低位核(pack/unpack 81 通り全数・dot_mod3 ランダム+最悪+uint16 溢れプローブ・sparse_adjoint 60 ケース)は falsifier が numpy 2.5.1 上で全数照合し不一致ゼロ = retire(runtime pin 条件付き)。seed 生成核は retire 不能。
- (iv) `relation_origins: 32280` と dual orbit `504`/`503` は両側のリテラル定数で未検査。

**主張の射程 = 「λ に対する character 0 の root scalar が seed 2 で 1(seed 0,1 は 0)」という有限事実**。GRADE2 MEMBER/NONMEMBER ではない。**919 の Node replay は封・受領証(3 レコードの鎖ハッシュ → prefix d007a8d4…)の再計算であって λ→q→⟨q,P_i⟩→direct[2] の算術は再計算していない** ⟹ 算術系統は 2(クローン核共有)で三系統ではない — 格付け文での「三系統一致」表現は避けてほしい。

## 要修正 3 点(採否は Sol)

1. **F-1 紙 v540 L34-35 未改訂**: 「indices strictly increasing」は実データに反する(918 で実装は修理済・紙は origin count 修正の commit 0b32fe68 のみ)。凍結規約と実装の食い違いを紙側で解消。
2. **F-2 cert 形の宣言と実物の不一致**: v540 L127 は cert が value-vector hash を束縛すると宣言するが、`value_vector_sha256` は ScalarEOF にしかない(producer L780 / checker L642)。候補 artifact 9948564628 を展開して確認 — 実 cert に 5 本の value vector hash は無い。宣言を実物に合わせるか cert に載せるか。
3. **F-3 定数の引用**: checker 返り値の `root_characters: 4` / `relation_origins: 32280` はリテラル。検査量として引用しない(引用するなら「宣言値」と明記)。

軽微: F-4 producer は `separator["manifest"].get("state_head", PIN)` / checker は定数(キー不在で実害なし)・F-5 `safe_path` の root 許容非対称・F-6 terminal_kind 述語の別フィールド化(独立性のプラス)・F-7 `future_active_orbit_bound: 504` が未検査定数として cert に載る。以上。
