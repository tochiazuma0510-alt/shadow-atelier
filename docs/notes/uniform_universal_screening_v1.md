# 「一様空間」発案の強い読み — 普遍補正の判定 短報

**状態札: 数学者判定・司令塔検分前・Sol 未監査**
判定: Claude 数学者 / 2026-08-19 / 発案 = 研究者本人 / 委嘱 = 司令塔
格: paper candidate。機械計算ゼロ。**cross-checked ではなく verified でもない。**
非接触: 封印 3 量・$u$ の値・$c$ の値・sealed $K^{(5)}$。$u=2m+1$ は形式変数。
NAME-COLLIDE: $\Lambda$ は完備群環(T-36 の相対 core tower $\Lambda_j$ とは別物 — 本書では後者を使わない)。$I$ は augmentation ideal(Frattini ではない)。

---

## 0. 冒頭申告と一行裁定

### 0.1 T33-L10 抵触自己申告

T33-L10 は「**離散**の単一 literal pair $(m,f)\in\mathbf Z\times F_2$ が cofinal 族の全段で shadow なら $2m+1=\pm1$」。証明は friendly gate $\gcd(2m+1,N_{\rm ord})=1$ と「$m$ が有理整数」であることに全面的に依存する。
本書が扱う「普遍補正」は **$\Lambda=\mathbf F_3[[\cdot]]$ の元 / $\widehat{F_2}$ の profinite 語**であって有理整数対ではない。$2\hat m+1\in\widehat{\mathbf Z}^\times$ は普通に可能なので **L10 は射程外**。⟹ **蘇らせない**(§2 で境界線を厳密に引く)。

### 0.2 一行裁定

**(a) 対象は well-defined。ただし「普遍」の射程を層内(S1)と塔全体(S2)に分けねばならない — $\beta$ の普遍性は (S1) では成立し (S2) では成立しない。(b) L10 との境界は「離散 vs profinite」で、抵触なし。(c) 普遍可解 ⟺ 全段可解 は証明できる(両向き)⟹ 論理的短縮ではなく方法論的短縮。(d) ★本命: twisted 化を阻む 3 候補のうち prefix conjugation は「群環の単位を挿入する」だけであり、augmentation で消える。⟹ 係数環が局所($3$-群/pro-3、より一般に捻り単位が $O_3(E)$ に入る)なら Nakayama で untwisted 分裂が持ち上がり、閉形式の普遍補正が Neumann 級数で書ける(定理 UU)。これは T-30 §4 の障害 5 本のうち #1・#2 を除去する。残るのは #3(correction domain)#4 #5、および $H_2\ne0$ 由来の syzygy(これは障害ではなく前件 $\mathbf D_4\beta=0$ として使う)。(e) 非可換層への波及は**ない**(UU は厳密に pro-3 現象)。**

---

## 1. (a) 対象の well-definedness

### 1.1 正しい環

GS-S(GS screening §2.5)より、Fox 複体は各段で自由 $\mathbf F_3[E_j]$-加群のランク $(|R|,|S|,1)$ で一定、$\mathbf D$ は $\mathbf Z[F]$ 上の**一つの固定行列**(Fox Jacobian)の係数替え像。従って普遍環の候補は
$$\Lambda_{\rm univ}:=\mathbf F_3[[\widehat{PB_4}]]=\varprojlim_U\mathbf F_3[PB_4/U],$$
各段は基底変換 $\Lambda_{\rm univ}\to\mathbf F_3[E_j]$。**行列の側は完全に普遍的**(基底変換は行列の函手であり、分裂は基底変換で保たれる ✓)。

### 1.2 $\beta$(残差)の普遍性 — ここで射程が割れる

$\beta_j$ は段 $j$ の literal pair $p_j$ の残差の Fox 微分像。CHP-2 の函手性は $\varrho(p_2\ast p_1)=\tilde T_{p_2}(\varrho(p_1))$ を与えるが、**段ごとに $p_j$ が異なる**(T33-L10 が定数 literal pair を禁じている)ので、$\beta_j$ たちが一つの $\beta\in\Lambda_{\rm univ}^{|S|}$ の特殊化になる保証はない。

⟹ **射程を分ける**:
- **(S1) 層内普遍**: 固定段 $H$ とその直下の層($\Phi_3(H)$、T-34)。pair は**一つ**なので $\beta$ は定義され、係数加群 $V$ の側を動かす。T-36 §2.4 (CN1)–(CN4) の枠。**ここでは $\beta$ の普遍性は成立する。**
- **(S2) 塔全体普遍**: 段をまたぐ。$\beta$ の普遍性は**成立しない**(pair が変わる)。塔全体の「普遍解」は §3 の同値により $\widehat{GT}$ の元そのもの、すなわち B4-B に等しい。

