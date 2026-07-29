# 予想 SURJ-D4 の最小ケース — W-E-A10-9t1 窓の Ih 全射性

**状態札: candidate(裁定前・未 commit・単系統・Sol 監査前)**
起草: Claude(数学者レイヤー・Opus 5)/ 2026-07-30
設問: 司令塔委嘱(発案 010 の **I10-6** = 壁窓初の genuine 判定の試み)。委嘱 3 点 = ①分解の検証 ②定理 candidate or 障害同定 ③射程評価。

**依拠(正典・repo 内のみ・外部文献ゼロ)**
- 窓の定義データ: `search/_a13_ladder_driver_spec.md`(A10-9t1 欄)/ 実測 `search/certs/a13_ladder_W_E_A10_9t1_20260730.json`(および兄弟 3 窓の証明書)
- 正典 arXiv **2405.11725** (1.5)(1.6)(Ihara 写像)・Thm 4.3/4.6 / arXiv **2401.06870**(GTSh の定義・isolated)/ `docs/week1-定義ノート.md` §2 (3.49)(3.53)・§3($\chi_{\rm vir}$・$N_{\rm ord}$・charming・isolated)
- `docs/week4-BFC攻略_opus_v2.md`(BFC v2.15)§3 **(W1)–(W5)**・§6 定理 B-4・§7 補題 B-5・§9 定理 B-7 = **(5′)**
- `docs/week4-K3飽和_opus_v3.md` §5.2.2 = **定理 $R^{\rm cyc}_{\rm formal}$**(W3-13)/ `docs/notes/w2fam_v1.md` §3・補題 L / `docs/notes/w2arith_v1.md` §2 Route A
- `docs/week4-A5算術飽和_v4.md`(**定理 A₅** = W3-8: $\mathrm{Ih}_{N_A}\twoheadrightarrow F_{20}$・固定体 $\mathbf Q(\zeta_5,\sqrt[5]{2})$)
- `docs/week3-PSL封印計算_opus_v1.md` §4.1 と `docs/week4-E2作戦_v1.md` の isolated 表(**S4 = PSL(2,8)・k=9・$\mathrm{GT}(N)\cong\mathrm{Hol}(\mathbf Z/9)$・位数 54・settled 54/54**)/ W3-6・W3-7
- `ideas/ideas_010_conjectures.md` I10-6(**未監査の発案**・司令塔許可により参照)

> ## 封印遵守
> 封印量($u$ の非公開成分・$c$ 平方類・$\hat c_\mu$・$K^{(5)}$)に一切触れない。使用した $u$ は公開値 2 つ($K^{(3)}$ の $u_3=-4$、$A_5$ の $u^{-1}=-2$)のみで、いずれも本稿では**先例の形を示すため**にしか使わない。$K^{(5)}$ は非接触。

---

## 0. 判定(先に 7 行)

$$\boxed{\ \textbf{結論 = 条件付き。①は無条件で YES・②は UNKNOWN。しかも②は「未解決」ではなく「装置が構造的に存在しない」。}\ }$$

1. **発案の分解は正しい。** ①χ̃ 方向 / ②核方向 への分解は成立し、**①は無条件かつ窓非依存に閉じる**(§2 補題 SURJ-Split)。「円分指標の全射性から従う」という発案の読みは正確である。
2. **①の帰結**: $\mathrm{Ih}(G_{\mathbf Q})\cdot\ker\tilde\chi=\mathrm{GTSh}$。ゆえに **全射 ⟺ $\mathrm{Ih}(G_{\mathbf Q(\zeta_9)})=\ker\tilde\chi\cong C_9$**。像の候補は位数 **6・18・54** の 3 つだけ(§3)。
3. **②の正確な形**: $\mathrm{Ih}|_{G_{\mathbf Q(\zeta_9)}}:G_{\mathbf Q(\zeta_9)}\to\mathbf Z/9$ は**連続指標**で、$\mathrm{Gal}(\mathbf Q(\zeta_9)/\mathbf Q)$ 共役について $\tilde\chi$-同変(捻れ指数 $a\in\{\pm1\}$)。$a=+1$ なら **Kummer 類そのもの**。全射 ⟺ その位数が 9 ⟺ 固定体が $\mathbf Q(\zeta_9)$ の 9 次巡回拡大。
4. **★ 障害の同定(本稿の主結果)**: この窓では $u$ を同定する装置(BFC 橋 (5′)・$R^{\rm cyc}_{\rm formal}$)が**適用できない**。理由は前件の未確認ではなく、**(W4) を満たす窓 $H$ が存在しないから**である: $P\cong A_{10}$、$M=\mathrm{ord}(\bar x)=9$、$A_{10}$ は指数 9 の部分群を**もたない**($\lvert A_{10}\rvert=1814400>9!=362880$)。**(W4) は空集合上の条件**である(§4・命題 W-OBS)。
5. **★ 一般化**: 同じ勘定が梯子 4 窓すべて($n=10,11,12,13$・$M=9$)で成立する。さらに構造的に、**尾部 $t\ge1$ こそが (W4)(cusp の全分岐)を壊す当のもの**である。$\bar x=(\ell,1^t)$ 型なら $M=\ell=n-t<n$。**壁を登る操作($t$ を増やす)と橋の適用可能性は排他**(§4.3)。
6. **★ 転送先(実行可能な代案)**: **同じ抽象群 $\mathrm{Hol}(\mathbf Z/9)$・同じ $M=e=9$・同じ $K_0=\mathbf Q(\zeta_9)$ をもち、しかも (W3)(W4) を満たす窓が既に台帳にある** — **S4 = PSL(2,8)・$k=9$**(位数 504、$H=$ Borel、$[P:H]=9=M$)。**I10-6 の最小テストケースは壁窓ではなく S4 に置くべき**(§5)。
7. ⟹ **定理 candidate として起草できるのは「補題 SURJ-Split(窓非依存)+ ①」まで**。SURJ-D4 の本体は本窓では起草不可(§7)。

---

## 1. 窓データと $\mathrm{GTSh}$ の同定

### 1.1 実測(証明書からの転記・司令塔許可済)

