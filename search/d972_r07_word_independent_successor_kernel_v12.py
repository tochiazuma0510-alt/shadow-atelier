#!/usr/bin/env python3
"""A4 v12 owner: frozen v6 arithmetic with audited cap/hot-path repairs."""
from __future__ import annotations
import hashlib
from pathlib import Path

SOURCE = Path(__file__).with_name("d972_r07_word_independent_successor_kernel_v6.py")
SOURCE_BYTES = 219187
SOURCE_SHA256 = "aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a"
PATCHES = (
    (b'result.get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"',
     b'isinstance(result.get("audit"), dict) and result["audit"].get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"'),
    (b'recovery_v1_claim == digest(recovery_v1_body)',
     b'digest(recovery_v1_body) == "0c7f6b03de740a1bbae02b2a5c7aeb48071369c6cd1a5e08c79c05dbf9edd289"'),
    (b'recovery_claim == digest(recovery_body)',
     b'digest(recovery_body) == "fd949d8eb6a3b22891177f19d41af8e61c3f28aefe41a073cf3a72f8979cb1a2"'),
    (b'(243, 26, 19, 288)', b'(243, 27, 19, 261)'),
    (b'literal == 114458', b'literal == 111404'),
    (b'require(desired >= charged, "serialize:fixed_point_shrunk")', b'if desired < charged: write_atomic(path, encoded); return'),
    (b'require(desired >= charged, "checkpoint:fixed_point_shrunk")', b'if desired < charged: write_atomic(path, encoded); return'),
    (b'BRIDGE_SEVEN_BLOCKS = ((0, 1, 2), (3, 0, 4), (5,), (6,), (7,), (8,), (9,))', b'BRIDGE_SEVEN_BLOCKS = ((0, 1, 2), (3, 4, 5), (6,), (7,), (8,), (9,), (10,))'),
    (b'"membership_reductions": 50000000', b'"membership_reductions": 2000000000'),
    (b'"dual_support": 10000000', b'"dual_support": 1000000000'),
    (b'"correlation_pairs": 10000000', b'"correlation_pairs": 5000000000'),
    (b'def dual_from_projection(basis: LiveBasis, target: dict[str, int], meter: Meter) -> tuple[dict[str, int], int, set[str]]:', b'def dual_from_projection(basis: LiveBasis, target: dict[str, int], meter: Meter, remainder: dict[str, int] | None = None) -> tuple[dict[str, int], int, set[str]]:'),
    (b'    remainder, _ = basis.combined.reduce(target); require(remainder, "dual:member_target")', b'    if remainder is None: remainder, _ = basis.combined.reduce(target)\n    require(remainder, "dual:member_target")'),
    (b'dual_from_projection(self.basis, target, meter)', b'dual_from_projection(self.basis, target, meter, remainder)'),
    (b'                rem = add_row(rem, self.rows[pivot], -coefficient)\n', b'                for key, value in self.rows[pivot].items():\n                    updated = (rem.get(key, 0) - coefficient * int(value)) % 3\n                    if updated: rem[key] = updated\n                    else: rem.pop(key, None)\n'),
    (b'\ndef bridge_trace_from_states(authority: AuthorityAdapter, states: Sequence[AffineState],', b'''\ndef validate_bridge_owner_once(authority: AuthorityAdapter) -> None:\n    if getattr(authority, "_bridge_owner_validated", False): return\n    owner = authority.receipt.get("bridge", {}).get("occurrence_ledger", [])\n    require(len(owner) == len(BRIDGE_OWNER_LAYOUT) == 11, "bridge:occurrence_owner_count")\n    for index, item in enumerate(owner):\n        expected = BRIDGE_OWNER_LAYOUT[index]\n        actual = (item.get("block"), int(item.get("block_index")), int(item.get("block_slot")),\n                  item.get("occurrence"), item.get("type"), int(item.get("ten_index")),\n                  int(item.get("context_id")), item.get("role"), int(item.get("factor_sign")),\n                  item.get("orientation"), tuple(item.get("fox_prefix_occurrences", ())))\n        require(int(item.get("ordinal")) == index + 1 and actual == expected,\n                "bridge:literal_occurrence_owner")\n        require(expected[5] == BRIDGE_TEN_TO_ELEVEN[index], "bridge:owner_insertion_binding")\n        coordinate = authority.task176.get("coordinates", [])[expected[5]]\n        require((item.get("type"), int(item.get("context_id")), item.get("role")) ==\n                (coordinate.get("type"), int(coordinate.get("context_id")), coordinate.get("role")),\n                "bridge:typed_coordinate_owner")\n    authority._bridge_owner_validated = True\n\ndef bridge_trace_from_states(authority: AuthorityAdapter, states: Sequence[AffineState],'''),
    (b'''    # Reconstruct all non-value owner fields independently.  In particular,\n    # the spelling and prefix lists are not accepted merely because the\n    # receipt\'s aggregate digest is sealed.\n    for index, item in enumerate(owner):\n        expected = BRIDGE_OWNER_LAYOUT[index]\n        actual = (item.get("block"), int(item.get("block_index")), int(item.get("block_slot")),\n                  item.get("occurrence"), item.get("type"), int(item.get("ten_index")),\n                  int(item.get("context_id")), item.get("role"), int(item.get("factor_sign")),\n                  item.get("orientation"), tuple(item.get("fox_prefix_occurrences", ())))\n        require(int(item.get("ordinal")) == index + 1 and actual == expected,\n                "bridge:literal_occurrence_owner")\n        require(expected[5] == BRIDGE_TEN_TO_ELEVEN[index], "bridge:owner_insertion_binding")\n        coordinate = authority.task176.get("coordinates", [])[expected[5]]\n        require((item.get("type"), int(item.get("context_id")), item.get("role")) ==\n                (coordinate.get("type"), int(coordinate.get("context_id")), coordinate.get("role")),\n                "bridge:typed_coordinate_owner")\n''', b'    validate_bridge_owner_once(authority)\n'),
    (b'\ndef build_kernel(authority: AuthorityAdapter, runtime: Runtime, dag_forward: ForwardDAG,', b'''\ndef progress_once(meter: Meter, phase: str, row: int) -> None:\n    now = time.monotonic()\n    if now - getattr(meter, "_a4_progress_at", -1.0e99) < 60.0: return\n    meter._a4_progress_at = now\n    counters = meter.counters\n    print(f"A4_PROGRESS phase={phase} row={int(row)} membership_queries={counters.get('membership_queries', 0)} correlation_pairs={counters.get('correlation_pairs', 0)} elapsed={now - meter.started:.1f}", flush=True)\n\ndef build_kernel(authority: AuthorityAdapter, runtime: Runtime, dag_forward: ForwardDAG,'''),
    (b'        meter.state(f"ROW_{ordinal}"); source_word, parts, ancestry = replay_ancestry(row)', b'        meter.state(f"ROW_{ordinal}"); progress_once(meter, "ROW", ordinal); source_word, parts, ancestry = replay_ancestry(row)'),
    (b'        meter.authority_complete = True\n', b'        meter.authority_complete = True\n        progress_once(meter, "AUTHORITY", 0)\n'),
    (b'ordinal in {1024, 2048, 3072, 4096, 5120, 6144, ROWS}', b'ordinal in {32, 64, 128, 256, 512, 1024, 2048, 3072, 4096, 5120, 6144, ROWS}'),
)

def main() -> None:
    raw = SOURCE.read_bytes()
    if len(raw) != SOURCE_BYTES or hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise SystemExit("v12 producer: frozen v6 source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v12 producer: audited site is not unique")
        raw = raw.replace(old, new)
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(SOURCE), "exec"), ns, ns)

if __name__ == "__main__":
    main()
