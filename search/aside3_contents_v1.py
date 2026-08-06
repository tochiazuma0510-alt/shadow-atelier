#!/usr/bin/env python3
"""
search/aside3_contents_v1.py -- R-1 (裁定721・軽量companion), 目的:
定理D-5の仮定(H2)の例外素数集合を明示有限集合化するため、aside3の中間
データ(厳密有理のsigma_3,sigma_5,sigma_7,sigma_9とv1={sigma_3,sigma_9},
v2={sigma_5,sigma_7})の content(分母の素因数分解込み)を読み出す。

新規計算ゼロ: search/aside3_exact_D_v1.py が既に検証済みのCRT+有理数
再構成パイプライン(reconstruct_ambient_dict/content_of/factorize_small/
q_ihara_bracket/RECON_PRIMES)をそのままimportして再利用するだけで、
新しい数式・新しいロジックは一切追加しない。aside3本体はD=v1-3*v2の
"深さ別"contentのみを報告したが、本スクリプトはv1,v2そのもの、および
sigma_m自体(各m全体、深さ別ではない)の"全体"contentを読み出す点だけが
新しい観測(観測対象の違いであって計算方式の違いではない)。

出力: search/certs/aside3_contents_v1_20260806.json
M := 6 個の content の分母に現れる素因数の合併集合(2,3以外があれば
それが新規の例外素数候補)。

No verdict language (S-AS-5): raw factorizations only.
"""
import json
import sys
import time

sys.path.insert(0, "search")
import edim_semidirect_v1 as ed
import aside1_run_single_prime as a1
import aside3_exact_D_v1 as a3


