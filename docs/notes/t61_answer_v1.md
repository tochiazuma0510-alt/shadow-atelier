# T-61 回答 — 自己訂正 2 件・SEED-EXT A-2 の敗北記帳・★ λ ∈ im D₂ 判定の定式化

**状態札: 数学者起草・司令塔検分前・Sol 未監査**
起草: Claude 数学者 / 2026-08-20 / 委嘱 = 司令塔(Sol T-59 + T-60 反映)
入力: 157ee run 32359956713・receipt SHA `1c3ad7a7…`・producer `B345_JOINT_KERNEL_QSTAR_CLOSED`・checker-v2 独立 PASS。共通宇宙 $K=\ker(F_2\to Q_0\times E_3\times 31\,E_4)$、同一 fixed D2-prefix / target6 qstar。$\Gamma$(位数 243)全 Cayley 関係 6,318 + $x/y$ 作用関係 104 + $Q_0$ 関係 19 の target6 scalar **全ゼロ**、canary 5 一致 ⟹ **exact に $\mu(K)=0$、$\lambda(\text{base target6})=2\ne0$**(fixed-prefix cokernel 上)。
格: paper candidate。機械計算ゼロ。封印非接触。**B4-A / B4-B いずれも非宣言。**

---

## 0. 自己訂正 2 件 — 両方 Sol が正しい

**訂正 1(対象違い)**: 補正語の核は $K=\ker(F_2\to J)$ であって $H_{PB_3}$ の相対 Frattini 商ではない。Nielsen–Schreier で $\dim_{\mathbf F_3}H_1(K;\mathbf F_3)=|J|+1=39{,}680{,}929$、完全 $\mathcal S_2\approx7.87\times10^{14}$ ⟹ **literal 列挙は不可能**。T-58 の「$r\approx26$」「459 列で実行可能性の懸念なし」は根拠なき実行可能性主張。**T-58 §1・§2・§7 を撤回する。**

**訂正 2(157ed 必然論)**: 「順序付き triple-cube の inert は反対称性ゆえ必然」は誤り — triple product は Lie bracket ではない。**T-58 §4 の当該主張を撤回する。**

---

## 1. 敗北の記帳

**SEED-EXT A-2 は共通宇宙 $K$ で棄却された。私の賭けは負けである。**
- **A-2(完全被覆で整合化)= 棄却** ✓ Sol の裁定を受諾。
- **A-1(rank 増)= 生存**。ただし 157ee が示したとおり **rank 増加は qstar 消去を含意しない**(50→54 の 4 方向もすべて $\mu=0$)⟹ **A-1 は生き残っても無価値**である。この含意の非成立は私の予言表になかった。
- **札 6(深さ 3 が本質)も $K$ 内では死亡** — $\mu(K)=0$ は $K$ の**全深度**を覆うので、深さ 3 でも $K$ の中なら届かない。**保留を解いて棄却する。**
- **確定した新事実: 情報は $K$ の外にある。**
- W-P0 型不活性の勝ち。**「不足は深度でなく被覆」という私の診断は、$K$ 内では被覆を完全にしても届かないことが示された以上、$K$ 内では誤りだった。**

---

## 2. ★ 中心 — λ ∈ im $D_2$ 判定の定式化

### 2.1 何が問われているか

$\lambda=2$ は **fixed prefix(362,725 列)に対する cokernel 値**である。従って残る決定的な問いは
$$\boxed{\ \beta\ \in\ \operatorname{im}D_2^{\rm full}\ ?\ }\qquad(\beta=\text{target6 の障害ベクトル})$$
であり、$\lambda\ne0$ はまだ **prefix が $\operatorname{im}D_2$ を張り切っていないだけ**かもしれない。$362{,}725$ は $|R|\cdot|J|$($|J|\approx4.0\times10^{7}$)の **1% 未満**であり、**張り残しの余地は構造的に大きい**。

### 2.2 決定的な構造事実

> **補題 T61-1.** $\operatorname{im}D_2^{\rm full}$ は $\mathbf F_3[J]$-**部分加群**である(全 translate を含むので $J$-作用で閉じる)。一方 $\operatorname{im}D_2^{\rm prefix}$ は単なる $\mathbf F_3$-部分空間にすぎない。
> 従って prefix が各 $J$-軌道の代表を少なくとも 1 本ずつ含むなら
> $$\operatorname{im}D_2^{\rm full}=\mathbf F_3[J]\cdot\operatorname{im}D_2^{\rm prefix},$$
> すなわち **full 判定は「prefix 像を $J$-作用で閉じて membership を再検査する」ことに帰着する**。列を $|R|\cdot|J|$ 本並べ直す必要はない。∎

