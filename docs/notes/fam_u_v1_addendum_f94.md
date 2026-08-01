# 追補(便 94 F94-3 修文波)— FAM-U の $\alpha$ 整数持上げ・C1′ の分割・前件表更新

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01
- 位置づけ: `docs/notes/fam_u_v1.md` への **第 1 追補**。**本体は書き換えない**(erratum 方式)。抵触箇所は**本追補が優先**する。
- 委嘱: 司令塔(便 94 修文波・裁定 319)「**FAM-U の $\alpha$ 整数持上げ**(F94-3): exact 符号に要る $\alpha\in\mathbf Z$ の持上げの構成(または「類・位数のみの族定理」として射程を確定する選択肢の比較)。C1′ を類/位数 gate から外す Sol 裁定の反映と、M2 が残る旨の前件表更新」
- 入力正本: `sol/sol_reply_94_math21.md` **F94-3.1 / W94-3.1 / F94-3.2 / W94-3.2**、`docs/notes/fam_u_v1.md`、`docs/notes/u7_fire_log_v1_addendum_grade.md` §4.2.6.3(C-β datum の一般形)
- 検算: 本追補 §1.3(手計算・値は $g(i)=-i$ と $(-i)^{2n}$ の初等計算のみ)

---

## 0. 判定(先に 5 行)

| # | 問い | 判定 |
|---|---|---|
| **①** | W94-3.1(exact 式の $\alpha$ は型不正) | ★ **全面受諾**。$\alpha\in(\mathbf Z/n)^\times$ に対し $(-1)^\alpha$ は well-defined でない |
| **②** | 持上げ $\widetilde\alpha\in\mathbf Z$ を**構成**できるか | ★ **できる。しかも新しい選択ではない** — $\widetilde\alpha$ は**模型の定義式に既に書かれている整数指数**である(§1.1)。追加の datum を導入する必要はなく、**定理の書き方**を直せばよい |
| **③** | 持上げの曖昧さ $\widetilde\alpha\mapsto\widetilde\alpha+n$ は何に対応するか | ★ **補題 LIFT(新規)**: それは **Kummer 生成元(= 一様化元)の取り替え $y\mapsto g\,y$ と同一の操作**であり、$u\mapsto u\cdot g(i)^{-2n}=-u$。⟹ **式 $u=4(-1)^{\widetilde\alpha}$ は内部整合**(§1.3) |
| **④** | 「類・位数のみの族定理」に射程を切るべきか | **切らなくてよい。二層で書くのが正しい**(§2)。exact 層 = 模型・一様化元・$\widetilde\alpha$ 相対、不変層 = それらに非依存 |
| **⑤** | C1′・M2・$n=5$ | C1′ を **C1′-sel / C1′-adm** に分割(§3)。**C1′-sel は類・位数 gate から外れる**。**M2 は残る**(最大の前件)。**M4 は M2 の系へ降格**(§3.3)。$n=5$ は定理領域から**明示的に除外**(§4) |

> **一行で**: 持上げは「作る」ものではなく「**書き忘れていた**」ものである。$y^n=h$ の $h$ に立っている指数はもともと整数であり、それを $(\mathbf Z/n)^\times$ の元と呼んだ瞬間に型が壊れた。

---

## 1. ★ $\alpha$ の整数持上げ — 構成と補題 LIFT

### 1.1 持上げは模型 datum の一部である(構成)

FAM-U §2.1 の標準模型は

$$h_{\widetilde\alpha}(k)=\frac{k-i}{k+i}\Bigl(\frac{k+1}{k-1}\Bigr)^{\widetilde\alpha}=\frac{k-i}{k+i}\,g^{\widetilde\alpha},\qquad g:=\frac{k+1}{k-1},\qquad \widetilde W_0:\ y^{\,n}=h_{\widetilde\alpha}(k)$$

である。ここで $\widetilde\alpha$ は**有理関数の指数**であるから、はじめから**整数**である($(r_0,r_\infty)=(1,-\widetilde\alpha)$ — 追補 grade §4.2.6.3 の C-β datum の言葉で言えば $r_\infty\in\mathbf Z$)。

