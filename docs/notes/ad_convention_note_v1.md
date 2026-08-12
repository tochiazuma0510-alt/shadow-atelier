# 規約照合 1 行 — $\mathrm{Ad}$ の向きと $\alpha_i^2$ の一致先(裁定 1133 の確認事項)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔(`k9_sigma_realization_v1` cert の規約行用)
生成 script = `scratchpad/ad_convention_check.g`(GAP 4.16.0・自由群 $F_2$)
⚠ $u$/$c$ 非接触。**格: candidate**。

---

## §0 裁定(1 行)

$$\boxed{\ \textbf{正典の規約は}\ \textbf{左}:\quad \mathrm{Ad}(g)(w)=g\,w\,g^{-1}\ }$$

**逐語根拠**(`照合_B3表示_T2土台.md`・p.4/p.5/p.11 の**画像照合済**):
- §4: 「B0.1: $\theta=\mathrm{Ad}(\Delta)\vert_{F_2}$(**$\mathrm{Ad}(\Delta)(w)=\Delta w\Delta^{-1}$**、$c$ 因子なし)」
- §4 末: 「委嘱文の懸念 3 点の検分: **逆向きなし**($\mathrm{Ad}$ は一貫して **$g\cdot(\cdot)\cdot g^{-1}$**)」
- 整合: (1.13) $\Delta x_{12}\Delta^{-1}=x_{23}$ が (1.14) $\theta(x)=y$ と一致 ✔

$$\Longrightarrow\ \boxed{\ \alpha_1^2=(w\mapsto x\,w\,x^{-1})\ \textbf{(左 }\mathrm{Ad}(x)\textbf{)}\ \textbf{が正典側の正解}\ }$$

---

## §1 実装係の「$\mathrm{Ad}_{\rm right}$ で一致」の正体 — **第 2 形で組んでいます**

正典 (1.11)(1.12) は $\sigma_i$ 共役と $\sigma_i^{-1}$ 共役の**両方**を与えており、`照合_B3表示` §2 が「**逆共役側($\sigma_i^{-1}\cdot\sigma_i$)は語順が $x_{12}^{-1}x_{23}^{-1}\leftrightarrow x_{23}^{-1}x_{12}^{-1}$ と入れ替わる**」と明記しています。⟹ **判別子は語順です**:

| | $\alpha_1(y)$ | $\alpha_2(x)$ | $\alpha_1^2(y)$ | 意味 |
|---|---|---|---|---|
| ★ **第 1 形(左・正典)** | $y^{-1}x^{-1}$ | $x^{-1}y^{-1}$ | $x\,y\,x^{-1}$ | $\sigma_i$ 共役 |
| 第 2 形(右) | $x^{-1}y^{-1}$ | $y^{-1}x^{-1}$ | $x^{-1}y\,x$ | $\sigma_i^{-1}$ 共役 |

**機械確認**(自由群 $F_2$・`ad_convention_check.g`):

```
LEFT  : a1(y)=y^-1*x^-1  a2(x)=x^-1*y^-1  braid: true
        a1^2(y) = x*y*x^-1   = LEFT Ad(x): true / = RIGHT y^x: false
        a2^2(x) = y*x*y^-1   = LEFT Ad(y): true / = RIGHT x^y: false
RIGHT : a1(y)=x^-1*y^-1  a2(x)=y^-1*x^-1  braid: true
        a1^2(y) = x^-1*y*x   = LEFT: false / = RIGHT: true
        a2^2(x) = y^-1*x*y   = LEFT: false / = RIGHT: true
beta_i = alpha_i^-1 : true / true
```

⟹ ★ **「$\mathrm{Ad}_{\rm right}$ で一致した」= $\alpha_i$ を第 2 形($y\mapsto x^{-1}y^{-1}$)で組んだ**ということです。私の spec [S-2] は第 1 形($y\mapsto y^{-1}x^{-1}$)を書いていたので、**実装で語順が入れ替わった**と思われます。

⚠ **GAP の既定にも注意**: GAP の $g^h$ は $h^{-1}gh$(**右**)です。⟹ **左規約で正しく組んだ $\alpha_1^2$ は GAP では `ConjugatorAutomorphism(G, x^-1)` と一致するのが正常**で、`ConjugatorAutomorphism(G, x)` と比べれば当然**不一致**になります。この 2 つの取り違えでも同じ症状が出ます。

---

## §2 実害の範囲

$\beta_i=\alpha_i^{-1}$(機械確認)ゆえ:

| 量 | 影響 |
|---|---|
| $\langle\alpha_1,\alpha_2\rangle$(群)と $\lvert\text{像}\rvert=17{,}496$ | ★ **不変**($\langle\alpha^{-1}\rangle=\langle\alpha\rangle$) |
| braid 関係 | ★ **不変**(両形とも成立・機械確認) |
| $C_Q(\bar\sigma_1)$(I-SET-4 の捻り集合 $D_1$) | ★ **不変**($C(g)=C(g^{-1})$) |
| ⚠ **$\bar\sigma_i$ の同定** | **逆元になる** |
| ⚠ **$T_{m,f}:\sigma_1\mapsto\sigma_1^{u}$ を経由する量**($\chi_{\rm vir}$・$\ker T$ の計算) | **$u\mapsto-u$ の符号反転**が入りうる |

⟹ ★ **W4 債務返済(位数 17,496 の実現)としては第 2 形でも成立**していますが、**$u$ に触れる計算に流用する前に向きを固定する必要があります**。charming 判定($\gcd(u,N_{\rm ord})=1$)は符号不変なので影響なし ✔

---

## §3 cert 規約行への推薦文

```
ad_convention : "canon = LEFT :  Ad(g)(w) = g w g^-1
                 (照合_B3表示_T2土台 §4 逐語・p.4/p.5 画像照合済)"
alpha_form    : "first form of (1.11)/(1.12) :  a1: x->x, y->y^-1 x^-1
                                                 a2: x->x^-1 y^-1, y->y"
alpha_sq      : "a1^2 = (w -> x w x^-1)  [LEFT Ad(x)]
                 ⚠ in GAP this equals ConjugatorAutomorphism(G, x^-1), NOT (G, x)
                    since GAP's g^h means h^-1 g h (RIGHT)"
implemented_form : "second form (sigma_i^-1 conj) if a1(y) = x^-1 y^-1"
                   -> then the realized sigma_i are the INVERSES of the canonical ones;
                      group / braid / |image| = 17,496 / centralizers are unaffected,
                      but any use of sigma_1^u (chi_vir, ker T) flips the sign of u.
```

★ **推薦**: 実装を**第 1 形へ直す**のが最も安全です(1 行の差し替え)。直さない場合は上の `implemented_form` 行を必ず cert に残し、$u$ を使う下流で参照できるようにしてください。

---

## §4 記帳

- ★ 本書の内容: 正典の $\mathrm{Ad}$ は**左**(逐語・画像照合済)/ 判別子は**語順**($y^{-1}x^{-1}$ vs $x^{-1}y^{-1}$)/ GAP の $g^h$ が右であることによる二重の取り違え要因 / 実害は「$\bar\sigma_i$ の同定が逆元」と「$u$ の符号」に限局。
- ⚠ **私の spec の書き方の反省**: `d972_h1_adjudication_v1.md` §7 [S-2] で式は第 1 形を書きましたが、**「これは左規約($\sigma_i$ 共役)である」と明示しませんでした**。⟹ 今後、共役を含む spec には**向きを 1 行で併記**します。
- **申告**: GAP 4.16.0(`scratchpad/ad_convention_check.g`・自由群のみ)+ 正典逐語。$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**。
