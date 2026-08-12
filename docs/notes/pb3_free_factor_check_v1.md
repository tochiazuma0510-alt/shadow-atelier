# $PB_3=F_2\times\langle c\rangle$ の自由因子確認 1 枚 — Sol 警告への正面回答(裁定 1090)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔(実装係 C の express 札・AT-2 P2 用)
正典 = `照合_B3表示_T2土台.md` §1–§2(2401 p.4 画像照合済)・定義ノート §2
⚠ **格: candidate**。$u$/$c$ 非接触・封印非接触。

---

## §0 三行

1. ★ **$PB_3=F_2\times\langle c\rangle$($F_2=\langle x,y\rangle=\langle\sigma_1^2,\sigma_2^2\rangle$)は正典の事実**(2401 §1.1 地の文)。⚠ ただし**原著 [17] 未照合**(`照合_B3表示` §5 の UNKNOWN 項)⟹ **引用格**。
2. ⚠ **Sol の警告は正しい**: この直積は **$PB_3/N$ に降りません**。しかも $F_2$ は $B_3$ で**正規でも特性的でもありません**。
3. ★ **しかし P2 の構成に直積は一切要りません**。$M=N\cap K_2$ は 2 本の全射の**核**として作れます(§4・3 行)⟹ **PARTIAL は解除できる見込み**。

---

## §1 正典で言えること・言えないこと

| 主張 | 格 | 根拠 |
|---|---|---|
| $Z(B_3)=Z(PB_3)=\langle c\rangle\cong\mathbf Z$ | 正典(地の文) | 2401 §1.1 p.4(`照合_B3表示` §1・画像照合済) |
| $PB_3\cong F_2\times\langle c\rangle$ | 正典(地の文・**原著未照合**) | 同上。原著 [17] Kassel–Turaev §1.3 は未照合 |
| $x:=x_{12}=\sigma_1^2$, $y:=x_{23}=\sigma_2^2$ が $F_2$ の自由基底 | 正典(規約) | 2401 §1.1 p.4 の定義表示 |
| $c=\Delta^2=\delta^3$ | 導出値(照合済) | `照合_B3表示` §3 (D2)(braid 関係 1 回) |

⟹ **「$x,y$ が中心と無混線の自由因子か」への答え: $PB_3$ の中では YES(正典)。** $F_2\cap\langle c\rangle=1$ かつ $F_2\langle c\rangle=PB_3$。

---

## §2 ⚠ しかし 3 つの「効かない」

### 2.1 $F_2$ は $B_3$ で**正規でない**

正典 (1.11)(画像照合済)より
$$\sigma_1x_{23}\sigma_1^{-1}=x_{23}^{-1}x_{12}^{-1}\,\boxed{c}$$
右辺に $c$ が現れる ⟹ $\sigma_1F_2\sigma_1^{-1}\not\subseteq F_2$。⟹ **braid 共役は $F_2$ を保ちません**(保つのは $F_2\langle c\rangle=PB_3$ だけ)。
★ これは定義ノート §2 の既記の注意「$\theta/\tau$ を商 $F_2/N_{F_2}$ 上で評価する近道は $c\in N$ に依存する」と**同一の現象**です。

### 2.2 $F_2$ は $PB_3$ で**特性的でない**

$PB_3=F_2\times\langle c\rangle$ の補元は一意ではありません: 任意の準同型 $\varphi:F_2\to\langle c\rangle$ に対し $\{w\varphi(w):w\in F_2\}$ も補元。
⟹ **「$x,y$ を自由因子に取る」は規約(正典の選択)であって標準ではありません。** 正典がこの選択を固定しているので実装上は確定ですが、**「自然に定まる」と書いてはいけません**。

### 2.3 ★★ 直積は商に降りない(Sol 警告の正体)

$N_{F_2}:=N\cap F_2$、$N_c:=N\cap\langle c\rangle=\langle c^{z}\rangle$($z=\mathrm{ord}(\bar c)$)とおく。自然な写像
$$\mu:\ \bigl(F_2/N_{F_2}\bigr)\times\bigl(\langle c\rangle/N_c\bigr)\ \longrightarrow\ PB_3/N$$
は**全射だが一般に単射でない**。核は $N\big/\bigl(N_{F_2}\cdot N_c\bigr)$ — すなわち **$N$ が $wc^j$ 型の「混線元」($w\notin N_{F_2}$, $c^j\notin N_c$)を含むぶん**です。
$$\boxed{\ N=N_{F_2}\cdot N_c\ \textbf{(無混線)のときに限り }PB_3/N\cong(F_2/N_{F_2})\times(\langle c\rangle/N_c)\ }$$
⟹ **$PB_3/N$ を安易に直積分解してはいけない、という Sol の警告は正しい。**

---

## §3 ★ 無条件に成り立つもの(実装が使ってよい 3 つ)

$Q:=F_2N/N$ とおく。

| # | 事実 | 理由 |
|---|---|---|
| **(a)** | $\boxed{Q\cong F_2/N_{F_2}}$ | ★ **第 2 同型定理のみ**($F_2N/N\cong F_2/(F_2\cap N)$)— **直積分解を使いません** |
| **(b)** | $Q\trianglelefteq PN:=PB_3/N$ | $F_2\trianglelefteq PB_3$(直積因子)⟹ $F_2N\trianglelefteq PB_3$ |
| **(c)** | $\boxed{[PN:Q]=z_0:=[\,\mathbf Z:\pi_c(N)\,]}$、$\pi_c:PB_3\twoheadrightarrow\langle c\rangle$ は $F_2$ に沿った射影 | $[PB_3:F_2N]=[\langle c\rangle:\pi_c(N)]$ |

### 3.1 ⚠ 私の検分 §6.1 の訂正

