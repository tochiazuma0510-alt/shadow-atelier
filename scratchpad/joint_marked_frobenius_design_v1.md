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

## 4. ~~★ **UNKNOWN(1 点・ここが全部)** — 正規化定数 $c$ の出所~~

> ### ⚠⚠ **本節は §6 で解消された(2026-08-28・裁定 1731(b))**
> **$c$ は不要になった。** §6 の再定式化により、SELECT は **$c$ を一切通らない有限計算**に落ちる。以下 §4/§5 は**歴史的記録**として残す(三択 (α)(β)(γ) の調査結果は §6.1 に要約)。

### 4.0(歴史)当初の UNKNOWN — 正規化定数 $c$ の出所

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

---

# §6 ★ $c$ の解消(2026-08-28・裁定 1731(b) ①)— **再定式化で $c$ が消える**

## 6.1 三択の調査結果

| 案 | 調査 | 結果 |
|---|---|---|
| **(β) 2405 Thm 4.3 からの導出** | 原文 `papers/txt/2405.11725-…txt` L945–957(Thm 4.3)+ Thm 5.2 の証明を精読 | ★ **半分成功 — GT 側から $c$ が消えた**(§6.2) |
| **(α) P1 corpus 本文の grep** | 索引に無いことは既確認。**本文**(`docs/notes/fam_u_assembly_v1.md` 等 P1 系)を grep | ❌ **空振り**。ヒットする "Kummer" は全て **B-5 の窓 torsor 類 $[u_n]_{2n}$(83/K9 線)**で、**二面体 GT-shadow の $k_\sigma$ marking ではない**。⟹ **(α) は正式に閉じる — §7.3.2 S7 の「P1 corpus の marking で符号確定」は裏づけを持たない**(要訂正) |
| **(γ) mod 9 アンカー** | (β) が $c$ を消したので**不要になった** | **不要** |

## 6.2 (β) の成果 — **$k$ は正典が pin する内在量。$c$ は GT 側の自由度ではない。**

**2405 Thm 4.3(逐語・L945–952)**:
$$GT(K^{(n)})=\bigl\{(m,(r^{2k},r^{-2k},r^{\kappa(m)}))\ \bigm|\ m\in X_n,\ k\in\mathbb Z\bigr\}\quad(4\nmid n)$$
**Thm 5.2 の証明(逐語)**: "Let $f:=x^{2k}y^{-2k}z^{\kappa(m)}$" ⟹ **$f$ の語形まで明示**。

⟹ **$k$ は第 1 $D_n$ 成分の指数($r^{2k}$)から直接読める内在座標**で、**任意定数は入らない**。

**機械確認**(`scratchpad/math_thm43_k_v1.g`・$\psi_9$ は 2405 (3.1) $x\mapsto(r,s,s),\ y\mapsto(rs,r,rs)$):
```
gate: D_9 order=18 ; s r s^-1 = r^-1 : true
      |G_9| = 2916  = 4n^3 (n odd) : true
      psi(x^{2k} y^{-2k} z^{kappa}) = (r^{2k}, r^{-2k}, r^{kappa})  for all k in [0..8], kappa even : TRUE
      2^-1 mod 9 = 5   =>  k = 5 * (exponent of r in the 1st component) mod 9
```
> ### ★ 副産物の canary(記録)
> 最初 $\kappa$ を $0..8$ 全域で走らせたところ **奇数 $\kappa$ で全滅**した。原因は $\psi_9(z)$ の第 1・第 2 成分が**鏡映**(位数 2)であること。
> **しかし $\kappa(m)=m+1$($m$ 奇)/ $-m$($m$ 偶)は常に偶数**なので、奇数 $\kappa$ は**そもそも出現しない** ⟹ 公式は無傷。
> ⟹ **「$\kappa(m)$ は常に偶数」は実装が守るべき不変条件**(破れば $\psi_n$ 評価が鏡映成分を拾って壊れる)。**新規 canary として登録を具申。**

## 6.3 ★ 再定式化 — **SELECT は $c$ を通らない**

$c$ が要るのは「Kummer 指標経由で Frobenius row を作る」経路だけである。**その経路を使わない。**

$$\boxed{\ A_{c'}\cap X^0=\ker\bigl(\Psi-c'\mathcal K_3\bigr)\big|_{X^0}\quad\text{を、既知の 2 つの roster 上で直接評価する。}\ }$$

- **$\mathcal K_3$**(二面体側の $C_3$ 座標)= **Thm 4.3 の $k$ の mod 3**。**正典が pin・$c$ 不要**(§6.2)。
- **$\Psi$**(PSL 側の $C_3$ 座標)= 規約 D + $u_{\rm dih}$ アンカーで pin 済(`local3_…_v2.md` §1)。$\varepsilon$ の自由度は**アンカーが吸収済**。
- **$c'=+1$** は LOCAL-3 で確定済(**$c$ を通らない比**)。
- **2 つの roster は 324-key の明示集合**(10/10 ハッシュ一致・札 7)。

