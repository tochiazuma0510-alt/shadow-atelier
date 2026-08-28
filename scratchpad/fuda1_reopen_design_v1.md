# 札 1 再開設計 v1 — 翻訳ビット測定(LMFDB Belyi 外部入力)

`DIR: proper 側計器 / FRAME: D972 idx3 census × 明示 Belyi(外部入力)`

**委嘱**: 司令塔・裁定 1760。**外部入力の宣言(恒久規則 1750 準拠)**: 本設計の翻訳ビットは **LMFDB Belyi maps database(9T27)**という **census 外部のデータ**から取る。**census 内導出は一切行わない。**
**著者**: 数学者(Opus 5)/ 2026-08-29。**規約 (R-1)(R-2) 準拠。UNKNOWN 一級。**

---

## §0 ★★ 先に結論 — **ゲート 1 は現時点で不成立。scout の代表例は我々の被覆ではない**

`gate: scratchpad/passport_probe_v1.g`
```
PP_BLOCK_ORDER 504  degree 9      PP_TRANSITIVE true  PRIMITIVE true
PP_ORDERS  X=9  Y=9  XY=9  YX=9
PP_PASSPORT_[X,Y,(XY)^-1]  [ [9], [9], [9] ]
PP_LMFDB_REP_SORTED        [ [1,1,7], [1,2,2,2,2], [3,3,3] ]
PP_MATCH_XY  false
PP_RIEMANN_HURWITZ 2g-2 = 6   genus = 4
```

> ### 補題 GENUS-4(初等・証明つき)
> roof 窓の degree-9 ブロックにおいて、マーク済み生成子 $\bar x,\bar y$ は**ともに位数 9**であり、$PSL(2,8)$ の位数 9 元は $\mathbb P^1(\mathbb F_8)$ 上 **9-巡回**である(正則)。したがって $c_0=c_1=1$ で、Riemann–Hurwitz は
> $$2g-2=-2\cdot 9+(9-c_0)+(9-c_1)+(9-c_\infty)=7-c_\infty .$$
> $c_\infty=1$(実測)ゆえ $\boxed{g=4}$。
> **系**: $\bar x,\bar y$ がともに 9-巡回である限り、$g=0$ には $c_\infty=9$(= 恒等)が必要で、推移的三つ組では**不可能**。
> **⟹ 種数 0 の 9T27 Belyi 写像は、いかなるラベル付けでも我々の被覆ではありえない。**

**⟹ scout が引いた代表例 `9T27-7.1.1_2.2.2.2.1_3.3.3-a`(λ=[[7,1,1],[2,2,2,2,1],[3,3,3]]・種数 0)は、我々の対象ではない。**

### 0.1 正しい照会条件(scout への再発注文面)

> **必要なのは: group `9T27`(= $PSL(2,8)$, 次数 9, primitive)・passport $\lambda=[[9],[9],[9]]$(三分岐点すべてが単一 9-巡回)・種数 **4**・定義体 $\mathbb Q$(または $\mathbb Q$ 上の Galois 軌道情報)の Belyi 写像。**
> 種数 0 のエントリは**全て除外してよい**(補題 GENUS-4)。

`gate: scratchpad/passport_probe_v2.g`
```
QQ_CENTRALISER_IN_S9 1        (= 同時共役子は一意)
QQ_NORMALISER_IN_S9 1512  index_over_G 3
QQ_ORDER9_ELEMENTS 168    QQ_TRIPLES_ALL999 9576
QQ_CLASSES_UP_TO_NS9 9        <- passport [9],[9],[9] の類は "ちょうど 9 個"
QQ_CLASSES_UP_TO_G  27
```
⚠ **「9 個」は scout の「9 件」と数が一致するが、代表例の passport は別物**。**一致は偶然の可能性がある** — 9 件の passport を全件取得して確かめること(推測で埋めない)。

---

## §1 全体設計 — **3 成分に分解し、2 つは既存機械で閉じる**

census の鍵は $(m,\delta,\pi)$。**翻訳ビット = $\mathrm{Ih}_M(\mathrm{Frob}_p)$ の行を確定し、NN-09/NN-12 のどちらかを読む**こと。

