# E-5(divisor orientation)の解釈ノート v1 — spec v18 の凍結を変えない読解

2026-07-28 起草: Claude(数学者レイヤー・Opus 5)。**状態 = candidate。** 実装 lane A からの裁定要請への回答。
**本稿は spec の改版ではない。** `mb/ninfty-stage2-predicate/v18` の本文は 1 バイトも変えず、**凍結条項 E-5 をどう読むか**だけを定める。
**lane の実装内容には触れていない**(相互不可視の維持)。扱うのは仕様解釈と紙上の数学のみ。

---

## 0. 結論(先に 5 行)

1. **E-5 は外部入力ではなく、E-1〜E-4 からの定理である。** $(a,p,f_6)$ の純代数だけで機械検証できる。
2. 検証手続きは **4 つの多項式検査**に尽きる(§2.3)。追加の幾何計算も S5 の参照も要らない。
3. ゆえに **`orientation_declared_ok` の宣言フラグ化は「凍結仕様と矛盾しない」が、必要以上に強い** — 未宣言 candidate を [6] で落とすと **accepted universe を狭める**(便 72 F13.3 の FAIL 類型)。**導出実装への移行を推奨**し、フラグは任意の cross-check に降格するのが最小修理(§3)。
4. `external_dependencies` の `S5/prop-S5-1` は **出所の束縛**であって検証の oracle ではない。EP では「S5-1 と独立導出が一致すること」を照合すればよい(§3.3)。
5. **[7](triple-root)候補は実在し、閉形で書ける。** 二枝あり、**枝 I の整数最小高さは 12** — `|係数| ≤ 7` の箱はこれを含まない。それが「見つからなかった」理由である(§4)。

---

## 1. 記法(spec v18 §1.1 の再掲・変更なし)

$$ C_{\rm crv}:\ y^2=f_6(x),\quad \deg f_6=6,\ f_6\ \text{monic squarefree};\qquad \mu=a(x)+p(x)\,y,\ \deg a=5,\ \deg p=2,\ a_5=p_2\ne0 $$
$$ \textbf{(Pell)}\ a^2-f_6p^2=C\in\mathbb Q^\times,\qquad \textbf{(Or)} = \textbf{E-5}:\ (\mu)=5P_0-5P_\infty $$
$\iota$ = 超楕円対合、$\mu^\iota = a-py$。$k=\bar{\mathbb Q}$。

$\deg f_6=6$ かつ $f_6$ monic(先頭係数 $1$ = 平方数)なので、**無限遠に 2 点** $\infty_+,\infty_-$ があり $\iota$ がそれらを入れ替える。局所助変数は $t=1/x$ で $\operatorname{ord}_{\infty_\pm}(x)=-1$、$\operatorname{ord}_{\infty_\pm}(y)=-3$。**$\infty_\pm$ の名付け**は $y/x^3\to\pm1$ で決める。

---

## 2. E-5 は E-1〜E-4 の帰結である

### 2.1 命題

> **命題 E5-D.** E-1(f₆ monic squarefree・deg 6)・E-2(deg a=5・deg p=2)・E-3($a_5=p_2\ne0$)・E-4(Pell・$C\ne0$)を仮定する。標数 0 とする。このとき
> $$ \boxed{\ \operatorname{div}(\mu)=5(\infty_-)-5(\infty_+)\ } $$
> が成り立つ。すなわち **E-5 は自動的に成立**し、しかも **$P_0=\infty_-$・$P_\infty=\infty_+$ と向きまで決まる。**

### 2.2 証明

**(1) $\mu$ はアフィン部分で正則。** $\mu=a+py$ は $x,y$ の多項式であり、$f_6$ squarefree だからアフィン曲線は滑らか。ゆえに $\mu$ はアフィン部分に極を持たない。同じ理由で $\mu^\iota=a-py$ も正則。

**(2) $\mu$ はアフィン部分に零点を持たない。** (Pell) は $\mu\,\mu^\iota=a^2-f_6p^2=C$ と書ける。$C\in\mathbb Q^\times$ は非零定数だから $\operatorname{div}(\mu)+\operatorname{div}(\mu^\iota)=0$。もしアフィン点 $Q$ で $\mu(Q)=0$ なら $\operatorname{ord}_Q(\mu^\iota)=-\operatorname{ord}_Q(\mu)<0$ となり (1) に矛盾。

**(3) よって $\operatorname{div}(\mu)$ は $\{\infty_+,\infty_-\}$ に台を持つ。** 次数 0 なので $\operatorname{div}(\mu)=n\big((\infty_-)-(\infty_+)\big)$、$n\in\mathbb Z$。

