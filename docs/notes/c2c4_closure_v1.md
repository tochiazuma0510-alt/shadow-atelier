# C2・C4 の閉鎖 — (W1) の族供給と formal 上界の組立 **v1**

2026-07-28: Claude(数学者レイヤー・Opus 5・第二インスタンス)。司令塔委嘱(裁定 112・I-13 採用分)。
**状態札**: `candidate / 単系統・未監査`。**commit していない。**
**依拠**: 正典(`docs/notes/抽出_Kn定義_D1.md` §4 = 2405.11725 Thm 4.3 画像照合済・`docs/week1-定義ノート.md` §isolated/§Thm 4.3・`docs/week4-K3飽和_opus_v3.md` §5.2.2 補題 R・BFC v2.15・TB4 v2.5・`docs/week4-A5算術飽和_v4.md` §1.4)+ repo(`provenance/CLAIMS.md` W3-13/W3-15①/W3-17・`sol/sol_reply_75*.md` F3.2)+ `docs/notes/hfun_functoriality_v1.md`・`docs/notes/t63_reconnaissance_v1.md`。**外部文献なし。$u$・封印量に触れていない。**

---

## 0. 判定(先に)

| 残件 | 判定 | 残る依存 |
|---|---|---|
| **C2**((W1) の $n=9$ 供給) | **閉鎖(族で)** — しかも全奇 $n\ge3$ で一斉 | (CAL)(**既証明**)のみ |
| **C4**($\mathrm{ord}(a_9)\mid9$) | **二経路。Route 1 は C3 に依存/Route 2 は (6.3) から無償** | 下記 §2.4 |

$$ \boxed{\ \textbf{C2 は「Thm 4.3 の引用 + (CAL) による規約整合」で閉じる。}\ \bar\iota\ \text{も族条項も要らない(§1.5)}.\ } $$
$$ \boxed{\ \textbf{C4 は tower 関係 (T) を仮定する文脈では追加仮定にならない(§2.3)}.\ } $$

---

## 1. C2 — (W1) の族供給(**W1-fam**)

### 1.1 引用箇所の特定

> **2405.11725 Theorem 4.3(p.18)**【`docs/notes/抽出_Kn定義_D1.md` §4・画像照合済・逐語】
> "**For every $n\ge3$**, the set of GT-shadows with the target $K^{(n)}$ is
> $\mathrm{GT}(K^{(n)})=\{(m,(r^{2k},r^{-2k},r^{\kappa(m)}))\mid m\in\mathcal X_n,\ k\in\mathbb Z\}$ if $4\nmid n$ … (4.12)
> … Furthermore, **$K^{(n)}$ is an isolated object of the groupoid GTSh**."

**$n=9$ は $n\ge3$ かつ $4\nmid n$** なので、この言明の射程に**そのまま入る**($n=3$ も同様 — 塔の下段に要る)。

**isolated の定義**(`docs/week1-定義ノート.md` §3):
> **settled**: $\ker(T_{m,f})=N$。**isolated**: 全 shadow が settled ⇒ $\mathrm{GT}(N)=\mathrm{GTSh}(N,N)$ は有限群。

### 1.2 isolated $\Rightarrow$ (W1)(規約差を捨象した形)

> ### 補題 W1-a
> $\bar N\trianglelefteq\hat F_2$ を開正規部分群とし、$N$ が GTSh の **isolated object** とする。このとき、$\gamma\in G_{\mathbb Q}$ の shadow が定める $\hat F_2$ の自己同型 $\alpha^{\rm Ih}_\gamma$ について
> $$ \alpha^{\rm Ih}_\gamma(\bar N)=\bar N\qquad(\forall\gamma\in G_{\mathbb Q}). $$

**証明.** $\gamma$ の shadow を $(m_\gamma,f_\gamma)=\mathrm{Ih}(\gamma)$ とすると、これは source $N$ をもつ GT-shadow であり、その **target は $\ker(T_{m_\gamma,f_\gamma})$** である(settled の定義に現れる量)。$T_{m,f}$ は $x\mapsto x^{2m+1},\ y\mapsto f^{-1}y^{2m+1}f$ が定める写像の $F_2/N$ への合成、すなわち $\alpha^{\rm Ih}_\gamma$ に $\bar N$ への還元を合成したものだから
$$ \ker\bigl(T_{m_\gamma,f_\gamma}\bigr)=\bigl(\alpha^{\rm Ih}_\gamma\bigr)^{-1}(\bar N). $$
$N$ が isolated ⇒ **全 shadow が settled** ⇒ とくに $\gamma$ の shadow も settled ⇒ $(\alpha^{\rm Ih}_\gamma)^{-1}(\bar N)=\bar N$、すなわち $\alpha^{\rm Ih}_\gamma(\bar N)=\bar N$。∎

