# 返書 138 — SINGLE-BIT 全路線キャンペーン

- 対象: `ops/inbox_codex/sol_task_138_campaign.txt`
- 実行日: 2026-08-15
- 着手時 HEAD: `e18bc725fd530346a46d3859322579dda9913afc`
- 完了時観測 HEAD: `8b8682ac93ce9fd91dd20b2eef26186e41c661ae`（本便は `.git` read-only）
- 最終段: prospective に有限化できた候補 inventory を全て消化して停止
- 数値の格: producer と helper 非共有 checker が一致したものだけ cross-checked と記す
- Lean certificate: なし

最終状態は本書末尾に置く。

## 0. C0 — 便 137 の統合

便 137 は完了済みなので、本便では C0 として輸入する。凍結済みの標数 3 の 4 窓と標数 2 の 1 窓では、全 1,620 roof template について

\[
C_tZ=-A_tT_t,
\qquad
r_t^{\rm obs}:=\operatorname{rank}[A_t\mid C_tZ]-\operatorname{rank}A_t=0
\]

であった。これはその二つの有限宇宙における `COCYCLE-ABSORB-137` であり、任意の compact 加群、非半単純加群、別 roof へは量化しない。通常の群拡大は全 class で分裂したが、標識作用と同変な補群は 0 であり、「同変分裂が零写像の理由」という説明機構は成立しなかった。従って C1 以降は、同じ roof に対してまず \(r_t^{\rm obs}\) を測る。

## 1. outcome 前に固定した全候補表

ここで「消費済み」は、その明記した有限宇宙または定理の仮定内だけを指す。「不能」は現環境・現構成器では候補を有限列挙できないことを指し、数学的不存在を意味しない。

