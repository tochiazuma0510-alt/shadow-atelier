# 命題 Φ-fam — $\Phi_n:\operatorname{GT}(K^{(n)})\hookrightarrow\operatorname{Aut}(G_n)$ の族単射性(全奇数 $n$)

**状態札: candidate(裁定前・未 commit)**
起草: Claude 第二インスタンス(数学者)/ 2026-07-28
設問: 裁定 129 / 発案 **I-21**(`ideas/ideas_004_commanders_questions.md`)の正式化
依拠: `docs/notes/oddH_full_proof_v1.md` §2 補題 A・§11.1(閉形式)/ `docs/notes/w2fam_v1.md` §3(完全列)/ `docs/notes/w2arith_v1.md` §1 補題 L / 正典 §2 Def 3.7・(3.53)・§3 Thm 4.3 (4.12)

---

## 1. 単窓の既出事実(引用特定・設問 1)

| 窓 | 言明 | 出所 | 状態 |
|---|---|---|---|
| $K^{(3)}$ | **F19((K4) Φ 単射)**: `∀ m ∈ X3, ∀ m' ∈ X3, ∀ k k' : Fin 3, (canonX m, canonY m k) = (canonX m', canonY m' k') → m = m' ∧ k = k'`(および `F19_injective_phicf` で $\Phi$ 本体でも直接確認) | `lean/K3/Shadows.lean` L68–79(`#print axioms` 済) | **verified(Lean)** |
| $N_A$($A_5$) | **(I2)**「$\Phi:\operatorname{GT}(N_A)\to S_5$ は単射で $\lvert\operatorname{GT}(N_A)\rvert=20$、像は $N_{S_5}(\langle X\rangle)=F_{20}$(定理 20′)」 | `docs/week4-A5算術飽和_v3.md` L435(飽和定理 §4 の入力・L449 で使用) | **紙上・単系統**(【GAP-C6】: 「$\Phi$ が単射」は紙上、$\lvert\operatorname{GT}\rvert=20$ のみ二系統) |

両者とも形は同じ「$\Phi:\operatorname{GT}(N)\to\operatorname{Aut}(G)$ が単射」($A_5$ では $\operatorname{Aut}(A_5)=S_5$)。**族版が言明されていなかっただけ**という発案の読みは正しい。

---

## 2. 命題 Φ-fam

$n\ge3$ 奇、$G_n=A\rtimes Q$(ODD-H 補題 A の座標)、$u:=2m+1$。GT-shadow $[m,f]$ に対し $\Phi_{m,f}$ を
$$\Phi_{m,f}(X)=X^{u},\qquad \Phi_{m,f}(Y)=F^{-1}Y^{u}F\qquad(F=f\ \text{の}\ G_n\ \text{での値})$$
で定める($E_{m,f}$ の $G_n=F_2/K^{(n)}_{F_2}$ への誘導)。

> **命題 Φ-fam.** 全奇数 $n\ge3$ で
> $$\Phi_n:\ \operatorname{GT}(K^{(n)})\longrightarrow\operatorname{Aut}(G_n),\qquad [m,f]\mapsto\Phi_{m,f}$$
> は**単射な群準同型**であり $\ker\Phi_n=\{[0,1]\}$。
> **向き(規約 W-4・発案が明記を要求した点)**: $\Phi$ は**共変**である:
> $$\boxed{\ \Phi_{[m_1,f_1]\circ[m_2,f_2]}=\Phi_{[m_1,f_1]}\circ\Phi_{[m_2,f_2]}\ }\qquad((\varphi\circ\psi)(g)=\varphi(\psi(g)))$$
> — 反準同型ではない。

**$\Phi_{m,f}\in\operatorname{Aut}(G_n)$ であること**: $[m,f]$ が GT-shadow なら $T_{m,f}$ は全射(Def 3.7)、$G_n$ は有限だから単射、すなわち自己同型。**isolated 性は不要**(発案が「破綻しそうな点」に挙げた懸念は空振り — isolated 性が要るのは $\operatorname{GT}(K^{(n)})$ が (3.53) で**群**になる部分だけで、そちらは Thm 4.3 が与える)。

