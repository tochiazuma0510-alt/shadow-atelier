# 発案札 — R3【S4-ORDER / S4-RAM-SUPPORT】攻撃アイデア 7 枚

- 起草: 発案係(ideator)/ 2026-08-12 / 委嘱: 司令塔(裁定 947)
- **格: 全て candidate 札**(証明なし・「機構はこう」まで)。採否は司令塔の専権。UNKNOWN は一級。
- **文脈**: 本日【ISO-S4】発効(candidate / Sol-audited・便 119 P2)⟹ $\rho_{S4}:G_\mathbf Q\to GT(N_{S4})$ が群準同型・$A_{S4},L_{S4},S_{S4}$ が定義され、R3 の二問【ENT-GAP-8 S4-ORDER】【ENT-GAP-7 S4-RAM-SUPPORT】が初めて型として健全になった。
- **標的構造の pin(型事故予防)**: 標的は $GT(N_{S4})\cong\mathrm{Hol}(\mathbf Z/9)$(位数 54・IdGroup [54,6]・`surj_s4_v2.md` §1 の $\Phi$ 全単射 = $N_{\mathrm{P\Gamma L}(2,8)}(\langle X\rangle)$)。**$PSL(2,8)$ は窓の商 $PB_3/N_{S4}$ であって標的群ではない**(TYPE-IMAGE$^\rho$ の (1) 窓 vs 標的の区別・B116-3 の教訓)。$(N_{S4})_{\rm ord}=9$(奇数)ゆえ **$K^{(9)}$ にあった $C_2$ 因子($\chi\bmod4$)が S4 側には無い**。
- **規律遵守**: 撤回済み(v1.4.8 §7 W-1〜47)不使用 — 特に W-47(pro-3 橋)・$u_9=3$・型→算術循環・972 の「空」「首位」。MB whitelist 遵守: $u_{S4}$ の値・平方類の計算・表示・値に基づく選択の提案はしない(blind receipt 設計のみ)。数値確信度なし(序数評価のみ)。

**記号**(本札内): $d_{S4}:=\lvert A_{S4}\cap(\text{translation }\mathbf Z/9)\rvert\in\{1,3,9\}$(ENT-GAP-8 の量)、$d_9$ = K9-ORDER の量(UNKNOWN・K9-COMPOSE は HOLD)、$[x]_9$ = $\mathbf Q^\times/(\mathbf Q^\times)^9$ ないし $\mathbf Q(\zeta_9)^\times/(\mathbf Q(\zeta_9)^\times)^9$ の類。

---

## 札 1【S4-COORD】— $\Theta_{S4}$ 座標明示と cocycle 化(R1 第一波の S4 移植・$C_2$ なしで一段軽い)

- **種**: 構成。**出所**: R1 第一波(`r1_k9_bridge_v1.md`)からの移植。**規模: 現在線級**。
- **機構**: marking $\Theta_{S4}:=\Phi$(`surj_s4_v2` §1 の `phi_bijective` を LOCAL-PIN/MARKING-COMPAT の型で pin)の下で $\Theta_{S4}\circ\rho_{S4}(g)=(t_{S4}(g),\ \chi(g)\bmod9)\in\mathbf Z/9\rtimes(\mathbf Z/9)^\times$。$\mathrm{Hol}(\mathbf Z/9)$ の積則から $t_{S4}(gh)=t_{S4}(g)+\chi(g)t_{S4}(h)$ ⟹ $t_{S4}\in Z^1(G_\mathbf Q,\mu_9)$。Kummer(K9 F3(a)5 と同一論法)⟹ ある $b\in\mathbf Q^\times/(\mathbf Q^\times)^9$ で $L_{S4}=\mathbf Q(\zeta_9,\sqrt[9]{b})$、$d_{S4}=[L_{S4}:\mathbf Q(\zeta_9)]=\mathrm{ord}([b]_9)$。
- **何が新しいか**: $\Phi$ 自体・共変性(Φ-univ)・`phi_bijective` は `surj_s4_v2` に既在。差分 = **$\rho_{S4}$ 発効後の TYPE-IMAGE$^\rho$ 五対象記帳としての座標化**+cocycle/Kummer 帰結+R1 受入 6 項(gate v3 §2.2)の S4 対応表(未起草を grep 確認)。$N_{\rm ord}=9$ 奇数ゆえ**罠 6($L$ vs $L_{\rm Aff}$ 分離)が消える** — K9 より受入条件が 1 項少ない。
- **検証の一手目**: 紙 = 数学者へ「$\mathrm{Hol}(\mathbf Z/9)$ 積則→cocycle の 3 行+有理 radical 降下の K9 論法流用可否」設問。機械 = implementer へ **MARKING-COMPAT-S4 の 54 元全数 cert**($\Phi$(shadow 合成) = 像の積・$\chi_{\rm vir}$ 両立)— 有限群ゆえ**全数検査で閉じられる**(K9 の MARKING-COMPAT より先に閉じ得る = §5 宿題 16 の突破口が S4 側から開く逆転)。
- **破れ方**: $\Phi$ は $\mathrm{Aut}(P)$ 経由の定義で、shadow 合成の向き(op 規約)や 2405 (1.13) の $\chi_{\rm vir}$ 同定と食い違う可能性(54 元検査が落とす)。cocycle 化は $\Theta_{S4}$ の可換性に全依存 — そこが落ちれば本札の下流(札 2〜5・7)は全部条件付きに落ちる。