| ID | 核・素数・構成・深さ・側 | 実行可能性と規模 | 検出量 | 事前判定 / 停止規則 |
|---|---|---|---|---|
| C0 | 可換 compact、\(p=2,3\)、一段、両側 roof | 既走 5 component × 324 | 障害写像、生成 | `COCYCLE-ABSORB-137` の凍結宇宙だけ消費済み |
| C1 | \(p=2\)、\(V_{12}^{\oplus2}\)、重複方向を混ぜる全標識作用、一段、両側 roof | \(\operatorname{Aut}_{G_3}=GL_2(2)^3\); 有限全列挙可 | \(H^2\)、SURJ、\(r_t^{\rm obs}\) | 全 anchor 軌道を列挙。全 rank 0 なら class outcome を開かず構造停止、正なら全 SURJ class × 324 |
| C2 | \(p=3\)、\(V_{21}\oplus V_7^{\oplus2}\)、\(V_7\) 重複方向を混ぜる全標識作用 | \(GL_2(3)\) の 2,304 lift 対、有限全列挙可 | 同上 | C1 と同じ |
| C3 | \(p=2\)、凍結した全 5 単純 \(G_3\)-加群間の非半単純 length-2 extension | 25 ordered pair の \(H^1(G_3,\operatorname{Hom})\) と標識同変部分、有限線型代数 | extension 非分裂性、\(H^2(C_2,-)\)、SURJ、\(r_t^{\rm obs}\) | 標識同変な非零 pure class を全て取り、rank 正なら全 class × 324 |
| C4 | \(p=3\)、\(P\times G_3\) の tensor/simple 間の非半単純 extension | simple inventory と Ext-quiver の正本が未整備。最大 Hom 次元が少なくとも \(21^2\) | 同上 | C1–C3 後に構成器を試す。有限 universe を正本化できなければ不能として記録 |
| C5 | 直接 \(H^2(Q,V)\) から作る非分裂可換 2-kernel extension | `PerfectGroup(32256,2)` の一窓は便126で raw 972。残り extension class の列挙器は未整備 | 元 survival、像サイズ、extension class | 既走一窓は消費済み。他 class を完全列挙できる場合だけ走る |
| C6 | 同じく 3-kernel、mixed-primary、非中心 action | 既登録 bounded target list なし | 元 survival、像サイズ、\(H^2\) class | 標数が 2,3 の modular 成分は理論上残る。構成不能なら UNKNOWN |
| C7 | Magnus / dimension subgroup、\(p=2\)、cutoff tower | cutoff 2–5 は便134で消費、最初の非可換相対核は cutoff 5、全 972 元の survival は各 16。cutoff 6 は環次元 63 | 元単位 survival、可換化障害 | cutoff 6 の有限群または多項式座標を構成できれば全数。資源上不能なら記録 |
| C8 | lower-central / Frattini / ANUPQ の別非可換商、多段 | bounded target list なし。便134では ANUPQ が起動前に環境失敗 | 元 survival、image size | 環境を一度再監査。不能は候補消費として数えるが不存在とはしない |
| C9 | S4 側細分、`GQuotients` / `lins` / 小群 bottom-up | top-down index は巨大。bounded target list があれば bottom-up 可 | reduction image、MCOV、元 survival | `SPLIT-NULL/SPLIT-NULL″` に当たる直積 roof は事前除外。非分裂・両因子非自明だけを残す |
| C10 | dihedral \(K^{(l)}\) 細分、prime-power / mixed、塔 | 既存奇数族の単独 reduction は `THM44-odd` で全射。\(p\mid l\) の Frattini 非分裂だけでは不足 (`K5-ENT-INSUF`) | MCOV、元 survival | 定理の仮定内の単独奇数 tower は除外。S4 側との絡み、2-primary/mixed のみ残す。封印 K5 には触れない |
| C11 | fiber product / Goursat、MCOV 破れ窓、両側同時細分 | 既走 119 組は 0 failure だが選択標本。mixed-2 を含む K 側母集団が未定義 | MCOV failure、元 survival | 共通商自明または純商直積なら `SPLIT-NULL` で除外。新しい共通商を明示できた候補だけ走る |
| C12 | 一段→多段→cofinal tower | 各有限段は実行可能でも全 tower の完了判定は不能 | 最初の survival 0、像の単調減少 | 0 が出れば即停止。有限個の全 survival から逆向きの結論を出さない |
| C13 | 別 invariant: obstruction class、image size、derived/Frattini quotient | 線型・有限群 invariant は前段 gate として安価 | 非零 obstruction、image < 324、個別元 0 | いずれも発火時だけ raw witness を保存。非発火はその invariant のみの陰性 |
| C14 | 非測定路: 全有限細分に対する equality の paper proof | 現在は一般命題なし | 普遍 factorisation / residual finiteness | `COCYCLE-ABSORB-137` の一般化、または全 finite quotient を分離する定理が必要。未証明なら UNKNOWN |
| C15 | B4 refinement / B4 endgame | 本便 scope 外 | — | 発車しない |

### 1.1 先に除外する構造盲点

1. **分裂 roof**: `SPLIT-NULL` と `SPLIT-NULL″` により、共通非自明商のない直積 pure roof は対象方向を削らない。失敗した証明機構ではなく、明記された仮定内の結論である。
2. **外部標数の可換線型障害**: \(p\nmid6\) では有限巡回群 \(C_2,C_3\) に対する averaging により \(H^{>0}(C_i,V)=0\)。従って現在の cyclic obstruction detector は盲である。非可換 kernel 全体への結論ではない。
3. **既走 component の単なる直和**: C0 の行列包含は直和するので、block-diagonal duplicate は同じ roof で rank 0。これは混合標識作用や非半単純 pure action を除外しない。
4. **奇数 dihedral 単独 tower**: `THM44-odd` の仮定内では reduction が全射。非分裂性だけで検出力は従わないことは `K5-ENT-INSUF` が明示する。
5. **有限段の全 survival**: これは equality の証明機構ではない。結論の否定ではなく、有限 detector の非発火に過ぎない。

### 1.2 公式 run の共通 freeze

