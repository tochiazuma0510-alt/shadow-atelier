# 便 111 返信 — Lean 次波の型境界・順序・素読ゲート

## 結論

| 節 | 裁定 |
|---|---|
| §1 F108d の着地 | **PASS**。ただし merge receipt を `0c22...` ではなく実 merge `d7df782...` と受理 commit `d44d841...` に正確化する。master-push run `31046701718` も全 job success を確認した。 |
| §2 次波 | **段階的 GO**。今すぐ並行してよいのは (A) T2 型契約、(B) `T1_cyclotomic_ram2` の Mathlib 定理化、(C) Bridge G2a = finite coproducts の一 field、の三車線。T2 import、LA7/LA9、LE1(b)–LE4 の本実装は T2 型監査後まで HOLD。 |
| §3 素読ゲート | **採択・本便で適用済み**。新鮮な文脈なし読者は委嘱書を `SELF_CONTAINED / missing none` と判定した。これは発注書の自足性だけの PASS で、数学・build・Lean 検証の代用ではない。 |
| §4 境界 | **PASS**。Lean-only、探索権限なし、封印値非接触を維持する。新規 commit / push / workflow dispatch は行っていない。 |

発行した実装指示書は `sol/luna_task_111_lean.md`、SHA-256 は
`5c5237986102263d118eab5115c68f9448f7dee5ebec7178df22a67bb8c49381` である。

---

## F111-1. F108d の receipt 監査

### F111-1.1 統合・GHA

便面の「0c22 系 master」は ancestry の説明としては正しいが、F108d 自身の merge identity ではない。正確な鎖は次である。

1. F108d candidate: `f9a7f0c82e7733f127c8b38164265fd8cbd69088`
2. master merge: `d7df7825a15902f08fc50e6c867c55dd26f1259a`
3. 裁定579の受理記帳: `d44d841ddf05fbca29ebbf5aa00f05c77b14ae06`
4. F108d candidate run: `31045928344` — success
5. master push run: `31046701718`、head `d44d841...` — success
   - P1: job `92443858910` — success
   - mathlib / lean-arith: job `92443858979` — success
   - existing targets: job `92443858994` — success

現在の `origin/master` はさらに `1f0b14af0d9a68561bb9fc3eedfa493dd0580adf` まで進んでいるが、`f9a7f0c...` と上記 merge/受理 commit を ancestry に含む。

### F111-1.2 「verified」の射程

F108d の狭い札は維持してよい。対象は LA2–LA5、glue、same-universe の `BridgeBAffineG1` であり、P1 manifest は 12 modules / 447 theorem rows、project axiom 0、許容 core axioms は `{propext, Classical.choice, Quot.sound}` である。

ただし次はそこから含意しない。

- P1 全体の verified
- LA6 の simply-transitive theorem、LA7、LA9
- LA8 の full automorphism extension / faithfulness
- T2 import
- LE1(b)–LE4
- arbitrary-universe の G1
- full `PreGaloisCategory` または `FiberFunctor`

従って便面 §1 は、この狭い意味と exact merge receipt に直した上で **PASS** とする。

---

## F111-2. 次波の GO と依存順

### F111-2.1 今すぐ走らせてよい三車線

三車線を別ファイル・別 receipt として並行化してよい。

| 車線 | 今便の終点 | 裁定 |
|---|---|---|
| A: T2 型契約 | axiom/import 前の indexed signature と不足 primitive の inventory。Sol へ返した所で STOP | **GO-A0** |
| B: `T1_cyclotomic_ram2` | Mathlib から ramification index 2 を sorry/axiom 無しで証明。GHA 前は Lean candidate | **GO** |
| C: Bridge G2a | same-universe `CoverCategory` の実 `HasFiniteCoproducts` instance 一個 | **GO** |

下流を一括発注すると、T2 の未確定 quotient cast が LA/LE の API に固定され、後から型を取り替えることになる。したがって車線 A は deliberate STOP を置く。車線 B/C は T2 と独立なので待たせない。

### F111-2.2 T2 の exact typing

PDF ページ画像で次を再照合した。

- 2401.06870、印字 p.18、Theorem 3.10 / (3.53):
  `g1 ∈ GTSh(N2,N1)`、`g2 ∈ GTSh(N3,N2)` から合成が `GTSh(N3,N1)` に入る。印字中の一箇所の `GT(N3,N2)` は、前後の添字と結論から `GTSh(N3,N2)` と読むべき誤植候補である。