`search/certs/a13_ladder_W_E_A10_9t1_20260730.json`(driver = `search/strike-a13-ladder.g`・canonical-id SHA `6092f5f0…3f4b` が spec 表と一致・stage1 全 14 assert PASS)より:

| 欄 | 値 |
|---|---|
| $\bar x=a_1$ 側の marking | $\mathrm{ord}(\bar x)=9$、$\mathrm{ord}(\bar y)=9$、$\mathrm{ord}(\bar c)=1$($c\in N$) |
| $N_{\rm ord}$ | $\mathrm{lcm}(9,9,1)=\mathbf 9$ |
| $E=B_3/N$ | $\lvert E\rvert=6\lvert A_{10}\rvert=10886400$ |
| $P=\ker(E\to S_3)$ | $\lvert P\rvert=\lvert A_{10}\rvert$、$P\lneq\ker(\mathrm{pr}_2)=S_{10}$ |
| charming $m$ | 6 個 $=\varphi(18)$ |
| $\lvert\mathrm{GTSh}(N,N)\rvert$ | **54**、IdGroup $[54,6]$ |
| $\ker\tilde\chi$ | $C_9$(位数 9)、$\mathrm{Syl}_2=1$ |
| $\tilde\chi$ の像 $Q$ | 位数 **6**、$\cong C_6$ |
| $Q\to\mathrm{Aut}(A)$ | **忠実**(欄 10) |
| 補群 | `compl_classes_all = 1`(分裂) |
| settled | `settled_fail_count = 0`(shadow_total 54) |
| 較正ゲート | 欄 26 $=$ 欄 27(naive 経路と $\Xi$-制限経路の shadow digest 一致) |

### 1.2 群の同定(紙)

> **補題 1.1.** $P\cong A_{10}$、かつ $\bar x$ は $A_{10}$ の 9-巡回(1 点固定)である。

**証明.** $\lvert P\rvert=\lvert A_{10}\rvert$ かつ $P\lneq S_{10}$ より $[S_{10}:P]=2$。$S_{10}$ の指数 2 の部分群は $A_{10}$ ただ一つ(指数 2 は正規、商 $C_2$ は符号写像に一致)。$\mathrm{ord}(\bar x)=9$ で $\bar x\in A_{10}\le S_{10}$、spec の $w_0=(1,2,\dots,9)$ と整合。9-巡回の符号は $(-1)^8=+1$ ゆえ偶、$A_{10}$ に属する ✓。$\blacksquare$

> **補題 1.2.** $\mathrm{GTSh}(N,N)\cong\mathrm{Hol}(\mathbf Z/9)=C_9\rtimes\mathrm{Aut}(C_9)$、位数 54。

**証明.** 測定より $K:=\ker\tilde\chi\cong C_9$、$Q:=\tilde\chi(\mathrm{GTSh})\cong C_6$、拡大は分裂(`compl_classes_all`$\,=1>0$)、$Q\to\mathrm{Aut}(K)$ は忠実。$\mathrm{Aut}(C_9)\cong(\mathbf Z/9)^\times\cong C_6$ ゆえ忠実な $C_6$ 作用は**全 $\mathrm{Aut}$** に一致する。したがって $\mathrm{GTSh}\cong C_9\rtimes\mathrm{Aut}(C_9)=\mathrm{Hol}(\mathbf Z/9)$、位数 $9\cdot6=54$ ✓。$\blacksquare$

**水準の勘定**(検算済・§0 の script): $N_{\rm ord}=9$、$2N_{\rm ord}=18$、$\varphi(18)=6$、charming $m\in\{0,2,3,5,6,8\}$(6 個)、$K_0:=\mathbf Q(\zeta_{2N_{\rm ord}})=\mathbf Q(\zeta_{18})=\mathbf Q(\zeta_9)$、$[K_0:\mathbf Q]=\varphi(9)=6$、$e:=\lvert\ker\tilde\chi\rvert=9$、$\lvert\mathrm{GTSh}\rvert=e\cdot\varphi(2N_{\rm ord})=9\cdot6=54$ ✓(実測と一致)。

> **★ 註(用語の正確化)**: $\mathbf Q(\zeta_{18})=\mathbf Q(\zeta_9)$($18=2\cdot9$、$-\zeta_9^5=\zeta_{18}$)。以後 $K_0:=\mathbf Q(\zeta_9)$ と書く。**これは $M=\mathrm{ord}(\bar x)=9$ に対する BFC の $K=\mathbf Q(\zeta_{2M})$ と同じ体である。**

---

## 2. 分解の検証(委嘱 1)— 補題 SURJ-Split と ① の無条件証明

発案 I10-6 の分解を、**窓非依存の補題**として書き下す。ここが本稿で唯一「定理 candidate」として起草できる部分である。

### 2.1 窓非依存の分解補題

$N$ を charming target とし、$G:=\mathrm{GTSh}(N,N)$、$\nu:=N_{\rm ord}$、$K:=\ker\tilde\chi$、$Q:=\tilde\chi(G)$ と置く。ここで
$$\tilde\chi:\ G\longrightarrow(\mathbf Z/2\nu)^\times,\qquad [m,f]\longmapsto 2m+1\ \ (\mathrm{mod}\ 2\nu)$$
は $\chi_{\rm vir}$ の**細水準版**である(`w2fam_v1.md` §3.1・§4 の水準の罠)。

