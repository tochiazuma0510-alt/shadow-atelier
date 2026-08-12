# 【TOWER 修理 ②】(5′) は既調達 — ★ **COMPOSE-GAP-1 は matched 実装だけで全閉** + 路② + UNRAM 設計

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5・後任)/ **委嘱**: 裁定 962(指示 3 件)
**格**: candidate(紙・単系統・**Sol 未監査**)。走行ゼロ。
**前版**: `tower_repair_v1.md`(路①・fixed-window 化)— ★ **本版は §6【TOWER-GAP-1】を撤回する**

> ## ★★★ 指示 1 の判定
> $$\boxed{\ \textbf{肯定 — }(5')@\alpha=1\ \textbf{は }B\text{-}1\ \textbf{の }(5'^b)\ \textbf{に含まれ、}\textbf{既調達}\ }$$
> ⟹ **COMPOSE-GAP-1 は matched 実装だけで全閉**(調達不要)。⚠ **私の v1 §6【TOWER-GAP-1】は誤り** — p1-check-past-first を踏んだ(**同日 4 回目**)。

---

## §1 ★★ 指示 1 — 既調達の確認(索引 → カプセル → 裁定)

### 1.1 一次記録(逐語・**索引 §3 と §5**)

| # | 記録 | 出所 |
|---|---|---|
| 1 | **B-1**(枠組み相対橋: $\operatorname{ord}([u_n])=n\to\operatorname{ord}(a_n)=n$)= 「**(5′) の TB 相対格で閉**: 条件付き PASS(**501**)→ 条件履行 v2.1(**504**)→ **PASS 格確定**(便 104 **F104-3.1**「TB v2.1/(5′) PASS・格据え置き」)」 | 索引 §3 |
| 2 | ★★ **(d1)**($\operatorname{ord}(a_n)=n\Rightarrow$ 像形)= **R$^{\rm cyc}$ + MATCH-one + (5′$^b$) 相対** → ★ **FAM-U-ASM 発効に内包** | 索引 §5(裁定 **495** → 516) |
| 3 | **APPLY-fam + MATCH-one/ORD-IDX** = **Sol PASS(条件文として)**・正本 `match_one_supply_v1.md` | 索引 §5(裁定 **490**・便 102 F102-5.2) |
| 4 | **定理 SIXP-fam**((6′) 族版)= 全奇 $n\ge3$・**全 $\alpha\ne0$** で紙成立(**枠組み層不使用**)→ **Sol PASS = 発効** | 索引 §5(裁定 484 → **490**) |
| 5 | 格(逐語)= `theorem-framework-relative [TB: canonical-source-pinned/v2]`(… **required bridge form = uniform (5′$^b$), not exact (5′)**) | 索引 §0 |

### 1.2 ★★★ 判定 = **含まれる**

