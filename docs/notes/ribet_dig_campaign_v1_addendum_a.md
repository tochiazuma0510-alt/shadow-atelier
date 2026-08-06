# RIBET-DIG 追補 A — 発案札 v2 の 3 枚検分(裁定 717)

**状態札: `paper proof / all candidate / Sol 未監査 / GAP 実走ゼロ・窓生成ゼロ・cert 発行ゼロ / 封印非接触・S₁₂@691 非形成(S 側の値に言及も推測もしない)/ 判定語の発効は司令塔専権 / 本体 ribet_dig_campaign_v1.md は不改変(versioned)`**

- 起草: 影工房 **数学者**(Claude / Opus 5)・2026-08-06 / 委嘱: **裁定 717**(発案札 v2 = `ideas_ribet_dig_v2.md`(b1a3c6e)の指定 3 枚 RDV-5 / RDV-2 / RDV-4)
- 入力正本: `ribet_dig_campaign_v1.md`(本体)/ `ideas_ribet_dig_v2.md` / `aside_measurement_design_v1_addendum_d.md`(**読み出しのみ・非改変**)/ `docs/week1-定義ノート.md` §2(hexagon (3.3)(3.4)・charming・GT-shadow・settled/isolated・reduction (3.60)・χ_vir)/ `sg_band_sweep_prereg_iffirst_v1.md` §2 / `search/certs/lins_twin_census_v1_20260806.json`(読み出しのみ)
- **自前検算の申告**: python の小スクリプト(整数演算・GAP 不使用・cert ではない)で $R_0(p)$($p=5,7,11,13$)を明示構成し、本追補の紙の導出($\mathrm{ord}(s_1)=2p$・$\bar x,\bar y$ の座標・**両 hexagon の恒等性**)を再現した。**格は上げない。**

---

## 0. 判定(先に 6 行)

| 札 | 判定 | 中身 |
|---|---|---|
| **RDV-2** | ★ **半分は既証明・吸収/半分は新規かつ正しい** | 回文(定理 D-1)と台 $[4,8]$(定理 D-2)は **`aside_measurement_design_v1_addendum_d.md` §1.2–§1.3 で既に証明済** ⟹ 重複。★ **新規なのは「正典超過 = 深さ 6 の 1 段だけ」への縮約**で、これは **3 行で正しく証明できる**(§1.2)。追補 D §0.8 の新規性会計「深さ 6,7,8 の消滅」を **「深さ 6 のみ」へ縮める**(§1.3) |
| **RDV-4(前半)** | ★ **成立・証明した** | **命題 UNIQUE-FLOOR**: $R_0(p)$ を $C_p$ で 1 階建て増しした群は同型を除き**ちょうど 3 種**、うち**非分裂はただ 1 つ = $G_p$**(§3.1) |
| **RDV-4(後半)** | ★ **反証した** | 札の分裂双子 $(\mathbf F_p(\chi)\oplus V)\rtimes S_3$ は **$(2,3)$-生成しない ⟹ 窓ではない**(§3.2)。札自身が挙げた破綻シナリオが的中 |
| **RDV-4(代替)** | ★ **正しい対照列を同定した** | 分裂 Borel 型の対照は $\boxed{C_p\rtimes(C_3\times S_3)}$(位数 $18p$・$6\mid p-1$ のときのみ存在)。**これは既存 census の 6 窓そのもの**(126/234/342/558/666/774 $=18q$、$q\equiv1\ (6)$)。$p=691$ では**位数 12,438** — 即計算可(§3.3) |
| **RDV-5(ii)** | ★ **紙で確定**(二択でなく一意) | $n:=\mathrm{ord}(\sigma_1N)=\mathbf{2p}$。$p=691$ で $\boxed{n=1382}$。札の「$n\in\{2,1382\}$」の $2$ は**起こらない**(§2.2・検算 4/4) |
| **RDV-5(iii)** | ★ **札の論法を却下・明示構成で置換** | $R_0(p)$ は**明示的自己同型 $\beta=\varphi_{-1}\circ\mathrm{Ad}(\tilde t)$ で reflexible**(§2.3)。★ **reflexible 窓に witness word は存在しない**(witness word は chiral 窓の証拠物)。札の「SECT 全通過 ⟹ 層 3 不能 ⟹ reflexible」は**既知偽の逆命題**を使っている(§2.3.1)。**ORB 不使用という結論だけは正しい** |
| **RDV-5(iv)(v)** | ★★★ **測る前に紙で閉じた** | **定理 LADDER-SAT**: 梯子窓は**深さ 1・深さ 2 とも** $N_{\rm ord}=p$・$\lvert GT(N)\rvert=p-1$・$GT(N)\cong C_{p-1}$・**全 shadow settled(isolated)**・**算術飽和**($\mathrm{Ih}_N$ 全射)。$p=691$ で $\lvert GT\rvert=\mathbf{690}$(§2.4–§2.6) |

> ### ★★ 本追補の最重要結果
> $$\boxed{\ \textbf{梯子 }\{R_0(p),\,G_p\}\ \textbf{は全ての }p\ge5\ \textbf{で算術飽和である(691 を含む)。ゆえに B 型 shadow は梯子に存在しない。}\ }$$
> これは **dihedral 族(FAM-U-ASM)に次ぐ第 2 の算術飽和族**であり、**測定ではなく紙で得られた**(機械は確認に使うだけ)。地図の**軸 (i) 算術飽和軸**への直接の領土追加である。
> ★ 同時に、RDV-6 が「ceremony の結果次第の二枝」として立てていた問い(梯子は B 型狩場か飽和観測所か)は、**$k^*$ の値に依存せず**決着する — 飽和が直接証明されたので SYN-0/W-1 を経由する必要がない。**S₁₂@691 に一切触れずに答えが出た。**

---

# 1. RDV-2 の検分(委嘱: 3 行検分)

## 1.1 重複部分 — **既証明・吸収**

RDV-2 の主張 (i)(ii)(iii) のうち:

