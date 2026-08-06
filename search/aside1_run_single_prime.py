#!/usr/bin/env python3
"""
search/aside1_run_single_prime.py -- ASIDE-1 measurement (裁定699 part2),
per docs/notes/aside_measurement_design_v1.md SS5 実測指示書 ASIDE-1
(verbatim, 数学者起草). Reads/imports the existing edim_semidirect_v1.py
GradedLie machinery UNCHANGED (no modification to any frozen ceremony
script) -- this is a NEW, standalone script.

Usage: python search/aside1_run_single_prime.py <prime>

What this computes (per the design doc, all at a single prime p):
  Stage A: for m in [3,5,7,9], retrieve the ACTUAL basis vector sigma_m of
    S_m (dim 1, asserted -- canary a / S-AS-1), normalized (leading nonzero
    Lyndon-coordinate scaled to 1). This reuses compute_H_S_at_k_safe's own
    H_basis construction (Q-image or nullspace fallback, identical logic,
    copied here since the frozen ceremony script only returns the
    DIMENSION, not the basis) plus a NEW nu.j-restricted-to-H nullspace
    step to isolate S_m's 1-dimensional subspace explicitly.
  Stage B: A12 := rank_Fp({[sigma_3,sigma_9], [sigma_5,sigma_7]}), computed
    as the FREE LIE bracket in L_12(X,Y) (h_alg's own ambient/Lyndon
    space). NOTE ON THE MODEL: per t_bracket_ambient's own source (verified
    by inspection, not assumed) -- for two elements embedded into t=n⋊h as
    (0,h1),(0,h2) (zero n-component, matching j's literal embedding
    h->(0,h)), the resulting bracket is EXACTLY (0,[h1,h2]) with n-part
    identically zero (word_bracket(n1,n2)={} since n1=n2={}, and
    delta_hexpr_on_nambient of the ZERO n-vector is zero by linearity).
    So "weight-graded A12 computed in t_12 (dim 44,555)" is mathematically
    IDENTICAL in value to the plain free-Lie bracket computed directly in
    h_alg's L_12(X,Y) (dim = h_alg.dim[12], much smaller) -- this fact is
    used to AVOID building the 44,555-dim n_alg/t apparatus at all (a
    verified simplification, not a shortcut taken on faith).
  Stage C: A12_depth2 := rank_Fp of the DEPTH-2 (Y-degree=2) homogeneous
    PROJECTION of the same two brackets, computed in the SAME L_12(X,Y)
    space (depth = count of the index-1 (Y) letter in each ambient word --
    confirmed convention: edim_semidirect_v1.py line ~1048 comment "X then
    Y, matches h basis order").
  Stage D: sigma_m's depth-1 leading term proportionality check against
    ad(X)^(m-1)(Y) (BH cross-check, second system, per the note).

NO verdict language is emitted anywhere (S-AS-5): only raw values,
RAW_FACT-style booleans for canaries, and the pre-registered STOP codes.
"""
import json
import sys
import time

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed
import numpy as np

KMAX = 9  # h_alg is only needed at degrees <=9 (sigma_m for m in {3,5,7,9}):
# the degree-12 bracket products [sigma3,sigma9],[sigma5,sigma7] are formed
# directly as ambient (tensor-algebra) word-vectors via word_bracket, which
# needs NO degree-12 Lyndon basis/solver construction at all (word-tuple
# concatenation is exact regardless of the Lyndon basis at that degree; the
# free-Lie -> tensor-algebra embedding being injective, per
# rank_nu_j_on_subspace_ambient's own docstring, is exactly what licenses
# computing rank directly on the ambient word-vectors below, with no need
# to convert to Lyndon coordinates at degree 12 either). This avoids ever
# building h_alg's (comparatively expensive) degree-10/11/12 Lyndon
# machinery, matching the E-DIM12/691 ceremony's own experience that
# degree-12 construction was heavy enough to warrant a 16GB GHA runner.
SIGMA_DEGREES = [3, 5, 7, 9]
BRACKET_PAIRS = [(3, 9), (5, 7)]


