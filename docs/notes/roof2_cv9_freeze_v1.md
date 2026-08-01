# 屋根第 2 点 $M_2=K^{(9)}\cap L$ — 紙 + CV-9 主検問用 IF-FIRST 凍結宣言 v1

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01
- 委嘱: 司令塔 **札 D**(発案第 18 便・裁定 394)「entangled 屋根の在庫レシピ — $n=9\times L$(Heisenberg 交叉)が SPLIT-NULL 前件を満たさない初の実測対象 = GEN(9) への初実弾」
- 様式: `docs/notes/gtpi_cv9_freeze_v1.md`(GTPI)/ `docs/notes/ihnec_v1.md` §6.5(R4a/R4b)の CV-9 IF-FIRST 凍結様式
- **本ファイルは $\mathrm{GT}(M_2)$ の列挙を一切走らせる前に固定する。以後、実測結果によって書き換えない**(改訂が要るなら v2 を作る)。
- **封印非接触**: $K^{(5)}$ blind campaign の封印 3 量に触れていない。$n=5$ 非接触。

---

## 0. 先に結論 3 行(司令塔向け)

1. **札 D の前提は正しい**: $E:=B_3/(K^{(9)}L)\cong B_3/K^{(3)}$(位数 648・$E_0\cong G_3$・位数 108)は**非自明**であり、$(K^{(9)},L)$ 対は定理 SPLIT-NULL の前件(共通商自明)を**満たさない**。工房初の実例である。
2. **しかし前件が破れても結論は破れない**。$L=K^{(3)}\cap N_0$ かつ $K^{(9)}\subseteq K^{(3)}$ ゆえ $M_2=K^{(9)}\cap L=K^{(9)}\cap N_0$ であり、**この第 2 表示では屋根は分裂している**(定理 REFACT)。⟹ SPLIT-NULL の結論(像 = $m$-fiber の合併)が適用され、(MCOV) も成立するので **$R_{M_2,K^{(9)}}$ は全射 108/108 と予言される**。$M_2$ は **GEN(9) への実弾ではない**。
3. **代わりに得たもの**: ①「本質的 entangle 性」の正しい判定条件(命題 ENT-CRIT = **正規補群の非存在**)②GEN(9) の**狩場の局在**(系 GEN9-$\Lambda$: 定理 K3 の下で非 genuine 部分は $\Lambda=\ker(\mathrm{GT}(K^{(9)})\to\mathrm{GT}(K^{(3)}))\cong C_3\times C_3$ の方向にしか存在し得ない)③entangled 屋根レシピの**修理仕様**(【IHNEC-GAP-5】・中心 $C_3$ では原理的に不可能・非自明 $Q$-指標つき $C_3$ が唯一の道)。

> **札 D への評価**: 「$N'\subseteq K^{(d)}$($d\mid n$ 奇)なら共通商が非自明」は**正しい**。誤っていたのは「共通商が非自明 ⟹ 検出力がある」という含意で、これは便 98 F98-3.7 が撤回した旧 SPLIT-NULL″ の裏返しの誤り(前件の必要条件と十分条件の混同)である。**今回の対象は 5 件目の同型事故ではなく、レシピの論理型の誤り**であり、修理の型は §7 に書いた。

---

## 1. 事前登録(universe)— 走査前に固定・後から変えない

### 1.1 対象は 1 個

$$\boxed{\ M_2\ :=\ K^{(9)}\cap L,\qquad L:=K^{(3)}\cap N_0,\qquad N_0:=\pi^{-1}(V),\ \ V:=F_2^3\gamma_3(F_2)\ }$$

