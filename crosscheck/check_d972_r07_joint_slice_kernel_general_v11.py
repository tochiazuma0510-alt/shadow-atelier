#!/usr/bin/env python3
"""Independent dense-tableau checker for the typed joint slice receipt."""
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
FIXTURE = "search/certs/d972_r07_joint_slice_kernel_general_selftest_v11_20260828.json"
FIXTURE_SEAL = "literal-static-fixture-v11"
PASS = "R07_JOINT_SLICE_KERNEL_GENERAL_V11_CHECKER_SELFTEST_PASS"
PRODUCER_PASS = "R07_JOINT_SLICE_KERNEL_GENERAL_V11_PRODUCER_SELFTEST_PASS"
STATIC = "STATIC_BLOCKED:actual typed matrices are not staged"
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


def require(condition, message):
    if condition is not True:
        raise RuntimeError(message)


class IndependentReject(Exception):
    """Narrow checker-owned semantic rejection for registered mutations."""

    def __init__(self, stage, code, reason):
        super().__init__(reason)
        self.stage = stage
        self.code = code
        self.reason = reason


def semantic_require(condition, owner):
    if condition is not True:
        entry = MUTATION_REGISTRY[owner]
        raise IndependentReject(entry["stage"], entry["code"],
                                entry["reason"])


def normalize(vector):
    return [int(x) % 3 for x in vector]


def apply_matrix(matrix, vector):
    return [sum(matrix[row][column] * vector[column]
                for column in range(len(vector))) % 3
            for row in range(len(matrix))]


def multiply(left, right):
    return [[sum(left[row][middle] * right[middle][column]
                 for middle in range(len(right))) % 3
             for column in range(len(right[0]))]
            for row in range(len(left))]


def combine(rows, coefficients, width):
    require(len(rows) == len(coefficients), "combination arity")
    return [sum(coefficients[row] * rows[row][column]
                for row in range(len(rows))) % 3
            for column in range(width)]


def matrix_rank(matrix):
    work = [normalize(row) for row in matrix]
    occupied = 0
    for column in range(len(work[0]) if work else 0):
        candidates = [row for row in range(occupied, len(work))
                      if work[row][column] != 0]
        if not candidates:
            continue
        chosen = candidates[-1]
        work[occupied], work[chosen] = work[chosen], work[occupied]
        multiplier = pow(work[occupied][column], -1, 3)
        work[occupied] = [(multiplier * scalar) % 3
                          for scalar in work[occupied]]
        for row in range(occupied + 1, len(work)):
            factor = work[row][column]
            if factor:
                work[row] = [(x - factor * y) % 3
                             for x, y in zip(work[row], work[occupied])]
        occupied += 1
        if occupied == len(work):
            break
    return occupied


def enumerated_solution(rows, target, width):
    wanted = normalize(target)
    for coefficients in itertools.product(range(3), repeat=len(rows)):
        if combine(rows, coefficients, width) == wanted:
            return list(coefficients)
    return None


def enumerated_independent_subset(candidates, width):
    accepted = []
    source_indices = []
    for index, candidate in enumerate(candidates):
        if enumerated_solution(accepted, candidate, width) is None:
            accepted.append(normalize(candidate))
            source_indices.append(index)
    return accepted, source_indices


