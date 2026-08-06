# Luna 委嘱 111d — G2b 公理境界と次の最小 Bridge 義務

## 0. この便だけで分かる目的・終点

便111cで、same-universe の canonical cover category
`LeanArith.BridgeBAffine.CoverCategory.{u,u} k` に対する有限群 quotient field G2b は、
固定 Mathlib v4.32.1 に有限群固定部分代数の `Algebra.Etale` 閉性が無いため
`BLOCKED-MATHLIB` で停止した。司令塔裁定610・正規便111dにより、ここだけを専用公理へ
隔離して **verified-modulo-axioms** として閉じることが認可された。

この委嘱の終点は二つである。

1. `ShadowAxioms` に有限 étale 代数の有限群固定部分代数が étale であることを、
   正確な有限性・作用・基底仮定つきで一公理だけ登録し、実際の Mathlib field
   `HasColimitsOfShape (SingleObj G) (CoverCategory.{u,u} k)` を構成する。
2. 残る橋のうち固定 Mathlib で最も閉じやすい一件として、geometric fiber functor が
   終対象を保存する exact field
   `PreservesLimitsOfShape (Discrete PEmpty) (fiber (k := k) Ω)` を構成する。

2 の選定理由は、圏の終対象自体は G1 で既に閉じている一方、その fiber は
`AU k →ₐ[AU k] Ω` という一元集合なので、fixed Mathlib の `AlgHom` extensionality と
`FintypeCat` terminal API だけで閉じる見込みが、pullback 保存や G3
mono/direct-summand より高いからである。2 は狭義 verified 候補であり、1 の公理を
実質使用してはならない。

基線は `origin/master@a0c1d774763d904ee00f3bb6020266a7abdb42a8`。
shared worktree の無関係な dirty/untracked file は所有者が別である。repository file は
一切編集せず、候補は `%TEMP%` のみで反復し、返信に final blob 全文を省略なく返す。
Git/GitHub、commit/push/workflow dispatch、`GH_TOKEN` は親 broker の仕事であり非接触とする。

開始時に次の anchor を照合し、一つでも違えば編集・実装せず `STOP-DRIFT` を返す。

| anchor | SHA-256 |
|---|---|
| `lean-arith/LeanArith/BridgeBAffine.lean` | `4d8d1f1b743c80a12bbf7a16b6e6b976e45dcc10637dd15137990e8879d945aa` |
| `lean-arith/LeanArith/BridgeBAffineG1.lean` | `8650244f41e03dcb0615a8a7ca58dbfafe49d669868d22e6dab0340900d17168` |
| `lean-arith/LeanArith/BridgeBAffineG2FiniteCoproducts.lean` | `9391d3f5efc565bc7a82404f376417aa45ae4aedfee991828fa0ebaef536dc24` |
| `lean-arith/lakefile.toml` | `661314c3b7914df241de26e2e6b511c57e21bfa73283d003759eb41668d7f049` |
| `lean-arith/lean-toolchain` | `8e3538e0ab5f81a3ee04927d8838c8c674e0e112838b4b3ce87ec218143276af` |
| `.github/workflows/lean.yml` | `d61796aadad70af56957669667958ba56a209ef1b81e865cf820a7ead64cce23` |
| `docs/notes/lean_axiom_policy_v1.md` | `3fa19f10011775715a2eb395f6abb0f5ddbceca7f53bf896d02f545618287a3b` |
| `lean/AXIOMS.md` | `c6929cccce6279d22150748d7ac3f6711519f283d253736c0f735b59c0bf6fb8` |
| `papers/sga1-grothendieck-raynaud-arxiv0206203.pdf` | `8e64218d356456c534eebf996940f0f957e43b54f1a080241debe12cbaf60d3c` |

固定 Mathlib checkout は tag v4.32.1、commit
`520045ab14e26149ee970e2e617ca04b09bde5d6` である。

## 1. G2b 用の唯一の project axiom

新規 module は `lean-arith/LeanArith/ShadowAxioms.lean`。axiom は top-level namespace
`ShadowAxioms` に置く。許可する project axiom は一個だけで、概念的な最弱形は次である。

```lean
axiom fixedPointsSubalgebra_etale_of_finite
    (R B G : Type u)
    [CommRing R] [CommRing B] [Algebra R B] [IsNoetherianRing R]
    [Module.Finite R B] [Algebra.Etale R B]
    [Group G] [Finite G] [MulSemiringAction G B]
    [SMulCommClass G R B] :
    Algebra.Etale R (FixedPoints.subalgebra R B G)
```