| RDV-2 の主張 | 既在 | 判定 |
|---|---|---|
| (i) $\theta$ は深さ $d\mapsto12-d$、$\theta D=-D$ ⟹ $\theta(D_d)=-D_{12-d}$ ⟹ 項数回文は定理 | **定理 D-1**(`aside_..._addendum_d.md` §1.2) | ★ **完全に同内容 ⟹ 吸収**(新規性なし) |
| (ii) 台の左端: $D_2=0$(定理 C-A)+ Prop 4.3 のパリティ ⟹ $D_3=0$ ⟹ 先頭深さ 4 | **定理 D-2**(同 §1.3 の (i)(ii)(iii)) | ★ **完全に同内容 ⟹ 吸収** |
| (iii) (i)+(ii) ⟹ 深さ 9..12 の消滅も自動 | **定理 D-2 の (iv)** | ★ **同内容 ⟹ 吸収** |

> ★ RDV-2 が「grep: 回文/palindrome の説明は repo 0 hit」としたのは**検索語の問題**である(追補 D は「回文」を平文で扱い、`D-1`/`D-2` という札名で立てている)。**発案係へのフィードバック**: 既在確認は札名(`D-1` 等)と概念語(「$\theta$-反対称」「台」)の両方で引くこと。

## 1.2 ★ 新規部分 — 「正典超過 = 深さ 6 の 1 段だけ」(**3 行で証明**)

RDV-2 の**残り 1 行**、すなわち
$$\text{「正典保証(深さ 4,5)}\ +\ \theta\ \Longrightarrow\ \text{深さ 7,8 は無料}\ \Longrightarrow\ \text{超過の実体は }D_6\ \text{のみ」}$$
は **追補 D に無い**(同 §0.8 の新規性会計は「深さ **6,7,8** の消滅」と 3 段を数えている)。これは**正しい**。証明:

> ### 命題 A-1(candidate・本追補)
> 定理 D-1($\theta(D_d)=-D_{12-d}$、係数保存の全単射)と、正典が $\bmod\,691$ で保証する範囲(**深さ 4** = Brown (8.8) の $\tfrac{691}{144}e_{12}$、**深さ 5** = 同 §8.4 の「prop 6.4 経由で depth 5 にも propagate」)を仮定する。このとき
> $$D_4\equiv0,\ D_5\equiv0\ (691)\ \Longrightarrow\ D_8=-\theta(D_4)\equiv0,\quad D_7=-\theta(D_5)\equiv0\ (691).$$
> 台は $[4,8]$(定理 D-2)、$\theta$ の対合で $4\leftrightarrow8$・$5\leftrightarrow7$・**$6$ は自己対**。ゆえに
> $$\boxed{\ \textbf{正典から従わない実質は }D_6\equiv0\ (691)\ \textbf{の 1 段のみ。}\ }$$
> **証明.** $\theta$ は語の全単射で係数を保存し $\bmod\,691$ の還元と可換 ⟹ $D_d\equiv0\Rightarrow D_{12-d}\equiv0$。$d=4,5$ に適用。深さ 6 は $\theta(D_6)=-D_6$ を与えるだけで、これは $D_6$ が $\theta$ の $(-1)$-固有部分にあることを言うにすぎず**消滅を強制しない**。∎

> ### ⚠ 条件の明示(過大主張しない)
> 命題 A-1 は「正典が深さ 4,5 を保証する」を**前提**にしている。その前提自体は
> - **深さ 4**: (8.8) の係数が $691/144$ であること + **$e_{12}$ が我々の格子で 691 進整**であること(逐語ノート §3.2 の「整性 UNKNOWN」)、
> - **深さ 5**: Brown の "propagates to depth five also"(prop 6.4 経由)の逐語主張、
> に依存する。ゆえに命題 A-1 は **条件付きの縮約**であり、【C-GAP-2】を**閉じるのではなく 1 次元に絞る**。⟹ 新規【A-GAP-1】: $e_{12}$ の整性が崩れると深さ 4 の「正典保証」が外れ、超過は $\{4,6,8\}$ の 2 自由度に戻る。

## 1.3 追補 D への差分提案(**1 行の書き換え**・本追補は D を改変しない)

追補 D §0.8 の新規性会計:
- 現行: 「新規 = **深さ 6,7,8 の消滅**・格子の明示・一般素数プロファイル・近傍対照の 4 点」
- 提案: 「新規 = **深さ 6 の消滅**(深さ 7,8 は定理 D-1 と正典の深さ 4,5 から従属・命題 A-1)・格子の明示・一般素数プロファイル・近傍対照の 4 点」
⟹ **新規性の主張が弱くなるのではなく、正確になる**(3 段のうち 2 段は自前の定理 D-1 の帰結だと明示できる = 説明力が上がる)。**書き換えの実行は D の管轄係へ**(本追補は触らない)。

---

# 2. RDV-5 の検分と再設計(最優先)

## 2.1 舞台の固定(記号)

本体 §1.1 の $G_p=H_{p^3}\rtimes_\rho S_3$、$R_0(p):=G_p/Z(H)\cong V\rtimes S_3$($V=\mathbf F_p^2$ = 標準表現、位数 $6p^2$)。
$V=\{x\in\mathbf F_p^3:\sum x_i=0\}$、$S_3$ は座標置換 $(\sigma\cdot x)_i=x_{\sigma^{-1}(i)}$。標識対は
$$U=\bigl((1,-1,0),\,(12)\bigr)\ (=\bar\Delta),\qquad W=\bigl((0,0,0),\,(123)\bigr)\ (=\bar\delta).$$
($v=(1,-1,0)$ は $\rho((12))$ の $(-1)$-固有直線の非零元 ⟹ 本体 定理 LADDER-WIN の生成条件を満たす。スケーリング $v\mapsto\lambda v$ は $\mathrm{Out}$ の作用ゆえ一般性を失わない。)
$B_3=\langle\Delta,\delta\mid\Delta^2=\delta^3\rangle$、$\sigma_1=\delta^{-1}\Delta$、$\sigma_2=\Delta^{-1}\delta^2$(`sg_band_sweep` §2.2)。

> ### 補題 A-2(生成元の像・本追補で計算・検算済)
> $$s_1:=\overline{\sigma_1}=W^{-1}U=\bigl((-1,0,1),\,(23)\bigr),\qquad s_2:=\overline{\sigma_2}=U^{-1}W^2=\bigl((1,-1,0),\,(13)\bigr),$$
> $$\bar x:=s_1^2=(-2,1,1),\qquad \bar y:=s_2^2=(1,-2,1)\quad(\in V).$$
> $\bar x,\bar y$ は $p\ge5$ で一次独立(比例なら $p\mid3$)⟹ $\langle\bar x,\bar y\rangle=V$。

