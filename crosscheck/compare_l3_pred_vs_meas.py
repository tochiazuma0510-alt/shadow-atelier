# -*- coding: utf-8 -*-
# L3-PRED-v1 (mathematician, blind) vs w6_bu_s35_v2 cert (implementer, sealed)
# Machine comparison only - no hand-copied values.
import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NOTE = r"C:\Users\81905\Desktop\shadow-atelier\docs\notes\theorem_check_mirrorall_l3vacuous_v1.md"
CERT = r"C:\Users\81905\Desktop\shadow-atelier\search\certs\w6_bu_s35_v2_20260806.json"

txt = open(NOTE, encoding='utf-8').read()
m = re.search(r"```json\s*(\{.*?\})\s*```", txt, re.S)
pred = json.loads(m.group(1))
cert = json.load(open(CERT, encoding='utf-8'))

# locate per-row data in cert (flexible key discovery)
def find_rows(obj, path=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            hits += find_rows(v, path + "/" + k)
    elif isinstance(obj, list) and obj and isinstance(obj[0], dict) and any(
            "module" in str(k).lower() for k in obj[0]):
        hits.append((path, obj))
    return hits

rowsets = find_rows(cert)
print("cert row-lists found:", [(p, len(r)) for p, r in rowsets])
path, rows = max(rowsets, key=lambda t: len(t[1]))
print("using:", path, "| first-row keys:", sorted(rows[0].keys()))

def pick(d, *cands):
    for c in cands:
        for k in d:
            if c == str(k).lower():
                return d[k]
    for c in cands:
        for k in d:
            if c in str(k).lower():
                return d[k]
    return None

meas = {}
for r in rows:
    mid = pick(r, "module_id", "module")
    meas[mid] = {
        "lifts": pick(r, "affine_solution_pairs", "solution_pairs", "pairs", "lifts"),
        "L3": pick(r, "l3_surjective", "l3_true", "l3"),
        "orbits": pick(r, "mark_iso_orbits", "orbits"),
        "dist": pick(r, "image_order_dist", "order_dist", "im_order", "image_orders", "diagnostic"),
    }

ok = bad = 0
for pr in pred["rows"]:
    mid = pr["module_id"]
    mrow = meas.get(mid)
    if mrow is None:
        print("MISSING in cert:", mid); bad += 1; continue
    problems = []
    if pr.get("lifts") is not None and mrow["lifts"] != pr["lifts"]:
        problems.append(f"lifts pred={pr['lifts']} meas={mrow['lifts']}")
    if mrow["L3"] != pr["L3"]:
        problems.append(f"L3 pred={pr['L3']} meas={mrow['L3']}")
    pdist = pr.get("image_order_dist") or pr.get("dist")
    if pdist is not None and mrow["dist"] is not None:
        nd = {int(k): v for k, v in (pdist.items() if isinstance(pdist, dict) else pdist)}
        md_raw = mrow["dist"]
        md = {int(k): v for k, v in (md_raw.items() if isinstance(md_raw, dict) else md_raw)}
        if nd != md:
            problems.append(f"dist pred={nd} meas={md}")
    if problems:
        bad += 1; print("MISMATCH", mid, ";", "; ".join(problems))
    else:
        ok += 1; print("match  ", mid, f"L3={pr['L3']}")

tot_pred = pred.get("total_L3_true"); tot_meas = sum(v["L3"] for v in meas.values())
print(f"rows: match={ok} mismatch={bad}")
print(f"total L3: pred={tot_pred} meas={tot_meas} {'MATCH' if tot_pred==tot_meas else 'MISMATCH'}")
lift_pred = pred.get("total_marked_lifts"); lift_meas = sum(v["lifts"] for v in meas.values())
print(f"total lifts: pred={lift_pred} meas={lift_meas} {'MATCH' if lift_pred==lift_meas else 'MISMATCH'}")
