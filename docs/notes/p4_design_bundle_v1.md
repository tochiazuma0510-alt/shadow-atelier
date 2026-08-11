# P4 設計束 v1 — CRT-ENTANGLE / W691-EXT / CMP-REP-1(裁定 834・便 115 同梱用監査請求)

**状態札: `candidate 設計札 3 枚 / 発案係(ideator)起草 / 新規実行ゼロ(設計のみ・走行中の W691 目撃者探索は入力として参照)/ Sol 未監査(本束が監査請求)/ 数学者検分 = v1.3 後 / 封印非接触 / 判定語なし / EXHAUST 準拠(「唯一」は網羅根拠つきのみ)/ P4-0(L_gen/L_sat 分離・格子比較)には触れない — 前提として引用のみ`**

- 委嘱: 裁定 834。仕様正本 = `sol/sol_reply_114_phase2_hunt_audit.md` P4-1/P4-2/P4-3(逐語準拠)。確定事項 = 裁定 829(GEN23-DET・目撃者方式・2688 全単射)〜833(v1.3 前哨)。文献 pin = `docs/scout/delta_mod23_dihedral_verbatim_v1.md`。
- **DOMAIN-PIN 強化列**(全予言に付す): 述語 / 関手(source→target)/ 比較射 / chi_semantics / factor_filter・落とした因子 / **陽含意** / **陰含意**。

---

# 札 P4-1: CRT-ENTANGLE 設計(実験列順位 1 — proxy なしで定義どおりの反例に届く唯一の既知経路)

## 1.1 対象と観測量(Sol 仕様の逐語形)

二窓 $N_1,N_2\trianglelefteq B_3$(算術較正済み・非自明共通商)、$N=N_1\cap N_2$、
$$X=\mathrm{im}\bigl(GT(N)\to GT(N_1)\times GT(N_2)\bigr),\qquad A=\mathrm{im}\bigl(G_\mathbb Q\to GT(N_1)\times GT(N_2)\bigr)\ (\textbf{同時像})$$
**観測量 = $X\setminus A$(fiber-product compatibility)。座標ごとの全射性ではない**(B114-2 の反模型 $C_2\times C_2$/対角を試金石として設計に内蔵)。

- **カナリア(定理)**: $A\subseteq X$($\gamma\in G_\mathbb Q$ は $N$-窓に影を持ち、その射影が対を与える)。破れ = 実装/意味論エラーで STOP。
- **陽性の意味**: $X\setminus A\ne\emptyset$ ⟹ $N$ 上の genuine 影で「両座標を同時に算術実現できない」もの ⟹ **窓 $N$ での非全射の定義どおりの証人候補**(前件 = 両窓の較正が完全であること — 選定基準 S1)。

## 1.2 選定基準(S1〜S3)と候補窓対(既存 census/registry から・**網羅主張はしない** — 現時点の較正済み在庫からの列挙)

**S1(較正)**: 各 $N_i$ 単独の算術像が cross-checked 以上で確定していること(A の決定に必須)。**S2(非自明共通商)**: $E:=B_3/(N_1N_2)\ne1$(Goursat の绞りが立つ)。**S3(交わりの実在)**: $GT(N)$ が測定済みか測定可能($[B_3:N]\le\lvert G_1\rvert\cdot\lvert G_2\rvert/\lvert E\rvert$)。

| 候補対 | S1 | S2 | S3 | 費用見積り |
|---|---|---|---|---|
| **(a) 本命: $K^{(9)}\times N_{S4}$(= 972 屋根 $M=K^{(9)}\cap N_{S4}$)** | $K^{(9)}$: 定理 U-11($\Theta_9\cong\mathrm{Aff}(\mathbb Z/9)\times C_2$)/ $N_{S4}$: 1 ビット帰着(ord$[u^{-1}]_9$)— **較正状態は registry で要確認・部分較正なら条件付き走** | subdirect 構造は E1 正典ノートの Goursat 分析で既知 | ★ $\lvert GT(M)\rvert=972$ **測定済**(二経路二環境・P-IHN 系)| **表結合+A の fiber-product 計算のみ = implementer 時間単位**(新走行ほぼゼロ) |
| **(b) $K^{(9)}\times K^{(12)}$(奇×混合・帯 0「K⁽¹²⁾ 交叉」領有済)** | 両側 dihedral 系定理で較正済(FAM-U/MIX 系) | 共通商 = 3-水準 | 交叉 cert の再読で立つ見込み | cert 再読+小計算 |
| **(c) 鏡映対 $N\times\iota(N)$(census 双子から)** | ι-対の算術は witness $[-1,1]$ 系で部分較正 | 商同型 = 共通商大 | 交わり指数は対ごと | 中(選定後見積り) |

