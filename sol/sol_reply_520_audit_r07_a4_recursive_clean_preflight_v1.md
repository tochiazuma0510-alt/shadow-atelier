# Task 520 independent audit — recursive clean-checkout A4 preflight

## Verdict and boundary

GO_FOR_GHA_REDISPATCH_CLEAN_PREFLIGHT.

The audited subject is exactly commit
043475a339391403cabde2d971c4e4f91407f362. This is transport-only
authorization. It promotes no A4, lift, fake, Ihara, A0, COMMON, or NONMEMBER
claim, and verified=false. No producer/checker production command or GAP
driver was run.

## Failed-run ordering

The read-only query of run 33578182231 returned completed/failure,
workflow_dispatch, exact head 5b379c7c5a39e15be7205e298167e3c0389480e8,
and failed job 100086613280. Checkout and GAP setup passed; Run GAP script
failed.

The traceback is v25 line 48 _load_v24, then v24 line 283 _generate, then v24
line 272 _v23_generated, ending only at:

    FileNotFoundError: .../search/d972_r07_word_independent_successor_kernel_v23.py

There is no realpath diagnostic. Because generated-shell line 10 was reached
under set -euo pipefail, repaired realpath line 7 had passed. The failed
source-patch-info pipeline precedes release curl at line 17, extraction at
line 18, and the actual producer launch at line 52. Its failure therefore
stopped the shell before curl, extraction, or producer.

## Subject-tree export and complete source chains

I resolved the subject as a commit and used read-only git archive directly on
043475a339391403cabde2d971c4e4f91407f362 into a fresh repository-external
directory. The export has no working-tree untracked files available to satisfy
a load. V47 is present there at 12536 bytes /
ba74cd1bb09bb87b50c582330bf54f943a5c4c1c77522a518460acf76a5748aa.
The Task519 reply is also present at 4476 bytes /
6bbc710043283525817244d95309ddaf3e4b72cb895dee3fcc663d65f1867053
and contains the unique final GO_FOR_GHA_REDISPATCH line.

Static AST/path inspection followed literal tuples, ROOT joins, every
Path(__file__).with_name construction, and the dynamic SOURCE recovered from
an owner namespace. The complete producer chain is

    v25 -> v24 -> v23 -> v22 -> v21 -> v20 -> v19 -> v18 -> v17
        -> v16 -> v15 -> v14 -> v13 -> v12 -> genuine generated base v6.

Every physical node in the subject archive equals its parent pin:

| node | bytes | SHA-256 |
|---|---:|---|
| producer v25 | 27075 | 8e5c16f28113218485f7196c6873dbbf3ce17a0e03bd7daafe71bc6e8da5015f |
| producer v24 | 34535 | 8dc698e43fa7971dff4af3a5a19a7ac309ab5d43a19bb1f5189c0c222df01dfe |
| producer v23 | 14472 | d9c082570cfa5c52254e159cd91ad0e722e5ad0ee1ea2c52e8161c2729ee1d9a |
| producer v22 | 4055 | 0186a8711ae356d1d01d7ccbd4e618ec5d19fa36442812a5dcfa8c452837d2c2 |
| producer v21 | 13268 | 23d90839025ae7dafdfef1a358666c640a32844544b4460aecec72644c6e0236 |
| producer v20 | 2239 | c45d48ac27f462cf342912e17e619be02ca68322c62a21897fcdc3d524e07a6f |
| producer v19 | 2388 | c7add6648f53e4ec85eb40620e3469008349e5676ac7d9602a6699a52cb4c6c1 |
| producer v18 | 27094 | 6d8b53755fc0c9e35aad6f04959f828a6ce5108767ffc57edfaa896366673f5a |
| producer v17 | 5596 | 20f1f8d08797d90017d057cf59a30d9a96bdadede64a9823c6fd0a364985963c |
| producer v16 | 15991 | bbd2c2093da3f18d2ea298c5d6955d987d4acbfc6eeb2dc9665abdad556bb2a7 |
| producer v15 | 7417 | 964b2311ac4f2a06ec2a1136e4ff798a9db1760da83bc2809deb912d9c238be7 |
| producer v14 | 11918 | 0c7595d50765062a6d2270d5b40c44b753f0ea4a96311795994a3c2502fe0c2c |
| producer v13 | 9731 | c8e93ba9b72971428f2a8dba96049e183bfe1d794ac6008cb6495e6d5661f514 |
| producer v12 | 7209 | 816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5 |
| producer base v6 | 219187 | aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a |