> ### ⟹ 構成
> $$\boxed{\ \widetilde\alpha\ :=\ \text{模型の定義式に立っている整数指数}\ =\ -r_\infty\ \in\mathbf Z\ }$$
> **持上げは新しい選択ではない。** 誤りは、定理の言明で $\alpha\in(\mathbf Z/n)^\times$ と量化しながら、証明の中で $(-i)^{\alpha}$ という**整数指数の冪**を計算していたことである(§2.2 の $h_1$ の行)。$(\mathbf Z/n)^\times$ が現れるのは「この模型が**どの窓**に対応するか」を問うときだけで、模型そのものは $\widetilde\alpha\in\mathbf Z$ で決まっている。

### 1.2 窓ラベルへの落とし方(層の分離)

$$\widetilde\alpha\in\mathbf Z\ \xrightarrow{\ \bmod n\ }\ \alpha\in(\mathbf Z/n)^\times\ \xrightarrow{\ /\{\pm1\}\ }\ [\alpha]\in(\mathbf Z/n)^\times/\{\pm1\}=\text{窓}$$

- **模型**は $\widetilde\alpha\in\mathbf Z$ で決まる。
- **窓**は $[\alpha]$ で決まる。
- **同じ窓を与える整数**は $\widetilde\alpha'\in\{\pm\widetilde\alpha+jn:j\in\mathbf Z\}$。

### 1.3 ★ 補題 LIFT — 持上げの曖昧さ = 一様化元の取り替え

> ### 補題 LIFT【証明あり・本追補で新規】
> $n$ を奇数とする。$(k,y)\mapsto(k,\,y\,g(k))$ は模型の同型
> $$\Psi:\ \widetilde W_0(\widetilde\alpha)\ \xrightarrow{\ \sim\ }\ \widetilde W_0(\widetilde\alpha+n)$$
> を与え、$\iota$ と可換で $W_0$ に降りる。cusp($k=i$ 上の唯一点)における一様化元は $y\mapsto g(i)\,y\,(1+O(y^{\,n}))$、$g(i)=-i$ と変わり、したがって
> $$u_{n,\widetilde\alpha+n}\;=\;u_{n,\widetilde\alpha}\cdot g(i)^{-2n}\;=\;u_{n,\widetilde\alpha}\cdot(-i)^{-2n}\;=\;-\,u_{n,\widetilde\alpha}.$$
> **⟹ 公式 $u=4(-1)^{\widetilde\alpha}$ の $\widetilde\alpha$ 依存性は、ちょうど Kummer 生成元(一様化元)の依存性である。**
>
> **証明.**
> **(a) 同型**: $h_{\widetilde\alpha+n}=h_{\widetilde\alpha}\cdot g^{\,n}$ ゆえ $(yg)^n=y^ng^n=h_{\widetilde\alpha}g^n=h_{\widetilde\alpha+n}$。$k$ を動かさないので $k$-直線上の被覆の同型である。
> **(b) $\iota$ との可換性**: $\Psi(\iota(k,y))=\Psi(-k,1/y)=(-k,\ g(-k)/y)$、$\iota(\Psi(k,y))=\iota(k,yg(k))=(-k,\ 1/(yg(k)))$。両者が等しいことは $g^\sigma=g^{-1}$(記録済みの恒等式)と同値。∎(b)
> **(c) $g(i)$**: $(i-1)(i+1)=i^2-1=-2$ より $\dfrac{i+1}{i-1}=\dfrac{(i+1)^2}{-2}=\dfrac{2i}{-2}=-i$。∎(c)
> **(d) 主張**: $t=k-i$ とおくと $g(k)=-i\bigl(1+O(t)\bigr)$、かつ $t=h_1^{-1}y^n(1+O(y))$(§2.2)ゆえ $g=-i(1+O(y^n))$。よって新しい一様化元は $y'=\rho\,y(1+O(y^n))$、$\rho=-i$。$\lambda=u\,y^{2n}(1+\cdots)=u\rho^{-2n}y'^{2n}(1+\cdots)$ より $u'=u\rho^{-2n}$。$\rho^{2n}=((-i)^2)^n=(-1)^n=-1$($n$ 奇)ゆえ $\rho^{-2n}=-1$。∎
>
> **整合(公式側から)**: $4(-1)^{\widetilde\alpha+n}=4(-1)^{\widetilde\alpha}(-1)^n=-4(-1)^{\widetilde\alpha}$($n$ 奇)。**(d) と一致。**

