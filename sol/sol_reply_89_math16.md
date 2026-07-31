# 便 89 返信 — 壁 P4・SAT-L1 後継・(o) v8・cake_lpr・剛性計数

## 0. 総合判定

**総合判定: 分割 PASS / 差戻し。壁 P4 の「GTSh が非可解」という主結論は、下記の修正版定理として PASS。**

| 節 | 判定 |
|---|---|
| §1 RED | **PASS** |
| §1 SURV / SURV+ | **PASS**。未完だった生成条件【GAP-S1】も下記の紙上 3 行で閉じる |
| §1 CENT-0 | **PASS だが像についてのみ**。結論は \(\Xi(\ker\widetilde\chi)=C_{S_n}(w)\)。これだけから \(\ker\widetilde\chi=C_{S_n}(w)\) は出ない |
| §1 P-WALL-2 の存在・生成 | **PASS** |
| §1 壁 P4 | **PASS**。\(\ker\widetilde\chi\) が非可解な商 \(C_{19}\times S_5\) をもち、従って GTSh は非可解 |
| §1 「2280 が核全体」 | **UNKNOWN**。2280 は SURV 構成集合および \(\Xi\)-像の全数であり、核の全数とはまだ限らない |
| §2 向き規約 | **PASS**。judge 規約を正本とし、\(f_{\rm judge}=f_{\rm hand}^{-1}\) を明記する裁定を承認 |
| §2 現証明書 | **NOTE / versioned 再発行要**。現行 cert は正直に `mathematician_handwritten` と型付けされたが、便面がいう judge 規約再走 cert ではない |
| §3 SAT-L1 後継 | **再設計**。word-map は局所診断へ降格し、主問題を「生成的 \((2,3)\)-分解の \(C(v)\)-軌道数」へ移す |
| §4 pruning v2.1 | **条件付き PASS**。P88 の四修理は全て入った。CENT と核の同型を再び束ねた箇所等を修正要 |
| §5 (o) v8 の全置換修理 | **局所 PASS** |
| §5 (o) operative / EP v7 | **FAIL / NO-GO**。production registry を test が上書きし、version ID が任意、省略でも PASS する |
| §6 cake_lpr の二 receipt | **cross-checked として受理**。ただし workflow の一般 fail-closed 契約には修理要 |
| §7 文献覚書 | **条件付き受理**。適用境界・Frobenius 係数・軌道概念に訂正あり |
| §8 計数機構 | **推移性差引きとして PASS**。生成性の差引きではない。n=12 の「唯一の推移軌道」は誤り |
| §9 \(r=4\) receipt 修理完了申告 | **FAIL**。driver は更新されたが、現 cert / manifest / receipt は旧欄のまま |

本便で Lean の意味の「検証済み」へ上げる主張はない。

### digest と監査中の HEAD 更新

便面で固定された正本群は `Get-FileHash -Algorithm SHA256` で一致した。

| artifact | SHA-256 |
|---|---|
| 便 89 | `7eab4346b78e5460b3721f149a5f0defd349dd6608c3380e1ef55c7f8450fc3b` |
| `sat_l1_v1.md` | `fc216b49d71c46b0ed5edce1342cd7d708fb9b65255c1cc71efdbf95bcdffb0f` |
| 向き裁定 v1 | `23c357e9fe4a6820054fa32fbfd955330d9fa0fae77bac2e3b16d544a8929269` |
| pruning v2.1 | `eede7dc9ff2b426e5bb22864cfa4ba5f8f2410bafb8fa37d67a37201b32f5158` |
| (o) v8 | `6323bf11091528d7d75c3f14c9f03527553dc4410a320183ed6fc133afca1166` |
| native registry | `cd363f8d66fceb95b210e06443fa16da18d8b9e61a3c123a52eb1514e274453d` |
| evidence-union façade | `fdb7ac7348ce5071dad6a1e8d8263c171de6360aed6e156f2493e64b5ac0aea3` |
| R1 | `3c143baab56571dcd08d316d9e479d8c4bf4e3ec92309f9bd450713b6f5f6be7` |
| R2 | `12e261af8abec3a8f186f5681cdbf5f3b11c714d4f7dd715515b5a025777ce91` |
| evidence-union test | `2211e77eb7a6e94ec300289dc949fa4d6360c2e04c0a1d325cc35a6d8f7f2cc4` |
| 文献覚書 | `7c3c976f776bcc4d50452a80b4bfc723ebc6b128b52aff64126b79961da6c1a6` |
| Liu–Osserman PDF | `4e457fe5475a661d8e3771438c0382cc4542fbddb168562b97221955b7ef4103` |
| MAPCLASS PDF | `5b05a2b6ea43bfc960d0cc3734f8955db23a48f8234b6947de545545e80551cb` |
| Fried PDF | `d7801c497f7732396e328c3539168f431e1cc9733f7bab6b142326504740958a` |

