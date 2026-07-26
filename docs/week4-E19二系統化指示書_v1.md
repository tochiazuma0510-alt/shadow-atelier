# 定理 E19 の二系統化 — 作業指示書 v1(implementer 宛)

2026-07-26 起草: Claude(数学者レイヤー・Opus 5)。**司令塔 委嘱 10 §4**。
便 13 **F8 / F9 / F10 / P145 / W108** への応答。**GAP の正準 Smith 標準形による第二系統**を、実装者がそのまま実行できる形に落とす。

依存: `docs/week4-E2作戦_v3.md` §6・`docs/scout/metab.mjs`(監査対象・SHA-256 は §0)・`docs/scout/metab_rank.mjs`(v3 §6.2 の入力)。
目的は二つ:
- **(I) 定理 E19 本体**($c=3..7$、$m=0..63$)を `candidate` から **`cross-checked`** へ上げる。
- **(II) 命題 E19-b′** の有限判定を $c=6,7$ まで実行し、$m$ 量化子を閉じる(v3 §6.2)。

---

## 0. 前提と対象ファイル

| 項目 | 値 |
|---|---|
| 監査対象 script | `docs/scout/metab.mjs`(便 13 F8 の SHA-256: `45CEA39CD2A3FD80C999DB21C5411B32202A50DFA744E48B0A86863F08FC09D9`) |
| 補助 script | `docs/scout/metab_rank.mjs`(本委嘱で新規・rank のみを測る。**metab.mjs とモデルコードを共有しており第二系統ではない**) |
| 第二系統 | **GAP**(`gap.ps1` 経由・`-o 2g`)。**`SmithNormalFormIntegerMatTransforms` を使う** |
| 出力先 | `certificates/e19/` と `crosscheck/verdicts/e19/`(既存の運用に合わせる) |

---

## 1. 第一段 — model 照合(F9 の 1)

**GAP 側で `metab.mjs` を参照せずにモデルを独立実装する。** 以下は数学的仕様であって、node のコードを移植してはならない。

### 1.1 対象と基底(正本・変更禁止)

$$ A_c:=\mathbb Z[S,T]/(S,T)^{c-1},\qquad n:=\dim_{\mathbb Z}A_c=\tbinom c2 . $$

**基底の順序(正本)**: 単項式 $S^aT^b$($a+b\le c-2$)を、
1. 全次数 $d=a+b$ の**昇順**、
2. 同じ $d$ の中では $a$ の**降順**($a=d,d-1,\dots,0$)

で並べる。すなわち
$$ 1;\ S,T;\ S^2,ST,T^2;\ S^3,S^2T,ST^2,T^3;\ \dots $$
**辞書**: $w=1$、$p=S$、$q=T$、$r_1=S^2$、$r_2=ST$、$r_3=T^2$。

### 1.2 写像の仕様

$s:=1+S$、$t:=1+T$ と置く($\mathbb Z[S,T]/(S,T)^{c-1}$ の単元)。

| 写像 | 定義 |
|---|---|
| $\theta$ | $f(S,T)\ \longmapsto\ -\,f(T,S)$ |
| $\tau$ | $f\ \longmapsto\ f\bigl(S\mapsto T,\ T\mapsto (st)^{-1}-1\bigr)\cdot s^{-1}$ |
| $\sigma_m$ | $f\ \longmapsto\ t^{\,m}\cdot\tau(f)$ |
| $\mathcal N$ | $1+\sigma_m+\sigma_m^2$ |
| $E_m$ | $E_m=c_m-s^{-m}A_m(s)A_m(st)$、$A_m(u)=1+u+\cdots+u^{m-1}$、$c_m=t\,A_{m-1}(st)+t\,c_{m-1}$、$c_1=0$、$E_0=0$ |

($u^{-1}$ は $u=1+U$ に対し $\sum_{k\ge0}(-U)^k$ の切断で計算する。$m<0$ は本指示書の範囲外。)