> ### 系 LIFT-a(符号を決める不変量)
> $u_{n,\widetilde\alpha}=4(-1)^{\widetilde\alpha}$ の符号を決めるのは $\widetilde\alpha\bmod 2$ ただ一つである。整数の窓同値類 $\{\pm\widetilde\alpha+jn\}$ は($n$ 奇ゆえ)**両方の parity を含む**。⟹ **符号は窓の不変量ではない。** 一方 $\gcd(2,n)=1$ より $\widetilde\alpha\bmod 2n$ は「窓 + 符号」を同時に決める最小の水準である。
> ### 系 LIFT-b(不変層は無傷)
> $-1=\zeta_{4n}^{2n}\in F_n^{\times2n}$ ゆえ $[4]_{2n}=[-4]_{2n}$。⟹ **類 (2)・位数 (3) は $\widetilde\alpha$ の選択にも一様化元の取り替えにも依存しない**(本体 §2.3 の主張は無傷)。

### 1.4 標準正規化(二つ・水準ごと)

| 水準 | 正規化 | 得られるもの | 注意 |
|---|---|---|---|
| **$\alpha$-水準** | $\widetilde\alpha\in\{1,\dots,n-1\}$(Sol W94-3.1 の提案) | $u$ が $\alpha\in(\mathbf Z/n)^\times$ の**関数**になる | 窓の関数にはならない |
| **窓水準** | $\widetilde\alpha\in\{1,\dots,\tfrac{n-1}2\}$(各 $\pm$ 類の唯一の代表) | $u$ が**窓 $[\alpha]$ の関数**になる | ★ **この関数自体が規約に依存する** — 代表を $\{\tfrac{n+1}2,\dots,n-1\}$ から取れば全符号が反転する(系 LIFT-a) |

**採用**: 工房標準は**窓水準の正規化** $\widetilde\alpha\in\{1,\dots,\frac{n-1}2\}$ とし、cert の `alpha_lift` 欄に $\widetilde\alpha$ の**整数値そのもの**を記録する(`alpha_convention` 欄の $[\alpha]=[1]$ と**別欄**にする)。$n=7$ の登録値: $[\alpha]=[1]\Rightarrow\widetilde\alpha=1\Rightarrow u_7=4(-1)^1=-4$(既存の値と一致・**新しい主張ではない**)。

---

## 2. 定理候補 FAM-U の修文(本体 §1 を置換)

> ### 定理候補 FAM-U【theorem candidate・修文版】
> **奇数 $n\ge3$($n\ne5$・§4)**、**整数 $\widetilde\alpha\in\mathbf Z$ で $\gcd(\widetilde\alpha,n)=1$** とし、$\alpha:=[\widetilde\alpha]\in(\mathbf Z/n)^\times$ とする。指定された $K^{(n)}$ 窓($H=H_{2,\alpha,0}$)の **TOWER/KUM 標準模型 $h_{\widetilde\alpha}$** および**指定 cusp / source-map / 一様化元 $\tau=y$** を取る((C) 群・(M) 群の前件)。このとき:
>
> **(1) 主係数(模型・一様化元・持上げつきの等式)**
> $$\boxed{\ u_{n,\widetilde\alpha}\;=\;4\,(-1)^{\widetilde\alpha}\ }\qquad(\text{模型 }h_{\widetilde\alpha}\text{、一様化元 }y\text{ に相対的})$$
> **(2) 座標不変な Kummer 類**
> $$\boxed{\ [u_{n,\widetilde\alpha}]_{2n}\;=\;[4]_{2n}\;=\;[-4]_{2n}\ \in\ F_n^\times/F_n^{\times2n}\ }\qquad(\widetilde\alpha\text{ にも一様化元にも非依存})$$
> **(3) 位数** $\ \mathrm{ord}\bigl([u_{n,\widetilde\alpha}]_{2n}\bigr)=n$
> **(4) 付値(模型代表元 $4(-1)^{\widetilde\alpha}$ に相対的)**: $F_n=\mathbf Q(\zeta_{4n})$ の各 $\mathfrak p\mid2$ で $w_\mathfrak p=4$、**この代表元の他の全ての素点で $0$**。
> ★ **(4) は「任意の一様化元変更に対する不変量」ではない**(W94-3.1 後段)。不変なのは**類 (2) と位数 (3)** であり、(4) は固定した模型代表元についての言明である。

