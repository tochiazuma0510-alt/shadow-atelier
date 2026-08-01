# gtpi_v1 追補 — 配達 U-PB4 を受けた監査点 A の閉鎖と、PB₄ 線の着手判定

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01
- 本体: `docs/notes/gtpi_v1.md`(`0d8f7f909d77c16568bfb511e43626008804b107620f2da702f696a9bab9d5bf`)— **本体は書き換えていない**(versioned 規律)
- 入力: 司令塔配達 `docs/scout/覚書_upb4_2008_v1.md` + `papers/2008.00066-what-are-gt-shadows.pdf`
- **読んだ範囲の申告**: 2008 は `papers/txt/` 経由で **Definition 2.19(charming)/ Definition 3.2(settled・isolated)/ Proposition 3.3(交叉構成)とその証明冒頭**のみ精読。App A.3・Thm 3.8・§4 は未読。2401 は **Definition 3.1(3.5)–(3.6) と Notational quirks (1.19)** を精読。全読していない。

---

## 1. ★ 監査点 A(模型忠実性)は **二重照合で閉じた**

司令塔推奨の「2008 §2.5 と 2401 対応条項の二重照合」を実行した。**両方に literal に一致する。**

| probe の条件(逐語) | 2401.06870(主線・B₃ gentle) | 2008.00066(B₄ 本来系) |
|---|---|---|
| `charm := Filtered([0..Nord-1], z -> GcdInt(2*z+1,Nord)=1)` | **Def 3.1 charming 第 1 条**「$2m+1$ が $\mathbb Z/N_{\rm ord}\mathbb Z$ の単元を代表する」 | (2008 は Def 2.19 に含めず・実質同じ) |
| **`c4 := (q in DerivedSubgroup(QP))`** | **Def 3.1 charming 第 2 条**「$fN_{F_2}\in[F_2/N_{F_2},\,F_2/N_{F_2}]$、**同値に** coset $fN_{F_2}$ が $[F_2,F_2]$ の元で代表できる」/ (1.19) | **Def 2.19 charming 第 1 条**「coset $fN_{PB_3}$ が $f_1\in[F_2,F_2]$ で代表できる」 |
| `c5 := (Size(sb) = Size(QF))` | Def 3.7(GT-shadow の全射条件) | **Def 2.19 charming 第 2 条**「$T^{F_2}_{m,f}:F_2\to F_2/(N_{PB_3}\cap F_2)$ が全射」 |

> ### 補題 C4-CANON【機械 + 2 行】
> 2401 Def 3.1 は導来部分群を **$[F_2/N_{F_2},F_2/N_{F_2}]=[Q_F,Q_F]$**(下付き $F_2$ = $Q_F$、位数 1500)で取り、probe の $c_4$ は **$[Q_P,Q_P]$**($Q_P$ 位数 7500)で取る。**両者は等しい。**
> **証明.** $\Psi(c)\in\ker\rho=Z(Q_P)$(定理 STR)ゆえ $Q_P=Q_F\cdot\langle\Psi(c)\rangle$ は中心拡大、よって $[Q_P,Q_P]=[Q_F,Q_F]$。∎
> **機械**(`scratchpad/gtpi_c4_canon_check.g`): $\lvert Q_P\rvert=7500$、$\lvert Q_F\rvert=1500$、$\lvert[Q_P,Q_P]\rvert=\lvert[Q_F,Q_F]\rvert=60$、**`[QP,QP] = [QF,QF] : true`**、`Psi(c) 中心 : true`、`[QP,QP] <= QF : true`。

**含意**: 正典では shadow の $f$ は $F_2/N_{F_2}=Q_F$ の元である(2401 (3.5))。probe の $q$ は $Q_P$ の元だが、$c_4$ により自動的に $[Q_F,Q_F]\le Q_F$ に落ちる。**型のズレは存在しなかった。** 【GAP-GTPI-1】(模型忠実性)のうち **charming 部分は閉鎖**。

