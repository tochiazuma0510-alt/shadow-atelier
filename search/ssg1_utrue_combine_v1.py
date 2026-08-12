"""SSG1-GAP-1 / Sol 122 B4-B5 sec.4.3 -- U_true cert assembly.

Combines the symbolic rail (search/ssg1_utrue_symbolic_v1.py) and the
literal rail (search/ssg1_utrue_literal_v1.py) into
search/certs/ssg1_utrue_cert_v1_20260813.json.

Also recomputes the sha256 of the SOL122_SCRIPT block quoted in
sol/sol_reply_122_r1_line3.md sec.6 (marker lines excluded, UTF-8/LF) so
the cert records whether the read-only reference script's provenance
matches Sol's own claimed digest.  This module does not import or execute
that script; it only hashes the quoted text found in the .md file.

Raw output only -- no verdict language (per task instruction: cert is
values only, no PASS/FAIL wording).
"""
import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SOL_REPLY_MD = REPO_ROOT / "sol" / "sol_reply_122_r1_line3.md"
BEGIN_MARK = "# BEGIN SOL122_SCRIPT"
END_MARK = "# END SOL122_SCRIPT"
SOL_CLAIMED_SCRIPT_SHA256 = "b9af7473fa825bcb81e4ba8eb2319e7a3177393a735934ebe674d575907c5be4"
KNOWN_LOWER_BOUND_A_NPRIME = 30360  # cyclotomic lower bound |a_{N'}| (docs/notes/ss_gap1_count_spec_v1.md CP-D)
KNOWN_CHECKPOINT_THRESHOLD = KNOWN_LOWER_BOUND_A_NPRIME / 2  # CP-D: U >= 30360/2 = 15180


def extract_sol_script_sha256() -> dict:
    text = SOL_REPLY_MD.read_text(encoding="utf-8")
    begin_i = text.index(BEGIN_MARK)
    end_i = text.index(END_MARK)
    # slice strictly between the two marker lines
    after_begin = text.index("\n", begin_i) + 1
    body = text[after_begin:end_i]
    body_lf = body.replace("\r\n", "\n")
    digest = hashlib.sha256(body_lf.encode("utf-8")).hexdigest()
    return {
        "recomputed_sha256": digest,
        "sol_claimed_sha256": SOL_CLAIMED_SCRIPT_SHA256,
        "matches_sol_claim": digest == SOL_CLAIMED_SCRIPT_SHA256,
    }


def run_json_script(script: str, args: list) -> dict:
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "search" / script)] + args,
        capture_output=True, text=True, check=True,
    )
    return json.loads(proc.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=691)
    ap.add_argument("--p-literal", type=int, default=7)
    ap.add_argument("--out", type=str,
                     default=str(REPO_ROOT / "search" / "certs" / "ssg1_utrue_cert_v1_20260813.json"))
    args = ap.parse_args()

    symbolic = run_json_script("ssg1_utrue_symbolic_v1.py", ["--p", str(args.p)])
    literal = run_json_script("ssg1_utrue_literal_v1.py", ["--p", str(args.p_literal)])
    sol_script = extract_sol_script_sha256()

    U_true_floor = symbolic["U_true"]["floor"]
    cert = {
        "schema": "ssg1-utrue-cert/v1",
        "generated_by": "search/ssg1_utrue_combine_v1.py",
        "task": "sol reply 122 sec 4.3 3-point plan / 裁定1109 task A",
        "definition": {
            "H_tilde": "{(A,s) in SL^pm(2,Z/p^2) x S3 : det(A)=sgn(s)}",
            "R": "Z/p^2",
        },
        "symbolic_rail": symbolic,
        "literal_rail": literal,
        "sol_reference_script": {
            "source_file": "sol/sol_reply_122_r1_line3.md",
            "note": "read for reference; ssg1_utrue_literal_v1.py is an independent fresh implementation, not copied from this script",
            **sol_script,
        },
        "known_lower_bound": {
            "a_Nprime_cyclotomic_lower_bound": KNOWN_LOWER_BOUND_A_NPRIME,
            "checkpoint_threshold_CP_D": KNOWN_CHECKPOINT_THRESHOLD,
            "source": "docs/notes/ss_gap1_count_spec_v1.md CP-D",
            "U_true_floor": U_true_floor,
            "U_true_floor_ge_checkpoint_threshold": U_true_floor >= KNOWN_CHECKPOINT_THRESHOLD,
            "U_true_floor_lt_2e6": U_true_floor < 2_000_000,
            "U_true_floor_lt_1e7": U_true_floor < 10_000_000,
        },
    }

    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(cert, indent=2, sort_keys=True)
    out_path.write_text(text + "\n", encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
