# mine/preflight.py -- 採掘場(mine)ジョブのローカル前哨(裁定237・ideas_013 §5.2 手順①)。
#
# 4 ゲートを実行する:
#   (a) schema 検査   -- mine-job-v1.schema.json の要旨を stdlib のみで再現
#                          (jsonschema 未導入・依存追加はしない方針)
#   (b) integrity 検査 -- universe.frozen_docs と resources.v0_driver.script の
#                          sha256 を、plan 記載値と "今この場で" 再計算して照合
#   (c) 予言ゲート     -- predictions.frozen+sha256 が非空、または
#                          predictions.declared_none の明示宣言があること
#   (d) registry ゲート -- pipeline[*].predicate が mine/registry/*.json の
#                          カード id を指す場合のみ、explorer/checker.file の
#                          impl_sha256 を再計算して照合(v1・裁定237)
#
# 全 PASS で exit 0。1 つでも違反があれば理由を全部印字して exit 1
# (fail-closed -- 部分合格という状態を作らない)。
#
# usage: python mine/preflight.py mine/jobs/queue/<job>.json

import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEX64 = re.compile(r"^[0-9a-f]{64}$")


def sha256_of(path):
    fp = os.path.join(ROOT, path)
    if not os.path.isfile(fp):
        return None
    with open(fp, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def is_nonempty_str(v):
    return isinstance(v, str) and len(v) > 0


# ---------------------------------------------------------------------------
# (a) schema 検査 -- mine-job-v1.schema.json の必須欄・形を手作業で再現
# ---------------------------------------------------------------------------
def gate_schema(job):
    errs = []

    if job.get("schema") != "mine-job/v1":
        errs.append(f'schema must be "mine-job/v1", got {job.get("schema")!r}')

    if not is_nonempty_str(job.get("job_id")) or not re.match(r"^[A-Za-z0-9_-]+$", job.get("job_id", "")):
        errs.append("job_id must be a non-empty string of [A-Za-z0-9_-]")

    claim_class = job.get("claim_class")
    if claim_class not in ("exploration", "negative-claim"):
        errs.append(f'claim_class must be "exploration" or "negative-claim", got {claim_class!r}')

    map_ref = job.get("map_ref")
    if not isinstance(map_ref, dict):
        errs.append("map_ref must be an object")
    else:
        polestar = map_ref.get("polestar")
        if not isinstance(polestar, list) or len(polestar) == 0 or not all(isinstance(p, str) for p in polestar):
            errs.append("map_ref.polestar must be a non-empty array of strings")
        if not isinstance(map_ref.get("band"), int):
            errs.append("map_ref.band must be an integer")

    universe = job.get("universe")
    if not isinstance(universe, dict):
        errs.append("universe must be an object")
        universe = {}
    else:
        if universe.get("generator") not in ("lins-band", "ladder-family", "cell-family", "direct-windows", "cnf-manifest"):
            errs.append(f'universe.generator must be a registered generator, got {universe.get("generator")!r}')
        if not isinstance(universe.get("params"), dict):
            errs.append("universe.params must be an object")
        fd = universe.get("frozen_docs")
        if not isinstance(fd, list) or len(fd) == 0:
            errs.append("universe.frozen_docs must be a non-empty array")
        else:
            for i, item in enumerate(fd):
                if not isinstance(item, dict) or not is_nonempty_str(item.get("path")) or not HEX64.match(item.get("sha256", "")):
                    errs.append(f"universe.frozen_docs[{i}] must be {{path: non-empty string, sha256: 64-hex}}")
        if claim_class == "negative-claim" and not HEX64.match(universe.get("sha256", "")):
            errs.append("universe.sha256 (64-hex) is required when claim_class=negative-claim")

    pipeline = job.get("pipeline")
    if not isinstance(pipeline, list) or len(pipeline) == 0:
        errs.append("pipeline must be a non-empty array")
    else:
        for i, item in enumerate(pipeline):
            if not isinstance(item, dict) or not is_nonempty_str(item.get("predicate")) or not isinstance(item.get("version"), int):
                errs.append(f"pipeline[{i}] must be {{predicate: non-empty string, version: integer}}")

    predictions = job.get("predictions")
    if not isinstance(predictions, dict):
        errs.append("predictions must be an object")
    else:
        has_frozen = is_nonempty_str(predictions.get("frozen")) and HEX64.match(predictions.get("sha256", ""))
        has_declared_none = is_nonempty_str(predictions.get("declared_none"))
        if not (has_frozen or has_declared_none):
            errs.append('predictions must be either {frozen, sha256} (both non-empty/64-hex) or {declared_none: "理由"}')

    resources = job.get("resources")
    if not isinstance(resources, dict):
        errs.append("resources must be an object")
        resources = {}
    else:
        if resources.get("backend") not in ("gap-ci", "sat-ci", "py-ci"):
            errs.append(f'resources.backend must be one of gap-ci/sat-ci/py-ci, got {resources.get("backend")!r}')
        if not isinstance(resources.get("timeout_min"), int) or resources.get("timeout_min", 0) < 1:
            errs.append("resources.timeout_min must be a positive integer")
        v0d = resources.get("v0_driver")
        if v0d is not None:
            if not isinstance(v0d, dict) or not is_nonempty_str(v0d.get("script")) or not HEX64.match(v0d.get("sha256", "")):
                errs.append("resources.v0_driver, when present, must be {script: non-empty string, sha256: 64-hex[, preamble]}")
        pyd = resources.get("py_driver")
        if pyd is not None:
            if not isinstance(pyd, dict) or not is_nonempty_str(pyd.get("script")) or not HEX64.match(pyd.get("sha256", "")):
                errs.append("resources.py_driver, when present, must be {script: non-empty string, sha256: 64-hex}")
        shards = resources.get("shards")
        if isinstance(shards, list):
            if len(shards) == 0 or len(shards) > 256:
                errs.append("resources.shards (array form) must have 1..256 items (GHA matrix cap)")
            valid_names = []
            for i, sh in enumerate(shards):
                if not isinstance(sh, dict) or not is_nonempty_str(sh.get("name")) \
                        or not re.match(r"^[A-Za-z0-9_-]+$", sh.get("name", "")) \
                        or "preamble" not in sh or not isinstance(sh.get("preamble"), str):
                    errs.append(f"resources.shards[{i}] must be {{name: [A-Za-z0-9_-]+, preamble: string}}")
                else:
                    valid_names.append(sh["name"])
            if len(set(valid_names)) != len(valid_names):
                errs.append("resources.shards (array form) shard names must be unique")
        elif shards is not None and not isinstance(shards, (str, int)):
            errs.append("resources.shards must be a string, integer, or array of {name, preamble}")

    outputs = job.get("outputs")
    if not isinstance(outputs, dict) or not is_nonempty_str(outputs.get("cert_schema")) or not is_nonempty_str(outputs.get("out_dir")):
        errs.append("outputs must be {cert_schema: non-empty string, out_dir: non-empty string}")

    crosscheck = job.get("crosscheck")
    if not isinstance(crosscheck, dict) or crosscheck.get("mode") not in ("auto-pair", "manual", "none"):
        errs.append('crosscheck.mode must be one of auto-pair/manual/none')

    if "ep_handoff" not in job:
        errs.append("ep_handoff must be present (null in v0 -- EP integration is out of scope, 裁定237)")

    return errs


# ---------------------------------------------------------------------------
# (b) integrity gate -- universe.frozen_docs + resources.v0_driver.script の
#     sha256 を「今この場で」再計算し、plan 記載値と照合する。
# ---------------------------------------------------------------------------
def gate_integrity(job):
    errs = []
    universe = job.get("universe") or {}
    for item in universe.get("frozen_docs") or []:
        path = item.get("path")
        expected = item.get("sha256")
        actual = sha256_of(path)
        if actual is None:
            errs.append(f"INTEGRITY_STOP: frozen_docs {path}: file not found")
        elif actual != expected:
            errs.append(f"INTEGRITY_STOP: frozen_docs {path}: sha256 mismatch (expected {expected}, got {actual})")

    v0d = ((job.get("resources") or {}).get("v0_driver")) or {}
    script = v0d.get("script")
    expected = v0d.get("sha256")
    if script and expected:
        actual = sha256_of(script)
        if actual is None:
            errs.append(f"INTEGRITY_STOP: v0_driver.script {script}: file not found")
        elif actual != expected:
            errs.append(f"INTEGRITY_STOP: v0_driver.script {script}: sha256 mismatch (expected {expected}, got {actual}) -- driver が plan 記載時から変更されている")

    pyd = ((job.get("resources") or {}).get("py_driver")) or {}
    py_script = pyd.get("script")
    py_expected = pyd.get("sha256")
    if py_script and py_expected:
        actual = sha256_of(py_script)
        if actual is None:
            errs.append(f"INTEGRITY_STOP: py_driver.script {py_script}: file not found")
        elif actual != py_expected:
            errs.append(f"INTEGRITY_STOP: py_driver.script {py_script}: sha256 mismatch (expected {py_expected}, got {actual}) -- script が plan 記載時から変更されている")

    return errs


# ---------------------------------------------------------------------------
# (c) 予言ゲート -- schema 検査で構造は見ているが、ここでは実ファイルの
#     sha256 一致まで念押しで確認する(prediction-first の機械化)。
# ---------------------------------------------------------------------------
def gate_predictions(job):
    errs = []
    predictions = job.get("predictions") or {}
    if is_nonempty_str(predictions.get("frozen")):
        expected = predictions.get("sha256")
        actual = sha256_of(predictions["frozen"])
        if actual is None:
            errs.append(f"PREDICTION_STOP: predictions.frozen {predictions['frozen']}: file not found")
        elif actual != expected:
            errs.append(f"PREDICTION_STOP: predictions.frozen {predictions['frozen']}: sha256 mismatch (expected {expected}, got {actual})")
    elif not is_nonempty_str(predictions.get("declared_none")):
        errs.append("PREDICTION_STOP: predictions has neither {frozen, sha256} nor {declared_none}")
    return errs


# ---------------------------------------------------------------------------
# (d) registry gate -- plan の pipeline[*].predicate が mine/registry/*.json
#     のカード id を指す場合のみ発動: カードの explorer/checker.file の
#     impl_sha256 を「今この場で」再計算して照合する。カード無しの述語
#     (v0 driver 直参照)はここでは何もしない -- §7-1「カード化は走った後で
#     よい」により合法。
# ---------------------------------------------------------------------------
def load_registry_cards():
    cards = {}
    reg_dir = os.path.join(ROOT, "mine", "registry")
    if not os.path.isdir(reg_dir):
        return cards
    for fn in sorted(os.listdir(reg_dir)):
        if not fn.endswith(".json"):
            continue
        fp = os.path.join(reg_dir, fn)
        try:
            with open(fp, encoding="utf-8") as f:
                card = json.load(f)
        except Exception:
            continue
        cid = card.get("id")
        if is_nonempty_str(cid):
            cards[cid] = card
    return cards


def gate_registry(job):
    errs = []
    cards = load_registry_cards()
    pipeline = job.get("pipeline")
    if not isinstance(pipeline, list):
        return errs
    for i, item in enumerate(pipeline):
        if not isinstance(item, dict):
            continue
        pred = item.get("predicate")
        card = cards.get(pred)
        if card is None:
            continue  # v0 driver 直参照のカード無し述語 -- 合法(§7-1)
        for role in ("explorer", "checker"):
            role_spec = card.get(role)
            if not isinstance(role_spec, dict):
                continue
            file_path = role_spec.get("file")
            expected = role_spec.get("impl_sha256")
            if not is_nonempty_str(file_path) or not is_nonempty_str(expected):
                continue
            actual = sha256_of(file_path)
            if actual is None:
                errs.append(f"REGISTRY_STOP: pipeline[{i}] predicate={pred!r} card.{role}.file {file_path}: file not found")
            elif actual != expected:
                errs.append(f"REGISTRY_STOP: pipeline[{i}] predicate={pred!r} card.{role}.file {file_path}: "
                             f"impl_sha256 mismatch (expected {expected}, got {actual}) -- 実装が card 記載時から変更されている")
    return errs


def main():
    if len(sys.argv) != 2:
        print("usage: python mine/preflight.py <job.json path>")
        sys.exit(1)
    job_path = sys.argv[1]
    fp = os.path.join(ROOT, job_path) if not os.path.isabs(job_path) else job_path
    try:
        with open(fp, encoding="utf-8") as f:
            job = json.load(f)
    except Exception as e:
        print(f"STOP: could not read/parse {job_path}: {e}")
        sys.exit(1)

    all_errs = []
    schema_errs = gate_schema(job)
    all_errs += [f"(a) SCHEMA_INVALID: {e}" for e in schema_errs]

    # integrity/prediction ゲートは schema が最低限成立していないと意味が
    # 無い値を触りに行く(存在しないキー参照)ので、schema が壊れていても
    # 出せる範囲までは試みる(fail-closed だが診断は最大限出す)。
    all_errs += [f"(b) {e}" for e in gate_integrity(job)]
    all_errs += [f"(c) {e}" for e in gate_predictions(job)]
    all_errs += [f"(d) {e}" for e in gate_registry(job)]

    if all_errs:
        print(f"STOP: {job_path} failed preflight ({len(all_errs)} violation(s)):")
        for e in all_errs:
            print(f"  {e}")
        sys.exit(1)

    print(f"PASS: {job_path} -- schema/integrity/prediction gates all clear "
          f"(job_id={job.get('job_id')}, claim_class={job.get('claim_class')})")
    sys.exit(0)


if __name__ == "__main__":
    main()
