# 157dn/157dp 貼り合わせの事前検収 — 短報

**状態札: 数学者事前検収・司令塔検分前・Sol 未監査・157dn run 未着**
起草: Claude 数学者 / 2026-08-19 / 委嘱 = 司令塔(`ops/express/20260819_sol_fable_157dn_intersection_run.md`・run 32174026086 実行中)
格: paper candidate。機械計算ゼロ。封印非接触。語法: exponent = 冪指数 / index = 指数。
記号: $H$ = frozen q3 kernel、$L=H\cap\ker\rho_{A_5}$、$\Phi=\Phi_3(H)$、$L'=L\cap\Phi$。

---

## 0. 一行裁定

**(a) 貼り合わせ補題は成立する。しかも Sol の理由(共通単純商の非存在)より強く単純な理由で成立する — $H/L\cong A_5^4$ は完全群、$H/\Phi$ は可換 ⟹ 共通商は完全かつ可換 ⟹ 自明。** これは $PB_4$/$PB_3$/$F_2$ の三水準すべてで(合成因子の議論で)成立する。
**(b) ゲート継承: hexagon・pentagon・friendly・charming(交換子代表)は自動。onto は「自動だが理由は Goursat + 共通商非存在」で、同じ前件に乗る。marking/representative-independence だけが要再検査。**
**(c) T48-1 は $L\to L'$ の置換でそのまま通る**(survive 写像の入力は $L'$ の代表対のみ・$L'$ の isolated 性不要)⟹ 区間 $[L',M]$ の全 isolated 段が閉じる。
**(d) $m=0$ は N2 規約を自明に満たす(良い知らせ)。ただし L10 の「危険な形」($u=\pm1$)そのものなので、$f$ が段ごとに変わることの明示と「内部自己同型でない」確認を要する。**
**(e) 157dn が UNKNOWN なら、探索を広げず「段の大きさを変える」— $\Phi$ を丸ごとでなく $H/\Phi$ の一つの $B_4$-chief 商へ縮めて再走。**
**★ 私が見つけた追加の残作業 1 件(最重要): CRT の前件 $\gcd(L_{\rm ord},\Phi_{\rm ord})=H_{\rm ord}$。Sol の「PB2 $C_5$」がこれを担っているはずだが、明示されていない。**

---

## 1. (a) 貼り合わせ補題 — 正しい。前件をより強い形で確定する

### 1.1 群論の核(3 行)

**補題 GL-1.** $G_1$ が非自明な 3-群商を持たず、$G_2$ が 3-群なら、$G_1,G_2$ に共通の非自明商はない。
*証明.* 共通商 $C$ は $G_2$ の商ゆえ 3-群、かつ $G_1$ の商 ⟹ 仮定より $C=1$。∎

**補題 GL-2(本件への適用・三水準).**
- **$PB_4$ 水準**: $H/L\cong A_5^4$ は完全(単純群の直積)⟹ 全ての商が完全 ⟹ 非自明 3-群商なし。$H/\Phi=H_1(H;\mathbf F_3)$ は elementary abelian 3。GL-1 より共通商は自明。
- **$PB_3$ 水準**: $L'_{PB_3}=\bigcap_j\varphi_j^{-1}(L\cap\Phi)=L_{PB_3}\cap\Phi_{PB_3}$(逆像は交叉と可換 ✓)。$H_{PB_3}/L_{PB_3}\hookrightarrow(H/L)^5$ ゆえ合成因子は $A_5$ のみ ⟹ 3-群商なし(Sol の $D_F=A_5\times C_5^2$ なら合成因子は $A_5,C_5$ ⟹ やはり 3-群商なし)。$H_{PB_3}/\Phi_{PB_3}$ は 3-群(T33-L9, $p=3$)。⟹ 共通商は自明。
- **$F_2$ 水準**: 同じ議論。
**系 GL-3(Goursat).** 各水準で $L_\bullet\Phi_\bullet=H_\bullet$、従って
$$H_\bullet/L'_\bullet\ \cong\ H_\bullet/L_\bullet\ \times\ H_\bullet/\Phi_\bullet\qquad(\bullet=PB_4,\,PB_3,\,F_2).$$
*証明.* $H/(L\Phi)$ は両者の共通商 ⟹ 自明 ⟹ $L\Phi=H$。$L\cap\Phi=L'$ と合わせ Goursat の同型。∎

> **⟹ Sol の主張は正しい。しかも理由は「完全 vs 可換」という最も頑健な形で書ける** — $D_F$ や PB2 の具体形に依存しない。**この形で書くことを推奨する**(実装の詳細が変わっても壊れない)。

### 1.2 ★ 見落とされている前件 — CRT の $m$-座標

