# 【K9-UNRAM】$L_{9,\mathrm{Aff}}$ の 3 外不分岐 — 在庫 pin からの自前導出 v1

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5・後任)/ **委嘱**: 裁定 910 → **裁定 920 で専念指示**
**格**: **candidate**(紙・単系統・**Sol 未監査**)。走行ゼロ。**verified は Lean に予約**。
**pin 束**: `docs/scout/k9_goodred_pin_v1.md`(reader 2 巡目・裁定 907)/ `docs/scout/ihara_icm_unram_pin_v1.md`(1 巡目)
**前提**: R1 第一波 `r1_k9_bridge_v1.md`(K9-COORD / K9-CYC / K9-C2 / K9-KUMMER)

> ## ★★ 到達点(先に 3 行)
> $$\boxed{\ \textbf{罠 2(inner ambiguity)と罠 3(向き)は}\textbf{閉じた}\ }$$
> **残るのは 1 点**: 幾何的 specialization(SGA1 XIII)から **算術的な $I_p$-作用の自明性**への落とし込み。**在庫に該当文献なし**(reader 明記)⟹ 骨子は §3、GAP は **1 段に局所化**。
> ⚠ **未完**: §3 の段 (3) =【**UNRAM-GAP-1**】。**「$L_{9,\mathrm{Aff}}$ は 3 外不分岐」を既成事実として扱わないこと。**

---

## §1 標的(R1 第一波からの継承)

$$t\in Z^1(G_\mathbf Q,\mu_9),\qquad L_{9,\mathrm{Aff}}=\mathbf Q(\zeta_9,\sqrt[9]{a}),\qquad a\in\mathbf Q^\times/(\mathbf Q^\times)^9$$
$$\boxed{\ \textbf{(K9-UNRAM)}\iff\forall p\ne3:\ t(I_p)=1\iff v_p(a)\equiv0\ (\mathrm{mod}\ 9)\ \ \forall p\ne3\ }$$
$t$ の定義: $\psi_9^{(1)}(f_g)=r^{2k}$ の $k$($\psi_9^{(1)}:F_2\to D_9$, $x\mapsto r$, $y\mapsto rs$)。

---

## §2 ★★ 罠 2(inner ambiguity)と罠 3(向き)の閉鎖

### 2.1 曖昧さの正体(SGA1 XIII 2.10・逐語)

> **Changer la classe de chemins de $a_1$ à $a_2$ revient à modifier $\pi$ par un automorphisme intérieur** de $\pi_1^{\mathbb L}(X_{\bar s_2},a_2)$

⟹ specialization 射の曖昧さは **inner automorphism ちょうど**。

### 2.2 命題 **INN-HARMLESS**(candidate・証明つき・機械確認済)

**主張**: inner 曖昧さは $t$ を $\pm t$ に送るだけで、**$\ker\rho_{9,\mathrm{Aff}}$・$L_{9,\mathrm{Aff}}$・$\operatorname{ord}(a)$ を変えない**。

**証明** $\mathrm{conj}(h)$ は像側で $\psi_9^{(1)}(h)\in D_9$ による共役を誘導する。$D_9$ の共役は $\langle r\rangle$ 上で
$$r^{j}r^{2k}r^{-j}=r^{2k},\qquad s\,r^{2k}s^{-1}=r^{-2k}$$
ゆえ $r^{2k}\mapsto r^{\pm2k}$、すなわち $t\mapsto\pm t$。よって $a\mapsto a^{\pm1}$ で、$\mathbf Q(\zeta_9,\sqrt[9]{a})=\mathbf Q(\zeta_9,\sqrt[9]{a^{-1}})$、$\operatorname{ord}(a)=\operatorname{ord}(a^{-1})$。∎
**機械確認**: $D_9$ 全 18 元での共役を全数計算、$k=1..4$ で $r^{2k}\mapsto\{r^{2k},r^{-2k}\}$ を確認(PASS)。

> ★ R1 第一波の **MARKING-COMPAT**($(\mathbf Z/9)^\times$-scaling は無害)と**同型の議論**。⟹ 罠 2 は「消去」ではなく「**不変量が鈍感**」で閉じる。

### 2.3 ★★ 命題 **INN-FORCES-TRIVIAL**(candidate・罠 3 の閉鎖)

**主張**: $g\in I_p$($p\ne3$)で **outer action が自明**なら $f_g=1$、従って **$t(g)=0$**。

