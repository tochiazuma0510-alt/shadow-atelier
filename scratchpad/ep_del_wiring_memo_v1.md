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

---

# §9 ★ pentagon_part 順の裁定(2026-08-28・裁定 1731(b) ②)

## 9.1 裁定

$$\boxed{\ \textbf{registry の }(21,\,1,\,26,\,27,\,28)\ \text{が正。v189 (1.6) の E4 タプル }(1,27,21,26,28)\ \text{は転記誤り。}\ }$$

$P_o/\sigma_o$ の実装は **registry の `pentagon_part_0..4` をそのまま位置対応で使う**。

## 9.2 根拠(上流の同定)

**上流は「生成コード」である。**`pentagon_part_j` を書いた実体を特定した:

```python
# search/check_d972_b345_relfrat3_fixed_candidate_v5.py  L804-812
    g = e4.generators
    pentagon = [
        (g[0], g[3]), (g[3], g[5]),
        (q_paper_product(e4, [g[1], g[3]]), g[5]),
        (q_paper_product(e4, [g[0], g[1]]),
         q_paper_product(e4, [g[4], g[5]])),
        (g[0], q_paper_product(e4, [g[3], g[4]])),
    ]
    for index, pair in enumerate(pentagon):
        register(f"pentagon_part_{index}", *pair)
```
(同一ブロックが `_v6.py` L837・`_pivot_surgery_v7.py` L856・`_v4.py` L806 にも在り、**4 世代で不変**。)

**決め手 3 点**:

| # | 根拠 | 効き方 |
|---|---|---|
| **R-1** | `pentagon` リストは **`q_paper_product`(= 論文の積規約)** で組まれ、`enumerate` で 0-based に登録される ⟹ **リストの並びは論文の印字順そのもの** | registry は印字順の**忠実な記録** |
| **R-2** | ★ **E3 側は registry と v189 (1.6) が完全一致**($\rho_{xy},\rho_{xz},\rho_{yz},\rho_{ux},\rho_{uy}\leftrightarrow21,22,23,24,25$;registry の `hexagon_1_fxy_4`=21 … `hexagon_2_fuy_4`=25)⟹ **v189 (1.6) は同一 registry を読んでいる**。ゆえに E4 側だけが食い違うのは**転記の問題**であって別 registry ではない | 食い違いの型を「版ずれ」から「転記誤り」へ確定 |
| **R-3** | 位置対応の突合: v194 (1.7) の印字順は $b_1,b_2,b_3,b_5^{-1},b_4^{-1}$、v189 (1.5) の並びは $(p_1,p_2,p_3,p_5,p_4)$ ⟹ **両者は同じ位置列**。registry も 0-based 位置列。⟹ **3 者は同じ位置規約**のはずで、値だけが v189 でずれている | 「順序規約の違い」ではないことを排除 |
| — | 両者は $p_4=28$ **のみ一致**、残り 4 本が置換 $(0{\to}1,1{\to}3,2{\to}0,3{\to}2)$ | 系統的な再ラベルではない = 転記 |

**v189 は散文の証明ノートで生成コードを持たない。registry は生成コードを持つ artifact。⟹ コードが上流。**

## 9.3 実装への指示

- **$P_o$(prefix)と $\sigma_o$(符号)は registry の位置順で読む。**
- **$\sigma_o=-1$ となるのは `pentagon_part_3` と `pentagon_part_4`**(印字順 $b_5^{-1},b_4^{-1}$ の 2 本が逆元 ⟹ 位置 3,4)。
- cert 必須欄: `pentagon_order_source: "registry/pentagon_part_j (q_paper_product enumerate)"` と `sigma_negative_positions: [3,4]`。
- **mutant EP-G4**(印字順を崩す)は、**v189 (1.6) の順序 $(1,27,21,26,28)$ を注入する形**で実装せよ ⟹ 判定が変わることを確認できれば、本裁定が実測で裏づく。

## 9.4 具申(v189 側の訂正)

