# Luna 委嘱 148 — D972 A 側の無期限 relative-extension dovetail

## 0. 目的・権限・停止線

Sol 便 148 第 1 節の実装を担当してください。対象は

\[
M=K^{(9)}\cap N_{S4},\qquad Q_0=PB_3/M,\qquad |Q_0|=1{,}469{,}664
\]

以下の全ての $B_3$-安定 marked extension

\[
PB_3\twoheadrightarrow E\twoheadrightarrow Q_0,\qquad |E|=k|Q_0|,\quad k=3,4,\ldots
\]

を $k$ 昇順に重複なく列挙し、isolated 性と $GT(E)\to GT(M)$ の 972 本の fiber を producer/checker の独立二系統で計算する半決定器です。両系統が同じ空 fiber を認定した最初の候補で terminal state に入り、それ以外は無期限に継続します。有限個の all-pass から B 型を宣言してはいけません。

workflow file の新設は受信便 148 が明示的に要求しています。ただし commit / push / workflow dispatch は親 broker の仕事で、本委嘱では行いません。既存 worktree の無関係な dirty file は利用・整形・削除しないでください。

変更可能候補は次だけです。必要最小限に絞り、別名を使う場合は返信で一対一対応を示してください。

- `search/d972_dovetail_producer_v1.py`
- `search/d972_dovetail_worker_v1.g`（GAP worker が必要な場合）
- `search/check_d972_dovetail_v1.py`
- `search/d972_dovetail_state_schema_v1.json`
- `search/d972_dovetail_manifest_v1.json`
- `search/fixtures/d972_dovetail_v1/` 以下の最小負試験
- `.github/workflows/d972-dovetail.yml`
- `sol/luna_reply_148_dovetail.md`

## 1. 開始 anchor

開始時に次を SHA-256 照合し、一つでも drift があれば実装せず `ANCHOR_DRIFT` を返してください。

| anchor | SHA-256 |
|---|---|
| `ops/inbox_codex/sol_task_148_dovetail.txt` | `8890c29cf3c399da863e6705f3ccc434164c1c233ff82f648b965f99612e71f9` |
| `docs/week1-定義ノート.md` | `24db1372fd191659f1f0149cb669870dff470db1f779d3e5f83dba4171501c6c` |
| `docs/notes/d972_phase2_cofinal_execution_v1.md` | `97998cac97611f10065b463efa8a417d5da200b23dd39ca7a8b2beed32de847e` |
| `docs/notes/triad972_canonical_addendum_v2.md` | `5dc660dd0023bf9b1986cefa65ec9947ad5b3b366f210933dbe09ac2544c7659` |
| `sol/sol_reply_143_typedfiber.md` | `ef6490f286b82ade2ee5995a00a857dd92fbca6f5e136c79f855d81adab7da3a` |
| `search/certs/nf972_sourcemap_a_v3_20260804.json` | `32e268c97c77446b85787c5d7750da758df67646de414eade709ca79baf98b37` |
| `search/certs/nf972_sourcemap_b_v6_20260804.json` | `e27a71fbf00295be9a74761ef11134e3a8f324ed57f523d11d44a67fb5a207de` |

開始 HEAD は記録だけ行い、特定 commit への reset はしない。

## 2. 列挙対象の厳密な型

$\bar Q:=B_3/M$ とし、標準生成元像を $(\bar s_1,\bar s_2)$ とします。列挙対象は marked-over-base 同型類

\[
(\bar E,s_1,s_2,\rho)
\]

で、次を全て満たすものです。

1. $\bar E=\langle s_1,s_2\rangle$ は有限群。
2. $s_1s_2s_1=s_2s_1s_2$。
3. $\rho:\bar E\twoheadrightarrow\bar Q$、$\rho(s_i)=\bar s_i$。
4. $|\ker\rho|=k$。
5. $\bar E\to\bar Q\to S_3$ の kernel を $E$ とすると $|E|=k|Q_0|$。

このとき $B_3\to\bar E$ の kernel $L$ は自動的に $L\le M$ かつ $B_3$-normal で、$PB_3/L\cong E$ です。逆に、委嘱対象の任意の $B_3$-安定 $L\le M$ は $\bar E=B_3/L$ として一度現れます。

同値関係は、$s_1,s_2$ をそれぞれ保ち $\rho$ と可換する群同型です。生成対を固定する同型は高々一つなので、これを直接検査して代表を一つだけ出してください。unmarked group の SmallGroups ID だけで deduplicate してはいけません。

なお