> **⟹ 発案の実りは (S1) にある。** (S2) は形を変えた B4-B であり、そこに近道はない。以下 §4 の本命はすべて (S1) の話である。

---

## 2. (b) T33-L10 との境界線

| 対象 | 住む場所 | L10 |
|---|---|---|
| 定数 witness(A-4 強形/A-5) | $(m,f)\in\mathbf Z\times F_2$(**離散**) | **死んでいる**(T33-L10) |
| 普遍補正 $\Sigma$、普遍解 $\gamma$ | $\Lambda$-加群の元/行列(**profinite 係数**) | **射程外**(有理整数性を使わない) |
| 塔全体の普遍解の逆極限 | $\widehat{GT}$ の元($\hat m\in\widehat{\mathbf Z}$, $\hat f\in\widehat{F_2}$) | **射程外**。$2\hat m+1\in\widehat{\mathbf Z}^\times$ は可 |

**境界の一行**: L10 は「$\widehat{\mathbf Z}^\times\cap\mathbf Z=\{\pm1\}$」という**整数論的剛性**の帰結であり、完備化した対象には一切効かない。従って普遍補正の路線は L10 を蘇らせない。
**同時に自由昼食も無い**: (S2) の普遍解を作ることは $\widehat{GT}$ の outside 元を作ることと同じ(§3)。

---

## 3. (c) compactness 同値の明示

**定理 UNIV-EQ.** 固定した段 $H$ と層(あるいは cofinal 族 $\{C_j\}$)について、各段の解集合を
$$\mathrm{Sol}_j:=\{\gamma\in\mathbf F_3[E_j]^{s_3}\ :\ \mathbf D_3^{(j)}\gamma=\beta_j\}$$
とし、遷移写像を基底変換 $\mathbf F_3[E_{j+1}]\to\mathbf F_3[E_j]$ とする。$\beta_{j+1}\mapsto\beta_j$(整合残差)を仮定すると:
1. 各 $\mathrm{Sol}_j$ は $\mathbf F_3$ 上有限次元アフィン集合(**有限**)。
2. 基底変換は $\mathrm{Sol}_{j+1}\to\mathrm{Sol}_j$ を誘導(行列の函手性 ✓)。
3. 従って $\varprojlim_j\mathrm{Sol}_j\ne\varnothing\iff\forall j:\mathrm{Sol}_j\ne\varnothing$(非空有限集合の逆極限は非空)。
4. $\varprojlim_j\mathrm{Sol}_j$ の元がまさに $\Lambda$ 上の**普遍解**である。
∎(3 は標準の compactness;固定入力 4 と同じ道具。)

**同じ主張が「解」ではなく「分裂 $\Sigma$」についても成り立つ**(分裂の集合も各段有限、遷移は基底変換 ✓)。

> **正確な言明(司令塔の要求)**:
> **普遍可解 $\iff$ 全段可解 は定理である。従って普遍系への移行は「論理的短縮」ではない — 証明義務は 1 グラムも減らない。** これは GS screening §6.1 の塔不変性と同じ構図である。
> **しかし方法論的短縮ではある**: 逆極限は非構成的だが、**閉形式の $\Sigma$ が書ければ**、無限個の段の検証が「一つの式 + 基底変換」に置き換わる。先例は T-30 §2(untwisted 分裂の明示逆 $ae_{12}+be_{14}+ce_{34}\mapsto ae_{12}-be_{13}+ce_{23}$、一つの整数行列が全係数環で通用)。**§4 が示すのは、その twisted 版が実際に書けるということである。**

---

## 4. (d) 偵察 — 何が閉形式を壊し得るか(本命)

### 4.1 twisted $\mathbf D_3$ の正確な形

T-38 補題 NA-1 の pentagon 補正項
$$P(w)Q(w)^{-1}=\varphi_{234}(w)^{a_2a_3}\cdot\varphi_{1,23,4}(w)^{a_3}\cdot\varphi_{123}(w)\cdot\bigl[\varphi_{1,2,34}(w)^{a_5}\cdot\varphi_{12,3,4}(w)\bigr]^{-1}$$
を可換係数へ線形化すると
$$\mathbf D_3=[a_2a_3]\,\Phi_{234}+[a_3]\,\Phi_{1,23,4}+\Phi_{123}-[a_5]\,\Phi_{1,2,34}-\Phi_{12,3,4}$$
($\Phi_j$ = T-30 §2 の**整数** coface 行列、$[g]$ = 群環の元による乗法)。