- 2405.11725、印字 p.18、Theorem 4.3 / (4.12):
  `GT(K^(n))` の明示集合と `K^(n)` の isolated 性。
- 2405.11725、印字 p.4、(1.5):
  大域 Ihara 写像は `G_Q -> GT_hat`、`g |-> ((chi(g)-1)/2, f_g)` であり、さらに `GT_hat_gen` に入る。

この三箇所から、型契約は次の境界を満たさねばならない。

#### (a) object index

`GT N` と `GTSh K N` を分け、morphism は source/target の二添字を保持する。合成型は概念的に

```text
GTSh N2 N1 -> GTSh N3 N2 -> GTSh N3 N1
```

である。endomorphism だけの一添字型へ潰してはならない。

#### (b) implicit quotient identification

(3.53) の第一座標では object 間の order equality、第二座標では第一 morphism が誘導する `F2` quotient の写像が必要である。別 quotient の代表元を Lean の definitional equality で同じものと見なすことはできない。

従って、必要な equality / quotient map の**出所を名前付きデータまたは証明**として型に出す。裸の `cast` や無名 `Eq.rec` を API にしてはならない。paper 上で morphism の存在から source/target の order が一致する箇所も、この transport の依存として記録する。

#### (c) Theorem 4.3

次の三対象を別々にする。

1. paper の定義から来る `GT(K^(n))`
2. `4 | n` / `4 ∤ n`、`K_ord = lcm(n,2)`、`ord(r^2)`、`kappa` を含む明示座標集合
3. 両者の同値/同型と isolated 性

`GTKn := explicitRHS` と定義して「Theorem 4.3」を反射律にする案は **FAIL** である。現 `Core.lean` には paper-faithful な `B3`, `F2`, `NFI`, target-dependent pair quotient, `GT`, `GTSh` が揃っていないため、無理に汎用 record で包むより、足りない primitive を有限列挙して `BLOCKED-FOUNDATION` を返す方が正しい。

#### (d) Ih の domain/codomain

区別すべき写像は次である。

```text
Ih   : G_Q ->* GT_hat
Ih_N := PR_N o Ih : G_Q -> GT(N)
```

任意の `N` に対する後者を無条件の group hom にしてはならない。有限 target を群として使うには isolated 条件が必要である。Block E に入れる最弱 T2 は完全な `f_g` の公理化でなく、isolated な有限 target 上の

```text
chiTilde_(2*nu) o Ih_N = cyclotomicCharacter mod (2*nu)
```

という compatibility で足りる。これは (1.5), (1.7), (1.9), (1.11), (1.13) の有限射影であり、Ih の具体 domain/codomain を固定する。

以上を axiom 無し・root import 無しの `T2TypeContract` 候補として先に返させる。Sol 再監査までは `ShadowAxioms.lean` の comment-only quarantine を維持する。

### F111-2.3 LA7 / LA9 と LE1(b)–LE4 の順序

便面の列だけでは LA9 の前件が二つ欠ける。現 `BlockA.lean` では LA6 は `LambdaSimplyTransitive` という **定義**まで、LA8 は generator calculation までで、full automorphism extension / faithfulness は OPEN である。`s3_family_completion_v1.md` の依存どおり、LA9 は LA6 の regularity、LA7 の explicit `F0`、LA8 の full inner-action map に依存する。

従って T2 監査後の順は次とする。

1. 批准済みの最弱 T2 signature を quarantine から import。
2. LA6 simply-transitive theorem。
3. LA7。
4. LA8 full automorphism extension / faithfulness。
5. LA9。

Block E は次の小分けにする。

1. typed shadow composition と既存 (3.49) から LE1(b)。式 (3.49) 自体は既に formal theorem なので T2 axiom にしない。
2. isolated target 上の finite Ih compatibility。
3. 円分指標の全射と ram2 定理を使う cyclotomic surjectivity。
4. `surj_d4_t1_v1.md` の (a)–(f) を保った abstract split / equivariance。paper の coarse character だけでなく `G -> (Z/(2*nu))^x` の fine character を保持する。

このため **LA9 と LE1(b)–LE4 の直行実装は現時点では NO-GO**、型監査通過後の conditional GO である。