class DenseTableau:
    """One full augmented Gauss-Jordan build from a complete raw-row list."""

    def __init__(self, rows, width, name):
        self.name = name
        self.width = width
        self.raw_rows = [normalize(row) for row in rows]
        require(all(len(row) == width for row in self.raw_rows),
                name + " tableau width")
        count = len(self.raw_rows)
        augmented = [row + [1 if i == j else 0 for j in range(count)]
                     for i, row in enumerate(self.raw_rows)]
        pivots = []
        occupied = 0
        for column in range(width):
            choices = [row for row in range(occupied, count)
                       if augmented[row][column] != 0]
            if not choices:
                continue
            chosen = choices[-1]
            augmented[occupied], augmented[chosen] = (
                augmented[chosen], augmented[occupied])
            inverse = pow(augmented[occupied][column], -1, 3)
            augmented[occupied] = [inverse * scalar % 3
                                   for scalar in augmented[occupied]]
            for row in range(count):
                if row == occupied:
                    continue
                factor = augmented[row][column]
                if factor:
                    augmented[row] = [(x - factor * y) % 3
                                      for x, y in
                                      zip(augmented[row],
                                          augmented[occupied])]
            pivots.append(column)
            occupied += 1
            if occupied == count:
                break
        require(occupied == count, name + " raw rows dependent")
        self.pivots = pivots
        self.reduced_rows = [row[:width] for row in augmented]
        self.transforms = [row[width:] for row in augmented]
        for pivot, row, transform in zip(
                self.pivots, self.reduced_rows, self.transforms):
            require(row[pivot] == 1 and
                    all(row[other] == 0 for other in self.pivots
                        if other != pivot), name + " tableau RREF")
            require(combine(self.raw_rows, transform, width) == row,
                    name + " augmented transform")
        self.transcript_sha256 = digest({
            "name": name, "width": width, "raw_rows": self.raw_rows,
            "pivots": self.pivots, "reduced_rows": self.reduced_rows,
            "transforms": self.transforms,
        })

    @property
    def rank(self):
        return len(self.pivots)

    def solve(self, target):
        remainder = normalize(target)
        require(len(remainder) == self.width, self.name + " target width")
        row_weights = [0] * self.rank
        for index, pivot in enumerate(self.pivots):
            factor = remainder[pivot]
            row_weights[index] = factor
            if factor:
                remainder = [(x - factor * y) % 3
                             for x, y in
                             zip(remainder, self.reduced_rows[index])]
        if any(remainder):
            return None
        raw_coefficients = [
            sum(row_weights[i] * self.transforms[i][j]
                for i in range(self.rank)) % 3
            for j in range(len(self.raw_rows))
        ]
        require(combine(self.raw_rows, raw_coefficients, self.width) ==
                normalize(target), self.name + " direct solve replay")
        return raw_coefficients

    def contains(self, target):
        return self.solve(target) is not None


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
            len(value.get("cases", [])) == 5, "five cases")
    require(value.get("typed_basis") == {
        "Theta": ["theta0", "theta1"], "Z": ["z0", "z1"],
        "E_hat": ["occurrence%02d" % i for i in range(11)],
        "E": ["printed0"],
    }, "typed basis")
    require(set(value.get("expected_cases", {})) ==
            {case["name"] for case in value["cases"]},
            "fixture expectations")
    require(value.get("mutation_roster") == list(OWNERS),
            "fixture mutation roster")
    require(value.get("mutation_registry") == MUTATION_REGISTRY,
            "fixture mutation registry")
    return value


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def reconstruct_raw(case):
    require(case.get("modulus") == 3, "typed field")
    require(case.get("occurrence_count") == 11 and
            case.get("occurrence_tags") ==
            ["occurrence%02d" % i for i in range(11)],
            "occurrence labels")
    require(case["theta_seeds"] == case["seed_bindings"],
            "theta seed owner")
    require(case["A_theta"] == case["A_theta_binding"] and
            case["A_Z"] == case["A_Z_binding"] and
            case["A_E"] == case["A_E_binding"], "action owner")
    require(case["D"] == case["D_binding"] and
            case["O"] == case["O_binding"] and
            case["C"] == case["C_binding"], "map owner")
    require(case["action_names"] == case["action_order_binding"] and
            case["C_phase"] == "after-closure" and
            case["left_kernel_method"] == "rref", "control owner")
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
    require(multiply(case["D"], case["A_theta"]) ==
            multiply(case["A_Z"], case["D"]), "D equivariance")
    require(multiply(case["O"], case["A_theta"]) ==
            multiply(case["A_E"], case["O"]), "O equivariance")
    require(len(case["actions"]) == len(case["action_names"]),
            "action count")
    for name, action in zip(case["action_names"], case["actions"]):
        require(action["name"] == name, "action binding")
        check_square(action["theta_matrix"], theta_dimension,
                     "stored theta action")
        check_square(action["z_matrix"], z_dimension, "stored z action")
        check_square(action["eta_matrix"], eta_dimension,
                     "stored eta action")
        require(multiply(case["D"], action["theta_matrix"]) ==
                multiply(action["z_matrix"], case["D"]) and
                multiply(case["O"], action["theta_matrix"]) ==
                multiply(action["eta_matrix"], case["O"]),
                "action equivariance")

    queue = [(normalize(seed), None, index, "seed", "seed")
             for index, seed in enumerate(case["theta_seeds"])]
    queued_flats = {
        tuple(apply_matrix(case["D"], item[0]) +
              apply_matrix(case["O"], item[0]))
        for item in queue
    }
    rows = []
    pops = 0
    maximum_pops = len(queue) + theta_dimension * len(case["actions"])
    while queue:
        pops += 1
        require(pops <= maximum_pops, "closure bound")
        theta, parent, seed_index, action_name, kind = queue.pop(0)
        z_value = apply_matrix(case["D"], theta)
        eta_value = apply_matrix(case["O"], theta)
        flat = z_value + eta_value
        if enumerated_solution([row["flat"] for row in rows], flat,
                               z_dimension + eta_dimension) is not None:
            continue
        rows.append({"theta": theta, "z": z_value, "eta": eta_value,
                     "flat": flat, "parent": parent,
                     "seed_index": seed_index, "action": action_name,
                     "kind": kind})
        for name, action in reversed(list(zip(case["action_names"],
                                               case["actions"]))):
            candidate = apply_matrix(action["theta_matrix"], theta)
            candidate_flat = (apply_matrix(case["D"], candidate) +
                              apply_matrix(case["O"], candidate))
            key = tuple(candidate_flat)
            if key not in queued_flats:
                queued_flats.add(key)
                queue.append((candidate, len(rows) - 1, seed_index,
                              name, "action"))
    closure_tableau = DenseTableau(
        [row["flat"] for row in rows], z_dimension + eta_dimension,
        "checker closure")
    images = [apply_matrix(case["C"], row["eta"]) for row in rows]
    all_kernel = [
        list(coefficients)
        for coefficients in itertools.product(range(3), repeat=len(rows))
        if all(sum(coefficients[row] * images[row][column]
                   for row in range(len(rows))) % 3 == 0
               for column in range(quotient_dimension))
    ]
    nonzero_kernel = [coefficients for coefficients in all_kernel
                      if any(coefficients)]
    kernel_basis, _ = enumerated_independent_subset(
        nonzero_kernel, len(rows))
    kernel_tableau = DenseTableau(kernel_basis, len(rows),
                                  "checker left kernel")
    hd1 = [combine([row["z"] for row in rows], coefficients, z_dimension)
           for coefficients in kernel_basis]
    theta_hd1 = [combine([row["theta"] for row in rows], coefficients,
                         theta_dimension) for coefficients in kernel_basis]
    eta_hd1 = [combine([row["eta"] for row in rows], coefficients,
                       eta_dimension) for coefficients in kernel_basis]
    for theta_value, h_value, eta_value in zip(theta_hd1, hd1, eta_hd1):
        require(h_value == apply_matrix(case["D"], theta_value) and
                not any(apply_matrix(case["C"], eta_value)),
                "independent kernel reconstruction")
    hd1_basis, hd1_sources = enumerated_independent_subset(hd1, z_dimension)
    hd1_tableau = DenseTableau(hd1_basis, z_dimension, "checker Hd1")
    target = normalize(case["target"])
    hd1_solution = hd1_tableau.solve(target)
    is_member = hd1_solution is not None
    require(case["terminal"] in ("MEMBER", "NONMEMBER"), "terminal enum")
    require(is_member == (case["terminal"] == "MEMBER"), "membership")
    checker_member_theta = None
    if is_member:
        kernel_coefficients = [0] * len(kernel_basis)
        for basis_index, coefficient in enumerate(hd1_solution):
            kernel_coefficients[hd1_sources[basis_index]] = coefficient
        closure_coefficients = [
            sum(kernel_coefficients[i] * kernel_basis[i][j]
                for i in range(len(kernel_basis))) % 3
            for j in range(len(rows))
        ]
        checker_member_theta = combine(
            [row["theta"] for row in rows], closure_coefficients,
            theta_dimension)
        require(apply_matrix(case["D"], checker_member_theta) == target,
                "independent member ancestry")
    checker_dual = None
    if not is_member:
        checker_dual = next((list(candidate) for candidate in
                             itertools.product(range(3), repeat=z_dimension)
                             if any(candidate) and
                             all(sum(candidate[i] * h_value[i]
                                     for i in range(z_dimension)) % 3 == 0
                                 for h_value in hd1_basis) and
                             sum(candidate[i] * target[i]
                                 for i in range(z_dimension)) % 3 == 1), None)
        require(checker_dual is not None, "independent dual")
    return {
        "case": case, "rows": rows, "pops": pops,
        "maximum_pops": maximum_pops,
        "closure_tableau": closure_tableau, "images": images,
        "all_kernel": all_kernel, "nonzero_kernel": nonzero_kernel,
        "kernel_basis": kernel_basis, "kernel_tableau": kernel_tableau,
        "Hd1": hd1, "theta_Hd1": theta_hd1, "eta_Hd1": eta_hd1,
        "Hd1_basis": hd1_basis, "Hd1_sources": hd1_sources,
        "Hd1_tableau": hd1_tableau, "target": target,
        "is_member": is_member, "member_theta": checker_member_theta,
        "dual": checker_dual,
    }


