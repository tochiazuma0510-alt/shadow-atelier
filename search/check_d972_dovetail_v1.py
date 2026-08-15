#!/usr/bin/env python3
"""Independent checker for D972 dovetail checkpoints and candidate ledgers.

This module deliberately does not import the producer, the GAP worker, or any
of their helpers.  It reconstructs the state hash, immutable bindings, finite
kernel table, marked witness shape, shadow/fiber classification, and cursor
agreement from serialized artifacts only.

Normal CLI:
  python search/check_d972_dovetail_v1.py \
    --state STATE.json --producer-ledger producer-ledger.jsonl --out-dir DIR

Exit codes: 0 = checked state written (including semantic STOP states),
2 = fail-closed state/infrastructure rejection, 64 = command-line error.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "search" / "d972_dovetail_state_schema_v1.json"
MANIFEST_PATH = ROOT / "search" / "d972_dovetail_manifest_v1.json"
TARGET_A = ROOT / "search" / "certs" / "nf972_sourcemap_a_tuples_v2_20260804.json"
TARGET_B = ROOT / "search" / "certs" / "nf972_sourcemap_b_tuples_v3_20260804.json"
SCHEMA_VERSION = "d972-dovetail-state/v1"
QBAR_ORDER = 8_817_984
ZERO_SHA = "0" * 64
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
TARGET_M_RE = re.compile(r"^\((-?[0-9]+);")
CURSOR_ORDER = ["k", "H", "outer_action", "extension_class", "marked_orbit"]


class CheckStop(RuntimeError):
    """Fail-closed malformed state, binding, or artifact."""


class Disagreement(RuntimeError):
    """Producer/checker semantic disagreement; becomes DISAGREE_STOP."""


class Inconsistent(RuntimeError):
    """A mathematically impossible isolated fiber classification."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def binding_set_digest(rows: Iterable[tuple[str, str]]) -> str:
    payload = "".join(f"{path}={digest}\n" for path, digest in sorted(rows))
    return sha_bytes(payload.encode("utf-8"))


def checkpoint_hash(state: dict[str, Any]) -> str:
    body = copy.deepcopy(state)
    try:
        body["hash_chain"]["checkpoint_sha256"] = ZERO_SHA
    except (KeyError, TypeError) as exc:
        raise CheckStop("STATE_STOP missing checkpoint hash field") from exc
    return sha_bytes(canonical_bytes(body))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    finally:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    finally:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckStop(message)


def require_disagreement(condition: bool, message: str) -> None:
    if not condition:
        raise Disagreement(message)


def is_sha(value: Any) -> bool:
    return isinstance(value, str) and SHA_RE.fullmatch(value) is not None