**証明**(4 行)
1. $p\ne3$ ゆえ $\mathbf Q(\zeta_9)/\mathbf Q$ は $p$ で不分岐 ⟹ $\chi(g)\equiv1\pmod 9$。$K^{(9)}$ 水準で $g$ の作用は $x\mapsto x,\ y\mapsto f_g^{-1}yf_g$。
2. outer が自明 ⟹ ある $h$ で $x\mapsto h^{-1}xh$、$y\mapsto h^{-1}yh$。
3. 第 1 座標より $h\in Z_{\widehat F_2}(x)$、第 2 座標より $f_gh^{-1}\in Z_{\widehat F_2}(y)$。**自由副有限群の非自明元の中心化群は procyclic**【要 pin・**UNRAM-GAP-2**】ゆえ $Z(x)=\overline{\langle x\rangle}$、$Z(y)=\overline{\langle y\rangle}$。
4. ⟹ $f_g\in\overline{\langle y\rangle}\cdot\overline{\langle x\rangle}$。一方 **charming 条件**(2405 §1.3・Pin D (1.4))で $f_g\in[\widehat F_2,\widehat F_2]^{\rm cl}$ ⟹ abelianization $\widehat{\mathbf Z}^2$ で $0$。$f_g=y^bx^a\mapsto(a,b)=(0,0)$ ⟹ $f_g=1$。∎

$$\boxed{\ \Longrightarrow\ \textbf{罠 3 の要求「pro-3 outer kernel に入れば Aff 像が単位」が}\textbf{従う}\ }$$
★ **機構**: inner を「消去」するのではなく、**$f_g$ が交換子群の元であること(charming)が inner を強制的に自明化する**。⟹ Pin D「惰性保存で based へ持ち上がる」と整合。

---

## §3 ★ 幾何 → 算術の落とし込み(**骨子**・在庫に該当文献なし)

**設定**: $p\ne3$、$S=\mathrm{Spec}\,\mathbf Z_p$、$X=\mathbf P^1_S$、$D=\{0,1,\infty\}$($S$ 上の**切断**・任意の $\mathbf F_p$ で相異なる ⟹ **相対正規交叉因子**)、$U=X-D$。