$\pi:PB_3\twoheadrightarrow PB_3/\langle c\rangle\cong F_2$、$H_3:=F_2/V$ = 位数 27 の Heisenberg 群(自由 class-2・exponent-3 商)。座標規約は `docs/week3-L設計.md` §1 を**逐語**採用: 元 $=(a,b,e)\in(\mathbb Z/3)^3$、$X=(1,0,0)$、$Y=(0,1,0)$、$(a,b,e)(a',b',e')=(a+a',b+b',e+e'+ab')$、$Z:=[X,Y]=(0,0,1)$。

**他の窓は触らない**($n=5$ 非接触・$N_{\rm S4}$ は §6 のアンカーとしてのみ再現)。

### 1.2 入力(既存・再測定しない)

| 出所 | SHA-256 | 使う内容 |
|---|---|---|
| `certificates/K3.v1.json` | `d7cd44ea6d71e341e3e1a6164ce03540e92c50d405113ad1d3dc26972b1e8171` | $\lvert\mathrm{GT}(K^{(3)})\rvert=12$・$K^{(3)}_{\rm ord}=6$・$[PB_3{:}K^{(3)}]=108$・$\lvert[G_3,G_3]\rvert=27$ |
| `certificates/K9.v1.json` | `ceac37e0039454d41254e549569aecef415ef4e3e53e484b0fc33ef6bffb8e5e` | $\lvert\mathrm{GT}(K^{(9)})\rvert=108$・$K^{(9)}_{\rm ord}=18$・$[PB_3{:}K^{(9)}]=2916$・$\lvert A_9\rvert=729$・reduction$\to$K3 |
| `certificates/L01.v1.json` | `a9121843cea1dc8f6d65c9e6e450a00a416986fb7f72f61b4d87358bb00b4b29` | $\lvert\mathrm{GT}(L)\rvert=36$・$L_{\rm ord}=6$・$[PB_3{:}L]=2916$・reduction$\to$K3(全射) |
| `docs/命題_中心持ち上げ_v2.md` | `7463e7281fe9df323ab2670517b31dcaa57befde8b1bced7c6d0d7aeece0b7e8` | 定理 A・補題 B/C/D0/D/E/F/G(**紙上相互監査 PASS**・Sol 便 05) |
| `docs/notes/ihnec_v1.md` | `498b24ef9e907b0708c0915c36aa3e2a13bf07e63c753967e920d4731bfe663f` | 定理 SPLIT-NULL・(MCOV)・命題 ROOF・方法 CMP |

**検算スクリプト**: `scratchpad/roof2_check.py`(SHA-256 `62de27427e78afe4e2259d6d7fa8545f6ecf1e4ab126322ec7c863be47677cc2`)。整数演算と証明書の読み出しのみ・**GT の列挙は一切していない**(IF-FIRST の「実測」に当たらない)。**failures 0 / ALL PASS**。**これは cross-check であって証明ではない。**

### 1.3 $L\subseteq K^{(3)}$ の機械確認(委嘱 §1 の「要確認」)

紙: 定義から $L=K^{(3)}\cap N_0\subseteq K^{(3)}$(`命題_中心持ち上げ_v2.md` (L1))。
機械(証明書のみから・検算 §2):

- `L01.v1.json` に `reduction: {to:"K3", surjective:true}` が**存在する**。$R_{N,H}$ (3.60) は $N\subseteq H$ のときにしか定義されないので、この欄の存在自体が $L\subseteq K^{(3)}$ の証明書側の主張である。
- その `image` は長さ 36・値域が $\{0,\dots,11\}$ を**過不足なく**覆い、**各値ちょうど 3 回**(繊維一様 3 = 定理 A(iii) と一致)。
- 指数の整合: $[PB_3{:}L]=2916=27\cdot108=\lvert H_3\rvert\cdot[PB_3{:}K^{(3)}]$。

⟹ **$L\subseteq K^{(3)}$ は紙 + 証明書の二重で確定**(ALL PASS)。

---

## 2. 補題群(すべて既存補題の逐語移送・新規の証明段は 2 か所のみ)

> ### 補題 D0$^n$($G_n$ の可換化 — **補題 D0 の $n$ 一般化**)
> 奇 $n\ge3$ に対し $G_n=\langle a,b\rangle\le D_n^3$、$a=(r,s,s)$、$b=(rs,r,rs)$(2405 (3.1) の marked 生成系)とすると
> $$[G_n,G_n]=R:=\langle r\rangle^3\cong C_n^3,\qquad G_n^{\rm ab}\cong C_2^2 .$$
> とくに **$3\nmid\lvert G_n^{\rm ab}\rvert$** であり、**$C_3$ は $G_n$ の商ではない**。

**証明.** `命題_中心持ち上げ_v2.md` 補題 D0 の 4 段を逐語移送する。$a^2=(r^2,1,1)$、$b^2=(1,r^2,1)$、$(ab)^2=(1,1,r)$ は $D_n$ の関係式($s^2=(rs)^2=1$・$sr=r^{-1}s$)だけを使うので $n$ に依らない。$n$ 奇より $\gcd(2,n)=1$ ゆえ $\langle r^2\rangle=\langle r\rangle$、したがって $\langle a^2,b^2,(ab)^2\rangle=R$。$G_n/R$ は各座標が $D_n/\langle r\rangle\cong C_2$ に落ちて $a\mapsto(0,1,1)$、$b\mapsto(1,0,1)$ ⟹ 位数 4 の $C_2^2$。可換ゆえ $[G_n,G_n]\le R$。逆向きは共役作用: $a$ は座標 2,3 を、$b$ は座標 1,3 を反転する($srs^{-1}=r^{-1}$)ので **3 座標のいずれもある $g\in Q$ で反転される**;$[e_i,g]=e_i^{-2}=e_i^{\,n-2}$ で $\gcd(n-2,n)=\gcd(2,n)=1$ より $\langle[e_i,g]\rangle=\langle e_i\rangle$。ゆえに $[R,Q]=R\le[G_n,G_n]$。∎

**機械側の独立確認**(検算 §1): $\lvert G_3\rvert/\lvert[G_3,G_3]\rvert=108/27=4$、$\lvert G_9\rvert/\lvert[G_9,G_9]\rvert=2916/729=4$(両方とも証明書 `derived_order` 欄から)。

> ### 補題 D1$^n$($G_n$ と $H_3$ は非自明な共通商をもたない)
> 奇 $n\ge3$。$G_n$ と $H_3$ の共通商は自明のみ。ゆえに部分直積 $S\le G_n\times H_3$ は必ず $S=G_n\times H_3$。

**証明.** 非自明な共通商 $D$ があればその単純商 $T$ は両者の共通単純商。$H_3$ は 3 群なので $T\cong C_3$。$C_3$ が $G_n$ の商なら $3\mid\lvert G_n^{\rm ab}\rvert=4$ — 矛盾(補題 D0$^n$)。Goursat より部分直積は共通商上の fiber 積、共通商自明なら全体。∎
(`命題_中心持ち上げ_v2.md` 補題 D.1 の $G_3\to G_n$ 置換。**$n=9$ での機械側の別証**: `week3-L設計.md` §1 の Sylow 橋渡し補題 —「$p$ 群商は Sylow $p$ 部分群の商」+ $\mathrm{Syl}_3(G_9)$ 可換(前哨の独立検算)+ $H_3$ 非可換。**二経路が一致**。)

> ### 補題 N0($N_0$ の完全記述)【**本稿の新規段 1**】
> $N_0\in\mathrm{NFI}_{PB_3}(B_3)$ であり
> $$(N_0)_{\rm ord}=3,\quad \mathcal X_{N_0}=\{0,2\},\quad \mathrm{GT}(N_0)=\{[m,Z^a]\ :\ m\in\{0,2\},\ a\in\mathbb Z/3\},\quad\lvert\mathrm{GT}(N_0)\rvert=6,$$
> **全 6 元は settled ⟹ $N_0$ は isolated**、$\mathfrak m(N_0)=\{0,2\}$、$\mathfrak F_0(N_0)=\langle Z\rangle\cong C_3$。

**証明.**(定理 A の証明を $K^{(3)}$ 成分を取り除いた形で走らせる。使う補題はすべて既存。)
- $N_0\in\mathrm{NFI}_{PB_3}(B_3)$: $V$ は verbal ゆえ $F_2$ で characteristic、$\langle c\rangle=Z(PB_3)$ は characteristic、$PB_3\trianglelefteq B_3$ ⟹ $N_0\trianglelefteq B_3$、$N_0\le PB_3$、$[PB_3{:}N_0]=27$((L1) と同じ論法)。$c\in N_0$ ゆえ $PB_3/N_0\cong F_2/V=H_3$。
- $(N_0)_{\rm ord}=\mathrm{lcm}(\mathrm{ord}(X),\mathrm{ord}(Y),1)=3$ ⟹ $\mathcal X_{N_0}=\{m\in\mathbb Z/3:\gcd(2m+1,3)=1\}=\{0,2\}$。
- **charming**: $f$ の像は $[H_3,H_3]=Z(H_3)=\langle Z\rangle$(補題 B.1)⟹ $f\mapsto Z^a$。
- **hexagon**: 補題 C.1/C.2 により (3.10) は全 $a$ で恒真、(3.11) は $m\not\equiv1\ (3)$ で全 $a$ で恒真。charming が $m\equiv1\ (3)$ を排除する(補題 C.3・$3\mid(N_0)_{\rm ord}$)ので**例外は空虚**。
- **全射性**: $\langle X^u,\ Z^{-a}Y^uZ^a\rangle=\langle X^u,Y^u\rangle=H_3$($Z$ 中心・$\gcd(u,3)=1$・exponent 3;補題 E の $H_3$ 成分の議論そのもの)。
- **settled**: $T^{PB_3}_{m,f}$ は $x\mapsto X^u,\ y\mapsto Y^u,\ c\mapsto1$、すなわち $\gamma_u\circ P_{N_0}$($\gamma_u\in\mathrm{Aut}(H_3)$ は補題 G)。補題 F((3.32))より settled。6 元すべてで同じ議論。∎

> ### 命題 E(**委嘱 §1 の本題** — 共通商の明示同定)
> $$K^{(9)}\!\cdot\!L=K^{(3)},\qquad\text{ゆえに}\qquad \boxed{\ E_0:=PB_3/(K^{(9)}L)\ \cong\ G_3\ (\lvert\ \rvert=108),\qquad E:=B_3/(K^{(9)}L)\ \cong\ B_3/K^{(3)}\ (\lvert\ \rvert=648)\ }$$
> $1\to E_0\to E\to S_3\to1$ は $B_3/K^{(3)}$ の標準列そのもの。**$E_0\ne1$ ゆえ $(K^{(9)},L)$ 対は定理 SPLIT-NULL の前件を満たさない。**

**証明.** $K^{(9)}\subseteq K^{(3)}$(補題 E1-D2(3) / ML-1: $K^{(a)}\cap K^{(b)}=K^{(\mathrm{lcm})}$)。
$PB_3/(K^{(9)}N_0)$ は $G_9$ と $H_3$ の共通商だから補題 D1$^9$ より自明、すなわち $K^{(9)}N_0=PB_3$。
Dedekind の modular law($K^{(9)}\subseteq K^{(3)}$ より)
$$K^{(9)}L=K^{(9)}(N_0\cap K^{(3)})=(K^{(9)}N_0)\cap K^{(3)}=PB_3\cap K^{(3)}=K^{(3)} .$$
$E_0=PB_3/K^{(3)}=G_3$、$E=B_3/K^{(3)}$、$[B_3{:}PB_3]=6$ より $\lvert E\rvert=648$。$E_0\ne1$。∎

**Goursat の形**: $PB_3/M_2\ \cong\ G_9\times_{G_3}(G_3\times H_3)$(共通商 $G_3$ 上の fiber 積)。位数は $2916\cdot2916/108=78{,}732$。

> ### 定理 REFACT(**屋根の再表示 — 本稿の核心**)【**本稿の新規段 2**】
> 奇 $d\mid n$、$N'=K^{(d)}\cap N_0'$($N_0'\in\mathrm{NFI}_{PB_3}(B_3)$)の形の窓に対し、$K^{(n)}\subseteq K^{(d)}$ より
> $$\boxed{\ K^{(n)}\cap N'\ =\ K^{(n)}\cap N_0'\ }$$
> すなわち**屋根は $N'$ の $K^{(d)}$ 成分に一切依存しない**。一方 $(K^{(n)},N')$ の Goursat 共通商 $E_0$ は $G_d$ を商にもつので**非自明**である。
> ⟹ **「$(K^{(n)},N')$ の共通商が非自明」は屋根 $M$ の検出力について何も言わない。** 検出力を支配するのは $(K^{(n)},N_0')$ 対である。

**証明.** $K^{(n)}\cap N'=K^{(n)}\cap K^{(d)}\cap N_0'=K^{(n)}\cap N_0'$($K^{(n)}\cap K^{(d)}=K^{(\mathrm{lcm}(n,d))}=K^{(n)}$)。$E_0=PB_3/(K^{(n)}N')\twoheadrightarrow PB_3/K^{(d)}=G_d$ は $K^{(n)}N'\subseteq K^{(d)}$ から。∎

