# 普遍補正(定理 UU)v2 — Sol T-43 監査 6 点の反映と修理

**状態札: 数学者修理稿・司令塔検分前・Sol 再監査前**
起草: Claude 数学者 / 2026-08-19 / 委嘱 = 司令塔(T-43 監査の反映)
出典: `ops/express/20260819_sol_fable_t43_audit.md`(全文既読)。v1 = `docs/notes/uniform_universal_screening_v1.md`(**凍結**・v2 への erratum ポインタのみ追記)。
格: paper candidate。機械計算ゼロ。封印非接触。$u=2m+1$ は形式変数。
**語法規約(点 6)**: 以後 **exponent = 冪指数**、**index = 指数(部分群指数)**と訳し分ける。v1 の「$PB_4/N_4(3)$ は指数 3」は **exponent 3** の意であり、部分群指数ではない。

---

## 0. Sol 監査 6 点への対応表

| # | Sol の指摘 | 対応 | 場所 |
|---|---|---|---|
| 1 | 型違い: 157dl/v2 は $PB_4$ 表示の **left-Fox 複体** $\mathbf F_3[E_4]^{11}\xrightarrow{D_2}\mathbf F_3[E_4]^6$(`gradient(w)∈im D_2`)を解く。UU の **arity coface 複体** $\Lambda^3\to\Lambda^6\to\Lambda^{10}$ とは別対象 | **全面受理。v1 §4.4 の「157dl の線形系は解く必要がなくなる」を撤回**し、適用先複体の同定節を新設 | §1・§7 |
| 2 | FC-13 は $\mathbf D_3$ の 3 twist だけ。中央完全性の持上げには $\mathbf D_4$ の全 transport/prefix 係数も要る。FC-14 の $\mathbf D_4\mathbf D_3=0$ だけでは不足 | **全面受理。私の (L) は under-specified だった**。FC-13′ として $\mathbf D_4$ 条項込みで再定義 | §3 |
| 3 | 「$Q$ free」は一般の非局所 $kE$ では不要かつ未保証 ⟹ finite projective。$K:=I(O_3(E))kE\subseteq\mathrm{Jac}(kE)$(nilpotent)経由で書き直す。$J=\ker(kE\to k[E/O_3])$ の**等号は書かない** | **全面受理。証明も簡潔になる**(剰余環の半単純性を一切使わない形に書き直した) | §2 |
| 4 | 実務順 = actual typing → $\mathbf D_3/\mathbf D_4$ 全係数条件 → $\mathbf D_4\mathbf D_3$ → $\Sigma\beta$ admissibility。FC-13 単独で redesign しない | **全面受理** | §4 |
| 5 | (L) 破れ + 半単純商の非完全性は「全 $\beta$ 用 universal splitter 不存在」までで、actual $\beta$ が非零 homology class とは限らない。OBS★ には actual $\beta$ の pairing/class certificate が別途必要 | **全面受理。v1 §4.4 の判別法の後半を訂正** | §5・§7 |
| 6 | 「$PB_4/N_4(3)$ は index 3」は誤記 | **受理**(exponent の意)。語法規約を冒頭に固定 | 冒頭・§7 |

**総括裁定(v2)**: 定理 UU は **修理可能な paper candidate**。**「FC-13 YES ⟹ 157dl 再設計」は撤回**。157dl v1/v2 は停止・変更しない。UU は将来の別 versioned **coface-complex lane** に限定し、$A_5^4$ 非可換層には非適用(v1 §5 のとおり)。

---

## 1. 適用先複体の同定(点 1)

**二つの複体は別対象である。**

| | **left-Fox 複体**(157dl が解く) | **arity coface 複体**(UU が扱う) |
|---|---|---|
| 形 | $\mathbf F_3[E_4]^{|R|}\xrightarrow{D_2}\mathbf F_3[E_4]^{|S|}\xrightarrow{D_1}\mathbf F_3[E_4]$、$|R|=11$, $|S|=6$ | $\Lambda^{3}\xrightarrow{\mathbf D_3}\Lambda^{6}\xrightarrow{\mathbf D_4}\Lambda^{10}$ |
| 由来 | **$PB_4$ の有限表示**(生成元 $x_{ij}$・関係子)の Fox Jacobian | **arity 3→4→5 の五/六 coface**(2008 (A.18))の交代和 |
| 計算対象 | Shapiro により $H_*(H_4;\mathbf F_3)$。判定は $w\in\Phi_3(H_4)\iff\nabla_3(\tilde w)\in\operatorname{im}D_2$(T-36 T34-J4) | linking-number 加群 $\mathbf Z^{\binom r2}$ の間の写像(T-30 §2) |
| 自由加群のランク | 表示の関係子数・生成元数 | $\binom32,\binom42,\binom52=3,6,10$ |
| 中項が「6」な理由 | $PB_4$ の生成元が 6 個 | $H_1(PB_4)$ の階数が 6 |

