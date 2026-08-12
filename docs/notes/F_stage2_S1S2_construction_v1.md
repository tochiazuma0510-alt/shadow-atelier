# (Ad) 段 2 — S2-1 / S2-2 の構成(裁定 1051・B2 GO)

作成: 数学者(Opus 5)/ 2026-08-13 / spec = `F_stage2_ad_spec_v1.md`(凍結 sha `aa49fb520ebfe2f3`)
⚠ **B2 の 5 条件を遵守**: target $=H_F$ / module $=\mathrm{Ad}$ / **twist $i=0$ 固定** / **窓資格は非結論** / **972・非円分供給・K9-K5 bridge へ流用禁止** / **R-1 は OPEN**。
⚠ $u$/$c$ 非接触。**格: candidate**(Sol 未監査)。

---

## §0 結論 — **S2-1 と S2-2 は同時に、紙で、探索ゼロで閉じます**

$$\boxed{\ \tilde H:=\bigl\{(A,\sigma)\in SL^{\pm}(2,\mathbf Z/691^2)\times S_3\ :\ \det A=\mathrm{sgn}(\sigma)\bigr\}\ }$$

⟹ $1\to\mathrm{Ad}\to\tilde H\to H_F\to1$ が **非分裂拡大**を与え、その類が $H^2(H_F,\mathrm{Ad})$($\dim=1$)の**生成元**。

---

## §1 S2-1(非零類の明示生成元)

**構成**: 段 1′ の系統 C で使った $1\to\mathfrak{sl}_2\to SL(2,\mathbf Z/691^2)\to SL(2,691)\to1$ を、**$H_F$ と同じ fiber product の型で $\mathbf Z/691^2$ 上に取り直す**だけです。

**検証(4 点・すべて紙)**
1. **核の同定**: $\det(I+691X)=1+691\,\mathrm{tr}X\pmod{691^2}$ ⟹ $\det=1\iff\mathrm{tr}X=0$
 ⟹ $\ker(\tilde H\to H_F)=\{(I+691X,1):\mathrm{tr}X=0\}\cong\mathfrak{sl}_2(\mathbf F_{691})=\mathrm{Ad}$ ✔
2. **全射性**: $SL^\pm(2,\mathbf Z/691^2)\twoheadrightarrow SL^\pm(2,691)$(Hensel / 滑らかさ)⟹ $\tilde H\twoheadrightarrow H_F$ ✔
 ($\sigma$ 成分は変わらず、$\det A=\mathrm{sgn}\sigma\in\{\pm1\}$ は $\mathbf Z/691^2$ 上でも整合)
3. **作用**: 核への共役作用は $\mathrm{Ad}$(行列共役)✔ ⟹ ★ **module は $\mathrm{Ad}$、twist は $i=0$**(det 捻りなし)✔ **B2 条件 1 を満たす**
4. **fiber product の整合**: $(A,\sigma)$ の条件 $\det A=\mathrm{sgn}\sigma$ は $\mathbf Z/691^2$ 上で well-defined($\det$ の値は $\pm1$)✔

⟹ ★ **拡大類 $[\tilde H]\in H^2(H_F,\mathrm{Ad})$ が定まる** ✔

## §2 S2-2(非分裂性)

**主張**: $\tilde H\to H_F$ に補元は存在しない。
**証明**: 補元 $\bar H\le\tilde H$($\bar H\cong H_F$・同型に写る)があるとする。$SL(2,691)\le H_F$ の逆像に制限すると、$\bar H\cap\bigl(\text{逆像}\bigr)$ は $SL(2,\mathbf Z/691^2)$ における $\mathfrak{sl}_2$ の**補元**になる。
⟹ 段 1′ の系統 C(**私が非当事者として悉皆検算 PASS**: $p=5,7,11,13$ で $u$ の $\det\equiv1$ なる全持ち上げ **125/343/1331/2197 個すべてで $w^p=I+pE_{12}\ne I$**)より、そのような補元は存在しない。∎

$$\boxed{\ \Longrightarrow\ [\tilde H]\ne0\ \textbf{かつ }\dim H^2(H_F,\mathrm{Ad})=1\ \Longrightarrow\ [\tilde H]\ \textbf{は生成元}\ }$$

⚠ **$p=691$ での非分裂性**: 上の悉皆は $p\le13$。$p=691$ では **$u^p=I+pE_{12}$**($(u-I)^2=0$ より $u^p=I+p(u-I)$)という**紙の 1 行**が同じ結論を与えます ⟹ ★ **$p$ 非依存** ✔

---

## §3 到達点と、**到達していない点**(B2 条件 2・3 の遵守)

| 項 | 状態 |
|---|---|
| **S2-1** 非零類の明示生成元 | ★ **完了**(§1) |
| **S2-2** 非分裂拡大 | ★ **完了**(§2) |
| **S2-3** braid lift | ⚠ **未着手**(【S2-GAP-1】) |
| **S2-4** 所要の surjectivity | ⚠ 未着手 |

$$\boxed{\ \textbf{★ 非結論行(必ず claim と cert に書く)}\ }$$
> 1. 本結果は「**窓が arithmetic に qualification された**」ことを**意味しない**(B2 条件 2)。
> 2. **972 / 非円分供給 / K9・K5 bridge へ流用しない**(B2 条件 3)。
> 3. **R-1 は OPEN**(B2 条件 4)— ③→① 非円分算術供給は未証明。
> 4. ★ 本結果は **$H_F$ と $\mathrm{Ad}$ の内部の群論**であり、**$G_\mathbf Q$ 側の実在**については何も言っていない(札 I-CEX-4 の「第 0 要求 = 両者を同じ空間に置く写像」は未構成)。

---

## §4 cert 記入(schema `F_stage2_ad/v1`)

```
stage : "S2-1" / "S2-2"(両方 PASS)
target : "H_F" ; module : "Ad" ; twist_i : 0
class_nonzero   : true      (§1+§2)
extension_split : false     (§2)
braid_lift      : null      (S2-3 未着手)
surjectivity    : null
method          : "paper_lemma"     ★ 探索ゼロ・機械走行ゼロ
★ r1_status : "OPEN"
★ r1_note : "③→① 非円分算術供給は未証明。段2 の内部構成の論理前件ではないが、段4 相当のゲートは OPEN。"
★ no_window_qualification : true
★ no_transfer : ["972", "non-cyclotomic supply", "K9/K5 bridge"]
name_collide_note : "H_F = pair_h2 の Ḡ。|H_F|=|H_6|。P-PH2-4 は再掲"
u_touched : false ; c_touched : false ; verdict : null
```

## §5 GAP・次の一手

- **【S2-GAP-1】(大・継続)** **S2-3(braid lift)**が残る唯一の重い段。★ spec §2 の私の推奨どおり、**S2-1/S2-2 を最小成果として切り出せた**ので、S2-3 の失敗は本結果を巻き込みません ✔
- **【S2-GAP-2】★ 閉鎖**($S_3$ 成分の持ち上げ = fiber product をそのまま $\mathbf Z/691^2$ 上に取る、で解決)。
- **★ 次の一手(推薦)**: S2-3 に入る前に **F4 の心構え**(braid lift 不存在 = 一級の否定的結果)を活かし、**「$\tilde H$ が braid 関係式を満たす表現をもつか」を先に紙で検査**する(⟹ 位数条件・$\Delta^2$ の像などの必要条件で早期に落ちるかもしれない)。⟹ ★ **教訓 F-1 の適用**(計器を作る前に紙で決まらないか)。
- **申告**: 機械走行ゼロ(紙のみ)・$u$/$c$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
