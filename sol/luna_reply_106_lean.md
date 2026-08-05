# Luna 返信 106-Lean — F105-6.4 親子実装第 1 束

## 0. 総括

**実装束判定: 条件付き DONE（local targeted-build candidate）**。

指定順（axiom/checker hygiene → Block H → Block A → Block E）で実装した。P1 の全 target は
`lake build P1` で exit 0、axiom gate は
`P1_AXIOM_AUDIT_PASS|modules=8|theorems=180|manifest=P1/AXIOMS.manifest.json` を出した。
これは local candidate であり、paper fidelity/PASS と GHA の acceptance は Sol/工房 gate に残す。

未閉鎖は、(i) Lambda-REG の指数・normalizer 仮説と証明、(ii) LA-2〜LA-5・LA-7・LA-9、
(iii) SURJ-Split の T2/Mathlib/副有限群部分、(iv) exact T2 statement の PDF 再照合・Sol 承認である。
これらを完成扱いも file-level grade もしていない。Bridge B には着手していない。

## 1. 要求 8 項の検収

| # | 状態 | 納品 |
|---:|---|---|
| 1 | **DONE** | `P1/AxiomCheck.lean` を全量 generator/fail-closed gate に変更。現在の全 8 source module（`ShadowAxioms` を含む）と 180 theorem declaration を列挙し、exact sorted axiom set・metadata-free type digest を manifest 化。全 P1-owned declaration も走査し、未使用 project axiom・def 内 `sorryAx` も fail する。 |
| 2 | **DONE** | 四つの bare T2 `Prop` を削除し、`ShadowAxioms.lean` を comment-only quarantine にした。二つの `: True` は消し、cardinality は実全単射、Lambda は real type/real proposition に置換。Lambda の proof は明示 OPEN。 |
| 3 | **DONE** | Block H に TORS-U の abstract core、explicit `Fin M` unit classification、両者の typed adapter を実装。character fitting は使っていない。 |
| 4 | **DONE（指定 foundation 範囲）** | 実 subtype `Gn n`、closure/group laws、`Xg : Gn n`、cardinality witness、real Lambda type/statement を実装。`xpowGn_val` を介して `Gn_ord_X` の結論を実 subtype 上にした。 |
| 5 | **DONE（算術核）** | `chiTilde_welldefined`、`chiTilde_isUnit`、(3.49) の Int identity と mod consequence を閉じ、inventory に入れた。残る SURJ-Split は OPEN。 |
| 6 | **DONE（表案のみ）** | §5 の T2 一枚表案。コード宣言は追加していない。 |
| 7 | **DONE** | `PAPER_STATEMENT_MAP.md`、180-row manifest、main-theorem receipt、targeted command receipt を作成。 |
| 8 | **DONE（proposal only）** | `sol/lean_workflow_106_proposal.yml` を起草。.github へ適用せず、dispatch もしていない。P1、既存 Marking/K3、Mathlib layer の coverage を別 target に保った。 |

## 2. Axiom/checker hygiene

`P1/AxiomCheck.lean` は次を行う。

1. `P1/*.lean`（checker 自身を除く）の現 source set 8 module を読み、すべて import 済みか確認する。
2. `ShadowAxioms` も import し、旧四 T2 名が environment に存在すれば即 fail する。
3. 全 P1-owned constant を走査し、`ci.isAxiom` は使用の有無によらず即 fail する。
4. theorem に限らず全 P1-owned declaration の依存 axioms を取り、`sorryAx` と unexpected axiom を即 fail する。
5. 全 theorem declaration を名前順に並べ、各 exact sorted axiom set と
   `Expr.consumeMData.hash` を記録する。

許可集合は Lean core の `{propext, Quot.sound, Classical.choice}` のみで、project/paper axiom は 0。
manifest は schema `p1-axiom-manifest/v2`、Lean `4.32.1`、180 rows、8 source modules である。
`Classical.choice` は Block H の一意存在から比較写像を選ぶ箇所だけに現れる。

## 3. Block H — TORS-U / B-6tw-lf

最終型は紙の LH-1 に合わせ、`m` を `FaithfulRegularAction`、比較表現 `tau` を
`FaithfulAction`（one/mul/faithful、regularity は要求しない）とした。

- `torsor_compare_unit`: generator 上の conjugacy equality を全巡回群へ伝播し、唯一の
  conjugation-implementing mapを構成。one/mul、injective/surjective、`a0 -> a1` を証明。
