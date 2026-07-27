# 総合判定: **凍結 1 は PASS・S5 Model-Builder を解禁可。Lean 対応表は条件付き PASS**

二つの判定軸を分ける。

- **Freeze 1**: commit `578b4fe` で便 41 の残 2 束と文書 finality は閉じた。Rule 1 v1.3 を受理し、**個別モデル探索を Model-Builder の役割範囲に限って解禁してよい**。
- **Lean 設計**: F33–F36 の分割方針は紙面と整合する。F37 と表 D には、実装前または実装途中で直すべき statement/scope がある。下記の確定リストを反映し、各「全行」の statement が通るまでは、その全行へ `verified` 札を付けてはならない。これは Freeze 1 の受理を妨げるものではない。

本便でも個別モデル探索コマンドは実行していない。

---

## F1. 便 41 残 2 束の差分検収

### F1.1 harness false-green — PASS

再走結果は次のとおり。

```text
node crosscheck/check-r5-r8-ninf-fail-closed.mjs
=== 42/42 PASS ===

node crosscheck/check-r7-bundle-attack.mjs
=== 5/5 PASS ===

node crosscheck/check-qparse-fail-closed.mjs
=== 30/30 PASS ===

node crosscheck/check-cli-fail-closed.mjs
=== 12/12 PASS ===

powershell.exe -NoProfile -ExecutionPolicy Bypass \
  -File crosscheck/check-cli-fail-closed.ps1
=== 12/12 PASS ===

node crosscheck/check-kummer-rational-parser-fail-closed.mjs
=== 11/11 PASS ===
```

管理下セッションでは Node 内の子 process 起動が `EPERM` になったため、Node CLI harness の 12 件と Kummer parser harness の 11 件は、明記された `in-process fallback` で判定された。これは OS process の実走を PASS に偽装しておらず、CLI 固有の残差は `ENV_LIMIT` として PASS 数の外へ出ている。さらに PowerShell 版を外側 process として再走し、実 CLI の 12/12・exit 0 を得た。

ソース上も次を確認した。

1. Node CLI は期待件数 `12`、Kummer parser は `11`、PowerShell は `12` を定数として持ち、実行数との**厳密一致**を末尾で assert する。
2. 0 件・不足・過剰、または fallback 自体の失敗は structured `ENV_FAIL` と非零 exit になる。旧 `0/0 PASS, exit 0` 経路はない。
3. `runCliCore(argv)` は判定本体を共有するが、副作用の薄い OS wrapper まで測ったとは主張しない。その穴を PowerShell 版の実 process 較正が埋める。
4. PowerShell 版は問題のあった `Start-Process` を廃し、呼び出し演算子による直接起動と `try/catch`、`$LASTEXITCODE` の採取へ移った。

従って、便 41 F4.2/F4.3 の発射 blocker は閉じた。

### F1.2 blob coverage/finality — PASS

この環境では Node からの `git hash-object` 起動が `EPERM` となり、
`node crosscheck/check-blob-hashes.mjs` は非零停止した。これは false green
ではない。外側 PowerShell から同じ表を独立に読み、`git hash-object` を直接
適用して次を得た。

```text
ACTIVE markers       = 1, 1
EXCLUDED markers     = 1, 1
active rows          = 37 (unique 37)
excluded rows        = 76 (unique 76)
coverage targets     = 109
uncovered            = 0
active ∩ excluded    = 0
duplicate rows       = 0
stale scoped entries = 0
blob mismatches      = 0
```

coverage 109 件の内訳は、coverage scope 内の active 33 件と理由付き除外
76 件である。active 表にはさらに coverage scope 外の凍結文書・証明書 4 件が
あり、合計 37 件となる。除外理由の空欄もない。

照合器は、(i) 四 marker の各一意性、(ii) active 内・excluded 内・両表間の
path 重複禁止、(iii) top-level の
`crosscheck/*.mjs`, `crosscheck/*.ps1`, `search/*.g`, `search/*.mjs`
の実列挙、(iv) 未登録・消滅済み登録の拒否、(v) 自身の active 表への登録を
実装している。従って、便 41 で挙げた coverage 対象行の削除・行複製・
第二表追加の三経路はいずれも非零停止へ入る。coverage 外の active 4 行も、
それを含む実装版表の最終 SHA-256 によって封印される。

### F1.3 文書 finality — PASS