**v189 (1.6) の E4 タプルは `(21, 1, 26, 27, 28)` へ訂正されるべき**(E3 タプル $(21,22,23,24,25)$ は正しい)。
⚠ ただし **v189 は Sol 側の文書**であり、**本便では触らない**(不介入)。**司令塔経由での申し送りを具申する。**

## 9.5 40 検査への影響 — **なし**

§4.2 の 40 検査は $\{$10 本の $\rho_o\}\times\{$4 本の $d_i\}$ の**集合上の走査**で、$P_o/\sigma_o$ を使わない ⟹ **順序非依存**。**implementer A の並行走行はそのまま続行してよい。**

---

# §10 ブロッカー 2 点への直接回答(2026-08-28・裁定 1732)

## 10.0 まず判明した重大事実 — **受領票に「入っていない」**

```
gate: ci/b345_157eh_lexblock_artifacts_32401947156/d972_b345_q3_chief_v1.json
  /maps = {"cofaces_3_4": [], "cofaces_4_5": [],
           "deletions_4_3": [], "deletions_5_4": [],
           "status": "BYPASSED_BY_EXACT_WORD_CORRECTION"}
  /chief_fox = {"executed": false, "d2_bypassed_by_exact_word": true,
                "status": "BYPASSED_BY_EXACT_WORD_CORRECTION", ...}
  /endpoint_retractions = {"status": "BYPASSED_BY_EXACT_WORD_CORRECTION",
                           "theorem": "i^-1 N_(r+1)(3)=N_r(3)"}
```

> ★ **`deletions_4_3` は空リスト。producer は削除写像の計算を意図的に迂回している**(`BYPASSED_BY_EXACT_WORD_CORRECTION`)。
> ⟹ **implementer A が「pinned JSON から $d_i$ の Q 成分を読む」ことは原理的に不可能**だった。仮説を立てざるを得なかったのは**受領票の欠落が原因**であり、実装の落ち度ではない。**同じく `chief_fox.executed=false` なので Fox 鎖も受領票に無い。**

---

## 10.1 ブロッカー① — $d_i$ の Q 成分($Q_4\to Q_0$)

### 10.1.1 反証された仮説の根因(診断)

**$Q_0$ は $PB_3$ の商ではなく $F_2$ の商である。**
```
gate: /coarse_models/Q0 = {degree: 36, order_decimal: "1469664", marked_permutations: 2}
      1469664 = 2^5 * 3^8 * 7
```
この **1,469,664 は $\lvert F_2/M_{F_2}\rvert$ の既知値**(972 窓の $F_2$-部分商;`gdyn_definition_draft_v2.md` §3.4 で使用)。⟹ **$Q_0=F_2/M_{F_2}$**、marked は **2 本($x,y$ の像 $q_{0x},q_{0y}$)**。
一方 `/groups/PB3` は `generator_count: 4`(= $a_{12},a_{13},a_{23},c$)で marked は 3 本。

⟹ **$a_{13}$ の像は marked に無く、$PB_3$ の関係式から解くしかない。**
$$a_{12}\,a_{13}\,a_{23}=c,\qquad \bar c=1\ \text{in}\ Q_0\ (\text{$F_2$ 商ゆえ中心は死ぬ})\ \Longrightarrow\ \bar a_{13}=\bar a_{12}^{-1}\bar a_{23}^{-1}$$
**⟹ 積の順序だけが問題**で、$(q_{0x}q_{0y})^{-1}$ と $(q_{0y}q_{0x})^{-1}$ の 2 通り。**仮説 $(q_{0x}\cdot q_{0y})^{-1}$ の反証は「もう一方の順序が正」を示唆する** — これは **W-1(paper 語順 ↔ GAP 語順)そのもの**。

### 10.1.2 ★ 正しい手順 — **推測せず GAP に決めさせる**

`GroupHomomorphismByImages` は関係式が破れると `fail` を返す。⟹ **これを裁定者に使う。**

