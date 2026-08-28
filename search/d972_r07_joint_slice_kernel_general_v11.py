#!/usr/bin/env python3
"""Typed coefficient/joint-slice kernel with retained F3 ancestry owners."""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-joint-slice-kernel-general/v11"
SELF = SCHEMA + "/selftest"
PASS = "R07_JOINT_SLICE_KERNEL_GENERAL_V11_PRODUCER_SELFTEST_PASS"
STATIC = "STATIC_BLOCKED:actual typed matrices are not staged"
FIXTURE = "search/certs/d972_r07_joint_slice_kernel_general_selftest_v11_20260828.json"
FIXTURE_SEAL = "literal-static-fixture-v11"
OWNERS = (
    "field_modulus", "theta_seed", "theta_action", "z_action",
    "eta_action", "D_entry", "O_entry", "C_entry", "action_order",
    "premature_C", "target", "seed_index", "parent", "row_theta",
    "left_kernel", "Hd1", "member_ancestry", "dual", "terminal",
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
                        "stage": "certificate.member_ancestry",
                        "code": "M_MEMBER_ANCESTRY",
                        "reason": "member theta ancestry does not replay"},
    "dual": {"scope": "certificate", "case_index": 1,
             "stage": "certificate.dual", "code": "M_DUAL",
             "reason": "separating dual does not replay"},
    "terminal": {"scope": "certificate", "case_index": 1,
                 "stage": "certificate.terminal", "code": "M_TERMINAL",
                 "reason": "certificate terminal changed"},
}


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def digest(value):
    return hashlib.sha256(canon(value)).hexdigest()


def vnorm(vector):
    return [int(x) % 3 for x in vector]


def vec(matrix, vector):
    return vnorm([sum(matrix[i][j] * vector[j]
                      for j in range(len(vector)))
                  for i in range(len(matrix))])


def mmul(left, right):
    return [[sum(left[i][k] * right[k][j]
                 for k in range(len(right))) % 3
             for j in range(len(right[0]))]
            for i in range(len(left))]


def lincomb(rows, coefficients, width):
    require(len(rows) == len(coefficients), "linear combination arity")
    value = [0] * width
    for coefficient, row in zip(coefficients, rows):
        require(len(row) == width, "linear combination width")
        for column, scalar in enumerate(row):
            value[column] = (value[column] + coefficient * scalar) % 3
    return value


def add_vectors(left, right):
    require(len(left) == len(right), "vector addition width")
    return [(x + y) % 3 for x, y in zip(left, right)]


def rref(matrix):
    work = [vnorm(row) for row in matrix]
    row_index = 0
    pivots = []
    for column in range(len(work[0]) if work else 0):
        pivot = next((i for i in range(row_index, len(work))
                      if work[i][column]), None)
        if pivot is None:
            continue
        work[row_index], work[pivot] = work[pivot], work[row_index]
        scale = 1 if work[row_index][column] == 1 else 2
        work[row_index] = [(scale * x) % 3 for x in work[row_index]]
        for i in range(len(work)):
            if i != row_index and work[i][column]:
                multiple = work[i][column]
                work[i] = [(x - multiple * y) % 3
                           for x, y in zip(work[i], work[row_index])]
        pivots.append(column)
        row_index += 1
        if row_index == len(work):
            break
    return work, pivots


def matrix_rank(rows):
    return len(rref(rows)[1])


def nullspace(matrix, width):
    reduced, pivots = rref(matrix)
    free = [column for column in range(width) if column not in pivots]
    basis = []
    for free_column in free:
        answer = [0] * width
        answer[free_column] = 1
        for row_index, pivot in reversed(list(enumerate(pivots))):
            answer[pivot] = (-sum(reduced[row_index][j] * answer[j]
                                  for j in free)) % 3
        basis.append(answer)
    return basis


def require(condition, message):
    if condition is not True:
        raise RuntimeError(message)


class SemanticReject(Exception):
    """The only exception which a mutation boundary may count as rejection."""

    def __init__(self, stage, code, reason):
        super().__init__(reason)
        self.stage = stage
        self.code = code
        self.reason = reason


def semantic_require(condition, owner):
    if condition is not True:
        entry = MUTATION_REGISTRY[owner]
        raise SemanticReject(entry["stage"], entry["code"], entry["reason"])