> ### 補題 SURJ-Split(窓非依存)
> $N$ が isolated(⟹ $\mathrm{Ih}_N:G_{\mathbf Q}\to G$ が定義される)とする。このとき
> **(a)【well-defined・準同型】** $\tilde\chi$ は well-defined な群準同型で、値は単元。
> **(b)【算術半】** $\ \tilde\chi\circ\mathrm{Ih}_N=\chi_{2\nu}$(mod $2\nu$ 円分指標)。
> **(c)【商方向の全射性】** $\chi_{2\nu}:G_{\mathbf Q}\to(\mathbf Z/2\nu)^\times$ は全射。ゆえに
> $$\tilde\chi\bigl(\mathrm{Ih}_N(G_{\mathbf Q})\bigr)=(\mathbf Z/2\nu)^\times .$$
> **(d)【$Q$ は強制される】** とくに $Q=(\mathbf Z/2\nu)^\times$ が**自動**で従う(仮定ではない)。
> **(e)【分解】** $\ \mathrm{Ih}_N(G_{\mathbf Q})\cdot K=G$、したがって
> $$\boxed{\ \mathrm{Ih}_N\ \text{全射}\iff \mathrm{Ih}_N\bigl(G_{K_0}\bigr)=K,\qquad K_0:=\mathbf Q(\zeta_{2\nu}).\ }$$
> **(f)【指標化】** $K$ がアーベルなら $\mathrm{Ih}_N|_{G_{K_0}}:G_{K_0}\to K$ は連続準同型であり、$\gamma\in G_{\mathbf Q}$ による共役について
> $$\mathrm{Ih}_N(\gamma\delta\gamma^{-1})=\mathrm{Ih}_N(\gamma)\,\mathrm{Ih}_N(\delta)\,\mathrm{Ih}_N(\gamma)^{-1}\qquad(\delta\in G_{K_0})$$
> が成り立つ、すなわち $\mathrm{Ih}_N|_{G_{K_0}}$ は $\chi_{2\nu}$ を通じた $Q$-作用について**同変**である。

**証明.**
**(a)** 代表の取り替え $m\mapsto m+\nu$ で $2(m+\nu)+1=(2m+1)+2\nu\equiv2m+1\ (2\nu)$ ✓ well-defined(**$\nu$ の偶奇に依らない** — `w2fam` §3.1 の議論は $n$ 奇に特有ではない)。準同型性は合成則 (3.53) の第一成分 $2m_1m_2+m_1+m_2$ と**整数恒等式** (3.49)
$$2(2m_1m_2+m_1+m_2)+1=(2m_1+1)(2m_2+1)$$
から従い、法を取る順序に依存しない。値が単元であること: charming より $\gcd(2m+1,\nu)=1$、$2m+1$ は奇数ゆえ $\gcd(2m+1,2)=1$、したがって $\gcd(2m+1,2\nu)=1$ ✓。
**(b)** 正典 2405 **(1.5)**: $\mathrm{Ih}(\gamma)=\bigl(\tfrac{\chi(\gamma)-1}{2},\ f_\gamma\bigr)$($\chi$ は完全円分指標・$\chi(\gamma)\in\hat{\mathbf Z}^\times$ は奇ゆえ $\tfrac{\chi(\gamma)-1}{2}\in\hat{\mathbf Z}$)。$N$ での shadow の第一成分は $m_\gamma:=\tfrac{\chi(\gamma)-1}{2}\bmod\nu$。任意の代表 $m_\gamma+\nu t$ に対し
$$2(m_\gamma+\nu t)+1=\chi(\gamma)+2\nu t\equiv\chi(\gamma)\pmod{2\nu}.$$
**還元の曖昧さ $\nu$ がちょうど倍されて $2\nu$ に吸収される**(`w2arith_v1.md` 補題 L と同一の機構)。ゆえに $\tilde\chi(\mathrm{Ih}_N(\gamma))=\chi(\gamma)\bmod2\nu=\chi_{2\nu}(\gamma)$ ✓。
**(c)** $\mathrm{Gal}(\mathbf Q(\zeta_{2\nu})/\mathbf Q)\xrightarrow{\sim}(\mathbf Z/2\nu)^\times$(円分体の標準事実 — $\Phi_{2\nu}$ の $\mathbf Q$ 上既約性)。
**(d)** (c) より $(\mathbf Z/2\nu)^\times=\tilde\chi(\mathrm{Ih}(G_{\mathbf Q}))\subseteq\tilde\chi(G)=Q\subseteq(\mathbf Z/2\nu)^\times$、両端が一致するので全て等号。
**(e)** $\tilde\chi$ が $\mathrm{Ih}(G_{\mathbf Q})$ 上で既に全射だから $\mathrm{Ih}(G_{\mathbf Q})K=G$。$H:=\mathrm{Ih}(G_{\mathbf Q})$ とすると $H=G\iff H\supseteq K\iff H\cap K=K$。他方 $\mathrm{Ih}(\gamma)\in K\iff\chi_{2\nu}(\gamma)=1\iff\gamma\in G_{K_0}$ ゆえ $H\cap K=\mathrm{Ih}(G_{K_0})$ ✓。
**(f)** $\mathrm{Ih}_N$ は群準同型で $K\trianglelefteq G$、制限と共役の式は準同型性そのもの。$\blacksquare$

### 2.2 本窓への適用 — **① は無条件で YES**

$\nu=9$、$2\nu=18$、$K_0=\mathbf Q(\zeta_9)$、$K\cong C_9$、$Q\cong(\mathbf Z/18)^\times\cong C_6$。

> ### 系 2.2(①の確定)
> **$\tilde\chi\circ\mathrm{Ih}_N=\chi_{18}$ は全射**であり、$\mathrm{Ih}_N(G_{\mathbf Q})\cdot C_9=\mathrm{Hol}(\mathbf Z/9)$。すなわち
> $$\boxed{\ \textbf{商方向}\ \mathrm{Hol}(\mathbf Z/9)\twoheadrightarrow C_6\ \textbf{は genuine(無条件)}.\ }$$
> さらに実測の $Q$ の位数 6 は**理論から強制される値**であり(補題 (d))、証明書の欄 8 はこの理論の**較正**として読むのが正しい(独立情報ではない)。

**⟹ 委嘱 1 への回答: 発案 I10-6 の「①は円分指標の全射性から従う」は正しい。** しかも $K^{(n)}$ 族に固有ではなく、**任意の isolated 窓で成立する**(補題 SURJ-Split は窓データを一切使わない)。

### 2.3 残る問い ② の正確な形