`docs/week4-K5_Rule1_impl_versions.md` の旧 `38/38`・`9/9` は発生時点を
明記した履歴へ降格され、現行 `42/42`・`11/11` が直後の更新注と active 表に
記録された。旧 `Q.parse` 懸念も「便 40 時点の観測」と明示され、現行
`30/30` と「解消済み」が同じ箇所に置かれた。現在状態と履歴値の衝突はない。

五つの最終 SHA-256 は全一致した。

| artifact | SHA-256 |
|---|---|
| `docs/week4-K5_Rule1_v1.md` | `8367ba7ac57876b490bbe775c56768747a519f3f5e4c1fe69dfab0c022cdf8db` |
| `docs/manifest_k5_appendixA_v1.md` | `903bb9f31b27f61f2af0f4f2aeb9e4cf5c7e71e7db011bad447297495da90b75` |
| `docs/manifest_k5_v1.md` | `2091dea7db6fca3cdc99fa5b688805b51a12cd86819d7b4f76df069d02a47b13` |
| `docs/week4-K5_Rule1_impl_versions.md` | `6a65086e1c6d28424a572942176c8e697e430e0eff151d0c7c0db1ac3f799de9` |
| `docs/week4-K5_S5設計_opus_v1.md` | `b5a14db3cd18412021fe64398a483e7dfeb4bbe7835ef499ca21108667a20555` |

---

## F2. Freeze 1 最終裁定

便 41 で確定した三条件、

1. CLI harness の 0/0 false green 閉鎖、
2. blob の全 path・単一表・checker 自己拘束、
3. `Q.parse`/件数/CLI 結果の文書整合、

はすべて閉じた。よって **Freeze 1 を受理し、S5 Model-Builder を解禁する**。

この解禁は Model-Builder の個別モデル探索までである。Extractor、`u` の
開示、Kummer 判定、二 dessin の片翼先行抽出は解禁しない。それらは
**両翼 atomic Freeze 2 + digest に束縛された一回性の発射錠**を待つ。

---

## F3. Model-Builder 委嘱文へ入れる最終注意

1. **正本の固定**: 上記五 SHA-256 と commit `578b4fe` に対応する
   manifest/Rule 1/S5 設計だけを読む。途中で規則を変更して候補を救済しない。
2. **役割 whitelist**: 出力を、明示曲線、Belyi map の完全な式、分岐 divisor、
   cusp、uniformizer、passport、exact monodromy triple、標的 triple への exact
   conjugator に限る。数値近似・database label は discovery 用であり証拠ではない。
3. **封印値へ触れない**: `u`、`λ/t^10` の非零定数項、leading coefficient、
   valuation/class、平方類などの同値量を計算・表示・候補選択に使わない。
   `λ/t^10` の定数項を 1 に正規化してはならない。
4. **`λ=cμ²` 漏洩を封じる**: `λ` は完全な一式として出してよいが、Freeze 2 前に
   `(c,μ)` の対へ分離して報告しない。`c` の値・平方類・平方因子・符号を
   計算・表示・選別に使わない。
5. **(N∞) の追加漏洩を封じる**: `ĉ_μ=a²-f₆p²` の値・平方類・平方因子・符号も
   同様に禁止する。μ/Pell ansatz は strict I-b∞ を守る sealed automation schema
   を先に登録しない限り、人間可視の探索に使わない。
6. **三枝を混同しない**: M0 の枝ラベルは
   `W / N_aff / N_infty` の三値だけで、未知値を既定枝へ丸めない。
   現在の既設探索器で `W/N_aff` だけを走らせる場合は
   **positive-only・非網羅**と明記し、`N_infty` は未探索、
   campaign 全体は `BRIDGE-UNKNOWN` のままにする。
   `N_infty` について「候補なし」と報告してはならない。
7. **二 dessin を独立に扱う**: sq/ns に同一曲線・同一 ansatz を強制しない。
   一方の値や候補順位を他方の選択へ流用しない。
8. **全順序と停止規則**: Rule 1 の canonicalization、全順序、tie-break を
   そのまま使う。一意候補が得られなければ `UNKNOWN`。係数・符号・座標を
   後から調整して一意化しない。
9. **記録と隔離**: 入出力 schema、全 transcript、役割別 access log、
   canonical serialization、digest、時刻、commit を保存する。禁止量が露出した
   run は quarantine し、後から hash を付けて救済しない。
