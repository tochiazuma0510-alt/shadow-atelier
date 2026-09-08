"""Task1128: public P6 selftest packaging only; no parent intake."""
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import signal
import stat
import subprocess
import sys
import time
import uuid
import zipfile

STEM = "d972_r07_P6_public_selftest_gha_v1"
CLAIMS = {"mathematical_parent_admission": False, "full_run": False, "candidate": False, "cross_checked": False, "verified": False}


def need(value, label):
    if not value:
        raise ValueError("task1128:" + label)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("ascii")


def save(path, value):
    with path.open("xb") as stream:
        stream.write(canonical(value))
        stream.flush()
        os.fsync(stream.fileno())


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "duplicate-JSON-key:" + key)
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError("task1128:nonfinite-JSON:" + value)


def document(path):
    pin(path)
    return json.loads(path.read_bytes().decode("utf-8"),
                      object_pairs_hook=unique_pairs, parse_constant=invalid_constant)


def exact(value, keys, label):
    need(type(value) is dict and set(value) == set(keys), label + ":exact-keys")


def relative(value):
    need(type(value) is str and value and "\\" not in value and ":" not in value and
         all(ord(ch) >= 32 for ch in value), "relative-name")
    parts = value.split("/")
    need(not value.startswith("/") and all(x not in ("", ".", "..") for x in parts)
         and PurePosixPath(value).as_posix() == value, "relative-components")
    return value


def ordinary_path(path, directory=False):
    need(path.is_absolute(), "absolute-path")
    for parent in reversed(path.parents):
        need(stat.S_ISDIR(parent.lstat().st_mode), "ordinary-parent:" + str(parent))
    kind = path.lstat().st_mode
    need(stat.S_ISDIR(kind) if directory else stat.S_ISREG(kind),
         "ordinary-path:" + str(path))


