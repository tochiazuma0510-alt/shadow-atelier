#!/usr/bin/env python3
"""parse_and_compare.py -- 便104認可事項1(GHA機能較正)の判定ロジック。

登録済み 13+5 fixture(sol/sol_reply_104_math31.md F104-1.4 が認可した
範囲そのもの):
  - 13: Lane V driver(search/probe/hsp7_cond4_laneV/driver_step4_evaluate_v3.g)
    の window-N judgments(8 dummy/h3 候補 + NW-P8 m-sweep 5 件)。
  - 5: Lane P p=5 control driver
    (search/probe/hsp7_cond4_laneP_p5control/driver_final_eval_p5.g)
    の NW-P7 main run(t=0..4)。

期待値は search/certs/hsp7_cond4_summary_v2_20260805.json(Lane Sigma v2、
4本の一次certを既にpath+digestでpinして集約した既存cert)から実行時に
読み取る -- コードに埋め込まない(F104-1.4 の要求どおり、実行後突合)。

このスクリプトは GAP の生 run.log をパースするだけで、GAP の判定ロジック
そのものには一切触れない(search/*.g は不可侵、Read するのみの既存駆動を
再利用)。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from receipt_schema import build_receipt, write_receipt  # noqa: E402

REPO_ROOT = HERE.parents[2]
SUMMARY_CERT_PATH = REPO_ROOT / "search" / "certs" / "hsp7_cond4_summary_v2_20260805.json"

RE_LANEV_CAND = re.compile(r"^N\s+candidate key_id=(\d+) f=(\S.*?)\s*:\s*\(3\.3\)=(true|false) \(3\.4\)=(true|false) verdict=(PASS|FAIL)\s*$")
RE_LANEV_MSWEEP = re.compile(r"^NW-P8 m=(\d+): N=(PASS|FAIL) N0=(PASS|FAIL) agree=(true|false)\s*$")
RE_P5CONTROL_MAIN = re.compile(r"^t=(\d+): f=jh4\^\d+ \(order-5 element in Q5\^\d+\), N_rho\(f\)=1 \? (true|false)\s*$")


def load_expected():
    summary = json.loads(SUMMARY_CERT_PATH.read_bytes())
    s8 = summary["s8prime_applied"]
    expected_13 = {}
    for row in s8["rows_8candidates"]:
        expected_13[f"cand_{row['key_id']}"] = row["verdictN"]
    for row in s8["rows_msweep"]:
        expected_13[f"msweep_m{row['m']}"] = row["verdictN"]
    if len(expected_13) != 13:
        raise SystemExit(f"expected_13 has {len(expected_13)} entries, want 13 -- summary cert layout changed?")

    pent_nwp7 = summary["laneP_pent_transcription"]["pent_NW_P7"]
    expected_5 = {}
    for row in pent_nwp7:
        expected_5[f"nwp7_t{row['t']}"] = "PASS" if row["N_rho_f_eq_1"] else "FAIL"
    if len(expected_5) != 5:
        raise SystemExit(f"expected_5 has {len(expected_5)} entries, want 5 -- summary cert layout changed?")
    return expected_13, expected_5, summary


def parse_lanev_log(text: str) -> dict:
    observed = {}
    for line in text.splitlines():
        m = RE_LANEV_CAND.match(line.strip())
        if m:
            key_id = int(m.group(1))
            observed[f"cand_{key_id}"] = m.group(5)
            continue
        m = RE_LANEV_MSWEEP.match(line.strip())
        if m:
            mval = int(m.group(1))
            observed[f"msweep_m{mval}"] = m.group(2)
    return observed


def parse_p5control_log(text: str) -> dict:
    observed = {}
    in_main_run = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("=== NW-P7 MAIN RUN"):
            in_main_run = True
            continue
        if in_main_run and line.startswith("==="):
            in_main_run = False
            continue
        if in_main_run:
            m = RE_P5CONTROL_MAIN.match(line)
            if m:
                t = int(m.group(1))
                observed[f"nwp7_t{t}"] = "PASS" if m.group(2) == "true" else "FAIL"
    return observed


def compare(expected: dict, observed: dict) -> list:
    rows = []
    for k in sorted(expected):
        exp = expected[k]
        obs = observed.get(k, "MISSING_FROM_LOG")
        rows.append({"candidate": k, "expected_verdict": exp, "observed_verdict": obs, "agree": exp == obs})
    extra = sorted(set(observed) - set(expected))
    if extra:
        rows.append({"candidate": f"UNEXPECTED_EXTRA_KEYS:{extra}", "expected_verdict": "n/a", "observed_verdict": "n/a", "agree": False})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True, choices=["laneV_13", "p5control_5"])
    ap.add_argument("--log", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--run-attempt", required=True)
    ap.add_argument("--commit-sha", required=True)
    ap.add_argument("--driver-digest", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    expected_13, expected_5, summary = load_expected()
    log_text = Path(args.log).read_text(encoding="utf-8", errors="replace")

    if args.lane == "laneV_13":
        expected = expected_13
        observed = parse_lanev_log(log_text)
    else:
        expected = expected_5
        observed = parse_p5control_log(log_text)

    rows = compare(expected, observed)
    summary_bytes = SUMMARY_CERT_PATH.read_bytes()
    import hashlib

    receipt = build_receipt(
        lane=args.lane,
        run_id=args.run_id,
        run_attempt=args.run_attempt,
        commit_sha=args.commit_sha,
        driver_digest=args.driver_digest,
        fixture_source_cert_path=str(SUMMARY_CERT_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        fixture_source_cert_sha256=hashlib.sha256(summary_bytes).hexdigest(),
        candidates=rows,
    )
    write_receipt(receipt, Path(args.out))
    print(json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True))

    if len(rows) != len(expected):
        print(f"::error::row count {len(rows)} != expected count {len(expected)}", file=sys.stderr)
        return 1
    if not receipt["overall_pass"]:
        print("::error::one or more candidates disagreed with the registered expected verdict", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
