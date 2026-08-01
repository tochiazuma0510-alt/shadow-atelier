# 追補(erratum・小)— **F93-5.2 の局所修文**: $N^{\rm gen}\le\mathcal N^{\rm w}\le\mathcal N^{\rm tr}$ と、$m=1$ 列挙の自己完結化

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01
- 位置づけ: `docs/notes/t3_quasi_purecycle_rigidity_v1.md`(本体)+ `_addendum_t0.md`(第 1 追補)+ `_addendum_weighted.md`(第 2 追補)への **第 3 追補**。**erratum 方式 — 既存 3 本は 1 バイトも書き換えない。**
- 委嘱: 司令塔(便 93 修理波・裁定 303)「T3-WALL″ の局所修文 1 件(Sol 指摘箇所)」
- 入力正本: `sol/sol_reply_93_math20.md` **F93-5.2**
- 検算: `search/probe/wac_v1/repair93_check.py` §E(SHA-256 `d35e7949…0faaf4e2`)

> **Sol の判定(F93-5.2 末尾)**: 「上の一文を直す NOTE つきで **T3 theorem group と weighted addendum の完全採択を承認する**。旧記法との衝突では weighted addendum を正本とする。」
> ⟹ **本追補がその NOTE である。** これで T3 系は完全採択の条件を充たす。

---

## 1. 【修文 E93-1】(**主件**)— 第 2 追補 §1 の一般文は $n\ge4$ で偽

### 1.1 該当箇所(逐語)

> 第 2 追補 §1 末尾:
> **$\mathcal N^{\mathrm w}$ と $N^{\mathrm{gen}}$ の間には一般に大小関係すらない**(⑥ の例では $\mathcal N^{\mathrm w}=1>0=N^{\mathrm{gen}}$;**逆に $\mathrm{Aut}$ が大きい非生成類が多ければ $\mathcal N^{\mathrm w}<N^{\mathrm{gen}}$ も原理的に起こりうる**)。

**太字の後半が偽である。**

### 1.2 修文後の正本

> ### 補題 E93-1(三量の順序)【定理・2 行・$n\ge4$】
> $n\ge4$ のとき
> $$\boxed{\ N^{\mathrm{gen}}\ \le\ \mathcal N^{\mathrm w}\ \le\ \mathcal N^{\mathrm{tr}}\ }$$
> **証明.**
> - **右**: $\mathcal N^{\mathrm w}=\sum_{M\ \text{推移}}1/\lvert\mathrm{Aut}(M)\rvert$ の各項は $\le1$、項数は $\mathcal N^{\mathrm{tr}}$。
> - **左**: 生成類 $M$($\langle g,h\rangle\supseteq A_n$)は $\mathrm{Aut}(M)=C_{S_n}(\langle g,h\rangle)\le C_{S_n}(A_n)=1$($n\ge4$;第 2 追補 系 T3-N0″-a の (A-gen))ゆえ **weight ちょうど 1** を寄与する。非生成な推移類の weight は $>0$。ゆえに $\mathcal N^{\mathrm w}\ge N^{\mathrm{gen}}$。∎
>
> **⟹ $\mathcal N^{\mathrm w}<N^{\mathrm{gen}}$ は $n\ge4$ では起こりえない。** 第 2 追補 §1 の括弧内後半を削除し、上式に置き換える。

### 1.3 $n\le3$ の但し書き(修文の射程)

$n=3$ では $C_{S_3}(A_3)=A_3\cong C_3\ne1$ なので (A-gen) が空振りし、生成類でも weight $1/3$ がありうる ⟹ **左の不等号は $n\le3$ で保証されない**。第 2 追補 §5 の $m=1$ 表には $n=1,2,3$ の退化行があるので、**補題 E93-1 は $n\ge4$ に限る**と明記する。**(J) 域($\ell$ 素数・$n/2<\ell\le n-3$)は $n\ge8$ を含意する**ので、T3-WALL″ の証明鎖には何の影響も無い。

### 1.4 実データ照合(機械・§E)

