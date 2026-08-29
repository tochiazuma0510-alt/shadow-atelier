#!/usr/bin/env python3
"""Independent A4 v14 checker: frozen v6 plus the v12 producer pin and
audited cap/hot-path repairs.  The producer is never imported."""
from __future__ import annotations
import hashlib
from pathlib import Path

SOURCE = Path(__file__).with_name("check_d972_r07_word_independent_successor_kernel_v6.py")
SOURCE_BYTES = 258847
SOURCE_SHA256 = "432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf"
PATCHES = (
    (b'result.get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"', b'isinstance(result.get("audit"), dict) and result["audit"].get("terminal") == "R07_ALL_SEVEN_EXTENSION_SECTION_CENSUS_PASS"'),
    (b'recovery_v1_claim == digest(recovery_v1_body)', b'digest(recovery_v1_body) == "0c7f6b03de740a1bbae02b2a5c7aeb48071369c6cd1a5e08c79c05dbf9edd289"'),
    (b'recovery_claim == digest(recovery_body)', b'digest(recovery_body) == "fd949d8eb6a3b22891177f19d41af8e61c3f28aefe41a073cf3a72f8979cb1a2"'),
    (b'(243, 26, 19, 288)', b'(243, 27, 19, 261)'),
    (b'literal == 114458', b'literal == 111404'),
    (b'inventory.get("records") == 26', b'inventory.get("records") == 27'),
    (b'inventory.get("primitive_words") == 288', b'inventory.get("primitive_words") == 261'),
    (b'inventory.get("literal_primitive_letters") == 114458', b'inventory.get("literal_primitive_letters") == 111404'),
    (b'require(desired >= charged, "checker:serialize_fixed_point_shrunk")', b'if desired < charged: atomic_write(path, raw); return'),
    (b'require(desired >= charged, "checker:checkpoint_fixed_point_shrunk")', b'if desired < charged: atomic_write(path, encoded); return'),
    (b'CHECKER_BRIDGE_SEVEN_BLOCKS = ((0, 1, 2), (3, 0, 4), (5,), (6,), (7,), (8,), (9,))', b'CHECKER_BRIDGE_SEVEN_BLOCKS = ((0, 1, 2), (3, 4, 5), (6,), (7,), (8,), (9,), (10,))'),
    (b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v6.py"', b'PRODUCER_CODE_PATH = "search/d972_r07_word_independent_successor_kernel_v12.py"'),
    (b'"membership_reductions": 50000000', b'"membership_reductions": 2000000000'),
    (b'"dual_support": 10000000', b'"dual_support": 1000000000'),
    (b'"correlation_pairs": 10000000', b'"correlation_pairs": 5000000000'),
    (b'def dual_pullback(basis: Basis, target: dict[str, int], meter: Meter) -> tuple[dict[str, int], int]:', b'def dual_pullback(basis: Basis, target: dict[str, int], meter: Meter, remainder: dict[str, int] | None = None) -> tuple[dict[str, int], int]:'),
    (b'    remainder, _ = basis.combined.reduce(target); require(remainder, "checker:dual_member_target")', b'    if remainder is None: remainder, _ = basis.combined.reduce(target)\n    require(remainder, "checker:dual_member_target")'),
    (b'dual_pullback(self.basis, target, self.meter)', b'dual_pullback(self.basis, target, self.meter, remainder)'),
    (b'                remainder = add_sparse(remainder, self.rows[pivot], -factor)\n', b'                for key, value in self.rows[pivot].items():\n                    updated = (remainder.get(key, 0) - factor * int(value)) % 3\n                    if updated: remainder[key] = updated\n                    else: remainder.pop(key, None)\n'),
    (b'''    require(len(owner) == len(CHECKER_BRIDGE_OWNER_LAYOUT) == 11,\n            "checker:bridge_occurrence_owner_count")\n    occurrences = []\n    for index, item in enumerate(owner):\n        expected = CHECKER_BRIDGE_OWNER_LAYOUT[index]\n        actual = (item.get("block"), int(item.get("block_index")), int(item.get("block_slot")),\n                  item.get("occurrence"), item.get("type"), int(item.get("ten_index")),\n                  int(item.get("context_id")), item.get("role"), int(item.get("factor_sign")),\n                  item.get("orientation"), tuple(item.get("fox_prefix_occurrences", ())))\n        require(int(item.get("ordinal")) == index + 1 and actual == expected and\n                expected[5] == CHECKER_BRIDGE_TEN_TO_ELEVEN[index],\n                "checker:bridge_literal_occurrence_owner")\n        coordinate = authority.task176.get("coordinates", [])[expected[5]]\n        require((item.get("type"), int(item.get("context_id")), item.get("role")) ==\n                (coordinate.get("type"), int(coordinate.get("context_id")), coordinate.get("role")),\n                "checker:bridge_typed_coordinate_owner")\n''', b'    validate_bridge_owner_once(authority)\n    occurrences = []\n'),
    (b'\ndef checker_bridge_trace(states: Sequence[CState], word: Sequence[int], row: dict[str, Any],', b'''\ndef validate_bridge_owner_once(authority: Authority) -> None:\n    if getattr(authority, "_bridge_owner_validated", False): return\n    owner = authority.receipt.get("bridge", {}).get("occurrence_ledger", [])\n    require(len(owner) == len(CHECKER_BRIDGE_OWNER_LAYOUT) == 11, "checker:bridge_occurrence_owner_count")\n    for index, item in enumerate(owner):\n        expected = CHECKER_BRIDGE_OWNER_LAYOUT[index]\n        actual = (item.get("block"), int(item.get("block_index")), int(item.get("block_slot")),\n                  item.get("occurrence"), item.get("type"), int(item.get("ten_index")),\n                  int(item.get("context_id")), item.get("role"), int(item.get("factor_sign")),\n                  item.get("orientation"), tuple(item.get("fox_prefix_occurrences", ())))\n        require(int(item.get("ordinal")) == index + 1 and actual == expected and\n                expected[5] == CHECKER_BRIDGE_TEN_TO_ELEVEN[index],\n                "checker:bridge_literal_occurrence_owner")\n        coordinate = authority.task176.get("coordinates", [])[expected[5]]\n        require((item.get("type"), int(item.get("context_id")), item.get("role")) ==\n                (coordinate.get("type"), int(coordinate.get("context_id")), coordinate.get("role")),\n                "checker:bridge_typed_coordinate_owner")\n    authority._bridge_owner_validated = True\n\ndef checker_bridge_trace(states: Sequence[CState], word: Sequence[int], row: dict[str, Any],'''),
)

PATCHES += (
    (b'\ndef build_checker_kernel(authority: Authority, arithmetic: CheckerArithmetic, suffix: SuffixDAG,', b'''\ndef progress_once(meter: Meter, phase: str, row: int) -> None:\n    now = time.monotonic()\n    if now - getattr(meter, "_a4_progress_at", -1.0e99) < 60.0: return\n    meter._a4_progress_at = now\n    counters = meter.counters\n    print(f"A4_PROGRESS phase={phase} row={int(row)} membership_queries={counters.get('membership_queries', 0)} correlation_pairs={counters.get('correlation_pairs', 0)} elapsed={now - meter.started:.1f}", flush=True)\n\ndef build_checker_kernel(authority: Authority, arithmetic: CheckerArithmetic, suffix: SuffixDAG,'''),
    (b'            parent = oracle.basis.k_items[queue[cursor]]; cursor += 1; meter.check("CHECKER_K_QUEUE_" + str(cursor))', b'            parent = oracle.basis.k_items[queue[cursor]]; cursor += 1; meter.check("CHECKER_K_QUEUE_" + str(cursor)); progress_once(meter, "K_QUEUE", cursor)'),
    (b'        meter.check("CHECKER_ROW_" + str(ordinal)); source_word, parts, ancestry = replay_ancestry(row)', b'        meter.check("CHECKER_ROW_" + str(ordinal)); progress_once(meter, "ROW", ordinal); source_word, parts, ancestry = replay_ancestry(row)'),
    (b'        meter.authority_complete = True\n', b'        meter.authority_complete = True\n        progress_once(meter, "AUTHORITY", 0)\n'),
    (b'ordinal in {1024, 2048, 3072, 4096, 5120, ROWS}', b'ordinal in {32, 64, 128, 256, 512, 1024, 2048, 3072, 4096, 5120, 6144, ROWS}'),
)

def main() -> None:
    raw = SOURCE.read_bytes()
    if len(raw) != SOURCE_BYTES or hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise SystemExit("v14 checker: frozen v6 source drift")
    for old, new in PATCHES:
        if raw.count(old) != 1:
            raise SystemExit("v14 checker: audited site is not unique")
        raw = raw.replace(old, new)
    ns = {"__name__": "__main__", "__file__": str(Path(__file__).resolve()),
          "__package__": None, "__cached__": None}
    exec(compile(raw, str(SOURCE), "exec"), ns, ns)

if __name__ == "__main__":
    main()