> **★ isolated は「全 shadow」について言う** — 算術的な($\mathrm{Ih}$ の像に来る)ものだけでなく全 charming pair について。したがって $\mathrm{Ih}$ の像を特定せずに使える。**これが「引用で済む」理由である。**

### 1.3 規約整合の一補題(**ここが C2 の実質**)

BFC の (W1) は $\alpha^{\rm Ih}$ ではなく **$\alpha^{\rm std}$**(接基点 $\vec{01}$ の標準係数切断 $s_{\vec{01}}$ の共役作用)で書かれている。両者を結ぶのが較正である。

> ### 補題 W1-b(規約整合)
> **較正 (CAL)**($\alpha^{\rm Ih}=\alpha^{\rm std}$・`docs/week4-A5算術飽和_v4.md` §1.4:補題 C + 補題 D0/D + 補題 I3‡ ⇒ 系 E。**窓非依存・証明済**)の下で、補題 W1-a は
> $$ \boxed{\ \alpha^{\rm std}_\gamma(\bar N_n)=\bar N_n\qquad(\forall\gamma\in G_{\mathbb Q},\ \forall n\ge3)\ } \tag{W1-fam} $$
> を与える。$\bar N_n=\ker(\hat F_2\twoheadrightarrow P_n)$ は開($\lvert P_n\rvert=4n^3<\infty$)。**すなわち (W1) が全 $n\ge3$ で成立する。**

**証明.** (CAL) は $\hat F_2$ の自己同型としての等式 $\alpha^{\rm Ih}_\gamma=\alpha^{\rm std}_\gamma$($\forall\gamma$)。補題 W1-a を代入。開性は $\bar N_n$ が有限指数の閉部分群であることから。∎

> **★ (CAL) が唯一の実質的入力である。** (CAL) は $A_5$ v4 §1.4 で**窓非依存に証明済**(補題 C は「標準実経路の Galois path cocycle が $[\hat F_2,\hat F_2]^{\rm top.cl.}$ に入る」という $\mathbf P^1-\{0,1,\infty\}$ 一般の主張で、$A_5$ を一切使わない)。**したがって新規の証明義務はない。**
> **⚠ 一点だけ確認事項**: 補題 W1-a の「target $=\ker(T_{m,f})$」という読みは `定義ノート` の settled の定義から取った。**$T_{m,f}$ と $\alpha^{\rm Ih}_\gamma$ の同一視(向き・逆元の位置)は規約 W-1 の下で読むこと**(★教材 T6: action law / 合成 / 向き を分ける)。**私は逆元の位置を $(\alpha)^{-1}(\bar N)$ と取ったが、$\alpha(\bar N)$ でも結論(不変性)は同じ**なので、この一点は結論に影響しない。**申告する。**

### 1.4 G3(便 75 F3.2)が要求する形との接続

便 75 F3.2 の abstract descent lemma(**PAPER-PROOF 済**)は (G3.2) の計算で
$$ \text{“}\bar N_d\trianglelefteq\hat F_2\ \text{と (W1) の}\ \alpha_\gamma(\bar N_d)=\bar N_d\text{”} $$
を使う。塔 $d=3\mid n=9$ に対し必要なのは
$$ \alpha^{\rm std}_\gamma(\bar N_3)=\bar N_3\quad\text{と}\quad \alpha^{\rm std}_\gamma(\bar N_9)=\bar N_9\qquad(\gamma\in G_{F_9}\subseteq G_{\mathbb Q}). $$
**(W1-fam) は $n\ge3$ の全段で与えるので、両方を同時に供給する** ✓。$\gamma$ が $G_{\mathbb Q}$ 全体で成り立つので、部分群 $G_{F_9}$ への制限は自動 ✓。

$$ \boxed{\ \textbf{C2 は閉鎖。G3 の前提が要求する両段の (W1) を (W1-fam) が同時に満たす。}\ } $$

### 1.5 **$\bar\iota$ も族条項も要らない**(委嘱への訂正)

