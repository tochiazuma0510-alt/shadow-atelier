# (F) カード v2.1 — falsifier 逐語との突合(F-GAP-5 閉鎖・裁定 1005)

作成: 数学者(Opus 5)/ 2026-08-12 / 発注 = 司令塔裁定 1005 queue ①
突合対象 = `docs/notes/fals_F_stage1_audit_v1.md`(逐語・事後収蔵)vs `docs/notes/F_card_v2_and_P6_v1.md`(私の再構成)
⚠ 数値出力なし・candidate 格。

---

## §0 判定:**一致ではありません**。差分 9 件(うち★**実質的な訂正 2 件**)

| # | 項 | 判定 |
|---|---|---|
| **D-1** ★★ | **和則**($\dim H^2(H_F,W)+\dim H^2(H_F,W{\otimes}\det)\le\dim H^2(SL,W)\le1$)が私の v2 に無い。逐語は「各々 $\le1$ は**緩すぎる**」と明記 | ★ **実質訂正** |
| **D-2** ★★ | 和則より **(Ad-c) も不可能**。私の v2 は (Ad-c)「両 $i$ で 1 ⟹ 容器 2 つ」を枝として残した | ★ **実質訂正** |
| D-3 | **cal 番号が食い違う**(逐語 cal-1=$(C_{691},W)$/cal-2=本題/cal-3=$\mathfrak{sl}_2$ 和=1/cal-4=$p{=}23$ リハ。私の番号は別物) | 要統一 |
| D-4 | cert 欄の**不足 7 件**(§2.2) | 要追加 |
| D-5 | **P-5(novelty 訂正)を書いていない**。P-PH2-4 = 「$\dim H^2(\bar G,W)\le1$ = 定理」は**既存**で、私の段 1 spec が「新規部分 ②」と申告したのは**過大** | ★ 記帳 |
| D-6 | §C-1 **EXHAUST の 2 段根拠**((i) $H_F^{ab}=C_2$ (ii) 2 次元既約は自然加群のみ)が私の cal-4 に無い | 要追加 |
| D-7 | §C-3 **(u3) は UNKNOWN 枝でなく事前登録項目**。私は UNKNOWN 枝に残した | 要移動 |
| D-8 | §C-6 **二系統(直接 vs Shapiro)が設計に無い** ⟹ 格は candidate 止まり | 要追加 |
| D-9 | §C-8 **撤退条件**(壁時計 cap・`-o 2g`)が無い | 要追加 |

★ **一致した点**: P-1 の紙決着(補題・適用・$H^n=0$)/ 判定枝を Ad へ書き換える方針 / 較正カード化の思想 / R-1 留保維持 / P-6(i)(ii) の数学。
★ **私が逐語より進んでいた点**: P-6(i) の **NARROW 全域閉**(逐語 §F は「分裂トーラス $\mathrm{diag}(a,a^{-1})|_{a=-1}$ の 1 行検算であって定式化への検分ではない — 数学者確認要」と自己申告。私の $SL(2,691)\le H\Rightarrow -I\in H$ が定式化そのものに対する答え)/ cert の `module`・`r_value` 欄。

---

## §1 ★★ 実質訂正 1・2 — 和則と (Ad-c) の削除

### 1.1 和則(逐語 §B-1 後段)
LHS 退化より $H^n(H_F,M)\cong H^n(SL(2,691),M)^{S_3}$。$\det$ は $SL$ 上自明なので $M=W$ と $M=W\otimes\det$ は**同じ $SL$-加群**で、$S_3$-作用が sign だけずれる。$\dim H^2(SL,W)\le1$ ゆえ、1 次元空間の $S_3$-等質分解は**自明成分か sign 成分のどちらか一方**:

$$\boxed{\ \dim H^2(H_F,M)+\dim H^2(H_F,M\otimes\det)\;=\;\dim H^2(SL,M)\;\le\;1\ }$$

