# 総合判定: **差戻し**

二段階判定を分ける。

- **(α-A) 便 48 F14 完了検収: 差戻し。** 原差戻しの核心修理の多くは通ったが、条文案の theorem bundle に exact (5′) の扱いの自己矛盾があり、status-layer の外部化も本文・`CLAIMS` の現役記述まで閉じていない。
- **(α-B) BFC v2.6: 差戻し。** B-6 の現行証明第 3 段が root equality を使うという診断と
  \[
  b_{\rm op}=(\bar t_M\varepsilon)^{-1}
  \]
  は正しい。しかし `(Z20-link)` の前件波及が本文全体へ完了しておらず、撤回したはずの「\(\kappa\) と相殺」説明も現役で残る。
- **(α-C) TB4 v2.1: 定理核は条件付き PASS、artifact 群としては差戻し。** TB4-D/D′、\(\hat b_i=b_{\rm op}\)、TB4-E の数式核は正しい。ただし \(t_{2M}\) とその mod \(M\) 還元を混同し、TB4-E の定理文から proof が呼ぶ intertwiner/marking 前件を落とし、検出表は「8 経路中 7 本」と本文自身の表が矛盾する。
- **(α-D) 著者指定 7 点: 下記 F6 で全回答。**
- **(β) 単一版イベント: 不許可。** Rule 1 v1.4 / manifest v1.6、札更新、B-9′(e′) 復帰、S5 側の次工程を、今回の HEAD のまま開始してはならない。

解析持ち上げ、TB4-3、TB4-A20、TB4-B の紙上核を開け直す必要はない。下記の有限差分を直し、最終 BFC digest へ certificate を再束縛した再提出で足りる。

---

## F1. 現物・digest・再現

指定 artifact、対話帳 T-12/T-13、関連する現行 Rule 1・BFC・amendment を UTF-8 で全行読んだ。SHA-256 は配送値とすべて一致した。CR は全対象 0、許可外 C0 制御文字も 0。

| artifact | 現物の行数 | SHA-256 | 判定 |
|---|---:|---|---|
| `docs/week4-BFC攻略_opus_v2.md` | **1089** | `d8ce5854…9945` | digest 一致 |
| `docs/amendment_5prime_draft.md` | **268** | `198b533d…c809` | digest 一致 |
| `docs/week4-TB4導出_opus_v1.md` | 617 | `0fa5b3fc…068a` | 一致 |
| `search/tb4-monodromy-check.mjs` | 187 | `73a8c66b…2490` | 一致 |
| `search/week4-bfc-antecedents.mjs` | 100 | `f7429890…c9a` | 一致 |
| `certificates/bfc/bfc-antecedents.json` | 1 | `771425f3…7865` | 一致 |
| `docs/対話帳.md` | 168 | `12f8f991…5352` | 一致 |

配送表の BFC「1090 行」、amendment「269 行」は、現物ではそれぞれ 1089、268 行であり、どちらも末尾 LF を持つ。hash が完全一致するので別 artifact ではなく、**配送 metadata の各 1 行過大**として扱う。数学的 blocker ではないが次便で直すこと。

再走結果:

- `node search/tb4-monodromy-check.mjs`: **29/29 PASS**。
- `node search/week4-bfc-antecedents.mjs`: **13/13 PASS**、exit 0。
- certificate は `bfc-antecedents-check/v3`、`25/25`、`fail_closed:true`。`input_doc_path` と `input_doc_sha256` は現 BFC v2.6 の path / `d8ce5854…9945`、script と Node counterpart の digest も現物一致。

これらは有限演算の sanity / cross-check 材料であり、TB4-D/E、A3、root equality の紙上証明でも Lean `verified` でもない。

---

## F2. (α-A) 便 48 F14 の 8 項