class RetainedF3Basis:
    """Online RREF owner carrying transforms in accepted-raw-row order."""

    def __init__(self, width, name):
        self.width = width
        self.name = name
        self.raw_rows = []
        self.raw_labels = []
        self._pivots = {}
        self.reductions = []

    @property
    def rank(self):
        return len(self.raw_rows)

    @property
    def pivots(self):
        return sorted(self._pivots)

    def reduce(self, row):
        original = vnorm(row)
        require(len(original) == self.width, self.name + " width")
        remainder = list(original)
        coefficients = [0] * len(self.raw_rows)
        for pivot in self.pivots:
            multiple = remainder[pivot]
            if multiple:
                owned = self._pivots[pivot]
                remainder = [(x - multiple * y) % 3
                             for x, y in zip(remainder, owned["row"])]
                coefficients = [(x + multiple * y) % 3
                                for x, y in zip(coefficients,
                                                owned["transform"])]
        reconstructed = add_vectors(
            lincomb(self.raw_rows, coefficients, self.width), remainder)
        require(reconstructed == original, self.name + " reduction replay")
        return remainder, coefficients

    def consider(self, row, label):
        original = vnorm(row)
        prior_count = len(self.raw_rows)
        remainder, prior_coefficients = self.reduce(original)
        accepted = any(remainder)
        accepted_index = None
        pivot = None
        if accepted:
            for owned in self._pivots.values():
                owned["transform"].append(0)
            accepted_index = len(self.raw_rows)
            self.raw_rows.append(original)
            self.raw_labels.append(copy.deepcopy(label))
            pivot = next(i for i, scalar in enumerate(remainder) if scalar)
            scale = 1 if remainder[pivot] == 1 else 2
            normalized = [(scale * x) % 3 for x in remainder]
            transform = [(-scale * x) % 3 for x in prior_coefficients] + [scale]
            for old_pivot in self.pivots:
                multiple = self._pivots[old_pivot]["row"][pivot]
                if multiple:
                    old = self._pivots[old_pivot]
                    old["row"] = [(x - multiple * y) % 3
                                  for x, y in zip(old["row"], normalized)]
                    old["transform"] = [
                        (x - multiple * y) % 3
                        for x, y in zip(old["transform"], transform)
                    ]
            self._pivots[pivot] = {"row": normalized,
                                   "transform": transform}
            direct_coefficients = [0] * len(self.raw_rows)
            direct_coefficients[accepted_index] = 1
        else:
            direct_coefficients = list(prior_coefficients)
        self.reductions.append({
            "candidate_index": len(self.reductions),
            "label": copy.deepcopy(label),
            "raw_row": original,
            "prior_roster_size": prior_count,
            "reduction_coefficients": prior_coefficients,
            "remainder": remainder,
            "accepted": accepted,
            "accepted_raw_index": accepted_index,
            "pivot": pivot,
            "direct_coefficients": direct_coefficients,
        })
        return accepted

    def solve(self, target):
        remainder, coefficients = self.reduce(target)
        return coefficients if not any(remainder) else None

    def contains(self, target):
        return self.solve(target) is not None

    def _padded_reductions(self):
        final_count = len(self.raw_rows)
        records = []
        for source in self.reductions:
            record = copy.deepcopy(source)
            record["direct_coefficients"] += [0] * (
                final_count - len(record["direct_coefficients"]))
            prior = record["prior_roster_size"]
            replay = add_vectors(
                lincomb(self.raw_rows[:prior],
                        record["reduction_coefficients"], self.width),
                record["remainder"])
            require(replay == record["raw_row"],
                    self.name + " recorded reduction replay")
            require(lincomb(self.raw_rows, record["direct_coefficients"],
                            self.width) == record["raw_row"],
                    self.name + " direct coefficient replay")
            payload = {key: record[key] for key in (
                "candidate_index", "label", "raw_row", "accepted",
                "accepted_raw_index", "direct_coefficients")}
            record["direct_reconstruction_sha256"] = digest(payload)
            records.append(record)
        return records

    def export(self):
        require(self.rank == len(self._pivots), self.name + " owner rank")
        pivots = self.pivots
        reduced_rows = [self._pivots[pivot]["row"] for pivot in pivots]
        transforms = [self._pivots[pivot]["transform"] for pivot in pivots]
        reconstruction_digests = []
        for pivot, reduced, transform in zip(pivots, reduced_rows, transforms):
            require(reduced[pivot] == 1, self.name + " normalized pivot")
            require(all(reduced[other] == 0 for other in pivots
                        if other != pivot), self.name + " reduced pivots")
            require(lincomb(self.raw_rows, transform, self.width) == reduced,
                    self.name + " transform replay")
            reconstruction_digests.append(digest({
                "pivot": pivot, "transform": transform,
                "reconstructed_row": reduced,
            }))
        require(all(self.contains(row) for row in self.raw_rows),
                self.name + " raw containment")
        body = {
            "owner": self.name,
            "width": self.width,
            "rank": self.rank,
            "insertion_order": copy.deepcopy(self.raw_labels),
            "raw_rows": copy.deepcopy(self.raw_rows),
            "pivots": pivots,
            "reduced_rows": copy.deepcopy(reduced_rows),
            "transforms": copy.deepcopy(transforms),
            "reconstruction_digests_sha256": reconstruction_digests,
            "reductions": self._padded_reductions(),
        }
        return dict(body, owner_digest_sha256=digest(body))