### 1.2 ⟹ (Ad-c) も不可能(私の v2 の誤り)
同じ論法が $M=\mathrm{Ad}=\mathfrak{sl}_2$ にそのまま適用されます($\det$ は $SL$ 上自明・$\dim H^2(SL,\mathrm{Ad})\le1$ は私の Sylow 還元)。
⟹ **両 $i$ で 1 は起こり得ない** ⟹ **(Ad-c) は削除**。
★ 逐語 §D の実測表がこれを裏付け: $p=5,7,11,23$ すべてで $(H^2(H_F,\mathfrak{sl}_2),H^2(H_F,\mathfrak{sl}_2{\otimes}\det))=(1,0)$、**和 = 1** ✔

### 1.3 ★★★ ⟹ 段 1′(Ad) は「0 か 1 か」ではなく **1 bit の測定**
$$\boxed{\ \text{和}=\dim H^2(SL,\mathrm{Ad})\in\{0,1\}\ \text{で、実測 4 点すべてで }1\ \Longrightarrow\ \textbf{測る内容は「どちらの }i\ \textbf{か」だけ}\ }$$
⟹ ★ **prereg 可能**: 逐語 §D の $p=5,7,11,23$ が**全て $i=0$ 側**なので、**$i=0$ で 1・$i=1$ で 0** を予言として凍結できます。⟹ 司令塔へ**新規 prereg の起票を上申**します(これは私の v2 に無かった機会)。

---

## §2 差分の埋め合わせ(v2 の該当節を置換)

### 2.1 判定枝(v2 §3 を置換)
| 枝 | 条件 | 帰結 |
|---|---|---|
| **(Ad-a)** | 和 $=0$ | ✘ $\mathrm{Ad}$ 層にも容器なし ⟹ ③ 線を閉じる |
| **(Ad-b)** ★ | 和 $=1$、非零は $i=i_0$ | ★ 段 2 入口が実在。$i_0$ が**予言($i_0=0$)と一致するか**を記録 |
| ~~(Ad-c)~~ | — | ★ **削除**(和則により不可能・§1.2) |
| **STOP** | 和 $\ge2$ または両方非零 | ⚠ 理論と矛盾 ⟹ 即停止(群/加群/器具の誤用を疑う) |
| **事前登録項目**(UNKNOWN 枝ではない) | $S_3$ 作用の持ち上げ・向き・$W$ の基底・$\det$ の $\mathbf F_{691}^\times$ への埋め込み | ★ **計算前に pin**(逐語 §C-3・CV-9 的危険) |
⚠ いずれでも **「窓資格」は結論しない**(段 2/3/4 が残る)。⚠ **R-1 留保は維持**。

### 2.2 cert schema(v2 §5.1 を置換 = 逐語 P-4 ∪ 私の追加)
```
★ 逐語 P-4 由来(私の v2 に欠けていた 7 件)
  positive_control_cal1, positive_control_cal3   (裁定 961)
  group_fingerprint : {|H_F|, |H_F^ab|, |Z(H_F)|, 合成因子, 生成系ハッシュ}
        ★ |H_F| = |H_6| の NAME-COLLIDE 対策 — 位数だけでは同定にならない
  s3_action_variant : 捻りごと 2 欄(1 欄では必ずどちらかが誤記される)
  method            : exact_linear_algebra | stable_elements | paper_lemma
  bound_violated    : bool   ★ dim は「0 or 1」型で縛らず非負整数+この bool
  r1_reservation    : "unproven(型 vs 実像・段 4 未閉)"  ★ 必須欄(下流テンプレが必ず引く)
  tool_version, input_hash, wall_clock_ms, cap_ms
★ 私の v2 由来(逐語に無く、残すべきもの)
  module   : "Ad" | "W"        (型境界)
  r_value  : 690 (W 層) | 345 (Ad 層)   ★「満額と容器は両立しない」がカードの心臓
  central_lemma_fires : bool
  lhs_degenerate      : bool
★ 新規(§1.3)
  sum_rule_value : dim H^2(H_F,M) + dim H^2(H_F,M⊗det)   ★ 本当の fail-closed 不変量
  i0_predicted : 0   /  i0_observed : 0|1                 ★ 1 bit prereg
```

