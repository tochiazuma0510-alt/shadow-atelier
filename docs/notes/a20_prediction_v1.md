# W-D-A20-15a の凍結予言(prediction-first)**v1**

**状態札: candidate(裁定前・未 commit・未凍結)**
起草: Claude(数学者レイヤー・Opus 5)/ 2026-07-29
設問: 司令塔委嘱(裁定 195-2)。**凍結は司令塔が commit で行う** — 本稿は起草のみ。

> ## 接触の申告(prediction-first の生命線)
> **本稿執筆時点で、私は `W-D-A20-15a` の測定値を一切見ていない。** 私が見た数値は
> (a) `search/certs/wall_miner_v5_20260729.json` の 66 行(すべて `W-A-B3idx*` 系)、
> (b) `search/certs/a16_kernel_structure_20260729.json`(A16 = $N_{\rm ord}=11$)、
> (c) atlas の 25 窓(`kerchi_equality_v2.md` §6)
> のみである。**A20-15a については「$N_{\rm ord}=15=3\cdot5$」という委嘱文中の 1 パラメータしか知らない。**
> ⚠ **司令塔への手続き要請**: 本稿を凍結する前に、**A20-15a の $|GTSh|$・$|\ker\widetilde\chi|$ 等が既にどこかで測定・記録されていないこと**を確認してください。既測なら prediction-first は成立せず、本稿は「後付けの整合説明」に格下げされます(私は探しに行きません — 探すこと自体が汚染です)。

> ## 封印遵守
> **$u$・封印 3 量に一切触れていない。** 本稿は有限群論と初等整数論のみ。

---

## 1. 予言の土台(既に証明済み/観測済みのもの)

### 1.1 無条件の定理(T-A/T-B/命題 ABS — `kerchi_equality_v2.md`)

* **(T-A5)** $|\ker\widetilde\chi|\cdot|Q|=|GTSh(N,N)|$、$Q:=\operatorname{Im}\widetilde\chi\le(\mathbf Z/2N_{\rm ord})^\times$。**無条件**。
* **(T-B)** $\ker\widetilde\chi/[G,G]\cong\operatorname{coker}\bigl(\Lambda^2Q\xrightarrow{\rm tg}(K^{\rm ab})_Q\bigr)$、$K:=\ker\widetilde\chi$。**無条件**。
* **(ABS)** $[K,K]\subseteq[G,G]$ ゆえ等号問題は $K^{\rm ab}$ 上でしか起きない。**無条件**。

### 1.2 $N_{\rm ord}=15$ の算術(本稿の要・**計算するだけ**)

$$2N_{\rm ord}=30,\qquad (\mathbf Z/30)^\times\cong(\mathbf Z/3)^\times\times(\mathbf Z/5)^\times\cong C_2\times C_4,\qquad \varphi(30)=8 .$$

$$\boxed{\ (\mathbf Z/30)^\times\ \text{は}\ \textbf{非巡回}\ (C_2\times C_4)\ \Longrightarrow\ \Lambda^2\bigl((\mathbf Z/30)^\times\bigr)\cong C_2\ne0\ }$$

これが A20-15a を **既存 3 標本のどれとも違う実験にする**理由である:

| 標本 | $N_{\rm ord}$ | $Q$(全射時) | $\Lambda^2Q$ | 機構 |
|---|---|---|---|---|
| $L$ | 6 | $C_2^2$ | $C_2$ | B3(位数互いに素で逃げ切り) |
| `idx162-s1` | 3 | $C_2$ | $0$ | B2 |
| A16 | 11 | $C_{10}$ | $0$ | B2(非可換核) |
| **A20-15a** | **15** | **$C_2\times C_4$** | **$C_2$** | **B2 は発火不能** ← 未踏 |

**⟹ 全射なら B2 型は原理的に使えない。** A20-15a は「**transgression が実在する場で余不変量が生き残れるか**」を問う、初の非 dihedral 実験である($K^{(2^\alpha)}$ 系では transgression が実際に働いて等号を保っていた — §4 註)。

