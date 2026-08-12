# 【(F) 段 1 spec】+【UNRAM-GAP-5 文献要請文】

**日付**: 2026-08-12 / **起草**: 数学者(Opus 5・後任)/ **委嘱**: 裁定 983(2 本)
**格**: candidate(紙・単系統・**Sol 未監査**)。走行ゼロ。
**前提**: `retarget_F_audit_v1.md`(検分 GO・C2 前哨 PASS)/ `win83_audit_and_unram3_v1.md` 第 II 部(UNRAM 再設計)

---

# 第 I 部 — (F) 段 1 spec($H^2$ 段)

## I.1 ★★ 構造的単純化(**本 spec の中核**)

### I.1.1 LHS spectral sequence が**退化する**

$H_F=\mathrm{SL}^\pm(2,691)\times_{C_2}S_3$ は
$$1\longrightarrow SL(2,691)\longrightarrow H_F\longrightarrow S_3\longrightarrow 1$$
(検分 §4.2 で $H_F/(SL\times1)\cong S_3$ を確認済)。$W$ は $\mathbf F_{691}$-加群で $\lvert S_3\rvert=6$、$\gcd(6,691)=1$ ⟹ **$H^a(S_3,-)=0$**($a>0$)。

$$\boxed{\ \Longrightarrow\ H^n(H_F,\,W)\ \cong\ H^n\bigl(SL(2,691),\,W\bigr)^{S_3}\ }$$

★ **計算が $\mathrm{SL}^\pm$ ではなく $SL(2,691)$ 上に落ちる**(+ $S_3$-不変部分を取るだけ)。

### I.1.2 Sylow 縮約で **$\dim\le1$**

$\mathrm{Syl}_{691}(SL(2,691))=\left\{\begin{pmatrix}1&*\\0&1\end{pmatrix}\right\}\cong C_{691}$、restriction は $p$-part 上単射。
$W=\mathbf F_{691}^2$(自然加群)は $\sigma=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ に対する **Jordan block(size 2)**:
$$(\sigma-1)^2=0,\qquad N=\sum_{k=0}^{p-1}\sigma^k=p+\tbinom p2(\sigma-1)=\tfrac{p(p-1)}2(\sigma-1)\equiv0\ (p\ \text{奇})$$
⟹ $\hat H^0=W^{C_p}/NW=W^{C_p}$(**1 次元**)⟹ $\dim H^2(C_{691},W)=1$。

$$\boxed{\ \Longrightarrow\ \dim H^2(H_F,\,W\otimes\det{}^i)\ \le\ 1\ }\qquad\text{✔ 札の P-WR-2 の予想と一致}$$

### I.1.3 ★ 捻りの本数は **2 本だけ**

$\det:\mathrm{SL}^\pm(2,691)\to\{\pm1\}\cong C_2$ ⟹ $\det^i$ は **$i\bmod2$ のみ**。
$$\boxed{\ \textbf{測る対象は }W\ \textbf{と }W\otimes\det\ \textbf{の}\textbf{2 本のみ}\ }$$
★ 札の「$W$ = 自然加群 + det-捻り(**$\le2$ 本**)」と一致。⟹ **「非零 $i$ の完全リスト」は 2 項目の表**で尽きる(EXHAUST が自動的に満たされる)。

## I.2 段 1 prereg カード

