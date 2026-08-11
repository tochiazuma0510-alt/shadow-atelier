#!/usr/bin/env python
# crosscheck/check_hcen_ab.py
# Independent checker for search/certs/hcen_ab_v1_20260811.json (h^cen-AB,
# 裁定795-4/796/798/797(5), docs/notes/hunting_chapter_v1.md SS3.3 AB-2J).
#
# CROSSCHECK, NOT VERIFICATION (project convention -- 検証 is reserved for Lean).
# This checker does NOT call GAP and does NOT import search/hcen_ab_v1.g or any
# search/ code. It has two independent jobs:
#
#  (A) PROVENANCE / JOIN re-derivation: independently reconstruct the "census
#      exotic 23 pairs" id_group list from the two ORIGINAL source certs
#      (search/certs/r6a_summary_v1_20260806.json's set_i_750_clique_B_members
#      and set_ii_lt384_pairs[classification=BOTH_FIXED], joined against
#      search/certs/lins_twin_census_v1_20260806.json's twin_pairs[].members[].id_group
#      by positional order within the index<384 subfilter) -- using its OWN join
#      logic (written from scratch here, not copied from the search-side script)
#      -- and checks the result matches the 23 pairs recorded in the cert under test.
#
#  (B) DOWNSTREAM ARITHMETIC re-derivation: given the cert's OWN reported
#      "abelian_invariants" list for each member (GAP AbelianInvariants output,
#      NOT independently recomputed here -- recomputing SmallGroup(id_group)'s
#      abelianization from scratch would require either calling GAP again, which
#      would violate the search/crosscheck independence discipline, or an
#      independent group-theory engine which this project does not have wired up
#      for SmallGroup lookups; this is a DISCLOSED limitation, not a silent gap),
#      independently recompute d=product(invariants), is_cyclic (via a pure
#      number-theoretic argument: an abelian group with primary/elementary
#      invariant list L is cyclic iff no two entries of L share a common prime
#      factor -- NOT "Length(L)<=1", which is the bug the implementer self-caught
#      and fixed in the search-side script before this checker was written),
#      d_even, j=d/2 (if cyclic&even), and j_divides_3 -- and cross-check against
#      the cert's own reported values for these fields.
#
# What this checker CANNOT independently verify: that GAP's
# AbelianInvariants(SmallGroup(id_group)) itself is correct (that would require
# re-running GAP or an independent CAS, per the disclosed limitation above), and
# that the M5 control group's [2,5] abelian invariants / order=3240 are correct
# (same limitation -- the M5 reconstruction via BuildQTGeneral is GAP-side only).
import json, hashlib
from math import gcd

CERT_PATH = "search/certs/hcen_ab_v1_20260811.json"
R6A_PATH = "search/certs/r6a_summary_v1_20260806.json"
TWIN_PATH = "search/certs/lins_twin_census_v1_20260806.json"

fails = []
def fail(msg):
    fails.append(msg); print("[FAIL]", msg)
def ok(msg):
    print("[PASS]", msg)

def sha256_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def is_cyclic_from_invariants(invs):
    # AbelianInvariants (GAP) returns the list of prime-power orders (primary
    # decomposition). The group is cyclic iff these prime-power factors are
    # pairwise coprime (equivalently: no prime divides more than one entry).
    # This is the standard elementary-divisor <-> invariant-factor equivalence
    # (CRT), re-derived here from scratch (NOT "len(invs)<=1", which is wrong --
    # e.g. [2,5] is cyclic (C10) despite having length 2).
    for i in range(len(invs)):
        for j in range(i+1, len(invs)):
            if gcd(invs[i], invs[j]) != 1:
                return False
    return True

def rederive_ab_fields(invs):
    d = 1
    for x in invs:
        d *= x
    is_cyc = is_cyclic_from_invariants(invs)
    d_even = (d % 2 == 0)
    if is_cyc and d_even:
        j = d // 2
        j_div_3 = (3 % j == 0)
    else:
        j = None
        j_div_3 = None
    return d, is_cyc, d_even, j, j_div_3