実在 API に応じた binder 順・暗黙引数化・同値な universe 表現はよい。ただし次は必須。

- 一般 `Algebra.Etale` だけでなく `[Module.Finite R B]` を明示する。
- `G` は `[Group G] [Finite G]`、作用は実際の semiring automorphism action で、
  `R`-scalar と可換することを型に持たせる。
- 原典の局所 noetherian 仮定に対応する `[IsNoetherianRing R]` を保持する。
  G2b では `R := AU k` に特殊化し、既存 instance から供給する。
- `HasColimits...` そのもの、cocone、普遍性、`Module.Finite` は公理に含めない。
- axiom を global instance にせず、G2b の étale object 構成位置で明示的な local instance
  としてだけ使用する。

宣言直上の doc-comment は少なくとも次を逐語的に束縛する。

- Content: finite étale algebra の finite-group fixed subalgebra の étale 閉性。
- Source: SGA 1, Exposé V, Proposition 3.1（印字 p.96、PDF p.112）と affine quotient の
  Proposition 1.1 / Corollaire 1.8。Sol が 2026-08-06 に PDF page image を照合済み。
- Tier: T1（古典 SGA1）。司令塔裁定610 / 便111dで追加認可。
- Mathlib status: v4.32.1 / commit `520045...e5d6` で fixed-subalgebra の
  `Algebra.Etale` theorem/instance 不在。G2b-exact は将来の axiom 除去標的として OPEN。
- Scope: noetherian base + finite étale + finite group action のみ。

小さな type/sanity witness を一件置き、少なくとも `R := AU k` へ特殊化できることを
型検査する。可能なら trivial group/action の既知ケースを公理なしで別 theorem として
証明し、難しければ「公理の binder sanity であって真偽の独立証明ではない」と返信に明記する。

## 2. G2b exact target

新規 module は
`lean-arith/LeanArith/BridgeBAffineG2FiniteGroupQuotients.lean`。
`BridgeBAffineG2FiniteCoproducts` と `LeanArith.ShadowAxioms` を明示 import する。

public target は exact に次の強さを持つ。

```lean
noncomputable instance coverCategoryHasQuotientsByFiniteGroups
    (G : Type u) [Group G] [Finite G] :
    HasColimitsOfShape (SingleObj G) (CoverCategory.{u,u} k)
```

任意の `F : SingleObj G ⥤ CoverCategory.{u,u} k` について、反対圏の affine variance の下で
有限 étale algebra `B` に入る有限群作用を取り出し、fixed subalgebra を quotient cover とする。
次を Lean term が実際に保持しなければならない。

1. fixed subalgebra の `Module.Finite (AU k)` は既存 Mathlib だけで証明する。
2. `Algebra.Etale` にだけ §1 の公理を使用し、その use-site 直上に
   `AXIOM USE: ShadowAxioms...` コメントと除去標的を記す。
3. cocone の各 leg と compatibility を構成する。
4. 任意 cocone から fixed subalgebra への一意な factorization を構成する。
5. `HasColimit F` から `HasColimitsOfShape` を実 instance として与える。
6. generic witness で `colimit F`, `colimit.ι F`, `colimit.isColimit F` が同じ instance から
   synthesize されることを型検査する。

必要なら `CategoryTheory.Action.functorCategoryEquivalence`、opposite diagram API、または
manual `Cocone/IsColimit` を使ってよい。弱い proxy は不可。

FAIL:

- `HasColimitsOfShape` を引数・typeclass・別 axiom として受けて返す循環。
- `Nonempty` / `True` / 独自 record / 候補 object だけで exact field を代用。
- fixed algebra の有限性、cocone condition、factorization uniqueness のいずれかを公理化。
- `sorry`, `admit`, §1以外の `axiom`, `unsafe`, `implemented_by`。
- full `PreGaloisCategory`、G3、任意 universe、`FiberFunctor` 全体の先取り。

固定 Mathlib API では fixed points の categorical construction 自体が閉じず、§1の公理以外の
新しい数学が必要なら、弱い blob を残さず `STOP-G2b-SECOND-BLOCKER` とし、exact blocker を返す。

## 3. 続行一件 — fiber の終対象保存

新規 module は原則
`lean-arith/LeanArith/BridgeBAffineFiberTerminal.lean`。
G2b module を import してよいが、この module の主 instance/theorem は G2b axiomを実質使用せず、
`#print axioms` に `ShadowAxioms.*` が現れないこと。