## 2.2 ★ (ii) $n=\mathrm{ord}(\sigma_1N)$ — **$2p$ に確定**(札の二択を解消)

$s_1=(w,\tau)$、$\tau=(23)$、$w=(-1,0,1)$。$s_1^2=\bigl((1+\rho(\tau))w,\,1\bigr)$ で $1+\rho(\tau)$ は階数 1(固有値 $2$ と $0$)。ゆえに
$$n=\begin{cases}2 & w\in\ker(1+\rho(\tau))\\ 2p & \text{otherwise}\end{cases}$$
$\ker(1+\rho((23)))=\{x:x_1=0,\ x_2=-x_3\}=\langle(0,1,-1)\rangle$。$w=(-1,0,1)\notin$ それ($w_1=-1\ne0$)。
$$\Longrightarrow\ \boxed{\ n=2p\ \ (\text{全 }p\ge5),\qquad p=691:\ n=\mathbf{1382}\ }$$
**一般性**: 生成条件は $v\ne0$ のみで、$w=\rho(u)^{-1}v$ の第 1 座標は $v$ のスケール倍 ⟹ $v\ne0$ なら常に $w_1\ne0$。$W=(0,u^2)$ を選んでも同様($\tau=(13)$、$w=\rho(u)v=(0,1,-1)\cdot$、$\ker(1+\rho((13)))=\langle(1,0,-1)\rangle$ で不属)。$G_p$ 上でも $s_1^2$ の $V$-像が非零ゆえ $\exp H=p$ より $\mathrm{ord}=2p$(**深さ 1・2 で同値**)。
**検算**: $p=5,7,11,13$ で $\mathrm{ord}(s_1)=10,14,22,26=2p$ ✔ 4/4。

> ★ **札への訂正**: 「$n\in\{2,1382\}$(どちらかは実測)」は**実測不要**。$n=2$ は生成条件と両立しない(生成する標識対では常に $n=2p$)。⟹ **MAP-DICT の突合キーは測る前に $1382$ で凍結してよい。**

## 2.3 ★ (iii) 掌性 — **明示構成で置換**(札の論法は却下)

> ### 補題 A-3(candidate・本追補。本体 §1.5 の $R_0$ 版・$Z$ 補正が不要な分だけ簡単)
> $\varphi_{-1}:(x,\sigma)\mapsto(-x,\sigma)$ は $\mathrm{Aut}(R_0)$ の元($-\mathrm{id}$ は $S_3$-同変)。$\tilde t:=(0,(12))$ とすると
> $$\beta:=\varphi_{-1}\circ\mathrm{Ad}(\tilde t)\ \in\mathrm{Aut}(R_0):\qquad \beta(U)=U,\quad \beta(W)=W^{-1}\quad(\textbf{どちらも厳密}).$$
> **証明.** $\mathrm{Ad}(\tilde t)(U)=(\rho(t)v,\,t)=(-v,t)$、$\varphi_{-1}$ で $(v,t)=U$ ✔。$\mathrm{Ad}(\tilde t)(W)=(0,tut^{-1})=(0,u^{-1})$、$\varphi_{-1}$ は $V$-成分 $0$ を動かさない ⟹ $W^{-1}$ ✔。∎
> ⟹ 補題 MIRROR-PSL より $\boxed{\iota(N_{R_0})=N_{R_0}}$ — **$R_0(p)$ は全 $p$ で reflexible**。

### 2.3.1 ★ 札 (iii) の論法の欠陥(2 点)

1. **witness word は存在しない。** MC-1 型の witness word は「$w\in N$ で $\rho(\iota(w))\ne1$」を出すもので、これは **$\iota(N)\ne N$(chiral)の証拠物**である。$R_0$ は reflexible なので**そのような語は原理的に存在しない**。札の「紙の結論を witness word 1 本で照合する」は**型が合っていない**。
2. **「SECT 全通過 ⟹ 層 3 不能 ⟹ reflexible」は既知偽の逆命題を使う。** 工房の確定事実(§G.9.2 の三層成層)は
 - **SECT 破れ $\Rightarrow$ chiral**(定理 SECT-CHIRAL)であって、
 - **SECT 全通過 $\Rightarrow$ reflexible は偽**(それが**層 3 の定義そのもの** — `(1944,826)`/`(1944,921)` が反例)。
 札は「$\Phi(R_0)=1$ ゆえ層 3 は不能」で穴を塞ごうとしているが、その根拠(1 ビット法則「層 3 $\iff X\le\Phi$」)は §G.11.1 で **5/5 の経験則を機構つき命題(candidate)に格上げした段階**であり、**定理ではない**。⟹ **札の連鎖は candidate の上に candidate を積む**。
 $$\Longrightarrow\ \textbf{補題 A-3 の明示 }\beta\ \textbf{が、その連鎖を全部不要にする。}$$

### 2.3.2 正しい機械照合(**秒・$\mathrm{Aut}$ 不使用**)

$$\text{(a) }\beta\ \text{が準同型か(生成元 }U,W\text{ 上の定義が関係子を保つか)を検査}\quad\text{(b) }\beta(U)=U,\ \beta(W)=W^{-1}\ \text{を検査}$$
$R_0$ の位数 $6p^2$ の元 1 つずつに $\beta$ を評価するだけ($p=691$ で 2.86M 元・線形写像 ⟹ 秒)。あるいは**もっと安く**、$\beta$ を $V$ 上の行列 $-\rho(t)$ と $S_3$ 上の $\mathrm{Ad}(t)$ で与えて $2\times2$ 行列 1 個の照合で終わる。
★ **札の結論「ORB(Aut 悉皆)は撃たない」は正しい**(位数 $10^6$ 超で汎用メソッドは実用外)。**理由が違う**だけである。

## 2.4 ★★★ (iv) hexagon — **線形式ではなく恒等式**(深さ 1)