> ### 系 REFACT-9L(**$M_2$ への適用**)
> $$M_2=K^{(9)}\cap L=K^{(9)}\cap N_0,\qquad PB_3/M_2\ \cong\ G_9\times H_3\ (\textbf{直積}),\quad \lvert PB_3/M_2\rvert=78{,}732=4\cdot3^9 .$$
> $(K^{(9)},N_0)$ の共通商は自明(補題 D1$^9$)ゆえ **定理 SPLIT-NULL がこの表示で適用でき**、$\mathrm{Im}\,R_{M_2,K^{(9)}}$ は $m$-fiber の合併である。さらに $M_{2,\rm ord}=\mathrm{lcm}(18,3)=18=2\cdot9$ ゆえ (MCOV) は $\mathcal X_9\bmod3\subseteq\mathfrak m(N_0)$ に退化し、$\mathcal X_9\bmod3=\{0,2\}=\mathfrak m(N_0)$(補題 N0)で**成立**。⟹ **$R_{M_2,K^{(9)}}$ は全射。**

> ### 命題 ENT-CRIT(**本質的 entangle 性の判定条件**)
> $M=K^{(n)}\cap N'$ とする。次は同値:
> (a) ある $N''\in\mathrm{NFI}_{PB_3}(B_3)$ で $K^{(n)}\cap N''=M$ かつ $PB_3/M\cong G_n\times PB_3/N''$(= $(K^{(n)},N'')$ が分裂屋根);
> (b) $K^{(n)}/M$ が $PB_3/M$ の中に**$B_3$-安定な正規補群**をもつ。
> (a)(b) が成り立つ屋根では、(SPLIT-NULL の残りの前件が $N''$ について満たされる限り)**像は $m$-fiber の合併**であり、**$\mathfrak F_0$ 方向の検出力はゼロ**である。
> ⟹ **屋根が $\mathfrak F_0$ 方向の検出力をもつための必要条件は「(b) の正規補群が存在しないこと」**(= 本稿でいう**本質的 entangle**)。$E_0\ne1$ は必要条件ですらなく、単に SPLIT-NULL の形式的前件が破れたことを言うだけである。

**証明.** (a)⟹(b): $N''/M$ が補群、$N''\trianglelefteq B_3$ より $B_3$-安定。(b)⟹(a): 補群の $PB_3\to PB_3/M$ による原像を $N''$ とすれば $B_3$-安定性から $N''\trianglelefteq B_3$、$K^{(n)}\cap N''=M$、直積分解を得る。∎
**注意(格)**: SPLIT-NULL の言明は $N''\in I$(isolated)を要求する。$N''$ の isolated 性が未確認なら、結論は「集合水準の像の記述」に留めて群水準の主張($R$ が準同型・$\mathrm{GT}$ が群)は分離すること。$M_2$ の場合は補題 N0 で $N_0$ の isolated 性を紙で得ているのでこの留保は**不要**。

> ### 定理 $M_2$(屋根の完全記述 — 定理 A の $n=3\to9$ 移送)
> $Q:=PB_3/M_2\cong G_9\times H_3$ の下で
> $$\mathrm{GT}(M_2)=\bigl\{[m,(f_9,Z^a)]\ :\ [m,f_9]\in\mathrm{GT}(K^{(9)}),\ a\in\mathbb Z/3\bigr\},\qquad\lvert\mathrm{GT}(M_2)\rvert=3\cdot108=\mathbf{324}.$$
> 全 324 元は settled ⟹ **$M_2$ は isolated**。$R_{M_2,K^{(9)}}$ は**群の全射準同型**で $\ker\cong C_3$、全繊維は一様に 3 個。さらに
> $$\mathrm{GT}(M_2)\ \cong\ \mathrm{GT}(K^{(9)})\times C_3\ \cong\ \bigl(\mathrm{Aff}(\mathbb Z/9)\times C_2\bigr)\times C_3\ =\ \mathrm{Hol}(\mathbb Z/9)\times C_6 .$$

**証明.** 定理 A の (i)–(iv) の証明を、$G_3\to G_9$・$K^{(3)}\to K^{(9)}$・$L_{\rm ord}=6\to M_{2,\rm ord}=18$ と置換して逐語で走らせる。置換が効く点を全部書き出す:
- **$M_{2,\rm ord}$**: $\mathrm{ord}_{G_9}(X)=18$(ODD-H 補題 A(3)・証明書 `N_ord`)、$\mathrm{ord}_{H_3}(X)=3$、$c\mapsto1$ ⟹ $\mathrm{lcm}=18$。$\mathcal X_{M_2}=\mathcal X_9$(12 個)。
- **charming の分解**: $M_{2,\rm ord}=K^{(9)}_{\rm ord}=18$ なので $m$ の単元条件は $K^{(9)}$ 側と同一。$[Q,Q]=[G_9,G_9]\times[H_3,H_3]=A_9\times\langle Z\rangle$(位数 $729\cdot3=2187$)ゆえ $f\mapsto(f_9,Z^a)$、$f_9\in A_9$ は自動。
- **hexagon の分解**: $B_3/M_2\hookrightarrow B_3/K^{(9)}\times B_3/N_0$(核 $M_2$)より成分ごと。$G_9$ 成分 $\iff$ $(m,f_9)$ が $K^{(9)}$ の簡約 hexagon を満たす。$H_3$ 成分は補題 C.1/C.2 が $m$ を **mod 3 でしか見ない**ので $L$ の場合と逐語同一 — $m\not\equiv1\ (3)$ で恒真、charming が $m\equiv1\ (3)$ を排除($3\mid18$)。
- **全射性**: 補題 E の議論($G_9$ 成分は仮定から全射・$H_3$ 成分は $\langle X^u,Y^u\rangle=H_3$)+ 補題 D1$^9$。
- **settled**: $T^{PB_3}_{m,f}=(\beta\times\gamma_u)\circ P_{M_2}$、$\beta\in\mathrm{Aut}(G_9)$ は $K^{(9)}$ の isolated 性(2405 Thm 4.3)から、$\gamma_u\in\mathrm{Aut}(H_3)$ は補題 G から。補題 F((3.32))で settled。
- **繊維・分裂**: $R_{M_2,K^{(9)}}$ は $M_{2,\rm ord}=K^{(9)}_{\rm ord}$ ゆえ (3.60) が第 1 射影に一致。$A:[m,(f_9,Z^a)]\mapsto Z^a$ が準同型であることは (3.53) の $E_{m_1,f_1}$ の $H_3$ 成分が $\gamma_{u_1}$ であること + $\gamma_{u_1}(Z^{a_2})=Z^{a_2u_1^2}=Z^{a_2}$($u_1^2\equiv1\bmod3$)から。$(R,A)$ が単射で位数一致 ⟹ 同型。∎