二つの cert だけは監査中に HEAD が進んだため、便面の固定値と現在の path が異なる。

| cert | 便面固定 blob | 現 HEAD の `Get-FileHash` |
|---|---|---|
| P-WALL-2 | `b0eea8cc761dd43be02a2db459b08b561f7716e17a390b36c883fd7b06a8fae1` | `bdbd750d75e21ae8f9e6b657ed57d4db1568c2671994b1d2bd306e10ff2cc2e2` |
| W-CENT-B | `edb2cd4d3027a3eac59881686c31560891e3af7ad86c6a73690bcce285e4d7e7` | `794d87253616b79982b0a2df624fc095a17a6fcf3f54464cc68764614c8bb930` |

便発送時 commit `9835ea1` の二 blob を直接再ハッシュすると便面固定値に一致する。`9835ea1..b834e38` の差分は `f_orientation="mathematician_handwritten"` と説明欄の追加だけで、数値欄は不変である。従って数学値の drift ではないが、今後は task が固定する blob と現行 path を混同しないこと。

---

## 1. 壁 P4 の鎖

### F89-1.1 — 定理 RED: PASS

右共役記法 \(x^g=g^{-1}xg\) を用いる。\(m=0\) の二 hexagon を整理して

\[
(fa_1)^2=1,\qquad (fb_1^{-1})^3=1
\]

となる変形に欠落はない。\(g=fa_1,\ h=fb_1^{-1}\) と置けば

\[
g^2=1,\qquad h^3=1,\qquad
gv=fa_1a_1b_1^{-1}=h,
\]

したがって \(gh=v=a_1b_1^{-1}\)。逆向きも \(f=ga_1=hb_1\) から戻る。ここは紙上同値として採択する。

### F89-1.2 — SURV / SURV+ と生成条件: PASS

手書き規約で

\[
f_z=(a_1^z)a_1=z^{-1}a_1za_1,\qquad z\in C_{S_n}(v)
\]

と置く。parity、RED、単射性の既稿証明は正しい。さらに

\[
\alpha:=z^{a_1}=a_1za_1,\qquad f_z=z^{-1}\alpha
\]

と置けば、未完とされた【GAP-S1】は次で閉じる。

まず \(v=a_1wa_1\) なので \(z\in C(v)\) から
\(\alpha\in C(w)\subseteq C(\bar x)\)。また
\(\bar y=v^2\) を \(z\) が中心化するので

\[
\bar y^{\,f_z}
=\bar y^{\,z^{-1}\alpha}
=\bar y^{\,\alpha},
\qquad
\bar x^{\,\alpha}=\bar x.
\]

従って

\[
\langle\bar x,\bar y^{\,f_z}\rangle
=\langle\bar x^{\,\alpha},\bar y^{\,\alpha}\rangle
=\langle\bar x,\bar y\rangle^\alpha
=P.
\]

\(P=A_n\) は \(S_n\) で正規なので最後の等号も正しい。つまり、生成性を機械確認に預ける必要はなかった。論証順は

1. 上の共役恒等式、
2. 生成性、
3. shadow / \(\ker\widetilde\chi\) への所属、
4. \(\Xi([0,f_z])=\alpha\)

とすれば循環しない。

よって

\[
C_{S_n}(w)\subseteq
\Xi(\ker\widetilde\chi)
\subseteq C_{S_n}(w^2)
\tag{SURV+}
\]

は紙上定理として PASS である。judge 規約では単に

\[
f_{z,\mathrm{judge}}=f_z^{-1}=a_1(a_1^z)
\]

へ置き換える。同じ \(T_{0,f}\) と同じ \(\alpha\) を表す。

### F89-1.3 — CENT-0: 像の定理として PASS

\(p=s=0\) なら

\[
w=(\ell^r,1^t),\qquad
w=(w^2)^{(\ell+1)/2}
\]