10. **Freeze 2 は両翼同時**: sq/ns のモデル・actual marking・uniformizer を
    一つの atomic bundle にする。一翼しか得られなければ保存だけ行い、
    Extractor を起動しない。将来の両 driver は digest だけでなく、
    **同じ canonical bundle から係数を直接読む**。
11. **比較段との境界**: `b_sq,b_ns`、`a_eff`、(5′)、Kummer 位数、算術全射性を
    Model-Builder の候補選択に使わない。これらは Freeze 2/Bridge/Extractor 側の
    後段記録である。
12. **即時停止**: schema mismatch、digest mismatch、禁止量の露出、枝の
    fallback、片翼先行、exact 証明書の欠落があれば Rule 1 の分類どおり
    integrity stop または `BRIDGE-UNKNOWN` とし、平均・符号合わせ・再正規化を
    行わない。

---

## F4. Lean 設計監査 — F33–F37

### F4.1 共通の型

分解の数学は紙面 §5.2.2/§5.2.4′ と一致する。ただし Lean では紙面の
`Ih|_{Γ_K}` や `Γ_K∩ker κ` をそのまま書くと型が合わない。先に次を一度だけ
構成すべきである。

- `F0 : Subgroup T`、`χT : T →* Q`、`F0 = ker χT`。
  `χT` の全射性と、紙面 (1) に対応する `χT.comp Ih` の全射性。
- 紙面 (2) の `F0 ≃ C_e`。群論段を安全に一般化して巡回性を使わないなら、
  少なくとも `Nat.card F0=e` を明示し、その一般化を docstring に記録する。
- `Ih : Γ →* T`、
  `ΓK := (χT.comp Ih).ker : Subgroup Γ`。
- exactness から値域を `F0` に絞った
  `IhK : ΓK →* F0`。包含との合成が `Ih.comp ΓK.subtype` に等しいこと。
- `κ : ΓK →* μM` と、その像が `μM[e]` に入ることを**導出した後**の
  corestriction `κe : ΓK →* μMe`。
- `ρ0 : F0 →* Equiv.Perm Λ` と
  `τe : μMe →* Equiv.Perm Λ`。

`μMe` は「位数 e の部分群」という文章だけで済ませず、
`Nat.card μMe=e`、`e>0`、必要なら `e∣M` を型または仮説に持たせる。

### F4.2 各行

**F33 — 条件付き PASS。**

群論段の正しい結論は

```text
Function.Surjective Ih ↔ Nat.card (MonoidHom.range κ) = e
```

で、紙面の段 1–4 と一致する。比較式は ill-typed な
`ρ0 ∘ Ih|ΓK = τ ∘ κ` ではなく

```text
ρ0.comp IhK = τ.comp κ
```

（右辺は必要なら `τ` の全 `μM` 版）とする。`ρ0`、`τ` の単射性と
`range ρ0 = range τe` も明示する。

ただし F33 が与えるのは **`|im κ|=e` という群論判定**までである。
紙面の `ord([u⁻¹]_M)=e` へ移すには
`|im κ_v|=ord([v]_M)` という Kummer 入力が別に要る。F33 単独を
`R6-full` 全体の `verified` 札にしてはならない。

**F34 — 条件付き PASS。**

全射性に依存しない分離は正しい。ただし「全射性なし」とは
`Ih` 自身の全射性を仮定しないという意味である。型付き結論は例えば

```text
Ih.ker = κ.ker.map ΓK.subtype
```

である。`κ.ker` は `ΓK` の部分群なので、紙面の
`ΓK ∩ ker κ` を Lean で無理に同じ ambient group の交わりとして書かない。

また、これは **固定体公式そのものではなく、その群論的 kernel identity** で
ある。`= G_{K(v^(1/M))}` への翻訳は M6‴。従って F34 が通っただけで
紙面 (7.4) 全体へ `verified` 札を付けない。この切り分け自体には同意する。

**F35 — PASS（statement の一意性 predicate が必須）。**

正準性は `τ,ρ0` を固定した上での正準性であり、紙面と一致する。最終形は
単に「ある `j` を定義」ではなく、

```text
∃! j : μMe ≃* F0,
  ρ0.comp j.toMonoidHom = τe
```

のように、可換条件を一意性 predicate に入れる。外から `j` を仮説として
渡して存在だけを示す形は、正準性を空にするので不可。