```gap
Read("search/koubou157f_q3_chief_lib_v1.g");;
q3   := JsonStringToGap(StringFile("ci/b345_157eh_lexblock_artifacts_32401947156/d972_b345_q3_chief_v1.json"));;
q0x  := PermList(List(q3.coarse_models.Q0.marked_permutations[1], Int));;
q0y  := PermList(List(q3.coarse_models.Q0.marked_permutations[2], Int));;
Q0   := Group(q0x, q0y);;
if Size(Q0) <> 1469664 then Error("Q0 order drift"); fi;          # ★ 較正 G-Q1

## (1) a13 の像を GAP に決めさせる  ------------------------------------------
P3    := D972Q3BuildPureFp(3);;            # PB3 (4 generators: a12, a13, a23, c)
g3    := GeneratorsOfGroup(P3);;
cands := [ (q0y*q0x)^-1, (q0x*q0y)^-1 ];;  # 2 通りだけ
ok    := [];;
for z in cands do
  h := GroupHomomorphismByImages(P3, Q0, g3, [q0x, z, q0y, One(Q0)]);   # c -> 1
  if h <> fail then Add(ok, z); fi;
od;
if Length(ok) <> 1 then Error("Q0-lift: not unique / none — 停止して報告"); fi;   # ★ G-Q2
imA13 := ok[1];;                            # ← これが正解。推測しない。

## (2) 削除写像 d_s : Q4 -> Q0  ----------------------------------------------
q4marks := List(q3.coarse_models.Q4.marked_permutations, r -> PermList(List(r,Int)));;
Q4  := Group(q4marks);;
del := D972Q3Deletions(4);;                 # del[s][k] = PB4 の pair k の PB3 語(pair-index 列)or []
imgs3 := [ q0x, imA13, q0y ];;              # PB3 pair 順 [1,2],[1,3],[2,3]
dQ := [];;
for s in [1..4] do
  dQ[s] := GroupHomomorphismByImages(Q4, Q0, q4marks,
             List([1..6], k -> D972Q3WordEval(del[s][k], imgs3)));;
od;
```

> ### ★ ゲート(結果がどちらでも一級)
> - **G-Q2**: `ok` が**ちょうど 1 本**であること。0 本なら「$\bar c=1$ の仮定」か marked の割当が誤り;2 本なら関係式が両順序を許す(=判別不能)⟹ **いずれも停止して報告**。
> - **G-Q3**: `dQ[s] <> fail` であること。**`fail` が出たら、それは実装ミスではなく「削除が $Q_4\to Q_0$ に降りない」という一級の否定結果**(v122 の $d_E=d_Q\times d_\Pi$ の Q 成分が実は存在しない)⟹ **回避せず報告**。
> - **G-Q4**: `D972Q3DeleteGenerator(4,s,pair)` が pair∋s で `[]` を返すこと(§4.1・確認済)⟹ 該当生成元が $1$ に落ちる。
> - **G-Q5(較正)**: $\lvert Q_0\rvert=1{,}469{,}664$、$\lvert Q_4\rvert=583{,}152{,}628{,}325{,}845{,}597{,}028{,}352$(implementer A 実測と一致済)。

**⚠ `D972Q3WordEval(w, imgs)` の引数規約**を cert に記録すること(`w` は符号つき pair-index 列・`imgs` は PB3 pair 順)。**W-1 の再発点。**

---

## 10.2 ブロッカー② — $w_e$(corrected residual の literal word)の所在

### 10.2.1 受領票にあるもの / ないもの

| 対象 | 所在 | 状態 |
|---|---|---|
| Fox 鎖 $e_P$ そのもの | `/chief_fox` | ❌ **`executed: false`**(exact word correction で迂回) |
| **corrected residual の literal word** | ★ **`/selected_solution`** | ✅ **在り** — `correction_word: []`、`correction_index: 1`、`correction_q_coords: [0,0,0]` |
| 補正核の 27 元(literal word つき) | ★ **`/correction_fibre/records[*].word`** | ✅ **在り**(符号つき整数列・`enumerated_count: 27`・`order: 27`) |
| $\tilde D$ 診断語 | `/selected_solution/dtilde_diagnostic.word` | ✅ 在り(長い明示語) |

> ★ **決定的**: **選ばれた解の補正語は空**(`correction_word: []`・`correction_index: 1`)。
> ⟹ **$w_e$ =(補正なしの)関係語の評価値そのもの**。**別の literal word を探しに行く必要はない。**

