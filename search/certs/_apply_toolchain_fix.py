"""
One-off maintenance script (throwaway, not a deliverable): apply commander
directive 115 fix (1) to laneB_manifest.json -- replace the placeholder
toolchain_digest string with the real sha256 of sys.executable, and fill
in the D-1/D-2 derived values (dependency-manifest v13 sec.2.2) for every
entry now that toolchain_digest is a real, dereferenceable content digest.
"""
import hashlib
import json
import sys

MANIFEST_PATH = "search/certs/laneB_manifest.json"


def canonical_serialize(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def d1(source_artifact_digests):
    s = sorted(set(source_artifact_digests))
    return hashlib.sha256(canonical_serialize(s).encode("utf-8")).hexdigest()


def d2(source_artifact_digests, toolchain_digest, build_step_digests):
    s = sorted(set(source_artifact_digests))
    obj = {"source": s, "toolchain": toolchain_digest, "steps": build_step_digests}
    return hashlib.sha256(canonical_serialize(obj).encode("utf-8")).hexdigest()


def main():
    with open(sys.executable, "rb") as f:
        exe_bytes = f.read()
    real_toolchain_digest = hashlib.sha256(exe_bytes).hexdigest()
    print("real toolchain_digest (sha256 of sys.executable):", real_toolchain_digest)
    print("sys.executable:", sys.executable)

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    dm = manifest["dependency_manifest"]
    for entry in dm["entries"]:
        entry["toolchain_digest"] = real_toolchain_digest
        entry.pop("_toolchain_note", None)
        src = entry.get("source_artifact_digests", [])
        steps = entry.get("build_step_digests", [])
        entry["source_closure_digest"] = d1(src)
        entry["implementation_lineage_digest"] = d2(src, real_toolchain_digest, steps)

    manifest["_meta"]["toolchain_provenance_note"] = (
        "toolchain_digest = sha256 of the exact CPython 3.13 interpreter "
        "binary (sys.executable) used to run/test this lane-B code, "
        "computed by this maintenance script (search/certs/_apply_toolchain_fix.py) "
        "and machine-verifiable by any receiving side with access to the same "
        "interpreter binary. Path recorded for provenance (path is NOT part of "
        "identity per dependency-manifest v13 H-2d -- only the digest is). "
        f"sys.executable path at generation time: {sys.executable} "
        f"(size {len(exe_bytes)} bytes)."
    )
    manifest["_meta"]["not_attempted_or_unknown_update"] = (
        "toolchain_digest is now a real content digest (directive 115 fix 1); "
        "source_closure_digest (D-1) and implementation_lineage_digest (D-2) "
        "are now filled in per each entry (producer-declared reference values, "
        "sec.2.1/2.2 -- receiving side must still independently recompute and "
        "compare per E-8''; these are NOT a substitute for that recomputation)."
    )

    with open(MANIFEST_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=True)
        f.write("\n")

    print("manifest updated.")


if __name__ == "__main__":
    main()
