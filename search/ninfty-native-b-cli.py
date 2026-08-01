#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search/ninfty-native-b-cli.py

Thin CLI wrapper around search/ninfty-checker.py's construct_native_from_scratch
(itself a thin wrapper over search/ninfty-checker-native.py's
construct_checker_native), for EP registry provisioning
(search/ninfty-ep-genuine-provisioning.py) to invoke as a subprocess -- mirrors
search/ninfty-nf-laneb.py's separation discipline: this file does nothing but
load a candidate JSON and print construct_native_from_scratch's own output
verbatim, no extra logic.

usage: python search/ninfty-native-b-cli.py path/to/candidate.json
       python search/ninfty-native-b-cli.py -   (reads candidate JSON from stdin)
"""
from __future__ import annotations
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _load_checker():
    path = os.path.join(HERE, "ninfty-checker.py")
    spec = importlib.util.spec_from_file_location("ninfty_checker_for_native_b_cli", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def canonical_serialize(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def main(argv):
    if not argv:
        print("usage: ninfty-native-b-cli.py <candidate.json | ->", file=sys.stderr)
        return 2
    src = argv[0]
    if src == "-":
        candidate = json.load(sys.stdin)
    else:
        with open(src, "r", encoding="utf-8") as f:
            candidate = json.load(f)
    checker = _load_checker()
    result = checker.construct_native_from_scratch(candidate["a"], candidate["p"], candidate["f6"])
    print(canonical_serialize(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
