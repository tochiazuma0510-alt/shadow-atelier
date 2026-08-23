#!/usr/bin/env python3
"""Generate the p3 transition worker v7 from the pinned v6 worker.

V7 changes only the state-roster serialization: GAP ``Tuples`` order is
replaced by the explicit base-three lexicographic order used by the frozen
Python state roster and by the worker's coordinate-to-index function.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "search/d972_row36_pent_bridge_p3_transition_worker_v6.g"
OUTPUT = ROOT / "search/d972_row36_pent_bridge_p3_transition_worker_v7.g"
SOURCE_SHA256 = "0133616171025f250bdc2f89dab0b56c0af920dc88f5b396631b5fe5f05ba7d1"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label} replacement count drift: {count}")
    return text.replace(old, new)


def main() -> None:
    raw = SOURCE.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != SOURCE_SHA256:
        raise SystemExit(f"v6 source pin mismatch: {actual}")
    text = raw.decode("ascii")
    text = text.replace("P159OR36P3W6", "P159OR36P3W7")
    text = text.replace("PENT159O_ROW36_P3_WORKER_V6",
                        "PENT159O_ROW36_P3_WORKER_V7")
    text = replace_once(
        text,
        "## Generated outcome-free p3 row36 Q3 transition worker v6.",
        "## Generated outcome-free p3 row36 Q3 transition worker v7.",
        "header version",
    )
    text = replace_once(
        text,
        "ci/out/d972_row36_pent_bridge_p3_transition_results_v6_20260824.json",
        "ci/out/d972_row36_pent_bridge_p3_transition_results_v7_20260824.json",
        "result path",
    )
    old_states = "P159OR36P3W7States:=Tuples([0..2],7);;"
    new_states = """P159OR36P3W7States:=List([0..2186],n->[
  QuoInt(n,729) mod 3,QuoInt(n,243) mod 3,QuoInt(n,81) mod 3,
  QuoInt(n,27) mod 3,QuoInt(n,9) mod 3,QuoInt(n,3) mod 3,n mod 3]);;
for P159OR36P3W7i in [1..2187] do
  if P159OR36P3W7Index(P159OR36P3W7States[P159OR36P3W7i])<>
       P159OR36P3W7i then
    Error("PENT159O_ROW36_P3_WORKER_V7: explicit lex state/index roundtrip drift index=",
      P159OR36P3W7i," coords=",P159OR36P3W7States[P159OR36P3W7i]);
  fi;
od;
Print("PENT159O_ROW36_P3_WORKER_V7_STATE_SERIALIZATION_PASS states=2187 order=explicit_base3_lex index_roundtrip=2187\\n");"""
    text = replace_once(text, old_states, new_states, "state roster")
    output_raw = text.encode("ascii")
    if OUTPUT.exists() and OUTPUT.read_bytes() != output_raw:
        raise SystemExit("immutable v7 transition worker output mismatch")
    if not OUTPUT.exists():
        OUTPUT.write_bytes(output_raw)
    print(f"{OUTPUT.relative_to(ROOT).as_posix()} {len(output_raw)} "
          f"{hashlib.sha256(output_raw).hexdigest()} source_sha256={actual}")


if __name__ == "__main__":
    main()
