# [Q3-R1] mod $691^2$ リフトの構成仕様(実装係へ直結)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔(実装係の確認への回答)
入力 = witness(cert `s2_3_pre_gen23_v1`)$a,b\in SL^\pm(2,\mathbf F_{691})$ / 前提 = `F_stage2_completion_v1.md`・`iso_family_lemma_v1.md`
⚠ $u$/$c$ 非接触・prereg 非抵触(純群論)。**格: candidate**。

---

## §0 ★★★ 先に訂正 1 点(仕様の前提)

> ⚠ **$PB_3/N'$ の生成元は $\sigma_i$ ではなく $\sigma_i^{\,2}$ です。**

定義ノート L163: **$x=\sigma_1^2$, $y=\sigma_2^2$** が $F_2$ を生成。$\sigma_i$ 自身は $\det=-1$ で **$SL$ の外**($SL^\pm\setminus SL$)にあります。
$$\boxed{\ \bar x=\sigma_1^{\,2},\quad \bar y=\sigma_2^{\,2}\quad(\det=1\ \Longrightarrow\ SL(2,\mathbf Z/691^2)=PB_3/N'\ \text{の中})\ }$$
⟹ ★ [Q3-R1] の前フィルタ($\bar x^u\sim\bar x$)は**この $\bar x,\bar y$** に対して行ってください。

---

## §1 手順 1 — $\det$ 調整つきリフト(正確な式)

$\hat a,\hat b\in M_2(\mathbf Z/691^2)$ を witness の**素朴な代表**(成分を $0..690$ のまま $\mathbf Z/691^2$ で読む)とする。

$$\boxed{\ \lambda_a:=-\bigl(\det\hat a\bigr)^{-1},\qquad \lambda_b:=\bigl(\det\hat b\bigr)^{-1}\qquad\text{in }(\mathbf Z/691^2)^\times\ }$$
$$a_0:=\begin{pmatrix}\lambda_a&0\\0&1\end{pmatrix}\hat a,\qquad b_0:=\begin{pmatrix}\lambda_b&0\\0&1\end{pmatrix}\hat b$$

**なぜ reduction が壊れないか**: $\det\hat a\equiv-1$、$\det\hat b\equiv1\pmod{691}$ ⟹ $\lambda_a\equiv\lambda_b\equiv1\pmod{691}$ ⟹ $a_0\equiv a$, $b_0\equiv b$ ✔
**実測**($p=691$): $\det\hat a=98812$、$\lambda_a=98814$、$\det a_0=477480=-1$ ✔ / $\det\hat b=98123$、$\lambda_b=379360$、$\det b_0=1$ ✔

---

## §2 手順 2 — ★ Teichmüller 冪リフト

$$\boxed{\ \tilde a:=a_0^{\,691},\qquad \tilde b:=b_0^{\,691}\ }$$

**正しさ(4 点)**
| # | 主張 | 理由 |
|---|---|---|
| 1 | $\tilde a^2=I$ | $a_0^2=I+691X$ ⟹ $(a_0^2)^{691}=I+691^2(\cdots)=I$ |
| 2 | $\tilde b^3=I$ | $b_0^3=I+691Y$ ⟹ 同様 |
| 3 | **reduction 保存** | $a^2=I$・**691 奇** ⟹ $a^{691}=a$ / $b^3=I$・**$691\equiv1\pmod3$** ⟹ $b^{691}=b$ |
| 4 | $\det$ 保存 | $\det\tilde a=(-1)^{691}=-1$(691 奇)/ $\det\tilde b=1$ |

★ **司令塔のたたき台は正しい**(4 点とも機械確認 ✔)。
**実測値**:
$$\tilde a=\begin{pmatrix}466908&379387\\59&10573\end{pmatrix},\qquad \tilde b=\begin{pmatrix}221365&197784\\456129&256115\end{pmatrix}\pmod{477481}$$

---

## §3 手順 3 — braid 対と、**関係式が自動である理由**

$$\boxed{\ \sigma_1:=\tilde b^{-1}\tilde a,\qquad \sigma_2:=\tilde a\,\tilde b^{\,2}\ }$$
(全単射 $(x,y)\mapsto(u,v)=(xyx,xy)$ の逆 $x=v^{-1}u$、$y=u^{-1}v^2$ に $u=\tilde a$、$v=\tilde b$。$\tilde a^{-1}=\tilde a$)

**★ braid 関係が自動である理由(純粋な語の計算)**
$$xyx=v^{-1}u\cdot u^{-1}v^2\cdot v^{-1}u=u\qquad\textbf{— 関係式を一切使わない単純簡約}$$
$$yxy=u^{-1}v^2\cdot v^{-1}u\cdot u^{-1}v^2=u^{-1}v^{3}$$
$$\Longrightarrow\quad xyx=yxy\iff u^{2}=v^{3}$$
⟹ **$\tilde a^2=\tilde b^3=I$($=z$)から即座に成立** ✔ ⟹ ★ **$C_2*C_3$ 表示からの自動性**は司令塔の指摘どおり ✔
**実測**: $\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2=\tilde a$ ✔(理論値 $=u$ と一致)

$$\sigma_1=\begin{pmatrix}158625&469515\\262365&86342\end{pmatrix},\qquad \sigma_2=\begin{pmatrix}96915&106060\\215057&148052\end{pmatrix}$$

---

## §4 手順 4 — ★ $PB_3/N'$ の生成元と $N_{\rm ord}$

$$\bar x=\sigma_1^{\,2}=\begin{pmatrix}9115&57725\\391912&442339\end{pmatrix},\qquad \bar y=\sigma_2^{\,2}=\begin{pmatrix}144005&26367\\434427&307449\end{pmatrix}$$
いずれも $\det=1$ ⟹ **$SL(2,\mathbf Z/691^2)$ の中** ✔

**実測(機械)**: $\mathrm{ord}(\bar x)=\mathrm{ord}(\bar y)=\mathbf{47679}$。$c\in N'$ ゆえ $\mathrm{ord}(\bar c)=1$ ⟹
$$\boxed{\ N_{\rm ord}=\mathrm{lcm}(47679,47679,1)=47679=3\cdot23\cdot691\ }$$
$$\Longrightarrow\ \#\{\text{charming な }u\}=\varphi(47679)=2\cdot22\cdot690=\mathbf{30360}$$
⟹ ★ **前フィルタの走査量は 30,360 個** — 完全に実行可能 ✔

---

## §5 ★★ 生成性 — **機械の Size 計算は不要**(司令塔の問いへの回答)

> **問い**: 「生成性 = 1384 点法の $691^2$ 版か別法か」
> **答え**: ★ **別法。紙で確定します。**

1. reduction $\langle\tilde a,\tilde b\rangle\to\langle a,b\rangle=SL^\pm(2,691)$ は全射(witness・既証)
2. $\ker=\mathfrak{sl}_2$ は $SL(2,691)$-加群として**既約**($p\ge5$)⟹ **極小正規部分群**
3. ⟹ $\langle\tilde a,\tilde b\rangle\cap\mathfrak{sl}_2\in\{1,\mathfrak{sl}_2\}$
4. $=1$ なら補元 ⟹ $SL^\pm(2,\mathbf Z/p^2)\to SL^\pm(2,p)$ が分裂 ⟹ $SL(2,\mathbf Z/p^2)$ に制限しても補元 ⟹ **系統 C の非分裂**(悉皆検算 PASS)に矛盾

$$\boxed{\ \Longrightarrow\ \langle\tilde a,\tilde b\rangle=SL^{\pm}(2,\mathbf Z/691^2)\quad\textbf{(紙で確定)}\ }$$

⚠ **実際上も不可能**: $\lvert SL^\pm(2,\mathbf Z/691^2)\rvert=2p^4(p^2-1)=217{,}719{,}521{,}095{,}540{,}560\approx2.2\times10^{17}$ ⟹ Size 計算は走りません。
⟹ ★ **機械でやるのは「reduction が witness と一致する」ことの確認だけ**で足ります。

---

## §6 assert 項目(実装係・cert 必須)

```
=== [Q3-R1-LIFT] assert 一覧 ===
[L1] det a_0 == -1 (mod 691^2)          ★ λ_a = -(det â)^{-1}
[L2] det b_0 == 1  (mod 691^2)          ★ λ_b = (det b̂)^{-1}
[L3] a_0 ≡ a,  b_0 ≡ b  (mod 691)       ★ λ ≡ 1 (mod 691) の帰結
[L4] ã := a_0^691,  b̃ := b_0^691
[L5] ã^2 == I   (mod 691^2)             ★ Teichmüller
[L6] b̃^3 == I   (mod 691^2)
[L7] det ã == -1,  det b̃ == 1  (mod 691^2)
[L8] ã ≡ a,  b̃ ≡ b  (mod 691)          ★ reduction 一致(a^p=a・b^p=b)
[L9] σ_1 := b̃^{-1} ã,  σ_2 := ã b̃^2
[L10] ★ σ_1σ_2σ_1 == σ_2σ_1σ_2 (mod 691^2)   ★ 理論上は [L5][L6] から自動だが fail-closed で必ず assert
[L11] det σ_1 == det σ_2 == -1           ★ S_3 成分は互換 ⟹ N' ⊆ PB_3 の根拠
[L12] ★ x̄ := σ_1^2,  ȳ := σ_2^2 ;  det x̄ == det ȳ == 1   ★ §0 の訂正
[L13] ord(x̄) == ord(ȳ) == 47679 ;  N_ord == 47679 == 3·23·691
[L14] ⚠ 生成性の Size 計算は *やらない*(§5・紙で確定・規模 2.2e17)
      代わりに: reduction ⟨ã mod p, b̃ mod p⟩ が witness と一致することのみ確認
出力: cert (schema q3_r1_lift/v1)。u_touched=false ; c_touched=false
```

---

## §7 次段([Q3-R1] 本体)への受け渡し

```
=== [Q3-R1] 前フィルタ(§4 の資産を使う)===
charming u の集合 X = (Z/47679)^×(30,360 個)
各 u ∈ X について ★ 「x̄^u が x̄ に共役か」を判定
  ⟹ SL(2,Z/691^2) の共役類は標準分類で書ける ⟹ 巨大群を構成せず判定可
  ⟹ 落ちた u は well_defined になり得ない(iso_family_lemma_v1 §4.2)
★ SETTLE-AUTO により kernel 計算は不要 — well_defined だけ測る
```

## §8 GAP・記帳

- **【Q3R1-GAP-1】(小)** $SL(2,\mathbf Z/p^2)$ の共役類の標準分類を実装で使う ⟹ **正典外の標準事実**。自前再導出可能(固有値・Jordan 型 + $p$ 進の持ち上げ)⟹ **文献要請は不要**・cert に申告を。
- ★ **本仕様の新規部分**: ① **$\det$ 調整の正確な式**($\lambda\equiv1\bmod p$ ゆえ reduction が壊れない、の証明つき)② Teichmüller 冪の**4 点の正しさ**(特に $p\equiv1\bmod3$ が $b^p=b$ を与えること)③ **braid 関係の自動性の純粋語計算**($xyx=u$ は簡約のみ・$yxy=u^{-1}v^3$)④ ★★ **$PB_3/N'$ の生成元が $\sigma_i^2$ である訂正** ⑤ **$N_{\rm ord}=47679=3\cdot23\cdot691$・charming 30,360 個**の実測 ⑥ **生成性は紙で確定し Size 計算は不要**(規模 $2.2\times10^{17}$)。
- **申告**: 私の側は python 行列演算のみ(GAP 走行ゼロ)・$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