\[
|\bar Q|=6|Q_0|=8{,}817{,}984,\qquad
|\bar E|=6k|Q_0|
\]

であり、$k=3$ でも $|\bar E|=26{,}453{,}952$ です。$\bar E$ の全乗法表を RAM に展開する旧 §1 の抽象列挙を実運転 engine にしてはいけません。

## 3. 完全な relative-extension engine

固定 base $\bar Q$ 上の kernel $H=\ker\rho$（$|H|=k$）から列挙してください。少なくとも次の有限段階を manifest と checkpoint に露出させます。

1. 位数 $k$ の群 $H$ の同型類を重複なく全列挙する。
2. 各 $H$ について $\bar Q\to\operatorname{Out}(H)$ の abstract kernel を全列挙する。
3. obstruction-zero の全 extension class を、base と kernel を固定する同値まで全列挙する。
4. 各 extension で $\bar s_1,\bar s_2$ の全 lift を取り、braid relation・生成性・exact kernel order を検査する。
5. base-fixing automorphism の marked orbit を取り、§2 の同型判定で一代表だけを emit する。

GAP package の extension routine を使ってよいですが、対象が「全 extension class」であることを API/documented theorem と独立な count receipt で束縛してください。split/central/solvable extension だけへの暗黙の制限は禁止です。SmallGroups library が当該 $k$ を完全収録する場合は $H$ 列挙の accelerator として使ってよいですが、未収録 order を飛ばして $k+1$ へ進んではいけません。

完全な nonabelian relative-extension 列挙を実装できない場合は、heuristic producer を「無期限 dovetail」と称して出荷せず、`BLOCKED_RELATIVE_EXTENSION_ENUMERATOR` と、欠ける正確な API/数学段階を返してください。sound-only の候補発見 lane を併設してもよいですが、`k_closed=true` や complete universe を名乗らせないこと。

処理順は $(k,H,\text{abstract kernel},\text{extension class},\text{marked orbit})$ の固定全順序です。各有限段階の iterator cursor を checkpoint 化し、同じ semantic key を二度 emit しないでください。後の $k$ を並行 prefetch しても、公開 ledger では小さい未閉鎖 $k$ を飛び越えて `closed` としないこと。

## 4. shadow / isolated / fiber の正本判定

候補 $L$ ごとに producer は次を有限悉皆します。

1. 正典の charming 条件を満たす全 $(m,f)$。
2. full $B_3/L$ 上の二 hexagon (3.3), (3.4)。積順序は paper convention。
3. $T_{m,f}$ の全射性。
4. 各 shadow の source kernel。全件 $L$ と一致するときだけ `isolated=true`。
5. isolated の場合だけ $GT(L)$ 全体を (3.60) で $GT(M)$ の canonical 972 keys へ reduce し、972 本全ての fiber cardinality と source-key digest を保存する。

`c in L` の場合だけ quotient-level $\theta,\tau$ shortcut を許します。`c notin L` では `docs/week1-定義ノート.md` の `word_level_required` を使い、自由群語に $\theta,\tau$ を作用させてから評価してください。両 case を schema で明示します。

$m$ 座標は正典 (3.60) の $m\bmod M_{\rm ord}$ で比較します。`M_ord/2` や $2m+1$ だけの一致で代用してはいけません。

target 972 keys は source-map A/B の一致済み canonical tuple を使用し、欠落・重複・digest drift を fail-closed にします。isolated 候補の reduction image は部分群で、紙の自然性から算術像 324 を含むため、既知前件の下で image size は `324` または `972` だけです。これ以外は `INCONSISTENT_STOP` であって witness ではありません。算術像 324 keys の登録済み lossless 列挙が見つかる場合だけ追加照合してよく、個別 key 一覧を推測・捏造しないこと。

## 5. helper 非共有 checker

checker は producer module、GAP worker helper、producer の cached shadow list を import してはいけません。共有してよいのは schema、固定 base marking、canonical target tuple、正典式だけです。

各 emitted candidate について、lossless witness（kernel presentation/table、compact permutation representation、marked lifts、factor map、必要な relator/coset witness）から次を再構成してください。

1. group law、位数、marked generation、braid relation、$\rho$ の well-definedness/surjectivity/kernel order。
2. $B_3$-安定性（§2 の quotient factorization として検査）。
3. charming universe と full hexagon を producer と別の loop/normal form で全再列挙。
4. settlement を、producer の presentation test と別の synchronized Cayley/Schreier traversal で直接検査。
5. exact (3.60) reduction、target set equality、972 fiber cardinalities、zero-key set。