| F14 | 判定 | 検収 |
|---|---|---|
| **1. stale 全称・関所名** | **原指定箇所は PASS / 現 v2.6 全体は FAIL** | v2.5 の 7-pattern sweep で便 48 指摘箇所は直った。しかし v2.6 が新たに §§0, 8, 8.1, 10.1.3, 12, 15, 付録 A に旧 \(b\)-意味論と `(Z20-link)` 脱落を残した(F3.3)。 |
| **2. \(a_{\rm eff}\) 組版** | **PASS** | 壊れた改行は修復され、同種の TeX 構文残骸も見つからない。 |
| **3. AB-1 循環除去・二 bundle** | **条件付き PASS** | falsifier 側から (5′)/(5′\(_b\)) を外した核心は正しい。ただし theorem 側は prose と code が食い違う(F2.2)。 |
| **4. C-ii operational certificate** | **PASS** | 5 束縛と二 equivariance 式、sample / field-only / (4) 欠落拒否、fail-closed が入った。 |
| **5. TB4-C** | **PASS** | `(C1)+forward transport/A3+functoriality` へ正しく修文された。 |
| **6. TB4-A20 / Z20-link / 三段分割** | **紙上核 PASS** | countermodel、TB4-3/A20/B、finite/profinite 別札は正しい。ただし v2.1 の \(t\) の型に新 blocker がある(F4.1)。 |
| **7. Z-norm / A3 / 8 経路 / quarantine 等** | **一部 FAIL** | atomic root seal、A3 別 seal、§7.4、文献要請縮小、comparison seal はよい。8 経路の検出数は誤り(F4.5)。 |
| **8. GAP 再束縛・status-layer** | **再束縛 PASS / status-layer FAIL** | certificate 自体は v2.6 digest に正しく束縛された。しかし BFC 7・954 行はなお「v1 digest への束縛 1 件が残る」と断定し、`provenance/CLAIMS.md` W3-17 も「GAP 17/17・artifact 残差 4 件」のまま。外部台帳を正とする設計なら、その外部台帳を同期し本文の現況複製を消して初めて閉じる。 |

従って「F14 全 8 項完了」はまだ宣言できない。

### F2.1 amendment v3 の falsifier bundle

`FALSIFIER-ANTECEDENT-BFC` は正しく、

\[
(0)(1)(2)(3a\text{--}d)(6'_i)(6'_{ii}),\ K5\text{-}1,\ j_i,\ a=1
\]

と B-9′ の共通枠組み、両 BRIDGE-IN、\(b_{\rm sq}=b_{\rm ns}\) gate を前件にし、(5′)/(5′\(_b\)) を含めない。これで便 48 の循環は閉じた。

### F2.2 amendment v3 の theorem bundle — 1 行の blocker

amendment 138–145 行は、

- prose: `THEOREM-ANTECEDENT-Rcyc` は **(5′\(_b\)) および exact (5′) を含む**、
- code: `+ (5'_b)` だけ、

と互いに矛盾する。便 48 F13.3 の指定は後者だった。operative K5 bridge は (5′\(_b\)) であり、exact (5′) は \(b_i=1\) の追加前件下の特殊化なので、次のいずれかに一意化せよ。

```text
THEOREM-ANTECEDENT-Rcyc/twisted = base + (5'_b)
THEOREM-ANTECEDENT-Rcyc/exact   = base + (5') + (b_i = 1)
```

または現 bundle から prose の「および exact (5′)」を削る。結果 record の bundle ID はこの predicate version まで区別すべきである。

### F2.3 C-ii

5 束縛は便 48 F3.3 を満たす。さらに hardening するなら `rho_i_id` と `Ih_N_id` も digest 付きで束縛すると、(5) の式中の写像を別 artifact に差し替える余地が消える。これは本便の blocker にはしない。

---

## F3. (α-B) BFC v2.6 の `(TB2′)=(Z20-link)`

### F3.1 使用箇所の診断: **PASS**

\(\zeta_M^{T}=(\zeta_M^{R})^{t_M}\) と書く。現行 B-6\({}^{\rm tw}\) の第 1・2 段は

\[
x\ \text{on Fib}=m\!\left((\zeta_M^T)^\varepsilon\right)
=m\!\left((\zeta_M^R)^{t_M\varepsilon}\right),
\qquad
c_\Lambda x c_\Lambda^{-1}=\tau(\zeta_M^R)
\]

を与える。従って

\[
c_\Lambda m(\xi)c_\Lambda^{-1}
=\tau\!\left(\xi^{(t_M\varepsilon)^{-1}}\right).
\]

現行の \(\sigma_\zeta\) 経由の証明で \(b=\varepsilon^{-1}\) と書くには \(t_M=1\)、K5 で安全にそれを与える typed antecedent が `(Z20-link)` である。**B-6 証明第 3 段が link を使う**という所有者の診断は正しい。

