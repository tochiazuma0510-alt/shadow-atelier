# 影工房 便 33 返信 — \(K^{(3)}\) 有限層 Lean 翻訳忠実性監査

## 総合判定

\[
\boxed{\textbf{要修正 3 行（Lean 2・CLAIMS 1、修理後 FAITHFUL）}}
\]

ここで「3 行」は statement 監査上の二項目と、台帳の射程表現一項目を指す。

1. `allT.Nodup` が無いため、`T_card`・`F0_card`・F22 の filter 長を
   \(T\)、\(\mathfrak F_0\) の**濃度**として読む最後のアンカーが一つ欠ける。
2. `T_chi_is_chiVal` は四つの値の**等号関係（同じファイバー）**しか固定せず、
   紙の
   \(\widetilde\chi(m,k)=2m+1\pmod {12}\)
   という**ラベル付きの値**までは述べていない。
3. CLAIMS W3-14d の「GT 接続」は広すぎる。Bridge が接続したのは
   正典パラメータ群 \(T\) と \(\Phi\)-像であり、Lean 内に GT や
   \(\mathrm{Ih}\) 自体はない。

数学的な誤定義、積・逆元の向き違い、量化子逆転、反例は見つからなかった。
上の二命題も現行定義について真であり、数学側で欠けているのは statement のみである。
現行 `Bridge.lean` は Opus 監査の構造的欠落 D-1・D-2 と
Conjugator 側 A-10 を正しく閉じている。

なお委嘱本文は「9 ファイル」と書くが、列挙されている対象は
`Bridge.lean` を含めて **10 ファイル**である。本便では列挙された 10 ファイルを
すべて対象にした。

---

## F1. 定義層

### F1.1 \(D_3\)、\(E\)、\(G_3\)

**PASS。**

- `D := Fin 3 × Bool` は \(r^a s^e\) の符号化である。
- `dmul` は
  \[
  (a,e)(b,f)=(a+(-1)^e b,\ e\mathbin{\mathrm{xor}}f)
  \]
  を逐語的に実装する。`dinv` も回転を \((-a,0)\)、鏡映を自分自身へ
  送る正しい逆元である。
- `E := D × D × D`、`emul`、`einv` は成分ごとの直積。
  `par` は三成分の reflection flag の xor、
  `inG := (par = false)` は正典の parity kernel である。
- `xb=(r,s,s)`、`yb=(rs,r,rs)`、
  `zb=(r^2s,r^{-1}s,r)=(r^2s,r^2s,r)` は (3.6) の逐語リテラル。
  `F3_marking` と Bridge の `F3_order_yb`/`F3_order_zb` を合わせると、
  marking と三元の位数 6 が揃う。
- `F6_G3_gen` は parity kernel と
  \(\langle\bar x,\bar y\rangle\) の両包含を、正典の
  \(J\)-コセット分解で述べる。従って Lean の `inG` は紙の \(G_3\) と同じ対象である。

### F1.2 \(\Phi\) の閉形

**PASS。**

`um`、`kappa3`、`X3=[0,2,3,5]` と

\[
\alpha_{v,t}(r^a)=r^{va},\qquad
\alpha_{v,t}(r^as)=r^{va+t}s
\]

は v3 §2.5 と一致する。`Phicf` の三成分は

\[
(v_1,t_1)=(u_m,1-4k-u_m),\quad
(v_2,t_2)=(u_m,0),\quad
(v_3,t_3)=(1-2\kappa(m),0)
\]

そのものである。`F18_closed_form_matches` は正典の生成元像を別定義
`canonX`/`canonY` と比較しており、閉形を仮定として密輸していない。
`F20_hom`、`F20_bijective`、parity 保存を合わせれば、対象の 12 写像は
\(G_3\) の自己同型である。

### F1.3 \(H\)、\(\Lambda\)、\(\tau\)、\(\rho_\Lambda\)

**PASS。**

`inHc c v` は

\[
v_2\in\langle r\rangle,\qquad v_3=c\,v_1c^{-1}
\]

であり、`inH = inHc done` は紙の
\(H=\{v\mid v_1=v_3,\ v_2\in\langle r\rangle\}\)。
`F10_conj_rule` の添字
\(g_3cg_1^{-1}\)、`tauAct` の
\((\bar x^j)_3c(\bar x^j)_1^{-1}\)、`rhoF0` の \(cr^{-k}\) は
すべて正典 N2/N4 と同じ向きである。

