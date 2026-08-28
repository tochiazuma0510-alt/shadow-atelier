#!/usr/bin/env python3
"""Independent reverse-order checker for the minimal typed joint slice."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "d972-r07-joint-slice-kernel-general/v4"
SELF = SCHEMA + "/selftest"
FIXTURE = "search/certs/d972_r07_joint_slice_kernel_general_selftest_v4_20260828.json"
PASS = "R07_JOINT_SLICE_KERNEL_GENERAL_V4_CHECKER_SELFTEST_PASS"
OWNERS = ("field_modulus", "theta_seed", "theta_action", "z_action", "eta_action", "D_entry", "O_entry", "C_entry", "action_order", "premature_C", "target", "seed_index", "parent", "row_theta", "left_kernel", "Hd1", "member_ancestry", "dual", "terminal")

def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")

def digest(value):
    return hashlib.sha256(canon(value)).hexdigest()

def vec(matrix, value):
    return [sum(matrix[i][j] * value[j] for j in range(len(value))) % 3 for i in range(len(matrix))]

def mmul(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(len(right[0]))) % 3
             for j in range(len(right[0]))] for i in range(len(left))]

def check_matrix(matrix, size):
    require(isinstance(matrix, list) and len(matrix) == size and
            all(isinstance(row, list) and len(row) == size and
                all(type(x) is int and x % 3 == x for x in row)
                for row in matrix), "matrix")
    require(rank(matrix) == size, "invertible action")

def check_map(matrix, rows, columns):
    require(isinstance(matrix, list) and len(matrix) == rows and
            all(isinstance(row, list) and len(row) == columns and
                all(type(x) is int and x % 3 == x for x in row)
                for row in matrix), "map")

def rank(rows):
    work = [[x % 3 for x in row] for row in rows]
    r = 0
    for c in range(len(work[0]) if work else 0):
        pivot = next((i for i in range(r, len(work)) if work[i][c]), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        inv = 1 if work[r][c] == 1 else 2
        work[r] = [(inv * x) % 3 for x in work[r]]
        for i in range(len(work)):
            if i != r and work[i][c]:
                q = work[i][c]
                work[i] = [(work[i][j] - q * work[r][j]) % 3 for j in range(len(work[i]))]
        r += 1
    return r

def left_kernel(rows):
    count = len(rows)
    coordinates = len(rows[0]) if rows else 0
    reverse_pivot_order = tuple(reversed(range(coordinates)))
    return [list(x) for x in itertools.product(range(3), repeat=count)
            if any(x) and all(sum(x[j] * rows[j][i] for j in range(count)) % 3 == 0
                              for i in reverse_pivot_order)]

def member(rows, target):
    if not rows:
        return not any(target)
    return rank(rows) == rank(rows + [target])

def span_contains(rows, target):
    return member(rows, target)

def solve(rows, target):
    for coefficients in itertools.product(range(3), repeat=len(rows)):
        value = [sum(coefficients[j] * rows[j][i] for j in range(len(rows))) % 3
                 for i in range(len(target))]
        if value == [x % 3 for x in target]:
            return list(coefficients)
    raise RuntimeError("combined theta outside span")

def require(condition, message):
    if condition is not True:
        raise RuntimeError(message)

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def replay(case, receipt):
    require(receipt["case"] == case["name"], "case identity")
    require(case.get("modulus") == 3 and case.get("occurrence_count") == 11, "typed field")
    require(case.get("occurrence_tags") == ["occurrence%02d" % i for i in range(11)], "occurrence labels")
    require(case["A_theta"] == case["A_theta_binding"], "theta action owner")
    require(case["A_Z"] == case["A_Z_binding"] and case["A_E"] == case["A_E_binding"], "action owner")
    require(case["D"] == case["D_binding"] and case["O"] == case["O_binding"] and case["C"] == case["C_binding"], "map owner")
    require(case["action_names"] == case["action_order_binding"] and case["theta_seeds"] == case["seed_bindings"], "seed/action order")
    require(case["C_phase"] == "after-closure", "premature C")
    tdim = len(case["theta_seeds"][0]); zdim = len(case["D"]); edim = len(case["O"]); qdim = len(case["C"])
    check_matrix(case["A_theta"], tdim); check_matrix(case["A_Z"], zdim); check_matrix(case["A_E"], edim)
    check_map(case["D"], zdim, tdim); check_map(case["O"], edim, tdim); check_map(case["C"], qdim, edim)
    require(mmul(case["D"], case["A_theta"]) == mmul(case["A_Z"], case["D"]), "D equivariance")
    require(mmul(case["O"], case["A_theta"]) == mmul(case["A_E"], case["O"]), "O equivariance")
    require(len(case["actions"]) == len(case["action_names"]), "action count")
    for name, action in zip(case["action_names"], case["actions"]):
        require(action["name"] == name, "action name")
        check_matrix(action["theta_matrix"],tdim); check_matrix(action["z_matrix"],zdim); check_matrix(action["eta_matrix"],edim)
        require(mmul(case["D"],action["theta_matrix"]) == mmul(action["z_matrix"],case["D"]) and mmul(case["O"],action["theta_matrix"]) == mmul(action["eta_matrix"],case["O"]), "action equivariance")
    rows = []
    queue = [(list(seed), None, i, None, "seed") for i, seed in enumerate(case["theta_seeds"])]
    while queue:
        current, parent, seed_index, action_name, kind = queue.pop(0)
        z = vec(case["D"], current)
        eta = vec(case["O"], current)
        flat = z + eta
        current_rank = rank([item["flat"] for item in rows])
        if rows and rank([item["flat"] for item in rows] + [flat]) == current_rank:
            continue
        rows.append({"theta": current, "z": z, "eta": eta, "flat": flat, "parent": parent, "action": action_name, "seed_index": seed_index, "kind": kind})
        basis_rows = [item["flat"] for item in rows]
        for name, action in reversed(list(zip(case["action_names"], case["actions"]))):
            candidate = vec(action["theta_matrix"], current)
            candidate_flat = vec(case["D"], candidate) + vec(case["O"], candidate)
            if rank(basis_rows + [candidate_flat]) > rank(basis_rows):
                queue.append((candidate, len(rows) - 1, seed_index, name, "action"))
    images = [vec(case["C"], item["eta"]) for item in rows]
    kernel = left_kernel(images)
    hd1 = [[sum(a[j] * rows[j]["z"][i] for j in range(len(rows))) % 3 for i in range(zdim)] for a in kernel]
    theta_hd1 = [[sum(a[j] * rows[j]["theta"][i] for j in range(len(rows))) % 3 for i in range(tdim)] for a in kernel]
    eta_hd1 = [[sum(a[j] * rows[j]["eta"][i] for j in range(len(rows))) % 3 for i in range(len(case["O"]))] for a in kernel]
    for theta_a, h_a, eta_a in zip(theta_hd1, hd1, eta_hd1):
        require(h_a == vec(case["D"], theta_a) and all(x == 0 for x in vec(case["C"], eta_a)), "kernel reconstruction")
    target = [x % 3 for x in case["target"]]
    is_member = member(hd1, target)
    require(is_member == (case["terminal"] == "MEMBER"), "membership")
    require(receipt["terminal"] == case["terminal"] and receipt["terminal"] == ("MEMBER" if is_member else "NONMEMBER"), "receipt terminal")
    require(span_contains([item["flat"] for item in rows], receipt["rows"][0]["flat"]), "producer row containment")
    require(all(span_contains([item["flat"] for item in rows], item["flat"]) for item in receipt["rows"]), "producer rows in checker span")
    require(all(span_contains([item["flat"] for item in receipt["rows"]], item["flat"]) for item in rows), "checker rows in producer span")
    require(receipt["closure_rank"] == rank([item["flat"] for item in rows]), "closure rank")
    for i,item in enumerate(receipt["rows"]):
        require(rank([row["flat"] for row in receipt["rows"][:i]] + [item["flat"]]) == i + 1, "receipt basis rank")
    action_by_name={action["name"]:action for action in case["actions"]}
    for i,item in enumerate(receipt["rows"]):
        require(item["z"] == vec(case["D"],item["theta"]) and item["eta"] == vec(case["O"],item["theta"]) and item["flat"] == item["z"] + item["eta"], "row typed replay")
        if item["kind"] == "seed":
            require(item["parent"] is None and item["action"] == "seed" and 0 <= item["seed_index"] < len(case["theta_seeds"]) and item["theta"] == case["theta_seeds"][item["seed_index"]], "seed replay")
        else:
            require(item["kind"] == "action" and isinstance(item["parent"],int) and 0 <= item["parent"] < i and item["action"] in action_by_name and item["seed_index"] == receipt["rows"][item["parent"]]["seed_index"], "action ancestry")
            require(item["theta"] == vec(action_by_name[item["action"]]["theta_matrix"],receipt["rows"][item["parent"]]["theta"]), "action theta replay")
    require(receipt["rows"][0]["parent"] is None and receipt["rows"][0]["action"] == "seed", "seed ancestry")
    receipt_kernel = receipt["left_kernel_basis"]
    require(isinstance(receipt_kernel,list) and all(len(a) == len(images) and any(a) and
                                   all(sum(a[j] * images[j][i] for j in range(len(images))) % 3 == 0
                                       for i in range(len(images[0])))
                                   for a in receipt_kernel), "kernel receipt")
    require(rank(receipt_kernel) == len(receipt_kernel), "kernel basis independence")
    require(len(kernel) + 1 == 3 ** len(receipt_kernel), "full kernel cardinality")
    require(all(span_contains(receipt_kernel, a) for a in kernel), "kernel basis spans full kernel")
    require(rank(hd1) == receipt["Hd1_rank"], "Hd1 rank")
    receipt_hd1=receipt["Hd1"]
    require(rank(receipt_hd1)==rank(hd1) and all(span_contains(receipt_hd1,h) for h in hd1) and all(span_contains(hd1,h) for h in receipt_hd1), "Hd1 content")
    if is_member:
        require(receipt["member_theta"] is not None, "member coefficient")
        combined = receipt["member_theta"]
        require(vec(case["D"], combined) == target and all(x == 0 for x in vec(case["C"], vec(case["O"], combined))), "member equations")
        require(span_contains(theta_hd1, combined), "member ancestry")
    else:
        duals = [x for x in itertools.product(range(3), repeat=len(target)) if any(x) and all(sum(x[i] * h[i] for i in range(len(target))) % 3 == 0 for h in hd1) and sum(x[i] * target[i] for i in range(len(target))) % 3 == 1]
        require(duals and receipt["dual"] is not None, "dual replay")
        dual = receipt["dual"]
        require(all(sum(dual[i] * h[i] for i in range(zdim)) % 3 == 0 for h in hd1) and sum(dual[i] * target[i] for i in range(zdim)) % 3 == 1, "dual equations")
    return {"case": case["name"], "closure_rank": rank([item["flat"] for item in rows]), "left_kernel_dim": len(receipt_kernel), "full_nonzero_kernel_cardinality": len(kernel), "Hd1_rank": rank(hd1), "terminal": receipt["terminal"], "reverse_span_checked": True}

def independent_terminal(case):
    """Independent mutation oracle: rebuild only from the raw case fields."""
    require(case.get("modulus") == 3 and case.get("occurrence_count") == 11, "typed field")
    require(case.get("occurrence_tags") == ["occurrence%02d" % i for i in range(11)], "occurrence labels")
    require(case["A_theta"] == case["A_theta_binding"] and case["A_Z"] == case["A_Z_binding"] and case["A_E"] == case["A_E_binding"], "action owner")
    require(case["D"] == case["D_binding"] and case["O"] == case["O_binding"] and case["C"] == case["C_binding"], "map owner")
    require(case["action_names"] == case["action_order_binding"] and case["theta_seeds"] == case["seed_bindings"] and case["C_phase"] == "after-closure" and case["left_kernel_method"] == "rref", "control owner")
    tdim=len(case["theta_seeds"][0]); zdim=len(case["D"]); edim=len(case["O"]); qdim=len(case["C"])
    check_matrix(case["A_theta"],tdim); check_matrix(case["A_Z"],zdim); check_matrix(case["A_E"],edim)
    check_map(case["D"],zdim,tdim); check_map(case["O"],edim,tdim); check_map(case["C"],qdim,edim)
    require(mmul(case["D"],case["A_theta"]) == mmul(case["A_Z"],case["D"]), "D equivariance")
    require(mmul(case["O"],case["A_theta"]) == mmul(case["A_E"],case["O"]), "O equivariance")
    rows=[]; queue=[(list(seed),None,i,None,"seed") for i,seed in enumerate(case["theta_seeds"])]
    while queue:
        theta,parent,seed_index,name,kind=queue.pop(0); z=vec(case["D"],theta); eta=vec(case["O"],theta); flat=z+eta
        current_rank=rank([item["flat"] for item in rows])
        if rows and rank([item["flat"] for item in rows]+[flat])==current_rank: continue
        rows.append({"theta":theta,"z":z,"eta":eta,"flat":flat,"parent":parent,"action":name,"seed_index":seed_index,"kind":kind})
        basis_rows=[item["flat"] for item in rows]
        for action_name,action in zip(case["action_names"],case["actions"]):
            require(action["name"]==action_name, "action binding")
            check_matrix(action["theta_matrix"],tdim);check_matrix(action["z_matrix"],zdim);check_matrix(action["eta_matrix"],edim)
            require(mmul(case["D"],action["theta_matrix"])==mmul(action["z_matrix"],case["D"]) and mmul(case["O"],action["theta_matrix"])==mmul(action["eta_matrix"],case["O"]), "action equivariance")
            candidate=vec(action["theta_matrix"],theta); candidate_flat=vec(case["D"],candidate)+vec(case["O"],candidate)
            if rank(basis_rows+[candidate_flat])>rank(basis_rows): queue.append((candidate,len(rows)-1,seed_index,action_name,"action"))
    images=[vec(case["C"],item["eta"]) for item in rows]; kernel=left_kernel(images)
    hd1=[[sum(a[j]*rows[j]["z"][i] for j in range(len(rows)))%3 for i in range(zdim)] for a in kernel]
    target=[x%3 for x in case["target"]]; computed="MEMBER" if member(hd1,target) else "NONMEMBER"
    require(case["terminal"]==computed,"terminal semantic gate")
    return computed

def checker_mutate(case, receipt, owner):
    mutated_case=json.loads(json.dumps(case)); mutated_receipt=json.loads(json.dumps(receipt))
    fixture_owners={"field_modulus","theta_seed","theta_action","z_action","eta_action","D_entry","O_entry","C_entry","action_order","premature_C","target"}
    if owner in fixture_owners:
        if owner=="field_modulus": mutated_case["modulus"]=9
        elif owner=="theta_seed": mutated_case["theta_seeds"][0][0]=(mutated_case["theta_seeds"][0][0]+1)%3
        elif owner=="theta_action": mutated_case["A_theta"][0][0]=2
        elif owner=="z_action": mutated_case["A_Z"][0][0]=2
        elif owner=="eta_action": mutated_case["A_E"][0][0]=2
        elif owner=="D_entry": mutated_case["D"][0][0]=2
        elif owner=="O_entry": mutated_case["O"][0][0]=2
        elif owner=="C_entry": mutated_case["C"][0][0]=2
        elif owner=="action_order": mutated_case["action_names"]=["mutated-action"]
        elif owner=="premature_C": mutated_case["C_phase"]="before-closure"
        elif owner=="target": mutated_case["target"]=[1,0]
        mutated_case["mutation_fixture_seal"]=digest(mutated_case)
        try:
            independent_terminal(mutated_case)
            return False
        except (RuntimeError,ValueError,KeyError,TypeError,IndexError):
            return True
    if owner=="seed_index": mutated_receipt["rows"][1]["seed_index"]=99
    elif owner=="parent": mutated_receipt["rows"][1]["parent"]=99
    elif owner=="row_theta": mutated_receipt["rows"][1]["theta"][0]=(mutated_receipt["rows"][1]["theta"][0]+1)%3
    elif owner=="left_kernel": mutated_receipt["left_kernel_basis"][0]=[1,1]; mutated_receipt["left_kernel_basis"][1]=[1,1]
    elif owner=="Hd1": mutated_receipt["Hd1"][0]=[1,1]
    elif owner=="member_ancestry": mutated_receipt["member_theta"][0]=(mutated_receipt["member_theta"][0]+1)%3
    elif owner=="dual": mutated_receipt["dual"][0]=(mutated_receipt["dual"][0]+1)%3
    elif owner=="terminal": mutated_receipt["terminal"]="MUTATED"
    else: raise RuntimeError("unknown mutation owner")
    body=dict(mutated_receipt); body.pop("self_digest_sha256",None); mutated_receipt["self_digest_sha256"]=digest(body)
    try:
        replay(mutated_case,mutated_receipt)
        return False
    except (RuntimeError,ValueError,KeyError,TypeError,IndexError):
        return True

def run(fixture, receipt):
    f = load(fixture)
    require(f.get("schema") == SELF and f.get("fixture_seal"), "fixture")
    require(len(f.get("cases", [])) == 5, "five cases")
    require(f.get("typed_basis") == {"Theta":["theta0","theta1"],"Z":["z0","z1"],"E_hat":["occurrence%02d" % i for i in range(11)],"E":["printed0"]}, "typed basis")
    require(set(f.get("expected_cases",{})) == {case["name"] for case in f["cases"]}, "fixture expectations")
    require(f.get("mutation_roster") == list(OWNERS), "fixture mutation roster")
    p = load(receipt)
    require(p.get("schema") == SELF and p.get("status") == "COMPLETE", "producer receipt")
    claimed = p.get("self_digest_sha256")
    body = dict(p)
    body.pop("self_digest_sha256", None)
    require(type(claimed) is str and claimed == digest(body), "receipt seal")
    results = [replay(case, got) for case, got in zip(f["cases"], p.get("cases", []))]
    require(len(results) == 5, "case count")
    for case, result, got in zip(f["cases"], results, p["cases"]):
        expected=f["expected_cases"][case["name"]]
        require(result["closure_rank"]==expected["closure_rank"] and result["left_kernel_dim"]==expected["kernel_dim"] and result["full_nonzero_kernel_cardinality"]==expected["full_nonzero_kernel_cardinality"] and result["Hd1_rank"]==expected["Hd1_rank"], "fixture expected rank")
        require(got["member_theta"]==expected["member_theta"] and got["dual"]==expected["dual"], "fixture expected equation")
    controls = p.get("mutation_controls", [])
    require([x.get("owner") for x in controls] == list(OWNERS), "mutation owner roster")
    receipt_case_index={"seed_index":0,"parent":0,"row_theta":0,"left_kernel":0,"member_ancestry":0,"Hd1":1,"dual":1,"terminal":1}
    independent_controls = [{"owner": owner, "rejected": checker_mutate(f["cases"][receipt_case_index.get(owner,1)], p["cases"][receipt_case_index.get(owner,1)], owner)} for owner in OWNERS]
    require(all(x["rejected"] is True for x in independent_controls), "independent mutation gate")
    return {"schema": SCHEMA + "/checker-verdict/v4", "accepted": True, "independent": True, "terminal": "SELFTEST_COMPLETE", "cases": results, "mutation_attempted": len(independent_controls), "mutation_rejected": sum(x["rejected"] for x in independent_controls), "producer_mutation_controls_ignored": True, "independent_mutation_controls": independent_controls, "producer_imported": False}

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("SELFTEST", "PRODUCTION"), required=True)
    parser.add_argument("--fixture", type=Path, default=ROOT / FIXTURE)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        verdict = run(args.fixture, args.receipt) if args.mode == "SELFTEST" else {"schema": SCHEMA, "accepted": False, "independent": True, "status": "STATIC_BLOCKED:actual typed matrices are not staged", "terminal": "STATIC_BLOCKED:actual typed matrices are not staged"}
    except Exception as exc:
        verdict = {"schema": SCHEMA + "/checker-verdict/v4", "accepted": False, "independent": True, "status": "UNKNOWN_INPUT", "terminal": "UNKNOWN_INPUT", "reason": str(exc), "producer_imported": False}
    args.output.write_bytes(canon(verdict) + b"\n")
    if verdict.get("accepted"):
        print(PASS + " mutation_attempted=%d mutation_rejected=%d" % (verdict["mutation_attempted"], verdict["mutation_rejected"]))
    else:
        print("R07_JOINT_SLICE_KERNEL_GENERAL_V4_CHECKER_TERMINAL " + verdict["terminal"])

if __name__ == "__main__":
    main()