**共変性の証明**: $y$ 上で
$$T_1\bigl(T_2(y)\bigr)=T_1(f_2^{-1}y^{u_2}f_2)=E_1(f_2)^{-1}\bigl(f_1^{-1}y^{u_1}f_1\bigr)^{u_2}E_1(f_2)
=\bigl(f_1E_1(f_2)\bigr)^{-1}y^{u_1u_2}\bigl(f_1E_1(f_2)\bigr),$$
$x$ 上で $T_1(T_2(x))=x^{u_1u_2}$。(3.49) より $u_1u_2=2(2m_1m_2+m_1+m_2)+1$、第二成分 $f_1E_{m_1,f_1}(f_2)$ は (3.53) そのもの。∎

---

## 3. 証明(設問 2 — 発案の「5 行」の検証)

**判定: 発案の 5 行は正しい。ギャップなし。** 以下は同じ論法を逐語化したものである。

$\Phi_{m,f}=\mathrm{id}_{G_n}$ とする。$G_n=\langle X,Y\rangle$ なので $\Phi(X)=X$ かつ $\Phi(Y)=Y$ を見ればよい。

1. **$\Phi(X)=X^{u}=X\iff X^{2m}=1$**。$\operatorname{ord}(X)=2n$(補題 A(3))より $2n\mid2m$、すなわち $n\mid m$。$m\in\mathbf Z/2n$ だから $m\in\{0,\,n\}$。
2. **$m=n$ の排除**: ODD-H §11.1 の閉形式
 $$\Phi_{m,f}\big|_A=\operatorname{diag}\bigl(u,\,u,\,1-2\varkappa(m)\bigr),\qquad 1-2\varkappa(m)=(-1)^m u$$
 に $m=n$($n$ 奇ゆえ $m$ 奇)を入れると $u=2n+1\equiv1$、$(-1)^mu\equiv-1\pmod n$。よって $\Phi\big|_A=\operatorname{diag}(1,1,-1)$。$n\ge3$ では $-1\ne1$ in $\mathbf Z/n$(さもなくば $n\mid2$)だから $\Phi(e_3)\ne e_3$、すなわち $\Phi\ne\mathrm{id}$。
3. **$m=0$**: このとき $u=1$、$\varkappa(0)=0$、(4.12) より $F=(2k,-2k,0)$、閉形式から
 $$\Phi_{0,f}(Y)=(1-2F_1,\;u,\;1-2F_3)\,q_2=(1-4k,\,1,\,1)\,q_2 .$$
 $Y=(1,1,1)q_2$ と比べて $1-4k\equiv1$、すなわち $4k\equiv0\pmod n$。$n$ 奇ゆえ $4\in(\mathbf Z/n)^\times$、よって $k\equiv0$、$F=1$、$[m,f]=[0,1]$。∎

> **各段が使う既証明部品**: 1 は補題 A(3)($\operatorname{ord}X=2n$ — ここで $n$ 奇が効く)、2 は §11.1 の閉形式、3 は (4.12) と §11.1、および $\gcd(4,n)=1$。**$m$ の水準は $\mathbf Z/2n$**(補題 L / w2fam §3.1)— ここを $\mathbf Z/n$ と読むと段 1 の「$m\in\{0,n\}$」が「$m=0$」に潰れ、段 2 が消えて**証明が短く見えるが穴になる**(段 2 こそが chirality を排除している段である)。

---

## 4. 作用対象の正確な言明(設問 3)

**対象 = marked 正則 dessin $G_n$ 自身**(= $\psi_n$ の像に marking $(X,Y)=(\psi_n(x),\psi_n(y))$ を付けたもの;対応する被覆は正則で deck 群は $G_n$)。命題 Φ-fam はこの**marked** 対象上での忠実性である。二層構造は (W2)-fam の完全列と次のように対応する:

$$1\longrightarrow \underbrace{\mathfrak F_0\cong C_n}_{\text{deck(並進)}}\longrightarrow\operatorname{GT}(K^{(n)})\xrightarrow{\ \widetilde\chi_{2M}\ }\underbrace{(\mathbf Z/4n)^\times}_{\text{円分}\times\text{chirality}}\longrightarrow1$$

* **下層**: $\Phi(\mathfrak F_0)=\operatorname{inn}(\langle X^2\rangle)$(命題 K5-1・w2fam §3.5 で再確認)。$\langle X^2\rangle=\langle a_1\rangle$ は deck 群 $G_n$ の中の**並進** $C_n$ で、w2fam の核(= $[\operatorname{GT},\operatorname{GT}]$ = Thm 4.6 座標の並進部)と同一物。
* **上層**: $\widetilde\chi_{2M}$ の $(\mathbf Z/n)^\times$ 成分が円分、$(\mathbf Z/4)^\times$ 成分が chirality $\delta=(-1)^m$(w2fam §4)。

> ### ⚠ 訂正(FINDING Φ1)— 「上層は $\operatorname{Out}$ へ単射」は**偽**
> 発案 I-21 は「剰余 $(\mathbf Z/4n)^\times$ は **$\operatorname{Out}$ への単射**」と書くが、これは成り立たない。$\Phi_{m,f}$ が内部自己同型になるのは、$\Phi\big|_A=\operatorname{diag}(u,u,(-1)^mu)$ が $Q$ の作用パターン $\{(+,+,+),(+,-,-),(-,+,-),(-,-,+)\}$ のいずれかになるときで、
> * $(+,+,+)$: $u\equiv1\ (n)$ かつ $(-1)^m=+1\Rightarrow m=0$;
> * $(-,-,+)$($q_3$ パターン): $u\equiv-1\ (n)$ かつ $(-1)^m=-1\Rightarrow m=2n-1$;
> * 残る 2 パターンは $u\equiv1$ と $u\equiv-1$ を同時に要求し $n\ge3$ で不可能。
>
> そして $m=2n-1$ は実際に内部である: $F=(2k,-2k,0)$ に対し
> $$\Phi_{2n-1,f}=\operatorname{inn}\bigl(((1-2k)e_1)\,q_3\bigr)$$
> ($X,Y$ 上で直接検算。$\bigl((1-2k)e_1\bigr)q_3$ は対合)。$m=2n-1$ は $u=4n-1\equiv-1\ (4n)$、すなわち $\widetilde\chi_{2M}$ の値が $-1$ — **複素共役に対応する元**である。したがって
> $$\Phi_n^{-1}\bigl(\operatorname{Inn}(G_n)\bigr)=\{[m,f]:m\in\{0,\,2n-1\}\},\qquad \bigl|\Phi_n^{-1}(\operatorname{Inn})\bigr|=2n,$$
> $$\operatorname{Im}\bigl(\operatorname{GT}(K^{(n)})\to\operatorname{Out}(G_n)\bigr)\cong(\mathbf Z/4n)^\times/\{\pm1\},\qquad \text{位数}\ \varphi(n)\ (\ne2\varphi(n)).$$
> **幾何的な読み**: **unmarked** dessin の上では chirality が消える(dessin はその鏡像と同型 — 複素共役が deck 変換で吸収される)。忠実性が成り立つのは **marked** 対象の上だけである。発案の「正則閉包に上がれば一本で復活する」は **marking を保持する限り正しい**が、「$\operatorname{Out}$ への単射」という形では誤り。**I-12(非正則 $H^{\rm fun}$ 塔では $\varepsilon$ が不可視)と同じ現象が、正則対象でも marking を落とした瞬間に再発する。**

> **混同注意**: $\{0,\,2n-1\}$ という $m$ の集合は、ODD-H §11.4 の**実装バグ生存集合**と偶然一致する($n=9$ でどちらも $\{0,17\}$)。両者の条件はともに「$u\equiv\pm1$ かつ $\delta$ が符合」に帰着するため一致するが、**意味は無関係**(一方は捻れ関手の固定点、他方は内部自己同型の判定)。台帳で引用する際に混ぜないこと。

