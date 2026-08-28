# EP-DEL 配線メモ v1 — 10 本の $\rho_o$・4 本の $d_i$・EP-G2・40 検査

`DIR: proper 側計器 / FRAME: Sol A7 endpoint × 工房 BRUN-DEF`
**委嘱**: 司令塔・裁定 1725(implementer A が $\rho_o$ の具体配線を特定できず誠実停止)。
**格**: §1–§3 = **repo 実物で確認済**(パス・SHA・関数名すべて機械確認)。§5 = **UNKNOWN 1 点**(復号器の所在は特定済)。
**著者**: 数学者(Opus 5)/ 2026-08-28。**規約 (R-1)(R-2) 準拠。**

> ### ★ 結論を先に(3 行)
> 1. **pinned JSON は 3 本とも repo 内に present**(GHA artifact 待ちではない)。**registry も repo 内**にあった。
> 2. **10 本の $\rho_o$ の context ID は完全に特定できた**(下表)。**4 本の $d_i$ は chief_lib の 1 関数で立つ。**
> 3. **残る UNKNOWN は 1 点だけ** — context 行の `left_hex/right_hex`(154 バイト element blob)を $\rho_o(x),\rho_o(y)$ へ復号する経路。**復号器の所在は §5 に特定済。**

---

## 1. 入力アーティファクト(**すべて repo 内・機械確認済**)

| # | パス | bytes | SHA256(pin 元) |
|---|---|---:|---|
| **A1** | `search/koubou157f_q3_chief_lib_v1.g` | 76,368 | (`Read()` するだけ・pin なし) |
| **A2** | `ci/b345_157eh_lexblock_artifacts_32401947156/d972_b345_q3_chief_v1.json` | 231,570 | `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72` |
| **A3** | `ci/out/koubou157f_iota_rewrite_v1.json` | 2,057 | `651291a073a33632301e17965a7212bca9f00c86bbc66ad5e9a61536c92ef48f` |
| **★ A4** | `ci/b345_157ee_artifacts_32359956713/d972_b345_joint_kernel_qstar_closure_v1.json` | 2,166,036 | **context registry の本体**(下記) |
| A5 | `search/koubou157f_iota_i0c_v1.g` | 16,467 | **群構築の手本**(L55–140 をそのまま流用) |

**A2/A3 の SHA は `search/koubou157f_iota_i0c_v1.g` L57–63 に pin されている**(`D972I0C_Q3ChiefSha` 等)。⟹ **同じ pin を再利用すること。**
**A4 の registry ダイジェスト**: `context_rows_sha256 = bf07578f91f5ed66e6ddddd4ef83dafa…`、`named_use_mapping_sha256 = 15cdac950ede8ce4596e5014ae1b6d0c…`。

⟹ **implementer A の停止理由「pinned JSON 3 本を要求」は解消**: **3 本とも在り、しかも registry(4 本目)も在る。**

---

## 2. 群の構築(A5 の L55–140 をそのまま使う)

```gap
Read("search/koubou157f_q3_chief_lib_v1.g");;
q3   := JsonStringToGap(StringFile("ci/b345_157eh_lexblock_artifacts_32401947156/d972_b345_q3_chief_v1.json"));;
# --- coarse models(marked permutations で生成される置換群)---
Q4   := Group(List(q3.coarse_models.Q4.marked_permutations, r -> PermList(List(r,Int))));;   # degree 144
Q0   := Group(List(q3.coarse_models.Q0.marked_permutations, r -> PermList(List(r,Int))));;   # degree 36
# --- Pi4[3] / Pi3[3] は pc 群(A5 の pcgs4/coll ブロックを流用)---
# --- 積: E4 = Q4 x Pi4[3] ,  E3 = Q0 x Pi3[3]   (v122 (57)・chief_lib L1083 逐語) ---
```

**機械確認済の諸元**(A2 から読んだ実値):

| model | degree | order | marked |
|---|---:|---|---:|
| `Q0` | 36 | 1,469,664 | 2 |
| `Q4` | 144 | 583,152,628,325,845,597,028,352 | 6 |
| `G9` | 27 | 2,916 | 2 |
| `H9` | 108 | 9,037,745,167,392 | 6 |
| `P` | 9 | 504 | 2 |

**$E_3=Q_0\times\Pi_3[3]$、$E_4=Q_4\times\Pi_4[3]$**(v122 (57)/chief_lib L1083)。
**A5 が既に検査している前提**: `marked_permutations_generate_Q4 = true`、`marked_pc_elements_generate_Pi4 = true`(A5 の出力 JSON `ci/out/koubou157f_iota_i0c_v1.json`)⟹ **同じ assert を再利用**。