## 札 2【S4-FULLPRE】— graph 型の排除・$\lvert A_{S4}\rvert=6\,d_{S4}$ 単系統化(K9-FULLPRE の非可換窓移植)

- **種**: 構成。**出所**: K9-FULLPRE(便 119 F3(a) PASS)からの移植。**規模: 現在線級**。
- **機構**: $A_{S4}\le\mathrm{Hol}(\mathbf Z/9)$。(i) $\chi$ 成分への射影は全射(正典 (1.13) の可換図+$\chi\bmod9$ の全射性)。(ii) 複素共役の像 $(t_c,-1)$ は位数 2 元。K9-FULLPRE と同じ「単位射影の全射性+fiber 論法」で、$T_1:=A_{S4}\cap(\mathbf Z/9)\in\{0,\ 3\mathbf Z/9,\ \mathbf Z/9\}$、各 $\chi$-fiber は $T_1$ の剰余類全体 ⟹ $A_{S4}=T_1\rtimes(\mathbf Z/9)^\times$ 形・**graph 型部分群は残らない** ⟹ $\lvert A_{S4}\rvert=6\,d_{S4}$、三枝 $\{6,18,54\}$ が**単系統**に確定。
- **何が新しいか**: `surj_s4_v2` §4 の対応表($\lvert\mathrm{Ih}(G_\mathbf Q)\rvert\in\{6,18,54\}$)は集合像時代+framework-conditional の帰着内の値。差分 = **部分群としての正当化を正典 (1.13)+群論のみで独立に出す**(BFC 枠組に依存しない)。副産物候補 = K9 と S4 を同一補題で処理する **FULLPRE-GEN**($\mathrm{Aff}(\mathbf Z/n)$ 型標的+χ 全射+複素共役 ⟹ graph 排除の窓非依存形)。
- **検証の一手目**: 機械 = GAP で $\mathrm{Hol}(\mathbf Z/9)$ の全部分群 census →「$\chi$-全射部分群はちょうど 3 共役型」の cert(54 位・数秒)。紙 = K9-FULLPRE 証明の $(0,-1)$ を $(t_c,-1)$ に置換して通るかの検分(数学者・1 頁未満)。
- **破れ方**: (1.13) の可換図が S4 窓で立つこと自体が札 1(MARKING-COMPAT-S4)依存 — 依存の向きを取り違えると型→算術循環(U9-RIGID の失敗型)を再演する。$t_c\ne0$ でも fiber 論法は通るはずだが、$(t_c,-1)$ の正規化(inner ambiguity)を消していないと $T_1$ の代表が動く。

## 札 3【S4-RECON / d_{S4}-receipt】— $d_{S4}=\mathrm{ord}([u_{S4}^{-1}]_9)$ 橋の格付け直しと blind ord-receipt(封印プロトコル下)

