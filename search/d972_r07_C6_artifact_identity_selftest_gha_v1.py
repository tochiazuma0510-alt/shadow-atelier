"""Task1126: public C6 selftest packaging only; no parent intake."""
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

STEM = "d972_r07_C6_artifact_identity_selftest_gha_v1"
CLAIMS = {"fullA0": False, "candidate": False, "cross_checked": False, "verified": False}


def need(value, label):
    if not value:
        raise ValueError("task1126:" + label)


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
    raise ValueError("task1126:nonfinite-JSON:" + value)


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


def source_pins(repo, entries, capture=None):
    result = []
    for entry in entries:
        exact(entry, ("file", "bytes", "sha256"), "source-registration")
        name = relative(entry["file"])
        need(type(entry["bytes"]) is int and entry["bytes"] > 0 and
             type(entry["sha256"]) is str and len(entry["sha256"]) == 64,
             "source-pin-types")
        target = None if capture is None else capture / name
        if target is not None:
            target.parent.mkdir(parents=True, exist_ok=True)
        observed = {"file": name, **pin(repo / name, target)}
        need(observed == entry, "registered-whole-source:" + name)
        result.append(observed)
    return result


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
                raise ValueError("task1126:fixture-nonregular-entry:" + name)
    return {"files": sorted(files, key=lambda x: x["file"]),
            "directories": sorted(directories), "empty_directories": sorted(empty)}


def run(argv, label, timeout, repo, out, environment):
    start = time.monotonic()
    value = {"schema": "task1126.execution.v1", "label": label, "argv": argv,
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
    for name in sorted(before["directories"], key=lambda value: (value.count("/"), value)):
        (copied / name).mkdir()
    for row in before["files"]:
        observed = pin(root / row["file"], copied / row["file"])
        need(observed == {k: row[k] for k in ("bytes", "sha256")}, "fixture-copy-bytes:" + row["file"])
    need(inventory(root) == before and inventory(copied) == before, "full-copy-source-equality")
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
        for row in before["files"]:
            entry = zipfile.ZipInfo("fixtures/" + row["file"])
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | 0o600) << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            with (copied / row["file"]).open("rb") as source, container.open(entry, "w", force_zip64=True) as target:
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
                need(not entry.is_dir() and stat.S_ISREG(mode) and
                     size == entry.file_size == row["bytes"] and digest.hexdigest() == row["sha256"],
                     "ZIP-full-file-EOF:" + entry.filename)
    after, copy_after = inventory(root), inventory(copied)
    save(out / "fixture-inventory-after.json", after)
    save(out / "fixture-copy-inventory.json", copy_after)
    need(before == after == copy_after and archive_before == pin(archive), "fixture-after-archive-equality")
    result = {"schema": "task1126.fixture-preservation.v1", "status": "PASS_FULL_BYTES",
              "runtime_root": str(root), "copy_root": str(copied), "archive": archive.name,
              "archive_pin": archive_before, "file_count": len(before["files"]),
              "directory_count_excluding_root": len(before["directories"]),
              "empty_directories": before["empty_directories"], "ZIP_entry_count": len(names),
              "every_entry_read_to_EOF": True, "zipfile_CRC_checked_on_read": True,
              "independent_CRC_implementation": False, "complete_selftest_inferred": False}
    save(out / "fixture-preservation.json", result)
    return before, result


