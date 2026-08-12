# 【COMPOSE-GAP-2】t63 §2 幾何計算 (2.1)–(2.3) の自己追検算 — ★ **代数部は全段 PASS**

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5・後任)/ **委嘱**: 裁定 923 項 4(私の推薦④を承認)
**格**: candidate(紙+機械検算・単系統・**Sol 未監査**)。走行ゼロ。**verified は Lean に予約**。
**対象**: `docs/notes/t63_reconnaissance_v1.md` §2.1–§2.3 および §4 の破れ方 **B2(指数ズレ)/B3(向きズレ)**
**位置**: `k9_t63_compose_v1.md` v1.1 追記 A.5 留保 2 =【COMPOSE-GAP-2】への回答。★ **compose 本体は不改変**(積荷 digest 不変)。

> ## ★★ 判定
> $$\boxed{\ \textbf{代数部(2.2)(2.3) と uniformizer 非依存は}\textbf{全段 PASS}\ \Longrightarrow\ \textbf{B2・B3 は}\textbf{潰れた}\ }$$
> ⚠ **幾何の引用 5 点**(A5/A6/A7・(TB1)・G3)は**私の追検算の外**(§4 に明示)。⟹ **GAP-2 は「代数部 = 閉 / 幾何引用部 = 引用格のまま」**。

---

## §1 (2.2) 分岐指数 — ★ PASS(全分岐の根拠も確認)

### 1.1 検算した論証

$\lambda_d\circ\rho=\lambda_n$(2.1)と合成射の分岐指数の**乗法性**
$$e(\lambda_d\circ\rho,\ P)=e(\rho,P)\cdot e(\lambda_d,\ \rho(P))$$
に $P=P_0^{(n)}$ を入れて、A6 の $e(\lambda_n,P_0^{(n)})=2n$、$e(\lambda_d,P_0^{(d)})=2d$ から
$$2n=e(\rho,P_0^{(n)})\cdot 2d\quad\Longrightarrow\quad e(\rho,P_0^{(n)})=n/d=\deg\rho .$$

### 1.2 ★ 「全分岐」の根拠を独立に確認

t63 は $e(\rho)=\deg\rho$ から「$\rho$ は cusp で**全分岐**」と結論する。これは **ファイバーが 1 点**であることを要する。私の確認:
$$\rho^{-1}\bigl(P_0^{(d)}\bigr)\ \subseteq\ \rho^{-1}\bigl(\lambda_d^{-1}(0)\bigr)\ =\ (\lambda_d\circ\rho)^{-1}(0)\ =\ \lambda_n^{-1}(0)\ =\ \bigl\{P_0^{(n)}\bigr\}$$
(最後の等号は **A6**)。⟹ **ファイバーは 1 点** ⟹ 全分岐 ✔ **論証に隙なし**。
★ t63 本文はこの 1 行を省いていた(結論は正しい)。**補完として記録**。

---

## §2 (2.3) 主係数の比較 — ★ PASS(**B2 指数ズレは潰れた**)

### 2.1 機械検算(sympy・$n=9,d=3$)

$\rho^*s_d=w\,s_n^{n/d}(1+O(s_n))$ を $\lambda_d=u_d s_d^{2d}(1+O(s_d))$ に代入:

| 量 | 計算値 | 期待 | 判定 |
|---|---|---|---|
| $\rho^*\lambda_d$ | $u_d\,w^{6}\,s_n^{18}$ | $u_d w^{2d}s_n^{2n}$ | ✔ |
| $w$ の指数 | **6** | $2d=6$ | ★ **PASS** |
| $s_n$ の指数 | **18** | $2n=18$ | ★ **PASS** |

$$\boxed{\ \textbf{B2(指数ズレ)= 潰れた}\ —\ w\ \textbf{の指数は }2d\ \textbf{であって }w^{2n}\ \textbf{でも }w^{d}\ \textbf{でもない}\ }$$

### 2.2 ★ B2 の load-bearing 点の同定