producer と checker が `isolated`, `|GT(L)|`, image set, 972 fiber vector, zero-key set の全てで一致したときだけ `cross_checked=true` とします。単なる SHA/count 一致は独立検査ではありません。

## 6. 較正・負試験・terminal rule

本探索は $k=3$ からですが、unlock 前に次を両系統で再現してください。

- $k=1$: base $M$、isolated、$|GT(M)|=972$、identity reduction。
- $k=2$: §5.4 の marked orbit は exactly 3。split 1 orbit は $|GT(L)|=972$、nonsplit 2 orbit は各 $|GT(L)|=1{,}944$。全三 orbit が isolated、image 972、zero fiber 0。

この較正は検索結果へ混ぜず `calibration_only=true` とします。一つでも不一致なら $k=3$ を開始しません。

最低限、factor map、kernel order、braid relation、word-level mode、settlement、$m$ modulus、fiber 一行を一つずつ壊す fixture を置き、対応 gate が `FAIL/STOP` になることを確認してください。

terminal rule は次だけです。

- 両系統が isolated と認定。
- 972 target keys と fiber vector が exact 一致。
- zero-key set が非空。
- image が target group の部分群で size 324（$A_{\rm ar}\le\operatorname{Im}R$ と $|A_{\rm ar}|=324$ から紙上は自動的に $A_{\rm ar}$ と一致）。

全て満たしたとき `A_WITNESS_CROSSCHECKED` とし、candidate ID、$k$、marked extension witness、最初の zero key、全 zero keys、両実装 digest、checkpoint parent hash を terminal artifact に保存します。Lean certificate は無いので `verified` と書かないでください。

all 972 fibers が非空なら `CONTINUE` だけです。何段続いても `B`, `genuine`, `all refinements survive` を宣言しないこと。二系統不一致は `DISAGREE_STOP`、timeout/resource exhaustion は checkpoint つき `UNKNOWN/RESUME` とします。

## 7. workflow — 無期限とは有限 slice の列

GitHub Actions の単一 job を無期限化してはいけません。`.github/workflows/d972-dovetail.yml` は次を満たす resumable slice とします。

1. `workflow_dispatch` と定期 `schedule` の両方。default branch 上で継続。
2. 固定 concurrency group、`cancel-in-progress: false`。
3. job timeout より短い内部 watchdog（目安 300 分対 330 分）で安全に checkpoint。
4. 前回の最新 valid state artifact を API で取得し、schema/code/input digests、parent SHA-256 hash chain、cursor monotonicity を照合。valid state が無い初回だけ initialize。
5. 各 run は terminal/nonterminal を問わず state、producer ledger、checker ledger、stderr、resource receipt を artifact 化。次 run は最後の両系統一致 cursor からだけ再開。
6. artifact download failure や hash-chain fork を新規初期化で隠さず `STATE_STOP`。
7. terminal state 後の schedule は no-op で同 terminal digest を報告。
8. workflow 自身は commit、push、次 run の自己 dispatch をしない。cron が次 slice を起動する。
9. permissions は read-only 最小限。secret や token を artifact/log に出さない。

`workflow_dispatch` input は `preflight_only`, `slice_seconds`, optional explicit resume run-id 程度に限定し、宇宙・開始 $k$・predicate を手動で変えられないようにしてください。

## 8. 受入条件と返信

`sol/luna_reply_148_dovetail.md` に次を記録します。

1. 開始 HEAD、全 anchor hash、変更ファイル一覧。
2. relative-extension 列挙の完全性根拠。使用 package/API と、その射程（nonabelian を含むか）。
3. canonical marked-over-base dedup の証明と実装 gate。
4. producer/checker の helper 非共有表。
5. $k=1,2$ 較正の raw counts と全 fiber histogram。
6. 全負試験の期待/実値。
7. checkpoint を意図的に中断・再開した試験。semantic key の欠落/重複 0、parent hash 一致。
8. producer/checker の実行コマンド、exit code、wall/RSS/disk receipt。
9. workflow YAML の static validation。親が dispatch していない段階で run id を推測しない。
10. `git diff --check` と `git status --short` の原文。commit/push/dispatch はしない。

完全 extension enumerator が閉じなければ、その一点を正直に `BLOCKED_RELATIVE_EXTENSION_ENUMERATOR` として返してください。候補限定 lane や有限 catalog laneだけを、委嘱された「全 marked extension の無期限 dovetail」に格上げしないこと。