---

## 5. 逆極限と F6.2(e)(設問 4)

**閉じるか: 対象を正しく取れば YES。ただし $H^{\rm fun}$ 塔の上ではない。**

奇数の整除順序で $d\mid n$ に対し $D_n\twoheadrightarrow D_d$($r\mapsto r,s\mapsto s$)は $G_n\twoheadrightarrow G_d$ を誘導し、marking を保つ($X_n\mapsto X_d$, $Y_n\mapsto Y_d$;座標では $A_n=(\mathbf Z/n)^3\twoheadrightarrow(\mathbf Z/d)^3$、$Q$ は不変)。$\Phi$ はこれと可換である:
$$\Phi^{(d)}_{R_{n,d}[m,f]}\circ\mathrm{red}=\mathrm{red}\circ\Phi^{(n)}_{[m,f]}$$
(生成元像 $X^u$, $F^{-1}Y^uF$ が準同型 $\mathrm{red}$ で送られるだけ。$u$ の水準は $\bmod\ 4d$ へ落ちて整合 — 補題 L)。したがって
$$G^{\rm odd}:=\varprojlim_{n\ \rm odd}G_n=(\widehat{\mathbf Z}^{\rm odd})^3\rtimes Q,\qquad
\Phi^{\rm odd}:\operatorname{GT}^{\rm odd}\longrightarrow\operatorname{Aut}(G^{\rm odd})$$
が定義でき、$\Phi^{\rm odd}(g)=\mathrm{id}$ なら各段で $\Phi^{(n)}(g_n)=\mathrm{id}$、命題 Φ-fam より $g_n=1$、よって $g=1$。**単射性は極限へ自動的に上がる**(連続性も各段が有限ゆえ自動)。

> **結論文(明言)**: $\operatorname{GT}^{\rm odd}\cong\operatorname{Aff}(\widehat{\mathbf Z}^{\rm odd})\times C_2$ は、**marked pro-正則 dessin $G^{\rm odd}=\varprojlim G_n$ の自己同型群への連続単射として忠実に実現される**。便 75 F6.2(e) の「一本の対象上の忠実作用」は、対象を**正則かつ marked** に取れば閉じる。

**追加前件(すべて明示)**

| # | 前件 | 状態 |
|---|---|---|
| P1 | $\operatorname{GT}^{\rm odd}=\varprojlim_n\operatorname{GT}(K^{(n)})\cong\operatorname{Aff}(\widehat{\mathbf Z}^{\rm odd})\times C_2$ | **便 75 F6.2 の引用**(本稿は再証明しない) |
| P2 | marked 還元系 $G_n\twoheadrightarrow G_d$($d\mid n$ 奇) | 本節で証明(初等) |
| P3 | $\Phi$ と還元の可換性 | 本節で証明(1 行) |
| P4 | 奇数の整除順序が有向 | 自明 |
| P5 | 各段の $\Phi_n$ 単射 | **命題 Φ-fam**(§3) |

**閉じない対象(重要)**

* **$H^{\rm fun}$ 塔**($2n$ 次の非正則被覆): $\Phi_g(H_{2,1,\beta})=H_{2,\delta,\beta u+c}$(ODD-H §11.2)なので $\delta=-1$ の元は $H^{\rm fun}$ を**自分自身に写さない** — 作用が塔の上に定義すらされない。I-12 が窓モジュライ $W_n$ へ広げたのはこのため。**F6.2(e) を $H^{\rm fun}$ 塔で閉じることはできない。**
* **unmarked 正則 dessin**($\operatorname{Out}$ 経由): §4 の FINDING Φ1 により核が位数 $2n$、逆極限でも非自明。**閉じない。**

したがって F6.2(e) の正しい閉じ方は、発案 I-21 の言うとおり「**一本の正則対象**」で、ただし**marked** の限定つきである。I-12 の $W_n$(窓モジュライ)とは排他でなく、**「marking を落とすなら対象を広げる/対象を一本にするなら marking を保つ」という双対**として並置するのが正確である。

