# 【K9-T63-COMPOSE】RECON × T63-P1 の合成検分 — ★ **成立(条件付き)**

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5・後任)/ **委嘱**: 裁定 916
**格**: candidate(紙・単系統・**Sol 未監査**)。**合成の格は W3-24 を超えない** = `paper-proof candidate / framework-conditional / Lean 未`。
**入力**: `provenance/CLAIMS.md` **W3-24**(逐語)/ `docs/notes/t63_reconnaissance_v1.md`(T63-P1)/ `docs/notes/k9_p1_recon_v2.md`(RECON)/ `E1_gt_odd_dih_canonical_v1.md` §5.1・§522 表 / `p1_corpus_index_v1.md`

> ## ★★ 判定
> $$\boxed{\ d_9\ \overset{\textbf{RECON}}{=}\ \operatorname{ord}(a_9)\ \overset{\textbf{T63-P1}}{=}\ 9\quad\Longrightarrow\quad \mathrm{Ih}_{K^{(9)}}\ \textbf{全射}\ =\ \textbf{Conj 5.1@}n=9\ }$$
> **(a) 型境界検問 = PASS** / **(b) 前件相続 = 条件付き PASS**(⚠ 1 件残)/ **(c) 正規化 = PASS**
> ⚠ **格は `paper-proof candidate / framework-conditional`**。「示された」ではなく「**工房内 candidate として完結した**」。

---

## §1 (c) 正規化の同一性 — ★ **PASS**

| | RECON 側(E1 §5.1) | T63-P1 側(t63 memo) |
|---|---|---|
| 定義 | $a_n:=[u_n^{-1}]_M\in F_n^\times/F_n^{\times M}$、$M=2n$、$F_n=\mathbf Q(\zeta_{2M})=\mathbf Q(\zeta_{4n})$ | $a_3=[v_3]_6=[-1/4]_6$($v_3=u_3^{-1}=(-4)^{-1}$)/ $a_9\in F_9^\times/F_9^{\times18}$ |
| $n=9$ | $[u_9^{-1}]_{18}$、$F_9=\mathbf Q(\zeta_{36})$ | 同左 |

★ **逆元の取り方**($u^{-1}$)・**mod の取り方**($M=2n$)・**基礎体**($F_n=\mathbf Q(\zeta_{4n})$)が**三点とも一致** ⟹ **同一正規化** ✔
(検算: $n=3$ で $M=6$・$F_3=\mathbf Q(\zeta_{12})$・$\operatorname{ord}([-4]_6)=3=e$ ✔ E1 §5.1 の記載と一致。)

---

## §2 (a) ★★ 型境界検問 — **PASS**($u_9$ 非接触は実質的に成立)

### 2.1 T63-P1 の導出鎖(逐語・W3-24 + t63 memo §5)

$$\textbf{(6.3-cls)}\quad \mathrm{res}_{F_n/F_d}(a_d)=\mathrm{pr}_{2n\to2d}(a_n)\quad\text{in }F_n^\times/F_n^{\times2d}$$
$d=3,n=9$ を入れて
$$\mathrm{pr}_{18\to6}(a_9)=\mathrm{res}_{F_9/F_3}(a_3)=[-1/4]_6,\qquad \operatorname{ord}\bigl([-1/4]_6\bigr)=3\ (\ne1).$$
上界 $\operatorname{ord}(a_9)\mid9$(C4-T)と合わせて $\operatorname{ord}(a_9)=9$。

### 2.2 ★ 核心論法の独立検算(**私の機械確認**)

$\mathbf Z/18\xrightarrow{\ \mathrm{pr}\ }\mathbf Z/6$ で位数を全数列挙:

| $\operatorname{ord}$ in $\mathbf Z/18$ | 元 | $\operatorname{ord}(\mathrm{pr})$ |
|---|---|---|
| 1 | 0 | 1 |
| **3** | **6, 12** | ★ **1**(pr で **0 に落ちる**) |
| **9** | 2,4,8,10,14,16 | ★ **3** |

$$\boxed{\ \textbf{上界 }\operatorname{ord}(a_9)\mid9\ \wedge\ \operatorname{ord}(\mathrm{pr}(a_9))=3\ \Longrightarrow\ \operatorname{ord}(a_9)=9\ }$$
★ **論法は厳密に正しい**(位数 3 の元は $\mathrm{pr}$ で消えるので、$\mathrm{pr}$ 側で位数 3 が見えたら $a_9$ は位数 9 しかありえない)。**機械確認 PASS**。