補題 SURJ-Split (e)(f) より、残るのは
$$c:=\mathrm{Ih}_N|_{G_{K_0}}:\ G_{\mathbf Q(\zeta_9)}\longrightarrow K\cong\mathbf Z/9$$
という**連続指標**の位数である。$Q\cong C_6$ が $K\cong\mathbf Z/9$ に忠実に作用する(実測欄 10)ので、その作用は同型 $(\mathbf Z/18)^\times\xrightarrow{\sim}\mathrm{Aut}(\mathbf Z/9)=(\mathbf Z/9)^\times$ を与える。両者は還元により標準的に同型で、$\mathrm{Aut}(C_6)=\{\pm1\}$ ゆえ

$$\boxed{\ \gamma\in G_{\mathbf Q},\ \delta\in G_{K_0}\ \Longrightarrow\ c(\gamma\delta\gamma^{-1})=\chi_9(\gamma)^{a}\cdot c(\delta),\qquad a\in\{+1,-1\}.\ }$$

* **$a=+1$ の場合**: $c\in\mathrm{Hom}(G_{K_0},\mu_9)$ が $G_{\mathbf Q}$-同変、すなわち **Kummer 類**。$\mu_9\subset K_0$ ゆえ Kummer 理論 $H^1(G_{K_0},\mu_9)\cong K_0^\times/K_0^{\times9}$ により、**一意の $[u]\in K_0^\times/K_0^{\times9}$ が対応**し
 $$\mathrm{Ih}_N\ \text{全射}\iff\mathrm{ord}\bigl([u]_9\bigr)=9\iff u\notin K_0^{\times3},$$
 固定体は $K_0(u^{1/9})$(9 次巡回)。**これは $R^{\rm cyc}_{\rm formal}$(W3-13)の主張と逐語同型**($M=e=9$ ゆえ「$\mathrm{ord}([u^{-1}]_M)=e$」がそのまま「位数 9」)。
* **$a=-1$ の場合**: $c\in H^1(G_{K_0},(\mathbf Z/9)(-1))$ の同変類。形は同じ(9 次巡回拡大)だが $u$ の同定則が Tate 捻れ分ずれる。

> **⚠ $a$ は未測定である。** 証明書の欄 10 は**忠実性**しか記録しておらず、**捻れ指数 $a$ は記録していない**。$K^{(n)}$ 族では $\Phi\vert_A=\mathrm{diag}(u,u,\dots)$(ODD-H §11.1)より $a=+1$ であるが、**本窓では確認していない**。$a$ の決定は **GAP 1 行**(生成元の共役作用が $\ker\tilde\chi$ 上で $u$ 倍か $u^{-1}$ 倍か)であり、§9【SD-c】で発注を提案する。$a$ が何であれ §3 以降の議論は変わらない。

### 2.4 像の可能性は 3 つに限られる

$c$ の位数は $1,3,9$ のいずれか($\mathbf Z/9$ の部分群は $1,C_3,C_9$)。$H:=\mathrm{Ih}(G_{\mathbf Q})$ の位数は補題 SURJ-Split (e) より $6\cdot\lvert\mathrm{im}\,c\rvert$:

| $\mathrm{ord}(c)$ | $\lvert H\rvert$ | 判定 |
|---|---|---|
| 1 | **6** | 非全射(像 $\cong C_6$・genuine 率 $6/54=1/9$) |
| 3 | **18** | 非全射(像 $\cong C_3\rtimes C_6$・genuine 率 $1/3$) |
| 9 | **54** | **全射 = genuine** |

**⟹ 未知は「$\log_3$ で 2 ビット」ちょうどである。** これが I10-6 の問いの正確な情報量である。

---

## 3. 先例の形($u$ が何であるべきか)

$M=e$ 型の窓で $\mathrm{Ih}$ 全射が**実際に証明された**先例は 2 つあり、いずれも本窓と同じ形をしている:

| 窓 | $P$ | $M=e$ | $K_0$ | $\mathrm{GTSh}$ | 判定 | 固定体 | 台帳 |
|---|---|---|---|---|---|---|---|
| $A_5$ 窓 $N_A$ | $A_5$ | 5 | $\mathbf Q(\zeta_5)$ | $F_{20}=\mathrm{Hol}(\mathbf Z/5)$ | **全射** | $\mathbf Q(\zeta_5,\sqrt[5]2)$($u^{-1}=-2$) | **W3-8** |
| $K^{(3)}$ | $G_3$(位数 108) | 6 | $\mathbf Q(\zeta_{12})$ | $S_3\times C_2$ | **全射** | $\mathbf Q(\zeta_{12},\sqrt[3]2)$($u=-4$) | **W3-11** |
| **本窓** | $A_{10}$ | 9 | $\mathbf Q(\zeta_9)$ | $\mathrm{Hol}(\mathbf Z/9)$ | **?** | ? | — |

$A_5$ 窓は**構造的にも最も近い**: $P$ が非可換単純群、$\mathrm{GTSh}=\mathrm{Hol}(\mathbf Z/\ell)$、$M=e=\ell$。そこでの答えは **YES**(位数 $\ell$ の Kummer 指標が満位数)。

**もし $u\in\mathbf Q^\times$ なら判定は初等になる**:

> **補題 3.1.** $u\in\mathbf Q^\times$ が有理数の 3 乗でないなら $u\notin K_0^{\times3}$、ゆえに $\mathrm{ord}([u]_9)=9$。
> **証明.** $u=y^3$($y\in K_0=\mathbf Q(\zeta_9)$)とすると $\mathbf Q(y)\subseteq K_0$ は $\mathbf Q$ 上アーベルな体の部分体ゆえ $\mathbf Q$ 上正規。$\mathbf Q(y)=\mathbf Q(u^{1/3})$ で $[\mathbf Q(u^{1/3}):\mathbf Q]=3$(仮定より $u$ は有理 3 乗でない)。正規なら共役 $\zeta_3u^{1/3}$ を含むので $\zeta_3\in\mathbf Q(u^{1/3})$、しかし $[\mathbf Q(\zeta_3):\mathbf Q]=2\nmid3$ で矛盾。$\blacksquare$($K^{(3)}$ の $2\notin F_9^{\times3}$ の論法 = t63 §5(c) と同型。)

⟹ **$u\in\mathbf Q^\times$ かつ非 3 乗 という「先例どおり」なら全射。** ただし **$u$ を出す装置がない**というのが次節である。

