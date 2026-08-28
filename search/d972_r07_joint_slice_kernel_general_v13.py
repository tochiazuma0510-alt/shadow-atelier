#!/usr/bin/env python3
"""R07 v13 semantic rebase: live joint closure and coefficient certificates.

This file intentionally reads the immutable v11 literal fixture.  The v13
JSON is only a wrapper binding that source; it is never treated as the source
fixture.  All arithmetic is over F3 and all input values are checked before a
modulo operation.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
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
PASS = "R07_JOINT_SLICE_KERNEL_GENERAL_V13_PRODUCER_SELFTEST_PASS"
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
    "field_modulus": {"scope": "raw_case", "case_index": 1,
        "stage": "raw.field_modulus", "code": "M_FIELD_MODULUS",
        "reason": "field modulus is not F3"},
    "theta_seed": {"scope": "raw_case", "case_index": 1,
        "stage": "raw.theta_seed", "code": "M_THETA_SEED",
        "reason": "theta seed binding changed"},
    "theta_action": {"scope": "raw_case", "case_index": 1,
        "stage": "raw.theta_action", "code": "M_THETA_ACTION",
        "reason": "theta action owner changed"},
    "z_action": {"scope": "raw_case", "case_index": 1,
        "stage": "raw.z_action", "code": "M_Z_ACTION",
        "reason": "z action owner changed"},
    "eta_action": {"scope": "raw_case", "case_index": 1,
        "stage": "raw.eta_action", "code": "M_ETA_ACTION",
        "reason": "eta action owner changed"},
    "D_entry": {"scope": "raw_case", "case_index": 1,
        "stage": "raw.D_entry", "code": "M_D_ENTRY",
        "reason": "D map owner changed"},
    "O_entry": {"scope": "raw_case", "case_index": 1,
        "stage": "raw.O_entry", "code": "M_O_ENTRY",
        "reason": "O map owner changed"},
    "C_entry": {"scope": "raw_case", "case_index": 1,
        "stage": "raw.C_entry", "code": "M_C_ENTRY",
        "reason": "C map owner changed"},
    "action_order": {"scope": "raw_case", "case_index": 1,
        "stage": "raw.action_order", "code": "M_ACTION_ORDER",
        "reason": "action order binding changed"},
    "premature_C": {"scope": "raw_case", "case_index": 1,
        "stage": "raw.premature_C", "code": "M_PREMATURE_C",
        "reason": "C was applied before closure"},
    "target": {"scope": "raw_case", "case_index": 1,
        "stage": "raw.target", "code": "M_TARGET",
        "reason": "target membership changed"},
    "seed_index": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.seed_index", "code": "M_SEED_INDEX",
        "reason": "certificate seed index is invalid"},
    "parent": {"scope": "certificate", "case_index": 4,
        "stage": "certificate.parent", "code": "M_PARENT",
        "reason": "certificate parent is invalid"},
    "row_theta": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.row_theta", "code": "M_ROW_THETA",
        "reason": "certificate row theta does not replay"},
    "left_kernel": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.left_kernel", "code": "M_LEFT_KERNEL",
        "reason": "left-kernel basis content changed"},
    "Hd1": {"scope": "certificate", "case_index": 1,
        "stage": "certificate.Hd1", "code": "M_HD1",
        "reason": "Hd1 content changed"},
    "member_ancestry": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.member_ancestry", "code": "M_MEMBER_ANCESTRY",
        "reason": "member theta ancestry does not replay"},
    "dual": {"scope": "certificate", "case_index": 1,
        "stage": "certificate.dual", "code": "M_DUAL",
        "reason": "separating dual does not replay"},
    "terminal": {"scope": "certificate", "case_index": 1,
        "stage": "certificate.terminal", "code": "M_TERMINAL",
        "reason": "certificate terminal changed"},
    "production_input": {"scope": "wrapper", "case_index": 0,
        "stage": "wrapper.production_input", "code": "M_PRODUCTION_INPUT",
        "reason": "production input binding changed"},
    "closure_queue_pops": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.closure_queue_pops", "code": "M_CLOSURE_QUEUE_POPS",
        "reason": "closure queue pop count changed"},
    "context_pops": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.context_pops", "code": "M_CONTEXT_POPS",
        "reason": "context pop receipt changed"},
    "closure_candidate_count": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.closure_candidate_count", "code": "M_CLOSURE_CANDIDATE_COUNT",
        "reason": "closure candidate count changed"},
    "closure_queue_bound": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.closure_queue_bound", "code": "M_CLOSURE_QUEUE_BOUND",
        "reason": "closure queue bound changed"},
    "candidate_parent": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.candidate_parent", "code": "M_CANDIDATE_PARENT",
        "reason": "candidate parent changed"},
    "candidate_action": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.candidate_action", "code": "M_CANDIDATE_ACTION",
        "reason": "candidate action changed"},
    "candidate_decision": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.candidate_decision", "code": "M_CANDIDATE_DECISION",
        "reason": "candidate decision changed"},
    "candidate_normalization": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.candidate_normalization", "code": "M_CANDIDATE_NORMALIZATION",
        "reason": "candidate normalization changed"},
    "candidate_coefficients": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.candidate_coefficients", "code": "M_CANDIDATE_COEFFICIENTS",
        "reason": "candidate coefficients changed"},
    "candidate_rank": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.candidate_rank", "code": "M_CANDIDATE_RANK",
        "reason": "candidate rank changed"},
    "dependent_record_deletion": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.dependent_record_deletion", "code": "M_DEPENDENT_RECORD_DELETION",
        "reason": "dependent candidate record deleted"},
    "dependent_record_reorder": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.dependent_record_reorder", "code": "M_DEPENDENT_RECORD_REORDER",
        "reason": "dependent candidate records reordered"},
    "f3_plus3_coefficient": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.f3_plus3_coefficient", "code": "M_F3_PLUS3_COEFFICIENT",
        "reason": "coefficient is outside canonical F3"},
    "member_witness_equality": {"scope": "certificate", "case_index": 0,
        "stage": "certificate.member_witness_equality", "code": "M_MEMBER_WITNESS_EQUALITY",
        "reason": "member witness does not map to the target slice"},
    "a4_anchor_identity": {"scope": "anchor", "case_index": 0,
        "stage": "production.anchor.identity", "code": "M_A4_ANCHOR_IDENTITY",
        "reason": "A4 anchor receipt identity changed"},
    "anchor_least_index": {"scope": "anchor", "case_index": 0,
        "stage": "production.anchor.least_index", "code": "M_ANCHOR_LEAST_INDEX",
        "reason": "A4 anchor least index changed"},
    "anchor_projected_exponent": {"scope": "anchor", "case_index": 0,
        "stage": "production.anchor.projected_exponent", "code": "M_ANCHOR_PROJECTED_EXPONENT",
        "reason": "A4 projected exponent changed"},
    "anchor_inverse_scalar": {"scope": "anchor", "case_index": 0,
        "stage": "production.anchor.inverse_scalar", "code": "M_ANCHOR_INVERSE_SCALAR",
        "reason": "A4 inverse scalar changed"},
    "anchor_substituted_cube": {"scope": "anchor", "case_index": 0,
        "stage": "production.anchor.forbidden_cube", "code": "M_ANCHOR_SUBSTITUTED_CUBE",
        "reason": "superseded literal cube pair was supplied"},
    "anchor_word": {"scope": "anchor", "case_index": 0,
        "stage": "production.anchor.word", "code": "M_ANCHOR_WORD",
        "reason": "A4 anchor word changed"},
    "anchor_rho1_kernel": {"scope": "anchor", "case_index": 0,
        "stage": "production.anchor.rho1_kernel", "code": "M_ANCHOR_RHO1_KERNEL",
        "reason": "A4 anchor rho1 is not in K"},
    "anchor_rho0": {"scope": "anchor", "case_index": 0,
        "stage": "production.anchor.rho0", "code": "M_ANCHOR_RHO0",
        "reason": "A4 anchor rho0 replay failed"},
    "anchor_q_z0": {"scope": "anchor", "case_index": 0,
        "stage": "production.anchor.q_z0", "code": "M_ANCHOR_Q_Z0",
        "reason": "A4 anchor q value is not z0"},
    "base_pair_order": {"scope": "anchor", "case_index": 0,
        "stage": "production.anchor.base_pair_order", "code": "M_BASE_PAIR_ORDER",
        "reason": "corrected base-pair order changed"},
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


class SemanticReject(Exception):
    """Narrow rejection emitted by a real owner gate during mutation tests."""
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
        if field not in self.FIELDS:
            raise RuntimeError("unknown meter field")
        amount = check_int(amount, "meter amount", nonnegative=True)
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


def check_int(value, label, nonnegative=False):
    if type(value) is not int:
        raise UnknownInput(label + " must be an exact int")
    if nonnegative and value < 0:
        raise UnknownInput(label + " must be nonnegative")
    return value


def f3(value, label):
    if type(value) is not int or value not in (0, 1, 2):
        raise UnknownInput(label + " is not canonical F3")
    return value


def _shape_matrix(matrix, rows, columns, label):
    if type(matrix) is not list or len(matrix) != rows:
        raise UnknownInput(label + " row shape")
    for i, row in enumerate(matrix):
        if type(row) is not list or len(row) != columns:
            raise UnknownInput(label + " column shape")
        for j, value in enumerate(row):
            f3(value, "%s[%d][%d]" % (label, i, j))


def f3_vector(vector, width, label):
    if type(vector) is not list or len(vector) != width:
        raise UnknownInput(label + " vector shape")
    for i, value in enumerate(vector):
        f3(value, "%s[%d]" % (label, i))


def f3_tree(value, label):
    """Canonical validation for coefficient-bearing receipt subtrees."""
    if type(value) is int:
        f3(value, label)
    elif type(value) is list:
        for index, item in enumerate(value):
            f3_tree(item, "%s[%d]" % (label, index))
    elif type(value) is dict:
        for key, item in value.items():
            f3_tree(item, "%s.%s" % (label, key))
    else:
        raise UnknownInput(label + " contains noncanonical coefficient")


def canon(value, meter=None):
    if meter is not None:
        meter.charge("canonicalizations")
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest(value, meter=None):
    if meter is not None:
        meter.charge("serializations")
    return hashlib.sha256(canon(value, meter)).hexdigest()


def record_digest(record, meter=None):
    body = dict(record)
    body.pop("record_sha256", None)
    return digest(body, meter)


def addv(left, right, meter=None):
    if len(left) != len(right):
        raise UnknownInput("vector addition width")
    if meter is not None:
        meter.charge("field_operations", len(left))
    return [(x + y) % 3 for x, y in zip(left, right)]


def submul(left, scalar, right, meter=None):
    if len(left) != len(right) or scalar not in (0, 1, 2):
        raise UnknownInput("field subtraction shape")
    if meter is not None:
        meter.charge("field_operations", len(left))
    return [(x - scalar * y) % 3 for x, y in zip(left, right)]


def matvec(matrix, vector, meter=None):
    if type(matrix) is not list or type(vector) is not list:
        raise UnknownInput("matvec type")
    if matrix and len(matrix[0]) != len(vector):
        raise UnknownInput("matvec dimension")
    if meter is not None:
        meter.charge("field_operations", sum(len(row) for row in matrix))
    return [sum(matrix[i][j] * vector[j] for j in range(len(vector))) % 3
            for i in range(len(matrix))]


def matmul(left, right, meter=None):
    if not left or not right or len(left[0]) != len(right):
        raise UnknownInput("matrix multiplication dimension")
    width = len(right[0])
    if any(len(row) != len(left[0]) for row in left):
        raise UnknownInput("left matrix rectangle")
    if any(len(row) != width for row in right):
        raise UnknownInput("right matrix rectangle")
    if meter is not None:
        meter.charge("field_operations", len(left) * len(left[0]) * width)
    return [[sum(left[i][k] * right[k][j] for k in range(len(right))) % 3
             for j in range(width)] for i in range(len(left))]


def lincomb(rows, coefficients, width, meter=None):
    if len(rows) != len(coefficients):
        raise UnknownInput("linear combination arity")
    for row in rows:
        f3_vector(row, width, "linear combination row")
    for i, value in enumerate(coefficients):
        f3(value, "linear combination coefficient[%d]" % i)
    result = [0] * width
    for coefficient, row in zip(coefficients, rows):
        for column, value in enumerate(row):
            result[column] = (result[column] + coefficient * value) % 3
    if meter is not None:
        meter.charge("coefficient_updates", len(rows) * width)
    return result


def rref(matrix, width=None, meter=None):
    work = [list(row) for row in matrix]
    if width is None:
        width = len(work[0]) if work else 0
    for row in work:
        f3_vector(row, width, "rref row")
    pivots, row_index = [], 0
    for column in range(width):
        pivot = next((i for i in range(row_index, len(work))
                      if work[i][column] != 0), None)
        if pivot is None:
            continue
        work[row_index], work[pivot] = work[pivot], work[row_index]
        scale = 1 if work[row_index][column] == 1 else 2
        work[row_index] = [(scale * value) % 3 for value in work[row_index]]
        if meter is not None:
            meter.charge("pivot_reductions")
        for i in range(len(work)):
            if i == row_index or work[i][column] == 0:
                continue
            work[i] = submul(work[i], work[i][column], work[row_index], meter)
            if meter is not None:
                meter.charge("pivot_reductions")
        pivots.append(column)
        row_index += 1
        if row_index == len(work):
            break
    return work, pivots


def matrix_rank(matrix, width=None, meter=None):
    if width is None:
        width = len(matrix[0]) if matrix else 0
    return len(rref(matrix, width, meter)[1])


def nullspace(matrix, width, meter=None):
    reduced, pivots = rref(matrix, width, meter)
    free = [column for column in range(width) if column not in pivots]
    basis = []
    for free_column in free:
        answer = [0] * width
        answer[free_column] = 1
        for row_index, pivot in reversed(list(enumerate(pivots))):
            answer[pivot] = (-sum(reduced[row_index][j] * answer[j]
                                  for j in free)) % 3
            if meter is not None:
                meter.charge("nullspace_work")
        basis.append(answer)
    return basis


class RetainedF3Basis:
    """One live online owner: normalized rows plus raw-roster transforms."""
    def __init__(self, width, name, meter=None):
        self.width = width
        self.name = name
        self.meter = meter
        self.raw_rows, self.raw_labels, self.reductions = [], [], []
        self._pivots = {}

    @property
    def rank(self):
        return len(self.raw_rows)

    @property
    def pivots(self):
        return sorted(self._pivots)

    def reduce(self, row):
        f3_vector(row, self.width, self.name + " candidate")
        remainder = list(row)
        coefficients = [0] * len(self.raw_rows)
        for pivot in self.pivots:
            multiple = remainder[pivot]
            if multiple:
                pivot_owner = self._pivots[pivot]
                remainder = submul(remainder, multiple,
                                   pivot_owner["row"], self.meter)
                coefficients = [
                    (x + multiple * y) % 3
                    for x, y in zip(coefficients, pivot_owner["transform"])
                ]
                if self.meter is not None:
                    self.meter.charge("coefficient_updates", len(coefficients))
                    self.meter.charge("pivot_reductions")
        replay = addv(lincomb(self.raw_rows, coefficients, self.width,
                              self.meter), remainder, self.meter)
        if replay != row:
            raise UnknownInput(self.name + " reduction invariant")
        return remainder, coefficients

    def consider(self, row, label, meter=None):
        if meter is None:
            meter = self.meter
        original = list(row)
        prior_rank = self.rank
        remainder, prior_coefficients = self.reduce(original)
        accepted = any(remainder)
        accepted_index = None
        pivot, normalization, normalized, transform = None, None, None, None
        if accepted:
            accepted_index = len(self.raw_rows)
            pivot = next(i for i, value in enumerate(remainder) if value)
            normalization = 1 if remainder[pivot] == 1 else 2
            normalized = [(normalization * value) % 3
                          for value in remainder]
            transform = [(-normalization * value) % 3
                         for value in prior_coefficients] + [normalization]
            # Padding is before roster growth and before any old-row update.
            for item in self._pivots.values():
                item["transform"].append(0)
            self.raw_rows.append(original)
            self.raw_labels.append(copy.deepcopy(label))
            for old_pivot in self.pivots:
                old = self._pivots[old_pivot]
                multiple = old["row"][pivot]
                if multiple:
                    old["row"] = submul(old["row"], multiple,
                                         normalized, meter)
                    old["transform"] = [
                        (x - multiple * y) % 3
                        for x, y in zip(old["transform"], transform)
                    ]
                    if meter is not None:
                        meter.charge("coefficient_updates", len(transform))
            self._pivots[pivot] = {"row": normalized,
                                   "transform": transform}
            direct = [0] * len(self.raw_rows)
            direct[accepted_index] = 1
            post_rank = prior_rank + 1
        else:
            direct = list(prior_coefficients)
            post_rank = prior_rank
        record = {
            "candidate_index": len(self.reductions),
            "label": copy.deepcopy(label),
            "raw_row": original,
            "pre_rank": prior_rank,
            "prior_roster_size": prior_rank,
            "reduction_coefficients": list(prior_coefficients),
            "remainder": list(remainder),
            "accepted": accepted,
            "accepted_raw_index": accepted_index,
            "pivot": pivot,
            "normalization": normalization,
            "normalized_row": normalized,
            "normalized_transform": transform,
            "direct_coefficients": direct,
            "post_rank": post_rank,
        }
        self.reductions.append(record)
        return record

    def solve(self, target, meter=None):
        remainder, coefficients = self.reduce(target)
        if meter is not None:
            meter.charge("solve_work")
        return coefficients if not any(remainder) else None

    def contains(self, target, meter=None):
        return self.solve(target, meter) is not None

    def export(self, meter=None):
        pivots = self.pivots
        reduced = [self._pivots[p]["row"] for p in pivots]
        transforms = [self._pivots[p]["transform"] for p in pivots]
        recon = []
        for pivot, row, transform in zip(pivots, reduced, transforms):
            if row[pivot] != 1 or any(row[q] != 0 for q in pivots if q != pivot):
                raise UnknownInput(self.name + " normalization")
            if lincomb(self.raw_rows, transform, self.width, meter) != row:
                raise UnknownInput(self.name + " transform replay")
            recon.append(digest({"pivot": pivot, "transform": transform,
                "reconstructed_row": row}, meter))
        padded = []
        final_count = len(self.raw_rows)
        for source in self.reductions:
            record = copy.deepcopy(source)
            record["direct_coefficients"] += [0] * (
                final_count - len(record["direct_coefficients"]))
            prior = record["prior_roster_size"]
            replay = addv(lincomb(self.raw_rows[:prior],
                record["reduction_coefficients"], self.width, meter),
                record["remainder"], meter)
            if replay != record["raw_row"]:
                raise UnknownInput(self.name + " reduction replay")
            if lincomb(self.raw_rows, record["direct_coefficients"],
                       self.width, meter) != record["raw_row"]:
                raise UnknownInput(self.name + " direct replay")
            record["direct_reconstruction_sha256"] = digest({
                key: record[key] for key in (
                    "candidate_index", "label", "raw_row", "accepted",
                    "accepted_raw_index", "direct_coefficients")}, meter)
            padded.append(record)
        body = {
            "owner": self.name, "width": self.width, "rank": self.rank,
            "insertion_order": copy.deepcopy(self.raw_labels),
            "raw_rows": copy.deepcopy(self.raw_rows), "pivots": pivots,
            "reduced_rows": copy.deepcopy(reduced),
            "transforms": copy.deepcopy(transforms),
            "reconstruction_digests_sha256": recon, "reductions": padded,
        }
        body["owner_digest_sha256"] = digest(body, meter)
        return body


def replay_owner(owner, meter=None):
    body = dict(owner)
    claimed = body.pop("owner_digest_sha256", None)
    if type(claimed) is not str or claimed != digest(body, meter):
        raise UnknownInput("owner export seal")
    width = check_int(owner["width"], "owner width", nonnegative=True)
    rows = owner["raw_rows"]
    rank = check_int(owner["rank"], "owner rank", nonnegative=True)
    if rank != len(rows) or rank != len(owner["insertion_order"]):
        raise UnknownInput("owner roster")
    for row in rows:
        f3_vector(row, width, "owner raw row")
    if len(owner["pivots"]) != len(owner["reduced_rows"]) \
            or len(owner["pivots"]) != len(owner["transforms"]) \
            or len(owner["pivots"]) != len(owner["reconstruction_digests_sha256"]):
        raise UnknownInput("owner transform arity")
    for pivot, row, transform, claimed_digest in zip(
            owner["pivots"], owner["reduced_rows"], owner["transforms"],
            owner["reconstruction_digests_sha256"]):
        check_int(pivot, "owner pivot")
        f3_vector(row, width, "owner reduced row")
        f3_vector(transform, rank, "owner transform")
        if lincomb(rows, transform, width, meter) != row:
            raise UnknownInput("owner transform replay")
        if claimed_digest != digest({"pivot": pivot, "transform": transform,
                                     "reconstructed_row": row}, meter):
            raise UnknownInput("owner reconstruction digest")
    accepted = 0
    for index, record in enumerate(owner["reductions"]):
        if record["candidate_index"] != index or record["prior_roster_size"] != accepted:
            raise UnknownInput("owner reduction order")
        prior = record["prior_roster_size"]
        f3_vector(record["raw_row"], width, "owner candidate")
        f3_vector(record["remainder"], width, "owner remainder")
        f3_vector(record["reduction_coefficients"], prior, "owner reduction coefficients")
        f3_vector(record["direct_coefficients"], rank, "owner direct coefficients")
        if addv(lincomb(rows[:prior], record["reduction_coefficients"], width,
                        meter), record["remainder"], meter) != record["raw_row"]:
            raise UnknownInput("owner reduction transcript")
        if lincomb(rows, record["direct_coefficients"], width, meter) != record["raw_row"]:
            raise UnknownInput("owner direct transcript")
        expected_digest = digest({key: record[key] for key in (
            "candidate_index", "label", "raw_row", "accepted",
            "accepted_raw_index", "direct_coefficients")}, meter)
        if record.get("direct_reconstruction_sha256") != expected_digest:
            raise UnknownInput("owner direct digest")
        if record["accepted"] is True:
            if record["accepted_raw_index"] != accepted or \
                    record["raw_row"] != rows[accepted] or not any(record["remainder"]):
                raise UnknownInput("owner accepted transcript")
            accepted += 1
        elif record["accepted"] is False:
            if record["accepted_raw_index"] is not None or any(record["remainder"]):
                raise UnknownInput("owner dependent transcript")
        else:
            raise UnknownInput("owner decision type")
    if accepted != rank:
        raise UnknownInput("owner accepted count")


def expected_cases_from_source(source):
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


def source_path():
    return (ROOT / SOURCE_REL).resolve()


def load_wrapper(path, meter=None):
    path = Path(path).resolve()
    if not path.is_file():
        raise UnknownInput("v13 wrapper is missing")
    if meter is not None:
        meter.charge("json_reads")
    value = json.loads(path.read_text(encoding="utf-8"))
    if meter is not None:
        meter.charge("json_parses")
    if value.get("schema") != SELF_SCHEMA:
        raise UnknownInput("v13 wrapper schema")
    binding = value.get("source_binding")
    if not isinstance(binding, dict):
        raise UnknownInput("source binding object")
    if binding.get("resolved_path") != str(source_path()) or \
            binding.get("relative_path") != SOURCE_REL or \
            binding.get("bytes") != SOURCE_BYTES or \
            binding.get("sha256") != SOURCE_SHA256 or \
            binding.get("schema") != SOURCE_SCHEMA or \
            binding.get("fixture_seal") != SOURCE_SEAL:
        raise UnknownInput("v13 source binding")
    if type(binding.get("bytes")) is not int or binding["bytes"] < 0:
        raise UnknownInput("v13 source byte type")
    if value.get("production_input") is not False:
        raise UnknownInput("v13 production input binding")
    if value.get("synthetic_linear_fixture") is not True or \
            value.get("actual_a5_a6_milestone") is not False:
        raise UnknownInput("v13 synthetic/actual milestone binding")
    if value.get("trailing_zero_repairs") != TRAILING_ZERO_REPAIRS:
        raise UnknownInput("v11 trailing-zero repair binding")
    if value.get("trace_expectations") != TRACE_EXPECTATIONS:
        raise UnknownInput("v13 trace expectation binding")
    if value.get("expected_cases") != expected_cases_from_source({}):
        raise UnknownInput("v13 expected tuple binding")
    for data in value["expected_cases"].values():
        for field in ("closure_rank", "kernel_dim",
                      "full_nonzero_kernel_cardinality", "Hd1_rank"):
            check_int(data.get(field), "v13 expected " + field, nonnegative=True)
        if data.get("member_theta") is not None:
            f3_vector(data["member_theta"], 2, "v13 expected member theta")
        if data.get("dual") is not None:
            f3_vector(data["dual"], 2, "v13 expected dual")
    for trace in value["trace_expectations"]:
        for field in ("seed_count", "action_applications", "candidate_count",
                      "queue_pops", "closure_rank", "kernel_dim", "Hd1_rank"):
            check_int(trace.get(field), "v13 trace " + field, nonnegative=True)
    check_anchor_contract(value, mutation=False)
    if value.get("mutation_roster") != list(OWNERS) or \
            value.get("mutation_registry") != MUTATION_REGISTRY:
        raise UnknownInput("v13 mutation registry")
    return value


def load_source(meter=None):
    path = source_path()
    if not path.is_file():
        raise UnknownInput("immutable v11 fixture missing")
    raw = path.read_bytes()
    if meter is not None:
        meter.charge("json_reads")
    if len(raw) != SOURCE_BYTES or hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise UnknownInput("immutable v11 fixture bytes or SHA drift")
    source = json.loads(raw.decode("utf-8"))
    if meter is not None:
        meter.charge("json_parses")
    return source


def gate(condition, owner, mutation=False):
    if condition is True:
        return
    if mutation:
        entry = MUTATION_REGISTRY[owner]
        raise SemanticReject(entry["stage"], entry["code"], entry["reason"])
    raise UnknownInput("owner gate: " + owner)


def check_source(source, mutation=False):
    gate(source.get("schema") == SOURCE_SCHEMA, "production_input", mutation)
    gate(source.get("fixture_seal") == SOURCE_SEAL, "production_input", mutation)
    gate(type(source.get("modulus")) is int and source["modulus"] == 3,
         "field_modulus", mutation)
    basis = {"Theta": ["theta0", "theta1"],
             "Z": ["z0", "z1"],
             "E_hat": ["occurrence%02d" % i for i in range(11)],
             "E": ["printed0"]}
    gate(source.get("typed_basis") == basis, "production_input", mutation)
    cases = source.get("cases")
    gate(type(cases) is list and len(cases) == 5, "production_input", mutation)
    expected = expected_cases_from_source(source)
    gate(source.get("expected_cases") == {
        name: {key: value for key, value in data.items() if key != "terminal"}
        for name, data in expected.items()}, "production_input", mutation)
    for data in source["expected_cases"].values():
        for field in ("closure_rank", "kernel_dim",
                      "full_nonzero_kernel_cardinality", "Hd1_rank"):
            check_int(data.get(field), "source expected " + field,
                      nonnegative=True)
        if data.get("member_theta") is not None:
            f3_vector(data["member_theta"], 2, "source expected member theta")
        if data.get("dual") is not None:
            f3_vector(data["dual"], 2, "source expected dual")
    # The v11 source registry is authenticated independently; v13's registry
    # is the expanded wrapper registry checked above.
    gate(source.get("mutation_roster") == list(OWNERS[:19]),
         "production_input", mutation)
    gate(source.get("mutation_registry") == {
        name: MUTATION_REGISTRY[name] for name in OWNERS[:19]},
         "production_input", mutation)
    seen_names = []
    for case_index, case in enumerate(cases):
        if type(case) is not dict:
            gate(False, "production_input", mutation)
        name = case.get("name")
        seen_names.append(name)
        gate(name in expected, "production_input", mutation)
        check_case_literals(case, mutation)
    gate(seen_names == list(expected), "production_input", mutation)
    return source


def check_case_literals(case, mutation=False):
    if mutation and "mutation_fixture_seal" in case:
        sealed = dict(case)
        claimed = sealed.pop("mutation_fixture_seal", None)
        gate(type(claimed) is str and claimed == digest(sealed),
             "production_input", mutation)
    name = case.get("name")
    gate(type(name) is str, "production_input", mutation)
    gate(name in expected_cases_from_source({}), "production_input", mutation)
    gate(type(case.get("modulus")) is int and case["modulus"] == 3,
         "field_modulus", mutation)
    gate(case.get("theta_seeds") == case.get("seed_bindings"),
         "theta_seed", mutation)
    for field, binding, owner in (
            ("A_theta", "A_theta_binding", "theta_action"),
            ("A_Z", "A_Z_binding", "z_action"),
            ("A_E", "A_E_binding", "eta_action"),
            ("D", "D_binding", "D_entry"),
            ("O", "O_binding", "O_entry"),
            ("C", "C_binding", "C_entry")):
        gate(case.get(field) == case.get(binding), owner, mutation)
    seeds = case.get("theta_seeds")
    gate(type(seeds) is list and len(seeds) >= 1, "theta_seed", mutation)
    for seed in seeds:
        f3_vector(seed, 2, "theta seed")
    gate(case.get("occurrence_count") == 11 and
         case.get("occurrence_tags") == ["occurrence%02d" % i for i in range(11)],
         "production_input", mutation)
    _shape_matrix(case.get("A_theta"), 2, 2, "A_theta")
    _shape_matrix(case.get("A_Z"), 2, 2, "A_Z")
    _shape_matrix(case.get("A_E"), 11, 11, "A_E")
    _shape_matrix(case.get("D"), 2, 2, "D")
    _shape_matrix(case.get("O"), 11, 2, "O")
    _shape_matrix(case.get("C"), 1, 11, "C")
    gate(matrix_rank(case["A_theta"], 2) == 2 and
         matrix_rank(case["A_Z"], 2) == 2 and
         matrix_rank(case["A_E"], 11) == 11,
         "production_input", mutation)
    gate(matmul(case["D"], case["A_theta"]) == matmul(case["A_Z"], case["D"]),
         "D_entry", mutation)
    gate(matmul(case["O"], case["A_theta"]) == matmul(case["A_E"], case["O"]),
         "O_entry", mutation)
    names, actions = case.get("action_names"), case.get("actions")
    gate(type(names) is list and type(actions) is list and
         len(names) == len(actions) and names == case.get("action_order_binding"),
         "action_order", mutation)
    gate(case.get("C_phase") == "after-closure", "premature_C", mutation)
    gate(case.get("left_kernel_method") == "rref" and case.get("parent_hint") == 0,
         "production_input", mutation)
    for index, action in enumerate(actions):
        gate(type(action) is dict and action.get("name") == names[index],
             "action_order", mutation)
        _shape_matrix(action.get("theta_matrix"), 2, 2, "action theta")
        _shape_matrix(action.get("z_matrix"), 2, 2, "action z")
        _shape_matrix(action.get("eta_matrix"), 11, 11, "action eta")
        gate(matrix_rank(action["theta_matrix"], 2) == 2 and
             matrix_rank(action["z_matrix"], 2) == 2 and
             matrix_rank(action["eta_matrix"], 11) == 11,
             "production_input", mutation)
        gate(matmul(case["D"], action["theta_matrix"]) ==
             matmul(action["z_matrix"], case["D"]), "D_entry", mutation)
        gate(matmul(case["O"], action["theta_matrix"]) ==
             matmul(action["eta_matrix"], case["O"]), "O_entry", mutation)
    target = case.get("target")
    f3_vector(target, 2, "target")
    gate(target == expected_cases_from_source({})[name]["member_theta"] or
         target == {"nonzero-member": [1, 1],
                    "outside-nonmember": [0, 1],
                    "zero-member": [0, 0],
                    "zero-nonmember": [1, 0],
                    "post-c-cancel": [1, 2]}[name], "target", mutation)
    gate(case.get("terminal") == {
        "nonzero-member": "MEMBER", "outside-nonmember": "NONMEMBER",
        "zero-member": "MEMBER", "zero-nonmember": "NONMEMBER",
        "post-c-cancel": "MEMBER"}[name], "production_input", mutation)


def direct_dual(rows, target, width, meter=None):
    # Solve [Hd1; target] * q = [0;1] by a polynomial augmented RREF.
    matrix = [list(row) + [0] for row in rows] + [list(target) + [1]]
    for row in matrix:
        f3_vector(row[:width], width, "dual equation")
        f3(row[width], "dual right side")
    reduced, pivots = rref_rhs(matrix, width, meter)
    for row in reduced:
        if not any(row[:width]) and row[width] != 0:
            return None
    result = [0] * width
    for row, pivot in zip(reduced, pivots):
        result[pivot] = row[width]
    return result


def rref_rhs(matrix, width, meter=None):
    """RREF whose last column is data, never an unknown pivot column."""
    work = [list(row) for row in matrix]
    pivots, row_index = [], 0
    for column in range(width):
        pivot = next((i for i in range(row_index, len(work))
                      if work[i][column] != 0), None)
        if pivot is None:
            continue
        work[row_index], work[pivot] = work[pivot], work[row_index]
        scale = 1 if work[row_index][column] == 1 else 2
        work[row_index] = [(scale * value) % 3 for value in work[row_index]]
        for i in range(len(work)):
            if i == row_index or work[i][column] == 0:
                continue
            factor = work[i][column]
            work[i] = [(x - factor * y) % 3
                       for x, y in zip(work[i], work[row_index])]
            if meter is not None:
                meter.charge("pivot_reductions")
        pivots.append(column)
        row_index += 1
        if row_index == len(work):
            break
    return work, pivots


def candidate_record(item, parent, action, candidate, pre_rank, basis_record,
                     queue_effect, queue_pop, meter):
    raw = {"theta": list(candidate["theta"]), "z": list(candidate["z"]),
           "eta": list(candidate["eta"]), "flat": list(candidate["flat"])}
    record = {
        "ordinal": None, "parent": parent, "action": action,
        "queue_pop_parent": queue_pop, "raw_candidate": raw,
        "pre_rank": pre_rank,
        "reduction_coefficients": list(basis_record["reduction_coefficients"]),
        "decision": "ACCEPTED" if basis_record["accepted"] else "DEPENDENT",
        "normalization": basis_record["normalization"],
        "normalized_row": basis_record["normalized_row"],
        "normalized_ancestry": basis_record["normalized_transform"],
        "post_rank": basis_record["post_rank"],
        "direct_coefficients": list(basis_record["direct_coefficients"]),
        "queue_effect": queue_effect,
        "basis_candidate_index": basis_record["candidate_index"],
    }
    record["raw_candidate_sha256"] = digest(raw, meter)
    return record


def compile_case(case, meter):
    check_case_literals(case)
    theta_dim, z_dim, eta_dim, quotient_dim = 2, 2, 11, 1
    closure = RetainedF3Basis(z_dim + eta_dim, "closure", meter)
    queue = deque()
    seen = set()
    transcript = []
    accepted_rows = []
    # Seeds are literal theta ancestry, with live D/O images.
    for seed_index, seed in enumerate(case["theta_seeds"]):
        theta = list(seed)
        z_value = matvec(case["D"], theta, meter)
        eta_value = matvec(case["O"], theta, meter)
        flat = z_value + eta_value
        candidate = {"theta": theta, "z": z_value, "eta": eta_value,
                     "flat": flat, "seed_index": seed_index,
                     "parent": None, "action": "seed", "kind": "seed"}
        meter.charge("candidate_constructions")
        basis_record = closure.consider(flat, {
            "kind": "seed", "seed_index": seed_index,
            "parent": None, "action": "seed"}, meter)
        queue_effect = "ENQUEUE_RANK_RAISE" if basis_record["accepted"] else "DEPENDENT"
        record = candidate_record(candidate, None, "seed", candidate,
            basis_record["pre_rank"], basis_record, queue_effect, None, meter)
        record["ordinal"] = len(transcript)
        record["record_sha256"] = record_digest(record, meter)
        transcript.append(record)
        if basis_record["accepted"]:
            accepted_index = len(accepted_rows)
            candidate["closure_index"] = accepted_index
            accepted_rows.append(candidate)
            queue.append(candidate)
            seen.add(tuple(flat))
        else:
            seen.add(tuple(flat))
    queue_bound = len(queue) + len(case["actions"]) * (
        len(case["theta_seeds"]) + len(case["actions"]) * 13)
    # This is a derived polynomial bound, never a stopping criterion.
    queue_bound = max(queue_bound, len(case["theta_seeds"]) +
                      len(case["actions"]) * max(1, 13))
    pops = 0
    while queue:
        item = queue.popleft()
        pops += 1
        meter.charge("queue_pops")
        parent_index = item["closure_index"]
        for action in case["actions"]:
            meter.charge("action_applications")
            name = action["name"]
            # Every stored matrix is applied to the live theta, z and eta.
            theta = matvec(action["theta_matrix"], item["theta"], meter)
            z_value = matvec(action["z_matrix"], item["z"], meter)
            eta_value = matvec(action["eta_matrix"], item["eta"], meter)
            gate(z_value == matvec(case["D"], theta, meter), "D_entry")
            gate(eta_value == matvec(case["O"], theta, meter), "O_entry")
            flat = z_value + eta_value
            candidate = {"theta": theta, "z": z_value, "eta": eta_value,
                         "flat": flat, "seed_index": item["seed_index"],
                         "parent": parent_index, "action": name,
                         "kind": "action"}
            meter.charge("candidate_constructions")
            basis_record = closure.consider(flat, {
                "kind": "action", "seed_index": item["seed_index"],
                "parent": parent_index, "action": name}, meter)
            key = tuple(flat)
            if basis_record["accepted"] and key not in seen:
                queue_effect = "ENQUEUE_RANK_RAISE"
            elif basis_record["accepted"]:
                queue_effect = "DEPENDENT_KEY_ALREADY_SEEN"
            else:
                queue_effect = "DEPENDENT"
            record = candidate_record(candidate, parent_index, name, candidate,
                basis_record["pre_rank"], basis_record, queue_effect, pops - 1, meter)
            record["ordinal"] = len(transcript)
            record["record_sha256"] = record_digest(record, meter)
            transcript.append(record)
            if basis_record["accepted"] and key not in seen:
                candidate["closure_index"] = len(accepted_rows)
                accepted_rows.append(candidate)
                queue.append(candidate)
                seen.add(key)
    if pops > queue_bound:
        raise UnknownResource("derived closure queue bound exhausted")
    # Freeze every direct coefficient/transform at the final raw-roster width.
    # Earlier records remain immutable mathematically, but their exported
    # coordinates are padded with zero as the roster grows.
    for record in transcript:
        record["direct_coefficients"] += [0] * (
            closure.rank - len(record["direct_coefficients"]))
        ancestry = record.get("normalized_ancestry")
        if ancestry is not None:
            record["normalized_ancestry"] = list(ancestry) + [0] * (
                closure.rank - len(ancestry))
        record["record_sha256"] = record_digest(record, meter)
    closure_rows = [item["flat"] for item in accepted_rows]
    if closure.raw_rows != closure_rows:
        raise UnknownInput("closure insertion order")
    # C is owned here, after complete occurrence-level closure.
    images = [matvec(case["C"], item["eta"], meter) for item in accepted_rows]
    kernel_matrix = [[images[j][i] for j in range(len(images))]
                     for i in range(quotient_dim)]
    kernel_basis = nullspace(kernel_matrix, len(accepted_rows), meter)
    hd1 = [lincomb([item["z"] for item in accepted_rows], coeff,
                   z_dim, meter) for coeff in kernel_basis]
    theta_hd1 = [lincomb([item["theta"] for item in accepted_rows], coeff,
                         theta_dim, meter) for coeff in kernel_basis]
    eta_hd1 = [lincomb([item["eta"] for item in accepted_rows], coeff,
                       eta_dim, meter) for coeff in kernel_basis]
    kernel_reconstruction = []
    for index, (coeff, theta, z_value, eta) in enumerate(
            zip(kernel_basis, theta_hd1, hd1, eta_hd1)):
        gate(z_value == matvec(case["D"], theta, meter), "D_entry")
        gate(matvec(case["C"], eta, meter) == [0], "C_entry")
        payload = {"kernel_basis_index": index,
                   "closure_coefficients": coeff,
                   "theta": theta, "z": z_value, "eta": eta}
        kernel_reconstruction.append(dict(payload,
            direct_reconstruction_sha256=digest(payload, meter)))
    hd1_owner = RetainedF3Basis(z_dim, "Hd1", meter)
    for index, row in enumerate(hd1):
        hd1_owner.consider(row, {"kernel_basis_index": index}, meter)
    target = list(case["target"])
    owner_coefficients = hd1_owner.solve(target, meter)
    is_member = owner_coefficients is not None
    terminal = "MEMBER" if is_member else "NONMEMBER"
    member_theta = ancestry = dual = None
    if is_member:
        hd1_coefficients = [0] * len(hd1)
        for raw_index, coefficient in enumerate(owner_coefficients):
            source_index = hd1_owner.raw_labels[raw_index]["kernel_basis_index"]
            hd1_coefficients[source_index] = coefficient
        closure_coefficients = [
            sum(hd1_coefficients[i] * kernel_basis[i][j]
                for i in range(len(kernel_basis))) % 3
            for j in range(len(accepted_rows))]
        member_theta = lincomb([item["theta"] for item in accepted_rows],
                               closure_coefficients, theta_dim, meter)
        member_z = lincomb([item["z"] for item in accepted_rows],
                           closure_coefficients, z_dim, meter)
        member_eta = lincomb([item["eta"] for item in accepted_rows],
                             closure_coefficients, eta_dim, meter)
        gate(member_z == target and matvec(case["D"], member_theta, meter) == target,
             "target")
        gate(matvec(case["C"], member_eta, meter) == [0], "C_entry")
        payload = {"Hd1_coefficients": hd1_coefficients,
                   "closure_coefficients": closure_coefficients,
                   "theta": member_theta, "z": member_z, "eta": member_eta}
        ancestry = dict(payload,
            direct_reconstruction_sha256=digest(payload, meter))
        meter.charge("ancestry_replays")
    else:
        dual = direct_dual(hd1_owner.raw_rows, target, z_dim, meter)
        if dual is None:
            raise UnknownInput("no separating dual")
        gate(all(sum(dual[i] * row[i] for i in range(z_dim)) % 3 == 0
                 for row in hd1_owner.raw_rows), "dual")
        gate(sum(dual[i] * target[i] for i in range(z_dim)) % 3 == 1, "dual")
    closure_export = closure.export(meter)
    hd1_export = hd1_owner.export(meter)
    replay_owner(closure_export, meter)
    replay_owner(hd1_export, meter)
    change_payload = {"closure_owner": closure_export,
        "Hd1_owner": hd1_export, "kernel_reconstruction": kernel_reconstruction,
        "member_ancestry": ancestry}
    body = {
        "case": case["name"], "terminal": terminal,
        "closure_rank": closure.rank, "closure_queue_pops": pops,
        "context_pops": pops, "closure_queue_bound": queue_bound,
        "closure_candidate_count": len(transcript),
        "production_input": False, "transcript": transcript,
        "rows": [{key: value for key, value in item.items()
                  if key != "closure_index"} for item in accepted_rows],
        "closure_owner": closure_export,
        "left_kernel_basis": kernel_basis,
        "kernel_reconstruction": kernel_reconstruction,
        "kernel_dim": len(kernel_basis),
        "full_nonzero_kernel_cardinality": 3 ** len(kernel_basis) - 1,
        "Hd1": hd1, "Hd1_rank": hd1_owner.rank,
        "Hd1_owner": hd1_export, "target": target,
        "member_theta": member_theta, "member_ancestry": ancestry,
        "dual": dual, "slice_membership": is_member,
        "change_of_basis_sha256": digest(change_payload, meter),
    }
    body["case_digest_sha256"] = digest(body, meter)
    return {"case": case, "receipt": body, "closure": closure,
            "Hd1_owner": hd1_owner, "kernel_basis": kernel_basis,
            "accepted_rows": accepted_rows}


def owner_value(obj, owner):
    if owner == "field_modulus": return obj.get("modulus")
    if owner == "theta_seed": return obj.get("theta_seeds")
    if owner in ("theta_action", "z_action", "eta_action", "D_entry", "O_entry", "C_entry"):
        return obj.get({"theta_action": "A_theta", "z_action": "A_Z",
                        "eta_action": "A_E", "D_entry": "D",
                        "O_entry": "O", "C_entry": "C"}[owner])
    if owner == "action_order": return obj.get("action_names")
    if owner == "premature_C": return obj.get("C_phase")
    if owner == "target": return obj.get("target")
    if owner == "seed_index": return [row.get("seed_index") for row in obj.get("rows", [])]
    if owner == "parent": return [row.get("parent") for row in obj.get("rows", [])]
    if owner == "row_theta": return [row.get("theta") for row in obj.get("rows", [])]
    if owner == "left_kernel": return obj.get("left_kernel_basis")
    if owner == "Hd1": return obj.get("Hd1")
    if owner == "member_ancestry": return obj.get("member_ancestry")
    if owner == "dual": return obj.get("dual")
    if owner == "terminal": return obj.get("terminal")
    if owner == "production_input": return obj.get("source_binding")
    if owner in ANCHOR_OWNERS:
        return obj.get("anchor_contract", {}).get({
            "a4_anchor_identity": "anchor_receipt_identity",
            "anchor_least_index": "least_index",
            "anchor_projected_exponent": "projected_exponent",
            "anchor_inverse_scalar": "inverse_scalar",
            "anchor_substituted_cube": "forbidden_pair",
            "anchor_word": "literal_word",
            "anchor_rho1_kernel": "rho1_kernel",
            "anchor_rho0": "rho0_replay",
            "anchor_q_z0": "q_z0_replay",
            "base_pair_order": "base_pair_order",
        }[owner])
    return obj.get(owner)


def mutate_raw(case, owner):
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
    else: raise RuntimeError("not a raw owner")
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
    elif owner in ("candidate_parent", "candidate_action", "candidate_decision",
                   "candidate_normalization", "candidate_coefficients", "candidate_rank"):
        record = value["transcript"][0]
        if owner == "candidate_parent": record["parent"] = 99
        elif owner == "candidate_action": record["action"] = "not-registered"
        elif owner == "candidate_decision": record["decision"] = "DEPENDENT" if record["decision"] == "ACCEPTED" else "ACCEPTED"
        elif owner == "candidate_normalization": record["normalization"] = 0
        elif owner == "candidate_coefficients": record["reduction_coefficients"] = [1]
        else: record["post_rank"] += 1
    elif owner == "dependent_record_deletion":
        value["transcript"] = value["transcript"][:-1]
    elif owner == "dependent_record_reorder":
        dependent = [i for i, row in enumerate(value["transcript"]) if row["decision"] == "DEPENDENT"]
        if len(dependent) < 2: raise RuntimeError("mutation fixture lacks two dependent records")
        i, j = dependent[:2]; value["transcript"][i], value["transcript"][j] = value["transcript"][j], value["transcript"][i]
    elif owner == "f3_plus3_coefficient": value["transcript"][0]["reduction_coefficients"] = [3]
    elif owner == "member_witness_equality": value["member_theta"][0] = (value["member_theta"][0] + 1) % 3
    else: raise RuntimeError("not a receipt owner")
    body = dict(value); body.pop("case_digest_sha256", None)
    value["case_digest_sha256"] = digest(body)
    return value


def validate_receipt(receipt, expected_context, mutation=False):
    expected = expected_context["receipt"]
    gate(receipt.get("case") == expected.get("case") and
         receipt.get("production_input") is False,
         "production_input", mutation)
    for field in ("closure_rank", "closure_queue_pops", "context_pops",
                  "closure_queue_bound", "closure_candidate_count",
                  "kernel_dim", "full_nonzero_kernel_cardinality", "Hd1_rank"):
        exact = receipt.get(field)
        if type(exact) is not int or exact < 0:
            raise UnknownInput("receipt scalar type: " + field)
    # Validate coefficient-bearing data before any arithmetic or digest replay.
    for index, record in enumerate(receipt.get("transcript", [])):
        for field in ("ordinal", "pre_rank", "post_rank", "basis_candidate_index"):
            if type(record.get(field)) is not int or record[field] < 0:
                raise UnknownInput("receipt transcript scalar type: " + field)
        raw = record.get("raw_candidate", {})
        for field, width in (("theta", 2), ("z", 2), ("eta", 11), ("flat", 13)):
            f3_vector(raw.get(field), width, "receipt.transcript[%d].%s" % (index, field))
        for field in ("reduction_coefficients", "normalized_ancestry", "direct_coefficients"):
            value = record.get(field)
            if value is not None:
                if type(value) is not list:
                    raise UnknownInput("receipt coefficient vector")
                for j, scalar in enumerate(value):
                    try:
                        f3(scalar, "receipt.transcript[%d].%s[%d]" % (index, field, j))
                    except UnknownInput:
                        gate(False, "f3_plus3_coefficient", mutation)
        if record.get("normalized_row") is not None:
            f3_vector(record["normalized_row"], 13,
                      "receipt transcript normalized row")
    for index, row in enumerate(receipt.get("rows", [])):
        for field, width in (("theta", 2), ("z", 2), ("eta", 11), ("flat", 13)):
            f3_vector(row.get(field), width, "receipt.rows[%d].%s" % (index, field))
    for index, row in enumerate(receipt.get("left_kernel_basis", [])):
        f3_vector(row, len(receipt.get("rows", [])), "receipt kernel[%d]" % index)
    for index, row in enumerate(receipt.get("Hd1", [])):
        f3_vector(row, 2, "receipt Hd1[%d]" % index)
    if receipt.get("member_theta") is not None:
        f3_vector(receipt["member_theta"], 2, "receipt member theta")
    if receipt.get("dual") is not None:
        f3_vector(receipt["dual"], 2, "receipt dual")
    # The two owner exports have their own exact scalar/shape and replay gate.
    replay_owner(receipt.get("closure_owner"), None)
    replay_owner(receipt.get("Hd1_owner"), None)
    if receipt.get("case_digest_sha256") != digest({
            key: value for key, value in receipt.items()
            if key != "case_digest_sha256"}):
        raise UnknownInput("receipt seal")
    def same(field, owner):
        gate(receipt.get(field) == expected.get(field), owner, mutation)
    for field, owner in (
        ("closure_queue_pops", "closure_queue_pops"),
        ("context_pops", "context_pops"),
        ("closure_candidate_count", "closure_candidate_count"),
        ("closure_queue_bound", "closure_queue_bound"),
        ("closure_rank", "candidate_rank"), ("kernel_dim", "candidate_rank"),
        ("full_nonzero_kernel_cardinality", "candidate_rank"),
        ("Hd1_rank", "Hd1"), ("target", "target"), ("terminal", "terminal"),
        ("slice_membership", "terminal"), ("member_ancestry", "member_ancestry"),
        ("dual", "dual"), ("left_kernel_basis", "left_kernel"),
        ("Hd1", "Hd1"), ("kernel_reconstruction", "left_kernel"),
        ("change_of_basis_sha256", "candidate_coefficients")):
        same(field, owner)
    if len(receipt.get("transcript", [])) != len(expected.get("transcript", [])):
        gate(False, "dependent_record_deletion", mutation)
    actual_order = [row.get("basis_candidate_index") for row in receipt.get("transcript", [])]
    expected_order = [row.get("basis_candidate_index") for row in expected.get("transcript", [])]
    actual_dependents = [row.get("basis_candidate_index") for row in receipt.get("transcript", [])
                         if row.get("decision") == "DEPENDENT"]
    expected_dependents = [row.get("basis_candidate_index") for row in expected.get("transcript", [])
                           if row.get("decision") == "DEPENDENT"]
    if actual_order != expected_order and set(actual_dependents) == set(expected_dependents):
        gate(False, "dependent_record_reorder", mutation)
    for index, (actual, wanted) in enumerate(zip(receipt.get("transcript", []), expected.get("transcript", []))):
        for field, owner in (("parent", "candidate_parent"), ("action", "candidate_action"),
                             ("decision", "candidate_decision"), ("normalization", "candidate_normalization"),
                             ("reduction_coefficients", "candidate_coefficients"),
                             ("post_rank", "candidate_rank"), ("raw_candidate", "candidate_action"),
                             ("queue_effect", "candidate_decision"),
                             ("normalized_row", "candidate_normalization"),
                             ("normalized_ancestry", "candidate_coefficients"),
                             ("direct_coefficients", "candidate_coefficients")):
            gate(actual.get(field) == wanted.get(field), owner, mutation)
        gate(actual.get("ordinal") == index, "candidate_rank", mutation)
        gate(actual.get("record_sha256") == wanted.get("record_sha256"),
             "candidate_decision", mutation)
    # Accepted-row occurrence data is a separate owner from the chronological
    # candidate records and must itself replay the live D/O maps.
    for index, (actual, wanted) in enumerate(zip(receipt.get("rows", []), expected.get("rows", []))):
        for field in ("seed_index", "parent", "action", "kind", "theta", "z", "eta", "flat"):
            gate(actual.get(field) == wanted.get(field),
                 "seed_index" if field == "seed_index" else
                 "parent" if field == "parent" else
                 "row_theta" if field in ("theta", "z", "eta", "flat") else
                 "candidate_action", mutation)
    # Dependent-record ordering is a semantic chronological gate, not a digest gate.
    dependent_ordinals = [row["ordinal"] for row in receipt["transcript"] if row["decision"] == "DEPENDENT"]
    expected_dependents = [row["ordinal"] for row in expected["transcript"] if row["decision"] == "DEPENDENT"]
    gate(dependent_ordinals == expected_dependents, "dependent_record_reorder", mutation)
    if receipt.get("member_theta") is not None:
        theta = receipt["member_theta"]
        f3_vector(theta, 2, "member theta")
        gate(matvec(expected_context["case"]["D"], theta) == receipt["target"],
             "member_witness_equality", mutation)
        if receipt.get("member_ancestry") is not None:
            gate(receipt["member_ancestry"].get("theta") == theta,
                 "member_ancestry", mutation)
    return True


def mutation_control(wrapper, source, contexts, owner, meter=None):
    if meter is not None:
        meter.charge("mutation_work")
    entry = MUTATION_REGISTRY[owner]
    context = contexts[entry["case_index"]]
    if entry["scope"] == "raw_case":
        before = source["cases"][entry["case_index"]]
        mutated = mutate_raw(before, owner)
        owned_before, owned_after = digest(owner_value(before, owner)), digest(owner_value(mutated, owner))
        before_digest = digest(before)
        mutated["mutation_fixture_seal"] = digest(mutated)
        after_digest = digest(mutated)
        oracle = lambda: check_case_literals(mutated, mutation=True)
        seal_field, seal_value = "mutation_fixture_seal", mutated["mutation_fixture_seal"]
    elif entry["scope"] == "wrapper":
        before = wrapper
        mutated = copy.deepcopy(wrapper)
        mutated["source_binding"]["sha256"] = "0" * 64
        owned_before, owned_after = digest(owner_value(before, owner)), digest(owner_value(mutated, owner))
        before_digest, after_digest = digest(before), digest(mutated)
        oracle = lambda: load_wrapper_from_value(mutated, mutation=True)
        seal_field, seal_value = "source_binding.sha256", mutated["source_binding"]["sha256"]
    elif entry["scope"] == "anchor":
        before = wrapper
        mutated = copy.deepcopy(wrapper)
        field = {
            "a4_anchor_identity": "anchor_receipt_identity",
            "anchor_least_index": "least_index",
            "anchor_projected_exponent": "projected_exponent",
            "anchor_inverse_scalar": "inverse_scalar",
            "anchor_substituted_cube": "forbidden_pair",
            "anchor_word": "literal_word",
            "anchor_rho1_kernel": "rho1_kernel",
            "anchor_rho0": "rho0_replay",
            "anchor_q_z0": "q_z0_replay",
            "base_pair_order": "base_pair_order",
        }[owner]
        mutated["anchor_contract"][field] = "MUTATED_" + field
        oracle = lambda: load_wrapper_from_value(mutated, mutation=True)
        seal_field, seal_value = "anchor_contract." + field, mutated["anchor_contract"][field]
    else:
        before = context["receipt"]
        mutated = mutate_receipt(before, owner)
        owned_before, owned_after = digest(owner_value(before, owner)), digest(owner_value(mutated, owner))
        before_digest, after_digest = digest(before), digest(mutated)
        oracle = lambda: validate_receipt(mutated, context, mutation=True)
        seal_field, seal_value = "case_digest_sha256", mutated["case_digest_sha256"]
    if owned_before == owned_after or before_digest == after_digest:
        raise RuntimeError("mutation did not change owned canonical object")
    try:
        oracle()
    except SemanticReject as rejection:
        if (rejection.stage, rejection.code, rejection.reason) != (
                entry["stage"], entry["code"], entry["reason"]):
            raise RuntimeError("wrong mutation owner gate")
    else:
        raise RuntimeError("mutation accepted by semantic validator")
    return {"owner": owner, "scope": entry["scope"], "case_index": entry["case_index"],
            "owned_before_sha256": owned_before, "owned_after_sha256": owned_after,
            "canonical_before_sha256": before_digest, "canonical_after_sha256": after_digest,
            "seal_field": seal_field, "resealed_sha256": seal_value,
            "semantic_oracle_reached": True, "rejection_stage": entry["stage"],
            "rejection_code": entry["code"], "rejection_reason": entry["reason"]}


def load_wrapper_from_value(value, mutation=False):
    binding = value.get("source_binding", {})
    gate(value.get("schema") == SELF_SCHEMA, "production_input", mutation)
    gate(binding.get("resolved_path") == str(source_path()) and
         binding.get("relative_path") == SOURCE_REL and
         binding.get("bytes") == SOURCE_BYTES and
         binding.get("sha256") == SOURCE_SHA256 and
         binding.get("schema") == SOURCE_SCHEMA and
         binding.get("fixture_seal") == SOURCE_SEAL,
         "production_input", mutation)
    gate(value.get("production_input") is False, "production_input", mutation)
    gate(value.get("synthetic_linear_fixture") is True and
         value.get("actual_a5_a6_milestone") is False,
         "production_input", mutation)
    check_anchor_contract(value, mutation=mutation)
    return value


def check_anchor_contract(value, mutation=False):
    contract = value.get("anchor_contract")
    if type(contract) is not dict:
        gate(False, "a4_anchor_identity", mutation)
    gate(type(contract.get("required")) is bool and
         contract.get("required") is True,
         "a4_anchor_identity", mutation)
    for field, owner in (
            ("package", "a4_anchor_identity"),
            ("required", "a4_anchor_identity"),
            ("anchor_receipt_identity", "a4_anchor_identity"),
            ("least_index", "anchor_least_index"),
            ("projected_exponent", "anchor_projected_exponent"),
            ("inverse_scalar", "anchor_inverse_scalar"),
            ("anchor_word", "anchor_word"),
            ("literal_word", "anchor_word"),
            ("rho1_kernel", "anchor_rho1_kernel"),
            ("rho0_replay", "anchor_rho0"),
            ("q_z0_replay", "anchor_q_z0"),
            ("base_pair", "anchor_substituted_cube"),
            ("forbidden_pair", "anchor_substituted_cube"),
            ("base_pair_order", "base_pair_order")):
        expected = ANCHOR_CONTRACT[field]
        gate(contract.get(field) == expected, owner, mutation)
    gate(contract.get("base_pair") != contract.get("forbidden_pair"),
         "anchor_substituted_cube", mutation)


def validate_actual_anchor(anchor, mutation=False):
    """Production ABI gate for an external accepted A4 anchor receipt.

    The synthetic five-case source has no word anchor.  If an actual input is
    ever supplied, this gate requires typed anchor data and rejects the
    superseded literal cube before any A5 pair is compiled.
    """
    gate(type(anchor) is dict, "a4_anchor_identity", mutation)
    gate(anchor.get("package") == ANCHOR_CONTRACT["package"],
         "a4_anchor_identity", mutation)
    gate(type(anchor.get("anchor_receipt_identity")) is str and
         anchor.get("anchor_receipt_identity"), "a4_anchor_identity", mutation)
    gate(type(anchor.get("least_index")) is int and anchor["least_index"] >= 0,
         "anchor_least_index", mutation)
    gate(type(anchor.get("projected_exponent")) is int and
         anchor["projected_exponent"] in (1, 2),
         "anchor_projected_exponent", mutation)
    gate(type(anchor.get("inverse_scalar")) is int and
         anchor["inverse_scalar"] in (1, 2),
         "anchor_inverse_scalar", mutation)
    gate(type(anchor.get("literal_word")) is str and anchor["literal_word"],
         "anchor_word", mutation)
    rho1_in_kernel = anchor.get("rho1_in_kernel",
                                anchor.get("rho1_kernel"))
    gate(rho1_in_kernel is True, "anchor_rho1_kernel", mutation)
    gate(anchor.get("rho0_replay") is True, "anchor_rho0", mutation)
    gate(anchor.get("q_z0_replay") is True, "anchor_q_z0", mutation)
    pairs = anchor.get("base_pairs")
    gate(type(pairs) is list and pairs, "base_pair_order", mutation)
    for pair in pairs:
        gate(type(pair) is dict and pair.get("left") != pair.get("right"),
             "anchor_substituted_cube", mutation)
        gate("[x,y]^3" not in str(pair), "anchor_substituted_cube", mutation)
    gate(anchor.get("base_pair_order") == "CORRECTED_BASE_PAIRS_FIRST",
         "base_pair_order", mutation)
    return anchor


def corrected_base_pairs(anchor, coefficients, section_words):
    """Materialize the only permitted A3/A4 base-pair family.

    This helper is intentionally not used by the synthetic five-case path:
    that path has no source words.  An actual production caller supplies the
    accepted A4 anchor and section words, and receives literal pairs whose
    two endpoints are replayable independently.  The old projected cube is
    never an input to this constructor.
    """
    validate_actual_anchor(anchor)
    if type(coefficients) is not list or type(section_words) is not list \
            or len(coefficients) != len(section_words):
        raise UnknownInput("actual base-pair arity")
    literal_word = anchor["literal_word"]
    pairs = []
    for index, (coefficient, section) in enumerate(
            zip(coefficients, section_words)):
        f3(coefficient, "actual base coefficient[%d]" % index)
        if type(section) is not str or not section:
            raise UnknownInput("actual section word")
        pairs.append({"coefficient": coefficient,
                      "left": section + "*" + literal_word,
                      "right": section,
                      "formula": ANCHOR_CONTRACT["base_pair"],
                      "rho0_left": anchor["rho0_replay"],
                      "rho0_right": anchor["rho0_replay"]})
    return pairs


def selftest(wrapper_path, output_path):
    meter = Meter()
    wrapper = load_wrapper(wrapper_path, meter)
    source = load_source(meter)
    check_source(source)
    contexts = []
    for case in source["cases"]:
        meter.begin(case["name"])
        contexts.append(compile_case(case, meter))
    for context in contexts:
        expected = wrapper["expected_cases"][context["receipt"]["case"]]
        receipt = context["receipt"]
        for field in ("closure_rank", "kernel_dim", "full_nonzero_kernel_cardinality", "Hd1_rank"):
            if receipt[field] != expected[field]:
                raise UnknownInput("arithmetic expected tuple mismatch")
        if receipt["terminal"] != expected["terminal"] or \
                receipt["member_theta"] != expected["member_theta"] or \
                receipt["dual"] != expected["dual"]:
            raise UnknownInput("arithmetic terminal mismatch")
        validate_receipt(receipt, context)
    controls = [mutation_control(wrapper, source, contexts, owner, meter)
                for owner in OWNERS]
    meter.rss()
    body = {"schema": SELF_SCHEMA, "status": "COMPLETE", "terminal": PASS,
            "source_binding": wrapper["source_binding"],
            "cases": [context["receipt"] for context in contexts],
            "mutation_controls": controls, "mutation_attempted": len(controls),
            "mutation_rejected": len(controls), "production_input": False,
            "synthetic_linear_fixture": True,
            "actual_a5_a6_milestone": False,
            "resource": {"per_case": copy.deepcopy(meter.cases),
                          "totals": dict(meter.totals),
                          "bounds": {"candidates": "N", "joint_width": 13,
                                     "closure_rank": "r", "kernel_dim": "d",
                                     "Hd1_rank": "h", "basis": "O(N*13*r)",
                                     "nullspace": "O(r^2*13)",
                                     "solve": "O(h^2+13*h)",
                                     "mutations": "O(44*(N+13^3))"}}}
    # Reserve the final digest serialization, output serialization, and write
    # in the detached snapshot before sealing.  The snapshot therefore does
    # not change while either canonical byte string is being produced.
    meter.charge("canonicalizations", 2)
    meter.charge("serializations")
    meter.charge("output_writes")
    body["resource"]["totals"] = dict(meter.totals)
    body["resource"]["per_case"] = copy.deepcopy(meter.cases)
    body["self_digest_sha256"] = digest(body)
    Path(output_path).write_bytes(canon(body) + b"\n")
    return body


def production(output_path, actual_input=None):
    if actual_input is not None:
        raw = Path(actual_input).read_text(encoding="utf-8")
        validate_actual_anchor(json.loads(raw))
    body = {"schema": VERSION, "status": STATIC, "terminal": STATIC,
            "reason": "actual typed matrices are not staged", "production_input": False,
            "synthetic_linear_fixture": False,
            "actual_a5_a6_milestone": False}
    body["self_digest_sha256"] = digest(body)
    Path(output_path).write_bytes(canon(body) + b"\n")
    return body


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"), required=True)
    parser.add_argument("--fixture", type=Path, default=ROOT /
                        "search/certs/d972_r07_joint_slice_kernel_general_selftest_v13_20260829.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--actual-input", type=Path, default=None)
    args = parser.parse_args(argv)
    try:
        if args.mode == "SELFTEST":
            value = selftest(args.fixture, args.output)
            print(PASS)
            print("R07_JOINT_SLICE_KERNEL_GENERAL_V13_PRODUCER_TERMINAL SELFTEST_COMPLETE")
        else:
            load_wrapper(args.fixture)
            value = production(args.output, args.actual_input)
            print("R07_JOINT_SLICE_KERNEL_GENERAL_V13_PRODUCER_TERMINAL " + value["terminal"])
    except UnknownResource as error:
        print("R07_JOINT_SLICE_KERNEL_GENERAL_V13_PRODUCER_TERMINAL UNKNOWN_RESOURCE " + str(error))
        raise SystemExit(2)
    except UnknownInput as error:
        print("R07_JOINT_SLICE_KERNEL_GENERAL_V13_PRODUCER_TERMINAL UNKNOWN_INPUT " + str(error))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
