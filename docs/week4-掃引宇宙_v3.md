# 掃引宇宙 v3 — `U-E2-nm5-r2-2026-07-26`(有限反証バッテリー)

2026-07-26 起草: Claude(数学者レイヤー・Opus 5)。**司令塔 委嘱 10 §3**。
便 13 **F15–F18 / P148 / P149 / P150 / W109 / W110 / W111 / W112** の修理リストに一つずつ答えた**再登録版**。

> **凍結の宣言(絶対).** 既存 ID **`U-E2-nm5-2026-07-26`(v2 §4.2 ①)は事前登録記録として凍結**する。上書き・削除・射程変更は**しない**。本稿は**新 ID** による再登録であり、v2 の宇宙を置き換えない。`U-E2-metab-2026-07-26`(②)と `U-E2-fin-2026-07-26`(③)も凍結のまま据え置く(②の後継作業は `docs/week4-E19二系統化指示書_v1.md`)。

依存: `docs/week4-E2作戦_v3.md`(v3 本体)・**`docs/命題_E22三段判定_v1.md`(判定の数学的正本)**・`sol/sol_reply_13_graded.md`・`sol/裁定_13_graded.md`。

---

## 0. この宇宙は何であって、何でないか(W110/W112 の先取り)

| | |
|---|---|
| **これは** | **有限反証バッテリー**。事前登録した **$j=1..6$、$m=0..63$ の 384 系**について、普遍 class-5 対象の合同商における同時可解性を全数判定する |
| **これでない** | 定理ゲートではない。全件通過は「全 $j$」「全 $m$」「class-5 非 metabelian 層全体」のいずれの証明でもない |
| **通過の読み** | 「この有限化と二つの lift 方程式が正しいという条件の下で、登録した 384 系が可解」**まで**。**class 6 以上へ狩場を移す理由にしない**(W110) |
| **失敗の読み** | まず `universal_class5_congruence_obstruction`。**E15 の反証ではない**(W112)。反証と呼ぶには、その合同対象を実際の有限許容 $P=PB_3/N$($c\in N$)へ実現し、該当 charming $m$ について `m_missing` 証明書を付ける必要がある |
| **前提の明示** | 判定の数学的正本は `docs/命題_E22三段判定_v1.md` の**定理 E22′**。この定理が誤っていれば結果は全て無効 |

---

## 1. 対象の定義 — 非可換 $A$ の有限化(F15 / W109 への応答)

### 1.1 なぜ $A\otimes\mathbb Z/2^j$ が使えないか(便 13 F15 の追認)

$A:=\gamma_2/\gamma_6$ は**非可換**(class 2)なので、テンソル積 $A\otimes\mathbb Z/2^j$ という対象は**定義されない**。また Hall 座標を単純に全て $\bmod\,2^j$ に落とすことも**できない**: class-2 collection に現れる $\binom a2$ は
$$ \binom{a+2^j}2-\binom a2 = 2^ja+\binom{2^j}2 = 2^ja+2^{j-1}(2^j-1) $$
であり、$2^{j-1}(2^j-1)\not\equiv0\pmod{2^j}$ なので**代表元依存**が起きる。**v2 §4.2 ① の対象定義は無効**であり、これが NO-GO の直接の理由である。

★ ただしこの計算は、**中心座標だけを $\bmod\,2^{j-1}$ に落とせば整合する**ことも同時に示している。以下の定義はそれを群論的に正しく実現したものである。

### 1.2 正本の有限化 — verbal(特性)冪商

> **定義 1.1.** $j\ge1$ に対し
> $$ \mho_j(A):=\bigl\langle\,a^{2^j}\ :\ a\in A\,\bigr\rangle,\qquad \boxed{\ A_j:=A/\mho_j(A)\ } $$
> $\mho_j$ は verbal subgroup ゆえ **$A$ の特性部分群**、したがって $\sigma,\theta$ は $A_j$ に降りる。さらに $\mho_j(A)$ は $P^{(5)}=F_2/\gamma_6$ で正規なので $P_j:=P^{(5)}/\mho_j(A)$ も定義でき、$[P_j,P_j]=A_j$。