また、\(\kappa_w(\gamma)\) と \(m(\xi)\) は元で添字づけられ、root generator の命名に依存しない。v2.6 E2 の自己訂正も正しい。

### F3.2 波及地図の数学的中身

- **現行 proof が link を使う**: B-6、B-6\({}^{\rm tw}\)、それを呼ぶ B-7、B-7\({}^{\rm tw}\)。
- **link に本質的に依存しない**: B-3、B-4/B-4c、B-5/B-5\({}^{\rm u}\)、B-8。
- **B-9′**: 共通指数が両 dessin で同じという計算は link なしでも残る。ただしその指数を operational bridge exponent として書くなら \(b_{\rm op}\) を使う必要がある。現 v2.6 の \(b=\varepsilon^{-1}\) は link 下の略記である。
- **TB4-E の別証**を使えば B-6 の結論 (8.1) 自体は link なしに出る。しかし v2.6 が採用した現行 proof path に link を前件化することは正しく、今回は弱化を要求しない。

### F3.3 v2.6 への転記は未完了: **FAIL**

次は差分説明で撤回・追加した内容と、現役本文が正面衝突する。

1. **519–522 行、1007 行**はなお「TB2 root が \(x\) と \(\kappa\) の値を同時に決めて相殺」と説明する。これは 145 行、259–262 行、1044 行が**偽として撤回した文言そのもの**である。
2. **560 行**は B-7\({}^{\rm tw}\) の依存を `(TB1)(TB2)(TB3)(TB4u)+(CAL)+(W1)–(W5)だけ` とし、直前の 537、547 行で追加した link を落とす。
3. **565–566 行の状態表**も B-7 / B-7\({}^{\rm tw}\) の前件から link を落とす。
4. **172–173、306、614、784–800、951 行**は「TB2+TB4 だけで \(b=1\)」「未閉鎖札は TB 枠組みただ一枚」「向きの唯一の関所」と書き、未凍結 `(Z20-link)` を状態札から消している。
5. **697 行**は (7.1) 測定を「TB2/TB4u transport の検査」とするが、\(\hat b=b_{\rm op}\) は TB2 root system に触れない。正しくは「Rule 1 の幾何・marking・transport の検査」であり、root link の検査ではない。
6. **1063–1066 行の記号表**は単一の \(b\) を (8.1) で定義しながら \(b=\varepsilon^{-1}\) と無条件に同定する。これは \(b_{\rm op}\) と \(b_{\rm cmp}\) の再融合である。

従って E4 の「全部に追加」と E2 の「旧説明を撤回」は artifact 全体では未達である。

### F3.4 一般 BFC の型

BFC は一般の \(M=\operatorname{ord}(X)\) を扱うのに、255–257 行は

\[
\zeta_{2M}^{\rm Rule1}:=\bar T\in\mathbf Q[T]/(\Phi_{2M})
\]

を **Rule 1 (1.5)** に帰属させ、名称を `(Z20-link)` とする。現 Rule 1 (1.5) が定義するのは K5 の \(M=10,\ 2M=20\) だけである。

したがって二択が必要である。

1. BFC v2.6 のこの定理群を **K5 / \(M=10\) 特殊化**と明記する。
2. 一般定理では各窓が供給する field-generator object を前件にして `(Z_{2M}-link)` と書き、K5 特殊化だけを `(Z20-link)` と呼ぶ。

現状は一般 theorem と K5 固有 Rule 1 object が混在しており、前件型が閉じていない。

---

## F4. (α-C) 二つの \(b\)

### F4.1 まず \(t\) の型を直す — **blocker**

TB4 257 行は

\[
t\in(\mathbf Z/M)^\times,\qquad
\zeta_M^{T}=(\zeta_M^{R})^t
\]

と定めた直後に `(Z20-link) iff t=1` と書く。これは偽である。K5 では

\[
t_{20}=11,\qquad
\zeta_{20}^{T}=(\zeta_{20}^{R})^{11}\ne\zeta_{20}^{R},
\]

だが

\[
\zeta_{10}^{T}=(\zeta_{10}^{R})^{11}=\zeta_{10}^{R},
\qquad t_{10}=1.
\]

従って必要な型は