### 2.3 ★★ $u_9=3$ の循環路と**交差しないこと**の確認

| | **撤回済 U9-RIGID の路**(B116-1) | **T63-P1 の路** |
|---|---|---|
| 出発点 | ★ **標的群型** $\mathrm{Aff}(\mathbf Z/9)$(「この型の体は Kummer-円分型」) | ★ **$n=3$ の算術的既知値** $u_3=-4$(**定理 K3** = Conj 5.1@$n=3$ 成立・W3-11) |
| 渡り方 | 型 → 実算術 Galois 群の**全射性**(密輸) | 塔関係 **(6.3-cls)**(cover functoriality から導出・G3 で紙上閉) |
| $u_9$ への接触 | ★ **$u_9=3$ を型から推測** | ★ **$u_9$ の値に一度も触れない**(触れるのは $\mathrm{pr}(a_9)$ の位数のみ) |
| 判定 | ✘ **循環** | ★ **循環しない** |

$$\boxed{\ \textbf{T63-P1 は「型 → 算術」を渡らない。渡るのは「}n=3\ \textbf{の算術 → 塔 → }n=9\ \textbf{の算術」}\ }$$
⟹ ★ **W3-24 の「$u_9$ 非接触」は実質的に成立** ✔。**$u_9=3$ の撤回は撤回のままでよく、本合成はそれを復活させない**(復活させるのは $u_9$ の**値**であって、$a_9$ の**位数**ではない)。

---

## §3 (b) named framework 前件の相続 — **条件付き PASS**(⚠ 1 件残)

### 3.1 ★ C1 の状態 — **完全閉鎖を独立確認**(索引の記載を訂正)

`p1_corpus_index_v1.md` 行 182 は「裁定 107 の本文は LEDGER に発見できず・**C1 を閉と記帳する根拠としては記録所在不明**・本索引も C1 = open 扱い」と書くが、**私の独立確認では閉である**:

| 根拠 | 内容 | 確認 |
|---|---|---|
| `E1_gt_odd_dih_canonical_v1.md` §522 表(逐語) | 「**C1($n=3$ の窓同定)= 完全閉鎖**(機械同定 + 族的機構 W-REL)/ 裁定 107(`CLOSED_MATCH`)・裁定 174」 | ✔ 実読 |
| cert `search/certs/c1_class_check_20260728.json` | `universe:{n:3}`・`pn_size=108`・`n_ord=6`・`h2fun_size=h3fun_size=18`・`h2fun_self_normalizing=true`・★ **`h2fun_h3fun_not_conjugate=true`** | ✔ **実在・実読** |

⟹ ★ **裁定 916 の「C1 = 完全閉鎖」は正しい**。索引の判定基準(LEDGER 本文限定)による誤りで、裁定 916 の訂正(4+1 系統を等価に検査)が妥当。

### 3.2 ⚠★ **残る 1 件 — C1′@$n=9$ の要否**【COMPOSE-GAP-1】

E1 §522 表は **C1 と C1′ を明確に分ける**:

| 札 | 内容 | 状態 |
|---|---|---|
| **C1** | **$n=3$ の窓同定** | ★ **完全閉鎖** |
| **C1′** | **$n\ge5$ の窓同定**($q=7$ で $[\alpha]$ 3 類) | ✘ **開**(唯一の閉鎖路 =【I24-a】$\alpha$ 軌道予想) |

★ **$n=9\ge5$ ゆえ、$n=9$ 側の窓同定は形式上 C1′ の管轄**である。

- **肯定材料**: W3-24 の導出鎖は **C1 のみを挙げ C1′ を挙げない**。(6.3-cls) が使うのは**下段窓 $d=3$**(= C1)であり、上段は $\mathrm{pr}_{18\to6}$ の**射影先**として現れるだけ。W1-fam・(W2)-fam は**族供給**(全奇 $n$)なので $n=9$ 固有の窓同定を要さない設計と読める。
- ⚠ **未確認**: 私は `t63_reconnaissance_v1.md` の**全文を読んでいない**(§5 の核心部のみ)。**C1′@9 非依存を確認しきれていない**。

