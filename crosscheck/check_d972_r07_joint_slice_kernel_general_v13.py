#!/usr/bin/env python3
"""Independent polynomial checker for the v13 joint-slice certificate.

The checker reads the same immutable v11 bytes as the producer, but it has a
separate bottom-pivot/tableau implementation.  It never imports producer code
or uses producer pivots, ancestry, ranks, terminals, or mutation Booleans as
mathematical evidence.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "d972-r07-joint-slice-kernel-general/v13"
SELF_SCHEMA = VERSION + "/selftest"
SOURCE_REL = "search/certs/d972_r07_joint_slice_kernel_general_selftest_v11_20260828.json"
SOURCE_SCHEMA = "d972-r07-joint-slice-kernel-general/v11/selftest"
SOURCE_SEAL = "literal-static-fixture-v11"
SOURCE_BYTES = 12964
SOURCE_SHA256 = "cab24a5e6ddd7812094b920bffd7688564092a3c9b718484bf3f887cf59d2058"
PASS = "R07_JOINT_SLICE_KERNEL_GENERAL_V13_CHECKER_SELFTEST_PASS"
STATIC = "STATIC_BLOCKED:actual typed matrices are not staged"

OWNERS = (
    "field_modulus", "theta_seed", "theta_action", "z_action",
    "eta_action", "D_entry", "O_entry", "C_entry", "action_order",
    "premature_C", "target", "seed_index", "parent", "row_theta",
    "left_kernel", "Hd1", "member_ancestry", "dual", "terminal",
    "production_input", "closure_queue_pops", "context_pops",
    "closure_candidate_count", "closure_queue_bound", "candidate_parent",
    "candidate_action", "candidate_decision", "candidate_normalization",
    "candidate_coefficients", "candidate_rank", "dependent_record_deletion",
    "dependent_record_reorder", "f3_plus3_coefficient",
    "member_witness_equality", "a4_anchor_identity", "anchor_least_index",
    "anchor_projected_exponent", "anchor_inverse_scalar",
    "anchor_substituted_cube", "anchor_word", "anchor_rho0",
    "anchor_rho1_kernel", "anchor_q_z0", "base_pair_order",
)

MUTATION_REGISTRY = {
    "field_modulus": {"scope": "raw_case", "case_index": 1, "stage": "raw.field_modulus", "code": "M_FIELD_MODULUS", "reason": "field modulus is not F3"},
    "theta_seed": {"scope": "raw_case", "case_index": 1, "stage": "raw.theta_seed", "code": "M_THETA_SEED", "reason": "theta seed binding changed"},
    "theta_action": {"scope": "raw_case", "case_index": 1, "stage": "raw.theta_action", "code": "M_THETA_ACTION", "reason": "theta action owner changed"},
    "z_action": {"scope": "raw_case", "case_index": 1, "stage": "raw.z_action", "code": "M_Z_ACTION", "reason": "z action owner changed"},
    "eta_action": {"scope": "raw_case", "case_index": 1, "stage": "raw.eta_action", "code": "M_ETA_ACTION", "reason": "eta action owner changed"},
    "D_entry": {"scope": "raw_case", "case_index": 1, "stage": "raw.D_entry", "code": "M_D_ENTRY", "reason": "D map owner changed"},
    "O_entry": {"scope": "raw_case", "case_index": 1, "stage": "raw.O_entry", "code": "M_O_ENTRY", "reason": "O map owner changed"},
    "C_entry": {"scope": "raw_case", "case_index": 1, "stage": "raw.C_entry", "code": "M_C_ENTRY", "reason": "C map owner changed"},
    "action_order": {"scope": "raw_case", "case_index": 1, "stage": "raw.action_order", "code": "M_ACTION_ORDER", "reason": "action order binding changed"},
    "premature_C": {"scope": "raw_case", "case_index": 1, "stage": "raw.premature_C", "code": "M_PREMATURE_C", "reason": "C was applied before closure"},
    "target": {"scope": "raw_case", "case_index": 1, "stage": "raw.target", "code": "M_TARGET", "reason": "target membership changed"},
    "seed_index": {"scope": "certificate", "case_index": 0, "stage": "certificate.seed_index", "code": "M_SEED_INDEX", "reason": "certificate seed index is invalid"},
    "parent": {"scope": "certificate", "case_index": 4, "stage": "certificate.parent", "code": "M_PARENT", "reason": "certificate parent is invalid"},
    "row_theta": {"scope": "certificate", "case_index": 0, "stage": "certificate.row_theta", "code": "M_ROW_THETA", "reason": "certificate row theta does not replay"},
    "left_kernel": {"scope": "certificate", "case_index": 0, "stage": "certificate.left_kernel", "code": "M_LEFT_KERNEL", "reason": "left-kernel basis content changed"},
    "Hd1": {"scope": "certificate", "case_index": 1, "stage": "certificate.Hd1", "code": "M_HD1", "reason": "Hd1 content changed"},
    "member_ancestry": {"scope": "certificate", "case_index": 0, "stage": "certificate.member_ancestry", "code": "M_MEMBER_ANCESTRY", "reason": "member theta ancestry does not replay"},
    "dual": {"scope": "certificate", "case_index": 1, "stage": "certificate.dual", "code": "M_DUAL", "reason": "separating dual does not replay"},
    "terminal": {"scope": "certificate", "case_index": 1, "stage": "certificate.terminal", "code": "M_TERMINAL", "reason": "certificate terminal changed"},
    "production_input": {"scope": "wrapper", "case_index": 0, "stage": "wrapper.production_input", "code": "M_PRODUCTION_INPUT", "reason": "production input binding changed"},
    "closure_queue_pops": {"scope": "certificate", "case_index": 0, "stage": "certificate.closure_queue_pops", "code": "M_CLOSURE_QUEUE_POPS", "reason": "closure queue pop count changed"},
    "context_pops": {"scope": "certificate", "case_index": 0, "stage": "certificate.context_pops", "code": "M_CONTEXT_POPS", "reason": "context pop receipt changed"},
    "closure_candidate_count": {"scope": "certificate", "case_index": 0, "stage": "certificate.closure_candidate_count", "code": "M_CLOSURE_CANDIDATE_COUNT", "reason": "closure candidate count changed"},
    "closure_queue_bound": {"scope": "certificate", "case_index": 0, "stage": "certificate.closure_queue_bound", "code": "M_CLOSURE_QUEUE_BOUND", "reason": "closure queue bound changed"},
    "candidate_parent": {"scope": "certificate", "case_index": 0, "stage": "certificate.candidate_parent", "code": "M_CANDIDATE_PARENT", "reason": "candidate parent changed"},
    "candidate_action": {"scope": "certificate", "case_index": 0, "stage": "certificate.candidate_action", "code": "M_CANDIDATE_ACTION", "reason": "candidate action changed"},
    "candidate_decision": {"scope": "certificate", "case_index": 0, "stage": "certificate.candidate_decision", "code": "M_CANDIDATE_DECISION", "reason": "candidate decision changed"},
    "candidate_normalization": {"scope": "certificate", "case_index": 0, "stage": "certificate.candidate_normalization", "code": "M_CANDIDATE_NORMALIZATION", "reason": "candidate normalization changed"},
    "candidate_coefficients": {"scope": "certificate", "case_index": 0, "stage": "certificate.candidate_coefficients", "code": "M_CANDIDATE_COEFFICIENTS", "reason": "candidate coefficients changed"},
    "candidate_rank": {"scope": "certificate", "case_index": 0, "stage": "certificate.candidate_rank", "code": "M_CANDIDATE_RANK", "reason": "candidate rank changed"},
    "dependent_record_deletion": {"scope": "certificate", "case_index": 0, "stage": "certificate.dependent_record_deletion", "code": "M_DEPENDENT_RECORD_DELETION", "reason": "dependent candidate record deleted"},
    "dependent_record_reorder": {"scope": "certificate", "case_index": 0, "stage": "certificate.dependent_record_reorder", "code": "M_DEPENDENT_RECORD_REORDER", "reason": "dependent candidate records reordered"},
    "f3_plus3_coefficient": {"scope": "certificate", "case_index": 0, "stage": "certificate.f3_plus3_coefficient", "code": "M_F3_PLUS3_COEFFICIENT", "reason": "coefficient is outside canonical F3"},
    "member_witness_equality": {"scope": "certificate", "case_index": 0, "stage": "certificate.member_witness_equality", "code": "M_MEMBER_WITNESS_EQUALITY", "reason": "member witness does not map to the target slice"},
    "a4_anchor_identity": {"scope": "anchor", "case_index": 0, "stage": "production.anchor.identity", "code": "M_A4_ANCHOR_IDENTITY", "reason": "A4 anchor receipt identity changed"},
    "anchor_least_index": {"scope": "anchor", "case_index": 0, "stage": "production.anchor.least_index", "code": "M_ANCHOR_LEAST_INDEX", "reason": "A4 anchor least index changed"},
    "anchor_projected_exponent": {"scope": "anchor", "case_index": 0, "stage": "production.anchor.projected_exponent", "code": "M_ANCHOR_PROJECTED_EXPONENT", "reason": "A4 projected exponent changed"},
    "anchor_inverse_scalar": {"scope": "anchor", "case_index": 0, "stage": "production.anchor.inverse_scalar", "code": "M_ANCHOR_INVERSE_SCALAR", "reason": "A4 inverse scalar changed"},
    "anchor_substituted_cube": {"scope": "anchor", "case_index": 0, "stage": "production.anchor.forbidden_cube", "code": "M_ANCHOR_SUBSTITUTED_CUBE", "reason": "superseded literal cube pair was supplied"},
    "anchor_word": {"scope": "anchor", "case_index": 0, "stage": "production.anchor.word", "code": "M_ANCHOR_WORD", "reason": "A4 anchor word changed"},
    "anchor_rho1_kernel": {"scope": "anchor", "case_index": 0, "stage": "production.anchor.rho1_kernel", "code": "M_ANCHOR_RHO1_KERNEL", "reason": "A4 anchor rho1 is not in K"},
    "anchor_rho0": {"scope": "anchor", "case_index": 0, "stage": "production.anchor.rho0", "code": "M_ANCHOR_RHO0", "reason": "A4 anchor rho0 replay failed"},
    "anchor_q_z0": {"scope": "anchor", "case_index": 0, "stage": "production.anchor.q_z0", "code": "M_ANCHOR_Q_Z0", "reason": "A4 anchor q value is not z0"},
    "base_pair_order": {"scope": "anchor", "case_index": 0, "stage": "production.anchor.base_pair_order", "code": "M_BASE_PAIR_ORDER", "reason": "corrected base-pair order changed"},
}

ANCHOR_CONTRACT = {
    "package": "r07-a4-anchored-relative-ideal-lift/v247",
    "required": True,
    "anchor_receipt_identity": "A4_ANCHOR_RECEIPT_REQUIRED",
    "least_index": "A4_REQUIRED_LEAST_INDEX",
    "projected_exponent": "A4_REQUIRED_PROJECTED_EXPONENT",
    "inverse_scalar": "A4_REQUIRED_INVERSE_SCALAR",
    "anchor_word": "u_z_REQUIRED_SOURCE_WORD",
    "literal_word": "u_z_REQUIRED_SOURCE_WORD",
    "rho1_kernel": "REQUIRED_RHO1_IN_KERNEL",
    "rho0_replay": "REQUIRED_RHO0_KERNEL_REPLAY",
    "q_z0_replay": "REQUIRED_Q_EQUALS_Z0_REPLAY",
    "base_pair": "s(g)u_z-s(g)",
    "forbidden_pair": "s(g)[x,y]^3-s(g)",
    "base_pair_order": "CORRECTED_BASE_PAIRS_FIRST",
}
ANCHOR_OWNERS = OWNERS[-10:]
TRAILING_ZERO_REPAIRS = ["v11-trailing-zero-repair-%02d" % i for i in range(1, 13)]
TRACE_EXPECTATIONS = [
    {"case": "nonzero-member", "seed_count": 2,
     "action_applications": 4, "candidate_count": 6, "queue_pops": 2,
     "closure_rank": 2, "kernel_dim": 2, "Hd1_rank": 2,
     "terminal": "MEMBER"},
    {"case": "outside-nonmember", "seed_count": 1,
     "action_applications": 1, "candidate_count": 2, "queue_pops": 1,
     "closure_rank": 1, "kernel_dim": 1, "Hd1_rank": 1,
     "terminal": "NONMEMBER"},
    {"case": "zero-member", "seed_count": 1,
     "action_applications": 1, "candidate_count": 2, "queue_pops": 1,
     "closure_rank": 1, "kernel_dim": 1, "Hd1_rank": 0,
     "terminal": "MEMBER"},
    {"case": "zero-nonmember", "seed_count": 1,
     "action_applications": 1, "candidate_count": 2, "queue_pops": 1,
     "closure_rank": 1, "kernel_dim": 0, "Hd1_rank": 0,
     "terminal": "NONMEMBER"},
    {"case": "post-c-cancel", "seed_count": 1,
     "action_applications": 2, "candidate_count": 3, "queue_pops": 2,
     "closure_rank": 2, "kernel_dim": 1, "Hd1_rank": 1,
     "terminal": "MEMBER"},
]


class UnknownInput(RuntimeError):
    pass


class UnknownResource(RuntimeError):
    pass


class IndependentReject(Exception):
    def __init__(self, stage, code, reason):
        super().__init__(reason)
        self.stage, self.code, self.reason = stage, code, reason


class Meter:
    FIELDS = (
        "json_reads", "json_parses", "candidate_constructions", "queue_pops",
        "action_applications", "field_operations", "pivot_reductions",
        "coefficient_updates", "nullspace_work", "solve_work",
        "ancestry_replays", "mutation_work", "canonicalizations",
        "serializations", "rss_bytes", "output_writes",
    )

    def __init__(self):
        self.cases = []
        self.totals = {field: 0 for field in self.FIELDS}
        self.current = None

    def begin(self, name):
        self.current = {"case": name, **{field: 0 for field in self.FIELDS}}
        self.cases.append(self.current)

    def charge(self, field, amount=1):
        if field not in self.FIELDS or type(amount) is not int or amount < 0:
            raise RuntimeError("invalid checker meter charge")
        self.totals[field] += amount
        if self.current is not None:
            self.current[field] += amount

    def rss(self):
        value = 0
        try:
            import resource
            value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        except (ImportError, AttributeError, OSError):
            value = 0
        self.charge("rss_bytes", max(0, value))


CHECKER_METER = None


def meter_charge(field, amount=1):
    if CHECKER_METER is not None:
        CHECKER_METER.charge(field, amount)


def fail(condition, owner=None, mutation=False, message="semantic failure"):
    if condition is True:
        return
    if mutation and owner is not None:
        entry = MUTATION_REGISTRY[owner]
        raise IndependentReject(entry["stage"], entry["code"], entry["reason"])
    raise UnknownInput(message if owner is None else "owner gate: " + owner)


def exact_int(value, label, nonnegative=False):
    if type(value) is not int or (nonnegative and value < 0):
        raise UnknownInput(label + " exact integer")
    return value


def f3(value, label):
    if type(value) is not int or value not in (0, 1, 2):
        raise UnknownInput(label + " canonical F3")
    return value


def vector(value, width, label):
    if type(value) is not list or len(value) != width:
        raise UnknownInput(label + " vector shape")
    for i, scalar in enumerate(value):
        f3(scalar, "%s[%d]" % (label, i))


def matrix(value, rows, columns, label):
    if type(value) is not list or len(value) != rows:
        raise UnknownInput(label + " row shape")
    for i, row in enumerate(value):
        if type(row) is not list or len(row) != columns:
            raise UnknownInput(label + " column shape")
        for j, scalar in enumerate(row):
            f3(scalar, "%s[%d][%d]" % (label, i, j))


def canonical(value):
    meter_charge("canonicalizations")
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def sha(value):
    meter_charge("serializations")
    return hashlib.sha256(canonical(value)).hexdigest()


def record_digest(record):
    body = dict(record)
    body.pop("record_sha256", None)
    return sha(body)


def apply(matrix_value, value):
    if matrix_value and len(matrix_value[0]) != len(value):
        raise UnknownInput("independent matvec dimension")
    meter_charge("field_operations", sum(len(row) for row in matrix_value))
    return [sum(matrix_value[i][j] * value[j]
                for j in range(len(value))) % 3
            for i in range(len(matrix_value))]


def multiply(left, right):
    if not left or not right or len(left[0]) != len(right):
        raise UnknownInput("independent matrix dimension")
    meter_charge("field_operations", len(left) * len(left[0]) * len(right[0]))
    return [[sum(left[i][k] * right[k][j] for k in range(len(right))) % 3
             for j in range(len(right[0]))] for i in range(len(left))]


def combine(rows, coefficients, width):
    if len(rows) != len(coefficients):
        raise UnknownInput("independent combination arity")
    for row in rows:
        vector(row, width, "independent combination row")
    for i, scalar in enumerate(coefficients):
        f3(scalar, "independent combination coefficient[%d]" % i)
    meter_charge("coefficient_updates", len(rows) * width)
    return [sum(coefficients[i] * rows[i][j]
                for i in range(len(rows))) % 3 for j in range(width)]


def bottom_reduce(rows, width):
    """Bottom-pivot row reduction used only by the checker."""
    work = [list(row) for row in rows]
    for row in work:
        vector(row, width, "bottom tableau row")
    pivots, occupied = [], 0
    for column in reversed(range(width)):
        choices = [i for i in range(occupied, len(work))
                   if work[i][column] != 0]
        if not choices:
            continue
        chosen = choices[-1]
        work[occupied], work[chosen] = work[chosen], work[occupied]
        scale = 1 if work[occupied][column] == 1 else 2
        work[occupied] = [(scale * x) % 3 for x in work[occupied]]
        for i in range(len(work)):
            if i == occupied or work[i][column] == 0:
                continue
            factor = work[i][column]
            work[i] = [(x - factor * y) % 3
                       for x, y in zip(work[i], work[occupied])]
            meter_charge("pivot_reductions")
        pivots.append(column)
        meter_charge("pivot_reductions")
        occupied += 1
        if occupied == len(work):
            break
    return work, pivots


def matrix_rank(value, width):
    return len(bottom_reduce(value, width)[1])


def bottom_nullspace(matrix_value, width):
    reduced, pivots = bottom_reduce(matrix_value, width)
    free = [column for column in reversed(range(width)) if column not in pivots]
    answer = []
    for free_column in free:
        row = [0] * width
        row[free_column] = 1
        for index, pivot in reversed(list(enumerate(pivots))):
            row[pivot] = (-sum(reduced[index][j] * row[j]
                               for j in range(width) if j != pivot)) % 3
            meter_charge("nullspace_work")
        answer.append(row)
    return answer


def solve_affine(rows, rhs, width):
    """Bottom-pivot solve with a protected right-hand-side column."""
    if len(rows) != len(rhs):
        raise UnknownInput("affine solve arity")
    table = [list(row) + [rhs[i]] for i, row in enumerate(rows)]
    for row in table:
        vector(row[:width], width, "affine equation")
        f3(row[width], "affine right side")
    pivots, occupied = [], 0
    for column in reversed(range(width)):
        choices = [i for i in range(occupied, len(table))
                   if table[i][column] != 0]
        if not choices:
            continue
        chosen = choices[-1]
        table[occupied], table[chosen] = table[chosen], table[occupied]
        scale = 1 if table[occupied][column] == 1 else 2
        table[occupied] = [(scale * x) % 3 for x in table[occupied]]
        for i in range(len(table)):
            if i == occupied or table[i][column] == 0:
                continue
            factor = table[i][column]
            table[i] = [(x - factor * y) % 3
                        for x, y in zip(table[i], table[occupied])]
            meter_charge("pivot_reductions")
        pivots.append(column)
        meter_charge("pivot_reductions")
        occupied += 1
        if occupied == len(table):
            break
    for row in table:
        if not any(row[:width]) and row[width] != 0:
            return None
    answer = [0] * width
    for row, pivot in zip(table, pivots):
        answer[pivot] = row[width]
    meter_charge("solve_work", len(table) * width)
    return answer


class BottomSpan:
    """Independent incremental membership owner, with rightmost pivots."""
    def __init__(self, width):
        self.width = width
        self.rows = []
        self.pivots = {}

    def reduce(self, row):
        vector(row, self.width, "bottom candidate")
        remainder = list(row)
        for pivot in sorted(self.pivots, reverse=True):
            factor = remainder[pivot]
            if factor:
                base = self.pivots[pivot]
                remainder = [(x - factor * y) % 3
                             for x, y in zip(remainder, base)]
        return remainder

    def contains(self, row):
        return not any(self.reduce(row))

    def add(self, row):
        remainder = self.reduce(row)
        if not any(remainder):
            return False
        pivot = next(i for i in reversed(range(self.width)) if remainder[i])
        scale = 1 if remainder[pivot] == 1 else 2
        normalized = [(scale * x) % 3 for x in remainder]
        for old_pivot in list(self.pivots):
            factor = self.pivots[old_pivot][pivot]
            if factor:
                self.pivots[old_pivot] = [
                    (x - factor * y) % 3
                    for x, y in zip(self.pivots[old_pivot], normalized)]
        self.pivots[pivot] = normalized
        self.rows.append(list(row))
        return True


class DenseTableau:
    """One complete bottom-pivot [raw | identity] tableau per owned basis."""
    def __init__(self, rows, width, name):
        self.name, self.width = name, width
        self.raw_rows = [list(row) for row in rows]
        for row in self.raw_rows:
            vector(row, width, name + " raw row")
        count = len(self.raw_rows)
        table = [row + [1 if i == j else 0 for j in range(count)]
                 for i, row in enumerate(self.raw_rows)]
        pivots, occupied = [], 0
        for column in reversed(range(width)):
            choices = [i for i in range(occupied, count)
                       if table[i][column] != 0]
            if not choices:
                continue
            chosen = choices[-1]
            table[occupied], table[chosen] = table[chosen], table[occupied]
            scale = 1 if table[occupied][column] == 1 else 2
            table[occupied] = [(scale * x) % 3 for x in table[occupied]]
            for i in range(count):
                if i == occupied or table[i][column] == 0:
                    continue
                factor = table[i][column]
                table[i] = [(x - factor * y) % 3
                            for x, y in zip(table[i], table[occupied])]
                meter_charge("pivot_reductions")
            pivots.append(column)
            meter_charge("pivot_reductions")
            occupied += 1
            if occupied == count:
                break
        if occupied != count:
            raise UnknownInput(name + " dependent raw rows")
        self.pivots = pivots
        self.reduced_rows = [row[:width] for row in table]
        self.transforms = [row[width:] for row in table]
        for pivot, row, transform in zip(self.pivots,
                                         self.reduced_rows, self.transforms):
            if row[pivot] != 1 or combine(self.raw_rows, transform, width) != row:
                raise UnknownInput(name + " tableau transform")
        self.transcript_sha256 = sha({"name": name, "width": width,
            "raw_rows": self.raw_rows, "pivots": self.pivots,
            "reduced_rows": self.reduced_rows, "transforms": self.transforms})

    @property
    def rank(self):
        return len(self.pivots)

    def solve(self, target):
        vector(target, self.width, self.name + " target")
        remainder = list(target)
        weights = [0] * self.rank
        for i, pivot in enumerate(self.pivots):
            factor = remainder[pivot]
            weights[i] = factor
            if factor:
                remainder = [(x - factor * y) % 3
                             for x, y in zip(remainder, self.reduced_rows[i])]
        if any(remainder):
            return None
        result = [sum(weights[i] * self.transforms[i][j]
                      for i in range(self.rank)) % 3
                  for j in range(len(self.raw_rows))]
        meter_charge("solve_work", self.rank * len(self.raw_rows))
        if combine(self.raw_rows, result, self.width) != target:
            raise UnknownInput(self.name + " solve replay")
        return result

    def contains(self, target):
        return self.solve(target) is not None


def source_file():
    return (ROOT / SOURCE_REL).resolve()


def load_wrapper(path):
    path = Path(path).resolve()
    if not path.is_file():
        raise UnknownInput("v13 wrapper missing")
    meter_charge("json_reads")
    value = json.loads(path.read_text(encoding="utf-8"))
    meter_charge("json_parses")
    check_wrapper_value(value)
    return value


def check_wrapper_value(value, mutation=False):
    binding = value.get("source_binding", {})
    fail(value.get("schema") == SELF_SCHEMA, "production_input", mutation)
    fail(binding.get("relative_path") == SOURCE_REL and
         binding.get("resolved_path") == str(source_file()) and
         binding.get("bytes") == SOURCE_BYTES and
         binding.get("sha256") == SOURCE_SHA256 and
         binding.get("schema") == SOURCE_SCHEMA and
         binding.get("fixture_seal") == SOURCE_SEAL,
         "production_input", mutation)
    fail(type(binding.get("bytes")) is int and binding["bytes"] >= 0,
         "production_input", mutation)
    fail(value.get("production_input") is False, "production_input", mutation)
    fail(value.get("synthetic_linear_fixture") is True and
         value.get("actual_a5_a6_milestone") is False,
         "production_input", mutation)
    fail(value.get("trailing_zero_repairs") == TRAILING_ZERO_REPAIRS,
         "production_input", mutation)
    fail(value.get("trace_expectations") == TRACE_EXPECTATIONS,
         "production_input", mutation)
    fail(value.get("expected_cases") == {
        name: dict(data) for name, data in expected_cases().items()},
         "production_input", mutation)
    for data in value["expected_cases"].values():
        for field in ("closure_rank", "kernel_dim",
                      "full_nonzero_kernel_cardinality", "Hd1_rank"):
            exact_int(data.get(field), "checker expected " + field, True)
        if data.get("member_theta") is not None:
            vector(data["member_theta"], 2, "checker expected member theta")
        if data.get("dual") is not None:
            vector(data["dual"], 2, "checker expected dual")
    for trace in value["trace_expectations"]:
        for field in ("seed_count", "action_applications", "candidate_count",
                      "queue_pops", "closure_rank", "kernel_dim", "Hd1_rank"):
            exact_int(trace.get(field), "checker trace " + field, True)
    fail(value.get("mutation_roster") == list(OWNERS) and
         value.get("mutation_registry") == MUTATION_REGISTRY,
         "production_input", mutation)
    check_anchor_contract(value, mutation)


def check_anchor_contract(value, mutation=False):
    contract = value.get("anchor_contract")
    if type(contract) is not dict:
        fail(False, "a4_anchor_identity", mutation)
    fail(type(contract.get("required")) is bool and
         contract.get("required") is True,
         "a4_anchor_identity", mutation)
    for field, owner in (
            ("package", "a4_anchor_identity"),
            ("required", "a4_anchor_identity"),
            ("anchor_receipt_identity", "a4_anchor_identity"),
            ("least_index", "anchor_least_index"),
            ("projected_exponent", "anchor_projected_exponent"),
            ("inverse_scalar", "anchor_inverse_scalar"),
            ("anchor_word", "anchor_word"), ("literal_word", "anchor_word"),
            ("rho1_kernel", "anchor_rho1_kernel"),
            ("rho0_replay", "anchor_rho0"),
            ("q_z0_replay", "anchor_q_z0"),
            ("base_pair", "anchor_substituted_cube"),
            ("forbidden_pair", "anchor_substituted_cube"),
            ("base_pair_order", "base_pair_order")):
        fail(contract.get(field) == ANCHOR_CONTRACT[field], owner, mutation)
    fail(contract.get("base_pair") != contract.get("forbidden_pair"),
         "anchor_substituted_cube", mutation)


def validate_actual_anchor(anchor, mutation=False):
    """External production ABI; synthetic linear cases never enter here."""
    fail(type(anchor) is dict, "a4_anchor_identity", mutation)
    fail(anchor.get("package") == ANCHOR_CONTRACT["package"], "a4_anchor_identity", mutation)
    fail(type(anchor.get("anchor_receipt_identity")) is str and anchor.get("anchor_receipt_identity"), "a4_anchor_identity", mutation)
    fail(type(anchor.get("least_index")) is int and anchor["least_index"] >= 0, "anchor_least_index", mutation)
    fail(type(anchor.get("projected_exponent")) is int and anchor["projected_exponent"] in (1, 2), "anchor_projected_exponent", mutation)
    fail(type(anchor.get("inverse_scalar")) is int and anchor["inverse_scalar"] in (1, 2), "anchor_inverse_scalar", mutation)
    fail(type(anchor.get("literal_word")) is str and anchor["literal_word"], "anchor_word", mutation)
    rho1_in_kernel = anchor.get("rho1_in_kernel", anchor.get("rho1_kernel"))
    fail(rho1_in_kernel is True, "anchor_rho1_kernel", mutation)
    fail(anchor.get("rho0_replay") is True, "anchor_rho0", mutation)
    fail(anchor.get("q_z0_replay") is True, "anchor_q_z0", mutation)
    pairs = anchor.get("base_pairs")
    fail(type(pairs) is list and pairs, "base_pair_order", mutation)
    for pair in pairs:
        fail(type(pair) is dict and pair.get("left") != pair.get("right"), "anchor_substituted_cube", mutation)
        fail("[x,y]^3" not in str(pair), "anchor_substituted_cube", mutation)
    fail(anchor.get("base_pair_order") == "CORRECTED_BASE_PAIRS_FIRST", "base_pair_order", mutation)
    return anchor


def load_source():
    path = source_file()
    if not path.is_file():
        raise UnknownInput("v11 source missing")
    raw = path.read_bytes()
    meter_charge("json_reads")
    if len(raw) != SOURCE_BYTES or hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise UnknownInput("v11 source bytes/SHA drift")
    value = json.loads(raw.decode("utf-8"))
    meter_charge("json_parses")
    return value


def expected_cases():
    return {
        "nonzero-member": {"closure_rank": 2, "kernel_dim": 2,
            "full_nonzero_kernel_cardinality": 8, "Hd1_rank": 2,
            "terminal": "MEMBER", "member_theta": [1, 1], "dual": None},
        "outside-nonmember": {"closure_rank": 1, "kernel_dim": 1,
            "full_nonzero_kernel_cardinality": 2, "Hd1_rank": 1,
            "terminal": "NONMEMBER", "member_theta": None, "dual": [0, 1]},
        "zero-member": {"closure_rank": 1, "kernel_dim": 1,
            "full_nonzero_kernel_cardinality": 2, "Hd1_rank": 0,
            "terminal": "MEMBER", "member_theta": [0, 0], "dual": None},
        "zero-nonmember": {"closure_rank": 1, "kernel_dim": 0,
            "full_nonzero_kernel_cardinality": 0, "Hd1_rank": 0,
            "terminal": "NONMEMBER", "member_theta": None, "dual": [1, 0]},
        "post-c-cancel": {"closure_rank": 2, "kernel_dim": 1,
            "full_nonzero_kernel_cardinality": 2, "Hd1_rank": 1,
            "terminal": "MEMBER", "member_theta": [1, 2], "dual": None},
    }


def check_case_literals(case, mutation=False):
    if mutation and "mutation_fixture_seal" in case:
        sealed = dict(case)
        claimed = sealed.pop("mutation_fixture_seal", None)
        fail(type(claimed) is str and claimed == sha(sealed),
             "production_input", mutation)
    name = case.get("name")
    fail(type(name) is str and name in expected_cases(), "production_input", mutation)
    fail(type(case.get("modulus")) is int and case["modulus"] == 3,
         "field_modulus", mutation)
    fail(case.get("theta_seeds") == case.get("seed_bindings"),
         "theta_seed", mutation)
    for field, binding, owner in (("A_theta", "A_theta_binding", "theta_action"),
                                  ("A_Z", "A_Z_binding", "z_action"),
                                  ("A_E", "A_E_binding", "eta_action"),
                                  ("D", "D_binding", "D_entry"),
                                  ("O", "O_binding", "O_entry"),
                                  ("C", "C_binding", "C_entry")):
        fail(case.get(field) == case.get(binding), owner, mutation)
    seeds = case.get("theta_seeds")
    fail(type(seeds) is list and len(seeds) >= 1, "theta_seed", mutation)
    for seed in seeds:
        vector(seed, 2, "checker theta seed")
    fail(case.get("occurrence_count") == 11 and
         case.get("occurrence_tags") == ["occurrence%02d" % i for i in range(11)],
         "production_input", mutation)
    matrix(case.get("A_theta"), 2, 2, "checker A_theta")
    matrix(case.get("A_Z"), 2, 2, "checker A_Z")
    matrix(case.get("A_E"), 11, 11, "checker A_E")
    matrix(case.get("D"), 2, 2, "checker D")
    matrix(case.get("O"), 11, 2, "checker O")
    matrix(case.get("C"), 1, 11, "checker C")
    fail(matrix_rank(case["A_theta"], 2) == 2 and
         matrix_rank(case["A_Z"], 2) == 2 and
         matrix_rank(case["A_E"], 11) == 11,
         "production_input", mutation)
    fail(multiply(case["D"], case["A_theta"]) == multiply(case["A_Z"], case["D"]), "D_entry", mutation)
    fail(multiply(case["O"], case["A_theta"]) == multiply(case["A_E"], case["O"]), "O_entry", mutation)
    names, actions = case.get("action_names"), case.get("actions")
    fail(type(names) is list and type(actions) is list and len(names) == len(actions) and
         names == case.get("action_order_binding"), "action_order", mutation)
    fail(case.get("C_phase") == "after-closure", "premature_C", mutation)
    fail(case.get("parent_hint") == 0 and case.get("left_kernel_method") == "rref",
         "production_input", mutation)
    for index, action in enumerate(actions):
        fail(type(action) is dict and action.get("name") == names[index], "action_order", mutation)
        matrix(action.get("theta_matrix"), 2, 2, "checker action theta")
        matrix(action.get("z_matrix"), 2, 2, "checker action z")
        matrix(action.get("eta_matrix"), 11, 11, "checker action eta")
        fail(matrix_rank(action["theta_matrix"], 2) == 2 and
             matrix_rank(action["z_matrix"], 2) == 2 and
             matrix_rank(action["eta_matrix"], 11) == 11,
             "production_input", mutation)
        fail(multiply(case["D"], action["theta_matrix"]) == multiply(action["z_matrix"], case["D"]), "D_entry", mutation)
        fail(multiply(case["O"], action["theta_matrix"]) == multiply(action["eta_matrix"], case["O"]), "O_entry", mutation)
    targets = {"nonzero-member": [1, 1], "outside-nonmember": [0, 1],
                "zero-member": [0, 0], "zero-nonmember": [1, 0],
                "post-c-cancel": [1, 2]}
    vector(case.get("target"), 2, "checker target")
    fail(case["target"] == targets[name], "target", mutation)
    fail(case.get("terminal") == expected_cases()[name]["terminal"],
         "production_input", mutation)


def reconstruct(case):
    """Rebuild the candidate queue with bottom-pivot membership only."""
    check_case_literals(case)
    span = BottomSpan(13)
    accepted, transcript, queue, seen = [], [], deque(), set()

    def visit(candidate, parent, action, queue_pop):
        raw = candidate["flat"]
        meter_charge("candidate_constructions")
        before = len(accepted)
        represented = span.contains(raw)
        decision = "DEPENDENT" if represented else "ACCEPTED"
        if not represented:
            span.add(raw)
            index = len(accepted)
            candidate["closure_index"] = index
            accepted.append(candidate)
            queue.append(candidate)
            seen.add(tuple(raw))
            effect = "ENQUEUE_RANK_RAISE"
        else:
            effect = "DEPENDENT"
        record = {"ordinal": len(transcript), "parent": parent,
                  "action": action, "queue_pop_parent": queue_pop,
                  "raw_candidate": {"theta": list(candidate["theta"]),
                      "z": list(candidate["z"]), "eta": list(candidate["eta"]),
                      "flat": list(candidate["flat"])},
                  "pre_rank": before, "decision": decision,
                  "normalization": None, "normalized_row": None,
                  "normalized_ancestry": None, "post_rank": len(accepted),
                  "direct_coefficients": None, "queue_effect": effect,
                  "basis_candidate_index": len(transcript)}
        record["raw_candidate_sha256"] = sha(record["raw_candidate"])
        record["record_sha256"] = record_digest(record)
        transcript.append(record)

    for seed_index, seed in enumerate(case["theta_seeds"]):
        theta = list(seed)
        z_value = apply(case["D"], theta)
        eta_value = apply(case["O"], theta)
        visit({"theta": theta, "z": z_value, "eta": eta_value,
               "flat": z_value + eta_value, "seed_index": seed_index,
               "parent": None, "action": "seed", "kind": "seed"},
              None, "seed", None)
    pops = 0
    while queue:
        item = queue.popleft()
        pops += 1
        meter_charge("queue_pops")
        for action in case["actions"]:
            meter_charge("action_applications")
            theta = apply(action["theta_matrix"], item["theta"])
            z_value = apply(action["z_matrix"], item["z"])
            eta_value = apply(action["eta_matrix"], item["eta"])
            fail(z_value == apply(case["D"], theta), "D_entry")
            fail(eta_value == apply(case["O"], theta), "O_entry")
            visit({"theta": theta, "z": z_value, "eta": eta_value,
                   "flat": z_value + eta_value,
                   "seed_index": item["seed_index"],
                   "parent": item["closure_index"],
                   "action": action["name"], "kind": "action"},
                  item["closure_index"], action["name"], pops - 1)
    # Checker owns a different dense tableau, built only after closure.
    closure_tableau = DenseTableau([item["flat"] for item in accepted], 13,
                                   "checker closure")
    images = [apply(case["C"], item["eta"]) for item in accepted]
    image_matrix = [[images[j][i] for j in range(len(images))] for i in range(1)]
    kernel_basis = bottom_nullspace(image_matrix, len(accepted))
    hd1_all = [combine([item["z"] for item in accepted], coeff, 2)
               for coeff in kernel_basis]
    hd1_span = BottomSpan(2)
    hd1_rows, hd1_labels = [], []
    for index, row in enumerate(hd1_all):
        if hd1_span.add(row):
            hd1_rows.append(row)
            hd1_labels.append(index)
    hd1_tableau = DenseTableau(hd1_rows, 2, "checker Hd1") if hd1_rows else None
    target = list(case["target"])
    membership = hd1_tableau.contains(target) if hd1_tableau else target == [0, 0]
    terminal = "MEMBER" if membership else "NONMEMBER"
    ancestry = dual = None
    if membership:
        coeff = hd1_tableau.solve(target) if hd1_tableau else []
        hd1_coeffs = [0] * len(hd1_all)
        for selected, value in zip(hd1_labels, coeff or []):
            hd1_coeffs[selected] = value
        closure_coeffs = [sum(hd1_coeffs[i] * kernel_basis[i][j]
                              for i in range(len(kernel_basis))) % 3
                          for j in range(len(accepted))]
        theta = combine([item["theta"] for item in accepted], closure_coeffs, 2)
        z_value = combine([item["z"] for item in accepted], closure_coeffs, 2)
        eta = combine([item["eta"] for item in accepted], closure_coeffs, 11)
        fail(z_value == target and apply(case["D"], theta) == target)
        fail(apply(case["C"], eta) == [0])
        ancestry = {"Hd1_coefficients": hd1_coeffs,
                    "closure_coefficients": closure_coeffs,
                    "theta": theta, "z": z_value, "eta": eta}
        ancestry["direct_reconstruction_sha256"] = sha(ancestry)
        meter_charge("ancestry_replays")
    else:
        # A dual is a column solution of Hd1*q=0 and target*q=1.
        dual = solve_affine(list(hd1_rows) + [target],
                            [0] * len(hd1_rows) + [1], 2)
        if dual is None:
            raise UnknownInput("checker dual solve")
        fail(all(sum(dual[i] * row[i] for i in range(2)) % 3 == 0
                 for row in hd1_rows))
        fail(sum(dual[i] * target[i] for i in range(2)) % 3 == 1)
    queue_bound = len(accepted) + len(case["actions"]) * (
        len(case["theta_seeds"]) + len(case["actions"]) * 13)
    queue_bound = max(queue_bound, len(case["theta_seeds"]) +
                      len(case["actions"]) * max(1, 13))
    if pops > queue_bound:
        raise UnknownResource("derived closure queue bound exhausted")
    return {"case": case, "transcript": transcript, "accepted": accepted,
            "closure_tableau": closure_tableau, "kernel_basis": kernel_basis,
            "hd1_all": hd1_all, "hd1_rows": hd1_rows,
            "hd1_tableau": hd1_tableau, "target": target,
            "terminal": terminal, "ancestry": ancestry, "dual": dual,
            "pops": pops, "queue_bound": queue_bound}


def check_f3_receipt(receipt, mutation=False):
    for field in ("closure_rank", "closure_queue_pops", "context_pops",
                  "closure_queue_bound", "closure_candidate_count",
                  "kernel_dim", "full_nonzero_kernel_cardinality",
                  "Hd1_rank"):
        exact_int(receipt.get(field), "receipt " + field, True)
    for index, record in enumerate(receipt.get("transcript", [])):
        for field in ("ordinal", "pre_rank", "post_rank",
                      "basis_candidate_index"):
            exact_int(record.get(field),
                      "receipt transcript " + field, True)
        raw = record.get("raw_candidate", {})
        for field, width in (("theta", 2), ("z", 2), ("eta", 11), ("flat", 13)):
            vector(raw.get(field), width, "receipt transcript raw")
        for field in ("reduction_coefficients", "normalized_ancestry", "direct_coefficients"):
            value = record.get(field)
            if type(value) is not list:
                raise UnknownInput("receipt coefficient vector")
            for j, scalar in enumerate(value):
                try:
                    f3(scalar, "receipt transcript coefficient[%d,%d]" % (index, j))
                except UnknownInput:
                    fail(False, "f3_plus3_coefficient", mutation)
        if record.get("normalized_row") is not None:
            vector(record["normalized_row"], 13, "receipt normalized row")
    for row in receipt.get("rows", []):
        for field, width in (("theta", 2), ("z", 2), ("eta", 11), ("flat", 13)):
            vector(row.get(field), width, "receipt accepted row")
    for row in receipt.get("left_kernel_basis", []):
        vector(row, len(receipt.get("rows", [])), "receipt left kernel")
    for row in receipt.get("Hd1", []):
        vector(row, 2, "receipt Hd1")
    if receipt.get("member_theta") is not None:
        vector(receipt["member_theta"], 2, "receipt member theta")
    if receipt.get("dual") is not None:
        vector(receipt["dual"], 2, "receipt dual")


def replay_producer_owner(owner):
    if type(owner) is not dict:
        raise UnknownInput("producer owner export object")
    body = dict(owner)
    claimed = body.pop("owner_digest_sha256", None)
    if type(claimed) is not str or claimed != sha(body):
        raise UnknownInput("producer owner seal")
    width = exact_int(owner.get("width"), "producer owner width", True)
    rank = exact_int(owner.get("rank"), "producer owner rank", True)
    rows = owner.get("raw_rows", [])
    if len(rows) != rank or len(owner.get("insertion_order", [])) != rank:
        raise UnknownInput("producer owner roster")
    for row in rows:
        vector(row, width, "producer owner raw")
    if not (len(owner.get("pivots", [])) == len(owner.get("reduced_rows", [])) ==
            len(owner.get("transforms", [])) == len(owner.get("reconstruction_digests_sha256", [])) == rank):
        raise UnknownInput("producer owner arity")
    for pivot, row, transform, claimed_digest in zip(owner["pivots"], owner["reduced_rows"], owner["transforms"], owner["reconstruction_digests_sha256"]):
        exact_int(pivot, "producer pivot")
        vector(row, width, "producer reduced")
        vector(transform, rank, "producer transform")
        if combine(rows, transform, width) != row:
            raise UnknownInput("producer transform replay")
        if claimed_digest != sha({"pivot": pivot, "transform": transform, "reconstructed_row": row}):
            raise UnknownInput("producer transform digest")
    accepted = 0
    for index, record in enumerate(owner.get("reductions", [])):
        if record.get("candidate_index") != index or record.get("prior_roster_size") != accepted:
            raise UnknownInput("producer reduction order")
        prior = record["prior_roster_size"]
        vector(record["raw_row"], width, "producer candidate")
        vector(record["remainder"], width, "producer remainder")
        vector(record["reduction_coefficients"], prior, "producer reduction coefficients")
        vector(record["direct_coefficients"], rank, "producer direct coefficients")
        if combine(rows[:prior], record["reduction_coefficients"], width) != [
                (x - y) % 3 for x, y in zip(record["raw_row"], record["remainder"])]:
            raise UnknownInput("producer reduction coefficient sign")
        if combine(rows, record["direct_coefficients"], width) != record["raw_row"]:
            raise UnknownInput("producer direct coefficient replay")
        if record.get("direct_reconstruction_sha256") != sha({
                key: record[key] for key in (
                    "candidate_index", "label", "raw_row", "accepted",
                    "accepted_raw_index", "direct_coefficients")}):
            raise UnknownInput("producer direct reconstruction digest")
        if record.get("accepted") is True:
            if record.get("accepted_raw_index") != accepted or \
                    record.get("raw_row") != rows[accepted] or \
                    not any(record.get("remainder")):
                raise UnknownInput("producer accepted index")
            accepted += 1
        elif record.get("accepted") is False:
            if record.get("accepted_raw_index") is not None or \
                    any(record.get("remainder")):
                raise UnknownInput("producer dependent transcript")
        else:
            raise UnknownInput("producer decision type")
    if accepted != rank:
        raise UnknownInput("producer owner accepted count")


def verify_receipt(receipt, independent, mutation=False):
    check_f3_receipt(receipt, mutation)
    claimed = receipt.get("case_digest_sha256")
    body = {key: value for key, value in receipt.items() if key != "case_digest_sha256"}
    fail(type(claimed) is str and claimed == sha(body), None, mutation,
         "producer receipt seal")
    case = independent["case"]
    fail(receipt.get("case") == case["name"] and
         receipt.get("production_input") is False,
         "production_input", mutation)
    expected_cases_map = expected_cases()
    def same(field, owner=None):
        wanted = {
            "closure_rank": len(independent["accepted"]),
            "closure_queue_pops": independent["pops"],
            "context_pops": independent["pops"],
            "closure_queue_bound": independent["queue_bound"],
            "closure_candidate_count": len(independent["transcript"]),
            "kernel_dim": len(independent["kernel_basis"]),
            "Hd1_rank": len(independent["hd1_rows"]),
            "target": independent["target"],
            "terminal": independent["terminal"],
            "slice_membership": independent["terminal"] == "MEMBER",
            "left_kernel_basis": independent["kernel_basis"],
            "Hd1": independent["hd1_all"],
        }
        if field in wanted:
            fail(receipt.get(field) == wanted[field], owner or "candidate_rank", mutation)
    same("closure_rank", "candidate_rank")
    same("closure_queue_pops", "closure_queue_pops")
    same("context_pops", "context_pops")
    same("closure_queue_bound", "closure_queue_bound")
    same("closure_candidate_count", "closure_candidate_count")
    same("kernel_dim", "candidate_rank")
    expected = expected_cases_map[case["name"]]
    if mutation:
        # Route transcript-owned shape/sign edits before the generic owner
        # replay, so an owner mutation cannot be hidden as a broad exception.
        for actual in receipt.get("transcript", []):
            index = actual.get("basis_candidate_index")
            if type(index) is not int or index < 0 or index >= len(receipt.get("closure_owner", {}).get("reductions", [])):
                fail(False, "candidate_rank", True)
            owner_record = receipt["closure_owner"]["reductions"][index]
            fail(actual.get("reduction_coefficients") == owner_record.get("reduction_coefficients"),
                 "candidate_coefficients", True)
    replay_producer_owner(receipt.get("closure_owner"))
    replay_producer_owner(receipt.get("Hd1_owner"))
    fail(receipt["closure_owner"]["raw_rows"] ==
         [row.get("flat") for row in receipt.get("rows", [])],
         "row_theta", mutation)
    for record in receipt.get("kernel_reconstruction", []):
        coeff = record.get("closure_coefficients")
        vector(coeff, len(receipt.get("rows", [])), "producer kernel coefficients")
        vector(record.get("theta"), 2, "producer kernel theta")
        vector(record.get("z"), 2, "producer kernel z")
        vector(record.get("eta"), 11, "producer kernel eta")
        payload = {key: record.get(key) for key in (
            "kernel_basis_index", "closure_coefficients", "theta", "z", "eta")}
        fail(record.get("direct_reconstruction_sha256") == sha(payload),
             "left_kernel", mutation)
        fail(combine([row["theta"] for row in receipt["rows"]], coeff, 2) == record["theta"] and
             combine([row["z"] for row in receipt["rows"]], coeff, 2) == record["z"] and
             combine([row["eta"] for row in receipt["rows"]], coeff, 11) == record["eta"] and
             apply(case["C"], record["eta"]) == [0],
             "left_kernel", mutation)
    fail(receipt.get("left_kernel_basis") ==
         [record.get("closure_coefficients") for record in receipt.get("kernel_reconstruction", [])],
         "left_kernel", mutation)
    fail(receipt.get("Hd1") ==
         [record.get("z") for record in receipt.get("kernel_reconstruction", [])],
         "Hd1", mutation)
    fail(receipt.get("full_nonzero_kernel_cardinality") == 3 ** len(independent["kernel_basis"]) - 1,
         "candidate_rank", mutation)
    same("Hd1_rank", "Hd1")
    same("target", "target")
    same("terminal", "terminal")
    same("slice_membership", "terminal")
    # Kernel/Hd1 bases are noncanonical.  Compare their mathematical spans in
    # both directions, rather than requiring the producer's coordinates.
    producer_kernel = receipt.get("left_kernel_basis", [])
    checker_kernel = independent["kernel_basis"]
    if mutation and len({tuple(row) for row in producer_kernel}) != len(producer_kernel):
        fail(False, "left_kernel", True)
    if producer_kernel:
        producer_kernel_tableau = DenseTableau(producer_kernel,
                                                len(independent["accepted"]),
                                                "producer-kernel span")
    else:
        producer_kernel_tableau = None
    checker_kernel_tableau = DenseTableau(checker_kernel,
                                          len(independent["accepted"]),
                                          "checker-kernel span") if checker_kernel else None
    for row in producer_kernel:
        fail(checker_kernel_tableau is not None and checker_kernel_tableau.contains(row),
             "left_kernel", mutation)
    for row in checker_kernel:
        fail(producer_kernel_tableau is not None and producer_kernel_tableau.contains(row),
             "left_kernel", mutation)
    producer_hd1 = receipt.get("Hd1", [])
    checker_hd1 = independent["hd1_rows"]
    producer_hd1_nonzero = [row for row in producer_hd1 if any(row)]
    producer_hd1_tableau = DenseTableau(producer_hd1_nonzero, 2,
                                        "producer-Hd1 span") if producer_hd1 and \
        producer_hd1_nonzero else None
    checker_hd1_tableau = DenseTableau(checker_hd1, 2,
                                       "checker-Hd1 span") if checker_hd1 else None
    for row in producer_hd1:
        if any(row):
            fail(checker_hd1_tableau is not None and checker_hd1_tableau.contains(row),
                 "Hd1", mutation)
        else:
            fail(row == [0, 0], "Hd1", mutation)
    for row in checker_hd1:
        fail(producer_hd1_tableau is not None and producer_hd1_tableau.contains(row),
             "Hd1", mutation)
    # Compare mathematical spans in both directions, never coordinate maps.
    closure_tableau = independent["closure_tableau"]
    producer_closure_tableau = DenseTableau(receipt["closure_owner"]["raw_rows"],
                                            13, "receipt closure check")
    for row in receipt["closure_owner"]["raw_rows"]:
        fail(closure_tableau.contains(row), None, mutation, "closure producer row outside checker span")
    for row in closure_tableau.raw_rows:
        fail(producer_closure_tableau.contains(row), None, mutation,
             "checker closure row outside producer span")
    order = [row.get("basis_candidate_index") for row in receipt["transcript"]]
    wanted_order = [row.get("basis_candidate_index") for row in independent["transcript"]]
    dependent = [row.get("basis_candidate_index") for row in receipt["transcript"] if row.get("decision") == "DEPENDENT"]
    wanted_dependent = [row.get("basis_candidate_index") for row in independent["transcript"] if row.get("decision") == "DEPENDENT"]
    if order != wanted_order and set(dependent) == set(wanted_dependent):
        fail(False, "dependent_record_reorder", mutation)
    for index, actual in enumerate(receipt["transcript"]):
        if index >= len(independent["transcript"]):
            fail(False, "dependent_record_deletion", mutation)
        wanted = independent["transcript"][index]
        fail(actual.get("ordinal") == index and
             actual.get("basis_candidate_index") == index,
             "candidate_rank", mutation)
        for field, owner in (("parent", "candidate_parent"),
                             ("action", "candidate_action"),
                             ("decision", "candidate_decision"),
                             ("pre_rank", "candidate_rank"),
                             ("post_rank", "candidate_rank"),
                             ("raw_candidate", "candidate_action"),
                             ("queue_effect", "candidate_decision")):
            fail(actual.get(field) == wanted.get(field), owner, mutation)
        owner_record = receipt["closure_owner"]["reductions"][actual["basis_candidate_index"]]
        for field, owner in (("pre_rank", "candidate_rank"),
                             ("reduction_coefficients", "candidate_coefficients"),
                             ("normalization", "candidate_normalization"),
                             ("normalized_row", "candidate_normalization"),
                             ("normalized_ancestry", "candidate_coefficients"),
                             ("direct_coefficients", "candidate_coefficients")):
            if field == "normalized_ancestry":
                transform = owner_record.get("normalized_transform")
                wanted_value = (list(transform) + [0] *
                                (receipt["closure_owner"]["rank"] - len(transform))) \
                    if transform is not None else None
            else:
                wanted_value = owner_record.get(field)
            fail(actual.get(field) == wanted_value, owner, mutation)
        fail(actual.get("raw_candidate_sha256") == sha(actual["raw_candidate"]),
             "candidate_action", mutation)
        fail(actual.get("record_sha256") == record_digest(actual),
             "candidate_decision", mutation)
    if len(receipt["transcript"]) != len(independent["transcript"]):
        fail(False, "dependent_record_deletion", mutation)
    for index, (actual, wanted) in enumerate(zip(receipt["rows"], independent["accepted"])):
        for field, owner in (("seed_index", "seed_index"), ("parent", "parent"),
                             ("action", "candidate_action"), ("kind", "candidate_action"),
                             ("theta", "row_theta"), ("z", "row_theta"),
                             ("eta", "row_theta"), ("flat", "row_theta")):
            fail(actual.get(field) == wanted.get(field), owner, mutation)
    if receipt.get("member_theta") is not None:
        theta = receipt["member_theta"]
        fail(apply(case["D"], theta) == receipt["target"],
             "member_witness_equality", mutation)
        ancestry = receipt.get("member_ancestry")
        fail(type(ancestry) is dict and ancestry.get("theta") == theta,
             "member_ancestry", mutation)
        ancestry_body = {key: ancestry.get(key) for key in (
            "Hd1_coefficients", "closure_coefficients", "theta", "z", "eta")}
        fail(ancestry.get("direct_reconstruction_sha256") == sha(ancestry_body),
             "member_ancestry", mutation)
        fail(combine(receipt["Hd1"], ancestry["Hd1_coefficients"], 2) == receipt["target"],
             "member_ancestry", mutation)
        fail(combine([row["theta"] for row in receipt["rows"]],
                     ancestry["closure_coefficients"], 2) == theta and
             combine([row["z"] for row in receipt["rows"]],
                     ancestry["closure_coefficients"], 2) == ancestry.get("z") and
             combine([row["eta"] for row in receipt["rows"]],
                     ancestry["closure_coefficients"], 11) == ancestry.get("eta"),
             "member_ancestry", mutation)
    else:
        fail(independent["terminal"] == "NONMEMBER", "member_ancestry", mutation)
    if independent["terminal"] == "NONMEMBER":
        dual = receipt.get("dual")
        fail(type(dual) is list and all(sum(dual[i] * row[i] for i in range(2)) % 3 == 0
             for row in independent["hd1_rows"]) and
             sum(dual[i] * independent["target"][i] for i in range(2)) % 3 == 1,
             "dual", mutation)
    else:
        fail(receipt.get("dual") is None, "dual", mutation)
    # The expected literal tuple is a post-computation comparison only.
    fail(receipt.get("closure_rank") == expected["closure_rank"] and
         receipt.get("kernel_dim") == expected["kernel_dim"] and
         receipt.get("Hd1_rank") == expected["Hd1_rank"] and
         receipt.get("terminal") == expected["terminal"], None, mutation,
         "arithmetic expected tuple mismatch")


def owner_value(obj, owner):
    if owner == "production_input": return obj.get("source_binding")
    if owner in ANCHOR_OWNERS:
        return obj.get("anchor_contract", {}).get({
            "a4_anchor_identity": "anchor_receipt_identity",
            "anchor_least_index": "least_index",
            "anchor_projected_exponent": "projected_exponent",
            "anchor_inverse_scalar": "inverse_scalar",
            "anchor_substituted_cube": "forbidden_pair",
            "anchor_word": "literal_word", "anchor_rho1_kernel": "rho1_kernel",
            "anchor_rho0": "rho0_replay",
            "anchor_q_z0": "q_z0_replay", "base_pair_order": "base_pair_order",
        }[owner])
    if owner in ("field_modulus", "theta_seed", "theta_action", "z_action", "eta_action", "D_entry", "O_entry", "C_entry", "action_order", "premature_C", "target"):
        key = {"field_modulus": "modulus", "theta_seed": "theta_seeds", "theta_action": "A_theta", "z_action": "A_Z", "eta_action": "A_E", "D_entry": "D", "O_entry": "O", "C_entry": "C", "action_order": "action_names", "premature_C": "C_phase", "target": "target"}[owner]
        return obj.get(key)
    return obj.get(owner)


def mutate_case(case, owner):
    value = copy.deepcopy(case)
    if owner == "field_modulus": value["modulus"] = 9
    elif owner == "theta_seed": value["theta_seeds"][0][0] = (value["theta_seeds"][0][0] + 1) % 3
    elif owner == "theta_action": value["A_theta"][0][0] = 2
    elif owner == "z_action": value["A_Z"][0][0] = 2
    elif owner == "eta_action": value["A_E"][0][0] = 2
    elif owner == "D_entry": value["D"][0][0] = 2
    elif owner == "O_entry": value["O"][0][0] = 2
    elif owner == "C_entry": value["C"][0][0] = (value["C"][0][0] + 1) % 3
    elif owner == "action_order": value["action_names"] = ["invalid-action"]
    elif owner == "premature_C": value["C_phase"] = "before-closure"
    elif owner == "target": value["target"] = [value["target"][0], (value["target"][1] + 1) % 3]
    else: raise RuntimeError("not checker raw owner")
    return value


def mutate_receipt(receipt, owner):
    value = copy.deepcopy(receipt)
    if owner == "seed_index": value["rows"][0]["seed_index"] = 99
    elif owner == "parent": value["rows"][1 if len(value["rows"]) > 1 else 0]["parent"] = 99
    elif owner == "row_theta": value["rows"][0]["theta"][0] = (value["rows"][0]["theta"][0] + 1) % 3
    elif owner == "left_kernel": value["left_kernel_basis"][0] = copy.deepcopy(value["left_kernel_basis"][1])
    elif owner == "Hd1": value["Hd1"][0] = [1, 1]
    elif owner == "member_ancestry": value["member_ancestry"]["theta"][0] = (value["member_ancestry"]["theta"][0] + 1) % 3
    elif owner == "dual": value["dual"][0] = (value["dual"][0] + 1) % 3
    elif owner == "terminal": value["terminal"] = "MUTATED"
    elif owner == "closure_queue_pops": value["closure_queue_pops"] += 1
    elif owner == "context_pops": value["context_pops"] += 1
    elif owner == "closure_candidate_count": value["closure_candidate_count"] += 1
    elif owner == "closure_queue_bound": value["closure_queue_bound"] += 1
    elif owner in ("candidate_parent", "candidate_action", "candidate_decision", "candidate_normalization", "candidate_coefficients", "candidate_rank"):
        row = value["transcript"][0]
        if owner == "candidate_parent": row["parent"] = 99
        elif owner == "candidate_action": row["action"] = "invalid-action"
        elif owner == "candidate_decision": row["decision"] = "DEPENDENT" if row["decision"] == "ACCEPTED" else "ACCEPTED"
        elif owner == "candidate_normalization": row["normalization"] = 0
        elif owner == "candidate_coefficients": row["reduction_coefficients"] = [1]
        else: row["post_rank"] += 1
    elif owner == "dependent_record_deletion": value["transcript"] = value["transcript"][:-1]
    elif owner == "dependent_record_reorder":
        indices = [i for i, row in enumerate(value["transcript"]) if row["decision"] == "DEPENDENT"]
        if len(indices) < 2: raise RuntimeError("checker mutation fixture lacks dependencies")
        i, j = indices[:2]; value["transcript"][i], value["transcript"][j] = value["transcript"][j], value["transcript"][i]
    elif owner == "f3_plus3_coefficient": value["transcript"][0]["reduction_coefficients"] = [3]
    elif owner == "member_witness_equality": value["member_theta"][0] = (value["member_theta"][0] + 1) % 3
    else: raise RuntimeError("not checker receipt owner")
    body = {key: item for key, item in value.items() if key != "case_digest_sha256"}
    value["case_digest_sha256"] = sha(body)
    return value


def mutation_control(wrapper, source, independent, owner):
    meter_charge("mutation_work")
    entry = MUTATION_REGISTRY[owner]
    context = independent[entry["case_index"]]
    if entry["scope"] == "wrapper":
        before = wrapper
        mutated = copy.deepcopy(wrapper)
        mutated["source_binding"]["bytes"] += 1
        oracle = lambda: check_wrapper_value(mutated, mutation=True)
    elif entry["scope"] == "anchor":
        before = wrapper
        mutated = copy.deepcopy(wrapper)
        field = {
            "a4_anchor_identity": "anchor_receipt_identity",
            "anchor_least_index": "least_index",
            "anchor_projected_exponent": "projected_exponent",
            "anchor_inverse_scalar": "inverse_scalar",
            "anchor_substituted_cube": "forbidden_pair",
            "anchor_word": "literal_word", "anchor_rho1_kernel": "rho1_kernel",
            "anchor_rho0": "rho0_replay",
            "anchor_q_z0": "q_z0_replay", "base_pair_order": "base_pair_order",
        }[owner]
        mutated["anchor_contract"][field] = "MUTATED_" + field
        oracle = lambda: check_wrapper_value(mutated, mutation=True)
    elif entry["scope"] == "raw_case":
        before = source["cases"][entry["case_index"]]
        mutated = mutate_case(before, owner)
        mutated["mutation_fixture_seal"] = sha(mutated)
        oracle = lambda: check_case_literals(mutated, mutation=True)
    else:
        before = context["receipt"]
        mutated = mutate_receipt(before, owner)
        oracle = lambda: verify_receipt(mutated, context, mutation=True)
    owned_before, owned_after = sha(owner_value(before, owner)), sha(owner_value(mutated, owner))
    canonical_before, canonical_after = sha(before), sha(mutated)
    if owned_before == owned_after or canonical_before == canonical_after:
        raise RuntimeError("checker mutation did not change owner")
    try:
        oracle()
    except IndependentReject as rejection:
        if (rejection.stage, rejection.code, rejection.reason) != (entry["stage"], entry["code"], entry["reason"]):
            raise RuntimeError("checker wrong owner rejection")
    else:
        raise RuntimeError("checker mutation accepted")
    return {"owner": owner, "scope": entry["scope"], "case_index": entry["case_index"],
            "owned_before_sha256": owned_before, "owned_after_sha256": owned_after,
            "canonical_before_sha256": canonical_before, "canonical_after_sha256": canonical_after,
            "resealed_sha256": mutated.get("case_digest_sha256",
                mutated.get("mutation_fixture_seal",
                           mutated.get("source_binding", {}).get("sha256"))),
            "semantic_oracle_reached": True, "rejection_stage": entry["stage"],
            "rejection_code": entry["code"], "rejection_reason": entry["reason"]}


def selftest(wrapper_path, receipt_path, output_path):
    global CHECKER_METER
    CHECKER_METER = Meter()
    meter = CHECKER_METER
    wrapper = load_wrapper(wrapper_path)
    source = load_source()
    fail(source.get("schema") == SOURCE_SCHEMA and source.get("fixture_seal") == SOURCE_SEAL,
         "production_input")
    fail(source.get("modulus") == 3 and source.get("typed_basis") == {
        "Theta": ["theta0", "theta1"], "Z": ["z0", "z1"],
        "E_hat": ["occurrence%02d" % i for i in range(11)],
        "E": ["printed0"]}, "production_input")
    fail(source.get("expected_cases") == {
        name: {key: value for key, value in data.items()
               if key not in ("terminal",)}
        for name, data in expected_cases().items()}, "production_input")
    for data in source["expected_cases"].values():
        for field in ("closure_rank", "kernel_dim",
                      "full_nonzero_kernel_cardinality", "Hd1_rank"):
            exact_int(data.get(field), "source expected " + field, True)
        if data.get("member_theta") is not None:
            vector(data["member_theta"], 2, "source expected member theta")
        if data.get("dual") is not None:
            vector(data["dual"], 2, "source expected dual")
    fail(source.get("mutation_roster") == list(OWNERS[:19]), "production_input")
    fail(source.get("mutation_registry") == {
        name: MUTATION_REGISTRY[name] for name in OWNERS[:19]},
         "production_input")
    fail(type(source.get("cases")) is list and len(source["cases"]) == 5,
         "production_input")
    for case in source["cases"]:
        check_case_literals(case)
    fail([case["name"] for case in source["cases"]] == list(expected_cases()),
         "production_input")
    meter_charge("json_reads")
    receipt = json.loads(Path(receipt_path).read_text(encoding="utf-8"))
    meter_charge("json_parses")
    claimed = receipt.pop("self_digest_sha256", None)
    fail(type(claimed) is str and claimed == sha(receipt), None, False,
         "producer self digest")
    fail(receipt.get("schema") == SELF_SCHEMA and receipt.get("status") == "COMPLETE" and
         receipt.get("production_input") is False and
         receipt.get("synthetic_linear_fixture") is True and
         receipt.get("actual_a5_a6_milestone") is False,
         "production_input")
    independent = []
    for case in source["cases"]:
        meter.begin(case["name"])
        independent.append(reconstruct(case))
    for index, (context, produced) in enumerate(zip(independent, receipt["cases"])):
        context["receipt"] = produced
        meter.current = meter.cases[index]
        verify_receipt(produced, context)
    meter.begin("mutation-controls")
    controls = [mutation_control(wrapper, source, independent, owner) for owner in OWNERS]
    body = {"schema": SELF_SCHEMA, "status": "COMPLETE",
            "terminal": PASS, "source_binding": wrapper["source_binding"],
            "cases": [{"case": item["case"]["name"], "terminal": item["terminal"],
                       "closure_rank": len(item["accepted"]),
                       "closure_queue_pops": item["pops"],
                       "closure_candidate_count": len(item["transcript"]),
                       "kernel_dim": len(item["kernel_basis"]),
                       "Hd1_rank": len(item["hd1_rows"]),
                       "checker_closure_tableau_sha256": item["closure_tableau"].transcript_sha256,
                       "checker_Hd1_tableau_sha256": item["hd1_tableau"].transcript_sha256 if item["hd1_tableau"] else None}
                      for item in independent],
            "producer_receipt_digest_sha256": sha(receipt),
            "mutation_controls": controls, "mutation_attempted": len(controls),
            "mutation_rejected": len(controls), "production_input": False,
            "synthetic_linear_fixture": True,
            "actual_a5_a6_milestone": False,
            "resource": {"per_case": copy.deepcopy(meter.cases),
                "totals": dict(meter.totals),
                "bounds": {"candidate_count": "N", "joint_width": 13,
                           "closure": "O(N*13*r)", "tableau": "O(r^2*(13+r))",
                           "nullspace": "O(r^2*q)", "solve": "O(h^2+13*h)",
                           "mutations": "O(44*(N+13^3))"}}}
    meter.rss()
    # Seal a detached final resource snapshot; reserve the hash, output
    # canonicalization, and write counters before taking that snapshot.
    meter.charge("canonicalizations", 2)
    meter.charge("serializations")
    meter.charge("output_writes")
    body["resource"]["totals"] = dict(meter.totals)
    body["resource"]["per_case"] = copy.deepcopy(meter.cases)
    saved_meter = CHECKER_METER
    CHECKER_METER = None
    body["verdict_digest_sha256"] = sha(body)
    payload = canonical(body) + b"\n"
    CHECKER_METER = saved_meter
    Path(output_path).write_bytes(payload)
    CHECKER_METER = None
    return body


def production(receipt_path, output_path, actual_input=None):
    if actual_input is not None:
        validate_actual_anchor(json.loads(Path(actual_input).read_text(encoding="utf-8")))
    receipt = json.loads(Path(receipt_path).read_text(encoding="utf-8"))
    claimed = receipt.pop("self_digest_sha256", None)
    fail(type(claimed) is str and claimed == sha(receipt), None, False,
         "production receipt seal")
    fail(receipt.get("schema") == VERSION and
         receipt.get("status") == STATIC and
         receipt.get("terminal") == STATIC and
         receipt.get("production_input") is False,
         "production_input")
    body = {"schema": VERSION, "status": STATIC, "terminal": STATIC,
            "producer_receipt_digest_sha256": sha(receipt),
            "production_input": False, "synthetic_linear_fixture": False,
            "actual_a5_a6_milestone": False}
    body["verdict_digest_sha256"] = sha(body)
    Path(output_path).write_bytes(canonical(body) + b"\n")
    return body


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"), required=True)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--actual-input", type=Path, default=None)
    args = parser.parse_args(argv)
    try:
        if args.mode == "SELFTEST":
            value = selftest(args.fixture, args.receipt, args.output)
            print(PASS + " mutation_attempted=44 mutation_rejected=44")
            print("R07_JOINT_SLICE_KERNEL_GENERAL_V13_CHECKER_TERMINAL SELFTEST_COMPLETE")
        else:
            load_wrapper(args.fixture)
            value = production(args.receipt, args.output, args.actual_input)
            print("R07_JOINT_SLICE_KERNEL_GENERAL_V13_CHECKER_TERMINAL " + value["terminal"])
    except UnknownResource as error:
        print("R07_JOINT_SLICE_KERNEL_GENERAL_V13_CHECKER_TERMINAL UNKNOWN_RESOURCE " + str(error))
        raise SystemExit(2)
    except (UnknownInput, IndependentReject) as error:
        print("R07_JOINT_SLICE_KERNEL_GENERAL_V13_CHECKER_TERMINAL UNKNOWN_INPUT " + str(error))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