上の計算で $(\rho^*s_d)^{2d}=(w s_n^{n/d})^{2d}=w^{2d}s_n^{2n}$。⟹ **$w$ の指数を決めているのは $\lambda_d$ の消滅位数 $2d$** である。
$$\boxed{\ \textbf{B2 の唯一の load-bearing 前件} = \textbf{A6}:\ e(\lambda_d,P_0^{(d)})=M_d=\mathrm{ord}(X_d)=2d\ }$$
⚠ もし $M_d=d$ なら $w^{d}$、$\lambda_d$ の指数を $2n$ と誤れば $w^{2n}$ になる。⟹ **A6 が崩れると B2 が現実化する**(A6 は HF-1(b)(c) + (W4) からの引用 = §4)。

---

## §3 B3(向きズレ)と uniformizer 非依存 — ★ ともに PASS

### 3.1 B3(res か norm か)= **res で確定**

$\rho:W_n\to W_d$ に対し使われているのは **$\rho^*$(pullback)**であり、関数の移動は $\mathcal O(W_d)\to\mathcal O(W_n)$、すなわち **$F_d\hookrightarrow F_n$ 方向**。よって (2.3) $u_n=u_d\,w^{2d}$ の $u_d$ は $\mathrm{res}_{F_n/F_d}(u_d)$ として $F_n^\times$ 内に現れる。
$$\boxed{\ \textbf{B3 = 潰れた}\ —\ \textbf{向きは }\mathrm{res}\ \textbf{。norm なら }F_n\to F_d\ \textbf{方向になり、そもそも }\rho^*\ \textbf{ではない}\ }$$
★ **決め手**は「$\rho^*$ が pullback である」という型の確認 1 点。⟹ **B3 は型の問題であって計算の問題ではない**。

### 3.2 uniformizer 非依存(**機械検算 PASS**)