**F36 — 条件付き PASS。**

`IhK = j ∘ κe` は紙面 (1.2) と一致し、coprime 条件は不要である。
ただし `im κ⊂μM[e]` を新しい無根拠な仮説として追加してはいけない。
F33 と同じ (5′)/(6′)、`τ` の単射性、像一致から導く補題を import するか、
F36 内で導く。そうして初めて paper corollary と 1:1 になる。

**F37 — 現行の一行は三分割が必要。**

設計表の一行は次の三内容を含む。

1. **F37a**: `ZMod e` 上の `x ↦ r*x` が全単射
   `↔ Nat.Coprime r e`。
2. **F37b**: 共通の代数閉包内で
   `q_e : μ_M[e] →* μ_e`, `z ↦ z^r` を実際に構成し、
   `e∣M`, `r=M/e`, `e>0` の下で
   `Function.Bijective q_e ↔ Nat.Coprime r e`、従って
   `MulEquiv` を得る。
3. **F37c**: coprime 時に
   `ι := q_e.symm.trans j`（すなわち `j ∘ q_e⁻¹`）を定義し、
   `q ∘ κ = q_e ∘ κe` を介して (7.5) を証明する。

便 42 同梱時点の `LeanArith/F37.lean` が示した `ZMod` の全単射同値は
**F37a のみ**である。数学的な核として正しいが、抽象巡回群との同型を
コメントで述べるだけでは F37b の typed instantiation にならず、
`ι` と (7.5) も含まない。従ってその定理が Lean を通っても札は
「F37a verified」までであり、「F37 verified」ではない。

さらに `ZMod 0` は有限位数 0 の巡回群ではなく整数なので、「有限巡回群」
という docstring を使うなら `0<e`/`NeZero e` を置く。一般の `e=0` まで
成り立つ算術定理として残す場合でも、roots-of-unity への instantiate 側では
`e>0` が必要である。

**総括**: F33/F34 の分割、F35 の正準 `j`、F36 の q-free 正規形、
F37 の coprime 時だけの (7.5) という紙面の段割りには同意する。
修理点は数学の変更ではなく、ambient subtype と「核だけを全行と呼ばない」
ための射程管理である。`B_FC` はこの形式化から一切閉じず、引き続き
`candidate / UNKNOWN` である。

---

## F5. Lean 設計監査 — 表 D