def selftest_gate(out, fixture, observed, wire):
    result = document(out / "checker.stdout.bin")
    wanted = wire["success_stdout"]
    exact(result, wanted["exact_top_keys"], "selftest-top")
    need(type(result["schema"]) is str and result["schema"] == wanted["schema"] and
         type(result["status"]) is str and result["status"] == "PASS", "selftest-schema-status")
    unsigned = {key: value for key, value in result.items() if key != "sha256"}
    need(type(result["sha256"]) is str and result["sha256"] == hashlib.sha256(canonical(unsigned)).hexdigest(),
         "selftest-inner-seal")
    need(type(result["fixture_scope"]) is str and bool(result["fixture_scope"]), "selftest-scope")
    need(type(result["old_success_suites"]) is int and result["old_success_suites"] == 0,
         "no-old-success-suite-replay")
    for field in ("actual_anchor_arithmetic_replayed", "candidate", "cross_checked", "verified"):
        need(result[field] is False, "selftest-false-assurance:" + field)
    need(type(result["production_interfaces_used"]) is list and
         all(type(name) is str and name for name in result["production_interfaces_used"]) and
         result["production_interfaces_used"] == wanted["production_interfaces_used"], "public-interface-order")
    tests = result["tests"]
    need(type(tests) is list and len(tests) == 5, "five-selftest-groups")
    for index, group in enumerate(tests):
        exact(group, wanted["group_exact_keys"], "selftest-group")
        need(type(group["name"]) is str and group["name"] == wanted["group_names"][index] and
             type(group["status"]) is str and group["status"] == "PASS", "group-order-status")
        rejected = group["rejected_cases"]
        need(type(rejected) is list and all(type(name) is str and name for name in rejected) and
             len(rejected) == wanted["rejection_counts"][index] and len(set(rejected)) == len(rejected),
             "group-actual-rejection-count")
    cases = wire["fifth_group_cases"]
    need(tests[-1]["rejected_cases"] == [case["case_name"] for case in cases], "fifth-ordered-rejections")
    expected_files = list(wire["supporting_files"])
    for case in cases:
        expected_files.extend(case[k] for k in ("positive", "negative", "rejection"))
    actual_files = [row["file"] for row in observed["files"] if row["file"].startswith("parent1834/")]
    need(sorted(expected_files) == actual_files and len(actual_files) == wire["fifth_subtree_file_count"],
         "fifth-exact-28-file-roster")
    expected_dirs = {"parent1834"}
    for name in expected_files + wire["explicit_extra_directories"]:
        parts = PurePosixPath(relative(name)).parts
        expected_dirs.update("/".join(parts[:n]) for n in range(1, len(parts)))
    expected_dirs.update(wire["explicit_extra_directories"])
    actual_dirs = {name for name in observed["directories"] if name == "parent1834" or name.startswith("parent1834/")}
    need(actual_dirs == expected_dirs, "fifth-all-directories")
    need([name for name in observed["empty_directories"] if name.startswith("parent1834/")] ==
         sorted(wire["explicit_extra_directories"]), "fifth-one-explicit-empty")
    inspected = []
    for case in cases:
        rejection = document(fixture / relative(case["rejection"]))
        exact(rejection, wire["rejection_keys"], "fifth-rejection")
        need(all(type(value) is str and value for value in rejection.values()), "fifth-rejection-strings")
        need(rejection == {"case_name": case["case_name"], "expected_label": case["expected_label"],
                           "observed_label": case["expected_observed_label"], "status": wire["rejection_status"]},
             "fifth-actual-purpose-label:" + case["case_name"])
        # These public documents are retained and decoded, not re-executed as new test cases.
        for kind in ("positive", "negative"):
            value = document(fixture / relative(case[kind]))
            need(type(value) is dict, "fifth-plain-object:" + case[kind])
        inspected.append({"case_name": case["case_name"], "rejection": rejection})
    document(fixture / "parent1834/case-ledger.json")
    output = {"schema": "task1126.selftest-gate.v1", "status": "PASS_PUBLIC_SELFTEST",
              "stdout_pin": pin(out / "checker.stdout.bin"), "stdout_inner_sha256": result["sha256"],
              "tests": tests, "production_interfaces_used": result["production_interfaces_used"],
              "fifth_actual_rejections": inspected,
              "artifact_identity_positive": {
                  "basis": "pinned C ordinary selftest loop plus sealed PASS; no separate measured-count field",
                  "public_expected_role_count": wire["positive_artifact_comparisons"],
                  "public_expected_fields_per_role": wire["positive_fields_per_role"],
                  "positive_fixture": wire["positive_fixture_file"],
                  "positive_fixture_pin": pin(fixture / wire["positive_fixture_file"]),
                  "separate_runtime_18_result_rows_present": False,
                  "parent_payload_admission_inferred": False}, **CLAIMS}
    save(out / "selftest-gate.json", output)
    return output