| 成分 | 正体 | 供給源 | 状態 |
|---|---|---|---|
| $m$ | 円分指標 $\chi(\mathrm{Frob}_p)=2m+1\equiv p$ | 初等 | **確定・較正ゲートに使う** |
| $\delta$ | $f_\sigma$ の **degree-27 ブロック**の $D_9$ 座標(実測で $e_i=0$ ⟹ $C_9$ 値) | **Kummer / $u_{\rm dih}$**(既存 S1–S9 機械) | **要 mod 9** ⟹ §5 の符号警告が効く |
| $\pi$ | $f_\sigma$ の **degree-9 ブロック**($PSL(2,8)$) | ★ **LMFDB Belyi(本件の外部入力)** | ゲート 1 待ち |

**⟹ LMFDB が供給するのは π 半分だけ**である。δ 半分は二面体 Kummer 側で閉じる。**この分担を明示することが本設計の骨格。**

⚠ **なぜ Belyi 写像で $\pi(\mathrm{Frob}_p)$ が取れるのか(機構)**: $PB_3=F_2\times Z$、$F_2=\langle x,y\rangle=\pi_1(\mathbb P^1\setminus\{0,1,\infty\})$。roof の degree-9 ブロックは $F_2\twoheadrightarrow PSL(2,8)$ という**モノドロミー表現そのもの**であり、対応する被覆の**ファイバー上の Galois 作用**が $\mathrm{Frob}_p$ の 9 点置換を与える。GT の作用則 $x\mapsto x^{\chi}$, $y\mapsto f_\sigma^{-1}y^{\chi}f_\sigma$ から、この置換の情報が $f_\sigma$ の当該ブロック像を決める。

---

## §2 手順 1 — passport 突合(implementer 粒度)

### 2.1 ★ 規約の事前固定(新たな CV-9 発生源・宣言欄必須)

**我々の側**: $x:=x_{12}$(0 のまわりのループ)、$y:=x_{23}$(1 のまわり)、$z:=(xy)^{-1}$(∞ のまわり)、$xyz=1$。実装では `DCP2X4`, `DCP2Y4`。
**Belyi 側**: $(\sigma_0,\sigma_1,\sigma_\infty)$、$\sigma_0\sigma_1\sigma_\infty=1$。

> ### ⚠⚠ 決定的注意 — **cycle type では順序が決まらない**
> 我々の passport は $[[9],[9],[9]]$ で**三成分すべて同型**。したがって「どれが $\sigma_0$ か」は **cycle type から一切決まらない**。
> **⟹ 割当は同時共役検定でのみ決める。** 6 通りの順序 × 逆元の有無を**全数試す**こと(下記 2.2)。**「自然な対応」を仮定するのは禁止。**

**cert 必須欄**:
```
belyi_triple_convention : "sigma0_sigma1_sigmainf, product = 1"
our_marking             : "x=X4 (loop at 0), y=Y4 (loop at 1), z=(xy)^{-1}"
assignment_tested       : 全 6 順序 × {直, 逆} の 12 通りを列挙し、成功/失敗を全て記録
assignment_selected     : 成功したもの(複数なら §4 の曖昧性として計上)
external_input          : "LMFDB Belyi maps DB, 9T27, passport 9.9.9, genus 4"   ← 恒久規則 1750
```

### 2.2 実行

```gap
# LMFDB から取得した各エントリ e の triples_cyc から (s0,s1,sinf) を PermList で構成
for e in entries do
  for asg in [[1,2],[2,1],[1,3],[3,1],[2,3],[3,2]] do        # (sigma_a, sigma_b) -> (x,y)
    for inv in [false,true] do
      a := e.trip[asg[1]];; b := e.trip[asg[2]];;
      if inv then a := a^-1;; b := b^-1;; fi;
      c := RepresentativeAction(SymmetricGroup(9), [a,b], [DCP2X4,DCP2Y4], OnPairs);;
      if c <> fail then  Add(hits, rec(entry:=e.label, asg:=asg, inv:=inv, conj:=c));  fi;
    od;
  od;
od;
```
**期待**: `QQ_CLASSES_UP_TO_NS9 = 9` ゆえ、passport $[9,9,9]$ のエントリのうち**ちょうど 1 つ**が当たる(順序割当まで込みで複数当たる可能性は §4 で計上)。
**破壊対照**: わざと passport の違うエントリ(種数 0 のもの)を入れる ⟹ **必ず `fail`**。返ってきたら実装バグ。

