# 影工房 便 31 返信 — \(K^{(5)}\) manifest v1.1 ゲート監査

## 総合判定

\[
\boxed{\textbf{差戻し（発射条件③は現状 NO-GO）}}
\]

有限群論と予測の数学的骨格は通る。とくに補題 K5-a の
\(a=1\) は、後述の型修正を入れれば **PASS** である。
K5e による \(8\mid n\) 側の負較正も、開示された証明書と裁定の
射程内で整合している。

しかし manifest はまだ「方針書」であって「凍結済み発射物」になっていない。
発射を止める blocker は次の四つである。

1. `K5-sq` / `K5-ns` の canonical \(H\)、正規化置換三つ組、hash、
   FORMAL-IN の証拠 ID が実際には記載されていない。
   manifest が参照する D1 v1.1 §1.3 にもそれらは存在しない。
2. 凍結 1 が「探索着手前**または初期**」となっており、
   個別候補を見てから規則を固定する余地が残る。また二モデルを
   同時に第二凍結する規定もない。
3. \(b\) は dessin ごとの \(b_{\rm sq},b_{\rm ns}\) として型付けすべきで、
   封印値 \(a\) 自体を後から更新してはならない。現在の
   \(a\mapsto ab^{-1}\) は一方だけが捻れた場合しか表していない。
4. Kummer 類の等号・非等号と位数について、陽性・陰性それぞれの
   厳密証明書型、成功状態、全結果組合せ、即時停止条件が未定義である。

従って許可するのは **S5 の紙上設計と凍結 1 文書の起草まで**である。
個別モデルの探索は修正版の凍結 1 が受理された後、
\(u\) 抽出は両モデルの共同凍結 2 と発射錠の後に限る。
以下の必須修理を v1.2 に入れれば、再監査は差分検収で足りる。

| 項目 | 判定 |
|---|---|
| 五札の数学的分類 | **条件付き PASS** |
| 封印予測 (P1) | **PASS** |
| 封印予測 (P2), \(a=1\) | **PASS**（共通 \(\tau\) 規約の下） |
| 補題 K5-a | **PASS**（D1 の一箇所を型修正） |
| 較正三層の設計 | **PASS**、ただし artifact ID/hash の実体化が必要 |
| 二段凍結 | **差戻し**（「または初期」を削除、両翼共同凍結へ） |
| Model-Builder / Extractor 分離 | **条件付き PASS**（grep は補助検査に降格） |
| \(u\) 二経路 | **条件付き PASS**（経路仕様・非共有 helper・不一致時停止を先に凍結） |
| \(b\) 判定 | **差戻し**（二側化と有効指数の式が必要） |
| 非対称結果ルール | **差戻し**（一組しか書かれていない） |
| 撤退期限 | **PASS**、ただし即時 integrity stop を追加 |
| S5 個別モデル探索 | **現時点 NO-GO**（凍結 1 待ち） |
| \(u\) 抽出 | **NO-GO** |

---

## F1. 五札と「封印の実体」

### F1.1 五札の内容

五札の役割分離そのものは便 30 F6 と整合する。

| 札 | 監査判定 |
|---|---|
| **FORMAL-IN** | 内容は正しいが、証拠 ID と二 fixture の有限対象が未記入なので、まだ札が実体化していない |
| **BRIDGE-IN** | 必須成分の大半を含む。追加で loop の向き、左右作用、\(K\) の原始根の表現、actual conjugator の完全な置換データ、局所助変数の式を固定すべき |
| **BRIDGE-FAIL** | (P2) は入っているが、(P1) の厳密な破れが入っていない。個別橋の FAIL と「少なくとも一方が FAIL」の pairwise FAIL も分ける必要がある |
| **BRIDGE-UNKNOWN** | 正しい。根判定・非冪判定の証明書が得られない場合もここへ入れる |
| **SCHEMA-OUT** | 正しい。bad \(H\)、非 regular、不安定、非忠実、\(8\mid n\) の \(K^{(n)}\) を混同せず保持している |

B5 を

\[
\text{形式 FAIL}\quad+\quad
\text{primary 分離による今回の迂回}
\]

の二段札に保った点も **PASS** である。「無害化」を B5 自体の PASS と
読んでいない。

### F1.2 参照先不存在

manifest の宇宙欄は

> canonical \(H\) 生成元と正規化置換三つ組の hash は D1 v1.1 §1.3

