# Sol 便 114 返信 — K13 T4/T5 再設計と壁 4 窓 crown census

作成: Sol / 2026-08-13  
対象: `ops/inbox_codex/sol_task_114_k13_wallcrown.txt` 全節 1–3  
作業枝: `sol/114-k13-wallcrown-v1`（master 非変更）  
格付け: K13 は exact candidate computation + 独立算術照合、壁 census は GAP producer + 非共有 GAP model + Python 理論照合による cross-checked。Lean verified ではない。

## 0. 着地

- final clean run **`31628909628`** は `conclusion=success`、実行 head は **`828824cc66ef7a8d580dfaadfa028eb18bf7c058`**。step1、K12 canary、step2 の 28 shard、二本の aggregate、prepare、FLINT minor 5 本、T5、壁 4 shard、独立 wall model、比較 job が全て `success`。
- K13 は `H_rank=210, r_prime=207, dim_h=630` の固定宇宙で step1 → step2 → finalize/T5 まで完了した。T5 の生欄は `factorization_fully_resolved=false` で停止し、未分解補因子に由来する素因子とその mod-rank は **UNKNOWN** のままにした。
- 壁 4 窓では、極大部分群共役類ごとの crown 分布は順に **wall24 = 5/3、wall28 = 5/3、wall36 = 6/3、wall37 = 6/5**（可換類数/非可換類数）。粒度は「socle の同型型」ではなく「極大部分群の共役類」である。
- 証拠 commit は **`6bffefd01921c25192bb0a995fe170863e3e744c`**。K13 の大型 cert は 237,590,803 bytes のため GHA artifact に置き、全主要生値と本体 SHA を versioned receipt に固定した。

## 1. K13 T4/T5 の再設計（裁定 1034）

### 1.1 死因と step1 の設計判断

run `31575182611` は `conclusion=cancelled`。630 本の generator-tree 和から制限行列を一枚岩で再構成し、`rank_nu_j_on_subspace_ambient` に入ったまま 4 時間上限へ達した。数学 checkpoint はなく、log は実質 2 行だった。

同じ対象は T2/T3 の mod-`2147483647` aggregate で既に完走していた。このため step1 を再び 630-tree monolith として走らせず、次の同一性を fail-closed で照合して schema adapter とした。

- `k=13`, H-basis、pivot prime、630-tree 和、restricted matrix、rank routine が同一。
- source aggregate run `31550443891`、source shard run `31527005518`。
- 7 shard の被覆は `[0,90),[90,180),...,[540,630)` で重複・欠落なし。
- source aggregate artifact SHA-256 は `dffa7108e288d95755b38eda2f24a804f5c609de7cdd36903225c51bee603d4d`。
- 出力は `r_check=207`、pivot positions 207 個、`r_check_matches_r_prime=true`。

したがってこれは別計算の流用ではなく、死んだ step1 と同じ行列計算の完走済み shard aggregate を、T4 schema に内容同一性つきで移したものである。

```text
step1 artifact SHA-256   c86509cc59c591c82b483b2413c487dd56d031c2db0e1cc20c09d1abe4d9b8f5
step1 checkpoint SHA-256 335866486e9b6b433094b43dabb3f1ee1d684b6120c04d2a879e06a62151f26e
```

### 1.2 step2 — 二本の exact modulus、28 shard、再開単位

各 modulus を 45-tree 幅 14 shard にし、合計 28 job とした。各 job は次を持つ。

- child hard timeout 110 分、outer timeout 125 分、heartbeat 15 秒。
- 完了した tree ごとの atomic `math_checkpoint.json`。
- `resume_run_id` から同じ modulus label・tree range の checkpoint のみを受理。
- aggregate は 14 区間が正確に `[0,630)` を被覆することを確認してから 630×207 列を組み立てる。

二本の生値は次のとおり。

| 欄 | A | B |
|---|---:|---:|
| exact modulus | `10000000000000000000000000000000000000000` | `10000000000000000000000000000000000000015` |
| aggregate file SHA-256 | `e2daeb6b17e119d04aa2de53fb8ae3f4a5ba1e978314240d506db9a18e0c4e4d` | `c62bad51f0d3b07eae2d4b7b1499a9e40c962cfb3b19b84090709c50f28890b5` |
| shape | 630×207 | 630×207 |

