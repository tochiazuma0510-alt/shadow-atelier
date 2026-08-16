"""Build and audit an independent row fixture for the A.18 D-tilde lane.

This helper is intentionally standalone: it does not import the production
checker or any GAP-facing code.  The generated fixture contains the expected
canonical final word and its row digest for all 972 rows.  The GAP diagnostic
reconstructs those rows independently and fails closed at the first mismatch.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "search/certs/d972_b4_p2_magnus_input_v2_20260816.json"
WORDS_PATH = ROOT / "search/certs/d972_b4_word_key_artifact_v1_20260816.json"
DEFAULT_FIXTURE = ROOT / "search/certs/d972_b4_a18_finite_dtilde_rows_fixture_v1_20260817.json"

SOURCE_SHA = "c61b2b77131127aca83a8d7c56b7fdadd2d519b040ea4d91093622c813c2b4a9"
WORDS_SHA = "564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9"
DTILDE_SHA = "32cdc85b315817e939feca628bc15235a55664157ca1e272815a53f1de4631ef"
SCHEMA = "d972-b4-a18-finite-dtilde-rows-fixture/v1"
FIXTURE_MAX_BYTES = 2_000_000
FIXTURE_SHA = "aab097b31c2e4a85aab28c6ebb5f3853d7b5b99ef4eb8b331a1faf6626d4bfa6"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def cjson(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(cjson(value)).hexdigest()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def free_reduce(word: Iterable[int]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(isinstance(letter, int) and not isinstance(letter, bool) and letter != 0,
                "signed word drift")
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return out


def inverse_word(word: Iterable[int]) -> list[int]:
    return [-x for x in reversed(list(word))]


def marked_substitute(word: list[int], first: tuple[int, ...],
                      second: tuple[int, ...]) -> list[int]:
    out: list[int] = []
    for letter in word:
        require(abs(letter) in (1, 4), "marked alphabet drift")
        image = first if abs(letter) == 1 else second
        out.extend(inverse_word(image) if letter < 0 else image)
    return free_reduce(out)


def exact_dtilde(f2_word: list[int]) -> list[int]:
    marked: list[int] = []
    for letter in f2_word:
        require(abs(letter) in (1, 2), "roof alphabet drift")
        if abs(letter) == 1:
            marked.append(1 if letter > 0 else -1)
        else:
            marked.append(4 if letter > 0 else -4)
    x15 = (-3, -2, -1)
    x45 = (-6, -5, -3)
    return free_reduce(
        inverse_word(marked_substitute(marked, x45, (6,)))
        + inverse_word(marked_substitute(marked, (1,), x15))
        + marked_substitute(marked, (4,), (6,))
        + marked_substitute(marked, x45, x15)
        + marked_substitute(marked, (1,), (4,))
    )


def load_words(input_path: Path, words_path: Path) -> list[list[int]]:
    require(file_sha(input_path) == SOURCE_SHA, "source SHA drift")
    source = json.loads(input_path.read_text(encoding="utf-8"))
    require(source.get("schema") == "d972-b4-p2-magnus-input/v2" and
            source.get("relator_count") == 158 and
            len(source.get("all_relators", [])) == 158 and
            source.get("all_relators_sha256") ==
            "12fc1146dce5179c2b5fc44a3ceed6356a6b2c4835a564b55e9a9cd679fccd2e",
            "source contract drift")
    require(file_sha(words_path) == WORDS_SHA, "word-artifact SHA drift")
    words = json.loads(words_path.read_text(encoding="utf-8"))
    require(words.get("schema") == "d972-b4-word-key-artifact/v1" and
            words.get("count") == 972 and len(words.get("rows", [])) == 972,
            "word-artifact contract drift")
    result: list[list[int]] = []
    for row in words["rows"]:
        require(isinstance(row, list) and len(row) == 3, "word row shape drift")
        value = [] if row[2] == "" else row[2]
        require(isinstance(value, list), "word row type drift")
        result.append([int(x) for x in value])
    return result


def build_fixture(input_path: Path, words_path: Path) -> dict[str, Any]:
    source_words = load_words(input_path, words_path)
    rows = []
    for index, source_word in enumerate(source_words, 1):
        final = exact_dtilde(source_word)
        rows.append({"index": index, "word": final, "sha256": digest(final)})
    final_words = [row["word"] for row in rows]
    require(digest(final_words) == DTILDE_SHA, "canonical D-tilde digest drift")
    return {
        "schema": SCHEMA,
        "source_sha256": SOURCE_SHA,
        "word_artifact_sha256": WORDS_SHA,
        "dtilde_sha256": DTILDE_SHA,
        "row_count": len(rows),
        "rows": rows,
    }


def check_fixture(path: Path, input_path: Path, words_path: Path) -> dict[str, Any]:
    fixture_raw = path.read_bytes()
    require(len(fixture_raw) <= FIXTURE_MAX_BYTES, "fixture exceeds bounded byte limit")
    require(hashlib.sha256(fixture_raw).hexdigest() == FIXTURE_SHA,
            "fixture byte SHA drift")
    fixture = json.loads(fixture_raw.decode("utf-8"))
    require(fixture.get("schema") == SCHEMA, "fixture schema drift")
    require(fixture.get("source_sha256") == SOURCE_SHA and
            fixture.get("word_artifact_sha256") == WORDS_SHA and
            fixture.get("dtilde_sha256") == DTILDE_SHA and
            fixture.get("row_count") == 972, "fixture pin drift")
    rows = fixture.get("rows")
    require(isinstance(rows, list) and len(rows) == 972, "fixture row count drift")
    for index, row in enumerate(rows, 1):
        require(isinstance(row, dict) and row.get("index") == index and
                isinstance(row.get("word"), list) and
                row.get("sha256") == digest(row["word"]),
                f"fixture row {index} digest drift")
    expected = build_fixture(input_path, words_path)
    require(expected["rows"] == rows, "independent Python fixture mismatch")
    require(digest([row["word"] for row in rows]) == DTILDE_SHA,
            "fixture final digest drift")
    return {
        "schema": SCHEMA,
        "fixture_sha256": hashlib.sha256(fixture_raw).hexdigest(),
        "source_sha256": SOURCE_SHA,
        "word_artifact_sha256": WORDS_SHA,
        "dtilde_sha256": DTILDE_SHA,
        "row_count": len(rows),
    }


def selftest(path: Path) -> None:
    result = check_fixture(path, INPUT_PATH, WORDS_PATH)
    require(result["row_count"] == 972, "selftest count drift")
    print("D972_B4_A18_FINITE_DIGEST_DIAG_PY_SELFTEST_PASS")
    print("D972_B4_A18_FINITE_DIGEST_DIAG_PY_FINAL_MARKER "
          f"status=PASS fixture={result['fixture_sha256']} dtilde={DTILDE_SHA}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--input", type=Path, default=INPUT_PATH)
    parser.add_argument("--words", type=Path, default=WORDS_PATH)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.generate:
        fixture = build_fixture(args.input, args.words)
        args.fixture.write_text(json.dumps(fixture, ensure_ascii=True,
                                            sort_keys=True, separators=(",", ":")) + "\n",
                                 encoding="utf-8")
    if args.selftest or args.generate:
        selftest(args.fixture)
        return 0
    result = check_fixture(args.fixture, args.input, args.words)
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