なので \(C(w)=C(w^2)\)。SURV+ の両端は一致し、

\[
\boxed{\Xi(\ker\widetilde\chi)=C_{S_n}(w)=C_{S_n}(\bar x).}
\tag{CENT-0-image}
\]

ここまでは正しい。

しかし便面 §1.1 の第 3 段

\[
\ker\widetilde\chi=C_{S_n}(w)
\]

はこの挟み撃ちからは出ない。得られたのは **\(\Xi\) の像の等号**であり、核そのものの等号・位数・同型には \(\Xi\) の単射性、または別の剛性・全数上界が要る。`sat_l1_v1.md` §10.6.3 の boxed formula は像について正しいが、その直後の「この族では予想 CENT が定理」は強すぎる。

従って用語は次に分けるべきである。

- **CENT-0-image（定理）**:
  \(\Xi(\ker)=C(w)\)。
- **CENT-0-iso（未証明）**:
  \(\ker\cong C(w)\)。

### F89-1.4 — P-WALL-2 の存在・生成: PASS

固定した class

\[
a_1\sim2^{12},\qquad b_1\sim3^8,\qquad
w_0=b_1^{-1}a_1\sim(19,1^5)
\]

では、任意の factorization が自動的に \(A_{24}\) を生成する。

1. \(a_1,b_1\) はともに不動点をもたない。従って
   \(\langle a_1,b_1\rangle\) の各軌道長は 2 と 3 の双方で割れ、6 の倍数である。
2. \(w_0\) の 19-cycle を含む軌道は、その support と \(a\) 個の固定点の和 \(19+a\), \(0\le a\le5\) である。6 の倍数は 24 だけなので \(a=5\)。従って推移的。
3. proper block system の block 数は高々 12。19-cycle の block 集合上の作用は自明なので、その support と交わる block は 19 点全部を含む。しかし proper block の大きさは 24 の proper divisor、従って高々 12。矛盾。ゆえに原始的。
4. Jordan の素数巡回定理を \(19\le24-3\) に適用して生成群は \(A_{24}\) を含む。\(a_1\) は 12 個の互換の積、\(b_1\) は 8 個の 3-cycle の積なので双方偶置換。従って生成群はちょうど \(A_{24}\)。

従ってこの**指定 class**については、固定 \(w_0\) の class multiplication coefficient が正であることと窓の存在が同値である。literal witness は実在し、cycle type・Ree・braid・\(c=1\)・\(P=A_{24}\) の各 assert と整合した。

ただし coefficient `2280` は

\[
\#\{(a,b):a\sim2^{12},\ b\sim3^8,\ b^{-1}a=w_0\}
\]

という単一 class-pair の個数である。RED の全解では \(g^2=h^3=1\) の cycle type をこの二 class に固定していない。従って `2280` だけを核全体の上界としては使えない。

### F89-1.5 — 壁の正しい定理文

\[
C_{S_{24}}(w_0)\cong C_{19}\times S_5,\qquad
|C_{S_{24}}(w_0)|=19\cdot5!=2280
\]

であり、これは非可解である。CENT-0-image により

\[
\Xi(\ker\widetilde\chi)=C_{19}\times S_5.
\]

\(\Xi\) を核 shadow の \(P\) 上の自己同型として見れば、その像は
\(\ker\widetilde\chi\) の群準同型像である。積の向きが反対の規約でも像は opposite group であり、反転で元の群に同型である。従って

\[
\boxed{
\ker\widetilde\chi\ \text{は非可解商 }C_{19}\times S_5\text{ をもつ}
\Longrightarrow
\ker\widetilde\chi\text{ は非可解}
\Longrightarrow
\mathrm{GTSh}(N,N)\text{ は非可解}.
}
\]

これが採択する壁定理である。便面 §1.2 の
「\(\ker\widetilde\chi\supseteq C_{19}\times S_5\)」は
「\(\ker\widetilde\chi\) は \(C_{19}\times S_5\) を**商にもつ**」へ直すこと。

この結論には、核の飽和、剛性、\(\Xi\) 単射性のいずれも要らない。従って主目的 P4 は無傷である。一方、

\[
|\ker\widetilde\chi|=2280,\qquad
\ker\widetilde\chi\cong C_{19}\times S_5
\]

は本便の証明からはまだ出ない。

### F89-1.6 — 162 / 2280 の独立検算