> **★ 注記(工程上の利得)**: $M_2$ の isolated 性は **$K^{(9)}$ 側(正典 Thm 4.3)・$N_0$ 側(補題 N0)・$M_2$ 本体(上の settled 段)がすべて紙**である。972 屋根が (S4-ISO)「機械測定のみ」に条件づけられていた(`ihnec_v1.md` §6.6)のと対照的に、**$M_2$ は工房初の「両脚とも紙で isolated な屋根」**である。さらに本証明は $M_2$ の settled を直接示すので、**正典 Prop 3.15(証明未掲載・工房の補題 INT で補完)を経由しない**。

> ### 系 GEN9-$\Lambda$(**GEN(9) の狩場の局在**)
> $\Lambda:=\ker\bigl(R_{K^{(9)},K^{(3)}}:\mathrm{GT}(K^{(9)})\to\mathrm{GT}(K^{(3)})\bigr)$ とおく。$\Theta_9$ 座標(追補 C.3)で
> $$\Lambda=\{(k,u,\varepsilon):k\equiv0\ (3),\ u\equiv1\ (3),\ \varepsilon=0\}\cong C_3\times C_3\quad(\lvert\Lambda\rvert=9).$$
> **定理 K3 の下で** $\mathrm{GT}_{\rm gen}(K^{(9)})\cdot\Lambda=\mathrm{GT}(K^{(9)})$、したがって
> $$[\mathrm{GT}(K^{(9)}):\mathrm{GT}_{\rm gen}(K^{(9)})]=[\Lambda:\Lambda\cap\mathrm{GT}_{\rm gen}(K^{(9)})]\in\{1,3,9\}.$$
> すなわち **GEN(9)(= $\mathrm{GT}_{\rm gen}(K^{(9)})=\mathrm{GT}(K^{(9)})$)が破れるとすれば、その破れは $\Lambda\cong C_3\times C_3$ の方向にしかあり得ない**($\lvert\mathrm{GT}_{\rm gen}(K^{(9)})\rvert\in\{108,36,12\}$;12 のときは $\mathrm{GT}_{\rm gen}(K^{(9)})\cong\mathrm{GT}(K^{(3)})$)。

**証明.** 補題 IH-0($d=3\mid n=9$)より $\mathcal{PR}_{K^{(3)}}=R_{K^{(9)},K^{(3)}}\circ\mathcal{PR}_{K^{(9)}}$。$\widehat{GT}_{\rm gen}$ を代入して $\mathrm{GT}_{\rm gen}(K^{(3)})=R(\mathrm{GT}_{\rm gen}(K^{(9)}))$。定理 K3 は $\mathrm{GT}_{\rm arith}(K^{(3)})=\mathrm{GT}(K^{(3)})$ を与えるので (1.A) の挟み撃ちで $\mathrm{GT}_{\rm gen}(K^{(3)})=\mathrm{GT}(K^{(3)})$。ゆえに $R$ の全射性と合わせて $\mathrm{GT}_{\rm gen}(K^{(9)})\Lambda=\mathrm{GT}(K^{(9)})$、第二同型定理で指数の等式。$\Lambda$ の構造は $\Theta_9$ 座標の直接計算($u\equiv1\ (3)$ かつ $k\equiv0\ (3)$ なら $uk\equiv k\ (9)$ ゆえ作用が自明・exponent 3)。∎
**新規性の申告(grep 済)**: 逆向きの含意(細窓 genuine ⟹ 粗窓 genuine)は**補題 GEN-DESC / 系 FIVE-BYPASS**(`ihnec_v1_addendum_e_fivebypass.md`)に既出。本系は**同じ IH-0 の可換性を粗→細の制約として使う**もので、工房内に既出を見つけられなかった。**Sol 監査未。**

---

## 3. 予言(**IF-FIRST**・$\mathrm{GT}(M_2)$ 列挙前に凍結)

| # | 予言 | 根拠 |
|---|---|---|
| **P-R2-1** | **共通商**: $E_0\cong G_3$($\lvert E_0\rvert=108$)・$E\cong B_3/K^{(3)}$($\lvert E\rvert=648$)。$(K^{(9)},L)$ は SPLIT-NULL の前件を**満たさない** | 命題 E |
| **P-R2-2** | **再表示**: $M_2=K^{(9)}\cap N_0$、$PB_3/M_2\cong G_9\times H_3$(**部分直積の真部分群ではなく全直積**)、$\lvert PB_3/M_2\rvert=\mathbf{78{,}732}=4\cdot3^9$、$[B_3{:}M_2]=\mathbf{472{,}392}$、$F_2/M_{2,F_2}\cong PB_3/M_2$($c\in M_2$) | 系 REFACT-9L |
| **P-R2-3** | $M_{2,\rm ord}=\mathbf{18}$、$\mathcal X_{M_2}=\mathcal X_9=\{0,2,3,5,6,8,9,11,12,14,15,17\}$(12 個)、$\lvert[Q,Q]\rvert=2187$、**raw 候補 $=12\times2187=26{,}244$** | 定理 $M_2$ |
| **P-R2-4** | $\lvert\mathrm{GT}(M_2)\rvert=\mathbf{324}$。$\mathfrak F_0(M_2)\cong C_9\times C_3$(位数 27)・$\widetilde\chi$ 像 $=(\mathbb Z/36)^\times$(位数 12)・$27\cdot12=324$(**4 通りの数え方で一致**) | 定理 $M_2$ |
| **P-R2-5** | $\mathrm{GT}(M_2)\cong\mathrm{GT}(K^{(9)})\times C_3\cong\mathrm{Hol}(\mathbb Z/9)\times C_6$。**位数分布** $\{1{:}1,\ 2{:}19,\ 3{:}26,\ 6{:}170,\ 9{:}54,\ 18{:}54\}$(和 324) | 定理 $M_2$(iv)+追補 C.3 の $\mathrm{GT}(K^{(9)})$ 分布 |
| **P-R2-6** ★ | $\mathrm{Im}\,R_{M_2,K^{(9)}}=\mathrm{GT}(K^{(9)})$ 全体(**108/108・全射・$d=1$**)⟹ **この屋根は fake を検出しない** | 系 REFACT-9L(SPLIT-NULL + (MCOV)) |
| **P-R2-7** | $\mathrm{Im}\,R_{M_2,L}=\mathrm{GT}(L)$ 全体(**36/36・全射**)、$\ker R_{M_2,L}\cong\Lambda\cong C_3\times C_3$(位数 9)、繊維一様 9 | 定理 $M_2$ + $R_{K^{(9)},K^{(3)}}$ 全射(証明書 K9)|
| **P-R2-8** ★ | **合成像**(トリップワイヤ本体): $\mathrm{Im}\,R_{M_2,K^{(3)}}=\mathrm{GT}(K^{(3)})$ 全体(**12/12**)。これは **P-FV-1 の第 8 プローブ**(`fake_void_v1.md` §4.2) | 定理 K3 + 系 FV-SUB(⟹ 予言であって独立証拠ではない) |
| **P-R2-9** | 全 324 shadow が **settled**(fail 0)⟹ $M_2$ は isolated。$\mathrm{GT}(M_2)$ は位数 324 の有限群 | 定理 $M_2$(ii) |
| **P-R2-10** | **アンカー**: 同一判定関数が $K^{(9)}$ 単体 $=108$・$L$ 単体 $=36$・$N_0$ 単体 $=6$・972 屋根の $m=0$ シャード $=81$ を再現 | 証明書 K9/L01 + 補題 N0 + 裁定 385/387 |
| **P-R2-11** | **負の設計判定**: $M_2$ は $\mathfrak F_0$ 方向の検出力を持たない ⟹ **GEN(9) への実弾ではない**。札 D の「初実弾」評価は本稿で**取り下げ**(修理仕様は §7) | 命題 ENT-CRIT + 系 REFACT-9L |