**retraction(v122 §2)**: $d_E=d_Q\times d_\Pi:E_4\to E_3$、$i_E:E_3\to E_4$、**$d_Ei_E=\mathrm{id}_{E_3}$**(v122 (111)(113)(120))。⟹ **E3 側の 5 本は「E4 context を測って $d_E$ で落とす」**。

---

## 3. ★ 10 本の $\rho_o$ — **context ID は完全特定**

**出所**: A4 の `/context_registry`(31 contexts + 46 `named_uses`)。**`named_uses` の名前がそのまま配線表になっている。**

### 3.1 E3 側 5 本(v189 (1.1)・task176 順 $d_EC_{21},\dots,d_EC_{25}$)

| $\rho$ | v189 の記号 | source pair | **context_id** | A4 の `named_uses` 名 |
|---|---|---|---:|---|
| $a$ | $\rho_{xy}$ | $(x,y)$ | **21** | `hexagon_1_fxy_4` / `hexagon_2_fxy_4` / `source_ff` |
| $b$ | $\rho_{xz}$ | $(x,z)$ | **22** | `hexagon_1_fxz_4` |
| $c$ | $\rho_{yz}$ | $(y,z)$ | **23** | `hexagon_1_fyz_4` |
| $d$ | $\rho_{ux}$ | $(u,x)$ | **24** | `hexagon_2_fux_4` |
| $e$ | $\rho_{uy}$ | $(u,y)$ | **25** | `hexagon_2_fuy_4` |

