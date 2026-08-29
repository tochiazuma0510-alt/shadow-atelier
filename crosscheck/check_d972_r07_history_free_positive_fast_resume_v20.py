#!/usr/bin/env python3
"""Independent A0 v20 checker with RSS/checkpoint transport repairs."""
from __future__ import annotations

import hashlib
from pathlib import Path


_BASE = Path(__file__).resolve().with_name(
    "check_d972_r07_history_free_positive_fast_resume_v13.py")
_BASE_BYTES = 131946
_BASE_SHA256 = "42e8f6df8d85169bf4039bc4195a0e47c284ad475a177414308ba28f99377b64"
_V18 = Path(__file__).resolve().with_name(
    "check_d972_r07_history_free_positive_fast_resume_v18.py")
_V18_BYTES = 1317
_V18_SHA256 = "83ebfe5088388f5c84bbab9e52ef28cb8888fb944fbe417cf98041bab34bfaa9"
_V20_PRODUCER = "search/d972_r07_history_free_positive_fast_resume_v20.py"
_V20_PRODUCER_BYTES = 10739
_V20_PRODUCER_SHA256 = "cf775975304a56cd3587470074e31d3a2000fba418fab5793fd25d6307150ed7"


def _replace_once(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("v20 checker " + label + " substitution cardinality")
    result = source.replace(old, new, 1)
    if (len(result) != len(source) - len(old) + len(new) or
            result.count(new) != 1):
        raise SystemExit("v20 checker " + label + " substitution failed")
    return result


def _delete_once(source: bytes, old: bytes, label: str) -> bytes:
    """Delete exactly one pinned fragment without counting b\"\"."""
    if not old or source.count(old) != 1:
        raise SystemExit("v20 checker " + label + " deletion cardinality")
    result = source.replace(old, b"", 1)
    if result.count(old) != 0 or len(result) != len(source) - len(old):
        raise SystemExit("v20 checker " + label + " deletion failed")
    return result


_v18_raw = _V18.read_bytes()
if len(_v18_raw) != _V18_BYTES or hashlib.sha256(
        _v18_raw).hexdigest() != _V18_SHA256:
    raise SystemExit("v20 checker v18 owner drift")
_patched = _BASE.read_bytes()
if len(_patched) != _BASE_BYTES or hashlib.sha256(
        _patched).hexdigest() != _BASE_SHA256:
    raise SystemExit("v20 checker frozen v13 owner drift")

_patched = _replace_once(
    _patched,
    b"search/d972_r07_history_free_positive_fast_resume_v13.py",
    _V20_PRODUCER.encode("ascii"),
    "producer-path",
)
_patched = _replace_once(
    _patched, b"147409", str(_V20_PRODUCER_BYTES).encode("ascii"),
    "producer-bytes",
)
_patched = _replace_once(
    _patched,
    b"4d1be83fefbb1a1c0b23010825c0013b80650439b714dce7e35a6e0f53a2ff2a",
    _V20_PRODUCER_SHA256.encode("ascii"),
    "producer-sha",
)

# Independently reconstruct the descriptor inverse canary and remove only the
# two hot-loop repetitions.  The checker shares no helper with the producer.
_checker_replacements = (
    (b"                h_raw = blob(runtime, h); h_inverse = quotient.inverse(h)\n",
     b"                h_raw = blob(runtime, h); h_inverse = quotient.inverse(h)\n"
     b"                require(quotient.mul(h_inverse, h) == quotient.identity and\n"
     b"                        quotient.mul(h, h_inverse) == quotient.identity,\n"
     b'                        "checker descriptor inverse canary")\n',
     "descriptor-inverse"),
    # JSON checkpoint literals contain lists nested two levels deep.  Freeze
    # them recursively before hash-cons replay; retain raw lists for schema
    # shape checks below.
    (b"def validate_dag_nodes(nodes: Any) -> None:\n",
     b"def _checker_freeze_dag_json(value: Any) -> Any:\n"
     b"    if type(value) is list:\n"
     b"        return tuple(_checker_freeze_dag_json(item) for item in value)\n"
     b"    require(type(value) in (str, int), \"DAG JSON atom\")\n"
     b"    return value\n\n\n"
     b"def validate_dag_nodes(nodes: Any) -> None:\n",
     "dag-normalizer"),
    (b"        node = tuple(raw); opcode = node[0]\n"
     b"        require(node not in seen, \"DAG hash-cons duplicate\")\n"
     b"        seen.add(node)\n",
     b"        node = tuple(raw); opcode = node[0]\n"
     b"        frozen = _checker_freeze_dag_json(raw)\n"
     b"        require(frozen not in seen, \"DAG hash-cons duplicate\")\n"
     b"        seen.add(frozen)\n",
     "dag-validation-key"),
    (b'    require(workers in (2, 4), "checker worker count")',
     b'    require(workers == 2, "checker worker count")',
     "two-worker-replay"),
    (b'    require(type(value) is dict and value.get("workers") in (2, 4) and',
     b'    require(type(value) is dict and value.get("workers") == 2 and',
     "two-worker-common-owner"),
    (b'    require(type(boundary) is dict and boundary.get("workers") in (2, 4) and',
     b'    require(type(boundary) is dict and boundary.get("workers") == 2 and',
     "two-worker-checkpoint-owner"),
)
for _old, _new, _label in _checker_replacements:
    _patched = _replace_once(_patched, _old, _new, _label)

_patched = _delete_once(
    _patched,
    b"            require(quotient.mul(translation, descriptor[\"h\"]) == g,\n"
    b"                    \"checker boundary t*h=g\")\n",
    "boundary-pair-canary",
)
_patched = _delete_once(
    _patched,
    b"            require(quotient.mul(translation, descriptor[\"h\"]) == g,\n"
    b"                    \"selected contributor orientation\")\n",
    "selected-pair-canary",
)

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
