#!/usr/bin/env python3
"""Versioned checker-only repair for the 157ee direct-canary shape drift."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "search/check_d972_b345_joint_kernel_qstar_closure_v1.py"
BASE_SHA256 = "9e721634d1f16be806e315eec263ec272bc023587f862703c094b7dd37c0111f"


def require(value: Any, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


require(BASE_PATH.is_file(), "157ef missing frozen checker v1")
require(sha_file(BASE_PATH) == BASE_SHA256, "157ef checker v1 SHA drift")
_spec = importlib.util.spec_from_file_location("_d972_jkq_checker_v1_frozen", BASE_PATH)
require(_spec is not None and _spec.loader is not None, "157ef checker import spec")
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)


def repaired_direct_canary(prev: Any, old: Any, e3: Any, e4: Any,
                           contexts: Sequence[Any], pool: Any, basis: Any,
                           oracle: Any, word: Sequence[int], expected: int,
                           label: str) -> dict[str, Any]:
    """Mirror the producer's private-value gate before its public projection."""
    base.require(e3.eval(old.embed_f2(word)) == e3.identity and all(
        e4.eval(word, [left, right]) == e4.identity
        for left, right in contexts), "checker canary typing")
    detail = old.checker_target6_formula(word, e4, include_gradient=True)
    raw = detail["direct_gradient"]
    public = old.checker_target6_public_from_detail(word, detail)
    base.require(detail["direct_value"] == e4.identity and
                 detail["formula_equals_direct"] is True and
                 public["formula_equals_direct"] is True,
                 "checker canary formula")
    direct = oracle.sparse(raw)
    remainder = old.checker_probe_remainder(raw, pool, basis)
    nf = prev.public_remainder_coefficient(remainder)
    base.require(direct == nf == expected, "checker canary direct/NF")
    return {"label": label, "word_length": len(word),
            "word_sha256": base.digest_obj(list(word)), "scalar": direct,
            "remainder_support": len(remainder),
            "remainder_sha256": base.digest_obj(sorted(remainder.items())),
            "formula_direct_equal": True, "NF_equal": True}


base.direct_canary = repaired_direct_canary


def self_test_repair() -> None:
    class ToyE3:
        identity = "e3-id"

        @staticmethod
        def eval(_word: Any) -> str:
            return "e3-id"

    class ToyE4:
        identity = "e4-id"

        @staticmethod
        def eval(_word: Any, _images: Any = None) -> str:
            return "e4-id"

    class ToyOld:
        direct_value = "e4-id"
        formula_flag = True

        @staticmethod
        def embed_f2(word: Sequence[int]) -> list[int]:
            return list(word)

        @classmethod
        def checker_target6_formula(cls, _word: Sequence[int], _e4: Any,
                                    *, include_gradient: bool) -> dict[str, Any]:
            require(include_gradient is True, "157ef toy gradient route")
            return {"direct_gradient": {"raw": 1},
                    "direct_value": cls.direct_value,
                    "formula_equals_direct": cls.formula_flag}

        @classmethod
        def checker_target6_public_from_detail(cls, _word: Sequence[int],
                                               detail: dict[str, Any]) -> dict[str, Any]:
            # This is the exact relevant v1 shape: no quotient_identity field.
            return {"formula_equals_direct": detail["formula_equals_direct"]}

        @staticmethod
        def checker_probe_remainder(_raw: Any, _pool: Any, _basis: Any) -> dict[str, int]:
            return {"remainder": 2}

    class ToyOracle:
        @staticmethod
        def sparse(_raw: Any) -> int:
            return 2

    class ToyPrev:
        @staticmethod
        def public_remainder_coefficient(_remainder: Any) -> int:
            return 2

    row = repaired_direct_canary(ToyPrev(), ToyOld(), ToyE3(), ToyE4(),
                                 [("left", "right")], None, None,
                                 ToyOracle(), [1, -2], 2, "toy")
    require(row["scalar"] == 2 and row["formula_direct_equal"] is True and
            row["NF_equal"] is True, "157ef repaired canary fixture")

    ToyOld.direct_value = "mutated"
    try:
        repaired_direct_canary(ToyPrev(), ToyOld(), ToyE3(), ToyE4(),
                               [("left", "right")], None, None,
                               ToyOracle(), [1], 2, "bad-value")
    except RuntimeError:
        pass
    else:
        raise RuntimeError("157ef direct-value mutation accepted")
    ToyOld.direct_value = "e4-id"

    ToyOld.formula_flag = False
    try:
        repaired_direct_canary(ToyPrev(), ToyOld(), ToyE3(), ToyE4(),
                               [("left", "right")], None, None,
                               ToyOracle(), [1], 2, "bad-formula")
    except RuntimeError:
        pass
    else:
        raise RuntimeError("157ef formula mutation accepted")
    ToyOld.formula_flag = True

    print("D972_B345_JOINT_KERNEL_QSTAR_CHECKER_V2_SELFTEST_PASS "
          "public_shape_without_quotient_identity=1 mutations=2", flush=True)


def main() -> int:
    if sys.argv[1:] == ["--self-test"]:
        base.self_test()
        self_test_repair()
        return 0
    result = base.main()
    require(result == 0, "157ef frozen checker return")
    print("D972_B345_JOINT_KERNEL_QSTAR_CHECKER_V2_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
