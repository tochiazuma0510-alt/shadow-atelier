# joint marked Frobenius row の測定設計 v1 — 216 行問題の真の閉じ手

`DIR: 972 の 1 ビット(SELECT)/ FRAME: B₃-gentle・IDX3`
**委嘱**: 司令塔・裁定 1726 ①。**c′=+1 の生値は確定済(anchor v2 §1)。残るのは translation bit。**
**格**: §1–§2 = `paper-proof`(構造の同定)。§3 = 設計(実装粒度)。§4 = **UNKNOWN(1 点)**。
**著者**: 数学者(Opus 5)/ 2026-08-28。**規約 (R-1)(R-2) 準拠。**

---

## 1. ★ 測定の正体 — **名前を経由しない**

census producer の `first_missing_datum`(`search/d972_idx3_arithmetic_producer_v2.py` L972–993)の `required_fields` 5 本を読んだ。**この測定の本質は次の 1 行である**:

> $$\boxed{\ \textbf{具体的な D972 key を 1 本測り、2 つの 324-key roster への「所属」を直接照合する。}\ }$$

- **どちらの roster が「$c'=+1$ 側」かを知る必要はない。**名前(NN-09 / NN-12)は辞書式順位で意味論ゼロ(falsifier 裁定 1726)だが、**集合そのものは 10/10 のハッシュで確定済**(札 7)。⟹ **所属判定は名前を通らない。**
- ⟹ **これが「translation bit」の正体**であり、**census 側に何かを書かせる話ではない**(§2 の宛先差替と整合)。

**なぜ 1 本で足りるか**: $A$ は位数 324 の部分群で $A\in\{A_+,A_-\}$。$A_+\cap A_-$ は位数 108、対称差は 432 key。⟹ **測った row が対称差に落ちれば所属は一意に決まる。**(落ちなければ判別不能 ⟹ 別の $\sigma$ を取り直す。§3 の DC-9。)

---

## 2. (i) P-a はこの測定に必要か — **必要。アンカー機構では消せない。**

| 自由度 | $c'$(比)への効き方 | **絶対 row への効き方** |
|---|---|---|
| $\mu_3$ フレーム($\omega:=g^{(p-1)/3}$ の取り方) | **相殺**(DC-2・両側同一フレーム) | **相殺**(要求フィールドが「同一 μ₃ フレーム」を明記しているのはこのため) |
| $\zeta_9$ 埋め込み($\zeta_9\mapsto\zeta_9^a$) | **相殺**(ORIENT (a): $\mathcal K_3,\Psi$ が同じ捻れで同時スケール) | ★ **相殺しない**。$e_\sigma\mapsto a^{-1}e_\sigma$ ⟹ $k$ が変わる ⟹ **roster が入れ替わりうる** |
| 正規化定数 $c\in(\mathbb Z/9)^\times$ | **相殺**(比に効かない) | ★ **相殺しない**。$k\equiv\tfrac12c\,e$ ⟹ $c\bmod3$ の符号が $k$ の符号を決める |

> ### ★ なぜアンカーで消せないか(1 行)
> **$u_{\rm dih}$ アンカー(完全立方の不可視性)が消すのは「比」の規約であって、「絶対値」の規約ではない。** row は絶対量なので、アンカーの相殺機構は原理的に届かない。
> ⟹ **P-a(埋め込み + $c$)は load-bearing。**

**$m$ 座標は規約不要だが情報ゼロ**: $\chi(\mathrm{Frob}_p)=p$ より $m=(p-1)/2\bmod18$ は**完全に規約なしで決まる**。しかし falsifier 実測 F2「両 roster は同一 $\varphi_m$ 分割・$\lambda\to-\lambda$ だけが違う」より、**$m$ 座標は両 roster で同一分布** ⟹ **判別力ゼロ**。⟹ **$\lambda$(= $k$)座標が必須**、したがって P-a が必須。(ORIENT (e) の「census から無料の 1 ビットは取れない」の再確認。)

**複素共役は使えない(確認)**: $\mathrm{Ih}_M(c)=[m_c,1]$、$2m_c+1=-1$ ⟹ $m_c=17$(charming ✓)。しかし $f_c=1$(Ihara ICM 1990 §2.3 逐語 pin・C-14 で使用)ゆえ $\mathcal K_3=\Psi=0$ ⟹ **$A_+\cap A_-$(位数 108)に落ちる** ⟹ **判別力ゼロ**。⟹ **$\mathcal K_3(\sigma)\ne0$ なる $\sigma$ が要る**。