**推奨**: (a) を第一走(全部品が既測定・費用最小)。(b) を第二走(dihedral 純系 = A の決定が定理で閉じる最良の対照)。

## 1.3 手続き(4 段・実行は監査後)

1. **X の厳密列挙**: $GT(N)$ の cert(972 屋根なら既存)から制限写像 $R_{N,N_i}$(2405 の関手性)で対を生成 — 全列挙・重複除去。
2. **A の決定**: $A_i$ = 各窓の算術像(S1 の定理/測定)。$A=\{(R_{L}(\gamma\text{-data}))\}$ = **$A_1\times_{\,\mathrm{Gal}(L_1\cap L_2)}A_2$ の Goursat fiber-product**(共通体 $L_1\cap L_2$ 上の両立 — 円分 λ-座標の一致条件が最初の絞り・以降は共通商 $E$ 上の像の一致)。**比較射 = 制限関手 $R$(2405 Rem 1.5)** — 新規の射は導入しない。
3. **差集合**: $\lvert X\rvert,\lvert A\rvert,\lvert X\setminus A\rvert$ を報告(判定語なし)。
4. 陽性時は QUAR 型検疫(独立再構成・両座標の genuine 再検査)を経てから報告。

## 1.4 DOMAIN-PIN 表(凍結案)

| 述語 | 関手 | 比較射 | chi_semantics | factor_filter/落とした因子 | 陽含意 | 陰含意 |
|---|---|---|---|---|---|---|
| P-CRT-0(カナリア): $A\subseteq X$ | $GT(-)$: 窓→有限集合 | $R_{N,N_i}$ | n/a | なし(全列挙) | — | 破れ = STOP(実装/意味論) |
| P-CRT-1: 対 (a) で $X\setminus A=\emptyset$ | 同上 | 同上 | n/a | なし | **非空 = 窓 $M$ の非全射証人候補**(検疫へ・S1 前件条件付き) | 空 = 「対 (a) の範囲で entanglement 両立」— **扉 2 はこの対に限り閉**(全域閉鎖は主張しない・EXHAUST) |
| P-CRT-2: $X$ の各射影の全射性(データとして記録) | 同上 | 同上 | n/a | — | 記録のみ(B114-2 の教訓 = 全射性は判定に使わない) | 同左 |

**リスク**: (a) の $N_{S4}$ 側較正が「1 ビット帰着まで」の場合、$A$ は上界としてしか決まらない ⟹ その場合の報告語は「$X\setminus A_{\rm ub}$」で凍結(過大主張防止)。$GT(N)$ の genuine 述語と積側述語の整合(CV-9 型)は falsifier 判読を 1 回挟む。

---

# 札 P4-2: W691-EXT 設計(四段・p=23 control 先行の二段構え)

## 2.0 旧 `pair_h2_design_draft_v1.md` の再利用/破棄の明示(Sol 指摘の履行)

| 部品 | 判定 |
|---|---|
| Sylow-691 縮約($v_{691}=1$ ⟹ $\dim H^2\le1$+安定性文字計算)| ★ **再利用**(段 2 の計算法の核) |
| 実現判定 2 条件($[\varepsilon]\ne0\wedge\varphi^*[\varepsilon]=0$ ⟹ 既約 $W$ で持ち上げ全射は自動)| ★ **再利用**(段 3 の論理) |
| Fox 計算による $H^2(B_3,W)$・Shapiro 帰着・RIBET-SECTION 整合の精密文(固有直線非正規)| ★ **再利用** |
| λ-捻り Burau($\det=-1$・$c\mapsto I$ の 2 恒等式)| **限定再利用**: $H_2$ 枝への braid 対供給ルートの一つ(「強制」ではない) |
| **det=±1 剛性**(係数と作用群が唯一に絞れるという枠)| ★ **破棄**(B114-4: CHI-DICHOTOMY は弱形のみ — 一般形 $\{\chi,\delta\chi^{-1}\}$・$\dim\ge3$ 未排除)|
| Design A/B の二枝で「(C) 全体」を語る枠 | ★ **破棄**(Sol: 二件が空でも (C) 閉鎖にならない — 本設計は**層別台帳**に置換)|