列配列の canonical SHA-256 は双方とも
`73dd3c7d1299bbaa279db1f5068df84f10886fe0bba91f0be1b1221f6d534a4e`、`exact_moduli_agree=true`。

### 1.3 finalize — release、内容同一性つき resume、FLINT 5 並列

基底は release tag `k13-basis-v1` の
`torsweep_k13_hnf_construct_v1_20260812.json.gz` を用いた。asset size は 152,475,282 bytes、SHA-256 は
`753f77ab416c94bc2455caa3793c40b809a486ab47c931710699f1da35c05845`。download 後、展開前に digest を照合した。

prepare は run `31610640291` の途中 checkpoint を次の順で認証した。

1. checkpoint 自身の SHA と `stage=MINOR_1_COMPLETE` を確認。
2. checkpoint が参照する旧 step1・旧 A/B・exact basis の SHA を確認。
3. 旧 A/B の exact columns が等しいことを確認。
4. 現行 A/B の exact columns が等しく、さらに旧 columns と現行 columns が等しいことを確認。
5. 以上が揃った場合だけ旧 `N_source` と minor 0 を受理。

```text
prepare SHA-256          5e7db5a75fdccc72555cf475c49be333e20c50100bbc495156924831ca4823d7
resume checkpoint SHA-256
                        514e84fc8dff4828cd64b1abb645ca235fe2c3c9fd2fe57cb789b1f28c041d95
old step2 A SHA-256      909497a81c8d248021bb4463f210f4aad24d21c8fa90eeb1f4519c40e9d13049
old step2 B SHA-256      41412811ce80cda32335cdbe60d715e7f259242ec1e6990b604bd1f9906dd789
exact basis JSON SHA-256 e75c44b04b5a72a98ca7829dacd06cce74374eeb992b5ef1785944df0866e430
resume accepted          true
N_source shape           210 x 207
```

5 個の決定的 row set を別 job にし、各 207×207 determinant を `python-flint fmpz_mat.det()` で計算した。minor 0 だけは上記認証済み checkpoint から再利用し、残る 4 本は並列計算した。全 5 本について producer の FLINT 経路とは別の modular Gaussian elimination で mod `2147483647` residue を照合した。hard timeout は各 job 100 分、outer timeout は 120 分。最終 aggregate は 429.604 秒、`timed_out=false`。

| minor | 桁数 | mod 2147483647 | checkpoint reuse |
|---:|---:|---:|---:|
| 0 | 377 | 1606374772 | true |
| 1 | 384 | 1562984548 | false |
| 2 | 383 | 1639843375 | false |
| 3 | 381 | 200545998 | false |
| 4 | 393 | 1074093544 | false |

row set は 5 本とも相異なる。各 determinant の exact 文字列 digest は receipt に固定した。

### 1.4 K12 参照系 canary

run `31565199573` の K12 完成 artifact から、同じ FLINT 経路で `N_source`、5 minor、gcd を再構成した。

```text
step1_dimensions=true
exact_moduli_agree=true
n_source_equal=true
minor_row_sets_equal=true
minor_determinants_equal=true
gcd_abs_equal=true
quar_tor_present_in_reference=true
all_checks_true=true
```

cert は `search/certs/torsweep_t4_flint_k12_check_20260812.json`、SHA-256
`6543842787d9ef79a4fb5937a7e9ba592d9354037bbdbec2809ab864bc25bbbd`。参照 QUAR-TOR 生配列は
`[2,3,5,13,37,90217,18629640697]`。

### 1.5 T4/T5 の生値

5 determinant の絶対値 gcd は独立に再計算して cert と一致した。

```text
gcd_abs = 962683674835876448190371740466972764572882250605485311695147836543576138620292053451912237619912403796351565872378511323155142592221902324141804289467675738640045122722101688758957569112826029729538159308405397255062558290968453029224516452969384663991648422242459927051107916347766691643810011879313282016325409599935187483042714342723013502914267622594753784025267448
gcd_abs_digits = 369
```

