# 命題 SETTLED-GRP の厳密証明(L3-GAP-2・裁定 1066)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔(③ 線 再出発の土台)
前提 = `iso_family_lemma_v1.md`(SETTLE-AUTO)・定義ノート L163–173(合成 (3.53)・逆射 (3.54)・(3.49))
⚠ $u$/$c$ 非接触・prereg 非抵触。**格: candidate**(Sol 未監査)。

---

## §0 結論

$$\boxed{\ \textbf{【定理 SETTLED-GRP】}\quad GT^{\rm settled}(N):=\{\text{settled な shadow}\}\ \textbf{は }GT(N)\ \textbf{の部分群であり、}\ \Psi:[m,f]\mapsto\bar E_{[m,f]}\ \textbf{は }\mathrm{Aut}(Q)\ \textbf{への群準同型}\ }$$

**射程**: ★ **群構造と準同型性は窓一般**(任意の $N\in\mathrm{NFI}_{PB_3}(B_3)$)。
⚠★ **埋入(= $\Psi$ の単射性)は自動ではありません — 窓依存**(§5)。司令塔の発注項目のうち**ここだけが条件つき**です。

---

## §1 ★★★ 補題 COMP-E(合成則の正体)

> **【補題 COMP-E】** $E_{m,f}:F_2\to F_2$($x\mapsto x^{u}$、$y\mapsto f^{-1}y^{u}f$、$u=2m+1$)について
> $$E_{[m_1,f_1]\circ[m_2,f_2]}\;=\;E_{[m_1,f_1]}\circ E_{[m_2,f_2]}$$
> すなわち **正典の合成 (3.53) は $E$ の合成そのもの**である。

**証明**(両生成元で確認・自由群なのでこれで十分):
- $x$ 側: $E_1\!\circ\!E_2(x)=E_1(x^{u_2})=(x^{u_1})^{u_2}=x^{u_1u_2}$。(3.49) で $u$ は乗法的、実際
 $2(2m_1m_2+m_1+m_2)+1=(2m_1+1)(2m_2+1)=u_1u_2$ ✔
- $y$ 側:
$$E_1\!\circ\!E_2(y)=E_1\bigl(f_2^{-1}y^{u_2}f_2\bigr)=E_1(f_2)^{-1}\bigl(f_1^{-1}y^{u_1}f_1\bigr)^{u_2}E_1(f_2)=\bigl(f_1E_1(f_2)\bigr)^{-1}y^{u_1u_2}\bigl(f_1E_1(f_2)\bigr)$$
 ⟹ $f_{[1]\circ[2]}=f_1\,E_{m_1,f_1}(f_2)$ と**完全一致**(= (3.53) の右辺)✔ ∎

★ **機械検算**: 自由群の乱択語 300 本($u\in\{1,3,5,7\}$・$f$ 長さ 0–4・$w$ 長さ 0–6)で **300/300 一致** ✔

---

## §2 補題 SETTLE-AUT(判定の言い換え)

$\pi:F_2\to Q:=F_2/N_{F_2}$、$\phi_{[m,f]}:=\pi\circ E_{[m,f]}:F_2\to Q$(準同型)。

> **【補題 SETTLE-AUT】** shadow $[m,f]$ について
> $$\textbf{settled}\iff \ker\phi_{[m,f]}=N_{F_2}\iff E_{[m,f]}(N_{F_2})\subseteq N_{F_2}\iff \bar E_{[m,f]}\in\mathrm{Aut}(Q).$$

**証明**: 便 121 A7.1 より $\pi_{S_3}\circ T=\pi_{S_3}$ ⟹ $\ker T\subset PB_3$、$N\subset PB_3$ ゆえ settled($\ker T=N$)は $F_2$ 水準の $\ker\phi=N_{F_2}$ と同値。
shadow は全射性を含む ⟹ $\phi$ は $Q$ へ全射。$N_{F_2}\subseteq\ker\phi$ なら $\bar E:Q\to Q$ が定まり全射 ⟹ $Q$ 有限ゆえ**単射** ⟹ $\ker\phi=N_{F_2}$。逆は自明。∎(= SETTLE-AUTO)

---

## §3 群構造の証明(4 点・逐語)

### 3.1 単位
$[0,1]$: $u=1$、$f=1$ ⟹ $E_{[0,1]}=\mathrm{id}_{F_2}$ ⟹ $E(N_{F_2})=N_{F_2}$ ⟹ well_defined、$\bar E=\mathrm{id}_Q\in\mathrm{Aut}(Q)$ ⟹ ★ **$[0,1]$ は settled** ✔

