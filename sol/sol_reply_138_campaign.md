# 返書 138 — SINGLE-BIT 全路線キャンペーン

- 対象: `ops/inbox_codex/sol_task_138_campaign.txt`、追補 `ops/inbox_codex/sol_task_138b_bside.txt`
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

| ID | 核・素数・構成・深さ・側 | 実行可能性と規模 | 検出量 | 事前判定 / 停止規則 | B 側 / cofinality への寄与 |
|---|---|---|---|---|---|
| C0 | 可換 compact、\(p=2,3\)、一段、両側 roof | 既走 5 component × 324 | 障害写像、生成 | `COCYCLE-ABSORB-137` の凍結宇宙だけ消費済み | **測定のみ、寄与 0**。任意の module・roof に一様な吸収定理へ上げて初めて煉瓦になる |
| C1 | \(p=2\)、\(V_{12}^{\oplus2}\)、重複方向を混ぜる全標識作用、一段、両側 roof | \(\operatorname{Aut}_{G_3}=GL_2(2)^3\); 有限全列挙可 | \(H^2\)、SURJ、\(r_t^{\rm obs}\) | 全 anchor 軌道を列挙。全 rank 0 なら class outcome を開かず構造停止、正なら全 SURJ class × 324 | **有限測定のみ、寄与 0**。block-diagonal 直和則は機構化できるが、混合作用全般の族定理ではない |
| C2 | \(p=3\)、\(V_{21}\oplus V_7^{\oplus2}\)、\(V_7\) 重複方向を混ぜる全標識作用 | \(GL_2(3)\) の 2,304 lift 対、有限全列挙可 | 同上 | C1 と同じ | **有限測定のみ、寄与 0**。`MULTIPLICITY-ABSORB-138` は凍結宇宙 candidate に留まる |
| C3 | \(p=2\)、凍結した全 5 単純 \(G_3\)-加群間の非半単純 length-2 extension | 25 ordered pair の \(H^1(G_3,\operatorname{Hom})\) と標識同変部分、有限線型代数 | extension 非分裂性、\(H^2(C_2,-)\)、SURJ、\(r_t^{\rm obs}\) | 標識同変な非零 pure class を全て取り、rank 正なら全 class × 324 | **有限測定のみ、寄与 0**。全 indecomposable extension を覆う定理は無い |
| C4 | \(p=3\)、\(P\times G_3\) の tensor/simple 間の非半単純 extension | simple inventory と Ext-quiver の正本が未整備。最大 Hom 次元が少なくとも \(21^2\) | 同上 | C1–C3 後に構成器を試す。有限 universe を正本化できなければ不能として記録 | 未構成・族定理なし、寄与 0 |
| C5 | 直接 \(H^2(Q,V)\) から作る非分裂可換 2-kernel extension | `PerfectGroup(32256,2)` の一窓は便126で raw 972。残り extension class の列挙器は未整備 | 元 survival、像サイズ、extension class | 既走一窓は消費済み。他 class を完全列挙できる場合だけ走る | 非分裂群の有限測定まで到達したが、source 条件は緩和され isolated/cofinal 配置も未証明。**寄与 0** |
| C6 | 同じく 3-kernel、mixed-primary、非中心 action | 既登録 bounded target list なし | 元 survival、像サイズ、\(H^2\) class | 標数が 2,3 の modular 成分は理論上残る。構成不能なら UNKNOWN | 未構成・族定理なし、寄与 0 |
| C7 | Magnus / dimension subgroup、\(p=2\)、cutoff tower | cutoff 2–5 は便134で消費、最初の非可換相対核は cutoff 5、全 972 元の survival は各 16。cutoff 6 は環次元 63 | 元単位 survival、可換化障害 | cutoff 6 の有限群または多項式座標を構成できれば全数。資源上不能なら記録 | cutoff 2–5 は**測定のみ、寄与 0**。全 cutoff の盲目性と塔の cofinality の二定理が必要 |
| C8 | lower-central / Frattini / ANUPQ の別非可換商、多段 | bounded target list なし。便134では ANUPQ が起動前に環境失敗 | 元 survival、image size | 環境を一度再監査。不能は候補消費として数えるが不存在とはしない | 未構成・族定理なし、寄与 0 |
| C9 | S4 側細分、`GQuotients` / `lins` / 小群 bottom-up | top-down index は巨大。bounded target list があれば bottom-up 可 | reduction image、MCOV、元 survival | 直積 roof も **(MCOV) 成立時だけ** `SPLIT-NULL″` で事前除外。MCOV 破れ、非分裂、両因子非自明を残す | 直積 + (MCOV) の範囲だけ族煉瓦。一般の S4 側深化は未被覆 |
| C10 | dihedral \(K^{(l)}\) 細分、prime-power / mixed、塔 | 既存奇数族の単独 reduction は `THM44-odd` で全射。\(p\mid l\) の Frattini 非分裂だけでは不足 (`K5-ENT-INSUF`) | MCOV、元 survival | 定理の仮定内の単独奇数 tower は除外。S4 側との絡み、2-primary/mixed のみ残す。封印 K5 には触れない | `PH2-VOID` / `THM44-odd` の仮定内は族煉瓦。ただし dihedral 系だけでは isolated 細分全体に cofinal でない |
| C11 | fiber product / Goursat、MCOV 破れ窓、両側同時細分 | 既走 119 組は 0 failure だが選択標本。mixed-2 を含む K 側母集団が未定義 | MCOV failure、元 survival | 共通商自明でも除外できるのは直積 + (MCOV) の場合だけ。新しい共通商又は MCOV 破れを明示した候補を走る | 119 組は**測定のみ、寄与 0**。直積 + (MCOV) の定理範囲だけ寄与 |
| C12 | 一段→多段→cofinal tower | 各有限段は実行可能でも全 tower の完了判定は不能 | 最初の survival 0、像の単調減少 | 0 が出れば即停止。有限個の全 survival から逆向きの結論を出さない | **B 側の主軸**。一様全射定理 + 族合併の cofinality が揃えば COMPACT を適用できるが、双方未達 |
| C13 | 別 invariant: obstruction class、image size、derived/Frattini quotient | 線型・有限群 invariant は前段 gate として安価 | 非零 obstruction、image < 324、個別元 0 | いずれも発火時だけ raw witness を保存。非発火はその invariant のみの陰性 | 陰性測定は寄与 0。全細分での消滅をいう functorial 定理になった場合だけ寄与 |
| C14 | 非測定路: 全有限細分に対する equality の paper proof | 現在は一般命題なし | 普遍 factorisation / residual finiteness | `COCYCLE-ABSORB-137` の一般化、または全 finite quotient を分離する定理が必要。未証明なら UNKNOWN | COMPACT 直結の B 路だが、現在は定理なし |
| C15 | B4 refinement / B4 endgame | 本便 scope 外 | — | 発車しない | 本追補でも範囲外 |

