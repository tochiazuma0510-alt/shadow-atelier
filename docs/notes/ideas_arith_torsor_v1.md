# 発案便 — 普遍性×トーサーの統一 v1(AT-1〜AT-5)

作成: 発案係(ideator)/ 2026-08-13
**帰属**: **研究者発案 7 号「普遍性×トーサーの統一」(裁定 1085・優先時刻 = 同裁定)・プロンプト = 研究者(「手術の普遍性にトーサー分解を加えて説明することって出来る?」)・統一像の定式化 = 司令塔**(窓の圏上の三層 settled(−) ↪ GT(−) ↠ C(−)・手術 = 列全体への自然変換・反例探索の二座標分解・【算術部分トーサー両立】)。本便はその candidate 札への開発。
入力 = `ideas_set_surgery_v1.md`(I-SET-1〜5・裁定 1082)・`set_surgery_fixture_v1_20260813.json`(裁定 1084: #C([1008,521]¹)=2・類サイズ [24,24]・均質分離・捻り生存 raw 値)・`settled_grp_proof_v1.md`(SETTLED-GRP・COMP-E・§6 条件つき閉鎖)・`iso_family_lemma_v1.md`(SETTLE-AUTO・ISO-RIGID)・`settled_layer_verdict_v1.md`(settled(N′)≅C₂・f_c 1 ビット・|a_{N′}|≥30,360)・`surg_universality_audit_v1.md`(U-2 検分・(T1) 前件・U-5)・定義ノート L153-182((3.53)(3.54)(3.60)・Prop 3.8/3.14・Cor 5.4・Thm 5.2)・`ihnec_v1.md` §B.2(isolated poset の有向性)。

**規律申告**: 全札 **candidate**(定理口調禁止・「定理候補」は全て条件つき・採否は司令塔専権)。$u$/$c$ 非接触(f_c は settled_layer_verdict 既出のビット構造のみ・値には触れない)・封印 3 量(K⁽⁵⁾ インスタンス)非接触・prereg 量(d₉・r)非計算・**W-48 遵守**(83 窓 fixture から $N'$ への言及は全て外挿ラベルつき)・Sol 未監査・verified ではない。
**新規性 grep 済**: 「部分トーサー/sub-torsor/subtorsor」= **0 hit**。「S_arith/C_arith/算術核類」= 0 hit。「量子化」= 別対象のみ(pent_settled_cent の中心化群値・旧 E2 の obstruction 分類 — 算術像の類単位計数への使用 0)。「二座標」= E2 系の座標計算のみ(本用法 0)。「Lagrange」= **isolated 窓では既出**(week3-J設計: |GT(J)| は 144 の約数)— 本便の新規分は**非 isolated 窓への一般化**であり isolated 退化は既知と明記。「genuine = 全細分に survive」= **Cor 5.4 そのもの(新規でない・引用)**。「König/逆極限非空」= 地図軸 (iv)・ihnec §B.2・e1_canonical 既出(機構は既在 — 本便は**類単位への適用**が新規分)。「Q-STAB/EXSEQ-STAB」= Sol 便の EXSEQ-STAB は楕円曲線系の別対象(名前衝突なしを確認・本便は Q-STAB を使用)。

---

## 総括(1 段落)

裁定 1085 の中核【算術部分トーサー両立】を分解した結果、それは算術の神秘ではなく、**「isolated 細分 $M\le N$ の部分群 $G\le GT(M)$ の reduction 押し出し $R_{M,N}(G)$ は、核類ごとに量子化される」という一般補題 1 本(札 1・SUBTOR)の $G=a_M(G_\mathbf Q)$ への特殊化**である見込みが立った — 証明スケルトンの部品は全て在庫(COMP-E・SETTLE-AUTO・SETTLED-GRP §3.4 の逆元技法の $Q_M$ 版)で、残る前件は (AT-a) $\mathcal{PR}_N$ の錐分解(= I-SET-3 一手目 (i) と**同一の pin**・追加コストゼロ)と I-SET-1 の自由性(数学者 queue 済)のみ。**算術入力はゼロ**(使うのは $\mathrm{Ih}$ が準同型であることだけ)。しかも SUBTOR は $G=GT(M)$ でも回るので、**「R-像の各類 trace は $S_M$-トーサーか空」という機械で今日反証可能な予言**(札 2)が出る — 既存 fixture cert の再集計(u-剰余類検定・GAP 走行ゼロ)と、[1008,521] の $N^\diamond$ 一段掘りの 2 本で装置全体の生死が決まる。成立時の帰結が札 3(二座標分解の命題化: **反例 ⟺ 群側のずれ ∨ 成分側のずれ**・α/β 台帳の座標化・f_c ビットの「c-正準性」精密化)。一方で司令塔の統一像(前層の短完全列)には**実関門が一つある**: settled(−) と C(−) が前層になるには「settled 作用が窓区間 $H/N$ を安定化する」(Q-STAB)が要り、これは自動でない(札 4・修理案 3 本つき)。札 5 は cofinality YES の下での座標の降下列(有限深度で安定・drop 点 = U-5 延長障害の住所)。**正直な会計**: $N'$ 規模では計数装置(I-SET-2 の類計数拡張)が別途要る点は不変 — 本便が買うのは「何を数えれば反例が出るか」の**座標の確定**と、fixture 規模での**即時の反証テコ**である。

---

## 札 AT-1 — 一般補題 SUBTOR: 【算術部分トーサー両立】の最小条件への分解(中核)

**規模**: 中間峰級 / **出所**: 正典 (3.53)(3.60) + SETTLED-GRP §3.4 の証明技法の再利用(工房内在庫の組み合わせ)/ **種**: 予想(条件つき定理候補・証明戦略同梱)

**1. 主張の種**: $M\le N$・$M$ isolated(Prop 3.14 で常に存在)・$G\le GT(M)$ 部分群とし、$X:=R_{M,N}(G)\subseteq GT(N)$、$S_X:=X\cap GT^{\rm settled}(N)$ とおく。
> **【補題候補 SUBTOR】** (i) $S_X\le GT^{\rm settled}(N)$ は部分群(非空: $R(1)=[0,1]$・有限閉性)。(ii) $X$ は $S_X$ の後合成作用で閉じる。(iii) 同一核類の $t,t'\in X$ は $S_X$ の元で移り合う。⟹ **各核類 $K$ で $X\cap GTSh(K,N)$ は $S_X$-トーサーか空**(自由性は I-SET-1 から継承・それ抜きでも「推移的 $S_X$-集合 ⟹ サイズは $|S_X|$ の約数」の弱形が残る)⟹ $|X|=|S_X|\cdot\#\mathcal C_X$。

> **【系 = 発案 7 の中核】** $G=a_M(G_\mathbf Q)$($=\mathcal{PR}_M\circ\mathrm{Ih}$ の像・$M$ isolated では群準同型の像 = 部分群)とすれば、**(AT-a) の下で** $a_N(G_\mathbf Q)=R_{M,N}(a_M(G_\mathbf Q))$ となり【算術部分トーサー両立】が従う: $S_{\rm arith}:=a_N(G_\mathbf Q)\cap GT^{\rm settled}(N)$ は部分群・**各核類の算術点は $S_{\rm arith}$-トーサーか空**・$|a_N(G_\mathbf Q)|=|S_{\rm arith}|\cdot\#\mathcal C_{\rm arith}(N)$。

**最小条件の同定**(発注 1 への回答): 必要なのは次の 3 つ**だけ**で、G_ℚ 固有の入力はゼロ:
- **(AT-a) 錐分解**: $\mathcal{PR}_N=R_{M,N}\circ\mathcal{PR}_M$(選択独立性込み)。**I-SET-3 一手目 (i) と同一の pin** — 数学者 queue 済・追加コストゼロ。ここだけが正典逐語の未確認点。
- **(AT-b) 代表元水準の乗法性**: $R(s\cdot t)=R(s)\circ R(t)$・$R(1)=1$ — (3.53) は $\mathbf Z\times F_2$ の代表元で計算される式なので、COMP-E と「$N_{\rm ord}\mid M_{\rm ord}$・$M_{F_2}\subseteq N_{F_2}$」の truncation 可換で機械的に出る見込み(演習級・要逐語)。
- **(AT-d) 同核差の settled 性**: $t=R(T),t'=R(T')$ 同核 ⟹ $d:=R(T'T^{-1})$ は settled。**証明スケッチ(5 行・SETTLED-GRP §3.4 の $Q_M$ 版)**: $M$ isolated ⟹ $T,D:=T'T^{-1}$ は $Q_M$ 上へ降りて $\bar e_T,\bar e_D\in\mathrm{Aut}(Q_M)$(SETTLE-AUTO)。$\bar K:=K_{F_2}/M_{F_2}$、$\bar N:=N_{F_2}/M_{F_2}$ とすると同核性から $\bar K=\bar e_T^{-1}(\bar N)$ かつ $\bar K=(\bar e_D\bar e_T)^{-1}(\bar N)$ ⟹ **全単射ゆえ** $\bar e_D(\bar N)=\bar N$ ⟹ $d$ は well_defined ⟹(R は shadow を shadow に送る (3.60)+ SETTLE-AUTO)settled。∎候補
  — 前件の効き所: **「isolated ⟹ 降りた写像が自己同型」の全単射性**が逆像の等式を押し返す。ここが SG-GAP-1 型の単射性(窓依存)を**回避**している点(単射性は $Q_M$ 側でしか使わず、SETTLE-AUTO が無償で供給)。
- 推移性 (iii) は (AT-b)(AT-d) から: $d\circ t=R(T'T^{-1}T)=t'$。**窓一般**(発注の問いへ: $N'$ 特化は不要 — $N'$ が効くのは座標の値だけ・札 3)。

**2. 何が新しいか**: 「部分トーサー」語彙・$|a_N|=|S_{\rm arith}|\cdot\#\mathcal C_{\rm arith}$ 型の計数は 0 hit(grep 上記)。isolated 窓では $a_N$ の像が部分群になり Lagrange に退化 — **これは week3-J設計で既出の推論**であり、本札の新規分は「**GT(N) が群でない非 isolated 窓で、なお Lagrange 型の約数法則が(類単位のトーサー構造として)生き残る**」の主張。settled_grp_proof §6 の条件つき閉鎖($a_N^{-1}(1)$ の部分群性 = 核側)の**像側の相棒**であり、あちらの「像が settled 部分に入る範囲で」という条件を「類ごとに全取り(トーサー)か空か」へ精密化する。

**3. 検証の一手目**: 数学者へ紙 1 枚(既送の I-SET-3 三設問便に**同梱可能**): (AT-a) の正典 pin(既 queue)+(AT-b) の逐語化+(AT-d) スケッチの検分(上記 5 行の穴の有無 — 特に「$R$ は shadow を shadow に送る」の (3.60) 逐語と、$\bar K=\bar e_T^{-1}(\bar N)$ の $F_2$/$PB_3$ 水準の混線チェック)。機械の先行検証は札 2(SUBTOR の $G=GT(M)$ 特殊化は fixture で今日反証可能)。

**4. 破綻しそうな点**: ① (AT-a) が折れる(= $\mathcal{PR}_N$ の正典定義が錐分解と不整合・または非 isolated 窓で $a_N$ 自体が未定義)と系が全滅 — ただしその場合も SUBTOR 本体($G=GT(M)$)は無傷で、「算術像」を「R-像」に読み替えた装置(札 2・5)は生きる。② (AT-d) スケッチで $K_{F_2}\supseteq M_{F_2}$ を暗黙に使っている($K\supseteq M$ — $t$ が $R$ の像であることから出るはずだが未逐語)。③ 自由性(I-SET-1)が折れると計数が「約数」に弱まる — 弱形でも量子化法則は残る(破綻ではなく減額)。④ $G_\mathbf Q$ の位相(Ih の連続性・像の閉性)を一切使っていない — 「$a_M(G_\mathbf Q)$ が**部分群**」は $\mathcal{PR}_M\circ\mathrm{Ih}$ が抽象群準同型なら像は部分群なので位相不要のはずだが、正典の $a_M$ が「閉包を取る」定義だと集合がずれる(pin 対象)。

---

## 札 AT-2 — R-trace 量子化: 今日反証可能な 2 つの機械的予言(fixture 即走)

**規模**: 現在線級(装置)/ **出所**: SUBTOR の $G=GT(M)$ 特殊化(値からの推測ではなく構造からの予言)/ **種**: 予想+fixture 設計(発注 2 への回答)

**1. 主張の種**: SUBTOR が正しければ、**算術入力ゼロで**次が成り立つはず — 反証は fixture 1 本で可能:
> **【予言 P1(u-剰余類)】** 各核類上の $u$-多重集合は「settled 群の $u$-集合 $u(S)$ の剰余類」: fiber $=S\circ t_0$ ⟹ $u$-値は $u(S)\cdot u_{t_0}$。**既存 cert(set_surgery_fixture_v1)の再集計だけで検定できる**(GAP 走行ゼロ): [1008,521] の settled 類(24 元)の $u$-集合 $u(S)$ を読み、非 settled 類(rep $m=2$)の $u$-多重集合が $u(S)\cdot 5$($u_{t_0}=2\cdot2+1=5$)に一致するか。
> **【予言 P2(R-trace 量子化)】** $M:=N\cap K_2$($N=[1008,521]^1$・$K_2$ = 1084 cert の第 2 核類の核・$M=N^\diamond$ = 成分 2 対象の交わり・Prop 3.14 で isolated)に対し、$X:=R_{M,N}(GT(M))$ の各類 trace は $|S_M|$($S_M:=X\cap{\rm settled}(N)$・24 の約数)か 0 — **中間サイズが 1 つでも出たら SUBTOR(または I-SET-1)が死ぬ**。同時に #C_R(R-像が当たる類数)∈{1,2} が測れ、**類 2 が外れれば「depth-1 で既に non-genuine な類」の初観測**(Cor 5.4 の類単位版 witness 候補)。

**量子化スペクトル**(発注 2 の受け皿): 成立時、$|a_N(G_\mathbf Q)|$ の可能値は $\{d\cdot k:\ d\mid|{\rm settled}(N)|,\ 1\le k\le\#\mathcal C(N)\}$ に量子化。[1008,521] なら $d\mid24$・$k\le2$。$N'$ なら(**外挿でなく** settled(N′)≅C₂ は確定値): $|a_{N'}|\in\{\#\mathcal C_{\rm arith},\,2\#\mathcal C_{\rm arith}\}$・円分下界(settled_layer_verdict §7.2)から $\#\mathcal C_{\rm arith}\ge15{,}180$ — **I-SET-1 の $\#\mathcal C(N')\ge15{,}180$ と同じ数字が算術側の類数に再登場**する(分母と分子が同じ座標系に乗った、が正確な言い方)。全射性 ⟺ $|S_{\rm arith}|=|{\rm settled}|$ **かつ** $\#\mathcal C_{\rm arith}=\#\mathcal C$。

**2. 何が新しいか**: 1084 cert の均質分離(settled 類 = 全 well_defined/他類 = 全非 well_defined)は SETTLE-AUTO の帰結の確認であって、**P1/P2 はそれより真に強い**(u-剰余類構造・trace の全取りか空か)。「R-像の類単位計数」は 0 hit。83 窓 census に「#C_R」「$|S_M|$」列を足す提案は I-SET-5 持ち帰り資産 (i) の具体化。

**3. 検証の一手目**: implementer 2 段 — (i) **P1: 既存 JSON の再集計**(python 数行・即日)。(ii) **P2: fixture 拡張 1 本**(GAP): $M=N\cap K_2$ を構成(|PB₃/M|≤168²=28,224 — census 機構の射程内見込み・超えたら正直に PARTIAL)→ GT(M) 列挙(isolated 検算 = 全 shadow settled も同時測定)→ (3.60) truncation で 48 元への像を marking → 類別 trace サイズ・$S_M$・#C_R・u-剰余類を cert 化(schema at_fixture/v1・u_touched=false)。

**4. 破綻しそうな点**: ① P1 が落ちる場合、真っ先に疑うべきは SUBTOR でなく **I-SET-1 の自由推移性**(fiber が単一軌道でない)— 切り分けには fiber 内の差 $t'\circ t^{-1}$ の直接計算が要る(同便に含める)。② $M=N\cap K_2$ の isolated 性を Prop 3.14 に頼っているが「成分の全対象 = C(N) の 2 つ」は Prop 3.8 の逆射経由の同一視(§本文)を使った私の導出 — 成分がもっと大きい可能性(要検算・fixture で全 shadow settled を実測するのはこのため)。③ 28,224 は census 実績(168・2916)より一桁大きい — 列挙が届かない場合、P2 は「像の一部サンプリング」に弱体化する(それでも中間サイズ 1 個で反証は成立 — 反証側は無傷)。④ **W-48**: 本 fixture の結果を $N'$ へ運ぶのは外挿(装置の較正であって $N'$ の結論ではない)。

---

## 札 AT-3 — 二座標分解の命題化: 反例 ⟺ 群側のずれ ∨ 成分側のずれ(α/β 台帳の座標化+f_c の精密化)

**規模**: 中間峰級 / **出所**: 裁定 1085 の二座標分解(司令塔)の命題化 + I-SET-3 α/β 弁別との合成 / **種**: 再定式化(発注 3 への回答)

**1. 主張の種**: 三段の包含 $a_N(G_\mathbf Q)\subseteq\mathcal{PR}_N(\widehat{GT}_{\rm gen})\subseteq GT(N)$ の各段が SUBTOR 型の分解を持つ(算術 = 系・genuine = $\mathcal{PR}_M(\widehat{GT})\le GT(M)$ への SUBTOR + 深さ方向の共通部分・全体 = I-SET-1)とすると、**部分群鎖と類集合鎖の対**が立つ:
$$S_{\rm arith}\ \le\ S_{\rm gen}\ \le\ GT^{\rm settled}(N),\qquad \mathcal C_{\rm arith}\ \subseteq\ \mathcal C_{\rm gen}\ \subseteq\ \mathcal C(N)$$
(Lagrange で $|S_{\rm arith}|\,\big|\,|S_{\rm gen}|\,\big|\,|{\rm settled}|$)。このとき:
> **【命題候補 COORD】** 全射性の破れは正確に二座標に分解される —
> **反例あり ⟺ $S_{\rm arith}\lneq{\rm settled}$(群側)∨ $\mathcal C_{\rm arith}\subsetneq\mathcal C$(成分側)**。
> さらに I-SET-3 の α/β が座標で書ける: **α(fake)⟺ $S_{\rm gen}\lneq{\rm settled}$ ∨ $\mathcal C_{\rm gen}\subsetneq\mathcal C$**/**β(genuine 非算術)⟺ $S_{\rm arith}\lneq S_{\rm gen}$ ∨ $\mathcal C_{\rm arith}\subsetneq\mathcal C_{\rm gen}$**。genuine 集合 = 全細分の R-像の共通部分は **Cor 5.4 そのもの**(新規でない)+ isolated 制限で足りること(cofinal+R の推移律・1 行)。
> **【飢餓判定】** 量子化の帰結: 類 $K$ の R-trace が $|S_{\rm arith}|$ 未満なら **$K$ の算術点は空**(全取りか空かの対偶)⟹ $|a_N|\le|S_{\rm arith}|\cdot\#\{K:\ |{\rm trace}_K|\ge|S_{\rm arith}|\}$ — **I-SET-3 の上界 $|a_N|\le|R(GT(M))|$ の類単位の強化**(trace が薄く広がるほど強くなる)。

**$N'$ 特化(settled ≅ C₂ 確定値を代入)**: 群座標は 1 ビット化し、しかも**二重化**する — $g$-bit := 「$[-1,1]\in\mathcal{PR}_{N'}(\widehat{GT})$」(genuine 側・機械寄り)と $a$-bit := 「$[-1,1]\in a_{N'}(G_\mathbf Q)$」(算術側)。settled_layer_verdict の $f_c$ 1 ビットとの正確な関係は:
- $f_c=1\ \Longrightarrow\ a$-bit$=1$(十分条件・[Q4-FINAL] の測定はこちら向き)。
- **逆は未確認**: $a$-bit$=1$ は「∃g: $a_{N'}(g)=[-1,1]$」であり $g=c$ とは限らない ⟹ **【設問 AT-Q1(c-正準性)】** $a$-bit$=1\Rightarrow f_c=1$ か(複素共役に正準化できるか)。トーサー座標の**内在量は $|S_{\rm arith}|$** であり、$f_c$ はその witness 測定という整理。
- $f_c\ne1$ の枝では $a_{N'}(c)$ が非 settled 算術点 ⟹ **$\mathcal C_{\rm arith}$ に非自明類が自動で立つ**(witness の座標が同時に確定する — 弁別の副産物)。

**2. 何が新しいか**: α/β 弁別(I-SET-3)は集合の差の言明で、**部分群鎖+類鎖の座標**は 0 hit。飢餓判定(trace 薄 ⟹ 類ごと空)は「量子化 × reduction 上界」の合成として 0 hit — I-SET-3 が「2 窓のサイズ比較」だったのに対し、**同一窓内で類ごとに発火する**点が形として新しい。$g$/$a$ の 2 ビット分解は settled_layer_verdict §2 の 1 ビットの精密化(粗くなる方向でなく細くなる方向)。

**3. 検証の一手目**: (i) 数学者へ: COORD の言明の型検査(特に $S_{\rm gen}$ の well-defined 性 — 深さ方向の共通部分がトーサー性を保つには I-SET-1 自由性で「差の一意性」が要る、の逐語)+ AT-Q1。(ii) implementer: 札 2 の fixture に「飢餓判定のミニチュア」列を追加(trace と $|S_M|$ の比較だけ・同一走行)。(iii) $g$-bit の無料部分: $[-1,1]$ が K 族全窓で shadow であること(Thm 4.3 で $m=-1\in\mathcal X_n$・$k=0$・$4\mid n$ 追加条件も $\varkappa(-1)=0$ で OK)は**紙 1 行の検算**として数学者便に同梱可(dihedral 塔上で $g$-bit が落ちない、の族的証拠)。

**4. 破綻しそうな点**: ① $S_{\rm gen}$ の構成は「共通部分のトーサー性」に I-SET-1 自由性を本質的に使う — 自由性が弱形に落ちると β の群側座標が「約数の鎖」になり、1 ビットの綺麗さが失われる($N'$ では settled が C₂ なので実害は小さい)。② AT-Q1 は否定的(c-正準化不能)でも装置は無傷だが、[Q4-FINAL] の 1 ビットが「十分条件測定」に格下げされる — settled_layer_verdict の結論文の書き換えが要る(裁定事項)。③ 飢餓判定は (AT-a) 条件つき — 錐分解が折れたら「算術点は R-像に入る」の第一歩が消える。

---

## 札 AT-4 — Q-STAB: 統一像(前層の短完全列)の well-definedness の関門(修理案 3 本つき)

**規模**: 現在線級(だが統一像の土台)/ **出所**: 裁定 1085 の合成観察の精密化(自然性の検算)/ **種**: 反例狙いの設問+装置提案

**1. 主張の種**: 裁定 1085 の「settled(−) ↪ GT(−) ↠ C(−) は窓の圏上の前層の列」には**未確認の前提が 1 つ埋まっている**: reduction $R_{N,H}$($N\le H$)が settled を settled に送ること。計算すると($s$ settled at $N$・$\bar T_s$ = 誘導自己同型):
$$\ker T_{R(s)}=\pi_N^{-1}\bigl(\bar T_s^{-1}(H/N)\bigr)\quad\Longrightarrow\quad R(s)\ \text{settled at}\ H\iff\bar T_s^{-1}(H/N)=H/N$$
> **【設問 Q-STAB】** settled 群の誘導作用は、窓区間 $[N,H]$ の正規部分群 $H/N\subseteq B_3/N$ を安定化するか。**これは自動でない**(自己同型は正規部分群を同型な別物に写し得る)。同じ条件が「類写像 $\mathcal C(N)\to\mathcal C(H)$ の well-defined 性」(= C(−) が前層になること)も支配する(同核の $t'=s\circ t$ の行き先の核が $\bar T_s^{-1}(H/N)$ 経由でずれ得る)。

**十分条件と含意**: $H/N$ が $B_3/N$ 内で「$S_3$-枠(Sol 閉鎖 C83-GAP-1: $\pi\circ T=\pi$)を固定する自己同型」に対し特性的なら YES — これは **ISO-RIGID(iso_family_lemma §4)と同族の rigidity 条件**で、「一意な正規部分群 ⟹ 安定」型。つまり**統一像が前層として立つ範囲 = 窓格子の rigidity が効く範囲**という予想が立つ。重要な救済: **札 1〜3・5 の計数装置は Q-STAB を使わない**(isolated $M$ からの押し出しは源側が全 settled で、類写像の well-defined 性を要求しない)— 関門は「列の自然変換」という**統一像の言葉**にだけ効く。

**修理案(Q-STAB が NO の場合)**: (A) 𝒲 を「安定対 $(N,H)$」の部分圏に制限(I-SET-3/AT 系の用途はこれで足りる)。(B) C(−) を前層でなく**対応(span)**とする(手術 = span の射・言葉は重くなるが嘘がない)。(C) C(N) を settled-誘導作用の軌道で粗化した $\bar{\mathcal C}(N)$ に取り替える(無条件に関手化するが計数が粗くなる — I-SET-2 の指標計数との整合は要再設計)。

**2. 何が新しいか**: 「前層の短完全列」は裁定 1085(司令塔)の言葉 — 本札の新規分は**その well-definedness が Q-STAB という具体的な群論条件に同値であることの摘出**と修理案。0 hit(「類写像」の既出は Sol 便 power-class map = 別対象)。統一像の検分でここが最初に突かれる見込みが高く、**先に自分で言っておく**のが本札の主目的。

**3. 検証の一手目**: implementer(安い・独立走行可): [1008,521] を**源**にし、粗い側 $H$ を作って測る — $B_3/N$(位数 1008)の正規部分群で $PB_3/N$(位数 168)内の最小非自明なものを 1 つ取り $H$ とする(構成は GAP 数行)→ 48 shadow を $R_{N,H}$ で落とし、(a) settled 24 元の像が settled か(Q-STAB 直接検定)(b) 2 類の行き先の類が類ごとに一定か(類写像の well-defined 性)を全数測定。どちらに転んでも一級(YES なら統一像の最初の族的証拠・NO なら修理案の選定材料)。

**4. 破綻しそうな点**: ① $\ker T_{R(s)}$ の計算で $T_{R(s)}=\pi_{N,H}\circ T_s$ を使った — (3.60) の座標 truncation と両立するはず(同じ語の粗い商)だが逐語未確認。② 一つの $H$ での YES は Q-STAB の証明ではない(区間ごとの条件)— 族で立てるには rigidity 側(ISO-RIGID の語彙)からの紙が要る。③ 修理案 (C) の粗化は、settled 作用が**各 fiber を保つ**(核を変えない)事実と混線しやすい — Q-STAB の作用は「reduction 先の核」への作用であり fiber 内の作用ではない(型注意を明記)。

---

## 札 AT-5 — 降下座標列: cofinality の下で二座標は有限深度で安定する(fake 侵入深度の局在)

**規模**: 中間峰級 / **出所**: Thm 5.2+Prop 3.14(cofinality YES)と SUBTOR の合成 / **種**: 予想+観測装置(発注 5 への回答)

**1. 主張の種**: isolated 細分の降下列 $M_1\ge M_2\ge\cdots$($\le N$・有向性は ihnec §B.2)に沿って、測定可能な座標対
$$d\ \longmapsto\ \bigl(\,S_{M_d}:=R_{M_d,N}(GT(M_d))\cap{\rm settled}(N),\ \ \mathcal C_{R,d}:=\text{R-像が当たる類集合}\,\bigr)$$
は**単調減少**(R の推移律で像は入れ子)で、値域が有限ゆえ**有限深度で安定**し、安定値は genuine 座標 $(S_{\rm gen},\mathcal C_{\rm gen})$ に一致する(Cor 5.4 + König 型持ち上げ — 機構は地図軸 (iv) 既在)。
> **【観測装置 DESCENT】** 座標対の**降下プロファイル**(どの深さで何が落ちるか)は非 isolated 窓の新しい不変量: **群座標の drop = settled 元の非 genuine 化の深度**・**成分座標の drop = 類の fake 化の深度**。U-5(延長障害)の語で言えば、drop 事象 = 延長障害の発火点であり、**「fake がどの細分段で塔に入れなくなるか」の住所録**になる。安定深度は一般に非効果的(UNKNOWN 一級)だが、**各有限段が既に正当な上界**なので測った分だけ使える。
> $N'$ の具体錨(外挿でない部分): dihedral 塔上では $[-1,1]$ は全段 shadow(札 3 一手目 (iii))⟹ **K 族に沿う群座標ビットは落ちない**(candidate)。83 窓の非 isolated 窓でどの深さから落ち始めるかが、fixture で測れる最初の降下プロファイル。

**2. 何が新しいか**: 「共通部分 = genuine」は Cor 5.4(引用)。新規分は ① 座標対としての単調安定化(自明だが 0 hit)② **プロファイルを窓の不変量として登録する提案** ③ U-5 との結線(U-5 は「(T1) 全射なら dihedral 族内で空振り」— 本装置は空振りの**外側**、非 isolated 窓で U-5 の照準を類単位に引き継ぐ)。

**3. 検証の一手目**: 札 2 の fixture(depth-1)がそのまま第 1 点。第 2 点は $M'\le M=N^\diamond$ の一段深掘り(候補: $M':=M^{\diamond\text{-of-}M}$ でなく、census 在庫の細分があるか ops 在庫検査から — 深掘りの窓構成は司令塔裁定事項)。プロファイルの器(cert schema に depth 列)だけ先に切っておく。

**4. 破綻しそうな点**: ① 「安定値 = genuine 座標」の証明は共通部分のトーサー性(札 3 破綻点 ①と同じ自由性依存)。② 深掘りは指数的に高くなる(28,224 → その平方) — 実際に測れるのは depth 1〜2 の見込みで、「プロファイル」は当面 2 点列(正直な規模申告)。③ K 族の錨は $c\in K^{(n)}$ の世界・83 窓は $c\notin N$・$N'$ は $c\in N'$ — 三者の橋渡しは全て**外挿ラベル必須**(W-48)。

---

## 付記 — 札間の結線と発火順の推薦(採否は司令塔)

- **結線**: 札 1(SUBTOR)が唯一の土台。札 2 はその機械検定(反証テコ)・札 3 は成立時の意味論(座標)・札 4 は統一像の言葉の関門(計数装置からは独立)・札 5 は深さ方向の延長。**単一障害点は札 1 の (AT-a) と I-SET-1 自由性** — どちらも既に数学者 queue にある pin と同一物で、**本便が新たに要求する数学者往復は実質ゼロ**(同梱 3 行: (AT-b)(AT-d) 検分・AT-Q1・$[-1,1]$ K 族 1 行)。
- **発火順の推薦**: ① **P1 再集計**(既存 JSON・python 数行・即日・GAP ゼロ)— 落ちたらこの時点で全札を再設計に回す(最安の検死)。② 札 4 の粗化検定(源 = 既列挙 48 元・GAP 数行)— 統一像の生死を先に見る。③ 札 2 の $N^\diamond$ fixture(28k 規模・PARTIAL 許容)。④ 数学者便(既送 I-SET 三設問と同便化: (AT-a) 共有 pin+(AT-b)(AT-d)+AT-Q1+K 族 1 行)。⑤ 結果を見て札 5 の depth-2 と $N'$ 向け計数拡張(I-SET-2 との合流)の GO/NO-GO。
- **正直な総括**: 本便は算術の代金(SURG-A6)を 1 円も安くしない — $f_c$ の 1 ビットと receipt の調達は従来どおり有料。買うのは **(a) 【算術部分トーサー両立】の「算術入力ゼロの一般補題+2 つの pin」への縮約**(検証可能性の確定)**(b) 今日走る反証テコ 2 本**(P1/P2 — SUBTOR が偽なら安く早く死ぬ)**(c) 反例探索の座標系**(反例 ⟺ 群側 ∨ 成分側・α/β・飢餓判定)**(d) 統一像の関門の事前摘出**(Q-STAB)。研究者発案 7 号の核心「トーサーで説明できるか」への現時点の答えは — **説明できる見込みが高く、しかも説明は算術より一段手前(reduction の押し出しの一般論)に住んでいる。ただし前層としての統一像には Q-STAB という実関門が一つあり、そこだけは群論の rigidity が代金を払う** — である。