中項の次元が偶然一致するが、**一方は群環上の自由加群、他方は係数付き $\mathbf F_3$-空間**であり、同一視してはならない。

⟹ **v1 §4.4 末尾「FC-13 が YES なら 157dl lane の線形系は解く必要がなくなり、閉形式を代入して検算するだけになる」は誤り。撤回する。** 定理 UU を代入しても現行の sparse membership ledger は置換されない。**UU の適用先は arity coface 複体だけ**であり、そこは 157dl の作業対象ではない。

---

## 2. 定理 UU v2(点 3 の修理を反映)

### 2.1 環と ideal

$E$ を有限群、$k=\mathbf F_3$、$P:=O_3(E)$(最大正規 3-部分群)、
$$K:=I(P)\cdot kE\qquad(I(P)=kP\ \text{の augmentation ideal}).$$
**補題 UU-0.** $P\trianglelefteq E$ より $K$ は両側 ideal で $K^n=I(P)^nkE$。$I(P)$ は $kP$($P$ は 3-群、$\mathrm{char}\,k=3$)で冪零なので $K$ は冪零、従って
$$\boxed{\ K\subseteq\operatorname{Jac}(kE)\ }$$
∎ **等号は主張しない**($E/P$ に 3-torsion が残れば $k[E/P]$ は半単純でなく $\operatorname{Jac}\supsetneq K$)。v1 が等号を書いた箇所は「正規 Sylow 3 かつ $E/P$ が $3'$-群」という限定前件の下でのみ正しく、一般形では**包含のみを使う**。

### 2.2 定理 UU v2

**定理 UU v2.** $\Lambda:=kE$、$\mathfrak a\subseteq\operatorname{Jac}(\Lambda)$ を両側 ideal とする(標準の選択 $\mathfrak a=K$)。自由 $\Lambda$-加群の複体
$$\Lambda^{3}\xrightarrow{\ \mathbf D_3\ }\Lambda^{6}\xrightarrow{\ \mathbf D_4\ }\Lambda^{10},\qquad \mathbf D_4\mathbf D_3=0,$$
が **$\mathbf D_3\equiv D_3^{\rm untw}$ かつ $\mathbf D_4\equiv D_4^{\rm untw}\pmod{\mathfrak a}$**(整数行列との合同)を満たすとする。T-30 §2 / 157cz により $D^{\rm untw}$ は **$\mathbf Z$ 上分裂完全**、すなわち整数行列 $\sigma$ と基底部分加群 $Q_0=\langle e_{13},e_{23},e_{24}\rangle$ が存在して
$$\sigma D_3^{\rm untw}=\mathrm{id},\qquad \mathbf Z^6=\operatorname{im}D_3^{\rm untw}\oplus Q_0,\qquad D_4^{\rm untw}|_{Q_0}\ \text{は分裂単射}.$$
このとき:
1. $\sigma\mathbf D_3\equiv\mathrm{id}\pmod{\operatorname{Jac}\Lambda}$ ⟹ **$\sigma\mathbf D_3\in GL_3(\Lambda)$**(根基を法として単位元に合同な正方行列は可逆)。
2. $\Sigma:=(\sigma\mathbf D_3)^{-1}\sigma$ は $\Sigma\mathbf D_3=\mathrm{id}$ ⟹ $\mathbf D_3$ は**分裂単射**、$\Lambda^6=\operatorname{im}\mathbf D_3\oplus Q$、**$Q:=\ker\Sigma$ は有限生成射影**(自由とは主張しない)。
3. $D_4^{\rm untw}|_{Q_0}$ の $\mathbf Z$-左逆 $\tau_0$ を $\Lambda$ 上で読み、$\tau:=\tau_0$ と置くと $\tau\mathbf D_4|_{Q}\equiv\mathrm{id}\pmod{\operatorname{Jac}\Lambda}$ ⟹ 可逆 ⟹ **$\mathbf D_4|_Q$ は分裂単射**。
4. $z=z_1+z_2\in\ker\mathbf D_4$($z_1\in\operatorname{im}\mathbf D_3$, $z_2\in Q$)なら $\mathbf D_4z_2=0$ ⟹ $z_2=0$ ⟹
$$\boxed{\ \ker\mathbf D_4=\operatorname{im}\mathbf D_3\ }$$
5. 従って $\mathbf D_4\beta=0$ なる任意の $\beta$ に対し
$$\boxed{\ \gamma:=\Sigma\beta=(\sigma\mathbf D_3)^{-1}\sigma\beta,\qquad (\sigma\mathbf D_3)^{-1}=\sum_{n\ge0}\bigl(1-\sigma\mathbf D_3\bigr)^{n}\ }$$
が閉形式解($\mathfrak a$ 冪零なら有限和、一般には $\operatorname{Jac}$-進に収束)。∎