### 1.3 パターン観察(2 標本・**証明ではない**)

* `idx162-s1`: $N_{\rm ord}=3$、$\ker\widetilde\chi\cong C_3=C_{N_{\rm ord}}$。
* A16: $N_{\rm ord}=11$、$\ker\widetilde\chi\cong C_{11}\times D_8=C_{N_{\rm ord}}\times(2\text{-群})$。
* **P81-B**: 「$R_\tau$ が $N_{\rm ord}$ 外の奇素数を殺す」。
* A16 の**部分生存**(v2.4 §13.3): $C_{N_{\rm ord}}$ 層は $[G,G]$ に死に、**2-部分が生き残った**。

---

## 2. 予言(凍結対象)— 4 段の committed 予言 + 1 条件付き

> ### 予言 A20-P1(核の奇部分の支持)
> $$\boxed{\ |\ker\widetilde\chi|\ \text{の奇部分は}\ \{3,5\}\text{-数である}\ }$$
> すなわち奇素数 $p\mid|\ker\widetilde\chi|$ なら $p\in\{3,5\}$($p\mid N_{\rm ord}=15$)。
> **外れたときの価値**: **P81-B($R_\tau$ が $N_{\rm ord}$ 外の奇素数を殺す)の反証。** $7,11,13,\dots$ のいずれかが核に現れれば、$R_\tau$ 所見は偽か、少なくとも $N_{\rm ord}$ 合成の場合に効かない。**一級。**

> ### 予言 A20-P2(核の奇部分の実体)
> $$\boxed{\ C_{15}\le\ker\widetilde\chi,\ \text{すなわち}\ 15\mid|\ker\widetilde\chi|\ \text{かつ奇部分は}\ C_{15}\ (\cong C_3\times C_5)\ }$$
> **外れ方は 2 通りあり、どちらも情報**: (i) $15\nmid|\ker|$(例: 3 だけ・5 だけ)⟹ **$N_{\rm ord}$ の素因子が核へ「全部」持ち上がるわけではない**という初の反例で、$N_{\rm ord}$ 合成の窓に固有の現象。(ii) 奇部分が $C_3\times C_5$ でなく $C_9,C_{25}$ 等 ⟹ 核の奇部分は $C_{N_{\rm ord}}$ でなく $N_{\rm ord}$ の**冪**まで太りうる。

> ### 予言 A20-P3(核の形)
> $$\boxed{\ \ker\widetilde\chi\ \cong\ C_{15}\times S,\quad S\ \text{は}\ 2\text{-群}\ }$$
> (奇部分は直積因子として分離し、非可換性があるとすれば $S$ の中だけ。A16 の $C_{11}\times D_8$ の形の反復。$S=1$ も許す。)
> **外れたときの価値**: 奇部分が直積因子でない(2-群が奇部分に非自明に作用する)なら、**$\ker\widetilde\chi$ の構造は半直積まで太る**ことになり、A16 の `complement_action_exponents = [1,1,1]`(自明作用)が偶然だったと分かる。**核の構造定理の形が変わる。**

> ### 予言 A20-P4(**最も鋭い**・生存層の非対称)
> $$\boxed{\ \ker\widetilde\chi/[G,G]\ \text{は}\ \mathbf{2}\text{-群}\ (\text{奇部分は}\ [G,G]\ \text{に吸収される})\ }$$
> 根拠: $Q\to\operatorname{Aut}(C_3)\times\operatorname{Aut}(C_5)$ が非自明であれば $(C_{15})_Q$ の対応成分が消える。$Q\le(\mathbf Z/30)^\times$ は $u\bmod3$、$u\bmod5$ を**両方**動かせる(全射なら全単射)ので、**奇部分は完全に死ぬ**はず。A16 の部分生存の反復。
> **外れたときの価値**: $\ker/[G,G]$ に $3$ または $5$ が現れれば、**$Q$ の奇部分への作用が(全射にもかかわらず)自明**ということで、$G$ の拡大構造が予想外($G$ が奇部分上で可換に割れている)。**idx162 型($G$ 可換ゆえ作用自明)が $N_{\rm ord}$ 合成でも起きることの witness。**