---

## 6. 機械検分($n=9$・独立実装・証明とは独立)

| 検査 | 実測 | 期待 |
|---|---|---|
| 108 shadow すべてで $\Phi\in\operatorname{Aut}(G_9)$ | true | ✓ |
| $\ker\Phi_9$ | **1 個** $=\{[0,1]\}$ | ✓(命題 Φ-fam) |
| $\Phi$ の像の相異個数 | **108/108** | ✓ 単射 |
| (3.53) の積が shadow 集合に閉じる | 11664/11664 | ✓ |
| **$\Phi_{g\circ h}=\Phi_g\circ\Phi_h$(共変)** | **11664/11664** | ✓ |
| $\Phi_{g\circ h}=\Phi_h\circ\Phi_g$(反変) | 2160/11664(可換対のみ) | ✗ = 反準同型ではない |
| $\Phi^{-1}(\operatorname{Inn})$ の位数 | **18** $=2n$ | ✓(FINDING Φ1) |
| その $m$ の集合 | $\{0,\,17\}$ | ✓ $=\{0,\,2n-1\}$ |
| $m=17$ の conjugator($f$ の $k=0,4,\dots$) | $((1)e_1)q_3,\ ((2)e_1)q_3,\ \dots$ | ✓ $((1-2k)e_1)q_3$ |
| $m=0$ の conjugator | $\mathrm{id},\ a_1,\dots$ | ✓ $\operatorname{inn}(a_1^{-2k})$(K5-1) |
| $\operatorname{Out}$ への像の位数 | **6** | ✓ $\varphi(9)=6$($\ne\varphi(36)=12$) |

---

## 7. FINDING と未閉鎖

| # | 種別 | 内容 |
|---|---|---|
| **Φ1** | **誤り(発案 I-21)** | 「剰余 $(\mathbf Z/4n)^\times$ は $\operatorname{Out}$ への単射」は**偽**。$m=2n-1$(複素共役・$u\equiv-1$)の $2n$ 個の shadow が内部自己同型 $\operatorname{inn}(((1-2k)e_1)q_3)$ になる。$\operatorname{Out}$ 像は $(\mathbf Z/4n)^\times/\{\pm1\}$(位数 $\varphi(n)$)。**忠実性は marked 対象に限る** |
| **Φ2** | 成立 | 発案の「5 行」証明は**ギャップなし**。段 2($m=n$ の排除)が chirality を排除する要で、$m$ の水準を $\mathbf Z/2n$ と正しく取ることに依存(補題 L) |
| **Φ3** | 簡略化 | $\Phi_{m,f}\in\operatorname{Aut}(G_n)$ に **isolated 性は不要**(Def 3.7 の全射性 + 有限性で足りる)。発案の懸念は空振り。isolated が要るのは $\operatorname{GT}$ が群であること |
| **Φ4** | 向きの確定 | $\Phi$ は**共変**(規約 W-4 の要求に回答)。$n=9$ で 11664/11664 対で機械確認 |
| **Φ5** | 対の提示 | F6.2(e) は「**marked 正則一本で忠実**(本稿)+ **marking を落とすと chirality が構造的に不可視**(§4 = I-12 と同型の現象)」の対で閉じる |

* 【Φ-1】紙上証明(paper-proof candidate)。$K^{(3)}$ のみ Lean 済(F19)、族版は未 Lean。$n=9$ の機械検分は単系統(本稿の独立実装)。
* 【Φ-2】P1(便 75 F6.2 の $\operatorname{GT}^{\rm odd}$ 同定)は**引用**であり本稿は再証明していない。
* 【Φ-3】$\Phi_n$ の**像**の記述($\operatorname{Aut}(G_n)$ の中でどこか)は本稿の射程外(発案の自認どおり、像を主張に含めると (1.12) の未較正に依存する)。単射性のみ。
