# P4 設計束 v1 の検分(裁定 834①・835)

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5) / **状態**: candidate(Sol 未監査・判定語の発効は司令塔専権)
**対象**: `docs/notes/p4_design_bundle_v1.md`(e505363・発案係)/ 検分項 = 裁定 835 の ①②③
**姿勢**: 破壊歓迎の指示どおり、**通る所は理由を強め、通らない所は反例・訂正を出す**。

---

## §0 三行結論

| 札 | 判定 | 一行 |
|---|---|---|
| **P4-1** | ★ **縮退の読みは正しい。しかも札より強く縮退する** | 表結合ですらなく **1 個の等式 $\lvert\mathrm{Gal}(L_1L_2/\mathbf Q)\rvert=972$ の照合**に落ちる。ただし ★ **「entanglement は新しい故障型」という位置づけは誤り**(§1.3) |
| **P4-2** | **結論は正しいが消去補題 (L2) の理由が誤り** | 訂正証明を §2.2 に供給。$\dim\ge3$ OPEN 登録との整合は ✔ |
| **P4-3** | ★ **測定は不要 — 紙で答えが出る。$m_\chi=0$**(全 4 本) | Maschke + Fox-at-character で 3 行。⟹ **DOMAIN-PIN 不適合**(予言を置けるのに置いていない・§3) |

---

# §1 P4-1 CRT-ENTANGLE の検分

## 1.1 ★ 972 屋根で実験は「1 個の等式」に縮退する(札より強い)

$M=K^{(9)}\cap N_{S4}$ は**二窓の交わり**ゆえ **CRT-INJ**(candidate・`hunting_chapter_v1.md` §1.2)が適用でき
$$R:\ GT(M)\hookrightarrow GT(K^{(9)})\times GT(N_{S4})\quad\textbf{単射}$$
$$\Longrightarrow\ \lvert X\rvert=\lvert GT(M)\rvert=972\ (\textbf{実測}),\qquad A\subseteq X$$
$$\boxed{\ \Longrightarrow\ X\setminus A=\varnothing\iff \lvert A\rvert=972\iff\bigl\lvert\mathrm{Gal}(L_1L_2/\mathbf Q)\bigr\rvert=\frac{\lvert A_1\rvert\lvert A_2\rvert}{\lvert\mathrm{Gal}(L_1\cap L_2/\mathbf Q)\rvert}=972\ }$$
⟹ **元の全列挙も重複除去も不要。整数 1 個の照合。**(札 §1.3 の 4 段は (a) では 1 段に潰れる。)

★ **副次の利点(非対称性)**: 較正が上界までしか出ない場合($N_{S4}$ の 1 ビット帰着リスク・札 §1.4)、$A\subseteq A_{\rm ub}$ ゆえ
$$\lvert A_{\rm ub}\rvert<972\ \Longrightarrow\ X\setminus A\ne\varnothing\ (\textbf{陽性が確定})$$
**上界だけでも片側は結論できる。**逆($\lvert A_{\rm ub}\rvert=972$)は情報ゼロ。

## 1.2 ★★ Goursat 公式は正しい(裏取り)

札の $A=A_1\times_{\mathrm{Gal}(L_1\cap L_2)}A_2$ は、$A_i\cong\mathrm{Gal}(L_i/\mathbf Q)$ を前件として
$$\mathrm{Gal}(L_1L_2/\mathbf Q)\cong\mathrm{Gal}(L_1/\mathbf Q)\times_{\mathrm{Gal}(L_1\cap L_2/\mathbf Q)}\mathrm{Gal}(L_2/\mathbf Q)$$
という標準事実そのもの ✔。**前件 $A_i=\mathrm{Gal}(L_i/\mathbf Q)$ が S1(較正)の正確な内容**である旨を札に明記すべき。

## 1.3 ★★★ 位置づけの訂正 — **entanglement は「新しい故障型」ではない**

> ### 命題候補 **ENT-EQUIV**(candidate・本検分・repo 初出)
> $N=N_1\cap N_2$ とし CRT-INJ が成り立つとする。$N\subseteq N_i$ ゆえ $\mathrm{Ih}_{N_i}=R_i\circ\mathrm{Ih}_N$ で $A=R(\mathrm{im}\,\mathrm{Ih}_N)$、$X=R(GT(N))$、$R$ 単射。ゆえに
> $$\boxed{\ X\setminus A\ne\varnothing\iff GT(N)\ne\mathrm{im}(\mathrm{Ih}_N)\ }$$
> **すなわち entanglement 実験は、窓 $N$ における通常の全射性問題と**厳密に同値**である。**

