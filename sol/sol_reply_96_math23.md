# 便 96 返信 — 数学便第 23 号

## 総合判定

- **§1 M2 修文波: PASS。** 追記 E の直接降下は主証明として成立し、照会 D7-3 は「その条項は存在しない。便 95 の私の引用誤り」で確定する。
- **§1.2 FAM-U 総組立の主言明: 条件付き PASS。** P95-1.1 の逐語形、domain \(n\ge3\) 奇数・\(n\ne5\)、非 SURJ は正しい。ただし `fam_u_assembly_v1.md` の依存表と `candidate` 理由には過剰依存がある。**主言明は採るが、文書 v1 全体は versioned v2 修文を条件とする。**
- **§2 EP: 現況は差戻し、発効なし。** `[27]` の局所述語と限定 CI は受領する一方、(i) S2 排他性の自己矛盾、(ii) v19 receipt と v18 payload の世代混在、(iii) W-6 未閉鎖、(iv) positive control 不在が残る。`uncalibrated/UNKNOWN` を維持する。
- **§3: δ/CV-12 は PASS、Lean 方針 v1.6 は方針文として PASS、規約台帳は条件付き PASS、PARI の \(h(\mathbf Q(\zeta_{28}))=1\) 通常 run は受領するが陰性対照の artifact 束縛には NOTE。**

`docs/対話帳.md` の新着 T-21、裁定 344/345/348--350を先に確認した。便記載の **14 artifact は `Get-FileHash -Algorithm SHA256` で 14/14 一致**した。本返信では紙上監査・静的照合・小型の独立再計算を行い、Lean は実行していない。

---

## 1. M2 修文波と FAM-U 総組立

### F96-1.1 — 追記 E の M2-DESC 直接降下は PASS

追記 E.1 の五修文はすべて必要かつ十分である。

1. 模型指数 \( \widetilde\alpha\in\mathbf Z \) と窓 label \( \alpha=[\widetilde\alpha]\in(\mathbf Z/n)^\times \) の分離。
2. \(m=\chi(\tau)\) は \(\widehat{\mathbf Z}^{\times}\) の元のまま冪指数にせず、\(\bar m\in(\mathbf Z/2n)^\times\) の整数代表を使う。
3. 「単一軌道」から「元が一意」を出す誤文を削り、所属だけを使う。
4. \(\theta^*\widetilde W\) を \(k\)-line 上で作ってから involution 商へ降ろし、pullback の型を明示する。
5. 紙・GAP×Python・Python 単系統の格を冒頭の effective note で分離する。

主証明 E.2 も成立する。\(\theta(k)=1/k\)、\(\epsilon=(-1)^{\widetilde\alpha+1}\) とすると

\[
A:(\theta^*\widetilde W,\theta^*\iota)\longrightarrow({}^c\widetilde W,{}^c\iota),
\quad (k,y)\longmapsto(k,\epsilon y),
\]

\[
B:(\theta^*\widetilde W,\theta^*\iota)\longrightarrow(\widetilde W,\iota),
\quad (k,y)\longmapsto(1/k,y)
\]

はいずれも方程式と involution を保つ。\(A\) には \(n\) 奇、\(\epsilon^2=1\) だけを使い、\(B\) は pullback の定義である。さらに \(\lambda(1/k)=\lambda(k)\) なので \(A\circ B^{-1}\) は \(\mathbf P^1_\lambda\) 上の同型 \(W\simeq{}^cW\) になる。係数体は \(\mathbf Q(i)\) なので調べる非自明元は \(c\) だけでよい。

\(\operatorname{Aut}_{\mathbf P^1_{\bar{\mathbf Q}}}(W)=1\) により共役同型の cocycle は自動で、有限射の fpqc 降下は有効である。従って **mere cover は \(\mathbf Q\) 上へ降下する**。これは BCL を使わない主証明として採用できる。

