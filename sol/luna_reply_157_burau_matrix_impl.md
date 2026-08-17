# Luna reply 157 — faithful matrix-56 Burau implementation

Implemented only the three authorized files:

- `search/d972_b4_burau_matrix_v1.g`
- `.github/workflows/d972-burau-matrix-v1.yml`
- this reply

The producer uses the frozen 36-point roof permutation matrix over `GF(q)`
and five literal 4x4 Burau blocks, block-diagonal in dimension 56.  It does
not construct the former high-degree point action or projectivize a Burau
block.  It builds `H`, `H'`, the exact roof homomorphism and its restriction,
enumerates the exact kernel, and replays all 972 common words.  Every row
requires an `H'` preimage with the correct roof image; each receipt includes
that full 56x56 representative, exact kernel generators, and all raw defect
counts, so a checker can reconstruct every `h0*K` fiber independently.

The workflow now runs a distinct GAP selftest for every `(q,a)` job before
calibration/full execution.  It gates on the unique dimension-56 selftest
PASS marker, GAP exit status, and diagnostic scan.  q3/q4 calibration remains
the prerequisite for q5, with fail-fast disabled and unique attempt artifacts.

Static evidence (no local GAP, GHA, git, commit, push, or dispatch was run):

- `YAML_PARSE_PASS`
- `PRODUCER_STATIC_PASS` (no legacy `D972BF`, `VectorPerm`, or old action
  marker; explicit H' preimage membership gate present)
- `WORKFLOW_GATE_STATIC_PASS` (two selftest drivers, PIPESTATUS handling,
  calibration dependency, credential-free checkout)
- producer SHA256:
  `92ECE7F5531438C69AA6D0CD2933B6F2FA2013804EC435CE53FF4344FAFBF41E`
- workflow SHA256:
  `CC28B6373066A76EC5D536E7E76C57D5C94205E397BC6E1983F7BBCAC9F2DFAB`

The remaining runtime risk is unbenchmarked GAP 4.16 behavior/resource use
for `GroupHomomorphismByImages`, `DerivedSubgroup`, exact `Kernel`, and the
roof-order computation in the 56-dimensional matrix group.  Those operations
are intentionally fail-closed in the workflow; no theorem or all-pass claim
is made here.  A finite zero-defect fiber remains only a candidate, while an
all-pass specialization is UNKNOWN.
