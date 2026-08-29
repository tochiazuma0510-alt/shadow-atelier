#!/usr/bin/env python3
"""A0 v20 minimal RSS/checkpoint repair over the frozen v13 owner."""
from __future__ import annotations

import hashlib
from pathlib import Path


_BASE = Path(__file__).resolve().with_name(
    "d972_r07_history_free_positive_fast_resume_v13.py")
_BASE_BYTES = 147409
_BASE_SHA256 = "4d1be83fefbb1a1c0b23010825c0013b80650439b714dce7e35a6e0f53a2ff2a"
_V18 = Path(__file__).resolve().with_name(
    "d972_r07_history_free_positive_fast_resume_v18.py")
_V18_BYTES = 2557
_V18_SHA256 = "55505c6b59ebc9cc61c12c0229668509a2fcf7530ca14dbd791a8b18a95c5433"


def _replace_once(source: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if not old or not new or old == new or source.count(old) != 1 or source.count(new) != 0:
        raise SystemExit("v20 " + label + " substitution cardinality")
    result = source.replace(old, new, 1)
    if (len(result) != len(source) - len(old) + len(new) or
            result.count(new) != 1):
        raise SystemExit("v20 " + label + " substitution failed")
    return result


def _delete_once(source: bytes, old: bytes, label: str) -> bytes:
    """Delete exactly one pinned fragment; never count the empty replacement."""
    if not old or source.count(old) != 1:
        raise SystemExit("v20 " + label + " deletion cardinality")
    result = source.replace(old, b"", 1)
    if result.count(old) != 0 or len(result) != len(source) - len(old):
        raise SystemExit("v20 " + label + " deletion failed")
    return result


_v18_raw = _V18.read_bytes()
if len(_v18_raw) != _V18_BYTES or hashlib.sha256(
        _v18_raw).hexdigest() != _V18_SHA256:
    raise SystemExit("v20 v18 correctness owner drift")
_patched = _BASE.read_bytes()
if len(_patched) != _BASE_BYTES or hashlib.sha256(
        _patched).hexdigest() != _BASE_SHA256:
    raise SystemExit("v20 frozen v13 arithmetic owner drift")

# Preserve the complete accepted v18 correctness/checkpoint delta.  Only the
# boundary-pair resource is raised further below, as in the intended v19 path.
_v18_replacements = (
    (b'"boundary_pairs": 8_000_000,',
     b'"boundary_pairs": 80_000_000,'),
    (b"                    selftest: dict[str, Any] | None) -> dict[str, Any]:",
     b"                    selftest: dict[str, Any] | None,\n"
     b"                    light_input_sha256: str | None = None) -> dict[str, Any]:"),
    (b'        "source": source, "source_snapshots": None if registry is None else registry.public(),\n'
     b'        "monitor": None if meter is None else meter.public(),',
     b'        "source": source, "source_snapshots": None if registry is None else registry.public(),\n'
     b'        "light_input_sha256": light_input_sha256,\n'
     b'        "monitor": None if meter is None else meter.public(),'),
    (b"            meter, None, None if search is None else search.boundary.public(), selftest)",
     b"            meter, None, None if search is None else search.boundary.public(), selftest,\n"
     b"            None if runtime is None else runtime.get(\"light_input_sha256\"))"),
    (b"                                  meter, reference, boundary_public, selftest)",
     b"                                  meter, reference, boundary_public, selftest,\n"
     b"                                  None if runtime is None else runtime.get(\"light_input_sha256\"))"),
    (b'        "heavy_input_sha256": None, "heavy_complete": False,\n'
     b'        "triangular_certificate": triangular,',
     b'        "heavy_input_sha256": None, "heavy_complete": False,\n'
     b'        "heavy_reconstructible": False,\n'
     b'        "triangular_certificate": triangular,'),
)
for _old, _new in _v18_replacements:
    _patched = _replace_once(_patched, _old, _new, "v18")

_v20_replacements = (
    (b'"boundary_pairs": 80_000_000,',
     b'"boundary_pairs": 500_000_000,',
     "boundary-cap"),
    # Descriptor construction owns the inverse canary once for all epochs.
    (b"                h_inverse = quotient.inverse(h)\n",
     b"                h_inverse = quotient.inverse(h)\n"
     b"                require(quotient.mul(h_inverse, h) == quotient.identity and\n"
     b"                        quotient.mul(h, h_inverse) == quotient.identity,\n"
     b'                        "descriptor inverse canary")\n',
     "descriptor-inverse"),
    # exact_dual consumes the already reduced target and its DAG node.  No
    # persistent decode cache is installed: worker epochs retain v13's bounded
    # local decode lifetime.
    (b"    def exact_dual(self, target: dict[bytes, int]) -> tuple[dict[bytes, int],\n"
     b"                                                            dict[bytes, int],\n"
     b"                                                            dict[str, int]]:\n"
     b"        remainder, solution_node = self.reduce(target)\n",
     b"    def exact_dual(self, target: dict[bytes, int],\n"
     b"                   known_remainder: dict[bytes, int] | None = None,\n"
     b"                   known_solution_node: int | None = None) -> tuple[dict[bytes, int],\n"
     b"                                                            dict[bytes, int],\n"
     b"                                                            dict[str, int]]:\n"
     b"        if known_remainder is None:\n"
     b"            remainder, solution_node = self.reduce(target)\n"
     b"        else:\n"
     b"            remainder, solution_node = known_remainder, known_solution_node\n"
     b"            require(remainder and isinstance(solution_node, int) and\n"
     b"                    0 <= solution_node < len(self.ancestry.nodes),\n"
     b'                    "replayed target reduction")\n',
     "dual-input"),
    (b"            if dual is None:\n"
     b"                dual, exact_remainder, exact_solution_node = self.reducer.exact_dual(self.target)\n",
     b"            if dual is None:\n"
     b"                dual, exact_remainder, exact_solution_node = self.reducer.exact_dual(\n"
     b"                    self.target, remainder, solution_node)\n",
     "dual-hot-loop"),
    # Recursive JSON-list normalization is used both for hash-cons validation
    # and for restoring literal nodes into immutable/hashable ancestry keys.
    (b"def validate_dag_nodes(nodes: Any) -> None:\n",
     b"def _freeze_dag_json(value: Any) -> Any:\n"
     b"    if type(value) is list:\n"
     b"        return tuple(_freeze_dag_json(item) for item in value)\n"
     b"    require(type(value) in (str, int), \"DAG JSON atom\")\n"
     b"    return value\n\n\n"
     b"def _thaw_dag_json(value: Any) -> Any:\n"
     b"    if type(value) is tuple:\n"
     b"        return [_thaw_dag_json(item) for item in value]\n"
     b"    require(type(value) in (str, int), \"DAG internal atom\")\n"
     b"    return value\n\n\n"
     b"def validate_dag_nodes(nodes: Any) -> None:\n",
     "dag-normalizers"),
    (b"        node = tuple(raw); opcode = node[0]\n"
     b"        require(node not in seen, \"DAG hash-cons duplicate\"); seen.add(node)\n",
     b"        node = tuple(raw); opcode = node[0]\n"
     b"        frozen = _freeze_dag_json(raw)\n"
     b"        require(frozen not in seen, \"DAG hash-cons duplicate\"); seen.add(frozen)\n",
     "dag-validation-key"),
    (b'                "dag_nodes": [list(node) for node in self.reducer.ancestry.nodes],',
     b'                "dag_nodes": [_thaw_dag_json(node) for node in self.reducer.ancestry.nodes],',
     "live-dag-serialization"),
    (b'        "dag_nodes": [list(node) for node in reducer.ancestry.nodes],',
     b'        "dag_nodes": [_thaw_dag_json(node) for node in reducer.ancestry.nodes],',
     "prepool-dag-serialization"),
    (b"    search.reducer.ancestry.nodes = [tuple(node) for node in formal[\"dag_nodes\"]]\n"
     b"    search.reducer.ancestry.intern = {\n"
     b"        tuple(node): index for index, node in enumerate(formal[\"dag_nodes\"])}",
     b"    search.reducer.ancestry.nodes = [\n"
     b"        _freeze_dag_json(node) for node in formal[\"dag_nodes\"]]\n"
     b"    search.reducer.ancestry.intern = {\n"
     b"        _freeze_dag_json(node): index\n"
     b"        for index, node in enumerate(formal[\"dag_nodes\"])}",
     "dag-restore"),
    (b'    require(formal.get("dag_nodes") == [list(node) for node in search.reducer.ancestry.nodes] and\n',
     b'    require(formal.get("dag_nodes") == [_thaw_dag_json(node) for node in search.reducer.ancestry.nodes] and\n',
     "dag-restore-roundtrip"),
    # A single production worker count is load-bearing for the RSS repair.
    (b"        if workers not in (2, 4):\n"
     b"            raise InputStop(\"workers_must_be_2_or_4\")",
     b"        if workers != 2:\n"
     b"            raise InputStop(\"workers_must_equal_2\")",
     "two-worker-owner"),
    (b'    value.add_argument("--workers", type=int, choices=(2, 4), default=4)',
     b'    value.add_argument("--workers", type=int, choices=(2,), default=2)',
     "two-worker-cli"),
    # Retain the one-minute rate limit while exposing live RSS and all four
    # search counters needed by the GHA operator.
    (b'            print("A0_PROGRESS side=producer phase=" + str(phase) +\n'
     b'                  " elapsed_seconds=" + str(int(elapsed)), flush=True)',
     b'            print("A0_PROGRESS side=producer phase=" + str(phase) +\n'
     b'                  " elapsed_seconds=" + str(int(elapsed)) +\n'
     b'                  " boundary_pairs=" + str(self.counters["boundary_pairs"]) +\n'
     b'                  " candidate_words=" + str(self.counters["candidate_words"]) +\n'
     b'                  " retained_columns=" + str(self.counters["retained_columns"]) +\n'
     b'                  " dag_nodes=" + str(self.counters["dag_node_allocations"]) +\n'
     b'                  " parent_rss=" + str(parent) +\n'
     b'                  " children_rss=" + str(children), flush=True)',
     "progress-rss-counters"),
)
for _old, _new, _label in _v20_replacements:
    _patched = _replace_once(_patched, _old, _new, _label)

# v19 used the generic replacement helper with b"", which rejects every
# deletion because bytes.count(b"") is always nonzero.  v20 deliberately owns
# these two deletions through the separate, exact-cardinality gate above.
_patched = _delete_once(
    _patched,
    b"        require(quotient.mul(translation, descriptor[\"h\"]) == g,\n"
    b"                \"worker t*h=g\")\n",
    "worker-pair-canary",
)
_patched = _delete_once(
    _patched,
    b"                require(quotient.mul(translation, descriptor[\"h\"]) == g,\n"
    b"                        \"parent t*h=g\")\n",
    "parent-pair-canary",
)

exec(compile(_patched, str(Path(__file__).resolve()), "exec"), globals(), globals())
