# physical connection v11 CV-9 判読(falsifier 逐語・裁定 2048 で正本化)
著者: falsifier(opus/max・非当事者)。司令塔が scratchpad 報告書(sha256 先頭 16 桁 5ceb16adfbeb8598)を逐語転記(2026-09-04)。

**工房裁定(2048)**: CV-9 = **同一対象**(限定 3 条)。工房格 = **checker PASS(同一著者系統・実装独立の全行 replay)・cross-checked は限定つき** — (a) 固定 P1 artifact 9931437113 の 8,059 offer に対する (ell,g) ペアと lower-first 消去が与える rank 6705/従属 1354/reductions 7,665,974 に限る (b) P1 の degree-2 内容は両系統が同一バイトを消費するのみで射程外 (c) 集約写像 Agg_le2 の規約・設計の正しさは射程外(アルゴリズム形が upstream の逐行インライン化)。verified=false(Lean 未)。

---

# CV-9 仕様同一性判読 — R07 canonical P1 physical connection v11(副検問・事後)

判読者: falsifier(非当事者) / 2026-09-04
対象: GHA run 33876776771/1(success)・producer v6 × checker v7
判読範囲: 「同一対象か」の一点のみ。数学的正しさの監査・実装レビュー・追加テスト発案は行わない(裁定 316/318 スコープ制限)。

---

## 0. 裁定

**同一対象**(三値のうち)。ただし cross-checked の射程に **限定 3 条**を必ず付す。

**格付け案(一行)**:
> checker PASS(同一著者系統・実装独立の全行 replay)。**cross-checked** は限定つき —
> (a) 対象は固定 P1 artifact `9931437113` の 8,059 offer に対する `(ell,g)` ペアと lower-first 消去が与える rank 6705 / 従属 1354 / reductions 7,665,974 **に限る**、
> (b) P1 の degree-2 内容(`degree2.cache.bin`)は両系統が同一バイトを消費するのみで**射程外**、
> (c) 集約写像 `Agg_le2` の**規約・設計の正しさ**は両系統が同一アルゴリズムを再打鍵しているため**射程外**(数学監査の領分)。

---

## 1. 同一対象の根拠(すべて確認済み事実)

### 1.1 入力 pin が両側で一致

| 対象 | producer | checker | 同一性 |
|---|---|---|---|
| Task554 prepare/blocks | `v6.py:44-63`(SOURCE_RUN/HEAD/TASK554/`TASK554_CONCLUSION="failure"`) | `v7.py:48-110`(同値を再打鍵) | 完全一致 |
| P1 ancestry | `v6.py:289` `expected_ancestry` | `v7.py:1265-1289` `source_ancestry()` | 同一 literal 集合 |
| semantic checker artifact | `v6.py:65` | `v7.py:111-117` | 同一 |
| Task712 artifact | `v6.py:66-67` | `v7.py:118-124` | 同一 |
| 座標系 | `v6.py:88-91` ORDER/CHARACTERS/ACTORS/MONOMIALS | `v7.py:59-65`(list→tuple の型差のみ) | 同一 |
| 幅定数 | `v6.py:29-34` ROWS/ELL/TOP | `v7.py:31-40` 同値 | 同一 |
| launch manifest | `v6.py:234-250` `validate_launch` | `v7.py:263-309` 同一制約 | 同一ファイルを両者が読む |

workflow `.github/workflows/d972-r07-canonical-p1-physical-connection-v11.yml:335`(producer)と `:353`(checker)は、**同一の** `$RUNNER_TEMP/{p1,prepare,block-0..3,task712}` と同一 `launch.json` を渡している。checker の候補入力は producer の出力 `$RUNNER_TEMP/connection-candidate`。

### 1.2 写像の定義が同一(紙の規約と両実装が一致)

紙 `sol/proof_r07_actual_p1_physical_connection_adapter_v530.md` §1 (1.1):
`(p0,p1,p2,paux)=Agg_le2(d0,d1,d2,aux)`, `ell=concat(p0,p1,paux) in F3^32260`, `g=p2 in F3^48384`。

- producer: `v6.py:479` `p2.aggregate_precision2(...)` → `v6.py:482` `pack(concat(p0,p1,paux),ELL_WIDTH), pack(p2row,TOP_WIDTH)`
- checker: `v7.py:1176` `aggregate(self.context,d0,d1,d2,auxiliary)` → `v7.py:1194-1195` 同じ連結・同じ幅