> ### 予言 A20-P5(条件付き・機構の帰属)
> **$\widetilde\chi$ が全射($|Q|=8$)ならば**:
> $$\boxed{\ \Lambda^2Q\cong C_2\ne0\ \Longrightarrow\ \text{破れても「B2 型」とは呼べない}\ }$$
> であり、判定は $\mathrm{tg}:\ C_2\to(K^{\rm ab})_Q$ の像を実際に見るしかない。**予測**:
> * $(K^{\rm ab})_Q\cong C_2^2$(A16 と同型の 2-部分)なら $|\operatorname{im}\mathrm{tg}|\le2$ ゆえ $\operatorname{coker}\ne0$ ⟹ **等号は破れる**($L$ と同じ「transgression が届かない」型 = **B3 型の一般化**)。
> * $(K^{\rm ab})_Q\cong C_2$ かつ $\mathrm{tg}$ 全射なら $\operatorname{coker}=0$ ⟹ **等号成立**。これは **$K8/K16$(dihedral 2 冪)で起きていた現象が非 dihedral で初めて再現**することを意味し、**破れないほうが大きな結果**。
>
> **committed な一言**: 上の二択のうち、**私は前者(破れる)に賭ける**。$L$・idx162・A16 の 3 標本すべてで $(K^{\rm ab})_Q$ は $\Lambda^2Q$ より真に大きかった。

---

## 3. 測定スペック(予言を判定するのに必要十分な 8 量)

凍結後の測定は次の 8 欄を出せば足りる(すべて既存の miner/capsule の語彙内):

```text
1. group_order            = |GTSh(N,N)|
2. ker_size               = |ker chi~|
3. chi_image_order        = |Q|              # phi(30) = 8 と比較(全射か)
4. Q_struct               = Q の不変因子      # C2 x C4 か・巡回か
5. K_struct               = ker chi~ の構造   # C15 x S の形か
6. Kprime_order           = |[K,K]|          # K^ab = K / [K,K]
7. Gprime_order           = |[G,G]|          # ker_size / Gprime_order = 破れの指数
8. KmodGprime_struct      = ker chi~ / [G,G] # ★ P4 の判定(2 群か)
+  Q_action_on_Kab        = Q 生成元の K^ab 上の作用行列   # ← KE-o と同じ欄。P4/P5 の直接判定
```

**判定表(凍結時点で固定)**:

| 予言 | PASS 条件 | FAIL なら |
|---|---|---|
| P1 | 欄 2 の奇部分が $3^a5^b$ | P81-B 反証 |
| P2 | 欄 2 の奇部分 $=15$ | $N_{\rm ord}$ 合成窓の新現象 |
| P3 | 欄 5 が $C_{15}\times(2\text{-群})$ | 核構造は半直積まで太る |
| P4 | 欄 8 が 2-群(位数 $2^k$) | $Q$ の奇部分作用が自明 = 拡大構造が予想外 |
| P5 | 欄 3 $=8$ かつ 欄 8 $\ne1$ | 等号成立なら K8/K16 型の非 dihedral 初例 |

---

## 4. 自己監査(誇張の抑制)