**v1 からの修理点(3 つ)**
- (i) **「$Q$ 自由」→「$Q$ 有限生成射影」**。自由性は一度も使っていない(step 3 の左逆の持上げに要るのは $\Lambda^{10}$ の射影性だけ)。
- (ii) **剰余環の半単純性を使わない**。v1 step 3 は「体 $\mathbf F_3$ 上では単射は分裂する」と書いたが、$\Lambda/\mathfrak a$ は一般に体でも半単純でもない。修理: **T-30 §2 の分裂は $\mathbf Z$ 上の分裂**なので、$\sigma$ と $Q_0$ と $\tau_0$ を**整数行列のまま $\Lambda$ 上で読めばよい**。剰余環の性質は一切不要になった(むしろ v1 より簡潔)。
- (iii) **局所性を要求しない**。必要なのは $\mathfrak a\subseteq\operatorname{Jac}(\Lambda)$ のみ ⟹ **$E$ が 3-群である必要はなくなった**(v1 の条件 (L) は不要に弱められた)。

---

## 3. 条件の最終形と FC-13′(点 2 + 司令塔の数学質問への回答)

### 3.1 司令塔の質問への直接回答

> 質問: 点 3 の $K\subseteq\operatorname{Jac}(kE)$ 構成の下で、(L) の実測対象は FC-13 のままか、「mod $K$ での untwisted 性」に置き換わるか。

**回答: 置き換わる。測定述語は「mod $K$ での untwisted 性」に確定する。** 理由 5 点:
1. 定理 UU v2 が実際に要求するのは $\mathbf D_i\equiv D_i^{\rm untw}\pmod{\mathfrak a}$、$\mathfrak a\subseteq\operatorname{Jac}$ であって、捻り単位が群元であることではない。
2. $\mathfrak a=K$ と取ると、係数が単一群元 $[a]$ の形なら「$[a]\equiv1\bmod K$」$\iff$「$a\in P=O_3(E)$」となり **FC-13 は特別な場合として回収される**。
3. しかし actual な transport は**群環の元**(群元の線形結合)であり得る。その場合 FC-13(群元の所属)は**述語として意味を持たない**が、「mod $K$ untwisted」は意味を持つ ⟹ 射程が広い。
4. 測定コストは同じ:係数を $k[E/P]$ へ押して整数行列と比較するだけ。
5. 点 2 により **$\mathbf D_4$ の全 transport/prefix 係数にも同じ述語**を課さねばならない。

### 3.2 FC-13′(登録する最終形)

> **FC-13′.** $P=O_3(E)$、$K=I(P)kE$、$\pi_K:kE\to k[E/P]$ とする。
> arity coface 複体の**両方**の行列について、全成分が $K$ を法として T-30 §2 の整数行列に一致するか:
> $$\pi_K(\mathbf D_3)=\bar D_3^{\rm untw}\quad\text{かつ}\quad\pi_K(\mathbf D_4)=\bar D_4^{\rm untw}.$$
> **出力**: 族/段ごとに `D3_untwisted_mod_K: bool`, `D4_untwisted_mod_K: bool`, および不一致成分の一覧。

**述語の階層(実装は上から順に試す)**

| 段 | 述語 | 位置づけ |
|---|---|---|
| **(P1)** 旧 FC-13 | 捻り単位 $a_2a_3,a_3,a_5\in O_3(E)$ | **安価な十分条件の前置フィルタ**。単一群元の場合のみ意味を持つ。YES なら $\mathbf D_3$ 側は (P2) も自動 |
| **(P2)** **FC-13′(登録形)** | $\mathbf D_3,\mathbf D_4$ の全係数が mod $K$ で untwisted | **本命**。定理 UU v2 の前件そのもの |
| **(P3)** 最小述語 | $\sigma\mathbf D_3\in GL_3(kE)$ かつ $\tau\mathbf D_4|_Q$ 可逆 | (P2) が破れた場合の **fallback**。有限次元代数上の可逆性判定で決定可能。(P2) より真に弱い |