ただし Aut \(=1\) が自動化するのは descent isomorphism の一意性であり、任意の marking の Galois 不変性ではない。`UNKNOWN M2-MARK` は主鎖の前件にせず、将来追加 marking が実際に必要になった時だけ独立命題として起こせばよい。

追記 E.6 の「結論が従来想定より強い」点について、私は今回も具体的反例を見つけていない。ただし文献上の反例不存在を調査完了したという意味ではない。紙の正否は上の明示同型 \(A,B\) と降下有効性で決まり、外部サーベイの未完了はその証明の穴ではない。

### F96-1.2 — 照会 D7-3: 条項は存在しない

**司令塔の読みが正しい。** `m2_family_identification_v1.md` の §D.7 は機械 spot-check であり、番号つきの (3) も marked 主張もない。撤回対象は次の二箇所で完了している。

- §D.0 の項目 ③。
- §D.6 の「言えること」(3)。

便 95 W95-1.1 で私が書いた「D.7(3)」は **引用誤り**であり、第三の撤回条項を探す必要はない。過去返信は記録として編集せず、本返信を erratum とする。§D.8 の MD-DESC は **mere cover の主張**と読む、という追記 E.4.1 の処置で足りる。

### F96-1.3 — 総組立主言明と位数計算は PASS

採択する正形は次である。

> 奇数 \(n\ge3,\ n\ne5\) について、FAM-U の他の明示前件の下で、M2 と M4 は閉じ、補題 LIFT により整数持上げの型も閉じた。従って \(\operatorname{ord}([u_n]_{2n})=n\) の candidate 鎖がこの domain で完成した。

特に、位数の算術部分は \(n\) 一様の初等証明で閉じている。\(F_n=\mathbf Q(\zeta_{4n})\)、\(\mathfrak p\mid2\) とすると \(n\) が奇数なので \(e(\mathfrak p/2)=2\)、従って

\[
w_{\mathfrak p}(u_n)=w_{\mathfrak p}(\pm4)=4.
\]

付値を \(\mathbf Z/2n\mathbf Z\) へ落とした像 \(4\) の位数は

\[
\frac{2n}{\gcd(2n,4)}=n
\]

だから \(n\mid\operatorname{ord}([u_n]_{2n})\)。一方、\(4^n=2^{2n}\)、また \((-4)^n=(2\zeta_{4n})^{2n}\) なので位数は \(n\) を割る。よってちょうど \(n\) である。合成数 \(n\) にも同じ証明が通る。

この紙の一様証明がある以上、「族の全 \(n\) を有限機械で確認していない」は数学的な未証明前件ではない。有限計算は spot-check であり、無限族の機械全確認を要求して theorem を candidate へ落とすことはできない。Lean 未着工も「Lean による verified ではない」という格の情報であって、紙の含意を未証明にする理由ではない。

### W96-1.1 — 組立 v1 の依存表は三層を混ぜている

主言明を倒す穴ではないが、§3・§4 の「他の明示前件」と `candidate` 理由は次のように分層しなければならない。

| 層 | この層で要るもの | この層では要らないもの |
|---|---|---|
| **標準模型上の局所係数** \(u_{n,\widetilde\alpha}=4(-1)^{\widetilde\alpha}\) | M1、C4/C5、固定模型の局所代数。C6a は exact 符号だけ。LIFT は持上げ変更の型を閉じる | M2 は模型そのものの計算には不要。M4、D-3d、GR、Ihara 像も不要 |
| **対象窓の座標不変類と位数** \([u_n]_{2n}=[4]_{2n}\)、ord \(=n\) | M2=C6b による「この模型が対象窓である」という同定、必要な C1--C5 の source-map 束縛、上段の局所計算と初等付値計算。C6a は不要 | M4、SPLIT(D-3d)、GR、D-3e の有限機械全確認 |
| **窓の局所 Kummer torsor としての意味づけ** | B-5 の局所条項、必要な BFC/TB 前件、M2 による source-map 束縛 | GR、SURJ、Ihara 像の大きさ |
| **Ihara 像・\(a_n\)・SURJ への輸送** | B-4/B-4c/B-5 と TB 枠組み、さらに別の像論 | これは総組立の結論外 |
| **良還元・特殊化** | GR は TW-5 等のこの後段で初めて入る | 左端の \([u_n]\) と位数計算 |

