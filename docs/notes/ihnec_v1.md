# IH-NEC v1 — 中間峰(P2)から大山塊(P6)への必要条件鎖・E1-GAP-4 の有限問題族への翻訳

**状態札: candidate / 研究内部文書**(論文ではない)
起草: 数学者(Opus 5)/ 2026-08-01 ・ 委嘱 = **採択札 P6-3**(発案係第 17 便・裁定 355 で採択)

> ★ **【裁定 374 追補あり — 本文より先に末尾 §A を読むこと】**(2026-08-01 検収)
> ① **用語裁定**: 「fake」は正典 Def 4.2 準拠(**非 genuine**)に一本化。本文 §3.3 の「**B 型証人**」は以後 **「非算術証人」**と呼び、**fake と呼ばない**。⟹ **§3.3・§5.2・§5.5 T-2・§7・§8 の「A 型 / B 型」の語は §A.1 の対応表を通して読むこと。§3.3 を単独で引用しないこと**(差し替え本文は §A.2–§A.4)。
> ② **条文 pin 工程**: 定理 ML-ODD(§4)が依拠する正典 3 条文は **reader の逐語抽出待ち**。**照合 PASS までは ML-ODD を便に載せない・実測(R4a/R4b)を起票しない**。事前登録予言 P-IHN-1〜7 は**凍結のまま不変**(§A.5)。
> **v1 本文は書き換えていない**(`fam_u_assembly_v1.md` の erratum 方式に倣う)。
>
> ★ **【追補 B(裁定 376)で pin 差替完了 — §A.5 の pin 先表は §B.1 に置換】**(2026-08-01)
> ★★ **最重要**: 逐語照合で **2401 Prop 3.15 の証明は原論文に無い**(「読者演習」と明記)ことが判明。**ML-ODD の最重要依存なので §B.2 で自前証明を補完**した(非循環性も確認)。**§1 表の (DIR) 行は §B.3 で 2 行に分解**((INT)$=$3.15 交叉閉/(COF)$=$3.14 系 共終)。
記法: 正典 arXiv **2401.06870**(GTSh・genuine・ML・Thm 5.2 の正本)/ arXiv **2405.11725**(Conj 5.1・$K^{(n)}$ 族)。工房内の定義正本は `docs/week1-定義ノート.md`、中間峰の正典文書は `docs/notes/E1_gt_odd_dih_canonical_v1.md`(以下「E1 ノート」)。
**封印遵守: $K^{(5)}$ 非接触**($n=5$ は本稿の全ての量化・全ての実測設計から明示的に除外しない — 除外の必要が生じる箇所は無い。本稿は $n=5$ の**値**に一切触れず、$n=9$ のみを実測対象とする)。

> ## 0. 本稿が置くもの・置かないもの
>
> **置くもの**: ① 補題 IH-FACT(定義水準の分解・数行)② 定理候補 IH-NEC(P6 ⟹ P2 の必要条件鎖)③ 系 FAKE-KILL(その対偶 = P5 哨戒の P6 的意味づけ)④ **定理 ML-ODD**(E1-GAP-4 を「有限問題族」へ落とす同値)⑤ 定理 SPLIT-NULL(分裂屋根は fake を検出しない = 哨戒設計の負の定理)⑥ 前件表(FAM-U-ASM 方式)⑦ 実測 1 対の設計と**事前登録予言 7 本**。
> **置かないもの**: 新しい算術。**(IH-S)(井原全射部)も (PR-S^odd) も U-10 も、本稿は一切証明しない** — すべて前件として名前をつけて表に載せるだけである。②③ は論理的にはほぼ自明な合成であり、**本稿の仕事はその合成が通る「水準」を全部書き出して前件を一つも落とさないこと**にある(P6-3 の第 5 項)。④⑤ が本稿の実質的な数学である。

---

## 1. 記法(E1 ノート §1 から。再定義はしない)

E1 ノート §1.2–§1.5 の記法をそのまま使う。要点のみ再掲する。

- $\mathrm{NFI}_{PB_3}(B_3)$、$N_{\rm ord}$ (3.1)、$N_{F_2}$ (3.2)、$\mathrm{GT}(N)$、$\mathrm{GTSh}(K,N)$、reduction $R_{N,H}$ (3.60)($N\le H$ のとき)。
- **$I:=\mathrm{NFI}^{\rm isolated}_{PB_3}(B_3)$**(isolated 対象のなす poset)。**refinement 順序**を $N\succeq H:\iff N\subseteq H$ と書く(「$N$ は $H$ を細分する」)。$\mathrm{ML}:I\to\mathbf{FinGrp}$、$\mathrm{ML}(N)=\mathrm{GT}(N)$、$\mathrm{ML}(N\to H)=R_{N,H}$(2401 (5.1)(5.2))。
- $\mathcal{PR}_N:\widehat{GT}_{\rm gen}\to\mathrm{GT}(N)$(2401 §4)、$\mathrm{Ih}:G_{\mathbb Q}\hookrightarrow\widehat{GT}\subseteq\widehat{GT}_{\rm gen}$、$\mathrm{Ih}_N:=\mathcal{PR}_N\circ\mathrm{Ih}$ (1.11)。
- $\mathrm{GT}_{\rm arith}(N):=\mathrm{Ih}_N(G_{\mathbb Q})$ (1.12)、**$\mathrm{GT}_{\rm gen}(N):=\mathcal{PR}_N(\widehat{GT}_{\rm gen})$**(本稿の記号。正典は「genuine な shadow 全体」と書く)。
  $$\boxed{\ \mathrm{GT}_{\rm arith}(N)\ \subseteq\ \mathrm{GT}_{\rm gen}(N)\ \subseteq\ \mathrm{GT}(N)\ }\tag{1.A}$$
  **本稿は一貫してこの三層で考える。** E1-3(同値定理)は**左の包含が等号か**を問い、E1-GAP-4 は**右の包含が等号か**を問う。
- $\mathrm{Dih}^{\rm odd}=\{K^{(n)}\mid n\ \text{奇}\ \ge3\}$、$\mathrm{GT}^{\rm odd}_{\rm Dih}=\varprojlim_{n\ \text{奇}}\mathrm{GT}(K^{(n)})$、$\mathrm{Ih}^{\rm odd}=(\mathrm{Ih}_{K^{(n)}})_n$(E1-D3)。
- $\mathrm{pr}_n:\mathrm{GT}^{\rm odd}_{\rm Dih}\to\mathrm{GT}(K^{(n)})$(極限の射影)。

**正典の引用(再証明しない)**:

| 札 | 内容 | 出所 |
|---|---|---|
| **(E1-1)** | 全 $n\ge3$ で $K^{(n)}$ は isolated ⟹ $\mathrm{GT}(K^{(n)})=\mathrm{GTSh}(K^{(n)},K^{(n)})$ は有限群 | 2405 Lemma 4.2 / Thm 4.3 |
| **(LIM)** | $\Psi:\widehat{GT}_{\rm gen}\ \cong\ \varprojlim\mathrm{ML}$(群同型 + 位相同型) | **2401 Thm 5.2** |
| **(DIR)** | isolated $\cap$ isolated $=$ isolated ⟹ $I$ は refinement 順序で**有向**。かつ $N^\diamond$ の構成で $I$ は $\mathrm{NFI}$ の中で**共終** | **2401 Prop 3.15 / Prop 3.14** |
| **(HOM)** | isolated $N\le H$ で $R_{N,H}$ は群準同型 | 2401 Remark 3.16 |
| **(COR54)** | $[m,f]\in\mathrm{GT}(N)$ が genuine $\iff$ $\forall K\in\mathrm{NFI}_N(B_3)$ で $[m,f]\in\mathrm{Im}\,R_{K,N}$(**全細分に survive**)。fake $=$ ある細分で像に入らない | **2401 Cor 5.4** |
| **(THM44)** | $K^{(q)}\le K^{(n)}$ のとき $R_{K^{(q)},K^{(n)}}$ は全射 | 2405 Thm 4.4 |
| **(GENTLE)** | $\widehat{GT}$(hexagon×2 + **pentagon**・$\widehat{B_4}$ 内)$\subseteq$ $\widehat{GT}_{\rm gen}$(pentagon を $\hat f\in[\widehat F_2,\widehat F_2]^{\rm cl}$ に置換)。**$\widehat{GT}=\widehat{GT}_{\rm gen}$ は未解決** | 定義ノート §2;**U-10** |

---

## 2. 補題 IH-FACT — 定義水準の分解

まず $\mathcal{PR}^{\rm odd}$ を定義する(E1 ノートは【E1-GAP-4】の欄で名前だけ使っており、定義が本文に無い)。

> ### 補題 IH-0($\mathcal{PR}^{\rm odd}$ の well-defined 性)
> 奇 $d\mid n$($d,n\ \text{奇}\ \ge3$)に対し
> $$R_{K^{(n)},K^{(d)}}\circ\mathcal{PR}_{K^{(n)}}=\mathcal{PR}_{K^{(d)}}\ :\ \widehat{GT}_{\rm gen}\longrightarrow\mathrm{GT}(K^{(d)}).$$
> ゆえに
> $$\mathcal{PR}^{\rm odd}:=\bigl(\mathcal{PR}_{K^{(n)}}\bigr)_{n\ \text{奇}\ \ge3}\ :\ \widehat{GT}_{\rm gen}\longrightarrow\mathrm{GT}^{\rm odd}_{\rm Dih}$$
> は well-defined な**連続群準同型**であり、$\mathrm{pr}_n\circ\mathcal{PR}^{\rm odd}=\mathcal{PR}_{K^{(n)}}$ を満たす。

**証明.** $\mathcal{PR}_N(\hat m,\hat f)=(\hat m\bmod N_{\rm ord},\ \hat fN_{F_2})$、$R_{N,H}([m,f])=(m\bmod H_{\rm ord},\ fH_{F_2})$(2401 §4・(3.60))。補題 E1-D2(3) より奇 $d\mid n$ で $K^{(n)}\subseteq K^{(d)}$、したがって $K^{(d)}_{\rm ord}=2d\mid2n=K^{(n)}_{\rm ord}$ と $K^{(n)}_{F_2}\subseteq K^{(d)}_{F_2}$。両成分とも「二段の還元 $=$ 一段の還元」なので等式が成り立つ。準同型性は (E1-1)+(HOM)(E1 ノート補題 E1-3a と同じ論法 — **isolated 性が効く**)、連続性は各段が有限離散であることから。∎

> ### 補題 IH-FACT(**定義水準分解**)
> $$\boxed{\ \mathrm{Ih}^{\rm odd}\ =\ \mathcal{PR}^{\rm odd}\big|_{\widehat{GT}}\ \circ\ \mathrm{Ih}\ :\ G_{\mathbb Q}\longrightarrow\mathrm{GT}^{\rm odd}_{\rm Dih}\ }$$
> (連続群準同型としての等式)。

**証明.** 各奇 $n\ge3$ で
$$\mathrm{pr}_n\circ\bigl(\mathcal{PR}^{\rm odd}\circ\mathrm{Ih}\bigr)\overset{\text{補題 IH-0}}{=}\mathcal{PR}_{K^{(n)}}\circ\mathrm{Ih}\overset{(1.11)}{=}\mathrm{Ih}_{K^{(n)}}\overset{\text{E1-D3}}{=}\mathrm{pr}_n\circ\mathrm{Ih}^{\rm odd}.$$
$\mathrm{GT}^{\rm odd}_{\rm Dih}$ は逆極限だから $(\mathrm{pr}_n)_n$ は点を分離する。ゆえに二つの写像は等しい。$\mathrm{Ih}(G_{\mathbb Q})\subseteq\widehat{GT}$ なので左辺は制限 $\mathcal{PR}^{\rm odd}|_{\widehat{GT}}$ で書ける。∎

> **★ この補題が「数行」で済むことの意味**: $\mathrm{Ih}^{\rm odd}$ は **$G_{\mathbb Q}$ から中間峰への写像として新しく作られたものではなく**、正典の (1.11) $\mathrm{Ih}_N=\mathcal{PR}_N\circ\mathrm{Ih}$ を奇 dihedral 窓の族に沿って束ねただけである。すなわち $\mathrm{Ih}^{\rm odd}$ は
> $$G_{\mathbb Q}\ \xrightarrow{\ \mathrm{Ih}\ (\textbf{算術水準})\ }\ \widehat{GT}\ \xrightarrow{\ \subseteq\ (\textbf{U-10 水準})\ }\ \widehat{GT}_{\rm gen}\ \xrightarrow{\ \mathcal{PR}^{\rm odd}\ (\textbf{窓族水準})\ }\ \mathrm{GT}^{\rm odd}_{\rm Dih}$$
> の三水準の合成である。**IH-NEC も FAKE-KILL も、この三本の矢印のどれが全射かを問うているだけ**であって、それ以上の内容はない。逆に言えば**三本を一本と誤読すると前件が消える** — 本稿の全ての注意はここに集中する。

---

## 3. 定理候補 IH-NEC

### 3.1 前件の名前

| 札 | 言明 | 状態 |
|---|---|---|
| **(IH-S)** | $\mathrm{Ih}:G_{\mathbb Q}\to\widehat{GT}$ が**全射**(井原予想の全射部;単射は Belyi による正典の定理) | **UNKNOWN**(P6・大山塊) |
| **(PR-S$^{\rm odd}$)** | $\mathcal{PR}^{\rm odd}\big|_{\widehat{GT}}:\widehat{GT}\to\mathrm{GT}^{\rm odd}_{\rm Dih}$ が**全射** | **UNKNOWN**(本稿で名前をつけた。§4 で $\widehat{GT}_{\rm gen}$ 版に有限問題族の同値を与える) |
| **(U-10)** | $\widehat{GT}=\widehat{GT}_{\rm gen}$ | **UNKNOWN**(正典・E1 ノート §8.1) |

### 3.2 定理候補

> ### 定理候補 IH-NEC
> **(E1-1)** と **(E1-3)**(E1 ノート定理 E1-3 = odd Conj 5.1 $\iff$ $\mathrm{Ih}^{\rm odd}$ 全射;裁定 266 採択)の下で、
> $$\boxed{\ (\text{IH-S})\ \wedge\ (\text{PR-S}^{\rm odd})\ \Longrightarrow\ \mathrm{Ih}^{\rm odd}\ \text{全射}\ \overset{\text{E1-3}}{\Longleftrightarrow}\ \textbf{odd Conjecture 5.1}\ }$$

**証明.** 補題 IH-FACT より $\mathrm{Ih}^{\rm odd}=\mathcal{PR}^{\rm odd}|_{\widehat{GT}}\circ\mathrm{Ih}$。(IH-S) より $\mathrm{Ih}$ は $\widehat{GT}$ への全射、(PR-S$^{\rm odd}$) より $\mathcal{PR}^{\rm odd}|_{\widehat{GT}}$ は全射。全射の合成は全射。E1-3 で言い換える。∎

