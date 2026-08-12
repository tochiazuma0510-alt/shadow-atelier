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


---

# 【v2 追記】Annals 123 Thm 1(i) による段 (3) の閉鎖 — ★ **検問 2 点 PASS・GAP-2 も閉**

**日付**: 2026-08-12 / **委嘱**: 裁定 931(研究者の JSTOR 配達 → reader pin 化 → 文献ゲート経由)/ **再開**: 裁定 932
**方式**: **additive addendum**(本文 §1–§5 は不改変)/ ★ **積荷同期: 本ファイルは便に積載済み ⟹ commit 時に通知**
**新 pin**: `docs/scout/ihara_annals123_unram_pin_v1.md`(65b8356)/ 現物画像 `papers/ihara-annals123-pp43-55/`

> ## ★★ 結論
> $$\boxed{\ \textbf{段 (3) は }\textbf{Theorem 1(i)(証明全文つき)}\ \textbf{で閉じる。格 = }\textbf{proof-pinned candidate}\ }$$
> **検問 (i) $\Phi$ の同一性 = PASS**(差 3 点すべて勘定)/ **検問 (ii) 基点系 = PASS**(Deligne 接基点 = Belyi lift 類)
> ★ **副産物 2 件**: **Belyi Prop 3 が INN-FORCES-TRIVIAL を正典側で代替** / ★ **【UNRAM-GAP-2】も pin で閉鎖**

---

## A. 段 (3) の差し替えと **(2)(3)(4) の縮約**

**旧(v1 §3 段 (3))**: 「specialization 同型の $G_{\mathbf Q_p}$-同変性と $I_p$-自明性 — **在庫文献なし**」= ✘【UNRAM-GAP-1】

**新**: **Ihara, Annals 123 (1986), Theorem 1(i)(p.53)+ 証明全文(p.54)**。

> **Theorem 1.** (i) *The Galois representation* $\varphi_{\mathbf Q}:\mathrm{Gal}(\bar{\mathbf Q}/\mathbf Q)\to\Phi$ *is unramified outside* $l$.
> (脚注: "This was proved also by Deligne.")

**証明の骨格**(p.54 逐語より): $K_n=K(t^{1/l^n},(1-t)^{1/l^n})$。$0,1,\infty$ の $K_n/K$ における分岐指数がちょうど $l^n$ ゆえ $M=\bigcup_n K_n^{\rm ur}$。$p\ne l$、$k=\mathbf Q_p$ とし、Fermat 曲線 $\mathfrak X_n/\mathbf Z$($X^{l^n}+Y^{l^n}=Z^{l^n}$)へ **Grothendieck comparison theorem [10]** を適用すると $\mathfrak X_n\otimes\bar{\mathbf Q}_p$ と $\mathfrak X_n\otimes\bar{\mathbf F}_p$ の有限エタール pro-$l$ 被覆が**圏同値** ⟹ $M'/\mathbf Q_p^{\rm ur}(t)$ で $M'\cdot\bar{\mathbf Q}_p=M$、$M'\cap\bar{\mathbf Q}_p=\mathbf Q_p^{\rm ur}$ なるものが存在 ⟹ $\varphi_{\mathbf Q_p}$ は $\mathrm{Gal}(\mathbf Q_p^{\rm ur}/\mathbf Q_p)$ を factor through。∎

### A.1 ★ 縮約の判定(司令塔の機構抽出の検証)

