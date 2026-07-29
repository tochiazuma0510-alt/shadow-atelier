"""
One-off maintenance script (throwaway): after ninfty-verifier-b.py content
changes (裁定127 fail-open/crash fixes, 裁定128 shape reshape), refresh
laneB_manifest.json's subject_code_digest and the corresponding entry's
content_digest/source_artifact_digests/D-1/D-2, keeping toolchain_digest
(already a real value) unchanged.
"""
import hashlib
import json

MANIFEST_PATH = "search/certs/laneB_manifest.json"
VERIFIER_PATH = "search/ninfty-verifier-b.py"


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
    with open(VERIFIER_PATH, "rb") as f:
        new_digest = hashlib.sha256(f.read()).hexdigest()
    print("new verifier-b.py digest:", new_digest)

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    dm = manifest["dependency_manifest"]
    old_digest = dm["subject_code_digest"]
    print("old subject_code_digest:", old_digest)
    dm["subject_code_digest"] = new_digest

    for entry in dm["entries"]:
        if entry.get("content_digest") == old_digest:
            entry["content_digest"] = new_digest
            entry["source_artifact_digests"] = [new_digest]
            entry["source_closure_digest"] = d1([new_digest])
            entry["implementation_lineage_digest"] = d2([new_digest], entry["toolchain_digest"],
                                                          entry.get("build_step_digests", []))
        elif old_digest in entry.get("reached_via", []):
            entry["reached_via"] = [new_digest if x == old_digest else x for x in entry["reached_via"]]

    manifest["_meta"]["subject_digest_refresh_note"] = (
        f"subject_code_digest and the corresponding entry refreshed from "
        f"{old_digest} to {new_digest} after 裁定127 (fail-open/crash "
        f"fixes) and 裁定128 (cert_shape_interpretation_v1 reshape) edits "
        f"to search/ninfty-verifier-b.py."
    )

    with open(MANIFEST_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=True)
        f.write("\n")
    print("manifest updated.")


if __name__ == "__main__":
    main()