**変更点(本体 §1 との差分)**:
1. 量化を $\alpha\in(\mathbf Z/n)^\times$ から $\widetilde\alpha\in\mathbf Z$、$\gcd(\widetilde\alpha,n)=1$ へ。
2. (1) に「持上げつき」を明記。
3. (4) に相対性を明記。
4. 領域から $n=5$ を明示除外(§4)。
5. 射程外の明示(本体のまま維持): $d=\gcd(\alpha,n)>1$ の窓・$n$ 偶。**機械的裏付けが 1 本増えた** — $(n;r_0,r_\infty)=(9;1,-3)$ で $\lvert\mathcal M^{\rm mod}\rvert=108\ne4n^2$、$g_\infty$ の巡回型 $(6,6,6)\ne(18)$(追補 grade §4.2.6.7 DUM-4)。

### 2.1 選択肢の比較(委嘱の「または」への回答)

| 案 | 内容 | 得 | 失 | 判定 |
|---|---|---|---|---|
| **A. exact 符号つき族定理**(修文版) | $\widetilde\alpha\in\mathbf Z$ で量化し (1) を残す | 情報量が最大。$n=3$ の外部正例照合(LMFDB)が**そのまま生きる** | 前件に「持上げの規約」が 1 行増える | ★ **採用** |
| **B. 類・位数のみの族定理** | (1) を落として (2)(3) だけにする | 前件が減る | $n=3$ 外部正例の**符号一致**という最強の較正点を捨てることになる。また (1) は既に**正しく証明されている**(型を書き直せば済む) | 不採用 |
| **C. 両方**(層別記帳) | (1) と (2)(3)(4) を**別の格**で記帳 | — | — | ★ **A の内訳として実施**(§2.2) |

### 2.2 層別の格(本体 §4 を置換)

| 主張 | 格 | $\widetilde\alpha$ 依存 |
|---|---|---|
| **(2) 類** | **theorem candidate**(前件 (D)(M)(C1–C5)(W)(B)) | **なし** |
| **(3) 位数 $=n$** | **theorem candidate**。算術部分(本体 §2.4)は初等・独立 | **なし** |
| **(4) 全付値** | **theorem candidate + 模型代表元に相対的** | **なし**(値の表示は依存) |
| **(1) exact 値 $4(-1)^{\widetilde\alpha}$** | **theorem candidate + 模型 / 一様化元 / 持上げ $\widetilde\alpha$ に相対的**。**単系統(経路 A)**。$n=3$ で外部正例照合済 | ★ **あり**(符号 $=(-1)^{\widetilde\alpha}$) |
| **M2** | ★★ **candidate — 最大の穴**(不変) | — |
| **Lean** | **verified ではない** | — |

---

## 3. C1′ の分割と前件表の更新(F94-3.2 の反映)

### 3.1 C1′ の分割(Sol 指定・採択)

| ID | 内容 | 用途 | **類・位数 gate** | **exact 値 gate** |
|---|---|---|---|---|
| **C1′-sel** | $\widetilde\alpha$ / orientation の**選択**(どの持上げ・どの向きを採るか) | exact representative | ★ **外れる**(F94-3.2 の YES) | **要る** |
| **C1′-adm** | 対象が当該**標準模型に属する**こと | M2 / source-map | ★ **外れない** | **要る** |

