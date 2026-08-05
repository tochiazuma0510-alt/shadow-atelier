# 双子 witness 検査 — 事前登録票 v1(IF-FIRST・発火前)

- 起草: **数学者**(Opus 5)・2026-08-06
- 委嘱: **裁定 594**(Sol 便 110 返信 F110-2.1「双子 witness 検査: 修正つき小 gate PASS」L80–114 の逐語具現)
- 認可の射程: **twin witness 探索の認可であり、S3.6 の unlock そのものではない**(F110-2.1 末尾逐語)
- 入力正本:
  - `sol/sol_reply_110_math36.md` §F110-2.1(小 gate scope 5 点)
  - `search/certs/lins_twin_census_v1_20260806.json`(裁定 548 W-1 の twin census・INVENTORY ONLY)
  - `docs/week1-定義ノート.md` §1.5(語規約 W-1〜W-4)・§2(GTSh・(3.3)(3.4)・charming・Def 3.7・Prop 3.2/3.6/3.8・settled/isolated)
  - `docs/notes/auto_settled_check_v1.md`(OP-SETTLED・§3.2 (N1)–(N4)・**R1-b**・VERBAL-ISO・A.2/【AS-GAP-6】)
  - `docs/notes/w6_bottomup_design_v4.md` §5(**R1〜R5**・紙 bridge B-1/B-2・mutant matrix M-ISO-1〜6)
  - `docs/notes/wall_design_audit_v1.md` §1.5(torsor)・§6(ι の初等的事実・命題 6.3 transport・命題 6.6 ι-固定族)
  - `docs/notes/counterexample_hotspots_ideation_v1.md` 札 2【TWIN-DIFF】(発案・candidate)
- **状態: 事前登録票(発火前)。本票の登録集合・手順・出力文言・停止規則は、機械実行の前に固定する。** §2・§7 の補題群は **candidate**(Sol 監査未了)。
- **規律申告**: 本票の作成で走らせた機械は次の 2 本のみ。**いずれも窓の探索ではない**。
  1. census cert からの**登録集合の抽出**(読み取りのみ・§1。集合を固定する行為そのもの = 登録)
  2. **$B_3$ 内の恒等式の検算**(§2.2。Artin 忠実表現 $B_3\hookrightarrow\mathrm{Aut}(F_3)$ 上の 40 行スクリプト。**census 行にも窓にも一切触れていない**)
  - **鏡映軌道分類・悉皆列挙・kernel 比較は本票では一切実行していない**(= 発火は登録の後)。理由は §2.4 の補題により「鏡映分類 = witness 判定」と論理的に等価であり、先に走らせれば事前登録の意味が消えるため。
  - **封印 3 量($n=5$ 関連・$\mathrm{Im}\,R_{N,K^{(5)}}$・$d_N$・genuine 層の $u$ 値)非接触**・705,894 対宇宙**非接触**・kill 定理**非適用**・外部ライブ検索**ゼロ**。

---

## 0. 一枚まとめ(先に 8 行)

