# mine/py_ci_contract.py -- backend=py-ci の CLI 契約解決/完走判定ロジック。
#
# .github/workflows/mine-dispatch.yml の py-ci 分岐(「Load job fields for
# downstream steps」「Write result.txt」の2ステップ)が呼ぶ、単一の実装。
# ロジックをワークフロー YAML の bash/python heredoc に二重実装しない --
# ここを唯一の実装にして、ワークフローからは import して呼ぶ・単体テスト
# (mine/test_py_ci_contract.py)もここを直接叩く。
#
# 2 つの CLI 契約(後方互換 -- 2026-08-01 miner の事前検出対応で汎用化):
#   (1) legacy-primes -- pipeline[0].params.primes(非空整数配列)がある
#       場合。無改変(u_meas_caseb_locus2.py 契約)。primes を CLI 引数に
#       し、完走判定は run.log 中「=== p = N ===」出現数が primes 数と一致。
#   (2) generic -- primes が無い場合。resources.py_driver.args(省略可・
#       文字列配列)を CLI 引数にし、完走判定は done_marker(省略時
#       "PY_DRIVER_DONE")の run.log 出現。result_count_check({marker,
#       expect}・省略可)があれば marker の出現行数と expect の突合も必須
#       にする(省略時はこの突合をスキップし done_marker 出現+exit 0 のみ
#       で done)。
#
# 両契約とも fail-closed: exit code が非 0 なら即 failed。判定ロジックは
# 完走(構造)チェックのみで、数学的な当否の判定はしない(gap-ci の
# DRIVER_DONE マーカー検出と同水準)。

import re


class PyCiConfigError(ValueError):
    """resolve_py_ci_config が job の資源記述を解決できないときに送出。
    呼び出し側(ワークフロー)は message を ERROR: 付きで stderr に出し
    exit 1 する(preflight 等と同じ fail-closed の作法)。"""


def resolve_py_ci_config(job):
    """mine-job/v1 の job dict から py-ci 実行設定を解決する。

    戻り値 dict:
      script               -- 起動するスクリプトのパス
      legacy_primes_mode   -- bool。True なら契約(1)、False なら契約(2)
      args                 -- CLI に渡す引数(文字列のリスト)
      nprimes              -- 契約(1)のときのみ int、それ以外は None
      done_marker          -- 契約(2)のときのみ非空文字列、それ以外は None
      rcc_marker           -- 契約(2)で result_count_check があれば文字列、
                               無ければ None
      rcc_expect           -- rcc_marker があれば int、無ければ None
    """
    res = job.get("resources") or {}
    pyd = res.get("py_driver") or {}
    script = pyd.get("script")
    if not script:
        raise PyCiConfigError("resources.py_driver.script is required for backend=py-ci")

    pipeline = job.get("pipeline") or []
    params = {}
    if pipeline and isinstance(pipeline[0], dict):
        params = pipeline[0].get("params") or {}
    primes = params.get("primes")
    legacy_primes_mode = primes is not None

    if legacy_primes_mode:
        if not isinstance(primes, list) or not primes or not all(
            isinstance(p, int) and not isinstance(p, bool) for p in primes
        ):
            raise PyCiConfigError(
                "pipeline[0].params.primes must be a non-empty array of integers for backend=py-ci"
            )
        return {
            "script": script,
            "legacy_primes_mode": True,
            "args": [str(p) for p in primes],
            "nprimes": len(primes),
            "done_marker": None,
            "rcc_marker": None,
            "rcc_expect": None,
        }

    args = pyd.get("args")
    if args is not None and not (isinstance(args, list) and all(isinstance(a, str) for a in args)):
        raise PyCiConfigError("resources.py_driver.args, when present, must be an array of strings")

    done_marker = pyd.get("done_marker")
    if done_marker is not None and not (isinstance(done_marker, str) and len(done_marker) > 0):
        raise PyCiConfigError("resources.py_driver.done_marker, when present, must be a non-empty string")
    done_marker = done_marker or "PY_DRIVER_DONE"

    rcc = pyd.get("result_count_check")
    rcc_marker = None
    rcc_expect = None
    if rcc is not None:
        if not isinstance(rcc, dict) or not isinstance(rcc.get("marker"), str) or not rcc.get("marker") \
                or not isinstance(rcc.get("expect"), int) or isinstance(rcc.get("expect"), bool) \
                or rcc.get("expect") < 0:
            raise PyCiConfigError(
                "resources.py_driver.result_count_check, when present, must be "
                "{marker: non-empty string, expect: non-negative integer}"
            )
        rcc_marker = rcc["marker"]
        rcc_expect = rcc["expect"]

    return {
        "script": script,
        "legacy_primes_mode": False,
        "args": [str(a) for a in (args or [])],
        "nprimes": None,
        "done_marker": done_marker,
        "rcc_marker": rcc_marker,
        "rcc_expect": rcc_expect,
    }


def _line_count(run_log_text, needle):
    """grep -c -F <needle> と同じ意味(needle を含む行の数)を python で再現。"""
    return sum(1 for line in run_log_text.splitlines() if needle in line)


def determine_py_ci_verdict(
    legacy_primes_mode,
    py_exit_code,
    run_log_text,
    nprimes=None,
    done_marker=None,
    rcc_marker=None,
    rcc_expect=None,
):
    """引数は resolve_py_ci_config(job) の戻り値の該当欄をそのまま渡せる形
    (flat kwargs -- ワークフロー側の bash ステップから scalar 出力値を直接
    渡しやすくするため、cfg dict でなく個別引数にしてある)。run_log_text は
    run.log 全文。戻り値は "done" または "failed"(mine-dispatch.yml の
    verdict と同じ語彙)。"""
    if legacy_primes_mode:
        result_count = len(re.findall(r"^=== p = ", run_log_text, flags=re.MULTILINE))
        if py_exit_code == 0 and result_count == nprimes:
            return "done"
        return "failed"

    if py_exit_code != 0:
        return "failed"
    if not done_marker or done_marker not in run_log_text:
        return "failed"
    if rcc_marker:
        actual = _line_count(run_log_text, rcc_marker)
        if actual != rcc_expect:
            return "failed"
    return "done"