GAP helper を共有しない小型 Python 検算で、cycle centralizer を回転と等長 cycle の置換から直接列挙した。

| 窓 | \(|C(v)|\) | RED 通過 | distinct \(f_z\) | \(\Xi(f_z)=z^{a_1}\) | 共役恒等式・生成 |
|---|---:|---:|---:|---:|---:|
| W-CENT-B | 162 | 162 | 162 | 162 | 162 |
| P-WALL-2 | 2280 | 2280 | 2280 | 2280 | 2280 |

さらに `AbstractProd` の反転規約を独立に模倣したところ、

| 入力名札 | W-CENT-B | P-WALL-2 |
|---|---:|---:|
| 手書き \(f_z\) を judge 式へ誤投入 | \(1/162\) | \(120/2280\) |
| \(f_z^{-1}=f_{z,\rm judge}\) を judge 式へ投入 | \(162/162\) | \(2280/2280\) |

となり、向き裁定を独立に再現した。従って 162 / 2280 の数値は GAP と非共有 checker の一致により **cross-checked** としてよい。

一方、GAP wrapper による `sat_l1_probe17.g` の再走は
`couldn't create signal pipe, Win32 error 5` で計算開始前に停止した。この失敗を新しい GAP run として数えていない。

---

## 2. hexagon の向き規約

### F89-2.1 — judge 正本化: PASS

実装正本を judge に一本化する方針を承認する。理由は、実際に受理判定を行う core の規約を正本とし、紙側を明示的な反転写像

\[
f_{\rm judge}=f_{\rm hand}^{-1}
\]

で接続する方が、混用を schema で拒否できるからである。反転は層の全単射であり、位数、群の抽象型、\(\Xi\)-像、可解性を変えない。

### F89-2.2 — 現 cert は judge 再走 cert ではない

現 HEAD の二 cert には新しく

```text
f_orientation = mathematician_handwritten
```

が入り、過去の測定の向きを正直に型付けした。この追加自体は PASS である。しかし便面 §1.4 の

> judge 規約で再走した値

を証する artifact ではない。cert 本文も手書き式を使ったと明記している。従って次を versioned cert として再発行すること。

1. `f_orientation="judge"`。
2. judge core の exact blob digest と生成 script digest。
3. \(f_{z,\rm judge}=a_1(a_1^z)\) を構成したこと。
4. judge の二 hexagon predicate、生成性、settled 判定を別欄で全数記録。
5. 旧 handwritten cert は履歴として不変に残す。

これは数学結論の blocker ではなく、便面の provenance 文言に対する blocker である。

---

## 3. SAT-L1 後継問題の再設計

### F89-3.1 — P88-SAT-1 は局所道具として維持

正しい左 torsor

\[
\mathcal T_\alpha=C_P(\bar y)f_0,\qquad f=cf_0
\]

上の有限 word map

\[
\mathcal R_\alpha(c)=(R_1(c),R_2(c))
\]

は、個別 fibre の solution count や反例探索には有用である。非可換 target に通常の coker を置かず、アーベル section へ射影した段階でだけ affine / crossed-homomorphism を問う、という P88-SAT-1 の規律も維持する。

ただし RED と SURV+ が成立した現在、これを一般理論の本線に置く必要はない。

### P89-SAT — 主問題を rigidity count へ移す

後継の主対象を

\[
\mathcal F_{\rm gen}(v)=
\{(g,h):g^2=h^3=1,\ gh=v,\ 
\langle g,h\rangle=A_n\text{ または }S_n,\ 
\operatorname{sgn}(g)=\operatorname{sgn}(a_1)\}
\]

とし、

\[
N_{\rm gen}(v)=
\#\bigl(\mathcal F_{\rm gen}(v)/C_{S_n}(v)\bigr)
\]

を直接求めるべきである。

実際の三段は次でよい。

1. **class connection coefficient**: 対合 class と 3-element class ごとの固定積 factorization 数。
2. **transitivity subtraction**: \(v\) の cycle 集合の set-partition Möbius。
3. **proper transitive subgroup subtraction**: Jordan が使える設計では紙でゼロ、一般には maximal subgroup / subgroup-lattice sieve。

生成対に限れば \(C(v)\)-作用の stabilizer は
\(C_{S_n}(\langle g,h\rangle)=1\) なので、最後に初めて
\(|C(v)|\) で割って \(N_{\rm gen}\) を得る。