| 段 | 内容 | 根拠 | 状態 |
|---|---|---|---|
| **(1)** | $U/S$ が **SGA1 XIII 2.11/2.12 の前提**(propre lisse $X$・相対正規交叉 $D$・除点は $S$ 上の切断)を満たす | 3 点が $\mathbf Z$ 上どの素点でも衝突しない(初等) | ★ **閉** |
| **(2)** | specialization $\pi_1^{(p')}(U_{\bar K})\xrightarrow{\ \sim\ }\pi_1^{(p')}(U_{\bar k})$ が**全単射** | ★ **Pin C 2.12 証明中の逐語**「le morphisme de spécialisation $\pi_1^{p'}(\bar U)\to\pi_1^{p'}(U)$ est **bijectif**」 | ★ **閉**(在庫 pin) |
| **(3)** | ⟹ $I_p$ が $\pi_1^{(p')}(U_{\bar K})$ に**自明に作用** | ⚠ **在庫文献なし**(reader 明記: 「両者をつなぐ算術的導出(**$I_p$ 上の自明性への落とし込み**)を書いた在庫文献は見つからなかった」) | ✘ ★ **【UNRAM-GAP-1】** |
| **(4)** | $\ell=3$、$p\ne3$ ⟹ pro-3 商は $\pi_1^{(p')}$ の商 ⟹ $I_p$ は pro-3 outer action に自明 | 群論(初等) | ★ **閉** |
| **(5)** | ⟹ §2.3 で $t(I_p)=1$ | 本ノート §2.3 | ★ **閉**(§2.3 が立てば) |

$$\boxed{\ \textbf{(1)(2)(4)(5) は在庫 pin と本ノートで閉じる。残るのは (3) ただ一段}\ }$$

### 3.1 【UNRAM-GAP-1】の正確な形

> **要る命題**: 良還元設定で **specialization 同型(段 (2))が $G_{\mathbf Q_p}$-同変であり、その $I_p$-作用が特殊ファイバー側では自明**であること。

★ **在庫で最も近いもの** = **Pin A(HS2000 印刷 pp.3121–3122)**:
> An application of Grothendieck's comparison theorem shows that the representation $\mathrm{Gal}(\bar{\mathbf Q}/\mathbf Q)\to\Phi$ is **unramified outside $\ell$**

⚠ **outer 表現についての結論の主張のみで、HS2000 内に証明は無い**。根拠として名指しされているのは "Grothendieck's comparison theorem" のみで、詳細は **[I1] = Ihara, Ann. Math. 123 (1986) 43–106**(**在庫外**)。

$$\boxed{\ \Longrightarrow\ \textbf{【UNRAM-GAP-1】は「引用格で埋める」か「自前で (3) を証明する」かの二択}\ }$$

### 3.2 引用格で埋めた場合の帰結(**格を明示**)

Pin A を**引用格**で採用するなら、$g\in I_p$($p\ne3$)で outer action 自明 ⟹ §2.3 で $f_g=1$ ⟹ $t(I_p)=1$ ⟹ **(K9-UNRAM) 成立**(格 = **引用依存 candidate**)。

$$\boxed{\ a=3^{\,j}\bmod(\mathbf Q^\times)^9,\qquad L_{9,\mathrm{Aff}}\subseteq\mathbf Q\bigl(\zeta_9,\sqrt[9]{3}\bigr)\ }$$
($v_p(a)\equiv0\ (p\ne3)$ と $-1=(-1)^9$ から。R1 第一波 §4.3 の条件付き帰結が発効。)

> ### ⚠★★ 封印姿勢の申告(**t63 の先例に倣う**)
> 上の帰結は **$a$(封印 3 量の一つ $a_9$ と同族)の値を絞る**。**測定ではなく演繹**だが、**予言先行(pre-registration)として扱われたい**。
> ★ **K9-COMPOSE**($\operatorname{ord}(a_9)=9$・candidate)と合わせると $j\in(\mathbf Z/9)^\times$ が従い
> $$\boxed{\ \textbf{予言 P-K9U-1}\ (\textbf{条件付き・凍結}):\quad L_{9,\mathrm{Aff}}=\mathbf Q\bigl(\zeta_9,\sqrt[9]{3}\bigr)\ }$$
> ⚠ **U9-RIGID の結論と同一の体だが導出は別物**(U9-RIGID は型 → 算術で循環・本導出は幾何 specialization → inner 強制 → Kummer)。
> ⚠ **$u_9=3$ の撤回を復活させない** — 復活するのは**体**であって、$u_9$ という**別対象の値**ではない(**NAME-COLLIDE 注意**: 私の $a$ / u9bit の $u_9$ / FAM-U の $u_n$ は三者別物 — `k9_p1_recon_v2.md` §2)。

---

## §4 【GAP】と次の一手

| # | 内容 | 重さ |
|---|---|---|
| ★★ **【UNRAM-GAP-1】** | §3 段 (3): specialization 同型の $G_{\mathbf Q_p}$-同変性と $I_p$-自明性。**在庫文献なし** ⟹ 遠征先 = **[I1] Ihara, Ann. Math. 123 (1986) 43–106** | ★★ 大 |
| ★ **【UNRAM-GAP-2】** | 自由副有限群 $\widehat F_2$ の非自明元の中心化群が procyclic(§2.3 段 3)【要 pin】 | 中 |
| — | 罠 2(inner ambiguity) | ★ **閉**(INN-HARMLESS + INN-FORCES-TRIVIAL) |
| — | 罠 3(factorization の向き) | ★ **閉**(INN-FORCES-TRIVIAL) |
| — | 罠 4(3 群と思わない) | ★ **閉**(R1 第一波 K9-CYC で非 3 部分は円分と同定済) |
| — | 罠 7(向きと連続性) | ★ **閉**(段 (4)(5)・両核の閉性は $\rho$ が連続準同型ゆえ自動) |

### ★ 推薦(裁定を仰ぐ)
1. **【文献要請】K9-LIT-2**: **Ihara, Ann. Math. 123 (1986) 43–106**(HS2000 [I1])の該当箇所 — 「$\mathrm{Gal}\to\Phi$ が $\ell$ 外不分岐」の**証明**。★ **要求が 1 論文・1 命題に確定**(K9-LIT-1 より更に狭い)。
2. **Pin A を引用格で暫定採用**し、§3.2 の**予言 P-K9U-1 を凍結**(測定・監査より先に記録 = t63 の先例)。
3. **【UNRAM-GAP-2】**は初等的 ⟹ Sol 監査で 1 行もらうのが安い。
4. ★ **自己追検算の候補(裁定 921)**: t63 §2 の幾何計算(2.1)(2.2)= **GAP-2**。$\S2.2$ は **TOWER-α-INV 第 2 段を支える**ので、Sol 監査と二重でも**位数主張の要**として無駄にならない。**UNRAM 完了後に着手を推薦**。

---

## §5 帰属・依存申告

- **pin 束**(HS2000 / SGA1 X・XIII / 2008.00066 (1.4) / Ihara ICM 再走査)= **reader 2 巡目**(裁定 907)・**文献ゲート経由**で受領。
- **罠 7 点** = Sol 便 118。**委嘱** = 司令塔(裁定 910/920/921)。
- **本ノートの新規部分**: ① **INN-HARMLESS**(inner 曖昧さ ⟹ $t\mapsto\pm t$・機械確認済)② ★ **INN-FORCES-TRIVIAL**(charming が inner を強制自明化 ⟹ 罠 3 閉鎖)③ **§3 の 5 段骨子**と **GAP の 1 段への局所化** ④ **§3.2 の条件付き帰結と予言 P-K9U-1 の凍結**(封印姿勢の申告つき)⑤ **K9-LIT-2 を 1 論文 1 命題へ確定**。
- **検算**: $D_9$ 共役の全数計算のみ(python 単系統)⟹ **cross-checked ではない**。
- **未実施**: [I1] 未入手・§3 段 (3) 未証明・Lean 未着手・**Sol 未監査**。⟹ **verified ではない**。