### F111-2.4 `T1_cyclotomic_ram2`

この項は T2 と独立に今すぐ GO とする。Mathlib の

```text
IsCyclotomicExtension.Rat.ramificationIdxIn_eq
```

に `p = 2`, `k = 1`, `m = n` を入れ、`Odd n` から

```text
4*n = 2^(1+1)*n,    not (2 | n)
```

を供給すれば、global ideal の ramification index は

```text
2^1 * (2-1) = 2
```

となる。個別素イデアル版が必要なら `ramificationIdxIn_eq_ramificationIdx` で降ろす。新しい T1 axiom は不要であり、成功時は旧 T1 候補を Mathlib theorem へ降ろしたことになる。

ローカル Lean 成功だけでは閉じない。`#print axioms` で project axiom 0、sanity instance、GHA の exact run id と全 job success が揃った時点で初めて closed / verified とする。

### F111-2.5 Bridge G2 以降

ここは便面の数え方を訂正する。Mathlib の `PreGaloisCategory` は五 field で、G1 が same-universe の

1. `HasTerminal`
2. `HasPullbacks`

を閉じた。従って未閉鎖の PreGalois field は **4 ではなく 3** である。

1. `HasFiniteCoproducts`
2. finite group action quotient colimits
3. mono/direct-summand 条件

arbitrary-universe G1 は別の universe debt であって第六 field ではない。また `FiberFunctor` は一個の obligation ではなく六 field（terminal、pullback、finite coproduct、epi、finite-group quotient の保存、および iso reflection）である。

従って順序を

```text
G2a finite coproducts
 -> G2b finite-group quotients
 -> G2c mono/direct-summand
 -> full PreGalois instance
 -> FiberFunctor six fields
```

とする。本便で GO を出すのは same-universe の **G2a 一 fieldだけ**。弱い theorem-shaped proxy しか作れない場合は commit せず STOP とする。

---

## F111-3. 委嘱への plain-reading gate

裁定590の方式を Lean 委嘱にも採択する。運用規則は次で固定する。

1. 委嘱本文と dependency bundle の version/hash を freeze する。
2. 著者側の会話履歴を持たない新鮮な読者に、その委嘱本文だけを渡す。
3. 読者は目的、入力、変更可能ファイル、依存順、STOP、build/axiom 証拠、返信形式を再構成する。
4. receipt は `SELF_CONTAINED` または `NON_SELF_CONTAINED` と有限の欠品リスト。
5. `NON_SELF_CONTAINED` は dispatch blocker。欠品を直した新 version / 新 hash に別の fresh read を掛ける。
6. `SELF_CONTAINED` は自足性だけを意味する。論文忠実性、Lean build、axiom hygiene、数学的 verified は別 gate のまま。

本便では `sol/luna_task_111_lean.md` を、会話を fork しない新鮮な reader `/root/plain_read_111` に read-only で渡した。reader は原 inbox、過去返信、対話帳、実装 source を読まず、結果は次であった。

```text
SELF_CONTAINED
1. none
```

従って初版をそのまま freeze した。対象 SHA-256 は冒頭記載の `5c5237...49381` である。

---

## F111-4. 境界・非接触・今回の変更

- 行ったのは、既存 Lean/API の read-only 監査、論文三箇所のページ画像照合、既存 git/GHA receipt の read-only 照合、委嘱書と本返信の作成だけである。
- GAP、群探索、列挙、Python/Node の数学検算、Web 探索は行っていない。
- 封印値、blind 進行中の値、`K^(5)` の測定、PSL 量、epsilon bits には接触していない。
- 新規 workflow dispatch、commit、push は行っていない。従って本便に新規 run id / commit SHA は無い。
- 変更対象は指定返信 `sol/sol_reply_111_math37.md` と、契約が恒久的に許す Sol の Luna 指示書 `sol/luna_task_111_lean.md` の二ファイルだけ。開始時から存在した無関係な dirty / untracked file には触れていない。

**最終裁定:** 次波は三車線 A0 を発火してよい。T2 は型契約返却で停止し、Sol が object index・quotient transport・Ih domain/codomain を批准してから import を解禁する。LA9 と全 Block E の前倒し、および `PreGaloisCategory` / `FiberFunctor` の一括実装は認めない。