| # | リスク | 判定 |
|---|---|---|
| R-1 | **標本 2 個からのパターン外挿** | △ **明示**。P2/P3 の根拠は idx162 と A16 の 2 標本のみ。**P1 だけは P81-B という所見に載っている**が、それも証明ではない |
| R-2 | $N_{\rm ord}=15$ が委嘱文の情報で、私が検算していない | △ **明示**。$N_{\rm ord}$ が実は 15 でなければ本稿の算術($\varphi(30)=8$・$C_2\times C_4$)ごと無効。**凍結前に $N_{\rm ord}$ だけは確認を** |
| R-3 | $\widetilde\chi$ の全射を暗に仮定していないか | ○ **P5 のみ条件付き**。P1–P4 は $Q$ の大きさに依らない。ただし P4 の根拠は「$Q$ が $u\bmod3,u\bmod5$ を動かせる」なので、**$Q$ が小さいと弱まる**(→ P4 の FAIL は「$Q$ が小さかった」でも起きうる。欄 3・4 を同時に見ること) |
| R-4 | 「B2 は発火不能」の射程 | ○ **全射時のみ**。$Q$ が真部分群で巡回(例 $Q\cong C_4$)なら $\Lambda^2Q=0$ で **B2 が復活する**。§1.2 の表の但し書きはここ |
| R-5 | 予言が全部当たっても「機構の理解」にはならない | ○ **明示**。当たれば「$C_{N_{\rm ord}}\times2$-群 + 奇部分死亡」という**現象法則**が 3 標本に増えるだけ。**なぜそうなるかの証明は依然 open**(【KE-d】重み分解の文献要請) |
| R-6 | 私が A20 の値を見ていないことの担保 | △ **自己申告のみ**。§0 の接触申告が唯一の担保であり、**司令塔の既測確認と commit タイムスタンプが手続き的な担保**になる |

---

## 5. 未閉鎖項

* 【A20-a】**凍結手続き**: 司令塔の commit(タイムスタンプ)で本稿を凍結。**その前に「A20-15a は未測定」の確認**(§0)。
* 【A20-b】測定発注は凍結後。スペックは §3 の 8+1 欄。
* 【A20-c】本稿は紙上(paper-proof candidate ですらなく **予言**)。**測定前の推測であり、証明ではない。**
* 【A20-d】$N_{\rm ord}$ 合成の窓は本稿が初めてなので、**$C_{N_{\rm ord}}$ が $C_3\times C_5$ に割れる**という現象自体が新しい観測対象。P2 が当たれば「核の奇部分 $=C_{N_{\rm ord}}$」を**合成 $N_{\rm ord}$ でも**言えることになり、次は $N_{\rm ord}=p^2$ 型(核が $C_{p^2}$ か $C_p^2$ か)が自然な次の実験。

---

# §A18 【追記・裁定 196】W-D-A18-13a — control 窓

**A20 節(§0–§5)は一字も変更していない。** 本節のみ追記(2026-07-29)。

## A18-0 接触申告(**訂正を含む・司令塔の想定より広く見てしまった**)

司令塔は「A18 の測定値も未見・段階 1 窓 assert のみ存在」と確認したが、**私が読んだ `search/certs/strike_a18_stage1_20260729.json` には段階 2 の単一 $m$ 試行値が同梱されていた**:

$$\texttt{stage2\_trial\_m}=1,\qquad \boxed{\texttt{stage2\_trial\_shadow\_total}=104},\qquad \texttt{settled\_fail\_count}=0$$

(**A20 側の同ファイルにも `shadow_total = 120`($m=3$)がある。**)$\widetilde\chi$ は準同型なので**非空ファイバーは全て位数 $|\ker\widetilde\chi|$**(補題 FIB)。ゆえに

$$\boxed{\ |\ker\widetilde\chi(\text{A18})|=104,\qquad |\ker\widetilde\chi(\text{A20})|=120\ }\qquad\textbf{— これは予言ではなく導出である。}$$

**⚠ 手続き上の含意**: $|\ker|$ を予言欄に入れてはならない(§A18-2 で導出として隔離した)。**A20 節の P1–P5 は $|\ker|$ の値を予言していないので無傷**。段階 2 の**フル**結果($K$ の構造・$[G,G]$・$K/[G,G]$・導来長)は両窓とも**未見**(証明書自身が `stage2_full_run_performed_locally: false` と申告)。

## A18-1 算術と圏の同定

$$N_{\rm ord}=13,\quad 2N_{\rm ord}=26,\quad (\mathbf Z/26)^\times\cong(\mathbf Z/13)^\times\cong C_{12}\ \textbf{(巡回)},\quad\varphi(26)=12 .$$
$$\boxed{\ \text{全射なら}\ \Lambda^2Q=0\ \Longrightarrow\ \textbf{B2 圏}\ (\text{A16}\ (\mathbf Z/22)^\times\cong C_{10}\ \text{・idx162 と同圏})\ }$$

