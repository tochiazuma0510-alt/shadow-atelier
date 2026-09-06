# Task1055: accepted parent1578, one k128 batch; current transitions and historical references stay separate.
import ast
import copy
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import resource
import shutil
import signal
import stat
import subprocess
import sys
import time
import traceback
import zipfile
from datetime import datetime, timezone

SCHEMA = 'd972.r07.fixed-lambda-cycle-batch.v4'
WF_SCHEMA = SCHEMA + '.workflow-v4'
ROOT = Path(os.environ['GITHUB_WORKSPACE']).resolve()
REPORT = Path(os.environ['RUNNER_TEMP']) / 'fixed-lambda-batch-v4'
INPUTS = Path(os.environ['RUNNER_TEMP']) / 'fixed-lambda-batch-v4-inputs'
OUTPUT = REPORT / 'output'
FIXTURES = REPORT / 'selftest-fixtures'
ROLES = ['state','delta','seed34','packet','refinement','oracle','e',
         'prepare','block-0','block-1','block-2','block-3','p1','task712','continuation','batch-parent']
EXPECTED_RUNTIME = {'python':os.environ['EXPECTED_PYTHON'],'numpy':os.environ['EXPECTED_NUMPY']}
REGISTRATION = {'batch_size':128,'max_batches':1,
    'selection_policy':'CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX',
    'partial_policy':'PRIVATE_PREFIX_FINAL_PHYSICAL_HEAD_ONLY','refill':False,
    'producer_limits':{'max_seconds':5400,'max_memory_mib':7168},
    'checker_limits':{'max_seconds':10800,'max_memory_mib':7168}}
SELFTEST_NAMES = ['k128-version-registration-and-types',
    'k128-full-roster-cutoff-and-restoration','batch-parent1578-admission-and-projection']
SELFTEST_REJECTIONS = {'producer-selftest':[30,10,6],'checker-selftest':[28,9,6]}
HISTORICAL_REGISTRY_PIN = {'file':'audit-historical-region-registry.json','bytes':76867,
    'sha256':'9fe3d9cf1449c3535618a8c7618c6ab6e5fa4426f0f902c419fbbf91ad873b38'}
HISTORICAL_REGISTRY_RAW = br'''{
    "schema":  "d972.r07.fixed-lambda-cycle-batch.v3.audit-registry.v1",
    "task":  1042,
    "status":  "STATIC_AUDIT_REGISTRY",
    "candidate":  false,
    "cross_checked":  false,
    "verified":  false,
    "line_contract":  {
                          "encoding":  "UTF-8",
                          "newline":  "LF",
                          "line_base":  1,
                          "last_line_inclusive":  true,
                          "include_each_line_lf":  true,
                          "normalization":  "NONE",
                          "comparison":  "EXACT_RAW_BYTES",
                          "source_execution_in_this_audit":  false
                      },
    "source_files":  [
                         {
                             "id":  "P1",
                             "side":  "P",
                             "version":  1,
                             "file":  "search/d972_r07_fixed_lambda_cycle_batch_v1.py",
                             "bytes":  213861,
                             "sha256":  "229785eb91be9852c0d4189e67806c8fc7af7e07ef1ad3ec9650044e85427591",
                             "lf":  3463,
                             "cr":  0,
                             "bom":  false,
                             "final_lf":  true,
                             "role":  "HISTORICAL_TEXT_ONLY"
                         },
                         {
                             "id":  "P2",
                             "side":  "P",
                             "version":  2,
                             "file":  "search/d972_r07_fixed_lambda_cycle_batch_v2.py",
                             "bytes":  208805,
                             "sha256":  "6626dbcad3400829baa0ac9f6ad00527ab1de002d253d41f39575f241f70d74e",
                             "lf":  3420,
                             "cr":  0,
                             "bom":  false,
                             "final_lf":  true,
                             "role":  "HISTORICAL_TEXT_ONLY"
                         },
                         {
                             "id":  "P3",
                             "side":  "P",
                             "version":  3,
                             "file":  "search/d972_r07_fixed_lambda_cycle_batch_v3.py",
                             "bytes":  209926,
                             "sha256":  "a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8",
                             "lf":  3434,
                             "cr":  0,
                             "bom":  false,
                             "final_lf":  true,
                             "role":  "CURRENT_RUN_EXECUTABLE"
                         },
                         {
                             "id":  "C1",
                             "side":  "C",
                             "version":  1,
                             "file":  "search/check_d972_r07_fixed_lambda_cycle_batch_v1.py",
                             "bytes":  181828,
                             "sha256":  "7a4289506ce78b0ea562c63c9fb0841179a5bac10bc08165b211ed83982d292f",
                             "lf":  2680,
                             "cr":  0,
                             "bom":  false,
                             "final_lf":  true,
                             "role":  "HISTORICAL_TEXT_ONLY"
                         },
                         {
                             "id":  "C2",
                             "side":  "C",
                             "version":  2,
                             "file":  "search/check_d972_r07_fixed_lambda_cycle_batch_v2.py",
                             "bytes":  177544,
                             "sha256":  "4ada8490ef931e639159b2c3522510b6fc2da82551daa9a7aa3f1a1970d0ca90",
                             "lf":  2675,
                             "cr":  0,
                             "bom":  false,
                             "final_lf":  true,
                             "role":  "HISTORICAL_TEXT_ONLY"
                         },
                         {
                             "id":  "C3",
                             "side":  "C",
                             "version":  3,
                             "file":  "search/check_d972_r07_fixed_lambda_cycle_batch_v3.py",
                             "bytes":  178914,
                             "sha256":  "1aebf6e47807466ec56426a55e34d0c7f622a5896c40184540e4d153060946d7",
                             "lf":  2695,
                             "cr":  0,
                             "bom":  false,
                             "final_lf":  true,
                             "role":  "CURRENT_RUN_EXECUTABLE"
                         }
                     ],
    "inheritance":  {
                        "status":  "STATIC_INHERITANCE_REFERENCE",
                        "arithmetic_selftest_inherited_from":  "d972-r07-fixed-lambda-cycle-batch-v1",
                        "old_mathematical_suites_rerun":  0,
                        "historical_payload_reacquired_in_this_run":  false,
                        "historical_sources_imported_or_executed_in_this_run":  false,
                        "historical_sources_report_directory":  "audit-history-sources",
                        "historical_source_ids":  [
                                                      "P1",
                                                      "P2",
                                                      "C1",
                                                      "C2"
                                                  ],
                        "current_source_ids":  [
                                                   "P3",
                                                   "C3"
                                               ],
                        "historical_source_files_are_additional_mathematical_parents":  false,
                        "candidate":  false,
                        "cross_checked":  false,
                        "verified":  false,
                        "historical_run":  {
                                               "run":  34004423047,
                                               "attempt":  1,
                                               "head":  "81a1b22975308ae0ac628f97da447a008a1d087e",
                                               "artifact":  9980697123,
                                               "zip_bytes":  94677901,
                                               "zip_sha256":  "d21f9e0b93b070327b4ef02e975dc377a8020e7f8aa7553a720d97d690ed85f0",
                                               "producer_selftest":  {
                                                                         "bytes":  2409,
                                                                         "sha256":  "1bfb8b4404d1d24e481dd139b6b84136ef21e8e79b1fd3548607a66b45d1c238"
                                                                     },
                                               "checker_selftest":  {
                                                                        "bytes":  1725,
                                                                        "sha256":  "2c8005f98883a711bece270552fa5f39f85755a8d06a27f0cf6c1b3fc257cdce"
                                                                    },
                                               "group_names":  [
                                                                   "fixed-selection-full-roster-and-aux",
                                                                   "dependent-independent-target-signs-and-packed",
                                                                   "private-prefix-publication-resume-and-isolation"
                                                               ],
                                               "producer_rejection_counts":  [
                                                                                 7,
                                                                                 6,
                                                                                 26
                                                                             ],
                                               "checker_rejection_counts":  [
                                                                                2,
                                                                                3,
                                                                                14
                                                                            ],
                                               "reference_basis":  "PUBLIC_TASK1040_ROOT_PREVIOUS_FULL_PAYLOAD_RECEPTION",
                                               "reference_is_current_run_execution":  false
                                           },
                        "unchanged_regions":  [
                                                  {
                                                      "id":  "P-core-before-workflow",
                                                      "side":  "P",
                                                      "scope":  "require through input preservation; fixed section, tree selection, selected E, reduction and durable publication",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "P1",
                                                                           "line_first":  79,
                                                                           "line_last":  2016,
                                                                           "bytes":  114836,
                                                                           "sha256":  "2c394f88247d1d767a63ac7a0529a66089b3814409a0bc474a946e6d0f1cff12"
                                                                       },
                                                                       {
                                                                           "source_id":  "P2",
                                                                           "line_first":  80,
                                                                           "line_last":  2017,
                                                                           "bytes":  114836,
                                                                           "sha256":  "2c394f88247d1d767a63ac7a0529a66089b3814409a0bc474a946e6d0f1cff12"
                                                                       },
                                                                       {
                                                                           "source_id":  "P3",
                                                                           "line_first":  80,
                                                                           "line_last":  2017,
                                                                           "bytes":  114836,
                                                                           "sha256":  "2c394f88247d1d767a63ac7a0529a66089b3814409a0bc474a946e6d0f1cff12"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "P-core-after-workflow",
                                                      "side":  "P",
                                                      "scope":  "invocation, saved prefix, recovery, result, finalizer and ordinary run_actual through pre-canary boundary",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "P1",
                                                                           "line_first":  2018,
                                                                           "line_last":  2890,
                                                                           "bytes":  56916,
                                                                           "sha256":  "be48b5ef5e519803b668a2679d5ff74be7702e7ca1c718586a65aa65db5de986"
                                                                       },
                                                                       {
                                                                           "source_id":  "P2",
                                                                           "line_first":  2019,
                                                                           "line_last":  2891,
                                                                           "bytes":  56916,
                                                                           "sha256":  "be48b5ef5e519803b668a2679d5ff74be7702e7ca1c718586a65aa65db5de986"
                                                                       },
                                                                       {
                                                                           "source_id":  "P3",
                                                                           "line_first":  2019,
                                                                           "line_last":  2891,
                                                                           "bytes":  56916,
                                                                           "sha256":  "be48b5ef5e519803b668a2679d5ff74be7702e7ca1c718586a65aa65db5de986"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "C-primitives-and-selector-signature",
                                                      "side":  "C",
                                                      "scope":  "resource boundaries, ordinary integer and packed vector types, selector signature",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "C1",
                                                                           "line_first":  138,
                                                                           "line_last":  193,
                                                                           "bytes":  2092,
                                                                           "sha256":  "910c5b1c8266de3069a40a8cf303bd8f1199ce5932dbd27e4378551a08c6b4de"
                                                                       },
                                                                       {
                                                                           "source_id":  "C2",
                                                                           "line_first":  139,
                                                                           "line_last":  194,
                                                                           "bytes":  2092,
                                                                           "sha256":  "910c5b1c8266de3069a40a8cf303bd8f1199ce5932dbd27e4378551a08c6b4de"
                                                                       },
                                                                       {
                                                                           "source_id":  "C3",
                                                                           "line_first":  139,
                                                                           "line_last":  194,
                                                                           "bytes":  2092,
                                                                           "sha256":  "910c5b1c8266de3069a40a8cf303bd8f1199ce5932dbd27e4378551a08c6b4de"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "C-selector-and-reduction-state",
                                                      "side":  "C",
                                                      "scope":  "full residual selector executable body, actual selected E interface, growing reduction and final pairing state",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "C1",
                                                                           "line_first":  195,
                                                                           "line_last":  456,
                                                                           "bytes":  14443,
                                                                           "sha256":  "a06ae680ec6064760162c24f6e862a64da6b4161dcbdb4a03b78c331044c66c3"
                                                                       },
                                                                       {
                                                                           "source_id":  "C2",
                                                                           "line_first":  196,
                                                                           "line_last":  457,
                                                                           "bytes":  14443,
                                                                           "sha256":  "a06ae680ec6064760162c24f6e862a64da6b4161dcbdb4a03b78c331044c66c3"
                                                                       },
                                                                       {
                                                                           "source_id":  "C3",
                                                                           "line_first":  196,
                                                                           "line_last":  457,
                                                                           "bytes":  14443,
                                                                           "sha256":  "a06ae680ec6064760162c24f6e862a64da6b4161dcbdb4a03b78c331044c66c3"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "C-pinned-inputs-and-root-records",
                                                      "side":  "C",
                                                      "scope":  "whole pinned readers, authenticated old physical anchor, all payload types, root records",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "C1",
                                                                           "line_first":  568,
                                                                           "line_last":  1086,
                                                                           "bytes":  33981,
                                                                           "sha256":  "24a8d482769e29d181c60c1c87681e07e4fc227fb321cc1292f217e8e84940b8"
                                                                       },
                                                                       {
                                                                           "source_id":  "C2",
                                                                           "line_first":  591,
                                                                           "line_last":  1109,
                                                                           "bytes":  33981,
                                                                           "sha256":  "24a8d482769e29d181c60c1c87681e07e4fc227fb321cc1292f217e8e84940b8"
                                                                       },
                                                                       {
                                                                           "source_id":  "C3",
                                                                           "line_first":  591,
                                                                           "line_last":  1109,
                                                                           "bytes":  33981,
                                                                           "sha256":  "24a8d482769e29d181c60c1c87681e07e4fc227fb321cc1292f217e8e84940b8"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "C-selected-tree-and-witnesses",
                                                      "side":  "C",
                                                      "scope":  "all tree payloads, full selected witness publication, current fixed oracle replay",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "C1",
                                                                           "line_first":  1102,
                                                                           "line_last":  1254,
                                                                           "bytes":  9947,
                                                                           "sha256":  "10e35b67be961b0408cf2af34497919a79da1d4f88053d6a9df996acd4ee11f1"
                                                                       },
                                                                       {
                                                                           "source_id":  "C2",
                                                                           "line_first":  1127,
                                                                           "line_last":  1279,
                                                                           "bytes":  9947,
                                                                           "sha256":  "10e35b67be961b0408cf2af34497919a79da1d4f88053d6a9df996acd4ee11f1"
                                                                       },
                                                                       {
                                                                           "source_id":  "C3",
                                                                           "line_first":  1127,
                                                                           "line_last":  1279,
                                                                           "bytes":  9947,
                                                                           "sha256":  "10e35b67be961b0408cf2af34497919a79da1d4f88053d6a9df996acd4ee11f1"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "C-candidate-replay-and-final",
                                                      "side":  "C",
                                                      "scope":  "reduction payloads, actual raw/source/primal/P1/four-B path, row/target publication, durable prefix and finalizer comparison",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "C1",
                                                                           "line_first":  1270,
                                                                           "line_last":  1720,
                                                                           "bytes":  33463,
                                                                           "sha256":  "c444459e89cb79341d3f93999a10797cf181ec33a06d1cba13609bc486fed0d8"
                                                                       },
                                                                       {
                                                                           "source_id":  "C2",
                                                                           "line_first":  1296,
                                                                           "line_last":  1746,
                                                                           "bytes":  33463,
                                                                           "sha256":  "c444459e89cb79341d3f93999a10797cf181ec33a06d1cba13609bc486fed0d8"
                                                                       },
                                                                       {
                                                                           "source_id":  "C3",
                                                                           "line_first":  1296,
                                                                           "line_last":  1746,
                                                                           "bytes":  33463,
                                                                           "sha256":  "c444459e89cb79341d3f93999a10797cf181ec33a06d1cba13609bc486fed0d8"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "C-input-result-diagnostics",
                                                      "side":  "C",
                                                      "scope":  "complete input inventories, completed-resume result binding and both saved diagnostic types",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "C1",
                                                                           "line_first":  1794,
                                                                           "line_last":  1905,
                                                                           "bytes":  8946,
                                                                           "sha256":  "5d8f1f3296d3d9350cc912571daa47a14a31ba6b78a3aafeea355b0e38f8f85a"
                                                                       },
                                                                       {
                                                                           "source_id":  "C2",
                                                                           "line_first":  1821,
                                                                           "line_last":  1932,
                                                                           "bytes":  8946,
                                                                           "sha256":  "5d8f1f3296d3d9350cc912571daa47a14a31ba6b78a3aafeea355b0e38f8f85a"
                                                                       },
                                                                       {
                                                                           "source_id":  "C3",
                                                                           "line_first":  1821,
                                                                           "line_last":  1932,
                                                                           "bytes":  8946,
                                                                           "sha256":  "5d8f1f3296d3d9350cc912571daa47a14a31ba6b78a3aafeea355b0e38f8f85a"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "C-whole-prefix-check-and-signs",
                                                      "side":  "C",
                                                      "scope":  "registered actual roster, all new payload comparison, final report, complete zero coefficients and literal signs",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "C1",
                                                                           "line_first":  1938,
                                                                           "line_last":  2166,
                                                                           "bytes":  15021,
                                                                           "sha256":  "d90ac1acd6b7a448eb87135253ccaad6a0e13cd7006b89adcfd68a2e49ed3d22"
                                                                       },
                                                                       {
                                                                           "source_id":  "C2",
                                                                           "line_first":  1966,
                                                                           "line_last":  2194,
                                                                           "bytes":  15021,
                                                                           "sha256":  "d90ac1acd6b7a448eb87135253ccaad6a0e13cd7006b89adcfd68a2e49ed3d22"
                                                                       },
                                                                       {
                                                                           "source_id":  "C3",
                                                                           "line_first":  1966,
                                                                           "line_last":  2194,
                                                                           "bytes":  15021,
                                                                           "sha256":  "d90ac1acd6b7a448eb87135253ccaad6a0e13cd7006b89adcfd68a2e49ed3d22"
                                                                       }
                                                                   ]
                                                  }
                                              ],
                        "literal_exclusions":  [
                                                   {
                                                       "id":  "P-workflow-literal",
                                                       "reason":  "Versioned launch identity, outside the two unchanged regions; not an arithmetic equality claim.",
                                                       "removed_by_normalization":  false,
                                                       "versions":  [
                                                                        {
                                                                            "source_id":  "P1",
                                                                            "line_first":  2017,
                                                                            "line_last":  2017,
                                                                            "bytes":  72,
                                                                            "sha256":  "3298b6e4b26f421d7db8bee3e0c054b61c264a5270c2f4e409306bb0e5d9236f",
                                                                            "raw_utf8":  "WORKFLOW = \".github/workflows/d972-r07-fixed-lambda-cycle-batch-v1.yml\"\n"
                                                                        },
                                                                        {
                                                                            "source_id":  "P2",
                                                                            "line_first":  2018,
                                                                            "line_last":  2018,
                                                                            "bytes":  72,
                                                                            "sha256":  "f3877af42ca5cde3943df48b6b6c615ac4899af3228ed48d4d656d9bd87ecf5e",
                                                                            "raw_utf8":  "WORKFLOW = \".github/workflows/d972-r07-fixed-lambda-cycle-batch-v2.yml\"\n"
                                                                        },
                                                                        {
                                                                            "source_id":  "P3",
                                                                            "line_first":  2018,
                                                                            "line_last":  2018,
                                                                            "bytes":  72,
                                                                            "sha256":  "dead93e7a131d185b84c2b60889b7fc375203a5f725e44dd7a8e8c0019749b16",
                                                                            "raw_utf8":  "WORKFLOW = \".github/workflows/d972-r07-fixed-lambda-cycle-batch-v3.yml\"\n"
                                                                        }
                                                                    ]
                                                   },
                                                   {
                                                       "id":  "C-selector-docstring",
                                                       "reason":  "Documentary first-k limit; executable selector body and its parameterized BATCH_SIZE use are separately registered.",
                                                       "removed_by_normalization":  false,
                                                       "versions":  [
                                                                        {
                                                                            "source_id":  "C1",
                                                                            "line_first":  194,
                                                                            "line_last":  194,
                                                                            "bytes":  86,
                                                                            "sha256":  "145f1558f73ba1e2172a5009716f2554361fbe12a29c290b7177db728e25c951",
                                                                            "raw_utf8":  "    \"\"\"Only the registered first 32 failures are offered; the whole array is read.\"\"\"\n"
                                                                        },
                                                                        {
                                                                            "source_id":  "C2",
                                                                            "line_first":  195,
                                                                            "line_last":  195,
                                                                            "bytes":  86,
                                                                            "sha256":  "03ba4ef7fa6e2c32b76245c2f02f6b6b73f0240615bb12b0a752b0ac1a1b5974",
                                                                            "raw_utf8":  "    \"\"\"Only the registered first 64 failures are offered; the whole array is read.\"\"\"\n"
                                                                        },
                                                                        {
                                                                            "source_id":  "C3",
                                                                            "line_first":  195,
                                                                            "line_last":  195,
                                                                            "bytes":  87,
                                                                            "sha256":  "f0fb80f9309dd731e391dd26d0406dbb7d0b774bd7fd030daedd192bce5bae92",
                                                                            "raw_utf8":  "    \"\"\"Only the registered first 128 failures are offered; the whole array is read.\"\"\"\n"
                                                                        }
                                                                    ]
                                                   }
                                               ],
                        "reviewed_change_regions":  [
                                                        {
                                                            "id":  "P-preamble",
                                                            "side":  "P",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "Version/schema/path, batch size 32 to 64 to 128, same one-batch no-refill scope; declarations are not byte-invariant arithmetic.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "P1",
                                                                                 "line_first":  1,
                                                                                 "line_last":  78,
                                                                                 "bytes":  3647,
                                                                                 "sha256":  "0a2a26500fe2a2f4b7ad723384f91aaa78e25eb64789b76c907b1e0d0c3e19ef"
                                                                             },
                                                                             {
                                                                                 "source_id":  "P2",
                                                                                 "line_first":  1,
                                                                                 "line_last":  79,
                                                                                 "bytes":  3688,
                                                                                 "sha256":  "630886d4e5d23bfa6ad5905b40882a356e100bf155e11d74b90c47e4fbbf632d"
                                                                             },
                                                                             {
                                                                                 "source_id":  "P3",
                                                                                 "line_first":  1,
                                                                                 "line_last":  79,
                                                                                 "bytes":  3691,
                                                                                 "sha256":  "0df29952a2358561561f8ccad49af24b599fbbc58b91962de00bac061f3cf533"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "P-canaries-cli-and-diagnostic",
                                                            "side":  "P",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "Old three suites replaced by retained-fixture two-group registration and full saved-reader tests; fresh selftest-root and diagnostic CLI; v3 adds the 128th zero-coefficient cycle-word refusal and stored full-residual truncation refusal.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "P1",
                                                                                 "line_first":  2891,
                                                                                 "line_last":  3463,
                                                                                 "bytes":  38390,
                                                                                 "sha256":  "b2004363d7452dae93a7bd234f54ef383c64374c7b5cdefd8f03a1cf97e393d7"
                                                                             },
                                                                             {
                                                                                 "source_id":  "P2",
                                                                                 "line_first":  2892,
                                                                                 "line_last":  3420,
                                                                                 "bytes":  33293,
                                                                                 "sha256":  "daea248d533cf079128aa7d743ac2ba9fb053055beaf52a898d2a17c339e7ca4"
                                                                             },
                                                                             {
                                                                                 "source_id":  "P3",
                                                                                 "line_first":  2892,
                                                                                 "line_last":  3434,
                                                                                 "bytes":  34411,
                                                                                 "sha256":  "42d4eb34c93a2547cb39e0a095b70895fcf3824d8f0421f84056edbf87be7dbb"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "C-preamble",
                                                            "side":  "C",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "Versioned schema/executable/workflow and 32 to 64 to 128 registration; unchanged accepted old64 metadata remains pinned by each whole source.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "C1",
                                                                                 "line_first":  1,
                                                                                 "line_last":  137,
                                                                                 "bytes":  9991,
                                                                                 "sha256":  "470c271899f8766a5b3b0e297a38ddb16fc255d676400c1a2411d45354d75786"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C2",
                                                                                 "line_first":  1,
                                                                                 "line_last":  138,
                                                                                 "bytes":  10076,
                                                                                 "sha256":  "821aa9049ed14d5df98e4ed8a89e266fb1bd7c00242a8e339728583ba6d76bc1"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C3",
                                                                                 "line_first":  1,
                                                                                 "line_last":  138,
                                                                                 "bytes":  10079,
                                                                                 "sha256":  "0af03569a6d0b2a897b8a2f5ebddae25b8b4e817c54857767f6bc418d368a96d"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "C-admission-extraction",
                                                            "side":  "C",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "v1 inline header and executable gates extracted in v2; strict registration helper added and called in admission and invocations; v3 helper binds k128. Whole admission block is not claimed identical.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "C1",
                                                                                 "line_first":  457,
                                                                                 "line_last":  567,
                                                                                 "bytes":  8221,
                                                                                 "sha256":  "4f29988438becbba26e74a340ecdf4d8c9a59504c29600aaf79279f7a5896bc3"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C2",
                                                                                 "line_first":  458,
                                                                                 "line_last":  590,
                                                                                 "bytes":  9269,
                                                                                 "sha256":  "f0f2645cc255151497cabd6c8bf89b25e74a01cfbcfe89ea06d90d80ca56a3d3"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C3",
                                                                                 "line_first":  458,
                                                                                 "line_last":  590,
                                                                                 "bytes":  9273,
                                                                                 "sha256":  "1492510d9904fdf88509199c9e8479596498dea6f92a0d9b193f07800d596a8d"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "C-phase-ordinal-gate",
                                                            "side":  "C",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "v2 adds strict ordinary candidate ordinal 0..BATCH_SIZE-1 before exact full payload comparison; v3 body byte-identical to v2.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "C1",
                                                                                 "line_first":  1087,
                                                                                 "line_last":  1101,
                                                                                 "bytes":  1070,
                                                                                 "sha256":  "a43f16ab658cc2a51c66972c81889553dd4cbc8f978f9935726d10eb954b83ed"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C2",
                                                                                 "line_first":  1110,
                                                                                 "line_last":  1126,
                                                                                 "bytes":  1169,
                                                                                 "sha256":  "62206cc9156991d4046225729cc0f47f8ef3dc68e098e184d554209cf40e4a7c"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C3",
                                                                                 "line_first":  1110,
                                                                                 "line_last":  1126,
                                                                                 "bytes":  1169,
                                                                                 "sha256":  "62206cc9156991d4046225729cc0f47f8ef3dc68e098e184d554209cf40e4a7c"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "C-row-offset-gate",
                                                            "side":  "C",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "v2 adds strict new-row local offset 0..BATCH_SIZE-1 before the existing accepted-row reference gate; v3 body byte-identical to v2.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "C1",
                                                                                 "line_first":  1255,
                                                                                 "line_last":  1269,
                                                                                 "bytes":  933,
                                                                                 "sha256":  "a86a40aeb7c1e69f86dd7f125eb3785ff054d0f64a493327cbe8a6b5b70863af"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C2",
                                                                                 "line_first":  1280,
                                                                                 "line_last":  1295,
                                                                                 "bytes":  1001,
                                                                                 "sha256":  "3c1f2a9d62186b1462190147f096c824af062f884d50974e2b2d689052be138a"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C3",
                                                                                 "line_first":  1280,
                                                                                 "line_last":  1295,
                                                                                 "bytes":  1001,
                                                                                 "sha256":  "3c1f2a9d62186b1462190147f096c824af062f884d50974e2b2d689052be138a"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "C-invocation-registration-and-launch",
                                                            "side":  "C",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "v2 calls strict registration helper and replaces arbitrary syntactically valid workflow name with exact registered launch; bootstrap, counts and historical binding retained; v3 body byte-identical to v2.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "C1",
                                                                                 "line_first":  1721,
                                                                                 "line_last":  1793,
                                                                                 "bytes":  5595,
                                                                                 "sha256":  "b3211f78e2f3dd49f47a52b46a5bdbf0788488e8a3af0081fb8fe1df5c46e1fb"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C2",
                                                                                 "line_first":  1747,
                                                                                 "line_last":  1820,
                                                                                 "bytes":  5594,
                                                                                 "sha256":  "22e9acf7bedbd13d57f28a871dc78ca36d9de2fdb3c988d5d662e2b49f915aa1"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C3",
                                                                                 "line_first":  1747,
                                                                                 "line_last":  1820,
                                                                                 "bytes":  5594,
                                                                                 "sha256":  "22e9acf7bedbd13d57f28a871dc78ca36d9de2fdb3c988d5d662e2b49f915aa1"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "C-registered-count-gate",
                                                            "side":  "C",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "v2 adds strict selected_count in 0..BATCH_SIZE; v3 body byte-identical to v2.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "C1",
                                                                                 "line_first":  1906,
                                                                                 "line_last":  1937,
                                                                                 "bytes":  2587,
                                                                                 "sha256":  "bf1699d8bdb8075665bd2f90a064ff587a448bbc9a4417976a33361f5cb6d08c"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C2",
                                                                                 "line_first":  1933,
                                                                                 "line_last":  1965,
                                                                                 "bytes":  2659,
                                                                                 "sha256":  "c2712937d70d9b3198e1ebd54b7d65e6cf16a30c164528571c62faf805278701"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C3",
                                                                                 "line_first":  1933,
                                                                                 "line_last":  1965,
                                                                                 "bytes":  2659,
                                                                                 "sha256":  "c2712937d70d9b3198e1ebd54b7d65e6cf16a30c164528571c62faf805278701"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "C-canaries-and-cli",
                                                            "side":  "C",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "Old three suites replaced by two retained-fixture groups; ordinary CLI/report path retained with fresh selftest-root, strict bootstrap and full saved-reader boundary coverage. New v3 28/8 refusals do not replay old mathematical suites.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "C1",
                                                                                 "line_first":  2167,
                                                                                 "line_last":  2680,
                                                                                 "bytes":  35452,
                                                                                 "sha256":  "cf5f214d68be6b8c429fdec72f7b866227c297bc2a012d78a2a54488f8ee0428"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C2",
                                                                                 "line_first":  2195,
                                                                                 "line_last":  2675,
                                                                                 "bytes":  29797,
                                                                                 "sha256":  "05e3e734302b2f0e543010a025a8ca9139e53af9949dded8e1d318a76478cf5b"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C3",
                                                                                 "line_first":  2195,
                                                                                 "line_last":  2695,
                                                                                 "bytes":  31159,
                                                                                 "sha256":  "2c9c0afa8fb1388bb1090a760c6fa54c2942a74153740c75822b1c9420a27c13"
                                                                             }
                                                                         ]
                                                        }
                                                    ],
                        "limits":  [
                                       "Unchanged function bytes remain parameterized by the separately reviewed registered batch size; equality is not a claim that all n produce the same output.",
                                       "No all-C-body identity is claimed: extraction and added gates are registered changes.",
                                       "Historical DEPENDENT/target/publication suite PASS is a reference, not a current-run pass.",
                                       "New auxiliary selftest coverage is distinct from previously unused runtime auxiliary branches.",
                                       "Whole P1-v1/P2-v2 first32 row file identity is metadata only; versioned owner/HEAD/manifest identities differ."
                                   ]
                    },
    "shared_tcb":  {
                       "status":  "DECLARED_SHARED_TCB",
                       "candidate":  false,
                       "cross_checked":  false,
                       "verified":  false,
                       "kernel_third_independence_claimed":  false,
                       "current_run_call_coverage":  "NOT_MEASURED",
                       "kernels":  [
                                       {
                                           "kernel":  "vectorized_projection_chunk",
                                           "side":  "P",
                                           "file":  "search/d972_r07_actual_grade2_root_scalar_batch_v2.py",
                                           "file_bytes":  118315,
                                           "file_sha256":  "3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856",
                                           "line_first":  342,
                                           "line_last":  357,
                                           "region_bytes":  1011,
                                           "region_sha256":  "b68bbb5af24240a8758fffa0902323727e0a22838f1acdaede8e1d1c867a5199",
                                           "kernel_third_independence_claimed":  false,
                                           "current_run_call_coverage":  "NOT_MEASURED"
                                       },
                                       {
                                           "kernel":  "vectorized_projection_chunk",
                                           "side":  "C",
                                           "file":  "search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py",
                                           "file_bytes":  119619,
                                           "file_sha256":  "e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6",
                                           "line_first":  269,
                                           "line_last":  284,
                                           "region_bytes":  1020,
                                           "region_sha256":  "6e785bdf5b4fb8b2010b3645462ffaff8d84e2ff2e2c134eafa0425c18b4beaf",
                                           "kernel_third_independence_claimed":  false,
                                           "current_run_call_coverage":  "NOT_MEASURED"
                                       },
                                       {
                                           "kernel":  "sparse_adjoint",
                                           "side":  "P",
                                           "file":  "search/d972_r07_targeted_grade2_owner_generated_join_v15.py",
                                           "file_bytes":  126565,
                                           "file_sha256":  "76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632",
                                           "line_first":  192,
                                           "line_last":  203,
                                           "region_bytes":  670,
                                           "region_sha256":  "4b75584298a67005d5af61bd972d8dfe5069b65f1dd5d32bdeb345bf2eadbd39",
                                           "kernel_third_independence_claimed":  false,
                                           "current_run_call_coverage":  "NOT_MEASURED"
                                       },
                                       {
                                           "kernel":  "sparse_adjoint",
                                           "side":  "C",
                                           "file":  "search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py",
                                           "file_bytes":  141770,
                                           "file_sha256":  "8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662",
                                           "line_first":  192,
                                           "line_last":  203,
                                           "region_bytes":  670,
                                           "region_sha256":  "4b75584298a67005d5af61bd972d8dfe5069b65f1dd5d32bdeb345bf2eadbd39",
                                           "kernel_third_independence_claimed":  false,
                                           "current_run_call_coverage":  "NOT_MEASURED"
                                       }
                                   ],
                       "known_static_load_bearing_paths":  [
                                                               {
                                                                   "kernel":  "vectorized_projection_chunk",
                                                                   "side":  "P",
                                                                   "file":  "search/d972_r07_full_origin_refinement_v1.py",
                                                                   "line":  448
                                                               },
                                                               {
                                                                   "kernel":  "vectorized_projection_chunk",
                                                                   "side":  "C",
                                                                   "file":  "search/check_d972_r07_complete_oracle_cegar_continuation_v2.py",
                                                                   "line":  236
                                                               }
                                                           ],
                       "limits":  [
                                      "sparse_adjoint current-run invocation count is not measured.",
                                      "The word Independent in a retained docstring does not establish independent arithmetic.",
                                      "Projection sides retain different docstring/error-label bytes; sparse_adjoint regions are byte-identical."
                                  ]
                   },
    "new_source_audit":  {
                             "status":  "STATIC_PASS_RUNTIME_PENDING",
                             "same_initial_completed_steps":  64,
                             "same_initial_rank":  1450,
                             "same_initial_generation":  8155,
                             "mathematical_parent_count":  15,
                             "executable_python_count":  21,
                             "raw_input_count":  3,
                             "batch_size":  128,
                             "max_batches":  1,
                             "refill":  false,
                             "selection_policy":  "CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX",
                             "new_selftest_groups":  2,
                             "producer_expected_rejections":  [
                                                                  30,
                                                                  9
                                                              ],
                             "checker_expected_rejections":  [
                                                                 28,
                                                                 8
                                                             ],
                             "new_selftests_executed_in_this_audit":  false,
                             "new_actual_arithmetic_executed_in_this_audit":  false,
                             "source_or_ast_executed_in_this_audit":  false,
                             "new_runtime_outcome":  "NOT_OBSERVED",
                             "author_replies":  [
                                                    {
                                                        "file":  "sol/luna_reply_1036_r07_fixed_lambda_k128_producer_v3.md",
                                                        "bytes":  18903,
                                                        "sha256":  "2e052e034ac22aa5108f9b02f935f3162a7a92e8c30450ba77a8e9e09d2f9881"
                                                    },
                                                    {
                                                        "file":  "sol/luna_reply_1037_r07_fixed_lambda_k128_checker_v3.md",
                                                        "bytes":  11196,
                                                        "sha256":  "eb10977969e239795d670ea9c52ae36dce1c0442f6b68a7ff8bc54b5853447ae"
                                                    }
                                                ]
                         }
}
'''
AUDIT_RECEIPTS = {
    'arithmetic-selftest-inheritance.json':('arithmetic-selftest-inheritance','STATIC_INHERITANCE_REFERENCE'),
    'shared-tcb.json':('shared-tcb','DECLARED_SHARED_TCB')}
HISTORICAL_ARITHMETIC_TESTS = {
    'arithmetic_selftest_inherited_from':'d972-r07-fixed-lambda-cycle-batch-v1',
    'launch':{'run':34004423047,'attempt':1,'head':'81a1b22975308ae0ac628f97da447a008a1d087e',
        'workflow':'.github/workflows/d972-r07-fixed-lambda-cycle-batch-v1.yml'},
    'artifact_id':9980697123,
    'archive':{'bytes':94677901,'sha256':'d21f9e0b93b070327b4ef02e975dc377a8020e7f8aa7553a720d97d690ed85f0'},
    'groups':['fixed-selection-full-roster-and-aux','dependent-independent-target-signs-and-packed',
        'private-prefix-publication-resume-and-isolation'],
    'payloads':{
        'producer':{'file':'producer-selftest-stdout.json','bytes':2409,
            'sha256':'1bfb8b4404d1d24e481dd139b6b84136ef21e8e79b1fd3548607a66b45d1c238'},
        'checker':{'file':'checker-selftest-stdout.json','bytes':1725,
            'sha256':'2c8005f98883a711bece270552fa5f39f85755a8d06a27f0cf6c1b3fc257cdce'}},
    'historical_rejection_counts':{'producer':[7,6,26],'checker':[2,3,14]},
    'historical_status':'PASS','old_mathematical_suites_rerun':0,
    'historical_payload_reacquired_in_this_run':False}
SHARED_TCB_CONTRACT = [
    {'kernel':'vectorized_projection_chunk','side':'producer',
        'source':{'file':'search/d972_r07_actual_grade2_root_scalar_batch_v2.py','bytes':118315,
            'sha256':'3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856'},
        'first_line':342,'last_line':357},
    {'kernel':'vectorized_projection_chunk','side':'checker',
        'source':{'file':'search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py','bytes':119619,
            'sha256':'e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6'},
        'first_line':269,'last_line':284},
    {'kernel':'sparse_adjoint','side':'producer',
        'source':{'file':'search/d972_r07_targeted_grade2_owner_generated_join_v15.py','bytes':126565,
            'sha256':'76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632'},
        'first_line':192,'last_line':203},
    {'kernel':'sparse_adjoint','side':'checker',
        'source':{'file':'search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py','bytes':141770,
            'sha256':'8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662'},
        'first_line':192,'last_line':203}]
COMPLETED_TERMINALS = {'BATCH_COMPLETE_CANDIDATE','COMPLETE_ZERO_CANDIDATE',
                       'LINEAR_MEMBERSHIP_CANDIDATE'}
HEX = re.compile(r'[0-9a-f]{64}\Z')
PHASES = ['raw','source','primal','p1','B','reduction']
P_DEPS = json.loads(r'[{"file":"search/d972_r07_actual_grade2_root_scalar_batch_v2.py","bytes":118315,"sha256":"3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856"},{"file":"search/d972_r07_actual_root_seed_materializer_v3.py","bytes":86643,"sha256":"36cc620bdc1b772a4eb4067f7e5b490dab851fb41213c5cd8a5487855207a332"},{"file":"search/d972_r07_complete_oracle_cegar_continuation_v1.py","bytes":126940,"sha256":"67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c"},{"file":"search/d972_r07_fixed_root_packet_loop_v2.py","bytes":84173,"sha256":"e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6"},{"file":"search/d972_r07_full_origin_refinement_v1.py","bytes":97806,"sha256":"d7e32aad9a9667c6af54ed7514d0417e48b3e363c60652ab585ce4633f2aedfa"},{"file":"search/d972_r07_rank1355_root_seed_scalars_v1.py","bytes":31578,"sha256":"973ccd1d5d0f8fa5a28294589ff655620745f0cc988c09abe8a6178593e185bb"},{"file":"search/d972_r07_section_cochain_oracle_v1.py","bytes":73290,"sha256":"4e7546eb1e8511b636527ffc0bc4c5eabf3c1bf60b32a5ae4f2a12fe975f44bb"},{"file":"search/d972_r07_selected_cycle_materializer_v1.py","bytes":88929,"sha256":"4f600aae93bf5749d15229cfdfe3e4546267f8b0a642ac46b65125a3c3164ac3"},{"file":"search/d972_r07_targeted_grade2_owner_generated_join_v15.py","bytes":126565,"sha256":"76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632"}]')
C_DEPS = json.loads(r'[{"file":"search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py","bytes":119619,"sha256":"e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6"},{"file":"search/check_d972_r07_actual_root_seed_materializer_v3.py","bytes":64626,"sha256":"eca60918eb943edddc321054f04b8547b3e88e5f7421f4de1e09ea04d7ca2701"},{"file":"search/check_d972_r07_complete_oracle_cegar_continuation_v2.py","bytes":129557,"sha256":"e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3"},{"file":"search/check_d972_r07_fixed_root_packet_loop_v2.py","bytes":66251,"sha256":"5289253a82d942d71b1ec55505d08ab772b111f2ba08e301f67387eae19b23e5"},{"file":"search/check_d972_r07_full_origin_refinement_v1.py","bytes":75083,"sha256":"1ee388c9cd39a43992bc9a6e075b087da3ae1672221a197719ea435d7d3529c2"},{"file":"search/check_d972_r07_rank1355_root_seed_scalars_v1.py","bytes":36236,"sha256":"f3c7ca2586a3734334b7d9823316601d18ab1d36561c72aa2c23c2aedfca0e62"},{"file":"search/check_d972_r07_section_cochain_oracle_v1.py","bytes":80740,"sha256":"2db166400dd819805f36b613993d4622e8365f04339ca7aef0371a28de71c967"},{"file":"search/check_d972_r07_section_cochain_oracle_v2.py","bytes":84402,"sha256":"a44ce4baaa5c73a30b5b28a76a84589f0a661f11e029b7869868d4a88706880d"},{"file":"search/check_d972_r07_selected_cycle_materializer_v1.py","bytes":103757,"sha256":"a6d52e0d12d97201f0a19f25c54e0924e3fbea89fefa3554727a7178881218b4"},{"file":"search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py","bytes":141770,"sha256":"8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662"}]')
DATA = json.loads(r'[{"file":"scratchpad/a0_paper_words_v1.json","bytes":115928,"sha256":"90ba603368307e16b27b2bad9d84847c7bedc501fab811b8919d96e3c8936893"},{"file":"scratchpad/a0_v2_words.json","bytes":106133,"sha256":"fb191e30d269b5392acbebfce914905eeb0d10ed4292eac31bbbcb928ae62612"},{"file":"scratchpad/fuda1_a0_rmax_data.g","bytes":4709,"sha256":"625b4d11ca882c9419d9e0d78510bf323a117673722b8dd9ec7d7e85554267ba"}]')
COMPLETION_ENTRIES = json.loads(r'''{
  "checker-result.json": {
    "bytes": 176622,
    "sha256": "4ef33b2d174064e2542dd07d1c838b476b549606a8be0fb2ecc4b301b1382690"
  },
  "repair-source-receipt.json": {
    "bytes": 4137,
    "sha256": "3f2c68a359c3b9200f88850432372abd78207c1cfacc39a8aeb371e184774be8"
  },
  "completion-run-receipt.json": {
    "bytes": 5006,
    "sha256": "aaa5a9900d37f9d56e72419d7073da0bec291890e6ccf940109d01168e6e77f8"
  },
  "completion-intake-receipt.json": {
    "bytes": 2218,
    "sha256": "f209153368adeb384ec94bcbd4d4f63d34c4dd175e6cc1ad50926116780f590b"
  },
  "preserved-input.json": {
    "bytes": 811910,
    "sha256": "914405978f9ad745e822e7009963a3da06f079af1bc6a6ef301119a1fa9a11ff"
  },
  "preservation-result.json": {
    "bytes": 389295,
    "sha256": "b1d465bd1af7174d1177ea9f78ee79c29d15bf1cb6f7c239b3efd6f802e53d98"
  },
  "all-parent-files-before.json": {
    "bytes": 168585,
    "sha256": "e370577d4bb30baf9d611cd13f08b392d1f4505b9810d8eaad78a9992e6ac113"
  },
  "all-parent-files-after.json": {
    "bytes": 168585,
    "sha256": "e370577d4bb30baf9d611cd13f08b392d1f4505b9810d8eaad78a9992e6ac113"
  },
  "snapshot-isolation-selftest.json": {
    "bytes": 727,
    "sha256": "ac5c37d865ee8f85dc13ddbb78878071b7d6d6abbec827827190ccedc83337c0"
  },
  "coverage-receipt.json": {
    "bytes": 86586,
    "sha256": "e0ee8b681793567e422da95a6d73475ffc8e2c8b06e6d491938218336b6d7bad"
  }
}''')
ACCEPTED_COMPLETION_ARTIFACT = json.loads(r'''{
  "run": 33988391926,
  "attempt": 1,
  "head": "22b628c0145d7d369a310179a64b88662f360b24",
  "workflow": ".github/workflows/d972-r07-complete-oracle-cegar-checker-completion-v1.yml",
  "id": 9976060093,
  "name": "d972-r07-complete-oracle-cegar-checker-completion-v1-candidate-33988391926-1",
  "bytes": 102582146,
  "sha256": "sha256:9f51b03805ca9de08669111e7aeb3acfc8169ff31cee4d27f1383c52bf5c96b1",
  "repository_id": 1312092366,
  "conclusion": "success"
}''')
# Root-observed successful resume64 pins; the empty-roster rejection below is retained.
CONTINUATION_ENTRIES = json.loads(r'''{
  "accepted-completion/checker-result.json": {
    "bytes": 176622,
    "sha256": "4ef33b2d174064e2542dd07d1c838b476b549606a8be0fb2ecc4b301b1382690"
  },
  "accepted-completion/completion-run-receipt.json": {
    "bytes": 5006,
    "sha256": "aaa5a9900d37f9d56e72419d7073da0bec291890e6ccf940109d01168e6e77f8"
  },
  "accepted-completion/coverage-receipt.json": {
    "bytes": 86586,
    "sha256": "e0ee8b681793567e422da95a6d73475ffc8e2c8b06e6d491938218336b6d7bad"
  },
  "accepted-completion/repair-source-receipt.json": {
    "bytes": 4137,
    "sha256": "3f2c68a359c3b9200f88850432372abd78207c1cfacc39a8aeb371e184774be8"
  },
  "accepted-completion/snapshot-isolation-selftest.json": {
    "bytes": 727,
    "sha256": "ac5c37d865ee8f85dc13ddbb78878071b7d6d6abbec827827190ccedc83337c0"
  },
  "all-parent-files-after.json": {
    "bytes": 593399,
    "sha256": "e89fe5fcac1ceb4bbc871d613774ac46ea00535536a891232eaf69af202d448c"
  },
  "all-parent-files-before.json": {
    "bytes": 593399,
    "sha256": "e89fe5fcac1ceb4bbc871d613774ac46ea00535536a891232eaf69af202d448c"
  },
  "before32/HEAD": {
    "bytes": 964,
    "sha256": "d489c06d40f1b06a8924558e8f751d08cd2b40259790de398b93c79f3657760b"
  },
  "before32/result.json": {
    "bytes": 28577,
    "sha256": "06c3053808179dd7706eb85fd30df8e1c360b5ee7f4640cd2a84581fe33a978a"
  },
  "checker-exit-code.txt": {
    "bytes": 2,
    "sha256": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa"
  },
  "checker-result.json": {
    "bytes": 330955,
    "sha256": "ff55c51e90acead643b9683af6f82d492c503a92c83a504a97eeb3f62c31cc4d"
  },
  "checker-stdout.json": {
    "bytes": 330955,
    "sha256": "ff55c51e90acead643b9683af6f82d492c503a92c83a504a97eeb3f62c31cc4d"
  },
  "completion-intake-receipt.json": {
    "bytes": 4878,
    "sha256": "bbb04136ff7d2d53d7940969bb696869fd79cf983b8e23e3b7fb89a3fb333d07"
  },
  "copy-before-resume.json": {
    "bytes": 778467,
    "sha256": "1475c86bf11868a9611b8562d3aeca18afce14b86d741c208c04c332847110c8"
  },
  "live-parent-intake.json": {
    "bytes": 8509,
    "sha256": "ef88ea88a491837a8fe32e120e491191037ba5c168354fae1de1c52688d29180"
  },
  "output/fixed/manifest.json": {
    "bytes": 3159,
    "sha256": "3ec178df5c2af9de7c55bb96075bb9e741111a241f7e02222ef5604587c87c41"
  },
  "output/HEAD": {
    "bytes": 964,
    "sha256": "4614d5c3fc619007879f3a5062cde90ac0cab86552ddd17ff14306bc961ac2f4"
  },
  "output/invocations/2c723e694ab1425c91308e5281031d1d.json": {
    "bytes": 738,
    "sha256": "30ab799a0166bccca1e1bfc4e8bfb13ab0ebdf3bb9152a74afc20af7ed797421"
  },
  "output/invocations/654a02070b2e4a9a99698fd6080c6035.json": {
    "bytes": 737,
    "sha256": "e004e29cde9c88fc06a0ccdcc75ed8e484419a09344893d55eae3cf54b04c82b"
  },
  "output/invocations/c1f691934ec343f8ba2de4e2819d564f.json": {
    "bytes": 737,
    "sha256": "f9217280d1563a6a8c08cec0866d9ddd98b2851cc7817aa2d1041c6b6bce376f"
  },
  "output/owner.json": {
    "bytes": 8612,
    "sha256": "e356f7d614828b9c466c70e4e446ec561de73a758b4c6a2292fdd97be39ff77b"
  },
  "output/result.json": {
    "bytes": 42785,
    "sha256": "75f76ac43c86cfae998b0f4fe757a79b500727c2bfa847849fa57dbfa05293fd"
  },
  "output/source.json": {
    "bytes": 2423,
    "sha256": "c787d53c65c6392845e6f26c545e213b6b17d9b08dc07d694a1c4e33282f2651"
  },
  "output/start.json": {
    "bytes": 54707,
    "sha256": "87bd9b89c593d68fba65b765bfe9f17bcc47d52cc9afce6f53f8c131a24f816b"
  },
  "preservation-result.json": {
    "bytes": 774326,
    "sha256": "178dc3c45a87fa848a94ed0a1c4e8b4074cb418b57892c74ffcda5197b743171"
  },
  "producer-output-before-checker.json": {
    "bytes": 774793,
    "sha256": "8ea7c0d5cdd0cef4bd7bf1beb9403041ca333a071fd4703fe90a656f993a9d02"
  },
  "producer-result.json": {
    "bytes": 42785,
    "sha256": "75f76ac43c86cfae998b0f4fe757a79b500727c2bfa847849fa57dbfa05293fd"
  },
  "resume-source-receipt.json": {
    "bytes": 4657,
    "sha256": "76c5cbd01fafb30e8ba503e27ae949f5a3e2dbb46e9108ca3d691d6d996369b0"
  },
  "run-receipt.json": {
    "bytes": 6883,
    "sha256": "ca9a42e10f207d2a57465ccdcf84b414d1a20b5170e04e38a645645fdb787694"
  },
  "source-receipt.json": {
    "bytes": 3643,
    "sha256": "3a50dd12025079a6089d15aac79573899e49692b61a53879adb9b0572342de6b"
  }
}''')

PREPARE_BODY = "1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865"
BLOCK_BODIES = ("9ebcc7ad1141c20aeaff82eb4a83a9489dc492b30220547f23526b4fcdd8dc74",
    "d783bbe6c92c15a241eb78d0b25bca5e7c00f60799ce82f6df8b1d3ee7a202f6",
    "a6dcc904fc3e9daae008f72de7e83ffadcd39055d557621b9cdf06baea0e83ac",
    "642a4ec0ad6ad4ea659e84330e34006c767ca029203446cb64a17c151fefdb01")
PRIMARY = {"state":"state/manifest.json","delta":"output/manifest.json","seed34":"output/manifest.json",
    "packet":"output/HEAD","refinement":"output/HEAD","oracle":"output/manifest.json","e":"output/manifest.json",
    "prepare":"prepare." + PREPARE_BODY + ".json","p1":"manifest.json",
    "task712":"r07-grade2-maps-v4/manifest.json","continuation":"output/HEAD",
    **{f"block-{i}":f"block-{i}.{digest}.json" for i,digest in enumerate(BLOCK_BODIES)}}
LOOP_FILES = {
    "output/HEAD": (964, "d489c06d40f1b06a8924558e8f751d08cd2b40259790de398b93c79f3657760b"),
    "output/owner.json": (8612, "e356f7d614828b9c466c70e4e446ec561de73a758b4c6a2292fdd97be39ff77b"),
    "output/source.json": (2423, "c787d53c65c6392845e6f26c545e213b6b17d9b08dc07d694a1c4e33282f2651"),
    "output/start.json": (54707, "87bd9b89c593d68fba65b765bfe9f17bcc47d52cc9afce6f53f8c131a24f816b"),
    "output/fixed/manifest.json": (3159, "3ec178df5c2af9de7c55bb96075bb9e741111a241f7e02222ef5604587c87c41"),
    "output/result.json": (28577, "06c3053808179dd7706eb85fd30df8e1c360b5ee7f4640cd2a84581fe33a978a")}
LOOP_PRODUCER = "67d2302c3c4d571a4ccbe524098fe97808f05069bfd2ed822408bde3e256733c"
LOOP_CHECKER = "e985b4ca3922fc4f89fe7c313d969bf4dd2b525fb92b4ee3ce3920888e6821e3"
LOOP_SCHEMA = 'd972.r07.complete-oracle-cegar-continuation.v1'
RAW = {entry['file']:(entry['bytes'],entry['sha256']) for entry in DATA}
FALSE_ASSURANCE = {'candidate':False,'cross_checked':False,'verified':False}
REPOSITORY = 'tochiazuma0510-alt/shadow-atelier'
BRANCH = 'sol/r07-explicit-lift-20260825'

# Full raw registry for the frozen v3-to-v4 source transitions.
INHERITANCE_REGISTRY_RAW = br'''{
  "schema": "d972.r07.fixed-lambda-cycle-batch.v4.audit-registry.v1",
  "task": 1055,
  "status": "STATIC_WORKFLOW_AUTHOR_REGISTRY",
  "candidate": false,
  "cross_checked": false,
  "verified": false,
  "line_contract": {"encoding":"UTF-8","newline":"LF","line_base":1,"last_line_inclusive":true,"include_each_line_lf":true,"normalization":"NONE","comparison":"EXACT_RAW_BYTES","source_execution_in_this_audit":false},
  "source_files": [
    {"id":"P1","side":"P","version":1,"file":"search/d972_r07_fixed_lambda_cycle_batch_v1.py","bytes":213861,"sha256":"229785eb91be9852c0d4189e67806c8fc7af7e07ef1ad3ec9650044e85427591","lf":3463,"cr":0,"bom":false,"final_lf":true,"role":"HISTORICAL_TEXT_ONLY"},
    {"id":"P2","side":"P","version":2,"file":"search/d972_r07_fixed_lambda_cycle_batch_v2.py","bytes":208805,"sha256":"6626dbcad3400829baa0ac9f6ad00527ab1de002d253d41f39575f241f70d74e","lf":3420,"cr":0,"bom":false,"final_lf":true,"role":"HISTORICAL_TEXT_ONLY"},
    {"id":"P3","side":"P","version":3,"file":"search/d972_r07_fixed_lambda_cycle_batch_v3.py","bytes":209926,"sha256":"a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8","lf":3434,"cr":0,"bom":false,"final_lf":true,"role":"HISTORICAL_TEXT_ONLY"},
    {"id":"C1","side":"C","version":1,"file":"search/check_d972_r07_fixed_lambda_cycle_batch_v1.py","bytes":181828,"sha256":"7a4289506ce78b0ea562c63c9fb0841179a5bac10bc08165b211ed83982d292f","lf":2680,"cr":0,"bom":false,"final_lf":true,"role":"HISTORICAL_TEXT_ONLY"},
    {"id":"C2","side":"C","version":2,"file":"search/check_d972_r07_fixed_lambda_cycle_batch_v2.py","bytes":177544,"sha256":"4ada8490ef931e639159b2c3522510b6fc2da82551daa9a7aa3f1a1970d0ca90","lf":2675,"cr":0,"bom":false,"final_lf":true,"role":"HISTORICAL_TEXT_ONLY"},
    {"id":"C3","side":"C","version":3,"file":"search/check_d972_r07_fixed_lambda_cycle_batch_v3.py","bytes":178914,"sha256":"1aebf6e47807466ec56426a55e34d0c7f622a5896c40184540e4d153060946d7","lf":2695,"cr":0,"bom":false,"final_lf":true,"role":"HISTORICAL_TEXT_ONLY"},
    {"id":"P4","side":"P","version":4,"file":"search/d972_r07_fixed_lambda_cycle_batch_v4.py","bytes":284974,"sha256":"3ba71767585b6a49efccb5d20bb60eb8939848669c19692a63018b9486f41d36","lf":4426,"cr":0,"bom":false,"final_lf":true,"role":"CURRENT_RUN_EXECUTABLE"},
    {"id":"C4","side":"C","version":4,"file":"search/check_d972_r07_fixed_lambda_cycle_batch_v4.py","bytes":261170,"sha256":"a29380ec00876225cc618c7025d671a3da79aea3b31b829dedba13c59ba84633","lf":3724,"cr":0,"bom":false,"final_lf":true,"role":"CURRENT_RUN_EXECUTABLE"}
  ],
  "historical_registry_pin": {"file":"audit-historical-region-registry.json","bytes":76867,"sha256":"9fe3d9cf1449c3535618a8c7618c6ab6e5fa4426f0f902c419fbbf91ad873b38"},
  "historical_registry": {
    "schema":  "d972.r07.fixed-lambda-cycle-batch.v3.audit-registry.v1",
    "task":  1042,
    "status":  "STATIC_AUDIT_REGISTRY",
    "candidate":  false,
    "cross_checked":  false,
    "verified":  false,
    "line_contract":  {
                          "encoding":  "UTF-8",
                          "newline":  "LF",
                          "line_base":  1,
                          "last_line_inclusive":  true,
                          "include_each_line_lf":  true,
                          "normalization":  "NONE",
                          "comparison":  "EXACT_RAW_BYTES",
                          "source_execution_in_this_audit":  false
                      },
    "source_files":  [
                         {
                             "id":  "P1",
                             "side":  "P",
                             "version":  1,
                             "file":  "search/d972_r07_fixed_lambda_cycle_batch_v1.py",
                             "bytes":  213861,
                             "sha256":  "229785eb91be9852c0d4189e67806c8fc7af7e07ef1ad3ec9650044e85427591",
                             "lf":  3463,
                             "cr":  0,
                             "bom":  false,
                             "final_lf":  true,
                             "role":  "HISTORICAL_TEXT_ONLY"
                         },
                         {
                             "id":  "P2",
                             "side":  "P",
                             "version":  2,
                             "file":  "search/d972_r07_fixed_lambda_cycle_batch_v2.py",
                             "bytes":  208805,
                             "sha256":  "6626dbcad3400829baa0ac9f6ad00527ab1de002d253d41f39575f241f70d74e",
                             "lf":  3420,
                             "cr":  0,
                             "bom":  false,
                             "final_lf":  true,
                             "role":  "HISTORICAL_TEXT_ONLY"
                         },
                         {
                             "id":  "P3",
                             "side":  "P",
                             "version":  3,
                             "file":  "search/d972_r07_fixed_lambda_cycle_batch_v3.py",
                             "bytes":  209926,
                             "sha256":  "a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8",
                             "lf":  3434,
                             "cr":  0,
                             "bom":  false,
                             "final_lf":  true,
                             "role":  "CURRENT_RUN_EXECUTABLE"
                         },
                         {
                             "id":  "C1",
                             "side":  "C",
                             "version":  1,
                             "file":  "search/check_d972_r07_fixed_lambda_cycle_batch_v1.py",
                             "bytes":  181828,
                             "sha256":  "7a4289506ce78b0ea562c63c9fb0841179a5bac10bc08165b211ed83982d292f",
                             "lf":  2680,
                             "cr":  0,
                             "bom":  false,
                             "final_lf":  true,
                             "role":  "HISTORICAL_TEXT_ONLY"
                         },
                         {
                             "id":  "C2",
                             "side":  "C",
                             "version":  2,
                             "file":  "search/check_d972_r07_fixed_lambda_cycle_batch_v2.py",
                             "bytes":  177544,
                             "sha256":  "4ada8490ef931e639159b2c3522510b6fc2da82551daa9a7aa3f1a1970d0ca90",
                             "lf":  2675,
                             "cr":  0,
                             "bom":  false,
                             "final_lf":  true,
                             "role":  "HISTORICAL_TEXT_ONLY"
                         },
                         {
                             "id":  "C3",
                             "side":  "C",
                             "version":  3,
                             "file":  "search/check_d972_r07_fixed_lambda_cycle_batch_v3.py",
                             "bytes":  178914,
                             "sha256":  "1aebf6e47807466ec56426a55e34d0c7f622a5896c40184540e4d153060946d7",
                             "lf":  2695,
                             "cr":  0,
                             "bom":  false,
                             "final_lf":  true,
                             "role":  "CURRENT_RUN_EXECUTABLE"
                         }
                     ],
    "inheritance":  {
                        "status":  "STATIC_INHERITANCE_REFERENCE",
                        "arithmetic_selftest_inherited_from":  "d972-r07-fixed-lambda-cycle-batch-v1",
                        "old_mathematical_suites_rerun":  0,
                        "historical_payload_reacquired_in_this_run":  false,
                        "historical_sources_imported_or_executed_in_this_run":  false,
                        "historical_sources_report_directory":  "audit-history-sources",
                        "historical_source_ids":  [
                                                      "P1",
                                                      "P2",
                                                      "C1",
                                                      "C2"
                                                  ],
                        "current_source_ids":  [
                                                   "P3",
                                                   "C3"
                                               ],
                        "historical_source_files_are_additional_mathematical_parents":  false,
                        "candidate":  false,
                        "cross_checked":  false,
                        "verified":  false,
                        "historical_run":  {
                                               "run":  34004423047,
                                               "attempt":  1,
                                               "head":  "81a1b22975308ae0ac628f97da447a008a1d087e",
                                               "artifact":  9980697123,
                                               "zip_bytes":  94677901,
                                               "zip_sha256":  "d21f9e0b93b070327b4ef02e975dc377a8020e7f8aa7553a720d97d690ed85f0",
                                               "producer_selftest":  {
                                                                         "bytes":  2409,
                                                                         "sha256":  "1bfb8b4404d1d24e481dd139b6b84136ef21e8e79b1fd3548607a66b45d1c238"
                                                                     },
                                               "checker_selftest":  {
                                                                        "bytes":  1725,
                                                                        "sha256":  "2c8005f98883a711bece270552fa5f39f85755a8d06a27f0cf6c1b3fc257cdce"
                                                                    },
                                               "group_names":  [
                                                                   "fixed-selection-full-roster-and-aux",
                                                                   "dependent-independent-target-signs-and-packed",
                                                                   "private-prefix-publication-resume-and-isolation"
                                                               ],
                                               "producer_rejection_counts":  [
                                                                                 7,
                                                                                 6,
                                                                                 26
                                                                             ],
                                               "checker_rejection_counts":  [
                                                                                2,
                                                                                3,
                                                                                14
                                                                            ],
                                               "reference_basis":  "PUBLIC_TASK1040_ROOT_PREVIOUS_FULL_PAYLOAD_RECEPTION",
                                               "reference_is_current_run_execution":  false
                                           },
                        "unchanged_regions":  [
                                                  {
                                                      "id":  "P-core-before-workflow",
                                                      "side":  "P",
                                                      "scope":  "require through input preservation; fixed section, tree selection, selected E, reduction and durable publication",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "P1",
                                                                           "line_first":  79,
                                                                           "line_last":  2016,
                                                                           "bytes":  114836,
                                                                           "sha256":  "2c394f88247d1d767a63ac7a0529a66089b3814409a0bc474a946e6d0f1cff12"
                                                                       },
                                                                       {
                                                                           "source_id":  "P2",
                                                                           "line_first":  80,
                                                                           "line_last":  2017,
                                                                           "bytes":  114836,
                                                                           "sha256":  "2c394f88247d1d767a63ac7a0529a66089b3814409a0bc474a946e6d0f1cff12"
                                                                       },
                                                                       {
                                                                           "source_id":  "P3",
                                                                           "line_first":  80,
                                                                           "line_last":  2017,
                                                                           "bytes":  114836,
                                                                           "sha256":  "2c394f88247d1d767a63ac7a0529a66089b3814409a0bc474a946e6d0f1cff12"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "P-core-after-workflow",
                                                      "side":  "P",
                                                      "scope":  "invocation, saved prefix, recovery, result, finalizer and ordinary run_actual through pre-canary boundary",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "P1",
                                                                           "line_first":  2018,
                                                                           "line_last":  2890,
                                                                           "bytes":  56916,
                                                                           "sha256":  "be48b5ef5e519803b668a2679d5ff74be7702e7ca1c718586a65aa65db5de986"
                                                                       },
                                                                       {
                                                                           "source_id":  "P2",
                                                                           "line_first":  2019,
                                                                           "line_last":  2891,
                                                                           "bytes":  56916,
                                                                           "sha256":  "be48b5ef5e519803b668a2679d5ff74be7702e7ca1c718586a65aa65db5de986"
                                                                       },
                                                                       {
                                                                           "source_id":  "P3",
                                                                           "line_first":  2019,
                                                                           "line_last":  2891,
                                                                           "bytes":  56916,
                                                                           "sha256":  "be48b5ef5e519803b668a2679d5ff74be7702e7ca1c718586a65aa65db5de986"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "C-primitives-and-selector-signature",
                                                      "side":  "C",
                                                      "scope":  "resource boundaries, ordinary integer and packed vector types, selector signature",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "C1",
                                                                           "line_first":  138,
                                                                           "line_last":  193,
                                                                           "bytes":  2092,
                                                                           "sha256":  "910c5b1c8266de3069a40a8cf303bd8f1199ce5932dbd27e4378551a08c6b4de"
                                                                       },
                                                                       {
                                                                           "source_id":  "C2",
                                                                           "line_first":  139,
                                                                           "line_last":  194,
                                                                           "bytes":  2092,
                                                                           "sha256":  "910c5b1c8266de3069a40a8cf303bd8f1199ce5932dbd27e4378551a08c6b4de"
                                                                       },
                                                                       {
                                                                           "source_id":  "C3",
                                                                           "line_first":  139,
                                                                           "line_last":  194,
                                                                           "bytes":  2092,
                                                                           "sha256":  "910c5b1c8266de3069a40a8cf303bd8f1199ce5932dbd27e4378551a08c6b4de"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "C-selector-and-reduction-state",
                                                      "side":  "C",
                                                      "scope":  "full residual selector executable body, actual selected E interface, growing reduction and final pairing state",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "C1",
                                                                           "line_first":  195,
                                                                           "line_last":  456,
                                                                           "bytes":  14443,
                                                                           "sha256":  "a06ae680ec6064760162c24f6e862a64da6b4161dcbdb4a03b78c331044c66c3"
                                                                       },
                                                                       {
                                                                           "source_id":  "C2",
                                                                           "line_first":  196,
                                                                           "line_last":  457,
                                                                           "bytes":  14443,
                                                                           "sha256":  "a06ae680ec6064760162c24f6e862a64da6b4161dcbdb4a03b78c331044c66c3"
                                                                       },
                                                                       {
                                                                           "source_id":  "C3",
                                                                           "line_first":  196,
                                                                           "line_last":  457,
                                                                           "bytes":  14443,
                                                                           "sha256":  "a06ae680ec6064760162c24f6e862a64da6b4161dcbdb4a03b78c331044c66c3"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "C-pinned-inputs-and-root-records",
                                                      "side":  "C",
                                                      "scope":  "whole pinned readers, authenticated old physical anchor, all payload types, root records",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "C1",
                                                                           "line_first":  568,
                                                                           "line_last":  1086,
                                                                           "bytes":  33981,
                                                                           "sha256":  "24a8d482769e29d181c60c1c87681e07e4fc227fb321cc1292f217e8e84940b8"
                                                                       },
                                                                       {
                                                                           "source_id":  "C2",
                                                                           "line_first":  591,
                                                                           "line_last":  1109,
                                                                           "bytes":  33981,
                                                                           "sha256":  "24a8d482769e29d181c60c1c87681e07e4fc227fb321cc1292f217e8e84940b8"
                                                                       },
                                                                       {
                                                                           "source_id":  "C3",
                                                                           "line_first":  591,
                                                                           "line_last":  1109,
                                                                           "bytes":  33981,
                                                                           "sha256":  "24a8d482769e29d181c60c1c87681e07e4fc227fb321cc1292f217e8e84940b8"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "C-selected-tree-and-witnesses",
                                                      "side":  "C",
                                                      "scope":  "all tree payloads, full selected witness publication, current fixed oracle replay",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "C1",
                                                                           "line_first":  1102,
                                                                           "line_last":  1254,
                                                                           "bytes":  9947,
                                                                           "sha256":  "10e35b67be961b0408cf2af34497919a79da1d4f88053d6a9df996acd4ee11f1"
                                                                       },
                                                                       {
                                                                           "source_id":  "C2",
                                                                           "line_first":  1127,
                                                                           "line_last":  1279,
                                                                           "bytes":  9947,
                                                                           "sha256":  "10e35b67be961b0408cf2af34497919a79da1d4f88053d6a9df996acd4ee11f1"
                                                                       },
                                                                       {
                                                                           "source_id":  "C3",
                                                                           "line_first":  1127,
                                                                           "line_last":  1279,
                                                                           "bytes":  9947,
                                                                           "sha256":  "10e35b67be961b0408cf2af34497919a79da1d4f88053d6a9df996acd4ee11f1"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "C-candidate-replay-and-final",
                                                      "side":  "C",
                                                      "scope":  "reduction payloads, actual raw/source/primal/P1/four-B path, row/target publication, durable prefix and finalizer comparison",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "C1",
                                                                           "line_first":  1270,
                                                                           "line_last":  1720,
                                                                           "bytes":  33463,
                                                                           "sha256":  "c444459e89cb79341d3f93999a10797cf181ec33a06d1cba13609bc486fed0d8"
                                                                       },
                                                                       {
                                                                           "source_id":  "C2",
                                                                           "line_first":  1296,
                                                                           "line_last":  1746,
                                                                           "bytes":  33463,
                                                                           "sha256":  "c444459e89cb79341d3f93999a10797cf181ec33a06d1cba13609bc486fed0d8"
                                                                       },
                                                                       {
                                                                           "source_id":  "C3",
                                                                           "line_first":  1296,
                                                                           "line_last":  1746,
                                                                           "bytes":  33463,
                                                                           "sha256":  "c444459e89cb79341d3f93999a10797cf181ec33a06d1cba13609bc486fed0d8"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "C-input-result-diagnostics",
                                                      "side":  "C",
                                                      "scope":  "complete input inventories, completed-resume result binding and both saved diagnostic types",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "C1",
                                                                           "line_first":  1794,
                                                                           "line_last":  1905,
                                                                           "bytes":  8946,
                                                                           "sha256":  "5d8f1f3296d3d9350cc912571daa47a14a31ba6b78a3aafeea355b0e38f8f85a"
                                                                       },
                                                                       {
                                                                           "source_id":  "C2",
                                                                           "line_first":  1821,
                                                                           "line_last":  1932,
                                                                           "bytes":  8946,
                                                                           "sha256":  "5d8f1f3296d3d9350cc912571daa47a14a31ba6b78a3aafeea355b0e38f8f85a"
                                                                       },
                                                                       {
                                                                           "source_id":  "C3",
                                                                           "line_first":  1821,
                                                                           "line_last":  1932,
                                                                           "bytes":  8946,
                                                                           "sha256":  "5d8f1f3296d3d9350cc912571daa47a14a31ba6b78a3aafeea355b0e38f8f85a"
                                                                       }
                                                                   ]
                                                  },
                                                  {
                                                      "id":  "C-whole-prefix-check-and-signs",
                                                      "side":  "C",
                                                      "scope":  "registered actual roster, all new payload comparison, final report, complete zero coefficients and literal signs",
                                                      "comparison":  "EXACT_RAW_BYTES_ALL_THREE_VERSIONS",
                                                      "normalization":  "NONE",
                                                      "versions":  [
                                                                       {
                                                                           "source_id":  "C1",
                                                                           "line_first":  1938,
                                                                           "line_last":  2166,
                                                                           "bytes":  15021,
                                                                           "sha256":  "d90ac1acd6b7a448eb87135253ccaad6a0e13cd7006b89adcfd68a2e49ed3d22"
                                                                       },
                                                                       {
                                                                           "source_id":  "C2",
                                                                           "line_first":  1966,
                                                                           "line_last":  2194,
                                                                           "bytes":  15021,
                                                                           "sha256":  "d90ac1acd6b7a448eb87135253ccaad6a0e13cd7006b89adcfd68a2e49ed3d22"
                                                                       },
                                                                       {
                                                                           "source_id":  "C3",
                                                                           "line_first":  1966,
                                                                           "line_last":  2194,
                                                                           "bytes":  15021,
                                                                           "sha256":  "d90ac1acd6b7a448eb87135253ccaad6a0e13cd7006b89adcfd68a2e49ed3d22"
                                                                       }
                                                                   ]
                                                  }
                                              ],
                        "literal_exclusions":  [
                                                   {
                                                       "id":  "P-workflow-literal",
                                                       "reason":  "Versioned launch identity, outside the two unchanged regions; not an arithmetic equality claim.",
                                                       "removed_by_normalization":  false,
                                                       "versions":  [
                                                                        {
                                                                            "source_id":  "P1",
                                                                            "line_first":  2017,
                                                                            "line_last":  2017,
                                                                            "bytes":  72,
                                                                            "sha256":  "3298b6e4b26f421d7db8bee3e0c054b61c264a5270c2f4e409306bb0e5d9236f",
                                                                            "raw_utf8":  "WORKFLOW = \".github/workflows/d972-r07-fixed-lambda-cycle-batch-v1.yml\"\n"
                                                                        },
                                                                        {
                                                                            "source_id":  "P2",
                                                                            "line_first":  2018,
                                                                            "line_last":  2018,
                                                                            "bytes":  72,
                                                                            "sha256":  "f3877af42ca5cde3943df48b6b6c615ac4899af3228ed48d4d656d9bd87ecf5e",
                                                                            "raw_utf8":  "WORKFLOW = \".github/workflows/d972-r07-fixed-lambda-cycle-batch-v2.yml\"\n"
                                                                        },
                                                                        {
                                                                            "source_id":  "P3",
                                                                            "line_first":  2018,
                                                                            "line_last":  2018,
                                                                            "bytes":  72,
                                                                            "sha256":  "dead93e7a131d185b84c2b60889b7fc375203a5f725e44dd7a8e8c0019749b16",
                                                                            "raw_utf8":  "WORKFLOW = \".github/workflows/d972-r07-fixed-lambda-cycle-batch-v3.yml\"\n"
                                                                        }
                                                                    ]
                                                   },
                                                   {
                                                       "id":  "C-selector-docstring",
                                                       "reason":  "Documentary first-k limit; executable selector body and its parameterized BATCH_SIZE use are separately registered.",
                                                       "removed_by_normalization":  false,
                                                       "versions":  [
                                                                        {
                                                                            "source_id":  "C1",
                                                                            "line_first":  194,
                                                                            "line_last":  194,
                                                                            "bytes":  86,
                                                                            "sha256":  "145f1558f73ba1e2172a5009716f2554361fbe12a29c290b7177db728e25c951",
                                                                            "raw_utf8":  "    \"\"\"Only the registered first 32 failures are offered; the whole array is read.\"\"\"\n"
                                                                        },
                                                                        {
                                                                            "source_id":  "C2",
                                                                            "line_first":  195,
                                                                            "line_last":  195,
                                                                            "bytes":  86,
                                                                            "sha256":  "03ba4ef7fa6e2c32b76245c2f02f6b6b73f0240615bb12b0a752b0ac1a1b5974",
                                                                            "raw_utf8":  "    \"\"\"Only the registered first 64 failures are offered; the whole array is read.\"\"\"\n"
                                                                        },
                                                                        {
                                                                            "source_id":  "C3",
                                                                            "line_first":  195,
                                                                            "line_last":  195,
                                                                            "bytes":  87,
                                                                            "sha256":  "f0fb80f9309dd731e391dd26d0406dbb7d0b774bd7fd030daedd192bce5bae92",
                                                                            "raw_utf8":  "    \"\"\"Only the registered first 128 failures are offered; the whole array is read.\"\"\"\n"
                                                                        }
                                                                    ]
                                                   }
                                               ],
                        "reviewed_change_regions":  [
                                                        {
                                                            "id":  "P-preamble",
                                                            "side":  "P",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "Version/schema/path, batch size 32 to 64 to 128, same one-batch no-refill scope; declarations are not byte-invariant arithmetic.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "P1",
                                                                                 "line_first":  1,
                                                                                 "line_last":  78,
                                                                                 "bytes":  3647,
                                                                                 "sha256":  "0a2a26500fe2a2f4b7ad723384f91aaa78e25eb64789b76c907b1e0d0c3e19ef"
                                                                             },
                                                                             {
                                                                                 "source_id":  "P2",
                                                                                 "line_first":  1,
                                                                                 "line_last":  79,
                                                                                 "bytes":  3688,
                                                                                 "sha256":  "630886d4e5d23bfa6ad5905b40882a356e100bf155e11d74b90c47e4fbbf632d"
                                                                             },
                                                                             {
                                                                                 "source_id":  "P3",
                                                                                 "line_first":  1,
                                                                                 "line_last":  79,
                                                                                 "bytes":  3691,
                                                                                 "sha256":  "0df29952a2358561561f8ccad49af24b599fbbc58b91962de00bac061f3cf533"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "P-canaries-cli-and-diagnostic",
                                                            "side":  "P",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "Old three suites replaced by retained-fixture two-group registration and full saved-reader tests; fresh selftest-root and diagnostic CLI; v3 adds the 128th zero-coefficient cycle-word refusal and stored full-residual truncation refusal.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "P1",
                                                                                 "line_first":  2891,
                                                                                 "line_last":  3463,
                                                                                 "bytes":  38390,
                                                                                 "sha256":  "b2004363d7452dae93a7bd234f54ef383c64374c7b5cdefd8f03a1cf97e393d7"
                                                                             },
                                                                             {
                                                                                 "source_id":  "P2",
                                                                                 "line_first":  2892,
                                                                                 "line_last":  3420,
                                                                                 "bytes":  33293,
                                                                                 "sha256":  "daea248d533cf079128aa7d743ac2ba9fb053055beaf52a898d2a17c339e7ca4"
                                                                             },
                                                                             {
                                                                                 "source_id":  "P3",
                                                                                 "line_first":  2892,
                                                                                 "line_last":  3434,
                                                                                 "bytes":  34411,
                                                                                 "sha256":  "42d4eb34c93a2547cb39e0a095b70895fcf3824d8f0421f84056edbf87be7dbb"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "C-preamble",
                                                            "side":  "C",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "Versioned schema/executable/workflow and 32 to 64 to 128 registration; unchanged accepted old64 metadata remains pinned by each whole source.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "C1",
                                                                                 "line_first":  1,
                                                                                 "line_last":  137,
                                                                                 "bytes":  9991,
                                                                                 "sha256":  "470c271899f8766a5b3b0e297a38ddb16fc255d676400c1a2411d45354d75786"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C2",
                                                                                 "line_first":  1,
                                                                                 "line_last":  138,
                                                                                 "bytes":  10076,
                                                                                 "sha256":  "821aa9049ed14d5df98e4ed8a89e266fb1bd7c00242a8e339728583ba6d76bc1"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C3",
                                                                                 "line_first":  1,
                                                                                 "line_last":  138,
                                                                                 "bytes":  10079,
                                                                                 "sha256":  "0af03569a6d0b2a897b8a2f5ebddae25b8b4e817c54857767f6bc418d368a96d"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "C-admission-extraction",
                                                            "side":  "C",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "v1 inline header and executable gates extracted in v2; strict registration helper added and called in admission and invocations; v3 helper binds k128. Whole admission block is not claimed identical.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "C1",
                                                                                 "line_first":  457,
                                                                                 "line_last":  567,
                                                                                 "bytes":  8221,
                                                                                 "sha256":  "4f29988438becbba26e74a340ecdf4d8c9a59504c29600aaf79279f7a5896bc3"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C2",
                                                                                 "line_first":  458,
                                                                                 "line_last":  590,
                                                                                 "bytes":  9269,
                                                                                 "sha256":  "f0f2645cc255151497cabd6c8bf89b25e74a01cfbcfe89ea06d90d80ca56a3d3"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C3",
                                                                                 "line_first":  458,
                                                                                 "line_last":  590,
                                                                                 "bytes":  9273,
                                                                                 "sha256":  "1492510d9904fdf88509199c9e8479596498dea6f92a0d9b193f07800d596a8d"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "C-phase-ordinal-gate",
                                                            "side":  "C",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "v2 adds strict ordinary candidate ordinal 0..BATCH_SIZE-1 before exact full payload comparison; v3 body byte-identical to v2.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "C1",
                                                                                 "line_first":  1087,
                                                                                 "line_last":  1101,
                                                                                 "bytes":  1070,
                                                                                 "sha256":  "a43f16ab658cc2a51c66972c81889553dd4cbc8f978f9935726d10eb954b83ed"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C2",
                                                                                 "line_first":  1110,
                                                                                 "line_last":  1126,
                                                                                 "bytes":  1169,
                                                                                 "sha256":  "62206cc9156991d4046225729cc0f47f8ef3dc68e098e184d554209cf40e4a7c"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C3",
                                                                                 "line_first":  1110,
                                                                                 "line_last":  1126,
                                                                                 "bytes":  1169,
                                                                                 "sha256":  "62206cc9156991d4046225729cc0f47f8ef3dc68e098e184d554209cf40e4a7c"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "C-row-offset-gate",
                                                            "side":  "C",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "v2 adds strict new-row local offset 0..BATCH_SIZE-1 before the existing accepted-row reference gate; v3 body byte-identical to v2.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "C1",
                                                                                 "line_first":  1255,
                                                                                 "line_last":  1269,
                                                                                 "bytes":  933,
                                                                                 "sha256":  "a86a40aeb7c1e69f86dd7f125eb3785ff054d0f64a493327cbe8a6b5b70863af"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C2",
                                                                                 "line_first":  1280,
                                                                                 "line_last":  1295,
                                                                                 "bytes":  1001,
                                                                                 "sha256":  "3c1f2a9d62186b1462190147f096c824af062f884d50974e2b2d689052be138a"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C3",
                                                                                 "line_first":  1280,
                                                                                 "line_last":  1295,
                                                                                 "bytes":  1001,
                                                                                 "sha256":  "3c1f2a9d62186b1462190147f096c824af062f884d50974e2b2d689052be138a"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "C-invocation-registration-and-launch",
                                                            "side":  "C",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "v2 calls strict registration helper and replaces arbitrary syntactically valid workflow name with exact registered launch; bootstrap, counts and historical binding retained; v3 body byte-identical to v2.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "C1",
                                                                                 "line_first":  1721,
                                                                                 "line_last":  1793,
                                                                                 "bytes":  5595,
                                                                                 "sha256":  "b3211f78e2f3dd49f47a52b46a5bdbf0788488e8a3af0081fb8fe1df5c46e1fb"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C2",
                                                                                 "line_first":  1747,
                                                                                 "line_last":  1820,
                                                                                 "bytes":  5594,
                                                                                 "sha256":  "22e9acf7bedbd13d57f28a871dc78ca36d9de2fdb3c988d5d662e2b49f915aa1"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C3",
                                                                                 "line_first":  1747,
                                                                                 "line_last":  1820,
                                                                                 "bytes":  5594,
                                                                                 "sha256":  "22e9acf7bedbd13d57f28a871dc78ca36d9de2fdb3c988d5d662e2b49f915aa1"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "C-registered-count-gate",
                                                            "side":  "C",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "v2 adds strict selected_count in 0..BATCH_SIZE; v3 body byte-identical to v2.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "C1",
                                                                                 "line_first":  1906,
                                                                                 "line_last":  1937,
                                                                                 "bytes":  2587,
                                                                                 "sha256":  "bf1699d8bdb8075665bd2f90a064ff587a448bbc9a4417976a33361f5cb6d08c"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C2",
                                                                                 "line_first":  1933,
                                                                                 "line_last":  1965,
                                                                                 "bytes":  2659,
                                                                                 "sha256":  "c2712937d70d9b3198e1ebd54b7d65e6cf16a30c164528571c62faf805278701"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C3",
                                                                                 "line_first":  1933,
                                                                                 "line_last":  1965,
                                                                                 "bytes":  2659,
                                                                                 "sha256":  "c2712937d70d9b3198e1ebd54b7d65e6cf16a30c164528571c62faf805278701"
                                                                             }
                                                                         ]
                                                        },
                                                        {
                                                            "id":  "C-canaries-and-cli",
                                                            "side":  "C",
                                                            "disposition":  "STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY",
                                                            "reason":  "Old three suites replaced by two retained-fixture groups; ordinary CLI/report path retained with fresh selftest-root, strict bootstrap and full saved-reader boundary coverage. New v3 28/8 refusals do not replay old mathematical suites.",
                                                            "versions":  [
                                                                             {
                                                                                 "source_id":  "C1",
                                                                                 "line_first":  2167,
                                                                                 "line_last":  2680,
                                                                                 "bytes":  35452,
                                                                                 "sha256":  "cf5f214d68be6b8c429fdec72f7b866227c297bc2a012d78a2a54488f8ee0428"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C2",
                                                                                 "line_first":  2195,
                                                                                 "line_last":  2675,
                                                                                 "bytes":  29797,
                                                                                 "sha256":  "05e3e734302b2f0e543010a025a8ca9139e53af9949dded8e1d318a76478cf5b"
                                                                             },
                                                                             {
                                                                                 "source_id":  "C3",
                                                                                 "line_first":  2195,
                                                                                 "line_last":  2695,
                                                                                 "bytes":  31159,
                                                                                 "sha256":  "2c9c0afa8fb1388bb1090a760c6fa54c2942a74153740c75822b1c9420a27c13"
                                                                             }
                                                                         ]
                                                        }
                                                    ],
                        "limits":  [
                                       "Unchanged function bytes remain parameterized by the separately reviewed registered batch size; equality is not a claim that all n produce the same output.",
                                       "No all-C-body identity is claimed: extraction and added gates are registered changes.",
                                       "Historical DEPENDENT/target/publication suite PASS is a reference, not a current-run pass.",
                                       "New auxiliary selftest coverage is distinct from previously unused runtime auxiliary branches.",
                                       "Whole P1-v1/P2-v2 first32 row file identity is metadata only; versioned owner/HEAD/manifest identities differ."
                                   ]
                    },
    "shared_tcb":  {
                       "status":  "DECLARED_SHARED_TCB",
                       "candidate":  false,
                       "cross_checked":  false,
                       "verified":  false,
                       "kernel_third_independence_claimed":  false,
                       "current_run_call_coverage":  "NOT_MEASURED",
                       "kernels":  [
                                       {
                                           "kernel":  "vectorized_projection_chunk",
                                           "side":  "P",
                                           "file":  "search/d972_r07_actual_grade2_root_scalar_batch_v2.py",
                                           "file_bytes":  118315,
                                           "file_sha256":  "3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856",
                                           "line_first":  342,
                                           "line_last":  357,
                                           "region_bytes":  1011,
                                           "region_sha256":  "b68bbb5af24240a8758fffa0902323727e0a22838f1acdaede8e1d1c867a5199",
                                           "kernel_third_independence_claimed":  false,
                                           "current_run_call_coverage":  "NOT_MEASURED"
                                       },
                                       {
                                           "kernel":  "vectorized_projection_chunk",
                                           "side":  "C",
                                           "file":  "search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py",
                                           "file_bytes":  119619,
                                           "file_sha256":  "e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6",
                                           "line_first":  269,
                                           "line_last":  284,
                                           "region_bytes":  1020,
                                           "region_sha256":  "6e785bdf5b4fb8b2010b3645462ffaff8d84e2ff2e2c134eafa0425c18b4beaf",
                                           "kernel_third_independence_claimed":  false,
                                           "current_run_call_coverage":  "NOT_MEASURED"
                                       },
                                       {
                                           "kernel":  "sparse_adjoint",
                                           "side":  "P",
                                           "file":  "search/d972_r07_targeted_grade2_owner_generated_join_v15.py",
                                           "file_bytes":  126565,
                                           "file_sha256":  "76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632",
                                           "line_first":  192,
                                           "line_last":  203,
                                           "region_bytes":  670,
                                           "region_sha256":  "4b75584298a67005d5af61bd972d8dfe5069b65f1dd5d32bdeb345bf2eadbd39",
                                           "kernel_third_independence_claimed":  false,
                                           "current_run_call_coverage":  "NOT_MEASURED"
                                       },
                                       {
                                           "kernel":  "sparse_adjoint",
                                           "side":  "C",
                                           "file":  "search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py",
                                           "file_bytes":  141770,
                                           "file_sha256":  "8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662",
                                           "line_first":  192,
                                           "line_last":  203,
                                           "region_bytes":  670,
                                           "region_sha256":  "4b75584298a67005d5af61bd972d8dfe5069b65f1dd5d32bdeb345bf2eadbd39",
                                           "kernel_third_independence_claimed":  false,
                                           "current_run_call_coverage":  "NOT_MEASURED"
                                       }
                                   ],
                       "known_static_load_bearing_paths":  [
                                                               {
                                                                   "kernel":  "vectorized_projection_chunk",
                                                                   "side":  "P",
                                                                   "file":  "search/d972_r07_full_origin_refinement_v1.py",
                                                                   "line":  448
                                                               },
                                                               {
                                                                   "kernel":  "vectorized_projection_chunk",
                                                                   "side":  "C",
                                                                   "file":  "search/check_d972_r07_complete_oracle_cegar_continuation_v2.py",
                                                                   "line":  236
                                                               }
                                                           ],
                       "limits":  [
                                      "sparse_adjoint current-run invocation count is not measured.",
                                      "The word Independent in a retained docstring does not establish independent arithmetic.",
                                      "Projection sides retain different docstring/error-label bytes; sparse_adjoint regions are byte-identical."
                                  ]
                   },
    "new_source_audit":  {
                             "status":  "STATIC_PASS_RUNTIME_PENDING",
                             "same_initial_completed_steps":  64,
                             "same_initial_rank":  1450,
                             "same_initial_generation":  8155,
                             "mathematical_parent_count":  15,
                             "executable_python_count":  21,
                             "raw_input_count":  3,
                             "batch_size":  128,
                             "max_batches":  1,
                             "refill":  false,
                             "selection_policy":  "CHORD_FIRST_ROSTER_128_THEN_FIRST_AUX",
                             "new_selftest_groups":  2,
                             "producer_expected_rejections":  [
                                                                  30,
                                                                  9
                                                              ],
                             "checker_expected_rejections":  [
                                                                 28,
                                                                 8
                                                             ],
                             "new_selftests_executed_in_this_audit":  false,
                             "new_actual_arithmetic_executed_in_this_audit":  false,
                             "source_or_ast_executed_in_this_audit":  false,
                             "new_runtime_outcome":  "NOT_OBSERVED",
                             "author_replies":  [
                                                    {
                                                        "file":  "sol/luna_reply_1036_r07_fixed_lambda_k128_producer_v3.md",
                                                        "bytes":  18903,
                                                        "sha256":  "2e052e034ac22aa5108f9b02f935f3162a7a92e8c30450ba77a8e9e09d2f9881"
                                                    },
                                                    {
                                                        "file":  "sol/luna_reply_1037_r07_fixed_lambda_k128_checker_v3.md",
                                                        "bytes":  11196,
                                                        "sha256":  "eb10977969e239795d670ea9c52ae36dce1c0442f6b68a7ff8bc54b5853447ae"
                                                    }
                                                ]
                         }
},
  "inheritance": {"status":"STATIC_INHERITANCE_REFERENCE","historical_source_ids":["P1","P2","P3","C1","C2","C3"],"current_source_ids":["P4","C4"],"historical_sources_report_directory":"audit-history-sources","historical_ranges_reference_only":true,"current_changes_not_covered_by_old60":true,"historical_sources_imported_or_executed_in_this_run":false,"historical_source_files_are_additional_mathematical_parents":false,"old_mathematical_suites_rerun":0},
  "new_source_audit": {"status":"STATIC_SOURCE_PINNED_RUNTIME_PENDING","upstream_completed_steps":64,"accepted_parent_batch_rows":128,"initial_rank":1578,"initial_generation":8283,"target_derivation_parents":225,"mathematical_parent_count":16,"executable_python_count":21,"raw_input_count":3,"batch_size":128,"max_batches":1,"refill":false,"producer_expected_rejections":[30,10,6],"checker_expected_rejections":[28,9,6],"new_selftests_executed_in_this_audit":false,"new_actual_arithmetic_executed_in_this_audit":false,"source_or_ast_executed_in_this_audit":false,"independent_workflow_audit_claimed":false},
  "current_transitions": [
    {
      "side": "P",
      "baseline_source_id": "P3",
      "current_source_id": "P4",
      "baseline_regions": [
        {"ordinal":0,"symbol":"MODULE_PREFIX","line_first":1,"line_last":75,"bytes":3646,"sha256":"6d43f5479b0e18f68b479b9e1dc32709b56629e79f587c903b1739b1ab4ab651"},
        {"ordinal":1,"symbol":"ResourceStop","line_first":76,"line_last":79,"bytes":45,"sha256":"2663eea930efd7508ae36f4a57ee62941488b3d7b44ac1c0e26fac114f8ab79e"},
        {"ordinal":2,"symbol":"require","line_first":80,"line_last":84,"bytes":134,"sha256":"80760f039039aad2789a03068aecc4b9992ea086984775a91de8e8ea368a6802"},
        {"ordinal":3,"symbol":"integer","line_first":85,"line_last":88,"bytes":184,"sha256":"e63a837212525f8b4e8e8957c14c7247ecfacf63db513ee21db461483452d8b8"},
        {"ordinal":4,"symbol":"trit","line_first":89,"line_last":92,"bytes":64,"sha256":"16d30509c0efe398d0cb95b7b10f82f8fbf83ffd47d44c098fdab9e97edbb223"},
        {"ordinal":5,"symbol":"signrep","line_first":93,"line_last":97,"bytes":108,"sha256":"7ec710a04080123c72e1b679b58b9a01b2830fb341f17a9658b1a20e81f6c392"},
        {"ordinal":6,"symbol":"canonical","line_first":98,"line_last":101,"bytes":167,"sha256":"db4677ec8bff3d9c88400f2adcc147356fc3e04ac4dc34b84e335b48c5dd8077"},
        {"ordinal":7,"symbol":"sha","line_first":102,"line_last":105,"bytes":73,"sha256":"d2c7cbbcf64af7faa72e068cf00a25c555a83bafb49c47bcbbe58d683eecac27"},
        {"ordinal":8,"symbol":"seal","line_first":106,"line_last":111,"bytes":272,"sha256":"135665a6af12bacefc2b83f450ceb41c8adf5b91478c03c81dbd79024d1ed633"},
        {"ordinal":9,"symbol":"check_seal","line_first":112,"line_last":118,"bytes":393,"sha256":"b44bc10939129e1ab7f9ecb7474f2980014e3c8aea18dd937f2ee37f80d9f669"},
        {"ordinal":10,"symbol":"exact_keys","line_first":119,"line_last":122,"bytes":143,"sha256":"21e67d0aedefd6f253ee7d9a3eb233662b4ace0de8e079e9577a4680685576cb"},
        {"ordinal":11,"symbol":"json_bytes","line_first":123,"line_last":128,"bytes":170,"sha256":"d2a2f1342c35663113456c09c6d30658a4112d5403187a811e296f547debd015"},
        {"ordinal":12,"symbol":"safe_name","line_first":129,"line_last":135,"bytes":313,"sha256":"d2aedb8a6633c14931c7b23c85b33606fbb08173659fb181a1986b1ddd796db4"},
        {"ordinal":13,"symbol":"safe_file","line_first":136,"line_last":146,"bytes":398,"sha256":"b0bef208fae9246053ad4c3399a9e5422b8465c882005432fce337999afdbee9"},
        {"ordinal":14,"symbol":"file_pin","line_first":147,"line_last":154,"bytes":410,"sha256":"30a0e4e1e706fd693b59fdae047f00684015e59767cd2ae5dbd53b2ccaa918d9"},
        {"ordinal":15,"symbol":"pin_type","line_first":155,"line_last":165,"bytes":623,"sha256":"6b92cd177b6e90fa75a878fb9dc766b5e93c3949cde1e8f748b8aa5c1c3e6181"},
        {"ordinal":16,"symbol":"read_json","line_first":166,"line_last":172,"bytes":205,"sha256":"11496f5c1b5b9f4d776268e93e1f1d7386ff37f956c95f4dc1810ab5f1501564"},
        {"ordinal":17,"symbol":"inventory","line_first":173,"line_last":187,"bytes":633,"sha256":"ff62d376e3f38a2670f388ed3b13880defed91ca32695addafa027b481e63916"},
        {"ordinal":18,"symbol":"check_deadline","line_first":188,"line_last":194,"bytes":182,"sha256":"769c7ba2a192ca53a253c14482747ba5877e60f25a2dd792d44ccf763e25b6f8"},
        {"ordinal":19,"symbol":"progress","line_first":195,"line_last":200,"bytes":176,"sha256":"acc8d4a3a843fdf95e485e2d51f90b4ae4d28839eeff46946f276c8867d8c14b"},
        {"ordinal":20,"symbol":"request_stop","line_first":201,"line_last":205,"bytes":107,"sha256":"f485a1770ca194490b974b83f65a2afc9396295dcbfa9b076d9f480fc664a152"},
        {"ordinal":21,"symbol":"sync_directory","line_first":206,"line_last":215,"bytes":213,"sha256":"9c83c7cc6f594420245775807c3b1fca91f02369a611511003aae6bb75c0087b"},
        {"ordinal":22,"symbol":"atomic_write","line_first":216,"line_last":231,"bytes":744,"sha256":"45873cc20ad288801a9163951fecebed266a63a9420802c3516b949c97c7986b"},
        {"ordinal":23,"symbol":"write_once","line_first":232,"line_last":239,"bytes":283,"sha256":"fab7807c5ff1376ecb3533f8a550412dbfcf949c2e69bd8e5b1a7ec6606efcff"},
        {"ordinal":24,"symbol":"own_dependencies","line_first":240,"line_last":257,"bytes":852,"sha256":"8fd5e86144534d1581960287e7fd62efc27749d875fc29ba4aa73dec45baffba"},
        {"ordinal":25,"symbol":"encode_array","line_first":258,"line_last":281,"bytes":1278,"sha256":"9ca5cb3025900ab69399730f5e176f0f8dfd48e4ea259087467c39305f991647"},
        {"ordinal":26,"symbol":"decode_array","line_first":282,"line_last":302,"bytes":1084,"sha256":"399a787ff018a3c71f02ac678d77ae8ed645c5d4d546479bda277a6e0c217bc9"},
        {"ordinal":27,"symbol":"process_measurement","line_first":303,"line_last":323,"bytes":773,"sha256":"43ee0607094422108218229b104d3b61608849394c730c5d7b24d6c4b1049fce"},
        {"ordinal":28,"symbol":"phase_telemetry","line_first":324,"line_last":332,"bytes":533,"sha256":"76b6006469c04a918753c2384925b912a28daf31a056dfc96de1b7b4f0b41dfe"},
        {"ordinal":29,"symbol":"validate_telemetry","line_first":333,"line_last":349,"bytes":1181,"sha256":"212846433d0ef07d768e3aaaf0a379626ffbdda212d33618e5fc0051f3c03b26"},
        {"ordinal":30,"symbol":"f3_array","line_first":350,"line_last":355,"bytes":269,"sha256":"6fc0276be283379f7eec48a50d6980c4ebb7aa8572f36034313f2f347eb47e9d"},
        {"ordinal":31,"symbol":"classify_batch","line_first":356,"line_last":413,"bytes":4192,"sha256":"e14f1ffce23568810497c62758449b1c5db4be69fd865370eb9d9335f523547e"},
        {"ordinal":32,"symbol":"current_batch_tree","line_first":414,"line_last":429,"bytes":1153,"sha256":"33625c87f0e64bae9552c8e15ba3e5fb7cb094fc963326c31501124cc3b34a6b"},
        {"ordinal":33,"symbol":"make_reduction_state","line_first":430,"line_last":444,"bytes":1158,"sha256":"cfa5160d814ded61164415bcf6cf1315adfb315394cbcf51e67b3f51489b60ca"},
        {"ordinal":34,"symbol":"reduce_candidate_numeric","line_first":445,"line_last":503,"bytes":4473,"sha256":"753470c3e040f48734c43a910962188eaa514446ac52dd6cfd7a2ea09549666a"},
        {"ordinal":35,"symbol":"advance_reduction_numeric","line_first":504,"line_last":537,"bytes":2535,"sha256":"24cfcc18c5546dcb326e0c3322450ca7437bca32e06c2a739f9cf514274be4fa"},
        {"ordinal":36,"symbol":"final_separator_numeric","line_first":538,"line_last":561,"bytes":1427,"sha256":"6c620072b6d5ad44c4aa8c385c191a9bed96fda2a026af5df49734b4d9589411"},
        {"ordinal":37,"symbol":"character_counts","line_first":562,"line_last":975,"bytes":15271,"sha256":"1eb0a1f09169fa5f71a7dd62873fdd1b85ef708b006c5412f53c9883f0b14b45"},
        {"ordinal":38,"symbol":"descriptor_list","line_first":976,"line_last":979,"bytes":151,"sha256":"da075cf37f380322819e090797f3187989416da592db2db833f51abfb017ed4d"},
        {"ordinal":39,"symbol":"validate_input_inventory","line_first":980,"line_last":990,"bytes":611,"sha256":"3747b6c6d79e2714bc8970f6ff3531c88480e6eb41a27cc159ea0be22f60b8c1"},
        {"ordinal":40,"symbol":"root_paths","line_first":991,"line_last":996,"bytes":294,"sha256":"9e3db7ca604440559c09464334e870d818712398c16232a44191fbd14629bca7"},
        {"ordinal":41,"symbol":"checked_descriptor","line_first":997,"line_last":1003,"bytes":310,"sha256":"e2acd494c9dadbd536ea16be45b8699cdfb37e97f51e36563b68c3232ba2c1d1"},
        {"ordinal":42,"symbol":"registered_policy","line_first":1004,"line_last":1010,"bytes":347,"sha256":"e452bed0ededa4ef34f8fdafe0478aa683585cb4044a95e3e4cff19f322c8f4e"},
        {"ordinal":43,"symbol":"authenticate_registration","line_first":1011,"line_last":1027,"bytes":1138,"sha256":"bd74cfa593503a07032d03759beff07d3292dbf71db9379b32ca110d50c20553"},
        {"ordinal":44,"symbol":"authenticate_code","line_first":1028,"line_last":1046,"bytes":1195,"sha256":"6f9bec704db261a944e52657dd3f92aaf6373e2761c039f3590d7472ca5f8aff"},
        {"ordinal":45,"symbol":"authenticate_anchor_metadata","line_first":1047,"line_last":1124,"bytes":6289,"sha256":"2d45494a3dbc6064b2ea08f39fba6e5288ba539e36eeeef893b427d0efca0b55"},
        {"ordinal":46,"symbol":"authenticate_acceptance","line_first":1125,"line_last":1167,"bytes":3000,"sha256":"4dda57734eda2f6fd86c68e1dafcbc3296497b4c531e0c3148ff40913d43e267"},
        {"ordinal":47,"symbol":"accepted_oracle_top_metadata","line_first":1168,"line_last":1192,"bytes":1920,"sha256":"47077c84812c4caf7cb782e12a43c4ee0e61126111e84fdf4b57e7339b96f610"},
        {"ordinal":48,"symbol":"parent_row_sources","line_first":1193,"line_last":1226,"bytes":2180,"sha256":"683367b46c3ffd5b586204e95562190fe42146a0542f8bacb3406125a616e4fa"},
        {"ordinal":49,"symbol":"thin_anchor","line_first":1227,"line_last":1295,"bytes":5144,"sha256":"2b2e5b425efdb999c47339888caad3c76313dcb83baaeefb9ff332b1f2aaf571"},
        {"ordinal":50,"symbol":"outer_metadata","line_first":1296,"line_last":1347,"bytes":4013,"sha256":"2bdf83f2e8cc63b7be176b22787e56d4ccacd7327d037304520b4f25c49d09a8"},
        {"ordinal":51,"symbol":"binding_from_metadata","line_first":1348,"line_last":1354,"bytes":407,"sha256":"2b85a6ec38c2fdb1e1acd2fc3f6300e46f590d6ff58743051b038e4514a91656"},
        {"ordinal":52,"symbol":"phase_roster","line_first":1355,"line_last":1380,"bytes":1730,"sha256":"de9749c25388cad93189eadc4ecab223f573db5edfed42f422ecb7427bebe74a"},
        {"ordinal":53,"symbol":"payload","line_first":1381,"line_last":1388,"bytes":346,"sha256":"b14f3da1a0a5fad3fb2d542e77e7a27c8077761e9c49a234a951be5bf0e1f3d3"},
        {"ordinal":54,"symbol":"serialize_arrays","line_first":1389,"line_last":1392,"bytes":128,"sha256":"09d8839ba5f9975100830a7432949c48319c264ca83b29cfda54bfc6f57d6151"},
        {"ordinal":55,"symbol":"payload_descriptor","line_first":1393,"line_last":1400,"bytes":297,"sha256":"41f499ed25421f16b147da49ddfb645ed6553b117de050473a8c71df49794551"},
        {"ordinal":56,"symbol":"atomic_diagnostic","line_first":1401,"line_last":1406,"bytes":259,"sha256":"b69bfad94ac6b65b0481d2068cfef2a833e41f64565a7f157df2d6d525c6953c"},
        {"ordinal":57,"symbol":"phase_manifest_body","line_first":1407,"line_last":1413,"bytes":415,"sha256":"7b2defb069001a281d981022f70b63d00ea779d662e932060acc6f2f20a7fef5"},
        {"ordinal":58,"symbol":"BatchPhaseStore","line_first":1414,"line_last":1521,"bytes":6460,"sha256":"9d41c05d760570919b6f845f651205909fe2a89be8785357b3b3426be3e77eda"},
        {"ordinal":59,"symbol":"tree_payloads","line_first":1522,"line_last":1544,"bytes":1791,"sha256":"25c5d65c9267fb6636f368ab7739b2d7e3018e8b4aa610a41322d7af6ab2cef3"},
        {"ordinal":60,"symbol":"saved_selection_values","line_first":1545,"line_last":1630,"bytes":7020,"sha256":"964ed49c83e494c170c80417d38194974d1722eec1e3a0c6b644f12e3b7493f6"},
        {"ordinal":61,"symbol":"publish_selection","line_first":1631,"line_last":1665,"bytes":2431,"sha256":"1575dd08155e35a1793e2de2c2aebf3aee5800c1f3235ac6c59f2a6a71a049f4"},
        {"ordinal":62,"symbol":"reduction_payloads","line_first":1666,"line_last":1716,"bytes":4212,"sha256":"e4751a2d613bc30100684315609f70acd7219bec66bcb7cf36d67a714f6cb338"},
        {"ordinal":63,"symbol":"restore_reduction","line_first":1717,"line_last":1773,"bytes":4169,"sha256":"887d29e4fff61523aa72d211023fc381cedf61397193bf710bd5ea7028a80ae1"},
        {"ordinal":64,"symbol":"publish_candidate_decision","line_first":1774,"line_last":1846,"bytes":5287,"sha256":"7579d2816d67431a64a7572be446d74c76e70002bd6af1e797e25ebdb0ec2b98"},
        {"ordinal":65,"symbol":"checkpoint_value","line_first":1847,"line_last":1866,"bytes":1757,"sha256":"1043b894a9bb02f6aabd5ebe4e8e75825a62ef70574a008b0a8c133c41d84fc5"},
        {"ordinal":66,"symbol":"private_head","line_first":1867,"line_last":1874,"bytes":509,"sha256":"3c0ad535c2a1db44c7f352101297530933723ea105d4f73fc36dbba7d6726c29"},
        {"ordinal":67,"symbol":"publish_private_checkpoint","line_first":1875,"line_last":1882,"bytes":303,"sha256":"8ab354b57eba7dc27f328bf461956daf031ee3b34aa28aac9558767f53737755"},
        {"ordinal":68,"symbol":"read_final","line_first":1883,"line_last":1943,"bytes":4246,"sha256":"6d076613b8add9573288dcb78803c46b815316e02f0e20cd6cf493e69112a26e"},
        {"ordinal":69,"symbol":"prepare_final","line_first":1944,"line_last":1971,"bytes":1688,"sha256":"0239a1406b5e5674ab6253f68100c0968300d08f2d1d84506cd4991659835168"},
        {"ordinal":70,"symbol":"inventory_documents","line_first":1972,"line_last":1976,"bytes":215,"sha256":"0b9f5ff6c3ae76f33242728f81489c8b5a7970aa23021fc8da74302812bb8182"},
        {"ordinal":71,"symbol":"authenticate_input_documents","line_first":1977,"line_last":1989,"bytes":597,"sha256":"b2c944484ae67c593ce4b0d71ff2b857bcf169e2b36acb790e35bb959ca00ea8"},
        {"ordinal":72,"symbol":"finish_inputs","line_first":1990,"line_last":2003,"bytes":861,"sha256":"1b1afb43fc5d485332d9a91ce306beb4fb8700cf7bb9a87869ffc7875d232af2"},
        {"ordinal":73,"symbol":"input_preservation","line_first":2004,"line_last":2024,"bytes":1452,"sha256":"6c62e7897781b578a51591362c7a7b37af03f6430980f9efaba1146629ec5978"},
        {"ordinal":74,"symbol":"validate_launch","line_first":2025,"line_last":2031,"bytes":403,"sha256":"f8b4dc6d1867422cffed0294e4ce0184b6e8b710a327af2bfb62cde7c6262c31"},
        {"ordinal":75,"symbol":"validate_host_paths","line_first":2032,"line_last":2038,"bytes":390,"sha256":"c3c1739a59b9f0a8e58fb683e6b0210d12f9a0aef162e483d3e0c5191c6da8f0"},
        {"ordinal":76,"symbol":"validate_invocation_history","line_first":2039,"line_last":2060,"bytes":1344,"sha256":"f5ab9ba4ed9d7ef761a850d2ae3e459111e6ba1c6b88fdf7270363d5027110b4"},
        {"ordinal":77,"symbol":"invocation_files","line_first":2061,"line_last":2122,"bytes":4227,"sha256":"0140c75f68d94658bbf08f0e79aadb350025b092816f0d1f656ef686820b121f"},
        {"ordinal":78,"symbol":"begin_invocation","line_first":2123,"line_last":2152,"bytes":2001,"sha256":"4dbbb5940c51bf978dacc5c5b9523fdd2d06303e45dc7ef7f220344c1988f5f4"},
        {"ordinal":79,"symbol":"candidate_view","line_first":2153,"line_last":2164,"bytes":872,"sha256":"8cd21ccdd7ae331827d83b67343f78b89ea1d0f19dc919b8793a050e9d65b5e8"},
        {"ordinal":80,"symbol":"legacy_e_input","line_first":2165,"line_last":2177,"bytes":1033,"sha256":"b10239987c49d6f029032b7d9442d32799b61d1ff9903707882e317266beee5d"},
        {"ordinal":81,"symbol":"run_candidate_phases","line_first":2178,"line_last":2237,"bytes":3952,"sha256":"de94fec175fec385c0990e94849964a50d4471367467642d33acbf4ff371f9a8"},
        {"ordinal":82,"symbol":"current_derived_rho2","line_first":2238,"line_last":2253,"bytes":1206,"sha256":"387ab5b6aff6369ec45f2483a2687b4c477038b905543999926bc12e333dd890"},
        {"ordinal":83,"symbol":"phase_telemetry_descriptor","line_first":2254,"line_last":2258,"bytes":228,"sha256":"844d45a46ea3ef153d5674b6157a60fd8177fde56d1c74e771c5dc9cd6c769ad"},
        {"ordinal":84,"symbol":"selection_readout","line_first":2259,"line_last":2281,"bytes":1622,"sha256":"d295fedb72d685fc247328850028b5026324a8993686a38eefa7aae66a5441a2"},
        {"ordinal":85,"symbol":"candidate_readout","line_first":2282,"line_last":2311,"bytes":2533,"sha256":"e9cdcff8fa97a92ff85ab7ee58192e5b511b2a5457929d7f5ce45580f5a94a28"},
        {"ordinal":86,"symbol":"final_payloads","line_first":2312,"line_last":2341,"bytes":2300,"sha256":"0e411c72683ce7fb4358c2302e20617a9ab4b5cfa6b96f34ac0c35140f7ce28d"},
        {"ordinal":87,"symbol":"final_manifest_value","line_first":2342,"line_last":2356,"bytes":1138,"sha256":"76b2af888eeefd726180ee25ad1f2bc37f1fefc459bd666bbd2fdf4b609952d3"},
        {"ordinal":88,"symbol":"public_head_value","line_first":2357,"line_last":2366,"bytes":650,"sha256":"b1b4fefcf5712b02991832af65bb31bd9622fcf544ecb3621b72c9b4282c1b41"},
        {"ordinal":89,"symbol":"same_json","line_first":2367,"line_last":2371,"bytes":210,"sha256":"595c85a6561119a5658390e769f3802ae9d654fd0a42bd9d559472d93da06825"},
        {"ordinal":90,"symbol":"phase_prefix","line_first":2372,"line_last":2377,"bytes":190,"sha256":"a8ce741ed077a98b35a882d3230aab8ce603f827ab39ff18f0d52bfa4dda316e"},
        {"ordinal":91,"symbol":"sequence_scope","line_first":2378,"line_last":2384,"bytes":336,"sha256":"44354f444ee46c3ef368f3c1b8bd76666a4d2d374125bb39336972f718054ad9"},
        {"ordinal":92,"symbol":"diagnostic_subtree","line_first":2385,"line_last":2394,"bytes":486,"sha256":"c3fe447764bb09e960278ef9bcda9c823abeeaf62894ef8d60c4292c0d916aa0"},
        {"ordinal":93,"symbol":"pending_directory","line_first":2395,"line_last":2416,"bytes":1043,"sha256":"892102472250354620e09d2c01ae8bd259d787cd45b4685985a46f1466abbd6b"},
        {"ordinal":94,"symbol":"authenticate_output_roster","line_first":2417,"line_last":2461,"bytes":2528,"sha256":"557ea4d9a04cd5c951189d06c19a6a9505a8271b3f6332b1af7d2be0c696d927"},
        {"ordinal":95,"symbol":"phase_files","line_first":2462,"line_last":2470,"bytes":353,"sha256":"662f9eef848530ad677b55cd29239370055eb933897834b7b125fdfafccc1e55"},
        {"ordinal":96,"symbol":"read_only_documents","line_first":2471,"line_last":2479,"bytes":390,"sha256":"2fe5a6084ffc461c69fdeba34130d813d9236631b6f71b765660882ab85b7e15"},
        {"ordinal":97,"symbol":"restoration_store","line_first":2480,"line_last":2486,"bytes":407,"sha256":"61cb32f9ef66cf3b49a6f5a6cb5561498f93b2e0e9f39d7d3cb0c80702d04e68"},
        {"ordinal":98,"symbol":"load_private_prefix","line_first":2487,"line_last":2584,"bytes":6509,"sha256":"42d05098144fa23aa8a57d9b6d4ed51156a67ceef1d10236570125d3d79da601"},
        {"ordinal":99,"symbol":"recover_private_metadata","line_first":2585,"line_last":2608,"bytes":1347,"sha256":"2f8994ca208aa585646f6b3236ccdb51cec1d37b99ddbf679b25cab29bfc9edc"},
        {"ordinal":100,"symbol":"completion_log","line_first":2609,"line_last":2614,"bytes":241,"sha256":"f0b0fc0b1ef997ce340da9fdb5914376d29173c802b0cd9db1d2cc08160a3f1e"},
        {"ordinal":101,"symbol":"result_value","line_first":2615,"line_last":2648,"bytes":2723,"sha256":"b926b25b8f52b53d4367a7ff15daf1aabe69f813b808f142649b443df0ea048d"},
        {"ordinal":102,"symbol":"authenticate_completed_result","line_first":2649,"line_last":2663,"bytes":927,"sha256":"bdf2b2df52b3aff38e99a4f5041f9df4e173122317d7f9fa453e2008b01e8f9c"},
        {"ordinal":103,"symbol":"append_checkpoint","line_first":2664,"line_last":2674,"bytes":732,"sha256":"76b60325ada7d315607d7889c849e1222c1efec5b6b49d2b8c5d94d3ec9d4dc6"},
        {"ordinal":104,"symbol":"run_selection","line_first":2675,"line_last":2705,"bytes":1775,"sha256":"180a431f3ddc9d1fbde1f12d162c3304497ec1f86955e28215106231458d5edb"},
        {"ordinal":105,"symbol":"run_candidates","line_first":2706,"line_last":2751,"bytes":2999,"sha256":"f98cdd69c1cc8d1e03c80fa6d782a40d09cf5fd3c9f33158e71a4aac28c02527"},
        {"ordinal":106,"symbol":"admit_diagnostics","line_first":2752,"line_last":2807,"bytes":4168,"sha256":"84d79aab78fd26b49e49c6bdc4dd005897630466b100359a1244233242ca92f9"},
        {"ordinal":107,"symbol":"output_path_gate","line_first":2808,"line_last":2822,"bytes":904,"sha256":"0d2fd36442b7dcac8ac284b05abbdc18ef3c41dceca8e81774a7a6380a6f7d2b"},
        {"ordinal":108,"symbol":"run_actual","line_first":2823,"line_last":2891,"bytes":4311,"sha256":"a1a5486f4f754c531844952085b57ff38b8a08f5d6606730477bcf350fd887b4"},
        {"ordinal":109,"symbol":"canary_reject","line_first":2892,"line_last":2900,"bytes":235,"sha256":"0c43737110b1fec08b4ec3b7a92191b12cd24471ca0065939178fb16ca92ccc4"},
        {"ordinal":110,"symbol":"canary_binding","line_first":2901,"line_last":2905,"bytes":215,"sha256":"6d23702c33c5772eadff05cbc09734a6e01b5860271f86eba25b2aa017c0577d"},
        {"ordinal":111,"symbol":"canary_selection_fixture","line_first":2906,"line_last":2943,"bytes":2544,"sha256":"5da935c6bba12d1b2d638cb995195f0c2d8ee5a01a8288e5540a9be47f7001e9"},
        {"ordinal":112,"symbol":"selftest_root_path","line_first":2944,"line_last":2966,"bytes":1149,"sha256":"9a1907f7845b1fcb44ecfa9cea4a91bb143a609e155865aca1dd2b8ff14c7e0f"},
        {"ordinal":113,"symbol":"k128_reject","line_first":2967,"line_last":2979,"bytes":590,"sha256":"a5db86c15ec181cc19fd6821621950bec1a438b627fdb4651136f9bc9b055036"},
        {"ordinal":114,"symbol":"k128_registration_canary","line_first":2980,"line_last":3140,"bytes":10576,"sha256":"a1f28e4c4bdeb144500d37ac2a4b6570249bbd7aaf889fd2f4140be25cf564bd"},
        {"ordinal":115,"symbol":"k128_tree_commit","line_first":3141,"line_last":3153,"bytes":741,"sha256":"9152dc0feb393e39e28ef877a358726cdb0c4789aaecdb935baa71e20151e4fc"},
        {"ordinal":116,"symbol":"k128_tree_reload","line_first":3154,"line_last":3176,"bytes":1493,"sha256":"ecf4b6938e5bfd428a904036d15c8b55bd17c192b08bbaf5c119c2bdc99f18df"},
        {"ordinal":117,"symbol":"k128_selection_canary","line_first":3177,"line_last":3298,"bytes":8363,"sha256":"d4fd8fa4a78ef66074f97708401725de8e349b34438de73b8b1069f55f6828f3"},
        {"ordinal":118,"symbol":"selftest","line_first":3299,"line_last":3324,"bytes":1676,"sha256":"51c6da21e2960b3ce42df8121cd1c2e8e0b921a87689d7857c94af22baaac0b9"},
        {"ordinal":119,"symbol":"diagnostic","line_first":3325,"line_last":3376,"bytes":3845,"sha256":"788572a74a9bac2226845a721be981a735813a44945a02a3875ac13f8aa036de"},
        {"ordinal":120,"symbol":"cli","line_first":3377,"line_last":3404,"bytes":1732,"sha256":"c61999d4c0c5d3146909e295af6e5f8024654713dc922c6d8f219ccf9417dfab"},
        {"ordinal":121,"symbol":"main","line_first":3405,"line_last":3434,"bytes":1252,"sha256":"1abfd61eb035bd3b9026a3730baa722f6433c196db469f4b75be7fe6093f419e"}
      ],
      "current_regions": [
        {"ordinal":0,"symbol":"MODULE_PREFIX","line_first":1,"line_last":246,"bytes":13261,"sha256":"5be6598c9473baaedda98d842200783c134ddb15a6792f4cb55918d02adc0bda"},
        {"ordinal":1,"symbol":"ResourceStop","line_first":247,"line_last":250,"bytes":45,"sha256":"2663eea930efd7508ae36f4a57ee62941488b3d7b44ac1c0e26fac114f8ab79e"},
        {"ordinal":2,"symbol":"require","line_first":251,"line_last":255,"bytes":134,"sha256":"80760f039039aad2789a03068aecc4b9992ea086984775a91de8e8ea368a6802"},
        {"ordinal":3,"symbol":"integer","line_first":256,"line_last":259,"bytes":184,"sha256":"e63a837212525f8b4e8e8957c14c7247ecfacf63db513ee21db461483452d8b8"},
        {"ordinal":4,"symbol":"trit","line_first":260,"line_last":263,"bytes":64,"sha256":"16d30509c0efe398d0cb95b7b10f82f8fbf83ffd47d44c098fdab9e97edbb223"},
        {"ordinal":5,"symbol":"signrep","line_first":264,"line_last":268,"bytes":108,"sha256":"7ec710a04080123c72e1b679b58b9a01b2830fb341f17a9658b1a20e81f6c392"},
        {"ordinal":6,"symbol":"canonical","line_first":269,"line_last":272,"bytes":167,"sha256":"db4677ec8bff3d9c88400f2adcc147356fc3e04ac4dc34b84e335b48c5dd8077"},
        {"ordinal":7,"symbol":"sha","line_first":273,"line_last":276,"bytes":73,"sha256":"d2c7cbbcf64af7faa72e068cf00a25c555a83bafb49c47bcbbe58d683eecac27"},
        {"ordinal":8,"symbol":"seal","line_first":277,"line_last":282,"bytes":272,"sha256":"135665a6af12bacefc2b83f450ceb41c8adf5b91478c03c81dbd79024d1ed633"},
        {"ordinal":9,"symbol":"check_seal","line_first":283,"line_last":289,"bytes":393,"sha256":"b44bc10939129e1ab7f9ecb7474f2980014e3c8aea18dd937f2ee37f80d9f669"},
        {"ordinal":10,"symbol":"exact_keys","line_first":290,"line_last":293,"bytes":143,"sha256":"21e67d0aedefd6f253ee7d9a3eb233662b4ace0de8e079e9577a4680685576cb"},
        {"ordinal":11,"symbol":"json_bytes","line_first":294,"line_last":299,"bytes":170,"sha256":"d2a2f1342c35663113456c09c6d30658a4112d5403187a811e296f547debd015"},
        {"ordinal":12,"symbol":"safe_name","line_first":300,"line_last":306,"bytes":313,"sha256":"d2aedb8a6633c14931c7b23c85b33606fbb08173659fb181a1986b1ddd796db4"},
        {"ordinal":13,"symbol":"safe_file","line_first":307,"line_last":317,"bytes":398,"sha256":"b0bef208fae9246053ad4c3399a9e5422b8465c882005432fce337999afdbee9"},
        {"ordinal":14,"symbol":"file_pin","line_first":318,"line_last":325,"bytes":410,"sha256":"30a0e4e1e706fd693b59fdae047f00684015e59767cd2ae5dbd53b2ccaa918d9"},
        {"ordinal":15,"symbol":"pin_type","line_first":326,"line_last":336,"bytes":623,"sha256":"6b92cd177b6e90fa75a878fb9dc766b5e93c3949cde1e8f748b8aa5c1c3e6181"},
        {"ordinal":16,"symbol":"read_json","line_first":337,"line_last":343,"bytes":205,"sha256":"11496f5c1b5b9f4d776268e93e1f1d7386ff37f956c95f4dc1810ab5f1501564"},
        {"ordinal":17,"symbol":"inventory","line_first":344,"line_last":358,"bytes":633,"sha256":"ff62d376e3f38a2670f388ed3b13880defed91ca32695addafa027b481e63916"},
        {"ordinal":18,"symbol":"check_deadline","line_first":359,"line_last":365,"bytes":182,"sha256":"769c7ba2a192ca53a253c14482747ba5877e60f25a2dd792d44ccf763e25b6f8"},
        {"ordinal":19,"symbol":"progress","line_first":366,"line_last":371,"bytes":176,"sha256":"acc8d4a3a843fdf95e485e2d51f90b4ae4d28839eeff46946f276c8867d8c14b"},
        {"ordinal":20,"symbol":"request_stop","line_first":372,"line_last":376,"bytes":107,"sha256":"f485a1770ca194490b974b83f65a2afc9396295dcbfa9b076d9f480fc664a152"},
        {"ordinal":21,"symbol":"sync_directory","line_first":377,"line_last":386,"bytes":213,"sha256":"9c83c7cc6f594420245775807c3b1fca91f02369a611511003aae6bb75c0087b"},
        {"ordinal":22,"symbol":"atomic_write","line_first":387,"line_last":402,"bytes":744,"sha256":"45873cc20ad288801a9163951fecebed266a63a9420802c3516b949c97c7986b"},
        {"ordinal":23,"symbol":"write_once","line_first":403,"line_last":410,"bytes":283,"sha256":"fab7807c5ff1376ecb3533f8a550412dbfcf949c2e69bd8e5b1a7ec6606efcff"},
        {"ordinal":24,"symbol":"own_dependencies","line_first":411,"line_last":428,"bytes":852,"sha256":"8fd5e86144534d1581960287e7fd62efc27749d875fc29ba4aa73dec45baffba"},
        {"ordinal":25,"symbol":"encode_array","line_first":429,"line_last":452,"bytes":1278,"sha256":"9ca5cb3025900ab69399730f5e176f0f8dfd48e4ea259087467c39305f991647"},
        {"ordinal":26,"symbol":"decode_array","line_first":453,"line_last":473,"bytes":1084,"sha256":"399a787ff018a3c71f02ac678d77ae8ed645c5d4d546479bda277a6e0c217bc9"},
        {"ordinal":27,"symbol":"process_measurement","line_first":474,"line_last":494,"bytes":773,"sha256":"43ee0607094422108218229b104d3b61608849394c730c5d7b24d6c4b1049fce"},
        {"ordinal":28,"symbol":"phase_telemetry","line_first":495,"line_last":503,"bytes":533,"sha256":"76b6006469c04a918753c2384925b912a28daf31a056dfc96de1b7b4f0b41dfe"},
        {"ordinal":29,"symbol":"validate_telemetry","line_first":504,"line_last":520,"bytes":1181,"sha256":"212846433d0ef07d768e3aaaf0a379626ffbdda212d33618e5fc0051f3c03b26"},
        {"ordinal":30,"symbol":"f3_array","line_first":521,"line_last":526,"bytes":269,"sha256":"6fc0276be283379f7eec48a50d6980c4ebb7aa8572f36034313f2f347eb47e9d"},
        {"ordinal":31,"symbol":"classify_batch","line_first":527,"line_last":584,"bytes":4192,"sha256":"e14f1ffce23568810497c62758449b1c5db4be69fd865370eb9d9335f523547e"},
        {"ordinal":32,"symbol":"current_batch_tree","line_first":585,"line_last":600,"bytes":1153,"sha256":"33625c87f0e64bae9552c8e15ba3e5fb7cb094fc963326c31501124cc3b34a6b"},
        {"ordinal":33,"symbol":"make_reduction_state","line_first":601,"line_last":615,"bytes":1158,"sha256":"cfa5160d814ded61164415bcf6cf1315adfb315394cbcf51e67b3f51489b60ca"},
        {"ordinal":34,"symbol":"reduce_candidate_numeric","line_first":616,"line_last":674,"bytes":4473,"sha256":"753470c3e040f48734c43a910962188eaa514446ac52dd6cfd7a2ea09549666a"},
        {"ordinal":35,"symbol":"advance_reduction_numeric","line_first":675,"line_last":708,"bytes":2535,"sha256":"24cfcc18c5546dcb326e0c3322450ca7437bca32e06c2a739f9cf514274be4fa"},
        {"ordinal":36,"symbol":"final_separator_numeric","line_first":709,"line_last":732,"bytes":1427,"sha256":"6c620072b6d5ad44c4aa8c385c191a9bed96fda2a026af5df49734b4d9589411"},
        {"ordinal":37,"symbol":"character_counts","line_first":733,"line_last":1148,"bytes":15333,"sha256":"687975c2a7349d28c04ed862b228f2b99a8ecd86a5a78506f37fbf66570eae6e"},
        {"ordinal":38,"symbol":"descriptor_list","line_first":1149,"line_last":1152,"bytes":151,"sha256":"da075cf37f380322819e090797f3187989416da592db2db833f51abfb017ed4d"},
        {"ordinal":39,"symbol":"validate_input_inventory","line_first":1153,"line_last":1163,"bytes":611,"sha256":"3747b6c6d79e2714bc8970f6ff3531c88480e6eb41a27cc159ea0be22f60b8c1"},
        {"ordinal":40,"symbol":"root_paths","line_first":1164,"line_last":1169,"bytes":294,"sha256":"9e3db7ca604440559c09464334e870d818712398c16232a44191fbd14629bca7"},
        {"ordinal":41,"symbol":"checked_descriptor","line_first":1170,"line_last":1176,"bytes":310,"sha256":"e2acd494c9dadbd536ea16be45b8699cdfb37e97f51e36563b68c3232ba2c1d1"},
        {"ordinal":42,"symbol":"registered_policy","line_first":1177,"line_last":1183,"bytes":347,"sha256":"e452bed0ededa4ef34f8fdafe0478aa683585cb4044a95e3e4cff19f322c8f4e"},
        {"ordinal":43,"symbol":"authenticate_registration","line_first":1184,"line_last":1200,"bytes":1138,"sha256":"bd74cfa593503a07032d03759beff07d3292dbf71db9379b32ca110d50c20553"},
        {"ordinal":44,"symbol":"authenticate_code","line_first":1201,"line_last":1219,"bytes":1195,"sha256":"6f9bec704db261a944e52657dd3f92aaf6373e2761c039f3590d7472ca5f8aff"},
        {"ordinal":45,"symbol":"authenticate_anchor_metadata","line_first":1220,"line_last":1297,"bytes":6289,"sha256":"2d45494a3dbc6064b2ea08f39fba6e5288ba539e36eeeef893b427d0efca0b55"},
        {"ordinal":46,"symbol":"batch_anchor_header","line_first":1298,"line_last":1326,"bytes":1892,"sha256":"525502f3203b07fe6f81f2fabdd193a569a900e6cac6e622383180980757c519"},
        {"ordinal":47,"symbol":"batch_old_input_projection","line_first":1327,"line_last":1335,"bytes":441,"sha256":"abd5ea691258763f41e2e16ab58d666f9c2af0db3f9aa15ab31b34ab20c171c5"},
        {"ordinal":48,"symbol":"batch_plain_target_binding","line_first":1336,"line_last":1345,"bytes":761,"sha256":"31c6e7a3713fded143b90fc7f4ae628c8450d08731dbb06d9219cde47a7f4ab1"},
        {"ordinal":49,"symbol":"old_batch_document","line_first":1346,"line_last":1352,"bytes":231,"sha256":"d12c54342deaf1750bf0a10f1e1adc48d667d1d4f8134125b74fe0fdb2a34df0"},
        {"ordinal":50,"symbol":"batch_binding_matches","line_first":1353,"line_last":1357,"bytes":254,"sha256":"46b1c7e4c2e30959907d9cb1226d8cdc1223bc9efed0ef14990f19456f50a338"},
        {"ordinal":51,"symbol":"batch_saved_manifest","line_first":1358,"line_last":1389,"bytes":1740,"sha256":"57b73fcccf188da560e3857559b8199b14bc0f6b367e48bc439593e3576de95e"},
        {"ordinal":52,"symbol":"batch_loader_regions","line_first":1390,"line_last":1413,"bytes":1381,"sha256":"ad2429a9ea2d44caea029457b0faf2d42fc5fe2dd0520b895a504970abe4c6a6"},
        {"ordinal":53,"symbol":"batch_saved_rows","line_first":1414,"line_last":1539,"bytes":11047,"sha256":"3063c442bd63be5415b18911b21cdf8437babd851097d1d08bd773d9fb55ce77"},
        {"ordinal":54,"symbol":"batch_saved_checkpoints","line_first":1540,"line_last":1599,"bytes":4626,"sha256":"1f6629ad4f916a3fe55eea6aa1a4440ceff44520775c7baabc2145539e822f17"},
        {"ordinal":55,"symbol":"authenticate_batch_parent","line_first":1600,"line_last":1758,"bytes":14090,"sha256":"a172fb776add8f9c05029c4cb907fc27797bf5afe4c086808f84c3c6d3c509ad"},
        {"ordinal":56,"symbol":"authenticate_acceptance","line_first":1759,"line_last":1803,"bytes":3114,"sha256":"47156ad03b336e993b75788b4fd814281c6c7ad56a25b32575d67404f1829d75"},
        {"ordinal":57,"symbol":"accepted_oracle_top_metadata","line_first":1804,"line_last":1828,"bytes":1920,"sha256":"47077c84812c4caf7cb782e12a43c4ee0e61126111e84fdf4b57e7339b96f610"},
        {"ordinal":58,"symbol":"parent_row_sources","line_first":1829,"line_last":1862,"bytes":2180,"sha256":"683367b46c3ffd5b586204e95562190fe42146a0542f8bacb3406125a616e4fa"},
        {"ordinal":59,"symbol":"thin_anchor","line_first":1863,"line_last":1931,"bytes":5144,"sha256":"2b2e5b425efdb999c47339888caad3c76313dcb83baaeefb9ff332b1f2aaf571"},
        {"ordinal":60,"symbol":"promote_batch_anchor","line_first":1932,"line_last":1995,"bytes":5389,"sha256":"6287349d222161fa93d22a4008a904e02324ea776dac76e2e8303cc682f73ed3"},
        {"ordinal":61,"symbol":"outer_metadata","line_first":1996,"line_last":2054,"bytes":4631,"sha256":"d55626d60753b595d41c7dccbb37fb8b0c7094e89343fb5734a7838c77eb876b"},
        {"ordinal":62,"symbol":"binding_from_metadata","line_first":2055,"line_last":2061,"bytes":407,"sha256":"2b85a6ec38c2fdb1e1acd2fc3f6300e46f590d6ff58743051b038e4514a91656"},
        {"ordinal":63,"symbol":"phase_roster","line_first":2062,"line_last":2087,"bytes":1730,"sha256":"de9749c25388cad93189eadc4ecab223f573db5edfed42f422ecb7427bebe74a"},
        {"ordinal":64,"symbol":"payload","line_first":2088,"line_last":2095,"bytes":346,"sha256":"b14f3da1a0a5fad3fb2d542e77e7a27c8077761e9c49a234a951be5bf0e1f3d3"},
        {"ordinal":65,"symbol":"serialize_arrays","line_first":2096,"line_last":2099,"bytes":128,"sha256":"09d8839ba5f9975100830a7432949c48319c264ca83b29cfda54bfc6f57d6151"},
        {"ordinal":66,"symbol":"payload_descriptor","line_first":2100,"line_last":2107,"bytes":297,"sha256":"41f499ed25421f16b147da49ddfb645ed6553b117de050473a8c71df49794551"},
        {"ordinal":67,"symbol":"atomic_diagnostic","line_first":2108,"line_last":2113,"bytes":259,"sha256":"b69bfad94ac6b65b0481d2068cfef2a833e41f64565a7f157df2d6d525c6953c"},
        {"ordinal":68,"symbol":"phase_manifest_body","line_first":2114,"line_last":2120,"bytes":415,"sha256":"7b2defb069001a281d981022f70b63d00ea779d662e932060acc6f2f20a7fef5"},
        {"ordinal":69,"symbol":"BatchPhaseStore","line_first":2121,"line_last":2228,"bytes":6460,"sha256":"9d41c05d760570919b6f845f651205909fe2a89be8785357b3b3426be3e77eda"},
        {"ordinal":70,"symbol":"tree_payloads","line_first":2229,"line_last":2251,"bytes":1791,"sha256":"25c5d65c9267fb6636f368ab7739b2d7e3018e8b4aa610a41322d7af6ab2cef3"},
        {"ordinal":71,"symbol":"saved_selection_values","line_first":2252,"line_last":2337,"bytes":7020,"sha256":"964ed49c83e494c170c80417d38194974d1722eec1e3a0c6b644f12e3b7493f6"},
        {"ordinal":72,"symbol":"publish_selection","line_first":2338,"line_last":2372,"bytes":2431,"sha256":"1575dd08155e35a1793e2de2c2aebf3aee5800c1f3235ac6c59f2a6a71a049f4"},
        {"ordinal":73,"symbol":"reduction_payloads","line_first":2373,"line_last":2423,"bytes":4212,"sha256":"e4751a2d613bc30100684315609f70acd7219bec66bcb7cf36d67a714f6cb338"},
        {"ordinal":74,"symbol":"restore_reduction","line_first":2424,"line_last":2480,"bytes":4169,"sha256":"887d29e4fff61523aa72d211023fc381cedf61397193bf710bd5ea7028a80ae1"},
        {"ordinal":75,"symbol":"publish_candidate_decision","line_first":2481,"line_last":2553,"bytes":5287,"sha256":"7579d2816d67431a64a7572be446d74c76e70002bd6af1e797e25ebdb0ec2b98"},
        {"ordinal":76,"symbol":"checkpoint_value","line_first":2554,"line_last":2573,"bytes":1757,"sha256":"1043b894a9bb02f6aabd5ebe4e8e75825a62ef70574a008b0a8c133c41d84fc5"},
        {"ordinal":77,"symbol":"private_head","line_first":2574,"line_last":2581,"bytes":509,"sha256":"3c0ad535c2a1db44c7f352101297530933723ea105d4f73fc36dbba7d6726c29"},
        {"ordinal":78,"symbol":"publish_private_checkpoint","line_first":2582,"line_last":2589,"bytes":303,"sha256":"8ab354b57eba7dc27f328bf461956daf031ee3b34aa28aac9558767f53737755"},
        {"ordinal":79,"symbol":"read_final","line_first":2590,"line_last":2650,"bytes":4246,"sha256":"6d076613b8add9573288dcb78803c46b815316e02f0e20cd6cf493e69112a26e"},
        {"ordinal":80,"symbol":"prepare_final","line_first":2651,"line_last":2678,"bytes":1688,"sha256":"0239a1406b5e5674ab6253f68100c0968300d08f2d1d84506cd4991659835168"},
        {"ordinal":81,"symbol":"inventory_documents","line_first":2679,"line_last":2683,"bytes":215,"sha256":"0b9f5ff6c3ae76f33242728f81489c8b5a7970aa23021fc8da74302812bb8182"},
        {"ordinal":82,"symbol":"authenticate_input_documents","line_first":2684,"line_last":2696,"bytes":597,"sha256":"b2c944484ae67c593ce4b0d71ff2b857bcf169e2b36acb790e35bb959ca00ea8"},
        {"ordinal":83,"symbol":"finish_inputs","line_first":2697,"line_last":2710,"bytes":861,"sha256":"0bd98bb84d202a800820280eff3862e932342a75662547703dcf0349d9fad2a6"},
        {"ordinal":84,"symbol":"input_preservation","line_first":2711,"line_last":2731,"bytes":1452,"sha256":"15a8a7afe34143cb6c6daaa4982a40cd7872f90c2bd806855f373302d09d56f4"},
        {"ordinal":85,"symbol":"validate_launch","line_first":2732,"line_last":2738,"bytes":403,"sha256":"f8b4dc6d1867422cffed0294e4ce0184b6e8b710a327af2bfb62cde7c6262c31"},
        {"ordinal":86,"symbol":"validate_host_paths","line_first":2739,"line_last":2745,"bytes":390,"sha256":"af939b9562ef86f1b23fb2e187c1d330d08925b87fcde7fafbb05ef1e566e696"},
        {"ordinal":87,"symbol":"validate_invocation_history","line_first":2746,"line_last":2767,"bytes":1344,"sha256":"f5ab9ba4ed9d7ef761a850d2ae3e459111e6ba1c6b88fdf7270363d5027110b4"},
        {"ordinal":88,"symbol":"invocation_files","line_first":2768,"line_last":2829,"bytes":4227,"sha256":"0140c75f68d94658bbf08f0e79aadb350025b092816f0d1f656ef686820b121f"},
        {"ordinal":89,"symbol":"begin_invocation","line_first":2830,"line_last":2859,"bytes":2001,"sha256":"4dbbb5940c51bf978dacc5c5b9523fdd2d06303e45dc7ef7f220344c1988f5f4"},
        {"ordinal":90,"symbol":"candidate_view","line_first":2860,"line_last":2871,"bytes":872,"sha256":"8cd21ccdd7ae331827d83b67343f78b89ea1d0f19dc919b8793a050e9d65b5e8"},
        {"ordinal":91,"symbol":"legacy_e_input","line_first":2872,"line_last":2884,"bytes":1033,"sha256":"b10239987c49d6f029032b7d9442d32799b61d1ff9903707882e317266beee5d"},
        {"ordinal":92,"symbol":"run_candidate_phases","line_first":2885,"line_last":2944,"bytes":3952,"sha256":"de94fec175fec385c0990e94849964a50d4471367467642d33acbf4ff371f9a8"},
        {"ordinal":93,"symbol":"current_derived_rho2","line_first":2945,"line_last":2963,"bytes":1422,"sha256":"8894fc476eeed997c0fb397ba4eadd467b5b73709bd63e4dbcc2f6630f815fc6"},
        {"ordinal":94,"symbol":"phase_telemetry_descriptor","line_first":2964,"line_last":2968,"bytes":228,"sha256":"844d45a46ea3ef153d5674b6157a60fd8177fde56d1c74e771c5dc9cd6c769ad"},
        {"ordinal":95,"symbol":"selection_readout","line_first":2969,"line_last":2991,"bytes":1622,"sha256":"d295fedb72d685fc247328850028b5026324a8993686a38eefa7aae66a5441a2"},
        {"ordinal":96,"symbol":"candidate_readout","line_first":2992,"line_last":3021,"bytes":2533,"sha256":"e9cdcff8fa97a92ff85ab7ee58192e5b511b2a5457929d7f5ce45580f5a94a28"},
        {"ordinal":97,"symbol":"final_payloads","line_first":3022,"line_last":3051,"bytes":2300,"sha256":"0e411c72683ce7fb4358c2302e20617a9ab4b5cfa6b96f34ac0c35140f7ce28d"},
        {"ordinal":98,"symbol":"final_manifest_value","line_first":3052,"line_last":3066,"bytes":1180,"sha256":"c35a7bce8e8159b1b8b6d19302c6d3bac2d88f6858b06fbeffe1218fe7c81ca0"},
        {"ordinal":99,"symbol":"public_head_value","line_first":3067,"line_last":3076,"bytes":687,"sha256":"05352fad3378b11dd4bac992318b945509fea19467ea918dc3e1b2cad506fba6"},
        {"ordinal":100,"symbol":"same_json","line_first":3077,"line_last":3081,"bytes":210,"sha256":"595c85a6561119a5658390e769f3802ae9d654fd0a42bd9d559472d93da06825"},
        {"ordinal":101,"symbol":"phase_prefix","line_first":3082,"line_last":3087,"bytes":190,"sha256":"a8ce741ed077a98b35a882d3230aab8ce603f827ab39ff18f0d52bfa4dda316e"},
        {"ordinal":102,"symbol":"sequence_scope","line_first":3088,"line_last":3094,"bytes":336,"sha256":"44354f444ee46c3ef368f3c1b8bd76666a4d2d374125bb39336972f718054ad9"},
        {"ordinal":103,"symbol":"diagnostic_subtree","line_first":3095,"line_last":3104,"bytes":486,"sha256":"c3fe447764bb09e960278ef9bcda9c823abeeaf62894ef8d60c4292c0d916aa0"},
        {"ordinal":104,"symbol":"pending_directory","line_first":3105,"line_last":3126,"bytes":1043,"sha256":"892102472250354620e09d2c01ae8bd259d787cd45b4685985a46f1466abbd6b"},
        {"ordinal":105,"symbol":"authenticate_output_roster","line_first":3127,"line_last":3171,"bytes":2528,"sha256":"557ea4d9a04cd5c951189d06c19a6a9505a8271b3f6332b1af7d2be0c696d927"},
        {"ordinal":106,"symbol":"phase_files","line_first":3172,"line_last":3180,"bytes":353,"sha256":"662f9eef848530ad677b55cd29239370055eb933897834b7b125fdfafccc1e55"},
        {"ordinal":107,"symbol":"read_only_documents","line_first":3181,"line_last":3189,"bytes":390,"sha256":"2fe5a6084ffc461c69fdeba34130d813d9236631b6f71b765660882ab85b7e15"},
        {"ordinal":108,"symbol":"restoration_store","line_first":3190,"line_last":3196,"bytes":407,"sha256":"61cb32f9ef66cf3b49a6f5a6cb5561498f93b2e0e9f39d7d3cb0c80702d04e68"},
        {"ordinal":109,"symbol":"load_private_prefix","line_first":3197,"line_last":3294,"bytes":6509,"sha256":"42d05098144fa23aa8a57d9b6d4ed51156a67ceef1d10236570125d3d79da601"},
        {"ordinal":110,"symbol":"recover_private_metadata","line_first":3295,"line_last":3318,"bytes":1347,"sha256":"2f8994ca208aa585646f6b3236ccdb51cec1d37b99ddbf679b25cab29bfc9edc"},
        {"ordinal":111,"symbol":"completion_log","line_first":3319,"line_last":3324,"bytes":241,"sha256":"f0b0fc0b1ef997ce340da9fdb5914376d29173c802b0cd9db1d2cc08160a3f1e"},
        {"ordinal":112,"symbol":"batch_observation","line_first":3325,"line_last":3395,"bytes":5750,"sha256":"8b24a0a109a2fc82dcbceea8fc2bef9b085e5239bf2b22e5648fe206c4925a18"},
        {"ordinal":113,"symbol":"result_value","line_first":3396,"line_last":3434,"bytes":3219,"sha256":"fc328c91627221721c22781b4365b6edd669e5785c36338b9d1aebd29a4d8fda"},
        {"ordinal":114,"symbol":"authenticate_completed_result","line_first":3435,"line_last":3449,"bytes":927,"sha256":"bdf2b2df52b3aff38e99a4f5041f9df4e173122317d7f9fa453e2008b01e8f9c"},
        {"ordinal":115,"symbol":"append_checkpoint","line_first":3450,"line_last":3460,"bytes":732,"sha256":"76b60325ada7d315607d7889c849e1222c1efec5b6b49d2b8c5d94d3ec9d4dc6"},
        {"ordinal":116,"symbol":"run_selection","line_first":3461,"line_last":3491,"bytes":1775,"sha256":"180a431f3ddc9d1fbde1f12d162c3304497ec1f86955e28215106231458d5edb"},
        {"ordinal":117,"symbol":"run_candidates","line_first":3492,"line_last":3537,"bytes":3020,"sha256":"3ded5ef6a491fd7a6520e6be7e6c485d935dd49c15a4b5a02cc1ffa0b827f452"},
        {"ordinal":118,"symbol":"admit_diagnostics","line_first":3538,"line_last":3601,"bytes":4911,"sha256":"54f22298529efce6f9bd6c672dde558e3118a43a545ab03e2c123666304004b5"},
        {"ordinal":119,"symbol":"output_path_gate","line_first":3602,"line_last":3616,"bytes":904,"sha256":"0d2fd36442b7dcac8ac284b05abbdc18ef3c41dceca8e81774a7a6380a6f7d2b"},
        {"ordinal":120,"symbol":"run_actual","line_first":3617,"line_last":3687,"bytes":4500,"sha256":"180412b6557144eeffb99dc0af6b7dd604da2977d6c5a864d17e61a0646d5341"},
        {"ordinal":121,"symbol":"canary_reject","line_first":3688,"line_last":3696,"bytes":235,"sha256":"0c43737110b1fec08b4ec3b7a92191b12cd24471ca0065939178fb16ca92ccc4"},
        {"ordinal":122,"symbol":"canary_binding","line_first":3697,"line_last":3701,"bytes":215,"sha256":"6d23702c33c5772eadff05cbc09734a6e01b5860271f86eba25b2aa017c0577d"},
        {"ordinal":123,"symbol":"canary_selection_fixture","line_first":3702,"line_last":3739,"bytes":2544,"sha256":"5da935c6bba12d1b2d638cb995195f0c2d8ee5a01a8288e5540a9be47f7001e9"},
        {"ordinal":124,"symbol":"selftest_root_path","line_first":3740,"line_last":3762,"bytes":1149,"sha256":"9a1907f7845b1fcb44ecfa9cea4a91bb143a609e155865aca1dd2b8ff14c7e0f"},
        {"ordinal":125,"symbol":"k128_reject","line_first":3763,"line_last":3775,"bytes":590,"sha256":"a5db86c15ec181cc19fd6821621950bec1a438b627fdb4651136f9bc9b055036"},
        {"ordinal":126,"symbol":"k128_registration_canary","line_first":3776,"line_last":3936,"bytes":10616,"sha256":"a126f95861021f05ba672cf2d70a20754d58eb3479a8f6dc548023242d45d07e"},
        {"ordinal":127,"symbol":"k128_tree_commit","line_first":3937,"line_last":3949,"bytes":741,"sha256":"9152dc0feb393e39e28ef877a358726cdb0c4789aaecdb935baa71e20151e4fc"},
        {"ordinal":128,"symbol":"k128_tree_reload","line_first":3950,"line_last":3972,"bytes":1493,"sha256":"ecf4b6938e5bfd428a904036d15c8b55bd17c192b08bbaf5c119c2bdc99f18df"},
        {"ordinal":129,"symbol":"k128_dependent_continuation_canary","line_first":3973,"line_last":4105,"bytes":9775,"sha256":"a731fa9cb1705102bca1ad306335c0fc0f8e25cbb2e63fc7d5c7294d8ba5cc74"},
        {"ordinal":130,"symbol":"k128_selection_canary","line_first":4106,"line_last":4227,"bytes":8363,"sha256":"d4fd8fa4a78ef66074f97708401725de8e349b34438de73b8b1069f55f6828f3"},
        {"ordinal":131,"symbol":"batch_parent_admission_canary","line_first":4228,"line_last":4281,"bytes":4538,"sha256":"2f0585db30c807fd66853d38042d00b52f33ac0749e25ff2d76b149fdc6aaa22"},
        {"ordinal":132,"symbol":"selftest","line_first":4282,"line_last":4312,"bytes":2388,"sha256":"84ba79cae4d8108c90e0c3a0288610c5ce742f454a6d8576b0a3347255081909"},
        {"ordinal":133,"symbol":"diagnostic","line_first":4313,"line_last":4368,"bytes":4073,"sha256":"c90e67a6ca462b7fca8f3c6b9d1fd90280a9b929f089c9400e652f2f05cad19e"},
        {"ordinal":134,"symbol":"cli","line_first":4369,"line_last":4396,"bytes":1732,"sha256":"8fbc9f9a64afc5d31f5a73b9273144f51332632c18254860778845218602fd75"},
        {"ordinal":135,"symbol":"main","line_first":4397,"line_last":4426,"bytes":1252,"sha256":"1abfd61eb035bd3b9026a3730baa722f6433c196db469f4b75be7fe6093f419e"}
      ],
      "comparisons": [
        {"symbol":"MODULE_PREFIX","baseline_ordinal":0,"current_ordinal":0,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"ResourceStop","baseline_ordinal":1,"current_ordinal":1,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"require","baseline_ordinal":2,"current_ordinal":2,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"integer","baseline_ordinal":3,"current_ordinal":3,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"trit","baseline_ordinal":4,"current_ordinal":4,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"signrep","baseline_ordinal":5,"current_ordinal":5,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"canonical","baseline_ordinal":6,"current_ordinal":6,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"sha","baseline_ordinal":7,"current_ordinal":7,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"seal","baseline_ordinal":8,"current_ordinal":8,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"check_seal","baseline_ordinal":9,"current_ordinal":9,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"exact_keys","baseline_ordinal":10,"current_ordinal":10,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"json_bytes","baseline_ordinal":11,"current_ordinal":11,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"safe_name","baseline_ordinal":12,"current_ordinal":12,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"safe_file","baseline_ordinal":13,"current_ordinal":13,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"file_pin","baseline_ordinal":14,"current_ordinal":14,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"pin_type","baseline_ordinal":15,"current_ordinal":15,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"read_json","baseline_ordinal":16,"current_ordinal":16,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"inventory","baseline_ordinal":17,"current_ordinal":17,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"check_deadline","baseline_ordinal":18,"current_ordinal":18,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"progress","baseline_ordinal":19,"current_ordinal":19,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"request_stop","baseline_ordinal":20,"current_ordinal":20,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"sync_directory","baseline_ordinal":21,"current_ordinal":21,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"atomic_write","baseline_ordinal":22,"current_ordinal":22,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"write_once","baseline_ordinal":23,"current_ordinal":23,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"own_dependencies","baseline_ordinal":24,"current_ordinal":24,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"encode_array","baseline_ordinal":25,"current_ordinal":25,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"decode_array","baseline_ordinal":26,"current_ordinal":26,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"process_measurement","baseline_ordinal":27,"current_ordinal":27,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"phase_telemetry","baseline_ordinal":28,"current_ordinal":28,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"validate_telemetry","baseline_ordinal":29,"current_ordinal":29,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"f3_array","baseline_ordinal":30,"current_ordinal":30,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"classify_batch","baseline_ordinal":31,"current_ordinal":31,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"current_batch_tree","baseline_ordinal":32,"current_ordinal":32,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"make_reduction_state","baseline_ordinal":33,"current_ordinal":33,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"reduce_candidate_numeric","baseline_ordinal":34,"current_ordinal":34,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"advance_reduction_numeric","baseline_ordinal":35,"current_ordinal":35,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"final_separator_numeric","baseline_ordinal":36,"current_ordinal":36,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"character_counts","baseline_ordinal":37,"current_ordinal":37,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"descriptor_list","baseline_ordinal":38,"current_ordinal":38,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"validate_input_inventory","baseline_ordinal":39,"current_ordinal":39,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"root_paths","baseline_ordinal":40,"current_ordinal":40,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"checked_descriptor","baseline_ordinal":41,"current_ordinal":41,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"registered_policy","baseline_ordinal":42,"current_ordinal":42,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"authenticate_registration","baseline_ordinal":43,"current_ordinal":43,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"authenticate_code","baseline_ordinal":44,"current_ordinal":44,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"authenticate_anchor_metadata","baseline_ordinal":45,"current_ordinal":45,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"authenticate_acceptance","baseline_ordinal":46,"current_ordinal":56,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"accepted_oracle_top_metadata","baseline_ordinal":47,"current_ordinal":57,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"parent_row_sources","baseline_ordinal":48,"current_ordinal":58,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"thin_anchor","baseline_ordinal":49,"current_ordinal":59,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"outer_metadata","baseline_ordinal":50,"current_ordinal":61,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"binding_from_metadata","baseline_ordinal":51,"current_ordinal":62,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"phase_roster","baseline_ordinal":52,"current_ordinal":63,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"payload","baseline_ordinal":53,"current_ordinal":64,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"serialize_arrays","baseline_ordinal":54,"current_ordinal":65,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"payload_descriptor","baseline_ordinal":55,"current_ordinal":66,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"atomic_diagnostic","baseline_ordinal":56,"current_ordinal":67,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"phase_manifest_body","baseline_ordinal":57,"current_ordinal":68,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"BatchPhaseStore","baseline_ordinal":58,"current_ordinal":69,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"tree_payloads","baseline_ordinal":59,"current_ordinal":70,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"saved_selection_values","baseline_ordinal":60,"current_ordinal":71,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"publish_selection","baseline_ordinal":61,"current_ordinal":72,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"reduction_payloads","baseline_ordinal":62,"current_ordinal":73,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"restore_reduction","baseline_ordinal":63,"current_ordinal":74,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"publish_candidate_decision","baseline_ordinal":64,"current_ordinal":75,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"checkpoint_value","baseline_ordinal":65,"current_ordinal":76,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"private_head","baseline_ordinal":66,"current_ordinal":77,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"publish_private_checkpoint","baseline_ordinal":67,"current_ordinal":78,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"read_final","baseline_ordinal":68,"current_ordinal":79,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"prepare_final","baseline_ordinal":69,"current_ordinal":80,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"inventory_documents","baseline_ordinal":70,"current_ordinal":81,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"authenticate_input_documents","baseline_ordinal":71,"current_ordinal":82,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"finish_inputs","baseline_ordinal":72,"current_ordinal":83,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"input_preservation","baseline_ordinal":73,"current_ordinal":84,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"validate_launch","baseline_ordinal":74,"current_ordinal":85,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"validate_host_paths","baseline_ordinal":75,"current_ordinal":86,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"validate_invocation_history","baseline_ordinal":76,"current_ordinal":87,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"invocation_files","baseline_ordinal":77,"current_ordinal":88,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"begin_invocation","baseline_ordinal":78,"current_ordinal":89,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"candidate_view","baseline_ordinal":79,"current_ordinal":90,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"legacy_e_input","baseline_ordinal":80,"current_ordinal":91,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"run_candidate_phases","baseline_ordinal":81,"current_ordinal":92,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"current_derived_rho2","baseline_ordinal":82,"current_ordinal":93,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"phase_telemetry_descriptor","baseline_ordinal":83,"current_ordinal":94,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"selection_readout","baseline_ordinal":84,"current_ordinal":95,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"candidate_readout","baseline_ordinal":85,"current_ordinal":96,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"final_payloads","baseline_ordinal":86,"current_ordinal":97,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"final_manifest_value","baseline_ordinal":87,"current_ordinal":98,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"public_head_value","baseline_ordinal":88,"current_ordinal":99,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"same_json","baseline_ordinal":89,"current_ordinal":100,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"phase_prefix","baseline_ordinal":90,"current_ordinal":101,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"sequence_scope","baseline_ordinal":91,"current_ordinal":102,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"diagnostic_subtree","baseline_ordinal":92,"current_ordinal":103,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"pending_directory","baseline_ordinal":93,"current_ordinal":104,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"authenticate_output_roster","baseline_ordinal":94,"current_ordinal":105,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"phase_files","baseline_ordinal":95,"current_ordinal":106,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"read_only_documents","baseline_ordinal":96,"current_ordinal":107,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"restoration_store","baseline_ordinal":97,"current_ordinal":108,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"load_private_prefix","baseline_ordinal":98,"current_ordinal":109,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"recover_private_metadata","baseline_ordinal":99,"current_ordinal":110,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"completion_log","baseline_ordinal":100,"current_ordinal":111,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"result_value","baseline_ordinal":101,"current_ordinal":113,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"authenticate_completed_result","baseline_ordinal":102,"current_ordinal":114,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"append_checkpoint","baseline_ordinal":103,"current_ordinal":115,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"run_selection","baseline_ordinal":104,"current_ordinal":116,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"run_candidates","baseline_ordinal":105,"current_ordinal":117,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"admit_diagnostics","baseline_ordinal":106,"current_ordinal":118,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"output_path_gate","baseline_ordinal":107,"current_ordinal":119,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"run_actual","baseline_ordinal":108,"current_ordinal":120,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"canary_reject","baseline_ordinal":109,"current_ordinal":121,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"canary_binding","baseline_ordinal":110,"current_ordinal":122,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"canary_selection_fixture","baseline_ordinal":111,"current_ordinal":123,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"selftest_root_path","baseline_ordinal":112,"current_ordinal":124,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"k128_reject","baseline_ordinal":113,"current_ordinal":125,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"k128_registration_canary","baseline_ordinal":114,"current_ordinal":126,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"k128_tree_commit","baseline_ordinal":115,"current_ordinal":127,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"k128_tree_reload","baseline_ordinal":116,"current_ordinal":128,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"k128_selection_canary","baseline_ordinal":117,"current_ordinal":130,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"selftest","baseline_ordinal":118,"current_ordinal":132,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"diagnostic","baseline_ordinal":119,"current_ordinal":133,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"cli","baseline_ordinal":120,"current_ordinal":134,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"main","baseline_ordinal":121,"current_ordinal":135,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"batch_anchor_header","baseline_ordinal":null,"current_ordinal":46,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"batch_old_input_projection","baseline_ordinal":null,"current_ordinal":47,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"batch_plain_target_binding","baseline_ordinal":null,"current_ordinal":48,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"old_batch_document","baseline_ordinal":null,"current_ordinal":49,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"batch_binding_matches","baseline_ordinal":null,"current_ordinal":50,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"batch_saved_manifest","baseline_ordinal":null,"current_ordinal":51,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"batch_loader_regions","baseline_ordinal":null,"current_ordinal":52,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"batch_saved_rows","baseline_ordinal":null,"current_ordinal":53,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"batch_saved_checkpoints","baseline_ordinal":null,"current_ordinal":54,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"authenticate_batch_parent","baseline_ordinal":null,"current_ordinal":55,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"promote_batch_anchor","baseline_ordinal":null,"current_ordinal":60,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"batch_observation","baseline_ordinal":null,"current_ordinal":112,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"k128_dependent_continuation_canary","baseline_ordinal":null,"current_ordinal":129,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"batch_parent_admission_canary","baseline_ordinal":null,"current_ordinal":131,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."}
      ]
    },
    {
      "side": "C",
      "baseline_source_id": "C3",
      "current_source_id": "C4",
      "baseline_regions": [
        {"ordinal":0,"symbol":"MODULE_PREFIX","line_first":1,"line_last":138,"bytes":10079,"sha256":"0af03569a6d0b2a897b8a2f5ebddae25b8b4e817c54857767f6bc418d368a96d"},
        {"ordinal":1,"symbol":"ResourceStop","line_first":139,"line_last":142,"bytes":42,"sha256":"071568f742101bf0c4baeb2502647700c4b4198f6a10d1fe94bcd3219ea9ebfc"},
        {"ordinal":2,"symbol":"require","line_first":143,"line_last":147,"bytes":122,"sha256":"c11073d6ee57543f49b3dcd50f3f5117782ab467f251394ab1f5bf0c62d9122d"},
        {"ordinal":3,"symbol":"integer","line_first":148,"line_last":152,"bytes":201,"sha256":"081afa579616b7da4b7ff894d81b4c635c4e9a03f4f73d1399ca1e29e8e55575"},
        {"ordinal":4,"symbol":"boundary","line_first":153,"line_last":168,"bytes":570,"sha256":"726ac0385214ec033671a3c0155a29d0b4fe3c750acfc7fb6dfdf228ce7fb095"},
        {"ordinal":5,"symbol":"document","line_first":169,"line_last":174,"bytes":272,"sha256":"10d512e1451d1b11c27b0f8b01c75991adaa678f54d163b826b81c6c22558589"},
        {"ordinal":6,"symbol":"scalar","line_first":175,"line_last":178,"bytes":84,"sha256":"0231b3668ac51144037e9dd60e0e0c7b1ac87b7d7611d1614898726b5c9c2927"},
        {"ordinal":7,"symbol":"trit_vector","line_first":179,"line_last":183,"bytes":212,"sha256":"5dfd03be2f51afb7c955749175bab47376919c64259ea9978a4fc42387ec2972"},
        {"ordinal":8,"symbol":"packed_vector","line_first":184,"line_last":191,"bytes":344,"sha256":"ecac611ebed4d43535811c9dee61af1c183378bd5ddced00f2c16faf05ffa229"},
        {"ordinal":9,"symbol":"select_all_residuals","line_first":192,"line_last":249,"bytes":4039,"sha256":"3c52d2668c5089a2bc2884257c23e2e23dacf8e5b28b9abf1470197e7cf20acf"},
        {"ordinal":10,"symbol":"SelectionArithmetic","line_first":250,"line_last":260,"bytes":216,"sha256":"50a9dae33cad7ea1afe4bbae71383842b6e5ced21d369bcf31ac787316b68fad"},
        {"ordinal":11,"symbol":"DecisionArithmetic","line_first":261,"line_last":278,"bytes":415,"sha256":"f1432a70cbdae7093d42559cfe70b9a0a98cf882fc80f30aebf18cce53585f54"},
        {"ordinal":12,"symbol":"BatchReductionState","line_first":279,"line_last":380,"bytes":6458,"sha256":"9031bfa4c5eef878974ee2af58f246186320878b947f0dc1796989371c04cbd8"},
        {"ordinal":13,"symbol":"relative_name","line_first":381,"line_last":389,"bytes":387,"sha256":"c864d2c6aac6517bbe9efc061bfc27070fdd06f5cb9c356b0bc86c954cf906da"},
        {"ordinal":14,"symbol":"file_path","line_first":390,"line_last":400,"bytes":445,"sha256":"958cb5f305102a02f89bc80b3830d4b41cc60c054c3599a4498bb2e6d20f9365"},
        {"ordinal":15,"symbol":"json_value","line_first":401,"line_last":416,"bytes":655,"sha256":"f802498bbf47558926b26ccacd0c9378d6b4d3fb121375d29a44cdddf6b90bd9"},
        {"ordinal":16,"symbol":"check_document","line_first":417,"line_last":424,"bytes":470,"sha256":"ad837f4d5346cb0e80cfa609968c0b81f9879b75eb1da33eb9a828bfa2419738"},
        {"ordinal":17,"symbol":"same_json","line_first":425,"line_last":428,"bytes":116,"sha256":"1cd7bad611ac0aa3ae5d9de749980be7794460a97f9f0e2990120404f897d26e"},
        {"ordinal":18,"symbol":"receipt","line_first":429,"line_last":432,"bytes":121,"sha256":"2cb95573e8476e8c369a8fe9b578a13be283f212067a34e6d37727eeb313136f"},
        {"ordinal":19,"symbol":"pin_receipts","line_first":433,"line_last":436,"bytes":194,"sha256":"b93a4cf7a014c0cdb91a5c81b50de1cff6cf3c89cce7ca96e10988a53a187f25"},
        {"ordinal":20,"symbol":"check_file_descriptor","line_first":437,"line_last":443,"bytes":381,"sha256":"68390817768e8511ac25d400a9bae80552c135fc756fd4f31ce17a45cd166cc9"},
        {"ordinal":21,"symbol":"artifact_identity","line_first":444,"line_last":450,"bytes":443,"sha256":"89562c8928112deb1eefd2334799ff0994ce970ce3b27227b9e2aa77f6d00bfe"},
        {"ordinal":22,"symbol":"registered_limits","line_first":451,"line_last":457,"bytes":435,"sha256":"b08c34f532f73f66178cf63bab20ffcfc945101177ee74d231d05b9647bdcf23"},
        {"ordinal":23,"symbol":"check_registration","line_first":458,"line_last":471,"bytes":923,"sha256":"4b80e8e235e649d132b8e1110359a45c7217f1d836f12811cd53000308388a8b"},
        {"ordinal":24,"symbol":"check_acceptance_header","line_first":472,"line_last":476,"bytes":262,"sha256":"62ad741f620ab56e59ab88220a8404200cf5880f6e6d661f8d295d16b87ff91a"},
        {"ordinal":25,"symbol":"check_executable_paths","line_first":477,"line_last":483,"bytes":293,"sha256":"deca02bd5060024a43a0febded006995a518aaaf1b86ecb509410e616aaff584"},
        {"ordinal":26,"symbol":"AcceptedInputs","line_first":484,"line_last":590,"bytes":7795,"sha256":"757db8a1f63e920c96f6f74f412ded311c39ab57d46ba0b3dbdce90631a61feb"},
        {"ordinal":27,"symbol":"hash_file","line_first":591,"line_last":604,"bytes":467,"sha256":"96743c4d7b1e015974ccd7701101817793a545e4a12a4f0a74c70ecdcd8e6f8a"},
        {"ordinal":28,"symbol":"tree_names","line_first":605,"line_last":624,"bytes":845,"sha256":"6ab04d271bddad0800655e90e610d288d708c6d42eee00ca17c825bace239f31"},
        {"ordinal":29,"symbol":"PinnedTree","line_first":625,"line_last":670,"bytes":2457,"sha256":"ac4e6d292c1da806ed90cbad55a620990a9b0c402c3583039b70a1fc7a03288d"},
        {"ordinal":30,"symbol":"SavedPhysicalRow","line_first":671,"line_last":677,"bytes":100,"sha256":"e85627f5435be92778ada7685d5f0014bb3e39931f434b92b0732f64add9cc4b"},
        {"ordinal":31,"symbol":"base_pivot_metadata","line_first":678,"line_last":711,"bytes":2403,"sha256":"5be807b3382c0c938dc16ac5af4906b85f507e8f16b6844004aceebccc6ec1d7"},
        {"ordinal":32,"symbol":"ThinAnchor","line_first":712,"line_last":773,"bytes":3516,"sha256":"f4fe4ef5620b7a4e5256d70e15a1c3b4139827d6b6a717ec3e23a02e6ad6e1a9"},
        {"ordinal":33,"symbol":"saved_manifest_members","line_first":774,"line_last":785,"bytes":582,"sha256":"003db21f67df6c219200f7995ecd3fcd88d9493cc8a4f4bbf7081ad379af7983"},
        {"ordinal":34,"symbol":"restore_physical_anchor","line_first":786,"line_last":956,"bytes":14011,"sha256":"3178867cb0c359149db73088e11bdee4b19b2e1c0acb9914ee4860044c72a231"},
        {"ordinal":35,"symbol":"CandidateFiles","line_first":957,"line_last":997,"bytes":2062,"sha256":"e957b5614092d1cede8c01e09ee73f988894b1ae6bdd2ae836172745973c2f2a"},
        {"ordinal":36,"symbol":"binary_descriptor","line_first":998,"line_last":1008,"bytes":445,"sha256":"9c522f95ff3f7b663c329c0691d055a29127edf38a2aeb466370797642b5ec6d"},
        {"ordinal":37,"symbol":"payload_roster","line_first":1009,"line_last":1012,"bytes":177,"sha256":"5019e1440fe36a6bfbeda39484f825c45574ced852ae356b87e1b5338216a47c"},
        {"ordinal":38,"symbol":"finite_measurement","line_first":1013,"line_last":1016,"bytes":146,"sha256":"371d8e1b1052ee3a3a86f8950d951e9f023e8f136a20ec7cfb533e50607db750"},
        {"ordinal":39,"symbol":"telemetry_record","line_first":1017,"line_last":1040,"bytes":1578,"sha256":"1966f2f42122233bc369ca69c44c3179e03e6507e2c78348f43c84f097ade988"},
        {"ordinal":40,"symbol":"RootRecords","line_first":1041,"line_last":1054,"bytes":529,"sha256":"6bdb51fcb8fe358285e12ffa555d18885c8ae8ac8ed789d76e2381f3fa239575"},
        {"ordinal":41,"symbol":"root_records","line_first":1055,"line_last":1102,"bytes":4242,"sha256":"efee65370f33177a82703931ca5fe64b13927d4570ad29a9f1e928f52bb7805c"},
        {"ordinal":42,"symbol":"compare_root_records","line_first":1103,"line_last":1109,"bytes":421,"sha256":"c7fc7bdb70fc43ea607b635f36eeb68cf9a994454252fbf21cb80cae283c7a6a"},
        {"ordinal":43,"symbol":"compare_phase","line_first":1110,"line_last":1126,"bytes":1169,"sha256":"62206cc9156991d4046225729cc0f47f8ef3dc68e098e184d554209cf40e4a7c"},
        {"ordinal":44,"symbol":"witness_records","line_first":1127,"line_last":1145,"bytes":1226,"sha256":"6110ffee27ac5db232b6070f97004b8f066adcaebefed3ab75f1b3d440fa2d1e"},
        {"ordinal":45,"symbol":"batch_tree_payloads","line_first":1146,"line_last":1170,"bytes":1925,"sha256":"fdf0dbf5ebd337a54059830c21f9283c94e87c50cb1fad5d010a82781d46e8d2"},
        {"ordinal":46,"symbol":"SelectionReplay","line_first":1171,"line_last":1184,"bytes":424,"sha256":"8afeda8ae9172dd400c85ffc20c1122e186dec3b8e185e11c63fc2bce5b010ee"},
        {"ordinal":47,"symbol":"selection_record","line_first":1185,"line_last":1202,"bytes":1563,"sha256":"327907546645f96261659e9c9942c44fe6bd89f4fa3673c57518b861f834ea54"},
        {"ordinal":48,"symbol":"oracle_view_record","line_first":1203,"line_last":1210,"bytes":601,"sha256":"cc94f939585fbf20440db5ac7e2e63cb6a5543b79de3b608048b96700e5efde0"},
        {"ordinal":49,"symbol":"compare_selection_publication","line_first":1211,"line_last":1241,"bytes":1721,"sha256":"28e94664ec7d2df8a5a276ca6fb254aec5574fa00915098ea5791b3c1023b568"},
        {"ordinal":50,"symbol":"replay_selection","line_first":1242,"line_last":1279,"bytes":2487,"sha256":"c48bd67d1486915ef75274c5aecb1c7d45f4281a4188e8a29e7c08fd821dff8c"},
        {"ordinal":51,"symbol":"row_source","line_first":1280,"line_last":1295,"bytes":1001,"sha256":"3c1f2a9d62186b1462190147f096c824af062f884d50974e2b2d689052be138a"},
        {"ordinal":52,"symbol":"reduction_payloads","line_first":1296,"line_last":1350,"bytes":4933,"sha256":"7ae9f3b66c80960b1fdf8b6e6d0b8cc65396376bb82e615b0535716de26b7083"},
        {"ordinal":53,"symbol":"accepted_row_record","line_first":1351,"line_last":1365,"bytes":1422,"sha256":"6cd9412be87ccad21a0882825c26567186c310f6f40b0170cd7c635da0951100"},
        {"ordinal":54,"symbol":"candidate_decision_record","line_first":1366,"line_last":1380,"bytes":1271,"sha256":"8d33554509f01107dedae244bf79bd5c3af8d9b53381cf4997a766d2d98a4bb0"},
        {"ordinal":55,"symbol":"batch_target_parent","line_first":1381,"line_last":1389,"bytes":597,"sha256":"d526aa4ac19529c0d3448b1330c4c70e2739c2fb906f155884124879cefaf9ac"},
        {"ordinal":56,"symbol":"compare_candidate_publication","line_first":1390,"line_last":1418,"bytes":1927,"sha256":"ced2bcdbbc182f54d76b7e49268669e1fa1bd114b7182cae4e056a890101fc17"},
        {"ordinal":57,"symbol":"CandidateReplay","line_first":1419,"line_last":1429,"bytes":273,"sha256":"37ad8748590fdb3bb35a4778ce23ca5169fa9e266f0f25cf9f7242874ecc3684"},
        {"ordinal":58,"symbol":"replay_candidate","line_first":1430,"line_last":1516,"bytes":6879,"sha256":"ecc980c101fae61ac1fbb208578e6069bc6e67ec15e51271537b867d7f6612cc"},
        {"ordinal":59,"symbol":"private_values","line_first":1517,"line_last":1523,"bytes":457,"sha256":"5b4353ceb3660b16f3dd3240067c4235230ceb0282fa1749b2a81f23f0adcb32"},
        {"ordinal":60,"symbol":"checkpoint_record","line_first":1524,"line_last":1534,"bytes":834,"sha256":"7a931843241ce5aff0007aa0ad9b4c0404109fa45d4dc0852f5804dbcd8e301a"},
        {"ordinal":61,"symbol":"progress_head_record","line_first":1535,"line_last":1541,"bytes":468,"sha256":"8d4d37d304a71d859629886ad3fd9f8ba77cec66be18287c6e41dc08f8fba01f"},
        {"ordinal":62,"symbol":"phase_at_sequence","line_first":1542,"line_last":1552,"bytes":490,"sha256":"0481aae937c8be70ab5a2fdd457faa6b2737200c2624e4eef7c0f489d6f7fe07"},
        {"ordinal":63,"symbol":"ProgressAudit","line_first":1553,"line_last":1623,"bytes":4825,"sha256":"09d13a42cfa836ee2e408b7ee4a4a10dc2d9e41e3a33e65b8c2bbfae66d13c40"},
        {"ordinal":64,"symbol":"character_support","line_first":1624,"line_last":1630,"bytes":455,"sha256":"9ef1047da47668632f530131721d89a5af5f81d4f570ff2730fbc828d56499c5"},
        {"ordinal":65,"symbol":"selection_readout","line_first":1631,"line_last":1649,"bytes":1583,"sha256":"dd835dbb2a0e5b3f195ff3333b42fb4054af9979ba1b6e58774094241d0f8124"},
        {"ordinal":66,"symbol":"final_rho2","line_first":1650,"line_last":1660,"bytes":1025,"sha256":"d7b55a251fd9fe483f6a2893e353f2f1d894a5e3aa36ff04598e6a5aab3f1b7e"},
        {"ordinal":67,"symbol":"candidate_readouts","line_first":1661,"line_last":1686,"bytes":1884,"sha256":"eb39a020dd3a34e7965f540c2fb4f5c83b851edb36341b0ef53e1a92d2e89593"},
        {"ordinal":68,"symbol":"FinalReplay","line_first":1687,"line_last":1697,"bytes":231,"sha256":"77247e3901475474710c100d851b057c3e44373eaed8eec0f89e9ba2736ba7ab"},
        {"ordinal":69,"symbol":"compare_final","line_first":1698,"line_last":1746,"bytes":3909,"sha256":"d89946cbe88002b60e6c10c96ad1440597056d3a34f3a41e0f6195325f900fcf"},
        {"ordinal":70,"symbol":"invocation_records","line_first":1747,"line_last":1820,"bytes":5594,"sha256":"22e9acf7bedbd13d57f28a871dc78ca36d9de2fdb3c988d5d662e2b49f915aa1"},
        {"ordinal":71,"symbol":"input_inventories","line_first":1821,"line_last":1835,"bytes":1016,"sha256":"7ff21aedd876decb9513496fe73acded5b388c433ae1c9d2cc150e8df3cdbd5e"},
        {"ordinal":72,"symbol":"compare_producer_result","line_first":1836,"line_last":1875,"bytes":3409,"sha256":"3517081fc652526ebe4c837c6485f14a3b42f189ca28e620a049588c92202473"},
        {"ordinal":73,"symbol":"compare_diagnostic","line_first":1876,"line_last":1922,"bytes":3889,"sha256":"69afafb2bdf14b726901cbef1a45e7b8c54e237f7887320f87c6a1ba56fb7b89"},
        {"ordinal":74,"symbol":"compare_diagnostics","line_first":1923,"line_last":1932,"bytes":632,"sha256":"ba6094cb594507ba563d43325d11b9afc7578a2be5fdb46d6549ca38c0c5678e"},
        {"ordinal":75,"symbol":"registered_basenames","line_first":1933,"line_last":1965,"bytes":2659,"sha256":"c2712937d70d9b3198e1ebd54b7d65e6cf16a30c164528571c62faf805278701"},
        {"ordinal":76,"symbol":"compare_candidate_roster","line_first":1966,"line_last":2013,"bytes":2718,"sha256":"988d4532f79b4bf50a087a2f56604b672e2cc5068896d4b8bfba09bd77f40f32"},
        {"ordinal":77,"symbol":"checker_receipt_template","line_first":2014,"line_last":2029,"bytes":1420,"sha256":"74e2fad12c5243e3524b94cac83b6005ff6b87837ef78f1d03f59e6c4a64cdf8"},
        {"ordinal":78,"symbol":"report_progress","line_first":2030,"line_last":2043,"bytes":758,"sha256":"acdb94f3157786ebe8f0185345d1b11844ab08f062d6bde4117b469c3b33dca7"},
        {"ordinal":79,"symbol":"check_actual","line_first":2044,"line_last":2164,"bytes":8395,"sha256":"d28019c0b46e2baa00425a6f3bcb057a753ab749fe57c9cb46841d223004c836"},
        {"ordinal":80,"symbol":"complete_reduction_coefficients","line_first":2165,"line_last":2180,"bytes":906,"sha256":"ccdd38cb93b30f3da6f3f220dcf3829c59f529ce4da876d3fd464ac160dc3d28"},
        {"ordinal":81,"symbol":"literal_signs","line_first":2181,"line_last":2194,"bytes":824,"sha256":"17dd1d86d73b16b77958181c98eff2cd8a196e423448996ea108506a72f0f060"},
        {"ordinal":82,"symbol":"rejected","line_first":2195,"line_last":2202,"bytes":256,"sha256":"ae49720e0b199586ead87ee270edfbeb6335dc4f7416f0f43b9ae173d9639229"},
        {"ordinal":83,"symbol":"prepare_selftest_root","line_first":2203,"line_last":2221,"bytes":1167,"sha256":"77738ce91b3adc4fef3b7f255f6c66c2b8d26ad125af47b96536435823902def"},
        {"ordinal":84,"symbol":"fixture_write","line_first":2222,"line_last":2232,"bytes":412,"sha256":"493cd2c89344435c20d5e7be0d290bd02a27176f4546cfcf6260bbe66f302bcc"},
        {"ordinal":85,"symbol":"fixture_directory","line_first":2233,"line_last":2240,"bytes":274,"sha256":"9a0e09f4013e70f8ff5e91b5e7d72251d2d08562aef3bf6fe16c408c1e2a2698"},
        {"ordinal":86,"symbol":"fixture_reseal","line_first":2241,"line_last":2246,"bytes":260,"sha256":"8aff96a23e2a2983e95dda84ab7fb8e40b55f13b2bc30ff47566ef969abada1b"},
        {"ordinal":87,"symbol":"k128_fixture_records","line_first":2247,"line_last":2258,"bytes":814,"sha256":"10e88ffdb4c9b15d17b955feff002c20bcfd9436198e8186eea1f9c1502436f8"},
        {"ordinal":88,"symbol":"fixture_phase","line_first":2259,"line_last":2274,"bytes":1112,"sha256":"6e5f008558ad19672380eb32be876e32f41fa9cc6f2029629f86be815064d2d0"},
        {"ordinal":89,"symbol":"K128MetadataAnchor","line_first":2275,"line_last":2288,"bytes":512,"sha256":"890ffa7a68e9cf14953e99ac7cffb59592fe2875490741d6fc63eb6c474263ae"},
        {"ordinal":90,"symbol":"k128_registration_canary","line_first":2289,"line_last":2447,"bytes":10623,"sha256":"0377e91e1a006c7cef6a63f1a512bb460aa59a06fa7f357fff2c745e29e22d6b"},
        {"ordinal":91,"symbol":"k128_roster_canary","line_first":2448,"line_last":2586,"bytes":9208,"sha256":"6e6c3286e17d42466d97dc8965e10056582f6efd00828f48222e9ed6168e864f"},
        {"ordinal":92,"symbol":"selftest","line_first":2587,"line_last":2601,"bytes":1132,"sha256":"d4edfb777faa7ba87c121f2f4793c4006fcc1abcdb00afc9b8ff5fa45b5ff4af"},
        {"ordinal":93,"symbol":"positive_integer","line_first":2602,"line_last":2606,"bytes":159,"sha256":"a82fe8ec06ebf0f0c3954c6c3f779b630c15f649e188ca4299a6fce9f43aca36"},
        {"ordinal":94,"symbol":"output_location","line_first":2607,"line_last":2622,"bytes":981,"sha256":"01356d2567ee2553bc48d31756008c6064c4a6e99a606beddf8b16199a248826"},
        {"ordinal":95,"symbol":"main","line_first":2623,"line_last":2695,"bytes":4249,"sha256":"267e5c23b93f27e2e9442b1d3898b40cb77a3119d9e39906f7138f62ed5571f4"}
      ],
      "current_regions": [
        {"ordinal":0,"symbol":"MODULE_PREFIX","line_first":1,"line_last":190,"bytes":15042,"sha256":"242ada6896d335f346ace87de61badb2ed0995cd2495936e45c715290d4a2193"},
        {"ordinal":1,"symbol":"ResourceStop","line_first":191,"line_last":194,"bytes":42,"sha256":"071568f742101bf0c4baeb2502647700c4b4198f6a10d1fe94bcd3219ea9ebfc"},
        {"ordinal":2,"symbol":"require","line_first":195,"line_last":199,"bytes":122,"sha256":"c11073d6ee57543f49b3dcd50f3f5117782ab467f251394ab1f5bf0c62d9122d"},
        {"ordinal":3,"symbol":"integer","line_first":200,"line_last":204,"bytes":201,"sha256":"081afa579616b7da4b7ff894d81b4c635c4e9a03f4f73d1399ca1e29e8e55575"},
        {"ordinal":4,"symbol":"boundary","line_first":205,"line_last":220,"bytes":570,"sha256":"726ac0385214ec033671a3c0155a29d0b4fe3c750acfc7fb6dfdf228ce7fb095"},
        {"ordinal":5,"symbol":"document","line_first":221,"line_last":226,"bytes":272,"sha256":"10d512e1451d1b11c27b0f8b01c75991adaa678f54d163b826b81c6c22558589"},
        {"ordinal":6,"symbol":"scalar","line_first":227,"line_last":230,"bytes":84,"sha256":"0231b3668ac51144037e9dd60e0e0c7b1ac87b7d7611d1614898726b5c9c2927"},
        {"ordinal":7,"symbol":"trit_vector","line_first":231,"line_last":235,"bytes":212,"sha256":"5dfd03be2f51afb7c955749175bab47376919c64259ea9978a4fc42387ec2972"},
        {"ordinal":8,"symbol":"packed_vector","line_first":236,"line_last":243,"bytes":344,"sha256":"ecac611ebed4d43535811c9dee61af1c183378bd5ddced00f2c16faf05ffa229"},
        {"ordinal":9,"symbol":"select_all_residuals","line_first":244,"line_last":301,"bytes":4039,"sha256":"3c52d2668c5089a2bc2884257c23e2e23dacf8e5b28b9abf1470197e7cf20acf"},
        {"ordinal":10,"symbol":"SelectionArithmetic","line_first":302,"line_last":312,"bytes":216,"sha256":"50a9dae33cad7ea1afe4bbae71383842b6e5ced21d369bcf31ac787316b68fad"},
        {"ordinal":11,"symbol":"DecisionArithmetic","line_first":313,"line_last":330,"bytes":415,"sha256":"f1432a70cbdae7093d42559cfe70b9a0a98cf882fc80f30aebf18cce53585f54"},
        {"ordinal":12,"symbol":"BatchReductionState","line_first":331,"line_last":432,"bytes":6458,"sha256":"9031bfa4c5eef878974ee2af58f246186320878b947f0dc1796989371c04cbd8"},
        {"ordinal":13,"symbol":"relative_name","line_first":433,"line_last":441,"bytes":387,"sha256":"c864d2c6aac6517bbe9efc061bfc27070fdd06f5cb9c356b0bc86c954cf906da"},
        {"ordinal":14,"symbol":"file_path","line_first":442,"line_last":452,"bytes":445,"sha256":"958cb5f305102a02f89bc80b3830d4b41cc60c054c3599a4498bb2e6d20f9365"},
        {"ordinal":15,"symbol":"json_value","line_first":453,"line_last":468,"bytes":655,"sha256":"f802498bbf47558926b26ccacd0c9378d6b4d3fb121375d29a44cdddf6b90bd9"},
        {"ordinal":16,"symbol":"check_document","line_first":469,"line_last":476,"bytes":470,"sha256":"ad837f4d5346cb0e80cfa609968c0b81f9879b75eb1da33eb9a828bfa2419738"},
        {"ordinal":17,"symbol":"same_json","line_first":477,"line_last":480,"bytes":116,"sha256":"1cd7bad611ac0aa3ae5d9de749980be7794460a97f9f0e2990120404f897d26e"},
        {"ordinal":18,"symbol":"receipt","line_first":481,"line_last":484,"bytes":121,"sha256":"2cb95573e8476e8c369a8fe9b578a13be283f212067a34e6d37727eeb313136f"},
        {"ordinal":19,"symbol":"pin_receipts","line_first":485,"line_last":488,"bytes":194,"sha256":"b93a4cf7a014c0cdb91a5c81b50de1cff6cf3c89cce7ca96e10988a53a187f25"},
        {"ordinal":20,"symbol":"check_file_descriptor","line_first":489,"line_last":495,"bytes":381,"sha256":"68390817768e8511ac25d400a9bae80552c135fc756fd4f31ce17a45cd166cc9"},
        {"ordinal":21,"symbol":"artifact_identity","line_first":496,"line_last":502,"bytes":443,"sha256":"89562c8928112deb1eefd2334799ff0994ce970ce3b27227b9e2aa77f6d00bfe"},
        {"ordinal":22,"symbol":"registered_limits","line_first":503,"line_last":509,"bytes":435,"sha256":"b08c34f532f73f66178cf63bab20ffcfc945101177ee74d231d05b9647bdcf23"},
        {"ordinal":23,"symbol":"check_registration","line_first":510,"line_last":523,"bytes":923,"sha256":"4b80e8e235e649d132b8e1110359a45c7217f1d836f12811cd53000308388a8b"},
        {"ordinal":24,"symbol":"check_acceptance_header","line_first":524,"line_last":528,"bytes":280,"sha256":"598c6655beb8354618bc0a768f8d6a1f190184b5d2f7588aad9953383ddbb2d5"},
        {"ordinal":25,"symbol":"check_executable_paths","line_first":529,"line_last":535,"bytes":293,"sha256":"deca02bd5060024a43a0febded006995a518aaaf1b86ecb509410e616aaff584"},
        {"ordinal":26,"symbol":"AcceptedInputs","line_first":536,"line_last":642,"bytes":7736,"sha256":"5a9df21c640b990f688e5c302fdcf927f0e6edd1e7983fb13112ec3e29991499"},
        {"ordinal":27,"symbol":"hash_file","line_first":643,"line_last":656,"bytes":467,"sha256":"96743c4d7b1e015974ccd7701101817793a545e4a12a4f0a74c70ecdcd8e6f8a"},
        {"ordinal":28,"symbol":"tree_names","line_first":657,"line_last":676,"bytes":845,"sha256":"6ab04d271bddad0800655e90e610d288d708c6d42eee00ca17c825bace239f31"},
        {"ordinal":29,"symbol":"PinnedTree","line_first":677,"line_last":722,"bytes":2457,"sha256":"ac4e6d292c1da806ed90cbad55a620990a9b0c402c3583039b70a1fc7a03288d"},
        {"ordinal":30,"symbol":"SavedPhysicalRow","line_first":723,"line_last":729,"bytes":100,"sha256":"e85627f5435be92778ada7685d5f0014bb3e39931f434b92b0732f64add9cc4b"},
        {"ordinal":31,"symbol":"base_pivot_metadata","line_first":730,"line_last":763,"bytes":2403,"sha256":"5be807b3382c0c938dc16ac5af4906b85f507e8f16b6844004aceebccc6ec1d7"},
        {"ordinal":32,"symbol":"ThinAnchor","line_first":764,"line_last":825,"bytes":3516,"sha256":"f4fe4ef5620b7a4e5256d70e15a1c3b4139827d6b6a717ec3e23a02e6ad6e1a9"},
        {"ordinal":33,"symbol":"saved_manifest_members","line_first":826,"line_last":837,"bytes":582,"sha256":"003db21f67df6c219200f7995ecd3fcd88d9493cc8a4f4bbf7081ad379af7983"},
        {"ordinal":34,"symbol":"restore_physical_anchor","line_first":838,"line_last":1008,"bytes":14011,"sha256":"3178867cb0c359149db73088e11bdee4b19b2e1c0acb9914ee4860044c72a231"},
        {"ordinal":35,"symbol":"old_batch_json","line_first":1009,"line_last":1016,"bytes":277,"sha256":"afd24959f3917e0b51a4a03d2c44cb20957e1cad0ae90837bdcb2b1dabd52c68"},
        {"ordinal":36,"symbol":"check_parent_roles","line_first":1017,"line_last":1022,"bytes":253,"sha256":"5cc6c67363229d2e87aae65df6b0c802467161925b059886a15934831b7ac4a4"},
        {"ordinal":37,"symbol":"check_batch_parent_header","line_first":1023,"line_last":1037,"bytes":1007,"sha256":"24a97bd8a5dc9b2ad7ef558d1d4d6baa10dbc51ca65bba6bbc8c325e8598d76e"},
        {"ordinal":38,"symbol":"projected_batch_current","line_first":1038,"line_last":1044,"bytes":398,"sha256":"b93456df3ea550adc24d040f37f61d9cb72c04281524bd5c838d37a2d3c74ad1"},
        {"ordinal":39,"symbol":"check_batch_current_projection","line_first":1045,"line_last":1049,"bytes":220,"sha256":"ad779c12327e967170c4e2daaa36da50e0b059f97962738f00f8f2d795382b9e"},
        {"ordinal":40,"symbol":"check_saved_batch_target","line_first":1050,"line_last":1060,"bytes":711,"sha256":"64b0357d3c829dcd077e647860746405b752609397a65a3be93abd5a803073b5"},
        {"ordinal":41,"symbol":"raw_loader_range","line_first":1061,"line_last":1076,"bytes":956,"sha256":"cb7060677fe363932bca6ed5aa1da51f4cb38e1759eefcce70dcdb62c813bbcc"},
        {"ordinal":42,"symbol":"loader_region_pairs","line_first":1077,"line_last":1101,"bytes":1596,"sha256":"06f6b8fdc447db331dabb4a7c5e89856d1652b8ef3cc257ff9864041f5a421ee"},
        {"ordinal":43,"symbol":"batch_bound","line_first":1102,"line_last":1106,"bytes":190,"sha256":"58d3a2c46d2fca4acbae5447924a4019ad4592ff30e3b83517521a52be1a4061"},
        {"ordinal":44,"symbol":"batch_manifest_files","line_first":1107,"line_last":1127,"bytes":1300,"sha256":"e83f7f78b3fdde25ac1e6b86edab1f58e1e799fe9e1eaf8f79b787a29ccd28c1"},
        {"ordinal":45,"symbol":"read_batch_phase","line_first":1128,"line_last":1148,"bytes":1605,"sha256":"f80106c94a17fcebd7ad6fa19daa6131a5fa30e56d1b0f68850c027c53138623"},
        {"ordinal":46,"symbol":"authenticate_batch_parent_metadata","line_first":1149,"line_last":1298,"bytes":13559,"sha256":"2e9952e9d51e7cb25b343625b3c3ce8cfcf523539593615cd2f8e5d9fbdc2479"},
        {"ordinal":47,"symbol":"old_batch_object","line_first":1299,"line_last":1303,"bytes":210,"sha256":"6e3f116e77b06639bf7ebd420a7c9b02dbdbff17db38ab3b77a058fc1f57ae6b"},
        {"ordinal":48,"symbol":"saved_row_source","line_first":1304,"line_last":1313,"bytes":506,"sha256":"663555403d719ed3c6a1f1f7bc5991d54a4ddeafe30c0ec597725b59f7876f5b"},
        {"ordinal":49,"symbol":"authenticate_saved_batch_rows","line_first":1314,"line_last":1536,"bytes":20163,"sha256":"bf01f63eda15e94a33773e5e0f4ce565e462c24067634bdb7fd57efbba559153"},
        {"ordinal":50,"symbol":"authenticate_saved_batch_progress","line_first":1537,"line_last":1630,"bytes":7473,"sha256":"b25886da6173b34fb91046f3386a26297f8d006ab85dcb7b06b7546dae772f33"},
        {"ordinal":51,"symbol":"promote_batch_parent","line_first":1631,"line_last":1649,"bytes":1129,"sha256":"bb36e4bb331cf7e64a184fbfb66ac88140ac172f9b6a45541838c73ec14822a2"},
        {"ordinal":52,"symbol":"parent_intake_record","line_first":1650,"line_last":1668,"bytes":1671,"sha256":"d27c6e7cf7fb57ea2bba4beabe392f3b33997ca3d9d699738d8998784ffe9623"},
        {"ordinal":53,"symbol":"CandidateFiles","line_first":1669,"line_last":1709,"bytes":2062,"sha256":"e957b5614092d1cede8c01e09ee73f988894b1ae6bdd2ae836172745973c2f2a"},
        {"ordinal":54,"symbol":"binary_descriptor","line_first":1710,"line_last":1720,"bytes":445,"sha256":"9c522f95ff3f7b663c329c0691d055a29127edf38a2aeb466370797642b5ec6d"},
        {"ordinal":55,"symbol":"payload_roster","line_first":1721,"line_last":1724,"bytes":177,"sha256":"5019e1440fe36a6bfbeda39484f825c45574ced852ae356b87e1b5338216a47c"},
        {"ordinal":56,"symbol":"finite_measurement","line_first":1725,"line_last":1728,"bytes":146,"sha256":"371d8e1b1052ee3a3a86f8950d951e9f023e8f136a20ec7cfb533e50607db750"},
        {"ordinal":57,"symbol":"telemetry_record","line_first":1729,"line_last":1752,"bytes":1578,"sha256":"1966f2f42122233bc369ca69c44c3179e03e6507e2c78348f43c84f097ade988"},
        {"ordinal":58,"symbol":"RootRecords","line_first":1753,"line_last":1767,"bytes":577,"sha256":"9a7de76fa85387a1fd3169638b43fcc5674ed93be6433c6c83970431caa13014"},
        {"ordinal":59,"symbol":"root_records","line_first":1768,"line_last":1823,"bytes":4939,"sha256":"be12b7e82bcc8faf08516e711a4805ba2b13cd4f0268d04071a060ad0bd3e013"},
        {"ordinal":60,"symbol":"compare_root_records","line_first":1824,"line_last":1832,"bytes":529,"sha256":"15b5e698a33d7bad963db94b9fbb2af971479a09d1547423269307947f25e9ca"},
        {"ordinal":61,"symbol":"compare_phase","line_first":1833,"line_last":1849,"bytes":1169,"sha256":"62206cc9156991d4046225729cc0f47f8ef3dc68e098e184d554209cf40e4a7c"},
        {"ordinal":62,"symbol":"witness_records","line_first":1850,"line_last":1868,"bytes":1226,"sha256":"6110ffee27ac5db232b6070f97004b8f066adcaebefed3ab75f1b3d440fa2d1e"},
        {"ordinal":63,"symbol":"batch_tree_payloads","line_first":1869,"line_last":1893,"bytes":1925,"sha256":"fdf0dbf5ebd337a54059830c21f9283c94e87c50cb1fad5d010a82781d46e8d2"},
        {"ordinal":64,"symbol":"SelectionReplay","line_first":1894,"line_last":1907,"bytes":424,"sha256":"8afeda8ae9172dd400c85ffc20c1122e186dec3b8e185e11c63fc2bce5b010ee"},
        {"ordinal":65,"symbol":"selection_record","line_first":1908,"line_last":1925,"bytes":1563,"sha256":"327907546645f96261659e9c9942c44fe6bd89f4fa3673c57518b861f834ea54"},
        {"ordinal":66,"symbol":"oracle_view_record","line_first":1926,"line_last":1933,"bytes":601,"sha256":"cc94f939585fbf20440db5ac7e2e63cb6a5543b79de3b608048b96700e5efde0"},
        {"ordinal":67,"symbol":"compare_selection_publication","line_first":1934,"line_last":1964,"bytes":1721,"sha256":"28e94664ec7d2df8a5a276ca6fb254aec5574fa00915098ea5791b3c1023b568"},
        {"ordinal":68,"symbol":"replay_selection","line_first":1965,"line_last":2002,"bytes":2487,"sha256":"c48bd67d1486915ef75274c5aecb1c7d45f4281a4188e8a29e7c08fd821dff8c"},
        {"ordinal":69,"symbol":"row_source","line_first":2003,"line_last":2018,"bytes":1001,"sha256":"3c1f2a9d62186b1462190147f096c824af062f884d50974e2b2d689052be138a"},
        {"ordinal":70,"symbol":"reduction_payloads","line_first":2019,"line_last":2073,"bytes":4933,"sha256":"7ae9f3b66c80960b1fdf8b6e6d0b8cc65396376bb82e615b0535716de26b7083"},
        {"ordinal":71,"symbol":"accepted_row_record","line_first":2074,"line_last":2088,"bytes":1422,"sha256":"6cd9412be87ccad21a0882825c26567186c310f6f40b0170cd7c635da0951100"},
        {"ordinal":72,"symbol":"candidate_decision_record","line_first":2089,"line_last":2103,"bytes":1271,"sha256":"8d33554509f01107dedae244bf79bd5c3af8d9b53381cf4997a766d2d98a4bb0"},
        {"ordinal":73,"symbol":"batch_target_parent","line_first":2104,"line_last":2112,"bytes":597,"sha256":"d526aa4ac19529c0d3448b1330c4c70e2739c2fb906f155884124879cefaf9ac"},
        {"ordinal":74,"symbol":"compare_candidate_publication","line_first":2113,"line_last":2141,"bytes":1927,"sha256":"ced2bcdbbc182f54d76b7e49268669e1fa1bd114b7182cae4e056a890101fc17"},
        {"ordinal":75,"symbol":"CandidateReplay","line_first":2142,"line_last":2152,"bytes":273,"sha256":"37ad8748590fdb3bb35a4778ce23ca5169fa9e266f0f25cf9f7242874ecc3684"},
        {"ordinal":76,"symbol":"replay_candidate","line_first":2153,"line_last":2239,"bytes":6879,"sha256":"ecc980c101fae61ac1fbb208578e6069bc6e67ec15e51271537b867d7f6612cc"},
        {"ordinal":77,"symbol":"private_values","line_first":2240,"line_last":2246,"bytes":457,"sha256":"5b4353ceb3660b16f3dd3240067c4235230ceb0282fa1749b2a81f23f0adcb32"},
        {"ordinal":78,"symbol":"checkpoint_record","line_first":2247,"line_last":2257,"bytes":834,"sha256":"7a931843241ce5aff0007aa0ad9b4c0404109fa45d4dc0852f5804dbcd8e301a"},
        {"ordinal":79,"symbol":"progress_head_record","line_first":2258,"line_last":2264,"bytes":468,"sha256":"8d4d37d304a71d859629886ad3fd9f8ba77cec66be18287c6e41dc08f8fba01f"},
        {"ordinal":80,"symbol":"phase_at_sequence","line_first":2265,"line_last":2275,"bytes":490,"sha256":"0481aae937c8be70ab5a2fdd457faa6b2737200c2624e4eef7c0f489d6f7fe07"},
        {"ordinal":81,"symbol":"ProgressAudit","line_first":2276,"line_last":2346,"bytes":4825,"sha256":"09d13a42cfa836ee2e408b7ee4a4a10dc2d9e41e3a33e65b8c2bbfae66d13c40"},
        {"ordinal":82,"symbol":"character_support","line_first":2347,"line_last":2353,"bytes":455,"sha256":"9ef1047da47668632f530131721d89a5af5f81d4f570ff2730fbc828d56499c5"},
        {"ordinal":83,"symbol":"selection_readout","line_first":2354,"line_last":2372,"bytes":1583,"sha256":"dd835dbb2a0e5b3f195ff3333b42fb4054af9979ba1b6e58774094241d0f8124"},
        {"ordinal":84,"symbol":"final_rho2","line_first":2373,"line_last":2385,"bytes":1119,"sha256":"3a5052ae7811a8b0b5349de2e4ac3177be72f7ff96d57444fe43c45d25aa2603"},
        {"ordinal":85,"symbol":"candidate_readouts","line_first":2386,"line_last":2411,"bytes":1884,"sha256":"eb39a020dd3a34e7965f540c2fb4f5c83b851edb36341b0ef53e1a92d2e89593"},
        {"ordinal":86,"symbol":"FinalReplay","line_first":2412,"line_last":2422,"bytes":231,"sha256":"77247e3901475474710c100d851b057c3e44373eaed8eec0f89e9ba2736ba7ab"},
        {"ordinal":87,"symbol":"compare_final","line_first":2423,"line_last":2472,"bytes":3995,"sha256":"6acdac202425c0c813ed2475c4c727e6a940ec9251893dbb995642410d3cff8b"},
        {"ordinal":88,"symbol":"invocation_records","line_first":2473,"line_last":2546,"bytes":5594,"sha256":"22e9acf7bedbd13d57f28a871dc78ca36d9de2fdb3c988d5d662e2b49f915aa1"},
        {"ordinal":89,"symbol":"input_inventories","line_first":2547,"line_last":2561,"bytes":1016,"sha256":"7ff21aedd876decb9513496fe73acded5b388c433ae1c9d2cc150e8df3cdbd5e"},
        {"ordinal":90,"symbol":"batch_observation","line_first":2562,"line_last":2626,"bytes":5124,"sha256":"9fff82efb5c7f1e62cb75c2efeb881760ea99c05142188ee185247f0e2c3f174"},
        {"ordinal":91,"symbol":"compare_producer_result","line_first":2627,"line_last":2667,"bytes":3554,"sha256":"f33718f7b8aa50dc8171337fe4ee2d7b242fbb4b0c19b8cb1495272623926bbb"},
        {"ordinal":92,"symbol":"compare_diagnostic","line_first":2668,"line_last":2725,"bytes":4763,"sha256":"e3078839cdb7ba4b62cdb59fc5cbc16ea91fcea70cfe683028b536e756b2fc24"},
        {"ordinal":93,"symbol":"compare_diagnostics","line_first":2726,"line_last":2735,"bytes":632,"sha256":"ba6094cb594507ba563d43325d11b9afc7578a2be5fdb46d6549ca38c0c5678e"},
        {"ordinal":94,"symbol":"registered_basenames","line_first":2736,"line_last":2768,"bytes":2681,"sha256":"21294a7f84e9d3e3d48f3315fc65110fcd401d294d014f240f3f24648b0bd151"},
        {"ordinal":95,"symbol":"compare_candidate_roster","line_first":2769,"line_last":2816,"bytes":2718,"sha256":"988d4532f79b4bf50a087a2f56604b672e2cc5068896d4b8bfba09bd77f40f32"},
        {"ordinal":96,"symbol":"checker_receipt_template","line_first":2817,"line_last":2834,"bytes":1572,"sha256":"37178d6b02276016438cf3da4ac831956a4968b0d7440d29d3d493e8c59da498"},
        {"ordinal":97,"symbol":"report_progress","line_first":2835,"line_last":2848,"bytes":758,"sha256":"acdb94f3157786ebe8f0185345d1b11844ab08f062d6bde4117b469c3b33dca7"},
        {"ordinal":98,"symbol":"check_actual","line_first":2849,"line_last":2978,"bytes":9292,"sha256":"0e876530877bc147df700b16c9760ce259e4e3ac8f9d27460771101d288fbb7d"},
        {"ordinal":99,"symbol":"complete_reduction_coefficients","line_first":2979,"line_last":2994,"bytes":906,"sha256":"ccdd38cb93b30f3da6f3f220dcf3829c59f529ce4da876d3fd464ac160dc3d28"},
        {"ordinal":100,"symbol":"literal_signs","line_first":2995,"line_last":3008,"bytes":824,"sha256":"17dd1d86d73b16b77958181c98eff2cd8a196e423448996ea108506a72f0f060"},
        {"ordinal":101,"symbol":"rejected","line_first":3009,"line_last":3016,"bytes":256,"sha256":"ae49720e0b199586ead87ee270edfbeb6335dc4f7416f0f43b9ae173d9639229"},
        {"ordinal":102,"symbol":"prepare_selftest_root","line_first":3017,"line_last":3035,"bytes":1167,"sha256":"77738ce91b3adc4fef3b7f255f6c66c2b8d26ad125af47b96536435823902def"},
        {"ordinal":103,"symbol":"fixture_write","line_first":3036,"line_last":3046,"bytes":412,"sha256":"493cd2c89344435c20d5e7be0d290bd02a27176f4546cfcf6260bbe66f302bcc"},
        {"ordinal":104,"symbol":"fixture_directory","line_first":3047,"line_last":3054,"bytes":274,"sha256":"9a0e09f4013e70f8ff5e91b5e7d72251d2d08562aef3bf6fe16c408c1e2a2698"},
        {"ordinal":105,"symbol":"fixture_reseal","line_first":3055,"line_last":3060,"bytes":260,"sha256":"8aff96a23e2a2983e95dda84ab7fb8e40b55f13b2bc30ff47566ef969abada1b"},
        {"ordinal":106,"symbol":"k128_fixture_records","line_first":3061,"line_last":3072,"bytes":814,"sha256":"10e88ffdb4c9b15d17b955feff002c20bcfd9436198e8186eea1f9c1502436f8"},
        {"ordinal":107,"symbol":"fixture_phase","line_first":3073,"line_last":3088,"bytes":1112,"sha256":"6e5f008558ad19672380eb32be876e32f41fa9cc6f2029629f86be815064d2d0"},
        {"ordinal":108,"symbol":"K128MetadataAnchor","line_first":3089,"line_last":3102,"bytes":512,"sha256":"890ffa7a68e9cf14953e99ac7cffb59592fe2875490741d6fc63eb6c474263ae"},
        {"ordinal":109,"symbol":"k128_registration_canary","line_first":3103,"line_last":3261,"bytes":10643,"sha256":"f1e74cf1844192bcc63919e02f7dd3f77a95a805f7e84fea7c69f752a4c44125"},
        {"ordinal":110,"symbol":"k128_dependent_publication_canary","line_first":3262,"line_last":3399,"bytes":10195,"sha256":"a7623d21301d17bf8254f67888748b081224adad1a8383551f28e4adc4a2c746"},
        {"ordinal":111,"symbol":"k128_roster_canary","line_first":3400,"line_last":3539,"bytes":9324,"sha256":"dbac467c0bc1ef708d66a6e0af0508359c85f2de544183eb3efeb1d5c6c3fce3"},
        {"ordinal":112,"symbol":"batch_parent_admission_canary","line_first":3540,"line_last":3609,"bytes":4813,"sha256":"09daca95d0d8ee0a59ad46adfbabb6bbaad203c509b6941079484648ec5aec93"},
        {"ordinal":113,"symbol":"selftest","line_first":3610,"line_last":3630,"bytes":1851,"sha256":"adc630433e43644924e44ef1132cd7ec737e7f9b689656542b002e63323aa6c2"},
        {"ordinal":114,"symbol":"positive_integer","line_first":3631,"line_last":3635,"bytes":159,"sha256":"a82fe8ec06ebf0f0c3954c6c3f779b630c15f649e188ca4299a6fce9f43aca36"},
        {"ordinal":115,"symbol":"output_location","line_first":3636,"line_last":3651,"bytes":981,"sha256":"01356d2567ee2553bc48d31756008c6064c4a6e99a606beddf8b16199a248826"},
        {"ordinal":116,"symbol":"main","line_first":3652,"line_last":3724,"bytes":4249,"sha256":"c1cca17d6ee99118be46cee48eaa349881c86b61e224594350f849b66ed5b1af"}
      ],
      "comparisons": [
        {"symbol":"MODULE_PREFIX","baseline_ordinal":0,"current_ordinal":0,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"ResourceStop","baseline_ordinal":1,"current_ordinal":1,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"require","baseline_ordinal":2,"current_ordinal":2,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"integer","baseline_ordinal":3,"current_ordinal":3,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"boundary","baseline_ordinal":4,"current_ordinal":4,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"document","baseline_ordinal":5,"current_ordinal":5,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"scalar","baseline_ordinal":6,"current_ordinal":6,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"trit_vector","baseline_ordinal":7,"current_ordinal":7,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"packed_vector","baseline_ordinal":8,"current_ordinal":8,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"select_all_residuals","baseline_ordinal":9,"current_ordinal":9,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"SelectionArithmetic","baseline_ordinal":10,"current_ordinal":10,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"DecisionArithmetic","baseline_ordinal":11,"current_ordinal":11,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"BatchReductionState","baseline_ordinal":12,"current_ordinal":12,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"relative_name","baseline_ordinal":13,"current_ordinal":13,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"file_path","baseline_ordinal":14,"current_ordinal":14,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"json_value","baseline_ordinal":15,"current_ordinal":15,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"check_document","baseline_ordinal":16,"current_ordinal":16,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"same_json","baseline_ordinal":17,"current_ordinal":17,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"receipt","baseline_ordinal":18,"current_ordinal":18,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"pin_receipts","baseline_ordinal":19,"current_ordinal":19,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"check_file_descriptor","baseline_ordinal":20,"current_ordinal":20,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"artifact_identity","baseline_ordinal":21,"current_ordinal":21,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"registered_limits","baseline_ordinal":22,"current_ordinal":22,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"check_registration","baseline_ordinal":23,"current_ordinal":23,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"check_acceptance_header","baseline_ordinal":24,"current_ordinal":24,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"check_executable_paths","baseline_ordinal":25,"current_ordinal":25,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"AcceptedInputs","baseline_ordinal":26,"current_ordinal":26,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"hash_file","baseline_ordinal":27,"current_ordinal":27,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"tree_names","baseline_ordinal":28,"current_ordinal":28,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"PinnedTree","baseline_ordinal":29,"current_ordinal":29,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"SavedPhysicalRow","baseline_ordinal":30,"current_ordinal":30,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"base_pivot_metadata","baseline_ordinal":31,"current_ordinal":31,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"ThinAnchor","baseline_ordinal":32,"current_ordinal":32,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"saved_manifest_members","baseline_ordinal":33,"current_ordinal":33,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"restore_physical_anchor","baseline_ordinal":34,"current_ordinal":34,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"CandidateFiles","baseline_ordinal":35,"current_ordinal":53,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"binary_descriptor","baseline_ordinal":36,"current_ordinal":54,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"payload_roster","baseline_ordinal":37,"current_ordinal":55,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"finite_measurement","baseline_ordinal":38,"current_ordinal":56,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"telemetry_record","baseline_ordinal":39,"current_ordinal":57,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"RootRecords","baseline_ordinal":40,"current_ordinal":58,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"root_records","baseline_ordinal":41,"current_ordinal":59,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"compare_root_records","baseline_ordinal":42,"current_ordinal":60,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"compare_phase","baseline_ordinal":43,"current_ordinal":61,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"witness_records","baseline_ordinal":44,"current_ordinal":62,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"batch_tree_payloads","baseline_ordinal":45,"current_ordinal":63,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"SelectionReplay","baseline_ordinal":46,"current_ordinal":64,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"selection_record","baseline_ordinal":47,"current_ordinal":65,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"oracle_view_record","baseline_ordinal":48,"current_ordinal":66,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"compare_selection_publication","baseline_ordinal":49,"current_ordinal":67,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"replay_selection","baseline_ordinal":50,"current_ordinal":68,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"row_source","baseline_ordinal":51,"current_ordinal":69,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"reduction_payloads","baseline_ordinal":52,"current_ordinal":70,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"accepted_row_record","baseline_ordinal":53,"current_ordinal":71,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"candidate_decision_record","baseline_ordinal":54,"current_ordinal":72,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"batch_target_parent","baseline_ordinal":55,"current_ordinal":73,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"compare_candidate_publication","baseline_ordinal":56,"current_ordinal":74,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"CandidateReplay","baseline_ordinal":57,"current_ordinal":75,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"replay_candidate","baseline_ordinal":58,"current_ordinal":76,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"private_values","baseline_ordinal":59,"current_ordinal":77,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"checkpoint_record","baseline_ordinal":60,"current_ordinal":78,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"progress_head_record","baseline_ordinal":61,"current_ordinal":79,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"phase_at_sequence","baseline_ordinal":62,"current_ordinal":80,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"ProgressAudit","baseline_ordinal":63,"current_ordinal":81,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"character_support","baseline_ordinal":64,"current_ordinal":82,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"selection_readout","baseline_ordinal":65,"current_ordinal":83,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"final_rho2","baseline_ordinal":66,"current_ordinal":84,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"candidate_readouts","baseline_ordinal":67,"current_ordinal":85,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"FinalReplay","baseline_ordinal":68,"current_ordinal":86,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"compare_final","baseline_ordinal":69,"current_ordinal":87,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"invocation_records","baseline_ordinal":70,"current_ordinal":88,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"input_inventories","baseline_ordinal":71,"current_ordinal":89,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"compare_producer_result","baseline_ordinal":72,"current_ordinal":91,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"compare_diagnostic","baseline_ordinal":73,"current_ordinal":92,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"compare_diagnostics","baseline_ordinal":74,"current_ordinal":93,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"registered_basenames","baseline_ordinal":75,"current_ordinal":94,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"compare_candidate_roster","baseline_ordinal":76,"current_ordinal":95,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"checker_receipt_template","baseline_ordinal":77,"current_ordinal":96,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"report_progress","baseline_ordinal":78,"current_ordinal":97,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"check_actual","baseline_ordinal":79,"current_ordinal":98,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"complete_reduction_coefficients","baseline_ordinal":80,"current_ordinal":99,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"literal_signs","baseline_ordinal":81,"current_ordinal":100,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"rejected","baseline_ordinal":82,"current_ordinal":101,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"prepare_selftest_root","baseline_ordinal":83,"current_ordinal":102,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"fixture_write","baseline_ordinal":84,"current_ordinal":103,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"fixture_directory","baseline_ordinal":85,"current_ordinal":104,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"fixture_reseal","baseline_ordinal":86,"current_ordinal":105,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"k128_fixture_records","baseline_ordinal":87,"current_ordinal":106,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"fixture_phase","baseline_ordinal":88,"current_ordinal":107,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"K128MetadataAnchor","baseline_ordinal":89,"current_ordinal":108,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"k128_registration_canary","baseline_ordinal":90,"current_ordinal":109,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"k128_roster_canary","baseline_ordinal":91,"current_ordinal":111,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"selftest","baseline_ordinal":92,"current_ordinal":113,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"positive_integer","baseline_ordinal":93,"current_ordinal":114,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"output_location","baseline_ordinal":94,"current_ordinal":115,"classification":"EXACT_RAW_BYTES_UNCHANGED","scope":"Full raw LF region unchanged; retained scope only, no current call coverage measured."},
        {"symbol":"main","baseline_ordinal":95,"current_ordinal":116,"classification":"REGISTERED_CHANGED_RAW_BYTES","scope":"Changed v4 whole raw LF region; includes registration, parent1578 adapter or fixture context and is not certified by historical60."},
        {"symbol":"old_batch_json","baseline_ordinal":null,"current_ordinal":35,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"check_parent_roles","baseline_ordinal":null,"current_ordinal":36,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"check_batch_parent_header","baseline_ordinal":null,"current_ordinal":37,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"projected_batch_current","baseline_ordinal":null,"current_ordinal":38,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"check_batch_current_projection","baseline_ordinal":null,"current_ordinal":39,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"check_saved_batch_target","baseline_ordinal":null,"current_ordinal":40,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"raw_loader_range","baseline_ordinal":null,"current_ordinal":41,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"loader_region_pairs","baseline_ordinal":null,"current_ordinal":42,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"batch_bound","baseline_ordinal":null,"current_ordinal":43,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"batch_manifest_files","baseline_ordinal":null,"current_ordinal":44,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"read_batch_phase","baseline_ordinal":null,"current_ordinal":45,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"authenticate_batch_parent_metadata","baseline_ordinal":null,"current_ordinal":46,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"old_batch_object","baseline_ordinal":null,"current_ordinal":47,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"saved_row_source","baseline_ordinal":null,"current_ordinal":48,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"authenticate_saved_batch_rows","baseline_ordinal":null,"current_ordinal":49,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"authenticate_saved_batch_progress","baseline_ordinal":null,"current_ordinal":50,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"promote_batch_parent","baseline_ordinal":null,"current_ordinal":51,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"parent_intake_record","baseline_ordinal":null,"current_ordinal":52,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"batch_observation","baseline_ordinal":null,"current_ordinal":90,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"k128_dependent_publication_canary","baseline_ordinal":null,"current_ordinal":110,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."},
        {"symbol":"batch_parent_admission_canary","baseline_ordinal":null,"current_ordinal":112,"classification":"ADDED_CURRENT","scope":"New v4 whole raw LF region; separately registered for root source review, not covered by historical60."}
      ]
    }
  ],
  "old_loader_context": [
    {"side":"P","name":"authenticate_anchor_metadata","baseline":{"source_id":"P3","line_first":1047,"line_last":1124,"bytes":6289,"sha256":"2d45494a3dbc6064b2ea08f39fba6e5288ba539e36eeeef893b427d0efca0b55"},"current":{"source_id":"P4","line_first":1220,"line_last":1297,"bytes":6289,"sha256":"2d45494a3dbc6064b2ea08f39fba6e5288ba539e36eeeef893b427d0efca0b55"},"old_anchor_semantics":{"completed_steps":64,"rank":1450,"generation":8155,"original_roles_count":15},"wrapper_and_roots_review":"authenticate_acceptance supplies paths[continuation], the unchanged acceptance.anchor and its inventory to authenticate_anchor_metadata. run_actual calls thin_anchor before promote_batch_anchor; thin_anchor reads continuation/output and its 64 snapshots, with parent_row_sources from original accepted parents. New batch rows enter only the later adapter. This statement is static source context, not measured call coverage.","changed_globals_review":"Outer SCHEMA, WORKFLOW and registered self source change to v4; ROLES appends batch-parent as16th. Original retained imports, continuation root, 64-loop bound, old anchor objects and saved loop schema stay distinct from BATCH_SCHEMA v3 and current batch_anchor. New parent promotion happens after the preserved old loader returns rank1450. Root separately reviews new adapter arithmetic.","byte_identical":true,"current_run_call_coverage":"NOT_MEASURED"},
    {"side":"P","name":"accepted_oracle_top_metadata","baseline":{"source_id":"P3","line_first":1168,"line_last":1192,"bytes":1920,"sha256":"47077c84812c4caf7cb782e12a43c4ee0e61126111e84fdf4b57e7339b96f610"},"current":{"source_id":"P4","line_first":1804,"line_last":1828,"bytes":1920,"sha256":"47077c84812c4caf7cb782e12a43c4ee0e61126111e84fdf4b57e7339b96f610"},"old_anchor_semantics":{"completed_steps":64,"rank":1450,"generation":8155,"original_roles_count":15},"wrapper_and_roots_review":"authenticate_acceptance supplies paths[continuation], the unchanged acceptance.anchor and its inventory to authenticate_anchor_metadata. run_actual calls thin_anchor before promote_batch_anchor; thin_anchor reads continuation/output and its 64 snapshots, with parent_row_sources from original accepted parents. New batch rows enter only the later adapter. This statement is static source context, not measured call coverage.","changed_globals_review":"Outer SCHEMA, WORKFLOW and registered self source change to v4; ROLES appends batch-parent as16th. Original retained imports, continuation root, 64-loop bound, old anchor objects and saved loop schema stay distinct from BATCH_SCHEMA v3 and current batch_anchor. New parent promotion happens after the preserved old loader returns rank1450. Root separately reviews new adapter arithmetic.","byte_identical":true,"current_run_call_coverage":"NOT_MEASURED"},
    {"side":"P","name":"parent_row_sources","baseline":{"source_id":"P3","line_first":1193,"line_last":1226,"bytes":2180,"sha256":"683367b46c3ffd5b586204e95562190fe42146a0542f8bacb3406125a616e4fa"},"current":{"source_id":"P4","line_first":1829,"line_last":1862,"bytes":2180,"sha256":"683367b46c3ffd5b586204e95562190fe42146a0542f8bacb3406125a616e4fa"},"old_anchor_semantics":{"completed_steps":64,"rank":1450,"generation":8155,"original_roles_count":15},"wrapper_and_roots_review":"authenticate_acceptance supplies paths[continuation], the unchanged acceptance.anchor and its inventory to authenticate_anchor_metadata. run_actual calls thin_anchor before promote_batch_anchor; thin_anchor reads continuation/output and its 64 snapshots, with parent_row_sources from original accepted parents. New batch rows enter only the later adapter. This statement is static source context, not measured call coverage.","changed_globals_review":"Outer SCHEMA, WORKFLOW and registered self source change to v4; ROLES appends batch-parent as16th. Original retained imports, continuation root, 64-loop bound, old anchor objects and saved loop schema stay distinct from BATCH_SCHEMA v3 and current batch_anchor. New parent promotion happens after the preserved old loader returns rank1450. Root separately reviews new adapter arithmetic.","byte_identical":true,"current_run_call_coverage":"NOT_MEASURED"},
    {"side":"P","name":"thin_anchor","baseline":{"source_id":"P3","line_first":1227,"line_last":1295,"bytes":5144,"sha256":"2b2e5b425efdb999c47339888caad3c76313dcb83baaeefb9ff332b1f2aaf571"},"current":{"source_id":"P4","line_first":1863,"line_last":1931,"bytes":5144,"sha256":"2b2e5b425efdb999c47339888caad3c76313dcb83baaeefb9ff332b1f2aaf571"},"old_anchor_semantics":{"completed_steps":64,"rank":1450,"generation":8155,"original_roles_count":15},"wrapper_and_roots_review":"authenticate_acceptance supplies paths[continuation], the unchanged acceptance.anchor and its inventory to authenticate_anchor_metadata. run_actual calls thin_anchor before promote_batch_anchor; thin_anchor reads continuation/output and its 64 snapshots, with parent_row_sources from original accepted parents. New batch rows enter only the later adapter. This statement is static source context, not measured call coverage.","changed_globals_review":"Outer SCHEMA, WORKFLOW and registered self source change to v4; ROLES appends batch-parent as16th. Original retained imports, continuation root, 64-loop bound, old anchor objects and saved loop schema stay distinct from BATCH_SCHEMA v3 and current batch_anchor. New parent promotion happens after the preserved old loader returns rank1450. Root separately reviews new adapter arithmetic.","byte_identical":true,"current_run_call_coverage":"NOT_MEASURED"},
    {"side":"C","name":"anchor_metadata","baseline":{"source_id":"C3","line_first":542,"line_last":567,"bytes":2463,"sha256":"ab20e3cbf8f0b0d72a4ffdff93ea09ca71e9b50eec7b5ce3ac9a7aa22d70656e"},"current":{"source_id":"C4","line_first":594,"line_last":619,"bytes":2463,"sha256":"ab20e3cbf8f0b0d72a4ffdff93ea09ca71e9b50eec7b5ce3ac9a7aa22d70656e"},"old_anchor_semantics":{"completed_steps":64,"rank":1450,"generation":8155,"original_roles_count":15},"wrapper_and_roots_review":"AcceptedInputs.anchor_metadata still reads value[anchor] and trees[continuation]. check_actual first calls restore_physical_anchor(inputs.trees), whose state/continuation lookups remain the old anchor, then promote_batch_parent separately. ThinAnchor is also reused by that adapter with the explicit projected current header (completed_steps64, rank1578, accepted_parent_batch_rows128), saved128 rows and225 parent identities; no saved HEAD field is renamed. Static context only.","changed_globals_review":"Outer SCHEMA/source/workflow and ordered parent list move to v4/16. The old loader still checks64/1450/8155 and reads the original continuation tree; retained imports and row codec remain fixed. New batch constants identify v3 as the saved parent and the new adapter projects to ThinAnchor without overwriting completed_steps. Root separately reviews that projection and new adapter arithmetic.","byte_identical":true,"current_run_call_coverage":"NOT_MEASURED"},
    {"side":"C","name":"base_pivot_metadata","baseline":{"source_id":"C3","line_first":678,"line_last":711,"bytes":2403,"sha256":"5be807b3382c0c938dc16ac5af4906b85f507e8f16b6844004aceebccc6ec1d7"},"current":{"source_id":"C4","line_first":730,"line_last":763,"bytes":2403,"sha256":"5be807b3382c0c938dc16ac5af4906b85f507e8f16b6844004aceebccc6ec1d7"},"old_anchor_semantics":{"completed_steps":64,"rank":1450,"generation":8155,"original_roles_count":15},"wrapper_and_roots_review":"AcceptedInputs.anchor_metadata still reads value[anchor] and trees[continuation]. check_actual first calls restore_physical_anchor(inputs.trees), whose state/continuation lookups remain the old anchor, then promote_batch_parent separately. ThinAnchor is also reused by that adapter with the explicit projected current header (completed_steps64, rank1578, accepted_parent_batch_rows128), saved128 rows and225 parent identities; no saved HEAD field is renamed. Static context only.","changed_globals_review":"Outer SCHEMA/source/workflow and ordered parent list move to v4/16. The old loader still checks64/1450/8155 and reads the original continuation tree; retained imports and row codec remain fixed. New batch constants identify v3 as the saved parent and the new adapter projects to ThinAnchor without overwriting completed_steps. Root separately reviews that projection and new adapter arithmetic.","byte_identical":true,"current_run_call_coverage":"NOT_MEASURED"},
    {"side":"C","name":"ThinAnchor","baseline":{"source_id":"C3","line_first":712,"line_last":773,"bytes":3516,"sha256":"f4fe4ef5620b7a4e5256d70e15a1c3b4139827d6b6a717ec3e23a02e6ad6e1a9"},"current":{"source_id":"C4","line_first":764,"line_last":825,"bytes":3516,"sha256":"f4fe4ef5620b7a4e5256d70e15a1c3b4139827d6b6a717ec3e23a02e6ad6e1a9"},"old_anchor_semantics":{"completed_steps":64,"rank":1450,"generation":8155,"original_roles_count":15},"wrapper_and_roots_review":"AcceptedInputs.anchor_metadata still reads value[anchor] and trees[continuation]. check_actual first calls restore_physical_anchor(inputs.trees), whose state/continuation lookups remain the old anchor, then promote_batch_parent separately. ThinAnchor is also reused by that adapter with the explicit projected current header (completed_steps64, rank1578, accepted_parent_batch_rows128), saved128 rows and225 parent identities; no saved HEAD field is renamed. Static context only.","changed_globals_review":"Outer SCHEMA/source/workflow and ordered parent list move to v4/16. The old loader still checks64/1450/8155 and reads the original continuation tree; retained imports and row codec remain fixed. New batch constants identify v3 as the saved parent and the new adapter projects to ThinAnchor without overwriting completed_steps. Root separately reviews that projection and new adapter arithmetic.","byte_identical":true,"current_run_call_coverage":"NOT_MEASURED"},
    {"side":"C","name":"restore_physical_anchor","baseline":{"source_id":"C3","line_first":786,"line_last":956,"bytes":14011,"sha256":"3178867cb0c359149db73088e11bdee4b19b2e1c0acb9914ee4860044c72a231"},"current":{"source_id":"C4","line_first":838,"line_last":1008,"bytes":14011,"sha256":"3178867cb0c359149db73088e11bdee4b19b2e1c0acb9914ee4860044c72a231"},"old_anchor_semantics":{"completed_steps":64,"rank":1450,"generation":8155,"original_roles_count":15},"wrapper_and_roots_review":"AcceptedInputs.anchor_metadata still reads value[anchor] and trees[continuation]. check_actual first calls restore_physical_anchor(inputs.trees), whose state/continuation lookups remain the old anchor, then promote_batch_parent separately. ThinAnchor is also reused by that adapter with the explicit projected current header (completed_steps64, rank1578, accepted_parent_batch_rows128), saved128 rows and225 parent identities; no saved HEAD field is renamed. Static context only.","changed_globals_review":"Outer SCHEMA/source/workflow and ordered parent list move to v4/16. The old loader still checks64/1450/8155 and reads the original continuation tree; retained imports and row codec remain fixed. New batch constants identify v3 as the saved parent and the new adapter projects to ThinAnchor without overwriting completed_steps. Root separately reviews that projection and new adapter arithmetic.","byte_identical":true,"current_run_call_coverage":"NOT_MEASURED"}
  ],
  "shared_tcb": {"status":"DECLARED_SHARED_TCB","candidate":false,"cross_checked":false,"verified":false,"kernel_third_independence_claimed":false,"current_run_call_coverage":"NOT_MEASURED","kernels":[{"kernel":"vectorized_projection_chunk","side":"P","file":"search/d972_r07_actual_grade2_root_scalar_batch_v2.py","file_bytes":118315,"file_sha256":"3c93c50c43020472d616b5c253ea3c6fac6fa34d9d0e41b5a10686da30b7a856","line_first":342,"line_last":357,"region_bytes":1011,"region_sha256":"b68bbb5af24240a8758fffa0902323727e0a22838f1acdaede8e1d1c867a5199","kernel_third_independence_claimed":false,"current_run_call_coverage":"NOT_MEASURED"},{"kernel":"vectorized_projection_chunk","side":"C","file":"search/check_d972_r07_actual_grade2_root_scalar_batch_v2.py","file_bytes":119619,"file_sha256":"e0237d100c7fd3e8826ce6ab8896fa8aecf6c7e04da23a603a3d9305ea9eebb6","line_first":269,"line_last":284,"region_bytes":1020,"region_sha256":"6e785bdf5b4fb8b2010b3645462ffaff8d84e2ff2e2c134eafa0425c18b4beaf","kernel_third_independence_claimed":false,"current_run_call_coverage":"NOT_MEASURED"},{"kernel":"sparse_adjoint","side":"P","file":"search/d972_r07_targeted_grade2_owner_generated_join_v15.py","file_bytes":126565,"file_sha256":"76546bef263ad260f24632c0da46cfb913ee48759e0533d591c507d072037632","line_first":192,"line_last":203,"region_bytes":670,"region_sha256":"4b75584298a67005d5af61bd972d8dfe5069b65f1dd5d32bdeb345bf2eadbd39","kernel_third_independence_claimed":false,"current_run_call_coverage":"NOT_MEASURED"},{"kernel":"sparse_adjoint","side":"C","file":"search/check_d972_r07_targeted_grade2_owner_generated_join_v15.py","file_bytes":141770,"file_sha256":"8f718811c518f8d3e1d09de497b955d18c221e983391721068cc35be0000a662","line_first":192,"line_last":203,"region_bytes":670,"region_sha256":"4b75584298a67005d5af61bd972d8dfe5069b65f1dd5d32bdeb345bf2eadbd39","kernel_third_independence_claimed":false,"current_run_call_coverage":"NOT_MEASURED"}],"known_static_load_bearing_paths":[{"kernel":"vectorized_projection_chunk","side":"P","file":"search/d972_r07_full_origin_refinement_v1.py","line":448},{"kernel":"vectorized_projection_chunk","side":"C","file":"search/check_d972_r07_complete_oracle_cegar_continuation_v2.py","line":236}],"limits":["sparse_adjoint current-run invocation count is not measured.","The word Independent in a retained docstring does not establish independent arithmetic.","Projection sides retain different docstring/error-label bytes; sparse_adjoint regions are byte-identical."]}
}
'''
INHERITANCE_REGISTRY_PIN = {'file':'audit-region-registry.json','bytes':235914,'sha256':'36ae3dc38419bcb711499b4f0216f1d9997d10fb6d23ff96cc8e79a48efc1867'}

def require(value, why):
    if not value:
        raise ValueError('batch_workflow:' + why)

def canonical(value):
    return (json.dumps(value,ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False) + '\n').encode('ascii')

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def digest(path):
    require(path.is_file() and not path.is_symlink(),'hash-regular-file:' + str(path))
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()

def pin(path,name=None):
    value = {'bytes':path.stat().st_size,'sha256':digest(path)}
    return value if name is None else {'file':name,**value}

def strict_pairs(items):
    result = {}
    for key,value in items:
        require(key not in result,'duplicate-JSON-key:' + key)
        result[key] = value
    return result

def parse(raw):
    def nonfinite(value):
        raise ValueError('nonfinite-JSON:' + value)
    return json.loads(raw,object_pairs_hook=strict_pairs,parse_constant=nonfinite)

def read(path,canonical_only=False):
    require(path.is_file() and not path.is_symlink(),'JSON-regular-file')
    raw = path.read_bytes()
    value = parse(raw)
    if canonical_only:
        require(canonical(value) == raw,'JSON-full-canonical-bytes:' + str(path))
    return value

def seal(prefix,suffix,body):
    value = {'schema':prefix + '.' + suffix,**body}
    return {**value,'sha256':sha(canonical(value))}

def sealed(path,schema=None):
    value = read(path,True)
    require(type(value) is dict and 'schema' in value and 'sha256' in value and
        HEX.fullmatch(value['sha256']) is not None,'sealed-JSON-fields')
    if schema is not None:
        require(value['schema'] == schema,'sealed-schema:' + str(path))
    require(value['sha256'] == sha(canonical({k:v for k,v in value.items() if k != 'sha256'})),
        'sealed-inner-SHA:' + str(path))
    return value

def save(name,value):
    target = REPORT / safe_name(name)
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as stream:
        stream.write(canonical(value))
        stream.flush()
        os.fsync(stream.fileno())

def safe_name(name):
    require(type(name) is str and name and '\\' not in name and ':' not in name and
        '\x00' not in name and not any(ord(ch) < 32 for ch in name),'safe-relative-name')
    path = PurePosixPath(name)
    require(not path.is_absolute() and all(part not in ('','.','..') for part in name.split('/')) and
        path.as_posix() == name,'canonical-relative-POSIX-name')
    return name

def inventory_fields(value):
    require(type(value) is dict and set(value) == {'files','directories'} and
        type(value['files']) is list and type(value['directories']) is list,'inventory-exact-fields')
    names = []
    for entry in value['files']:
        require(type(entry) is dict and set(entry) == {'file','bytes','sha256'} and
            type(entry['bytes']) is int and entry['bytes'] >= 0 and type(entry['sha256']) is str and
            HEX.fullmatch(entry['sha256']) is not None,'inventory-file-descriptor')
        names.append(safe_name(entry['file']))
    dirs = [safe_name(name) for name in value['directories']]
    require(len(names) == len(set(names)) and len(dirs) == len(set(dirs)) and
        set(names).isdisjoint(dirs),'inventory-unique-disjoint-names')
    combined = names + dirs
    require(len({name.casefold() for name in combined}) == len(combined),'inventory-casefold-unique')
    for name in combined:
        parent = PurePosixPath(name).parent
        while str(parent) != '.':
            require(str(parent) in dirs,'inventory-all-parent-directories')
            parent = parent.parent
    return names,dirs

def validate_inventory(value,actual_files,actual_directories):
    names,dirs = inventory_fields(value)
    require(names == sorted(names) and dirs == sorted(dirs),'inventory-full-string-order')
    require({entry['file']:entry for entry in value['files']} == actual_files and
        set(dirs) == actual_directories,'inventory-full-bytes-and-directories')
    return value

def retained_inventory(value,role,observed):
    require(type(value) is dict and set(value) == {'role','files','directories'} and
        value['role'] == role,'retained-inventory-role')
    original = {'files':value['files'],'directories':value['directories']}
    inventory_fields(original)
    compared = {'files':sorted((dict(entry) for entry in original['files']),key=lambda x:x['file']),
        'directories':sorted(original['directories'])}
    inventory_fields(observed)
    return validate_inventory(compared,{entry['file']:entry for entry in observed['files']},
        set(observed['directories']))

def scan(root):
    require(root.is_dir() and not root.is_symlink(),'inventory-regular-root')
    files,dirs = [],[]
    for item in root.rglob('*'):
        require(not item.is_symlink(),'inventory-no-symlink')
        name = safe_name(item.relative_to(root).as_posix())
        if item.is_dir():
            dirs.append(name)
        else:
            require(stat.S_ISREG(item.stat().st_mode),'inventory-regular-file')
            files.append(pin(item,name))
    value = {'files':sorted(files,key=lambda x:x['file']),'directories':sorted(dirs)}
    return validate_inventory(value,{entry['file']:entry for entry in files},set(dirs))

def exact_pin(root,name,expected):
    require(pin(root / safe_name(name)) == expected,'exact-pin:' + name)

def ordinary(value,minimum=0,maximum=None):
    require(type(value) is int and value >= minimum and (maximum is None or value <= maximum),
        'ordinary-integer')
    return value

def audit_source_bytes(entry):
    # Non-executing source evidence only: no import, AST or numerical helper call.
    require(type(entry) is dict and set(entry) == {'file','bytes','sha256'},
        'audit-source-exact-file-descriptor')
    name = safe_name(entry['file'])
    ordinary(entry['bytes'],1)
    require(name.startswith('search/') and name.endswith('.py') and
        type(entry['sha256']) is str and HEX.fullmatch(entry['sha256']) is not None,
        'audit-registered-Python-source-descriptor')
    source = ROOT / name
    require(ROOT in source.resolve().parents,'audit-source-contained-in-checkout')
    for path in (source,*source.parents):
        if path == ROOT:
            break
        require(not path.is_symlink(),'audit-source-no-ancestor-link')
    require(pin(source,name) == entry,'audit-whole-checkout-source-pin')
    raw = source.read_bytes()
    require(len(raw) == entry['bytes'] and sha(raw) == entry['sha256'],
        'audit-source-full-read-stable')
    require(raw.endswith(b'\n') and b'\r' not in raw and not raw.startswith(b'\xef\xbb\xbf'),
        'audit-source-raw-LF-no-BOM')
    raw.decode('utf-8',errors='strict')
    return raw

def audit_raw_lines(raw,first,last):
    # Registered inclusive, one-based LF lines; never normalize source text.
    require(type(raw) is bytes and raw.endswith(b'\n') and b'\r' not in raw,
        'audit-range-input-LF-bytes')
    lines = raw.split(b'\n')[:-1]
    ordinary(first,1,len(lines))
    ordinary(last,first,len(lines))
    return b'\n'.join(lines[first - 1:last]) + b'\n'

def audit_registered_range(raw,first,last,expected):
    require(type(expected) is dict and set(expected) == {'bytes','sha256'},
        'audit-range-exact-raw-pin')
    ordinary(expected['bytes'],1)
    require(type(expected['sha256']) is str and HEX.fullmatch(expected['sha256']) is not None,
        'audit-range-SHA-type')
    selected = audit_raw_lines(raw,first,last)
    require({'bytes':len(selected),'sha256':sha(selected)} == expected,
        'audit-entire-registered-line-range')
    return selected

def launch():
    value = {'run':int(os.environ['GITHUB_RUN_ID']),'attempt':int(os.environ['GITHUB_RUN_ATTEMPT']),
        'head':os.environ['GITHUB_SHA'],'workflow':os.environ['WF_FILE']}
    ordinary(value['run'],1)
    ordinary(value['attempt'],1)
    require(re.fullmatch(r'[0-9a-f]{40}',value['head']) is not None and
        os.environ['GITHUB_REPOSITORY'] == REPOSITORY and os.environ['GITHUB_REF'] == 'refs/heads/' + BRANCH,
        'actual-repository-branch-launch')
    return value

def observed_runtime():
    try:
        import numpy
        version = numpy.__version__
    except ImportError:
        version = None
    return {'python':sys.version,'numpy':version}

def runtime():
    observed = observed_runtime()
    require(observed == EXPECTED_RUNTIME,'exact-accepted-runtime')
    return observed

def artifact_specs():
    table = {}
    def add(role,prefix,artifact_prefix=None):
        key = artifact_prefix or prefix
        old = prefix == 'TASK554'
        suffix = '' if old else '_ARTIFACT'
        table[role] = {'run':int(os.environ[prefix + '_RUN']),'attempt':int(os.environ[prefix + '_ATTEMPT']),
            'head':os.environ[prefix + '_HEAD'],'workflow':os.environ[prefix + '_WORKFLOW'],
            'id':int(os.environ[key + suffix + '_ID']),'name':os.environ[key + suffix + '_NAME'],
            'bytes':int(os.environ[key + ('_BYTES' if old else '_ARCHIVE_BYTES')]),
            'sha256':os.environ[key + ('_DIGEST' if old else '_ARCHIVE_DIGEST')],
            'repository_id':1312092366,'conclusion':'failure' if old else 'success'}
    for role,prefix in (('state','SEPARATOR'),('delta','DELTA'),('seed34','SEED34'),('packet','PACKET'),
            ('refinement','REFINEMENT'),('oracle','ORACLE'),('e','E'),('p1','P1'),('task712','TASK712'),
            ('continuation','CONTINUATION'),('batch-parent','BATCH_PARENT')):
        add(role,prefix)
    add('prepare','TASK554','TASK554_PREP')
    for number in range(4):
        add('block-' + str(number),'TASK554','TASK554_B' + str(number))
    require(set(table) == set(ROLES) and len({item['id'] for item in table.values()}) == 16,'sixteen-artifact-pins')
    return {role:table[role] for role in ROLES}

ARTIFACTS = artifact_specs()
PRIMARY['batch-parent'] = 'output/HEAD'

def code_contract():
    value = {'producer':{'file':os.environ['PRODUCER_FILE'],'bytes':int(os.environ['PRODUCER_BYTES']),
            'sha256':os.environ['PRODUCER_SHA256']},
        'checker':{'file':os.environ['CHECKER_FILE'],'bytes':int(os.environ['CHECKER_BYTES']),
            'sha256':os.environ['CHECKER_SHA256']},
        'producer_dependencies':copy.deepcopy(P_DEPS),'checker_dependencies':copy.deepcopy(C_DEPS),
        'data':copy.deepcopy(DATA)}
    return value

def code_union(value):
    entries = [value['producer'],value['checker'],*value['producer_dependencies'],
        *value['checker_dependencies'],*value['data']]
    require(len(entries) == 24 and len({row['file'] for row in entries}) == 24,'21-Python-plus-3-raw')
    require(len(value['producer_dependencies']) == 9 and len(value['checker_dependencies']) == 10 and
        len(value['data']) == 3,'public-closure-counts')
    return sorted(entries,key=lambda row:row['file'])

def observe_code():
    return [pin(ROOT / row['file'],row['file']) for row in code_union(code_contract())]

def capture_sources():
    observed = []
    for entry in code_union(code_contract()):
        file = ROOT / safe_name(entry['file'])
        current = pin(file,entry['file'])
        target = REPORT / 'checkout-sources' / entry['file']
        target.parent.mkdir(parents=True,exist_ok=True)
        with file.open('rb') as src,target.open('xb') as dst:
            shutil.copyfileobj(src,dst,1 << 20)
        require(pin(target,entry['file']) == current,'saved-source-exact-bytes')
        observed.append(current)
        save('acquired-code/' + str(len(observed)).zfill(2) + '.json',{
            'file':entry['file'],'expected':entry,'observed':current,'copy':str(target)})
    workflow = ROOT / os.environ['WF_FILE']
    driver = REPORT / 'driver.py'
    shutil.copyfile(workflow,REPORT / 'workflow.yml')
    save('source-before.json',{'schema':WF_SCHEMA + '.source-before','files':observed,
        'workflow':pin(workflow,os.environ['WF_FILE']),'driver':pin(driver,'driver.py'),
        'launch':launch(),'expected_code':code_contract(),**FALSE_ASSURANCE})

def source_mode():
    public_audit_registry()
    before = read(REPORT / 'source-before.json',True)
    observed = observe_code()
    workflow,driver = ROOT / os.environ['WF_FILE'],REPORT / 'driver.py'
    save('runtime-observation.json',{'schema':WF_SCHEMA + '.runtime-observation','actual':observed_runtime(),
        'expected':EXPECTED_RUNTIME,'launch':launch()})
    require(observed == before['files'] and before['workflow'] == pin(workflow,os.environ['WF_FILE']) and
        before['driver'] == pin(driver,'driver.py'),'source-capture-precedes-runtime-admission')
    require(observed == code_union(code_contract()),'all-final-source-and-raw-pins')
    require(all(HEX.fullmatch(row['sha256']) and row['bytes'] > 0 for row in observed),'final-source-pins-present')
    executable_names = [row['file'] for row in observed if row['file'].endswith('.py')]
    require(len(executable_names) == 21 and
        'search/check_d972_r07_complete_oracle_cegar_continuation_v1.py' not in executable_names,
        'actual-closure-excludes-historical-C-v1')
    for name in executable_names:
        raw = (ROOT / name).read_bytes()
        require(not raw.startswith(b'\xef\xbb\xbf') and b'\r' not in raw and raw.endswith(b'\n'),
            'Python-LF-no-BOM:' + name)
        ast.parse(raw.decode('utf-8'),filename=name)
    save('source-receipt.json',seal(WF_SCHEMA,'source-receipt',{
        'status':'PASS','code':code_contract(),'files':observed,'runtime':runtime(),
        'python_executables':21,'raw_files':3,'Python_AST_and_LF_checked':True,
        'raw_bytes_normalized':False,'historical_C_v1_executed':False,
        'driver':pin(driver,'driver.py'),'workflow':pin(workflow,os.environ['WF_FILE']),
        'source_before_sha256':digest(REPORT / 'source-before.json'),'launch':launch(),**FALSE_ASSURANCE}))

def audit_material_observation(before):
    require(type(before['nonexecuting_sources']) is list and before['nonexecuting_sources'],
        'audit-history-nonempty-source-roster')
    names = [row['file'] for row in before['nonexecuting_sources']]
    require(names == sorted(set(names)) and
        set(names).isdisjoint(row['file'] for row in code_union(code_contract())),
        'audit-history-sorted-distinct-and-outside-executable-closure')
    observed = []
    for entry in before['nonexecuting_sources']:
        audit_source_bytes(entry)
        observed.append(pin(ROOT / entry['file'],entry['file']))
    return {'nonexecuting_sources':observed,'history_copy_inventory':scan(REPORT / 'audit-history-sources'),
        'registry':pin(REPORT / 'audit-region-registry.json','audit-region-registry.json'),
        'historical_registry':pin(REPORT / 'audit-historical-region-registry.json','audit-historical-region-registry.json'),
        'receipts':{name:pin(REPORT / name,name) for name in AUDIT_RECEIPTS}}

def audit_material_bindings():
    registry = public_audit_registry()
    before = sealed(REPORT / 'audit-materials-before.json',WF_SCHEMA + '.audit-materials-before')
    require(set(before) == {'schema','sha256','status','nonexecuting_sources','history_copy_inventory',
        'registry','historical_registry','receipts','source_receipt_sha256','launch','historical_sources_executed',
        'historical_sources_added_to_mathematical_parents',*FALSE_ASSURANCE},
        'audit-materials-before-exact-fields')
    require(before['status'] == 'RECORDED_METADATA' and before['launch'] == launch() and
        before['source_receipt_sha256'] == digest(REPORT / 'source-receipt.json') and
        before['historical_sources_executed'] is False and
        before['historical_sources_added_to_mathematical_parents'] is False and
        all(before[key] is False for key in FALSE_ASSURANCE),'audit-materials-source-launch-and-scope')
    require(canonical(before['registry']) == canonical(INHERITANCE_REGISTRY_PIN) and
        (REPORT / 'audit-region-registry.json').read_bytes() == INHERITANCE_REGISTRY_RAW,
        'audit-baseline-root-admitted-registry-original-full-bytes')
    require(canonical(before['historical_registry']) == canonical(HISTORICAL_REGISTRY_PIN) and
        (REPORT / 'audit-historical-region-registry.json').read_bytes() == HISTORICAL_REGISTRY_RAW,
        'old60-full-original-registry-bytes-remain-historical')
    observed = audit_material_observation(before)
    require(canonical(observed) == canonical({key:before[key] for key in observed}),
        'all-audit-source-copy-registry-and-receipt-bytes-unchanged')
    require(observed['history_copy_inventory']['files'] == before['nonexecuting_sources'],
        'all-nonexecuting-history-full-source-copies-and-file-EOF')
    for name,(suffix,status) in AUDIT_RECEIPTS.items():
        receipt = sealed(REPORT / name,WF_SCHEMA + '.' + suffix)
        require(receipt['status'] == status and receipt['launch'] == launch() and
            receipt['source_receipt_sha256'] == before['source_receipt_sha256'] and
            canonical(receipt['registry']) == canonical(before['registry']) and
            canonical(receipt['historical_registry']) == canonical(before['historical_registry']) and
            canonical(receipt['nonexecuting_sources']) == canonical(before['nonexecuting_sources']) and
            canonical(receipt['registered_source_files']) == canonical(registry['source_files']) and
            canonical(receipt['line_contract']) == canonical(registry['line_contract']) and
            canonical(receipt['code']) == canonical(code_contract()) and
            all(receipt[key] is False for key in FALSE_ASSURANCE),
            'audit-receipt-whole-pin-source-registry-history-and-false-assurance')
    inherited = sealed(REPORT / 'arithmetic-selftest-inheritance.json')
    require(canonical(inherited['historical_arithmetic_tests']) == canonical(HISTORICAL_ARITHMETIC_TESTS) and
        canonical(inherited['registered_inheritance']) == canonical(registry['inheritance']) and
        canonical(inherited['static_source_audit']) == canonical(registry['new_source_audit']) and
        inherited['current_transition_comparison']['historical60_used_as_current_change_proof'] is False and
        canonical(inherited['current_transition_comparison']['old_loader_context']) == canonical(registry['old_loader_context']) and
        inherited['old_mathematical_suites_rerun'] == 0 and
        type(inherited['old_mathematical_suites_rerun']) is int and
        inherited['historical_payload_reacquired_in_this_run'] is False,
        'historical-mathematical-suites-reference-only')
    shared = sealed(REPORT / 'shared-tcb.json')
    require(canonical(shared['registered_kernels']) == canonical(SHARED_TCB_CONTRACT) and
        canonical(shared['registered_shared_tcb']) == canonical(registry['shared_tcb']) and
        shared['current_run_call_coverage'] == 'NOT_MEASURED' and
        shared['kernel_third_independence_claimed'] is False,'declared-shared-TCB-limits')
    return {'baseline':pin(REPORT / 'audit-materials-before.json','audit-materials-before.json'),
        'registry':before['registry'],'historical_registry':before['historical_registry'],'receipts':before['receipts'],
        'nonexecuting_sources':before['nonexecuting_sources'],
        'history_copy_inventory_sha256':sha(canonical(before['history_copy_inventory']))}

def public_audit_registry():
    raw = INHERITANCE_REGISTRY_RAW
    require(type(raw) is bytes and type(INHERITANCE_REGISTRY_PIN['bytes']) is int and
        len(raw) == INHERITANCE_REGISTRY_PIN['bytes'] and sha(raw) == INHERITANCE_REGISTRY_PIN['sha256'],
        'root-admitted-current-registry-full-raw-pin-required')
    value = parse(raw)
    require(value['schema'] == SCHEMA + '.audit-registry.v1' and type(value['task']) is int and value['task'] == 1055 and
        value['status'] == 'STATIC_WORKFLOW_AUTHOR_REGISTRY' and all(value[key] is False for key in FALSE_ASSURANCE),
        'current-registry-author-scope-not-independent-review-or-runtime')
    require(len(HISTORICAL_REGISTRY_RAW) == HISTORICAL_REGISTRY_PIN['bytes'] and
        sha(HISTORICAL_REGISTRY_RAW) == HISTORICAL_REGISTRY_PIN['sha256'] and
        canonical(value['historical_registry_pin']) == canonical(HISTORICAL_REGISTRY_PIN) and
        canonical(value['historical_registry']) == canonical(parse(HISTORICAL_REGISTRY_RAW)),
        'old60-original-registry-full-bytes-and-separate-historical-role')
    old = value['historical_registry']
    require(old['schema'] == BATCH_SCHEMA + '.audit-registry.v1' and old['task'] == 1042 and
        canonical(value['line_contract']) == canonical(old['line_contract']),
        'old60-retains-its-original-v3-schema-and-raw-LF-contract')
    require([row['id'] for row in value['source_files']] == ['P1','P2','P3','C1','C2','C3','P4','C4'],
        'six-historical-and-two-current-source-versions')
    for row in value['source_files']:
        require(set(row) == {'id','side','version','file','bytes','sha256','lf','cr','bom','final_lf','role'} and
            row['side'] == row['id'][0] and type(row['version']) is int and row['version'] == int(row['id'][1]) and
            type(row['cr']) is int and row['cr'] == 0 and row['bom'] is False and row['final_lf'] is True,
            'registry-source-descriptor-exact-version-and-EOL-types')
        ordinary(row['lf'],1)
        if row['version'] == 4:
            role = 'producer' if row['side'] == 'P' else 'checker'
            require(row['role'] == 'CURRENT_RUN_EXECUTABLE' and
                canonical({key:row[key] for key in ('file','bytes','sha256')}) == canonical(code_contract()[role]),
                'actual-current-P4-C4-complete-pins')
        else:
            prior = next(item for item in old['source_files'] if item['id'] == row['id'])
            require(row['role'] == 'HISTORICAL_TEXT_ONLY' and
                canonical({key:val for key,val in row.items() if key != 'role'}) ==
                canonical({key:val for key,val in prior.items() if key != 'role'}),
                'old-source-descriptor-bytes-with-explicit-new-history-role')
    inherited = value['inheritance']
    require(inherited['historical_source_ids'] == ['P1','P2','P3','C1','C2','C3'] and
        inherited['current_source_ids'] == ['P4','C4'] and inherited['historical_ranges_reference_only'] is True and
        inherited['current_changes_not_covered_by_old60'] is True and
        inherited['historical_sources_imported_or_executed_in_this_run'] is False and
        inherited['historical_source_files_are_additional_mathematical_parents'] is False and
        type(inherited['old_mathematical_suites_rerun']) is int and inherited['old_mathematical_suites_rerun'] == 0,
        'historical60-not-a-current-change-proof')
    expected = {'status':'STATIC_SOURCE_PINNED_RUNTIME_PENDING','upstream_completed_steps':64,
        'accepted_parent_batch_rows':128,'initial_rank':1578,'initial_generation':8283,'target_derivation_parents':225,
        'mathematical_parent_count':16,'executable_python_count':21,'raw_input_count':3,'batch_size':128,
        'max_batches':1,'refill':False,'producer_expected_rejections':SELFTEST_REJECTIONS['producer-selftest'],
        'checker_expected_rejections':SELFTEST_REJECTIONS['checker-selftest'],
        'new_selftests_executed_in_this_audit':False,'new_actual_arithmetic_executed_in_this_audit':False,
        'source_or_ast_executed_in_this_audit':False,'independent_workflow_audit_claimed':False}
    require(canonical(value['new_source_audit']) == canonical(expected),'current-source-scope-fixed-separate-from-old60')
    require(canonical(value['shared_tcb']) == canonical(old['shared_tcb']),
        'same-four-shared-kernel-descriptors-and-unmeasured-call-coverage')
    require(type(value['current_transitions']) is list and len(value['current_transitions']) == 2 and
        type(value['old_loader_context']) is list and len(value['old_loader_context']) == 8,
        'current-transitions-and-eight-loader-contexts-must-be-complete')
    return value


def compare_current_transitions(registry,raw_sources):
    observations = []
    sources = {item['id']:item for item in registry['source_files']}
    for side,transition in zip(('P','C'),registry['current_transitions'],strict=True):
        require(set(transition) == {'side','baseline_source_id','current_source_id','baseline_regions',
            'current_regions','comparisons'} and transition['side'] == side and
            transition['baseline_source_id'] == side + '3' and transition['current_source_id'] == side + '4',
            'each-current-transition-is-v3-to-v4-only')
        blocks = {}
        for key,source_id in (('baseline_regions',side + '3'),('current_regions',side + '4')):
            rows = transition[key]
            require(type(rows) is list and rows,'current-transition-nonempty-partition')
            cursor,selected = 1,[]
            for index,row in enumerate(rows):
                require(set(row) == {'ordinal','symbol','line_first','line_last','bytes','sha256'} and
                    type(row['ordinal']) is int and row['ordinal'] == index and type(row['symbol']) is str and row['symbol'] and
                    type(row['line_first']) is int and row['line_first'] == cursor and
                    type(row['line_last']) is int and row['line_last'] >= row['line_first'],
                    'current-transition-every-region-ordered-and-no-gap-overlap')
                selected.append(audit_registered_range(raw_sources[source_id],row['line_first'],row['line_last'],
                    {field:row[field] for field in ('bytes','sha256')}))
                cursor = row['line_last'] + 1
            require(cursor == sources[source_id]['lf'] + 1 and b''.join(selected) == raw_sources[source_id],
                'current-transition-complete-raw-source-EOF-including-all-new-functions')
            blocks[key] = selected
        used_old,used_new,compared = set(),set(),[]
        for item in transition['comparisons']:
            require(set(item) == {'symbol','baseline_ordinal','current_ordinal','classification','scope'} and
                type(item['symbol']) is str and item['symbol'] and type(item['scope']) is str and item['scope'],
                'current-transition-explicit-classification-and-scope')
            old_index,new_index = item['baseline_ordinal'],item['current_ordinal']
            for index,key,used in ((old_index,'baseline_regions',used_old),(new_index,'current_regions',used_new)):
                if index is not None:
                    ordinary(index,0,len(blocks[key]) - 1)
                    require(index not in used and transition[key][index]['symbol'] == item['symbol'],
                        'current-transition-each-region-classified-exactly-once')
                    used.add(index)
            require(old_index is not None or new_index is not None,'current-transition-not-an-empty-comparison')
            actual = ('ADDED_CURRENT' if old_index is None else 'REMOVED_BASELINE' if new_index is None else
                'EXACT_RAW_BYTES_UNCHANGED' if blocks['baseline_regions'][old_index] == blocks['current_regions'][new_index] else
                'REGISTERED_CHANGED_RAW_BYTES')
            require(item['classification'] == actual,'current-transition-classification-matches-actual-raw-bytes')
            compared.append(copy.deepcopy(item))
        require(used_old == set(range(len(blocks['baseline_regions']))) and used_new == set(range(len(blocks['current_regions']))),
            'current-transition-all-baseline-and-current-regions-classified')
        observations.append({'side':side,'baseline_source_id':side + '3','current_source_id':side + '4',
            'baseline_regions':len(used_old),'current_regions':len(used_new),'comparisons':compared,
            'full_EOF_no_gap_or_overlap':True,'source_executed':False})
    loaders = []
    expected_names = {'P':['authenticate_anchor_metadata','accepted_oracle_top_metadata','parent_row_sources','thin_anchor'],
        'C':['anchor_metadata','base_pivot_metadata','ThinAnchor','restore_physical_anchor']}
    for item in registry['old_loader_context']:
        require(set(item) == {'side','name','baseline','current','old_anchor_semantics','wrapper_and_roots_review',
            'changed_globals_review','byte_identical','current_run_call_coverage'} and item['side'] in expected_names and
            item['name'] in expected_names[item['side']] and item['byte_identical'] is True and
            item['current_run_call_coverage'] == 'NOT_MEASURED','registered-loader-raw-and-context-contract')
        selected = []
        for key,version in (('baseline',3),('current',4)):
            row = item[key]
            require(set(row) == {'source_id','line_first','line_last','bytes','sha256'} and
                row['source_id'] == item['side'] + str(version),'loader-exact-source-region-identity')
            selected.append(audit_registered_range(raw_sources[row['source_id']],row['line_first'],row['line_last'],
                {field:row[field] for field in ('bytes','sha256')}))
        require(selected[0] == selected[1] and canonical(item['old_anchor_semantics']) == canonical({
            'completed_steps':64,'rank':1450,'generation':8155,'original_roles_count':15}) and
            type(item['wrapper_and_roots_review']) is str and item['wrapper_and_roots_review'] and
            type(item['changed_globals_review']) is str and item['changed_globals_review'],
            'old-loader-raw-unchanged-and-registered-old-anchor-context-not-just-bytes')
        loaders.append(copy.deepcopy(item))
    require([(item['side'],item['name']) for item in loaders] == [(side,name) for side in ('P','C') for name in expected_names[side]],
        'all-eight-public-loader-contexts-in-order')
    return {'transitions':observations,'old_loader_context':loaders,
        'historical60_used_as_current_change_proof':False,'current_run_call_coverage':'NOT_MEASURED'}

def capture_audit_source_versions(registry):
    raw_sources,history = {},[]
    for row in registry['source_files']:
        entry = {key:row[key] for key in ('file','bytes','sha256')}
        raw = audit_source_bytes(entry)
        require(raw.count(b'\n') == row['lf'],'registered-source-full-line-EOF')
        raw_sources[row['id']] = raw
        if row['role'] == 'HISTORICAL_TEXT_ONLY':
            target = REPORT / 'audit-history-sources' / entry['file']
            target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            require(pin(target,entry['file']) == entry,'nonexecuting-history-copy-all-bytes')
            history.append(entry)
            save('acquired-audit-history/' + row['id'] + '.json',{
                'source_id':row['id'],'source':entry,'copy':str(target),
                'imported_or_executed':False,**FALSE_ASSURANCE})
    require(len(history) == 6 and len(raw_sources) == 8,'six-historical-and-two-current-batch-sources')
    return raw_sources,sorted(history,key=lambda row:row['file'])

def compare_audit_regions(registry,raw_sources):
    inherited = registry['inheritance']
    groups = [('unchanged_regions',9),('literal_exclusions',2),('reviewed_change_regions',9)]
    coverage = {key:[] for key in raw_sources}
    observations,seen_ids,descriptors = {},set(),0
    for category,count in groups:
        entries = inherited[category]
        require(type(entries) is list and len(entries) == count,'registered-region-category-count')
        observations[category] = []
        for region in entries:
            require(region['id'] not in seen_ids and len(region['versions']) == 3,'unique-region-and-three-versions')
            seen_ids.add(region['id'])
            side = region['versions'][0]['source_id'][0]
            require([row['source_id'] for row in region['versions']] == [side + str(n) for n in (1,2,3)],
                'each-registered-region-all-same-side-versions')
            compared = []
            for row in region['versions']:
                wanted_keys = {'source_id','line_first','line_last','bytes','sha256'}
                if category == 'literal_exclusions':
                    wanted_keys.add('raw_utf8')
                require(set(row) == wanted_keys,'registered-region-descriptor-exact-type')
                raw = audit_registered_range(raw_sources[row['source_id']],row['line_first'],row['line_last'],
                    {key:row[key] for key in ('bytes','sha256')})
                coverage[row['source_id']].append((row['line_first'],row['line_last'],category,region['id']))
                compared.append(raw)
                descriptors += 1
                if category == 'literal_exclusions':
                    require(region['removed_by_normalization'] is False and row['line_first'] == row['line_last'] and
                        type(row['raw_utf8']) is str and raw == row['raw_utf8'].encode('utf-8'),
                        'exact-excluded-literal-bytes-retained-not-normalized')
            if category == 'unchanged_regions':
                require(region['comparison'] == 'EXACT_RAW_BYTES_ALL_THREE_VERSIONS' and region['normalization'] == 'NONE' and
                    compared[0] == compared[1] == compared[2],'all-three-versions-direct-raw-byte-equality')
                result = 'EXACT_RAW_BYTES_ALL_THREE_VERSIONS_CONFIRMED'
            elif category == 'reviewed_change_regions':
                require(region['disposition'] == 'STATICALLY_REVIEWED_CHANGE_NOT_ALL_THREE_BYTE_IDENTITY',
                    'changed-regions-excluded-from-byte-inheritance-claim')
                result = 'REGISTERED_CHANGED_RAW_RANGES_MATCH'
            else:
                result = 'REGISTERED_LITERAL_RAW_RANGES_MATCH'
            observations[category].append({'id':region['id'],'status':result,
                'versions':copy.deepcopy(region['versions'])})
    require(descriptors == 60,'all-sixty-batch-source-region-descriptors')
    partitions = []
    for source in registry['source_files']:
        cursor = 1
        rows = sorted(coverage[source['id']])
        for first,last,category,region in rows:
            require(first == cursor,'registered-whole-source-no-gap-or-overlap')
            cursor = last + 1
        require(cursor == source['lf'] + 1,'registered-whole-source-partition-EOF')
        partitions.append({'source_id':source['id'],'line_count':source['lf'],
            'registered_ranges':len(rows),'no_gap_or_overlap':True,'complete_source_EOF':True})
    return {'range_descriptors_compared':descriptors,'unchanged_regions_compared':9,
        'literal_exclusions_compared':2,'reviewed_change_regions_compared':9,
        'normalization_performed':False,'all_C_body_identity_claimed':False,
        'observations':observations,'source_partitions':partitions}

def compare_audit_shared_kernels(registry):
    entries,raw_by_kernel = [],{}
    code = {row['file']:row for row in code_union(code_contract())}
    for row in registry['shared_tcb']['kernels']:
        source = {'file':row['file'],'bytes':row['file_bytes'],'sha256':row['file_sha256']}
        require(canonical(source) == canonical(code.get(source['file'])),'shared-kernel-is-in-retained-executable-closure')
        raw = audit_source_bytes(source)
        selected = audit_registered_range(raw,row['line_first'],row['line_last'],
            {'bytes':row['region_bytes'],'sha256':row['region_sha256']})
        require(row['kernel_third_independence_claimed'] is False and row['current_run_call_coverage'] == 'NOT_MEASURED',
            'individual-shared-kernel-measurement-limit')
        raw_by_kernel[(row['kernel'],row['side'])] = selected
        entries.append({'kernel':row['kernel'],'side':row['side'],'source':source,
            'line_first':row['line_first'],'line_last':row['line_last'],
            'region_bytes':len(selected),'region_sha256':sha(selected),'status':'REGISTERED_RAW_RANGE_MATCH'})
    require(len(entries) == 4 and raw_by_kernel[('sparse_adjoint','P')] == raw_by_kernel[('sparse_adjoint','C')],
        'four-kernels-and-declared-identical-sparse-adjoint-bytes')
    return {'ranges_compared':4,'kernels':entries,'source_execution_for_range_comparison':False,
        'current_run_call_coverage':'NOT_MEASURED','kernel_third_independence_claimed':False}

def audit_mode():
    registry = public_audit_registry()
    source = sealed(REPORT / 'source-receipt.json',WF_SCHEMA + '.source-receipt')
    require(source['status'] == 'PASS' and source['code'] == code_contract(),'admitted-source-before-static-audit')
    with (REPORT / 'audit-region-registry.json').open('xb') as stream:
        stream.write(INHERITANCE_REGISTRY_RAW)
        stream.flush()
        os.fsync(stream.fileno())
    require(pin(REPORT / 'audit-region-registry.json','audit-region-registry.json') == INHERITANCE_REGISTRY_PIN,
        'whole-public-registry-original-bytes-preserved')
    with (REPORT / 'audit-historical-region-registry.json').open('xb') as stream:
        stream.write(HISTORICAL_REGISTRY_RAW)
        stream.flush()
        os.fsync(stream.fileno())
    raw_sources,history = capture_audit_source_versions(registry)
    inherited_comparison = compare_audit_regions(registry['historical_registry'],
        {key:raw for key,raw in raw_sources.items() if not key.endswith('4')})
    current_comparison = compare_current_transitions(registry,raw_sources)
    shared_comparison = compare_audit_shared_kernels(registry)
    common = {'registry':INHERITANCE_REGISTRY_PIN,'historical_registry':HISTORICAL_REGISTRY_PIN,'source_receipt_sha256':digest(REPORT / 'source-receipt.json'),
        'nonexecuting_sources':history,'launch':launch(),'code':code_contract(),
        'registered_source_files':copy.deepcopy(registry['source_files']),
        'line_contract':copy.deepcopy(registry['line_contract']),**FALSE_ASSURANCE}
    save('arithmetic-selftest-inheritance.json',seal(WF_SCHEMA,'arithmetic-selftest-inheritance',{
        **common,'status':'STATIC_INHERITANCE_REFERENCE','historical_arithmetic_tests':HISTORICAL_ARITHMETIC_TESTS,
        'arithmetic_selftest_inherited_from':HISTORICAL_ARITHMETIC_TESTS['arithmetic_selftest_inherited_from'],
        'old_mathematical_suites_rerun':0,'historical_payload_reacquired_in_this_run':False,
        'historical_sources_imported_or_executed_in_this_run':False,
        'historical_sources_are_additional_mathematical_parents':False,
        'registered_inheritance':copy.deepcopy(registry['inheritance']),
        'static_source_audit':copy.deepcopy(registry['new_source_audit']),
        'historical_raw_region_comparison':inherited_comparison,'current_transition_comparison':current_comparison}))
    save('shared-tcb.json',seal(WF_SCHEMA,'shared-tcb',{
        **common,'status':'DECLARED_SHARED_TCB','registered_kernels':SHARED_TCB_CONTRACT,
        'registered_shared_tcb':copy.deepcopy(registry['shared_tcb']),
        'raw_range_comparison':shared_comparison,'current_run_call_coverage':'NOT_MEASURED',
        'kernel_third_independence_claimed':False}))
    body = {'nonexecuting_sources':history}
    observed = audit_material_observation(body)
    save('audit-materials-before.json',seal(WF_SCHEMA,'audit-materials-before',{
        'status':'RECORDED_METADATA',**observed,'source_receipt_sha256':common['source_receipt_sha256'],
        'launch':launch(),'historical_sources_executed':False,
        'historical_sources_added_to_mathematical_parents':False,**FALSE_ASSURANCE}))
    audit_material_bindings()

def safe_extract(archive,destination,remaining_bytes=32 * (1 << 30)):
    require(not destination.exists(),'new-extraction-root')
    destination.mkdir()
    entry_limit,byte_limit = 1000000,min(32 * (1 << 30),ordinary(remaining_bytes))
    with zipfile.ZipFile(archive) as bundle:
        infos = bundle.infolist()
        require(0 < len(infos) <= entry_limit,'ZIP-entry-count-bound')
        declared = sum(ordinary(info.file_size) for info in infos)
        require(declared <= byte_limit,'ZIP-expanded-size-bound')
        seen,nodes = set(),{}
        def register(name,directory):
            folded = name.casefold()
            if folded in nodes:
                prior_name,prior_dir = nodes[folded]
                require(prior_name == name and prior_dir and directory,'ZIP-casefold-or-node-collision')
            else:
                nodes[folded] = (name,directory)
        for info in infos:
            raw_name = info.filename
            name = raw_name[:-1] if info.is_dir() else raw_name
            safe_name(name)
            require(info.orig_filename == raw_name and name not in seen and
                raw_name == name + ('/' if info.is_dir() else ''),'ZIP-exact-name-and-duplicate')
            seen.add(name)
            mode = (info.external_attr >> 16) & 0xffff
            kind = stat.S_IFMT(mode)
            require(kind in (0,stat.S_IFREG,stat.S_IFDIR) and not info.flag_bits & 1,
                'ZIP-no-symlink-special-encrypted-entry')
            require((not info.is_dir() or kind in (0,stat.S_IFDIR)) and
                not (kind == stat.S_IFDIR and not info.is_dir()),'ZIP-exact-directory-type')
            if info.is_dir():
                require(info.file_size == 0,'ZIP-empty-directory-payload')
            register(name,info.is_dir())
            parent = PurePosixPath(name).parent
            while str(parent) != '.':
                register(str(parent),True)
                parent = parent.parent
        actual_total = 0
        for info in infos:
            name = info.filename[:-1] if info.is_dir() else info.filename
            target = destination.joinpath(*PurePosixPath(name).parts)
            require(destination.resolve() in target.resolve().parents,'ZIP-contained-destination')
            if info.is_dir():
                target.mkdir(parents=True,exist_ok=True)
                continue
            target.parent.mkdir(parents=True,exist_ok=True)
            written = 0
            with bundle.open(info) as src,target.open('xb') as dst:
                while True:
                    raw = src.read(1 << 20)
                    if not raw:
                        break
                    written += len(raw)
                    actual_total += len(raw)
                    require(written <= info.file_size and actual_total <= byte_limit,'ZIP-stream-size-bound')
                    dst.write(raw)
            require(written == info.file_size == target.stat().st_size,'ZIP-complete-CRC-and-EOF')
        require(actual_total == declared,'ZIP-full-expanded-EOF')
    return {'entries':len(infos),'expanded_bytes':actual_total,'entry_limit':entry_limit,
        'expanded_byte_limit':byte_limit,'full_EOF':True,'duplicate_and_casefold_checked':True}

BATCH_SCHEMA = 'd972.r07.fixed-lambda-cycle-batch.v3'
BATCH_WF_SCHEMA = BATCH_SCHEMA + '.workflow-v3'
BATCH_TRANSPORT_PINS = {
    'run-receipt.json':(39614,'e8edc336d16cc4a030b4726aea992f3e1e1633af11635911bdb9dc0cbc1839ca'),
    'envelope-inventory-before-run.json':(2091680,'588d2ff5a799519ea3e1479da0bc314054eaf197a83d8144d5b9aded2e8fa1e6'),
    'selftest-fixtures-archive-receipt.json':(1806,'fd1946101bd6b98d93d23c77fc49f538a35b60a906140762b5b8a28426ca1f8f'),
    'selftest-fixtures-inventory.json':(880738,'d174c1157639794baa4ca8ad69118225418dea79daaf11af1f59392b362d3cf7'),
    'selftest-fixtures-archive-readback.json':(880738,'d174c1157639794baa4ca8ad69118225418dea79daaf11af1f59392b362d3cf7'),
    'selftest-fixtures-after-archive.json':(880738,'d174c1157639794baa4ca8ad69118225418dea79daaf11af1f59392b362d3cf7'),
    'selftest-fixtures.zip':(4278300,'3cafe814400a8000310822f87e8f9ef320503b5caf31e9f34c7c479f92ad974f'),
    'intake-controls-before.json':(1034304,'c9beef2a481ed34406b825079d1e09063dab084f4b8c8e4411fce2513bdbc81a')}
BATCH_NONFIXTURE_EMPTY = ['ZIP-casefold-extracted','ZIP-duplicate-extracted',
    'ZIP-traversal-extracted','metadata-fixture/empty']
BATCH_ABSENT_DIRECTORIES = sorted(BATCH_NONFIXTURE_EMPTY + [name for host in range(2)
    for name in ['selftest-fixtures/P/registration/host-' + str(host) + '/parents',
        *['selftest-fixtures/P/registration/host-' + str(host) + '/parents/' + role for role in ROLES[:-1]]]])
BATCH_FIELDS = {
    'head':'output/HEAD','result':'output/result.json','checker':'checker-result.json',
    'owner':'output/owner.json','source':'output/source.json','start':'output/start.json',
    'parent_layout':'output/parent-layout.json','fixed':'output/fixed/manifest.json',
    'selection_start':'output/selection/start.json','selection':'output/selection/selection.json',
    'final_manifest':'output/final/manifest.json','separator':'output/final/separator.json',
    'target':'output/final/target-remainder.bin','lambda':'output/final/lambda.bin',
    'progress_head':'output/progress/HEAD','run_receipt':'run-receipt.json','source_receipt':'source-receipt.json'}
BATCH_STATE = {'upstream_completed_steps':64,'accepted_parent_batch_rows':128,
    'processed_parent_candidates':128,'dependent_parent_candidates':0,'rank':1578,'generation':8283,
    'kind':'Separator','terminal':'BATCH_COMPLETE_CANDIDATE','target_derivation_parents':225,
    'state_head':'e793896e585bd0e540e25770359e8d36d1a84d69c012d88615e5ecffc02dfba9',
    'target_remainder_sha256':'7868b7806a0dc41c2bda8a1c4c6a10d1cfa2c2e6968aadf561e93820f12053e1',
    'lambda_sha256':'6a0fe9368f2ec7f28c4d8076e7d3184fb57322b9d0905a8e7c3c26b467bcee4e',
    'old_oracle':{'failed_count':36274,'first_failed_index':70,'first_failed_edge':125}}


def batch_transport_pins(root):
    entries = {}
    for name,(length,checksum) in BATCH_TRANSPORT_PINS.items():
        exact_pin(root,name,{'bytes':length,'sha256':checksum})
        entries[name] = {'file':name,'bytes':length,'sha256':checksum}
    return entries


def batch_envelope_inventory(root):
    for name in ('run-receipt.json','envelope-inventory-before-run.json'):
        length,checksum = BATCH_TRANSPORT_PINS[name]
        exact_pin(root,name,{'bytes':length,'sha256':checksum})
    run = sealed(root / 'run-receipt.json',BATCH_WF_SCHEMA + '.run-receipt')
    require(type(run['status']) is str and run['status'] == 'PASS','batch-parent-successful-envelope')
    spec = ARTIFACTS['batch-parent']
    require(canonical(run['launch']) == canonical({'run':spec['run'],'attempt':spec['attempt'],
        'head':spec['head'],'workflow':spec['workflow']}),'batch-parent-original-v3-launch')
    before = read(root / 'envelope-inventory-before-run.json',True)
    names,dirs = inventory_fields(before)
    require(names == sorted(names) and dirs == sorted(dirs) and len(names) == 11435 and len(dirs) == 3475,
        'batch-parent-original-complete-inventory-counts')
    excludes = ['envelope-inventory-before-run.json','run-receipt.json']
    require(canonical(run['envelope_payload_before_this_receipt']) == canonical({
        'bytes':1265467844,'directories':3475,'files':11435,'excludes':excludes,
        'inventory':{'file':excludes[0],'bytes':BATCH_TRANSPORT_PINS[excludes[0]][0],
            'sha256':BATCH_TRANSPORT_PINS[excludes[0]][1]}}),'batch-parent-envelope-self-exclusion')
    require(sum(entry['bytes'] for entry in before['files']) == 1265467844 and
        set(excludes).isdisjoint(names),'batch-parent-original-payload-bytes')
    files = copy.deepcopy(before['files'])
    files.extend({'file':name,'bytes':BATCH_TRANSPORT_PINS[name][0],
        'sha256':BATCH_TRANSPORT_PINS[name][1]} for name in excludes)
    files.sort(key=lambda item:item['file'])
    value = {'files':files,'directories':dirs}
    validate_inventory(value,{entry['file']:entry for entry in files},set(dirs))
    require(len(files) == 11437 and sum(item['bytes'] for item in files) == 1267599138,
        'batch-parent-full-original-file-count-and-bytes')
    return value,run


def batch_inner_zip_read(root,inventory):
    names,dirs = inventory_fields(inventory)
    require(names == sorted(names) and dirs == sorted(dirs) and len(names) == 4600 and len(dirs) == 2281,
        'batch-parent-inner-fixture-roster')
    files = {entry['file']:entry for entry in inventory['files']}
    expected_dirs,seen_files,seen_dirs,folded = set(dirs),set(),set(),set()
    total = 0
    with zipfile.ZipFile(root / 'selftest-fixtures.zip') as archive:
        infos = archive.infolist()
        require(len(infos) == 6881,'batch-parent-inner-all-entry-count')
        for info in infos:
            directory = info.is_dir()
            name = safe_name(info.filename[:-1] if directory else info.filename)
            require(info.orig_filename == info.filename and name.split('/')[0] in ('P','C') and
                info.filename == name + ('/' if directory else '') and name.casefold() not in folded and
                not info.flag_bits & 1,'batch-parent-inner-name-owner-and-unique')
            folded.add(name.casefold())
            kind = stat.S_IFMT((info.external_attr >> 16) & 0xffff)
            require(kind == (stat.S_IFDIR if directory else stat.S_IFREG),'batch-parent-inner-exact-entry-type')
            require((directory and name in expected_dirs and info.file_size == 0) or
                (not directory and name in files and info.file_size == files[name]['bytes']),
                'batch-parent-inner-registered-entry-and-size')
            checksum,size = hashlib.sha256(),0
            with archive.open(info) as stream:
                while True:
                    block = stream.read(1 << 20)
                    if not block:
                        break
                    size += len(block)
                    require(size <= info.file_size,'batch-parent-inner-stream-size-bound')
                    checksum.update(block)
            require(size == info.file_size,'batch-parent-inner-full-EOF-and-CRC')
            if directory:
                seen_dirs.add(name)
            else:
                require(checksum.hexdigest() == files[name]['sha256'],'batch-parent-inner-whole-file-SHA')
                seen_files.add(name)
                total += size
    require(seen_files == set(files) and seen_dirs == expected_dirs,'batch-parent-inner-exact-all-files-directories')
    return {'entries':6881,'files':len(files),'directories':len(dirs),'bytes':total,
        'every_entry_full_EOF_CRC_and_SHA':True,'ignored_entries':[]}


def restore_batch_parent_directories(root,extraction):
    # Authenticate every existing byte and every registered missing directory before the first mkdir.
    begun = time.monotonic()
    pins = batch_transport_pins(root)
    wanted,run = batch_envelope_inventory(root)
    before = scan(root)
    require(canonical(before['files']) == canonical(wanted['files']),
        'batch-parent-all-11437-files-authenticated-before-directory-restoration')
    ancestors = set()
    for entry in wanted['files']:
        parent = PurePosixPath(entry['file']).parent
        while str(parent) != '.':
            ancestors.add(str(parent))
            parent = parent.parent
    require(type(extraction['entries']) is int and extraction['entries'] == 11437 and
        extraction['expanded_bytes'] == 1267599138 and extraction['full_EOF'] is True and
        len(ancestors) == 3439 and set(before['directories']) == ancestors,
        'batch-parent-original-file-only-ZIP-and-3439-implicit-directories')
    missing = sorted(set(wanted['directories']) - ancestors)
    require(ancestors <= set(wanted['directories']) and missing == BATCH_ABSENT_DIRECTORIES and len(missing) == 36,
        'batch-parent-only-36-registered-missing-directories')
    controls = read(root / 'intake-controls-before.json',True)
    inventory_fields(controls)
    require(set(missing) <= set(controls['directories']),'batch-parent-all-missing-directories-in-original-pre-P-controls')
    inventory = read(root / 'selftest-fixtures-inventory.json',True)
    projected = {'files':[dict(item,file=item['file'][18:]) for item in wanted['files']
        if item['file'].startswith('selftest-fixtures/')],
        'directories':[name[18:] for name in wanted['directories'] if name.startswith('selftest-fixtures/')]}
    require(canonical(projected) == canonical(inventory) and
        (root / 'selftest-fixtures-inventory.json').read_bytes() ==
        (root / 'selftest-fixtures-archive-readback.json').read_bytes() ==
        (root / 'selftest-fixtures-after-archive.json').read_bytes(),'batch-parent-three-inner-inventories-and-envelope-projection')
    archived = sealed(root / 'selftest-fixtures-archive-receipt.json',BATCH_WF_SCHEMA + '.selftest-fixture-archive')
    require(type(archived['status']) is str and archived['status'] == 'PASS' and archived['reason'] is None and
        archived['excluded_entries'] == [] and all(archived[key] is True for key in (
            'all_entries_and_explicit_directories_read','all_file_bytes_SHA_EOF_and_CRC_read',
            'both_completed_roots_unchanged','container_present','raw_fixtures_retained')) and
        all(archived[key] is False for key in ('archive_contains_itself','partial_or_missing_roots_claimed_complete',
            'silently_filtered_entries',*FALSE_ASSURANCE)),'batch-parent-actual-complete-fixture-archive')
    for key,name in (('inventory','selftest-fixtures-inventory.json'),
            ('readback_inventory','selftest-fixtures-archive-readback.json'),
            ('after_inventory','selftest-fixtures-after-archive.json'),('archive','selftest-fixtures.zip')):
        require(canonical(archived[key]) == canonical(pins[name]) and
            canonical(run['selftest_fixture_archive_files'][name]) == canonical(pins[name]),
            'batch-parent-archive-run-exact-file-pin:' + key)
    inner = batch_inner_zip_read(root,inventory)
    plan = sorted(missing,key=lambda name:(len(PurePosixPath(name).parts),name))
    planned,base = set(),root.resolve()
    for name in plan:
        target = root / safe_name(name)
        require(base in target.resolve().parents and not target.exists() and not target.is_symlink(),
            'batch-parent-new-directory-contained-and-absent')
        parent = target.parent
        relative_parent = parent.relative_to(root).as_posix()
        require((parent.is_dir() and not parent.is_symlink()) or relative_parent in planned,
            'batch-parent-all-directory-parents-planned-first')
        planned.add(name)
    save('batch-parent-restoration-plan.json',seal(WF_SCHEMA,'batch-parent-restoration-plan',{
        'artifact':ARTIFACTS['batch-parent'],'root':str(base),'source_pins':pins,'original_files':11437,
        'original_directories':3439,'expected_directories':3475,'missing':plan,'inner_zip':inner,
        'all_file_bytes_authenticated_before_first_mkdir':True,'only_registered_missing_directories':True,
        'old_numerical_replays':0,**FALSE_ASSURANCE}))
    created = []
    try:
        for ordinal,name in enumerate(plan):
            target = root / name
            require(target.parent.is_dir() and not target.parent.is_symlink() and not target.exists() and
                not target.is_symlink(),'batch-parent-directory-create-boundary')
            returned = os.mkdir(target)
            require(returned is None and target.is_dir() and not target.is_symlink() and
                target.resolve() == base.joinpath(*PurePosixPath(name).parts),
                'batch-parent-directory-return-and-immediate-exists')
            row = {'ordinal':ordinal,'relative':name,'resolved_path':str(target.resolve()),
                'mkdir_return':None,'immediate_exists':True,'regular_directory':True}
            created.append(row)
            save('batch-parent-restoration/' + str(ordinal).zfill(2) + '.json',row)
        after = scan(root)
        require(canonical(after) == canonical(wanted),'batch-parent-full-reread-after-directory-restoration')
        require(canonical(scan(root / 'selftest-fixtures')) == canonical(inventory),
            'batch-parent-full-fixture-reread-after-directory-restoration')
        status,reason = 'PASS',None
    except BaseException as exc:
        status,reason = 'FAIL',type(exc).__name__ + ':' + str(exc)
        raise
    finally:
        save('batch-parent-restoration-result.json',seal(WF_SCHEMA,'batch-parent-restoration-result',{
            'status':status,'reason':reason,'plan':pin(REPORT / 'batch-parent-restoration-plan.json',
                'batch-parent-restoration-plan.json'),'created':created,'created_count':len(created),
            'all_expected_files_and_directories_reread':status == 'PASS','elapsed_seconds':time.monotonic() - begun,
            'mathematical_replays':0,**FALSE_ASSURANCE}))
    return pin(REPORT / 'batch-parent-restoration-result.json','batch-parent-restoration-result.json')


def batch_registered_descriptor(root,name,expected_files):
    name = safe_name(name)
    require(name in expected_files,'batch-parent-registered-file:' + name)
    expected = expected_files[name]
    require(canonical(pin(root / name,name)) == canonical(expected),'batch-parent-actual-file-pin:' + name)
    return copy.deepcopy(expected)


def batch_saved_manifest(folder,suffix):
    value = sealed(folder / 'manifest.json',BATCH_SCHEMA + '.' + suffix)
    require(value.get('eof',True) is True and type(value['files']) is list,'batch-parent-manifest-full-EOF')
    names = []
    for entry in value['files']:
        require(type(entry) is dict and set(entry) in ({'file','bytes','sha256'},
            {'file','bytes','sha256','dtype','shape'}),'batch-parent-manifest-descriptor-shape')
        name = safe_name(entry['file'])
        require('/' not in name and type(entry['bytes']) is int and entry['bytes'] >= 0 and
            type(entry['sha256']) is str and HEX.fullmatch(entry['sha256']) is not None,
            'batch-parent-manifest-descriptor-types')
        require(canonical(pin(folder / name,name)) == canonical({key:entry[key]
            for key in ('file','bytes','sha256')}),'batch-parent-full-manifest-payload-hash')
        names.append(name)
    require(names == sorted(set(names)) and {p.name for p in folder.iterdir()} == {*names,'manifest.json'},
        'batch-parent-manifest-full-directory-EOF')
    return value


def batch_fixture_history(root,run):
    archive = sealed(root / 'selftest-fixtures-archive-receipt.json',BATCH_WF_SCHEMA + '.selftest-fixture-archive')
    require(canonical(run['selftest_fixture_archive_receipt']) ==
        canonical(pin(root / 'selftest-fixtures-archive-receipt.json','selftest-fixtures-archive-receipt.json')),
        'batch-parent-run-archive-receipt-join')
    summaries = []
    for stage in ('before-producer','before-checker','after-checker'):
        descriptor = run['selftest_fixture_comparisons'][stage]
        payload_descriptor(root,descriptor)
        comparison = sealed(root / descriptor['file'],BATCH_WF_SCHEMA + '.selftest-fixture-comparison')
        require(type(comparison['stage']) is str and comparison['stage'] == stage and
            comparison['status'] == 'PASS' and comparison['errors'] == comparison['missing'] == [] and
            [row['label'] for row in comparison['fixtures']] == ['producer-selftest','checker-selftest'],
            'batch-parent-historical-complete-fixture-comparison')
        if stage == 'after-checker':
            require(canonical(archive['comparison']) == canonical(descriptor),'batch-parent-archive-last-comparison')
        for row in comparison['fixtures']:
            label = row['label']
            require(row['present'] is True and row['unchanged'] is True and row['state'] == 'COMPLETE' and
                row['reason'] is None and row['root'] == run['selftest_fixture_roots'][label],
                'batch-parent-historical-both-complete-roots')
            for key in ('baseline','inventory'):
                payload_descriptor(root,row[key])
            baseline = sealed(root / row['baseline']['file'],BATCH_WF_SCHEMA + '.selftest-fixture-baseline')
            inventory = read(root / row['inventory']['file'],True)
            require(baseline['status'] == 'PASS' and baseline['label'] == label and baseline['root'] == row['root'] and
                canonical(baseline['inventory']) == canonical(inventory),
                'batch-parent-historical-exact-baseline-inventory')
            actual = scan(root / 'selftest-fixtures' / ('P' if label == 'producer-selftest' else 'C'))
            require(canonical(actual) == canonical(inventory),'batch-parent-restored-complete-fixture-subtree')
            for key in ('execution','selftest'):
                payload_descriptor(root,baseline[key])
            execution = sealed(root / baseline['execution']['file'],BATCH_WF_SCHEMA + '.execution-result')
            test = sealed(root / baseline['selftest']['file'],BATCH_SCHEMA + '.selftest')
            require(execution['label'] == label and type(execution['exit_code']) is int and execution['exit_code'] == 0 and
                execution['outer_terminated'] is False and test['status'] == 'PASS',
                'batch-parent-actual-historical-selftest-receipts-without-rerun')
        summaries.append({'stage':stage,'receipt':descriptor,'both_complete_roots_unchanged':True})
    return summaries


def authenticate_batch_parent(paths,inventories,anchor,code):
    root = paths['batch-parent']
    registered,run = batch_envelope_inventory(root)
    require(canonical(inventories['batch-parent']) == canonical(registered),
        'batch-parent-whole-restored-registered-inventory')
    require(sha(canonical(registered['files'])) == '115c912a735b18f483bf85cdfe5fce5cb591b87816f12529e25be18117ba4598' and
        sha(canonical(registered['directories'])) == 'b34abb0e22435e2328b6f9b892f8a652aab6f50d640644e1ed09c0f1852072f2',
        'batch-parent-public-whole-inventory-list-hashes')
    expected = {item['file']:item for item in registered['files']}
    descriptors = {key:batch_registered_descriptor(root,name,expected) for key,name in BATCH_FIELDS.items()}
    layout = sealed(root / BATCH_FIELDS['parent_layout'],BATCH_SCHEMA + '.parent-layout')
    old_parents = [{'role':role,'artifact':ARTIFACTS[role],**inventories[role]} for role in ROLES[:-1]]
    require(canonical(layout['parents']) == canonical(old_parents) and canonical(layout['anchor']) == canonical(anchor) and
        canonical(layout['runtime']) == canonical(runtime()) and canonical(layout['registration']) == canonical(REGISTRATION),
        'batch-parent-original-fifteen-parents-old64-anchor-and-runtime')
    for key in ('producer_dependencies','checker_dependencies','data'):
        require(canonical(layout['code'][key]) == canonical(code[key]),'batch-parent-retained-code-list:' + key)
    original_code = layout['code']
    require(canonical(original_code['producer']) == canonical({'file':'search/d972_r07_fixed_lambda_cycle_batch_v3.py',
        'bytes':209926,'sha256':'a286dca4a2d94273d2496e16317579be06173e0e4802471b2840dc4263e5a3e8'}) and
        canonical(original_code['checker']) == canonical({'file':'search/check_d972_r07_fixed_lambda_cycle_batch_v3.py',
        'bytes':178914,'sha256':'1aebf6e47807466ec56426a55e34d0c7f622a5896c40184540e4d153060946d7'}),
        'batch-parent-original-P3-C3-not-renamed-to-current')
    receipt = sealed(root / 'source-receipt.json',BATCH_WF_SCHEMA + '.source-receipt')
    require(receipt['status'] == 'PASS' and canonical(receipt['code']) == canonical(original_code) and
        canonical(receipt['runtime']) == canonical(runtime()) and canonical(receipt['launch']) == canonical(run['launch']),
        'batch-parent-original-source-receipt-code-runtime-launch')
    for entry in receipt['files']:
        exact_pin(root,'checkout-sources/' + safe_name(entry['file']),{key:entry[key] for key in ('bytes','sha256')})
    require(len(receipt['files']) == 24 and canonical(receipt['files']) == canonical(code_union(original_code)),
        'batch-parent-all24-original-source-and-raw-bytes')
    head = sealed(root / BATCH_FIELDS['head'],BATCH_SCHEMA + '.head')
    result = sealed(root / BATCH_FIELDS['result'],BATCH_SCHEMA + '.result')
    checked = sealed(root / BATCH_FIELDS['checker'],BATCH_SCHEMA + '.checker-result')
    start = sealed(root / BATCH_FIELDS['start'],BATCH_SCHEMA + '.start')
    final = batch_saved_manifest(root / 'output/final','final-manifest')
    separator = sealed(root / BATCH_FIELDS['separator'],BATCH_SCHEMA + '.separator')
    selection = sealed(root / BATCH_FIELDS['selection'],BATCH_SCHEMA + '.selection')
    state_fields = {'anchor_completed_steps':64,'selected_count':128,'processed_candidates':128,
        'dependent_candidates':0,'accepted_new_rows':128,'rank':1578,'generation':8283,
        **{key:BATCH_STATE[key] for key in ('state_head','target_remainder_sha256','lambda_sha256','terminal')}}
    for value in (head,result,checked,final):
        for key,wanted in state_fields.items():
            require(canonical(value[key]) == canonical(wanted),'batch-parent-actual-terminal-field:' + key)
        for key,name in (('owner_sha256','owner'),('source_sha256','source'),('start_sha256','start'),
                ('selection_sha256','selection'),('selection_start_sha256','selection_start')):
            require(value[key] == descriptors[name]['sha256'],'batch-parent-all-root-file-join:' + key)
    require(checked['status'] == result['status'] == 'PASS' and checked['partial'] is False and
        checked['cross_checked'] is True and checked['candidate'] is True and result['candidate'] is True and
        checked['verified'] is False and result['verified'] is False and
        checked['public_final_compared'] is True and checked['all_completed_payloads_and_json_compared'] is True and
        checked['durable_tail'] is None and checked['public_head_sha256'] == result['head_sha256'] == descriptors['head']['sha256'] and
        checked['producer_result_sha256'] == descriptors['result']['sha256'] and
        checked['final_manifest_sha256'] == result['final_manifest_sha256'] == head['final_manifest_sha256'] == descriptors['final_manifest']['sha256'],
        'batch-parent-successful-whole-checker-not-just-cursor')
    require(canonical(checked['checker_source']) == canonical(original_code['checker']) and
        canonical(checked['runtime']) == canonical(runtime()) and head['kind'] == result['kind'] == final['kind'] == 'Separator' and
        head['new_lambda_oracle'] is result['new_lambda_oracle'] is separator['new_lambda_oracle'] is None,
        'batch-parent-source-and-uncomputed-final-lambda-oracle')
    require(canonical({key:selection[key] for key in BATCH_STATE['old_oracle']}) == canonical(BATCH_STATE['old_oracle']) and
        selection['eof'] is True and ordinary(selection['chords_checked']) == 54433 and ordinary(selection['auxiliary_tests']) == 2,
        'batch-parent-old-complete-54433-plus2-oracle-observation')
    require(start['rank'] == 1450 and start['generation'] == 8155 and start['anchor_completed_steps'] == 64 and
        start['anchor_head_sha256'] == anchor['head']['sha256'] and start['target_remainder_sha256'] == anchor['target_remainder_sha256'] and
        start['selection_lambda_sha256'] == anchor['lambda_sha256'],'batch-parent-original1450-start-and-selection-lambda')
    derived = separator['lambda_rho2']
    require(derived['mode'] == 'derived' and type(derived['value']) is int and derived['value'] == 1 and
        derived['original_rho2_directly_read'] is False and derived['original_rho2_packed_sha256'] == start['original_rho2_packed_sha256'] and
        type(derived['accepted_target_derivation_parents']) is list and len(derived['accepted_target_derivation_parents']) == 225 and
        derived['accepted_target_derivation_parents'][:97] == start['accepted_target_derivation_parents'] and
        len(start['accepted_target_derivation_parents']) == 97,'batch-parent-original97-plus128-DERIVED-not-direct-rho2')
    require(descriptors['target']['bytes'] == descriptors['lambda']['bytes'] == 12096 and
        descriptors['target']['sha256'] == BATCH_STATE['target_remainder_sha256'] and
        descriptors['lambda']['sha256'] == BATCH_STATE['lambda_sha256'],'batch-parent-packed-target-and-lambda')
    fixed = batch_saved_manifest(root / 'output/fixed','fixed-manifest')
    require(canonical(fixed['accepted_fixed_manifest']) == canonical(pin(paths['continuation'] / 'output/fixed/manifest.json',
        'output/fixed/manifest.json')) and fixed['fixed_values_independent_of_lambda'] is True,
        'batch-parent-old-fixed-identity')
    for phase in ('section','cochain','tree'):
        saved = root / 'output/selection' / phase
        batch_saved_manifest(saved,'phase-manifest')
        require(selection['phase_manifests'][phase] == digest(saved / 'manifest.json'),
            'batch-parent-all-three-selection-manifest-joins')
    require(checked['selection_phases_compared'] == ['section','cochain','tree'] and
        checked['candidate_phases_compared'] == [{'ordinal':i,'phases':PHASES} for i in range(128)] and
        type(checked['candidate_decisions_compared']) is int and checked['candidate_decisions_compared'] == 128 and
        type(checked['accepted_rows_compared']) is int and checked['accepted_rows_compared'] == 128,
        'batch-parent-successful-all128-decisions-rows-and768-phases')
    previous_candidate,previous_row,state,target = None,None,start['state_head'],start['target_remainder_sha256']
    for ordinal in range(128):
        folder = root / 'output/candidates' / f'{ordinal:06d}'
        candidate = sealed(folder / 'manifest.json',BATCH_SCHEMA + '.candidate-manifest')
        row_folder = root / 'output/rows' / f'{ordinal:06d}'
        row = batch_saved_manifest(row_folder,'row-manifest')
        require(canonical({key:candidate[key] for key in ('ordinal','outcome','rank_before','rank_after','generation_before',
            'generation_after','accepted_new_rows_before','accepted_new_rows_after')}) == canonical({'ordinal':ordinal,
                'outcome':'INDEPENDENT','rank_before':1450 + ordinal,'rank_after':1451 + ordinal,
                'generation_before':8155 + ordinal,'generation_after':8156 + ordinal,
                'accepted_new_rows_before':ordinal,'accepted_new_rows_after':ordinal + 1}),
            'batch-parent-actual-each-candidate-count-transition')
        require(candidate['eof'] is True and candidate['parent_state_head'] == state and candidate['target_before_sha256'] == target and
            candidate['predecessor_candidate_manifest_sha256'] == previous_candidate and
            candidate['row_manifest_sha256'] == digest(row_folder / 'manifest.json') and
            row['predecessor_row_manifest_sha256'] == previous_row and row['candidate_ordinal'] == ordinal and
            row['local_row_offset'] == ordinal and row['global_row_id'] == 1450 + ordinal,
            'batch-parent-candidate-row-full-hash-chain')
        for phase in PHASES:
            phase_folder = folder / phase if phase == 'reduction' else folder / 'e' / phase
            saved = batch_saved_manifest(phase_folder,'phase-manifest')
            require(saved['phase'] == phase and saved['candidate_ordinal'] == ordinal and
                candidate['phase_manifests'][phase] == digest(phase_folder / 'manifest.json'),
                'batch-parent-all768-actual-phase-manifest-files')
        instruction = sealed(row_folder / 'instruction.json',BATCH_SCHEMA + '.physical-instruction')
        plain_target = read(row_folder / 'target.json',True)
        require(instruction['target_sha256'] == digest(row_folder / 'target.json') and
            instruction['physical_sha256'] == digest(row_folder / 'physical-normalized.bin') and
            plain_target['parent_remainder_sha256'] == target and
            plain_target['remainder_sha256'] == candidate['target_after_sha256'] == digest(folder / 'reduction/target-remainder.bin') and
            instruction['rolling_sha256'] == row['state_head'] == candidate['state_head'] and
            canonical(derived['accepted_target_derivation_parents'][97 + ordinal]) == canonical({
                'role':'batch-row','candidate_ordinal':ordinal,'local_row_offset':ordinal,
                'instruction_sha256':digest(row_folder / 'instruction.json'),
                'row_manifest_sha256':digest(row_folder / 'manifest.json'),
                'target_sha256':digest(row_folder / 'target.json'),'scalar':plain_target['scalar'],
                'parent_remainder_sha256':target,'remainder_sha256':candidate['target_after_sha256'],
                'state_head':candidate['state_head']}),
            'batch-parent-plain-target-packed-target-row-and-DERIVED-join')
        previous_candidate,previous_row = digest(folder / 'manifest.json'),digest(row_folder / 'manifest.json')
        state,target = candidate['state_head'],candidate['target_after_sha256']
    require(state == head['state_head'] and target == head['target_remainder_sha256'] and
        final['last_candidate_manifest_sha256'] == previous_candidate and final['last_row_manifest_sha256'] == previous_row,
        'batch-parent-complete128-prefix-final-state')
    for key,directory,pattern,suffix,count in (
            ('invocations','output/invocations',r'[0-9a-f]{32}\.json','invocation',1),
            ('checkpoints','output/progress/checkpoints',r'[0-9a-f]{64}\.json','checkpoint',772)):
        descriptors[key] = []
        for file in sorted((root / directory).iterdir(),key=lambda item:item.name):
            if re.fullmatch(pattern,file.name) is None:
                require(key == 'invocations' and re.fullmatch(r'\.[0-9a-f]{32}\.json\.pending-[0-9a-f]{32}',file.name),
                    'batch-parent-only-registered-nonordinary-receipt')
                continue
            name = file.relative_to(root).as_posix()
            descriptor = batch_registered_descriptor(root,name,expected)
            value = sealed(file,BATCH_SCHEMA + '.' + suffix)
            require(value['owner_sha256'] == descriptors['owner']['sha256'] and
                value['source_sha256'] == descriptors['source']['sha256'] and value['start_sha256'] == descriptors['start']['sha256'],
                'batch-parent-all-historical-invocation-checkpoint-root-joins')
            descriptors[key].append(descriptor)
        require(len(descriptors[key]) == count,'batch-parent-actual-ordinary-receipt-count:' + key)
    progress = sealed(root / BATCH_FIELDS['progress_head'],BATCH_SCHEMA + '.progress-head')
    require(progress['sequence'] == 771 and progress['current_lambda_sha256'] is None and
        progress['kind'] == 'BatchReductionState' and progress['reduction_state_head'] == head['state_head'] and
        progress['checkpoint_sha256'] == digest(root / 'output/progress/checkpoints' / (progress['checkpoint_sha256'] + '.json')),
        'batch-parent-final-real-private-checkpoint-reference')
    fixture_history = batch_fixture_history(root,run)
    value = {'accepted_schema':BATCH_SCHEMA,**descriptors,**copy.deepcopy(BATCH_STATE)}
    require(len(value) == 33,'batch-anchor-exact33-public-fields')
    save('batch-parent-envelope-intake.json',seal(WF_SCHEMA,'batch-parent-envelope-intake',{
        'status':'PASS','artifact':ARTIFACTS['batch-parent'],'batch_anchor':value,'original_anchor':anchor,
        'input_inventory':{'files':11437,'directories':3475,'bytes':1267599138},
        'restoration':pin(REPORT / 'batch-parent-restoration-result.json','batch-parent-restoration-result.json'),
        'fixture_history':fixture_history,'candidate_manifests_checked':128,'row_manifests_checked':128,
        'candidate_phase_manifests_checked':768,'checkpoints_checked':772,'invocations_checked':1,
        'old_numerical_replays':0,'old_schema_renamed':False,'direct_rho2_claimed':False,**FALSE_ASSURANCE}))
    return value


def api(suffix,destination):
    with destination.open('xb') as stream:
        subprocess.run(['gh','api','repos/' + REPOSITORY + '/' + suffix],stdout=stream,check=True)
    return read(destination)

def live_mode():
    require(sealed(REPORT / 'source-receipt.json')['status'] == 'PASS','source-before-live-admission')
    audit_material_bindings()
    live = REPORT / 'live-parents'
    live.mkdir()
    current = api('actions/runs/' + str(launch()['run']) + '/attempts/' + str(launch()['attempt']),
        live / 'current-run.json')
    require(current['id'] == launch()['run'] and type(current['run_attempt']) is int and current['run_attempt'] == launch()['attempt'] and
        current['head_sha'] == launch()['head'] and current['path'] == launch()['workflow'] and
        current['repository']['id'] == current['head_repository']['id'] == 1312092366 and
        current['head_branch'] == BRANCH,'actual-current-launch-tuple')
    runs,rows,expanded = {},[],0
    for role,spec in ARTIFACTS.items():
        if spec['run'] not in runs:
            runs[spec['run']] = api('actions/runs/' + str(spec['run']),live / ('run-' + str(spec['run']) + '.json'))
        run = runs[spec['run']]
        require(run['id'] == spec['run'] and type(run['run_attempt']) is int and run['run_attempt'] == spec['attempt'] and
            run['head_sha'] == spec['head'] and run['path'] == spec['workflow'] and
            run['repository']['id'] == run['head_repository']['id'] == spec['repository_id'] and
            run['status'] == 'completed' and run['conclusion'] == spec['conclusion'],'live-exact-run:' + role)
        if role in ('continuation','batch-parent'):
            require(run['head_branch'] == BRANCH,'fixed64-same-branch')
        artifact = api('actions/artifacts/' + str(spec['id']),live / ('artifact-' + str(spec['id']) + '.json'))
        require(artifact['id'] == spec['id'] and artifact['name'] == spec['name'] and
            artifact['size_in_bytes'] == spec['bytes'] and artifact['digest'] == spec['sha256'] and
            artifact['expired'] is False,'live-exact-artifact:' + role)
        require(datetime.fromisoformat(artifact['expires_at'].replace('Z','+00:00')) > datetime.now(timezone.utc),
            'live-artifact-not-expired')
        link = artifact['workflow_run']
        require(link['id'] == spec['run'] and link['head_sha'] == spec['head'] and
            link['repository_id'] == link['head_repository_id'] == 1312092366,'live-artifact-run-join')
        archive = INPUTS / (role + '.zip')
        with archive.open('xb') as stream:
            subprocess.run(['gh','api','repos/' + REPOSITORY + '/actions/artifacts/' + str(spec['id']) + '/zip'],
                stdout=stream,check=True)
        require(pin(archive) == {'bytes':spec['bytes'],'sha256':spec['sha256'][7:]},'whole-ZIP-bytes-and-SHA')
        destination = INPUTS / role
        extraction = safe_extract(archive,destination,64 * (1 << 30) - expanded)
        expanded += extraction['expanded_bytes']
        require(expanded <= 64 * (1 << 30),'all-parent-expanded-byte-limit')
        if role == 'batch-parent':
            save('batch-parent-transport-before.json',seal(WF_SCHEMA,'batch-parent-transport-baseline',{
                'status':'RECORDED_METADATA','artifact':spec,'archive':str(archive),'root':str(destination),
                'extraction':extraction,'inventory':scan(destination),'restoration_started':False,**FALSE_ASSURANCE}))
        restoration = restore_batch_parent_directories(destination,extraction) if role == 'batch-parent' else None
        observed = scan(destination)
        row = {'role':role,'artifact':spec,'archive':str(archive),'extraction_root':str(destination),
            'expires_at':artifact['expires_at'],'extraction':extraction,'directory_restoration':restoration}
        save('acquired-parents/' + role + '.json',seal(WF_SCHEMA,'acquired-parent-before',{
            'status':'PASS',**row,**observed,**FALSE_ASSURANCE}))
        rows.append(row)
    save('live-parent-intake.json',seal(WF_SCHEMA,'live-parent-intake',{
        'status':'PASS','launch':launch(),'parents':rows,'count':16,
        'task554_accepted_failure':True,'expanded_bytes':expanded,**FALSE_ASSURANCE}))

def root_paths():
    intake = sealed(REPORT / 'live-parent-intake.json',WF_SCHEMA + '.live-parent-intake')
    require(intake['status'] == 'PASS' and intake['count'] == 16,'complete-live-parent-admission')
    extras = {'state':['state/physical.bin','state/instructions.jsonl','output/result.json'],
        'p1':['instructions.jsonl','degree2.cache.bin'],
        'task712':['r07-grade2-maps-v4-receipt.json','r07-grade2-maps-v4-checker.json'],
        'prepare':['prepare.HEAD'],
        'continuation':['run-receipt.json','accepted-completion/completion-run-receipt.json','checker-result.json'],
        'batch-parent':['run-receipt.json','envelope-inventory-before-run.json','checker-result.json','output/final/manifest.json']}
    for number in range(4):
        extras['block-' + str(number)] = ['block-' + str(number) + '.HEAD']
    for role in ('delta','seed34','packet','refinement','oracle','e'):
        extras[role] = ['checker-result.json','source-receipt.json']
    paths = {}
    for row in intake['parents']:
        role = row['role']
        base = Path(row['extraction_root']).resolve()
        wanted = [PRIMARY[role],*extras.get(role,[])]
        candidates = [folder for folder in [base,*[p for p in base.rglob('*') if p.is_dir()]]
            if all((folder / name).is_file() and not (folder / name).is_symlink() for name in wanted)]
        require(len(candidates) == 1,'one-exact-parent-envelope:' + role)
        paths[role] = candidates[0].resolve()
    require(list(paths) == ROLES,'all-sixteen-parent-roots-in-order')
    for index,left in enumerate(paths.values()):
        for right in [REPORT,OUTPUT,*list(paths.values())[index + 1:]]:
            require(left != right and left not in right.parents and right not in left.parents,'disjoint-input-output-roots')
    return paths

def observe_original_start_header(root,start):
    fields = ("rank","generation","completed_steps","external_e_attached","external_e_numerically_replayed")
    save("original-start-header.json",seal(SCHEMA,"original-start-header",{
        "status":"OBSERVED","actual_start":pin(root / "output/start.json","output/start.json"),
        "expected_start":CONTINUATION_ENTRIES["output/start.json"],
        "fields":{key:{"value":start.get(key),"type":type(start.get(key)).__name__} for key in fields},
        "header_gate_applied":False,"start_replaced_or_renamed":False,**FALSE_ASSURANCE}))


def validate_original_start_header(start):
    require(isinstance(start,dict),"original-start-object")
    for key,wanted in (("rank",1386),("generation",8091),("completed_steps",0),("external_e_attached",1)):
        require(type(start.get(key)) is int and start[key] == wanted,"original-start-exact-integer:" + key)
    require(start.get("external_e_numerically_replayed") is False,"original-start-external-E-not-replayed")


def authenticate_continuation(paths, inventories):
    root = paths["continuation"]
    for name,expected in CONTINUATION_ENTRIES.items():
        exact_pin(root,name,expected)
    prior = root / "accepted-completion"
    for name,expected in COMPLETION_ENTRIES.items():
        exact_pin(prior,name,expected)
    for name,(size,sha256) in LOOP_FILES.items():
        exact_pin(prior,name,{"bytes":size,"sha256":sha256})
    for name in ("output/owner.json","output/source.json","output/start.json","output/fixed/manifest.json"):
        require((root / name).read_bytes() == (prior / name).read_bytes(),"same-frozen-owner-source-start-fixed")
    head = sealed(root / "output/HEAD",LOOP_SCHEMA + ".head")
    result = sealed(root / "output/result.json",LOOP_SCHEMA + ".result")
    checked = sealed(root / "checker-result.json",LOOP_SCHEMA + ".checker-result")
    start = sealed(root / "output/start.json",LOOP_SCHEMA + ".start")
    observe_original_start_header(root,start)
    source = sealed(root / "output/source.json")
    run = read(root / "run-receipt.json",True)
    completion = read(prior / "completion-run-receipt.json",True)
    repair = read(prior / "repair-source-receipt.json",True)
    original_source = read(prior / "source-receipt.json",True)
    resume_source = read(root / "resume-source-receipt.json",True)
    require(run["schema"] == "d972.r07.complete-oracle-cegar-resume64.v1.run-receipt" and
        run["status"] == checked["status"] == completion["status"] == "PASS","successful-saved-continuation")
    require(run["current_launch"] == {key:ARTIFACTS["continuation"][key] for key in ("run","attempt","head","workflow")},
        "observed-resume64-launch")
    require(run["completion_launch"] == completion["completion_launch"] ==
        {key:ACCEPTED_COMPLETION_ARTIFACT[key] for key in ("run","attempt","head","workflow")},"retained-completion-launch")
    require({key:run["accepted_completion_artifact"][key] for key in ACCEPTED_COMPLETION_ARTIFACT} ==
        ACCEPTED_COMPLETION_ARTIFACT,"exact-prior-completion-artifact")
    require(run["original_launch"] == completion["original_launch"] and
        run["original_artifact"] == completion["original_artifact"],"original-producer-lineage")
    require(run["producer_sha256"] == source["producer_sha256"] == resume_source["producer_sha256"] ==
        completion["producer_sha256"] == LOOP_PRODUCER and
        run["checker_sha256"] == checked["checker_sha256"] == resume_source["checker_sha256"] ==
        completion["checker_sha256"] == repair["files"][-1]["sha256"] == LOOP_CHECKER,"same-frozen-P971-Cv2")
    require(len(original_source["files"]) == 19 and len(repair["files"]) == len(resume_source["files"]) == 20 and
        repair["files"][:19] == original_source["files"] and resume_source["files"] == repair["files"],
        "original-and-completion-and-resume-source-roles")
    require(source["data"] == original_source["data"] == repair["data"] == resume_source["data"],"retained-raw-source-identity")
    require({name:(value["bytes"],value["sha256"]) for name,value in source["data"].items()} ==
        {name:value for name,value in RAW.items() if name.startswith("scratchpad/")},"retained-three-raw-pins")
    for value in (source,checked,repair,resume_source):
        require({key:value[key] for key in ("python","numpy")} == runtime(),"same-saved-runtime")
    require(run["producer_runtime"] == run["checker_runtime"] == completion["producer_runtime"] ==
        completion["checker_runtime"] == runtime(),"three-launch-runtime-identity")
    require(head["completed_steps"] == result["completed_steps"] == checked["completed_steps"] ==
        checked["prefix_steps_replayed"] == run["completed_steps"] == run["prefix_steps_replayed"] == 64,
        "observed-complete-sixty-four-prefix")
    require(head["rank"] == 1450 and head["generation"] == 8155 and head["kind"] == "Separator" and
        head["current_snapshot_sha256"] is None and head["current_checkpoint_sha256"] is None and
        result["terminal"] == checked["terminal"] == run["terminal"] == "UNKNOWN_CAP","observed-current-status")
    for key in ("rank","generation","kind","state_head","target_remainder_sha256","lambda_sha256",
                "current_snapshot_sha256","current_checkpoint_sha256"):
        require(head[key] == result[key] == checked[key] == run[key],"saved-current-identity:" + key)
    for key,name in (("owner_sha256","output/owner.json"),("source_sha256","output/source.json"),
                    ("start_sha256","output/start.json"),("fixed_manifest_sha256","output/fixed/manifest.json")):
        require(head[key] == result[key] == checked[key] == digest(root / name),"saved-current-parent:" + key)
    require(checked["head_sha256"] == result["head_sha256"] == run["head_sha256"] == digest(root / "output/HEAD") and
        checked["result_sha256"] == run["producer_result_sha256"] == digest(root / "output/result.json") and
        run["checker_result_sha256"] == digest(root / "checker-result.json"),"saved-HEAD-result-checker-files")
    validate_original_start_header(start)
    for key in ("all_new_committed_arrays_and_json_compared","current_checkpoint_fully_compared",
                "full_four_character_scope","ordinary27_actual_source","all_four_B_summed_each_E"):
        require(checked[key] is True,"whole-prefix-arithmetic-scope:" + key)
    for key,wanted in (("section_equalities_each",8059),("chords_each",54433),("auxiliary_tests_each",2),
            ("source_lower_trits_each_E",96776),("literal_modulus",54),("external_e_attached",1),
            ("old_scans_numerically_replayed",0),("old_inserts_numerically_replayed",0),("old_success_suites",0)):
        require(type(checked[key]) is int and checked[key] == wanted,"whole-prefix-scope:" + key)
    for key in ("actual_resume","all_past32_step_and_snapshot_receipts_match","old_prefix_unchanged",
                "all_readonly_parents_unchanged","all_sources_unchanged","output_unchanged_by_checker"):
        require(run[key] is True,"accepted-resume-preservation:" + key)
    require(run["before_completed_steps"] == run["new_appends_this_run"] == 32 and
        run["producer_invocations_this_run"] == run["checker_invocations_this_run"] == 1 and
        run["old_success_suites_rerun"] == 0,"one-real-saved-resume")
    for value in (checked,result,run,completion):
        require(value["cross_checked"] is False and value["verified"] is False and
            value["grade2_member"] == value["grade2_nonmember"] == "NOT_DECIDED" and value["full_A0"] is False,
            "retained-assurance-boundary")
    for field,name in (("accepted_completion_run_receipt_sha256","accepted-completion/completion-run-receipt.json"),
            ("accepted_completion_checker_result_sha256","accepted-completion/checker-result.json"),
            ("original_source_receipt_sha256","source-receipt.json"),
            ("repair_source_receipt_sha256","accepted-completion/repair-source-receipt.json"),
            ("resume_source_receipt_sha256","resume-source-receipt.json"),
            ("completion_intake_receipt_sha256","completion-intake-receipt.json"),
            ("copy_before_resume_sha256","copy-before-resume.json"),
            ("producer_output_before_checker_sha256","producer-output-before-checker.json"),
            ("preservation_result_sha256","preservation-result.json"),
            ("all_parent_files_before_sha256","all-parent-files-before.json"),
            ("all_parent_files_after_sha256","all-parent-files-after.json")):
        require(run[field] == digest(root / name),"resume-provenance-file:" + field)
    preserved = read(root / "preservation-result.json",True)
    before_checker = read(root / "producer-output-before-checker.json",True)
    output = scan(root / "output")
    require(preserved["status"] == before_checker["status"] == "PASS" and preserved["errors"] == [] and
        output["files"] == preserved["files"] == before_checker["files"] and
        output["directories"] == preserved["directories"] == before_checker["directories"],
        "entire-saved-output-preserved-after-C")
    require(len(output["files"]) == run["output_files"] and len(output["directories"]) == run["output_directories"] and
        sum(row["bytes"] for row in output["files"]) == run["output_bytes"] == preserved["output_bytes"],"saved-output-EOF")
    require(len(checked["steps"]) == len(checked["snapshots"]) == 64,"saved-C-receipt-cardinality")
    phases = ("section","cochain","tree","raw","source","primal","p1","B","physical")
    for index,(snapshot,step) in enumerate(zip(checked["snapshots"],checked["steps"],strict=True)):
        base = root / "output/snapshots" / f"{index:06d}"
        require(snapshot["step"] == index and step["step"] == index + 1 and
            snapshot["snapshot_sha256"] == digest(base / "start.json") and
            snapshot["oracle_manifest_sha256"] == digest(base / "oracle-manifest.json") and
            step["manifest_sha256"] == digest(root / "output/steps" / f"{index + 1:06d}" / "manifest.json"),
            "saved-C-complete-snapshot-files")
        require(set(snapshot["phase_manifests"]) == set(phases),"all-nine-saved-phases")
        for phase in phases:
            folder = base / phase if phase in phases[:3] else base / "e" / phase
            require(snapshot["phase_manifests"][phase] == digest(folder / "manifest.json"),"saved-phase-file-hash")
    old_parents = read(root / "all-parent-files-before.json",True)
    require(old_parents == read(root / "all-parent-files-after.json",True) and old_parents["count"] == 15,
        "accepted-resume-all-parents-unchanged")
    aliases = {role:("BLOCK_" + role[-1] + "_ROOT" if role.startswith("block-") else
        {"state":"STATE_ROOT","delta":"DELTA_ROOT","seed34":"SEED34_ROOT","packet":"PACKET_ROOT",
         "refinement":"REFINEMENT_ROOT","oracle":"ORACLE_ROOT","e":"E_ROOT","prepare":"PREPARE_ROOT",
         "p1":"P1_ROOT","task712":"TASK712_ROOT"}[role]) for role in ROLES[:14]}
    expected_old_roles = {*aliases.values(),"COMPLETION_ROOT"}
    require(isinstance(old_parents["parents"],list) and len(old_parents["parents"]) == 15 and
        all(isinstance(item,dict) and isinstance(item.get("role"),str) for item in old_parents["parents"]) and
        len({item["role"] for item in old_parents["parents"]}) == 15 and
        {item["role"] for item in old_parents["parents"]} == expected_old_roles,"retained-exact-unique-fifteen-roles")
    previous_by_role = {item["role"]:item for item in old_parents["parents"]}
    for role,alias in aliases.items():
        require(retained_inventory(previous_by_role[alias],alias,inventories[role]) == inventories[role],
            "same-fourteen-retained-parent-bodies")
    prior_inventory = scan(prior)
    require(retained_inventory(previous_by_role["COMPLETION_ROOT"],"COMPLETION_ROOT",prior_inventory) ==
        prior_inventory,"saved-completion-root-unchanged")
    prior_tests = []
    for entry in run["prior_tests_authenticated_without_rerun"]:
        path = prior / safe_name(entry["file"])
        require(digest(path) == entry["sha256"] and read(path)["status"] == "PASS" and entry["rerun"] is False,
            "retained-old-test-receipt-only")
        prior_tests.append(entry)
    # Archive provenance, not another copy of all old numerical payloads.
    for folder,label in ((root,"resume64"),(prior,"completion32")):
        for path in sorted(folder.iterdir()):
            if path.is_file() and path.suffix in (".json",".py",".yml",".txt",".log"):
                target = REPORT / "retained-parent-receipts" / label / path.name
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(path,target)
    save("continuation-intake.json",seal(SCHEMA,"continuation-intake",{
        "status":"PASS","artifact":ARTIFACTS["continuation"],"original_launch":run["original_launch"],
        "completion_launch":run["completion_launch"],"resume_launch":run["current_launch"],"new_launch":launch(),
        "producer_sha256":LOOP_PRODUCER,"checker_sha256":LOOP_CHECKER,
        "completion_entry_files":[{"file":name,**value} for name,value in sorted(COMPLETION_ENTRIES.items())],
        "continuation_entry_files":[{"file":name,**value} for name,value in sorted(CONTINUATION_ENTRIES.items())],
        "observed_head":head,"terminal":result["terminal"],"output":output,
        "old_success_suites_rerun":0,"prior_tests_authenticated_without_rerun":prior_tests,**FALSE_ASSURANCE}))
    return head,result,checked

def saved_invocations(root,head,result,checked):
    directory = root / 'output/invocations'
    all_files,normal = [],[]
    identities = ('owner_sha256','source_sha256','start_sha256','fixed_manifest_sha256')
    for file in sorted(directory.iterdir(),key=lambda p:p.name):
        require(file.is_file() and not file.is_symlink(),'accepted-invocation-file-type')
        all_files.append(pin(file,file.relative_to(root).as_posix()))
        if re.fullmatch(r'\.[0-9a-f]{32}\.json\.pending-[0-9a-f]{32}',file.name):
            continue
        require(re.fullmatch(r'[0-9a-f]{32}\.json',file.name) is not None,'accepted-invocation-filename')
        value = sealed(file,LOOP_SCHEMA + '.invocation')
        require(value['invocation'] + '.json' == file.name and
            all(value[key] == head[key] for key in identities),'accepted-invocation-owner')
        normal.append({**{k:v for k,v in value.items() if k != 'sha256'},'sha256':digest(file)})
    require(len(normal) == 3 and canonical(normal) == canonical(checked['invocations']),
        'actual-three-invocations-and-complete-checked-list')
    require(sum(value['sha256'] == result['invocation_sha256'] for value in normal) == 1,
        'saved-explicit-current-invocation')
    prior = sealed(root / 'accepted-completion/checker-result.json',LOOP_SCHEMA + '.checker-result')
    require(canonical(checked['steps'][:32]) == canonical(prior['steps']) and
        canonical(checked['snapshots'][:32]) == canonical(prior['snapshots']) and
        all(value in checked['invocations'] for value in prior['invocations']),
        'accepted-completion-entire32-metadata-prefix-preserved')
    require((root / 'checker-exit-code.txt').read_bytes() == b'0\n' and
        (root / 'checker-stdout.json').read_bytes() == (root / 'checker-result.json').read_bytes() and
        (root / 'producer-result.json').read_bytes() == (root / 'output/result.json').read_bytes(),
        'accepted-actual-exit-and-stdout-file-equality')
    historic = read(root / 'resume-source-receipt.json',True)
    historical_map = {entry['file']:{k:entry[k] for k in ('file','bytes','sha256')} for entry in historic['files']}
    historical_map.pop('search/check_d972_r07_complete_oracle_cegar_continuation_v1.py')
    expected_map = {entry['file']:entry for entry in [*P_DEPS,*C_DEPS]}
    require(canonical(historical_map) == canonical(expected_map),'all19-retained-current-closure-pins')
    return all_files

def anchor_value(root,head,result,checked):
    descriptors = {key:pin(root / name,name) for key,name in (
        ('head','output/HEAD'),('result','output/result.json'),('checker','checker-result.json'),
        ('owner','output/owner.json'),('source','output/source.json'),('start','output/start.json'),
        ('fixed','output/fixed/manifest.json'))}
    descriptors['invocations'] = saved_invocations(root,head,result,checked)
    descriptors['checker_prefix'] = {'steps':len(checked['steps']),'snapshots':len(checked['snapshots']),
        'steps_sha256':sha(canonical(checked['steps'])),
        'snapshots_sha256':sha(canonical(checked['snapshots'])),
        'invocations_sha256':sha(canonical(checked['invocations']))}
    for key in ('completed_steps','rank','generation','kind','state_head','target_remainder_sha256','lambda_sha256'):
        descriptors[key] = copy.deepcopy(head[key])
    descriptors['terminal'] = result['terminal']
    require(descriptors['completed_steps'] == 64 and descriptors['rank'] == 1450 and
        descriptors['generation'] == 8155,'registered-actual64-anchor')
    return descriptors

def validate_acceptance(value,paths,inventories,anchor,code,batch_anchor):
    require(type(value) is dict and set(value) == {'schema','parents','anchor','batch_anchor','code','runtime','registration'} and
        value['schema'] == SCHEMA + '.acceptance','acceptance-exact-seven-plain-keys')
    require(type(value['parents']) is list and len(value['parents']) == 16 and
        [entry.get('role') for entry in value['parents']] == ROLES,'acceptance-sixteen-ordered-roles')
    for entry in value['parents']:
        require(type(entry) is dict and set(entry) == {'role','path','artifact','files','directories'},
            'acceptance-parent-exact-fields')
        role = entry['role']
        require(type(entry['path']) is str and entry['path'] == str(paths[role]) and
            Path(entry['path']).is_absolute(),'acceptance-exact-absolute-parent-root')
        require(canonical(entry['artifact']) == canonical(ARTIFACTS[role]),'acceptance-exact-artifact-types')
        actual = inventories[role]
        validate_inventory({'files':entry['files'],'directories':entry['directories']},
            {row['file']:row for row in actual['files']},set(actual['directories']))
    require(type(value['anchor']) is dict and canonical(value['anchor']) == canonical(anchor),
        'acceptance-exact-observed-anchor')
    for key,wanted in (('completed_steps',64),('rank',1450),('generation',8155)):
        require(type(value['anchor'][key]) is int and value['anchor'][key] == wanted,
            'acceptance-anchor-ordinary-integer')
    require(type(value['batch_anchor']) is dict and canonical(value['batch_anchor']) == canonical(batch_anchor),
        'acceptance-exact-observed-batch-anchor')
    for key in ('upstream_completed_steps','accepted_parent_batch_rows','processed_parent_candidates',
            'dependent_parent_candidates','rank','generation','target_derivation_parents'):
        require(type(value['batch_anchor'][key]) is int and value['batch_anchor'][key] == BATCH_STATE[key],
            'acceptance-batch-anchor-ordinary-integer:' + key)
    require(canonical(value['code']) == canonical(code),'acceptance-complete-code-pins')
    require(canonical(value['runtime']) == canonical(EXPECTED_RUNTIME),'acceptance-exact-runtime')
    require(canonical(value['registration']) == canonical(REGISTRATION),'acceptance-fixed-registration-types')
    return value

def portable_acceptance(value):
    portable = copy.deepcopy(value)
    for entry in portable['parents']:
        del entry['path']
    return portable

def intake_mode():
    require(len(CONTINUATION_ENTRIES) == 30 and len(COMPLETION_ENTRIES) == 10 and len(LOOP_FILES) == 6,
        'all-observed-historical-entry-pins-present')
    paths = root_paths()
    inventories = {role:scan(paths[role]) for role in ROLES}
    # This baseline is saved before any historical metadata gate can reject.
    save('parent-files-before.json',[{'role':role,**inventories[role]} for role in ROLES])
    save('parent-roots.json',{role:str(paths[role]) for role in ROLES})
    head,result,checked = authenticate_continuation(paths,inventories)
    anchor = anchor_value(paths['continuation'],head,result,checked)
    code = code_contract()
    batch_anchor = authenticate_batch_parent(paths,inventories,anchor,code)
    value = {'schema':SCHEMA + '.acceptance','parents':[
        {'role':role,'path':str(paths[role]),'artifact':ARTIFACTS[role],**inventories[role]} for role in ROLES],
        'anchor':anchor,'batch_anchor':batch_anchor,'code':code,'runtime':runtime(),'registration':copy.deepcopy(REGISTRATION)}
    validate_acceptance(value,paths,inventories,anchor,code,batch_anchor)
    save('acceptance.json',value)
    save('acceptance-receipt.json',seal(WF_SCHEMA,'acceptance-receipt',{
        'status':'PASS','acceptance':pin(REPORT / 'acceptance.json','acceptance.json'),
        'portable_acceptance_sha256':sha(canonical(portable_acceptance(value))),
        'parent_inventory_sha256':digest(REPORT / 'parent-files-before.json'),
        'source_receipt_sha256':digest(REPORT / 'source-receipt.json'),
        'anchor':anchor,'batch_anchor':batch_anchor,'code':code,'registration':REGISTRATION,'runtime':runtime(),
        'launch':launch(),'fresh_invocations_registered':1,'old_success_suites_rerun':0,**FALSE_ASSURANCE}))

def metadata_canary():
    begun = time.monotonic()
    actual = read(REPORT / 'acceptance.json',True)
    paths = {role:Path(value) for role,value in read(REPORT / 'parent-roots.json',True).items()}
    inventories = {row['role']:{key:row[key] for key in ('files','directories')}
        for row in read(REPORT / 'parent-files-before.json',True)}
    accepted_anchor = copy.deepcopy(actual['anchor'])
    accepted_batch_anchor = copy.deepcopy(actual['batch_anchor'])
    code = code_contract()
    validate_acceptance(actual,paths,inventories,accepted_anchor,code,accepted_batch_anchor)
    cases = []
    def reject(name,call,reason):
        try:
            call()
        except ValueError as error:
            require(reason in str(error),'canary-intended-rejection:' + name)
            cases.append({'name':name,'reason':str(error)})
        else:
            raise ValueError('missing-metadata-rejection:' + name)
        require(time.monotonic() - begun < 300,'metadata-canary-300-second-limit')
    for name,mutate,reason in (
        ('anchor-rank',lambda v:v['anchor'].__setitem__('rank',1482),'exact-observed-anchor'),
        ('anchor-bool-count',lambda v:v['anchor'].__setitem__('completed_steps',True),'exact-observed-anchor'),
        ('registration-bool-max-batches',lambda v:v['registration'].__setitem__('max_batches',True),'fixed-registration-types'),
        ('registration-cap',lambda v:v['registration'].__setitem__('max_batches',2),'fixed-registration-types'),
        ('missing-code-pin',lambda v:v['code']['checker_dependencies'].pop(),'complete-code-pins'),
        ('missing-parent-file',lambda v:v['parents'][0]['files'].pop(),'full-bytes-and-directories'),
        ('duplicate-parent-role',lambda v:v['parents'].__setitem__(1,copy.deepcopy(v['parents'][0])),'sixteen-ordered-roles'),
        ('file-byte-bool',lambda v:v['parents'][0]['files'][0].__setitem__('bytes',True),'inventory-file-descriptor'),
        ('artifact-attempt-bool',lambda v:v['parents'][0]['artifact'].__setitem__('attempt',True),'exact-artifact-types')):
        changed = copy.deepcopy(actual)
        mutate(changed)
        reject(name,lambda:validate_acceptance(changed,paths,inventories,accepted_anchor,code,accepted_batch_anchor),reason)
    fixture = REPORT / 'metadata-fixture'
    fixture.mkdir()
    for name,raw in {'same/child.txt':b'one\n','same-flat.txt':b'two\n','A/file.txt':b'three\n'}.items():
        file = fixture / name
        file.parent.mkdir(parents=True,exist_ok=True)
        file.write_bytes(raw)
    (fixture / 'empty').mkdir()
    observed = scan(fixture)
    mapping = {row['file']:row for row in observed['files']}
    dirs = set(observed['directories'])
    component_order = copy.deepcopy(observed)
    component_order['files'].sort(key=lambda row:Path(row['file']))
    require(component_order != observed,'fixture-distinguishes-full-string-from-component-order')
    reject('Path-component-order',lambda:validate_inventory(component_order,mapping,dirs),'full-string-order')
    legacy = {'role':'fixture',**component_order}
    legacy_before = canonical(legacy)
    require(retained_inventory(legacy,'fixture',observed) == observed and canonical(legacy) == legacy_before,
        'retained-comparison-copy-without-changing-original')
    repeated = copy.deepcopy(observed)
    repeated['files'].append(copy.deepcopy(repeated['files'][0]))
    reject('duplicate-file',lambda:validate_inventory(repeated,mapping,dirs),'unique-disjoint-names')
    reject('duplicate-JSON-key',lambda:parse(b'{"rank":1450,"rank":1482}'),'duplicate-JSON-key')
    reject('nonfinite-JSON',lambda:parse(b'{"elapsed":NaN}'),'nonfinite-JSON')
    for name,entries,reason in (
        ('ZIP-casefold',[('A/file',b'a'),('a/file',b'b')],'casefold-or-node-collision'),
        ('ZIP-duplicate',[('file',b'a'),('file',b'b')],'exact-name-and-duplicate'),
        ('ZIP-traversal',[('../escape',b'a')],'canonical-relative-POSIX-name')):
        archive = REPORT / (name + '.zip')
        with zipfile.ZipFile(archive,'x') as bundle:
            for filename,payload in entries:
                bundle.writestr(filename,payload)
        reject(name,lambda:safe_extract(archive,REPORT / (name + '-extracted')),reason)
    positive = REPORT / 'ZIP-positive.zip'
    with zipfile.ZipFile(positive,'x') as bundle:
        bundle.writestr('folder/file',b'whole-EOF\n')
    extraction = safe_extract(positive,REPORT / 'ZIP-positive-extracted')
    require(extraction['full_EOF'] is True and (REPORT / 'ZIP-positive-extracted/folder/file').read_bytes() == b'whole-EOF\n',
        'actual-safe-extractor-positive')
    require(time.monotonic() - begun < 300,'metadata-canary-complete-within-limit')
    save('metadata-selftest.json',seal(WF_SCHEMA,'metadata-selftest',{
        'status':'PASS','fixture_scope':'actual acceptance types plus small filesystem/ZIP fixtures',
        'production_interfaces_used':['validate_acceptance','validate_inventory','retained_inventory','parse','safe_extract'],
        'rejected_cases':cases,'rejected_count':len(cases),'old_success_suites':0,
        'metadata_regression_from':'d972-r07-fixed-lambda-cycle-batch-v1',
        'metadata_regression_count':16,'mathematical_success_suites_rerun':0,
        'actual_anchor_arithmetic_replayed':False,'elapsed_seconds':time.monotonic() - begun,**FALSE_ASSURANCE}))

def fixture_root(label):
    require(label in SELFTEST_REJECTIONS,'registered-selftest-fixture-owner')
    return FIXTURES / ('P' if label == 'producer-selftest' else 'C')

def prepare_fixture_root(label):
    require(REPORT.is_absolute() and REPORT.is_dir() and not REPORT.is_symlink(),
        'fixture-absolute-regular-REPORT')
    if not FIXTURES.exists() and not FIXTURES.is_symlink():
        FIXTURES.mkdir()
    require(FIXTURES.is_dir() and not FIXTURES.is_symlink() and FIXTURES.resolve() == FIXTURES,
        'fixture-existing-regular-parent')
    root = fixture_root(label)
    require(not root.exists() and not root.is_symlink(),'fresh-selftest-root-before-source-invocation')
    return root

def fixture_baseline(label):
    root = fixture_root(label)
    require(root.is_dir() and not root.is_symlink(),'completed-selftest-actual-root')
    value = {'status':'PASS','label':label,'root':str(root),'inventory':scan(root),
        'execution':pin(REPORT / 'execution' / (label + '-result.json'),'execution/' + label + '-result.json'),
        'selftest':pin(REPORT / (label + '-stdout.json'),label + '-stdout.json'),
        'source':code_contract()[label.split('-')[0]],'empty_directories_and_hidden_files_included':True,
        **FALSE_ASSURANCE}
    name = 'fixture-baselines/' + root.name + '.json'
    save(name,seal(WF_SCHEMA,'selftest-fixture-baseline',value))
    return pin(REPORT / name,name)

def fixture_audit(stage):
    require(stage in ('before-producer','before-checker','after-checker'),'registered-fixture-scan-stage')
    rows,errors,missing = [],[],[]
    for label in SELFTEST_REJECTIONS:
        root = fixture_root(label)
        entry = {'label':label,'root':str(root),'present':root.exists() or root.is_symlink(),
            'state':'UNFORMED','inventory':None,'baseline':None,'unchanged':False,'reason':None}
        try:
            if not entry['present']:
                missing.append(label + ':root-unformed')
            else:
                entry['state'] = 'PARTIAL'
                require(root.is_dir() and not root.is_symlink(),'fixture-root-regular-directory:' + label)
                observed = scan(root)
                name = 'fixture-inventories/' + stage + '/' + root.name + '.json'
                save(name,observed)
                entry['inventory'] = pin(REPORT / name,name)
                baseline_file = REPORT / 'fixture-baselines' / (root.name + '.json')
                if baseline_file.is_file() and not baseline_file.is_symlink():
                    before = sealed(baseline_file,WF_SCHEMA + '.selftest-fixture-baseline')
                    require(before['status'] == 'PASS' and before['label'] == label and before['root'] == str(root) and
                        before['source'] == code_contract()[label.split('-')[0]],'fixture-baseline-owner')
                    execution = checked_execution(label)
                    require(execution['selftest_root'] == str(root),'fixture-explicit-executed-root')
                    for field in ('execution','selftest'):
                        payload_descriptor(REPORT,before[field])
                    gate = sealed(REPORT / (label + '-gate.json'),WF_SCHEMA + '.selftest-gate')
                    entry['baseline'] = pin(baseline_file,baseline_file.relative_to(REPORT).as_posix())
                    require(gate['status'] == 'PASS' and gate['fixture'] == entry['baseline'],
                        'fixture-baseline-joins-passed-source-test')
                    require(canonical(observed) == canonical(before['inventory']),
                        'exact-whole-fixture-subtree-unchanged:' + label)
                    entry['unchanged'],entry['state'] = True,'COMPLETE'
                else:
                    missing.append(label + ':passed-baseline-unformed')
        except BaseException as exc:
            entry['reason'] = type(exc).__name__ + ':' + str(exc)
            errors.append(label + ':' + entry['reason'])
        rows.append(entry)
    try:
        require(FIXTURES.is_dir() and not FIXTURES.is_symlink(),'fixture-container-regular-directory')
        require(sorted(path.name for path in FIXTURES.iterdir()) == ['C','P'],
            'complete-fixture-container-has-only-two-explicit-roots')
    except BaseException as exc:
        if missing and not errors:
            missing.append('container:' + str(exc))
        else:
            errors.append('container:' + type(exc).__name__ + ':' + str(exc))
    value = {'status':'FAIL' if errors else ('INCOMPLETE' if missing else 'PASS'),
        'stage':stage,'fixtures':rows,'errors':errors,'missing':missing,
        'producer_execution_observed':(REPORT / 'execution/producer-result.json').is_file(),
        'checker_execution_observed':(REPORT / 'execution/checker-result.json').is_file(),
        'scope':'each entire P/C fixture subtree, including all empty directories and hidden tails',
        'mathematical_replays':0,**FALSE_ASSURANCE}
    save('selftest-fixtures-' + stage + '.json',seal(WF_SCHEMA,'selftest-fixture-comparison',value))
    return value

def parent_arguments():
    paths = read(REPORT / 'parent-roots.json',True)
    require(set(paths) == set(ROLES),'execution-sixteen-roots')
    args = []
    for role in ROLES:
        args.extend(['--block-root' if role.startswith('block-') else '--' + role + '-root',paths[role]])
    return args + ['--acceptance',str(REPORT / 'acceptance.json')]

def command(label):
    if label == 'metadata':
        return [sys.executable,'-B',str(REPORT / 'driver.py'),'metadata-canary'],300,300,None
    if label in ('producer-selftest','checker-selftest'):
        role = label.split('-')[0]
        return [sys.executable,'-B',str(ROOT / code_contract()[role]['file']),
            '--selftest','--selftest-root',str(fixture_root(label)),
            *(['--batch-size','128'] if role == 'producer' else []),
            '--max-seconds','300','--max-memory-mib','7168'],300,360,role
    if label == 'producer':
        return [sys.executable,'-B',str(ROOT / os.environ['PRODUCER_FILE']),*parent_arguments(),
            '--output',str(OUTPUT),'--batch-size','128','--max-seconds','5400',
            '--max-memory-mib','7168'],5400,6000,'producer'
    require(label == 'checker','registered-execution-label')
    return [sys.executable,'-B',str(ROOT / os.environ['CHECKER_FILE']),*parent_arguments(),
        '--candidate-root',str(OUTPUT),'--output',str(REPORT / 'checker-result.json'),
        '--max-seconds','10800','--max-memory-mib','7168',
        '--producer-max-seconds','5400','--producer-max-memory-mib','7168'],10800,11400,'checker'

def utc():
    return datetime.now(timezone.utc).isoformat()

def rusage(value):
    return {key:getattr(value,key) for key in ('ru_utime','ru_stime','ru_maxrss','ru_minflt','ru_majflt',
        'ru_inblock','ru_oublock','ru_nvcsw','ru_nivcsw')}

def child_io(pid):
    try:
        lines = Path('/proc') / str(pid) / 'io'
        return {key:int(value.strip()) for key,value in (line.split(':',1) for line in lines.read_text().splitlines())}
    except (OSError,ValueError):
        return None

def execute(label):
    args,seconds,outer_seconds,role = command(label)
    require(sealed(REPORT / 'source-receipt.json')['status'] == 'PASS','execution-admitted-source')
    audit_bindings = audit_material_bindings()
    observed_runtime = runtime()
    if label in SELFTEST_REJECTIONS:
        prepare_fixture_root(label)
    if label == 'producer':
        require(not OUTPUT.exists() and not OUTPUT.is_symlink(),'one-fresh-producer-output')
        require(fixture_audit('before-producer')['status'] == 'PASS','both-fixtures-whole-before-producer')
        save('intake-controls-before.json',scan(REPORT))
    if label == 'checker':
        require(fixture_audit('before-checker')['status'] == 'PASS','both-fixtures-whole-after-P-before-checker')
    begin = time.monotonic()
    before_usage = rusage(resource.getrusage(resource.RUSAGE_CHILDREN))
    receipt = {'label':label,'argv':args,'working_directory':str(ROOT),'started_utc':utc(),
        'internal_seconds':seconds,'outer_seconds':outer_seconds,'term_grace_seconds':30,
        'max_memory_mib':7168 if role is not None else None,'runtime':observed_runtime,
        'source':None if role is None else code_contract()[role],
        'source_receipt_sha256':digest(REPORT / 'source-receipt.json'),
        'audit_materials':audit_bindings,
        'acceptance_sha256':digest(REPORT / 'acceptance.json'),
        'driver':pin(REPORT / 'driver.py','driver.py'),'launch':launch(),
        'selftest_root':str(fixture_root(label)) if label in SELFTEST_REJECTIONS else None,
        'old_success_suites':0,**FALSE_ASSURANCE}
    if label == 'producer':
        receipt['intake_controls_before_sha256'] = digest(REPORT / 'intake-controls-before.json')
    save('execution/' + label + '-start.json',seal(WF_SCHEMA,'execution-start',receipt))
    stdout_path,stderr_path = REPORT / (label + '-stdout.json'),REPORT / (label + '-stderr.log')
    process = None
    exit_code,reason,last_io,io_at = None,None,None,None
    term_sent = False
    try:
        with stdout_path.open('xb') as stdout,stderr_path.open('xb') as stderr:
            process = subprocess.Popen(args,cwd=ROOT,stdout=stdout,stderr=stderr,start_new_session=True)
            while True:
                elapsed = time.monotonic() - begin
                sampled = child_io(process.pid)
                if sampled is not None:
                    last_io,io_at = sampled,elapsed
                code = process.poll()
                if code is not None:
                    exit_code = code
                    break
                if elapsed >= outer_seconds - 30 and not term_sent:
                    os.killpg(process.pid,signal.SIGTERM)
                    term_sent = True
                    reason = 'outer-deadline-TERM'
                if elapsed >= outer_seconds:
                    os.killpg(process.pid,signal.SIGKILL)
                    exit_code = process.wait()
                    reason = 'outer-deadline-KILL'
                    break
                time.sleep(min(0.5,max(0.01,outer_seconds - elapsed)))
    except BaseException as error:
        reason = type(error).__name__ + ':' + str(error)
        if process is not None and process.poll() is None:
            os.killpg(process.pid,signal.SIGTERM)
            try:
                exit_code = process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid,signal.SIGKILL)
                exit_code = process.wait()
    after_usage = rusage(resource.getrusage(resource.RUSAGE_CHILDREN))
    finish = {'start_receipt_sha256':digest(REPORT / 'execution' / (label + '-start.json')),
        **receipt,'finished_utc':utc(),'elapsed_seconds':time.monotonic() - begin,'exit_code':exit_code,
        'outer_terminated':term_sent,'reason':reason,
        'stdout':pin(stdout_path,label + '-stdout.json') if stdout_path.is_file() else None,
        'stderr':pin(stderr_path,label + '-stderr.log') if stderr_path.is_file() else None,
        'child_rusage_before':before_usage,'child_rusage_after':after_usage,
        'child_io_last_sample':last_io,'child_io_sample_elapsed_seconds':io_at,
        'child_io_sample_is_complete_final_counter':False,
        'rusage_scope':'all children of this fresh launcher; ru_maxrss in KiB, block counters from OS'}
    save('execution/' + label + '-result.json',seal(WF_SCHEMA,'execution-result',finish))
    (REPORT / (label + '-exit-code.txt')).write_text(str(exit_code) + '\n',encoding='ascii')
    return 0 if exit_code == 0 and not term_sent and reason is None else 1

def checked_execution(label):
    value = sealed(REPORT / 'execution' / (label + '-result.json'),WF_SCHEMA + '.execution-result')
    start = REPORT / 'execution' / (label + '-start.json')
    require(value['start_receipt_sha256'] == digest(start),'execution-start-file-identity')
    initial = sealed(start,WF_SCHEMA + '.execution-start')
    require(all(canonical(value[key]) == canonical(item) for key,item in initial.items()
        if key not in ('schema','sha256')),'execution-start-and-finish-fields')
    args,seconds,outer,role = command(label)
    require(value['argv'] == args and value['internal_seconds'] == seconds and value['outer_seconds'] == outer and
        value['source'] == (None if role is None else code_contract()[role]) and value['runtime'] == runtime() and
        value['launch'] == launch() and value['acceptance_sha256'] == digest(REPORT / 'acceptance.json') and
        value['driver'] == pin(REPORT / 'driver.py','driver.py') and
        value['source_receipt_sha256'] == digest(REPORT / 'source-receipt.json'),'execution-registered-inputs')
    require(canonical(value['audit_materials']) == canonical(audit_material_bindings()),
        'execution-bound-both-static-audits-and-nonexecuting-history')
    require(value['selftest_root'] == (str(fixture_root(label)) if label in SELFTEST_REJECTIONS else None),
        'execution-explicit-selftest-root-and-no-mathematical-parent-selftest-arguments')
    require(type(value['elapsed_seconds']) in (int,float) and math.isfinite(value['elapsed_seconds']) and
        0 <= value['elapsed_seconds'] <= outer + 15,'execution-observed-seconds')
    require(type(value['exit_code']) is int and value['exit_code'] == 0 and value['outer_terminated'] is False and value['reason'] is None and
        (REPORT / (label + '-exit-code.txt')).read_bytes() == b'0\n','execution-actual-success')
    for field in ('stdout','stderr'):
        entry = value[field]
        require(pin(REPORT / safe_name(entry['file']),entry['file']) == entry,'execution-' + field + '-full-bytes')
    return value

def test_gate(label):
    execution = checked_execution(label)
    if label == 'metadata':
        result = sealed(REPORT / 'metadata-selftest.json',WF_SCHEMA + '.metadata-selftest')
        require(result['status'] == 'PASS' and type(result['old_success_suites']) is int and result['old_success_suites'] == 0 and
            result['actual_anchor_arithmetic_replayed'] is False and type(result['rejected_count']) is int and result['rejected_count'] == 16 and
            len(result['rejected_cases']) == 16,'metadata16-registration-regression-exact-gate')
        require(result['metadata_regression_from'] == 'd972-r07-fixed-lambda-cycle-batch-v1' and
            type(result['metadata_regression_count']) is int and result['metadata_regression_count'] == 16 and
            type(result['mathematical_success_suites_rerun']) is int and result['mathematical_success_suites_rerun'] == 0,
            'sixteen-existing-metadata-cases-without-old-mathematical-suites')
    else:
        result = sealed(REPORT / (label + '-stdout.json'),SCHEMA + '.selftest')
        require(set(result) == {'schema','sha256','status','tests','fixture_scope','production_interfaces_used',
            'old_success_suites','actual_anchor_arithmetic_replayed','candidate','cross_checked','verified'},
            'new-selftest-exact-fields')
        require(result['status'] == 'PASS' and type(result['tests']) is list and
            [item['name'] for item in result['tests']] == SELFTEST_NAMES and
            all(type(item) is dict and set(item) == {'name','status','rejected_cases'} and item['status'] == 'PASS' and
                type(item['rejected_cases']) is list and item['rejected_cases'] and
                all(type(name) is str and name for name in item['rejected_cases']) for item in result['tests']),
            'new-selftest-two-literal-and-third-parent-metadata-group')
        require([len(item['rejected_cases']) for item in result['tests']] == SELFTEST_REJECTIONS[label],
            'public-k128-rejection-counts-from-frozen-source-pins')
        require(type(result['fixture_scope']) is str and result['fixture_scope'] and
            type(result['production_interfaces_used']) is list and result['production_interfaces_used'] and
            all(type(name) is str and name for name in result['production_interfaces_used']),
            'new-selftest-explicit-helper-fixture-scope')
        require(type(result['old_success_suites']) is int and result['old_success_suites'] == 0 and
            result['actual_anchor_arithmetic_replayed'] is False,'new-selftest-no-old-actual-replay')
    require(all(result[key] is False for key in ('candidate','cross_checked','verified')),'selftest-false-assurance')
    fixture = None if label == 'metadata' else fixture_baseline(label)
    save(label + '-gate.json',seal(WF_SCHEMA,'selftest-gate',{'status':'PASS',
        'execution':pin(REPORT / 'execution' / (label + '-result.json'),'execution/' + label + '-result.json'),
        'selftest':pin(REPORT / ('metadata-selftest.json' if label == 'metadata' else label + '-stdout.json'),
            'metadata-selftest.json' if label == 'metadata' else label + '-stdout.json'),
        'fixture':fixture,'metadata_regression_cases':16 if label == 'metadata' else 0,
        'new_mathematical_selftest_groups':0 if label == 'metadata' else 2,
        'new_parent_metadata_selftest_groups':0 if label == 'metadata' else 1,
        'old_success_suites':0,**FALSE_ASSURANCE}))

def fixture_archive_boundary(begun):
    require(time.monotonic() - begun < 300,'fixture-preservation-300-second-limit')
    require(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss <= 7168 * 1024,
        'fixture-preservation-7168-MiB-limit')

def fixture_zip_info(name,directory):
    info = zipfile.ZipInfo(safe_name(name) + ('/' if directory else ''),date_time=(1980,1,1,0,0,0))
    info.create_system = 3
    info.external_attr = ((stat.S_IFDIR | 0o755) if directory else (stat.S_IFREG | 0o600)) << 16
    if directory:
        info.external_attr |= 0x10
    info.compress_type = zipfile.ZIP_DEFLATED
    return info

def fixture_archive_write(archive,observed,begun):
    inventory_fields(observed)
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as bundle:
        for name in observed['directories']:
            fixture_archive_boundary(begun)
            directory = FIXTURES / name
            require(directory.is_dir() and not directory.is_symlink(),'archive-directory-remains-regular:' + name)
            bundle.writestr(fixture_zip_info(name,True),b'')
        for entry in observed['files']:
            fixture_archive_boundary(begun)
            source = FIXTURES / entry['file']
            require(source.is_file() and not source.is_symlink(),'archive-source-regular-file:' + entry['file'])
            count,hasher = 0,hashlib.sha256()
            with source.open('rb') as incoming, bundle.open(fixture_zip_info(entry['file'],False),'w',force_zip64=True) as outgoing:
                require(stat.S_ISREG(os.fstat(incoming.fileno()).st_mode),'archive-opened-regular-file')
                while True:
                    fixture_archive_boundary(begun)
                    block = incoming.read(1 << 20)
                    if not block:
                        break
                    count += len(block)
                    require(count <= entry['bytes'],'archive-source-longer-than-inventory')
                    hasher.update(block)
                    require(outgoing.write(block) == len(block),'archive-whole-write')
            require(count == entry['bytes'] and hasher.hexdigest() == entry['sha256'],
                'archive-source-full-bytes-SHA-and-EOF:' + entry['file'])

def fixture_archive_read(archive,observed,begun):
    files = {entry['file']:entry for entry in observed['files']}
    directories = set(observed['directories'])
    seen,folded,read_files,read_directories = set(),set(),[],[]
    with zipfile.ZipFile(archive,'r') as bundle:
        entries = bundle.infolist()
        require(len(entries) == len(files) + len(directories) and len(entries) <= 1000000,
            'fixture-archive-entire-entry-count')
        for entry in entries:
            fixture_archive_boundary(begun)
            require(entry.orig_filename == entry.filename and not entry.flag_bits & 1,
                'fixture-archive-exact-unencrypted-name')
            is_dir = entry.is_dir()
            name = safe_name(entry.filename[:-1] if is_dir else entry.filename)
            require(name not in seen and name.casefold() not in folded,'fixture-archive-duplicate-or-casefold')
            seen.add(name)
            folded.add(name.casefold())
            mode = entry.external_attr >> 16
            require(entry.create_system == 3 and stat.S_IFMT(mode) == (stat.S_IFDIR if is_dir else stat.S_IFREG),
                'fixture-archive-exact-regular-node-type')
            if is_dir:
                require(name in directories and entry.file_size == 0,'fixture-archive-all-explicit-directory-entries')
                with bundle.open(entry,'r') as stream:
                    require(stream.read(1) == b'','fixture-directory-EOF')
                read_directories.append(name)
            else:
                require(name in files and entry.file_size == files[name]['bytes'],'fixture-archive-full-file-size')
                count,hasher = 0,hashlib.sha256()
                with bundle.open(entry,'r') as stream:
                    while True:
                        fixture_archive_boundary(begun)
                        block = stream.read(1 << 20)
                        if not block:
                            break
                        count += len(block)
                        require(count <= files[name]['bytes'],'fixture-archive-no-tail-outside-declared-file')
                        hasher.update(block)
                value = {'file':name,'bytes':count,'sha256':hasher.hexdigest()}
                require(value == files[name],'fixture-archive-entire-decompressed-bytes-SHA-EOF-and-CRC')
                read_files.append(value)
    recovered = {'files':sorted(read_files,key=lambda row:row['file']),'directories':sorted(read_directories)}
    inventory_fields(recovered)
    require(canonical(recovered) == canonical(observed),'fixture-archive-all-files-and-directories-equal-scan')
    return recovered

def fixture_archive_mode():
    begun = time.monotonic()
    archive = REPORT / 'selftest-fixtures.zip'
    status,error,comparison = 'INCOMPLETE',None,None
    present = FIXTURES.exists() or FIXTURES.is_symlink()
    inventory_pin,recovered_pin,after_pin,archive_pin = None,None,None,None
    full_eof = False
    try:
        comparison = fixture_audit('after-checker')
        if present:
            observed = scan(FIXTURES)
            save('selftest-fixtures-inventory.json',observed)
            inventory_pin = pin(REPORT / 'selftest-fixtures-inventory.json','selftest-fixtures-inventory.json')
            fixture_archive_write(archive,observed,begun)
            recovered = fixture_archive_read(archive,observed,begun)
            save('selftest-fixtures-archive-readback.json',recovered)
            recovered_pin = pin(REPORT / 'selftest-fixtures-archive-readback.json','selftest-fixtures-archive-readback.json')
            after = scan(FIXTURES)
            save('selftest-fixtures-after-archive.json',after)
            after_pin = pin(REPORT / 'selftest-fixtures-after-archive.json','selftest-fixtures-after-archive.json')
            require(canonical(after) == canonical(observed),'fixture-source-unchanged-during-archive-and-readback')
            archive_pin = pin(archive,'selftest-fixtures.zip')
            fixture_archive_boundary(begun)
            full_eof = True
            status = 'FAIL' if comparison['status'] == 'FAIL' else 'PASS'
        else:
            error = 'fixture-container-unformed; no synthetic empty completion was created'
    except BaseException as exc:
        status,error = 'FAIL',type(exc).__name__ + ':' + str(exc)
        if archive.is_file() and not archive.is_symlink():
            archive_pin = pin(archive,'selftest-fixtures.zip')
    comparison_file = REPORT / 'selftest-fixtures-after-checker.json'
    save('selftest-fixtures-archive-receipt.json',seal(WF_SCHEMA,'selftest-fixture-archive',{
        'status':status,'reason':error,'fixture_container':str(FIXTURES),'container_present':present,
        'comparison':pin(comparison_file,'selftest-fixtures-after-checker.json') if comparison_file.is_file() else None,
        'both_completed_roots_unchanged':comparison is not None and comparison['status'] == 'PASS',
        'inventory':inventory_pin,'archive':archive_pin,'readback_inventory':recovered_pin,'after_inventory':after_pin,
        'all_entries_and_explicit_directories_read':full_eof,'all_file_bytes_SHA_EOF_and_CRC_read':full_eof,
        'raw_fixtures_retained':True,'excluded_entries':[],'silently_filtered_entries':False,
        'partial_or_missing_roots_claimed_complete':False,'archive_contains_itself':False,
        'elapsed_seconds':time.monotonic() - begun,'rusage':rusage(resource.getrusage(resource.RUSAGE_SELF)),
        'internal_seconds':300,'outer_seconds':360,'max_memory_mib':7168,'mathematical_replays':0,
        'scope':'all actually present fixture files and every directory; no private fixture layout assumptions',
        **FALSE_ASSURANCE}))
    return 0 if status == 'PASS' else 1

def post_producer():
    current = scan(OUTPUT) if OUTPUT.is_dir() and not OUTPUT.is_symlink() else None
    execution = read(REPORT / 'execution/producer-result.json',True) if (REPORT / 'execution/producer-result.json').is_file() else None
    save('producer-output-before-checker.json',seal(WF_SCHEMA,'producer-output-before-checker',{
        'status':'PASS' if current is not None else 'INCOMPLETE','output':current,
        'producer_execution':None if execution is None else pin(REPORT / 'execution/producer-result.json',
            'execution/producer-result.json'),'taken_before_checker':True,**FALSE_ASSURANCE}))
    roots = read(REPORT / 'parent-roots.json',True)
    parents = [{'role':role,**scan(Path(roots[role]))} for role in ROLES]
    code = observe_code()
    before = read(REPORT / 'source-before.json',True)
    audit_bindings = audit_material_bindings()
    actual_acceptance = pin(REPORT / 'acceptance.json','acceptance.json')
    admission = sealed(REPORT / 'acceptance-receipt.json',WF_SCHEMA + '.acceptance-receipt')
    inputs_unchanged = (canonical(parents) == (REPORT / 'parent-files-before.json').read_bytes() and
        code == before['files'] == code_union(code_contract()) and actual_acceptance == admission['acceptance'] and
        pin(REPORT / 'driver.py','driver.py') == before['driver'] and
        pin(ROOT / os.environ['WF_FILE'],os.environ['WF_FILE']) == before['workflow'])
    save('inputs-after-producer-before-checker.json',seal(WF_SCHEMA,'inputs-after-producer',{
        'status':'PASS' if inputs_unchanged else 'FAIL','parents':parents,'code':code,
        'acceptance':actual_acceptance,'driver':pin(REPORT / 'driver.py','driver.py'),
        'audit_materials':audit_bindings,
        'workflow':pin(ROOT / os.environ['WF_FILE'],os.environ['WF_FILE']),
        'parent_before_sha256':digest(REPORT / 'parent-files-before.json'),
        'source_before_sha256':digest(REPORT / 'source-before.json'),'taken_before_checker':True,**FALSE_ASSURANCE}))
    require(inputs_unchanged,'all-P-inputs-unchanged-before-C')
    complete_exit = execution is not None and type(execution['exit_code']) is int and execution['exit_code'] == 0
    partial_exit = execution is not None and type(execution['exit_code']) is int and execution['exit_code'] == 3
    formed = current is not None and all((OUTPUT / name).is_file() for name in
        ('parent-intake.json','owner.json','source.json','start.json','parent-layout.json','fixed/manifest.json','selection/start.json','progress/HEAD'))
    eligible = formed and (complete_exit or partial_exit)
    with open(os.environ['GITHUB_OUTPUT'],'a',encoding='utf-8') as stream:
        stream.write('checker=' + ('true' if eligible else 'false') + '\n')

def preservation_mode():
    errors,missing = [],[]
    flags = {}
    def guard(name,call):
        try:
            result = call()
            flags[name] = True
            return result
        except BaseException as error:
            flags[name] = False
            errors.append({'scope':name,'reason':type(error).__name__ + ':' + str(error)})
            return None
    source_before = REPORT / 'source-before.json'
    if source_before.is_file():
        def source_after():
            before = read(source_before,True)
            observed = observe_code()
            save('source-after.json',{'files':observed,'workflow':pin(ROOT / os.environ['WF_FILE'],os.environ['WF_FILE']),
                'driver':pin(REPORT / 'driver.py','driver.py')})
            require(observed == before['files'] and before['workflow'] == pin(ROOT / os.environ['WF_FILE'],os.environ['WF_FILE']) and
                before['driver'] == pin(REPORT / 'driver.py','driver.py'),'all-code-raw-driver-workflow-unchanged')
            require((REPORT / 'workflow.yml').read_bytes() == (ROOT / os.environ['WF_FILE']).read_bytes(),
                'workflow-diagnostic-copy-unchanged')
            for entry in before['files']:
                require(pin(REPORT / 'checkout-sources' / entry['file'],entry['file']) == entry,
                    'diagnostic-code-and-raw-copy-unchanged')
            return observed
        guard('all_code_raw_driver_and_copies_unchanged',source_after)
    else:
        missing.append('source-before.json')
        # Preserve and authenticate even a partial source acquisition.
        for file in sorted((REPORT / 'acquired-code').glob('*.json')):
            def acquired_code(file=file):
                value = read(file,True)
                require(pin(ROOT / value['file'],value['file']) == value['observed'] and
                    pin(Path(value['copy']),value['file']) == value['observed'],'partial-acquired-source-unchanged')
            guard('acquired_code:' + file.name,acquired_code)
    audit_before = REPORT / 'audit-materials-before.json'
    if audit_before.is_file():
        def audits_after():
            before = sealed(audit_before,WF_SCHEMA + '.audit-materials-before')
            observed = audit_material_observation(before)
            save('audit-materials-after.json',seal(WF_SCHEMA,'audit-materials-after',{
                'observation':observed,'baseline':pin(audit_before,'audit-materials-before.json'),
                'launch':launch(),**FALSE_ASSURANCE}))
            return audit_material_bindings()
        guard('all_static_audit_receipts_registry_and_history_copies_unchanged',audits_after)
    else:
        missing.append('audit-materials-before.json')
        # A stopped audit acquisition still retains and checks every completed copy.
        for file in sorted((REPORT / 'acquired-audit-history').glob('*.json')):
            def acquired_audit(file=file):
                item = read(file,True)
                audit_source_bytes(item['source'])
                require(pin(REPORT / 'audit-history-sources' / item['source']['file'],
                    item['source']['file']) == item['source'],'partial-audit-history-copy-unchanged')
            guard('acquired_audit_history:' + file.stem,acquired_audit)
        history_root = REPORT / 'audit-history-sources'
        if history_root.is_dir() and not history_root.is_symlink():
            guard('partial_audit_history_inventory_saved',lambda:save('audit-history-partial-after.json',scan(history_root)))
    transport_before = REPORT / 'batch-parent-transport-before.json'
    if transport_before.is_file():
        def batch_transport_after():
            before = sealed(transport_before,WF_SCHEMA + '.batch-parent-transport-baseline')
            root,archive = Path(before['root']),Path(before['archive'])
            require(INPUTS.resolve() in root.resolve().parents and INPUTS.resolve() in archive.resolve().parents and
                canonical(before['artifact']) == canonical(ARTIFACTS['batch-parent']),
                'batch-parent-transport-original-paths-and-artifact')
            observed = scan(root)
            expected_dirs = set(before['inventory']['directories']) | set(BATCH_ABSENT_DIRECTORIES)
            files_equal = canonical(observed['files']) == canonical(before['inventory']['files'])
            dirs_allowed = set(before['inventory']['directories']) <= set(observed['directories']) <= expected_dirs
            save('batch-parent-transport-after.json',seal(WF_SCHEMA,'batch-parent-transport-after',{
                'before':pin(transport_before,'batch-parent-transport-before.json'),'inventory':observed,
                'all_original_files_unchanged':files_equal,'only_registered_directory_additions':dirs_allowed,
                'all36_registered_directories_now_present':set(observed['directories']) == expected_dirs,
                'completed_admission_inferred':False,**FALSE_ASSURANCE}))
            require(files_equal and dirs_allowed and pin(archive) == {
                'bytes':before['artifact']['bytes'],'sha256':before['artifact']['sha256'][7:]},
                'batch-parent-transport-full-ZIP-files-and-partial-restoration-preserved')
        guard('batch_parent_transport_files_unchanged_and_only_registered_directories',batch_transport_after)
    else:
        missing.append('batch-parent-transport-before.json')
    acquired = sorted((REPORT / 'acquired-parents').glob('*.json'),key=lambda p:p.name)
    for file in acquired:
        def acquired_parent(file=file):
            before = sealed(file,WF_SCHEMA + '.acquired-parent-before')
            root = Path(before['extraction_root'])
            archive = Path(before['archive'])
            require(INPUTS.resolve() in root.resolve().parents and INPUTS.resolve() in archive.resolve().parents,
                'acquired-inputs-remain-contained')
            after = scan(root)
            save('acquired-parents-after/' + file.name,after)
            require(after == {key:before[key] for key in ('files','directories')} and
                pin(archive) == {'bytes':before['artifact']['bytes'],'sha256':before['artifact']['sha256'][7:]},
                'entire-ZIP-and-extraction-unchanged')
        guard('acquired_parent:' + file.stem,acquired_parent)
    if len(acquired) != 16:
        missing.append('all-sixteen-acquired-parent-baselines')
    parent_before = REPORT / 'parent-files-before.json'
    parent_roots = REPORT / 'parent-roots.json'
    if parent_before.is_file() and parent_roots.is_file():
        def parents_after():
            roots = read(parent_roots,True)
            after = [{'role':role,**scan(Path(roots[role]))} for role in ROLES]
            save('parent-files-after.json',after)
            require(canonical(after) == parent_before.read_bytes(),'all-sixteen-full-parent-inventories-unchanged')
        guard('all_parent_files_and_directories_unchanged',parents_after)
    else:
        missing.append('resolved-parent-baseline')
    if (REPORT / 'acceptance-receipt.json').is_file():
        def acceptance_after():
            receipt = sealed(REPORT / 'acceptance-receipt.json',WF_SCHEMA + '.acceptance-receipt')
            require(pin(REPORT / 'acceptance.json','acceptance.json') == receipt['acceptance'],
                'actual-acceptance-all-bytes-unchanged')
            value = read(REPORT / 'acceptance.json',True)
            require(sha(canonical(portable_acceptance(value))) == receipt['portable_acceptance_sha256'],
                'portable-acceptance-unchanged')
        guard('acceptance_unchanged',acceptance_after)
    else:
        missing.append('acceptance-receipt.json')
    if (REPORT / 'intake-controls-before.json').is_file():
        def controls_after():
            before = read(REPORT / 'intake-controls-before.json',True)
            inventory_fields(before)
            for entry in before['files']:
                require(pin(REPORT / entry['file'],entry['file']) == entry,'all-preproducer-control-files-unchanged')
            for directory in before['directories']:
                require((REPORT / directory).is_dir() and not (REPORT / directory).is_symlink(),
                    'all-preproducer-control-directories-retained')
            initial = sealed(REPORT / 'execution/producer-start.json',WF_SCHEMA + '.execution-start')
            require(initial['intake_controls_before_sha256'] == digest(REPORT / 'intake-controls-before.json'),
                'control-baseline-original-start-binding')
        guard('all_intake_controls_and_old_test_receipts_unchanged',controls_after)
    else:
        missing.append('preproducer-control-baseline')
    if (REPORT / 'selftest-fixtures-archive-receipt.json').is_file():
        guard('both_complete_fixture_subtrees_and_entire_archive_unchanged',check_fixture_preservation)
    else:
        missing.append('selftest-fixtures-archive-receipt.json')
    if (REPORT / 'inputs-after-producer-before-checker.json').is_file():
        def between_and_after():
            between = sealed(REPORT / 'inputs-after-producer-before-checker.json',WF_SCHEMA + '.inputs-after-producer')
            after_code = read(REPORT / 'source-after.json',True)
            require(between['status'] == 'PASS' and between['taken_before_checker'] is True and
                between['parents'] == read(REPORT / 'parent-files-after.json',True) and
                between['code'] == after_code['files'] and between['driver'] == after_code['driver'] and
                between['workflow'] == after_code['workflow'] and
                canonical(between['audit_materials']) == canonical(audit_material_bindings()) and
                between['acceptance'] == pin(REPORT / 'acceptance.json','acceptance.json'),
                'full-C-input-baseline-equals-after-C')
        guard('all_inputs_unchanged_separately_across_P_and_C',between_and_after)
    else:
        missing.append('inputs-after-producer-before-checker.json')
    output_after = None
    baseline = REPORT / 'producer-output-before-checker.json'
    if baseline.is_file():
        def output_unchanged():
            before = sealed(baseline,WF_SCHEMA + '.producer-output-before-checker')
            require(before['taken_before_checker'] is True and before['output'] is not None,'formed-P-output-baseline')
            observed = scan(OUTPUT)
            save('producer-output-after-checker.json',observed)
            require(observed == before['output'],'all-P-output-bytes-directories-hidden-tails-unchanged')
            return observed
        output_after = guard('producer_output_unchanged_by_checker',output_unchanged)
    else:
        missing.append('producer-output-before-checker.json')
        if OUTPUT.is_dir() and not OUTPUT.is_symlink():
            guard('diagnostic_output_inventory_saved',lambda:save('diagnostic-output-inventory.json',scan(OUTPUT)))
    status = 'FAIL' if errors else 'INCOMPLETE' if missing else 'PASS'
    save('preservation-result.json',seal(WF_SCHEMA,'preservation-result',{
        'status':status,'flags':flags,'errors':errors,'missing':missing,
        'acquired_parent_baselines':len(acquired),'output':output_after,
        'all_hidden_pending_and_orphan_payloads_retained':output_after is not None,
        'no_parent_file_renamed_trimmed_or_overwritten':len(acquired) == 16 and
            flags.get('all_parent_files_and_directories_unchanged') is True and
            all(flags.get('acquired_parent:' + role) is True for role in ROLES),
        'producer_and_checker_outcomes_checked_separately':True,**FALSE_ASSURANCE}))
    return 0 if status == 'PASS' else 1

def check_fixture_preservation():
    for stage in ('before-producer','before-checker','after-checker'):
        value = sealed(REPORT / ('selftest-fixtures-' + stage + '.json'),WF_SCHEMA + '.selftest-fixture-comparison')
        require(value['status'] == 'PASS' and value['stage'] == stage and value['errors'] == value['missing'] == [] and
            [row['label'] for row in value['fixtures']] == list(SELFTEST_REJECTIONS),
            'all-three-exact-fixture-comparisons')
        for row in value['fixtures']:
            require(row['present'] is True and row['state'] == 'COMPLETE' and row['unchanged'] is True and
                row['reason'] is None and row['root'] == str(fixture_root(row['label'])),
                'two-actual-completed-fixture-roots')
            for field in ('inventory','baseline'):
                payload_descriptor(REPORT,row[field])
            actual = read(REPORT / row['inventory']['file'],True)
            before = sealed(REPORT / row['baseline']['file'],WF_SCHEMA + '.selftest-fixture-baseline')
            require(canonical(actual) == canonical(before['inventory']),'exact-fixture-stage-baseline-join')
    receipt = sealed(REPORT / 'selftest-fixtures-archive-receipt.json',WF_SCHEMA + '.selftest-fixture-archive')
    require(receipt['status'] == 'PASS' and receipt['reason'] is None and receipt['container_present'] is True and
        receipt['fixture_container'] == str(FIXTURES) and receipt['both_completed_roots_unchanged'] is True and
        receipt['all_entries_and_explicit_directories_read'] is True and receipt['all_file_bytes_SHA_EOF_and_CRC_read'] is True and
        receipt['raw_fixtures_retained'] is True and receipt['excluded_entries'] == [] and
        receipt['silently_filtered_entries'] is False and receipt['partial_or_missing_roots_claimed_complete'] is False,
        'complete-fixture-archive-and-raw-preservation')
    for field in ('comparison','inventory','archive','readback_inventory','after_inventory'):
        payload_descriptor(REPORT,receipt[field])
    whole = read(REPORT / receipt['inventory']['file'],True)
    inventory_fields(whole)
    require(canonical(whole) == (REPORT / receipt['readback_inventory']['file']).read_bytes() ==
        (REPORT / receipt['after_inventory']['file']).read_bytes() == canonical(scan(FIXTURES)),
        'archive-all-entry-readback-and-current-full-fixture-inventory')
    expected_files,expected_directories = [],['C','P']
    for label in SELFTEST_REJECTIONS:
        letter = fixture_root(label).name
        before = sealed(REPORT / 'fixture-baselines' / (letter + '.json'),WF_SCHEMA + '.selftest-fixture-baseline')
        expected_files.extend({'file':letter + '/' + entry['file'],'bytes':entry['bytes'],'sha256':entry['sha256']}
            for entry in before['inventory']['files'])
        expected_directories.extend(letter + '/' + name for name in before['inventory']['directories'])
    require(canonical(whole) == canonical({'files':sorted(expected_files,key=lambda row:row['file']),
        'directories':sorted(expected_directories)}),'whole-archive-inventory-is-exact-union-of-both-fixture-baselines')

def payload_descriptor(root,entry):
    require(type(entry) is dict and set(entry) in ({'file','bytes','sha256'},
        {'file','bytes','sha256','dtype','shape'}),'payload-exact-descriptor')
    ordinary(entry['bytes'])
    require(type(entry['sha256']) is str and HEX.fullmatch(entry['sha256']) is not None,'payload-SHA-type')
    path = root / safe_name(entry['file'])
    require(root.resolve() in path.resolve().parents,'payload-descriptor-containment')
    if 'dtype' in entry:
        require(type(entry['dtype']) is str and type(entry['shape']) is list and
            all(type(value) is int and value >= 0 for value in entry['shape']),'typed-binary-shape')
    require(pin(path,entry['file']) == {key:entry[key] for key in ('file','bytes','sha256')},'payload-full-bytes-EOF')
    return path

def phase_receipt(prefix,phase,descriptor):
    telemetry_path = payload_descriptor(OUTPUT,descriptor)
    require(telemetry_path == OUTPUT / prefix / 'telemetry.json','phase-telemetry-exact-root-path')
    manifest_path = OUTPUT / prefix / 'manifest.json'
    manifest = sealed(manifest_path,SCHEMA + ('.final-manifest' if phase == 'final' else '.phase-manifest'))
    require(manifest['eof'] is True and type(manifest['files']) is list,'complete-phase-roster-EOF')
    names = []
    for entry in manifest['files']:
        require('/' not in safe_name(entry['file']),'phase-local-payload-name')
        payload_descriptor(manifest_path.parent,entry)
        names.append(entry['file'])
    require(names == sorted(set(names)) and 'telemetry.json' in names,'phase-complete-roster-names')
    telemetry = sealed(telemetry_path,SCHEMA + '.phase-telemetry')
    require(set(telemetry) == {'schema','sha256','phase','elapsed_seconds','process_ru_maxrss_kib',
        'proc_io_before','proc_io_after','payload_bytes','measurement_scope','eof'},'phase-telemetry-fields')
    require(telemetry['phase'] == phase and telemetry['eof'] is True and
        type(telemetry['elapsed_seconds']) in (int,float) and math.isfinite(telemetry['elapsed_seconds']) and
        telemetry['elapsed_seconds'] >= 0 and telemetry['measurement_scope'] ==
        'process-cumulative-rusage-and-proc-io;payload-bytes-are-output-only','phase-telemetry-types-and-scope')
    ordinary(telemetry['process_ru_maxrss_kib'])
    ordinary(telemetry['payload_bytes'])
    require(telemetry['payload_bytes'] == sum(entry['bytes'] for entry in manifest['files']
        if entry['file'] != 'telemetry.json'),'phase-payload-bytes-exclude-own-receipt')
    for name in ('proc_io_before','proc_io_after'):
        value = telemetry[name]
        require(value is None or type(value) is dict and set(value) == {'rchar','wchar','read_bytes','write_bytes'} and
            all(type(count) is int and count >= 0 for count in value.values()),'phase-IO-counter-types')
    return {'phase':phase,'manifest':pin(manifest_path,prefix + '/manifest.json'),
        'telemetry':copy.deepcopy(descriptor),'measurement':telemetry}

def character_rows(rows,width):
    require(type(rows) is list and len(rows) == 4,'four-character-rows')
    for character,row in enumerate(rows):
        require(type(row) is dict and set(row) == {'character','offset','trits','support','trit_counts'},
            'character-exact-fields')
        for key,wanted in (('character',character),('offset',character * width),('trits',width)):
            require(type(row[key]) is int and row[key] == wanted,'character-registered-coordinate')
        ordinary(row['support'],0,width)
        counts = row['trit_counts']
        require(type(counts) is list and len(counts) == 3 and all(type(count) is int and count >= 0 for count in counts) and
            sum(counts) == width and sum(counts[1:]) == row['support'],'character-all-trit-counts')
    return rows

def coverage_receipt(result,checked):
    selection = sealed(OUTPUT / 'selection/selection.json',SCHEMA + '.selection')
    readout = result['selection_readout']
    require(type(readout) is dict and set(readout) == {'failed_count','first_failed_index','first_failed_edge',
        'failed_indices','failed_edges','q_characters','lambda_characters','aux_values','score_support',
        'kappa_support','p1_equation_residual_support'},'selection-readout-exact-fields')
    count = ordinary(readout['failed_count'],0,54433)
    for key,name in (('failed_indices','failed-indices.u32'),('failed_edges','failed-edges.u32')):
        entry = readout[key]
        require(entry == selection[key] and entry['file'] == name and entry['dtype'] == 'u32le' and
            entry['shape'] == [count] and entry['bytes'] == 4 * count,'entire-failed-roster-descriptor')
        payload_descriptor(OUTPUT / 'selection/tree',entry)
    for key in ('failed_count','first_failed_index','first_failed_edge'):
        require(canonical(readout[key]) == canonical(selection[key]),'selection-complete-roster-metadata')
    if count:
        ordinary(readout['first_failed_index'],0,54432)
        ordinary(readout['first_failed_edge'],0,108863)
    else:
        require(readout['first_failed_index'] is None and readout['first_failed_edge'] is None,'empty-failed-roster-null')
    character_rows(readout['q_characters'],36288)
    character_rows(readout['lambda_characters'],12096)
    require(type(readout['aux_values']) is list and len(readout['aux_values']) == 2 and
        all(type(x) is int and 0 <= x <= 2 for x in readout['aux_values']),'two-current-auxiliary-values')
    score = readout['score_support']
    require(set(score) == {'total','by_tag'} and len(score['by_tag']) == 6 and
        all(type(value) is int and value >= 0 for value in score['by_tag']) and
        type(score['total']) is int and score['total'] == sum(score['by_tag']),'all-six-score-tags')
    kappa = readout['kappa_support']
    require(set(kappa) == {'total','degree0_by_character_tag','degree1_by_character_tag','aux_values'},
        'kappa-exact-support-fields')
    totals = 0
    for key in ('degree0_by_character_tag','degree1_by_character_tag'):
        require(type(kappa[key]) is list and len(kappa[key]) == 4 and all(type(row) is list and len(row) == 6 and
            all(type(value) is int and value >= 0 for value in row) for row in kappa[key]),'kappa-all4-by6-tags')
        totals += sum(sum(row) for row in kappa[key])
    require(type(kappa['aux_values']) is list and len(kappa['aux_values']) == 8 and
        all(type(value) is int and 0 <= value <= 2 for value in kappa['aux_values']),'kappa-shared-eight-aux-trits')
    require(type(kappa['total']) is int and kappa['total'] == totals + sum(value != 0 for value in kappa['aux_values']) and
        type(readout['p1_equation_residual_support']) is int and readout['p1_equation_residual_support'] == 0,
        'kappa-total-and-full8059-equation-residual')
    measurements = []
    require(set(result['selection_telemetry']) == {'section','cochain','tree'},'three-selection-telemetries')
    for phase in ('section','cochain','tree'):
        measurements.append(phase_receipt('selection/' + phase,phase,result['selection_telemetry'][phase]))
    candidates = result['candidates']
    require(type(candidates) is list and len(candidates) == result['selected_count'],'all-selected-candidate-readouts')
    accepted = 0
    rows = []
    for ordinal,candidate in enumerate(candidates):
        ordinary(ordinal,0,127)
        require(type(candidate['ordinal']) is int and candidate['ordinal'] == ordinal and
            type(candidate['selection_scalar']) is int and candidate['selection_scalar'] in (1,2),
            'ordered-selected-nonzero-scalar')
        prefix = 'candidates/' + f'{ordinal:06d}'
        witness = sealed(OUTPUT / prefix / 'witness.json',SCHEMA + '.witness')
        require(candidate['witness_sha256'] == digest(OUTPUT / prefix / 'witness.json') and
            witness['scalar'] == candidate['selection_scalar'],'candidate-own-witness-pin')
        if ordinal >= result['processed_candidates']:
            require(candidate['outcome'] == 'SKIPPED_AFTER_LINEAR' and candidate['raw_readout'] is None and
                candidate['phase_telemetry'] == {phase:None for phase in PHASES},'unprocessed-tail-has-no-measurement')
            rows.append(copy.deepcopy(candidate))
            continue
        require(set(candidate['phase_telemetry']) == set(PHASES),'six-processed-phase-telemetries')
        for phase in PHASES:
            path = prefix + ('/reduction' if phase == 'reduction' else '/e/' + phase)
            measurements.append(phase_receipt(path,phase,candidate['phase_telemetry'][phase]))
        require(candidate['candidate_manifest_sha256'] == digest(OUTPUT / prefix / 'manifest.json'),
            'candidate-decision-file-pin')
        raw = candidate['raw_readout']
        require(type(raw) is dict and set(raw) == {'epsilon_unrepaired','omega_unrepaired','repair_exponents',
            'raw_slp_letters','source_homogeneous_scalar','section_scalar','selection_scalar','alpha_support'},
            'raw-readout-fields')
        require(type(raw['epsilon_unrepaired']) is list and len(raw['epsilon_unrepaired']) == 2 and
            all(type(value) is int for value in raw['epsilon_unrepaired']),'raw-ordinary-epsilon')
        ordinary(raw['omega_unrepaired'],0,2)
        ordinary(raw['raw_slp_letters'])
        ordinary(raw['alpha_support'],0,8059)
        for key in ('source_homogeneous_scalar','section_scalar','selection_scalar'):
            ordinary(raw[key],0,2)
        require(raw['selection_scalar'] == candidate['selection_scalar'],'same-selection-scalar-readout')
        if witness['kind'] == 'chord':
            require(type(raw['repair_exponents']) is list and len(raw['repair_exponents']) == 3 and
                all(type(value) is int for value in raw['repair_exponents']) and raw['repair_exponents'][2] in (-1,0,1),
                'ordered-three-signed-repair-exponents')
        else:
            require(raw['repair_exponents'] is None,'auxiliary-has-no-chord-repair-exponents')
        if candidate['outcome'] == 'INDEPENDENT':
            ordinary(accepted,0,127)
            folder = 'rows/' + f'{accepted:06d}'
            require(candidate['row_manifest_sha256'] == digest(OUTPUT / folder / 'manifest.json'),
                'accepted-local-row-manifest')
            target = read(OUTPUT / folder / 'target.json',True)
            require(set(target) == {'parent_remainder_sha256','remainder_sha256','scalar'} and
                type(target['scalar']) is int and target['scalar'] in (0,1,2) and
                target['scalar'] == candidate['target_scalar'],'target-scalar-is-separate-coefficient')
            ordinary(candidate['lead'],0,48383)
            require(type(candidate['sigma']) is int and candidate['sigma'] in (1,2),'single-monic-normalization-scale')
            accepted += 1
        else:
            require(candidate['outcome'] == 'DEPENDENT' and all(candidate[key] is None for key in
                ('lead','sigma','target_scalar','row_manifest_sha256')),'dependent-typed-null-no-new-row')
        rows.append(copy.deepcopy(candidate))
    require(accepted == result['accepted_new_rows'],'all-accepted-row-readouts')
    measurements.append(phase_receipt('final','final',result['final_telemetry']))
    if result['kind'] == 'Separator':
        character_rows(result['final_lambda_characters'],12096)
    else:
        require(result['final_lambda_characters'] is None,'linear-final-lambda-support-not-applicable')
    save('coverage-receipt.json',seal(WF_SCHEMA,'coverage-receipt',{
        'status':'PASS','producer_result':pin(OUTPUT / 'result.json','output/result.json'),
        'checker_result':pin(REPORT / 'checker-result.json','checker-result.json'),
        'selection':pin(OUTPUT / 'selection/selection.json','output/selection/selection.json'),
        'selection_readout':copy.deepcopy(readout),'failed_roster_directory':'output/selection/tree',
        'candidates':rows,'phase_measurements':measurements,'final_lambda_characters':result['final_lambda_characters'],
        'final_lambda_file':None if result['lambda_sha256'] is None else pin(OUTPUT / 'final/lambda.bin','output/final/lambda.bin'),
        'new_lambda_oracle':None,'new_final_q_computed':False,'current_zero_support_is_operator_identity':False,
        'normalizer_convention':'sr(0)=0,sr(1)=1,sr(2)=-1; ordered repair x,y,central; mod54 then exact /18',
        'target_update_sign':'remainder_before - theta * normalized_row',
        'correction_word_factor_sign':'+sr(theta)','partial_physical_flush':False,
        'measurement_scope':'authenticated saved payloads and counters only; no new numerical replay',
        'phase_peak_is_process_cumulative':True,'old_success_suites':0,
        'rank':result['rank'],'generation':result['generation'],**FALSE_ASSURANCE}))

def registered_loader_receipt(side):
    registry = public_audit_registry()
    source_table = {entry['id']:entry for entry in registry['source_files']}
    rows = []
    for item in registry['old_loader_context']:
        if item['side'] != side:
            continue
        projected = {'name':item['name'],'byte_identical':True}
        for key in ('baseline','current'):
            region = item[key]
            source = source_table[region['source_id']]
            raw = audit_source_bytes({field:source[field] for field in ('file','bytes','sha256')})
            lines = raw.splitlines(keepends=True)
            offset = sum(len(line) for line in lines[:region['line_first'] - 1])
            prefix = 'checkout-sources/' if key == 'baseline' else ''
            projected[key] = {'file':prefix + source['file'],'offset':offset,
                'bytes':region['bytes'],'sha256':region['sha256']}
        rows.append(projected)
    require(len(rows) == 4,'all-four-current-side-loader-range-receipts')
    return rows


def check_parent_intake(acceptance,start,checked):
    batch = acceptance['batch_anchor']
    roots = read(REPORT / 'parent-roots.json',True)
    parent = Path(roots['batch-parent'])
    previous = sealed(parent / BATCH_FIELDS['start'],BATCH_SCHEMA + '.start')
    separator = sealed(parent / BATCH_FIELDS['separator'],BATCH_SCHEMA + '.separator')
    actual = sealed(OUTPUT / 'parent-intake.json',SCHEMA + '.parent-intake')
    expected = {'portable_acceptance_sha256':sha(canonical(portable_acceptance(acceptance))),
        'accepted_batch_anchor_sha256':sha(canonical(batch)),'old_anchor_head_sha256':acceptance['anchor']['head']['sha256'],
        'accepted_batch_head_sha256':batch['head']['sha256'],'accepted_batch_result_sha256':batch['result']['sha256'],
        'accepted_batch_checker_sha256':batch['checker']['sha256'],'upstream_completed_steps':64,
        'accepted_parent_batch_rows':128,'old_rank':1450,'rank':1578,'generation':8283,
        'state_head':batch['state_head'],'previous_target_remainder_sha256':previous['target_remainder_sha256'],
        'target_remainder_sha256':batch['target_remainder_sha256'],'lambda_sha256':batch['lambda_sha256'],
        'old_target_derivation_parents':97,'target_derivation_parents':225,
        'candidate_manifests_checked':128,'row_manifests_checked':128,'candidate_phase_manifests_checked':768,
        'checkpoints_checked':772,'invocations_checked':1,'old_loader_regions':registered_loader_receipt('P'),
        'old_snapshot_numeric_replays':0,'old_batch_numeric_replays':0,'original_rho2_directly_read':False}
    require(set(actual) == {'schema','sha256','direct_pairing',*expected} and
        canonical({key:actual[key] for key in expected}) == canonical(expected),
        'new-parent-intake-exact-public-metadata-and-old-loader-pins')
    pairing = actual['direct_pairing']
    require(type(pairing) is dict and set(pairing) == {'rows','row_pairings_sha256','lambda_pivots',
        'lambda_parent_remainder','lambda_new_remainder'} and
        canonical({key:pairing[key] for key in ('rows','lambda_pivots','lambda_parent_remainder','lambda_new_remainder')}) ==
        canonical({'rows':1578,'lambda_pivots':0,'lambda_parent_remainder':1,'lambda_new_remainder':1}) and
        type(pairing['row_pairings_sha256']) is str and HEX.fullmatch(pairing['row_pairings_sha256']) is not None,
        'new-parent-intake-all1578-rows-and-both-targets-pairing-receipt')
    for key,wanted in (('accepted_batch_anchor_sha256',sha(canonical(batch))),
            ('accepted_batch_head_sha256',batch['head']['sha256']),('accepted_batch_result_sha256',batch['result']['sha256']),
            ('accepted_batch_checker_sha256',batch['checker']['sha256']),('parent_intake_sha256',digest(OUTPUT / 'parent-intake.json')),
            ('accepted_parent_batch_rows',128),('accepted_parent_target_derivations',225),('rank',1578),('generation',8283),
            ('state_head',batch['state_head']),('target_remainder_sha256',batch['target_remainder_sha256']),
            ('selection_lambda_sha256',batch['lambda_sha256']),('previous_target_remainder_sha256',previous['target_remainder_sha256'])):
        require(canonical(start[key]) == canonical(wanted),'new-start-explicit-batch-parent-binding:' + key)
    require(canonical(start['accepted_target_derivation_parents']) ==
        canonical(separator['lambda_rho2']['accepted_target_derivation_parents']) and
        checked['parent_intake_sha256'] == digest(OUTPUT / 'parent-intake.json') and
        canonical(checked['checker_old_loader_regions']) == canonical(registered_loader_receipt('C')),
        'unchanged225-start-ancestry-and-checker-own-old-loader-certificate')
    return actual


def check_batch_observation(result,checked,acceptance):
    value = result['batch_observation']
    require(canonical(checked['batch_observation']) == canonical(value),
        'producer-checker-same-independent-batch-observation')
    require(type(value) is dict and set(value) == {'old','current','comparison_status','first_candidate',
        'failure_set_monotonicity_asserted','independence_rate_predicted'} and
        value['failure_set_monotonicity_asserted'] is False and value['independence_rate_predicted'] is False and
        type(value['comparison_status']) is str and value['comparison_status'] == 'OBSERVED',
        'completed-batch-observation-without-monotonicity-or-rate-claim')
    paths = read(REPORT / 'parent-roots.json',True)
    prior = sealed(Path(paths['batch-parent']) / BATCH_FIELDS['start'],BATCH_SCHEMA + '.start')
    batch = acceptance['batch_anchor']
    old = {'parent_role':'continuation','parent_artifact':ARTIFACTS['continuation'],
        'state_head':prior['state_head'],'lambda_sha256':prior['selection_lambda_sha256'],
        'selection_sha256':batch['selection']['sha256'],**batch['old_oracle']}
    selection = sealed(OUTPUT / 'selection/selection.json',SCHEMA + '.selection')
    current = {'parent_role':'batch-parent','parent_artifact':ARTIFACTS['batch-parent'],
        'state_head':batch['state_head'],'lambda_sha256':batch['lambda_sha256'],
        'selection_sha256':digest(OUTPUT / 'selection/selection.json'),
        **{key:selection[key] for key in ('failed_count','first_failed_index','first_failed_edge')}}
    require(canonical(value['old']) == canonical(old) and canonical(value['current']) == canonical(current),
        'old36274-70-125-and-new-full-oracle-bound-to-different-lambda-and-state')
    failed = ordinary(current['failed_count'],0,54433)
    if failed:
        ordinary(current['first_failed_index'],0,54432)
        ordinary(current['first_failed_edge'],0,108863)
    else:
        require(current['first_failed_index'] is None and current['first_failed_edge'] is None,
            'complete-zero-chord-failure-roster-null-first-fields')
    first = value['first_candidate']
    require(type(first) is dict and set(first) == {'status','conditions','ordinal','selection_scalar','raw_pairing',
        'expected_outcome','observed_outcome','matches_prediction'} and first['expected_outcome'] == 'INDEPENDENT',
        'conditional-first-candidate-exact-public-fields')
    if result['selected_count'] == 0:
        wanted = {'status':'NOT_APPLICABLE','conditions':{'candidate_exists':False,'first_processing_complete':False,
            'parent_span_zero':True,'derived_rho2_one':True,'raw_pairing_matches_nonzero_selection':None},
            'ordinal':None,'selection_scalar':None,'raw_pairing':None,'expected_outcome':'INDEPENDENT',
            'observed_outcome':None,'matches_prediction':None}
    else:
        require(ordinary(result['processed_candidates'],0,128) > 0,'completed-nonempty-selection-has-first-decision')
        witness = sealed(OUTPUT / 'candidates/000000/witness.json',SCHEMA + '.witness')
        reduction = sealed(OUTPUT / 'candidates/000000/reduction/reduction.json',SCHEMA + '.reduction')
        manifest = sealed(OUTPUT / 'candidates/000000/manifest.json',SCHEMA + '.candidate-manifest')
        scalar = ordinary(witness['scalar'],1,2)
        require(ordinary(reduction['selection_scalar'],1,2) == ordinary(reduction['raw_pairing'],1,2) == scalar,
            'conditional-first-raw-pairing-matches-nonzero-selection')
        wanted = {'status':'OBSERVED','conditions':{'candidate_exists':True,'first_processing_complete':True,
            'parent_span_zero':True,'derived_rho2_one':True,'raw_pairing_matches_nonzero_selection':True},
            'ordinal':0,'selection_scalar':scalar,'raw_pairing':scalar,'expected_outcome':'INDEPENDENT',
            'observed_outcome':manifest['outcome'],'matches_prediction':manifest['outcome'] == 'INDEPENDENT'}
        require(wanted['matches_prediction'] is True,'conditional-first-independent-under-all-measured-premises')
    require(canonical(first) == canonical(wanted),'conditional-first-observed-or-not-applicable-exact-types')
    save('batch-observation-receipt.json',seal(WF_SCHEMA,'batch-observation-receipt',{
        'status':'PASS','parent_intake':pin(OUTPUT / 'parent-intake.json','output/parent-intake.json'),
        'producer_result':pin(OUTPUT / 'result.json','output/result.json'),
        'checker_result':pin(REPORT / 'checker-result.json','checker-result.json'),'observation':value,
        'new_final_lambda_oracle_not_inferred':True,'independence_rate_predicted':False,**FALSE_ASSURANCE}))
    return value


def final_gate():
    audit_material_bindings()
    for label in ('metadata','producer-selftest','checker-selftest','producer','checker'):
        checked_execution(label)
    for label in ('metadata','producer-selftest','checker-selftest'):
        gate = sealed(REPORT / (label + '-gate.json'),WF_SCHEMA + '.selftest-gate')
        require(gate['status'] == 'PASS' and gate['old_success_suites'] == 0,'metadata16-and-both-two-literal-plus-parent-metadata-gates')
        for field in ('execution','selftest'):
            payload_descriptor(REPORT,gate[field])
    require((REPORT / 'checker-stdout.json').read_bytes() == (REPORT / 'checker-result.json').read_bytes(),
        'actual-checker-stdout-equals-external-report')
    require((REPORT / 'producer-stdout.json').read_bytes() == (OUTPUT / 'result.json').read_bytes(),
        'actual-producer-stdout-equals-complete-result')
    result = sealed(OUTPUT / 'result.json',SCHEMA + '.result')
    head = sealed(OUTPUT / 'HEAD',SCHEMA + '.head')
    final = sealed(OUTPUT / 'final/manifest.json',SCHEMA + '.final-manifest')
    separator = sealed(OUTPUT / 'final/separator.json',SCHEMA + '.separator')
    checked = sealed(REPORT / 'checker-result.json',SCHEMA + '.checker-result')
    acceptance = read(REPORT / 'acceptance.json',True)
    portable = portable_acceptance(acceptance)
    layout = sealed(OUTPUT / 'parent-layout.json',SCHEMA + '.parent-layout')
    require(canonical({key:value for key,value in layout.items() if key not in ('schema','sha256')}) ==
        canonical({'portable_acceptance_sha256':sha(canonical(portable)),
            **{key:portable[key] for key in ('parents','anchor','batch_anchor','code','runtime','registration')}}),
        'whole-portable-parent-layout-and-acceptance')
    source = sealed(OUTPUT / 'source.json',SCHEMA + '.source')
    require(source['producer'] == code_contract()['producer'] and source['checker'] == code_contract()['checker'] and
        source['retained_producer_dependencies'] == P_DEPS and source['retained_checker_dependencies'] == C_DEPS and
        source['data'] == DATA and source['runtime'] == runtime() and
        source['retained_TCB_independence_reproved'] is False,'complete-actual-source-runtime-closure')
    start = sealed(OUTPUT / 'start.json',SCHEMA + '.start')
    owner = sealed(OUTPUT / 'owner.json',SCHEMA + '.owner')
    check_parent_intake(acceptance,start,checked)
    selection_start = sealed(OUTPUT / 'selection/start.json',SCHEMA + '.selection-start')
    require(ordinary(selection_start['anchor_accepted_parent_batch_rows']) == 128,
        'new-selection-start-keeps-upstream64-and-accepted-parent128-separate')
    selection = sealed(OUTPUT / 'selection/selection.json',SCHEMA + '.selection')
    require(owner['registration'] == REGISTRATION and owner['portable_acceptance_sha256'] == sha(canonical(portable)) and
        owner['parent_layout_sha256'] == result['parent_layout_sha256'] == digest(OUTPUT / 'parent-layout.json'),
        'portable-owner-registration-and-layout')
    require(start['anchor_head_sha256'] == acceptance['anchor']['head']['sha256'] and
        start['anchor_result_sha256'] == acceptance['anchor']['result']['sha256'] and
        start['anchor_checker_sha256'] == acceptance['anchor']['checker']['sha256'] and
        start['rank'] == 1578 and start['generation'] == 8283 and start['anchor_completed_steps'] == 64 and
        type(start['external_e_attached']) is int and start['external_e_attached'] == 1,
        'original64-anchor-receipts-with-new1578-start-and-integer-E-count')
    for key,name in (('owner_sha256','owner.json'),('source_sha256','source.json'),('start_sha256','start.json'),
            ('selection_start_sha256','selection/start.json'),('selection_sha256','selection/selection.json')):
        require(result[key] == head[key] == final[key] == checked[key] == digest(OUTPUT / name),
            'all-complete-root-binding:' + key)
    require(checked['status'] == result['status'] == 'PASS' and checked['partial'] is False and
        checked['candidate'] is True and result['candidate'] is True and checked['cross_checked'] is True and
        result['cross_checked'] is False and checked['public_final_compared'] is True and
        checked['all_completed_payloads_and_json_compared'] is True and checked['durable_tail'] is None,
        'completed-full-comparison-candidate-scope')
    for value in (result,checked):
        require(value['grade2_member'] == value['grade2_nonmember'] == 'NOT_DECIDED' and
            value['full_A0'] is False and value['verified'] is False,'grade-and-verification-limits')
        for key in ('old_snapshot_numeric_replays','old_insert_numeric_replays','old_success_suites'):
            require(type(value[key]) is int and value[key] == 0,'no-old-arithmetic-replay:' + key)
    require(result['terminal'] in COMPLETED_TERMINALS and
        result['terminal'] == checked['terminal'] == head['terminal'] == final['terminal'],
        'exact-completed-terminal-not-workflow-status')
    for key in ('anchor_completed_steps','anchor_accepted_parent_batch_rows','selected_count','processed_candidates','dependent_candidates',
            'accepted_new_rows','rank','generation','state_head','target_remainder_sha256','lambda_sha256'):
        require(canonical(result[key]) == canonical(head[key]) == canonical(final[key]) == canonical(checked[key]),
            'all-terminal-state-count-fields:' + key)
    selected = ordinary(result['selected_count'],0,128)
    processed = ordinary(result['processed_candidates'],0,selected)
    dependent = ordinary(result['dependent_candidates'],0,processed)
    accepted = ordinary(result['accepted_new_rows'],0,processed)
    require(type(result['anchor_completed_steps']) is int and result['anchor_completed_steps'] == 64 and
        type(result['rank']) is int and result['rank'] == 1578 + accepted and
        type(result['generation']) is int and result['generation'] == 8283 + accepted and
        processed == dependent + accepted,'actual-rank-generation-and-independent-dependent-counts')
    skipped = result['skipped_after_linear']
    require(type(skipped) is list and all(type(value) is int for value in skipped) and
        skipped == list(range(processed,selected)) and selected == processed + len(skipped) and
        final['skipped_after_linear'] == skipped and (selected == 0 or accepted >= 1),'whole-selected-and-skipped-partition')
    require(checked['selection_phases_compared'] == ['section','cochain','tree'] and
        checked['candidate_phases_compared'] == [{'ordinal':i,'phases':PHASES} for i in range(processed)] and
        type(checked['candidate_decisions_compared']) is int and checked['candidate_decisions_compared'] == processed and
        type(checked['accepted_rows_compared']) is int and checked['accepted_rows_compared'] == accepted,
        'all-new-selection-candidate-decision-and-row-comparisons')
    require(result['head_sha256'] == checked['public_head_sha256'] == digest(OUTPUT / 'HEAD') and
        checked['producer_result_sha256'] == digest(OUTPUT / 'result.json') and
        result['final_manifest_sha256'] == head['final_manifest_sha256'] == checked['final_manifest_sha256'] ==
        digest(OUTPUT / 'final/manifest.json'),'complete-HEAD-result-final-file-hashes')
    require(checked['checker_source'] == code_contract()['checker'] and checked['runtime'] == runtime(),
        'actual-independent-checker-source-and-runtime')
    progress = sealed(OUTPUT / 'progress/HEAD',SCHEMA + '.progress-head')
    ordinary(progress['sequence'],0,771)
    require(checked['progress_head_sha256'] == digest(OUTPUT / 'progress/HEAD') and
        progress['kind'] == 'BatchReductionState' and progress['current_lambda_sha256'] is None and
        type(progress['sequence']) is int and progress['sequence'] == 3 + 6 * processed,
        'private-prefix-retains-its-distinct-type')
    checkpoint_path = OUTPUT / 'progress/checkpoints' / (progress['checkpoint_sha256'] + '.json')
    checkpoint = sealed(checkpoint_path,SCHEMA + '.checkpoint')
    require(digest(checkpoint_path) == progress['checkpoint_sha256'],'real-final-private-checkpoint-reference')
    for key in ('processed_candidates','dependent_candidates','accepted_new_rows','rank','generation'):
        require(type(progress[key]) is int and progress[key] == result[key] == checkpoint[key],
            'committed-private-prefix-final-count:' + key)
    require(progress['reduction_state_head'] == checkpoint['reduction_state_head'] == result['state_head'] and
        progress['target_remainder_sha256'] == checkpoint['target_remainder_sha256'] == result['target_remainder_sha256'],
        'private-final-physical-chain-and-target')
    require(result['new_lambda_oracle'] is head['new_lambda_oracle'] is separator['new_lambda_oracle'] is None and
        separator['source_lower_zero'] == 'NOT_ASSERTED' and separator['physical_lower_zero'] is True,
        'new-oracle-uncomputed-and-lower-type-boundary')
    require(result['kind'] == head['kind'] == final['kind'] == separator['kind'],'terminal-kind-equality')
    if result['terminal'] == 'LINEAR_MEMBERSHIP_CANDIDATE':
        require(result['kind'] == 'LinearMembershipCandidate' and processed > 0 and accepted > 0 and
            result['positive_readout'] == 'NEW_BATCH_SAME_WORD_ADAPTER_PENDING' and
            all(separator[key] is None for key in ('lambda_sha256','lambda_rho2','direct_pairing',
                'anchor_pairing_rows','final_pairing_rows')) and result['lambda_sha256'] is None and
            result['final_lambda_characters'] is None and not (OUTPUT / 'final/lambda.bin').exists(),
            'linear-typed-null-with-positive-adapter-pending')
    else:
        require(result['kind'] == 'Separator' and result['positive_readout'] == 'NOT_APPLICABLE' and
            processed == selected and skipped == [] and
            separator['lambda_sha256'] == result['lambda_sha256'] == digest(OUTPUT / 'final/lambda.bin'),
            'completed-separator-all-candidates')
        pairing = separator['direct_pairing']
        require(set(pairing) == {'rows','row_pairings_sha256','lambda_pivots','lambda_parent_remainder','lambda_new_remainder'} and
            pairing['rows'] == result['rank'] and pairing['lambda_pivots'] == 0 and
            pairing['lambda_parent_remainder'] == pairing['lambda_new_remainder'] == 1 and
            separator['anchor_pairing_rows'] == 1578 and separator['final_pairing_rows'] == result['rank'],
            'direct-all-row-and-both-target-receipt')
        derived = separator['lambda_rho2']
        require(set(derived) == {'mode','value','original_rho2_directly_read','original_rho2_packed_sha256',
            'accepted_target_derivation_parents','identity_convention','anchor_completed_steps','anchor_accepted_parent_batch_rows','new_batch_target_steps_executed'} and
            derived['mode'] == 'derived' and derived['value'] == 1 and derived['original_rho2_directly_read'] is False and
            derived['original_rho2_packed_sha256'] == start['original_rho2_packed_sha256'] and
            derived['anchor_completed_steps'] == 64 and ordinary(derived['anchor_accepted_parent_batch_rows']) == 128 and
            derived['new_batch_target_steps_executed'] == accepted and
            len(start['accepted_target_derivation_parents']) == 225 and
            derived['accepted_target_derivation_parents'][:225] == start['accepted_target_derivation_parents'] and
            len(derived['accepted_target_derivation_parents']) == 225 + accepted,'retained225-plus-actual-new-batch-target-identities')
        if result['terminal'] == 'COMPLETE_ZERO_CANDIDATE':
            require(selected == processed == accepted == dependent == 0 and selection['terminal'] == 'COMPLETE_ZERO_CANDIDATE' and
                result['lambda_sha256'] == start['selection_lambda_sha256'],'same-current-lambda-complete-zero')
        else:
            require(selected > 0 and accepted > 0 and selection['terminal'] == 'VIOLATION_CANDIDATE',
                'nonempty-completed-batch')
    require(digest(OUTPUT / 'final/target-remainder.bin') == result['target_remainder_sha256'],
        'actual-final-packed-target-hash')
    invocations = result['invocations']
    normal_paths = []
    for file in sorted((OUTPUT / 'invocations').iterdir(),key=lambda p:p.name):
        require(file.is_file() and not file.is_symlink(),'new-invocation-file-type')
        if re.fullmatch(r'\.[0-9a-f]{32}\.json\.pending-[0-9a-f]{32}',file.name):
            continue
        require(re.fullmatch(r'[0-9a-f]{32}\.json',file.name) is not None,'new-invocation-registered-name')
        normal_paths.append(file)
    require(len(normal_paths) == len(invocations) == 1 and
        invocations[0] == pin(normal_paths[0],normal_paths[0].relative_to(OUTPUT).as_posix()) and
        invocations[0]['sha256'] == result['invocation_sha256'],'one-fresh-explicit-invocation')
    invocation = sealed(normal_paths[0],SCHEMA + '.invocation')
    require(invocation['resume'] is False and invocation['launch'] == launch() and
        invocation['host_paths'] == {'parents':read(REPORT / 'parent-roots.json',True),
            'acceptance':str(REPORT / 'acceptance.json'),'output':str(OUTPUT)} and
        invocation['acceptance_sha256'] == digest(REPORT / 'acceptance.json') and
        invocation['portable_acceptance_sha256'] == sha(canonical(portable)) and
        canonical(invocation['registration']) == canonical(REGISTRATION),'fresh-launch-and-paths-kept-outside-owner')
    for key,wanted in (('batch_size',128),('max_batches',1),('max_seconds',5400),('max_memory_mib',7168),
            ('processed_candidates_before',0),('accepted_new_rows_before',0)):
        require(type(invocation[key]) is int and invocation[key] == wanted,'fresh-registered-invocation:' + key)
    require(invocation['progress_head_before_sha256'] is None and invocation['physical_head_before_sha256'] is None,
        'fresh-has-no-before-HEAD')
    preserved = sealed(REPORT / 'preservation-result.json',WF_SCHEMA + '.preservation-result')
    require(preserved['status'] == 'PASS' and preserved['errors'] == preserved['missing'] == [] and
        preserved['acquired_parent_baselines'] == 16 and all(value is True for value in preserved['flags'].values()),
        'all-input-output-and-source-before-after-gates')
    require(preserved['flags']['both_complete_fixture_subtrees_and_entire_archive_unchanged'] is True,
        'all-selftest-fixtures-explicit-preservation-gate')
    require(preserved['flags']['all_static_audit_receipts_registry_and_history_copies_unchanged'] is True and
        preserved['flags']['all_inputs_unchanged_separately_across_P_and_C'] is True,
        'both-static-audits-and-history-explicit-before-P-between-and-after-C-gates')
    check_fixture_preservation()
    restoration = sealed(REPORT / 'batch-parent-restoration-result.json',WF_SCHEMA + '.batch-parent-restoration-result')
    require(restoration['status'] == 'PASS' and restoration['reason'] is None and
        type(restoration['created_count']) is int and restoration['created_count'] == 36 and
        restoration['all_expected_files_and_directories_reread'] is True and
        preserved['flags']['batch_parent_transport_files_unchanged_and_only_registered_directories'] is True,
        'new-parent-complete-authenticated36-restoration-and-all-ending-preservation')
    payload_descriptor(REPORT,restoration['plan'])
    expected_preservation = {'parents_before_sha256':digest(OUTPUT / 'inputs/parents-before.json'),
        'parents_after_sha256':digest(OUTPUT / 'inputs/parents-after.json'),
        'code_before_sha256':digest(OUTPUT / 'inputs/code-before.json'),
        'code_after_sha256':digest(OUTPUT / 'inputs/code-after.json'),
        'portable_acceptance_sha256':sha(canonical(portable)),'acceptance_sha256':digest(REPORT / 'acceptance.json'),
        'all_parent_files_and_directories_unchanged':True,'all_code_and_raw_unchanged':True,'acceptance_unchanged':True}
    require(canonical(result['input_preservation']) == canonical(expected_preservation) and
        canonical(checked['input_preservation']) == canonical(expected_preservation),'P-C-own-input-preservation-receipts')
    require((OUTPUT / 'inputs/parents-before.json').read_bytes() == (REPORT / 'parent-files-before.json').read_bytes() ==
        (OUTPUT / 'inputs/parents-after.json').read_bytes() == (REPORT / 'parent-files-after.json').read_bytes() and
        (OUTPUT / 'inputs/code-before.json').read_bytes() == canonical(code_union(code_contract())) ==
        (OUTPUT / 'inputs/code-after.json').read_bytes(),'independent-full-input-inventory-bytes')
    check_batch_observation(result,checked,acceptance)
    coverage_receipt(result,checked)
    return result,checked

def final_mode():
    status,error,result,checked = 'PASS',None,None,None
    try:
        result,checked = final_gate()
    except BaseException as exc:
        status,error = 'FAIL',type(exc).__name__ + ':' + str(exc)
    # Full REPORT may grow; only the two complete fixture subtrees must remain exactly equal.
    inventory,inventory_error = None,None
    try:
        inventory = scan(REPORT)
        save('envelope-inventory-before-run.json',inventory)
    except BaseException as exc:
        inventory_error = type(exc).__name__ + ':' + str(exc)
        status,error = 'FAIL',(error + ';' if error else '') + 'envelope-scan:' + inventory_error
    executions = {}
    for label in ('metadata','producer-selftest','checker-selftest','producer','checker'):
        file = REPORT / 'execution' / (label + '-result.json')
        executions[label] = {'receipt':pin(file,'execution/' + label + '-result.json'),'value':read(file,True)} if file.is_file() else None
    source = REPORT / 'source-receipt.json'
    acceptance = REPORT / 'acceptance.json'
    preservation = REPORT / 'preservation-result.json'
    producer_inventory = read(REPORT / 'producer-output-after-checker.json',True) if (REPORT / 'producer-output-after-checker.json').is_file() else None
    parent_pin = {role:copy.deepcopy(spec) for role,spec in ARTIFACTS.items()}
    save('run-receipt.json',seal(WF_SCHEMA,'run-receipt',{
        'status':status,'reason':error,'launch':launch(),'registration':REGISTRATION,
        'source_receipt':pin(source,'source-receipt.json') if source.is_file() else None,
        'arithmetic_selftest_inheritance':pin(REPORT / 'arithmetic-selftest-inheritance.json',
            'arithmetic-selftest-inheritance.json') if (REPORT / 'arithmetic-selftest-inheritance.json').is_file() else None,
        'shared_tcb':pin(REPORT / 'shared-tcb.json','shared-tcb.json') if (REPORT / 'shared-tcb.json').is_file() else None,
        'audit_material_receipts':{name:pin(REPORT / name,name) if (REPORT / name).is_file() else None
            for name in ('audit-region-registry.json','audit-materials-before.json','audit-materials-after.json')},
        'audit_history_sources_are_nonexecuting_evidence':True,
        'arithmetic_selftest_inherited_from':HISTORICAL_ARITHMETIC_TESTS['arithmetic_selftest_inherited_from'],
        'old_mathematical_suites_rerun':0,'historical_payload_reacquired_in_this_run':False,
        'current_run_call_coverage':'NOT_MEASURED','kernel_third_independence_claimed':False,
        'code':code_contract(),'runtime':observed_runtime(),'accepted_artifacts':parent_pin,
        'acceptance':pin(acceptance,'acceptance.json') if acceptance.is_file() else None,
        'preservation':pin(preservation,'preservation-result.json') if preservation.is_file() else None,
        'executions':executions,'fresh_producer_invocations_registered':1,'old_success_suites_rerun':0,
        'metadata_regression_cases_registered':16,'metadata_regression_base':'d972-r07-fixed-lambda-cycle-batch-v1',
        'new_selftest_groups_registered':{'producer':3,'checker':3},
        'selftest_group_scopes':['two-k128-literal-groups','one-parent1578-metadata-group'],
        'new_selftest_rejections_registered':SELFTEST_REJECTIONS,
        'selftest_fixture_roots':{label:str(fixture_root(label)) for label in SELFTEST_REJECTIONS},
        'selftest_fixture_comparisons':{stage:pin(REPORT / ('selftest-fixtures-' + stage + '.json'),
            'selftest-fixtures-' + stage + '.json') if (REPORT / ('selftest-fixtures-' + stage + '.json')).is_file() else None
            for stage in ('before-producer','before-checker','after-checker')},
        'selftest_fixture_archive_receipt':pin(REPORT / 'selftest-fixtures-archive-receipt.json','selftest-fixtures-archive-receipt.json')
            if (REPORT / 'selftest-fixtures-archive-receipt.json').is_file() else None,
        'selftest_fixture_archive_files':{name:pin(REPORT / name,name) if (REPORT / name).is_file() and not (REPORT / name).is_symlink() else None
            for name in ('selftest-fixtures.zip','selftest-fixtures-inventory.json',
                'selftest-fixtures-archive-readback.json','selftest-fixtures-after-archive.json')},
        'producer_result':pin(OUTPUT / 'result.json','output/result.json') if (OUTPUT / 'result.json').is_file() else None,
        'checker_result':pin(REPORT / 'checker-result.json','checker-result.json') if (REPORT / 'checker-result.json').is_file() else None,
        'parent_intake':pin(OUTPUT / 'parent-intake.json','output/parent-intake.json') if (OUTPUT / 'parent-intake.json').is_file() else None,
        'accepted_batch_anchor':None if not acceptance.is_file() else read(acceptance,True)['batch_anchor'],
        'batch_observation':None if result is None else result['batch_observation'],
        'batch_observation_receipt':pin(REPORT / 'batch-observation-receipt.json','batch-observation-receipt.json')
            if (REPORT / 'batch-observation-receipt.json').is_file() else None,
        'batch_parent_restoration':pin(REPORT / 'batch-parent-restoration-result.json','batch-parent-restoration-result.json')
            if (REPORT / 'batch-parent-restoration-result.json').is_file() else None,
        'batch_parent_envelope_intake':pin(REPORT / 'batch-parent-envelope-intake.json','batch-parent-envelope-intake.json')
            if (REPORT / 'batch-parent-envelope-intake.json').is_file() else None,
        'producer_resource_or_failure_diagnostics':{name:pin(OUTPUT / name,'output/' + name)
            for name in ('resource-stop.json','rejected.json') if (OUTPUT / name).is_file()},
        'early_diagnostic_null_is_not_a_completed_observation':True,
        'first_independent_prediction_is_conditional':True,'failure_set_monotonicity_asserted':False,
        'independence_rate_predicted':False,
        'current':None if result is None else {key:result[key] for key in ('terminal','kind','anchor_completed_steps','anchor_accepted_parent_batch_rows',
            'selected_count','processed_candidates','dependent_candidates','accepted_new_rows','skipped_after_linear',
            'rank','generation','state_head','target_remainder_sha256','lambda_sha256','positive_readout')},
        'coverage':pin(REPORT / 'coverage-receipt.json','coverage-receipt.json') if (REPORT / 'coverage-receipt.json').is_file() else None,
        'producer_output':None if producer_inventory is None else {'files':len(producer_inventory['files']),
            'directories':len(producer_inventory['directories']),'bytes':sum(row['bytes'] for row in producer_inventory['files'])},
        'envelope_payload_before_this_receipt':None if inventory is None else {
            'files':len(inventory['files']),'directories':len(inventory['directories']),
            'bytes':sum(row['bytes'] for row in inventory['files']),
            'inventory':pin(REPORT / 'envelope-inventory-before-run.json','envelope-inventory-before-run.json'),
            'excludes':['envelope-inventory-before-run.json','run-receipt.json']},
        'envelope_inventory_error':inventory_error,
        'producer_full_output_includes_hidden_diagnostics':producer_inventory is not None,
        'all_upstream_archives_and_entries_retained_on_runner':preservation.is_file() and
            read(preservation,True)['acquired_parent_baselines'] == 16 and
            all(read(preservation,True)['flags'].get('acquired_parent:' + role) is True for role in ROLES),
        'upstream_archives_uploaded_again':False,'upstream_payloads_referenced_by_live_pins_and_full_inventories':True,
        'candidate_and_diagnostics_upload_the_same_envelope_root':True,
        'new_final_q_computed':False,'new_lambda_oracle':None,
        'selection_lambda1578_oracle_is_separate_from_new_final_lambda_oracle':True,
        '96_control_elapsed_seconds_used_as_batch_measurement':False,
        'same_word_adapter_for_batch_rows':None if result is None else result['positive_readout'],
        'grade2_member':'NOT_DECIDED','grade2_nonmember':'NOT_DECIDED','full_A0':False,
        'candidate':status == 'PASS','cross_checked':status == 'PASS','verified':False,
        'cross_check_scope':'new fixed-lambda selection and every completed new candidate/row/final payload; retained TCB limits unchanged',
        'workshop_CV9':'PENDING'}))
    with open(os.environ['GITHUB_OUTPUT'],'a',encoding='utf-8') as stream:
        stream.write('candidate=' + ('true' if status == 'PASS' else 'false') + '\n')
    return 0 if status == 'PASS' else 1

def main():
    mode = sys.argv[1]
    try:
        if mode == 'capture':
            capture_sources()
        elif mode == 'source':
            source_mode()
        elif mode == 'audit':
            audit_mode()
        elif mode == 'live':
            live_mode()
        elif mode == 'intake':
            intake_mode()
        elif mode == 'metadata-canary':
            metadata_canary()
        elif mode == 'execute':
            return execute(sys.argv[2])
        elif mode == 'test-gate':
            test_gate(sys.argv[2])
        elif mode == 'post-producer':
            post_producer()
        elif mode == 'fixtures':
            return fixture_archive_mode()
        elif mode == 'preserve':
            return preservation_mode()
        elif mode == 'final':
            return final_mode()
        else:
            raise ValueError('unregistered-driver-mode')
        return 0
    except BaseException as error:
        reason = type(error).__name__ + ':' + str(error)
        traceback.print_exc()
        label = mode + ('-' + sys.argv[2] if len(sys.argv) > 2 else '')
        save('driver-failure-' + label + '.json',seal(WF_SCHEMA,'driver-failure',{
            'status':'FAIL','mode':label,'reason':reason,'utc':utc(),**FALSE_ASSURANCE}))
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
