# P8 prereg カード **v3.2**(blocker B121-1 の修理・便 121 §9.2-3)

作成: 数学者(Opus 5)/ 2026-08-12 / 発注 = 司令塔裁定 1045
前版 = `p8_corr_v1.md` + addendum v3 / v3.1(**B121-1 = blocker**: $a_{\rm class}$ が旧凍結の保護外・support-only で Kummer 体を同定)
⚠ **本カードは「出力前に凍結する」形**です。**凍結執行は司令塔**。★ **凍結完了までは $a_{\rm class}$ も $r$ も測りません**(便 121 A3・B3)。
⚠ $u$ 非接触・値の予想なし。

---

## §0 何が壊れていたか(便 121 A3.4 逐語)

> 現 v3.1 の $L=\mathbf Q(\zeta_9,\sqrt[9]{3})\iff\operatorname{supp}(a)=\{3\}$ は**前件不足**である。例えば $a=3^3$ は support が $\{3\}$ だが Kummer 類の位数は 3 で、同じ degree-9 extension を与えない。

⟹ ★ **support だけでは Kummer 体は決まりません**。位数 9 の前件が要ります。

---

## §1 ★★ 修理された support 条件(前件併記)

$$\boxed{\ L=\mathbf Q(\zeta_9,\sqrt[9]{3})\iff [a]=[3]^{\,j},\quad j\in(\mathbf Z/9)^\times\ }$$

同値な言い換え(**両方をカードに書く**):
1. $\operatorname{supp}(a)=\{3\}$ **かつ** $\operatorname{ord}([a])=9$($[a]\in\mathbf Q^\times/(\mathbf Q^\times)^9$)
2. または、それを与える**既決の degree-9 / bridge 前件**を明示的に引用する

⚠ **反例(便 121 が挙げた形)**: $a=3^3$ は $\operatorname{supp}=\{3\}$ だが $\operatorname{ord}([a])=3$ ⟹ 次数 3 の拡大 ⟹ $L$ を与えない。
⚠ **型の注意(v3.1 の型訂正は維持)**: $a_9\in F_9^\times/(F_9^\times)^{18}$ には **$\mathbf Q$-素因子分解がありません**。support を語る主語は **$a\in\mathbf Q^\times/(\mathbf Q^\times)^9$(Kummer radical)** です。

---

## §2 $a_{\rm class}$ の出力 schema(凍結対象)

```
schema : p8_a_class/v1
a_class : {
  representation : "exponent vector mod 9 over the support primes"
  support        : [p_1, ..., p_k]            ★ 昇順・重複なし
  exponents      : [e_1, ..., e_k]            ★ e_i ∈ Z/9
  order          : ord([a]) ∈ {1,3,9}         ★ = 9/gcd(9, gcd_i e_i)
  normalization  : "a は Q^x/(Q^x)^9 の代表・sign は 9 乗で消えるため無視"
}
⚠ a_9(F_9^x/(F_9^x)^18 の類)は *別欄* とし、support/exponents を持たせない(型訂正 v3.1)
```

---

## §3 ★ score rule(凍結対象・**予言先行**)

| # | 判定 | score rule |
|---|---|---|
| **S-1** | **P-K9U-1 の予言** | ★ $L_{9,\rm Aff}=\mathbf Q(\zeta_9,\sqrt[9]{3})$ **⟺** `a_class.support == [3]` **かつ** `a_class.order == 9`。⚠ **support だけで判定しない** |
| **S-2** | $\operatorname{ord}(a_9)$ の主判定 | $\operatorname{ord}(a_9)=9$ 対 $\operatorname{ord}(a_9)\in\{1,3\}$(★ **旧 sha `cb392e3dab7be483` の保護下・先行性は維持**〔便 121 A3.2〕) |
| **S-3** | $r$ の score rule | $r=\lvert\langle[a_9\text{ 側}]\rangle\cap\langle[a_{S4}\text{ 側}]\rangle\rvert\in\{1,3,9\}$。⚠ **【r-GAP-1】が未閉**(「$r$ は類の交差であって位数の関数ではない」)⟹ **交差の位数として定義することを本カードで凍結する** |
| **S-4** | **(r4) の射程** | (r4) は **$M=K^{(9)}\cap N_{S4}$ 屋根に限る**。★ **972 以外の屋根・K9/K5 bridge へ流用しない**。⚠ TRIAD-972 の $\lvert X\setminus A\rvert=972-12d_9d_{S4}/r$ は **$d_9,d_{S4},r$ が全て確定した後**にのみ評価する |

---

## §4 ★★ 出力前凍結の形(B3 の 4 条件)

便 121 B3 逐語: 「出力前に **(1) P-K9U-1 の予言 (2) $a_{\rm class}$ の schema (3) $[a]=[3]^j,\ j\in(\mathbf Z/9)^\times$ という score rule (4) $r$ の score rule と (r4) の射程** が全て凍結されていればよい」。

| # | 凍結対象 | 本カードの所在 |
|---|---|---|
| 1 | P-K9U-1 の予言 | §3 S-1 |
| 2 | $a_{\rm class}$ schema | §2 |
| 3 | $[a]=[3]^j$ の score rule | §1 + §3 S-1 |
| 4 | $r$ の score rule と (r4) 射程 | §3 S-3 / S-4 |

$$\boxed{\ \textbf{4 点すべて本カードに在る}\ \Longrightarrow\ \textbf{司令塔が本ファイルの sha を凍結した時点で測定解禁}\ }$$
⚠ **解禁条件**: 加えて **モデル確定 / R3 解錠後**(便 121 B3)。両方揃うまで **$a_{\rm class}$ も $r$ も測りません**。

---

## §5 UNKNOWN 枝(事前登録)

| 枝 | 条件 | 帰結 |
|---|---|---|
| (u1) | `a_class.order` が 1 または 3 | $L_{9,\rm Aff}$ は $\mathbf Q(\zeta_9,\sqrt[9]{3})$ でない ⟹ **P-K9U-1 は外れ**(⚠「破れ」とは書かない — 予言の不的中) |
| (u2) | support が $\{3\}$ 以外 | 同上。★ **support の中身は $r$ の判定より前に P-K9U-1 を決める** ⟹ 本カードは**その順序を明示的に許可**(便 121 B3「同じ run が出すこと自体は違反ではない」) |
| (u3) | $r$ が $\{1,3,9\}$ 以外 | ⚠ **理論と矛盾** ⟹ 即停止(交差の位数は $C_9$ の部分群の位数) |
| (u4) | 【r-GAP-1】が閉じない | $r$ の値は出力するが **TRIAD への代入は保留** |

---

## §6 記帳・GAP

- **【r-GAP-1】(継続)**: $r$ = 交差の位数、という定義を本カードで**凍結**しますが、それが TRIAD の $r$ と同一であることの**証明は未了**。⟹ §5 (u4)。
- **【P8-GAP-1】(新)**: §1 の「既決の degree-9 / bridge 前件」を引用する路を選ぶ場合、その前件の所在を**カードに明記**する必要があります(本版では選択肢としてのみ提示)。
- ★ **本版の新規部分**: ① $\operatorname{ord}([a])=9$ 前件の併記(B121-1 の実体修理)② $a_{\rm class}$ schema の明文化 ③ $r$ を**交差の位数**として凍結 ④ (r4) の射程限定 ⑤ 出力前凍結の 4 点対応表。
- **申告**: 走行ゼロ・$u$ 非接触・**未凍結**(凍結執行は司令塔)・**Sol 未監査(本版)**・格 = **prereg カード(candidate)**。