とする。しかし D1 §1.3 にあるのは (P-a)、`all_two_classes`、
採否規則であり、canonical \(H\)、置換三つ組、hash はない。
D1 全体にも hash の値は記載されていない。
従って現在の `K5-sq` / `K5-ns` は名前だけで、凍結された fixture ではない。

v1.2 では dessin ごとに少なくとも次を**値として**置く必要がある。

\[
\begin{array}{c|c}
\text{field} & \text{内容}\\ \hline
\texttt{fixture\_id} & \texttt{K5-sq},\ \texttt{K5-ns}\\
\texttt{marking\_version} & (X,Y,Z)\text{ の正本と作用規約}\\
\texttt{H\_generators} & G_5\text{ の固定座標での生成元列}\\
\texttt{perm\_triple} & (\sigma_0,\sigma_1,\sigma_\infty)\in S_{10}^3\\
\texttt{normalization\_algorithm} & \text{同時共役の正規化法と tie-break}\\
\texttt{sha256} & \text{canonical serialization の digest}\\
\texttt{evidence\_ids} & \text{node/GAP の検査項目と出力 artifact}
\end{array}
\]

hash の対象となる serialization、UTF-8、改行、配列順序も固定する。
単に文書のどこかを SHA-256 に通すだけでは、同じ数学対象に複数の
digest が生じる。

K5 finite fixture と K3 regression fixture も同様である。
現 manifest は「証拠 ID を転記」と命じているが、転記済みの表がない。
これは発射時に後から埋める欄ではない。

### F1.3 manifest と結果記録

manifest 自体は開示後も不変でなければならない。
したがって FORMAL-IN の `(5′) = PENDING` を同じファイル上で
`PASS` に書き換える方式は採らない。

別の versioned result record に

- `bridge_result_sq ∈ {PASS, FAIL, UNKNOWN}`,
- `bridge_result_ns ∈ {PASS, FAIL, UNKNOWN}`,
- `pair_gate ∈ {PASS, FAIL, OPEN}`,
- `saturation_result ∈ {PROVED, NOT_PROVED}`,

を保存し、凍結 manifest の hash を参照させるべきである。
五札を保ったまま、欠けている「成功状態」をこれで補える。

これは便 30 F6.2 の私の骨子にも書き落としていた点である。
過去返信は変更せず、本返信を erratum とする。

---

## F2. 封印予測 (P1)(P2) と厳密判定

### F2.1 数学的妥当性

\[
\boxed{\operatorname{ord}([u_i^{-1}]_{10})\in\{1,5\}}
\tag{2.1}
\]

は (5′)、\(\rho_i(\mathfrak F_0)=\tau_i(\mu_{10}[5])\)、
\(\mathfrak F_0=C_5\) の帰結として正しい。

また共通の formal \(\tau\) 規約で補題 K5-a を用いれば

\[
\boxed{
[u_{\rm ns}^{-1}]_{10}=[u_{\rm sq}^{-1}]_{10}
\quad\text{in }K^\times/K^{\times10}
}
\tag{2.2}
\]

も正しい。生の \(u\) の一致を要求しない点も正しい。

ただし (2.1) は「2 または 10 なら記録事故」とだけ処理してはならない。
FORMAL-IN、BRIDGE-IN、数体演算が独立に閉じているなら、
位数 2 または 10 はまさに (5′) の候補反例、すなわち
**BRIDGE-FAIL** である。どの前件が壊れたか未確定なら
`integrity quarantine` とし、再監査まで新現象とも記録事故とも断定しない。

### F2.2 Kummer 証明書型

\[
v_i:=u_i^{-1}\in K^\times
\]

と置く。浮動小数点の root search や「根が見つからなかった」は
判定証明書にならない。

位数 1 の陽性証明書は

\[
c^{10}=v_i,\qquad c\in K^\times
\tag{2.3}
\]

という明示 witness である。位数 5 の陽性証明書は

\[
c^{10}=v_i^5
\quad\text{かつ}\quad
v_i\notin K^{\times10}.
\tag{2.4}
\]

後半には、例えば

- ある素イデアルで valuation が \(10\) の倍数でない、
- 単数・根-of-unity 成分の exact obstruction、
- \(T^{10}-v_i\) が \(K\) に根を持たないことの厳密数体証明書、

のいずれかが要る。探索失敗しかない場合は UNKNOWN である。

有効指数を \(a_{\rm eff}\) としたとき、(P2) は

\[
r:=\frac{v_{\rm ns}}{v_{\rm sq}^{\,a_{\rm eff}}}
\tag{2.5}
\]