### 2.3 cal スイート(逐語の番号に統一・v2 §2 を置換)
```
[cal-1] (C_691, W)                       予言 dim H^2 = 1   陽性対照(Sylow 層)
[cal-2] (H_F, W), (H_F, W⊗det)           予言 0, 0          本題(紙で決着済)
[cal-3] (H_F, sl_2), (H_F, sl_2⊗det)     予言 和 = 1        陽性対照(SL 層+S_3 層を貫通)
[cal-4] p=23 リハーサル(全 3 本)          予言 0/0, 和 1     実測済(逐語 §D)
不変量 assert: dim H^2(H_F,W) + dim H^2(H_F,W⊗det) <= dim H^2(SL,W) <= 1
1 本でも外れたら UNKNOWN + STOP(MISS ではない)
```
⟹ ★ 私の旧 cal-3(LHS 退化検定)・旧 cal-4(twist 網羅)は**番号を譲り**、下記 §2.4 の EXHAUST 根拠に統合します。

### 2.4 EXHAUST の 2 段根拠(逐語 §C-1・私の cal-4 の不足を補う)
1. $H_F^{ab}=C_2$ かつ 691 奇 ⟹ $\mathrm{Hom}(H_F,\mathbf F_{691}^\times)=\{1,\det\}$
2. $SL$ を含む作用群の 2 次元 $\mathbf F_{691}$-既約は**自然加群のみ**(素体上 Frobenius 捻り無し・双対 $W^*\cong W\otimes\det$)
⟹ この 2 行で初めて「捻りは 2 本で尽きる」が閉じます(「$\det$ の位数が 2」だけでは**なぜ $\det$ の冪だけか**が閉じない)。

### 2.5 二系統(逐語 §C-6)・撤退条件(§C-8)
- **二系統必須**: 直接計算 vs Shapiro 経由の一致を**カナリア**に(旧札に既在)。無ければ格は **candidate/single-run** 止まり。
- **撤退条件**: 壁時計 cap・`-o 2g` メモリ・超過時の行き先を cert に記載。★ 逐語 §B-2 の実測(cohomolo が次数 2016 で溢れ・次数 51 なら 0.1 秒)⟹ **次数選択が生死を分ける**を仕様に明記。

---

## §3 記帳

- ★ **暫定札 m1005-1(novelty 過大)**: 段 1 spec(裁定 983)で「本ノートの新規部分 ②」と申告した $\dim H^2\le1$ は、`pair_h2_design_draft_v1.md` の **P-PH2-4 に既存**でした。⟹ 記憶規範 *novelty-claims-need-grep* 該当。**v2.1 冒頭訂正**: 「本カードは pair_h2_design_draft_v1.md(M-3/P-PH2-4/P-PH2-5)と同一対象・同一量を扱う。P-PH2-4 は再掲であり本カードの新規ではない」。
- ★ **暫定札 m1005-2(和則の見落とし)**: 「各々 $\le1$」で止め、**和則**に気づきませんでした。⟹ (Ad-c) という**空の枝**を残す誤りに直結。教訓 **F-2**: **LHS 退化で $H^n(G,M)^{S}$ の形になったら、捻り全体の和が母空間の次元で抑えられることを先に書く**(枝の可能性を数える前に)。
- **【F-GAP-4 の番号衝突】**: 司令塔採番の F-GAP-4 = **非可換 $W$**(満額の残存扉・逐語 §F 第 2 項)。私が v2 で立てた F-GAP-4($\mathrm{Ad}\otimes\det^i$ の $S_3$-不変部の marking 依存)は ⟹ **F-GAP-6 へ改番**します(案 B: 司令塔/Sol 採番を正)。
- **F-GAP-5 は本書で閉鎖**(逐語取得・突合完了)。
- **申告**: 走行ゼロ・$u$ 非接触・$c$ 未評価・Sol 未監査・candidate 格。