T5 の factor 欄は

```text
2^3 * 269 * 103928833037 * C
C = 4304327317070645669976359810163102066931205257837883243277284753165995353178973799361334512243541642573516467207626513592574379165261565855643302678159066583024941135959458549265586119727223399067155966839199009799741011194326589594795087530048294307438100974789235843277229215723897009758044137560494941160156191429137708547861323228842007454156661201927
isprime(C) = false
factorization_fully_resolved = false
```

既知 3 素数について、producer helper を共有しない modular rank を再計算した。

| p | rank_p | r_prime | jumps |
|---:|---:|---:|---:|
| 2 | 206 | 207 | true |
| 269 | 206 | 207 | true |
| 103928833037 | 206 | 207 | true |

QUAR-TOR 生欄は次のとおり。

```text
triggered = true
quarantined_primes = [2,269,103928833037]
commander_disposition_required = true
```

未分解合成数 `C` の素因数分解、およびその素因数での rank は **UNKNOWN**。ここから算術実現性に関する語は付していない。

### 1.6 K13 cert と receipt

- full cert: run `31628909628` / artifact id `9157008470` / artifact name `torsweep-k13-t4t5-v2-finalize` / member `torsweep_k13_t4t5_finalize_v2.json`。
- member size: 237,590,803 bytes。
- member SHA-256: `662029d808cbafcd67d044c58303e9625eb3f1555595d9687adcfba5d6f546da`。
- artifact retention expiry: `2026-09-11T20:08:21Z`。
- durable compact receipt: `search/certs/torsweep_k13_t4t5_finalize_v2_20260813_RECEIPT.json`。
- receipt SHA-256: `a6f05418a3ff91e3e90ccdad2415304fe57f96b38e60bdaa5a92077f8e1858fd`。

receipt は full cert SHA、release SHA、step1/2 SHA、minor の桁数・文字列 SHA・剰余、gcd、既知因子、未分解補因子、3 rank、QUAR-TOR を保持する。full matrix 自体は含めない。

## 2. 壁 4 窓 crown census（裁定 1046/1049）

### 2.1 宇宙、wall24、完全群の小型化

宇宙は `n in {24,28,36,37}` の 4 壁窓だけに固定した。受信便の「wall24 は repo に未在」は発送時点の在庫記述であり、処理時点には versioned witness と
`search/certs/wall2_cert_judge_20260731.json` が存在した。wall24 の `(a1,b1)` はその versioned driver から逐語的に採り、他の 3 窓と同じ `MakeWindow` 経路で再構成した。

巨大な `PN` や全 `[P,P]` を列挙せず、次の群論的縮約を用いた。

1. charming な各 `m` について `u=2m+1` と置き、`CorrectedShadowsXi` と同じ Stabilizer/Centralizer 制限で settled shadow を 1 個だけ求める。
2. 各候補で二つの hexagon、生成全射、`Bq` 上の homomorphism 定義可能性を逐一確認する。
3. `chi` の非空 fibre は `ker(chi)` の coset であり、合成は正本 (3.53)。従って各 fibre の全列挙は不要。
4. 既存 kernel cert では `ker(chi)` の shadow 数とその Xi 像位数がともに `ell * |S_t|` で、Xi は kernel 上で単射。さらに `Xi(s)=1` なら `Xi(s)(x)=x^u=x` から `u=1 mod ell`、従って `s in ker(chi)`。ゆえに Xi は全体でも単射。
5. 全 charming layer に settled representative があり、その代表と kernel Xi 像が生成する `X` は完全な `GT(N)` の忠実置換模型となる。実測で `X=Normalizer(S_n,<x>)`。

このため以下の census は単なる normalizer の上界ではなく、上記単射・全 layer coset 再構成を通した `GT(N)` 本体の census である。全 4 窓で `Phi(X)=1` なので `GT(N)/Phi` と `X` は同じ生群になった。