**charming の帰結(効く順に)**: $c\in N$ ゆえ $F_2/N_{F_2}\cong PB_3/N=P$。$R_0$ では $P=V$ で**可換** ⟹
$$[F_2/N_{F_2},\,F_2/N_{F_2}]=1\ \Longrightarrow\ \boxed{\ \textbf{charming GT-pair は }f\equiv1\ \textbf{を強制}\ }$$

> ### 補題 A-4(candidate・本追補。一般形)
> $N$ を $B_3$ 窓($c\in N$)とし $P=PB_3/N$ が**可換**なら、$GT(N)$ の全ての元は $[m,1]$ の形。ゆえに $\chi_{\rm vir}:[m,f]\mapsto2m+1$ は **$GT(N)\hookrightarrow(\mathbf Z/N_{\rm ord})^\times$ 単射**。

$f=1$ を hexagon (3.3)(3.4) に代入すると、$T_{m,1}(\sigma_i)=\sigma_i^{2m+1}$ の well-definedness、すなわち
$$s_1^{2m+1}s_2^{2m+1}s_1^{2m+1}=s_2^{2m+1}s_1^{2m+1}s_2^{2m+1}$$
と同値になる。$s_i^{2m+1}=\bar x^m s_1$ 型に展開して $V$ 成分を比べると:

> ### 命題 A-5(candidate・本追補。**札が「凍結すべき線形式」と呼んだもの**)
> (3.3) $\iff m\cdot\bigl[\ \bar x+\rho(\tau_1)\bar y+\rho(\tau_1\tau_2)\bar x\ \bigr]=0$、(3.4) $\iff m\cdot\bigl[\ \bar y+\rho(\tau_2)\bar x+\rho(\tau_2\tau_1)\bar y\ \bigr]=0$。
> ここで $\tau_1=(23)$、$\tau_2=(13)$、$\tau_1\tau_2=(123)$、$\tau_2\tau_1=(132)$。**両括弧は $\mathbf 0$ である**:
> $$\bar x+\rho(\tau_1)\bar y+\rho(u)\bar x=(-2,1,1)+(1,1,-2)+(1,-2,1)=(0,0,0),$$
> $$\bar y+\rho(\tau_2)\bar x+\rho(u^{-1})\bar y=(1,-2,1)+(1,1,-2)+(-2,1,1)=(0,0,0).$$
> $$\Longrightarrow\ \boxed{\ \textbf{両 hexagon は }m\ \textbf{に依らず恒等的に成立する。線形式は退化しており「凍結すべき係数」は存在しない。}\ }$$
> **検算**: $p=5,7,11,13$ で「全ての $m$ について braid 関係が成立」を機械で確認 ✔ 4/4。

## 2.5 ★★★ (iv) の帰結 — $GT$ の完全決定

- $N_{\rm ord}=\mathrm{lcm}(\mathrm{ord}\,\bar x,\mathrm{ord}\,\bar y,\mathrm{ord}\,\bar c)=\mathrm{lcm}(p,p,1)=\mathbf p$。
- charming: $\gcd(2m+1,p)=1\iff 2m+1\not\equiv0$ ⟹ $m$ は $p-1$ 通り。
- 全射性: $\langle\bar x^{2m+1},\bar y^{2m+1}\rangle=\langle(2m+1)\bar x,(2m+1)\bar y\rangle=V$ ✔(補題 A-2)。
- hexagon: 恒等(命題 A-5)。

> ### 定理 A-6(candidate・本追補)
> $$\boxed{\ GT(N_{R_0(p)})=\{[m,1]\ :\ 2m+1\in(\mathbf Z/p)^\times\},\qquad \lvert GT\rvert=p-1 .\ }$$
> **さらに全 shadow は settled、$N_{R_0(p)}$ は isolated、$GT\cong C_{p-1}$。**
> **証明(settled).** $T_{m,1}$ は $B_3\twoheadrightarrow R_0$ の全射で、その核 $K$ は $B_3/K\cong R_0$ を与える。$T_{m,1}$ が定める標識対は $(\Delta,\delta)\mapsto(U,\,s_1^{2m+1}s_2^{2m+1})$ であり、これも生成 $(2,3)$-対である。本体 **定理 LADDER-UNIQ-N**($R_0$ 版: 生成 $(2,3)$-標識対は $6p^2(p-1)$ 個、$\lvert\mathrm{Inn}\rvert=6p^2$($Z(R_0)=1$)、スカラー $\mathbf F_p^\times\le\mathrm{Out}$ ⟹ $\mathrm{Aut}$-軌道は 1 個)より、**任意の生成標識対は $(U,W)$ と $\mathrm{Aut}$-同値** ⟹ $K=N$。∎
> **群構造.** 合成 (3.53) で $2m+1$ は乗法的 ⟹ $\chi_{\rm vir}$ は単射準同型 $GT\to(\mathbf Z/p)^\times$ で、位数一致 ⟹ 同型。∎

## 2.6 ★★★ (v) 算術像 — **飽和が紙で出る**(下界ではなく等号)

> ### 定理 LADDER-SAT(candidate・本追補。**戦役の主結果**)
> 全ての $p\ge5$ について、深さ 1 の窓 $N_{R_0(p)}$ と深さ 2 の窓 $N_{G_p}$ の**両方**で
> $$\boxed{\ N_{\rm ord}=p,\quad \lvert GT(N)\rvert=p-1,\quad GT(N)\cong C_{p-1},\quad N\ \text{は isolated},\quad \mathrm{Ih}_N:G_{\mathbf Q}\twoheadrightarrow GT(N)\ \textbf{全射(算術飽和)}\ }$$
> **ゆえに梯子には非算術 shadow が存在しない — B 型は棲めない。**

**証明.**
**(A) 深さ 1 の飽和.** $\chi_{\rm vir}\circ\mathrm{Ih}_{N}=\chi_{\rm cyc}\bmod N_{\rm ord}=\chi_{\rm cyc}\bmod p$ は $(\mathbf Z/p)^\times$ に**全射**(円分指標の全射性)。定理 A-6 より $\chi_{\rm vir}:GT(N_{R_0})\xrightarrow{\sim}(\mathbf Z/p)^\times$ ⟹ $\mathrm{Ih}$ 全射。∎

