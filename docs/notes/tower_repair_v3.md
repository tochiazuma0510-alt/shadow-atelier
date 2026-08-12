# tower_repair **v3** — T63-CONNECT^fix の四行形(便 121 §9.2-2)

作成: 数学者(Opus 5)/ 2026-08-12 / 発注 = 司令塔裁定 1045 / 前版 = `tower_repair_v2.md`(**M121-2 = FAIL・正本化不可**)
⚠ **格: candidate / framework-conditional**。★ **全窓不変性も無条件の $d_9=9$ も主張しません**。

---

## §0 前版の何が失敗したか(M121-2 逐語)

> 積荷には文字列 T63-CONNECT$^{\rm fix}$ も、便 120 が指定した四前件の同窓表示もない。特に §1.3 の「uniform $(5'^b)$ なら全窓で MATCH-one が自動」という読みが残り、§2 の T63-CONNECT は M-b を独立前件にしていない。

⟹ 本版は **(a) 四行を逐語で置く (b) all-window 読みを除去する (c) M-b を独立前件として立てる** の 3 点を成果物とします。

---

## §1 ★★ T63-CONNECT$^{\rm fix}$ — 四行形(便 120 F2(c) / 便 121 A2 逐語)

> **【T63-CONNECT$^{\rm fix}$】** 固定窓 $\alpha=1$ で、次の四つが**同じ marking / convention** で成立するなら、$\operatorname{ord}(a_9)=9$ から $d_9=9$ が従う。
>
> | 行 | 前件 | 種別 |
> |---|---|---|
> | **(i)** | **GEO9** | 幾何側の供給 |
> | **(ii)** | **$(5'^b)@\alpha=1$**(= **M-a**) | ★ 固定窓・$b$ は当該窓内で $\gamma$ 非依存 |
> | **(iii)** | **T63-MATCH$@\alpha=1$**(= **M-b**) | ★ **独立前件**(M-a から従わない) |
> | **(iv)** | **$R^{\rm cyc}$** | 円分側の整合 |
>
> **格**: **candidate / framework-conditional**。

$$\boxed{\ \textbf{(i)}\ \mathrm{GEO9}\ \wedge\ \textbf{(ii)}\ (5'^b)@\alpha{=}1\ \wedge\ \textbf{(iii)}\ \text{T63-MATCH}@\alpha{=}1\ \wedge\ \textbf{(iv)}\ R^{\rm cyc}\quad(\text{同 marking})\ \Longrightarrow\ \operatorname{ord}(a_9)=9\ \vdash\ d_9=9\ }$$

---

## §2 ★ all-window 読みの除去(M120-5 / M121-2)

**✘ 撤回(前版 §1.3 に残っていた読み)**:
> ~~uniform $(5'^b)$ が成り立つなら、全窓で MATCH-one が自動的に従う~~

**正**(便 120 の逐語・W-52):
$$\boxed{\ \textbf{uniform }(5'^b)\ \textbf{は「}b\ \textbf{が}\textbf{固定窓の内部で}\ \gamma\ \textbf{非依存」であって「全窓で同じ」ではない}\ }$$

⟹ ★ **M-a($(5'^b)@\alpha=1$)から M-b(T63-MATCH$@\alpha=1$)は従いません**。両者は **同一窓 $\alpha=1$ 上の独立な 2 前件**です。
⟹ 前版が (iii) を (ii) の帰結として扱ったのが **M121-2 の実体**です。

---

## §3 ★ 同 marking / convention の意味(型境界)

四行が**別々の marking で成立**しても結論は出ません。要求されるのは:
1. **同一の基点・路の取り方**(接基点 / 生成元の向き)
2. **同一の $\zeta$ 正規化**($R^{\rm cyc}$ と GEO9 が同じ $\zeta_{18}$ 規約を使う)
3. **同一の $a_9$ の定義**($F_9^\times/(F_9^\times)^{18}$ の類として・⚠ **$\mathbf Q$-素因子 support を読ませない**(便 121 A3.1 の型訂正))

⚠ **未点検**: 私は上記 3 点を四行すべてで**逐条照合していません** ⟹ 【TOWER-GAP-3】(§5)。

---

## §4 ★ 帰結の射程(何を主張し、何を主張しないか)

| 主張する | 主張**しない** |
|---|---|
| 四行が同 marking で立てば $\operatorname{ord}(a_9)=9\vdash d_9=9$ | ✘ **無条件の $d_9=9$** |
| 固定窓 $\alpha=1$ での連結 | ✘ **全窓不変性**($b$ の窓間一致) |
| framework-conditional な candidate | ✘ **Conj 5.1@$n=9$ の証明**(公開未解決問題) |

⚠ さらに:$d_9=\operatorname{ord}(a_9)$ は**無条件等式ではありません**(v1.4.9 §8 の【K9-COMPOSE 旧行】)。本命題は $\operatorname{ord}(a_9)=9$ を**入力**として $d_9=9$ を出す形であり、$\operatorname{ord}(a_9)$ 自体の決定は**別問題**(P8 prereg の対象・⚠ **v3.2 凍結まで測定停止**)。

---

## §5 GAP・記帳

- **【TOWER-GAP-3】(中・新)** §3 の marking 三点の**逐条照合が未了**。四行が同 marking であることの確認は本版では**前件のまま**。
- **【COMPOSE-GAP-1】**: 便 119 で再 OPEN。本版はその上に立つ **framework-conditional** な連結であり、GAP を閉じるものではありません。
- **記帳**: 本版は **M121-2 の修理**であって新規の数学ではありません(四行はすべて便 120 F2(c) の逐語)。★ 新規部分は **all-window 読みの明示的撤回**と **M-b の独立前件化**の 2 点のみ。
- **申告**: 走行ゼロ・$u$ 非接触・**Sol 未監査(本版)**・**verified ではない**・格 = **candidate / framework-conditional**。