> ### 系 IH-NEC′(**「必要条件」としての読み** — これが札の名前の由来)
> **対偶**:
> $$\neg\,\textbf{odd Conj 5.1}\ \Longrightarrow\ \neg(\text{IH-S})\ \vee\ \neg(\text{PR-S}^{\rm odd}).$$
> すなわち **odd Conj 5.1(中間峰 P2 の本丸)は「井原予想の全射部 $\wedge$ 中間峰への射影の全射性」の必要条件である**。P2 が落ちれば、P6 か (PR-S$^{\rm odd}$) のどちらかが落ちる。
>
> ⚠ **ただし単独では P6 を殺さない**: $\neg$odd Conj 5.1 から $\neg$(IH-S) を取り出すには **(PR-S$^{\rm odd}$) を独立に持っている**必要がある。これが §4 の主題であり、§6 の実測設計の動機である。

> ### 注 IH-N1(**逆は成り立たない**)
> odd Conj 5.1 が真でも (IH-S) は従わない。$\mathrm{GT}^{\rm odd}_{\rm Dih}\cong\mathrm{Aff}(\widehat{\mathbb Z}^{\rm odd})\times C_2$(定理 E1-2)は**二段可解**であり、$\widehat{GT}$ の像のごく一部しか見ていない。**中間峰は井原予想の必要条件を一枚提供するだけで、十分条件には全く近づかない。** これは E1 ノート §5.7「中間峰の勘定の正直な形」と同じ規律を、$P2\to P6$ 方向にも明記したものである。

> ### 注 IH-N2(**U-10 は IH-NEC の前件ではない**)
> 定理 IH-NEC は $\widehat{GT}$ の中だけで閉じており、U-10 を使わない。U-10 が要るのは §3.3 の FAKE-KILL(と、(PR-S$^{\rm odd}$) を §4 の $\widehat{GT}_{\rm gen}$ 版と同一視するとき)だけである。**この分離を保つこと。**

### 3.3 系 FAKE-KILL(対偶系・P5 哨戒の P6 的意味づけ)

> ### 系 FAKE-KILL(**点ごとの最小形** — 前件は U-10 だけ)
> **(U-10)** の下で、**任意の**窓 $N\in\mathrm{NFI}_{PB_3}(B_3)$(dihedral でなくてよい・isolated でなくてよい)に
> $$g\in\mathrm{GT}_{\rm gen}(N)\setminus\mathrm{GT}_{\rm arith}(N)\qquad(\textbf{genuine だが非算術 = B 型証人})$$
> が **1 つでも**存在すれば、
> $$\boxed{\ \textbf{(IH-S)}\ \text{は偽 — すなわち井原予想の全射部が偽。}\ }$$

**証明.** $g$ が genuine ⟹ $g=\mathcal{PR}_N(\sigma)$ なる $\sigma\in\widehat{GT}_{\rm gen}$ が存在する。(U-10) より $\sigma\in\widehat{GT}$。もし (IH-S) が真なら $\sigma=\mathrm{Ih}(\gamma)$ なる $\gamma\in G_{\mathbb Q}$ があり、(1.11) より
$$g=\mathcal{PR}_N(\mathrm{Ih}(\gamma))=\mathrm{Ih}_N(\gamma)\in\mathrm{GT}_{\rm arith}(N),$$
これは $g$ が非算術であることに反する。∎

> **★ 最小形の値打ち**: 群構造も isolated 性も E1-3 も使わない — **集合水準の一行**である。ゆえに **dihedral 窓に限らない**(壁窓・PSL 窓・$K_\pi$ 窓でもよい)。**B 型証人はどこで見つけても P6 を殺す。**
> **★ 対偶(こちらが実質的な内容)**: **(IH-S) $\wedge$ (U-10) $\Longrightarrow$ 全窓 $N$ で $\mathrm{GT}_{\rm arith}(N)=\mathrm{GT}_{\rm gen}(N)$** — すなわち **B 型証人は 1 つも存在しない**。井原予想は「算術と genuine の一致」を全窓で強制する。

> ### 系 FAKE-KILL′(**窓の言葉で使う形** — B 型判定を (PR-S$^{\rm odd}_{\rm gen}$) が肩代わりする)
> 最小形の使用には「その証人が **genuine** であること」の証明が要る — 正典 Cor 5.4 より **これは有限深度では出ない**。そこを窓ぐるみの前件で肩代わりするのが実用形である。
> $$(\text{PR-S}^{\rm odd}_{\rm gen}):\quad\mathcal{PR}^{\rm odd}:\widehat{GT}_{\rm gen}\to\mathrm{GT}^{\rm odd}_{\rm Dih}\ \text{全射}\quad\overset{\textbf{定理 ML-ODD}}{\iff}\quad\text{全奇窓の全 shadow が genuine}$$
> この前件の下では**奇窓の非算術 shadow はすべて自動的に B 型**になる。ゆえに
> $$\boxed{\ (\text{PR-S}^{\rm odd}_{\rm gen})\ \wedge\ (\text{U-10})\ \wedge\ \bigl[\text{ある奇窓 }K^{(n)}\text{ に非算術 shadow が 1 つ}\bigr]\ \Longrightarrow\ \neg(\text{IH-S}).\ }$$
> **さらに弱い形で足りる**: 上の前件のうち必要なのは **その窓 $K^{(n)}$ ただ 1 つでの genuine 性**(ML-ODD (iii) の $n$ 成分)であって、全奇 $n$ での成立ではない。**実測設計はこの「1 窓分」を標的にすればよい**(§6・系 FK-Q7)。
> **⚠ (U-10) を落とすと**: 証人は「$\widehat{GT}_{\rm gen}$ からの全射性」の話で止まり、**井原予想($\widehat{GT}$ 版)には届かない**。これが罠 T-1(完備化規約)の実効的な現れであり、**本札で最もありそうな事故**である。
>
> ⚠ **$\widehat{GT}$ 版の前件 (PR-S$^{\rm odd}$) を直接持てるなら U-10 は不要**(その場合は §3.2 の系 IH-NEC′ の対偶がそのまま働く)。ただし **(PR-S$^{\rm odd}$) を有限計算に落とす経路は本稿には無い** — 定理 ML-ODD が翻訳するのは $\widehat{GT}_{\rm gen}$ 版だけである(【IHNEC-GAP-3】)。

> ### ⚠ 注意 FK-TYPE(**「fake」の二義 — 正典と工房で語が食い違っている**)
> **正典 Def 4.2**: genuine $=$ $\widehat{GT}_{\rm gen}$ の元の射影。**それ以外を fake と呼ぶ**。すなわち正典の fake $=$ **非 genuine**。
> **工房の地図 P1 行**: 「1 つの窓で非全射 $=$ fake witness」— こちらは **非算術**の意味で使っている。
> (1.A) の三層でこの二つは別物である。証人を二型に分ける:
>
> | 型 | 定義 | 単独で殺すもの(追加前件なし) | 追加前件つきで殺すもの |
> |---|---|---|---|
> | **A 型**(**正典の fake**) | $g\in\mathrm{GT}(K^{(n)})\setminus\mathrm{GT}_{\rm gen}(K^{(n)})$ | **odd Conj 5.1(P1/P2)**(arith $\subseteq$ gen より)/ **(PR-S$^{\rm odd}_{\rm gen}$) 自身** | ★ **なし。A 型は (PR-S$^{\rm odd}_{\rm gen}$) と両立しないので前件が消え、P6 には何も言えない** |
> | **B 型**(genuine だが非算術) | $g\in\mathrm{GT}_{\rm gen}(N)\setminus\mathrm{GT}_{\rm arith}(N)$(**窓は任意**) | **odd Conj 5.1(P1/P2)**($N$ が奇 dihedral 窓のとき) | ★ **(U-10) だけで (IH-S) $=$ 井原全射部**(系 FAKE-KILL 最小形) |
>
> **非算術 shadow は A 型か B 型のいずれか**(排他的)。**(PR-S$^{\rm odd}_{\rm gen}$) は奇窓での A 型を排除する ⟹ 残る全ては B 型 ⟹ (U-10) と合わせて FAKE-KILL′ が発火する。** これが系 FAKE-KILL′ の内実である。
>
> ### ★ P5 哨戒の P6 的意味づけ(3 行)
> 1. **P5 哨戒(A 型 = 正典 fake の探索・「全細分に survive するか」)が witness を出しても、それは P1/P2 を殺すだけで P6 は生き残る。** A 型は (PR-S$^{\rm odd}_{\rm gen}$) の反例であって (IH-S) の反例ではない。**現在の哨戒(細分での survive 判定)が測っているのは A 型である。**
> 2. **P6 を殺すのは B 型**であり、B 型の証人は「genuine であること」を示す必要がある。正典 Cor 5.4 により **fake は有限証明書 1 個で確定するが genuine は有限深度では確定しない** — したがって **B 型の証人は原理的に「有限深度の PASS」からは作れない**(工房の掟 2「genuine を有限深度の PASS から導かない」と同じ壁)。
> 3. ゆえに **B 型の実用的な入手経路は「その窓で genuine 性(= ML-ODD (iii) の 1 成分)を先に証明し、然る後に非算術性を測る」**の一本である。§4 はその「窓ごとの genuine 性」を**有限問題族**に翻訳する。**非算術性の側は工房が既に装置をもつ**(定理 $R^{\rm cyc}_{\rm formal}$ = $\mathrm{ord}(a_n)\ne n$)⟹ **B 型探索は「genuine 側の証明」一点に律速される。**

> ### 系 FK-Q7(**前線 q=7 への適用 — 帰結の型だけ**)
> $q=7$ の右枝($[u_7]_2=[3]$;E1 ノート §5.2)が実現すれば $\mathrm{ord}(a_7)\ne7$、定理 $R^{\rm cyc}_{\rm formal}$ の全前件の下で $\mathrm{Ih}_{K^{(7)}}$ は**非全射** — すなわち $K^{(7)}$ に**非算術 shadow が存在する**。このとき
> $$\text{右枝}\ \wedge\ \bigl[\ \mathrm{GT}(K^{(7)})\ \text{の全 shadow が genuine}\ \bigr]\ \wedge\ (\text{U-10})\ \Longrightarrow\ \textbf{井原予想の全射部が偽}.$$
> **追加で要るのは「$n=7$ 窓ただ 1 つでの genuine 性」だけ**であり、それは §4 定理 ML-ODD の証明中の (ii)$\iff$(iii) の $n=7$ 成分 — すなわち **$K^{(7)}$ の全 isolated 細分 $N$ で $R_{N,K^{(7)}}$ が全射**(正典 Cor 5.4)という有限問題族である。**全奇 $n$ での (PR-S$^{\rm odd}_{\rm gen}$) は要らない。**
> ⚠ **事前確率は低い**(i17 §4 の抑制条項)。本系は「右枝が出たら何がどこまで届くか」の**型**を確定するだけであり、右枝を予測するものではない。

---

## 4. 【E1-GAP-4】の Mittag-Leffler 型翻訳(**本稿の主定理**)

### 4.1 問題の再掲

E1-GAP-4(E1 ノート §8):
> $\mathcal{PR}^{\rm odd}:\widehat{GT}_{\rm gen}\to\mathrm{GT}^{\rm odd}_{\rm Dih}$ の全射性は別主張であり、**$\mathrm{Dih}^{\rm odd}$ が isolated poset の中で cofinal でない以上、2401 Thm 5.2 から自動では出ない**。状態 **UNKNOWN**。

$\mathrm{Dih}^{\rm odd}$ が $I$ の中で共終でないのは正しい(例: $\mathrm{PSL}(2,8)$ 窓は $\mathrm{Dih}^{\rm odd}$ のどの元も細分しない — §6.2 で証明する)。したがって $\varprojlim_I\to\varprojlim_{\mathrm{Dih}^{\rm odd}}$ は同型ではない。**本節はこの写像の像を有限段の言葉で完全に決定する。**

### 4.2 補助補題

> ### 補題 ML-1(**$\mathrm{Dih}^{\rm odd}$ の下方閉包**)
> 奇 $a,b\ge3$ に対し $K^{(a)}\cap K^{(b)}=K^{(\mathrm{lcm}(a,b))}$。ゆえに任意の $N\in\mathrm{NFI}_{PB_3}(B_3)$ に対し
> $$D(N):=\{\,d\ \text{奇}\ \ge3\ \mid\ N\subseteq K^{(d)}\,\}$$
> は**有限**で、**約数について閉じ、$\mathrm{lcm}$ について閉じる**。とくに $D(N)\ne\emptyset$ なら $n(N):=\mathrm{lcm}\,D(N)\in D(N)$ であり、$D(N)=\{d\ \text{奇}\ \ge3:d\mid n(N)\}$。

**証明.** $c:=\mathrm{lcm}(a,b)$。$a\mid c$ より $D_c\twoheadrightarrow D_a$ が $r\mapsto r$、$s\mapsto s$ で定まり $\psi_a$ は $\psi_c$ を経由する、ゆえに $K^{(c)}\subseteq K^{(a)}$、同様に $\subseteq K^{(b)}$。逆に $\mathbb Z/c\hookrightarrow\mathbb Z/a\times\mathbb Z/b$($1\mapsto(1,1)$;核は $\mathrm{lcm}$ の定義から自明)より $D_c\hookrightarrow D_a\times D_b$、したがって $\ker(\psi_a\times\psi_b)=\ker\psi_c$、すなわち $K^{(a)}\cap K^{(b)}=K^{(c)}$。
有限性: $N\subseteq K^{(d)}$ なら $B_3/N\twoheadrightarrow B_3/K^{(d)}$ より $K^{(d)}_{\rm ord}=2d$ は $N_{\rm ord}$ を割る、ゆえに $d\le N_{\rm ord}/2$。約数閉性は補題 E1-D2(3)(奇 $d'\mid d$ $\Rightarrow$ $K^{(d)}\subseteq K^{(d')}$)。$\mathrm{lcm}$ 閉性は前段。∎

> ### 補題 ML-2(**$N_{\rm ord}$ の単調性** — 比較可能性の数値篩)
> $N\subseteq H$($N,H\in\mathrm{NFI}_{PB_3}(B_3)$)ならば $H_{\rm ord}\mid N_{\rm ord}$。

**証明.** $B_3/N\twoheadrightarrow B_3/H$ の下で $\mathrm{ord}(xH)\mid\mathrm{ord}(xN)$、$y,c$ も同様。(3.1) の $\mathrm{lcm}$ を取る。∎

> ### 補題 ML-3(**逆極限の像 = 安定像**;標準)
> 有向 poset 上の**有限**集合の逆系で全ての項が空でないものは、逆極限が空でない。とくに $I$ 上の逆系 $\{Y_i\}$ で全 $Y_i\ne\emptyset$ なら $\varprojlim Y\ne\emptyset$。

**証明.** 有限離散空間の逆系の極限はコンパクト空間の共通部分として空でない(Bourbaki の標準結果;有向 $=$ cofiltered が効く)。$I$ の有向性は (DIR)。∎

### 4.3 主定理