$PB_2\cong\mathbf Z$ で部分群は $\langle x_{12}^n\rangle$、$L'_{PB_2}=L_{PB_2}\cap\Phi_{PB_2}$ ⟹
$$L'_{\rm ord}=\operatorname{lcm}\bigl(L_{\rm ord},\ \Phi_{\rm ord}\bigr).$$
貼り合わせで $m$ を作るには **CRT の両立条件**が要る:
$$\boxed{\ \gcd\bigl(L_{\rm ord},\ \Phi_{\rm ord}\bigr)\ =\ H_{\rm ord}\ }$$
(2 成分は $H_{\rm ord}$ を法としてしか一致を保証されないため)。これは**自動ではない**:$\Phi_{\rm ord}/H_{\rm ord}$ は 3 冪(T33-L9)、$L_{\rm ord}/H_{\rm ord}$ は $|A_5|=2^2\!\cdot\!3\!\cdot\!5$ 由来なので **3 を含み得る**。含めば CRT は破れ、貼り合わせは $m$ 座標で止まる。
> **Sol の「PB2 $C_5$」がまさにこの前件を担っているはず**($L_{\rm ord}/H_{\rm ord}=5$ なら 3 と互いに素 ✓)。**しかし express 便でその役割が明示されていない。** ⟹ **FC-29** として明示登録を要求する。gentle 側 150 便が $\gcd(18\cdot3^r,36)=18=M_{\rm ord}$ を明示的に確認していたのと同じ箇所である。

---

## 2. (b) ゲート継承 — 型ごと

$L'_\bullet=L_\bullet\cap\Phi_\bullet$ より $B_3/L'_{PB_3}\hookrightarrow B_3/L_{PB_3}\times B_3/\Phi_{PB_3}$、$PB_4/L'\hookrightarrow PB_4/L\times PB_4/\Phi$(常に成立・GL-3 より実は同型)。