> ⚠ **P-R2-5 の抽象型は $\mathrm{GT}(K^{(9)})\cong\mathrm{Hol}(\mathbb Z/9)\times C_2$(追補 C.3・U-11)に依存する。U-11 の格は「有限 exhaustive candidate / single lane」(追補 D.4)であって cross-checked ではない。**⟹ P-R2-5 は「予言」であって主張ではない。**位数分布は `IdGroup` ラベルの代用**として置く(GAP で `IdGroup` を測るなら別欄・追補 C.3 の ⚠ 枠の規律に従う)。

---

## 4. $d$ の候補値とトリップワイヤ(委嘱 §2 の主題)

$d:=[\mathrm{GT}(K^{(9)}):\mathrm{Im}\,R_{M_2,K^{(9)}}]=108/\lvert\mathrm{Im}\rvert$ とおく。**3 つの独立な守り**がかかる。

| 守り | 何を強制するか | 出所 | 格 |
|---|---|---|---|
| **(G1) 定理 K3 + 系 FV-SUB** | $\mathrm{Im}\cdot\Lambda=\mathrm{GT}(K^{(9)})$、すなわち **$d\mid9$**($d\in\{1,3,9\}$) | `week4-K3飽和_opus_v3.md` §2.4・W3-11 | paper-proof / 両数学者監査 PASS / **framework-conditional**((K1)–(K4)) |
| **(G2) SPLIT-NULL(REFACT 経由)** | 像は $m$-fiber の合併 ⟹ $\lvert\mathrm{Im}\rvert=9\cdot\#\{m\}$、$\#\{m\}\in\{0,6,12\}$($\mathfrak m(N_0)\subseteq\{0,2\}$)⟹ **$d\in\{1,2\}$** | 定理 SPLIT-NULL(便 98 PASS)+ 定理 REFACT(本稿) | paper-proof(本稿部分は Sol 監査未) |
| **(G3) (MCOV)** | $\mathfrak m(N_0)=\{0,2\}$ ⟹ **$d=1$** | 補題 N0(本稿) | paper-proof(Sol 監査未) |

**(G1)∧(G2) の共通解は $d=1$ のみ**(検算 §8 で機械確認)。したがって:

| 実測値 | 何が倒れるか(読み方) |
|---|---|
| **$d=1$**(108/108) | **予言どおり**。何も新しい数学は出ない(較正 + 定理 REFACT の実証) |
| **$d=2$**(54/108) | ★ **定理 K3 が倒れる**($2\nmid9$ ⟹ $K^{(3)}$ 水準で像が落ちる ⟹ 系 FV-SUB の対偶)。同時に補題 N0 の $\mathfrak m(N_0)=\{0,2\}$ も倒れる。**(G2) が許す唯一の非自明値**がこれ = 実際のトリップワイヤはここ |
| **$d=3$ または $9$** | **定理 REFACT / SPLIT-NULL / 補題 D1$^9$ のどれかが倒れる**。**定理 K3 は無傷**。⟹ この場合は $\Lambda$ 方向の落下 = **$n=9$ の初の $\mathfrak F_0$ 方向 fake witness**(GEN(9) 破れ)であり、研究上の大当たり |
| **$d\in\{4,6,12,\dots\}$** | K3 と SPLIT-NULL の**両方**が倒れる(実装バグを最初に疑う) |
| $\mathrm{GT}(M_2)=\emptyset$ または $\lvert\mathrm{GT}(M_2)\rvert\ne324$ | 定理 $M_2$ が倒れる(charming 集合・向き規約・群構成のいずれか) |

> ### ★ 委嘱文の「$d=3$ 方向は定理 K3 が保護」の**訂正**
> 正確には**逆**である。$\Lambda=\ker(\mathrm{GT}(K^{(9)})\to\mathrm{GT}(K^{(3)}))$ は $K^{(3)}$ 水準から**見えない**方向であり、**定理 K3 の射程外**である。K3 が禁じるのは「$9$ を割らない $d$」であって、$d\in\{3,9\}$ は K3 と両立する。
> さらに **$d$ の値そのものはトリップワイヤにならない**: $d=3$ は「$\Lambda$ 内部の落下(K3 無傷)」と「$K^{(3)}$ 水準の落下(K3 崩壊)」の**両方と両立する**($[\,\mathrm{GT}(K^{(9)}):\mathrm{Im}\Lambda\,]$ が 1 か 3 かで分かれる)。
> ⟹ **トリップワイヤの本体は合成像 $\mathrm{Im}\,R_{M_2,K^{(3)}}$(P-R2-8)である。実測はこれを $d$ とは別欄で必ず報告すること**(§5 の R5b を必須欄にした理由)。
> **そして系 GEN9-$\Lambda$ が言うとおり、$\Lambda\cong C_3\times C_3$ こそが GEN(9) の唯一の狩場である** — K3 が既に他を全部守っている。

---

## 5. 実測工程(**設計のみ** — 実装は implementer へ)

### 5.0 位置づけと前提

- **R4b 様式の再利用**: 単一判定関数 `ScanRoofHexagon(qrec, charmingSet)`(`search/probe/wac_v1/ihnec_r4b_run.g` L77–L116・SHA-256 `5bf6bc551eb7309c0b83adc363c15985973d9cb04e2cde9e7e34fe45c5277aa2`)を**逐語再利用**する(改造禁止・CV-13 の精神 = 生成・受理・生成条件が同一関数を通る)。
- **証明書非読**: driver は `certificates/*.json` を**一切読まない**(R4a/本稿の紙との独立性を維持)。期待値は driver 内のリテラル定数として hard assert する。
- **規模**: raw 候補 26,244(972 屋根 R4b の 4,408,992 の **1/168**)。群位数 78,732。⟹ **シャード不要・1 実行**(600 秒 cap に対し大幅な余裕)。**シャードしないという設計判断を plan に事前登録すること**(R4b の逆で、ここは分割の方が高くつく)。
- **RAM**: $\lvert Q\rvert=78{,}732$ の置換表現(点数は $G_9$ 側の `MakeGn(9)` の点数 + 27)。`Elements(DerivedSubgroup(Q))` が 2187 元 ⟹ 8GB 制約に対して無害。

### 5.1 作業段