- **v122 (150)–(151) の表と完全一致**(source pair ↔ E4 context ID 21–25)✓
- **5 本とも `_4` サフィックス = coface-4 行**。registry は coface 0..4 で 5 セット持っており(ID 1–5 / 6–10 / 11–15 / 16–20 / 21–25)、**task176 が採るのは coface-4 セット**。
- **`hexagon_1_fxy_4` と `hexagon_2_fxy_4` が同一 ID 21** ⟹ **v189 の「H1/1 と H2/2 は同じ E3 写像」が registry で裏づけられる** ✓(独立検算 #1)。

### 3.2 E4 側 5 本(pentagon)

| A4 の名前 | **context_id** |
|---|---:|
| `pentagon_part_0` | **21** |
| `pentagon_part_1` | **1** |
| `pentagon_part_2` | **26** |
| `pentagon_part_3` | **27** |
| `pentagon_part_4` | **28** |

**集合は $\{1,21,26,27,28\}$** で、v189 (1.6) の task176 順 $(C_1,C_{27},C_{21},C_{26},C_{28})$ と**集合として一致** ✓。

> ### ⚠⚠ **順序の食い違い(CV-9 型・必ず pin すること)**
> - registry: `pentagon_part_j` $\;(j=0..4)\;\mapsto\;(21,\,1,\,26,\,27,\,28)$
> - v189 (1.6) task176 順 $(p_1,p_2,p_3,p_5,p_4)\;\mapsto\;(1,\,27,\,21,\,26,\,28)$
>
> **同じ 5 本だが割り当てが違う。**v194 (1.7) の印字順は $b_1,b_2,b_3,b_5^{-1},b_4^{-1}$(**うち 2 本は逆元 = 符号 $\sigma_o=-1$**)なので、**$P_o$ と $\sigma_o$ を使う計算では順序が load-bearing**。
> **⟹ 影響の切り分け**:
> - **§4.2 の 40 検査(④a)は順序に依存しない** ⟹ **今すぐ走らせてよい。**
> - **§4.3 の evaluator(④b)は順序が要る** ⟹ **走らせる前に「registry 順」か「task176 順」かを cert に宣言し、両方で走らせて差を見ること**(mutant EP-G4 がこれを検出する)。

---

## 4. 実行形

### 4.1 4 本の $d_i$(chief_lib の 1 関数)

```gap
del := D972Q3Deletions(4);;      # del[s] = strand s を削除したときの、PB4 の 6 本の pair 生成子の PB3 語
                                 # D972Q3DeleteGenerator(4,s,pair) は pair に s を含めば [] を返す
```
**逐語で確認した性質(D-NAT の前提そのもの)**:
```
D972Q3DeleteGenerator := function(rank, strand, pair)
  if strand=i or strand=j then return [];; fi;        # ← 生成子が 1 に落ちる
  ...  return [D972Q3PairIndex(rank-1,[i,j])];        # ← それ以外は生成子 1 本に落ちる
```
⟹ **「生成元 ↦ 生成元 or 1」が実装レベルで確認された**(`ep_del_verdict_v2.md` §3 の補題 D-NAT の前提が満たされる)✓ **独立検算 #2。**
合成は `D972Q3ComposeMaps(first, second)`、恒等は `D972Q3IdentityMap(rank)`。

### 4.2 ★ 40 検査(④a・**最優先・順序非依存**)

```gap
for o in TenContexts do                       # §3 の 10 本(context_id で引く)
  for s in [1..4] do
    gx := Image_of_x_under( d_s o rho_o );;   # §5 の復号が要る 1 点
    gy := Image_of_y_under( d_s o rho_o );;
    H  := Group(gx, gy);;                     # ← 型: E3 or E4 の部分群(下記)
    Print(o, s, IsAbelian(H), "\n");;
  od;
od;
```
> ### 型の明示(委嘱 ④ の (4))
> - **E4 側 5 本**: $\rho_o(x),\rho_o(y)\in E_4=Q_4\times\Pi_4[3]$。$d_s$ の像は **PB3 文脈**なので、比較は **$E_3=Q_0\times\Pi_3[3]$ の元として**行う(retraction $d_E$ を通す)。
> - **E3 側 5 本**: 既に $d_EC_{2k}$ で $E_3$ に居る。$d_s$ の像も $E_3$ 内。
> - ⟹ **40 回すべて $\langle g_x,g_y\rangle\le E_3$ の `IsAbelian`。**直積なので **成分ごとに** `IsAbelian(Q0-part)` かつ `IsAbelian(Pi3-part)` かつ **成分間は可換**(直積ゆえ自動)で判定してよい ⟹ **置換群と pc 群の 2 本の安い判定に分解できる。**

**出口**: **40/40 可換 ⟹ (C-β) = 0 ⟹ EP-DEL は定理**(`ep_del_verdict_v2.md` §5.1 の boxed 命題)。**1 つでも非可換 ⟹ その $(o,i)$ で個別評価(§4.3)へ。**

⚠ **$E_3$ 自身は非可換**(`chief_lib` L972 逐語: `E3=Q0 x B(2,3)`・27 元右繊維 ⟹ $B(2,3)$ は位数 27・類 2)。⟹ **40 検査は自明ではない。**しかし問うているのは**削除後の像**なので、非可換 $E_3$ の中で可換部分群に落ちることは十分ありうる。

### 4.3 EP-G2 の実行形($(d_i)_*\epsilon_P$)

$\epsilon_P=D_{1,P}e_P=w_e-1$(Fox 恒等式)なので、**$\epsilon_P$ を Fox 鎖として作る必要はない**:

```
G2-1  w_e := corrected residual の literal word(v198 (1.3) の "retained literal word provenance")
G2-2  for i in 1..4:  d_i(w_e) を PB4 -> PB3 で評価し、E3 の元として 1 か否かを見る
G2-3  (d_i)_* eps_P = d_i(w_e) - 1  =  0  <=>  d_i(w_e) = 1
```
**期待値: 4 本とも 0**(BRUN-DEF ⟹ $w_e\in B_P=\mathrm{Im}(\mathrm{Brun}_4\to G_P)$ ⟹ $d_i(w_e)=1$)。
⚠ **非零なら (C-α) が崩れる** ⟹ BRUN-DEF の適用条件か $w_e$ の provenance が誤り ⟹ **E3 以降は無意味。最初に回すこと。**

**charming 台 $M$ の工房生成**(Sol の実 $M$ が無いため):
```
M1  U_j, V_j を [F(x,y),F(x,y)] から取る(例: [x,y], [x,y^2], [x^2,y], [[x,y],x] …)
M2  roof 条件 pi(U_j)=pi(V_j) は、pi(= v191 Delta_0)が未読なので
    ★ 代用: rho_o(U_j) = rho_o(V_j) を全 10 context で満たす対を探索し、その旨を cert に宣言
    (これは pi 経由より強い条件なので、代用で作った M は真の roof-fibre 対の部分集合)
M3  a_j in F_3 を任意に取る
```

---

## 5. ★ UNKNOWN — **残り 1 点**(所在は特定済・推測で埋めない)

**context 行 $(\texttt{left\_hex},\texttt{right\_hex})$ から $\rho_o(x),\rho_o(y)$ を取り出す復号。**

**測定した符号化の事実**:
```
gate: A4 /context_registry/contexts : 31 rows, keys = {context_id, left_hex, right_hex}
      len(left_hex) = len(right_hex) = 308 hex chars = 154 bytes  (全 31 行で同一)
```
- 154 バイトは $Q_4$ の次数 144 とも $Q_0$ の 36 とも一致しない ⟹ **単純な置換リストではない**(直積の 2 成分を連結した blob と思われるが**確認していない**)。
- **復号器の所在(特定済)**: `search/d972_b345_joint_kernel_qstar_closure_v1.py` の **`_element_blob`**(L230 と L406 で `bytes(self.old._element_blob(value))` として使われている)+ それが包む `old` モデル。**同ディレクトリの checker(`search/check_d972_b345_joint_kernel_qstar_closure_v1.py` / `_v2.py`)も `left_hex` を読んでいる**ので、**逆変換はそちらに在る可能性が高い**。
- **代替経路(復号を回避できるかもしれない)**: `named_uses` の名前(`hexagon_1_fxy_4` 等)は **どの hexagon のどの位置・どの coface か**を完全に指定しているので、**chief_lib の `D972Q3Cofaces(3)` と `D972Q3HexPairs/D972Q3Pairs` から $\rho_o$ を再構成できる可能性がある**(registry を読まずに済む)。**未検証。**

> **implementer への指示**: **まず代替経路を試す**(chief_lib だけで $\rho_o$ が立つなら registry 復号は不要)。立たなければ `_element_blob` の逆を checker から読む。**どちらも不可なら UNKNOWN で停止し、blob レイアウトの仕様を要求すること。推測で復号しない。**

---

## 6. 較正(委嘱 5・**配線が正しいことの独立検算**)

| # | 検査 | 期待 | 出所 |
|---|---|---|---|
| **W-1** | `hexagon_1_fxy_4` と `hexagon_2_fxy_4` の context_id が**一致** | 両方 **21** | ★ **確認済**(§3.1)— v189「H1/1 と H2/2 は同じ E3 写像」の独立裏づけ |
| **W-2** | `D972Q3DeleteGenerator(4,s,pair)` が pair∋s で `[]` を返す | true | ★ **確認済**(§4.1)— D-NAT の前提 |
| **W-3** | source pair ↔ context ID の表 | $(x,y)(x,z)(y,z)(u,x)(u,y)\leftrightarrow 21,22,23,24,25$ | ★ **確認済**(v122 (150)-(151) と registry が一致) |
| **W-4** | `pentagon_part_*` の ID 集合 | $\{1,21,26,27,28\}$ = v189 (1.6) の E4 集合 | ★ **確認済**(⚠ 順序は §3.2 の食い違い) |
| **W-5** | $\lvert Q_4\rvert$、$\lvert Q_0\rvert$ | 583152628325845597028352 / 1469664 | ★ **確認済**(A2 から実読) |
| **W-6** | `marked_permutations_generate_Q4` | true | A5 の出力 JSON に既記録 |
| W-7 | $E_3=Q_0\times B(2,3)$ の $B(2,3)$ が位数 27 | 27 | chief_lib L972 逐語(`27-element right fibre`)|

⟹ **W-1〜W-6 は本メモ作成中に機械で確認済**。W-7 は逐語引用。**配線の骨格は 6 点で裏取りされている。**

---

## 7. 実行順(推奨)

1. **EP-G2**($(d_i)_*\epsilon_P=0$ の 4 本)— **最初に**。落ちたら以降は無意味。
2. **40 検査**(§4.2)— **順序非依存なので §3.2 の食い違いを待たずに走る。40/40 可換なら EP-DEL は定理。**
3. 40/40 でなければ **evaluator**(§4.3・`ep_del_verdict_v2.md` §5.2 の E1–E4)— **その前に pentagon の順序を cert で宣言**。

## 8. UNKNOWN 一覧

1. **§5 の blob 復号**(所在は特定済・代替経路あり)。
2. **§3.2 の pentagon 順序の食い違い**(registry 順 vs task176 順)— 40 検査には無影響、evaluator には load-bearing。
3. **$\pi$(v191 $\Delta_0$)の定義**未読 ⟹ §4.3 M2 は**代用条件**で走る(cert に宣言)。
4. $E_4$ の `IsAbelian` 実測は未実行(§4.2 は**削除後の像**を問うので、これは不要)。
