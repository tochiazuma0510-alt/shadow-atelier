# Luna 委嘱 111 — Lean 次波 A0（T2 型契約 / ram2 / Bridge G2a）

## 0. この便だけで分かる目的・裁定

この委嘱は、P1 Lean 化の次波を三つの互いに独立な車線で開始するためのものです。

1. **T2 型契約**: 論文由来の型境界を、axiom import より前に Lean の型として固定する。
2. **T1_cyclotomic_ram2**: `4*n` 次円分体で 2 の分岐指数が 2 であることを Mathlib から証明する。
3. **Bridge G2a**: `CoverCategory` の有限余積だけを閉じる。

三車線は並行してよい。ただし T2 車線は **型契約の候補を Sol に返す所で STOP** する。T2 axiom の追加、`ShadowAxioms` への import、LA/LE 下流の証明着手は本便の権限外である。

基線は `master@1f0b14af0d9a68561bb9fc3eedfa493dd0580adf`。開始時に基線との差を記録し、下記 anchor の内容 hash が違えば実装せず drift を報告する。

| anchor | SHA-256 |
|---|---|
| `lean/P1/ShadowAxioms.lean` | `d02949b306db28e251f93ab18983cf7245a6e38b2498e253c149d98e2419eff0` |
| `lean/P1/BlockA.lean` | `1004d829112ce6767b7cd9fc392a91445e5ef19dcc4ffa71318b10cd5409354b` |
| `lean/P1/BlockE.lean` | `d7cb27e4aecf51501805b48eb900fb27d181897fecdda03c950edac0727dd241` |
| `lean-arith/LeanArith/BridgeBAffineG1.lean` | `8650244f41e03dcb0615a8a7ca58dbfafe49d669868d22e6dab0340900d17168` |
| `docs/notes/lean_axiom_policy_v1.md` | `3fa19f10011775715a2eb395f6abb0f5ddbceca7f53bf896d02f545618287a3b` |

既存 worktree の無関係な dirty file は利用・整形・削除しない。commit / push / workflow dispatch は親 broker の仕事であり、本委嘱ではしない。

## 1. 共通制約

- **Lean-only**。GAP、探索、列挙、Python/Node による数学検算、Web 検索をしない。
- 封印値・blind 戦役・`K^(5)` の測定値・PSL 量・epsilon bits には触れない。
- `sorry`、`admit`、新規 `axiom`、`unsafe`、証明を隠す `implemented_by` を禁止する。
- 「verified」は Lean が通った対象にだけ用いる。設計文書・型契約だけなら `typed candidate` と呼ぶ。
- Mathlib の補題名はローカル source / `#check` / Lean server search で確認する。記憶だけで書かない。
- 既存の allowed core axioms `{propext, Classical.choice, Quot.sound}` を越える project axiom が `#print axioms` に出たら FAIL。
- 変更可能候補は次だけ。不要なファイルは作らない。
  - `lean/P1/T2TypeContract.lean`（車線 T2。条件を満たせないなら作らず blocker）
  - `lean-arith/LeanArith/CyclotomicRam2.lean`（車線 ram2）
  - `lean-arith/LeanArith/BridgeBAffineG2FiniteCoproducts.lean`（車線 G2a）
  - 各 package の最小 import/manifest 変更（ram2/G2a の GHA 対象化に本当に必要な場合だけ。T2 は root import 禁止）
  - `sol/luna_reply_111_lean.md`
- 一車線が STOP しても、独立な他車線は続けてよい。返信では車線別に PASS / FAIL / BLOCKED を付ける。

## 2. 車線 T2 — axiom 前の厳密な型契約

### 2.1 正典 locator

ページ画像で再確認する対象は次の三つだけである。

- `papers/2401.06870-gt-shadows-gentle-version.pdf`、印字 p.18、Theorem 3.10 と式 (3.53):
  `GTSh(N2,N1)` と `GTSh(N3,N2)` の合成が `GTSh(N3,N1)` に入る。
- `papers/2405.11725-nonabelian-quotients-gt-elementary.pdf`、印字 p.18、Theorem 4.3 と式 (4.12):
  `GT(K^(n))` の明示記述、および `K^(n)` の isolated 性。
- 同 2405 論文、印字 p.4、式 (1.5)、ならびに (1.7), (1.9), (1.11), (1.13):
  大域 Ihara 準同型、有限射影、virtual cyclotomic character の可換性。

テキスト抽出は検索補助に限る。式の採否は画像を正本とする。Theorem 3.10 の印字中に一箇所ある `GT(N3,N2)` は、前後の object index と結論から `GTSh(N3,N2)` と読むべき誤植候補として、勝手に直さず返信に明記する。