def h_basis_at_k(k, h_alg, p):
    """EXACT copy of compute_H_S_at_k_safe's H_basis construction (dim +
    basis columns), from search/edim_run_c9_c10_v3_single_prime.py --
    reproduced here because the frozen ceremony script only returns
    H_dim, not the basis itself, and that script is NOT modified (freeze
    discipline). p is assumed coprime to 6 (true for all 5 dispatch
    primes here: 2147483647, 998244353, 691, 677, 701)."""
    dim_h = h_alg.dim[k]
    theta = np.array(ed.build_theta_tau_matrix(k, h_alg, 'theta', p), dtype=np.int64) % p
    tau = np.array(ed.build_theta_tau_matrix(k, h_alg, 'tau', p), dtype=np.int64) % p
    I_h = np.eye(dim_h, dtype=np.int64)
    one_plus_theta = (I_h + theta) % p
    tau2 = ed.mat_mul_modp_np_safe(tau, tau, p)
    one_plus_tau_tau2 = (I_h + tau + tau2) % p
    H_stack = np.concatenate([one_plus_theta, one_plus_tau_tau2], axis=0)
    H_dim = dim_h - ed.rank_modp_np(H_stack, p)
    if p % 2 and p % 3:
        Q = ed.mat_mul_modp_np_safe((I_h - theta) % p, (I_h - tau) % p, p)
        H_basis = ed.sparse_column_space_basis_modp_np(Q, p)
        if H_basis.shape[1] != H_dim:
            raise ValueError(f"H_basis dim {H_basis.shape[1]} != H_dim {H_dim} at k={k}")
    else:
        H_basis = ed.nullspace_modp_np(H_stack, p)
        if H_basis.shape[1] != H_dim:
            raise ValueError("nullspace dimension/rank mismatch")
    return H_dim, H_basis


def nu_j_restricted_vectors(k, h_alg, H_basis, p):
    """Adapted from ed.rank_nu_j_on_subspace_ambient: returns the list of
    sparse (tag,word)->coeff dicts (one per H_basis column) INSTEAD OF
    just their rank, so the nullspace (= S_m's coordinates within H_basis)
    can be extracted explicitly. Logic is otherwise IDENTICAL (same state
    cache, same eval_tree_in_t_ambient calls) -- copied, not modified in
    place, to avoid touching the frozen module."""
    subspace_basis = np.asarray(H_basis, dtype=np.int64) % p
    dim_h = h_alg.dim[k]
    subspace_dim = subspace_basis.shape[1]
    if subspace_dim == 0:
        return []
    state = getattr(h_alg, "_nu_ambient_state", None)
    if state is None or state["p"] != p:
        state = {
            "p": p,
            "leaf_images": ed._rho_power_h_leaf_images_ambient(p),
            "tree_caches": [dict() for _ in range(5)],
            "base_table": ed._delta_base_table(p),
        }
        h_alg._nu_ambient_state = state

    restricted = [dict() for _ in range(subspace_dim)]
    for basis_index, tree in enumerate(h_alg.trees[k]):
        coefficients = subspace_basis[basis_index, :]
        nonzero_columns = np.nonzero(coefficients)[0]
        if len(nonzero_columns) == 0:
            continue
        nu_n = {}
        nu_h = {}
        for power in range(5):
            action_cache = {}
            n_part, h_part, h_expr, degree = ed.eval_tree_in_t_ambient(
                tree, state["leaf_images"][power], p,
                cache=state["tree_caches"][power], base_table=state["base_table"],
                action_cache=action_cache, cache_result=False)
            if degree != k:
                raise ValueError("ambient rho evaluation returned wrong degree")
            nu_n = ed.word_add([nu_n, n_part], p)
            nu_h = ed.word_add([nu_h, h_part], p)
        for column in nonzero_columns:
            scalar = int(coefficients[column])
            target = restricted[int(column)]
            for word, value in nu_n.items():
                key = (0,) + word
                new_value = (target.get(key, 0) + scalar * value) % p
                if new_value:
                    target[key] = new_value
                else:
                    target.pop(key, None)
            for word, value in nu_h.items():
                key = (1,) + word
                new_value = (target.get(key, 0) + scalar * value) % p
                if new_value:
                    target[key] = new_value
                else:
                    target.pop(key, None)
    return restricted