**(B) 深さ 2 の $f$ は $m$ で決まる.** $G_p$ では $P=H$ 非可換で $[F_2/N_{F_2},F_2/N_{F_2}]=[H,H]=Z\cong C_p$ ⟹ charming は $f\in Z$ を許す。$f=\zeta^k$ と書く。$Z$ への共役は $\mathrm{sgn}$ でねじれる($\det=-1$・本体 補題 DET-FORCED)ので、$s_2^{2m+1}$ の $S_3$-成分が奇($\tau_2^{2m+1}=\tau_2$)であることから
$$f^{-1}s_2^{2m+1}f=s_2^{2m+1}f^{2},\qquad f^{-1}s_1s_2=s_1s_2f^{-1}\ (\tau_1\tau_2=u\ \text{は偶}).$$
(3.3) はしたがって
$$(s_1s_2)^{-1}s_1^{2m+1}s_2^{2m+1}\,\bar x^{\,m}\ =\ f^{-3}$$
となる。左辺は命題 A-5 により $V$ で $0$ ⟹ **$Z$ の元**。$p\ge5$ ゆえ $3\in\mathbf F_p^\times$ ⟹ **$k$ は $m$ から一意に定まる**。
$$\Longrightarrow\ \boxed{\ R:GT(N_{G_p})\longrightarrow GT(N_{R_0(p)}),\ [m,f]\mapsto[m,1]\ \textbf{は単射}\ }\qquad\text{ゆえに }\lvert GT(N_{G_p})\rvert\le p-1 .$$
($R$ は reduction (3.60);$N_{G_p}\le N_{R_0}$ かつ両者の $N_{\rm ord}$ はともに $p$、$Z\le N_{R_0}\cap F_2$ ゆえ $R$ は「$f$ を忘れる」写像である。)

**(C) 深さ 2 の飽和.** 関手性 $R\circ\mathrm{Ih}_{N_{G_p}}=\mathrm{Ih}_{N_{R_0}}$ と (A) より $R(\mathrm{Im}\,\mathrm{Ih}_{N_{G_p}})=GT(N_{R_0})$、位数 $p-1$。(B) の単射性より
$$p-1=\bigl\lvert R(\mathrm{Im}\,\mathrm{Ih})\bigr\rvert=\lvert\mathrm{Im}\,\mathrm{Ih}\rvert\le\lvert GT(N_{G_p})\rvert\le p-1 .$$
⟹ 全て等号 ⟹ **$\mathrm{Ih}_{N_{G_p}}$ 全射・$\lvert GT(N_{G_p})\rvert=p-1$・$R$ は全単射**。∎
**(D) isolated.** 本体 定理 LADDER-UNIQ-N(軌道数 1)より $B_3\twoheadrightarrow G_p$ の核は一意 ⟹ 全 shadow settled ⟹ isolated。$GT\cong C_{p-1}$ は $\chi_{\rm vir}$ が単射準同型で位数一致。∎
$\blacksquare$

> ### ★ $p=691$ での値(**測る前に凍結**)
> | 量 | 深さ 1: $R_0(691)$(位数 2,864,886) | 深さ 2: $G_{691}$(位数 1,979,636,226) |
> |---|---|---|
> | $N_{\rm ord}$ | **691** | **691** |
> | $n=\mathrm{ord}(\sigma_1N)$ | **1382** | **1382** |
> | $\lvert GT(N)\rvert$ | **690** | **690** |
> | $GT(N)$ | $\cong C_{690}$ | $\cong C_{690}$ |
> | $f$ の形 | $f\equiv1$(全 shadow) | $f=\zeta^{k(m)}\in Z$、$k$ は $m$ の関数 |
> | settled / isolated | 全 settled・isolated | 全 settled・isolated |
> | 算術像 | **$GT$ 全体(飽和)** | **$GT$ 全体(飽和)** |
> | 掌性 | **reflexible**(補題 A-3) | **reflexible**(本体 定理 LADDER-REFL) |
> | B 型 | **ゼロ**(飽和の帰結) | **ゼロ**(飽和の帰結) |

> ### ⚠ 格の限定(**正直に**)
> - 全て **candidate(単系統・Sol 未監査)**。「飽和」は**判定語**であり、**発効は司令塔専権**(本追補は「紙で証明した」までを主張する)。
> - (A) は円分指標 $G_{\mathbf Q}\to(\mathbf Z/p)^\times$ の全射性(古典)を使う。**これは工房の Lean 化対象外の古典事実**として引用している(既在の規律「Mathlib 不在定理は公理化」と同じ扱いを推奨)。
> - (B) の共役計算は $\det=-1$(補題 DET-FORCED)に全面的に依存する。**作用が忠実標準表現であることが前提**。
> - 定理 A-6 の settled 部分は **LADDER-UNIQ-N に依存**し、そちらは【DIG-GAP-2】(本体 §7.1)で $\lvert\mathrm{Out}\rvert$ の上界を軌道数から逆算している。**独立の $\mathrm{Aut}$ 計算で裏を取るのが望ましい**(§4 の V-5)。

## 2.7 ★ RDV-5 の再設計(**発注可能な粒度**・IF-FIRST 凍結込み)

**位置づけの変更**: 札は 5 点を「第一実弾(発見のための測定)」としたが、§2.2–§2.6 により **5 点すべてが紙で閉じた**。ゆえに残るのは**確認**であり、優先度は下がるが**検定力は上がる**(全ての値が事前に凍結されているため)。

