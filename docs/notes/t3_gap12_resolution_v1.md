# T3-GAP-1 / GAP-2 の決着 — 走査パラメータの置換(裁定 1051)

作成: 数学者(Opus 5)/ 2026-08-13 / 発注 = 司令塔(R-1 クリティカルパス)
対象 = `t3_spec_and_C2_calib_v1.md` 第 I 部 §4(極点走査)/ Sol 便 113(t3 $m=4$・$\Pi_0=-Q_0$ で空)
⚠ $u$/$c$ 非接触・prereg 非抵触。

---

## §0 結論(2 行)

1. ★★★ **T3-GAP-1(「$m$ の上界」)は解くべき問題ではありません** — **$m$ 走査というパラメータ化そのものが誤り**でした。正しい走査対象は **Tschirnhaus 束 $\mathcal E$**($E$ 上 rank 2)で、その次数は **RH により $\deg\mathcal E=3$ に一意固定**されます ⟹ **停止保証は「上界」ではなく「次数の固定 + $\mathrm{Pic}$ の 1 次元走査」から出ます**。
2. ★★ **T3-GAP-2**: Sol 113 の「$m=4$・$\Pi_0=-Q_0$ で空」は **$\mathcal E$-moduli の 1 点**にすぎません。全極点・全 $m$ への拡張は不要で、**$\mathcal E$-moduli 上の走査へ置換**するのが正しい。

---

## §1 ★★ 正しい走査パラメータ

$\pi:W_9\to E$(次数 3・$E$ は genus 1)に対し
$$\pi_*\mathcal O_{W_9}=\mathcal O_E\oplus\mathcal E^{\vee},\qquad \mathcal E=\text{Tschirnhaus 束(rank 2)}$$
**標準事実**: 分岐因子の次数 $=2\deg\mathcal E$。

RH: $2\cdot4-2=3(2\cdot1-2)+R\Rightarrow R=6$。分岐の内訳(検分済): $Q_0,Q_\infty$($e=3$・寄与 2 ずつ)+ $B_1,B_2$($e=2$・寄与 1 ずつ)$=6$ ✔

$$\boxed{\ \deg\mathcal E=\frac{R}{2}=3\qquad\textbf{— RH で一意に固定(走査対象ではない)}\ }$$

⟹ ★ **$z^3+Az+B$ の係数の住処は $\mathcal E$ が決めます**。$A,B$ を「$L(m\Pi_0)$ の元」と書くのは、**$\mathcal E$ を 1 点の倍数で無理に表した歪み**です。

---

## §2 ★★★ conductor は**湧きません**($\delta=0$ が強制)

$\mathcal D:=-4A^3-27B^2$ は $(\det\mathcal E)^{\otimes2}$ の切断 ⟹ $\deg\mathcal D=2\deg(\det\mathcal E)=2\cdot3=6$。
一方、私の重複度公式より $\deg\mathcal D=\underbrace{6}_{\text{分岐}}+2\delta$。
$$\boxed{\ \Longrightarrow\ \delta=0\ \textbf{が強制される — 正しい }\mathcal E\ \textbf{を取れば conductor は湧かない}\ }$$

⟹ ★ 旧設計の $\deg C=(3m-6)/2$(= $m$ が増えるほど conductor 点が増える)は**パラメータ化の歪みの産物**であって、幾何の性質ではありませんでした。⟹ **ideator 札 3 の破綻点 (ii)(conductor の湧き)も同時に解消**します。

---

## §3 ★ 走査空間(有限次元・停止保証つき)

$E$ は楕円曲線 ⟹ **Atiyah の分類**が使えます。rank 2・$\deg3$ の束:

| 型 | 記述 | パラメータ |
|---|---|---|
| **(a) 分解型** | $\mathcal E=L_1\oplus L_2$、$\deg L_1+\deg L_2=3$ | 各 $L_i\in\mathrm{Pic}^{d_i}(E)\cong E$ ⟹ **2 次元**(ただし $\det$ 固定で 1 次元) |
| **(b) 非分解型** | $\gcd(2,3)=1$ ⟹ ★ **存在**。$\det$ で $\mathrm{Pic}^3(E)\cong E$ に parametrize | **1 次元** |

⟹ ★ **どちらも低次元の族**。⟹
$$\boxed{\ \textbf{停止保証} = \textbf{「}\deg\mathcal E=3\ \textbf{の固定(RH)」} + \textbf{「}\mathrm{Pic}\ \textbf{の 1 次元走査」}\ }$$
⚠ **「$m$ の上界」という問いは消滅**します(T3-GAP-1 は**問題の消滅として閉鎖**)。

### 3.1 分解型の型の絞り込み
$(\deg L_1,\deg L_2)$ は $\{(0,3),(1,2),(2,1),(3,0)\}$(負次数成分は切断が消えて退化)。⟹ **順序を除き 2 型**: $(0,3)$ と $(1,2)$。
★ さらに $A,B$ の**非零性**と $Q_0,Q_\infty$ での**全分岐条件**($A(Q_0)=0$・$\mathrm{ord}_{Q_0}B=1$)が型を絞ります ⟹ **実装係の一手目**(§5)。

---

## §4 ★ Sol 113 の実測の位置づけ(T3-GAP-2 の答え)