### 1.3 必須の自己検査(GAP 側・**FAIL なら非零終了して本走査へ進まない**)

`metab.mjs` の 13 項と**同じ数学的内容**を GAP で独立に検査する:

| # | 検査 |
|---|---|
| 1 | $\theta^2=\mathrm{id}$ |
| 2 | $\tau^3=\mathrm{id}$ |
| 3 | $\theta(w)=-w$ |
| 4 | $\tau(w)=w-p+r_1$ |
| 5 | $\tau(p)=q-r_2$ |
| 6 | $\tau(q)=-p-q+2r_1+2r_2+r_3$ |
| 7 | $E_1=(-1,1,0,-1,0,0)$($c=4$ の基底順) |
| 8 | $E_2=(-3,4,-1,-5,1,0)$ |
| 9 | $E_3=(-6,10,-4,-15,5,-1)$ |
| 10 | **命題 E1**: $\theta\tau\theta=\iota_x\circ\tau^{-1}$($\iota_x$ = $s$ 倍、$\tau^{-1}=\tau^2$) |
| 11 | $\sigma_m(E_m)=E_m$($m=0..6$) |
| 12 | **Lemma A**: $\mathcal N(p+q)=3(r_1+r_2+r_3)$、$m=0..8$ で $m$ 非依存 |
| 13 | **Lemma B**: $3E_m=-T_m\kappa_m+B_m\rho$($m=0..12$、$T_m=\binom{m+1}2$、$B_m=\binom{T_m+1}2$、$\kappa_m=\mathcal N(w)$、$\rho=r_1+r_2+r_3$) |

### 1.4 系のダンプ形式(両系統で**バイト同一**を要求する正本形式)

各 $(c,m)$ について、次を**この順・この書式**で出力する。

**行列 $M$**: $2n\times n$ 整数行列。
- 行 $i$($0\le i<n$)= $\bigl((1+\theta)f\bigr)_i$ の $x$ に関する係数、
- 行 $n+i$($0\le i<n$)= $\bigl(\mathcal N f\bigr)_i$ の $x$ に関する係数。
すなわち $M_{i,k}=\bigl((1+\theta)e_k\bigr)_i$、$M_{n+i,k}=\bigl(\mathcal N e_k\bigr)_i$。

**右辺 $b$**: $b_i=0$($0\le i<n$)、$b_{n+i}=-(E_m)_i$。

**直列化(正本)**
```
行:   各成分を十進(符号つき・空白なし)で "," 区切り
行列: 行を ";" 区切り、末尾に区切り文字を置かない
b:    成分を "," 区切りの 1 行
hash: 上の ASCII 文字列を UTF-8 バイト列として SHA-256、16 進小文字
```
出力ファイル: `certificates/e19/system_c{c}_m{m}.txt`(1 行目 `M=...`、2 行目 `b=...`)。

**照合手順(段 1)**
```
for c in 3..7, m in 0..63:
    node 側 M_content_hash / b_content_hash   vs   GAP 側 M_content_hash / b_content_hash
```
**一つでも不一致 ⇒ 即停止**(モデルが食い違っている)。原因調査は「基底順」「行/列の向き」「$\tau$ の代入方向」「$a^g=g^{-1}ag$ 規約」の順に疑う(v1 §1.0 の注意)。

> ★ **node 側の必要な改修 (F8-3)**: `metab.mjs` は現在 `max_v2` しか出さない。上の $M,b$ の直列化とハッシュ出力を追加すること。

---

## 2. 第二段 — 線型代数照合(F9 の 2)

### 2.1 GAP の正準 Smith 形