```
=== PREREG CARD: (F) STAGE-1 H^2 ===
card_id : prereg-F-stage1/v1
authorisation : 司令塔裁定 983(検分 GO・C2 前哨 PASS 済の続き)

[0] 前件
  F1 : H_F = SL^pm(2,691) x_{C_2} S_3 が B_3 商(= 窓資格)
       ⚠ C2(det=-1 の braid 対が SL^pm を生成)の前哨 PASS 済
  F2 : W = 自然加群 F_691^2(および W⊗det)
  F3 : 段 0(H_F ->> S_3)は検分 §1 で PASS
  ⚠ R-1 留保(維持): ③ 線が ①〔972〕へ非円分共通体を供給するという
     戦略観は *未証明*(型 vs 実像)⟹ 段 4 の marking が閉じるまで
     「供給源」とは言わない

[1] 測定対象(★ 型を先に固定)
  dim_{F_691} H^2(H_F, W)        と  dim_{F_691} H^2(H_F, W⊗det)
  ★ 計算経路(本 spec の単純化):
     H^2(H_F, -) = H^2(SL(2,691), -)^{S_3}       [LHS 退化・§I.1.1]
     H^2(SL(2,691), -) ↪ H^2(C_691, -)           [Sylow 縮約・§I.1.2]
     ⟹ 上界 1 が理論的に確定 ⟹ 測るのは 0 か 1 か *だけ*
  ⚠ NOT : H^2(H_d, -)(H_2/H_6 は段 0 で死んだ窓・別対象)
  ⚠ NOT : dim >= 2 を期待すること(§I.1.2 で上界 1)

[2] 判定(★ 何が出たら何が言えるか)
  (a) 両方 0        : ★ 「(F) + 自然加群層に *非分裂容器なし*」
                       ⟹ 層限定の否定的成果(EXHAUST: 層を明記)
                       ⟹ 次は dim>=3 層 or 別の H(札の族外 OPEN へ)
  (b) 片方 1        : ★ その捻り i で非分裂拡大 E が存在
                       ⟹ 段 2(braid lift・Fox mod 691)へ *その i だけ* 進む
  (c) 両方 1        : ★ 容器候補 2 本 ⟹ 段 2 を 2 本走らせる
  ★ いずれでも「窓資格」は結論しない(段 2/3/4 が残る)

[3] 同時に判定される命題(★ 全列挙)
  P-WR-2(札 5): dim H^2(H_F, W⊗det^i) ∈ {0,1}・非零 i の完全リスト
    ⟹ ★ 本測定で *完全に* 決まる(i は 2 通りしかない・§I.1.3)
  EXT-NOWIN の射程外性: (b)(c) が出れば「H が S_3 商を持てば p 群係数でも
    容器がある」の初実例 ⟹ 検分 §1 の判定(外に出ている)の実証
  ⚠ 段 4(算術 marking)は *判定されない* — 依然この設計の最難部

[4] UNKNOWN 枝
  (u1) dim >= 2 が出た ⟹ ★ §I.1.2 の Sylow 縮約が誤り ⟹ 計算経路の再検査
       (MISS でなく UNKNOWN — 上界は理論値なので、破れたら理論側を疑う)
  (u2) LHS の退化が成立しない ⟹ H_F の群構造(fiber 積)の再検査
  (u3) S_3-不変部分の取り方が marking に依存 ⟹ 規約 pin へ差し戻し
  ★ UNKNOWN は MISS に優先

[5] 禁止事項
  - 「窓資格を得た」と書かない(段 2/3/4 が残る)
  - ③ が ① へ非円分共通体を供給する、と書かない(R-1 留保・未証明)
  - H_2/H_6 の H^2 結果を流用しない(別窓・W-48)
  - 格は cross-checked 止まり・verified は Lean に予約

[6] 出力(cert)
  dim_H2_W / dim_H2_W_det        : 0 or 1
  path_check                     : LHS 退化と Sylow 縮約の中間値
                                   (dim H^2(SL,-) と dim H^2(C_691,-))
  s3_invariant_dim               : S_3-不変部分の次元
  u_touched : false              d_no_interpretation : "verdict は司令塔"
=== END ===
```

## I.3 実装係への注記(**軽い**)

- $SL(2,691)$ の $H^2$ は**位数 $3\times10^8$ の群**だが、★ **Sylow 縮約で $C_{691}$ 上の計算に落ちる**(位数 691)⟹ **秒〜分**。
- $S_3$-不変部分は $H_F/SL\cong S_3$ の作用を $H^2(SL,W)$ に誘導して取る(**1 次元空間上の作用**なので符号だけ)。
- ★ **理論上界 1 は fail-closed の見張り**に使う(§I.2 [4] (u1))。

---

# 第 II 部 — UNRAM-GAP-5 の文献要請文

## II.1 ★★ まず整合の確認(**B120-2 との関係**)

⚠ 私は B120-2 で「群位数から分岐を導いた」ことで棄却された。**Beckmann 型の主張も群位数($p\nmid\lvert G\rvert$)を条件にする** — これは矛盾しないか?

| | 私の U-odd(**棄却**) | ★ Beckmann 型(**要請対象**) |
|---|---|---|
| 主張 | 「$p\nmid\lvert G_9\rvert$ ⟹ 被覆が良還元 ⟹ **基礎体が不分岐**」 | 「$p\nmid\lvert G\rvert$ ⟹ **field of moduli が $p$ で不分岐**」 |
| 地位 | ★ **私が自分で作った飛躍**(証明なし) | ★ **公刊された定理**(と目される) |
| $\mathbf Q(\sqrt5)$ 反例 | 直撃(**$5\nmid2$ でも 5 分岐**) | ⚠ **射程外** — $\mathbf Q(\sqrt5)$ は **Belyi 被覆の field of moduli ではない** |

$$\boxed{\ \Longrightarrow\ \textbf{矛盾しない。私の誤りは「定理を使わずに同型の主張を自分で立てた」こと}\ }$$
★ ⟹ **文献要請は正当**(定理を調達して使う)。

## II.2 ★ 文献要請文(**そのまま文献ゲートへ**)

