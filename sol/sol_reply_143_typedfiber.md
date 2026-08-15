# Sol 便 143 返信 — typed fiber は全元で局所通過するが、単一窓の陽性は屋根を決着しない

## 0. 結論

便 143 を §0 から §4 まで順に処理した。入力
`ops/inbox_codex/sol_task_143_typedfiber.txt` の SHA-256 は
`4fbcf170181eb0293596c4e21b7f3211e79b423949e181a9d17adf41931e8173`
である。

便 142 の `PENT-NODESCENT`、`GATE_FAILED` の撤回、および式 (4)

\[
C_M=\bigcap_{i=1}^{4}p_i^{-1}(M),\qquad
\widetilde K=C_M\cap\widetilde{\mathbf N}^{*}
\tag{1}
\]

の型は受理する。ただし、便 143 §1.3 の

\[
\text{「一つの outside-}A_{\rm ar}\text{ 元が }\widetilde K
\text{ で通過」}
\Longrightarrow
\mathfrak G_{\widehat{GT}}\ne A_{\rm ar}
\tag{2}
\]

は成立しない。単一の有限窓での通過は genuine 性の必要条件の一つにすぎない。
2008 Cor. 3.13 は genuine を **全ての**細分窓への survival と同値にしている。
原文 PDF p.38 のページ画像でもこの全称量化を再確認した。従って陰性は一窓で
確定できるが、陽性は一窓から確定できない。

さらに (1) の窓については、列挙より強い一様な紙の結論が出る。

> **定理 `TYPED-FIBER-ALLPASS-143`.** 任意の
> \(g\in GT(M)\) に対し、\(g\) へ reduce する charming B4 shadow
> \(\widetilde g\in GT^\heartsuit(\widetilde K)\) が少なくとも一つ存在する。
> とくに (2.20)-PASS を含む reduction fiber は 972 個すべてで非空である。

従ってこの typed 窓が与える局所像は

\[
\operatorname{Im}\!\left(
 GT^\heartsuit(\widetilde K)\longrightarrow GT(M)
\right)=GT(M).
\tag{3}
\]

これは **局所全通過**であり、\(\widehat{GT}\) からの大域的持上げ 972/972 ではない。
よって `SETTLED_NOT_LIFTABLE` も `SETTLED_LIFTABLE` も出せず、972 屋根の
\(\widehat{GT}\) 水準のビットは未決である。

## 1. 式 (1) の誘導 B3 窓を展開する

五つの coface を \(\Phi\)、
\(\lambda_{i,\varphi}:=p_i\circ\varphi:PB_3\to PB_3\) と書く。
2008 (2.4) と逆像の分配則、B4-CANON から

\[
\begin{aligned}
K_3:=(\widetilde K)_{PB_3}
&=\bigcap_{\varphi\in\Phi}\varphi^{-1}
   (C_M\cap\widetilde{\mathbf N}^{*})\\
&=\mathbf N_0\cap
  \bigcap_{\substack{1\le i\le4\\\varphi\in\Phi}}
  \lambda_{i,\varphi}^{-1}(M).
\end{aligned}
\tag{4}
\]

ここで \((\widetilde{\mathbf N}^{*})_{PB_3}=\mathbf N_0\) を使った。
従って \(K_3\le M\) で、便のいう reduction map は確かに存在する。

既存の 20 合成完全表には次の二種類しかない。

1. 8 本は \(F_2\) 上で自然な \(M\)-商写像そのもの。
2. 12 本は \(x,y\) の像が同一巡回群に入る退化写像。

この分類は NW(7) の特殊な元の値ではなく、\(p_i\circ\varphi\) の語の形から
出る。\(M=K^{(9)}\cap N_{S4}\) は \(c\) を含むため、direct 行に現れ得る
中心因子も \(PB_3/M\) で消える。従って

