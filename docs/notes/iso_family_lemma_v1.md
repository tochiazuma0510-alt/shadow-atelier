# isolated 性の族補題 — $SL(2,\mathbf Z/p^2)$ 型窓([Q3-c]・裁定 1058)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔([Q3-c])
対象 = $N'=\ker(B_3\to\tilde H)$、$PB_3/N'\cong SL(2,\mathbf Z/p^2)$、$c\in N'$($p=691$・$p\ge5$ 一様を狙う)
⚠ $u$/$c$ 非接触。**格: candidate**(Sol 未監査)。

---

## §0 結論(3 行)

1. ★★★ **補題 SETTLE-AUTO を得ました**:**shadow については well_defined $\Rightarrow$ settled**(有限性 + 全射性の 2 行)。⟹ **settled 判定が well_defined 判定だけに縮約**され、**kernel 計算が不要**になります。census **1034 件・例外 0** で実証。
2. ★★ **族補題を 2 形で定式化**:**ISO-FI**(fully invariant ⟹ isolated・verbal の一般化)と ★ **ISO-RIGID**(全射の rigidity ⟹ isolated)。
3. ⚠ **本件($SL(2,\mathbf Z/p^2)$ 型)については族補題は立ちません = UNKNOWN**。ISO-FI は前件を満たさず、ISO-RIGID は $(2,3)$-生成の多重性から**成り立ちにくい**と見ます。⟹ §5 に**残る道 3 本**。

---

## §1 ★★★ 補題 SETTLE-AUTO

> **【補題 SETTLE-AUTO】** $N\in\mathrm{NFI}_{PB_3}(B_3)$、$Q:=F_2/N_{F_2}$(有限)。GT-**shadow** $[m,f]$ について
> $$\textbf{well\_defined}\ \Longrightarrow\ \textbf{settled}.$$
>
> **証明**: shadow は Def 3.7 で**全射性**を含むので $T^{F_2}:F_2\twoheadrightarrow Q$。well_defined は「$T$ が $Q\to Q$ に降りる」= $N_{F_2}\subseteq\ker T$。降りれば $\bar T:Q\to Q$ は**全射**。$Q$ 有限ゆえ**全射自己準同型は単射** ⟹ $\ker\bar T=1$ ⟹ $\ker T^{F_2}=N_{F_2}$ ⟹ settled。∎

$$\boxed{\ \Longrightarrow\ \textbf{isolated}\iff\textbf{全 shadow で }T\ \textbf{が }Q\ \textbf{の自己準同型に降りる}\ }$$

★ **census による実証**: 全候補 **1034 件**(15 窓 + witness + 陽性対照 2 本)のうち `well_defined=True` は **622 件**、そのうち `kernel_size≠1` は ★ **0 件**。⟹ 補題と**完全に整合** ✔
★ **工学的帰結**: (Q3) の測定から **kernel 計算(高価)が落ちます** — well_defined 判定だけで済みます。

---

## §2 ★★ $E_{m,f}$ は $F_2$ の**自己準同型**(定式化の鍵)

定義ノート L171: $E_{m,f}(x)=x^{2m+1}$, $E_{m,f}(y)=f^{-1}y^{2m+1}f$、$f\in F_2$。
⟹ ★ **$E_{m,f}:F_2\to F_2$ は自己準同型**($F_2$ の外へ出ない)。

$$\boxed{\ \textbf{well\_defined}\iff E_{m,f}(N_{F_2})\subseteq N_{F_2}\ }$$

---

## §3 ★★ 族補題 その 1 — ISO-FI

> **【補題 ISO-FI】** $N_{F_2}$ が $F_2$ で **fully invariant**(完全不変 = **全自己準同型**で不変)ならば、$N$ は **isolated**。
>
> **証明**: 全 $(m,f)$ で $E_{m,f}(N_{F_2})\subseteq N_{F_2}$ ⟹ 全 shadow で well_defined ⟹ SETTLE-AUTO で全 shadow が settled ⟹ isolated。∎

★ **verbal 部分群は fully invariant** ⟹ 既出の「verbal ⟹ isolated」(`auto_settled_check_v1.md`)を**含みます**。
★ **新規部分**: fully invariant は verbal より**広い**(有限生成自由群では一致する場合もあるが一般には広い)⟹ **十分条件の拡張**。