> ### ⚠ 所見 C5-ORIENT(正直な開示・本体 §4 への追加)
> `Chk6` の $c_5$ は `sb := Group(Psi(gx^u), Psi(w^-1*gy^u*w))` と、**著者側の式を $\Psi$(反準同型)で運んだ混成の向き**で書かれている(整合規約なら $\langle\Psi(x)^u,\ q\Psi(y)^uq^{-1}\rangle$)。
> **ただしこの窓では影響しない**: cert `pent_t2t3_v32` の全 20 行で `c5_pass = 125`(fiber の 125 元**すべて**が通る)。$c_5$ は $K_\pi$ 窓で**空虚**であり、$\mathcal G$ の決定に一切寄与していない。
> ⟹ **定理 GTPI の結論は $c_5$ の向きに依存しない**($\mathcal G$ は $c_1,c_2,c_3,c_4$ で決まっている)。**別窓へ移すときは先に直すこと**(f/f⁻¹ 族の 4 件目の候補として登録)。

**残る【GAP-GTPI-1】**: hexagon($c_1,c_2$)と pentagon($c_3$)の正典条項との逐語照合は**未実施**。$c_3$ の `Pent`(= $E^5$ の 5 成分に対する $v_1v_4v_2=v_3v_5$)が 2008 App A.3 (A.13)–(A.15) と同値かは **UNKNOWN**。

---

## 2. 着手可否: **可**。ただし決定的なゲートが 1 枚ある

### 2.1 ★ 最重要の構造的発見 — **shadow のパラメータ空間は PB₄ 理論でも PB₃ 水準の対象である**

2008 Def 2.19 で shadow は $(m,f)\in\mathbb Z\times F_2$、charming は $f$ mod $N_{F_2}$、$N_{F_2}=(N\cap PB_3)\cap F_2$。すなわち:

$$\text{探索宇宙}=\{0,1,3,4\}\times\bigl[F_2/N_{F_2},\ F_2/N_{F_2}\bigr].$$

**$PB_4$ の精密化はこの宇宙に入らない。** $N\in\mathrm{NFI}_{PB_4}(B_4)$ を $N\cap PB_3=K_\pi$ となるように取れれば $F_2/N_{F_2}=Q_F$、宇宙は $[Q_F,Q_F]=A$ の **60 元** — **P6-1 で既に払った 240 走査と同額**である。

⟹ **条件付き見積もり(c₄ 型崩落で $d\lesssim10^3$)は、正典の定義から構造的に確認された。** しかも条件が外れる余地が小さい: $7500d$ は「関係式を評価する群の大きさ」にしか効かず、**走査量には効かない**。忠実置換表現の次数が中程度なら $d\sim10^4$ でも回る。
**⟹ 爆発リスクは当初見積もりより低い。**

### 2.2 決定的ゲート(初動 1 手目)— **窓の存在**

必要なのは
$$N\trianglelefteq B_4,\quad [B_4:N]<\infty,\quad N\le PB_4,\quad N\cap PB_3=K_\pi .$$
$N\le PB_4$ は「$B_4/N\twoheadrightarrow S_4$」と同値。問題は最後の条件 — **$B_3\to E\ (\cong S_3\times A_5,\ 位数\ 360)$ が $B_4$ へ延びるか**。これは自明でない(3 本の組紐生成元 $\sigma_1,\sigma_2,\sigma_3$ を、$\sigma_1,\sigma_2$ の既存の像を保ったまま braid 関係を満たすように置けるか)。