> **命題 1.2(構造).** $A$ が class 2、$C=[A,A]$ と $\bar A=A/C$ がともに自由アーベルであるとき、$j\ge1$ について
> $$ \text{(i) }\ \overline{\mho_j(A)}=2^j\bar A,\qquad \text{(ii) }\ \mho_j(A)\cap C=2^{j-1}C . $$
> したがって $A_j$ は
> $$ 1\longrightarrow C_j:=C/2^{j-1}C\longrightarrow A_j\longrightarrow \bar A_j:=\bar A/2^j\bar A\longrightarrow 1 $$
> という中心拡大であり、$P^{(5)}$ の場合は
> $$ \bar A_j\cong(\mathbb Z/2^j)^{10},\qquad C_j\cong(\mathbb Z/2^{j-1})^2,\qquad \lvert A_j\rvert=2^{12j-2}. $$

**証明.** (i) は明らか。(ii) $\supseteq$: class 2 の Hall–Petrescu $(ab)^n=a^nb^n[b,a]^{\binom n2}$ より、$n=2^j$ 冪が生成する部分群は $[b,a]^{\binom{2^j}2}$ をすべて含むので $\binom{2^j}2C=2^{j-1}(2^j-1)C$ を含み、また $z\in C$ に対し $z^{2^j}=2^jz$ ゆえ $2^jC$ も含む。$\gcd\bigl(2^{j-1}(2^j-1),\,2^j\bigr)=2^{j-1}$($2^j-1$ は奇数)なので $2^{j-1}C\subseteq\mho_j(A)$。
$\subseteq$: $g=a_1^{n}\cdots a_k^{n}\in C$($n=2^j$、逆元は $(a^{-1})^n$ に吸収)とする。$\bar A$ での像は $n\sum\bar a_i=0$ で $\bar A$ は自由なので $\sum\bar a_i=0$、すなわち $a_1\cdots a_k=:z\in C$。$a^nb^n=(ab)^n[b,a]^{-\binom n2}$ を $k$ について反復すると($\binom n2C$ は部分群なので各段の補正が吸収される)
$$ a_1^n\cdots a_k^n=(a_1\cdots a_k)^n\cdot c=z^n\cdot c,\qquad c\in\tbinom n2C, $$
よって $g\in2^jC+2^{j-1}(2^j-1)C=2^{j-1}C$。∎

> **★ 選択理由(なぜこの定義か)**
> 1. **特性である**(verbal)。$\sigma,\theta$ の降下が**証明つき**で保証される — F15 が要求した `action descent certificate` は命題 1.2 の (i)(ii) がそれにあたる。
> 2. **§1.1 の代表元依存が起きない**。中心が自動的に $2^{j-1}$ で落ちるので、collection の $\binom a2$ 項が整合する。
> 3. **Hall 正規形の一意性が保たれる**: $A_j$ の元は $\bigl(\bar a\in(\mathbb Z/2^j)^{10},\ z\in(\mathbb Z/2^{j-1})^2\bigr)$ で**一意**に表される(中心拡大の section)。
> 4. **他の候補との比較**: (a) 座標を一律 $\bmod2^j$ にする素朴案 → §1.1 で破綻。(b) $\bar A$ を $2^j$、$C$ を $2^j$ で落とす案 → そのような部分群は存在しない(§1.1 の計算がその不存在の証明)。(c) $\mathbb Z_2$-Mal'cev 座標上の普遍恒等式 → **別宇宙**であり、有限許容対象の E15 とは同一でない(F15 の警告)。本宇宙は (c) を採らない。

> **⚠ $j=1$ は退化(必ず明記して集計する).** $C_1=0$ なので $A_1$ は**基本アーベル**(階数 10)。非可換性がまったく効かないので、$j=1$ は**可換 control** として扱い、live discovery に混ぜない。実質的な層は $j=2,\dots,6$ の 5 層 × 64 = **320 系**、$j=1$ の 64 系は control。

### 1.3 事前登録する基底と section(正本・以後変更しない)