**これが control である理由**: A16($n=11$)から**素数を一つ替えただけ**で、$2N_{\rm ord}=2p$ ゆえ $Q$ は巡回のまま。A20($N_{\rm ord}=15$ 合成・$Q\cong C_2\times C_4$ 非巡回・$\Lambda^2Q\cong C_2\ne0$)だけが圏を跨ぐ。**A18 が A16 を再現し A20 が外れれば、原因は「$\Lambda^2Q\ne0$」に一意に帰属できる。**

**族の観察(段階 1 から)**: $|P|=3201186852864000=18!/2$、$C_P(\bar y)\cong C_{13}\times A_5$(780)、$\operatorname{Stab}_{\operatorname{Aut}P}(\bar x)\cong C_{13}\times S_5$(1560)。$P\cong A_{18}$ で $\bar x,\bar y$ は **13-サイクル**、$18-13=5$ 点が余る(A16: $A_{16}$・11-サイクル・余り 5 / A20: $A_{20}$・15-サイクル・余り 5 — **三窓とも余り 5 点**)。A16 の核の 2-部分 $D_8$ は $\operatorname{Syl}_2(S_5)$ と位数・構造が一致する。**この「余り 5 点」仮説が本節の予言の骨格**(私の読み。証明書は $P$ の名前を書いていない)。

## A18-2 導出(予言ではない)

| 量 | 値 | 出所 |
|---|---|---|
| $|\ker\widetilde\chi|$ | **104** $=8\cdot13$ | 補題 FIB + 試行値(§A18-0) |
| $|GTSh|$(全 $m$ 生存なら) | $104\times12=$ **1248** | 上 + `charming_count = 12`(**全射は予言 P0′**) |

参考: A16 は $88=8\cdot11$、$88\times10=880$(実測一致)。A20 は $120=8\cdot15$。**$|\ker|=8\cdot N_{\rm ord}$ が三窓で成立。**

## A18-3 予言 P0′–P5′

| # | 予言 | 反証条件 | FAIL の価値 |
|---|---|---|---|
| **P0′** | $\widetilde\chi$ **全射**($|Q|=12$、$|GTSh|=1248$) | いずれかの charming $m$ で shadow 全滅 | 非全射なら**命題 NI(v2.1 §11.2)より当該窓は非 isolated 確定** — $\chi$-退化系の第 2 実例 |
| **P1′** | $|\ker\widetilde\chi|$ の**奇部分は $\{13\}$-数**(奇素数 $p\mid|\ker|$ ⟹ $p=13$) | $3,5,7,\dots$ が核に現れる | **P81-B($R_\tau$ が $N_{\rm ord}$ 外の奇素数を殺す)の反証** |
| **P2′** | 奇部分 $=C_{13}$(**$C_{169}$ でも $C_{13}^2$ でもない**) | 奇部分 $\ne C_{13}$ | 核の奇部分が $C_{N_{\rm ord}}$ を超えて太る初例 |
| **P3′** | $\ker\widetilde\chi\cong C_{13}\times(2\text{-群})$、**具体的には $C_{13}\times D_8$** | $C_{13}\times Q_8$ / $C_{13}\times C_8$ / $C_{13}\times C_2\!\times\!C_4$ / $C_{13}\times C_2^3$ / 非分裂 $C_{13}\rtimes C_8$ 等 | **$D_8=\operatorname{Syl}_2(S_5)$ という族仮説が崩れる**(位数 104 の一致は構造の一致ではない) |
| **P4′** | $\ker\widetilde\chi/[G,G]$ は **2-群**、具体的には $C_2\times C_2$(⟺ $[G,G]=Z(K)\cong C_{13}\times C_2$、位数 26) | 商に 13 が現れる / 位数が 4 でない | 13-層が生き残るなら**「奇は死に偶は生きる」の部分生存(v2.4 §13.3)が族的でない** |
| **P5′** | **等号は破れる**(指数 4)。機構は **B2**($\Lambda^2Q=0$ ゆえ transgression 不在) | **等号成立** | **B2 圏の反例 = 大事件**。$\Lambda^2Q=0$ なら T-B は $\ker/[G,G]\cong(K^{\rm ab})_Q$ ちょうどなので、等号成立は $(K^{\rm ab})_Q=0$、すなわち **$Q$ が $K^{\rm ab}$ の 2-部分にも非自明に作用**することを意味する($u$ が常に奇であることと衝突しない形で)。A16 との唯一の差が素数 $11\to13$ なので、**原因の同定が極めて容易な反例**になる |
| **P6′** | $G^{\rm ab}\cong C_2^2\times Q\cong C_2\times C_2\times C_{12}$(位数 48・不変因子 $[2,2,12]$) | 位数 $\ne48$ | A16 の $[2,2,2,5]=C_2^2\times C_{10}$ が偶然だったことになる |
| **P7′** | $GTSh$ は **metabelian**(導来長 2) | 導来長 $\ge3$ | **壁の突破**。非可解 $C_P(\bar y)=C_{13}\times A_5$ をもつ窓で GT が非 metabelian なら壁キャンペーン最大の当たり |

