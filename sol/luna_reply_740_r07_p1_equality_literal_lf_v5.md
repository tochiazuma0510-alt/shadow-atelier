# Luna Reply 740 — P1 equality literal-LF producer v5 / checker v3

## Result

v489 の有限 literal-LF repair のみを versioned producer/checker に適用した。実 parent replay、workflow、git、GHA は行っていない。

Producer v5 は四つの `record_sha256` を canonical JSON + literal LF (`0a`) の値へ置換し、`EQUALITY_SHA` を `e04c0d8de2cfbd264d3c93d915dc19e613a001c5278c8efdb704f06d1abb3565` へ置換した。lower/lifted pin、serialization、schema、arithmetic、replay、resource cap、claim flag は変更していない。

Checker v3 は producer v5 の path と sealed SHA のみへ追随した。producer を import せず、独立 equality calculation は変更しておらず、修正された五つの equality literal を checker に導入していない。

## Sealed peer binding

Checker v3 が byte authentication する producer は次のとおり。

```text
path   search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py
bytes  41,619
SHA256 dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf
```

## Fixture and AST scope

Producer selftest の既存 join fixture は corrected equality list と aggregate を production validator に通す。追加した一件は、character 0 の record digest を旧 backslash-`n` digest に戻し、aggregate まで協調更新しても `equality_record_pin` が拒否する live regression である。

AST top-level comparison結果:

```text
producer v4 -> v5:
  changed assignments: EQUALITY_RECORDS, EQUALITY_SHA
  changed function:    selftest
  added/removed:       none

checker v2 -> v3:
  renamed assignments: PRODUCER_V4_SOURCE/SHA -> PRODUCER_V5_SOURCE/SHA
  changed functions:   validate_producer_source, producer_source_digest, selftest
  added/removed functions: none
```

Checker の三関数差は global pin symbol の v4→v5 rename のみで、算術/replay executable body の変更ではない。scope 外の executable node change はなかった。

## Bounded commands

bytecode cache を `%TEMP%/task740-pycache` に置き、次だけを実行した。

```powershell
python -m py_compile search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v3.py
python -B search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py --selftest
python -B crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v3.py --selftest
```

結果:

```text
py_compile:       PASS
producer selftest PASS; fixture_accept=2; rejections=35
checker selftest: PASS; fixture_accept=6; rejections=41
```

## Output receipts

| file | bytes | LF lines | final LF | SHA-256 |
|---|---:|---:|---:|---|
| `search/d972_r07_grade2_p1_componentwise_semantic_replay_v5.py` | 41,619 | 382 | yes | `dc5931c3fd3ad5d1a947346599824b02ad1d7b5f699361c05f1f051076dcbdcf` |
| `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v3.py` | 130,683 | 2,689 | yes | `3cfdbe0485711b9b4a08db2d664ded7719a126e3a499724d33cd122a101e774e` |
| `sol/luna_reply_740_r07_p1_equality_literal_lf_v5.md` | self-referential reply | LF-only | yes | supplied externally after sealing |

## Boundary

```text
CLASSIFICATION=FINITE_LITERAL_LF_REPAIR
REAL_FIVE_ARTIFACT_REPLAY=DEFERRED_TO_GHA
P1_SEMANTIC_REPLAY=NOT_YET_ACCEPTED
A0/COMMON/COFINAL/FAKE/IHARA=NOT_DECLARED
verified=false
```