> ### 定理 ML-ODD(**E1-GAP-4 の有限問題族への翻訳**)
> **(E1-1)(LIM)(DIR)(COR54)(THM44)** の下で、次は同値。
>
> **(i)** $\mathcal{PR}^{\rm odd}:\widehat{GT}_{\rm gen}\to\mathrm{GT}^{\rm odd}_{\rm Dih}$ が**全射**。
> **(ii)** すべての奇 $n\ge3$ とすべての $N\in I$ with $N\subseteq K^{(n)}$ に対し
> $$R_{N,K^{(n)}}:\mathrm{GT}(N)\longrightarrow\mathrm{GT}(K^{(n)})\quad\textbf{が全射}.$$
> **(iii)** すべての奇 $n\ge3$ で $\mathrm{GT}(K^{(n)})$ の**全 shadow が genuine**、すなわち $\mathrm{GT}_{\rm gen}(K^{(n)})=\mathrm{GT}(K^{(n)})$。
>
> $$\boxed{\ \textbf{E1-GAP-4}\ \iff\ \text{各奇窓での }\textbf{有限問題族}\ \{R_{N,K^{(n)}}\ \text{全射}\}_{N\in I,\ N\subseteq K^{(n)}}\ }$$

**証明.**

**(ii) $\iff$ (iii).** (COR54) より $[m,f]\in\mathrm{GT}(K^{(n)})$ が genuine $\iff$ 全ての細分 $K\in\mathrm{NFI}_{K^{(n)}}(B_3)$ で $[m,f]\in\mathrm{Im}\,R_{K,K^{(n)}}$。したがって
$$\mathrm{GT}_{\rm gen}(K^{(n)})=\bigcap_{K\subseteq K^{(n)}}\mathrm{Im}\,R_{K,K^{(n)}}.$$
各 $\mathrm{Im}\,R\subseteq\mathrm{GT}(K^{(n)})$ だから、この共通部分が全体 $\iff$ 各 $\mathrm{Im}\,R$ が全体。**isolated への制限で十分**であること: 任意の $K\in\mathrm{NFI}$ に対し (DIR) の $K^\diamond\subseteq K$ は isolated で、$R_{K^\diamond,K^{(n)}}=R_{K,K^{(n)}}\circ R_{K^\diamond,K}$ ゆえ $\mathrm{Im}\,R_{K^\diamond,K^{(n)}}\subseteq\mathrm{Im}\,R_{K,K^{(n)}}$。よって isolated だけを走らせた共通部分は同じ。∎(この段)

**(i) $\Rightarrow$ (iii).** $g\in\mathrm{GT}(K^{(n)})$ を任意に取る。補題 E1-3d((THM44) から従う)より $\mathrm{pr}_n$ は全射なので $y\in\mathrm{GT}^{\rm odd}_{\rm Dih}$ を $\mathrm{pr}_n(y)=g$ に取れる。(i) より $\sigma\in\widehat{GT}_{\rm gen}$ が $\mathcal{PR}^{\rm odd}(\sigma)=y$ を満たす。補題 IH-0 より $\mathcal{PR}_{K^{(n)}}(\sigma)=\mathrm{pr}_n(y)=g$、すなわち $g$ は genuine。

**(iii) $\Rightarrow$ (i).** $y=(y_d)_{d\ \text{奇}\ \ge3}\in\mathrm{GT}^{\rm odd}_{\rm Dih}$ を取る。各 $N\in I$ に対し
$$Y_N:=\{\,x\in\mathrm{GT}(N)\ \mid\ \forall d\in D(N):\ R_{N,K^{(d)}}(x)=y_d\,\}$$
と置く($D(N)=\emptyset$ なら $Y_N:=\mathrm{GT}(N)$)。

*(a) $\{Y_N\}$ は逆部分系.* $N\subseteq N'$($N,N'\in I$)なら $D(N)\supseteq D(N')$ で、$x\in Y_N$、$d\in D(N')$ に対し $R_{N',K^{(d)}}(R_{N,N'}(x))=R_{N,K^{(d)}}(x)=y_d$。

*(b) $Y_N\ne\emptyset$.* $D(N)=\emptyset$ なら明らか($\mathrm{GT}(N)\ni[0,1]$)。$D(N)\ne\emptyset$ とし $n_0:=n(N)$(補題 ML-1)と置く。$y$ の整合性より、$d\mid n_0$ なる全 $d\in D(N)$ については $y_d=R_{K^{(n_0)},K^{(d)}}(y_{n_0})$ が自動的に従う。ゆえに
$$Y_N=R_{N,K^{(n_0)}}^{-1}\bigl(y_{n_0}\bigr).$$
(iii) より $y_{n_0}$ は genuine、(COR54) より $y_{n_0}\in\mathrm{Im}\,R_{K,K^{(n_0)}}$ が**全ての**細分 $K\subseteq K^{(n_0)}$ で成り立つ。$N\subseteq K^{(n_0)}$ だからとくに $K=N$ で成立、すなわち $Y_N\ne\emptyset$。

*(c) 合成.* (a)(b) と補題 ML-3 より $\varprojlim_I Y\ne\emptyset$。その元 $\sigma$ は (LIM) により $\widehat{GT}_{\rm gen}$ の元を与える。$N=K^{(n)}$ のとき $D(K^{(n)})=\{d\ \text{奇}\ \ge3:d\mid n\}$、$n(K^{(n)})=n$ なので $Y_{K^{(n)}}=\{y_n\}$、ゆえに $\mathcal{PR}_{K^{(n)}}(\sigma)=y_n$ が全 $n$ で成り立つ。すなわち $\mathcal{PR}^{\rm odd}(\sigma)=y$。$\blacksquare$

### 4.4 定理 ML-ODD の読み

> ### 系 ML-A(**三層の中での位置**)
> (1.A) の三層に対し、各奇窓 $K^{(n)}$ で
> $$\underbrace{\mathrm{GT}_{\rm arith}(K^{(n)})}_{\text{E1-3 / Conj 5.1 が問う}}\ \subseteq\ \underbrace{\mathrm{GT}_{\rm gen}(K^{(n)})=\bigcap_{N\in I,\ N\subseteq K^{(n)}}\mathrm{Im}\,R_{N,K^{(n)}}}_{\textbf{ML-ODD が問う(安定像)}}\ \subseteq\ \mathrm{GT}(K^{(n)}).$$
> **右の $\mathrm{Im}\,R_{N,K^{(n)}}$ は((E1-1)(HOM) より)有限群 $\mathrm{GT}(K^{(n)})$ の部分群の減少有向族**であり、$\lvert\mathrm{GT}(K^{(n)})\rvert=2n\varphi(n)$ が有限だから**必ず停留する**(Mittag-Leffler 条件が自動で成立)。停留値が $\mathrm{GT}_{\rm gen}(K^{(n)})$ である。

> ### 系 ML-B(**odd Conj 5.1 ⟹ (i)**;既知の含意の再確認)
> arithmetical $\Rightarrow$ genuine より、odd Conj 5.1 $\Rightarrow$ (iii) $\Rightarrow$ (i)。**逆は不明**(E1 ノート §3.2 注と整合)。したがって **(PR-S$^{\rm odd}$) は odd Conj 5.1 より真に弱い可能性がある命題**であり、系 FAKE-KILL がそれを前件に置くのは循環ではない。

> ### 系 ML-C(**$\mathrm{Dih}^{\rm odd}$ 内部だけでは何も分からない**;正典の観察の定量化)
> 2401 §4 の観察「$\mathrm{Dih}$ 内 reduction は全射ゆえ $\mathrm{Dih}$ 内部だけでは fake は見つからない」は、ML-ODD の言葉では
> $$\bigcap_{N\in\mathrm{Dih}^{\rm odd},\ N\subseteq K^{(n)}}\mathrm{Im}\,R_{N,K^{(n)}}=\mathrm{GT}(K^{(n)})\qquad(\text{(THM44)})$$
> である。すなわち **(ii) の量化を $\mathrm{Dih}^{\rm odd}$ に制限すると恒真になる。(ii) の内容はすべて「$\mathrm{Dih}^{\rm odd}$ の外の isolated 細分 $N$」に載っている。** ⟹ **E1-GAP-4 を攻める実測は、必ず非 dihedral な細分を作るところから始まる**(§6 の設計はこれに従う)。

> ### 系 ML-D(**点ごと版** — 実測と FK-Q7 が使うのはこちら)
> 奇 $n\ge3$ を**固定**して
> $$\bigl[\mathrm{GT}(K^{(n)})\ \text{の全 shadow が genuine}\bigr]\iff\bigl[\forall N\in I,\ N\subseteq K^{(n)}:\ R_{N,K^{(n)}}\ \text{全射}\bigr]$$
> — これは (COR54) そのものである(本稿の寄与ではない)。**本稿が新しく置いたのは、この点ごとの条件を全奇 $n$ で束ねると (i) $\mathcal{PR}^{\rm odd}$ の全射性に一致するという一段**(定理 ML-ODD の (iii)$\Rightarrow$(i);コンパクト性 + 補題 ML-1)である。
> ⟹ **系 FAKE-KILL′ と系 FK-Q7 が要求するのは点ごと版 (ML-D) であって全体版 (i) ではない。**

> ### 【IHNEC-GAP-1】(**埋めていない**)
> (ii) は各 $(N,n)$ については有限計算だが、**$N$ の量化は無限**である。停留は保証されるが「どの $N$ で停留するか」の**上界を与える装置は無い**。したがって ML-ODD は **UNKNOWN を有限問題族へ翻訳した**のであって、**決定手続きを与えたのではない**。
> **要る型**: 奇 $n$ に対し「$\mathrm{GT}_{\rm gen}(K^{(n)})=\mathrm{Im}\,R_{N_0,K^{(n)}}$ となる明示的 $N_0$」あるいは「有限個の $N$ で停留を保証する構造的理由」。**状態: UNKNOWN。**

> ### 【文献要請 IHNEC-L1】
> **困難**: 有限群の逆系 $\{\mathrm{GT}(N)\}_{N\in I}$ について、部分 poset $J\subseteq I$(共終でない)への射影 $\varprojlim_I\to\varprojlim_J$ の像を、$J$ の各点での「安定像」以外の不変量で下から評価する機構が欲しい。とくに **$J$ が可解商の族(本件では $\mathrm{Aff}(\widehat{\mathbb Z}^{\rm odd})\times C_2$)で、$I$ が非可解商を含む**という非対称性を使いたい。
> **欲しい結果の型**: 「$\varprojlim_I G_i\twoheadrightarrow\varprojlim_J G_j$ が、$J$ の各段で $\mathrm{Im}$ が停留していれば全射」— これは本稿定理 ML-ODD として自前で得た。**その先** = 「停留の深さの上界」を与える型の結果(pro-群の Mittag-Leffler 条件の有効版・有限性定理)。

---

## 5. 前件表(**FAM-U-ASM 方式** — `fam_u_assembly_v1.md` §V.2/§V.5 の様式に倣う)

### 5.1 最短鎖(IH-NEC / FAKE-KILL の導出に**実際に使う段だけ**)

| 段 | 内容 | 使う前件 |
|---|---|---|
| **(A0)** | 定義: $\mathrm{Ih}$、$\mathcal{PR}_N$、$\mathrm{Ih}_N=\mathcal{PR}_N\circ\mathrm{Ih}$ (1.11) | 正典の定義のみ |
| **(A1)** | (E1-1) ⟹ $\mathrm{GT}(K^{(n)})$ は有限群、$\mathcal{PR}_{K^{(n)}}$ と $\mathrm{Ih}_{K^{(n)}}$ は群準同型 | **(E1-1)**・2405 Remark 1.4・Prop 3.14 |
| **(A2)** | reduction 整合 ⟹ $\mathcal{PR}^{\rm odd}$・$\mathrm{Ih}^{\rm odd}$ が well-defined(補題 IH-0・E1-3b/3c) | (A1)・(3.60)・E1-D2(3) |
| **(A3)** | **補題 IH-FACT**: $\mathrm{Ih}^{\rm odd}=\mathcal{PR}^{\rm odd}\vert_{\widehat{GT}}\circ\mathrm{Ih}$ | (A2)・極限の分離性 |
| **(A4)** | (IH-S) $\wedge$ (PR-S$^{\rm odd}$) ⟹ $\mathrm{Ih}^{\rm odd}$ 全射 | **(IH-S)**・**(PR-S$^{\rm odd}$)** |
| **(A5)** | E1-3 ⟹ **odd Conj 5.1** | **(E1-3)**(その内部で E1-3d ⟸ (THM44)、コンパクト性) |
| **(A6)** | 対偶 ⟹ **FAKE-KILL(素形)** | (A5) のみ(**U-10 は不要**) |
| **(A7)** | (PR-S$^{\rm odd}_{\rm gen}$)$+$(U-10) $\Rightarrow$ (PR-S$^{\rm odd}$) ⟹ **FAKE-KILL′(実用形)** | **(U-10)**。**ここだけが U-10 の効き所** |

**終点 = odd Conj 5.1(A5)/ (IH-S) の否定(A6)(A7)。鎖は 6 段 + 2。**

### 5.2 前件表(**落とすと何が壊れるか**を明記)

| 札 | 言明 | 格 | 出所 | **落とすと壊れるもの** |
|---|---|---|---|---|
| **(E1-1)** | 全 $n\ge3$ で $K^{(n)}$ isolated | **正典の定理** | 2405 Lemma 4.2/Thm 4.3 | (A1) が消え $\mathrm{GT}(K^{(n)})$ に群構造が無い ⟹ **「全射」を群論の言葉で扱えない**(E1 ノート「E1-1 の効き所」) |
| **(E1-3)** | odd Conj 5.1 $\iff$ $\mathrm{Ih}^{\rm odd}$ 全射 | **紙上相互監査 PASS**(裁定 266 採択) | 便 75 F6.2(d)・E1 ノート §3.2 | (A5) が消え、結論が「極限への全射」止まりで**有限段の主張に翻訳できない** |
| **(THM44)** | $\mathrm{Dih}$ 内 reduction 全射 | **正典の定理** | 2405 Thm 4.4 | E1-3d(= $\mathrm{pr}_n$ 全射)が消え、**E1-3 の (ii)$\Rightarrow$(i) と ML-ODD の (i)$\Rightarrow$(iii) の両方**が壊れる |
| **(LIM)** | $\widehat{GT}_{\rm gen}\cong\varprojlim\mathrm{ML}$ | **正典の定理** | 2401 Thm 5.2 | ML-ODD (iii)$\Rightarrow$(i) の最後の一段(極限の元を $\widehat{GT}_{\rm gen}$ の元と読む)が消える |
| **(DIR)** | $I$ が有向・$\mathrm{NFI}$ で共終 | **正典の定理** | 2401 Prop 3.15 / Prop 3.14 | **補題 ML-3 が使えない** ⟹ ML-ODD (iii)$\Rightarrow$(i) が壊れる。また (ii) の「isolated に制限してよい」が壊れる |
| **(COR54)** | genuine $\iff$ 全細分に survive | **正典の定理** | 2401 Cor 5.4 | ML-ODD (ii)$\iff$(iii) が壊れる |
| **(HOM)** | isolated 間の $R$ は群準同型 | **正典の定理** | 2401 Remark 3.16 | 系 ML-A の「部分群の減少族」が「部分集合の減少族」に落ちる(**停留性そのものは保つ** — 有限集合でも減少族は停留する。**格下げであって破綻ではない**) |
| **(IH-S)** | $\mathrm{Ih}:G_{\mathbb Q}\twoheadrightarrow\widehat{GT}$ | ★ **UNKNOWN**(P6) | 正典(井原予想) | IH-NEC の前提そのもの |
| **(PR-S$^{\rm odd}$)** | $\mathcal{PR}^{\rm odd}\vert_{\widehat{GT}}$ 全射(**$\widehat{GT}$ 版**) | ★ **UNKNOWN**(本稿で命名) | 本稿 §3.1 | IH-NEC の前提そのもの。**FAKE-KILL(素形)ではこれが A 型証人を排除する役** |
| **(PR-S$^{\rm odd}_{\rm gen}$)** | $\mathcal{PR}^{\rm odd}$ 全射(**$\widehat{GT}_{\rm gen}$ 版**) | ★ **UNKNOWN**(本稿で命名)。**§4 で有限問題族 (ii)(iii) と同値** | 本稿 §3.3・§4.3 | これだけでは (IH-S) に届かない。**(U-10) と対で使う** |
| **(U-10)** | $\widehat{GT}=\widehat{GT}_{\rm gen}$ | ★ **UNKNOWN**(正典) | 定義ノート §2 | **(A7)/FAKE-KILL′ のみ**に効く。落とすと (PR-S$^{\rm odd}_{\rm gen}$) から (PR-S$^{\rm odd}$) へ渡れず、証人は $\widehat{GT}_{\rm gen}$ の話で止まり**井原予想($\widehat{GT}$ 版)には届かない**(罠 T-1) |
| **(CPT)** | 有向 poset 上の空でない有限集合の逆系は極限が空でない | **標準**(Bourbaki) | 補題 ML-3 | ML-ODD (iii)$\Rightarrow$(i) が壊れる |

