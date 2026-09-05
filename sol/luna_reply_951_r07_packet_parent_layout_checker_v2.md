# Task951 -- versioned checker/workflow repair for actual mixed-generation parents

## F1. Actual read scope and failure boundary

Read Tasks951/950/947, reply946 and the workshop2123 express for
run33963515077/1 (commit25501f62c326290bafd223fe3b7a1d7b0ba51f0c).
The reported v1 failure occurred after the initial1356-row lambda sweep,
before packet construction, because the producer required the new v3
target_derivation_accepted_as_premise key from the older seed30 parent.
Seven synthetic canaries had passed; the actual parent layout was the gap.

Independently read the actual base/seed30/seed34 JSON through PowerShell
metadata tools, using the three exact TEMP fixtures in Task950. No local
numerical Python/GAP, network, credentials, git or dispatch was used.
Result byte/hash observations match the accepted pins:

| Actual result | Bytes | SHA256 | Result schema | Target schema |
| --- | ---: | --- | --- | --- |
| Base1354 | 457791 | d23892a4319a6d7eaa3d09af17a84e59cb6b0a1635f527fb77dc1038ae749968 | d972.r07.physical-state.Separator.v1 | d972.r07.physical-state.target-reduction.v1 |
| Seed30 | 2903961 | 60e47f7c673942611647a69087d29bd0223e40394144b43aae9e0f55da10fb8b | d972.r07.actual-seed30-materializer.v1.result | d972.r07.actual-seed30-materializer.v1.target-update |
| Seed34 | 3135681 | 3a8357365f4e5f3f7d281b811d36d49e4f334cbec3828c82833ae1b1d5af0242 | d972.r07.actual-root-seed-materializer.v3.result | d972.r07.actual-root-seed-materializer.v3.target-update |

Seed30 parents.rho2 has exactly artifact/manifest_sha256/packed_sha256.
Seed34 has those same identities and the additional premise flag=true.
The original packed rho2 identity is
b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e;
both parents join the base target manifest
55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488.
The base remainder is e0053fc6e745e4459e0324d26320bf9f5e434a2942fa4a519ebaf9e28df50011;
seed30 and seed34 retain the already registered f5040e3f... and46a6b828...
remainders respectively. No original-rho2 payload was read or target solved.

## F2. Bounded v2 delta

Created only the three Task951 paths. Published v1 files and all old lineages
remain immutable. The v2 checker copies its own accepted v1 implementation;
no new producer arithmetic was read/imported/shared. Packet construction,
all-four dynamic roots, prefix replay, physical/target arithmetic, resource
semantics and finite ROOT claim boundaries remain unchanged. Schema is v2
and the producer source identity points to the new v2 file.

The new validate_parent_generations function is called by the same metadata
loader in actual production and the actual-parent regression CLI. It requires
the exact three result/target schemas, exact legacy key absence and a typed
true flag on the v3 parent. Unexpected schemas, missing/false v3 flags and
changed original-rho2/base-target identities are rejected. It joins the exact
old target record/result/remainder references across base, seed30 and seed34.
No parent dictionary is altered and no missing flag is assigned true.

The metadata loader authenticates accepted JSON/payload byte/SHA receipts
without vector decoding, raw seed evaluation or physical/target replay.
The added start.parent_layout is an explicit sealed receipt: legacy admission
is exact-accepted-legacy-target-chain with flag_present=false/value=null;
v3 admission is exact-accepted-v3-explicit-target-premise with true/true.
It includes exact result/target/manifest/rho2/source-d/normalized/remainder
identities. The original M3-1 derived lambda_rho2 record and its three target
parents remain; actual original-rho2 reading stays false.

## F3. Actual-parent regression and workflow

```text
python -B -u search/check_d972_r07_fixed_root_packet_loop_v2.py
  --parent-layout-selftest --state-root STATE
  --delta-root SEED30 --seed34-root SEED34
```

The new mode reads the actual pinned three parents, runs the production
metadata join, and emits statusPASS, metadata_only=true, parent_layout,
exact fixture file identities and rejected_cases. The five focused in-memory
mutations are v3-flag-false, v3-flag-missing, rho2-packed-identity,
unexpected-parent-schema and base-target-manifest. The authenticated originals
are checked again after the mutations. This is separate from the inherited
parent-free --selftest; no fake large fixture replaces the actual regression.
The CLI and all numerical paths remain unexecuted locally.

Workflow d972-r07-fixed-root-packet-loop-v2 retains the ten exact input tuples,
the four modules on each arithmetic lineage, both source-data byte pins,
Python3.13/numpy2.5.1, phase markers, internal deadlines and conditional
candidate upload from reply946. It runs BOTH actual-parent metadata CLIs
after root discovery, checks the absent/true generation-specific facts and
all five rejection cases, and compares canonical parent_layout receipts.
Both JSON outputs and logs are preserved in diagnostics. It then runs the
seven inherited interface canaries before the unchanged actual schedule:
producer cap1 -> actual same-owner resume cap176 -> whole-prefix checker.

The marker is [r07-fixed-root-packet-loop-v2-run] and artifact prefixes are
v2. Only new executable pins changed; old parent and data pins are unchanged.
The normal checker CLI is reply946 F4 with the v2 filename; --max-seconds1800,
optional --output and UNKNOWN_RESOURCE/exit2 remain. No runtime PASS,
new packet rank or next selected seed is claimed in this reply.

## F4. Freeze and remaining gates

| New file | Bytes | SHA256 | LF |
| --- | ---: | --- | ---: |
| search/check_d972_r07_fixed_root_packet_loop_v2.py | 66251 | 5289253a82d942d71b1ec55505d08ab772b111f2ba08e301f67387eae19b23e5 | 1054 |
| .github/workflows/d972-r07-fixed-root-packet-loop-v2.yml | 27963 | 329429a3e8bda8461db4bc872f9c3aa614f5f346d20a398fb3480e8c8fd4e711 | 496 |

Both have CR0, finalLF and no BOM. Workflow producer freeze is84173 bytes,
SHAe040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6.
The four checker modules and two raw-data pins remain exactly reply946 F3.
Metadata readback also confirms v1 checker56545/c6a4202180342471d6e8938c0ca50c88d0fcd11bf5d2a8f9d100b83e993dfb3f
and v1 workflow26054/7586d9cdd2483d648d4f6a677e93916f02cb20bc8e039ea7113f4e208f8161d7
are unchanged. Get-Item/Get-FileHash -Algorithm SHA256 reproduce these pins.

Task952 reports PASS_STATIC_DELTA at the exact checker/producer freezes above,
with no required source fix; its scope excludes workflow/runtime execution.
Remaining gates:
root release/live-parent checks, GHA syntax and actual-parent regression,
actual fixed44 packet plus resume, full independent checker and external
incremental CV-9. No additional mathematical prerequisite is proposed.
New commit SHA / run ID: NONE by this worker; root is the release broker.

TASK951_STATUS: IMPLEMENTED_FROZEN_RUNTIME_PENDING; cross_checked=false; verified=false