- outcome universe: 各候補の全 gauge orbit、全 SURJ class、frozen S4/K3 roof 324 行。rank gate が全行 0 の候補は class outcome を開かない。
- row order: orbit canonical key、class representative の辞書順、`t_index=0..323`。
- positive control: C0 の既知 972-row family と既知 group/order・rank 分布を各実装で再構成し、survivor lower bound 324 を下回れば停止。
- blind boundary: engineering preflight は orbit / dimension / rank のみ。新候補の class survival、像、個別元は 0 行開封。
- stop: 最初の非零 obstruction、像 324 未満、または survival 0 で即時停止し、候補 ID・window・class・row・元または class 座標を保存する。
- checkpoint: candidate/orbit 単位で atomic 更新。外側 hard timeout 240 秒。
- mismatch: producer/checker の universe、rank、digest のいずれかが違えば campaign を停止して UNKNOWN。

## 2. C1--C3 — compact 重複度と標数 2 非半単純入口

### 2.1 prospective freeze

`campaign138_compact_prereg/v1` で、C1 は (V_{12}^{\oplus2}) の anchor-compatible 全作用、C2 は (V_7^{\oplus2}) の同全作用、C3 は既知の標数 2 単純加群 5 個の全 ordered pair に対する pure length-2 extension と固定した。行は frozen roof の 324 行、rank gate は

\[
r_t^{\rm obs}=\operatorname{rank}[A_t\mid C_tZ]-\operatorname{rank}A_t
\]

であり、正ならその class だけを開き、全て 0 なら class outcome を開かず停止する規則である。測定前の outcome 開封数は 0、`blind_before_measurement=true`。陽性対照は既走 ESCAPE-2 の 324 行と ESCAPE-28 の 1,099,008 行を別実装で再生し、双方通過した。

### 2.2 生値

- C1: anchor solution 144、gauge orbit 2。orbit size は 108 と 36、marked group order は双方 648。(\dim H^2(C_2,V)) はそれぞれ 0, 4。後者だけ block duplicate。各 orbit の 324 行は全て (r_t^{\rm obs}=0)。
- C2: anchor solution 62、gauge orbit 5。orbit size は (24,24,12,1,1)、marked group order は (3024,3024,1008,504,1008)、(\dim H^2(C_3,V)=2,2,4,4,4)、(\dim H^1(\Gamma,V)=3,3,5,6,4)。5×324 行は全て (r_t^{\rm obs}=0)。
- C3: row=下加群、column=商加群、単純加群順 (1,D,6,12,8) とすると pure (\operatorname{Ext}^1) 次元表は

\[
\begin{pmatrix}
2&4&0&0&0\\
4&8&0&0&0\\
0&0&3&0&0\\
0&0&0&0&0\\
0&0&0&0&0
\end{pmatrix}.
\]

  標識と両立する非零 pure class は `one<-D`, `D<-one`, `D<-D` の 3 個だけで、次元は 3,3,4、(\dim H^2(C_2,-)=1,1,0)、(\dim H^1(\Gamma,-)=2,1,2)。3×324 行は全て (r_t^{\rm obs}=0)。

合計 rank template は 3,240、正 rank は 0、従って prereg どおり class/element outcome の開封数は 0。producer と独立 checker の全項目が一致したので、この有限宇宙について cross-checked。Lean certificate はない。

### 2.3 新しい盲族候補と限界

`MULTIPLICITY-ABSORB-138` 候補: frozen C1 の全 anchor-compatible 標数 2 (V_{12}^{\oplus2}) 作用、及び frozen C2 の全 anchor-compatible 標数 3 (V_7^{\oplus2}) 作用について、frozen 324 roof row 上の写像

\[
Z^1(\Gamma,V)\longrightarrow\operatorname{coker}A_t
\]

は零である。これは有限全列挙の結論であり、任意の重複度加群へ量化する紙の証明機構は UNKNOWN。