```gap
r := SmithNormalFormIntegerMatTransforms( M );;   # r.normal, r.rowtrans, r.coltrans, r.rank
U := r.rowtrans;;  V := r.coltrans;;  D := r.normal;;
```
**postcondition(全て検査し、一つでも FAIL なら停止)**
1. `DeterminantMat(U)` $=\pm1$ かつ `DeterminantMat(V)` $=\pm1$(unimodularity)。
2. `U * M * V = D`(再乗算で一致)。
3. `D` は対角、対角成分 $d_1,\dots,d_\rho>0$($\rho=$`r.rank`)、それ以降 0。
4. **整除鎖** $d_i\mid d_{i+1}$($1\le i<\rho$)。
5. `r.rank` $=$ 非零対角成分の個数。

> **なぜこれが要るか(F8-1/2)**: `metab.mjs` の内蔵 `snf` は Euclid 操作による**整数対角化**であって canonical Smith 形ではない(正値化も整除鎖も作らない)。また $V$ を保存せず、$UMV=D$ の postcondition を検査していない。**したがって「バイト一致」は現状の node 出力に対しては実行不能**であり、比較対象を定義し直す必要がある(§2.3)。

### 2.2 判定量

```
c_vec := U * b;
rank_Q  := r.rank                                  # = 非零 d_i の個数
rank_F2 := #{ i <= rank_Q : d_i is odd }           # 奇数基本因子の個数
elementary_divisors := [ d_1, ..., d_rho ]
max_v2_divisor := max_i v_2(d_i)
Z2_solvable := ( forall i<=rank_Q : v_2(c_vec[i]) >= v_2(d_i) )
               and ( forall i>rank_Q : c_vec[i] = 0 )
Q_solvable  := ( forall i>rank_Q : c_vec[i] = 0 )
all_divisors_odd := ( max_v2_divisor = 0 )         # <=> rank_Q = rank_F2
```

### 2.3 node 側の改修と比較対象(F8 / F9)

**選択肢 A(推奨)**: node 側にも $V$ と整除鎖正規化を実装し、**canonical elementary divisor list を出力**する。この場合の比較対象は
```
elementary_divisors(全リスト)・rank_Q・rank_F2・max_v2_divisor・Z2_solvable・Q_solvable
```
の**完全一致**。$U,V$ 自体は一意でないので**比較しない**(postcondition だけ検査する)。

**選択肢 B(最小改修)**: node 側は canonical 化せず、比較対象を
```
rank_Q ・ rank_F2 ・ Z2_solvable ・ Q_solvable ・ §3 の witness residual
```
に限定する。この場合 **`elementary_divisors` の「バイト一致」は要求しない**(できない)。**どちらを採ったかを証明書に明記する。**

> **F8-4/5 の必須改修(選択肢によらず)**
> - 自己検査が一件でも FAIL したら **`process.exit(1)`**。現状は FAIL しても結果部へ進む。
> - 既定は `maxM=31` なので、$0..63$ を再現するには **明示コマンド `node docs/scout/metab.mjs 7 63`** が必要。**exact command・stdout・exit code・script SHA-256 を証明書に固定する。**

---

## 3. 第三段 — witness 照合(F9 の 3)

**肯定例**: 各 $(c,m)$ と各 $j=1,\dots,6$ について、少なくとも一つの $f$ を復元する。

```
y_i := c_vec[i] / d_i         (i <= rank_Q; 2 進整数として。d_i が偶数でも v_2(c_i)>=v_2(d_i) なら可)
y_i := 0                      (i >  rank_Q)
x   := V * y                  (mod 2^j に落とす)
```
**必ず元の $M,b$ に直接代入して residual を検査する**:
$$ \bigl((1+\theta)f\bigr)\equiv0,\qquad \bigl(\mathcal N f+E_m\bigr)\equiv0 \pmod{2^j} $$
を、SNF を経由せず**モデルの写像そのもの**で再計算すること。両系統で同じ $f$ を代入し、residual がともに 0 であることを照合する。

**否定例**: dual witness $y$($yM\equiv0$、$yb\not\equiv0\bmod2^j$)を出力し、両系統で $yM$ と $yb$ を再計算(便 12 F13 の形式)。

---

## 4. 第四段(新規)— 命題 E19-b′ の $m$ 量化子(W108 / v3 §6.2)

