#!/usr/bin/env python3
"""Guarded compact-row successor of the adopted Task458 actual owner."""
from __future__ import annotations
import ast
import hashlib
from pathlib import Path

BASE = Path(__file__).with_name("d972_r07_zero_base_a5_a6_compiler_v6.py")
BASE_BYTES = 2342
BASE_SHA256 = "32cbc1a8e1faea0d4dc7a88a41a2ad3b535e7b2fd94b73ff286d78001262b96c"
V5_BYTES = 2810
V5_SHA256 = "df659de36c8c27255836c6da06812ab8af61185566e98210f46f32ae75fb4cd2"
GENERATED_V6_BYTES = 59382
GENERATED_V6_SHA256 = "83b31959a0c35bdeb1e2569e0ee384b116ed6ed0b7d57e9c363cecdc29fcfe87"
COMPACT_SOURCE = ("search/d972_r07_a0_compact_pc_invariant_owner_v1.py", 68222,
                  "be17be107103a218123cd0e1eb8455377ca2b52a2e54ec629f3744ad4c2d32f9")
COMPACT_COUNT = 44
COMPACT_SHA256 = "7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8"
TASK193_OWNER = "task193-v5-firewall"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _guarded_body() -> bytes:
    base = BASE.read_bytes()
    if len(base) != BASE_BYTES or _sha(base) != BASE_SHA256:
        raise SystemExit("Task458 v6 producer pin drift")
    tree = ast.parse(base)
    changes = next((ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                    and isinstance(n.targets[0], ast.Name)
                    and n.targets[0].id == "changes"), None)
    v5 = BASE.with_name("d972_r07_zero_base_a5_a6_compiler_v5.py")
    v5raw = v5.read_bytes()
    if len(v5raw) != V5_BYTES or _sha(v5raw) != V5_SHA256:
        raise SystemExit("Task456 v5 producer pin drift")
    v5tree = ast.parse(v5raw)
    v5changes = next((ast.literal_eval(n.value) for n in v5tree.body if isinstance(n, ast.Assign)
                      and isinstance(n.targets[0], ast.Name)
                      and n.targets[0].id == "changes"), None)
    v5counts = next((ast.literal_eval(n.value) for n in v5tree.body if isinstance(n, ast.Assign)
                     and isinstance(n.targets[0], ast.Name)
                     and n.targets[0].id == "counts"), None)
    v4name = next((n.args[0].value for n in ast.walk(v5tree)
                   if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                   and n.func.attr == "with_name" and n.args
                   and isinstance(n.args[0], ast.Constant)), None)
    v6counts = next((ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                     and isinstance(n.targets[0], ast.Name)
                     and n.targets[0].id == "counts"), None)
    if (not isinstance(changes, list) or not isinstance(v5changes, list) or
            not isinstance(v5counts, list) or not isinstance(v6counts, list) or
            not isinstance(v4name, str)):
        raise SystemExit("Task458 v6 transform manifest")
    x = v5.with_name(v4name).read_bytes()
    for (old, new), count in zip(v5changes, v5counts):
        if x.count(old) != count or (new and x.count(new) != 0):
            raise SystemExit("Task458 v6 transform cardinality")
        x = x.replace(old, new)
    if len(x) != 59232 or _sha(x) != "c478b41db2ae1aae96178e2d4d6d26489b9c7de3611fada93f1f061bf1fab3d8":
        raise SystemExit("Task456 v5 generated body drift")
    for (old, new), count in zip(changes, v6counts):
        if x.count(old) != count or (new and x.count(new) != 0):
            raise SystemExit("Task458 v6 transform cardinality")
        x = x.replace(old, new)
    if len(x) != GENERATED_V6_BYTES or _sha(x) != GENERATED_V6_SHA256:
        raise SystemExit("Task458 v6 generated body drift")
    replacements = [
        (b"d972-r07-zero-base-a5-a6-compiler/v6", b"d972-r07-compact-direct-relator-a5-a6-positive-owner/v2"),
        (b"R07_ZERO_BASE_A5_A6_COMPILER_V6", b"R07_COMPACT_DIRECT_RELATOR_A5_A6_POSITIVE_V2"),
        (b"UNKNOWN_INCOMPLETE:K_conjugation_closure_not_implemented", b"UNKNOWN_INCOMPLETE:compact_direct_span_exhausted"),
        (b"ROWS = 6441", b"ROWS = 44"),
        (b"args.rss_bytes == 8_000_000_000", b"args.rss_bytes == 5_700_000_000"),
        (b"default=8_000_000_000", b"default=5_700_000_000"),
        (b"authority = helper.AuthorityAdapter(args, meter)\n        runtime = helper.Runtime(authority, meter)\n        boundary = helper.BoundaryLedger(runtime, meter)",
         b"original_authority = helper.AuthorityAdapter(args, meter)\n        runtime = helper.Runtime(original_authority, meter)\n        boundary = helper.BoundaryLedger(runtime, meter)\n        authority = CompactAuthorityProxy(original_authority)"),
    ]
    for old, new in replacements:
        if x.count(old) != 1 or x.count(new) != 0:
            raise SystemExit("compact v2 replacement cardinality")
        x = x.replace(old, new)
    marker = b"from __future__ import annotations\n"
    proxy = b'''\nCOMPACT_SOURCE = ("search/d972_r07_a0_compact_pc_invariant_owner_v1.py", 68222,\n                  "be17be107103a218123cd0e1eb8455377ca2b52a2e54ec629f3744ad4c2d32f9")\nCOMPACT_COUNT = 44\nCOMPACT_SHA256 = "7612682d024b61f873928ad122c9a5d7462c812a6633112f08706cda4412b6c8"\n\ndef _compact_rows():\n    path = ROOT / COMPACT_SOURCE[0]\n    raw = path.read_bytes()\n    if len(raw) != COMPACT_SOURCE[1] or hashlib.sha256(raw).hexdigest() != COMPACT_SOURCE[2]:\n        raise InputStop("compact:task411_pin")\n    ns = {"__name__": "task411_compact_producer", "__file__": str(path)}\n    exec(compile(raw, COMPACT_SOURCE[0], "exec"), ns, ns)\n    pres = ns["compact"](ns["load"](ns["JOINT"]), ns["load"](ns["Q3"]))\n    if pres.get("compact_relator_count") != COMPACT_COUNT or pres.get("relators_sha256") != COMPACT_SHA256:\n        raise InputStop("compact:roster")\n    return tuple({"word": list(word)} for word in pres["relators"])\n\nclass CompactAuthorityProxy:\n    def __init__(self, delegate):\n        self._delegate = delegate\n        self.rows = _compact_rows()\n        self.compact_relator_roster = {"owner": "Task411", "count": COMPACT_COUNT,\n                                       "sha256": COMPACT_SHA256}\n    def __getattr__(self, name):\n        return getattr(self._delegate, name)\n\n'''
    proxy = proxy.replace(b"return tuple({\"word\": list(word)} for word in pres[\"relators\"])" ,
                          b"return tuple(types.MappingProxyType({\"word\": tuple(word)}) for word in pres[\"relators\"])" )
    proxy = proxy.replace(b"    def __getattr__(self, name):", b"    def __setattr__(self, name, value):\n        if name in self.__dict__: raise AttributeError(\"compact proxy is read-only\")\n        if name not in (\"_delegate\", \"rows\", \"compact_relator_roster\"): raise AttributeError(\"compact proxy is read-only\")\n        object.__setattr__(self, name, value)\n    def __getattr__(self, name):")
    if x.count(marker) != 1:
        raise SystemExit("compact v2 future marker")
    x = x.replace(marker, marker + proxy, 1)
    split = x.rsplit(b"if __name__ == \"__main__\":", 1)
    if len(split) != 2:
        raise SystemExit("compact v2 main marker")
    trailer = b'''_compact_seal = seal\ndef seal(value):\n    if isinstance(value, dict):\n        value["compact_relator_roster"] = {"owner": "Task411", "count": COMPACT_COUNT,\n                                           "sha256": COMPACT_SHA256}\n    return _compact_seal(value)\n\n'''
    return split[0] + trailer + b"if __name__ == \"__main__\":" + split[1]


_BODY = _guarded_body()
GENERATED_V2_BYTES = 61341
GENERATED_V2_SHA256 = "289dbff63af59daec0478bdc6eee376b711c4b944fee08d671b3e10a323b5539"
if len(_BODY) != GENERATED_V2_BYTES or _sha(_BODY) != GENERATED_V2_SHA256:
    raise SystemExit("compact v2 generated body drift")
exec(compile(_BODY, str(Path(__file__).resolve()), "exec"), globals(), globals())
