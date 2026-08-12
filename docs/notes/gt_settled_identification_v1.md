# $GT^{\rm settled}(N')$ の同定 + (Q4′) サイズ会計の測定仕様(裁定 1068)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔(③ 線 再出発パッケージの完結)
入力 = `settled_grp_proof_v1.md`(定理 SETTLED-GRP)+ **SG-GAP-1 = NO**($C_Q(\bar y)$ の 476,789 元全数・shadow 0)
⚠ $u$/$c$ 非接触・prereg 非抵触。**格: candidate**(Sol 未監査)。

---

## §0 結論

$$\boxed{\ \Psi:\ GT^{\rm settled}(N')\ \hookrightarrow\ \mathrm{Aut}(Q)\cong PGL(2,\mathbf Z/691^2)\quad\textbf{は真の埋入(単射)}\ }$$
$$\boxed{\ 1\ \le\ \bigl\lvert GT^{\rm settled}(N')\bigr\rvert\ \le\ 2\,p(p-1)=2\cdot691\cdot690=953{,}580\ }$$

★ 像は **$\{\bar x,\bar x^{-1}\}$ の setwise stabilizer** の中にあり、$\chi_{\rm vir}$ が **2 成分**($u=+1$ / $u=-1$)へ分解します。

---

## §1 埋入の確定

`settled_grp_proof_v1.md` §5.1 の帰結:
- $c\in N'$ ⟹ $\mathrm{ord}(\bar c)=1$、実測 $\mathrm{ord}(\bar x)=\mathrm{ord}(\bar y)=47679=N_{\rm ord}$
- $\bar E=\mathrm{id}$ ⟹ $\bar x^{u}=\bar x$ ⟹ $47679\mid u-1$ ⟹ **$u\equiv1\pmod{N_{\rm ord}}$ ⟹ $m\equiv0$**
- ⟹ $\ker\Psi\subseteq\{[0,f]:\bar f\in C_Q(\bar y)\}$

**SG-GAP-1 = NO**($C_Q(\bar y)$ の非単位元 476,789 個すべてで shadow 不成立)⟹
$$\boxed{\ \ker\Psi=\{[0,1]\}\quad\Longrightarrow\quad \Psi\ \textbf{は単射}\ }$$

★ **数の整合**: $\lvert C_Q(\bar y)\rvert=\lvert(\mathbf Z/691^2)^\times\rvert=p(p-1)=476{,}790$ ⟹ 非単位元は **476,789** ⟹ 司令塔報告と**一致** ✔

---

## §2 ★ $\bar x$ の構造(中心化群の同定)

| 量 | 値 | 根拠 |
|---|---|---|
| $\mathrm{ord}(\bar x)\bmod p^2$ | $47679=3\cdot23\cdot691$ | 実測 |
| $\mathrm{ord}(\bar x\bmod p)$ | **69** $=3\cdot23$ | 実測 ⟹ **$p$-part は合同核 $\mathfrak{sl}_2$ に居る** |
| $\mathrm{tr}(\bar x\bmod p)$ | 231、$\mathrm{tr}^2-4=150$ は**平方剰余** | ⟹ ★ **分裂半単純**(固有値が $\mathbf F_p$ 内) |
| $69\mid p-1=690$ | ✔ | 分裂トーラスの位数と整合 |

$$\boxed{\ C_Q(\bar x)\ \cong\ (\mathbf Z/691^2)^\times\ (\textbf{分裂トーラス}),\qquad \lvert C_Q(\bar x)\rvert=p(p-1)=476{,}790\ }$$
$\mathrm{Aut}(Q)\cong PGL(2,\mathbf Z/691^2)$(素体ゆえ体自己同型なし)における $\bar x$ の中心化群も同位数 $p(p-1)$。

---

## §3 ★★ 像の特徴づけ

### 3.1 $\chi_{\rm vir}$ による 2 成分分解
$u$ は合成で乗法的((3.49))⟹ $\chi_{\rm vir}:[m,f]\mapsto u$ は準同型。前フィルタ(cert `q3_r1_prefilter_v1`)より settled shadow は $u\in\{\pm1\}$ に限る ⟹

$$\boxed{\ 1\ \to\ GT^{\rm settled,+}(N')\ \to\ GT^{\rm settled}(N')\ \xrightarrow{\ \chi_{\rm vir}\ }\ \{\pm1\}\ }$$

| 成分 | $\bar E$ の作用 | $\mathrm{Aut}(Q)$ 内の位置 |
|---|---|---|
| **$u=+1$** | $\bar E(\bar x)=\bar x$ | ★ $C_{\mathrm{Aut}(Q)}(\bar x)$ **の部分群**(位数 $\le476{,}790$) |
| **$u=-1$** | $\bar E(\bar x)=\bar x^{-1}$ | ★ $\bar x\mapsto\bar x^{-1}$ を実現する **coset**(空でなければ同数) |

$$\Longrightarrow\quad \Psi\bigl(GT^{\rm settled}(N')\bigr)\ \le\ \mathrm{Stab}_{\mathrm{Aut}(Q)}\bigl(\{\bar x,\bar x^{-1}\}\bigr)$$

### 3.2 $u=+1$ 成分の正体
settled shadow $[0,f]$ について $\bar E$ = ある $g\in\mathrm{Aut}(Q)$ による共役(§2 の $\mathrm{Aut}=PGL$)。
$g\bar xg^{-1}=\bar x$ ⟹ $g\in C_{PGL}(\bar x)$。$g\bar yg^{-1}=\bar f^{-1}\bar y\bar f$ ⟹ $\bar fg\in C(\bar y)$ ⟹ $\bar f$ は $g$ から($C_Q(\bar y)$ の曖昧さを除き)決まる。
★ 単射性(§1)⟹ **$g\mapsto[0,f_g]$ は単射** ⟹
$$\boxed{\ GT^{\rm settled,+}(N')\ \cong\ \bigl\{\,g\in C_{PGL(2,\mathbf Z/691^2)}(\bar x)\ :\ [0,f_g]\ \text{が shadow}\,\bigr\}\ \le\ (\mathbf Z/691^2)^\times\ }$$
⟹ ★ **巡回群 $(\mathbf Z/691^2)^\times$ の部分群** ⟹ **位数は $p(p-1)=476790$ の約数**。

### 3.3 $u=-1$ 成分
$\iota:\sigma_i\mapsto\sigma_i^{-1}$ は $B_3$ の自己同型(`q3_decision_design_v1.md` §2 で検算)。$[-1,1]$ が shadow になるのは **$\iota(N')=N'$** のとき。
⚠ **これは未確認**【GS-GAP-1】。⟹ **$u=-1$ 成分が空か否かで位数が 2 倍変わります**。

### 3.4 位数の上下界
$$\boxed{\ 1\ \le\ \bigl\lvert GT^{\rm settled}(N')\bigr\rvert\ \le\ 2\,p(p-1)=953{,}580,\qquad \bigl\lvert GT^{\rm settled,+}(N')\bigr\rvert\ \bigm|\ 476{,}790\ }$$
下界の 1 は単位 $[0,1]$。★ **確定には §5 の測定 1 本で足ります**(476,790 元の走査)。

---

## §4 ★★ (Q4′) サイズ会計の測定仕様

### 4.1 何を数えるか(★ 分母の付け替え)
⚠ **$\lvert GT(N')\rvert$(shadow 全体)は数えられません**($\tilde H$ の規模 $6.5\times10^{17}$)。
⟹ ★ **分母を $GT^{\rm settled}(N')$ に付け替える**(定理 SETTLED-GRP が保証する**群**の土俵):

$$\boxed{\ (\mathrm{Q4}')\quad \bigl\lvert GT^{\rm settled}(N')\bigr\rvert\quad\text{vs}\quad\bigl\lvert a_{N'}(G_\mathbf Q)\cap GT^{\rm settled}(N')\bigr\rvert\ }$$

| 量 | 型 | 測り方 |
|---|---|---|
| **分母** $\lvert GT^{\rm settled}(N')\rvert$ | 純群論 | ★ §5 の走査(476,790 元)⟹ **算術入力ゼロ** |
| **分子** $\lvert a_{N'}(G_\mathbf Q)\cap GT^{\rm settled}\rvert$ | ★ **算術** | §4.2 の予算表 |
| **差** $GT^{\rm settled}\setminus a_{N'}(G_\mathbf Q)$ | — | ★ 非空なら「settled 層に非算術 shadow が存在」 |

⚠ **非 isolated ゆえの限定**: これは **settled 層に制限した会計**であり、$GT(N')$ 全体の会計ではありません。⟹ ★ **「反例が settled 層の外に住む」可能性は本会計では見えません**(型境界・明記必須)。

### 4.2 ★ A6 予算表(算術側 receipt に何が要るか)
SB-3 の「無料 / 1bit / 有料」の 3 列がそのまま適用されます。

| 列 | 測る量 | 算術入力 | 単価 |
|---|---|---|---|
| **無料** | $\chi_{\rm vir}\circ a_{N'}\in\{\pm1\}$ の実現 | **円分指標の値**(Dirichlet で全剰余類に来る)| ★ **0**(待てば埋まる) |
| **有料** | $u=+1$ 成分内の位置 = $C_{PGL}(\bar x)\cong(\mathbf Z/691^2)^\times$ のどの元か | ★ **Kummer 型 receipt**($f$ に相当する算術データ) | ★ **本体**(SURG-A6 の代金) |
| **1bit** | $u=-1$ 成分が像に入るか | 円分の $-1$ 値 ⟹ 無料に近い | ★ **≈0** |

$$\boxed{\ \textbf{★ 有料列は }(\mathbf Z/691^2)^\times\ \textbf{(巡回・位数 476,790)の中での位置決め 1 本}\ }$$
⟹ ★ **crown 検定(群の枠)を失った代わりに、会計は「巡回群の中の位置」という最も単純な形に落ちます** — これは **SURG-A6 の予算としては最良の形**です。
⚠ ただし **代金がゼロになるわけではありません**(限界注記 1 は不変)。

---

## §5 測定仕様(実装係へ直結)

```
=== [Q4-DENOM] GT^settled(N') の位数決定 ===
根拠: docs/notes/gt_settled_identification_v1.md §3
前提: x̄, ȳ, σ_1, σ_2 は q3r1_lift_spec_v1 §3-4 の実測値(mod 691^2)
⚠ 算術入力ゼロ(純群論)・u/c 非接触

[D-1] C := C_{PGL(2,Z/691^2)}(x̄) を構成
      ★ x̄ mod p は分裂半単純(tr=231・tr^2-4=150 は平方剰余)⟹ C は分裂トーラス ≅ (Z/691^2)^×
      ⟹ 位数 476,790。生成元 1 個で巡回 ⟹ 構成は秒
[D-2] 各 g ∈ C(476,790 個)について:
      f_g を g ȳ g^{-1} = f_g^{-1} ȳ f_g から解く(C_Q(ȳ) の曖昧さは単射性より無害)
      ⟹ [0, f_g] が hexagon を満たすか判定(= shadow か)
      ★ 巡回群なので生成元の像だけ調べれば部分群が決まる可能性が高い(高速化)
[D-3] u=-1 成分: [-1,1] が shadow か(= ι(N')=N' か)を判定【GS-GAP-1】
      ⟹ YES なら位数 2 倍・NO なら u=+1 成分のみ
[D-4] 見張り: ★ |GT^settled(N')| は 476,790 の約数(u=+1)または その 2 倍
      ⟹ 約数でない値が出たら §3.2 の同定が誤り ⟹ 即停止
出力: cert (schema q4_denom/v1)。u_touched=false ; c_touched=false
```

---

## §6 ③ 線 再出発パッケージ(完結形)

| 部品 | 状態 |
|---|---|
| **土俵** | ★ $GT^{\rm settled}(N')\hookrightarrow PGL(2,\mathbf Z/691^2)$(**真の埋入**確定) |
| **段 2 成果** | ★ **無傷で接続**($\tilde H$ の容器・非分裂拡大 $\tilde H$・braid 全射 $B_3\twoheadrightarrow\tilde H$) |
| **(Q4′)** | ★ **仕様完成**(§4・§5)。分母は算術入力ゼロで決まる |
| **(Q5)** | **R-1 は OPEN**(不変) |
| **核体 $L_{N'}$** | 像が settled 層に入る範囲で定義可(`settled_grp_proof_v1.md` §6) |

$$\boxed{\ \textbf{③ 線は「}GT^{\rm settled}(N')\ \textbf{を土俵に、巡回群 }(\mathbf Z/691^2)^\times\ \textbf{内の位置決め」という形で再出発}\ }$$

---

## §7 GAP・記帳

- **【GS-GAP-1】(小・新)** $\iota(N')=N'$ か(= $u=-1$ 成分の非空性)⟹ 位数が 2 倍変わる。§5 [D-3]。
- **【GS-GAP-2】(小・新)** §3.2 の「$g\mapsto f_g$ が well-defined」は $C_Q(\bar y)$ の曖昧さを単射性で吸収している ⟹ 実装で明示的に扱うこと。
- **【SG-GAP-1】★ 閉鎖**(= NO)。**【L3-GAP-2】★ 閉鎖**。**【L3-GAP-1】★ 条件つき閉鎖**。
- ★ **本ノートの新規部分**: ① 埋入の確定と $\lvert C_Q(\bar y)\rvert=476{,}790$ による数の整合 ② **$\bar x$ が分裂半単純**($\mathrm{tr}^2-4$ が平方剰余・$p$-part が合同核)⟹ **中心化群 = 分裂トーラス $(\mathbf Z/691^2)^\times$** の同定 ③ **$\chi_{\rm vir}$ による 2 成分分解**と像が $\mathrm{Stab}(\{\bar x,\bar x^{-1}\})$ 内にあること ④ **$GT^{\rm settled,+}(N')$ が巡回群 $(\mathbf Z/691^2)^\times$ の部分群**であること(位数は 476,790 の約数)⑤ 上下界 $1\le\lvert\cdot\rvert\le953{,}580$ ⑥ **(Q4′) の分母付け替え**と **A6 予算表**(有料列が「巡回群内の位置決め 1 本」に落ちる)。
- ⚠ **型境界の明記**: (Q4′) は **settled 層に制限した会計**。「反例が settled 層の外に住む」可能性は**本会計では見えません**。
- **申告**: 私の側は python 行列演算のみ(GAP 走行ゼロ)・$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