⚠ **本件には使えません**: $N'_{F_2}$ は**単一の全射** $F_2\twoheadrightarrow SL(2,\mathbf Z/p^2)$ の核。fully invariant にするには**すべての** $SL(2,\mathbf Z/p^2)$-全射の核の交わりを取る必要があり、そのとき商は **subdirect product** であって $SL(2,\mathbf Z/p^2)$ 自身ではありません。
$$\boxed{\ \Longrightarrow\ \textbf{ISO-FI は本件の }N'\ \textbf{に直接適用できない}\ }$$

---

## §4 ★★ 族補題 その 2 — ISO-RIGID(**本件に効きうる形**)

$T$ が well_defined でないとき、$\ker T\ne N'$ かつ(全射性より)$B_3/\ker T\cong\tilde H$。
⟹ ★ **$\ker T$ は $\tilde H$ を商にもつ *別の* 正規部分群**(Def 3.13 の「別 source kernel」の正体)。

> **【補題 ISO-RIGID】** $B_3\twoheadrightarrow\tilde H$ なる全射が $\mathrm{Aut}(\tilde H)$ の作用で**単一軌道**(= rigid)ならば、$N'$ は isolated。
>
> **証明**: $\ker T$ と $N'$ はどちらも $B_3\twoheadrightarrow\tilde H$ の核。単一軌道なら $\exists\alpha\in\mathrm{Aut}(\tilde H)$ で二つの全射が移り合う ⟹ **核が一致** ⟹ $\ker T=N'$ ⟹ settled(全 shadow)⟹ isolated。∎

★ **判定量**: $z=1$(段 2 前検査 §2)より **braid 対 ⟷ $(2,3)$-生成対の全単射**が使えます ⟹
$$\boxed{\ \textbf{判定量} = \tilde H\ \textbf{の}(2,3)\text{-生成対の}\ \mathrm{Aut}(\tilde H)\text{-軌道数}\ }$$

⚠ **見込み**: $SL^\pm(2,q)$ 型の群は $(2,3)$-生成対を**多数**もつのが普通(witness が trial 1 で当たったことも示唆的)⟹ ★ **単一軌道は成り立ちにくい** ⟹ **ISO-RIGID の前件は満たされない見込み**。

### 4.1 ★ 弱形(本件に残る唯一の現実的な形)
> **【ISO-RIGID$^{\rm w}$】** **GT 形の全射のみ**($\sigma_1\mapsto\sigma_1^u$、$\sigma_2\mapsto f^{-1}\sigma_2^uf$)を考え、それらの核がすべて $N'$ に一致すれば isolated。

★ **GT 形は非常に特殊**($\sigma_1$ の像が $\sigma_1$ の**冪そのもの**)⟹ 一般の $(2,3)$-生成対より**桁違いに少ない** ⟹ ★ **弱形なら成り立つ可能性が残ります**。

### 4.2 ★ $\mathrm{Aut}(Q)$ 経由の必要条件(実行可能)
well_defined なら $\bar T$ は $Q$ の全射自己準同型 ⟹ **自己同型**。$Q=SL(2,\mathbf Z/p^2)$ は素体上ゆえ体自己同型がなく $\mathrm{Aut}(Q)\cong PGL(2,\mathbf Z/p^2)$(内部・対角)⟹ $\bar T$ は**共役**。
$$\boxed{\ \textbf{必要条件}:\ \bar x^{\,u}\sim\bar x\ \textbf{かつ}\ \bar f^{-1}\bar y^{\,u}\bar f\sim\bar y\ \textbf{が}\textbf{同時に}\textbf{一つの }g\ \textbf{で実現される}\ }$$
⟹ ★ **charming $u$ ごとに「$\bar x^u$ が $\bar x$ に共役か」を先に見れば、大半の $u$ が落ちる可能性があります**(安い前フィルタ)。

---

## §5 ⚠ 本件の判定 — **UNKNOWN**(正直な申告)と、残る道 3 本

$$\boxed{\ SL(2,\mathbf Z/p^2)\ \textbf{型窓の isolated 性は、本ノートでは}\ \textbf{立ちません}\ }$$
理由: ISO-FI は前件不成立(§3)/ ISO-RIGID は前件が成り立ちにくい(§4)。

**残る道(推薦順)**
1. ★★ **[R1] ISO-RIGID$^{\rm w}$ の実行**: GT 形全射の核が一意かを、**$\mathrm{Aut}(Q)$ 経由の必要条件**(§4.2)で先にふるう。⟹ **charming $u$ の集合を $N_{\rm ord}$ から求め、$\bar x^u\sim\bar x$ を満たす $u$ だけ残す** — これは **$Q$ の共役類だけの計算**で、$GT(N')$ の列挙は不要 ⟹ ★ **規模の壁を回避**。
2. ★ **[R2] $c\in N$ 側の単純化を使う**: $c\in N'$ ゆえ $\tau$ は降り、hexagon は簡約形 (3.10)(3.11) が $Q$ 内で完結(wcp5d の 16/16 安全側)⟹ **列挙器の分岐が不要**。⟹ ただし規模の壁は残る。
3. ★ **[R3] 正典 Prop 3.14 系の直接適用**: $N^\diamond$(成分の全対象の交わり)は isolated。⟹ **$N'$ 自体でなく $N'^\diamond$ に降りて話を進める**路。⚠ その場合 $B_3/N'^\diamond$ は $\tilde H$ より大きく、段 2 の対象が変わる ⟹ ★ **③ 線の標的の付け替え**になるので**司令塔裁定事項**。

---

## §6 実行仕様([R1]・実装係へ直結)

```
=== [Q3-R1] GT 形全射の一意性(ISO-RIGID^w の前フィルタ)===
根拠: docs/notes/iso_family_lemma_v1.md §4.2 / 前提 = Q := PB_3/N' ≅ SL(2,Z/691^2)
⚠ GT(N') の列挙は *しない*(規模 6.5e17)。Q の共役類だけを使う。

[R1-a] N_ord を出す: N_ord = lcm(ord(x̄), ord(ȳ))(c∈N' ゆえ ord(c)=1)
       ⟹ charming な u = 2m+1 ∈ (Z/N_ord)^× の集合 X を確定
[R1-b] ★ 前フィルタ: 各 u ∈ X について「x̄^u が x̄ と共役か」を判定
       (Q の共役類は SL(2,Z/p^2) の標準的な分類で書ける ⟹ 巨大群を構成せず判定可)
       ⟹ 落ちた u は well_defined になり得ない ⟹ その u の shadow は非 settled 候補
[R1-c] ★ 判定:
       ・残る u が 1 個も無い ⟹ ★ shadow が存在しない ⟹ isolated は自明(空虚)⟹ 要別扱い
       ・残る u があれば、その u についてのみ ȳ 側の同時共役性を検査
[R1-d] 見張り: SETTLE-AUTO により kernel 計算は *不要*(well_defined だけ測る)
出力: cert (schema q3_r1/v1)。u_touched=false ; c_touched=false
```

---

## §7 GAP・記帳

- **【ISO-GAP-1】(中・新)** ISO-RIGID$^{\rm w}$ の前件($GT$ 形全射の核の一意性)は未証明。⟹ [R1] が実測路。
- **【ISO-GAP-2】(小・新)** §4.2 の必要条件は「$\bar x^u\sim\bar x$」だが、**十分条件は「対の同時共役」**。前者だけでは判定できません(片側フィルタ)。
- **【S2-GAP-5】★ 縮小**: SETTLE-AUTO により kernel 計算が落ち、[R1] で $GT(N')$ の構成も回避 ⟹ **規模の壁は前フィルタで越えられる見込み**。
- ★ **本ノートの新規部分**: ① **補題 SETTLE-AUTO**(well_defined ⟹ settled・census 1034 件で実証)② **$E_{m,f}$ が $F_2$ の自己準同型**であることを使った well_defined の再定式化 ③ **ISO-FI**(fully invariant ⟹ isolated・verbal の一般化)④ **ISO-RIGID / ISO-RIGID$^{\rm w}$**(全射の rigidity ⟹ isolated)と判定量($(2,3)$-生成対の $\mathrm{Aut}$-軌道数)⑤ $\mathrm{Aut}(Q)=PGL(2,\mathbf Z/p^2)$ 経由の**安い前フィルタ**。
- ⚠ **正直な申告**: **族補題は立っていません**。得たのは **(a) 判定の縮約(SETTLE-AUTO)(b) 2 つの十分条件 (c) 規模の壁を回避する前フィルタ**で、**$SL(2,\mathbf Z/p^2)$ 型の isolated 性そのものは UNKNOWN** です。
- **申告**: 機械走行ゼロ(census の既走値の再集計のみ)・$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