**$A$ の Hall 基底(順序固定)**:
$$ w;\ \ p,q;\ \ r_1,r_2,r_3;\ \ t_1=[r_1,x],\,t_2=[r_1,y],\,t_3=[r_2,y],\,t_4=[r_3,y];\ \ t_5=[w,p],\,t_6=[w,q]. $$
**$\bar A$ の基底(10)**: 上の $w,p,q,r_1,r_2,r_3,t_1,t_2,t_3,t_4$ の像。`metab.mjs` の $c=5$ モデルの単項式基底 $S^aT^b$($a+b\le3$)と、辞書 $w=1,\ p=S,\ q=T,\ r_1=S^2,\ r_2=ST,\ r_3=T^2$、$t_i\leftrightarrow$ 3 次単項式 で**一対一に対応させる**(対応表は証明書に載せる)。
**$C$ の基底(2)**: $t_5,t_6$。
**canonical section** $s:\bar A_j\to A_j$: Hall 正規形
$$ s(\bar a)=w^{a_1}p^{a_2}q^{a_3}r_1^{a_4}r_2^{a_5}r_3^{a_6}t_1^{a_7}t_2^{a_8}t_3^{a_9}t_4^{a_{10}},\qquad 0\le a_i<2^j $$
(**この順序と代表元区間を正本とする**)。

### 1.4 二つの中心欠損(F14/P147 の登録)

定理 E22′(`命題_E22三段判定_v1.md` §3)に従い、**登録する量は二つの中心値写像**である:
$$ q_\theta(\bar f)=\theta(s\bar f)\,s\bar f\ \in C_j,\qquad q_N(\bar f)=E_m\,\sigma^2(s\bar f)\sigma(s\bar f)\,s\bar f\ \in C_j . $$
中心補正の像は $\Lambda(z)=\bigl((1+\theta)z,\ \mathcal N_C z\bigr)$、障害群は $\mathrm{Ob}_j=(C_j\times C_j)/\operatorname{im}\Lambda$。

> **★ 事前に登録しておく構造的予測(系 E22.6).** $\mathcal N\vert_C=0$ なので
> $$ \operatorname{im}\Lambda=\langle(t_5+t_6,\,0)\rangle\cong\mathbb Z/2^{j-1},\qquad \lvert\mathrm{Ob}_j\rvert=2^{3(j-1)} . $$
> すなわち **$q_N$ は中心補正で一切修正できず、厳密に $0$ でなければならない**。
> **これは実装が最初に再現すべき構造事実であり、GAP 側が独立に $\mathcal N\vert_{C_j}=0$ を確認できなければ即停止**(§4 の停止規則 S-3)。

---

## 2. 事前登録表

| 項目 | 事前登録値 |
|---|---|
| **universe_id** | `U-E2-nm5-r2-2026-07-26` |
| **対象(普遍側)** | $P^{(5)}=F_2/\gamma_6$、$A=\gamma_2/\gamma_6$(Hirsch length 12、class 2、$C=[A,A]$ は階数 2・中心) |
| **有限化** | $A_j=A/\mho_j(A)$、**定義 1.1**。$j=1,\dots,6$($j=1$ は可換 control) |
| **$m$ の範囲** | $m=0,\dots,63$ |
| **系の総数** | $6\times64=\mathbf{384}$(うち live $=5\times64=320$、control $=64$) |
| **判定** | 定理 E22′ の三段判定(① 線型段 ② 線型障害段 ③ 二次段) |
| **列挙対象** | 列挙は $K=\ker(1+\bar\theta)\cap\ker\bar{\mathcal N}\le\bar A_j$ の**全元**。$\lvert K\rvert=\prod_i n_i$($n_i$ = invariant factors) |
| **規模の見積り** | 線型段: $20\times10$ 級の $\mathbb Z/2^j$ 上の SNF。二次段: $\lvert K\rvert$ の全数走査。$\lvert K\rvert$ が $10^7$ を超える $(j,m)$ は **cap 対象**として先に列挙する |
| **二系統** | route N(node: Hall collection 多項式 + 二欠損)/ route G(GAP: 独立な PC presentation 上の**直接群演算**)。**二次表を共有しない**(F18) |

### 2.1 cap の単位(F18 — 単位を明示的に固定)

| キー | 値 | 意味 |
|---|---|---|
| `wall_seconds_per_pair` | **120** | 一つの $(j,m)$ の判定(線型段+二次段の合計)。route ごとに個別計測 |
| `wall_seconds_per_route` | **1800** | 一つの route(node または GAP)の $j$ 一つぶん(= 64 個の $m$) |
| `wall_seconds_universe_total` | **7200** | 宇宙全体(両 route 合計) |
| `heap_bytes_per_process` | **2 GB**(`gap.ps1 -o 2g` / node `--max-old-space-size=2048`) | `RAM 8GB constraint` に従う |
| `enumeration_cap_per_pair` | $\lvert K\rvert\le 2^{24}$ | 超えたら全数走査を行わず `status="cap_exceeded"` |