実行は GHA 上の GAP を用い、4 窓を別 job・別 artifact にした。各 wall child hard timeout は 120 分、outer timeout は 135 分、heartbeat は 15 秒であり、1 窓の異常が他の 3 窓の receipt を失わせない構成である。

### 2.2 crown の粒度

`Q := X/Phi(X)` とし、`ConjugacyClassesMaximalSubgroups(Q)` の各共役類から代表 `M` を一つ取った。各行の crown データは

```text
core = Core_Q(M)
primitive quotient = Q/core
crown socle = Socle(Q/core)
crown_abelian = IsAbelian(crown socle)
```

である。従って同じ `A5` または `A6` が複数行に現れるのは重複除去漏れではなく、異なる極大部分群共役類に対応する。chief factor の同型型ごとに束ねた crown quotient と、今回依頼された maximal-class census を混同していない。

### 2.3 分布表

| 壁窓 | charming layer | `GT(N)/Phi` 構造・位数 | 極大類 | 可換 crown（socle 別） | 非可換 crown（socle・index） |
|---|---:|---|---:|---|---|
| wall24 | 18/18 | `S5 x (C19 : C18)`, 41040 | 8 | 5 = `C2`×3, `C3`×1, `C19`×1 | 3 = `A5`, index 10,5,6 |
| wall28 | 22/22 | `S5 x (C23 : C22)`, 60720 | 8 | 5 = `C2`×3, `C11`×1, `C23`×1 | 3 = `A5`, index 10,5,6 |
| wall36 | 30/30 | `S5 x (C31 : C30)`, 111600 | 9 | 6 = `C2`×3, `C3`×1, `C5`×1, `C31`×1 | 3 = `A5`, index 10,5,6 |
| wall37 | 30/30 | `S6 x (C31 : C30)`, 669600 | 11 | 6 = `C2`×3, `C3`×1, `C5`×1, `C31`×1 | 5 = `A6`, index 15,6,15,10,6 |

補助生値は次のとおり。

| 壁窓 | kernel Xi | Xi image | normalizer | `Xi image = normalizer` | `|Phi|` |
|---|---|---:|---:|---:|---:|
| wall24 | `C19 x S5`, 2280 | 41040 | 41040 | true | 1 |
| wall28 | `C23 x S5`, 2760 | 60720 | 60720 | true | 1 |
| wall36 | `C31 x S5`, 3720 | 111600 | 111600 | true | 1 |
| wall37 | `C31 x S6`, 22320 | 669600 | 669600 | true | 1 |

したがって指定 4 窓の生値として、非可換 crown 類数は `[3,3,3,5]`。

### 2.4 producer、独立 model、理論照合、陽性対照

producer は wall witness、shadow equations、kernel-coset 再構成から上表の群を作った。独立 model は wall witness、`MakeWindow`、`CorrectedShadowsXi`、producer helper を一切使わず、各窓を直接

```text
AGL(1,ell) x S_t
```

として構成し、Frattini、極大類、core、primitive quotient、socle を別 GAP script で計算した。両者の maximal-class multiset は全 4 窓で完全一致した。

さらに Python checker は群構成を共有せず、理論個数

```text
abelian classes    = omega(ell-1) + 3
nonabelian classes = (# maximal classes of S_t) - 1
```

および group order、Frattini order、quotient order を比較した。共有 `C2` quotient による diagonal class を含めた値で、全欄 `true`。

陽性対照は本番と同じ census 関数で走らせた。

| control | GAP group | 極大類 | 可換 | 非可換 |
|---|---|---:|---:|---:|
| K9 | `SmallGroup(36,12)` | 5 | 5 | 0 |
| roof972 | `SmallGroup(108,43)` | 8 | 8 | 0 |

いずれも `frattini_resolution_v2` の既知個数と一致した。K9 は群論的陽性対照としてのみ使用した。

### 2.5 wall cert

repo に固定した strict cert は次の 3 本。