def verify_owner_export(owner, expected_name, expected_rows):
    body = dict(owner)
    claimed = body.pop("owner_digest_sha256", None)
    require(type(claimed) is str and claimed == digest(body),
            expected_name + " owner seal")
    require(owner.get("owner") == expected_name and
            owner.get("raw_rows") == expected_rows and
            owner.get("rank") == len(expected_rows) ==
            len(owner.get("insertion_order", [])),
            expected_name + " owner roster")
    width = owner["width"]
    require(len(owner["pivots"]) == len(owner["reduced_rows"]) ==
            len(owner["transforms"]) ==
            len(owner["reconstruction_digests_sha256"]) == owner["rank"] and
            owner["pivots"] == sorted(set(owner["pivots"])) and
            all(0 <= pivot < width for pivot in owner["pivots"]),
            expected_name + " owner transform arity")
    for pivot, row, transform, claimed_digest in zip(
            owner["pivots"], owner["reduced_rows"], owner["transforms"],
            owner["reconstruction_digests_sha256"]):
        require(row[pivot] == 1 and
                all(row[other] == 0 for other in owner["pivots"]
                    if other != pivot), expected_name + " reduced row")
        require(combine(expected_rows, transform, width) == row,
                expected_name + " direct transform")
        require(claimed_digest == digest({
            "pivot": pivot, "transform": transform,
            "reconstructed_row": row,
        }), expected_name + " reconstruction digest")
    accepted_count = 0
    for candidate_index, record in enumerate(owner["reductions"]):
        require(record["candidate_index"] == candidate_index and
                record["prior_roster_size"] == accepted_count,
                expected_name + " reduction order")
        prior = record["prior_roster_size"]
        partial = combine(expected_rows[:prior],
                          record["reduction_coefficients"], width)
        replay = [(x + y) % 3
                  for x, y in zip(partial, record["remainder"])]
        require(replay == record["raw_row"],
                expected_name + " reduction replay")
        require(combine(expected_rows, record["direct_coefficients"], width) ==
                record["raw_row"], expected_name + " direct replay")
        payload = {key: record[key] for key in (
            "candidate_index", "label", "raw_row", "accepted",
            "accepted_raw_index", "direct_coefficients")}
        require(record["direct_reconstruction_sha256"] == digest(payload),
                expected_name + " direct digest")
        if record["accepted"] is True:
            require(record["accepted_raw_index"] == accepted_count and
                    record["raw_row"] == expected_rows[accepted_count] and
                    record["label"] == owner["insertion_order"][accepted_count]
                    and any(record["remainder"]),
                    expected_name + " accepted reduction")
            accepted_count += 1
        else:
            require(record["accepted_raw_index"] is None and
                    not any(record["remainder"]),
                    expected_name + " dependent reduction")
    require(accepted_count == owner["rank"],
            expected_name + " accepted count")