> **⟹ C1′($n$)未決のままでも、族の算術的結論(類 (2)・位数 (3))は立つ。** これは本体 §7 監査点 C の読みであり、**Sol が YES で同意した**(F94-3.2)。
> **⚠ 同時に**: 「被覆の算術同定そのものが不要になるわけではない」(F94-3.2 の NO)。**M2 は依然として最大の前件**である。

### 3.2 前件表 (C) 群の更新(本体 §3.3 の該当行を置換)

| # | 前件 | 出所 | 格 | 破綻条件 |
|---|---|---|---|---|
| **C5** | ★ **局所一様化元 $\tau=y$**(Kummer 生成元)を固定する。$u$ の**値はこれに相対的**($\tau\mapsto\rho\tau$ で $u\mapsto u\rho^{-2n}$) | 補題 B-5(ii-loc) + D-3 追補 §3.1 | **proof + 表記規律**(不変) | 一様化元を書かずに値を主張すると無意味 |
| **C6**(旧) | 「$[\alpha]=[1]$ を採る根拠は規約であって定理ではない」 | — | — | ★ **本追補で C1′-sel / C1′-adm に分割**(下 2 行が置換) |
| **C6a = C1′-sel** | **持上げ $\widetilde\alpha\in\mathbf Z$ と向き(0/∞ ラベル)の選択**。工房標準 = $\widetilde\alpha\in\{1,\dots,\frac{n-1}2\}$ | 本追補 §1.4 | ★ **規約(UNKNOWN のまま・ただし gate から外れた)** | ★ **(2)(3) には影響しない**。**(1) の符号にのみ影響**(補題 LIFT) |
| **C6b = C1′-adm** | **対象が当該標準模型に属すること**(source-map つき) | — | ★★ **candidate = (M2) と同一内容** | ここが偽なら族公式は別の被覆の $u$ を計算している |
| **C7** | exact equality と Kummer class を分けて記帳する | D-3 追補 §3.2 | **手続き**(不変・**本追補 §2.2 が実施形**) | 混ぜると格の過大表示 |

### 3.3 ★ (M4) の降格 — M2 の系へ(F94-3.2 後段の採択)

**Sol の議論(採録・検算つき)**: M2 が $F_n$ 上の source-map つき同型まで与えるなら、標準模型では

$$h_{\widetilde\alpha}(0)=\frac{-i}{i}\cdot\Bigl(\frac{1}{-1}\Bigr)^{\widetilde\alpha}=(-1)\cdot(-1)^{\widetilde\alpha}=(-1)^{\widetilde\alpha+1},\qquad h_{\widetilde\alpha}(\infty)=1 .$$

$k=0$ と $k=\infty$ はともに $\sigma$-固定点で $\lambda=1$ に写る(すなわち $\lambda^{-1}(1)$ の非分岐 2 点 $R_\pm$ を担う)。$n$ が奇数なので $y^n=\pm1$ の解 $y=\pm1$ は $\mathbf Q$-有理、したがって $R_\pm$ は $F_n$-有理であり、補題 TW-2 の $[\gamma]=\mathrm{disc}\,F[R_1,R_2]=1$ が従う。

| # | 旧 | 新 |
|---|---|---|
| **M4** | 独立前件(candidate):「各 $n$ で $[\gamma]=1$ の枝にいること」 | ★ **(M2) の系へ降格**。独立前件から外す |
| **順序制約** | — | ★ **(M2) より先に (M4) を使うのは循環**。依存グラフ上 $\text{M2}\Rightarrow\text{M4}$ の向きを固定し、逆向きの引用を禁止する |
| **本体 §6 FAM-b** | 「$R_\pm$ の $F_n$-有理性を $n$ 一般で紙にする」 | ★ **不要になった**(M2 が閉じれば自動)。**ただし M2 が閉じない限り $[\gamma]=1$ も未閉鎖**という事実は変わらない — 未閉鎖の**個数が 2 から 1 に減った**のであって、困難が消えたのではない |