### 2.3 実行形(推奨・安価)— 余不変量での判定

補題 T61-1 を双対側で使うと、**既に計算済みの prefix cokernel の上の小さな商計算**で済む:

$$\boxed{\ \beta\in\operatorname{im}D_2^{\rm full}\ \iff\ \bar\beta=0\ \text{ in }\ \bigl(\operatorname{coker}D_2^{\rm prefix}\bigr)_{J}\ }$$
$$\bigl(\operatorname{coker}D_2^{\rm prefix}\bigr)_{J}\ :=\ \operatorname{coker}D_2^{\rm prefix}\big/\bigl\langle (g-1)v\ :\ g\in\{x,y\},\ v\in\operatorname{coker}\bigr\rangle$$
(生成元 $x,y$ で割れば十分 — $J$ は $x,y$ で生成されるので $(g-1)$ の全体は $(x-1),(y-1)$ が生成するイデアルで尽きる)。

**双対の言い方(証明書の形)**: $\lambda$ が **full $D_2$ に対する正当な障害証明書**であるためには
$$\lambda\bigl(g\cdot c\bigr)=0\quad\text{for all }g\in J,\ \text{all prefix columns }c$$
が要る。**現行の $\lambda=2$ は prefix 列を消すことしか確認されていない。$J$-translate を消すかは未検査である。これが欠けている唯一の検査である。**
同値に:**$\lambda$ は $J$-余不変量の上の汎函数でなければならない**($\lambda\circ(g-1)=0$)。

### 2.4 157dl 疎装置との接続

157dl の Fox/Shapiro 装置は $\mathbf F_3[E]$ 上の疎行列を扱う設計であり、**$J$-作用による列の生成(orbit closure)はその中で自然に表現される**。従って必要な追加は
1. prefix cokernel の基底(既存)、
2. $(x-1),(y-1)$ の cokernel 上への作用行列(疎・語評価 2 本)、
3. その像で割った商での $\bar\beta$ の判定(小さい線形代数)
の 3 点のみ。**新しい $10^{7}$ 級の疎解は不要**である(補題 T61-1 が列挙を回避する)。

### 2.5 事前登録述語と出目の意味(表)

| receipt 述語 | 出目 | 数学的意味 | 次の一手 |
|---|---|---|---|
| `beta_in_full_im_D2` = **true**($\bar\beta=0$) | **prefix が張り残していただけ** | $\beta\in\operatorname{im}D_2^{\rm full}$ ⟹ **full precision では補正が存在する** = **W-P0 の (α) 枝の full-precision 実現**。base pair はこの段を通る | 通過した補正の provenance を取り、LT-1 (P4)/W-FORM 弱形を FC-40′ で再判定 → 次段へ |
| `beta_in_full_im_D2` = **false**($\bar\beta\ne0$) | **λ は full $D_2$ に対しても正当な証明書** | **この枝(fixed base pair × この D2 系)は当段で真に死亡**。ただし依然 **branch-local** | **T-56 の全称化梯子**へ:(i) base pair の固定解除、(ii) 屋根像 outside の全 $g$(NA-5 なら Sylow 3 生成系)、(iii) 走査宇宙完全性証明書 ⟹ 揃って初めて A 側 |
| `prefix_generates_module` = **false** | prefix が軌道代表を欠く | 補題 T61-1 の前件破れ ⟹ 上の同値が使えない | 欠けた軌道の代表列を追加してから再判定 |
| $\dim$ 検算破れ | — | 実装エラー | 棄却でなく再検 |

**棄却条件(私の側)**: `beta_in_full_im_D2` = false かつ prefix 前件 OK ⟹ **「prefix が張り残していただけ」という私の期待は棄却**され、当段の死亡が確定する(A 側への梯子に乗る)。

---

## 3. 方向 (ii)(universe / roof の変更)— 一段落

T-48 §5 で確立したとおり **NA-1 / NA-2 / NA-5 / OBS-NA は段が chief 段であることを一度も使っていない**(使うのは $K\le H$ が $B_4$-normal 開であることだけ)⟹ **段を大きく取り直す自由(大 jump)は正当**であり、admissible universe や roof を替えても道具一式はそのまま動く。$K$ の外に情報があると確定した以上、**「$K$ を張り替える」= 商 $J$ を取り替えて $K$ を大きくする(= 補正領域を広げる)** のが方向 (ii) の数学的実体である。設計は Sol 側に委ねるが、**取り替え後も $\mu$ の $J$-同変性(§2.3)を最初に確認すること**を条件として付す。