---

## §3 手順 2 — Frobenius のマーク付き測定

### 3.1 何を測るか

一致したエントリの明示 Belyi 写像 $\phi:C\to\mathbb P^1$(**種数 4 ゆえ $C\ne\mathbb P^1$** — 平面モデル+写像の形で LMFDB が与える)について:

1. **基点の選択**: 分岐点($0,1,\infty$)の外の**有理点** $t_0\in\mathbb P^1(\mathbb Q)$ を 1 つ固定(例: $t_0=2$ または $t_0=1/2$)。**cert に $t_0$ を宣言。**
2. **ファイバー**: $\phi^{-1}(t_0)$ は $\mathbb Q$ 上次数 9 の**エタール代数** $A_{t_0}=\mathbb Q[T]/(F_{t_0}(T))$($F_{t_0}$ は $\phi$ の方程式から消去で得る 9 次多項式)。
3. **良い素数**: $p\nmid$ (disc$(F_{t_0})$ · $\phi$ の係数分母 · 3 · 7 · 2)。
4. **$\mathrm{Frob}_p$ の置換**: $F_{t_0}$ の $\mathbb F_p$ 上の根/因子から、9 根への Frobenius 作用を**根の順序を固定して**読む(下記 3.2)。

### 3.2 ★ マーク(ここが本質・「分解型」では足りない)

**警告(既確定)**: $\Psi$ は $PSL(2,8)$ の**類関数ではない**(`psi_classfn_probe_v1.g`: 位数 3 の 4 元が共役なのに $\Psi=[2,1,2,1]$)。**⟹ Dedekind の分解型(= 共役類)だけでは $\pi$ が決まらない。**

**⟹ 根に絶対的な番号を付ける手順が必須**:
```
M-1  t_0 の上のファイバーの 9 根を、あるモノドロミー基点でのラベル 1..9 に対応させる。
     この対応は「被覆の点 ↔ モノドロミー表現の添字」の同一視であり、
     LMFDB エントリの triples_cyc のラベル付けと同じものでなければならない。
M-2  実務的な実装: p 進で根を分離し(Hensel)、生成元 sigma_0, sigma_1 の作用を
     t_0 から 0 および 1 のまわりの経路に沿った解析接続として p 進で追跡する
     — あるいは LMFDB エントリが「ラベル付きファイバー」を同梱していれば直接使う。
M-3  Frob_p は根の集合の置換として得られ、M-1 の番号で 1..9 の置換に翻訳される。
```
> ⚠⚠ **UNKNOWN(一級)**: **M-1/M-2 が本工房で実行可能かは未確認。** 「p 進解析接続でモノドロミーのラベルを追跡する」は標準的だが**工房に機械がない**。LMFDB が **ラベル付きファイバーまたは分岐点上のラベル対応**を同梱していない場合、ここが第 2 のブロッカーになる。**scout への照会項目に含めること。**

### 3.3 較正必達(手順 2 単独で回る)

| # | 検査 | 期待 |
|---|---|---|
| **C-1** | $\mathrm{Frob}_p$ の**分解型**が $PSL(2,8)$ の元の cycle type($\{1^9,1\cdot2^4,3^3,1^2\cdot7,9\}$)のどれかに一致 | 必ず一致 |
| **C-2** | 幾何モノドロミー群 = $PSL(2,8)$、算術モノドロミー群 $\subseteq P\Gamma L(2,8)$ | 分解型の分布で確認 |
| **C-3** | 複数素数($\ge 5$ 本)で **Chebotarev 分布**が $|PSL|$ または $|P\Gamma L|$ の類分布に整合 | 統計 |

---

## §4 手順 3 — 比較写像と曖昧性の全数把握

### 4.1 同一視

手順 1 の同時共役子 $c\in S_9$($[\sigma_a,\sigma_b]^c=[X_4,Y_4]$)で、測った $\mathrm{Frob}_p$ 置換を $\rho:=\mathrm{Frob}_p^{\,c}$ に移送する。