**⟹ 手順(有限・その場で回る)**
```
K1  X^0 := ker(chi mod 3) <= X     (|X^0| = 486)
K2  各 roster R in {NN-09, NN-12} について R ∩ X^0 を取る   (各 162 元のはず)
K3  R ∩ X^0 の全元で  Psi - K3  を評価
K4  恒等的に 0 になる方が c'=+1 側     ->  SELECT
K5  検算: もう一方では Psi + K3 が恒等的に 0 になること(両立しなければデータ不整合)
```
**必要な入力は $X$ の座標関数 $\mathcal K_3,\Psi$ と 2 つの key 集合だけ。Frobenius も素数も $c$ も要らない。**

> ⚠ **残る 1 ビットの所在が変わった(消えてはいない)**: $\Psi$ と $\mathcal K_3$ の**各々の $\mathbb F_3$ 同一視の向き**。
> - **$\mathcal K_3$ 側は正典が固定**(Thm 4.3 の $k$・§6.2 機械確認)✓
> - **$\Psi$ 側は規約 D + アンカーが固定**(`local3_…_v2.md` §1・8/8 機械確認)✓
> ⟹ **両方とも工房が握っている対象で固定済**。**$c$ のように「どこにあるか分からない外部定数」ではない。**
> ⟹ **実装は K3 の評価器が $\mathcal K_3$ を Thm 4.3 の $k\bmod3$ として、$\Psi$ を 規約 D の向きで実装していることを cert に宣言すること**(新 D-12)。

## 6.4 §7.3.2 S7 への訂正具申

正本 §7.3.2 の S7 コメント「(P1 corpus の marking で符号確定)」は **(α) の空振り**により**裏づけを持たない**。
⟹ **「$k_3$ はアンカー由来($S_{\rm anc}$ の離散対数)。P1 corpus は $k_\sigma$ marking を持たない(2026-08-28 grep 済)」へ差し替えを具申**(本便では正本を触らず、司令塔の裁可を待つ)。

## 6.5 UNKNOWN(残り)

1. **$\Psi$ の評価器**が census 内でどう実装されているか(規約 D 準拠か)— **未確認**。K3 の前に 1 回見ること。
2. §6.3 K2 の「各 162 元」は ORIENT §7.1 からの**予測値**。**実測で確認すること**(ずれたら $X^0$ の取り方が違う)。
3. **$\kappa(m)$ 偶数不変条件**の canary 登録(§6.2)。

---

# §7 ★ Ψ(π) 評価器の構成(2026-08-28・裁定 1734)

**契機**: implementer B が pre-check (a) で正当に停止 — 「π 列だけで回る Ψ 評価器」は repo に無く、既存 Ψ は全て S1–S9 の Frobenius/離散対数鎖経由(= §6 が置換しようとした経路そのもの)。cert = `search/certs/d972_local3_select_k15_v1_20260828.json`。

## 7.0 ⚠⚠ まず §6.3 の自己訂正 — **私は過大に書いた**

> **§6.3 の記述(訂正対象)**: 「$\mathcal K_3$ 側は正典が固定 ✓ / **$\Psi$ 側は規約 D + アンカーが固定 ✓** ⟹ 両方とも工房が握っている対象で固定済。」
> **誤り**: 規約 D + アンカーが固定したのは**幾何的な $u$ どうしの比**であって、**窓の指標 $\Psi:X^0\to\mathbb F_3$ の $\mathbb F_3$ 同一視ではない**。両者を繋ぐには**比較写像(P5′ の marked 同型)**が要る — これは私自身が §7.2 NO-CANON で「欠品の正体は正規化の欠如ではなく**比較写像の欠如**」と書いた当のものである。
> ⟹ **§6.3 の「両方固定済」は撤回。**正しくは **§7.2(Ψ 側は本節で固定できる)+ §7.4($\mathcal K_3$ 側の $r$ 選択が残る)**。
> ⟹ **implementer B の停止は正当**であり、**K1–K5 は本節の評価器を入れて初めて回る。**

## 7.1 Ψ(π) 評価器は構成可能 — **純群論・Frobenius が正準生成元**

```
gate: scratchpad/math_psi_pi_v1.g
  |PSL(2,8)| = 504   |PGL(2,8)| = 504   |PGammaL(2,8)| = 1512
  PGL = PSL (q even) ? true          [PGammaL : PSL] = 3
  PSL normal in PGammaL ? true       quotient = C3  order 3  cyclic ? true
  Frobenius (order 3, outside PSL) exists ? true ; its image generates C3 ? true
  Psi(id)=0  Psi(frob)=1  Psi(frob^2)=2 ; homomorphism on 200 random pairs ? true
```