def replay_owner_export(owner):
    body = dict(owner)
    claimed = body.pop("owner_digest_sha256", None)
    require(type(claimed) is str and claimed == digest(body),
            "owner export seal")
    width = owner["width"]
    raw_rows = owner["raw_rows"]
    require(owner["rank"] == len(raw_rows) == len(owner["insertion_order"]),
            "owner export roster")
    require(len(owner["pivots"]) == len(owner["reduced_rows"]) ==
            len(owner["transforms"]) ==
            len(owner["reconstruction_digests_sha256"]) == owner["rank"] and
            owner["pivots"] == sorted(set(owner["pivots"])) and
            all(0 <= pivot < width for pivot in owner["pivots"]),
            "owner export transform arity")
    for pivot, reduced, transform, claimed_digest in zip(
            owner["pivots"], owner["reduced_rows"], owner["transforms"],
            owner["reconstruction_digests_sha256"]):
        require(lincomb(raw_rows, transform, width) == reduced,
                "owner exported transform")
        require(claimed_digest == digest({
            "pivot": pivot, "transform": transform,
            "reconstructed_row": reduced,
        }), "owner reconstruction digest")
    accepted_count = 0
    for candidate_index, record in enumerate(owner["reductions"]):
        require(record["candidate_index"] == candidate_index and
                record["prior_roster_size"] == accepted_count,
                "owner reduction order")
        prior = record["prior_roster_size"]
        require(add_vectors(
            lincomb(raw_rows[:prior], record["reduction_coefficients"], width),
            record["remainder"]) == record["raw_row"],
            "owner reduction transcript")
        require(lincomb(raw_rows, record["direct_coefficients"], width) ==
                record["raw_row"], "owner direct transcript")
        payload = {key: record[key] for key in (
            "candidate_index", "label", "raw_row", "accepted",
            "accepted_raw_index", "direct_coefficients")}
        require(record["direct_reconstruction_sha256"] == digest(payload),
                "owner direct reconstruction digest")
        if record["accepted"] is True:
            require(record["accepted_raw_index"] == accepted_count and
                    record["raw_row"] == raw_rows[accepted_count] and
                    record["label"] == owner["insertion_order"][accepted_count]
                    and any(record["remainder"]),
                    "owner accepted reduction")
            accepted_count += 1
        else:
            require(record["accepted_raw_index"] is None and
                    not any(record["remainder"]),
                    "owner dependent reduction")
    require(accepted_count == owner["rank"], "owner accepted count")


def check_square(matrix, size, label):
    require(isinstance(matrix, list) and len(matrix) == size and
            all(isinstance(row, list) and len(row) == size and
                all(type(x) is int and 0 <= x < 3 for x in row)
                for row in matrix), label + " matrix")
    require(matrix_rank(matrix) == size, label + " invertibility")


def check_map(matrix, rows, columns, label):
    require(isinstance(matrix, list) and len(matrix) == rows and
            all(isinstance(row, list) and len(row) == columns and
                all(type(x) is int and 0 <= x < 3 for x in row)
                for row in matrix), label + " map")


def _literal_matrix(matrix, rows, columns, label):
    require(isinstance(matrix, list) and len(matrix) == rows and
            all(isinstance(row, list) and len(row) == columns and
                all(type(x) is int and 0 <= x < 3 for x in row)
                for row in matrix), "fixture preflight dimensions " + label)


def fixture_preflight(value):
    shapes = {"A_theta": (2, 2), "A_Z": (2, 2), "A_E": (11, 11),
              "D": (2, 2), "O": (11, 2), "C": (1, 11)}
    require(isinstance(value.get("cases"), list) and
            len(value["cases"]) == 5, "fixture preflight case count")
    for case in value["cases"]:
        require(isinstance(case, dict), "fixture preflight case object")
        for base, binding in (
                ("A_theta", "A_theta_binding"),
                ("A_Z", "A_Z_binding"), ("A_E", "A_E_binding"),
                ("D", "D_binding"), ("O", "O_binding"),
                ("C", "C_binding")):
            rows, columns = shapes[base]
            left, right = case.get(base), case.get(binding)
            require(left == right,
                    "fixture preflight binding equality " + base)
            _literal_matrix(left, rows, columns, base)
            _literal_matrix(right, rows, columns, binding)
        names, actions = case.get("action_names"), case.get("actions")
        require(isinstance(names, list) and isinstance(actions, list) and
                len(actions) == len(names),
                "fixture preflight action count")
        for index, action in enumerate(actions):
            require(isinstance(action, dict) and
                    action.get("name") == names[index],
                    "fixture preflight action order")
            for field, rows, columns in (
                    ("theta_matrix", 2, 2), ("z_matrix", 2, 2),
                    ("eta_matrix", 11, 11)):
                _literal_matrix(action.get(field), rows, columns,
                                "action[%d].%s" % (index, field))
    return value


def validate_fixture(value):
    require(value.get("schema") == SELF and
            value.get("fixture_seal") == FIXTURE_SEAL,
            "fixture seal/schema")
    require(value.get("modulus") == 3 and
            len(value.get("cases", [])) == 5, "fixture cases")
    require(value.get("typed_basis") == {
        "Theta": ["theta0", "theta1"], "Z": ["z0", "z1"],
        "E_hat": ["occurrence%02d" % i for i in range(11)],
        "E": ["printed0"],
    }, "typed basis")
    require(set(value.get("expected_cases", {})) ==
            {case["name"] for case in value["cases"]},
            "fixture expectations")
    require(value.get("mutation_roster") == list(OWNERS),
            "mutation roster")
    require(value.get("mutation_registry") == MUTATION_REGISTRY,
            "mutation registry")
    return value


def parse_fixture(path):
    value = json.loads(path.read_text(encoding="utf-8"))
    return fixture_preflight(validate_fixture(value))