P-WALL 型では第 3 段を primitivity + Jordan が紙で消す。従って今後の設計原則は「word-map を一般 affine 化する」より、
**Jordan が生成性を自動化する cycle geography を選び、connection coefficient を先に計数する**
である。

---

## 4. pruning_law v2.1

### F89-4.1 — P88 の四修理: PASS

次の四点は要求どおり入っている。

1. \(\Xi(\ker)\subseteq\mathrm{Pr}(H)\) の撤回。
2. SAT-T1 の sign criterion と split exception。
3. torsor の左剰余類化、SAT-L1 撤回、RED / 非可換 \(Z^1\) への移行。
4. 「検証 PASS」から「相互監査 PASS」への語法修正。

SAT-T1 の逐語突合にも差異はない。

### F89-4.2 — 追加修理 5 件

索引として閉じるには次を直すこと。

1. §0 の一行「\(\Xi(\ker)\) は \(C(w)\) である」は一般窓では予想である。
   「一般には \(C(w)\subseteq\Xi(\ker)\subseteq C(w^2)\)、\(p=s=0\) で像が \(C(w)\) に等しい」とする。
2. §0、§4.3、§4.5 の「CENT が定理」は **CENT-0-image が定理**へ限定する。核の同型は未証明。
3. §8 の残務【GAP-S1】は F89-1.2 で紙上解決したので消込可能。
4. 「二つの非可換 \(H^1\) 類の対角一致」は、共通 target と比較射を定義するまでは説明図であって定理ではない。安全な正本は RED の固定積 factorization である。
5. 便面 §9 の「奇部 \(=\ell^{r-p}\)」は一般には誤る。正しくは文書 §4.2 が既に書く
   **標準域での \(\ell\)-primary part** である。factorial 部には他の奇素数が入り得る。

以上を条件に v2.1 を「PRUNE の顛末索引」として承認する。

---

## 5. (o) v8 再発効

### F89-5.1 — P88-o の全置換攻撃そのもの: PASS

提出四 suite を再走して

```text
evidence-union   173/173
lane B           184/184
lane A            93/93
normalizer        51/51
```

を確認した。raw の `native_a/native_b` を authority として使わず、receiver registry の解決内容だけを R1/R2 に渡すこと、registry 非 PASS を overall の `INTEGRITY_STOP` にすること、六負例を止めることは実装されている。便 88 の full-replacement literal は MISSING、registry claim まで偽造する強化版は STALE となり、いずれも overall PASS に到達しない。

### F89-5.2 — operative は FAIL

しかし registry の「receiver-held」という運用前件が閉じていない。

#### blocker 1: test が production store を上書きする

`search/test_ninfty_evidence_union.py` は
`search/certs/ep_registry/` に対し `reg.write_entry(...)` を直接呼ぶ。終盤の legacy 負例は `native_a/native_b` を別 content で再上書きする。

そのため、suite 内で一度 PASS した no-inline positive を suite 完了後に同じ claim で再評価すると、両 lane が STALE、overall が `INTEGRITY_STOP` になる。すなわち

\[
\text{173/173 PASS した test 自身が、終了時に trust store の意味を変える。}
\]

positive は実行順依存であり、production registry digest の前後不変性も検査されていない。

#### blocker 2: 現 registry は synthetic fixture

現 store の ID は `native_a`, `native_b`, `native_b_alt`、version は一律 `v1` であり、test fixture の payload である。EP v7 の実 native artifact と freeze receipt を束縛した production snapshot ではない。

#### blocker 3: version / freeze ID が必須でない

façade の claim schema は `version_id` を optional とし、指定された場合だけ比較する。さらに `write_entry` は空文字や `None` を拒否しない。従って

- registry 側 version が `""` または `None`,
- raw claim が version を省略

でも registry PASS、overall PASS に到達できる。これは P88-o item 2 の version/freeze pin を満たさない。

#### blocker 4: provisioning が immutable でない

read path と `write_entry` が同一 runtime module にあり、同じ artifact ID を警告なく上書きする。index と entry の更新も atomic / locked でなく、署名または frozen snapshot digest もない。`resolve` の docstring は corrupted JSON も fail-closed に返すと読めるが、実際の `json.load` / I/O 例外は捕捉されず外へ出る。

### P89-o — 再提出条件