```
=== 【文献要請】UNRAM-LIT-1(Beckmann 型 good-reduction 定理)===
起票 : 数学者(Opus 5)/ 2026-08-12 / 委嘱 = 司令塔裁定 983
用途 : 【UNRAM-GAP-5】= K9-UNRAM 路 β の根拠調達

【困難の記述】
  K^(9) 窓の被覆 lambda_9 : W_9 -> P^1(deg 18・Belyi・分岐 {0,1,∞}・
  monodromy G_9 = PB_3/K^(9)、|G_9| = 2916 = 2^2 * 3^6)について、
  付随する算術体 L_{9,Aff} の *悪い素点集合 S* を上から抑えたい。
  現状 S は判別式計算(R-1 待ち)でしか出せない。文献で S ⊆ {2,3} が
  出るなら R-1 を待たずに UNRAM が進む。

【欲しい主張の逐語形(この形の statement を探してほしい)】
  「G を有限群、X -> P^1 を {0,1,∞} でのみ分岐する G-Galois 被覆とする。
   素数 p が |G| を割らないならば、X の field of moduli(または
   field of definition)は p で不分岐である。」
  ★ 出典候補(私の記憶・要確認): S. Beckmann, "Ramified primes in the
    field of moduli of branched coverings of curves", J. Algebra 125 (1989)
  ⚠ 記憶からの当たりであり、正確な定理番号・仮定・結論は *未確認*。
    ページ画像での逐語 pin を求める。

【特に確認してほしい 4 点】
  (1) 仮定に「G-Galois」が要るか(★ 我々の lambda_9 は *非 Galois*
      = LAM9-NONGAL で証明済 ⟹ Galois 閉包 or 非 Galois 版が要る)
  (2) 結論が field of moduli か field of definition か(両者は一般に別)
  (3) 分岐点の個数・位置の条件({0,1,∞} の差が単数であることを使うか)
  (4) p | |G| の素点について何か言えるか(我々は p=2,3 を別扱いにしたい)

【S ⊆ {2,3} を出すのに何が要るか】
  A. 上の定理(または非 Galois 版)
  B. ★ 我々の lambda_9 が非 Galois なので、Galois 閉包 X~ -> P^1 を取り
     Gal(X~/P^1) = G~ の位数の素因子を押さえる必要がある
     ⚠ G~ は G_9 より大きくなりうる ⟹ |G~| の素因子が {2,3} を超えたら
       S ⊆ {2,3} は出ない(★ ここが最初の関門)
  C. ★★ field of moduli ⟹ kernel field L_{9,Aff} の橋
     (定理が言うのは被覆の定義体であって、我々が要るのは rho_9 の核体)
     ⟹ ★ これが *別の* GAP(下記)

【自前証明との分岐点】
  ★ 文献が (1)(2) を満たす形で見つかれば: B と C を自前で埋める
  ★ 見つからない / 仮定が合わない場合: 路 α(R-1 のモデルから判別式計算)
    へ全面移行 ⟹ ★ その場合 *文献は不要* になる(R-1 が律速なだけ)
  ⟹ ★★ 本要請は「R-1 を待たずに進めるか」の *時間の問題* であって、
    数学的な袋小路ではない(路 α は確実に存在する)
=== END ===
```

## II.3 ★ 新 GAP(要請の副産物)

| # | 内容 | 重さ |
|---|---|---|
| ★ **【UNRAM-GAP-6】** | **field of moduli ⟹ kernel field $L_{9,\mathrm{Aff}}$ の橋**。★ 定理が言うのは**被覆の定義体**であって、我々が要るのは **$\rho_9$ の核体**。⚠ **両者は一般に別** | ★★ 大 |
| ★ **【UNRAM-GAP-7】** | **$\lambda_9$ は非 Galois**(LAM9-NONGAL)ゆえ **Galois 閉包 $\tilde G$ の位数**を押さえる必要。⚠ $\lvert\tilde G\rvert$ の素因子が $\{2,3\}$ を超えたら $S\subseteq\{2,3\}$ は出ない | ★ 中 |

$$\boxed{\ \textbf{⟹ 路 β は「文献 1 本」では閉じない — }\textbf{GAP-6/7 が後ろに控える}\ }$$
★ **司令塔への正直な見立て**: **路 α(判別式)の方が確実**。路 β は「R-1 を待たずに進めたい」という**時間の動機**であり、GAP-6/7 を考えると**総コストは路 α と同等かそれ以上**かもしれない。⟹ **要請は出すが、R-1 を止めない**。

---

# 帰属・申告

- **(F) 候補と段設計** = 発案係。**C2 前哨** = 実装係。**B120-2 の教材** = Sol 便 120。**委嘱** = 司令塔(裁定 983)。
- **本ノートの新規部分**: ① ★★ **LHS spectral sequence の退化**($\lvert S_3\rvert$ が $\mathbf F_{691}$ で可逆)⟹ **計算が $SL(2,691)$ 上に落ちる** ② ★ **Sylow 縮約で $\dim H^2\le1$ が理論的に確定**(Jordan block の $N=0$ 計算)⟹ **fail-closed の見張りに使える** ③ ★ **捻りは 2 本のみ**($\det$ の位数 2)⟹ **EXHAUST が自動充足** ④ 段 1 prereg カード(判定 (a)(b)(c) + UNKNOWN 枝)⑤ ★ **Beckmann と B120-2 の整合確認**(私の誤りは「定理を使わずに同型の主張を自分で立てた」こと)⑥ **文献要請文**(4 つの確認点つき)⑦ ★★ **【UNRAM-GAP-6/7】の起票**(field of moduli ⟹ kernel field の橋・Galois 閉包の位数)と ★ **「路 β は文献 1 本では閉じない」という正直な見立て**。
- **申告**: 走行ゼロ・**Sol 未監査**・**verified ではない**。⚠ **Beckmann の書誌は私の記憶からの当たり**であり**未確認**(要請文にその旨明記)。