def compile_case(case):
    require(case.get("modulus") == 3, "modulus")
    require(case["theta_seeds"] == case["seed_bindings"], "theta seeds")
    require(case["A_theta"] == case["A_theta_binding"] and
            case["A_Z"] == case["A_Z_binding"] and
            case["A_E"] == case["A_E_binding"], "action owner")
    require(case["D"] == case["D_binding"] and
            case["O"] == case["O_binding"] and
            case["C"] == case["C_binding"], "map owner")
    require(case["action_names"] == case["action_order_binding"] and
            case["parent_hint"] == 0 and
            case["C_phase"] == "after-closure" and
            case["left_kernel_method"] == "rref", "control owner")
    require(case.get("occurrence_count") == 11 and
            case.get("occurrence_tags") ==
            ["occurrence%02d" % i for i in range(11)],
            "eleven occurrence")
    theta_dimension = len(case["theta_seeds"][0])
    z_dimension = len(case["D"])
    eta_dimension = len(case["O"])
    quotient_dimension = len(case["C"])
    check_square(case["A_theta"], theta_dimension, "A_theta")
    check_square(case["A_Z"], z_dimension, "A_Z")
    check_square(case["A_E"], eta_dimension, "A_E")
    check_map(case["D"], z_dimension, theta_dimension, "D")
    check_map(case["O"], eta_dimension, theta_dimension, "O")
    check_map(case["C"], quotient_dimension, eta_dimension, "C")
    require(mmul(case["D"], case["A_theta"]) ==
            mmul(case["A_Z"], case["D"]), "D equivariance")
    require(mmul(case["O"], case["A_theta"]) ==
            mmul(case["A_E"], case["O"]), "O equivariance")
    require(len(case["actions"]) == len(case["action_names"]) and
            len(case["theta_seeds"]) >= 1, "action/seed count")
    for name, action in zip(case["action_names"], case["actions"]):
        require(action["name"] == name, "action name")
        check_square(action["theta_matrix"], theta_dimension,
                     "stored theta action")
        check_square(action["z_matrix"], z_dimension, "stored z action")
        check_square(action["eta_matrix"], eta_dimension,
                     "stored eta action")
        require(mmul(case["D"], action["theta_matrix"]) ==
                mmul(action["z_matrix"], case["D"]) and
                mmul(case["O"], action["theta_matrix"]) ==
                mmul(action["eta_matrix"], case["O"]),
                "action equivariance")

    closure = RetainedF3Basis(z_dimension + eta_dimension,
                              "closure")
    queue = [{"theta": vnorm(seed), "seed_index": index,
              "parent": None, "action": "seed", "kind": "seed"}
             for index, seed in enumerate(case["theta_seeds"])]
    queued_flats = {
        tuple(vec(case["D"], item["theta"]) +
              vec(case["O"], item["theta"]))
        for item in queue
    }
    rows = []
    pops = 0
    maximum_pops = len(queue) + theta_dimension * len(case["actions"])
    while queue:
        pops += 1
        require(pops <= maximum_pops, "closure bound")
        item = queue.pop(0)
        z_value = vec(case["D"], item["theta"])
        eta_value = vec(case["O"], item["theta"])
        flat = z_value + eta_value
        label = {"queue_pop": pops - 1, "kind": item["kind"],
                 "seed_index": item["seed_index"],
                 "parent": item["parent"], "action": item["action"]}
        if not closure.consider(flat, label):
            continue
        item = dict(item, z=z_value, eta=eta_value, flat=flat)
        rows.append(item)
        for name, action in zip(case["action_names"], case["actions"]):
            candidate = vec(action["theta_matrix"], item["theta"])
            candidate_flat = (vec(case["D"], candidate) +
                              vec(case["O"], candidate))
            key = tuple(candidate_flat)
            if key not in queued_flats:
                queued_flats.add(key)
                queue.append({"theta": candidate,
                              "seed_index": item["seed_index"],
                              "parent": len(rows) - 1,
                              "action": name, "kind": "action"})
    require(closure.raw_rows == [item["flat"] for item in rows],
            "closure insertion order")
    images = [vec(case["C"], item["eta"]) for item in rows]
    kernel_matrix = [[images[j][i] for j in range(len(images))]
                     for i in range(quotient_dimension)]
    kernel_basis = nullspace(kernel_matrix, len(rows))
    hd1 = [lincomb([item["z"] for item in rows], coefficients,
                   z_dimension) for coefficients in kernel_basis]
    theta_hd1 = [lincomb([item["theta"] for item in rows], coefficients,
                         theta_dimension)
                 for coefficients in kernel_basis]
    eta_hd1 = [lincomb([item["eta"] for item in rows], coefficients,
                       eta_dimension) for coefficients in kernel_basis]
    kernel_reconstruction = []
    for index, (coefficients, h_value, theta_value, eta_value) in enumerate(
            zip(kernel_basis, hd1, theta_hd1, eta_hd1)):
        require(h_value == vec(case["D"], theta_value) and
                not any(vec(case["C"], eta_value)),
                "left kernel replay")
        payload = {"kernel_basis_index": index,
                   "closure_coefficients": coefficients,
                   "theta": theta_value, "z": h_value,
                   "eta": eta_value}
        kernel_reconstruction.append(
            dict(payload, direct_reconstruction_sha256=digest(payload)))

    hd1_owner = RetainedF3Basis(z_dimension, "Hd1")
    for index, h_value in enumerate(hd1):
        hd1_owner.consider(h_value, {"kernel_basis_index": index})
    target = vnorm(case["target"])
    owner_coefficients = hd1_owner.solve(target)
    is_member = owner_coefficients is not None
    require(case["terminal"] in ("MEMBER", "NONMEMBER"), "terminal enum")
    require(is_member == (case["terminal"] == "MEMBER"),
            "terminal/member")
    member_theta = None
    ancestry = None
    dual = None
    if is_member:
        hd1_coefficients = [0] * len(hd1)
        for raw_index, coefficient in enumerate(owner_coefficients):
            source = hd1_owner.raw_labels[raw_index]["kernel_basis_index"]
            hd1_coefficients[source] = coefficient
        closure_coefficients = [
            sum(hd1_coefficients[i] * kernel_basis[i][j]
                for i in range(len(kernel_basis))) % 3
            for j in range(len(rows))
        ]
        member_theta = lincomb([item["theta"] for item in rows],
                               closure_coefficients, theta_dimension)
        member_eta = lincomb([item["eta"] for item in rows],
                             closure_coefficients, eta_dimension)
        member_z = lincomb([item["z"] for item in rows],
                           closure_coefficients, z_dimension)
        require(member_z == target and
                vec(case["D"], member_theta) == target and
                not any(vec(case["C"], member_eta)),
                "member ancestry replay")
        payload = {
            "Hd1_coefficients": hd1_coefficients,
            "closure_coefficients": closure_coefficients,
            "theta": member_theta, "z": member_z,
            "eta": member_eta,
        }
        ancestry = dict(payload,
                        direct_reconstruction_sha256=digest(payload))
    else:
        dual = next((list(candidate) for candidate in
                     itertools.product(range(3), repeat=z_dimension)
                     if any(candidate) and
                     all(sum(candidate[i] * h_value[i]
                             for i in range(z_dimension)) % 3 == 0
                         for h_value in hd1_owner.raw_rows) and
                     sum(candidate[i] * target[i]
                         for i in range(z_dimension)) % 3 == 1), None)
        require(dual is not None, "dual")

    closure_export = closure.export()
    hd1_export = hd1_owner.export()
    replay_owner_export(closure_export)
    replay_owner_export(hd1_export)
    change_payload = {"closure_owner": closure_export,
                      "Hd1_owner": hd1_export,
                      "kernel_reconstruction": kernel_reconstruction,
                      "member_ancestry": ancestry}
    body = {
        "case": case["name"], "terminal": case["terminal"],
        "closure_rank": closure.rank, "closure_queue_pops": pops,
        "closure_queue_bound": maximum_pops, "rows": rows,
        "closure_owner": closure_export,
        "left_kernel_basis": kernel_basis,
        "kernel_reconstruction": kernel_reconstruction,
        "kernel_dim": len(kernel_basis),
        "full_nonzero_kernel_cardinality": 3 ** len(kernel_basis) - 1,
        "Hd1": hd1, "Hd1_rank": hd1_owner.rank,
        "Hd1_owner": hd1_export, "target": target,
        "member_theta": member_theta, "member_ancestry": ancestry,
        "dual": dual, "slice_membership": is_member,
        "change_of_basis_sha256": digest(change_payload),
    }
    receipt = dict(body, case_digest_sha256=digest(body))
    context = {"case": case, "receipt": receipt, "closure": closure,
               "Hd1_owner": hd1_owner, "kernel_basis": kernel_basis,
               "theta_hd1": theta_hd1, "eta_hd1": eta_hd1}
    audit_certificate(context)
    return context


