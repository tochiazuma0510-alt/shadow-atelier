# Luna 委嘱 106g-BridgeB — affine 経路 A0 型/API スパイク

## 0. 目的と裁定境界

便 106g の Bridge B 内製案について、固定版 mathlib で既在 API を実際に型検査する最小の
**無公理 foundation spike** を作る。これは Bridge B、TB1、TB3、TB4、EXSEQ の証明ではない。
Sol の暫定裁定は「affine foundation は GO、Bridge B 全体の完成宣言は NO-GO」であり、本委嘱は
その A0 だけを実行する。

## 1. 入力と固定版

- branch: `sol/task106-math33-20260806` の親指定 head（LA 束を先に統合した場合はその head）。
- package: `lean-arith/`。
- `lake-manifest.json`: mathlib `v4.32.1`, exact rev
  `520045ab14e26149ee970e2e617ca04b09bde5d6`。依存版を更新しない。
- 使用候補:
  - `Mathlib.RingTheory.Etale.Finite`
  - `Mathlib.CategoryTheory.Galois.Basic`
  - `Mathlib.CategoryTheory.Galois.Topology`
  - 必要最小限の polynomial/localization import

## 2. 実装する A0

`lean-arith/LeanArith/BridgeBAffine.lean` に、少なくとも次を actual Lean types として置く。

1. 体 `k` に対する
   `A_U = k[t, t^{-1}, (t-1)^{-1}]` を
   `Localization.Away (X * (X - 1))` として定義する（同値な逐語型でもよい）。
2. 被覆圏の向きを
   `((CommAlgCat.FiniteEtale A_U)ᵒᵖ)` として定義する。`FiniteEtale A_U` 自体を被覆圏と
   取り違えない。
3. 幾何点 `A_U -> Ω`（`Ω` は separably closed field）を明示的な
   `[Field Ω] [IsSepClosed Ω] [Algebra A_U Ω]` 入力として、
   `CommAlgCat.FiniteEtale.fiber A_U Ω` を定義する。
4. この functor の自然自己同型群 `CategoryTheory.Aut F` を affine `piOne` の候補型として定義する。
5. 未証明の接続点を、証明済み instance のように偽装せず、型が通る **goal/obligation 型**として分離する:
   - `PreGaloisCategory ((FiniteEtale A_U)ᵒᵖ)`;
   - その instance の下での `PreGaloisCategory.FiberFunctor F`。

名前は Lean の衝突回避のため調整可。ただし上の数学的内容・圏の向き・入力を弱めない。

## 3. 禁止と停止条件

- `axiom` / `sorry` / `admit` / `native_decide` / `Lean.ofReduceBool` / `True` placeholder 禁止。
- `PreGaloisCategory` や `FiberFunctor` の instance を「既在」と仮定しない。固定版ソース検索では
  `FiniteEtale` 用 instance は未検出であり、A0 では goal を型付けするだけ。
- tangential base point、`piOne ~= Fhat2`、慣性元 `(x,y)`、TB3/TB4、EXSEQ の exactness を主張しない。
- mathlib や manifest/toolchain/workflow を変更しない。
- 型が一意に通らない箇所は別の弱い命題で代用せず、最小エラーと候補を報告する。

## 4. 検収と報告

- 独立 `%TEMP%` clone/worktree で作業し、credential、commit、push、dispatch は行わない。
- local cache が使える場合は targeted build のみ。最終判定は親が branch commit 後に GHA へ dispatch する。
- `rg` で固定版に `FiniteEtale` 用 `PreGaloisCategory` / `FiberFunctor` instance が無いことを
  対象ディレクトリ内で再確認する。
- `sol/luna_reply_106g_bridgeB.md` に path、変更一覧、build 結果、exact imports、
  何が definition まで閉じ何が obligation のままかを書く。