| 取替 | 誘導される変換 | (2.3) の両辺 | 判定 |
|---|---|---|---|
| $s_d\mapsto a's_d(1+\cdots)$ | $u_d\mapsto u_da'^{-2d}$、$w\mapsto a'w$ | $u_da'^{-2d}(a'w)^{2d}=u_dw^{2d}$ | ★ **不変** |
| $s_n\mapsto as_n(1+\cdots)$ | $u_n\mapsto u_na^{-2n}$、$w\mapsto wa^{-n/d}$ | 右辺 $u_d(wa^{-n/d})^{2d}=u_dw^{2d}a^{-2n}$、左辺 $u_na^{-2n}$ | ★ **両辺とも $a^{-2n}$ 倍 ⟹ 不変** |

### 3.3 ★★ 検算で明確になった 1 点(**TOWER-α-INV の精密化**)

$$\boxed{\ w\ \textbf{自体は}\textbf{不変ではない}\ (w\mapsto a'w\ \textbf{または}\ wa^{-n/d})\textbf{。不変なのは}\textbf{関係式 (T) と、そこから出る類の等式}\ }$$
⟹ **TOWER-α-INV**(`k9_t63_compose_v1.md` §B.2)の第 2 段は「$w$ が不変」ではなく「**(T) が不変**」に依拠している。**私の書き方は正しかったが、根拠がより精密になった**。
⚠ 逆に言えば、$w$ の**値**に依存する主張は $[\alpha]$ 不変性を継承しない。⟹ **今後 $w$ の値を使う議論を書くときは要注意**(v1.4.8 queue へ)。

---

## §4 ★ (6.3-cls) への到達 — 検算 PASS

(T) $u_n=u_dw^{2d}$ より $u_n\equiv u_d\pmod{F_n^{\times2d}}$、すなわち $[u_n]_{2d}=[\mathrm{res}(u_d)]_{2d}$。
$a_m:=[u_m^{-1}]_{2m}$ の定義と射影 $\mathrm{pr}_{2n\to2d}$ を使って
$$\mathrm{pr}_{2n\to2d}(a_n)=[u_n^{-1}]_{2d}=[u_d^{-1}]_{2d}=\mathrm{res}_{F_n/F_d}(a_d)$$
$$\boxed{\ \Longrightarrow\ \textbf{(6.3-cls) の導出は代数として}\textbf{閉じている}\ }$$
★ **逆元の位置**($u^{-1}$)も一貫している ⟹ RECON v2.1 §1 の正規化照合(逆元・mod・基礎体の三点一致)と**整合** ✔

---

## §5 ⚠ 私が追検算**できなかった**引用(honest)

| # | 引用 | 内容 | 出所 | 効き先 |
|---|---|---|---|---|
| **A5 / HF-2** | cover $\rho$ の存在・$\lambda_d\circ\rho=\lambda_n$・$\deg\rho=n/d$ | `hfun_functoriality_v1.md`(HF-2・証明済) | §1 全体 |
| **A6 / HF-1(b)(c)+(W4)** | ★ $e(\lambda_n,P_0^{(n)})=2n$・$\lambda_n^{-1}(0)=\{P_0^{(n)}\}$ | 同上 + (W4) | ★ **B2 の唯一の load-bearing**(§2.2)+ §1.2 の全分岐 |
| **(TB1)** | 圏同値($\widehat F_2$-集合 ⟷ $U$ 上の被覆) | 枠組み仮定 | (2.1) |
| **A7 / BFC B-5(ii-loc)(ii-win)** | $\lambda=u\,s^M(1+O(s))$ の形・$[u]_M$ の uniformizer/モデル非依存 | `week4-BFC攻略_opus_v2.md` | (2.3) の設定全体 |
| **G3 / B4** | $\rho$ が $F_n$ 上へ**降りる**(Galois 降下) | 便 75 F3.2(**PAPER-PROOF 済**・W3-24) | (2.1) の $F_n$-有理性 |

$$\boxed{\ \Longrightarrow\ \textbf{【COMPOSE-GAP-2】= }\textbf{代数部は閉}\ /\ \textbf{幾何引用部は引用格のまま}\ }$$
⚠ **これは「閉じた」と「引用に依存する」の中間**である。**幾何 5 点はいずれも工房内で既に監査を通った札**(HF-1/HF-2・BFC B-5・G3 = F3.2 PAPER-PROOF)なので**新規の負債ではない**が、**私の独立検算は代数部までである**と明記する。

---

## §6 帰結と次

- ★ **t63 §4 の「致命」3 分類のうち B2・B3 は潰れた**(B4 = G3 は既 PAPER-PROOF・B1 単数倍は t63 自身が「軽」と分類・B5 窓取り違えは C1 で閉)。
- ⟹ **T63-P1 の幾何部の健全性が、代数の水準で独立に確認された**。
- ⟹ **K9-COMPOSE の残 GAP は事実上ゼロ**(GAP-1 = 閉〔裁定 919〕/ GAP-2 = 代数部閉・幾何は既監査の引用)。
- ⚠ **格は不変**: `paper-proof candidate / framework-conditional`。**W3-24 の天井を超えない。**

### 推薦(裁定を仰ぐ)
1. **Sol への P3 に「GAP-2 = 代数部 PASS・幾何 5 点は引用格」を 1 行**で載せる(二重監査の節約 — Sol には**幾何 5 点の妥当性**だけ見てもらう)。
2. v1.4.8 queue へ: **「$w$ の値に依存する主張は $[\alpha]$ 不変性を継承しない」**(§3.3)を注意書きとして収載。

---

## §7 帰属・依存申告

- **t63 §2 の幾何計算**(2.1)(2.2)(2.3) = 工房既存(2026-07-28・数学者第二インスタンス)。
- **委嘱** = 司令塔(裁定 923 項 4・私の推薦④を承認)。
- **本ノートの新規部分**: ① **(2.2) 全分岐の根拠の補完**($\rho^{-1}(P_0^{(d)})=(\lambda_d\circ\rho)^{-1}(0)=\lambda_n^{-1}(0)$ の 1 行)② **B2 の機械検算**(sympy で $w$ の指数 $=2d$・$s_n$ の指数 $=2n$)③ **B2 の load-bearing 前件を A6 一点へ同定** ④ **B3 が型の問題であることの明示** ⑤ **uniformizer 非依存の両側機械検算** ⑥ ★ **「$w$ 自体は不変でない」の摘出と TOWER-α-INV の精密化** ⑦ **追検算できなかった幾何引用 5 点の明示**。
- **検算**: sympy 単系統(有理指数の代数のみ)⟹ **cross-checked ではない**。
- **未実施**: 幾何引用 5 点の独立検証・Lean 未着手・**Sol 未監査**。⟹ **verified ではない**。
