#!/usr/bin/env python3
"""Independent checker for a sound multi-target B4 SAT shard.

The encoder shares one six-generator permutation image across all selected
roof words and adds one clause over every off-diagonal final-state variable.
Consequently SAT means at least one selected norm is nonidentity.  This
checker reconstructs every selected roof independently, verifies the complete
model and all 158 U_M relators, and emits only a finite B4-A candidate receipt.
UNSAT/all-pass is never promoted to B.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Sequence

RELATOR_SHA256 = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
TARGET_KEY_SHA256 = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
FROZEN_TUPLE_SHA256 = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
WORD_KEY_ARTIFACT_SHA256 = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
P2_INPUT_SCHEMA = "d972-b4-p2-magnus-input/v2"
P2_INPUT_SHA256 = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
RHO_WORDS_SOURCE = "universal_v2_canonical"
RHO_WORDS_SHA256 = "23db316e11e6486e0475b8425ff8ea6666941b5bff0943bf872e39761d0398ed"
RHO = [[-6, -5, -3], [3], [5], [-3, -2, -1], [-5, -4, -1], [1]]


def cjson(x: object) -> bytes:
    return json.dumps(x, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def sha(x: object) -> str:
    return hashlib.sha256(cjson(x)).hexdigest()


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def substitute(word: Sequence[int], rho: Sequence[Sequence[int]]) -> list[int]:
    out: list[int] = []
    for raw in word:
        if raw == 0 or abs(raw) > 6:
            raise ValueError(f"invalid U_M letter {raw}")
        atom = list(rho[abs(raw) - 1])
        out.extend(atom if raw > 0 else [-x for x in reversed(atom)])
    return out


def rho_power_words(power: int) -> list[list[int]]:
    out = [[i] for i in range(1, 7)]
    for _ in range(power):
        out = [substitute(word, RHO) for word in out]
    return out


def embed_f2_word(word: Sequence[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        if raw == 1:
            out.append(1)
        elif raw == -1:
            out.append(-1)
        elif raw == 2:
            out.append(4)
        elif raw == -2:
            out.append(-4)
        else:
            raise ValueError(f"invalid F2 letter {raw}")
    return out


def selected_roof_word(word: Sequence[int]) -> list[int]:
    marked = embed_f2_word(word)
    out: list[int] = []
    for power in reversed(range(5)):
        out.extend(substitute(marked, rho_power_words(power)))
    return out


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(q[x - 1] for x in p)


def identity(degree: int) -> tuple[int, ...]:
    return tuple(range(1, degree + 1))


def inverse(p: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(p)
    for i, x in enumerate(p, 1):
        out[x - 1] = i
    return tuple(out)


def eval_word(word: Sequence[int], gens: Sequence[tuple[int, ...]]) -> tuple[int, ...]:
    out = identity(len(gens[0]))
    for raw in word:
        g = gens[abs(raw) - 1]
        out = compose(out, g if raw > 0 else inverse(g))
    return out


def load_inputs(manifest_path: Path, relator_path: Path,
                artifact_path: Path) -> tuple[dict[str, Any], list[list[int]], list[list[Any]]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(isinstance(manifest, dict) and
            manifest.get("schema") == "d972-b4-permutation-sat-or/v1",
            "OR manifest schema mismatch")
    require(hashlib.sha256(relator_path.read_bytes()).hexdigest() == P2_INPUT_SHA256,
            "relator input is not the pinned v2 artifact")
    rel_obj = json.loads(relator_path.read_text(encoding="utf-8"))
    require(isinstance(rel_obj, dict) and
            rel_obj.get("schema") == P2_INPUT_SCHEMA and
            rel_obj.get("rho_words_source") == RHO_WORDS_SOURCE and
            rel_obj.get("rho_words") == RHO,
            "relator input schema/rho source is not canonical v2")
    rels = rel_obj.get("relators", rel_obj.get("all_relators"))
    require(isinstance(rels, list) and len(rels) == 158 and sha(rels) == RELATOR_SHA256,
            "relators are not the frozen 158-word list")
    art = json.loads(artifact_path.read_text(encoding="utf-8"))
    rows = art.get("rows") if isinstance(art, dict) else art
    require(isinstance(art, dict) and art.get("schema") == "d972-b4-word-key-artifact/v1",
            "word/key artifact schema")
    require(isinstance(rows, list) and len(rows) == 972 and sha(rows) == WORD_KEY_ARTIFACT_SHA256,
            "word/key artifact digest/count")
    require(art.get("source_target_key_digest") == TARGET_KEY_SHA256 and
            art.get("frozen_tuple_sha256") == FROZEN_TUPLE_SHA256,
            "word/key artifact frozen fields")
    require(manifest.get("target_artifact_sha256") == WORD_KEY_ARTIFACT_SHA256,
            "OR manifest artifact digest")
    require(manifest.get("relator_sha256") == RELATOR_SHA256 and
            manifest.get("target_key_digest") == TARGET_KEY_SHA256 and
            manifest.get("frozen_tuple_sha256") == FROZEN_TUPLE_SHA256 and
            manifest.get("p2_input_schema") == P2_INPUT_SCHEMA and
            manifest.get("p2_input_file_sha256") == P2_INPUT_SHA256 and
            manifest.get("rho_words_source") == RHO_WORDS_SOURCE and
            manifest.get("rho_words_sha256") == RHO_WORDS_SHA256 and
            manifest.get("rho_words") == RHO,
            "OR manifest frozen digests")
    indices = manifest.get("target_indices")
    keys = manifest.get("target_keys")
    words = manifest.get("target_words")
    roofs = manifest.get("roof_words")
    count = manifest.get("target_count")
    require(isinstance(indices, list) and isinstance(keys, list) and
            isinstance(words, list) and isinstance(roofs, list) and
            isinstance(count, int) and count == len(indices) >= 2 and
            len(keys) == len(words) == len(roofs) == count,
            "OR target arrays/count")
    require(len(set(indices)) == count and all(isinstance(i, int) and 0 <= i < 972 for i in indices),
            "OR target indices")
    require(len({tuple(w) for w in words}) == count,
            "OR shard contains duplicate roof words")
    for i, key, word, roof in zip(indices, keys, words, roofs, strict=True):
        require(rows[i][1] == key and rows[i][2] == word,
                "OR target row binding")
        require(isinstance(word, list) and all(isinstance(x, int) and x != 0 and abs(x) <= 2 for x in word),
                "OR F2 target word")
        require(roof == selected_roof_word(word), "OR roof reconstruction")
    return manifest, rels, rows


def parse_model(path: Path) -> tuple[set[int], set[int]]:
    true_vars: set[int] = set()
    seen: set[int] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or not line.startswith("v"):
            continue
        for token in line[1:].split():
            raw = int(token)
            if raw == 0:
                continue
            var = abs(raw)
            require(var not in seen, f"duplicate model assignment {var}")
            seen.add(var)
            if raw > 0:
                true_vars.add(var)
    require(bool(seen), "model contains no v-lines")
    return true_vars, seen


def check_cnf(path: Path, true_vars: set[int], nvars: int) -> tuple[int, int]:
    clauses: list[list[int]] = []
    declared: tuple[int, int] | None = None
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            _, kind, nv, nc = line.split()
            require(kind == "cnf", "CNF header kind")
            declared = (int(nv), int(nc))
            continue
        vals = [int(x) for x in line.split()]
        require(vals and vals[-1] == 0, "unterminated CNF clause")
        require(all(1 <= abs(literal) <= nvars for literal in vals[:-1]),
                "CNF literal is outside declared variable range")
        clauses.append(vals[:-1])
    require(declared == (nvars, len(clauses)), "CNF header/clauses mismatch")
    for i, clause in enumerate(clauses):
        require(any((literal > 0) == (abs(literal) in true_vars) for literal in clause),
                f"model does not satisfy clause {i}")
    return declared


def reconstruct_generators(true_vars: set[int], degree: int) -> list[tuple[int, ...]]:
    gens: list[tuple[int, ...]] = []
    for g in range(6):
        image: list[int] = []
        for i in range(degree):
            base = 1 + g * degree * degree + i * degree
            chosen = [j + 1 for j in range(degree) if base + j in true_vars]
            require(len(chosen) == 1, f"generator {g + 1} row {i + 1} not one-hot")
            image.append(chosen[0])
        require(set(image) == set(range(1, degree + 1)), f"generator {g + 1} not bijective")
        gens.append(tuple(image))
    return gens


def self_test() -> None:
    require(embed_f2_word([1, -2, 2, -1]) == [1, -4, 4, -1], "marked F2 selftest")
    expected: list[int] = []
    old: list[int] = []
    for power in reversed(range(5)):
        expected.extend(substitute([4], rho_power_words(power)))
        old.extend(substitute([2], rho_power_words(power)))
    require(selected_roof_word([2]) == expected, "marked y roof selftest")
    require(selected_roof_word([2]) != old, "old y=U2 roof accepted")
    require(check_cnf(Path(_tiny_cnf_path("p cnf 1 1\n1 0\n")), {1}, 1) == (1, 1),
            "tiny CNF selftest")


def _tiny_cnf_path(text: str) -> str:
    # Used only by selftest; a named temp file avoids importing the encoder.
    import tempfile
    handle = tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False, encoding="ascii")
    handle.write(text)
    handle.close()
    return handle.name


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--cnf", type=Path)
    ap.add_argument("--manifest", type=Path)
    ap.add_argument("--model", type=Path)
    ap.add_argument("--relators", type=Path)
    ap.add_argument("--word-key-artifact", type=Path)
    ap.add_argument("--receipt", type=Path)
    args = ap.parse_args()
    if args.self_test:
        self_test()
        print("D972_B4_SAT_OR_CHECKER_SELFTEST_PASS")
        return 0
    required = (args.cnf, args.manifest, args.model, args.relators, args.word_key_artifact)
    if any(x is None for x in required):
        ap.error("--cnf, --manifest, --model, --relators, and --word-key-artifact are required")
    assert args.cnf and args.manifest and args.model and args.relators and args.word_key_artifact
    manifest, rels, rows = load_inputs(args.manifest, args.relators, args.word_key_artifact)
    degree = manifest.get("degree")
    require(isinstance(degree, int) and 2 <= degree <= 8, "degree bound")
    true_vars, assigned = parse_model(args.model)
    nvars = manifest.get("nvars")
    require(isinstance(nvars, int) and assigned == set(range(1, nvars + 1)),
            "model assignment is incomplete")
    require(manifest.get("cnf_sha256") == hashlib.sha256(args.cnf.read_bytes()).hexdigest(),
            "manifest CNF digest")
    parsed_nvars, parsed_clauses = check_cnf(args.cnf, true_vars, nvars)
    require(manifest.get("nvars") == parsed_nvars and
            manifest.get("clauses") == parsed_clauses,
            "manifest CNF size does not match parsed CNF")
    gens = reconstruct_generators(true_vars, degree)
    one = identity(degree)
    for i, rel in enumerate(rels):
        require(eval_word(rel, gens) == one, f"relator {i} nonidentity")
    for i, word in enumerate(rho_power_words(5)):
        require(eval_word(word, gens) == gens[i], f"rho^5 generator {i + 1} mismatch")
    defects = []
    indices = manifest["target_indices"]
    words = manifest["target_words"]
    keys = manifest["target_keys"]
    for index, key, word in zip(indices, keys, words, strict=True):
        defect = eval_word(selected_roof_word(word), gens)
        if defect != one:
            defects.append({"target_index": index, "target_key": key,
                            "target_word": word, "defect": list(defect)})
    require(defects, "OR SAT model has no nonidentity selected roof")
    receipt = {
        "schema": "d972-b4-finite-image-sat-or/v1",
        "status": "B4-A_CANDIDATE_FINITE_SAT_OR",
        "degree": degree,
        "target_indices": indices,
        "target_count": len(indices),
        "defects": defects,
        "h_images": [list(g) for g in gens],
        "rho_words": RHO,
        "rho_words_source": RHO_WORDS_SOURCE,
        "rho_words_sha256": RHO_WORDS_SHA256,
        "source_sha256": P2_INPUT_SHA256,
        "rho_words_legacy_json_mismatch": False,
        "p2_input_schema": P2_INPUT_SCHEMA,
        "p2_input_file_sha256": P2_INPUT_SHA256,
        "all_relators": rels,
        "all_relators_sha256": RELATOR_SHA256,
        "target_key_digest": TARGET_KEY_SHA256,
        "word_key_artifact_sha256": WORD_KEY_ARTIFACT_SHA256,
        "cnf_sha256": manifest["cnf_sha256"],
    }
    if args.receipt:
        args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
