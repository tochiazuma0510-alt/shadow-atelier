# 返書 129 — `[vN-1]` 在庫走査と G₃ 橋の規模ゲート

日付: 2026-08-13  
仕様正本: `docs/notes/ab_instrument_redesign_v2.md` (`f2296400`)  
実行時 HEAD: `8350656364041b50f94e1715426d785624751f7f`

## 0. 到達点

便 129 の §0、§1.1–§1.4、§2 を順に処理した。

1. 凍結した有限在庫では、テンソル型 \(V\) を持つ行は **0** だった。これは task 125 の明示4行、83 marked records、atlas で isolated と明記された行を対象とする値であり、task 125 §1.1 の無限 dovetail の完走や全 isolated 窓での非存在は含意しない。
2. \(P=\operatorname{PSL}(2,8)\) の \(\mathbf F_3\) 上最小非自明加群次元は **7**、\(G_3\) 側は **1** である。従って最小テンソル候補は \(\dim V=7\)、
   \[
   |E|=54\,432\cdot3^7=\mathbf{119\,042\,784}.
   \]
3. 現行 producer は群要素を permutation tuple として全 materialize する。faithful な次数 \(d\) は \(|E|\le d!\) より \(d\ge12\)。次数12 tuple 一個の CPython 生値 136 bytes だけでも、最小 \(E\) の全要素に対し **16,189,818,624 bytes = 15.078 GiB** となり、8 GiB を越える。set table・点 object・屋根側はこの下限に含めていない。
4. よって到達段は **2**。\(E\) の構成、BLIND-vNext の機械ゲート、P-vN-1 の実体化、648対の rigidity 測定は行っていない。`raw_image_size=null`、状態は **UNKNOWN** である。

## 1. §0 の型固定

本走では次を区別した。

- \(G_3=PB_3/K^{(3)}\)、\(|G_3|=108\)、\(|G_3^{\rm ab}|=4\)。
- \(P=PB_3/N_{S4}\cong\operatorname{PSL}(2,8)\)、\(|P|=504\)。
- \(E=PB_3/N_E\) と \(V=\ker(E\to P\times G_3)\)。
- \(\theta,\tau\) は marked pure quotient に誘導される作用であり、外側商 \(B_3/PB_3\cong S_3\) の元とは読んでいない。SPLIT-TWIN の外側 \(S_3\) も入力していない。

従って G-vN-0 が true なら \(E\to P\times G_3\) があり、\(|E|\) は少なくとも \(504\cdot108=54\,432\) である。この安価な位数条件を83記録と atlas に先に適用した。

## 2. `[vN-1]` 有限在庫走査

### 2.1 宇宙の事前固定

| 層 | 生記録数 | 今回評価した範囲 |
|---|---:|---|
| task 125 明示 refinement | 4 | \(M=K^{(9)}\cap N_{S4}\)、\(K^{(27)}\cap N_{S4}\)、\(K^{(36)}\cap N_{S4}\)、累積 \(K^{(108)}\cap N_{S4}\) |
| WIN-CNOTN 83 | 83 marked records | `wincnotn_v1` の帯 \((1000,2000]\)。isolated の成否に依存しない位数 obstruction を評価 |
| atlas CSV | 189 | 現 CSV で `isolated=TRUE` が明記された W-5 一行。残る188行は isolated typing が無いため別記 |
| 構造 control | 3 | \(K^{(3)}\cap N_{S4}\)、\(N_{S4}\)、\(K^{(3)}\) |

task 125 §1.1 は「全有限乗法表を dovetail する」という有効列挙の設計であり、有限時刻に完了する在庫表ではない。従って今回の `hit_count=0` をその無限宇宙へ拡張しない。

また、83件を一括して「isolated 83件」とは扱っていない。既存 deep15 の生値は15 records 中 `all_kernel_trivial=true` が3 records、isomorphism ID は `[1152,154161]`, `[1152,154163]` の2種である。残る68 records の isolated typing は今回の入力には無い。ただし全83件は次の位数 obstruction だけで G-vN-0 が false になる。

### 2.2 task 125 明示4行の生値

| \(l\) | \(|G_l|\) | \(|E|=504|G_l|\) | \(|V|=|G_l|/108\) |
|---:|---:|---:|---:|
| 9 | 2,916 | 1,469,664 | 27 |
| 27 | 78,732 | 39,680,928 | 729 |
| 36 | 23,328 | 11,757,312 | 216 |
| 108 | 629,856 | 317,447,424 | 5,832 |

各 \(G_l\) は可解で \(P\) と非自明共通商を持たず、task 125 cert の roof order も \(504|G_l|\) であるため、この4行では

\[
E\cong P\times G_l,\qquad V=\ker(G_l\to G_3)\subseteq G_l
\]