> ### 発注仕様 **DIG-R0-1**(数学者 → 実装係・**IF-FIRST 凍結済**)
> **宇宙の事前登録(後から変えない)**: $p\in\{5,7,13\}$(較正)$\cup\{691\}$(本番)。群は $R_0(p)=V\rtimes S_3$、$V=\{x\in\mathbf F_p^3:\sum x_i=0\}$、$S_3$ = 座標置換。標識対 $U=((1,-1,0),(12))$、$W=(0,(123))$。**この生成系以外を使わない。**
> **環境制約の織り込み**(裁定 709 系の実測): 位数 $10^6$ 超で GAP の汎用メソッド(`AutomorphismGroup`・`IdGroup`・`ConjugacyClasses`)は実用外。$p=691$ では **`Group()` + `Size` + 行列演算のみ**で完結する設計にする(下の全項目はそれで足りる)。
>
> | # | 測る量 | 実装(全て線形代数 + $S_3$ の 6 元) | **凍結予言** | 外れたら |
> |---|---|---|---|---|
> | **R0-a** | $\lvert R_0(p)\rvert$、$R_0^{\rm ab}$、$\lvert Z(R_0)\rvert$、$\Phi(R_0)$ | 直接 | $6p^2$、$C_2$、$1$、$1$ | 本体 LADDER-WIN の $R_0$ 版が誤り ⟹ STOP |
> | **R0-b** | $(2,3)$-生成 | $\langle U,W\rangle$ の閉包サイズ | $=6p^2$ | 同上 ⟹ STOP |
> | **R0-c** | $n=\mathrm{ord}(s_1)$、$s_1=W^{-1}U$ | 直接 | $\mathbf{2p}$($p=691$: **1382**) | §2.2 の導出が誤り |
> | **R0-d** | $\bar x=s_1^2$、$\bar y=s_2^2$ の座標と一次独立性 | 直接 | $(-2,1,1)$、$(1,-2,1)$、独立 | 補題 A-2 が誤り |
> | **R0-e** | 全 $m\in\mathbf Z/p$ で braid 関係 $A B A=B A B$($A=s_1^{2m+1}$, $B=s_2^{2m+1}$) | $p$ 回の積 | **全 $m$ で成立** | 命題 A-5 が誤り ⟹ hexagon に非自明な線形式が残る(その係数が新データ) |
> | **R0-f** | $N_{\rm ord}$、$\lvert GT(N)\rvert$ | $\mathrm{lcm}$ と $m$ の数え上げ | $p$、$\mathbf{p-1}$($p=691$: **690**) | 定理 A-6 が誤り |
> | **R0-g** | 反射 $\beta=\varphi_{-1}\circ\mathrm{Ad}(\tilde t)$ が $\beta(U)=U$、$\beta(W)=W^{-1}$ を満たす自己同型か | $2\times2$ 行列 1 個 + 生成元 2 点 | **満たす(reflexible)** | 補題 A-3 が誤り ⟹ 掌性が復活(一級) |
> | **R0-h** | ★ $\mathrm{Aut}$-軌道数の独立確認(**$p=5,7$ のみ**) | 生成 $(2,3)$-対の BFS 正準形の相異なる個数 | **1**(⟹ settled / isolated / LADDER-UNIQ-N) | $\ge2$ ⟹【DIG-GAP-2】が現実の穴 |
>
> **カナリア**: (a) $p=5$ の $R_0(5)$ は位数 150 ⟹ SmallGroups で `IdGroup` が引ける — 引いて記録(照合用の外部キー)。(b) R0-e は $m=0$ で自明に成立するので**$m\ne0$ を必ず含める**。(c) 深さ 2($G_p$)は別発注(§4)。
> **禁止**: ORB(`AutomorphismGroup` 悉皆)は $p\ge11$ で撃たない。witness word 探索は**行わない**(reflexible では存在しないため — §2.3.1)。

---

# 3. RDV-4 の検分

## 3.1 ★ 前半「唯一の上階」 — **成立(証明)**

> ### 命題 UNIQUE-FLOOR(candidate・本追補)
> $p\ge5$、$R_0=R_0(p)=V\rtimes S_3$。$1\to C_p\to E\to R_0\to1$ なる拡大($C_p\trianglelefteq E$)の**群同型類**はちょうど 3 つ:
> $$E\cong R_0\times C_p,\qquad E\cong C_p\rtimes_{\rm sgn}R_0\ (\text{分裂}),\qquad E\cong G_p\ (\textbf{非分裂}).$$
> とくに $\boxed{\textbf{非分裂な 1 階建て増しは }G_p\ \textbf{ただ一つ}}$。
> **証明.** 作用は $R_0\to\mathrm{Aut}(C_p)=\mathbf F_p^\times$ で、可換ゆえ $R_0^{\rm ab}=C_2$ を経由 ⟹ **triv か sgn の 2 通りのみ**(TWIST-6 の $R_0$ 版)。
> *triv 側*: $\lvert S_3\rvert$ が $\bmod p$ 可逆ゆえ $H^2(R_0,\mathbf F_p)=H^2(V,\mathbf F_p)^{S_3}=(\Lambda^2V^*\oplus V^*)^{S_3}=(\mathrm{sgn}\oplus\mathrm{std})^{S_3}=0$ ⟹ **分裂のみ**。
> *sgn 側*: 本体 §1.5 より $H^2(R_0,\mathbf F_p(\mathrm{sgn}))=\mathbf F_p$(1 次元)⟹ 類は $0$ と非零 $p-1$ 個。$\mathrm{Aut}(C_p)=\mathbf F_p^\times$ が非零類に推移的に作用する ⟹ **群同型類としては分裂 1 つと非分裂 1 つ**。非分裂の代表は $Z\le\Phi$(FRAT-SPLIT)を満たす拡大 = $G_p$(本体 定理 LADDER-WIN (e))。∎

> ### ★ 意味(辞書行)
> $$\boxed{\ \textbf{各 }p\ \textbf{で「Frattini に隠れる 1 階」は選択肢ではなく一意 — 梯子は強制である。}\ }$$
> これは本体 定理 LADDER-UNIQ(**横**の一意性: $S_3$-作用は 1 つ)の**縦**版であり、札の言う「LADDER-UNIQ の階層版」という位置づけは正しい。

## 3.2 ★ 後半「分裂双子」 — **反証(窓ではない)**