| 役割 | path | SHA-256 |
|---|---|---|
| producer | `search/certs/wall_crown_census_v1_20260812.json` | `8577cab61dfed850c0b520ceccabec2aa0d2b17fd006d67937b8d36ddb8b1b43` |
| independent abstract model | `search/certs/wall_crown_model_checker_v1_20260812.json` | `0018732bc989af94d5fe61362e606208b4974f9c6344ce90af0a78d9d84e61f3` |
| signature/theory comparison | `search/certs/wall_crown_census_v1_check_20260812.json` | `ebd3b442cf490da889adcd2c264898c4b2643096dd8fee99f989ce22d1f687e6` |

strict producer run `31612370595` と independent model run `31612373849` はともに `success`。final clean run `31628909628` でも 4 shard、model、combine を新しい checkout から再走し、`all_signatures_equal=true`, `all_independent_theory_fields_equal=true` を再現した。

## 3. 規律、UNKNOWN、実行・commit 台帳

### 3.1 証拠の格

- K13: exact integer artifact。FLINT determinant ごとの独立 mod-p residue、5 determinant からの独立 gcd、既知因子積、primality/compositeness、3 個の full-matrix mod-rank を別コードで再計算した。Lean verified ではないため「verified」とは呼ばない。
- 壁: witness/shadow producer と、witness 非共有の abstract product model が full maximal-class signature で一致し、さらに Python の理論個数とも一致したので cross-checked。
- どちらからも算術実現性、genuine/fake、U-6 の埋め込み問題の可解性に関する語は導いていない。壁表は U-6 の先決純群論データだけである。
- K13 の未分解合成補因子の内部と、その素因数での rank は UNKNOWN。

### 3.2 封印検疫 4 行

1. **K^(9)**: group-theory positive control のみ。算術 receipt、封印値、prereg 量には触れていない。
2. **K^(5)**: 未アクセス。
3. **sealed u/c**: 未アクセス。wall script 内の `u=2m+1` は shadow 定義の局所変数だけで、封印量 `u/c` ではない。
4. **prereg / NAME-COLLIDE**: prereg 量は非計算。4 対象のラベルは全て **「壁窓インスタンス」** とした。

### 3.3 run 台帳

| run id | conclusion | 役割・生状態 |
|---:|---|---|
| 31575182611 | cancelled | 旧 monolithic step1、4h、checkpoint なし |
| 31610365529 | failure | 初回 dependency/GAP syntax を露出 |
| 31610640291 | failure | 28 step2 shard、A/B aggregate、K12 canary は完了。旧 finalize は minor 0 後に 100 分 hard timeout |
| 31612370595 | success | strict wall producer |
| 31612373849 | success | independent wall model |
| 31627958039 | failure | resume が wrapper receipt SHA に過剰依存する点を露出 |
| 31628448590 | cancelled | sequential resume を 5-minor 並列設計で置換したため停止 |
| 31628909628 | success | final clean、head `828824cc66ef7a8d580dfaadfa028eb18bf7c058` |

### 3.4 commit / push

主要 commit は次のとおり。

```text
8d738446722f242346e454fe63d5d11113ab36d2  initial shard/checkpoint/crown workflow
d77b3154b92ab2376a33b16186ce4f98e8f2765b  dependency and first-run repairs
4acfcf7fa4e1f2c660adfe4ce825019a57cc325b  strict JSON and independent affine model
0b640d6188c25b2f9f0e1f1b3be00aaab13fcf19  versioned wall certs/check
4e7564006f9096fd9526ff7239e7773c033ef0f9  content-bound finalize resume
828824cc66ef7a8d580dfaadfa028eb18bf7c058   five parallel exact minors; final run head
6bffefd01921c25192bb0a995fe170863e3e744c   K12 canary + K13 final receipt
```

branch history の中間 `b5fdf4f876e3cb9a673cc6a2599dcdd37ef6e8b1` は一時的な tree 作成失敗で、直後の `4e7564...` が workflow と全 task file を復元した。final clean run は復元後かつ並列化後の `828824...` 上である。

作業枝 `sol/114-k13-wallcrown-v1` へ push 済み。task 実装 13 file は local content と remote blob が全て一致し、Python 10 file の構文 compile、workflow YAML parse、task path の `git diff --check` は全て通った。共有 worktree に先在した無関係な dirty file は commit に含めず、変更もしていない。master merge は工房に委ねる。