**cap 規則(厳守)**
- **S-1**: いずれかの cap に触れたら、その $(j,m)$ は `status="cap_exceeded"` = **UNKNOWN**。**可解とも不可解とも書かない。**
- **S-2**: cap に触れた $(j,m)$ を**全て列挙**して証明書の `unprocessed_pairs` に書き、**宇宙全体の verdict を `partial`** にする。「320/320 通過」とは書けない。
- **S-3**: **cap の事後引き上げは禁止**。引き上げが必要なら**新 ID で再登録**する(v3 → v4)。

---

## 3. 全数性(completeness)の証明書 — F17/W111 への応答

「$K$ の全元を走査した」を**再構成可能に**証明する。hash だけでは不可。

### 3.1 パラメータ領域の確定

1. 線型段の係数行列 $M_j(m)$($\mathbb Z/2^j$ 上、$20\times10$)と右辺 $b_j(m)$ を出力(content hash + **基底順序**+ **modulus** つき)。
2. $\mathbb Z$ 上に持ち上げて **canonical Smith 標準形** $U M V=D$ を計算し、$U,V$ を**保存**。postcondition:
 - $\lvert\det U\rvert=\lvert\det V\rvert=1$、
 - $D$ が対角で $d_i>0$ かつ $d_i\mid d_{i+1}$、
 - $UMV=D$ の再乗算一致。
3. $\mathcal L\ne\emptyset$ の判定と $\bar f_0$ の復元。$K$ の生成元 $e_i$ と位数 $n_i$ を $V$ と $D$ から構成し、
 $$ \lvert K\rvert=\prod_i n_i $$
 を宣言する。**根拠は $U,V,D$ の postcondition**(2 の三点)であって、求解器の内部主張ではない。
4. **独立検査**: checker は $e_i$ が実際に $(1+\bar\theta)e_i=0$、$\bar{\mathcal N}e_i=0$ を満たすこと、$n_ie_i=0$、かつ $\{e_i\}$ が生成する部分群の位数が $\prod n_i$ であることを**自前で**再計算する。

### 3.2 二次表と mass check

`docs/命題_E22三段判定_v1.md` §6 の (6.1) に従い、
$$ \omega_0,\qquad F(e_i)\ (i=1..r),\qquad \pi B(e_i,e_j)\ (i\le j) $$
の**全値**($\mathrm{Ob}_j$ の座標)を保存する。これで $F$ の全値が再構成できる。

**必須の自己検査 (6.2)**: 各 $i$ について $\ n_iF(e_i)+\binom{n_i}2\pi B(e_i,e_i)=0$ in $\mathrm{Ob}_j$。**一本でも FAIL なら結果は無効**(停止)。

**mass check**: 値ごとの重複度表 `value_multiplicity_table` を出し、
$$ \sum_{v\in\mathrm{Ob}_j}\mathrm{mult}(v)=\prod_i n_i=\lvert K\rvert $$
を検査する。**target 非所属**は「$\mathrm{mult}(-\omega_0)=0$」として提示する。

### 3.3 不可解性証明書(二種)

**(A) 線型段が空** — `unsolvability_certificate`(便 12 F13 の形式を維持):
```json
{ "claim": "linear_stage_empty",
  "method": "left_kernel_mod_prime_power/v1",
  "modulus": 64,
  "matrix_shape": [20,10],
  "basis_order_Abar": ["w","p","q","r1","r2","r3","t1","t2","t3","t4"],
  "relation_row_order": ["theta_1..theta_10","norm_1..norm_10"],
  "matrix_content_hash": "...", "b_content_hash": "...",
  "dual_witness_y": ["..."],            // y*M = 0 (mod 2^j),  y*b != 0 (mod 2^j)
  "recheck": "y*M と y*b を独立に再計算" }
```
> **F17 の指示に従い、$\bar A$ の 10 座標と $C$ の 2 座標を混ぜない。行列の空間ごとに別欄で記録する。**