def certificate_seal(receipt):
    body = dict(receipt)
    body.pop("case_digest_sha256", None)
    return digest(body)


def owner_value(scope_object, owner):
    if owner == "field_modulus":
        return scope_object["modulus"]
    if owner == "theta_seed":
        return scope_object["theta_seeds"]
    if owner == "theta_action":
        return scope_object["A_theta"]
    if owner == "z_action":
        return scope_object["A_Z"]
    if owner == "eta_action":
        return scope_object["A_E"]
    if owner == "D_entry":
        return scope_object["D"]
    if owner == "O_entry":
        return scope_object["O"]
    if owner == "C_entry":
        return scope_object["C"]
    if owner == "action_order":
        return scope_object["action_names"]
    if owner == "premature_C":
        return scope_object["C_phase"]
    if owner == "target":
        return scope_object["target"]
    if owner == "seed_index":
        return [row["seed_index"] for row in scope_object["rows"]]
    if owner == "parent":
        return [row["parent"] for row in scope_object["rows"]]
    if owner == "row_theta":
        return [row["theta"] for row in scope_object["rows"]]
    if owner == "left_kernel":
        return scope_object["left_kernel_basis"]
    if owner == "Hd1":
        return scope_object["Hd1"]
    if owner == "member_ancestry":
        return scope_object["member_ancestry"]
    if owner == "dual":
        return scope_object["dual"]
    if owner == "terminal":
        return scope_object["terminal"]
    raise RuntimeError("unknown mutation owner")


