# Task982 — 保存target履歴から一つのordered語とnormalized pairを読むconsumer

役: Luna producer実装。Task980を未来の実completion pin以外完成させた後に着手する。
変更可は `search/d972_r07_continuation_positive_word_readout_v1.py` と
`sol/luna_reply_982_r07_continuation_positive_word_consumer.md` のみ。
旧producer/checker/workflow/公刊票は不変。rootが唯一のgit/GHA broker。
ローカルPython/import/AST/数値/GAP、network/git/credential、追加agentは禁止。
source編集・読取・metadata/bytes/hashだけ可。実試験は後続GHAで行う。
Task983の独立算術は読取・コピー・importせず、公開ABI/schemaだけを共有する。

reply974全文のA/B/Cを実装する。reply958とreply975の公開境界、v478(2.7)/§3、
v547(4.2)/v548と2144のsigned代表を継承する。新探索宇宙や修正版canonical源を作らない。
現accepted1386/候補1418でtarget零・grade2 MEMBERは未観測。非零でも保存履歴を読めるが
positive適用はNOT_APPLICABLE、linear zeroでも独立D・side/localization条件未了なら候補に止める。

先にF4の公開ABIと**exact node op/args/receipt schema**を返書へ保存し、983/rootへ送る。
独立983はそのschemaから同一語11slotを実装する。算術実装の共有で独立性を失わせない。

## 入出力とA

971と同じ14親、`--continuation-root`、実fresh `--rho2-root`、rootが実tupleを入れる
`--acceptance` receipt、別`--output`を受ける。未観測の成功pinを作らずmissingを拒否する。
全bytes/roster/EOF/source/owner/runtime/acceptance/HEAD/完成数を結ぶ入口を設ける。
保存readerはHEADまでに限定し、既存P.load_prefixを呼ばない。読みながらHEAD外のdurable phaseを
採用したり、親へresume/writeしたりしない。異なるrunのOS絶対pathをownerにしない。

`read_target_history(parents, continuation, acceptance) -> TargetHistory`:
base全target.reductions、seed30/34、packet、旧26段、外部E、新loopのtarget.scalarを挿入順で結ぶ。
新step jはsnapshot j−1、global pivotはstart.rank+j−1。baseだけphysical store内offset、
個別delta/stepのnormalized payloadはoffset0。selected scalar、normalizing sigma、target scalarを区別。
scalar0でもpivot/ancestry/後続参照を保持。元rho2のDERIVEDはtarget bookkeepingの前提として明記する。
baseのskipped Connもnested元recordを保持しており、Conn消去や旧scanをやり直さない。
全typed pivot表・係数列・residual・selected HEAD・named parentsのreceiptを作る。

## BとC

`compile_target_word(history, literal_parents) -> OrderedWordBundle`:
reply974 F2/F3の式とprior-only typed namespace/閉包を実装する。P1の全positioned instructionsと
Task554 old-defect/Rel/actor/owner-local reductions、Conn lower/raw、physical、raw E、targetを区別。
P1非零最終alphaだけでなく、実literal依存の推移的閉包を認証する。
P1 eventsは保存順（old embedded元lead昇順→new owner-major元lead昇順）、scaleは対応箇所で一回。
V=raw * ordered P1 correction、S=(V * ordered physical correction)^sr(sigma)、
targetは全target coefficientの挿入順積。leaf係数相殺をword rootの置換に使わない。
source-lower零はV、Conn後Sのphysical-lower零と混同しない。Eに旧character projectorを加えない。
raw6cycleは0係数も保存、tree pathとnormalizerを先行nodeへ解決し、chord raw/aux9乗を区別する。
rawの普通整数epsilon/6、commutator順、sr(2)=-1を実recipeへ結ぶ。

全flattenを避け、memoized prior-only DAGをordered-word.jsonlへ出力する。
F4の八op/連続ID/node seal/child id+hash、全使用edge・receipt参照・一つの最終rootを維持。
入力receipt閉包とliteral依存閉包を別に保持し、各refのfile/offset/length/hash/pointerを認証する。

`read_normalized_pair(word_bundle) -> NormalizedPair`:
**Bと同じroot**から整数epsilon mod54を再帰計算する。標準剰余0..53、bool拒否。
18整除は剰余0/18/36、normalized pairは普通整数商r/18をF3値として読む。
raw /6は小raw SLPの普通整数のまま。巨大P1/target全語の十進整数を出したとは記さない。

prefix `d972.r07.continuation-positive-word.v1`、ASCII/sorted/compact/final LF。
F4のtarget-history/ancestor-index/ordered-word/word-manifest/normalized-pair/top manifest/result。
fresh-rho2/context、raw/word dictionaries、P1/Task554/Task712、acceptedHEAD、全source/file hashesを結ぶ。
raw word_stream SHA、node root SHA、JSONL全file SHAを区別。結果はcandidate/cross_checked=false/verified=false。
期限・memory上限はCLIで明示し、不足はUNKNOWN_RESOURCE/不正はFAILにして部分PASSを作らない。

新境界のcanaryはreply974の具体例から必要なものをまとめる。順序・逆・各scale・typed ID/offset・
target0・snapshot j−1・HEAD外tail・aux/四B・mod54/18と同一rootの誤結合を狙う。
旧suiteを再走しない。ローカルASTや試験を実行しない。保存blockとexact ABIを早めに渡す。
最終source bytes/SHA、試験未走、D/実terminal/side条件/新GHA/CV9の残件を報告する。
最終行 `AUDIT_982_VERDICT:`。