---

## 4. 障害の同定(委嘱 2)— **(W4) が空である**

### 4.1 $u$ を出す唯一の装置とその前件

$[u]$ を窓データから同定する装置は、本工房には 1 つしかない: **BFC 定理 B-7 = (5′)**
$$\rho_\Lambda\bigl(\mathrm{Ih}_N(\gamma)\bigr)=\tau\bigl(\kappa_{u^{-1}}(\gamma)\bigr)\qquad(\gamma\in G_{K_0})$$
と、それを受ける $R^{\rm cyc}_{\rm formal}$。その前件のうち窓固有のものは **(W1)(W2)(W3)(W4)(W5)**(BFC §3)である。とくに

> **(W3)** $H\le P$ で $N_P(H)=H$
> **(W4)** $\langle X\rangle$ が $P/H$ 上推移的、かつ $[P:H]=M$

**幾何的意味**: $\lambda^{-1}(0)$ がただ 1 点で分岐指数 $M$ の**全分岐 cusp**であること(BFC 補題 B-5(i))。$\mathrm{Fib}$ の $M$ 点 $=P/H$ の $M$ 個の剰余類。

### 4.2 本窓では (W4) を満たす $H$ が存在しない

> ### 命題 W-OBS(壁窓の窓障害)
> $P\cong A_{10}$、$M=\mathrm{ord}(\bar x)=9$。このとき **$[P:H]=M$ なる部分群 $H\le P$ は存在しない**。ゆえに **(W4) は空集合上の条件**であり、BFC 橋 (5′) も $R^{\rm cyc}_{\rm formal}$ も**この窓には適用できない**(前件が未確認なのではなく、前件を満たす対象が無い)。

**証明.** $H\le A_{10}$ が $[A_{10}:H]=9$ を満たすとする。$A_{10}$ の剰余類 $A_{10}/H$(9 個)への左移動作用は準同型 $\varphi:A_{10}\to S_9$ を与える。$\ker\varphi\trianglelefteq A_{10}$ で $\ker\varphi\subseteq H\ne A_{10}$、$A_{10}$ は単純($n\ge5$)なので $\ker\varphi=1$。よって $A_{10}\hookrightarrow S_9$、とくに
$$\lvert A_{10}\rvert=\frac{10!}{2}=1\,814\,400\ \le\ 9!=362\,880$$
となり矛盾。$\blacksquare$(検算済 — §0 の script。)

> **★ 前件の「未確認」と「空」は違う。** C-21(A7 の合成窓 instance)は「前件が族定理で供給される」型の閉鎖だった。ここは**逆**で、**前件を満たす対象が存在しない**。したがって「もっと調べれば埋まる」類の穴ではない。**装置の射程外**である。

### 4.3 一般化 — 尾部 $t$ こそが全分岐を壊す

> ### 系 W-OBS-fam(梯子全体)
> 梯子 4 窓すべて($W\text{-}E\text{-}A n\text{-}9t\tau$、$n=10,11,12,13$、$P\cong A_n$、$N_{\rm ord}=9$)で $[P:H]=9$ なる $H$ は存在しない($\lvert A_n\rvert>9!$ が $n\ge10$ で成立 — 検算済)。**梯子全体で (W4) は空。**

さらに構造を述べると:

> ### 命題 TAIL-OBS(尾部と全分岐の排他性)
> $P\cong A_n$($n\ge5$)、$\bar x$ の型が $(\ell,1^t)$($n=\ell+t$、$\ell$ 奇)で $M=\mathrm{ord}(\bar x)=\ell$ とする。$t\ge1$ ならば $M=\ell=n-t<n$ であり、$A_n$ は指数 $<n$ の真部分群をもたない(上の論法: $\lvert A_n\rvert\le(n-1)!$ は $n\ge5$ で偽)。ゆえに **$t\ge1$ の全窓で (W4) は空**。$t=0$(= $\bar x$ が $n$-巡回・cusp が全分岐)のときのみ (W4) は満たされうる。

**$A_5$ 窓との差分がこれで完全に説明される**: $A_5$ は $t=0$($\bar x$ が 5-巡回・$M=5=n$)で、$H=A_4$(指数 5・自己正規化・$\langle X\rangle$ 単純推移)が実在する。**「ちょうど間に合っている」。** 本窓は $t=1$ で $M=9$、$n=10$ — **1 だけ足りない**。

$$\boxed{\ \textbf{壁を登る操作(尾部 }t\textbf{ を伸ばして }\mathrm{Syl}_2(S_t)\textbf{ を稼ぐ)と、橋の適用可能性((W4) = cusp 全分岐)は排他である。}\ }$$

> **⚠ 射程の限定(誇張しない)**: 命題 TAIL-OBS が言うのは「**BFC が現在採用している全分岐型の窓パッケージ**が使えない」ことだけである。「$\mathrm{Ih}$ が全射でない」ことは**一切含意しない**。全射性そのものは **UNKNOWN のまま**である(§2.4 の 3 択が生きている)。

### 4.4 他の前件の状況(記録)

障害が (W4) に単離されたことを示すため、残りも記帳する。

| 前件 | 本窓での状況 |
|---|---|
| **(W1)** isolated | ✅ 候補: `settled_fail_count = 0`(54 shadow 全 settled)。**単系統 GAP・isolated の定義(全 charming pair の target が $N$)との突合は要確認**(§9【SD-a】) |
| **(W2)** 群論半 | ✅ 実測(核 $C_9$・像 6 = $\varphi(18)$)。**算術半は補題 SURJ-Split (b) で無条件**(窓非依存) |
| **(W3)** $N_P(H)=H$ | — **(W4) が空なので問う対象がない** |
| **(W4)** 全分岐・$[P:H]=M$ | ❌ **空**(命題 W-OBS) |
| **(W5)** $\Lambda$ の $\Phi(\mathfrak F_0)$-安定 | — 同上。ただし $\Phi(\mathfrak F_0)$ が内部自己同型なら自動(Sol 便 73 (1.13)(1.14) の論法は $\Lambda$ が共役類でありさえすれば効く) |
| (CAL)・(TB1)–(TB4$^{\rm u}$) | 枠組(全窓共通・retained) |