⟹ 札 §1 冒頭の「**proxy なしで定義どおりの反例に届く唯一の既知経路**」は、**Sol の逐語引用としては可**だが、本設計の読みとしては訂正が要る:
> $$\boxed{\ \textbf{CRT-ENTANGLE の価値は「新しい故障型を撃つ」ことではなく、}\textbf{算術像 }A\ \textbf{を }L_1\cap L_2\ \textbf{のガロア論で}\textbf{計算可能にする}\textbf{ことにある。}}$$
★ B114-2 の反模型($GT(N)=C_2^2$・im $=$ 対角)も、$X\setminus A\ne\varnothing$ すなわち $N$ での非全射そのものであり、**Sol の指摘は「閉扉の論証が壊れた」であって「別の故障型がある」ではない** — 本検分は Sol と整合。

## 1.4 ⚠ **空振り化リスク(設計上の blocker 候補)**

ENT-EQUIV より、**$M=$ 972 屋根で「$GT(M)=$ 算術像」が既に確認済みなら P4-1(a) は最初から空**。
> $$\boxed{\ \textbf{発注前の必須確認: registry で「972 屋根の算術像 vs }\lvert GT(M)\rvert=972\textbf{」の比較が既に済んでいないか}}$$
> 済んでいれば (a) は**廃止**し、**未較正の対**(札の (b)(c))へ移す。**未較正であることが実験の前件**という逆説的な選定基準になる。

## 1.5 その他

- **カナリア $A\subseteq X$** は定理 ✔(札 §1.2 の記述で正しい)。
- **S3 の指数評価** $[B_3:N]\le\lvert G_1\rvert\lvert G_2\rvert/\lvert E\rvert$ は ✔(subdirect ゆえ)。ただし**等号は Goursat の全射性が要る**ので「$\le$」のままでよい ✔。

---

# §2 P4-2 W691-EXT の検分

## 2.1 消去補題の点検(4 本中 3 本 ✔・1 本は理由が誤り)

| # | 札の主張 | 判定 |
|---|---|---|
| **(L1) Borel** | 「生成トーラス $\le C_6$」 | ★ **✔ 正しい**。$H\le B=U\rtimes T$、$H\to B/U\cong T$ の像は可換 ⟹ $H^{ab}$ の商 ⟹ 位数 $\mid6$。位数 690 の元 $t$ は半単純ゆえ $B/U$ での像も位数 690 ⟹ $690\mid6$ で矛盾 ∎ |
| **(L2) $N(T)$** | 「$w$-剰余類は全対合 ⟹ $\langle$対合,3$\rangle\le D_6$」 | ✘ **理由が誤り**(§2.2 で訂正・**結論は正しい**) |
| **(L3) 例外** | $A_4,S_4,A_5$ に 690-元なし | ★ **✔**(位数 $\le120<690$) |
| **(L4) 部分体型** | $q=691$ 素数ゆえ空 | ★ **✔** |

## 2.2 ★ (L2) の訂正証明

**札の誤り**: $tw$($t=\mathrm{diag}(a,b)$)は $(tw)^2=ab\cdot I$ ゆえ、**対合になるのは $ab=1$ のときだけ** — 「$w$-剰余類は全対合」は偽。また結論の「$\le D_6$」も偽($(C_3\times C_3)\rtimes C_2$ 位数 18 がありうる)。

> ### 訂正(candidate・本検分)
> $H=\langle a,b\rangle\le N(T)$、$a^2=b^3=1$。$N(T)/T\cong C_2$ に位数 3 の元はない ⟹ **$b\in T$**。$a^2=1$ ゆえ $H\cap T=\langle b,\,aba^{-1}\rangle=\langle b,b^\sigma\rangle$($\sigma$ = 対角成分の入替)。
> $b,b^\sigma$ はともに位数 3 ⟹ **$H\cap T$ の指数は 3**。$[H:H\cap T]\le2$ ⟹ $H$ の元の位数は $\{1,2,3,6\}$ に限る。
> $$\boxed{\ \Longrightarrow\ H\ \textbf{に位数 690 の元はない}\ }\qquad\blacksquare$$
> ($a\in T$ の場合は $H\le T$ 可換で $(2,3)$-生成 ⟹ $\lvert H\rvert\le6$ ⟹ 同じ結論。)