### 5.3 **除外欄**(= 前件では**ない**もの・混ぜないこと)

| 除外するもの | 理由 |
|---|---|
| **定理 E1-2**($\mathrm{GT}^{\rm odd}_{\rm Dih}\cong\mathrm{Aff}(\widehat{\mathbb Z}^{\rm odd})\times C_2$) | IH-NEC・FAKE-KILL・ML-ODD のどれにも使わない。構造は**注 IH-N1(逆が成り立たない理由)の説明**にしか現れない |
| **E1-4**($\Phi$-fam の忠実性) | 使わない |
| **(S3) / 定理 $R^{\rm cyc}_{\rm formal}$ / CASC / $q=7$ の 1 ビット** | **系 FK-Q7 の中でしか現れない**。IH-NEC 本体・ML-ODD には不要 |
| **(W2)-fam / W2-arith / (CAL) / (TB$*$)** | 本稿の主鎖には現れない。**§6.4 の系 SPLIT-NULL′(強形)の一つの導出経路にだけ現れ、そこでは代替経路(実測値)を用意した** |
| **U-10** | **IH-NEC 本体では前件ではない**(注 IH-N2)。**FAKE-KILL 系((A6)(A7))でのみ前件** |
| **$K^{(5)}$ 関連の一切** | 封印。本稿は $n=5$ の値に触れない |

### 5.4 矢印表(**距離の図** — 一本矢印にしない)

| 矢印 | 内容 | 格・条件 |
|---|---|---|
| **(α)** | $G_{\mathbb Q}\to\widehat{GT}$ 全射 | ★ **(IH-S) = UNKNOWN(P6 そのもの)** |
| **(β)** | $\widehat{GT}\subseteq\widehat{GT}_{\rm gen}$ が等号 | ★ **(U-10) = UNKNOWN(正典)** |
| **(γ)** | $\widehat{GT}_{\rm gen}\to\mathrm{GT}^{\rm odd}_{\rm Dih}$ 全射 | ★ **§4 定理 ML-ODD で有限問題族 (ii)(iii) と同値**。UNKNOWN だが**翻訳済** |
| **(δ)** | $\mathrm{Ih}^{\rm odd}$ 全射 $\iff$ odd Conj 5.1 | **紙上相互監査 PASS**(E1-3・裁定 266) |
| **(ε)** | odd Conj 5.1 $\iff$ 全奇 $n$ で $\mathrm{ord}(a_n)=n$ | **candidate / framework-conditional**($R^{\rm cyc}_{\rm formal}$・裁定 24;**本稿の主鎖の外**) |

$$G_{\mathbb Q}\ \xrightarrow[\textbf{(α) UNKNOWN}]{\ \text{(IH-S)}\ }\ \widehat{GT}\ \xrightarrow[\textbf{(β) UNKNOWN}]{\ \text{(U-10)}\ }\ \widehat{GT}_{\rm gen}\ \xrightarrow[\textbf{(γ) 有限問題族へ翻訳済}]{\ \mathcal{PR}^{\rm odd}\ }\ \mathrm{GT}^{\rm odd}_{\rm Dih}\ \xrightarrow[\textbf{(δ) PASS}]{\ \text{E1-3}\ }\ \textbf{odd Conj 5.1}$$

> **⚠ (β) の読み方**: 図の第 2 矢印は**包含であって全射性の主張ではない**。合成 $\mathcal{PR}^{\rm odd}\circ(\subseteq)\circ\mathrm{Ih}=\mathrm{Ih}^{\rm odd}$(補題 IH-FACT)は常に正しいが、**合成の全射性に必要なのは (γ) ではなく「(γ) の $\widehat{GT}$ への制限」= (PR-S$^{\rm odd}$)** である。(β) が等号(U-10)でなければ両者は一致しない。**この 1 点が本稿で最も落としやすい前件**(§3.3 系 FAKE-KILL′ の警告と同じ穴)。

**禁止(FAM-U-ASM §V.5.2 の規律を継承)**: **矢印を跨いだ主張をしない**。とくに (δ) の PASS を (α)(β)(γ) の証拠に使わない。**本稿が新しく置いたのは (γ) の翻訳(定理 ML-ODD)・(γ) が $\mathfrak F_0$ 方向で削られない条件(定理 SPLIT-NULL)・五本を一列に並べたときの型の管理(§3)だけ**である。

### 5.5 ★ 正典水準の罠(**前件を黙って落とさないための名指し**)

| # | 罠 | 正しい扱い |
|---|---|---|
| **T-1** | **完備化規約**: 「井原予想」の $\widehat{GT}$ は **pentagon つき($\widehat{B_4}$ 内)の Drinfeld $\widehat{GT}$**。本工房の主線 2401 が扱うのは **gentle 系 $\widehat{GT}_{\rm gen}$**(pentagon を $\hat f\in[\widehat F_2,\widehat F_2]^{\rm cl}$ に置換)。**両者の同定は U-10 = 未解決** | 二つを別記号で書き分ける(本稿は一貫してそうした)。**「$\widehat{GT}_{\rm gen}$ への全射」を「井原予想」と呼ばない**。地図 P6 行の「profinite 全体で $G_{\mathbb Q}\to GT$ が同型」は Drinfeld 側を指すと読む |
| **T-2** | **「fake」の二義**: 正典 Def 4.2 の fake $=$ **非 genuine**(A 型)。工房の地図 P1 行の「fake witness」$=$ **非算術**(A∪B) | 注意 FK-TYPE の二型表を使う。**P5 哨戒(細分での survive 判定)が測っているのは A 型**である(地図 §別線「K³/K⁵ 細分」の記述から) |
| **T-3** | **全射の水準**: odd Conj 5.1 は**全有限段**の全射、$\mathrm{Ih}^{\rm odd}$ 全射は**極限**への全射 | 橋は E1-3 で、その中で $\mathrm{pr}_n$ 全射(E1-3d ⟸ (THM44))とコンパクト性を使う。**遷移写像の全射性だけから極限の全射性は出ない**(便 75 F6.2(d) 原文) |
| **T-4** | **$m$ の水準**: $m\in\mathbb Z/N_{\rm ord}$ であって $\mathbb Z/n$ ではない(補題 L) | §6 の $\mathrm{GT}(K^{(9)})$ は $m\in\mathbb Z/18$、$\mathrm{PSL}(2,8)$ 窓は $m\in\mathbb Z/9$。**屋根での貼り合わせはこの水準差の上で行う**(§6.3) |
| **T-5** | **isolated と settled の別**: $\mathrm{GT}(N)=\mathrm{GTSh}(N,N)$ と書けるのは isolated のときだけ。壁窓の isolated 性は**全キャンペーンで未検証**(【SD-a】裁定 219) | §6 の $\mathrm{PSL}(2,8)$ 窓は **settled 54/54 の機械測定**であって定理ではない(`surj_s4_v2.md` §3.5;証明書は `"isolated":"UNKNOWN"`)。**前件表の (S4-ISO) 行に立てる** |

---

## 6. 実測 1 対の設計 — **$\mathrm{PSL}(2,8)$ 窓 $\times$ $K^{(9)}$**

### 6.1 何を測るのか(ML-ODD (ii) の**最初の 1 点**)

系 ML-C により、E1-GAP-4 の内容は**すべて非 dihedral 細分**に載っている。裁定 226 の交差の観察
$$\lvert\mathrm{GTSh}(\mathrm{S4}=\mathrm{PSL}(2,8))\rvert=54=\mathrm{IdGroup}\ [54,6]=\mathrm{Hol}(\mathbb Z/9)=\mathrm{Aff}(\mathbb Z/9),\qquad \lvert\mathrm{GT}(K^{(9)})\rvert=108=2\cdot9\cdot\varphi(9)$$
は、**中間峰の $K^{(9)}$ と壁の $\mathrm{PSL}(2,8)$ 窓が同じ $\mathrm{Hol}(\mathbb Z/9)$ を出す**ことを言っている。本節はこの一致を出発点に、**ML-ODD (ii) の finite instance を 1 点だけ実測する設計**を書く。

**窓データ**(既存・再測定しない):
- $N_{\rm S4}$: `provenance/LEDGER.md` L642 の証明書。$\lvert B_3/N_{\rm S4}\rvert=3024=6\cdot504$、$PB_3/N_{\rm S4}\cong P:=\mathrm{PSL}(2,8)$($\lvert P\rvert=504$)、$c\in N_{\rm S4}$、$(N_{\rm S4})_{\rm ord}=9$、charming set $=\{0,2,3,5,6,8\}\subset\mathbb Z/9$、$\lvert\mathrm{GT}(N_{\rm S4})\rvert=54$、$\mathfrak F_0\cong C_9$、settled 54/54。
- $K^{(9)}$: 正典。$K^{(9)}_{\rm ord}=18$、$PB_3/K^{(9)}\cong G_9=A\rtimes Q$、$A\cong(\mathbb Z/9)^3=[G_9,G_9]$、$Q\cong C_2^2$、$\lvert G_9\rvert=4\cdot9^3=2916$(ODD-H 補題 A)。$\lvert\mathrm{GT}(K^{(9)})\rvert=108$。

### 6.2 まず**比較可能性**を確定する(P6-3 第 6 項の「確認方法」)

> ### 方法 CMP(isolated poset 内での比較可能性の確認手順)
> $N,H\in\mathrm{NFI}_{PB_3}(B_3)$ に対し $N\subseteq H$ を判定する。
> 1. **数値篩(必要条件・紙)**: 補題 ML-2 より $N\subseteq H\Rightarrow H_{\rm ord}\mid N_{\rm ord}$。割れなければ即座に**否定**。
> 2. **構造篩(必要条件・紙)**: $N\subseteq H\Rightarrow PB_3/N\twoheadrightarrow PB_3/H$。ゆえに $PB_3/H$ の合成因子は $PB_3/N$ の合成因子の部分多重集合。とくに $PB_3/N$ 可解 $\Rightarrow$ $PB_3/H$ 可解。
> 3. **決定的判定(機械)**: $F_2/N_{F_2}\to F_2/H_{F_2}$、$x\mapsto x$、$y\mapsto y$ が well-defined か。GAP なら `GroupHomomorphismByImages(QN,QH,[xN,yN],[xH,yH])` が `fail` を返すか否か($\mathtt{fail}\iff N\not\subseteq H$)。$c$ の扱いは両窓とも $c\in N$ を確認してから($LEDGER L642 の `c_in_N=true`)。
> 4. **比較不能なら屋根を取る**: $M:=N\cap H=\ker\bigl(F_2\to(F_2/N_{F_2})\times(F_2/H_{F_2})\bigr)$。**(DIR)(Prop 3.15)より両方 isolated なら $M$ も isolated**、$M$ は両方への reduction をもつ。
> 5. **屋根の商の同定**: $PB_3/M\hookrightarrow(PB_3/N)\times(PB_3/H)$ は subdirect。**Goursat** より $PB_3/M$ が全直積 $\iff$ $PB_3/N$ と $PB_3/H$ に共通の非自明商が無い。

> ### 命題 CMP-S4($N_{\rm S4}$ と $K^{(9)}$ は**比較不能**)
> $$N_{\rm S4}\not\subseteq K^{(9)}\quad\text{かつ}\quad K^{(9)}\not\subseteq N_{\rm S4}.$$

**証明.** 前者: 手順 1。$K^{(9)}_{\rm ord}=18\nmid9=(N_{\rm S4})_{\rm ord}$。
後者: 手順 2。$K^{(9)}\subseteq N_{\rm S4}$ なら $G_9=PB_3/K^{(9)}\twoheadrightarrow PB_3/N_{\rm S4}=\mathrm{PSL}(2,8)$。$G_9=A\rtimes Q$ は可解(ODD-H 補題 A)、可解群の商は可解、$\mathrm{PSL}(2,8)$ は非可換単純ゆえ非可解。矛盾。∎

> **⟹ $\mathrm{Dih}^{\rm odd}$ は $I$ の中で共終でない**ことの**具体的な証人**が得られた(E1-GAP-4 が「自動では出ない」と述べた理由の実体)。$\mathrm{PSL}(2,8)$ 窓はどの $K^{(n)}$($n$ 奇)も細分しない。

### 6.3 屋根 $M:=K^{(9)}\cap N_{\rm S4}$ の構造(**紙で先に決める**)

> ### 命題 ROOF(**分裂屋根**)
> $M:=K^{(9)}\cap N_{\rm S4}$ と置く。このとき
> 1. $PB_3/M\ \cong\ G_9\times\mathrm{PSL}(2,8)$($\lvert\ \rvert=2916\cdot504=1{,}469{,}664$)、$F_2/M_{F_2}\cong PB_3/M$($c\in M$ より)。
> 2. $M_{\rm ord}=18$。
> 3. $(N_{\rm S4}$ が isolated なら$)$ $M$ は isolated であり、$R_{M,K^{(9)}}$・$R_{M,N_{\rm S4}}$ はともに群準同型。
> 4. $[m,f]$($m\in\mathbb Z/18$、$f=(f_9,f_P)\in F_2/M_{F_2}$)が $\mathrm{GT}(M)$ に属する $\iff$ $[m\bmod18,f_9]\in\mathrm{GT}(K^{(9)})$ かつ $[m\bmod9,f_P]\in\mathrm{GT}(N_{\rm S4})$。すなわち
> $$\mathrm{GT}(M)\ \cong\ \mathrm{GT}(K^{(9)})\ \times_{(\mathbb Z/18)^\times}\ \mathrm{GT}(N_{\rm S4})$$
> (貼り合わせは $\widetilde\chi:[m,f]\mapsto2m+1$ の共通水準 $(\mathbb Z/18)^\times$ 上)。