## 2.1 段 1 — 候補 $(H,W)$ の分類(EXHAUST 準拠の層別)

**凍結スコープ**: $p=691$・$W$ の固有指標対が**フル位数 690** を含む場合(χ¹¹ 運搬の定義域)。層別台帳:

| 層 | 分類 | 格 |
|---|---|---|
| **$\dim W=2$・分裂トーラス元(位数 690)あり** | ★ **網羅済(導出鎖)**: SL 非包含なら Dickson 分類(Borel/Cartan 正規化群/例外 $A_4S_4A_5$/部分体型)— 順に (2,3)-生成不能(Borel: 生成トーラス $\le C_6$ / $N(T)$: $w$-剰余類は全対合 ⟹ $\langle$対合,3$\rangle\le D_6$ / 例外: 690-元なし / 部分体: 素体ゆえ空)⟹ **$H\supseteq\mathrm{SL}$ が強制** ⟹ GEN23-DET($D\subseteq\mu_6\wedge\lvert D\rvert$ 偶)⟹ $\boxed{H\in\{H_2=\mathrm{SL}^\pm,\ H_6\}}$ — **2 群で網羅**(前提 pin: Dickson 分類・消去補題 4 本は数学者検分項)。$W$ = 自然加群とその det-捻り $W\otimes\det^i$($i\bmod\lvert D\rvert$ — **$\le8$ 本の有限列挙**)+双対(自然と同型か機械確認) | candidate(消去補題 vet 待ち) |
| **$\dim W=2$・非分裂トーラス** | **空**(位数 $q+1=692$・$690\nmid692$ ⟹ 690-元なし)| 導出(1 行) |
| **$\dim W\ge3$** | ★ **OPEN と登録**(閉鎖主張なし — B114-4 準拠)。着手条件 = 段 2-3 の機械が $\dim2$ で較正済みになったとき、$\mathrm{Sym}^2$ 型から | UNKNOWN |
| **固有指標位数 $<690$** | スコープ外(別の扉 — 本設計は χ¹¹ 定義域に限定)| 凍結 |

**braid 対の存在**(段 3 の前件): 走行中の W691-GEN23 目撃者探索($H_2/H_6$・seed 固定・上限 2000)が供給。$z=(aba)^2\in\{\pm I\}$ の両枝を記録($z=I$ 枝 = c∈N・2688 全単射の 691 版/$z=-I$ 枝 = 存否自体が新データ)。

## 2.2 段 2 — $H^2(H,W)$ の拡大類列挙(計算法と規模)

- **方法**: $v_{691}(\lvert H\rvert)=1$ ⟹ Syl $=C_{691}$(単巾)⟹ $H^2(C_{691},W)$ は Jordan ブロックで 1 次元 ⟹ **$\dim H^2(H,W\otimes\det^i)\in\{0,1\}$ が定理** — 決定は安定元(Borel トーラスの $H^2$-直線への指標が自明か)= **文字計算(紙半頁+検算スクリプト・秒)**。det-捻り $i$ は指標を $\det^i$ 分シフト ⟹ **$i$-列挙で非零になる $i$ の完全リスト**が出る(≤8 本 ⟹ EXHAUST ✓)。
- **二系統**: 直接(安定元)と Shapiro 経由($W\vert$ 誘導形のとき)の一致を必須カナリア。
- **規模**: 全て紙+秒。GHA 不要。

## 2.3 段 3 — braid lift 判定($\langle\tilde\sigma_1,\tilde\sigma_2\rangle=E$)

- 目撃者 $\varphi:B_3\twoheadrightarrow H$ ごとに $\varphi^*[\varepsilon]\in H^2(B_3,W)$(one-relator Fox 計算 mod 691・秒)。**非分裂類**: $[\varepsilon]\ne0\wedge\varphi^*[\varepsilon]=0$ ⟹ 持ち上げは全て全射(既約 $W$ の補群論法)⟹ $\langle\tilde\sigma_1,\tilde\sigma_2\rangle=E$ **自動**。**分裂類**($E=W\rtimes H$): 持ち上げ族は $Z^1(B_3,W)$-torsor ⟹ 全射持ち上げの存否は導分掃引(次元 = $\dim H^0+\dim H^2$ の小空間・秒)で決定的に判定。
- 出力: 類ごとの (実現/障害/分裂実現) の三値表。**判定は決定的計算のみ**(乱択は目撃者探索に限る — 829 の哲学)。

## 2.4 段 4 — 算術 marking(**p=23 control で較正してから 691**)