`INDECOMP-ENTRY-138` 候補: 上記 5 単純加群から作る標識両立 pure nonsplit length-2 extension はちょうど上記 3 個で、その全 roof rank は 0。標数 3 tensor lane への一般化は UNKNOWN。ここで成立しなかったのは「任意の非半単純加群まで同じ」という一般化機構であり、上記有限宇宙の零結論ではない。

## 3. C5/C6 — PerfectGroups 直接拡大棚

### 3.1 GAP 起動と helper 非共有 metadata inventory

prospective prereg 後に `./gap.ps1 search/campaign138_perfect_inventory_v1.g` を実行したが、script 読込前に `couldn't create signal pipe, Win32 error 5` で終了した。これは群の不存在ではなく、この環境の GAP process 起動失敗である。失敗 cert を保存した。

代替の read-only metadata producer と独立 checker は、order 2,000,000 未満で (504\cdot2^d) 形の PerfectGroups record を 17 件抽出した。次元分布は (d=6:2,d=7:4,d=8:6,d=9:4,d=10:1)。これは metadata のみで、群構成・radical・splitness・標識・影像に関する主張ではない。

### 3.2 d=7 の完全 preflight と正式測定

GAP library `perf6.grp` の exact finite presentation を SymPy relator-based coset enumeration で再構成した。三つの nonsplit 表示 record ([16,7,2..4]) は degree 112、order 64,512、核 order 128。生値は次の通り。

| key | order-2 lift | order-3 lift | marked pair | gauge orbit | full-generation orbit | complement orbit |
|---|---:|---:|---:|---:|---:|---:|
| `[16,7,2]` | 0 | 64 | 0 | 0 | 0 | 0 |
| `[16,7,3]` | 16 | 64 | 1,024 | 16 | 16 | 0 |
| `[16,7,4]` | 0 | 64 | 0 | 0 | 0 | 0 |

producer は custom closure、checker は library を再解析して Schreier--Sims を使い、全配列・全 orbit を一致させた。影像を一切開けない preflight として cross-checked。

続いて ([16,7,3]) の全16 orbit を prospective に凍結した。各 orbit の宇宙は charming exponent 6 個×群元 64,512 個 = 387,072 行。生成条件は「核で割った 504 元商を生成」に緩和した。従って得る source image は実際の source image の上界であり、欠落は荷重を持つが全像には負の結果以上の力を与えない。

正式生値は全16 orbit で同一だった。

- source shadow count: 432（16/16）
- reduced target key: 54/54（16/16）
- roof raw image: 972（16/16）
- missing key: 0（16/16）
- 陽性対照: target 54 key×18=972、既走 972 も再現

独立 checker は producer helper を import せず、`perf6.grp` から群を再構成して全16×387,072 行を再走した。全 check true。よってこの必要条件 detector の「欠落 0」は cross-checked だが、有限深度から逆向きの認定はしない。

### 3.3 d=8--10 全 record preflight

metadata inventory 中、nonsplit marker を持つ higher 7 record を全て prospective に固定し、record ごとの 240 秒 hard timeout で最後まで処理した。親 preflight v1 の生値は次の通り。

| key | kernel | degree | order-2 lift | order-3 lift | gauge orbit | full-generation orbit |
|---|---|---:|---:|---:|---:|---:|
| `[16,8,2]` | order 4 元あり | 288 | 0 | 64 | 0 | 0 |
| `[16,8,3]` | elementary (2^8) | 224 | 0 | 64 | 0 | 0 |
| `[16,8,4]` | elementary (2^8) | 224 | 32 | 64 | 32 | 32 |
| `[16,8,5]` | elementary (2^8) | 224 | 0 | 64 | 0 | 0 |
| `[16,9,2]` | order 4 元あり | 576 | 0 | 64 | 0 | 0 |
| `[16,9,3]` | elementary (2^9) | 336 | 0 | 64 | 0 | 0 |
| `[16,10,1]` | order 4 元あり | 400 | 0 | 64 | 0 | 0 |

重要な procedural audit:

1. 親 prereg は7件全てを elementary と予想したため、親 cert の aggregate positive control は `passed=false` になった。これは隠さず、order 4 元を持つ `[16,8,2]`, `[16,9,2]`, `[16,10,1]` を非可換核レーンへ再分類した。
2. `[16,10,1]` は最初の parser が GAP の inline comment、次に `a^b` conjugation notation で停止した。群 outcome は未開封だったので、v1, v2 の prospective prereg を別ファイルに残した。v2 は order 516,096、kernel order 1,024、degree 400 を再現し、order-2 lift 0 を得た。
3. 独立 checker は七群を全て library から再構成し、上表、全 orbit 配列、三つの非可換核 record、唯一の生成可能 family `[16,8,4]` を一致させた。親 control の失敗原因まで一致したので、表の個別生値は cross-checked。親の誤った「全て elementary」という仮定は棄却されたままである。

### 3.4 `[16,8,4]` の正式全32-orbit測定

唯一残った family の全32 generating orbit を outcome 前に凍結した。各 orbit は charming exponent 6 個×129,024 群元 = 774,144 行、総計 24,772,608 行。d=7 と同じ必要条件緩和を用いた。600 秒 hard timeout は二度正常作動し、さらに Windows の checkpoint rename と監視 read の競合が一度起きたが、完成 orbit は保持し、同時 read を止めて再開した。候補数・行数の切詰めはない。

生値は全32 orbit で同一:

- source shadow count: 432（32/32）
- reduced target key: 54/54（32/32）
- roof raw image: 972（32/32）
- missing key: 0（32/32）
- internal floor 324 と target 972: 通過

独立 checker は producer helper 非共有で、有限表示、二つの112点 coset block、群・核・商を再構成し、全32×774,144 行を再走した。`raw_image_size_distribution={972:32}`, `source_shadow_count_distribution={432:32}`、全 check true。従って cross-checked。Lean certificate はない。

`MARKED-LIFT-VOID-138` 候補: frozen base words `S=accbxbccb`, `T=cacaccwb` と上表の `[16,8,2]`, `[16,8,3]`, `[16,8,5]`, `[16,9,2]`, `[16,9,3]`, `[16,10,1]` に限れば、order-2 lift が 0、従って標識 pair が 0。これは exact library census であって、任意の higher extension の定理ではない。

`PERFECT-RELAXED-SURJ-138` 候補: `[16,7,3]` の全16 orbit と `[16,8,4]` の全32 orbit、frozen charming exponent、商生成緩和の下で、reduced key set は target 54 key 全体。これは有限結論として cross-checked。一般の perfect extension に対する証明機構は未構成であり、「機構がない」とこの有限結論を取り違えない。

## 4. C4, C6--C15 の消化判定

