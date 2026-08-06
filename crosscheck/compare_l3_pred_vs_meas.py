# -*- coding: utf-8 -*-
# L3-PRED-v1 (mathematician, blind) vs w6_bu_s35_v2.1 cert (implementer, sealed)
# Machine comparison only - no hand-copied values.
#
# v2.1 fix (裁定615 item 1, falsifier judgment): the original version of
# this script silently SKIPPED the image-order-distribution comparison
# whenever the cert side could not find a matching key (the prediction uses
# "image_orders" as a per-ROW dict; the cert only ever carried per-CLASS
# distributions under rows[].class_detail[].sizeH_distribution, so the
# fuzzy `pick()` lookup for a row-level "image_orders"-like key always
# returned None and the whole distribution check was quietly bypassed --
# every row appeared to "match" on lifts/L3 alone while the sharper P-L3-1
# .. P-L3-5 predictions were never actually checked).
#
# Fixed here:
#   (a) the cert-side per-row distribution is now computed HONESTLY by
#       summing rows[].class_detail[].sizeH_distribution across all classes
#       in that row (that field name is exactly what 司令塔 named as the
#       correct alignment target) -- not looked up by fuzzy key guessing.
#   (b) FAIL-CLOSED: if EITHER side is missing ANY comparable value (module
#       row missing, lifts missing, L3 missing, or distribution missing/
#       unaggregable on either side), that row is now a FAIL, never a
#       silent skip. There is no code path left that treats "data not
#       found" as "nothing to compare".
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NOTE = r"C:\Users\81905\Desktop\shadow-atelier\docs\notes\theorem_check_mirrorall_l3vacuous_v1.md"
CERT = r"C:\Users\81905\Desktop\shadow-atelier\search\certs\w6_bu_s35_v2_1_20260806.json"


def load_prediction(path):
    import re
    txt = open(path, encoding='utf-8').read()
    m = re.search(r"```json\s*(\{.*?\})\s*```", txt, re.S)
    if m is None:
        print("FAIL_CLOSED: could not locate the ```json ... ``` prediction block in", path)
        sys.exit(1)
    return json.loads(m.group(1))


def aggregate_row_distribution(row):
    """Sum rows[].class_detail[].sizeH_distribution across all classes of
    one cert row -> {int(order): int(count)}. FAILS CLOSED (raises) rather
    than returning an empty/partial dict if class_detail or
    sizeH_distribution is missing or malformed -- a caller that wants a
    soft "None" must catch explicitly; this function never silently
    produces {} to mean "nothing found"."""
    class_detail = row.get("class_detail")
    if class_detail is None:
        raise ValueError(f"row {row.get('module_id')}: no class_detail field at all")
    agg = {}
    saw_any_dist = False
    for c in class_detail:
        dist = c.get("sizeH_distribution")
        if dist is None:
            raise ValueError(f"row {row.get('module_id')}: a class_detail entry (vec={c.get('vec')}) has no sizeH_distribution key")
        for k, v in dist.items():
            agg[int(k)] = agg.get(int(k), 0) + int(v)
            saw_any_dist = True
    if not saw_any_dist and row.get("accepted_classes", 0) > 0:
        raise ValueError(f"row {row.get('module_id')}: accepted_classes>0 but no sizeH_distribution entries were found anywhere in class_detail")
    return agg


def main():
    pred = load_prediction(NOTE)
    cert = json.load(open(CERT, encoding='utf-8'))

    rows = cert.get("rows")
    if not rows:
        print("FAIL_CLOSED: cert has no 'rows' array")
        sys.exit(1)

    meas = {}
    agg_errors = {}
    for r in rows:
        mid = r.get("module_id")
        if mid is None:
            print("FAIL_CLOSED: a cert row has no module_id:", r)
            sys.exit(1)
        try:
            dist = aggregate_row_distribution(r)
        except ValueError as e:
            dist = None
            agg_errors[mid] = str(e)
        meas[mid] = {
            "lifts": r.get("affine_solution_pairs"),
            "L3": r.get("L3_surjective_lifts"),
            "orbits": r.get("MARK_ISO_orbits"),
            "dist": dist,
        }

    ok = bad = 0
    for pr in pred["rows"]:
        mid = pr["module_id"]
        problems = []

        mrow = meas.get(mid)
        if mrow is None:
            problems.append("MISSING in cert (fail-closed: no silent skip)")
            bad += 1
            print("FAIL", mid, ";", "; ".join(problems))
            continue

        # lifts: fail-closed (both sides required, must be present and equal)
        pred_lifts = pr.get("lifts")
        if pred_lifts is None or mrow["lifts"] is None:
            problems.append(f"lifts missing on one side (pred={pred_lifts}, meas={mrow['lifts']}) -- fail-closed, not skipped")
        elif mrow["lifts"] != pred_lifts:
            problems.append(f"lifts pred={pred_lifts} meas={mrow['lifts']}")

        # L3: fail-closed (both sides required, must be present and equal)
        pred_l3 = pr.get("L3")
        if pred_l3 is None or mrow["L3"] is None:
            problems.append(f"L3 missing on one side (pred={pred_l3}, meas={mrow['L3']}) -- fail-closed, not skipped")
        elif mrow["L3"] != pred_l3:
            problems.append(f"L3 pred={pred_l3} meas={mrow['L3']}")

        # distribution: fail-closed (both sides required, must be present and equal)
        pred_dist_raw = pr.get("image_orders")
        if pred_dist_raw is None:
            problems.append("prediction has no image_orders field -- fail-closed, not skipped")
        elif mrow["dist"] is None:
            problems.append(f"cert-side distribution unavailable: {agg_errors.get(mid, 'unknown aggregation failure')} -- fail-closed, not skipped")
        else:
            pred_dist = {int(k): v for k, v in pred_dist_raw.items()}
            if pred_dist != mrow["dist"]:
                problems.append(f"dist pred={pred_dist} meas={mrow['dist']}")

        if problems:
            bad += 1
            print("FAIL", mid, ";", "; ".join(problems))
        else:
            ok += 1
            print("match", mid, f"L3={pr['L3']} dist={mrow['dist']}")

    # totals: fail-closed (both must be present and match)
    tot_pred = pred.get("total_L3_true")
    tot_meas = sum(v["L3"] for v in meas.values() if v["L3"] is not None)
    if tot_pred is None:
        print("FAIL total L3: prediction has no total_L3_true field")
        bad += 1
    else:
        print(f"total L3: pred={tot_pred} meas={tot_meas} {'MATCH' if tot_pred == tot_meas else 'MISMATCH'}")
        if tot_pred != tot_meas:
            bad += 1

    lift_pred = pred.get("total_marked_lifts")
    lift_meas = sum(v["lifts"] for v in meas.values() if v["lifts"] is not None)
    if lift_pred is None:
        print("FAIL total lifts: prediction has no total_marked_lifts field")
        bad += 1
    else:
        print(f"total lifts: pred={lift_pred} meas={lift_meas} {'MATCH' if lift_pred == lift_meas else 'MISMATCH'}")
        if lift_pred != lift_meas:
            bad += 1

    print()
    print(f"rows: match={ok} mismatch/fail={bad}")
    if bad > 0:
        print("RESULT: FAIL (fail-closed)")
        sys.exit(1)
    else:
        print("RESULT: PASS (all rows + totals matched, fail-closed comparator, distribution keys aligned)")
        sys.exit(0)


if __name__ == "__main__":
    main()
