#!/usr/bin/env python3
"""Independent, fail-closed checker for the typed B4 6/158 bundle.

This checker is intentionally stricter than the older finite-image checker.
The older checker answers a finite permutation-image question.  This file
checks the *meaning* of a receipt: the marked six generators, the current
Hurwitz rotation, the 18+28x5 layout, the A.18 words, the exact 972 word/key
rows, and the presence of raw certificates for the finite-group assertions.

The checker never promotes a fixed-U all-pass, a supplied boolean, or a
relator digest to a B4 theorem.  A receipt is accepted (exit 0) only as a
``LOCAL_TYPED_RECEIPT_CROSSCHECKED`` receipt when every semantic gate has a
raw certificate.  The checker does not emit an A/B or Ihara conclusion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "search" / "certs" / "d972_b4_p2_magnus_input_v2_20260816.json"
DEFAULT_WORDS = ROOT / "search" / "certs" / "d972_b4_word_key_artifact_v1_20260816.json"
DEFAULT_STAGE2 = ROOT / "search" / "probe" / "hsp7_gap_v1" / "stage2_k05.g"
DEFAULT_CERT = Path("d972_b4_typed_bundle_v2_certificate.json")

SOURCE_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
RELATOR_SHA = "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e"
ROOF_SHA = "3015b4e00a02ca2a9d6183dad4cb7ddabfd21ef03828837198aa96b2dc3461f8"
TARGET_SHA = "9c77e6768feb7ffe7143abf18f753af70e81b8e9cc792910c30ae0075d3b1d62"
ROWS_SHA = "283bf9cc728ced084a3b276e4496fbbc69026589813a2f31caa0dcb7a3682930"
TUPLE_SHA = "32e78ca5b97cd8a6fa59a150dac77719c1b8cb527f0467570c4d284600465a91"
NORM_SHA = "ecf0cc8425bc24bdf6a8a352c223398221c4b179e09ee9a0bfe3dc888861683e"
STAGE2_SHA = "b2522f7d701525dc81c408d2b37b9fe693f017a11eeafb9333131de8c361daf5"
WORKER_SHA = "f9ad3f8f71dc5af3d20dbef66dc6a25c79a50393be55767c0fb9f077d46994e8"

# This is not copied from the receipt.  It is reconstructed below from the
# stage2 labels, sphere rows and the Hurwitz shift.
RHO = ((-6, -5, -3), (3,), (5,), (-3, -2, -1), (-5, -4, -1), (1,))
LEGACY_RHO = ((-3, -5, -6), (3,), (5,), (-1, -2, -3), (-1, -4, -5), (1,))

F6_LABELS = ("X12", "X13", "X14", "X23", "X24", "X34")
F6_PAIRS = ((1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4))


def cjson(value: Any) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def reduce_word(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        n = int(raw)
        require(n != 0, "zero in signed word")
        if out and out[-1] == -n:
            out.pop()
        else:
            out.append(n)
    return out


def inverse_word(word: Sequence[int]) -> list[int]:
    return [-int(x) for x in reversed(word)]


def rho_word(word: Sequence[int], rho: Sequence[Sequence[int]] = RHO) -> list[int]:
    out: list[int] = []
    for raw in word:
        n = int(raw)
        require(1 <= abs(n) <= 6, "rho alphabet drift")
        image = list(rho[abs(n) - 1])
        out.extend(inverse_word(image) if n < 0 else image)
    return reduce_word(out)


def exact_norm(f2_word: Sequence[int]) -> list[int]:
    """The frozen local norm, only as a word-level diagnostic."""
    base = []
    for raw in f2_word:
        n = int(raw)
        require(n != 0 and abs(n) <= 2, "F2 alphabet drift")
        image = 1 if abs(n) == 1 else 4
        base.append(image if n > 0 else -image)
    orbit: list[list[int]] = []
    current = reduce_word(base)
    for _ in range(5):
        orbit.append(current)
        current = rho_word(current)
    out: list[int] = []
    for item in reversed(orbit):
        out = reduce_word(out + item)
    return out


def signed_word(value: Any, width: int, label: str) -> list[int]:
    require(isinstance(value, list), f"{label}: not a list")
    out: list[int] = []
    for i, raw in enumerate(value):
        require(type(raw) is int and raw != 0 and abs(raw) <= width,
                f"{label}[{i}]: signed-word alphabet drift")
        out.append(raw)
    return out


def key_string(key: Any) -> str:
    require(isinstance(key, list) and len(key) == 3, "target key shape")
    m, blocks, can4 = key
    require(type(m) is int and isinstance(blocks, list) and len(blocks) == 3,
            "target key mode/blocks shape")
    require(all(isinstance(x, list) and len(x) == 2 and
                all(type(y) is int for y in x) for x in blocks),
            "target key D9 shape")
    require(isinstance(can4, list) and len(can4) == 9 and
            all(type(x) is int for x in can4), "target key PSL shape")
    flat = [x for block in blocks for x in block]
    return "(" + str(m) + ";" + ",".join(map(str, flat)) + ";" + \
        ",".join(map(str, can4)) + ")"


def parse_stage2_rho(stage2_path: Path) -> dict[str, Any]:
    """Re-derive rho from the source, rather than trusting JSON metadata.

    The parser accepts only the current six labels and current sphere rows.
    It deliberately recognizes the inverse product as a reversed signed word;
    this catches the historical ``[-3,-5,-6]`` metadata typo.
    """
    raw = stage2_path.read_bytes()
    require(file_digest(stage2_path) == STAGE2_SHA, "stage2 source digest drift")
    text = raw.decode("utf-8")
    m = re.search(r"gensPB4\s*:=\s*\[([^]]+)\]", text)
    require(m is not None, "stage2 generator-order line missing")
    labels = tuple(x.strip() for x in m.group(1).split(","))
    require(labels == F6_LABELS, "stage2 marked F6 label/order drift")

    # Parse the four sphere rows.  The right hand side is a product of named
    # PB4 generators followed by ^-1.  Parsing this expression is enough to
    # recover the signed free word independently of the frozen rho JSON.
    token_to_word = {name: [i + 1] for i, name in enumerate(F6_LABELS)}
    token_to_word.update({"k" + name: [i + 1]
                          for i, name in enumerate(F6_LABELS)})
    sphere: dict[str, list[int]] = {}
    for name in ("x15", "x25", "x35", "x45"):
        pat = rf"{name}\s*:=\s*\(([^)]*)\)\^\s*-1\s*;;"
        mm = re.search(pat, text)
        require(mm is not None, f"stage2 sphere row missing: {name}")
        factors = [x.strip() for x in mm.group(1).split("*") if x.strip()]
        require(factors and all(x in token_to_word for x in factors),
                f"stage2 sphere factors drift: {name}")
        expanded = [token_to_word[x][0] for x in factors]
        sphere[name] = inverse_word(expanded)

    require(sphere["x15"] == [-3, -2, -1], "x15 sphere/Hurwitz row drift")
    require(sphere["x25"] == [-5, -4, -1], "x25 sphere/Hurwitz row drift")
    require(sphere["x45"] == [-6, -5, -3], "x45 sphere/Hurwitz row drift")

    # The six unordered pairs are shifted by +3 modulo 5.  Reconstruct the
    # corresponding target word from the sphere dictionary and labels.
    pair_to_word: dict[tuple[int, int], list[int]] = {
        pair: [i + 1] for i, pair in enumerate(F6_PAIRS)
    }
    pair_to_word[(1, 5)] = sphere["x15"]
    pair_to_word[(2, 5)] = sphere["x25"]
    pair_to_word[(3, 5)] = sphere["x35"]
    pair_to_word[(4, 5)] = sphere["x45"]

    def shift(pair: tuple[int, int]) -> tuple[int, int]:
        values = tuple(((x - 1 + 3) % 5) + 1 for x in pair)
        return tuple(sorted(values))  # x_ji=x_ij

    shifted_pairs = tuple(shift(pair) for pair in F6_PAIRS)
    derived = tuple(tuple(pair_to_word[p]) for p in shifted_pairs)
    require(derived == RHO, "Hurwitz shift does not derive current rho")

    rm = re.search(r"rhoImages\s*:=\s*\[([^]]+)\]", text)
    require(rm is not None, "stage2 rhoImages line missing")
    source_tokens = tuple(x.strip() for x in rm.group(1).split(","))
    token_words: dict[str, list[int]] = {
        "x45": sphere["x45"], "kX14": [3], "kX24": [5],
        "x15": sphere["x15"], "x25": sphere["x25"], "kX12": [1],
    }
    require(tuple(tuple(token_words[x]) for x in source_tokens) == RHO,
            "stage2 rhoImages does not equal derived rho")
    require("rho(x_ij) = x_{i+3,j+3}" in text,
            "stage2 Hurwitz-shift comment missing")
    require("x_{i,5} := (x_{i,1} x_{i,2} x_{i,3} x_{i,4})^-1" in text,
            "stage2 sphere/Hurwitz convention missing")
    return {
        "status": "PROVED",
        "source_sha256": STAGE2_SHA,
        "generator_labels": list(labels),
        "generator_pairs": [list(x) for x in F6_PAIRS],
        "shifted_pairs": [list(x) for x in shifted_pairs],
        "sphere_rows": {k: list(v) for k, v in sphere.items()},
        "source_rho_tokens": list(source_tokens),
        "derived_rho_words": [list(x) for x in derived],
        "legacy_rho_rejected": True,
    }


def tail_layout(relators: Sequence[Sequence[int]]) -> dict[str, Any]:
    require(len(relators) == 158, "158 relator count drift")
    seeds = [list(x) for x in relators[18:46]]
    require(len(seeds) == 28, "28 seed count drift")
    matches: list[bool] = []
    for power in range(5):
        expected = [list(x) for x in seeds]
        for _ in range(power):
            expected = [rho_word(x) for x in expected]
        actual = [list(x) for x in relators[18 + 28 * power:18 + 28 * (power + 1)]]
        matches.append(actual == expected)
    return {
        "status": "PROVED" if all(matches) else "FAIL",
        "prefix_count": 18,
        "seed_count": 28,
        "block_count": 5,
        "block_match": matches,
        "blocks": [[list(x) for x in relators[18 + 28 * p:18 + 28 * (p + 1)]]
                   for p in range(5)],
    }


def load_canonical(input_path: Path, words_path: Path,
                   stage2_path: Path = DEFAULT_STAGE2) -> dict[str, Any]:
    require(file_digest(input_path) == SOURCE_SHA, "canonical source SHA drift")
    source = json.loads(input_path.read_text(encoding="utf-8"))
    require(source.get("schema") == "d972-b4-p2-magnus-input/v2",
            "canonical input schema drift")
    rels = [signed_word(x, 6, f"relator[{i}]")
            for i, x in enumerate(source.get("all_relators", []))]
    require(len(rels) == 158 and source.get("relator_count") == 158,
            "canonical 158 count drift")
    stage2_facts = parse_stage2_rho(stage2_path)
    require(source.get("rho_words") == stage2_facts["derived_rho_words"],
            "canonical rho is not source-derived current rho")
    require(digest(rels) == RELATOR_SHA and
            source.get("all_relators_sha256") == RELATOR_SHA,
            "canonical relator digest drift")
    tail = tail_layout(rels)
    require(tail["status"] == "PROVED", "canonical tail orbit layout drift")

    require(file_digest(words_path) == WORDS_SHA, "word artifact SHA drift")
    words = json.loads(words_path.read_text(encoding="utf-8"))
    require(words.get("schema") == "d972-b4-word-key-artifact/v1" and
            words.get("count") == 972, "word artifact schema/count drift")
    require(words.get("source_target_key_digest") == TARGET_SHA and
            words.get("frozen_tuple_sha256") == TUPLE_SHA,
            "word artifact target pin drift")
    rows = words.get("rows")
    require(isinstance(rows, list) and len(rows) == 972, "word artifact rows drift")
    roof: list[list[int]] = []
    keys: list[str] = []
    normalized: list[list[Any]] = []
    for i, row in enumerate(rows):
        require(isinstance(row, list) and len(row) == 3,
                f"word artifact row {i} shape drift")
        m, key, word = row
        require(type(m) is int and isinstance(key, list),
                f"word artifact row {i} mode/key drift")
        fw = [] if word == "" else signed_word(word, 2, f"word[{i}]")
        require(word == "" or isinstance(word, list), f"word[{i}] type drift")
        flat = key_string(key)
        require(flat.startswith("(" + str(m) + ";"), f"word/key row {i} mismatch")
        roof.append(fw)
        keys.append(flat)
        normalized.append([m, key, fw])
    require(digest(normalized) == ROWS_SHA and
            words.get("canonical_bytes_sha256") == ROWS_SHA,
            "word artifact canonical digest drift")
    require(source.get("roof_words") == roof and
            source.get("roof_words_sha256") == ROOF_SHA and
            digest(roof) == ROOF_SHA, "canonical roof/artifact binding drift")
    require(source.get("target_keys") == keys and len(set(keys)) == 972,
            "canonical key row-order/uniqueness drift")
    key_digest = hashlib.sha256(("\n".join(sorted(keys)) + "\n").encode()).hexdigest()
    require(key_digest == TARGET_SHA and source.get("target_key_digest") == TARGET_SHA,
            "canonical target digest drift")
    groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for i, word in enumerate(roof):
        groups[tuple(word)].append(i)
    require(len(groups) == 486 and Counter(map(len, groups.values())) == Counter({2: 486}),
            "canonical duplicate map drift")
    duplicate_map = [v for _, v in sorted(groups.items())]
    norms = [exact_norm(w) for w in roof]
    require(digest(norms) == NORM_SHA, "canonical norm digest drift")
    return {
        "source_sha256": SOURCE_SHA,
        "word_artifact_sha256": WORDS_SHA,
        "relator_sha256": RELATOR_SHA,
        "roof_sha256": ROOF_SHA,
        "target_sha256": TARGET_SHA,
        "norm_sha256": NORM_SHA,
        "relators": rels,
        "roof_words": roof,
        "target_keys": keys,
        "duplicate_map": duplicate_map,
        "norms": norms,
        "tail": tail,
        "stage2": stage2_facts,
    }


def resolve_certificate(receipt_path: Path, requested: Any) -> Path | None:
    if not isinstance(requested, str) or not requested:
        return None
    candidate = Path(requested)
    if candidate.is_file():
        return candidate.resolve()
    sibling = receipt_path.parent / candidate.name
    if sibling.is_file():
        return sibling.resolve()
    # GHA download can flatten artifact directories; basename fallback is
    # deliberately restricted to the receipt's directory.
    for path in receipt_path.parent.glob(candidate.name):
        if path.is_file():
            return path.resolve()
    return None


def require_raw_certificate(receipt: dict[str, Any], receipt_path: Path) -> tuple[dict[str, Any], Path]:
    cert_ref = receipt.get("certificate_path")
    cert_path = resolve_certificate(receipt_path, cert_ref)
    require(cert_path is not None, "raw typed certificate file is missing")
    raw = cert_path.read_bytes()
    declared = receipt.get("certificate_sha256")
    require(isinstance(declared, str) and len(declared) == 64 and
            hashlib.sha256(raw).hexdigest() == declared,
            "raw certificate bytes are not receipt-bound")
    cert = json.loads(raw.decode("utf-8"))
    require(cert.get("schema") == "d972-b4-typed-bundle-certificate/v2",
            "raw certificate schema drift")
    require(cert.get("source_sha256") == SOURCE_SHA,
            "raw certificate source pin drift")
    require(cert.get("word_artifact_sha256") == WORDS_SHA and
            cert.get("word_rows_sha256") == ROWS_SHA,
            "raw certificate word/key artifact pins drift")
    require(cert.get("stage2_sha256") == STAGE2_SHA and
            cert.get("worker_sha256") == WORKER_SHA,
            "raw certificate authoritative source pins drift")
    return cert, cert_path


def validate_signed_rows(value: Any, count: int, width: int, label: str) -> list[list[int]]:
    require(isinstance(value, list) and len(value) == count, f"{label} count drift")
    return [signed_word(row, width, f"{label}[{i}]") for i, row in enumerate(value)]


def substitute_f2_word(word: Sequence[int], a: Sequence[int],
                       b: Sequence[int]) -> list[int]:
    out: list[int] = []
    for raw in word:
        image = list(a if abs(int(raw)) == 1 else b)
        out.extend(inverse_word(image) if int(raw) < 0 else image)
    return reduce_word(out)


def validate_permutation(p: Any, degree: int, label: str) -> tuple[int, ...]:
    require(isinstance(p, list) and len(p) == degree, f"{label} degree drift")
    out = tuple(int(x) for x in p)
    require(sorted(out) == list(range(1, degree + 1)), f"{label} is not a permutation")
    return out


def validate_m_binding(cert: dict[str, Any]) -> dict[str, Any]:
    obj = cert.get("m_binding")
    require(isinstance(obj, dict), "M binding certificate missing")
    # A digest or a declared order is not a certificate.  Require raw images
    # for both marked generators on both actual component permutation sets.
    components = obj.get("components")
    require(isinstance(components, list) and len(components) == 2,
            "M component certificate must contain K9 and N_S4")
    names = {str(x.get("name")) for x in components if isinstance(x, dict)}
    require(names == {"K9", "N_S4"}, "M component names are not K9/N_S4")
    combined_degree = obj.get("combined_degree")
    require(combined_degree == 20520,
            "combined marked image degree missing")
    combined_images = obj.get("combined_generator_images")
    require(isinstance(combined_images, list) and len(combined_images) == 2,
            "combined marked generator images missing")
    combined_perms = [list(validate_permutation(p, combined_degree,
                                                 f"combined.image[{i}]"))
                      for i, p in enumerate(combined_images)]
    require(obj.get("combined_order") == 8817984 and
            obj.get("combined_pure_kernel_order") == 1469664,
            "combined finite marked image/kernel order drift")
    require(obj.get("epsilon_generator_images") == [[2, 1, 3], [1, 3, 2]],
            "combined epsilon marking drift")
    component_facts: dict[str, Any] = {}
    for comp in components:
        require(isinstance(comp, dict), "M component row shape")
        name = str(comp.get("name"))
        degree = comp.get("degree")
        images = comp.get("generator_images")
        expected_degree = {"K9": 17496, "N_S4": 3024}[name]
        require(degree == expected_degree, f"{name} component degree drift")
        require(isinstance(images, list) and len(images) == 2,
                f"{name} raw marked images missing")
        perms = [list(validate_permutation(p, degree, f"{name}.image[{i}]"))
                 for i, p in enumerate(images)]
        component_facts[name] = {"degree": degree, "generator_images": perms,
                                 "order": comp.get("order"),
                                 "kernel_order": comp.get("kernel_order"),
                                 "source_definition": comp.get("source_definition")}
        require(comp.get("raw_image_certificate") is True,
                f"{name} raw image certificate flag missing")
        require(type(comp.get("kernel_order")) is int and
                comp.get("kernel_order") > 0,
                f"{name} component kernel order missing")
    for i in range(2):
        expected_combined = component_facts["K9"]["generator_images"][i] + [
            x + 17496 for x in component_facts["N_S4"]["generator_images"][i]]
        require(combined_perms[i] == expected_combined,
                f"combined image {i} is not the recorded K9/N_S4 direct sum")
    require(obj.get("intersection_definition") == "M=K^(9) intersect N_S4",
            "M intersection definition is not exact")
    require(obj.get("marked_generators") == ["s1", "s2"],
            "M marked generator binding missing")
    require("B4_stable" not in obj and "b4_core" not in obj,
            "M binding incorrectly mixes a PB4/B4 core field")
    require(obj.get("b3_normality_certificate") ==
            "PROVED_FINITE_EPSILON_KERNEL",
            "B3 marked-kernel normality certificate is missing")
    require(obj.get("kernel_certificate") ==
            "PROVED_NAMED_INTERSECTION",
            "M named intersection is not proved")
    return {"status": "PROVED", "components": component_facts,
            "combined_degree": combined_degree,
            "combined_generator_images": combined_perms,
            "intersection": obj.get("intersection_definition")}


def validate_cofaces(cert: dict[str, Any], canonical: dict[str, Any]) -> dict[str, Any]:
    obj = cert.get("cofaces")
    require(isinstance(obj, dict), "coface certificate missing")
    blocks = obj.get("blocks")
    require(isinstance(blocks, list) and len(blocks) == 5,
            "coface raw block count drift")
    normalized = [[signed_word(row, 6, f"coface[{p}][{i}]")
                   for i, row in enumerate(block)] for p, block in enumerate(blocks)]
    expected = canonical["tail"]["blocks"]
    require(normalized == expected, "coface blocks do not exactly equal canonical 28x5 tail")
    require(obj.get("block_order") == [0, 1, 2, 3, 4],
            "coface block order is not current rho order")
    maps = obj.get("a18_maps")
    require(isinstance(maps, list) and len(maps) == 5,
            "A.18 map rows missing")
    names = [x.get("name") for x in maps if isinstance(x, dict)]
    require(names == ["123", "234", "12,3,4", "1,23,4", "1,2,34"],
            "A.18 coface names/order drift")
    expected_maps = {
        "123": [[1], [4]],
        "234": [[4], [6]],
        "12,3,4": [[2, 4], [6]],
        "1,23,4": [[1, 2], [5, 6]],
        "1,2,34": [[1], [4, 5]],
    }
    block_indices_seen: list[int] = []
    for row in maps:
        require(isinstance(row, dict), "A.18 row shape")
        name = row.get("name")
        require(row.get("f6_substitution") == expected_maps.get(name),
                f"A.18 substitution drift for {name}")
        require(type(row.get("raw_word_replay")) is bool and
                row.get("raw_word_replay") is True,
                f"A.18 raw replay missing for {name}")
        candidate_rows = validate_signed_rows(row.get("candidate_rows"), 28, 6,
                                             f"A.18[{name}] candidate rows")
        expected_candidates = [substitute_f2_word(seed,
                            expected_maps[name][0], expected_maps[name][1])
                               for seed in canonical["relators"][18:46]]
        require(candidate_rows == expected_candidates,
                f"A.18 raw substitution rows drift for {name}")
        block_indices = row.get("block_indices")
        require(isinstance(block_indices, list) and len(block_indices) == 1 and
                type(block_indices[0]) is int and 0 <= block_indices[0] < 5,
                f"A.18 block index missing for {name}")
        block_indices_seen.append(block_indices[0])
        equal_rows = row.get("group_equal_rows")
        require(isinstance(equal_rows, list) and len(equal_rows) == 28 and
                all(x is True for x in equal_rows),
                f"A.18 group replay rows missing for {name}")
    require(sorted(block_indices_seen) == [0, 1, 2, 3, 4],
            "A.18 block matches are not a complete permutation")
    require(obj.get("a18_to_block_certificate") == "PROVED",
            "A.18-to-tail block identification is not PROVED")
    return {"status": "PROVED", "blocks": normalized, "a18_maps": maps}


def validate_k05(cert: dict[str, Any], canonical: dict[str, Any]) -> dict[str, Any]:
    obj = cert.get("k05")
    require(isinstance(obj, dict), "K05 certificate missing")
    rows = validate_signed_rows(obj.get("relator_rows"), 18, 6, "K05 relators")
    require(rows == canonical["relators"][:18],
            "K05 18 raw rows do not equal canonical direct prefix")
    rho_replay = obj.get("rho_relator_replay")
    require(isinstance(rho_replay, list) and len(rho_replay) == 18,
            "K05 per-relator rho replay rows missing")
    for i, row in enumerate(rho_replay):
        require(isinstance(row, dict) and row.get("relator") == rows[i],
                f"K05 rho replay row {i} not raw-bound")
        require(row.get("identity_at_all_powers") is True and
                row.get("power_count") == 5,
                f"K05 rho replay row {i} not complete")
    gen_rows = obj.get("rho5_generator_replay")
    require(isinstance(gen_rows, list) and len(gen_rows) == 6,
            "K05 rho5 generator replay missing")
    for i, row in enumerate(gen_rows):
        require(isinstance(row, dict) and row.get("generator_index") == i + 1 and
                row.get("identity_after_five") is True,
                f"K05 rho5 generator row {i} invalid")
    require(obj.get("rho_relator_bad") == 0 and obj.get("rho5") is True and
            obj.get("rho_nonidentity") is True and
            obj.get("group_internal_certificate") == "PROVED",
            "K05 group-internal rho certificate is incomplete")
    return {"status": "PROVED", "relator_rows": rows}


def validate_q0(cert: dict[str, Any], canonical: dict[str, Any]) -> dict[str, Any]:
    obj = cert.get("q0")
    require(isinstance(obj, dict) and obj.get("marked_generators") == ["s1^2", "s2^2"],
            "marked Q0 certificate missing")
    rows = validate_signed_rows(obj.get("relator_rows"), 28, 6, "Q0 relators")
    # Q0 rows are F2 rows in the direct canonical artifact, not arbitrary
    # relators from a newly simplified GAP presentation.
    require(rows == [list(x) for x in canonical["relators"][18:46]],
            "Q0 28 rows are not the canonical marked seeds")
    bits = obj.get("image_identity")
    require(isinstance(bits, list) and bits == [True] * 28 and
            obj.get("image_certificate") == "PROVED",
            "Q0 28-row marked image replay is incomplete")
    return {"status": "PROVED", "relator_count": 28}


def validate_presentation(cert: dict[str, Any], canonical: dict[str, Any]) -> dict[str, Any]:
    obj = cert.get("presentation")
    require(isinstance(obj, dict), "direct presentation certificate missing")
    require(obj.get("mode") == "direct_F6_158",
            "presentation is not direct F6/158")
    require(obj.get("generator_labels") == list(F6_LABELS),
            "direct marked F6 labels drift")
    rows = validate_signed_rows(obj.get("relator_rows"), 158, 6, "direct relators")
    require(rows == canonical["relators"], "direct raw rows do not equal canonical 158")
    require(obj.get("source_sha256") == SOURCE_SHA and
            obj.get("all_relators_sha256") == RELATOR_SHA,
            "direct presentation source/digest binding missing")
    require(obj.get("rho_words") == [list(x) for x in RHO],
            "direct presentation rho drift")
    require(obj.get("rho_derivation") == "stage2_sphere_hurwitz_independent",
            "direct presentation rho provenance missing")
    return {"status": "PROVED", "mode": obj["mode"]}


def validate_fibers(cert: dict[str, Any], canonical: dict[str, Any]) -> dict[str, Any]:
    obj = cert.get("fibers")
    require(isinstance(obj, dict), "fiber certificate missing")
    rows = obj.get("rows")
    require(isinstance(rows, list) and len(rows) == 972,
            "fiber raw row count is not 972")
    expected = list(zip(canonical["target_keys"], canonical["roof_words"]))
    seen: set[tuple[int, tuple[int, ...], str]] = set()
    settled = onto = cond_i = cond_ii = 0
    arithmetic = outside = 0
    for i, row in enumerate(rows):
        require(isinstance(row, dict) and row.get("index") == i + 1,
                f"fiber row {i} index drift")
        word = signed_word(row.get("f2_word"), 2, f"fiber[{i}].f2_word")
        key = str(row.get("target_key"))
        require((key, word) == expected[i], f"fiber row {i} is not canonical typed word/key")
        require(type(row.get("m")) is int and key.startswith("(" + str(row["m"]) + ";"),
                f"fiber row {i} m/key binding drift")
        # The booleans below must be tied to raw replay subobjects, not only
        # to a producer aggregate.  The checker still does not call GAP; it
        # verifies that every claimed fact has its per-row witness structure.
        for field in ("settled", "onto", "condition_I", "condition_II",
                      "charming", "arithmetic", "outside"):
            require(type(row.get(field)) is bool, f"fiber row {i} missing {field}")
        require(isinstance(row.get("proof"), dict), f"fiber row {i} proof missing")
        proof = row["proof"]
        require(proof.get("source_key") == key and
                proof.get("source_word") == word and
                proof.get("raw_replay") is True,
                f"fiber row {i} proof is not raw-bound")
        require(isinstance(proof.get("settled_replay"), dict) and
                isinstance(proof.get("onto_replay"), dict) and
                isinstance(proof.get("condition_replay"), dict),
                f"fiber row {i} replay subcertificates missing")
        settled_replay = proof["settled_replay"]
        onto_replay = proof["onto_replay"]
        condition_replay = proof["condition_replay"]
        require(settled_replay.get("value") == row["settled"],
                f"fiber row {i} settled replay mismatch")
        require(onto_replay.get("value") is True and
                onto_replay.get("image_order") == 8817984 and
                onto_replay.get("target_order") == 8817984 and
                onto_replay.get("raw_generator_replay") is True,
                f"fiber row {i} onto replay is not raw finite-image data")
        require(condition_replay.get("I") is True and
                condition_replay.get("II") is True and
                condition_replay.get("theta_equation") is True and
                condition_replay.get("tau_equation") is True and
                condition_replay.get("literal_equations") is True and
                condition_replay.get("raw_equation_replay") is True,
                f"fiber row {i} condition replay is incomplete")
        seen.add((row["m"], tuple(word), key))
        settled += int(row["settled"])
        onto += int(row["onto"])
        cond_i += int(row["condition_I"])
        cond_ii += int(row["condition_II"])
        arithmetic += int(row["arithmetic"])
        outside += int(row["outside"])
    require(len(seen) == 972, "fiber rows are not unique")
    require(obj.get("settled_count") == settled == 972,
            "settled_count is not 972")
    require(obj.get("onto_count") == onto == 972 and
            obj.get("condition_I_count") == cond_i == 972 and
            obj.get("condition_II_count") == cond_ii == 972,
            "fiber onto/condition counts are incomplete")
    require(obj.get("arithmetic_count") == arithmetic and
            obj.get("outside_count") == outside and
            obj.get("classification_certificate") == "PROVED",
            "arithmetic/outside classification is not raw-certified")
    require(obj.get("source_full_fiber") is True and
            obj.get("target_full_fiber") is True and
            obj.get("duplicate_map_exact") is True and
            obj.get("onto") is True,
            "full 972 fiber completeness gate is incomplete")
    return {"status": "PROVED", "count": 972, "settled_count": settled,
            "arithmetic_count": arithmetic, "outside_count": outside}


def validate_dtilde(cert: dict[str, Any], canonical: dict[str, Any]) -> dict[str, Any]:
    obj = cert.get("dtilde")
    require(isinstance(obj, dict), "Dtilde certificate missing")
    rows = obj.get("rows")
    require(isinstance(rows, list) and len(rows) == 972,
            "Dtilde row count drift")
    for i, row in enumerate(rows):
        require(isinstance(row, dict) and row.get("index") == i + 1,
                f"Dtilde row {i} index drift")
        require(row.get("source_word") == canonical["roof_words"][i],
                f"Dtilde row {i} source word drift")
        require(row.get("formula") ==
                "f(x45,x34)^-1*f(x12,x15)^-1*f(x23,x34)*f(x45,x51)*f(x12,x23)",
                f"Dtilde row {i} formula drift")
        require(type(row.get("dtilde_identity")) is bool and
                type(row.get("norm_identity")) is bool and
                type(row.get("equal_in_K05")) is bool,
                f"Dtilde row {i} replay flags missing")
        require(row.get("raw_replay") is True, f"Dtilde row {i} raw replay missing")
    require(obj.get("formula_source") == "PENT-FORM-prime-docs-notes-b4_direct_adjudication_feasibility_v1_2:155-165",
            "Dtilde formula provenance drift")
    require(obj.get("all_rows_raw_replayed") is True and
            obj.get("equal_count") == 972 and
            obj.get("equality_certificate") == "PROVED",
            "Dtilde/norm equality is not complete")
    return {"status": "PROVED", "count": 972,
            "equal_count": obj.get("equal_count")}


def validate_core(cert: dict[str, Any]) -> dict[str, Any]:
    obj = cert.get("b4_s4_core")
    require(isinstance(obj, dict), "B4/S4 core certificate missing")
    require(obj.get("status") == "PROVED" and
            obj.get("normality") is True and
            obj.get("B4_stable") is True and
            obj.get("S4_core_complete") is True,
            "B4/S4 normal core gate incomplete")
    conjugates = obj.get("conjugate_rows")
    require(isinstance(conjugates, list) and len(conjugates) > 0,
            "B4/S4 conjugate raw rows missing")
    for i, row in enumerate(conjugates):
        require(isinstance(row, dict) and row.get("raw_replay") is True,
                f"B4/S4 conjugate row {i} is not raw-certified")
    return {"status": "PROVED", "conjugate_count": len(conjugates)}


def validate_receipt(receipt: dict[str, Any], canonical: dict[str, Any],
                     cert: dict[str, Any]) -> dict[str, Any]:
    require(receipt.get("schema") == "d972-b4-typed-bundle/v2",
            "typed bundle schema drift")
    require(receipt.get("terminal_claim") is False,
            "typed bundle must not make an A/B terminal claim")
    require(receipt.get("presentation_source_sha256") == SOURCE_SHA,
            "receipt presentation source pin drift")
    require(receipt.get("canonical_relator_sha256") == RELATOR_SHA and
            receipt.get("target_key_digest") == TARGET_SHA and
            receipt.get("word_artifact_sha256") == WORDS_SHA and
            receipt.get("word_rows_sha256") == ROWS_SHA,
            "receipt canonical pin drift")
    require(receipt.get("rho_words") == [list(x) for x in RHO],
            "receipt rho drift")
    # The raw certificate is the load-bearing object.  Every successful gate
    # below is recomputed from its rows and current canonical input.
    presentation = validate_presentation(cert, canonical)
    k05 = validate_k05(cert, canonical)
    q0 = validate_q0(cert, canonical)
    m = validate_m_binding(cert)
    cofaces = validate_cofaces(cert, canonical)
    fibers = validate_fibers(cert, canonical)
    dtilde = validate_dtilde(cert, canonical)
    core = validate_core(cert)
    return {"presentation": presentation, "k05": k05, "q0": q0, "m": m,
            "cofaces": cofaces, "fibers": fibers, "dtilde": dtilde,
            "core": core}


def selftest() -> None:
    require(reduce_word([1, -1, 2, 2, -2]) == [2], "free reduction selftest")
    require(rho_word([]) == [] and exact_norm([]) == [], "empty-word selftest")
    facts = parse_stage2_rho(DEFAULT_STAGE2)
    require(facts["status"] == "PROVED" and facts["legacy_rho_rejected"],
            "source rho selftest")
    require(tuple(tuple(x) for x in facts["derived_rho_words"]) == RHO,
            "current rho derivation selftest")
    require(tuple(tuple(x) for x in LEGACY_RHO) != RHO,
            "legacy rho must differ")
    toy = {"schema": "d972-b4-typed-bundle/v2", "terminal_claim": False,
           "presentation_source_sha256": SOURCE_SHA,
           "canonical_relator_sha256": RELATOR_SHA,
           "target_key_digest": TARGET_SHA,
           "rho_words": [list(x) for x in RHO]}
    try:
        validate_receipt(toy, {}, {})
    except (TypeError, ValueError, KeyError):
        pass
    else:
        raise AssertionError("incomplete toy typed receipt was accepted")
    print("D972_B4_TYPED_BUNDLE_V2_SELFTEST_PASS")


def run(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    ap.add_argument("--word-artifact", type=Path, default=DEFAULT_WORDS)
    ap.add_argument("--stage2", type=Path, default=DEFAULT_STAGE2)
    ap.add_argument("--receipt", type=Path, required=False)
    ap.add_argument("--certificate", type=Path, required=False)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    result: dict[str, Any]
    try:
        canonical = load_canonical(args.input.resolve(), args.word_artifact.resolve(),
                                   args.stage2.resolve())
        require(args.receipt is not None, "--receipt is required")
        receipt_path = args.receipt.resolve()
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        cert_ref = args.certificate if args.certificate is not None else receipt.get("certificate_path")
        if args.certificate is not None:
            receipt = dict(receipt)
            receipt["certificate_path"] = str(args.certificate)
        cert, cert_path = require_raw_certificate(receipt, receipt_path)
        gates = validate_receipt(receipt, canonical, cert)
        result = {
            "schema": "d972-b4-typed-bundle-independent-check/v2",
            "status": "LOCAL_TYPED_RECEIPT_CROSSCHECKED",
            "terminal_claim": False,
            "receipt_sha256": file_digest(receipt_path),
            "certificate_sha256": file_digest(cert_path),
            "gates": gates,
            "global_survival": "UNKNOWN",
            "note": "This is a typed local receipt only; no B4-A/B/Ihara promotion is emitted.",
        }
        code = 0
    except (OSError, TypeError, ValueError, KeyError, IndexError,
            json.JSONDecodeError, AssertionError) as exc:
        result = {
            "schema": "d972-b4-typed-bundle-independent-check/v2",
            "status": "UNKNOWN_TYPED_BUNDLE",
            "terminal_claim": False,
            "reason": str(exc),
            "global_survival": "UNKNOWN",
        }
        code = 2
    if args.output:
        args.output.resolve().parent.mkdir(parents=True, exist_ok=True)
        args.output.resolve().write_text(json.dumps(result, sort_keys=True, indent=2) + "\n",
                                         encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(run())