| v1 の段 | 内容 | v2 での扱い |
|---|---|---|
| (1) | $U/S$ が SGA1 XIII 2.11/2.12 の前提を満たす | ★ **不要になった** — Ihara は Fermat 曲線 $\mathfrak X_n$(**proper**)を使うので、私が開曲線用に用意した前提充足は**そもそも別ルート** |
| (2) | $\pi_1^{(p')}$ の specialization 全単射 | ★ **Thm 1(i) の証明内部**(圏同値 [10])が担う |
| (3) | $I_p$ 自明作用 | ★ **Thm 1(i) そのもの** |
| (4) | pro-3 は $p'$-商 | ★ Ihara は最初から **pro-$l$** で構成 ⟹ 段として不要(代わりに **B.2(a) の落とし込み**が要る) |
| (5) | INN-FORCES-TRIVIAL(outer → based) | ★ **存続・load-bearing**(さらに C.2 で正典側の代替を得る) |

$$\boxed{\ \textbf{⟹ 骨子 5 段は }\textbf{「Thm 1(i) 引用 1 本 + 段 (5)」}\ \textbf{の 2 段へ縮約される}\ }$$
★ **司令塔の見立て「(2)(3)(4) は Thm 1(i) の引用 1 本に縮約」は正しい**。⚠ ただし**段 (1) も落ちる**(Ihara は proper な Fermat 曲線経由で、私の開曲線ルートとは別機構)— **縮約は 3 段でなく 4 段**である。
⚠ **格**: 「引用依存 candidate」→ ★ **proof-pinned candidate**(**証明全文が頁画像で pin 済**)。⚠ **cross-checked ではない**(工房の独立再証明なし)。

---

## B. ★★ 検問 (i) — Ihara の $\Phi$ は私の outer 対象と同一か

### B.1 論文側の定義(逐語)

**(p.49 式 (2))**: $\mathrm{Brd}(\mathfrak G;x_0,\dots,x_r)=\{\sigma\in\mathrm{Aut}\,\mathfrak G\mid\sigma(x_i)\sim x_i^\alpha\ (0\le i\le r),\ \exists\alpha\in\mathbf Z_l^\times\}/\mathrm{Int}\,\mathfrak G$
**(p.53 式 (1))**: $\Phi=\mathrm{Brd}^{(2)}=\mathrm{Brd}(\mathfrak F;x,y,z)$、$\mathfrak F$ = **free pro-$l$ group** of rank 2、$z=(xy)^{-1}$。

### B.2 差の勘定(**3 点・すべて閉じる**)

| # | 差 | 勘定 | 判定 |
|---|---|---|---|
| **(a)** | **完備化**: Ihara は **pro-$l$** の $\mathfrak F$ / 私は **profinite** $\widehat F_2$ | ★ **$t$ は pro-3 を経由する**: $t$ は $\psi_9^{(1)}$ の**交換子群への制限**で定義され、$\psi_9^{(1)}\bigl([\widehat F_2,\widehat F_2]\bigr)\subseteq[D_9,D_9]=\langle r\rangle\cong\mathbf Z/9$ = **3-群**。⟹ $[\widehat F_2,\widehat F_2]\to\mathbf Z/9$ は pro-3 商を経由 ⟹ $\ell=3$ で $\mathfrak F$ 版に落ちる | ★ **PASS** |
| **(b)** | **$\alpha$ の条件**($\sigma(x_i)\sim x_i^\alpha$・$\alpha$ は $i$ に依らない) | 2405 (1.5) の作用は $g(x)=x^{\chi(g)}$、$g(y)=f_g^{-1}y^{\chi(g)}f_g\sim y^{\chi(g)}$、$z=(xy)^{-1}$ より $g(z)\sim z^{\chi(g)}$ ⟹ $\alpha=\chi(g)$ で $i$ に依らない。★ **Prop 2(p.53)が「$N\circ\varphi$ = $l$-cyclotomic character」を証明済** ⟹ **私の K9-CYC と正典側で一致** | ★ **PASS** |
| **(c)** | **outer vs based**($/\mathrm{Int}\,\mathfrak F$) | ★ **INN-FORCES-TRIVIAL**(v1 §2.3)が橋。⟹ **さらに C.2 で Belyi Prop 3 が正典側の代替を与える** | ★ **PASS** |

> ### ★★ (a) で再び **charming が効いている**
> $\psi_9^{(1)}$ 自体は $D_9$(位数 $18$・**3-群ではない**)への射で pro-3 を経由しない。**pro-3 に落ちるのは $f_g\in[\widehat F_2,\widehat F_2]$(charming)だからである。**
> $$\boxed{\ \textbf{罠 4(奇 dihedral 商全体を 3 群と思わない)の正しい処理は、}\textbf{charming で交換子群へ落とすこと}\ }$$
> ⟹ **INN-FORCES-TRIVIAL と同じ機構**。R1 第一波 K9-CYC の「非 3 部分は円分」と合わせて**二重に確認**された。

$$\boxed{\ \textbf{検問 (i) = PASS}\ }$$

---

## C. ★★ 検問 (ii) — 基点系は LOCAL-PIN と同一か

### C.1 論文側の正規化(逐語)

**Prop 1(p.51)**: $\iota:\mathfrak F^{(r)}\xrightarrow{\sim}\mathrm{Gal}(M/K)$ で $\iota(x_i)$ が $P_i$ 上のある place の**惰性群を生成**する。$\varphi$ は $\iota$ に依存するが **inner を除いて一意**(p.53: "the dependence of $\varphi$ on $\iota$ is only up to inner automorphisms")。

**(p.47・決定的)**:
> Deligne, on the other hand, considered a "**tangential base point**" for $\pi_1(\mathbf P^1\setminus\{0,1,\infty\})$ … and has kindly informed the author that **this is equivalent to considering the class of Belyi's liftings for all $\iota$**.

### C.2 ★★★ Belyi の $\Phi^*$ と Proposition 3 — **based 側が正典で確保される**

**(p.54 逐語)**: $\Phi^*=\{\sigma\in\mathrm{Aut}\,\mathfrak F\mid \sigma x\sim x^\alpha,\ \sigma y\approx y^\alpha,\ \sigma z=z^\alpha,\ \exists\alpha\in\mathbf Z_l^\times\}$
($\approx$ は **$\mathfrak F'=[\mathfrak F,\mathfrak F]$ の元による共役**)
**(p.55) Proposition 3 (Belyi)**: 「*The canonical homomorphism* $\mathrm{Aut}\,\mathfrak F\to\mathrm{Aut}\,\mathfrak F/\mathrm{Int}\,\mathfrak F$ *induces an isomorphism* $\Phi^*\xrightarrow{\ \sim\ }\Phi$.」

> ### ★★★ 本追記の最大の発見
> $\Phi^*$ の定義条件「$\sigma y\approx y^\alpha$($[\mathfrak F,\mathfrak F]$ の元による共役)」は、**私の charming 条件 $f_g\in[\widehat F_2,\widehat F_2]^{\rm cl}$ そのもの**である。
> $$\boxed{\ \textbf{⟹ 私の based 対象は Belyi の }\Phi^*\ \textbf{であり、Prop 3 で }\Phi\ \textbf{と}\textbf{群同型}\ }$$
> ⟹ **Thm 1(i) の outer 側の不分岐性が、Prop 3 の同型でそのまま based 側へ移る。**
> ★ **私の INN-FORCES-TRIVIAL は正しかったが、正典はより強い形(群同型)を既に持っていた** — 自前証明は**独立確認**として残す(**二経路一致**)。

### C.3 LOCAL-PIN との照合

| データ | 私の LOCAL-PIN(R1 §1) | Annals 123 | 判定 |
|---|---|---|---|
| 接基点 | $\overrightarrow{01}$(Ihara ICM 印刷 pp.105–106) | ★ **p.47 の Deligne tangential base point**(**同一著者・同一対象**) | ★ 同一 |
| $x,y,z$ | $x$ = $0$ 周りの正向き小ループ、$y=p^{-1}x'p$、$z=(xy)^{-1}$ | $x,y,z$ が $0,1,\infty$ 上の惰性群を生成(Prop 1)、$z=(xy)^{-1}$(p.53) | ★ 同一 |
| 正規化の型 | 接基点で based | $\iota$ + **Belyi lift の類** = Deligne 接基点(**p.47 が同値と明言**) | ★ 同一 |
| $\alpha$ | $\chi$(2405 (1.5)) | $N\circ\varphi=\chi_l$(**Prop 2**) | ★ 同一 |

$$\boxed{\ \textbf{検問 (ii) = PASS}\ —\ \textbf{差の勘定は「}l\ \textbf{進成分への制限」1 点のみで、それは B.2(a) で閉じている}\ }$$

---

## D. ★ 副産物 —【UNRAM-GAP-2】も pin で閉鎖

v1 §2.3 段 3 で【要 pin】とした「**自由副有限群の非自明元の中心化群は procyclic**」は、pro-$l$ 版が**二箇所で pin 済**:

1. **Remark 1(p.52 逐語)**: 「the **normalizer** of the group $\langle x_i\rangle$ generated by $x_i$ in $\mathfrak F^{(r)}$ **coincides with $\langle x_i\rangle$ itself**」⟹ 中心化群 $\subseteq$ 正規化群 $=\langle x_i\rangle$。
2. **Prop 3 の証明(p.55)**: 「**centralizer of $x$ (resp. $y$, $z$) in $\mathfrak F$ is $\langle x\rangle$**」— ★ **中心化群そのものの言明**。

⚠ **差の勘定 1 行**: Ihara は **pro-$l$ の $\mathfrak F$**、私は $\widehat F_2$ で使った。★ **B.2(a) により $t$ は pro-3 を経由する**ので、**INN-FORCES-TRIVIAL を $\mathfrak F=F_2^{(3)}$ 上で走らせれば pin がそのまま適用できる** ⟹ **profinite 版は不要**。

$$\boxed{\ \textbf{【UNRAM-GAP-2】= }\textbf{閉}\ \textbf{(pro-3 版で走らせる・差は 1 行で勘定済)}\ }$$

---

## E. P-K9U-1 の条件更新(**凍結本体は不改変**)

| | v1 §3.2 時点 | ★ **v2** |
|---|---|---|
| 不分岐性の根拠 | **Pin A(HS2000)= 引用依存**(結論の主張のみ・証明なし) | ★ **Annals 123 Thm 1(i) = proof-pinned**(証明全文・頁画像) |
| outer → based | INN-FORCES-TRIVIAL(自前) | ★ **Belyi Prop 3(正典・群同型)** + INN-FORCES-TRIVIAL(独立確認) |
| 中心化群 | 【UNRAM-GAP-2】要 pin | ★ **閉**(Remark 1 / Prop 3 証明) |
| **残る条件** | Pin A 引用依存 + GAP-1 + GAP-2 | ★ **framework 層のみ**(K9-COMPOSE の $\operatorname{ord}(a_9)=9$ が framework-conditional) |

$$\boxed{\ \textbf{予言 P-K9U-1}:\ L_{9,\mathrm{Aff}}=\mathbf Q\bigl(\zeta_9,\sqrt[9]{3}\bigr)\quad\textbf{— 条件が }\mathbf{1}\ \textbf{枚外れた(引用依存 → proof-pinned)}\ }$$
⚠ **凍結本体(commit `bd80c44`)は不改変**。本追記は**条件欄の更新のみ**。
⚠ **$u_9=3$ の撤回は撤回のまま** — 復活するのは**体**であって、$u_9$ という**別対象の値**ではない(NAME-COLLIDE)。

---

## F. ★ 便 119 P3③ の書換案(**1 行**・裁定 931 指示 4)

> ★ **新(書換案)**: 「**(K9-UNRAM) の文献入力は解決した** — Ann. Math. **123** (1986) **Theorem 1(i)(p.53)+ 証明(p.54)** を頁画像で pin 済(`docs/scout/ihara_annals123_unram_pin_v1.md`)。**請求は「供給」から「監査」へ切り替える**: ① $\Phi$ の同一性判定(pro-$l$ vs profinite・$\alpha=\chi$・outer/based の**差 3 点**)② 基点系の同一性判定(Deligne 接基点 = Belyi lift 類)③ ★ **Belyi Prop 3 の $\Phi^*\cong\Phi$ が私の charming 条件と一致し INN-FORCES-TRIVIAL を代替する**という読みの可否 — の 3 点をご覧いただきたい。」

---

## G. 残 GAP と格

| # | 内容 | 状態 |
|---|---|---|
| **【UNRAM-GAP-1】** | ★ **閉**(Thm 1(i)・**proof-pinned candidate**) |
| **【UNRAM-GAP-2】** | ★ **閉**(Remark 1 / Prop 3 証明・pro-3 版) |
| ⚠ **[10] の正体** | Grothendieck comparison theorem の**書誌が pin 範囲外**(pp.43–55 に References なし)。SGA 1 と推定だが **UNKNOWN** | ★ 小(追加撮影候補 1) |
| ⚠ **$\Phi_1$ が pro-$l$** | Remark 1(p.54)が使用・"to be shown later"(I §5・**範囲外**)。⚠ ただし **Thm 1(i) 自体はこれを使わない** ⟹ **私の用途には不要** | 小 |
| **格** | ★ **proof-pinned candidate**(**cross-checked ではない**・Lean 未・**Sol 未監査**) |

$$\boxed{\ \Longrightarrow\ \textbf{(K9-UNRAM) は}\textbf{文献入力として閉じた}\textbf{。R1 の実質は完結し、残るのは}\textbf{監査}\ }$$

---

## H. 帰属・依存申告(v2 分)

- **頁画像の入手** = **研究者**(JSTOR 閲覧)。**pin 化** = **reader**(65b8356)。**配達・機構抽出** = 司令塔(裁定 931)。
- **本追記の新規部分**: ① 段 (3) の差し替えと格の昇格 ② ★ **縮約は 3 段でなく 4 段**という判定(段 (1) も落ちる — Ihara は proper な Fermat 曲線経由で私の開曲線ルートとは別機構)③ **検問 (i) の差 3 点の勘定**(特に **charming が pro-3 への落とし込みを担う**という機構)④ **検問 (ii)** と ★ **Belyi $\Phi^*$ の定義条件 = charming 条件という同定**(⟹ Prop 3 が正典側の橋)⑤ **【UNRAM-GAP-2】の pin による閉鎖と差の勘定** ⑥ **P-K9U-1 の条件 1 枚除去** ⑦ **便 119 P3③ 書換案**。
- **検算**: v2 で新規の機械検算はなし(v1 の $D_9$ 共役全数計算を継承)。⟹ **cross-checked ではない**。
- **未実施**: [10] の書誌確定・$\Phi_1$ pro-$l$ の確認(いずれも私の用途には不要)・Lean 未着手・**Sol 未監査**。⟹ **verified ではない**。