**T63 の接続**(fixed-window class $\operatorname{ord}(a_9)=9$ → 算術 $d_9$)は、記録 2 の **(d1) そのもの**である。そして (d1) は
$$\text{(d1)} = R^{\rm cyc}_{\rm formal}\ +\ \textbf{MATCH-one}\ +\ (5'^b)\ \textbf{相対}\ \longrightarrow\ \textbf{FAM-U-ASM 発効に内包}$$
と記録されている。⟹ **接続に要る (5′) は uniform (5′$^b$) で足り、それは B-1 として閉じている**(記録 1・5)。

$$\boxed{\ \Longrightarrow\ \textbf{exact }(5')@\alpha=1\ \textbf{の個別調達は}\textbf{不要}\ \textbf{。}\textbf{要求形が }(5'^b)\ \textbf{だから}\ }$$

### 1.3 ★ matched 量化は**自動的に満たされる**

MATCH-one は「(5′) と (6′) を**同じ一つの窓で取る**」ことを要求する。

| 前件 | 成立範囲 |
|---|---|
| **(6′)** | ★ **全奇 $n\ge3$・全 $\alpha\ne0$**(SIXP-fam・記録 4・**枠組み層不使用**) |
| **(5′$^b$)** | ★ **uniform 形**(記録 5)= 窓一様 ⟹ B-1 の閉で全窓 |

⟹ **両方が全窓で成立する** ⟹ **どの窓を選んでも matched** ⟹ ★ **窓 $H_{2,1,0}$($\alpha=1$)を選ぶだけで matched 条件は満たされる**。

$$\boxed{\ \textbf{【COMPOSE-GAP-1】= }\textbf{全閉}\ \textbf{(残るのは「}\alpha=1\ \textbf{を選んだと明記する」matched 実装のみ)}\ }$$

### 1.4 ⚠★ NAME-COLLIDE 登録(**司令塔の指示どおり 1 行**)

$$\boxed{\ \textbf{exact }(5')\ \textbf{と uniform }(5'^b)\ \textbf{は}\textbf{別物}\ \textbf{。FAM-U-ASM/(d1) が要求するのは}\textbf{後者}\textbf{で、それは既調達}\ }$$
⟹ 今後 **「(5′)」と書くときは exact / uniform($^b$)を必ず区別**する。c2c4 の **C3**(= $B_{\rm FC}$ の $n=9$ instance)は **exact 側**の札であり、**(d1) の要求ではない**。

### 1.5 ⚠⚠ 自己申告 — **p1-check-past-first を同日 4 回目に踏んだ**

`tower_repair_v1.md` §6 で私は【TOWER-GAP-1】=「**(5′)@$\alpha=1$ の調達**」を「★★ 大」の GAP として立てた。**誤り**である。

| 私が見たもの | 見るべきだったもの |
|---|---|
| LEDGER **1942**(2026-08-04): 「残る本丸 = (5′) = 橋 B-1 = **調達が文字どおり律速**」 | ★ その**翌日**の裁定 **501→504→515/520**(便 104 F104-3.1)で **B-1 は閉じている** |

⟹ ★ **私はまた「その時点のスナップショット」を現在形として読んだ**(RECON v1 の stale 読みと**同じ失敗型**)。**W-43(鮮度を一次台帳で確認せず断じる)を自分で踏んだ**。
★ **教訓の更新**: 「LEDGER の日付つき記述を引くときは、**その後の裁定で supersede されていないか**を必ず後方走査する」。⟹ **W-43 の運用細則**として v1.4.9 へ。

---

## §2 指示 2 — 路②(接続)の**条件文明示化**

> ### 命題 **T63-CONNECT**(candidate / framework-conditional・条件文)
> **固定**: 窓 $H_{2,1,0}$($\alpha=1$)。
> **前件**:
> 1. **(6′)@$\alpha=1$** — ★ **閉**(SIXP-fam・枠組み層不使用)
> 2. **(5′$^b$)** — ★ **閉**(B-1・**TB 相対格** `theorem-framework-relative [TB: canonical-source-pinned/v2]`)
> 3. **MATCH-one** — ★ **供給済**(`match_one_supply_v1.md`・Sol PASS 条件文)
> 4. **$R^{\rm cyc}_{\rm formal}$** の残り前件 (0)(1)(2)(3) — 既存(C1 閉・C2 閉・$e=9$ 正典・(6′) 閉)
>
> **結論**:
> $$\boxed{\ \operatorname{ord}(a_9)=9\ \ (\textbf{fixed window }H_{2,1,0})\quad\Longrightarrow\quad d_9=9\ \ (\textbf{= }\rho_9\ \textbf{全射 = Conj 5.1@}n=9)\ }$$
> ⚠ **格**: `framework-conditional`。**TB 層(TB1–TB4・canonical-source-pinned/v2)+ FAM-U-ASM の残余 6 項(W2-fam/W5/Λ-REG/(M-b)/ASM-α/始点算術)を継承**。
> ⚠ **無条件ではない**(**M119-5** の指摘は生きている)— 無条件なのは **$d_9=\lvert A_9\cap\mathfrak F_0\rvert$ まで**。

★ **本命題は (5′) 到着を待たずに書ける**(司令塔の見立てどおり)— **実際には既に到着していた**ので、**条件文ではなく発効した含意**として読んでよい。

---

## §3 指示 3 — UNRAM 修理②の設計(**奇素数先行・$p=2$ 切り離し**)

### 3.1 標的の分割(採択済み方式)

Sol 便 119 F3(e) 路②: 「各 $p\ne3$ について**二面体 quotient 自体の based inertia を直接計算**し、translation が 0 であることを示す。特に **$p=2$ は prime-to-$p$ specialization の素朴適用では落ちない**ので別段が必要」。

$$\boxed{\ \textbf{(K9-UNRAM)}\iff\forall p\ne3:\ t(I_p)=1\ \Longrightarrow\ \textbf{分割: }\ \underbrace{p\ \textbf{奇}\ne3}_{\textbf{U-odd}}\ \ +\ \ \underbrace{p=2}_{\textbf{U-2(別段)}}\ }$$

### 3.2 U-odd の設計(**先行**)

| 段 | 内容 | 根拠 / 状態 |
|---|---|---|
| **U-odd-1** | $p$ 奇 $\ne3$ ⟹ $\mathbf Q(\zeta_9)/\mathbf Q$ は $p$ で不分岐 ⟹ $\chi(I_p)\equiv1\pmod9$ ⟹ $t\vert_{I_p}$ は**準同型** | ★ 既証(UNRAM v1 §2.3 段 1) |
| **U-odd-2** | 暴分岐 $P_p$ は pro-$p$、$p\ne3$ ⟹ $t(P_p)=1$ ⟹ **$t\vert_{I_p}$ は従順商を経由** | ★ 既証(**K9-TAME**) |
| ★ **U-odd-3** | 従順商 $I_p^{\rm t}$ の**像**を二面体 quotient 側で**直接計算**する。$\lambda_9$ の $p$ での還元(**$p\nmid\lvert G_9\rvert=2^2\cdot3^6$ ⟹ $p\ge5$ で良還元**)から $\psi_9(f_g)$ の translation を読む | ⚠ **本体**。⚠ **W-47 を使わない**(pro-3 経由の橋は禁止) |
| **U-odd-4** | ⟹ $t(I_p)=1$($p\ge5$) | U-odd-3 待ち |

★★ **設計上の要点**: $\lvert G_9\rvert=2916=2^2\cdot3^6$ ゆえ **$p\ge5$ では $p\nmid\lvert G_9\rvert$** ⟹ **$G_9$-被覆が $p$ で良還元**する ⟹ **prime-to-$p$ specialization が素朴に効く**。⟹ ★ **$p\ge5$ は「$p=2$ が難しい」理由(SGA1 の $p'$-部分)を回避できる**。
⚠ ただし **$p=2$ は $2\mid\lvert G_9\rvert$** ⟹ **良還元の素朴適用が効かない**(Sol の指摘どおり)。

### 3.3 実装係への指示書(**U-odd の機械前哨**)

```
=== 作業指示: U-odd-3 の前哨(K9-UNRAM 修理②)===
根拠: 司令塔裁定 962 / 設計 = docs/notes/tower_repair_v2.md §3
⚠ 停止線: 「t(I_p)=1 を示した」と書かない。機械が出すのは下記の boolean/値のみ。
⚠ 禁止: W-47(交換子像が 3 群 ⟹ ambient pro-3 経由)を根拠に使うこと。

[U0] 前提の機械確認
  (a) |G_9| = |PB_3/K^(9)| を計算し 2916 = 2^2 * 3^6 を確認
  (b) p >= 5 の素数で p ∤ |G_9| であることを確認(自明だが fail-closed で)
  出力: cert (schema uodd0/v1)

[U1] 二面体 quotient の惰性像(小さい p から)
  対象: p = 5, 7, 11, 13 (奇・≠3・|G_9| を割らない)
  (a) psi_9 : F_2 -> D_9 の translation 座標を、p での還元データから読む設計を
      実装係が可能な形に落とせるか *設計可否の報告* を先に出す
      ⚠ ここは数学者(私)の設計が未完 — 実装前に往復が要る
  (b) 可能なら: 各 p で translation が 0 か否かの boolean
  出力: cert (schema uodd1/v1) または「設計未確定」の報告

[共通]
  u_touched : false        ★ u_9 の値には触れない
  d_no_interpretation : "machine values only; verdict は司令塔"
=== END ===
```

⚠★ **正直な申告**: **U-odd-3 の「直接計算」の具体形は私の設計が未完**。⟹ **[U1](a) を「設計可否の報告」として先に出させる**のが正しい順序(実装前の往復)。

### 3.4 U-2(別段)の見立て

$p=2$ は $2\mid\lvert G_9\rvert$ ゆえ良還元が使えない。★ **ただし K9-C2 が効く**: $L_9=L_{9,\mathrm{Aff}}(i)$ で **$\mathbf Q(i)$ が 2 で分岐する**ことは既知。⟹ **$L_9$ が 2 で分岐するのは織り込み済**で、問うべきは **$L_{9,\mathrm{Aff}}$ が 2 で分岐するか**。
⟹ ★ **$p=2$ は「$C_2$ 因子と translation を分離して測る」問題**に落ちる(罠 6 の再来)。**UNRAM v1 §3 の段 (5) を $p=2$ 用に書き直す**のが道筋。

---

## §4 会計・【GAP】

| 項目 | 修理前(v1) | ★ 本版 |
|---|---|---|
| **【COMPOSE-GAP-1】** | 「(5′)@$\alpha=1$ の調達」= ★★ 大 | ★★★ **全閉**(matched 実装のみ) |
| **【TOWER-GAP-1】** | ★★ 大 | ★ **撤回**(私の誤り・§1.5) |
| **【TOWER-GAP-2】**(路② 明示化) | ★ 中 | ★ **閉**(§2 の T63-CONNECT) |
| **K9-COMPOSE** | HOLD | ⟹ ★ **修理完了の候補**(Sol 検収待ち) |
| **【UNRAM-GAP-1】** | OPEN | **OPEN**(§3 で分割・U-odd-3 が本体) |
| ★ 新 **【UNRAM-GAP-3】** | — | **U-odd-3 の「直接計算」の具体形**(★ **私の設計が未完**) |

**帰属**: 指示・p1-check-past-first の適用 = 司令塔(裁定 962)。(d1)/MATCH-one/SIXP-fam/B-1 = 工房既存(裁定 484/490/495/504/516)。
**本ノートの新規部分**: ① **(5′)@$\alpha=1$ の既調達確認**((d1) の行が決定打)② ★ **matched 量化が自動充足であることの指摘**((6′) 全 $\alpha$ + (5′$^b$) uniform)③ **exact (5′) / uniform (5′$^b$) の NAME-COLLIDE 登録** ④ ★ **自己申告(p1-check-past-first 同日 4 回目・W-43 の運用細則)** ⑤ **T63-CONNECT の条件文** ⑥ **UNRAM の U-odd/U-2 分割設計**と ★ **$p\ge5$ で $p\nmid\lvert G_9\rvert$ ゆえ良還元が素朴に効く**という要点 ⑦ **U-odd-3 の設計未完の正直な申告**。
**申告**: 走行ゼロ・$u_9$ 非接触・**Sol 未監査**・**verified ではない**。