### 10.2.2 EP-G2 の実行形(受領票だけで回る)

```gap
## w_e := 選ばれた解に対する P ブロック関係語の値(補正語が空なので追加項なし)
##   1) /selected_solution から f の語(source word)を取る
##   2) pentagon 関係語 P(.) を registry の pentagon_part_0..4 の順(§9 裁定)で組む
##   3) E4 で評価して w_e を得る
for s in [1..4] do
  Print("EP-G2 strand ", s, " : ", IsOne( Image(dE_s, w_e) ), "\n");;   # 期待: 4/4 true
od;
```
- **$(d_i)_*\epsilon_P=d_i(w_e)-1$** なので、**Fox 鎖を作る必要は無い**(`ep_del_verdict_v2.md` §3.1 の Fox 恒等式 $D_1\mathrm{Fox}(w)=w-1$)。
- **期待値 4/4 `true`**(BRUN-DEF ⟹ $w_e\in B_P$)。**非零なら (C-α) が崩れる ⟹ 以降は無意味・即報告。**

### 10.2.3 予備手順 — 工房生成の $M$ から $\epsilon_P$ を作る(元仕様 E3 の具体形)

10.2.2 が何らかの理由で回らない場合のみ:

```
E3-a  U_j, V_j を [F(x,y),F(x,y)] から取る:  [x,y], [x,y^2], [x^2,y], [[x,y],x], [[x,y],y]
E3-b  roof 条件の代用(pi 未読のため):
        全 10 context o で rho_o(U_j) = rho_o(V_j) を満たす対だけを採用
        ⟹ 真の roof-fibre 対の部分集合(cert に「代用条件」と宣言)
E3-c  a_j in F_3 を任意に取り  M := sum_j a_j (U_j - V_j)
E3-d  eta_P(M) := eps_P - sum_o sigma_o P_o sum_j a_j (rho_o(U_j) - rho_o(V_j)) xi_o   # v198 (2.2)
        ここで sigma_o = -1 は位置 3,4 のみ(§9.3)
E3-e  (d_i)_* eta_P(M) を 4 本計算
```
⚠ **E3-b の代用条件は真の roof 条件より強い**ので、**得られる結論は「その部分集合上で成立」**に留まる。**cert に必ず明記。**

---

## 10.3 実行順(更新)

1. **G-Q1 → G-Q2 → G-Q3**($d_i$ の Q 成分・§10.1.2)— **`fail` が出たらそこで停止・報告**(否定結果も一級)。
2. **40 検査**(§4.2)— Q 成分が立てば即走る。**順序非依存。**
3. **EP-G2**(§10.2.2)— **$w_e$ は受領票内。**
4. evaluator(§10.2.3 は予備)。

## 10.4 §9.4 の裁定反映(裁定 1732(c))

**v189 (1.6) の E4 転記誤りの Sol 申し送りは「不介入につき保留」と裁定された。**
⟹ 工房側は **EP-G4 mutant(v189 順序 $(1,27,21,26,28)$ を注入)で pin 済**とし、**次期 Sol 接触時のオンボーディング材料として本メモ §9 を提示する**。**本便でも Sol 文書は触らない。**

## 10.5 UNKNOWN(本節で新たに確定したもの含む)

1. **`deletions_4_3` が受領票に無い**(§10.0)— **これは受領票の欠落であり、再生成が要るなら producer 側の作業**。本メモの §10.1.2 は「受領票なしで chief_lib から組む」経路。
2. **$\bar a_{13}$ の順序**は GAP が決める(§10.1.2 G-Q2)— **私は答えを断定しない**。反証済み仮説から「もう一方」が有力だが、**G-Q2 の実測で確定させること**。
3. **削除が $Q_4\to Q_0$ に降りるか**(G-Q3)— **未検証**。降りなければ v122 の $d_Q$ 成分の存在自体が疑わしくなる ⟹ 一級の否定結果。
4. $\pi$(v191 $\Delta_0$)未読 ⟹ §10.2.3 E3-b は代用条件。