1. 登録集合を cert から機械抽出して固定した: **全 174 対 / PB₃ 層 28 対 / 現 ISO 層 15 対($c\in N$)/ 別層 13 対($c\notin N$)**。Sol の読み(F110-2.1)と**完全一致**。directed は各々 348 / 56 / 30 / 26。
2. 鏡映 $\iota(\sigma_i)=\sigma_i^{-1}$ は工房既在(`wall_design_audit_v1.md` §6)。本票の新しい橋は **標準 pair $[-1,1]$ が「常に」GT-shadow であること**(§2.2・$B_3$ 内の恒等式で証明・機械検算済)。
3. ゆえに $\ker T_{-1,1}=\iota(N)$ で、$$\boxed{\ \iota(N)\ne N\ \Longrightarrow\ N\ \textbf{は非 isolated(明示 witness }[-1,1])\ }$$ 対偶: **isolated $\Rightarrow$ $\iota$-不変**(atlas の isolated 列への安価な必要条件・副産物)。
4. 判定基準 **MIRROR-CRIT**: $\iota(N)=N\iff(\bar x,\bar y)\mapsto(\bar x^{-1},\bar y^{-1})$ が $P=F_2/N_{F_2}$ の自己同型に延びる。系: **$P$ 可換 ⟹ 鏡映不変(witness なし)**/**$P$ に特性巡回部分群 $A$ があり共役表現 $\mu:P\to\mathrm{Aut}(A)$ の像が初等可換 2 群でない ⟹ $\iota(N)\ne N$**。
5. これに紙の補題 **ABEL-INDEX**(「$P$ 可換 ⟹ $\lvert P\rvert=n^2$ または $3n^2$」)を併せると、**15 対のうち 8 対(指数 126, 234, 342, 378, 558, 666, 702, 774)は紙だけで witness が出る**という予言になる(§7)。残り 7 対は紙で UNKNOWN。
6. 非鏡映層の手順は **R1-b 厳守**: $(m,\bar f)$ を**群の元として**悉皆 → hexagon+charming+SURJ で shadow 確定 → **その後**に kernel 比較。descent/settled を列挙 filter にしない。
7. 二系統は「GAP」対「**GAP helper 非共有の python 証明書再検査(置換演算のみ)**」+ 鏡映経路では**紙証明**。★**$\lvert GT(N)\rvert$ と $\lvert GT(K)\rvert$ の差は witness にならない** — それどころか差の存在は $\mathrm{GTSh}(K,N)=\emptyset$ の**証明**である(§4.2 命題 TWIN-CARD の系)。発案札 2 の差動論法はここで向きが逆転する。
8. 出力文言は先に固定: witness 無し ⟹ 「**登録した directed pair 群で未発見**」のみ(AS-GAP-6 の非存在も AUTO-SETTLED も主張しない)。witness 有り ⟹ **M-ISO-2 の実物 fixture** として R1〜R5 aggregate receipt に接続。

---

## 1. 登録集合の固定(scope ①)

### 1.1 入力 cert の同定

| 項目 | 値 |
|---|---|
| path | `search/certs/lins_twin_census_v1_20260806.json` |
| **sha256** | `8bfd762ef565f5ce72f9a4a25368783b96b02f4905274e858d460e30bb335610` |
| bytes | 641,947 |
| generated_by | `search/lins-twin-census-v1.g`(裁定 548 W-1) |
| `census_index_hi` | **1000**(= LINS 探索上界) |
| `lins_nodes_total_this_call` | 1946(single process / single LINS call = LID-1) |
| `rows_processed` / `pair_checks` | 1945 / 5970 |
| `twin_pairs_found` | **174** |

**twin の定義(cert の実装どおり)**: $N\ne K$ がともに $B_3$ の正規部分群で、$[B_3:N]=[B_3:K]\le1000$ かつ $B_3/N\cong B_3/K$。同型判定は IdGroup ラベル一致(両者利用可のとき)、不可なら StructureDescription 一致を前置フィルタとした `IsomorphismGroups`。**同一部分群は両向き包含で除外済み。**

### 1.2 層の定義(cert 欄に対する 3 行の述語)と個数

| 層 | 述語(pair の両 member に対して) | **unordered** | **directed** | 最小指数 |
|---|---|---|---|---|
| **L0** | (全 twin pair) | **174** | **348** | 24 |
| **L1** | `in_PB3 = true`(両 member) | **28** | **56** | **126** |
| **L2 = 現 ISO 層** | L1 かつ `c_in_N = true`(両 member) | **15** | **30** | **126** |
| **L3 = 別層** | L1 かつ `c_in_N = false`(両 member) | **13** | **26** | 252 |

- **L2 ⊔ L3 = L1**(機械確認)。**L1 内に `c_in_N` が混在する対はゼロ**(全 174 対中の混在対は 5 件で、いずれも L1 の外)。
- **集合の digest**(pair UID の昇順連結の sha256。UID = `sha256(index # sorted(member UID))` の先頭 12 桁、member UID = `sha256(canonical_id_words を "|" で連結)` の先頭 12 桁):

| 層 | SETDIGEST(sha256) |
|---|---|
| L0 | `babc71f11022694bafde5f4b73ab06c677fc25aee6cd3bff6651e2aaac47be87` |
| L1 | `f94a8ae0384144189950d61ba727fc713a0eacb751a712784d5923a7a067daa3` |
| **L2** | `ec72ed77e1bb6040c5a4d29e43b51e45a63b5d2ffa6d50f8e8455aa16d7c9bba` |
| L3 | `af88692a78341c82688169c4b3ade43b4d4c83ed0e7c54e160365249b0e18ebd` |

> **★ 登録の意味**: 本走で用いる集合は **L2 の 15 対(directed 30)に限る**。L1 の残り(= L3)と L0 の残り 146 対は**現 checker の入力にしない**。集合を後から広げる場合は本票の versioned 後継(v2)で再登録する。

### 1.3 unordered pair と directed $\mathrm{GTSh}(K,N)$ の区別(**混同禁止**)

定義ノート §2 逐語: $\mathrm{GTSh}(K,N):=\{[m,f]\in GT(N)\mid\ker T_{m,f}=K\}$(**$K$ = source、$N$ = target**)。

$$\boxed{\ \textbf{unordered pair }\{A,B\}\ \longmapsto\ \textbf{directed 2 件: }\mathrm{GTSh}(B,A)\ (\subseteq GT(A))\ \textbf{と}\ \mathrm{GTSh}(A,B)\ (\subseteq GT(B))\ }$$

- 検査の**単位は directed**。「対 $\{A,B\}$ を検査した」は無定義であり、cert には **必ず `(target_window, source_kernel)` の順序つきで**記録する。
- 片方向が非空でもう片方が空、はこの段階では**排除しない**(群oid の逆射 (3.54) から両方向同時に非空になるはずだが、それは**検査すべき整合性**であって前提ではない — §6 S-TW-5)。
- 登録 directed 集合 **D2**(30 件)= L2 の 15 対 × 2 方向。

### 1.4 L2 = 現 ISO 層 15 対(全表・これが登録集合)

$\widehat P:=B_3/N$(位数 = 指数)、$P:=PB_3/N\cong F_2/N_{F_2}$(**$c\in N$ ゆえ同型**)、$\lvert P\rvert=\text{指数}/6$($[B_3:PB_3]=6$)。

| # | pair UID | 指数 $=\lvert\widehat P\rvert$ | $\lvert P\rvert$ | $\widehat P$ の構造 | IdGroup | member UID (A / B) |
|---|---|---|---|---|---|---|
| 1 | `b6b8a3feb9d2` | 126 | **21** | `C7 : (C3 x S3)` | [126, 9] | `7bee16618268` / `84f28df5792d` |
| 2 | `2858cc2db1a7` | 234 | **39** | `C13 : (C3 x S3)` | [234, 9] | `6e60ce938838` / `e9194840bb09` |
| 3 | `475adabdc9ed` | 342 | **57** | `C19 : (C3 x S3)` | [342, 11] | `2dd0872a952c` / `f9572974b65e` |
| 4 | `73d458be805c` | 378 | **63** | `C7 : ((C3 x C3) : C6)` | [378, 22] | `30c41b0ef152` / `1b9cbbe23386` |
| 5 | `4b717d423b93` | 432 | **72** | `(((C3 x C3) : Q8) : C3) : C2` | [432, 734] | `c89d28a7c1a5` / `663166de6a6e` |
| 6 | `b2bef4dba95b` | 486 | **81** | `((C9 : C9) : C3) : C2` | [486, 39] | `da05b7bd8bc7` / `7536e5f8c117` |
| 7 | `c5b8a47f5d70` | 504 | **84** | `C7 : (A4 x S3)` | [504, 186] | `e649609337b1` / `a1319ba72dbf` |
| 8 | `e181bd7062ce` | 504 | **84** | `C7 : (C3 x S4)` | [504, 160] | `668f2afaa377` / `3b801a7ba0f9` |
| 9 | `f266c8765cb8` | 558 | **93** | `C31 : (C3 x S3)` | [558, 9] | `0f93a4433f8e` / `776022fa7d45` |
| 10 | `0c820fc5fbc3` | 666 | **111** | `C37 : (C3 x S3)` | [666, 11] | `afe28f765b59` / `b93a8f9d4927` |
| 11 | `ef6b2f6322d6` | 702 | **117** | `C13 : ((C3 x C3) : C6)` | [702, 22] | `ec9233a60dd6` / `3349ceec8779` |
| 12 | `c34212b7dd19` | 774 | **129** | `C43 : (C3 x S3)` | [774, 9] | `3ec759fe7a89` / `c95f99244140` |
| 13 | `a3fd068a4467` | 882 | **147** | `C49 : (C3 x S3)` | [882, 9] | `6afd80ecad54` / `b384172dd375` |
| 14 | `4351f9476f2c` | 936 | **156** | `C13 : (C3 x S4)` | [936, 169] | `c4fd6495ff27` / `cf5757e9dd21` |
| 15 | `f8599b5bccee` | 936 | **156** | `C13 : (A4 x S3)` | [936, 202] | `540adb3380a3` / `6e0a2700e658` |

member の A/B の並びは cert 内の出現順。**A/B のラベルに数学的意味はない**(directed の向きは §1.3 の記法で別に書く)。

### 1.5 L3 = $c\notin N$ の 13 対(**別層 — 現 checker で TRUE/FALSE を付けない**)

| # | pair UID | 指数 | $\widehat P$ の構造 | IdGroup |
|---|---|---|---|---|
| 1 | `33109fc9986e` | 252 | `C7 : (C3 x (C3 : C4))` | [252, 18] |
| 2 | `7f9ec635ec01` | 378 | `C7 : (C9 x S3)` | [378, 21] |
| 3 | `0ec4049a3895` | 468 | `C13 : (C3 x (C3 : C4))` | [468, 21] |
| 4 | `e4326ce0ccfb` | 504 | `C7 : (C3 x (C3 : C8))` | [504, 44] |
| 5 | `9484279fd426` | 630 | `C5 x (C7 : (C3 x S3))` | [630, 17] |
| 6 | `7c9f1acd0a27` | 684 | `C19 : (C3 x (C3 : C4))` | [684, 20] |
| 7 | `5adae3b6eacc` | 702 | `C13 : (C9 x S3)` | [702, 21] |
| 8 | `a70eef14a40b` | 756 | `C7 : (C9 x (C3 : C4))` | [756, 30] |
| 9 | `f8b5a91df53b` | 756 | `C7 : (((C3 x C3) : C3) : C4)` | [756, 31] |
| 10 | `dc518d193b59` | 864 | `(((C3 x C3) : Q8) : C3) : C4` | [864, 4053] |
| 11 | `81258e6b764e` | 882 | `C7 x (C7 : (C3 x S3))` | [882, 48] |
| 12 | `4945f0e1fd64` | 936 | `C13 : (C3 x (C3 : C8))` | [936, 47] |
| 13 | `4f4b94434f22` | 972 | `((C9 : C9) : C3) : C4` | [972, 42] |

**理由(F110-2.1 逐語)**: v4 ISO-GATE の R1/紙 bridge B-1 は $c\in N$ を前件とし、**M-ISO-6 は $c\notin N$ を `UNKNOWN` に送る**。この 13 対を現 checker に入れて TRUE/FALSE を付けることは M-ISO-6 違反(空虚な真の混入・【W6K-GAP-1】)である。

> ★ **ただし記録しておく(裁定請求・実行しない)**: §2.2 の補題 MIRROR-SHADOW は **$c\in N$ を使っていない**($B_3$ 内の恒等式のみ)。ゆえに紙の witness 経路は原理的に L3 にも延びる。**本票ではこれを主張も実行もしない** — 前件が違う以上、L3 への適用は別 gate(checker 側の $c\notin N$ 対応 = 語レベル評価と DESCENT-c 不成立の扱い、定義ノート §2 の 2026-07-25 注記)を要する。**【要裁定 T-1】**として起票し、認可なしに L3 へは撃たない。

### 1.6 抽出で観測した構造的事実(4 件・すべて機械確認)

| # | 事実 | 何に効くか |
|---|---|---|
| **O-1** | **L1 の 56 member はすべて相異なる**(L0 全体では 348 member 中 15 件が複数対に重複出現するが、その全部が L1 の外) | ⟹ **L1 上で twin 関係は完全マッチング**(3 つ以上が互いに twin になっている塊が無い)。⟹ §2.5 の系: L1 の $N$ について $\iota(N)\ne N$ なら $\iota(N)$ は**その対の相手 $K$ そのもの**(依存 D-1) |
| **O-2** | L1 の全指数が 6 で割り切れる | $\lvert P\rvert=$ 指数$/6$ が整数として確定(§1.4 の $\lvert P\rvert$ 列) |
| **O-3** | L1 内に `c_in_N` 混在対はゼロ(L0 全体では 5 件) | L2/L3 の二分が clean。混在対の扱いを設計しなくてよい |
| **O-4** | 対の両 member は structure/IdGroup が常に一致(174 対全件) | cert の twin 判定が設計どおり動作している傍証 |

### 1.7 依存(登録と同時に固定する前提)

| # | 依存 | 破れた場合の影響 |
|---|---|---|
| **D-1** | LINS の $\le1000$ 悉皆性(cert の LID-1 規律) | O-1 の系(「$\iota(N)$ = 対の相手」)が崩れる。**witness そのものは崩れない**(§2.2 は census に依存しない) |
| **D-2** | 探索上界 1000 | 指数 > 1000 の双子は登録宇宙外。**「未発見」の文言はこの上界つきでのみ有効** |
| **D-3** | `in_PB3` / `c_in_N` / index の cert 値 | §2.6 の MC-1 証明書(python 再検査)で**独立に再検証する**(cert を信用しない設計) |
| **D-4** | quotient 同型判定(IdGroup / IsomorphismGroups) | 対の**組み方**にのみ効く。directed 検査自体は組み方に依存しない |

---

## 2. 鏡映軌道分類(scope ②)

### 2.1 規約の pin(**発火前に固定・以降の全計算はこれに従う**)

| 記号 | 定義(正本 = 定義ノート) |
|---|---|
| $B_3$ | $\langle\sigma_1,\sigma_2\mid\sigma_1\sigma_2\sigma_1=\sigma_2\sigma_1\sigma_2\rangle$。cert の生成元は $a=\sigma_1$, $b=\sigma_2$ |
| $\Delta,\ c$ | $\Delta=\sigma_1\sigma_2\sigma_1$、$c=\Delta^2=(\sigma_1\sigma_2)^3$(中心)。cert の `c` は `(a*b*a)^2` = 同一物 |
| $x,y$ | $x=\sigma_1^2$、$y=\sigma_2^2$。$F_2=\langle x,y\rangle$、$PB_3=F_2\times\langle c\rangle$ |
| $\theta,\tau$ | $\theta:x\leftrightarrow y$、$\tau:x\mapsto y\mapsto z\mapsto x$($z=(xy)^{-1}$、$\tau^3=\mathrm{id}$) |
| hexagon | (3.3)(3.4) を $B_3/N$ 内で。簡約形 (3.10) $f\theta(f)\in N_{F_2}$、(3.11) $\tau^2(y^mf)\tau(y^mf)y^mf\in N_{F_2}$ |
| 積の向き | **規約 W-1〜W-4**。paper 語 $"AB"$ ↔ GAP 乗算 `B*A`。**判定式の積も paper 積**(W-4) |
| $T_{m,f}$ | $\sigma_1\mapsto\sigma_1^{2m+1}N$、$\sigma_2\mapsto f^{-1}\sigma_2^{2m+1}fN$(Prop 3.2)。$u:=2m+1$ |
| $\iota$ | $\iota(\sigma_i)=\sigma_i^{-1}$。$\iota\in\mathrm{Aut}(B_3)\setminus\mathrm{Inn}$、$\iota^2=\mathrm{id}$、$\iota(PB_3)=PB_3$(`wall_design_audit_v1.md` §6.2 の初等 3 行。**Dyer–Grossman は「これ以外に無い」の完全性にのみ必要で、本票は完全性を使わない**) |
| $\iota|_{F_2}$ | $x\mapsto x^{-1}$、$y\mapsto y^{-1}$。$\iota(c)=c^{-1}$(機械検算済 §2.2) |

**標準 pair の同定**: $[m,f]=[-1,1]$ は $u=2m+1=-1$ と同値($2m+1=-1\iff m=-1$ — **どちらの読みでも同一物**であり曖昧さがない)。

### 2.2 補題 MIRROR-SHADOW(candidate・本票)

> ### 補題 MIRROR-SHADOW
> $N\in\mathrm{NFI}_{PB_3}(B_3)$ を任意にとる($c\in N$ は**不要**)。このとき
> $$\boxed{\ [-1,1]\in GT(N)\ \textbf{は常に GT-shadow であり、}\ \ker T_{-1,1}=\iota(N)\ }$$
> ゆえに $\mathrm{GTSh}(\iota(N),N)\ne\emptyset$ であり、
> $$\boxed{\ \iota(N)\ne N\ \Longrightarrow\ [-1,1]\ \textbf{は非 settled shadow}\ \Longrightarrow\ N\ \textbf{は非 isolated}\ }$$
> 対偶: **$N$ が isolated $\Rightarrow$ $\iota(N)=N$**。

**証明.**

**(a) hexagon**: $m=-1,f=1$ を (3.3)(3.4) に代入すると、$x=\sigma_1^2$, $y=\sigma_2^2$, $c=\Delta^2$ の下で
$$\text{(3.3)}:\ \sigma_1^{-1}\sigma_2^{-1}\ \overset{?}{=}\ \sigma_1\sigma_2\,x\,c^{-1},\qquad
\text{(3.4)}:\ \sigma_2^{-1}\sigma_1^{-1}\ \overset{?}{=}\ \sigma_2\sigma_1\,y\,c^{-1}.$$
右辺 (3.3) $=\sigma_1\sigma_2\sigma_1^2\Delta^{-2}=\Delta\sigma_1\Delta^{-2}=(\Delta\sigma_1\Delta^{-1})\Delta^{-1}=\sigma_2\Delta^{-1}=\sigma_2(\sigma_2\sigma_1\sigma_2)^{-1}=\sigma_1^{-1}\sigma_2^{-1}$ = 左辺。
(3.4) も同様($\Delta\sigma_2\Delta^{-1}=\sigma_1$ を使う)。**これは $N$ に依らず $B_3$ 内の恒等式である**(mod $N$ ではなく等号)。

**(b) charming**: $2m+1=-1$ は任意の $\mathbf Z/N_{\rm ord}$ で単元(逆元は自分自身)。$f=1\in[F_2/N_{F_2},F_2/N_{F_2}]$。✓

**(c) (SURJ)**: $T_{-1,1}(\sigma_1)=\sigma_1^{-1}N$、$T_{-1,1}(\sigma_2)=\sigma_2^{-1}N$ であり $\langle\sigma_1^{-1},\sigma_2^{-1}\rangle=B_3$。ゆえに $T_{-1,1}$ は全射(Def 3.7 の全射性・Prop 3.6 のどの水準で見ても同じ)。✓ ⟹ (a)(b)(c) より $[-1,1]$ は **GT-shadow**。

**(d) kernel**: $T_{-1,1}=\pi_N\circ\iota$($\pi_N:B_3\twoheadrightarrow B_3/N$)。$\iota^2=\mathrm{id}$ より
$$\ker T_{-1,1}=\iota^{-1}(N)=\iota(N).$$
(N1)(N2)(N3)(`auto_settled_check_v1.md` §3.2)より非 settled $\iff\ker T_{m,f}\ne N$。∎

**機械検算(窓非接触)**: 忠実表現 $B_3\hookrightarrow\mathrm{Aut}(F_3)$($\sigma_i:t_i\mapsto t_it_{i+1}t_i^{-1},\ t_{i+1}\mapsto t_i$)上の 40 行スクリプトで、braid 関係・$\Delta^2=(\sigma_1\sigma_2)^3$・$c$ の中心性・**(3.3)(3.4) の恒等成立**・$\iota$ の braid 関係保存・$\iota(c)=c^{-1}$・$\tau^3=\mathrm{id}$ をすべて確認(**ALL TRUE**)。

**★ 副産物 = 無料の規約カナリア(必須検査に格上げ推奨)**: 簡約 (3.11) を $[-1,1]$ で評価すると
$$\underbrace{\tau^2(y^{-1})\,\tau(y^{-1})\,y^{-1}=x^{-1}\cdot(xy)\cdot y^{-1}=1}_{\textbf{paper 積(規約 W-4・正本)}}\qquad\text{vs.}\qquad\underbrace{y^{-1}\cdot(xy)\cdot x^{-1}=[y^{-1},x]\ne1}_{\textbf{逆順}}$$
**規約が正しければ $[-1,1]$ は全窓で hexagon を通らねばならない。通らなければ規約か実装が壊れている**(§6 S-TW-6)。(3.10) は $f=1$ ゆえ向きに鈍感((H-a) と同型の現象)。

**帰属**: 「$K=\iota^{-1}(N)$ なら $\ker T_{-1,1}=K$、$K\ne N$ なら non-settled shadow の候補」という**着想は Sol(F110-2.1 L98–104)**。$\iota$ の初等的性質と transport(命題 6.3)・$\iota$-固定族(命題 6.6)は**工房既在**(`wall_design_audit_v1.md` §6)。本補題の新規部分は **(a)(b)(c) = $[-1,1]$ が無条件に shadow であることの証明**(候補ではなく確定)である。**novelty grep**: `MIRROR`(0 hit)・`鏡映`(既出だが $[-1,1]$ との接続は無し)・「複素共役」(Ihara ICM 経由の $\chi(\iota)=-1,f_\iota=1$ は `bhunt_prereg_iffirst_v1.md` に既出)・`GTSh(K,N)`(定義のみ)。**「$[-1,1]$ が常に shadow」「$\iota(N)\ne N\Rightarrow$ 非 isolated」「isolated $\Rightarrow$ $\iota$-不変」は repo 未出。**

> ⚠ **格の限定(重要)**: $[-1,1]$ は Ihara ICM の複素共役そのもの($\chi=-1,f=1$)であり、したがって**算術元**である。⟹ 本経路が出す witness は「**settled 述語が FALSE を返せることの実物**(M-ISO-2)」であって、**非算術証人(B 型)ではない**。発案札 2 の狙い(非算術証人の名指し)とは**別物**であり、混同を禁止する。

### 2.3 補題 MIRROR-CRIT(candidate・本票)— 判定基準の finite 化

> $c\in N$、$P:=F_2/N_{F_2}$、$\bar x,\bar y\in P$ を $x,y$ の像とする($\langle\bar x,\bar y\rangle=P$)。このとき
> $$\boxed{\ \iota(N)=N\iff\exists\alpha\in\mathrm{Aut}(P):\ \alpha(\bar x)=\bar x^{-1}\ \wedge\ \alpha(\bar y)=\bar y^{-1}\ }$$

**証明.** $c\in N$ かつ $N\le PB_3=F_2\times\langle c\rangle$ より $N=N_{F_2}\cdot\langle c\rangle$($n=wc^k\in N$ なら $w=nc^{-k}\in N\cap F_2$)。$\iota(c)=c^{-1}$ ゆえ $\iota(N)=\iota(N_{F_2})\cdot\langle c\rangle$、したがって $\iota(N)=N\iff\iota(N_{F_2})=N_{F_2}$。
$\pi:F_2\to P$ とすると $\ker(\pi\circ\iota|_{F_2})=\iota^{-1}(N_{F_2})=\iota(N_{F_2})$。二つの全射 $F_2\to P$ が同じ核をもつ $\iff$ 自己同型 $\alpha$ で差がつく。$\pi\circ\iota$ は $x\mapsto\bar x^{-1},y\mapsto\bar y^{-1}$ を送るから、条件は上式。∎

### 2.4 系(**紙で判定が付く帯**)

> **系 (a)(可換)**: $P$ が可換なら反転 $g\mapsto g^{-1}$ は $\mathrm{Aut}(P)$ の元。⟹ **$\iota(N)=N$**(鏡映 witness なし)。
>
> **系 (b) MIRROR-OBSTRUCTION**: $A\le P$ を**特性部分群で $\mathrm{Aut}(A)$ が可換**なもの(例: $A$ 巡回)とし、$\mu:P\to\mathrm{Aut}(A)$ を共役表現とする。このとき $\mu$ は $\mathrm{Aut}(P)$-不変($\mu\circ\alpha=\mu$)。ゆえに
> $$\mu(P)\ \textbf{が初等可換 2 群でない}\ \Longrightarrow\ \iota(N)\ne N\ \Longrightarrow\ N\ \textbf{は非 isolated}.$$
>
> **系 (c) Frobenius**: $P\cong C_p\rtimes C_q$($q$ **奇**・作用忠実)なら $\iota(N)\ne N$。

**証明.** (b) $\alpha\in\mathrm{Aut}(P)$、$\alpha_0:=\alpha|_A\in\mathrm{Aut}(A)$。$g\in P,a\in A$ に対し $\alpha(gag^{-1})=\alpha(g)\alpha(a)\alpha(g)^{-1}$ より $\mu(\alpha(g))\circ\alpha_0=\alpha_0\circ\mu(g)$、$\mathrm{Aut}(A)$ 可換ゆえ $\mu(\alpha(g))=\mu(g)$。
いま $\alpha(\bar x)=\bar x^{-1}$ なら $\mu(\bar x)=\mu(\bar x)^{-1}$、すなわち $\mu(\bar x)^2=1$。$\bar y$ も同様。$\mu(P)=\langle\mu(\bar x),\mu(\bar y)\rangle$ は可換群 $\mathrm{Aut}(A)$ の中で位数 $\le2$ の 2 元が生成 ⟹ 初等可換 2 群。対偶が主張。
(c) $A=$ Sylow$_p$(Frobenius 核・特性・巡回)、$\mathrm{Aut}(A)=C_{p-1}$ 可換、$\mu(P)\cong C_q$($q$ 奇 $>1$)は初等可換 2 群でない。∎

> **補題 ABEL-INDEX(candidate・本票)**: $c\in N$ とする。$P$ が可換なら
> $$\boxed{\ \lvert P\rvert=n^2\ \textbf{または}\ 3n^2\quad(n\in\mathbf Z_{\ge1})\ }$$

**証明.** $P$ 可換 $\Rightarrow N_{F_2}\supseteq[F_2,F_2]$、$P=\mathbf Z^2/M$($\mathbf Z^2=F_2^{\rm ab}$、$M=N_{F_2}/[F_2,F_2]$)。$N\trianglelefteq B_3$ と $c\in N$ より $M$ は $B_3$-作用で安定。$F_2\cong PB_3/\langle c\rangle$ 上の $B_3$-作用は $PB_3$ が自明に作用するので $S_3=B_3/PB_3$ を経由し、$F_2^{\rm ab}$ 上では $\{\bar x,\bar y,\bar z\}$($\bar x+\bar y+\bar z=0$)の**置換作用** = $A_2$ 根格子上の $W(A_2)=S_3$ 作用である($\sigma_1$: $A_{12}\mapsto A_{12}$, $A_{23}\leftrightarrow A_{13}$)。
$A_2\cong\mathbf Z[\omega]$、3-巡回 = $\omega$ 倍、互換 = 共役つき反射。$S_3$-安定部分格子 = 共役安定イデアル $(\alpha)$ で、$(\bar\alpha)=(\alpha)$ ⟹ $\alpha\sim n(1-\omega)^\varepsilon$($n\in\mathbf Z$、$\varepsilon\in\{0,1\}$、$(1-\omega)^2=(3)$)。指数 $=N(\alpha)=n^2 3^\varepsilon$。∎

**novelty grep**: `ABEL-INDEX`・`A_2 格子`・`Eisenstein` は repo 未出(`MIRROR-OBSTRUCTION` も 0 hit)。

### 2.5 分類手順(**実行は登録の後**)

L1 の 28 対(56 member)を対象に、各 member $N$ について $\iota(N)$ を計算し、次の 3 類に分類する。

| 類 | 定義 | 帰結 |
|---|---|---|
| **M0** | $\iota(N)=N$(自己鏡映) | $[-1,1]$ は settled。**この窓では鏡映 witness なし**(非 isolated かは §3 の悉皆で別途判定) |
| **M1** | $\iota(N)=K$(= その対の相手) | ★ **鏡映対**。$[-1,1]\in\mathrm{GTSh}(K,N)$ かつ $[-1,1]\in\mathrm{GTSh}(N,K)$ ⟹ **両方向が同時に非空** |
| **M2** | $\iota(N)\notin\{N,K\}$ | witness としては有効(§2.2)だが **directed pair が登録集合の外**。⟹ §5.3 の分岐 (iv) へ。**同時に O-1/D-1 の破れの信号**(L1 の完全マッチング性と矛盾)なので **S-TW-7 で STOP して census 側を再検分**する |

**判定手続き(系統 A・GAP)**: cert の `canonical_id_words` $n_1,\dots,n_r$($N$ の生成元語)に対し、$\pi_N:B_3\to B_3/N$(有限商)を作り
$$\iota(N)=N\iff\pi_N(\iota(n_i))=1\ \ (\forall i),\qquad \iota(n_i)=n_i(a\mapsto a^{-1},\,b\mapsto b^{-1})\ \textbf{(語の指数一斉反転・順序は不変)}$$
($\iota(N)\subseteq N$ と $[B_3:\iota(N)]=[B_3:N]$ から等号。$\iota$ は準同型であって反準同型ではない ⟹ **語を逆順にしない**。定義ノート §1.5.2 補題 W1 の $\iota$ と**同じ写像**であることに注意 — `wall_design_audit_v1.md` §6.5 の警告どおり、transport 欄と規約検査欄を混同しない)。

### 2.6 直接検査 4 点(**M1 の $[-1,1]$ に対する必須検査**・順序も固定)

登録した順に、**独立に**実行し、4 つとも cert に記録する(1 つでも欠けたら witness と呼ばない)。

| 検査 | 内容 | 判定式 |
|---|---|---|
| **W-a hexagon** | 簡約 (3.10)(3.11) を $m=-1,f=1$ で。**加えて** full (3.3)(3.4) を $B_3/N$ 上で(探索器と照合器の分離・定義ノート §4-2) | (3.10): $1\cdot\theta(1)=1\in N_{F_2}$ ✓/(3.11): $\tau^2(y^{-1})\tau(y^{-1})y^{-1}=1$ ✓(**paper 積**)/(3.3)(3.4): $\pi_N$ で両辺一致 |
| **W-b charming** | $\gcd(2m+1,N_{\rm ord})=1$ と $\bar f\in[P,P]$ | $2m+1=-1$、$\bar f=1$ |
| **W-c SURJ** | $\langle\bar x^{u},\bar f^{-1}\bar y^{u}\bar f\rangle=P$($u=-1$) | $\langle\bar x^{-1},\bar y^{-1}\rangle=P$ |
| **W-d kernel equality** | $\ker T_{-1,1}=K\ne N$ | (i) $\pi_N(\iota(k_j))=1$($K$ の全生成元語 $k_j$)⟹ $K\subseteq\ker$、(ii) $\lvert\mathrm{Im}\,T_{-1,1}\rvert=[B_3:N]$ ⟹ 等号、(iii) $\exists i:\pi_N(\iota(n_i))\ne1$ ⟹ $K\ne N$ |

**W-d の (iii) が本体**(= $\iota(N)\ne N$)。(i)(ii) は $K$ の同定であり、**(iii) だけで非 settled は確定する**(§2.2)。

### 2.7 証明書 MC-1(mirror certificate・第二系統の入力)

```
mirror_cert/v1 {
  target_window_uid, source_kernel_uid,        # member UID(§1.2 の定義)
  index, in_PB3, c_in_N,                       # cert 由来。python 側で再検証する
  perm_degree, s1_perm, s2_perm,               # rho: B3 -> Q  の生成元像(置換)
  N_gen_words: [...],  K_gen_words: [...],     # a,b 語(cert 逐語)
  witness_word: w,                             # w in N_gen_words で rho(iota(w)) != 1
  shadow: { m: -1, f_word: [] },               # [-1,1]
  checks: { braid, N_in_ker, K_in_ker, imorder, iota_w_nontrivial, hexagon_full, surj }
}
```

**python 側(GAP helper 非共有)が再検証する内容**(すべて置換の積のみ・群論ライブラリ不要):

1. `s1*s2*s1 == s2*s1*s2`(braid 関係)⟹ $\rho:B_3\to\mathrm{Sym}$ が well-defined。
2. 全 `N_gen_words` について $\rho(n_i)=1$ ⟹ $N\subseteq\ker\rho$。
3. **$\rho(\iota(w))\ne1$**($w\in N$)⟹ $\iota(w)\notin\ker\rho\supseteq N$ ⟹ $\iota(w)\in\iota(N)\setminus N$ ⟹ $\boxed{\iota(N)\ne N}$。
   **★ この 3 点だけで非 settled が確定する**($\lvert\mathrm{Im}\rho\rvert$ も index も不要 = cert への依存が最小)。
4. (同定のため)BFS で $\lvert\langle s_1,s_2\rangle\rvert$ を数え `index` と一致すること、全 `K_gen_words` で $\rho(\iota(k_j))=1$ ⟹ $\ker T_{-1,1}=K$。
5. (独立確認)$\rho$ 上で full hexagon (3.3)(3.4) at $[-1,1]$、SURJ、$c=(ab a)^2$ の像で `c_in_N` を再判定。

---

## 3. 非鏡映層の悉皆手順(scope ③・**R1-b 厳守**)

対象: **M0 に分類された L2 の窓すべて**(および M1 の窓も、shadow 全体と $\lvert GT\rvert$ を得るために実行してよい)。

### 3.1 手順の順序(**この順序が仕様である**)

> **(i) 列挙**: $(m,\bar f)\in(\mathbf Z/N_{\rm ord})\times[P,P]$ を、$m$ は整数代表 $0..N_{\rm ord}-1$、$\bar f$ は**有限群 $[P,P]$ の元として**(語ではなく)1 回ずつ悉皆(紙 bridge B-1・`enumeration_domain: group_elements`)。$N_{\rm ord}=\mathrm{lcm}(\mathrm{ord}\,\bar x,\mathrm{ord}\,\bar y)$($c\in N$ ゆえ $\mathrm{ord}\,\bar c=1$)。
> **(ii) 絞り込み**: hexagon (3.10)(3.11)(**paper 積**)+ charming($\gcd(2m+1,N_{\rm ord})=1$)+ **(SURJ)** $\langle\bar x^u,\bar f^{-1}\bar y^u\bar f\rangle=P$。⟹ **GT-shadow の集合** $\mathfrak S(N)$。
> **(iii) その後**に kernel を比較する(settled 判定・§3.3)。

**禁止(R1-b・S-BU-17)**: (iii) の述語(descent / K5-8 / `Aut` への延長可否 / `GroupHomomorphismByImages` の成否 / settled)を **(i)(ii) の絞り込みに使ってはならない**。使うと isolated が false-TRUE になりうる(`auto_settled_check_v1.md` §4 H-5)。
**禁止(H-4)**: $f$ を語のまま列挙してはならない(無重複が壊れる)。

### 3.2 窓ごとの宇宙サイズ(**事前登録**・上界)

各窓の候補数 $=N_{\rm ord}\cdot\lvert[P,P]\rvert\le\lvert P\rvert^2$。L2 全 15 対(30 窓)の上界合計は
$$\sum 2\cdot\lvert P\rvert^2\ \le\ 2\times156{,}618\ =\ 313{,}236\ \text{候補}$$
($\lvert P\rvert$ = 21, 39, 57, 63, 72, 81, 84, 84, 93, 111, 117, 129, 147, 156, 156)。**単一 GAP プロセスで cap 内**。**この上界を超える実測が出たら列挙域の取り違え** ⟹ S-TW-4。

### 3.3 kernel 同定の判定式(fail-closed)

$[m,f]\in\mathfrak S(N)$ に対し $T:=T_{m,f}:B_3\to\widehat P=B_3/N$(hexagon より well-defined 準同型・Prop 3.2)。

| 判定 | 式 | 注意 |
|---|---|---|
| **settled** | $\ker T=N$ $\iff$ (i) $T(N)=1$ かつ (ii) 誘導 $t:\widehat P\to\widehat P$ が全単射(紙 bridge B-2) | (i) を省く実装は不可。GAP なら `GroupHomomorphismByImages` の `fail` を捕まえる。あるいは Reidemeister–Schreier で $N_{F_2}$ の自由生成系 $\{n_1..n_r\}$($r=1+\lvert P\rvert$)を取り $\varphi(n_i)=1$ を全 $i$ で検査 |
| **$\ker T=K$** | (i) $T(k_j)=1$(全生成元)かつ (ii) $\lvert\mathrm{Im}\,T\rvert=[B_3:N]$ | 個数一致・指数一致だけでは不足(定義ノート §4-3 の source kernel 証明書規律) |
| **それ以外** | $\ker T\notin\{N,K\}$ | 登録外 kernel。**捨てずに記録**(§5.3 分岐 (iv)) |

**整合性検査(無料・命題 1.5 torsor)**: $\lvert GT(N)\rvert=\lvert G_N\rvert\cdot\#\{K':\mathrm{GTSh}(K',N)\ne\emptyset\}$。列挙した source kernel の異なり数 × $\lvert G_N\rvert$ が $\lvert GT(N)\rvert$ に一致しなければ列挙が壊れている ⟹ S-TW-4。

### 3.4 出力 cert(schema・発火前に固定)

`search/certs/twin_witness_v1_<date>.json`:
```
{ prereg_doc_sha256, census_cert_sha256, setdigest_L2,
  group_side: "Phat = B3/N (order = index); P = PB3/N (order = index/6)",
  enumeration_domain: "group_elements",
  descent_filter_used_in_enumeration: false,          # R1-b 宣言(source-map 検査つき)
  per_window: [ { window_uid, index, P_order, N_ord, commutator_order,
                  candidates_total, hexagon_pass, charming_pass, shadow_count,
                  mirror_class: "M0|M1|M2", iota_image_uid,
                  kernels: [ {source_kernel_uid|"OFF_REGISTER", count} ],
                  settled_count, nonsettled_count, isolated_verdict: "TRUE|FALSE|UNKNOWN",
                  canary_minus1_hexagon_pass: true } ],
  second_system: { name, language, shares_helper_with_gap: false, agreement: [...] },
  grade: "candidate / cross-checked / not verified (no Lean)" }
```

---

## 4. 二系統要件(scope ④)

### 4.1 三つの経路(**どれか一つでは candidate 止まり**)

| 経路 | 内容 | 何を独立に担保するか |
|---|---|---|
| **系統 A** | GAP(既存 helper 使用可): §2.5 の $\iota$ 判定 + §3 の悉皆 | 主計算 |
| **系統 B** | **python/node の MC-1 再検査器**(§2.7)。**GAP helper 非共有・群論ライブラリ不使用・置換の積と語評価のみ**(BFS で位数を数える) | 主計算と**データ構造も言語も共有しない**再計算。R4 の「第二 enumerator/checker」 |
| **紙** | §2.2(shadow 性・kernel = $\iota(N)$)+ §2.3/§2.4(判定の finite 化と障害) | **鏡映経路では機械依存が $\iota(N)\ne N$ という 1 ビットに縮む**。そのビットも MC-1 の 3 点検査で閉じる ⟹ R4 の「同値な独立紙証明」 |

**格の規律**: 系統 A+B 一致 = **cross-checked**(verified ではない — Lean 不使用)。`isolated_verdict=FALSE`(計算出力)と `iso_gate_state`(格)を混同しない(R5)。

### 4.2 ★ $\lvert GT(N)\rvert$ と $\lvert GT(K)\rvert$ の差について(**明記事項**)

> ### 命題 TWIN-CARD(candidate・本票。命題 1.5(torsor・`wall_design_audit_v1.md` §1.5)の系)
> $$\boxed{\ \mathrm{GTSh}(K,N)\ne\emptyset\ \Longrightarrow\ \lvert GT(N)\rvert=\lvert GT(K)\rvert\ }$$
> **証明.** $\mathrm{GTSh}(K,N)\ne\emptyset$ なら $N,K$ は同一連結成分 $\mathcal C$ にある。命題 1.5 より $\lvert GT(N)\rvert=\lvert G_N\rvert\cdot\lvert\mathcal C\rvert$、$\lvert GT(K)\rvert=\lvert G_K\rvert\cdot\lvert\mathcal C\rvert$($\mathcal C$ は両者で同じ対象集合)。任意の $\varphi\in\mathrm{GTSh}(K,N)$ による共役 $g\mapsto\varphi^{-1}\circ g\circ\varphi$ が $G_N\cong G_K$ を与える。∎

したがって:

| 観測 | 正しい読み |
|---|---|
| $\lvert GT(N)\rvert\ne\lvert GT(K)\rvert$ | ★ **両方向とも空**($\mathrm{GTSh}(K,N)=\mathrm{GTSh}(N,K)=\emptyset$)の**証明**。witness の**不在**を示す。「差分元が証人候補」は**誤り** |
| $\lvert GT(N)\rvert=\lvert GT(K)\rvert$ | **無情報**。同一成分の必要条件にすぎない |
| いずれの場合も | $$\boxed{\ \textbf{witness は「}\ker T_{m,f}=K\ne N\ \textbf{なる明示の }[m,f]\ \textbf{」以外にありえない}\ }$$ 個数比較・位数比較・$\lvert GT\rvert$ 差はいずれも witness ではない |

> **発案札 2【TWIN-DIFF】への訂正(candidate)**: 札 2 (J-ii) は「$\lvert GT(N)\rvert$ vs $\lvert GT(K)\rvert$ の差 ⟹ 痩せた側の差分元が非算術証人候補」と設計していたが、TWIN-CARD により**差が出るのは両方向が空のとき**であり、そこには差動増幅すべき対応がない。**差動の意味は逆**(差 = 成分が別・witness 不在の証明)。なお札 2 (J-i) の「鏡映で移る対は差動ゼロ」という見立ては TWIN-CARD と整合するが、**鏡映対を捨ててはならない**(F110-2.1 逐語: AS-GAP-6 では鏡映対こそ最安の陽性候補)。

---

## 5. 出力規則(scope ⑤・**文言を発火前に固定**)

### 5.1 witness 無しの場合(**この文言以外を書かない**)

> **「$\iota$ 分類および悉皆列挙の結果、本票 §1 で登録した directed pair 群(L2 の 15 対 = 30 directed)において、非 settled GT-shadow は**未発見**である。」**

**禁止語(書いたら S-TW-3)**:
- 「AS-GAP-6 の witness は存在しない」「非 isolated 窓は無い」(**非存在の証明ではない**)
- 「AUTO-SETTLED」「全 shadow は settled」(裁定 528 で無条件偽と確定済)
- 「$B_3$ 窓は鏡映を除き一意」等の剛性主張(登録宇宙は指数 $\le1000$・L2 限定 — D-2)
- L3(13 対)や L0 の残り 146 対についての TRUE/FALSE(M-ISO-6 違反)

**書いてよい付随事実**: 各窓の $\mathfrak S(N)$ の実測個数・$N_{\rm ord}$・$\lvert[P,P]\rvert$・鏡映類 M0/M1/M2 の内訳・torsor 整合(§3.3)の成否。

### 5.2 witness 有りの場合 — M-ISO-2 充足経路への接続

witness $(N,K,[m,f])$ が §2.6 の 4 点(または §3 の悉皆)+ 二系統一致で確定したとき、**次の順に**接続する。

| 段 | 内容 | 参照 |
|---|---|---|
| **①** | **M-ISO-2 の実物 fixture 登録**: 「既知 non-isolated 陰性」= 窓 $N$、期待値 `isolated_verdict = FALSE`。★ **fixture の shadow は charming+SURJ を満たす真の GT-shadow である**(h11-fail 候補が失格だった理由 = Def 3.7 の全射性欠如 — A.2)。$[-1,1]$ は (SURJ) を恒等的に満たす ⟹ **A.2 の要求を正面から満たす** | v4 §5.3 / `auto_settled_check_v1.md` A.2 |
| **②** | **M-ISO-3(constant-TRUE)が同時に discharge される**(M-ISO-2 で落ちるから)。**M-ISO-4**(settled 1 件反転)の期待値 FALSE も、この窓で初めて**偽側の実行**になる | v4 §5.3 |
| **③** | **R3(mutant 6 件)**の残り(M-ISO-1/5/6)と合わせて matrix を閉じる。**R1**(interface + B-1)と **R2**(B-2)は既に紙で証明済 ⟹ 残るは **R4(第二系統)= §4.1 系統 B** と **R5(格分離)** | v4 §5.1–5.5 |
| **④** | **aggregate receipt**: R1〜R5 の 5 件を**一つの受領書**にまとめ、各項に (a) 根拠文書 sha256 (b) cert path+sha (c) 二系統一致の実測 (d) 格(candidate / cross-checked / not verified)を併記。**`iso_gate_state=PROVEN` はここで初めて請求可能**(CV-9 判読を経ること) | v4 §5.5 / 裁定 543 |
| **⑤** | **【AS-GAP-6】の状態更新**を裁定請求(UNKNOWN → 閉)。同時に **W-5 の `UNKNOWN (pending route-2 gate)` は不変**(F104-2.3 逐語)であることを明記 | `p1_ratification_bundle_v1.md` |

**★ ④ に必ず載せる限定文(先に固定)**:
> 「本 witness は**算術元**($[-1,1]$ = 複素共役)であり、**非算術証人(B 型)ではない**。本件が閉じるのは M-ISO-2(settled 述語が FALSE を返せることの実証)であって、FAKE-VOID・非算術証人の存在/非存在には一切触れない。」

### 5.3 分岐表(**発火前に全分岐の扱いを固定**)

| # | 観測 | 処理 |
|---|---|---|
| (i) | L2 に M1(鏡映対)が 1 件以上 | §2.6 の 4 点 → 二系統 → §5.2 へ。**最小指数の対を第一 witness とする**(126 番・`b6b8a3feb9d2`) |
| (ii) | L2 が全て M0、悉皆で非 settled shadow 発見 | 同じく §5.2 へ(witness は $[-1,1]$ ではない別の $[m,f]$ — **より強い結果**: 鏡映で説明できない非 isolated) |
| (iii) | L2 が全て M0、悉皆でも非 settled ゼロ | §5.1 の文言。**追加で記録**: 「L2 の 15 対は $\iota$-不変であり、双子性は鏡映以外の起源をもつ」= 一級の構造観測(negative でも領土) |
| (iv) | $\ker T\notin\{N,K\}$(登録外 kernel) | **witness としては有効**(窓 $N$ は登録内)。ただし directed pair が登録外 ⟹ 「登録窓から到達した**登録外 directed pair**」と明記し、**同時に O-1/D-1 の破れの可能性**として census 再検分を起票(S-TW-7) |
| (v) | 二系統が食い違う | **witness を主張しない**。差分を cert に記録し、CV-9 型の非当事者判読(falsifier)へ回す(裁定 543 の手順) |
| (vi) | §7 の予言が外れる(予言 YES の窓で M0 が出る) | **STOP**(S-TW-6/7)。補題 MIRROR-SHADOW / MIRROR-CRIT / ABEL-INDEX のどれかが偽か、規約・実装が壊れている。**先に紙を疑い、次に規約カナリアを見る** |

---

## 6. 停止規則(発火前に登録)

| # | trigger | verdict |
|---|---|---|
| **S-TW-1** | 列挙段(§3.1 (i)(ii))で descent / settled / kernel / `Aut` 延長 / hom 構成の成否を使った(source-map 検査で検出) | `ENUMERATION_FILTER_CONTAMINATION / STOP`(= S-BU-17) |
| **S-TW-2** | $f$ を語のまま列挙した / 判定式の積を GAP 順で書いた(規約 W-4 違反) | `CONVENTION_VIOLATION / STOP` |
| **S-TW-3** | 出力に §5.1 の禁止語が現れた(AS-GAP-6 非存在・AUTO-SETTLED・剛性主張・L3 への TRUE/FALSE) | `OVERCLAIM / STOP` |
| **S-TW-4** | 候補数が §3.2 の上界を超える、または torsor 整合(§3.3)が破れる | `ENUMERATION_BROKEN / STOP` |
| **S-TW-5** | 片方向のみ非空($\mathrm{GTSh}(K,N)\ne\emptyset$ かつ $\mathrm{GTSh}(N,K)=\emptyset$)が実測された | `GROUPOID_INCONSISTENCY / STOP`(逆射 (3.54) と矛盾 ⟹ 実装 bug の強い信号) |
| **S-TW-6** | **規約カナリア失敗**: いずれかの窓で $[-1,1]$ が hexagon を通らない | `CANARY_FAIL / STOP`(§2.2。$[-1,1]$ は全窓で通らねばならない) |
| **S-TW-7** | M2 が出た / §7 の予言 YES の窓で M0 が出た | `PREREG_PREDICTION_FALSIFIED / STOP`(census 完全性か本票の補題かを特定するまで再開しない) |

---

## 7. 予言(**candidate・値から**・§2.4 の紙補題による)

各窓は $\lvert P\rvert=$ 指数$/6$。ABEL-INDEX($P$ 可換 ⟹ $\lvert P\rvert\in\{n^2,3n^2\}$)と MIRROR-OBSTRUCTION を当てる。

| # | 指数 | $\lvert P\rvert$ | 紙の推論 | **予言** |
|---|---|---|---|---|
| 1 | 126 | $21=3\cdot7$ | $21\notin\{n^2,3n^2\}$ ⟹ $P$ 非可換 ⟹ 位数 $3p$ 非可換 $\Rightarrow P\cong C_7\rtimes C_3$(Frobenius, $q=3$ 奇)⟹ 系 (c) | **$\iota(N)\ne N$ = M1** |
| 2 | 234 | $39=3\cdot13$ | 同上($C_{13}\rtimes C_3$) | **M1** |
| 3 | 342 | $57=3\cdot19$ | 同上 | **M1** |
| 4 | 378 | $63=3^2\cdot7$ | $63\notin\{n^2,3n^2\}$ ⟹ 非可換。Sylow$_7=C_7$ 正規(唯一)⟹ 特性。$\mu(P)\le\gcd(9,6)=3$。$\mu(P)=1$ なら $P=C_7\times(\text{位数 }9)$ = 可換で矛盾 ⟹ $\mu(P)=C_3$ ⟹ 系 (b) | **M1** |
| 5 | 432 | $72$ | 非可換($72\notin\{n^2,3n^2\}$)。特性巡回部分群が紙で押さえられない | **UNKNOWN** |
| 6 | 486 | $81=9^2$ | ABEL-INDEX 不決($81=9^2$)。$\widehat P$ の構造 `((C9:C9):C3):C2` は $P$ 非可換を示唆(candidate) | **UNKNOWN** |
| 7 | 504 | $84$ | 非可換。Sylow$_7$ 特性巡回だが $\mu(P)$ の 3-part が紙で未定 | **UNKNOWN** |
| 8 | 504 | $84$ | 同上 | **UNKNOWN** |
| 9 | 558 | $93=3\cdot31$ | #1 と同型の推論 | **M1** |
| 10 | 666 | $111=3\cdot37$ | 同上 | **M1** |
| 11 | 702 | $117=3^2\cdot13$ | #4 と同型の推論(Sylow$_{13}$ 特性・$\mu(P)=C_3$) | **M1** |
| 12 | 774 | $129=3\cdot43$ | #1 と同型 | **M1** |
| 13 | 882 | $147=3\cdot7^2$ | ABEL-INDEX 不決($147=3\cdot7^2$) | **UNKNOWN** |
| 14 | 936 | $156$ | 非可換。$\mu(P)$ の 3-part 未定 | **UNKNOWN** |
| 15 | 936 | $156$ | 同上 | **UNKNOWN** |

**登録する予言(反証可能な形)**:

> - **P-1**: #1,2,3,4,9,10,11,12 の **8 対 16 窓は M1**(鏡映対)であり、$[-1,1]$ が非 settled shadow になる。⟹ **AS-GAP-6 の witness が最小指数 126 で得られる。**
> - **P-2**: **M2 はゼロ**(O-1 の完全マッチング + D-1)。
> - **P-3**: M1 の窓では **両方向が同時に非空**、かつ $\lvert GT(N)\rvert=\lvert GT(K)\rvert$(TWIN-CARD)、かつ source kernel の異なり数 $\ge2$。
> - **P-4**(弱い予想・candidate): 残り 7 対のうち #6(486)・#13(882)は $\widehat P$ の構造記述から $P$ 非可換で、Sylow の特性巡回部分群経由で M1 になる見込みがある。#5(432)・#7,8(504)・#14,15(936)は判断材料なし(50/50)。
> - **P-5**(外れたら STOP): 予言 M1 の窓で M0 が出たら S-TW-7。**先に §2.2 の規約カナリアを見る**(カナリアが落ちていれば実装、通っていれば紙の補題を疑う)。

**予言の位置づけ**: P-1 は「値からの推測」ではなく**紙の証明**である(census が与える 3 事実 — 指数・$N\le PB_3$・$c\in N$ — を入力とする)。ゆえに本走は **予言の検証 = 実質的な第三の系統**として働く。**機械が P-1 に反したら、機械か census を疑うのが先。**

---

## 8. 【GAP】・規律・novelty

### 8.1 【GAP】(本票で埋められなかった穴)

| # | 内容 | 状態 |
|---|---|---|
| **【TW-GAP-1】** | 補題 MIRROR-SHADOW / MIRROR-CRIT / ABEL-INDEX / TWIN-CARD は **candidate**(Sol 監査未了)。TWIN-CARD は既在の命題 1.5(これも candidate)に依存 | Sol 監査待ち |
| **【TW-GAP-2】** | §2.4 系 (b) の「$\mathrm{Aut}(A)$ 可換」前件は $A$ 巡回で満たすが、$\lvert P\rvert\in\{72,81,84,147,156\}$ の窓では**適切な $A$ を紙で特定できていない** | UNKNOWN(機械で決着) |
| **【TW-GAP-3】** | $c\notin N$(L3)への紙経路の延長は**原理的に可能**だが、現 checker の前件外。**【要裁定 T-1】**(§1.5) | 未起票 → 本票で起票 |
| **【TW-GAP-4】** | 「$[-1,1]$ = $\mathrm{Ih}_N$(複素共役)」は Ihara ICM(印字 106)に依拠する既在の読み。**本票の witness 性はこれを使っていない**(使うのは §2.2 の $B_3$ 内恒等式のみ)ので、この帰属が仮に誤っても witness は無傷 | 分離済 |
| **【TW-GAP-5】** | 副線 2106.06645 §5.2 の $D_{5,0}$ 窓は「not settled・連結成分の対象がちょうど 2 個・$\lvert GT^\heartsuit\rvert=16$」= **正典(副線)内の非 settled 実例**。ただし $B_4$ 系(pentagon あり・同名別物)であり、**M-ISO-2 の fixture には使えない**(移送不可・H-3) | 参考(別系) |

### 8.2 規律申告

- **宇宙の事前登録**: §1 で固定(L2 = 15 対 / 30 directed / SETDIGEST 記載)。**後から広げない**(広げる場合は v2 を新規登録)。
- **UNKNOWN は一級**: §7 の 7 対、【TW-GAP-2】、L3 全体。
- **格**: 本票の全補題は candidate。実行後も **cross-checked が上限**(Lean 不使用 ⟹ verified と呼ばない)。**genuine 性・非算術性には一切触れない。**
- **封印非接触**: 封印 3 量・705,894 対宇宙・kill 定理・$\mathrm{Im}\,R$ に触れていない。$u$ の記号は本票では $u:=2m+1$ の意味でのみ使用(封印記号と別物)。
- **文献ゲート**: 外部文献の新規参照ゼロ。Dyer–Grossman は §2.1 で**使わない形に分離済**(既在の `wall_design_audit_v1.md` §6.2 の処理を踏襲)。**文献要請は出さない。**

### 8.3 novelty grep(実施済)

| 語 | 結果 |
|---|---|
| `MIRROR` / `MIRROR-CRIT` / `MIRROR-OBSTRUCTION` / `ABEL-INDEX` / `TWIN-CARD` | **0 hit**(全て本票が初出) |
| `鏡映` | 既出(`wall_design_audit_v1.md` §6・発案札 2 ほか)。**$[-1,1]$ との接続・shadow 性・非 isolated 判定は未出** |
| `Out(B₃)` / `Dyer` | 既出(`wall_design_audit_v1.md` §6.2・裁定 152/161・発案札 2)。**本票は完全性主張を使わない** |
| 「複素共役」 | 既出(`bhunt_prereg_iffirst_v1.md`: Ihara ICM $\chi(\iota)=-1,f_\iota=1$)。**$\ker T_{-1,1}=\iota(N)$ は未出** |
| `GTSh(K,N)` | 定義(定義ノート §2)と Prop 3.8 のみ。**濃度の等式(TWIN-CARD)は未出**(命題 1.5 = torsor は既在) |
| `A_2 格子` / `Eisenstein` / `$n^2$ or $3n^2$` | **0 hit** |

**既在への帰属**: ι の初等的性質・transport 命題 6.3・ι-固定族 命題 6.6・torsor 命題 1.5 = `docs/notes/wall_design_audit_v1.md`(工房既在)。鏡映を AS-GAP-6 の陽性候補として使う着想 = **Sol F110-2.1**。双子 census = 裁定 548 W-1。差動発案 = 発案係 札 2(§4.2 で訂正)。

---

## 9. 実行チェックリスト(発火時にこの順で)

1. 本票の sha256 を cert の `prereg_doc_sha256` に書く(**本票のコミット後に確定**)。
2. census cert の sha256 と SETDIGEST L2 を再計算し §1 と一致を確認(不一致なら STOP)。
3. **規約カナリア**($[-1,1]$ の hexagon)を全 30 窓で先に走らせる(S-TW-6)。
4. §2.5 の鏡映分類(28 対 56 member)→ M0/M1/M2 を確定。
5. M1 があれば §2.6 の 4 点 → §2.7 MC-1 生成 → 系統 B で再検査。
6. M0 の窓に §3 の悉皆(R1-b 順序厳守・source-map 検査つき)。
7. torsor 整合(§3.3)を全窓で確認。
8. §5 の文言規則に従って結論を書く。§7 の予言との突合表を必ず添える。

---

> ### 発火前単独コミット済み
> 本票は **twin witness 検査の発火(鏡映分類・悉皆列挙・kernel 比較)に先立ち、単独コミットされた**(F110-2.1 scope ① 逐語「発火前の単独 prereg」)。
> 本票のコミット時点で実行済みの機械は §規律申告の 2 本(census cert からの登録集合抽出・$B_3$ 内恒等式の検算)のみであり、**登録集合のどの窓に対しても $\iota$ の計算・shadow の列挙・kernel の比較は行っていない**。
