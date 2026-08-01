#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/gen_ep_freeze_receipt_sol99.py

Generator for the COMMANDER FREEZE RECEIPT that binds the exact trio

    spec      mb/ninfty-stage2-predicate/v20
    contract  mb/ninfty-verifier-contract/v15
    manifest  mb/dependency-manifest/v15

plus the self-audit script bundle-selfaudit/v11, following the receipt
convention established by provenance/ninfty_freeze_receipt_sol75.md
(裁定111) -- a JSON control-plane artifact plus a human-readable provenance
rendering, both produced from the SAME machine-computed values.

AUTHORISATION: Sol 便99 §5 F99-5.2 (`sol_freeze_gate = PASS`), 裁定412.
This script issues nothing by itself: it recomputes every digest from the
repository files, mechanically re-extracts the digests Sol's reply declares,
and REFUSES to emit anything if the two sets disagree (fail-closed -- a
receipt whose bound digests were typed by hand is exactly the defect the
receipt exists to prevent, 便98 F98-6.1 / RC-1).

WHAT THE RECEIPT DOES *NOT* AUTHORISE is written into the artifact itself
(Sol 便99 F99-5.2, verbatim exclusion list): W6_CLOSED=true, IMAGE-MU=PASS,
EP detector activation/mint, positive-control event, candidate acceptance or
Freeze 2 unlocking. None of these may be derived from this freeze PASS.

Usage:
    python search/gen_ep_freeze_receipt_sol99.py [--check]

`--check` re-derives everything and diffs against the artifacts on disk
without writing (used by the suite so that a hand-edited receipt is caught).
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

SOL_REPLY = "sol/sol_reply_99_math26.md"

RECEIPT_ID = "mb/ninfty-stage2-freeze-receipt/sol99/92025385-8f26416b-72623050"
FREEZE_ID = "mb/ninfty-stage2-freeze/92025385-8f26416b-72623050"

# (receipt field prefix, artifact id, repository path)
BOUND = [
    ("predicate_spec", "mb/ninfty-stage2-predicate/v20", "docs/week4-NInfty_stage2_spec_v20.md"),
    ("verifier_contract", "mb/ninfty-verifier-contract/v15", "docs/mb_ninfty_verifier_contract_v15.md"),
    ("dependency_manifest_schema", "mb/dependency-manifest/v15", "docs/mb_dependency_manifest_v15.md"),
    ("selfaudit", "bundle-selfaudit/v11", "search/bundle-selfaudit-v11.py"),
]

# The predecessors that stay byte-frozen as history (F99-5.2: "凍結済み
# predecessor v19/v14/v14 は byte 不変のまま残り、新 trio は上書きでなく
# v20/v15/v15 の追加 plane である").
PREDECESSORS = [
    ("mb/ninfty-stage2-predicate/v19", "docs/week4-NInfty_stage2_spec_v19.md"),
    ("mb/ninfty-verifier-contract/v14", "docs/mb_ninfty_verifier_contract_v14.md"),
    ("mb/dependency-manifest/v14", "docs/mb_dependency_manifest_v14.md"),
]

JSON_OUT = "search/certs/ep_freeze_receipt_sol99_20260802.json"
MD_OUT = "provenance/ninfty_freeze_receipt_sol99.md"

# The two ERA_W6KEY planes declared by spec v20 sec.5.3.4 (M-7: declared
# first, adopted afterwards; PENDING_ADOPTION until a freeze receipt binds
# this trio, and PENDING_ADOPTION counts as neither PASS nor FAIL).
W6KEY_PLANES = {
    "w6_point_map_producer": [
        "search/ninfty-w6-pointmap-lanea.mjs",
        "search/ninfty-w6-pointmap-laneb.py",
    ],
    "w6_key_route": [
        "search/ninfty-w6-key-gate-r1p.py",
        "search/ninfty-w6-key-gate-r2p.py",
    ],
}

NOT_AUTHORISED = [
    "W6_CLOSED=true",
    "IMAGE-MU=PASS",
    "EP detector activation / mint",
    "positive-control event",
    "candidate acceptance or Freeze 2 unlocking",
]