委嘱は「その構成が我々の正規化(Rule 1 族条項・$\bar\iota$ 制限)と整合する」ことを求めたが、**(W1) にはそれらは入らない**:

| 量 | (W1) に現れるか |
|---|---|
| $\alpha^{\rm std}$((TB2) の係数分裂) | **現れる**。ただし (TB2) の分裂は「$G_{\mathbb Q}$ が $\Omega$ に係数のみで作用し全 $\beta^{1/n}$ を固定する」で、**根系 $(\zeta_n)$ の選択に依らない** |
| $\bar\iota:\bar{\mathbb Q}\hookrightarrow\mathbf C$ | **現れない** |
| 族条項($K_q=\mathbb Q[T]/\Phi_{4q}$・$\iota_\infty^{(q)}$) | **現れない** |
| marking $\pi:\hat F_2\twoheadrightarrow P_n$ | 現れる($\bar N_n$ の定義)。D1 (3.6) で凍結済 |

$$ \boxed{\ \textbf{C2 は root-normalization-free である。}\ } $$

**⇒ 手続き上の含意**: $n=9$ 窓の `Z-norm-seal/v1` window inventory 行(`not_assessed`)は **C2 の前提ではない**。両者を同じ関門に入れないこと(scope 逆行の防止)。

---

## 2. C4 — formal 上界 $\mathrm{ord}(a_9)\mid9$

### 2.1 Route 1 — 補題 R の第 3 段の $n=9$ instance 化

正典 `docs/week4-K3飽和_opus_v3.md` §5.2.2(**定理 $R^{\rm cyc}_{\rm formal}$ = 補題 R**)の証明第 3 段は逐語:

> 3. (6′) の像の等式と (5′) より $\kappa_{u^{-1}}(G_K)\subseteq\mu_M[e]$、すなわち $\mathrm{ord}([u^{-1}]_M)\mid e$。

**$n=9$ での部品**:

| 部品 | $n=9$ での値/供給 | 状態 |
|---|---|---|
| $M=\mathrm{ord}(X_9)$ | $M=2n=18$ | **HF-1(b)**(証明済) |
| $e=\lvert\mathfrak F_0\rvert$ | $e=n=9$($\mathfrak F_0\cong C_n$) | 正典(便 29 (6.1))— **要転記確認** |
| (6′) の像の等式 $\rho_0(\mathfrak F_0)=\tau(\mu_M[e])$ と忠実性 | 全奇 $n$ で自動 | **命題 K5-1**($\Phi_{0,k}=\mathrm{inn}(X^{-2k})$・W3-15①) |
| $\mathrm{Ih}_N(G_K)\subseteq\mathfrak F_0$ | (W2) の完全列 + $\tilde\chi\circ\mathrm{Ih}=\chi_{2M}$ | **(W2) = C3** ⚠ |
| (5′) | $\rho_\Lambda(\mathrm{Ih}_N(\gamma))=\tau(\kappa_{u^{-1}}(\gamma))$ | **B_FC の $n=9$ instance = C3** ⚠ |

$$ \Longrightarrow\ \mathrm{ord}\bigl([u_9^{-1}]_{18}\bigr)\ \Bigm|\ 9. $$

> **⚠ I-13 の主張の訂正(自認材料)**: I-13 は「C4 = 補題 R(3)+HF-1+K5-1 の組立・**新規導出ゼロ**」とした。**新規導出がゼロなのは正しい**が、**C4 は C3 から独立に閉じない** — 補題 R の第 3 段は **(5′) と (W2) を呼ぶ**。**したがって Route 1 の C4 は「C3 が閉じれば自動」という従属項目**であって、独立に消せる残件ではない。

### 2.2 等価な言い換え — **C4 $\iff$ $u_9$ が $F_9$ の平方**

$F_9=\mathbb Q(\zeta_{36})$、$v_9=u_9^{-1}$、$a_9=[v_9]_{18}$。$\mu_9\subset F_9^{\times2}$($\zeta_9=\zeta_{36}^4=(\zeta_{36}^2)^2$)より
$$ \mathrm{ord}(a_9)\mid9\iff v_9^9\in F_9^{\times18}\iff v_9\in\mu_9\cdot F_9^{\times2}=F_9^{\times2}\iff \boxed{\ u_9\in F_9^{\times2}\ } $$