## A18-4 測定スペック(A20 §3 と同一の 8+1 欄)

```text
1. group_order        = |GTSh|                  # 1248 ?
2. ker_size           = |ker chi~|              # 104(導出済・regression 欄)
3. chi_image_order    + Q の不変因子             # 12 / C12 ?        ← P0′
4. K_struct           = ker chi~ の構造          # C13 x D8 ?        ← P2′ P3′
5. Kprime_order       = |[K,K]|                 # 2 ?
6. Gprime_order       + Gprime_struct           # 26 = C13 x C2 ?   ← P4′
7. ZK_order, ZK_equals_Gprime                   # true ?
8. KmodGprime_struct  = ker chi~ / [G,G]        # C2 x C2 ?         ← P4′ P5′
9. derived_length(G) + GmodGprime_invariant_factors  # 2 / [2,2,12] ? ← P6′ P7′
+  Q_action_on_Kab    = Q 生成元の K^ab 上の作用行列  # P4′/P5′ を逆算でなく直接判定(KE-o と同欄)
```

**PASS/FAIL 判定表(凍結時点で固定)**

| 予言 | PASS 条件 | FAIL なら |
|---|---|---|
| P0′ | 欄 1 $=1248$ かつ 欄 3 $=12$ | 非 isolated 確定(命題 NI) |
| P1′ | 欄 2 の奇部分が $13^a$ | P81-B 反証 |
| P2′ | 欄 4 の奇部分 $=C_{13}$ | 核の奇部分が太る初例 |
| P3′ | 欄 4 $=C_{13}\times D_8$ | 族仮説($\operatorname{Syl}_2S_5$)崩壊 |
| P4′ | 欄 8 $=C_2\times C_2$ かつ 欄 6 $=26$ | 部分生存が族的でない |
| P5′ | 欄 8 $\ne1$ | **B2 圏の反例(大事件)** |
| P6′ | 欄 9 の不変因子 $=[2,2,12]$ | $G^{\rm ab}\cong C_2^2\times Q$ の族則崩壊 |
| P7′ | 欄 9 の導来長 $=2$ | **壁突破** |

## A18-5 手続き

* **launch order は証明書記載の `Sp45 -> A20 -> A18`**。A18 は control なので、**A20 の結果を見てから A18 の予言を書き換えないこと**が本節の生命線。凍結 commit のタイムスタンプがその担保。
* 本節も**予言**であり証明ではない。土台の段階 1 証明書は**単系統 GAP・`NOT a ledger claim` 自己申告**。
* 族の次項: $n=17$($N_{\rm ord}=17$・$(\mathbf Z/34)^\times\cong C_{16}$ 巡回 ⟹ また control)/ $n=21$($(\mathbf Z/42)^\times\cong C_2\times C_6$ 非巡回 ⟹ A20 型)。