$$\boxed{\ \textbf{【COMPOSE-GAP-1】}\ \textbf{T63-P1 が }C1'@n=9\ \textbf{を要さないことの確認}\ \textbf{— 合成の唯一の残件}\ }$$

### 3.3 FAM-U-ASM 残余 6 項との重複整理

| 残余項 | T63-P1 との関係 |
|---|---|
| **始点算術**(= E1-GAP-5/6 = 全奇 $n$ の $\operatorname{ord}(a_n)=n$ 供給) | ★ **重複ではなく補完** — T63-P1 は**その $n=9$ instance を供給する**もの。索引行 89 の「open・閉扱い禁止」は**全奇 $n$** の話で、$n=9$ 単独とは矛盾しない |
| **(W2)-fam** | ★ **共有前件**(T63-P1 の導出鎖にも FAM-U-ASM にも現れる)⟹ **二経路は独立でない** |
| W5 / Λ-REG / (M-b) / ASM-α | T63-P1 の導出鎖には明示的に現れない(**要確認**・【COMPOSE-GAP-1】に含める) |

---

## §4 ★ 私の RECON v2 §2 の訂正(自己申告)

RECON v2 §2 は測定路を「**P1/FAM-U-ASM ⟹ $\operatorname{ord}(a_9)=9$**」と書いた。**これは誤り**である。

> `p1_corpus_index_v1.md` §1 逐語(F105-1.2): 昇格対象は 2 つ**だけ**。**意味しない 3 項**: W2-fam 全奇数成立 / ★ **全奇数で $\operatorname{ord}(a_n)=n$** / 算術的始点の閉鎖 — これらは candidate/open を保つ。

$$\boxed{\ \textbf{P1 の発効は }\operatorname{ord}(a_n)=n\ \textbf{を}\textbf{意味しない}\ \Longrightarrow\ \textbf{供給元は }\textbf{T63-P1(W3-24)}\ \textbf{である}\ }$$
⟹ **RECON v2 §2 の図の第 1 矢印を「P1」から「T63-P1」へ差し替える**(v1.4.8 queue 項目 15 に登録)。
⚠ **RECON の主結論($d_9=\operatorname{ord}(a_9)$)は無傷** — 訂正は「誰が $\operatorname{ord}(a_9)=9$ を供給するか」の帰属のみ。

---

## §5 合成の正確な言明(**この形でのみ流通させる**)

> ### 命題 **K9-COMPOSE**(candidate・framework-conditional)
> 次の 3 つを認めるとき $d_9=9$、すなわち $\mathrm{Ih}_{K^{(9)}}$ は全射(= Conj 5.1@$n=9$)である。
> 1. **RECON**(本工房・正典内在・無条件): $d_9=\lvert A\cap\mathfrak F_0\rvert=\operatorname{ord}(a_9)$。
> 2. **T63-P1 / W3-24**(paper-proof candidate・Sol 便 76 F3.2 検分済): C1 + named framework 前件の下で $\operatorname{ord}(a_9)=9$。
> 3. **【COMPOSE-GAP-1】**: T63-P1 が C1′@$n=9$ および W5/Λ-REG/(M-b)/ASM-α を要さないこと(**未確認**)。

**格**: `paper-proof candidate / framework-conditional / 単系統 / Sol 未監査 / Lean 未`。
⚠ **禁止**: 「$d_9=9$ が示された」「Conj 5.1@$n=9$ を証明した」「verified」。**言ってよいのは「工房内 candidate として完結した」まで**。
⚠ **receipt**: full $a_9$ の独立測定(**P8-value 線**)は**別線・未着**。**前件ではない**(便 76 ★教材 5)が、**独立確認としては要る**。

---

## §6 帰属・依存申告

- **T63-P1 / W3-24 / (6.3-cls)** = 工房既存(2026-07-28・Sol 便 76 F3.2 検分済)。**C1 の cert** = 実装係(2026-07-28)。
- **RECON($d_9=\operatorname{ord}(a_9)$)** = 私(裁定 912・`k9_p1_recon_v2.md`)。
- **委嘱・再発見** = 司令塔(裁定 916)。
- **本ノートの新規部分**: ① 核心論法($\mathbf Z/18\to\mathbf Z/6$ の位数表)の**独立機械検算** ② **型境界検問**(T63-P1 の出発点が $n=3$ の**算術**であって型でないことの対比表)③ **C1 の完全閉鎖の独立確認**(cert 実読・索引行 182 の訂正)④ ★ **【COMPOSE-GAP-1】**(C1′@9 の要否)の摘出 ⑤ **RECON v2 §2 の帰属訂正**(供給元は P1 ではなく T63-P1)。
- **未実施**: `t63_reconnaissance_v1.md` 全文精読・W5/Λ-REG/(M-b)/ASM-α の依存確認・receipt。**Sol 未監査**。⟹ **verified ではない**。

---

# 【v1.1 追記】COMPOSE-GAP-1 = ★ **閉鎖**(裁定 918 指示 2・t63 memo 全文精読)

**日付**: 2026-08-12 / **追記者**: 数学者(Opus 5・後任)/ **方式**: additive addendum(**本文 §1–§6 は不改変**)
**精読対象**: `docs/notes/t63_reconnaissance_v1.md`(**162 行・全文**)— ★ **独立ファイルとして実在**(司令塔の「未特定」に対する回答)

## A.1 ★★ 結論 — **C1′@$n=9$ 依存は無い**

t63 memo §5 の **caveat 表(5 枚)を逐語で確認**した。$n=9$ 側について要求されているのは **C2・C3** であり、**窓同定(C1′)は 1 枚も現れない**。

| # | caveat(t63 §5 逐語) | t63 v1 時点(2026-07-28) | ★ **現在**(本検分で突合) |
|---|---|---|---|
| **C1** | **$K^{(3)}$ の実測窓が $H_3^{\rm fun}=H_{2,1,0}$ か**($n=3$ で good な $H$ が $2n(n-1)=12$ 個・$\alpha\in\{1,2\}$ の二通り) | UNKNOWN・**最優先** | ★ **完全閉鎖**(裁定 107 `CLOSED_MATCH` + 174・cert `c1_class_check_20260728.json` 実読) |
| **C2** | (W1) が $n=9$ で成立(G3 が要求) | **未供給** | ★ **閉鎖**(`c2c4_closure_v1.md`: 「C2 =(W1) の $n=9$ 供給 = **閉鎖(族で)**、しかも全奇 $n\ge3$ で一斉」) |
| **C3** | ★ **$n=9$ 窓の (W5)・(W2)・BFC (5′) instance** | **OPEN** | ⚠ **named framework 前件として繰り込み**(下記 A.3) |
| **C4** | $\operatorname{ord}(a_9)\mid9$ の formal upper bound($e=n=9$・$\rho_0$ 忠実) | 要確認 | ★ **従属項目**(C3 または (6.3) から無償 = 命題 C4-T) |
| **C5** | $[-4]_6$ を $F_3$ でなく **$F_9$ で評価**すること | **閉** | ★ 閉(§5(c) は $F_9$ で計算済) |

$$\boxed{\ \textbf{下段窓の同定 = C1(閉)。上段(}n=9\textbf{)側の窓は }\textbf{HF-2 が構成的に与える}\ \bar\pi_{9,3}:P_9/H_9^{\rm fun}\to P_3/H_3^{\rm fun}\ }$$

★ **機構**: t63 §1 の A5 が示すとおり、cover は **HF-2(証明済)**により $H^{\rm fun}$ 窓**間**の射として最初から構成される。⟹ **$n=9$ 側の窓は「同定する」対象ではなく「定義して使う」対象**。同定が要るのは **実測値 $u_3=-4$ がどの窓の値か**という一点だけで、それが **C1** である(t63 §4 の破れ方 **B5「窓の取り違え($K^{(3)}$ の実測窓 $\ne H_3^{\rm fun}$)= 致命・最優先で潰すべき」**と整合)。

$$\boxed{\ \Longrightarrow\ \textbf{【COMPOSE-GAP-1】の第 1 問「(6.3-cls) の下段窓使用が }d=3\ \textbf{のみか」= }\textbf{YES(閉)}\ }$$

## A.2 ★ W3-24 の表現との完全整合

W3-24 は「**C1(裁定 107)+ named framework 前件の下で**」と書く。本検分の結果:

- **C1・C2・C4・C5 = 閉**
- **C3 のみが framework 前件**

⟹ **W3-24 の表現は正確**(C1 を名指しし、残りを named framework 前件へ繰り込んだ形)。★ **記載と実体が一致していることを独立確認した。**

## A.3 W5 / Λ-REG / (M-b) / ASM-α の依存 — ★ **合成は新規の枠組み仮定を追加しない**

| 項 | T63-P1 での出現 | FAM-U-ASM 残余 6 項との関係 |
|---|---|---|
| **(W5)** | ★ **C3 に明示的に含まれる**(t63 §5 caveat C3 逐語) | ★ **重複**(残余の「W5」そのもの) |
| **(W2)** | ★ **C3 に明示的に含まれる** | ★ **重複**(残余の「W2-fam」) |
| **BFC (5′)** | ★ **C3 に明示的に含まれる** | B-1/(5′) は P1 発効で `theorem-framework-relative` 格(裁定 515/520・F104-3.1) |
| **Λ-REG / (M-b) / ASM-α** | ⚠ **t63 の caveat 表には明示されない**。t63 の依拠は「正典(**BFC v2.15**・TB4 v2.5・Rule 1 v1.5)」なので **BFC v2.15 の前件群に内包される可能性**(未確認) | いずれも **FAM-U-ASM 残余に既出** ⟹ **新規負担にならない** |

$$\boxed{\ \textbf{K9-COMPOSE の枠組み負担は }\textbf{FAM-U-ASM 残余 6 項に包含される}\ \textbf{— 合成が新しい仮定を持ち込むことはない}\ }$$
⚠ **格の申告**: Λ-REG/(M-b)/ASM-α の **BFC 内包は candidate**(`week4-BFC攻略_opus_v2.md` の前件表を未読)。★ ただし**包含関係の結論は変わらない**(いずれも残余 6 項の中にある)。

## A.4 ★ 追加で確認した T63-P1 の健全性 2 点

1. **外部文献ゼロ**: t63 は「**外部文献なし**」と明記。依拠は正典 + $K^{(3)}$ の公開実測値 + 幾何/群論のみ ⟹ **文献ゲート違反なし**。
2. ★ **封印遵守の実質確認**: 「封印 3 量($u_9/a_9$ の値・$c$ 平方類・$\hat c_\mu$)に一切接触していない。使ったのは $K^{(3)}$ の公開実測値 $u_3=-4$ のみ」。**本検分でも導出鎖に $u_9$ の値が現れないことを確認**(現れるのは $\mathrm{pr}_{18\to6}(a_9)$ の**位数**のみ)⟹ **§2 の型境界検問 PASS を再確認**。
   ★ **$2\notin F_9^{\times3}$ の証明も検分**: 「$2=y^3$ なら $\mathbf Q(y)\cong\mathbf Q(2^{1/3})$ は $\mathbf Q$ 上**非正規**。しかし $F_9=\mathbf Q(\zeta_{36})$ は**アーベル**ゆえ部分体は全て正規。矛盾」— ★ **正しい**(初等的で隙がない)。

## A.5 ⚠ 残る留保(honest)

| # | 内容 | 重さ |
|---|---|---|
| 1 | **Λ-REG/(M-b)/ASM-α の BFC 内包**が未確認(結論は不変だが根拠が間接) | 小 |
| 2 | t63 §4 の **破れ方 B2(指数ズレ)・B3(向きズレ)・B4(cover 非存在 = G3)** は t63 自身が「致命」と分類。**G3 は便 75 F3.2 で PAPER-PROOF 済**(W3-24)だが、B2/B3 は (2.2) の $e(\rho)=n/d$ と (2.1) の引き戻しに依存 — **私は §2 の幾何計算を追検算していない** | ★ 中 |
| 3 | **C3 が「閉じた」のではなく「framework 仮定へ繰り込まれた」**という読みは私の判読 — 裁定 916 の「C3 = T63-P1 鎖内で処理済み」と**同義と解した**が、**別解釈の余地がある** | ★ 中 |

## A.6 ⟹ COMPOSE-GAP-1 の最終判定

$$\boxed{\ \textbf{【COMPOSE-GAP-1】= }\textbf{閉鎖}\ \textbf{(C1}'@n=9\ \textbf{依存なし・枠組み負担は残余 6 項に包含)}\ }$$

⟹ **命題 K9-COMPOSE(§5)の前件 3 が解消**し、前件は **1(RECON)+ 2(T63-P1/W3-24)**の二枚になる。
⚠ **格は変わらない**: `paper-proof candidate / framework-conditional / 単系統 / Sol 未監査 / Lean 未`。**W3-24 の天井を超えない。**
⚠ **A.5 の留保 2(B2/B3 の幾何追検算)は新規の【COMPOSE-GAP-2】として起票**(重さ = 中・Sol 監査で潰すのが安い)。