> ### 命題 A-7(candidate・本追補)
> $E:=\bigl(\mathbf F_p(\mathrm{sgn})\oplus V\bigr)\rtimes S_3$(位数 $6p^3$、$\mathrm{Syl}_p$ 可換)は $(2,3)$-生成**しない**。ゆえに **$B_3$ 窓商ではない**(定理 SG-EXACT の G2 で落ちる)。
> **証明.** $W_1:=\mathbf F_p(\mathrm{sgn})$ は $E$ の直和因子ゆえ射影 $\pi:E\twoheadrightarrow W_1\rtimes S_3$ がある。$E=\langle U',W'\rangle$($\mathrm{ord}\,U'=2$、$\mathrm{ord}\,W'=3$)なら $\pi(E)=\langle\pi U',\pi W'\rangle$。$W_1\rtimes S_3$ で $\chi=\mathrm{sgn}$、$\chi(\pi W')=\mathrm{sgn}(3\text{-巡回})=1$ ⟹ **補題 CYC-CHAR**(本体 §2.2)より $\langle\pi U',\pi W'\rangle\ne W_1\rtimes S_3$ ⟹ 矛盾。∎
> (明示: $A_3$ が $W_1$ に自明作用 ⟹ 位数 3 の元は $W_1$-成分 $0$;位数 2 の元 $(b,\tau)$ と合わせて生成部分は位数 6 に閉じる。本体 §2.3 の erratum E-1 と**同じ死に方**。)

> ★ **札の自己申告どおり**(「分裂窓の (2,3)-生成は未証明 — 生成しない可能性も普通にある。その場合『分裂側は窓になれない』が新 no-go」)。**その枝が実現した**。得られた no-go の一般形:
> ### 系 SPLIT-1DIM-DEAD(candidate・本追補)
> $B_3$ 窓商 $\widehat G$ の正規 $p$-部分群($p\ge5$)が、**1 次元 $\mathbf F_p$-加群を $\widehat G$-直和因子として含む**なら、その因子の指標 $\psi$ は $\psi(U)\ne1$ **かつ** $\psi(W)\ne1$ を満たさねばならない ⟹ $\mathrm{ord}(\psi)=6$、$\widehat G^{\rm ab}=C_6$、$6\mid p-1$。
> (証明は命題 A-7 と同じ: 直和因子への射影 + CYC-CHAR。**TWIST-6 と RW-CYC の統合形**。)

## 3.3 ★★ 正しい対照列の同定(**RDG-6 死亡の穴を埋める**)

系 SPLIT-1DIM-DEAD より、**分裂 Borel 型の対照窓は $S_3$ トーラスでは作れない**($S_3^{\rm ab}=C_2$ で $\mathrm{ord}\psi\le2$)。$\mathrm{ord}\psi=6$ を実現する最小のトーラスは $Q$ で $Q^{\rm ab}=C_6$、$Q\twoheadrightarrow S_3$ ⟹ **$Q=C_3\times S_3$**(位数 18)。

> ### 定義・命題 SPLIT-TWIN(candidate・本追補)
> $6\mid p-1$ なる $p\ge5$ に対し、$\psi:C_3\times S_3\twoheadrightarrow C_6\hookrightarrow\mathbf F_p^\times$(位数 6)を取り
> $$\boxed{\ E_p\ :=\ C_p\rtimes_\psi(C_3\times S_3),\qquad \lvert E_p\rvert=18p\ }$$
> とすると $E_p$ は **$B_3$ 窓商**である:
> - $E_p^{\rm ab}=C_6$ ✔($\psi\ne1$ ゆえ $[E,E]\supseteq C_p$、$(C_3\times S_3)^{\rm ab}=C_6$)
> - $\twoheadrightarrow S_3$ ✔
> - $(2,3)$-生成 ✔($Q$ 側: $U'=(0,t)$、$W'=(a,u)$($a\ne0$)は $C_3\times S_3$ を生成;$\psi(U')$ は位数 2、$\psi(W')$ は位数 3 ⟹ **CYC-CHAR の条件を両方満たす** ⟹ 生成する)
> - $\mathrm{Syl}_p=C_p$ **巡回・正規** ⟹ **定理 MIRROR-ODD が発火** ⟹ **chiral**、witness $[-1,1]$ は**算術元**。
> - **RW-CYC と整合**: $\mathrm{ord}(\psi)=6$・$\widehat G^{\rm ab}=C_6$・$6\mid p-1$ ✔(3 条件すべて)。

> ### ★★ これは**既存 census の 6 窓そのもの**である
> | 指数 | $=18q$ | 構造(cert) | $q\bmod6$ |
> |---:|---|---|---:|
> | 126 | $18\cdot7$ | `C7 : (C3 x S3)` | 1 |
> | 234 | $18\cdot13$ | `C13 : (C3 x S3)` | 1 |
> | 342 | $18\cdot19$ | `C19 : (C3 x S3)` | 1 |
> | 558 | $18\cdot31$ | `C31 : (C3 x S3)` | 1 |
> | 666 | $18\cdot37$ | `C37 : (C3 x S3)` | 1 |
> | 774 | $18\cdot43$ | `C43 : (C3 x S3)` | 1 |
> | (882) | $18\cdot49$ | `C49 : (C3 x S3)` | $q=7$ の 2 乗版 |
>
> $$\boxed{\ \textbf{分裂 Borel 対照列は「新設」ではなく「既に測ってある」。}\ }$$
> ⟹ **RDG-6(死亡)の穴は、新規構成ゼロで埋まる。** $p=691$ の member は $E_{691}=C_{691}\rtimes(C_3\times S_3)$、**位数 12,438** — 汎用 GAP メソッドの射程内(位数 $10^6$ 未満)。
> ⚠ **存在条件**: $6\mid p-1$。梯子の素数では **$p=7,13,37$ で存在**、**$p=5,11,41$ では存在しない**($6\nmid4,10,40$)。⟹ 対照列は**全 $p$ で並ばない**(札の「毎 $p$ 並ぶ」は誤り)。

> ### ★ Ribet 辞書の 2 側面が $p=691$ で実物として並ぶ
> | | **分裂 Borel 型** $E_{691}$ | **Frattini 隠れ型** $G_{691}$ |
> |---|---|---|
> | 位数 | **12,438**($=18\cdot691$) | 1,979,636,226 |
> | $\mathrm{Syl}_{691}$ | $C_{691}$ **巡回** | $H_{691^3}$ **非巡回** |
> | $C_{691}\le\Phi$? | **✗**(FRAT-SPLIT: 分裂) | **✔**(非分裂) |
> | ねじれ $\mathrm{ord}\chi$ | **6** | **2**(sgn) |
> | $\widehat G^{\rm ab}$ | $C_6$ | $C_2$ |
> | 掌性 | **chiral**(MIRROR-ODD) | **reflexible** |
> | $[-1,1]$ | 非 settled・**算術元** witness | settled |
> | 算術飽和 | **未決**(本追補の射程外) | ★ **飽和**(定理 LADDER-SAT) |
>
> ⟹ 「算術的非分裂は余素部分に現れず $p$ 群内部の非分裂へ強制される」という**戦役の辞書**が、**同一素数 691 の 2 つの実在窓**として並んだ。**これが RDV-4 の本当の収穫である。**

---

# 4. 【GAP】と次の一手

## 4.1 新規【GAP】

| # | 内容 | 重さ |
|---|---|---|
| **【A-GAP-1】** | 命題 A-1(超過 = 深さ 6 のみ)は「正典が深さ 4,5 を保証する」を前提とし、それは (8.8) の $e_{12}$ の**691 進整性**(逐語ノート §3.2 で UNKNOWN)に依存する。整性が崩れると超過は $\{4,6,8\}$ に戻る | 中 |
| **【A-GAP-2】** | 定理 LADDER-SAT (A) は円分指標の全射性(古典)を使う。工房内 pin なし(Lean 化対象外の古典事実として引用) | 小 |
| **【A-GAP-3】** | 定理 A-6 の settled 部分は **LADDER-UNIQ-N** 経由で、そちらは【DIG-GAP-2】(本体)で $\lvert\mathrm{Out}\rvert$ を軌道数から逆算している。$p=5,7$ の独立 $\mathrm{Aut}$ 計算(R0-h)で裏を取ること | 中 |
| **【A-GAP-4】** | 定理 LADDER-SAT (B) の共役計算は $\det=-1$(補題 DET-FORCED)に依存 ⟹ **忠実標準表現以外の作用では成り立たない**(そもそも窓でないが、混同注意) | 小 |
| **【A-GAP-5】** | $E_p$(分裂 Borel 対照)の**算術飽和は未検分**。census 6 窓は測定済だが、飽和の可否は本追補の射程外 | 中 |
| **【A-GAP-6】** | 本追補の全命題は **candidate(単系統・Sol 未監査)**。とくに **LADDER-SAT / A-6 / UNIQUE-FLOOR / A-7 を確定として引用しない**。**「飽和」の発効判定は司令塔専権** | — |

## 4.2 novelty grep(実施済・`docs/` `provenance/` `sol/` 全域)

| 語 | hit |
|---|---|
| `LADDER-SAT` / `UNIQUE-FLOOR` / `SPLIT-TWIN` / `SPLIT-1DIM-DEAD` / `ABEL-F1` | **0**(本追補初出) |
| `命題 A-1`〜`A-7`(本追補の番号) | **0** |
| 「算術飽和」+ 梯子/Heisenberg | **0**(dihedral 族 FAM-U-ASM・NW(7) BH-α-pent のみ既在)⟹ **第 2 の飽和族という位置づけは新規** |
| $C_p\rtimes(C_3\times S_3)$ = 指数 $18p$ 族としての**同定** | **0**(census には個別に載るが「族」としての定式化と $p=691$ への延長は初出) |

## 4.3 次の一手(優先順・司令塔裁定用)

1. ★ **Sol 便への積荷を差し替え/追加**: **定理 LADDER-SAT** を最優先で監査に出す(本体の TWIST-6 / RW-CYC / LADDER-WIN / MIRROR-ODD-B4 に加えて 5 本目)。理由: **算術飽和は地図の軸 (i) に直接領土を足す判定語**であり、発効前に外部監査を通すべき最重要主張。
2. **DIG-R0-1**(§2.7)の発注可否。$p=5,7,13$ は秒、$p=691$ も線形代数のみで分。**全予言が凍結済ゆえ検定力が最大**。
3. **深さ 2 の確認発注**($G_p$、$p=5,7$): $\lvert GT\rvert=p-1$ と $f=\zeta^{k(m)}$ の $k(m)$ の**具体形**を実測(紙では「一意に決まる」までしか出していない — $k(m)$ が $m$ の何次の多項式かは新データ)。
4. **RDV-2 の差分**(§1.3)を追補 D の管轄係へ回付(本追補は D を改変していない)。
5. **$E_{691}$(位数 12,438)の測定**: 分裂 Borel 対照の 691 member。MIRROR-ODD の予言(chiral・witness $[-1,1]$)の**実弾較正**を兼ねる — RDG-6 が死んで空いた較正枠の正しい埋め方。
6. **HR-WIN 予想の再起票**: 定理 LADDER-SAT により**梯子については決着**($\delta(p)=0$ が全 $p$ で成立 = 「$S_3$ 窓は Eisenstein 盲」)。RDV-7(37 vs 41/43)は**測る前に紙で答えが出た** ⟹ 発注不要。残る問いは「**飽和が壊れる最小の窓は何か**」へ移る。

## 4.4 帰属

- 委嘱: 司令塔(裁定 717)。発案: 発案係 `ideas_ribet_dig_v2.md`(RDV-2 の縮約アイデア・RDV-4 の唯一性と対照列アイデア・RDV-5 の 5 点構成)。
- **本追補の新規部分**: 命題 A-1 / 補題 A-2 / $n=2p$ の確定 / 補題 A-3 / **補題 A-4(ABEL-F1)** / **命題 A-5(hexagon 恒等性)** / **定理 A-6** / **定理 LADDER-SAT** / **命題 UNIQUE-FLOOR** / **命題 A-7** / **系 SPLIT-1DIM-DEAD** / **命題 SPLIT-TWIN と census 6 窓の族同定** / RDV-5(iii) の論法欠陥の指摘。
- 既在(吸収・引用): 定理 D-1 / D-2(`aside_..._addendum_d.md`)・定理 C-A・Prop 4.3 / 定理 SG-EXACT・補題 SG-AB・SG-S3 / 定理 MIRROR-ODD・補題 MIRROR-PSL / 補題 FRAT-SPLIT / 定理 SECT-CHIRAL・三層成層 / 本体の LADDER-WIN・LADDER-UNIQ・LADDER-REFL・LADDER-UNIQ-N・DET-FORCED・TWIST-6・CYC-CHAR・RW-CYC。
- 逐語: `docs/week1-定義ノート.md` §2((3.3)(3.4)・(3.53)・(3.60)・charming・settled/isolated・$\chi_{\rm vir}$)。