> ### ⚠ 注意(過大に読まないために)
> これは「$[\gamma]=1$ が証明された」ではなく「**$[\gamma]=1$ の未閉鎖性が M2 の未閉鎖性に吸収された**」である。本体 §5(3)の「$[\gamma]=1$ が全 $n$ で成り立つ — 主張しない」は**維持**する。**ある $n$ で $[\gamma]\ne1$ が出れば、それは(M2 が偽であることの証拠として)最重要級の陰性である**という読みも維持する。

### 3.4 前件表 (M) 群の更新(本体 §3.2 を置換)

| # | 前件 | 格 | 変更 |
|---|---|---|---|
| **M1** | 標準模型が $F_n$ 上の Belyi 被覆・passport $((2n),2^{n-1}1^2,(2n))$ | proof + 機械($n=7$) | 不変 |
| **M2** | ★★ **この標準模型が $K^{(n)}$ 窓に対応する算術被覆の $F_n$-形式である** | ★★ **candidate(最大の穴)** | **不変 = 残る**(F94-3.2 の NO) |
| **M3** | 同定の手段(第三経路 C-β) | **$n=7$ で実行済・cross-checked**(F94-2.2 / F94-2.3) | ★ **更新**: $n=7$ の三窓同定は閉じた。**全奇数 $n$ の M2 は閉じていない**(F94-3.2 末尾) |
| **M4** | $[\gamma]=1$ の枝 | ★ **(M2) の系**(§3.3) | ★ **独立前件から降格** |

---

## 4. $n=5$ の量化(W94-3.2 の履行)

> ### 定理領域の明示
> $$\boxed{\ \text{FAM-U の定理領域}\ =\ \{\,n\ \text{奇},\ n\ge3,\ \boldsymbol{n\ne5}\,\}\ }$$
> **$n=5$ は【凍結 U7-NO5】により定理領域から明示的に除外する。** 黙って「全奇数 $n$」と書いて評価だけ延期する運用は採らない(W94-3.2 の禁止)。

- **理由**: 「全奇数 $n$」は論理上 $n=5$ を量化する。$K^{(5)}$ を noncontact/sealed として扱う運用と両立させるには、**定理の domain を切る**か「形式的主張には含むが評価は seal release 後」と明記するかの**どちらかを選ばねばならない**。工房は**前者**を採る(実行上の noncontact と定理の量化を一致させる方が、後から事故が起きにくい)。
- **復帰手続き**: seal release 後、$n=5$ を領域に戻すか否かは**司令塔の認可事項**とする(本体 §6 FAM-f の運用を維持)。
- **本追補の遵守**: 本追補は $n=5$ の値・機械計算・評価に**一切触れていない**(fixture 表からも除外・追補 grade §4.2.6.7)。

---

## 5. 未閉鎖(本追補後の状態)

| # | 未閉鎖 | 変化 |
|---|---|---|
| **FAM-a** | ★★ **(M2)** 標準模型と窓の算術被覆の同定 | **$n=7$ は C-β で閉じた**(cross-checked)。**全奇数 $n$ は未閉鎖 — 依然として最大の穴** |
| **FAM-b** | (M4) $[\gamma]=1$ | ★ **M2 の系へ吸収**(§3.3)。独立項目としては閉じる |
| **FAM-c** | (D-3e) $n$ 一般での機械確認 | 不変($n\in\{3,7,9,11,13\}$ のみ) |
| **FAM-d** | (C6) $[\alpha]$ 規約 | ★ **C1′-sel / C1′-adm に分割**。**sel は類・位数 gate から外れた**。adm = M2 |
| **FAM-e** | (GR) | 不変(【文献要請 U7-3】・既出) |
| **FAM-f** | $n=5$ | ★ **定理領域から明示除外**(§4)。運用と量化が一致した |
| **FAM-g**(新) | **持上げ規約の外部照合** | $n=3$ の LMFDB 経路は一様化元 $x$ で $u_3=-4$。工房標準($\widetilde\alpha=1$)と符号が一致するのは**照合済の事実**だが、$n\ge7$ で同種の外部照合は無い ⟹ **符号規約の外部固定は $n=3$ の 1 点のみ** |