### 3.2 閉性(合成)
$[1],[2]$ settled ⟹ $E_i(N_{F_2})\subseteq N_{F_2}$。COMP-E より
$$E_{[1]\circ[2]}(N_{F_2})=E_1\bigl(E_2(N_{F_2})\bigr)\subseteq E_1(N_{F_2})\subseteq N_{F_2}$$
⟹ well_defined。$[1]\circ[2]$ は shadow(正典: $GTSh(N,N)$ は groupoid ⟹ 合成は shadow)⟹ SETTLE-AUT で **settled** ✔
さらに $\overline{E_{[1]\circ[2]}}=\bar E_1\circ\bar E_2$ ⟹ ★ **$\Psi$ は準同型** ✔

### 3.3 結合律
$GT(N)$ 自体が正典で群(groupoid $GTSh(N,N)$)⟹ 結合律は継承 ✔
★ 独立確認: COMP-E より $\Psi$ の像側は**写像の合成**で、これは結合的 ✔

### 3.4 ★★ 逆元(証明の要)
$[m,f]$ settled、$[\tilde m,\tilde f]:=[m,f]^{-1}$(正典 (3.54)・shadow)とする。
$[m,f]\circ[\tilde m,\tilde f]=[0,1]$ と COMP-E より、$Q$ の中で
$$\phi_{[m,f]}\circ E_{[\tilde m,\tilde f]}=\pi\circ E_{[m,f]}\circ E_{[\tilde m,\tilde f]}=\pi\circ E_{[0,1]}=\pi$$
いま $n\in N_{F_2}$ を取ると
$$\phi_{[m,f]}\bigl(E_{[\tilde m,\tilde f]}(n)\bigr)=\pi(n)=1$$
⟹ $E_{[\tilde m,\tilde f]}(n)\in\ker\phi_{[m,f]}\overset{\text{settled}}{=}N_{F_2}$。

$$\boxed{\ \Longrightarrow\ E_{[m,f]^{-1}}(N_{F_2})\subseteq N_{F_2}\ \Longrightarrow\ [m,f]^{-1}\ \textbf{は well\_defined}\ \Longrightarrow\ \textbf{settled}\ }$$

★ **要点**: 使ったのは **$\ker\phi_{[m,f]}=N_{F_2}$(= $[m,f]$ の settledness そのもの)**。逆射の明示式 (3.54) を展開する必要はありません。∎

⟹ **§3.1–3.4 より $GT^{\rm settled}(N)\le GT(N)$ は部分群**、$\Psi$ は群準同型 ✔

---

## §4 ★ 射程(窓一般か $N'$ 固有か)

| 段 | 使ったもの | 射程 |
|---|---|---|
| COMP-E(§1) | 正典 (3.53)(3.49) のみ | ★ **窓一般**(実は $N$ に無関係な $F_2$ 上の恒等式) |
| SETTLE-AUT(§2) | 便 121 A7.1 + $Q$ 有限 + shadow の全射性 | ★ **窓一般** |
| 単位・閉性・結合・逆元(§3) | 上の 2 つのみ | ★ **窓一般** |
| **埋入の単射性**(§5) | $\bar E=\mathrm{id}\Rightarrow[m,f]=[0,1]$ | ⚠ **窓依存** |

$$\boxed{\ \textbf{群構造と準同型性は任意の }N\in\mathrm{NFI}_{PB_3}(B_3)\ \textbf{で成立}\ }$$

---

## §5 ⚠★ 埋入の単射性 — **自動ではありません**(発注項目のうちここだけ条件つき)

$\ker\Psi=\{[m,f]\in GT^{\rm settled}(N) : \bar E_{[m,f]}=\mathrm{id}_Q\}$。
$\bar E=\mathrm{id}$ ⟺ $\bar x^{\,u}=\bar x$ かつ $\bar f^{-1}\bar y^{\,u}\bar f=\bar y$。

- $\bar x^{u}=\bar x$ ⟹ $\mathrm{ord}(\bar x)\mid u-1$。
- ⚠ しかし $N_{\rm ord}=\mathrm{lcm}(\mathrm{ord}\bar x,\mathrm{ord}\bar y,\mathrm{ord}\bar c)$ ⟹ **$u\equiv1\pmod{N_{\rm ord}}$ は従いません** ⟹ $m\equiv0$ が出ない。
- 第 2 条件からも $\bar y^{u}=\bar f\bar y\bar f^{-1}$($\bar y^u$ は $\bar y$ に共役)までで、$u\equiv1$ は出ません。

$$\boxed{\ \Longrightarrow\ \Psi\ \textbf{の単射性は一般には成り立たない — 「埋入」と書くには窓ごとの確認が要る}\ }$$

### 5.1 ★ $N'$($=\ker(B_3\to\tilde H)$)での状況
- $c\in N'$ ⟹ $\mathrm{ord}(\bar c)=1$
- 実測(`q3r1_lift_spec_v1.md` §4): $\mathrm{ord}(\bar x)=\mathrm{ord}(\bar y)=47679=N_{\rm ord}$

