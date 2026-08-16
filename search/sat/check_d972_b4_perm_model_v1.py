#!/usr/bin/env python3
"""Independent fail-closed checker for d972_b4 permutation SAT models."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Sequence

RELATOR_SHA256 = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
TARGET_KEY_SHA256 = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
FROZEN_TUPLE_SHA256 = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
P2_INPUT_SCHEMA = "d972-b4-p2-magnus-input/v2"
P2_INPUT_SHA256 = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
RHO_WORDS_SOURCE = "universal_v2_canonical"
RHO_WORDS_SHA256 = "23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed"
RHO = [[-6, -5, -3], [3], [5], [-3, -2, -1], [-5, -4, -1], [1]]


def cjson(x: object) -> bytes:
    return json.dumps(x, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def sha(x: object) -> str:
    return hashlib.sha256(cjson(x)).hexdigest()


def substitute(word: Sequence[int], rho: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for letter in word:
        atom = list(rho[abs(letter) - 1])
        if letter < 0:
            atom = [-x for x in reversed(atom)]
        out.extend(atom)
    return out


def rho_power_words(t: int) -> list[list[int]]:
    out = [[i] for i in range(1, 7)]
    for _ in range(t):
        out = [substitute(w, RHO) for w in out]
    return out


def embed_f2_word(target_word: Sequence[int]) -> list[int]:
    """Mark F2 into U_M via j(x)=U_1 and j(y)=U_4."""
    out: list[int] = []
    for letter in target_word:
        if letter == 1:
            out.append(1)
        elif letter == -1:
            out.append(-1)
        elif letter == 2:
            out.append(4)
        elif letter == -2:
            out.append(-4)
        else:
            raise ValueError(f"F2 roof word has invalid letter {letter}")
    return out


def selected_roof_word(target_word: Sequence[int]) -> list[int]:
    out: list[int] = []
    marked_word = embed_f2_word(target_word)
    for t in reversed(range(5)):
        out.extend(substitute(marked_word, rho_power_words(t)))
    return out


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(q[x - 1] for x in p)


def identity(d: int) -> tuple[int, ...]:
    return tuple(range(1, d + 1))


def inv(p: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(p)
    for i, x in enumerate(p, 1):
        out[x - 1] = i
    return tuple(out)


def eval_word(word: Sequence[int], gens: Sequence[tuple[int, ...]]) -> tuple[int, ...]:
    out = identity(len(gens[0]))
    for x in word:
        g = gens[abs(x) - 1]
        out = compose(out, g if x > 0 else inv(g))
    return out


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def load_inputs(manifest_path: Path, relator_path: Path, artifact_path: Path) -> tuple[dict, list[list[int]], list[list[object]]]:
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict) or manifest.get("schema") != "d972-b4-permutation-sat/v1":
        raise ValueError("manifest schema mismatch")
    if hashlib.sha256(relator_path.read_bytes()).hexdigest() != P2_INPUT_SHA256:
        raise ValueError("relator input is not the pinned v2 artifact")
    rel_obj = load_json(relator_path)
    if (not isinstance(rel_obj, dict) or
            rel_obj.get("schema") != P2_INPUT_SCHEMA or
            rel_obj.get("rho_words_source") != RHO_WORDS_SOURCE or
            rel_obj.get("rho_words") != RHO):
        raise ValueError("relator input schema/rho source is not canonical v2")
    rels = rel_obj.get("relators", rel_obj.get("all_relators"))
    if not isinstance(rels, list) or len(rels) != 158 or sha(rels) != RELATOR_SHA256:
        raise ValueError("relators are not the frozen 158-word list")
    art_obj = load_json(artifact_path)
    rows = art_obj.get("rows") if isinstance(art_obj, dict) else art_obj
    if not isinstance(rows, list) or len(rows) != 972:
        raise ValueError("word/key artifact count is not 972")
    if not isinstance(art_obj, dict) or art_obj.get("canonical_bytes_sha256") != sha(rows):
        raise ValueError("word/key artifact canonical digest mismatch")
    if art_obj.get("source_target_key_digest") != TARGET_KEY_SHA256:
        raise ValueError("word/key artifact target digest mismatch")
    if art_obj.get("frozen_tuple_sha256") != FROZEN_TUPLE_SHA256:
        raise ValueError("word/key artifact frozen tuple digest mismatch")
    if (manifest.get("relator_sha256") != RELATOR_SHA256 or
            manifest.get("target_key_digest") != TARGET_KEY_SHA256 or
            manifest.get("p2_input_schema") != P2_INPUT_SCHEMA or
            manifest.get("p2_input_file_sha256") != P2_INPUT_SHA256 or
            manifest.get("rho_words_source") != RHO_WORDS_SOURCE or
            manifest.get("rho_words_sha256") != RHO_WORDS_SHA256 or
            manifest.get("rho_words") != RHO):
        raise ValueError("manifest frozen digest mismatch")
    if manifest.get("target_artifact_sha256") != sha(rows):
        raise ValueError("manifest/artifact digest mismatch")
    ti = manifest.get("target_index")
    if not isinstance(ti, int) or not 0 <= ti < 972:
        raise ValueError("manifest target index out of range")
    return manifest, rels, rows


def parse_model(path: Path | str) -> tuple[set[int], set[int]]:
    true_vars: set[int] = set()
    seen: set[int] = set()
    source = path if isinstance(path, str) else path.read_text(encoding="utf-8")
    for line in source.splitlines():
        line = line.strip()
        if not line or not line.startswith("v"):
            continue
        for token in line[1:].split():
            x = int(token)
            if x == 0:
                continue
            a = abs(x)
            if a in seen:
                raise ValueError(f"duplicate model assignment for variable {a}")
            seen.add(a)
            if x > 0:
                true_vars.add(a)
    if not seen:
        raise ValueError("model contains no v-lines")
    return true_vars, seen


def check_cnf(cnf_path: Path | str, true_vars: set[int], nvars: int) -> tuple[int, int]:
    clauses: list[list[int]] = []
    declared = None
    source = cnf_path if isinstance(cnf_path, str) else cnf_path.read_text(encoding="ascii")
    for line in source.splitlines():
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            _, kind, nv, nc = line.split()
            if kind != "cnf":
                raise ValueError("CNF header kind")
            declared = (int(nv), int(nc))
            continue
        vals = [int(x) for x in line.split()]
        if not vals or vals[-1] != 0:
            raise ValueError("unterminated CNF clause")
        clauses.append(vals[:-1])
    if declared != (nvars, len(clauses)):
        raise ValueError(f"CNF header mismatch {declared} vs {(nvars, len(clauses))}")
    for i, clause in enumerate(clauses):
        if not any((x > 0) == (abs(x) in true_vars) for x in clause):
            raise ValueError(f"model does not satisfy CNF clause {i}")
    return declared[0], len(clauses)


def self_test() -> None:
    """Positive tiny semantic/model checks plus tamper rejection."""
    gens = [(2, 1)] * 6
    rho5 = rho_power_words(5)
    assert all(eval_word(w, gens) == gens[i] for i, w in enumerate(rho5))
    assert eval_word(selected_roof_word([1]), gens) == (2, 1)
    assert embed_f2_word([1, -2, 2, -1]) == [1, -4, 4, -1]
    asymmetric = [(2, 1, 3), (1, 3, 2), (2, 3, 1),
                  (3, 2, 1), (1, 2, 3), (3, 1, 2)]
    expected_y: list[int] = []
    old_y: list[int] = []
    for t in reversed(range(5)):
        expected_y.extend(substitute([4], rho_power_words(t)))
        old_y.extend(substitute([2], rho_power_words(t)))
    assert selected_roof_word([2]) == expected_y
    assert selected_roof_word([2]) != old_y
    assert eval_word(selected_roof_word([1]), asymmetric) != \
        eval_word(selected_roof_word([2]), asymmetric)
    # A one-variable model/CNF is enough to exercise parser and clause checks.
    tiny_cnf = "p cnf 1 1\n1 0\n"
    assert check_cnf(tiny_cnf, parse_model("v 1 0\n")[0], 1) == (1, 1)
    try:
        check_cnf(tiny_cnf, parse_model("v -1 0\n")[0], 1)
    except ValueError:
        pass
    else:
        raise AssertionError("tampered tiny model accepted")
    # The checker must remain independent of the encoder module.
    needle = "from " + "encode_d972_b4_perm_v1"
    assert needle not in Path(__file__).read_text(encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--cnf", type=Path)
    ap.add_argument("--manifest", type=Path)
    ap.add_argument("--model", type=Path)
    ap.add_argument("--relators", type=Path)
    ap.add_argument("--word-key-artifact", type=Path)
    ap.add_argument("--receipt", type=Path)
    args = ap.parse_args(argv)
    if args.self_test:
        self_test()
        print("D972_B4_SAT_CHECKER_SELFTEST_PASS")
        return 0
    required = (args.cnf, args.manifest, args.model, args.relators, args.word_key_artifact)
    if any(x is None for x in required):
        ap.error("--cnf, --manifest, --model, --relators, and --word-key-artifact are required unless --self-test is used")
    assert args.cnf is not None and args.manifest is not None and args.model is not None
    assert args.relators is not None and args.word_key_artifact is not None
    manifest, rels, rows = load_inputs(args.manifest, args.relators, args.word_key_artifact)
    d = manifest.get("degree")
    if not isinstance(d, int) or d < 2 or d > 8:
        raise ValueError("invalid degree")
    true_vars, assigned = parse_model(args.model)
    if assigned != set(range(1, int(manifest["nvars"]) + 1)):
        missing = sorted(set(range(1, int(manifest["nvars"]) + 1)) - assigned)
        extra = sorted(assigned - set(range(1, int(manifest["nvars"]) + 1)))
        raise ValueError(f"model assignment is not complete: missing={missing[:5]} extra={extra[:5]}")
    actual_sha = hashlib.sha256(args.cnf.read_bytes()).hexdigest()
    if manifest.get("cnf_sha256") != actual_sha:
        raise ValueError("manifest CNF SHA-256 mismatch")
    parsed_nvars, parsed_clauses = check_cnf(args.cnf, true_vars, int(manifest["nvars"]))
    if manifest.get("nvars") != parsed_nvars or manifest.get("clauses") != parsed_clauses:
        raise ValueError("manifest CNF size does not match parsed header/clauses")
    gens: list[tuple[int, ...]] = []
    for g in range(6):
        vals = []
        for i in range(d):
            row = [1 + g * d * d + i * d + j for j in range(d)]
            chosen = [j + 1 for j, var in enumerate(row) if var in true_vars]
            if len(chosen) != 1:
                raise ValueError(f"generator {g+1} row {i+1} is not one-hot")
            vals.append(chosen[0])
        if set(vals) != set(range(1, d + 1)):
            raise ValueError(f"generator {g+1} is not bijective")
        gens.append(tuple(vals))

    for i, rel in enumerate(rels):
        if eval_word(rel, gens) != identity(d):
            raise ValueError(f"relator {i} is nonidentity")
    rho5 = rho_power_words(5)
    for i, word in enumerate(rho5):
        if eval_word(word, gens) != gens[i]:
            raise ValueError(f"rho^5 generator {i+1} mismatch")

    ti = int(manifest["target_index"])
    row = rows[ti]
    if not isinstance(row, list) or len(row) != 3:
        raise ValueError("selected artifact row malformed")
    target_word = row[2]
    if manifest.get("target_word") != target_word or manifest.get("target_key") != row[1]:
        raise ValueError("manifest target row binding mismatch")
    roof = selected_roof_word(target_word)
    defect = eval_word(roof, gens)
    if defect == identity(d):
        raise ValueError("roof defect is identity")
    receipt = {
        "schema": "d972-b4-finite-image-sat/v1",
        "status": "B4-A_CANDIDATE_FINITE_SAT",
        "degree": d, "target_index": ti, "target_key": row[1],
        "target_word": target_word, "roof_order": [4, 3, 2, 1, 0],
        "roof_word": roof, "defect": list(defect),
        "h_images": [list(g) for g in gens], "rho_words": RHO,
        "rho_words_source": RHO_WORDS_SOURCE,
        "rho_words_sha256": RHO_WORDS_SHA256,
        "source_sha256": P2_INPUT_SHA256,
        "rho_words_legacy_json_mismatch": False,
        "p2_input_schema": P2_INPUT_SCHEMA,
        "p2_input_file_sha256": P2_INPUT_SHA256,
        "all_relators": rels, "all_relators_sha256": RELATOR_SHA256,
        "target_keys_count": 972,
        "word_key_artifact_sha256": sha(rows),
        "cnf_sha256": hashlib.sha256(args.cnf.read_bytes()).hexdigest(),
        "manifest": str(args.manifest),
    }
    if args.receipt:
        args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