The complete checker chain is

    v35 -> v34 -> v33 -> v32 -> v31 -> v30 -> v28 -> v27 -> v26
        -> v25 -> v24 -> v23 -> v22 -> v17 -> v16 -> v15 -> v14
        -> genuine generated base v6.

The v30-to-v28 and v22-to-v17 jumps are actual owner edges; v29 and v18–v21
are not silently omitted dependencies. Every physical checker node likewise
equals its parent pin:

| node | bytes | SHA-256 |
|---|---:|---|
| checker v35 | 10246 | c8383a18169ec2da63e4e7a64de17f05d305c35e15393bcbb9e3c312ac6d5dd7 |
| checker v34 | 5838 | b00219523c2e5703b8c6c52c7bf24655c727ddc72c7da9fd06c746063875a9ba |
| checker v33 | 24033 | 44e79864424a21d836d0b61dbe066889e3567d250e722026143a2eb8f7d87ccf |
| checker v32 | 10036 | 8582b707cc63a965d0eef55a9df5d514b0601afee68118dddba236765034ffa0 |
| checker v31 | 19483 | 7efc8609bc7632b1705e2928228fa0269f3272f81ed0b4128468d27639eecf8e |
| checker v30 | 19871 | 660d71f34931d138a7d4fb9a4e3e2e17f7b10d3a73a32d59b90b85c9f2419529 |
| checker v28 | 11048 | c2c1629dc225ebea085b72d1900d7684f4c4184f8e064da8ec4057dc921d2bfa |
| checker v27 | 21489 | 79f42e751684f12814ac25dc7bd17ee5a6fa21b8ab9b8bdfc07c14bd37e4af2a |
| checker v26 | 2216 | b447bfc371090262a881db4b76261c534a8ef7a2b884edd65729aba1ea5fb2f4 |
| checker v25 | 2540 | 4c04fd31fe4a27c96841ddc5931961cc6d2e4162f98f239df3577ee367a57317 |
| checker v24 | 7508 | 3e10816d31a791695cf0b01fb1386ceb9c0dcd064dfcde63ab59e413278be2c6 |
| checker v23 | 2554 | c9fcbf9b4c8d56a6dd773c878b87014cc24e6bdc23e649109de75ebf5963adce |
| checker v22 | 6579 | 91ae327d9a983136cc5a1ac9188dc1ea11f9e553aef606e8bc4bf45cb9bd819a |
| checker v17 | 7574 | 0b0281af7d38f4c255f7cd3346dc816987da863a29275a2c6c1851366171cef0 |
| checker v16 | 12407 | 1470f12585d8ed16bb1dea0480787ba99d80592d3a034215cbbde20748f6090e |
| checker v15 | 10487 | 7779d545a679580130a0a191705f96e32834e67eaed37eb934e79aa7875a932d |
| checker v14 | 8074 | 7ff0fb8888b46febb8b373914a3ba31ee555e43c829e60dae915bacfb16b7b47 |
| checker base v6 | 258847 | 432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf |

Thus 33/33 chain files are committed, regular, present, and exact. In
particular the commissioned v23 and v32 repairs are not being supplied by the
working tree.

## Clean-export Python gates

In the clean export, Python 3.13.14 ran the exact wrapper/flag combinations.
All exited 0:

- v25 --source-patch-info returned generated
  286439 / e4fb7ead7e1dcfc5806574481f1e83e008991e516de20e2eb3a67753fec03098,
  with v24 owner-generated
  285814 / 9e3619f2e83dc7bea2e58d250bff3fafc24b8e09910c389b7a402a3b2d0d2d6a.
- v35 --source-patch-info returned generated
  312553 / 2ffcdede9a20acdd99bab3c4847db4c4a4f013e33fc151ac01b77f088d21df75.
- v35 --self-test emitted exactly one
  R07_A4_PHYSICAL_SHARD_V35_SELFTEST_PASS line. Its exact call counts were
  validate=2, physical-chain=2, materializer=2, read-json=2; it rejected the
  two mutations as physical:live_dual_history and
  physical:semantic_counter_order.

Each recursive restore checks both the physical parent pin and its generated
pin before returning, so reaching these final hashes exercises every link
listed above rather than only the immediate owners.

## Clean preflight through the producer boundary

The starting shell is Task519's exact 61-line reconstructed v47 shell,
16061 bytes /
f88c278bf32d6d320bd997e34bf32a62ee2b786ea921be7ff76283e7ae384d1e.
I retained lines 1–50 exactly. Their SHA-256 including LF is
ee2e0e5092dd9ce94d8f14b0fe3821b42b6fbe46e7289cef09e9bbe80578afdb.
Original line 51 is producer_start=$SECONDS. In the external audit copy it is
replaced by the unique marker print followed by exit 0, and original lines
51–61 are omitted. No conditional is open at the cut; bash -n exited 0.

The audit-only shell is 52 lines, 11228 bytes /
acf17a4c59f109bcb1f4da8edd098d8cb96045d1a2499a4eaa480b7e2a26d487.
The clean export reproduced the runner's established precondition
mkdir -p ci/out before execution. The final run emitted exactly one
TASK520_R07_A4_CLEAN_PREFLIGHT_PASS_BEFORE_PRODUCER and exited 0.

Consequently every unmodified preceding line passed: corrected realpath;
physical and generated v25/v35 pins; v44, v43, and proof pins; all five
authority regular/non-symlink gates; cap inequalities and ulimit; release
download, 56410-byte size and
5771806de2bfa769ef7d83364acd65d618be2a663d02a74497943c746a3360e3
digest; exact-one ZIP member tests; extraction; six copies; and all six
post-copy size/SHA gates.

The copied members were:

| member | bytes | SHA-256 |
|---|---:|---|
| v40.json | 9300 | 7fd2ec4a308d155e73431ae19441b29a1860dedb6243d0ddfd91d24cc8faecc5 |
| producer base checkpoint | 25581 | 595213bab8936ef10e94ce90ccf526c105d02d871c4dc5d02b6c76cb51593445 |
| producer HEAD | 700 | 910cc8afcca333dab56d9fefe35e63066eab764ac6325e3130c43a3c3d6f0114 |
| producer delta 1 | 3551 | d1f0ffdda299316ff1805f7a565ffe012fed63001bca74f0bc9e3ef2aeaf0e19 |
| producer delta 2 | 3625 | acb34c8c69863cc274df4a12c614b002101770d97292f2c0df8bb43158df8523 |
| checker checkpoint | 8991 | b96919b38272d87a6885da98a18603065d1c2ccf805cd2c4f65dd22e32ed7af2 |

The physical-root directory exists after the cut. Producer output, producer
log, checker output, and the production success marker are all absent, proving
that neither producer nor checker was invoked.

For provenance: two preliminary local harness attempts stopped before the
marker because the first omitted the runner-created ci/out directory and the
second pointed at the earlier export rather than the newly prepared export.
The accepted evidence above is from a separate fresh archive export which
neither attempt executed; only the runner precondition was created there
before its single successful preflight.

## Runtime dependency closure and unchanged post-cut shell

