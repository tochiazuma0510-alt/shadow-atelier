# D972 Phase 2b — 非分裂 $2^6\!\cdot\mathrm{PSL}(2,8)$ 窓 実行報告 v1

日付: 2026-08-13。実験 ID `PH2B-NS64-v1.1`。旧 product family に PH2-VOID を先に適用し、別構造の isolated 窓だけを測った。

## 1. 設計判断

### 1.1 PΓL route

$N_{S_9}(P)=\mathrm{P\Gamma L}(2,8)$ は算術 monodromy として現れるが、それだけでは純 kernel の包含 $K\subseteq M$ も新しい $PB_3$ 商も与えない。従って $N_{S4}$ の自動的な refinement とは扱わず、今回の候補には選ばなかった。この route の不存在は主張しない。

### 1.2 選んだ候補

GAP perfect-groups library の

```text
PerfectGroup(32256,2)
label = L2(8) N 2^6
```

を $E$ とした。ライブラリの次数 72 coset action を再構成し、$V\cong C_2^6$ と $E/V\cong P=\mathrm{PSL}(2,8)$ を使う。固定標識は

```text
S = accbxbccb
T = cacaccwb
W = S*T^-1
X = W^2
Y = S^-1*X*S
```

で、位数は $2,3,9,9,9$、$\langle X,Y\rangle=E$ であった。

## 2. 実行順序

### 2.1 規模ゲート

像を作らない preflight を先に実行した。

\[
|E|=32256=64\cdot504,
\quad |G_9\times E|=94{,}058{,}496,
\]

候補 hexagon scan 上限は $6|E|=193{,}536$、置換次数 72、hard timeout 900 秒とした。preflight cert の `measurement_performed=false`, `reduction_image_formed=false` を checker が再確認した。

### 2.2 事前登録

`d972_phase2b_nonsplit_prereg_v1.md` で候補・標識・ゲート順・スペクトル $\{324,972\}$・分岐を固定した。engineering probe が先行していたので

```text
engineering_probe_before_freeze = true
preregistration_blind = false
```

と明記した。

G5 の最初の二実行は strong presentation の非一意性を文字列一致として扱ったため、raw boolean が `false`、`raw_image_size=null` のまま測定前に停止した。そこで、候補・スペクトルを変えず `d972_phase2b_nonsplit_prereg_v1_1.md` を先に固定し、実行時に有限置換群から再生成する strong presentation を使う方法へ限定修理した。

### 2.3 測定前 G0–G5

| gate | raw receipt |
|---|---|
| G0 | $|E|=32256$, degree 72 |
| G1 | $V\triangleleft E$, $|V|=64$, elementary abelian、$|E/V|=504$、標識付き $P$ |
| G2 | $E$ perfect、$V$ 既約、512 lift 対すべて kernel 非自明、非分裂、PH2-VOID 適用 `false` |
| G3 | $G_9$ 可解・$E$ perfect より共通非自明商なし、source 純商 $G_9\times E$ |
| G4 | source shadow 432 個、非空 |
| G5 | 432 個すべて settled、$N_E$ isolated、従って $K^{(9)}\cap N_E$ isolated |

G2 の詳細は、位数 2 lift 8 個と位数 3 lift 64 個の全 $8\cdot64=512$ 対が $V$ と非自明に交わること、63 個の非零 $V$ 元の normal closure がすべて位数 64 であること、$[X,Y]$ の normal closure が位数 32256 であることから成る。

列挙の前に $\theta:X\mapsto Y,Y\mapsto X$ と $\tau:X\mapsto Y,Y\mapsto(XY)^{-1}$ を Cayley graph 上で矛盾なく構成した。従って pure kernel $N_E$ は $B_3$ の作用で不変である。さらに標識付き商 $E/V\cong P$ は既登録 $N_{S4}$ 商と一致するので $N_E\subseteq N_{S4}$ であり、$E\to P$ が今回の reduction を与える。

$G_9\times E$ 自体は直積だが、第二因子 $E$ が非分裂拡大であり $(\text{可解})\times P$ ではない。従って旧 PH2-VOID の「dihedral と P が完全分離」という条件には戻らない。

## 3. source scan と isolatedness

source scan の raw counters は

```text
candidate_total = 193536
h10_fail       = 190128
h11_fail       = 2976
generation_fail= 0
shadow_total   = 432
```

で、帳尻恒等式は成立した。producer は実行時 strong presentation を各像 $(X',Y')$ に評価し、432 個を settled とした。固定 10 語も全 432 個で単位元となった。

helper 非共有 checker は SymPy を使わず、各 $(X',Y')$ について domain Cayley graph と image Cayley graph を同期 BFS した。その結果

```text
well_defined = 432 / 432
bijective    = 432 / 432
```

を直接再計算した。これにより G5 は producer の presentation algorithm だけに依存しない。

## 4. G5 後の raw 測定

$E\to E/V\cong P$ の target は $N_{S4}$ の 54 shadow である。

| quantity | raw integer |
|---|---:|
| source $E$ shadows | 432 |
| source roof shadows $18\cdot432$ | 7776 |
| target $N_{S4}$ shadows | 54 |
| reduction の candidate shadow 像 | 54 |
| target roof shadows $18\cdot54$ | 972 |
| $|\operatorname{Im}R_{K^{(9)}\cap N_E,M}|$ | **972** |

54 target keys はすべて像に含まれ、reduced key 集合は target key 集合と一致した。

凍結分岐に従い

```text
raw_image_size = 972
status = UNKNOWN
candidate_exhausted = true
finite_depth_B_type_recognition = false
```

と記録する。この候補では 324 側の有限 certificate は得られず、972 から B 型を認定しない。結果は次候補を探索できるという境界までである。

## 5. 再現と証明書

```powershell
python search/d972_phase2b_gate_v1.py --hard-timeout-seconds 120
python search/check_d972_phase2b_gate_v1.py
python search/d972_phase2b_nonsplit_v1.py --hard-timeout-seconds 900
python search/check_d972_phase2b_nonsplit_v1.py --hard-timeout-seconds 900
```

- `search/certs/d972_phase2b_gate_v1_20260813.json`
- `search/certs/d972_phase2b_gate_v1_check_20260813.json`
- `search/certs/d972_phase2b_nonsplit_v1_20260813.json`
- `search/certs/d972_phase2b_nonsplit_v1_check_20260813.json`
- 対応する producer/checker checkpoint 4 本

producer/checker の一致は cross-checked。Lean certificate は無い。$u,c$、封印 K5、既登録量は非接触である。