⟹ $\bar x^{u}=\bar x$ から $47679\mid u-1$ ⟹ ★ **$u\equiv1\pmod{N_{\rm ord}}$ ⟹ $m\equiv0$** ✔
⟹ $\ker\Psi\subseteq\{[0,f]\ :\ \bar f\in C_Q(\bar y)\}$($\bar E(\bar y)=\bar f^{-1}\bar y\bar f=\bar y$ より)

$$\boxed{\ \textbf{残る問い}:\ [0,f]\ (\bar f\in C_Q(\bar y),\ \bar f\ne1)\ \textbf{が shadow になり得るか}\ }$$
⟹ 【SG-GAP-1】。★ **なり得なければ $\Psi$ は $N'$ 上で単射**(= 真の埋入)。
★ **測定は安い**: $C_Q(\bar y)$ は $SL(2,\mathbf Z/691^2)$ の中心化群 ⟹ 構造は標準($\bar y$ が正則なら巡回)⟹ その元 $f$ で hexagon が立つかを見るだけ。

---

## §6 ★ L3-GAP-1($a_N^{-1}(1)$ の部分群性)との関係

$a_N=\mathcal{PR}_N\circ\mathrm{Ih}$。$\mathrm{Ih}:G_\mathbf Q\to\widehat{GT}_{\rm gen}$ は**群準同型**、$\mathcal{PR}_N$ は非 isolated 時に**集合写像**。

★ **本定理からの帰結**:
$$\mathcal{PR}_N^{-1}\bigl(GT^{\rm settled}(N)\bigr)\ \textbf{の上では、}\ \mathcal{PR}_N\ \textbf{は群の言葉で扱える}$$
理由: $GT^{\rm settled}(N)$ は**群**であり(§3)、そこへの射影は $\Psi$ を通じて $\mathrm{Aut}(Q)$ の中で合成と整合する(COMP-E)。
$$\boxed{\ \Longrightarrow\ \textbf{像が }GT^{\rm settled}(N)\ \textbf{に入る範囲では }a_N^{-1}(1)\ \textbf{は部分群 ⟹ 核体 }L_N\ \textbf{が定義できる}\ }$$
⟹ ★ **L3-GAP-1 は「像が settled 部分に入るか」という 1 条件に縮約**されます(完全な閉鎖ではなく**条件つき閉鎖**)。
⚠ 像が settled 部分をはみ出す場合は、$a_N^{-1}(1)$ の部分群性は**依然 UNKNOWN**。

---

## §7 ⟹ ③ 線 再出発の形

| 対象 | 状態 |
|---|---|
| 土俵 | ★ **$GT^{\rm settled}(N')$(群)** — 本定理で確立 |
| 段 2 の成果($\tilde H$ の容器・非分裂拡大・braid 全射) | ★ **無傷のまま接続**($\tilde H$ 側の群論で $GT$ の型に依存しない) |
| **(Q4′)** | ★ **サイズ会計**: $\lvert GT(N')\rvert$ vs $\lvert a_{N'}(G_\mathbf Q)\rvert$ + **像が $GT^{\rm settled}(N')$ に入るか** |
| **(Q5)** | 不変(**R-1 は OPEN**) |
| 核体 $L_{N'}$ | ★ **像が settled 部分に入れば定義可**(§6) |

★ **次の一手(推薦)**: **【SG-GAP-1】**($[0,f]$、$\bar f\in C_Q(\bar y)\setminus\{1\}$ が shadow か)⟹ 立てば $\Psi$ が**真の埋入**になり、$GT^{\rm settled}(N')$ が $\mathrm{Aut}(Q)$ の部分群として**具体的に同定**できます ⟹ **(Q4′) のサイズ会計の分母が確定**します。

---

## §8 GAP・記帳

- **【SG-GAP-1】(小・新)** $\ker\Psi$ の自明性($N'$ 上)。⟹ §5.1・測定は安い。
- **【SG-GAP-2】(小・新)** §3.2 で使った「合成は shadow」は正典の groupoid 性に依拠。⟹ 逐語 pin(定義ノート L169–171)を cert に。
- **【L3-GAP-1】★ 条件つき閉鎖**(§6)。
- **【L3-GAP-2】★ 閉鎖**(本ノート §3)。
- ★ **本ノートの新規部分**: ① **補題 COMP-E**(合成 (3.53) が $E$ の合成そのものであること・手計算 + 300/300 機械検算)② **逆元の証明**($\ker\phi=N_{F_2}$ だけを使い (3.54) を展開しない短い論法)③ ★ **単射性が自動でないことの摘出**と $N'$ での縮約($m\equiv0$ まで確定)④ **L3-GAP-1 の条件つき閉鎖**。
- ⚠ **正直な申告**: 司令塔の発注は「群をなし $\mathrm{Aut}(Q)$ へ**埋入**すること」でしたが、★ **埋入(単射)は一般には言えません**。**群構造・準同型・窓一般性**は立ちました。
- **申告**: 機械検算は自由群の語計算のみ(GAP 走行ゼロ)・$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