### 2.2 固定すべき型境界

少なくとも次を、Lean signature と依存図で一意化する。

1. **object index**
   - `GT N` と `GTSh K N` を区別する。
   - `GTSh N₂ N₁` は source/target の二添字を保持し、単なる endomorphism 型へ潰さない。
   - `K^(n)` の object と、一般の `N` を混同しない。
2. **合成**
   - 型は概念的に
     `GTSh N₂ N₁ → GTSh N₃ N₂ → GTSh N₃ N₁`。
   - 第一座標は `N₂_ord = N₁_ord` 等の由来を持つ transport を通す。
   - 第二座標は第一 morphism が誘導する `F₂` 商の写像/同型を通す。異なる quotient の元を definitional equality で同一視しない。
   - (3.53) の `f₁ * E_{m₁,f₁}(f₂)` がこの transport 後に型を持つことを示す。
3. **Theorem 4.3**
   - `GT(K^(n))` そのものと、その明示座標集合が同値/同型である statement を分ける。
   - isolated 性はさらに別 statement とする。
   - `GT(K^(n))` を明示座標集合の `abbrev` と定義して定理を反射律にすることを禁止する。
   - `4 ∣ n` と `4 ∤ n` の分岐、`K_ord = lcm(n,2)`、`ord(r^2)`、`kappa` の型を落とさない。
4. **Ihara**
   - 大域 `Ih : G_Q →* GT_hat`（さらに `GT_hat_gen` への包含）と、有限 `Ih_N := PR_N ∘ Ih` を区別する。
   - 任意の `N` について `Ih_N` を無条件に group hom としない。有限 group hom が必要なら isolated 条件を引数にする。
   - Block E が必要とする最弱の T2 境界は、完全な `f_g` データではなく
     `chiTilde_(2*nu) ∘ Ih_N = cyclotomicCharacter mod (2*nu)`
     という有限 compatibility である。

### 2.3 実装の正直さ

現行 `Core.lean` には paper-faithful な `B3`, `F2`, `NFI`, target-dependent pair quotient, `GT`, `GTSh` が揃っていない可能性が高い。したがって次の二択だけを許す。

- **TYPED-CANDIDATE**: 実在する基礎定義から上記境界を忠実に型付けし、`T2TypeContract.lean` が単独で通る。
- **BLOCKED-FOUNDATION**: 不足する最小 primitive を、名前・期待型・正典 locator・なぜ既存型で代用不能か、の四点で有限列挙し、Lean ファイルは作らないか、既存定義だけを参照する非偽装の最小草案に留める。

以下は FAIL とする。

- theorem 内容を field に持つ汎用 record を作り、それを「GT object」と呼ぶ。
- `Prop` parameter や typeclass parameter に T2 の結論を隠す。
- quotient 同一視を無名の `Eq.rec` / `cast` で押し通す。
- `GTKn := explicitRHS` と置いて Theorem 4.3 を `Iff.rfl` にする。
- 大域 Ihara と有限 projection を一つの無添字定数に潰す。
- `ShadowAxioms.lean`、`P1.lean`、package root からこの草案を import する。

返信には declaration inventory を置き、各 declaration を `existing definition / new definition / proposed T2 axiom / theorem to prove` のどれかに分類する。**本便では `proposed T2 axiom` は署名提案までで、Lean declaration にしない。**

### 2.4 型の負試験

コンパイル可能な草案を作れた場合、少なくとも次を `example` またはコメント付き `#check` で記録する。

- 中間 object が一致しない二 morphism は合成できない。
- 異なる order / `F2` quotient の座標は transport 無しに掛けられない。
- isolated 証拠無しの一般 `N` から finite `MonoidHom` は得られない。
- `n = 3` と `4 ∣ n` 側の一例がそれぞれ同じ statement family に入る。

型契約を返したら **STOP-T2**。Sol の再監査前に T2 import、LA7、LA9、LE1(b)–LE4 へ進まない。

## 3. 車線 ram2 — `T1_cyclotomic_ram2`

### 3.1 数学的 target

`n` が奇数、`K/Q` が `4*n` 次根を含む円分拡大であるとき、2 の ramification index が 2 であることを Mathlib だけから証明する。まず global ideal statement を閉じる。

概念的な形:

```lean
theorem cyclotomic_ramificationIdxIn_two
    (n : ℕ) (hn : Odd n)
    (K : Type*) [Field K] [NumberField K]
    [IsCyclotomicExtension {4 * n} ℚ K] :
    (Ideal.span {2} : Ideal ℤ).ramificationIdxIn (𝓞 K) = 2 := ...
```

実在 API に合わせた binder/notation の調整はよいが、結論を弱めない。必要ならその後、`P` が 2 の上にある素イデアルなら個別の ramification index も 2、という corollary を付ける。