| 行 | 判定 | 監査結果・確定修理 |
|---|---|---|
| **M1** | **PASS** | `x^p=(a:K) ⇒ ∃n:ℤ, n^p=a^[K:ℚ]` は補題 NC と 1:1。`p` が素数でなく自然数でも真なので安全な強化。cast を明示し、`p=0` を処理すれば空虚性はない。 |
| **M2** | **PASS** | `finrank ℚ (CyclotomicField 12 ℚ)=4` は紙面の次数主張そのもの。後続の field equality に使う際は、抽象 cyclotomic field と共通代数閉包内の `K=ℚ(ζ₁₂)` の embedding を別途接続する。 |
| **M3** | **PASS** | `¬∃x:K, x^3=-4` は NC-1 と一致する。`K` が M2 の `ℚ(ζ₁₂)` であることを statement/namespace で固定する。 |
| **M4** | **PASS** | `(∃z,z^6=-64) ∧ ¬∃z,z^6=-4` は `[−4]_6^3=1` かつ `[−4]_6≠1`、従って位数 3、と正確に同値。δ2 の説明を docstring に残す。 |
| **M5** | **条件付き PASS** | 次数 12 は正しい。ただし裸の記号 `L₃` では任意の体を差し込める。`L₃` を `K` に 2 の三乗根を adjoin した具体的な体、またはその同型として定義してから `finrank` を述べる。三次多項式は「根なし ⇒ 既約」で足り、Kummer API に過剰依存する必要はない。 |
| **M6** | **statement 修理必須** | 数学は正しいが `2^(1/3)` は Lean の正準元ではない。共通代数閉包 `Ω`、`α β:Ω`、`α^6=-1/4`、`β^3=2` を量化し、`adjoin K {α}=adjoin K {β}` と書く。任意の `β` で同じ体になる代金は `μ₃⊂K`。具体定数を含むので札は基本的に `α`。一般補題へ分ける場合だけ `β` とする。 |
| **M7** | **statement 修理必須・延期可** | 数学的看板は正しいが、`ZMod 2` はそのままでは `≃*` の乗法群 `C₂` ではない。右辺は例えば `(Equiv.Perm (Fin 3)) × Multiplicative (ZMod 2)` とする。`L₃` の具体定義も M5 と共有する。M5+F28 は M7 の代用品ではなく、M7 未実装の間は Galois 群同型を Lean `verified` と表示しない。 |
| **M8** | **条件付き PASS** | 提案命題は N5 の条件付き Vieta 補題と一致し、`t=X^6v`, `v(0)=4` は `t` の主係数 4 を与える。ただし statement 単独は branch `t` の存在、`λ=-t`、局所変数の同定を証明しない。札は「N5 の代数的主係数補題」までとし、幾何比較 B6 や実在する `u=-4` 全体へ広げない。 |
| **M9** | **PASS** | `¬∃x:ℚ(ζ₅),x^5=2` は NC-3 と一致する。M1 と次数 4 の instantiate。 |
| **M10** | **FAIL（式の修理が必要）** | 現行骨子 `¬∃z, z^3=2 ∧ ¬∃z, z^2=2ζ₃^j` は括弧が誤り、`j` も自由変数である。少なくとも `(¬∃z,z^3=2) ∧ (∀j:Fin 3, ¬∃z,z^2=2*ζ₃^(j:ℕ))` とする。`μ₆⊂K` を使えば第二項は `¬∃z,z^2=2` に簡約できる。非 load-bearing でも、残すならこの修理は必須。 |
| **M6′** | **FAIL（骨子が弱い）** | `finrank ... = e ほか` だけでは紙面 (7.2) の十分方向と 1:1 でない。`ord_e([v])=e`、二つの adjoin 体の等号、両次数 `e` を一つの conjunction または名前付き三補題で明示する。`M>0, e>0, e∣M, r=M/e, μ_M⊂K, ord_M([v])=e, Coprime e r` を全て型に出す。 |
| **M6″** | **FAIL（核だけへの縮小不可）** | 最終の field inequality だけでも紙面の (7.2′)・order drop を覆わない。`∃a∈K×,∃ξ∈μ_M,v=(aξ)^r`、`ord_e([v])∣e/gcd(e,r)<e`、二次数の不等式、体の不一致を分割して全て残す。着工済みの `orderOf(g^r)=M/gcd(M,r)` は有用な補助補題だが M6″ 本体ではない。また抽象版には `M>0`/有限位数を入れ、`M=0` の無限位数ケースを混ぜない。 |
| **M6‴** | **FAIL（現骨子は ill-typed）** | `(κ v).ker = ...` の右辺を何の部分群として比較するかが未定義。共通代数閉包 `Ω` を固定し、`G_K=Aut(Ω/K)` の中の fixing subgroup `Aut(Ω/K(v^(1/M)))`、または restriction map の kernel として書く。`ker κ_v = fixingSubgroup (K⟮α⟯)` の typed equalityを得て初めて F34 から (7.4) へ渡せる。API が無ければ引き続き UNKNOWN でよい。 |

M6 の紙上等号自体は簡単に確認できる。`α^6=-1/4` なら
`(-2α²)^3=2`、また `α³=±i/2∈K` なので
`α=α³/α²∈K(α²)`。従って `K(α)=K(-2α²)` であり、他の 2 の三乗根は
`μ₃⊂K` によって同じ生成体を与える。問題は真偽ではなく、非正準な
`2^(1/3)` を Lean の term として書いた点である。

---

## F6. Lean 札の付け方 — 本監査範囲の確定条件

1. `F37_zmod_mul_bijective_iff_coprime` は **F37a** としてのみ登録する。
2. `orderOf_pow` 系は **M6″-core** としてのみ登録する。
3. F33 は Kummer 位数翻訳なしに `R6-full` 全体を名乗らない。
4. F34 は M6‴なしに固定体公式 (7.4) 全体を名乗らない。
5. M8 は branch の存在・`λ=-t` の橋なしに「定理 K3 の `u=-4` 全体」を名乗らない。
6. 補助核が Lean を通ったことと、対応表の紙面一行全体が `verified` であることを別欄にする。
7. 比較橋 `B_FC` は F33–F37 の成否と独立に `candidate / UNKNOWN` のまま残す。

以上が表 D・F33–F37 の本便における**完全な修正リスト**である。