| ゲート | 継承 | 根拠 |
|---|---|---|
| **hexagon (2.18)(2.19)** | **自動** | 埋め込みゆえ「mod $L'_{PB_3}$ で成立 ⟺ 両成分で成立」 |
| **pentagon (2.20)** | **自動** | 同上($PB_4/L'$) |
| **friendly**($2m+1\in(\mathbf Z/L'_{\rm ord})^\times$) | **自動** | $L'_{\rm ord}=\operatorname{lcm}$ ⟹ 両方に互いに素 ⟺ lcm に互いに素 |
| **charming 前半**($f$ が $[F_2,F_2]$ 代表を持つ) | **自動** | $[G_1\times G_2,G_1\times G_2]=[G_1,G_1]\times[G_2,G_2]$、かつ $[F_2/N,F_2/N]=[F_2,F_2]N/N$ ⟹ **実際の交換子語が必ず取れる**(Sol の残作業 2 は自動で埋まる) |
| **onto**($T^{F_2},T^{PB_3},T^{PB_2}$ 全射) | **自動。ただし理由は非自明** | 部分群 $U=\langle x^u,\ f'^{-1}y^uf'\rangle\le F_2/L'_{F_2}\cong G_1\times G_2$ は両成分へ全射。**Goursat**: 全射な部分群は共通商上の fibre product ⟹ **共通商が自明(GL-2)なので $U=G_1\times G_2$** ⟹ 全射。⟹ **(a) と同じ前件に乗る** |
| **marking / representative-independence** | **要再検査** | fibre product 上の marked 同型が $H$ 上で一致することの確認が要る(gentle 150 §1.3 の「settled automorphism は $Q_0$ 上で同じ写像を誘導」に対応)。⟹ **FC-30** |
| **settlement / isolated** | **不要**(Sol も非主張)✓ | FV-5 / T48-1 が source 側の isolation を要求しない |

> **⟹ 「onto が自動で継承される」ことは事前検収の収穫である**(素朴には Goursat の反例が怖い箇所)。ただし**共通商非存在に完全に依存する**ので、(a) の前件が壊れれば onto も壊れる — **単一障害点**として記録すべき。

---

## 3. (c) T48-1 との接続 — そのまま通る

**命題 T48-1 の証明は survive 写像 (3.24) しか使わず、入力は $L'$ 精度の literal 代表対 $(m,f)$ のみ**であり、$L'$ の isolated 性・settlement を一切要求しない(T-34 の軽量化)。⟹ $L\to L'$ の置換は**そのまま可**:
$$\text{$L'$ に outside roof の pair} \ \Longrightarrow\ \forall\ \text{isolated }H'\ \text{with}\ L'\le H'\le M:\ I_{H'}=X .$$
$[L',M]\supsetneq[L,M]$ なので**閉じる窓が真に増える** ✓。**下向きについては T-48 §2 のとおり何も出ない**(一様吸収は B4-B と同値)。

---

## 4. (d) $m=0$ の罠検査

$u=2m+1=1$。
1. **N2 規約(chp_proof E-1.2)**: $\gcd(2m+1,K_{\rm ord})=\gcd(1,\cdot)=1$ ⟹ **自明に成立** ✓。Sol の T-42 が指摘した $m$-被覆の問題(**$m_{\rm new}=m+H_{\rm ord}u s'$ で $u$ の可逆性が要る**)も $u=1$ なら完全に消える ✓✓ — **この pair では $m$-補正が全被覆する**。良い知らせ。
2. **L10 との関係**: T33-L10 は「単一 literal pair が全段で shadow ⟹ $2m+1=\pm1$」。本 pair は $u=1$ で**まさにその形**。L10 は矛盾を出さない($m\in\{0,-1\}$ は許される)が、**もし同一の $(0,f)$ が全段で通り続ければ「離散 GT 元」という異常に強い主張になる**(GS §6.9)。⟹ **段ごとに $f$ が変わっていることを明示的に記録すること**(157dp candidate 124 と 157dn の $f$ が異なることの申告)。今回は補正が入るので問題ないはずだが、**$m=0$ の positive が続いたら警報**。
3. **内部自己同型でないことの確認**: $m=0$ では $T_{0,f}(x)=x,\ T_{0,f}(y)=f^{-1}yf$ となり、T-29 否定済み 3.4 が扱った当の形。**もし $T$ が大域的な内部自己同型なら屋根像は自明 ⟹ $A$ の中 ⟹ outside 性と矛盾**。run が outside を主張している以上そうではないはずだが、**安価な健全性検査**として組み込む価値がある ⟹ **FC-31**。

---

## 5. (e) 157dn が UNKNOWN(300 分 soft stop)の場合 — 一行

**探索を広げるのではなく段の大きさを変える**: T-48 §5 で確立したとおり **NA-1/NA-2/NA-5/OBS-NA は chief 段であることを使っていない**ので段は自由に取れる ⟹ **$\Phi$ を丸ごとでなく $H/\Phi$ の一つの $B_4$-chief 商へ縮めて再走**(層は閉じないが前線は前進し、$L'$ の代わりに $L\cap\Phi_1$ で T48-1 が発火する)。

---

## 6. Sol の残作業リストの仕分け(一行ずつ)

| Sol の残作業 | 仕分け |
|---|---|
| **$J_LJ_\Phi=J_H$ の marked 証明** | **工房側で先に埋まる(本書 §1)**。群論の核は「完全 vs 可換」で三水準とも証明済み。Sol 側に残るのは marked 同型の一致の literal 確認のみ(= FC-30) |
| **実 glued commutator representative** | **工房側で埋まる(自動)**。$[F_2/N,F_2/N]=[F_2,F_2]N/N$ より必ず取れる(§2 表) |
| **全 literal gate の独立 replay** | **Sol 側実装が正しい**。producer/checker 分離の本体で、紙では代替できない |
| **(追加・私が見つけた)$\gcd(L_{\rm ord},\Phi_{\rm ord})=H_{\rm ord}$** | **Sol 側で明示登録が必要(FC-29)**。CRT の前件で、破れると $m$ 座標で貼り合わせが止まる。最重要 |
| **(追加)marking/representative-independence の継承** | **Sol 側(FC-30)** |
| **(追加)$m=0$ が内部自己同型でないことの健全性検査** | **どちらでも可・安価(FC-31)** |

---

## 7. 新規の有限検査

| 番号 | 検査 | 重要度 |
|---|---|---|
| **FC-29** | $\gcd(L_{\rm ord},\Phi_{\rm ord})=H_{\rm ord}$(= $L_{\rm ord}/H_{\rm ord}$ の 3-部分が自明)。Sol の「PB2 $C_5$」がこれを担うなら明示せよ | **最重要**(貼り合わせの単一障害点その 1) |
| **FC-30** | marked 同型が $H$ 上で一致すること(representative-independence の継承) | 高 |
| **FC-31** | $m=0$ の $T_{0,f}$ が大域内部自己同型でないこと(屋根像 outside の健全性検査) | 低・安価 |

---

## 8. 申告

- 手計算で検証: GL-1/GL-2/GL-3(三水準の共通商非存在と Goursat)、$L'_\bullet=L_\bullet\cap\Phi_\bullet$(逆像と交叉の可換性)、$L'_{\rm ord}=\operatorname{lcm}$、CRT 前件、5 ゲートの継承(特に **onto の Goursat 論法**)、$[F_2/N,F_2/N]=[F_2,F_2]N/N$、$u=1$ での N2 と T-42 被覆の自明化。
- **157dn の結果は未着**。本書は「157dn が positive を返した場合」の事前検収であり、**positive を前提していない**。
- **単一障害点**: (a) の共通商非存在。これが壊れると Goursat も onto 継承も同時に壊れる。ただし「完全 vs 可換」なので壊れる余地は小さい。
- **UNKNOWN**: FC-29/30/31、157dn の結果。
- **一様吸収は依然出ていない**(T-48 §2)。**B4-B は宣言していない。**