- **種**: 予想(橋)+装置提案。**出所**: 既存 SURJ-S4 v2 §4 の再接続(工程観察)+K9 P8-value 線の設計流用。**規模: 中間峰級**。
- **機構**: `surj_s4_v2` §4(framework-conditional)は $[L:K]=\mathrm{ord}([u_{S4}^{-1}]_9)\in\{1,3,9\}$・像位数 $\{6,18,54\}$ の表を既に持つ。札 1・2 の座標が立てば **$d_{S4}=\mathrm{ord}([u_{S4}^{-1}]_9)$**(= 札 1 の $[b]_9=[u_{S4}^{-1}]_9$)として R3 の主装置に接続できる。ただし K9 の教訓(M119-5: $d_9=\mathrm{ord}(a_9)$ は比較段を経る)を**先取りして framework-conditional と最初から記帳**する: 前件 = TB1–4+**$(Z_{18}$-link$)$(S4 は inventory 未登録 = `not_assessed`)**+**C1′(S4)**(`c1prime_s4_design_v1.md` の G-1〜: dessin 6 個の同着問題)。装置 = 既設計の測定線 M0–M7 の出力を「$\mathrm{ord}\in\{1,3,9\}$ **のみ**」の blind receipt に落とす(**$u_{S4}$ 値は封印のまま**・K9 の P8-value receipt と同型・Sol 設計承認 F3(f) の先例に相乗り)。
- **何が新しいか**: 表・測定計画とも既在(novelty 申告)。差分 = ①「v2 の $\lvert\mathrm{Ih}\rvert$ 表」と「$A_{S4}$ 部分群の $d_{S4}$」の同一視に札 1・2 が要るという**依存の摘出**(型再検収)②**二窓同時 ord-receipt**($d_9$ と $d_{S4}$ を同一 blind 様式で)③ $d_{S4}\in\{1,3\}$ なら 972 が単独窓事由で自動発火(札 4)= **S4 は Conj 5.1 の族外なので、$d_{S4}<9$ は正典予想と矛盾せずに非全射 witness になり得る**(K9 の $d_9<9$= 大事件との非対称・攻撃価値の根拠)。
- **検証の一手目**: 事務 = $(Z_{18}$-link$)$ の S4 inventory 登録(`not_assessed` 解消)。紙 = C1′(S4) 工程 G-1 の再起動見積り(数学者)。
- **破れ方**: C1′(S4) が閉じない限り「測った $u$」と「表の $u$」の同語が立たない(W92-5 の指摘そのまま)。framework 前件が K9-COMPOSE と同種の HOLD を食らう(そのときは receipt は「予言なし測定」に降格)。

## 札 4【TRIAD-972】— 972 屋根の完全パラメータ化: $\lvert X\setminus A\rvert=972-12\,d_9 d_{S4}/r$・発火 $\iff(d_9,d_{S4},r)\ne(9,9,1)$

- **種**: 構成(縮約定理の候補)。**出所**: Kummer 理論からの構成+COMPOSITUM-ρ(前件 1 発効)。**規模: 中間峰級**。
- **機構**: 札 1 の Kummer 表示($L_{9,\rm Aff}=\mathbf Q(\zeta_9,\sqrt[9]{a})$・$L_{S4}=\mathbf Q(\zeta_9,\sqrt[9]{b})$)の下で $r:=\lvert\langle[a]\rangle\cap\langle[b]\rangle\rvert$(9 乗類群内・$r\mid\gcd(d_9,d_{S4})$)と置くと、Kummer の標準論法で $[L_9L_{S4}:\mathbf Q]=12\,d_9d_{S4}/r$、$q=\lvert Q_A\rvert=[L_9\cap L_{S4}:\mathbf Q]=6r$、$a_1=12d_9$・$a_2=6d_{S4}$。一般式(Sol 批准・§10)に代入して $\boxed{\lvert X\setminus A\rvert=972-12\,d_9d_{S4}/r}$。**発火 $\iff d_9d_{S4}/r<81\iff(d_9,d_{S4},r)\ne(9,9,1)$**。⟹ 972 の問い全体が**整数 3 個**に完全縮約され、**$L_{S4}$ の全情報は不要 — $[b]_9$ の $\langle[a]\rangle$ への従属度 $r$ だけが要る**(委嘱の「$L_{S4}$ の部分情報で足りる形」への回答)。
- **何が新しいか**: 一般式 $972-a_1a_2/q$ は批准済・(b) 分岐表($q=6/18/54\to0/648/864$)は `ideas_ent_targets_v1` に既在。差分 = **$q,a_2$ の Kummer 化・飽和仮定の除去・三整数への縮約**。検算済(機械): $(9,9,r)$ 系列が既存表 0/648/864 を再現・P-ENT-U9(same-$u$)は $r=9$ の特殊ケースとして包含。ENT-GAP-4($Q_A^{\rm lb}$ 構成)は「$r\ge r_0$ の witness 構成」へ再定義される。
- **検証の一手目**: 紙 = 数学者へ 5 行 Kummer 設問($[\mathbf Q(\zeta_9,\sqrt[9]{a},\sqrt[9]{b},i):\mathbf Q]=12d_9d_{S4}/r$ と $q=6r$・下記 2 穴込み)。
- **破れ方**: ① $C_2$ 分離の小穴($i\notin L_{S4}$ は $\mathrm{Gal}(L_{S4}/\mathbf Q)$ の可換化が $\chi\bmod9$ 円分で尽きることから出る見込みだが、$L_9\cap L_{S4}=L_{9,\rm Aff}\cap L_{S4}$ の 1 行は要証明)② Kummer 類の Galois 固有成分($t$ は cocycle であって準同型でない — $[a],[b]$ が同一 $\chi$-固有成分に住むことの確認・PARITY-EIG の向き pin)③ COMPOSITUM-ρ 前件 2($\rho_i=R_i\circ\rho_M$・関手性から出る見込み)と前件 3(CRT-INJ)の検収が未了 — ここが落ちると式ごと HOLD。