- `fin_cyclic_automorphism_unit`: `1<M` の `Fin M` additive automorphism について、唯一の
  `b : Fin M` を返し、`Nat.Coprime b.val M` と `phi k = k*b` を同じ conclusion type に持つ。
- `CyclicMul` / `torsor_compare_fin_unit`: additive `Fin M` を multiplicative notation の
  `C_M` に包み、abstract theorem の `phi` を上の unique unit `b` へ接続する real typed bridge。

従って abstract automorphism と `(Z/MZ)^x` の記述は別々の prose ではなく一つの corollary に
接続済みである。公理集合は最後の adapter でも `[propext, Classical.choice, Quot.sound]`。

## 4. Block A / E の境界

Block A では `Gn := {x : En n // inG x}` を実 carrier とし、積・単位・逆・全群則を閉じた。
`GnCode` との明示全単射と `n*n*n*2*2 = 4*n^3` は core-only cardinality witness である。
これは literal `Fintype.card` theorem ではないので、将来 Mathlib cardinal API が必須ならその包装だけ OPEN。

`Gn_ord_X_ambient` は ambient calculation と明記し、`xpowGn_val` bridge を追加した上で、
`Gn_ord_X` は actual `Gn n` における `xpowGn (2*n)=1` と最小性を結論する。ambient/subtype の
混同は残していない。

Lambda については部分群述語、共役類 subtype、`Fin (2*n)` 上の existence/uniqueness まで型にした。
ただし exact index/normalizer hypotheses と proof は OPEN で、theorem は export していない。

Block E の本波の閉鎖範囲は Nat/Int 算術核のみである。GT-shadow composition を (3.49) から
勝手に復元せず、(3.53) と Ihara decomposition は quarantine のままにした。

## 5. T2 exact-statement 一枚表案（コード追加前 gate）

注意: 下表は既存の画像照合済み抽出ノートと `papers/txt` の locator をまとめた**提案**である。
本 Luna 波では PDF page image の再照合をしていない。したがって exact Lean signature はすべて
**Sol approval pending**、不確定な implicit definitions は OPEN とする。

| 候補 | 原典 theorem/page | 全 hypotheses（表案） | domain → codomain | 最弱の必要 conclusion | sanity instance |
|---|---|---|---|---|---|
| Thm 4.3 explicit `(4.12)` | 2405.11725, Thm 4.3, printed p.18, (4.12) | `n ∈ Z`, `n≥3`; earlier definitions of `D_n=<r,s>`, `psi_n`, `K^(n)=ker psi_n`, `K_ord^(n)`, `X_n`, `kappa(m)`; branch `4|n` carries `k ≡ kappa(m)/2 mod 2` | equality describing `GT(K^(n))` as the displayed subset of admissible `(m,(r^(2k),r^(-2k),r^kappa(m)))` pairs | For LA-7, membership/coordinate theorem retaining `m,k,f` and both divisibility branches; not a bare existence Prop | `n=3`: `X_3={0,2,3,5}`, `k mod ord(r^2)=3`; `n=4` must exercise the parity branch |
| Thm 4.3 isolated conclusion | same theorem/proof end, printed p.18 | same `n≥3` and `K^(n)` definitions | `GTSh` objects/morphisms → proposition | `∀ source, GTSh(source,K^(n)) -> source=K^(n)` (hence the connected component has the single object), rather than an unindexed `Prop` | `n=3`, identity shadow has source=target; an ill-typed different source cannot instantiate the conclusion |
| Ihara decomposition `(1.5)` | 2405.11725, (1.5), printed p.4 | `g ∈ G_Q`; fixed cyclotomic character `chi`; the standard `f_g` attached to the Ihara action; membership in `widehat GT`/`widehat GT_gen` from surrounding definitions | `Ih : G_Q -> widehat GT` (also inclusion into `widehat GT_gen`) | a typed pair identity `Ih(g)=((chi(g)-1)/2,f_g)`, or for LE-1(b) at minimum the first-coordinate equality with codomain fixed | `g=1`: first coordinate 0 and `Ih(1)` is the identity pair |
| Composition `(3.53)` | 2401.06870, Thm 3.10, printed p.18 (PDF p.18), (3.53) | `N1,N2,N3 ∈ NFI_PB3(B3)`; `[m1,f1]∈GTSh(N2,N1)`; `[m2,f2]∈GTSh(N3,N2)`; `N_ord^(1)=N_ord^(2)=N_ord^(3)` | composable-morphism fibre product → `GTSh(N3,N1)` | typed coordinate equation `m12=2m1*m2+m1+m2` plus the exact `f1 E_(m1,f1)(f2)` coordinate if Block E claims a homomorphism | `(0,1)` is the identity in both composable orders; (3.49) follows on the m-coordinate |