def cursor_tuple(cursor: dict[str, Any]) -> tuple[int, ...]:
    stages = {
        "H": 0,
        "outer_action": 1,
        "extension_class": 2,
        "marked_orbit": 3,
        "candidate_evaluation": 4,
        "k_closure": 5,
    }
    try:
        return (
            int(cursor["k"]),
            int(cursor["H"]["index"]),
            int(cursor["outer_action"]["index"]),
            int(cursor["extension_class"]["index"]),
            int(cursor["marked_orbit"]["index"]),
            stages[cursor["stage"]],
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise CheckStop("STATE_STOP malformed five-coordinate cursor") from exc


def validate_state_core(state: dict[str, Any], *, bind_current: bool = True) -> None:
    expected_top = {
        "schema_version", "state_kind", "universe", "cursor_order", "integrity",
        "hash_chain", "run", "status", "calibration_gate", "cursors",
        "enumeration", "ledgers", "terminal_witness", "receipts",
    }
    require(isinstance(state, dict) and set(state) == expected_top,
            "STATE_STOP unexpected or missing top-level fields")
    require(state["schema_version"] == SCHEMA_VERSION, "STATE_STOP schema version drift")
    require(state["cursor_order"] == CURSOR_ORDER, "STATE_STOP cursor order drift")
    require(state["universe"].get("start_k") == 3, "STATE_STOP start-k drift")
    require(state["universe"].get("manual_universe_override") is False,
            "STATE_STOP manual universe override")
    chain = state["hash_chain"]
    require(chain.get("algorithm") == "sha256", "STATE_STOP hash algorithm drift")
    require(isinstance(chain.get("sequence"), int) and chain["sequence"] >= 0,
            "STATE_STOP invalid sequence")
    parent = chain.get("parent_checkpoint_sha256")
    require((chain["sequence"] == 0 and parent is None) or
            (chain["sequence"] > 0 and is_sha(parent)),
            "STATE_STOP parent hash/sequence mismatch")
    require(is_sha(chain.get("checkpoint_sha256")) and
            chain["checkpoint_sha256"] == checkpoint_hash(state),
            "STATE_STOP checkpoint hash mismatch")

    status = state["status"]
    allowed = {
        "INITIALIZED", "CALIBRATION_PENDING", "CHECKER_PENDING", "CALIBRATION_STOP",
        "CONTINUE", "UNKNOWN/RESUME", "A_WITNESS_CROSSCHECKED", "DISAGREE_STOP",
        "INCONSISTENT_STOP", "STATE_STOP", "BLOCKED_RELATIVE_EXTENSION_ENUMERATOR",
    }
    require(status.get("code") in allowed, "STATE_STOP unknown status")
    halted = status["code"] in {
        "CALIBRATION_STOP", "A_WITNESS_CROSSCHECKED", "DISAGREE_STOP",
        "INCONSISTENT_STOP", "STATE_STOP", "BLOCKED_RELATIVE_EXTENSION_ENUMERATOR",
    }
    require(status.get("terminal") is halted and status.get("resumable") is (not halted),
            "STATE_STOP status terminal/resumable mismatch")
    require((state["state_kind"] == "TERMINAL") is halted,
            "STATE_STOP state_kind/status mismatch")

    cursors = state["cursors"]
    for lane in ("producer", "checker", "agreed"):
        cursor_tuple(cursors[lane])
    equal = cursors["producer"] == cursors["checker"] == cursors["agreed"]
    require(cursors.get("exact_equal") is equal,
            "STATE_STOP false cursor equality flag")

    last_k = 2
    open_seen = False
    for row in state["enumeration"]["k_ledger"]:
        k = row.get("k")
        require(isinstance(k, int) and k > last_k, "STATE_STOP duplicate/gapped-order k ledger")
        last_k = k
        if row.get("k_closed"):
            require(not open_seen and row.get("status") == "CLOSED" and
                    row.get("enumerator_complete") is True and
                    row.get("producer_checker_agree") is True and
                    row.get("remaining_items") == 0 and
                    is_sha(row.get("completeness_receipt_sha256")),
                    "STATE_STOP false or out-of-order k_closed")
        else:
            open_seen = True

    if bind_current:
        integrity = state["integrity"]
        require(integrity["schema"]["path"] ==
                "search/d972_dovetail_state_schema_v1.json",
                "STATE_STOP schema path drift")
        require(SCHEMA_PATH.is_file() and
                sha_file(SCHEMA_PATH) == integrity["schema"]["sha256"],
                "STATE_STOP schema digest drift")
        input_rows: list[tuple[str, str]] = []
        for binding in integrity["inputs"]:
            path = ROOT / binding["path"]
            require(path.is_file() and sha_file(path) == binding["sha256"],
                    f"STATE_STOP input digest drift: {binding['path']}")
            input_rows.append((binding["path"], binding["sha256"]))
        require(binding_set_digest(input_rows) == integrity["input_set_sha256"],
                "STATE_STOP input-set digest mismatch")
        if integrity["ready"]:
            code_rows: list[tuple[str, str]] = []
            for binding in integrity["code"].values():
                path = ROOT / binding["path"]
                require(path.is_file(), f"STATE_STOP required code missing: {binding['path']}")
                observed = sha_file(path)
                require(observed == binding["sha256"],
                        f"STATE_STOP code digest drift: {binding['path']}")
                code_rows.append((binding["path"], observed))
            require(binding_set_digest(code_rows) == integrity["code_set_sha256"],
                    "STATE_STOP code-set digest mismatch")
            runtime = state["receipts"].get("runtime_integrity", {})
            require(runtime.get("manifest_sha256") == sha_file(MANIFEST_PATH),
                    "STATE_STOP manifest digest drift")


def validate_transition(previous: dict[str, Any], current: dict[str, Any]) -> None:
    require(current["hash_chain"]["sequence"] == previous["hash_chain"]["sequence"] + 1,
            "STATE_STOP sequence gap")
    require(current["hash_chain"]["parent_checkpoint_sha256"] ==
            previous["hash_chain"]["checkpoint_sha256"],
            "STATE_STOP parent hash mismatch")
    require(cursor_tuple(current["cursors"]["agreed"]) >=
            cursor_tuple(previous["cursors"]["agreed"]),
            "STATE_STOP agreed cursor regression")


def _current_run_metadata() -> dict[str, Any]:
    """Return provenance for a newly sealed checker transition only."""
    run_id = os.environ.get("CURRENT_RUN_ID", "").strip()
    if not run_id:
        return {
            "run_id": f"local-{time.time_ns()}",
            "run_attempt": 0,
            "event": "local_seed",
            "commit_sha": None,
            "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "resume_run_id": None,
        }
    attempt_raw = os.environ.get("CURRENT_RUN_ATTEMPT", "")
    event = os.environ.get("CURRENT_EVENT", "")
    commit = os.environ.get("CURRENT_COMMIT", "").lower()
    source = os.environ.get("SOURCE_RUN_ID", "").strip() or None
    if not attempt_raw.isdigit() or event not in {"workflow_dispatch", "schedule"}:
        raise CheckStop("STATE_STOP malformed current workflow run metadata")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise CheckStop("STATE_STOP malformed current workflow commit")
    if source is not None and not re.fullmatch(r"[1-9][0-9]*", source):
        raise CheckStop("STATE_STOP malformed source workflow run id")
    return {
        "run_id": run_id,
        "run_attempt": int(attempt_raw),
        "event": event,
        "commit_sha": commit,
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "resume_run_id": source,
    }


def transition(old: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    new = copy.deepcopy(old)
    for key, value in updates.items():
        new[key] = value
    new["run"] = _current_run_metadata()
    new["hash_chain"]["sequence"] = old["hash_chain"]["sequence"] + 1
    new["hash_chain"]["parent_checkpoint_sha256"] = old["hash_chain"]["checkpoint_sha256"]
    new["hash_chain"]["checkpoint_sha256"] = ZERO_SHA
    new["hash_chain"]["checkpoint_sha256"] = checkpoint_hash(new)
    validate_transition(old, new)
    return new


def serialize_a_tuple(row: Any) -> str:
    require(isinstance(row, list) and len(row) == 3 and isinstance(row[0], int),
            "TARGET_STOP malformed source-map-A tuple")
    require(isinstance(row[1], list) and len(row[1]) == 3 and
            all(isinstance(pair, list) and len(pair) == 2 for pair in row[1]),
            "TARGET_STOP malformed source-map-A can9 tuple")
    require(isinstance(row[2], list) and len(row[2]) == 9,
            "TARGET_STOP malformed source-map-A PSL tuple")
    can9 = [int(x) for pair in row[1] for x in pair]
    psl = [int(x) for x in row[2]]
    return f"({row[0]};{','.join(map(str, can9))};{','.join(map(str, psl))})"


def canonical_target_keys() -> list[str]:
    a_doc = json.loads(TARGET_A.read_text(encoding="utf-8"))
    b_doc = json.loads(TARGET_B.read_text(encoding="utf-8"))
    a_keys = [serialize_a_tuple(row) for row in a_doc.get("tuples", [])]
    b_keys = b_doc.get("tuples")
    require(isinstance(b_keys, list) and all(isinstance(x, str) for x in b_keys),
            "TARGET_STOP malformed source-map-B tuples")
    require(len(a_keys) == len(set(a_keys)) == 972 and
            len(b_keys) == len(set(b_keys)) == 972,
            "TARGET_STOP missing or duplicate canonical keys")
    require(set(a_keys) == set(b_keys), "TARGET_STOP source-map A/B set disagreement")
    return sorted(a_keys)


def parse_jsonl(path: Path) -> list[dict[str, Any]]:
    require(path.is_file(), f"STATE_STOP ledger missing: {path}")
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise CheckStop(f"STATE_STOP malformed ledger line {number}: {exc}") from exc
        require(isinstance(row, dict), f"STATE_STOP non-object ledger line {number}")
        rows.append(row)
    return rows


def validate_group_table(table: Any) -> int:
    require(isinstance(table, list) and table, "WITNESS_STOP empty kernel table")
    n = len(table)
    universe = list(range(n))
    require(all(isinstance(row, list) and len(row) == n for row in table),
            "WITNESS_STOP nonsquare kernel table")
    require(table[0] == universe and [row[0] for row in table] == universe,
            "WITNESS_STOP kernel identity label is not zero")
    require(all(sorted(row) == universe for row in table),
            "WITNESS_STOP kernel table row is not Latin")
    require(all(sorted(table[a][b] for a in universe) == universe for b in universe),
            "WITNESS_STOP kernel table column is not Latin")
    for a in universe:
        for b in universe:
            for c in universe:
                require(table[table[a][b]][c] == table[a][table[b][c]],
                        "WITNESS_STOP kernel table is nonassociative")
    return n


def validate_automorphism(table: list[list[int]], label: Any) -> None:
    n = len(table)
    require(isinstance(label, list) and sorted(label) == list(range(n)) and label[0] == 0,
            "WITNESS_STOP malformed kernel automorphism label")
    for a in range(n):
        for b in range(n):
            require(label[table[a][b]] == table[label[a]][label[b]],
                    "WITNESS_STOP label is not a kernel automorphism")


def validate_signed_words(words: Any, generator_count: int, name: str) -> None:
    require(isinstance(words, list), f"WITNESS_STOP {name} is not a list")
    for row in words:
        require(isinstance(row, list) and all(
            isinstance(x, int) and x != 0 and abs(x) <= generator_count for x in row
        ), f"WITNESS_STOP malformed signed word in {name}")


def freely_reduce(word: Iterable[int]) -> list[int]:
    """Return the canonical freely reduced signed-generator word."""
    reduced: list[int] = []
    for letter in word:
        if reduced and reduced[-1] == -letter:
            reduced.pop()
        else:
            reduced.append(letter)
    return reduced


def expected_extension_relators(candidate: dict[str, Any]) -> list[list[int]]:
    """Rebuild the serialized presentation without producer/worker helpers.

    Generator labels 1..k-1 are the nonidentity elements of the labelled
    kernel Cayley table; labels k,k+1 are the two fixed quotient lifts.
    This is the lossless presentation convention claimed by each candidate.
    """
    table = candidate["kernel_table"]
    k = candidate["k"]
    automorphisms = candidate["automorphism_labels"]
    defects = candidate["defects"]
    q_relators = candidate["cell"]["q_relators"]

    def h(label: int) -> list[int]:
        return [] if label == 0 else [label]

    def h_inverse(label: int) -> list[int]:
        return [] if label == 0 else [-label]

    relators: list[list[int]] = []
    for a in range(k):
        for b in range(k):
            relators.append(freely_reduce(
                h(a) + h(b) + h_inverse(table[a][b])
            ))
    for j, automorphism in enumerate(automorphisms):
        lift_generator = k + j
        for a in range(k):
            relators.append(freely_reduce(
                [lift_generator] + h(a) + [-lift_generator] +
                h_inverse(automorphism[a])
            ))
    for q_word, defect in zip(q_relators, defects, strict=True):
        lifted = [
            (k - 1 + abs(letter)) * (1 if letter > 0 else -1)
            for letter in q_word
        ]
        relators.append(freely_reduce(lifted + h_inverse(defect)))
    return relators


def _gap_word_lists(words: list[list[int]]) -> str:
    return json.dumps(words, separators=(",", ":"))


def select_gap_command(
    script_path: Path,
    *,
    platform_name: str | None = None,
    finder: Any = shutil.which,
) -> tuple[list[str], str]:
    """Select the repository wrapper on Windows and the installed CLI on POSIX."""
    platform_name = os.name if platform_name is None else platform_name
    if platform_name == "nt":
        wrapper = ROOT / "gap.ps1"
        require(wrapper.is_file(),
                "STATE_STOP full-P reconstruction UNKNOWN: gap.ps1 is absent")
        powershell = finder("powershell.exe") or finder("powershell")
        require(powershell is not None,
                "STATE_STOP full-P reconstruction UNKNOWN: PowerShell is absent")
        return ([
            powershell, "-NoProfile", "-ExecutionPolicy", "Bypass",
            "-File", str(wrapper), str(script_path),
        ], "windows-gap.ps1")
    gap = finder("gap")
    require(gap is not None,
            "STATE_STOP full-P reconstruction UNKNOWN: GAP CLI is absent")
    return ([gap, "-q", "--quitonbreak", str(script_path)], "posix-gap-cli")


def run_isolated_gap(script: str, purpose: str) -> tuple[str, str, str]:
    """Run one generated ASCII GAP program and remove it unconditionally."""
    timeout = int(os.environ.get("D972_CHECKER_GAP_TIMEOUT", "3600"))
    temp_handle = tempfile.NamedTemporaryFile(
        mode="w", encoding="ascii", newline="\n", prefix="d972-independent-",
        suffix=".g", delete=False,
    )
    script_path = Path(temp_handle.name)
    try:
        with temp_handle:
            temp_handle.write(script)
            temp_handle.flush()
            os.fsync(temp_handle.fileno())
        command, command_mode = select_gap_command(script_path)
        try:
            completed = subprocess.run(
                command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=timeout, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise CheckStop(
                f"STATE_STOP independent {purpose} UNKNOWN: {type(exc).__name__}"
            ) from exc
    finally:
        try:
            script_path.unlink()
        except FileNotFoundError:
            pass
    require(completed.returncode == 0,
            f"STATE_STOP independent {purpose} UNKNOWN: GAP failed with exit "
            f"{completed.returncode}")
    return completed.stdout, completed.stderr, command_mode


def independent_gap_reconstruction(
    candidate: dict[str, Any], target_keys: list[str]
) -> dict[str, Any]:
    """Independently rebuild P and rerun the complete shadow/fiber loop.

    The generated GAP program never reads the campaign worker or producer.  It
    reconstructs the finite presentation, marked factor map, canonical D972
    permutation marking, literal equations (3.3)/(3.4), surjectivity, and two
    synchronized finite settlement tests.  A missing backend or any incomplete
    receipt is UNKNOWN and fail-closed.
    """
    k = candidate["k"]
    generator_count = candidate["fp_generator_count"]
    relators = candidate["fp_relators"]
    q_relators = candidate["cell"]["q_relators"]
    lifts = candidate["lift_labels"]
    factor = candidate["factor_images"]
    shadow = candidate["shadow_receipt"]
    source_words = [row["f_word"] for row in shadow["source_rows"]]
    factor_expr = ",".join(
        "One(Q)" if label == 0 else f"qg[{label}]" for label in factor
    )
    target_expr = json.dumps(
        target_keys, ensure_ascii=True, separators=(",", ":")
    )
    script = f"""\
MakeRels := function(F, rows)
  local g, out, row, w, x;
  g := GeneratorsOfGroup(F); out := [];
  for row in rows do
    w := One(F);
    for x in row do
      if x > 0 then w := w * g[x]; else w := w * g[-x]^-1; fi;
    od;
    Add(out, w);
  od;
  return out;
end;;
EvalSigned := function(g, row)
  local w, x;
  ## row is a serialized GAP ExtRep word, not a paper-notation product.
  ## Consequently its signed letters are evaluated in stored GAP order.
  w := One(Group(g));
  for x in row do
    if x > 0 then w := w * g[x]; else w := w * g[-x]^-1; fi;
  od;
  return w;
end;;
## Independent W-1/W-4 adapter: a paper product A1...An is the
## reversed GAP product An*...*A1.  This checker-local helper deliberately
## does not import or call the worker's AbstractProd implementation.
PaperProd := function(xs)
  local v, i;
  if Length(xs)=0 then Error("PaperProd needs a nonempty paper word"); fi;
  v:=xs[1]^0;
  for i in [Length(xs),Length(xs)-1..1] do v:=v*xs[i]; od;
  return v;
end;;
## Checker-local realization of the fixed six-coset B3 marking.  The block
## transitions and right multipliers are the twelve defining rules themselves;
## no producer, worker, or repository GAP helper is loaded.
CheckerQT := function(Q,x,y,c)
  local elts,pos,posOf,n,one,xi,yi,to1,to2,mul1,mul2,a1,a2,t,i,d;
  elts:=Elements(Q); n:=Length(elts); one:=One(Q); xi:=x^-1; yi:=y^-1;
  pos:=NewDictionary(elts[1],true);
  for i in [1..n] do AddDictionary(pos,elts[i],i); od;
  posOf:=v->LookupDictionary(pos,v);
  to1:=[2,1,5,6,3,4];
  to2:=[3,4,1,2,6,5];
  mul1:=[one,x,one,one,xi*yi*c,y];
  mul2:=[one,one,y,yi*xi*c,one,x];
  a1:=[]; a2:=[];
  for t in [1..6] do for i in [1..n] do
    d:=elts[i];
    a1[(t-1)*n+i]:=(to1[t]-1)*n+posOf(d*mul1[t]);
    a2[(t-1)*n+i]:=(to2[t]-1)*n+posOf(d*mul2[t]);
  od; od;
  return rec(s1:=PermList(a1),s2:=PermList(a2),elts:=elts,posOf:=posOf);
end;;
JoinStrings := function(xs, sep)
  local ans, i;
  if Length(xs)=0 then return ""; fi;
  ans:=xs[1];
  for i in [2..Length(xs)] do ans:=Concatenation(ans,sep,xs[i]); od;
  return ans;
end;;
ShiftPerm := function(p, offset, size)
  local images, j;
  images := [1..offset+size];
  for j in [1..size] do images[offset+j] := offset + (j^p); od;
  return PermList(images);
end;;
DirectSumPerm := function(p, psize, q, qsize)
  return p * ShiftPerm(q,psize,qsize);
end;;
BlockRestrict := function(p, offset, size)
  local images, j;
  images:=[];
  for j in [1..size] do images[j]:=(offset+j)^p-offset; od;
  if Set(images)<>[1..size] then Error("normal-form block failure"); fi;
  return PermList(images);
end;;
D9Coordinates := function(p)
  local r, s, a, e;
  r:=PermList([2,3,4,5,6,7,8,9,1]);
  s:=PermList([1,9,8,7,6,5,4,3,2]);
  for a in [0..8] do for e in [0..1] do
    if p=r^a*s^e then return [a,e]; fi;
  od; od;
  Error("D9 normal form failure");
end;;
TargetKey := function(m, p27, p9)
  local coords, i, oneLine;
  coords:=[];
  for i in [0..2] do
    Append(coords,D9Coordinates(BlockRestrict(p27,9*i,9)));
  od;
  oneLine:=List([1..9],i->i^p9);
  return Concatenation("(",String(m mod 18),";",
    JoinStrings(List(coords,String),","),";",
    JoinStrings(List(oneLine,String),","),")");
end;;

F := FreeGroup({generator_count}, "z");;
P := F / MakeRels(F, {_gap_word_lists(relators)});;
pg := GeneratorsOfGroup(P);;
FQ := FreeGroup(2, "r");;
Q := FQ / MakeRels(FQ, {_gap_word_lists(q_relators)});;
qg := GeneratorsOfGroup(Q);;
rho := GroupHomomorphismByImages(P, Q, pg, [{factor_expr}]);;
rhoOK := rho <> fail and IsSurjective(rho);;
if rhoOK then kerSize := Size(Kernel(rho)); else kerSize := -1; fi;;
h := Concatenation([One(P)], pg{{[1..{k - 1}]}});;
s1 := h[{lifts[0] + 1}] * pg[{k}];;
s2 := h[{lifts[1] + 1}] * pg[{k + 1}];;
pSize := Size(P);; qSize := Size(Q);;
braidOK := s1*s2*s1 = s2*s1*s2;;
generatedSize := Size(Group(s1,s2));;
markedOK := rhoOK and Image(rho,s1)=qg[1] and Image(rho,s2)=qg[2];;

## Frozen fixed-base generators, stored losslessly as one-line permutations.
## These are the K9 degree-27 and PSL(2,8) degree-9 markings allowed by task
## section 5; rebuilding below uses only GAP builtins and CheckerQT.
x9 := PermList([2,3,4,5,6,7,8,9,1,10,18,17,16,15,14,13,12,11,19,27,26,25,24,23,22,21,20]);;
y9 := PermList([2,1,9,8,7,6,5,4,3,11,12,13,14,15,16,17,18,10,20,19,27,26,25,24,23,22,21]);;
G9 := Group(x9,y9);;
x4 := PermList([8,5,2,1,9,7,4,3,6]);;
y4 := PermList([2,6,7,5,8,4,1,9,3]);;
P4 := Group(x4,y4);;
if Size(G9)<>2916 or Size(P4)<>504 then
  Error("checker-local fixed-base pure marking drift");
fi;
qt9 := CheckerQT(G9,x9,y9,());;
qt4 := CheckerQT(P4,x4,y4,());;
off9 := 6*Size(G9);; size4 := 6*Size(P4);;
bs1 := DirectSumPerm(qt9.s1,off9,qt4.s1,size4);;
bs2 := DirectSumPerm(qt9.s2,off9,qt4.s2,size4);;
BQ := Group(bs1,bs2);;
qToBase := GroupHomomorphismByImages(Q,BQ,qg,[bs1,bs2]);;
if qToBase=fail or not IsBijective(qToBase) then
  Error("canonical D972 marked quotient reconstruction failed");
fi;

isoP := IsomorphismPermGroup(P);; PP := Image(isoP);;
s1p := Image(isoP,s1);; s2p := Image(isoP,s2);;
rhoPerm := GroupHomomorphismByImages(PP,Q,[s1p,s2p],qg);;
if rhoPerm=fail or not IsSurjective(rhoPerm) or Size(Kernel(rhoPerm))<>{k} then
  Error("permutation factor reconstruction failed");
fi;
x := s1p^2;; y := s2p^2;; c := PaperProd([s1p,s2p,s1p])^2;;
D := DerivedSubgroup(Group(x,y));; fElts := Elements(D);;
Nord := Lcm(Order(x),Order(y),Order(c));;
charming := Filtered([0..Nord-1],m->Gcd(2*m+1,Nord)=1);;
targetKeys := {target_expr};;
sourceWords := {_gap_word_lists(source_words)};;
h33Count:=0;; h34Count:=0;; hexCount:=0;; shadowCount:=0;;
settledCount:=0;; unsettledCount:=0;; syncErrors:=0;;
for m in charming do
  u:=2*m+1;
  for fpos in [1..Length(fElts)] do
    f:=fElts[fpos];
    h33 := PaperProd([s1p^u,f^-1,s2p^u,f]) =
      PaperProd([f^-1,s1p,s2p,x^(-m),c^m]);
    h34 := PaperProd([f^-1,s2p^u,f,s1p^u]) =
      PaperProd([s2p,s1p,y^(-m),c^m,f]);
    if h33 then h33Count:=h33Count+1; fi;
    if h34 then h34Count:=h34Count+1; fi;
    if h33 and h34 then
      hexCount:=hexCount+1;
      img1:=s1p^u;; img2:=PaperProd([f^-1,s2p^u,f]);;
      surj:=Size(Group(img1,img2))=pSize;
      if surj then
        shadowCount:=shadowCount+1;
        hom:=GroupHomomorphismByImages(PP,PP,[s1p,s2p],[img1,img2]);
        if hom=fail then
          settledCayley:=false;; settledSchreier:=false;
        else
          settledCayley:=Size(Image(hom))=pSize;
          settledSchreier:=Index(PP,Image(hom))=1;
        fi;
        if settledCayley<>settledSchreier then syncErrors:=syncErrors+1; fi;
        settled:=settledCayley and settledSchreier;
        if settled then settledCount:=settledCount+1;
        else unsettledCount:=unsettledCount+1; fi;
        qf:=Image(rhoPerm,f);; qp:=Image(qToBase,qf);;
        i9:=qt9.posOf(One(G9))^qp;
        i4:=(off9+qt4.posOf(One(P4)))^qp-off9;
        if i9<1 or i9>Length(qt9.elts) or i4<1 or i4>Length(qt4.elts) then
          Error("canonical pure-block reduction failed");
        fi;
        key:=TargetKey(m,qt9.elts[i9],qt4.elts[i4]);;
        keyPos:=Position(targetKeys,key);
        if keyPos=fail then Error("independent target key is outside frozen set"); fi;
        Print("D972_ENUM ",m," ",fpos-1," ",keyPos-1," ",settled,"\\n");
      fi;
    fi;
  od;
od;
for i in [1..Length(sourceWords)] do
  sf:=Image(isoP,EvalSigned(pg,sourceWords[i]));;
  spos:=Position(fElts,sf);
  if spos=fail then spos:=-1; else spos:=spos-1; fi;
  Print("D972_SOURCE ",i-1," ",spos,"\\n");
od;
Print("D972_INDEPENDENT ",pSize," ",qSize," ",kerSize," ",
  generatedSize," ",braidOK," ",rhoOK," ",markedOK," ",Nord," ",
  Size(D)," ",Length(charming)," ",Length(charming)*Size(D)," ",
  h33Count," ",h34Count," ",hexCount," ",shadowCount," ",
  settledCount," ",unsettledCount," ",syncErrors," ",c=One(PP),"\\n");
QUIT_GAP(0);
"""
    stdout, stderr, command_mode = run_isolated_gap(script, "shadow reconstruction")
    summaries = [
        line.split() for line in stdout.splitlines()
        if line.startswith("D972_INDEPENDENT ")
    ]
    require(len(summaries) == 1 and len(summaries[0]) == 20,
            "STATE_STOP independent shadow reconstruction UNKNOWN: receipt marker absent")
    parts = summaries[0]
    p_order, q_order, kernel_order, generated_order = map(int, parts[1:5])
    braid_ok, rho_ok, marked_ok = [x == "true" for x in parts[5:8]]
    (
        n_ord, derived_order, charming_count, pair_universe,
        h33_count, h34_count, hex_count, shadow_count,
        settled_count, unsettled_count, sync_errors,
    ) = map(int, parts[8:19])
    c_in_l = parts[19] == "true"

    enum_rows: list[tuple[int, int, int, bool]] = []
    source_positions: dict[int, int] = {}
    for line in stdout.splitlines():
        enum_match = re.fullmatch(
            r"D972_ENUM (\d+) (\d+) (\d+) (true|false)", line
        )
        if enum_match:
            m, dpos, target_index = map(int, enum_match.groups()[:3])
            enum_rows.append((m, dpos, target_index, enum_match.group(4) == "true"))
        source_match = re.fullmatch(r"D972_SOURCE (\d+) (-?\d+)", line)
        if source_match:
            index, dpos = map(int, source_match.groups())
            require(index not in source_positions,
                    "STATE_STOP duplicate independent source-position row")
            source_positions[index] = dpos
    source_rows = shadow["source_rows"]
    require(set(source_positions) == set(range(len(source_rows))) and
            all(position >= 0 for position in source_positions.values()),
            "STATE_STOP independent source-word decoding incomplete")
    producer_canonical = [
        (row["m"], source_positions[index], row["target_index"], row["settled"])
        for index, row in enumerate(source_rows)
    ]
    require_disagreement(
        len(enum_rows) == len(set(enum_rows)) == shadow_count and
        sorted(enum_rows) == sorted(producer_canonical),
        "independent charming/full-hexagon/source-kernel loop disagrees",
    )

    independent_counts = [0] * 972
    for _, _, target_index, _ in enum_rows:
        independent_counts[target_index] += 1
    zero_indices = [i for i, count in enumerate(independent_counts) if count == 0]
    zero_keys = [target_keys[i] for i in zero_indices]
    source_material = "\n".join(
        f"{m}:{dpos}:{target}:{str(settled).lower()}"
        for m, dpos, target, settled in sorted(enum_rows)
    ) + "\n"
    require_disagreement(
        p_order == k * QBAR_ORDER and q_order == QBAR_ORDER and
        kernel_order == k and generated_order == p_order and braid_ok and
        rho_ok and marked_ok,
        "independent full-P order/factor/braid/marked-generation disagreement",
    )
    require_disagreement(
        n_ord == shadow["n_ord"] and derived_order == shadow["derived_subgroup_order"] and
        charming_count == shadow["charming_m_count"] and
        pair_universe == shadow["charming_pair_universe"] and
        h33_count == shadow.get("hexagon_3_3_pass_count") and
        h34_count == shadow.get("hexagon_3_4_pass_count") and
        hex_count == shadow["full_hexagon_pair_count"] and
        shadow_count == shadow["shadow_count"] and
        settled_count == shadow["settled_shadow_count"] and
        unsettled_count == shadow["unsettled_shadow_count"] and
        sync_errors == 0 and c_in_l is shadow["c_in_l"],
        "independent full-shadow counters/settlement disagreement",
    )
    require_disagreement(
        independent_counts == shadow["fiber_counts"] and
        zero_indices == shadow["zero_indices"] and zero_keys == shadow["zero_keys"],
        "independent normal-form fiber/zero set disagreement",
    )
    return {
        "backend": (
            "generated isolated GAP program; checker-local fixed-base permutations, "
            "six-coset rules, paper-product adapter, and normal form; no repository "
            "GAP helper, campaign producer, or worker read"
        ),
        "command_mode": command_mode,
        "script_sha256": sha_bytes(script.encode("ascii")),
        "stdout_sha256": sha_bytes(stdout.encode("utf-8")),
        "stderr_sha256": sha_bytes(stderr.encode("utf-8")),
        "p_order": p_order,
        "q_order": q_order,
        "kernel_order": kernel_order,
        "generated_order": generated_order,
        "braid": braid_ok,
        "factor_surjective": rho_ok,
        "marked_factor_images": marked_ok,
        "n_ord": n_ord,
        "derived_subgroup_order": derived_order,
        "charming_pair_universe": pair_universe,
        "hexagon_3_3_pass_count": h33_count,
        "hexagon_3_4_pass_count": h34_count,
        "full_hexagon_pair_count": hex_count,
        "shadow_count": shadow_count,
        "settled_shadow_count": settled_count,
        "unsettled_shadow_count": unsettled_count,
        "cayley_schreier_sync_errors": sync_errors,
        "c_in_l": c_in_l,
        "independent_source_rows": len(enum_rows),
        "independent_source_coordinate_sha256": sha_bytes(source_material.encode("ascii")),
        "independent_fiber_counts": independent_counts,
        "independent_zero_indices": zero_indices,
        "independent_zero_keys": zero_keys,
        "normal_form": "independent triple-D9 plus PSL(2,8) one-line marking",
        "classification": "FULL_P_AND_SHADOW_RECONSTRUCTED",
    }


def semantic_key(candidate: dict[str, Any]) -> str:
    material = {
        "k": candidate["k"],
        "kernel_table": candidate["kernel_table"],
        "fp_relators": candidate["fp_relators"],
        "lift_labels": candidate["lift_labels"],
        "factor_images": candidate["factor_images"],
    }
    return "d972:" + sha_bytes(canonical_bytes(material))


def verify_shadow_receipt(
    candidate: dict[str, Any],
    target_keys: list[str],
    *,
    expected_isolated: bool = True,
) -> dict[str, Any]:
    receipt = candidate.get("shadow_receipt")
    require_disagreement(isinstance(receipt, dict),
                         "candidate lacks attached independent shadow receipt")
    if receipt.get("status") == "INCONSISTENT_STOP":
        raise Inconsistent("producer shadow classifier returned INCONSISTENT_STOP")
    require_disagreement(receipt.get("schema") == "d972_dovetail_worker/v1" and
                         receipt.get("mode") == "shadow-fiber" and
                         receipt.get("status") == "PASS",
                         "shadow receipt schema/mode/status mismatch")
    truth_fields = (
        "runnable", "classification_terminal", "relative_extension_rebuilt",
        "factor_map_exact", "fp_permutation_isomorphism_exact",
        "full_hexagon_3_3_literal", "full_hexagon_3_4_literal",
        "shadow_surjectivity_exact",
    )
    require_disagreement(all(receipt.get(key) is True for key in truth_fields),
                         "RAW/incomplete shadow receipt")
    require_disagreement(receipt.get("extension_order") == candidate["order"] and
                         receipt.get("kernel_order") == candidate["kernel_order"],
                         "shadow receipt extension/kernel order mismatch")

    n_ord = receipt.get("n_ord")
    require_disagreement(isinstance(n_ord, int) and n_ord > 0 and
                         receipt.get("target_n_ord") == 18,
                         "noncanonical m modulus")
    expected_m = [m for m in range(n_ord) if math.gcd(2 * m + 1, n_ord) == 1]
    require_disagreement(receipt.get("charming_m") == expected_m and
                         receipt.get("charming_m_count") == len(expected_m),
                         "charming m universe mismatch")
    derived = receipt.get("derived_subgroup_order")
    require_disagreement(isinstance(derived, int) and derived > 0 and
                         receipt.get("charming_pair_universe") == len(expected_m) * derived,
                         "charming pair universe mismatch")
    pair_universe = receipt["charming_pair_universe"]
    hex_count = receipt.get("full_hexagon_pair_count")
    shadow_count = receipt.get("shadow_count")
    settled = receipt.get("settled_shadow_count")
    unsettled = receipt.get("unsettled_shadow_count")
    require_disagreement(all(isinstance(x, int) and x >= 0 for x in
                             (hex_count, shadow_count, settled, unsettled)) and
                         shadow_count <= hex_count <= pair_universe and
                         settled + unsettled == shadow_count,
                         "hexagon/shadow/settlement counts mismatch")
    isolated = unsettled == 0
    require_disagreement(receipt.get("isolated") is isolated and
                         receipt.get("all_shadows_settled") is isolated and
                         isolated is expected_isolated,
                         "isolated/nonisolated classification mismatch")
    require_disagreement(isinstance(receipt.get("source_kernel_method"), str) and
                         receipt["source_kernel_method"],
                         "source-kernel method absent")
    c_in_l = receipt.get("c_in_l")
    expected_mode = (
        "full_b3_literal_c_in_L" if c_in_l is True
        else "full_b3_literal_c_not_in_L_word_safe"
    )
    require_disagreement(c_in_l in (True, False) and
                         receipt.get("evaluation_mode") == expected_mode and
                         receipt.get("theta_tau_shortcut_used") is False,
                         "word-level/quotient-level evaluation mode mismatch")

    require_disagreement(receipt.get("target_count") == 972 and
                         receipt.get("target_key_count") == 972 and
                         len(target_keys) == len(set(target_keys)) == 972,
                         "target key cardinality mismatch")
    target_digest = sha_bytes(("\n".join(target_keys) + "\n").encode("utf-8"))
    require_disagreement(receipt.get("target_key_order_sha256") == target_digest,
                         "target key order digest mismatch")

    rows = receipt.get("source_rows")
    require_disagreement(isinstance(rows, list), "source_rows absent")
    counts = [0] * 972
    source_keys: list[str] = []
    source_maps: list[str] = []
    settled_from_rows = 0
    for row in rows:
        require_disagreement(isinstance(row, dict) and
                             set(row) == {"m", "u", "f_word", "target_index", "target_key", "settled"},
                             "malformed lossless source row")
        m = row["m"]
        require_disagreement(isinstance(m, int) and 0 <= m < n_ord and
                             m in expected_m and row["u"] == 2 * m + 1,
                             "m modulus/u mismatch")
        word = row["f_word"]
        require_disagreement(isinstance(word, list) and
                             all(isinstance(x, int) and x != 0 for x in word),
                             "malformed source f word")
        index = row["target_index"]
        require_disagreement(isinstance(index, int) and 0 <= index < 972 and
                             row["target_key"] == target_keys[index],
                             "fiber row target index/key mismatch")
        match = TARGET_M_RE.match(row["target_key"])
        require_disagreement(match is not None and int(match.group(1)) == m % 18,
                             "equation (3.60) m modulus mismatch")
        require_disagreement(isinstance(row["settled"], bool),
                             "source settlement bit is not Boolean")
        settled_from_rows += int(row["settled"])
        counts[index] += 1
        source_key = f"({m};{','.join(map(str, word))})"
        source_keys.append(source_key)
        source_maps.append(source_key + "=>" + row["target_key"])

    require_disagreement(len(source_keys) == len(set(source_keys)) and
                         receipt.get("source_key_count") == len(rows) == shadow_count,
                         "source-key collision/count mismatch")
    require_disagreement(settled_from_rows == settled and
                         len(rows) - settled_from_rows == unsettled,
                         "source-row settlement recount mismatch")
    source_digest = sha_bytes(("\n".join(sorted(source_keys)) + "\n").encode("utf-8"))
    source_map_digest = sha_bytes(("\n".join(sorted(source_maps)) + "\n").encode("utf-8"))
    require_disagreement(receipt.get("source_digest_sha256") == source_digest and
                         receipt.get("source_map_digest_sha256") == source_map_digest,
                         "source/source-map digest mismatch")
    require_disagreement(receipt.get("fiber_counts") == counts,
                         "fiber vector does not equal recomputed source rows")
    fiber_digest = sha_bytes((",".join(map(str, counts)) + "\n").encode("ascii"))
    require_disagreement(receipt.get("fiber_vector_sha256") == fiber_digest,
                         "fiber vector digest mismatch")

    zero_indices = [i for i, count in enumerate(counts) if count == 0]
    zero_keys = [target_keys[i] for i in zero_indices]
    positive = sorted(set(count for count in counts if count > 0))
    image_size = 972 - len(zero_indices)
    uniform = len(positive) == 1
    fiber_size = positive[0] if uniform else 0
    require_disagreement(receipt.get("zero_indices") == zero_indices and
                         receipt.get("zero_keys") == zero_keys and
                         receipt.get("first_empty_target_key") ==
                         (zero_keys[0] if zero_keys else None),
                         "zero fiber set mismatch")
    valid_isolated_image = image_size in (324, 972)
    require_disagreement(receipt.get("image_subgroup_order") == image_size and
                         receipt.get("image_subgroup_order_324_or_972") is
                         valid_isolated_image,
                         "image size flag/count mismatch")
    require_disagreement(receipt.get("fiber_uniform_on_image") is uniform and
                         receipt.get("fiber_size_on_image") == fiber_size and
                         (not uniform or shadow_count == image_size * fiber_size),
                         "fiber uniformity/cardinality mismatch")
    exact_fibers = isolated and uniform and valid_isolated_image and (
        shadow_count == image_size * fiber_size
    )
    campaign_stop = exact_fibers and image_size == 324 and bool(zero_keys)
    require_disagreement(receipt.get("equation_3_60_exact") is exact_fibers and
                         receipt.get("exact_972_fibers") is exact_fibers and
                         receipt.get("accept_for_ledger") is exact_fibers and
                         receipt.get("ready_for_producer_ledger") is exact_fibers and
                         candidate.get("ready_for_producer_ledger") is exact_fibers and
                         receipt.get("campaign_stop_first_empty_fiber") is campaign_stop,
                         "classification/ledger terminal flag mismatch")
    return {
        "candidate_id": candidate["candidate_id"],
        "semantic_key": candidate["semantic_key"],
        "k": candidate["k"],
        "isolated": isolated,
        "image_size": image_size,
        "fiber_size": fiber_size,
        "zero_keys": zero_keys,
        "first_zero_key": zero_keys[0] if zero_keys else None,
        "producer_digest": sha_bytes(canonical_bytes(candidate)),
        "checker_digest": sha_bytes(canonical_bytes({
            "source_digest": source_digest,
            "source_map_digest": source_map_digest,
            "fiber_digest": fiber_digest,
            "image_size": image_size,
            "zero_keys": zero_keys,
        })),
    }


def validate_extension_witness(candidate: dict[str, Any]) -> None:
    require_disagreement(isinstance(candidate.get("candidate_id"), str) and
                         isinstance(candidate.get("semantic_key"), str),
                         "candidate id/semantic key absent")
    k = candidate.get("k")
    require_disagreement(isinstance(k, int) and k >= 3,
                         "candidate k is outside the preregistered search")
    table = candidate.get("kernel_table")
    require_disagreement(validate_group_table(table) == k and
                         candidate.get("kernel_order") == k,
                         "kernel table/order mismatch")
    automorphisms = candidate.get("automorphism_labels")
    require_disagreement(isinstance(automorphisms, list) and len(automorphisms) == 2,
                         "two automorphism labels are required")
    for label in automorphisms:
        validate_automorphism(table, label)
    defects = candidate.get("defects")
    lift_labels = candidate.get("lift_labels")
    cell = candidate.get("cell")
    require_disagreement(isinstance(cell, dict) and cell.get("kernel_table") == table,
                         "lossless marked cell absent or kernel mismatch")
    q_relators = cell.get("q_relators")
    require_disagreement(isinstance(q_relators, list) and q_relators and
                         isinstance(defects, list) and len(defects) == len(q_relators) and
                         all(isinstance(x, int) and 0 <= x < k for x in defects),
                         "extension defect tuple mismatch")
    require_disagreement(isinstance(lift_labels, list) and len(lift_labels) == 2 and
                         all(isinstance(x, int) and 0 <= x < k for x in lift_labels),
                         "marked lift labels mismatch")
    generator_count = candidate.get("fp_generator_count")
    require_disagreement(isinstance(generator_count, int) and generator_count == k + 1,
                         "fp generator count mismatch")
    validate_signed_words(candidate.get("fp_relators"), generator_count, "fp_relators")
    validate_signed_words(q_relators, 2, "q_relators")
    require_disagreement(candidate.get("fp_relators") == expected_extension_relators(candidate),
                         "full extension relators do not reconstruct from the lossless cell")
    factor = candidate.get("factor_images")
    require_disagreement(factor == [0] * (k - 1) + [1, 2],
                         "factor map generator images mismatch")
    require_disagreement(candidate.get("order") == k * QBAR_ORDER and
                         candidate.get("braid") is True and
                         candidate.get("marked_generation") is True,
                         "order/braid/marked-generation gate failed")
    require_disagreement(candidate["semantic_key"] == semantic_key(candidate),
                         "semantic key mismatch")


def verify_candidate(
    candidate: dict[str, Any],
    target_keys: list[str],
    *,
    require_full_backend: bool = False,
    expected_isolated: bool = True,
) -> dict[str, Any]:
    validate_extension_witness(candidate)
    summary = verify_shadow_receipt(
        candidate, target_keys, expected_isolated=expected_isolated
    )
    if require_full_backend:
        backend = independent_gap_reconstruction(candidate, target_keys)
    else:
        backend = {
            "classification": "PARSE_ONLY_FIXTURE",
            "note": "self-test only; never eligible for a cross-checked campaign row",
        }
    fiber_digest = summary["checker_digest"]
    summary["fiber_checker_digest"] = fiber_digest
    summary["full_p_reconstruction"] = backend
    summary["checker_digest"] = sha_bytes(canonical_bytes({
        "fiber_checker_digest": fiber_digest,
        "full_p_reconstruction": backend,
    }))
    return summary


CLASSIFICATION_KEYS = {
    "schema", "record_index", "record_kind", "cursor", "cell", "cell_sha256",
    "semantic_key", "classification_status", "classification_terminal",
    "raw_extension", "shadow_receipt", "eligible_candidate_id",
    "canonical_representative_record_index", "canonical_semantic_key",
    "exact_duplicate_receipt", "parent_record_sha256", "record_sha256",
}


def classification_record_hash(row: dict[str, Any]) -> str:
    body = copy.deepcopy(row)
    body["record_sha256"] = ZERO_SHA
    return sha_bytes(canonical_bytes(body))


def classification_candidate(row: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(row["raw_extension"])
    isolated = row["classification_status"] == "ISOLATED_EXACT"
    candidate.update({
        "cell": copy.deepcopy(row["cell"]),
        "k": row["cursor"]["k"],
        "candidate_id": row["eligible_candidate_id"] or
                        f"CLASSIFICATION-{row['record_index']:08d}",
        "semantic_key": row["semantic_key"],
        "classification_status": (
            "SHADOW_FIBER_CLASSIFIED" if isolated else row["classification_status"]
        ),
        "ready_for_producer_ledger": isolated,
        "shadow_receipt": copy.deepcopy(row["shadow_receipt"]),
    })
    return candidate


def independent_marked_pair_isomorphism(
    left: dict[str, Any], right: dict[str, Any]
) -> dict[str, Any]:
    """Check an EXACT_DUPLICATE_LINK by rebuilding both marked fp groups."""
    require_disagreement(left["k"] == right["k"],
                         "duplicate link crosses kernel orders")
    k = left["k"]
    script = f"""\
MakeRels := function(F, rows)
  local g,out,row,w,x;
  g:=GeneratorsOfGroup(F); out:=[];
  for row in rows do
    w:=One(F);
    for x in row do
      if x>0 then w:=w*g[x]; else w:=w*g[-x]^-1; fi;
    od;
    Add(out,w);
  od;
  return out;
end;;
F1:=FreeGroup({left['fp_generator_count']},"a");;
P1:=F1/MakeRels(F1,{_gap_word_lists(left['fp_relators'])});;
g1:=GeneratorsOfGroup(P1);;
h1:=Concatenation([One(P1)],g1{{[1..{k - 1}]}});;
a1:=h1[{left['lift_labels'][0] + 1}]*g1[{k}];;
a2:=h1[{left['lift_labels'][1] + 1}]*g1[{k + 1}];;
F2:=FreeGroup({right['fp_generator_count']},"b");;
P2:=F2/MakeRels(F2,{_gap_word_lists(right['fp_relators'])});;
g2:=GeneratorsOfGroup(P2);;
h2:=Concatenation([One(P2)],g2{{[1..{k - 1}]}});;
b1:=h2[{right['lift_labels'][0] + 1}]*g2[{k}];;
b2:=h2[{right['lift_labels'][1] + 1}]*g2[{k + 1}];;
size1:=Size(P1);; size2:=Size(P2);;
gen1:=Size(Group(a1,a2));; gen2:=Size(Group(b1,b2));;
f:=GroupHomomorphismByImages(P1,P2,[a1,a2],[b1,b2]);;
g:=GroupHomomorphismByImages(P2,P1,[b1,b2],[a1,a2]);;
fok:=f<>fail and IsBijective(f);; gok:=g<>fail and IsBijective(g);;
Print("D972_PAIR_ISO ",size1," ",size2," ",gen1," ",gen2," ",
  fok," ",gok,"\\n");
QUIT_GAP(0);
"""
    stdout, stderr, command_mode = run_isolated_gap(script, "marked-pair isomorphism")
    match = re.search(
        r"^D972_PAIR_ISO (\d+) (\d+) (\d+) (\d+) (true|false) (true|false)$",
        stdout, re.MULTILINE,
    )
    require(match is not None,
            "STATE_STOP independent marked-pair isomorphism receipt absent")
    size1, size2, gen1, gen2 = map(int, match.groups()[:4])
    forward, reverse = [x == "true" for x in match.groups()[4:]]
    require_disagreement(
        size1 == size2 == gen1 == gen2 == k * QBAR_ORDER and forward and reverse,
        "independent marked-pair duplicate criterion disagrees",
    )
    return {
        "classification": "EXACT_MARKED_PAIR_DUPLICATE_RECONSTRUCTED",
        "command_mode": command_mode,
        "script_sha256": sha_bytes(script.encode("ascii")),
        "stdout_sha256": sha_bytes(stdout.encode("utf-8")),
        "stderr_sha256": sha_bytes(stderr.encode("utf-8")),
        "left_order": size1, "right_order": size2,
        "forward_bijective": forward, "reverse_bijective": reverse,
    }


def validate_classification_ledger(
    state: dict[str, Any],
    producer_ledger_path: Path,
    producer_rows: list[dict[str, Any]],
    target_keys: list[str],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Audit the complete representative/duplicate classification ledger."""
    require_disagreement(state["receipts"].get("classification_checker_required") is True,
                         "classification checker was not required by producer")
    binding = state["receipts"].get("classification_ledger")
    require_disagreement(isinstance(binding, dict),
                         "classification-ledger binding absent")
    path = producer_ledger_path.parent / "producer-classification-ledger.jsonl"
    require(path.is_file(), f"STATE_STOP classification ledger missing: {path}")
    require(binding.get("path") == path.name and
            binding.get("sha256") == sha_file(path),
            "STATE_STOP classification-ledger relative path/digest mismatch")
    rows = parse_jsonl(path)
    parent: str | None = None
    representative_count = 0
    duplicate_count = 0
    seen_cursors: set[tuple[int, ...]] = set()
    summaries: list[dict[str, Any]] = []
    representatives: dict[int, dict[str, Any]] = {}
    producer_by_id = {row.get("candidate_id"): row for row in producer_rows}
    eligible_ids: set[str] = set()
    for index, row in enumerate(rows):
        require(set(row) == CLASSIFICATION_KEYS and
                row.get("schema") == "d972-classification-ledger/v1" and
                row.get("record_index") == index and
                row.get("parent_record_sha256") == parent and
                is_sha(row.get("record_sha256")) and
                row["record_sha256"] == classification_record_hash(row),
                f"STATE_STOP classification row/hash-chain failure at {index}")
        parent = row["record_sha256"]
        cursor_key = cursor_tuple(row["cursor"])
        require(cursor_key not in seen_cursors,
                "STATE_STOP two classification rows claim one pre-advance cursor")
        seen_cursors.add(cursor_key)
        cell = row.get("cell")
        require(isinstance(cell, dict) and
                row.get("cell_sha256") == sha_bytes(canonical_bytes(cell)) and
                row["cursor"]["k"] >= 3 and
                row["cursor"]["outer_action"]["index"] == cell.get("aut_pair_index") and
                row["cursor"]["extension_class"]["index"] == cell.get("defect_index") and
                row["cursor"]["marked_orbit"]["index"] == cell.get("lift_pair_index"),
                "STATE_STOP classification cell/cursor binding mismatch")
        raw = row.get("raw_extension")
        require_disagreement(isinstance(raw, dict) and
                             raw.get("relative_extension_only") is True and
                             raw.get("ready_for_producer_ledger") is False,
                             "classification row lacks a raw extension")
        candidate = classification_candidate(row)
        require_disagreement(row.get("semantic_key") == semantic_key(candidate),
                             "classification semantic key mismatch")
        kind = row.get("record_kind")
        if kind == "REPRESENTATIVE":
            representative_count += 1
            isolated = row.get("classification_status") == "ISOLATED_EXACT"
            require_disagreement(row.get("classification_status") in
                                 {"ISOLATED_EXACT", "NONISOLATED"} and
                                 row.get("classification_terminal") is True and
                                 isinstance(row.get("shadow_receipt"), dict) and
                                 row.get("canonical_representative_record_index") == index and
                                 row.get("canonical_semantic_key") == row["semantic_key"] and
                                 row.get("exact_duplicate_receipt") is None and
                                 ((isinstance(row.get("eligible_candidate_id"), str)) is isolated),
                                 "malformed classification representative")
            summary = verify_candidate(
                candidate, target_keys, require_full_backend=True,
                expected_isolated=isolated,
            )
            summaries.append({
                "kind": "classification-representative", "record_index": index,
                "record_sha256": row["record_sha256"],
                "checker_digest": summary["checker_digest"],
                "classification_status": row["classification_status"],
            })
            representatives[index] = candidate
            if isolated:
                candidate_id = row["eligible_candidate_id"]
                eligible_ids.add(candidate_id)
                expected_producer = copy.deepcopy(raw)
                expected_producer.update({
                    "cell": copy.deepcopy(cell), "k": row["cursor"]["k"],
                    "candidate_id": candidate_id, "semantic_key": row["semantic_key"],
                    "classification_status": "SHADOW_FIBER_CLASSIFIED",
                    "ready_for_producer_ledger": True,
                    "shadow_receipt": copy.deepcopy(row["shadow_receipt"]),
                })
                require_disagreement(producer_by_id.get(candidate_id) == expected_producer,
                                     "isolated classification/producer-ledger mismatch")
        elif kind == "EXACT_DUPLICATE_LINK":
            duplicate_count += 1
            canonical_index = row.get("canonical_representative_record_index")
            prior = representatives.get(canonical_index)
            duplicate_receipt = row.get("exact_duplicate_receipt")
            require_disagreement(row.get("classification_status") == "EXACT_DUPLICATE" and
                                 row.get("classification_terminal") is True and
                                 row.get("shadow_receipt") is None and
                                 row.get("eligible_candidate_id") is None and
                                 isinstance(prior, dict) and
                                 row.get("canonical_semantic_key") ==
                                 rows[canonical_index]["canonical_semantic_key"] and
                                 isinstance(duplicate_receipt, dict) and
                                 duplicate_receipt.get("marked_over_base_isomorphic") is True and
                                 duplicate_receipt.get("left_cell_sha256") ==
                                 rows[canonical_index]["cell_sha256"] and
                                 duplicate_receipt.get("right_cell_sha256") == row["cell_sha256"],
                                 "malformed exact duplicate link")
            validate_extension_witness(candidate)
            pair_summary = independent_marked_pair_isomorphism(prior, candidate)
            summaries.append({
                "kind": "classification-duplicate", "record_index": index,
                "record_sha256": row["record_sha256"],
                "checker_digest": sha_bytes(canonical_bytes(pair_summary)),
            })
        else:
            raise CheckStop("STATE_STOP unknown classification record kind")
    require(binding.get("record_count") == len(rows) and
            binding.get("representative_count") == representative_count and
            binding.get("duplicate_link_count") == duplicate_count and
            binding.get("last_record_sha256") == parent and
            binding.get("through_cursor_sha256") ==
            sha_bytes(canonical_bytes(state["cursors"]["producer"])),
            "STATE_STOP classification-ledger binding totals/cursor mismatch")
    require_disagreement(eligible_ids == set(producer_by_id),
                         "classification ledger does not cover isolated producer candidates")
    audit = {
        "schema": "d972-classification-checker/v1",
        "classification_ledger_sha256": binding["sha256"],
        "checked_record_count": len(rows),
        "representative_count": representative_count,
        "duplicate_link_count": duplicate_count,
        "through_record_sha256": parent,
        "through_cursor_sha256": binding["through_cursor_sha256"],
        "summary_set_sha256": sha_bytes(canonical_bytes(summaries)),
        "full_independent_reconstruction": True,
    }
    audit["receipt_sha256"] = sha_bytes(canonical_bytes(audit))
    return audit, summaries


def calibration_observation(raw: Any) -> dict[str, Any]:
    keys = (
        "marked_orbit_count", "gt_orders", "image_sizes",
        "zero_fiber_counts", "fiber_histograms",
    )
    require_disagreement(isinstance(raw, dict) and all(key in raw for key in keys),
                         "calibration raw receipt is missing observed values")
    observed = {key: raw[key] for key in keys}
    observed["receipt_sha256"] = sha_bytes(canonical_bytes(observed))
    return observed


def independently_check_calibration(state: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    """Record worker observations but keep the gate shut without a second scan.

    The worker's planned lossless calibration witness was not frozen in time
    for this checker revision.  Rehashing its five metrics is not independent
    reproduction, so this routine deliberately cannot return PASSED.
    """
    gate = copy.deepcopy(state["calibration_gate"])
    raw = state.get("receipts", {}).get("producer_preflight", {}).get("worker", {}).get(
        "calibration"
    )
    require_disagreement(isinstance(raw, dict), "producer preflight calibration receipt absent")
    all_ok = True
    for case in gate["cases"]:
        observed = calibration_observation(raw.get(case["case_id"]))
        case["checker"] = observed
        expected = case["expected"]
        producer = case.get("producer")
        metrics = {key: observed[key] for key in expected}
        producer_metrics = (
            {key: producer.get(key) for key in expected} if isinstance(producer, dict) else None
        )
        # These comparisons are useful diagnostics only.  They are never an
        # independent calibration system and therefore carry no unlock power.
        case_ok = False
        if isinstance(producer, dict):
            producer_body = {key: producer[key] for key in expected}
            require_disagreement(
                producer.get("receipt_sha256") == sha_bytes(canonical_bytes(producer_body)),
                "producer calibration observation digest mismatch",
            )
        require_disagreement(metrics == expected and producer_metrics == expected,
                             "producer calibration values disagree with the frozen gate")
        case["agreed"] = case_ok
        all_ok = all_ok and case_ok
    gate["status"] = "PASSED" if all_ok else "FAILED"
    gate["search_unlocked"] = all_ok
    gate["producer_checker_agree"] = all_ok
    return gate, all_ok


def ledger_binding(path: Path, rows: list[dict[str, Any]], cursor: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": path.name,
        "sha256": sha_file(path) if path.is_file() else None,
        "record_count": len(rows),
        "through_cursor_sha256": sha_bytes(canonical_bytes(cursor)) if rows else None,
    }


def write_checked_state(
    state_path: Path,
    producer_ledger: Path,
    out_dir: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    old = json.loads(state_path.read_text(encoding="utf-8"))
    validate_state_core(old)
    claimed = old["ledgers"]["producer"]
    require(claimed.get("path") == producer_ledger.name or
            (claimed.get("path") is None and claimed.get("sha256") is None and
             claimed.get("record_count") == 0),
            "STATE_STOP producer ledger binding is not artifact-relative")
    if producer_ledger.is_file():
        producer_rows = parse_jsonl(producer_ledger)
        observed_producer_digest: str | None = (
            None if producer_ledger.stat().st_size == 0 and claimed["sha256"] is None
            else sha_file(producer_ledger)
        )
    else:
        require(old["status"]["code"] == "CALIBRATION_PENDING" and
                claimed["sha256"] is None and claimed["record_count"] == 0,
                f"STATE_STOP ledger missing: {producer_ledger}")
        producer_rows = []
        observed_producer_digest = None
    require(claimed["sha256"] == observed_producer_digest,
            "STATE_STOP producer ledger digest mismatch")
    require(claimed["record_count"] == len(producer_rows),
            "STATE_STOP producer ledger count mismatch")
    if claimed.get("path") == producer_ledger.name:
        require(claimed.get("through_cursor_sha256") ==
                sha_bytes(canonical_bytes(old["cursors"]["producer"])),
                "STATE_STOP producer ledger cursor binding mismatch")
    semantic_keys = [row.get("semantic_key") for row in producer_rows]
    require(all(isinstance(key, str) for key in semantic_keys) and
            len(semantic_keys) == len(set(semantic_keys)),
            "STATE_STOP duplicate/missing semantic key")
    ids = [row.get("candidate_id") for row in producer_rows]
    require(len(ids) == len(set(ids)), "STATE_STOP duplicate candidate id")
    for index, candidate_id in enumerate(ids):
        require(isinstance(candidate_id, str) and candidate_id.endswith(f"-{index:08d}"),
                "STATE_STOP candidate-id gap")

    checker_ledger = out_dir / "checker-ledger.jsonl"
    claimed_checker = old["ledgers"]["checker"]
    require(claimed_checker.get("path") in (None, checker_ledger.name),
            "STATE_STOP checker ledger binding is not artifact-relative")
    if checker_ledger.is_file():
        prior_checker_rows = parse_jsonl(checker_ledger)
        observed_checker_digest: str | None = (
            None if checker_ledger.stat().st_size == 0 and
                    claimed_checker.get("sha256") is None
            else sha_file(checker_ledger)
        )
    else:
        prior_checker_rows = []
        observed_checker_digest = None
    require(claimed_checker.get("sha256") == observed_checker_digest and
            claimed_checker.get("record_count") == len(prior_checker_rows),
            "STATE_STOP restored checker-ledger digest/count mismatch")
    require((not prior_checker_rows and
             claimed_checker.get("through_cursor_sha256") is None) or
            (bool(prior_checker_rows) and
             claimed_checker.get("through_cursor_sha256") ==
             sha_bytes(canonical_bytes(old["cursors"]["checker"]))),
            "STATE_STOP restored checker-ledger cursor binding mismatch")
    checker_rows: list[dict[str, Any]] = []
    receipts = copy.deepcopy(old["receipts"])
    cursors = copy.deepcopy(old["cursors"])
    enumeration = copy.deepcopy(old["enumeration"])
    ledgers = copy.deepcopy(old["ledgers"])
    terminal_witness = None

    if old["status"]["code"] == "CALIBRATION_PENDING":
        gate, passed = independently_check_calibration(old)
        receipts["independent_calibration_checker"] = {
            "status": "BLOCKED",
            "subcode": "INDEPENDENT_CALIBRATION_WITNESS_NOT_FROZEN",
            "reason": (
                "Worker observations were read from receipts, but a second lossless "
                "calibration construction/scan was unavailable; expected values were "
                "not promoted to observations."
            ),
            "search_unlock_authority": False,
        }
        checker_rows.append({
            "kind": "calibration",
            "passed": passed,
            "case_receipts": [case["checker"]["receipt_sha256"] for case in gate["cases"]],
        })
        cursors["checker"] = copy.deepcopy(cursors["producer"])
        cursors["agreed"] = copy.deepcopy(cursors["producer"])
        cursors["exact_equal"] = True
        cursors["agreement_receipt_sha256"] = sha_bytes(canonical_bytes({
            "cursor": cursors["agreed"], "calibration": checker_rows[-1],
        }))
        if passed:
            if not enumeration.get("complete_relative_extensions"):
                enumeration["engine_status"] = "BLOCKED"
                enumeration["complete_relative_extensions"] = False
                enumeration["engine_completeness_receipt_sha256"] = None
                status = {
                    "code": "BLOCKED_RELATIVE_EXTENSION_ENUMERATOR",
                    "terminal": True,
                    "resumable": False,
                    "reason": (
                        "Calibration passed, but no documented complete nonabelian relative-extension "
                        "enumerator/count receipt is present."
                    ),
                }
                state_kind = "TERMINAL"
            else:
                status = {
                    "code": "UNKNOWN/RESUME", "terminal": False, "resumable": True,
                    "reason": "Independent k=1,2 calibration passed; enumeration may resume.",
                }
                state_kind = "CHECKPOINT"
        else:
            status = {
                "code": "CALIBRATION_STOP", "terminal": True, "resumable": False,
                "reason": "Independent calibration disagreed with an observed producer value.",
            }
            state_kind = "TERMINAL"
        calibration_gate = gate
    else:
        calibration_gate = copy.deepcopy(old["calibration_gate"])
        require_disagreement(calibration_gate.get("status") == "PASSED" and
                             calibration_gate.get("search_unlocked") is True,
                             "candidate ledger reached checker before calibration passed")
        require_disagreement(enumeration.get("engine_status") == "COMPLETE" and
                             enumeration.get("complete_relative_extensions") is True and
                             is_sha(enumeration.get("engine_completeness_receipt_sha256")),
                             "candidate ledger lacks a complete relative-extension receipt")
        target_keys = canonical_target_keys()
        classification_audit, classification_summaries = validate_classification_ledger(
            old, producer_ledger, producer_rows, target_keys
        )
        receipts["classification_checker"] = classification_audit
        checker_rows.extend(classification_summaries)
        summaries: list[dict[str, Any]] = []
        for row in producer_rows:
            summary = verify_candidate(row, target_keys, require_full_backend=True)
            summaries.append(summary)
            checker_rows.append({"kind": "candidate", **summary})
            if summary["image_size"] == 324 and summary["zero_keys"]:
                terminal_witness = {
                    "candidate_id": summary["candidate_id"],
                    "k": summary["k"],
                    "marked_extension_witness_sha256": summary["producer_digest"],
                    "isolated": True,
                    "target_key_count": 972,
                    "image_size": 324,
                    "first_zero_key": summary["first_zero_key"],
                    "zero_keys": summary["zero_keys"],
                    "producer_digest": summary["producer_digest"],
                    "checker_digest": summary["checker_digest"],
                    "checkpoint_parent_sha256": old["hash_chain"]["checkpoint_sha256"],
                }
                break
        checked_keys = [row["semantic_key"] for row in summaries]
        expected_set_digest = (
            sha_bytes(("\n".join(sorted(checked_keys)) + "\n").encode("utf-8"))
            if checked_keys else None
        )
        require_disagreement(enumeration.get("semantic_key_count") == len(producer_rows) and
                             enumeration.get("semantic_key_set_sha256") == expected_set_digest,
                             "semantic key count/set digest disagreement")
        cursors["checker"] = copy.deepcopy(cursors["producer"])
        cursors["agreed"] = copy.deepcopy(cursors["producer"])
        cursors["exact_equal"] = True
        cursors["agreement_receipt_sha256"] = sha_bytes(canonical_bytes({
            "producer_cursor": cursors["producer"],
            "semantic_keys": checked_keys,
            "checker_digests": [row["checker_digest"] for row in summaries],
        }))
        pending = receipts.get("pending_k_closure")
        if isinstance(pending, dict):
            require_disagreement(pending.get("all_stages_exhausted") is True and
                                 pending.get("k") == cursors["producer"]["k"] and
                                 pending.get("receipt_sha256") ==
                                 sha_bytes(canonical_bytes(pending.get("radices"))),
                                 "k-closure exhaustion receipt mismatch")
            binding = receipts.get("classification_ledger", {})
            require_disagreement(
                classification_audit["checked_record_count"] == binding.get("record_count") and
                classification_audit["through_record_sha256"] ==
                binding.get("last_record_sha256") and
                classification_audit["through_cursor_sha256"] ==
                sha_bytes(canonical_bytes(cursors["producer"])),
                "k-closure lacks complete classification-ledger agreement",
            )
            row = next((x for x in enumeration["k_ledger"] if x["k"] == pending["k"]), None)
            require_disagreement(row is not None and row["k_closed"] is False,
                                 "missing/open k ledger row")
            closure_receipt = sha_bytes(canonical_bytes({
                "pending": pending,
                "cursor": cursors["agreed"],
                "semantic_key_set_sha256": expected_set_digest,
                "classification_checker_receipt_sha256":
                    classification_audit["receipt_sha256"],
            }))
            row.update({
                "status": "CLOSED", "k_closed": True, "enumerator_complete": True,
                "producer_checker_agree": True, "remaining_items": 0,
                "completeness_receipt_sha256": closure_receipt,
            })
        if terminal_witness is not None:
            status = {
                "code": "A_WITNESS_CROSSCHECKED", "terminal": True, "resumable": False,
                "reason": "Independent checker confirmed the first isolated empty fiber.",
            }
            state_kind = "TERMINAL"
        else:
            status = {
                "code": "CONTINUE", "terminal": False, "resumable": True,
                "reason": "All producer rows were independently checked; no empty fiber was found.",
            }
            state_kind = "CHECKPOINT"

    all_checker_rows = prior_checker_rows + checker_rows
    atomic_text(checker_ledger, "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for row in all_checker_rows
    ))
    ledgers["checker"] = ledger_binding(checker_ledger, all_checker_rows, cursors["checker"])
    receipts["checker_summary"] = {
        "input_checkpoint_sha256": old["hash_chain"]["checkpoint_sha256"],
        "producer_ledger_sha256": observed_producer_digest,
        "checked_rows_this_run": len(checker_rows),
        "checked_rows_total": len(all_checker_rows),
        "helper_independence": (
            "Python checker imports no producer/worker code; every campaign candidate also "
            "passes a generated self-contained GAP reconstruction with checker-local "
            "fixed-base primitives that reads no repository GAP helper"
        ),
    }
    new = transition(old, {
        "state_kind": state_kind,
        "status": status,
        "calibration_gate": calibration_gate,
        "cursors": cursors,
        "enumeration": enumeration,
        "ledgers": ledgers,
        "terminal_witness": terminal_witness,
        "receipts": receipts,
    })
    atomic_json(state_path, new)
    return new, checker_rows


def terminalize(
    old: dict[str, Any], code: str, reason: str,
    *, ledgers: dict[str, Any] | None = None,
    receipts: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cursors = copy.deepcopy(old["cursors"])
    if code == "DISAGREE_STOP":
        cursors["exact_equal"] = False
        cursors["agreement_receipt_sha256"] = None
    updates: dict[str, Any] = {
        "state_kind": "TERMINAL",
        "status": {"code": code, "terminal": True, "resumable": False, "reason": reason},
        "cursors": cursors,
        "terminal_witness": None,
    }
    if ledgers is not None:
        updates["ledgers"] = ledgers
    if receipts is not None:
        updates["receipts"] = receipts
    new = transition(old, updates)
    return new


def binary_word(index: int) -> list[int]:
    bits = bin(index + 1)[2:]
    return [1 if bit == "1" else -1 for bit in bits]


def synthetic_candidate(target_keys: list[str]) -> dict[str, Any]:
    k = 3
    table = [[0, 1, 2], [1, 2, 0], [2, 0, 1]]
    rows = [
        {
            "m": int(TARGET_M_RE.match(key).group(1)),
            "u": 2 * int(TARGET_M_RE.match(key).group(1)) + 1,
            "f_word": binary_word(i),
            "target_index": i,
            "target_key": key,
            "settled": True,
        }
        for i, key in enumerate(target_keys)
    ]
    source_keys = [f"({row['m']};{','.join(map(str, row['f_word']))})" for row in rows]
    source_maps = [source_keys[i] + "=>" + rows[i]["target_key"] for i in range(972)]
    counts = [1] * 972
    receipt = {
        "schema": "d972_dovetail_worker/v1", "mode": "shadow-fiber", "status": "PASS",
        "runnable": True, "classification_terminal": True, "accept_for_ledger": True,
        "ready_for_producer_ledger": True, "relative_extension_rebuilt": True,
        "extension_order": k * QBAR_ORDER, "kernel_order": k, "factor_map_exact": True,
        "fp_permutation_isomorphism_exact": True, "permutation_witness_degree": 1,
        "n_ord": 18, "target_n_ord": 18,
        "charming_m": [m for m in range(18) if math.gcd(2 * m + 1, 18) == 1],
        "charming_m_count": 12, "derived_subgroup_order": 81,
        "charming_pair_universe": 972, "full_hexagon_pair_count": 972,
        "shadow_count": 972, "settled_shadow_count": 972, "unsettled_shadow_count": 0,
        "isolated": True, "all_shadows_settled": True,
        "source_kernel_method": "synthetic exact bijective marked maps",
        "full_hexagon_3_3_literal": True, "full_hexagon_3_4_literal": True,
        "shadow_surjectivity_exact": True, "evaluation_mode": "full_b3_literal_c_not_in_L_word_safe",
        "c_in_l": False, "theta_tau_shortcut_used": False,
        "target_count": 972, "target_key_count": 972,
        "target_key_order_sha256": sha_bytes(("\n".join(target_keys) + "\n").encode()),
        "image_subgroup_order": 972, "image_subgroup_order_324_or_972": True,
        "fiber_uniform_on_image": True, "fiber_size_on_image": 1,
        "fiber_counts": counts,
        "fiber_vector_sha256": sha_bytes((",".join(map(str, counts)) + "\n").encode()),
        "zero_indices": [], "zero_keys": [], "first_empty_target_key": None,
        "campaign_stop_first_empty_fiber": False,
        "equation_3_60_exact": True, "exact_972_fibers": True,
        "source_key_count": 972,
        "source_digest_sha256": sha_bytes(("\n".join(sorted(source_keys)) + "\n").encode()),
        "source_map_digest_sha256": sha_bytes(("\n".join(sorted(source_maps)) + "\n").encode()),
        "source_digest_canonicalization": "fixture",
        "source_map_digest_canonicalization": "fixture",
        "source_rows": rows,
    }
    candidate = {
        "candidate_id": "D972-k3-00000000", "k": 3,
        "kernel_table": table, "kernel_order": 3,
        "automorphism_labels": [[0, 1, 2], [0, 1, 2]], "defects": [0],
        "lift_labels": [0, 0], "fp_generator_count": 4,
        "fp_relators": [], "factor_images": [0, 0, 1, 2],
        "order": 3 * QBAR_ORDER, "braid": True, "marked_generation": True,
        "cell": {"kernel_table": table, "q_relators": [[1]], "aut_pair_index": 0,
                 "defect_index": 0, "lift_pair_index": 0},
        "classification_status": "SHADOW_FIBER_CLASSIFIED",
        "ready_for_producer_ledger": True, "shadow_receipt": receipt,
    }
    candidate["fp_relators"] = expected_extension_relators(candidate)
    candidate["semantic_key"] = semantic_key(candidate)
    return candidate


def set_path(value: Any, path: str, replacement: Any) -> None:
    parts = path.split(".")
    cursor = value
    for part in parts[:-1]:
        cursor = cursor[int(part)] if isinstance(cursor, list) else cursor[part]
    last = parts[-1]
    if isinstance(cursor, list):
        cursor[int(last)] = replacement
    else:
        cursor[last] = replacement


def run_selftest() -> int:
    fixtures = ROOT / "search" / "fixtures" / "d972_dovetail_v1"
    win_command, win_mode = select_gap_command(
        Path("fixture.g"), platform_name="nt", finder=lambda _: "powershell.exe"
    )
    posix_command, posix_mode = select_gap_command(
        Path("fixture.g"), platform_name="posix", finder=lambda _: "/usr/bin/gap"
    )
    require(win_mode == "windows-gap.ps1" and "-File" in win_command and
            posix_mode == "posix-gap-cli" and posix_command[:3] ==
            ["/usr/bin/gap", "-q", "--quitonbreak"],
            "cross-platform GAP command selection failed")
    negative = json.loads((fixtures / "negative_witness_mutations.json").read_text(encoding="utf-8"))
    targets = canonical_target_keys()
    valid = synthetic_candidate(targets)
    verify_candidate(valid, targets)
    checked = 0
    for row in negative["cases"]:
        broken = copy.deepcopy(valid)
        set_path(broken, row["path"], row["replacement"])
        if row.get("reseal_semantic_key"):
            broken["semantic_key"] = semantic_key(broken)
        try:
            verify_candidate(broken, targets)
        except (CheckStop, Disagreement, Inconsistent):
            checked += 1
        else:
            raise AssertionError(f"negative fixture was accepted: {row['id']}")

    base = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    base["hash_chain"]["checkpoint_sha256"] = checkpoint_hash(base)
    interrupt = json.loads(
        (fixtures / "intentional_interrupt_resume.json").read_text(encoding="utf-8")
    )
    resumed = transition(base, {"status": interrupt["interrupted_status"]})
    validate_transition(base, resumed)
    require(resumed["hash_chain"]["sequence"] - base["hash_chain"]["sequence"] ==
            interrupt["expected_sequence_delta"],
            "intentional-resume sequence delta failed")
    require(resumed["hash_chain"]["parent_checkpoint_sha256"] ==
            base["hash_chain"]["checkpoint_sha256"],
            "intentional-resume parent failed")
    require(resumed["cursors"]["agreed"] == base["cursors"]["agreed"],
            "intentional-resume agreed cursor changed")
    state_cases = json.loads((fixtures / "negative_state_mutations.json").read_text(encoding="utf-8"))
    for row in state_cases["cases"]:
        if row["id"] == "parent_hash":
            broken = copy.deepcopy(resumed)
            broken["hash_chain"]["parent_checkpoint_sha256"] = row["replacement"]
            broken["hash_chain"]["checkpoint_sha256"] = checkpoint_hash(broken)
            try:
                validate_transition(base, broken)
            except CheckStop:
                checked += 1
            else:
                raise AssertionError("parent-hash fixture was accepted")
        elif row["id"] == "sequence_gap":
            broken = copy.deepcopy(resumed)
            broken["hash_chain"]["sequence"] += 1
            broken["hash_chain"]["checkpoint_sha256"] = checkpoint_hash(broken)
            try:
                validate_transition(base, broken)
            except CheckStop:
                checked += 1
            else:
                raise AssertionError("sequence-gap fixture was accepted")
        elif row["id"] == "duplicate_semantic_key":
            rows = [copy.deepcopy(valid), copy.deepcopy(valid)]
            keys = [x["semantic_key"] for x in rows]
            if len(keys) == len(set(keys)):
                raise AssertionError("duplicate fixture construction failed")
            checked += 1
    print(json.dumps({
        "status": "PASS", "negative_cases": checked,
        "intentional_interrupt_hash_transition": "PASS", "semantic_key_missing": 0,
        "semantic_key_duplicates_after_resume": 0,
        "parent_hash_match": True,
        "gap_command_selection": {"windows": "PASS", "posix": "PASS"},
        "campaign_full_p_backend": "REQUIRED_OUTSIDE_PARSE_ONLY_SELFTEST",
    }, sort_keys=True))
    return 0


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, help="producer checkpoint JSON; updated in place")
    parser.add_argument("--producer-ledger", type=Path, help="producer JSONL ledger")
    parser.add_argument("--out-dir", type=Path, help="checker artifact directory")
    parser.add_argument("--self-test", action="store_true", help="run fixture and resume tests")
    args = parser.parse_args(argv)
    if not args.self_test and not (args.state and args.producer_ledger and args.out_dir):
        parser.error("--state, --producer-ledger, and --out-dir are required")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.self_test:
        return run_selftest()
    state_path = args.state.resolve()
    producer_ledger = args.producer_ledger.resolve()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    stderr_lines: list[str] = []
    exit_code = 0
    try:
        state, rows = write_checked_state(state_path, producer_ledger, out_dir)
        print(f"{state['status']['code']} {state['hash_chain']['checkpoint_sha256']}")
    except (Disagreement, Inconsistent) as exc:
        old = json.loads(state_path.read_text(encoding="utf-8"))
        validate_state_core(old)
        code = "INCONSISTENT_STOP" if isinstance(exc, Inconsistent) else "DISAGREE_STOP"
        checker_path = out_dir / "checker-ledger.jsonl"
        prior_rows = parse_jsonl(checker_path) if checker_path.is_file() else []
        stop_row = {
            "kind": "stop", "status": code, "reason": str(exc),
            "input_checkpoint_sha256": old["hash_chain"]["checkpoint_sha256"],
        }
        stop_rows = prior_rows + [stop_row]
        atomic_text(checker_path, "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
            for row in stop_rows
        ))
        ledgers = copy.deepcopy(old["ledgers"])
        ledgers["checker"] = ledger_binding(
            checker_path, stop_rows, old["cursors"]["checker"]
        )
        receipts = copy.deepcopy(old["receipts"])
        receipts["checker_stop"] = {
            "status": code, "reason": str(exc),
            "checker_ledger_sha256": sha_file(checker_path),
        }
        stopped = terminalize(old, code, str(exc), ledgers=ledgers, receipts=receipts)
        atomic_json(state_path, stopped)
        stderr_lines.append(str(exc))
        print(f"{code} {stopped['hash_chain']['checkpoint_sha256']}")
    except (CheckStop, OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        exit_code = 2
        stderr_lines.append(str(exc))
        atomic_json(out_dir / "state-stop.json", {"status": "STATE_STOP", "reason": str(exc)})
        print(str(exc), file=sys.stderr)
    finally:
        atomic_text(out_dir / "stderr.log", "\n".join(stderr_lines) + ("\n" if stderr_lines else ""))
        files = [path for path in out_dir.rglob("*") if path.is_file()]
        atomic_json(out_dir / "resource_receipt.json", {
            "wall_seconds": round(time.monotonic() - started, 6),
            "artifact_file_count": len(files),
            "artifact_bytes_before_receipt": sum(path.stat().st_size for path in files),
            "pid": os.getpid(), "exit_code": exit_code,
        })
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