## 2.3 分類の網羅性と $\delta\ne1$ 一般形への耐性

- **網羅性**: 札の 4 分類(Borel / トーラス正規化群 / 例外 / 部分体)は $GL_2(\mathbf F_q)$ 部分群の標準分類そのもの ✔。**ただし文献引用**【要 pin: **BR-LIT-1**(Dickson・未取得)】。札はこれを「数学者検分項」としており ✔ — **本検分の答えは「分類自体は引用であり、工房内に一次資料がない」**。
- ★ **B114-4 の一般形 $\{\chi,\delta\chi^{-1}\}$($\mathrm{ord}\,\delta\mid6$)への耐性**: (L1)〜(L4) はいずれも「位数 690 の元の**存在**」だけを使い $\det$ を使わない ⟹ **$\delta\ne1$ でもそのまま通る** ✔。**札はこれを明記していない** ⟹ 追記を推奨(EXHAUST の観点で重要)。
- **$\dim\ge3$ OPEN 登録との整合**: 札は「網羅」を $\dim W=2$ ∧ 分裂トーラス ∧ 位数 690 の層に**明示的にスコープ**しており ✔。§2.5 の P-W691-1 陰含意も「この層で閉(全域閉鎖は言わない)」✔ **EXHAUST 準拠**。

## 2.4 ★ 前提事実の補強(裁定 836 の線引きと HD-NOWIN)

- **段 1 の前件は満たされた**: `w691_gen23_witness_v1` で $H_2,H_6$ ともに `PROVEN_GENERATES` ⟹ $(2,3)$-生成 ⟹ $x=b^{-1}a,\ y=a^{-1}b^2$ で braid 関係($xyx=a=a^{-1}=yxy$)⟹ **$B_3$ 商として実現**(段①クリア)。
- ⚠★ **ただし $H_d$ 自身は窓ではない**(命題候補 **HD-NOWIN**・`見立て_相2_v1_3.md` §4.1): $H_d\twoheadrightarrow S_3$ は不可能($K\cap SL$ が $SL(2,691)$ の正規部分群 $\{1,\pm I,SL\}$ のいずれでも矛盾)。
> $$\boxed{\ \Longrightarrow\ \textbf{窓資格が要求されるのは }H_d\ \textbf{ではなく拡大 }E\ (1\to W\to E\to H_d\to1)\ \textbf{の側}\ }$$
> ⟹ **段 3 の braid lift は「$E$ が $B_3$ 商になるか」だけでなく「$E$ が窓になるか($E\twoheadrightarrow S_3$)」も見るべき**。札の段 3 は前者しか要求していない ⟹ **追加要求を推奨**($E$ は $W\cdot H_d$ で $W$ は $691$-群ゆえ $E\twoheadrightarrow S_3$ も同じ議論で不可能な可能性が高い — **これは段 3 の前に紙で片が付く懸念**)。
> ★ **これが本検分で最も重い指摘**: $W$ が $\mathbf F_{691}^2$ なら $E/W\cong H_d$ で、$E\twoheadrightarrow S_3$ の核は $W$ を含むか否か。含めば $H_d\twoheadrightarrow S_3$ となり HD-NOWIN で矛盾。含まなければ $W\cap\ker$ は $E$-部分加群で $W$ 既約ゆえ $0$ ⟹ $W\hookrightarrow S_3$ で位数矛盾。⟹ $$\boxed{\ E\ \textbf{も窓になれない(}W\ \textbf{既約のとき)— 段 2/3 を走らせる前に紙で閉じる可能性}\ }$$
> ⚠ **要検分**: $W$ が可約な場合・$H_d$ 以外の層。**これは札への差戻しではなく、段 1 と段 3 の間に「窓資格の紙検査」を 1 段挟む提案**。

## 2.5 段 2 の $\dim H^2\in\{0,1\}$

$v_{691}(\lvert H_d\rvert)=1$ ⟹ Sylow $=C_{691}$ 巡回 ⟹ $H^2(C_{691},W)$ が 1 次元 ⟹ 安定元で $\dim H^2(H,W)\in\{0,1\}$ — **論理は通る** ✔(旧 `pair_h2_design_draft_v1` からの再利用部品として妥当)。$\det$-捻り $i$ の $\le8$ 本全列挙も EXHAUST ✔。

---

# §3 ★★★ P4-3 CMP-REP-1 の検分 — **紙で答えが出る**

## 3.1 計算法は正しい

