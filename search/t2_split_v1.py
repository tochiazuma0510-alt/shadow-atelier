#!/usr/bin/env python3
"""
search/t2_split_v1.py -- T2-SPLIT (裁定778(1), per
docs/notes/cone_design_v1_addendum_e.md §4 追加発注 T2-SPLIT, 段 H-h).

For each dim P_k=2 weight k in {24,28,30,32}, reads d_K (the squarefree
part of disc(Z[T_2]), i.e. the Hecke field discriminant since 144169 was
independently confirmed prime and ==1 mod 4 in addendum E §1 -- reused
here from the already-committed, already-cross-checked T2-HECKE cert
search/certs/t2_hecke_v1_20260807.json's H_g_order_index.squarefree_part
field, NOT recomputed from scratch) and computes the Legendre symbol
(d_K/p) for the "echo prime" p at that weight (the smallest prime factor
of num(B_k), matching addendum E's stated crossing with the P-CONE-3
built-in-control primes and the P-CONE-5/6 echo primes):
    k=24: p=103   k=28: p=7   k=30: p=5   k=32: p=37 (the open target)

No verdict language -- raw Legendre symbol values only. The frozen
branch-reading (+1 = eigenform branch / -1 = scalar-looking branch) is
recorded as the design's own stated interpretation key, not asserted here
as a conclusion (発効は司令塔専権, addendum E's own explicit note).
"""
import json

T2_HECKE_CERT_PATH = "search/certs/t2_hecke_v1_20260807.json"

# (k, echo prime p) -- p = smallest prime factor of num(B_k), per
# docs/notes/cone_design_v1_addendum_b.md §1.3 and the CB-RECON/P-CONE-3/5/6
# already-committed work (search/certs/cb_recon_sweep_v1_20260807.json).
ECHO_PRIME = {24: 103, 28: 7, 30: 5, 32: 37}


def legendre_symbol(a, p):
    """Legendre symbol (a/p) via Euler's criterion, p an odd prime.
    Returns 1, -1, or 0 (if p | a)."""
    a_mod = a % p
    if a_mod == 0:
        return 0
    ls = pow(a_mod, (p - 1) // 2, p)
    return 1 if ls == 1 else -1


def factorize(n):
    n = abs(n)
    if n <= 1:
        return {}
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def main():
    t2 = json.load(open(T2_HECKE_CERT_PATH, encoding="utf-8"))
    order_index = t2["H_g_order_index"]

    per_k = {}
    for k in [24, 28, 30, 32]:
        d_K = order_index[str(k)]["squarefree_part"]
        p = ECHO_PRIME[k]
        ls = legendre_symbol(d_K, p)
        per_k[k] = {
            "d_K": d_K,
            "d_K_source": "search/certs/t2_hecke_v1_20260807.json H_g_order_index.squarefree_part (already-committed, already-cross-checked -- not recomputed here)",
            "d_K_factorization": {str(pr): e for pr, e in factorize(d_K).items()},
            "echo_prime": p,
            "legendre_symbol_dK_over_p": ls,
            "p_divides_d_K": (ls == 0),
        }
        print(f"k={k}: d_K={d_K} (factorization={per_k[k]['d_K_factorization']}) echo_prime={p} "
              f"(d_K/p)={ls}", flush=True)

    out = {
        "schema": "shadow-atelier/t2_split_v1",
        "authority": "裁定778(1) (司令塔), docs/notes/cone_design_v1_addendum_e.md §4 追加発注 T2-SPLIT 段H-h (verbatim)",
        "input_source_note": "d_K values are the squarefree_part field ALREADY COMPUTED and ALREADY "
                             "CROSS-CHECKED in search/certs/t2_hecke_v1_20260807.json (裁定769(3)/d4394df) "
                             "-- this script does not recompute the Hecke matrices or discriminants, only "
                             "the Legendre symbols.",
        "echo_prime_source_note": "echo primes (103,7,5,37) are the smallest prime factors of num(B_k) "
                                  "at each weight, matching the P-CONE-3 built-in-control primes "
                                  "(7@28, 5@30) and the P-CONE-5/6 echo primes (37@32, 103@24) already "
                                  "committed in search/certs/cb_recon_sweep_v1_20260807.json.",
        "per_k": {str(k): v for k, v in per_k.items()},
        "branch_reading_key_UNASSERTED": {
            "note": "addendum E §4's own stated interpretation key, recorded here as design context "
                    "ONLY -- this script does not assert which branch obtains; that judgment is "
                    "司令塔専権 (addendum E §3 (H3)/(H4) explicit limitation).",
            "legendre_plus_1": "(d_K/p)=+1 read by the design as 'eigenform branch' (p splits in the "
                               "Hecke field)",
            "legendre_minus_1": "(d_K/p)=-1 read by the design as 'scalar-looking branch' (p inert)",
        },
        "k32_p37_is_the_open_target": {
            "note": "addendum E §4 explicitly names (d_32/37) as 'the target of this measurement' "
                    "(未知=本測定の標的) -- reported as raw value below, no verdict attached.",
            "legendre_symbol": per_k[32]["legendre_symbol_dK_over_p"],
        },
        "no_verdict_note": "raw Legendre symbol values and factorizations only. No judgment words "
                           "('固有形式枝が実在', '共鳴' etc.) written anywhere in this cert -- 発効は司令塔専権.",
        "stop_code": None,
    }
    out_path = "search/certs/t2_split_v1_20260811.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