### 4.1 判定基準(v3 §6.2 の命題 E19-b′)

剰余類 $\bar m\in\mathbb Z/8$ ごとに、標本 $m=\bar m,\bar m+8,\dots,\bar m+8K$ **すべて**で
$$ \operatorname{rank}_{\mathbb Q}M(m)=\operatorname{rank}_{\mathbb F_2}M(m)=\operatorname{rank}_{\mathbb Q}[\,M(m)\mid b(m)\,]=:r_{\bar m} $$
が成り立ち、かつ
$$ K\ \ge\ (r_{\bar m}+1)\,d+c,\qquad d:=2(c-2) $$
ならば、**その剰余類の全ての $m\in\mathbb Z$** で ① 全非零基本因子が奇数、② $\mathbb Q$-可解、③ $\mathbb Z_2$-可解(= 全 $j$ で mod $2^j$ 可解)が従う。

### 4.2 実行表(**$r$ を先に測ってから上限を決める**)

**$r_{\bar m}$ は $m=0..63$ で先に測定済み(全 $c$・全剰余類で剰余類によらず一定だった)。**

| $c$ | $n=\binom c2$ | $d=2(c-2)$ | 観測 $r$(全剰余類共通) | 必要 $K=(r{+}1)d+c$ | 必要な $m$ の上限 $7+8K$ | 状態 |
|---|---|---|---|---|---|---|
| 3 | 3 | 2 | **2** | 9 | 79 | **単系統・GAP 照合待ち** `node docs/scout/metab_rank.mjs 3 80`(falsifier 掃引v3ゲート指摘 F#1 反映: GAP 独立再現前は CLOSED と書かない) |
| 4 | 6 | 4 | **4** | 24 | 199 | **単系統・GAP 照合待ち** `node docs/scout/metab_rank.mjs 4 260` |
| 5 | 10 | 6 | **8** | 59 | 479 | **単系統・GAP 照合待ち** `node docs/scout/metab_rank.mjs 5 480` |
| 6 | 15 | 8 | **11** | 102 | **823** | **要実行** `node docs/scout/metab_rank.mjs 6 830` |
| 7 | 21 | 10 | **16** | 177 | **1423** | **要実行** `node docs/scout/metab_rank.mjs 7 1430` |

**手順**
1. 上の $m$ 上限まで node を走らせ、**全剰余類で `=> CLOSED`** が出ることを確認する。
2. **一つでも rank が食い違ったら、その剰余類は UNKNOWN**(その剰余類だけ落とす。他は生きる)。
3. §4.3 の GAP 独立実装で**同じ rank 表**を再現し、`cross-checked` へ上げる。
4. 参考: $\mathbb Q$ 上の解空間の次元 $n-r$ は $c=3..7$ で $1,2,2,4,5$。**$c\le7$ ではどの $c$ でも系は $\mathbb Q$-可解で、解空間は正次元**である。

### 4.3 GAP 側での実装(第二系統)

```gap
rQ  := RankMat( M );                       # over Rationals
rF2 := RankMat( One(GF(2)) * M );          # over GF(2)
rA  := RankMat( TransposedMat( Concatenation( TransposedMat(M), [ b ] ) ) );  # [M|b]
```
$c\le5$ については **`metab_rank.mjs` の出力(node)と完全一致**を要求する(これが E19-b′ の二系統化)。

> **注意(語の規律)**: `metab_rank.mjs` は `metab.mjs` とモデルコードを共有している。**したがって node 単独では二系統ではない。** GAP 側の独立実装と一致して初めて `cross-checked` を名乗れる。

---

## 5. 証明書 `e19-crosscheck-cert/v1`

```json
{
  "schema": "e19-crosscheck-cert/v1",
  "target": "theorem E19 + proposition E19-b'",
  "comparison_mode": "A_canonical_divisors | B_ranks_and_witness",   // §2.3 のどちら
  "per_pair": [{
    "c": 5, "m": 17,
    "model": { "M_content_hash": "...", "b_content_hash": "...",
               "basis_order": "deg-asc, within-deg a-desc",
               "row_order": ["theta_0..theta_{n-1}","norm_0..norm_{n-1}"],
               "routes_agree": true },
    "linear_algebra": {
      "gap": { "rank": 8, "elementary_divisors": [1,1,1,1,1,1,1,3],
               "max_v2_divisor": 0, "rank_F2": 8,
               "postconditions": { "det_U": 1, "det_V": -1, "UMV_recheck": true,
                                   "diagonal": true, "divisibility_chain": true } },
      "node": { "...": "..." },
      "agree": true },
    "solvability": { "Q_solvable": true, "Z2_solvable": true, "agree": true },
    "witness": { "j": [1,2,3,4,5,6],
                 "f_coords": { "1": ["..."], "...": "..." },
                 "residual_theta": 0, "residual_norm": 0,
                 "recomputed_by": ["node","gap"] }
  }],
  "E19b_prime": {
    "per_class": [{ "c": 5, "residue": 3, "samples": 60, "K_required": 59,
                    "rank_Q": 8, "rank_F2": 8, "rank_aug": 8, "closed": true }],
    "conclusion": "c<=5: all m in Z, Z2-solvable and Q-solvable"
  },
  "provenance": {
    "gap_version": "4.16.0", "node_version": "...",
    "script_sha256": { "metab.mjs": "...", "metab_rank.mjs": "...", "e19.g": "..." },
    "exact_commands": [ "node docs/scout/metab.mjs 7 63",
                        "node docs/scout/metab_rank.mjs 5 480",
                        "./gap.ps1 -o 2g search/e19.g" ],
    "exit_codes": [0,0,0], "stdout_sha256": [ "...","...","..." ]
  },
  "verdict": "all_pass | mismatch_stop | cap_exceeded"
}
```

**禁止事項**
- **`verified` の語を使わない**(Lean 予約)。二系統一致は `cross-checked`。
- 自己検査 FAIL のまま結果を出力しない(非零終了)。
- `max_v2` だけを比較対象にしない(F8-3)。
- 「基本因子が全て奇数」から $m$ 量化子を**推論しない**(W108)。$m$ 量化子は §4 の判定を通った剰余類についてのみ主張する。

---

## 6. 期待される成果と昇格条件

| 成果 | 昇格条件 |
|---|---|
| 定理 E19($c=3..7$、$m=0..63$、全 $j$) | §1–§3 の三段すべてで `routes_agree` ⇒ **`cross-checked`** |
| 命題 E19-b′ の適用($c=3,4,5$、**全 $m\in\mathbb Z$**) | §4.3 で GAP と node が一致 ⇒ **`cross-checked`** |
| 同($c=6,7$) | §4.2 の実行後。rank が剰余類ごとに一定でなければ **UNKNOWN のまま** |
| $c\ge8$ | 8GB 制約。**UNKNOWN のまま盤面に残す**(便 13 F11 — metabelian class $\ge8$ は落とさない) |

> **★ この作業が閉じても E15 は閉じない。** 閉じるのは「自由 metabelian 塔の 2-一次障害と $m$ 量化子」だけである。**$A$ 非可換の層(掃引 ① r2)は独立に残る。**

---

## 7. 状態札

| 項目 | 札 |
|---|---|
| 本指示書の仕様(§1.1–§1.2) | 数学的仕様。`metab.mjs` の冒頭コメントと一致するが、**GAP 実装は独立に行うこと** |
| 命題 E19-b′ | **紙上証明**(v3 §6.2・Opus 単独・Sol 未監査) |
| $c=3,4,5$ の適用結果 | **candidate(単系統)**。本指示書 §4.3 の完了で `cross-checked` へ |
| 定理 E19($m\le63$) | `Z2-solvable candidate (single system, statically audited)`。本指示書の完了で `cross-checked` へ |
