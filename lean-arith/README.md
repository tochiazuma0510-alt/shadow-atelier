# lean-arith/ — Mathlib 依存の数論層(Lean Phase 3)

設計書 `docs/lean/K3対応表_v0.md` §1.4・表 D(数論層)・§4.7–§4.8(β 一般補題)の実装先。
既存 `lean/`(plain Lean 4・Mathlib 非依存)とは**別パッケージ**であり、`lean/` の K⁵ キャンペーン線
のファイルには一切触れない。

## なぜ別パッケージか(8GB RAM 制約 — 恒久規律)

Mathlib は**ローカルで full build しない**。このパッケージは CI(`.github/workflows/lean-arith.yml`)
専用として設計されている。ローカルで検証したい場合は `lake exe cache get` でビルド済み oleans を
取得してから `lake build` する(Mathlib 自体のコンパイルは発生しない)。キャッシュ取得に失敗しても、
CI 側では成功する前提の構成なので支障はない。

## Lean / Mathlib のバージョン

`lean-toolchain` は `lean/lean-toolchain` と同じ `leanprover/lean4:v4.32.1` に固定し、
`lakefile.toml` の Mathlib 依存も**同じ Lean バージョンに対応するタグ `v4.32.1`** に固定している
(両パッケージが異なる Lean バージョンで分岐しないようにするため)。

## 信頼札(設計書 §0.2 準拠)

- **✔M**: Mathlib 上の通常証明。想定公理は `propext, Classical.choice, Quot.sound` まで
  (設計書 §8 検収基準 2)。
- 各ファイルの末尾に `#print axioms` を置き、実際の公理集合を CI ログに正直に記録する。

## 実装済み(このコミット時点・ローカルビルドで `#print axioms` まで確認済み)

| ファイル | 定理名 | 対応表の行 | 内容 | 備考 |
|---|---|---|---|---|
| `LeanArith/F37.lean` | `F37a_zmod_mul_bijective_iff_coprime` | **F37a**(F37 全体ではない) | 巡回群 `ZMod e` 上 `x ↦ r*x` が全単射 ⟺ `Nat.Coprime r e` | 便 42 Sol 監査(§F4.2/§F6.1)で「F37a のみ・F37b(roots-of-unity への typed instantiation)・F37c(ι・(7.5))は未実装」と確定。**verified 札は F37a に限る** |
| `LeanArith/M6pp.lean` | `M6pp_core_orderOf_pow`・`M6pp_core_zpowers_card` | **M6″-core**(M6″ 全体ではない) | `orderOf (g^r) = M / gcd(M,r)` と、その部分群版(`[Finite G]` 前提) | 便 42 Sol 監査(§F5/§F6.2)で「FAIL(核だけへの縮小不可)・着工済みの補題は M6″-core としてのみ登録」と確定 |
| `LeanArith/M1.lean` | `norm_obstruction` | **M1**(補題 NC・全体) | 一般形ノルム障害: `x^p=(a:K)` (K は数体) ⇒ `∃ n:ℤ, n^p = a^(finrank ℚ K)` | 便 42 Sol 監査(§F5)で **PASS**(statement・証明とも修理不要)。系(NC-1〜3・M3 等)は instantiate として別行 |

いずれも `#print axioms` は `[propext, Classical.choice, Quot.sound]`(Mathlib 層の想定範囲・
設計書 §8 検収基準 2 の上限内)。`sorry`・`native_decide`・`Lean.ofReduceBool` は使用していない。

**未実装(このコミットのスコープ外)**: F33・F34・F35・F36・F37b/F37c・M6″ 本体・M2–M10(M1 以外)・
F31 系・F26′ 等(設計書 §7.1 Phase 4–8)。

## 便 42・Sol Lean 設計監査の反映(sol/sol_reply_42_final.md §F4–F6)

司令塔経由で Sol の型レベル監査(F33–F37・表 D)が着工中に届いたため、本コミットの範囲
(F37・M6″-core・M1)についてのみ反映済み。要点:

- **F37**: Sol は設計表の一行を F37a(巡回群の初等命題)/F37b(roots-of-unity への typed
  instantiation)/F37c(ι の構成・(7.5))の三つに分割し、本ファイルが実装していたのは F37a のみ
  と確定した。**定理名を `F37_zmod_mul_bijective_iff_coprime` → `F37a_zmod_mul_bijective_iff_coprime`
  に改名**し、docstring に三分割と未実装部分(F37b/F37c)を明記した。`e=0` は `ZMod 0 ≃ ℤ` で
  巡回群でないという Sol の指摘も反映(statement 自体は e=0 込みの一般形のまま、「巡回群」と
  読めるのは e>0 のときだけという限定を明記)。
- **M6″-core**: Sol は着工済みの `orderOf(g^r)=M/gcd(M,r)` を「有用な補助補題だが M6″ 本体では
  ない」と判定(表 D 全体としては FAIL)。本ファイルは元々「鍵だけを実装」とスコープを明示して
  いたため statement の変更は不要だったが、Sol の判定を docstring に引用し、`M6″-core` という
  登録名を明記した(§F6.2 の確定条件どおり)。
- **M1**: Sol は PASS と判定し、修理事項なし。docstring に判定を追記したのみ。
- **F33–F36**(型レベル修正の詳細指定): 本コミットのスコープ外(未着手)。次コミット以降の
  実装者は `sol/sol_reply_42_final.md` §F4.1(共通の型)・§F4.2(F33/F34/F35/F36 の各行)を
  先に読み、`F0 = ker χT`・`ΓK := (χT.comp Ih).ker`・値域を絞った `IhK : ΓK →* F0`・
  corestriction `κe`・`ρ0.comp IhK = τ.comp κ`(ill-typed な制限記法を使わない)・F34 の
  `Ih.ker = κ.ker.map ΓK.subtype`・F35 の `∃! j` predicate、を型レベルで先に固定してから
  実装すること。

## API 偵察について(設計書 §5・§7.3 の方針)

`M1.lean` が使う `Algebra.norm_algebraMap` / `Algebra.isIntegral_norm` /
`IsIntegrallyClosed.isIntegral_iff` 等は当初「実在が本セッションでは確認できていない」
UNKNOWN 扱い(設計書【GAP-L1】)だったが、**本コミットでローカル `lake build`(`lake exe cache
get` でキャッシュ取得後)により実在を確認済み**(便 42 の監査より前に判明)。`F37.lean`・
`M6pp.lean` の API も同様にローカルビルドで実在確認済み。UNKNOWN は解消したため、
今後の対応表更新時にこの節を反映すること。

## commit / push の運用

このディレクトリの commit・push は司令塔が行う(実装担当は commit しない)。CI はコミット後に
GitHub Actions 上で走る構成であり、ローカルの `lake exe cache get` の成否は最終的な緑・赤の
判定を代替しない。
