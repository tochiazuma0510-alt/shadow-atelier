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