### 1.1 先に除外する構造盲点

1. **分裂 roof**: `SPLIT-NULL` が無条件に与えるのは、共通非自明商のない直積 pure roof の像が \(m\)-fiber の合併であり、\(\mathfrak F_0\) 方向を部分的に削らないことまでである。全面的な全射には **(MCOV)** が必要であり、無条件版 `SPLIT-NULL″` は撤回済み、現行版は (MCOV) 付きである。
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
| C9 | split/pure roof で無条件に盲なのは \(\mathfrak F_0\) 方向だけ。全面的に全射なのはさらに (MCOV) が立つ部分族。残る MCOV 破れと mixed S4 refinement は index/order bound がない | `GQuotients`/`lins` 用の有限 presentation、事前登録可能な bound、MCOV の族判定 |
| C10 | odd dihedral単商は `THM44-odd` で reduction 全射、従ってこの detector では盲。(p=2,3) modular tower は未構成 | modular Frattini tower。sealed K5 と `u,c` には本便で接触しない |
| C11 | 既走 fiber-product 選択標本は MCOV failure 0。split/common-direct-factor でも全面的に盲といえるのは (MCOV) 成立時だけ | mixed-2 common quotient の全分類、Goursat data canonicaliser、MCOV 破れの悉皆化 |
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

## 7. 便 138b 追補 — B 側と cofinality

### 7.1 COMPACT を使うための量化