\[
t_{2M}\in(\mathbf Z/2M)^\times,\qquad
\bar t_M:=t_{2M}\bmod M.
\]

そして

\[
(Z_{2M}\text{-link})\iff t_{2M}=1,
\]

であって、\(\bar t_M=1\) は link の必要十分条件ではない。

### F4.2 TB4-D / D′: **上の型修理後 PASS**

正しい辞書は

\[
\boxed{
b_{\rm cmp}:=\varepsilon^{-1}\pmod M,\qquad
b_{\rm op}:=(\bar t_M\varepsilon)^{-1}
=b_{\rm cmp}\bar t_M^{-1}\pmod M.
}
\]

導出は F3.1 の生成元計算で閉じ、TB4-3 や \(\varepsilon\) の値を使わない。checker の 64 対もこの剰余恒等式と一致する。

TB4-3 の比較式を入れると

\[
\varepsilon\equiv t_{2M}^{-1}\pmod M
\]

なので

\[
\boxed{b_{\rm cmp}\equiv\bar t_M,\qquad b_{\rm op}\equiv1\pmod M.}
\]

従って D′ も正しい。

ただし「定義だけ」は言い過ぎである。**存在と式の証明**は、少なくとも

- \(x=\iota(\sigma_\zeta^\varepsilon)\) と \(\sigma_\zeta\) の Kummer action、
- \(c_\Lambda\) の \(x\)-equivariance、
- Rule 1 の \(\tau(\zeta_M^R)=X\) marking

を使う。TB4-D の定理文にこれらを named antecedent として掲示せよ。付録 A だけに置くのでは不足である。

### F4.3 \(\hat b_i=b_{\rm op}\): **PASS**

Rule 1 の三 object を辿ると、

1. \(c_i\) は §4.3 の actual intertwinerで、B-4c の \(c_\Lambda\) と同じ source/target・同じ \(\hat F_2\)-equivariance を持つ。
2. (7.1) の \(\zeta_{10}\) は (1.7) の **Rule 1 field generator** で、TB2 root ではない。
3. \(\ell_i\) は Belyi map \(\lambda:W_0\to U\) の \(0\) の正 local monodromyであり、§1.1 の \(x=\gamma_0\) の fiber actionである。ここは同じ底 \(U\) の base coordinate を §1 と §7 で読んでおり、別 object ではない。

従って

\[
c_i\ell_i c_i^{-1}
=\tau_i((\zeta_{10}^{R})^{\hat b_i})
\]

は \(m\) と \(\tau\) の operational twist を測り、

\[
\boxed{\hat b_i=b_{\rm op}.}
\]

**amendment の `b_value_i` は \(b_{\rm op}\) と確定してよい。** Rule 1 結果 record では `b_semantics="op"` を固定値にし、`b_value_i=b_op_value` とする。`b_cmp_value` は別欄・root-system ID 付きでのみ許すべきである。

### F4.4 TB4-E: **証明核 PASS / 定理文の前件脱落**

正の \(x=\gamma_0\) は Kummer torsor 上で

\[
x=m(\eta_M),\qquad
\eta_M=\bar\iota^{-1}(e^{2\pi i/M}).
\]

\(\bar\iota|_K=\iota_\infty\) と Rule 1 (1.6)(1.7) から

\[
\eta_M=\zeta_M^{R}.
\]

さらに actual marking/intertwiner から

\[
c_\Lambda x c_\Lambda^{-1}=\tau(\zeta_M^R).
\]

よって生成元で一致し、

\[
\boxed{b_{\rm op}=1}
\]

である。この経路は \(\sigma_\zeta^{T}\) を通らないので `(Z20-link)` も \(b_{\rm cmp}\) も不要である。

しかし TB4-E の定理文 283 行は A1–A3/C1/C5/C6/A12/A6/(1.8) だけを列挙し、証明 287 行で呼ぶ **B-4c / \(c_\Lambda\) の \(x\)-equivariance** を前件に載せていない。K5 固有定理として書くなら Rule 1 §1.2–§1.5・§4.3 の actual marking/intertwiner を、一般 BFC 定理として書くなら B-4c とその前件を明記せよ。

なお TB4-E は TB4-3 全体でなく TB4-2 の orientation package で足りる。前件を強く置くこと自体は偽ではないが、**使う前件を落とすこと**は許されない。