def sigma_m_ambient(m, h_alg, p):
    """Returns (H_dim, S_dim, sigma_ambient_dict_or_None, leading_word)."""
    H_dim, H_basis = h_basis_at_k(m, h_alg, p)
    restricted = nu_j_restricted_vectors(m, h_alg, H_basis, p)
    if H_dim == 0:
        return H_dim, 0, None, None
    # build dense matrix: rows = union of all (tag,word) keys, cols = H_dim
    all_keys = sorted(set().union(*[set(v.keys()) for v in restricted])) if restricted else []
    key_index = {k_: i for i, k_ in enumerate(all_keys)}
    M = np.zeros((len(all_keys), H_dim), dtype=np.int64)
    for col, vec in enumerate(restricted):
        for k_, val in vec.items():
            M[key_index[k_], col] = val % p
    S_basis_in_H = ed.nullspace_modp_np(M, p) if M.shape[0] else np.eye(H_dim, dtype=np.int64)
    S_dim = S_basis_in_H.shape[1]
    if S_dim != 1:
        return H_dim, S_dim, None, None
    # S_m vector in h_alg Lyndon coordinates at degree m: H_basis @ coeffs
    coeffs = S_basis_in_H[:, 0] % p
    coords = (H_basis.astype(np.int64) @ coeffs.astype(np.int64)) % p
    coords = [int(x) for x in coords]
    # normalize: scale so the first nonzero Lyndon coordinate is 1
    lead_idx = next((i for i, c in enumerate(coords) if c % p), None)
    if lead_idx is None:
        return H_dim, S_dim, None, None
    inv = ed.modinv(coords[lead_idx], p)
    coords_norm = [(c * inv) % p for c in coords]
    ambient = h_alg.coords_to_ambient(m, coords_norm)
    lead_word = h_alg.words[m][lead_idx]
    return H_dim, S_dim, ambient, lead_word


def depth(word):
    """Y-degree of an ambient associative word (tuple of 0/1 letters),
    letter index 1 = Y (confirmed convention, see module docstring)."""
    return sum(1 for letter in word if letter == 1)


def project_depth(vec, target_depth):
    return {w: c for w, c in vec.items() if depth(w) == target_depth}


def rank_of_two_ambient_vectors(v1, v2, p):
    """Rank (0,1,2) of the span of two sparse ambient vectors -- cheap
    direct method (no full coordinate solve needed for just 2 vectors):
    build the tiny dense matrix over the union of their nonzero keys and
    rank it mod p."""
    keys = sorted(set(v1.keys()) | set(v2.keys()))
    if not keys:
        return 0
    M = np.zeros((len(keys), 2), dtype=np.int64)
    for i, k_ in enumerate(keys):
        M[i, 0] = v1.get(k_, 0) % p
        M[i, 1] = v2.get(k_, 0) % p
    return int(ed.rank_modp_np(M, p))


def ad_X_pow_Y(power, p):
    """ad(X)^power (Y) as an ambient vector: repeated left-bracket by X.
    letter 0 = X, letter 1 = Y (see module docstring)."""
    vec = {(1,): 1 % p}
    for _ in range(power):
        vec = ed.word_bracket({(0,): 1 % p}, vec, p)
    return vec


def proportional(v1, v2, p):
    """True iff v1,v2 span a space of rank <= 1 (proportional or one/both
    zero)."""
    return rank_of_two_ambient_vectors(v1, v2, p) <= 1