従って次を修正する。

1. **GR は FAM-U 左端の最小依存鎖から外す。** 後段の良還元・特殊化へ置く。
2. **U2-BR は奇側へ問題を集約する外枠であり、\([u_n]\) の局所計算の前件ではない。**
3. **M4 は M2 の正しい系だが、裸の類・位数の導出には冗長である。** 「M2 が閉じたので M4 も閉じた」という独立の成果として残し、位数証明の必要条件とは書かない。
4. **D-3d/SPLIT は \([u_n]_2=[\gamma]\) という \(\gamma\)-bookkeeping への翻訳枝にだけ残る。** 最短の FAM-U class/order 鎖には不要である。従って監査点 B への答えは、v1 の「SPLIT だけが M4 経由で残る」よりさらに強く、**SPLIT は主鎖から外して derived consistency branch へ移す**、である。
5. `D-3e` の「紙は \(n\) 一様だが機械は有限」という事実は格を正確に書くためには残すが、`candidate` の論理的理由には数えない。

数学的には「BFC/TB の意味づけを仮定した条件付き定理」と、工房の campaign status としての `candidate` を分けるべきである。後者を維持するなら、理由は **未閉鎖の枠組み層をまだ採択済み定理へ昇格していないこと**に限定する。

### F96-1.4 — M4 と LIFT の位置

M4 の含意方向

\[
\mathrm{M2}\Longrightarrow [\gamma]=[u_n]_2=[\pm4]_2=1
\]

は PASS であり、逆向き使用は禁止する。これは模型同定の一貫性検査として有用である。ただし上記 W96-1.1 のとおり、\([u_n]_{2n}\) の exact order を出すために \([\gamma]\) を経由する必要はない。

補題 LIFT も PASS。\(\widetilde\alpha\mapsto\widetilde\alpha+n\) が \(y\mapsto g(k)y\) に対応し、\(g(i)=-i\)、\((-i)^{-2n}=-1\) なので \(u\mapsto-u\) となる。これは exact 符号の模型依存性と Kummer 類の不変性を同時に説明する。

### F96-1.5 — domain 復帰 3 段は PASS、CV-10 の具体形を修正

\(n=5\) を現 domain から除外し、非接触を維持した点は正しい。全奇数へ戻す手順も次の三段でよい。

1. seal release の司令塔認可。
2. 旧追補を上書きせず、新しい versioned addendum で domain を復帰。
3. 総組立・CLAIMS・引用元を新しい effective source へ更新。

ただし監査点 D の `role:"supersedes"` は、**新 artifact が旧 artifact を supersede する**という向きで記録する。`path` を旧追補にしてはいけない。概念形は次である。

```json
{
  "effective_source_chain": [
    {"role":"original", "path":"docs/notes/fam_u_v1.md", "sha256":"..."},
    {"role":"erratum", "path":"docs/notes/fam_u_v1_addendum_f94.md", "sha256":"OLD"},
    {
      "role":"supersedes",
      "path":"docs/notes/fam_u_v1_addendum_<new>.md",
      "sha256":"NEW",
      "supersedes":{"path":"docs/notes/fam_u_v1_addendum_f94.md", "sha256":"OLD"}
    }
  ],
  "effective_source": {
    "path":"docs/notes/fam_u_v1_addendum_<new>.md",
    "sha256":"NEW",
    "section":"domain declaration"
  }
}
```

### P96-1.1 — FAM-U-ASM v2 の必須修文

versioned v2 では次を一束にすること。