def main():
    t_start = time.time()
    print("=== ASIDE-3 companion (R-1): content readout for sigma_m, v1, v2 ===", flush=True)

    per_prime_sigma = {m: {} for m in a1.SIGMA_DEGREES}
    lead_words = {m: None for m in a1.SIGMA_DEGREES}
    lead_word_mismatch = {}
    dims = {m: None for m in a1.SIGMA_DEGREES}
    for p in a3.RECON_PRIMES:
        t0 = time.time()
        h_alg = ed.GradedLie(2, a1.KMAX, p, sparse_degrees=set(range(1, a1.KMAX + 1)))
        for m in a1.SIGMA_DEGREES:
            H_dim, S_dim, ambient, lead_word = a1.sigma_m_ambient(m, h_alg, p)
            if S_dim != 1:
                out = {"schema": "shadow-atelier/aside3_contents/v1", "stop_code": "SIGMA_NONUNIQUE",
                       "stop_detail": {"prime": p, "m": m, "S_dim": S_dim}}
                json.dump(out, open("search/certs/aside3_contents_v1_20260806.json", "w", encoding="utf-8"),
                          indent=2, ensure_ascii=False)
                print("ASIDE3_CONTENTS_STOP", flush=True)
                sys.exit(1)
            per_prime_sigma[m][p] = ambient
            if dims[m] is None:
                dims[m] = (H_dim, S_dim)
            if lead_words[m] is None:
                lead_words[m] = lead_word
            elif tuple(lead_word) != tuple(lead_words[m]):
                lead_word_mismatch[m] = lead_word_mismatch.get(m, []) + [(p, lead_word)]
        print(f"prime={p}: sigma_m realized, elapsed={time.time()-t0:.1f}s", flush=True)

    if lead_word_mismatch:
        out = {"schema": "shadow-atelier/aside3_contents/v1", "stop_code": "LEAD_WORD_MISMATCH",
               "stop_detail": {str(k): v for k, v in lead_word_mismatch.items()}}
        json.dump(out, open("search/certs/aside3_contents_v1_20260806.json", "w", encoding="utf-8"),
                  indent=2, ensure_ascii=False)
        print("ASIDE3_CONTENTS_STOP", flush=True)
        sys.exit(1)

    sigma_Q = {}
    for m in a1.SIGMA_DEGREES:
        try:
            sigma_Q[m] = a3.reconstruct_ambient_dict(per_prime_sigma[m])
        except ValueError as exc:
            out = {"schema": "shadow-atelier/aside3_contents/v1", "stop_code": "RECONSTRUCTION_FAIL",
                   "stop_detail": {"m": m, "error": str(exc)}}
            json.dump(out, open("search/certs/aside3_contents_v1_20260806.json", "w", encoding="utf-8"),
                      indent=2, ensure_ascii=False)
            print("ASIDE3_CONTENTS_STOP", flush=True)
            sys.exit(1)
        print(f"sigma_{m}^Q reconstructed: {len(sigma_Q[m])} terms", flush=True)

    v1_Q = a3.q_ihara_bracket(sigma_Q[3], sigma_Q[9])
    v2_Q = a3.q_ihara_bracket(sigma_Q[5], sigma_Q[7])
    print(f"v1_Q={len(v1_Q)} terms, v2_Q={len(v2_Q)} terms", flush=True)

    objects = {
        "sigma_3": sigma_Q[3], "sigma_5": sigma_Q[5],
        "sigma_7": sigma_Q[7], "sigma_9": sigma_Q[9],
        "v1_ihara_sigma3_sigma9": v1_Q, "v2_ihara_sigma5_sigma7": v2_Q,
    }

    content_report = {}
    exceptional_primes = set()
    for name, vec in objects.items():
        c = a3.content_of(vec)
        num_fact = a3.factorize_small(c.numerator)
        den_fact = a3.factorize_small(c.denominator)
        content_report[name] = {
            "num_terms": len(vec),
            "content_numerator": c.numerator,
            "content_denominator": c.denominator,
            "content_numerator_factorization": {str(k): v for k, v in num_fact.items()},
            "content_denominator_factorization": {str(k): v for k, v in den_fact.items()},
        }
        exceptional_primes |= set(num_fact.keys()) | set(den_fact.keys())
        print(f"content({name}) = {c} num_fact={num_fact} den_fact={den_fact}", flush=True)

    M_exceptional_primes = sorted(exceptional_primes)
    M_value = 1
    for q in M_exceptional_primes:
        M_value *= q
    print(f"M (union of all prime factors appearing in these 6 contents) = {M_exceptional_primes}, "
          f"M_value={M_value}", flush=True)

    out = {
        "schema": "shadow-atelier/aside3_contents/v1",
        "authority": "裁定721 (司令塔), R-1 -- companion readout of search/aside3_exact_D_v1.py's "
                      "already-computed reconstruction (no new computation logic; same "
                      "RECON_PRIMES/reconstruct_ambient_dict/content_of/q_ihara_bracket, applied to "
                      "sigma_m and v1/v2 as WHOLE vectors rather than D's per-depth projections)",
        "purpose": "定理D-5の仮定(H2)の例外素数集合(q not dividing 6M)のMを明示有限集合化するための"
                   "生値読み出し(判定語なし)",
        "reconstruction_primes": a3.RECON_PRIMES,
        "sigma_dims": {str(m): {"H_dim": dims[m][0], "S_dim": dims[m][1]} for m in a1.SIGMA_DEGREES},
        "lead_words": {str(m): list(lead_words[m]) for m in a1.SIGMA_DEGREES},
        "content_report": content_report,
        "M_exceptional_primes": M_exceptional_primes,
        "M_value": M_value,
        "note": "M_exceptional_primes は、この6個の content (numerator+denominator) に現れた"
                "素因数の合併集合の生値。定理D-5(H2)の「q not | 6M」の解釈・適用は数学者/司令塔の専権。",
        "no_verdict_note": "S-AS-5 compliance: raw factorizations only, no interpretive verdict prose.",
        "stop_code": None,
        "total_elapsed_sec": round(time.time() - t_start, 2),
    }
    out_path = "search/certs/aside3_contents_v1_20260806.json"
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}", flush=True)
    print(f"=== JOB END total_elapsed_sec={out['total_elapsed_sec']} ===", flush=True)
    print("ASIDE3_CONTENTS_DONE", flush=True)


if __name__ == "__main__":
    main()