def certificate_seal(receipt):
    body = dict(receipt)
    body.pop("case_digest_sha256", None)
    return digest(body)


def valid_seed_indices(receipt, case):
    return all(type(row.get("seed_index")) is int and
               0 <= row["seed_index"] < len(case["theta_seeds"]) and
               (row["kind"] != "seed" or
                row["theta"] == case["theta_seeds"][row["seed_index"]])
               for row in receipt["rows"])


def valid_parents(receipt):
    return all((row["parent"] is None if row["kind"] == "seed" else
                type(row["parent"]) is int and
                0 <= row["parent"] < index)
               for index, row in enumerate(receipt["rows"]))


def valid_row_theta(receipt, case):
    actions = {action["name"]: action for action in case["actions"]}
    valid = True
    for index, row in enumerate(receipt["rows"]):
        valid = valid and row["z"] == apply_matrix(case["D"], row["theta"])
        valid = valid and row["eta"] == apply_matrix(case["O"], row["theta"])
        valid = valid and row["flat"] == row["z"] + row["eta"]
        if row["kind"] == "seed":
            valid = valid and row["theta"] == case["theta_seeds"][
                row["seed_index"]]
        elif type(row["parent"]) is int and 0 <= row["parent"] < index:
            valid = valid and row["action"] in actions
            if row["action"] in actions:
                valid = valid and row["theta"] == apply_matrix(
                    actions[row["action"]]["theta_matrix"],
                    receipt["rows"][row["parent"]]["theta"])
        else:
            valid = False
    return valid


def receipt_kernel_enumeration(receipt, case):
    row_count = len(receipt["rows"])
    images = [apply_matrix(case["C"], row["eta"])
              for row in receipt["rows"]]
    all_vectors = [
        list(coefficients)
        for coefficients in itertools.product(range(3), repeat=row_count)
        if all(sum(coefficients[row] * images[row][column]
                   for row in range(row_count)) % 3 == 0
               for column in range(len(case["C"])))
    ]
    nonzero = [coefficients for coefficients in all_vectors
               if any(coefficients)]
    basis, _ = enumerated_independent_subset(nonzero, row_count)
    return {"all": all_vectors, "nonzero": nonzero, "basis": basis,
            "images": images}