| ID | 本便での消化 | 残る UNKNOWN / 必要な新技術 |
|---|---|---|
| C4 | 標数 3 の既知 direct-sum/重複度 lane は C0/C2 で rank 0。非半単純 tensor/simple extension の正規化された有限 universe は現棚にない | (P\times G_3) の modular simple/Ext-quiver、標識両立 class の canonical enumerator |
| C5 | order 2,000,000 未満の PerfectGroups 17 metadata record を全数棚卸し。nonsplit marker の d=7--10 全10 record は d=7 の3件と higher 7件で構成・標識 preflight 済み。生成可能なのは2 family、双方正式測定で 972 | library 外の (H^2(Q,V)) class を重複なく列挙する cohomology-to-presentation compiler |
| C6 | 標数 3 / mixed-primary の bounded target list がなく、負の有限探索を非存在へ格上げしない | modular (H^2) database、mixed radical action builder、標識 gauge canonicalisation |
| C7 | Magnus cutoff 2--5 は既走、cutoff 6 は現次元 63 で有限群表示を構成できず、環境限界として消化 | sparse graded-Lie / dimension-subgroup collector と quotient certificate |
| C8 | 本便 GAP は script 前に signal-pipe error、既便 ANUPQ も起動前失敗。数学的な空集合とはしない | 動作する GAP/ANUPQ worker、同一入力の独立 collector |
| C9 | split/pure roof は `SPLIT-NULL` / `SPLIT-NULL″` で構造的に盲。残る mixed S4 refinement は index/order bound がない | `GQuotients`/`lins` 用の有限 presentation と事前登録可能な bound |
| C10 | odd dihedral単商は `THM44-odd` で reduction 全射、従ってこの detector では盲。(p=2,3) modular tower は未構成 | modular Frattini tower。sealed K5 と `u,c` には本便で接触しない |
| C11 | 既走 fiber-product 選択標本は MCOV failure 0。split/common-direct-factor は `SPLIT-NULL` で盲 | mixed-2 common quotient の全分類と Goursat data canonicaliser |
| C12 | 各有限段は実行可能でも cofinal tower 全体を有限表にできない。有限段の全 survival から逆向きに結論しない | cofinal separation theorem、又は compactness を荷重可能にする証明書 |
| C13 | rank gate、cyclic obstruction、image cardinality を実行。新しい非零 obstruction は 0 | derived/Frattini quotient 上の新しい functorial obstruction と陽性対照 |
| C14 | `COCYCLE-ABSORB-137` を全有限商へ一般化する紙の証明も、その反対向きの分離定理もない | universal factorisation 又は residual separation の定理 |
| C15 | B4 endgame は明示的に本便範囲外 | 工房裁定後のみ実行 |

ここで「消化」は、構造定理による除外、凍結有限宇宙の完走、又は再現可能な環境/技術限界の記録のいずれかを意味する。負の探索を非存在の証明とはしていない。実行可能かつ prospective に有限化できた候補表は尽きた。

## 5. 最終監査

### 5.1 生値による停止規則

- nonzero obstruction: 0
- missing target key: 0
- minimum raw image among formally measured perfect-extension orbits: 972
- survivor floor 324 violation: 0
- 従って immediate stop 条件は発火しなかった。
- 全 finite-depth survival から逆向きの型認定はしていない。最終数学的 1-bit は本便では UNKNOWN のまま。

### 5.2 endgame scope

```text
endgame_scope=gentle
PENT_W=NOT_RUN
B4/U-10=NOT_RUN
required_order=PENT_W-PASS -> B4/U-10
B4_in_scope=false
```

### 5.3 novelty grep receipt

```text
command: rg -n 'MULTIPLICITY-ABSORB-138|INDECOMP-ENTRY-138|MARKED-LIFT-VOID-138|PERFECT-RELAXED-SURJ-138' docs sol search crosscheck --glob '!sol_reply_138_campaign.md'
exit_code: 1
output: (empty)
```

これは名称衝突が見つからなかったという receipt に限る。数学的新規性の証明ではない。

## 6. 成果物 SHA-256

