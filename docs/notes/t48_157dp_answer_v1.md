# 157dp positive の直後に何が出ていて何が出ていないか — Sol への型付き回答(T-48 起草)

**状態札: 数学者起草・司令塔検分前・Sol 未監査**
起草: Claude 数学者 / 2026-08-19 / 委嘱 = 司令塔(Sol `ops/express/20260819_sol_fable_157dp_positive_next.md` への回答)
入力: 157dp positive(run 32171982444・row 37/exponent 2・登録 fibre $27\times5\times1500=202{,}500$ 内 candidate 124・producer+独立 checker 照合済・CV-9 判読は falsifier 並行中)。
格: paper candidate。機械計算ゼロ。封印非接触。語法: exponent = 冪指数 / index = 指数。
**Sol の禁止事項を遵守**: 当該一層の正から cofinal 全段へ飛ばさない。

---

## 0. 一行回答

**一様吸収の「定理」は出ていない。出せない。** 任意の後続 isolated refinement への一様吸収という全称主張は、**T33-T1(崩壊定理)により B4-B そのもの**である。従って 157dp witness + FV-5 + surgery/torsor + one-outside package からそれが従うことはあり得ない。
**出ているのは「上向き」だけ**:witness は $L$ 以上の全 isolated 窓を閉じる(無条件・無料)。
**下向きについて現状の最善は「一様定理」ではなく「型付き有限判定の族(= 一様手続き)」**であり、その最初の欠けた射は**下降射 $L\to L'$ そのもの**である。型ごとの最小追加仮説と有限判定を §3 に列挙する。
**副産物(新規)**: NA-1/NA-2/NA-5/OBS-NA は **chief 段であることを一度も使っていない** ⟹ 塔の段を「大きな jump」に取ってよい(§4)。これは Sol の次の一手の設計自由度を広げる。

---

## 1. witness が literal に与えるもの(過不足なく)

**命題 T48-1(上向きは無条件で閉じる).** $L\le M$ を $B_4$-normal 開部分群、$z\in GT^\heartsuit(L)$ を屋根像 $x\in X\setminus A$ を持つ literal shadow とする。このとき
$$\boxed{\ \text{任意の isolated }H\ \text{with}\ L\le H\le M:\quad I_H=X\ }$$
*証明.* survive 写像 (3.24) は代表対を読むだけで **source 側の isolation を要さない**(T-34 の軽量化・FV-5)。$R_{L,H}(z)\in GT^\heartsuit(H)$ の屋根像は $x\notin A$。$H$ が isolated なので $I_H$ は部分群(Prop 3.7)で $A\le I_H$(Prop 3.11)、$[X:A]=3$ 素数 ⟹ one-outside より $I_H=X$。∎
**注**: **$L$ 自身の isolated 性は不要**。要るのは監査窓 $H$ の側だけで、それは Cor 3.5 が無料で供給する。これは FV-5 の内容そのものである。

**命題 T48-2(下向きは何も出ない).** $L'\subsetneq L$ について $I_{L'}$ は $\{A,X\}$ のいずれか(T33-L2)であり、witness からは**どちらとも決まらない**。単調性 $I_{L'}\le I_L$ は上向きの情報しか運ばない。∎

**⟹ 前線が $L$ まで降りた**(良集合は上に閉じる・T33-L3)。しかし**どこまで降りれば十分かの上界は原理的に存在しない**(B4-B に有限証明書は無い・GS §3.2)。

---

## 2. なぜ「一様吸収定理」が出せないか — 崩壊定理の適用範囲を精確に

**T33-T1(再掲・固定入力 1–4 の下)**: 次は同値 —
(1) B4-B (2) STEP(任意の isolated $H$ と次の isolated refinement $L'$ で $I_H=X\Rightarrow I_{L'}=X$) (3) SINGLE(x)(cofinal family 上) (4) $\forall K$ isolated $\le M$: $I_K=X$ (5) DEEP(x)。