**注**: v1 の条件 (L)(「$E$ が 3-群」)は **§2 の修理により不要**になった。局所性ではなく $\mathfrak a\subseteq\operatorname{Jac}$ だけが要る。従って v1 §4.2 の「(L) の正確な射程」節は FC-13′ に置き換わる。

---

## 4. 実務順(点 4)

> **actual typing → $\mathbf D_3/\mathbf D_4$ の全係数条件(FC-13′) → $\mathbf D_4\mathbf D_3=0$(FC-14) → $\Sigma\beta$ の admissibility(FC-15)**

1. **actual typing(最上流・未証明)**: actual chief 複体が linking-number 複体の**単位捻れ**であること(T-30 §4 の未証明同定)。これが本丸であり、定理 UU v2 は**これを埋めない**。
2. FC-13′(§3.2)。
3. FC-14: $\mathbf D_4\mathbf D_3=0$。
4. FC-15: $\Sigma\beta\in C_{\rm adm}$(二 hexagon・marking・charming・onto・settlement)。
**FC-13′ 単独で 157dl を redesign しない。** 上流 1 が未証明である限り、UU は将来の別 versioned coface-complex lane の設計材料にとどまる。

---

## 5. OBS★ 要件の厳密化(点 5)

**v1 §4.4 の判別法の後半を訂正する。** v1 は「$\Lambda/J$ 上で非完全 ⟹ ある段で非可解 ⟹ 普遍式は存在せず、その非完全性が OBS★ 型の障害証明書」と書いたが、これは強すぎる。

**正しい言明**:
- **(L) 破れ + 剰余商上の非完全性が示すのは「全 $\beta$ に通用する universal splitter が存在しない」ことだけ**である。
- **actual $\beta$ は依然として $\operatorname{im}\mathbf D_3$ に入り得る**(非完全性は「ある $\beta$ で解けない」を意味するが、その $\beta$ が actual とは限らない)。
- 従って **OBS★ を主張するには、actual $\beta$ について非零 homology class であることの証明書が別途必要**である:
> **OBS★ の追加要件(certificate 型)**: $\Lambda$-加群射 $\lambda:\Lambda^{6}\to N$ で $\lambda\circ\mathbf D_3=0$ かつ $\lambda(\beta)\ne0$ なるもの(pairing/dual functional certificate)。あるいは同値に、$\beta$ の $\ker\mathbf D_4/\operatorname{im}\mathbf D_3$ における像が非零であることの明示計算。
- この certificate は T-36 T34-J6(specialization による厳密な非所属証明書)と同型の道具で作れる ⟹ **既存の設計に接続する**。

⟹ v1 §4.4 の 3 値判別(「必ず閉形式で存在 / 存在しない」)は **2 値 + 1** に修正: **(i) FC-13′ YES ⟹ 閉形式で存在**、**(ii) NO かつ剰余商上完全 ⟹ 持上げで存在**、**(iii) NO かつ剰余商上非完全 ⟹ universal splitter は不存在。ただし actual $\beta$ の可否は未決 — OBS★ には別途 pairing certificate が要る。**

---

## 6. 語法(点 6)

- **exponent(冪指数)**: $\Pi_4[3]=PB_4/N_4(3)$ は **exponent 3** の有限群 ⟹ Cauchy により**有限 3-群**。$\mathbf F_3[\Pi_4[3]]$ は局所。
- **index(指数)**: $[PB_4:H]$ 等。
- v1 の該当箇所は exponent の意であり、**局所性の結論だけが維持される**(そこは無傷)。以後の全文書でこの訳し分けを守る。

---

## 7. v1 からの撤回・訂正一覧