| lane | prereg | producer | raw cert | checker | verdict |
|---|---|---|---|---|---|
| C1--C3 compact | `39bf63af8f3574785e3c55188d246eaa6bfa4e02e32d81b3e45ed6ac5a935cbe` | `691be784536bbd91687b049b4910f00067caa2175bee62eeca0077570708c9b7` | `81e25f53c1a7494481660b3bd405116020897d8f7ba94607769947980f86bec2` | `e8fbbe552fb4dbe245b6b8c988b93a0939d0485186c11eb7c349336794a2fce4` | `bd9135f9cf7683f708b9583ed7608b02dcc9dbabf248bb2967255eb9e9f0f2a4` |
| GAP inventory failure | `1260ccbd3244aee019a024efc6b2855de8227546fe3eb7a6257599030c645f50` | `fc3c4b419a06ca2677d5e05491ff4e09e32944a28c99bfac7922d949885eb248` | `9df6549f7d21604911daa26db7d32c04695c3dcdd03e0193610ef366f1f8411b` | — | — |
| metadata 17 | `812777cb6dce9071718afd767a7a3a732a66b79543860a273fe377329588b0da` | `c3c85ee517dee67d55b2583c3313a984fc348d2022912507d5664a8c311e8e9c` | `c984c65acbc211b3340aef9c019d22180831bbe5e95a51bccbf83d004424cb84` | `c7625d85b4bd54f18fc5f8cfa9d8bfaee661da49dc3e6b079144b96976531956` | `d53258f49e72c53eba48d37ddf8c573d548c6fa8fabb5b8a5965ea38f05b0372` |
| d=7 preflight | `00be09344e94d4111bb48f732c16936fdaad8af1c0603efafc30d698766ceec5` | `8e9628d13808d8e358ab6b0a0c74748cf0d47ad89ce68dde7ec53e66fb7e704f` | `dddd51b7c03af8d1644fe9fba99f0a3970d9d3961f94bee0eea83bff66db19b1` | `7dafa72c22c985092ead3e9d53e6ee949b9dc83d633a7f82410e5bc4c794210c` | `2fc67f7c4e6fbf06c8256e35b745feb30830957425b53889e76926d36c5c5f8e` |
| d=7 measure | `b0ee3124cc16cee0137486e9248cc84416226b6a5712fa594174e5205a20d367` | `e9ebaad5b32e21c46e0ef6e15fcc8453d2ab6e393bc41bad48cfa52792ba9a0a` | `b79a0ab18ea79f56430563d3aca0a74725894dbb54121c1fd913e8052b9f5aaf` | `dc699be65be3e3db37753cf69e7168d1749d2014737b38dbb5c18c2b45c21835` | `492cb8dcd35c8caf31270bd1f48d00d69fbd6893077ce59d1227d4a839495e51` |
| higher preflight | `b7010527da7a733a3b892602e3b2a5e2695990bb482f7672673b631e147bb3b6` | `8f32e036584680c66e685c6158d1bc51e9b76e84a1861a59cd261f4a6ffc9069` | `20a09328de0be5839ff551ab8de503b9ee427b0d96e97c1c4eb627b2ef25ef43` | `58304b4d725ec04b15f43b1b341cbb0fb73aa855afe315c7b7d3ff28773889ab` | `1610ce5b7cd64c7824e2abdd2e41b3f75ea7a911c00a3a7bd8af7651df1ad7b4` |
| d=10 parser v1/v2 | `023bf3106bb49bc57cae1514659bebd59f585f2e3338b3842447f221d130ada2`, `37785a65163086ccccb042279b50e7df4499ff6a185392266bd66eeb8a5c84e4` | `1b07117a7066491e891589bebc357d3053f396c5769c7b8cbfbed20de6b14bfe`, `83da8581fb961272ace4e6e8a397e7961e352bf9158fd4aa2afdb49e7ddf4a76` | v2 `74e35727021c57d336e6905ac2f10ec70c546807755931de1fcaff56bb77ccae` | higher checker に統合 | higher verdict に統合 |
| d=8 measure | `0bceaff295cf61399ba274b048c48c02fe767b61791f1a5cb8038091d1f75a22` | `a2861fb7e30024c58624a4ffc0e1ecee8c428dac632154cb71011e7947e2e236` | `bfc2247f994cb4e8fd9a00fc573f8de94524e1a1b523b8aaddee20961e2d618e` | `0fab334a36e0a02c95a3a3e4fc27568f7c7011c9eec93b0cf77476062cd4e04f` | `5296a41b2fa758cae49bf7186caf0bfd421f47dd4e14eade90dcb51da2309e9c` |

対応 path は各 lane の `search/campaign138_*`, `search/certs/campaign138_*`, `crosscheck/check_campaign138_*`, `crosscheck/verdicts/campaign138_*`。checkpoint も同じ通常位置に保存した。

候補表 C0--C15 は、既在定理による構造除外、cross-checked finite run、又は明記した環境・新技術限界のいずれかに到達した。発火はなく、現在の道具で prospective に有限化できる候補 inventory は尽きたため停止する。

CAMPAIGN_STATUS: EXHAUSTED