**証明.**
(1) $PB_3/M\hookrightarrow G_9\times P$ は subdirect(両射影が全射)。$G_9$ 可解・$P$ 非可換単純ゆえ、$P$ の商は $1$ と $P$ のみで $P$ は非可解、したがって $G_9$ と $P$ の共通商は $1$。Goursat より $PB_3/M=G_9\times P$。$c\in K^{(9)}$($\psi_9(c)=(1,1,1)$)かつ $c\in N_{\rm S4}$(証明書)より $c\in M$、$PB_3=F_2\times\langle c\rangle$ から $F_2/M_{F_2}\cong PB_3/M$。
(2) (1) より $\mathrm{ord}(xM)=\mathrm{lcm}(\mathrm{ord}_{G_9}(X),\mathrm{ord}_P(X_P))=\mathrm{lcm}(18,9)=18$(ODD-H 補題 A(3) で $\mathrm{ord}(X)=2n=18$、証明書で $\mathrm{ord}_P=9$)。$y$ も同様、$\mathrm{ord}(cM)=1$。(3.1) より $M_{\rm ord}=18$。
(3) (DIR)(Prop 3.15)+(HOM)(Remark 3.16)。
(4) $B_3/M\hookrightarrow B_3/K^{(9)}\times B_3/N_{\rm S4}$(核が $M$)ゆえ、$B_3/M$ での等式は**両成分での等式と同値**。hexagon (3.3)(3.4) と charming の第二条件はこれで分解する($[A\times B,A\times B]=[A,A]\times[B,B]$)。charming の第一条件は水準 $M_{\rm ord}=\mathrm{lcm}(18,9)=18$ で $\gcd(2m+1,18)=1$、これは二成分の条件 $\gcd(2m+1,K^{(9)}_{\rm ord})=\gcd(2m+1,18)=1$ と $\gcd(2m+1,(N_{\rm S4})_{\rm ord})=\gcd(2m+1,9)=1$ の連言と同値($\mathrm{lcm}$ ゆえ)。
残るのは **$T_{m,f}:B_3\to B_3/M$ の全射性**。像は $B_3/M$ の subdirect 部分群で、両成分では(各因子が GT-shadow なので)全射。Goursat により像は共通商 $E$ 上の fiber 積であり、$B_3/M$ 自身は $S_3=B_3/PB_3$ 上の fiber 積。$E_0:=\ker(E\to S_3)$ は $PB_3/K^{(9)}=G_9$ の商かつ $PB_3/N_{\rm S4}=P$ の商であるから、(1) の議論より $E_0=1$、すなわち $E=S_3$ で像は $B_3/M$ 全体。∎

### 6.4 分裂屋根は fake を検出しない(**負の定理・設計の教訓**)

