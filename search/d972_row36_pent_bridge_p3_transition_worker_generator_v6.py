#!/usr/bin/env python3
"""Generate the outcome-free p3 Q3 transition worker v6."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "ci/pent159n_p3_v5_artifacts_32661138818/d972_pent_interleave_canary_p3_receipt_v5_20260824.json"
OUTPUT = ROOT / "search/d972_row36_pent_bridge_p3_transition_worker_v6.g"
EXPECTED_RECEIPT = "8838dbfecbb8f487265801de860c91207de56e4acf5e98088e6d9cd161390530"
RESULT_PATH = "ci/out/d972_row36_pent_bridge_p3_transition_results_v6_20260824.json"


def checked_json(path: Path, expected: str) -> dict:
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected:
        raise SystemExit(f"input pin mismatch {path}: {actual}")
    return json.loads(raw)


def canonical_digest(value) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def gap(value) -> str:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=True)


def projection_from_receipt(receipt: dict) -> list[dict]:
    trace = receipt["actual_charming_onto_gate"]["full_gate_trace"]
    if len(trace) != 19683:
        raise SystemExit(f"trace count drift: {len(trace)}")
    words: dict[tuple[int, ...], tuple[int, ...]] = {}
    repetitions: dict[tuple[int, ...], set[int]] = {}
    counts: dict[tuple[int, ...], int] = {}
    for row in trace:
        coords = tuple(row["f_coords"])
        word = tuple(row["f_word"])
        if len(coords) != 7 or any(x not in (0, 1, 2) for x in coords):
            raise SystemExit("projection coordinate drift")
        if any(x not in (-2, -1, 1, 2) for x in word):
            raise SystemExit("projection word drift")
        if coords in words and words[coords] != word:
            raise SystemExit("projection word conflict")
        words.setdefault(coords, word)
        repetitions.setdefault(coords, set()).add(int(row["m"]))
        counts[coords] = counts.get(coords, 0) + 1
    expected = list(itertools.product(range(3), repeat=7))
    if sorted(words) != expected or len(set(words.values())) != 2187:
        raise SystemExit("projection bijection drift")
    if any(counts[c] != 9 or repetitions[c] != set(range(9)) for c in expected):
        raise SystemExit("projection repetition drift")
    return [{"q_coords": list(c), "signed_xy": list(words[c]),
             "word_sha256": canonical_digest(list(words[c]))} for c in expected]


def main() -> None:
    receipt = checked_json(RECEIPT, EXPECTED_RECEIPT)
    q3 = receipt["quotients"]["Q2"]
    if (q3["pc_generator_count"] != 7 or q3["relative_orders"] != [3] * 7 or
            int(q3["order_decimal"]) != 2187 or q3["exponent"] != 9 or
            q3["nilpotency_class"] != 3):
        raise SystemExit("Q3 public record shape drift")
    projection = projection_from_receipt(receipt)
    powers = q3["pc_power_relations"]
    inverses = q3["pc_inverse_relations"]
    conjugates = [[r["i"], r["j"], r["coords"]]
                  for r in q3["pc_conjugate_relations"]]
    inverse_conjugates = [[r["i"], r["j"], r["coords"]]
                          for r in q3["pc_inverse_conjugate_relations"]]
    marks = [r["coords"] for r in q3["marked_generators"]]
    inverse_marks = [r["inverse_coords"] for r in q3["marked_generators"]]
    source_relators = q3["source_presentation"]["relations"]
    projection_words = [r["signed_xy"] for r in projection]
    projection_sha = canonical_digest(projection)
    text = f'''#############################################################################
## Generated outcome-free p3 row36 Q3 transition worker v6.
## receipt_sha256={EXPECTED_RECEIPT}
## projection_sha256={projection_sha}
#############################################################################

P159OR36P3W6Orders:={gap(q3["relative_orders"])};;
P159OR36P3W6Powers:={gap(powers)};;
P159OR36P3W6Inverses:={gap(inverses)};;
P159OR36P3W6Conjugates:={gap(conjugates)};;
P159OR36P3W6InverseConjugates:={gap(inverse_conjugates)};;
P159OR36P3W6MarkCoords:={gap(marks)};;
P159OR36P3W6InverseMarkCoords:={gap(inverse_marks)};;
P159OR36P3W6SourceRelators:={gap(source_relators)};;
P159OR36P3W6ProjectionWords:={gap(projection_words)};;

P159OR36P3W6Syllables:=function(coords)
  local out,i;
  out:=[];
  for i in [1..Length(coords)] do
    if coords[i]<>0 then Add(out,i); Add(out,coords[i]); fi;
  od;
  return out;
end;;

P159OR36P3W6CoordElt:=function(gens,coords)
  local z,i;
  z:=One(gens[1]);
  for i in [1..Length(coords)] do
    if coords[i]<>0 then z:=z*gens[i]^coords[i]; fi;
  od;
  return z;
end;;

P159OR36P3W6Coords:=function(x)
  local e;
  e:=Exponents(x);
  if e=fail or Length(e)<>7 then
    Error("PENT159O_ROW36_P3_WORKER_V6: defining coordinate failure");
  fi;
  return List(e,Int);
end;;

P159OR36P3W6Eval:=function(word,images)
  local z,x;
  z:=One(images[1]);
  for x in word do
    if x>0 then z:=z*images[x]; else z:=z*images[-x]^-1; fi;
  od;
  return z;
end;;

P159OR36P3W6Index:=function(coords)
  local value,x;
  value:=0;
  for x in coords do value:=3*value+x; od;
  return value+1;
end;;

P159OR36P3W6Collector:=FromTheLeftCollector(7);;
for P159OR36P3W6i in [1..7] do
  SetRelativeOrder(P159OR36P3W6Collector,P159OR36P3W6i,
    P159OR36P3W6Orders[P159OR36P3W6i]);
  SetPower(P159OR36P3W6Collector,P159OR36P3W6i,
    P159OR36P3W6Syllables(P159OR36P3W6Powers[P159OR36P3W6i]));
od;
for P159OR36P3W6row in P159OR36P3W6Conjugates do
  SetConjugate(P159OR36P3W6Collector,P159OR36P3W6row[1],
    P159OR36P3W6row[2],P159OR36P3W6Syllables(P159OR36P3W6row[3]));
od;
for P159OR36P3W6row in P159OR36P3W6InverseConjugates do
  SetConjugate(P159OR36P3W6Collector,P159OR36P3W6row[1],
    -P159OR36P3W6row[2],P159OR36P3W6Syllables(P159OR36P3W6row[3]));
od;
UpdatePolycyclicCollector(P159OR36P3W6Collector);
if IsConfluent(P159OR36P3W6Collector)<>true then
  Error("PENT159O_ROW36_P3_WORKER_V6: nonconfluent collector");
fi;
P159OR36P3W6Group:=PcpGroupByCollectorNC(P159OR36P3W6Collector);;
P159OR36P3W6Gens:=GeneratorsOfGroup(P159OR36P3W6Group);;
P159OR36P3W6Marks:=List(P159OR36P3W6MarkCoords,
  c->P159OR36P3W6CoordElt(P159OR36P3W6Gens,c));;
if Size(P159OR36P3W6Group)<>2187 or Exponent(P159OR36P3W6Group)<>9 or
   NilpotencyClassOfGroup(P159OR36P3W6Group)<>3 then
  Error("PENT159O_ROW36_P3_WORKER_V6: order/exponent/class drift");
fi;

for P159OR36P3W6i in [1..7] do
  P159OR36P3W6Unit:=List([1..7],x->0);;
  P159OR36P3W6Unit[P159OR36P3W6i]:=1;;
  if P159OR36P3W6Coords(P159OR36P3W6Gens[P159OR36P3W6i])<>
       P159OR36P3W6Unit or
     P159OR36P3W6Coords(P159OR36P3W6Gens[P159OR36P3W6i]^3)<>
       P159OR36P3W6Powers[P159OR36P3W6i] or
     P159OR36P3W6Coords(P159OR36P3W6Gens[P159OR36P3W6i]^-1)<>
       P159OR36P3W6Inverses[P159OR36P3W6i] then
    Error("PENT159O_ROW36_P3_WORKER_V6: defining unit/power/inverse drift index=",
      P159OR36P3W6i);
  fi;
od;
for P159OR36P3W6row in P159OR36P3W6Conjugates do
  if P159OR36P3W6Coords(P159OR36P3W6Gens[P159OR36P3W6row[1]]^
       P159OR36P3W6Gens[P159OR36P3W6row[2]])<>P159OR36P3W6row[3] then
    Error("PENT159O_ROW36_P3_WORKER_V6: conjugate replay drift ",
      P159OR36P3W6row{{[1,2]}});
  fi;
od;
for P159OR36P3W6row in P159OR36P3W6InverseConjugates do
  if P159OR36P3W6Coords(P159OR36P3W6Gens[P159OR36P3W6row[1]]^(
       P159OR36P3W6Gens[P159OR36P3W6row[2]]^-1))<>P159OR36P3W6row[3] then
    Error("PENT159O_ROW36_P3_WORKER_V6: inverse conjugate replay drift ",
      P159OR36P3W6row{{[1,2]}});
  fi;
od;
for P159OR36P3W6i in [1..2] do
  if P159OR36P3W6Coords(P159OR36P3W6Marks[P159OR36P3W6i])<>
       P159OR36P3W6MarkCoords[P159OR36P3W6i] or
     P159OR36P3W6Coords(P159OR36P3W6Marks[P159OR36P3W6i]^-1)<>
       P159OR36P3W6InverseMarkCoords[P159OR36P3W6i] then
    Error("PENT159O_ROW36_P3_WORKER_V6: marked defining-coordinate drift index=",
      P159OR36P3W6i);
  fi;
od;
if ForAny(P159OR36P3W6SourceRelators,
     w->P159OR36P3W6Eval(w,P159OR36P3W6Marks)<>One(P159OR36P3W6Group)) then
  Error("PENT159O_ROW36_P3_WORKER_V6: source relator replay drift");
fi;
Print("PENT159O_ROW36_P3_WORKER_V6_PUBLIC_PC_PASS units=7 powers=7 inverses=7 conjugates=21 inverse_conjugates=21 marks=2 source_relators={len(source_relators)}\\n");

P159OR36P3W6States:=Tuples([0..2],7);;
if Length(P159OR36P3W6States)<>2187 or
   Length(Set(P159OR36P3W6States))<>2187 then
  Error("PENT159O_ROW36_P3_WORKER_V6: state roster drift");
fi;
P159OR36P3W6Elements:=List(P159OR36P3W6States,
  c->P159OR36P3W6CoordElt(P159OR36P3W6Gens,c));;
P159OR36P3W6Positive:=List([1..2],j->List([1..2187],i->
  P159OR36P3W6Index(P159OR36P3W6Coords(
    P159OR36P3W6Elements[i]*P159OR36P3W6Marks[j]))));;
for P159OR36P3W6perm in P159OR36P3W6Positive do
  if Set(P159OR36P3W6perm)<>[1..2187] then
    Error("PENT159O_ROW36_P3_WORKER_V6: positive transition not permutation");
  fi;
od;
P159OR36P3W6Negative:=[];;
for P159OR36P3W6perm in P159OR36P3W6Positive do
  P159OR36P3W6InversePerm:=List([1..2187],x->0);;
  for P159OR36P3W6i in [1..2187] do
    P159OR36P3W6InversePerm[P159OR36P3W6perm[P159OR36P3W6i]]:=P159OR36P3W6i;
  od;
  if 0 in P159OR36P3W6InversePerm then
    Error("PENT159O_ROW36_P3_WORKER_V6: incomplete inverse permutation");
  fi;
  Add(P159OR36P3W6Negative,P159OR36P3W6InversePerm);
od;

P159OR36P3W6Seen:=List([1..2187],x->false);;
P159OR36P3W6Seen[1]:=true;;
P159OR36P3W6Queue:=[1];;
P159OR36P3W6Head:=1;;
while P159OR36P3W6Head<=Length(P159OR36P3W6Queue) do
  P159OR36P3W6Current:=P159OR36P3W6Queue[P159OR36P3W6Head];;
  P159OR36P3W6Head:=P159OR36P3W6Head+1;
  for P159OR36P3W6perm in P159OR36P3W6Positive do
    P159OR36P3W6Next:=P159OR36P3W6perm[P159OR36P3W6Current];;
    if not P159OR36P3W6Seen[P159OR36P3W6Next] then
      P159OR36P3W6Seen[P159OR36P3W6Next]:=true;
      Add(P159OR36P3W6Queue,P159OR36P3W6Next);
    fi;
  od;
od;
if Length(P159OR36P3W6Queue)<>2187 then
  Error("PENT159O_ROW36_P3_WORKER_V6: positive monoid cover drift count=",
    Length(P159OR36P3W6Queue));
fi;

if Length(P159OR36P3W6ProjectionWords)<>2187 then
  Error("PENT159O_ROW36_P3_WORKER_V6: projection word count drift");
fi;
for P159OR36P3W6i in [1..2187] do
  P159OR36P3W6Current:=1;
  for P159OR36P3W6Letter in P159OR36P3W6ProjectionWords[P159OR36P3W6i] do
    if P159OR36P3W6Letter=1 then
      P159OR36P3W6Current:=P159OR36P3W6Positive[1][P159OR36P3W6Current];
    elif P159OR36P3W6Letter=-1 then
      P159OR36P3W6Current:=P159OR36P3W6Negative[1][P159OR36P3W6Current];
    elif P159OR36P3W6Letter=2 then
      P159OR36P3W6Current:=P159OR36P3W6Positive[2][P159OR36P3W6Current];
    elif P159OR36P3W6Letter=-2 then
      P159OR36P3W6Current:=P159OR36P3W6Negative[2][P159OR36P3W6Current];
    else
      Error("PENT159O_ROW36_P3_WORKER_V6: projection letter drift");
    fi;
  od;
  if P159OR36P3W6Current<>P159OR36P3W6i then
    Error("PENT159O_ROW36_P3_WORKER_V6: signed projection replay drift state=",
      P159OR36P3W6i);
  fi;
od;

P159OR36P3W6OutputPath:="{RESULT_PATH}";;
P159OR36P3W6Out:=OutputTextFile(P159OR36P3W6OutputPath,false);;
if P159OR36P3W6Out=fail then
  Error("PENT159O_ROW36_P3_WORKER_V6: cannot open transition output");
fi;
SetPrintFormattingStatus(P159OR36P3W6Out,false);
PrintTo(P159OR36P3W6Out,[P159OR36P3W6States,
  List(P159OR36P3W6Positive,p->List(p,x->x-1)),
  List(P159OR36P3W6Negative,p->List(p,x->x-1))],"\\n");
CloseStream(P159OR36P3W6Out);
P159OR36P3W6Raw:=StringFile(P159OR36P3W6OutputPath);;
if P159OR36P3W6Raw=fail then
  Error("PENT159O_ROW36_P3_WORKER_V6: transition readback failure");
fi;
Print("PENT159O_ROW36_P3_WORKER_V6_PASS states=2187 positive_permutations=2 inverse_permutations=2 signed_replays=2187 projection_sha256={projection_sha} output=",
  P159OR36P3W6OutputPath," bytes=",Length(P159OR36P3W6Raw),
  " sha256=",HexSHA256(P159OR36P3W6Raw),"\\n");
'''
    raw = text.encode("ascii")
    if OUTPUT.exists() and OUTPUT.read_bytes() != raw:
        raise SystemExit("immutable transition worker output mismatch")
    if not OUTPUT.exists():
        OUTPUT.write_bytes(raw)
    print(f"{OUTPUT.relative_to(ROOT).as_posix()} {len(raw)} "
          f"{hashlib.sha256(raw).hexdigest()} projection_sha256={projection_sha}")


if __name__ == "__main__":
    main()