---

## 3. (ii)(iii) 実行設計

### 3.1 素点の選択 — **既用素数で足りる**

条件: (a) $p\equiv1\pmod 9$($\mu_9\subset\mathbb F_p$)、(b) $p\nmid2\cdot3\cdot5$、(c) LOCAL-3 (iii) の両側非自明。
**$p=19$**: $m=(19-1)/2=9$ ⟹ $\gcd(2\cdot9+1,18)=\gcd(19,18)=1$ ✓ **charming**、$9$ は charming 表 $[0,2,3,5,6,8,9,11,12,14,15,17]$ に在り ✓。**(c) は `math_s4norm_v1.py` の 8/8 走に $p=19$ が含まれており非退化を実測済** ✓。
⟹ **新しい素数計算は不要。$p=19$ を第一候補、$37,73,163$ を DC-9 の再試行用に。**

### 3.2 $a_M(\mathrm{Frob}_p)$ の実計算手順(2 座標)

| 座標 | 式 | コスト | 規約依存 |
|---|---|---|---|
| $m$ | $m\equiv\dfrac{p-1}{2}\pmod{M_{\rm ord}=18}$($\chi(\mathrm{Frob}_p)=p$) | **$O(1)$** | **なし** |
| $k$($\lambda$ 座標) | $k\equiv\tfrac12\,c\cdot e_p\pmod 9$、$e_p:=\log_{\zeta_9}\!\bigl(\beta^{(p-1)/9}\bmod p\bigr)$、$\beta=2$(候補) | **ミリ秒** | ★ **$c$ と $\zeta_9$ 埋め込み** |
| row | Thm 4.3 座標 $(m,(r^{2k},r^{-2k},r^{\varkappa(m)}))$ から canonical key へ | census の key 化ルーチンを再利用 | — |

**⟹ 幾何(被覆・Belyi 写像・点数え)は一切不要。**必要なのは $p$、$\beta$、$\zeta_9$ 埋め込み、$c$ の 4 つだけ。

### 3.3 PSL 側 Frobenius(同一 $\mu_3$ フレーム)

$\omega:=g^{(p-1)/3}$($g$ = $\mathbb F_p$ の原始根・**$k$ 側と同一の $g$**)で
$$\Psi(\mathrm{Frob}_p)=\log_\omega\bigl(u_{S4}^{(p-1)/3}\bmod p\bigr),\qquad u_{S4}=u_0 .$$
**規約 D の正規化因子 $\pm3\sqrt{-3}$ は完全立方ゆえ無視してよい**(anchor v2 §1.2・8/8 機械確認)。

### 3.4 実装手順(implementer 粒度)

```
J1  p := 19 ;  g := 素根 ;  zeta9 := g^((p-1)/9) ;  omega := g^((p-1)/3)      # 同一 g を両側で
J2  e_p  := discrete_log(2^((p-1)/9) mod p, base=zeta9)          # in Z/9
J3  k    := (1/2)*c*e_p mod 9                                    # ★ c は P-a 入力(§4)
J4  m    := (p-1)/2 mod 18                                       # 規約なし
J5  row  := canonical_key( m, k )      # Thm 4.3 -> D972 canonical key(census の key 化を再利用)
J6  psi  := discrete_log(u0^((p-1)/3) mod p, base=omega)         # PSL 側・同一フレーム
J7  一貫性: k mod 3 と psi の比が c'(= +1) と一致するか      # 既知値との突合(自己検査)
J8  SELECT := (row in NN09_keys) ? "NN-09" : ((row in NN12_keys) ? "NN-12" : UNDECIDABLE)
J9  対称差検査: row が NN-09 △ NN-12(432 key)に属すること     # 属さねば UNDECIDABLE
```

### 3.5 破壊対照(必須)

| # | 対照 | 期待 |
|---|---|---|
| **DC-9(対称差)** | `row` が 432-key 対称差に属することを検査 | **属さねば判別不能で停止**(別の $\sigma$/$p$ へ)。属さないのに SELECT を返したら fail-closed 違反 |
| **DC-10($c$ 反転)** | $c\mapsto-c$ で再走 | **SELECT が入れ替わる**。入れ替わらなければ $k$ が実装に効いていない |
| **DC-11(埋め込み flip)** | $\zeta_9\mapsto\zeta_9^{-1}$ で再走 | **SELECT が入れ替わる**(§2 の表)。⚠ **$c'$ とは違って不変ではない** |
| **DC-12($m$ 単独)** | $m$ 座標だけで判別を試みる | **必ず判別不能**(F2: 同一 $\varphi_m$ 分割)。判別できたら roster データが壊れている |
| **DC-13(複素共役)** | $\sigma=c$($[17,1]$)で走らせる | **$A_+\cap A_-$ に落ちて判別不能**。判別できたら $f_c=1$ の pin か roster が壊れている |
| **DC-14(素数間一貫性)** | $p=19,37,73$ で SELECT 一致 | 不一致なら $\beta=2$ か linkage が偽 ⟹ STOP |