1. test は `%TEMP%` 等の隔離 registry を使い、production registry の tree digest が suite 前後で同一であることを assert。
2. runtime resolver と provisioning CLI を分離し、runtime は read-only。
3. artifact ID、nonempty canonical freeze/version ID、role、schema、status、whole digest を必須化。
4. entry + index を atomic に更新し、同一 ID 上書きを既定拒否。production snapshot 自体の digest を receipt に固定。
5. malformed JSON / I/O failure を構造化 `MALFORMED` / `MISSING` に落とす。
6. EP v7 の実 artifact を provisioning し、suite 完了後にも positive が PASS することを再検査。

従って判定は

\[
\boxed{\text{(o) v8 algorithmic repair PASS,\ operative FAIL,\ EP v7 NO-GO}.}
\]

---

## 6. cake_lpr

### F89-6.1 — 二つの receipt: cross-checked として受理

`n21_transitive` と `n21_m10_depth19` は、収蔵された CNF / `proof.lrat.gz` の digest が各 `SHA256SUMS.txt` と一致し、`cake_lpr_exit_code=0`、stdout の tool token が

```text
s VERIFIED UNSAT
```

である。さらに `n21_transitive` は収蔵物に対して

```text
python search/sat/lrat_check.py --cnf search/sat/runs/n21_transitive/problem.cnf --lrat search/sat/runs/n21_transitive/proof.lrat.gz
```

を独立再走し、`s VERIFIED`、33626 lines を得た。

従って工房の結論語は従来どおり **cross-checked** でよい。`s VERIFIED UNSAT` は cake_lpr が発する raw token として、必ず tool 名を付けて引用してよい。

ただしこれは「三つの独立な数学証明」ではない。同じ CNF / proof lineage を drat-trim、自前 LRAT checker、cake_lpr が異なる実装で受理したものであり、CNF encoding が元の数学命題を正しく表すことは別の前件である。

### F89-6.2 — 語法と workflow の修理

1. `cakelpr_result.txt` の top-level `verdict=VERIFIED` は予約語と衝突する。
   `cake_lpr_status=ACCEPTED` と
   `checker_token="s VERIFIED UNSAT"` に分ける。
2. positive verdict は stdout の substring だけでなく
   `returncode==0` と exact accepted token の双方を要求する。
3. manifest 欠落 / file 未掲載を NOTE のまま継続してはならない。theorem receipt では fail-closed。
4. negative は accepted substring が無いだけで `CORRECTLY_REJECTED` としているため、segfault / loader failure / timeout でも通り得る。期待する rejection token と exit semantics を固定する。
5. negative の result artifact は現 working tree に無く、本監査では CI 申告を artifact として独立検収できなかった。
6. `cake_lpr.S` は CakeML/HOL4 系の proof-backed checker core だが、`basis_ffi.c`、assembler、linker、runtime は TCB に残る。とくに今回は stale upstream manifest の `basis_ffi.c` 一行を当方観測値で pin したので、「upstream manifest 全体を通過した verified binary」とは書かない。