となる。従って \(P\) は \(V\) に自明に作用する。G-vN-3 は \(G_3\) 側の作用を測らずとも false である。

| 在庫行 | G-vN-0 | G-vN-1 | G-vN-2 | \(P\)-作用非自明 | G-vN-3 | tensor |
|---|---|---|---|---|---|---|
| \(K^{(9)}\cap N_{S4}=M\) | true | false | true | false | false | false |
| \(K^{(27)}\cap N_{S4}\) | true | true | true | false | false | false |
| \(K^{(36)}\cap N_{S4}\) | true | true | true | false | false | false |
| \(K^{(108)}\cap N_{S4}\) | true | true | true | false | false | false |

基準 \(K^{(3)}\cap N_{S4}\) は \(V=1\) なので G-vN-1 と G-vN-2 がともに false、\(N_{S4}\) 単独と \(K^{(3)}\) 単独は G-vN-0 が false である。

### 2.3 83 marked records と atlas の生値

83 records の \(B_3\)-商位数は **1,008 以上 1,998 以下**だった。G-vN-0 が true なら、その \(B_3\)-商は部分群 \(E\) を含み \(|E|\ge54\,432\) でなければならない。

| 層 | 記録数 | G-vN-0=false | tensor hit |
|---|---:|---:|---:|
| WIN-CNOTN | 83 | 83 | 0 |

この行は isolated 判定を仮定しない。

atlas CSV は189行で、`atlas_stats_survey_v2.md` の typing と現 CSV の note を合わせると、isolated が明記されたものは W-5 一行だった。W-5 は \(|PB_3/N|=1000\) なので G-vN-0=false、tensor hit は0。残り188行に G-vN-0/1/2/3 の値を創作していない。

以上より、**凍結有限在庫の tensor hit count は0**。未列挙の isolated refinement、将来の dovetail 項、atlas の typing 未登録行については UNKNOWN のままである。

## 3. `[vN-2]` 加群次元と規模

### 3.1 \(\dim V_P=7\) の二方向照合

producer は GAP 4.16.0 同梱 AtlasRep の次の三記録を読んだ。

- `L2(8), Characteristic 3` の最小次数 = 7。
- `L2(8), Size 3` の最小次数 = 7。
- characteristic 3 の表は `complete=true`。

checker はこの保存値を計算根拠にせず、次を再構成した。

1. Atlas 標準生成元
   \[
   (1\,2)(3\,4)(6\,7)(8\,9),\qquad
   (1\,3\,2)(4\,5\,6)(7\,8\,9)
   \]
   の閉包は位数504。
2. 一点安定化群は位数56、元の位数分布は \(\{1:1,2:7,7:48\}\)。その8元の正規部分群は \(2^3\)、位数7元は7個の非自明元を一軌道にする。
3. 非自明な \(P\)-加群の核は \(P\) の正規部分群なので、その表現は faithful。標数3では \(2^3\) の作用は \(\mathbf F_3\) 上で weight 分解し、\(C_7\) が7個の非自明 weight を巡回する。非自明 weight が一つあれば7個すべてが同じ正次元で現れるため \(\dim V_P\ge7\)。
4. 9点 permutation module の augmentation subspace を定数直線で割った7次元 heart を作り、**全2186非零ベクトル**について生成部分加群の次元を計算した。分布は `{7:2186}`。従って7次元上界も得る。

二経路の値はともに

\[
\boxed{\dim_{\mathbf F_3}V_P=7}
\]

である。Lean 証明書は作っていない。

### 3.2 \(G_3\) 側と位数表

\(|G_3^{\rm ab}|=4\) なので \(G_3\) は \(C_2\) 商を持ち、\(C_2=\mathbf F_3^\times\) を通じた1次元非自明加群を持つ。従って最小値は \(\dim V_{G_3}=1\)。

| \(\dim V_P\) | \(\dim V_{G_3}\) | \(\dim V\) | \(|E|=54\,432\,3^{\dim V}\) | \(|PB_3/(K^{(9)}\cap N_E)|\) | 現行 tuple 下限 |
|---:|---:|---:|---:|---:|---:|
| 7 | 1 | 7 | **119,042,784** | **[119,042,784, 3,214,155,168]** | **15.078 GiB** |
| 7 | 2 | 14 | 260,346,568,608 | [260,346,568,608, 7,029,357,352,416] | 38,794.662 GiB |

屋根位数は構成前には等号で固定できない。正確には

\[
\left|PB_3/(K^{(9)}\cap N_E)\right|
=\frac{|G_9|\,|E|}{|Q|},\qquad
108\le |Q|\le2916,
\]

ここで \(Q=PB_3/(K^{(9)}N_E)\) は実際の共通商である。\(Q=G_3\) なら上端 \(27|E|\)、\(Q=G_9\) なら下端 \(|E|\) になる。\(E\) 未構成の段階で \(27|E|\) を exact 値とはしていない。