| 段 | 内容 | 出力 | 予言 | fail-closed assert |
|---|---|---|---|---|
| **R2-0** | $G_9:=$ `MakeGn(9)`(`search/week3-battery-common.g`)、$H_3:=$ `week3-L-explorer.g` の座標規約による位数 27 群($X=(1,0,0)$、$Y=(0,1,0)$、正則表現 27 点)。$Q:=G_9\times H_3$、$x_Q:=(X_9,X)$、$y_Q:=(Y_9,Y)$ | 生成対 | — | `Size(G9)=2916`・`Size(H3)=27`・$H_3$ fixture($X^3=Y^3=(XY)^3=1$・$Z=[X,Y]$ 中心・位数 3・$\lvert[H_3,H_3]\rvert=3$)・`Size(Q)=78732`・`Size(DerivedSubgroup(Q))=2187` |
| **R2-1** | $M_{2,\rm ord}:=\mathrm{lcm}(\mathrm{ord}(x_Q),\mathrm{ord}(y_Q))$、`CharmingSetOf` | 18・12 元 | P-R2-2/3 | $=18$、charming set $=\mathcal X_9$ のリテラル |
| **R2-2**(アンカー A1) | `ScanRoofHexagon` を **$K^{(9)}$ 単体**に適用 | 108 | P-R2-10 | $=108$ でなければ **中止** |
| **R2-3**(アンカー A2) | 同関数を **$L$ 単体**($Q_L=G_3\times H_3$・`MakeGn(3)`)に適用 | 36 | P-R2-10 | $=36$ でなければ中止。**外部 anchor**(L01 cert の独立再現) |
| **R2-4**(アンカー A3) | 同関数を **$N_0$ 単体**($H_3$)に適用し、**6 元の集合を全部書き出す** | 6 | P-R2-10・補題 N0 | 個数 $=6$ **かつ** 集合が $\{(m,Z^a):m\in\{0,2\},a\in\mathbb Z/3\}$ と**集合等号**。⟹ CV-13 が要求する「独立 source-map route」(紙の予言との集合等号)を**ここで満たす** |
| **R2-5**(アンカー A4) | 既存 R4b driver を**無改変**で $m=0$ シャードだけ再走(972 屋根の再現) | 81 | P-R2-10 | $=81$ でなければ中止(向き規約の経時変化の検出) |
| **R2-6**(主計算) | `ScanRoofHexagon(qrec_M2, charming)` | 324・shadow 一覧 | P-R2-4 | `candidate_total=26244`・`shadow_total=324` |
| **R2-7** | 各 shadow の $\widetilde\chi=2m+1\bmod36$ の像と $\mathfrak F_0$ の位数 | 12・27 | P-R2-4 | $12\cdot27=324$ |
| **R2-8** | **settled**: 各 shadow で $x_Q\mapsto x_Q^u$、$y_Q\mapsto f^{-1}y_Q^uf$ が $\mathrm{Aut}(Q)$ に延びるか(`GroupHomomorphismByImages` + `IsBijective`) | 324/324 | P-R2-9 | fail 0。**「真の settled」**(核 $=M_2$)であって壁 judge の well-definedness ではない(`ihnec_v1.md` §6.6 注意 2) |
| **R2-9** | $\mathrm{Im}\,R_{M_2,K^{(9)}}$ = shadow の第 1 射影 $(m,f_9)$ の相異個数 | **108** | ★P-R2-6 | 個数と $d=108/\lvert\mathrm{Im}\rvert$ を**別欄で報告** |
| **R2-10** | $\mathrm{Im}\,R_{M_2,L}$: $(m\bmod6,(\rho(f_9),Z^a))$、$\rho:G_9\twoheadrightarrow G_3$ は `GroupHomomorphismByImages(G9,G3,[X9,Y9],[X3,Y3])` | **36** | P-R2-7 | $\rho\ne$ `fail`・全射・$\lvert\ker\rho\rvert=27$ |
| **R2-11**(★必須欄) | **合成像** $\mathrm{Im}\,R_{M_2,K^{(3)}}$: $(m\bmod6,\rho(f_9))$ の相異個数 | **12** | ★P-R2-8 | **12 未満なら定理 K3 が倒れる — 実行を中止して司令塔へ即報**(P-FV-1 発火) |
| **R2-12** | $\mathrm{GT}(M_2)$ の位数分布(合成表 (3.53) を組む場合のみ・任意段) | P-R2-5 の分布 | P-R2-5 | 和 $=324$。`IdGroup` を測るなら別欄・ラベルの由来を明記 |

### 5.2 証明書スキーマ(`gtsh-cert/v1` 互換 + 本件の追加欄)

```
target.id            = "M2"            target.family = "general"
target.construction  = { g9: "MakeGn(9)", h3: "(a,b,e) coords, X=(1,0,0), Y=(0,1,0)", note: "M2 = K^(9) cap N0 = K^(9) cap L" }
invariants           = { index_PB3: 78732, index_B3: 472392, N_ord: 18, derived_order: 2187 }
counts               = { raw_candidates, hexagon_pass, charming_pass, surjective_pass, settled_fail }
anchors              = { k9_alone: 108, l_alone: 36, n0_alone: 6, n0_set_equality: true, roof972_m0_shard: 81 }
reduction            = [ {to:"K9", image_size, surjective, d}, {to:"L", image_size, surjective},
                         {to:"K3", image_size, surjective}   # ← ★ トリップワイヤ欄・必須
                       ]
provenance           = { script_sha256, gap_version, plan_frozen_sha, predictions_frozen: "docs/notes/roof2_cv9_freeze_v1.md", predictions_sha256 }
scope                = { isolated_K9: "canon Thm 4.3", isolated_N0: "paper (補題 N0, Sol 監査未)",
                         isolated_M2: "paper (定理 M2(ii), Sol 監査未)", lane: "GAP single lane" }
```

### 5.3 CV-9(仕様同一性判読)への申し送り

- **二系統になるのは何か**: 本工程は **GAP 単系統**である。第 2 系統は「紙(定理 $M_2$)」であって実装ではない ⟹ **cross-checked を請求しない**。請求するのは「**予言先行の的中**」までである。
- 二系統化したい場合の設計: R4a と同じく **証明書 K9 + 補題 N0 の紙記述から python で組み立てる独立実装**を作る(列挙は GAP 単系統のまま)。**その場合も追補 C.1 と同じ格の申告**(列挙は単系統・組立のみ第 2 実装)を書くこと。
- **competitor universe**(CV-9-5): 主張「$\lvert\mathrm{GT}(M_2)\rvert=324$」は raw 26,244 のうち 324 を当てる主張(偶然一致率 $324/26244\approx1/81$)。「$d=1$」は $\mathrm{GT}(K^{(9)})$ の部分群 108 個中の 1 つを当てる主張。
- **識別力のある dummy fixture**(CV-9-5): $m=1$($\notin\mathcal X_9$)を charming set に混ぜた走行で `charming_pass` が増えないこと、および $H_3$ 成分を $Z^a$ でなく一般の $f_H\in H_3$ に開いた走行で `hexagon_pass` が **324 のままである**こと(補題 C の空虚性は $f_H\in\langle Z\rangle$ を仮定していない — charming がそれを強制している)。後者は**紙の予言と食い違えば紙が誤り**という識別力を持つ。

---

## 6. 格の正直申告(委嘱 §4)

### 6.1 $L$ の isolated 性 — **機械測定のみではない**

| 主張 | 格 | 出所 |
|---|---|---|
| $L$ は isolated(全 36 shadow が settled) | ★ **紙上証明 + 相互監査 PASS** | `docs/命題_中心持ち上げ_v2.md` 定理 A(ii)。証明は**補題 F**((3.32) の逐語・p.12 ページ画像照合済)+ **補題 G**(verbal 部分群の多様体論法)による。Sol 便 05 で相互監査 PASS、**W23(transversal 降下の互換性)は Sol が自己撤回** |
| 同上・機械側 | **cross-checked**(3 実装一致) | GAP `L01.v1.json` + node 照合器 `L01.v1.verdict.json` + 数学者の第 3 独立実装(§6 の 36/36 settled) |
| $N_0$ は isolated | **paper-proof candidate(Sol 監査未)** | 本稿 補題 N0(定理 A(ii) の逐語移送) |
| $M_2$ は isolated | **paper-proof candidate(Sol 監査未)** | 本稿 定理 $M_2$(ii)。**Prop 3.15 / 補題 INT を経由しない直接証明** |
| $K^{(9)}$ は isolated | **正典の定理** | 2405 Thm 4.3 |