> ### 定理 SPLIT-NULL
> $n$ 奇 $\ge3$、$N'\in I$、$M:=K^{(n)}\cap N'$ とし、**$G_n=PB_3/K^{(n)}$ と $PB_3/N'$ に共通の非自明商が無い**(⟹ $PB_3/M\cong G_n\times PB_3/N'$)と仮定する。$\mathfrak m(N')\subseteq\mathbb Z/N'_{\rm ord}$ を $\mathrm{GT}(N')$ の $m$-像とすると
> $$\mathrm{Im}\,R_{M,K^{(n)}}=\bigl\{[m,f]\in\mathrm{GT}(K^{(n)})\ \big|\ \exists\,\tilde m\in\mathbb Z/M_{\rm ord}:\ \tilde m\equiv m\ (\mathrm{mod}\ 2n),\ \tilde m\bmod N'_{\rm ord}\in\mathfrak m(N')\bigr\}.$$
> とくに $\mathrm{Im}\,R_{M,K^{(n)}}$ は **$\widetilde\chi$-fiber($=$ $m$-fiber・補題 L)の合併**であり、
> $$\boxed{\ \textbf{分裂屋根は }\mathfrak F_0\ \textbf{方向を一切削らない — 像の減少は }\chi\ \textbf{水準にしか起こらない。}\ }$$

**証明.** 命題 ROOF(4) と同じ分解が一般の分裂屋根で成り立つ(証明は逐語同一;$P$ 単純性は使わず「共通商 $=1$」だけを使った)。$[m,f_n]$ が像に入る $\iff$ ある $\tilde m$ と**ある** $f_{B}$ で $(\tilde m,(f_n,f_B))\in\mathrm{GT}(M)$ $\iff$ $\tilde m$ が上の条件を満たす($f_n$ 側は $m$ にしか依存しない条件で既に満たされている)。$f_n$ が自由なので像は $m$-fiber の合併。∎

> ### 系 SPLIT-NULL′(**強形** — 分裂屋根の reduction は全射)
> 上の設定でさらに **$\widetilde\chi\bigl(\mathrm{GT}_{\rm arith}(K^{(n)})\bigr)=(\mathbb Z/4n)^\times$**((S2) $=$ W2-arith・裁定 122・**framework-conditional**)を仮定すれば、$R_{M,K^{(n)}}$ は**全射**。
> **証明.** $\mathrm{GT}_{\rm arith}(K^{(n)})\subseteq\mathrm{GT}_{\rm gen}(K^{(n)})\subseteq\mathrm{Im}\,R_{M,K^{(n)}}$(系 ML-A)。仮定より像の $\widetilde\chi$-像は全体 $(\mathbb Z/4n)^\times$、補題 L で $m$-水準と同一視すると全 $m\in\mathcal X_n$ が像に現れる。定理 SPLIT-NULL より像は $m$-fiber の合併ゆえ全体。∎
>
> **代替経路($n=9$ の実測ではこちらを使う・framework-free)**: $\mathfrak m(N_{\rm S4})$ を証明書から直接読む($\lvert\mathrm{GT}(N_{\rm S4})\rvert=54$、$\mathfrak F_0\cong C_9$ ⟹ $m$-像はちょうど 6 元 $=$ charming set 全体)。§6.5 の検算 3 行目がこれを確認する。

> ### ★ 系 SPLIT-NULL″(**哨戒設計への含意**)
> **fake(A 型)を検出しうる細分は、$K^{(n)}$ 側の商 $G_n$ と非自明な共通商をもつ「entangled 屋根」に限る。** 分裂屋根をいくら積んでも $\mathrm{GT}_{\rm gen}(K^{(n)})$ は縮まない。
> ⟹ **ML-ODD (ii) の量化を実効的に走らせる設計は、「$G_n$ と共通商をもつ非 dihedral isolated 窓」を作るところから始めるべき**である。$\mathrm{PSL}(2,8)$ 窓はこの意味で**最も検出力の低い型**(共通商が完全に自明)であり、本実測は**較正点**として位置づける(下記 §6.6)。

### 6.5 事前登録予言(**prediction-first**・実測前に凍結)

宇宙の事前登録: **対象は $(N_{\rm S4},K^{(9)})$ の 1 対のみ**。$n=5$ 非接触。以下 7 本は §6.3 の紙から導かれる予言であり、**実測はこれの独立確認**である。

| # | 予言 | 根拠 |
|---|---|---|
| **P-IHN-1** | $N_{\rm S4}$ と $K^{(9)}$ は poset で**比較不能**(両向きとも `fail`) | 命題 CMP-S4 |
| **P-IHN-2** | $\lvert PB_3/M\rvert=1{,}469{,}664=2916\cdot504$、かつ $PB_3/M\cong G_9\times\mathrm{PSL}(2,8)$(直積・非 subdirect 真部分群) | 命題 ROOF(1) |
| **P-IHN-3** | $M_{\rm ord}=18$ | 命題 ROOF(2) |
| **P-IHN-4** | $\lvert\mathrm{GT}(M)\rvert=\mathbf{972}$。$\mathfrak F_0(M)\cong C_9\times C_9$(位数 81)、$\widetilde\chi$ 像 $=(\mathbb Z/36)^\times$(位数 12)、$81\cdot12=972$ | 命題 ROOF(4) |
| **P-IHN-5** | $\mathrm{Im}\,R_{M,K^{(9)}}=\mathrm{GT}(K^{(9)})$(**108/108・全射**)⟹ **この細分は fake を検出しない** | 定理 SPLIT-NULL + $\mathfrak m(N_{\rm S4})=$ charming set 全体 |
| **P-IHN-6** | $\mathrm{Im}\,R_{M,N_{\rm S4}}=\mathrm{GT}(N_{\rm S4})$(**54/54・全射**) | 同上(対称) |
| **P-IHN-7** | **副産物・U-11 の閉鎖**: $\mathrm{IdGroup}\bigl(\mathrm{GT}(K^{(9)})\bigr)=[108,26]$($=C_2\times\mathrm{Hol}(\mathbb Z/9)$)。さらに $\mathrm{GT}(M)\cong\bigl((C_9\times C_9)\rtimes C_6\bigr)\times C_2$($C_6=(\mathbb Z/9)^\times$ が対角に乗法作用) | 定理 E1-2(有限段 $\cong\mathrm{Aff}(\mathbb Z/9)\times C_2$)+ 裁定 226 の交差表 |

> **⚠ P-IHN-7 の後半($\mathrm{GT}(M)$ の抽象型)は $N_{\rm S4}$ 側の $(\mathbb Z/9)^\times$ 作用が「$u$ 倍」であることに依存する。これは $\mathrm{GTSh}=\mathrm{Hol}(\mathbb Z/9)$ の実測から自然だが工房に証明が無い ⟹ 予言であって主張ではない。**

**検算(証明とは独立・整数演算のみ・単系統)**: `scratchpad/ihnec_check.py`(SHA-256 `edf618137697377f2eba5f4d59be53bd07ac5a598ee2246f70eedf372ad49309`)で ①$\lvert\mathcal X_9\rvert=12$・$\lvert\mathcal X_{\rm S4}\rvert=6$・S4 charming set $=\{0,2,3,5,6,8\}$(`surj_s4_v2.md` §1 と一致)②$\mathcal X_9\bmod9$ の像 $=$ S4 charming set(各 2 回)③$\lvert\mathrm{GT}(M)\rvert=972$ が 3 通りの数え方で一致 ④$\lvert G_9\rvert\cdot504=1469664$ ⑤数値篩 $18\nmid9$ ⑥像が全 $m$-fiber を含む、を確認。**failures 0 / ALL PASS**。**これは cross-check であって証明ではない。**

### 6.6 実測の工程(**設計のみ** — 実装は implementer へ)

> **前件の明示**: **(S4-ISO)** $N_{\rm S4}$ が isolated であること。**状態: 機械測定(settled 54/54)のみ・証明書は `"isolated":"UNKNOWN"`**(`surj_s4_v2.md` §3.5・【SD-a】裁定 219)。**これが落ちると命題 ROOF(3) が消え、$\mathrm{GT}(M)$ が群である保証も、$R$ が準同型である保証も消える**(集合としての像の測定は残る)。⟹ **報告は「(S4-ISO) 条件つき」と明記すること。**

| 段 | 内容 | 出力 | コスト見積 |
|---|---|---|---|
| **R0** | 既存証明書から $N_{\rm S4}$ の生成データ($X_P,Y_P\in\mathrm{PSL}(2,8)$)と $G_9$ の生成データ($X,Y$;ODD-H 補題 A(3) の明示形)を再構成 | 2 組の生成対 | 分 |
| **R1** | **方法 CMP 手順 3** を両向きに実行 ⟹ **P-IHN-1** | `fail`/`fail` | 秒 |
| **R2** | $\langle(X,X_P),(Y,Y_P)\rangle\le G_9\times P$ の位数を測る ⟹ **P-IHN-2**(直積になっていることの直接確認 = Goursat 論法の機械照合) | 位数 1,469,664 | 秒〜分 |
| **R3** | $\mathrm{ord}$ of $(X,X_P)$, $(Y,Y_P)$ ⟹ **P-IHN-3** | $M_{\rm ord}=18$ | 秒 |
| **R4a**(**主・安価**) | **因子ごとの悉皆走査**: $m\in\mathcal X_9$(12 個)$\times$ $f_9\in[G_9,G_9]=A$(729 個)で $\mathrm{GT}(K^{(9)})$ を再現(108 期待)/ $m\in\mathcal X_{\rm S4}$(6 個)$\times$ $f_P\in[P,P]=P$(504 個)で $\mathrm{GT}(N_{\rm S4})$ を再現(54 期待)。**計 $12\cdot729+6\cdot504=11{,}772$ 判定** | 108・54・IdGroup ⟹ **P-IHN-7 前半 = U-11 閉鎖** | 分 |
| **R4b**(**確認・高価・シャード必須**) | **屋根での悉皆走査**: $m\in\mathcal X_{M}$(12)$\times$ $f\in[F_2/M_{F_2},\cdot]=A\times P$(367,416)= **4,408,992 判定**。命題 ROOF(4) の**独立確認**(R4a の結果を使わずに $\lvert\mathrm{GT}(M)\rvert$ を出す) | 972 ⟹ **P-IHN-4** | **600 秒 cap 超過が確実 ⟹ $m$ で 12 シャードに分割**(工房の shard 規律) |
| **R5** | $R_{M,K^{(9)}}$・$R_{M,N_{\rm S4}}$ の像を数える ⟹ **P-IHN-5 / P-IHN-6** | 108/108・54/54 | 秒(R4 の出力から) |
| **R6** | $\mathrm{GT}(M)$ の `IdGroup`(位数 972)⟹ **P-IHN-7 後半** | IdGroup | 秒 |

> **設計上の注意 3 点**
> 1. **R4a と R4b は独立でなければならない**。R4b が R4a の出力(命題 ROOF(4) の分解)を前提にすると、確認が循環する。R4b は $B_3/M$ の中で hexagon を直接検査すること。
> 2. **`settled` の意味論**: `surj_s4_v2.md` §3.5 の指摘どおり、「$T_{m,f}$ を実現する $h\in\mathrm{Aut}$ の witness 探索」と「壁 judge の `settled_fail_count`(well-definedness)」は別物。**屋根 $M$ での settled 判定は前者(真の settled)を使うこと**。
> 3. **RAM 8GB 制約**: $\lvert G_9\times P\rvert\approx1.47\times10^6$ の要素を明示的に持たない。置換表現($G_9$ は $27+\cdots$ 次、$P$ は 9 点)の直積で持ち、$[G_9,G_9]=A\cong(\mathbb Z/9)^3$ は座標で持つ。

### 6.7 この実測が**何を与え・何を与えないか**

| 得られるもの | 得られないもの |
|---|---|
| **ML-ODD (ii) の finite instance の第 1 点**(工房で初めて「非 dihedral 細分での $R$ の像」を測る) | **E1-GAP-4 の解決**(量化は無限・【IHNEC-GAP-1】) |
| **U-11 の閉鎖**($\mathrm{GT}(K^{(9)})$ の IdGroup;裁定 226 が「GAP 1 発」と記帳した宿題) | fake の存在・非存在に関する情報(**P-IHN-5 は設計上あらかじめ全射と分かっている** — 定理 SPLIT-NULL) |
| **方法 CMP の較正**(比較可能性判定の手順が実際に動くことの確認) | $\mathrm{PSL}(2,8)$ 窓の isolated 性(**(S4-ISO) は依然機械測定のみ**) |
| **定理 SPLIT-NULL の機械照合**(紙の分解が実物で成り立つこと) | 中間峰の登頂に関する一切 |

> **正直な評価**: 本実測は **negative result を予言して確認する較正**である。研究上の値打ちは「$\mathrm{PSL}(2,8)$ 窓では何も出ない」ことを**実測前に紙で決めた**点と、**次に何を作るべきか(entangled 屋根)を系 SPLIT-NULL″ が名指しする**点にある。**これを「fake が無い証拠」と読んではならない**(工房の掟 2)。

---

## 7. 格付け表

**語彙**: 正典の定理 / 紙上相互監査 PASS / paper-proof candidate / framework-conditional / candidate / UNKNOWN。**「verified」は Lean に予約 — 本表では一度も使わない。**

| # | statement | 状態 | 出所 |
|---|---|---|---|
| **IH-0** | $\mathcal{PR}^{\rm odd}$ well-defined・連続準同型 | **paper-proof candidate**(初等段;E1-3b と同型の論法) | 本稿 §2 |
| **IH-FACT** | $\mathrm{Ih}^{\rm odd}=\mathcal{PR}^{\rm odd}\vert_{\widehat{GT}}\circ\mathrm{Ih}$ | **paper-proof candidate**(定義の展開のみ) | 本稿 §2 |
| **IH-NEC** | (IH-S)$\wedge$(PR-S$^{\rm odd}$) ⟹ odd Conj 5.1 | **paper-proof candidate**(論理は自明・**値打ちは前件表 §5 にある**) | 本稿 §3.2 |
| **FAKE-KILL** | **(U-10)$\wedge$B 型証人 1 個(任意の窓)⟹ $\neg$(IH-S)**;対偶 = (IH-S)$\wedge$(U-10) ⟹ 全窓で arith $=$ gen | **paper-proof candidate**(集合水準の一行) | 本稿 §3.3 |
| **FAKE-KILL′** | (PR-S$^{\rm odd}_{\rm gen}$)$\wedge$(U-10)$\wedge$奇窓の非算術 shadow 1 個 ⟹ $\neg$(IH-S) | **paper-proof candidate** | 本稿 §3.3 |
| **FK-TYPE** | 証人の A 型 / B 型の分離と各々が殺すもの | **paper-proof candidate**(**用語の食い違いの是正を含む**) | 本稿 §3.3 |
| **ML-1** | $K^{(a)}\cap K^{(b)}=K^{(\mathrm{lcm})}$・$D(N)$ の閉性 | **paper-proof candidate** | 本稿 §4.2 |
| **ML-2** | $N\subseteq H\Rightarrow H_{\rm ord}\mid N_{\rm ord}$ | **paper-proof candidate**(初等) | 本稿 §4.2 |
| **ML-ODD** | (i)$\iff$(ii)$\iff$(iii) | ★ **paper-proof candidate**(**本稿の主定理**・Sol 監査未) | 本稿 §4.3 |
| **ML-A/B/C** | 三層・odd Conj 5.1 ⟹ (i)・$\mathrm{Dih}^{\rm odd}$ 内部は恒真 | **paper-proof candidate** | 本稿 §4.4 |
| **CMP-S4** | $N_{\rm S4}$ と $K^{(9)}$ は比較不能 | **paper-proof candidate**(可解性 + $N_{\rm ord}$。$\lvert G_9\rvert$ は ODD-H 補題 A) | 本稿 §6.2 |
| **ROOF** | $PB_3/M\cong G_9\times\mathrm{PSL}(2,8)$・$M_{\rm ord}=18$・$\mathrm{GT}(M)$ の fiber 積 | **paper-proof candidate / (S4-ISO) 条件つき** | 本稿 §6.3 |
| **SPLIT-NULL** | 分裂屋根の像は $m$-fiber の合併 | ★ **paper-proof candidate**(**本稿の第 2 の実質**) | 本稿 §6.4 |
| **SPLIT-NULL′** | 分裂屋根の $R$ は全射 | **paper-proof candidate / framework-conditional**((S2) 経路)または **実測依存**($n=9$ の代替経路) | 本稿 §6.4 |
| **P-IHN-1〜7** | 実測予言 7 本 | **prediction(未測定)** | 本稿 §6.5;検算 ALL PASS(単系統) |
| **(IH-S)/(PR-S$^{\rm odd}$)/(U-10)** | — | **UNKNOWN** | §5.2 |

> **⚠ 全表にかかる注意**: 本稿は **Sol 未監査**。§4 の主定理 ML-ODD は正典 4 本(Thm 5.2・Cor 5.4・Prop 3.14/3.15)に全面的に依存しており、**それらの引用が正しいこと自体が監査対象**である。とくに **(DIR)(Prop 3.15: isolated $\cap$ isolated $=$ isolated)は原文画像で確認していない**(抽出ノート `2401.06870-抽出ノート_v1.md` L94 の記述に依拠)。⟹ **§8 の申し送り 1 を参照。**

---

## 8. 【IHNEC-GAP】一覧・申し送り

| # | ギャップ | 状態 |
|---|---|---|
| **IHNEC-GAP-1** | ML-ODD (ii) の $N$ の量化は無限。停留は保証されるが**停留深さの上界を与える装置が無い** ⟹ 決定手続きではない | **UNKNOWN**(§4.4・文献要請 IHNEC-L1) |
| **IHNEC-GAP-2** | **entangled 屋根の構成法が無い**。系 SPLIT-NULL″ は「$G_n$ と共通商をもつ非 dihedral isolated 窓」を要求するが、そのような窓の**構成レシピ**(2401 Prop 5.1 の $(5.4)$ から作れるか)は未検討 | **未着手**(§6.4) |
| **IHNEC-GAP-3** | (PR-S$^{\rm odd}$) の $\widehat{GT}$ 版と $\widehat{GT}_{\rm gen}$ 版の差 $=$ U-10。**U-10 を迂回して $\widehat{GT}$ 版だけを直接攻める経路**があるか(pentagon 情報を有限段で使う = P6 の $K_\pi$ 線との接続) | **未検討**(定理 GTPI・裁定 359 の線と接続しうる) |

### 申し送り(司令塔へ)

1. **(DIR) の原文照合を要請する** — 本稿の主定理は 2401 **Prop 3.15**(isolated $\cap$ isolated $=$ isolated)に本質的に依存する(有向性が無いと補題 ML-3 が使えない)。工房内では抽出ノートの 1 行にしか記録が無い。**pdftocairo でのページ画像照合を 1 回**お願いしたい(Prop 3.14/3.15・Cor 5.4 の 3 点)。
2. **用語の裁定を求める(注意 FK-TYPE)** — 正典 Def 4.2 の **fake $=$ 非 genuine** と、地図 P1 行の **fake witness $=$ 非算術**が食い違っている。P5 哨戒が測っているのは前者(A 型)であり、**A 型の witness は P6 を殺さない**。地図 P5 行に「A 型 / B 型」の別を書くか否かは司令塔の裁定事項。**同じ札で違う峰を狙っている状態は危険**と判断して名指しした。
3. **P-IHN-7 前半は U-11(裁定 226 の待ち行列)そのもの** — R4a を回せば「GAP 1 発」の宿題が予言つきで閉じる。**U-11 を単独で起票するより本設計に同梱するほうが安い**(同じ走査で 108 と 54 の両方が出る)。
4. **系 SPLIT-NULL″ を P5 哨戒の設計原則として採るか** — 「分裂屋根では fake は原理的に出ない」は、これまでの哨戒(バッテリー 7 窓など)がどの型だったかを**遡って点検する**根拠になりうる。**遡及点検を起票するかは司令塔判断。**
5. **Sol 監査の優先順位案**: ① ML-ODD の (iii)$\Rightarrow$(i)(補題 ML-3 の適用と $Y_N=R^{-1}(y_{n(N)})$ への還元)② 命題 ROOF(4) の全射性の段(Goursat の $E_0=1$)③ 注意 FK-TYPE の型分離 ④ 前件表 §5.2 の「落とすと壊れるもの」欄。
6. **実装は R4a まで(安価)を先行させ、R4b(シャード)は R4a の結果を見てから**を推奨。R4b は独立確認のためのものであり、R4a が予言と外れた場合は設計自体を見直す。

---

## 9. 出所・新規性の申告

### 9.1 出所

| 節 | 主たる出所 |
|---|---|
| §1 | `docs/notes/E1_gt_odd_dih_canonical_v1.md` §1(記法)/ `docs/week1-定義ノート.md` §2–§3 / `docs/notes/2401.06870-抽出ノート_v1.md` §9–§10 |
| §2 | 正典 (1.11)(3.60)・2401 §4 / E1 ノート補題 E1-3a/3b |
| §3 | E1 ノート定理 E1-3(裁定 266)/ 正典 Def 4.2 / `docs/地図.md` P1・P5・P6 行 / `docs/notes/i17_check_v1.md` §4(q=7 二枝) |
| §4 | **2401 Thm 5.2・Cor 5.4・Prop 3.14・Prop 3.15**(抽出ノート §9–§10)/ 2405 Thm 4.4 / E1 ノート補題 E1-D2・E1-3d |
| §5 | `docs/notes/fam_u_assembly_v1.md` §V.2/§V.3/§V.5(**様式の借用**)/ 定義ノート §2(U-10・gentle の意味) |
| §6 | **裁定 226**(交差の観察・[54,6])/ `provenance/LEDGER.md` L642(S4 証明書)/ `docs/notes/surj_s4_v2.md` §1・§3.5 / `docs/notes/oddH_full_proof_v1.md` §2 補題 A / `docs/notes/e1_canonical_v1.md` §4 窓族統一表 |

### 9.2 新規性の申告(grep 済)

**grep 語**: `PR^odd`・`\mathcal{PR}^{\rm odd}`・`IH-NEC`・`FAKE-KILL`・`ML-ODD`・`SPLIT-NULL`・`Mittag-Leffler`・`安定像`・`Goursat`・`比較不能`・`屋根`・`E1-GAP-4`・`U-11`・`Cor 5.4`・`共終`。

- **既出**: E1-GAP-4 の言明そのもの(E1 ノート §8)/ arithmetical $\Rightarrow$ genuine $\Rightarrow$ charming(定義ノート §3)/ Cor 5.4 の「fake は有限証明書・genuine は無限深度」(定義ノート §3・抽出ノート §9)/ 「Dih 内部だけでは fake は見つからない」(抽出ノート §9)/ 裁定 226 の [54,6] 交差 / U-11 / Goursat の使用(E1 ノート §5.6・`n12_goursat_v1.md`)。
- **本稿で新しいもの**: ① **定理 ML-ODD**(E1-GAP-4 $\iff$ 有限問題族。工房内 grep で `Mittag-Leffler`・`安定像`・`stable image` は**ヒット 0**)② **定理 SPLIT-NULL** と系 SPLIT-NULL″(分裂屋根は fake を検出しない — 哨戒設計の負の定理。grep ヒット 0)③ **注意 FK-TYPE**(正典 fake と工房 fake witness の二義の分離・各々が殺す峰の表。**二義の指摘自体が repo に無い** — grep 済)④ **命題 CMP-S4**($\mathrm{Dih}^{\rm odd}$ が共終でないことの具体的証人)と**方法 CMP**(比較可能性の 5 手順)⑤ **命題 ROOF**($PB_3/M\cong G_9\times\mathrm{PSL}(2,8)$・$\mathrm{GT}(M)$ の fiber 積表示)⑥ 前件表 §5.2 の「落とすと壊れるもの」欄と §5.5 の罠表 ⑦ 実測予言 7 本。
- **IH-FACT / IH-NEC / FAKE-KILL は論理的に自明な合成**であり、**定理としての新規性は主張しない**。値打ちは前件表(§5)と型分離(FK-TYPE)にある。
- **「初」という語は使わない**(工房外の文献での既知性は未調査 — ML-ODD の型の主張は pro-有限群論の標準的な安定像議論であり、一般論としては既知である可能性が高い。**本設定への翻訳が本稿の寄与**)。

---

# 追補 A(**裁定 374 = P6-3 検収**・2026-08-01)

**位置づけ**: 司令塔の裁定 2 件を反映する差し替え節。**v1 本文(§0–§9)は改変していない** — 置換関係を各節の見出しに明記する(`fam_u_assembly_v1.md` の CV-10 erratum 方式に倣う)。起草: 数学者(Opus 5)。

## A.1 用語の一本化(裁定 374 ①)— **§3.3 冒頭・§5.5 T-2 を置換**

正式用語を **3 語**に確定する。$N$ は任意の窓、三層は (1.A)。

| 正式用語 | 定義 | v1 本文での旧称 |
|---|---|---|
| **fake** | $g\in\mathrm{GT}(N)\setminus\mathrm{GT}_{\rm gen}(N)$(**非 genuine**・正典 Def 4.2 準拠) | 「A 型」「正典の fake」 |
| **非算術証人** | $g\in\mathrm{GT}_{\rm gen}(N)\setminus\mathrm{GT}_{\rm arith}(N)$(**genuine だが非算術**) | 「B 型証人」 |
| **非算術 shadow** | $g\in\mathrm{GT}(N)\setminus\mathrm{GT}_{\rm arith}(N)$ $=$ **fake $\sqcup$ 非算術証人**(排他和) | 「非算術 shadow」(同じ) |

> ### ⚠ 予約語の規約(**この一行を落とすと裁定 374 の意図が壊れる**)
> **fake も非算術である**($\mathrm{GT}_{\rm arith}\subseteq\mathrm{GT}_{\rm gen}$ より)。それでも **「非算術証人」という語は genuine かつ非算術の元にのみ予約する**。fake を「非算術証人」と呼んではならないし、非算術証人を「fake」と呼んでもならない。両者を一括で指すときは **「非算術 shadow」**を使う。

> ### 札名についての注意(**混同の残り火**)
> **系の名前「FAKE-KILL」は P6-3 札から引き継いだ歴史的名称**であり、その証人は **fake ではなく非算術証人**である。台帳・地図に登録された札名はそのまま使うが、**言明を読むときは必ず §A.2 の差し替え本文を見ること**。

> ### 本文で**訂正不要**な箇所(**過剰訂正の防止** — grep 済で列挙)
> v1 本文の次の「fake」は**すべて正典 Def 4.2 の意味**で使われており、裁定 374 の下で**そのまま正しい**: §0 の ⑤、§1 表の (COR54) 行、§4.4 系 ML-C、**§6.4 の節題・定理 SPLIT-NULL・系 SPLIT-NULL″**、§6.5 P-IHN-5、§6.7 の 2 箇所、§9.2。⟹ **SPLIT-NULL 系の言明は無改訂**(「分裂屋根は fake を検出しない」は正典語で正しい)。

## A.2 系 FAKE-KILL / FAKE-KILL′ の差し替え本文(**§3.3 の 2 つの枠を置換**)

> ### 系 FAKE-KILL(点ごとの最小形・**裁定 374 用語**)
> **(U-10)** の下で、**任意の**窓 $N\in\mathrm{NFI}_{PB_3}(B_3)$(dihedral でなくてよい・isolated でなくてよい)に **非算術証人**
> $$g\in\mathrm{GT}_{\rm gen}(N)\setminus\mathrm{GT}_{\rm arith}(N)$$
> が 1 つでも存在すれば、**(IH-S)** は偽 — すなわち**井原予想の全射部が偽**。
> **証明**は v1 §3.3 のまま(集合水準の一行)。
> **対偶**: **(IH-S) $\wedge$ (U-10) $\Longrightarrow$ 全窓 $N$ で $\mathrm{GT}_{\rm arith}(N)=\mathrm{GT}_{\rm gen}(N)$**、すなわち **非算術証人は 1 つも存在しない**。

> ### 系 FAKE-KILL′(窓の言葉で使う形・**裁定 374 用語**)
> $$(\text{PR-S}^{\rm odd}_{\rm gen})\ \wedge\ (\text{U-10})\ \wedge\ \bigl[\text{ある奇窓 }K^{(n)}\text{ に非算術 shadow が 1 つ}\bigr]\ \Longrightarrow\ \neg(\text{IH-S}).$$
> **理由**: (PR-S$^{\rm odd}_{\rm gen}$)(= 定理 ML-ODD (iii) = 全奇窓の全 shadow が genuine)は **奇窓の fake を排除する**。ゆえに前件の非算術 shadow は**必ず非算術証人**であり、系 FAKE-KILL が発火する。
> **弱形で足りる**: 必要なのは**その窓 $K^{(n)}$ 1 つでの genuine 性**(系 ML-D)であって全奇 $n$ ではない。
> **(U-10) を落とすと**井原予想($\widehat{GT}$ 版)には届かない(罠 T-1)。

## A.3 注意 FK-TYPE の差し替え表(**§3.3 の二型表を置換**)

**非算術 shadow は fake か非算術証人のいずれか一方**(排他的)。それぞれが殺すもの:

| 証人 | 定義 | 単独で殺すもの(追加前件なし) | 追加前件つきで殺すもの |
|---|---|---|---|
| **fake**(正典 Def 4.2) | $\mathrm{GT}(K^{(n)})\setminus\mathrm{GT}_{\rm gen}(K^{(n)})$ | **odd Conj 5.1(P1/P2)**($\mathrm{arith}\subseteq\mathrm{gen}$ より)/ **(PR-S$^{\rm odd}_{\rm gen}$) 自身** | ★ **なし**。fake は (PR-S$^{\rm odd}_{\rm gen}$) と両立しないので前件が消え、**P6 には何も言えない** |
| **非算術証人** | $\mathrm{GT}_{\rm gen}(N)\setminus\mathrm{GT}_{\rm arith}(N)$(**窓は任意**) | **odd Conj 5.1(P1/P2)**($N$ が奇 dihedral 窓のとき) | ★ **(U-10) だけで (IH-S) $=$ 井原全射部**(§A.2 最小形) |

## A.4 P5 哨戒の P6 的意味づけ(**§3.3 末尾の 3 行を置換**)

1. **P5 哨戒の現行 predicate は fake(正典 Def 4.2・「全細分に survive するか」)である**(裁定 374 で確認)。**fake witness が出ても P1/P2 を殺すだけで P6 は生き残る。**
2. **P6 を殺すのは非算術証人**であり、その証人は「genuine であること」の証明を要する。正典 Cor 5.4 により **fake は有限証明書 1 個で確定するが genuine は有限深度では確定しない** ⟹ **非算術証人は原理的に「有限深度の PASS」からは作れない**(工房の掟 2 と同じ壁)。
3. ゆえに入手経路は「その窓で genuine 性(系 ML-D)を先に証明 → 然る後に非算術性を測る」の一本。**非算術性の側は装置がある**(定理 $R^{\rm cyc}_{\rm formal}$)⟹ **非算術証人の探索は genuine 側の証明一点に律速される**。裁定 374 により **entangled 屋根を作る線は P5 とは別戦線として台帳登録**される(系 SPLIT-NULL″ が名指しした線)。

## A.5 条文 pin 工程(裁定 374 ②)— **§8 申し送り 1 の処理結果**

**reader へ逐語抽出を発注済**(司令塔)。着弾後に本追補へ逐語 pin を貼り、**それから**便 98 に載せる。pin されるまで **ML-ODD は「条文 pin 未」**の札を外さない。

| 正典条文 | 本稿での**唯一の**効き所(照合時はここだけ見ればよい) |
|---|---|
| **2401 Prop 3.15**(isolated $\cap$ isolated $=$ isolated) | ① 補題 ML-3 の適用条件($I$ の**有向性**)— これが無いと ML-ODD (iii)$\Rightarrow$(i) が全崩壊 ② 命題 ROOF(3)($M=K^{(9)}\cap N_{\rm S4}$ の isolated 性) |
| **2401 Prop 3.14**($N^\diamond$ が isolated) | ML-ODD (ii)$\iff$(iii) の**「量化を isolated に制限してよい」段のみ**。落ちても (ii) を $\mathrm{NFI}$ 全体で量化すれば定理は生き残る(**射程が広がるだけで破綻しない**) |
| **2401 Cor 5.4**(genuine $\iff$ 全細分に survive) | ① ML-ODD (ii)$\iff$(iii) 本体 ② (iii)$\Rightarrow$(i) の $Y_N\ne\emptyset$ の段 ③ §A.4 の「fake は有限証明書・genuine は無限深度」 |

**凍結の維持**: 事前登録予言 **P-IHN-1〜7 は不変**(§6.5)。検算スクリプト `scratchpad/ihnec_check.py`(SHA-256 `edf618137697377f2eba5f4d59be53bd07ac5a598ee2246f70eedf372ad49309`)も不変。**実測 R4a/R4b の起票は reader 照合 PASS 後**(裁定 374 ②)。

> **⚠ pin 前に禁止すること**: ML-ODD を「定理」として他文書から引用しない・地図の P2/P6 行を ML-ODD で更新しない・U-11 を「閉じた」と書かない(R4a 未実施)。

## A.6 §8 申し送りの処理状況(**§8「申し送り」を更新**)

| # | 内容 | 状態(2026-08-01 裁定 374 後) |
|---|---|---|
| 1 | (DIR) の原文照合要請 | ★ **処理済 — reader へ発注済**(§A.5 が pin 先) |
| 2 | 用語の裁定要請 | ★ **裁定済 — 裁定 374 ①**(§A.1 が正本。地図 P1/P5 行は司令塔が次回一括更新で訂正) |
| 3 | U-11 を R4a に同梱 | **保留 — reader 照合 PASS 後に起票**(裁定 374 ②) |
| 4 | 系 SPLIT-NULL″ を哨戒設計原則に採るか | ★ **採用方向 — 「entangled 屋根 = 非算術証人の別戦線」として台帳登録**(裁定 374 ①末) |
| 5 | Sol 監査の優先順位案 | 変更なし(便 98 へ。**pin 後**) |
| 6 | R4a 先行・R4b 後追い | 変更なし(ただし起票は照合 PASS 後) |

---

# 追補 B(**裁定 376 = 条文 pin 差替**・2026-08-01)

**入力**: `docs/notes/reading_2401_ml_odd_pins_v1.md`(reader・150dpi ページ画像照合済)。
**位置づけ**: 追補 A.5 の pin 先表を置換し、逐語 pin を貼る。**v1 本文・追補 A の他節は不改変**。起草: 数学者(Opus 5)。

## B.1 逐語 pin 表(**§A.5 の表を置換**)

| 札 | 正典逐語(reader 抽出・p. は 2401) | 本稿での効き所 | 格 |
|---|---|---|---|
| **(SET)** | Def 3.13 (p.20): "*[m,f] ∈ GT(N) is called **settled** if ker(T_{m,f}) = N … N is called **isolated** if every GT-shadow in GT(N) is settled.*" | isolated の定義正本。§B.2 の証明が使う | **正典の定義** |
| **(INT)** | Prop 3.15 (p.21): "*For all N, K ∈ NFI^{isolated}_{PB₃}(B₃), N ∩ K ∈ NFI^{isolated}_{PB₃}(B₃).*" | ① 補題 ML-3 の適用条件($I$ の**有向性**)② 命題 ROOF(3)($M=K^{(9)}\cap N_{\rm S4}$ の isolated 性) | ★ **正典の言明・原論文に証明なし**(下記)⟹ **§B.2 で自前補完** |
| **(COF)** | Prop 3.14 の系 (p.21): "*Proposition 3.14 implies that the subposet NFI^{isolated}_{PB₃}(B₃) … is **cofinal**, i.e. for every N ∈ NFI_{PB₃}(B₃), there exists Ñ ∈ NFI^{isolated} such that Ñ ≤ N.*"(Prop 3.14 本体 = $N^\diamond:=\bigcap_{K\in\mathrm{Ob}(\mathrm{GTSh_{conn}}(N))}K$ (3.61) が isolated) | ML-ODD (ii)$\iff$(iii) の**「量化を isolated に制限してよい」段のみ** | **正典の定理**(証明あり;Prop 3.12・3.8 使用) |
| **(COR54)** | Cor 5.4 (p.28): "*Let N ∈ NFI_{PB₃}(B₃). A GT-shadow [m,f] ∈ GT(N) is **genuine** if and only if [m,f] belongs to the image of the map R_{K,N}: GT(K) → GT(N) for **every** K ∈ NFI_N(B₃).*" | ① ML-ODD (ii)$\iff$(iii) 本体 ② (iii)$\Rightarrow$(i) の $Y_N\ne\emptyset$ の段 ③ §A.4 の「fake は有限証明書・genuine は無限深度」 | **正典の定理** |
| **(HOM)** | Remark 3.16 (p.21): $N\le H$(共に isolated)で $R_{N,H}:\mathrm{GT}(N)\to\mathrm{GT}(H)$ は**群準同型**。(3.60): $R([m,f]):=(m+H_{\rm ord}\mathbb Z,\ fH_{F_2})$ | 系 ML-A(像が**部分群**の減少族であること)・命題 ROOF(3) | **正典の定理** |
| **(LIM)** | Thm 5.2: $\Psi:\widehat{GT}_{\rm gen}\cong\varprojlim\mathrm{ML}$(群同型 + 同相) | ML-ODD (iii)$\Rightarrow$(i) の最終段 | **正典の定理** |

> ### ★ 逐語照合で確定した 3 点(**本稿の記述を訂正・補強する**)
> 1. **(COR54) は $N$ 任意・$K\in\mathrm{NFI}_N(B_3)$ 任意で、奇数条件も isolated 制限も無い。** ⟹ 本稿 §4.3 の (ii)$\iff$(iii) の使用形は**逐語と整合**(私は「isolated に制限してよい」を別段として分けていた — その分離が正しかった)。
> 2. **共終性の出所は Prop 3.15 ではなく Prop 3.14 の系。** ⟹ v1 §1 表の **(DIR) 行は 2 つの別条文を 1 行に潰していた**(§B.3 で分解)。**有向性の実体(交叉閉)が 3.15 であることは正しかった。**
> 3. **Prop 3.15 の証明は原論文に無い**(逐語: "*The proof of the following proposition is straightforward and we leave it to the reader*")。⟹ **格は「正典の定理」ではなく「正典の言明(証明未掲載)」**。ML-ODD の最重要依存なので §B.2 で補完する。

## B.2 補題 INT(= 2401 Prop 3.15)の**自前証明**(裁定 376 ①)

> ### 補題 INT
> $N,H\in\mathrm{NFI}^{\rm isolated}_{PB_3}(B_3)$ ならば $M:=N\cap H\in\mathrm{NFI}^{\rm isolated}_{PB_3}(B_3)$。

**証明.** $M\trianglelefteq B_3$、$M\le PB_3$、$[B_3:M]\le[B_3:N][B_3:H]<\infty$ より $M\in\mathrm{NFI}_{PB_3}(B_3)$。$[m,f]\in\mathrm{GT}(M)$ を任意に取り、$K:=\ker T^M_{m,f}$ と置く。

**(段 1) $K\subseteq M$.** (3.60) より $R_{M,N}([m,f])=(m+N_{\rm ord}\mathbb Z,\ fN_{F_2})\in\mathrm{GT}(N)$。$\pi_N:B_3/M\twoheadrightarrow B_3/N$ を自然な射影とすると、生成元の上で
$$\pi_N\bigl(T^M_{m,f}(\sigma_1)\bigr)=\sigma_1^{2m+1}N,\qquad \pi_N\bigl(T^M_{m,f}(\sigma_2)\bigr)=f^{-1}\sigma_2^{2m+1}fN$$
であり、$x=\sigma_1^2$、$y=\sigma_2^2$ の $B_3/N$ での位数が $N_{\rm ord}$ を割ること(3.1)と $m\equiv m'\ (\mathrm{mod}\ N_{\rm ord})$、$f\equiv f'\ (\mathrm{mod}\ N_{F_2})$ から、これは $T^N_{R_{M,N}([m,f])}$ の生成元の像に一致する。ゆえに
$$\pi_N\circ T^M_{m,f}=T^N_{R_{M,N}([m,f])}.$$
$N$ は isolated だから (SET) より右辺は settled、すなわち $\ker\bigl(\pi_N\circ T^M_{m,f}\bigr)=N$。$K\subseteq\ker(\pi_N\circ T^M_{m,f})=N$。$H$ についても同様に $K\subseteq H$。よって $K\subseteq N\cap H=M$。

**(段 2) $K=M$.** $[m,f]$ は GT-shadow だから Def 3.7 より $T^M_{m,f}:B_3\to B_3/M$ は**全射**。準同型定理より $B_3/K\cong B_3/M$、ゆえに $[B_3:K]=[B_3:M]<\infty$(これは正典 Prop 3.8「指数一致」と同じ内容)。$K\subseteq M$ と有限指数の一致から $K=M$。

すなわち $[m,f]$ は settled。$[m,f]$ は任意だったから (SET) より $M$ は isolated。$\blacksquare$

> ### ★ 依存の向きの確認(**非循環** — この確認が無いと補完に意味がない)
> 上の証明が使ったのは **Def 3.7・Def 3.13 (SET)・(3.1)・(3.60)・準同型定理**のみ。**Prop 3.14・Prop 5.1・Thm 5.2・Cor 5.4 を一切使っていない。**
> これは重要である: reader 抽出によれば **正典 Prop 5.1 の証明が $N^{(1)}\cap N^{(2)}$ に Prop 3.15 を適用**しており、**Cor 5.4 の依存は Thm 5.2 + Prop 5.1 + 3.14/3.15** である。すなわち **正典側の $\text{3.15}\to\text{5.1}\to\text{5.4}$ の鎖も、証明未掲載の 3.15 に載っている**。§B.2 はその根も同時に支える(そして下流を使っていないので循環しない)。

> ### 格付け(**正直な形**)
> | # | 状態 |
> |---|---|
> | **2401 Prop 3.15 の言明** | **正典の言明**(p.21・逐語照合済)。**原論文に証明は無い**(読者演習と明記) |
> | **補題 INT の証明** | **paper-proof candidate**(本稿 §B.2・**Sol 未監査**)。**「正典の定理」と書いてはならない** |
> ⟹ **ML-ODD と命題 ROOF(3) の格は「補題 INT(工房の紙上証明)に相対的」**。Sol 監査の優先順位を §B.6 で 1 位に繰り上げる。

## B.3 (DIR) の分解(**§1 表の (DIR) 行を置換**・裁定 376 ③)

v1 §1 の表の **(DIR) 行は破棄**し、次の 2 行に置き換える。

| 札 | 言明 | 出所 | 効き所 |
|---|---|---|---|
| **(INT)** | isolated $\cap$ isolated $=$ isolated ⟹ **$I$ は refinement 順序で有向** | 2401 **Prop 3.15**(言明のみ)+ **本稿 §B.2 の証明** | 補題 ML-3・命題 ROOF(3) |
| **(COF)** | $\mathrm{NFI}^{\rm isolated}_{PB_3}(B_3)$ は $\mathrm{NFI}_{PB_3}(B_3)$ の中で**共終**($\forall N\ \exists\widetilde N\in\mathrm{NFI}^{\rm isolated},\ \widetilde N\le N$) | 2401 **Prop 3.14 の系**(p.21 逐語) | ML-ODD (ii)$\iff$(iii) の「isolated 制限」段**のみ** |

**本文の該当箇所の読み替え**(v1 §4.3 の (ii)$\iff$(iii) の末段):
> 「**isolated への制限で十分**であること: 任意の $K\in\mathrm{NFI}$ に対し **(DIR) の** $K^\diamond\subseteq K$ は isolated で…」
> ⟹ 「…**(COF) の** $K^\diamond\subseteq K$ は isolated で…」と読む(**(INT) ではない**)。

**重さの差**(照合の優先順位の根拠):
- **(INT) が落ちると ML-ODD (iii)$\Rightarrow$(i) は全崩壊**(補題 ML-3 の有向性が消える)。
- **(COF) が落ちても定理は生き残る** — (ii) の量化を $\mathrm{NFI}$ 全体に戻せばよい((COR54) は逐語で $K$ 任意なので、そのままで (ii)$\iff$(iii) が成立する)。**射程が広がるだけで破綻しない。**

## B.4 (COR54) の使用形の整合(裁定 376 ②)

逐語は **$N$ 任意・$K\in\mathrm{NFI}_N(B_3)$ 任意・isolated 制限なし・奇数条件なし**。本稿の使用は 3 箇所で、いずれも整合:

| 使用箇所 | 使用形 | 整合 |
|---|---|---|
| §4.3 (ii)$\iff$(iii) 本体 | $N=K^{(n)}$($n$ 奇)・$K$ は全細分 | ✓ 逐語の特殊化 |
| §4.3 (iii)$\Rightarrow$(i) の $Y_N\ne\emptyset$ | $N=K^{(n_0)}$・$K=N\in I$(**isolated な特定の 1 つ**) | ✓ 逐語が「$K$ 任意」なので isolated な $K$ でも当然成立 |
| §A.4 / §3.3 の「fake は有限証明書・genuine は無限深度」 | 否定側($\exists K$ で像に入らない)の読み | ✓ 逐語の否定 |

⟹ **(COR54) 側に修正は不要。** また §4.4 系 ML-A の「$\mathrm{GT}_{\rm gen}(K^{(n)})=\bigcap_{N}\mathrm{Im}\,R_{N,K^{(n)}}$」は逐語をそのまま集合の言葉に書き直したものである。**部分群**の減少族と言えるのは (HOM)(Remark 3.16 逐語)による。

## B.5 記法の申告(reader の気づきへの応答)

reader の指摘どおり **「$K^{(a)}\cap K^{(b)}$」は 2401 の記法ではなく 2405 側の記法**である。本稿 **補題 ML-1**($K^{(a)}\cap K^{(b)}=K^{(\mathrm{lcm}(a,b))}$)は **2405 の $\psi_n$・$K^{(n)}$ を使った工房の補題**であり、2401 側の対応物は Prop 3.15 の $N\cap K$ と Prop 5.1 の $N^{(1)}\cap N^{(2)}$ である。**補題 ML-1 を 2401 の定理として引用してはならない**(本稿 §4.2 の自前証明が出所)。

## B.6 差替後の格・工程

| 項目 | 差替前(追補 A.5) | **差替後(本追補)** |
|---|---|---|
| ML-ODD | 「条文 pin 未」 | ★ **pin 済**。ただし格は **paper-proof candidate / 補題 INT(工房の紙上証明)に相対的** — **「正典の定理に完全に乗っている」とは書かない** |
| 命題 ROOF(3)($M$ の isolated 性) | (DIR) 依存 | **(INT) 依存 ⟹ 補題 INT に相対的**(加えて前件 (S4-ISO)) |
| Sol 監査の優先順位(§8 申し送り 5) | ① ML-ODD (iii)$\Rightarrow$(i) … | ★ **① 補題 INT の証明(§B.2)を 1 位に繰り上げ** ② ML-ODD (iii)$\Rightarrow$(i) ③ 命題 ROOF(4) の Goursat 段 ④ §A.3 の型分離 ⑤ 前件表 §5.2 |
| **R4a**(11,772 判定) | 起票保留 | ★ **起票 GO**(裁定 376)。予言 P-IHN-1〜4・6・7 前半(U-11)が対象 |
| **R4b**(4,408,992 判定・12 シャード) | 起票保留 | **待機継続** — mine backend 修理の実証テスト後(裁定 376) |
| 予言 P-IHN-1〜7 | 凍結 | ★ **凍結不変**(検算 SHA-256 `edf6181376…d49309` も不変) |

> **pin 後も残る禁止事項**: 補題 INT が Sol 監査を通るまで、**ML-ODD を「正典に完全に還元された定理」として他文書から引用しない**。地図 P2/P6 行の更新は Sol 監査後。**U-11 は R4a 実施後にのみ「閉じた」と書く。**

---

# 追補 C(**R4a 実施記録**・裁定 376 GO・2026-08-01)

**実行者**: 数学者(Opus 5)。**script**: `scratchpad/ihnec_r4a_run.py`(SHA-256 `f8be65ae5bf1ed2b0a175bb88057e0fb1d36b9c790cd014ce1fa09eb9c88820b`)。
**入力(既存証明書・GAP 再走なし)**:
- `certificates/K9.v1.json` SHA-256 `ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e`
- `certificates/S4.v2.json` SHA-256 `c878673aa96dc22e0039e2e2b7868d68984d684ffed622de713af4ad566e0f4d`

**結果: failures 0 / ALL PASS。**

## C.1 設計からの変更(**先に申告する**)

v1 §6.6 の R4a は「因子ごとの**悉皆走査**を新規に回す」と書いた。実施にあたり、**両因子の悉皆走査は既に証明書として存在する**ことが判明したため、**再走せず証明書を入力とする独立実装**に切り替えた。

| | v1 §6.6 の設計 | **実施したもの** |
|---|---|---|
| 列挙 | GAP で新規悉皆走査 | **既存証明書を使用**(GAP 単系統のまま — **二系統一致ではない**) |
| 構造同定・組立 | GAP | **python の独立実装**(合成表を入力に $\Theta_9$ 座標で再導出) |

⟹ **格の正確な形**: **列挙は単系統**(GAP 証明書)。**構造同定と屋根の組立は独立第 2 実装**。**「cross-checked」とは書かない。**
なお証明書の `counts.raw_candidates = 8748 = 12\times729` は **v1 §6.6 R4a-1 で予言した走査規模と厳密に一致**した(設計のコスト模型の的中)。

## C.2 予言の照合(**P-IHN 凍結分**)

| # | 予言 | 実測 | 判定 |
|---|---|---|---|
| **P-IHN-4** | $\lvert\mathrm{GT}(M)\rvert=972$・$\mathfrak F_0(M)=81$・$\widetilde\chi$ 像 $=12$ | **972 = 81×12**(3 通りの数え方で一致) | ★ **HIT** |
| **P-IHN-5** | $\mathrm{Im}\,R_{M,K^{(9)}}=$ 全体(108/108) | 全 12 個の $m$-fiber を含む ⟹ **108/108 全射** | ★ **HIT** |
| **P-IHN-6** | $\mathrm{Im}\,R_{M,N_{\rm S4}}=$ 全体(54/54) | 全 6 個の $m$-fiber を含む ⟹ **54/54 全射** | ★ **HIT** |
| **P-IHN-7 前半(= U-11)** | $\mathrm{GT}(K^{(9)})\cong C_2\times\mathrm{Hol}(\mathbb Z/9)$ | **合成表 11,664 対すべてで $\mathrm{Aff}(\mathbb Z/9)\times C_2$ の積法則と一致**(下記 C.3) | ★ **HIT** |
| **P-IHN-1/2/3** | 比較不能・$PB_3/M\cong G_9\times\mathrm{PSL}(2,8)$・$M_{\rm ord}=18$ | **R4a の射程外**(紙の証明のみ・機械脚は未実施) | **未測定** |
| **P-IHN-7 後半** | $\mathrm{GT}(M)\cong((C_9\times C_9)\rtimes C_6)\times C_2$ | **R4b が要る**(GT(M) 自体は作っていない) | **未測定** |

**副次的に確認された正典・工房の主張**(証明書からの独立再導出):
- $K^{(9)}_{\rm ord}=18$・$\lvert\mathrm{GT}(K^{(9)})\rvert=108$・$m$-像 $=\mathcal X_9$(12 個)・各 fiber $=9$。
- Thm 4.3 (4.12) の $f$-三つ組の形($r^{2k},r^{-2k},r^{\varkappa(m)}$)が**全 108 shadow で成立**(第 2 成分 $=r^{-2k}$・第 3 成分 $=r^{\varkappa(m)}$ を各個検査)。
- $\lvert\mathrm{GT}(N_{\rm S4})\rvert=54$・$m$-像 $=\{0,2,3,5,6,8\}=$ charming set 全体・各 fiber $=9$。⟹ **§6.4 の「代替経路(framework-free)」が実測で成立**((S2)/W2-arith を使わずに系 SPLIT-NULL′ が $n=9$ で閉じた)。

## C.3 U-11 の閉鎖(**裁定 226 の待ち行列**)

$\Theta_9([m,f]):=\bigl(k,\ u=2m+1\bmod9,\ \varepsilon=m\bmod2\bigr)$($k$ は $f$-三つ組 第 1 成分 $=2k$ から復元)と置くと:

- $\Theta_9$ は $\mathrm{GT}(K^{(9)})\to\mathbb Z/9\times(\mathbb Z/9)^\times\times\mathbb Z/2$ の**全単射**(108 点・単射性を確認・$u$ 像 $=(\mathbb Z/9)^\times$)。
- **証明書の合成表の全 $108^2=11{,}664$ 対**で $\Theta_9(g_1\circ g_2)=(k_1+u_1k_2,\ u_1u_2,\ \varepsilon_1+\varepsilon_2)$ を検査 ⟹ **不一致 0**。

$$\boxed{\ \mathrm{GT}(K^{(9)})\ \cong\ \mathrm{Aff}(\mathbb Z/9)\times C_2\ =\ \mathrm{Hol}(\mathbb Z/9)\times C_2\quad(\textbf{明示同型・11,664 対で確定})\ }$$

**副産物**: これは **命題 E1-S1(自然座標)の $n=9$ での独立機械確認**でもある(E1 ノートの検算は $\Theta_n$ の全単射性と積を自作モデルで見たが、**正典由来の証明書の合成表で見たのは本件が初**)。
**測定した不変量**: 中心の位数 $=2$($\mathrm{Aff}(\mathbb Z/9)$ の中心自明 $+$ $C_2$ 因子と整合)。位数分布 $\{1{:}1,\ 2{:}19,\ 3{:}8,\ 6{:}44,\ 9{:}18,\ 18{:}18\}$(合計 108)。

> ### ⚠ U-11 の閉じ方の正確な形
> **数学的内容(同型型)は閉じた**。ただし **GAP の catalogue 番号 `[108,26]` というラベル自体は本実行では出していない**(python には IdGroup が無い)。`[108,26]=C_2\times\mathrm{Hol}(\mathbb Z/9)$ という同定は**裁定 213 の司令塔独立計算**に依る。⟹ 台帳には「**U-11 = 同型型で閉鎖(明示同型)/ IdGroup ラベルは裁定 213 の同定を経由**」と二段で書くこと。**「GAP で [108,26] を測った」とは書かない。**

## C.4 R4a が**確認していない**こと(**循環の防止**)

- **命題 ROOF(4)(fiber 積分解)は確認していない。** $\lvert\mathrm{GT}(M)\rvert=972$ と 2 つの像は **ROOF(4) を使って因子データから組み立てた値**である。⟹ **R4b(屋根での悉皆走査・4,408,992 判定)が ROOF(4) の独立確認であるという v1 §6.6 の役割分担は不変**(mine backend 修理の実証テスト後まで待機・裁定 376)。
- **P-IHN-1/2/3 の機械脚**(方法 CMP 手順 3 の `GroupHomomorphismByImages` 両向き・$\langle(X,X_P),(Y,Y_P)\rangle$ の位数 1,469,664・$M_{\rm ord}$)は **GAP が要る**。R4b と同じ批次に回すのが安い。
- **(S4-ISO)**(PSL(2,8) 窓の isolated 性)は依然 **機械測定のみ**。証明書の `isolated` 欄は `"UNKNOWN"` のまま。⟹ 命題 ROOF(3) と本実測の群論的解釈はこの前件に相対的。

## C.5 結論(**この 1 点が何を意味するか**)

$$\textbf{ML-ODD (ii) の finite instance 第 1 点は「全射」= 何も出なかった。} $$
これは**設計どおりの negative result** であり(定理 SPLIT-NULL が実測前に予言していた)、**fake が無いことの証拠では一切ない**(工房の掟 2)。得たものは:
1. **U-11 の閉鎖**(同型型・明示同型 11,664 対)。
2. **系 SPLIT-NULL′ が $n=9$ で framework-free に閉じた**($\mathfrak m(N_{\rm S4})=$ charming set 全体を実測)。
3. **方法 CMP と屋根の設計が実データで回ることの較正**。
4. ⟹ **次に作るべきは entangled 屋根**(系 SPLIT-NULL″・【IHNEC-GAP-2】)。$\mathrm{PSL}(2,8)$ 窓は共通商が自明で、**検出力ゼロが確定した**。