**核心の観察**: $[g]$ は群環の**単位**であり、augmentation $\varepsilon:\Lambda\to\mathbf F_3$、$[g]\mapsto1$ の下で
$$\boxed{\ \mathbf D_3\equiv D_3^{\rm untw}=\textstyle\sum_i(-1)^i d^i\pmod{I}\ }$$
(T-38 §3.3 で検算済みの順序対応と一致 ✓)。**すなわち prefix conjugation は「untwisted 行列の単位変形」に過ぎず、augmentation で消える。** 同じことが「五 coface の transport が同一でない」(T-30 §4 障害 #1)にも当てはまる — 相違が群元の共役である限り、それは単位の挿入である。

### 4.2 定理 UU(閉形式の普遍補正)

**定理 UU.** $\Lambda$ を、Jacobson 根基 $J$ が augmentation ideal に一致する $\mathbf F_3$-代数とする(下の条件 (L) 参照)。自由 $\Lambda$-加群の複体
$$\Lambda^{s_3}\xrightarrow{\ \mathbf D_3\ }\Lambda^{s_4}\xrightarrow{\ \mathbf D_4\ }\Lambda^{s_5},\qquad \mathbf D_4\mathbf D_3=0,$$
が $\mathbf D_i\equiv D_i^{\rm untw}\pmod J$ を満たすとする。T-30 §2/157cz により $D_3^{\rm untw}$ は**整数の左逆** $\sigma$($\sigma D_3=\mathrm{id}$)を持ち、$\ker D_4^{\rm untw}=\mathrm{im}\,D_3^{\rm untw}$。このとき
1. $\sigma\mathbf D_3\equiv\mathrm{id}\pmod J$ ⟹ **$\sigma\mathbf D_3$ は $\Lambda$ 上可逆**(根基を法として可逆な行列は可逆)。
2. $\Sigma:=(\sigma\mathbf D_3)^{-1}\sigma$ は $\Sigma\mathbf D_3=\mathrm{id}$ を満たす ⟹ $\mathbf D_3$ は**分裂単射**、$\Lambda^{s_4}=\mathrm{im}\,\mathbf D_3\oplus Q$、$Q$ 自由。
3. $\mathbf D_4|_Q$ も $J$ を法として単射(体 $\mathbf F_3$ 上では分裂単射)なので左逆が持ち上がり、$\mathbf D_4|_Q$ は分裂単射。$\mathbf D_4\mathbf D_3=0$ と合わせて
$$\boxed{\ \ker\mathbf D_4=\mathrm{im}\,\mathbf D_3\ }$$
4. 従って任意の $\beta$ with $\mathbf D_4\beta=0$ に対し
$$\boxed{\ \gamma:=\Sigma\beta=(\sigma\mathbf D_3)^{-1}\sigma\beta,\qquad (\sigma\mathbf D_3)^{-1}=\sum_{k\ge0}\bigl(1-\sigma\mathbf D_3\bigr)^{k}\ }$$
が $\mathbf D_3\gamma=\beta$ の**閉形式解**。級数は $J$-進に収束($J$ 冪零 or 位相的冪零)。∎

**条件 (L)(局所性の正確な射程).**
- $E$ が有限 **3-群** ⟹ $\mathbf F_3[E]$ は局所、$J=I$ ✓。$\Gamma$ pro-3 なら $\mathbf F_3[[\Gamma]]$ も ✓。
- より一般に $E$ が正規 Sylow 3-部分群 $P$ を持ち $E/P$ が $3'$-群なら $J(\mathbf F_3[E])=\ker(\mathbf F_3[E]\to\mathbf F_3[E/P])$。このとき $\mathbf D_i\equiv D_i\pmod J$ となる条件は
$$\boxed{\ \text{捻り単位 } a_2a_3,\ a_3,\ a_5\ \text{が } O_3(E)\ \text{に入ること}\ }$$
(untwisted 行列は整数係数なので $\mathbf F_3[E/P]$ へそのまま降り、T-30 の分裂は基底変換で保たれる ✓)。
- **campaign への当てはめ**: $P_4=PB_4/N_4(3)$ は指数 3 ⟹ 有限 3-群 ✓ ⟹ **ambient exponent-3 層では条件 (L) は自動**。一方 $E_4=PB_4/K_*$($K_*=M\cap N_4(3)$)は $|PB_4:M|$ が 4 を含むので 3-群でない ⟹ **捻り単位の $O_3$ 所属を実測する必要**(新 **FC-13**)。

### 4.3 3 つの阻害候補の判別(司令塔の名指し要求への回答)

| 候補 | 普遍式を殺すか | 理由 |
|---|---|---|
| **prefix conjugation**(T-30 §4 #2) | **殺さない**(条件 (L) の下で) | 単位の挿入にすぎず augmentation で消える。定理 UU が吸収 |
| **五 coface transport の相違**(#1) | **殺さない**(同上・相違が群元共役である限り) | 同じ機構 |
| **extension cocycle / nonsplit**(T-34 注意 c2) | **殺さない** | 語で評価する限り自動処理(T-36 §6.5 で既述)。線形化後は $\Lambda$ 係数に吸収される |
| **$H_2\ne0$(syzygy 実在)**(GS §2.5) | **殺さない — むしろ前件** | syzygy は $\beta$ に $\mathbf D_4\beta=0$ を課す条件であり、定理 UU はまさにその条件下でのみ解を出す。「制約」ではなく「入力の型」 |
| **correction domain の制限**(T-30 §4 #3) | **★殺し得る** | $\Sigma\beta$ が $C_{\rm adm}$(二 hexagon・marking・charming・onto・settlement)に入る保証がない。定理 UU は $\Lambda^{s_3}$ 全体を補正領域とみなしている |
| **actual chief complex の同定**(T-30 §4 #3–#5) | **★殺し得る(前件不成立)** | 定理 UU の前件「$\mathbf D_i\equiv D_i^{\rm untw}\pmod J$」は、actual 複体が linking-number 複体の単位捻れであることを要求する。これは T-30 §4 の未証明同定そのもの |
| **条件 (L) の破れ** | **★殺し得る** | $E$ が 3-群でなく捻り単位が $O_3$ 外なら Nakayama が効かない |

### 4.4 「普遍式が存在するが非構成的」vs「存在しない」の判別法

**判別は有限計算に落ちる**:
1. **条件 (L) を検査**(FC-13)。成立すれば ⟹ 定理 UU により**必ず閉形式で存在**(非構成的な場合は生じない)。$\Sigma$ は Neumann 級数で明示的に書ける。
2. (L) が破れる場合 ⟹ $\Lambda/J$(有限次元**半単純**代数)上で twisted 複体の中央完全性を検査する。半単純なので**純粋な線形代数の有限判定** ✓。
   - $\Lambda/J$ 上で完全 ⟹ Nakayama で $\Lambda$ 上へ持ち上がる(定理 UU の証明がそのまま動く) ⟹ **閉形式で存在**。
   - $\Lambda/J$ 上で非完全 ⟹ **ある段で非可解**(基底変換で不完全性は残る) ⟹ **普遍式は存在しない**、しかも**その非完全性が OBS★ 型の障害証明書そのもの**。
> ⟹ **「非構成的にだけ存在する」という中間状態は起きない。** 判別は 1 段階の半単純線形代数で決着する。これは (d) への直接回答である。

---

## 5. (e) 非可換層への波及 — なし

冪公式 $\varrho(p^{\ast n})=\tilde T_p^{\,n-1}(\varrho(p))$(CHP-2 の系)は**函手性の言い換え**であって普遍解ではない。NA-5 の Sylow-3 生成元持ち上げに「普遍持ち上げ」版を作るには残差方程式が線形でなければならないが、NA-5 が使われる層は $N=S^t$(FC-8\* の実例は $A_5^4$)で**線形化そのものが存在しない**(T-38 §4.2)。定理 UU は $\mathbf F_3$-係数の局所群環に依存する厳密に **pro-3 の現象**である。⟹ **一言: 波及しない。**

---

## 6. 新規の有限検査

| 番号 | 検査 | 由来 |
|---|---|---|
| **FC-13** | 捻り単位 $a_2a_3,\ a_3,\ a_5$($=\varphi_j(f)$ の像)が $O_3(E)$ に入るか。$E$ が 3-群なら自動 | 定理 UU の条件 (L)・§4.2 |
| **FC-14** | $\mathbf D_4\mathbf D_3=0$(twisted 複体条件)の確認 | 定理 UU の前件 |
| **FC-15** | $\Sigma\beta\in C_{\rm adm}$ か(閉形式解が許容補正領域に入るか) | §4.3 の唯一の「殺し得る」項目のうち計算で見えるもの |

**優先度**: FC-13 → FC-14 → FC-15。FC-13 が YES なら 157dl lane の線形系は**解く必要がなくなり、閉形式を代入して検算するだけ**になる(producer の探索が checker の 1 回評価に落ちる)。

---

## 7. novelty grep 領収書(2026-08-19)

| 語彙 | 結果 | 扱い |
|---|---|---|
| Nakayama | 既在(`157da:105`, `157de:122`, `157do:79`)だが用途は**$H_9$ の生成ランク**。**twisted 複体の分裂持ち上げへの使用は該当なし** | 定理 UU は新規 |
| completed group ring / $\mathbf F_3[[\cdot]]$ / Iwasawa algebra | 既在は自書 GS screening §2.4 のみ(**否定的**文脈:Λ-構造は無い) | 本書は Noether 性でなく**局所性**だけを使うので §2.4 と両立 ✓ |
| universal correction / 普遍補正 | 既在(`152_b4_global_lift_literature_v1:116` — 普遍補正に必要な 4 条件を列挙、非可換 $S^t$ は非線形と明記) | **本書は (i)(iii) に該当する部分を pro-3 で解決**、(ii)(iv) は未解決として残す(§4.3 の「殺し得る」欄と一致) |
| 閉形式 | 既在は別文脈(数論側の閉形式) | 衝突なし |
| Typed contraction lemma | 既在(`152_b4_chief_obstruction_v2` §2:「B4-同変な contracting homotopy が存在すれば (C) は可解。ただし原典はこの複体も homotopy も定義していない」) | **定理 UU はその homotopy を pro-3 で明示的に構成する**もの — 既在の条件付き主張の前件を一つ埋める |
| Magnus / Fox 逆元 | 既在(T-34, T-38 §6.3–6.4, 157dl) | 引用 |

---

## 8. 申告

- 全結果 paper candidate。機械計算ゼロ。**cross-checked ではなく verified でもない。**
- 手計算で検証したのは:§4.1 の augmentation 還元、定理 UU の 4 ステップ、条件 (L) の 2 形、§3 の compactness 同値、§4.4 の判別法。
- **未証明の前件(定理 UU が乗っているもの)**: (i) actual chief 複体が linking-number 複体の**単位捻れ**であること(T-30 §4 の未証明同定)、(ii) $\mathbf D_4\mathbf D_3=0$(FC-14)、(iii) 条件 (L)(FC-13)、(iv) $\Sigma\beta\in C_{\rm adm}$(FC-15)。**(i) が本丸であり、定理 UU はそれを埋めない。**
- **UNKNOWN**: (S2)(塔全体普遍)は B4-B と同値ゆえ未決。FC-13/14/15。
- T33-L10 は蘇っていない(§0.1・§2)。禁止短路は未使用。
- **B4-B は宣言していない。**

---

## Erratum ポインタ(2026-08-19・本文凍結・追記のみ)

**本稿は `docs/notes/uniform_universal_screening_v2.md` に置き換えられた。** Sol T-43 監査(`ops/express/20260819_sol_fable_t43_audit.md`)6 点を反映した修理稿である。v1 の以下は **撤回・訂正済み**:

1. **§4.4 末尾「FC-13 が YES なら 157dl lane の線形系は解く必要がなくなる」— 撤回。** 157dl が解くのは $PB_4$ 表示の **left-Fox 複体** $\mathbf F_3[E_4]^{11}\to\mathbf F_3[E_4]^{6}$ であり、UU の **arity coface 複体** $\Lambda^3\to\Lambda^6\to\Lambda^{10}$ とは**別対象**(v2 §1)。**157dl v1/v2 は停止・変更しない。**
2. **§4.2 の FC-13 は under-specified。** $\mathbf D_4$ の全 transport/prefix 係数にも同じ条件が要る ⟹ **FC-13′** へ拡張、測定述語は「捻り単位 $\in O_3(E)$」から「**mod $K=I(O_3(E))kE$ で untwisted**」へ確定(v2 §3)。
3. **§4.2 定理 UU の「$Q$ 自由」→ 有限生成射影**。証明 step 3 の「体 $\mathbf F_3$ 上では単射が分裂」も撤回($\mathbf Z$-分裂を読む形へ)。**条件 (L)(局所性)は不要化**され、$\mathfrak a\subseteq\operatorname{Jac}(kE)$ のみで足りる。$J=\ker(kE\to k[E/O_3])$ の**等号は書かない**(v2 §2)。
4. **§4.4 の判別法後半「非完全 ⟹ ある段で非可解 ⟹ OBS★ 証明書」— 訂正。** それは「全 $\beta$ 用 universal splitter の不存在」までで、**actual $\beta$ の非零 class には別途 pairing certificate が必要**(v2 §5)。
5. **§4.2「$P_4=PB_4/N_4(3)$ は指数 3」は exponent 3(冪指数)の意**。以後 exponent / index を訳し分ける(v2 §6)。

**維持されるもの**: §1(環の同定)・§2(T33-L10 との境界)・§3(compactness 同値)・§5(非可換層へ波及なし)。
