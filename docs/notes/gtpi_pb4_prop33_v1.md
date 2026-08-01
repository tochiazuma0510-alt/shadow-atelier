# 手 3 実測 — **$N_0$ は isolated・LEVEL CAVEAT 解除**(定理 GTPI は $PB_4$ 水準の主張になった)

- 起草: 影工房 数学者(Claude / Opus 5)/ 2026-08-01・司令塔 GO 初動 3 手の**手 3**
- **IF-FIRST 凍結(計算前)**: `docs/notes/gtpi_pb4_cv9_freeze_v1.md` SHA-256 `66bd8743ceaec9de4d67c7a706dca40d1ffbc469d567f865b9597011925d5d90`
- probe: `search/probe/wac_v1/gtpi_pb4_prop33_20260801.g`(窓ブロック逐語移植・単系統)
- effective source: 裁定 370 + 読解ノート v1.1 + 2008.00066

---

## 0. 結論

| 予言(凍結済) | 実測 | 判定 |
|---|---|---|
| **P-PB4-1** WD-1/2/3 全 true | WD-1 `[true×5]`・WD-2 `[true×5]`・WD-3 true・$\mathrm{ord}(c)=1$ | **的中** |
| P-PB4-1 後半 WD-4 に識別力 | **`[true×5]`・識別力 false** | **外れ**(§2・正直な負) |
| **P-PB4-2a** $\lvert PB_3/N_{PB_3}\rvert=7500$ | **7500**($\lvert Q_F\rvert=1500$・$[Q_P,Q_P]=[Q_F,Q_F]=60$ true) | **的中** |
| **P-PB4-3** $\mathrm{GT}^\heartsuit(N_0)$ = P6-1 の 20 行 | **20**(charm × $[Q_P,Q_P]$ の悉皆) | **的中** |
| **P-PB4-4(本命)** 整合規約で 20/20 settled$^{PB_4}$・$N^\sharp=N_0$ | **$T$ は $B_4$ 表現 20/20・対写像の像 60 が 20/20・$\lvert PB_4/N^\sharp\rvert=60=\lvert PB_4/N_0\rvert$** | **的中** |
| **P-PB4-5** 混成規約では落ちる | **$T$ が $B_4$ 表現になるのは 4/20**(像サイズ `[-1,60]`) | **的中** |
| **P-PB4-6** LEVEL CAVEAT 解除 | 上記より **解除** | **的中** |

> ### ★★ 定理 GTPI$^{PB_4}$(格上げ)
> $N_0:=\ker(\pi:B_4\to E)\cap PB_4\in\mathrm{NFI}_{PB_4}(B_4)$、$\lvert PB_4/N_0\rvert=60$。
> 1. **$N_{PB_3}(N_0)=K_\pi$**(正典 (2.4) の 5 本引き戻し交叉)、$\lvert PB_3/K_\pi\rvert=7500$。
> 2. **$\mathrm{GT}^\heartsuit(N_0)$ は P6-1 の $\mathcal G$ と同一の 20 行**(charming 宇宙 $=[F_2/N_{F_2},F_2/N_{F_2}]$、60 元、悉皆)。
> 3. **20 行すべてが settled$^{PB_4}$**($\ker T^{PB_4}_{m,f}\cap PB_4=N_0$)⟹ **$N_0$ は isolated**(2008 Def 3.2)。
> 4. Prop 3.3 の $N^\sharp=\bigcap_K K$ は $\lvert PB_4/N^\sharp\rvert=60$ ⟹ **$N^\sharp=N_0$**(isolated の再確認)。
> ⟹ **$\mathrm{GT}^\heartsuit(N_0)=\mathrm{GTSh}^\heartsuit(N_0,N_0)$ は群**であり、定理 GTPI により **$\cong F_{20}=\mathrm{AGL}(1,5)$**。
> **`gtpi_v1.md` の LEVEL CAVEAT(「$PB_3$ 実装模型水準のみ」)は解除される。**

---

## 1. 実測原文(機械生成)

```
== WD gates ==
  WD-3 braid: s1s2s1=s2s1s2 ? true
  order of c=(s1s2)^3 in E : 1    N_ord = 5    charm = [ 0, 1, 3, 4 ]
  WD-1 (A.5) x13 = x12^-1 c x23^-1 per component : [ true, true, true, true, true ]
  WD-2 cofc[i] central in <cof[i][1],cof[i][2]> : [ true, true, true, true, true ]
  WD-4 mixing detector (fwd gens x rev rows) : [ true, true, true, true, true ]
       discriminating (contains false) ? false
== (2.4) N_PB3 ==
  |PB3/N_PB3| = |QP| = 7500   |F2/N_F2| = |QF| = 1500
  |[QF,QF]| = 60   [QP,QP]=[QF,QF] ? true
  |PB4/N_0| = |<X_ij>| = 60
== GT-heart(N_0) ==
  |GT^heart(N_0)| (exhaustive charm x [QP,QP]) = 20
== PB_4 settled ==
  |pi(PB_4)| = 60
  [aligned v(.)v^-1] T is a B_4 rep : 20/20   pair-image size = |pi(PB4)| : 20/20
     sizes seen : [ 60 ]
  [mixed  v^-1(.)v ] T is a B_4 rep : 4/20   pair-image size = |pi(PB4)| : 4/20
     sizes seen : [ -1, 60 ]
== Prop 3.3 : N^sharp ==
  #sources packed = 20   |PB_4/N^sharp| = 60
  |PB_4/N^sharp| = |PB_4/N_0| ? true
```