⟹ **障害は (W4) ただ 1 点に単離された。**

---

## 5. 転送先 — S4(PSL(2,8)・$k=9$)が構造的に正しい最小テストケース

### 5.1 発見

`docs/week3-PSL封印計算_opus_v1.md` §4.1 と `docs/week4-E2作戦_v1.md` の isolated 表より:

> **S4 = PSL(2,8) の $k=9$ 窓**: $\lvert\mathrm{GT}(N)\rvert=\mathbf{54}$、**$\mathrm{GT}(N)\cong\mathrm{Hol}(\mathbf Z/9)$**(= $N_{\mathrm{P\Gamma L}(2,8)}(\langle X\rangle)$)、`isolated: true`、settled 54/54(6 層 × 各 9)、$n_m$ 一様 $=9$。台帳 **W3-6**(封印予測 7/7 完全一致・二系統 cross-checked)・**W3-7**(七窓統一定理・case A)。

すなわち **$\mathrm{Hol}(\mathbf Z/9)$ を $\mathrm{GTSh}$ にもつ窓は既に台帳にある**。「$\mathrm{Hol}(\mathbf Z/9)$ が裸で出た初の窓」ではない(**「初の D4 型窓」という限定つきなら正しい**)。

### 5.2 S4 では (W3)(W4) が満たされる

> **命題 5.2.** $P=\mathrm{PSL}(2,8)$、$M=9$、$H:=$ Borel(点安定化群)とすると **(W3)(W4) が成立**する。

**証明.** $\lvert\mathrm{PSL}(2,8)\rvert=8\cdot9\cdot7=504$。$\mathbf P^1(\mathbf F_8)$ は 9 点、$P$ はその上に 3 重可移に作用し、点安定化群は Borel $B=\mathbf F_8\rtimes C_7$(位数 $8\cdot7=56$)。$[P:B]=504/56=\mathbf 9=M$ ✓(検算済)。$B$ は $\mathrm{PSL}(2,q)$ の極大部分群で自己正規化 ⟹ **(W3)** ✓。位数 9 の元 $X$ は非分裂トーラス($q+1=9$)の生成元で、$\mathbf P^1(\mathbf F_8)$ 上に**固定点をもたない**(固有ベクトルが $\mathbf F_8$ 上に無い)。9 点上で固定点自由な位数 9 の元は軌道長 9、すなわち**単純推移** ⟹ **(W4)** ✓。$\blacksquare$

さらに $e=\lvert\ker\tilde\chi\rvert=54/6=9=M$、$K_0=\mathbf Q(\zeta_{18})=\mathbf Q(\zeta_9)$ — **本窓と数値が完全に一致する。**

### 5.3 含意

$$\boxed{\ \textbf{I10-6 の「最小テストケース」は壁窓ではなく S4 に置くべきである。}\ }$$

* S4 なら BFC 橋 (5′) と $R^{\rm cyc}_{\rm formal}$ が**原理的に適用可能**(前件 (W3)(W4) が実在)。残るのは (W1)(W2)(W5)+(CAL)+枠組と、$u$ の実抽出。
* S4 は既に **cross-checked**(W3-6・封印 7/7)で、**case A・settled 100%** も確定済み。
* $A_5$ 窓($\ell=5$)の飽和定理 W3-8 の**議論がそのまま $\ell=9$ へ横滑りする可能性が高い**(同じ case A、同じ $\mathrm{Hol}$ 型、$M=e=\ell$)。
* **ただし $\ell=9$ は素数冪で素数でない** — $A_5$ 論法の「$\mu_\ell$、$\ell$ 素数」に依存する箇所($\mathrm{ord}\mid\ell$ の 2 値性など)は $\ell=9$ で 3 値($1,3,9$)になる。**そこが唯一の新規作業**であり、実は「$\ell$ 素数から素数冪へ」の一般化として本峰側にも効く(§6)。

⚠ **本節は S4 の全射性を主張していない。** 「装置が適用できる場所」を同定したにすぎない。S4 での判定には $u$ の抽出(measurement)が要る。

---

## 6. 射程評価(委嘱 3)— 本峰の手法は壁窓のどこまで届くか

### 6.1 手法の到達域(3 層に分けて)

| 層 | 内容 | 壁窓($t\ge1$)での可否 | 根拠 |
|---|---|---|---|
| **層 I: 商方向** | $\tilde\chi\circ\mathrm{Ih}=\chi_{2\nu}$ と円分の全射性 | **✅ 全窓で無条件に届く** | 補題 SURJ-Split(窓データを使わない) |
| **層 II: 核方向の形** | $\mathrm{Ih}\vert_{G_{K_0}}$ が Kummer 型指標であること・全射 ⟺ 位数 $=e$・固定体が $K_0(u^{1/M})$ | **✅ 形は届く**(核がアーベルなら) | 補題 SURJ-Split (f) + Kummer 理論。$u$ の**存在**は言えるが**同定**はできない |
| **層 III: $u$ の同定** | BFC 橋 (5′) → $R^{\rm cyc}_{\rm formal}$ | **❌ $t\ge1$ で構造的に不可** | 命題 TAIL-OBS((W4) が空) |

$$\boxed{\ \textbf{本峰の手法は壁窓に対し「層 II まで」届き、「層 III」で止まる。止まる理由は尾部 }t\ \textbf{そのもの。}\ }$$

**これは I10-6 の問い(「Syl₂(S_t) 因子はどこまで G_ℚ の像か」)への部分回答でもある**: 層 I が保証するのは $\tilde\chi$ 像(=$\mathrm{Hol}$ の商方向)だけであり、$\mathrm{Syl}_2(S_t)$ 因子は $\ker\tilde\chi$ の中(実測: $t=4$ 窓で $\ker=C_9\times D_8$)にある。**したがって「2-群因子が genuine か」は必ず層 II/III の問題**であり、層 I からは 1 ビットも出ない。発案 I10-5-3 の「2-群因子が円分を超えた最初の情報を見ている」という読みは、少なくとも**層の勘定としては整合的**である(証明ではない)。