| $(\ell,t,n)$ | $N^{\rm gen}$ | $\mathcal N^{\rm w}$ | $\mathcal N^{\rm tr}$ | $N^{\rm gen}\le\mathcal N^{\rm w}\le\mathcal N^{\rm tr}$ |
|---|---|---|---|---|
| $(7,2,9)$ | 0 | 1 | 1 | ✓ |
| $(9,1,10)$ | 6 | 6 | 6 | ✓(等号 3 つ = (J) 域) |
| $(9,3,12)$ | 0 | $1/3$ | 1 | ✓ |
| $(3,1,4)$ | 1 | 1 | 1 | ✓ |

### 1.5 T3-WALL″ への影響 — **無い**(明示)

系 T3-WALL″ の証明鎖の段 1 は「(J) ⟹ 補題 J-AUT ⟹ $N^{\mathrm{gen}}=\mathcal N^{\mathrm w}$」という**等号**であり、大小関係の一般論は一度も使っていない。⟹ **$(n,\ell,t,k,j)=(24,19,5,12,8)$ の一意性は無傷**(Sol も「この局所修文は T3-WALL″ の結論を壊さない」と明言)。

> **★教材**: 「一般には大小関係すら無い」と書くときは、**自分の設定でその一般性が本当に成り立つか**を一度確かめること。私は $\mathcal N^{\rm w}$ の項が $\le1$ であることばかり見て、**生成類の項は必ず $=1$** という(自分で §2 に書いた)事実を、隣の段落で使い忘れた。**同じ文書の中で自分の補題を使い落とす**型の誤りである。

---

## 2. 【修文 E93-2】(**従件**)— $m=1$ 列挙の自己完結化(第 2 追補 §5)

Sol F93-5.2: 「$m=1$ の五 passport は実現可能なものを尽くしている。見かけ上の**第六候補 $(t,f_2,f_3)=(0,2,0)$** は方程式から $n=0$ を強制し、$n\ge1$ で不可能、と一行明記すると列挙が自己完結する。」

> ### 追加の一行(第 2 追補 §5 の表に添える)
> $t+f_2+f_3=2$ の多重集合は $\{(1,1,0),(1,0,1),(0,1,1),(2,0,0),(0,0,2),(0,2,0)\}$ の **6 通り**。最後の $(0,2,0)$ は
> $$k=\frac{n-f_2}2=\frac{n-2}2,\qquad j=\frac{n-f_3}3=\frac n3,\qquad k+2j=n+t-1=n-1$$
> に代入して
> $$\frac{n-2}2+\frac{2n}3=n-1\ \Longleftrightarrow\ 3(n-2)+4n=6(n-1)\ \Longleftrightarrow\ 7n-6=6n-6\ \Longleftrightarrow\ n=0$$
> ⟹ **$n\ge1$ では不可能。ゆえに $m=1$ 層の realizable passport はちょうど 5 個**であり、第 2 追補 §5 の表は完全である。∎

**同じ式で 5 行を再検算**(自己完結の確認):$(1,1,0)\Rightarrow n=3$、$(1,0,1)\Rightarrow n=4$、$(0,1,1)\Rightarrow n=1$、$(2,0,0)\Rightarrow n=6$、$(0,0,2)\Rightarrow n=2$ — **すべて第 2 追補 §5 の表と一致** ✓

---

## 3. 格付け(本追補の分)

| 主張 | 格 |
|---|---|
| **補題 E93-1**($N^{\rm gen}\le\mathcal N^{\rm w}\le\mathcal N^{\rm tr}$・$n\ge4$) | **定理**(2 行)+ 4 行の実データ照合 |
| 第 2 追補 §1 の括弧内後半の削除 | **erratum**(私の誤記) |
| $n\le3$ での射程限定 | **明示**((J) 域は $n\ge8$ ゆえ無害) |
| $(0,2,0)\Rightarrow n=0$ | **proof**(1 行)⟹ $m=1$ 層の列挙が**自己完結** |
| 系 T3-WALL″ の結論 | **無傷**(Sol 追認) |
| 種数 $\ge1$ の閉形【GAP-T3a】 | **UNKNOWN のまま** |
| 外部新規性 | **主張しない**(第 2 追補 §7 のまま) |
