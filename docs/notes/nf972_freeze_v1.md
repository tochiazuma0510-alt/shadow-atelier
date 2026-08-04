# NF-972 凍結仕様 v1(canonical NF / source-map・IF-FIRST)

**状態**: frozen(裁定 434・2026-08-04)。**設計の出所 = Sol 便 100 P100-4.2(逐語基盤)**+司令塔の運用条項。目的 = 屋根 M = K⁽⁹⁾∩N_{S₄} の |GT(M)| = 972 の格を「基数のみ cross-checked」(裁定 412)から**集合一致**へ上げる唯一の道(W99-2.1 ③)。Lean verified にはならない。

## 1. 数学 interface(Sol P100-4.2 逐語基盤)

- 屋根 M = K⁽⁹⁾ ∩ N_{S₄}。自由群部分 **M_{F₂} = M ∩ F₂ = (K⁽⁹⁾∩F₂) ∩ (N_{S₄}∩F₂)**。
- marked quotient maps を固定: **q₉: F₂ → F₂/(K⁽⁹⁾∩F₂)**・**q₄: F₂ → F₂/(N_{S₄}∩F₂)**。
- 凍結 NF:
  **NF([m, f·M_{F₂}]) = (m₀, can₉(q₉(f)), can₄(q₄(f)))**, 0 ≤ m₀ < M_ord。
- **can₉ / can₄ は GAP の列挙 index や任意 word ではなく、固定した marked presentation 上の内容依存 serialization**:
  - dihedral 座標側(q₉ の像)= r^a s^ε の指数 tuple(a mod n・ε ∈ {0,1}・成分順固定)。
  - 置換像側(q₄ の像)= 固定 degree・固定生成元・one-line image。
  - CV-1/CV-2(合成順序・作用の側)を schema に含める(規約台帳 v1.6 準拠・cert の conventions_used 必須)。
- **完全性の紙上根拠: ker(q₉, q₄) = M_{F₂}** ⟹ 二射影の組は F₂/M_{F₂} の元を分離し、先頭の m₀ と合わせて marked roof shadow の元を分離する。

## 2. 二 source map(別実装係・schema のみ共有・normalizer helper 非共有)

- **source map A**: factor cert(K9.v1.json・S4.v2.json)から組み立てた fiber-product の各点を上の tuple へ写す。
- **source map B**: 屋根の直接悉皆で得た各 [m, f] を、**独立に評価した q₉, q₄** で同じ tuple へ写す(A の正規化コード・中間表現を import しない)。

## 3. 合格条件(全て機械判定・fail-closed)

1. 両 tuple 集合の**集合等号**・各 **972**・重複 **0**。
2. 射影像 = **108**(q₉ 側)/**54**(q₄ 側)・compatibility quotient 一致。
3. cert に conventions_used(v1_6)・出所 digest・DRIVER_DONE。

## 4. 分離 fixture(識別力の事前実証・DUM-G3 規律)

次の 3 変異が**必ず set inequality を起こす**ことを両実装で確認してから本走とする:
1. 非自己逆元の**向き反転**(f ↦ f⁻¹ 型)。
2. **片側 generator swap**(q₉ or q₄ の生成元対応の入替)。
3. **m の法の誤り**(M_ord の取り違え)。

## 5. 停止・格

- fixture が発火しない(識別力ゼロ)→ CALIBRATION_FAILED / INTEGRITY_STOP(期待値を弱めない)。
- 集合不等号 → 保存・即報(どちらが誤りかを裁定へ — 補正禁止)。
- 通過時の格 = **集合水準 cross-checked 候補**(CV-9 判読[falsifier]と Sol 検収を経て確定)。U-11(合成表)には伝播しない。

## 6. v1.1 追補(裁定 442・2026-08-04)— marking の pin(第 1 回突合の教訓)

**経緯**: 第 1 回突合(A vs B)は per-m 構造完全一致(12 値×81)にも関わらず交わり 9/972 — 原因は §1 の「固定した marked presentation」が**どの marking かを pin していなかった**仕様穴(CV-7「比較相手の未宣言」型・司令塔の非)。A は factor cert の座標系・B は自前構成の座標系で serialize しており、両者は点ラベル・D₉ 基底の付け替えで結ばれる(はず — 検証は辞書化後)。

**pin(v1.1 正本)**: canonical marking = **factor cert の座標系**とする。
- can₉ の座標 = **K9.v1.json の f_triple 欄の座標規約そのもの**(K9 cert の marked 生成元が定める D₉³ 基底・ブロック順)。
- can₄ の点ラベル = **S4.v2.json の witness 置換の点ラベルそのもの**(9 点・one-line)。
- 自前構成側(source map B 型)は **marked 生成元対応による辞書**(自構成の marked 生成元像 ↔ cert 側 marked 生成元像を結ぶ同型・置換側は RepresentativeAction 等で σ∈S₉ を機械決定・一意性も機械検査)を構築し、辞書経由で cert 座標に落として serialize する。辞書構築は罠 #3 遵守(marked factor map・部分群等号に依らない)。
- **辞書の自己検査(義務)**: 辞書適用後の q₉ 射影集合が K9 cert の f_triple 行集合と**逐語一致**・q₄ 射影集合が S4 cert の witness 集合と逐語一致すること(不一致なら辞書が誤り — INTEGRITY_STOP)。