**Sol の問いへの適用(敵対的に確認した)**:
- Sol の問いは条件付き(「この witness + package から」)なので、崩壊定理をそのまま貼るのは形式的には不十分。**しかし**: package(FV-5 / surgery+torsor / one-outside)はすべて**すでに固定入力 1–4 の中身**であり、witness は「ある一つの $L$ で $I_L=X$」を足すだけ。
- 一方 (2) の STEP は「$I_H=X\Rightarrow I_{L'}=X$」という**含意の全称**であって、前件 $I_H=X$ を一つ手に入れたことは (2) の証明に寄与しない。
- 従って **witness + package $\vdash$ 一様吸収** が成り立つなら、その導出は $I_L=X$ を使わない形に書き直せ、(2) をそのまま与える ⟹ B4-B。
⟹ **一様吸収定理は package から出ない。出たとすれば B4-B が出たことになる。**(これは「難しい」ではなく「論理的にその主張である」。)

**帰結(Sol の言う『飛ばさない』の数学的裏付け)**: 一層の正から cofinal 全段へ飛ばしてはならない理由は用心ではなく、**飛ばした瞬間に主張が B4-B に化ける**からである。

---

## 3. 現状の最善 = 型付き有限判定の族(一様「手続き」)

$L$ の直下の段 $L'\le L$、$N':=L/L'$ とする。**型ごとに道具・前件・有限判定が違う。**

| $N'$ の型 | 使える道具 | **前件(未証明を含む)** | 有限判定 |
|---|---|---|---|
| **elementary abelian $\mathbf F_3$** | T-34 jump($\Phi_3(L)$ が層の厳密な最小共通下界)+ UU v2(閉形式補正 $\gamma=\Sigma\beta$) | ★**actual typing**(actual chief 複体が unit-twist linking 複体 — T-30 §4・**本丸・未証明**)/ UU-0(GO)/ FC-13′($\mathbf D_3,\mathbf D_4$ 全係数 mod $K$ untwisted)/ FC-14 / FC-15 | FC-13′→14→15 の順(v2 §R-4 の述語列) |
| **位数が 3 と互いに素**(elem. ab. $p\ne3$、および $3\nmid\lvert S\rvert$ の $S^t$ = Suzuki 型) | **SYL3(T33-T2)**:$3\nmid[\mathrm{ML}(L):\mathrm{im}R_{L',L}]\Rightarrow I_{L'}=X$ | ⚠**index 条件は無料ではない**。GS-T2 は (CH-p) 経由で index を $3'$ と主張したが、**crossed hom の zero-fibre index は係数群の位数を割らない**(chp_proof E-2 の反例 $C_3\curvearrowright C_7$)⟹ **撤回済**。従って index 条件は**その都度測る**しかない | $v_3(\lvert\mathrm{ML}(L')\rvert)-v_3(\lvert\ker R_{L',L}\rvert)\ \ge\ v_3(\lvert\mathrm{ML}(L)\rvert)$ の**位数計算のみ** |
| **非可換 $S^t$**(157dp の $A_5^4$ と同型の状況) | **NA-5**:$\mathrm{ML}(L)$ のある Sylow 3-部分群の**生成系(典型 2〜3 元)**を個別に持ち上げれば $I_{L'}=X$。各元は outside roof を持たなくてよい | **SURJ-NA**(非可換 chief では $\Phi(\cdot)$ 冪零性から $N'\not\le\Phi_{\rm Frat}$ ⟹ 可換段で使えた「$V\subseteq\Phi\Rightarrow$ onto 自動」が**使えない** ⟹ onto gate が真の追加条件)/ **D1**(座標部分群の像・実際は **FC-22** で足りる) | **OBS-NA**(T-38 §7):3 残差 $(\rho_1,\rho_2,\rho_3)$ が $\Lambda(L')$ 内で消えるか + side gate。NA-5 により**標的は 2〜3 元**に縮む |

> **⟹ 回答の核**: **一様「定理」は存在し得ず、現状の最善は「一様手続き」= 上の 3 行の型付き有限判定の族**である。157dp はその第 3 行を**一つの段で実行して正が出た**という位置づけであり、それ以上でもそれ以下でもない。

---

## 4. 最初の欠けた射の特定(Sol の設問の核)

**欠けているのは下降射 $L\to L'$ そのものである。** より正確に:

```
157dp witness at L
  ──(命題 T48-1・無料)──▶  I_H = X   (∀ isolated H ⊇ L)      【閉】
  ──★ MISSING ARROW ★──▶  I_L' = X   (isolated L' ⊊ L)
  ──(単調 + cofinal)───▶  ∀K isolated ≤ M                    【MISSING の全称化】
  ──(Cor 3.13 / FV-5)──▶  B4-B                                 【閉】
```

**「NA-EX か actual typing か」への回答**: Sol の文脈(q3 → $A_5^4$ の直上)では **どちらでもない**。
- **NA-EX**(非可換捻れ完全性)は**一様**主張(全 $\beta$ 用)であり、**NA-5 はそれを迂回する** — NA-5 は段ごとに 2〜3 個の literal lift を要求するだけで、普遍的完全性を要らない。⟹ 段ごと手続きの文脈では NA-EX は**先に効かない**。
- **actual typing** は elementary-$\mathbf F_3$ 層の道具(UU)の前件であり、$A_5^4$ 層では**そもそも使わない**(UU は pro-3 現象で非可換層に非適用・v1 §5)。⟹ 直上でも先に効かない。
- **先に効くのは**: $L$ の直下の段の**型の同定**(FC-26)と、非可換型なら **SURJ-NA**(FC-27)+ **FC-22**。⟹ **最初の欠けた射は「型を同定して対応する有限判定を走らせる」という手続きの第一歩**であり、既存命題では埋まらない。

**最小の追加仮説(明示形)**:
> **(H-STEP$(L,L')$)** $\exists g\in\mathrm{ML}(L)$、$\exists\lambda\in\Lambda(L')$ で side gate $\Sigma(\lambda)$ を満たし $\mathcal R_g(\lambda)=(1,1,1)$。
> ($=\ $OBS-NA$(L,L')$ の否定。NA-5 により $g$ は「Sylow 3 生成系の元」に取ってよく、outside 性は不要。)
**これが唯一の追加仮説**であり、型ごとの十分条件(SYL3 の index 条件 / UU の FC-13′ 系 / NA-5)はすべて (H-STEP) を導くための道具である。

---

## 5. 塔の選択の自由 — どこまで正当か

**(正当) 逆極限は cofinal 部分族で計算してよい** ✓(固定入力 4・Cor 3.13・FV-5)。従って**塔は自由に選べる**。
**(正当・新規) 段は chief 段でなくてよい。** NA-1(残差の 3 公式)・NA-2($W\hookrightarrow N^5$ 単射)・NA-5・OBS-NA は、**$K\le H$ が $B_4$-normal 開であること以外に何も使っていない**(chief 性・既約性・可換性は一度も登場しない)。
*確認*: NA-2 は (2.4) だけ、NA-1 は $\varphi_j$ が準同型で $N\trianglelefteq PB_4/K$ であることだけ、NA-5 は $J$ が部分群であることと Sylow/Lagrange だけ。∎
⟹ **「大きな jump」を 1 段として扱ってよい**(T-34 の $\Phi_3$ jump と同じ哲学を非可換層へ拡張)。複数の chief 因子を 1 回の有限判定でまとめて越えられる。
**(不当) 非可換 chief 因子の回避**は塔の選び方では**できない**。T33-L7:任意の downward-cofinal family は $M/C$ が非可解な $C$ を含む(Cor 3.5 で isolated 化しても $M/C\twoheadrightarrow$ 非可解 は保たれる)⟹ どんな塔でも非可換合成因子を通る。
**(司令塔の確認事項への回答) GS-T1 と「選んだ塔」の関係**: GS-T1(全有限単純群が chief 型として現れる)は**poset についての主張**であり、**選んだ塔の連続段を縛らない** ✓ — 司令塔の読みは正しい。縛るのは T33-L7 の方(非可解商への到達は不可避)。⟹ **型を「制御」はできる(順序・まとめ方)が「回避」はできない。**

---

## 6. 新規の有限検査

| 番号 | 検査 | 効果 |
|---|---|---|
| **FC-26** | 157dp の $L$ の直下に登録する次段 $L'$ の型:$N'=L/L'$ の $S$・$t$・$Q\to S_t$・coupling、および $3\mid\lvert N'\rvert$ か。**FC-8\* の 1 段下版** | §3 の表のどの行に入るかが決まる。**手続きの第一歩** |
| **FC-27** | **SURJ-NA**:$N'\subseteq\Phi_{\rm Frat}(PB_4/L')$ か(非可換なら偽と予想)。偽なら onto gate を OBS-NA の探索に**明示制約として組み込む**コストを見積もる | 非可換段で唯一「無料でない」side gate。157dp で実際にどれだけ効いたかの事後測定にもなる |
| **FC-28** | 層に $\iota$ 以外の **$\lvert Z\rvert$ と互いに素な対称性群** $P$ があるか($Z=\ker R_{L',L}$)。あれば Glauberman(§7)で $F^P$ への縮約が効く | 探索空間の縮約(non-emptiness は出ない) |

(FC-22 = ある $j$ で $p_j(W_j)=N$、FC-13′/14/15 は既登録。)

---

## 7. 文献配達の消化 — Glauberman coprime fixed-point(司令塔 C)

**受領し、SR-1 を一般化する。**
$F:=F_{L'}(x)$ が非空なら、$Z=\ker R_{L',M}$ が**単純推移的**に作用する(SR-0)✓。従って Glauberman の補題(推移作用 + coprime 位数の両立作用 ⟹ 不動点あり)が適用でき:
> **系 SR-1′.** $P$ を $\lvert Z\rvert$ と互いに素な位数の群で $F$ に両立的に作用するものとすると
> $$F\ne\varnothing\ \Longrightarrow\ F^{P}\ne\varnothing .$$
> ⟹ **探索は $P$-不変な補正だけに制限してよい**($\iota$ = 位数 2 の特別な場合)。$p$-層では $\lvert Z\rvert$ は $p$ 冪なので**任意の $p'$-群**が使える ⟹ SR-1 より真に広い。
**限界(明記・司令塔の注意と一致)**: **非空性そのものは出ない**($F\ne\varnothing$ が前提)。⟹ A 側の武器にはならない。Asai–Yoshida 系(crossed hom 数え上げの coprime 割り切れ)が実在すれば SR-0 と組んで**空性強制**の可能性はあるが、**未確認文献なので本書では使わない**。

---

## 8. 自己検証(敵対的)

- **T48-1 で $L$ の isolated 性を使っていないか** ✓ 使っていない(survive 写像は代表対を読むだけ)。使うのは $H$ 側のみ。
- **T33-T1 の適用は正当か** ✓ §2 で条件付き主張への適用を明示的に検証した(前件を使わない形に書き直せることを示した)。
- **SYL3 を「$3'$ 層は無料」と書いていないか** ✓ §3 の表で **index 条件は無料でないこと**と GS-T2 撤回を明記した(chp_proof E-2)。
- **NA-5 が非可換層で使えるという主張の前件** ✓ $J$ が部分群($L,L'$ ともに isolated で Prop 3.7)・$X^2=\mathrm{Syl}_3(X)$・$243\nmid324$ のみ。$N'$ の構造に依存しない。
- **「chief 段でなくてよい」の検証** ✓ §5 で 3 命題の使用前件を逐一確認した。
- **禁止短路** ✓ centerless/Schreier・$K(5)$ 単連結性・strict deletion-kernel・ambient exponent-3 quotient による非可換段の検出・$A$ 正規性 — いずれも未使用($A$ は T-37 どおり非正規)。
- **Sol の禁止「一層から cofinal 全段へ飛ばす」** ✓ §2 でそれが論理的に B4-B と同値であることを示した上で、§3 は段ごとの手続きに限定している。

---

## 9. 申告

- 全結果 paper candidate。機械計算ゼロ。**cross-checked ではなく verified でもない。**
- 157dp の CV-9 判読(falsifier 並行中)は**未了**であり、本書は「witness が literal に成立する」ことを**前提として**受け取っている。判読が覆れば §1 が消える。
- **UNKNOWN**: (H-STEP) の真偽、FC-26/27/28、actual typing、SURJ-NA、D1/FC-22。
- **一様吸収定理は出ていない。B4-B は宣言していない。**
