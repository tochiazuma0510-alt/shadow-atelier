# mine/test_py_ci_contract.py -- mine/py_ci_contract.py の単体テスト
# (mine-dispatch.yml py-ci 分岐が呼ぶ、唯一の実装に対するテスト)。
#
# 対象:
#   1. 旧 u_meas 型 plan(pipeline[0].params.primes あり)の後方互換
#      (無改変で従来動作すること -- args/done_marker/result_count_check が
#      無くても resolve_py_ci_config が legacy-primes を返すこと)。
#   2. 新型(args なし・done_marker のみ)の正常系(done)+marker 欠落
#      (failed)。
#
# stdlib のみ(unittest)。実行: python mine/test_py_ci_contract.py
# または: python -m unittest mine.test_py_ci_contract -v (repo ルートから)

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from py_ci_contract import (  # noqa: E402
    PyCiConfigError,
    determine_py_ci_verdict,
    resolve_py_ci_config,
)


def _base_job(resources_extra=None, pipeline_params=None):
    job = {
        "schema": "mine-job/v1",
        "job_id": "test-job",
        "resources": {
            "backend": "py-ci",
            "timeout_min": 10,
            "py_driver": {
                "script": "search/probe/wac_v1/u_meas_caseb_locus2.py",
                "sha256": "0" * 64,
            },
        },
        "pipeline": [{"predicate": "p", "version": 1, "params": {}}],
    }
    if resources_extra:
        job["resources"]["py_driver"].update(resources_extra)
    if pipeline_params is not None:
        job["pipeline"][0]["params"] = pipeline_params
    return job


class TestResolveLegacyPrimesBackwardCompat(unittest.TestCase):
    """旧 u_meas 型 plan(primes あり)が無改変で動くこと。"""

    def test_legacy_plan_with_no_new_fields_resolves_as_legacy(self):
        job = _base_job(pipeline_params={"primes": [7, 13, 19]})
        cfg = resolve_py_ci_config(job)
        self.assertTrue(cfg["legacy_primes_mode"])
        self.assertEqual(cfg["args"], ["7", "13", "19"])
        self.assertEqual(cfg["nprimes"], 3)
        self.assertIsNone(cfg["done_marker"])
        self.assertIsNone(cfg["rcc_marker"])
        self.assertIsNone(cfg["rcc_expect"])

    def test_legacy_plan_new_fields_present_are_ignored(self):
        # primes が存在すれば旧契約優先(新欄が紛れ込んでいても無視)。
        job = _base_job(
            resources_extra={"args": ["ignored"], "done_marker": "ignored"},
            pipeline_params={"primes": [7]},
        )
        cfg = resolve_py_ci_config(job)
        self.assertTrue(cfg["legacy_primes_mode"])
        self.assertEqual(cfg["args"], ["7"])

    def test_legacy_plan_empty_primes_is_config_error(self):
        job = _base_job(pipeline_params={"primes": []})
        with self.assertRaises(PyCiConfigError):
            resolve_py_ci_config(job)

    def test_legacy_plan_non_int_primes_is_config_error(self):
        job = _base_job(pipeline_params={"primes": ["7"]})
        with self.assertRaises(PyCiConfigError):
            resolve_py_ci_config(job)

    def test_legacy_verdict_done_matches_prior_behavior(self):
        run_log = "=== p = 7 ===\nok\n=== p = 13 ===\nok\n"
        verdict = determine_py_ci_verdict(
            legacy_primes_mode=True, py_exit_code=0, run_log_text=run_log, nprimes=2
        )
        self.assertEqual(verdict, "done")

    def test_legacy_verdict_count_mismatch_is_failed(self):
        run_log = "=== p = 7 ===\nok\n"
        verdict = determine_py_ci_verdict(
            legacy_primes_mode=True, py_exit_code=0, run_log_text=run_log, nprimes=2
        )
        self.assertEqual(verdict, "failed")

    def test_legacy_verdict_nonzero_exit_is_failed(self):
        run_log = "=== p = 7 ===\nok\n"
        verdict = determine_py_ci_verdict(
            legacy_primes_mode=True, py_exit_code=1, run_log_text=run_log, nprimes=1
        )
        self.assertEqual(verdict, "failed")


