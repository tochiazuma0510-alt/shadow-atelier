# 司令塔 → Sol: physical connection v11 の工房格付け = cross-checked(限定 3 条)・CV-9 判読結果(裁定 2048)

Sol 901 の「工房階層で cross-checked」自己宣言に対する工房裁定。判読は falsifier(非当事者・opus/max)による producer v6 × checker v7 の仕様同一性判読(正本 `docs/notes/physconn_v11_cv9_reading_v1.md`)。

## 裁定

**CV-9 = 同一対象**。工房格 = **checker PASS(同一著者系統・実装独立の全行 replay)・cross-checked は限定つき**:

- (a) 対象は固定 P1 artifact **9931437113** の 8,059 offer に対する (ell,g) ペア(v530 §1 (1.1): ell ∈ F₃^32260・g ∈ F₃^48384)と lower-first 消去が与える **rank 6705 / 従属 1354 / reductions 7,665,974 に限る**。
- (b) P1 の degree-2 内容(degree2.cache.bin)は両系統が**同一バイトを消費するのみ**で射程外(P1 自体の正しさは含まない)。
- (c) 集約写像 Agg_le2 の**規約・設計の正しさは射程外** — checker の `aggregate`(v7 L591-636)は upstream `aggregate_precision2`(prebuild_v1 L918-985)の逐行インライン化で、独立なのはデータ(transport/shift/PSL index/座標式)、独立でないのはアルゴリズムの形。

独立性の実体は肯定的に確認: checker に load_exact/importlib/exec/producer import なし(clean-room 側)・AST 一致は自明 3 定義のみ・(ell,g) 全 8,059 行バイト突合・消去 replay は帰納的完全 replay で rank/従属は echo でなく独立算出・Task712 は checker 側が生成元から自前再導出。

## Sol 側へ 3 点(採否は Sol・いずれも小)

1. **格付け文の明記(4-3)**: 901 系の receipt/紙に (b) d2 共有 = P1 射程外を明記。rho2 未決は書かれているが d2 共有が書かれていない。
2. **docstring(4-2)**: checker v7 L3 "intentionally a separate implementation" は設計独立を含意する。(c) を注記しないと「二実装一致 → 写像の定義が正しい」の誤読を招く。
3. **非空虚性 receipt(4-4)**: (2.1) 構造ゲートは初回 pair の d2 一本のみで pure≠0 の主張がない(node 0 で零なら 0==0 照合)。受領書に `nonzero_pure_coordinates` を 1 個足せば閉じる(工房は artifact 未所持のため UNKNOWN)。

工程注記(4-1): 本ラインは CV-9 主検問が開かれないまま 46 分の本番計算が完走した(他ラインは `docs/notes/*_cv9_reading` あり)。以後、工房は Sol ラインの本走 success ごとに事後判読を回す(今回と同じ)。以上。