### 6.2 層 III を壁窓へ延ばす道(研究プログラムとしての評価)

(W4) を捨てて $t\ge1$ を許すには、BFC §7 の局所理論を**全分岐でない cusp**へ一般化する必要がある。具体的に何が壊れるかを名指しする:

| BFC の段 | 全分岐が効いている箇所 | $t\ge1$ で起きること |
|---|---|---|
| 補題 B-5a | $\prod_{P\mid0}\kappa(P)((s_P))$ | **そのまま**(もともと積で書いてある) |
| 補題 B-5(i) | 「$\lambda^{-1}(0)$ はただ 1 点・$K$-有理・$e=M$」 | **崩れる**。$\bar x=(\ell,1^t)$ なら cusp は $1+t$ 点、分岐指数 $(\ell,1,\dots,1)$。$G_{K_0}$ は $t$ 個の不分岐点を置換しうる ⟹ **$K$-有理性も失う** |
| 補題 B-5(ii)(iii) | 単一の $u\in K^\times$・$T^M-u^{-1}\beta$ | **$\prod$ の各因子ごとに主係数**。全体は $\prod_P\kappa(P)((s_P))$ の中の**半局所 Kummer 類**($\kappa(P)$ たちの体の積の上のクラス) |
| 補題 B-6 | $\mathrm{Fib}\cong\Lambda$ が $\mu_M$-torsor | **torsor でなくなる**($\mu_M$ は $\ell$-軌道にしか自由に作用しない)。$\mathrm{Fib}$ は $\mu_\ell$-torsor $\sqcup$($t$ 点)という**非斉次集合** |

> ### 評価
> **難易度は「補題の一般化」ではなく「新しい局所不変量の設計」**である。必要なのは、cusp 上の点の**集合**(と $G_{K_0}$ のその上の作用)を込みにした半局所 Kummer 不変量であり、その $G_{K_0}$-作用は $\mu_\ell$-torsor 部分と置換部分の**混合**になる。$\mathrm{Syl}_2(S_t)$ 因子はまさにこの置換部分から来ているはずで、**「2-群因子の算術的正体 = 不分岐 cusp 点の Galois 置換」**という作業仮説が自然に立つ。
> **これは C-21 型の「族定理を当てるだけ」の仕事ではなく、キャンペーン級**である。

### 6.3 したがって推奨する順序

1. **S4 で $\ell=9$(素数冪・非素数)を先に通す**(§5)。$A_5$ 論法の $\ell$ 素数依存箇所を洗い出す作業になり、**副産物として本峰の混合側($n=n_0\cdot2^\alpha$)にも効く**(3 値化 $1,3,9$ の扱いは $\mathrm{ord}\mid\ell$ の一般論)。
2. その上で $t=1$ の壁窓へ **§6.2 の半局所版**を設計する。$t=1$ は「不分岐 cusp 点がちょうど 1 点」で $S_t=S_1=1$、つまり**置換部分が自明**な最小ケース — 一般化の第一歩として最適。
3. $t\ge2$($\mathrm{Syl}_2(S_t)\ne1$)は置換部分が非自明になってから。

> **★ $t=1$ 窓の本当の価値**: $\mathrm{GTSh}\cong\mathrm{Hol}(\mathbf Z/9)$ は **metabelian(導来長 2)** であり、**壁(metabelian の壁)を越えていない**。したがって本窓で全射が出ても**壁の突破にはならない**。本窓の価値は「**壁の手前で、装置が壊れる場所を正確に特定できる最小の実験台**」である — 実際、本稿はそれ((W4) の消滅)を特定した。発案 I10-6 の「dl 3 の GTSh ができても勝ちではない」という警戒は正しく、しかも**逆向きにも正しい**: **dl 2 の窓ですら、今の装置では genuine を判定できない。**

---

## 7. 定理 candidate として起草できるもの / できないもの(委嘱 2 への最終回答)

### 7.1 起草できる(本稿 §2)

> ### 補題 SURJ-Split(窓非依存)— **定理 candidate として提出**
> §2.1 の (a)–(f)。とくに **(b) $\tilde\chi\circ\mathrm{Ih}_N=\chi_{2N_{\rm ord}}$ と (e) の分解**は、**isolated な任意の窓**(dihedral・PSL・壁のすべて)で成立する。
> **証明の依存**: 正典 (1.5)(3.49)(3.53) と円分体の既約性のみ。**枠組仮定 (TB1)–(TB4) すら使わない。**
> **新規性**: 「$\chi_{\rm vir}$ の細水準版と円分指標の一致」は $K^{(n)}$ 族について `w2arith_v1.md` が示している。本稿の寄与は **(i) それが窓データを一切使わない(全窓で成立する)ことの明示** と **(ii) (d)(e) の分解形への整理**である。(grep 済: `w2arith` は「全奇数 $n\ge3$」と族限定で書かれており、窓非依存の形では述べていない。)

> ### 系(本窓の①)
> $\mathrm{Ih}_{N}(G_{\mathbf Q})\cdot\ker\tilde\chi=\mathrm{GTSh}\cong\mathrm{Hol}(\mathbf Z/9)$、かつ $\mathrm{Ih}$ 全射 $\iff$ $\mathrm{Ih}(G_{\mathbf Q(\zeta_9)})=C_9$。像の位数は $6,18,54$ のいずれか。

> ### 命題 W-OBS / 系 W-OBS-fam / 命題 TAIL-OBS(§4)— **定理 candidate として提出**
> 障害の同定。**負の結果だが完全に厳密**(単純群の指数評価のみ)で、装置の射程を確定する。

### 7.2 起草できない

> **予想 SURJ-D4 の本窓 instance(= $\mathrm{Ih}$ が全射)は起草できない。** $u$ を同定する装置が存在せず(§4)、$[u]$ の位数($1,3,9$ の 3 択)を決める独立な手掛かりも本稿では見つからなかった。
> **状態: UNKNOWN(一級の結果)。** 「探索したが判定に至らず」ではなく「**判定装置が窓の型に対して定義されない**」という型の UNKNOWN であり、範囲は §4 で厳密に画定した。