def valid_left_kernel(receipt, context, enumeration=None):
    vectors = receipt["left_kernel_basis"]
    row_count = len(receipt["rows"])
    data = (enumeration if enumeration is not None else
            receipt_kernel_enumeration(receipt, context["case"]))
    images = data["images"]
    if not (len(vectors) == len(data["basis"]) and
            all(len(coefficients) == row_count and any(coefficients) and
                all(sum(coefficients[row] * images[row][column]
                        for row in range(row_count)) % 3 == 0
                    for column in range(len(context["case"]["C"])))
                for coefficients in vectors)):
        return False
    independent, _ = enumerated_independent_subset(vectors, row_count)
    if len(independent) != len(vectors):
        return False
    return (all(enumerated_solution(data["basis"], vector,
                                    row_count) is not None
                for vector in vectors) and
            all(enumerated_solution(vectors, vector, row_count) is not None
                for vector in data["basis"]))


def expected_receipt_hd1(receipt, case):
    return [combine([row["z"] for row in receipt["rows"]], coefficients,
                    len(case["D"]))
            for coefficients in receipt["left_kernel_basis"]]


def valid_hd1(receipt, context):
    expected = expected_receipt_hd1(receipt, context["case"])
    if receipt["Hd1"] != expected:
        return False
    width = len(context["case"]["D"])
    return (all(context["Hd1_tableau"].contains(row)
                for row in receipt["Hd1"]) and
            all(enumerated_solution(receipt["Hd1"], row, width) is not None
                for row in context["Hd1_basis"]))


def valid_member_ancestry(receipt, case):
    ancestry = receipt.get("member_ancestry")
    if not isinstance(ancestry, dict):
        return False
    payload = {key: ancestry.get(key) for key in (
        "Hd1_coefficients", "closure_coefficients", "theta", "z", "eta")}
    if ancestry.get("direct_reconstruction_sha256") != digest(payload):
        return False
    return (
        combine(receipt["Hd1"], ancestry["Hd1_coefficients"],
                len(case["D"])) == receipt["target"] and
        combine([row["theta"] for row in receipt["rows"]],
                ancestry["closure_coefficients"],
                len(case["theta_seeds"][0])) == ancestry["theta"] and
        combine([row["z"] for row in receipt["rows"]],
                ancestry["closure_coefficients"],
                len(case["D"])) == ancestry["z"] == receipt["target"] and
        combine([row["eta"] for row in receipt["rows"]],
                ancestry["closure_coefficients"],
                len(case["O"])) == ancestry["eta"] and
        receipt["member_theta"] == ancestry["theta"] and
        apply_matrix(case["D"], ancestry["theta"]) == receipt["target"] and
        not any(apply_matrix(case["C"], ancestry["eta"]))
    )


def valid_dual(receipt, context):
    dual = receipt.get("dual")
    width = len(context["case"]["D"])
    return (isinstance(dual, list) and len(dual) == width and
            all(sum(dual[i] * h_value[i] for i in range(width)) % 3 == 0
                for h_value in context["Hd1_basis"]) and
            sum(dual[i] * receipt["target"][i]
                for i in range(width)) % 3 == 1)