**二段構え(Sol 助言)**:
- **Control C1(陰性・p=23)**: $\Delta\bmod23$ の像(dihedral・`delta_mod23_dihedral_verbatim_v1.md` pin 済)。dihedral は (2,3)-生成不能 ⟹ **段 3 が正しく棄却することの fail-closed 較正**+段 4 の marking 機構を**既知の算術**(pin 済の $\tau(\ell)\bmod23$ 分岐則 = $\mathbb Q(\sqrt{-23})$ の分解型)に対して較正 — marking の読みが文献値を再現するかの検温。
- **Control C2(陽性・p=23)**: $\mathrm{SL}^\pm(2,23)$ で四段を端から端まで通す(全て極小規模)— パイプライン完走の実証。
- **本走(p=691)**: marking 観測量(凍結): (m1) 実現切片 $W\subset E$ 上のトーラス固有指標対の指数(円分マーキングに対する相対値 — **$k-1=11$ の座標はここに住む**: 固有指標の指数対が $\omega$-正規化で $\{11,-11\}$ 型かの判定)・(m2) 小素数 $\ell$ の Frobenius 指紋($\mathrm{tr}$ の合同型 vs Eisenstein 型 $1+\ell^{11}$)・(m3) 拡大類の非分裂性の算術対応(**対応射の構成は設計課題と明示** — P4-0 の比較射問題と同族だが別対象・ここでは観測量の凍結まで)。

## 2.5 DOMAIN-PIN 表(凍結案・抜粋)

| 述語 | 関手 | 比較射 | chi_semantics | factor_filter | 陽含意 | 陰含意 |
|---|---|---|---|---|---|---|
| P-W691-1: $H_2/H_6$ の目撃者存在 | — | — | n/a(群) | — | 段 2 へ進む | 両群不能 = $\dim2$ 層の (C) 道が**この層で**閉(全域閉鎖は言わない) |
| P-W691-2: $\dim H^2(H,W\otimes\det^i)$ の $i$-完全リスト | $H^2(H,-)$ | 安定元 vs Shapiro(二系統) | **切片読み**(拡大核として) | 落とした因子なし(≤8 本全列挙) | 非零 $i$ あり = 容器候補 | 全零 = **この層で非分裂容器なし**(層限定) |
| P-W691-3: 非零類の braid 実現 | $\varphi^*$ | $H^2(H,W)\to H^2(B_3,W)$ | 切片読み | z-枝別記録 | ★ 実現 = **切片読みの χ¹¹ 対運搬の初実例** ⟹ 段 4 へ | 障害 = この $(\varphi,[\varepsilon])$ 対で不能(目撃者複数で掃く — 有限個) |
| P-W691-4(control): C1 棄却・C2 完走・marking が pin 値再現 | — | — | — | — | 較正成立 | 破れ = パイプライン STOP |

---

# 札 P4-3: CMP-REP-1 設計(正準関手 $V_p(N)=N/[N,N]N^p$・二段凍結)

## 3.1 関手と第一段の計算法($M_5$, $p=11$)

- **関手**: $V_p(N)=N/[N,N]N^p$、$G=B_3/N$ が共役で作用(Sol 提示の正準最小候補・source = 窓の圏、target = $\mathbf F_p[G]$-加群)。**「抽象加群の全列挙は無意味」の教訓を設計原理に**: 測るのは**この関手の値**のみ。
- **計算法**($[B_3:M_5]=3240$): 被覆の胞体複体 $\mathbf F_{11}[G]\xrightarrow{\partial_2=\mathrm{Fox}(r)}\mathbf F_{11}[G]^2\xrightarrow{\partial_1}\mathbf F_{11}[G]$(one-relator・正則表現で $3240\times6480$ 級の疎行列)から $V_{11}(M_5)\cong\ker\partial_1/\mathrm{im}\,\partial_2$。**規模 = ローカル分オーダー**(F₁₁ 線形代数・GHA 不要)。二系統: GAP の Reidemeister–Schreier 経由 `AbelianInvariants` mod 11 と突合。
- **第一段の凍結問い(表現段)**: 位数 10 の指標 $\chi$($G\twoheadrightarrow C_{10}\hookrightarrow\mathbf F_{11}^\times$・**φ(10)=4 本を全列挙**)の各々について、重複度 $m_\chi:=\dim e_\chi V_{11}(M_5)$($e_\chi$ = 1 次元指標の等型射影子)。**予言は置かない(真の UNKNOWN 測定)** — 含意のみ凍結(下表)。