この表を Sol が PDF 画像と照合し、implicit quotient/equality conventions と各 object index を承認するまで、
四候補はいずれも Lean declaration に戻さない。

## 6. Build receipt

実行はいずれも `lean/` からで、bare `lake build` は一度も実行していない。

| command | exit | 摘要 |
|---|---:|---|
| `lake build +P1.FinArith:olean` | 0 | symbolic `Fin n` laws |
| `lake build +P1.Core:olean` | 0 | actual `Gn` and group laws |
| `lake build +P1.BlockH:olean` | 0 | abstract + explicit unit + adapter |
| `lake build +P1.BlockA:olean` | 0 | actual subtype order bridge を含む |
| `lake build +P1.BlockE:olean` | 0 | arithmetic kernel |
| `lake build +P1.ShadowAxioms:olean` | 0 | comment-only quarantine module |
| `lake build +P1.AxiomCheck:olean` | 0 | fail-closed generated audit |
| `lake build P1` | 0 | 11 jobs; terminal PASS は modules=8, theorems=180 |

warning は `unusedSimpArgs` / `unusedSectionVars` の linter warning のみ。`declaration uses 'sorry'`、
`sorryAx`、unexpected axiom は 0。`git diff --check` は exit 0（最終再確認は §8）。

## 7. Workflow proposal

`sol/lean_workflow_106_proposal.yml` は proposal only。

- P1 source hygiene（P1 axiom 宣言、proof placeholder、`: True` no-op）、foundation modules の targeted build。
- cache hit でも audit log が消えないよう、`lake build P1` 後に
  `lake env lean P1/AxiomCheck.lean | tee axiom-audit.log` を強制。
- manifest と build/audit logs を artifact upload。
- 既存 coverage を落とさず `lake build Marking K3` を別 targeted job に保持し、flat
  `lean/Marking.lean` も cache key に束縛して build log を artifact 保存。
- Mathlib は source hash を cache key に含め、`lake exe cache get` の後に
  `lake build LeanArith`、log artifact upload。

`.github/**` は変更しておらず、workflow dispatch もしていない。

## 8. 成果物・hash・作業木規律

作業中に master HEAD が外部で `48afad87034c4667e04706ff01b19dc9d82b8dae` へ進んだことを確認した。
rebase/commit/push 等の git 操作はしていない。指定外の既存 dirty changes には触れていない。

主要 SHA-256（最終 audit 後）:

| file | SHA-256 |
|---|---|
| `lean/P1/AxiomCheck.lean` | `f605fd82efd1540abc8a38c9d22384369a06e08f73a3339070fad4209203cfa3` |
| `lean/P1/AXIOMS.manifest.json` | `049e8452c8d56acbbbf9656e2c9554da7e8d1380fe7c0c1cd97427fd49c4d6dd` |
| `lean/P1/AxiomAudit.receipt.md` | `6e385656f78d5406d93f90be3d94e3fca54bd913e3713835218ec03bc9cfd3c0` |
| `lean/P1/PAPER_STATEMENT_MAP.md` | `27005fb3cf3a6f513ee3c54f418bef62880bcffcbd7f71997426193b9b53cb56` |
| `lean/P1/BlockH.lean` | `a3f21551e74049f3a60a9cde95d3152b6046102532eda8856a75368902232bde` |
| `lean/P1/BlockA.lean` | `427152999e23d10b4da1200743261679b00d047eda1907b4ae141a5dfc3a8733` |
| `lean/P1/BlockE.lean` | `d7cb27e4aecf51501805b48eb900fb27d181897fecdda03c950edac0727dd241` |
| `sol/lean_workflow_106_proposal.yml` | `ece3297d1a4a0938db00269ea3ce0585dc7ba58e42ddad1e0f14b5c2807fd986` |

JSON/YAML parse はともに PASS。最終 `git diff --check` は exit 0。scoped status には上記の
assigned Lean/proposal/reply paths だけが現れ、外部 dirty changes は変更していない。

## 9. 残る OPEN

1. Lambda-REG の exact hypotheses（index、normalizer/stabilizer）と proof。
2. LA-2〜LA-5・LA-7・LA-9。
3. LE-1(b)〜LE-4（T2 exact typing、cyclotomic/Mathlib、profinite subgroup theory）。
4. T2 表の PDF image 再照合と Sol signature approval。
5. GHA authoritative run と workflow proposal の workshop approval/application。

以上を越えて completed/verified とは主張しない。