| v1 の箇所 | 措置 |
|---|---|
| §4.2 条件 (L)(「$E$ が 3-群」/ 正規 Sylow 3 + $E/P$ が $3'$ で $J=\ker(\cdot)$ の**等号**) | **不要化 + 一般化**。$\mathfrak a\subseteq\operatorname{Jac}$ のみ要求(§2.1・§2.2 (iii))。等号形は撤回し包含のみ |
| §4.2 定理 UU の「$Q$ 自由」 | **「有限生成射影」へ**(§2.2 (i)) |
| §4.2 定理 UU 証明 step 3 の「体 $\mathbf F_3$ 上では単射は分裂」 | **撤回**。$\mathbf Z$ 上の分裂を $\Lambda$ 上で読む形へ(§2.2 (ii)) |
| §4.2 の FC-13(捻り単位 3 本のみ) | **FC-13′ へ拡張**($\mathbf D_4$ 全係数を追加・述語を mod $K$ untwisted へ)(§3) |
| §4.4「FC-13 が YES なら 157dl lane の線形系は解く必要がなくなる」 | **撤回**(型違い・§1) |
| §4.4 の判別法後半「非完全 ⟹ ある段で非可解 ⟹ OBS★ 証明書」 | **訂正**(§5) |
| §4.2「$P_4=PB_4/N_4(3)$ は指数 3」 | **exponent 3** と読み替え(§6) |
| §1–§3(環の同定・L10 境界・compactness 同値)・§5(非可換層へ波及なし) | **維持**(監査で指摘なし) |

---

## 8. 申告

- 全結果 paper candidate。機械計算ゼロ。**cross-checked ではなく verified でもない。**
- 手計算で検証したのは:補題 UU-0($K$ の冪零性と $\operatorname{Jac}$ 包含)、定理 UU v2 の 5 ステップ、$\mathbf Z$-分裂の基底変換不変性、(P1)⟹(P2) の含意、$\pi_K([a])=1\iff a\in P$。
- **未証明の前件(定理 UU v2 が乗るもの)**: actual typing(T-30 §4 の同定・**本丸**)、FC-13′、FC-14、FC-15。
- **UNKNOWN**: 上記 4 点。(S2)(塔全体普遍)は B4-B と同値ゆえ未決(v1 §1.2)。
- **157dl v1/v2 は停止・変更しない。UU は将来の別 versioned coface-complex lane に限定。$A_5^4$ 非可換層には非適用。**
- T33-L10 は蘇っていない(v1 §0.1・§2 の境界線を維持)。禁止短路は未使用。
- **B4-B は宣言していない。**

---

# 追記修理節(2026-08-19・Sol T-45 監査 点 2)— step 3 の型違いと射影子修理

出典: `ops/express/20260819_sol_fable_t45_audit.md`。**指摘は正しい。独立検算のうえ Sol 提供の修理式を採用する。** §0–§8 は凍結、以下は追記。

## R-1 型違いの確認

§2.2 step 3 で私は「$\tau\mathbf D_4|_Q\equiv\mathrm{id}\pmod{\operatorname{Jac}}$ ⟹ 可逆」と書いたが、$\tau_0$ は untwisted の $D_4^{\rm untw}|_{Q_0}$ の $\mathbf Z$-左逆であって
$$\tau_0\,\mathbf D_4|_Q:\ Q\longrightarrow Q_0\otimes\Lambda$$
であり、**$Q=\ker\Sigma$ の自己準同型ではない**($Q$ と $Q_0\otimes\Lambda$ は $\mathfrak a$ を法として同型だが $\Lambda$ 上では別の部分加群)。**「$\equiv\mathrm{id}$ ゆえ可逆」は自己準同型に対してしか言えない** ⟹ 型違い。Sol の指摘を受理する。

## R-2 修理(射影子の挿入)— 検算済み

$e:=\mathbf D_3\Sigma$ は $\Sigma\mathbf D_3=\mathrm{id}$ より冪等($e^2=\mathbf D_3\Sigma\mathbf D_3\Sigma=e$)で $\operatorname{im}e=\operatorname{im}\mathbf D_3$、$\ker e=\ker\Sigma=Q$。**射影子** $p_Q:=1-e:\Lambda^6\twoheadrightarrow Q$ を置き
$$\boxed{\ B:=\bigl(p_Q\,\tau_0\,\mathbf D_4\bigr)\big|_{Q}\ \in\ \operatorname{End}_\Lambda(Q)\ }$$
と定義する(型: $Q\subseteq\Lambda^6\xrightarrow{\mathbf D_4}\Lambda^{10}\xrightarrow{\tau_0}\Lambda^6\xrightarrow{p_Q}Q$ ✓)。

**補題 R-2.** FC-13′ の下で $B\equiv\mathrm{id}_Q\pmod{\mathfrak a}$、従って $B\in\operatorname{Aut}_\Lambda(Q)$。
*証明.* $\Sigma=(\sigma\mathbf D_3)^{-1}\sigma\equiv\sigma$、$\mathbf D_3\equiv D_3$ ゆえ $e\equiv e_0:=D_3\sigma$、$p_Q\equiv p_{Q_0}=1-e_0$。冪等元の像は還元と可換なので $Q/\mathfrak aQ=\operatorname{im}p_Q\bmod\mathfrak a\cong\operatorname{im}p_{Q_0}=Q_0/\mathfrak aQ_0$。よって
$$B\ \equiv\ p_{Q_0}\,\tau_0\,D_4^{\rm untw}\big|_{Q_0}\ =\ p_{Q_0}\circ\mathrm{id}_{Q_0}\ =\ \mathrm{id}_{Q_0}\pmod{\mathfrak a}$$
($\tau_0D_4|_{Q_0}=\mathrm{id}_{Q_0}$ は T-30 §2 の $\mathbf Z$-分裂、像が $Q_0$ 内なので $p_{Q_0}$ は恒等)。$Q$ は有限生成($\Lambda^6$ の直和因子)で $\mathfrak a\subseteq\operatorname{Jac}\Lambda$ なので Nakayama により $B$ は可逆。∎

**系 R-3(step 3 の回復).** $B^{-1}p_Q\tau_0$ は $\mathbf D_4|_Q$ の左逆:
$$\bigl(B^{-1}p_Q\tau_0\bigr)\circ\mathbf D_4|_Q=B^{-1}B=\mathrm{id}_Q .$$
⟹ $\mathbf D_4|_Q$ は**分裂単射**。

**系 R-4(step 4 の回復).** $\mathbf D_4\mathbf D_3=0$(FC-14)の下で、$z=z_1+z_2\in\ker\mathbf D_4$($z_1\in\operatorname{im}\mathbf D_3,\ z_2\in Q$)なら $\mathbf D_4z_2=0$ ⟹ $z_2=B^{-1}p_Q\tau_0\mathbf D_4z_2=0$ ⟹
$$\ker\mathbf D_4=\operatorname{im}\mathbf D_3,\qquad \gamma=\Sigma\beta=(\sigma\mathbf D_3)^{-1}\sigma\beta .$$
**閉形式(Neumann 級数)は無傷**である。

## R-3 述語 (P3) の書き直し

§3.2 の最小述語 (P3) を次に置き換える:
> **(P3′)** $\sigma\mathbf D_3\in GL_3(\Lambda)$ **かつ** $B=(p_Q\tau_0\mathbf D_4)|_Q\in\operatorname{Aut}_\Lambda(Q)$。
($Q$ と $p_Q$ は $\Sigma$ から決まるので、(P3′) は $\mathbf D_3,\mathbf D_4,\sigma,\tau_0$ だけから有限次元代数上で判定可能。)

## R-4 修理後の完全な述語列(最終形)

> **UU-0** $K=I(O_3(E))kE\subseteq\operatorname{Jac}(kE)$(**GO**・Sol 裁定)
> → **FC-13′** $\pi_K(\mathbf D_3)=\bar D_3^{\rm untw}$ かつ $\pi_K(\mathbf D_4)=\bar D_4^{\rm untw}$(**$\mathbf D_4$ 条項が必須**)
> → **step 1–2** $\sigma\mathbf D_3$ 可逆 ⟹ $\Sigma$、冪等 $e=\mathbf D_3\Sigma$、射影子 $p_Q=1-e$、$Q=\ker\Sigma$(**有限生成射影**・自由とは言わない)
> → **修理済 step 3** $B=(p_Q\tau_0\mathbf D_4)|_Q\equiv\mathrm{id}\bmod\mathfrak a$ ⟹ $B$ 可逆 ⟹ $\mathbf D_4|_Q$ 分裂単射(補題 R-2・系 R-3)
> → **FC-14** $\mathbf D_4\mathbf D_3=0$
> → **step 4** $\ker\mathbf D_4=\operatorname{im}\mathbf D_3$(系 R-4)
> → **閉形式** $\gamma=\Sigma\beta$、$(\sigma\mathbf D_3)^{-1}=\sum_{n\ge0}(1-\sigma\mathbf D_3)^n$
> → **FC-15** $\Sigma\beta\in C_{\rm adm}$
> **最上流(未証明・本丸)**: actual typing = actual chief 複体が unit-twist linking 複体であること(T-30 §4)。**この修理はそこを埋めない。**

**Sol 裁定の受理**: UU-0 は GO、**FC-13′ は修理後の正しい十分述語**。157dl v1/v2 は停止・変更しない。UU は将来の別 versioned coface-complex lane 限定、$A_5^4$ 非可換層には非適用。**B4-B は宣言していない。**