I extracted the final generated v25/v35 AST constants without entering either
production CLI. Both final sources name the same repo-local runtime owner set.
All 17 distinct owners below are regular files in the subject archive and
match their generated-source pins:

| owner group/item | bytes | SHA-256 |
|---|---:|---|
| task198 receipt | 31017244 | 82f7955580039f2a0271896c928515d26996f636d8e73231331da6a37f6b19f5 |
| task198 manifest | 2722 | cc8c16c8ad8f2d094868f0897bcca2a98adba75c18bf7ff397f0da67fd233ea4 |
| task198 producer attestation | 81 | b5ab577d14ed490af12e3921ee41cfea533abcbf92d60cc037f0d40035ba5090 |
| task198 checker attestation | 95 | 260eb23f73a8fb6b9cd2316aa4ea6c29a4a6db92e77d8c5c6f4f1dd6e7ff290e |
| task198 verdict | 150 | ac841c5a979bbe89bdd47c73151ecabf29783793b7b288b4d08c4824596251de |
| task176 receipt | 13649089 | 715441d8ecb1b4bb39a51cf3df15f04d6179ee6adeafa5b925485dbbe91f7f41 |
| task176 manifest | 349 | de62e5e55a2e348a3cce297764f7ff4bfedc10ebe2545f22cbc1551f15e1adc1 |
| task176 producer source | 66109 | 878cf1d8d44e74a993309ed1c613c9fc57eb62fd2da48a30fd8797ff4b19af3b |
| task176 checker source | 84980 | 4e6b97aa315fdccb4250de21e99dd78302477b90fd420215de6c6bea7d1fa695 |
| task176 checker result | 757 | e6a45a34353ce1fb54c99b4f9cbc8b106f34bfc751dd50044f2a79da72cad5e5 |
| task176 recovery v1 | 2035 | 41d2cb72614ce7e2d5b2d7a9000e861414da1c749876b3d51f1ccf2ca63390a8 |
| task176 recovery v2 | 2690 | 67dd555f6e0f943d0161ef2f2c8124b4cc31c9167846b45b43fd2001f5fbba3f |
| task198 producer source | 137169 | 6b2645b80f97256a659af81e856c086cca724b36e2a22ae70335b29ffa95d44c |
| task198 checker source | 157253 | 001277d44dbbc2acd7e03c6ecb6c6419df84996ae188cbb4be7b18f7cfb56ca1 |
| task198 GAP driver source | 20541 | 6048174be12d5f6f48508f1b2e80c87b3e1cb9df9ed348b30b6d3e19420b5068 |
| E4 source | 535219 | fe18fc31fdf3f9416ebb829112ccbd514c27e6a8d30fe24691842865277a0b29 |
| Q3 receipt | 231570 | 3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72 |

The final generated checker additionally constructs PRODUCER_CODE_PATH as
producer v22, exactly 4055 /
0186a8711ae356d1d01d7ccbd4e618ec5d19fa36442812a5dcfa8c452837d2c2;
that owner is already in the producer chain. All remaining dynamic paths are
owned input/output/checkpoint paths under ci/in or ci/out, or the six
release-supplied members. No other repo-local runtime dependency is absent
from the committed subject tree.

Finally, unexecuted production lines 51–61 have SHA-256
91241b034e778adcaf744dc3882d40de4c810233a81d09cda02d61e0f9872280
and are byte-identical between generated v46 and Task519 reconstructed v47.
They contain exactly one actual producer launch and one checker launch; the
checker remains only in the producer-PASS branch, while producer RESOURCE
runs no checker. The branch predicates, time/RSS gates, terminal cardinality,
error rejection, output ownership, and positive/RESOURCE schemas remain the
Task516/519 shell. The audit-only cut changes no production owner and weakens
no frozen production gate.

The final physical bytes/SHA-256 of this reply are supplied after freeze in
the parent delivery envelope because embedding its own digest would be
self-referential.

GO_FOR_GHA_REDISPATCH_CLEAN_PREFLIGHT
