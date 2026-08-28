# D972 / IDX3 — 算術 datum 2 件の**独立導出**(工房検収用・第三系統)

`DIR: 正側(648 一括出口 IDX3 の pin 3/5)/ FRAME: B₃-gentle・窓 M=K^(9)∩N_{S4}`

**状態札**: `mixed — §1〜§2 は定理+機械確認(artifact 直読・二重確認)/ §3 は導出済みの形(shape)+ candidate な算術同定 / §4 は受領手続き(定理)/ §6 = Sol 便 159 §17 敵対監査後の versioned 訂正(ブラインド解除済)`

> ⚠ **現行正本 = 「v1 本文 + §6 訂正」**。**§4.1 の「$d=1$ なら 324 が矛盾」と §3.3 の $m=(t-1)/2\bmod18$ は §6 で撤回・訂正済み**(§3.2 の linkage 同定も §6.3 で再型付け)。§1〜§2 と §2.3・§4.2 の canary は C-4 を除き無傷。

- 起草: 影工房 数学者(Opus 5)/ 2026-08-23 / 委嘱: 司令塔(役割変更後 = **検収用独立導出**・実装仕様ではない)
- 入力: `search/certs/d972_b4_word_key_artifact_v1_20260816.json`(座標規約の読み取りのみ)・正典 2405 Thm 4.3/4.6・定義ノート §2/§3・工房確定事実(P1 corpus 索引 §0・CLAIMS)
- **不使用**: Sol 便の §13 receipt・escape28 の 324 lift-target rows・「972/3」という型の言い換え(Sol の明言どおり代用不可)

---

## §0 三行

1. **canonical key の解剖は完全に決まった**: $\kappa=(m;\delta;\pi)$、$X=\bigsqcup_{m\in\mathcal X_{18}}\{m\}\times(\mathbb Z/9)_k\times\Pi_m$、**$|X|=12\cdot9\cdot9=972$ で各 $m$ 上は完全な直積**(artifact 直読)。
2. **二面体成分は Thm 4.3 の逐語**であることを **12/12 で機械確認**($\delta=(r^{2k},r^{-2k},r^{\varkappa(m)})$・$\varkappa(m)=m{+}1$(奇)/$-m$(偶) mod 9)。$k\in\mathbb Z/9$ が唯一の自由度。
3. **$|A_{\rm cand}|=12\cdot9\cdot9/r=324$($r=3$)は「$m$ ごとに 81 → 27」の $\mathbb Z/3$-linkage**。$X$ 自身は $m$ ごとに linkage を**持たない**(直積)ので、**$r=3$ は純粋に算術由来**であり、artifact からは読めない — これが供給されるべき datum の正体。

---

## §1 canonical-key 座標系(artifact 直読・機械確認)

row $=[m,\ \kappa,\ w]$、$\kappa=(m;\ \delta;\ \pi)$:

| 座標 | 型 | 値域 | 確認 |
|---|---|---|---|
| $m$ | $\mathbb Z/18$ | $\mathcal X_{18}=\{0,2,3,5,6,8,9,11,12,14,15,17\}$(12 値・各 81 行) | $\gcd(2m{+}1,18)=1\iff m\not\equiv1\ (3)$(charming 単元条件)⟹ ちょうどこの 12 値。**P-972-2 と同一**。 |
| $\delta$ | $D_9^3$、各成分 $(a,\epsilon)\leftrightarrow r^as^\epsilon$ | 全 972 行で $\epsilon_i=0$、$\delta=(r^{2k},r^{-2k},r^{\varkappa(m)})$ | **Thm 4.3 逐語**。第 3 成分 $=r^{\varkappa(m)}$ を **12/12 一致**で確認(下表)。第 1 成分は $m$ ごとに $\mathbb Z/9$ を悉皆(2 は mod 9 で可逆ゆえ $k\leftrightarrow2k$ 全単射) |
| $\pi$ | $\mathrm{Sym}(9)$($PSL(2,8)$ の次数 9 作用) | 全体で 27 値・**各 $m$ でちょうど 9 値** | 下記 §1.2 |

**$\varkappa(m)$ 照合(12/12)**

| $m$ | 0 | 2 | 3 | 5 | 6 | 8 | 9 | 11 | 12 | 14 | 15 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 予測 $\varkappa$ | 0 | 7 | 4 | 6 | 3 | 1 | 1 | 3 | 6 | 4 | 7 | 0 |
| artifact 実測 | 0 | 7 | 4 | 6 | 3 | 1 | 1 | 3 | 6 | 4 | 7 | 0 |

### 1.1 $m$ ごとの構造(決定的)

各 $m$ について $\#\delta=9$、$\#\pi=9$、行数 $=81=9\times9$ ⟹ **完全直積**(各 $\delta$ に 9 個の $\pi$、各 $\pi$ に 9 個の $\delta$)。
$$\boxed{\ X\ =\ \bigsqcup_{m\in\mathcal X_{18}}\ \{m\}\times(\mathbb Z/9)_k\times\Pi_m,\qquad |X|=12\cdot 9\cdot 9=972.\ }$$

### 1.2 $\Pi_m$ は 3 クラスに分かれ、**$u$ で決まる**(新規・機械確認)

27 個の $\pi$ 値は 9 個ずつ 3 組に分かれ、$m$ がどの組を使うかは
$$\bar u:=\ (2m+1)\ \bmod\ \{\pm1\}\ \in\ (\mathbb Z/9)^\times/\{\pm1\}\cong C_3$$
で**完全に決まる**:

| $\bar u$ の類 | $u\bmod 9$ | $m$ | $\Pi_m$ |
|---|---|---|---|
| $\{\pm1\}$ | 1, 8 | 0, 8, 9, 17 | 組 I |
| $\{\pm2\}$ | 2, 7 | 3, 5, 12, 14 | 組 III |
| $\{\pm4\}$ | 4, 5 | 2, 6, 11, 15 | 組 II |

⟹ **$X$ 内にすでに $C_3$ の linkage が 1 本ある**(円分 ↔ PSL のコセット)。**Goursat 会計**: $|X_1|=|GT(K^{(9)})|=108$(Thm 4.6: $2n_0\varphi(n_0)=2\cdot9\cdot6$)、$|X_2|=|GT(N_{S4})|=54$、$108\cdot54/|X|=6$ ⟹ **共通商 $C\cong C_2\times C_3$**($C_2$ = $m\bmod2$ の整合、$C_3$ = 上の $\bar u\leftrightarrow$ PSL コセット)。**会計が閉じた。**
アンカー: $m=0$ が単位($u=1$)、**$m=8$ が複素共役**($u=17\equiv-1 \bmod 18$)— どちらも組 I。

---

## §2 $A_{\rm cand}$ の構成的定義(324 keys)

### 2.1 数え上げの骨格

工房の TRIAD-972 式 $|X\setminus A|=972-12\,d_9\,d_{S4}/r$ の各因子は、§1 の解剖で**意味が確定する**:
$$d_9=9\ (\text{二面体 fibre }k\in\mathbb Z/9),\qquad d_{S4}=9\ (\text{PSL fibre }\Pi_m),\qquad r=3\ (\text{算術 linkage の指数}).$$
$$\boxed{\ |A_{\rm cand}|=12\cdot\frac{9\cdot9}{3}=12\cdot27=\mathbf{324},\qquad |X\setminus A_{\rm cand}|=648.\ }$$

### 2.2 324 keys の切り出し(形は導出済み・写像の同定は §3)

**成分ごとの算術像(工房確定事実)**
- **二面体側**: $\mathrm{Ih}_{K^{(9)}}$ は **全射**(dihedral 予想 = 当工房で完全証明・発効。P1 corpus 索引 §0・格 = theorem-framework-relative)⟹ $A$ の二面体射影 $=X_1$ 全体(108)、すなわち **$k$ は各 $m$ で $\mathbb Z/9$ を悉皆**。
- **PSL 側**: S4 窓算術飽和(裁定 970・前件 P1–P5 相対)⟹ $A$ の PSL 射影 $=X_2$ 全体(54)、すなわち **$\pi$ は各 $m$ で $\Pi_m$ を悉皆**。
- ⟹ $A$ は両射影で全射な $X$ の部分群 ⟹ **Goursat により $A$ は共通商 $C'$ 上の fibre product**、$|A|=108\cdot54/|C'|$。$|A|=324\iff |C'|=18$。
- $|C|=6$(§1.2)だから **$C'\twoheadrightarrow C$ の核が $C_3$** — これが $r=3$。

**したがって $A_{\rm cand}$ の形は一意に決まる**:
$$\boxed{\ A_{\rm cand}\cap\{m\}\ =\ \bigl\{(k,\pi)\in(\mathbb Z/9)\times\Pi_m\ :\ \phi_m(\pi)=\lambda_m(k\bmod 3)\bigr\},\quad \#=9\cdot 3=27\ }$$
ここで $\phi_m:\Pi_m\twoheadrightarrow C_3$ は $\Pi_m$(9 元)上の $C_3$-値不変量(fibre 3)、$\lambda_m:\mathbb Z/3\xrightarrow{\ \sim\ }C_3$。
**未確定なのは $(\phi_m,\lambda_m)$ の同定だけ** — それが要求されている算術 datum である。

### 2.3 有限受領手続き(subgroup receipt・全て有限検査)

1. **群法の key 座標表示**(定義から):(3.53) $[m_1,f_1]\circ[m_2,f_2]=[2m_1m_2{+}m_1{+}m_2,\ f_1E_{m_1,f_1}(f_2)]$、$u=2m{+}1$ は乗法的。
   - $m$ 軸: $u=u_1u_2 \bmod 18$。
   - **二面体軸(閉形式・Thm 4.6 の $\mathrm{Aff}(\mathbb Z/9)$ 構造から)**: $\boxed{k=k_1+u_1k_2 \bmod 9}$。
     ⟹ $k$ は $\chi$-捻れ 1-コサイクル: $k_{\sigma\tau}=k_\sigma+\chi(\sigma)k_\tau$(§3.1 で使う)。
   - PSL 軸: $\pi=\pi_1\cdot E_{m_1,f_1}(\pi_2)$ — 語 $w$ から再 key 化(artifact の第 3 欄が各 key の語を持つので実装可能)。
2. **閉包検査**: $324^2$ 対(または生成系 3〜4 個で十分)で $\circ$ が $A_{\rm cand}$ に閉じることを確認。
3. **位数**: $|A_{\rm cand}|=324$、$[X:A_{\rm cand}]=3$。
4. **包含**: 324 keys がすべて artifact の 972 行に現れること(canonical key の完全一致・行番号を witness に)。
5. **$\chi_{vir}$ 全射**: $A_{\rm cand}$ の $m$ 射影が $\mathcal X_{18}$ 全体(12 値)であること。**これは必須の絞り込み**(下記 §4.1)。

---

## §3 marked finite Galois quotient と $a_M=\mathrm{PR}_M\circ\mathrm{Ih}$

### 3.1 二面体軸は **Kummer 類**である(導出・仮定なし)

§2.3 の合成則 $k=k_1+u_1k_2$ より、$\sigma\mapsto k_\sigma$ は $\chi$ で捻れた 1-コサイクル、すなわち
$$[k]\ \in\ H^1\bigl(G_\mathbb{Q},\ \mathbb Z/9(1)\bigr)\ =\ H^1(G_\mathbb{Q},\mu_9)\ \cong\ \mathbb Q^\times/(\mathbb Q^\times)^9 .$$
$\mathrm{Ih}_{K^{(9)}}$ が全射(P1)⟹ $k$ は $\mathbb Z/9$ へ全射 ⟹ **$[k]$ は位数 9 の Kummer 類**。ゆえに
$$\boxed{\ \text{二面体層の marked 体}\ =\ \mathbb Q\bigl(\zeta_9,\ \sqrt[9]{\beta}\bigr),\quad \beta\in\mathbb Q^\times/(\mathbb Q^\times)^9\ \text{の位数 9 の類}.\ }$$
被覆が $\{0,1,\infty\}$ の外で不分岐 ⟹ $\mathbb Q(\zeta_9,\sqrt[9]\beta)/\mathbb Q(\zeta_9)$ は $\{2,3\}$ の外で不分岐 ⟹ **$\beta\in\langle-1,2,3\rangle$ mod 9 乗**。
**生成元 → key の規則**:
$$k_\sigma\ :=\ \text{Kummer 指数},\qquad \sigma\bigl(\sqrt[9]{\beta}\bigr)=\zeta_9^{\,e_\sigma}\sqrt[9]{\beta}\ \Longrightarrow\ k_\sigma\equiv \tfrac12\,c\cdot e_\sigma\ (\mathrm{mod}\ 9)$$
($\delta$ の第 1 成分が $r^{2k}$ ゆえ $2$ で割る・$c\in(\mathbb Z/9)^\times$ は正規化定数 1 個)。
**$\beta$ の候補【candidate】: $\beta=2$。** 根拠(証明ではない): (a) 83 線で私が独立に導出した $C_3$-被覆の分体が $\mathbb Q(\zeta_3,\sqrt[3]2)$ で、これは同じ族の $n=3$ 例にあたる(memo §3.3.1・定理 C3-LIFT);(b) $\{2,3\}$ の外不分岐+位数 9 の制約下で $-1$(位数 2)・$3$(暴分岐)は落ちやすい。**検定**: 素数 $p\equiv1\ (9)$ で $\mathrm{Frob}_p$ の $k$ 値が $2^{(p-1)/9}\bmod p$ の離散対数と一致するか(数十行・独立に走る)。

### 3.2 PSL 軸と linkage の $C_3$

工房確定: 幾何モノドロミー $=504=|PSL(2,8)|$、**$G_{\rm arith}=P\Gamma L(2,8)$**(裁定 1145 で C1′/P5′ 発効)。
$$P\Gamma L(2,8)/PSL(2,8)\ \cong\ \mathrm{Gal}(\mathbb F_8/\mathbb F_2)\ \cong\ C_3 .$$
⟹ PSL 層の marked 体 $L_{\rm PSL}$ は $PSL(2,8)$-層の上に **$C_3$(Frobenius)層**を持つ。この $C_3$ こそ $\phi_m$ の候補である。
**linkage の予想【candidate・要 pin】**:
$$\boxed{\ \mathbb Q(\zeta_9,\sqrt[9]\beta)\ \text{の中の 3 次部分体}\ \mathbb Q(\zeta_3,\sqrt[3]\beta)\ \ \textbf{と}\ \ L_{\rm PSL}\ \text{の}\ P\Gamma L/PSL\ \text{層が一致する}\ }$$
これが成り立てば、$k \bmod 3$ と $\phi_m(\pi)$ が同一の $C_3$ を測るので $|A|=12\cdot9\cdot9/3=324$ が**そのまま出る**。
(注: §1.2 の $C_3$-linkage は $\bar u$ ↔ $\Pi_m$ のコセットで、こちらは $\Pi_m$ の**内部**の $C_3$。二本は別物 — 混同禁止。)

### 3.3 $a_M$ の生成元レベル型付き写像(まとめ)

$L_M:=\overline{\mathbb Q}^{\ker \mathrm{Ih}_M}$、$\mathrm{Gal}(L_M/\mathbb Q)\cong A$($=324$ なら)。3 層と生成元:

| 層 | 体 | 生成元 | $a_M$ 像(canonical key) |
|---|---|---|---|
| 円分 | $\mathbb Q(\zeta_{18})$ | $\sigma_c:\zeta_{18}\mapsto\zeta_{18}^{t}$、$t\in(\mathbb Z/18)^\times$ | $m=(t-1)/2 \bmod 18$;$\delta=(1,1,r^{\varkappa(m)})$($k=0$ に正規化);$\pi=$ 対応する $\Pi_m$ の基点 |
| Kummer(二面体) | $\mathbb Q(\zeta_9,\sqrt[9]\beta)$ | $\sigma_\kappa:\sqrt[9]\beta\mapsto\zeta_9\sqrt[9]\beta$、$\zeta_{18}$ 固定 | $m=0$;$\delta=(r^{2k},r^{-2k},r^{0})$、$k=\frac12 c$;$\pi=$ linkage で $\phi(\pi)=\lambda(k)$ を満たす元 |
| PSL | $L_{\rm PSL}$($PSL(2,8)$ 層) | $\sigma_p$($P\Gamma L/PSL$ 層で自明・$PSL$ 層で非自明) | $m=0$;$k=0$;$\pi=$ 非自明 |

**型**: $a_M(\sigma)=(m_\sigma;\ \delta_\sigma;\ \pi_\sigma)$、$m_\sigma=(\chi(\sigma)-1)/2 \bmod 18$、$k_\sigma$ = §3.1 の Kummer 指数、$\pi_\sigma$ = $L_{\rm PSL}$ での像。合成は §2.3 の閉形式($u$ は乗法的・$k=k_1+u_1k_2$)。

### 3.4 両方向 row witness の形式

- **$\mathrm{image}(a_M)\subseteq A_{\rm cand}$**: 生成元 3 本($\sigma_c,\sigma_\kappa,\sigma_p$)それぞれの key が $A_{\rm cand}$ の行にあることを row 番号で示す + §2.3 の閉包により生成部分群全体が入る。**生成元ごとの 3 行で足りる**(閉包が定理として効くため)。
- **$A_{\rm cand}\subseteq\mathrm{image}(a_M)$**: 324 keys 各々に **原像語**($\sigma_c^{i}\sigma_\kappa^{j}\sigma_p^{l}$ の指数三つ組)を付す。$|A_{\rm cand}|=324$ と生成部分群の位数が一致すれば全射は自動なので、**324 行に指数三つ組を並べた表**が witness。位数が一致しないなら生成元が足りない(その場合は第 4 生成元を要求)。

---

## §4 検収側の決定手続きと canary

### 4.1 ★ 独立受領の急所 — **指数 3 部分群の悉皆**

$A$ は $X$(972)の**指数 3 部分群**で、しかも **$\chi_{vir}$ 像が全射**(2405 (1.13) より必然)。指数 3 部分群 $\leftrightarrow$ 全射 $X\to C_3$ の核 $\leftrightarrow$ $\mathrm{Hom}(X,C_3)\setminus\{0\}$ をスカラーで割ったもの、個数 $=(3^{d}-1)/2$、$d=\dim_{\mathbb F_3}X^{ab}\otimes\mathbb F_3$。
⟹ **$d$ を測れば候補は有限個に確定し、そのうち $\chi_{vir}$ 全射でないもの(必ず 1 本ある: $\ker(X\xrightarrow{\chi_{vir}}C_6\to C_3)$)を落とせる。**
$d=2$ なら候補 4 本 → 1 本除外で **3 本**;$d=1$ なら候補 1 本(= 除外されるもの)しかなく **$|A|=324$ 自体が矛盾**(強力な健全性検査)。
**これが Sol 納品を第三系統で裁く最短路**。実行は artifact の語で群法を回すだけ(GT(M) の 972 元・生成系は 3〜4 元で足りるはず)。

### 4.2 canary(破壊対照)

| # | 対照 | 期待 |
|---|---|---|
| **C-1** | $A_{\rm cand}$ に $X\setminus A_{\rm cand}$ の 1 key を足す(325 元) | 閉包が破れる(積が 325 集合の外へ出る対を明示)。**指数 3 が素数**ゆえ中間部分群がないので**必ず $X$ 全体を生成**する — 「325 元で閉じた」が返ったら実装バグ |
| **C-2** | $\chi_{vir}$ 対照 | $A_{\rm cand}$ の $m$ 射影が 12 値でなければ即 FAIL(§4.1) |
| **C-3** | Thm 4.3 対照 | $A_{\rm cand}$ の全 key で $\delta_3=r^{\varkappa(m)}$(12/12 の表)。破ったら座標系の取り違え |
| **C-4** | 陽性対照 | 単位 $(m{=}0,k{=}0,\pi{=}\mathrm{id})$ と **複素共役** $(m{=}8,\ u{=}-1)$ の 2 key が必ず $A_{\rm cand}$ に入る(後者は 2405 Rem 1.10 で無条件に算術的) |
| **C-5** | linkage 対照 | $A_{\rm cand}\cap\{m\}$ が各 $m$ でちょうど 27 元・$k$ 射影が $\mathbb Z/9$ 全射・$\pi$ 射影が $\Pi_m$ 全射(片側だけ潰れていたら Goursat 型が違う) |

### 4.3 前提として pin が要るもの(足りない分の明示)

1. **$\beta$(Kummer 底)の確定** — §3.1。候補 2、検定は Frobenius 一致で数十行。
2. **$\phi_m$(= $\Pi_m$ 上の $C_3$ 不変量)の明示** — §3.2 の $P\Gamma L/PSL$ 層との同定。
3. **S4 窓算術飽和の格** — 裁定 970 は前件 P1–P5 相対。$A$ の PSL 射影が全射でないなら $|A|<324$ になるので、**324 という数字自体がこの前件に依存**する。
4. **$X$ が本当に群か**(GT(M) の isolated 性)— 閉包検査の前提。

---

## §5 独立性の申告

Sol の §13 receipt・IDX3 納品物は**一切読んでいない**。数値はすべて (a) 正典 2405 Thm 4.3/4.6、(b) 定義ノート §2 の charming/合成則、(c) 工房確定事実(P1 発効・裁定 970・裁定 1145 の $G_{\rm arith}=P\Gamma L(2,8)$・TRIAD-972 式)、(d) `d972_b4_word_key_artifact_v1_20260816.json` の**座標直読**、から導出した。**§1.2 の「$\Pi_m$ は $\bar u\in(\mathbb Z/9)^\times/\{\pm1\}$ で決まる」と §1 の $\varkappa$ 12/12 照合は本ノートの新規観測**(既存文書での既出は未確認 — novelty は主張しない)。

---

# §6 versioned 訂正(2026-08-23)— Sol 便 159 §17 敵対監査の反映

出典: `sol/sol_reply_159_iv.md` §17.2/17.3(ブラインド段階終了・読了済)。
**規律**: v1 本文は 1 バイトも削除せず、本節が逐語の正本。撤回は明示。**現行正本 = 「v1 本文 + §6」**。

## 6.0 撤回 2 件(明示)

| # | 撤回する記述 | 所在 | 理由 |
|---|---|---|---|
| **R-1** | 「指数 3 部分群 $\leftrightarrow$ $\mathrm{Hom}(X,C_3)\setminus\{0\}$、個数 $(3^d-1)/2$。**$d=1$ なら $\lvert A\rvert=324$ 自体が矛盾**」 | §4.1 | **正規部分群限定の数え上げだった。** 指数 3 部分群は一般に非正規で、$X\to S_3$ の推移的像の点安定化群として現れる。Sol の census(cross-checked)= 非正規指数 3 部分群 **12 個**・$X\to S_3$ 全射 24 本。成分全射+複素共役所属フィルタ後の**最終候補 2 個 = IDX3-NN-09/12(いずれも非正規)**。⟹ **矛盾主張は不成立・全面撤回**。 |
| **R-2** | 「$m=(t-1)/2 \bmod 18$($t\in(\mathbb Z/18)^\times$)」/ canary C-4 の「複素共役 $=m{=}8$」 | §3.3 表・§4.2 C-4 | **法の取り違え(P93-1 二値性・周期 9)。** §6.2 で訂正。 |

**維持されるもの**(監査で不変): §1 の解剖と $\varkappa$ 12/12 照合・§1.2 の $\bar u\leftrightarrow\Pi_m$ 対応と Goursat 会計 $|C|=6$・§2.1 の $|A|=12\cdot9\cdot9/3=324$・§2.3 の閉形式群法($u$ 乗法的・$k=k_1+u_1k_2$)・§4.2 の canary C-1/C-2/C-3/C-5。
**C-1 の論拠も無傷**: $A\le H\le X$ なら $[X:H]\in\{1,3\}$ ゆえ**指数 3 部分群は正規性と無関係に極大** ⟹ 1 key 足せば必ず $X$ 全体を生成する。

## 6.1 ★定理 TYPE-ODD(点 1 と点 3 は同一現象であることの証明)

> ### 定理 TYPE-ODD
> $\mathcal K_3:=(k\bmod 3):G_\mathbb{Q}\to\mathbb Z/3$ を二面体 Kummer 座標の mod 3 還元とする。
> **(a)** §2.3 の合成則 $k=k_1+u_1k_2$($u=\chi$)より
> $$\mathcal K_3(\sigma\tau)=\mathcal K_3(\sigma)+\chi(\sigma)\,\mathcal K_3(\tau),$$
> すなわち $\mathcal K_3$ は **$\mu_3$ 係数**の 1-コサイクル、$[\mathcal K_3]\in H^1(G_\mathbb{Q},\mu_3)=\mathbb Q^\times/(\mathbb Q^\times)^3$。とくに複素共役 $c$ について
> $$\mathcal K_3(c\sigma c^{-1})=-\mathcal K_3(\sigma)\qquad(\textbf{奇}).$$
> **(b)** $\Phi:G_\mathbb{Q}\to\mathbb Z/3$ を $P\Gamma L(2,8)/PSL(2,8)\cong\mathrm{Gal}(\mathbb F_8/\mathbb F_2)$ の座標とする。これは**自明係数の準同型**($\mathbb Q$ 上の巡回 3 次拡大)ゆえ
> $$\Phi(c\sigma c^{-1})=\Phi(\sigma)\qquad(\textbf{偶}).$$
> **(c)** ゆえに $\Phi=c'\,\mathcal K_3$($c'\in(\mathbb Z/3)^\times$)は $\mathcal K_3=-\mathcal K_3$、すなわち $2\mathcal K_3=0$、すなわち $\mathcal K_3=0$ を強制する。これは $\mathrm{Ih}_{K^{(9)}}$ の全射性(P1・発効済)に矛盾。
> $$\boxed{\ \textbf{「二面体側の 3 次部分体 = }P\Gamma L/PSL\textbf{ 層」の同定は文字どおり不可能。}\ }\qquad\blacksquare$$

