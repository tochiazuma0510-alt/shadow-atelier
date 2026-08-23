#!/usr/bin/env python3
"""P2-first frozen execution layer for the fixed-row36 bridge.

V3 preserves the v2 preregistration as a superseded preflight, retains the
literal status gate expected by the base runner, evaluates onto on every row,
and caches exact factor closures.  No mathematical universe is changed.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter
from pathlib import Path
from typing import Any, Sequence

import d972_row36_pent_bridge_common_v1 as base
import d972_row36_pent_bridge_common_v2 as v2


def install(prime: int, out_dir: str | None) -> None:
    v2.install(prime, out_dir)
    build_raw_v2 = base.build_raw_universe
    execute_v2 = base.execute
    build_manifest_v2 = base.build_manifest
    component_cache: dict[str, dict[Any, int]] = {
        "G36": {}, "PSL2_8": {}, "Qp": {}
    }

    def source_pins(_: int) -> list[dict[str, Any]]:
        return [
            base.file_pin("search/d972_row36_pent_bridge_common_v1.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v2.py"),
            base.file_pin("search/d972_row36_pent_bridge_common_v3.py"),
            base.file_pin(f"search/d972_row36_pent_bridge_p{prime}_producer_v3.py"),
        ]

    def paths_for(_: int) -> dict[str, str]:
        prefix = Path(out_dir).as_posix().rstrip("/") if out_dir else "search/certs"
        return {
            "prereg": f"search/certs/d972_row36_pent_bridge_p{prime}_prereg_v3_{base.DATE}.json",
            "receipt": f"{prefix}/d972_row36_pent_bridge_p{prime}_receipt_v3_{base.DATE}.json",
            "manifest": f"{prefix}/d972_row36_pent_bridge_p{prime}_manifest_v3_{base.DATE}.json",
        }

    def build_raw(prime_arg: int, receipt: dict[str, Any]):
        prereg, runtime = build_raw_v2(prime_arg, receipt)
        prereg["schema"] = f"d972-row36-pent-bridge-p{prime_arg}-prereg/v3"
        prereg["source_pins"] = source_pins(prime_arg)
        prereg["execution_routing"] = {
            "local_failed_attempts": [
                {"timeout_seconds": 120, "last_marker": "COLLECTORS_START",
                 "classification": "generic rank-26 Python inverse expansion resource trap; no prereg emitted"},
                {"timeout_seconds": 180, "last_marker": "COLLECTORS_PASS",
                 "classification": "generic rank-26 Python A.18 replay resource trap; no prereg emitted"},
            ],
            "superseded_preregs": [
                "search/certs/d972_row36_pent_bridge_p2_prereg_v1_20260824.json",
                "search/certs/d972_row36_pent_bridge_p2_prereg_v2_20260824.json",
            ] if prime_arg == 2 else [],
            "prepare": "bind immutable canary receipt/verdict and its exported A.18 10/10 gate; no quotient rerun",
            "execute": "direct same-signed-word Q4 evaluation with exported pc tables and explicit inverse marked coordinates",
            "route": "GHA gap-run launcher invoking bounded Python producer",
        }
        prereg["complete_predicate_rule"] = {
            "both_hexagons_every_row": True,
            "charming_every_row": True,
            "onto_full_joint_every_row": True,
            "literal_Dpap_every_row_same_word": True,
            "sequential_rejection_reason_also_recorded": True,
        }
        # Retain the literal fail-closed status required by the inherited runner.
        prereg["status"] = "PREREGISTERED_BEFORE_ROW_PREDICATE_OUTCOME"
        prereg["terminal_token"] = f"PENT159O_ROW36_P{prime_arg}_PREREG_V3_FROZEN"
        return prereg, runtime

    def cached_component_orders(word_a: Sequence[int], word_b: Sequence[int],
                                qcol: base.PcCollector,
                                qmarks: Sequence[bytes]) -> dict[str, int]:
        ga, gb = base.eval_word_g(word_a, 36), base.eval_word_g(word_b, 36)
        pa, pb = base.eval_word_perm(word_a), base.eval_word_perm(word_b)
        qa, qb = qcol.eval(word_a, qmarks), qcol.eval(word_b, qmarks)
        gkey = (ga, gb)
        pkey = (pa, pb)
        qkey = (qa, qb)
        if gkey not in component_cache["G36"]:
            component_cache["G36"][gkey] = len(base.g_closure((ga, gb), 36))
        if pkey not in component_cache["PSL2_8"]:
            component_cache["PSL2_8"][pkey] = len(base.perm_closure((pa, pb)))
        if qkey not in component_cache["Qp"]:
            component_cache["Qp"][qkey] = len(base.q_closure(qcol, (qa, qb)))
        return {name: component_cache[name][key]
                for name, key in (("G36", gkey), ("PSL2_8", pkey), ("Qp", qkey))}

    def abelianization_gate(prime_arg: int, qcol: base.PcCollector,
                            qmarks: Sequence[bytes]) -> dict[str, Any]:
        qmod = prime_arg * prime_arg
        add4 = lambda a, b: ((a[0] + b[0]) % 4, (a[1] + b[1]) % 4)
        # finite_marked_map uses one operation for source and target, so the
        # heterogeneous G36/additive target is replayed explicitly here.
        gmap = {base.gid(): (0, 0)}
        queue = base.deque([base.gid()])
        source_steps = (base.gx(36), base.ginv(base.gx(36), 36),
                        base.gy(36), base.ginv(base.gy(36), 36))
        target_steps = ((1, 0), (3, 0), (0, 1), (0, 3))
        while queue:
            current = queue.popleft()
            for source_step, target_step in zip(source_steps, target_steps):
                nxt = base.gmul(current, source_step, 36)
                image = add4(gmap[current], target_step)
                if nxt in gmap:
                    base.require(gmap[nxt] == image, "G36_ABELIAN_MAP_DESCENT")
                else:
                    gmap[nxt] = image
                    queue.append(nxt)
        base.require(len(gmap) == 23328 and len(set(gmap.values())) == 16,
                     "G36_ABELIAN_MAP_COVER")

        addq = lambda a, b: ((a[0] + b[0]) % qmod, (a[1] + b[1]) % qmod)
        qtarget_steps = ((1, 0), ((-1) % qmod, 0),
                         (0, 1), (0, (-1) % qmod))
        qsource_steps = (qmarks[0], qcol.inverse(qmarks[0]),
                         qmarks[1], qcol.inverse(qmarks[1]))
        qmap = {qcol.one(): (0, 0)}
        qqueue = base.deque([qcol.one()])
        while qqueue:
            current = qqueue.popleft()
            for source_step, target_step in zip(qsource_steps, qtarget_steps):
                nxt = qcol.mul(current, source_step)
                image = addq(qmap[current], target_step)
                if nxt in qmap:
                    base.require(qmap[nxt] == image, "QP_ABELIAN_MAP_DESCENT")
                else:
                    qmap[nxt] = image
                    qqueue.append(nxt)
        expected_q = 128 if prime_arg == 2 else 2187
        base.require(len(qmap) == expected_q and len(set(qmap.values())) == qmod * qmod,
                     "QP_ABELIAN_MAP_COVER")
        modulus = 4 if prime_arg == 2 else 36
        return {
            "G36_complete_marked_abelian_map": {"target": "C4xC4",
                                                 "source_order": len(gmap),
                                                 "image_order": len(set(gmap.values()))},
            "Qp_complete_marked_abelian_map": {"target": f"C{qmod}xC{qmod}",
                                                "source_order": len(qmap),
                                                "image_order": len(set(qmap.values()))},
            "joint_abelianization": f"C{modulus}xC{modulus}",
            "charming_exponent_sum_modulus": modulus,
            "p2_exactness": "both marked abelianizations are C4xC4; the C2 fibre product has no larger marked common quotient",
            "p3_exactness": "CRT combines C4xC4 and C9xC9 into C36xC36; PSL(2,8) is perfect",
        }

    def execute(prime_arg: int, prereg_pin: dict[str, Any], prereg: dict[str, Any],
                runtime: dict[str, Any], input_pins: list[dict[str, Any]]):
        base.component_orders = cached_component_orders
        receipt, extra = execute_v2(prime_arg, prereg_pin, prereg, runtime, input_pins)
        qcol: base.PcCollector = runtime["qcol"]
        qmarks: Sequence[bytes] = runtime["qmarks"]
        rows = receipt["predicate_ledger"]["complete_rows"]
        expected_components = {"G36": 23328, "PSL2_8": 504,
                               "Qp": 128 if prime_arg == 2 else 2187}
        sequential = Counter(raw_count=0, unit_pass=0, charming_pass=0,
                             hexagon_310_pass=0, hexagon_311_pass=0, onto_pass=0)
        reasons: Counter[str] = Counter()
        survivors = []
        for row in rows:
            word = tuple(row["canonical_signed_source_word"])
            u = int(row["u_2m_plus_1"])
            gen_a = base.group_power_word(1, u)
            gen_b = base.reduce_word(word + base.group_power_word(2, u) +
                                     base.inverse_word(word))
            orders = cached_component_orders(gen_a, gen_b, qcol, qmarks)
            onto = orders == expected_components
            reason = base.reason_for(row["unit_mod_36"], row["charming"],
                                     row["literal_gentle_hexagon_310"],
                                     row["literal_gentle_hexagon_311"], onto)
            row["onto_component_generated_orders"] = orders
            row["onto_full_joint_quotient"] = onto
            row["onto"] = onto
            row["onto_evaluated_despite_earlier_gate_failure"] = True
            row["rejection_reason"] = reason
            row["passed"] = reason == "pass"
            sequential["raw_count"] += 1
            if row["unit_mod_36"]:
                sequential["unit_pass"] += 1
                if row["charming"]:
                    sequential["charming_pass"] += 1
                    if row["literal_gentle_hexagon_310"]:
                        sequential["hexagon_310_pass"] += 1
                        if row["literal_gentle_hexagon_311"]:
                            sequential["hexagon_311_pass"] += 1
                            if onto:
                                sequential["onto_pass"] += 1
            reasons[reason] += 1
            if row["passed"]:
                survivors.append({"row_id": row["row_id"], "m": row["m"],
                                  "L_code": row["L_code"],
                                  "hall_vector_abedh": row["hall_vector_abedh"],
                                  "word_sha256": row["word_sha256"],
                                  "Dpap_coords": row["literal_Dpap_coords"],
                                  "Dpap_sha256": row["literal_Dpap_sha256"]})
        expected = 64 if prime_arg == 2 else 34992
        base.require(len(rows) == expected and sequential["raw_count"] == expected,
                     "V3_COMPLETE_ONTO_ROW_COVER")
        ledger = receipt["predicate_ledger"]
        ledger["onto_evaluated_for_every_materialized_row"] = True
        ledger["sequential_counts"] = dict(sequential)
        ledger["rejection_reason_counts"] = dict(sorted(reasons.items()))
        ledger["actual_survivor_count"] = len(survivors)
        ledger["actual_survivor_roster"] = survivors
        ledger["actual_survivor_roster_sha256"] = base.digest(survivors)
        ledger["complete_rows_sha256"] = base.digest(rows)
        receipt["claim_cover_pent_canary_2"]["evaluated_row_ledger_sha256"] = base.digest(rows)
        aggregate = {
            "row_ledger_sha256": base.digest(rows),
            "reason_ledger": dict(sorted(reasons.items())),
            "defect_histogram": ledger["defect_histogram"],
            "actual_survivor_roster_sha256": base.digest(survivors),
            "sequential_counts": dict(sequential),
        }
        receipt["aggregate_payload"] = aggregate
        receipt["aggregate_sha256"] = base.digest(aggregate)
        receipt["destructive_controls"] = base.destructive_controls(
            prime_arg, prereg, rows,
            {"aggregate_payload": aggregate, "aggregate_sha256": base.digest(aggregate)})
        receipt["collector_and_map_gates"]["abelianization_exactness"] = \
            abelianization_gate(prime_arg, qcol, qmarks)
        receipt["onto_cache_accounting"] = {
            name: {"distinct_generator_pairs": len(cache)}
            for name, cache in component_cache.items()
        }
        receipt["schema"] = f"d972-row36-pent-bridge-p{prime_arg}-receipt/v3"
        receipt["source_pins"] = source_pins(prime_arg)
        receipt["terminal_token"] = f"PENT159O_ROW36_P{prime_arg}_PRODUCER_V3_CANDIDATE__CHECKER_REQUIRED"
        return receipt, extra

    def build_manifest(prime_arg: int, prereg_pin: dict[str, Any], receipt_pin: dict[str, Any]):
        manifest = build_manifest_v2(prime_arg, prereg_pin, receipt_pin)
        manifest["schema"] = f"d972-row36-pent-bridge-p{prime_arg}-manifest/v3"
        manifest["source_pins"] = source_pins(prime_arg)
        manifest["execution"]["local_command_prepare"] = f"python search/d972_row36_pent_bridge_p{prime_arg}_producer_v3.py prepare"
        manifest["execution"]["GHA_command"] = f"python3 search/d972_row36_pent_bridge_p{prime_arg}_producer_v3.py execute --out-dir ci/out"
        manifest["terminal_token"] = f"PENT159O_ROW36_P{prime_arg}_MANIFEST_V3_FROZEN"
        return manifest

    base.source_pins = source_pins
    base.paths_for = paths_for
    base.build_raw_universe = build_raw
    base.component_orders = cached_component_orders
    base.execute = execute
    base.build_manifest = build_manifest


def main_for_prime(prime: int) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("prepare", "execute"))
    parser.add_argument("--out-dir")
    args = parser.parse_args()
    if args.phase == "prepare":
        base.require(args.out_dir is None, "PREPARE_OUT_DIR_FORBIDDEN")
    else:
        base.require(args.out_dir is not None, "EXECUTE_OUT_DIR_REQUIRED")
        rel = Path(args.out_dir)
        base.require(not rel.is_absolute() and ".." not in rel.parts,
                     "EXECUTE_OUT_DIR_UNSAFE", args.out_dir)
    install(prime, args.out_dir)
    raise SystemExit(base.run(prime, [args.phase]))