def pin(path, copy_to=None):
    ordinary_path(path)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    with os.fdopen(os.open(path, flags), "rb") as source:
        before = os.fstat(source.fileno())
        need(stat.S_ISREG(before.st_mode), "regular-open-file:" + str(path))
        output = None if copy_to is None else copy_to.open("xb")
        digest = hashlib.sha256()
        size = 0
        try:
            while True:
                chunk = source.read(1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
                size += len(chunk)
                if output is not None:
                    output.write(chunk)
            if output is not None:
                output.flush()
                os.fsync(output.fileno())
        finally:
            if output is not None:
                output.close()
        after = os.fstat(source.fileno())
    end = path.lstat()
    identity = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    need(identity(before) == identity(after) == identity(end) and size == before.st_size,
         "file-changed-during-full-read:" + str(path))
    return {"bytes": size, "sha256": digest.hexdigest()}


def captured_source_path(capture, name):
    relative(name)
    mapped = "workflow/gap-run.yml" if name == ".github/workflows/gap-run.yml" else "repository/" + name
    need(all(not item.startswith(".") for item in mapped.split("/")), "nonhidden-source-copy-path")
    target = capture / relative(mapped)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def source_pins(repo, entries, capture=None):
    result = []
    for entry in entries:
        exact(entry, ("file", "bytes", "sha256"), "source-registration")
        name = relative(entry["file"])
        need(type(entry["bytes"]) is int and entry["bytes"] > 0 and
             type(entry["sha256"]) is str and len(entry["sha256"]) == 64 and
             all(ch in "0123456789abcdef" for ch in entry["sha256"]), "source-pin-types")
        target = None if capture is None else captured_source_path(capture, name)
        observed = {"file": name, **pin(repo / name, target)}
        need(observed == entry, "registered-whole-source:" + name)
        result.append(observed)
    return result


def source_copy_gate(out, entries, outer):
    root = out / "source-copy"
    observed = inventory(root)
    need(all(not part.startswith(".") for row in observed["files"]
             for part in row["file"].split("/")), "source-copy-all-files-nonhidden")
    save(out / "source-copy-inventory.json", observed)
    mapping = []
    expected_names = []
    for row in [*entries, *outer]:
        name = relative(row["file"])
        mapped = "workflow/gap-run.yml" if name == ".github/workflows/gap-run.yml" else "repository/" + name
        expected_names.append(mapped)
        copied = pin(root / mapped)
        need(copied == {key: row[key] for key in ("bytes", "sha256")}, "copied-source-whole-pin:" + name)
        mapping.append({"original": row, "artifact_file": "source-copy/" + mapped, "copy_pin": copied})
    need([row["file"] for row in observed["files"]] == sorted(expected_names), "all-seventeen-source-and-raw-copies")
    receipt = {"schema": "task1128.source-copy.v1", "status": "PASS_FULL_BYTES", "mappings": mapping,
               "hidden_artifact_source_paths": 0, "workflow_original_path": ".github/workflows/gap-run.yml",
               "workflow_artifact_file": "source-copy/workflow/gap-run.yml", "source_count": len(mapping)}
    save(out / "source-copy-receipt.json", receipt)
    return receipt



def inventory(root):
    ordinary_path(root, directory=True)
    files, directories, empty = [], [], []
    pending = [root]
    while pending:
        folder = pending.pop()
        ordinary_path(folder, directory=True)
        with os.scandir(folder) as stream:
            children = sorted(list(stream), key=lambda item: item.name)
        if not children:
            empty.append("." if folder == root else folder.relative_to(root).as_posix())
        for child in children:
            path = Path(child.path)
            name = relative(path.relative_to(root).as_posix())
            kind = path.lstat().st_mode
            if stat.S_ISDIR(kind):
                directories.append(name)
                pending.append(path)
            elif stat.S_ISREG(kind):
                files.append({"file": name, **pin(path)})
            else:
                raise ValueError("task1128:fixture-nonregular-entry:" + name)
    return {"files": sorted(files, key=lambda x: x["file"]),
            "directories": sorted(directories), "empty_directories": sorted(empty)}


def run(argv, label, timeout, repo, out, environment):
    start = time.monotonic()
    value = {"schema": "task1128.execution.v1", "label": label, "argv": argv,
             "cwd": str(repo), "started_utc": utc(), "finished_utc": None,
             "timeout_seconds": timeout, "timed_out": False, "returncode": None,
             "elapsed_seconds": None, "error": None, "pid": None,
             "stdout": label + ".stdout.bin", "stderr": label + ".stderr.bin"}
    save(out / (label + ".start.json"), value)
    try:
        with (out / value["stdout"]).open("xb") as stdout, (out / value["stderr"]).open("xb") as stderr:
            child = subprocess.Popen(argv, cwd=repo, env=environment, stdin=subprocess.DEVNULL,
                                     stdout=stdout, stderr=stderr, start_new_session=True)
            value["pid"] = child.pid
            try:
                value["returncode"] = child.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                value["timed_out"] = True
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                value["returncode"] = child.wait(timeout=30)
    except BaseException as exc:
        value["error"] = type(exc).__name__ + ":" + str(exc)
    finally:
        value["finished_utc"] = utc()
        value["elapsed_seconds"] = time.monotonic() - start
        for channel in ("stdout", "stderr"):
            path = out / value[channel]
            value[channel + "_pin"] = pin(path) if path.exists() else None
        save(out / (label + ".execution.json"), value)
    return value


def successful(execution):
    return execution["returncode"] == 0 and not execution["timed_out"] and execution["error"] is None

def preserve_fixture(root, out):
    before = inventory(root)
    save(out / "fixture-inventory-before.json", before)
    copied = out / "fixture-copy"
    copied.mkdir()
    (copied / "files").mkdir()
    mappings = []
    for index, row in enumerate(before["files"]):
        flat = "files/" + format(index, "06d") + ".bin"
        observed = pin(root / row["file"], copied / flat)
        need(observed == {key: row[key] for key in ("bytes", "sha256")}, "fixture-copy-bytes:" + row["file"])
        mappings.append({"original": row, "artifact_file": "fixture-copy/" + flat, "copy_pin": observed})
    copy_inventory = inventory(copied)
    expected_copy = [{"file": entry["artifact_file"].removeprefix("fixture-copy/"), **entry["copy_pin"]}
                     for entry in mappings]
    need(copy_inventory["files"] == expected_copy and inventory(root) == before, "full-flat-copy-source-equality")
    save(out / "fixture-copy-map.json", {"schema": "task1128.fixture-copy-map.v1", "files": mappings,
         "original_directories": before["directories"], "original_empty_directories": before["empty_directories"],
         "hidden_original_paths_preserved_in_explicit_ZIP": True, "flat_names_are_transport_only": True})
    archive = out / "selftest-fixtures.zip"
    names = ["fixtures/"] + ["fixtures/" + name + "/" for name in before["directories"]]
    names += ["fixtures/" + row["file"] for row in before["files"]]
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=6, allowZip64=True) as container:
        for name in names[:1 + len(before["directories"])]:
            entry = zipfile.ZipInfo(name)
            entry.create_system = 3
            entry.external_attr = ((stat.S_IFDIR | 0o700) << 16) | 0x10
            container.writestr(entry, b"")
        for mapping in mappings:
            entry = zipfile.ZipInfo("fixtures/" + mapping["original"]["file"])
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | 0o600) << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            with (out / mapping["artifact_file"]).open("rb") as source, container.open(entry, "w", force_zip64=True) as target:
                while True:
                    chunk = source.read(1024 * 1024)
                    if not chunk:
                        break
                    target.write(chunk)
    archive_before = pin(archive)
    rows = {"fixtures/" + row["file"]: row for row in before["files"]}
    with zipfile.ZipFile(archive, "r") as container:
        entries = container.infolist()
        need([entry.filename for entry in entries] == names and len(set(names)) == len(names),
             "ZIP-exact-all-entry-roster")
        for entry in entries:
            digest, size = hashlib.sha256(), 0
            with container.open(entry, "r") as stream:
                while True:
                    chunk = stream.read(1024 * 1024)
                    if not chunk:
                        break
                    digest.update(chunk)
                    size += len(chunk)
            mode = entry.external_attr >> 16
            if entry.filename not in rows:
                need(entry.is_dir() and stat.S_ISDIR(mode) and size == 0 and entry.file_size == 0,
                     "ZIP-directory-entry")
            else:
                row = rows[entry.filename]
                need(not entry.is_dir() and stat.S_ISREG(mode) and size == entry.file_size == row["bytes"] and
                     digest.hexdigest() == row["sha256"], "ZIP-full-file-EOF:" + entry.filename)
    after, copy_after = inventory(root), inventory(copied)
    save(out / "fixture-inventory-after.json", after)
    save(out / "fixture-copy-inventory.json", copy_after)
    need(before == after and copy_after == copy_inventory and archive_before == pin(archive),
         "fixture-after-archive-equality")
    result = {"schema": "task1128.fixture-preservation.v1", "status": "PASS_FULL_BYTES",
              "runtime_root": str(root), "copy_root": str(copied), "archive": archive.name,
              "archive_pin": archive_before, "file_count": len(before["files"]),
              "directory_count_excluding_root": len(before["directories"]),
              "empty_directories": before["empty_directories"], "ZIP_entry_count": len(names),
              "copy_layout": "ordinal flat files with original-name map; all original directories explicit in ZIP",
              "every_entry_read_to_EOF": True, "zipfile_CRC_checked_on_read": True,
              "independent_CRC_implementation": False, "complete_selftest_inferred": False}
    save(out / "fixture-preservation.json", result)
    return before, result



