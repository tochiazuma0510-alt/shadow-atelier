#!/usr/bin/env python3
"""Generate the outcome-free GAP Q4 same-word worker for p2 row36 v4."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "ci/pent159n_p2_v14_artifacts_32660080668/d972_pent_interleave_canary_p2_receipt_v14_20260824.json"
PREREG = ROOT / "search/certs/d972_row36_pent_bridge_p2_prereg_v3_20260824.json"
OUTPUT = ROOT / "search/d972_row36_pent_bridge_p2_dpap_worker_v4.g"
EXPECTED_RECEIPT = "2722e4acfd7087a613bdc63b15a8741c34c84480658682565e3b5af833f75ed5"
EXPECTED_PREREG = "a88fac834e6a5238b95b8d364af4fd7ec4fa343386a75577f29bdb5647ce71ea"


def checked(path: Path, expected: str) -> dict:
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected:
        raise SystemExit(f"pin mismatch {path}: {actual}")
    return json.loads(raw)


def gap(value) -> str:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=True)


def main() -> None:
    receipt = checked(RECEIPT, EXPECTED_RECEIPT)
    prereg = checked(PREREG, EXPECTED_PREREG)
    q4 = receipt["quotients"]["Q4"]
    words = [row["canonical_signed_xy"] for row in prereg["canonical_word_roster"]]
    if len(words) != 32 or len({tuple(word) for word in words}) != 32:
        raise SystemExit("p2 word roster drift")
    powers = q4["pc_power_relations"]
    conjugates = [[row["i"], row["j"], row["coords"]]
                  for row in q4["pc_conjugate_relations"]]
    inverse_conjugates = [[row["i"], row["j"], row["coords"]]
                          for row in q4["pc_inverse_conjugate_relations"]]
    marks = [row["coords"] for row in q4["marked_generators"]]
    inverse_marks = [row["inverse_coords"] for row in q4["marked_generators"]]
    text = f'''#############################################################################
## Generated outcome-free p2 row36 direct same-word Q4 worker v4.
## receipt_sha256={EXPECTED_RECEIPT}
## prereg_sha256={EXPECTED_PREREG}
#############################################################################

P159OR36P2W4Orders:={gap(q4["relative_orders"])};;
P159OR36P2W4Powers:={gap(powers)};;
P159OR36P2W4Conjugates:={gap(conjugates)};;
P159OR36P2W4InverseConjugates:={gap(inverse_conjugates)};;
P159OR36P2W4MarkCoords:={gap(marks)};;
P159OR36P2W4InverseMarkCoords:={gap(inverse_marks)};;
P159OR36P2W4Words:={gap(words)};;
P159OR36P2W4Cofaces:=[[[4],[5],[6]],[[2,4],[3,5],[6]],
  [[1,2],[3],[5,6]],[[1],[2,3],[4,5]],[[1],[2],[4]]];;
P159OR36P2W4OldCofaces:=[[[4],[5],[6]],[[4,2],[5,3],[6]],
  [[2,1],[3],[6,5]],[[1],[3,2],[5,4]],[[1],[2],[4]]];;
P159OR36P2W4PB3Relators:=[[-1,2,1,2,3,-2,-3,-2],[-1,3,1,2,-3,-2]];;

P159OR36P2W4Syllables:=function(coords)
  local out,i;
  out:=[];
  for i in [1..Length(coords)] do
    if coords[i]<>0 then Add(out,i); Add(out,coords[i]); fi;
  od;
  return out;
end;;

P159OR36P2W4CoordElt:=function(gens,coords)
  local z,i;
  z:=One(gens[1]);
  for i in [1..Length(coords)] do
    if coords[i]<>0 then z:=z*gens[i]^coords[i]; fi;
  od;
  return z;
end;;

P159OR36P2W4Eval:=function(word,images)
  local z,x;
  z:=One(images[1]);
  for x in word do
    if x>0 then z:=z*images[x]; else z:=z*images[-x]^-1; fi;
  od;
  return z;
end;;

P159OR36P2W4Coords:=function(pc,x)
  local e;
  e:=ExponentsOfPcElement(pc,x);
  if e=fail then Error("PENT159O_ROW36_P2_WORKER_V4: coordinate failure"); fi;
  return List(e,Int);
end;;

P159OR36P2W4Collector:=FromTheLeftCollector(Length(P159OR36P2W4Orders));;
for P159OR36P2W4i in [1..Length(P159OR36P2W4Orders)] do
  SetRelativeOrder(P159OR36P2W4Collector,P159OR36P2W4i,
    P159OR36P2W4Orders[P159OR36P2W4i]);
  SetPower(P159OR36P2W4Collector,P159OR36P2W4i,
    P159OR36P2W4Syllables(P159OR36P2W4Powers[P159OR36P2W4i]));
od;
for P159OR36P2W4row in P159OR36P2W4Conjugates do
  SetConjugate(P159OR36P2W4Collector,P159OR36P2W4row[1],
    P159OR36P2W4row[2],P159OR36P2W4Syllables(P159OR36P2W4row[3]));
od;
for P159OR36P2W4row in P159OR36P2W4InverseConjugates do
  SetConjugate(P159OR36P2W4Collector,P159OR36P2W4row[1],
    -P159OR36P2W4row[2],P159OR36P2W4Syllables(P159OR36P2W4row[3]));
od;
UpdatePolycyclicCollector(P159OR36P2W4Collector);
if IsConfluent(P159OR36P2W4Collector)<>true then
  Error("PENT159O_ROW36_P2_WORKER_V4: nonconfluent collector");
fi;
P159OR36P2W4Group:=PcpGroupByCollectorNC(P159OR36P2W4Collector);;
P159OR36P2W4Pc:=Pcgs(P159OR36P2W4Group);;
P159OR36P2W4Gens:=GeneratorsOfGroup(P159OR36P2W4Group);;
P159OR36P2W4Marks:=List(P159OR36P2W4MarkCoords,
  c->P159OR36P2W4CoordElt(P159OR36P2W4Gens,c));;
if Size(P159OR36P2W4Group)<>{int(q4["order_decimal"])} or
   NilpotencyClassOfGroup(P159OR36P2W4Group)<>3 then
  Error("PENT159O_ROW36_P2_WORKER_V4: Q4 order/class drift");
fi;
for P159OR36P2W4i in [1..6] do
  if P159OR36P2W4Coords(P159OR36P2W4Pc,P159OR36P2W4Marks[P159OR36P2W4i])<>
       P159OR36P2W4MarkCoords[P159OR36P2W4i] or
     P159OR36P2W4Coords(P159OR36P2W4Pc,P159OR36P2W4Marks[P159OR36P2W4i]^-1)<>
       P159OR36P2W4InverseMarkCoords[P159OR36P2W4i] then
    Error("PENT159O_ROW36_P2_WORKER_V4: marked coordinate drift");
  fi;
od;

P159OR36P2W4LiteralRows:=[];;
for P159OR36P2W4slot in [1..5] do
  P159OR36P2W4Images:=List(P159OR36P2W4Cofaces[P159OR36P2W4slot],
    w->P159OR36P2W4Eval(w,P159OR36P2W4Marks));
  for P159OR36P2W4rel in P159OR36P2W4PB3Relators do
    Add(P159OR36P2W4LiteralRows,
      P159OR36P2W4Eval(P159OR36P2W4rel,P159OR36P2W4Images)=
        One(P159OR36P2W4Group));
  od;
od;
if Length(P159OR36P2W4LiteralRows)<>10 or false in P159OR36P2W4LiteralRows then
  Error("PENT159O_ROW36_P2_WORKER_V4: literal A18 relator gate");
fi;
P159OR36P2W4MutantImages:=List(P159OR36P2W4OldCofaces[2],
  w->P159OR36P2W4Eval(w,P159OR36P2W4Marks));;
if P159OR36P2W4Eval(P159OR36P2W4PB3Relators[1],P159OR36P2W4MutantImages)=
   One(P159OR36P2W4Group) then
  Error("PENT159O_ROW36_P2_WORKER_V4: reversal mutant not rejected");
fi;
if Length(P159OR36P2W4Words)<>32 or Length(Set(P159OR36P2W4Words))<>32 then
  Error("PENT159O_ROW36_P2_WORKER_V4: word roster coverage");
fi;

P159OR36P2W4Contexts:=List(P159OR36P2W4Cofaces,row->[
  P159OR36P2W4Eval(row[1],P159OR36P2W4Marks),
  P159OR36P2W4Eval(row[3],P159OR36P2W4Marks)]);;
P159OR36P2W4Results:=[];;
for P159OR36P2W4word in P159OR36P2W4Words do
  P159OR36P2W4Values:=List(P159OR36P2W4Contexts,
    c->P159OR36P2W4Eval(P159OR36P2W4word,c));
  P159OR36P2W4C:=P159OR36P2W4Values[1];
  P159OR36P2W4A:=P159OR36P2W4Values[2];
  P159OR36P2W4E:=P159OR36P2W4Values[3];
  P159OR36P2W4B:=P159OR36P2W4Values[4];
  P159OR36P2W4F:=P159OR36P2W4Values[5];
  P159OR36P2W4D:=P159OR36P2W4F*P159OR36P2W4E*P159OR36P2W4C*
    P159OR36P2W4B^-1*P159OR36P2W4A^-1;
  P159OR36P2W4Mutant:=P159OR36P2W4A^-1*P159OR36P2W4B^-1*
    P159OR36P2W4C*P159OR36P2W4E*P159OR36P2W4F;
  Add(P159OR36P2W4Results,[P159OR36P2W4word,
    P159OR36P2W4Coords(P159OR36P2W4Pc,P159OR36P2W4D),
    P159OR36P2W4Coords(P159OR36P2W4Pc,P159OR36P2W4Mutant),
    List(P159OR36P2W4Values,x->P159OR36P2W4Coords(P159OR36P2W4Pc,x))]);
od;
P159OR36P2W4OutputPath:=
  "ci/out/d972_row36_pent_bridge_p2_dpap_results_v4_20260824.json";;
P159OR36P2W4Out:=OutputTextFile(P159OR36P2W4OutputPath,false);;
if P159OR36P2W4Out=fail then
  Error("PENT159O_ROW36_P2_WORKER_V4: cannot open output");
fi;
SetPrintFormattingStatus(P159OR36P2W4Out,false);
PrintTo(P159OR36P2W4Out,P159OR36P2W4Results,"\\n");
CloseStream(P159OR36P2W4Out);
P159OR36P2W4Raw:=StringFile(P159OR36P2W4OutputPath);;
if P159OR36P2W4Raw=fail then
  Error("PENT159O_ROW36_P2_WORKER_V4: closed readback failure");
fi;
Print("PENT159O_ROW36_P2_WORKER_V4_PASS words=32 literal_relators=10 output=",
  P159OR36P2W4OutputPath," bytes=",Length(P159OR36P2W4Raw),
  " sha256=",HexSHA256(P159OR36P2W4Raw),"\\n");
'''
    raw = text.encode("ascii")
    if OUTPUT.exists() and OUTPUT.read_bytes() != raw:
        raise SystemExit("immutable worker output mismatch")
    if not OUTPUT.exists():
        OUTPUT.write_bytes(raw)
    print(f"{OUTPUT.relative_to(ROOT).as_posix()} {len(raw)} {hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()