`N4_Phicf0_is_conj` の共役元 `g0 k=(r^k,1,1)` も正しい。
奇数族の式 \(\Phi_{0,k}=\operatorname{inn}(\bar x^{-2k})\) は、
\(n=3\) では
\(\bar x^{-2k}=(r^k,1,1)\) になるので符号矛盾はない。

### F1.4 抽象 12 元型 \(T\)

**定義は PASS。非空虚性 statement に P1 が必要。**

`T := (Bool × Fin 3) × Bool` と

\[
((v,t),w)((v',t'),w')
 =((vv',\,vt'+t),\,ww')
\]

を実装する `mulT` は、文字どおり
\(\operatorname{Aff}(\mathbb Z/3)\times C_2\) の積である。
`oneT`、`invT`、`chiT((v,t),w)=(v,w)` も正しい。

Bridge の `param` は
\(\mathcal X_3\times\mathbb Z/3\to T\) の正しい座標変換であり、
`T_param_injective` と `T_param_surjective` が全単射を述べる。
`phiOf`、`T_phiOf_eq_Phicf`、`T_phiOf_hom`、
`T_mul_is_comp` により、`T` の積は実際に 12 個の `Phicf` の合成と一致する。
従って旧 D-1 の「ある 12 元群の真理」問題は解消している。

### F1.5 exact conjugator

**PASS。**

`Conjugator.lean` の七リテラルと `hinv` を
裁定 28・v3.3 erratum に照合した。

- \(h=[2,3,5,6,4,1]\)（1-indexed one-line）で一致。
- 共役は \(h\bar xh^{-1}=\sigma_0\)、
  \(h\bar yh^{-1}=\sigma_1\)、
  \(h\bar zh^{-1}=\sigma_\infty\) の向きで一致。
- 左作用 \((p\circ q)(i)=p(q(i))\) と一致。
- `allPerms6_complete` と `allPerms6_are_perms` が、長さ 720 だけだった
  旧い悉皆性の穴を閉じる。
- \(\delta1\) のリテラル pin・再導出禁止を守る。
- `sigma_marking`、両三つ組の ordered passport、Bridge の
  `A10_simultaneous_conjugate` が、本体の \(\Lambda\)-作用と pin した三つ組を
  「ラベルを同一視する」のではなく**同時共役の存在**で正しく接続する。

`A10_simultaneous_conjugate` の式
\(g\,\mathrm{permXFin}=xbar\,g\) 等は
\(g\,\mathrm{permXFin}\,g^{-1}=xbar\) の正しい書換えである。
`g ∈ allPerms6` と `allPerms6_are_perms` が全単射性を供給するため空虚でない。

---

## F2. statement 層の行別判定

| 行 | 判定 | 忠実性判定 |
|---|---|---|
| F1–F7 | **PASS** | 群公理、parity、\(\lvert G_3\rvert=108\)、生成、\(H\le G_3\)、\(\lvert H\rvert=18\) は紙と一致。`allE_nodup` が濃度解釈を閉じる |
| F8 | **受理する実装逸脱** | Lean の直接 statement は \(108=6\cdot18\)。F7 の部分群性と合わせれば Lagrange により \([G_3:H]=6\)。ただし「剰余類型を Lean で構成した」とは書かない |
| F9–F13 | **PASS** | normalizer、一般共役則、単純推移、全分岐、ordered passport。Bridge の `cosetAct_action` と X の直接位数検査により F13 の旧非対称も解消 |
| F14 | **受理する実装逸脱** | `¬∃` 形は「全ての kernel 元が `coreG3` に入る」の論理的同値形。`F14_core_mem` が逆包含、`core_card` が 3、`image_order36` が像 36 を与える |
| F15 | **PASS** | \(H'\cap\langle\bar x\rangle=1\) だが stabilizer がちょうど \(\{0,3\}\) という反例を両向きで述べる |
| F16 | **PASS（強い）** | 紙は \(v\ne0\) を使うが、Lean の準同型性は全 \(v\) で真 |
| F17 | **受理する狭形置換** | 一般の拡張原理そのものは未実装。代わりに F19 が生成元像の対から \((m,k)\) を直接回収する。(K4) 単射にはこれで十分。一般 F17 を `verified` と数えてはならない |
| F18–F20 | **PASS** | 正典生成元像、12 パラメータの単射、準同型性・全単射性・\(G_3\) 保存を満たす |
| F21–F22 | **P1 条件付き PASS** | 群構造・直積定義・位数 profile・中心は正しい。`allT_nodup` 後に濃度札が閉じる。明示的な `GroupEquiv` 定理ではなく「定義的直積 + profile」である |
| F23 | **P2 条件付き PASS** | `X3.map chiVal = Z12x` 自体は正しい。Bridge の現行 \(\chi\) 接続はファイバー同定まで |
| F24–F25 | **P1 条件付き / PASS** | kernel の述語と準同型性、\(\mathfrak F_0\) の忠実・不動点なし・位数 3 は正しい。核の濃度 3 の札だけ P1 に依存 |
| F26 | **PASS** | 抽象述語版は紙の counting の中核そのもの。閉性、\(A\supseteq\mathfrak F_0\)、\(\widetilde\chi(A)\) 全射から \(A=T\)。\(A\equiv\top\) が前件の証人なので空虚でない |
| F27 | **PASS** | `rhoLam_conj_correct` と `rhoLam_param0_eq_rhoF0` により、天下りの写像でなく `Phicf` が誘導する真の \(\Lambda\)-作用について述べている |
| F29 | **PASS** | 正典値、三共役式、marking、悉皆性、\(\delta1\)、A-10 が揃う |
| F32 | **PASS** | inclusion は写像の等式で述べ、subset/superset の両方向を持つ。cycle type だけで \(C_3\) を同定する誤りはない |

F28 は F22 の定義的直積/profile で支払うという設計判断、
F30 は探索として射程外という設計判断を、そのまま受理する。

---

## F3. Bridge.lean の重点監査

### F3.1 D-1

**PASS。**

次の鎖がすべて statement として存在する。

\[
\mathcal X_3\times\mathbb Z/3
\xrightarrow[\sim]{\mathrm{param}}T
\xrightarrow{\mathrm{phiOf}}\operatorname{Aut}(G_3),
\qquad
\mathrm{phiOf}(\mathrm{param}(m,k))=\Phi_{m,k},
\]

\[
\mathrm{phiOf}(ab)=\mathrm{phiOf}(a)\circ\mathrm{phiOf}(b).
\]

`T_param_surjective` が全 \(t:T\) を覆うので、接続は 12 個のうち一部に
限られていない。合成順序も紙の左作用規約と一致する。

### F3.2 D-2

**PASS。**

`rhoLam_conj_correct` は全
\(m\in\mathcal X_3,k,c,v\) について

\[
v\in H_c
\iff
\Phi_{m,k}(v)\in H_{\rho_\Lambda(\mathrm{param}(m,k))(c)}
\]

を述べる。`rhoLam_hom` と合わせて真の作用であり、
`rhoLam_param0_eq_rhoF0` が F25/F32 側との二重定義を消す。

### F3.3 A-10

**PASS。**

存在量化子は `∃ g ∈ allPerms6` で \(S_6\) 全体を走り、
三つの generator を**同じ \(g\)** で結ぶ。従って ordered triple の同時共役であり、
三本を別々の共役子で結ぶ弱い命題ではない。

### F3.4 残る \(\widetilde\chi\) の型穴

**要修正 P2。**

現行

```lean
(chiT (param m k) = chiT (param m' k'))
  ↔ chiVal m = chiVal m'
```

は、「二つの四元集合が同じファイバー分割を持つ」ことを言う。
四値を任意に置換してもこの命題は変わらない。従って紙のラベル

\[
\begin{array}{c|cccc}
m&0&2&3&5\\ \hline
\chiVal(m)&1&5&7&11\\
\chiT(\mathrm{param}(m,k))
 &(0,0)&(1,1)&(0,1)&(1,0)
\end{array}
\]

までは固定しない。counting と kernel の同定には現行のファイバー命題で足りるが、
F23/K2 の「\(\widetilde\chi=2m+1\)」という exact statement には足りない。

---

## F4. 非空虚性アンカー

| アンカー | 現状 |
|---|---|
| \(D,E,G_3\) の正典実現 | **PASS** |
| `allE_complete` + `allE_nodup` + F5 | **PASS** |
| \(H\le G_3\)、\(\lvert H\rvert=18\) | **PASS** |
| \(c\mapsto H_c\) の単射、\(\Lambda\) の 6 点 | **PASS** |
| \(\langle\bar x\rangle\) の単純推移 | **PASS** |
| core 3 元・monodromy 像 36 | **PASS** |
| `param` の単射・全射 | **PASS** |
| 12 個の `Phicf` の準同型・全単射 | **PASS** |
| `allT_complete` + `T_card` | **不足** — Nodup が無い |
| `F0_card` | **同じ不足** — filter 元の相異性は `allT_nodup` に依存 |
| F29 の \(S_6\) 悉皆 | **PASS** |
| A-10 の証人が真の順列 | **PASS** |

`allT_complete` と `allT.length=12` だけでは、一般には
「全元を重複なく 12 個列挙した」ことにならない。
現行 `allT` が実際には重複を持たないことは定義から明らかだが、
それを kernel が受理した命題にする一行が欠けている。

---

## 必須修理

### P1. \(T\) の列挙アンカー

少なくとも次の statement を追加する。

```lean
theorem allT_nodup : allT.Nodup
```

これと既存の `allT_complete`、`T_card` を合わせて初めて
\(\lvert T\rvert=12\) が plain Lean の列挙語彙で閉じる。
同じ一行が `F0_card`、F22 の位数分布・中心の濃度解釈も同時に閉じる。

### P2. 円分指標の exact code

`Bool × Bool` と \((\mathbb Z/12)^\times\) の対応を

\[
(0,0)\mapsto1,\qquad
(1,1)\mapsto5,\qquad
(0,1)\mapsto7,\qquad
(1,0)\mapsto11
\]

とリテラルで pin し、全 \(m\in X3,k\) について

\[
\operatorname{decodeChi}(\chiT(\operatorname{param}(m,k)))
=\operatorname{chiVal}(m)
\]

を statement にする。現行 `T_chi_is_chiVal` はその系として残してよい。
これにより「同じ情報を運ぶ」から「紙と同じラベル付き円分指標」へ上がる。

### P3. CLAIMS の語彙修理

W3-14d の「GT 接続」は

> 正典パラメータ群 \(T\) と 12 個の \(\Phi\)-像の接続

へ狭めるべきである。Lean 内には
\(\mathrm{GT}(K^{(3)})\)、\(\mathrm{Ih}\)、\(G_{\mathbb Q}\) 自体は無い。
従って Bridge が閉じたのは **\(T\leftrightarrow\Phi\) の有限接続**であって、
圏論的 GT や算術像への接続ではない。

---

## F5. 現行 CLAIMS W3-14b/c/d の射程

| 行 | 判定 |
|---|---|
| **W3-14b** | **P1/P2 条件付き PASS**。F1–F27 の記載定理の有限内容はよい。ただし \(T\cong S_3\times C_2\) は「`T` が定義的に \(\mathrm{Aff}(\mathbb Z/3)\times C_2\) で、F22 が profile を与える」という札。Lean の明示 `Equiv` 定理がある、とは読ませない |
| **W3-14c** | **PASS**。exact conjugator の値・三式・一意性・第二系統という射程に過大さはない。LMFDB 三つ組の provenance は verified でないという `Conjugator.lean` の限定を維持する |
| **W3-14d** | **P3 条件付き PASS**。D-1/D-2・A-10・旧アンカーの修理内容は正しい。「GT 接続」だけが広すぎる |

P1/P2 後なら、

> \(K^{(3)}\) の正典有限パラメータ層、\(\Phi\)-像、\(G_3,H,\Lambda\)、
> counting の条件付き群論命題、F29

という射程で `verified` を認める。
一方、定理 K3 の全射性、固定体
\(\mathbb Q(\zeta_{12},\sqrt[3]2)\)、arithmetical/genuine、
外部正典がパラメータ集合を本当に \(\mathrm{GT}(K^{(3)})\) と同定する部分は
この Lean 層の `verified` には含めない。

---

## F6. Opus 監査との後読みによる突合

独立監査を終えるまで
`docs/lean/K3対応表_監査_opus_v1.md` は読まず、その後に突合した。

### 一致した点

- \(D,E,G_3\)、marking、N1/N2/N4 の定義は正典に忠実。
- F8 数値化、F10 構造化、F14 `¬∃`、F17 狭形、
  F26 抽象述語はいずれも数学的内容を壊さない。
- 旧版の load-bearing な欠落は D-1（\(T\) と \(\Phi\) の非接続）と
  D-2（`rhoLam` の正当化不足）だった。
- 旧 F29 は `allPerms6.length=720` だけでは悉皆にならなかった。
- exact conjugator のリテラル、共役の向き、\(\delta1\) は正しい。

現行 Bridge/Conjugator は、Opus が要求した D-1、D-2、F20、F13、F3、
`allE_nodup`、F29 悉皆、A-10 をすべて閉じている。

### 独立監査で追加した二点

1. Opus 監査 §1 D-H は `allT` の Nodup 未記載にも触れていたが、
   §3.3/§6 の修理指定では `T_card` の長さだけになった。
   Bridge はその指定を忠実に実装したため、**Nodup の穴だけが残った**。
2. Opus が D-1 修理として指定した `T_chi_is_chiVal` 自体が
   equality-of-fibres であり、紙の \(1,5,7,11\) の exact labels より弱い。
   これは counting には無害だが、翻訳忠実性ゲートでは P2 を要する。

従って Opus の「数学的誤りゼロ」は追認するが、
Lean の「修理後は全行 FAITHFUL」は P1/P2 の二行後、
台帳の最終札はさらに P3 の語彙修理後に上げる。

---

## 警告

- **W1**: `T_card : allT.length = 12` は、単独では型 \(T\) の濃度定理ではない。
  completeness・Nodup・length の三点を一組で読むこと。
- **W2**: 四元集合どうしのファイバー一致は、ラベル付き character の一致ではない。
  特に character 値を Kummer/Galois 側へ渡す文脈では exact code が要る。
- **W3**: F22 は direct product の定義と有限 profile の証明である。
  `T ≃ S3 × C2` という型付き同型写像を Lean が構成した、という札へ
  無断で強めない。
- **W4**: A-10 は本体と pin した置換三つ組の同時共役を証明するが、
  \(\sigma\) 三つ組の LMFDB provenance までは証明しない。
- **W5**: `K3_counting` は正しい条件付き定理であり、
  算術像 \(A\) がその三前件を満たすことは Lean 射程外である。

---

## ★教材

1. **全列挙は completeness + Nodup + length の三脚である。**
   一脚でも欠ければ、リストの長さを集合の濃度と呼べない。
2. **同じファイバーを持つことと、同じラベル付き写像であることは違う。**
   character の値域を別型で符号化したら、decoder を pin して exact equality を置く。
3. **パラメータ群と \(\Phi\)-像を接続しても、外部の GT 対象を形式化したことにはならない。**
   「有限モデルへの橋」と「圏論的・算術的対象への橋」は別札にする。
4. **任意のラベル付けを接続する正しい命題は、リテラルの再導出ではなく同時共役の存在である。**
   A-10 は \(\delta1\) を壊さずに二つの 6 点模型を結ぶ好例である。

---

## 監査範囲外申告

本便で statement/definition を静的に監査した対象は次である。

- `sol/sol_task_33_lean_fidelity.txt` 全文、
- `docs/対話帳.md` の新着確認、
- `docs/lean/K3対応表_v0.md`、
- `docs/week4-K3飽和_opus_v3.md` の v3.1・v3.2 addendum・v3.3 erratum、
- `sol/裁定_28_f29_conjugator.md`、
- `lean/K3/Base.lean`,
  `Shadows.lean`,
  `Counting.lean`,
  `Lambda.lean`,
  `Group.lean`,
  `LambdaFull.lean`,
  `Struct.lean`,
  `CountingFull.lean`,
  `Conjugator.lean`,
  `Bridge.lean`,
- `provenance/CLAIMS.md` の W3-14b/c/d、
- 独立監査後に
  `docs/lean/K3対応表_監査_opus_v1.md`。

監査対象は定義本体と theorem statement の翻訳忠実性である。
証明項・tactic の妥当性、クリーンビルド、公理印字、CI、実行時間は
カーネル/CI 側の既存検収を前提とし、本便の判定根拠にはしていない。
`Marking.lean`、Mathlib 側 F17′/F26′/F31 系、F30 の探索、
D1 原論文 PDF の再照合、LMFDB provenance、GAP/node 証明書の再実行、
\(\mathrm{Ih}\)、Galois/Kummer、固定体、arithmetical/genuine は監査範囲外である。