- **延びる場合**: $N:=\ker(B_4\to G)$ を取り、Prop 3.3 の $N^\sharp$ で isolated 化。指数 $=\lvert PB_4/N\rvert=7500\,d$。走査は 240。**そのまま P6-1 の全工程が $^{PB_4}$ 版で再演できる。**
- **延びない場合**: Prop 3.3 を「$N\cap PB_3\le K_\pi$ なる任意の $N$」から出発させ $N^\sharp$ を取る。このとき $PB_3$ 側の shadow 集合が 20 より**細かくなる**恐れがあり、**比較対象が別窓になる**。この分岐は CV-9 の観点から致命的なので、**着手前に必ず判定して凍結に書く**。

**判定コスト**: 安い。棚の **`lins`(低指数正規部分群)** で $B_4$ の有限表示から候補を出すか、`GQuotients(B4, G)` を候補 $G$($S_3\times A_5$、$S_5$、$S_3\times S_5$ 等)に対して回す。**半日以内**。

### 2.3 初動 3 手(この順で・各手の後に停止点)

| 手 | 内容 | 見積 | 停止条件 |
|---|---|---|---|
| **1** | **窓の存在判定**(§2.2)。$B_3\to E$ の $B_4$ への延長を `lins`/`GQuotients` で探索。結果を $^{PB_4}$ 記号つきで記帳 | 半日 | 延長不在なら**即停止して司令塔判断**(別窓比較になるため) |
| **2** | **CV-9 凍結 $^{PB_4}$ 版**を先に書く。とくに **pentagon (A.13)–(A.15) の向き**(現行 `Pent` は $E^5$ packing 条件であって (A.13)–(A.15) ではない — **f/f⁻¹ 族 5 件目の最有力候補**)と、$c_5$ の向き修理(所見 C5-ORIENT)を凍結に含める | 半日 | 凍結なしに計算しない |
| **3** | Prop 3.3 の交叉構成で $N^\sharp$ を作り、$\lvert PB_4/N^\sharp\rvert$ と $\lvert[F_2/N_{F_2},\cdot]\rvert$ を実測。**条件付き見積もりの検証** | 1 日 | $\lvert[\,\cdot\,]\rvert>10^6$ なら打ち切り UNKNOWN 記帳(8GB) |

**手 1 が通れば、定理 GTPI の $^{PB_4}$ 版は P6-1 と同じ骨格(補題 UNIV → DICT → CLOSURE)で通る見込みが高い** — 補題 UNIV の証明は「$c_4$ が宇宙を導来部分群に落とす」だけに依存し、これは §2.1 で $PB_4$ 水準でも成立するから。**ただし $\rho\vert_A$ が同型である($A\cong A_5$ 単純)という第二の柱は $PB_4$ 側で改めて要確認**(定理 STR の $^{PB_4}$ 版が要る)。

### 2.4 記号規律(混同防止・覚書 §17 に従う)

$PB_4$ 線の対象はすべて右上に $^{PB_4}$ を付す: $N^{PB_4}$、$\mathrm{settled}^{PB_4}$、$\mathrm{isolated}^{PB_4}$、$T^{PB_4}_{m,f}$、$\mathcal G^{PB_4}$。**主線の $K^{(n)}$ 族・$K_\pi$・$\mathcal G$ とは物理的に別記号**とする(2405 Remark 1.2 の同名別物)。

---

## 3. 本体への差分(要約)

1. **【GAP-GTPI-2】($PB_4$ 水準)の記述を更新**: 「現行構成に窓が存在しない」は正しいが、**「窓を新たに取れば埋まる」**(NFI$_{PB_4}(B_4)$ の元として)。閉塞は解消可能。
2. **【GAP-GTPI-1】を分割**: charming($c_4$/$c_5$)部分は**閉鎖**(§1)。hexagon/pentagon 部分は **UNKNOWN のまま**。
3. **新規の開示**: 所見 C5-ORIENT($c_5$ が混成の向き・ただしこの窓で空虚・結論に影響なし)。
4. **Sol への監査点 A** は「$c_4$ が正典条件か」から「**$c_3$(pentagon)が App A.3 (A.13)–(A.15) と同値か**」へ**移動**した(A は閉じ、次の重心はそこ)。