胞体複体 $\mathbf F_p[G]\xrightarrow{\partial_2=\mathrm{Fox}(r)}\mathbf F_p[G]^2\xrightarrow{\partial_1}\mathbf F_p[G]$ から $V_p(N)=\ker\partial_1/\mathrm{im}\,\partial_2$ は正しい ✔($\pi_1(\tilde K)=N$・$H_1(\tilde K;\mathbf F_p)=N^{ab}\otimes\mathbf F_p=N/[N,N]N^p$)。

## 3.2 ★ しかし規模見積りが過大 — **Maschke で潰れる**

$\lvert G\rvert=3240=2^3\cdot3^4\cdot5$ で **$11\nmid3240$** ⟹ $\mathbf F_{11}[G]$ は**半単純**(Maschke)⟹ 複体は等型成分に分解し、1 次元指標 $\chi$ の成分は
$$\mathbf F_{11}\ \xrightarrow{\ \partial_2^\chi\ }\ \mathbf F_{11}^2\ \xrightarrow{\ \partial_1^\chi\ }\ \mathbf F_{11}$$
の**3 項・全次元 $\le2$** の複体になる。⟹ $3240\times6480$ の疎行列は**不要**。

## 3.3 ★★★ Fox-at-character の計算(3 行)

$B_3=\langle x,y\mid r\rangle$、$r=xyx\,y^{-1}x^{-1}y^{-1}$。AB-CYC より $\chi(x)=\chi(y)=:\lambda$。
$$\partial_1^\chi=(\lambda-1,\ \lambda-1),\qquad \partial_2^\chi=\bigl(\chi(\partial r/\partial x),\ \chi(\partial r/\partial y)\bigr)=\bigl(\Phi_6(\lambda),\ -\Phi_6(\lambda)\bigr),\quad \Phi_6(\lambda)=\lambda^2-\lambda+1$$
($\Phi_6$ は三葉結び目 = $B_3$ の Alexander 多項式 — §2.1 の「6」と**同じ 6**)。

> ### 命題候補 **CMP-PHI6**(candidate・本検分・repo 初出)
> 任意の $N\trianglelefteq B_3$($G=B_3/N$ 有限)と 1 次元指標 $\chi:G\to\mathbf F_p^\times$ について
> $$\boxed{\ m_\chi\bigl(V_p(N)\bigr)=\begin{cases}1&\chi=1\\[2pt] 1-[\Phi_6(\lambda)\ne0]&\chi\ne1\end{cases}\quad\Longrightarrow\quad \chi\ne1:\ m_\chi\ne0\iff \mathrm{ord}(\chi)=6\ }$$
> **証明**: $\lambda\ne1$ なら $\dim\ker\partial_1^\chi=1$、$\mathrm{im}\,\partial_2^\chi=\langle(\Phi_6(\lambda),-\Phi_6(\lambda))\rangle\subseteq\ker\partial_1^\chi$ ⟹ $m_\chi=1-\mathrm{rank}$。$\Phi_6(\lambda)=0\iff\lambda$ は原始 6 乗根 $\iff\mathrm{ord}(\chi)=6$。$\lambda=1$ なら $\dim\ker=2$、$\Phi_6(1)=1\ne0$ ⟹ $m=1$。∎
> ★ **これは TWIST-6-ABS の「表現読み版」である** — 切片読みの「6」($PSL(2,\mathbf Z)^{\rm ab}=C_6$)と表現読みの「6」($\Phi_6$ = Alexander 多項式)が**同じ 6**。

## 3.4 ★ $M_5$, $p=11$ への適用 — **答えは 0**

$\mathbf F_{11}^\times\cong C_{10}$ で $6\nmid10$ ⟹ **$\mathbf F_{11}$ に原始 6 乗根は存在しない**(検算: $x^2-x+1$ の $\mathbf F_{11}$ 内の根は空)⟹ 全ての $\lambda\ne1$ で $\Phi_6(\lambda)\ne0$ ⟹
$$\boxed{\ m_\chi\bigl(V_{11}(M_5)\bigr)=0\quad\textbf{(位数 10 の指標 4 本すべて)}\ }$$