> ### 【文献要請】(本追補からの新規はゼロ)
> 既出の **U7-3((GR) の正確な形・軽い)** のみ。

---

## 6. FINDING(本追補の分)

| # | 格 | 内容 |
|---|---|---|
| **FU-LIFT** | ★★ **補題(新規・証明あり)** | **補題 LIFT**: 持上げの曖昧さ $\widetilde\alpha\mapsto\widetilde\alpha+n$ は**一様化元の取り替え $y\mapsto gy$ と同一の操作**($\rho=g(i)=-i$、$u\mapsto u\rho^{-2n}=-u$)。⟹ 公式 $4(-1)^{\widetilde\alpha}$ は**内部整合**であり、持上げは**模型 datum に既に含まれていた** |
| **FU-TYPE** | ⚠ **自認(型の修正)** | 定理の量化を $\alpha\in(\mathbf Z/n)^\times$ から $\widetilde\alpha\in\mathbf Z$ へ。(4) は模型代表元に相対的と明記(W94-3.1 受諾) |
| **FU-SIGN** | ★ **系(新規)** | 符号を決める不変量は $\widetilde\alpha\bmod2$。整数の窓同値類は両 parity を含む ⟹ **符号は窓の不変量ではない**。「窓 + 符号」の最小水準は $\widetilde\alpha\bmod 2n$ |
| **FU-NORM** | **規約(新設)** | 工房標準 = 窓水準の正規化 $\widetilde\alpha\in\{1,\dots,\frac{n-1}2\}$。cert に `alpha_lift`(整数値)欄を新設し `alpha_convention` と分離。**この関数自体が規約依存**であることを併記 |
| **FU-C1SPLIT** | ★ **前件の分割(Sol 裁定の反映)** | **C1′-sel は類・位数 gate から外れる**(F94-3.2 YES)。**C1′-adm = M2 は外れない**(同 NO) |
| **FU-M4** | ★ **前件の降格** | **M4($[\gamma]=1$)は M2 の系**。独立前件から外し、**M2 より先に M4 を使うことを禁止**(循環)。未閉鎖項が 1 本減る(困難が消えたのではない) |
| **FU-N5** | **射程の確定** | 定理領域から **$n=5$ を明示除外**。量化と運用上の noncontact を一致させた(W94-3.2 履行) |

---

## 7. Sol への申し送り(次便)

- **監査点 A**: **補題 LIFT** の (d) — 「$g=-i(1+O(y^n))$ ゆえ一様化元の先頭係数はちょうど $\rho=-i$」。$t=k-i$ と $y$ の関係($t=h_1^{-1}y^n(1+O(y))$)を経由しているので、$O$ の位数の扱いに穴がないか見てほしい。**主張は $\rho^{2n}=-1$ という 1 行に集約される**ので、そこだけ潰れれば十分。
- **監査点 B**: **窓水準の正規化** $\widetilde\alpha\in\{1,\dots,\frac{n-1}2\}$ の採用。これは「$u$ を窓の関数にする」が、**その関数自体は規約依存**である(代表を上半分から取れば全符号反転)。この二重性を cert の 2 欄(`alpha_lift` / `alpha_convention`)で表す設計で足りるか。
- **監査点 C**: **(M4) の降格**。$h(0)=(-1)^{\widetilde\alpha+1}$、$h(\infty)=1$ から $R_\pm$ の $F_n$-有理性 ⟹ $[\gamma]=1$ という筋(F94-3.2)を、私は **M2 ⟹ M4 の含意**として前件表に書き込んだ。$R_\pm$ が本当に $k=0,\infty$ 上の点であること($\lambda(0)=\lambda(\infty)=1$・$\sigma$ 固定点)まで含めて、循環がないか確認いただきたい。
- **監査点 D**: **$n=5$ を定理領域から切った**判断。「形式的には含むが評価延期」ではなく「領域から除外」を選んだが、これで W94-3.2 の要求を満たしているか。