\[
PB_3/K_3\hookrightarrow
(PB_3/\mathbf N_0)\times(PB_3/M)^{20},
\qquad
F_2/(K_3\cap F_2)\hookrightarrow P_7\times H_M^{20},
\tag{5}
\]

\[
H_M=F_2/M_F\cong PB_3/M,\qquad P_7=F_2/V.
\]

という faithful な座標表示を使える。重複する direct 座標は残してよい。

また \(M_{\rm ord}=18\)、\((\widetilde{\mathbf N}^{*})_{\rm ord}=7\) で、
direct 座標が 18、NW 座標が 7 を実現するので

\[
(\widetilde K)_{\rm ord}=\operatorname{lcm}(18,7)=126.
\tag{6}
\]

## 2. `TYPED-FIBER-ALLPASS-143` の証明

### 2.1 任意の target と恒等 NW residue を同時に持ち上げる

\(g=[m,\bar f]_M\in GT(M)\) を任意に取る。charming 性から
\(\bar f\in H_M'\) である。便 142 の Goursat 計算は

\[
(\alpha,\beta)([F_2,F_2])=H_M'\times P_7'
\tag{7}
\]

を与える。従って

\[
f^\sharp\in[F_2,F_2],\qquad
\alpha(f^\sharp)=\bar f,qquad
\beta(f^\sharp)=1
\tag{8}
\]

を選べる。さらに中国剰余定理で

\[
\mu\equiv m\pmod {18},\qquad
\mu\equiv0\pmod7
\tag{9}
\]

を選ぶ。すると \([\mu,f^\sharp]\) は \(M\) 側で \(g\)、NW 側で恒等
shadow \([0,1]_{\mathbf N_0}\) に reduce する。さらに
\(u=2\mu+1\) は 18 と 7 の双方に素、従って 126 に素である。

### 2.2 hexagon は (4) の全座標で成立する

式 (5) の座標ごとに簡約 hexagon の二つの defect を調べる。

- NW 座標では (8)(9) により恒等 shadow なので成立する。
- 8 本の direct \(M\) 座標では、\([\mu,f^\sharp]\) は
  \([m,\bar f]_M=g\) と同じなので成立する。
- 12 本の退化座標では \(\lambda(x),\lambda(y)\) が一つの巡回群に入る。
  \(f^\sharp\in[F_2,F_2]\) だから、\(f^\sharp\) および
  \(\theta(f^\sharp),\tau(f^\sharp),\tau^2(f^\sharp)\) の像は 1 である。
  第 1 hexagon は直ちに 1、第 2 hexagon の残りは、巡回群内で
  \[
  \lambda(x)^\mu\lambda((xy)^{-1})^\mu\lambda(y)^\mu=1
  \]
  となる。

(5) は単射なので、二つの hexagon defect は \(K_3\cap F_2\) に入る。

### 2.3 charming/SURJ も自動である

\(f^\sharp\) は交換子語そのものなので charming の代表条件を満たす。
\(T^{PB_3}_{\mu,f^\sharp}\) とその \(F_2\) 制限を (5) の各座標へ写すと、

- NW 座標では恒等 shadow の自己同型、
- direct \(M\) 座標では settled な \(g\) の自己同型、
- 退化巡回座標では \(u\) 乗写像

になる。最後の写像も \(\gcd(u,18)=1\) により自己同型である。生成元上の
この可換性から \(T(K_3)\subseteq K_3\) および
\(T(K_3\cap F_2)\subseteq K_3\cap F_2\) が従い、両写像は対応する有限商の
自己準同型になる。もしその核元があれば、各座標自己同型の逆を使って元自身の
全座標が 1、(5) の単射性から元は 1 である。従って
\(T^{PB_3}\) と \(T^{F_2}\) はともに有限群上の単射、したがって全射である。
(6) と \(\gcd(u,126)=1\) は PB2 の全射も与える。2008 Prop. 2.10 により
GT-shadow の全射条件が揃い、\(F_2\) 全射と交換子代表により charming 条件も揃う。

### 2.4 pentagon は二つの因子で同時に成立する

\(D(f^\sharp)\) を (2.20) の pentagon defect とする。

まず \(C_M\) 側を見る。各 \(p_i\) 座標では、五つの
\(p_i\circ\varphi\) のうち二つが direct、三つが巡回退化である。
交換子語は退化三項で 1 となり、direct 二項は (2.20) の両辺で同じ項として
残る。これは B4-VAC の証明を \(M\) に適用した同じ語計算であり、

\[
D(f^\sharp)\in C_M.
\tag{10}
\]

次に (8) の \(\beta(f^\sharp)=1\) は \(f^\sharp\in V\) をいう。
\(V=\gamma_5(F_2)F_2^7\) は verbal なので、五つの coface の各々が
\(f^\sharp\) を \(\mathcal V(PB_4)=\widetilde{\mathbf N}^{*}\) に送る。
従って

\[
D(f^\sharp)\in\widetilde{\mathbf N}^{*}.
\tag{11}
\]

(10)(11) から \(D(f^\sharp)\in\widetilde K\)。よって
\([\mu,f^\sharp]\in GT^\heartsuit(\widetilde K)\) は pentagon-pass で、
しかも \(g\) へ reduce する。\(g\) は任意だったから定理と (3) が従う。∎

## 3. 便 143 §1.2–§1.3 の裁定

### 3.1 陰性方向

便 143 §1.2 の陰性規則は正しい。一つの outside-\(A_{\rm ar}\) 元について、
ある有限 B4 窓への **全** reduction fiber が空、または全て (2.20)-FAIL
なら、その元は \(\widehat{GT}\) から来ない。実像が
\(A_{\rm ar}\) を含む部分群で指数 3 の二択にあることから、実像は
\(A_{\rm ar}\) に確定する。

ただし今回の \(\widetilde K\) では定理により全 972 fiber が少なくとも一つの
PASS を含む。従ってこの窓から陰性証明書は出ない。

### 3.2 陽性方向

便 143 §1.3 は **FAIL** と裁定する。正しい包含は

\[
\mathfrak G_{\widehat{GT}}(M)
\subseteq
\operatorname{Im}\bigl(GT^\heartsuit(\widetilde K)\to GT(M)\bigr),
\tag{12}
\]

であって逆包含ではない。今回 (3) により (12) の右辺が \(GT(M)\) 全体に
なっただけである。2008 Cor. 3.13 の正しい陽性条件は、一窓の PASS ではなく
**全ての** B4 細分窓での survival、同値に互換な逆極限元の存在である。

実際、既存の `b4_direct_adjudication_feasibility_v1_2.md` §4.1 も
「陰性は 1 窓で有限、陽性は切り詰めから出ない」と明記している。
従って (3) と指数 3 の二分法を合成して `SETTLED_LIFTABLE` とするのは
有限-to-family の過大格付けになる。

## 4. 要求された実装・較正・資源への回答

便は「全数列挙に固執せず、代数で決まるならそれでよい」と明記している。
本便ではその代数路が (3) まで閉じたため、
`m972_b4_fiber.g` と `check_b4_m972_fiber.py` を新造して巨大 fiber を走査する
必要はない。存在判定の witness は各 target に対し (8)(9) で一様に構成される。

したがって本便で新しい producer/checker、GHA workflow、commit、push、dispatch は
作っていない。新実装が無いので N⁽¹⁹⁾ の 216 を「各新実装で再現した」とも
申告しない。既存の GAP/Package GT による 216 の一致は便 142b の在庫 5 として
そのまま維持する。

この紙の閉鎖が依存する既存有限入力は、20 合成表の direct 8 / cyclic 12 分解、
\(M_{\rm ord}=18\)、\(\mathbf N_{0,\rm ord}=7\)、および便 142 の
導来 Goursat 全射 (7) である。新しい生値や封印値は使っていない。

## 5. 在庫 1–8

| # | 状態 | 本便後の正確な会計 |
|---:|---|---|
| 1 | **未消化** | \(R_7\) 上の五 coface を保持した direct full-pentagon 計算は未実行。本証明は verbal 性で恒等 NW residue だけを選び、この全表を代行しない |
| 2 | **消化** | 型付き \(\widetilde K=C_M\cap\widetilde{\mathbf N}^{*}\) の reduction fiber の存在判定を代数で完了。全 972 target で PASS fiber 非空、局所像は 972/972 |
| 3 | **未消化** | Prop. 3.3 + CORE-4 による cofinal/source refinement の列挙・族定理は未了 |
| 4 | **未消化** | 四つの \(Q_8\) 窓の shadow/pentagon/source-kernel 測定は未了 |
| 5 | **消化済みを維持** | 既存 Package GT 較正。N⁽¹⁹⁾ pentagon-pass 216 が GAP と一致。本便で再実行したとは数えない |
| 6 | **消化済みを維持** | MIRROR-SHADOW-B4。現用六窓の mirror 線は既裁定どおり空 |
| 7 | **未消化** | \(B=2|Q|\) の central \(C_2\) event と、それ以後の kernel order は未走 |
| 8 | **未消化** | 四 cofinal 命題の同一族上の証明は 0 本のまま |

従って消化済みは **2, 5, 6**、未消化は **1, 3, 4, 7, 8** である。

## 6. endgame scope と格

- 本便で測ったのは、単一の B4 窓 \(\widetilde K\) から B3 target \(M\) への
  **局所** reduction 像である。
- \(\widehat{GT}\) 水準の像 \(\mathfrak G_{\widehat{GT}}(M)\) は未決。
- \(\widehat{GT}_{\rm gen}\) 水準の A 型/B 型二分法や (U-10) について新しい
  結論を出していない。
- `TYPED-FIBER-ALLPASS-143` は paper-proof。20 合成表には既存の独立再導出が
  あるが、定理全体の独立 checker は無く、Lean certificate も無い。
- `verified` とは呼ばない。finite-to-family の格上げも行わない。
- \(A_{\rm ar}\), \(S=\mathrm{PSL}(2,8)\), \(P_7\), \(R_7\),
  \(C_M\), \(\widetilde K\) は分記した。
- 封印 3 量、`u`、`c`、sealed K5 は非接触。本便で変更した作業木対象は
  この返信だけである。

## 7. provenance

| 入力 | SHA-256 |
|---|---|
| `ops/inbox_codex/sol_task_143_typedfiber.txt` | `4fbcf170181eb0293596c4e21b7f3211e79b423949e181a9d17adf41931e8173` |
| `sol/sol_reply_142_b4.md` | `c5c8b685a856003a0515ad5c1bbae2922fba7e0a7bc47b0f06a77064a0f12dcc` |
| `docs/notes/b4_direct_adjudication_feasibility_v1_2.md` | `7d1f882da75fce8fddaa2303afb8fb0515231771a15984d61718175c35bee990` |
| `docs/notes/b4_theorem_check_v1.md` | `70ef1991ea3d4728e4a61bc43e4a468269a396c8db8dec3270f61f9818eae8b6` |
| `search/certs/d972_phase0_v1_20260813.json` | `dbd34c59638363762cee1eb77720625704935e50a269528df0f88daeaf3841fe` |
| `search/certs/d972_h1_ns4_v1_20260813.json` | `a100893d151b4f4885bab8d950d09fc9d7b875d5651481ae9496f6edc93c8292` |
| `search/certs/cal_b4_integrated_v2_20260806.json` | `71b6fa73b99c4afafc624df844bda61d654248908bc813a4651864d603d44f1b` |

novelty grep は `TYPED-FIBER-VAC` / `TYPED-PASS-ALL` /
`LOCAL-PASS-972` / `ONE-WINDOW-PASS` の四語で 0 hit だった。

FIBER_VERDICT: INVENTORY_2_5_6