def main():
    if len(sys.argv) != 2:
        print("usage: aside1_run_single_prime.py <prime>", file=sys.stderr)
        sys.exit(2)
    p = int(sys.argv[1])

    t_start = time.time()
    print(f"=== ASIDE-1: JOB START prime={p} ===", flush=True)

    t0 = time.time()
    h_alg = ed.GradedLie(2, KMAX, p, sparse_degrees=set(range(1, KMAX + 1)))
    build_elapsed = time.time() - t0
    print(f"p={p}: h_alg built, elapsed={build_elapsed:.1f}s", flush=True)

    stop_code = None
    sigmas = {}
    stage_a = {}
    for m in SIGMA_DEGREES:
        H_dim, S_dim, ambient, lead_word = sigma_m_ambient(m, h_alg, p)
        stage_a[m] = {"H_dim": H_dim, "S_dim": S_dim, "sigma_norm_ok": (S_dim == 1 and ambient is not None),
                      "lead_word": list(lead_word) if lead_word is not None else None,
                      "num_ambient_terms": (len(ambient) if ambient is not None else None)}
        print(f"p={p} stage A m={m}: H_dim={H_dim} S_dim={S_dim} sigma_ok={stage_a[m]['sigma_norm_ok']}", flush=True)
        if S_dim != 1:
            stop_code = "SIGMA_NONUNIQUE"
            print(f"p={p} m={m}: S_dim={S_dim} != 1 -- SIGMA_NONUNIQUE / STOP (S-AS-1)", flush=True)
            break
        sigmas[m] = ambient

    out = {
        "schema": "shadow-atelier/aside1/v1",
        "authority": "裁定699 (司令塔), ASIDE-1 per docs/notes/aside_measurement_design_v1.md SS5 実測指示書 (verbatim, 数学者起草)",
        "prime": p,
        "stage_A_sigma": stage_a,
        "no_verdict_note": "S-AS-5 compliance: this script emits ONLY raw numeric values and the pre-registered STOP codes below (SIGMA_NONUNIQUE / CALIBRATION_FAIL / CONGRUENCE_NOT_REPRODUCED / IMPOSSIBLE_CELL) -- no interpretive verdict prose of the 4 forbidden kinds listed in docs/notes/aside_measurement_design_v1.md S7 (S-AS-5) is written anywhere in this cert.",
    }

    if stop_code is None:
        # Stage B: weight-graded A12 (see module docstring for the verified
        # t-model-reduction fact -- computed directly in h_alg, no n_alg
        # needed).
        v_39 = ed.word_bracket(sigmas[3], sigmas[9], p)
        v_57 = ed.word_bracket(sigmas[5], sigmas[7], p)
        A12 = rank_of_two_ambient_vectors(v_39, v_57, p)
        print(f"p={p} stage B: A12={A12}", flush=True)

        # Stage C: depth-2 projection of the SAME brackets, using the
        # depth-1 leading terms f_m := ad(X)^(m-1)(Y) as specified (the
        # note computes d2 from f_3,f_9 / f_5,f_7's depth-2 bracket
        # component, i.e. bracket the DEPTH-1 LEADING TERMS, then take
        # the resulting bracket's depth-2 part -- note f_m itself has
        # depth 1, so [f_m,f_m'] naturally has depth <= 2, and its depth-2
        # part is what's compared to the Ihara-Takao congruence).
        f = {m: ad_X_pow_Y(m - 1, p) for m in SIGMA_DEGREES}
        ihara_39 = ed.word_bracket(f[3], f[9], p)
        ihara_57 = ed.word_bracket(f[5], f[7], p)
        d2_39 = project_depth(ihara_39, 2)
        d2_57 = project_depth(ihara_57, 2)
        A12_depth2 = rank_of_two_ambient_vectors(d2_39, d2_57, p)
        print(f"p={p} stage C: A12_depth2={A12_depth2}", flush=True)

        # Stage D: BH cross-check -- sigma_m's depth-1 leading term
        # proportional to ad(X)^(m-1)(Y)?
        stage_d = {}
        for m in SIGMA_DEGREES:
            sigma_depth1 = project_depth(sigmas[m], 1)
            prop = proportional(sigma_depth1, f[m], p)
            stage_d[m] = {"proportional_to_adXpow_Y": prop}
        print(f"p={p} stage D: {stage_d}", flush=True)

        out["stage_B_model_weight_graded"] = {
            "bracket_39_num_terms": len(v_39), "bracket_57_num_terms": len(v_57),
            "A12": A12,
        }
        out["stage_C_free_lie_depth_graded"] = {
            "f_leading_terms_computed": list(SIGMA_DEGREES),
            "d2_39_num_terms": len(d2_39), "d2_57_num_terms": len(d2_57),
            "A12_depth2": A12_depth2,
        }
        out["stage_D_bh_crosscheck"] = stage_d

        # canary/stop evaluation (raw booleans only, no verdict text)
        is_general_prime = p not in (691,)
        canary_b_ok = None
        canary_c_ok = None
        if is_general_prime:
            canary_b_ok = (A12 == 2 and A12_depth2 == 2)
            if not canary_b_ok:
                stop_code = "CALIBRATION_FAIL"
        else:
            canary_c_ok = (A12_depth2 == 1)
            if not canary_c_ok:
                stop_code = "CONGRUENCE_NOT_REPRODUCED"
        if A12 > 2:  # S12 not measured here; this is a basic sanity bound (A12<=dim{v1,v2}<=2)
            stop_code = "IMPOSSIBLE_CELL"

        out["canary_b_general_prime_A12_2_and_depth2_2"] = canary_b_ok
        out["canary_c_691_depth2_eq_1"] = canary_c_ok
    else:
        out["stop_code"] = stop_code

    total_elapsed = time.time() - t_start
    out["stop_code"] = stop_code
    out["total_elapsed_sec"] = round(total_elapsed, 2)

    out_path = f"search/certs/aside1_prime_{p}_v1_20260806.json"
    with open(out_path, "w", encoding="utf-8") as f_out:
        json.dump(out, f_out, indent=2, ensure_ascii=False)

    print(f"=== ASIDE-1: JOB END prime={p} total_elapsed_sec={out['total_elapsed_sec']} stop_code={stop_code} ===", flush=True)
    print(f"Wrote {out_path}", flush=True)
    if stop_code is not None:
        print("ASIDE1_STOP", flush=True)
        sys.exit(1)
    print("ASIDE1_DONE", flush=True)


if __name__ == "__main__":
    main()
