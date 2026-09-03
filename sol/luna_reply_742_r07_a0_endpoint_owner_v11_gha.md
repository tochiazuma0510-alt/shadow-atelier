# Luna Task742 -- A0 endpoint owner-binding v11 GHA wrapper

```text
RESULT=COMPLETE
REAL_GHA_RUN=NOT_RUN
verified=false
```

Created only the commissioned workflow and this reply.  The workflow is
`workflow_dispatch`-only and has no job-level fire condition.  It is the v10
accepted path with producer v5 bound to the unchanged checker v4; the v4
producer protocol, payload names, producer/checker arguments, v4 checker
marker, caps, serial limits, timeouts, Task625 identities, exact 1120-byte
verdict staging, and always-upload logs are retained.  Output and log artifact
names are v11.  No parent replay, generic boundary build, real endpoint build,
GHA, or git operation was run.

The v488 proof, Task735 reply, and Task737 audit are authenticated by exact
byte size and SHA-256, with both required audit tokens checked as exact
backtick-delimited lines.  Every v10 parent/source pin and download identity
remains in the new workflow.

## Exact receipts

| path | bytes | LF | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v11.yml` | `11586` | `177` | yes | `c90509e0717081a2770b9bd8c6bf0150e9f5157ea4775357691214eebe57698d` |
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v5.py` | `43838` | `671` | yes | `2f8cb910c79cb6046c8cd7a83f77e9e883187fe81b43209e3a8d09679a12ad6b` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py` | `93236` | `1592` | yes | `581f9a5a9aa65ae298bf6d6f785ed1063ddfb0caf8a0c06e15f30ec2e713fd6f` |
| `sol/proof_r07_task640_v10_missing_owner_binding_v488.md` | `2232` | `70` | yes | `e07d52e7864042d1a3fe22538b4ba408d7cc56721135b07c34b4111e726cf763` |
| `sol/luna_reply_735_r07_task640_owner_binding_v5.md` | `4067` | `107` | yes | `a547638073b64bced8e9e0893786d8bd9fc437b3ada85b47515d5d9dfde34184` |
| `sol/sol_reply_737_audit_r07_task640_owner_binding_v5.md` | `7999` | `174` | yes | `13e6d021c197cec3ca0213ab0f57fe711b982ecc11a4e9d3ca54984d3bd8cb49` |

The reply's own post-seal receipt is intentionally not embedded because that
would be self-referential; the commander can compute it after sealing.

## Bounded checks

```text
python -B search/d972_r07_a0_fresh_precision2_endpoint_signature_v5.py --selftest
exit 0
fixture=PASS
build_heavy_trap_called=false
generic_builders_called=false
endpoint_fine_source_order=59049
q0_marked_rows=2
rho2_bytes=12096

python -B search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py --selftest
exit 0
fixture=PASS
endpoint_ceiling=484
occurrence_components=11
rho2_bytes=12096
```

The workflow was YAML-parsed locally; `workflow_dispatch` is the only event
and `fresh-endpoint.if` is absent.  No real producer/checker invocation,
parent download, artifact upload, endpoint, or rho2 was produced.