def mutate_raw(case, owner):
    mutated = copy.deepcopy(case)
    if owner == "field_modulus":
        mutated["modulus"] = 9
    elif owner == "theta_seed":
        mutated["theta_seeds"][0][0] = (
            mutated["theta_seeds"][0][0] + 1) % 3
    elif owner == "theta_action":
        mutated["A_theta"][0][0] = 2
    elif owner == "z_action":
        mutated["A_Z"][0][0] = 2
    elif owner == "eta_action":
        mutated["A_E"][0][0] = 2
    elif owner == "D_entry":
        mutated["D"][0][0] = 2
    elif owner == "O_entry":
        mutated["O"][0][0] = 2
    elif owner == "C_entry":
        mutated["C"][0][0] = 2
    elif owner == "action_order":
        mutated["action_names"] = ["mutated-action"]
    elif owner == "premature_C":
        mutated["C_phase"] = "before-closure"
    elif owner == "target":
        mutated["target"] = [1, 0]
    else:
        raise RuntimeError("raw mutation owner")
    return mutated


def mutate_certificate(receipt, owner):
    mutated = copy.deepcopy(receipt)
    if owner == "seed_index":
        mutated["rows"][1]["seed_index"] = 99
    elif owner == "parent":
        mutated["rows"][1]["parent"] = 99
    elif owner == "row_theta":
        mutated["rows"][1]["theta"][0] = (
            mutated["rows"][1]["theta"][0] + 1) % 3
    elif owner == "left_kernel":
        mutated["left_kernel_basis"][1] = copy.deepcopy(
            mutated["left_kernel_basis"][0])
    elif owner == "Hd1":
        mutated["Hd1"][0] = [1, 1]
    elif owner == "member_ancestry":
        mutated["member_ancestry"]["closure_coefficients"][0] = (
            mutated["member_ancestry"]["closure_coefficients"][0] + 1) % 3
        payload = {key: mutated["member_ancestry"][key] for key in (
            "Hd1_coefficients", "closure_coefficients", "theta", "z", "eta")}
        mutated["member_ancestry"]["direct_reconstruction_sha256"] = (
            digest(payload))
        mutated["change_of_basis_sha256"] = digest({
            "closure_owner": mutated["closure_owner"],
            "Hd1_owner": mutated["Hd1_owner"],
            "kernel_reconstruction": mutated["kernel_reconstruction"],
            "member_ancestry": mutated["member_ancestry"],
        })
    elif owner == "dual":
        mutated["dual"][0] = (mutated["dual"][0] + 1) % 3
    elif owner == "terminal":
        mutated["terminal"] = "MUTATED"
    else:
        raise RuntimeError("certificate mutation owner")
    mutated["case_digest_sha256"] = certificate_seal(mutated)
    return mutated


def raw_owner_oracle(case, owner, context):
    if owner == "field_modulus":
        semantic_require(case.get("modulus") == 3, owner)
    elif owner == "theta_seed":
        semantic_require(case["theta_seeds"] == case["seed_bindings"], owner)
    elif owner == "theta_action":
        semantic_require(case["A_theta"] == case["A_theta_binding"], owner)
    elif owner == "z_action":
        semantic_require(case["A_Z"] == case["A_Z_binding"], owner)
    elif owner == "eta_action":
        semantic_require(case["A_E"] == case["A_E_binding"], owner)
    elif owner == "D_entry":
        semantic_require(case["D"] == case["D_binding"], owner)
    elif owner == "O_entry":
        semantic_require(case["O"] == case["O_binding"], owner)
    elif owner == "C_entry":
        semantic_require(case["C"] == case["C_binding"], owner)
    elif owner == "action_order":
        semantic_require(case["action_names"] ==
                         case["action_order_binding"], owner)
    elif owner == "premature_C":
        semantic_require(case["C_phase"] == "after-closure", owner)
    elif owner == "target":
        mutated_membership = context["Hd1_owner"].contains(
            vnorm(case["target"]))
        semantic_require(mutated_membership ==
                         (case["terminal"] == "MEMBER"), owner)
    else:
        raise RuntimeError("raw semantic owner")


def independent_vectors(vectors, width):
    accepted = []
    for vector in vectors:
        represented = any(
            lincomb(accepted, coefficients, width) == vnorm(vector)
            for coefficients in itertools.product(range(3),
                                                   repeat=len(accepted)))
        if represented:
            return False
        accepted.append(vnorm(vector))
    return True