について \(r\in K^{\times10}\) を判定する問題である。
PASS は \(c^{10}=r\) の明示 witness、FAIL は
\(r\notin K^{\times10}\) の exact obstruction を要求する。
二つの \(u\) 抽出経路が同じ代表を返したことだけでは、
(2.3)–(2.5) の Kummer 判定を閉じない。

### F2.3 「全 \(\gamma\)」の量化子

(5′) は

\[
\rho_i(\operatorname{Ih}(\gamma))
=\tau_i(\kappa_i(\gamma))
\qquad(\forall\gamma\in G_K)
\tag{2.6}
\]

である。有限個の Frobenius サンプル一致は較正にはなるが、
PASS の証明にはならない。PASS は character の恒等を与える
普遍的導出または同値な Kummer 拡大の厳密同定を必要とする。
FAIL には一つの exact な \(\gamma\) の反例で足りる。

---

## F3. 較正三層

### F3.1 K5 finite fixture

内容は便 30 F6.4 と一致し **PASS** である。
ただし「D1 v1.1 で済」だけでは発射 artifact にならない。
二 dessin の代表、置換三つ組、\(\rho_i\)、\(j_i\)、\(a=1\)、
node/GAP の証拠 ID と digest を一表に固定する必要がある。

### F3.2 K3 regression fixture

次の区別を守った点は **PASS** である。

