# 発案 6 号「集合版の手術」札 5 枚の検分(裁定 1082)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔裁定 1082
対象 = `docs/notes/ideas_set_surgery_v1.md`(発案係・commit `43b64e27`・全札 candidate)
併合入力 = 実装係 B の fixture cert `search/certs/set_surgery_fixture_v1_20260813.json`(commit `429c18b3`)+ 司令塔便 2 通(検分項目 5・研究者発案 7 号仮札)
正典 = 定義ノート L153–179(groupoid GTSh・(3.49)(3.53)(3.54)(3.60)・Prop 3.6/3.8/3.14・Cor 5.4・Thm 5.2)
⚠ $u$/$c$ 非接触・封印 3 量($K^{(5)}$ インスタンス)非接触・prereg 量非計算。**全結果 candidate 格**(Sol 未監査・verified ではない)。

---

## §0 判定表(先出し)

| 札 | 判定 | 一行理由 |
|---|---|---|
| **I-SET-1** トーサー分解 | ★★★ **採用・格上げ(予想 → 定理)** | 正典 Thm 3.10 + COMP-E で**証明できます**(§1)。fixture が厳密一致(§2)。破綻点 ①②③ はすべて解消 |
| **I-SET-2** 指標計数 | ★ **採用(改造)** | 公式は**正しい**(独立検算 §3.1)。⚠ ただし **指標は不要** — 類サイズ + べき写像だけで $O(\#\text{classes})$、発案係見積り $10^{11}$ が $10^{5\text{–}6}$ に落ちます(§3.2)。用途の指定は誤り(§5.3) |
| **I-SET-3** 存在検定 | ⚠ **改造(存在検定は棄却・α/β 弁別は採用)** | 包含鎖は**正典 Cor 5.4 から無料**(§5.1・発案係の心配は杞憂)。しかし ★ **この検定は原理的に発火しません**(§5.2 で証明)。α/β 弁別は採用 |
| **I-SET-4** 剛性 | ⚠ **保留(証拠の格下げ)** | SG-GAP-1 も fixture も **charming 条件で説明されうる**(§6.2)— 現状の測定設計では hexagon の剛性を分離できていません。捻りの型も要修正(§6.1・**検分項目 5 への回答**) |
| **I-SET-5** 結審 | ⚠ **条件節を撤回・結論は別根拠で概ね維持** | 「札2×札3 の合流が唯一の残存路」は **論理的に成立しません**(上界と下界の取り違え・§7.1)。ただし ★ **別の合流が立ちます**(§4) |

$$\boxed{\ \textbf{本検分の最大の獲得物(発案係も私も v1 では書いていない)}:\ \textbf{札 1}\times\textbf{札 2 は}\ \lvert GT(N')\rvert\ \textbf{の}\textbf{上界}\ \textbf{を与える}\ }$$
⟹ `gt_settled_identification` §4.1「$\lvert GT(N')\rvert$ は数えられません」・`settled_layer_verdict` §7.3「サイズ会計 ✘ 計数不能」を**覆しうる**唯一の路(§4)。しかも既知の下界 30,360 との**突合が一致検査になる**。

$$\boxed{\ \textbf{見積り(§4.1・16 群で較正した機構からの外挿)}:\quad 3\times10^4\ \le\ \bigl\lvert GT(N')\bigr\rvert\ \lesssim\ 10^{6\text{–}7}\ }$$
⚠ **$10^{17}$ は $\lvert\tilde H\rvert$ であって $\lvert GT(N')\rvert$ ではありません** — ③ 線の「規模で詰んだ」判定は**約 11 桁の取り違え**の疑いがあります(見積り格・証明ではない)。

---

# §1 【I-SET-1】★★★ 定理 TORSOR — 予想ではなく**定理**です

## 1.0 記号

$N\in\mathrm{NFI}_{PB_3}(B_3)$、$Q:=F_2/N_{F_2}$、$u:=2m+1$。$[m,f]\in GT(N)$ に対し
$$T_{m,f}:B_3\to B_3/N,\qquad \sigma_1\mapsto\sigma_1^{u}N,\quad\sigma_2\mapsto f^{-1}\sigma_2^{u}fN$$
は全射(Def 3.7)。$\kappa([m,f]):=\ker T_{m,f}$、$GTSh(K,N)=\kappa^{-1}(K)$、$GT^{\rm settled}(N)=GTSh(N,N)$。

## 1.1 補題 0(ファイバー分解は**分割**である)— 検分項目 (b) への回答

$\ker T_{m,f}$ は $B_3$ の有限指数正規部分群で、便 121 A7.1($\pi_{S_3}\circ T=\pi_{S_3}$)より $\subseteq PB_3$ ⟹ $\kappa$ は**写像** $GT(N)\to\mathrm{NFI}_{PB_3}(B_3)$。写像のファイバーは互いに素で全体を覆う ⟹
$$GT(N)=\bigsqcup_{K\in\mathcal C(N)}GTSh(K,N),\qquad \mathcal C(N):=\kappa\bigl(GT(N)\bigr)=\{K:GTSh(K,N)\ne\emptyset\}$$

$$\boxed{\ \textbf{空ファイバーは }\mathcal C(N)\ \textbf{の定義から除かれ、和にも寄与しない ⟹ 等式は壊れません}\ }$$
⟹ 発注の検分項目 **(b) は非問題**。⚠ 発案係が破綻点として挙げていないが、$\kappa$ が写像である(= 核が 1 個に決まる)ことが本当の要で、それは $T$ が写像であること以上のものを要しません。

## 1.2 ★★ 補題 1(合成の正体)— 発案係の破綻点 ① を**計算で**解消

> **【補題 COMP-T】** $s=[m_1,f_1]$ が **settled**($\kappa(s)=N$)、$t=[m_2,f_2]\in GT(N)$ とする。このとき
> (i) 正典の合成 (3.53) $s\circ t$ は **well-defined**、
> (ii) $\boxed{\ T_{s\circ t}=\bar T_s\circ T_t\ }$($\bar T_s:B_3/N\to B_3/N$ は $T_s$ の誘導写像)。

**証明**: (i) $\bar T_s$ が定まるのは $T_s(N)\subseteq N$、すなわち SETTLE-AUT の $E_s(N_{F_2})\subseteq N_{F_2}$ — これが settled の内容そのもの(`settled_grp_proof_v1` §2)。(3.53) の $f$ 成分 $f_1E_{m_1,f_1}(f_2)$ が $\bmod N_{F_2}$ で定まる条件も同一。
(ii) 生成元で確認する:
- $\bar T_s\bigl(T_t(\sigma_1)\bigr)=\bar T_s(\sigma_1^{u_2})=\sigma_1^{u_1u_2}$。一方 (3.49) より $u(s\circ t)=2(2m_1m_2+m_1+m_2)+1=u_1u_2$ ✔
- $\bar T_s\bigl(T_t(\sigma_2)\bigr)=\bar T_s\bigl(f_2^{-1}\sigma_2^{u_2}f_2\bigr)=T_s(f_2)^{-1}\bigl(f_1^{-1}\sigma_2^{u_1}f_1\bigr)^{u_2}T_s(f_2)=\bigl(f_1E_s(f_2)\bigr)^{-1}\sigma_2^{u_1u_2}\bigl(f_1E_s(f_2)\bigr)$
 ⟹ (3.53) の $f$ 成分 $f_1E_{m_1,f_1}(f_2)$ と**完全一致** ✔ ∎

$$\boxed{\ \Longrightarrow\ \textbf{source/target 規約は「圏論の慣例」ではなく (3.53) から}\textbf{計算で読める}:\ \mathrm{source}(s)=\mathrm{target}(t)=N\ \textbf{が合成可能条件}\ }$$
⟹ 発案係の破綻点 ①(「規約を式でなく慣例から推測している」)は**解消**。左右が入れ替わる余地もありません。

## 1.3 補題 2(ファイバー保存)

> $s$ settled、$t\in GTSh(K,N)$ ⟹ $\kappa(s\circ t)=K$。

**証明**: $T_s$ 全射 ⟹ $\bar T_s:B_3/N\to B_3/N$ 全射、$B_3/N$ 有限 ⟹ **全単射**。よって
$$\ker T_{s\circ t}=\ker(\bar T_s\circ T_t)=T_t^{-1}(\ker\bar T_s)=T_t^{-1}(1)=\ker T_t=K\ ∎$$
★ **settled が効く唯一の場所**がここ($\bar T_s$ の存在と単射性)。非 settled な $s$ では合成が**そもそも定義されません**。

## 1.4 ★★★ 定理 TORSOR

> **【定理 TORSOR】** 任意の $K\in\mathcal C(N)$ に対し、$GTSh(K,N)$ は左からの合成により **$GT^{\rm settled}(N)$-トーサー**(自由かつ推移的)である。したがって
> $$\boxed{\ \bigl\lvert GT(N)\bigr\rvert\ =\ \bigl\lvert GT^{\rm settled}(N)\bigr\rvert\ \times\ \#\mathcal C(N)\ }$$

**証明**:
- **作用**: 補題 1・2 より $(s,t)\mapsto s\circ t$ は $GT^{\rm settled}(N)\times GTSh(K,N)\to GTSh(K,N)$。結合律は正典 Thm 3.10、単位元は $[0,1]$(settled: `settled_grp_proof_v1` §3.1)⟹ 群作用 ✔
- **自由**: $s\circ t=s'\circ t$ ⟹ 右から $t^{-1}$(正典 (3.54)・Thm 3.10)を合成し結合律を使う ⟹ $s\circ(t\circ t^{-1})=s'\circ(t\circ t^{-1})$ ⟹ $s\circ\mathrm{id}_N=s'\circ\mathrm{id}_N$ ⟹ $s=s'$ ✔
 ⚠ ★ **ここで $T$ 経由の議論を使わないことが重要**: 同じ $T$ に複数のペア $[m,f]$ が対応しうる(発案係の破綻点 ②)ので、**逆射で消すのが正しい**。⟹ 破綻点 ② も解消。
- **推移的**: $t,t'\in GTSh(K,N)$ に対し $s:=t'\circ t^{-1}$。$t^{-1}\in GTSh(N,K)$(source $N$・target $K$)ゆえ $\mathrm{source}(s)=N$, $\mathrm{target}(s)=N$ ⟹ $s\in GTSh(N,N)$、かつ $s\circ t=t'\circ(t^{-1}\circ t)=t'\circ\mathrm{id}_K=t'$ ✔
- ⟹ $\lvert GTSh(K,N)\rvert=\lvert GT^{\rm settled}(N)\rvert$($K\in\mathcal C(N)$)⟹ 補題 0 の分割で総和 ∎

## 1.5 系(すべて新規)

- **系 A**: 射がすべて可逆ゆえ $\mathcal C(N)=$ **groupoid $GTSh$ における $N$ の連結成分**。⟹ $\#\mathcal C(N)$ は成分の大きさ、$N^\diamond=\bigcap_{K\in\mathcal C(N)}K$(Prop 3.14)。
- **系 B**: 同一成分の全対象で $\lvert GT\rvert$ と $\lvert GT^{\rm settled}\rvert$ が一致(vertex 群が同型)。
- **系 C(isolated の特徴づけ)**: $\boxed{N\ \text{isolated}\iff\#\mathcal C(N)=1\iff\lvert GT(N)\rvert=\lvert GT^{\rm settled}(N)\rvert}$
 (⟸ は $[0,1]$ の核が $N$ ゆえ $\mathcal C=\{N\}$ ⟹ 全 shadow settled)。
 ⟹ ★ **$\#\mathcal C(N)$ は「isolated からのずれ」を測る窓不変量**であり、census83 の「半率 $1/2$」は**厳密に $1/\#\mathcal C(N)$**。
- **系 D(★ 裁定 999 の $u\equiv1\ (\mathrm{mod}\ 3)$ 法則の機構)**: $u$ は合成で乗法的 (3.49) ⟹ ファイバー $s\circ t$($s$ settled)上で $u$ は $u(t)\cdot\chi_{\rm vir}(GT^{\rm settled}(N))$ を走る。よって
$$\chi_{\rm vir}\bigl(GT^{\rm settled}(N)\bigr)\subseteq\{u\equiv1\ (\mathrm{mod}\ 3)\}\ \Longrightarrow\ u\bmod3\ \textbf{はファイバー上一定}$$
 $\#\mathcal C=2$ かつ 2 類の $u\bmod3$ が異なれば **$u\bmod3$ はファイバーの完全不変量** ⟹ census83 §3 の観測法則。
 ★ さらに逆向きは**数え上げで自動**: [1008,521] では $\lvert\{u\equiv1\}\rvert=4\times6=24=\lvert GT^{\rm settled}\rvert$ ⟹ 包含が等号 ⟹ 「settled $\iff u\equiv1\ (3)$」の**⟸ 向きは ⟹ 向きから従う**。
$$\boxed{\ \textbf{残る未証明部分は「settled }\Rightarrow u\equiv1\ (\mathrm{mod}\ 3)\text{」の 1 本のみ — しかも }\chi_{\rm vir}|_{GT^{\rm settled}}\ \textbf{という}\textbf{群の準同型}\textbf{についての主張}\ }$$
 ⟹ 裁定 999 の機構問題が「群の指標の像」という扱いやすい形に縮約されました。

---

# §2 fixture との突合(実装係 B・cert `set_surgery_fixture_v1_20260813`)

| 検算 | 予言(定理 TORSOR) | 実測 | 判定 |
|---|---|---|---|
| [1008,521] slot1 | $\lvert GT\rvert=\lvert GT^{\rm settled}\rvert\cdot\#\mathcal C$ | $48=24\times2$・類サイズ **[24,24]** | ★★ **厳密一致** |
| 類サイズの均一性 | ★ トーサーゆえ**全ファイバーが同サイズ** | [24,24] | ★★ **これがトーサー性の直接証拠** |
| $K^{(9)}$(陽性対照) | isolated ⟹ $\#\mathcal C=1$(系 C) | $108$・$\#\mathcal C=1$ | ★ 一致 |
| 構造観察(descent の true/false) | ★ settled 類 = 全 true・他類 = 全 false(補題 2 の内容そのもの) | 24 で真の fail・**0 mismatch** | ★★ **一致** |

★ **司令塔の指摘「トーサー分解の検分の生データに使えるはず」は的中**しています: 「**均質に分離**」= $\kappa$ が写像であること(補題 0)と、settled 判定が核の等式であること(SETTLE-AUT)の合わせ技。ファイバーが**混ざらない**ことこそがトーサー分解の観測可能な帰結です。
⚠ **fixture は 1 窓 + 1 対照**。W-48 により $N'$ への外挿はしません(定理自体は窓一般なので外挿は不要 — **定理が保証し fixture が較正する**という正しい役割分担)。

**発注の検分項目 (c)「偶然でないか」への回答**: ★ **偶然ではありません**。定理の帰結であり、$108=108\times1$ と $48=24\times2$ は同一の等式の 2 例です。

---

# §3 【I-SET-2】指標計数の検分 — 公式は正しい・しかし**指標は要らない**

## 3.1 公式の検分(独立検算)

$B_3\cong\langle a,b\mid a^2=b^3\rangle$($a=\Delta$, $b=\delta$・`照合_B3表示_T2土台` (D3) で照合済)⟹
$$\#\mathrm{Hom}(B_3,H)=\#\{(A,B)\in H^2:A^2=B^3\}=\sum_{g\in H}\theta_2(g)\theta_3(g),\qquad \theta_k(g)=\#\{h:h^k=g\}$$
$\theta_k$ は類関数で $\langle\theta_k,\chi\rangle=\overline{\nu_k(\chi)}=\nu_k(\bar\chi)$ ⟹ $\theta_k=\sum_\chi\nu_k(\bar\chi)\chi$。よって
$$\sum_g\theta_2(g)\theta_3(g)=\sum_{\chi,\psi}\nu_2(\bar\chi)\nu_3(\bar\psi)\sum_g\chi(g)\psi(g)=\lvert H\rvert\sum_\chi\nu_2(\bar\chi)\nu_3(\chi)$$
$\chi\leftrightarrow\bar\chi$ の付け替えで発案係の式と一致 ⟹
$$\boxed{\ \#\mathrm{Hom}(B_3,H)=\lvert H\rvert\sum_\chi\nu_2(\chi)\,\nu_3(\bar\chi)\qquad\textbf{— 正しい}\ }$$
★ **手検算 2 本**: $H=\mathbf Z/2$ ⟹ $2\cdot[1\cdot1+1\cdot0]=2=\#\mathrm{Hom}(\mathbf Z,\mathbf Z/2)$ ✔ / $H=S_3$ ⟹ $6\cdot[1+0+1]=12$ = 直接列挙 12 ✔
⚠ **1 点修正**: $\nu_k(\chi)$ は $k\ge3$ では**一般に有理数ではありません**($\sigma(\nu_k(\chi))=\nu_k(\sigma\chi)$)。$\theta_k$ が整数値なのは総和後です。実装で有理数を仮定すると壊れます。

## 3.2 ★★ 改造 — 指標表は不要($10^{11}\to10^{5\text{–}6}$)

$\theta_k$ は類上一定で、$h\mapsto h^k$ は類 $C'$ から類 $C$ への**等ファイバー**写像($\lvert C'\rvert/\lvert C\rvert$ 個ずつ)⟹
$$\boxed{\ \#\mathrm{Hom}(B_3,H)=\sum_{C}\frac{A(C)\,B(C)}{\lvert C\rvert},\qquad A(C)=\#\{h:h^2\in C\},\ \ B(C)=\#\{h:h^3\in C\}\ }$$
$A,B$ は**類サイズと 2・3 べき写像だけ**から $O(\#\text{classes})$ で作れます。

| 方式 | 必要データ | 計算量($\tilde H$ 本体: $\#\text{classes}\approx5\times10^5$) |
|---|---|---|
| 全数列挙 | — | $\lvert H\rvert^2\approx4\times10^{35}$ |
| 発案係(指標和) | **指標表**($SL(2,\mathbf Z/p^2)$ 型 — **正典外・文献要請案件**) | $\approx2.5\times10^{11}$(代数的数演算) |
| ★ **本改造(類 + べき写像)** | 類サイズ・$p_2,p_3$ **のみ** | ★ $\approx5\times10^5$(有理整数演算) |

$$\boxed{\ \Longrightarrow\ \textbf{発案係の破綻点 ③(}\tilde H\ \textbf{の指標表が正典外・文献要請)は}\textbf{回避}\textbf{されます — 文献要請は不要}\ }$$
★ mod-$\Phi$ 水準に落とす必要もなくなります(発案係の実行案の前提が消える)。

## 3.3 $S_3$ 両立(核が $PB_3$ に入る条件)の扱い

$\ker\varphi\subseteq PB_3\iff\varphi(PB_3)$ の指数が 6 $\iff$ $H$ の(本質的に一意な)$S_3$-商 $p:H\twoheadrightarrow S_3$ に対し **$p(A)$ が互換・$p(B)$ が 3-巡回**($a=\Delta\mapsto$ 互換, $b=\delta\mapsto$ 3-巡回)。
★ $p^{-1}(\{\text{互換}\})$・$p^{-1}(\{3\text{-巡回}\})$ は**共役類の和**(共役類は $S_3$ の共役類へ写る)⟹ §3.2 の類公式は**そのまま部分和に制限できます**:
$$\#\mathrm{Hom}_{PB_3}(B_3,H)=\sum_{C\subseteq p^{-1}(1)}\frac{A_\tau(C)B_\rho(C)}{\lvert C\rvert},\qquad A_\tau(C)=\#\{h\in p^{-1}(T):h^2\in C\},\ \ \text{等}$$
⚠ **一方、指標和は素直には制限できません**(Clifford 理論が要る)。⟹ ★ **改造版のもう 1 つの利点**。発案係の「同じ和の部分和で入る」は**類公式では正しく、指標公式では不正確**です。

## 3.4 得られる量(★ 用途は §4 へ)

$$\#\mathcal C(N)\ \le\ \#\{K\in\mathrm{NFI}_{PB_3}:B_3/K\cong B_3/N\}\ =\ \frac{\#\mathrm{Epi}_{PB_3}(B_3,\ B_3/N)}{\lvert\mathrm{Aut}(B_3/N)\rvert}\ \le\ \frac{\#\mathrm{Hom}_{PB_3}(B_3,\ B_3/N)}{\lvert\mathrm{Aut}(B_3/N)\rvert}$$
(1 つ目は Prop 3.8「$GTSh(K,N)\ne\emptyset\Rightarrow B_3/K\cong B_3/N$」。$\#\mathrm{Epi}$ は部分群束の Möbius で $\#\mathrm{Hom}$ から得るが、**上界だけなら Möbius すら不要**。)

---

# §4 ★★★ 本検分の主獲得物 — 札 1 × 札 2 は $\lvert GT(N')\rvert$ の**上界**を与える

発案係は札 2 を**札 3 の存在検定の燃料**としてのみ使い(そこでは §5.2 のとおり**使えません**)、札 1 の等式と組む用途を書いていません。組むとこうなります:

$$\boxed{\ \bigl\lvert GT(N)\bigr\rvert=\bigl\lvert GT^{\rm settled}(N)\bigr\rvert\cdot\#\mathcal C(N)\ \le\ \bigl\lvert GT^{\rm settled}(N)\bigr\rvert\cdot\frac{\#\mathrm{Hom}_{PB_3}(B_3,B_3/N)}{\lvert\mathrm{Aut}(B_3/N)\rvert}\ }$$

$N'$ では $\lvert GT^{\rm settled}(N')\rvert=2$(cert `e41191d6`・全数確定)⟹

$$\boxed{\ \bigl\lvert GT(N')\bigr\rvert\ \le\ \frac{2\,\#\mathrm{Hom}_{PB_3}(B_3,\tilde H)}{\lvert\mathrm{Aut}(\tilde H)\rvert}\qquad(\textbf{算術入力ゼロ・純群論})\ }$$

## 4.1 ★★ 桁の見立て — **測りました**(機械・16 群)

`scratchpad/set_surgery_hom_b3.g`(GAP 4.16.0)で **3 系統(全数列挙 / 類公式 / 指標和)が全群で一致** ✔(装置の較正完了)。比 $\#\mathrm{Hom}(B_3,H)/\lvert H\rvert$:

| $H$ | $\lvert H\rvert$ | 比 | $H$ | $\lvert H\rvert$ | 比 |
|---|---|---|---|---|---|
| $SL(2,7)$ | 336 | **8** | $SL(2,31)$ | 29,760 | **32** |
| $SL(2,11)$ | 1,320 | **10** | $SL(2,37)$ | 50,616 | **40** |
| $SL(2,13)$ | 2,184 | **16** | $SL(2,41)$ | 68,880 | **42** |
| $SL(2,17)$ | 4,896 | **18** | $SL(2,43)$ | 79,464 | **44** |
| $SL(2,19)$ | 6,840 | **20** | $SL(2,47)$ | 103,776 | **46** |
| $SL(2,23)$ | 12,144 | **22** | $SL(2,53)$ | 148,824 | **54** |
| $SL(2,25)$ | 15,600 | **28** | $SL(2,59)$ | 205,320 | **58** |
| $PSL(2,7)$ | 168 | **8** | $SL(2,61)$ | 226,920 | **64** |
| $PSL(2,11)$ | 660 | **10** | $SL(2,67)$ | 300,696 | **68** |

$$\boxed{\ \#\mathrm{Hom}(B_3,SL(2,q))=\lvert SL(2,q)\rvert\cdot(q+\varepsilon),\qquad \varepsilon=\begin{cases}+3&q\equiv1\\+1&q\equiv5,7\\-1&q\equiv11\end{cases}\ (\mathrm{mod}\ 12)\ }$$
(★ 観測法則・candidate。$\gcd(q,6)=1$ の全 15 例で例外 0。$SL(2,9)$ は $3\mid q$ ゆえ別系統で比 11。)

★ **機構(紙)**: 和 $\sum_C A(C)B(C)/\lvert C\rvert$ を支配するのは**中心の類**($\lvert C\rvert=1$)。$SL(2,q)$ では $\theta_2(-I)=\#\{\mathrm{tr}=0\}\approx q^2$、$\theta_3(-I)=\#\{\text{位数 }6\}\approx q^2$ ⟹ 項 $\approx q^4$、$\lvert H\rvert\approx q^3$ ⟹ **比 $\approx q$** ✔ 実測と一致。
⟹ ★ **比は $O(1)$ ではなく $\approx\lvert H\rvert^{1/3}$**(私の当初の見立ては誤りでした — 測って修正)。

**$\tilde H$ への外挿(★ 外挿ラベルつき・W-48)**: $Q\cong SL(2,\mathbf Z/691^2)$ 型では $\lvert H\rvert\approx p^6$、$\theta_k(\pm I)\approx\lvert H\rvert/p^2\approx p^4$ ⟹ 比 $\approx p^2=691^2\approx4.8\times10^5$。$\lvert\mathrm{Aut}(\tilde H)\rvert\ge\lvert\tilde H/Z\rvert$ ⟹

$$\boxed{\ \bigl\lvert GT(N')\bigr\rvert\ \lesssim\ 2\cdot p^2\cdot\lvert Z(\tilde H)\rvert\ \approx\ 10^6\text{–}10^7\qquad(\textbf{見積り・証明ではない})\ }$$

$$\boxed{\ \Longrightarrow\ \textbf{「}\lvert GT(N')\rvert\approx10^{17}\ \textbf{ゆえ計数不能」は}\textbf{約 11 桁の取り違え}\ \textbf{— }10^{17}\ \textbf{は }\lvert\tilde H\rvert\ \textbf{であって }\lvert GT(N')\rvert\ \textbf{ではない}\ }$$

★ **既知の下界 30,360 と無矛盾**($3\times10^4\le\lvert GT(N')\rvert\lesssim10^7$)⟹ 見積りは**一致検査を通ります**。⚠ ただしこれは**見積りであり証明ではありません** — 実測には $\tilde H$ の類データが要ります(【SS-GAP-1】)。

## 4.2 ★ どちらに転んでも結論が出る(既知の下界との突合)

既知: $\chi_{\rm vir}\circ a_{N'}=$ 円分 ⟹ Dirichlet より $u$ は $(\mathbf Z/47679)^\times$ の全 30,360 値を取る ⟹ $\lvert a_{N'}(G_{\mathbf Q})\rvert\ge30{,}360$ ⟹ $\lvert GT(N')\rvert\ge30{,}360$ ⟹ $\#\mathcal C(N')\ge15{,}180$。

| 上界の測定結果 | 帰結 |
|---|---|
| **$<30{,}360$** | ⚠ **矛盾** ⟹ 前提のどれかが誤り(Prop 3.8 の使い方 / $\lvert GT^{\rm settled}(N')\rvert=2$ / 円分下界 / $\tilde H$ の同定)⟹ **一致検査として一級**(即停止・洗い直し) |
| **$=30{,}360$**(ちょうど) | ★★★ **$a_{N'}(G_{\mathbf Q})=GT(N')$** ⟹ **$N'$ で全射性が成立**(正の結果・井原型の族的証拠) |
| **$30{,}360<\cdot<\infty$ の具体値** | ★ **比較のギャップが有限の名前つき数になる** ⟹ (Q4′) が「settled 層限定」でなく**全体**で書ける |

$$\boxed{\ \Longrightarrow\ \textbf{`settled\_layer\_verdict` §7.3 の道具表に「サイズ会計 ✘ 計数不能」と書いた行は、}\textbf{書き換えの候補}\textbf{になります}\ }$$
⚠ **実行の壁は残ります**: $\tilde H$($\approx6.5\times10^{17}$)の共役類リストとべき写像を作れるか。$\#\text{classes}\approx5\times10^5$ は**構造論(Clifford / 合同フィルトレーション)で書き下す**のが本筋で、群を列挙するのではありません。⟹ **【SS-GAP-1】**(§9)。

## 4.3 較正(先に走らせるべきもの)

fixture [1008,521] で **上界と実測 $\#\mathcal C=2$ の比**を測れば、緩み(Prop 3.8 の上界がどれだけ甘いか)が初めて数値で分かります。$K^{(9)}$($\#\mathcal C=1$)も同様。⟹ **§8 の一手目**。

---

# §5 【I-SET-3】存在検定の検分

## 5.1 包含鎖は**正典から無料**(発案係の心配は杞憂)

発案係は「中段 $\mathcal{PR}_{N'}=R_{M,N'}\circ\mathcal{PR}_M$ の逐語確認が要る・ここが折れたら札全体が落ちる」と書きましたが、**Cor 5.4(画像照合済・定義ノート L176)がそのまま与えます**:
$$\text{genuine}\iff\text{全ての細分 }K\le N\text{ に survive}\quad\Longrightarrow\quad \mathcal{PR}_{N'}(\widehat{GT}_{\rm gen})=\bigcap_{K\le N'}\mathrm{Im}\,R_{K,N'}$$
⟹ 各 $M\le N'$ で $\mathcal{PR}_{N'}(\widehat{GT}_{\rm gen})\subseteq\mathrm{Im}\,R_{M,N'}$ ✔(等号つきでより強い)。$a_{N'}=\mathcal{PR}_{N'}\circ\mathrm{Ih}$ ゆえ左端も自明。
$$\boxed{\ a_{N'}(G_{\mathbf Q})\ \subseteq\ \mathcal{PR}_{N'}(\widehat{GT}_{\rm gen})\ =\ \bigcap_{K\le N'}\mathrm{Im}\,R_{K,N'}\ \subseteq\ \mathrm{Im}\,R_{M,N'}\ \ (\forall M\le N')\qquad\textbf{✔ 成立}\ }$$
★ **isolated である必要すらありません**(任意の細分で成立)。発案係の破綻点 ① は解消・(iii) の設問も不要になります(下記の理由で検定自体を使わないため)。
★ $M$ の存在も無料: $N'^\diamond$(Prop 3.14)が isolated な細分 ✔

## 5.2 ★★ しかしこの検定は**原理的に発火しません**(証明)

検定は「$\lvert GT(M)\rvert<\lvert GT(N')\rvert$ なる $M$ を見つける」。ところが §5.1 の鎖から
$$\bigl\lvert a_{N'}(G_{\mathbf Q})\bigr\rvert\ \le\ \bigl\lvert\mathrm{Im}\,R_{M,N'}\bigr\rvert\ \le\ \bigl\lvert GT(M)\bigr\rvert\qquad(\forall M\le N')$$

> **【観察 NOFIRE】** $\lvert GT(N')\rvert$ の下界が**算術像に由来する**(すなわち $\le\lvert a_{N'}(G_{\mathbf Q})\rvert$ の量から作られる)かぎり、その下界は自動的に $\lvert GT(M)\rvert$ 以下であり、**検定条件 $\lvert GT(M)\rvert<\lvert GT(N')\rvert$ を満たすことは決してありません**。

現在の下界 30,360 は**まさに像由来**(円分指標の全射性)⟹
$$\boxed{\ \textbf{発案係の「ギャップ 12 桁」は「まだ足りない」ではなく「この路では}\textbf{永久に}\textbf{足りない」}\ }$$
⟹ 発火には**非像由来の** $\lvert GT(N')\rvert$ の下界が要る。定理 TORSOR より それは $\#\mathcal C(N')$ の**下界**を要求しますが、**札 2 が与えるのは上界だけ**(§3.4)。

$$\boxed{\ \Longrightarrow\ \textbf{札 2 × 札 3 の「合流」は}\textbf{論理的に成立しません}\ (\text{上界と下界の取り違え})\ }$$

⚠ 発案係は破綻点 ③ で「下界が像由来であることは弱み」と正直に書いていますが、**それが致命的**(単なる弱みではない)ことを見落としています。判定: **存在検定は棄却**。

## 5.3 採用する部分

- ★ **α/β 弁別は採用**: $GT(N')\setminus a_{N'}(G_{\mathbf Q})\ne\emptyset$ の 2 つの意味(α: $\widehat{GT}$ 由来でない fake / β: genuine だが非算術 = 井原型の真の反例)を分けるのは**台帳の型整備として正しく、安い**。⟹ 語規約への追記を推薦。
- ⚠ ただし発案係の「本検定が出すのは α」は、検定を棄却したので**宙に浮きます**。§4 の上界路が出すのは **α でも β でもなく「$\lvert GT\rvert$ と $\lvert a\rvert$ の差」そのもの**(どちらの型かは別途 Cor 5.4 の有限深度検査で分ける)。

---

# §6 【I-SET-4】剛性 — 保留(証拠の格下げ)+ **検分項目 5 への回答**

## 6.1 ★ 捻りの型が 2 か所ずれています(検分項目 5 = 司令塔便の問い)

**(a) 中心化群を取る場所**: $f$ は **$Q=F_2/N_{F_2}$ の元**です(定義ノート: $[m,f]=(m+N_{\rm ord}\mathbf Z,\ fN_{F_2})$)。したがって捻り $q$ も $Q$ の元でなければ**型が合いません**。
実装係が読んだ「$PN=PB_3/N$ 内の中心化群」は**正典の意図と合いません**:
$$PB_3=F_2\times\langle c\rangle\ \Longrightarrow\ Q\cong F_2N/N\ \le\ PN,\qquad [PN:Q]=\mathrm{ord}(\bar c)=z$$
83 窓は $c\notin N$(census83 の型境界)ゆえ $z>1$ — [1008,521] では $z=2$、$\lvert PN\rvert=1008$、$\lvert Q\rvert=504$。
$$\boxed{\ C_{PN}(\bar x)\cap Q=C_Q(\bar x)\ \textbf{であり、}\ C_{PN}(\bar x)\ \textbf{は最大 }z\ \textbf{倍大きい} \Longrightarrow\ \textbf{生存率 }1/12\ \textbf{は測り直しが必要}\ }$$
⟹ **判定: 実装係の読みは正典の意図と不一致。$Q$ 内で取り直すこと**(差が出なければ結果は不変・出れば率が変わる)。

**(b) どの元の中心化群か**: 捻り $[m,f]\mapsto[m,fq]$ が「$T$ の内部自己同型による捻り」になるには
$$T_{m,fq}(\sigma_1)=\sigma_1^{u}\quad\text{と}\quad \mathrm{inn}_q\bigl(T_{m,f}(\sigma_1)\bigr)=q^{-1}\sigma_1^{u}q$$
が一致する必要があり、条件は $q\in C(\bar\sigma_1^{\,u})$ であって $C(\bar x)=C(\bar\sigma_1^{\,2})$ **ではありません**($u$ は奇数)。⟹ 発案係の「$q\in C_Q(\bar x)$ による座標捻り」は**候補集合の指定として不正確**。

## 6.2 ★★ 証拠の格下げ — charming 条件が交絡しています

**charming**(定義ノート)は $\bar f\in[Q,Q]$ を要求します。したがって $[m,fq]$ が shadow であるためには
$$\bar f\bar q\in[Q,Q]\ \text{かつ}\ \bar f\in[Q,Q]\ \Longrightarrow\ \boxed{\ \bar q\in[Q,Q]\ }$$
が**必要**。⟹ $q\notin[Q,Q]$ の捻りは **hexagon を見るまでもなく落ちます**。

| 対象 | $[Q,Q]$ | 交絡の有無 |
|---|---|---|
| fixture [1008,521]($\lvert Q\rvert=504$・可解) | ★ **真部分群**(可解ゆえ) | ⚠ **交絡する** — 生存率 $1/12$・$1/28$ は charming だけで説明されうる |
| $N'$($Q\cong SL(2,\mathbf Z/691^2)$ 型) | $p\ge5$ ゆえ**完全** ⟹ $[Q,Q]=Q$ | ✔ 交絡なし ⟹ **SG-GAP-1 = NO は hexagon の情報** |

$$\boxed{\ \Longrightarrow\ \textbf{fixture 検算 B は現状の設計では RIGID の証拠になりません}\ (\text{落ちた理由が分離されていない})}$$
⟹ **測定の修正**: 落ちた捻りを「charming で落ちた / 全射性で落ちた / **hexagon で落ちた**」の 3 分に分類して記録すること。hexagon 起因が支配的なら初めて RIGID の証拠になります。
★ **SG-GAP-1(=NO・$N'$)は交絡なし**なので、発案係の「既存実測が NO 側の証拠」は $N'$ については**有効**です(ただし $u=1$ 断面・$f\in C_Q(\bar y)$ という特定断面 — 発案係の破綻点 ① のとおり状況証拠)。

## 6.3 「1 生存 = 恒等のみ」の推論について

$q=1$ は常に生存する(元の shadow そのもの)⟹ **「shadow 1 個あたりちょうど 1 個生存」が実測されれば、その 1 個は恒等**で確定します ✔ 論理は正しい。
⚠ ただし cert が持つのは**総率 $1/12$**(平均 1)であって**各 shadow ごとに 1**ではありません。平均 1 は「ある shadow で 0・別で 2」でも成立します。⟹ **per-shadow の分布を出すこと**(実装係の「恒等のみと**推定**」は正しく推定に留まっています)。

## 6.4 紙の証明について

発案係の破綻点 ② のとおり、私も **RIGID を紙で証明できていません**(hexagon (3.3)(3.4) の $f$ 依存性を捻り一般で追う必要がある)。⟹ **【SS-GAP-2】**。
★ ただし §6.2 で「必要条件 $\bar q\in[Q,Q]$」は紙で立ちました(部分的な剛性)。可解窓ではこれだけで生存率が $1/[Q:[Q,Q]]$ 以下に落ちます。

## 6.5 発案係の「代償としての座標決定性」について

「剛性が立てば shadow の $f$ 座標は核と $u$ からほぼ決まる」— ★ **これは定理 TORSOR から既に、しかもより強く出ています**: ファイバー $GTSh(K,N)$ の元は settled 群の作用で**一意に**移り合う(自由推移的)。⟹ 「核 + settled 群の元」が完全座標。⟹ 発案係の (i)「軌道空間 $=\mathcal C(N')$」は正しく、**縮約率 $\lvert GT^{\rm settled}\rvert$**(発案係の言う「2」は $N'$ での実測値)。

---

# §7 【I-SET-5】結審の検分

## 7.1 条件節は撤回

「唯一の残存路は札 2(計数)× 札 3(存在検定)の合流」は §5.2 により**不成立**(上界 vs 下界)。⟹ 発案係の結審の**条件部分は誤り**です。

## 7.2 しかし結論(83 窓回帰は覆らない)は**別の理由で概ね維持**、ただし ★ **一点だけ覆りうる**

| 発案係の主張 | 私の判定 |
|---|---|
| 「どの装置も算術側の代金(SURG-A6)を 1 円も安くしない」 | ★ **維持**(§4 の上界も分母側だけ・分子は不変) |
| 「$N'$ 一窓の完全な比較には届かない」 | ⚠ **条件つきで否**: §4 の上界が具体値を出せば**分母は確定し、比較の差が有限の名前つき数になる** |
| 「83 窓回帰の結論は覆らない」 | ⚠ **部分的に覆りうる**: 「$N'$ は計数不能ゆえ小窓へ」の**理由**が消える可能性がある(§4.2)。⟹ ★ §4.1 の見積り $\lvert GT(N')\rvert\lesssim10^{6\text{-}7}$ が正しければ **$N'$ は「規模で詰んだ窓」ではなく「GAP の射程内の窓」**。ただし**実行の壁**【SS-GAP-1】は残る |
| ★ 教訓 W-7 提案「窓を選ぶとき比較装置が届く規模か先に確認する」 | ⚠ **前提が怪しい**: 「窓が $10^{17}$」は $\lvert\tilde H\rvert$ の話で、比較すべき $\lvert GT(N)\rvert$ とは**別の量**。W-7 は「$\lvert\tilde H\rvert$ でなく $\lvert GT(N)\rvert=\lvert GT^{\rm settled}\rvert\cdot\#\mathcal C$ の見積りで判断する」と**述べ直すべき**です |

## 7.3 統合会計表(改訂)

| 装置 | 縮約/変換 | v1 の評価 | ★ 本検分の評価 |
|---|---|---|---|
| トーサー分解(札 1) | $\div\lvert GT^{\rm settled}\rvert$ + 値域を核 census へ | 予想 | ★★★ **定理**(§1)・fixture 厳密一致 |
| 指標計数(札 2) | 列挙 $10^{35}\to$ 指標和 $10^{11}$ | 計数のみ可 | ★ **類公式で $10^{5\text{–}6}$**(§3.2)・文献要請不要 |
| reduction 上界(札 3) | 存在検定 | ギャップ 12 桁 | ✘ **原理的に発火せず**(§5.2)。包含鎖は無料 |
| 座標捻り軌道(札 4) | 立てば $\div10^5$ | NO 予想優勢 | ⚠ **証拠が交絡**(§6.2)・型も要修正 |
| ★ **札 1 × 札 2(新)** | $\lvert GT(N')\rvert$ の**上界** | — | ★★★ **「計数不能」を覆しうる唯一の路**(§4) |

## 7.4 発案係の「持ち帰り資産」3 点の検分

(i) 「$\#\mathcal C$ 列を 83 窓 census に足せば新しい窓不変量」⟹ ★ **正しく、かつ系 C で isolated 判定と同値**(単なる列ではなく既存判定の精密化)。さらに系 D で $u\equiv1\,(3)$ 法則の機構に**直結**しました ✔ 発案係の見立ては当たりです。
(ii) 「指標計数は大きすぎて諦めた窓の census を拡張する汎用装置」⟹ ★ 正しい。§3.2 の改造でさらに安くなります。
(iii) α/β 弁別 ⟹ ★ 採用(§5.3)。

---

# §8 研究者発案 7 号(仮札)への回答 — 算術部分トーサーは**立ちます**(条件つき)

問い: 「$a_N(G_{\mathbf Q})$ はトーサー構造と両立するか(算術 settled 元の作用で閉じた部分トーサーか)」。

> **【補題 ARITH-T】** $\hat g_1,\hat g_2\in\widehat{GT}_{\rm gen}$ とし、$\mathcal{PR}_N(\hat g_1)$ が **settled** とする。このとき
> $$\mathcal{PR}_N(\hat g_1\hat g_2)=\mathcal{PR}_N(\hat g_1)\circ\mathcal{PR}_N(\hat g_2)$$

**証明の筋**: $\widehat{GT}_{\rm gen}$ の合成も $(m_1,f_1)\circ(m_2,f_2)=(2m_1m_2+m_1+m_2,\ f_1E_{m_1,f_1}(f_2))$。$\bmod N$ に落とすとき $E_{m_1,f_1}(f_2)$ が $f_2\bmod N_{F_2}$ だけで決まる条件は $E_{m_1,f_1}(N_{F_2})\subseteq N_{F_2}$ = **$\mathcal{PR}_N(\hat g_1)$ が settled**(SETTLE-AUT)。$m$ 成分は無条件 ✔ ∎(⚠ 副有限側の $\widehat{N}_{F_2}$ の扱いは 1 行の詰めが要る ⟹【SS-GAP-3】)

**帰結**:
1. $\mathcal A_N:=\{\sigma\in G_{\mathbf Q}:a_N(\sigma)\ \text{settled}\}$ は $G_{\mathbf Q}$ の**部分群**(積・逆元とも補題 ARITH-T と SETTLED-GRP で閉じる)。
2. $\boxed{\ a_N(\mathcal A_N)\ \le\ GT^{\rm settled}(N)\ \textbf{は部分群}\ }$
3. $\boxed{\ a_N(G_{\mathbf Q})\ \textbf{は }a_N(\mathcal A_N)\ \textbf{の左作用で安定}\ \Longrightarrow\ \textbf{各ファイバー内で}\ a_N(\mathcal A_N)\textbf{-軌道の和(= 部分トーサーの和)}\ }$
4. ⟹ 比較が**2 因子に分解**する:
$$\frac{\lvert GT(N)\rvert}{\lvert a_N(G_{\mathbf Q})\rvert}=\underbrace{\frac{\lvert GT^{\rm settled}(N)\rvert}{\lvert a_N(\mathcal A_N)\rvert}}_{\textbf{settled 指数}}\times\underbrace{\frac{\#\mathcal C(N)}{\#(\text{像の軌道数})}}_{\textbf{核類指数}}$$
★ **成立条件**(研究者の問いへの直接の答え): 「**単一の**部分トーサー」になるのは $a_N(\mathcal A_N)=GT^{\rm settled}(N)$(settled 層の算術飽和)のとき。
- $N'$ では $GT^{\rm settled}(N')\cong C_2$ ⟹ 条件は **$f_c=1$ の 1 ビット**([Q4-FINAL])に一致 ⟹ **既存の結審と同じものに落ちます**。
- ⚠ **83 窓など $GT^{\rm settled}$ が大きい窓では新しい不変量**(settled 指数)になります ⟹ ★ **発案 7 号は $N'$ ではなく小窓で価値が出る**、というのが私の見立てです。

---

# §9 GAP・記帳

- **【SS-GAP-1】(★大・新)** $\tilde H$($\approx6.5\times10^{17}$)の共役類サイズと 2・3 べき写像を**構造論で書き下せるか**(Clifford 理論 / $SL(2,\mathbf Z/p^2)$ の合同フィルトレーション)。⟹ §4 の上界が実行可能かはここに懸かる。★ これが立てば「計数不能」が覆る。
- **【SS-GAP-2】(中・新)** 予想 RIGID の紙証明(hexagon の $f$ 依存性)。§6.2 で必要条件 $\bar q\in[Q,Q]$ までは立ったが、$[Q,Q]=Q$ の窓($N'$)では未着手。
- **【SS-GAP-3】(小・新)** 補題 ARITH-T の副有限側の詰め($\widehat{N}_{F_2}$ と $N_{F_2}$ の対応)。
- **【SS-GAP-4】(小・新)** 系 D の残り「settled $\Rightarrow u\equiv1\ (\mathrm{mod}\ 3)$」= $\chi_{\rm vir}\bigl(GT^{\rm settled}(N)\bigr)$ の像の決定(裁定 999 の機構)。
- **閉鎖**: 発案係の破綻点 I-SET-1 ①②③ すべて閉鎖(§1.2・§1.4・§1.1)。I-SET-3 ① 閉鎖(§5.1・Cor 5.4 で無料)。

## 9.1 実装係への差し戻し・追加測定(安い順)

```
[SS-1] fixture 再測定(検分項目 5 の修正・秒級)
   捻り集合を Q = F_2/N_{F_2} 内で取り直す(現状は PN = PB_3/N の疑い・[PN:Q]=ord(c̄))
   かつ落ちた理由を 3 分類: charming(f̄q̄ ∉ [Q,Q]) / 全射性 / hexagon
   かつ per-shadow の生存個数分布を出す(総率でなく)
   ⟹ hexagon 起因が支配的でなければ RIGID の証拠にならない(§6.2/§6.3)
[SS-2] 上界装置の較正(§4.3・秒〜分級)
   [1008,521] と K^(9) で #Hom_{PB3}(B_3, B_3/N) / |Aut(B_3/N)| を計算し
   実測 #C(=2, 1)との比(= Prop 3.8 上界の緩み)を出す
   ★ 二系統: (a) 類サイズ+べき写像(§3.2)  (b) 全数列挙(小窓なので可能)
[SS-3] 83 窓 census に #C 列を追加(系 C: #C=1 ⟺ isolated の回帰テストを兼ねる)
[SS-4] χ_vir(GT^settled(N)) の像を 83 窓全部で測る(【SS-GAP-4】の入力)
⚠ すべて u/c 非接触・封印非接触・算術入力ゼロ
```

## 9.2 申告

- ★ **本検分の新規部分**: ① **定理 TORSOR の証明**(補題 COMP-T の生成元計算で source/target 規約を確定・自由性を逆射で示し $T$ の多価性を回避)② 系 A–D(成分との同定・isolated の特徴づけ・**裁定 999 の機構の縮約**)③ $\#\mathrm{Hom}$ の**類公式**($10^{11}\to10^{5\text{–}6}$・$S_3$ 制限が素直に入る)④ ★★ **札 1 × 札 2 ⟹ $\lvert GT(N')\rvert$ の上界**(「計数不能」を覆しうる路・どちらに転んでも結論)⑤ **観察 NOFIRE**(像由来の下界では存在検定は永久に発火しない)⑥ **charming 交絡の摘出**(fixture 検算 B の証拠力の格下げ)⑦ 捻りの型の 2 か所の修正(検分項目 5 への回答)⑧ **補題 ARITH-T** と発案 7 号の 2 因子分解。
- **手計算の機械確認**: $\#\mathrm{Hom}(B_3,H)$ の 3 系統一致($H=\mathbf Z/2$, $S_3$ は手計算・その他は `scratchpad/set_surgery_hom_b3.g`)。
- **申告**: GAP 4.16.0 + 手計算。$u$/$c$ 非接触・封印非接触・prereg 非抵触・**Sol 未監査**・**verified ではない**(全 candidate 格)。

---
---

# 第 II 部 — 発案 7 号「普遍性×トーサーの統一」札 AT-1〜AT-5 の検分

対象 = `docs/notes/ideas_arith_torsor_v1.md`(発案係・commit `9c18c9f4`・全札 candidate)。司令塔便により**同便検分**。
⚠ 第 I 部の定理 TORSOR(§1)と系 A–D を前提として使います。

## §10 判定表(第 II 部)

| 札 | 判定 | 一行理由 |
|---|---|---|
| **AT-1** SUBTOR | ★★★ **採用・格上げ(補題候補 → 定理)** | (AT-a) は**定義的**・(AT-b) は**条件を足せば正しい**・(AT-d) の 5 行スケッチは**正しい**(§11 で $B_3$ 水準に書き直して穴 ② も解消)。⟹ **発案 7 号の中核は定理**であり、私の §8 補題 ARITH-T を**真に強化**します(安定性 → 推移性) |
| **AT-2** P1/P2 | ★ **採用。ただし P1 は既に確認済** | ★ **P1 は既存 census83 のデータで厳密一致**($5\cdot\{1,7,13,19\}\equiv\{5,11,17,23\}\bmod24$)⟹ 再集計すら不要(§12.1)。P2 は良い検定・設計は妥当 |
| **AT-3** COORD / AT-Q1 | ★ **採用(COORD は系)**・⚠ **AT-Q1 の摘出は正しく、既存結審の格下げを要求** | COORD・飢餓判定は SUBTOR+TORSOR の系(§13.1)。★ **AT-Q1 は当たり**: `settled_layer_verdict` §2.2 の「$f_c\ne1$ ⟹ $[-1,1]$ は非算術 = 一級」は**無効**(§13.2) |
| **AT-4** Q-STAB | ★ **摘出は正しい・採用**。⚠ ただし「救済」の**理由**は誤り | Q-STAB の条件式は正しい(私も独立に同じ式を得た・§11.2)。★ 正しい救済理由は「**(AT-d) が必要な元について Q-STAB を証明している**」(§14.1)。修理は **(A) を推薦**+より正直な定式化を提案 |
| **AT-5** DESCENT | ⚠ **採用(格下げ: ほぼ自明)** | 単調性・有限安定は自明、安定値 = genuine は Cor 5.4 + cofinality。★ **装置提案(降下プロファイルを窓不変量に)としては採用**(§14.2) |

---

## §11 【AT-1】SUBTOR — **定理です**(証明を $B_3$ 水準で起草)

### 11.0 基本補題(reduction の正体)

$M\le N$、$T\in GT(M)$、$R:=R_{M,N}$。(3.60) は座標の truncation($N_{\rm ord}\mid M_{\rm ord}$・$M_{F_2}\subseteq N_{F_2}$)。生成元で確認すると

$$\boxed{\ T_{R(T)}=\pi_{M,N}\circ T_T\qquad(\pi_{M,N}:B_3/M\twoheadrightarrow B_3/N)\ }\tag{R1}$$

($\sigma_1\mapsto\sigma_1^{u}N$ ✔ / $\sigma_2\mapsto f^{-1}\sigma_2^{u}fN$ ✔)。ゆえに
$$\boxed{\ \ker T_{R(T)}=T_T^{-1}\bigl(N/M\bigr)\ }\tag{R2}$$
$M$ isolated ⟹ 全 shadow settled ⟹ $\bar T_T\in\mathrm{Aut}(B_3/M)$(SETTLE-AUT の $B_3$ 版)⟹ (R2) は $\bar T_T^{-1}(N/M)$ の $B_3$ への引き戻し。
★ **$F_2$ 水準に降りないので、発案係の破綻点 ②($F_2$/$PB_3$ の混線)は生じません。**

### 11.1 (AT-a) は**定義的**

$\mathcal{PR}_N$ も $R_{M,N}$ も同じ座標 truncation($\hat{\mathbf Z}\times\hat F_2$ からの)⟹
$$\mathcal{PR}_N=R_{M,N}\circ\mathcal{PR}_M\quad(\forall M\le N)\qquad\textbf{✔ 選択独立}$$
⟹ 発案係が「唯一の正典逐語の未確認点」「ここが折れたら系が全滅」とした (AT-a) は、**truncation の推移性以上のものを要しません**。★ 第 I 部 §5.1 と合わせ、**I-SET-3 一手目 (i) も AT-a も、正典 pin としては既に済んでいます**。

### 11.2 (AT-b) — ★ **条件を 1 つ足す必要があります**

> **【補題 R-MULT】** $s,t\in GT(M)$ とし、**$R(s)$ が $N$ で settled** とする。このとき $R(s)\circ R(t)$ は定義され $=R(s\circ t)$。$R([0,1])=[0,1]$。

**証明**: $m$ 成分は整係数多項式ゆえ $\bmod N_{\rm ord}$ に落ちる ✔ $f$ 成分 $f_sE_{m_s,f_s}(f_t)$ が $\bmod N_{F_2}$ で定まるには $E_{m_s,f_s}(N_{F_2})\subseteq N_{F_2}$、これが $R(s)$ の settled 性(SETTLE-AUT)✔ また $f_s$ を $N_{F_2}$ の元で変えても $\pi_N\circ E$ は不変($E'(y)=n^{-1}E(y)n$・$\pi_N(n)=1$)⟹ 代表元の取り方に依らない ✔ ∎

⚠ **発案係の (AT-b) は無条件に書かれていますが、$R(s)$ が settled でなければ右辺の合成が groupoid で定義されません**(補題 COMP-T)。⟹ **要修正**。★ ただし SUBTOR の使用箇所ではすべて $R(s)$ が settled なので、**実害はありません**(§11.4)。

### 11.3 ★★ (AT-d) — **正しい**($B_3$ 水準の書き直し)

> **【補題 DIFF-S】** $M$ isolated、$T,T'\in GT(M)$、$R(T)$ と $R(T')$ が $GT(N)$ で**同核**とする。$D:=T'\circ T^{-1}$ とおくと **$R(D)$ は $N$ で settled**。

**証明**: (R2) より $\ker T_{R(T)}$ は $\bar T_T^{-1}(N/M)$ の引き戻し、同様に $T'$ 側は $\bar T_{T'}^{-1}(N/M)$。
$T'=D\circ T$ と補題 COMP-T($M$ isolated ⟹ $D$ は $M$ で settled)より $\bar T_{T'}=\bar T_D\circ\bar T_T$。よって
$$\bar T_T^{-1}\bigl(\bar T_D^{-1}(N/M)\bigr)=\bar T_{T'}^{-1}(N/M)=\bar T_T^{-1}(N/M)$$
$\bar T_T$ は**全単射**($M$ isolated)⟹ $\bar T_D^{-1}(N/M)=N/M$ ⟹ $\bar T_D(N/M)=N/M$ ⟹ (R2) で $\ker T_{R(D)}=T_D^{-1}(N/M)=N$ ⟹ **settled** ∎

★ **発案係の摘出どおり、効き所は「isolated ⟹ 降りた写像が全単射」**。SG-GAP-1 型の窓依存な単射性を**回避**している、という発案係の読みは**正しい**です。
★ **破綻点 ②($K_{F_2}\supseteq M_{F_2}$ の暗黙使用)は解消**: (R2) は $B_3$ 水準の式で、$\ker T_{R(T)}\supseteq\ker T_T=M$ は自動 ✔

### 11.4 ★★★ 定理 SUBTOR

> **【定理 SUBTOR】** $M\le N$、$M$ isolated、$G\le GT(M)$ 部分群。$X:=R_{M,N}(G)$、$S_X:=X\cap GT^{\rm settled}(N)$。このとき
> (i) $S_X\le GT^{\rm settled}(N)$ は部分群、(ii) $X$ は $S_X$ の後合成で閉じる、(iii) 各核類 $K$ について $X\cap GTSh(K,N)$ は **$S_X$-トーサーか空**。ゆえに
> $$\boxed{\ \lvert X\rvert=\lvert S_X\rvert\cdot\#\mathcal C_X,\qquad \mathcal C_X:=\{K:\ X\cap GTSh(K,N)\ne\emptyset\}\ }$$

**証明**:
(i) $[0,1]=R([0,1])\in S_X$ ✔。$d=R(D),d'=R(D')\in S_X$ ⟹ 補題 R-MULT($R(D)$ settled)で $d\circ d'=R(D\circ D')\in X$、SETTLED-GRP §3.2 で settled ⟹ $\in S_X$ ✔。逆元: R-MULT より $R(D)\circ R(D^{-1})=R([0,1])=[0,1]$ ⟹ $R(D^{-1})=d^{-1}\in X$、SETTLED-GRP §3.4 で settled ✔
(ii) $d=R(D)\in S_X$, $t=R(T)\in X$ ⟹ R-MULT で $d\circ t=R(D\circ T)\in X$ ✔
(iii) $t=R(T),t'=R(T')$ 同核 ⟹ 補題 DIFF-S で $d:=R(T'\circ T^{-1})\in S_X$、R-MULT で $d\circ t=R(T'\circ T^{-1}\circ T)=R(T')=t'$ ⟹ **推移的** ✔ 自由性は**定理 TORSOR**(第 I 部 §1.4)から継承($GT^{\rm settled}(N)$ の作用が自由 ⟹ 部分群 $S_X$ の作用も自由)✔ ∎

★ **発案係の破綻点 ③(自由性が折れると「約数」に弱まる)は不要**: 自由性は定理として立ちました。

### 11.5 ★★ 系(発案 7 号の中核)— 私の §8 を**真に強化**します

$M\le N$ を isolated 細分(Prop 3.14)とすると (AT-a) より $a_N(G_{\mathbf Q})=R_{M,N}\bigl(a_M(G_{\mathbf Q})\bigr)$、かつ $M$ isolated ⟹ $GT(M)$ は群・$a_M=\mathcal{PR}_M\circ\mathrm{Ih}$ は準同型 ⟹ $G:=a_M(G_{\mathbf Q})\le GT(M)$ ✔ SUBTOR を適用:

$$\boxed{\ S_{\rm arith}:=a_N(G_{\mathbf Q})\cap GT^{\rm settled}(N)\ \textbf{は部分群},\qquad \bigl\lvert a_N(G_{\mathbf Q})\bigr\rvert=\lvert S_{\rm arith}\rvert\cdot\#\mathcal C_{\rm arith}(N)\ }$$
$$\boxed{\ \textbf{各核類の算術点は }S_{\rm arith}\textbf{-トーサーか空}\ }$$

| 私の §8(補題 ARITH-T) | AT-1(SUBTOR) |
|---|---|
| $a_N(G_{\mathbf Q})$ は $S_{\rm arith}$ の作用で**安定**(軌道の和) | ★ **各類でちょうど 1 軌道**(推移的) |
| 比較は 2 因子に分解 | 同じ + **軌道数 = $\#\mathcal C_{\rm arith}$ と同定** |

★ **差を生んだのは補題 DIFF-S**(同核な算術点の「差」が**算術かつ settled**)。⟹ **発案係の勝ち**です。私は §8 で推移性を出せていませんでした(isolated 細分を経由する発想がなかった)。**採用**。

⚠ **残る前提**: (a) 正典 pin「(3.60) は shadow を shadow に送る」(定義ノート L176 の $R$ の定義に含まれる — 逐語 1 行)(b) $a_M$ の正典定義が閉包を取らない集合論的像であること(発案係の破綻点 ④ — 私も pin できていません)⟹【SS-GAP-6】。

---

## §12 【AT-2】機械的予言の検分

### 12.1 ★★ P1(u-剰余類)は **既存データで確認済み** — 再集計不要

第 I 部 系 D のとおり、ファイバー $=S\circ t_0$ ⟹ $u$-値は $u(S)\cdot u_{t_0}$。[1008,521] は $N_{\rm ord}=24$、settled の $u$-集合 $=\{1,7,13,19\}$(census83 §3)、非 settled 代表 $u_{t_0}=5$:

$$5\cdot\{1,7,13,19\}=\{5,35,65,95\}\equiv\{5,11,17,23\}\pmod{24}$$

census83 §3 の非 settled $u$ = **$\{5,11,17,23\}$** ⟹ ★★ **厳密一致**。
$$\boxed{\ \textbf{P1 は }\textbf{既に}\textbf{通っています — GAP 走行も再集計も不要}\ }$$
★ **副産物**: 「$u\equiv1\ (\mathrm{mod}\ 3)$ 法則」(裁定 999)と「ファイバー = settled 群の剰余類」は**同一の事実**でした。発案係は P1 を「1084 cert の均質分離より真に強い」と書いていますが、**実は census83(裁定 999)の時点で観測済みだった**、が正確な整理です。

### 12.2 P2(R-trace 量子化)— 設計は妥当・採用

$M=N\cap K_2=N^\diamond$ が成分の交わりであることは ★ **第 I 部 系 A**(=$\mathcal C(N)$ が連結成分)で保証されます ⟹ 発案係の破綻点 ② は**解消**。
予言「各類 trace は $\lvert S_M\rvert$ か 0・中間サイズが 1 つでも出たら死ぬ」は **SUBTOR の直接の帰結** ✔ ⟹ **今日走る反証テコとして採用**。
⚠ 実行注意: $\lvert PB_3/M\rvert\le168^2=28{,}224$ は上界であって実値ではありません($M=N\cap K_2$ の指数は 2 つの核の**積より小さい**ことが普通)。★ 先に指数だけ測れば規模が確定します(GAP 1 行)。

---

## §13 【AT-3】COORD と AT-Q1

### 13.1 COORD・飢餓判定は **系**(正しい)

$S_{\rm gen}:=\mathcal{PR}_N(\widehat{GT}_{\rm gen})\cap GT^{\rm settled}(N)$ が群であることは、$\mathcal{PR}_M(\widehat{GT}_{\rm gen})$ が $GT(M)$ の**有限部分モノイド ⟹ 部分群**(有限消約)ゆえ SUBTOR が適用できるため ✔

$$a_N(G_{\mathbf Q})=GT(N)\iff \lvert S_{\rm arith}\rvert\cdot\#\mathcal C_{\rm arith}=\lvert GT^{\rm settled}\rvert\cdot\#\mathcal C\iff \bigl(S_{\rm arith}=GT^{\rm settled}\ \wedge\ \mathcal C_{\rm arith}=\mathcal C\bigr)$$
(包含 $S_{\rm arith}\le GT^{\rm settled}$, $\mathcal C_{\rm arith}\subseteq\mathcal C$ の下では積の等号は両因子の等号と同値)⟹ **命題 COORD は正しい** ✔
**飢餓判定**: $a_N\cap GTSh(K,N)$ は $S_{\rm arith}$-トーサーか空 ⟹ trace$_K$ のサイズが $\lvert S_{\rm arith}\rvert$ 未満なら**空** ✔ 正しい。★ 第 I 部 §5.2 で棄却した「2 窓のサイズ比較」と違い、これは**同一窓内・類ごとに発火**するので **NOFIRE の障害を受けません** — ★ **I-SET-3 の代替として一級**です。

### 13.2 ★★ AT-Q1 — 摘出は**当たり**。既存結審の格下げが必要

$a$-bit $:=\bigl([-1,1]\in a_{N'}(G_{\mathbf Q})\bigr)$。
- $f_c=1\Rightarrow a_{N'}(c)=[-1,1]\Rightarrow a$-bit$=1$ ✔(十分)
- ⚠ **逆は言えません**: $a$-bit$=1$ は「∃$\sigma$: $a_{N'}(\sigma)=[-1,1]$」であり、$\chi_{\rm vir}(a_{N'}(\sigma))=-1$ は $\chi_{\rm cyc}(\sigma)\equiv-1$ を意味するだけで、$\sigma$ が複素共役である必要はありません(そのような $\sigma$ は指数 2 の開部分群の**剰余類全体**を走る)。

$$\boxed{\ \Longrightarrow\ \texttt{settled\_layer\_verdict} \S2.2\ \textbf{の}\ \text{「}f_c\ne1\Rightarrow[-1,1]\ \text{は算術像に入らない}\Rightarrow\text{一級」}\ \textbf{は}\ \textbf{無効}\ }$$
$f_c\ne1$ が言うのは $a_{N'}(c)\ne[-1,1]$ だけで、**他の $\sigma$ が $[-1,1]$ を取る可能性を排除しません**。
⟹ **[Q4-FINAL] の格を書き換えるべきです**: 「$f_c=1$ ⟹ 情報ゼロ(settled 層は完全被覆)」は**有効**、「$f_c\ne1$ ⟹ 非算術 shadow の実在」は**無効**(片側検定に格下げ)。⟹ 【SS-GAP-7】(裁定事項)。
★ **内在量は $\lvert S_{\rm arith}\rvert$**(発案係の整理どおり)。$N'$ では $GT^{\rm settled}(N')\cong C_2$ ゆえ $a$-bit$=1\iff S_{\rm arith}=GT^{\rm settled}(N')$。
★ **部分的な正の結果**(私の追加): $a_N|_{\mathcal A_N}$ は準同型(§8 補題 ARITH-T / SUBTOR)⟹ $a$-bit$=1$ は「$\mathcal A_{N'}\to C_2$ が全射」と同値 ⟹ **$G_{\mathbf Q}$ のある指数 2 の開部分群(= ある 2 次体)の名指しと同値**。$c$-正準化は一般には不成立ですが、**「2 次体を 1 つ特定する」という形の内在的な言い換えは可能**です。

---

## §14 【AT-4】Q-STAB と【AT-5】DESCENT

### 14.1 Q-STAB — 摘出は正しい・「救済」の理由は差し替え

条件式は私も独立に得ました((R2) と同じ):
$$\boxed{\ R_{N,H}(s)\ \text{が }H\ \text{で settled}\iff \bar T_s(H/N)=H/N\ }$$
自己同型が正規部分群を保つ保証はない ⟹ **自動でないという摘出は正しい** ✔ 同じ条件が類写像 $\mathcal C(N)\to\mathcal C(H)$ の well-defined 性を支配する、も**正しい**(同核 $t'=s\circ t$ の行き先の核が $\bar T_s^{-1}(H/N)$ でずれる)✔

⚠ **発案係の「救済」の理由は誤り**: 「札 1〜3 は源側が全 settled だから類写像の well-defined 性を要求しない」— しかし補題 R-MULT は **$R(s)$ が settled であること**を要求します(発案係の (AT-b) は無条件に書かれている・§11.2)。
★ **正しい救済理由**:
$$\boxed{\ \textbf{補題 DIFF-S は「必要な元 }D=T'T^{-1}\textbf{ については Q-STAB が}\textbf{自動で成り立つ}\textbf{」ことの証明}\ }$$
⟹ SUBTOR は Q-STAB を**仮定せず、必要な範囲で証明している**。結論(計数装置は Q-STAB から独立)は**維持**、理由は差し替え。

**修理案の選定**: ★ **(A) を推薦**(安定対の部分圏に制限)。理由: (B) の span は言葉が重く得るものがない、(C) の粗化は $\#\mathcal C$ を壊して I-SET-2 の計数と整合しなくなる(発案係も懸念しているとおり)。
★ **さらに正直な定式化を提案**(私の追加):
$$\boxed{\ GT(-)\ \textbf{は }R\ \textbf{により}\textbf{常に}\textbf{前層。壊れるのは }GT(N)\twoheadrightarrow\mathcal C(N)\ \textbf{への}\textbf{商の自然性}\ }$$
すなわち $\kappa_H\circ R_{N,H}:GT(N)\to\mathcal C(H)$ は**常に定義され**、$\kappa_N$ を経由して**分解するか**だけが Q-STAB。⟹ 統一像は「$GT(-)$ の前層 + 核類フィルトレーション」と書けば**無条件に正しく**、「三層の短完全列」は Q-STAB 部分圏上の言明として述べるのが正確です。

### 14.2 DESCENT — 採用(ただし格下げ)

単調性は $R$ の推移律、有限安定は値域有限 ⟹ **自明**。安定値 = genuine 座標は Cor 5.4 + isolated poset の cofinality(定義ノート L176-177)⟹ ★ 第 I 部 §5.1 で既に書いた等式の座標版。
⟹ **新規性は「降下プロファイルを窓の不変量として登録する」提案**にあり、そこは**採用**(U-5 の照準を非 isolated 窓へ引き継ぐ形として妥当)。
⚠ 発案係の破綻点 ②(depth 1〜2 が限界)は正直。★ **私の追加注意**: 「安定深度は非効果的」は正しいが、**各有限段が正当な上界**(発案係の言うとおり)なので、**depth 1 だけでも飢餓判定(§13.1)の入力として十分**です — 深掘りを待つ必要はありません。

---

## §15 第 II 部の記帳

- **【SS-GAP-5】(小・新)** $\ker T$($B_3$ 水準)と $\ker\varphi$($F_2$ 水準)の同値性。$c\notin N$ の窓では $PB_3/N$ 内で $F_2$ 像と $\langle c\rangle$ 像が交わりうるため自明ではない。⟹ 第 I 部の定理 TORSOR・第 II 部の SUBTOR は**どちらも $B_3$ 水準で証明したので影響を受けません**が、fixture 実装(marked factor map)がどちらで核を判定しているかは**確認事項**。
- **【SS-GAP-6】(小・新)** (a) 正典 pin「$R$ は shadow を shadow に送る」(3.60) の逐語 1 行。(b) $a_M$ の正典定義が集合論的像か(閉包を取らないか)。⟹ SUBTOR の系(算術版)の唯一の未 pin 部。
- **【SS-GAP-7】(中・新・裁定事項)** [Q4-FINAL] の格の書き換え(§13.2)。「$f_c\ne1$ ⟹ 一級」は**無効**。
- **閉鎖**: AT-1 の (AT-a)(§11.1・定義的)・(AT-d)(§11.3・証明)・破綻点 ②③。AT-2 の P1(§12.1・既存データで確認)・破綻点 ②。
- **要修正(発案係へ)**: (AT-b) は無条件では偽(§11.2)・AT-4 の「救済」の理由(§14.1)・P1 の新規性主張(§12.1: census83 で既観測)。
- ★ **第 II 部の新規部分(私)**: ① (R1)(R2) による $B_3$ 水準の書き直し(混線の解消)② 補題 R-MULT の条件の摘出 ③ 補題 DIFF-S の $B_3$ 版証明 ④ **定理 SUBTOR の完全証明**(自由性を定理 TORSOR から継承)⑤ SUBTOR が私の §8 を推移性の分だけ強化することの明示 ⑥ ★ **P1 が census83 で既に通っていることの発見**(exact な剰余類一致)⑦ **AT-Q1 の帰結として [Q4-FINAL] の片側検定への格下げ**と「2 次体の名指し」への言い換え ⑧ Q-STAB の救済理由の差し替えと「$GT(-)$ は常に前層・壊れるのは商の自然性」という定式化。
- **申告**: 紙のみ(第 II 部は機械走行ゼロ)。$u$/$c$ 非接触($f_c$ はビット構造のみ・値未接触)・封印非接触・prereg 非抵触・**Sol 未監査**・**verified ではない**(全 candidate 格)。
