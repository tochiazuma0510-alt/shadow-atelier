# ISO-GATE R3/R4 IF-FIRST freeze v1.2 erratum — M-ISO-8 の検出層

**状態札: `versioned erratum / 過去 IF-FIRST 本文不改変 / 再走ゼロ / Sol 再監査待ち`**

- 日付: 2026-08-05
- 修正対象: `docs/notes/iso_r3r4_iffirst_freeze_v1.md` (SHA-256 `9694d6010c7c042630731b682452bbd44ba4fe5cb317c36ad8aab4010c294bab`)
- 根拠:
  - `sol/sol_reply_105_math32.md` F105-3.2
  - `docs/notes/iso_r3r4_cv9_reading_v2.md` (SHA-256 `25b45991a1fb8ffb9612c29320e8a2119a08bf2fd8482138bac2033d614da818`)
  - `search/certs/w6_bu_s0_iso_gate_r3r4_v2_1_20260805.json` (SHA-256 `925fc4957b6e05e02659a084164b6765e78f9d772e906e46f37014232ffdf880`)

## 1. 誤り

旧 IF-FIRST §7 の M-ISO-8 行は、`settled:=true` 固定 mutant が `TRUE` を返し、real の `UNKNOWN(NONSHADOW_IN_DATUM)` と verdict mismatch を起こすため kill される、と読める。この帰属は誤りである。

## 2. 正しい 4-input verdict と不感性

v1.1 erratum どおり verdict 関数は

~~~text
ComputeVerdict(allShadowsGenuine, shadowSumOk, total, settled)
~~~

の 4 入力であり、`allShadowsGenuine=false` の `NONSHADOW_IN_DATUM` gate が settled count より先に発火する。M-ISO-2(v2) の同じ 13-element datum では:

| 経路 | allShadowsGenuine | shadowSumOk | settled/total | verdict |
|---|---:|---:|---:|---|
| real `SettledCheckGeneral` | false | true | 12/13 | `UNKNOWN(NONSHADOW_IN_DATUM)` |
| M-ISO-8 `settled:=true` mutant | false | true | 13/13 | `UNKNOWN(NONSHADOW_IN_DATUM)` |

したがって

$$
\boxed{\text{real verdict}=\text{mutant verdict}=\texttt{UNKNOWN(NONSHADOW_IN_DATUM)}}
$$

であり、verdict 比較は M-ISO-8 に対して**識別力ゼロ**である。

## 3. M-ISO-8 の唯一の正しい kill 機構

同一 datum・同一 witness の detail entry を比較し、次の二つを assertion する。

~~~text
real.witnessSettledEntry.settled   == false
mutant.witnessSettledEntry.settled == true
~~~

補助的に `real.settled_count=12`、`mutant.settled_count=13` を検査してよい。kill はこの **detail-channel mismatch** による。verdict mismatch による、と記録した cert/manifest/説明は `MISO8_SEMANTICS_STALE / STOP` とする。

この mutant は「settled predicate が常に true」を殺す較正であって、真の non-isolated marked datum、`isolated=FALSE`、または GT-shadow の陰性 witness を与えない。M-ISO-2 の混入 witness は非 shadow なので、正しい最終状態は fail-closed UNKNOWN である。

## 4. 差替表

旧 IF-FIRST §7 の M-ISO-8 行は次で差し替える。

| 量 | M-ISO-8(v1.2 正文) |
|---|---|
| datum | M-ISO-2(v2) と同じ 13-element datum / 同じ witness |
| real detail | witness `settled=false`; count 12/13 |
| mutant detail | witness `settled=true`; count 13/13 |
| verdict | real/mutant とも `UNKNOWN(NONSHADOW_IN_DATUM)` |
| detection | **detail-element comparison only** |
| 禁止帰属 | `mutant TRUE != real UNKNOWN`、verdict mismatch、`isolated=FALSE` witness |

## 5. 手続き上の射程

これは過去の再走より後に作られた versioned erratum であり、過去に欠けた事前性を遡及的に作り出さない。将来の再走・manifest・checker は本 v1.2 を規範として参照する。本書では再走、候補生成、探索を行っていない。