### F4.5 検出対照表: **FAIL**

TB4 412–425 行と 322–328 行を数えると、

- \(\hat b=9\) として見える: 経路 **1,2,3,4,6,7** — **6 本**。
- 経路 **8** root-object mismatch: \(\hat b=b_{\rm op}=1\) — 見えない。
- 経路 **5** \(n\nmid20\) の root 変更: \(M\mid20\) の測定では \(\hat b=1\) — これも見えない、正確には finite 測定の射程外。

従って、

- 8 経路を母数にするなら **6/8 が見え、2/8 が見えない**。
- finite \(M\mid20\) に適用可能な 7 経路だけを母数にするなら **6/7 が見え、1/7 が見えない**。

「8 経路中 7 本が \(\hat b=9\)」「盲点は root-object mismatch だけ」はどちらの数え方でも偽である。path 5 は `(Z20-link)` の破れではなく **full (Z-norm) の \(n\nmid20\) 部分**の破れなので、運用上の含意もある:

> (7.1) は `(Z20-link)` の代替でないだけでなく、**(Z-norm) 全体の certificate にもならない**。

checker 5(c)(d) は path 8 と embedding reversal だけを検査し、この 8-path count を検査していない。29/29 から検出表の網羅性は出ない。

### F4.6 comparison seal: **設計核 PASS**

`b_semantics` を必須・既定値なしにする判断は正しい。ただし上の型修理を反映し、

```text
root_twist_2M_value
root_twist_mod_M_value
b_cmp_value
b_op_value
b_dictionary = b_op = b_cmp * root_twist_mod_M^{-1}
```

とせよ。`root_twist_mod_M=1` から `(Z20-link)` を推論してはならない。

---

## F5. \(b\)-semantics の最終裁定

今回以後、単一文字 \(b\) を無注記で使うことを認めない。

| 量 | 定義 | 依存 | 運用上の所有者 |
|---|---|---|---|
| \(b_{\rm cmp}\) | \(\varepsilon^{-1}\bmod M\) | TB2 root system と \(x\) の比較 | TB4/BFC の比較帳簿 |
| \(b_{\rm op}\) | \(c_\Lambda m(\xi)c_\Lambda^{-1}=\tau(\xi^{b_{\rm op}})\) | Kummer torsor、actual marking、Rule 1 field generator | bridge predicate |
| \(\hat b_i\) | Rule 1 (7.1) の実測 | \(c_i,\ell_i,\tau_i,\zeta_{10}^{R}\) | Model-Builder / Freeze 2 |

\[
\boxed{\hat b_i=b_{\rm op},\qquad
b_{\rm op}=b_{\rm cmp}\bar t_M^{-1}.}
\]

`(Z20-link)` の下では \(\bar t_M=1\) なので両者は一致する。**一致する規約下で永久に同値に見えることが、同一記号へ融合してよい理由にはならない。**

BFC v2.6 の B-9′ は数学的には救える。両 dessin で共通なのは \(t_{2M}\) も \(\varepsilon\) も framework-level だから、\(b_{\rm op}\) も共通であり、

\[
b_{{\rm op},\rm sq}=b_{{\rm op},\rm ns}
\]

として同じ可換性消去が通る。ただし現 644–668 行は \(b=\varepsilon^{-1}\) と書くので、link-free を主張するなら \(b_{\rm op}\) へ修文が必要である。現行 B-7\({}^{\rm tw}\) proof bundle に `(Z20-link)` を残すなら、その条件下では \(b_{\rm op}=b_{\rm cmp}\) なので定理適用は壊れない。

---

## F6. (α-D) TB4 §8.8 の 7 問

### F6.1 問 1 — TB4-A20 前件

**PASS。** TB4-3 の前件に加え、chosen \(\bar\iota\) の \(K\) への制限、`(Z20-link)`、Rule 1 (1.6) を別立てにしたのは正しい。TB2 整合性は \(n=20\) 一点から mod 20 を出すだけなら不要だが、全 \(M\mid20\) へ降ろす注には使うので過剰ではない。結論の `b=1` は今後 `b_cmp=b_op=1` と型を付けること。

### F6.2 問 2 — (3.3)

**PASS。** \(t_{20}\) を使えば

\[
\varepsilon\equiv t_{20}^{-1}\pmod{20},\qquad
b_{\rm cmp}\equiv t_{20}\pmod{10}
\]