def main():
    started = time.monotonic()
    repo = Path.cwd().resolve(strict=True)
    out = repo / "ci/out/task1126"
    ordinary_path(out, directory=True)
    receipt = {"schema": "task1126.C6-selftest-end.v1", "status": "FAIL",
               "started_utc": utc(), "finished_utc": None, "elapsed_seconds": None,
               "errors": [], "checker_execution": None, "selftest_gate": None,
               "fixture_preservation": None, "source_pins_unchanged": False,
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
        need(registration["schema"] == "task1126.C6-selftest-runner.registration.v1", "registration-schema")
        entries = [registration["checker"], *registration["checker_dependencies"], registration["workflow"]]
        need(len(entries) == 12 and len({entry["file"] for entry in entries}) == 12, "C-plus-ten-dependencies-plus-WF")
        code = out / "checkout-sources"
        code.mkdir()
        before = source_pins(repo, entries, capture=code)
        save(out / "registered-source-before.json", before)
        outer_before = []
        for suffix in (".g", ".sh", ".py", ".json"):
            name = "search/" + STEM + suffix
            outer_before.append({"file": name, **pin(repo / name, code / name)})
        save(out / "outer-source-before.json", outer_before)
        gha = {key: os.environ.get(key) for key in (
            "GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT", "GITHUB_SHA", "GITHUB_REF",
            "GITHUB_WORKFLOW_REF", "GITHUB_REPOSITORY", "GITHUB_JOB")}
        need(all(type(value) is str and value for value in gha.values()), "GHA-context-required")
        need(len(gha["GITHUB_SHA"]) == 40 and all(ch in "0123456789abcdef" for ch in gha["GITHUB_SHA"]),
             "GHA-head-shape")
        for key in ("GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT"):
            need(all(ch in "0123456789" for ch in gha[key]) and int(gha[key]) > 0, "GHA-positive-ID")
        save(out / "launch-context.json", {"schema": "task1126.launch-context.v1", "GHA": gha,
             "checkout_basis": "existing checkout@v4 and GITHUB_SHA/REF; no git command", "argv": sys.argv})
        need(sys.platform == "linux", "registered-ubuntu-runtime")
        runner_value = os.environ.get("RUNNER_TEMP")
        need(type(runner_value) is str and bool(runner_value), "RUNNER_TEMP-required")
        runner = Path(runner_value)
        ordinary_path(runner, directory=True)
        need(runner != repo and repo not in runner.parents, "RUNNER_TEMP-repository-disjoint")
        work = runner / ("task1126-" + uuid.uuid4().hex)
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
                              "same_environment_as_main_run_claim": False, "numpy_expected": settings["numpy"],
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
        argv = [str(python), "-B", str(repo / registration["checker"]["file"]),
                "--selftest", "--selftest-root", str(fixture), "--max-seconds", str(settings["inner_seconds"]),
                "--max-memory-mib", str(settings["memory_mib"])]
        receipt["checker_execution"] = run(argv, "checker", settings["outer_seconds"], repo, out, environment)
    except BaseException as exc:
        receipt["errors"].append({"site": "setup-or-child", "reason": type(exc).__name__ + ":" + str(exc)})
    # Preservation is attempted even when the child stopped, returned nonzero, or printed invalid JSON.
    observed = None
    try:
        if fixture is not None and (fixture.exists() or fixture.is_symlink()):
            observed, receipt["fixture_preservation"] = preserve_fixture(fixture, out)
        else:
            receipt["fixture_preservation"] = {"schema": "task1126.fixture-preservation.v1",
                "status": "NOT_CREATED", "runtime_root": None if fixture is None else str(fixture),
                "complete_selftest_inferred": False}
            save(out / "fixture-preservation.json", receipt["fixture_preservation"])
    except BaseException as exc:
        receipt["errors"].append({"site": "full-fixture-preservation", "reason": type(exc).__name__ + ":" + str(exc)})
        receipt["fixture_preservation"] = {"schema": "task1126.fixture-preservation.v1", "status": "FAIL",
                                           "complete_selftest_inferred": False}
        if not (out / "fixture-preservation.json").exists():
            save(out / "fixture-preservation.json", receipt["fixture_preservation"])
    try:
        need(receipt["checker_execution"] is not None and successful(receipt["checker_execution"]),
             "actual-C-exit-zero-no-timeout-required")
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
    if not receipt["errors"]:
        receipt["status"] = "PASS_SELFTEST_ONLY"
    receipt["finished_utc"] = utc()
    receipt["elapsed_seconds"] = time.monotonic() - started
    save(out / "selftest-end.json", receipt)
    print("TASK1126_OUTER_FINAL status=" + receipt["status"], flush=True)
    return 0 if receipt["status"] == "PASS_SELFTEST_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