**整合確認($K^{(3)}$ で)**: $u_3=-4=(2i)^2$、$i=\zeta_{12}^3\in F_3$ ⇒ $u_3\in F_3^{\times2}$ ✓。これは appendixA の実測 $\mathrm{ord}([u_3^{-1}]_6)=3\mid3$ と整合する ✓。**$u$ の値そのものではなく「平方かどうか」だけを見ており、$K^{(3)}$ の値は公開量である。**

### 2.3 **Route 2 — tower 関係から C4 は無償で出る**(本メモの新結果)

`t63_reconnaissance_v1.md` の (T): $u_n=u_d\,w^{2d}$($w\in F_n^\times$)。$d=3,n=9$ で
$$ u_9=u_3\,w^{6}=(-4)\,w^6=(2i)^2\,(w^3)^2=\bigl(2i\,w^3\bigr)^2\ \in\ F_9^{\times2}. $$

> ### 命題 C4-T
> **(T)**($d=3,n=9$)**と $u_3=-4$ の下で $u_9\in F_9^{\times2}$、すなわち $\mathrm{ord}(a_9)\mid9$。**
> **⇒ (5′) も (W2) も使わない。**

$$ \boxed{\ \textbf{T63-P1 は (6.3) を既に仮定しているので、その文脈では C4 は\textbf{追加仮定にならない}。}\ } $$

> **⚠ 封印姿勢の申告**: 命題 C4-T は「$u_9$ は $F_9$ の平方である」という **$u_9$ についての情報**を(条件つきで)導く。**測定ではなく (T) からの演繹**であり、未知量 $w$ を含む形でしか $u_9$ に触れていない($u_9$ の値も $a_9$ の位数も本メモは決めない — 後者は t63 memo の T63-P1 が別途扱う)。**T63-P1 と同じ予言先行(pre-registration)の身分**として扱われたい。**封印 3 量($u_9/a_9$ の値・$c$ 平方類・$\hat c_\mu$)の実データには一切接触していない。**
>
> **★ 効き目**: t63 memo の予測 T63-P1 は「(6.3-cls) と C1–C4 が成立するなら…」という条件だったが、**C4 は C1+(6.3) から従うので条件から落ちる**。残る条件は **C1((6.3) の下段窓が $H^{\rm fun}$ か)・C2(本メモで閉鎖)・C3・G3(便 75 F3.2 で PAPER-PROOF 済)** に整理される。
> **⚠ ただし Route 2 は C1 を相続する** — $u_3=-4$ が $H_3^{\rm fun}$ 窓の値でなければ (T) の下段が違う。**C1 は依然として最優先。**

### 2.4 C4 の判定

| Route | 前提 | 判定 |
|---|---|---|
| **Route 1**(補題 R 段 3) | (5′)+(W2)[C3]+K5-1+HF-1+$e=9$ | **C3 が閉じれば自動**(独立には閉じない) |
| **Route 2**(tower) | (T)/(6.3)+$u_3=-4$[C1] | **T63-P1 の文脈では無償** |

$$ \boxed{\ \textbf{C4 は「独立に閉じる残件」ではなく、C3 または (6.3) のいずれかに従属する記帳項目である。}\ } $$

---

## 3. C3 に正確に残るもの — inventory(**対象外だが誰が何を供給するかを一覧化**)