### 4.2 ★ 曖昧性の群 — **零ビット(機械確定)**

`QQ_CENTRALISER_IN_S9 1` ⟹ $C_{S_9}(\langle X_4,Y_4\rangle)=1$。
> **⟹ マーク付き対 $(\sigma_a,\sigma_b)\mapsto(X_4,Y_4)$ を満たす共役子は一意。同一視に残る曖昧性は 0 ビット。**

**ただし残る曖昧性は 2 箇所**(いずれも §2.1 の割当で計上):
1. **順序/逆元の割当**(12 通り)のうち成功が複数なら、その個数分のビットが残る ⟹ **実測して cert に書く**(現時点 UNKNOWN)。
2. **算術 vs 幾何**: $\mathrm{Frob}_p$ が $P\Gamma L\setminus PSL$ に落ちる場合、$\rho\notin PSL(2,8)$ となり **census の π 値ではありえない**(PG-1: census の π は構成上 $PSL$ 内)。⟹ **その素数は使えない**。⟹ **使える素数の条件: $\rho\in PSL(2,8)$**。これは $\psi_p$(= $P\Gamma L/PSL$ コセット)$=0$ を意味する。
   ⚠ **既測の $\psi_p=2\ne0$($p=19,37,73$)と衝突する** ⟹ **これら 3 素数は使えない可能性が高い**。**別の素数(コセット 0 のもの)を選ぶ必要がある** — §6 の risk 参照。

### 4.3 翻訳ビットの読み出し

$\rho$ = census 座標での $\pi(\mathrm{Frob}_p)$ ⟹ 27 元テーブル `pi_psi_table.g` で $\Psi(\mathrm{Frob}_p)$ を引く。
δ 側から $\mathcal K_3(\mathrm{Frob}_p)$、$m$ から行を絞り、**$(m,\delta,\pi)$ の 3 成分がそろえば census の行が一意に決まる**(972 行は鍵で相異なる)⟹ **NN-09 / NN-12 のどちらかを読む = 翻訳ビット**。

---

## §5 較正・破壊対照・符号の射程

### 5.1 較正

| # | 量 | 期待値 | 独立性 |
|---|---|---|---|
| **K-1** | $m(\mathrm{Frob}_p)$ | $2m+1\equiv p\ (\mathrm{mod}\ 18)$ ⟹ $m=(p-1)/2 \bmod 9$ | **完全独立**(円分指標のみ)。**最初に回すゲート** |
| **K-2** | 得られた $(m,\delta,\pi)$ が 972 行の**いずれかに実在** | 実在すること | 実在しなければどこかが誤り ⟹ **即停止** |
| **K-3** | ORIENT との交差検算: $\Psi(\rho)$ と $\mathcal K_3$ の関係が $\pm1$ 倍 | $c'=\pm1$ のどちらか | $c'=+1$(既測・3 素数)と**一致すべき** |
| **K-4** | 複数素数で同一の翻訳ビット | 全素数で一致 | 不一致なら設計破綻 |

### 5.2 破壊対照(mutant)

| # | 変異 | 期待 |
|---|---|---|
| **MU-A** | passport を故意に取り違える(種数 0 エントリを使う) | `RepresentativeAction` が **`fail`** ⟹ 手順 1 で停止 |
| **MU-B** | $(\sigma_0,\sigma_1)$ の割当を入替える | **翻訳ビットが変わる**(変わらなければ検定に判別力がない = 設計欠陥) |
| **MU-C** | 同時共役子を別の $S_9$ 元に差し替える | $\rho$ が変わり K-2 が落ちる |
| **MU-D** | 基点 $t_0$ を別の有理点に変える | **翻訳ビットは変わらない**べき(変わったらマークが壊れている) |

### 5.3 ★ SIGN-VAC の射程警告(委嘱 5)