**(B) 線型段は非空だが全 lift が失敗** — `central_lift_obstruction/v2`(新設・P149):
```json
{ "claim": "linear_solutions_exist_but_none_lifts",
  "method": "central_quadratic_exhaustion/v2",
  "object": { "A_j_presentation_hash": "...", "section_convention": "Hall(w,p,q,r1,r2,r3,t1..t4), 0<=a_i<2^j",
              "Abar_j_invariants": ["2^j x10"], "C_j_invariants": ["2^(j-1) x2"] },
  "linear": { "f0": ["..."], "K_generators": [["..."]], "K_moduli": [ ... ],
              "K_order": 0, "snf": {"U_hash":"...","V_hash":"...","D":[...],
                                    "det_U":1,"det_V":1,"UMV_recheck":true} },
  "obstruction_group": { "Lambda_matrix": [[...]], "im_Lambda_generators": [["..."]],
                         "Ob_invariants": [ ... ], "pi_matrix": [[...]] },
  "quadratic_table": { "omega0": ["..."], "F_e": [["..."]], "piB": [["..."]] },
  "selftest_6_2": [0,0,0],                   // 全て 0 でなければ無効
  "exhaustion": { "parameter_domain_size": 0, "scanned": 0,
                  "value_multiplicity_table": {"...":0}, "mass_check": true,
                  "target": ["-omega0 の座標"], "target_multiplicity": 0 },
  "independent_recheck": "checker は群の積から theta(f)f と E_m N(f) を再計算する" }
```

**(C) 肯定側** — `solution_witness`:
- $f$ の **Hall 座標**(section 規約つき)、
- checker が**非可換群の積**として $\theta(f)f=1$ と $E_m\sigma^2(f)\sigma(f)f=1$ を直接再計算、
- **生成条件は別欄**(`generation` — torsion 解と混同しない。便 12 Errata 4 / W97)。

### 3.4 schema

`e2-sweep-cert/v3`(v2 からの**追加のみ**)。禁止事項は v2 §4.3 をすべて継承し、さらに:
- **`kernel_representatives_hash` / `form_values_hash` **だけ**で否定を宣言してはならない**(W111)。
- **`kernel_rank` を全数の根拠にしてはならない**($\mathbb Z/2^j$ は体でない)。
- **`verified` の語を使わない**(Lean 予約)。二系統一致は `cross-checked`、単系統は `candidate`。
- `A_finitization` 欄を新設し、`"mho_j"` と定義 1.1 への参照、$C_j$ の invariant factors を必ず書く。**`"tensor_Z_mod_2j"` は禁止値**。

---

## 4. 二系統の分離と停止規則(F18)

| route | 実装 | 独立性の担保 |
|---|---|---|
| **route N**(node) | $\bar A_j$ を `metab.mjs` の $c=5$ モデル(切断多項式)で、$C_j$ と二欠損を Hall collection 多項式で | 多項式代数 |
| **route G**(GAP) | $A_j$ の **PC presentation**(`PcGroupFpGroup`/`NilpotentQuotient` 経由)を独立に構成し、$\theta,\sigma,E_m$ を群自己同型として与え、**群の積そのもの**で $\theta(f)f$ と $E_m\mathcal N(f)$ を評価 | 群演算 |

**共有してはならないもの**: 二次表 $(F(e_i),\pi B(e_i,e_j))$、$\mathrm{Ob}_j$ の座標系、section の実装コード。

**照合の対象**
- 肯定: 全 $(j,m)$ について**少なくとも一つの witness $f$** を双方で直接代入。可能なら全 witness。
- 否定: `parameter_domain_size`、`mass_check`、`target_multiplicity=0` を双方で照合。
- 構造: $\lvert A_j\rvert$、$C_j$ の invariant factors、$\operatorname{im}\Lambda$ の生成元、$\lvert\mathrm{Ob}_j\rvert$。

**停止規則**
- **S-3**: GAP 側が $\mathcal N\vert_{C_j}=0$(系 E22.6)を再現できない ⇒ **即停止**(数学かモデルのどちらかが誤り)。
- **S-4**: 自己検査 (6.2) が一本でも FAIL ⇒ **即停止**、結果を出力しない(`fails>0` で非零終了)。
- **S-5**: route N と route G の `Ob_invariants` または可解性 boolean が食い違う ⇒ **即停止**。
- **S-6**: control($j=1$、可換層)で不可解が出る ⇒ **実装バグ**。$j=1$ では $A_1$ が可換なので定理 E9′ の class-5 版が使えるか要検討 — **不可解が出たら停止して数学者へ差し戻す**。