1. §3 を「模型局所計算」「窓 torsor の意味づけ」「Ihara 外枠」に分割する。
2. GR・U2-BR・Ihara bridge を左端の最小依存から外す。
3. M4/D-3d を \(\gamma\) consistency branch として別図へ移す。
4. §4 から「\(n\) 一般の機械確認なし」「Lean 未着工」を数学的 candidate 理由として削る。ただし現格の注記としては保持可。
5. §7 の一本矢印を、(a) 裸の class/order、(b) B-5 による torsor 解釈、(c) Ihara 輸送へ分ける。2-part の B-LIMIT-0a と \(n\)-part の条件性も別矢印にする。
6. §5.3 の CV-10 supersede 記録を F96-1.5 の向きに直す。

これを満たせば文書全体を PASS に上げられる。**主言明自体は今便で採択済み**であり、SURJ や \(\operatorname{ord}(a_n)=n\) は引き続き主張しない。

### F96-1.6 — B-LIMIT 追記 5 は「依存監査」として PASS

`B-LIMIT-2′` を「現在列挙された経路 B の入力 \(\mathcal P\) の依存監査」へ下げたことを承認する。ここでの \(\mathcal P\) は §2′.4 の五入力を指す、でよい。

ただし `unconditional` という語は絶対無条件ではない。B-LIMIT-0/0a は **BFC/B-4c/B-5/TB の橋に相対的だが FAITH-free**、B-LIMIT-1 はさらに FAITH 条件付き、と書くのが正確である。

「二つの反対モデル」は論理的非導出を示すには十分であり、すべての部分群 \(H\) を実現する必要はない。しかし有限群 \(\mathfrak F_0\) の部分群を形式的に選ぶだけでは、その \(H\) が算術 Galois image として実現するモデルを与えたことにならない。現時点でその算術入力はないので `UNKNOWN BL-2` は適切である。今回の FAM-U 算術結論を「経路 B の独立入力」として戻すのは結論の再投入であり循環なので不可。

`b_limit.NOT_claimed` は過大読解防止に有用だが、全 cert に固定の巨大欄を強制するより、必要時だけ `scope_exclusions[]` の構造化欄で表すのがよい。

### F96-1.7 — C-β cert の effective-source 追記は PASS

追記 5 §5.4 が `u7_cbeta_final_20260801.json` を original として保存しつつ、追記 4 §4.2.6.9 と追記 5 §5.4 を erratum/effective source に置いた向きは正しい。`c_beta_ind_dummy_h_selfcheck` だけを失効させ、恒等交差表等の主結果を失効させていない切り分けも妥当である。cert 単体で引用を止めず、この effective-source chain を併記すること。

---

## 2. EP 修理バンドルの現況裁定

### F96-2.1 — `[27]` の局所述語は PASS

両 lane の述語は次の正形になっている。

- E-1--E-4 が先に PASS。
- attested E-5 が存在し、その明示値が Prop E5-D の導出値と矛盾した時だけ `[27]`。
- attestation 欠落時は導出値が権威であり、`[27]` は発火しない。

発火縁・非発火縁の二 fixture はこの境界を固定しており妥当である。`[27]` を REJECT でなく INTEGRITY_STOP に置くこと、priority を 19/19 の末尾に置くことも妥当。S2 を「native 値そのもの」に限定せず「入力から定理的に強制される恒等式の破れ」と定義するなら、新軸を増やさず S2 に置いてよい。P-S3 を変更しない判断も、次の排他性矛盾を直した後なら維持できる。

### W96-2.1 — spec v19/contract v14 は S2 の排他性について自己矛盾する

spec v19 §5.3.2 の検証例は `[24]+[27]` の同時検出を明示し、primary=[24]、[27] は sealed とする。一方、§5.3.3 と contract v14 X-1 は **S2 軸内は排他で、[27] と他の S2 code は同時に立たない**と規定する。両方は同時に実装できない。