## 札 5【S4-RAM 二段化】— RAM-SUPPORT の 972 上の役割 = $r$ の上界制御・P-K9U-1 併用で発火が具体的数論述語に落ちる

- **種**: 予想(構造)。**出所**: 類体論/Kummer 分岐からの類推。**規模: 中間峰級**。
- **機構**: $\sqrt[9]{c}$ の分岐は $\mathrm{supp}(c)\cup\{3\}$ に台をもつ。共有類 $[c]\in\langle[a]\rangle\cap\langle[b]\rangle$ は両体に入るので $\mathrm{supp}(c)\subseteq(\mathrm{supp}(a)\cup\{3\})\cap(\mathrm{supp}(b)\cup\{3\})$。⟹ **分岐台の交差が $\{3\}$ に潰れるなら共有類は 3-unit 類に限定され $r$ が上から絞られる**。RAM-SUPPORT を「$S_{S4}$ それ自体」でなく「**$r$ の上界を与える計器**」として位置づけ直す(972 直結の使い道の同定)。さらに条件付き予言 **P-K9U-1**($a=3$・凍結済)と併用すると: $\boxed{\text{発火}\iff[b]\in\langle[3]\rangle\setminus\{1\}}$($r>1$ 部分)または $d$ 側の退化 — すなわち「$u_{S4}^{-1}$ が 3 の冪 × 9 乗か」という**一個の数論述語**に落ちる。
- **何が新しいか**: ENT-GAP-7 は「support は $\lvert PSL(2,8)\rvert$ から読めない・比較射が要る」の OPEN 宣言で止まっている。差分 = RAM の**下流(972)における正確な役割**の同定と、P-K9U-1 との合成で出る発火述語の明示。K9-KUMMER-SUPP の honest negative(tame では絞れない)とは別問題(こちらは supp を「仮説・条件」として使う設計で、無条件主張をしない)。
- **検証の一手目**: 紙 = 「$\mathrm{supp}$ 交差 $\subseteq\{3\}$ ⟹ 共有類は $\langle[3],[-1]?,[\zeta\text{-unit}]\rangle$ 内」の Kummer 補題(数学者・数行・単数の寄与の精査込み)。機械 = 札 7 の grid で「supp 仮説ごとの $r$ の取り得る値表」を先行計算。
- **破れ方**: $\mathrm{supp}(b)$ を押さえる手段が無ければ片側が開いたまま(それが ENT-GAP-7 本体 — 本札は解消でなく「使い道の固定」)。$\mathbf Q(\zeta_9)$ 水準で考えると円単数・類数の寄与で「3-unit のみ」の限定が甘くなる可能性($\mathbf Q^\times$ 水準に降下できれば消える — 札 1 の有理 radical 降下に依存)。

## 札 6【S4-BECKMANN 比較射】— $L_{S4}\subseteq$(dessin の field of moduli)の橋+Beckmann 型不分岐で $S_{S4}\subseteq\{2,3,7\}$