def audit_receipt(case, receipt, context):
    require(receipt.get("case") == case["name"], "case identity")
    require(receipt.get("case_digest_sha256") == certificate_seal(receipt),
            "case receipt seal")
    receipt_rows = receipt.get("rows")
    require(isinstance(receipt_rows, list), "receipt rows")
    require(valid_seed_indices(receipt, case), "receipt seed index")
    require(valid_parents(receipt), "receipt parent")
    require(valid_row_theta(receipt, case), "receipt row theta")
    receipt_flats = [row["flat"] for row in receipt_rows]
    verify_owner_export(receipt["closure_owner"], "closure", receipt_flats)
    require(receipt["closure_owner"]["insertion_order"] ==
            [record["label"] for record in
             receipt["closure_owner"]["reductions"]
             if record["accepted"] is True],
            "closure insertion transcript")
    receipt_closure = DenseTableau(
        receipt_flats, len(case["D"]) + len(case["O"]),
        "receipt closure")
    require(all(context["closure_tableau"].contains(row)
                for row in receipt_flats) and
            all(receipt_closure.contains(row["flat"])
                for row in context["rows"]), "closure two-way span")
    require(receipt["closure_rank"] == receipt_closure.rank ==
            context["closure_tableau"].rank,
            "receipt closure rank")

    receipt_kernel_data = receipt_kernel_enumeration(receipt, case)
    require(valid_left_kernel(receipt, context, receipt_kernel_data),
            "left-kernel content")
    receipt_kernel = DenseTableau(
        receipt["left_kernel_basis"], len(receipt_rows),
        "receipt left kernel")
    require(receipt["kernel_dim"] == receipt_kernel.rank ==
            context["kernel_tableau"].rank,
            "receipt kernel dimension")
    require(receipt["full_nonzero_kernel_cardinality"] ==
            len(receipt_kernel_data["nonzero"]) ==
            len(context["nonzero_kernel"]),
            "receipt full kernel cardinality")
    require(all(receipt_kernel.contains(vector)
                for vector in receipt_kernel_data["nonzero"]),
            "receipt full kernel span")
    require(len(receipt["kernel_reconstruction"]) ==
            len(receipt["left_kernel_basis"]),
            "kernel reconstruction count")
    for index, (record, coefficients) in enumerate(zip(
            receipt["kernel_reconstruction"],
            receipt["left_kernel_basis"])):
        payload = {"kernel_basis_index": index,
                   "closure_coefficients": coefficients,
                   "theta": combine([row["theta"] for row in receipt_rows],
                                    coefficients,
                                    len(case["theta_seeds"][0])),
                   "z": combine([row["z"] for row in receipt_rows],
                                coefficients, len(case["D"])),
                   "eta": combine([row["eta"] for row in receipt_rows],
                                  coefficients, len(case["O"]))}
        require(all(record.get(key) == value for key, value in payload.items())
                and record.get("direct_reconstruction_sha256") ==
                digest(payload), "kernel reconstruction transcript")

    require(valid_hd1(receipt, context), "Hd1 content")
    receipt_hd1_basis, receipt_hd1_sources = (
        enumerated_independent_subset(receipt["Hd1"], len(case["D"])))
    require(receipt["Hd1_owner"]["insertion_order"] ==
            [{"kernel_basis_index": index}
             for index in receipt_hd1_sources],
            "Hd1 insertion order")
    verify_owner_export(receipt["Hd1_owner"], "Hd1", receipt_hd1_basis)
    receipt_hd1 = DenseTableau(receipt_hd1_basis, len(case["D"]),
                               "receipt Hd1")
    require(all(context["Hd1_tableau"].contains(row)
                for row in receipt_hd1_basis) and
            all(receipt_hd1.contains(row)
                for row in context["Hd1_basis"]), "Hd1 two-way span")
    require(receipt["Hd1_rank"] == receipt_hd1.rank ==
            context["Hd1_tableau"].rank, "receipt Hd1 rank")

    require(receipt["target"] == context["target"] ==
            normalize(case["target"]), "receipt target")
    require(receipt["slice_membership"] is context["is_member"],
            "receipt slice membership")
    computed_terminal = "MEMBER" if context["is_member"] else "NONMEMBER"
    require(receipt["terminal"] == case["terminal"] == computed_terminal,
            "receipt terminal")
    if context["is_member"]:
        require(valid_member_ancestry(receipt, case), "member ancestry")
        require(receipt["member_theta"] == context["member_theta"],
                "independent member theta")
        require(receipt["dual"] is None, "member dual absence")
    else:
        require(receipt["member_theta"] is None and
                receipt["member_ancestry"] is None,
                "nonmember ancestry absence")
        require(valid_dual(receipt, context), "dual replay")
    change_payload = {
        "closure_owner": receipt["closure_owner"],
        "Hd1_owner": receipt["Hd1_owner"],
        "kernel_reconstruction": receipt["kernel_reconstruction"],
        "member_ancestry": receipt["member_ancestry"],
    }
    require(receipt["change_of_basis_sha256"] == digest(change_payload),
            "change-of-basis transcript seal")
    return {
        "receipt_closure": receipt_closure,
        "receipt_kernel": receipt_kernel,
        "receipt_Hd1": receipt_hd1,
    }


def owner_value(scope_object, owner):
    mapping = {
        "field_modulus": "modulus", "theta_seed": "theta_seeds",
        "theta_action": "A_theta", "z_action": "A_Z",
        "eta_action": "A_E", "D_entry": "D", "O_entry": "O",
        "C_entry": "C", "action_order": "action_names",
        "premature_C": "C_phase", "target": "target",
        "left_kernel": "left_kernel_basis", "Hd1": "Hd1",
        "member_ancestry": "member_ancestry", "dual": "dual",
        "terminal": "terminal",
    }
    if owner == "seed_index":
        return [row["seed_index"] for row in scope_object["rows"]]
    if owner == "parent":
        return [row["parent"] for row in scope_object["rows"]]
    if owner == "row_theta":
        return [row["theta"] for row in scope_object["rows"]]
    if owner in mapping:
        return scope_object[mapping[owner]]
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
        semantic_require(context["Hd1_tableau"].contains(
            normalize(case["target"])) ==
            (case["terminal"] == "MEMBER"), owner)
    else:
        raise RuntimeError("raw semantic owner")