## 3.2 第二段 — 比較射の候補定式化(**未定義部は設計課題と明示**)

- **候補**: 窓 $N$ に付随する被覆(dessin/曲線模型)の étale $H_1$ と $V_p(N)$ の比較 — 図式
  $$c_N:\ H_1^{\text{ét}}(\text{被覆};\mathbf F_p)(\text{円分捻り})\ \longrightarrow\ V_p(N)\quad(\text{$N$ に関手的・}G_\mathbb Q\text{-同変})$$
  で、**問い = $\chi$-等型成分への像が非零か**。source の $G_\mathbb Q$-作用は工房の算術計器(κ/Kummer 橋系・S4 窓の曲線模型)が既知部分を供給。
- **★ 設計課題(明示)**: $c_N$ の正確な構成(位相 $H_1$ と群論 $V_p$ の同一視の正規化・捻りの規約)は**未定義** — P4-0 の比較射問題と同じ型の欠落であり、本札は (i) source/target/自然性の要求仕様 (ii) 構成候補 2 案(被覆の胞体同一視経由/Alexander 加群の Galois 化経由)の列挙まで。構成の採否は数学者+Sol。
- **拡張プロトコル**(Sol 末行の履行): 別関手(tangent/cohomology)を採る場合は同 4 点(source・target・自然性・算術比較射)の固定を必須とする、を規約行として登録。

## 3.3 DOMAIN-PIN 表(凍結案)

| 述語 | 関手 | 比較射 | chi_semantics | factor_filter | 陽含意 | 陰含意 |
|---|---|---|---|---|---|---|
| **P-CMP-1a**(表現段): $m_\chi$($\chi$ 位数 10・4 本全て) | $V_{11}(-)$ | なし(関手の値) | ★ **表現読み**(明記 — 切片主張はしない) | 等型射影の全指標列挙(落とし なし) | $m_\chi>0$ = **容器の実在**(この関手上・非算術 shadow とは**しない**) | $m_\chi=0$(全 4 本)= **この関手上の (B) 道が $M_5,p=11$ で閉**(関手限定・全域主張なし) |
| **P-CMP-1b**(比較段): $c_N$ の $\chi$-成分像 $\ne0$ | $V_{11}$×étale $H_1$ | $c_N$(**構成 = 設計課題**) | 表現読み | — | 非零 = 算術がこの容器に配管される(なお container 止まり) | 零 = 配管なし(容器あれど算術は流れず) |

---

## 束末尾 — 三札共通の規律・費用総括・帰属

- **費用総括**(全て監査後の実行想定・新規実行なし): P4-1(a) = implementer 時間単位(表結合中心)/ P4-2 = control 込みで分〜時間(GHA 不要)/ P4-3 第一段 = ローカル分。
- **共通規律**: EXHAUST(網羅主張は導出鎖 or 全列挙つきのみ・OPEN 層は台帳に残す)・chi_semantics 必記・cert に factor_filter と落とした因子の $\lvert G/C_G\rvert$ 併記(813⑪)・判定は決定的計算のみ(乱択は探索限定)・陽性は QUAR 検疫後に報告。
- **novelty grep 申告**: P-CRT-*/P-W691-*/P-CMP-1a/1b・層別台帳・消去補題 4 本 = repo 0 hit。972 屋根・U-11・K⁽¹²⁾交叉・GEN23-DET・2688 全単射・Sylow 縮約・実現 2 条件 = 既在(引用)。**「唯一」の使用は 2 箇所**(P4-1 の「唯一の既知経路」= Sol の逐語引用・§2.1 の $H\in\{H_2,H_6\}$ = 導出鎖つき)— EXHAUST 準拠を自己点検済。
- **帰属**: 仕様 = Sol(P4-1/2/3)・GEN23-DET/目撃者方式 = 数学者(裁定 829)・B114-2 反模型/B114-4 弱形化/[750,6] 実例 = Sol+falsifier・旧 pair_h2 の再利用部品 = 発案係(本束で明示仕分け)。本束の新規部分 = 候補窓対 3 家族と 972 屋根の即用性・層別台帳と消去補題 4 本の導出鎖・det-捻り $i$-列挙の EXHAUST 化・control C1/C2 の陰陽二面較正・$V_{11}(M_5)$ の胞体複体計算法と二系統・比較射 2 候補案の要求仕様化・DOMAIN-PIN 強化表 3 枚。