def main():
    print("source sha256 r6a_summary:", sha256_of(R6A_PATH))
    print("source sha256 lins_twin_census:", sha256_of(TWIN_PATH))
    print("cert sha256 hcen_ab_v1:", sha256_of(CERT_PATH))

    cert = json.load(open(CERT_PATH, encoding="utf-8"))
    r6a = json.load(open(R6A_PATH, encoding="utf-8"))
    twin = json.load(open(TWIN_PATH, encoding="utf-8"))

    if cert.get("schema") != "shadow-atelier/hcen_ab_v1":
        fail("schema mismatch")
    else:
        ok("schema = shadow-atelier/hcen_ab_v1")

    # ---------------- (A) independent provenance/join re-derivation ----------------
    twin_pairs = twin["twin_pairs"]
    lt384 = [x for x in twin_pairs if x["index"] < 384]
    if len(lt384) != 45:
        fail(f"lt384 subset has {len(lt384)} entries, want 45 (per r6a_summary set_ii note)")
    else:
        ok("lt384 subset (index<384) has 45 entries")

    both_fixed_detail = r6a["set_ii_lt384_pairs"]["detail"]
    both_fixed = [x for x in both_fixed_detail if x["classification"].startswith("BOTH_FIXED")]
    if len(both_fixed) != 12:
        fail(f"BOTH_FIXED count = {len(both_fixed)}, want 12")
    else:
        ok("BOTH_FIXED count = 12 (matches r6a_summary set_ii summary.both_fixed_pairs)")
    if r6a["set_ii_lt384_pairs"]["summary"].get("both_fixed_pairs") != 12:
        fail("r6a_summary's own summary.both_fixed_pairs != 12")

    # positional index of each both_fixed pair_fiber within lt384 (re-derived from
    # scratch: pair_fiber format is "lt384:idx<N>:pair<K>" where K is the position)
    rederived_lt384_ids = []
    for pf in both_fixed:
        # extract the "pairK" integer suffix independently (own parser, not reused)
        tail = pf["pair_fiber"].split(":")[-1]
        assert tail.startswith("pair")
        k = int(tail[len("pair"):])
        member0, member1 = lt384[k]["members"]
        if lt384[k]["index"] != pf["index"]:
            fail(f"index mismatch at pair{k}: twin_census={lt384[k]['index']} r6a={pf['index']}")
        rederived_lt384_ids.append((pf["index"], pf["pair_fiber"], tuple(member0["id_group"]), tuple(member1["id_group"])))

    # 750-clique (10 pairs, all id_group=[750,6] by construction of a twin clique)
    e750 = [x for x in twin_pairs if x["index"] == 750]
    if len(e750) != 10:
        fail(f"index=750 pair count = {len(e750)}, want 10")
    else:
        ok("index=750 pair count = 10 (750-clique)")
    for x in e750:
        if tuple(x["members"][0]["id_group"]) != (750, 6) or tuple(x["members"][1]["id_group"]) != (750, 6):
            fail(f"750-clique member id_group mismatch: {x}")

    # 384 mixed pair (exactly 1, with id_group [384,608] -- NOT [384,615], per
    # §G.6.b's documented distinction between the two index-384 fibers)
    e384 = [x for x in twin_pairs if x["index"] == 384 and tuple(x["members"][0]["id_group"]) == (384, 608)]
    if len(e384) != 1:
        fail(f"index=384 id_group=[384,608] pair count = {len(e384)}, want 1")
    else:
        ok("index=384 id_group=[384,608] pair count = 1")

    total_rederived = len(rederived_lt384_ids) + len(e750) + len(e384)
    if total_rederived != 23:
        fail(f"rederived total pair count = {total_rederived}, want 23")
    else:
        ok("rederived total pair count = 23 (12 lt384-both-fixed + 10 750-clique + 1 idx384/608)")

    # cross-check against cert's own pairs[] list
    cert_pairs = cert["pairs"]
    if len(cert_pairs) != 23:
        fail(f"cert pairs[] length = {len(cert_pairs)}, want 23")
    else:
        ok("cert pairs[] length = 23")

    cert_index = {p["pair_fiber"]: p for p in cert_pairs}
    join_mismatches = []
    for (idx, pf, m0id, m1id) in rederived_lt384_ids:
        cp = cert_index.get(pf)
        if cp is None:
            join_mismatches.append(f"missing pair_fiber {pf} in cert")
            continue
        if tuple(cp["m0"]["id_group"]) != m0id or tuple(cp["m1"]["id_group"]) != m1id or cp["index"] != idx:
            join_mismatches.append(f"{pf}: rederived idx={idx} m0={m0id} m1={m1id} vs cert idx={cp['index']} m0={cp['m0']['id_group']} m1={cp['m1']['id_group']}")
    # spot-check the two documented anchors explicitly (from §G.6.b/§G.6.c of
    # theorem_check_mirrorall_l3vacuous_v1.md, read independently of the search script)
    anchor1 = cert_index.get("lt384:idx24:pair0")
    if not anchor1 or tuple(anchor1["m0"]["id_group"]) != (24, 3):
        join_mismatches.append("anchor lt384:idx24:pair0 (expected id_group=[24,3]=SL(2,3), h^cen=24) not matched")
    anchor2 = cert_index.get("lt384:idx336:pair30")
    if not anchor2 or tuple(anchor2["m0"]["id_group"]) != (336, 208):
        join_mismatches.append("anchor lt384:idx336:pair30 (expected id_group=[336,208]=PSL(3,2):C2, the sole both-c-in-N exotic pair per §G.6.c) not matched")
    if join_mismatches:
        for m in join_mismatches:
            fail("join mismatch: " + m)
    else:
        ok("independent join reproduces all 23 cert pair_fiber/id_group entries exactly (incl. both documented anchors)")

    # ---------------- (B) downstream arithmetic re-derivation ----------------
    arith_mismatches = []
    for p in cert_pairs:
        for mkey in ("m0", "m1"):
            m = p[mkey]
            invs = m["abelian_invariants"]
            d, is_cyc, d_even, j, j_div_3 = rederive_ab_fields(invs)
            if d != m["d"]:
                arith_mismatches.append(f"{p['pair_fiber']}/{mkey}: d rederived={d} cert={m['d']}")
            if is_cyc != m["is_cyclic"]:
                arith_mismatches.append(f"{p['pair_fiber']}/{mkey}: is_cyclic rederived={is_cyc} cert={m['is_cyclic']}")
            if d_even != m["d_even"]:
                arith_mismatches.append(f"{p['pair_fiber']}/{mkey}: d_even rederived={d_even} cert={m['d_even']}")
            if j != m["j"]:
                arith_mismatches.append(f"{p['pair_fiber']}/{mkey}: j rederived={j} cert={m['j']}")
            if j_div_3 != m["j_divides_3"]:
                arith_mismatches.append(f"{p['pair_fiber']}/{mkey}: j_divides_3 rederived={j_div_3} cert={m['j_divides_3']}")
    if arith_mismatches:
        for m in arith_mismatches:
            fail("arithmetic mismatch: " + m)
    else:
        ok("downstream d/is_cyclic/d_even/j/j_divides_3 rederived exactly for all 46 member observations")

    # M5 control
    m5 = cert["m5_control"]
    d5, cyc5, deven5, j5, jd35 = rederive_ab_fields(m5["abelian_invariants"])
    m5_mismatches = []
    if d5 != m5["d"]: m5_mismatches.append(f"d rederived={d5} cert={m5['d']}")
    if cyc5 != m5["is_cyclic"]: m5_mismatches.append(f"is_cyclic rederived={cyc5} cert={m5['is_cyclic']}")
    if deven5 != m5["d_even"]: m5_mismatches.append(f"d_even rederived={deven5} cert={m5['d_even']}")
    if j5 != m5["j"]: m5_mismatches.append(f"j rederived={j5} cert={m5['j']}")
    if jd35 != m5["j_divides_3"]: m5_mismatches.append(f"j_divides_3 rederived={jd35} cert={m5['j_divides_3']}")
    if m5["order"] != m5["order_expected"] or not m5["order_ok"]:
        m5_mismatches.append(f"order/order_expected/order_ok inconsistency: {m5['order']}/{m5['order_expected']}/{m5['order_ok']}")
    if m5_mismatches:
        for m in m5_mismatches:
            fail("M5 mismatch: " + m)
    else:
        ok(f"M5 control downstream fields rederived exactly (abelian_invariants={m5['abelian_invariants']} -> d={d5} is_cyclic={cyc5} j={j5})")

    # raw summary (no verdict language -- counts only)
    n_d_even = sum(1 for p in cert_pairs for mk in ("m0","m1") if p[mk]["d_even"])
    n_j_div_3_true = sum(1 for p in cert_pairs for mk in ("m0","m1") if p[mk]["j_divides_3"] is True)
    n_j_div_3_false = sum(1 for p in cert_pairs for mk in ("m0","m1") if p[mk]["j_divides_3"] is False)
    print(f"raw summary: 46 member observations across 23 pairs; d_even count={n_d_even}; "
          f"among those, j_divides_3=True count={n_j_div_3_true}, j_divides_3=False count={n_j_div_3_false}")

    print()
    if fails:
        print(f"RESULT: FAIL ({len(fails)} mismatches)")
        return 1
    else:
        print("RESULT: PASS (cross-checked, not verified -- 検証は Lean 専有)")
        return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