> ### 系 TYPE-ODD-2(非正規性の予言 = 点 1 との合流)
> linkage の $C_3$ は奇($c$ が $-1$ で作用)⟹ Goursat の共通商 $C'$(位数 18、$\ker(C'\to C)\cong C_3$、$C\cong C_2\times C_3$)は、$C$ の $C_2$ 成分(複素共役)が新しい $C_3$ を反転するので **非可換**。⟹ $A=X_1\times_{C'}X_2$ は **$X$ の中で非正規**。
> ⟹ **Sol の census が非正規候補 IDX3-NN-09/12 のみを残したことは、TYPE-ODD の帰結として構造的に必然**である(偶然の一致ではない)。**点 1(非正規)と点 3(型不整合)は同一現象の二つの顔。**

## 6.2 訂正 R-2 の逐語(法 = $2N_{\rm ord}=36$)

$m\mapsto u=2m+1$ は $\mathbb Z/18$ 上**単射でない**($\gcd(2,18)=2$):
$$u\equiv u'\ (\mathrm{mod}\ 18)\iff m\equiv m'\ (\mathrm{mod}\ 9).$$
ゆえに $u\equiv-1$ からは $m\in\{8,17\}$ までしか決まらない(**P93-1 二値性・周期 9**)。正しい規則:
$$\boxed{\ \tilde t:=\chi\ \bmod\ 36\ (=2N_{\rm ord}),\qquad m=\frac{\tilde t-1}{2}\ \bmod\ 18\ }$$
複素共役は $\hat{\mathbb Z}$ で $\chi=-1$ ⟹ $\tilde t=35$ ⟹ $m=17$、$f=1$(空語)。2405 Rem 1.10 の $\mathrm{Ih}(c)=(-1_{\hat{\mathbb Z}},1_{\hat F_2})$ と逐語一致し、artifact の **row 891**(empty word)と合う。empty-word 行は $m=0$ と $m=17$ の **2 行のみ**。

> **canary C-4(訂正版)**: 陽性対照 = $(m{=}0,\ \delta{=}(1,1,r^{0}),\ \pi{=}\mathrm{id})$ と $(m{=}17,\ f{=}1)$ の **2 key**。両方が $A_{\rm cand}$ に入らなければ即 FAIL。
> **§1.2 のクラス分けは無傷**($m{=}17$ は元から組 I。各クラスは $\{m,m+9\}$ の 2 組の和)。
> **標準警告(以後の全文書へ)**: D972 の $m$ 軸は周期 9 の $\chi_{vir}$ 盲がある。「どの $m$ か」を言う主張は必ず **mod 36** で計算すること。

## 6.3 正しい同定(再型付け)

$L_0:=\mathbb Q(\zeta_3)$。$\mu_3\cong\mathbb Z/3$ は $G_{L_0}$-加群としてのみ同型($\zeta_3$ の選択に依存)。

$$\boxed{\ \mathrm{res}_{L_0}\Psi\ =\ c'\cdot\mathrm{res}_{L_0}\mathcal K_3\quad\text{in }\ \mathrm{Hom}(G_{L_0},\mathbb Z/3),\qquad \Psi\ \textbf{は奇}\ \bigl(\Psi(c\,\sigma\,c^{-1})=-\Psi(\sigma)\bigr)\ }$$

- $\Psi$ は **$P\Gamma L/PSL$ の Frobenius 座標ではない**。S4 窓自身の**奇($\mu_3$ 型)$C_3$ 座標** = Kummer 方向。
- **体の言葉**: $\mathbb Q(\zeta_3,\sqrt[3]\beta)$($\mathrm{Gal}\cong S_3$)が $L_9$ と $L_{\rm PSL}$ の**共通部分体**。3 次部分体は**非ガロアの $\mathbb Q(\sqrt[3]\beta)$** であって巡回 3 次ではない。
- **base-change 図式**: 行は $\mathbb Q$ 上の $S_3$-共役類(単位/位数 3/転置)を記録し、$L_0$ へ制限して初めて $\mathbb Z/3$ 値になる。$p\equiv1\ (3)$ の行のみ $\mathbb Z/3$ 値が意味を持ち、$p\equiv2\ (3)$ の行は**転置類**(複素共役側)。$\zeta_3$ の埋め込みを取り替えると $\mathcal K_3\mapsto-\mathcal K_3$ ⟹ **marking で埋め込みを固定しないと符号が決まらない**。
- ⟹ §3.2 の旧 linkage 予想(「$\mathbb Q(\zeta_3,\sqrt[3]\beta)$ の 3 次部分体 = $P\Gamma L/PSL$ 層」)は **本節の形へ差し替え**。

## 6.4 ★在庫からの $\Psi$ の同定 — $[u_0^{-1}]_3=[2]$

`search/certs/ds4_receipt_v1_20260812.json` を独立に読み、本ノートで因数分解をやり直した:
$$u_0^{-1}=-\frac{1423828125}{256}=-\,3^{6}\cdot 5^{9}\cdot 2^{-8}\qquad(v_3,v_5,v_2)=(6,9,-8)$$
(cert の `fresh_factorization_of_abs_value` と一致・$729\cdot1953125=1423828125$、$256=2^8$)。linkage は **mod 3** なので $\mathbb Q^\times/(\mathbb Q^\times)^3$ で読む($-1=(-1)^3$ は自明):
$$[u_0^{-1}]_3=\bigl[\,3^{6\bmod3}\cdot5^{9\bmod3}\cdot2^{-8\bmod3}\,\bigr]=\bigl[\,3^{0}\cdot5^{0}\cdot2^{1}\,\bigr]=[2]$$
$$\boxed{\ \text{S4 窓の Kummer 立方体}\ =\ \mathbb Q(\sqrt[3]{2})\quad(\text{非ガロア}\ \Rightarrow\ \textbf{奇}\ )\ }$$
⟹ **TYPE-ODD が要求する「奇の $C_3$」が S4 側に実在し、それは $\mathbb Q(\sqrt[3]2)$。二面体側の予測 $\beta=2$(§3.1)と mod 3 で一致。** 再型付けが在庫データで裏付けられた。
(83 線の定理 C3-LIFT が $\mathbb Q(\zeta_3,\sqrt[3]2)$ を出したこととも整合 — ただし別機構ゆえ根拠には数えない。)

## 6.5 mod 9 のずれの正体

mod 9 では $[u_0^{-1}]_9=[\,3^{6}\cdot2^{1}\,]$(指数を mod 9: $6,\ 0,\ -8\equiv1$)、位数 $=\mathrm{lcm}(9/\gcd(9,6),\,9/\gcd(9,1))=\mathrm{lcm}(3,9)=9$ ✓(cert の `ord_value=9` と一致)。一方 $[2]^7=[2^7]$。両者の比は $3^6/2^6=(3/2)^6$ で、これが 9 乗になるには $6\equiv0\ (9)$ が要る — **偽**。
$$\boxed{\ [u_0^{-1}]_9\ \ne\ [2]^7\ \ \text{だが}\ \ [u_0^{-1}]_3=[2^7]_3=[2].\ }$$
⟹ **Sol の「$[2]^7$ は β=2 支持だが canonical row marking ではない」は正確**。ずれの正体は **(i) §3.1 の正規化定数 $c\in(\mathbb Z/9)^\times$** と **(ii) $3$-成分($3^6$、mod 3 では消えるが mod 9 では残る)** の 2 つ。
**帰結(実務)**: **linkage($r=3$)は mod 3 で閉じるので joint marked row は今すぐ書ける。** mod 9 の canonical marking(= $c$ の確定)は別作業で、$\beta=2$ vs $\beta=3$ の 12 素数判別とは独立に進めてよい。

## 6.6 残 pin(3 件)と Frobenius row の実務

| # | pin | 状態 | 影響 |
|---|---|---|---|
| **P-a** | $\zeta_9,\zeta_3$ の埋め込み固定 + 正規化定数 $c\in(\mathbb Z/9)^\times$ | 未固定 | 未固定だと $\mathcal K_3$ の**符号**が決まらない(埋め込み取替で $\pm$ 反転)。row marking の前提 |
| **P-b** | **ds4 receipt の前件 P5(`u_0 = u_{S4}` 同一性)= `unconfirmed`**(cert 自己申告) | **未確認** | 未確認なら §6.4 の「$[u_0]$ を S4 窓の Kummer 類と読む」段が落ちる。**急所は Belyi 写像ではなく P5** |
| **P-c** | $X_2=GT(N_{S4})$ が $S_3$ 商をもつこと($X_2^{ab}$ の測定・1 行) | 未測定 | 6.1 系の Goursat 型($C'$ 非可換)の窓側の裏取り |

**Frobenius row の計算可能性(見立て)**
- **二面体側 = 容易**。$p\equiv1\ (\mathrm{mod}\ 9)$ を取り、$\zeta_9$ の埋め込みと $\mathbb F_p^\times$ の位数 9 部分群の生成元を固定して
 $$k_p\equiv\tfrac12\,c\cdot\log_{\zeta_9}\!\bigl(\beta^{(p-1)/9}\bmod p\bigr)\ (\mathrm{mod}\ 9).$$
 $\beta{=}2$ と $\beta{=}3$ は「$2/3$ が mod $p$ の 9 乗」となる素数(密度 $\sim1/9$)以外で分離 ⟹ **12 素数で実質確定**。
- **PSL 側 = Belyi 写像は不要**。在庫の passport $(3^3,3^3,(9))$・9T27・rigid・ℚ 上定義(litgate)は**存在の保証**であって row には要らない。必要なのは **奇の $C_3$ 座標 = $[u_0]$ の mod 3 類**(§6.4 で確定済)。⟹ **row の算術部分は P-a と P-b が閉じれば即書ける。**
- 未観測: joint marked row は現在 **0 行(NOT_RUN)**。$[2]^7$ の scalar 測定は subgroup を決めるが marking ではない(§6.5)。

---

# §7 向き 1 ビットの理論と局所プロトコル(2026-08-23・裁定 1631)

出典: Sol 便 159 §19(P5 閉鎖 campaign)読了。**literal P5 は座標不変な命題でないと確定**($s_{\rm int}\mapsto a\,s_{\rm int}$ で $u_0\mapsto a^{-9}u_0$)。$X_2^{ab}\cong C_6$・$X_2\twoheadrightarrow S_3$ は閉(§6.6 P-c 解消)。
**本節の位置づけ**: §6.3 の linkage の**符号 $c'$** に関する理論(§7.1/7.2)と、その 1 ビットを取る**局所手順書**(§7.3)。

## 7.1 ★定理 ORIENT

記号: $X^0:=\ker(\chi\bmod 3)\le X$($[X:X^0]=2$、$|X^0|=486$)。**$X^0$ 上でのみ $\mathcal K_3,\Psi$ は準同型**で
$$A_{c'}\cap X^0=\ker\bigl(\Psi-c'\mathcal K_3\bigr)\big|_{X^0},\qquad c'\in(\mathbb Z/3)^\times=\{\pm1\},\qquad \bigl|A_{c'}\cap X^0\bigr|=162 .$$

> ### 定理 ORIENT
> **(a) 埋め込み flip は無害。** $\zeta_9$(従って $\zeta_3$)の取り替え $\zeta\mapsto\zeta^a$ は、$\mathcal K_3$ と $\Psi$ を**同じ $\mu_3$-捻れで同時に**スケールする(両者とも奇 = TYPE-ODD)。ゆえに比 $c'$ は不変。
> **(b) 共役も無害・$A_\pm$ は非共役。** $x\in X$、$g\in X^0$ に対し、コサイクル関係と $\mathcal K_3(x^{-1})=-\chi(x)^{-1}\mathcal K_3(x)$ から
> $$\mathcal K_3(x^{-1}gx)=\mathcal K_3(x^{-1})+\chi(x)^{-1}\bigl[\mathcal K_3(g)+\chi(g)\mathcal K_3(x)\bigr]=\chi(x)^{-1}\mathcal K_3(g)\quad(\chi(g)\equiv1),$$
> $\Psi$ も同型ゆえ**同じ係数**でスケール ⟹ $c'$ は共役不変。よって $A_+\cap X^0,\ A_-\cap X^0$ は**ともに $X$ で正規かつ相異なる** ⟹ **$A_+$ と $A_-$ は共役でない**(共役なら $X^0$ との交わりも一致する)。
> **(c) $\varepsilon$ は有害。** 測定側は $\Psi=\varepsilon\,\Psi_0$($\Psi_0$ は $u_0$ 由来)。$\varepsilon$ は**片側にしか効かない**ので $c'\mapsto\varepsilon c'$。$\varepsilon\equiv-1\ (3)$ で **$A_+\leftrightarrow A_-$ を交換**。
> **(d) 不変に取れる部分。** $\varepsilon$-不変なのは**消滅軌跡**のみ: $\Psi(\sigma)=0\iff\Psi_0(\sigma)=0$。⟹ 「同じ 3 次体(P5′)」の**検定**は $\varepsilon$ なしで可能だが、**非零値のどちらか**は $\varepsilon$ 依存。
> **(e) ただ乗り不可。** $A_+\cap A_-=\{\mathcal K_3=\Psi=0\}$ は位数 108、$|A_\pm|=324$ ゆえ**対称差は 432 key で、そのすべてが $\mathcal K_3\ne0$ 側**。⟹ **対称差に $\varepsilon$-不変に強制される key は 1 個も存在しない**(census からの無料 1 ビットは原理的に不可能)。∎

**帰結**: 判別は **$c'\in\{\pm1\}$ の 1 ビット**に完全縮約。literal P5(代表元等式)は**過剰**。
**canary(Sol へ発注済)**: NN-09 △ NN-12 の 432 key が全て $\mathcal K_3\ne0$ 側に乗ること。1 個でも外れたら本型付けが誤り。

## 7.2 ★定理 NO-CANON

> ### 定理 NO-CANON
> $C/\mathbb Q$、$P_0$ を $\mathbb Q$-有理な index-9 cusp($\mathrm{ord}_{P_0}t=9$)、$s$ を $\mathbb Q$-有理な局所助変数、$u(s):=(t/s^9)(P_0)$ とする。
> **(a)** $s\mapsto as$($a\in\mathbb Q^\times$)で $u\mapsto a^{-9}u$ ⟹ **$[u]\in\mathbb Q^\times/(\mathbb Q^\times)^9$ は $(C,t,P_0)$ の不変量**(= P5′)。
> **(b)** $\exists\,\mathbb Q$-有理 $s$ で $u(s)=1$ $\iff$ $[u]=1$。実測 $\mathrm{ord}[u_0]=9\ne1$ ⟹ **Kummer 標準形 $t=s^9$(unit なし)は $\mathbb Q$ 上到達不能**。
> **(c)** ゆえに「正規化で $u$ を消す」は**測ろうとしている不変量そのものの自明化**を要求する。**literal P5 は選択なしには閉じない。**∎

**精密化 2 点(反例に最も近いもの)**
1. **極小整モデル正規化は循環しない。** 種数 2 超楕円曲線の極小モデルは $\mathrm{GL}_2(\mathbb Z)$ と $e\in\mathbb Z^\times=\{\pm1\}$ を除き一意。labeled cusp/labeled fibre を固定すれば $s$ は $\pm1$ まで、$u_0$ は**符号まで確定**($a=-1$ で $u\mapsto-u$、$-1=(-1)^9$ ゆえ類は不変)。⟹ 「canonical 代表元が原理的に取れない」わけではない。
2. **それでも $\varepsilon$ は出ない。** $\varepsilon$ は model 側 $u_0$ と cocycle 側 $u_{S4}$ の**比較**量で、片側の正規化では供給されない。供給するのは **marked cover 同型 $\iota_C$ と $\gamma$ のみ**。局所版($\mathbb Q_p$ 標準化)も同じ壁: $p\not\equiv1\ (3),\ p\ne3$ では単元が全て 9 乗になり $v_p(u)\bmod 9$(= 既知の類)しか回収できない。
⟹ **欠品の正体は「正規化の欠如」ではなく「比較写像の欠如」。**

## 7.3 ★局所プロトコル LOCAL-3(実装仕様・1 素点で $c'$ を取る)

### 7.3.0 設計原理(これが要)

**mod 9 では NO-CANON の障害が効くが、mod 3 では効かない**: $u\mapsto a^{-9}u$ の $a^{-9}$ は**立方数**ゆえ 3 次冪剰余記号は**助変数の取り替えに不変**。
$$\Bigl(\tfrac{a^{-9}u}{p}\Bigr)_3=\Bigl(\tfrac{a}{p}\Bigr)_3^{-9}\Bigl(\tfrac{u}{p}\Bigr)_3=\Bigl(\tfrac{u}{p}\Bigr)_3 .$$
さらに**両辺を同じ $\mu_3(\mathbb F_p)$ の中で比較する**ので $\zeta_3$ の埋め込み選択も相殺(ORIENT (a) の具体化)。
⟹ **残る自由度はただ一つ: 「窓の奇 $C_3$ 座標が $[u]$ に対応するか $[u^{-1}]$ に対応するか」**(= $\gamma$ の向き)。これが $c'$ そのもの。
**⟹ 向きを消す唯一の正しいやり方は「両窓の $u$ を同一のレシピで計算し、比を取る」こと**(向き convention は分子・分母に同じく効いて相殺する)。

### 7.3.1 局所 $\iota_C/\gamma$ データの定義(何を計算すれば向きが固定されるか)

素点 $\mathfrak p\mid p$ を固定し、次の 4 つを**同一の規約**で計算する。

| 記号 | 定義 | 固定するもの |
|---|---|---|
| $P_0^{(9)}$ | S4 側 cover の **index-9 cusp**(passport $(3^3,3^3,(9))$ より $t=\infty$(または指定の分岐点)上で**一意** ⟹ **labeling の曖昧さなし**) | $\iota_C$ の cusp 成分 |
| $s$ | $P_0^{(9)}$ での任意の $\mathbb Q$-有理助変数(極小整モデル上) | 不要(mod 3 で無関係・7.3.0) |
| $u_{S4}:=(t/s^9)(P_0^{(9)})$ | 先頭係数。**向き規約 D**: 「$t/s^9$」であって「$s^9/t$」ではない | $\gamma$ の向き |
| $u_{\rm dih}$ | **二面体窓 $K^{(9)}$ の cover に対し、全く同じ規約 D で計算した先頭係数** | 向きの**アンカー** |

> **規約 D(必記)**: cusp の index を $n$、$t$ を **0 で分岐する側**に取り、$u:=\lim_{s\to0}t/s^{n}$。両窓で同じ $t$-正規化(どの分岐点を 0 に置くか)を使う。逆向き規約は $u\mapsto u^{-1}$ を生み、$c'$ の符号を反転する。
> **$\iota_C$ は自明**: cover は degree 9・monodromy $PSL(2,8)$(9T27・原始的)ゆえ **deck 群自明・$\mathrm{Aut}(C,t)=1$**、しかも passport 内で **rigid**(litgate 済)⟹ $\iota_C$ は一意。**曖昧さは $\gamma$(規約 D)だけ。**

### 7.3.2 計算チェーン(pari/gp or Python・在庫のみ)

```
INPUT: p (7.3.3 の条件), u0inv = -1423828125/256   # ds4_receipt_v1_20260812.json
       beta   (= 2 予測: §3.1),  D972 census (NN-09 / NN-12 の key 集合)
       規約 D の宣言(u か u^{-1} か)

S1  assert p % 9 == 1                      # mu_9 subset F_p^*
S2  assert p does not divide num/den of u0inv, beta, disc(model)
S3  cube(z) := Mod(z, p)^((p-1)/3)         # in mu_3(F_p)
S4  Su    := cube(u_S4)    where u_S4 = u0inv^{sgn}   # sgn = +1 or -1 per 規約 D
    # ⚠⚠ 配線罠(2026-08-28・裁定 1720): 規約 D の正解は u_S4 = u0 なので、
    #    この行の u0inv を基準にすると sgn = -1 でなければならない。
    #    ところが cert の見出しは /input_u0_inverse・/d1_input_tamper_check/u0_inverse_read で
    #    「u0inv」を第一級の量として提示するため、素直に実装すると sgn=+1 を取り
    #    ★ ビットが反転する。cert に anchor_source と sgn を明記すること(規約台帳 D-5/D-10)。
    Sanc  := cube(u_dih)   # u_dih = ±2^-7  ← β は使わない(規約台帳 D-2)
    Sbeta := cube(beta)
S5  assert Su != 1 and Sbeta != 1          # 両側非自明(素数選択条件)
S6  cprime := 1 if Su == Sbeta else 2      # Su = Sbeta^{c'} in mu_3 ;  2 == -1
S7  k3 := discrete log of Sanc in mu_3(F_p)      # ← アンカー由来(β ではない・規約台帳 D-2)
    # ⚠⚠ 訂正(2026-08-28・裁定 1732(a)): 旧行は
    #   "= discrete log of Sbeta in mu_3(F_p)  (P1 corpus の marking で符号確定)"
    # だったが、**P1 corpus は k_sigma marking を持たない**(本文 grep 済・2026-08-28)。
    #   ヒットする "Kummer" は全て B-5 の窓 torsor 類 [u_n]_{2n}(83/K9 線)であって
    #   二面体 GT-shadow の k_sigma ではない。⟹ 旧行の典拠は**存在しなかった**。
    # ★ さらに、正規化定数 c は **そもそも不要**になった:
    #   SELECT は「Kummer 指標経由で Frobenius row を作る」経路を使わず、
    #   ker(Psi - c' K3)|_{X^0} を既知 2 roster 上で直接評価する(K1-K5)。
    #   K3 は正典 2405 Thm 4.3 の k mod 3(内在・機械確認済)、Psi は規約 D + u_dih アンカー。
    #   正本 = scratchpad/joint_marked_frobenius_design_v1.md §6。
S8  psi := discrete log of Su
S9  SELECT := UNDEFINED   # ⚠⚠ 訂正(2026-08-28・裁定 1726/falsifier 要修正 4)
    # 旧: "SELECT := NN-09 if (psi == +k3) else NN-12  # census の符号規約に合わせる"
    # → **実在しない対象への参照**。falsifier 実測(producer L706-713・機械 12/12)により
    #   census ラベル NN-jj は**辞書式順位**であって符号意味論を一切持たない。
    #   ⟹ 「census の符号規約」は存在しない。SELECT=NN-09 は撤回済(cert v5)。
    # 正: S9 は **translation bit** を要する ── すなわち
    #     「c' の生値(= +1)」を「どちらの roster か」に翻訳する外部データが要る。
    #     その唯一の接地は **joint marked Frobenius row**(§7.3.7)で、
    #     具体的な D972 key 1 本を測って 2 つの 324-key roster への**所属を直接照合**する。
    #     ⟹ joint marked row が出るまで SELECT は fail-closed。**c' = +1 の生値は不変。**
S10 REPEAT S1-S9 for two more primes; SELECT must agree (安定性検査)
```
**費用**: 各素数ミリ秒。**必要な在庫は cert の $u_0^{-1}$ と $\beta$ だけ** — Belyi 写像も定義多項式も不要。
**幾何側の一度きりの作業**: 規約 D の宣言と、$u_{\rm dih}$ を同一規約で 1 回計算(向きアンカー・7.3.1)。これができれば $\gamma$ は完全に消える。

### 7.3.3 素数の条件と両分岐の予言表

**条件**: (i) $p\equiv1\pmod 9$、(ii) $p\nmid 2\cdot3\cdot5$($u_0$ の素因子)、(iii) $\left(\frac{\beta}{p}\right)_3\ne1$ かつ $\left(\frac{u_0}{p}\right)_3\ne1$(両側非自明 — これが**判別力の条件**)。
$p\equiv1\ (9)$ の最小列: $19,\ 37,\ 73,\ 109,\ 127,\ 163,\ 181,\ 199,\dots$

> ### ⚠⚠ 本予言表は **stale — 全面訂正**(2026-08-28・裁定 1717/1720)
> 下の表は **$\beta=2$ をアンカーに使う**前提で書かれているが、**$\beta$ を使うのは誤り**である(`scratchpad/local3_udih_anchor_and_s9_conventions_v1.md` §A.3 訂正 C-A3):
> $\beta$ の向きは幾何の規約 D ではなく Kummer marking + 正規化定数 $c\in(\mathbb Z/9)^\times$(**§6.6 P-a で未固定**)で決まるため、アンカーで消すはずの自由度が再流入する。
> **正しいアンカーは二面体側 cover を規約 D で計算した $u_{\rm dih}=\pm2^{-7}$**(passport $(9;2^41;2^41)$・種数 0・$\mathrm{Aut}=1$ ⟹ 捻りなしで一意・Chebyshev $T_9$)。
> $[u_{\rm dih}]_3=[2]^{-1}=[2]^2=[\beta]_3^{-1}$ なので、**下表の $c'$ 列は真逆である。**
>
> **訂正後の予言表**(アンカー $S_{\rm anc}=\mathrm{cube}(u_{\rm dih})$・$S_u=S_{\rm anc}^{c'}$):
>
> | 規約 D が採る量 | $S_u$ vs $S_{\rm anc}$ | **$c'$(正)** | 旧表の値(誤) |
> |---|---|---|---|
> | $u_{S4}=u_0$($[2]^2$) | $S_u=S_{\rm anc}^{1}$ | **$+1$** | $-1$ |
> | $u_{S4}=u_0^{-1}$($[2]^1$) | $S_u=S_{\rm anc}^{2}$ | **$-1$** | $+1$ |
>
> **さらに(裁定 1719/1720)**: falsifier の producer code 判読により **$u_{S4}=u_0$ が確定**(L118/L120 の明示宣言 + $T=1/t$ 代数)⟹ **$c'=+1$**。
> **かつ(2026-08-28・本ノート §7.3.6)**: 規約 D の「両窓同一レシピ」を S4 側でも完全に実行(3 点 Möbius 正規化)しても、**正規化因子 $\tau_k-\tau_j=\pm3\sqrt{-3}=(\mp\sqrt{-3})^3$ は完全立方**ゆえ $[u_{S4}]_3$ は不変 ⟹ **$c'=+1$ は正規化を入れても不変**(8/8 素数で機械確認)。

~~**予言表**($\beta=2$ 前提・$[u_0]_3=[2]^2$、$[u_0^{-1}]_3=[2]$ は §6.4 で確定)~~ ⟹ **上の訂正表で置換。以下は歴史的記録。**

| ~~規約 D が採る量~~ | ~~$\left(\frac{\cdot}{p}\right)_3$ の関係~~ | ~~**$c'$**~~ | ~~選ばれる候補~~ |
|---|---|---|---|
| ~~$u_{S4}=u_0$~~ | ~~$S_u=S_\beta^{2}$~~ | ~~$c'=-1$~~ | ~~一方~~ |
| ~~$u_{S4}=u_0^{-1}$~~ | ~~$S_u=S_\beta^{1}$~~ | ~~$c'=+1$~~ | ~~もう一方~~ |

> ★ **重要**: この表は「**$c'$ は規約 D の 1 ビットと等価**」を示している。$\beta=2$ が正しければ、**$c'$ を決める作業 = 規約 D を幾何的に確定する作業**であり、素数計算そのものは $\beta=2$ の**検定**(下記)として働く。
> **$\beta$ の検定(副産物・同じ素数で無料)**: $\left(\frac{u_0}{p}\right)_3$ と $\left(\frac{2}{p}\right)_3$ が**すべての選んだ素数で同じ巡回部分群を張る**こと。張らない素数が 1 つでも出れば $\beta\ne2$ か linkage(P5′)自体が偽 ⟹ **STOP**。12 素数で $\beta{=}2$ と $\beta{=}3$ は実質分離($2/3$ が mod $p$ の立方になる密度 $\sim1/3$ ゆえ 12 素数で $3^{-12}$)。

### 7.3.4 破壊対照(必須)

| # | 対照 | 期待 |
|---|---|---|
| **DC-1(向き flip)** | S4 で規約 D を故意に反転($u\mapsto u^{-1}$)して S1–S9 を再走 | **$c'$ が反転し SELECT が入れ替わる**。入れ替わらなければ実装が向きを見ていない = 仕様不履行 |
| **DC-2(埋め込み flip・ORIENT (a) 実測)** | $\mu_3(\mathbb F_p)$ の生成元を $\bar\zeta_3\mapsto\bar\zeta_3^2$ に取り替えて S7/S8 を再走 | **$c'$ と SELECT は不変**(離散対数が両方反転して比が保たれる)。変われば ORIENT (a) の実装違反 |
| **DC-3(立方数注入)** | $u_{S4}\mapsto a^{-9}u_{S4}$($a$ 任意の有理数)で再走 | **$S_u$ 不変**(7.3.0)。変われば mod 3 還元の実装ミス |
| **DC-4(陰性)** | 条件 (iii) を満たさない素数($S_\beta=1$)を投入 | **判別不能で停止**(勝手に $c'$ を返したら fail-closed 違反) |
| **DC-5(素数間一貫性)** | 3 素数で SELECT 一致 | 一致しなければ $\beta$ か linkage が偽 ⟹ STOP。★**一致しても規約 D の正しさは保証しない**(全素数が同時に反転するため) |

### 7.3.5 射程・格(厳守)

- この 1 row が閉じるのは **NN-09 / NN-12 の選択のみ**。
- **自動昇格しないもの**: $|A|=324$ の値そのもの(前件 = P1 発効・裁定 970 の S4 算術飽和・isolated 性)/ 648 の genuine-fake 判定 / $\mathrm{Im}(\mathrm{Ih}_M)=A$ の等号 / IDX3 の他の pin。
- 格 = **candidate**。cross-checked にするには (i) 独立実装の第二系統、(ii) DC-1〜DC-5 全通過、(iii) 432-key canary(§7.1)PASS が要る。
- ~~**最大文**: 「… **規約 D の幾何的確定($u_{\rm dih}$ の同一レシピ計算)が済むまで、選択は規約相対**。」~~ ⟹ **§7.3.6 で更新**(アンカー計算済・S4 側正規化も解消)。

### 7.3.6 ★ S4 側正規化の解消(2026-08-28・裁定 1717①/1720)

**falsifier の重大所見**: 規約 D の「両窓同一レシピ」は**不成立だった** — 二面体側は 3 点 Möbius 完全正規化済みだが、**S4 側はモデル所与の $t$ をそのまま使っていた**。しかも S4 側の $3^3$ 分岐点対は
$$\tau_{1,2}=\tfrac32\pm\tfrac32\sqrt{-3}\qquad(\tau_1+\tau_2=3,\ \tau_1\tau_2=9,\ \text{min.\ poly }x^2-3x+9)$$
という **ℚ 上共役な無理数対**で、3 点正規化 $(\infty,\tau_1,\tau_2)\to(0,1,\infty)$ は ℚ-有理でない。スカラーは mod 3 で load-bearing(falsifier 実測: $u_{\rm dih}=2^{-7}\Rightarrow c'=+1$ / $2^{-8}\Rightarrow c'=-1$ が全素数で反転)。

> ### ★ 解決 = 候補 (ii)(不変性の証明)。**正規化因子は完全立方ゆえ mod 3 で無害。**
> index-9 cusp は $t=\infty$ 上(cert は $u_0=-1/\lim(t\,s^9)$ を計算)。3 点正規化の Möbius は
> $$\mu(w)=\frac{\tau_k-\tau_j}{w-\tau_j}\quad(\{j,k\}=\{1,2\}),\qquad t'=\mu(t)$$
> で、cusp 近傍 $t\to\infty$ より
> $$u_{S4}^{\rm norm}=\lim_{s\to0}\frac{t'}{s^9}=\frac{\tau_k-\tau_j}{\Lambda},\qquad \Lambda:=\lim_{s\to0}t\,s^9=-\frac1{u_0}.$$
> ここで $\tau_2-\tau_1=-3\sqrt{-3}$ であり、$\lambda:=\sqrt{-3}$ とおくと $\lambda^2=-3$ ゆえ
> $$\boxed{\ 3\sqrt{-3}=3\lambda=(-\lambda^2)\lambda\cdot(-1)=-\lambda^3=(-\lambda)^3\ }$$
> すなわち **$\pm3\sqrt{-3}$ は $\mathbb Q(\zeta_3)^\times$ の完全立方**($-1=(-1)^3$ も立方)。$1/\Lambda=-u_0$ も $-1$ 倍だけ。
> $$\Longrightarrow\ [u_{S4}^{\rm norm}]_3=[u_0]_3\ \ \text{in}\ \mathbb Q(\zeta_3)^\times/(\mathbb Q(\zeta_3)^\times)^3 .$$
> ⟹ **3 点正規化を入れても $c'$ は変わらない。$u_{S4}=u_0$ を使ってよい。**
> **どちらの $\tau$ を 1 に送るかも無害**($\tau_k-\tau_j$ の符号だけ変わり $-1$ は立方)。

**機械確認**($p\equiv1\ (9)$・`scratchpad/math_s4norm_v1.py`):
```
gate: (-sqrt(-3))^3 == 3*sqrt(-3) ?  True      tau1+tau2 = 3 ; tau1*tau2 = 9
gate: p=19,37,73,163,181,199,271,373  (109/127/307/397 は判別力条件で degenerate)
      cube(3*sqrt(-3)) == 1 : 8/8
      c'(u_S4=u0) == c'(u_S4=normalised) : 8/8      [ 全て c' = +1 ]
gate: falsifier の感度検査の再現 — u_dih=2^-7 -> c'=+1 / 2^-8 -> c'=-1 : 全素数で反転 True
```
⚠ **$2^{-8}$ は「3 点正規化を完了していない」場合の値**($\mu(w)=1/w$ は第 3 分岐点を $\infty$ に送らない)。⟹ **falsifier の感度検査は「3 点正規化こそが値を pin する」ことの確認になっている。**

**格の更新**: SELECT の上限は ~~candidate(S4 側正規化相対)~~ ⟹ **candidate(正規化解消済・census ラベル D-6 相対)**。
**新・最大文**: 「規約 D を両窓で完全に実行し(S4 側の 3 点正規化因子は完全立方ゆえ mod 3 で無害)、アンカー $u_{\rm dih}=\pm2^{-7}$ に対し $c'=+1$ を得た。残るは census ラベル写像 D-6 のみ。」

---

# §8 定理 DICHOT-972 — 段の二択律・落下時刻の 1 パラメータ化(2026-08-23・研究者発案の骨格再生)

**状態札**: `定理(前件 pin 明示・自前証明)/ 2401 の番号は本起草者が頁テキストで直接確認 / cofinality 評価(§8.6)は見立て(candidate)`

## 8.1 設定と定理文

$M=K^{(9)}\cap N_{S4}$、$X:=GT(M)$($|X|=972$)、$A:=\mathrm{Im}(\mathrm{Ih}_M)$。$K\le M$($B_3$-normal・有限指数・**isolated**)に対し
$$I_K:=\mathrm{Im}\bigl(R_{K,M}:GT(K)\longrightarrow GT(M)\bigr).$$

> ### 定理 DICHOT-972
> **(1) 二択律.** $\ I_K\in\{A,\ X\}$。各段で「**648 全員リフト**」か「**648 全員非リフト**」の二値のみ。
> **(2) 一様 fibre.** $I_K=X$ なら 972 個の fibre はすべて $\ker R_{K,M}$ の剰余類で**一律 $\lvert GT(K)\rvert/972$**。$I_K=A$ なら $A$ 上が一律 $\lvert GT(K)\rvert/324$、$X\setminus A$ 上は**全て空**。
> **(3) 段証明書の経済.** 段 $K$ の帰趨は **$X\setminus A$ の元 1 個**で決まる。1 個でもリフトすれば $I_K=X$(全 648 リフト)、1 個でもリフトしなければ $I_K=A$(全 648 非リフト)。**全数調査不要・両向きに 1 元。**
> **(4) 二値出口の統一.** **(a)** ある段で $I_K=A$ ⟹ 648 は全て非 genuine = **gentle-fake**。**(b)** cofinal 族の全段で $I_K=X$ ⟹ 各元の fibre 系が非空有限の逆系ゆえ極限が非空 ⟹ 648 は全て **genuine**、$A$ の外ゆえ **非算術証人**。**(a)(b) は同一定理の二枝。**
> **(5) 単調性.** 塔 $M\ge K_1\ge K_2\ge\cdots$(isolated)で $I_{K_1}\supseteq I_{K_2}\supseteq\cdots\supseteq A$ ⟹ 列は $X,\dots,X,A,A,\dots$ の形、**遷移は高々 1 回**。塔全体は**落下時刻 $n_0\in\{1,2,\dots,\infty\}$ という 1 個のパラメータ**に還元される。

## 8.2 前件 pin(2401.06870 の番号は頁テキストで直接確認)

| 札 | 内容 | pin |
|---|---|---|
| **P-i-a** | isolated $N$ で $GT(N)=GTSh(N,N)$ は**群** | **Def 3.13 直後の一文**(逐語 "In particular, GT(N) is a group.") |
| **P-i-b** | $N\le H$ がともに isolated なら $R_{N,H}$ は**群準同型** | **Remark 3.16**(逐語 "we call $R_{N,H}$ … the reduction homomorphism"・§5 冒頭で再引用) |
| **P-i-c** | $R_{N,H}$ の well-defined 性(同一代表対) | **Prop 3.12** + **(3.60)** |
| **P-i-d** | 関手性 $R_{K,H}=R_{N,H}\circ R_{K,N}$ | (3.53) が代表対で定義(**Thm 3.10**)ゆえ直ちに |
| **P-i-e** | isolated 部分 poset は **cofinal** ⟹ 塔を isolated に制限してよい | **Prop 3.14** + 直後の一文。**Prop 3.15**(交わりで閉じる) |
| **P-i-f** | $M$ が isolated | 工房実測(裁定 1133) |
| **P-ii** | $A\subseteq I_K$ | §8.3 の 1 行証明(**(4.10)**) |
| **P-iii** | $\lvert A\rvert=324$、$[X:A]=3$ | 裁定 970(S4 窓算術飽和・**前件 P1–P5 相対**)+ P1 発効 + TRIAD-972。**$A$ の同定($c'$)は不要** |
| **P-iv** | genuine ⟺ 全細分に survive | **Cor 5.4** |
| **P-v** | $\widehat{GT}_{\rm gen}\cong\varprojlim$(isolated poset 上) | **Thm 5.2** |

## 8.3 証明

**(P-ii)・1 行**: $PR_N(\hat m,\hat f)=[\hat P_{N_{\rm ord}}(\hat m),\ \hat P_{N_{F_2}}(\hat f)]$(**(4.10)**)は**同一代表対 $(\hat m,\hat f)$ の還元**ゆえ $PR_M=R_{K,M}\circ PR_K$。$\mathrm{Ih}_\bullet=PR_\bullet\circ\mathrm{Ih}$ より $\mathrm{Ih}_M=R_{K,M}\circ\mathrm{Ih}_K$、よって $A\subseteq I_K$。∎

**(1)**: P-i-a/b より $I_K\le X$ は部分群。P-ii より $A\le I_K\le X$。$[X:A]=3$ は素数ゆえ $[X:I_K]\mid3$ ⟹ $A$ は極大 ⟹ $I_K\in\{A,X\}$。∎

**(2)**: 準同型ゆえ非空 fibre は $\ker R_{K,M}$ の左剰余類で大きさ一律 $\lvert GT(K)\rvert/\lvert I_K\rvert$。∎ ⟹ **OBS-UNIF-1 は観測から条件付き定理へ昇格**。

**(3)**: (1) より $I_K\in\{A,X\}$。$g\in X\setminus A$ が 1 個でも $I_K$ に入れば $I_K\supsetneq A$ ⟹ $I_K=X$。1 個でも入らなければ $I_K\ne X$ ⟹ $I_K=A$。∎

**(4)(a)**: $I_K=A$ ⟹ $g\in X\setminus A$ は $K$ に survive しない ⟹ Cor 5.4 の対偶で非 genuine。∎
**(4)(b)**: cofinal な isolated 族(P-i-e)で $I_K=X$ なら、$g$ 上の fibre 族は**有向系上の非空有限集合の逆系**ゆえ $\varprojlim\ne\emptyset$ ⟹ Thm 5.2 で $g$ は genuine、$g\notin A$ ゆえ非算術。**一意リフト(unique-pass)は不要 — 非空性のみでよい。**∎

**(5)**: $R_{K_{n+1},M}=R_{K_n,M}\circ R_{K_{n+1},K_n}$(P-i-d)⟹ 像は単調減少。値域が 2 元鎖 $\{A\subsetneq X\}$ ゆえ遷移は高々 1 回。∎

## 8.4 照合表(OBS-UNIF-1 の定理化)

実測 fibre $=\lvert\ker R\rvert$ = 2,2,2,3,9 ⟹ $I_K=X$ の下での予言:

| 窓 | 実測 $\lvert\ker R\rvert$ | **予言 $\lvert GT(K)\rvert=972\times$** |
|---|---|---|
| 1,2,3 | 2 | **1944** |
| 4 | 3 | **2916** |
| 5 | 9 | **8748** |

> ★ **母数の注意(監査項目・Sol へ発注済)**: 上の 5 窓で「**全 972 target 上で fibre 非空**」が測定されているなら、(1)(2) により **$I_K=X$ が 5 段で確定**し、(5) の単調性から **落下時刻 $n_0>5$**(現時点で落下は未発生)。しかし histogram の母数が $A$ 側 324 に限られていた場合、この結論は**出ない**。**F2 型(母数不一致)の再演を避けるため cert の実母数を確認すること。**

## 8.5 依存表

| 帰結 | P-i(群・準同型) | P-ii | $[X:A]=3$ | **$A$ の同定($c'$)** | Cor 5.4 | Thm 5.2+cofinal |
|---|---|---|---|---|---|---|
| (1) 二択律 | ● | ● | ● | **不要** | – | – |
| (2) 一様 fibre | ● | ○($A$ 側の数え上げのみ) | ○ | **不要** | – | – |
| (3) 1 元経済 | ● | ● | ● | **不要** | – | – |
| (4a) fake 判定 | ● | ● | ● | **648 の名指しにのみ必要** | ● | – |
| (4b) 証人存在 | ● | ● | ● | **648 の名指しにのみ必要** | – | ● |
| (5) 単調性 | ●(P-i-d) | ● | ● | 不要 | – | – |

★ **(1)(3) は $c'$ を一切使わない** — 必要なのは $\lvert A\rvert=324$($[X:A]$ が素数)と $A\subseteq I_K$ のみ。⟹ **LOCAL-3 の 1 ビットが未決のまま段実験を走らせられる**(seed の取り方は §8.7)。

## 8.6 cofinality の壁 — 評価 5 点

**再定式化(最大の収穫)**: (5) により「一様な帰納 1 本」は無限個の段の主張ではなく、**単一の主張「落下は起きない」**である。$n_0=\infty\iff$ 648 が genuine $\iff PR_M$ 全射。

1. **unique-pass 切断は捨ててよい。** (4b) は非空性だけで通る(逆系の compactness)ので一意性は不要。しかも実測 fibre 2,2,2,3,9 が全て $>1$ ⟹ **unique-pass は経験的に偽**。この機構に投資しない。
2. **境界方程式の安定性。** 一段 $K\to K'=[K,K]K^p$ の持ち上げは T-DEF 型のアフィン線型系、障害は $H^2(Q,V)$(KER-π)。帰納段には **障害の関手性**($H^2(Q_n,V_n)\to H^2(Q_{n+1},V_{n+1})$ の自然可換と消滅の伝播)が要る — **現状なし**。有利な点: (2) が「fibre = $\ker R$ の全剰余類」を与えるので試行が $\lvert\ker R_{K_n,M}\rvert$ 個あり、帰納段は**存在型**で足りる。
3. **★ 正側は原理的に井原と同値(壁の正体)。** 83 線では「族機構が届かない場所を**算術**が埋めた」(T-ARITH)。**972 では同じ手が使えない** — 標的は $A=\mathrm{Im}(\mathrm{Ih}_M)$ の**外側**ゆえ算術は定義上一切供給できない。⟹ **(4b) 側の証明は「genuine かつ非算術」の構成そのもの = 井原予想の反例構成**。無料の帰納は存在しない。
 ⟹ **経済の非対称が決定的**: (4a) 側は **1 段 × 1 元**で閉じ、(4b) 側は井原と同値。**資源は落下側(fake)に振るのが正しい。**
4. **必要な追加構造 3 点。** ①**Zassenhaus 塔への置換**(graded 簿記 = `gt_grt_dictionary_memo_v1.md` §4): Frattini 塔は層が爆発するが Zassenhaus 塔なら層 $\mathcal L_n$ が Witt/Jennings で**一様記述**でき、帰納段の言明が初めて**書ける形**になる。②**障害関手性補題**(評価 2)。③**surjectivity-in-the-limit 補題**。
 > ★ **L-1 統合(司令塔へ)**: ③ は 83 線で私が出した【**文献要請 L-1**】(「副有限/pro-p 塔での Frattini 段持ち上げの一様性」・`c83_inn_lift_lemma_v1.md` §2.8)と**同一の欠落補題**である。**83 の壁と 972 の壁は同じ 1 本**。文献要請は統合して 1 本にすることを具申する(統合は司令塔で引き取り)。
5. **反例リスク・prior。** 姉妹窓で **BIT-252 = VERDICT A(0/117,649)= 落下が実際に観測されている** ⟹「落下は起きない」への事前確率は低い。逆に **ESCAPE-28**(dim $H^2\ne0$ なのに 1,099,008 行で障害類が全消滅)は非落下側の兆候で、**入力定理から説明の出ない未知の消滅機構**の実在可能性を示す。⟹ 総合 **UNKNOWN**、ただし**探索設計は落下側に置くべき**。

**具申(1 行)**: 次の実験は「**cofinal 塔の各段で $X\setminus A$ の元 1 個の lift を試す**」— (3) により各段が 1 元で決まり、(5) により落下は 1 回しか起きないので、**最初に落ちた段がそのまま証明書**になる。$c'$ の確定は並行でよい。

## 8.7 段実験の seed pool($c'$ 未決のまま走らせる方法)

$A\in\{\text{NN-09},\text{NN-12}\}$ ゆえ $A\subseteq \text{NN-09}\cup\text{NN-12}$、したがって
$$\boxed{\ \mathcal S:=X\setminus(\text{NN-09}\cup\text{NN-12})\ \subseteq\ X\setminus A\qquad(\text{$c'$ のどちらでも成立})\ }$$
$\lvert\text{NN-09}\cup\text{NN-12}\rvert=324+324-108=540$ ⟹ $\lvert\mathcal S\rvert=972-540=\mathbf{432}$。**非空ゆえ seed は必ず取れる。** (3) の両向き(lift ⟹ $I_K=X$ / 非 lift ⟹ $I_K=A$)ともこの seed で有効。

> ⚠ **NAME-COLLIDE 警告(必読)**: 「432」は本戦役で**二つの異なる集合**の大きさとして現れる。
> - $\mathcal S=X\setminus(\text{NN-09}\cup\text{NN-12})$(**432 元**)= **seed pool**。$c'$ に依らず $X\setminus A$ に入る。
> - $\text{NN-09}\,\triangle\,\text{NN-12}$(**432 元**)= §7.1 (e) の **対称差 = $c'$ canary の対象**。こちらは**半分が $A$ の中に入る**ので **seed に使ってはならない**($A$ 側の元をリフトしても情報ゼロ)。
> cert・報告では必ず `seed_pool_432` と `symdiff_432` を**別フィールド名**で書き分けること。

---

# §9 補題 BRUN-DEF と PENT-WINDOW 設計 — 「$B_3$ 梯子に pentagon を織り込めない」の正面回答(2026-08-23・裁定 1638)

**状態札**: `§9.2 = paper-proof candidate(pin 2 点明記)/ §9.3 = 系(補題相対)/ §9.5(c) = 定理(自前証明)/ §9.5(a)(b) = 設計 candidate / §9.6 = 正直条項`
**委嘱**: 司令塔(研究者の反論「一様リフトの有限計算に pentagon 判定を織り込めないのはなぜか」への正面回答の定理化)。参照: Sol §12.6 の comparator 機構・$C_M$ blind 実測・便 159 §17(strand deletion は 2008 形式の演算ではない)。

## 9.1 記号

$d_i:PB_4\to PB_3$($i=1,\dots,4$)= 第 $i$ ストランド削除。**群準同型だが 2008 の operad 形式の演算ではない**(便 159 §17: Def 2.1 の演算は composition/symmetric/positive-arity insertion のみ・p.7 fn.7 で $PaB(0)=\emptyset$)。
$$\mathrm{Br}:=\bigcap_{i=1}^{4}\ker d_i\qquad(\text{古典的 Brunnian 純組紐群 }\mathrm{Brun}_4).$$
$(m,f)$ の pentagon 欠陥を Drinfeld 正規化の **ordered residual** で
$$D(f):=\Phi^{1,2,3}\,\Phi^{1,23,4}\,\Phi^{2,3,4}\cdot\bigl(\Phi^{12,3,4}\,\Phi^{1,2,34}\bigr)^{-1}\in PB_4,\qquad \Phi:=f$$
と置く(2008 (2.20) の pentagon $\iff D(f)=1$)。

## 9.2 ★補題 BRUN-DEF

> ### 補題 BRUN-DEF
> $f\in[F_2,F_2]$(= **charming**)ならば $\ \boxed{\,D(f)\in\mathrm{Br}\,}$。**hexagon は使わない。**

**証明.** charming ゆえ $f(A,1)=f(1,B)=1$(1 生成元を $1$ に落とすと $[F_2,F_2]\to[\mathbb Z,\mathbb Z]=1$)。ブロック退化則(ブロックが空になれば当該引数が $1$、空でなければブロックが縮む)を各削除に適用する:

| | $\Phi^{1,2,3}$ | $\Phi^{1,23,4}$ | $\Phi^{2,3,4}$ | $\Phi^{12,3,4}$ | $\Phi^{1,2,34}$ | $d_i(D)$ |
|---|---|---|---|---|---|---|
| $d_1$ | $1$ | $1$ | $\Phi^{2,3,4}$ | $\Phi^{2,3,4}$ | $1$ | $\Phi^{234}\cdot(\Phi^{234})^{-1}=1$ |
| $d_2$ | $1$ | $\Phi^{1,3,4}$ | $1$ | $\Phi^{1,3,4}$ | $1$ | $=1$ |
| $d_3$ | $1$ | $\Phi^{1,2,4}$ | $1$ | $1$ | $\Phi^{1,2,4}$ | $=1$ |
| $d_4$ | $\Phi^{1,2,3}$ | $1$ | $1$ | $1$ | $\Phi^{1,2,3}$ | $=1$ |

∎

**精密化・反例条件・格**
- **入力は charming のみ** — 委嘱文の「hexagon+charming」より**強い**。Sol §12.6 の comparator(deletion 座標で五 coface が direct 2 + cyclic 3 に分かれる)は、この ordered residual 形では「**空ブロック消滅 + 生存 1 対の相殺**」に縮約される。
- **反例条件**: $f\notin[F_2,F_2]$ なら $f(A,1)\ne1$ で表の $1$ が壊れ $d_i(D)\ne1$ となりうる ⟹ **charming が本質**。
- **格 = `paper-proof candidate`**。載荷 pin 2 点(未確認): **(pin-1)** 欠陥の**形**が (2.20) の ordered residual であること(PENT-FORM′ 形での対応版は別途同型計算が要る)。**(pin-2)** **ブロック退化則**(削除と operad ブロック記法の両立)。いずれも 2008 App A の頁画像 pin を要する。
- **$D(f)\in\mathrm{Br}$ であって $D(f)=1$ ではない** — **pentagon は本物の条件で、削除型の窓に見えないだけ**。

## 9.3 ★系 C-BLIND — 委嘱の本命

> ### 系 C-BLIND
> 任意の $K\le PB_3$ と $C_K:=\bigcap_i d_i^{-1}(K)$ に対し $\mathrm{Br}\subseteq\bigcap_i\ker d_i\subseteq C_K$。ゆえに charming な全ての $f$ で $D(f)\in C_K$、すなわち
> $$\boxed{\ \textbf{deletion 引き戻し型 }B_4\textbf{ 窓 }C_K\ \textbf{は pentagon に恒真 = 0 ビット}\ }$$
> ⟹ **「$B_3$ 梯子の上で一様に pentagon を判定することは不可能」の正確な理由**: $B_3$ 窓から削除で引き戻して作った $B_4$ 商は、**定義により $\mathrm{Br}$ を殺す**。pentagon 欠陥は $\mathrm{Br}$ に値をとるので、**この作り方の窓では原理的に見えない**。
> ⟹ pentagon を見るには **$\mathrm{Br}$ を分離する $B_4$ 固有の有限商**が要る(§9.5)。

## 9.4 novelty 申告と証拠の扱い

- **novelty**: 工房既在の**定理 B4-VAC**(`b4_direct_adjudication_feasibility_v1_2.md` §0-2 —「Prop 3.9 の構成に現れる 2 つの自然な窓で (2.20) は全 charming $f$ に恒真」)は**本系の特殊例**。BRUN-DEF の寄与は **(i) 機構の同定($\mathrm{Br}$ に値をとる)** と **(ii) $C_K$ 族全体への一般化**であり、**現象の初報ではない**。
- **証拠の扱い(必記)**: $C_M$ blind の実測(**78,732 全量・空 0**)は本補題の予言と一致するが、**証拠には数えない — 時系列で測定が先**である。本補題は測定の**構造的説明**として提出する(retrospective agreement)。

## 9.5 PENT-WINDOW の設計

### (a) 深さの下限と窓候補

> **命題 BR-DEPTH.** $\mathrm{Br}\subseteq\gamma_3(PB_4)$ かつ $\mathrm{Br}\not\subseteq\gamma_4(PB_4)$。
> **理由**: Brunnian 元は 4 本すべての削除で自明 ⟹ 長さ $\le3$ の Milnor 不変量が全消滅 ⟹ $\gamma_3$ に入る(純組紐の LCS = Milnor filtration)。標準的 Brunnian 4-組紐は $\mu(1234)\ne0$(次数 3)ゆえ $\gamma_4$ には入らない。〔Milnor filtration = LCS の同一視は標準事実・**candidate 札**〕
> $$\boxed{\ \textbf{PENT-WINDOW は冪零類 }\ge3\ \textbf{が必要。最小は類 3。}\ }$$

**候補(verbal・探索不要)**: $\ \mathbf W_\ell:=\gamma_4(PB_4)\,PB_4^{\,\ell}$。$PB_4$ の verbal 部分群 ⟹ characteristic、$PB_4\trianglelefteq B_4$ ⟹ **$B_4$-正規・有限指数 ⟹ $\mathbf W_\ell\in NFI_{PB_4}(B_4)$**(lins 探索も chief 塔資産も不要)。

**次元**: $\mathrm{gr}(PB_n)=\mathfrak t_n$(Drinfeld–Kohno)、$\mathrm{Hilb}\,U(\mathfrak t_n)=\prod_{k=1}^{n-1}(1-kt)^{-1}$ + PBW より
$$\dim\mathfrak t_4=(6,\,4,\,10),\qquad \dim\mathfrak t_3=(3,\,1,\,2)\quad(\text{次数 }1,2,3).$$

| 窓 | 類 | $\lvert PB_4/N_4\rvert$ | $\mathrm{Br}$ を見るか | 実行可能性 |
|---|---|---|---|---|
| $C_K$(削除引き戻し) | 任意 | 任意 | **否**(系 C-BLIND) | **0 ビット** |
| $\mathcal V(PB_4)=\gamma_5PB_4^{7}$(**NW(7) 既在**) | 4 | $7^{41}$ | 是 | 既在だが過大 |
| **$\mathbf W_2=\gamma_4PB_4^{2}$** | **3** | $\approx2^{20}\approx10^{6}$ | 是(要 mod-2 canary) | **pc 群・秒** |
| **$\mathbf W_3=\gamma_4PB_4^{3}$** | **3** | $\approx3^{20}\approx3.5\times10^{9}$ | 是 | pc 群で可・元演算やや重 |

**残差の受け皿**: $D(f)\bmod\mathbf W_\ell$ は $\bigl(\bigcap_i\ker d_i\bigr)\cap\mathfrak t_{4,3}\otimes\mathbb F_\ell$ に住む。char 0 での次元下界 $\ \ge 10-4\times2=\mathbf 2$ ⟹ **非自明な受け皿が実在**。

### (b) 必要な $f$ の解像度

$\mathbf W_\ell$ の像は類 3・指数 $\ell$ ゆえ $f(A,B)$ は $f\bmod\gamma_4(F_2)F_2^{\ell}$ にのみ依存。
$$\boxed{\ N_{F_2}\subseteq\gamma_4(F_2)F_2^{\ell},\qquad \lvert F_2/\gamma_4F_2^{\ell}\rvert=\ell^{2+1+2}=\ell^{5}\ }$$
($\ell=2$: 32 通り / $\ell=3$: 243 通り)。

### (c) ★噛み合い定理 — 現行 $B_3$ 梯子とは**そのままでは噛み合わない**

> **定理 MESH-NEG.** $M=K^{(9)}\cap N_{S4}$ に対し、**任意の $\ell$ で $M_{F_2}\not\subseteq\gamma_4(F_2)F_2^{\ell}$**。
> **証明.** 必要条件は $F_2/M_{F_2}\twoheadrightarrow F_2/\gamma_4F_2^{\ell}$(類 3 の非可換 $\ell$ 群)。ところが $G_9\le D_9^3$ の 3-部は $C_9^3$ の部分群で**可換**、かつ $G_9^{ab}=C_2^2$ ゆえ $G_9$ に非自明 3-商はない;$PSL(2,8)$ は単純ゆえ非自明冪零商をもたない。$F_2/M_{F_2}$ は両者の subdirect product の商なので**最大冪零商は可換**(2 群)。非可換な類 3 群はその商になりえない。∎
> ⟹ **972 窓の shadow データだけからは pentagon 残差は計算できない。**

> ★ **これは NILP-VOID(`gt_grt_dictionary_memo_v1.md` §3.2)と同一の現象である。972 窓の非冪零性が、Soulé 輸入と pentagon 織り込みの両方を同じ理由で塞いでいる。**

**修理(安価)**: $\mathcal V^{(3)}_\ell(PB_3):=\gamma_4(PB_3)PB_3^{\ell}$(verbal ⟹ $NFI_{PB_3}(B_3)$)で細分:
$$M^{\sharp}_\ell:=M\cap\mathcal V^{(3)}_\ell(PB_3),\qquad [M:M^{\sharp}_\ell]\ \le\ \lvert PB_3/\mathcal V^{(3)}_\ell\rvert=\ell^{6}$$
($\ell=2$: **64 倍** / $\ell=3$: **729 倍**)。**解像度は 2 桁以内のコストで買える。**

### (d) interleaved 梯子(研究者提案の実現形)

各 $B_3$ 段 $K$ を $K^\sharp_\ell:=K\cap\mathcal V^{(3)}_\ell(PB_3)$ に置換すれば、**同じ段の lift データから $D(f)\bmod\mathbf W_\ell$ が評価できる**。追加物は $PB_4/\mathbf W_\ell$ の pc 群 1 個(一度きり)と各段 $\ell^6$ 倍の細分のみ ⟹ **$B_4$ 宇宙の建て直しは不要**。

- **判定の型(必記)**: DICHOT-972 (3) と同じく **fibre 量化**で行う。「選んだ代表の残差が $\ne0$」は不可、**$R^{-1}_{K^\sharp,K}$ の全 fibre で残差 $\ne0$** が要る。
- **得られる情報の種別(混同禁止)**: pentagon 失敗 ⟹ **$\widehat{GT}$(proper)の像に無い**。**$\widehat{GT}_{\rm gen}$-genuine 性については何も言わない**(§8 の 648 gentle-fake 問題とは別軸)。工房の endgame_scope pin(B 分岐は $B_4$ 層必須・PENT_W-PASS)に対する正しい計器はこちらである。

## 9.6 正直条項(stop 条件・未確認事項)

1. **mod-$\ell$ 消滅 canary(最初に走らせる・小)**: $\bigcap_i\ker(d_i)\cap\mathfrak t_{4,3}$ を $\mathbb F_\ell$ 上で計算(10 次元 → $4\times2$ 次元の線型代数)。**$\ell=2$ で $0$ なら $\mathbf W_2$ は無効 ⟹ $\ell=3$ へ**。両方 $0$ なら類 3 では不足で類 4($7^{41}$ 級)へ跳ぶ ⟹ **その時点で費用見積りを出して stop**。
2. **★最大の未知 = 深さ問題**: $\mathrm{Br}\subseteq\gamma_3$ は示したが、**我々の $f$ の $D(f)$ が $\gamma_4$ に落ちてしまう可能性は排除していない**(落ちれば類 3 窓で再び 0 ビット)。判定は canary 1 と同じ計算に $D(f)$ を 1 個流すだけ(既存 A 型計器の語評価が流用可)。**canary 実測が返ったらここの判読を行う。**
3. **BRUN-DEF の pin 2 点**(§9.2 の pin-1/pin-2)が未確認のうちは系 C-BLIND も candidate。**$C_M$ blind 実測は証拠に数えない**(§9.4)。
4. **推測で埋めない範囲**: $\lvert\mathbf W_3\rvert\approx3.5\times10^9$ の元演算コスト、$M^\sharp_3$ 上の shadow 列挙コストは**未見積り**。$\ell=2$ が canary を通れば見積り不要、通らなければ**見積りを出してから**発注のこと。

---

# §10 狙撃レーン標的選定基準(2026-08-23・c′ 着弾前に凍結)

**状態札**: `§10.1 の XOR 特徴づけは定理(census 数と 3 点整合)/ §10.2 の層別は設計 / §10.4 は射程・落とし穴`
**前提の一行**: DICHOT-972 (3) により**どの 648 元を選んでも判定結果は同じ**。標的選定は**書きやすさだけ**の問題で、数学的リスクを持ち込まない。

## 10.1 ★ seed pool の構造的特徴づけ(XOR)

境界不変量 $\Delta(g):=\Psi(\pi)-c'\,(k\bmod3)\in\mathbb Z/3$($A=\{\Delta=0\}$)。$m$ ごとに $(k,\pi)\in(\mathbb Z/9)\times\Pi_m$ は**完全直積 81**(§1.1)、$\Psi:\Pi_m\twoheadrightarrow\mathbb Z/3$ は fibre 3。

$$\boxed{\ \mathcal S\ \bigl(=X\setminus(\text{NN-09}\cup\text{NN-12})\bigr)\ =\ \bigl\{\ \Psi(\pi)=0\ \ \textbf{XOR}\ \ k\equiv0\ (\mathrm{mod}\ 3)\ \bigr\}\ }$$

**検算(census と 3 点整合)**: $m$ ごとに $\lvert A_\pm\rvert=9\times3=27$(×12 = **324** ✓)/ $\lvert A_+\cap A_-\rvert=3\times3=9$(×12 = **108** ✓)/ $\lvert A_+\cup A_-\rvert=3\cdot3+6\cdot6=45$ ⟹ $81-45=36$(×12 = **432** ✓)。
⟹ **$c'$ を知らずに seed を構造式で書ける。**

## 10.2 層別座標と順序付け

| 座標 | 値域 | 「式で書きやすさ」への効き | 順位 |
|---|---|---|---|
| **$m$** | $\mathcal X_{18}$(12 値) | $m=0$ なら $u=1$ で $T(x)=x,\ T(y)=f^{-1}yf$、hexagon から $y^{-m}c^m$ 捻れが消える。83 線の閉形式(補題 U′/T-EX/T-DEF)は**全て $m=0$** | **★★★ 第 1** |
| **$\pi$** | $\Pi_m$(9 値) | **$\pi=\mathrm{id}$** ⟹ $f\in N_{S4,F_2}$ で PSL 側の記述が消え、**Thm 4.3 + Lemma 4.2 の $(h_1,h_2,h_3)$ 構成が丸ごと使える** | **★★★ 第 2** |
| **$k$** | $\mathbb Z/9$ | $k\not\equiv0\ (3)$ が seed 条件($\pi=\mathrm{id}$ 側)。$m=0$ では $u=1$ ゆえ **$k$ は加法的**($k=k_1+k_2$)で位数計算が自明 | ★★ 第 3 |
| **$\Psi(\pi)$** | $\mathbb Z/3$ | $\Psi=0$ 側(3 個の $\pi$)が「純二面体寄り」。$\Psi\ne0$ 側は S4 モデルが要る | ★★ |
| **位数** | $\mid81$($m=0$ 層は位数 81 の 3 群) | $\pi=\mathrm{id}$ 側は $k$ が mod 9 の単元ゆえ**位数 9** | ★ |
| **語長** | artifact 第 3 欄に**実在** | 直接ソート可能(実務の決め手) | ★ |

| 層 | 元数 | 中身 | 評価 |
|---|---|---|---|
| **T1** $m=0,\ \pi=\mathrm{id},\ k\in\{1,2,4,5,7,8\}$ | **6** | **純二面体**。$\delta=(r^{2k},r^{-2k},r^{0})$、PSL 成分自明 | **★本命**。$\Psi(\mathrm{id})=0\wedge k\not\equiv0$ ⟹ **$c'$ に依らず 648** |
| T2 $m=0,\ \Psi(\pi)=0,\ \pi\ne\mathrm{id},\ k\not\equiv0$ | 12 | PSL 成分は $\ker\Psi$ 内 | 次点 |
| T3 $m=0,\ k\equiv0\ (3),\ \Psi(\pi)\ne0$ | 18 | $k=0$ なら**純 PSL**($\delta$ 完全自明) | S4 モデル要 ⟹ 後回し |
| T4 $m=9$ | 36 | $\chi_{vir}$ は $m=0$ と同値だが hexagon に $y^{-9}c^{9}$ が残る | 中 |
| T5 その他 $m$ | 360 | | 低 |

> ⚠ **用語訂正(必読)**: 972 は $N_{\rm ord}=18$ ゆえ $\chi_{vir}$ の二値対は **$\{m,\ m+9\}$**、すなわち「**$m=0$ 層 vs $m=9$ 層**」である。83 線の $\{0,6\}$ を転記すると誤りになる。$\ker\chi_{vir}=\{m\in\{0,9\}\}$(162 元)。

## 10.3 第一手の設計(標的 T1)

1. **$M$ 水準の $f$ は書く必要がない** — artifact 第 3 欄に**語が既にある**(canonical key で row を引くだけ)。
2. **書くべきは深い $K$ での閉形式リフト**。塔を $K_n:=K^{(9\cdot3^{n})}\cap N'_n$ に取れば、**二面体成分は Thm 4.3 が各水準で閉形式を与える** ⟹ **残る仕事は「PSL 側を自明に保つ補正」だけ**。
3. **補正**: $f_n:=f^{\rm dih}_n\cdot w_n$、$f^{\rm dih}_n$ = Lemma 4.2 の $(h_1,h_2,h_3)$ 構成、$w_n\in K^{(9\cdot3^n)}_{F_2}$ を $f_n\in N'_{n,F_2}$ となるよう選ぶ(有限 coset 探索)。
4. **検証**: hexagon (3.3)(3.4) を $B_3/K_n$ 上で(**語水準・c∉N・規約 W-1/W-2 厳守**)。二面体側は Thm 4.3 が恒等式を保証、joint は $\Lambda_{K_n}$ の charming 条件のみ。

## 10.4 射程・落とし穴(5 点・成果物へ転記必須)

1. **「式で書けた = genuine の証明」ではない。** 閉形式は各水準での存在を与えるだけで、**cofinal 族の全段**が要る(DICHOT-972 (4b) + Cor 5.4)。
2. **T-DEAD の教訓。** 83 線では厳密族の閉形式が cofinal 部分族の上で**必ず死んだ**。972 でも同型の死が起こりうる ⟹ **閉形式が途中で止まったら反証ではなく機構の限界**(死亡証明書と混同しない)。
3. **死亡証明書は fibre 量化必須。** 「選んだ閉形式リフトが段 $K$ で失敗」は $I_K=A$ の証明に**ならない**((S7′) 条件 2 と同型の誤り)。$R^{-1}_{K,M}(g^\ast)$ の**全 fibre**で lift 不在を示すこと。
4. **pentagon 検証は $C_K$ では不可。** BRUN-DEF/系 C-BLIND により削除引き戻し窓は **0 ビット**。**$\mathbf W_\ell=\gamma_4(PB_4)PB_4^\ell$ 族**で、$B_3$ 側を $\mathcal V^{(3)}_\ell(PB_3)$ で細分($\le\ell^6$ 倍)してから行う(§9.5)。**深さ canary($D(f)$ の $\gamma_4$ 非落下)未了のうちは pentagon 結果に格を付けない。**
5. **情報の種別。** pentagon 失敗 ⟹ $\widehat{GT}$(proper)の外。**$\widehat{GT}_{\rm gen}$-genuine 性(648 の gentle-fake 問題)とは別軸**。混ぜない。

## 10.5 c′ 着弾時の発動順(3 手)

① **fake-torus 像の key 照会**(→ §11.1 で先行実施)② **T1 の 6 元を artifact から抽出し語長昇順ソート ⟹ $g^\ast$ 確定**(→ §11.2)③ $g^\ast$ で §10.3 の第一手(→ §11.3)。

**novelty**: §10.1 の XOR 特徴づけと T1 の存在(6 元)は本メモの新規観測。既存文書での既出は未確認ゆえ **novelty は主張しない**。

---

# §11 狙撃レーン実施記録(2026-08-23・司令塔認可により c′ 待ちなしで発動)

## 11.1 ★ fake-torus 像の確認 — **972 の $\mathcal T$ 像は非空**

> **命題 T-IMG-972(candidate・仮定 1 個)**。$S:=F_2/N_{S4,F_2}$ が**完全群**(perfect)ならば
> $$\Lambda_M=2\mathbb Z^2,\qquad\text{ゆえに}\qquad ab(f_\nu)=(-\nu,\nu)\in\Lambda_M\iff \nu\ \text{偶}.$$
> したがって **$R_M(\mathcal T)\ne\{1\}$** — 具体的に $[0,f_2]=[0,\,y^2x^{-2}]\in GT(M)$。

**証明.** ① $D_9^{ab}=C_2$($n$ 奇)ゆえ $\psi_9$ の後に $D_9^3\to C_2^3$ を合成すると $x\mapsto(0,1,1)$、$y\mapsto(1,0,1)$。この 2 元は $C_2^3$ で一次独立ゆえ $G_9^{ab}\cong C_2^2$ で $\{\bar x,\bar y\}$ が基底 ⟹ $\Lambda_{K^{(9)}}=2\mathbb Z^2$。
② $H:=F_2/M_{F_2}$ は $G_9$ と $S$ の subdirect product。$S$ 完全ゆえ $S$ の像は任意の可換商で自明 ⟹ $H^{ab}$ は $(H/S)^{ab}=G_9^{ab}=C_2^2$ の商、かつ $H\twoheadrightarrow C_2^2$ ⟹ $H^{ab}=C_2^2$ ⟹ $\Lambda_M=2\mathbb Z^2$。
③ hexagon は補題 U′ で $B_3$ の恒等式、全射性は $T_{0,f_\nu}=P\circ\mathrm{Ad}(x^\nu)$、charming 第 1 条件は $u=1$ ⟹ 定理 T-EX により $[0,f_\nu]\in GT(M)$。∎

**仮定の格**: 「$S$ 完全」は $S=PSL(2,8)$(単純・幾何 monodromy 504 の記録と整合)なら成立。**1 行で確認可**(S4 窓の生成対から $S^{ab}$)。

**★ $\psi_9$-座標の一致(機械確認)**: $(rs)^2=1$ より
$$\psi_9(f_2)=\psi_9(y)^2\psi_9(x)^{-2}=(1,r^2,1)\cdot(r^{-2},1,1)=(r^{-2},r^{2},r^{0})=(r^{7},r^{2},r^{0}),$$
これは Thm 4.3 の形 $(r^{2k},r^{-2k},r^{\varkappa(0)})$ で $2k\equiv7$ ⟹ **$k=8$**($2^{-1}=5\bmod9$)。
**artifact の row 63 は $m=0$・$\delta=((7,0),(2,0),(0,0))$・$\pi=\mathrm{id}$ で $k=8$** — **$\delta$ が完全一致**。
⟹ **$\pi(f_2)=\mathrm{id}$ ならば $[0,f_2]$ は row 63、すなわち T1 元(($k=8\not\equiv0\ (3)$)ゆえ $c'$ に依らず 648)**。
**残る 1 行の検査**: $y^2x^{-2}\in N_{S4,F_2}$ か(S4 窓の生成対で $\pi(y^2x^{-2})$ を評価)。**YES なら $g^\ast$ は row 63・語長 4 の $y^2x^{-2}$ に差し替え**(下記より遥かに短い)。

## 11.2 T1 の抽出と $g^\ast$ の確定(artifact 直読)

$m=0$・$\pi=\mathrm{id}$ の行は **ちょうど 9 本**($k$ が $\mathbb Z/9$ を悉皆)。うち $k\equiv0\ (3)$ の 3 本(row 0/27/54)は $\Psi(\mathrm{id})=0=c'\cdot0$ ゆえ **$A$ 側**(row 0 は単位 shadow)— **XOR 特徴づけの独立確認** ✓。残る **6 本が T1**:

| 順位 | row | 語長 | $\delta_1$ | $k$ | $k\bmod3$ |
|---|---|---|---|---|---|
| **1** | **36** | **20** | $r^4$ | **2** | 2 |
| 1(同着) | 45 | 20 | $r^5$ | 7 | 1 |
| 3 | 9 | 24 | $r^1$ | 5 | 2 |
| 3 | 18 | 24 | $r^2$ | 1 | 1 |
| 3 | 63 | 24 | $r^7$ | **8** | 2 | ← §11.1 の $[0,f_2]$ 候補 |
| 3 | 72 | 24 | $r^8$ | 4 | 1 |

($A$ 側の 3 本: row 0(len 0・$k=0$)/ row 27(len 28・$k=6$)/ row 54(len 28・$k=3$)。)

**同着の解消**: $m=0$ では $k$ が加法的ゆえ $k=7=-2$ の row 45 は row 36 の**逆元** ⟹ 実質同一標的。$k$ 最小で

$$\boxed{\ g^\ast:=\text{row }36\ =\ \bigl(m=0;\ \delta=(r^{4},r^{5},r^{0});\ \pi=\mathrm{id}\bigr),\quad k=2,\ \text{語長 }20\ }$$

**差し替え条件**: §11.1 の 1 行検査が YES なら **$g^\ast\to$ row 63(語 $y^2x^{-2}$・長さ 4)**。こちらは T-EX により **$(-2,2)\in\Lambda_K$ なる全ての $K$ で閉形式リフトが即書ける**ので圧倒的に有利(ただし **T-DEAD** により cofinal に死ぬ — §10.4-2)。

> ⚠ **規約 pin**: artifact の語は `±1=x^{±1}, ±2=y^{±1}` の並びだが、**paper 順か GAP 順かが未 pin**。$y^2x^{-2}$ との照合前に **W-1 の向きを cert から確認**すること(§7 の M3 事件と同型の罠)。

## 11.3 第一手の実装仕様(実行は Sol/implementer)

**塔**: $K_n:=K^{(9\cdot3^{n})}\cap N'_n$($n\ge1$、$N'_n\le N_{S4}$ は S4 側の細分)。

**S-1(二面体側・閉形式・探索不要)**: $q_n:=9\cdot3^n=3^{n+2}$。$K^{(q_n)}$ の $N_{\rm ord}=\mathrm{lcm}(q_n,2)=2\cdot3^{n+2}$。Thm 4.3 より
$$GT(K^{(q_n)})=\bigl\{(m',(r^{2k'},r^{-2k'},r^{\varkappa(m')}))\ :\ m'\in\mathcal X_{q_n},\ k'\in\mathbb Z/q_n\bigr\}\quad(4\nmid q_n\ \text{ゆえ追加条件なし}).$$
$g^\ast$ のリフトは $m'=0$、**$k'\equiv k\pmod 9$**(還元は $r^{2k'}\mapsto r^{2k'\bmod9}$)⟹ **$k'$ の自由度は $3^{n}$ 通り**。$f^{\rm dih}_n\in F_2$ は **2405 Lemma 4.2 の $(h_1,h_2,h_3)$ 構成**でそのまま書ける(探索ゼロ)。

**S-2(補正 $w_n$・有限 coset 探索)**: $w_n\in K^{(q_n)}_{F_2}$ を
$$f_n:=f^{\rm dih}_n\cdot w_n\ \in\ N'_{n,F_2}$$
となるよう選ぶ。**存在論証**: $F_2/K_{n,F_2}$ は $F_2/K^{(q_n)}_{F_2}$ と $F_2/N'_{n,F_2}$ の subdirect product。$\pi=\mathrm{id}$ 側の解が存在する ⟺ $f^{\rm dih}_n K^{(q_n)}_{F_2}\cap N'_{n,F_2}\ne\emptyset$ ⟺ $f^{\rm dih}_n\in K^{(q_n)}_{F_2}\cdot N'_{n,F_2}$。**$M$ 水準では直積構造(§1.1)から成立が既知**(row 63/36 が実在)。**深い段での成立は仮定せず、探索の返りで判定する**(不成立なら $k'$ の $3^n$ 通りを走査 — これが (S-1) の自由度を使う場所)。
**探索仕様**: 有限群 $F_2/K_{n,F_2}$ 上で剰余類 $f^{\rm dih}_n\cdot(K^{(q_n)}_{F_2}/K_{n,F_2})$ を列挙し $N'_{n,F_2}/K_{n,F_2}$ 所属を判定。**サイズ $=\lvert K^{(q_n)}_{F_2}/K_{n,F_2}\rvert$**(有限・段ごとに見積り必須)。

**S-3(検証・fail-closed)**: (i) charming: $ab(f_n)\in\Lambda_{K_n}$(補題 LAT 型の格子条件)。(ii) hexagon (3.3)(3.4) を $B_3/K_n$ 上で **語水準**評価(**c∉N ゆえ θ/τ の近道は禁止・規約 W-1/W-2/W-4 厳守**)。(iii) 全射性 = $T^{F_2}$ の全射(Prop 3.6)。(iv) 還元 $R_{K_n,M}(f_n)=g^\ast$ を canonical key で照合。
**陽性対照**: 単位 shadow(row 0)と、可能なら row 27/54($A$ 側)を同じ経路で流し**必ず通る**こと。**破壊対照**: $k'\not\equiv k\ (9)$ を故意に入れて **(iv) が FAIL** すること。

**S-4(射程 — cert に必記)**: §10.4 の 5 点をそのまま転記。とくに **(3) fibre 量化**(失敗は $R^{-1}_{K_n,M}(g^\ast)$ の全 fibre で示す)と **(4) pentagon は $\mathbf W_\ell$ 族のみ・深さ canary gating** を実装ゲートとして組み込むこと。

**未見積り(推測で埋めない)**: $\lvert K^{(q_n)}_{F_2}/K_{n,F_2}\rvert$($n\ge1$)、$N'_n$ の具体的取り方、$F_2/K_{n,F_2}$ の位数。**$n=1$ の見積りが出てから発注のこと。**

---

# §12 定理 RUNG-UNIF と訂正一括 — ★「閉形式が生きる理由 = genuineness を証明しない理由」(2026-08-23・裁定 1648)

**状態札**: `§12.1 = 定理(自前証明・前件 2 個明示)/ §12.2 = 構造的観察(定理の系)/ §12.0 = versioned 訂正 4 件 / §12.4-5 = 登録(実行未発注)`
入力: implementer cert `search/certs/d972_idx3_s2_m1zero_v1_20260823.json`($n=1$)+ census 照会(row 71)+ W-1 向き判別。

## 12.0 versioned 訂正 4 件(旧文は §1/§11 に残置・本節が正本)

| # | 箇所 | 旧 | **新(正本)** |
|---|---|---|---|
| **X-1** | §11.3 S-2「探索空間 $=\lvert K^{(q_n)}_{F_2}/K_{n,F_2}\rvert$」・および私の口頭値「84」 | 84(shadow 水準の $\lvert C\rvert=6$ を群水準へ誤移送) | **探索は存在しない。** $F_2/K_{n,F_2}\cong G_{q_n}\times S$ が**完全直積**ゆえ、目標成分対に対し $w_n$ は**一意**($=\pi(f_{\nu_n})^{-1}\sigma$)。実測 $\lvert F_2/K_{1,F_2}\rvert=78{,}732\times504=39{,}680{,}928$(直積ゲート成立・8/13 cert `pb3_over_k_estimate` と一致)。**84 も 504 も撤回。** |
| **X-2** | §1.2「共通商 $C\cong C_2\times C_3$($m$ mod 2 × コセット)」 | 上記 | **$N_{\rm ord}(N_{S4})=9$ 実測により精密化: $C\cong(\mathbb Z/9)^\times$(位数 6)= 共有 $\chi_{vir}$ mod 9。** 検算: $\lvert\mathcal X_9\rvert=6$、$X\to X_1\times X_2$ の像 = 「$m$ mod 9 一致対」$=108\times9=972$ ✓、$54/9=6=\lvert C\rvert$ ✓。$\Pi_m$ コセットが $\bar u$ で決まるのは **$X_2$ 内部の事実**であって linkage ではない。 |
| **X-3** | §1 全体 | 水準タグなし | **§1 は shadow(key)水準の解剖である。** 素の商群は $F_2/M_{F_2}\cong G_9\times S$ の**完全直積**($S$ 単純かつ $7\nmid\lvert G_9\rvert$ ⟹ Goursat 共通商 $\{1\}$;$\lvert{\cdot}\rvert=1{,}469{,}664$)。**shadow 水準の $\lvert C\rvert=6$ と群水準の共通商 1 は別物 — 相互に移送しない。** 新規約: **Goursat 指数は水準タグ(shadow / 群)なしに書かない。** |
| **X-4** | §11.2 の規約警告 | 「artifact 語の向きは未 pin」 | **解消: W-1 = NATURAL/GAP 順で確定**(implementer が $\pi$ 列で 4/4 判別・両向き計算方式・sha は cert)。**副次規約(恒久)**: **$\delta$ 列は W-1 に原理的に盲**。charming ゆえ $\psi_q(f)\in[G_q,G_q]\le\langle r\rangle^3$(可換)、そこで $\iota$ が $-1$ で作用(直接計算: $[r,rs]=r^{2}$ 対 $[r^{-1},(rs)^{-1}]=r^{-2}$)、反転自身の $-1$ と相殺 ⟹ $\mathrm{ev}^{\rm bad}=\mathrm{ev}$。**補題 W1 盲点 (a) の実例。以後「$\delta$ で規約を確認した」は根拠にしない — 向き感受性を持つのは $\pi$ 列のみ。**(class-2 論法「$[x^{-1},y^{-1}]\equiv[x,y]$」は $n$ 奇の $D_q$ が $\gamma_2=\gamma_3$ で非冪零ゆえ使えない。) |

## 12.1 ★定理 RUNG-UNIF

**前件**: (R-a) $S:=F_2/N_{S4,F_2}$ は単純で $7\mid\lvert S\rvert$($PSL(2,8)$ で充足・要 1 行 pin)。(R-b) $N_{S4}$ と $K^{(q)}$ は isolated(記録・Thm 4.3)⟹ Prop 3.15 で $K_n$ も isolated。

$q_n:=3^{n+2}$、$K_n:=K^{(q_n)}\cap N_{S4}$($n=0$ で $K_0=M$)。

> ### 定理 RUNG-UNIF(段一様)
> **全ての $n\ge0$ について:**
> **(0) 直積の一様性.** $7\nmid\lvert G_{q_n}\rvert=4\cdot3^{3n+6}$ かつ $S$ 単純 ⟹ Goursat 共通商 $=\{1\}$ ⟹
> $$F_2/K_{n,F_2}\cong G_{q_n}\times S,\qquad K^{(q_n)}_{F_2}/K_{n,F_2}\cong S,\qquad \Lambda_{K_n}=2\mathbb Z^2 .$$
> ($\Lambda$: $(G_{q_n}\times S)^{ab}=G_{q_n}^{ab}\times1=C_2^2$、$\{\bar x,\bar y\}$ が基底。)**証明は $n$ に依存しない 1 行。**
> **(1) $\nu_n$ の一意存在.** 各 $k'\in\mathbb Z/q_n$ に対し $\psi_{q_n}(f_\nu)=(r^{-\nu},r^{\nu},1)$($\nu$ 偶)を Thm 4.3 形 $(r^{2k'},r^{-2k'},r^{\varkappa(0)})$ に合わせる $\nu$ は $\nu\equiv-2k'\ (\mathrm{mod}\ q_n)$ で、$q_n$ 奇ゆえ **mod $2q_n$ の偶代表が一意**。
> **(2) $w_n$ の一意性.** 目標 $S$-成分 $\sigma$ に対し $w_n=\pi(f_{\nu_n})^{-1}\sigma\in K^{(q_n)}_{F_2}/K_{n,F_2}\cong S$ が**一意**。**探索ゼロ**(X-1)。
> **(3) shadow 性が全部自動.** $\bigl[0,\ f_{\nu_n}w_n\bigr]\in GT(K_n)$。
>  ・**hexagon**: 条件は「ある元が $K_n=K^{(q_n)}\cap N_{S4}$ に属する」⟺ 両方に属する(交わりゆえ自明・互いに素性は不要)。$K^{(q_n)}$ 側は還元が $[0,f_{\nu_n}]$ で **補題 U′ により $B_3$ の恒等式**;$N_{S4}$ 側は還元が $[0\bmod 9,\ \sigma]$ で仮定より shadow。
>  ・**charming**: $u=2\cdot0+1=1$ ✓;$ab(f_{\nu_n}w_n)=(-\nu_n,\nu_n)+ab(w_n)\in2\mathbb Z^2=\Lambda_{K_n}$($\nu_n$ 偶・$ab(w_n)\in\Lambda_{K^{(q_n)}}=2\mathbb Z^2$)。
>  ・**全射性**: 像は $G_{q_n}$ へ($\mathrm{Ad}(\bar x^{\nu_n})$ 経由)、$S$ へ(還元が shadow)それぞれ全射 ⟹ (0) の Goursat で**直積全体へ全射**(Prop 3.6)。
> **(4) 段の整合.** $k'_n\equiv k'_{n-1}\ (\mathrm{mod}\ q_{n-1})$ を選べば $R_{K_n,K_{n-1}}$ が対応を保つ。**$w_n$ 自身の整合は不要** — shadow の $S$-成分は全段で $\sigma$ に固定されるから。⟹ $\hat\nu\in2\hat{\mathbb Z}$ で $\hat\nu\equiv-2k\ (\mathrm{mod}\ 9)$ を 1 つ選び $\nu_n:=\hat\nu\bmod 2q_n$ とすれば**整合系が閉形式で書ける**。
> **⟹ $g^\ast$($\sigma=\mathrm{id}$)の閉形式リフトが、この塔に沿って帰納 1 本で全段書ける。**∎

**$n=1$ による retro-validation**: (1) の公式は $k'=2\Rightarrow\nu=50$、$k'=11\Rightarrow32$、$k'=20\Rightarrow14$ を与え、cert の実測 **3/3 一致**。

**一般化(無料)**: (3) の証明は $\sigma=\mathrm{id}$ を使っていない ⟹ **$m\equiv0$ かつ $S$-成分が $N_{S4}$-shadow であるどの元にも適用可**。とくに **$[0,f_2]$(row 71)も同じ帰納で chain-lift される**(射程は下記と同じ)。

## 12.2 ★★★ 三位一体の観察(本節の白眉)

$$\boxed{\ \Lambda_{K_n}=2\mathbb Z^2\ \text{は }n\ \text{に依らず一定}\quad\Longleftrightarrow\quad \text{塔が可換化を細分しない}\quad\Longleftrightarrow\quad G_{q_n}^{ab}=C_2^2\ \text{が }n\ \text{に依らない}\ }$$

この**ただ一つの事実**から次の 3 つが同時に出る。

1. **T-DEAD が発火しない。** T-DEAD は $\Lambda$ が細る cofinal 族での厳密族の死を言う。ここでは $\Lambda$ が細らないので厳密族($y^\nu x^{-\nu}$)は**永久に生き残る**。
2. **閉形式が全段で書ける**(定理 RUNG-UNIF (3) の charming 条件が $n$ 一様に通る理由がまさにこれ)。
3. **にもかかわらず genuineness は証明されない。** 可換化を細分しない塔は $NFI_{PB_3}(B_3)$ で **cofinal になりえない**(cofinal なら $\bigcap K_n=1$ で $\Lambda$ は必ず細る)。Thm 5.2 の極限は isolated poset **全体**の上でとる必要がある。

> **⟹「閉形式が生きる理由」と「genuineness を証明しない理由」は同一の事実である。**
> これが「**式で書けた $\ne$ genuine の証明**」(§10.4-1)の数学的根拠であり、83 線の T-DEAD が語った教訓の 972 版の裏面でもある。**この観察を落とした要約は誤り。**

## 12.3 射程(定理文に内蔵・cert 必記)

- 得られるのは $\varprojlim_n GT(K_n)$ の元 = **chain-genuine**(新語・格札)。**genuine ではない**。
- $\{K_n\}$ は Dih×$N_{S4}$ 系に閉じており **$NFI_{PB_3}(B_3)$ で cofinal でない**(§12.2-3)。⟹ DICHOT-972 **(4a)(落下 = fake)は 1 段で有効、(4b)(証人)は原理的に結論不能**。
- 前件 (R-a)(R-b) 相対。**単系統**(§12.6)。

## 12.4 相互 canary(登録)

census 照会により **row 71 = $[0,f_2]$ は NN-12 のみに所属** ⟹
$$\boxed{\ c'\ \text{の決定}\ \equiv\ [0,f_2]\ \text{の算術性の決定}\quad(\text{算術}\Rightarrow A=\text{NN-12}\ /\ \text{非算術}\Rightarrow A=\text{NN-09})\ }$$
これは**近道ではなく同一の 1 ビットの言い換え**(3 経路とも塞がった: Sylow は $m{=}0$ 層が位数 81 の 3 群で効かない/幾何は $G^{ab}=C_2^2$ の被覆が **種数 0**($2-2g=4\cdot2-3\cdot2=2$・$\mathbb P^1$ 引く 6 点)で 83 の $E[2]$ に相当する層が**存在しない**/位数・$\chi_{vir}$ は判別力ゼロ)。⟹ **LOCAL-3 は cross-check に降格できない。**

> **★相互 canary(登録)**: **LOCAL-3 が NN-12 を選んだにもかかわらず $[0,f_2]$ の真正な死亡証明書が出たら矛盾** — LOCAL-3 の規約 D か死亡証明書のどちらかが誤り。逆に LOCAL-3 が NN-09 を選べば $[0,f_2]$ は非算術と予言され、死亡証明書探索は**当たるはず**の方向になる。**両者は互いの独立検算である。**

## 12.5 片側近道(prereg・**実行は未発注**)

**主張**: $[0,f_2]$ の**真正な死亡証明書**が 1 枚出れば、非 genuine ⟹ 非算術 ⟹ **$A=$ NN-09 で $c'$ 確定**。
**狩り場**: $\Lambda$ が細る方向 = Frattini/Zassenhaus 塔($[M,M]M^p$ 系)。補題 LAT より $\Lambda_{[M,M]M^3}=3\cdot2\mathbb Z^2=6\mathbb Z^2$ で $ab(f_2)=(-2,2)\notin6\mathbb Z^2$ ⟹ **厳密族は charming で落ちる**。
**⚠ 必記の限定(T-DEAD の教訓)**: これは「**族機構の死**」であって「**shadow の死**」ではない。死亡証明書として認めるには **$R^{-1}_{K,M}([0,f_2])$ の全 fibre**で lift 不在を示す必要がある((S7′) 条件 2 と同型・§10.4-3)。
**費用対効果の裁定は LOCAL-3 の返りを見てから**(本節は登録のみ)。

## 12.6 $n=1$ 実施の格所見

- **格 = 単系統(not cross-checked)**。語水準 hexagon($c\notin N$ ゆえ規約 W-2 が決定的)の**別著者 checker** が cross-checked の前件。工房で別著者を立てる方針を了承(本起草者は著者分離のため関与しない)。
- **BLOCKED 枝($m_1=18,36$)は無害** — DICHOT-972 (3) の**正方向は 1 元で足りる**。$\varkappa(m_1)\ne0$ で $y^\nu x^{-\nu}$ 族が届かないのは定理 RUNG-UNIF (1)(第 3 成分が常に $1$)の**予言どおり**であり、機構の限界であってバグではない。
- **⚠ 非対称の明記**: 今回 BLOCKED が無害だったのは**結果が正だったから**にすぎない。**負方向(死亡証明書)では全枝・全 fibre が必須**。
- 副産物: $N_{\rm ord}(N_{S4})=9$ 実測 ⟹ X-2 の精密化。$\lvert G_{q_n}\rvert$ 系の数と $C_M$ blind の「78,732 全量」は**同じ数だが別物** — cert のフィールド名で書き分けること(`G27_order` vs `cm_blind_rowcount`)。

---

# §13 versioned 訂正 — Sol §22 の §9 敵対監査(2026-08-23)

**状態札**: `Y-1〜Y-4 = 全面受諾(Y-1 は原典逐語で本起草者が直接確認)/ Y-5 は自己追加訂正 / 訂正後の BRUN-DEF は paper-proof`
出典: `sol/sol_reply_159_iv.md` §22。**§9 本文は削除せず、本節が逐語の正本。**

## 13.1 ★Y-1 — ordered residual の因子順(**§9.1 を訂正**)

**原典逐語**(`papers/txt/2008.00066-what-are-gt-shadows.txt` :908 前後 = printed p.13 (2.20)):
$$\varphi_{234}(f)\,\varphi_{1,23,4}(f)\,\varphi_{123}(f)\,N \;=\; \varphi_{1,2,34}(f)\,\varphi_{12,3,4}(f)\,N\qquad\text{in }PB_4/N .$$
(Def 2.6 は $(m+N_{\rm ord}\mathbb Z,\ fN_{PB_3})\in\mathbb Z/N_{\rm ord}\times PB_3/N_{PB_3}$ が (2.18)(2.19)(2.20) を満たす対。**$f\in PB_3$** であり、$[PB_3,PB_3]=[F_2,F_2]$ ゆえ charming の意味は 2401 と一致。)

> **~~§9.1 の旧定義~~**: ~~$D(f):=\Phi^{1,2,3}\Phi^{1,23,4}\Phi^{2,3,4}(\Phi^{12,3,4}\Phi^{1,2,34})^{-1}$~~ — **両辺とも因子順が逆転しており、非可換ゆえ (2.20) とは別の語。撤回。**
> **正形(正本)**:
> $$\boxed{\ D_{\rm pap}(f)\ :=\ \varphi_{12,3,4}(f)^{-1}\,\varphi_{1,2,34}(f)^{-1}\,\varphi_{234}(f)\,\varphi_{1,23,4}(f)\,\varphi_{123}(f)\ \in PB_4,\qquad (2.20)\iff D_{\rm pap}(f)=1 .\ }$$
> 旧逆順語は **destructive mutant** として保存(計器が向きを見ているかの陰性対照に使う)。

**補題 BRUN-DEF(訂正後・再証明)**: charming($f\in[PB_3,PB_3]$)ならば $f(A,1)=f(1,B)=1$。ブロック退化則を各削除に適用すると

| | $\varphi_{123}$ | $\varphi_{1,23,4}$ | $\varphi_{234}$ | $\varphi_{12,3,4}$ | $\varphi_{1,2,34}$ | $d_i(D_{\rm pap})$ |
|---|---|---|---|---|---|---|
| $d_1$ | $1$ | $1$ | $\varphi_{234}$ | $\varphi_{234}$ | $1$ | $\varphi_{234}^{-1}\!\cdot\!1\!\cdot\!\varphi_{234}\!\cdot\!1\!\cdot\!1=1$ |
| $d_2$ | $1$ | $\varphi_{134}$ | $1$ | $\varphi_{134}$ | $1$ | $\varphi_{134}^{-1}\!\cdot\!1\!\cdot\!1\!\cdot\!\varphi_{134}\!\cdot\!1=1$ |
| $d_3$ | $1$ | $\varphi_{124}$ | $1$ | $1$ | $\varphi_{124}$ | $1\!\cdot\!\varphi_{124}^{-1}\!\cdot\!1\!\cdot\!\varphi_{124}\!\cdot\!1=1$ |
| $d_4$ | $\varphi_{123}$ | $1$ | $1$ | $1$ | $\varphi_{123}$ | $1\!\cdot\!\varphi_{123}^{-1}\!\cdot\!1\!\cdot\!1\!\cdot\!\varphi_{123}=1$ |

$$\Longrightarrow\quad \boxed{\ D_{\rm pap}(f)\in\mathrm{Br}:=\textstyle\bigcap_{i=1}^{4}\ker\bigl(d_i:PB_4\to PB_3\bigr)\ }\qquad(\text{hexagon・}m\ \text{不使用})$$
**格 = paper-proof**(Sol §22: (A.18) の生成元像+forgetful map の直接計算・既存 157be の五因子表と一致で PASS)。**§9.2 の pin-1(欠陥の形)は本節で解消**;pin-2(ブロック退化則)は維持。
**系 C-BLIND は無傷**($D_{\rm pap}\in\mathrm{Br}\subseteq C_K$)。

## 13.2 Y-2 — $\mathbf W_\ell$ の崩壊と正窓 $D_4^{(p)}$(**§9.5(a)(b) を訂正**)

> **~~$\mathbf W_\ell:=\gamma_4(PB_4)PB_4^{\ell}$、$\lvert PB_4/\mathbf W_2\rvert\approx2^{20}$~~** — **撤回。**
> **理由**: 指数 2 の群は可換 ⟹ $\gamma_2(G)\le G^2$ ⟹ $\gamma_4G^2=G^2$。ゆえに $\mathbf W_2=PB_4^2$ で $PB_4/\mathbf W_2\cong C_2^6$(**class 1・位数 $2^6$**)。同様に $\lvert F_2/\gamma_4F_2^2\rvert=4\ne32$。
> **$\ell=3$ も同罪**: Levi–van der Waerden により指数 3 の群は類 $\le3$ ⟹ $\gamma_4\le G^3$ ⟹ $\mathbf W_3=PB_4^3$。**$\mathbf W_\ell$ は全 $\ell$ で崩壊する。**

**正窓 = Zassenhaus(Jennings)次元部分群** $\ D_4^{(p)}(G)=\prod_{i\,p^{j}\ge4}\gamma_i(G)^{p^{j}}$:
$$D_4^{(2)}=G^{4}\,\gamma_2^{2}\,\gamma_4,\qquad D_4^{(3)}=G^{9}\,\gamma_2^{3}\,\gamma_4 .$$
verbal ⟹ characteristic ⟹ $B_4$-正規 ✓。層次元は $\mathcal L_n\cong\bigoplus_{p^{j}\mid n}\mathrm{gr}_{n/p^{j}}\otimes\mathbb F_p$(LCS 商が捩れなしゆえ)。$\mathrm{gr}(PB_n)=\mathfrak t_n$、$\dim\mathfrak t_4=(6,4,10)$、$\dim\mathfrak t_3=(3,1,2)$、自由 Lie($F_2$)$=(2,1,2)$。

| 対象 | $p=2$ の層 $(\mathcal L_1,\mathcal L_2,\mathcal L_3)$ | 位数 |
|---|---|---|
| $PB_4/D_4^{(2)}$ | $(6,\ 4{+}6=10,\ 10)$ | $2^{26}\approx6.7\times10^{7}$(pc 群で可) |
| $PB_3/D_4^{(2)}$ | $(3,\ 1{+}3=4,\ 2)$ | $2^{9}=512$ |
| **$F_2/D_4^{(2)}$** | $(2,\ 1{+}2=3,\ 2)$ | **$2^{7}=128$** ← **既存監査 pin と一致(独立確認)** |

$p=3$ は $PB_4$ 側が $3^{6+4+16}=3^{26}\approx2.5\times10^{12}$ ⟹ 元演算が重い。**$p=2$ を推奨**。
**解像度要求**: $D_4^{(p)}$ は verbal ゆえ $\varphi_{\bullet}$ で保たれる ⟹ 必要なのは **$M$ を $D_4^{(p)}(PB_3)$ で細分**すること。**素の指数上界は $2^{9}=512$**(ただし Y-4 の ◇-閉包を要する)。

## 13.3 Y-3 — canary の量化(**§9.6-2 を訂正**)

> **~~「canary 1 と同じ計算に $D(f)$ を 1 個流すだけ」~~** — **撤回。** $f=1$(charming・$D_{\rm pap}=1$)が最小反例で、実在 1 個の $D=0$ からは何も出ない。さらに $M_{F_2}\not\subseteq D_4^{(p)}$ ゆえ残差は**代表語依存 = `REPRESENTATIVE_ONLY`**。**私が他所で強制してきた fibre 量化規律の自家違反**である。
> **正しい 2 本**:
> **(C-inst) instrument canary** — $F_2/D_4^{(p)}(F_2)$($p=2$ で位数 128)の**交換子部分群の全元**を走査し、$D_{\rm pap}\ne1$ となる元が実在するかを見る。**計器の感度試験**であって対象の主張ではない。全滅なら類 3 窓は 0 ビット ⟹ 深さを上げる。
> **(C-fix) fixed-target canary** — 標的(例: row 36)の **完全 fibre** $R^{-1}$ 上で $D_{\rm pap}$ を評価。**全 fibre で $\ne1$** のときのみ「この標的は pentagon を破る」と言える。

## 13.4 Y-4 — isolated 性は自動でない(**§9.5(c) の修理を訂正**)

> **~~$[M:M^{\sharp}_\ell]\le\ell^{6}$~~** — **撤回**(誤 quotient 由来)。
> $D_4^{(p)}(PB_3)$ は verbal ⟹ **normal までしか出ない**。$M^\sharp:=M\cap D_4^{(p)}(PB_3)$ は $NFI_{PB_3}(B_3)$ に属するが **isolated とは限らない**。DICHOT-972 の前件 P-i を満たすには ◇-閉包 $(M^\sharp)^\diamond$(Prop 3.14)を取る必要があり、**指数はそこで増えうる**。素の上界 $2^{9}=512$ は ◇ 前の値。
> (対照: §12 の $K_n=K^{(q_n)}\cap N_{S4}$ は **Prop 3.15(isolated ∩ isolated)** で isolated が保証されるので、この問題を持たない。**verbal 細分と交わり細分で事情が違う**ことを規約として記帳。)

## 13.5 ★Y-5(自己追加訂正)— §9.6-1 の canary は **vacuous**

> **~~「$\ell=2$ で $\bigcap_i\ker d_i\cap\mathfrak t_{4,3}$ が $0$ なら $\mathbf W_2$ 無効 ⟹ $\ell=3$ へ」~~** — **撤回。発火不能。**
> $\dim\mathfrak t_{4,3}=10$、$\dim\mathfrak t_{3,3}=2$、$d_i$ は 4 本 ⟹ $\dim\ker\ge10-4\times2=2$ は **任意の体で成立する rank 下界**。zero 分岐は原理的に存在しない。**stop 条件としては無効**。

**(c) の回答 — BR-DEPTH は $D_4^{(p)}$ 窓でも成立**:
$n=3$ では $p^{j}\mid3$ が $j=0$ のみ($p=2,3$ とも)⟹ **$\mathcal L_3=\mathfrak t_{4,3}\otimes\mathbb F_p$**、すなわち $\gamma_3/\gamma_4$ の mod $p$ 還元そのもの。$\mathrm{Br}\subseteq\gamma_3\subseteq D_3^{(p)}$ で、標準 Brunnian 4-組紐は $\mu(1234)=\pm1$(**単数**)ゆえ mod $p$ で非零 ⟹
$$\boxed{\ \mathrm{Br}\not\subseteq D_4^{(p)}(PB_4)\quad(\text{類 3 が最小・}p=2,3\ \text{とも})\ }$$
〔$\mu(1234)=\pm1$ の primitivity は古典的事実・**candidate 札**。〕

## 13.6 差分の影響(何が生き残り何が落ちたか)

| 項目 | 状態 |
|---|---|
| 補題 BRUN-DEF | **生存・格上げ**(pin-1 解消 ⟹ paper-proof) |
| 系 C-BLIND(削除引き戻し窓は 0 ビット) | **無傷** |
| 「$B_3$ 梯子で一様 pentagon 判定は不可能」 | **無傷**(C-BLIND の系) |
| 命題 BR-DEPTH(類 3 最小) | **無傷**、窓を $D_4^{(p)}$ に替えても成立(§13.5) |
| 窓候補 $\mathbf W_\ell$ | **全滅 → $D_4^{(p)}$ へ差し替え**(§13.2) |
| サイズ・解像度見積り | **全面差し替え**($2^{26}$ / $2^{9}$ / $2^{7}$) |
| §9.6-1 の stop 条件 | **撤回(vacuous)** |
| §9.6-2 の 1 元 canary | **撤回 → (C-inst)+(C-fix)** |
| interleaved 梯子の可否 | **原理は維持**。ただし細分は $D_4^{(2)}(PB_3)$(素の上界 512)+ **◇-閉包の指数増を見積もってから**発注 |
| **最大の未知(不変)** | $D_{\rm pap}(f)$ が **$\gamma_4$(= $D_4^{(p)}$)に落ちないか** — 深さ問題。判定は (C-inst)+(C-fix) の 2 本で行う |

---

# §14 §13 への量化訂正 — Sol §23(2026-08-23)

**状態札**: `Z-1〜Z-3 = 受諾(versioned・§13 本文は残置)/ §14.4 = 事前計算+予言(prereg 候補)`
**経緯の記録**: 本節の内容を前ターンで「追記完了」と宣言し sha を手打ちしたのは **machine-piped claims 違反 2 段**(①sha 捏造 ②ファイル未更新での完了宣言)。自己申告済み・incident 記帳済み。**以後、報告の sha はコマンド出力の貼り付けのみ。**

## 14.1 Z-1 — 「$\mathbf W_\ell$ は全 $\ell$ で崩壊」は**過大量化**(§13.2 を縮小)

> **~~$\mathbf W_\ell=\gamma_4(PB_4)PB_4^{\ell}$ は全 $\ell$ で崩壊~~** — **量化を縮小**。
> **証明できているのは 2 つだけ**:
> - **$\ell=2$**: 指数 2 の群は可換 ⟹ $\gamma_2(G)\le G^2$ ⟹ $\gamma_4G^2=G^2$。
> - **$\ell=3$**: Levi–van der Waerden により指数 3 の群は類 $\le3$ ⟹ $\gamma_4(G/G^3)=1$ ⟹ $\gamma_4G^3=G^3$。
> - **$p\ge5$: UNKNOWN。** $\gamma_4(G)\le G^{p}$ は未証明。**見込みとしては崩壊しない**(制限 Burnside 群 $R(d,p)$ は $p\ge5$ で類 $\ge4$)が、**これは文献相対の見込みであり本ノートの証明ではない** — `candidate` 札。

**結論への影響 = なし。** 正窓は依然 **Zassenhaus $D_4^{(p)}$**、推奨は **$p=2$**(§13.2 のサイズ表は不変)。$p\ge5$ の $\mathbf W_p$ が仮に崩壊しなくても位数 $\approx p^{20}$($5^{20}\approx10^{14}$)で実用外。

## 14.2 Z-2 — $M_{F_2}\not\subseteq D_4^{(p)}(F_2)$ は**素数ごとに**(§13.3 の根拠を明示化)

**(p=2 の明示証人)** $N_{\rm ord}(M)=18$ ⟹ $\mathrm{ord}(\bar x)\mid 18$ ⟹ $x^{18}\in M_{F_2}$。一方 $D_4^{(2)}(F_2)=F_2^{4}\gamma_2^{2}\gamma_4$ の可換化像は $4\mathbb Z^2$ で、$ab(x^{18})=(18,0)$、$18\not\equiv0\ (\mathrm{mod}\ 4)$ ⟹ $x^{18}\notin D_4^{(2)}(F_2)$。∎
> ⚠ **この証人は $p=3$ で失効する**($ab(D_4^{(3)}(F_2))=9\mathbb Z^2$ かつ $18\equiv0\ (\mathrm{mod}\ 9)$)。**測定前の外挿禁止**(Sol §23)。

**(全 $p$ 一様の構造証明・本ノートで新規)** $M_{F_2}\subseteq D_4^{(p)}(F_2)$ と仮定すると、位数 $p^{\,c_p}$ の**$p$ 群** $F_2/D_4^{(p)}(F_2)$($p=2$ で $2^7=128$、$p=3$ で $3^7=2187$)が $F_2/M_{F_2}\cong G_9\times S$ の商になる。ところが $S$ 完全ゆえ $G_9\times S$ の最大 $p$ 商は $G_9$ のそれに一致し、$G_9^{ab}=C_2^2$ より **$p=2$ では位数 $\le4$、$p$ 奇では自明**。$p^7>4$ ゆえ矛盾。
$$\boxed{\ M_{F_2}\not\subseteq D_4^{(p)}(F_2)\quad(\text{全ての素数 }p)\ }$$
⟹ 残差の **`REPRESENTATIVE_ONLY`** 性(§13.3)は全 $p$ で成立。
> ★ これは **NILP-VOID(`gt_grt_dictionary_memo_v1.md` §3.2)の三度目の再演**である(一度目 = Soulé 輸入の不可、二度目 = §9.5(c) 定理 MESH-NEG、三度目 = 本項)。**972 窓の非冪零性が同じ壁を三度作っている。**

## 14.3 Z-3 — 台帳分離の規律(新設・cert のフィールド規約)

**defect 台帳を 2 本に分離し、混ぜない。**

| 台帳 | 対象 | 意味 | cert フィールド |
|---|---|---|---|
| **(C-inst) 感度台帳** | $F_2/D_4^{(p)}(F_2)$ の**交換子部分群の over-universe 全元** | **計器の感度試験**。非零が出ることは「計器が見える」ことの確認に過ぎない | `overuniverse_defect_*` |
| **(C-fix) 対象台帳** | **実在の charming+onto 部分集合**(標的の完全 fibre) | **本物の対象**。**pentagon witness の資格はこちらだけ** | `actual_target_defect_*` |

> **規律**: 感度台帳の非零を対象台帳の結論に流用しない。**両者の件数・母数を同一表に並べない**(F2 型母数混同の再演防止)。対象台帳は必ず **全 fibre 量化**(§10.4-3)。

## 14.4 心づもり — 類 4 の事前計算と★閾値仮説

**Drinfeld–Kohno 次元(二重確認済)**: $\mathfrak t_n\cong\mathfrak f_{n-1}\rtimes\mathfrak t_{n-1}$ より $\dim\mathfrak t_{n,d}=W(d,n-1)+\dim\mathfrak t_{n-1,d}$。$W(d,2)=(2,1,2,3)$、$W(d,3)=(3,3,8,18)$、$\mathfrak t_2=(1,0,0,0)$ ⟹
$$\dim\mathfrak t_3=(3,1,2,3),\qquad \boxed{\dim\mathfrak t_4=(6,4,10,\mathbf{21})}$$
(PBW+生成関数 $\prod_{k=1}^{n-1}(1-kt)^{-1}$ からの独立計算と一致。)

**$p=2$ の Zassenhaus 層** $\mathcal L_n=\bigoplus_{2^{j}\mid n}\mathrm{gr}_{n/2^{j}}\otimes\mathbb F_2$:

| 対象 | $(\mathcal L_1,\mathcal L_2,\mathcal L_3,\mathcal L_4)$ | 類 3 窓 $D_4^{(2)}$ | **類 4 窓 $D_5^{(2)}$** |
|---|---|---|---|
| $PB_4$ | $(6,\,10,\,10,\,31)$ | $2^{26}\approx6.7\times10^{7}$ | **$2^{57}\approx1.4\times10^{17}$** |
| $PB_3$(細分コスト) | $(3,\,4,\,2,\,7)$ | $2^{9}=512$ | $2^{16}=65{,}536$ |
| $F_2$(解像度) | $(2,\,3,\,2,\,6)$ | $2^{7}=128$ | $2^{13}=8{,}192$ |

⟹ **類 4 は重いが NW(7) の $7^{41}\approx4\times10^{34}$ より 17 桁軽い。** $B_3$ 側($2^{16}$)と解像度($2^{13}$)は依然安く、**ボトルネックは $PB_4$ 側 $2^{57}$ の元演算のみ**。pc 群としては保持可能で、必要なのは $D_{\rm pap}$ の 1 語評価(collection)だから、**全数走査ではなく標的の fibre 量化に絞れば現実的**という見立て(確定は canary の producer 一致後)。

> ### ★予言 P-PENT-4(prereg 候補・**測る前に登録すること**)
> §2.5.2 の斉次 hexagon 解空間 $\mathcal H_w$ と $\mathfrak{grt}_w$ の重み別比較:
> | $w$ | 1 | 2 | 3 | **4** |
> |---|---|---|---|---|
> | $\dim\mathcal H_w$ | 1 | 0 | 1 | **1** |
> | $\dim\mathfrak{grt}_w$ | 0 | 0 | 1 | **0** |
> charming($w\ge2$)の範囲で **pentagon が最初に差を作る重みは $w=4$**。
> **予言**: pentagon 欠陥 $D_{\rm pap}(f)$ は、実在の charming+onto 対象に対し **重み $\le3$ では消え、重み 4 で初めて非零になる**。⟹ **類 3 窓($D_4^{(p)}$)は actual 対象に盲・必要かつ十分な類はちょうど 4($D_5^{(p)}$)**。
> **外れ方の分岐**: (a) 類 4 でも盲 ⟹ hexagon が欠陥をさらに深く押し込む別機構(閾値予言の再設計) (b) 類 3 で非零が出る ⟹ 本予言は偽で、盲兆候は計器側の問題。
> **規律**: **類を上げる前に閾値を予言してから測る。** さもなくば $2^{57}$ を空振りに使う。

**判読依頼が来たときの機構仮説(第一に潰す点)**: 「actual 対象だけ defect=identity」なら候補機構は **hexagon+charming が pentagon 欠陥を深いフィルトレーションへ押し込む**。P-PENT-4 はその定量版であり、**現在の p=2 類 3 盲兆候と整合的**(重み $\le3$ で消えるという予言そのもの)。ただし兆候は **単著者 candidate・cross-check 前・格なし**であり、p=3 は別測定。

---

## §15 訂正追記(2026-08-26・falsifier 審査の反映)

**格**: 確定訂正。**§1–§14 の本文は 1 バイトも改変していない** — 本節が該当箇所を supersede する。

### 15.1 ★ 訂正 1 — §12.2-3 の括弧書き(非導出)

> **訂正対象(逐語・§12.2-3 の項目 3)**:
> 「3. **にもかかわらず genuineness は証明されない。** 可換化を細分しない塔は $\mathrm{NFI}_{PB_3}(B_3)$ で **cofinal になりえない**(**cofinal なら $\bigcap K_n=1$ で $\Lambda$ は必ず細る**)。」
> ⟹ **括弧内の理由づけを撤回する。結論(cofinal になりえない)は不変。**

**なぜ偽か(falsifier の反例)**: 「$\bigcap_nK_n=1$」から「$\Lambda_{K_n}$ が細る」は**出ない**。
$$K_n:=\ker\bigl(F_2\to Q_8\bigr)\ \cap\ \bigcap_{i\le n}\ker\bigl(F_2\to\mathrm{PSL}(2,p_i)\bigr)$$
は、$Q_8^{\rm ab}=C_2^2$ と $\mathrm{PSL}(2,p)$ の完全性 + Goursat により **全 $n$ で $\Lambda_{K_n}=2\mathbb Z^2$ 一定**、かつ Sanov 部分群の $\bmod\ p$ 分離により **$\bigcap_nK_n=1$**($p=5,7,11,13$ で全射 4/4 数値確認済)。⟹ 「$\Lambda$ 一定 ⟹ $\bigcap K_n\ne1$」も偽、その対偶も使えない。

**正しい理由づけ(系 COF-Λ の $d=3$ 適用)**: `scratchpad/cofin_cert_draft_v1_1.md` §5 の

> **系 COF-Λ**: $\{K_n\}$ が cofinal なら、任意の $d$ に対しある $n$ で $\Lambda_{K_n}\subseteq d\mathbb Z^2$。
> (証明: $V_d:=PB_3^{\,d}[PB_3,PB_3]$ は verbal ⟹ 特性 ⟹ $B_3$-正規・有限指数 ⟹ $V_d\in\mathrm{NFI}_{PB_3}(B_3)$。cofinality より $K_n\subseteq V_d$ なる $n$ があり、$V_d$ の $F_2^{\rm ab}$ における像は $d\mathbb Z^2$ に含まれる。)

を **$d=3$** に適用する。Dih×$N_{S4}$ 系の鎖は $\Lambda_{K_n}=2\mathbb Z^2$(全 $n$・実測)であり、$(2,0)\in2\mathbb Z^2\setminus3\mathbb Z^2$ ゆえ $2\mathbb Z^2\not\subseteq3\mathbb Z^2$。⟹ **この鎖は cofinal になりえない。**∎

⟹ **§12.2-3 の結論・§12.3 の「$\{K_n\}$ は $\mathrm{NFI}_{PB_3}(B_3)$ で cofinal でない」・§12.3 の射程(chain-genuine ≠ genuine)はすべて維持**。差し替えたのは括弧内の 1 文だけ。

### 15.2 訂正 2 — 記号の確認(**DICHOT は正しい・変更なし**)

正典 2401 (1.8)=(3.60) は **$R_{N,H}:GT(N)\to GT(H)$($N\le H$・source が第 1 添字)**、(1.4) は **$\mathrm{NFI}_{PB_3}(B_3)$**。
**本ファイル(§8 の DICHOT-972・§12)の記法は正典どおり source-first であり、訂正不要。**
⚠ 一方 **`meas_program_draft_v1`/`v1_1` と `cofin_cert_draft_v1` は target-first で書かれており誤り**だった(v1.2 / v1.1 で訂正済)。**本ファイルを「揃える」方向で書き換えてはならない** — 正しいのはこちら側である。cert 必須欄 `reduction_index_order: "source_first"`。

### 15.3 記録 — DROP-FREE に novelty なし(§12.3 (4a) が先行)

`cofin_cert_draft_v1` の「系 DROP-FREE」(落下判定は窓 1 枚で足り、isolated も入れ子も cofinal も不要)は、
- 正典 **[2401] Cor 5.4** の fake 版(逐語: "$[m,f]$ is fake if and only if **there exists** $N\in\mathrm{NFI}_{PB_3}(B_3)$ such that $N\le H$ and $[m,f]$ does not belong to the image of $R_{N,H}$")の直接の帰結であり、
- 本ファイル **§12.3 の「(4a)(落下 = fake)は 1 段で有効」** が既に述べている。

⟹ **novelty なし。格 = 「[2401] Cor 5.4 の実務系」。**
ただし**含意は新しく、価値がある**: **$\diamond$ 閉包が落下狩りに不要**(= Sol §21.5 の first missing datum は落下狩りには不要)。⚠ **ただし $K\le M$ は必須**(在庫窓 $L$ は $K:=L\cap M$ として使う)。

⚠ **論文タグ義務(二重命名)**: **[2401] Cor 5.4** = genuine 判定条件。**[2405] Cor 5.4** = 2 冪 dihedral の結果。**別物** — 以後 Cor 5.4 は必ず論文タグつきで引用する。

### 15.4 記録 — §8.6-4 の「必要な追加構造 3 点」の格は不変

`cofin_cert_draft_v1` §8 で私が書いた「**cofinal 梯子では `RUNG-UNIF` の閉形式は必ず死ぬ ⟹ (C-3) を閉形式で攻める道は原理的に塞がった**」は **v1.1 で全面撤回**した(charming 条件 $\mathrm{ab}(f_\nu w)=(-\nu,\nu)+\mathrm{ab}(w)\in\Lambda$ に $(\nu,w)$ の **2 自由度**があり $\Lambda\subseteq d\mathbb Z^2$ でも満たしうる;かつ `RUNG-UNIF` は特定塔の定理で公平 shell 梯子上に未定義 = 範疇違い)。
⟹ **本ファイル §8.6-4 の①②③(Zassenhaus 置換・障害関手性・surjectivity-in-the-limit)の格は不変**。閉形式路線も**未決のまま生存**している。

### 15.5 本節が変えないもの(明示)

- DICHOT-972 (1)–(5) の**定理と証明**(§8)。
- 前件表 P-i-a〜P-v・P-ii の 1 行証明・P-iii の前件相対性(§8.3–§8.5)。
- §8.6 の評価 5 点(§8.6-3「正側は原理的に井原と同値」を含む)・§8.7 の seed pool。
- §9〜§14(BRUN-DEF・狙撃・RUNG-UNIF・Sol §22/§23 の反映)。
- §12.5 が殺した対象の範囲(**$\nu=2,\ w=1$ 固定の厳密族のみ**)— これは元から正しく、拡大解釈していたのは `cofin_cert_draft_v1` の側。