> **★ 記帳の食い違いを 1 件申告する**: `docs/notes/kerchi_equality_v2.md` の註 2 / R-4b は「$L,M_5,N_Q,\dots$ の isolated 性は**未確認**」と書いており、これは同稿の射程内では正しい(同稿は $L$ の isolated 性を使わずに $\widetilde\chi$ 全射を実測証明書として扱う設計)。しかし **`命題_中心持ち上げ_v2.md` 定理 A(ii) は 2026-07-25 に $L$ の isolated 性を紙で証明し Sol 監査 PASS を得ている**。⟹ **kerchi 側の「未確認」を「$L$ については紙上証明あり(中心持ち上げ 定理 A(ii))・他の 8 窓は未確認」へ修文する必要がある**。本稿は kerchi を改訂しない(versioned 規律)。**司令塔裁定を要請する。**
> なお $\widetilde\chi$ 全射性の格は**この修文で自動的には上がらない** — T-A(4′) は isolated **かつ (AR)** を要求し、(AR) は framework-conditional だからである。**$L$ の $Q_L=(\mathbb Z/12)^\times$ は実測証明書のまま**でよい。

### 6.2 本稿全体にかかる留保

- 定理 REFACT・命題 ENT-CRIT・補題 N0・定理 $M_2$・系 GEN9-$\Lambda$ は **すべて Sol 監査未**(paper-proof candidate)。
- 定理 SPLIT-NULL(便 98 PASS)と (MCOV)(P98-3.1 逐語採用)は既に監査済だが、**それを $N''=N_0$ に適用してよい**という一段(= 定理 REFACT)が本稿の新規段であり、そこが監査対象である。
- **定理 K3 は framework-conditional**((K1)–(K4)+(TB1)(TB2)(TB3)(TB4$^{\rm u}$)+(CAL))。§4 の (G1) はこの条件つきの守りである。
- 予言 P-R2-1〜11 は **prediction(未測定)**。検算 `roof2_check.py` は **単系統の cross-check** であって証明ではない。

---

## 7. 【IHNEC-GAP-5・新設】entangled 屋根レシピの修理

### 7.1 何が要るか(命題 ENT-CRIT の言い換え)

$\mathfrak F_0$ 方向の検出力をもつ屋根 $M=K^{(n)}\cap N'$ を作るには、
$$1\to B_0\to PB_3/M\to G_n\to1\qquad(B_0:=K^{(n)}/M)$$
が **$B_3$-安定な正規補群をもたない**ようにする必要がある。この拡大は $1\to B_0\to PB_3/N'\to E_0\to1$ の $G_n\twoheadrightarrow E_0$ に沿った引き戻しである。

### 7.2 ★ 最安の候補は**原理的に不可能**(負の補題)

> ### 補題 NO-CENTRAL
> 奇 $n\ge3$ に対し $H^2(G_n,\mathbb Z/3)=0$(自明係数)。すなわち **$G_n$ の中心 $C_3$-拡大はすべて分裂する**。

**証明.** $G_n=A\rtimes Q$、$A=\langle r\rangle^3\cong(\mathbb Z/n)^3$、$Q\cong C_2^2$(補題 D0$^n$)。$\lvert Q\rvert=4$ は 3 と互いに素なので LHS スペクトル系列は $H^2(G_n,\mathbb Z/3)=H^2(A,\mathbb Z/3)^Q$ に退化する。$H^2(A,\mathbb Z/3)\cong\Lambda^2(A^*\otimes\mathbb F_3)\ \oplus\ (A^*\otimes\mathbb F_3)$(交換子対から来る部分と Bockstein 部分)。補題 D0$^n$ の作用表から $A\otimes\mathbb F_3$ は $Q$ の**相異なる 3 つの非自明指標** $\chi_1,\chi_2,\chi_3$($\chi_1=(+,-)$、$\chi_2=(-,+)$、$\chi_3=(-,-)$ を $(a,b)$ で表示)の和であり、$\mathbb F_3$ 上 $\chi_i^*=\chi_i$。したがって Bockstein 部の $Q$-不変部分は $0$、$\Lambda^2$ 部は $\chi_i\chi_j$($i<j$)= 再び $\{\chi_1,\chi_2,\chi_3\}$ の置換で、いずれも非自明ゆえ不変部分は $0$。∎(指標の計算は検算 §7 で機械確認)

⟹ **「$G_n$ の上に中心 $C_3$ を載せた窓」は存在しない。$L$ を Heisenberg 中心 $Z\cong C_3$ で拡張する方向(= 中心持ち上げ補題の方向)では、entangled 屋根は絶対に作れない。**これが $M_2$ が分裂してしまう根本原因である。

### 7.3 唯一残る型(**修理仕様**)

$B_0=C_3$ に **$Q$ が非自明な指標 $\chi_i$ で作用する**($B_0$ が $PB_3/M$ の中で中心でない)場合は
$$H^2(G_n,\chi_i)\ \cong\ \bigl(H^2(A,\mathbb F_3)\otimes\chi_i\bigr)^Q\ \ne\ 0$$
(Bockstein 部から 1 次元・$\Lambda^2$ 部から 1 次元 ⟹ $\dim=2$)。ゆえに**非分裂拡大は存在する**。さらに $n=9$ では inflation が生き残るかを次で判定できる:

> ### 補題 INF(**$G_3$ の非分裂性は $G_9$ へ引き上がるか**)
> $W:=\ker(G_9\twoheadrightarrow G_3)=3A_9\cong(\mathbb Z/3)^3$ とする。$1\to W\to G_9\to G_3\to1$ の 5 項完全列
> $$0\to H^1(G_3,\chi_i)\xrightarrow{\ \mathrm{inf}\ }H^1(G_9,\chi_i)\xrightarrow{\ \mathrm{res}\ }H^1(W,\chi_i)^{G_3}\xrightarrow{\ \mathrm{tg}\ }H^2(G_3,\chi_i)\xrightarrow{\ \mathrm{inf}\ }H^2(G_9,\chi_i)$$
> において $\dim H^2(G_3,\chi_i)=2$、$\dim\ker(\mathrm{inf})=1$。ゆえに **inflation の像はちょうど 1 次元**であり、**$G_3$ 上の非分裂 $\chi_i$-拡大のうちある類は $G_9$ へ引き上げても非分裂**である。

**証明.** すべて $\lvert Q\rvert=4$ の可逆性による退化 $H^*(G,\ -)=H^*(A,\ -)^Q$ を使う($A$ は $\chi_i$ に自明に作用する)。
- $H^1(G_d,\chi_i)=(\mathrm{Hom}(A_d,\mathbb F_3)\otimes\chi_i)^Q$。$\mathrm{Hom}(A_9,\mathbb F_3)=\mathrm{Hom}(A_9/3A_9,\mathbb F_3)=\mathrm{Hom}(A_3,\mathbb F_3)$ なので **inflation $H^1(G_3,\chi_i)\to H^1(G_9,\chi_i)$ は同型**(ともに $\dim=1$ = $\chi_i$ の重複度)。
- ゆえに完全性から $\mathrm{res}=0$、したがって $\mathrm{tg}$ は単射で $\ker(\mathrm{inf})\cong H^1(W,\chi_i)^{G_3}=(\mathrm{Hom}(W,\mathbb F_3)\otimes\chi_i)^Q$。$W\cong\chi_1\oplus\chi_2\oplus\chi_3$ より $\dim=1$。
- $\dim H^2(G_3,\chi_i)=(H^2(A_3,\mathbb F_3)\otimes\chi_i)^Q$ の次元 $=$ $H^2(A_3,\mathbb F_3)$ 内の $\chi_i$ の重複度 $=1$(Bockstein 部 $y_i$)$+1$($\Lambda^2$ 部 $x_jx_k$、$\{j,k\}=\{1,2,3\}\setminus\{i\}$、$\chi_j\chi_k=\chi_i$)$=2$。∎

