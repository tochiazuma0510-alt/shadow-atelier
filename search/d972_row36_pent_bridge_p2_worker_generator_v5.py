#!/usr/bin/env python3
"""Generate the p2 row36 v5 GAP worker by an exact-count basis repair."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "search/d972_row36_pent_bridge_p2_dpap_worker_v4.g"
OUTPUT = ROOT / "search/d972_row36_pent_bridge_p2_dpap_worker_v5.g"
EXPECTED_SOURCE = "9fc4caa01a2696704fee32503377bd001f59a34bee7d405a8c39c15efbc00aba"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label} replacement count drift: {count}")
    return text.replace(old, new)


def main() -> None:
    raw = SOURCE.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != EXPECTED_SOURCE:
        raise SystemExit(f"v4 worker pin mismatch: {actual}")
    text = raw.decode("ascii")
    text = text.replace("P159OR36P2W4", "P159OR36P2W5")
    text = text.replace("PENT159O_ROW36_P2_WORKER_V4", "PENT159O_ROW36_P2_WORKER_V5")
    text = text.replace("results_v4_20260824", "results_v5_20260824")
    text = replace_once(
        text,
        "## Generated outcome-free p2 row36 direct same-word Q4 worker v4.",
        "## Generated p2 row36 direct same-word Q4 worker v5.\n"
        "## Exact repair: report canonical-Pcgs versus defining-collector coordinates\n"
        "## and serialize every accepted result in the exported defining basis.",
        "header",
    )
    old_coords = '''P159OR36P2W5Coords:=function(pc,x)
  local e;
  e:=ExponentsOfPcElement(pc,x);
  if e=fail then Error("PENT159O_ROW36_P2_WORKER_V5: coordinate failure"); fi;
  return List(e,Int);
end;;'''
    new_coords = '''P159OR36P2W5Coords:=function(pc,x)
  local e;
  # The receipt relations and marked vectors are in the defining NQ pc basis.
  # PcpGroupByCollectorNC preserves that basis in Exponents(x), whereas
  # Pcgs(G) may choose another valid sequence.  The pc argument is retained
  # solely to keep the v4 call signature unchanged.
  e:=Exponents(x);
  if e=fail or Length(e)<>Length(P159OR36P2W5Orders) then
    Error("PENT159O_ROW36_P2_WORKER_V5: defining coordinate failure");
  fi;
  return List(e,Int);
end;;'''
    text = replace_once(text, old_coords, new_coords, "coordinate function")
    anchor = '''P159OR36P2W5Marks:=List(P159OR36P2W5MarkCoords,
  c->P159OR36P2W5CoordElt(P159OR36P2W5Gens,c));;'''
    bridge = anchor + '''
P159OR36P2W5DefiningUnitRows:=[];;
for P159OR36P2W5i in [1..Length(P159OR36P2W5Orders)] do
  P159OR36P2W5Unit:=List(P159OR36P2W5Orders,x->0);;
  P159OR36P2W5Unit[P159OR36P2W5i]:=1;;
  P159OR36P2W5DefiningActual:=List(Exponents(
    P159OR36P2W5Gens[P159OR36P2W5i]),Int);;
  if P159OR36P2W5DefiningActual<>P159OR36P2W5Unit then
    Error("PENT159O_ROW36_P2_WORKER_V5: defining generator basis drift index=",
      P159OR36P2W5i," expected=",P159OR36P2W5Unit,
      " actual=",P159OR36P2W5DefiningActual);
  fi;
  Add(P159OR36P2W5DefiningUnitRows,true);
od;
for P159OR36P2W5i in [1..6] do
  P159OR36P2W5CanonicalActual:=List(ExponentsOfPcElement(
    P159OR36P2W5Pc,P159OR36P2W5Marks[P159OR36P2W5i]),Int);;
  P159OR36P2W5DefiningActual:=P159OR36P2W5Coords(P159OR36P2W5Pc,
    P159OR36P2W5Marks[P159OR36P2W5i]);;
  P159OR36P2W5CanonicalInverseActual:=List(ExponentsOfPcElement(
    P159OR36P2W5Pc,P159OR36P2W5Marks[P159OR36P2W5i]^-1),Int);;
  P159OR36P2W5DefiningInverseActual:=P159OR36P2W5Coords(P159OR36P2W5Pc,
    P159OR36P2W5Marks[P159OR36P2W5i]^-1);;
  if P159OR36P2W5CanonicalActual<>P159OR36P2W5MarkCoords[P159OR36P2W5i] or
     P159OR36P2W5CanonicalInverseActual<>
       P159OR36P2W5InverseMarkCoords[P159OR36P2W5i] then
    Print("PENT159O_ROW36_P2_WORKER_V5_V4_COORD_MISMATCH mark=",
      P159OR36P2W5i," expected=",P159OR36P2W5MarkCoords[P159OR36P2W5i],
      " canonical_pcgs_actual=",P159OR36P2W5CanonicalActual,
      " expected_inverse=",P159OR36P2W5InverseMarkCoords[P159OR36P2W5i],
      " canonical_pcgs_inverse_actual=",P159OR36P2W5CanonicalInverseActual,
      " defining_actual=",P159OR36P2W5DefiningActual,
      " defining_inverse_actual=",P159OR36P2W5DefiningInverseActual,"\\n");
  fi;
od;
Print("PENT159O_ROW36_P2_WORKER_V5_COORDINATE_BRIDGE_PASS defining_units=",
  Length(P159OR36P2W5DefiningUnitRows)," marks=6\\n");
if IsBound(P159OR36P2W5CoordinateProbeOnly) and
   P159OR36P2W5CoordinateProbeOnly=true then
  Print("PENT159O_ROW36_P2_WORKER_V5_COORDINATE_PROBE_ONLY_PASS\\n");
  QUIT_GAP(0);
fi;'''
    text = replace_once(text, anchor, bridge, "coordinate bridge")
    encoded = text.encode("ascii")
    if OUTPUT.exists() and OUTPUT.read_bytes() != encoded:
        raise SystemExit("immutable v5 worker output mismatch")
    if not OUTPUT.exists():
        OUTPUT.write_bytes(encoded)
    print(f"{OUTPUT.relative_to(ROOT).as_posix()} {len(encoded)} "
          f"{hashlib.sha256(encoded).hexdigest()}")


if __name__ == "__main__":
    main()