```gap
S   := PSL(2,8);;  G := PGammaL(2,8);;
S2  := First(NormalSubgroups(G), N -> Size(N) = 504);;
nat := NaturalHomomorphismByNormalSubgroup(G, S2);;          # G ->> C3
frob:= First(Elements(G), g -> Order(g) = 3 and not g in S2);;   # Frobenius t -> t^2
PsiPi := function(g)                                          # π 列 -> F_3
  local t, im; im := Image(nat, g);
  for t in [0,1,2] do if im = Image(nat, frob)^t then return t; fi; od;
  return fail; end;;
```

> ### ★ 正準性(これが Ψ 側の D-12 を埋める)
> $P\Gamma L(2,8)/PSL(2,8)\cong C_3$ の生成元は **$\mathbb F_8$ の Frobenius $\phi:t\mapsto t^2$**。これは**体の構造から一意に決まる**(選択でない)。
> $$\boxed{\ \Psi(\phi):=1\ \ \text{— 規約でなく正準。}\ }$$
> ⟹ **π 列だけで $\mathbb F_3$ 値が返る評価器が立つ。**離散対数も素数も要らない。

⚠ **実装注意(私の script の誤りを記録)**: PSL(2,8) の**次数 9 の作用**は $\mathbb P^1(\mathbb F_8)$ 上の作用で、点固定化群は**位数 56 の Borel**($504/9=56$)。私は Sylow-3(位数 9)を取って **degree 56** を作ってしまった(`transitive false` の出力はこれが原因で、Ψ の構成には無関係)。**9T27 を作るときは `FactorCosetAction(S, Borel)` を使うこと。**

## 7.2 算術との橋(P5′)— **今は使える**

$\sigma\in G_{\mathbb Q}$ に対し、$\mathrm{Ih}(\sigma)$ の π 列は $P\Gamma L/PSL$ のどのクラスか。橋は
$$\mathrm{Frob}_p\ \longmapsto\ \phi^{\,\psi_p},\qquad \psi_p:=\log_\omega\bigl(u_0^{(p-1)/3}\bmod p\bigr),\ \ \omega=g^{(p-1)/3}$$
すなわち **$P\Gamma L/PSL$ 層の体が $\mathbb Q(\zeta_3,\sqrt[3]{u_0})$ の 3 次部分体である(P5′)** という言明を、**marked** な形で使う。

**この橋が使える根拠 2 点**:
1. **$\iota_C$ は一意**(正本 §7.3.1): 被覆は degree 9・モノドロミー PSL(2,8)(9T27・原始的)ゆえ **deck 群自明・$\mathrm{Aut}(C,t)=1$**、かつ passport 内で rigid ⟹ **marked 同型は一意**。
2. **P5($u_0=u_{S4}$)は実質確認済**: falsifier が producer code L118/L120 の明示宣言 + $T=1/t$ 代数で判読(裁定 1719)。cert の `unconfirmed` 自己申告は**この判読より前のもの**。
⟹ **Ψ 側は正準生成元(§7.1)+ 一意な比較写像(1)+ 確認済の同定(2)で完全に pin される。**

## 7.3 ★ 二経路相互検算(DC 級・**これが本節の実用価値**)

| 経路 | 入力 | 出力 |
|---|---|---|
| **経路 A(既存・S1–S9)** | $p$、$u_0$、$\zeta_9/\omega$ | $\psi_p=2$($p=19,37,73$ で実測済) |
| **経路 B(新・π 列)** | D972 key の π 列のみ | $\Psi_\pi\in\{0,1,2\}$ |

**整合すべき点(明示)**:
$$\boxed{\ \text{任意の }\sigma\ \text{に対し}\quad \Psi_\pi\bigl(\pi\text{-column of }\mathrm{Ih}_M(\sigma)\bigr)\ =\ \psi_\sigma\ \ (\text{経路 A の値})\ }$$
とくに **$p=19,37,73$ で経路 A が $\psi=2$ を返している**ので、**$\mathrm{Ih}_M(\mathrm{Frob}_p)$ の π 列は $\phi^2$-クラスでなければならない**。
⟹ **経路 B で $\Psi_\pi=2$ を返す key の集合**が、$A=\mathrm{Im}(\mathrm{Ih}_M)$ の $\mathrm{Frob}_p$ 像を含む集合である。
**両経路一致 = DC 級の相互検算**(片方だけの実装ミスを検出する)。⚠ ただし**これ自体は SELECT を決めない**(§7.4)。

