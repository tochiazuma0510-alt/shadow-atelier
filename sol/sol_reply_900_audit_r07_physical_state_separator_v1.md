# Sol Task900 — physical state / separator v1 release audit

## Verdict

**PASS.**  I accept the bounded physical-state / `ConnectionMember` /
canonical-`Separator` implementation.  This is an implementation verdict
only: no production state was built or opened in this audit, and no Grade-2
membership result is declared.

## Exact receipts

| file | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_grade2_physical_state_separator_v1.py` | 75,934 | 1,407 | `5f1267a7296a6f613f46a1d431c807da22239419362f32ea7c08b51fd7d6e13f` |
| `search/check_d972_r07_grade2_physical_state_separator_v1.py` | 57,325 | 734 | `01df70e8c6be4bfdff4fbedc227488edce47b1e9c195466ea7658d36b63ee107` |
| `sol/luna_reply_871_r07_physical_state_separator_v1.md` | 7,068 | 152 | `04f0c661b0648dd4005bdc7477778f64cf34f0b8fa6056a13093fc02a9bf4632` |

All three files are UTF-8 without BOM, use LF rather than CRLF, and end in
LF.  The executable receipts agree with Luna's final reply.

The live authority constants are exact: repository
`tochiazuma0510-alt/shadow-atelier`, workflow
`.github/workflows/d972-r07-canonical-p1-physical-connection-v11.yml`,
run/attempt `33876776771/1`, head
`b44ec9bd078ce0a6ca596a38cfea5012f4fee4d2`, job `101035535909`, completed
successfully, artifact id `9939860701`, name
`d972-r07-canonical-p1-physical-connection-v11-candidate-33876776771-1`,
archive bytes `245546516`, digest
`sha256:0c3753d7384a7850aadab41c9ec2755114475862a0b03fd806e875005a72995a`,
and expiry `2026-12-03T13:12:28Z`.  The accepted v6 producer, v7 checker and
v11 workflow hashes are respectively
`6c450c2d82f7ad5795d9188e2912a4587882ae3fb9351217f33393c96f75526a`,
`b5b210f6063a8fed6172417d350510eeccbafa0f60e5e676aa2732fee5e8757e`,
and `c7f3c9a8b728fa5ab0bd6be0b550b381e5b33d8ce1f59523dc04fb82b306fb74`.
The live connection terminal is pinned to offers/rank/dependent
`8059/6705/1354`, `7665974` reductions, and rolling head
`3cb1bcf691038d71082b8d4774c5dd8898a239e71ef64da22ec486ba923cb8bd`.

The rho2-v4 acquisition and its complete live roster are pinned.  In
particular, `rho2.bin` is 12,096 bytes with SHA-256
`b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e`,
`rho2-dense.bin` is 48,384 bytes with SHA-256
`abfafbc7521af43c75f1b5a73a6da5d37b90ec1648b649401d684a58cf16752e`,
and `lower-dense.bin` is 32,260 bytes with SHA-256
`c5657f998c12426cb1f2c1b4ae1e3a99ce4df9d61101eb33fba7921303bb4830`.

## Gate table

| gate | result | audit finding |
|---|---|---|
| 1. public authority | PASS | The ordinary path fixes the successful v11 tuple, accepted v6/v7/workflow hashes, live counts/head, canonical manifest and complete store receipts, and exact rho2-v4 acquisition/manifest/files. Producer and checker public CLIs reject `fixture_only=true`. A nonfixture `resume=true` launch is rejected before any root is consumed, because v1 has no authenticated live-resume authority. There is no wildcard, `ANY`, `NOT_READY`, or caller-selected terminal authority. |
| 2. physical state | PASS | The connection instruction stream is read once in offer/P1 order and all 8,059 records and EOF are authenticated. Exactly the 1,354 lower-dependent `connection` rows are offered. Each insertion-order physical elimination is applied synchronously to its packed 8,059-coordinate companion; zero remainders add no pivot. Only the packed physical and P1-companion stores are retained—there is no second dense coefficient matrix. |
| 3. v536 echelon/replay | PASS | Each new pivot is reduced at every earlier insertion lead, normalized to lead value 1, and checked for a unique lead; numerical lead order is never assumed. The independent checker reconstructs raw top/P1 rows and compares the complete reductions, scale, lead, offsets, rank/dependent counts, stores, rolling chain, generation and `HEAD`. Completed state publication uses a durable manifest followed by the atomic `HEAD` visibility switch. Internal bounded restart remains path-free; unauthenticated live restart is fail-closed. |
| 4. target and separator | PASS | The exact authenticated 48,384-trit rho2 is reduced through the same insertion-order pivots. Zero remainder yields the complete packed P1 expression. Otherwise the least free coordinate is selected and reverse **insertion** substitution constructs lambda. Producer and checker use overflow-safe `uint32` full-coordinate dot products and check every pivot pairing is 0 and `lambda(rho2)=1`. |
| 5. independence/tests/resources | PASS | The checker imports no producer helper and independently rebuilds source, state, target reduction and terminal. Both positive outcomes, the nonmonotone `[100,10,300]` / reverse `[300,10,100]` control, all 19 commissioned mutations, false EOF, missing/extra files, and claim boundaries pass. A bounded stop is `UNKNOWN_RESOURCE`, never NONMEMBER. The benchmark reports only a bounded measurement and the honest `c(c-1)/2 + target + reverse` envelope. |

## Bounded execution

With `PYTHONPYCACHEPREFIX` directed outside the repository, I ran:

```text
python -m py_compile search/d972_r07_grade2_physical_state_separator_v1.py search/check_d972_r07_grade2_physical_state_separator_v1.py
python search/d972_r07_grade2_physical_state_separator_v1.py --selftest
python search/check_d972_r07_grade2_physical_state_separator_v1.py --selftest
python search/d972_r07_grade2_physical_state_separator_v1.py --benchmark
```

All exited 0.  The producer reported both member and separator, physical rank
3, nonmonotone insertion leads `[100,10,300]`, reverse leads `[300,10,100]`,
and stop/resume state equality.  The independent checker reported both cases,
all 48,384 coordinates, and rejection of all 19 mutations.  My benchmark run
reported 6 operations in `0.1255331999855116` s, 9,193.02 packed
physical/P1 AXPY pairs/s, 17,054.39 reverse dot checks/s, and
`status=BOUNDED_ONLY`.  Its live envelope was correctly
`1354*1353/2=915981` physical reductions, plus target and reverse passes; this
is not a production runtime claim.  At maximal live physical rank 1,354, the
physical and companion stores are respectively 16,377,984 and 2,728,310
bytes.

I also exercised the ordinary subprocess entry points with external temporary
fixtures.  Public producer and checker each returned rc 1 with
`public_fixture_path_disabled`; the exact live launch mutated only to
`resume=true` returned rc 1 with `live_resume_not_exposed`.  Finally, I copied
a stopped checkpoint to a distinct absolute directory, resumed it, and
materialized the same Separator from fresh and resumed states: the complete
state rosters and every state byte matched, and the complete output rosters
and every terminal byte matched.

```text
VERDICT=PASS
IMPLEMENTATION_ACCEPTED=yes
PHYSICAL_STATE_SEPARATOR_ACCEPTED=yes
ACTUAL_CONNECTION_STATE=false
GRADE2_MEMBER/NONMEMBER=NOT_DECIDED
A0/COMMON/COFINAL_LIFT/FAKE/IHARA=NOT_DECLARED
verified=false
```