> **注意(自明係数との整合)**: 係数が自明 $\mathbb F_3$ のときは $H^2(G_3,\mathbb F_3)=0$(補題 NO-CENTRAL)で両側 0 になり、上の議論は空虚に成立する。**非自明指標に移して初めて $H^2$ が立ち上がる**のがこの節の要点である。
> **⚠ 起草時の誤りの申告**: 本補題の初稿は「$G^{\rm ab}=C_2^2$ ゆえ $H^1(G,\chi)=0$」と書いていたが、これは**自明係数でしか正しくない**($\chi_i$ 係数では $\dim H^1=1$)。結論($\mathrm{im}(\mathrm{inf})\ne0$)は変わらないが、根拠は上のとおり **$H^1$ の inflation が同型であること**に置き換えた。

### 7.4 実装可能な標的(次波の起票候補)

> **標的 ENT-1**: $N'\trianglelefteq B_3$、$N'\subseteq K^{(3)}$、$[K^{(3)}{:}N']=3$、$PB_3/N'$ が $G_3$ の**非分裂 $\chi_i$-拡大**(位数 324)であるものを探す。見つかれば
> $$M_{\rm ENT}:=K^{(9)}\cap N',\qquad \lvert PB_3/M_{\rm ENT}\rvert=2916\cdot324/108=8748=4\cdot3^7$$
> が**工房初の本質的 entangled 屋根**になる(補題 INF が保証する類を選べば)。走査規模は $M_2$ と同程度(数万候補)。
> **探索手段**: `lins`(low index normal subgroups・同梱パッケージ)で $B_3$ の指数 $6\cdot324=1944$ の正規部分群を列挙し、$K^{(3)}$ に含まれるものに絞る。**あるいは** `hap` / `cohomolo` で $H^2(G_3,\chi_i)$ の 2 次元を明示し、各類の拡大が $F_2$ の 2 生成商として実現するか + $B_3$-安定($\theta,\tau$ 同変)かを判定する。
> **前提の弱点(正直に)**: **$B_3$-安定性($S_3$ 同変性)が追加の制約であり、これが 2 次元の $H^2$ をどこまで削るかは UNKNOWN**。削り切って 0 になる可能性は排除できていない。⟹ **これは「存在する」の主張ではなく「ここを見よ」の設計である。**

> ### 【文献要請 ROOF2-L1】
> **困難**: 有限群 $G$ とその正規部分群による商 $\bar G$、および外側の有限群作用 $\Gamma=S_3$(本件では $B_3/PB_3$)が与えられたとき、**$\Gamma$-同変な非分裂拡大類の存在**($H^2(\bar G,M)^\Gamma\ne0$ かつ対応する拡大が $\Gamma$-同変に実現)を判定・構成する機構が欲しい。とくに **$\bar G=A\rtimes Q$($A$ が $p$ 群・$Q$ が $p'$ 群・$A$ が $Q$ の相異なる非自明指標の和)という非常に特殊な形**で、$\Gamma$ が $A,Q$ の両方を動かす場合。
> **欲しい結果の型**: 「$\Gamma$-同変 Schur 乗数」あるいは「equivariant central/abelian extension の障害理論」の**計算可能な形**(具体的には $H^2_\Gamma$ の inflation-restriction 版、または $\Gamma$-同変な covering group の存在定理)。$B_3$ の braid 群としての構造(自由群の $\mathrm{Out}$ 作用)に翻訳できる形が望ましい。
> **既に持っているもの**: `lins` による総当たり列挙(有限だが指数 1944 は重い可能性)。**総当たりで済むなら文献は不要** — 判断は司令塔へ委ねる。

---

## 8. 出所・新規性の申告(grep 済)

### 8.1 出所

| 使ったもの | 出所 |
|---|---|
| 定理 A(中心持ち上げ)・補題 B/C/D0/D/E/F/G | `docs/命題_中心持ち上げ_v2.md`(紙上証明 + Sol 便 05 相互監査 PASS) |
| 定理 SPLIT-NULL・(MCOV)・命題 ROOF・方法 CMP・系 ML-A/D | `docs/notes/ihnec_v1.md` §6 + 追補 D(便 98 PASS・裁定 388/389) |
| 補題 IH-0(奇 $d\mid n$ の可換性) | 同 §2 |
| $\mathrm{GT}(K^{(9)})\cong\mathrm{Hol}(\mathbb Z/9)\times C_2$・$\Theta_9$ 座標・位数分布 | 同 追補 C.3(**有限 exhaustive candidate / single lane**) |
| 定理 K3・系 FV-SUB・P-FV-1 | `docs/week4-K3飽和_opus_v3.md` §2.4・`docs/notes/fake_void_v1.md` §1.5/§4.2 |
| $K^{(n)}$ の isolated 性・Thm 4.3・Thm 4.4 | 正典 2405.11725 |
| (3.32)/(3.59)/(3.60)/Def 3.7/Def 3.13/Prop 3.4/Prop 3.6/Prop 3.12 | 正典 2401.06870(定義ノート経由) |
| $N_0,V,H_3$ の構成と座標規約 | `docs/week3-L設計.md` §1 |
| `ScanRoofHexagon` | `search/probe/wac_v1/ihnec_r4b_run.g`(裁定 385/387) |

### 8.2 新規性(**本稿が初めて書いたと判断するもの**・いずれも Sol 監査未)

1. **補題 N0**($N_0$ 単体の完全記述と isolated 性)— repo 内に $N_0$ 単体の GT を書いた文書は見つからなかった($L$ の記述はあるが $N_0$ は「$L$ の材料」としてしか現れない)。
2. **命題 E**($K^{(9)}L=K^{(3)}$ による共通商の明示同定)。
3. **定理 REFACT**(屋根の再表示 — 「$E_0\ne1$ は検出力を意味しない」)。**これが本稿の主結果**であり、札 D の含意を訂正する。
4. **命題 ENT-CRIT**(本質的 entangle 性 = $B_3$-安定正規補群の非存在)。
5. **定理 $M_2$**(定理 A の $n=9$ 移送)— 移送自体は機械的だが、$M_2$ という対象を書いた文書は repo に無い。
6. **系 GEN9-$\Lambda$**(K3 の下で GEN(9) の破れは $\Lambda\cong C_3^2$ に局在)。逆向き(FIVE-BYPASS)は既出、この向きは見つからず。
7. **補題 NO-CENTRAL / 補題 INF**($H^2(G_n,\mathbb Z/3)=0$ と $\chi_i$ 係数での非消滅・inflation の非退化)。
8. **既出であることの明示**: 「entangled 屋根が要る」という**問題設定自体**は系 SPLIT-NULL″(裁定 374)+ 追補 D.1.5 +【IHNEC-GAP-2】の再定義が既に置いている。本稿はその**レシピの型を訂正した**のであって問題を発見したのではない。トリップワイヤ(P-R2-8)も **P-FV-1 の第 8 プローブ**であって新しい機構ではない。

### 8.3 検算

`scratchpad/roof2_check.py`(SHA-256 `62de27427e78afe4e2259d6d7fa8545f6ecf1e4ab126322ec7c863be47677cc2`)。
①証明書 3 本からの一次事実 ②$L\subseteq K^{(3)}$ の証明書側確認(reduction 欄・繊維一様 3)③$R_{K^{(9)},K^{(3)}}$ 全射・繊維一様 9 ④charming 集合と (MCOV) の前件 ⑤$\lvert PB_3/M_2\rvert$ の二表示一致と $\lvert\mathrm{GT}(M_2)\rvert$ の 4 通り一致 ⑥走査規模 ⑦$Q$ の 3 指標と $\Lambda^2$・Bockstein の不変部分 $=0$(補題 NO-CENTRAL の機械側)⑧$\Lambda$ が $C_3\times C_3$ で $(G1)\wedge(G2)\Rightarrow d=1$ ⑨$\mathrm{GT}(M_2)$ の位数分布の予言。**failures 0 / ALL PASS。cross-check であって証明ではない。**