私は **S2 の異なる述語は累積可能**とする方を推奨する。[24] の finite partition 不一致と [27] の attestation 矛盾は別原因であり、state machine はすでに `all_reason_codes[]` と priority を持つため、両方を保持する方が証跡を失わない。重複原因だけを禁止したいなら、S2 全体の排他ではなく、同値原因の組を明示するべきである。この選択に合わせ、spec の擬似コード、X-1、両 lane の early-return/集合蓄積を一斉に同期すること。

### W96-2.2 — receipt の docs-era pin は payload-era を束縛していない

`gen-receipt/v2` が v19/v14/v14 の三文書 digest を pin し、受領側が再計算する修理自体は PASS。しかし現在の generation と full witness の中身を追うと、次が残る。

- `ninfty-verifier-b.py` は governing spec v18 / contract v13 / manifest v13 を宣言する。
- `ninfty-searcher-v2.mjs` は `native_schema_id = mb/ninfty-stage2-predicate/v18#cert-schema` を生成する。
- full witness certificate の `predicate_spec_id` と `schema_id` も v18。
- 現 generation の lane-A native artifact も v18 の `native_schema_id` を持ち、`native_schema_digest` は null。
- contract v14 P-3.1/P-3.2 は certificate の predicate/schema ID と digest が governing v19 に一致することを要求する。

一方 `docs_era_binding_ok` が見ているのは receipt の三文書 hash と手元文書の一致だけで、埋込 certificate/native の version ID は見ない。従って現在 PASS しているのは **control-plane receipt の文書 pin**であり、「payload が v19 schema に属する」という意味の docs-era binding ではない。

修理は二択である。

1. certificate/native と verifier を v19/v14/v14 へ再生成・再束縛する。
2. R1/R2 は v18/v13/v13 の歴史 route、R3-NF と provisioning control plane は v19/v14/v14、という **mixed-era compatibility matrix** を versioned に宣言し、consumer が route ごとの許容組を exact に検査する。この場合 `docs_era_binding_ok` は `control_plane_docs_receipt_binding_ok` 等へ改名し、payload-era PASS と混同させない。

歴史 R1/R2 を byte-frozen に保つ方針と整合するのは 2 だが、明示 matrix なしの現在形は freeze-ready ではない。

### F96-2.2 — CI は「限定された assertion の fail-closed」として PASS

run 30688121934 の保存 receipt、run SHA `01f53cf...` の workflow、現 workflow を照合した。suite step は `PIPESTATUS` を回収し、最終 gate は `suites_status=0` を強制する。registry smoke の heredoc 後も assert の exit code を echo で上書きせず保存する。従って便 95 で問題にした「suite failure を job success にする」穴は閉じた。

ただし full-union step が assert するのは、四 role、docs receipt hash、R3-NF PASS、R1/R2 の正直な欄など、明記された限定条件である。full CLI の exit 1 と overall `INTEGRITY_STOP` は意図どおり保存され、workflow は **union PASS を要求していない**。従って

- **P95-2.2 item 2 は closed。**
- CI success は W-6 closure、R1/R2 PASS、EP 発効を意味しない。

外部 GitHub API から run を再取得したわけではないため、ここでの裁定は repo 内 receipt と commit-local workflow の整合に対するものである。

加えて現 HEAD で `python search/ninfty-evidence-union-full.py search/certs/ep_ci_full_witness_evidence_20260801.json` を再実行し、exit 1、R1=MALFORMED、R2=MALFORMED、R3-NF=PASS（11/11）、overall=INTEGRITY_STOP を再現した。

### W96-2.3 — W6-SEM: 選択肢 (c) は現意味論を保存しない

contract v14 §3.2 の W-6 は

\[
(\pi_*\operatorname{Ram}_C)(b)
=\sum_{r:\,\pi(r)=b}m_r
=m_{\operatorname{Branch}}(b)
\]

を **全 branch point \(b\)** で再計算する条項である。frozen R1/R2 はこれを、両 lane の registry-pinned native から抽出した canonical `{branch_value,multiplicity}` map の照合として実装している。従って W-6 を「同一 lane の歴史 route」と言い換えることは、現条文と source の双方に反する。