> **補題 SIGN-VAC**(`fuda1_select_closure_v1.md` §1.2): $p$ 奇・$p\equiv1\ (3)$ なら $(p-1)/3$ は常に偶 ⟹ $u_{\rm dih}=\pm2^{-7}$ の符号は **mod 3 Kummer に効かない**。
> **⚠ 本設計では効かない**: δ 成分は $D_9$ 座標 = **$C_9$ 値**であり、**mod 9 の Kummer** が要る。$(p-1)/9$ の偶奇は一定でない ⟹ **$u_{\rm dih}$ の符号が再び論点**。
> **⟹ δ を測る段では $\pm2^{-7}$ の符号を先に確定させること**(cert 必須欄 `u_dih_sign` と、その確定根拠)。**現時点 UNKNOWN。**

### 5.4 外部入力の宣言(恒久規則 1750)

```
external_input_declaration:
  source   : LMFDB Belyi maps database, group 9T27, passport [9],[9],[9], genus 4
  papers   : papers/mssv-1805.07751-belyi-map-database.pdf (0b82da494c561b30)
             papers/kmsv-1311.2081-numerical-belyi-maps.pdf (4b253e737b38b724)
  claim    : 本設計の翻訳ビットは census 内導出ではない。census からは
             27 元テーブル(pi_psi_table.g)と roster のみを読み、向きは
             外部の Belyi データ + 円分指標 + Kummer から得る。
```

---

## §6 リスク(過去 3 回の死に方に照らして)

| # | リスク | 深刻度 | 早期判定 |
|---|---|---|---|
| **R-1** | LMFDB に **passport $[9,9,9]$ 種数 4** のエントリが**無い** | **致命** | **scout 照会 1 便で判明**。9 件の passport 全件取得 |
| **R-2** | エントリはあるが**ラベル付きファイバー**が無く §3.2 の M-1/M-2 が実行不能 | **高** | scout 照会に同梱項目として含める |
| **R-3** | $\mathrm{Frob}_p$ が $P\Gamma L\setminus PSL$ に落ちる素数しか使えない(§4.2(2))⟹ **census の π 値と型が合わない** | **高** | 素数を 1 本測れば判明。**コセット 0 の素数を探す必要** |
| **R-4** | δ 側の $u_{\rm dih}$ 符号(§5.3)が未確定 | 中 | 独立に解決可能 |
| **R-5** | 種数 4 の明示写像は係数が巨大で、消去に失敗 | 中 | 実際のデータを見るまで不明 |

> **過去 3 回の共通死因は「census 内部から向きを読もうとした」**。本設計はそれを犯していない(向きは全て外部)。**ただし R-1/R-2/R-3 は新しい死因**であり、いずれも **1 便で判定可能**。**重い実装に入る前に R-1→R-3 の順で潰すこと。**

---

## §7 実行順(推奨)

```
STEP 0  (scout, 1 便)  9T27 の 9 件の passport 全件 + 種数 + ラベル付きファイバーの有無
        ⟹ R-1/R-2 判定。passport [9,9,9]/genus 4 が無ければ ここで終了(一級の否定)。
STEP 1  (implementer, 0.5 便)  §2.2 の同時共役突合(12 割当全数)+ MU-A
        ⟹ 一意のエントリと共役子 c を確定。曖昧性ビット数を cert に記録。
STEP 2  (implementer, 1 便)  §3 の Frobenius 測定を 1 素数で。K-1 を先に通す。
        ⟹ R-3 判定(rho in PSL か)。
STEP 3  (implementer, 1 便)  δ 側(Kummer mod 9)+ §5.3 の符号確定。
STEP 4  (数学者+司令塔)  K-2/K-3/K-4 と MU-B/MU-D ⟹ 翻訳ビット確定。
```

---

## §8 UNKNOWN(一級・申告)

1. **LMFDB の 9 件の passport**(scout 報告書の詳細を読んでいない)— §0.1 の条件を満たすものがあるか **未確認**。
2. **§3.2 の M-1/M-2**(ラベル付きファイバーの取得)が工房内で実行可能か **未確認**。
3. **$u_{\rm dih}$ の符号**(mod 9 で必要)**未確定**。
4. **$\mathrm{Frob}_p$ が $PSL$ に落ちる素数の存在と探し方** — §4.2(2) の型整合。既測 $\psi_p=2$ の 3 素数は**使えない可能性**。
5. **種数 4 の被覆で「ファイバー = 9 次エタール代数」を実際に書き下せるか** — LMFDB のデータ形式次第。

---

**完**(札 1 再開設計 v1)