`set_surgery_vetting_v1.md` §6.1 で私は **$[PN:Q]=\mathrm{ord}(\bar c)$** と書きました。**誤りです**。正しくは
$$\boxed{\ [PN:Q]=z_0\ \Bigm|\ z=\mathrm{ord}(\bar c),\qquad z_0=z\iff N\ \text{が無混線}\ }$$
$N_c=\langle c^z\rangle\subseteq\pi_c(N)=\langle c^{z_0}\rangle$ ゆえ $z_0\mid z$。**混線があると $z_0<z$ になり、極端には $z_0=1$(= $Q=PN$)もあり得ます。**
⟹ **実装は $z_0=[PN:Q]$ を仮定せず測ること**(GAP 1 行: `Index(PN, Q)`)。[1008,521] は $z=2$ なので $|Q|\in\{84,168\}$ の**どちらか** — 実測で決めてください。
⟹ 検算 B′ spec(`iset4_remeasure_spec_v1.md` §2.1・[B′-0])も同様に読み替えてください(spec 本体の測定手順は $[PN:Q]$ を**測る**設計なので**変更不要**)。

### 3.2 ⚠ もう 1 つの注意

**$Q\trianglelefteq B_3/N$ は一般に成り立ちません**($F_2$ が $B_3$ で正規でないため・§2.1)。成り立つのは $c\in F_2N$、すなわち $z_0=1$ のとき。
⟹ $Q$ を「$B_3/N$ の正規部分群」として扱うコードがあれば**要修正**。$N'$ は $c\in N'$ ⟹ $z=z_0=1$ ⟹ $Q=PN$ で問題なし ✔ 83 窓は要注意 ⚠

---

## §4 ★ $M=N\cap K_2$ の正しい構成(3 行・分解を一切使わない)

$K_2=\ker T_{m,f}$(fixture の第 2 核類)。$\pi_N:B_3\twoheadrightarrow B_3/N$ と $T_{m,f}:B_3\twoheadrightarrow B_3/N$ の**対**を取ります:

```
(1) rho := g |-> ( pi_N(g), T_{m,f}(g) )   :  B_3 --> (B_3/N) x (B_3/N)
(2) M := ker rho = N ∩ K_2 ,  B_3/M ≅ Im(rho)  (subdirect product)
(3) 実装: 2 本の epi を GroupHomomorphismByImages で σ_1,σ_2 の像から作り、
    直積への対角写像の Image を取る。|Im rho| を *先に測る*(上界ではなく実値)。
```

- ★ **なぜ正しいか**: $\ker\rho=\ker\pi_N\cap\ker T_{m,f}=N\cap K_2$ ✔ 定義そのものです。$PB_3$ の分解も $F_2$ の正規性も使いません。
- ★ **規模**: $\lvert B_3/M\rvert\le1008^2=1{,}016{,}064$、$\lvert PB_3/M\rvert\le168^2=28{,}224$ は**上界**です。$N$ と $K_2$ は同一成分の対象で $B_3/N\cong B_3/K_2$ ゆえ、**実値はずっと小さいのが普通**(subdirect product は fiber product になり、共通商のぶん縮む)。⟹ **測ってから諦めること**。
- ★ **isolated 検算**: $M=N^\diamond$ は Prop 3.14 で isolated のはず ⟹ $GT(M)$ の全 shadow が settled を実測(= 検分第 I 部 系 C の回帰テスト)。
- ⚠ **$c$ の扱い**: [1008,521] は $c\notin N$ ⟹ $c\notin M$。$T_{m,f}(c)=c^{u}N$ なので $K_2\ni c^j\iff c^{ju}\in N$、$\gcd(u,z)=1$ ⟹ $K_2\cap\langle c\rangle=N\cap\langle c\rangle$ ⟹ **$M\cap\langle c\rangle=\langle c^z\rangle$ も不変** ✔(規模の見積りに使えます)。

---

## §5 P2 再開判断への一言

$$\boxed{\ \textbf{再開可}\ —\ \S4\ \textbf{の構成に直積分解は不要。PARTIAL の原因は「作り方が無い」ではなく「作り方が誤っていた」}\ }$$
**先に測るべき 1 つ**: $\lvert\mathrm{Im}\,\rho\rvert$(= $\lvert B_3/M\rvert$)。これが GAP の射程内なら P2 は完走できます。射程外なら**そこで正直に PARTIAL** ⟹ その場合でも「中間サイズが 1 個でも出れば SUBTOR が死ぬ」という**反証側は無傷**(部分サンプリングで足りる)。

## §6 記帳

- ★ **本書の新規部分**: ① $F_2$ が $B_3$ で非正規・$PB_3$ で非特性的であることの明示((1.11) の $c$ 因子)② 直積が商に降りない条件の同定($N=N_{F_2}N_c$)③ **$[PN:Q]=z_0\mid\mathrm{ord}(\bar c)$** への訂正(検分 §6.1 の誤り)④ $Q\trianglelefteq B_3/N$ が一般に偽であることの摘出 ⑤ $M$ の分解フリーな構成。
- ⚠ **自己捕獲(暫定札 m1090-1)**: `set_surgery_vetting_v1.md` §6.1 の「$[PN:Q]=\mathrm{ord}(\bar c)$」は誤り。正しくは $z_0\mid\mathrm{ord}(\bar c)$。⟹ 上書きせず本書で訂正。
- **【PB3-GAP-1】(小・新)** $PB_3\cong F_2\times\langle c\rangle$ の原著([17] Kassel–Turaev §1.3)照合は未実施(`照合_B3表示` §5 から継続)。⟹ 引用格のまま。**文献要請の必要はありません**(古典的事実・正典の地の文で足りる)。
- **申告**: 紙のみ(機械走行ゼロ)・$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