- **種**: 別分野からの翻訳(regular IGP / field of moduli)+**文献要請**。**規模: 中間峰〜夢級**。
- **機構**: $g\in\ker\rho_{S4}$ は 54 shadow の座標全部を固定 ⟹(C1′(S4) の同一視 $D_W\cong D_{\rm meas}$ を経て)対応する $PSL(2,8)$-dessin(passport $((9),(9),(9))$・6 個)の同型類+marking を固定 ⟹ $L_{S4}\subseteq K_D$(marking 込み field of moduli の合成)。そこで **Beckmann 型定理**($p\nmid\lvert\text{monodromy}\rvert=504$ ⟹ moduli 体は $p$ 不分岐)が使えれば $\boxed{S_{S4}\subseteq\{2,3,7\}}$。副産物: $u_{S4}$ 測定用の厳密モデル $(C,t)$(`c1prime_s4_design_v1` の fibre 積構成)が**そのまま判別式読み出し器**になる — 測定(札 3)と分岐(本札)が同一幾何対象で閉じる一石二鳥。さらに札 5 と合成: $\mathrm{supp}(a)=\{3\}$(P-K9U-1)なら交差 $\subseteq\{3\}$ が**両側から**立ち、$r$ 制限が無条件化へ近づく。
- **何が新しいか**: 「Beckmann 型 moduli 経路の比較射が要る」の一句は v1.4.8 §8 に既在。差分 = **比較射の具体形の提案**($\ker\rho_{S4}\to$ dessin stabilizer・C1′ 資産の転用)+必要文献の特定。**文献要請【BECK-LIT-1】**: Beckmann 1989(または Coombes–Harbater 系)の正確な statement(G-被覆/moduli 体/good reduction の前件)— 文献ゲート経由・司令塔へ。
- **検証の一手目**: 紙 = 「shadow 座標固定 ⟹ dessin 固定」橋の前件洗い出し(数学者・NAME-COLLIDE 6 点表つき: 2106 系 dessin 作用は B₄ 系 = 同名別物リスク)。並行して BECK-LIT-1 発注。
- **破れ方**: B₃-gentle 系の shadow と dessin 作用の対応が正典に無い ⟹ 橋が「翻訳」でなく「新定理」になる(重くなる)。based/outer の差で moduli 体と核体がズレる — **B119-1(K9-UNRAM の失敗)と同型の罠**であり、「文献が見つかった」と「橋が架かった」を混同しないこと(W-47 の教訓の S4 版)。$p=2$ は K9 同様に別段の可能性。

## 札 7【S4-HYPOTHESIS-GRID】— 開封前の発火地形図: supp 仮説下の候補 $[b]$ 有限列挙と $(d_{S4},r,972)$ 全表(機械先行)

- **種**: 装置提案(機械先行)。**出所**: 値からの推測解禁(2026-07-28 裁定)+K9 KUMMER-SUPP の negative を条件付き有限化で回避する設計。**規模: 現在線級**。
- **機構**: 「$\mathrm{supp}(b)\subseteq\{2,3,7\}$」を**明示仮説**として置く(札 6 が立てば定理化・立たなくても fail-closed な作業仮説)と、$[b]$ の候補空間は $\mathbf Q^\times/(\mathbf Q^\times)^9$ の $\{-1,2,3,7\}$-生成部分群 = **有限リスト**。各候補に $(d_{S4}=\mathrm{ord}[b],\ r=\lvert\langle[3]\rangle\cap\langle[b]\rangle\rvert$(P-K9U-1 併用)$,\ 972-12d_9d_{S4}/r)$ を全列挙した**発火地形表を開封前に凍結**。測定(札 3 の receipt)後に一発照合。副産物: 地形の形(発火候補の分布)そのものが「どの測定が判別力最大か」を教える(序数評価のみ・確率は出さない)。
- **何が新しいか**: 該当装置は repo に無い(grep: KUMMER-SUPP は「絞れない」の honest negative で終了・仮説条件付きの有限化+地形表は未着手)。**$u_{S4}$ 封印に非接触**: 候補列挙は公開数学(仮説空間の構造)であり、封印値がどれかは触れない。
- **検証の一手目**: 機械 = implementer へ pari/gp(または GAP)スクリプト: $\mathbf Q^\times/(\mathbf Q^\times)^9$ 内の $\langle[-1],[2],[3],[7]\rangle$ の群構造($\cong(\mathbf Z/9)^3\times\mathbf Z/2$ 程度)と全候補の $(d,r,\text{972 値})$ 表(軽量・8GB 内)。必要なら $\mathbf Q(\zeta_9)$ 水準版(bnfinit・S-unit mod 9 乗・χ-固有成分)を第二段で。
- **破れ方**: supp 仮説が偽なら表は的中しない(ただし「仮説下の地形」として台帳に残る・凍結予言 DOMAIN-PIN 表に仮説を明記すれば fail-closed)。$\mathbf Q(\zeta_9)$ 水準の単数寄与を無視すると候補空間を取りこぼす(第二段で回収)。$d_9$ が UNKNOWN のままなので表は $d_9$ を変数に持つ 2 次元表になる(見かけの複雑化 — 表の軸設計で吸収)。