def public_descriptor(root, value, expected_name):
    exact(value, ("file", "bytes", "sha256"), "public-file-descriptor")
    need(type(value["file"]) is str and value["file"] == expected_name and
         type(value["bytes"]) is int and value["bytes"] >= 0 and
         type(value["sha256"]) is str and len(value["sha256"]) == 64 and
         all(ch in "0123456789abcdef" for ch in value["sha256"]), "public-descriptor-types-and-name")
    need(value == {"file": expected_name, **pin(root / relative(expected_name))}, "public-descriptor-full-file")
    return value


def selftest_gate(out, fixture, observed, wire):
    result = document(out / "producer.stdout.bin")
    wanted = wire["success_stdout"]
    exact(result, wanted["exact_top_keys"], "selftest-top")
    need(type(result["schema"]) is str and result["schema"] == wanted["schema"] and
         type(result["status"]) is str and result["status"] == "PASS", "selftest-schema-status")
    unsigned = {key: value for key, value in result.items() if key != "sha256"}
    need(type(result["sha256"]) is str and result["sha256"] == hashlib.sha256(canonical(unsigned)).hexdigest(),
         "selftest-inner-seal")
    need((out / "producer.stdout.bin").read_bytes() == canonical(result), "whole-canonical-stdout-and-final-LF")
    need(type(result["fixture_scope"]) is str and result["fixture_scope"] == wanted["fixture_scope"], "selftest-scope")
    need(type(result["old_success_suites"]) is int and result["old_success_suites"] == 0, "no-old-success-suite-replay")
    for field in wanted["false_fields"]:
        need(result[field] is False, "selftest-false-assurance:" + field)
    need(type(result["production_interfaces_used"]) is list and
         all(type(name) is str and name for name in result["production_interfaces_used"]) and
         result["production_interfaces_used"] == wanted["production_interfaces_used"], "public-interface-order")
    tests = result["tests"]
    need(type(tests) is list and len(tests) == 5, "five-selftest-groups")
    inspected = []
    for index, group in enumerate(tests):
        exact(group, wanted["group_exact_keys"], "selftest-group")
        registered = wire["groups"][index]
        need(type(group["name"]) is str and group["name"] == wanted["group_names"][index] == registered["name"] and
             type(group["status"]) is str and group["status"] == "PASS", "group-order-status")
        rejected = group["rejected_cases"]
        cases = registered["cases"]
        need(type(rejected) is list and all(type(name) is str and name for name in rejected) and
             rejected == [case["name"] for case in cases] and
             len(rejected) == wanted["rejection_counts"][index] and len(set(rejected)) == len(rejected),
             "group-actual-ordered-rejections")
        for case in cases:
            path = fixture / relative(case["rejection"])
            rejection = document(path)
            exact(rejection, wire["rejection_keys"], "actual-rejection-four-keys")
            need(all(type(value) is str and value for value in rejection.values()), "actual-rejection-plain-strings")
            need(rejection["fixture_scope"] == wire["rejection_fixture_scope"] and rejection["name"] == case["name"] and
                 rejection["expected_gate"] == case["expected_gate"], "actual-rejection-case-and-purpose")
            if case["observed_error_mode"] == "exact-prefixed":
                need(rejection["observed_error"] == "fixed_lambda_batch:" + case["expected_gate"],
                     "fifth-exact-caught-purpose-label")
            else:
                need(case["observed_error_mode"] == "contains" and
                     case["expected_gate"] in rejection["observed_error"], "retained-substring-caught-purpose-label")
            inspected.append({"group": group["name"], "file": case["rejection"], "pin": pin(path), "receipt": rejection})
    fifth = wire["fifth"]
    prefix = relative(fifth["root"])
    actual_files = [row["file"] for row in observed["files"] if row["file"].startswith(prefix + "/")]
    need(actual_files == fifth["exact_files"] and len(actual_files) == fifth["file_count"], "fifth-exact-34-file-roster")
    expected_dirs = {prefix}
    for name in fifth["exact_files"] + fifth["empty_directories"]:
        parts = PurePosixPath(relative(name)).parts
        expected_dirs.update("/".join(parts[:n]) for n in range(1, len(parts)))
    expected_dirs.update(fifth["empty_directories"])
    actual_dirs = {name for name in observed["directories"] if name == prefix or name.startswith(prefix + "/")}
    need(actual_dirs == expected_dirs, "fifth-all-exact-directories")
    need([name for name in observed["empty_directories"] if name.startswith(prefix + "/")] ==
         fifth["empty_directories"], "fifth-exact-one-empty-directory")
    ledger = document(fixture / fifth["ledger_file"])
    exact(ledger, fifth["ledger_keys"], "fifth-ledger")
    need(type(ledger["fixture_scope"]) is str and ledger["fixture_scope"] == fifth["ledger_scope"] and
         type(ledger["name"]) is str and ledger["name"] == tests[-1]["name"] and
         type(ledger["status"]) is str and ledger["status"] == "PASS" and
         type(ledger["cases"]) is list and len(ledger["cases"]) == 8, "fifth-ledger-header-and-count")
    group_root = fixture / prefix
    for actual, case in zip(ledger["cases"], fifth["cases"]):
        exact(actual, fifth["ledger_case_keys"], "fifth-ledger-case")
        need(type(actual["name"]) is str and actual["name"] == case["name"] and
             type(actual["expected_gate"]) is str and actual["expected_gate"] == case["expected_gate"] and
             type(actual["observed_error"]) is str and actual["observed_error"] == case["expected_observed_error"],
             "fifth-ledger-actual-purpose-label")
        for side in ("positive", "negative"):
            need(type(actual[side]) is list and len(actual[side]) == len(case[side]), "fifth-ledger-file-list")
            for row, name in zip(actual[side], case[side]):
                public_descriptor(group_root, row, name)
        public_descriptor(group_root, actual["rejection"], case["rejection"])
    scope = document(fixture / fifth["scope_file"])
    exact(scope, fifth["scope_keys"], "fifth-scope")
    need(type(scope["fixture_scope"]) is str and scope["fixture_scope"] == fifth["ledger_scope"] and
         scope["actual_parent_arithmetic"] is False and scope["full_1834_admission"] is False and
         scope["old17_projection"] is True and scope["registered_inventory_from_real_synthetic_files"] is True,
         "fifth-scope-assurances")
    need(type(scope["rejected_cases"]) is list and all(type(name) is str for name in scope["rejected_cases"]) and
         scope["rejected_cases"] == tests[-1]["rejected_cases"], "fifth-scope-rejection-order")
    exact(scope["original_prefix_shapes"], ("five_key", "six_key", "ten_key"), "fifth-original-prefix-shapes")
    need(all(type(value) is int for value in scope["original_prefix_shapes"].values()) and
         scope["original_prefix_shapes"] == {"five_key": 32, "six_key": 65, "ten_key": 256},
         "fifth-original-prefix-ordinary-counts")
    positive_inventory = inventory(group_root / "positive")
    exact(scope["positive_inventory"], ("files", "directories"), "fifth-positive-inventory")
    # Canonical byte comparison distinguishes JSON bool/int without accepting Python equality aliases.
    need(canonical(scope["positive_inventory"]) == canonical({key: positive_inventory[key]
         for key in ("files", "directories")}), "fifth-positive-complete-files-and-directories")
    json_files = []
    for row in observed["files"]:
        if row["file"].endswith(".json"):
            value = document(fixture / relative(row["file"]))
            json_files.append({"file": row["file"], "bytes": row["bytes"], "sha256": row["sha256"],
                               "JSON_root_type": type(value).__name__})
    save(out / "fixture-JSON-read-receipt.json", {"schema": "task1128.fixture-JSON-read.v1",
         "files": json_files, "all_formed_JSON_read": True,
         "invalid_negative_semantics_reaccepted": False, "math_helpers_executed_by_outer": 0})
    output = {"schema": "task1128.selftest-gate.v1", "status": "PASS_SELFTEST_ONLY",
              "stdout_pin": pin(out / "producer.stdout.bin"), "stdout_inner_sha256": result["sha256"],
              "tests": tests, "production_interfaces_used": result["production_interfaces_used"],
              "actual_rejection_receipts": inspected,
              "fifth_positive_evidence": {
                  "basis": "pinned P ordinary selftest positive calls followed by complete sealed PASS and exact saved ledger",
                  "public_expected_case_count": 8, "positive_inventory": scope["positive_inventory"],
                  "separate_runtime_positive_call_counter_present": False,
                  "parent_payload_admission_inferred": False},
              "root_math_and_runtime_review_required": True, **CLAIMS}
    save(out / "selftest-gate.json", output)
    return output



