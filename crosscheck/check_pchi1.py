#!/usr/bin/env python
# crosscheck/check_pchi1.py
# Independent checker for search/certs/pchi1_v1_20260811.json (P-CHI-1', 裁定803[3],
# docs/notes/hunting_chapter_v1_addendum_a.md §2.4).
#
# CROSSCHECK, NOT VERIFICATION. Does NOT call GAP, does NOT import search/pchi1_v1.g.
#
# DISCLOSED LIMITATION: the core per-member measurement (ChiefSeries + conjugation-action
# twist order on each prime-order chief factor) is a GAP-only group-theoretic computation on
# SmallGroup objects. This checker CANNOT independently re-derive that primitive without
# either re-running GAP or reimplementing chief-series+conjugation-action machinery in a
# second language -- neither is attempted, following the same established convention as
# crosscheck/check_hcen_ab.py and crosscheck/check_m5_win_chk.py (GAP primitives are ground
# truth; the checker's job is provenance/downstream-logic re-derivation).
#
# What IS independently checked:
#  (A) provenance: the 23-pair/46-member id_group domain list in this cert is IDENTICAL to
#      the one in the already cross-checked search/certs/hcen_ab_v1_20260811.json (fa7b175) --
#      re-extracted from that EARLIER cert's own "pairs" field independently, not copy-pasted
#      from pchi1_v1.g's source.
#  (B) M5 exclusion: confirms this cert's "members" list has exactly 23 entries (46 members),
#      NOT 24 (i.e. M5 is correctly excluded from the domain, per the addendum's own "census
#      全46メンバー" domain statement).
#  (C) downstream boolean re-derivation: max_twist_order, all_twist_orders_le_3,
#      any_twist_order_ge_5 are independently recomputed from the raw per-member twist lists
#      and compared against the cert's own reported values.
#  (D) sanity: every reported "p" is prime (pure arithmetic check, independent of GAP).
import json

CERT_PATH = "search/certs/pchi1_v1_20260811.json"
HCEN_AB_PATH = "search/certs/hcen_ab_v1_20260811.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def main():
    cert = json.load(open(CERT_PATH, encoding="utf-8"))
    hcen = json.load(open(HCEN_AB_PATH, encoding="utf-8"))

    if cert.get("schema") != "shadow-atelier/pchi1_v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/pchi1_v1")

    members = cert.get("members", [])
    if len(members) != 23:
        fail(f"members count = {len(members)}, want 23 (46 total via m0/m1)")
    else:
        ok("members count = 23 (46 total via m0/m1)")

    # (A) provenance: id_group domain identical to hcen_ab_v1's pairs[]
    hcen_pairs = {p["pair_fiber"]: p for p in hcen["pairs"]}
    domain_mismatches = []
    for m in members:
        pf = m["pair_fiber"]
        hp = hcen_pairs.get(pf)
        if hp is None:
            domain_mismatches.append(f"{pf}: not found in hcen_ab_v1's pairs[]")
            continue
        if m["index"] != hp["index"]:
            domain_mismatches.append(f"{pf}: index mismatch {m['index']} vs hcen_ab {hp['index']}")
        if tuple(m["m0_id_group"]) != tuple(hp["m0"]["id_group"]):
            domain_mismatches.append(f"{pf}: m0_id_group mismatch {m['m0_id_group']} vs hcen_ab {hp['m0']['id_group']}")
        if tuple(m["m1_id_group"]) != tuple(hp["m1"]["id_group"]):
            domain_mismatches.append(f"{pf}: m1_id_group mismatch {m['m1_id_group']} vs hcen_ab {hp['m1']['id_group']}")
    if len(members) != len(hcen_pairs):
        domain_mismatches.append(f"member count {len(members)} != hcen_ab_v1 pairs count {len(hcen_pairs)}")
    if domain_mismatches:
        for d in domain_mismatches:
            fail("domain mismatch: " + d)
    else:
        ok("all 23 pair_fiber/index/id_group entries match hcen_ab_v1_20260811.json's "
           "already-cross-checked domain exactly (provenance re-derivation)")

    # (B) prime sanity on all reported chief-factor primes
    bad_primes = []
    for m in members:
        for key in ("m0_twists", "m1_twists"):
            for t in m[key]:
                if not is_prime(t["p"]):
                    bad_primes.append((m["pair_fiber"], key, t["p"]))
    if bad_primes:
        for b in bad_primes:
            fail(f"non-prime 'p' reported: {b}")
    else:
        ok("all reported chief-factor 'p' values are prime")

    # (C) downstream boolean re-derivation
    all_twist_orders = []
    for m in members:
        for key in ("m0_twists", "m1_twists"):
            for t in m[key]:
                all_twist_orders.append(t["twist_order"])

    rederived_max = max(all_twist_orders) if all_twist_orders else 0
    rederived_all_le_3 = all(x <= 3 for x in all_twist_orders)
    rederived_any_ge_5 = any(x >= 5 for x in all_twist_orders)

    if rederived_max != cert.get("max_twist_order"):
        fail(f"max_twist_order rederived={rederived_max} cert={cert.get('max_twist_order')}")
    else:
        ok(f"max_twist_order = {rederived_max}")

    if rederived_all_le_3 != cert.get("all_twist_orders_le_3"):
        fail(f"all_twist_orders_le_3 rederived={rederived_all_le_3} cert={cert.get('all_twist_orders_le_3')}")
    else:
        ok(f"all_twist_orders_le_3 = {rederived_all_le_3}")

    if rederived_any_ge_5 != cert.get("any_twist_order_ge_5"):
        fail(f"any_twist_order_ge_5 rederived={rederived_any_ge_5} cert={cert.get('any_twist_order_ge_5')}")
    else:
        ok(f"any_twist_order_ge_5 = {rederived_any_ge_5}")

    print()
    print(f"raw summary: {len(all_twist_orders)} total (prime-order chief factor, twist_order) "
          f"observations across 46 members. distinct twist_order values seen: "
          f"{sorted(set(all_twist_orders))}")
    print("DISCLOSED LIMITATION: the core GAP computation (ChiefSeries + conjugation-action "
          "twist order per prime chief factor) is NOT independently re-derived by this checker "
          "(see module docstring) -- only provenance/domain match, prime sanity, and downstream "
          "boolean re-derivation are checked.")

    print()
    if fails:
        print(f"RESULT: FAIL ({len(fails)} mismatches)")
        return 1
    else:
        print("RESULT: PASS (cross-checked, not verified -- 検証は Lean 専有; core GAP primitive not independently re-derived, see docstring)")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