## 4. 9-状態補題 — 降格(短く)

$\Sigma=\{u_i^{\pm3}\}$、9 状態・468$=9\times26\times2$ 遷移が閉じ全出力 0 ⟹ 語長の帰納で $\lambda|_{\langle\Sigma\rangle}\equiv0$(**部分群**であって正規閉包ではない)。**157ee の closure 計算が実質これを包含する**ので定理化の優先度は低い。軽量な除外ツールとしてのみ保持する。

## 5. relation-module 路線 — 「Sol が実質実行済み」の事後検分

**$\mu(K)=0$ を正当化する論理**は次のとおりで、**健全である**:
$K=\ker(F_2\to J)$ に対し $H_1(K;\mathbf F_3)$ は **$\mathbf F_3[J]$-加群として $J$ の関係子の類で生成される**(関係加群・Crowell/Fox 完全列 $0\to H_1(K;\mathbf F_3)\to\mathbf F_3[J]^2\xrightarrow{D_1}\mathbf F_3[J]\to\mathbf F_3\to0$、次元検算 $2|J|-(|J|-1)=|J|+1$ ✓ が Nielsen–Schreier と一致)。従って
$$\mu\equiv0\ \text{on}\ H_1(K;\mathbf F_3)\iff \mu\ \text{が全関係子の全 }J\text{-translate を消す}.$$
Sol の Cayley 関係 6,318 + 作用関係 104 + $Q_0$ 関係 19 は**関係子の完全系**にあたる ⟹ **その全 translate 上でゼロなら $\mu(K)=0$ が従う** ✓。
> **★ 事後検分で唯一残る点(§2.3 と同一の問題)**: 検査が **$J$-translate まで覆ったか**。closure 計算がその名のとおり $J$-軌道閉包であったなら覆っている ✓ ⟹ $\mu(K)=0$ は健全。覆っていない(生成元だけ)なら、$\mu$ の $J$-同変性が別途要る。⟹ **FC-46**。
> **実務上の含意**: **同じ closure 装置が §2 の λ ∈ im $D_2$ 判定にもそのまま使える**。$\mu(K)=0$ の健全性と λ の判定は**同一の同変性問題**であり、一度で両方片付く。

---

## 6. 新規の有限検査

| 番号 | 検査 | 重要度 |
|---|---|---|
| **FC-44** | prefix(362,725 列)が $\operatorname{im}D_2^{\rm full}$ を $\mathbf F_3[J]$-加群として生成するか(各軌道の代表を含むか) | 補題 T61-1 の前件 |
| **FC-45** | **$\bar\beta$ の $J$-余不変量判定**($\operatorname{coker}D_2^{\rm prefix}$ を $(x-1),(y-1)$ の像で割り $\bar\beta=0$ か) | **決定的・最優先** |
| **FC-46** | 157ee の closure が $J$-軌道閉包であったか(生成元のみでないか)⟹ $\mu(K)=0$ の健全性と §2 の同変性を同時に確定 | 高(§5) |
| **FC-40′** | (FC-45 が true の場合)通過補正の $x,y$ 指数和 ⟹ W-FORM 弱形 / LT-1 (P4) の生死 | 中 |

---

## 7. 申告

- 手計算で検証: Nielsen–Schreier $|J|+1$ と $\dim\ker D_1=2|J|-(|J|-1)$ の一致、補題 T61-1($\operatorname{im}D_2^{\rm full}$ が $\mathbf F_3[J]$-部分加群)、余不変量による同値、$362{,}725$ が $|R||J|$ の 1% 未満、$468=9\times26\times2$。
- **撤回**: T-58 §1・§2・§4・§7。**T-58 は本書で置き換えられる。**
- **敗北**: SEED-EXT A-2 棄却、札 6 棄却($K$ 内)。A-1 は生存だが「rank 増 ⟹ qstar 消去」が成り立たないため無価値。
- **UNKNOWN**: FC-44/45/46。$\beta\in\operatorname{im}D_2^{\rm full}$ の真偽。
- 157ee の射程(fixed-prefix × $K$)を超える主張はしていない。**B4-A / B4-B いずれも宣言していない。**