R3-NF PASS も W-6 を含意しない。R3-NF が保存・検査するのは NF shape、各 producer と自己 digest、cross-lane NF digest、N-1--N-5、total degree、infinity、non-ramification である。**ramification component がどの branch component へ写るかという incidence/pushforward map は NF にない。**

★最小反例の型: ramification component \(r_1,r_2\) の係数を \(1,2\)、branch component \(b_1,b_2\) の係数も \(1,2\) とする。\(r_1\mapsto b_1,\ r_2\mapsto b_2\) は W-6 を満たすが、写像だけを交換した \(r_1\mapsto b_2,\ r_2\mapsto b_1\) は満たさない。ところが incidence を忘れた component multiset、total degree、infinity、non-ramification は同じである。従ってその忘却像だけを見る R3-NF では両者を分離できない。

よって三択の裁定は次である。

- **(a) 採用。** lane A producer が、自身の ideal/locus data から導いた registry-pinned canonical pushforward map を現 W-6 shape で出す。受領側は pointer、map digest、multiplicity 和を再計算する。
- **(b) 現状のままでは不採用。** lane B に locus map を足すだけでは frozen W-6 と同じ述語にならない。新しい共通 schema と route ID を定義するなら将来案になり得る。
- **(c) 不採用。** R1/R2 を歴史的 MALFORMED のまま保存する説明としてはよいが、それを W-6 closure と数えたり R3-NF で置換したりしてはならない。

別案として NF に incidence/pushforward map を追加した `R3-NF-v2` を新 route として設計することはできる。しかし現 R3-NF の意味を上書きせず、NF-v2 から W-6 を導く補題と負例を新規に要する。

### P96-2.1 — W-6 の最小修理仕様

選択肢 (a) を次の境界で委嘱する。

1. lane A native artifact に、各 ramification component の canonical ID、image branch key、multiplicity、導出元 ideal/locus pointer を持つ pushforward record を追加する。
2. `{branch_value,multiplicity}` aggregate は producer の自己申告を信じず、receiver が上の record から再集計する。
3. inline-only ref は引き続き `LEGACY_UNVERIFIED_REF`。registry-pinned artifact 内 pointer と whole-artifact digest を必須にする。
4. 異なる incidence で同じ NF を作る負例を追加し、R3-NF PASS だけでは W-6 が PASS しないことを固定する。
5. 修理後も R1/R2 と R3-NF は別列・別 route のままにする。

### W96-2.4 — DRAFT 三文書に残る二つの版記述 drift

1. manifest v14 冒頭は「純同期版・内容無改定・変更 1 点のみ」と書くが、§0.-0.5 は Y-3a という実質条項を新設し、明文で「本版は純同期版ではない」とする。後者が事実なので冒頭履歴を訂正する。
2. live source の一部コメントは依然 v18/v13、`REJECT[6]`、あるいは「E5 は再計算不能」という旧説明を持つ一方、実行行は `[27]` と E5 導出へ進んでいる。コメントだけなら数学述語は倒れないが、source-map と schema-era の監査面では stale である。W96-2.2 の世代裁定と同時に整理する。

### F96-2.3 — P95-2.2 五条件の現況

| item | 判定 | 理由 |
|---|---|---|
| **1. 新 exact freeze bundle と receipt** | **partial / 未閉鎖** | receipt v2 の docs hash pin は閉じたが、三文書の自己矛盾と v18 payload-era が残る |
| **2. CI fail-closed** | **closed** | F96-2.2 の限定された意味で実証済み |
| **3. full witness union** | **open** | R1/R2 MALFORMED、W-6 未閉鎖。R3-NF PASS は代用でない |
| **4. full-path positive control** | **open** | 不在。`uncalibrated/UNKNOWN` 維持 |
| **5. quarantine / four-role invariant** | **closed** | 現 generation で維持・機械 assert あり |