### 3.6 出力 cert 必須欄(producer の `required_fields` 5 本に対応)

1. `prime`: $p$、$\mathbb Q(\zeta_9)$ の素イデアル、**`zeta9_to_Fp` 規約(生成元 $g$ と $\zeta_9=g^{(p-1)/9}$)**
2. `a_M_Frob`: 測った canonical D972 row + **$k$ 座標の正規化(`c` の値と出所)**
3. `psl_frobenius`: $\Psi(\mathrm{Frob}_p)$ と **同一 $\mu_3$ フレーム $\omega=g^{(p-1)/3}$ の明示**
4. `restriction_values`: 全成分の制限値 + 単数指数/共役子規約
5. `diagram`: $\mathbb Q$ と $\mathbb Q(\zeta_3)$ 上の base-change/restriction/conjugation 図式
\+ 本設計固有: `c_source`(§4)、`symmetric_difference_membership`(DC-9)、`anchor_source:"u_dih"`、`reduction_index_order:"source_first"`

---

## 4. ★ **UNKNOWN(1 点・ここが全部)** — 正規化定数 $c$ の出所

**$c\bmod 3\in\{\pm1\}$ が決まれば、216 行問題は $p=19$ のミリ秒計算で完全決着する。**($c\bmod 9$ の完全形は mod 9 marking にのみ必要で、SELECT には $c\bmod3$ で足りる。)

**正本 §7.3.2 の S7 は「P1 corpus の marking で符号確定」と書いているが、私が `docs/notes/p1_corpus_index_v1.md` を検索した限り、正規化定数 $c$ / Kummer 指数 $k_\sigma$ / marking 規約に該当する項目は索引に無い**(§11「見つからなかった項目」にも未記載)。

⟹ **格 = UNKNOWN。以下の三択を司令塔裁定に上げる**:

| 案 | 内容 | 判定 |
|---|---|---|
| **(α)** | P1 の**本文**(索引ではなく)に $c$ が pin されている | **要確認**(索引に項目が無いだけかもしれない)⟹ **最優先で確認すべき 1 点** |
| **(β)** | $c$ は 2405 Thm 4.3 の marking 規約から**導出できる**($\varkappa(m)$ の定義と $k$ の符号の突合) | **紙で closable の可能性**。$k=\varkappa(m)/2$ 型の関係が Thm 4.3 に明示されているなら $c$ は定数として読める |
| **(γ)** | どこにも無い ⟹ **$c$ 自体が新規に決めるべき量**で、決め方は「幾何側($K^{(9)}$ の cover の $\mu_9$ 作用)と Kummer 側の突合」= **$u_{\rm dih}$ アンカーの mod 9 版** | **新規作業**(mod 3 版は済んでいるので延長線上) |

> ⚠ **推測で $c=1$ とおいてはならない。** $c\bmod3$ の符号が SELECT を直接反転させる(DC-10)。**$c$ の出所を明記せずに SELECT を宣言することは、falsifier が指摘した「50/50 の後付け選択の制度化」そのものである。**

**⟹ 本設計は「実行可能な形まで書けたが、入力 1 個($c$)が未定」という状態。**(iii) の実計算は $c$ さえ入れば**ミリ秒**であり、幾何計算は一切不要。**不能ではなく、欠品 1 個。**

---

## 5. 副産物 — この測定が閉じると何が従うか

$\mathrm{SELECT}$ が決まる ⟹ $A$ が 324 key の具体集合として確定 ⟹ **$X\setminus A$ の 648 元が名指しで確定**(うち **432 は既に確定非算術**、**216 が保留中**)⟹ **216 行問題が完全決着**。
⚠ ただし **648 の genuine/fake 判定は別問題**(DICHOT-972 の枝・§8)。SELECT は「どれが非算術か」を決めるだけで、「非算術元が genuine か」は決めない。**混同禁止。**