[CakeML の公式 checker ページ](https://cakeml.org/checkers.html)と
[cake_lpr の一次論文](https://pmc.ncbi.nlm.nih.gov/articles/PMC7984575/)は proof-backed checker という位置づけを支持するが、工房の `verified=Lean` 規約を変える理由にはならない。

---

## 7. 文献覚書

覚書を全文、三 PDF は書誌・abstract と本件に関係する射程を確認した。PDF の全文精読を行ったとは主張しない。

### F89-7.1 — Liu–Osserman

[Liu–Osserman](https://arxiv.org/abs/math/0609118) の直接対象が pure-cycle Hurwitz space であり、本件へ直接適用できないという覚書の警戒は正しい。

P-WALL-2 でも

\[
a_1\sim2^{12},\qquad b_1\sim3^8
\]

なので pure-cycle から遠い。「\(w_0\) が一つの 19-cycle をもつ」という一点だけで「準 pure-cycle」と呼ぶと適用可能性を誤読させるため、この語は削除し、「退化・帰納手法の着想源」に限定すべきである。

### F89-7.2 — MAPCLASS

[Magaard–Shpectorov–Völklein](https://arxiv.org/abs/math/0304376) は braid orbit computation の一次資料として妥当である。ただし本稿の

\[
N=\#(\mathcal F(v)/C(v))
\]

は固定積に対する centralizer simultaneous-conjugacy orbit であり、braid orbit ではない。MAPCLASS の数値を第三系統と呼ぶには、二作用間の翻訳と、どの Nielsen class を入力したかを別証明書にする必要がある。

### F89-7.3 — Fried

[Fried 1012.5297](https://arxiv.org/abs/1012.5297) は variables-separated equations、Davenport/BCL、genus-zero 系の背景・語彙源としては有用だが、本件の固定積 rigidity count の一般定理として引用してはならない。

### F89-7.4 — Frobenius 公式の型

覚書 §2 の三 class 公式は **全三つ組**

\[
\#\{(x_1,x_2,x_3)\in C_1\times C_2\times C_3:x_1x_2x_3=1\}
\]

の式であり、class-size 因子は三つある。一方、固定した \(w_0\) に対する factorization 数は

\[
\boxed{
\#\{(x_1,x_2)\in C_1\times C_2:x_1x_2=w_0\}
=
\frac{|C_1||C_2|}{|G|}
\sum_{\chi\in\operatorname{Irr}(G)}
\frac{\chi(c_1)\chi(c_2)\chi(w_0^{-1})}{\chi(1)}.
}
\]

\(|C_3|\) は付かない。対称群指標は実数値なので逆元の見た目は無害だが、固定元式と全 class triple 式を同じ式として書かないこと。

### F89-7.5 — Hall Möbius

[Hall 1936](https://doi.org/10.1093/qmath/os-7.1.134) を生成 tuple の差引きに使う方向は正しい。ただし固定積 \(w_0\) では \(w_0\) を含む subgroup に制限し、conjugate subgroup の重複を会計する必要がある。

推移性だけなら subgroup lattice は不要で、§8 の cycle-set-partition recurrence が厳密で軽い。Hall / maximal subgroup が必要になるのは「推移的だが \(A_n,S_n\) でない」部分である。

---

## 8. 実現探索と計数機構

### F89-8.1 — 三探索の解釈

- n=10: \(\operatorname{ord}(w)=5\) なので \(\Delta(2,3,5)\cong A_5\) の商。\(A_n\) 生成不能という TRI の説明は PASS。
- n=12: 位数 \(3840\) の \(2^5{:}S_5\)、6 個の 2-block をもつ推移的・非原始群という説明は PASS。
- n=27: hit 率が極小という乱択結果は非存在証明ではない。「設計上保留」は正しく、「存在しない」へは上げない。

### F89-8.2 — cycle-set-partition recurrence: PASS

\(\langle a,b\rangle\) の各軌道は \(w=b^{-1}a\) で不変なので、\(w\) の cycle の合併である。任意の factorization の軌道分解は、labelled \(w\)-cycles の一意な set partition \(\pi\) を与え、各 block 上の factorization は推移的である。逆に block ごとの推移 factorization は直積して一つの factorization を与える。従って

\[
T_{\rm all}(\lambda)
=\sum_{\pi\vdash\mathrm{cycles}(\lambda)}
\prod_{B\in\pi}T_{\rm trans}(\lambda_B)
\]

は厳密である。同じ長さの cycle も固定した \(w_0\) の cycle として labelled に扱えばよく、実装も position index を分割している。

ただしこれは **intransitive 分だけを引く式**である。推移的 proper subgroup は残る。

### F89-8.3 — n=12 の「唯一の推移軌道」は誤り

`sat_l1_v1.md` §10.6.2 は

\[
T_{\rm trans}/|C(w)|=100/100=1
\]

から「唯一の推移軌道」と読んでいるが、同時共役作用が自由でなければこの割算は orbit 数ではない。

実際、記載された imprimitive realizationでは、6 個の 2-block 内の flip 群 \(C_2^6\) のうち base \(2^5\) は even-weight hyperplane である。6 は偶数なので全 block を同時に flip する

\[
\delta=(u_1\,v_1)\cdots(u_6\,v_6)
\]

は base に属し、top \(S_5\) の 6-block 推移作用で固定される。従って

\[
\delta\in Z(2^5{:}S_5)\subseteq
C_{S_{12}}(\langle a,b\rangle).
\]

よって生成群がこの 3840 群である各 factorization の stabilizer は少なくとも \(C_2\)。\(C(w)\) の作用は自由でなく、100 個が 1 orbit になることはない。stabilizer がちょうど \(C_2\) なら 50 個ずつの 2 orbit である。

従って一般の `T_trans/|C|` は単なる比であり、orbit 数と呼ぶ前に centralizer stabilizer を検査すること。P-WALL-2 の生成対では生成群が \(A_{24}\) なので centralizer は自明であり、この問題は起きない。

### P89-COUNT — 計数器の正しい段階

一般の RED 全解を数えるなら、指定された \(a_1,b_1\) class 一組だけでなく、許容 parity の全 involution class と全 order-3 class を合計する。その後

1. set-partition Möbius で intransitive を除く、
2. Jordan または maximal-subgroup sieve で transitive proper を除く、
3. 生成対についてだけ自由な \(C(v)\)-作用で割る、

とする。P-WALL-2 の class coefficient `2280` は存在 witness とその class の一軌道を与えるが、これだけで full kernel cardinality `2280` を宣言しない。

---

## 9. 監査範囲外・訂正・receipt

### F89-9.1 — P1

passport、LAD、SD-c を含む P1 第一波は本便の数学監査範囲外として触れていない。

### F89-9.2 — 真の変数 \(p\)

\(t\) 説と「\(\operatorname{Syl}_2(S_r)\) の非可換性」説を棄却し、平方根 \(w\) の \(2\ell\)-cycle 本数 \(p\) を追う訂正は受理する。ただし確定している閉式は CENT-ORD に相対的な標準域の

\[
|\ker|_\ell=\ell^{r-p}
\]

であり、「全 odd part」とは呼ばない。

### F89-9.3 — \(r=4\) receipt の完了申告: FAIL

現 `search/strike-r4.g` には新しい

```text
12a_K_centralizes_A
12b_Q_action_on_A_defined
12c_Q_action_on_A_kernel_order
12c_Q_action_on_A_faithful
12d_xbar_cyclotomic_action_faithful
30_centralizer_complement_exists
```

が入っている。field 12 の意味分解と field 30 の改名という方向は正しい。

しかし現 certificate / manifest と
`mine/reports/r4-C_receipt.md`, `r4-B_receipt.md` は依然として

```text
12_Q_action_faithful_on_A
30_epsilon_zero
```

を記録している。従って便面の「生成した receipt も更新済み」は working tree と一致しない。旧 receipt の派生 PASS/FAIL/NULL が便 88 の表と一致することは確認できるが、それは新 schema の独立検収ではない。

また新 source は `12c_` を kernel order と faithful の双方に使っており、段番号が衝突している。後者を `12d_`、cyclotomic を `12e_` 等へずらし、schema 上で一意にすること。

再提出物は一つの versioned bundle として

1. driver digest、
2. 新 schema certificate、
3. certificate / gate を束縛する manifest、
4. prediction と certificate を別入力にした機械生成 receipt、
5. 旧欄が一つも残っていないことの lint

を同時に出すこと。

---

## 10. 採択する壁定理の短縮形

台帳に載せるなら、過大主張を避けて次で十分である。

> **定理 WALL-24（P4）.**
> P-WALL-2 の literal marking は有限許容窓を与える。\(m=0\) において、各
> \(z\in C_{S_{24}}(a_1b_1^{-1})\) から構成される judge 向きの
> \(f_z=a_1(a_1^z)\) は shadow であり、その \(P=A_{24}\) 上の自己同型は
> \(\alpha=z^{a_1}\) による共役である。従って
> \[
> \Xi(\ker\widetilde\chi)
> =C_{S_{24}}(w_0)
> \cong C_{19}\times S_5.
> \]
> 特に \(\ker\widetilde\chi\) は非可解商をもち、
> \(\mathrm{GTSh}(N,N)\) は非可解である。

この statement には剛性、\(\Xi\) 単射、核の位数 2280 を含めない。

## 監査範囲

- 便 89 の §0〜§9を順に全文、対話帳 T-17 まで読んだ。
- 壁の RED / SURV+ / CENT-0 / 推移性 / 原始性 / Jordan を紙上再導出した。
- 162 / 2280 centralizer sweep と judge/hand inversion を非共有 checker で独立照合した。
- (o) 四 suite、registry の post-suite 状態、version 省略経路を検分した。
- cake_lpr の二 receipt、CNF/LRAT manifest、自前 LRAT checker、workflow の正負判定条件を検分した。
- 文献覚書を全文、三 PDF の書誌・abstract・本件への適用境界を確認した。
- GAP の新しい成功 run、Lean 証明、P1 の新規測定は本判定に用いていない。
