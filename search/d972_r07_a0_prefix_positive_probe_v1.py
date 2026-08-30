#!/usr/bin/env python3
"""Task432: positive-only fork of the authenticated v12 occurrence prefix."""
from __future__ import annotations
import argparse, hashlib, json, sys, traceback, types
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V12_REL = "search/d972_r07_a0_pb34_direct_quotient_owner_v12.py"
V12_BYTES = 51884
V12_SHA = "3016b6a21d9fafbf037dbb5384dcca81f49e1fa44ae45a466ff16f1fd13948b3"
INPUT_BYTES = 326449173
INPUT_SHA = "0b3169fe6e7051fe46a28bb966ffd3dfeada841dce1a6fe2358959dd99402ff1"
SCHEMA = "d972-r07-a0-pb34-direct-quotient-owner/v12"
UNKNOWN = "UNKNOWN"
RESOURCE = "UNKNOWN_RESOURCE"


def need(value, message):
    if not value:
        raise RuntimeError(message)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def seal_input(path):
    p = Path(path)
    need(not p.is_absolute() and p.parent == Path("ci/out"), "input_path")
    need(not p.is_symlink() and p.is_file(), "input_regular_file")
    h = hashlib.sha256()
    n = 0
    with p.open("rb") as src:
        for chunk in iter(lambda: src.read(1 << 20), b""):
            h.update(chunk)
            n += len(chunk)
    digest = h.hexdigest()
    need(n == INPUT_BYTES and digest == INPUT_SHA, "input_seal")
    return n, digest


class FalseTruthDeque(deque):
    """A content-preserving queue whose truth value suppresses actor scans."""

    def __bool__(self):
        return False


def load_v12():
    p = ROOT / V12_REL
    blob = p.read_bytes()
    need(len(blob) == V12_BYTES and sha_bytes(blob) == V12_SHA, "v12_pin")
    mod = types.ModuleType("task432_v12_pinned")
    mod.__file__ = str(p)
    sys.modules[mod.__name__] = mod
    exec(compile(blob, V12_REL, "exec"), mod.__dict__, mod.__dict__)
    return mod


def run_probe(input_path, output_path, seconds=9000, rss_bytes=4800000000):
    inp = Path(input_path)
    out = Path(output_path)
    n, digest = seal_input(inp)
    need(not out.is_absolute() and out.parent == Path("ci/out"), "output_path")
    need(not out.exists() and not out.is_symlink(), "output_must_be_fresh")
    mod = load_v12()
    mod.LAST_DURABLE = None
    mod.LAST_INPUT_SEAL = None
    old_deque = mod.deque
    for attr in ("_progress_rank", "_progress_time"):
        if hasattr(mod.run, attr):
            delattr(mod.run, attr)
    mod.deque = FalseTruthDeque
    try:
        args = types.SimpleNamespace(
            resume=str(inp).replace("\\", "/"),
            resume_v11_url=None,
            checkpoint=None,
            seconds=float(seconds),
            rss_bytes=int(rss_bytes),
        )
        try:
            result = mod.run(args)
        except Exception as exc:
            status = RESOURCE if str(exc).startswith(getattr(mod, "RESOURCE", RESOURCE)) else UNKNOWN
            result = {"status": status, "reason": str(exc), "durable_state": mod.LAST_DURABLE}
            if status == UNKNOWN:
                result["exception"] = {
                    "type": type(exc).__name__,
                    "reason": str(exc),
                    "traceback": traceback.format_exc(limit=24)[-12288:],
                }
    finally:
        mod.deque = old_deque
    status = result.get("status", UNKNOWN)
    if status == RESOURCE:
        result["probe_terminal"] = RESOURCE
        status = UNKNOWN
    if result.get("reason") == "six_action_exhausted":
        result["reason"] = "positive_only_six_action_exhausted"
    if status not in {"COMMON_CANDIDATE", UNKNOWN, RESOURCE}:
        result["reason"] = "positive_only_forbidden_terminal:" + str(status)
        status = UNKNOWN
    result["status"] = status
    envelope = {
        "schema": SCHEMA,
        "status": status,
        "terminal": status,
        "complete": False,
        "a0": result,
        "durable_state": result.get("durable_state") or mod.LAST_DURABLE,
        "eliminated_boundary_rows": 0,
        "old_boundary_closure_present": False,
        "claim_boundary": {
            "common_word": False,
            "A0_membership": False,
            "fake": False,
            "Ihara_witness": False,
            "compatible_lift": False,
            "verified": False,
        },
        "checkpoint_input": str(inp).replace("\\", "/"),
        "checkpoint_output": None,
        "checkpoint_input_seal": {"path": str(inp).replace("\\", "/"), "bytes": n, "sha256": digest},
        "prefix_probe": {
            "input": {"path": str(inp).replace("\\", "/"), "bytes": n, "sha256": digest},
            "original_rank": 1316,
            "original_frontier": 906,
            "positive_only": True,
        },
    }
    out.write_bytes(json.dumps(envelope, sort_keys=True, separators=(",", ":"), default=str).encode() + b"\n")
    return envelope


def fixture():
    q = FalseTruthDeque([1, 2, 3])
    need(not q and len(q) == 3 and list(q) == [1, 2, 3], "false_truth_deque")
    source = Path(__file__).read_text(encoding="utf-8")
    need("checkpoint=None" in source and ("cp" + "_write") not in source, "probe_no_checkpoint_write")
    mod = load_v12()
    need(mod.fixture().get("status") == "FIXTURE_PASS", "v12_fixture")
    return {"status": "FIXTURE_PASS", "false_truth_deque": True, "v12_fixture": True, "checkpoint_write": False}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("FIXTURE", "PRODUCTION"), default="PRODUCTION")
    ap.add_argument("--input-checkpoint")
    ap.add_argument("--output")
    ap.add_argument("--seconds", type=float, default=9000)
    ap.add_argument("--rss-bytes", type=int, default=4800000000)
    a = ap.parse_args()
    try:
        if a.mode == "FIXTURE":
            out = fixture()
            print("R07_A0_PREFIX_POSITIVE_PROBE_V1_FIXTURE_PASS " + json.dumps(out, sort_keys=True, separators=(",", ":")), flush=True)
            return 0
        need(a.input_checkpoint and a.output, "production_paths_required")
        envelope = run_probe(a.input_checkpoint, a.output, a.seconds, a.rss_bytes)
        print("R07_A0_PREFIX_POSITIVE_PROBE_V1 " + envelope["status"], flush=True)
        return 0
    except Exception as exc:
        print("R07_A0_PREFIX_POSITIVE_PROBE_V1 " + UNKNOWN + " " + str(exc), flush=True)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