class TestGenericContract(unittest.TestCase):
    """新型(args なし・done_marker のみ)の正常系+marker 欠落 -> failed。"""

    def test_resolve_generic_no_args_default_done_marker(self):
        job = _base_job()  # primes 無し、args/done_marker/result_count_check 無し
        cfg = resolve_py_ci_config(job)
        self.assertFalse(cfg["legacy_primes_mode"])
        self.assertEqual(cfg["args"], [])
        self.assertIsNone(cfg["nprimes"])
        self.assertEqual(cfg["done_marker"], "PY_DRIVER_DONE")
        self.assertIsNone(cfg["rcc_marker"])
        self.assertIsNone(cfg["rcc_expect"])

    def test_resolve_generic_with_args_and_custom_done_marker(self):
        job = _base_job(resources_extra={"args": ["--fast"], "done_marker": "SWEEP_DONE"})
        cfg = resolve_py_ci_config(job)
        self.assertFalse(cfg["legacy_primes_mode"])
        self.assertEqual(cfg["args"], ["--fast"])
        self.assertEqual(cfg["done_marker"], "SWEEP_DONE")

    def test_resolve_generic_invalid_args_type_is_config_error(self):
        job = _base_job(resources_extra={"args": "not-a-list"})
        with self.assertRaises(PyCiConfigError):
            resolve_py_ci_config(job)

    def test_resolve_generic_result_count_check_shape(self):
        job = _base_job(
            resources_extra={"result_count_check": {"marker": "OK:", "expect": 3}}
        )
        cfg = resolve_py_ci_config(job)
        self.assertEqual(cfg["rcc_marker"], "OK:")
        self.assertEqual(cfg["rcc_expect"], 3)

    def test_resolve_generic_result_count_check_invalid_shape_is_config_error(self):
        job = _base_job(resources_extra={"result_count_check": {"marker": "OK:"}})
        with self.assertRaises(PyCiConfigError):
            resolve_py_ci_config(job)

    def test_no_script_is_config_error(self):
        job = _base_job()
        del job["resources"]["py_driver"]["script"]
        with self.assertRaises(PyCiConfigError):
            resolve_py_ci_config(job)

    def test_generic_verdict_done_marker_present_no_rcc_is_done(self):
        run_log = "some output\nPY_DRIVER_DONE\n"
        verdict = determine_py_ci_verdict(
            legacy_primes_mode=False,
            py_exit_code=0,
            run_log_text=run_log,
            done_marker="PY_DRIVER_DONE",
        )
        self.assertEqual(verdict, "done")

    def test_generic_verdict_marker_missing_is_failed(self):
        run_log = "some output without the marker\n"
        verdict = determine_py_ci_verdict(
            legacy_primes_mode=False,
            py_exit_code=0,
            run_log_text=run_log,
            done_marker="PY_DRIVER_DONE",
        )
        self.assertEqual(verdict, "failed")

    def test_generic_verdict_nonzero_exit_is_failed_even_with_marker(self):
        run_log = "PY_DRIVER_DONE\n"
        verdict = determine_py_ci_verdict(
            legacy_primes_mode=False,
            py_exit_code=1,
            run_log_text=run_log,
            done_marker="PY_DRIVER_DONE",
        )
        self.assertEqual(verdict, "failed")

    def test_generic_verdict_result_count_check_match_is_done(self):
        run_log = "OK: 1\nOK: 2\nOK: 3\nPY_DRIVER_DONE\n"
        verdict = determine_py_ci_verdict(
            legacy_primes_mode=False,
            py_exit_code=0,
            run_log_text=run_log,
            done_marker="PY_DRIVER_DONE",
            rcc_marker="OK:",
            rcc_expect=3,
        )
        self.assertEqual(verdict, "done")

    def test_generic_verdict_result_count_check_mismatch_is_failed(self):
        run_log = "OK: 1\nOK: 2\nPY_DRIVER_DONE\n"
        verdict = determine_py_ci_verdict(
            legacy_primes_mode=False,
            py_exit_code=0,
            run_log_text=run_log,
            done_marker="PY_DRIVER_DONE",
            rcc_marker="OK:",
            rcc_expect=3,
        )
        self.assertEqual(verdict, "failed")


class TestSweep744EndToEnd(unittest.TestCase):
    """search/certs/ep_sweep744/run_laneb_sweep744.py 型(args なし・
    PY_DRIVER_DONE のみ)を想定した end-to-end 相当のシナリオ。"""

    def test_sweep744_style_plan_resolves_and_verdicts_done(self):
        job = _base_job()
        job["resources"]["py_driver"]["script"] = (
            "search/certs/ep_sweep744/run_laneb_sweep744.py"
        )
        cfg = resolve_py_ci_config(job)
        self.assertEqual(cfg["args"], [])
        self.assertEqual(cfg["done_marker"], "PY_DRIVER_DONE")
        run_log = '{\n  "total": 744\n}\nPY_DRIVER_DONE\n'
        verdict = determine_py_ci_verdict(
            legacy_primes_mode=cfg["legacy_primes_mode"],
            py_exit_code=0,
            run_log_text=run_log,
            nprimes=cfg["nprimes"],
            done_marker=cfg["done_marker"],
            rcc_marker=cfg["rcc_marker"],
            rcc_expect=cfg["rcc_expect"],
        )
        self.assertEqual(verdict, "done")


if __name__ == "__main__":
    unittest.main()