- \(u=-4\) はモデル・branch・cusp・uniformizer と一体の期待値。
- モデルから raw に再計算し、定数 `-4` の直書き比較を較正と呼ばない。
- \(u'=-256/729\) は同じ class の covariance control。
- K3 の成功を K5 の証拠や期待値に数えない。

ただしここも fixture の式、exact conjugator、局所助変数、
checker の版と hash が manifest に実体化されていない。
既存 K3 の \(u=-4\) は二者一致だが、厳密 blind independence は
過去裁定でも主張していない。回帰 fixture としては十分だが、
「独立二経路の新証拠」へ札を上げないこと。

### F3.3 covariance controls

三項とも正しい。

1. \(X\mapsto X^{-1}\) で class は反転し、位数・kernel・固定体は不変。
2. \(s\mapsto cs\) で \(u\mapsto u c^{-10}\)、class は不変。
3. \(\tau\mapsto\tau\circ[d]\) と Kummer character の逆冪変換を
   同時に行えば (5′) は不変。

ただし第三項は後述の \(b_i\) と同じ型で実装し、
formal invariant \(a\) の値を書き換えない。

### F3.4 K5e 負較正

`certificates/k5e/summary.v1.json` の静的記録は

\[
n=12:\ (M,e,M/e)=(12,3,4),\qquad
n=8,16:\ \Phi_{0,n/4}=1
\]

を持ち、裁定 27 と一致する。
`K24.v1.json` も冒頭 note で
「SCHEMA-OUT 較正用であり合格を意味しない」と明記している。
従って D1 §12.2 論点 3 は閉鎖済みとしてよい。

本便ではその GAP/node 計算を再実行していないので、札は
`cross-checked と報告された証明書の静的突合` であって
Lean の `verified` ではない。
\(n\equiv2\pmod4\) 分岐は開示どおり宇宙外・未検査のままであり、
この負較正からその分岐まで一般化しない。

---

## F4. BRIDGE-IN 構築の独立性

### F4.1 凍結 1 の時点

現文の

> 探索の着手前または初期

は fail-open である。「初期」が個別候補、データベース hit、
数値近似、局所係数のいずれかを見た後を含み得る。

次のように一意に直す必要がある。

> **凍結 1 は、両 dessin のいかなる個別モデル候補・係数・数値近似にも
> 接する前、探索コマンドを一度も実行する前に完了する。**

凍結 1 には次を含める。

- モデルの同値関係と正規形アルゴリズム、
- 複数候補の全順序と tie-break、
- \(y\) の符号、基底三点、sheet numbering、
- cusp と uniformizer の決定アルゴリズム、
- 例外分岐と「一意に決まらなければ UNKNOWN」の規則、
- 二つの \(u\) 経路の数式・実装版・受理規則、
- \(b_i\) の決定式、
- exact number-field/Kummer 判定器の版。

「規則を先に死なせる」という発想は正しいが、現文の時点指定では
まだ死んでいない。

### F4.2 凍結 2 は両翼同時

二 dessin を「同時進行」と書くだけでは足りない。

\[
\boxed{
\text{両モデル、両 actual marking、両 uniformizer を
一つの atomic bundle として凍結 2}
}
\tag{4.1}
\]

とする必要がある。一方のモデルを凍結して \(u\) を開けた後、
もう一方の複数候補から選べるなら (P2) は盲検でなくなる。

一方のモデルしか得られないときは、そのモデルを保存してよいが、
両翼共同凍結と Extractor 起動は保留する。片翼だけを先に開ける
別キャンペーンを行うなら、目的と結果規則を別 manifest にする。

### F4.3 役割分離

Model-Builder / Extractor 分離は有効な緩和策であるが、
自己申告と transcript grep は独立性の証明ではない。
例えば「\(u\)」や「series」という文字列を使わず、
同値な leading coefficient や Kummer class を計算できる。

従って A の出力を whitelist する。

- 許可: 明示モデル、Belyi map、分岐 divisor、cusp、uniformizer の式、
  target triple への exact conjugator。
- 禁止: \(\lambda/t^{10}\) の cusp 値、同値な leading coefficient、
  その valuation/class、候補選択にそれらを使うこと。
- A は「\(u\) 未計算」を申告し、全 transcript を保存する。
- grep は sanity check として残すが、主根拠は凍結済み入出力 schema と
  役割別 access log とする。

Model-Builder が分岐指数 10 や `uniformizer` であることを証明するのは
許される。禁止対象は \(\lambda/t^{10}\) の非零定数項である。

### F4.4 \(u\) の二経路

「cusp 展開 × Vieta/単数」はよい組合せである。
ただし独立性を名乗るには、少なくとも

- 非共有 helper、
- 別の中間表現、
- raw output の別保存、
- 一致判定だけを行う第三の小さい checker、

が必要である。同じ CAS の同じ局所展開を、一方で級数表示、
他方で `leading_coefficient` と呼ぶだけでは二経路でない。

不一致時は平均、符号調整、座標再選択を禁止し、直ちに
`integrity stop / BRIDGE-UNKNOWN` とする。

### F4.5 hash commitment

hash は内容同一性を検査するが、「いつ固定したか」を単独では証明しない。
凍結記録に

- canonical serialization の digest、
- UTC/JST timestamp、
- immutable ledger/commit ID、
- 凍結対象の全ファイル一覧、
- 発射錠が拘束する digest の組、

を置くべきである。`FIRE_k5bridge.auth` はこの digest 組に束縛し、
別 artifact へ再利用できない一回性の記録にする。

---

## F5. \(b\) の正しい型と封印法

### F5.1 一個の \(b\) ではない

dessin \(i\in\{\mathrm{sq},\mathrm{ns}\}\) ごとに、
凍結された sheet identification を \(c_i\)、
正向きの実 local monodromy を \(\ell_i\) とする。
次の式を**凍結 1 で定義**する。

\[
c_i\ell_i c_i^{-1}
=\tau_i(\zeta_{10}^{\,b_i}),
\qquad b_i\in(\mathbb Z/10)^\times.
\tag{5.1}
\]

\(\tau_i\) は単射なので、右辺の巡回群に属する generator なら
\(b_i\) は一意である。属さなければ actual marking が閉じておらず
BRIDGE-UNKNOWN である。

\[
|(\mathbb Z/10)^\times|=\varphi(10)=4
\]

なので候補は \(1,3,7,9\) の四つであり、八つではない。
\((\mathbb Z/20)^\times\) の lift は八つあるが、
\(\mu_{10}\) 上では二つずつ同じ作用になり、これは別の封印項目である。

### F5.2 有効指数

actual comparison が

\[
\rho_i(\operatorname{Ih}(\gamma))
=\tau_i\!\left(\kappa_i(\gamma)^{b_i}\right)
\tag{5.2}
\]

という規約なら

\[
\operatorname{Ih}|_{G_K}
=j_i\circ[b_i]\circ\kappa_i.
\]

従って二 dessin の正しい比較指数は

\[
\boxed{
a_{\rm eff}
=[b_{\rm ns}]^{-1}\,a\,[b_{\rm sq}],
\qquad a=j_{\rm ns}^{-1}j_{\rm sq}=1.
}
\tag{5.3}
\]

ここで \([b_i]\) は \(\mu_{10}[5]\) への制限である。
縮約
\((\mathbb Z/10)^\times\to(\mathbb Z/5)^\times\) は全単射なので、
この記法に lift の曖昧さはない。

現在の \(a\mapsto ab^{-1}\) は
\(b_{\rm sq}=1,\ b_{\rm ns}=b\) とした一側だけの特殊形である。

最重要点は、

\[
\boxed{\text{formal invariant }a=1\text{ は永久に不変}}
\]

であり、後から更新するのは \(a\) でなく、別欄の
\(b_{\rm sq},b_{\rm ns},a_{\rm eff}\) だということである。
履歴上の \(a\) を上書きすると、有限群側の封印と橋側の規約が混ざる。

### F5.3 推奨する厳格運用

主予測 (P2) の「完全一致」を守るなら、両 dessin に同じ pipeline を
使う以上

\[
b_{\rm sq}=b_{\rm ns}
\tag{5.4}
\]

を BRIDGE-IN の受理条件とするのが最も明快である。
共通値が 1 でなくても (5.3) では \(a_{\rm eff}=a=1\) となる。
不一致なら \(u\) を開けず、規約不整合として停止する。

より一般の \(b_{\rm sq}\ne b_{\rm ns}\) を許すなら、v1.2 で (5.3) を
先に封印し、(P2) を

\[
[u_{\rm ns}^{-1}]_{10}
=[u_{\rm sq}^{-1}]_{10}^{\,a_{\rm eff}}
\tag{5.5}
\]

へ一般化する。四通りまたは十六組の結果を列挙する必要はなく、
(5.1)(5.3) という全称規則を先に封印すればよい。

現在のように「\(b\ne1\) が出たら司令塔裁定で \(a\) を更新」は、
結果開示前ではあっても規則の事後変更であるため認めない。

---

## F6. 非対称結果と撤退条件

### F6.1 結果規則

現 manifest が書くのは

> 一方 PASS、他方 UNKNOWN

の一組だけである。少なくとも次を先に固定する。

1. **両方 PASS**:
   (P1)(P2) の exact 証明書まで一致して pair gate PASS。
2. **PASS + UNKNOWN**:
   PASS 側で class 位数 5 まで閉じれば、存在型の飽和定理には
   一つの witness となり得る。ただし `all_two_classes` campaign と
   (P2) は OPEN。一方を証拠集合から消さない。
3. **PASS + FAIL**:
   PASS 側が独立に完全なら存在型結論は残り得るが、
   B_FC の dessin 非依存な主張は反証された。
   FAIL 側を捨てて campaign PASS としない。
4. **FAIL + UNKNOWN / 両方 FAIL**:
   飽和の証拠なし。個別または pairwise bridge falsifier として記録。
5. **(P2) の exact な破れ**:
   両 BRIDGE-IN が閉じていれば「少なくとも一方の (5′) が偽」。
   それだけでどちらが偽かは同定しない。
6. **(P1) の exact な破れ**:
   FORMAL-IN と class 証明書に問題がなければ、その dessin の
   (5′) に対する BRIDGE-FAIL 候補。
7. **二つの \(u\) 経路の不一致**:
   数学結果を一切宣言せず integrity stop。

「存在型の定理」と「二 detector の橋の普遍性」と
「本 campaign の全二類整合」を別々の出力にする必要がある。

### F6.2 撤退期限

2026-08-10 または S5 委嘱 8 回の早い方、という資源上限は
明確であり **PASS** である。ただし

- 「一回」の定義と委嘱 ID、
- 失敗、timeout、再走を数えるか、
- 片翼だけ得られた場合も「両翼未閉鎖」として期限発火すること、

を台帳化する。
本ゲート差戻しを理由に 2026-08-10 の期限を黙って後ろへ動かさない。
期限を変更するなら別 version の明示的な研究資源裁定とし、
元の期限も履歴に残す。

これとは別に、次は期限を待たない即時停止条件である。

- 凍結 1 前に個別候補へ接触した。
- 凍結 2 前に \(u\) または同値な leading class が漏れた。
- hash、serialization、発射錠の対象が一致しない。
- 両モデルを共同凍結する前に一方の \(u\) を開けた。
- モデル検査の二系統が不一致。
- \(u\) 二経路が不一致。
- \(b_i\) が一意に決まらない、または採用する共通規約を破る。
- K3 regression/covariance control が失敗。
- exact Kummer 証明書が得られず、探索失敗だけで PASS/FAIL を宣言した。

漏洩した run は後から同じ規則を hash して救済しない。
汚染 artifact を隔離し、規則を変えるなら新 version の campaign とする。

---

## F7. 補題 K5-a

### F7.1 型を直した証明

\[
c_k:=\Phi_{0,k}\in\mathfrak F_0,\qquad k\in\mathbb Z/5
\]

と置き、共通の抽象同定

\[
\iota:\mu_{10}\xrightarrow{\sim}\langle X\rangle,
\qquad \zeta_{10}\longmapsto X
\]

を固定する。命題 K5-1 より、各
\(i\in\{\mathrm{sq},\mathrm{ns}\}\) で

\[
\rho_i(c_k)
=\tau_i(\zeta_{10}^{-2k}).
\tag{7.1}
\]

\(z=\zeta_{10}^{2t}\in\mu_{10}[5]\) に対して

\[
-2k\equiv2t\pmod {10}
\quad\Longleftrightarrow\quad
k\equiv-t\pmod5.
\]

従って

\[
\boxed{j_i(\zeta_{10}^{2t})=c_{-t}}
\tag{7.2}
\]

であり、右辺は \(i\) に依らない。ゆえに

\[
\boxed{j_{\rm sq}=j_{\rm ns},\qquad a=1.}
\]

これは「\(\operatorname{inn}(g)\) の各共役類上の作用が同じ群元
\(g\) による共役である」という一段を正確に型付けしたものなので、
論法に穴はない。

### F7.2 D1 の軽微な型誤り

D1 §6.3.2 の

\[
j_i(\tau_i(X^{2t}))
\]

は、\(j_i\) の domain が \(\mu_{10}[5]\) である定義のままでは
ill-typed である。入力は \(\zeta_{10}^{2t}\) または
共通同定後の \(X^{2t}\) と書くべきで、(7.2) に直せばよい。
結論には影響しない。

inner の規約を全体で反転すれば両 \(j_i\) が同じように反転するため、
\(j_{\rm ns}^{-1}j_{\rm sq}=1\) は不変である。

### F7.3 \(a\) の意味

\(a=1\) は K5-1 の帰結であり、独立の仮定ではない。
それでも sealed checksum として保存する価値はある。

ただし「actual marking の捻れで \(a\) がずれる」という表現は避ける。
ずれるのは formal \(a\) ではなく (5.3) の \(a_{\rm eff}\) であり、
捻れ検出器は \(b_{\rm sq},b_{\rm ns}\) である。

---

## F8. D1 v1.1 §12.2 の残論点

### F8.1 論点 1 — K5-a

**PASS。** F7 の型修正だけを入れる。
「二 detector は K5-1 により formal に coherent」という読みでよい。
\(a\) は独立情報でないが、有限側の不変な checksum として封印する。

### F8.2 論点 2 — \(b\)

四通りを出力別に列挙する必要はない。八通りではない。
モデル前に (5.1) の決定規則を封印し、凍結 2 で
\(b_{\rm sq},b_{\rm ns}\) を機械的に記録する。
比較式は (5.3)。formal \(a\) は更新しない。

主予測を完全一致のまま保つ推奨運用は
\(b_{\rm sq}=b_{\rm ns}\) を BRIDGE-IN 条件とする方式である。

### F8.3 論点 3 — 偶数側

K5e と裁定 27 により閉鎖済みとしてよい。
本便の追加【GAP】要求はない。

### F8.4 論点 4 — 攻略分岐

短期の優先は

\[
\boxed{\text{① }K^{(n)}\text{ 族外の repeated-primary かつ忠実な窓}}
\]

である。理由は、現行 \(R^{\rm cyc}\) のまま falsifier を撃てるからである。

②「中心 \(C_2\) を測る拡張スキーマ」は長期価値が高いが、
単に \(\Lambda\) に線束・接方向を付ければよいわけではない。
\[
\ker\bigl(\Phi:\mathfrak F_0\to\operatorname{Aut}(P)\bigr)
\]
の元は、作用が \(\operatorname{Aut}(P)\) を経由する限り、
\(P\) から関手的に作ったあらゆる decoration にも恒等に作用する。
従って接方向案が有効になるには、GT の作用が
\(\operatorname{Aut}(P)\) を経由しない新しい lift

\[
\widetilde\rho:\mathfrak F_0\longrightarrow
\operatorname{Aut}(\widetilde\Lambda)
\]

を構成し、中心 \(C_2\) 上で忠実であることを別に証明しなければならない。
これは既存 detector の小修理でなく、新スキーマである。

従って①を現行スキーマの次 falsifier、②を並行する定理設計課題とする。

### F8.5 論点 5 — \(n=7\)

\(n=7\) finite gate は安価な三点目として価値があるが、
K5 の算術橋を一歩も閉じない。優先順位は

1. K5 の凍結 1 を先に確定、
2. K5 S5 を律速主線として開始、
3. 主線を遅らせない別資源がある場合だけ \(n=7\) finite gate を並走、

とする。単線なら S5 が先である。
\(n=7\) の結果は別 manifest に記録し、K5 の予測・正規化選択へ
フィードバックしない。

---

## F9. S5 の紙上設計

### F9.1 divisor から始める

passport

\[
(10,\ 2^4 1^2,\ 10)
\]

の Riemann–Hurwitz は

\[
2g-2=-20+(9+4+9)=2,
\qquad g=2.
\tag{9.1}
\]

\(\lambda=0,\infty\) の各 fiber は一点なので、\(\mathbb Q\)-モデル上で

\[
P_0,P_\infty\in C(\mathbb Q)
\]

であり、

\[
(\lambda)=10P_0-10P_\infty.
\tag{9.2}
\]

従って

\[
[P_0-P_\infty]\in J(C)(\mathbb Q)[10].
\tag{9.3}
\]

その位数は 1 ではない。位数 2 なら
\(\lambda=c f^5\) となる degree-2 関数 \(f\) が存在し、
genus 2 の一意な hyperelliptic involution が \(\lambda\) を固定する。
これは \(\operatorname{Aut}(C/\mathbb P^1)=1\) に反する。
従って探索候補では

\[
\boxed{\operatorname{ord}[P_0-P_\infty]\in\{5,10\}}
\tag{9.4}
\]

が強い紙上 filter になる。

\(\lambda=1\) 上の二重点を \(Q_1,\dots,Q_4\)、単純点を
\(R_1,R_2\) とすれば

\[
(\lambda-1)
=2Q_1+\cdots+2Q_4+R_1+R_2-10P_\infty
\tag{9.5}
\]

である。また

\[
(d\lambda)
=9P_0+Q_1+\cdots+Q_4-11P_\infty
\tag{9.6}
\]

は次数 2 の canonical divisor になる。(9.2)(9.5)(9.6) を
係数 ansatz より先に使うと探索変数を減らせる。

### F9.2 hyperelliptic ansatz の注意

genus 2 なので

\[
C:\ y^2=f_5(x)\ \text{または}\ f_6(x)
\]

と置ける。しかし

\[
\lambda\in\mathbb Q(x)
\]

と仮定してはならない。その場合 hyperelliptic involution が
\(\lambda\) を固定し、cover automorphism が少なくとも \(C_2\) となって
Aut \(=1\) に反する。

従って一般に

\[
\boxed{\lambda=A(x)+B(x)y,\qquad B\ne0}
\tag{9.7}
\]

を許す必要がある。

二 dessin は同じ曲線上の二写像かもしれず、異なる曲線かもしれない。
「同時に探索」は同じ曲線・同じ係数 ansatz を強制する意味ではなく、
両方を選別せず共同凍結する意味に限る。

### F9.3 凍結 1 に要求する正規化規則

Model-Builder に最初に提出させる Rule 1 は、少なくとも次の問いへ
モデル非依存に答えなければならない。

1. ordered branch \(0,1,\infty\) をどの loop orientation で
   \(X,Y,Z\) に対応させるか。
2. 同型な hyperelliptic model のうちどれを選ぶか。
3. integral/minimal model が複数なら何を全順序の最小とするか。
4. \(y\mapsto-y\)、Möbius 変換、sheet numbering の tie-break。
5. \(P_0\) での uniformizer を、\(\lambda\) の leading coefficient を
   使わずどう選ぶか。
6. 規則が一意な候補を返さない場合に UNKNOWN へ止まる条件。

uniformizer は、選んだモデル上の Riemann–Roch 基底から
\(\operatorname{ord}_{P_0}(t)=1\) となる最初の有理関数を取る、などの
total algorithm にできる。\(P_0\) が Weierstrass 点か否かで
\(x-x(P_0)\) の位数が変わるので、その分岐も先に書く。
\(\lambda/t^{10}\) の定数項を 1 にする正規化は \(u\) を使うため禁止する。

### F9.4 探索結果の受理

候補発見が数値的でも、凍結 2 に入れるのは exact な

- 曲線方程式と Belyi map、
- (9.2)(9.5)(9.6)、
- 種数・分岐型、
- monodromy 群と target triple への actual conjugator、
- \(\operatorname{Aut}(C/\mathbb P^1)=1\)、
- \(P_0,P_\infty\) と uniformizer、

を閉じたものだけにする。
数値近似や database label は discovery 用であり証拠でない。

---

## 必須修理

- **P1**: v1.2 に `K5-sq` / `K5-ns` の canonical data、証拠 ID、
  canonical serialization と実 hash を値として埋める。
- **P2**: 凍結 1 の「または初期」を削除し、個別候補への接触前とする。
- **P3**: 凍結 2 を二 dessin の atomic joint freeze とする。
- **P4**: \(a\) を不変の formal seal とし、
  \(b_{\rm sq},b_{\rm ns},a_{\rm eff}\) を (5.1)(5.3) で別記録する。
- **P5**: (P1)(P2) の exact Kummer 陽性・陰性証明書型を追加する。
- **P6**: 個別 bridge、pair gate、存在型 saturation の結果表を分離する。
- **P7**: Model-Builder の whitelist と二 \(u\) 経路の
  nonshared-helper 規則を凍結 1 に入れる。
- **P8**: 暦日/委嘱回数の撤退とは別に、F6.2 の即時停止条件を置く。
- **P9**: S5 は (9.2)–(9.7) を紙上 ansatz とし、Rule 1 を
  個別モデル探索より先に提出させる。
- **P10**: D1 v1.1 §0 の壊れた TeX 制御文字を次版で修理する。
  数学結論は動かさず、hash 対象は人間向け Markdown と分離する。

## 警告

- **W1**: 「D1 §1.3 に hash がある」という参照は現物と一致しない。
- **W2**: 「探索着手前または初期」の「初期」は blind split を無効にする。
- **W3**: formal \(a\) を bridge の \(b\) で上書きすると、
  有限群入力と局所規約の provenance が失われる。
- **W4**: transcript grep は語彙検査であって情報独立性の証明でない。
- **W5**: 二つの抽出器の一致と、Kummer 類の等号証明は別ゲートである。
- **W6**: 片翼だけで存在型定理が閉じ得ることと、
  `all_two_classes` campaign が PASS することを混同しない。
- **W7**: \(P\) から関手的に作った decoration は、
  \(\ker\Phi\) を自動的には検出できない。

---

## ★教材

1. **hash は書かれて初めて seal である。**
   「別文書にあるはず」という参照は、実値・対象・serialization がなければ
   事前登録にならない。
2. **複数 detector の convention twist は一個の補正値でなく各翼の値である。**
   不変な formal 比較 \(a\) と、橋由来の \(b_i\) を分けると
   \(a_{\rm eff}=b_{\rm ns}^{-1}ab_{\rm sq}\) が自動的に現れる。
3. **blindness は結果を読まないことだけでなく、候補選択関数を先に殺すことである。**
   二翼問題では、一翼の結果を開く前に両翼を同時に凍結しなければならない。
4. **\(\ker\Phi\) は表現の選び替えだけでは見えない。**
   \(\operatorname{Aut}(P)\) を経由する全 detector が同じ盲点を共有するなら、
   必要なのは decoration でなく、作用そのものの非因子化 lift である。
5. **genus 2 の Aut \(=1\) は探索 ansatz を強く制約する。**
   \(\lambda\in\mathbb Q(x)\) は hyperelliptic involution を deck 変換にしてしまうため、
   \(\lambda=A(x)+B(x)y\), \(B\ne0\) を許さなければならない。

---

## 監査範囲外申告

本便では次を読んで紙上・静的監査した。

- `sol/sol_task_31_manifest.txt` 全文、
- `docs/対話帳.md` の新着確認（T-11 より後の新着なし）、
- `docs/manifest_k5_v1.md` v1.1 全文、
- `sol/裁定_26_ben30.md` 全文、
- `sol/裁定_27_k5e.md` 全文、
- `docs/week4-K5橋_D1_opus_v1.md` v1.1 の差分表、
  §0–§1.3、§4.2–§6.3、§8–§10、§12
  （不変部分は便 30 での全文監査を継承）、
- `certificates/k5e/summary.v1.json` と `K24.v1.json` の schema/note、
- 便 30 の自分の返信（本便 erratum の照合用）。

D1 の node 87/87、GAP 52/52、K5e の GAP/node、
K3 regression pipeline は再実行していない。
明示 genus-2 モデル、actual monodromy、\(u\)、二経路 extractor、
数体での Kummer 判定、(5′) はまだ artifact がないため監査していない。
外部文献照合、Lean 証明も本便の範囲外であり、
`verified` の語は用いない。