幅の恒等式を数値検証(整数のみ): `4*2*2*1*504=8064`, `4*2*2*3*504=24192`, `8064+24192+4=32260=ELL_WIDTH`, `4*2*2*6*504=48384=TOP_WIDTH`, `24192+72576+8=96776=P1_WIDTH`, `6*2*6*504=36288`, `4*36288=145152=D2_WIDTH`。すべて一致。

紙 §2 の規約(Walsh `W[label,parity]=(-1)^<label,parity>`・PSL 左移動 `q -> q_o q`・parity XOR・`E(k)=prod_j (1+u_j)^{k_j} mod (u)^3` で指数 2 は `1+2u_j+u_j^2`)は checker `v7.py:399`(character_sign)・`v7.py:503-507`(left_map)・`v7.py:604-605`(parity XOR)・`v7.py:544-560`(e_polynomial)にそのまま現れる。

### 1.3 rank/従属の判定規則が同一

- producer `v6.py:610`: `kind = "pivot" if remainder is not None else "connection"`(`remainder = first_nonzero_unchecked(lower_acc, ELL_WIDTH)`)
- checker `v7.py:1392-1396`: `remainder = first(ell, ELL_WIDTH)` → 同一規則、`dependent += 1` も同位置

数値: `6705 + 1354 = 8059 = offers`。ORDER 差分 `[505,503,503,503]` / `[1509,1512,1512,1512]` は checker の `OLD_RANKS`/`NEW_RANKS`(`v7.py:60-61`)と一致 — 行選択が同じ行を指している。

---

## 2. 独立性の実体

### 2.1 コード共有はない(grep 実証)

checker には `load_exact` / `importlib` / `exec(` / `compile(` / `__import__` / producer の import が **一件もない**。production 経路(`v7.py:1752`)は自前の `PhysicalSourceAdapter` のみ。
producer は逆に 7 本の pinned upstream module を `exec` する(`v6.py:498-499`, `v6.py:419`)。
→ 「checker = clean-room 側、producer = upstream 経路側」という非対称構造。

AST レベルの重複を測定: producer 59 定義 / checker 86 定義のうち **AST 完全一致は 3 個のみ**(`canon`, `plain_int`, `BoundedTask712.__init__` — いずれも自明)。同名 24 個のうち 21 個は本体が異なる。**コピーではなく再打鍵**。

### 2.2 「再計算して突合」か「読み直して整合確認」か → **再計算して突合**

1. **P1 行 (d0,d1,aux)**: producer は `p1v10.LazyP1(...).row(index)`(`v6.py:479`)、checker は自前の `Task554Rows.row(index)`(`v7.py:1166`, 実装 `v7.py:966-985`)で Task554 の blob から直接再構成。**両者とも同一の `meta["p1_sha256"]` pin に一致することを要求**(`v6.py:479` / `v7.py:1169`)→ 推移的に相互一致。
2. **(ell, g) ペア**: checker は自前 `aggregate` で 8,059 行すべてを再計算し、`v7.py:1372-1374` で `record["ell_sha256"] == sha(自分の ell)` かつ `record["g_sha256"] == sha(自分の g)` を要求。**32,260 trit + 48,384 trit を全行バイト一致**で突合。受領書 `source_pair_calls=8059` が全行到達を裏づける。
3. **消去 replay**: checker は producer の `reductions` script を追うが、各段で `first(ell)` が当該 pivot の lead に**一意に一致**することを要求(`v7.py:1379-1383`)し、終端で `remainder is None or remainder[0] not in leads`(`v7.py:1392-1394`)を要求する。→ script に自由度がなく lower-first 貪欲手順に強制される。pivot 行は自分が過去に検証した行のみを使う帰納的完全 replay(`v7.py:1408-1421`)。したがって **rank/従属は producer の値の echo ではなく checker の独立算出**(`v7.py:1428-1430` で初めて manifest と突合)。
4. **Task712 (2.1) ゲート**: producer は pinned Task712 producer v3 を **exec して** oracle を作る(`v6.py:416-426`)= 表とその生成コードの自己照合。checker は `occurrence_records`(`v7.py:639-662`)で marking 生成元・OCCURRENCE_WORDS から**自前再導出**して照合(`v7.py:890-900`)。**checker 側の方が強い**。

### 2.3 独立性が及んでいない箇所(重要)

checker の `aggregate`(`v7.py:591-636`)は upstream `aggregate_precision2`(`search/d972_r07_a0_first_rung_grade2_prebuild_v1.py:918-985`)の **逐行インライン化(トランスリテレーション)** である。対応は一対一:

| upstream (prebuild_v1 / grade1_v4) | checker (v7) |
|---|---|
| `context.aggregate_table` | `OCCURRENCES` (`v7.py:128`) |
| `context.physical_shifts[tag]` | `ctx.shifts[tag]` (`v7.py:499-500`) |
| `source_degree_view` (prebuild_v1:603) | `source_view` (`v7.py:576`) |
| `source_character_sign` → `grade1.cv` (prebuild_v1:599) | `character_sign` (`v7.py:399`) |
| `grade1.sign_kernel` (grade1_v4:184) | `kernel_action` (`v7.py:403`) |
| `context.psl_left_map` (grade1_v4:339) | `left_map` (`v7.py:503`) |
| `e_polynomial` (prebuild_v1:580) | `e_polynomial` (`v7.py:544`) |
| `multiply_polynomial_rows` (prebuild_v1:567) | `multiply_rows` (`v7.py:534`) |
| `physical_lower_coord` / `physical_grade_coord` (grade1_v4:173/177) | `v7.py:624` / `:627` の inline 式 |

**独立なのは「データ」**(transport tau_o・shift h_o・PSL 列挙と index・座標式)であり、**独立でないのは「アルゴリズムの形」**(Walsh 入 → 移動 → Walsh 出 → 符号 → 加算の順序、切断規約、parity XOR 規約)。
→ upstream の `Context` の転記/データ誤りは捕捉される。**紙 §2 と両実装が共有する設計・規約の誤りは捕捉されない。**

---

## 3. 主張の射程

**「cross-checked」と呼べるもの**:
- 8,059 offer それぞれの `(ell_i, g_i)` の**値**(バイト一致・全行)
- lower-first 消去の**手順の正しさ**(各段が canonical、未消去 lead なし、pivot 重複なし)
- **rank = 6705 / 従属 = 1354 / reductions = 7,665,974 / rolling = 3cb1bcf6…**(checker の独立算出値が producer と一致)
- P1 行 (d0,d1,aux) の Task554 からの再構成が P1 artifact の per-node pin と整合
- Task712 の 4 本の `B_fwd_a*` 表が checker の自前再導出と全 36,288 列一致

**cross-checked に含まれないもの**:
- **P1 自体の正しさ**。`degree2.cache.bin`(d2)は producer(`v6.py:479` mmap)・checker(`v7.py:1170`)とも**同一バイトを読むだけで再計算していない**。degree-2 lift の内容は別キャンペーン(task757 semantic checker)の pin に依存。
- **`Agg_le2` の設計・規約の正しさ**(§2.3)。紙 v530 §2 / Prop 3.1 の数学的妥当性は Sol/数学者の領分。
- **`span(c_i) = g(ker ell)` の下流の含意**。Sol 901 も「rho2 が physical span にあるかは未決」と明記している(この点は正しい)。
- **Lean 検証**。`verified=false` は全 manifest/checkpoint/受領書に不変で載っており(`v6.py:92` FALSE_FLAGS, `v7.py:66-67`)、`A0/COMMON/COFINAL_LIFT/FAKE/IHARA` も同様に false 固定。**「照合済み(cross-checked)」であって「検証済み」ではない**という工房の規律に沿っている。

---

## 4. 指摘

**【要修正】4-1. CV-9 主検問が開かれないまま本番計算が完走した。**
裁定 316/318 は「主検問(計算前・IF-FIRST 凍結時点、両実装が数値を出す前)が本体」と定める。`docs/notes/` には他ラインの `*_cv9_reading_*.md` / `*_cv9_freeze_*.md` が 10 本以上あるが、**R07 physical connection ラインのものは存在しない**(grep 済)。今回は副検問位置での事後判読であり、約 46 分(13:12:30Z → 13:58:58Z)の本番計算が無検問で走った。制度どおりなら v10/v11 の実装凍結時点で主検問を通すべきだった。

**【要修正】4-2. 「独立 checker」という表現が設計独立を含意してしまう。**
実体は §2.3 のトランスリテレーション。checker の docstring 冒頭は "The checker is intentionally a separate implementation."(`v7.py:3`)と書くが、`aggregate` は upstream の逐行写しである。格付け文言に **(c) の限定**を明示しないと、「二実装が独立に同じ数を出した」→「写像の定義が正しい」という誤読を招く。