def main():
    started = time.monotonic()
    repo = Path.cwd().resolve(strict=True)
    out = repo / "ci/out/task1128"
    ordinary_path(out, directory=True)
    receipt = {"schema": "task1128.P6-selftest-end.v1", "status": "FAIL",
               "started_utc": utc(), "finished_utc": None, "elapsed_seconds": None,
               "errors": [], "producer_execution": None, "selftest_gate": None,
               "fixture_preservation": None, "source_copy_receipt": None, "source_pins_unchanged": False,
               "outer_sources_unchanged": False, "runtime": None, "isolated_runtime_root": None,
               "GAP_setup_seconds_included": False, "normal_run_substituted": False,
               "root_actual_receipt_review_required": True, **CLAIMS}
    fixture = None
    entries = None
    before = None
    outer_before = None
    registration = None
    try:
        need(len(sys.argv) == 1 and Path(__file__).resolve(strict=True) == repo / "search" / (STEM + ".py"),
             "fixed-outer-entry-and-no-input-arguments")
        registration = document(repo / "search" / (STEM + ".json"))
        need(registration["schema"] == "task1128.P6-selftest-runner.registration.v1", "registration-schema")
        entries = [registration["producer"], *registration["producer_dependencies"], *registration["raw_inputs"], registration["workflow"]]
        need(len(entries) == 13 and len({entry["file"] for entry in entries}) == 13, "P-plus-nine-dependencies-two-raw-plus-WF")
        code = out / "source-copy"
        code.mkdir()
        before = source_pins(repo, entries, capture=code)
        save(out / "registered-source-before.json", before)
        outer_before = []
        for suffix in (".g", ".sh", ".py", ".json"):
            name = "search/" + STEM + suffix
            outer_before.append({"file": name, **pin(repo / name, captured_source_path(code, name))})
        save(out / "outer-source-before.json", outer_before)
        gha = {key: os.environ.get(key) for key in (
            "GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT", "GITHUB_SHA", "GITHUB_REF",
            "GITHUB_WORKFLOW_REF", "GITHUB_REPOSITORY", "GITHUB_JOB")}
        need(all(type(value) is str and value for value in gha.values()), "GHA-context-required")
        need(len(gha["GITHUB_SHA"]) == 40 and all(ch in "0123456789abcdef" for ch in gha["GITHUB_SHA"]),
             "GHA-head-shape")
        for key in ("GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT"):
            need(all(ch in "0123456789" for ch in gha[key]) and int(gha[key]) > 0, "GHA-positive-ID")
        save(out / "launch-context.json", {"schema": "task1128.launch-context.v1", "GHA": gha,
             "checkout_basis": "existing checkout@v4 and GITHUB_SHA/REF; no git command", "argv": sys.argv})
        dispatch = {key: os.environ.get(key) for key in
                    ("GAP_RUN_SCRIPT", "GAP_RUN_PREAMBLE", "GAP_RUN_OUT_DIR", "GAP_WITH_PQUOT_PACKAGES")}
        need(dispatch == {"GAP_RUN_SCRIPT": "search/" + STEM + ".g", "GAP_RUN_PREAMBLE": "",
                          "GAP_RUN_OUT_DIR": "ci/out/task1128", "GAP_WITH_PQUOT_PACKAGES": "false"},
             "registered-gap-run-dispatch-inputs")
        need(os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch", "workflow-dispatch-event")
        save(out / "dispatch-inputs.json", {"schema": "task1128.dispatch-inputs.v1", "inputs": dispatch,
             "event": "workflow_dispatch", "timeout_min_registered_in_root_plan": 20,
             "timeout_min_observed_inside_process": None})
        need(sys.platform == "linux", "registered-ubuntu-runtime")
        runner_value = os.environ.get("RUNNER_TEMP")
        need(type(runner_value) is str and bool(runner_value), "RUNNER_TEMP-required")
        runner = Path(runner_value)
        ordinary_path(runner, directory=True)
        need(runner != repo and repo not in runner.parents, "RUNNER_TEMP-repository-disjoint")
        work = runner / ("task1128-" + uuid.uuid4().hex)
        work.mkdir()
        ordinary_path(work, directory=True)
        receipt["isolated_runtime_root"] = str(work)
        fixture = work / "selftest-fixtures"
        home = work / "home"
        home.mkdir()
        environment = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(home),
                       "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TMPDIR": str(work),
                       "TEMP": str(work), "TMP": str(work), "RUNNER_TEMP": str(runner),
                       "PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1"}
        settings = registration["runtime"]
        actual_python = ".".join(str(value) for value in sys.version_info[:3])
        receipt["runtime"] = {"runner_python_executable": sys.executable, "runner_python_version": actual_python,
                              "runner_python_full": sys.version, "main_run_python_version": settings["main_python"],
                              "same_python_version_as_main_run": actual_python == settings["main_python"],
                              "same_environment_as_main_run_claim": False, "memory_limit_kind": "RLIMIT_AS",
                              "RSS_limit_claim": False, "RSS_measured_by_outer": False, "RSS_peak_mib": None,
                              "inner_deadline_kind": "cooperative monotonic deadline; outer timeout is separate",
                              "numpy_expected": settings["numpy"],
                              "numpy_observed": None}
        save(out / "runtime-before.json", receipt["runtime"])
        venv = work / "venv"
        execution = run([sys.executable, "-B", "-m", "venv", "--copies", str(venv)],
                        "venv", settings["venv_seconds"], repo, out, environment)
        need(successful(execution), "venv-setup-failed")
        python = venv / "bin/python"
        ordinary_path(python)
        execution = run([str(python), "-B", "-m", "pip", "--isolated", "--disable-pip-version-check",
                         "--no-cache-dir", "install", "--index-url", "https://pypi.org/simple",
                         "--report", str(out / "pip-install-report.json"), "numpy==" + settings["numpy"]],
                        "pip", settings["pip_seconds"], repo, out, environment)
        need(successful(execution), "exact-numpy-install-failed")
        probe = "import sys,json,numpy;print(json.dumps({'python':list(sys.version_info[:3]),'numpy':numpy.__version__,'executable':sys.executable}))"
        execution = run([str(python), "-B", "-c", probe], "runtime-probe", settings["probe_seconds"], repo, out, environment)
        need(successful(execution), "runtime-version-probe-failed")
        actual = document(out / "runtime-probe.stdout.bin")
        exact(actual, ("python", "numpy", "executable"), "runtime-probe")
        need(type(actual["python"]) is list and len(actual["python"]) == 3 and
             all(type(n) is int for n in actual["python"]) and actual["python"] == list(sys.version_info[:3]),
             "venv-python-version")
        need(type(actual["numpy"]) is str and actual["numpy"] == settings["numpy"] and
             type(actual["executable"]) is str and Path(actual["executable"]) == python, "actual-numpy-and-interpreter")
        receipt["runtime"]["numpy_observed"] = actual["numpy"]
        save(out / "runtime-observed.json", receipt["runtime"])
        # Recheck registered sources immediately before the child, after environment setup.
        need(source_pins(repo, entries) == before, "registered-source-pre-execution")
        argv = [str(python), "-B", str(repo / registration["producer"]["file"]),
                "--selftest", "--selftest-root", str(fixture), "--batch-size", "128",
                "--max-seconds", str(settings["inner_seconds"]),
                "--max-memory-mib", str(settings["memory_mib"])]
        receipt["producer_execution"] = run(argv, "producer", settings["outer_seconds"], repo, out, environment)
    except BaseException as exc:
        receipt["errors"].append({"site": "setup-or-child", "reason": type(exc).__name__ + ":" + str(exc)})
    # Preservation is attempted even when the child stopped, returned nonzero, or printed invalid JSON.
    observed = None
    try:
        if fixture is not None and (fixture.exists() or fixture.is_symlink()):
            observed, receipt["fixture_preservation"] = preserve_fixture(fixture, out)
        else:
            receipt["fixture_preservation"] = {"schema": "task1128.fixture-preservation.v1",
                "status": "NOT_CREATED", "runtime_root": None if fixture is None else str(fixture),
                "complete_selftest_inferred": False}
            save(out / "fixture-preservation.json", receipt["fixture_preservation"])
    except BaseException as exc:
        receipt["errors"].append({"site": "full-fixture-preservation", "reason": type(exc).__name__ + ":" + str(exc)})
        receipt["fixture_preservation"] = {"schema": "task1128.fixture-preservation.v1", "status": "FAIL",
                                           "complete_selftest_inferred": False}
        if not (out / "fixture-preservation.json").exists():
            save(out / "fixture-preservation.json", receipt["fixture_preservation"])
    try:
        need(receipt["producer_execution"] is not None and successful(receipt["producer_execution"]),
             "actual-P-exit-zero-no-timeout-required")
        need(observed is not None and receipt["fixture_preservation"]["status"] == "PASS_FULL_BYTES",
             "whole-fixture-preservation-required")
        receipt["selftest_gate"] = selftest_gate(out, fixture, observed, registration["public_wire"])
    except BaseException as exc:
        receipt["errors"].append({"site": "selftest-result-gate", "reason": type(exc).__name__ + ":" + str(exc)})
    try:
        need(entries is not None, "registered-source-list-not-formed")
        after = source_pins(repo, entries)
        save(out / "registered-source-after.json", after)
        receipt["source_pins_unchanged"] = before is not None and before == after
        need(receipt["source_pins_unchanged"], "all-registered-sources-unchanged")
        need(outer_before is not None, "outer-source-list-not-formed")
        outer_after = source_pins(repo, outer_before)
        save(out / "outer-source-after.json", outer_after)
        receipt["outer_sources_unchanged"] = outer_after == outer_before
        need(receipt["outer_sources_unchanged"], "all-outer-sources-unchanged")
    except BaseException as exc:
        receipt["errors"].append({"site": "all-source-after", "reason": type(exc).__name__ + ":" + str(exc)})
    try:
        need(entries is not None and outer_before is not None, "source-copy-registration-not-formed")
        receipt["source_copy_receipt"] = source_copy_gate(out, entries, outer_before)
    except BaseException as exc:
        receipt["errors"].append({"site": "all-source-copy", "reason": type(exc).__name__ + ":" + str(exc)})
        try:
            if (out / "source-copy").is_dir():
                save(out / "source-copy-partial-inventory.json", inventory(out / "source-copy"))
        except BaseException as failure:
            receipt["errors"].append({"site": "source-copy-partial-inventory", "reason": type(failure).__name__ + ":" + str(failure)})

    if not receipt["errors"]:
        receipt["status"] = "PASS_SELFTEST_ONLY"
    receipt["finished_utc"] = utc()
    receipt["elapsed_seconds"] = time.monotonic() - started
    save(out / "selftest-end.json", receipt)
    print("TASK1128_OUTER_FINAL status=" + receipt["status"], flush=True)
    return 0 if receipt["status"] == "PASS_SELFTEST_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