「$m=4$・$\Pi_0=-Q_0$ で空」は、$\mathcal E$ を $\mathcal O(4\Pi_0)$ 系で表した **分解型の特定の 1 点**(次数と類の両方を固定)にあたります。
$$\boxed{\ \Longrightarrow\ \textbf{全極点・全 }m\ \textbf{への拡張は}\textbf{不要}\ \textbf{— }\mathcal E\textbf{-moduli 上の走査へ置換する}\ }$$
⚠ **$m$ 走査の上界を探すのは、誤ったパラメータ化を延命させる作業**です。
★ **CRT-C2 の構造簡約が先か**という問いへの回答: ⟹ ★ **どちらでもなく、$\mathcal E$ 走査が先**。CRT-C2(層 $(0,5)$)は $w$-line 車線の話で、t3 車線とは**独立**です(検分 §0 の「札 3 ∥ [札 1→札 6]」は不変)。

---

## §5 次走査仕様(実装係 / Sol へ直結)

```
=== [P1-D2] t3 車線 — Ê-moduli 走査(m 走査の置換)===
根拠: docs/notes/t3_gap12_resolution_v1.md / 前提 = E の明示モデル(w9_E_model_v1 + v1.1)

[D2-0] ★ 前提の再確認(秒)
  Ê の次数 = 3(RH: R=6 = 2·deg Ê)。★ δ=0(conductor なし)を assert。
  ⟹ deg D(= disc)= 6 ちょうど。これを走査の *不変条件* として全候補で検査。

[D2-1] 型の列挙(有限)
  (a) 分解型 Ê = L_1 ⊕ L_2、(deg L_1, deg L_2) ∈ {(0,3),(1,2)}(順序を除く)
  (b) 非分解型(Atiyah・det で Pic^3(E) ≅ E に parametrize)
  ★ 各型で A ∈ H^0(Sym^2 系), B ∈ H^0(det 系) の次元を RR で出す(E は genus 1 ⟹ dim = deg for deg≥1)

[D2-2] 分岐条件(§I.3 の逐語・不変)
  Q_0, Q_inf で全分岐: A(Q_0)=A(Q_inf)=0 かつ ord_{Q_0}B = ord_{Q_inf}B = 1
  B_1, B_2 で単純分岐: disc の単根
  ★ 群法則の無料拘束: 2Q_0 ⊕ 2Q_inf ⊕ B_1 ⊕ B_2 = O(δ=0 ゆえ conductor 項が消える ⟹ 前版より 1 項少ない)

[D2-3] 走査
  各型について Pic の 1 次元パラメータを走らせ、Gröbner で解を求める
  ⚠ 実装条件(不変): B_3+B_4 は F_9-有理因子として扱う(個点を取らない)

[D2-4] 見張り(★ 走らせる前から確定)
  (E-a) ★ deg D = 6 ちょうど。7 以上なら Ê の取り方が誤り ⟹ 即停止
  (E-b) ★ δ = 0。conductor が湧いたら §2 と矛盾 ⟹ 即停止
  (E-c) 得た W_9 の genus = 4(重複度公式 = D8 の条件付き形で確認)
  (E-d) ord(P_0-P_inf) = 9
  (E-e) 全型で解ゼロ ⟹ ★ 「W_9 → E の次数 3 被覆は存在しない」= 一級の否定的結果
        ⟹ [P1-0b] の分岐内訳(私が独立検算 PASS)と矛盾するので、その場合は
        ★ E の同定(Nielsen 指紋 = 位数36・ブロック系(3,2)・deck 自明)を再検査せよ

出力: cert (schema r13-p1d2/v1)。記録: Ê の型・Pic パラメータ・deg D・δ・解の個数・(E-a)〜(E-e)・u_touched=false
```

---

## §6 GAP・記帳

- **【T3-GAP-1】★ 閉鎖**(問題の消滅: $m$ の上界は不要 — $\deg\mathcal E=3$ が RH で固定)。
- **【T3-GAP-2】★ 閉鎖**(Sol 113 は $\mathcal E$-moduli の 1 点 ⟹ 走査空間を置換)。
- **【T3-GAP-3】(小・新)** Atiyah 分類(楕円曲線上の rank 2 束)は**正典外の標準事実**。⟹ ★ **自前再導出可能な水準**(rank 2・deg 奇の非分解束の存在と $\det$ による parametrize)⟹ **文献要請は不要**と判定。⚠ ただし cert には「標準事実として使用・自前再導出は未記載」と申告すること。
- **【T3-GAP-4】(小・新)** $\pi_*\mathcal O=\mathcal O\oplus\mathcal E^\vee$ と「分岐次数 $=2\deg\mathcal E$」も標準事実。⟹ 同上。
- ★ **記帳(m1051-1)**: 私の `t3_spec_and_C2_calib_v1.md` §4 は、**極点を 1 点の倍数 $m\Pi_0$ に取る**という**恣意的なパラメータ化**を導入し、その結果 conductor $(3m-6)/2$ という**幻の量**を生みました。⟹ ★ **教訓 T-1**(提案): **被覆の係数の住処は「勝手な因子」でなく被覆自身が決める束($\pi_*\mathcal O$ の構造)で書く**。歪んだパラメータ化は**存在しない停止問題**を作る。
- **申告**: 走行ゼロ・$u$ 非接触・**Sol 未監査**・**verified ではない**(candidate 格)。