---

## 依存図(札間・一目)

$$\text{札1 S4-COORD}\ \to\ \text{札2 FULLPRE}\ \to\ \text{札3 RECON/receipt}\ ;\qquad\text{札1}\to\text{札4 TRIAD-972}\ \leftarrow\ \text{札5 RAM二段化}\ \leftarrow\ \text{札6 BECKMANN}\ ;\qquad\text{札7 GRID は札5・6 の仮説を先行消費(独立走行可)}$$

R3 の受入条件の芯(司令塔への提案): R1 の 6 項(gate v3 §2.2)の S4 対応 = **R3-a** $\Theta_{S4}$ pin(札 1)/ **R3-b** (1.13) 可換図(札 1 cert)/ **R3-c** inner ambiguity(K9 と同文)/ **R3-d** 罠 6 は**消滅**($C_2$ 因子なし — 要 1 行確認)/ **R3-e** graph 排除(札 2)/ **R3-f** 分岐は別 GAP(札 5・6)。

## novelty grep 申告

- **既在を確認して引用**: $\Phi$/`phi_bijective`/Φ-univ/W5Q-S4/$\mathfrak F_0\cong C_9$(`surj_s4_v2.md`)・SURJ-S4 の $\mathrm{ord}([u^{-1}]_9)$ 3 枝表(同 §4)・測定計画 M0–M7(同 §5)・C1′(S4) 設計(`c1prime_s4_design_v1.md`)・一般式 $972-a_1a_2/q$(v1.4.8 §10・Sol 批准)・(b) 分岐表 0/648/864・P-ENT-U9(`ideas_ent_targets_v1.md`)・「Beckmann 型」の語(v1.4.8 §8 ENT-GAP-7)・K9-FULLPRE/K9-COORD/P8-value(便 119 F3)・P-K9U-1(凍結 `bd80c44`)。
- **本札初出(repo 0 hit を grep 確認)**: S4-COORD / S4-FULLPRE / S4-RECON / FULLPRE-GEN / TRIAD-972 / 三整数縮約 $(d_9,d_{S4},r)$ と $q=6r$ の Kummer 化 / 「RAM = $r$ の上界計器」の位置づけ / 発火述語「$[b]\in\langle[3]\rangle$」/ BECK-LIT-1 / S4-HYPOTHESIS-GRID / R3 受入 6 項対応表。
- **非接触の確認**: W-30/36(972 の空・canary 格)不使用・W-38(isolated 前の $\rho_{S4}$)は発効済につき非該当・W-40(単純性→isolated)不使用・W-44/45(T63 系の量化)不使用・W-47(pro-3 橋)不使用(札 6 で「同型の罠」として警戒言及のみ)・$u_9=3$/8.5 割/「残り 1 ビット」不使用。$u_{S4}$ の値・平方類に非接触。

## 委嘱項目との対応(1 行ずつ)

- 座標明示の S4 版 → 札 1(+受入 6 項)/ 円分成分の分離 → 札 1・2((1.13) 経由・$C_2$ 消滅の指摘)/ Kummer parametrization の非可換窓での姿 → 札 1(標的は $\mathrm{Hol}(\mathbf Z/9)$ で K9 と同型の座標・「非可換」は窓の商 $PSL(2,8)$ 側に隔離される、が本件の型の答)。
- PSL(2,8) の構造から像位数を絞る路 → 札 2(census は $\mathrm{Hol}(\mathbf Z/9)$ 水準が正しい住所・PSL 側でないことの pin 込み)。
- Thm 1(i) 系の他 ℓ 版 → 直接は張らない(W-47 の教訓: pin と橋は別)。分岐は札 5(役割固定)・札 6(比較射)の二段で。
- 機械で先に測れるもの → 札 2(census cert)・札 7(発火地形)・札 3(blind ord-receipt)。
- 972 直結の最小限 → 札 4: **整数 3 個 $(d_9,d_{S4},r)$・$L_{S4}$ の全体は不要**。