---

## 5. 事前登録した両方向の読み(W110/W112 遵守)

### 5.1 全件可解だった場合

> **書いてよい**: 「有限化 $A_j=A/\mho_j(A)$($j=1..6$)と $m=0..63$ の登録 384 系すべてで、二つの lift 方程式は同時可解である(二系統一致)」。
> **書いてはならない**: 「全ての $j$」「全ての $m$」「class-5 非 metabelian 層は安全」「狩場を class 6 へ移す」。**通過を class 6 移動の理由にしない**(W110)。
> **次の一手**: (a) $j$ を上げるのではなく、**具体的な有限許容 $P$**(charming $m$ つき)への実現へ進む。(b) $\lvert K\rvert$ と $\lvert\mathrm{Ob}_j\rvert$ の $j$ 依存を見て、二次写像 $F$ が全射に近いのか偶然なのかを判定する材料を残す。

### 5.2 一件でも不可解だった場合

> **書いてよい**: `universal_class5_congruence_obstruction`。すなわち「普遍 class-5 対象の合同商 $A_j$ において、$m$ に対する同時解が存在しない」。
> **書いてはならない**: 「E15 は反証された」(W112)。
> **反証に必要な追加**: (i) その $A_j$ を $[P,P]$ にもつ**有限許容対象** $P=PB_3/N$($N\in\mathrm{NFI}_{PB_3}(B_3)$、$c\in N$)の構成、(ii) 該当 $m$ が **charming** であることの確認、(iii) `m_missing` 証明書。
> **注意(実現ギャップの明示)**: $A_j$ が有限でも $P^{(5)}/\mho_j(A)$ は**無限**である($P/\gamma_2\cong\mathbb Z^2$ が残る)。有限許容対象を作るには $\bar X,\bar Y$ の位数も落とす必要があり、その商で $A_j$ がそのまま生き残る保証はない。**この段は【GAP-E20】と合流する。**
> **次の一手**: 障害ベクトル $-\omega_0\notin F(K)$ を出力し、$\mathrm{Ob}_j$ のどの成分で外れているかを記録($q_N$ 側か $q_\theta$ 側か)。系 E22.6 により **$q_N$ 側で外れる可能性が構造的に高い**。

---

## 6. 作業指示

> **W-r2-1(implementer・最優先)**: route N の実装。§1.2–§1.4 の対象定義、定理 E22′ の三段判定、§3 の証明書。**否定側は `central_lift_obstruction/v2` を必須**。自己検査 (6.2) と系 E22.6 の再現を**先に**通し、FAIL なら本走査へ進まない(非零終了)。
> **W-r2-2(implementer)**: route G の実装(GAP・独立 PC presentation・群演算で直接評価)。二次表を共有しない。
> **W-r2-3(falsifier)**: 本稿の事前登録への反証前哨。特に (a) 定義 1.1 の有限化が「$\sigma,\theta$ の降下」以外の落とし穴を持たないか(**命題 1.2 の証明を独立に検分**)、(b) §3 の全数性証明書が独立再構成可能か、(c) §5 の両方向の読みが空虚テストになっていないか、(d) $j=1$ control の扱い。
> **W-r2-4(司令塔経由・Sol へ)**: 定理 E22′ と系 E22.6・命題 1.2 の相互監査。**特に「section cocycle の寄与が $\operatorname{im}\Lambda$ で消える」(命題 E22.3)は便 13 F14 への直接回答なので、独立検分を求める。**

---

## 7. 状態札

| 項目 | 札 |
|---|---|
| 定義 1.1 / 命題 1.2(有限化) | **紙上証明**(Opus 単独・Sol 未監査) |
| 判定の数学的正本(定理 E22′) | **紙上証明**(Opus 単独・Sol 未監査) |
| 系 E22.6($\mathcal N\vert_C=0$・$\lvert\mathrm{Ob}_j\rvert=2^{3(j-1)}$) | **紙上証明**(手計算)。GAP 側の独立再計算を停止規則 S-3 に組み込み |
| 掃引結果 | **未実行**。実行後の札は route N/G 一致で `cross-checked`、単系統なら `candidate` |
| verified(Lean) | 一つもない |