def certificate_owner_oracle(receipt, owner, context):
    if owner == "seed_index":
        semantic_require(valid_seed_indices(receipt, context["case"]), owner)
    elif owner == "parent":
        semantic_require(valid_parents(receipt), owner)
    elif owner == "row_theta":
        semantic_require(valid_row_theta(receipt, context["case"]), owner)
    elif owner == "left_kernel":
        semantic_require(valid_left_kernel(receipt, context), owner)
    elif owner == "Hd1":
        semantic_require(valid_hd1(receipt, context), owner)
    elif owner == "member_ancestry":
        semantic_require(valid_member_ancestry(receipt, context["case"]),
                         owner)
    elif owner == "dual":
        semantic_require(valid_dual(receipt, context), owner)
    elif owner == "terminal":
        computed = "MEMBER" if context["Hd1_tableau"].contains(
            receipt["target"]) else "NONMEMBER"
        semantic_require(receipt.get("terminal") == computed, owner)
    else:
        raise RuntimeError("certificate semantic owner")


def verify_mutation_control(fixture, producer_cases, contexts,
                            producer_record, owner):
    entry = MUTATION_REGISTRY[owner]
    case_index = entry["case_index"]
    context = contexts[case_index]
    if entry["scope"] == "raw_case":
        before = fixture["cases"][case_index]
        mutated = mutate_raw(before, owner)
        owned_before = digest(owner_value(before, owner))
        owned_after = digest(owner_value(mutated, owner))
        require(owned_before != owned_after,
                "independent owned mutation unchanged")
        canonical_before = digest(before)
        resealed = digest(mutated)
        require(canonical_before != resealed,
                "independent canonical mutation unchanged")
        mutated["mutation_fixture_seal"] = resealed
        require(mutated["mutation_fixture_seal"] == digest({
            key: value for key, value in mutated.items()
            if key != "mutation_fixture_seal"}),
            "independent fixture reseal")
        canonical_after = digest(mutated)
        seal_field = "mutation_fixture_seal"
        seal_value = mutated[seal_field]
        oracle = lambda: raw_owner_oracle(mutated, owner, context)
    else:
        before = producer_cases[case_index]
        mutated = mutate_certificate(before, owner)
        owned_before = digest(owner_value(before, owner))
        owned_after = digest(owner_value(mutated, owner))
        require(owned_before != owned_after,
                "independent owned mutation unchanged")
        canonical_before = digest(before)
        canonical_after = digest(mutated)
        require(canonical_before != canonical_after,
                "independent canonical mutation unchanged")
        require(mutated["case_digest_sha256"] == certificate_seal(mutated),
                "independent certificate reseal")
        seal_field = "case_digest_sha256"
        seal_value = mutated[seal_field]
        oracle = lambda: certificate_owner_oracle(
            mutated, owner, context)
    try:
        oracle()
    except IndependentReject as rejection:
        require(rejection.stage == entry["stage"] and
                rejection.code == entry["code"] and
                rejection.reason == entry["reason"],
                "independent wrong semantic rejection")
    else:
        raise RuntimeError("independent semantic oracle accepted")
    observed = {
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
    require(producer_record == observed,
            "producer mutation transcript mismatch " + owner)
    return observed


def run(fixture_path, receipt_path):
    fixture = fixture_preflight(validate_fixture(load(fixture_path)))
    wrong_fixture = dict(fixture)
    wrong_fixture["fixture_seal"] = "wrong-nonempty-seal"
    wrong_fixture_rejected = False
    try:
        validate_fixture(wrong_fixture)
    except RuntimeError:
        wrong_fixture_rejected = True
    require(wrong_fixture_rejected is True,
            "wrong fixture seal canary")
    producer = load(receipt_path)
    require(producer.get("schema") == SELF and
            producer.get("status") == "COMPLETE" and
            producer.get("terminal") == PRODUCER_PASS, "producer receipt")
    claimed = producer.get("self_digest_sha256")
    body = dict(producer)
    body.pop("self_digest_sha256", None)
    require(type(claimed) is str and claimed == digest(body),
            "producer receipt seal")
    require(producer.get("wrong_seal_rejected") is True,
            "producer wrong-seal record")
    wrong_producer = dict(producer)
    wrong_producer["self_digest_sha256"] = "wrong-nonempty-seal"
    wrong_producer_rejected = False
    wrong_body = dict(wrong_producer)
    wrong_claimed = wrong_body.pop("self_digest_sha256", None)
    try:
        require(type(wrong_claimed) is str and
                wrong_claimed == digest(wrong_body),
                "wrong producer receipt seal")
    except RuntimeError:
        wrong_producer_rejected = True
    require(wrong_producer_rejected is True,
            "wrong producer seal canary")
    producer_cases = producer.get("cases", [])
    require(len(producer_cases) == 5, "producer case count")
    contexts = [reconstruct_raw(case) for case in fixture["cases"]]
    receipt_contexts = [
        audit_receipt(case, receipt, context)
        for case, receipt, context in
        zip(fixture["cases"], producer_cases, contexts)
    ]
    require(len(receipt_contexts) == 5, "receipt audit count")
    results = []
    for case, receipt, context, receipt_context in zip(
            fixture["cases"], producer_cases, contexts, receipt_contexts):
        expected = fixture["expected_cases"][case["name"]]
        require(receipt["closure_rank"] == expected["closure_rank"] and
                receipt["kernel_dim"] == expected["kernel_dim"] and
                receipt["full_nonzero_kernel_cardinality"] ==
                expected["full_nonzero_kernel_cardinality"] and
                receipt["Hd1_rank"] == expected["Hd1_rank"],
                "fixture expected rank")
        require(receipt["member_theta"] == expected["member_theta"] and
                receipt["dual"] == expected["dual"],
                "fixture expected equation")
        results.append({
            "case": case["name"],
            "closure_rank": context["closure_tableau"].rank,
            "kernel_dim": context["kernel_tableau"].rank,
            "full_nonzero_kernel_cardinality":
            len(context["nonzero_kernel"]),
            "Hd1_rank": context["Hd1_tableau"].rank,
            "target": context["target"],
            "slice_membership": context["is_member"],
            "terminal": receipt["terminal"],
            "checker_closure_transform_sha256":
            context["closure_tableau"].transcript_sha256,
            "checker_kernel_transform_sha256":
            context["kernel_tableau"].transcript_sha256,
            "checker_Hd1_transform_sha256":
            context["Hd1_tableau"].transcript_sha256,
            "checker_receipt_closure_transform_sha256":
            receipt_context["receipt_closure"].transcript_sha256,
            "checker_receipt_kernel_transform_sha256":
            receipt_context["receipt_kernel"].transcript_sha256,
            "checker_receipt_Hd1_transform_sha256":
            receipt_context["receipt_Hd1"].transcript_sha256,
            "producer_transforms_directly_replayed": True,
            "two_way_span_checked": True,
        })
    producer_controls = producer.get("mutation_controls", [])
    require([record.get("owner") for record in producer_controls] ==
            list(OWNERS), "producer mutation owner roster")
    require(producer.get("mutation_attempted") == len(OWNERS) and
            producer.get("mutation_rejected") == len(OWNERS),
            "producer mutation accounting")
    independent_controls = [
        verify_mutation_control(fixture, producer_cases, contexts,
                                producer_record, owner)
        for producer_record, owner in zip(producer_controls, OWNERS)
    ]
    require(len(independent_controls) == len(OWNERS),
            "independent mutation count")
    return {
        "schema": SCHEMA + "/checker-verdict/v11",
        "accepted": True, "independent": True,
        "terminal": "SELFTEST_COMPLETE", "cases": results,
        "mutation_attempted": len(independent_controls),
        "mutation_rejected": len(independent_controls),
        "wrong_fixture_seal_rejected": wrong_fixture_rejected,
        "wrong_producer_seal_rejected": wrong_producer_rejected,
        "producer_mutation_transcripts_independently_replayed": True,
        "independent_mutation_controls": independent_controls,
        "producer_imported": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"),
                        required=True)
    parser.add_argument("--fixture", type=Path, default=ROOT / FIXTURE)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    try:
        verdict = (run(arguments.fixture, arguments.receipt)
                   if arguments.mode == "SELFTEST" else
                   {"schema": SCHEMA, "accepted": False,
                    "independent": True, "status": STATIC,
                    "terminal": STATIC})
    except Exception as exception:
        verdict = {"schema": SCHEMA + "/checker-verdict/v11",
                   "accepted": False, "independent": True,
                   "status": "UNKNOWN_INPUT", "terminal": "UNKNOWN_INPUT",
                   "reason": str(exception), "producer_imported": False}
    verdict_body = dict(verdict)
    verdict = dict(verdict_body,
                   verdict_digest_sha256=digest(verdict_body))
    arguments.output.write_bytes(canon(verdict) + b"\n")
    if verdict.get("accepted"):
        print(PASS + " mutation_attempted=%d mutation_rejected=%d" %
              (verdict["mutation_attempted"],
               verdict["mutation_rejected"]))
        print("R07_JOINT_SLICE_KERNEL_GENERAL_V11_CHECKER_TERMINAL "
              "SELFTEST_COMPLETE")
    else:
        print("R07_JOINT_SLICE_KERNEL_GENERAL_V11_CHECKER_TERMINAL " +
              verdict["terminal"])


if __name__ == "__main__":
    main()