**【要修正】4-3. Sol 901 は d2 の共有(P1 射程外)を明示していない。**
901 は「This closes the actual J1 connection input.」と述べ rho2 の未決は明記するが、**P1 の degree-2 内容が cross-check の対象外である**ことは書かれていない。格付け時に (b) を明記すること。

**【軽微】4-4. (2.1) 構造ゲートは offer 0 の d2 一本のみ。**
producer `v6.py:480-481`、checker `v7.py:1179-1185` とも `_restriction_checked` / `restriction_checked` フラグで**初回 pair 呼び出し 1 回だけ**実行。かつ「その d2 に対する pure 出力が非零である」という**非空虚性の主張がない**。もし node 0 の pure 部分が零なら `0 == 0` の照合になる。ローカルでは artifact(245MB)を持たないため**非空虚性は UNKNOWN**。安価な追試: 受領書に `nonzero_pure_coordinates` を 1 個足すだけ。

**【軽微】4-5. 共有カーネルの common-mode(ただし rank に対しては load-bearing でない)。**
`DIGITS` / `AXPY` / `SCALE2` / `FIRST_TRIT` / `FIRST_VALUE` は両側で同一式を再打鍵(producer `v6.py:135-147` / checker `v7.py:176-194`)。数値検査で両テーブルが一致することを確認した。ただし rank 値への影響を検討した結果:
- packing 規約の誤りは両側が同じ packing で比較するため相殺する。
- `first()` の座標順が仮に誤っていても、非零座標を返す限り Gauss 消去の**階数は pivot 選択順に依らない**。`ELL_WIDTH % 4 = 0`(padding なし)なので非零ベクトルに対し `first()` が `None` を返す経路もない。
→ したがって【軽微】。ただしこれは「0 でない」保証ではなく「この観点では rank を壊す経路を見つけられなかった」という報告。

**【軽微】4-6. checker は semantic 6 receipts / checker result / workflow receipt をファイルとして読まない。**
producer のみ `v6.py:496-497` で 8 本のバイト pin を検査。checker は `source_ancestry()`(`v7.py:1265-1289`)の literal 一致で代替。同一値なので同一対象性は損なわれないが、両側の検査範囲は非対称。

**【軽微】4-7. P1 artifact id は実行可能ファイルに固定されておらず workflow_dispatch 入力。**
`v11.yml:10` の `p1_artifact_name`(required, default `task809-...-33851744070-1`)。両 executable は `p1["id"] > 0` と内部整合しか要求しない(`v6.py:244` / `v7.py:290-298`)。ただし `source_ancestry` の literal 固定により**内容**は縛られているため、事前登録の実害は小さい。格付け文の (a) に artifact id `9931437113` を書き込んで固定すること。

---

## 5. 反証できなかった範囲(正直な報告 — 保証ではない)

- **artifact 実体を見ていない**。判読はソース・workflow・Sol 監査・受領書に基づく。245MB の候補 artifact と 200MB 級の Task554 blob はローカルにない。したがって「実際に走ったバイト」が読んだソースと同一である保証は、workflow の `--selftest` と Sol 892/896 の受領書ハッシュ(`v6.py` = `6c450c2d…`, `v7.py` = `b5b210f6…`)への信頼に依存する。
- **`aggregate` と `aggregate_precision2` の数学的等価性**は §2.3 の構造対応で判定したが、`Context.transport` / `physical_shifts` の値そのものが checker の `IndependentContext` と一致するかは、8,059 行のバイト一致から**逆算的に**支持されるのみ(直接照合はしていない)。ただしこれは「同一対象か」に対しては十分。
- **紙 v530 §2 の規約が物理 hexagon 写像として正しいか**は判読対象外(スコープ制限により意図的に扱わない)。
- producer/checker は**同一 job・同一 runner・同一 numpy 2.5.1 / Python 3.13** で逐次実行される(`v11.yml:137-140`)。環境レベルの common-mode は残る(工房の標準運用の範囲内)。

---

## 6. 司令塔への一行

**同一対象。checker は producer を一切 import せず全 8,059 行を再計算して突合しており、rank/従属は独立算出値。ただし `Agg_le2` は逐行トランスリテレーションであり、d2 は共有入力。cross-checked を発するなら限定 (a)(b)(c) を必ず同文に含めること。**

---

本文(この行より上、区切り線を含まない)の sha256 = `e09b929caf791c07fde69ceb80ce2e82ce6e6eaa5bc5383296bf2ed9956813bb`  /  先頭 16 桁 = **e09b929caf791c07**
