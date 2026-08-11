#!/usr/bin/env python
# crosscheck/check_w691_gen23_braid_backconv.py
# Independent checker for search/certs/w691_gen23_braid_backconv_v1_20260812.json (裁定836).
#
# CROSSCHECK, NOT VERIFICATION. Does NOT call GAP, does NOT import
# search/w691_gen23_braid_backconv_v1.g. Independently reconstructs (a,b) from the ORIGINAL
# witness cert (search/certs/w691_gen23_witness_v1_20260812.json), applies the back-conversion
# x=v^-1*u,y=u^-1*v^2 with its own matrix-inverse implementation, and re-derives the braid
# relation and generation checks from scratch (reusing the Schreier-Sims order computation
# already validated in crosscheck/check_w691_gen23_witness.py).
import json

P = 691


def mat_mul(A, B, mod=P):
    return (
        ((A[0][0]*B[0][0] + A[0][1]*B[1][0]) % mod, (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % mod),
        ((A[1][0]*B[0][0] + A[1][1]*B[1][0]) % mod, (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % mod),
    )


def mat_det(A, mod=P):
    return (A[0][0]*A[1][1] - A[0][1]*A[1][0]) % mod


def mat_inv(A, mod=P):
    d = mat_det(A, mod)
    dinv = pow(d, mod - 2, mod)
    return (
        ((A[1][1]*dinv) % mod, ((-A[0][1]) % mod * dinv) % mod),
        (((-A[1][0]) % mod * dinv) % mod, (A[0][0]*dinv) % mod),
    )


def mat_vec(M, v, mod=P):
    return ((M[0][0]*v[0] + M[0][1]*v[1]) % mod, (M[1][0]*v[0] + M[1][1]*v[1]) % mod)


def canon(v, mod=P):
    if v[0] != 0:
        inv = pow(v[0], mod - 2, mod)
        return (1, (v[1] * inv) % mod)
    else:
        inv = pow(v[1], mod - 2, mod)
        return ((v[0] * inv) % mod, 1)


def build_proj_points(mod=P):
    pts = [canon((x, 1), mod) for x in range(mod)]
    pts.append(canon((1, 0), mod))
    return sorted(set(pts))


def perm_of_matrix(M, proj_pts, pos):
    return tuple(pos[canon(mat_vec(M, v))] for v in proj_pts)


def perm_compose(p, q):
    return tuple(p[q[i]] for i in range(len(q)))


def perm_inverse(p):
    inv = [0] * len(p)
    for i, x in enumerate(p):
        inv[x] = i
    return tuple(inv)


def group_order_from_perms(gens, n):
    ident = tuple(range(n))
    order = 1
    current_gens = list(gens)
    remaining_points = list(range(n))
    while current_gens and any(g != ident for g in current_gens):
        base = None
        for p in remaining_points:
            if any(g[p] != p for g in current_gens):
                base = p
                break
        if base is None:
            break
        remaining_points = [p for p in remaining_points if p != base]
        orbit = {base: ident}
        frontier = [base]
        while frontier:
            new_frontier = []
            for x in frontier:
                ux = orbit[x]
                for g in current_gens:
                    y = g[x]
                    if y not in orbit:
                        orbit[y] = perm_compose(g, ux)
                        new_frontier.append(y)
            frontier = new_frontier
        order *= len(orbit)
        schreier_gens = set()
        for x, ux in orbit.items():
            for g in current_gens:
                y = g[x]
                uy = orbit[y]
                uy_inv = perm_inverse(uy)
                s = perm_compose(uy_inv, perm_compose(g, ux))
                if s != ident:
                    schreier_gens.add(s)
        current_gens = list(schreier_gens)
    return order


def mult_group_order(a, b, mod=P):
    cur = {a % mod, b % mod, 1}
    changed = True
    while changed:
        changed = False
        new_elts = set()
        for x in cur:
            for g in (a, b):
                y = (x * g) % mod
                if y not in cur:
                    new_elts.add(y)
        if new_elts:
            cur |= new_elts
            changed = True
    return len(cur)


WITNESS_PATH = "search/certs/w691_gen23_witness_v1_20260812.json"
CERT_PATH = "search/certs/w691_gen23_braid_backconv_v1_20260812.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)


def main():
    witness = json.load(open(WITNESS_PATH, encoding="utf-8"))
    cert = json.load(open(CERT_PATH, encoding="utf-8"))

    if cert.get("schema") != "shadow-atelier/w691_gen23_braid_backconv_v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/w691_gen23_braid_backconv_v1")

    sl_order = 691 * (691**2 - 1)
    proj_pts = build_proj_points()
    pos = {v: i for i, v in enumerate(proj_pts)}

    cert_results = {r["label"]: r for r in cert["results"]}
    witness_results = {r["label"]: r for r in witness["results"]}

    for label, target_d in (("H_2", 2), ("H_6", 6)):
        wr = witness_results[label]
        w = wr["witness"]
        u = (tuple(w["a"][0]), tuple(w["a"][1]))
        v = (tuple(w["b"][0]), tuple(w["b"][1]))

        cr = cert_results.get(label)
        if cr is None:
            fail(f"{label}: missing from cert")
            continue

        # provenance: cert's own x,y should match our independent re-derivation of the
        # back-conversion applied to the SAME source witness (u,v)
        v_inv = mat_inv(v)
        u_inv = mat_inv(u)
        v2 = mat_mul(v, v)
        x = mat_mul(v_inv, u)
        y = mat_mul(u_inv, v2)

        cert_x = (tuple(cr["x"][0]), tuple(cr["x"][1]))
        cert_y = (tuple(cr["y"][0]), tuple(cr["y"][1]))
        if x != cert_x or y != cert_y:
            fail(f"{label}: back-converted x,y mismatch: rederived x={x} y={y}, cert x={cert_x} y={cert_y}")
        else:
            ok(f"{label}: back-converted x=v^-1*u, y=u^-1*v^2 independently reproduced exactly "
               f"from the SOURCE witness cert (not copied from the search script)")

        # braid relation
        xyx = mat_mul(mat_mul(x, y), x)
        yxy = mat_mul(mat_mul(y, x), y)
        braid_ok = (xyx == yxy)
        if braid_ok != cr["braid_relation_ok"]:
            fail(f"{label}: braid_relation_ok rederived={braid_ok} cert={cr['braid_relation_ok']}")
        else:
            ok(f"{label}: braid_relation_ok = {braid_ok} (x*y*x == y*x*y independently confirmed)")

        # generation check via fast projective action (same decisive method as the witness checker)
        perm_x = perm_of_matrix(x, proj_pts, pos)
        perm_y = perm_of_matrix(y, proj_pts, pos)
        size_perm = group_order_from_perms([perm_x, perm_y], 692)
        if size_perm != cr["size_perm"]:
            fail(f"{label}: size_perm rederived={size_perm} cert={cr['size_perm']}")
        else:
            ok(f"{label}: size_perm = {size_perm} independently re-derived (Schreier-Sims)")
        if size_perm != sl_order:
            fail(f"{label}: size_perm != |SL(2,691)|={sl_order} -- generation NOT confirmed")

        det_order = mult_group_order(mat_det(x), mat_det(y))
        if det_order != cr["det_order"]:
            fail(f"{label}: det_order rederived={det_order} cert={cr['det_order']}")
        else:
            ok(f"{label}: det_order = {det_order} independently re-derived")
        if det_order != target_d:
            fail(f"{label}: det_order {det_order} != target_d {target_d}")

        generates_ok_rederived = (size_perm == sl_order and det_order == target_d)
        if generates_ok_rederived != cr["generates_H_d"]:
            fail(f"{label}: generates_H_d rederived={generates_ok_rederived} cert={cr['generates_H_d']}")
        else:
            ok(f"{label}: generates_H_d = {generates_ok_rederived} (braid pair (x,y) independently "
               f"confirmed to generate H_{target_d})")

    rederived_all_ok = all(
        cert_results[l]["braid_relation_ok"] and cert_results[l]["generates_H_d"]
        for l in ("H_2", "H_6")
    ) and not fails
    if not fails and rederived_all_ok != cert.get("all_ok"):
        fail(f"all_ok rederived={rederived_all_ok} cert={cert.get('all_ok')}")
    elif not fails:
        ok(f"all_ok = {rederived_all_ok}")

    print()
    if fails:
        print(f"RESULT: FAIL ({len(fails)} mismatches)")
        return 1
    else:
        print("RESULT: PASS (cross-checked, not verified -- 検証は Lean 専有; FULL independent "
              "re-derivation including the back-conversion arithmetic and the decisive "
              "generation check)")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