### 3.2 使用予定の Mathlib 錨

- `Mathlib/NumberTheory/NumberField/Cyclotomic/Ideal.lean` の
  `IsCyclotomicExtension.Rat.ramificationIdxIn_eq`。
- `Mathlib/NumberTheory/NumberField/RamificationInertia/Galois.lean` の
  `ramificationIdxIn_eq_ramificationIdx`（個別素イデアル corollary を作る場合）。

`4*n = 2^(1+1)*n` と `¬ 2 ∣ n` を `Odd n` から供給する。新規 T1 axiom は作らない。この Mathlib proof が通れば、旧ラベル `T1_cyclotomic_ram2` は「T1 を追加」ではなく「T1 候補を定理へ降ろして解消」と報告する。

### 3.3 受入条件

- `lake env lean LeanArith/CyclotomicRam2.lean` 相当が成功。
- `#print axioms` の対象 theorem と corollary を列挙し、project axiom 0。
- `n = 1` または `n = 3` の少なくとも一つの型付き sanity instance。
- theorem locator、使用 lemma、build command、exit code を返信に記録。
- **closed の札は親 broker の GHA run id と全 job success が付いてから**。ローカル成功だけなら `Lean candidate`。

## 4. 車線 Bridge G2a — 有限余積だけ

### 4.1 正確な残件数

Mathlib の `PreGaloisCategory` は五 field であり、G1 は same-universe の `HasTerminal` と `HasPullbacks` を閉じた。従って PreGalois の未閉鎖 field は **3 個**:

1. `HasFiniteCoproducts`
2. finite group action quotient colimits
3. mono が direct summand 上の iso を誘導する条件

「残り 4」は誤り。arbitrary-universe (`u != v`) の G1 debt は別勘定で、field 数に足さない。また `FiberFunctor` は単一 obligation ではなく六 field なので、本便では触れない。

### 4.2 本便の target

same-universe の既存 canonical category
`CoverCategory.{u,u} k`
について、public instance として `HasFiniteCoproducts` を構成する。既存 `BridgeBAffineG1.lean` の対象・morphism・equivalence をそのまま使う。

受入条件:

- target は theorem-shaped proxy でなく、Mathlib が実際に探索できる `HasFiniteCoproducts` instance。
- finite coproduct の object、injection、universal property が同じ instance から出る。
- same-universe 限定をファイル名・docstring・返信に明記。
- full `PreGaloisCategory` instance、finite-group quotient、direct-summand field、`FiberFunctor` は宣言しない。
- `lake env lean LeanArith/BridgeBAffineG2FiniteCoproducts.lean` 相当、関連する既存 G1 target、package build が成功。
- public theorem/instance の `#print axioms` を全列挙し、project axiom 0。
- API が canonical instance を作れず弱い proxy しか出せないなら、proxy を commit せず `STOP-G2a` として blocker を返す。

## 5. この便の後にのみ許される順序（本便では実装しない）

依存順は次で固定する。

1. Sol が T2 型契約を再監査。
2. 批准された署名だけを `ShadowAxioms` に最弱 T2 として import。
3. Block A は **LA6 の simply-transitive theorem** を先に閉じ、LA7 を閉じる。LA9 の前に LA8 の full automorphism extension / faithfulness も閉じる。現行 LA6 は definition のみ、LA8 は generator calculation のみなので、LA7 から LA9 へ直行しない。
4. Block E は、typed composition、有限 Ih compatibility、円分指標全射、abstract split/equivariance を順に閉じる。(3.49) 自体は既に formal theorem であり T2 axiom にしない。
5. Bridge は G2a finite coproducts → finite group quotients → mono/direct-summand → full `PreGaloisCategory` の順。一 field 一便を原則とする。
6. その後に `FiberFunctor` の六 field を分割して扱う。

## 6. 返信の必須形式

`sol/luna_reply_111_lean.md` に次を置く。

1. 開始 commit、anchor hash 照合、変更ファイル一覧。
2. T2 / ram2 / G2a ごとの PASS・FAIL・BLOCKED。
3. T2 declaration inventory、型依存図、負試験、STOP-T2 の遵守。
4. 各 Lean command と exit code、`#print axioms` の逐語結果。
5. `git diff --check` と `git status --short`。
6. GHA は親が行うため、run id が無い段階では「未実施」と明記。推測の run id を書かない。
7. 未閉鎖事項を、T2 import / LA6–9 / LE / PreGalois remaining / FiberFunctor に分けて列挙。

数学的主張を狭める必要が出た場合は、弱い代用品を作らず STOP し、必要な追加裁定を一問に絞って返す。
