#!/usr/bin/env python3
"""Generate the frozen p3 row36 v11 direct same-word Q4 GAP worker."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CANARY = ROOT / (
    "ci/pent159n_p3_v5_artifacts_32661138818/"
    "d972_pent_interleave_canary_p3_receipt_v5_20260824.json"
)
PREREG = ROOT / (
    "ci/row36_p3_prereg_artifacts_32670144124/"
    "d972_row36_pent_bridge_p3_prereg_v8_20260824.json"
)
OUTPUT = ROOT / "search/d972_row36_pent_bridge_p3_q4_outcome_worker_v11.g"

CANARY_PIN = (5223102,
              "8838dbfecbb8f487265801de860c91207de56e4acf5e98088e6d9cd161390530")
PREREG_PIN = (66337660,
              "2d33542ba797440ec96d16e02f9f8d7ea537048eb84d02b2ce57153d147faea4")
Q4_DIGEST = "042ab5607977d896401c3373ce4b37285cfd4eeb03925c7fa2559bbe3dea9384"
WORD_ROSTER_DIGEST = "25a1192cb60321035feb5f36045c4417eb0a92a07e1be7918cbabadff19a04a1"
RAW_ROSTER_DIGEST = "644e254535d210c2cf16778ee2d09b762358fb80ea0a82c839f5a8e1c01561ee"


def pin(path: Path, expected: tuple[int, str]) -> bytes:
    raw = path.read_bytes()
    actual = (len(raw), hashlib.sha256(raw).hexdigest())
    if actual != expected:
        raise SystemExit(f"pin drift {path}: {actual!r} != {expected!r}")
    return raw


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def gap(value: Any) -> str:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=True)


def main() -> None:
    canary = json.loads(pin(CANARY, CANARY_PIN))
    prereg = json.loads(pin(PREREG, PREREG_PIN))
    if canary.get("status") != "MEASURED_P3_LITERAL_A18_IDENTITY_SERIALIZATION_REPAIR_V5":
        raise SystemExit("canary status drift")
    if prereg.get("schema") != "d972-row36-pent-bridge-p3-prereg/v8" or \
       prereg.get("status") != "PREREGISTERED_BEFORE_ROW_PREDICATE_OUTCOME":
        raise SystemExit("prereg schema/status drift")
    if prereg.get("terminal_token") != "PENT159O_ROW36_P3_PREREG_V8_FROZEN":
        raise SystemExit("prereg terminal drift")
    if prereg["coverage_freeze"]["canonical_word_roster_sha256"] != WORD_ROSTER_DIGEST or \
       prereg["coverage_freeze"]["raw_roster_sha256"] != RAW_ROSTER_DIGEST:
        raise SystemExit("prereg roster digest drift")

    q4 = canary["quotients"]["Q4"]
    if digest(q4) != Q4_DIGEST or q4.get("prime") != 3 or \
       q4.get("pc_generator_count") != 26 or \
       q4.get("relative_orders") != [3] * 26 or \
       q4.get("order_decimal") != "2541865828329" or \
       q4.get("nilpotency_class") != 3:
        raise SystemExit("Q4 public pc record drift")
    words = prereg["canonical_word_roster"]
    if len(words) != 17496:
        raise SystemExit(f"word count drift {len(words)}")
    signed_words = []
    seen = set()
    for index, row in enumerate(words):
        word = row["canonical_signed_xy"]
        if row["word_id"] != f"W{index + 1:05d}" or \
           row["word_sha256"] != digest(word) or \
           any(x not in (-2, -1, 1, 2) for x in word):
            raise SystemExit(f"word row drift {index}")
        key = tuple(word)
        if key in seen:
            raise SystemExit(f"duplicate word {index}")
        seen.add(key)
        signed_words.append(word)
    if digest(words) != WORD_ROSTER_DIGEST:
        raise SystemExit("word roster canonical digest drift")

    powers = q4["pc_power_relations"]
    conjugates = [[int(r["i"]), int(r["j"]), r["coords"]]
                  for r in q4["pc_conjugate_relations"]]
    inverse_conjugates = [[int(r["i"]), int(r["j"]), r["coords"]]
                          for r in q4["pc_inverse_conjugate_relations"]]
    marks = [r["coords"] for r in q4["marked_generators"]]
    inverse_marks = [r["inverse_coords"] for r in q4["marked_generators"]]
    if not (len(powers) == 26 and len(conjugates) == 325 and
            len(inverse_conjugates) == 325 and len(marks) == len(inverse_marks) == 6):
        raise SystemExit("Q4 relation/mark count drift")

    prefix = f'''#############################################################################
## Generated p3 row36 direct same-word Q4 outcome worker v11.
## canary_receipt_sha256={CANARY_PIN[1]}
## prereg_sha256={PREREG_PIN[1]}
## q4_public_record_sha256={Q4_DIGEST}
## canonical_word_roster_sha256={WORD_ROSTER_DIGEST}
#############################################################################

P159OR36P3W11Orders:={gap(q4["relative_orders"])};;
P159OR36P3W11Powers:={gap(powers)};;
P159OR36P3W11Conjugates:={gap(conjugates)};;
P159OR36P3W11InverseConjugates:={gap(inverse_conjugates)};;
P159OR36P3W11MarkCoords:={gap(marks)};;
P159OR36P3W11InverseMarkCoords:={gap(inverse_marks)};;
P159OR36P3W11Words:={gap(signed_words)};;
P159OR36P3W11Cofaces:=[[[4],[5],[6]],[[2,4],[3,5],[6]],
  [[1,2],[3],[5,6]],[[1],[2,3],[4,5]],[[1],[2],[4]]];;
P159OR36P3W11OldCofaces:=[[[4],[5],[6]],[[4,2],[5,3],[6]],
  [[2,1],[3],[6,5]],[[1],[3,2],[5,4]],[[1],[2],[4]]];;
P159OR36P3W11PB3Relators:=[[-1,2,1,2,3,-2,-3,-2],[-1,3,1,2,-3,-2]];;

'''
    body = r'''P159OR36P3W11Syllables:=function(coords)
  local out,i;
  out:=[];
  for i in [1..Length(coords)] do
    if coords[i]<>0 then Add(out,i); Add(out,coords[i]); fi;
  od;
  return out;
end;;

P159OR36P3W11CoordElt:=function(gens,coords)
  local z,i;
  z:=One(gens[1]);
  for i in [1..Length(coords)] do
    if coords[i]<>0 then z:=z*gens[i]^coords[i]; fi;
  od;
  return z;
end;;

P159OR36P3W11Eval:=function(word,images)
  local z,x;
  z:=One(images[1]);
  for x in word do
    if x>0 then z:=z*images[x]; else z:=z*images[-x]^-1; fi;
  od;
  return z;
end;;

P159OR36P3W11Coords:=function(x)
  local e;
  e:=Exponents(x);
  if e=fail or Length(e)<>26 then
    Error("PENT159O_ROW36_P3_WORKER_V11: defining coordinate failure");
  fi;
  return List(e,Int);
end;;

P159OR36P3W11Collector:=FromTheLeftCollector(26);;
for P159OR36P3W11i in [1..26] do
  SetRelativeOrder(P159OR36P3W11Collector,P159OR36P3W11i,
    P159OR36P3W11Orders[P159OR36P3W11i]);
  SetPower(P159OR36P3W11Collector,P159OR36P3W11i,
    P159OR36P3W11Syllables(P159OR36P3W11Powers[P159OR36P3W11i]));
od;
for P159OR36P3W11row in P159OR36P3W11Conjugates do
  SetConjugate(P159OR36P3W11Collector,P159OR36P3W11row[1],
    P159OR36P3W11row[2],P159OR36P3W11Syllables(P159OR36P3W11row[3]));
od;
for P159OR36P3W11row in P159OR36P3W11InverseConjugates do
  SetConjugate(P159OR36P3W11Collector,P159OR36P3W11row[1],
    -P159OR36P3W11row[2],P159OR36P3W11Syllables(P159OR36P3W11row[3]));
od;
UpdatePolycyclicCollector(P159OR36P3W11Collector);
if IsConfluent(P159OR36P3W11Collector)<>true then
  Error("PENT159O_ROW36_P3_WORKER_V11: nonconfluent collector");
fi;
P159OR36P3W11Group:=PcpGroupByCollectorNC(P159OR36P3W11Collector);;
P159OR36P3W11Gens:=GeneratorsOfGroup(P159OR36P3W11Group);;
P159OR36P3W11Marks:=List(P159OR36P3W11MarkCoords,
  c->P159OR36P3W11CoordElt(P159OR36P3W11Gens,c));;

for P159OR36P3W11i in [1..26] do
  P159OR36P3W11Unit:=List([1..26],x->0);;
  P159OR36P3W11Unit[P159OR36P3W11i]:=1;
  if P159OR36P3W11Coords(P159OR36P3W11Gens[P159OR36P3W11i])<>
     P159OR36P3W11Unit then
    Error("PENT159O_ROW36_P3_WORKER_V11: defining basis drift index=",
      P159OR36P3W11i);
  fi;
od;
for P159OR36P3W11i in [1..6] do
  if P159OR36P3W11Coords(P159OR36P3W11Marks[P159OR36P3W11i])<>
       P159OR36P3W11MarkCoords[P159OR36P3W11i] or
     P159OR36P3W11Coords(P159OR36P3W11Marks[P159OR36P3W11i]^-1)<>
       P159OR36P3W11InverseMarkCoords[P159OR36P3W11i] then
    Error("PENT159O_ROW36_P3_WORKER_V11: marked coordinate drift index=",
      P159OR36P3W11i);
  fi;
od;
if Size(P159OR36P3W11Group)<>2541865828329 or
   NilpotencyClassOfGroup(P159OR36P3W11Group)<>3 then
  Error("PENT159O_ROW36_P3_WORKER_V11: Q4 order/class drift");
fi;
Print("PENT159O_ROW36_P3_WORKER_V11_PUBLIC_PC_PASS units=26 powers=26 conjugates=325 inverse_conjugates=325 marks=6 inverse_marks=6 order=2541865828329 class=3\n");

P159OR36P3W11LiteralRows:=[];;
for P159OR36P3W11slot in [1..5] do
  P159OR36P3W11Images:=List(P159OR36P3W11Cofaces[P159OR36P3W11slot],
    w->P159OR36P3W11Eval(w,P159OR36P3W11Marks));
  for P159OR36P3W11rel in P159OR36P3W11PB3Relators do
    Add(P159OR36P3W11LiteralRows,
      P159OR36P3W11Eval(P159OR36P3W11rel,P159OR36P3W11Images)=
        One(P159OR36P3W11Group));
  od;
od;
if Length(P159OR36P3W11LiteralRows)<>10 or false in P159OR36P3W11LiteralRows then
  Error("PENT159O_ROW36_P3_WORKER_V11: literal A18 relator gate");
fi;
P159OR36P3W11MutantImages:=List(P159OR36P3W11OldCofaces[2],
  w->P159OR36P3W11Eval(w,P159OR36P3W11Marks));;
if P159OR36P3W11Eval(P159OR36P3W11PB3Relators[1],
     P159OR36P3W11MutantImages)=One(P159OR36P3W11Group) then
  Error("PENT159O_ROW36_P3_WORKER_V11: reversal mutant not rejected");
fi;
if Length(P159OR36P3W11Words)<>17496 or
   Length(Set(P159OR36P3W11Words))<>17496 then
  Error("PENT159O_ROW36_P3_WORKER_V11: word roster coverage");
fi;
Print("PENT159O_ROW36_P3_WORKER_V11_A18_WORD_GATE_PASS literal_relators=10 mutant_rejected=true words=17496\n");

P159OR36P3W11Contexts:=List(P159OR36P3W11Cofaces,row->[
  P159OR36P3W11Eval(row[1],P159OR36P3W11Marks),
  P159OR36P3W11Eval(row[3],P159OR36P3W11Marks)]);;
P159OR36P3W11Results:=[];;
for P159OR36P3W11i in [1..17496] do
  P159OR36P3W11word:=P159OR36P3W11Words[P159OR36P3W11i];;
  P159OR36P3W11Values:=List(P159OR36P3W11Contexts,
    c->P159OR36P3W11Eval(P159OR36P3W11word,c));;
  P159OR36P3W11C:=P159OR36P3W11Values[1];;
  P159OR36P3W11A:=P159OR36P3W11Values[2];;
  P159OR36P3W11E:=P159OR36P3W11Values[3];;
  P159OR36P3W11B:=P159OR36P3W11Values[4];;
  P159OR36P3W11F:=P159OR36P3W11Values[5];;
  P159OR36P3W11D:=P159OR36P3W11F*P159OR36P3W11E*
    P159OR36P3W11C*P159OR36P3W11B^-1*P159OR36P3W11A^-1;;
  P159OR36P3W11Mutant:=P159OR36P3W11A^-1*P159OR36P3W11B^-1*
    P159OR36P3W11C*P159OR36P3W11E*P159OR36P3W11F;;
  Add(P159OR36P3W11Results,[P159OR36P3W11word,
    P159OR36P3W11Coords(P159OR36P3W11D),
    P159OR36P3W11Coords(P159OR36P3W11Mutant),
    List(P159OR36P3W11Values,P159OR36P3W11Coords)]);
  if P159OR36P3W11i mod 1000=0 then
    Print("PENT159O_ROW36_P3_WORKER_V11_PROGRESS words=",
      P159OR36P3W11i,"/17496\n");
  fi;
od;
P159OR36P3W11OutputPath:=
  "ci/out/d972_row36_pent_bridge_p3_q4_results_v11_20260824.json";;
P159OR36P3W11Out:=OutputTextFile(P159OR36P3W11OutputPath,false);;
if P159OR36P3W11Out=fail then
  Error("PENT159O_ROW36_P3_WORKER_V11: cannot open output");
fi;
SetPrintFormattingStatus(P159OR36P3W11Out,false);
PrintTo(P159OR36P3W11Out,P159OR36P3W11Results,"\n");
CloseStream(P159OR36P3W11Out);
P159OR36P3W11Raw:=StringFile(P159OR36P3W11OutputPath);;
if P159OR36P3W11Raw=fail then
  Error("PENT159O_ROW36_P3_WORKER_V11: closed readback failure");
fi;
Print("PENT159O_ROW36_P3_WORKER_V11_PASS words=17496 literal_relators=10 direct_same_word=true output=",
  P159OR36P3W11OutputPath," bytes=",Length(P159OR36P3W11Raw),
  " sha256=",HexSHA256(P159OR36P3W11Raw),"\n");
'''
    output = (prefix + body).encode("ascii")
    if OUTPUT.exists() and OUTPUT.read_bytes() != output:
        raise SystemExit("immutable v11 worker output mismatch")
    if not OUTPUT.exists():
        OUTPUT.write_bytes(output)
    print(f"{OUTPUT.relative_to(ROOT).as_posix()} {len(output)} "
          f"{hashlib.sha256(output).hexdigest()}")


if __name__ == "__main__":
    main()