| # | 項目 | 供給者 | 状態 |
|---|---|---|---|
| I1 | **(W1)** $\alpha^{\rm std}_\gamma(\bar N_9)=\bar N_9$ | **本メモ §1**(Thm 4.3 + (CAL)) | **閉** |
| I2 | **(W3)(W4)** $N_{P_9}(H_9^{\rm fun})=H_9^{\rm fun}$・$\langle X\rangle$ 単純推移・$[P_9:H_9]=18$ | **HF-1**(証明済) | **閉** |
| I3 | **(W5)** $\Lambda_9$ の $\Phi(\mathfrak F_0)$-安定 | **便 75 F2**(現物確認済: 「$\mathrm{GT}(K^{(9)})=108$、W5、W3-22/23 は cross-checked」「(W3)(W4)(W5) は UNKNOWN ではない」) | **閉(cross-checked)** |
| I3′ | $\lvert\mathrm{GT}(K^{(9)})\rvert=108$ | 便 75 F2 | **閉**。正典の導出値 $2n_0\varphi(n_0)$($\alpha=0$)$=2\cdot9\cdot6=108$ と一致(D1 §4)— **I6 の検分に使える較正点** |
| I4 | **(6′-ii)** $\rho_0$ 忠実・$\rho_0(\mathfrak F_0)=\tau(\mu_M[e])$ | **命題 K5-1**(W3-15①・全奇 $n$) | **閉** |
| I5 | **(CAL)** $\alpha^{\rm Ih}=\alpha^{\rm std}$ | $A_5$ v4 §1.4 | **閉**(窓非依存) |
| **I6** | **(W2)** $1\to\mathfrak F_0\to\mathrm{GT}(K^{(9)})\to(\mathbb Z/18)^\times\to1$ 完全・$\tilde\chi\circ\mathrm{Ih}=\chi_{18}$ | **正典 Thm 4.3 (4.12) + $K_{\rm ord}^{(n)}=\mathrm{lcm}(n,2)=2n$**(D1 §3)からの読み取り | **OPEN**。**族閉鎖の見込みあり**(候補)— 要検分 |
| **I7** | $\mathfrak F_0\cong C_n$・$e=n$ | 正典(便 29 (6.1)) | **OPEN(転記確認のみ)** |
| **I8** | **(5′) の $n=9$ instance**(B_FC) | I1–I7 + (TB1)(TB3)(TB4$^{\rm u}$) + $(Z_{36}$-link$)$ を B_FC 定理 B-7 へ投入 | **OPEN(本体)** |
| **I9** | $(Z_{36}$-link$)$ と window inventory の `K9` 行 | `Z-norm-seal/v1` §1(4) の migration/compatibility certificate | **OPEN**(現状 `not_assessed`) |
| **I10** | **(E-iv)** 命名規約 $\tau(\zeta_{18}^{\rm Rule})=\tau(X_9)$ | family Rule 1(I-2 残留・便 73 Q3.3) | **OPEN** |
| I11 | **A3** framework gate | 全窓共通・文献要請 13(ii) | **未閉**(別線) |

> **⇒ C3 の実質は I6・I7・I8・I9・I10 の 5 項**。うち **I6・I7 は正典の読み取り**、**I9 は手続き(seal)**、**I10 は条項起草**、**I8 だけが数学の合成**である。
> **⇒ I6 についての所見(候補・未検証)**: Thm 4.3 (4.12) は $\mathrm{GT}(K^{(n)})$ を $m\in\mathcal X_n$ と $k$ で**明示的に**与え、$\mathcal X_n=\{m:\gcd(2m+1,K_{\rm ord}^{(n)})=1\}$、$K_{\rm ord}^{(n)}=2n$($n$ 奇)。$\tilde\chi:(m,f)\mapsto2m+1$ の像と核がこの式から直接読めるはずで、**(W2) も全奇 $n$ で族閉鎖する見込みがある**。ただし $m\mapsto2m+1$ の $\bmod\ 2n$ での多重度(2 対 1 になる可能性)を**実際に確かめていない**ので **UNKNOWN**。**この確認は安価で、閉じれば C3 が I8・I9・I10 に縮む。**

---

## 4. まとめ(4 行)

1. **C2 は閉鎖**。2405.11725 **Thm 4.3(p.18)の isolated 性(全 $n\ge3$)** + **(CAL)** で **(W1-fam)** が出る。**新規の証明義務はなく、$\bar\iota$ も族条項も要らない**(root-normalization-free)。便 75 F3.2 の G3 が要求する**両段($d=3$ と $n=9$)の (W1) を同時に供給**する。
2. **C4 は「独立に閉じる残件」ではない**。Route 1(補題 R 段 3)は **(5′)+(W2) を呼ぶので C3 従属**。**I-13 の「新規導出ゼロ」は正しいが「独立に閉じる」は誤り** — 自認材料として記録。
3. **ただし C4 は tower から無償で出る**(命題 C4-T): $u_9=u_3w^6=(2iw^3)^2$ が平方 ⟹ $\mathrm{ord}(a_9)\mid9$。**T63-P1 の条件から C4 が落ち、条件は C1・C2(閉)・C3・G3(済)に整理される。**
4. **C3 の実質は 5 項**(I6 (W2)・I7 $e=n$・I8 (5′) 本体・I9 $Z_{36}$-link/inventory・I10 (E-iv))。**うち I6 は Thm 4.3 (4.12) からの族閉鎖の見込みがあり、確認は安価。** 最優先は依然 **C1**(下段窓が $H^{\rm fun}$ か)。