def certificate_owner_oracle(receipt, owner, context):
    case = context["case"]
    rows = receipt["rows"]
    if owner == "seed_index":
        valid = all(type(row.get("seed_index")) is int and
                    0 <= row["seed_index"] < len(case["theta_seeds"]) and
                    (row["kind"] != "seed" or
                     row["theta"] == case["theta_seeds"][row["seed_index"]])
                    for row in rows)
        semantic_require(valid, owner)
    elif owner == "parent":
        valid = all((row["parent"] is None if row["kind"] == "seed" else
                     type(row["parent"]) is int and
                     0 <= row["parent"] < index)
                    for index, row in enumerate(rows))
        semantic_require(valid, owner)
    elif owner == "row_theta":
        action_by_name = {action["name"]: action
                          for action in case["actions"]}
        valid = True
        for index, row in enumerate(rows):
            valid = valid and row["z"] == vec(case["D"], row["theta"])
            valid = valid and row["eta"] == vec(case["O"], row["theta"])
            valid = valid and row["flat"] == row["z"] + row["eta"]
            if row["kind"] == "seed":
                valid = valid and row["theta"] == case["theta_seeds"][
                    row["seed_index"]]
            elif type(row["parent"]) is int and 0 <= row["parent"] < index:
                valid = valid and row["action"] in action_by_name
                if row["action"] in action_by_name:
                    valid = valid and row["theta"] == vec(
                        action_by_name[row["action"]]["theta_matrix"],
                        rows[row["parent"]]["theta"])
            else:
                valid = False
        semantic_require(valid, owner)
    elif owner == "left_kernel":
        images = [vec(case["C"], row["eta"]) for row in rows]
        vectors = receipt["left_kernel_basis"]
        valid = (len(vectors) == len(context["kernel_basis"]) and
                 all(len(coefficients) == len(rows) and any(coefficients) and
                     all(sum(coefficients[j] * images[j][i]
                             for j in range(len(rows))) % 3 == 0
                         for i in range(len(images[0])))
                     for coefficients in vectors) and
                 independent_vectors(vectors, len(rows)))
        semantic_require(valid, owner)
    elif owner == "Hd1":
        expected = [lincomb([row["z"] for row in rows], coefficients,
                            len(case["D"]))
                    for coefficients in receipt["left_kernel_basis"]]
        semantic_require(receipt["Hd1"] == expected, owner)
    elif owner == "member_ancestry":
        if receipt["slice_membership"] is False:
            semantic_require(receipt.get("member_ancestry") is None and
                             receipt.get("member_theta") is None, owner)
            return
        ancestry = receipt.get("member_ancestry")
        valid = isinstance(ancestry, dict)
        if valid:
            payload = {key: ancestry.get(key) for key in (
                "Hd1_coefficients", "closure_coefficients", "theta", "z",
                "eta")}
            valid = ancestry.get("direct_reconstruction_sha256") == digest(payload)
            valid = valid and lincomb(
                receipt["Hd1"], ancestry["Hd1_coefficients"],
                len(case["D"])) == receipt["target"]
            valid = valid and lincomb(
                [row["theta"] for row in rows],
                ancestry["closure_coefficients"],
                len(case["theta_seeds"][0])) == ancestry["theta"]
            valid = valid and lincomb(
                [row["z"] for row in rows], ancestry["closure_coefficients"],
                len(case["D"])) == ancestry["z"] == receipt["target"]
            valid = valid and lincomb(
                [row["eta"] for row in rows],
                ancestry["closure_coefficients"], len(case["O"])) == ancestry["eta"]
            valid = valid and receipt["member_theta"] == ancestry["theta"]
            valid = valid and vec(case["D"], ancestry["theta"]) == receipt["target"]
            valid = valid and not any(vec(case["C"], ancestry["eta"]))
        semantic_require(valid, owner)
    elif owner == "dual":
        if receipt["slice_membership"] is True:
            semantic_require(receipt.get("dual") is None, owner)
            return
        dual = receipt.get("dual")
        valid = (isinstance(dual, list) and len(dual) == len(case["D"]) and
                 all(sum(dual[i] * h_value[i]
                         for i in range(len(dual))) % 3 == 0
                     for h_value in context["Hd1_owner"].raw_rows) and
                 sum(dual[i] * receipt["target"][i]
                     for i in range(len(dual))) % 3 == 1)
        semantic_require(valid, owner)
    elif owner == "terminal":
        computed = "MEMBER" if context["Hd1_owner"].contains(
            receipt["target"]) else "NONMEMBER"
        semantic_require(receipt.get("terminal") == computed, owner)
    else:
        raise RuntimeError("certificate semantic owner")


def audit_certificate(context):
    receipt = context["receipt"]
    case = context["case"]
    require(receipt["case_digest_sha256"] == certificate_seal(receipt),
            "case receipt seal")
    require(receipt["closure_rank"] == context["closure"].rank and
            receipt["kernel_dim"] == len(context["kernel_basis"]) and
            receipt["full_nonzero_kernel_cardinality"] ==
            3 ** len(context["kernel_basis"]) - 1 and
            receipt["Hd1_rank"] == context["Hd1_owner"].rank,
            "receipt scalar replay")
    require(receipt["target"] == vnorm(case["target"]) and
            receipt["slice_membership"] ==
            context["Hd1_owner"].contains(receipt["target"]),
            "receipt target replay")
    replay_owner_export(receipt["closure_owner"])
    replay_owner_export(receipt["Hd1_owner"])
    require(receipt["closure_owner"]["raw_rows"] ==
            [row["flat"] for row in receipt["rows"]],
            "closure owner raw rows")
    require(all(context["closure"].contains(row["flat"])
                for row in receipt["rows"]) and
            all(any(raw == row["flat"] for row in receipt["rows"])
                for raw in context["closure"].raw_rows),
            "closure retained two-way span")
    expected_hd1_rows = []
    for h_value in receipt["Hd1"]:
        if not any(h_value):
            continue
        if not any(lincomb(expected_hd1_rows, coefficients, len(case["D"])) ==
                   h_value for coefficients in itertools.product(
                       range(3), repeat=len(expected_hd1_rows))):
            expected_hd1_rows.append(h_value)
    require(receipt["Hd1_owner"]["raw_rows"] == expected_hd1_rows,
            "Hd1 owner raw rows")
    require(all(context["Hd1_owner"].contains(h_value)
                for h_value in receipt["Hd1"]) and
            all(any(raw == h_value for h_value in receipt["Hd1"])
                for raw in context["Hd1_owner"].raw_rows),
            "Hd1 retained two-way span")
    for owner in OWNERS[11:]:
        certificate_owner_oracle(receipt, owner, context)