固定した基底窓 \(M\) の下の isolated 細分を

\[
\mathcal I_M:=\{K:K\subseteq M,\ K\text{ は isolated}\}
\]

とする。部分族 \(\mathcal U\subseteq\mathcal I_M\) がここで必要な意味で cofinal とは

\[
\forall K\in\mathcal I_M\ \exists L\in\mathcal U:\quad L\subseteq K
\]

である。\(L\subseteq K\subseteq M\) なら

\[
\operatorname{Im}R_{L,M}\subseteq\operatorname{Im}R_{K,M},
\]

従って \(\mathcal U\) が cofinal で、全 \(L\in\mathcal U\) について \(\lvert\operatorname{Im}R_{L,M}\rvert=972\) を**族定理**で示せれば、全 isolated 細分上の像の交わりは \(GT(M)\) になる。正典 Thm 5.2 の系である定理 COMPACT により、これが B 側の確定条件である。

逆に、有限個の窓で 972 を測っても上の全称量化も cofinality も与えない。本便の C0--C13 の陰性値は、対応する族定理へ上がらない限り B 側の勘定ではすべて 0 である。

### 7.2 正典の二つの射程訂正

被覆を数える前に、旧表の略記を現行正本へ戻す。

1. `SPLIT-NULL` の結論は、直積 pure roof の像が \(m\)-fiber の合併であり、\(\mathfrak F_0\) 方向を部分的に削らないことまでである。`ihnec_v1.md` D.1（裁定 388）により、無条件版 `SPLIT-NULL″` は撤回済みである。全面的な全射には
   \[
   \forall m\in\mathcal X_n\ \exists\widetilde m:\quad
   \widetilde m\equiv m\pmod{2n},\qquad
   \widetilde m\bmod N'_{\rm ord}\in\mathfrak m(N')
   \tag{MCOV}
   \]
   が別に要る。(MCOV) が破れれば、直積 roof でも欠けた \(m\)-fiber 全体を削る。
2. `OBS-VOID (i)` の自動消滅範囲は \(p\ne3\) ではなく **\(p\nmid6\)** である。\(p=2\) では \(H^2(C_2,V)\)、\(p=3\) では \(H^2(C_3,V)\) が残りうる。

従って L107 の旧残余「非分裂・非テンソル・\(p=3\)・非自由」だけでは不足する。現況には \(p=2\) 非自由、非可換核、多段、S4 側深化、さらに **MCOV が破れる直積 roof** も含める必要がある。

### 7.3 cofinality 被覆台帳

次表の「覆う」は、全面的な像 972 をいう行と、部分機構しか与えない行を明記して分けた。後者を COMPACT の被覆数には算入しない。