で正しい。\(t_{20}=3\) で \(\varepsilon=7,\ b_{\rm cmp}=3\) も再現する。

### F6.3 問 3 — BFC 波及

**PASS。** 現行 \(\sigma_\zeta\) 経由 proof の B-6 第 3 段が link を使う。B-6/B-7 系への前件追加は正しい。ただし F3.3 の未波及を直すこと。TB4-E は別 proof なので「結論の最小前件」と「現行 proof artifact の前件」を分けて台帳化せよ。

### F6.4 問 4 — 8 経路

**FAIL。** F4.5 のとおり 7/8 ではない。またこの表は「独立 axis の代表例」であって、複数反転の合成まで含む全 counterfactual の悉皆ではない。「8 本ですべて」とは書かず、**単一-axis regression set** と呼ぶのが安全である。

### F6.5 問 5 — `(Z20-link)` だけ先に凍結

**条件付き PASS。** K5 finite layer を先行させること自体は安全で、TB4-A20 と \(M=10\) を閉じる。ただし full `(Z-norm)` の一部を凍結したとは呼ばず、独立 ID の `Z20-link-seal/v1` とすること。Rule 1 / TB4 / BFC / result record が同じ root IDs と equality certificate digest を参照しなければならない。

### F6.6 問 6 — \(\hat b_i\)

**PASS。** F4.3 のとおり \(\hat b_i=b_{\rm op}\)。\(\ell_i\) と \(x=\gamma_0\) は同じ base \(U\) の \(0\)-loop action である。ただしこの同一 object を新 Rule 1 v1.4 の条文にも明記し、単なる同じ glyph に戻さないこと。

### F6.7 問 7 — TB4-E

**定理文修理を条件に PASS。** 結論 \(b_{\rm op}=1\) は `(Z20-link)` 不要である。BFC v2.6 の link 前件は現行 proof path には正しく、今回弱めなくてよい。TB4-E の定理文に actual marking/intertwiner 前件を足し、別 proof ID として射程を記録せよ。

---

## F7. ★教材 T7 方式 — BFC 前件の型列挙

| 主張 | 必要前件 | `(Z_{2M}-link)` |
|---|---|---|
| B-3 | (W1)–(W5) | 不要 |
| B-4(a), B-4c | (W1)(W2)(W3)(W5)+(CAL)、TB1–TB3 間接 | 不要 |
| B-5 | TB1–TB4+(W4) | 不要 |
| B-5\({}^{\rm u}\) | TB1,TB2,TB3,TB4\({}^{\rm u}\)+(W4) | 不要 |
| B-6（現行 proof） | TB1–TB4+(W1)–(W5)+(CAL) | **必要** |
| B-6\({}^{\rm tw}\)（現行 proof） | TB1,TB2,TB3,TB4\({}^{\rm u}\)+(W1)–(W5)+(CAL) | **\(b=\varepsilon^{-1}\) と書くなら必要** |
| B-7 / B-7\({}^{\rm tw}\) | 対応 B-6 を継承 | 同上 |
| B-8 | twisted identity (10.1) | 不要 |
| B-9′ の共通指数・消去 | B-7\({}^{\rm tw}\)+両 (6′-ii)+K5-a | 本質的には不要。ただし link-free 版では指数を \(b_{\rm op}\) と書く |
| TB4-E alternate | TB4-2 orientation package + Rule 1 marking/intertwiner | 不要 |

この表から、BFC 560・565–566・644 行のどこを同期すべきかが一意になる。

---

## F8. (β) 単一 version event の裁定

**不許可。S5 Model-Builder の unlock も本便からは出さない。**

再提出の最小条件は次の 6 件。

1. TB4 の \(t\) を \(t_{2M}\) と \(\bar t_M\) に分け、`(Z20-link) iff t=1` の型落ちを直す。
2. TB4-D/E と \(\hat b=b_{\rm op}\) の theorem statement に、proof が使う \(c_\Lambda\)/actual marking/intertwiner 前件を明記する。
3. TB4 の 8-path 検出数を `6/8` または finite 射程の `6/7` に直し、(7.1) は Z20/Z-norm の certificate でないと明記する。
4. BFC v2.6 の 519–522、560、565–566、614、697、1007、1063–1066 等を \(b_{\rm cmp}/b_{\rm op}\) と link 前件へ同期し、一般 theorem の `(Z_{2M}-link)` と K5 の `(Z20-link)` を分ける。
5. amendment の theorem bundle を predicate-version 別に一意化し、`b_value_i=b_op`、`b_semantics="op"` を operative schema に入れる。
6. status-layer の本文複製を除去し、`provenance/CLAIMS.md` を現 certificate へ同期する。BFC を編集した最終 digest に GAP certificate を再束縛する。

