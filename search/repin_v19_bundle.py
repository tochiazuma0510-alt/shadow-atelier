#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/repin_v19_bundle.py -- 便95 修理バンドル用の digest 再 pin ツール。

hash 順序(便 66 F11)は manifest -> contract -> spec -> receipt。上流文書の
1 バイト変更は下流の pin を必ず stale にするので、pin 値を人手で書き写す
運用は「手写し禁止」に反する。本ツールは

  1. manifest の実バイト digest を計算し、contract 内の全 manifest pin を置換、
  2. その結果の contract の実バイト digest を計算し、spec 内の全 contract pin を置換、
  3. spec の実バイト digest を計算して表示、

を 1 パスで行う(非循環なので反復不要)。置換は「64 hex の literal を別の
64 hex へ」の exact 置換のみで、置換件数が 0 の文書があれば異常として非零終了
する(黙って何もしないことを許さない)。

usage: python search/repin_v19_bundle.py [--check]
  --check : 置換せず、現状の pin が実 digest と一致するかだけを報告する
            (不一致なら非零終了)。
"""
from __future__ import annotations
import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MANIFEST = "docs/mb_dependency_manifest_v14.md"
CONTRACT = "docs/mb_ninfty_verifier_contract_v14.md"
SPEC = "docs/week4-NInfty_stage2_spec_v19.md"

HEX64 = re.compile(r"\b[0-9a-f]{64}\b")


def _read(rel):
    with io.open(os.path.join(ROOT, rel), encoding="utf-8", newline="") as f:
        return f.read()


def _write(rel, text):
    with io.open(os.path.join(ROOT, rel), "w", encoding="utf-8", newline="") as f:
        f.write(text)


def _digest(rel):
    with open(os.path.join(ROOT, rel), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# Pin sites are located STRUCTURALLY (the line that assigns the pin, or the
# live_authority_refs entry that labels the artifact), never by hard-coding
# the hex value being replaced.
PIN_PATTERNS = {
    "manifest": [
        re.compile(r"(dependency_manifest_schema_digest\s*=\s*)([0-9a-f]{64})"),
        re.compile(r'(artifact_id: "mb/dependency-manifest/v\d+",\s*\n\s*digest_or_receipt_slot: ")([0-9a-f]{64})'),
    ],
    "contract": [
        re.compile(r"(verifier_contract_digest\s*=\s*)([0-9a-f]{64})"),
        re.compile(r'(artifact_id: "mb/ninfty-verifier-contract/v\d+",\s*\n\s*digest_or_receipt_slot: ")([0-9a-f]{64})'),
    ],
}


def repin(text, which, new_digest):
    total = 0
    stale = []
    for pat in PIN_PATTERNS[which]:
        def _sub(m):
            nonlocal total
            total += 1
            if m.group(2) != new_digest:
                stale.append(m.group(2))
            return m.group(1) + new_digest
        text = pat.sub(_sub, text)
    return text, total, stale


def main(argv):
    check_only = "--check" in argv
    report = []
    ok = True

    manifest_digest = _digest(MANIFEST)
    contract_text, n, stale = repin(_read(CONTRACT), "manifest", manifest_digest)
    if n == 0:
        print("ERROR: no manifest pin site found in contract", file=sys.stderr)
        return 2
    report.append(("contract <- manifest pin", n, stale))
    if stale and not check_only:
        _write(CONTRACT, contract_text)
    if stale and check_only:
        ok = False

    contract_digest = _digest(CONTRACT)
    spec_text, n2, stale2 = repin(_read(SPEC), "contract", contract_digest)
    if n2 == 0:
        print("ERROR: no contract pin site found in spec", file=sys.stderr)
        return 2
    report.append(("spec <- contract pin", n2, stale2))
    if stale2 and not check_only:
        _write(SPEC, spec_text)
    if stale2 and check_only:
        ok = False

    # spec also carries the manifest pin directly (§6 実装契約 block + §10).
    spec_text2, n3, stale3 = repin(_read(SPEC), "manifest", manifest_digest)
    if n3 == 0:
        print("ERROR: no manifest pin site found in spec", file=sys.stderr)
        return 2
    report.append(("spec <- manifest pin", n3, stale3))
    if stale3 and not check_only:
        _write(SPEC, spec_text2)
    if stale3 and check_only:
        ok = False

    print("manifest sha256 =", _digest(MANIFEST), MANIFEST)
    print("contract sha256 =", _digest(CONTRACT), CONTRACT)
    print("spec     sha256 =", _digest(SPEC), SPEC)
    for name, n_, st in report:
        print("  %-26s sites=%d stale_before=%s" % (name, n_, st if st else 0))
    if check_only and not ok:
        print("RESULT: STALE PINS (re-run without --check to repin)")
        return 1
    print("RESULT: pins consistent" if check_only else "RESULT: repinned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