| 族名 | 仮定(逐語) | 覆う細分の範囲 | 未被覆として残る範囲 | 定理格(定理/candidate/機構のみ) |
|---|---|---|---|---|
| `SPLIT-NULL` | \(n\) は奇数 \(\ge3\)、\(N'\in I\)、\(M=K^{(n)}\cap N'\)、\(G_n\) と \(PB_3/N'\) に共通の非自明商が無い | その全直積 pure roof の **\(\mathfrak F_0\) 方向だけ**。像は \(m\)-fiber の合併 | MCOV 破れによる \(\chi\) 方向、entangled roof、相対拡大 | **定理**（paper-proof 相互監査 PASS、ただし部分機構） |
| `SPLIT-NULL″` 差替版 | `SPLIT-NULL` の全仮定 **かつ (MCOV)** | その仮定を満たす全直積 roof で \(R_{M,K^{(n)}}\) 全射 | MCOV 不明・破れ、共通商非自明、一般の相対拡大 | **candidate**（paper-proof。(MCOV) 無しの形は撤回） |
| `PH2-VOID` | \(9\mid l\)、\(K^{(l)}\subseteq K^{(9)}\)、\(K=K^{(l)}\cap N_{S4}\)。dihedral reduction は Thm 4.3 で全射、S4 の各 \(u\)-fiber は 9 元 | 固定 S4 roof の下で dihedral 側だけを深める全 admissible \(l\) | S4 側深化、両側同時細分、一般 isolated 細分 | **定理**（`SPLIT-NULL` + 当該族の MCOV の系） |
| `PH2-VOID′` / perfect \(E\) | \(PB_3/K\cong G_l\times E\)、reduction が \(\mathrm{id}\times(E\to P)\) | 像公式 \(18\cdot\lvert\operatorname{Im}(GT(N_E)\to GT(N_{S4}))\rvert\)。Phase 2b の一つの \(E\) では右因子全射を測定 | 一般 perfect \(E\) の右因子全射、非完全 \(E\)、非直積拡大 | **機構のみ**。直積性だけでは 972 を与えない |
| 可換 \(C_3\) 橋 | \(E=P\times C_3\)、\(G_l^{\rm ab}\) は 2 群、従って全 \(l>0\) で共通非自明商なし | 全 level で pure 商が直積になること | MCOV と full image。便 127 は `raw_image_size=null` | **機構のみ**（紙 + preflight 測定） |
| `BLIND-vNext (c)` | \(E=PB_3/N_E\)、\(V=\ker(E\to P\times G_3)\ne1\)、\(V\) に \(P\) 又は \(G_3\) の一方が自明に作用 | 該当 affine roof がさらに直積分解すること | MCOV、両因子が非自明に作用する加群、非半単純混合 | **定理**（直積化）。COMPACT への全面被覆は **機構のみ** |
| `OBS-VOID` | \(K=K^{(l)}\cap N_E\)、\(PB_3/N_E=E=V\rtimes W\)、\(V\) は \(\mathbf F_p\)-加群、\(H^2(B_3/\langle c\rangle,V)=0\) | この一段可換 semidirect 族で reduction 全射。十分条件は \(p\nmid6\)、又は \(p=3\) で \(V\!\downarrow_{\langle\tau\rangle}\) が自由 | \(p=2\) の \(\theta\)-非自由、\(p=3\) の \(\tau\)-非自由、非可換・非分裂・多段 | **定理**（paper-proof、単系統。Lean certificate なし） |
| block-diagonal 直和 | \(V=\bigoplus_iV_i\) で \(A_t,C_t,Z\) が同じ分解に関して block diagonal、各 \(C_{t,i}Z_i\subseteq\operatorname{Im}A_{t,i}\) | 既知の吸収成分の任意有限直和で \(r_t^{\rm obs}=0\) | 混合標識作用、非半単純 extension、GEN-AFF | **機構のみ**（有限次元線型代数の直和則） |
| `(H-SPLIT)` 条件部 | 相対拡大に \(\theta,\tau\)-同変な群準同型 section があり、さらに GEN-AFF が別に成立 | この強い前件を満たす split 相対拡大では relation を section で運べる | 通常分裂だけの拡大、同変 section 不在、全非分裂拡大 | **機構のみ**。既走 3,399 class では前件成立 0 |
| `COCYCLE-ABSORB-137` / `MULTIPLICITY-ABSORB-138` / `INDECOMP-ENTRY-138` | frozen S4/K3 roof 324 行と、各命題に列記した有限 module・marking 宇宙 | その有限宇宙で \(C_tZ\subseteq\operatorname{Im}A_t\) | 任意 roof、任意 module、base change、塔 | **candidate**（有限 exhaustive 結論）。**族定理ではない** |
| `THM44-odd` / `K5-ENT-INSUF` | 指定された odd dihedral reduction。特に \(N=K^{(np)}\subset K^{(n)}\)、\(p\mid n\) でも reduction 全射 | odd dihedral 単独 tower の定理射程 | 2-primary、mixed-primary、S4 と絡む tower | **定理 / candidate**（各札の既存格どおり）。dihedral 族は cofinal でない |

この台帳から全面的な 972 の族煉瓦として数えられるのは、(i) `SPLIT-NULL″` の **(MCOV) 付き**部分族、(ii) `PH2-VOID` の admissible dihedral 部分族、(iii) `OBS-VOID` の \(H^2=0\) 一段可換 semidirect 部分族である。残りの行は部分機構、又は有限 candidate であり、cofinality への加算は 0 である。「7 族」は独立な七方向ではなく、実質的には **直積 + MCOV** と **一段可換核の \(H^2\) 消滅**の二機構に集中している。

### 7.4 測定台帳 — cofinality への加算は全て 0

| 測定 | 有限宇宙と生値 | 族定理との差 |
|---|---|---|
| ESCAPE-28 | \(p=3\)、\(\tau\)-非自由。3,392 class、1,099,008 行、全不発 | 一つの module/roof 構成。任意の \(p=3\) 非自由細分へ量化しない |
| ESCAPE-2 | \(p=2\)、\(\theta\)-非自由。7 class、2,268 行、全不発 | 一つの module/roof 構成。任意の \(p=2\) 非自由細分へ量化しない |
| 便 134 | 非可換相対核を持つ cutoff 5 の一窓。全 972 元の lift 数は各 16 | 非可換核一般、多段、全 cutoff へ量化しない |
| C1--C3 | 3,240 rank template で \(r_t^{\rm obs}>0\) は 0 | 凍結した重複度作用と三つの length-2 class に限る |
| C5 d=7 | `[16,7,3]` は complement orbit 0、16 orbit 全て relaxed raw image 972、missing key 0 | 非分裂**群拡大**の有限測定。source generation は商上全射へ緩和され、isolatedness も未確認 |
| C5 d=8 | `[16,8,4]` は generating orbit 32、全て relaxed raw image 972、missing key 0 | 同上。一般の非分裂 2-kernel extension へ量化しない |
| C11 既走標本 | 119 組で MCOV failure 0 | 選択標本であり、MCOV の族定理でも悉皆でもない |

従って、L107 の「非分裂」については更新が要る。**非分裂群拡大の有限例は C5 で得た**ので、抽象的存在が未確認という段階ではない。しかし、その kernel が COMPACT の添字となる isolated 細分であること、本来の source 条件で全射であること、まして非分裂 isolated 細分の族全体が盲であることは示していない。B 側の穴は閉じていない。

### 7.5 `(H-SPLIT)` と非分裂主戦線の裁定

便 137 の判定は次の三層に分かれる。

1. ESCAPE-28 の 3,392 class と ESCAPE-2 の 7 class は、相対拡大としては全て通常分裂した。
2. \(\theta,\tau\)-同変な補群は全 3,399 class で 0 だった。従って「通常分裂なら全て盲」という族定理は `(H-SPLIT)` から出ない。
3. 「同変 section は relation を運ぶ」という条件命題は正しいが、GEN-AFF は別前件である。よってこれは強い前件を持つ機構に留まり、現時点の被覆は空である。

ここで pure roof の直積性を扱う `SPLIT-NULL` と、相対拡大の section を扱う `(H-SPLIT)` を混同してはならない。前者でも全面的な盲目性には (MCOV) が要り、後者では通常 section より強い同変 section が要る。

`(H-SPLIT)` の広い族化が立たなかった場合の有限側行動は、本キャンペーン C5 で既に実行した。真に非分裂な `[16,7,3]` と `[16,8,4]` を構成し、緩和 detector で撃った結果は全 orbit 972 / missing 0 だった。ただしこれは陰性測定である。次の分岐は次の二択になる。

- B 側: 非分裂 isolated 細分について、\(C_tZ\subseteq\operatorname{Im}A_t\) を base-change 安定かつ roof 一様に証明する。
- 有限排除側: C5 の kernel の isolatedness を先に確定し、緩和していない source generation と full reduction を測る。さらに \(p=2,3\)、非半単純、非可換の bounded family を事前登録して同じ gate を掛ける。

現時点で最有力の B 側定理候補は、`COCYCLE-ABSORB-137` の数値等式そのものではなく、その背後にある写像包含

\[
C_t\bigl(Z^1(\Gamma,V)\bigr)\subseteq\operatorname{Im}A_t
\]

を module、marking、roof、base change に自然な chain homotopy として示すことである。これが交叉と多段合成で保たれ、GEN-AFF も一様に供給されれば、一段半単純という現制限を越える。現在はその自然変換も保存則も無いので、格は**機構候補**である。

block-diagonal 重複度についてだけは、各成分の包含を直和すれば総包含が従う。この小さな族化は紙の線型代数で可能だが、同じ既知成分の直和しか覆わず、混合作用・非半単純性・多段を全て外す。そのため cofinality を実質的には進めない。C1/C2 の有限結果をこれ以上広く読む根拠はない。

### 7.6 現時点で本当に未被覆の範囲

1. **MCOV 不明又は破れの直積 roof**。`SPLIT-NULL` だけでは全面 972 にならない。
2. **entangled / Goursat mixed roof**。共通商非自明、両因子非自明の一般形に盲目性定理が無い。
3. **非分裂 isolated 相対拡大**。群拡大の有限例は得たが、isolated family とその全射定理が無い。
4. **非可換核**。便 134 は一窓の測定に留まる。
5. **modular 非自由核**。\(p=3,\tau\)-非自由と \(p=2,\theta\)-非自由は各一設定を測っただけである。
6. **非半単純・混合標識作用・mixed-primary**。C3 の三 class 以外は canonical universe すら無い。
7. **多段 / 塔**。一段命題を交叉後の新基底へ移す base-change 安定性が無い。
8. **S4 側深化と両側同時深化**。bounded target list と族正規形が無い。

そして上の各範囲を個別に覆うだけでも十分ではない。最後に

\[
\forall K\in\mathcal I_M\ \exists L\subseteq K:\quad
L\text{ は上記の全射族のいずれかに属する}
\tag{COFINAL-NORMAL-FORM}
\]

という **任意の isolated 細分を覆われた正規形へさらに細分する定理**が要る。現在はこの比較定理が無い。cofinal までに必要なものを一言でまとめると、

> **(a) 非分裂・非可換・modular 非自由・多段を含む base-change 安定な一様吸収定理、(b) split 枝の MCOV 族判定、(c) S4/mixed 枝を含む COFINAL-NORMAL-FORM の三本。**

である。現被覆の合併が cofinal だという証拠は無く、B 側の最終 1 ビットは UNKNOWN のままである。

### 7.7 COMPACT 以外の B 側経路

論理的な経路は三つあるが、現在実装可能又は証明済みの第二経路は無い。

1. **整合する逆極限元の直接構成。** \(g_M\in GT(M)\setminus A\) を一つ固定し、cofinal な下降 isolated chain \((K_j)\) 上で
   \[
   g_{j+1}\longmapsto g_j,\qquad g_0=g_M
   \]
   を満たす \(g_j\in GT(K_j)\) を全深度で作る。各深度の charming/hexagon/SURJ と遷移整合性を一様に証明すれば、Thm 5.2 から逆極限元を得る。個々の深度で像 972 だったことだけでは、同じ元を選び続ける整合性を与えない。必要品は cofinal chain、全遷移の lift section 又は Mittag--Leffler 条件、全深度一様式である。
2. **大域不変量又は像下界。** \(\widehat{GT}_{\rm gen}\to GT(M)\) の像が 324 元を越えること、又は \(A\) の外へ出ることを、有限窓ごとの全射とは別の functorial invariant で示す。候補は mod-3 deformation class、連続 cohomology class、あるいは coordinate image が \(A\) では満たせない群論的性質である。現台帳にはその invariant も、有限位相群へ積分する定理も無い。接空間の非零だけでは profinite 元の存在にならない。
3. **変形・コホモロジーからの直接構成。** 実際の算術像の \(M\)-成分が \(A\) なので、\(A\) 外の元を実 Galois 元として作ることは定義上できない。可能なのは、算術起源の deformation 理論等を用いて **generic 側**に新しい profinite 元を積分し、その \(M\)-像が \(A\) 外だと示す経路である。これは一様な有限窓計算を迂回するが、実質的には井原型の主問題を直接解く強さを要する。現在その積分・収束・有限像同定のいずれも無い。

従って、概念上は直接逆極限構成と変形論経路があるものの、現時点で荷重を持つのは定理 COMPACT に向けた cofinal な族定理路だけである。本追補は新しい B 側証明を得たのではなく、既走測定を 0 と正しく勘定し、必要な三本の族定理を特定した。

`EXHAUSTED` は「現在の道具で prospective に有限化できた C0--C15 の在庫が尽きた」という意味に限る。cofinality の数学、上記の新技術、B 側の最終判定が尽きたという意味ではない。

CAMPAIGN_STATUS: EXHAUSTED