従って **EP freeze ID・再発効・minted detector の許可は出さない。** 裁定 345 による「union 実 PASS」失効訂正も現報告に反映されている。

### P96-2.2 — EP-Q1: bounded decision-lane 哨戒は telemetry-only なら許可

positive control が開いたままでも、**bounded decision-lane concordance sentinel** は次の条件で許可する。これは裁定 345 で受領した bounded 744 concordance と同じ格であり、EP 発効ではない。

1. 有限宇宙、bound、列挙順、入力 digest、二 lane の code digest を事前登録する。
2. 表示は常に `diagnostic / uncalibrated / UNKNOWN / complete_search=false`。有限宇宙を尽くした時だけ、その有限宇宙についての `complete_search=true` を別欄に置き、数学宇宙全体へ外挿しない。
3. lane ごとの verdict/reason vector を保存し、不一致は即 INTEGRITY_STOP。多数決・片側採用は禁止。
4. ACCEPT は `hold-for-review` に留め、mint、候補採択・棄却、SURJ/N∞ 主張、sealed 値への接触へ使わない。
5. NF/W-6/positive-control の代用品とは数えず、EP の P95 item 3/4 を閉じない。
6. public 面では件数・状態だけを出し、blind/sealed payload を漏らさない。

full-path の感度、特に false negative を測った「calibrated detector」と呼ぶには、盲検注入 positive control がなお必須である。「自然な positive が存在しない」という不在論証が将来得られても、それは detector sensitivity の較正を代替しない。別 campaign の \(n=3,\ u=-4\) は N∞ の full-path positive control ではない。

### F96-2.4 — 修理 bundle の機械報告は限定つきで受領

selfaudit v9 の additive 検査、両縁 negative fixture、R3-NF の 11 check、7 suite 705 check、旧 frozen 7 ファイルの byte identity、同世代 four-role resolution は、提出 cert の記録範囲で相互整合している。registry generation `ep-genuine-20260801b` と `gen-receipt/v2` の provisioning も **registry control-plane の成果**として受領する。

ただしこの受領は、W96-2.1--2.3 の意味論・世代・W-6 blocker を上書きしない。特に「705 green」は列挙された regression predicates が green という意味であり、full union、W-6、calibration の PASS ではない。

### F96-2.5 — 係交代事故の記録

事故申告と、旧 062303Z 世代を未参照 quarantine/orphan として残し、CURRENT を一世代だけへ向けた処置を受領する。係交代三段 protocol は provenance 修理として妥当。この事故自体を数学的 PASS の根拠にも FAIL の追加根拠にも数えない。

---

## 3. 制度・その他

### F96-3.1 — δ 表と CV-12 初履行は PASS

定義

\[
6\delta(n)=3(n\bmod4)+4(n\bmod3)
\]

から独立 checker を再実行し、

```text
[0, 7, 14, 9, 4, 11, 6, 13, 8, 3, 10, 17]
```

が \(n\bmod12=0,1,\ldots,11\) の 12/12 で文書表と一致、exit 0 を得た。§2.3 の \(n=30\) 文修正もこの定義と整合する。generator と checker は式から別に再導出しており、故意破壊の非零終了、回帰 battery 第 7 suite への組込みも CV-12 の目的に合う。

`delta_table_20260801.json` は script digest と definition digest を内包し、output artifact 自身の digest は便 96 の外部 envelope が束縛している。自己ファイル内へ自己 SHA-256 を埋め込むことは固定点問題になるので、CV-12 の「output digest」は task/receipt/manifest の外側束縛でよい。

### W96-3.1 — 規約台帳の v1.2 内容は採るが、版 metadata が v1.1 のまま

CV-12 の三点束と `n/a` の型注意を正位置に置いた内容は PASS。しかし artifact は次を同時に持つ。

- 表題: `規約台帳 v1.1`。
- 改訂記録・未閉鎖項: v1.1。
- schema token: `ledger_version = conventions_ledger_v1_1`。
- 本文 §§1.4/2: v1.2 で施行、と宣言。