**混成規約で再び 4/20** — 便 92 F92-1.1 の指紋・裁定 293 の 4/8/8 と同じ数字が、$PB_4$ 水準でも同じ規約誤りから出る。**規約の正否は「$T$ が $B_4$ 表現になるか」で $PB_4$ 水準でも判定できる**(P6-1 の「群になるか」判定の $PB_4$ 版)。

---

## 2. ★ 正直な負 — **WD-4(混成検出器)に識別力がなかった**

司令塔 追加条件 (b) は「(A.5) 二表示一致の assert」だったが、**私の実装した WD-4 は裁定 370 が指摘した私自身のバグを捕まえられない**。

- **原因は同じ罠の三度目**: `cofcMix[i]` を `cofMix` の行から導出したため、$x_{13}=x_{12}^{-1}c\,x_{23}^{-1}$ が**再び同語反復**になった。修理版(`scratchpad/wd4_fix.g`: $\mathrm{cofc}[i]$ を独立に決めた $\pi(c)$ と比較)も **識別力 false**。
- **実際に識別力をもっていたのは別の検査**: 主測定の **「$T$ が $B_4$ 表現か」= 整合 20/20 vs 混成 4/20**。要件 (b) の趣旨(規約混成を機械で殺す)は**この検査が実質的に果たしている**。
- **残件**: `gtpi_pb4_gate_stdwindow_20260801.g` L35 型のバグ(fwd 生成元 × rev 行順で $\lvert Q_P\rvert$ が 7500→60)を**直接**捕まえる WD は**未発見**。⟹ **【GAP-WD-1】として登録**し、便 98 の監査点に載せる。

---

## 3. ★ 司令塔 追加条件 (c)(cc 空虚性)への回答 — **この窓では空虚ではない**

falsifier 指摘は「現行較正族は全窓で $c$ 像自明 ⟹ $c$ 項実装が未検査」だったが、実測は**部分的に否定**する。

| 量 | 値 |
|---|---|
| $\pi(c)=(s_1s_2)^3$ の位数(**周囲の $E$**) | **1** |
| $\mathrm{cofc}[1..5]$($c$ の 5 成分像) | `[ (), (), (1,2,3,5,4), (1,2,5,4,3), (1,2,3,5,4) ]` |
| $\Psi(c)$ の位数($Q_P$ 内) | **5** |

**成分 3・4・5 で $c$ の像は非自明**(位数 5)。よって `Chk6` の $c$ 項は**この窓で実際に走っている**。空虚なのは「周囲の $E$ での $\pi(c)$」だけである。
⟹ **(c) の緊急度は下がる**。ただし「成分 1・2 で $c\mapsto1$」は事実なので、**$\phi_{123},\phi_{234}$ 経路の $c$ 項は未検査**。この限定つきで便 98 に起票する(新規較正窓の作成は据え置き)。

---

## 4. 格付けと残件

| 主張 | 格 |
|---|---|
| $N_0\in\mathrm{NFI}_{PB_4}(B_4)$ が存在($\sigma_3\mapsto s_1$・$E$ 内一意) | **機械**(手 1) |
| $N_{PB_3}(N_0)=K_\pi$・$\lvert PB_3/K_\pi\rvert=7500$ | **機械** + 裁定 370(literal 一致・核厳密一致) |
| $\mathrm{GT}^\heartsuit(N_0)=\mathcal G$(20 行・悉皆) | **機械**(補題 UNIV の $c_4$ 崩落による悉皆性は紙) |
| **20/20 settled$^{PB_4}$・$N_0$ isolated・$N^\sharp=N_0$** | **機械**(単系統) |
| **定理 GTPI$^{PB_4}$**($\mathrm{GT}(K_\pi)\cong F_{20}$ が $PB_4$ 水準) | **紙(定理 GTPI)+ 機械(本走)**。**単系統・CV-9 主検問前・Sol 監査前** |
| 【GAP-WD-1】混成を直接殺す WD が未発見 | **未解決** |
| $\phi_{123},\phi_{234}$ 経路の $c$ 項 | **未検査**(§3) |
| $c_5$ の混成向き(所見 C5-ORIENT) | **erratum 済・この窓では空虚**・別窓前に修理 |

**Sol への監査点(便 98)**: (F) 窓の由来 → 裁定 370 で閉鎖済として提示。(G) **$T^{PB_4}$ の共役の向き**(整合 $v(\cdot)v^{-1}$ の採択根拠 = Rev 規約の転送)。(H) **【GAP-WD-1】**。(I) §3 の $c$ 項の射程。