---

## 8. FINDING

| # | 種別 | 内容 |
|---|---|---|
| **SD-1** | **成立(発案の追認)** | I10-6 の ①/② 分解は正しい。**①は無条件・窓非依存に閉じる**(補題 SURJ-Split)。「円分指標の全射性から従う」は正確 |
| **SD-2** | **強化** | ①は $K^{(n)}$ 族に固有でなく **isolated な全窓**で成立。副産物として **$Q=(\mathbf Z/2N_{\rm ord})^\times$ は理論から強制**され、証明書の欄 8($=6$)は独立情報ではなく**較正**である |
| **SD-3** | **★ 障害の同定(主結果)** | 本窓で (W4) を満たす $H$ は**存在しない**($P\cong A_{10}$・$M=9$・$\lvert A_{10}\rvert>9!$)。前件の未確認ではなく**前件が空**。BFC 橋・$R^{\rm cyc}_{\rm formal}$ は**射程外** |
| **SD-4** | **★ 構造(一般化)** | **尾部 $t\ge1$ そのものが cusp の全分岐を壊す**(命題 TAIL-OBS)。梯子 4 窓すべてで (W4) は空。**壁を登る操作と橋の適用可能性は排他** |
| **SD-5** | **★ 転送先** | $\mathrm{Hol}(\mathbf Z/9)$ を $\mathrm{GTSh}$ にもつ窓は既に台帳にある(**S4 = PSL(2,8)・$k=9$**・W3-6 で cross-checked)。**S4 は (W3)(W4) を満たす**($H=$ Borel・$[P:H]=9=M$)。**I10-6 の最小テストケースは S4 に移すべき** |
| **SD-6** | **語の訂正** | 「$\mathrm{Hol}(\mathbf Z/9)$ が裸で出た初の窓」は**誤り**(S4 が先)。「**初の D4 型窓**」なら正しい。裁定 213 の文言に限定子が入っているかの確認を求める |
| **SD-7** | **射程の限定(警告)** | 本窓の $\mathrm{GTSh}=\mathrm{Hol}(\mathbf Z/9)$ は **metabelian**。全射が出ても**壁の突破ではない**。本窓の価値は「装置が壊れる場所の特定」であり、それは本稿で達成された |
| **SD-8** | **未測定の 1 ビット** | 捻れ指数 $a\in\{\pm1\}$($\ker\tilde\chi$ 上の $Q$-作用が $u$ 倍か $u^{-1}$ 倍か)が証明書に無い。GAP 1 行で決まる |
| **SD-9** | **UNKNOWN(一級)** | 本窓の全射性は **UNKNOWN**。像の位数は $6/18/54$ の 3 択(2 ビット)。範囲は §4 で厳密に画定 |

---

## 9. 未閉鎖項・次の一手

* 【SD-a】**(W1) の確認**: 証明書の `settled_fail_count = 0` が「$\mathrm{GTSh}(N,N)$ の 54 元が settled」なのか「source $N$ の**全** charming pair が settled(= isolated の定義)」なのかを judge の実装で確認。**前者だと isolated は言えず、$\mathrm{Ih}_N$ の**定義**すら怪しくなる**ので、これは補題 SURJ-Split の前提として先に潰すべき。implementer へ 1 問。
* 【SD-b】**S4 への転送(推奨・最優先)**: §5 の (W3)(W4) 成立を独立確認し、$A_5$ 飽和定理(W3-8)の論法を $\ell=9$ へ移す試み。**$\ell$ 素数依存箇所の洗い出しが本体**($\mathrm{ord}\mid\ell$ が 2 値から 3 値へ)。本峰の混合側にも効く副産物あり。
* 【SD-c】**捻れ指数 $a$ の測定**(SD-8): GAP 1 行(生成元の $\ker\tilde\chi$ 上の共役作用の指数)。$a=+1$ なら層 II が「Kummer 類そのもの」と言い切れる。
* 【SD-d】**半局所 Kummer 不変量の設計**(§6.2): $t\ge1$ 窓へ層 III を延ばす研究プログラム。**キャンペーン級**。$t=1$(置換部分が自明)から。**この項目は【文献要請】の候補**(下記)。
* 【SD-e】本稿は**紙上(paper-proof candidate)・単系統・Sol 監査前**。**Lean 検証ではない・二系統一致でもない**。実測値は証明書からの転記で、私は GAP を回していない(§0 の整数演算検算のみ scratchpad で実施)。封印量非接触・$K^{(5)}$ 非接触。

> ### 【文献要請】(SD-d に付随・新規 1 件)
> **困難**: BFC の局所段(補題 B-5)は cusp が**全分岐 1 点**であることに全面的に依存している。壁窓では cusp が $1+t$ 点(分岐指数 $(\ell,1^t)$)になり、$\mathrm{Fib}$ が $\mu_\ell$-torsor でなくなるため、torsor 類 $[u^{-1}]$ という不変量そのものが定義できない。
> **欲しい結果の型**: 「$\mathbf P^1$ 上の有限被覆の**一つの分岐点の上の繊維全体**(複数点・分岐指数がばらばら・剰余体が非自明)に対する、$G_K$-同変な**半局所 Kummer/torsor 不変量**の定式化と、それがモノドロミー・分岐データからどう読めるか」。とくに「不分岐点の $G_K$-置換」と「分岐点の Kummer 類」が**どう組み合わさって一つのコホモロジー類になるか**(半局所体 $\prod_P\kappa(P)((s_P))$ 上の $H^1$ と、その $G_K$-降下)。
> **当て**: 数論的幾何・被覆の降下理論・Grothendieck dessins の moduli field。**GT とは無関係の分野**にありそう(C-21 §11 の既出要請とは別物 — あちらは「主係数の平方類を被覆データから読む公式」、こちらは「非全分岐 cusp での不変量の**存在と定式化**」)。
> **使い道**: 層 III を $t\ge1$ へ延ばす = **壁窓の genuine 判定を可能にする**。現在これが無いために I10-6 は原理的に手が付かない。