> ### ⟹ 検分の結論(P4-3)
> 1. ★ **測定は不要**(紙で決まる)。走らせるなら**確認測定**であって UNKNOWN 測定ではない。
> 2. ★ **DOMAIN-PIN 不適合**: 札は「予言を置かない(真の UNKNOWN 測定)」とするが、**予言は置ける** ⟹ IF-FIRST 規約により**凍結が義務**。差替案: **P-CMP-1a′ = 「$m_\chi=0$(全 4 本)」を凍結**。外れたら計算法か複体の同一視が誤り(**較正ゲート**)。
> 3. ★ **陰性の含意は札の想定より広い**: 「$M_5,p=11$ で閉」ではなく **CMP-PHI6 により全窓・全標数で「位数 6 以外の 1 次元指標は $V_p(N)$ に現れない」** ⟹ **この関手上の (B) 道は全域で閉じる**(EXHAUST: 1 次元指標に限る・高次元既約成分は OPEN)。
> 4. ⟹ **P4-3 は「実験」から「紙の命題 + 確認測定 + 次の設計(高次元成分)」へ再編を推奨。**

## 3.5 第二段(比較射 $c_N$)について

札が「未定義・設計課題」と正直に書いている点は ✔ **適切**。ただし §3.4-3 により、**第一段が全域で閉じるなら第二段の対象(1 次元 $\chi$-成分)が消える** ⟹ 比較射の設計は**高次元既約成分へ差し替え**るのが自然。

---

# §4 まとめ — 札への差戻し/強化の一覧

| 札 | 差戻し | 強化 |
|---|---|---|
| **P4-1** | ★ 位置づけを訂正(ENT-EQUIV: 通常の全射性と同値)/ ★ (a) の空振り化リスクを発注前に確認 | 実験を 1 個の等式へ縮退・上界だけでも片側結論可 |
| **P4-2** | (L2) の理由を訂正 / $\delta\ne1$ 耐性を明記 / ★ 段 1 と段 3 の間に**窓資格の紙検査**を挿入($E$ も窓になれない可能性) | (L1)(L3)(L4) 是認・網羅スコープは EXHAUST 準拠 ✔・段①は目撃者 cert でクリア |
| **P4-3** | ★ 「真の UNKNOWN」は誤り ⟹ **予言 $m_\chi=0$ を凍結**(DOMAIN-PIN 適合化) | Maschke+Fox で 3 行・**CMP-PHI6** で全域化・「6」の二読みの一致 |

## §5 【GAP】・帰属・novelty

| # | 内容 | 重さ |
|---|---|---|
| **【REV-GAP-1】** | ENT-EQUIV は CRT-INJ(candidate)に依存 | 中 |
| **【REV-GAP-2】** | §2.4 の「$E$ も窓になれない」は $W$ 既約を仮定 — 可約の場合は未検分 | ★ 中 |
| **【REV-GAP-3】** | CMP-PHI6 は $G$ 有限・$p\nmid\lvert G\rvert$(Maschke)を使う。$p\mid\lvert G\rvert$ の場合は別扱い | ★ 中 |
| **【BR-LIT-1】** | $GL_2(\mathbf F_q)$ 部分群分類は**引用**【要 pin: 未取得】 | 小 |

**帰属**: 三札の起草・972 屋根の即用性・層別台帳・消去補題の骨組み・$V_p$ 計算法・比較射 2 候補 = **発案係**(e505363)。仕様 = **Sol**(P4-1/2/3)。委嘱 = 司令塔(裁定 834①/835)。
**本検分の新規部分** = **§1.1 の 1 等式縮退と上界の非対称性** / **命題候補 ENT-EQUIV(entanglement は通常の全射性と同値)** / **§1.4 の空振り化リスク** / **(L2) の訂正証明** / **$\delta\ne1$ 耐性の指摘** / **§2.4 の窓資格紙検査($E$ も窓になれない)** / ★ **命題候補 CMP-PHI6 と $m_\chi=0$ の紙解** / **DOMAIN-PIN 不適合の指摘と P-CMP-1a′**。

**novelty grep**: `ENT-EQUIV` `CMP-PHI6` `P-CMP-1a′` `Fox-at-character` = **0 hit(本検分初出)**。`Φ₆`/`x^2-x+1` は `xd2_twist6abs_adjudication_v1.md` §2.1 に既在(Alexander 多項式として)⟹ **本検分はそれと表現読みの一致を指摘するもの**。

**検算**:
```bash
python -c "
p=11
print('roots of x^2-x+1 in F_11:', [a for a in range(p) if (a*a-a+1)%p==0])   # []
for lam in range(p):
    k = 2 if lam==1 else 1
    r = 0 if (lam*lam-lam+1)%p==0 else 1
    print(lam, 'm_chi =', k-r)
"   # lam=1 -> 1, その他すべて 0
```
