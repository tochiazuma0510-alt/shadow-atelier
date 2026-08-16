#!/usr/bin/env python3
"""Independent checker for configurable direct AutomaticStructure v2.

The producer is never imported or executed.  The pinned source/norm data and
the producer's reduced ledger are checked here, while a separately executed
GAP replay must be supplied before an A/B terminal result is accepted.  The
replay receipt is required to report an independent GpGenMult/GpCheckMult /
GpAxioms pass and the all-972 ReducedForm ledger.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "search" / "d972_b4_original_automatic_v2.g"
REPLAY = ROOT / "search" / "check_d972_b4_original_automatic_replay_v2.g"
V1_SOURCE_SHA = "fcb32175837412bbce9bf117fbe0eb8c4f8cc1b11f9fa921b46acf133ecc6874"
SOURCE_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
RHO_SHA = "23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed"
ROOF_SHA = "3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8"
NORM_SHA = "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"


def load_v1_checker():
    path = ROOT / "search" / "check_d972_b4_original_automatic_v1.py"
    spec = importlib.util.spec_from_file_location("d972_original_v1_checker", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("v1 checker unavailable")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def source_gate() -> str:
    raw = PRODUCER.read_bytes()
    if any(b >= 128 for b in raw):
        raise ValueError("v2 producer is not ASCII")
    text = raw.decode("ascii")
    if re.search(r"(?m)^\s*QUIT;\s*$", text):
        raise ValueError("v2 producer has a bare QUIT")
    for needle in (
        "D972OA2CallNew",
        "D972OA2MaxEqns",
        "D972OA2MaxStored",
        "v2_settings",
        "B4_ORIGINAL_AUTOMATIC_V2_FINAL_MARKER",
    ):
        if needle not in text:
            raise ValueError(f"v2 producer missing {needle}")
    return hashlib.sha256(raw).hexdigest()


def replay_gate() -> str:
    raw = REPLAY.read_bytes()
    if any(b >= 128 for b in raw):
        raise ValueError("v2 replay is not ASCII")
    text = raw.decode("ascii")
    if re.search(r"(?m)^\s*QUIT;\s*$", text):
        raise ValueError("v2 replay has a bare QUIT")
    for needle in (
        "GpGenMult(",
        "GpCheckMult(",
        "GpAxioms(",
        "gpaxioms_rechecked",
        "B4_ORIGINAL_AUTOMATIC_V2_REPLAY_FINAL_MARKER",
    ):
        if needle not in text:
            raise ValueError(f"v2 replay missing {needle}")
    return hashlib.sha256(raw).hexdigest()


def expected_settings(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "producer": "d972_b4_original_automatic_v2",
        "large": bool(args.large),
        "filestore": bool(args.filestore),
        "diff1": bool(args.diff1),
        "compute_size": bool(args.compute_size),
        "post_replay": bool(args.post_replay),
        "maxeqns": args.maxeqns,
        "maxstates": args.maxstates,
        "maxwdiffs": args.maxwdiffs,
        "maxstoredlen": [args.maxstoredlen[0], args.maxstoredlen[1]],
        "v1_source_sha256": V1_SOURCE_SHA,
    }


def _check_reduced_ledger(receipt: dict[str, Any]) -> tuple[list[list[int]], int]:
    rw = receipt.get("reduced_norm_words")
    if not isinstance(rw, list) or len(rw) != 972:
        raise ValueError("reduced ledger")
    for w in rw:
        if not isinstance(w, list) or any(type(x) is not int or x == 0 or abs(x) > 6 for x in w):
            raise ValueError("reduced word shape")
    digest = hashlib.sha256(json.dumps(rw, separators=(",", ":"), ensure_ascii=True).encode()).hexdigest()
    if digest != receipt.get("reduced_norm_words_sha256"):
        raise ValueError("reduced ledger digest")
    empty = sum(not w for w in rw)
    if receipt.get("empty_count") != empty:
        raise ValueError("empty count")
    return rw, empty


def _check_automata(receipt: dict[str, Any]) -> None:
    names = receipt.get("automaton_names")
    bindings = receipt.get("automaton_bindings")
    states = receipt.get("automaton_states")
    shas = receipt.get("automaton_sha256")
    paths = receipt.get("automaton_paths")
    if names not in (["wa", "diff1", "diff2"], ["wa", "diff1", "diff2", "reduction"]):
        raise ValueError("automaton names")
    expected_bindings = ["D972OAWA", "D972OADiff1", "D972OADiff2"]
    if len(names) == 4:
        expected_bindings.append("D972OAReduction")
    if bindings != expected_bindings:
        raise ValueError("automaton bindings")
    if not isinstance(states, list) or len(states) != len(names) or any(type(x) is not int or x <= 0 for x in states):
        raise ValueError("automaton states")
    if not isinstance(shas, list) or len(shas) != len(names) or any(not isinstance(x, str) or len(x) != 64 for x in shas):
        raise ValueError("automaton hashes")
    if not isinstance(paths, list) or len(paths) != len(names):
        raise ValueError("automaton paths")
    for path, expected, nstates in zip(paths, shas, states):
        p = Path(path)
        if not p.is_file():
            raise ValueError(f"automaton missing: {path}")
        raw = p.read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError("automaton SHA")
        m = re.search(rb"states\s*:=\s*\[([^]]*)\]", raw, re.S)
        if m is None:
            raise ValueError("automaton states ledger")
        txt = m.group(1).strip()
        got = int(txt[3:].strip()) if txt.startswith(b"1..") else len([x for x in txt.split(b",") if x.strip()])
        if got != nstates:
            raise ValueError("automaton state drift")


def _check_replay(
    replay: dict[str, Any],
    replay_path: Path,
    receipt_sha: str,
    settings: dict[str, Any],
    empty: int,
) -> dict[str, Any]:
    if replay.get("schema") != "d972-b4-original-automatic-gap-replay/v2":
        raise ValueError("replay schema drift")
    if replay.get("automatic_receipt_sha256") != receipt_sha:
        raise ValueError("replay receipt binding drift")
    for key, expected in (
        ("source_sha256", SOURCE_SHA),
        ("word_artifact_sha256", WORDS_SHA),
        ("relator_sha256", RELATOR_SHA),
        ("rho_words_sha256", RHO_SHA),
        ("roof_words_sha256", ROOF_SHA),
        ("roof_norm_sha256", NORM_SHA),
    ):
        if replay.get(key) != expected:
            raise ValueError(f"replay {key} drift")
    if replay.get("norm_count") != 972 or replay.get("empty_count") != empty:
        raise ValueError("replay norm/empty count drift")
    if replay.get("nonempty_count") != 972 - empty:
        raise ValueError("replay nonempty count drift")
    if replay.get("all_empty") is not (empty == 972):
        raise ValueError("replay all-empty drift")
    for key in ("automata_replayed", "gpgenmult_rechecked", "gpcheckmult_rechecked", "gpaxioms_rechecked", "gpaxioms_result"):
        if replay.get(key) is not True:
            raise ValueError(f"replay {key} missing")
    if settings is None:
        if replay.get("v2_settings") is not None or replay.get("legacy_v1") is not True or replay.get("post_replay") is not True:
            raise ValueError("legacy replay settings/default binding drift")
    elif replay.get("v2_settings") != settings:
        raise ValueError("replay settings drift")
    status = replay.get("status")
    if empty == 972 and status != "B4_B_TERMINAL_CANDIDATE_REPLAYED":
        raise ValueError("replay B status drift")
    if empty != 972 and status != "B4_A_CANDIDATE_REPLAYED":
        raise ValueError("replay A status drift")
    return {
        "replay_sha256": hashlib.sha256(replay_path.read_bytes()).hexdigest(),
        "replay_status": status,
        "gpaxioms_rechecked": True,
        "gpaxioms_result": True,
        "all_empty": empty == 972,
    }


def check_receipt(
    receipt: dict[str, Any],
    args: argparse.Namespace,
    mod: Any,
    replay: dict[str, Any] | None,
    replay_path: Path | None,
    receipt_sha: str,
) -> dict[str, Any]:
    legacy = bool(args.legacy_v1)
    settings = None if legacy else receipt.get("v2_settings")
    expected = expected_settings(args)
    if legacy:
        if (args.large, args.filestore, args.diff1, args.compute_size, args.post_replay) != (1, 1, 0, 1, 1):
            raise ValueError("legacy v1 replay settings must be the exact v1 defaults")
        if (args.maxeqns, args.maxstates, args.maxwdiffs, args.maxstoredlen) != (250000, 250000, 250000, [4000, 4000]):
            raise ValueError("legacy v1 replay numeric caps drift")
        if "v2_settings" in receipt:
            raise ValueError("legacy v1 receipt unexpectedly has v2_settings")
    elif settings != expected:
        raise ValueError(f"v2 settings drift: got {settings!r}, want {expected!r}")
    if receipt.get("source_sha256") != SOURCE_SHA or receipt.get("word_artifact_sha256") != WORDS_SHA:
        raise ValueError("canonical source/word SHA drift")
    if receipt.get("relator_sha256") != RELATOR_SHA or receipt.get("rho_words_sha256") != RHO_SHA:
        raise ValueError("canonical relator/rho SHA drift")
    if receipt.get("roof_words_sha256") != ROOF_SHA or receipt.get("roof_norm_sha256") != NORM_SHA:
        raise ValueError("canonical roof/norm SHA drift")
    if receipt.get("norm_count") != 972:
        raise ValueError("norm count drift")
    rel, norms = mod.canonical()
    if len(rel) != 158 or len(norms) != 972:
        raise ValueError("independent canonical reconstruction count drift")
    if receipt.get("schema") == "d972-b4-original-automatic-precheck/v1":
        if legacy:
            raise ValueError("legacy v1 cannot be a precheck receipt")
        if receipt.get("status") != "INPUT_PRECHECK_PASS" or receipt.get("automatic_invoked") is not False:
            raise ValueError("precheck status gate")
        if receipt.get("relator_count") != 158:
            raise ValueError("precheck relator count")
        return {
            "schema": "d972-b4-original-automatic-v2-independent-check/v1",
            "status": "PRECHECK_CROSSCHECKED",
            "norm_count": 972,
            "automatic_invoked": False,
            "settings": settings,
        }
    if receipt.get("schema") != "d972-b4-original-automatic/v1":
        raise ValueError("receipt schema drift")
    if receipt.get("automatic_success") is not True:
        return {
            "schema": "d972-b4-original-automatic-v2-independent-check/v1",
            "status": "UNKNOWN_AUTOMATIC_STRUCTURE_FAILURE",
            "norm_count": 972,
            "terminal_claim": False,
            "settings": settings,
        }
    _, empty = _check_reduced_ledger(receipt)
    _check_automata(receipt)
    # The producer's field is only a historical success bit.  It is not an
    # independent axiom proof, so a heavy receipt is UNKNOWN until the GAP
    # replay has re-run GpAxioms and replayed all 972 words.
    if replay is None or replay_path is None:
        return {
            "schema": "d972-b4-original-automatic-v2-independent-check/v1",
            "status": "UNKNOWN_V2_REPLAY_REQUIRED",
            "norm_count": 972,
            "empty_count": empty,
            "settings": settings,
            "terminal_claim": False,
        }
    replay_out = _check_replay(replay, replay_path, receipt_sha, settings, empty)
    status = "B4_B_TERMINAL_CANDIDATE_REPLAYED" if empty == 972 else "B4_A_CANDIDATE_REPLAYED"
    out = {
        "schema": "d972-b4-original-automatic-v2-independent-check/v1",
        "status": status,
        "norm_count": 972,
        "empty_count": empty,
        "settings": settings,
        "terminal_claim": True,
    }
    out.update(replay_out)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--receipt", type=Path, required=True)
    ap.add_argument("--replay", type=Path, default=None,
                    help="independently generated v2 GAP replay receipt")
    ap.add_argument("--legacy-v1", action="store_true",
                    help="check a frozen v1 receipt with the v2 independent replay")
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--large", type=int, choices=(0, 1), default=1)
    ap.add_argument("--filestore", type=int, choices=(0, 1), default=1)
    ap.add_argument("--diff1", type=int, choices=(0, 1), default=0)
    ap.add_argument("--compute-size", type=int, choices=(0, 1), default=1)
    ap.add_argument("--post-replay", type=int, choices=(0, 1), default=0)
    ap.add_argument("--maxeqns", type=int, default=250000)
    ap.add_argument("--maxstates", type=int, default=250000)
    ap.add_argument("--maxwdiffs", type=int, default=250000)
    ap.add_argument("--maxstoredlen", type=int, nargs=2, default=[4000, 4000])
    args = ap.parse_args()
    if min(args.maxeqns, args.maxstates, args.maxwdiffs, *args.maxstoredlen) <= 0:
        raise ValueError("nonpositive cap")
    producer_sha = source_gate()
    replay_source_sha = replay_gate()
    receipt_path = args.receipt.resolve()
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt_sha = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    replay = None
    replay_path = None
    if args.replay is not None:
        replay_path = args.replay.resolve()
        replay = json.loads(replay_path.read_text(encoding="utf-8"))
    mod = load_v1_checker()
    out = check_receipt(receipt, args, mod, replay, replay_path, receipt_sha)
    out["producer_source_sha256"] = producer_sha
    out["replay_source_sha256"] = replay_source_sha
    out["receipt_sha256"] = receipt_sha
    if replay_path is not None:
        out["replay_receipt_path"] = str(replay_path)
    args.output.resolve().write_text(json.dumps(out, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, sort_keys=True))
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"B4_ORIGINAL_AUTOMATIC_V2_CHECK_FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