**(4) $n=5$。** $t=1/x$ で展開する。$a=a_5t^{-5}(1+O(t))$、$y=\pm t^{-3}(1+O(t))$(符号が $\infty_\pm$ の定義)、$py=\pm p_2t^{-5}(1+O(t))$。ゆえに
$$ \mu = (a_5\pm p_2)\,t^{-5}+O(t^{-4}). $$
E-3 より $a_5=p_2\ne0$ だから $\infty_+$ では先頭係数が $2a_5\ne0$(標数 0)で $\operatorname{ord}_{\infty_+}(\mu)=-5$。$\iota$ は $\infty_+\leftrightarrow\infty_-$ を入れ替え $\mu\circ\iota=\mu^\iota$ かつ $\operatorname{div}(\mu^\iota)=-\operatorname{div}(\mu)$ だから
$$ \operatorname{ord}_{\infty_-}(\mu)=\operatorname{ord}_{\infty_+}(\mu^\iota)=-\operatorname{ord}_{\infty_+}(\mu)=+5. $$
(3) と合わせて $n=5$。∎

**系 E5-D1(S5-1 の内容の再取得).** $5\big[(\infty_-)-(\infty_+)\big]=0$ が従う。位数は 1 か 5 だが、位数 1 なら $\infty_+\sim\infty_-$ となり種数 2 の曲線に次数 1 の $\mathbb P^1$ 写像が生じて矛盾。**ゆえに位数はちょうど 5。** これは命題 S5-1 の主張と一致する。**S5-1 を oracle として引く必要はない。**

### 2.3 機械検証手続き(実装が実行すべき全部)

```text
V-E5.1  f6 は monic・deg 6・squarefree            (gcd(f6, f6') が定数)
V-E5.2  deg a = 5 かつ deg p = 2
V-E5.3  a5 = p2 かつ a5 != 0                      (先頭係数の exact 一致)
V-E5.4  a^2 - f6 * p^2 が非零定数                 (= C・E-4 そのもの)
        --------------------------------------------------------
        以上が全て真 ⟹ E-5 は命題 E5-D により成立。
        向き: P_0 := ∞_-(y/x^3 -> -1 の枝)・P_∞ := ∞_+。
```
**すべて有理係数多項式の演算だけ**であり、追加入力・外部参照・数値近似を要しない。**E-3 の符号($a_5=+p_2$)が向きを決める** — もし $a_5=-p_2$ なら $P_0$ と $P_\infty$ が入れ替わる。ここが「orientation」の実体であり、**符号として既に E-3 に埋め込まれている**。

### 2.4 公開テストベクトル(封印集合と無関係・本稿で新たに構成)

```text
a  = x^5 + 1
p  = x^2
f6 = x^6 + 2x
C  = a^2 - f6 p^2 = 1
```
E-1〜E-4 を満たす($f_6=x(x^5+2)$ は squarefree)。$t$ 展開の実測:

```text
ord_{∞+}(mu) = -5   先頭係数 2
ord_{∞-}(mu) = +5   先頭係数 1/2
=> div(mu) = 5(∞-) - 5(∞+)     (Or) と一致
```
**この例は三重根を持たない**($a'=5x^4$、$a(0)=1\ne0$)ので、E-5 検査の positive fixture として使える。

---

## 3. 宣言フラグ実装への回答

### 3.1 凍結仕様との整合

**矛盾しない。** E-5 は entrance condition であり、`orientation_declared_ok` を要求する実装は**凍結条項より狭い述語**を実装している(fail-closed 側)。凍結仕様に反する動作は生じない。

### 3.2 ただし accepted universe を狭める

**推奨は導出実装への移行である。** 理由:
- E-5 は §2 のとおり **E-1〜E-4 から導出可能**なので、宣言を要求すると **valid instance representability** が変わる — **E-1〜E-4 を満たす正当な candidate が、フラグ未宣言というだけで [6] になる。**
- これは便 72 F13.3 が freeze-blocking FAIL と定めた類型(`accepted universe` を変える)に該当する。**外部入力でないものを外部入力として扱うと、述語が狭くなる。**

**最小修理形(spec 改版なしで実装側だけで閉じる)**:

```text
E-5 の判定 = 導出(V-E5.1..V-E5.4 を実行し、真なら E-5 成立・向きも決定)
orientation_declared_ok = optional cross-check input
  - 欠落     -> 導出値を採用(REJECT しない)
  - 存在     -> 導出値と一致することを検査。不一致は [6]
  - 導出の前提(V-E5.1..4)が偽 -> その前提自身の code([1]..[6])で REJECT
```
この形なら fail-closed 性は保たれ(前提が崩れれば落ちる)、かつ正当な candidate を落とさない。

### 3.3 `external_dependencies` の `S5/prop-S5-1` の身分

**出所(provenance)の束縛であって、検証の oracle ではない。**
- spec §2 の provenance map が「E-5 = 命題 S5-1(+S5-3∞ との同値)」と書くのは、**条項の出所**の記録である。
- §2.2 の証明は S5-1 を使わず、逆に **系 E5-D1 として S5-1 の内容(位数ちょうど 5)を再取得**する。
- したがって receipt の `external_dependency` 欄は**そのままでよい**(digest 束縛は provenance の完全性のため)。

**EP 検収での照合指示**:
```text
EP-E5.1  EP fixture(non-campaign 係数)について V-E5.1..V-E5.4 を実行し、
         導出された向き(P_0 = ∞_-)を記録する。
EP-E5.2  同じ fixture について S5-1 の主張(位数ちょうど 5)を独立に確認し、
         系 E5-D1 の導出結果と一致することを照合する。
EP-E5.3  不一致は provenance の破れとして INTEGRITY_STOP に送る
         (述語の [6] ではない — 出所と導出の齟齬は別事象)。
```

---

## 4. [7](triple-root)候補の存在領域

### 4.1 三重根は $p$ を完全に決める

$a$ が $x_0$ で三重根を持つとする: $a=(x-x_0)^3b$、$\deg b=2$。(Pell) を微分して $2aa'=p(f_6'p+2f_6p')$、$\gcd(a,p)=1$(E-6)より **$p\mid a'$**。ここで
$$ a'=(x-x_0)^2\big(3b+(x-x_0)b'\big),\qquad \deg\big(3b+(x-x_0)b'\big)=2 . $$
$p$ が $(x-x_0)$ を因子に持てば $\gcd(a,p)\ne1$ で E-6 に反するから、
$$ \boxed{\ p \doteq 3b+(x-x_0)b'\ } $$
先頭係数を E-3 で合わせると比例定数は $1/5$:
$$ p=\tfrac15\big(3b+(x-x_0)b'\big). $$

### 4.2 残る条件と二つの枝(機械で解いた)

$x_0=0$ に平行移動し $b=x^2+\beta x+\gamma$($a_5=1$ に正規化)とすると $p=x^2+\tfrac{4\beta}{5}x+\tfrac{3\gamma}{5}$。(Pell) は「$a^2 \bmod p^2$ が定数」と同値で、$x^3,x^2,x^1$ 係数の 3 本の方程式になる。**多変数多項式演算で厳密に計算した結果、3 本は同一因子に落ちる**:

$$ [x^3]=\beta\cdot E,\qquad [x^2]=\tfrac65\,\beta^2\cdot E,\qquad [x^1]=\tfrac95\,\beta\gamma\cdot E, $$
$$ E=-\tfrac{18}{125}\gamma^3+\tfrac{208}{625}\beta^2\gamma^2-\tfrac{2816}{15625}\beta^4\gamma+\tfrac{2048}{78125}\beta^6 . $$

ゆえに解は **$\beta=0$ か $E=0$** の二枝しかない。

### 4.3 枝 I($\beta=0$)— 閉形の 1 助変数族

$$ \boxed{\ a=x^5+5g\,x^3,\quad p=x^2+3g,\quad f_6=x^6+4g\,x^4-8g^2x^2+12g^3\ }\qquad(g\in\mathbb Q^\times) $$
機械検算(厳密有理数)で $g=1,2,3,-1,\tfrac12$ について **(Pell) 恒等式が成立**し、$f_6$ は monic・deg 6・squarefree、$\gcd(a,p)=1$、$a_5=p_2$、そして **[7] の述語**($\deg\gcd(a,a')=2$・$\gcd(a,a')$ 非 squarefree・$\deg\gcd(a,a',a'')=1$)がすべて真 = **triple-root 判定に落ちる**ことを確認した。

- $x\to\lambda x$ は $g\to g/\lambda^2$ を誘導する。**ゆえに $g$ は尺度助変数で、$\bar{\mathbb Q}$ 上ではこの枝は曲線 1 本**、$\mathbb Q$ 上では $g$ の平方類による捻れ族である。
- **整数係数表現の最小高さ**: $4g,8g^2,12g^3\in\mathbb Z$ を要求すると実質 $g\in\mathbb Z\setminus\{0\}$ で、$|g|=1$ が最小。そのとき $\max|\text{係数}|=\mathbf{12}$($f_6$ の定数項 $12g^3$)。

> **★ 「$|係数|\le7$ で見つからなかった」ことの説明**: **枝 I の最小高さは 12 であり、箱 $|係数|\le7$ の外側にある。** 探索が $f_6$ の係数まで箱に入れているなら、この族は原理的に見つからない。**箱を $\ge 12$ に広げれば $g=\pm1$ で即座に当たる。**

### 4.4 枝 II($E=0$)— 有理根 1 つ + 無理共役 2 つ

$s:=\gamma/\beta^2$ とおくと $E=0$ は $5625s^3-13000s^2+7040s-1024=0$。**有理根は $s=8/5$ のみ**(残る二次因子 $5625s^2-4000s+640$ の判別式 $1600000$ は有理平方数でない ⟹ 残り 2 根は無理共役)。

$s=8/5$ の実在を機械確認した($\beta=5,\gamma=40$):
$$ a=x^5+5x^4+40x^3,\quad p=x^2+4x+24,\quad f_6=x^6+2x^5+25x^4-120x^3+1728x-5184 $$
E-1〜E-6 を満たし、**[7] triple-root=真**。ただし **最小高さは 5184** で、枝 I よりはるかに大きい。

### 4.5 まとめ(存在領域の見当)

| 枝 | 記述 | $\mathbb Q$ 上の解 | 整数最小高さ |
|---|---|---|---|
| **I** | $\beta=0$ | $g\in\mathbb Q^\times$(尺度)— $\bar{\mathbb Q}$ 上は曲線 1 本 | **12** |
| **II** | $E=0$・$s=\gamma/\beta^2=8/5$ | 尺度を除いて 1 点 | **5184** |
| **II′** | $E=0$ の残り 2 根 | **無理** ⟹ $\mathbb Q$ 上に解なし | — |

**「Pell 整合下では稀」は正しいが「不可能」ではない。** 三重根の locus は $\mathbb Q$ 上でも空でなく、**尺度を除いて本質的に 2 点**($s=0$ と $s=8/5$)である。

---

## 5. 実装 lane への具体的な提案(仕様解釈の範囲内)

1. **E-5 は導出せよ**(§2.3 の V-E5.1〜V-E5.4)。`orientation_declared_ok` は任意の cross-check に降格(§3.2)。
2. **[6] は「導出の前提が崩れた」場合と「宣言と導出の不一致」に限る。** 宣言の欠落で [6] を出さない。
3. **positive fixture** は §2.4 の $(x^5+1,\ x^2,\ x^6+2x)$ を使える(三重根なし・E-5 成立)。
4. **[7] negative fixture** は §4.3 の $g=\pm1$:
   ```text
   a = x^5 + 5x^3,  p = x^2 + 3,  f6 = x^6 + 4x^4 - 8x^2 + 12
   期待: REJECT / triple-root-of-a
        a_root_partition = [3,1,1] / triple_gcd_degree > 0 / gcd_squarefree = false
   ```
   **探索箱を $|係数|\le 12$ 以上に広げれば候補レベルでも到達する。**

---

## 6. 規律の申告

- **本ノートは数値(fixture)を含む。** spec / contract / manifest を**値に依存させない**規律は不変であり、上記 fixture は**仕様本文ではなく fixture store に置く**。
- **⚠ 注意(取り違え防止)**: 枝 I の Pell 定数 $C(g)=-108\,g^5$ は、$g=1$ で campaign 記録に現れる数値と**字面が一致する**。これは **[7] で棄却される三重根候補の Pell 定数**であって campaign の答ではない。**同一視してはならない。** 本稿の自己 lint はこの数値を封印語彙として扱うので、**この一致は spec 側へ持ち込まないこと。**
- **接触規律**: 本稿の計算はすべて**自作の公開インスタンスと記号計算**による。封印集合(`ninfty-neg-01..08`)の係数には**一度も触れていない**。
- **lane 不可視**: lane A/B の実装内容は参照していない。
- **UNKNOWN**: 枝 II′ の無理根が $\mathbb Q$ 以外の基礎体で意味を持つか、および三重根 locus が $\bar{\mathbb Q}$ 上でちょうど 2 点であることの**モジュライ論的証明**は本稿では与えていない(機械的な解の完全列挙は $\beta,\gamma$ の 2 変数系についてのみ)。