### 3.3 規模による停止境界

既存の Phase 2 系は `Elements(...)` または Python の `closure(...)` で群要素を列挙し、`source_index` を全要素から作る (`search/d972_phase2_v1.g:37,167`; `search/d972_phase2b_nonsplit_v1.py:515,698`)。後者の要素表現は permutation tuple である。faithful な次数 \(d\) には \(|E|\le d!\) が必要で、最小 \(E\) では \(11!=39\,916\,800<|E|\le12!=479\,001\,600\)、従って \(d\ge12\)。

最小 \(E\) について、tuple object 本体だけの下限は

\[
119\,042\,784\times136
=16\,189\,818\,624\ {\rm bytes}
=15.078\ {\rm GiB}.
\]

これは set hash table、各点、\(V\) の追加作用点、屋根要素を除いた値である。物理8 GiB、`gap.ps1` heap cap 2 GiB の現設備では、既存列挙器を用いた次段を置かなかった。compact な extension／cohomology backend で要素全 materialization を避ける路の可否は今回評価しておらず、数学的構成不能とは主張しない。

## 4. 条件付き第3段以後

規模ゲートで止めたため、次はすべて未実行である。

| 項目 | 生値 |
|---|---|
| \(E\) 構成 | false |
| BLIND-vNext tensor machine gate | false（未走行） |
| P-vN-1 の実体化 | false |
| 凍結値 \(\{972,324\}\) | untouched |
| 162/486 の観測 | なし |
| blind measurement declaration | 未作成 |
| \(54\times12=648\) 対の形成 | false |
| rigidity 測定 | false |
| reduction image set | 未形成 |
| `raw_image_size` | `null` |
| 到達段 | 2 |
| 状態 | `UNKNOWN` |

従って \(\Theta_2\) が \(t_2\) から \(k\bmod3\) を決めるかについて値は無い。有限深度から B 型を認定する操作も行っていない。

## 5. producer / checker と GAP 起動記録

run ID は `g3bridge-inventory-20260813T042832Z`。

再現コマンド:

```powershell
python search/g3bridge_inventory_v1.py
python search/check_g3bridge_inventory_v1.py
```

両スクリプトは原子的 checkpoint と内部120秒 hard-timeout を持つ。最終 checkpoint は双方 `complete=true`。checker は producer module、SymPy、AtlasRep の保存最小次数値を使わず、tuple permutation と \(\mathbf F_3\) 線形代数を標準ライブラリだけで再構成した。`all_equalities_true=true`。

指定の GAP 経路も

```powershell
.\gap.ps1 search\g3bridge_moddim_v1.g
```

として試したが、GAP は script 読込前に signal pipe を作れず、Win32 error 5、process return code `3221225794` で終了した。従って GAP 生 cert／GAP checkpoint は生成されていない。この値を GAP 実走値とは数えず、producer は同じ GAP 配布物の AtlasRep/CTblLib 原表を読み、checker の独立再構成と照合した。

## 6. 非接触・型境界

- u/c: 非接触。
- 封印3量・sealed K5: 非接触。
- preregistered measurement quantities: 未読。
- P-vN-1: 仕様正本の二値を変更せず、実体化なし。
- \(B_3/PB_3\) の外側 \(S_3\) と pure quotient \(PB_3/N\) は全表で分離。
- global absence、compact backend の不能、未列挙在庫の陰性はいずれも主張しない。

## 7. 成果物 SHA-256

| 成果物 | SHA-256 |
|---|---|
| `search/g3bridge_moddim_v1.g` | `04b001cbb93eca551057350a1ebffc78cd45bf0e1685e104dc85f90cb284257e` |
| `search/g3bridge_inventory_v1.py` | `a3a9c0dd6841496e615e6f96b0a8cb4a603d4a1615cbc3a2a7b1a07dea0fbe9f` |
| `search/check_g3bridge_inventory_v1.py` | `e96c4caf17815077dda7710b97c98f6626fd759e44ea750f7d2ecac613ccf168` |
| `search/certs/g3bridge_inventory_v1_20260813.json` | `abe10cd5478598dbb13d26a2099e6028700bd4b2622dc814c32e7eff8bba0dac` |
| `search/certs/g3bridge_inventory_v1_checkpoint.json` | `1276d85167ad707e439113233adc129f28314f0bbb6c496366a040e654596ff6` |
| `search/certs/g3bridge_inventory_v1_check_20260813.json` | `638a00b14f1d4e9cac50c03818b819ea10a458c6d37f60895e9f8d6fa1d9317a` |
| `search/certs/g3bridge_inventory_v1_check_checkpoint.json` | `e781b647ee9b714ed2284a67ae9a72d698a908b10919aeabd27311a8ab9d9d66` |

git commit、push、workflow dispatch は行っていない。