この 6 件が閉じた次便では、次の **版イベント設計そのもの**は再利用できる。

- Rule 1 v1.4: amendment v3 + §7.4 quarantine + finite/full root seals + A3 seal + typed \(b\) semantics。
- manifest v1.6: BRIDGE-FAIL ①差し替え、twisted/exact bundle ID、結果 schema 同期。
- TB1/TB3/TB4\({}^{\rm u}\)/A3 = framework、TB2+root seals = workshop convention、TB4-A20/B = finite/profinite theorem の別札。
- 文献要請 13(ii) は A3 の comparison orientation だけへ縮小維持。
- B-9′(e′) は amendment 成立後、**operational exponent を \(b_{\rm op}\) とした形**で復帰。

これは将来の再提出条件を示すもので、今回の事前承認ではない。

---

## F9. ★教材

1. **剰余へ射影した unit は、元の root equality を証明しない。** \(t_{10}=1\) でも \(t_{20}=11\) は残る。seal の equality level と定理が見る modulus を同じ欄に潰してはならない。
2. **proof が named object を呼んだら theorem statement の前件表にも出す。** TB4-E の最後の一行が正しくても、\(c_\Lambda\) の出所を前件から落とせば theorem gate は閉じない。
3. **有限 diagnostic は profinite normalization の証明書にならない。** path 5 は \(M=10\) の測定に映らない。検査対象外を「盲点ではない」と数え直して 7/8 にしてはならない。
4. **status を外部化するなら、本文の live status copy を全部消し、外部台帳を実際に更新する。** 「外部が正」と宣言しながら外部が旧 17/17 のままでは参照化は完成しない。
5. **同じ量名も typed equality を要する。** \(b_{\rm cmp}\) と \(b_{\rm op}\) が seal 下で一致することは、seal 外の countermodel で同じ量であることを意味しない。

---

## F10. 共同設計者としての発案

### F10.1 `TB4-b-dictionary/v1`

```text
modulus_2M
root_system_tb2_id
rule1_root_2M_id
root_twist_2M_value
root_twist_mod_M_value
epsilon_cmp_value
b_cmp_value
b_op_value
b_dictionary_proof_id
b_value_i = b_op_value
b_semantics = "op"
```

次の invariant を checker に入れる。

```text
b_cmp = epsilon_cmp^{-1} mod M
b_op  = b_cmp * root_twist_mod_M^{-1} mod M
Z2M_link_pass => root_twist_2M = 1
root_twist_mod_M = 1 !=> Z2M_link_pass
```

最後の negative fixture は \(M=10,\ t_{20}=11\) とする。

### F10.2 regression 表を二つに分ける

- **finite operational orientation suite**: paths 1,2,3,4,6,7,8。期待 `6 detected / 1 root-link blind`。
- **profinite root-normalization suite**: path 5 と全 \(n\nmid20\)。期待 `finite b measurement out-of-scope`。

これで「検出できない」と「測定宇宙に入っていない」を混ぜずに済む。

### F10.3 theorem bundle ID

```text
THEOREM-ANTECEDENT-Rcyc/twisted/v1
THEOREM-ANTECEDENT-Rcyc/exact/v1
FALSIFIER-ANTECEDENT-BFC/twisted/v1
```

predicate、前件、結果 record の三つを同じ ID で束縛すれば、exact と twisted を prose の括弧書きで再融合する事故を防げる。

---

監査範囲外は、K\(^{(5)}\) の個別モデル・\(u\)・封印値、S5/Model-Builder 探索、Lean 形式化、外部文献の原文照合である。GAP artifact は certificate の schema/digest/provenance を検収したが再生成していない。実行した機械計算は上記 Node 2 本のみで、いずれも既存 artifact の再走である。本返信以外の作業ツリーは変更していない。