## 7.4 ★ 残る 1 ビットの正確な所在 — **$\mathcal K_3$ 側の $r$ 選択**

$\mathcal K_3$ は 2405 Thm 4.3 の $k\bmod3$ だが、**$k$ は $D_n$ の生成元 $r$ の選択に相対**である:
$$r\mapsto r^a\ (a\in(\mathbb Z/9)^\times)\ \Longrightarrow\ k\mapsto a^{-1}k\ \Longrightarrow\ \mathcal K_3\mapsto (a\bmod 3)^{-1}\mathcal K_3 .$$
$a\equiv2\ (3)$ で**符号反転**。⟹ **$r$ の選択が残りの 1 ビット。**

**閉じ手の候補(未実行)**: 二面体側の被覆(Chebyshev $T_9$・$u_{\rm dih}=\pm2^{-7}$)でも **$\mathrm{Aut}(\text{cover})=1$**(`math_udih_v1.g` で機械確認済)なので、**PSL 側と同型の rigidity 論法で $r$ が正準に決まる可能性がある**。
⚠ ただし **Galois 閉包の $C_9$ には $\mathrm{Out}$ が作用する**ので、「被覆の $\mathrm{Aut}$ が自明」から直ちに「$r$ が一意」は**出ない**。**私は verify していない。**⟹ **UNKNOWN(名前つき標的)**。

> **⟹ 正直な現状**: K1–K5 は **§7.1 の評価器を入れれば回る**が、**SELECT の最終ビットは $\mathcal K_3$ 側の $r$ 選択に移った**。$c$(所在不明の外部定数)ではなく、**幾何側の明示された選択**である点は前進。

## 7.5 それでも今すぐ走る価値がある検査(**SELECT なしでも一級**)

$r$ の選択を**任意に固定**して(どちらでもよい)次を回す:

```
V1  X^0 := ker(chi mod 3)      |X^0| = 486        (実測済)
V2  各 roster R について R ∩ X^0 を取る            (各 162 — 実測済・ORIENT 予測一致)
V3  Psi_pi と K3 を X^0 の全 486 元で評価
V4  ★ 検査: 一方の roster ∩ X^0 上で Psi_pi - K3 ≡ 0、
            もう一方で Psi_pi + K3 ≡ 0 になるか
```
> **V4 が通れば、ORIENT §7.1 の構造($A_{c'}\cap X^0=\ker(\Psi-c'\mathcal K_3)$)が実データで初めて検証される。**
> **通らなければ、ORIENT の型付けか roster か評価器のどれかが誤り** ⟹ **一級の否定結果**。
> ⚠ **V4 は $r$ の選択に依らない**(選択を変えると 2 つの roster の役割が入れ替わるだけで、「片方が $-$、他方が $+$」という構造は不変)。⟹ **今すぐ回せて、しかも決定的。**

## 7.6 較正必達値

| 量 | 値 | 出所 |
|---|---|---|
| $\lvert PSL(2,8)\rvert=\lvert PGL(2,8)\rvert$ | **504** | §7.1 `gate:` |
| $\lvert P\Gamma L(2,8)\rvert$ | **1512** | 同 |
| $[P\Gamma L:PSL]$ | **3**、商 $\cong C_3$ | 同 |
| $\Psi_\pi(\phi)=1$、$\Psi_\pi(\phi^2)=2$、$\Psi_\pi(1)=0$ | — | 同 |
| $\lvert X^0\rvert$ | **486** | implementer B 実測 |
| 各 roster $\cap X^0$ | **162 / 162** | implementer B 実測(ORIENT 予測一致) |
| $\lvert X_2\rvert$、$X_2^{\rm ab}$ | **54**、$C_6$ | d972 §6.6 P-c(既測) |
| 経路 A の値 | $\psi=2$($p=19,37,73$) | 既存 S1–S9 |

## 7.7 UNKNOWN

1. ★ **$\mathcal K_3$ 側の $r$ 選択**(§7.4)— **SELECT の最終ビット**。rigidity で閉じる可能性はあるが**未検証**。
2. **π 列の実体**: D972 key から $P\Gamma L(2,8)$ の元(またはそのクラス)をどう取り出すかの**データ経路**を私は確認していない(census が π 列をどう格納しているか)。**§7.1 の評価器は「$P\Gamma L$ の元が与えられたら」の部分**であり、**key → π 列の抽出は implementer 側で 1 回確認が要る**。
3. **V4 が通るか**(§7.5)— 未実行。**通らなければ ORIENT の型付けを見直す**。
4. §6.5 の残項(census 内 Ψ 評価器の規約 D 準拠確認)は **本節で「存在しない」と確定**したので、**新規に §7.1 を実装する**のが正しい対応。