variables は existing `BridgeBAffine.fiber` と同じ
`k : Type u [Field k]`, `Ω : Type w [Field Ω] [IsSepClosed Ω]
[Algebra (AU k) Ω]`。source category は same-universe `CoverCategory.{u,u} k` に限定する。

public target:

```lean
noncomputable instance fiberPreservesTerminalObjects :
  PreservesLimitsOfShape (Discrete PEmpty) (fiber (k := k) Ω)
```

実在 binder/universe に調整してよい。proof は、既存 G1 の terminal objectが affine algebra
`AU k` に対応し、その fiber `AU k →ₐ[AU k] Ω` が singleton であることを用いてよい。
generic terminal diagramについて `mapCone` が limit であること、または Mathlib の同値な
`PreservesLimit` constructorを実際に供給する。exact field が閉じたことを型検査する witness を置く。

この一件では次を宣言しない。

- full `PreGaloisCategory`（G3 が未閉鎖）。
- full `PreGaloisCategory.FiberFunctor`。
- pullback、finite coproduct、epi、finite-group quotient の保存、iso reflection。
- mono/direct-summand。

閉じなければ `BLOCKED-FIBER-TERMINAL` とし、同型の fail-closed inventory を返す。G2b が
先に STOP しても独立 probe は続ける。

## 4. axiom 台帳 patch

canonical registry `lean/AXIOMS.md` の末尾へ追加する完全な Markdown patch/blob を返す。
既存内容は一 byte も改変せず append-only とする。新 section は少なくとも次を含む。

- exact axiom name と正規化した Lean type（省略しない。type全文を載せれば digest は不要）。
- Tier T1、裁定610/便111d、SGA1 locator、PDF hash。
- Mathlib tag/commit と不在確認方法。
- actual use-site 一覧。
- main G2b declarations の exact sorted `#print axioms` set。
- G2b-exact の axiom-free replacement は OPEN、削除条件は同型 theorem/instance の Mathlib到着または自前形式化。
- fiber terminal theoremは当公理非依存。

## 5. 必須 Lean / axiom / byte gate

最終分割 blobを `%TEMP%` で再現可能な形にし、最低限次を返す。

1. `lake env lean LeanArith/ShadowAxioms.lean` 相当 exit 0。
2. G1, G2a, G2b, FiberTerminal の四 target の個別 exit 0。
3. `lake build LeanArith` 相当。資源上未完なら個別 target成功と未完理由を区別する。
4. `#print axioms` の逐語出力:
   - axiom sanity/witness。
   - G2b public instance と generic colimit witness。
   - FiberTerminal public instance と witness。
5. G2b exact axiom set は許容 core
   `{propext, Classical.choice, Quot.sound}` の部分集合と
   `{ShadowAxioms.fixedPointsSubalgebra_etale_of_finite}` の和だけ。
6. FiberTerminal exact axiom set は許容 core の部分集合だけ。
7. 全 candidate で `sorryAx`、§1以外の project axiom、
   `sorry|admit|unsafe|implemented_by` がゼロ。
8. BOM無し、strict UTF-8 round-trip、trailing whitespace 0、LF。
9. final fileごとの byte length と SHA-256。

ローカル成功は candidate。G2b は authoritative GHA success 後も
**verified-modulo-axioms** のみ。FiberTerminal はその public declaration 自体の
exact axiom setに project axiomがなく、clean GHA success後のみ狭義 verified 候補となる。

## 6. 非接触と返信形式

Lean-only。GAP、群探索、列挙、Python/Node数学検算、Web検索をしない。封印値、blind値、
`K^(5)`測定、PSL量、epsilon bits、曲線データに触れない。workflow file、既存 branch/run、
unrelated dirty/untracked、P1 T2/LA/LEを変更しない。

返信には次を順番どおり置く。

1. start/base/anchor照合、repository/Git/GitHub read-only申告。
2. `PASS-G2b-MODULO-AXIOMS` または STOP と、構成説明。
3. `PASS-FIBER-TERMINAL` または BLOCKED と、選定一件の結果。
4. final 3 Lean filesの全文と `lean/AXIOMS.md` append blob（省略なし）。
5. 全 command、exit code、`#print axioms`逐語出力。
6. byte length/hash、禁止語scan、非接触、未閉鎖一覧。

質問は blocker が発生した場合だけ一問に絞る。実装が終わるまで turn を閉じない。
