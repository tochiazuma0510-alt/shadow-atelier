"""
Bootstrap loader for Dolgushev et al.'s "Package GT" (search/thirdparty/PackageGT/).

WHY THIS FILE EXISTS (Windows-only technical workaround, not a mathematical
or algorithmic change):

  Windows reserves the device name "AUX" (case-insensitively, with or
  without extension) at the Win32 API level. The package's own source file
  Aux.py -- which PaB.py imports via "from Aux import ..." -- therefore
  cannot be opened by CPython's native-Windows build under ANY filename
  spelled "Aux.py"/"AUX.py"/etc, even with a \\?\ extended-length prefix.
  (MSYS/Git-Bash tools such as cp/cat CAN read/write it, which is how the
  byte-identical copy got into the repo at all -- see
  search/thirdparty/PackageGT/Aux.py, sha256 verified equal to the vault
  original.)

  This loader works around the OS restriction WITHOUT editing a single
  byte of the author's code:
    1. It reads the *content* of Aux.py (via a byte-identical sibling copy
       AuxSafe.py, which is not a reserved name and so is a normal file
       Windows Python can open) and execs that source into a module object
       registered in sys.modules under the exact name "Aux".
    2. It then loads PaB.py (and NotUsed.py) straight from their real,
       untouched paths in search/thirdparty/PackageGT/ via importlib. Their
       "from Aux import ..." statements resolve against the sys.modules
       cache from step 1 and never touch the filesystem for "Aux".

  PaB.py, NotUsed.py and Aux.py in search/thirdparty/PackageGT/ are left
  100% byte-identical to the zip (see pent_thirdparty_gt_20260731.json for
  hashes). AuxSafe.py is a verbatim copy of Aux.py under a Windows-legal
  filename, produced by `diff`-verified `cp` -- not a rewrite.

Usage:
    import sys
    sys.path.insert(0, r"...\search\probe\wac_v1")
    from gt_thirdparty_bootstrap import PaB, NotUsed
    PaB.penta(...)
"""

import os
import sys
import types
import importlib.util
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parents[2] / "thirdparty" / "PackageGT"
AUX_SAFE = PKG_DIR / "AuxSafe.py"
PAB_PY = PKG_DIR / "PaB.py"
NOTUSED_PY = PKG_DIR / "NotUsed.py"


def _load_aux_into_sys_modules():
    if "Aux" in sys.modules:
        return sys.modules["Aux"]
    src = AUX_SAFE.read_text(encoding="utf-8")
    mod = types.ModuleType("Aux")
    mod.__file__ = str(AUX_SAFE)  # provenance breadcrumb; content == Aux.py
    exec(compile(src, str(AUX_SAFE), "exec"), mod.__dict__)
    sys.modules["Aux"] = mod
    return mod


def _load_from_path(name, path: Path, seed_globals=None):
    # PaB.py's module-level code does load_now('subGrPB4_org35') etc. with a
    # RELATIVE filename (author's own code, untouched) -- so cwd must be
    # PKG_DIR for the duration of the exec. We restore cwd afterwards.
    # PaB.py's module-level code also calls input(...) once; the caller of
    # this bootstrap is responsible for feeding stdin (e.g. echo no | ...)
    # so that call returns immediately instead of hanging.
    cwd0 = os.getcwd()
    try:
        os.chdir(PKG_DIR)
        spec = importlib.util.spec_from_file_location(name, str(path))
        mod = importlib.util.module_from_spec(spec)
        if seed_globals:
            # NotUsed.py has no imports of its own -- the author wrote it to
            # be pasted/run in the SAME session as PaB.py (it references
            # PaB's names directly, e.g. N_PB3, Nord, gcd, permut). We seed
            # its module namespace with PaB's, matching that intended usage
            # exactly (not a code edit -- NotUsed.py's text is untouched).
            # Dunder keys (__name__, __loader__, __spec__, ...) are excluded
            # so NotUsed keeps its own module identity.
            mod.__dict__.update(
                {k: v for k, v in seed_globals.items() if not k.startswith("__")}
            )
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    finally:
        os.chdir(cwd0)
    return mod


_load_aux_into_sys_modules()
PaB = _load_from_path("PaB", PAB_PY)
NotUsed = _load_from_path("NotUsed", NOTUSED_PY, seed_globals=PaB.__dict__)