def sha256_file(rel):
    with open(os.path.join(REPO, *rel.split("/")), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def sol_declared_digests():
    """Mechanically re-extract the digest block from Sol's reply. Nothing in
    this file is transcribed by hand; if the reply's wording changes so that
    the block no longer parses, the generator fails closed."""
    with open(os.path.join(REPO, *SOL_REPLY.split("/")), "rb") as f:
        text = f.read().decode("utf-8")
    out = {}
    for key in ("predicate_spec_digest", "verifier_contract_digest",
                "dependency_manifest_schema_digest", "selfaudit_digest"):
        m = re.search(re.escape(key) + r"\s*=\s*\n?\s*([0-9a-f]{64})", text)
        if m is None:
            raise SystemExit(f"FAIL-CLOSED: {SOL_REPLY} carries no parseable {key}")
        out[key] = m.group(1)
    for key, want in (("predicate_spec_freeze_id", FREEZE_ID),):
        m = re.search(re.escape(key) + r"\s*=\s*\n?\s*\"([^\"]+)\"", text)
        if m is None or m.group(1) != want:
            raise SystemExit(f"FAIL-CLOSED: {SOL_REPLY} {key} is {m and m.group(1)!r}, expected {want!r}")
    if not re.search(r"sol_freeze_gate\s*=\s*PASS", text):
        raise SystemExit(f"FAIL-CLOSED: {SOL_REPLY} does not carry `sol_freeze_gate = PASS`")
    return out, hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_receipt(issued_at):
    declared, sol_digest = sol_declared_digests()
    bound, mismatches = [], []
    for field, artifact_id, path in BOUND:
        mine = sha256_file(path)
        theirs = declared.get(field + "_digest")
        if theirs != mine:
            mismatches.append({"artifact_id": artifact_id, "recomputed": mine, "sol_declared": theirs})
        bound.append({"artifact_id": artifact_id, "path": path, "sha256": mine,
                      "sol_declared_sha256": theirs, "agrees": theirs == mine})
    if mismatches:
        raise SystemExit("FAIL-CLOSED: recomputed digests disagree with Sol's declared block: "
                         + json.dumps(mismatches, indent=2))
    return {
        "receipt_id": RECEIPT_ID,
        "freeze_id": FREEZE_ID,
        "receipt_format": ("commander freeze receipt, JSON rendering of the convention established by "
                           "provenance/ninfty_freeze_receipt_sol75.md (裁定111). This is a control-plane "
                           "receipt, not a normative schema of its own."),
        "authorized_by": {
            "document": SOL_REPLY,
            "sha256": sol_digest,
            "clause": "F99-5.2 (sol_freeze_gate = PASS) / F99-5.1 (lane B independent producer 実装認可)",
            "commander_ruling": "裁定412",
        },
        "issued_at": issued_at,
        "bound_artifacts": bound,
        "byte_frozen_predecessors": [
            {"artifact_id": aid, "path": path, "sha256": sha256_file(path),
             "status": "byte-frozen history -- superseded, never overwritten (F99-5.2)"}
            for aid, path in PREDECESSORS
        ],
        "authorized_scope": [
            "the W6KEY-plane specification bundle (spec v20 / contract v15 / manifest v15 / "
            "bundle-selfaudit v11) is ADOPTED",
            "the lane B independent per-point W-6 producer implementation scope (F99-5.1), under the "
            "acceptance conditions restated in `lane_b_conditions`",
        ],
        "not_authorized_by_this_receipt": NOT_AUTHORISED,
        "not_authorized_note": ("Sol 便99 F99-5.2 verbatim: these may not be implicitly derived from the "
                               "same freeze PASS. A green suite, a green CI job and a completed lane B "
                               "producer move none of them."),
        "lane_b_conditions": [
            "lane B constructs each rational root's exact witness from its OWN curve/native data",
            "lane B imports/reads no lane A producer, canonicaliser, branch-token helper or output token; "
            "only the normative schema and its literals are shared",
            "finite points carry the x-root AND the y-root rank; infinity carries its own branch; the "
            "total degree-12 accounting is reconstructed from the per-point records",
            "both R1' and R2' are exercised, with mutation/negative fixtures and source digests, "
            "fail-closed",
            "diagnostic_construction=true, W6_CLOSED=false; AGGREGATE stays ABSENT until lane B exists",
            "even with lane B complete, only the AGGREGATE plane closes: IMAGE-MU stays UNKNOWN, so W-6 "
            "is OPEN and EP stays uncalibrated/UNKNOWN",
        ],
        "era_adoption": {
            "authority": "governing spec sec.5.3.4 M-7 / dependency manifest Y-3c (宣言先行・採用後行)",
            "transition": "PENDING_ADOPTION -> ADOPTED",
            "era": {
                "predicate_spec_id": "mb/ninfty-stage2-predicate/v20",
                "verifier_contract_id": "mb/ninfty-verifier-contract/v15",
                "dependency_manifest_schema_id": "mb/dependency-manifest/v15",
            },
            "planes": W6KEY_PLANES,
            "note": ("before this receipt the two ERA_W6KEY planes were recorded PENDING_ADOPTION and "
                     "counted as neither PASS nor FAIL. From this receipt on they are evaluated exactly "
                     "like every other plane: exact era match, no 'newer is fine'. The other planes "
                     "(frozen_route_verifier / native_payload_schema / nf_route / decision_lane_predicate "
                     "/ control_plane) are UNCHANGED -- this receipt does not move them to v20/v15/v15."),
        },
        "ep_status": "uncalibrated/UNKNOWN",
        "w6_closed": False,
        "image_mu": "UNKNOWN",
        "calibrated_detector": False,
        "citation_convention": ("spec sec.5.3.7 RC-1..RC-4: this receipt binds ONLY the fields written in "
                               "it. Suite check counts, green/red breakdowns and timings are NOT bound by "
                               "it and must be cited with the suite log's own provenance."),
        "pending_queue_carried_forward": [
            "CR-11 implemented_checks layer = PENDING/UNKNOWN",
            "QD-6 bootstrap leaf lost guarantees = PENDING/UNKNOWN",
            "N-2(2)/H-1a'' independent rederive = PENDING/UNKNOWN",
        ],
    }


def render_md(receipt):
    lines = []
    A = lines.append
    A("# N∞ stage-2 freeze receipt(commander・便99 F99-5.2 / 裁定412)")
    A("")
    A("> **本稿は機械生成である。** 生成器 `search/gen_ep_freeze_receipt_sol99.py`、正本 JSON "
      f"`{JSON_OUT}`。digest は全て repository の実ファイルから再計算し、Sol 返信 §5 の宣言 block から"
      "機械抽出した値と突合して一致した場合にのみ発行される(不一致なら発行せず停止)。")
    A("")
    A(f"- receipt_id: `{receipt['receipt_id']}`")
    A(f"- freeze_id: `{receipt['freeze_id']}`")
    A("- authorized_by: `{0}` {1}(sha256 `{2}`・{3})".format(
        receipt["authorized_by"]["document"], receipt["authorized_by"]["clause"],
        receipt["authorized_by"]["sha256"], receipt["authorized_by"]["commander_ruling"]))
    A(f"- issued_at: {receipt['issued_at']}")
    A("")
    A("## 束縛する artifact(4 点)")
    A("")
    A("| artifact_id | path | sha256 | Sol 宣言値と一致 |")
    A("|---|---|---|---|")
    for b in receipt["bound_artifacts"]:
        A(f"| `{b['artifact_id']}` | `{b['path']}` | `{b['sha256']}` | {'yes' if b['agrees'] else 'NO'} |")
    A("")
    A("## byte 凍結のまま残る前版(上書きしない)")
    A("")
    for b in receipt["byte_frozen_predecessors"]:
        A(f"- `{b['artifact_id']}` — `{b['path']}` — `{b['sha256']}`")
    A("")
    A("## 発効対象(scope)")
    A("")
    for s in receipt["authorized_scope"]:
        A(f"- {s}")
    A("")
    A("## 発効対象**外**(この freeze PASS から導出することを禁じる)")
    A("")
    for s in receipt["not_authorized_by_this_receipt"]:
        A(f"- **{s}**")
    A("")
    A(f"> {receipt['not_authorized_note']}")
    A("")
    A("## lane B per-point producer の受入条件(F99-5.1)")
    A("")
    for s in receipt["lane_b_conditions"]:
        A(f"- {s}")
    A("")
    A("## era 遷移(PENDING_ADOPTION → ADOPTED)")
    A("")
    A(f"- 根拠: {receipt['era_adoption']['authority']}")
    A(f"- era: `{receipt['era_adoption']['era']['predicate_spec_id']}` / "
      f"`{receipt['era_adoption']['era']['verifier_contract_id']}` / "
      f"`{receipt['era_adoption']['era']['dependency_manifest_schema_id']}`")
    for plane, sources in sorted(receipt["era_adoption"]["planes"].items()):
        A(f"- plane `{plane}`: " + ", ".join(f"`{s}`" for s in sources))
    A(f"- {receipt['era_adoption']['note']}")
    A("")
    A("## 札(receipt が明記する状態)")
    A("")
    A(f"- ep_status = `{receipt['ep_status']}` / w6_closed = `{receipt['w6_closed']}` / "
      f"IMAGE-MU = `{receipt['image_mu']}` / calibrated_detector = `{receipt['calibrated_detector']}`")
    A(f"- {receipt['citation_convention']}")
    A("")
    A("## pending queue(そのまま保持)")
    A("")
    for s in receipt["pending_queue_carried_forward"]:
        A(f"- {s}")
    A("")
    return "\n".join(lines) + "\n"


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="verify the on-disk artifacts against a fresh derivation; write nothing")
    args = ap.parse_args(argv)

    json_path = os.path.join(REPO, *JSON_OUT.split("/"))
    md_path = os.path.join(REPO, *MD_OUT.split("/"))

    if args.check:
        with open(json_path, encoding="utf-8") as f:
            on_disk = json.load(f)
        fresh = build_receipt(on_disk.get("issued_at"))
        if fresh != on_disk:
            print("MISMATCH: the on-disk receipt is not what the generator derives now.")
            return 1
        with open(md_path, encoding="utf-8") as f:
            md_disk = f.read()
        if md_disk != render_md(on_disk):
            print("MISMATCH: the provenance rendering is not what the generator derives from the JSON.")
            return 1
        print("receipt OK: JSON and provenance rendering both reproduce from the repository files.")
        return 0

    issued_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt = build_receipt(issued_at)
    with open(json_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    with open(md_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(render_md(receipt))
    print(json.dumps({"receipt_id": receipt["receipt_id"],
                      "json": JSON_OUT, "json_sha256": sha256_file(JSON_OUT),
                      "md": MD_OUT, "md_sha256": sha256_file(MD_OUT)}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
