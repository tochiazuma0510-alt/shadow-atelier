#!/usr/bin/env python3
"""Generate the p3 transition worker v8 from the pinned v7 worker.

V8 keeps the explicit state roster and exports both native-right transitions
and paper-append/native-left transitions.  The frozen canary projection words
are paper words, so their complete replay gate uses the latter.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "search/d972_row36_pent_bridge_p3_transition_worker_v7.g"
OUTPUT = ROOT / "search/d972_row36_pent_bridge_p3_transition_worker_v8.g"
SOURCE_SHA256 = "de654fc73fb3d69f7736c97b48b04619122bdca04c015817ff07c27a321f6768"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label} replacement count drift: {count}")
    return text.replace(old, new)


def main() -> None:
    raw = SOURCE.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != SOURCE_SHA256:
        raise SystemExit(f"v7 source pin mismatch: {actual}")
    text = raw.decode("ascii")
    text = text.replace("P159OR36P3W7", "P159OR36P3W8")
    text = text.replace("PENT159O_ROW36_P3_WORKER_V7",
                        "PENT159O_ROW36_P3_WORKER_V8")
    text = replace_once(
        text,
        "## Generated outcome-free p3 row36 Q3 transition worker v7.",
        "## Generated outcome-free p3 row36 Q3 transition worker v8.",
        "header version",
    )
    marker = "P159OR36P3W8Elements:=List(P159OR36P3W8States,"
    if text.count(marker) != 1:
        raise SystemExit(f"transition-tail marker drift: {text.count(marker)}")
    prefix = text.split(marker, 1)[0]
    tail = r'''P159OR36P3W8Elements:=List(P159OR36P3W8States,
  c->P159OR36P3W8CoordElt(P159OR36P3W8Gens,c));;

## Native right multiplication: state -> state*mark.
P159OR36P3W8RightPositive:=List([1..2],j->List([1..2187],i->
  P159OR36P3W8Index(P159OR36P3W8Coords(
    P159OR36P3W8Elements[i]*P159OR36P3W8Marks[j]))));;
for P159OR36P3W8perm in P159OR36P3W8RightPositive do
  if Set(P159OR36P3W8perm)<>[1..2187] then
    Error("PENT159O_ROW36_P3_WORKER_V8: native-right transition not permutation");
  fi;
od;
P159OR36P3W8RightNegative:=[];;
for P159OR36P3W8perm in P159OR36P3W8RightPositive do
  P159OR36P3W8InversePerm:=List([1..2187],x->0);;
  for P159OR36P3W8i in [1..2187] do
    P159OR36P3W8InversePerm[P159OR36P3W8perm[P159OR36P3W8i]]:=P159OR36P3W8i;
  od;
  if 0 in P159OR36P3W8InversePerm then
    Error("PENT159O_ROW36_P3_WORKER_V8: incomplete native-right inverse permutation");
  fi;
  Add(P159OR36P3W8RightNegative,P159OR36P3W8InversePerm);
od;

## Append a paper letter on the right: native GAP left multiplication.
P159OR36P3W8PaperPositive:=List([1..2],j->List([1..2187],i->
  P159OR36P3W8Index(P159OR36P3W8Coords(
    P159OR36P3W8Marks[j]*P159OR36P3W8Elements[i]))));;
for P159OR36P3W8perm in P159OR36P3W8PaperPositive do
  if Set(P159OR36P3W8perm)<>[1..2187] then
    Error("PENT159O_ROW36_P3_WORKER_V8: paper-left transition not permutation");
  fi;
od;
P159OR36P3W8PaperNegative:=[];;
for P159OR36P3W8perm in P159OR36P3W8PaperPositive do
  P159OR36P3W8InversePerm:=List([1..2187],x->0);;
  for P159OR36P3W8i in [1..2187] do
    P159OR36P3W8InversePerm[P159OR36P3W8perm[P159OR36P3W8i]]:=P159OR36P3W8i;
  od;
  if 0 in P159OR36P3W8InversePerm then
    Error("PENT159O_ROW36_P3_WORKER_V8: incomplete paper-left inverse permutation");
  fi;
  Add(P159OR36P3W8PaperNegative,P159OR36P3W8InversePerm);
od;

## State 2 is the frozen destructive orientation witness.
P159OR36P3W8State2Word:=P159OR36P3W8ProjectionWords[2];;
P159OR36P3W8State2Expected:=P159OR36P3W8States[2];;
P159OR36P3W8State2Direct:=P159OR36P3W8Coords(
  P159OR36P3W8Eval(P159OR36P3W8State2Word,P159OR36P3W8Marks));;
P159OR36P3W8State2Reversed:=P159OR36P3W8Coords(
  P159OR36P3W8Eval(Reversed(P159OR36P3W8State2Word),P159OR36P3W8Marks));;
P159OR36P3W8State2RightIndex:=1;;
P159OR36P3W8State2PaperIndex:=1;;
for P159OR36P3W8Letter in P159OR36P3W8State2Word do
  if P159OR36P3W8Letter=1 then
    P159OR36P3W8State2RightIndex:=P159OR36P3W8RightPositive[1][P159OR36P3W8State2RightIndex];
    P159OR36P3W8State2PaperIndex:=P159OR36P3W8PaperPositive[1][P159OR36P3W8State2PaperIndex];
  elif P159OR36P3W8Letter=-1 then
    P159OR36P3W8State2RightIndex:=P159OR36P3W8RightNegative[1][P159OR36P3W8State2RightIndex];
    P159OR36P3W8State2PaperIndex:=P159OR36P3W8PaperNegative[1][P159OR36P3W8State2PaperIndex];
  elif P159OR36P3W8Letter=2 then
    P159OR36P3W8State2RightIndex:=P159OR36P3W8RightPositive[2][P159OR36P3W8State2RightIndex];
    P159OR36P3W8State2PaperIndex:=P159OR36P3W8PaperPositive[2][P159OR36P3W8State2PaperIndex];
  elif P159OR36P3W8Letter=-2 then
    P159OR36P3W8State2RightIndex:=P159OR36P3W8RightNegative[2][P159OR36P3W8State2RightIndex];
    P159OR36P3W8State2PaperIndex:=P159OR36P3W8PaperNegative[2][P159OR36P3W8State2PaperIndex];
  else
    Error("PENT159O_ROW36_P3_WORKER_V8: state2 orientation letter drift");
  fi;
od;
if P159OR36P3W8State2Direct<>
     P159OR36P3W8States[P159OR36P3W8State2RightIndex] or
   P159OR36P3W8State2Reversed<>P159OR36P3W8State2Expected or
   P159OR36P3W8State2PaperIndex<>2 or
   P159OR36P3W8State2Direct=P159OR36P3W8State2Expected then
  Error("PENT159O_ROW36_P3_WORKER_V8: state2 orientation discriminator drift");
fi;
Print("PENT159O_ROW36_P3_WORKER_V8_ORIENTATION_PASS state=2 word=",
  P159OR36P3W8State2Word," expected=",P159OR36P3W8State2Expected,
  " native_written_right=",P159OR36P3W8State2Direct,
  " reversed_native=",P159OR36P3W8State2Reversed,
  " right_transition_index=",P159OR36P3W8State2RightIndex,
  " paper_left_transition_index=",P159OR36P3W8State2PaperIndex,"\n");

P159OR36P3W8Seen:=List([1..2187],x->false);;
P159OR36P3W8Seen[1]:=true;;
P159OR36P3W8Queue:=[1];;
P159OR36P3W8Head:=1;;
while P159OR36P3W8Head<=Length(P159OR36P3W8Queue) do
  P159OR36P3W8Current:=P159OR36P3W8Queue[P159OR36P3W8Head];;
  P159OR36P3W8Head:=P159OR36P3W8Head+1;
  for P159OR36P3W8perm in P159OR36P3W8RightPositive do
    P159OR36P3W8Next:=P159OR36P3W8perm[P159OR36P3W8Current];;
    if not P159OR36P3W8Seen[P159OR36P3W8Next] then
      P159OR36P3W8Seen[P159OR36P3W8Next]:=true;
      Add(P159OR36P3W8Queue,P159OR36P3W8Next);
    fi;
  od;
od;
if Length(P159OR36P3W8Queue)<>2187 then
  Error("PENT159O_ROW36_P3_WORKER_V8: positive monoid cover drift count=",
    Length(P159OR36P3W8Queue));
fi;

if Length(P159OR36P3W8ProjectionWords)<>2187 then
  Error("PENT159O_ROW36_P3_WORKER_V8: projection word count drift");
fi;
for P159OR36P3W8i in [1..2187] do
  P159OR36P3W8Current:=1;
  for P159OR36P3W8Letter in P159OR36P3W8ProjectionWords[P159OR36P3W8i] do
    if P159OR36P3W8Letter=1 then
      P159OR36P3W8Current:=P159OR36P3W8PaperPositive[1][P159OR36P3W8Current];
    elif P159OR36P3W8Letter=-1 then
      P159OR36P3W8Current:=P159OR36P3W8PaperNegative[1][P159OR36P3W8Current];
    elif P159OR36P3W8Letter=2 then
      P159OR36P3W8Current:=P159OR36P3W8PaperPositive[2][P159OR36P3W8Current];
    elif P159OR36P3W8Letter=-2 then
      P159OR36P3W8Current:=P159OR36P3W8PaperNegative[2][P159OR36P3W8Current];
    else
      Error("PENT159O_ROW36_P3_WORKER_V8: projection letter drift");
    fi;
  od;
  if P159OR36P3W8Current<>P159OR36P3W8i then
    Error("PENT159O_ROW36_P3_WORKER_V8: signed paper projection replay drift state=",
      P159OR36P3W8i);
  fi;
od;

P159OR36P3W8OutputPath:="ci/out/d972_row36_pent_bridge_p3_transition_results_v8_20260824.json";;
P159OR36P3W8Out:=OutputTextFile(P159OR36P3W8OutputPath,false);;
if P159OR36P3W8Out=fail then
  Error("PENT159O_ROW36_P3_WORKER_V8: cannot open transition output");
fi;
SetPrintFormattingStatus(P159OR36P3W8Out,false);
PrintTo(P159OR36P3W8Out,[P159OR36P3W8States,
  List(P159OR36P3W8RightPositive,p->List(p,x->x-1)),
  List(P159OR36P3W8RightNegative,p->List(p,x->x-1)),
  List(P159OR36P3W8PaperPositive,p->List(p,x->x-1)),
  List(P159OR36P3W8PaperNegative,p->List(p,x->x-1))],"\n");
CloseStream(P159OR36P3W8Out);
P159OR36P3W8Raw:=StringFile(P159OR36P3W8OutputPath);;
if P159OR36P3W8Raw=fail then
  Error("PENT159O_ROW36_P3_WORKER_V8: transition readback failure");
fi;
Print("PENT159O_ROW36_P3_WORKER_V8_PASS states=2187 native_right_positive=2 native_right_inverse=2 paper_left_positive=2 paper_left_inverse=2 signed_paper_replays=2187 projection_sha256=05a78aaf62e2ff691dbe80a95daebab849df8d9cb0dc7914a797a9e7e7590228 output=",
  P159OR36P3W8OutputPath," bytes=",Length(P159OR36P3W8Raw),
  " sha256=",HexSHA256(P159OR36P3W8Raw),"\n");
'''
    output_raw = (prefix + tail).encode("ascii")
    if OUTPUT.exists() and OUTPUT.read_bytes() != output_raw:
        raise SystemExit("immutable v8 transition worker output mismatch")
    if not OUTPUT.exists():
        OUTPUT.write_bytes(output_raw)
    print(f"{OUTPUT.relative_to(ROOT).as_posix()} {len(output_raw)} "
          f"{hashlib.sha256(output_raw).hexdigest()} source_sha256={actual}")


if __name__ == "__main__":
    main()