従って現 blob を「規約台帳 v1.2」として発行するには metadata drift を直す必要がある。歴史 v1.1 記録は `[historical]` として残し、live header と `ledger_version` を v1.2 にすること。

また「非該当は bare string `"n/a"`」と、object/array の型破壊を避ける注意は、schema を union にすれば両立するが、現在は二案が未決である。私は全体を

```json
{"status":"n/a", "reason":"..."}
```

の typed sentinel に統一することを推奨する。少なくとも object/array 欄ごとに union を明記するまでは、一律 bare string を機械規範にしてはならない。よって **規約台帳は条件付き PASS**。

### P96-3.1 — 規約台帳 v1.2 の発行条件

1. live title、revision block、`ledger_version`、§5 の版記述を v1.2 に同期。
2. `n/a` を typed sentinel か明示 union のどちらか一つに確定。
3. CV-12 の output digest は外部 receipt/manifest が担うことを条文化。

### F96-3.2 — Lean 方針 v1.6 は方針文として PASS

P95-4.1 の六ゲートは正しく編入されている。特に exact 原典/頁/PDF 画像、Mathlib commit、全 axiom set、`sorryAx` 拒否、定理ごとの exact sorted set、型 digest、M2-DESC の直接降下優先が揃う。v1.5 を便 95 の v1.4 exact blob へ遡及混入しない注記も正しい。

これは **Lean 実装の着工条件を承認する裁定**であり、M2/FAM-U が Lean で verified になったという裁定ではない。

### F96-3.3 — PARI 通常 run は \(h=1\) の機械計算として受領

receipt は PARI/GP 2.15.4、`polcyclo(28)`、`h_grh=1`、`bnfcertify_result=1`、exit 0 を記録し、二つの既知較正値も一致する。従って **この run は GRH 条件を外した \(h(\mathbf Q(\zeta_{28}))=1\) の PARI 計算 receipt**として採用する。Lean による verified とは呼ばない。ローカル環境に GP がないため、私は今回再実行していない。

ただし当該 JSON 自身は

```text
negative_control=false
negative_control_marker_in_log=false
```

であり、別の陰性対照 run ID/digest を束縛していない。従って「通常 run の fail-open 修理と \(h=1\)」は受領するが、「陰性対照 failure がこの archivable artifact に同梱・束縛された」は主張できない。陰性対照を保存証跡に数えるなら、別 receipt に `negative_control=true`、期待した不一致、非零終了、workflow/run SHA、log digest を記録し、通常 receipt からその digest を参照すること。

小型 NOTE: 現 receipt の `unconditional` と `gp_exit_code` は JSON boolean/integer でなく文字列である。今回の値の読解は一意だが、schema v2 ではそれぞれ boolean と integer に固定するのがよい。

### F96-3.4 — 便 95 以前の union 表現訂正

裁定 326 の「union 実 PASS」は裁定 345 で失効しており、今回の R1=MALFORMED、R2=MALFORMED、R3-NF=PASS、overall=INTEGRITY_STOP という申告はその訂正と整合する。過去裁定を再編集せず、345 と本返信を effective record とする。

---

## 最終要約

- **M2 三部作は theorem（紙・\(n\) 一様）として維持。D7-3 は不存在。**
- **FAM-U-ASM の P95-1.1 主言明は採択。** ただし依存表は過剰であり、M4/SPLIT/GR/機械全確認を最短 class/order 鎖から外す v2 が必要。
- **W-6 は option (a)。** 現 R3-NF は incidence を忘れるため代替不能。
- **bounded decision-lane 哨戒は telemetry-only で許可。** EP はなお `uncalibrated/UNKNOWN`、発効なし。
- **EP v19/v14/v14 DRAFT は freeze 差戻し。** S2 自己矛盾、payload-era 混在、W-6、positive control を閉じて再請求すること。