def mutation_control(fixture, contexts, owner):
    entry = MUTATION_REGISTRY[owner]
    case_index = entry["case_index"]
    context = contexts[case_index]
    if entry["scope"] == "raw_case":
        before = fixture["cases"][case_index]
        mutated = mutate_raw(before, owner)
        owned_before = digest(owner_value(before, owner))
        owned_after = digest(owner_value(mutated, owner))
        require(owned_before != owned_after, "mutation owned object unchanged")
        canonical_before = digest(before)
        body_digest = digest(mutated)
        require(canonical_before != body_digest, "mutation canonical unchanged")
        mutated["mutation_fixture_seal"] = body_digest
        require(mutated["mutation_fixture_seal"] == digest({
            key: value for key, value in mutated.items()
            if key != "mutation_fixture_seal"}), "mutation fixture reseal")
        canonical_after = digest(mutated)
        seal_field = "mutation_fixture_seal"
        seal_value = mutated[seal_field]
        oracle = lambda: raw_owner_oracle(mutated, owner, context)
    else:
        before = context["receipt"]
        mutated = mutate_certificate(before, owner)
        owned_before = digest(owner_value(before, owner))
        owned_after = digest(owner_value(mutated, owner))
        require(owned_before != owned_after, "mutation owned object unchanged")
        canonical_before = digest(before)
        canonical_after = digest(mutated)
        require(canonical_before != canonical_after,
                "mutation canonical unchanged")
        require(mutated["case_digest_sha256"] == certificate_seal(mutated),
                "mutation certificate reseal")
        seal_field = "case_digest_sha256"
        seal_value = mutated[seal_field]
        oracle = lambda: certificate_owner_oracle(
            mutated, owner, context)
    try:
        oracle()
    except SemanticReject as rejection:
        require(rejection.stage == entry["stage"] and
                rejection.code == entry["code"] and
                rejection.reason == entry["reason"],
                "mutation wrong semantic rejection")
    else:
        raise RuntimeError("mutation semantic oracle accepted")
    return {
        "owner": owner, "scope": entry["scope"],
        "case_index": case_index,
        "owned_before_sha256": owned_before,
        "owned_after_sha256": owned_after,
        "canonical_before_sha256": canonical_before,
        "canonical_after_sha256": canonical_after,
        "seal_field": seal_field, "resealed_sha256": seal_value,
        "semantic_oracle_reached": True,
        "rejection_stage": entry["stage"],
        "rejection_code": entry["code"],
        "rejection_reason": entry["reason"],
    }


def selftest(path):
    fixture = parse_fixture(path)
    contexts = [compile_case(case) for case in fixture["cases"]]
    receipts = [context["receipt"] for context in contexts]
    wrong_seal = dict(fixture)
    wrong_seal["fixture_seal"] = "wrong-nonempty-seal"
    wrong_seal_rejected = False
    try:
        validate_fixture(wrong_seal)
    except RuntimeError:
        wrong_seal_rejected = True
    require(wrong_seal_rejected is True,
            "wrong nonempty fixture seal canary")
    for receipt in receipts:
        expected = fixture["expected_cases"][receipt["case"]]
        require(receipt["closure_rank"] == expected["closure_rank"] and
                receipt["kernel_dim"] == expected["kernel_dim"] and
                receipt["full_nonzero_kernel_cardinality"] ==
                expected["full_nonzero_kernel_cardinality"] and
                receipt["Hd1_rank"] == expected["Hd1_rank"],
                "fixture expected rank")
        require(receipt["member_theta"] == expected["member_theta"] and
                receipt["dual"] == expected["dual"],
                "fixture expected equation")
    controls = [mutation_control(fixture, contexts, owner)
                for owner in OWNERS]
    require([item["owner"] for item in controls] == list(OWNERS) and
            all(item["semantic_oracle_reached"] is True
                for item in controls), "mutation controls")
    body = {
        "schema": SELF, "status": "COMPLETE", "terminal": PASS,
        "cases": receipts, "mutation_controls": controls,
        "mutation_attempted": len(controls),
        "mutation_rejected": len(controls),
        "wrong_seal_rejected": wrong_seal_rejected,
        "production_input": False,
    }
    return dict(body, self_digest_sha256=digest(body))


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"),
                        required=True)
    parser.add_argument("--fixture", type=Path, default=ROOT / FIXTURE)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    if arguments.mode == "SELFTEST":
        value = selftest(arguments.fixture)
    else:
        body = {"schema": SCHEMA, "status": STATIC, "terminal": STATIC,
                "reason": "actual typed matrices are not staged"}
        value = dict(body, self_digest_sha256=digest(body))
    arguments.output.write_bytes(canon(value) + b"\n")
    if arguments.mode == "SELFTEST":
        print(PASS)
        print("R07_JOINT_SLICE_KERNEL_GENERAL_V11_PRODUCER_TERMINAL "
              "SELFTEST_COMPLETE")
    else:
        print("R07_JOINT_SLICE_KERNEL_GENERAL_V11_PRODUCER_TERMINAL " +
              value["terminal"])


if __name__ == "__main__":
    main()
